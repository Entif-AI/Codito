"""Deterministic illustrations of UCA candidate boundaries, positive and negative."""
import unittest
from dataclasses import replace
from codito.uca_reference import *


class CandidateContractTests(unittest.TestCase):
    def setUp(self):
        self.base = Materialization("v1", "e1", "a1")
        self.entry = dict(principal="p", entitlement="tenant-a", policy="policy1",
                          source_bundle="bundle1", source_version="source1")
        self.ctx = AdmissionContext(**self.entry, now="2026-09-28T12:00:00Z",
                                    expires_at="2026-09-28T12:01:00Z")

    def test_stable_state_has_no_changes(self):
        self.assertEqual(changed_facets(self.base, self.base), frozenset())

    def test_equal_value_does_not_erase_changed_evidence(self):
        changes = changed_facets(self.base, replace(self.base, evidence_digest="e2"))
        self.assertEqual(changes, frozenset({Facet.EVIDENCE}))
        self.assertTrue(affected(changes, frozenset({Facet.EVIDENCE})))
        self.assertFalse(affected(changes, frozenset({Facet.VALUE})))

    def test_authority_change_does_not_require_changed_value(self):
        self.assertEqual(changed_facets(self.base, replace(self.base, admission_digest="a2")),
                         frozenset({Facet.ADMISSION}))

    def test_complete_current_context_is_eligible(self):
        self.assertEqual(may_serve(self.entry, self.ctx), (True, "ELIGIBLE"))

    def test_absent_context_fails_closed(self):
        self.assertEqual(may_serve(self.entry, None), (False, "MISSING_CONTEXT"))

    def test_missing_binding_fails_closed(self):
        self.assertFalse(may_serve({}, self.ctx)[0])

    def test_changed_entitlement_is_not_a_cache_hit(self):
        self.assertFalse(may_serve(self.entry, replace(self.ctx, entitlement="tenant-b"))[0])

    def test_changed_policy_requires_new_admission(self):
        self.assertFalse(may_serve(self.entry, replace(self.ctx, policy="policy2"))[0])

    def test_expiry_boundary_is_inclusive(self):
        self.assertEqual(may_serve(self.entry, replace(self.ctx, now=self.ctx.expires_at)), (False, "EXPIRED"))

    def test_invalid_time_is_not_silently_eligible(self):
        self.assertEqual(may_serve(self.entry, replace(self.ctx, now="bad")), (False, "INVALID_TIME"))

    def test_naive_time_is_not_a_declared_time_basis(self):
        self.assertFalse(may_serve(self.entry, replace(self.ctx, now="2026-09-28T12:00:00"))[0])

    def test_revoked_context_is_not_eligible(self):
        self.assertEqual(may_serve(self.entry, replace(self.ctx, revoked=True)), (False, "REVOKED"))

    def test_submission_is_not_observed_completion(self):
        with self.assertRaises(ValueError):
            transition(EffectState.AUTHORIZED, EffectState.OBSERVED, "authorization-only")

    def test_empty_transition_evidence_is_refused(self):
        with self.assertRaises(ValueError):
            transition(EffectState.SUBMITTED, EffectState.ACKNOWLEDGED, "")

    def test_ambiguous_effect_requires_reconciliation_before_unsafe_replay(self):
        self.assertFalse(may_replay(EffectState.AMBIGUOUS, False, False))
        self.assertTrue(may_replay(EffectState.AMBIGUOUS, False, True))

    def test_observed_effect_is_not_replayed(self):
        self.assertFalse(may_replay(EffectState.OBSERVED, True, True))

    def test_inheritance_exposes_lost_scope_and_uncertainty(self):
        self.assertEqual(inheritance_losses(frozenset({"content", "scope", "uncertainty"}),
                                             frozenset({"content"})), frozenset({"scope", "uncertainty"}))

    def test_copies_do_not_multiply_independent_roots(self):
        self.assertEqual(len(independent_roots([frozenset({"r1"})] * 5)), 1)
        self.assertEqual(independent_roots([frozenset()]), frozenset())

    def test_model_cost_can_outweigh_payload_savings(self):
        self.assertGreater(transport_cost(100, 10, 10, 5, 5), 90)
        self.assertLess(transport_cost(100, 10, 10, 5, 5, 10), 90)

    def test_invalid_cost_is_refused(self):
        with self.assertRaises(ValueError):
            transport_cost(1, -1, 0, 0, 0)

    def test_partial_collection_is_not_complete(self):
        self.assertFalse(collection_complete(False, "page2", False))
        self.assertFalse(collection_complete(True, None, True))
        self.assertTrue(collection_complete(False, None, True))

    def test_correction_requires_scope_completion(self):
        with self.assertRaises(ValueError):
            advance_correction(1, 2, frozenset({"index", "cache"}), frozenset({"index"}))
        self.assertEqual(advance_correction(1, 2, frozenset({"index"}), frozenset({"index"})), 2)

    def test_correction_epoch_cannot_move_backward(self):
        with self.assertRaises(ValueError):
            advance_correction(2, 1, frozenset(), frozenset())


if __name__ == "__main__":
    unittest.main(verbosity=2)