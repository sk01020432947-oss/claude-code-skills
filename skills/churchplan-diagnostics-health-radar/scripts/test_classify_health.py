import sys,os
sys.path.insert(0,os.path.expanduser('~/.claude/skills/churchplan-diagnostics-health-radar/scripts'))
from classify_health import classify_health as C
h={"예배":{"score":4,"trend":"↑"},"전도":{"score":2,"trend":"↓"},"양육":{"score":2,"trend":"↑"},"교제":{"score":4,"trend":"↓"},
   "봉사":{"score":3,"trend":"↑"},"선교":{"score":3,"trend":"↓"},"재정":{"score":3,"trend":"→"},"말씀":{"score":None}}
r=C(h); both=set(r["strong"])&set(r["needs_care"])
exp_s={"예배","교제","봉사"}; exp_c={"전도","양육","선교"}
ok=not both and set(r["strong"])==exp_s and set(r["needs_care"])==exp_c
print("PASS" if ok else "FAIL", "strong=",r["strong"],"care=",r["needs_care"],"both=",both); sys.exit(0 if ok else 1)
