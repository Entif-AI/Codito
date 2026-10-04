import copy
import json
import unittest
from pathlib import Path

from codito.namespace_registry import census, extract_key, preflight, validate_registry


def record(slug="ABC", scope="repository", owner="Entif-AI/one", **extra):
    return dict(slug=slug, scope=scope, owner=owner, status="historical",
                meaning="Unreviewed public historical use", aliases=[],
                source_refs=["https://github.com/Entif-AI/one/issues/1"],
                publication_posture="public", allocation="unreviewed", **extra)


def registry(*records):
    return {"format_version": 1, "authority": "candidate", "records": list(records)}


class NamespaceTests(unittest.TestCase):
    def test_extracts_compound_and_bracketed_keys_without_prose_guessing(self):
        self.assertEqual(extract_key("[MAC-AX-001] Capture helper"), ("MAC-AX", "001"))
        self.assertEqual(extract_key("ENTIF-v0-012: Research"), ("ENTIF-v0", "012"))
        self.assertIsNone(extract_key("Research methods for 100 projects"))

    def test_census_tracks_historical_key_reuse_and_no_titles(self):
        rows = [{"repo": "Entif-AI/one", "status": "complete", "issues": [
            {"number": 1, "title": "ABC-001: First", "url": "u1", "state": "open"},
            {"number": 2, "title": "abc-001: Different", "url": "u2", "state": "closed"}]}]
        result = census(rows)
        self.assertEqual(len(result["key_reuse"]), 1)
        self.assertNotIn("title", json.dumps(result))
        self.assertEqual(result["issue_count"], 2)

    def test_exact_and_case_normalized_collisions(self):
        r = registry(record())
        self.assertEqual(preflight(r, "ABC", "Entif-AI/one")["conflicts"][0]["match"], "exact")
        self.assertEqual(preflight(r, "abc", "Entif-AI/one")["conflicts"][0]["match"], "case-normalized")

    def test_repository_scope_does_not_allocate_global_namespace(self):
        self.assertFalse(preflight(registry(record()), "ABC", "Entif-AI/two")["conflicts"])
        self.assertTrue(preflight(registry(record()), "ABC", "Entif-AI/two", "organization")["conflicts"])

    def test_organization_reservation_and_aliases_conflict_everywhere(self):
        r = record(scope="organization")
        r["aliases"] = ["OLD"]
        self.assertTrue(preflight(registry(r), "old", "Entif-AI/two")["conflicts"])

    def test_deprecated_historical_and_withheld_names_still_block_reuse(self):
        for status in ("active", "reserved", "deprecated", "historical", "alias", "protected-withheld"):
            r = record()
            r["status"] = status
            if status == "alias":
                r["alias_of"] = "NEW"
                rows = [r, record("NEW")]
            else:
                rows = [r]
            if status == "protected-withheld":
                r.update(owner=None, meaning=None, publication_posture="withheld")
            self.assertTrue(preflight(registry(*rows), "ABC", "Entif-AI/one")["conflicts"])

    def test_unresolved_home_never_grants_allocation(self):
        result = preflight(registry(), "NEW", "Entif-AI/one")
        self.assertEqual(result["disposition"], "needs-owner-decision")
        self.assertFalse(result["allocation_authorized"])

    def test_invalid_slug_status_owner_and_duplicate_records_fail(self):
        for field, value in (("slug", "A B"), ("status", "invented"), ("owner", None)):
            r = record()
            r[field] = value
            with self.assertRaises(ValueError):
                validate_registry(registry(r))
        with self.assertRaises(ValueError):
            validate_registry(registry(record(), record()))
        with self.assertRaises(ValueError):
            preflight(registry(), "BAD/KEY", "Entif-AI/one")

    def test_alias_cycles_and_missing_targets_fail(self):
        a, b = record("A"), record("B")
        a.update(status="alias", alias_of="B")
        b.update(status="alias", alias_of="A")
        for rows in ([a], [a, b]):
            with self.assertRaises(ValueError):
                validate_registry(registry(*rows))

    def test_registry_does_not_mutate_inputs(self):
        r = registry(record())
        before = copy.deepcopy(r)
        preflight(r, "ABC", "Entif-AI/one")
        self.assertEqual(r, before)

    def test_checked_in_candidate_registry_and_provisional_dispositions(self):
        p = Path(__file__).resolve().parents[1] / "research/issue-namespaces/candidate-registry.json"
        r = json.loads(p.read_text())
        validate_registry(r)
        self.assertEqual(r["authority"], "candidate")
        for slug in ("ADI", "MCA"):
            rows = [x for x in r["records"] if x["slug"] == slug]
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["allocation"], "provisional")
            self.assertEqual(rows[0]["status"], "reserved")


if __name__ == "__main__":
    unittest.main()
