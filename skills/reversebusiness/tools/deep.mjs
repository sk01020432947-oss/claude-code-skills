// 정밀 모드에서 쓰는 풀이 도구. 의존성 없음, 네트워크를 쓰지 않는다.
//   - 흐름 읽기: 페이지가 요청을 보내려던 호스트 이름을 결제사, 분석 도구, 영상 호스팅 같은 종류로 나눈다.
//   - 속 읽기: 이미 내려온 스크립트의 글에서 화면 경로 이름, 결제 모듈 이름, 가격과 요금제처럼 보이는 글자를 찾는다.
//     찾은 주소는 이름만 적는다. 절대 불러 보지 않는다.
//   - 약관: 서비스 코드 분석을 금지하는 조항이 있는지 낱말로 찾아본다.
import { PRICE, scrub } from './from-rea.mjs';

const uniq = (a) => [...new Set(a)];

// ---------- 호스트 이름으로 바깥 서비스 알아보기 ----------
const SERVICES = [
  ['payment', '토스페이먼츠', /(^|\.)tosspayments\.com$/], ['payment', '포트원', /(^|\.)(portone\.io|iamport\.(kr|co))$/], ['payment', 'Stripe', /(^|\.)stripe\.(com|network)$/],
  ['payment', 'PayPal', /(^|\.)(paypal\.com|paypalobjects\.com)$/], ['payment', 'Paddle', /(^|\.)paddle\.com$/], ['payment', 'Lemon Squeezy', /(^|\.)lemonsqueezy\.com$/],
  ['payment', 'Polar', /(^|\.)polar\.sh$/], ['payment', '카카오페이', /(^|\.)kakaopay\.com$/], ['payment', '네이버페이', /(^|\.)pay\.naver\.com$/], ['payment', 'KG이니시스', /(^|\.)inicis\.com$/],
  ['payment', 'NICE페이', /(^|\.)nicepay\.co\.kr$/], ['payment', 'KCP', /(^|\.)kcp\.co\.kr$/], ['payment', 'Gumroad', /(^|\.)gumroad\.com$/],
  ['analytics', 'Google 태그', /(^|\.)(googletagmanager\.com|google-analytics\.com|analytics\.google\.com)$/], ['analytics', 'Google 광고', /(^|\.)(doubleclick\.net|googlesyndication\.com|googleadservices\.com)$/],
  ['analytics', 'Meta 픽셀', /(^|\.)(facebook\.net|connect\.facebook\.com|facebook\.com)$/], ['analytics', 'Microsoft Clarity', /(^|\.)clarity\.ms$/], ['analytics', 'Hotjar', /(^|\.)hotjar\.(com|io)$/],
  ['analytics', 'Amplitude', /(^|\.)amplitude\.com$/], ['analytics', 'Mixpanel', /(^|\.)mixpanel\.com$/], ['analytics', 'PostHog', /(^|\.)posthog\.com$/], ['analytics', 'Plausible', /(^|\.)plausible\.io$/],
  ['analytics', 'Segment', /(^|\.)segment\.(io|com)$/], ['analytics', '네이버 분석', /(^|\.)wcs\.naver\.(net|com)$/], ['analytics', 'Sentry', /(^|\.)sentry\.io$/], ['analytics', 'Vercel 분석', /(^|\.)(vercel-insights\.com|vitals\.vercel-insights\.com)$/],
  ['video', 'Vimeo', /(^|\.)(vimeo\.com|vimeocdn\.com)$/], ['video', 'YouTube', /(^|\.)(youtube\.com|youtube-nocookie\.com|ytimg\.com|googlevideo\.com)$/], ['video', 'Wistia', /(^|\.)wistia\.(com|net)$/],
  ['video', 'Mux', /(^|\.)mux\.com$/], ['video', 'Cloudflare Stream', /(^|\.)(cloudflarestream\.com|videodelivery\.net)$/], ['video', 'Bunny', /(^|\.)(b-cdn\.net|bunnycdn\.com|mediadelivery\.net)$/],
  ['auth', 'Firebase 로그인', /(^|\.)(identitytoolkit\.googleapis\.com|securetoken\.googleapis\.com|firebaseapp\.com)$/], ['auth', 'Auth0', /(^|\.)auth0\.com$/], ['auth', 'Clerk', /(^|\.)(clerk\.com|clerk\.dev|accounts\.dev)$/],
  ['auth', 'Google 로그인', /(^|\.)accounts\.google\.com$/], ['auth', '카카오 로그인', /(^|\.)kauth\.kakao\.com$/], ['auth', '네이버 로그인', /(^|\.)nid\.naver\.com$/],
  ['data', 'Firebase', /(^|\.)(firestore\.googleapis\.com|firebaseio\.com|firebasestorage\.googleapis\.com|firebaseinstallations\.googleapis\.com|firebase\.googleapis\.com)$/], ['data', 'Supabase', /(^|\.)supabase\.(co|in)$/],
  ['data', 'AWS', /(^|\.)amazonaws\.com$/], ['data', 'Azure', /(^|\.)(azurewebsites\.net|azureedge\.net|windows\.net|azurestaticapps\.net)$/], ['data', 'Google Cloud', /(^|\.)(cloudfunctions\.net|run\.app|storage\.googleapis\.com)$/],
  ['data', 'Algolia', /(^|\.)(algolia\.net|algolianet\.com)$/], ['data', 'Sanity', /(^|\.)sanity\.io$/], ['data', 'Contentful', /(^|\.)contentful\.com$/],
  ['chat', '채널톡', /(^|\.)channel\.io$/], ['chat', 'Intercom', /(^|\.)(intercom\.io|intercomcdn\.com)$/], ['chat', 'Zendesk', /(^|\.)(zendesk\.com|zdassets\.com)$/], ['chat', 'Crisp', /(^|\.)crisp\.chat$/], ['chat', 'tawk.to', /(^|\.)tawk\.to$/],
  ['font', 'Google 글꼴', /(^|\.)(fonts\.googleapis\.com|fonts\.gstatic\.com)$/], ['font', 'Adobe 글꼴', /(^|\.)typekit\.net$/],
  ['cdn', 'jsDelivr', /(^|\.)jsdelivr\.net$/], ['cdn', 'unpkg', /(^|\.)unpkg\.com$/], ['cdn', 'cdnjs', /(^|\.)cdnjs\.cloudflare\.com$/], ['cdn', 'CloudFront', /(^|\.)cloudfront\.net$/],
];
export const SERVICE_KINDS = { payment: '결제', analytics: '분석과 광고', video: '영상', auth: '로그인', data: '데이터와 서버', chat: '상담 채팅', font: '글꼴', cdn: 'CDN', other: '그 밖' };

// hosts: [{ host, count, sent }] 또는 호스트 이름 배열. 같은 사이트(own)는 뺀다.
export function classifyHosts(hosts, ownHost = '') {
  const own = String(ownHost).replace(/^www\./, '');
  const groups = new Map();
  for (const h of hosts) {
    const host = String(typeof h === 'string' ? h : h.host || '').toLowerCase();
    if (!host || host.replace(/^www\./, '') === own || /^(127\.0\.0\.1|localhost)$/.test(host)) continue;
    const hit = SERVICES.find(([, , re]) => re.test(host));
    const kind = hit ? hit[0] : 'other';
    const name = hit ? hit[1] : host;
    const key = `${kind}|${name}`;
    const g = groups.get(key) || { kind, name, hosts: [], sent: false };
    if (!g.hosts.includes(host)) g.hosts.push(host);
    if (typeof h !== 'string' && h.sent) g.sent = true;
    groups.set(key, g);
  }
  const order = Object.keys(SERVICE_KINDS);
  return [...groups.values()].sort((a, b) => order.indexOf(a.kind) - order.indexOf(b.kind) || a.name.localeCompare(b.name));
}

// ---------- 스크립트 글에서 흔적 찾기 ----------
const PAY_IN_CODE = [
  ['토스페이먼츠', /tosspayments/i], ['포트원', /portone|iamport|IMP\.request_pay/i], ['Stripe', /js\.stripe\.com|loadStripe|Stripe\(/], ['PayPal', /paypal\.com\/sdk|paypal\.Buttons|PayPalScriptProvider|paypalobjects/i],
  ['Paddle', /Paddle\.(Setup|Checkout|Initialize)|cdn\.paddle\.com/], ['Lemon Squeezy', /lemonsqueezy/i], ['Polar', /polar\.sh/i], ['카카오페이', /kakaopay/i], ['네이버페이', /naverpay|pay\.naver\.com/i],
  ['KG이니시스', /inicis/i], ['NICE페이', /nicepay/i], ['KCP', /\bkcp\b|kcp\.co\.kr/i],
];
const ASSET = /\.(js|mjs|css|png|jpe?g|webp|gif|svg|ico|json|map|woff2?|ttf|mp4|webm|txt|xml)$/i;
const routeOk = (p) => p.length >= 2 && p.length <= 60 && !ASSET.test(p) && !/^\/(static|assets|_next|_nuxt|node_modules|images?|img|fonts?|media|locales?|i18n)\//i.test(p) && !/^\/\//.test(p) && /[a-z]/i.test(p);
const toNumber = (raw) => {
  const s = String(raw).replace(/[_,]/g, '');
  const m = /^(\d+(?:\.\d+)?)e(\d+)$/i.exec(s);
  const n = m ? Number(m[1]) * 10 ** Number(m[2]) : Number(s);
  return Number.isFinite(n) ? n : NaN;
};

// scripts: [{ url, text }]. 글은 훑기만 하고 돌려주지 않는다. 돌려주는 것은 짧은 이름과 숫자뿐이다.
export function scanScripts(scripts) {
  const routes = new Set(), endpoints = new Set(), payments = new Set(), prices = new Set(), plans = new Set();
  let bytes = 0;
  for (const s of scripts) {
    const text = String(s.text || '');
    bytes += text.length;
    for (const m of text.matchAll(/(?:\bpath|\bto|\bhref|\broute|\bpathname|\bredirect(?:To)?)\s*[:=]\s*["'`](\/[A-Za-z0-9_\-/:.]{1,60})["'`]/g)) if (routeOk(m[1])) routes.add(m[1]);
    for (const m of text.matchAll(/(?:navigate|push|replace|redirect)\(\s*["'`](\/[A-Za-z0-9_\-/:.]{1,60})["'`]/g)) if (routeOk(m[1])) routes.add(m[1]);
    for (const m of text.matchAll(/["'`](\/api\/[A-Za-z0-9_\-/:.]{1,60})["'`]/g)) endpoints.add(m[1]);
    for (const [name, re] of PAY_IN_CODE) if (re.test(text)) payments.add(name);
    for (const m of text.matchAll(/\b(?:price|amount|cost|fee|salePrice|originalPrice|earlyBirdPrice|regularPrice)[A-Za-z]*["']?\s*[:=]\s*["'`]?(\d[\d_,.]*(?:e\d)?)/gi)) {
      const n = toNumber(m[1]);
      if (n >= 100 && n <= 100000000) prices.add(String(n));
    }
    for (const m of text.matchAll(/["'`]([^"'`\n\\]{0,20}(?:₩|￦|\$|€)\s?\d[^"'`\n\\]{0,16}|[^"'`\n\\]{0,12}\d{1,3}(?:,\d{3})+\s?원[^"'`\n\\]{0,6})["'`]/g)) { const hit = PRICE.exec(m[1]); if (hit) prices.add(scrub(hit[0])); }
    for (const m of text.matchAll(/\b(?:plan|tier|membership|product|course|package)(?:Name|_name|Title|_title|Label)["']?\s*[:=]\s*["'`]([^"'`\n\\]{2,28})["'`]/g)) plans.add(scrub(m[1]));
  }
  const take = (set, n) => [...set].slice(0, n);
  return { files: scripts.length, bytes, routes: take(routes, 60).sort(), endpoints: take(endpoints, 20).sort(), payments: [...payments], prices: take(prices, 12), plans: take(plans, 10) };
}

// REA analyze-web-bundle 근거에서 경로 이름과 호출 주소의 수를 뽑는다.
export function readBundleFacts(record) {
  const n = (record && record.normalized_result) || {};
  const inv = n.route_inventory || {};
  const routes = uniq([...(inv.routes || []).map((r) => r.path), ...((n.observations || {}).routes || []).map((r) => r.value)].filter((p) => typeof p === 'string' && p.startsWith('/') && routeOk(p) || p === '/'));
  return {
    evidence_id: record ? record.evidence_id || '' : '',
    scripts: (n.capture || {}).scripts_observed || 0,
    parsed: (n.completeness || {}).parsed_scripts || 0,
    status: (n.completeness || {}).status || '',
    routes: routes.map(scrub).slice(0, 60),
    endpoints: ((n.observations || {}).endpoints || []).length,
  };
}

// 로그인 뒤나 결제 쪽으로 보이는 경로 이름인지.
const BEHIND = /^\/(dashboard|account|accounts|my|mypage|my-page|me|profile|settings|admin|checkout|payment|payments|billing|orders?|cart|purchase|subscription|learn|classroom|lecture|player|library|members?)(\/|$)/i;
export const looksBehindLogin = (p) => BEHIND.test(String(p));

// ---------- 약관이 코드 분석을 금지하는지 ----------
const FORBID = /(역공학|역설계|리버스\s?엔지니어링|디컴파일|역컴파일|디스어셈블|소스\s?코드[^.。\n]{0,20}(분석|추출|해독)|reverse[\s-]?engineer|decompil|disassembl)/i;
export function termsForbidCodeReading(text) {
  const m = FORBID.exec(String(text || ''));
  return { forbids: !!m, word: m ? scrub(m[1]).slice(0, 20) : '' };
}
