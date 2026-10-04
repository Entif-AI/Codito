# Doctrine: domain, type, boundary, and state discipline

Apply foundational-thinking, model-the-domain, type-system-discipline, boundary-discipline, separate-before-serializing-shared-state, and make-operations-idempotent as constraints, not peer workflows.

- Choose core state/data structures before downstream logic.
- Encode domain states and invariants explicitly.
- Make illegal states difficult or impossible to represent.
- Parse/validate external data at real boundaries; trust typed internals.
- Remove avoidable shared mutable state before adding synchronization.
- Design retries/restarts to converge under explicit idempotency contracts.
