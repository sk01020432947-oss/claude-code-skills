# 생산성·유틸리티 (1개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/util.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-util && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-util && cd /tmp/ccs-util && git sparse-checkout set skills/folder-tidy-recipes && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [folder-tidy-recipes](../skills/folder-tidy-recipes) | 폴더 하나를 대상으로 하는 사무 정리 레시피 3종 — (1) 다운로드·스캔 폴더를 삭제후보/보관추천/확인필요로 분류만 하고 승인받기, (2) 영수증·증빙 사진을 엑셀로(확인필요·중복의심 표시), (3) 파일명 일괄 규칙 변경(전후 대조표). "다운로드 | 다운로드 폴더 정리·영수증 엑셀로·파일명 바꿔줘 |
