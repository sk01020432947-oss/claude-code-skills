// 구역 종류마다 우리 말로 붙인 이름과 "여기에 무엇을 쓸지" 안내.
// 수집기(뼈대 이름), 새 사이트 만들기(make-site.mjs), 적용 계획(apply-plan.mjs)이 함께 쓴다.
// 여기 있는 글은 전부 이 도구의 말이다. 어떤 사이트의 문구도 들어 있지 않다.

export const KIND_NAME = { media: '영상이나 그림 구역', headline: '큰 제목 구역', price: '가격 구역', nav: '이동 메뉴', numbers: '숫자로 보여 주는 구역', list: '목록 구역', notice: '안내 구역', quotes: '후기 구역', faq: '자주 묻는 물음', cta: '신청 단추 구역', footer: '꼬리말', text: '글 구역' };
export const KINDS = Object.keys(KIND_NAME);
export const ROLE_NAME = { attract: '데려오는 층', value: '가치를 주는 층', pay: '돈 받는 층', return: '다시 오게 하는 층', other: '그 밖' };

// 구역에 무엇을 쓸지. 한 줄씩, 만드는 사람에게 하는 말이다.
export const KIND_WRITE = {
  nav: '내 이름과, 이 페이지 안에서 옮겨 갈 곳 서너 개.',
  media: '무엇을 얻는지 한눈에 보여 주는 한 장면. 직접 만든 영상이나 그림만 씁니다.',
  headline: '누가 무엇을 얻는지 한 문장으로 쓴 약속과, 그 아래 한 줄 설명.',
  price: '지금 가격, 가격에 들어 있는 것, 가격이 바뀐다면 그 날짜, 신청 단추, 환불 안내 한 줄.',
  numbers: '근거가 있는 숫자 세 개와 그 숫자가 무엇인지. 근거가 없으면 이 구역을 지웁니다.',
  list: '주는 것을 항목으로 나눠 한 줄씩. 항목마다 받는 사람이 얻는 결과를 씁니다.',
  notice: '일정, 조건, 바뀔 수 있는 것을 숨기지 않고 한 상자에 모읍니다.',
  quotes: '실제로 받은 말만, 허락을 받고 씁니다. 지어낸 후기는 넣지 않습니다. 아직 없으면 이 구역을 비워 둡니다.',
  faq: '사기 전에 가장 많이 걱정하는 것 서너 개와 솔직한 답.',
  cta: '마지막으로 한 번 더 권하는 한 문장과 신청 단추.',
  footer: '사업자 정보, 약관, 환불 정책, 문의할 곳.',
  text: '이 자리에서 꼭 말해야 하는 것 하나를 짧은 제목과 두세 문장으로.',
};

export const kindName = (k) => KIND_NAME[k] || KIND_NAME.text;
export const kindWrite = (k) => KIND_WRITE[k] || KIND_WRITE.text;
export const roleName = (r) => ROLE_NAME[r] || ROLE_NAME.other;

// 대상의 이름으로 볼 글자들: 리포트의 대상 이름, 주소의 호스트, 그리고 source.json 의 브랜드 이름과 도메인.
// 띄어쓰기와 기호를 뗀 모양으로 견준다 ("AI CITY", "ai-city", "AiCity" 를 같게 본다).
const squash = (t) => String(t).toLowerCase().replace(/[^a-z0-9가-힣぀-ヿ一-鿿]+/g, '');
const COPY_WORDS = /(클론|clone|카피|copycat|짝퉁)/i;
export function targetNames(report, source = null) {
  const out = new Set();
  const add = (s) => { const q = squash(s); if (q.length >= 3) out.add(q); };
  const t = (report && report.meta && report.meta.target) || {};
  try {
    const host = new URL(String(t.url || '')).hostname.replace(/^www\./, '');
    if (host && !/^(localhost|\d+\.\d+\.\d+\.\d+)$/.test(host)) {
      add(host);
      const labels = host.split('.');
      // 가운데 이름: example.com 의 example, shop.example.co.kr 의 example
      const core = labels.length >= 3 && labels[labels.length - 2].length <= 3 ? labels[labels.length - 3] : labels[labels.length - 2];
      if (core && core.length >= 4) add(core);
    }
  } catch { /* 주소가 아니면 건너뛴다 */ }
  if (source) for (const n of [...(source.names || []), ...(source.domains || [])]) add(n);
  return [...out];
}
// 글에 대상의 이름이나 "클론" 같은 말이 들어 있으면 그 까닭을 돌려준다. 없으면 빈 글자.
export function nameProblem(text, names) {
  const s = String(text || '');
  if (COPY_WORDS.test(s)) return '클론, 카피 같은 말';
  const q = squash(s);
  return names.some((n) => q.includes(n)) ? '대상의 이름' : '';
}
