# 웹 발행 절차 (Artifact)

1. `artifact-design` 스킬 로드(페이지 계약). 남이 쓴 HTML·md는 **끝까지 Read**한 뒤에만 발행.
2. 사본 만들기 (`<폴더>/_웹발행/`):
   - 소책자·강의안: `python3 scripts/webcopy.py 원본.html _웹발행/원본.html "<제목> 소책자|강의안"` — 껍데기·meta 제거, 인쇄 버튼/P키 제거(뷰어에서 print() 불가).
   - 논고: `python3 scripts/md2web.py 논고.md _웹발행/논고_<제목>.html "<제목>" "<부제>" "김병곤 · 우리동네작은교회" "<날짜>"`
   - 응용가이드: 껍데기 제거 + dark 블록에 `color-scheme:dark` + §산출물 표를 아티팩트 URL로 교체(로컬 상대링크는 웹에서 깨진다). 그래서 **응용가이드는 마지막에** 발행.
3. 발행: 첫 발행에 `icon`(book/slides/document/compass)과 한 문장 `description`. 제목은 "<제목> 소책자" 식으로 서로 구별.
4. URL 기록: 옵시디언 허브 노트 `## 웹 발행` 섹션 + 메모리 reference 파일(재발행 시 재사용, 규칙 1).
5. 사용자에게: 비공개라 Share 메뉴에서 공유해야 남이 열 수 있음, 응용가이드 안의 링크도 각 페이지가 공유돼야 열림.
