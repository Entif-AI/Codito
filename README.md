# Codito

> *Codito, ergo sum.*

Codito is the experimental and reference implementation workspace for Entif.AI's **Unified Cognitive Architecture (UCA)**.

Rosetta remains the authority for Rosetta Core semantics. Codito composes and tests those semantics. It does not redefine the Rosetta Core Spine.

## Why Codito

Model inference is one execution substrate, not the ontology of cognition. Codito studies whether useful cognition can avoid four different serialization costs:

- **token seriality:** output advances through a sequential generation chain;
- **representational seriality:** intermediate cognition is repeatedly flattened into language;
- **workflow seriality:** independent operations run in prompt order instead of dependency order;
- **historical seriality:** useful cognition is forgotten and later recomputed.

Model architecture can lower the cost of one reasoning episode. UCA also asks whether a system can reduce how many expensive episodes are required, which parts must pass through language, and what reusable state survives afterward.

The working synthesis, candidate experiments, and Cognitive IR hypothesis are documented in [Serialization boundaries and Cognitive IR](docs/serialization-boundaries.md).

UCA also has an attention-allocation problem. Not every available signal deserves the same cognitive budget. SÍ SÉ SON treats impact, exigency, and novelty as separate salience dimensions between ingestion and expensive cognition. That layer is orthogonal to the four serialization costs: serialization asks how cognition pays, while salience asks what deserves cognition at all.

See [Salience metabolism in UCA](docs/salience-metabolism.md) for the working architecture and research plan.

## Status

Codito is research software. The current code is a finite reference model extracted from ETR-2026-12. It tests specific architectural distinctions and failure cases. It is not a production cognitive runtime, Rosetta conformance implementation, authorization service, database, or distributed-systems proof.

The initial baseline contains 55 deterministic unit tests with no runtime dependencies beyond Python 3.10 or newer. They cover:

- independent value, evidence, and admission change propagation;
- fail-closed serving context and expiry behavior;
- effect-state transitions and ambiguous replay;
- inheritance loss and evidence genealogy;
- bounded collection completeness and correction closure;
- scoped query witnesses for bounded absence;
- coherent recovery cuts and tamper detection;
- intent-bound idempotency and stale-executor fencing.

## Run the reference tests

```bash
python -m unittest discover -s tests -v
```

No provider credentials, network calls, model calls, external effects, or third-party Python packages are required.

## Repository map

- `codito/` contains the finite executable reference models.
- `tests/` contains positive and negative contract fixtures.
- `technical/` contains candidate UCA contracts and architecture dependency data from the ETR-2026-12 production package.
- `technical/rosetta-owner-crosswalk.json` maps Codito engineering items, candidate contracts, and selected hypotheses to current Rosetta owners and opaque protected-authority IDs without rewriting the source-locked research registers.
- `research/` contains the source-locked hypothesis registry, proposed engineering backlog, and preregistration template.
- `interop/rosetta/` contains bounded interoperability probes. These are evidence about a pinned Rosetta implementation, not Codito-owned Rosetta semantics.
- `docs/rosetta-alignment.md` records the authority boundary for this repository.
- `docs/serialization-boundaries.md` records a post-ETR research synthesis on serialization, Cognitive IR, and candidate experiments.
- `docs/salience-metabolism.md` records the post-ETR SÍ SÉ SON salience and assimilation research surface.

## Research posture

A passing test establishes only the property exercised by that test. It does not establish production safety, benchmark savings, model-learning efficacy, distributed consistency, or Rosetta conformance.

Codito makes UCA claims easier to inspect, falsify, reproduce, and replace when evidence warrants a better mechanism.

Post-ETR research notes do not silently rewrite the source-locked ETR-2026-12 registers. A new idea becomes part of the formal program only after an explicit research or engineering update records its scope and evidence boundary.

## Source

The initial reference model comes from **ETR-2026-12, Entif.AI Unified Cognitive Architecture**, native continuation source lock `ETR12-NATIVE-SL-20260929-02`.

Rosetta reference pin for the initial alignment pass: `1fc05c404d15fa7cc9713e7ee19d87b94316f07a`.

Ownership reconciliation was repeated on 2026-10-02 against Rosetta `9c2006ef2ffc06ae876d4b311112bb803beab897`; see `technical/rosetta-owner-crosswalk.json`.

## License

MIT. See `LICENSE`.
