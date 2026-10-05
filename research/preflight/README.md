# Cheap-first preflight experiment

[Codito #71](https://github.com/Entif-AI/Codito/issues/71) owns this offline
experiment. Rosetta #1089 owns benchmark contracts, #457 weak-to-strong evidence,
#1480/#1507 routing evidence and #1712 interchange. The Python dataclasses and
synthetic transport wrapper here are research instruments, not official schemas,
an AXI adapter or a production routing policy.

Run `python -m codito.preflight`. `results.json` retains the actual measured run.
Seven authored fixture generators cover large valid JSON, truncated JSON-like
input, source code, verbose browser state, MCP/AXI-like response fields,
chronological logs and a tiny-input overhead control. All six required families
have raw, structural, exact-path/AST, literal heuristic and layered treatments.

Two synthetic placements exercise distinct input operations: a temporary file
write/read and a tool-envelope decode/digest check. The latter preserves both
transport and payload hashes. It is not a deployed MCP transport. The measured
preflight time includes fixture boundary instrumentation, source parsing,
selection, identity checks and packet serialization, so it must not be reported
as production latency or model savings.

The structural control inspects a fixed 128-byte prefix and can miss a decisive
region. The deterministic filter uses exact JSON pointers or AST symbol ranges,
including decorator preconditions. The heuristic is an explicit keyword tree
over original source lines. The layered treatment prefers a requested structural
region and otherwise uses the heuristic. A bounded semantic scorer can select
only offered excerpt identities or abstain; no provider is needed or evaluated.
All source/UI text is untrusted data and none of these choices grants effects.

Every excerpt binds its immutable source digest, exact byte range, optional
path and excerpt identity. Hydration rejects source/range/path drift. UTF-8
offsets and JSON escape bytes survive. Complete JSON is validated before path
indexing. Duplicate keys, nonfinite constants and malformed/truncated sources
never become invented repaired meaning. Opaque malformed line excerpts remain
useful source evidence with `inspect_more`, not a repaired parsed object.

Missing paths can request fuller source, and a raw packet hydrates the entire
original. Bounded snippets do not claim complete program semantics; enclosing
scope, dependencies or omitted context can still require escalation. The toy
fixtures' required spans remain outside projection and measure recall and false
exclusion afterward.

Metrics include source bytes, serialized packet bytes, actual preflight
nanoseconds, decisive-span recall, false exclusions, syntax/shape status and
abstention. The strict probe's `syntax_valid` also rejects ambiguous duplicate
keys for projection even though duplicate-key JSON is lexically parsable.
The raw control counts original payload bytes; narrowed packets include metadata
and lossless base64 snippet bytes. This charges overhead to narrowing rather
than treating a short content string as the whole context cost.

`net-positive-bytes-only` means decisive evidence survives with fewer packet
bytes. It does not establish net inference/compute benefit. `net-negative`
means a decisive span was excluded or packet bytes exceeded raw bytes. Invalid
syntax or unresolved completeness can remain inconclusive despite compression.
The tiny control is deliberately net-negative; prefix sampling can lose decisive
evidence. Model calls are actually zero, tokens/cost are unmeasured and no
frontier-call savings are invented.

`value_of_information` separately computes explicit probability times error
cost and compares it to a supplied, comparable context cost. It can reject more
context. The caller supplies those quantities; these are illustrative mathematics,
not private production thresholds. A future independent study must account for
all preflight/model/rehydration costs and can reject every cheap layer.

Protocol posture: unregistered synthetic experiment, fixed generators/controls,
no sealed holdout, no efficacy/generalization claim. Runtime and source digests
are retained; exact timings vary between runs. Default tests are offline and
standard-library-only.
