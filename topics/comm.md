# 커뮤니케이션·원격·협업 (24개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/comm.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-comm && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-comm && cd /tmp/ccs-comm && git sparse-checkout set skills/gws-calendar skills/gws-calendar-agenda skills/gws-calendar-insert skills/gws-classroom skills/gws-docs skills/gws-docs-write skills/gws-drive skills/gws-drive-upload skills/gws-forms skills/gws-gmail skills/gws-gmail-read skills/gws-gmail-reply skills/gws-gmail-send skills/gws-gmail-triage skills/gws-shared skills/gws-sheets skills/gws-sheets-append skills/gws-sheets-read skills/gws-slides skills/gws-tasks skills/gws-workflow skills/gws-workflow-meeting-prep skills/gws-workflow-weekly-digest skills/nopal && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [gws-calendar](../skills/gws-calendar) | Google Calendar: Manage calendars and events. |  |
| [gws-calendar-agenda](../skills/gws-calendar-agenda) | Google Calendar: Show upcoming events across all calendars. |  |
| [gws-calendar-insert](../skills/gws-calendar-insert) | Google Calendar: Create a new event. |  |
| [gws-classroom](../skills/gws-classroom) | Google Classroom: Manage classes, rosters, and coursework. |  |
| [gws-docs](../skills/gws-docs) | Read and write Google Docs. |  |
| [gws-docs-write](../skills/gws-docs-write) | Google Docs: Append text to a document. |  |
| [gws-drive](../skills/gws-drive) | Google Drive: Manage files, folders, and shared drives. |  |
| [gws-drive-upload](../skills/gws-drive-upload) | Google Drive: Upload a file with automatic metadata. |  |
| [gws-forms](../skills/gws-forms) | Read and write Google Forms. |  |
| [gws-gmail](../skills/gws-gmail) | Gmail: Send, read, and manage email. |  |
| [gws-gmail-read](../skills/gws-gmail-read) | Gmail: Read a message and extract its body or headers. |  |
| [gws-gmail-reply](../skills/gws-gmail-reply) | Gmail: Reply to a message (handles threading automatically). |  |
| [gws-gmail-send](../skills/gws-gmail-send) | Gmail: Send an email. |  |
| [gws-gmail-triage](../skills/gws-gmail-triage) | Gmail: Show unread inbox summary (sender, subject, date). |  |
| [gws-shared](../skills/gws-shared) | gws CLI: Shared patterns for authentication, global flags, and output formatting. |  |
| [gws-sheets](../skills/gws-sheets) | Google Sheets: Read and write spreadsheets. |  |
| [gws-sheets-append](../skills/gws-sheets-append) | Google Sheets: Append a row to a spreadsheet. |  |
| [gws-sheets-read](../skills/gws-sheets-read) | Google Sheets: Read values from a spreadsheet. |  |
| [gws-slides](../skills/gws-slides) | Google Slides: Read and write presentations. |  |
| [gws-tasks](../skills/gws-tasks) | Google Tasks: Manage task lists and tasks. |  |
| [gws-workflow](../skills/gws-workflow) | Google Workflow: Cross-service productivity workflows. |  |
| [gws-workflow-meeting-prep](../skills/gws-workflow-meeting-prep) | Google Workflow: Prepare for your next meeting: agenda, attendees, and linked docs. |  |
| [gws-workflow-weekly-digest](../skills/gws-workflow-weekly-digest) | Google Workflow: Weekly summary: this week's meetings + unread email count. |  |
| [nopal](../skills/nopal) | Google Workspace 오케스트레이션 — 자연어로 9개 서비스를 자동 조합 Gmail·Calendar·Drive·Sheets·Docs·Slides·Chat·Tasks·Meet을 gws CLI로 조합한다. 읽기 조회는 바로 실행하고 쓰기·변경은  |  |
