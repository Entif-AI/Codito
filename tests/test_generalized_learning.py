import dataclasses
import json
import unittest

from codito.generalized_learning import (Recipient, correct, export_candidate, fixtures, run_study)


class GeneralizedLearningTests(unittest.TestCase):
    def setUp(self):
        self.case = fixtures()[0]

    def test_export_contains_only_generalized_scope_provenance_and_no_raw_history(self):
        result = export_candidate(self.case["episodes"], self.case["profile"])
        self.assertEqual(result["state"], "exported")
        encoded = json.dumps(dataclasses.asdict(result["lesson"]))
        for episode in self.case["episodes"]:
            self.assertNotIn(episode.raw.decode(), encoded)
            self.assertNotIn(episode.local_id, encoded)
        self.assertNotIn("raw", encoded)
        self.assertEqual(result["independent_roots"], 2)

    def test_rights_consent_sensitivity_third_party_and_purpose_can_block_export(self):
        for field, value in (("consent", False), ("rights", False), ("sensitive", True),
                             ("third_party", True), ("purpose", "unapproved-purpose")):
            episodes = tuple(dataclasses.replace(e, **{field: value}) for e in self.case["episodes"])
            result = export_candidate(episodes, self.case["profile"])
            self.assertIsNone(result["lesson"])
            self.assertEqual(result["state"], "no-export")

    def test_correlated_copies_are_not_independent_support(self):
        first, second = self.case["episodes"]
        copies = (first, dataclasses.replace(second, evidence_root=first.evidence_root))
        result = export_candidate(copies, self.case["profile"])
        self.assertEqual(result["independent_roots"], 1)
        self.assertIsNone(result["lesson"])

    def test_conflicting_validated_lessons_preserve_dissent_without_majority_truth(self):
        a, b = self.case["episodes"]
        result = export_candidate((a, dataclasses.replace(b, rule_ref="verify-tool-postcondition")), self.case["profile"])
        self.assertEqual(result["state"], "conflicting-evidence")
        self.assertTrue(result["dissent"])
        self.assertIsNone(result["lesson"])

    def test_poisoned_unvalidated_contributor_is_excluded_not_promoted(self):
        a, b = self.case["episodes"]
        result = export_candidate((a, dataclasses.replace(b, locally_validated=False)), self.case["profile"])
        self.assertIsNone(result["lesson"])
        self.assertEqual(result["independent_roots"], 1)

    def test_recipient_revalidates_scope_version_and_local_result(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        recipient = Recipient(**self.case["recipient"])
        self.assertEqual(recipient.adopt(lesson)["state"], "accepted-local")
        for change in ({"version": "different"}, {"scope": "different"}, {"purpose": "different"}):
            args = dict(self.case["recipient"], **change)
            self.assertTrue(Recipient(**args).adopt(lesson)["state"].startswith("rejected"))
        args = dict(self.case["recipient"], validation={lesson.rule_ref: False})
        self.assertEqual(Recipient(**args).adopt(lesson)["state"], "rejected-local-test")

    def test_missing_and_conflicting_local_evidence_are_distinct(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        for response, expected in ((None, "insufficient-evidence"), ("conflict", "conflicting-evidence")):
            args = dict(self.case["recipient"], validation={lesson.rule_ref: response})
            self.assertEqual(Recipient(**args).adopt(lesson)["state"], expected)

    def test_correction_preserves_old_record_and_invalidates_admitted_derivative(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        recipient = Recipient(**self.case["recipient"])
        recipient.adopt(lesson)
        correction = correct(lesson, "challenge:counterexample")
        self.assertEqual(lesson.status, "active")
        self.assertEqual(correction.status, "revoked")
        self.assertEqual(correction.previous, lesson.id)
        recipient.receive(correction)
        self.assertEqual(recipient.adopt(lesson)["state"], "rejected-superseded")
        self.assertNotIn(lesson.id, recipient.accepted)

    def test_correction_arriving_before_original_prevents_late_resurrection(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        recipient = Recipient(**self.case["recipient"])
        recipient.receive(correct(lesson, "challenge:erasure"))
        self.assertEqual(recipient.adopt(lesson)["state"], "rejected-superseded")

    def test_digest_drift_and_unapproved_rule_fail_closed(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        with self.assertRaises(ValueError):
            Recipient(**self.case["recipient"]).adopt(dataclasses.replace(lesson, version="forged"))
        episodes = tuple(dataclasses.replace(e, rule_ref="publish-raw-secret") for e in self.case["episodes"])
        self.assertIsNone(export_candidate(episodes, self.case["profile"])["lesson"])

    def test_no_acceptance_transfers_execution_authority(self):
        lesson = export_candidate(self.case["episodes"], self.case["profile"])["lesson"]
        self.assertFalse(Recipient(**self.case["recipient"]).adopt(lesson)["execution_authorized"])

    def test_four_families_and_six_controls_retain_harm_and_bytes(self):
        report = run_study()
        self.assertEqual(set(report["families"]), {"computer-use", "personal-assistance", "retail", "engineering"})
        self.assertEqual(len(report["runs"]), 24)
        self.assertTrue(any(r["utility_proxy"] > 0 and r["raw_marker_exposure_proxy"] == 0 for r in report["runs"]))
        self.assertTrue(any(r["export_state"] == "no-export" for r in report["runs"]))
        self.assertTrue(any(r["harm_proxy"] > 0 for r in report["runs"]))
        for run in report["runs"]:
            self.assertEqual(run["network_bytes"], 0)
            self.assertIn("serialized_export_bytes", run)
            self.assertIn("local_validation", run)

    def test_correct_terminal_result_does_not_repair_naive_privacy_judgment(self):
        runs = [r for r in run_study()["runs"] if r["strategy"] == "naive"]
        self.assertTrue(any(r["terminal_outcome"]["state"] == "correct" for r in runs))
        self.assertTrue(all(r["decision_integrity"] is False and r["joint_correctness"] is False for r in runs))

    def test_local_validation_and_later_terminal_failure_remain_separate(self):
        case = dict(self.case, expected_suggestion="deliberately-different-postcondition")
        run = next(r for r in run_study(cases=[case])["runs"] if r["strategy"] == "rights-safe")
        self.assertEqual(run["local_validation"]["state"], "accepted-local")
        self.assertEqual(run["terminal_outcome"]["state"], "wrong")
        self.assertFalse(run["joint_correctness"])


if __name__ == "__main__":
    unittest.main()
