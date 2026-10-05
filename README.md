# Codito

> *Codito, ergo sum.*

Codito is the experimental and reference workspace for the **connective tissue of Entif AI's Unified Cognitive Architecture (UCA)**.

If Rosetta preserves what an artifact means and where it came from, Bilqis investigates whether explicit meaning can be made cheaper to learn, Akasha preserves admitted persistent state, and IndraNet connects independently bounded participants, Codito studies what has to exist **between** those systems so they can compose into one inspectable cognitive episode.

The short version is:

> **Codito converts correspondence into coherence.**

Not by forcing everything into one ontology. By making dependencies, distinctions, mappings, eligibility, reuse, invalidation, and unresolved novelty explicit enough that the architecture can decide what should happen next without paying a frontier model to reconstruct the entire situation from prose every time.

## The metacognitive atlas

Codito treats cognition itself as something the system can inspect.

A successful result can reveal a reusable transformation. A failed result can reveal a missing distinction. A contradiction can expose two assumptions that should never have been merged. A correction can identify which projections, procedures, routes, and downstream conclusions became stale. A repeated expensive operation can become a candidate for a smaller learned operator or deterministic procedure.

The resulting atlas is developmental. Experience can change not only what the system knows, but the coordinate system by which later cognition is decomposed and routed.

That creates a feedback loop:

```text
experience
   ↓
observation / result / failure / correction
   ↓
explicit dependencies and competing explanations
   ↓
discriminating tests
   ↓
qualified reusable structure
   ↓
cheaper or better task-local cognition
   ↓
new experience
```

The atlas is not a second truth system. Durable meaning remains subordinate to the applicable Rosetta authority and provenance.

## The orchestration problem

Model inference is one execution substrate, not the ontology of cognition.

Codito studies a cognitive episode as an explicit dependency graph that may recruit:

- deterministic operators;
- exact solvers and validators;
- bounded decision-native models;
- local learned functions;
- specialist models;
- general generative models;
- retrieval and persistent memory;
- tools and simulators;
- human expertise.

The architecture should be free to use strong general intelligence when novelty or consequence warrants it and equally free **not** to use it when a smaller, exact, cheaper, or already-validated mechanism can do the job.

This is progressive determinization as a learning strategy: repeated successful cognition can become structured decomposition, then a narrower probabilistic operator, then deterministic procedure where the evidence warrants the demotion in generality.

A cache remembers an answer. Codito is interested in preserving the **method and its validity conditions**.

## The UCA relationship map

| Component | Primary job in the architecture |
| --- | --- |
| **Rosetta** | Public semantic identity, provenance, ambiguity, receipts, lifecycle, interoperability, and authority boundaries. |
| **Bilqis** | Experimental developmental semantics and semantic initialization; asks whether useful relational structure can be cheaper to acquire. |
| **GNOSIS** | Dependency-aware reusable computation and incremental revalidation. |
| **Cognitive Tiles / Lattices / Tapestries** | Materialized semantic objects, relations, and compiled working context. |
| **Akasha / Forget Me Not** | Governed persistent cognition, inheritance, retention, correction, revalidation, and rollback. |
| **SÍ SÉ SON** | Attention allocation through distinct impact, exigency, and novelty signals. |
| **OMoC** | Task-local composition of heterogeneous cognitive operators. |
| **Commitment / Guard / Tripwire** | Separate recommendation, justified commitment, admission to effect, and independent interruption. |
| **Swarm Gnosis** | Rights-aware exchange and correction of reusable cognition across independently bounded participants. |
| **IndraNet** | Relational fabric among those participants, or Jewels, with a current physical-context proving path. |
| **Mission Control / Experience Compiler** | Human- and agent-facing inspection and device/task-specific materialization of governed state. |

Codito is the orchestration and metacognitive seam among these layers, not a claim that they all need one runtime or one internal representation.

## Why semantic typing matters

The architecture is trying to avoid several different taxes at once:

- **token seriality:** bounded machine decisions need not always be narrated token by token before software can use them;
- **representational seriality:** intermediate cognition need not always be flattened into natural language between operations;
- **workflow seriality:** independent operations can run according to dependencies instead of prompt order;
- **historical seriality:** validated work should not be forgotten and later repurchased as inference;
- **rehydration cost:** task-relevant state should not always be reconstructed from raw memory when compact, source-backed structure already exists;
- **maintenance cost:** correcting an upstream premise should reveal which downstream cognition actually depends on it.

Bilqis and Rosetta do not prove those savings. Codito exists partly to make them measurable.

## Context is compiled cognition

Retrieval is not the same thing as context inclusion.

A context compiler can take admitted persistent state and construct a task- and consumer-specific view under rights, authority, uncertainty, time, evidence, latency, and resource constraints. OMoC can then compile **how to operate on that view**.

That gives the architecture two distinct questions:

1. What is this consumer allowed and required to know right now?
2. What cognitive machinery should act on it?

Keeping those questions separate prevents retrieval relevance from quietly turning into permission, and prevents a model's probability from quietly becoming governance.

## Rosetta boundary

Rosetta owns every official schema, data structure, semantic contract, serialization, storage/integration/exchange contract, and adapter used as a public interoperability surface.

Codito owns none of that official meaning by default.

Its code, candidate shapes, tests, and fixtures are demonstrative research support for publications and for later Rosetta or protected implementation planning. A successful Codito experiment is evidence. It is not a constitutional amendment.

## Current status

Codito is research software. The current executable baseline is a finite demonstrative model extracted from earlier ETR-2026-12 production work. The current conceptual architecture follows **ETR-2026-12, Unified Cognitive Architecture v0.5.8**; that does not imply every existing reference file was regenerated from that manuscript revision.

The baseline contains 55 deterministic unit tests with no runtime dependencies beyond Python 3.10 or newer. They cover:

- independent value, evidence, and admission change propagation;
- fail-closed serving context and expiry behavior;
- effect-state transitions and ambiguous replay;
- inheritance loss and evidence genealogy;
- bounded collection completeness and correction closure;
- scoped query witnesses for bounded absence;
- coherent recovery cuts and tamper detection;
- intent-bound idempotency and stale-executor fencing.

Run them with:

```bash
python -m unittest discover -s tests -v
```

No provider credentials, network calls, model calls, external effects, or third-party Python packages are required.

## Repository map

- `codito/` contains the finite executable reference models.
- `tests/` contains positive and negative contract fixtures.
- `technical/` contains candidate UCA contracts and architecture dependency data from the ETR-2026-12 production package.
- `technical/rosetta-owner-crosswalk.json` records that Codito owns nothing official and maps demonstrative engineering items, candidate shapes, and selected hypotheses to their Rosetta data owners and, where relevant, protected policy authorities.
- `research/` contains the source-locked hypothesis registry, proposed engineering backlog, and preregistration template.
- `interop/rosetta/` contains bounded interoperability probes. These are evidence about a pinned Rosetta implementation, not Codito-owned Rosetta semantics.
- `docs/rosetta-alignment.md` records the authority boundary for this repository.
- `docs/serialization-boundaries.md` records the research synthesis on serialization, Cognitive IR, and candidate experiments.
- `docs/salience-metabolism.md` records the SÍ SÉ SON salience and assimilation research surface.

## Research posture

A passing test establishes only the property exercised by that test. It does not establish production safety, benchmark savings, model-learning efficacy, distributed consistency, or Rosetta conformance.

Codito exists to make UCA claims easier to inspect, falsify, reproduce, compose, and replace when evidence warrants a better mechanism.

## License

MIT. See `LICENSE`.
