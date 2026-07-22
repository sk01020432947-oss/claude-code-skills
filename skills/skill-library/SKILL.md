---
name: skill-library
description: 내 스킬 폴더(~/.claude/skills) 전체를 스캔해 카테고리별로 분류하고, 공유용 ZIP과 검색·복사 가능한 HTML 카탈로그를 만들어 아티팩트 링크로 게시하는 스킬. 사용자가 "내 스킬 정리해줘", "스킬 목록 뽑아줘", "스킬 공유하고 싶어", "스킬 나눠줄게", "스킬 카탈로그 만들어줘", "스킬 라이브러리", "스킬 몇 개야", "스킬 분류해줘", "새 스킬 카탈로그에 반영해줘", "/skill-library"를 언급하거나, 자기 스킬 자산을 남에게 배포·전달·정리하려 할 때 발동한다. 카탈로그를 다시/재생성/갱신/업데이트하거나 새로 만든 스킬을 반영할 때도 이 스킬을 사용한다.
---

# 스킬 라이브러리 — 스캔·분류·공유 패키징

내 스킬 자산을 **남이 골라 가져갈 수 있는 형태**로 만든다. 산출물 3종:

| 산출물 | 경로 | 용도 |
|---|---|---|
| 인벤토리 JSON | `~/.claude/skills-inventory.json` | 중간 데이터 (스킬명 + description) |
| 공유용 ZIP | `~/Documents/claude-skills-share-<날짜>.zip` | 받는 사람이 압축 풀어 설치 |
| HTML 카탈로그 | `~/Documents/skills-catalog.html` + 아티팩트 링크 | 무엇이 있는지 보고 고르는 화면 |

## 실행 순서

### 1. 스캔 + 카탈로그 생성

```bash
python ~/.claude/skills/skill-library/scripts/build_catalog.py
```

이 한 줄이 스캔·분류·HTML 생성을 모두 한다. `~/.claude/skills/*/SKILL.md`의 frontmatter `description`을 읽어 인벤토리를 만들고, 카테고리별로 묶어 카탈로그를 쓴다.

**출력을 반드시 확인한다.** 두 줄이 핵심이다:

- `unmapped: [...]` — 분류 규칙에 안 걸린 새 스킬. 비어 있어야 정상.
- `english w/o translation: [...]` — 한글 번역이 없는 영어 description. 비어 있어야 정상.

둘 중 하나라도 항목이 있으면 **스크립트를 고치고 재실행한다** (아래 "새 스킬이 추가됐을 때" 참조). 항목이 남은 채로 게시하지 않는다.

### 2. 비밀정보 스캔 (ZIP 만들기 전 필수)

남에게 주는 파일이다. API 키가 섞여 나가면 되돌릴 수 없다.

```bash
cd ~/.claude/skills && grep -rIlE "(sk-[A-Za-z0-9]{20,}|sk_[A-Za-z0-9]{20,}|xi-api-key[\"': ]+[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,}|Bearer [A-Za-z0-9_\-\.]{30,}|api_keys?\s*[:=]\s*[\"'][A-Za-z0-9_-]{25,})" . 2>/dev/null
```

출력이 있으면 **ZIP을 만들지 말고** 해당 파일을 사용자에게 보고한다. 출력이 없으면 진행.

### 3. ZIP 패키징

PowerShell로 압축한다 (`날짜`는 오늘 날짜, 예: `2026-07-22`):

```powershell
$dest = "$env:USERPROFILE\Documents\claude-skills-share-<날짜>.zip"
if (Test-Path $dest) { Remove-Item $dest -Force }
Compress-Archive -Path "$env:USERPROFILE\.claude\skills\*" -DestinationPath $dest -CompressionLevel Optimal
```

240개 규모에서 약 12MB, 1~2분 걸린다. timeout을 300000으로 준다.

### 4. 아티팩트 게시

Artifact 도구로 `~/Documents/skills-catalog.html`을 게시한다. favicon은 `📚` 고정.

**갱신일 때는 반드시 이전 URL을 재사용한다** — `data/artifact-url.txt`에 기록된 URL을 `url` 파라미터로 넘긴다. 이 파일이 있는데 그냥 게시하면 새 링크가 발급되어 이미 공유한 링크가 낡는다. 최초 게시라면 반환된 URL을 이 파일에 적어 둔다.

### 5. 사용자에게 전달

SendUserFile로 ZIP과 HTML을 보내고, 아티팩트 링크와 카테고리별 개수 표를 답변에 담는다. **아티팩트는 기본 비공개**이므로, 남에게 보이려면 페이지 공유 메뉴에서 직접 공개해야 한다는 점을 반드시 안내한다.

## 새 스킬이 추가됐을 때

`scripts/build_catalog.py` 상단의 두 곳만 고치면 된다. HTML/CSS는 건드릴 일이 거의 없다.

**분류 추가** — `put()` 호출에 이름을 넣거나, 접두사 규칙이면 `category()` 함수에 한 줄 추가:

```python
put('ministry', 'new-church-skill')          # 개별 지정
if name.startswith('newprefix-'): return 'x' # 접두사 규칙
```

**번역 추가** — description이 영어면 `TRANSLATIONS` 딕셔너리에 한국어 번역을 넣는다. 원문은 지우지 않는다 — 카탈로그가 번역을 위에, 원문을 "원문 (English)" 라벨과 함께 아래에 자동 배치한다.

```python
TRANSLATIONS = {
    'skill-name': "한국어 번역문…",
}
```

**묶음(suite) 추가** — 부모-자식 스킬이 `parent-child` 이름 규칙을 따르면 `SUITE_PARENTS` 리스트에 부모 이름만 추가한다. 자식들이 부모 카드 안에 접혀 들어간다.

## 카테고리 설계 원칙

카테고리는 **폴더 구조가 아니라 쓰는 사람의 목적**으로 나눈다. 받는 사람이 "나는 설교를 준비한다" / "나는 공문서를 쓴다"로 자기 자리를 찾을 수 있어야 한다. 현재 15개 분류는 `CATS` 리스트에 정의되어 있고, 각 항목은 `(키, 표시명, 한 줄 설명)`이다.

한 카테고리가 40개를 넘어가면 쪼개는 것을 고려한다. 반대로 3개 미만이면 인접 카테고리에 합친다.

## 카탈로그가 갖춰야 할 것 (회귀 방지)

수정 시 아래가 깨지지 않았는지 확인한다:

- **복사 버튼** — 모든 카드(하위 스킬 포함)에 폴더명 복사 아이콘. 클립보드 API 실패 시 `execCommand` 폴백.
- **검색** — 카드 텍스트 전체 대상 실시간 필터, 결과 없는 섹션은 통째로 숨김.
- **번역 우선 배치** — 한국어 번역이 위, 영어 원문이 "원문 (English)" 아래.
- **양쪽 테마** — `prefers-color-scheme`와 `data-theme` 양방향 모두 동작.
- **설치 안내 4단계** — 받기 / 설치 / 사용 / 골라 가져가기. 준비물(API 키 필요 스킬) 경고 포함.

## 주의

- 카탈로그는 SKILL.md의 description만 읽는다. description이 부실한 스킬은 카탈로그에서도 부실하게 보인다 — 그런 스킬이 보이면 사용자에게 알린다.
- ZIP은 스킬 폴더를 통째로 담는다. 스킬 안에 개인 데이터 파일(수집한 자료, 로그)이 있으면 함께 나간다. 2단계 스캔은 API 키만 잡으므로, 용량이 유난히 큰 스킬 폴더가 있으면 내용을 확인한다.
