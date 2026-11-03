---
name: pkm-os
description: "김병곤의 옵시디언 지식 OS(PKM 폴더: raw→wiki→output 3층 + MOC) 운영 스킬. 유튜브·논문·도서·클리핑·설교자료를 raw에 넣고(ingest), wiki를 근거로 답하고(query), 건강 검진(lint), 세이브 포인트(log), 설교·논문·독서·업무·회고 목적별 워크플로우를 실행한다. 트리거: /pkm-os, 지식 OS, 위키에 넣어 줘, 인제스트, 위키 참고해서, 위키 정비, 설교 조각화, 문헌 노트 만들어, 책 노트 만들어, 영상 자막 위키로."
---

# pkm-os — 지식 OS 운영자

볼트 `/Users/kbg1023/obsidian/Obsidian 2025` 안의 `PKM/`(설치 시 루트명이 다르면 `~/Documents/KBG-PKM-System/config.json`의 `root`)를 운영한다. 규칙의 정본은 볼트 안 `PKM/CLAUDE.md`(AI용)와 `PKM/01 가이드.md`(사람용)다. **이 스킬은 절차를 외우지 않고 그 두 파일을 먼저 읽는다.**

## 0. 시작 체크 (매번)
```bash
python3 - <<'PY'
import json,os
c=os.path.expanduser('~/Documents/KBG-PKM-System/config.json')
cfg=json.load(open(c)) if os.path.exists(c) else {}
print('vault:',cfg.get('vault','/Users/kbg1023/obsidian/Obsidian 2025'),'root:',cfg.get('root','PKM'))
PY
```
- `PKM/`가 없으면: "아직 설치 전입니다. `python3 ~/Documents/KBG-PKM-System/install.py --apply`" 안내 후 중단.
- 읽기 순서: `PKM/CLAUDE.md` → `PKM/02 나의 핵심 맥락.md` → `PKM/20 wiki/index.md`.
- 볼트 루트 `CLAUDE.md` 계약을 지킨다: 정본 폴더(100~1004)에는 쓰지 않고 `_agent-drafts/`로. `PKM/10 raw/`는 읽기 전용.

## 1. 명령 라우팅
| 사용자의 말 | 할 일 |
|---|---|
| "넣어 줘 / 인제스트 / 위키에 반영" | **ingest** — `PKM/CLAUDE.md` §ingest 절차. `why`/`use_for` 없으면 먼저 묻기 |
| "위키 참고해서 … / 찾아 줘 / 초안" | **query** — index → 노트 → `[[근거]]`. 저장 여부 묻기 |
| "정비 / 건강 검진 / lint" | **lint** — 고아·미처리·규칙 위반·60일 미갱신. raw 불변 |
| "저장해 줘 / 세이브" | **log**(데일리 AI 로그) 또는 **save**(다섯 필터 → wiki) |
| "설교 …" | §2-1 |
| "논문 / 문헌 …" | §2-2 |
| "책 …" | §2-3 |
| "유튜브 / 영상 / 자막" | §2-4 |
| "회고 / 데일리" | §2-5 |
| "묵은 메모 정리 / 일괄 분류 / 중복 찾기 / 메모에서 할 일" | `references/legacy-triage.md` — 스캔(`scripts/legacy_scan.py`) → 분류 제안 → 승인 후 태깅 → 할 일 |

## 2. 목적별 절차
### 2-1 설교
- 준비: `본문 노트`가 없으면 `PKM/90 system/템플릿/본문 노트.md`로 생성. 주석은 `logos-bible-research` MCP → 결과를 `PKM/10 raw/설교자료/`에 저장(사람 확인) → ingest.
- 초안: "내 설교 60% + 자료 40%" 비율을 존중. `sermon-*` 스킬(본문분석·역사문화·코칭)은 raw를 풍부하게 하는 용도로만.
- 완료 후 조각화: 원고를 `PKM/20 wiki/설교/조각/`에 재사용 단락으로 쪼개고 본문·주석·예화와 링크. `theology`는 폐쇄 목록만.
### 2-2 논문
- Zotero citekey 우선(`zotero` 스킬). 발췌를 `raw/논문/`에, `rq: [[RQ-n]]` 연결. 문헌 노트 템플릿 필드 준수. 인용 검증은 `citation-gate`.
### 2-3 도서
- 서지: `kr-book-info-plugin`(옵시디언) 또는 `library-book-search` 스킬. 한줄평·다음 공부할 것은 `02 나의 핵심 맥락` §5 페르소나로.
### 2-4 유튜브
- 자막: `watch` 스킬(`--detail transcript`, ko 자막) 또는 `youtube-wiki-ingest`. `[MM:SS]` 유지, raw에 저장 후 ingest. 인용은 `URL&t=초`.
### 2-5 회고
- `/log`는 오늘 데일리 `## 5. AI 로그`에만 덧붙인다. 회고는 사람이 "회고 써 줘"라고 할 때만 `## 회고 (AI)`.

## 3. 다른 스킬과의 관계
- 노트 형식·프론트매터 → `zettelkasten-note`, `obsidian-markdown`
- 링크 감사·재편 → `km-link-audit`, `km-archive-reorganization` (lint가 커질 때)
- 새 볼트 스캐폴드 → `wiki` (이 스킬은 기존 볼트 운영 전용)
- 설치·토글 변경 → `~/Desktop/cysjavis/매뉴얼/AI도구/KBG_지식OS_매뉴얼.html` (매뉴얼·빌더), `install.py`

## 4. 금지
- raw 수정, 정본 폴더 직접 쓰기, 근거 없는 사실 주입, 사람 문장 요약·수정, 폐쇄 목록 밖 분류값.
