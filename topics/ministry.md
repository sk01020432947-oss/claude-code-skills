# 목회·교회 사역 (16개)

## 설치

**Claude Code 채팅창에 아래 한 줄을 붙여 넣습니다.**

```
https://github.com/sk01020432947-oss/claude-code-skills/blob/main/topics/ministry.md 를 읽고, 거기 적힌 스킬을 모두 ~/.claude/skills/ 에 설치해줘
```

클로드가 할 일: 아래 명령으로 이 주제의 스킬 폴더만 내려받아 `~/.claude/skills/`에 복사한다(Windows는 `%USERPROFILE%\.claude\skills\`). 같은 이름의 스킬이 이미 있으면 덮어쓰지 않는다. 끝나면 설치한 스킬 수를 알려 주고 Claude Code를 다시 시작하라고 안내한다.

```bash
rm -rf /tmp/ccs-ministry && git clone --depth 1 --filter=blob:none --sparse https://github.com/sk01020432947-oss/claude-code-skills.git /tmp/ccs-ministry && cd /tmp/ccs-ministry && git sparse-checkout set skills/ai-license-3day skills/announcement-script skills/church-admin-assistant skills/church-comment-reply skills/church-email skills/church-letter skills/church-social-post skills/meeting-agenda skills/midweek-devotional skills/next-gen-ministry-bible skills/pastor-ai-safety-guide skills/pastor-foundation skills/pastoral-prompt-engineering skills/school-ministry-radar skills/small-group-questions skills/social-media-calendar && mkdir -p ~/.claude/skills && cp -Rn skills/. ~/.claude/skills/; ls skills | wc -l
```

외부 오픈소스에서 온 스킬은 각 `SKILL.md`의 license·저자 표기를 따릅니다.

## 수록 스킬

| 스킬 | 기능 | 부르는 말 |
|---|---|---|
| [ai-license-3day](../skills/ai-license-3day) | AI 입문자에게 '3일 AI 면허' 코스(정거장 9개 + 보너스 커넥터)를 대상 맞춤으로 만들어 주는 교육 설계 스킬. 청중(교사·목회자·교인 시니어·사회복지사·청년·소상공인 등)과 시간(90분 특강/3일 과정/소그룹 3회)을 받아 정거장별 미션 카드 |  |
| [announcement-script](../skills/announcement-script) | 주일 아침 광고용 60~90초 구두 안내 대본 작성. 대화체, 우선순위 정리, 최대 3~4개 항목. 아무도 졸지 않는 광고. |  |
| [church-admin-assistant](../skills/church-admin-assistant) | 교회행정 비서. 첨부된 연간계획(CSV)·교회요람·문체가이드를 근거로 주보 광고, 교회소식, 카톡·문자 공지, 행사 안내문, 월간 일정표, 일정·장소 문의 답변을 쓴다. 파일에 없는 날짜·시간·장소는 지어내지 않고 [확인 필요]로 표시한다. "주보 광 | 주보 광고 써줘·이번 주 교회소식·11월 일정 정리 |
| [church-comment-reply](../skills/church-comment-reply) | 교회에 달린 댓글·후기·문의(유튜브 설교 영상 댓글, 인스타·페이스북 댓글, 카카오 채널 문의, 구글 지도 리뷰)에 답글 초안을 3가지 버전으로 쓴다. "댓글 답글 써 줘", "이 문의에 답장", "리뷰 답글" 요청이나 댓글 캡처를 받았을 때 쓴다. | 댓글 답글 써 줘·이 문의에 답장·리뷰 답글 |
| [church-email](../skills/church-email) | 주간 교회 이메일 완성본 작성. 제목·미리보기 텍스트·본문까지. 따뜻하고 훑어보기 좋고 모바일 친화적. 광고와 행사 내용을 붙여넣으면 바로 보낼 수 있는 이메일이 나온다. |  |
| [church-letter](../skills/church-letter) | 모든 상황에 맞는 교회 서신 작성. 리더십 교체, 시설 안내, 정책 변경, 환영 편지, 민감한 소통까지. 상황에 맞는 무게감을 갖춘 목회적 어조. |  |
| [church-social-post](../skills/church-social-post) | 교회용 플랫폼별 SNS 게시물 작성. 주제·행사·성경구절을 주면 Facebook·Instagram·Twitter용 캡션과 이미지 제안을 플랫폼별로 최적화해 돌려준다. |  |
| [meeting-agenda](../skills/meeting-agenda) | 시간 블록·토론 질문·액션아이템 프롬프트가 있는 구조화된 회의 안건 작성. 교역자 회의, 장로회, 제직회, 봉사자 모임에 사용. |  |
| [midweek-devotional](../skills/midweek-devotional) | 이메일이나 앱으로 보내는 짧은 주중 묵상글(200~300단어) 작성. 성경 기반, 개인적, 따뜻한 톤. 주일과 주일 사이 성도들과의 연결을 유지. |  |
| [next-gen-ministry-bible](../skills/next-gen-ministry-bible) | 『다음세대 목회 바이블 — 일곱개의 사랑이 만드는 한 해의 기적』(안세주 저, 총회 교육훈련처, 7 LOVE Project) 전체를 기반으로 교회학교·다음세대 사역을 설계하는 스킬. 12개월 상세 로드맵(1월 RESET~12월 LOVE CELEBRAT | 다음세대·교회학교 프로그램·주일학교 |
| [pastor-ai-safety-guide](../skills/pastor-ai-safety-guide) | 목회자를 위한 인공지능 안전 활용 가이드 스킬. 『인공지능 안전 활용 가이드북 50선』을 기반으로 (1) 목회 업무에 맞는 안전 프롬프트 처방(50선 라이브러리 + 안전 강화판), (2) AI 산출물의 환각·이단성·비성경적 요소 검증, (3) AI 입 | AI 안전 가이드·인공지능 안전 활용·안전 프롬프트 |
| [pastor-foundation](../skills/pastor-foundation) | 모든 목회자 AI 스킬의 공유 컨텍스트 레이어. 신학적 가드레일, 목회적 어조, 교회 컨텍스트 변수, 산출물 표준을 설정한다. 다른 작업 스킬과 함께 설치. |  |
| [pastoral-prompt-engineering](../skills/pastoral-prompt-engineering) | 이경석 저 『목회 프롬프트 엔지니어링』(2026) 기반의 목회·사역용 프롬프트 설계 스킬. 목회 현장의 문서·기획·교육·연구·미디어·로컬비즈니스 과업을 CRIT/BAB/CARE/RISE/RTF 프레임워크와 골든 프롬프트 50선 템플릿으로 처리한다. 트 | 목회 프롬프트·골든 프롬프트·프롬프트 짜줘/설계해줘 |
| [school-ministry-radar](../skills/school-ministry-radar) | 교회학교·청소년부·청년부 사역을 지역 학교 데이터와 맞물리게 하는 레시피 스킬. 이미 설치된 korean-school MCP(우리학교 알리미, mcp.gomdori.app/school)로 출석 학생들 학교의 시험기간·학사일정·학교 규모를 모아 ① 수련 | 시험기간 피해서 수련회·우리 아이들 학교 시험 언제·교회학교 학사일정 |
| [small-group-questions](../skills/small-group-questions) | 주일 설교 기반 주간 소그룹 토론 질문 생성. 관찰→해석→적용 흐름. 아이스브레이커와 마무리 기도 제목 포함. 소그룹 리더에게 바로 전달 가능. |  |
| [social-media-calendar](../skills/social-media-calendar) | 1주 또는 1개월치 SNS 콘텐츠를 날짜별로 생성. 다가오는 설교·행사·강조점을 주면 게시물 아이디어·유형·플랫폼 배정이 있는 구조화된 캘린더를 돌려준다. |  |
