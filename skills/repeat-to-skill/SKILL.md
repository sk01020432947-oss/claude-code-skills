---
name: repeat-to-skill
description: 지난 N일 Claude Code 세션 기록(~/.claude/projects/*.jsonl)에서 내가 3번 이상 비슷하게 입력한 요청을 찾아 "스킬 후보"로 뽑고, 이미 설치된 스킬과 겹치는지 함께 보여준다. "같은 말 세 번 했으면 스킬로 빼라"는 원칙을 기계로 확인하는 도구. "반복 요청 찾아줘", "스킬 후보 뽑아줘", "내가 자주 시키는 일", "뭘 스킬로 만들까", "반복 작업 점검" 요청에 쓴다. 스킬을 실제로 만드는 건 anthropic-skills:skill-creator·superpowers:writing-skills, 만들기 전 외부 탐색은 skill-scout, 설치된 스킬 품질 점검은 skill-stocktake.
---

# repeat-to-skill — 세 번 반복한 요청 → 스킬 후보

근거: 베비투스의 AI 아틀리에, 「같은 말 세 번 했으면 스킬로 빼세요」(2026-09-12, https://www.youtube.com/watch?v=24Bgx6O22tA).

## 실행

```bash
python3 ~/.claude/skills/repeat-to-skill/scripts/scan.py --days 30
# 옵션: --min 3 (서로 다른 세션 수) --sim 0.35 (단어 겹침 기준, 낮출수록 넓게 묶음) --top 15
```

출력 한 묶음 = `N회 · 세션 M곳 · 기간 / 예시 문장 / 가장 가까운 스킬(겹침 점수)`.
겹침 0.25 이상이면 "이미 있음 → 그 스킬을 부르면 됨", 미만이면 "스킬 후보".

## 판정 다음

1. 후보마다 사용자에게 보여주고 고르게 한다. 만들 대상은 사용자가 정한다.
2. 고른 후보는 전역 규칙 7대로 중복 판정을 먼저 한다(설치 스킬 description 대조, 필요하면 skill-scout).
3. 덮이지 않으면 skill-creator로 만든다. 예시 문장 3개를 SKILL.md 트리거 문구로 쓴다.

## 한계

- 단어 겹침(Jaccard)만 쓴다. 뜻은 같고 단어가 다른 요청은 못 묶는다 → `--sim`을 0.25까지 낮춰 본다.
- 하네스·서브에이전트가 넣은 문장은 머리말로 거른다(`NOISE`). 새 잡음이 보이면 거기에 한 줄 추가.
- 1,500자 넘는 붙여넣기는 건너뛴다.
