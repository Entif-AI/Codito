#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text()
RECOVERY = (ROOT / "references" / "connector-recovery.md").read_text()
COMPOSITION = (ROOT / "references" / "composition.md").read_text()

required_recovery = [
    "CAPABILITY_NOT_EXPOSED",
    "PERMISSION_DENIED",
    "Do not merely repeat tool discovery against the current connector instance",
    "rebind, reinitialize, or restart the connector/session itself",
    "transient stream/tool interruption",
    "do not ask for another user prompt",
    "at least three full cycles",
    "reconcile the target before retrying",
]
required_skill = [
    "same-invocation connector recovery protocol",
    "Only an explicit provider denial counts as `PERMISSION_DENIED`",
    "do **not** require another user prompt",
]
required_composition = [
    "do not compress it to generic `refresh binding`/`rediscover` language",
    "restart/reinitialize/rebind the connector/session itself",
]

missing = []
for label, text, required in [
    ("connector-recovery.md", RECOVERY, required_recovery),
    ("SKILL.md", SKILL, required_skill),
    ("composition.md", COMPOSITION, required_composition),
]:
    for item in required:
        if item not in text:
            missing.append(f"{label}: {item}")

if missing:
    raise SystemExit("Connector recovery contract regression:\n- " + "\n- ".join(missing))

print("connector recovery contract: PASS")
