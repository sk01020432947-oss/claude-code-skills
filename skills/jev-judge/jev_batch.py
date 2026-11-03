#!/usr/bin/env python3
"""Jev(TypeSafe) 일괄 판정 + 신뢰도 게이트.

  dry-run(기본, 호출 0회): 건수·추정 토큰·추정 비용만 출력
  실행:                    --yes 를 붙이면 cys feed 로 오너 승인을 묻고, 승인(종료코드 0)일 때만 실제 호출
  자체검증:                --selftest

입력 items.jsonl 한 줄 = {"id": "...", "state": "텍스트 또는 객체"}
질문 questions.json = {"이름": {"type": "choice|score|noul", "instructions": "...", "criteria": ...}, ...}
출력 out.jsonl 한 줄 = {"id", "answers", "needs_review", "error"}
"""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

VENV_PY = os.path.expanduser("~/.cys/local/venv-typesafe/bin/python")
KEY_FILE = os.path.expanduser("~/.config/typesafe/.env")
USD_PER_MTOK = 0.042  # 입력만 과금, 출력 무료(공식 models 문서, 2026-10-02 확인)


def est_tokens(state, questions):
    # ponytail: 문자수 기반 보수 추정(한글은 1자≈1토큰), 실제값은 응답 usage로 확인
    return len(json.dumps({"s": state, "q": questions}, ensure_ascii=False))


def needs_review(answers, gate):
    for a in answers.values():
        if a.get("type") == "noul":
            if 1 - gate < a["noul"] < gate:
                return True
        elif a.get("confidence", 0) < gate:
            return True
    return False


def owner_approved(body):
    """오너 feed 승인 — 종료코드 0(allow)만 True. 2=deny·3=timeout·cys 없음·그 밖 전부 False(fail-closed).
    에이전트가 스스로 붙이는 플래그로는 승인을 대신하지 못한다(오너 결정 2026-10-16 종량제 추가 지출 금지)."""
    try:
        rc = subprocess.run(["cys", "feed", "push", "--wait", "--title", "클라우드 jev 호출 승인 요청",
                             "--body", body]).returncode
    except Exception as e:  # cys 미설치·실행 불가도 '승인 없음'
        print("feed 실행 실패(%s) — 호출하지 않음" % type(e).__name__)
        return False
    if rc != 0:
        print("오너 승인 없음(feed rc=%d) — 클라우드 jev 호출하지 않음" % rc)
    return rc == 0


def load_key():
    for line in open(KEY_FILE, encoding="utf-8"):
        k, _, v = line.strip().partition("=")
        if k == "TYPESAFE_API_KEY":
            os.environ["TYPESAFE_API_KEY"] = v.strip().strip("'\"")
    os.environ.pop("TYPESAFE_LOG_LEVEL", None)  # 디버그 로그는 state 원문을 남긴다


def run(items, questions, gate, workers):
    from typesafe_sdk import TypeSafeClient
    load_key()
    with TypeSafeClient() as client:
        def one(it):
            try:
                r = client.system_one(it["state"], questions)
                ans = {k: v.model_dump(mode="json") for k, v in r.answers.items()}
                return dict(id=it.get("id"), answers=ans, needs_review=needs_review(ans, gate),
                            tokens=r.usage.input_tokens, error=None)
            except Exception as e:  # 실패도 결과로 남겨 사람 검토로 보낸다
                return dict(id=it.get("id"), answers=None, needs_review=True, tokens=0,
                            error="%s: %s" % (type(e).__name__, str(e)[:200]))
        with ThreadPoolExecutor(workers) as ex:
            return list(ex.map(one, items))


def selftest():
    assert needs_review({"a": {"type": "choice", "confidence": 0.5}}, 0.8)
    assert not needs_review({"a": {"type": "choice", "confidence": 0.9}}, 0.8)
    assert needs_review({"a": {"type": "noul", "noul": 0.6}}, 0.8)
    assert not needs_review({"a": {"type": "noul", "noul": 0.05}}, 0.8)
    assert est_tokens("가나", {}) > 0
    import tempfile
    path = os.environ.get("PATH", "")
    with tempfile.TemporaryDirectory() as d:
        fake = os.path.join(d, "cys")
        try:
            for rc, ok in ((0, True), (2, False), (3, False), (1, False)):
                open(fake, "w").write("#!/bin/sh\nexit %d\n" % rc); os.chmod(fake, 0o755)
                os.environ["PATH"] = d
                assert owner_approved("t") is ok, "feed rc=%d" % rc
            os.remove(fake)
            assert owner_approved("t") is False, "cys 없음은 거부여야 한다"
        finally:
            os.environ["PATH"] = path
    print("selftest ok")


def main():
    if os.path.exists(VENV_PY) and sys.prefix != os.path.dirname(os.path.dirname(VENV_PY)):
        os.execv(VENV_PY, [VENV_PY, __file__] + sys.argv[1:])
    p = argparse.ArgumentParser()
    p.add_argument("--items", help="items.jsonl")
    p.add_argument("--text", help="단건 판정용 텍스트")
    p.add_argument("--questions", help="questions.json 경로 또는 JSON 문자열")
    p.add_argument("--gate", type=float, default=0.8, help="이 신뢰도 미만은 needs_review")
    p.add_argument("--out", default="jev_out.jsonl")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--yes", action="store_true", help="실제 호출(없으면 dry-run)")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    q = a.questions
    questions = json.load(open(q, encoding="utf-8")) if os.path.exists(q) else json.loads(q)
    if a.text:
        items = [{"id": "1", "state": a.text}]
    else:
        items = [json.loads(l) for l in open(a.items, encoding="utf-8") if l.strip()]
    tok = sum(est_tokens(it["state"], questions) for it in items)
    print("건수 %d · 추정 입력 %d토큰 · 추정 비용 $%.5f (≈%.1f원)" % (len(items), tok, tok * USD_PER_MTOK / 1e6, tok * USD_PER_MTOK / 1e6 * 1400))
    if not a.yes:
        print("dry-run — 실제 호출하려면 --yes")
        return
    src = a.items or "단건 --text"
    if not owner_approved("입력 %s · 건수 %d · 추정 입력 %d토큰 · 추정 $%.5f (종량 과금 · 클라우드 TypeSafe)"
                          % (src, len(items), tok, tok * USD_PER_MTOK / 1e6)):
        return 2
    res = run(items, questions, a.gate, a.workers)
    with open(a.out, "w", encoding="utf-8") as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    used = sum(r["tokens"] for r in res)
    rev = sum(r["needs_review"] for r in res)
    err = sum(bool(r["error"]) for r in res)
    print("완료 → %s · 자동 %d · 사람검토 %d · 오류 %d · 실제 %d토큰 $%.5f" % (a.out, len(res) - rev, rev, err, used, used * USD_PER_MTOK / 1e6))
    if a.text:
        print(json.dumps(res[0], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
