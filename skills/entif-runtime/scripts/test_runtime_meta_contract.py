#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).parents[1]
skill=(root/'SKILL.md').read_text()
inv=(root/'references/MIGRATION_INVENTORY.md').read_text()
required=[
    ('SKILL.md','references/PR_CLOSEOUT.md',skill),
    ('SKILL.md','references/WORK_ORCHESTRATION.md',skill),
    ('SKILL.md','references/FEATURE_POSTMORTEM.md',skill),
    ('SKILL.md','references/HANDOFF_RECOVERY.md',skill),
    ('SKILL.md','references/SURFACE_CAPABILITIES.md',skill),
    ('SKILL.md','references/FAILURE_INTELLIGENCE.md',skill),
    ('SKILL.md','Chat and Codex are common profiles, not the ontology',skill),
    ('MIGRATION_INVENTORY.md','`entif-pr-closeout` | `MOVE_TO_MODULE`',inv),
    ('MIGRATION_INVENTORY.md','`entif-postmortem-logger` | `MOVE_TO_MODULE`',inv),
    ('MIGRATION_INVENTORY.md','`entif-governed-creator` | `KEEP_TOP_LEVEL_EXCEPTION`',inv),
]
missing=[f'{f}: {needle}' for f,needle,text in required if needle not in text]
if missing:
    raise SystemExit('runtime meta contract regression:\n- '+'\n- '.join(missing))
for ref in ['references/SURFACE_CAPABILITIES.md','references/FAILURE_INTELLIGENCE.md']:
    if not (root/ref).exists():
        raise SystemExit(f'runtime meta contract regression: missing {ref}')
print('runtime meta contract: PASS')
