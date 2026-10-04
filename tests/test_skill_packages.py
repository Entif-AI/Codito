import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_architecture_validator():
    subprocess.run([sys.executable,str(ROOT/"skills/entif-architecture/scripts/validate_architecture_skill.py")],check=True)
def test_architecture_routing_fixtures():
    subprocess.run([sys.executable,str(ROOT/"skills/entif-architecture/scripts/verify_routing_fixtures.py")],check=True)
def test_axi_skill_has_governance():
    root=ROOT/"skills/entif-axi"
    assert (root/"SKILL.md").is_file()
    text=(root/"SKILL.md").read_text()
    assert "SCAFFOLD_NEW_AXI" in text
    assert "CodyEngel/axi-axi" in text
    assert (root/"PROJECT_GOVERNANCE.yaml").is_file()
