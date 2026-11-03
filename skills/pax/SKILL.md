---
name: pax
description: 공공AX 사례 아카이브(PAX, hollobit.github.io/PAX) 검색·인용. 사용자가 공공부문 AI 도입·AI전환(AX) 사례, 지자체·중앙부처·공공기관·교육청·복지·돌봄·상담 현장의 AI 활용 사례, 공무원이 만든 AI 도구·MCP, AX 성숙도, 정부 AI 가이드라인 근거, 공공AX 관련 뉴스·영상, 공공 MCP 보안·품질 점검, 공공AX 실천가(챔피언), 사례별 AX 단계 평가를 요구하거나, 강의안·논문·뉴스레터·보고서에 국내 공공 AI 사례가 들어갈 자리가 있으면 사용한다. 로컬 캐시가 8시간 넘게 지나면 원본에서 자동 갱신한다.
---

# PAX 사례 인용

1. 검색 (8시간 넘으면 자동으로 최신본을 받는다):
   ```bash
   python3 ~/.claude/skills/pax/pax.py <키워드...> [-n 10] [--org-type 지방자치단체] [--refresh]
   ```
   키워드는 동의어를 여러 개 넣는다(예: `복지 돌봄 사례관리 상담`). 일치가 적으면 키워드를 바꿔 다시 찾는다.
2. 인용 규칙:
   - 결과의 요약·기관·날짜만 쓴다. 출력에 없는 내용은 지어내지 않는다.
   - 본문에 `[PAX-1]` 식 번호를 달고, 끝에 참고 목록: `[PAX-1] 제목 — 기관(유형), 날짜. 출처 링크. 모두의 공공AX 사례 아카이브(PAX), hollobit.github.io/PAX, YYYY-MM-DD 접속.`
   - 출력 첫 줄의 "PAX 원본 갱신" 시각을 기준 시점으로 밝힌다.
   - PAX는 자발 제보 표본이라 공공부문 전체를 대표하지 않는다 — 통계·일반화 주장에 쓸 때 이 한계를 함께 적는다.
3. 사례 외 아카이브 (같은 명령에 `--in <이름>`, 키워드는 모두 포함(AND) 일치, 8시간 자동 갱신, 캐시 `data/`):
   | `--in` | 내용 |
   |---|---|
   | `news` | 공공AX 기사·글 1,200여 건(제목·매체·게시일·공유 수) |
   | `videos` | 공공AX 영상 120여 건(제목·채널·링크) |
   | `mcp` | 공공 MCP 도구 점검 리뷰(권한 범위·동적 점검·종합 판정) |
   | `evals` | 사례별 AX 성숙도 평가(ax 단계·S/C/M 축) |
   | `champions` / `unattributed` | 공공AX 실천가(공개 계정·소속·사례) / 제작자 미상 사례 |
   | `changelog` | 사이트 갱신 기록(날짜별) |
   | `index` · `community` · `dashboard` | 분기 집계 통계 / 커뮤니티 현황 / 일별 대시보드 이력 (키워드 없이 통째 출력) |
   - 실천가 데이터에는 실명·계정이 있다 — 공개 프로필 근거만 인용하고, 개인을 평가·순위 매기는 데 쓰지 않는다.
   - 뉴스·영상은 PAX가 모은 링크 목록이다. 내용을 인용하려면 원문 링크를 열어 확인한다.
4. HTML 전용 페이지(필요할 때만 WebFetch):
   - AX 성숙도 4단계(AI-Ready→Enabled→First→Native)+S/C/M 축: https://hollobit.github.io/PAX/ax-maturity-infographic.html
   - 정부 AI 가이드라인 단계별 매핑: https://hollobit.github.io/PAX/guidelines.html
   - 우수기관: https://hollobit.github.io/PAX/champions.html · 평가 대시보드: https://hollobit.github.io/PAX/dashboard.html
   - 그 밖의 화면(위 데이터를 시각화): 플레이북 playbook.html · 관측소 observatory.html · 부처별 공백지도 gap-map.html · 3D 지도 pax3d.html · MCP 리뷰 mcp-review.html — 모두 https://hollobit.github.io/PAX/ 아래. 데이터가 필요하면 화면보다 위 `--in` 검색을 쓴다.
