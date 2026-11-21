#!/usr/bin/env node
// reversebusiness report.json 검사기. 의존성 없음.
// 사용: node check-report.mjs <report.json> [--dissect-only]
//   --dissect-only  해부만 한 리포트를 검사한다. 내 버전 칸(6번)이 비어 있어도 통과한다.
// 오류가 있으면 종료 코드 1. 경고만 있으면 0.
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

// observed 관찰: 화면이나 흐름에서 직접 봄. inferred 추정. unknown 모름. code 코드 흔적: 내려온 코드 안에서만 본 것.
const STATUS = ['observed', 'inferred', 'unknown', 'code'];
// 근거를 어디서 봤는지: page 화면에서, flow 흐름(펼치기와 요청)에서, code 코드에서
const SEEN = ['page', 'flow', 'code'];
const DEPTHS = ['surface', 'flow', 'code'];
const STEP_STATES = ['done', 'partial', 'skipped', 'blocked', 'failed'];
const EV_TYPES = ['url', 'screen', 'doc', 'file', 'run'];
const STAGES = ['arrive', 'first_value', 'signup', 'payment', 'return', 'other'];
const ROLES = ['attract', 'value', 'pay', 'return', 'other'];
const KINDS = ['web-service', 'desktop-app', 'mobile-app', 'local-tool', 'other'];
// checked: 약관 조항까지 읽음. robots-only: robots.txt 까지만 확인하고 약관은 아직 못 읽음. not-found: 둘 다 찾지 못함.
const TERMS = ['checked', 'robots-only', 'not-applicable', 'not-found'];
const COPY_WORDS = /(클론|clone|카피|copycat|짝퉁)/i;

const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);
const isStr = (v) => typeof v === 'string';
const filled = (v) => isStr(v) && v.trim().length > 0;

export function checkReport(r, { dissectOnly = false } = {}) {
  const errors = [];
  const warnings = [];
  const err = (where, msg) => errors.push(`${where}: ${msg}`);
  const warn = (where, msg) => warnings.push(`${where}: ${msg}`);
  const counts = { observed: 0, inferred: 0, unknown: 0, code: 0 };
  let myVersion = 'filled';

  if (!isObj(r)) return { errors: ['report: JSON 객체가 아니에요'], warnings, counts, myVersion };
  if (r.schema !== 'rebiz/report@1') err('schema', '"rebiz/report@1" 이어야 해요');

  // ---- meta
  const m = r.meta;
  const t = isObj(m) ? m.target : null;
  if (!isObj(m)) err('meta', '없어요');
  else {
    if (!isObj(t)) err('meta.target', '없어요');
    else {
      if (!filled(t.name)) err('meta.target.name', '대상 이름이 비었어요');
      if (!KINDS.includes(t.kind)) err('meta.target.kind', `${KINDS.join(' | ')} 중 하나`);
      if (!['own', 'third-party'].includes(t.relation)) err('meta.target.relation', 'own 또는 third-party');
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(m.analyzed_at || '')) err('meta.analyzed_at', 'YYYY-MM-DD 날짜가 필요해요');
    if (!filled(m.analyst)) err('meta.analyst', '분석한 주체가 비었어요');
    if (!filled(m.scope)) err('meta.scope', '무엇을 봤고 무엇을 안 봤는지 적어 주세요');
    if (!Array.isArray(m.method) || m.method.length === 0) err('meta.method', '본 방법을 한 줄 이상 적어 주세요');
    if (!filled(m.one_line)) err('meta.one_line', '한 줄 요약이 비었어요');
    if (!isObj(m.terms) || !TERMS.includes(m.terms.status)) err('meta.terms.status', `${TERMS.join(' | ')} 중 하나`);
    else {
      if (!filled(m.terms.note)) err('meta.terms.note', '이용약관 확인 결과를 한 줄 적어 주세요');
      if (isObj(t) && t.relation === 'third-party' && m.terms.status === 'not-applicable')
        err('meta.terms.status', '남의 서비스는 not-applicable 을 쓸 수 없어요. 약관을 확인하고 checked 또는 not-found');
      if (m.terms.status === 'robots-only') warn('meta.terms.status', 'robots.txt 까지만 확인한 상태예요. 이용약관을 읽은 뒤 checked 로 바꾸고 note 에 한 줄 적어 주세요');
    }
  }
  const relation = isObj(t) ? t.relation : null;

  // ---- evidence ledger
  const ids = new Set();
  const evType = new Map();
  const evSeen = new Map();
  if (!Array.isArray(r.evidence)) err('evidence', '배열이어야 해요');
  else {
    r.evidence.forEach((e, i) => {
      const w = `evidence[${i}]`;
      if (!isObj(e)) return err(w, '객체가 아니에요');
      if (!/^E\d+$/.test(e.id || '')) err(w, 'id 는 E1, E2 같은 모양');
      else if (ids.has(e.id)) err(w, `id ${e.id} 가 겹쳐요`);
      else { ids.add(e.id); evType.set(e.id, e.type); evSeen.set(e.id, e.seen || 'page'); }
      if (e.seen !== undefined && !SEEN.includes(e.seen)) err(w, `seen 은 ${SEEN.join(' | ')} 중 하나`);
      if (!EV_TYPES.includes(e.type)) err(w, `type 은 ${EV_TYPES.join(' | ')} 중 하나`);
      if (!filled(e.ref)) err(w, 'ref 가 비었어요');
      if (e.type === 'url' && filled(e.ref) && !/^https?:\/\//.test(e.ref)) err(w, 'url 근거는 http(s) 주소여야 해요');
      if (e.type === 'file' && relation === 'third-party') err(w, '남의 서비스에는 file(소스 파일) 근거를 쓸 수 없어요');
      if (!filled(e.note)) warn(w, 'note 에 무엇을 봤는지 적어 두면 좋아요');
    });
  }
  const used = new Set();

  const checkRefs = (where, refs, status) => {
    if (!Array.isArray(refs)) return err(where, 'evidence 는 배열');
    for (const id of refs) {
      if (!ids.has(id)) err(where, `근거 ${id} 가 장부에 없어요`);
      else used.add(id);
    }
    if ((status === 'observed' || status === 'inferred') && refs.length === 0)
      err(where, `${status === 'observed' ? '관찰' : '추정'}에는 근거가 1개 이상 필요해요. 없으면 unknown(모름)으로`);
    const known = refs.filter((id) => ids.has(id));
    // 코드에서만 본 것은 관찰이 아니다. 화면에서 확인되기 전에는 "지금 그렇다"고 쓸 수 없다.
    if (status === 'observed' && known.length > 0 && known.every((id) => evSeen.get(id) === 'code'))
      err(where, '코드에서만 본 것은 관찰(observed)이 아니라 코드 흔적(status: code)으로 적어요. 화면이나 흐름에서 본 근거가 있어야 관찰이에요');
    if (status === 'code' && !known.some((id) => evSeen.get(id) === 'code'))
      err(where, '코드 흔적(status: code)에는 코드에서 본 근거(seen: code)가 1개 이상 필요해요');
  };
  const checkClaim = (where, c) => {
    if (!isObj(c)) return err(where, '객체가 아니에요');
    if (!filled(c.text)) err(where, 'text 가 비었어요');
    if (!STATUS.includes(c.status)) return err(where, `status 는 ${STATUS.join(' | ')} 중 하나`);
    counts[c.status] += 1;
    checkRefs(where, c.evidence, c.status);
  };
  const checkClaims = (where, arr, { allowEmpty = false } = {}) => {
    if (!Array.isArray(arr)) return err(where, '배열이어야 해요');
    if (!allowEmpty && arr.length === 0) err(where, '한 줄 이상 필요해요. 모르면 status unknown 으로 한 줄');
    arr.forEach((c, i) => checkClaim(`${where}[${i}]`, c));
  };

  // terms evidence
  if (isObj(m) && isObj(m.terms) && Array.isArray(m.terms.evidence)) checkRefs('meta.terms.evidence', m.terms.evidence, null);

  const s = r.sections;
  if (!isObj(s)) {
    err('sections', '없어요');
    return { errors, warnings, counts, myVersion };
  }

  // ---- 1 money
  if (!isObj(s.money)) err('sections.money', '1번 칸이 없어요');
  else {
    checkClaims('money.customer', s.money.customer);
    checkClaims('money.problem', s.money.problem);
    checkClaims('money.price', s.money.price);
    checkClaims('money.revenue', s.money.revenue, { allowEmpty: true });
    (Array.isArray(s.money.revenue) ? s.money.revenue : []).forEach((c, i) => {
      const w = `money.revenue[${i}]`;
      if (!isObj(c)) return;
      if (c.status !== 'observed') err(w, '수익 숫자는 공개된 근거가 있는 관찰만 적어요. 추정, 모름, 코드 흔적이면 지우고 unknowns 에 올리기');
      const pub = (c.evidence || []).some((id) => ['url', 'doc'].includes(evType.get(id)));
      if (c.status === 'observed' && !pub) err(w, '수익 숫자에는 공개 출처(url 또는 doc 근거)가 필요해요');
    });
  }

  // ---- 2 flow
  if (!isObj(s.flow) || !Array.isArray(s.flow.steps)) err('sections.flow.steps', '2번 칸이 없어요');
  else {
    const seen = new Set();
    s.flow.steps.forEach((c, i) => {
      const w = `flow.steps[${i}]`;
      checkClaim(w, c);
      if (!isObj(c)) return;
      if (!STAGES.includes(c.stage)) err(w, `stage 는 ${STAGES.join(' | ')} 중 하나`);
      else seen.add(c.stage);
      if (!filled(c.label)) err(w, 'label 이 비었어요');
    });
    for (const need of ['signup', 'first_value', 'payment'])
      if (!seen.has(need)) err('flow.steps', `${need} 단계가 없어요. 없거나 모르면 그렇게 한 줄`);
  }

  // ---- 흐름에서 본 바깥 서비스 (선택)
  if (isObj(s.flow) && s.flow.services !== undefined) {
    if (!Array.isArray(s.flow.services)) err('flow.services', '배열이어야 해요');
    else s.flow.services.forEach((sv, i) => {
      const w = `flow.services[${i}]`;
      if (!isObj(sv)) return err(w, '객체가 아니에요');
      if (!filled(sv.kind)) err(w, 'kind 가 비었어요');
      if (!Array.isArray(sv.names) || sv.names.length === 0) err(w, 'names 가 비었어요');
      if (!['flow', 'code'].includes(sv.seen)) err(w, 'seen 은 flow | code 중 하나');
      checkRefs(w, sv.evidence, null);
      if (Array.isArray(sv.evidence) && sv.seen === 'flow' && sv.evidence.filter((id) => ids.has(id)).every((id) => evSeen.get(id) === 'code')) err(w, '흐름에서 봤다고 적으려면 흐름에서 본 근거가 있어야 해요');
    });
  }

  // ---- 3 map
  if (!isObj(s.map) || !Array.isArray(s.map.screens)) err('sections.map.screens', '3번 칸이 없어요');
  else {
    if (s.map.screens.length === 0) err('map.screens', '화면이 하나도 없어요');
    s.map.screens.forEach((sc, i) => {
      const w = `map.screens[${i}]`;
      if (!isObj(sc)) return err(w, '객체가 아니에요');
      if (!filled(sc.name)) err(w, 'name 이 비었어요');
      if (!filled(sc.purpose)) err(w, 'purpose 가 비었어요');
      if (!Array.isArray(sc.features)) err(w, 'features 는 배열');
      if (!STATUS.includes(sc.status)) return err(w, `status 는 ${STATUS.join(' | ')} 중 하나`);
      counts[sc.status] += 1;
      checkRefs(w, sc.evidence, sc.status);
    });
  }

  // ---- 4 tech
  if (!isObj(s.tech) || !Array.isArray(s.tech.items)) err('sections.tech.items', '4번 칸이 없어요');
  else {
    if (s.tech.items.length === 0) err('tech.items', '한 줄 이상 필요해요. 모르면 unknown 으로');
    s.tech.items.forEach((c, i) => {
      checkClaim(`tech.items[${i}]`, c);
      if (isObj(c) && !filled(c.layer)) err(`tech.items[${i}]`, 'layer 가 비었어요');
    });
  }

  // ---- 5 unknowns
  if (!Array.isArray(s.unknowns)) err('sections.unknowns', '5번 칸의 모르는 것 목록이 없어요');
  else {
    s.unknowns.forEach((u, i) => {
      const w = `unknowns[${i}]`;
      if (!isObj(u)) return err(w, '객체가 아니에요');
      if (!filled(u.question)) err(w, 'question 이 비었어요');
      if (!filled(u.why)) err(w, 'why(왜 모르는지)가 비었어요');
    });
    if (s.unknowns.length === 0 && counts.unknown === 0)
      warn('unknowns', '모르는 것이 0개예요. 밖에서 본 분석이라면 다시 확인해 보세요');
  }

  // ---- 6 my_version
  const mv = s.my_version;
  // 해부만 할 때: 내 버전 칸을 하나도 쓰지 않았으면 "아직 안 씀"으로 두고 넘어간다. 쓰기 시작했으면 끝까지 검사한다.
  const blank = !isObj(mv) || (!filled(mv.working_name) && !filled(mv.same_problem) && !filled(mv.who) && !(Array.isArray(mv.mvp) && mv.mvp.length) && !(Array.isArray(mv.not_taken) && mv.not_taken.length) && !(Array.isArray(mv.differences) && mv.differences.some((d) => isObj(d) && (filled(d.title) || filled(d.text)))));
  if (blank) myVersion = 'empty';
  if (dissectOnly && blank) { /* 아직 안 씀 */ } else if (!isObj(mv)) err('sections.my_version', '6번 칸이 없어요');
  else {
    for (const k of ['working_name', 'same_problem', 'who']) if (!filled(mv[k])) err(`my_version.${k}`, '비었어요');
    if (!Array.isArray(mv.mvp) || mv.mvp.length === 0) err('my_version.mvp', '최소 기능을 한 줄 이상');
    if (!Array.isArray(mv.differences) || mv.differences.length !== 3) err('my_version.differences', '차별점은 정확히 3개');
    else mv.differences.forEach((d, i) => { if (!isObj(d) || !filled(d.title) || !filled(d.text)) err(`my_version.differences[${i}]`, 'title 과 text 가 필요해요'); });
    if (!Array.isArray(mv.not_taken) || mv.not_taken.length === 0) err('my_version.not_taken', '가져오지 않는 것을 한 줄 이상');
    const name = String(mv.working_name || '');
    if (COPY_WORDS.test(name)) err('my_version.working_name', '클론, 카피 같은 말을 이름에 쓰지 않아요');
    const target = isObj(t) && filled(t.name) ? t.name.trim().toLowerCase() : '';
    if (target && name.toLowerCase().includes(target)) err('my_version.working_name', '대상의 이름을 내 버전 이름에 넣지 않아요');
  }

  // ---- 읽은 깊이 (선택)
  if (isObj(m) && m.depth !== undefined) {
    const d = m.depth;
    if (!isObj(d) || !Array.isArray(d.steps)) err('meta.depth', 'steps 배열이 필요해요');
    else {
      d.steps.forEach((st, i) => {
        if (!isObj(st) || !DEPTHS.includes(st.key)) return err(`meta.depth.steps[${i}]`, `key 는 ${DEPTHS.join(' | ')} 중 하나`);
        if (!STEP_STATES.includes(st.state)) err(`meta.depth.steps[${i}]`, `state 는 ${STEP_STATES.join(' | ')} 중 하나`);
        if (st.state !== 'done' && !filled(st.note)) err(`meta.depth.steps[${i}]`, '끝까지 못 읽은 단계에는 까닭(note)을 적어요');
      });
      const codeStep = d.steps.find((st) => isObj(st) && st.key === 'code');
      const usedCode = [...evSeen.values()].includes('code');
      if (usedCode && (!codeStep || !['done', 'partial'].includes(codeStep.state))) err('meta.depth', '코드에서 본 근거가 있는데 속 읽기 단계가 done 이나 partial 이 아니에요');
    }
  }

  // ---- skeleton (선택): 해부 장면에 쓰는 뼈대
  if (r.skeleton !== undefined) {
    const sk = r.skeleton;
    if (!isObj(sk) || !Array.isArray(sk.blocks) || sk.blocks.length === 0) err('skeleton.blocks', '구역이 한 개 이상 있어야 해요. 뼈대가 없으면 skeleton 을 통째로 빼기');
    else {
      sk.blocks.forEach((b, i) => {
        const w = `skeleton.blocks[${i}]`;
        if (!isObj(b)) return err(w, '객체가 아니에요');
        if (!filled(b.name)) err(w, 'name 이 비었어요');
        if (!ROLES.includes(b.role)) err(w, `role 은 ${ROLES.join(' | ')} 중 하나`);
        if (!(Number(b.weight) > 0)) err(w, 'weight 는 0보다 큰 숫자');
        if (b.status !== undefined && !STATUS.includes(b.status)) err(w, `status 는 ${STATUS.join(' | ')} 중 하나`);
      });
      if (Array.isArray(sk.evidence)) checkRefs('skeleton.evidence', sk.evidence, null);
    }
  }

  // ---- whole-file hygiene
  const raw = JSON.stringify(r);
  if (/\/Users\/|\/home\/[a-z]|[A-Za-z]:\\\\Users\\\\/.test(raw)) warn('report', '내 컴퓨터의 절대 경로가 들어 있어요. 상대 경로로 바꿔 주세요');
  if (/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/.test(raw)) warn('report', '이메일 주소처럼 보이는 글자가 있어요');
  if (/(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{12,}|AIza[0-9A-Za-z_-]{20,})/.test(raw)) err('report', '비밀 키처럼 보이는 글자가 있어요. 지워 주세요');
  for (const id of ids) if (!used.has(id)) warn('evidence', `${id} 는 어떤 주장에도 쓰이지 않았어요`);

  return { errors, warnings, counts, myVersion };
}

function main() {
  const args = process.argv.slice(2);
  const dissectOnly = args.includes('--dissect-only');
  const file = args.find((a) => !a.startsWith('--'));
  if (!file) {
    console.error('사용: node check-report.mjs <report.json> [--dissect-only]');
    process.exit(2);
  }
  let r;
  try {
    r = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    console.error(`읽을 수 없어요: ${e.message}`);
    process.exit(2);
  }
  const { errors, warnings, counts, myVersion } = checkReport(r, { dissectOnly });
  console.log(`관찰 ${counts.observed} · 추정 ${counts.inferred} · 모름 ${counts.unknown}${counts.code ? ` · 코드 흔적 ${counts.code}` : ''}`);
  if (dissectOnly) console.log(`내 버전 칸  ${myVersion === 'empty' ? '아직 안 씀 (해부만 검사)' : '쓰여 있어서 함께 검사'}`);
  for (const w of warnings) console.log(`경고  ${w}`);
  for (const e of errors) console.log(`오류  ${e}`);
  console.log(errors.length ? `오류 ${errors.length}개. 고친 뒤 다시 검사해 주세요.` : `통과 (경고 ${warnings.length}개)${dissectOnly && myVersion === 'empty' ? ' · 해부만' : ''}`);
  process.exit(errors.length ? 1 : 0);
}

// 바로 실행했을 때만 돈다. 경로에 심볼릭 링크가 끼어 있어도 알아보도록 실제 경로로 견준다.
const direct = (() => { try { return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url)); } catch { return false; } })();
if (direct) main();
