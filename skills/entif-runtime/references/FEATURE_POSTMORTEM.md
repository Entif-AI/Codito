# Feature Post-Mortem Runtime Module

This module absorbs the execution-facing behavior formerly exposed as `entif-feature-postmortem` while preserving Governance as the institutional-learning authority.

## Trigger

Run only after the full root feature reaches its governing completion gate on trunk and, when deployment is part of the contract, required production verification.

Do not confuse this with immediate incident logging. Material failures discovered during active work still trigger the independently eager `entif-postmortem-logger` when its materiality gate applies.

## Runtime-owned work

1. Compile the complete feature work tree and accepted implementation evidence: issues, plans, feature/runtime handoffs, Work Stack receipts, PR/review history, merge/production proof, validation evidence, and prior incidents.
2. Resolve the applicable governed evaluator/rubric authority. Protected scoring/routing details remain protected; do not copy them into public Codito Skill text.
3. Invoke the required evaluator configuration and record objective evidence plus explicit residual uncertainty.
4. Convert material findings into implementation-complete proposal(s) with target surfaces, proving steps, rollback/supersession notes, and required authority references.
5. Create a **separate** proposal issue/workstream and draft PR when authorized. Do not contaminate the completed feature record with the improvement experiment.
6. Automation may observe, recommend, stage, test, and prepare proposals. It may not silently merge, activate, or promote protected self-improvements.
7. Hand institutional candidates to Governance for case/pattern/policy/adoption/version/supersession handling.

## Governance boundary

Runtime may say:

- what evidence was observed;
- what evaluator output was produced;
- what remediation proposal was staged;
- what verification evidence supports the proposal.

Runtime may not convert a score or proposal into accepted governance merely by writing it down.

Governance owns accepted institutional memory, adoption, supersession, policy status, and disclosure posture.

## Closeout

The post-mortem workstream itself uses normal Runtime durability/handoff rules and the shared PR Closeout capability. It remains independently reviewable and must not auto-merge merely because the evaluator recommended the change.
