# Rosetta alignment

Codito is an application and research layer over Rosetta semantics. It is not a competing semantic authority.

## Authority

The Rosetta v3.0.0 Core Spine owns the meanings of Core artifacts such as `Run`, `Action`, `ToolCall`, `Observation`, `Evaluation`, `Receipt`, and `Tapestry`. Codito must reuse, compose, specialize, or translate those meanings through governed Rosetta mechanisms. It must not redefine them locally.

The initial Codito reference harness uses ordinary Python types to isolate finite UCA propositions. Those fixture types are test instruments. They are not new `rosetta.*` artifact kinds and do not claim Rosetta conformance.

## Public and protected boundary

Codito may publish representational contracts, validation fixtures, interoperability mappings, research hypotheses, and failure semantics needed for independent inspection. Operational advantage remains separately governed. Routing algorithms, scoring formulas, promotion logic, context optimization, private inference, and other protected methods do not become public merely because Codito has a public representation for their inputs or outputs.

## Initial proof boundary

The first baseline proves only that the included deterministic fixtures behave as asserted. It does not prove distributed execution, database durability, provider semantics, authorization correctness, learned-model performance, physical actuation, or production readiness.

## Rosetta pin

The initial authority review used Rosetta commit:

`1fc05c404d15fa7cc9713e7ee19d87b94316f07a`

Future work that changes Rosetta-facing behavior must repeat the authority check against the then-current Rosetta authority and applicable public/private bridge edges.
