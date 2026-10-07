# Failure Intelligence

Failure intelligence is the Runtime-owned path that converts a material failure, near miss, abnormal termination, or recurring operational trap into immediate preservation, usable diagnosis, and safer continuation.

It is execution infrastructure. Governance remains canonical for institutional adoption, policy status, casebook semantics, supersession, and disclosure authority.

## Trigger

Run this module when any of the following occurs:

- a material failure or near miss;
- a failed or missing handoff that requires reconstruction;
- an abnormal run/session termination;
- an ambiguous side effect with meaningful duplicate/destructive risk;
- a repeated tool/connector/environment trap;
- a user correction that exposes a reusable execution/governance failure;
- a feature-postmortem finding that should become an incident/case candidate.

Do not wait for feature completion if evidence may decay or the same automation may be reused.

## Left-shifted workflow

```text
failure signal
  -> freeze source/evidence
  -> contain immediate risk
  -> recover strongest durable execution state
  -> logic-assisted triage when needed
  -> query prior incidents/root causes/patterns
  -> file or enrich canonical incident
  -> project bounded gotchas into current run
  -> checkpoint the changed risk model
  -> resume only from reconciled state
```

Filing and full remediation are separate commitments.

## Evidence first

Preserve, by durable reference when available:

- exact run/session/thread/work/checkpoint identity;
- issue/spec/plan/repository/branch/PR refs;
- timestamps and relevant tool/connector receipts;
- canonical target state before/after when material;
- user correction or observable failure statement;
- reduced trace/recovery artifact when structured state is absent;
- what is known, inferred, reconstructed, or still unknown.

A missing platform error code does not license a causal assertion such as “context overflow definitely happened.” Record the observable termination and the evidence supporting the leading hypothesis.

## Compose Logic deliberately

Use the `logic` meta-skill for ambiguous, repeated, high-impact, or decision-authoritative failure analysis.

At minimum preserve:

1. **Observation**: what directly happened or was read back.
2. **Interpretation**: what the evidence suggests.
3. **Reconstructed premise**: any bridge needed to infer a mechanism.
4. **Alternative hypotheses / defeaters**: plausible rival causes and what would discriminate them.
5. **Evaluation provenance**: rubric/control used to call something a failure, severity, or governance defect.
6. **Decision boundary**: what is safe to rely on now despite uncertainty.

Do not force formalization when a source-preserving natural-language map is clearer.

## Canonical incident filing

Runtime owns making the filing happen. During migration the legacy `entif-postmortem-logger` may remain as an eager trigger/compatibility veneer, but it should delegate to this module.

Use the canonical ledger contract and its live target state. Bind writes to the live schema/headers before positional mutation. Reuse existing root causes/patterns when they already explain the mechanism; do not multiply abstractions to prove activity.

If the filing write is ambiguous, reconcile the canonical ledger before retrying.

## Prior-failure lookback

Before resuming the same operation family, query relevant incident/pattern history when available.

Retrieve by the strongest available match dimensions:

- tool/connector/service and operation;
- execution capability profile;
- mutation class;
- artifact type / target system;
- failure signature;
- root-cause/pattern tags;
- current workflow stage;
- authority/governance gate.

Prefer exact mechanism/surface matches over vague topical similarity.

## Gotcha projection

Convert relevant prior learning into a **small run-local risk projection**, not a dump of the ledger.

Each gotcha should carry:

- short mechanism label;
- evidence/pattern reference;
- applicability condition;
- prevention/reconciliation action;
- status/freshness;
- whether it is observation-backed, inferred, or policy-backed.

Prioritize using bounded factors such as:

- operation/surface match;
- recurrence frequency;
- recency;
- severity/materiality;
- unresolved/open status;
- evidence quality;
- mitigation applicability.

Exact weights/thresholds are runtime policy, not universal semantics. Recency may increase urgency but must not erase strong older evidence.

Example:

```text
GOTCHA: Drive connector AuthZ/capability state may be stale.
APPLIES WHEN: expected Drive write/read action is absent or transiently denied after prior availability.
DO: rebind/reinitialize and retry capability discovery in the same run; only explicit provider denial is PERMISSION_DENIED; reconcile target before replaying an ambiguous write.
SOURCE: prior incidents/patterns + connector-recovery contract.
```

## Recovery placement

A successor recovering a failed run is often the best-situated observer to file the incident because it is already reconstructing:

- last verified checkpoint;
- unsafely incomplete work;
- exact tool/connector behavior;
- what survived;
- what had to be inferred;
- what the predecessor failed to externalize.

Therefore, after state reconstruction and before broad new mutation:

1. assess materiality;
2. file/enrich the incident if required;
3. retrieve applicable gotchas;
4. incorporate them into the new Runtime handoff/checkpoint;
5. continue.

This is not ceremony. It prevents the recovered run from immediately repeating the predecessor's failure.

## Governance boundary

Runtime may preserve and report evidence, invoke Logic, file incidents, reuse accepted root-cause/pattern records, and rank operational gotchas for the current run.

Runtime may not declare a proposed pattern/policy accepted, rewrite institutional authority, or treat telemetry frequency as self-ratifying doctrine. Those remain Governance responsibilities.
