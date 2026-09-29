# Codito

> *Codito, ergo sum.*

Codito is the experimental and reference implementation workspace for Entif.AI's **Unified Cognitive Architecture (UCA)**.

Rosetta remains the authority for Rosetta Core semantics. Codito composes and tests those semantics. It does not redefine the Rosetta Core Spine.

## Status

Codito is research software. The current code is a finite reference model extracted from ETR-2026-12. It tests specific architectural distinctions and failure cases. It is not a production cognitive runtime, Rosetta conformance implementation, authorization service, database, or distributed-systems proof.

The initial baseline contains 55 deterministic unit tests with no runtime dependencies beyond Python 3.10 or newer. They cover:

- independent value, evidence, and admission change propagation.
- fail-closed serving context and expiry behavior.
- effect-state transitions and ambiguous replay.
- inheritance loss and evidence genealogy.
- bounded collection completeness and correction closure.
- scoped query witnesses for bounded absence.
- coherent recovery cuts and tamper detection.
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
- `research/` contains the hypothesis registry, proposed engineering backlog, and preregistration template.
- `interop/rosetta/` contains bounded interoperability probes. These are evidence about a pinned Rosetta implementation, not Codito-owned Rosetta semantics.
- `docs/rosetta-alignment.md` records the authority boundary for this repository.

## Research posture

A passing test establishes only the property exercised by that test. It does not establish production safety, benchmark savings, model-learning efficacy, distributed consistency, or Rosetta conformance.

Codito makes UCA claims easier to inspect, falsify, reproduce, and replace when evidence warrants a better mechanism.

## Source

The initial reference model comes from **ETR-2026-12, Entif.AI Unified Cognitive Architecture**, native continuation source lock `ETR12-NATIVE-SL-20260929-02`.

Rosetta reference pin for the initial alignment pass: `1fc05c404d15fa7cc9713e7ee19d87b94316f07a`.

## License

MIT. See `LICENSE`.
