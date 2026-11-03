---
name: laya-decide
description: 로컬 무료 의사결정 모델 Laya(Jev 오픈소스 대안)로 텍스트를 빠르게 분류·라우팅·점수화한다. 메일/문서/메모/댓글 대량 분류, 폴더·태그 자동 배정, 트리아지, 프롬프트 가드, "Jev", "Laya", "빠른 분류", "라우팅", "system one" 트리거. 긴 글 생성·요약이 필요하면 쓰지 않는다.
---

# Laya — 로컬 System-1 결정 엔진

설치: `~/.venvs/laya` (Python 3.12, Apache-2.0). 모델 캐시 `~/.cache/huggingface/hub/`.
MCP 자동 연결은 2026-10-02에 해제했다(세션마다 서버가 떠 메모리를 차지해서). 아래 파이썬·CLI로 쓴다. 다시 켜려면: `claude mcp add -s user laya -e LAYA_DEVICE=mps -- ~/.venvs/laya/bin/laya-mcp-server`

## 호출

```bash
~/.venvs/laya/bin/python - <<'EOF'
import laya
agent = laya.load("convaiinnovations/laya", subfolder="multilingual")  # 한국어는 반드시 multilingual
q = {"kind": {"type": "choice", "instructions": "이 글은 어떤 종류인가?",
              "criteria": {"billing": "결제·환불", "schedule": "일정", "spam": "광고", "other": "기타"}}}
print(agent.predict("어제 결제가 두 번 됐어요", q, min_confidence=0.7)["answers"])
EOF
```
- 대량: `agent.predict_batch([{"body": t} for t in texts], q, batch_size=32)`
- 긴 문서: `agent.predict_long(text, q, window=256)`
- CLI: `~/.venvs/laya/bin/laya "텍스트" --predict --model ml --json`
- HTTP(Jev 호환 `POST /v1/systemone`): `LAYA_DEVICE=mps LAYA_HOST=127.0.0.1 ~/.venvs/laya/bin/laya-serve`

## 실측 한계 (2026-09-29, M-시리즈 MPS)
- 한국어 `choice`(주제 분류)는 잘 맞음 — 결제/일정/광고 3/3 정답, 건당 ~220ms(첫 호출 ~1.5s).
- 한국어 `score`·`noul`·예/아니오형 choice는 zero-shot에서 **신뢰 불가**(광고에 "답장 필요 0.95"). 판단형 질문은 파인튜닝 전까지 쓰지 않거나 사람 검토로 넘긴다.
- 옵시디언 받은 메모 8개 폴더 분류(2026-09-29)는 실패: 제목 검증 40%, 1,110개 중 980개 저신뢰. 선택지 4개 이상인 실제 노트 분류는 Claude로 하고, 그 라벨(`~/Desktop/cysjavis/jev-laya/train_obsidian_inbox.jsonl`)로 파인튜닝한 뒤 다시 시험한다.
- 파인튜닝 참고(코드팩토리 영상, 재현 안 함, 합성 CS 6분류): M4 Pro 24GB에서 1천 건 48분에 32.8%→86.4%, 같은 시험 Jev 100%. 비교 기준은 옵시디언 1,110건 Jev 71.4%.
- `low_confidence` 플래그가 뜨면 Claude가 직접 판단한다.
- 텍스트를 생성하지 않는다. 결과는 확률뿐이다.

매뉴얼: `~/Desktop/cysjavis/jev-laya/jev-laya-manual.html`
