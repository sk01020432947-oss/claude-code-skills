#!/usr/bin/env python3
"""최종보고 린트: 에이전트가 사용자에게 보내는 마지막 메시지를 Mythos 5.1 'Writing for the user' 규칙으로 점검한다."""
import re, sys

ASK = re.compile(r"(할까요|드릴까요|볼까요|원하시면|필요하시면|말씀해\s?주세요|알려\s?주세요|어떠신가요)")
PROMISE = re.compile(r"(하겠습니다|할게요|드리겠습니다|예정입니다|진행하겠|해\s?두겠)")
PREAMBLE = re.compile(r"^(네[,.!]|좋습니다|알겠습니다|물론입니다|훌륭한 질문)|살펴보겠습니다")
HEDGE = re.compile(r"(솔직히|진심으로|정말로 말씀드리면|간단히 말해|사실상 그냥)")
DASH = re.compile(r"(—|–|→|⇒|->)")
PAREN = re.compile(r"\([^)]{6,}\)")
LONG = 90  # ponytail: 글자 수 근사, 한국어 약 20어절 ≈ 60~90자


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def lint(text):
    t = strip_code(text).strip()
    out = []
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip()]
    if not paras:
        return out
    if PREAMBLE.search(paras[0].splitlines()[0]):
        out.append(("서두", "첫 줄이 인사·예고다. 결론부터 쓴다."))
    last = paras[-1]
    if ASK.search(last):
        out.append(("끝질문", "마지막 문단이 질문·제안이다. 할 수 있는 일이면 지금 하고, 아니면 지운다."))
    if PROMISE.search(last):
        out.append(("미완약속", "마지막 문단이 하지 않은 일의 약속이다. 지금 실행하거나 '못 한 것'으로 적는다."))
    headers = [l for l in t.splitlines() if l.lstrip().startswith("#")]
    if headers and len(t) < 1200:
        out.append(("머리글", f"짧은 글(약 500단어 미만)에 머리글 {len(headers)}개. 빼고 문단으로 쓴다."))
    elif len(headers) > 3:
        out.append(("머리글", f"머리글 {len(headers)}개. 셋 이하로 줄인다."))
    for i, line in enumerate(t.splitlines(), 1):
        if line.lstrip().startswith(("|", "#")):
            continue
        if DASH.search(line):
            out.append((f"줄표 L{i}", "줄표·화살표 대신 문장을 나눈다."))
        if PAREN.search(line):
            out.append((f"괄호 L{i}", "긴 괄호 주석은 별도 문장으로 뺀다."))
        if HEDGE.search(line):
            out.append((f"수식어 L{i}", "'솔직히·진심으로' 류는 지운다."))
        for s in re.split(r"(?<=[.!?다요])\s+", line):
            if len(s) > LONG:
                out.append((f"긴문장 L{i}", f"{len(s)}자. 두 문장으로 나눈다."))
                break
    return out


def selftest():
    bad = "네, 살펴보겠습니다.\n\n## 결과\n작업은 끝났다 — 다만 남은 것이 있다.\n\n원하시면 PR도 만들어 드릴까요?"
    good = "린트 스크립트를 설치했다. 셀프테스트는 통과했다.\n\n남은 일은 없다."
    kinds = {k.split()[0] for k, _ in lint(bad)}
    assert {"서두", "끝질문", "머리글", "줄표"} <= kinds, kinds
    assert lint(good) == [], lint(good)
    assert lint("```\n원하시면 할까요?\n```") == []
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    res = lint(src)
    for k, m in res:
        print(f"[{k}] {m}")
    print(f"{len(res)}건" if res else "통과")
    sys.exit(1 if res else 0)
