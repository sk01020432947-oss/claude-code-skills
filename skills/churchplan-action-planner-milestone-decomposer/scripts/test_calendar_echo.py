import sys,os,json,subprocess
S=os.path.expanduser('~/.claude/skills'); import tempfile; D=tempfile.mkdtemp()
BM=S+'/churchplan-action-planner-milestone-decomposer/scripts/build_milestones.py'
VA=S+'/churchplan-action-planner-fidelity-guard/scripts/validate_action.py'
goals={"meta":{"chosen_theme":"한 식탁","status":"확정"},"axes":[{"axis":"전도","goals":[{"direction_goal":"한 영혼 정착","indicators":[{"label":"정착률","target":"2/3","by":"3Q"}]}]}]}
cal={"meta":{"year":2027,"season_frame":{"1Q":"영성","2Q":"전도","3Q":"양육","4Q":"감사"},"status":"확정"},
     "weeks":[{"week":13,"events":[{"id":"E1","title":"환영 페스티벌","type":"핵심"}]},{"week":14,"events":[]}]}
json.dump(goals,open(D+'/goals.json','w'),ensure_ascii=False); json.dump(cal,open(D+'/calendar.json','w'),ensure_ascii=False)
def run(link):
    args=['python3','-I',BM,D+'/goals.json','전도',D+'/action.json']
    if '--calendar' in open(BM,encoding='utf-8').read(): args+=['--calendar',D+'/calendar.json']
    subprocess.run(args,check=True,capture_output=True)
    a=json.load(open(D+'/action.json')); a["actions"][0].update(linked_event=link,department="전도",purpose="정착 돕기")
    json.dump(a,open(D+'/action.json','w'),ensure_ascii=False)
    out=subprocess.run(['python3','-I',VA,D+'/action.json'],capture_output=True,text=True).stdout
    return '행사위장' in out, a["inputs_echo"].get("from_calendar")
ok=True
for link,expect in [("E1",False),("E99",True)]:
    hit,fc=run(link); good=hit==expect; ok&=good
    print(f"{'PASS' if good else 'FAIL'} linked_event={link}: 행사위장={hit} expect={expect} from_calendar={fc}")
sys.exit(0 if ok else 1)
