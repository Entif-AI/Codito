#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("work_stack.py")


def run(*args, ok=True):
    cp = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
    if ok and cp.returncode != 0:
        raise AssertionError(f"command failed: {cp.args}\nstdout={cp.stdout}\nstderr={cp.stderr}")
    if not ok and cp.returncode == 0:
        raise AssertionError(f"command unexpectedly passed: {cp.args}\nstdout={cp.stdout}")
    return cp


class WorkStackTest(unittest.TestCase):
    def test_dependency_hash_and_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            init = run("init", "--root", str(root), "--title", "test", "--work-id", "W1")
            work = Path(init.stdout.strip())
            inp = root / "input.txt"; inp.write_text("alpha")
            out = root / "out.txt"
            run("add-task", "--work", str(work), "--task-id", "T001", "--title", "derive", "--input-file", str(inp), "--output-file", str(out))
            run("add-task", "--work", str(work), "--task-id", "T002", "--title", "persist", "--depends-on", "T001", "--side-effect-class", "reconcile_before_retry", "--idempotency-key", "remote:W1:T002")
            status = json.loads(run("status", "--work", str(work)).stdout)
            self.assertEqual(status["ready"], ["T001"])
            run("start", "--work", str(work), "--task", "T002", ok=False)
            run("start", "--work", str(work), "--task", "T001")
            out.write_text("derived")
            run("verify", "--work", str(work), "--task", "T001")
            run("commit", "--work", str(work), "--task", "T001")
            status = json.loads(run("status", "--work", str(work)).stdout)
            self.assertIn("T002", status["ready"])
            run("start", "--work", str(work), "--task", "T002")
            run("fail", "--work", str(work), "--task", "T002", "--reason", "ack unknown", "--ambiguous")
            t2 = json.loads((work / "tasks" / "T002.json").read_text())
            self.assertEqual(t2["state"], "safe_hold")
            run("start", "--work", str(work), "--task", "T002", ok=False)
            run("reconcile", "--work", str(work), "--task", "T002", "--outcome", "retryable", "--note", "target absent")
            run("start", "--work", str(work), "--task", "T002")
            run("receipt", "--work", str(work), "--task", "T002", "--receipt-ref", "drive:file:123")
            run("verify", "--work", str(work), "--task", "T002")
            run("commit", "--work", str(work), "--task", "T002")
            run("validate", "--work", str(work))
            inp.write_text("beta")
            stale = run("validate", "--work", str(work), ok=False)
            self.assertIn("stale committed input", stale.stdout)

    def test_nested_and_event_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            work = Path(run("init", "--root", str(root), "--title", "parent", "--work-id", "P").stdout.strip())
            child = Path(run("spawn-child", "--work", str(work), "--title", "child", "--work-id", "C").stdout.strip())
            cw = json.loads((child / "WORK.json").read_text())
            self.assertEqual(cw["parent_work_id"], "P")
            ep = work / "EVENTS.jsonl"
            lines = ep.read_text().splitlines()
            obj = json.loads(lines[-1]); obj["data"]["path"] = "tampered"; lines[-1] = json.dumps(obj)
            ep.write_text("\n".join(lines) + "\n")
            bad = run("validate", "--work", str(work), ok=False)
            self.assertIn("event digest mismatch", bad.stdout)


if __name__ == "__main__":
    unittest.main()
