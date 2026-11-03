---
name: km-archive-reorganization
description: Use when needing Archive Reorganization Mode (Mode R) - 대규모 vault 폴더 재편을 위한 6-Phase 반복 적용 워크플로우. 얼룩소 프로젝트 4단계를 일반화.
---

# Archive Reorganization Skill (Mode R)

대규모 vault 폴더(50+ 파일)를 체계적으로 재편하는 워크플로우.
얼룩소 아카이브 재편 프로젝트(587편, 8카테고리, 34시리즈)에서 검증된 패턴.

## ⚠️ 이 환경의 실행 규칙 (아래 본문보다 우선)

- **Obsidian CLI(`Obsidian.com`)는 이 PC에 설치되어 있지 않다.** 본문의 `OBSIDIAN_CLI=...` 및 Tier 1/Tier 2 명령은 전부 **무시**하고 Tier 3 기본 도구(Glob·Grep·Read·Write·Edit·Bash mv)로 수행한다.
- **볼트 경로**: `/Users/kbg1023/obsidian` (등록된 작업 디렉터리). 원본은 WSL 기준이므로 경로는 Windows 형식으로 바꿔 쓴다.
- **미설치 참조 무시**: 본문이 "상세 패턴 참조"로 가리키는 `km-rules-engine.md`(R3 규칙서 설계)·`km-batch-python.md`(R4 배치 실행)·`km-export-formats.md`·`drawio-diagram.md`는 설치돼 있지 않다. 해당 Phase는 이 문서에 적힌 내용만으로 수행하고, R4 배치는 Python 스크립트를 직접 작성해 실행한다.
- **파일 이동 전 필수**: 대량 이동은 되돌리기 어렵다. Phase R4 실행 전 대상 폴더를 백업하거나 git으로 스냅샷을 남기고, 이동 계획을 사용자에게 먼저 보여 승인받는다.
- **삭제 금지 — 보관함 이동으로 대체**: 재편 중 파일을 `rm`으로 지우지 않는다. 불필요·중복으로 판정된 파일은 볼트 내 `_archive/` 폴더로 이동한다. 지운 파일은 되돌릴 수 없지만 보관함은 언제든 복구·최종 삭제를 사용자가 결정할 수 있다.

## 도구 — 이 환경에서 쓸 수 있는 것

CLI도 MCP도 없다. 기본 도구와 Python 배치가 전부다.

| 작업 | 도구 |
|------|------|
| 노트 읽기 / 검색 / 목록 | Read · Grep · Glob |
| 노트 생성 / 수정 | Write · Edit |
| 파일 이동 | `Bash(mv)` 또는 Python `shutil.move` |
| 링크 그래프 계산·검증 | `~/.claude/skills/km-link-audit/scripts/vault_graph.py` |

### ⚠️ 이동하면 링크가 깨진다

Obsidian CLI의 `move`는 파일을 옮기며 그를 가리키던 wikilink를 자동으로 고쳐 준다.
**`mv`는 고쳐 주지 않는다.** 그래서 이 환경에서 재편은 반드시 한 묶음이다:

```
파일 이동  →  즉시 링크 일괄 수정  →  vault_graph.py로 깨진 링크 0개 확인
```

이동만 하고 멈추면 볼트가 이동 전보다 나빠진다. R4에서 이동 스크립트를 쓸 때는
**옮긴 파일의 옛 이름을 가리키는 모든 링크를 같은 스크립트 안에서 고친다.**

## 적용 조건

| 조건 | 설명 |
|------|------|
| 대상 파일 수 | 50+ 파일 |
| 사용자 표현 | "아카이브 정리", "카테고리 재편", "일괄 링크", "대규모 재편" |
| 기존 vault 폴더 지칭 | Mode R 자동 제안 |

## 사전 질문 (Mode R 진입 시)

```json
AskUserQuestion({
  "questions": [
    {
      "question": "재편 대상 폴더와 범위를 알려주세요.",
      "header": "대상 폴더",
      "options": [
        {"label": "특정 폴더", "description": "vault 내 특정 폴더 지정"},
        {"label": "전체 vault", "description": "vault 전체 재편"}
      ]
    },
    {
      "question": "어떤 재편을 원하시나요?",
      "header": "재편 범위",
      "options": [
        {"label": "카테고리 재분류", "description": "파일을 새 카테고리로 재배치"},
        {"label": "링크 강화", "description": "기존 구조 유지, 교차 링크만 추가"},
        {"label": "풀 재편", "description": "카테고리 + 링크 + MOC + 시리즈 전체"}
      ]
    },
    {
      "question": "매 배치 후 auto-commit 할까요?",
      "header": "Auto-commit",
      "options": [
        {"label": "예 (권장)", "description": "매 Python 배치 후 즉시 commit+push"},
        {"label": "아니오", "description": "모든 작업 완료 후 한 번에 커밋"}
      ]
    }
  ]
})
```

---

## Phase R0: 사전 정리 (Pre-Cleanup)

**목적**: 분석 전 데이터 품질 확보. Lead가 직접 수행.

### R0-1. Merge Conflict 스캔

```bash
# vault 전체에서 merge conflict 마커 검색
grep -rl "<<<<<<< " {target_folder}/ | wc -l
```

발견 시 Python 스크립트로 일괄 해결:
```python
# resolve_conflicts.py - "ours" 버전 유지
import re, glob
for f in glob.glob("{target}/**/*.md", recursive=True):
    content = open(f).read()
    if "<<<<<<< " in content:
        content = re.sub(r'<<<<<<< .*?\n(.*?)=======\n.*?>>>>>>> .*?\n', r'\1', content, flags=re.DOTALL)
        open(f, 'w').write(content)
```

### R0-2. Dead Link 스캔

```bash
# 무효 URL 패턴 검색 (사용자 지정 또는 자동 감지)
grep -rl "https://{dead_domain}" {target_folder}/ | wc -l
```

발견 시 링크 텍스트만 보존, URL 제거.

### R0-3. 레거시/중복 폴더 탐지

```
1. Glob으로 폴더 구조 스캔
2. 동일 파일명 중복 탐지
3. 빈 폴더 탐지
4. 사용자 확인 후 통합 — 제거 대상은 삭제하지 않고 `_archive/`로 이동
```

### R0-4. Auto-sync 보호

```bash
# 매 정리 작업 후 즉시 커밋
git add -A && git commit -m "Phase R0: pre-cleanup" && git push
```

> **Why**: Windows OneDrive/auto-sync 환경에서 지연 커밋 시 경합 발생.
> 얼룩소 프로젝트에서 auto-sync 경합으로 파일 덮어쓰기 경험.

---

## Phase R1: Progressive Reading + 분석

**목적**: 대상 파일 전체의 주제 클러스터, 시리즈, 교차 링크 파악.

### Progressive Reading 전략

```
Level 1: frontmatter + 첫 5줄 (전체 파일)
Level 2: 전문 읽기 (Hub 후보 + 분류 애매한 파일만)
```

> **Why**: 587편 전문 읽기는 비현실적. frontmatter + 첫 5줄로 90%+ 분류 가능.

### 파일 수에 따른 분석 전략

| 파일 수 | 전략 | 에이전트 |
|--------|------|---------|
| 50-100 | 단일 분석 | Lead 직접 또는 1 Explore |
| 100-300 | 2-3 병렬 분석 | Explore 에이전트 2-3개 |
| 300+ | 5 병렬 분석 | Explore 에이전트 5개 (얼룩소 패턴) |

### 에이전트 스폰 (AT 모드)

```
Task(analyst-{name}):
  subagent_type: "Explore"
  model: "sonnet[1m]"
  prompt: |
    {target_folder}의 파일들을 Progressive Reading으로 분석하세요.
    Level 1: frontmatter + 첫 5줄 스캔
    Level 2: 분류 애매한 파일만 전문 읽기

    산출물 형식:
    topic_clusters: [클러스터명, 멤버 파일 목록]
    series: [시리즈명, 멤버, 순서, 근거]
    reply_chains: [원글→답글 관계]
    hubs: [3+ 연결 가능한 노트]
    cross_links: [카테고리 A ↔ 카테고리 B 연결]
```

### 산출물 저장

```
.team-os/artifacts/analyst-{name}-result.txt
```

> **CRITICAL**: Explore 에이전트는 읽기 전용. 파일 저장은 Lead가 직접 수행.

---

## Phase R2: 카테고리 설계

**목적**: analyst 결과를 종합하여 카테고리 구조 확정.

### R2-1. 결과 종합

```
1. 모든 analyst-*-result.txt 읽기
2. topic_clusters 병합 → 카테고리 후보 도출
3. 중복/유사 클러스터 병합
4. 파일 수 균형 확인 (극단적 불균형 시 분할/병합)
```

### R2-2. CATEGORY_DESIGN.md 생성

```markdown
# Category Design

## 카테고리 구조

| # | 카테고리명 | 폴더 경로 | 예상 파일 수 | 설명 |
|---|----------|----------|------------|------|
| 1 | {name} | {folder} | {count} | {description} |

## 파일 분배 규칙

| 규칙 | 설명 |
|------|------|
| 주 카테고리 | 파일의 핵심 주제 기준 |
| 교차 카테고리 | 2개+ 카테고리에 관련 시 주 카테고리에 배치, 유사주제 링크로 연결 |
| 미분류 | '기타' 카테고리에 임시 배치, 추후 재분류 |
```

### R2-3. DA 검증 (km-rules-engine.md 참조)

```
DA에게 CATEGORY_DESIGN.md 제출
→ CONCERN 시 이슈 수정
→ ACCEPTABLE 시 동결
→ 최대 3회 반복
```

---

## Phase R3: 규칙서 생성

**목적**: 일관된 적용을 위한 규칙서 설계. 상세 패턴: `km-rules-engine.md` 참조.

### 규칙서 구성요소

| 구성요소 | 설명 |
|---------|------|
| Footer 템플릿 | `## 관련 노트` 구조 (시리즈, 유사주제, 답글/원글) |
| 시리즈 레지스트리 | 시리즈명, 멤버, 순서, 상태 |
| 교차 카테고리 링크 맵 | 카테고리 A ↔ B 연결 규칙 |
| 허브 노트 목록 | 3+ 연결 가능한 허브 노트 |
| MOC 계획 | 메인 MOC + 카테고리별 MOC 구조 |

### 규칙서 생성 절차

```
1. analyst 결과 + CATEGORY_DESIGN.md 종합
2. {TARGET}_RULES.md 초안 작성
3. 3개 예시 파일에 시범 적용
4. DA 검증 (CONCERN → 수정 → ACCEPTABLE)
5. 규칙서 동결 → .team-os/artifacts/{TARGET}_RULES.md 저장
```

### Footer 템플릿 (검증된 패턴)

```markdown
---

## 관련 노트

### 같은 시리즈
- [[시리즈 글 제목]] — n/N편

### 유사 주제
- [[관련 글 제목]] — 연결 근거 키워드

### 답글/원글
- 원글: [[원글 제목]]
- 답글: [[답글 제목]]

---
← [[카테고리-MOC|카테고리명]] · [[메인-MOC|전체 목록]]
```

> **빈 섹션 규칙**: 해당 없는 섹션은 ### 헤더 자체를 생략. 빈 헤더 금지.

---

## Phase R4: 배치 실행

**목적**: 동결된 규칙서를 전체 파일에 일괄 적용. 상세 패턴: `km-batch-python.md` 참조.

### CRITICAL: 실행 주체 규칙

| 허용 | 금지 |
|------|------|
| Lead가 Python 스크립트 생성 + 직접 실행 | Agent Teams 팀원에게 쓰기 위임 |
| Lead가 Bash로 스크립트 실행 | Task 에이전트에게 Write/Bash 위임 |

> **Why**: Agent Teams worktree 버그로 팀원의 파일 수정이 TeamDelete 시 유실됨.
> 얼룩소 프로젝트에서 실제 발생 → Python 폴백으로 해결.

### 실행 순서

```
1. /tmp/에 Python 스크립트 생성
2. --dry-run으로 변경 예정 파일 수 확인
3. 사용자 승인
4. 실행 → 즉시 git add + commit + push
5. Glob/Read로 5개 랜덤 파일 spot-check
6. 다음 스크립트로 진행
```

### 표준 스크립트 목록

| 스크립트 | 용도 |
|---------|------|
| `apply_footers.py` | 전체 파일에 관련 노트 푸터 삽입/교체 |
| `update_mocs.py` | MOC 파일 생성/강화 |
| `restructure.py` | 폴더 재구조화 (파일 이동) |
| `fix_frontmatter.py` | frontmatter 배치 수정 (태그, 카테고리) |
| `remove_dead_links.py` | dead link 일괄 제거 |

### 개별 파일 이동 (소량, 비배치)

소량이라도 이동 후 링크 수정은 똑같이 필요하다.

```bash
V="/Users/kbg1023/obsidian/Obsidian 2025"

# 1. 그 노트를 가리키는 링크가 어디 있는지 먼저 찾는다
grep -rl "\[\[old-note" "$V" --include='*.md'

# 2. 옮긴다
mv "$V/002. Folder/old-note.md" "$V/200. Literature/old-note.md"

# 3. 찾은 파일들의 링크를 고친다 (파일명이 그대로면 3단계는 불필요 —
#    Obsidian은 파일명으로 해석하므로 폴더만 바뀐 경우 링크는 살아 있다)
```

> 폴더만 바꾸고 **파일명을 유지하면 링크는 깨지지 않는다.**
> 이름까지 바꿀 때만 링크 수정이 필요하다. 재편에서 이름 변경은 되도록 피한다.

---

## Phase R5: 검증 + 보고

**목적**: 전체 적용 결과 검증 + 요약 보고서 생성.

### R5-1. 자동 검증

깨진 링크 검증은 직접 짜지 말고 이미 있는 스크립트를 쓴다 —
링크 해석 규칙(경로 우선, 동명 처리, 코드블록 제외)이 이미 맞춰져 있다.

```bash
# 재편 전에 한 번, 후에 한 번. 깨진 링크가 늘었으면 재편이 망친 것이다.
python "$HOME/.claude/skills/km-link-audit/scripts/vault_graph.py" \
  --vault "/Users/kbg1023/obsidian/Obsidian 2025" --folder "{대상폴더}" --top 30
```

푸터 커버리지만 따로 세면 된다:

```python
import glob
files = glob.glob(r"{target}/**/*.md", recursive=True)
has = [f for f in files
       if "## 관련 노트" in open(f, encoding="utf-8", errors="replace").read()]
print(f"푸터 {len(has)}/{len(files)} = {len(has)/len(files)*100:.1f}%")
```

### R5-2. 검증 기준

| 지표 | 목표 |
|------|------|
| 푸터 커버리지 | 100% (모든 대상 파일) |
| MOC 완전성 | 100% (모든 파일이 해당 MOC에 등록) |
| 깨진 wikilink | 0개 |
| 시리즈 양방향 링크 | 100% (A→B이면 B→A도 존재) |

### R5-3. 보고서 생성

```markdown
## Archive Reorganization Report

### 대상
- 폴더: {target_folder}
- 파일 수: {total_files}

### 결과
| 지표 | 결과 |
|------|------|
| 카테고리 | {N}개 |
| 시리즈 | {N}개 |
| MOC | {N}개 |
| 푸터 커버리지 | {N}/{total} ({pct}%) |
| 깨진 wikilink | {N}개 |

### 주요 변경
- 이동된 파일: {N}
- 추가된 링크: {N}
- 생성된 MOC: {N}

### DA 검증
- CATEGORY_DESIGN: {ACCEPTABLE/CONCERN}
- RULES: {ACCEPTABLE/CONCERN}
- 반복 횟수: {N}
```

---

## 참조 스킬

| 스킬 | 용도 |
|------|------|
| `km-rules-engine.md` | 규칙서 설계 + DA 검증 패턴 |
| `km-batch-python.md` | Python 배치 실행 + auto-sync 보호 |
| `km-export-formats.md` | 노트 출력 형식 |
| `drawio-diagram.md` | 작업 과정 시각화 |

## 검증된 사례

- **얼룩소 아카이브 재편** (2026-02-25): 587편, 8카테고리, 34시리즈, 100% 커버리지
  - 문서: `Library/Research/얼룩소-아카이브/얼룩소-아카이브-작업과정-2026-02-25.md`
  - 커밋: `b49799c`
