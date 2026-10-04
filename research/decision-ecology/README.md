# Partial-information decision experiment

[Codito #70](https://github.com/Entif-AI/Codito/issues/70) owns this synthetic
experiment. No fixture value is an Entif production weight or allocation rule.
Rosetta #1134 owns decision representations, #1495 budget state, #1483 later
episode outcomes and #1509 work lifecycle. This Python/JSON fixture is a research
instrument and claims no official Rosetta schema or conformance.

Run `python -m codito.decision_ecology research/decision-ecology/fixture.json`.
The checked-in `results.json` preserves the actual run. Its elapsed nanoseconds
are measured on the orchestration host; all tests and experiment logic are
lightweight and offline. Tokens, model cost and human review time are unmeasured.

Five representatives A-E each receive all four approved local fact units and
0/1/2/4 units from each peer, for 0/25/50/100% apertures. Sampling is balanced by
peer and reproducible for seeds 3, 11 and 29. A fact unit can contain several
attributed candidate criteria, so percentages describe dossier units rather
than equal token shares. Every representative sees the exact same nine-candidate
grid. Grid/profile/context digests and sampled fact IDs survive in each record.

Representatives are simulated fixture readers, not live neural models. Their
criteria come from authored dossier judgments, and an explicit toy profile
supplies weights. Missing peer contributions are zero-imputed lower bounds for
this treatment, explicitly marked `bounded-missing-evidence`; they are not
observed zero value. Future experiments can replace this treatment and inject
bounded semantic criterion evidence without changing the formal aggregation.

Weighted sum ranks all candidates. Pareto filtering removes dominated choices
before weighted ranking. Pareto may remove a low-scored enabling prerequisite;
that loss is retained as a negative result. Both use the same deterministic
budget, declared-dependency, duplicate and exclusivity controller as the random,
prerequisite-order and local-A baselines. Constraints supplied by this controller
are not competence attributed to a semantic judge. A hidden prerequisite is
visible only in E's sampled evidence until independent outcome evaluation.

Separate authored terminal outcomes include shared unlocks, local benefit,
future benefit, competing solutions, duplicate proposals, negative externality
and hidden dependency failure. Evaluation consults truth only after selection.
An exhaustive finite oracle enumerates legal budget subsets for a regret proxy;
its information is not passed to representatives. Successful completion does
not revise an intermediate judgment, dissent record or missing-evidence state.

Metrics are selected-work quality in authored outcome units, shared unlocks,
duplicate-proposal avoidance, failed-prerequisite cost as rework, regret to the
finite oracle, pairwise rank disagreement to the full weighted panel, and
myopia as absolute criterion deviation from full-dossier fixture judgments.
The latter reference is attributed judgment, not world truth. Human review
burden is a proxy counting candidates whose representative weighted scores
differ by the explicit experimental gap. UTF-8 context bytes are measured over
actual serialized fact units. Seeds and all per-run ranks expose sensitivity.

The full-context strong-model comparator is `not-run`: this experiment has no
qualified provider or model invocation. The full-context simulated panel is a
distinct available control. No claim about model ability, 25% optimality, a
production allocation policy or real productivity follows from these runs.

## Preregistration posture

`preregistration.json` is an unregistered protocol record, not a retrospective
claim of sealed evaluation. Fixed fixture, seeds, treatments and metric rules
are digest-bound; the synthetic outcomes are authored and public. Advance only
if a later independent task family retains quality/recall while reducing full
cost. Reject or refine if aperture sensitivity, hidden dependencies or Pareto
pruning erase gains. Negative and inconclusive outcomes remain first-class.
