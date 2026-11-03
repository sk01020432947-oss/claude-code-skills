---
name: aios-map
description: "나를 아는 AI를 만드는 맥락 지도(MAP)를 점검·보강하고, 작업마다 '관련된 맥락만' 골라 컨텍스트 팩으로 묶어 준다. Meaning(나는 누구인가)·Asset(내 지식)은 PKM 볼트의 기존 문서를 재사용하고, 비어 있는 Action(AI가 쓸 도구)·Persona(AI는 누구인가)만 새로 만든다. 트리거: /aios-map, 맥락 지도, 나를 아는 AI, 컨텍스트 팩, MAP 점검, 페르소나 정의, 이 작업 맥락 챙겨 줘."
---

# aios-map — 맥락 지도와 컨텍스트 팩

출처: 브라이언(브레인 트리니티), 「모두가 '나를 아는 AI OS'를 설계하는 시대」, Seoul Metaweek 2026.
핵심 주장 두 가지 — ① 도구가 아니라 **내 맥락**이 격차를 만든다. ② 맥락은 **다 넣으면 안 된다**. 다 넣으면 환각·비용·품질 저하. 지금 이 작업에 관련된 것만 넣는다.

## 경계 (중복 금지)

| 일 | 담당 |
|---|---|
| 자료 인제스트·위키 정비·질의 | `pkm-os` |
| 주간·월간 회고 | `weekly-review` |
| 대화 내용 저장 | `save` |
| 세션 토큰 낭비 진단 | `context-budget` |
| **맥락 지도 관리 + 작업별 맥락 선별** | **이 스킬** |

이 스킬은 노트를 인제스트하지 않는다. 회고도 하지 않는다. MAP 네 층을 관리하고, 그중 필요한 조각만 꺼내 준다.

## MAP 네 층

| 층 | 질문 | 정본 위치 | 주체 |
|---|---|---|---|
| **M**eaning | 나는 누구인가 | `PKM/02 나의 핵심 맥락.md` | 사람 |
| **A**sset | 내가 아는 것·가진 산출물 | `PKM/20 wiki`, `PKM/30 output` | 사람 |
| **A**ction | AI가 나를 도울 때 쓸 도구 | `PKM/90 system/MAP-action.md` | 사람이 등록, AI가 실행 |
| **P**ersona | 내 AI는 어떤 사람인가 | `PKM/90 system/MAP-persona.md` | 사람 |

볼트 루트 = `~/Documents/KBG-PKM-System/config.json`의 `vault` + `root`(상대경로). 없으면 `/Users/kbg1023/obsidian/Obsidian 2025/PKM`.

## 모드

### 1) 점검 (`/aios-map` 인자 없음)

네 파일의 존재와 신선도를 python3으로 확인한다(한글 경로 — 셸 글롭 금지).

```bash
python3 - <<'PY'
import json, os, datetime, pathlib
cfg = pathlib.Path.home()/'Documents/KBG-PKM-System/config.json'
root = pathlib.Path('/Users/kbg1023/obsidian/Obsidian 2025/PKM')
if cfg.exists():
    c = json.loads(cfg.read_text(encoding='utf-8'))
    root = pathlib.Path(c['vault']) / c['root']   # root는 vault 상대경로다
targets = {
 'Meaning': root/'02 나의 핵심 맥락.md',
 'Action' : root/'90 system/MAP-action.md',
 'Persona': root/'90 system/MAP-persona.md',
}
for k, p in targets.items():
    if p.exists():
        st = p.stat()
        age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(st.st_mtime)).days
        print(f'{k:8} OK    {st.st_size:6}B  {age}일 전 수정  {p.name}')
    else:
        print(f'{k:8} 없음                        {p}')
asset = root/'20 wiki'
n = len(list(asset.rglob('*.md'))) if asset.exists() else 0
print(f'Asset    위키 노트 {n}개')
PY
```

보고 규칙: 없는 층 / 90일 넘게 안 고친 층 / `(확인)`·빈 불릿이 남은 층을 지적한다. 없는 층이 있으면 그 층 채우기를 이어서 제안한다. **추측으로 채우지 않는다.**

### 2) 층 채우기 (`/aios-map action`, `/aios-map persona`)

**Action** — 이미 설치된 자산을 세는 게 먼저다. 새로 만들지 않는다.
`~/.claude/skills`, `~/.claude/plugins`, 연결된 MCP 서버를 훑어, 실제로 쓰는 것만 목적별로 묶어 `MAP-action.md`에 적는다. 형식:

```markdown
| 목적 | 도구 | 부르는 말 | 마지막 사용 |
|---|---|---|---|
| 설교 준비 | sermon-pipeline | "설교 파이프라인" | 2026-09 |
```

583개를 다 적지 않는다. **실제로 손이 가는 것만.** 나머지는 존재 자체가 맥락 오염이다 → `context-budget`으로 넘긴다.

**Persona** — 사람에게 물어서 쓴다. 다섯 질문, 한 번에 하나씩:
1. AI가 나를 부르는 호칭과 말투는? (존댓말/반말, 길이)
2. 초안을 줄 때 기본값은? (완성본 vs 뼈대, 분량)
3. 내가 틀렸을 때 어떻게 하길 원하나? (바로 지적 / 근거 대고 지적 / 일단 따르고 나중에)
4. 절대 하지 말아야 할 것은? (추측 인용, 과장, 감정 위로 등)
5. 신학·연구·강의 각각에서 AI의 역할은 다른가?

답을 20줄 이내로 압축해 저장한다. 길면 페르소나가 아니라 매뉴얼이 된다.

### 3) 컨텍스트 팩 (`/aios-map pack <작업>`) — 이 스킬의 본체

지금 작업에 **관련된 맥락만** 3층으로 묶는다.

| 층 | 무엇 | 분량 상한 |
|---|---|---|
| 영속 | Meaning + Persona에서 이 작업에 걸리는 줄만 | 15줄 |
| 프로젝트 | 이 작업이 속한 프로젝트의 목표·이해관계자·마감·이전 산출물 | 15줄 |
| 태스크 | 지금 한 번에 끝낼 일, 완료 기준, 형식 | 10줄 |

절차:
1. 작업 문장에서 명사·고유명사를 뽑는다.
2. Meaning/Persona/위키에서 그 단어에 걸리는 줄만 인용한다 — 파일 전체를 붙이지 않는다.
3. 프로젝트 층이 비면 사람에게 한 번 묻는다: "이건 어느 프로젝트인가, 마감과 독자는?"
4. 세 층을 합쳐 40줄 이내 마크다운 블록으로 출력한다.
5. 빠뜨린 게 있으면 **빠졌다고 적는다.** 채워 넣지 않는다.

출력 끝에 한 줄: `제외한 것: …` — 무엇을 일부러 안 넣었는지 밝힌다. 이게 이 스킬의 핵심 가치다.

## 철칙

- 없는 사실을 만들지 않는다. 빈 칸은 빈 칸으로 보고한다.
- Meaning·Asset은 사람의 영역이다. AI가 대신 쓰지 않고, 인터뷰해서 받아 적는다.
- 맥락 팩은 길수록 나빠진다. 40줄을 넘기면 태스크를 쪼갠다.
- 모델을 바꿔도 MAP은 남는다. 도구 이름을 MAP 본문에 박지 말고 Action 표에만 둔다.
