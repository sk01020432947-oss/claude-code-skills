# -*- coding: utf-8 -*-
"""~/.claude/skills 스캔 -> 공유용 스킬 카탈로그 HTML 생성 (skill-library 스킬의 빌드 스크립트)

사용: python build_catalog.py
산출: ~/Documents/skills-catalog.html + ~/.claude/skills-inventory.json
새 스킬이 '기타'로 빠지거나 'english w/o translation'이 출력되면
아래 EXPLICIT(put 호출)·TRANSLATIONS 딕셔너리에 항목을 추가하고 재실행한다.
"""
import json, html, re, os, sys, datetime
sys.stdout.reconfigure(encoding='utf-8')

# 인자로 스캔 폴더/출력 경로를 바꿀 수 있다 (배포본 등 부분집합 카탈로그용)
#   python build_catalog.py [스킬폴더] [출력.html]
SKILLS_DIR = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else '~/.claude/skills')
OUT = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else '~/Documents/skills-catalog.html')
INV = os.path.expanduser('~/.claude/skills-inventory.json')
OWNER = '김병곤'

# ---------- scan SKILL.md frontmatter ----------
skills = []
for d in sorted(os.listdir(SKILLS_DIR)):
    p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
    if not os.path.isfile(p):
        continue
    try:
        t = open(p, encoding='utf-8').read()
    except Exception:
        skills.append({'name': d, 'desc': ''}); continue
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    desc = ''
    if m:
        dm = re.search(r'^description:\s*(.*(?:\n(?![a-zA-Z_-]+:).*)*)', m.group(1), re.M)
        if dm:
            desc = re.sub(r'\s+', ' ', dm.group(1)).strip().strip('"\'')
    skills.append({'name': d, 'desc': desc[:400]})
json.dump(skills, open(INV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
by_name = {s['name']: s for s in skills}

# ---------- categories ----------
CATS = [
    ('sermon',   '설교·강단',        '설교 준비의 전 과정 — 본문 분석·주해, 신학자별 코칭, 설교문 작성·퇴고·검증, 콘텐츠 활용까지.'),
    ('bible',    '성경 연구·묵상',    '개인성경연구(PBS)와 본문 묵상, 로마서·바울신학 전문 연구.'),
    ('ministry', '목회·교회 사역',    '주보·행사·교육부서·소통 등 교회 운영 실무.'),
    ('writing',  '글쓰기 코칭',      '한국어 글쓰기 코칭과 AI 문체 윤문.'),
    ('academic', '논문·학술·독서',    '논문 기획·학습·심사와 책과의 대화.'),
    ('vision',   '비전 코칭·진단',    '최윤식 박사 미래준비학교 기반 비전 발견·진단·전략 코칭.'),
    ('foresight','미래학 방법론',     'Millennium Project 미래연구방법론(V3.0) 풀 구현 — 환경 스캐닝·퓨처스 휠·시나리오·와일드카드.'),
    ('video',    '영상 제작',        '주제 한 문장 → 완성 유튜브 영상까지의 자동 파이프라인(대본·음성·아바타·B-roll·합성·검증).'),
    ('webtoon',  '웹툰 제작',        '트렌드 조사 → 시나리오 → 패널 렌더 → 조립·검수까지 웹툰 제작 하네스.'),
    ('design',   '디자인·프레젠테이션','PPT·레이아웃·디자인 시스템·이미지 생성.'),
    ('gov-doc',  '공공·행정 문서',    'HWP/HWPX·공문서·보고서·회의록 등 한국 공공문서 실무.'),
    ('gov-data', '공공데이터·법령 조사','나라장터·KOSIS·국회·법령·지원사업 등 공공 정보 조회.'),
    ('research', '리서치·심층조사',   '멀티에이전트 딥리서치, 차단 사이트 접근, 다중 관점 분석.'),
    ('dev',      '개발·자동화',      '앱 빌드 파이프라인, 에이전트 하네스, 개발 도구.'),
    ('etc',      '기타',            '분류 밖의 도구들.'),
]
CAT_TITLE = {k: t for k, t, _ in CATS}

EXPLICIT = {}
def put(cat, *names):
    for n in names: EXPLICIT[n] = cat

put('ministry', 'announcement-script', 'meeting-agenda', 'midweek-devotional',
    'small-group-questions', 'social-media-calendar', 'next-gen-ministry-bible',
    'pastor-foundation', 'pastor-ai-safety-guide', 'pastoral-prompt-engineering',
    'weekly-content-board')
put('writing', 'adult-vocabulary-writing-coach', 'godowon-writing-coach',
    'frontline-writing-coach', 'my-writing-master-prompt', 'redteam')
put('academic', 'paper-study', 'paper-critical-review', 'paper-writing-order',
    'talk-to-my-books')
put('gov-doc', 'official-report-skillset', 'gov-meeting-minutes', 'hwpx-mouseco',
    'hwpxskill', 'read-hwp', 'korean-doc-corpus', 'sungahna-foundation',
    'transport-receipt-collector', 'officecli', 'nudocs', 'nutrient-openclaw',
    'elegant-reports')
put('gov-data', 'alio', 'g2b-bid-search', 'kosis-stats', 'public-data-finder',
    'national-assembly-tracker', 'korean-law-search', 'ir-search')
put('research', 'deep-research', 'deep-research-pro', 'agent-reach', 'insane-search',
    'last30days', 'autoresearch-loop', 'council', 'deep-interview')
put('design', 'design-pick', 'design-audit', 'insane-design', 'layout-design-coach',
    'my-ppt', 'pptx-design-styles', 'pumasi')
put('dev', 'harness', 'harness-engineering', 'agents-md', 'task-orchestrator',
    'planner', 'parallel-task', 'goaljaby', 'kkirikkiri', 'skillers-suda',
    'git-teacher', 'docs-guide', 'gemini-agents-api', 'gemini-api',
    'gemini-interactions-api', 'uxui-design-system', 'show-me-the-prd',
    'fakechat-dashboard-agent', 'agent-native-app-harness', 'context-recovery',
    'iam-recommendations-fetcher', 'nopal', 'skill-library')
put('etc', 'vibe-sunsang')

def category(name):
    if name in EXPLICIT: return EXPLICIT[name]
    if name.startswith('sermon-') or name in ('dwelling-sermon-coach', 'kangjunmin-sermon-writing-coach'):
        return 'sermon'
    if name.startswith('pbs-') or name in ('romans-meditation-study', 'pauline-law-hermeneutics'):
        return 'bible'
    if name.startswith('vision-foresight'): return 'foresight'
    if name.startswith('vision-'): return 'vision'
    if name.startswith('appbuild'): return 'dev'
    if name.startswith('webtoon'): return 'webtoon'
    if name.startswith(('media-gen', 'video-', 'audio-post', 'script-writer',
                        'voice-clone', 'heygen')) or name in (
            'youtube-video-pipeline', 'explainer-video', 'remotion',
            'cost-preview-confirm', 'suite-runtime-keys'):
        return 'video'
    if name.startswith('humanize'): return 'writing'
    if name.startswith('church-'): return 'ministry'
    return 'etc'

# ---------- suites (parent -> children grouped under one card) ----------
SUITE_PARENTS = ['appbuild', 'vision-foresight-environmental-scanning',
                 'vision-foresight-futures-wheel', 'vision-foresight-scenarios',
                 'vision-foresight-wild-cards', 'media-gen', 'script-writer',
                 'voice-clone-elevenlabs', 'heygen-avatar-render', 'audio-post',
                 'video-stitch', 'video-verify', 'humanize']
children_of = {p: [] for p in SUITE_PARENTS}
child_names = set()
for s in skills:
    n = s['name']
    for p in sorted(SUITE_PARENTS, key=len, reverse=True):
        if n != p and n.startswith(p + '-'):
            children_of[p].append(n); child_names.add(n)
            break

# ---------- Korean translations for English descriptions ----------
TRANSLATIONS = {
 'agent-native-app-harness': "Agent Native Agent(ANA) 하네스 — 대시보드를 '보면서' 코딩 에이전트와 '대화하며' 운영하는 에이전트 네이티브 앱/에이전트를 만들고 발전시키는 스킬. '에이전트 네이티브 에이전트', 'ANA', 'ANL', '보면서 대화하는 운영 도구', 셀프호스팅 개인/1인 사업 도구를 만들고 싶을 때 사용.",
 'agent-reach': "인터넷에서 무언가를 조사·검색해야 할 때 사용하는 스킬. 특정 플랫폼(샤오홍슈, 트위터/X, 빌리빌리, Reddit, Facebook, Instagram, V2EX, LinkedIn, YouTube, GitHub 코드검색, 팟캐스트, 주식 시세, RSS 등)이나 URL·링크가 언급될 때도 반드시 사용.",
 'announcement-script': "주일 아침 광고용 60~90초 구두 안내 대본 작성. 대화체, 우선순위 정리, 최대 3~4개 항목. 아무도 졸지 않는 광고.",
 'autoresearch-loop': "Karpathy의 autoresearch를 일반화한 도메인 불문 지표 기반 개선 루프. 프로젝트/목표에 대해 무엇을 측정할지 스스로 발견한 뒤, 변경 제안→측정→개선은 유지·퇴보는 되돌리는 keep-or-revert 실험 루프를 돌리고 구현된 개선을 기록한다. 코드 성능 감사, 코드 생성, 버그 찾기, 광고 최적화 등에 적응.",
 'church-email': "주간 교회 이메일 완성본 작성. 제목·미리보기 텍스트·본문까지. 따뜻하고 훑어보기 좋고 모바일 친화적. 광고와 행사 내용을 붙여넣으면 바로 보낼 수 있는 이메일이 나온다.",
 'church-letter': "모든 상황에 맞는 교회 서신 작성. 리더십 교체, 시설 안내, 정책 변경, 환영 편지, 민감한 소통까지. 상황에 맞는 무게감을 갖춘 목회적 어조.",
 'church-social-post': "교회용 플랫폼별 SNS 게시물 작성. 주제·행사·성경구절을 주면 Facebook·Instagram·Twitter용 캡션과 이미지 제안을 플랫폼별로 최적화해 돌려준다.",
 'context-recovery': "세션 컴팩션(압축) 후 또는 문맥이 사라진 채 이어서 작업해야 할 때 작업 컨텍스트를 자동 복구. Discord, Slack, Telegram, Signal 등 지원 채널 전반에서 작동.",
 'council': "지성 위원회 소집 — 역사적 사상가들의 다중 페르소나 숙의로 복잡한 문제를 더 깊이 분석.",
 'design-audit': "Jobs/Ive 철학의 프리미엄 UI/UX 디자인 감사관. 기존 UI를 검토·평가·격상할 때 사용 — '디자인 검토해줘', 'UI 리뷰', '프리미엄 느낌으로', 'UX 감사', '기능은 그대로 두고 시각 품질만 올려줘' 요청 시 발동.",
 'docs-guide': "어떤 라이브러리든 공식 문서를 가져와 설명해주는 스킬.",
 'elegant-reports': "북유럽 감성의 아름다운 PDF 보고서 생성. 마크다운·HTML로부터 Nutrient DWS를 거쳐 세련된 경영진 브리핑, 분석 보고서, 프레젠테이션형 PDF를 만들 때 사용.",
 'fakechat-dashboard-agent': "'대시보드 에이전트' 구축 — 사용자가 Claude Code 세션과 대화하면서 동시에 실시간 데이터(일정·지표·주문·대기열)를 화면으로 보는 웹 대시보드. 채팅은 fakechat 채널로 라우팅되고, Claude가 대시보드의 데이터 API를 읽어 사용자가 승인할 수 있는 제안으로 응답한다.",
 'gemini-agents-api': "Gemini Enterprise Agent Platform의 커스텀 Agent 리소스 관리. 대화 실행 전에 서버 관리형 상태 유지 Agent 리소스를 프로그램으로 생성·설정·조회·수정·삭제(파일·스킬·도구 마운트 포함)할 때 사용.",
 'gemini-api': "기업 환경에서 Gemini를 쓰거나 Vertex AI, Google Cloud, Agent Platform이 언급될 때 사용. Google Gen AI SDK 기반 Gemini API 사용법 안내 — SDK(Python, JS/TS, Go, Java, C#), 멀티모달 입력, 도구, 미디어 생성, 캐싱, 배치 예측, Live API.",
 'gemini-interactions-api': "Gemini Enterprise Agent Platform의 Interactions API 사용 안내. 멀티턴 대화, 백그라운드 실행, 스트리밍, 구조화 출력, 함수 호출을 서버 관리형 상태 유지 API로 쓰고 싶을 때 사용.",
 'iam-recommendations-fetcher': "Google Cloud에서 지정한 범위(조직·폴더·프로젝트)의 원시 IAM 권한 추천과 보안 인사이트를 가져온다. 추천을 분석·적용하기 전 조회 용도 — 적용은 별도 스킬이 담당.",
 'insane-search': "차단된 웹사이트 적응형 접근 — 되는 방법이 나올 때까지 모든 수단을 시도. WebFetch가 402/403/차단될 때, X/Twitter·Reddit·YouTube·GitHub·Medium·Substack·네이버·쿠팡·LinkedIn 등 WAF/봇 차단 플랫폼 접근 시 사용. yt-dlp(1,858개 미디어 사이트), Jina Reader, 공개 API, curl_cffi TLS 위장, Playwright 실브라우저 체인을 자동 의존성 설치와 함께 활용.",
 'korean-law-search': "한국 법령 조회는 korean-law-mcp를 우선 사용하고, 기본 서비스가 안 될 때 법망(Beopmang)으로 폴백.",
 'last30days': "최근 30일의 Reddit + X + 웹에서 어떤 주제든 조사해 종합하고, 복붙 가능한 프롬프트로 정리. '요즘 사람들이 X에 대해 뭐라고 해?', 최신 모범 사례 학습 요청 시 사용. 전체 기능엔 OPENAI_API_KEY/XAI_API_KEY 필요, 없으면 웹 검색으로 폴백.",
 'meeting-agenda': "시간 블록·토론 질문·액션아이템 프롬프트가 있는 구조화된 회의 안건 작성. 교역자 회의, 장로회, 제직회, 봉사자 모임에 사용.",
 'midweek-devotional': "이메일이나 앱으로 보내는 짧은 주중 묵상글(200~300단어) 작성. 성경 기반, 개인적, 따뜻한 톤. 주일과 주일 사이 성도들과의 연결을 유지.",
 'nudocs': "Nudocs.ai로 문서 업로드·편집·내보내기. 협업 편집용 공유 문서 링크 생성, 마크다운 업로드, 편집된 내용 회수 시 사용.",
 'nutrient-openclaw': "Nutrient DWS용 OpenClaw 네이티브 문서 처리 스킬. 파일 변환, 텍스트·표 추출, 스캔 OCR, 개인정보 마스킹, PDF 워터마크, 전자서명, 크레딧 사용량 확인.",
 'officecli': "officecli CLI 도구로 Office 문서(.docx, .xlsx, .pptx)를 생성·분석·교정·수정. 문서 생성, 검사, 서식 확인, 문제 찾기, 차트 추가, 수정 요청 시 사용.",
 'parallel-task': "계획 파일을 조율해 막히지 않은 작업들에 병렬 서브에이전트를 여럿 띄운다. '/parallel-task' 명시 호출로 발동.",
 'pastor-foundation': "모든 목회자 AI 스킬의 공유 컨텍스트 레이어. 신학적 가드레일, 목회적 어조, 교회 컨텍스트 변수, 산출물 표준을 설정한다. 다른 작업 스킬과 함께 설치.",
 'planner': "task-orchestrator 스킬이 사용할 수 있는 다중 작업 프로젝트의 구조화된 계획 수립. 복잡한 작업을 의존성 있는 병렬·순차 작업으로 분해할 때 사용.",
 'pptx-design-styles': "PPTX 슬라이드·프레젠테이션 제작 시 30가지 현대 디자인 스타일 적용 — 글래스모피즘, 네오브루탈리즘, 벤토 그리드, 다크 아카데미아, 그라디언트 메시, 클레이모피즘, 스위스 인터내셔널, 오로라 네온, 레트로 Y2K, 노르딕 미니멀리즘, 타이포그래픽 볼드 등.",
 'read-hwp': "HWP/HWPX 문서의 에이전트 네이티브 파싱은 kordoc 사용 — JSON 추출, 문서 비교(diff), 서식 필드 추출, 마크다운→HWPX 역변환. 읽기/변환 전용 — 바이너리 편집은 rhwp-edit 사용.",
 'remotion': "React 기반 Remotion 영상 제작 모범 사례 — 컴포지션, 시퀀스, 애니메이션, 타이밍, 렌더링. Remotion 영상을 만들거나 리뷰·디버깅할 때 사용.",
 'sermon-brainstorm': "설교 준비를 위한 인터랙티브 브레인스토밍 파트너. 유도 질문으로 메시지를 명확히 하고 핵심 긴장을 찾아 설교 브리프를 만든다. 목회자와 '함께' 생각하며, 설교를 대신 써주지 않는다.",
 'sermon-research': "주간 설교 준비용 심층 리서치 도우미. 본문·주제·질문을 주면 주석 통찰, 역사적 배경, 원어 노트, 생각거리를 돌려준다. 리서치 전용 — 개요·설교문 작성은 하지 않는다.",
 'sermon-series': "여러 주에 걸친 설교 시리즈 기획. 주제나 성경 책과 주차 수를 주면 시리즈 제목 후보, 주차별 본문·제목·핵심 아이디어를 돌려준다.",
 'sermon-to-blog': "설교 녹취록을 읽기 좋은 800~1200단어 블로그 글로 변환. 단순 녹취가 아닌 독립된 아티클. SEO 친화적 제목, 메타 설명, 웹 서식 본문.",
 'sermon-to-youtube': "설교 영상 유튜브 최적화. 제목과 녹취록을 주면 최적화된 제목, 타임스탬프 포함 설명, 태그, 썸네일 컨셉, 숏폼 클립 추천을 돌려준다.",
 'small-group-questions': "주일 설교 기반 주간 소그룹 토론 질문 생성. 관찰→해석→적용 흐름. 아이스브레이커와 마무리 기도 제목 포함. 소그룹 리더에게 바로 전달 가능.",
 'social-media-calendar': "1주 또는 1개월치 SNS 콘텐츠를 날짜별로 생성. 다가오는 설교·행사·강조점을 주면 게시물 아이디어·유형·플랫폼 배정이 있는 구조화된 캘린더를 돌려준다.",
 'task-orchestrator': "의존성 분석, 병렬 tmux/Codex 실행, 자가 치유 하트비트 모니터링을 갖춘 자율 멀티에이전트 작업 오케스트레이션. 조율된 병렬 실행이 필요한 여러 이슈/작업의 대형 프로젝트에 사용.",
 'uxui-design-system': "UI 의존성 제로로 토스 스타일(클린 핀테크) UX/UI 디자인 시스템을 설계·구현 — 토큰 체계(색·타이포·형태·엘리베이션), 컴포넌트 패턴, 반응형/다크모드/접근성 규칙, 빌드 워크플로우. 새 웹 UI 시작, 일관성 없는 UI 통일, '디자인 시스템' 요청 시 사용.",
 'vision-foresight-futures-wheel-delphi-rounds': "Glenn의 '인터넷 델파이 퓨처스 휠' 변형 구현 — 국제 패널이 비동기로 모여 5라운드 델파이로 퓨처스 휠을 체계적으로 구축. 빈도 가중 타원 크기, 위키 협업 지원. 마스터 스킬 전용 내부 하위 스킬.",
 'vision-foresight-futures-wheel-domain-v2': "Glenn 'Version 2' 구현 — 원래 퓨처스 휠이 놓치기 쉬운 영향 범위를, 사전에 정한 도메인 세트별로 강제 검토하게 하는 변형. 마스터 전용 내부 하위 스킬.",
 'vision-foresight-futures-wheel-scenario-forecast': "Glenn '대안 시나리오 내 예측 생성' 구현 — 시나리오 하나와 그 안의 항목을 골라 퓨처스 휠로 파급 영향을 전개해 시나리오 내부 예측을 만든다. 마스터 전용 내부 하위 스킬.",
 'vision-foresight-futures-wheel-temporal-v3': "Glenn 'Version 3' 구현 — 역사적 동인(과거)·현재 상관·미래 함의를 원뿔(cone) 형태 3차원으로 쌓는 시간축 확장 퓨처스 휠. 마스터 전용 내부 하위 스킬.",
 'vision-foresight-scenarios-cone-of-plausibility': "Charles W. Taylor(미 육군전쟁대학)의 'Cone of Plausibility(개연성 원뿔)' 모델러 — 시나리오 대표 스킬의 9번째 내부 하위 스킬.",
 'vision-foresight-scenarios-driving-forces-identification': "Schwartz 2단계 '환경의 핵심 동인·트렌드 식별' + TFG 시나리오 공간 정의 구현 — 시나리오의 빌딩블록인 추동력(driving forces)을 도출한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-focal-issue-definition': "Schwartz 1단계 '초점 이슈/결정 식별' + Bishop 워크숍 양식 구현 — '향후 [도메인]에서 가장 중요한 이슈는 무엇인가'를 확정한다. 시나리오의 1번째 내부 하위 스킬.",
 'vision-foresight-scenarios-importance-uncertainty-ranking': "Schwartz 3단계 '중요도×불확실성 순위' 구현 — 추동력·트렌드를 2×2 매트릭스로 평가해 시나리오 축 후보를 고른다. 내부 하위 스킬.",
 'vision-foresight-scenarios-internal-consistency-check': "'좋은 시나리오' 3기준(개연성·내적 일관성·의사결정 관련성) 검사기 — 시나리오 세트의 인과 경로와 논리 모순을 점검한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-key-measures-events': "TFG 개발 2단계 '핵심 지표 정의' 구현 — 각 시나리오 내 경제성장·입법 환경·기술 등 핵심 측정치와 사건을 설계한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-leading-indicators': "Schwartz 7단계 '선행 지표와 이정표 선정' 구현 — 현실이 어느 시나리오로 향하는지 조기 감지할 모니터링 지표를 고른다. 내부 하위 스킬.",
 'vision-foresight-scenarios-narrative-writing': "Schwartz 5단계 '시나리오 채우기' 구현 — 현재와 미래 상태를 개연성 있는 인과로 잇는 시나리오 내러티브를 집필한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-policy-testing': "TFG '정책 테스트' 구현 — 시나리오 범위 전체에 정책을 대입해 강건(robust) 요소와 조건부(contingent) 요소로 이분한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-projection-engine': "TFG '핵심 지표 투영' 구현 — 트렌드 영향 분석(TIA)으로 각 시나리오의 핵심 지표를 수치로 투영한다. 내부 하위 스킬.",
 'vision-foresight-scenarios-scenario-logics-selection': "Schwartz 4단계 '시나리오 로직 선택' 구현 — 2×2 사분면(MITRE 사례)·다차원 조합으로 시나리오 골격 이론을 세운다. 내부 하위 스킬.",
 'vision-foresight-wild-cards': "Petersen & Steinmüller의 Wild Cards(미래연구방법론 V3.0 10장) 풀 구현 대표 스킬 — '발생 확률은 낮지만 영향은 극대'인 뜻밖의 사건을 식별·평가·모니터링·대응하는 방법론. Shell의 'rapids'(1970s) 기원, Petersen 『Out of the Blue』 78개 와일드카드 카탈로그와 Arlington Impact Index 계보를 잇는다.",
 'vision-foresight-wild-cards-assessment': "'내 조직에 가장 중요한 와일드카드는?' 평가 단계 — Petersen 4요인 피라미드(존재·생존·행동·도구, 파워팩터 1~4)로 우선순위를 매긴다. 내부 하위 스킬.",
 'vision-foresight-wild-cards-identification': "'원리상 어떤 와일드카드가 발생할 수 있나' 식별 단계 — 브레인스토밍, AI 전문가 패널 인터뷰, 설문, 역사적 유추(1918 독감·닷컴버블·9/11·SARS·2008 금융위기) 등 5기법 오케스트레이션. 내부 하위 스킬.",
 'vision-foresight-wild-cards-impact-index': "Arlington Impact Index 공식(ΔC+R+V+O+T+Op+P=I_AI) 구현 — 변화 속도·파급 범위·취약성·결과 불확실성·시점 등 7요인으로 와일드카드 영향 지수를 산출한다. 내부 하위 스킬.",
 'vision-foresight-wild-cards-implications-synthesis': "최종 통합 단계 — 앞 단계 산출물을 종합해 '비범한 함의'와 강점·약점·프런티어까지 정리한 와일드카드 종합 보고를 만든다. 내부 하위 스킬.",
 'vision-foresight-wild-cards-monitoring': "'도래를 미리 감지할 수 있나' 모니터링 단계 — 레이더에 잡힌 와일드카드의 전조 사건(precursor)을 추적하는 감시 체계를 설계한다. 내부 하위 스킬.",
 'vision-foresight-wild-cards-options-action': "'우리가 할 수 있는 일은 무엇인가' 대응 옵션 단계 — 시스템 사고·창의성 훈련·직관 등 비선형 사고 기법으로 비관습적 대응책을 설계한다. 내부 하위 스킬.",
 'vision-foresight-wild-cards-scenario-integration': "시나리오 구축과의 결합 단계 — Steinmüller의 6가지 선별 규칙을 자동 적용해 와일드카드를 시나리오에 통합한다. 내부 하위 스킬.",
}

def hangul_ratio(t):
    if not t: return 1.0
    h = sum(1 for ch in t if '가' <= ch <= '힣')
    return h / max(len(t), 1)

# ---------- summary extraction ----------
def clean(d):
    if not d: return ''
    d = re.sub(r'^[>|]\s*', '', d.strip())
    d = re.sub(r'^##\s*TLDR\s*[—-]*\s*', '', d)
    d = re.sub(r'\*\*?', '', d)
    return d.strip()

def summary(d):
    d = clean(d)
    if not d: return '(설명 없음)'
    for marker in [' 사용자가 ', ' 트리거', ' Use when', ' ## Triggers']:
        i = d.find(marker)
        if i > 30: d = d[:i]; break
    m = re.search(r'\.\s', d)
    if m and m.start() > 30: d = d[:m.start()+1]
    i = d.find('다. ')
    if i > 30: d = d[:i+2]
    if len(d) > 160: d = d[:158].rstrip() + '…'
    return d

def esc(t): return html.escape(t, quote=True)

# ---------- group into categories ----------
cat_items = {k: [] for k, _, _ in CATS}
unmapped = []
for s in skills:
    n = s['name']
    if n in child_names: continue
    c = category(n)
    if c not in cat_items: unmapped.append(n); c = 'etc'
    cat_items[c].append(s)

total = len(skills)
print('unmapped:', unmapped)
for k, t, _ in CATS:
    cnt = sum(1 + len(children_of.get(x['name'], [])) for x in cat_items[k])
    print(f'{t}: {cnt}')

# ---------- render ----------
COPY_SVG = ('<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
            'stroke-width="1.5" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/>'
            '<path d="M10.5 5.5V4a1.5 1.5 0 0 0-1.5-1.5H4A1.5 1.5 0 0 0 2.5 4v5A1.5 1.5 0 0 0 4 10.5h1.5"/></svg>')

def copy_btn(name, small=False):
    cls = 'copy small' if small else 'copy'
    return (f'<button class="{cls}" type="button" data-copy="{esc(name)}" '
            f'title="스킬 폴더명 복사" aria-label="{esc(name)} 폴더명 복사">{COPY_SVG}</button>')

def desc_block(name, raw_desc):
    """Returns (summary_text, details_html). Korean translation first, English original kept below."""
    d = clean(raw_desc or '')
    tr = TRANSLATIONS.get(name)
    if tr:
        inner = (f'<p class="full">{esc(tr)}</p>'
                 f'<p class="orig-label">원문 (English)</p>'
                 f'<p class="full orig">{esc(d)}</p>')
        return summary(tr), f'<details><summary>상세 설명 · 발동 트리거</summary>{inner}</details>'
    s = summary(raw_desc)
    det = ''
    if d and d != s:
        det = f'<details><summary>상세 설명 · 발동 트리거</summary><p class="full">{esc(d)}</p></details>'
    return s, det

def card(s):
    n = s['name']
    kids = children_of.get(n, [])
    sum_txt, det = desc_block(n, s.get('desc'))
    h = ['<article class="card">']
    h.append(f'<div class="card-head"><code class="slug">/{esc(n)}</code>{copy_btn(n)}')
    if kids: h.append(f'<span class="suite-badge">묶음 · 하위 {len(kids)}개</span>')
    h.append('</div>')
    h.append(f'<p class="sum">{esc(sum_txt)}</p>')
    if det: h.append(det)
    if kids:
        h.append(f'<details class="kids"><summary>하위 스킬 {len(kids)}개 보기</summary><ul>')
        for kn in kids:
            ks = by_name[kn]
            ksum, _ = desc_block(kn, ks.get('desc'))
            h.append(f'<li><div class="kid-head"><code class="slug small">/{esc(kn)}</code>{copy_btn(kn, small=True)}</div>'
                     f'<span class="kid-sum">{esc(ksum)}</span></li>')
        h.append('</ul></details>')
    h.append('</article>')
    return '\n'.join(h)

# report any English description still lacking a translation
missing = [s['name'] for s in skills
           if hangul_ratio(s.get('desc') or '') < 0.05 and (s.get('desc') or '').strip()
           and s['name'] not in TRANSLATIONS]
print('english w/o translation:', missing)

sections = []
navchips = []
for k, title, blurb in CATS:
    items = cat_items[k]
    if not items: continue
    cnt = sum(1 + len(children_of.get(x['name'], [])) for x in items)
    navchips.append(f'<a class="chip" href="#cat-{k}">{esc(title)} <b>{cnt}</b></a>')
    cards = '\n'.join(card(s) for s in sorted(items, key=lambda x: x['name']))
    sections.append(f'''
<section class="cat" id="cat-{k}">
  <header class="cat-head">
    <h2>{esc(title)} <span class="count">{cnt}</span></h2>
    <p class="blurb">{esc(blurb)}</p>
  </header>
  <div class="grid">{cards}</div>
</section>''')

page = '''<title>스킬 라이브러리 · __TOTAL__ Skills</title>
<style>
:root{
  --bg:#F6F7F5; --surface:#FFFFFF; --ink:#20261F; --muted:#5A6357;
  --accent:#2F6B4F; --accent-ink:#FFFFFF; --accent-soft:#E3EFE7;
  --line:#E1E5DE; --code-bg:#EEF2EC; --shadow:0 1px 3px rgba(32,38,31,.06);
}
@media (prefers-color-scheme: dark){:root{
  --bg:#151A17; --surface:#1D2420; --ink:#E6EBE4; --muted:#95A096;
  --accent:#7CBE9C; --accent-ink:#10241A; --accent-soft:#24352C;
  --line:#2A332D; --code-bg:#232C26; --shadow:0 1px 3px rgba(0,0,0,.3);
}}
:root[data-theme="dark"]{
  --bg:#151A17; --surface:#1D2420; --ink:#E6EBE4; --muted:#95A096;
  --accent:#7CBE9C; --accent-ink:#10241A; --accent-soft:#24352C;
  --line:#2A332D; --code-bg:#232C26; --shadow:0 1px 3px rgba(0,0,0,.3);
}
:root[data-theme="light"]{
  --bg:#F6F7F5; --surface:#FFFFFF; --ink:#20261F; --muted:#5A6357;
  --accent:#2F6B4F; --accent-ink:#FFFFFF; --accent-soft:#E3EFE7;
  --line:#E1E5DE; --code-bg:#EEF2EC; --shadow:0 1px 3px rgba(32,38,31,.06);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Pretendard Variable",Pretendard,"Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif;
  line-height:1.65;font-size:15px}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px 80px}
.hero{padding:56px 0 8px}
.hero .eyebrow{font-size:12px;letter-spacing:.14em;color:var(--accent);font-weight:700;text-transform:uppercase}
.hero h1{font-size:clamp(28px,4vw,40px);margin:.2em 0 .1em;letter-spacing:-.02em;text-wrap:balance}
.hero .meta{color:var(--muted);margin:0 0 4px}
.hero .meta b{color:var(--ink)}
.guide{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:20px 24px;margin:24px 0;box-shadow:var(--shadow)}
.guide h2{margin:0 0 10px;font-size:17px}
.guide ol{margin:0 0 10px;padding-left:22px}
.guide li{margin:4px 0}
.guide .note{color:var(--muted);font-size:13.5px;border-top:1px dashed var(--line);padding-top:10px;margin:10px 0 0}
.toolbar{position:sticky;top:0;z-index:9;background:var(--bg);
  padding:12px 0 10px;border-bottom:1px solid var(--line)}
.search{width:100%;padding:10px 14px;font-size:15px;border:1.5px solid var(--line);
  border-radius:8px;background:var(--surface);color:var(--ink)}
.search:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.chip{font-size:12.5px;color:var(--ink);background:var(--surface);border:1px solid var(--line);
  border-radius:99px;padding:4px 11px;text-decoration:none;white-space:nowrap}
.chip b{color:var(--accent);font-weight:700;margin-left:2px}
.chip:hover{border-color:var(--accent);background:var(--accent-soft)}
.cat{margin-top:44px;scroll-margin-top:120px}
.cat-head h2{font-size:22px;margin:0;letter-spacing:-.01em}
.cat-head .count{display:inline-block;font-size:13px;font-weight:700;color:var(--accent);
  background:var(--accent-soft);border-radius:99px;padding:1px 10px;vertical-align:3px;margin-left:6px}
.cat-head .blurb{color:var(--muted);margin:4px 0 16px;max-width:65ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:16px 18px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:8px}
.card-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.slug{font-family:"JetBrains Mono",Consolas,"Courier New",monospace;font-size:13.5px;
  background:var(--code-bg);color:var(--accent);border-radius:6px;padding:2px 8px;font-weight:600;
  overflow-wrap:anywhere}
.slug.small{font-size:12px}
.suite-badge{font-size:11.5px;font-weight:700;color:var(--accent);border:1px solid var(--accent);
  border-radius:99px;padding:1px 8px}
.copy{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;
  border:1px solid var(--line);border-radius:6px;background:var(--surface);color:var(--muted);
  cursor:pointer;padding:0;flex:none}
.copy:hover{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}
.copy:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.copy.small{width:22px;height:22px}
.copy.done{color:var(--accent-ink);background:var(--accent);border-color:var(--accent)}
.kid-head{display:flex;align-items:center;gap:6px}
.orig-label{margin:10px 0 2px;font-size:11.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted)}
.full.orig{opacity:.75;font-size:12.5px}
#toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(8px);
  background:var(--ink);color:var(--bg);border-radius:8px;padding:8px 16px;font-size:13.5px;
  opacity:0;pointer-events:none;transition:opacity .18s,transform .18s;z-index:99}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
@media (prefers-reduced-motion:reduce){#toast{transition:none}}
.sum{margin:0;font-size:14px}
details{font-size:13.5px}
details summary{cursor:pointer;color:var(--muted);font-weight:600}
details summary:hover{color:var(--accent)}
details .full{color:var(--muted);margin:8px 0 0;white-space:pre-wrap}
.kids ul{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.kids li{border-left:2px solid var(--line);padding-left:10px}
.kid-sum{display:block;color:var(--muted);font-size:12.5px;margin-top:2px}
.hidden{display:none!important}
footer{margin-top:56px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}
@media (prefers-reduced-motion:no-preference){
  .card{transition:border-color .15s}
  .card:hover{border-color:var(--accent)}
}
</style>
<div class="wrap">
  <header class="hero">
    <div class="eyebrow">Claude Code Skill Library</div>
    <h1>스킬 라이브러리</h1>
    <p class="meta">__OWNER__ · 총 <b>__TOTAL__개</b> 스킬 · __DATE__ 기준 · 카테고리 __NCAT__개</p>
  </header>

  <div class="guide">
    <h2>설치 및 사용법</h2>
    <ol>
      <li><b>받기</b> — 공유받은 <code class="slug">claude-skills-share.zip</code> 압축을 풉니다.</li>
      <li><b>설치</b> — 원하는 스킬 폴더만 골라 <code class="slug">C:\\Users\\&lt;내이름&gt;\\.claude\\skills\\</code> (Mac/Linux는 <code class="slug">~/.claude/skills/</code>)에 복사합니다. 전부 복사해도 됩니다.</li>
      <li><b>사용</b> — Claude Code를 재시작한 뒤, 채팅에서 <code class="slug">/스킬이름</code>을 입력하거나 각 스킬의 발동 트리거 문장(카드의 "상세 설명" 참조)을 자연어로 말하면 자동 발동됩니다.</li>
      <li><b>골라 가져가기</b> — 각 카드의 복사 아이콘을 누르면 스킬 폴더명이 클립보드에 복사됩니다. ZIP 압축을 푼 곳에서 같은 이름의 폴더를 찾아 <code class="slug">.claude\\skills\\</code>에 넣으면 그 스킬만 설치됩니다.</li>
    </ol>
    <p class="note">⚠ 일부 스킬은 별도 준비물이 필요합니다 — 영상 제작 계열(ElevenLabs·HeyGen·fal.ai API 키), 이미지 렌더 계열(codex CLI), 검색 계열 ir-search·insane-search(Python + curl_cffi), 공공데이터 계열(data.go.kr 등 본인 API 키). 키가 없으면 실행 시 스킬이 안내합니다.</p>
  </div>

  <div class="toolbar">
    <input class="search" id="q" type="search" placeholder="스킬 이름·키워드 검색 (예: 설교, 웹툰, 보고서, HWPX…)" aria-label="스킬 검색">
    <nav class="chips">__CHIPS__</nav>
  </div>

  __SECTIONS__

  <footer>이 카탈로그는 각 스킬 폴더의 SKILL.md 설명을 기반으로 자동 생성되었습니다. 스킬은 개인 환경(Windows·Claude Code)에서 제작·검증된 것으로, 환경에 따라 일부 조정이 필요할 수 있습니다.</footer>
</div>
<div id="toast" role="status" aria-live="polite"></div>
<script>
const toast=document.getElementById('toast');let toastT;
function showToast(msg){toast.textContent=msg;toast.classList.add('show');
  clearTimeout(toastT);toastT=setTimeout(()=>toast.classList.remove('show'),1600);}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(t);}
  return new Promise((res,rej)=>{const ta=document.createElement('textarea');ta.value=t;
    ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy')?res():rej();}catch(e){rej(e);}finally{ta.remove();}});
}
document.addEventListener('click',e=>{
  const b=e.target.closest('.copy');if(!b)return;
  const name=b.dataset.copy;
  copyText(name).then(()=>{
    showToast('복사됨: '+name);
    b.classList.add('done');setTimeout(()=>b.classList.remove('done'),1200);
  }).catch(()=>showToast('복사 실패 — 이름을 직접 선택해 복사해 주세요'));
});
const q=document.getElementById('q');
q.addEventListener('input',()=>{
  const v=q.value.trim().toLowerCase();
  document.querySelectorAll('.card').forEach(c=>{
    c.classList.toggle('hidden', v && !c.textContent.toLowerCase().includes(v));
  });
  document.querySelectorAll('.cat').forEach(s=>{
    s.classList.toggle('hidden', !s.querySelector('.card:not(.hidden)'));
  });
});
</script>'''

today = datetime.date.today()
page = page.replace('__TOTAL__', str(total)).replace('__NCAT__', str(len(navchips)))
page = page.replace('__OWNER__', OWNER).replace('__DATE__', f'{today.year}년 {today.month}월 {today.day}일')
page = page.replace('__CHIPS__', '\n'.join(navchips))
page = page.replace('__SECTIONS__', '\n'.join(sections))
open(OUT, 'w', encoding='utf-8').write(page)
print('written', OUT, len(page), 'chars')
