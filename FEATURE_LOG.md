# Codito #71 cheap-first preflight

Issue: https://github.com/Entif-AI/Codito/issues/71
Base: 46a1ae8afa857d1942e77361acb9d08feb58563d
Publication posture: public authored research payloads and conventional deterministic probes.
No production routing thresholds, provider calls, source repair or Rosetta schema.
Native lease/finalization tooling is absent. One writer uses Git/remote readback.

Acceptance proof: JSON, malformed JSON-like, code, browser, MCP/AXI and chronology
fixtures; raw, structural, path and heuristic controls; source byte spans/digests;
recall/false exclusions, abstention, two boundary placements, actual preflight time
and packet bytes; explicit VOI and optional bounded scorer; retained negative case.
Current focus: red behavioral tests. Next safe step: implement offline demonstrator.

Result: 69 offline unittest cases pass. Red missing implementation, transport
boundary and lost-decorator cases preceded their fixes. Seventy fixture/treatment
placements retain packet/source bytes, source/transport digests, recall, exclusions
and actual instrumentation-inclusive nanoseconds. Negative tiny/prefix controls
and opaque malformed excerpts survive. Provider/model calls are zero.
Next safe step: review PR, exact log archive, remote final readback; no merge.
