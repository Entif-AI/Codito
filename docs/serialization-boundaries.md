# Serialization boundaries and Cognitive IR

**Status:** Working research note, post-ETR-2026-12  
**Origin:** 2026-09-29 inference-economics discussion  
**Authority:** Exploratory. This note does not amend the source-locked ETR-2026-12 hypothesis or engineering registers.

Codito treats token generation as one execution substrate rather than the ontology of cognition. The working hypothesis is that cognitive systems pay several different serialization costs, and that different mechanisms can attack different costs without competing for the same role.

## Four serialization boundaries

| Boundary | Failure pattern | UCA connection | Candidate direction |
| --- | --- | --- | --- |
| Token seriality | Output advances one generated token at a time. | Operator execution cost | Multi-token, speculative, block, diffusion, or other non-AR execution |
| Representational seriality | Intermediate cognition must repeatedly become language before another computation can use it. | Rosetta, Bithkuil, Tapestries | Structured or latent model adapters |
| Workflow seriality | Independent operations run in prompt order instead of dependency order. | GNOSIS, OMoC execution cohorts | Dependency-aware batching and parallel execution |
| Historical seriality | Useful cognition is forgotten and recomputed in later episodes. | GNOSIS materialization, Akasha, cognitive inheritance | Reuse, promotion, correction, and successor inheritance |

These boundaries are independent enough that gains can compound. A faster decoder can reduce the cost of one inference episode while GNOSIS reduces how many expensive episodes need to occur. A structured model adapter can reduce representational reconstruction while OMoC batches independent work.

The broader research question is therefore larger than token throughput:

> Can cognition stop being repeatedly serialized, reconstructed, forgotten, and repurchased at every boundary?

## Salience is orthogonal to serialization

Reducing seriality can make cognition cheaper, more parallel, or more reusable. It does not decide which unresolved signals deserve expensive cognition.

SÍ SÉ SON supplies a separate candidate attention layer based on impact, exigency, and novelty. Its immediate role is to sit after source-preserving ingestion and before expensive context hydration, model inference, research, or human review. It can also recur when aggregate patterns, contradictions, failures, or changed context appear.

The relationship is complementary:

```text
salience      -> what deserves cognition?
serialization -> where are we paying avoidable cognitive tax?
reuse          -> what valid work has already been earned?
routing        -> which eligible operator should resolve the remainder?
authority      -> what may become a commitment or effect?
```

See [Salience metabolism in UCA](salience-metabolism.md).

## Cognitive IR hypothesis

A longer-term interpretation of UCA treats portable semantic state as an intermediate representation above any one neural execution architecture.

```text
              portable cognitive IR
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
     transformer   diffusion   recurrent/SSM
       adapter       adapter       adapter
```

The portable object could be a Rosetta artifact, Bithkuil semantic object, Tapestry, procedure, or another governed UCA artifact. A model-specific representation is a compiled target derived from that object.

This interpretation gives the existing architecture compiler-like roles:

- Rosetta supplies interoperable semantic and provenance contracts.
- Bithkuil investigates explicit machine-facing semantic structure.
- Tapestries provide task-specific compiled working sets.
- OMoC selects and composes eligible operators.
- GNOSIS tracks dependencies, reuse, invalidation, and materialization.
- Akasha retains governed durable state.
- Guard and Commitment govern the transition from computation to consequence.

This is an architectural hypothesis. Codito does not currently implement a neural IR compiler, latent-prefix adapter, diffusion reasoner, or model-independent latent representation.

## Research lane: semantic batching

The nearest experiment stays above neural architecture.

**Question:** Can a dependency graph identify independent learned decisions and execute them in compatible cohorts without losing per-node identity, evidence, or retry semantics?

Compare:

1. separate autoregressive calls;
2. ordinary provider batching;
3. dependency-preserving execution cohorts;
4. decision-native or non-autoregressive execution when a qualified implementation exists.

Measure accelerator utilization, decisions per second, tail latency, orchestration cost, task quality, and receipt correctness.

A negative result is useful. If graph analysis and cohort management cost more than they save, keep the simpler execution path for that workload.

This lane overlaps existing ETR hypotheses H3, H4, H6, and the ETR12-C09/C10/C11 contract family.

## Research lane: Bithkuil semantic denoising

Bithkuil's bounded semantic worlds offer a controlled test bed for non-autoregressive semantic inference.

A fixture might contain partially unknown semantic structure:

```text
ENTITY(A)
RELATION(?)
ENTITY(B)
EVIDENCE(?)
SCOPE(global)
POLARITY(?)
```

Compare matched implementations of:

1. an autoregressive semantic decoder;
2. a masked bidirectional semantic denoiser;
3. a block semantic denoiser.

The target is not better prose. The target is correct resolution of interdependent semantic constraints under a fixed information and compute budget.

Measure exact semantic accuracy, calibration, contradictions, revision count, latency, compute, sample efficiency, and failure under ambiguous or conflicting evidence. Use formal oracles where the bounded world permits them.

The experiment should fail cleanly. If autoregression matches or beats denoising on quality and total cost, structured semantics do not create a useful non-autoregressive regime for that task class.

This lane extends the questions already represented by H1 and H4 without changing those source-locked records.

## Research lane: Tapestry direct ingress

Current systems often structure information and then flatten it back into prose before model use:

```text
structured state
      |
      v
serialize as prose
      |
      v
model reconstructs structure
```

Codito should test whether that linguistic round trip is an avoidable intermediate tax.

A staged comparison can use:

1. raw prose or history;
2. conventional retrieval rendered as prose;
3. canonical structured Tapestry serialization;
4. a model-specific structured adapter;
5. a learned latent adapter, if a suitable model permits controlled ingress.

Measure task quality, semantic conservation, source attribution, input representation size, prefill cost, wall time, correction behavior, and portability across model families.

The durable object must remain portable. A GPT-specific, diffusion-specific, or recurrent hidden representation is a derived compilation target. It must not become the only surviving account of the cognitive state.

This lane overlaps H2, H13, H14, and H16.

## Relationship to the ETR-2026-12 program

This note adds a lens across existing questions rather than a new source-locked hypothesis set.

- **H1** already asks whether explicit semantic structure changes learning economics.
- **H2** already tests compiled Tapestries against raw history and ordinary retrieval.
- **H4** already asks whether typed parallel decisions can beat ordinary autoregressive generation.
- **H6** already tests progressive determinization.
- **H13** tests immediate-edge dependency sufficiency.
- **H14** tests recursive computation reuse.
- **H16** tests whether successor systems can inherit explicit cognitive capital more cheaply than reconstructing it.

Future evidence can justify a formal hypothesis revision or a new registered experiment. Until then, this note remains exploratory context around those frozen records.

## Non-claims

This note does not claim that:

- non-autoregressive models will outperform autoregressive models;
- latent reasoning is inherently more correct than language-mediated reasoning;
- semantic structure automatically creates parallel compute;
- a hidden-state representation is portable between model families;
- token savings imply lower total system cost;
- current Codito code implements any neural research lane described here.

The current executable baseline remains a finite contract model. New mechanisms should enter Codito only with explicit comparators, bounded claims, and tests that can reject the attractive story.
