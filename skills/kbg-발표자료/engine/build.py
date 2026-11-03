import sys,os
d=os.path.dirname(os.path.abspath(__file__))
base=open(f'{d}/base.css').read(); eng=open(f'{d}/engine.js').read()
for f in sys.argv[1:]:
    s=open(f).read().replace('/*BASE*/',base).replace('/*ENGINE*/',eng)
    out=f.replace('.html','.built.html'); open(out,'w').write(s); print(out)
