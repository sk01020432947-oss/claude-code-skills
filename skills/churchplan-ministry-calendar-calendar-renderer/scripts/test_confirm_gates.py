import sys,os,importlib.util as U
S=os.path.expanduser('~/.claude/skills')
R={'action-planner-action-renderer':'build_action','goal-architect-checklist-builder':'build_checklist','plan-compiler-compiler-renderer':'build_package',
   'plan-reinforce-reinforce-renderer':'build_reinforce','prayer-scripture-kit-kit-renderer':'build_kit','resource-aligner-aligner-renderer':'build_resource',
   'review-rhythm-rhythm-renderer':'build_review','sermon-planner-52-plan-renderer':'build_sermon_plan','signature-events-blueprint-renderer':'build_event_plan',
   'ministry-calendar-calendar-renderer':'build_calendar'}
TAG='--preview'
ok=True
for d,m in R.items():
    p=f'{S}/churchplan-{d}/scripts'; sys.path.insert(0,p)
    spec=U.spec_from_file_location(m,f'{p}/{m}.py'); mod=U.module_from_spec(spec); sys.modules[m]=mod; spec.loader.exec_module(mod)
    draft={"meta":{"chosen_theme":"한 식탁","status":"제안"},"confirmed":None}
    final={"meta":{"chosen_theme":"한 식탁","status":"확정"},"confirmed":{"by":"목사 확정(HITL)"}}
    try:
        blocked=any(TAG in e for e in mod.gate(draft)); prev=any(TAG in e for e in mod.gate(draft,preview=True)); fin=any(TAG in e for e in mod.gate(final))
    except TypeError as ex:
        blocked,prev,fin=False,None,None
    good=blocked and prev is False and fin is False; ok&=good
    print(f"{'PASS' if good else 'FAIL'} {d}: 미확정차단={blocked} preview허용={prev is False} 확정통과={fin is False}")
    sys.path.remove(p)
sys.exit(0 if ok else 1)
