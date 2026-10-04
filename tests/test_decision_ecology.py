import copy
import json
import math
import unittest
from pathlib import Path

from codito.decision_ecology import (evaluate, pareto, rank, run_study,
                                     sample_context, select, validate)

FIXTURE = Path(__file__).resolve().parents[1] / "research/decision-ecology/fixture.json"


class DecisionEcologyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text())

    def test_own_dossier_is_complete_and_peer_aperture_is_exact(self):
        for aperture in (0, .25, .5, 1):
            contexts = sample_context(self.fixture, aperture, 17)
            for project, facts in contexts.items():
                for peer in "ABCDE":
                    visible = [f for f in facts if f["project"] == peer]
                    self.assertEqual(len(visible), 4 if project == peer else int(4 * aperture))

    def test_seed_is_repeatable_and_changes_partial_evidence(self):
        self.assertEqual(sample_context(self.fixture, .25, 1), sample_context(self.fixture, .25, 1))
        self.assertNotEqual(sample_context(self.fixture, .25, 1), sample_context(self.fixture, .25, 2))

    def test_weights_are_explicit_finite_and_never_invented(self):
        for weights in (None, {"impact": float("nan")}, {"impact": -1}, {"impact": 0}):
            bad = copy.deepcopy(self.fixture)
            bad["profile"]["weights"] = weights
            with self.assertRaises(ValueError):
                validate(bad)

    def test_weighted_and_pareto_aggregators_have_distinct_behavior(self):
        vectors = {"a": {"x": 3, "y": 3}, "b": {"x": 2, "y": 2}, "c": {"x": 1, "y": 4}}
        self.assertEqual(rank(vectors, {"x": .5, "y": .5}), ["a", "c", "b"])
        self.assertEqual(pareto(vectors), {"a", "c"})

    def test_legal_budget_controller_preserves_dependencies_and_exclusions(self):
        options = self.fixture["candidates"]
        result = select(["local", "shared", "compete_a", "compete_b", "dup_a", "dup_b"], options, 6)
        self.assertLessEqual(sum(next(c["cost"] for c in options if c["id"] == x) for x in result), 6)
        self.assertLess(result.index("shared"), result.index("local"))
        self.assertFalse({"compete_a", "compete_b"}.issubset(result))
        self.assertFalse({"dup_a", "dup_b"}.issubset(result))

    def test_hidden_dependency_failure_remains_separate_from_rank(self):
        outcome = evaluate(["hidden"], self.fixture)
        self.assertEqual(outcome["attempts"][0]["state"], "failed-prerequisite")
        self.assertGreater(outcome["downstream_rework_proxy"], 0)
        self.assertEqual(outcome["quality"], 0)

    def test_truth_is_not_available_to_the_context_sampler(self):
        altered = copy.deepcopy(self.fixture)
        altered["truth"]["hidden"]["quality"] = -10000
        self.assertEqual(sample_context(altered, .25, 17), sample_context(self.fixture, .25, 17))

    def test_full_study_preserves_candidate_provenance_scores_and_outcome_join(self):
        report = run_study(self.fixture, seeds=(3, 11, 29))
        self.assertEqual(report["strong_model_comparator"]["status"], "not-run")
        for run in report["runs"]:
            self.assertEqual(run["candidate_grid_digest"], report["candidate_grid_digest"])
            self.assertEqual(run["outcome"]["decision_id"], run["decision_id"])
            self.assertLessEqual(run["outcome"]["spent"], self.fixture["budget"])
            self.assertGreaterEqual(run["regret_proxy"], -1e-9)
            self.assertIsNone(run["tokens"])
        panel = [r for r in report["runs"] if r["strategy"] == "panel"]
        self.assertEqual({r["aperture"] for r in panel}, {0, .25, .5, 1})
        self.assertEqual({r["aggregator"] for r in panel}, {"weighted", "pareto"})
        self.assertTrue(panel[0]["judgments"]["A"]["evidence_refs"])
        self.assertIn("missing-evidence", panel[0]["judgments"]["A"]["state"])
        self.assertTrue(any(r["regret_proxy"] > 0 for r in report["runs"]))

    def test_report_is_replayable_except_measured_time(self):
        a = run_study(self.fixture, seeds=(7,))
        b = run_study(self.fixture, seeds=(7,))
        for report in (a, b):
            report.pop("elapsed_ns")
        self.assertEqual(a, b)

    def test_rank_and_judgment_diagnostics_are_measured_for_each_panel(self):
        report = run_study(self.fixture, seeds=(1, 2))
        for run in report["runs"]:
            if run["strategy"] == "panel":
                self.assertTrue(math.isfinite(run["myopia_proxy"]))
                self.assertIn("pairwise_rank_disagreement", run)
                self.assertIn("review_items_proxy", run)

    def test_seed_sensitivity_separates_stable_full_context_from_partial_runs(self):
        report = run_study(self.fixture)
        sensitivity = report["seed_sensitivity"]
        full = [s for s in sensitivity if s["aperture"] == 1]
        self.assertTrue(all(s["unique_rankings"] == 1 for s in full))
        self.assertTrue(any(s["unique_rankings"] > 1 for s in sensitivity if s["aperture"] == .25))


if __name__ == "__main__":
    unittest.main()
