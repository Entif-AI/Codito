"""Owned, deterministic fixtures. Passing is not production qualification."""
import unittest
from dataclasses import replace
from copy import deepcopy
from codito.continuation_contracts import *

class QueryTests(unittest.TestCase):
    def setUp(self):
        self.index=ScopedIndex();self.scope=Scope('a','read','p1');self.pred={'kind':'revocation'}
        self.w=self.index.query(self.scope,self.pred,authorized=True)
    def test_complete_empty_is_bounded_absence(self): self.assertTrue(self.w.bounded_absence)
    def test_partial_empty_is_not_absence(self): self.assertFalse(replace(self.w,complete=False).bounded_absence)
    def test_empty_query_invalidates_on_matching_insertion(self):
        self.index.put('a','r1',{'kind':'revocation'})
        self.assertFalse(self.index.reusable(self.w,self.scope,self.pred,authorized=True))
    def test_unrelated_tenant_does_not_change_generation(self):
        self.index.put('b','r1',{'kind':'revocation'})
        self.assertTrue(self.index.reusable(self.w,self.scope,self.pred,authorized=True))
    def test_corrected_membership_invalidates(self):
        self.index.put('a','r1',{'kind':'note'});w=self.index.query(self.scope,self.pred,authorized=True)
        self.index.put('a','r1',{'kind':'revocation'})
        self.assertFalse(self.index.reusable(w,self.scope,self.pred,authorized=True))
    def test_deletion_invalidates(self):
        self.index.put('a','r1',{'kind':'revocation'});w=self.index.query(self.scope,self.pred,authorized=True)
        self.index.delete('a','r1');self.assertFalse(self.index.reusable(w,self.scope,self.pred,authorized=True))
    def test_unchanged_record_does_not_increment(self):
        self.index.put('a','r1',{'kind':'revocation'});w=self.index.query(self.scope,self.pred,authorized=True)
        self.index.put('a','r1',{'kind':'revocation'});self.assertTrue(self.index.reusable(w,self.scope,self.pred,authorized=True))
    def test_authorization_change_invalidates(self): self.assertFalse(self.index.reusable(self.w,replace(self.scope,policy_epoch='p2'),self.pred,authorized=True))
    def test_purpose_change_invalidates(self): self.assertFalse(self.index.reusable(self.w,replace(self.scope,purpose='train'),self.pred,authorized=True))
    def test_revoked_admission_does_not_reuse(self): self.assertFalse(self.index.reusable(self.w,self.scope,self.pred,authorized=False))
    def test_changed_query_version_invalidates(self): self.assertFalse(self.index.reusable(self.w,self.scope,self.pred,authorized=True,query_version='v2'))
    def test_changed_predicate_invalidates(self): self.assertFalse(self.index.reusable(self.w,self.scope,{'kind':'note'},authorized=True))
    def test_partial_witness_is_not_reusable(self): self.assertFalse(self.index.reusable(replace(self.w,complete=False),self.scope,self.pred,authorized=True))
    def test_unadmitted_query_exposes_no_witness(self):
        with self.assertRaises(PermissionError): self.index.query(self.scope,self.pred,authorized=False)
    def test_scope_cannot_omit_policy(self):
        with self.assertRaises(ValueError): Scope('a','read','')

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.files={'sources/a':b'a','edges.json':b'[]','effects.json':b'{}'}
        self.cut={'sources':'s1','edges':'e1','effects':'x1'}
        self.m=capture_manifest(self.files,set(self.files),self.cut,self.cut)
    def test_full_manifest_restores_all_components(self): self.assertTrue(restore_plan(self.m,self.files,{})['rebuild_indexes'])
    def test_mixed_capture_is_rejected(self):
        with self.assertRaises(ValueError): capture_manifest(self.files,set(self.files),self.cut,{**self.cut,'effects':'x2'})
    def test_missing_required_component_is_rejected(self):
        with self.assertRaises(ValueError): capture_manifest(self.files,{'missing'},self.cut,self.cut)
    def test_tamper_is_rejected(self):
        with self.assertRaises(ValueError): restore_plan(self.m,{**self.files,'sources/a':b'b'}, {})
    def test_missing_payload_is_rejected(self):
        with self.assertRaises(ValueError): restore_plan(self.m,{'sources/a':b'a'}, {})
    def test_unmanifested_payload_is_rejected(self):
        with self.assertRaises(ValueError): restore_plan(self.m,{**self.files,'extra':b''}, {})
    def test_unsafe_path_is_rejected(self):
        with self.assertRaises(ValueError): capture_manifest({'../outside':b'x'},{'../outside'},self.cut,self.cut)
    def test_old_authority_is_not_reactivated(self):
        m=deepcopy(self.m);m['restore_authority']='reuse_old_lease'
        with self.assertRaises(ValueError): restore_plan(m,self.files,{})
    def test_ambiguous_and_submitted_effects_reconcile(self):
        p=restore_plan(self.m,self.files,{'one':'ambiguous','two':'observed','three':'submitted'})
        self.assertEqual(p['reconcile'],['one','three']);self.assertFalse(p['automatic_effect_replay']);self.assertFalse(p['live_leases_restored'])
    def test_unknown_effect_state_is_rejected(self):
        with self.assertRaises(ValueError): restore_plan(self.m,self.files,{'x':'probably_done'})

class IntentTests(unittest.TestCase):
    def setUp(self): self.x=FencedIntentExecutor();self.x.advance_epoch(1)
    def test_same_key_same_payload_no_second_effect(self):
        self.assertEqual(self.x.execute('a','k','d',1,admitted=True),'applied')
        self.assertEqual(self.x.execute('a','k','d',1,admitted=True),'duplicate');self.assertEqual(self.x.effects,1)
    def test_same_key_different_payload_conflicts(self):
        self.x.execute('a','k','d',1,admitted=True)
        with self.assertRaises(ValueError):self.x.execute('a','k','other',1,admitted=True)
        self.assertEqual(self.x.effects,1)
    def test_distinct_intents_can_have_identical_payloads(self):
        self.x.execute('a','k1','d',1,admitted=True);self.x.execute('a','k2','d',1,admitted=True);self.assertEqual(self.x.effects,2)
    def test_same_key_in_distinct_scopes_is_distinct(self):
        self.x.execute('a','k','d',1,admitted=True);self.x.execute('b','k','d',1,admitted=True);self.assertEqual(self.x.effects,2)
    def test_replaced_worker_cannot_act(self):
        self.x.advance_epoch(2)
        with self.assertRaises(ValueError):self.x.execute('a','k','d',1,admitted=True)
        self.assertEqual(self.x.effects,0)
    def test_missing_admission_is_rejected(self):
        with self.assertRaises(PermissionError):self.x.execute('a','k','d',1,admitted=False)
    def test_epoch_cannot_go_backwards(self):
        with self.assertRaises(ValueError):self.x.advance_epoch(1)

if __name__=='__main__': unittest.main(verbosity=2)