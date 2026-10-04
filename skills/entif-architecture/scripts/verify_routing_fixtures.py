#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def hit(rule,t):
    starts=rule.get("starts_with_any",[]); anyv=rule.get("contains_any",[]); allv=rule.get("contains_all",[])
    if starts and not any(t.startswith(x) for x in starts) and not any(x in t for x in anyv): return False
    if anyv and not any(x in t for x in anyv) and not (starts and any(t.startswith(x) for x in starts)): return False
    if allv and not all(x in t for x in allv): return False
    return bool(starts or anyv or allv)
def route(text):
    t=text.lower(); modules=[]; shared=[]; doctrine=[]
    for r in json.loads((ROOT/"references/router/rules.json").read_text())["rules"]:
        if hit(r,t):
            modules += r.get("modules",[]); shared += r.get("shared",[]); doctrine += r.get("doctrine",[])
            if r.get("terminal"): break
    return list(dict.fromkeys(modules)),list(dict.fromkeys(shared)),list(dict.fromkeys(doctrine))
def main():
    fixtures=json.loads((ROOT/"fixtures/routing-fixtures.json").read_text()); registry=json.loads((ROOT/"references/module-registry.json").read_text()); known={x["id"] for x in registry["modules"]}; failures=[]
    for f in fixtures:
        got,shared,doc=route(f["prompt"]); gs=set(got); ss=set(shared); ds=set(doc); exp=set(f["expected_modules"]); forb=set(f["forbidden_modules"]); es=set(f.get("expected_shared",[])); ed=set(f.get("expected_doctrine",[]))
        if not exp.issubset(gs) or gs&forb or not es.issubset(ss) or not ed.issubset(ds): failures.append({"id":f["id"],"got":got,"missing":sorted(exp-gs),"forbidden_loaded":sorted(gs&forb),"shared_missing":sorted(es-ss),"doctrine_missing":sorted(ed-ds)})
    unknown=set()
    for f in fixtures: unknown |= set(f["expected_modules"])-known
    if unknown: failures.append({"unknown_modules":sorted(unknown)})
    for m in registry["modules"]:
        if not (ROOT/m["path"]).is_file() or not (ROOT/"references/modules"/m["domain"]/"INDEX.md").is_file(): failures.append({"missing_surface":m["id"]})
    if failures: print(json.dumps({"ok":False,"failures":failures},indent=2)); return 1
    print(json.dumps({"ok":True,"fixtures":len(fixtures),"modules":len(known),"depth":"parent -> domain INDEX -> leaf -> doctrine/shared"},indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
