import dataclasses
import unittest

from codito.graph_navigation import (Graph, Heat, Visit, fixtures, navigate, recruit, run_study)


class GraphNavigationTests(unittest.TestCase):
    def setUp(self):
        self.case = fixtures()[0]
        self.graph = self.case["graph"]

    def test_heat_updates_cannot_mutate_graph_facts(self):
        before = self.graph.digest
        heat = Heat((Visit("hot", "repair", 0, True, "episode:1", self.graph.digest),))
        heat.score("hot", "repair", 2, "decayed-task", self.graph.digest, 2)
        self.assertEqual(self.graph.digest, before)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            self.graph.nodes[0].text = "changed"

    def test_decay_is_explicit_and_old_success_fades(self):
        heat = Heat((Visit("hot", "repair", 0, True, "episode:1", self.graph.digest),))
        a = heat.score("hot", "repair", 0, "decayed-task", self.graph.digest, 2)
        b = heat.score("hot", "repair", 4, "decayed-task", self.graph.digest, 2)
        self.assertAlmostEqual(b, a / 4)

    def test_task_and_version_changes_invalidate_reinforced_heat(self):
        heat = Heat((Visit("hot", "old-task", 0, True, "episode:1", "old-version"),))
        self.assertEqual(heat.score("hot", "repair", 2, "decayed-task", self.graph.digest, 2), 0)
        self.assertEqual(heat.score("hot", "repair", 2, "frequency", self.graph.digest, 2), 1)

    def test_copied_observations_do_not_multiply_independent_reinforcement(self):
        visit = Visit("hot", "repair", 0, True, "episode:copied", self.graph.digest)
        one, copies = Heat((visit,)), Heat((visit,) * 50)
        self.assertEqual(one.score("hot", "repair", 1, "decayed-task", self.graph.digest, 2),
                         copies.score("hot", "repair", 1, "decayed-task", self.graph.digest, 2))

    def test_scout_identity_is_distinct_from_source_evidence_identity(self):
        reports = [dict(scout=f"s{i}", node="rare", evidence_root="same-source", claimed_useful=True) for i in range(4)]
        result = recruit(reports)
        self.assertEqual(result["independent_roots"], 1)
        self.assertEqual(result["scout_count"], 4)
        reports.append(dict(scout="s5", node="rare", evidence_root="different-source", claimed_useful=True))
        self.assertEqual(recruit(reports)["independent_roots"], 2)

    def test_rights_fence_precedes_all_navigation_strategies(self):
        case = next(c for c in fixtures() if c["id"] == "rights-fence")
        for strategy in ("random", "dependency", "lexical", "recency", "frequency", "decayed-task", "scout"):
            result = navigate(case, strategy, 11, budget=4)
            self.assertNotIn("hot", result["trace"])
            self.assertNotIn("hot", result["legal_candidates"])

    def test_rare_decisive_and_stale_hot_cases_remain_falsifiable(self):
        rare = next(c for c in fixtures() if c["id"] == "rare-decisive")
        stale = next(c for c in fixtures() if c["id"] == "stale-hot")
        wrong = navigate(rare, "frequency", 3, budget=1)
        self.assertEqual(wrong["relevant_evidence_recall"], 0)
        self.assertGreater(wrong["wrong_path_rate"], 0)
        result = navigate(stale, "decayed-task", 3, budget=6)
        self.assertEqual(result["relevant_evidence_recall"], 1)

    def test_seeds_replay_and_cold_start_does_not_invent_history(self):
        cold = next(c for c in fixtures() if c["id"] == "cold-start")
        self.assertFalse(cold["heat"].visits)
        a, b = navigate(cold, "random", 11), navigate(cold, "random", 11)
        a.pop("wall_ns")
        b.pop("wall_ns")
        self.assertEqual(a, b)

    def test_heat_has_no_authority_to_create_graph_nodes_or_evidence(self):
        case = dict(self.case)
        case["heat"] = Heat((Visit("invented", "repair", 0, True, "fake", self.graph.digest),))
        result = navigate(case, "frequency", 7)
        self.assertNotIn("invented", result["trace"])
        self.assertNotIn("invented", result["legal_candidates"])

    def test_invalid_time_decay_and_graph_edges_fail(self):
        heat = Heat((Visit("hot", "repair", 10, True, "root", self.graph.digest),))
        for half_life in (0, -1, float("nan")):
            with self.assertRaises(ValueError):
                heat.score("hot", "repair", 20, "decayed-task", self.graph.digest, half_life)
        with self.assertRaises(ValueError):
            Graph("bad", self.graph.nodes, (("missing", "rare", "source-fact"),))

    def test_two_graph_families_and_all_failure_cases_have_metrics(self):
        report = run_study(seeds=(3, 11))
        self.assertEqual(set(report["graph_families"]), {"ast-code", "operational-view"})
        self.assertTrue({"stale-hot", "copied-prior", "rare-decisive", "noisy-agent", "frequent-low-value", "rights-fence", "cold-start"}
                        .issubset({r["fixture"] for r in report["runs"]}))
        for run in report["runs"]:
            self.assertIn("nodes_inspected", run)
            self.assertIn("edges_inspected", run)
            self.assertIn("context_bytes", run)
            self.assertIn("exploration_coverage", run)
        self.assertTrue(any(r["relevant_evidence_recall"] < 1 for r in report["runs"]))


if __name__ == "__main__":
    unittest.main()
