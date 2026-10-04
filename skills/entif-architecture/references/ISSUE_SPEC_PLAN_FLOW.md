# Issue -> Spec -> Plan -> Execution

```text
idea/request/issue
 -> authority + publication preflight
 -> durable problem framing
 -> change posture
 -> durable issue decomposition only where needed
 -> Spec Impact Gate
 -> accepted desired-state spec unless RESEARCH/no normative change
 -> temporal plan DAG
 -> readiness/legal next work
 -> execution
 -> verify against spec
 -> close/freeze plan + preserve Git/PR evidence
```

Change posture: `NORMATIVE|CONFORMANCE|RESEARCH|MAINTENANCE`.

Spec Impact Gate: `COVERED|AMEND|CREATE|NO_NORMATIVE_CHANGE|BLOCKED_SPEC_AUTHORITY`.

Issues say why durable work exists and who owns it. Specs say what must remain true. Plans say temporal motion. Execution readiness comes from plan/runtime state, not issue prose.
