---
name: gemini-skill-export
description: 설치된 Claude 스킬(~/.claude/skills/<이름>)을 제미나이 앱 '스킬'(설정 > 스킬 > 업로드)에 올릴 수 있는 .zip으로 변환하고 규격을 점검한다. name 소문자-하이픈, description 1024자, 100MB, 미지원 형식(.docx/.xlsx/.hwp 등) 제외, MCP·Bash 등 Claude 전용 의존 경고. "제미나이 스킬로 옮겨", "Gemini 스킬 업로드용으로", "스킬을 폰에서도 쓰게", "/gemini-skill-export" 요청 시 사용. Gems용 프롬프트 생성(prompt-sync-gems)과 다르다 — 여기는 SKILL.md 그대로 이식.
---

# Claude 스킬 → 제미나이 스킬 이식

제미나이 앱 스킬(2026-09-30 출시)은 Anthropic이 시작한 SKILL.md 공개 규격을 그대로 받는다. 그래서 변환은 '번역'이 아니라 '규격 점검 + 포장'이다.

## 실행

```bash
python3 ~/.claude/skills/gemini-skill-export/export.py <스킬이름> [<스킬이름> ...]
```

- 결과: `~/Desktop/cysjavis/AI동향_검토/제미나이스킬_업로드팩/<name>.zip`
- 업로드가 거부되면 `--nested`로 다시 만든다(zip 안을 `<name>/SKILL.md` 구조로).
- 자체 점검: `python3 export.py --demo`

## 이식 전에 고를 것

| 잘 옮겨지는 스킬 | 옮겨도 반쪽인 스킬 |
|---|---|
| 글쓰기·문체·양식 지침(설교→블로그, 소그룹 질문, 공지문) | MCP 도구 호출(logos, korean-law, 공공데이터) |
| 참고문서(md/csv/pdf)를 읽고 답하는 비서 | 웹 검색·API 호출 스크립트(외부 접속 차단) |
| 썸네일·이미지 스타일 지침 | Bash·서브에이전트·파일 쓰기 파이프라인 |

## 업로드 후

1. gemini.google.com 또는 맥 앱 → 설정 > 스킬 > 업로드 → zip 선택.
2. 새 채팅에서 `/` → 스킬 이름 선택 → 요청 입력.
3. 두 개를 이어 부르면 함께 적용된다(스킬 스태킹).
4. 개인 구글 계정(만 18세 이상)만 된다. Workspace 계정은 아직 미지원.
