---
name: hycli-recipes
description: 김병곤 목사·교수의 Hycli 실행 레시피 모음. "복지 보도자료 모아줘", "블로그 임시저장", "hycli 점검", "사이트 도구로 만들어줘", "교회 홈페이지 공지", "LMS 공지 확인" 등 Hycli로 웹사이트 작업을 할 때 사용. 일반 동작 규칙은 hycli 스킬을 따르고, 이 스킬은 사용자 고유 작업 순서만 담는다.
---

# Hycli 레시피 (사용자 전용)

먼저 `hycli status`로 엔진이 도는지 보고, 꺼져 있으면 `hycli open --no-open`. 설치된 사이트는 `hycli describe`(또는 MCP `hycli_sites`)로 확인한다. 동작 이름은 추측하지 말고 describe 결과에서 고른다. 일반 규칙(쓰기 1회 허락, `action_outcome_unknown` 재시도 금지, 쿠키를 채팅에 받지 않기)은 `hycli` 스킬을 따른다.

인자로 레시피 이름이 오면 해당 절만 실행한다. 인자가 없으면 아래 목록을 보여주고 고르게 한다.

## 1. 복지보도자료 — 보건복지부 보도자료 주간 요약
- 사이트: `mohw-press` (직접 작성한 정의, 원본 `~/Desktop/cysjavis/매뉴얼/AI도구/hycli_specs/mohw-press.yaml`). 없으면 `hycli spec install` 그 파일. AI 준비 불필요.
- 동작: `hycli run mohw-press list-press-releases [--arg nPage=2] [--arg keyWord=아동 --arg keyField=TITLE|CONTENT|DEPT_NAME]` → `{items:[{no,title,url,dept,date,views}]}` (제목 앞 "새글 " 제거) / `read-press-release --arg list_no=N` → `{items:[{title,info,body}]}` / `list-attachments --arg list_no=N`. list_no는 url의 `list_no=` 값.
- 지난 7일치만 상세를 읽는다(첫 페이지 15건이면 대개 충분, 부족하면 nPage=2).
- 출력: 날짜·제목·담당부서·원문 링크 표 + 아동·청소년·노인·장애·사회보장 키워드별 3줄 요약 + "강의 활용 포인트(사회복지정책론/청소년복지론)".
- 저장: `~/Desktop/cysjavis/복지정책/보도자료_주간/YYYY-MM-DD_보건복지부_보도자료.md` (python3으로 한글 경로 처리).

## 2. 블로그임시저장 — 설교·글을 네이버 블로그 임시저장
- 전제: 계정 화면에서 네이버 계정이 `verified_identity: true`. 아니면 "대시보드 → 계정 → 다시 확인"을 안내하고 멈춘다.
- 사이트가 없으면 `hycli prepare https://blog.naver.com --language ko --intent "내 블로그 글 목록, 카테고리 목록, 임시저장 글 목록, 임시저장 글 작성·수정 (발행은 제외)"`. 결과의 `capability_gaps`를 그대로 보고한다. 네이버 스마트에디터는 브라우저 편집기라 임시저장 동작이 안 만들어질 수 있다.
- 원고는 먼저 `sermon-to-blog` 스킬로 다듬는다. 임시저장 실행 전 사용자에게 제목·카테고리를 보여주고 확인받는다. 처음이면 쓰기 허락 질문을 1회 한다. **발행 동작은 실행하지 않는다.**

## 3. 점검 — 로그인 만료·사이트 변경 확인
- `hycli check` 결과를 사이트별로 표로: `ok` / `signed_out`(대시보드에서 다시 로그인) / `site_changed`(`hycli request 사이트 "깨진 동작 수리"`) / `blocked` / `unreachable`.

## 4. 새사이트 — 새 웹사이트를 도구로 만들기
- 사용자에게 URL과 "하고 싶은 일"만 받는다. 먼저 AI 없이 `hycli recon URL`로 구조를 본 뒤 `hycli prepare URL --language ko --intent "..."`.
- 완료 후 `available_actions`, `coverage.uncovered`, `capability_gaps`를 쉬운 말로 요약한다.
- 금지 대상: 은행·결제·정부24·홈택스·본인인증 서비스, 교인 상담 기록, 학생 성적 화면.

## 5. 게시판감시 — 교단·학교·기관 게시판 새 글
- 해당 사이트의 목록 동작으로 첫 페이지만 읽고, `~/Desktop/cysjavis/ledger/hycli_게시판감시.json`에 저장된 지난 제목과 비교해 새 글만 보고한 뒤 파일을 갱신한다.

## 6. 기능추가 — 이미 만든 사이트에 기능 더하기
- `hycli request 사이트 "추가할 기능"` → 작업 결과의 `added_actions`, `capability_gaps`를 보고.
