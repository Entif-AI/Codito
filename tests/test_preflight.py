import dataclasses
import json
import unittest

from codito.preflight import (Source, fixtures, hydrate, project, project_response, response_envelope,
                             run_study, value_of_information)


class PreflightTests(unittest.TestCase):
    def test_exact_json_path_retains_original_bytes_and_escaped_pointer(self):
        source = Source(b'{"noise": [1,2], "a/b": {"~key": "caf\\u00e9"}}', "json")
        packet = project(source, "paths", paths=("/a~1b/~0key",))
        self.assertEqual(hydrate(source, packet.excerpts[0]), b'"caf\\u00e9"')
        self.assertEqual(packet.excerpts[0].path, "/a~1b/~0key")
        self.assertEqual(packet.state, "bounded")

    def test_unicode_offsets_are_utf8_bytes(self):
        source = Source('{"前":0,"target":"é"}'.encode(), "json")
        packet = project(source, "paths", paths=("/target",))
        self.assertEqual(hydrate(source, packet.excerpts[0]), '"é"'.encode())

    def test_malformed_source_stays_opaque_but_sparse_excerpts_survive(self):
        source = Source(b'{"noise": [1,2,\n"critical": "keep original"', "json")
        packet = project(source, "layered", hints=("critical",))
        self.assertFalse(packet.syntax_valid)
        self.assertEqual(packet.state, "inspect_more")
        self.assertTrue(packet.excerpts)
        self.assertEqual(hydrate(source, packet.excerpts[0]), b'"critical": "keep original"')
        self.assertFalse(packet.repaired)

    def test_duplicate_keys_and_nonfinite_json_are_not_silently_interpreted(self):
        for raw in (b'{"target":1,"target":2}', b'{"target":NaN}'):
            packet = project(Source(raw, "json"), "paths", paths=("/target",))
            self.assertFalse(packet.syntax_valid)
            self.assertEqual(packet.state, "inspect_more")

    def test_missing_paths_abstain_and_allow_full_source_hydration(self):
        source = Source(b'{"other": 1}', "json")
        packet = project(source, "paths", paths=("/missing",))
        self.assertEqual(packet.state, "inspect_more")
        self.assertFalse(packet.excerpts)
        self.assertEqual(project(source, "raw").excerpts[0].start, 0)

    def test_source_drift_and_forged_ranges_fail(self):
        source = Source(b'{"target": 1}', "json")
        excerpt = project(source, "paths", paths=("/target",)).excerpts[0]
        with self.assertRaises(ValueError):
            hydrate(Source(b'{"target": 2}', "json"), excerpt)
        for start, end in ((-1, 3), (2, 1), (0, 100)):
            with self.assertRaises(ValueError):
                hydrate(source, dataclasses.replace(excerpt, start=start, end=end))

    def test_code_selection_uses_ast_locality_not_rewritten_source(self):
        source = Source(b'def noise():\n    return 1\n\ndef target():\n    return 42\n', "code")
        packet = project(source, "paths", symbols=("target",))
        selected = hydrate(source, packet.excerpts[0])
        self.assertIn(b'return 42', selected)
        self.assertNotIn(b'def noise', selected)

    def test_function_excerpt_includes_decorator_preconditions(self):
        source = Source(b'@requires_review\ndef target():\n    return 42\n', "code")
        packet = project(source, "paths", symbols=("target",))
        self.assertIn(b'@requires_review', hydrate(source, packet.excerpts[0]))

    def test_sparse_log_selection_keeps_source_order(self):
        source = Source(b'00 ok\n01 ERROR first\n02 ok\n03 WARN later\n', "log")
        packet = project(source, "heuristic", hints=("ERROR", "WARN"))
        self.assertEqual([hydrate(source, x) for x in packet.excerpts], [b'01 ERROR first\n', b'03 WARN later\n'])

    def test_semantic_scorer_can_abstain_and_cannot_forge_excerpt_identity(self):
        source = Source(b'{"target":1}', "json")
        self.assertEqual(project(source, "layered", paths=("/target",), scorer=lambda _: None).state, "abstain")
        with self.assertRaises(ValueError):
            project(source, "layered", paths=("/target",), scorer=lambda _: ["forged"])

    def test_voi_is_explicit_and_can_reject_more_context(self):
        self.assertTrue(value_of_information(.8, 10, 2)["load_more"])
        self.assertFalse(value_of_information(.1, 10, 2)["load_more"])
        for probability in (-1, 2, float("nan")):
            with self.assertRaises(ValueError):
                value_of_information(probability, 10, 2)

    def test_all_six_families_and_two_boundaries_have_controls_and_metrics(self):
        report = run_study()
        self.assertTrue({"json", "malformed", "code", "browser", "axi", "log"}.issubset({r["fixture"] for r in report["runs"]}))
        self.assertGreaterEqual(len({r["boundary"] for r in report["runs"]}), 2)
        for run in report["runs"]:
            self.assertGreaterEqual(run["preflight_ns"], 0)
            self.assertIn("relevant_evidence_recall", run)
            self.assertIn("false_exclusion_count", run)
            self.assertIsNone(run["tokens"])
        self.assertTrue(any(r["disposition"] == "net-negative" for r in report["runs"]))

    def test_ground_truth_labels_do_not_enter_projection(self):
        case = fixtures()[0]
        self.assertNotIn("required_spans", dataclasses.asdict(project(case["source"], "raw")))

    def test_tool_envelope_retains_transport_and_payload_provenance_and_rejects_drift(self):
        source = Source(b'{"target":1}', "json")
        envelope = response_envelope(source)
        packet = project_response(envelope, "paths", paths=("/target",))
        self.assertEqual(packet.source_digest, source.digest)
        self.assertIsNotNone(packet.transport_digest)
        self.assertEqual(hydrate(source, packet.excerpts[0]), b'1')
        bad = json.loads(envelope)
        bad["payload_base64"] = "e30="
        with self.assertRaises(ValueError):
            project_response(json.dumps(bad).encode(), "paths", paths=("/target",))


if __name__ == "__main__":
    unittest.main()
