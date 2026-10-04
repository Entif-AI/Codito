#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; errors=[]
required=["SKILL.md","PROJECT_GOVERNANCE.yaml","references/router/ROOT.md","references/router/rules.json","references/module-registry.json","references/MIGRATION_INVENTORY.md","references/ISSUE_SPEC_PLAN_FLOW.md","references/SPECOPS_ADAPTER.md","references/doctrine/agent-interface-axi.md","fixtures/routing-fixtures.json"]
for p in required:
    if not (ROOT/p).exists(): errors.append({"missing":p})
reg=json.loads((ROOT/"references/module-registry.json").read_text()) if (ROOT/"references/module-registry.json").exists() else {"modules":[]}; mods=reg.get("modules",[])
if len(mods)<35: errors.append({"module_count":len(mods),"min":35})
domains={m.get("domain") for m in mods}; expected={"intake","product","specification","architecture","work-shaping","planning","investigate","risk","review","implementation","delivery"}
if not expected.issubset(domains): errors.append({"missing_domains":sorted(expected-domains)})
for m in mods:
    p=ROOT/m["path"]; idx=ROOT/"references/modules"/m["domain"]/"INDEX.md"
    if not p.is_file(): errors.append({"missing_module_file":m["id"]})
    if not idx.is_file(): errors.append({"missing_domain_index":m["domain"]})
    if p.is_file():
        txt=p.read_text()
        for field in ["Preferred surface","Agent interface kind","AXI candidate","AXI disposition default","AXI scaffolder","Raw interface fallback","Handoff"]:
            if field not in txt: errors.append({"module":m["id"],"missing_field":field})
skill=(ROOT/"SKILL.md").read_text() if (ROOT/"SKILL.md").exists() else ""
if len(skill.splitlines())>180: errors.append({"skill_lines":len(skill.splitlines()),"max":180})
for needle in ["Chat-first / Codex-minimal routing","First-class Agent Interface Gate","references/router/ROOT.md","entif-axi"]:
    if needle not in skill: errors.append({"skill_missing":needle})
print(json.dumps({"ok":not errors,"errors":errors,"modules":len(mods),"domains":len(domains)},indent=2)); raise SystemExit(1 if errors else 0)
