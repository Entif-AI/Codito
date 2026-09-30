# Salience metabolism in UCA

**Status:** Working research note, post-ETR-2026-12  
**Source:** ETR-2026-14, *SÍ SÉ SON: Salient Impact, Exigence and Osmotic Novelty*  
**Authority:** Exploratory. This note does not amend the source-locked ETR-2026-12 registers or define new Rosetta Core semantics.

UCA needs an explicit answer to a simple allocation question: what deserves cognition now?

The architecture already separates evidence, reusable state, operator selection, authority, and effect. Those controls do not decide which newly ingested signals deserve scarce model time, context hydration, graph expansion, research, or human attention. SÍ SÉ SON supplies a candidate salience layer for that gap.

## Architectural placement

Salience belongs after source-preserving ingestion and before expensive cognition. It can also recur inside later stages when new evidence, aggregate patterns, contradictions, or failures appear.

```text
sources and events
      |
      v
Rosetta / Akasha ingestion
      |
      v
SÍ SÉ SON salience
      |
      v
Tapestry compilation / OMoC planning
      |
      v
GNOSIS operators and reusable computation
      |
      v
Commitment / Guard
      |
      v
effects, observations, evaluation
      |
      +----> process learning and revised priors ----+
                                                    |
                                                    +--> salience again
```

This layer allocates attention. It does not establish truth, utility, authorization, or permission to act.

## Three salience signals

The working primitive keeps three dimensions separate.

- **Salient Impact (SÍ):** the magnitude of possible consequence, positive or negative.
- **Salient Exigency (SÉ):** how soon or intensely the matter deserves attention under present conditions.
- **Salient Novelty:** departure from expectation and the amount of model revision or learning the signal may induce.

Novelty is broader than first occurrence. Contradictions, missing expected events, unexpected transitions, newly visible aggregate patterns, and failures that expose unknown weaknesses can all be novel.

The triad is provisional. UCA should not add a fourth primitive for aesthetic completeness, and it should not freeze these properties into one weighted score. The public research surface can define what the dimensions mean while implementation-specific weighting, thresholds, and routing remain separate concerns.

## Recursive salience

A low-salience leaf event can become important through accumulation. Salience therefore applies at more than one scale:

```text
event -> cluster -> pattern -> trend -> system condition
```

The reverse direction matters too. A salient contradiction can point back toward assumptions, transforms, procedures, or decisions that helped produce the contradicted state.

This makes salience compatible with GNOSIS dependency tracking and correction propagation. It does not replace either mechanism. Salience says that a change deserves attention. Dependency structure says what the change can affect.

## SÍ -> SÉ -> SON

The mnemonic also describes a candidate assimilation cycle.

**SÍ** recognizes consequence without premature closure: this may matter.

**SÉ** interrogates the current interpretation: what do we think we know, what remains uncertain, what deserves attention now, and what would change the judgment?

**SON** asks whether consequential novelty has actually propagated into the relevant cognitive system. Storage alone does not establish learning. Retrieval alone does not establish learning. A useful idea becomes operationally assimilated when it changes later cognition or behavior under the conditions where it should apply and continues to survive evaluation.

The recursive form is:

```text
SÍ_t -> SÉ_t -> SON_t -> revised priors -> SÍ_(t+1)
```

This cycle must preserve dissent and corrigibility. Collective uptake does not convert consensus into truth.

## Relationship to the four serialization boundaries

Salience is orthogonal to the serialization model in `serialization-boundaries.md`.

The four serialization boundaries ask where cognition pays avoidable representation, sequencing, or reconstruction costs. Salience asks whether a candidate signal deserves expensive cognition in the first place.

Together they suggest a more complete allocation sequence:

```text
What deserves cognition?
      -> SÍ SÉ SON
What valid cognitive capital already exists?
      -> Akasha / GNOSIS
What unresolved work remains?
      -> Tapestry / dependency frontier
Which eligible operator should perform it?
      -> OMoC
What may become a commitment or effect?
      -> Commitment / Guard
```

A system can reduce recomputation and still waste enormous resources on unimportant work. A salience layer attacks that failure mode without turning every signal into a universal score.

## Failure as information

The desired experimental failure is often low impact, low exigency, and high novelty. It teaches the system something new without creating an emergency or large irreversible cost.

Repeated failure of the same class is different. Once the failure becomes familiar, recurrence can indicate a propagation defect. The system learned locally but failed to change the later mechanism that reproduced the mistake.

This connects salience to process intelligence. Corrections, near misses, surprising successes, and repeated failures can become candidate evidence about how the architecture itself learns.

## Osmotic learning

SON creates a useful distinction between stored knowledge and operationally assimilated knowledge.

A future Codito experiment can track a chain such as:

```text
session insight
  -> architectural conjecture
  -> candidate principle
  -> changed workflow or skill
  -> later behavior
  -> evaluation
  -> revised principle
```

Useful measures include propagation breadth, depth, latency, cross-domain transfer, selective rejection, mutation, reinforcement, resistance, and downstream behavioral change.

The purpose is not to maximize propagation. A bad idea should fail to spread. A context-bound idea may remain local. An unresolved idea may stay provisional. The research question is whether validated learning reaches the places where it should matter without erasing scope, provenance, or dissent.

## UCA integration map

The salience layer sharpens several existing UCA components without replacing them.

| UCA surface | Salience contribution |
| --- | --- |
| Rosetta | Represents source identity, evidence, provenance, and later salience evidence without making salience a Core truth claim. |
| Akasha | Preserves source material and the persistent state against which expectations, recurrence, and changed context can be evaluated. |
| GNOSIS | Uses salient changes to focus revalidation and reuse while dependency edges determine actual propagation scope. |
| Tapestries | Compile working context from material judged relevant to the current task rather than hydrating everything available. |
| OMoC | Consumes salience evidence as one input to planning or routing while capability, policy, cost, and assurance remain separate. |
| Commitment | Distinguishes "this deserves attention" from "this is worth wagering resources on." |
| Guard | Distinguishes "this deserves attention" from "this effect is authorized." |
| Process intelligence | Treats recurring corrections and informative failures as evidence about how the system learns and fails to propagate learning. |
| Swarm Gnosis | Lets validated insights propagate across participants without making broad propagation or consensus a truth test. |

## Candidate experiments

The first experiments should test the information value of the abstraction before designing a production scoring engine.

### Attention gating

Compare an ungated or simple-priority baseline with a cheap explainable salience pass on a fixed corpus and task stream. Hold the available evidence constant.

Measure useful-signal recall, missed consequential signals, unnecessary escalations, time to attention, expensive model work avoided, human review burden, and downstream decision quality. A salience layer that saves tokens while hiding important evidence has failed.

### Recursive accumulation

Construct streams where individual events are low impact, low exigency, and unsurprising, but their aggregate forms a consequential pattern. Include controls where repetition remains harmless.

Measure whether the aggregate becomes salient at the correct scale, how quickly it appears, and how often the system promotes meaningless repetition.

### Osmotic propagation

Introduce a bounded candidate principle with known applicability and observe whether later relevant workflows change. Include irrelevant workflows, known exceptions, negative evidence, and a later correction.

Measure propagation breadth, latency, correct activation, false activation, correction uptake, and whether downstream behavior changes rather than merely retrieving the principle text.

## Research and authority boundaries

Codito should keep this surface representational and experimental.

Public work may define the salience dimensions, evidence requirements, failure states, evaluation fixtures, and observable outcomes. It should not publish tuned weighting formulas, private thresholds, routing heuristics, learned coefficients, or other protected operating policy merely to make the concept executable.

A salience assessment must not silently promote epistemic or operational status. High impact does not prove a claim. High exigency does not authorize an effect. High novelty does not make an interpretation correct. Broad SON propagation does not make consensus true.

## Non-claims

This note does not claim that:

- impact, exigency, and novelty are the final complete basis of salience.
- any one scalar function can combine them correctly.
- the current repository implements salience routing.
- a salience layer will reduce total cost on every workload.
- novelty is inherently valuable.
- consensus, repetition, or propagation establishes truth.
- storing a principle means the system has learned it.

The immediate research target is narrower. Test whether a small, inspectable salience layer helps UCA spend cognition on better targets and learn from later outcomes.
