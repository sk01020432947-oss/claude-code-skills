---
name: hop-desktop
description: HOP(golbin/hop, 오픈소스 HWP/HWPX 데스크톱 앱)로 한글 문서를 사람 눈으로 열람·확인·PDF 내보내기 할 때 사용. "HOP로 열어줘", "hwp 미리보기", "만든 hwpx 화면으로 확인", "Finder에서 hwp 썸네일", "한컴 없이 hwp 열기", "HOP 설치" 요청 시. 파싱·변환은 hwp/read-hwp(kordoc), 바이너리 편집은 rhwp-edit, 레이아웃 디버그는 rhwp-advanced, HWPX 생성은 hwpx 계열 스킬을 쓰고 이 스킬은 마지막 '눈 검수·배포' 단계만 맡는다.
---

# hop-desktop

HOP = rhwp 엔진(Rust+WASM) 위에 Tauri 2로 씌운 얇은 데스크톱 셸. CLI는 없다. 에이전트가 할 수 있는 일은 **설치 확인 → 파일 열기 → Quick Look 미리보기**까지이고, 저장·PDF 내보내기·인쇄는 사용자가 앱에서 누른다.

## 1. 설치 확인

```bash
ls -d /Applications/HOP.app 2>/dev/null || brew info --cask hop | head -3
```

없으면 사용자에게 아래 명령을 제안만 한다(설치는 사용자 승인 후).

```bash
brew install --cask hop
```

## 2. 열기 (시각 검수)

```bash
open -a HOP "/절대/경로/문서.hwpx"
```

- 한글 경로는 python3 `subprocess.run(["open","-a","HOP",path])`로 넘긴다(NFD 문제 회피).
- 다른 스킬로 만든/고친 문서는 여기서 열어 표·글꼴·쪽 넘김을 눈으로 확인하게 안내한다.

## 3. Finder 미리보기 (macOS 12+, HOP 번들의 Quick Look 확장)

```bash
qlmanage -p "/경로/문서.hwp"            # 미리보기 창
qlmanage -t -s 512 -o /tmp "/경로/문서.hwp"  # 첫 쪽 PNG 썸네일
```

한컴 뷰어가 같은 UTI를 잡고 있으면 HOP 미리보기가 안 뜰 수 있다 → `qlmanage -r` 후 재시도.

## 4. 사용자에게 안내할 앱 기능(v0.4.5 기준)

| 기능 | 상태 |
|---|---|
| HWP/HWPX 열기, 다중 창, 드래그&드롭, 파일 연결 | 지원 |
| HWP 저장/다른 이름 저장(원자적 저장, 외부 변경 감지) | 지원 |
| HWPX 저장 | **막혀 있음** → HWP로 Save As 또는 hwpx 스킬로 생성 |
| PDF 내보내기(텍스트 검색 가능, rhwp v0.8.4+) | 지원 |
| 인쇄, 다크 테마, 암호 문서 열기 | 지원 |
| autosave/복구 | 없음 → 자주 Cmd+S |

단축키: Cmd+S 저장, Cmd+Shift+S 다른 이름, Cmd+P 인쇄, Cmd+F 찾기, Cmd+F2 바꾸기, Alt+L 글자모양, Alt+T 문단모양, F6 스타일.

## 경계

- 문서 내용·경로를 로그/외부 서비스로 보내지 않는다.
- HOP 대신 한컴 오피스가 필요한 경우: 누름틀·매크로·정밀 조판 최종본.
