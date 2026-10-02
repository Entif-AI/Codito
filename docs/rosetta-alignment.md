# Rosetta alignment

Codito is an application and research layer over Rosetta semantics. It is not a competing semantic authority.

## Authority

The Rosetta v3.0.0 Core Spine owns the meanings of Core artifacts such as `Run`, `Action`, `ToolCall`, `Observation`, `Evaluation`, `Receipt`, and `Tapestry`. Codito must reuse, compose, specialize, or translate those meanings through governed Rosetta mechanisms. It must not redefine them locally.

The initial Codito reference harness uses ordinary Python types to isolate finite UCA propositions. Those fixture types are test instruments. They are not new `rosetta.*` artifact kinds and do not claim Rosetta conformance.

## Public and protected boundary

Codito may publish representational contracts, validation fixtures, interoperability mappings, research hypotheses, and failure semantics needed for independent inspection. Operational advantage remains separately governed. Routing algorithms, scoring formulas, promotion logic, context optimization, private inference, and other protected methods do not become public merely because Codito has a public representation for their inputs or outputs.

## Compiled adapter boundary

Future Codito research may test model-specific projections of portable UCA artifacts, including structured inputs or learned latent adapters. Such a projection is a compilation target, not the durable semantic authority.

The portable Rosetta or UCA artifact must remain independently identifiable. Replacing a model or adapter must not mutate that source artifact or make its meaning depend on one provider's hidden state.

A qualified adapter should declare enough information to identify its source artifact, adapter version, model target, and known loss or reconstruction contract. These are research requirements for Codito adapters, not new Rosetta Core semantics.

## Salience boundary

Codito may represent salience dimensions, evidence, scopes, aggregate lineage, and evaluation outcomes needed for independent research. A salience assessment does not confer truth, provenance authority, commitment readiness, or effect admission.

Public documentation may define the meanings of impact, exigency, novelty, and observable failure states. Tuned weighting formulas, thresholds, ranking policy, adaptive routing, and other operational selection methods remain separate implementation concerns subject to the public/private boundary.

Osmotic propagation also does not create semantic authority. A belief, principle, or method may spread across workflows or participants while remaining provisional, scoped, contested, or wrong.

## Initial proof boundary

The first baseline proves only that the included deterministic fixtures behave as asserted. It does not prove distributed execution, database durability, provider semantics, authorization correctness, learned-model performance, physical actuation, or production readiness.

The serialization and Cognitive IR work in `docs/serialization-boundaries.md` is exploratory. The repository does not currently implement a neural IR compiler, latent-prefix adapter, or non-autoregressive semantic reasoner.

The salience and osmotic-learning work in `docs/salience-metabolism.md` is also exploratory. The repository does not currently implement a production salience scorer, attention router, or cross-agent learning mechanism.

## Rosetta pin

The initial authority review used Rosetta commit:

`1fc05c404d15fa7cc9713e7ee19d87b94316f07a`

Future work that changes Rosetta-facing behavior must repeat the authority check against the then-current Rosetta authority and applicable public/private bridge edges.

## 2026-10-02 ownership reconciliation

A cross-repository review against current Rosetta public contracts and protected-authority identifiers is recorded in `technical/rosetta-owner-crosswalk.json`.

The crosswalk is a planning projection. It does not modify the source-locked ETR-2026-12 registers or promote Codito candidate contracts into Rosetta semantics.

Current dispositions:

- context compilation uses Core `Tapestry`, public Rosetta #1488, and protected authority `IPR-0027`;
- control-plane selection composes existing public routing, budget, planner, specialist, and operator contracts plus their mapped protected authorities;
- public salience representation is owned by Rosetta #1670; protected SÍ SÉ SON operational policy is mapped to `IPR-0218`;
- progressive determinization composes public StrategyEpisode, experiment, benchmark, and procedural-promotion contracts; protected counterfactual mechanism-substitution work is mapped to `IPR-0219`;
- Codito C22 remains a research fixture over existing view/frontier, revalidation, and graph-query contracts rather than a new query ontology;
- Codito C23 remains a research fixture over existing replay, execution-tape, migration/recovery, and protected continuity authority.

The canonicalization interoperability probe has one concrete current finding. The pinned Rosetta helper labels its output `RFC8785_JCS`, but JavaScript integer-like property ordering can diverge from JCS lexicographic ordering. Public Rosetta #528 owns the conformance vectors and any implementation repair. Codito retains the probe as evidence.

Future Codito work should update the crosswalk when a candidate contract gains a canonical owner, when an owner is superseded, or when a genuine gap survives Rosetta and protected-authority review.
