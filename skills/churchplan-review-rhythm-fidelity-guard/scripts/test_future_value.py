import sys,os,io,contextlib
S=os.path.expanduser('~/.claude/skills')
sys.path[:0]=[S+'/churchplan-review-rhythm-fidelity-guard/scripts',S+'/churchplan-review-rhythm-rhythm-renderer/scripts']
import validate_review as V, build_review as B
def r(status,reviewed_at=None,confirmed=True):
    ind={"ref":"양육 · 정착률","baseline":"절반","target":"2/3","by":"2Q","signal_only":True,"verify_at_review":False,"status":status}
    if reviewed_at: ind["reviewed_at"]=reviewed_at
    return {"meta":{"chosen_theme":"한 식탁","status":"확정" if confirmed else "제안"},
            "inputs_echo":{"indicators_from_goals":[{"ref":"양육 · 정착률"}],"sustainability_from_resource":{}},
            "scorecard":{"quarters":[{"quarter":"2Q","indicators":[ind]}]},
            "schedule":{"midyear_revision":{"official":True,"when":"7월 첫 주"}},
            "confirmed":{"by":"목사 확정(HITL)"} if confirmed else None}
def fv(x):
    with contextlib.redirect_stdout(io.StringIO()):
        e,w=V.validate(x)
    g=B.gate(x)
    return any('미래값' in s for s in e), any('미래값' in s for s in g)
cases=[("확정 후 지어낸 🟢",r("🟢"),True),("확정 전 🟢",r("🟢",confirmed=False),True),
       ("미래 점검일",r("🟢","2099-01-01"),True),("실제 점검 후",r("🟢","2026-07-05"),False),("빈 status",r(None),False)]
ok=True
for name,x,expect in cases:
    v,g=fv(x); good=(v==expect and g==expect); ok&=good
    print(f"{'PASS' if good else 'FAIL'} {name}: validator={v} renderer={g} expect={expect}")
sys.exit(0 if ok else 1)
