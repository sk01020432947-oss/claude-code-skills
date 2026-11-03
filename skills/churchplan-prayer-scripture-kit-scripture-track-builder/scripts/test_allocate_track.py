import sys,os,re
S=os.path.expanduser('~/.claude/skills')
sys.path[:0]=[S+'/churchplan-prayer-scripture-kit-scripture-track-builder/scripts',S+'/churchplan-prayer-scripture-kit-fidelity-guard/scripts']
import allocate_track as A, validate_kit as K, bible_validator as bv
def verses(sched):
    out=[]
    for d in sched:
        for p in d["portions"]:
            m=re.match(r"^(\S+) (\d+)(?::(\d+)(?:-(\d+))?|-(\d+))?$",p); b,c=m.group(1),int(m.group(2))
            if m.group(3): out+= [(b,c,v) for v in range(int(m.group(3)),int(m.group(4) or m.group(3))+1)]
            else:
                e=int(m.group(5) or c)
                for cc in range(c,e+1): out+=[(b,cc,v) for v in range(1,bv.BOOK_CHAPTERS[b][cc-1]+1)]
    return out
ok=True
for track,days,books in [("신약 1년",None,A.NT_BOOKS),("시편잠언",365,["시편","잠언"]),("1년 통독",None,A.ALL_BOOKS),("시편잠언",None,["시편","잠언"]),("신약 1년",100,A.NT_BOOKS)]:
    s=A.allocate_track(track,days); want=days or A.TRACKS[track][1]
    full=[(b,c,v) for b in books for c,n in enumerate(bv.BOOK_CHAPTERS[b],1) for v in range(1,n+1)]
    bad=[p for d in s for p in d["portions"] if not K.check_scripture(p)[0]]
    good=len(s)==want and verses(s)==full and not bad and all(d["portions"] for d in s)
    ok&=good; print(f"{'PASS' if good else 'FAIL'} {track} {days}: days={len(s)}/{want} cover={verses(s)==full} invalid={bad[:2]} last={s[-1]}")
sys.exit(0 if ok else 1)
