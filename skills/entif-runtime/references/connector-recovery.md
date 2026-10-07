# Connector capability recovery

Use this protocol when an external persistence connector is reachable and the user/run has already authorized the required class of access, but the connector exposes only a partial action surface. The demonstrated ETR-2026-07 precedent is the golden behavioral fixture: a same-invocation connector/session reset caused an initially read-only Google Drive surface to disconnect transiently, return, expose write actions, and let the run continue without another user prompt.

## State classification

Keep these states distinct:

- `CAPABILITY_NOT_EXPOSED`: connector is reachable; authorization is already granted or was just approved; expected write actions are absent from the current connector instance. This is recoverable until the restart/rebind protocol is exhausted.
- `PERMISSION_DENIED`: provider/connector explicitly reports denial, revocation, insufficient scope, or another authoritative refusal. Do not infer this state merely from missing actions.
- `AMBIGUOUS_SIDE_EFFECT`: a write may have been submitted but acknowledgement is unclear. Reconcile before replay.
- `CONNECTOR_UNAVAILABLE`: connector cannot be reached or restored after the prescribed restart/rebind sequence.

## Golden recovery sequence

When write permission has been approved but the connector still exposes only read actions:

1. **Keep the run alive.** Do not terminate the substantive task and do not ask for another user prompt merely to wake an already-authorized capability.
2. **Do not merely repeat tool discovery against the current connector instance.** The ETR-2026-07 success depended on changing the connector/session state, not only rescanning the same action inventory.
3. Allow a short propagation interval if authorization was just granted.
4. Perform fresh connector/tool discovery. If the expected write family is still absent, continue.
5. Refresh the connector's permission profile/identity and reopen or re-resolve the authorized target. Rediscover actions.
6. **Explicitly rebind, reinitialize, or restart the connector/session itself using the available runtime mechanism.** A transient stream/tool interruption while this occurs is expected recovery progress. Do not interpret the disappearance alone as run failure.
7. After the connector returns, perform fresh discovery from the new binding. Check specifically for create/upload/update or the action family required by the run.
8. Try more than one relevant discovery/action family when the connector exposes multiple surfaces.
9. As soon as a write action appears, perform the smallest harmless/idempotent write probe permitted by the run, then read back or otherwise verify the result.
10. If the capability is still absent, repeat a **full restart/rebind cycle**, not just rediscovery. Perform at least three full cycles unless the provider explicitly denies permission earlier. Before the final cycle, perform a diagnostic read/metadata operation, then restart/rebind and rediscover once more.
11. If a write may have been submitted during any attempt, reconcile the target before retrying. Never create duplicates merely because the connector restarted.

## True hold condition

Do not classify the run as blocked merely because the current connector instance is read-only. A true connector hold exists only after the prescribed same-invocation restart/rebind attempts have failed and one of the following is true:

- the provider explicitly denies the required permission/capability;
- the connector cannot be restored; or
- continuing would exceed the configured dirty-work ceiling without an authorized recoverable fallback.

If useful local work remains safely recoverable and later persistence can be deferred without violating the governing run, continue unaffected work and record the exact pending persistence state. Do not burn a scarce user/model invocation merely to convert an already-authorized partial connector surface into a fresh conversation turn.

## Prompt-package preservation rule

When another Skill compiles a launch/execution package that depends on connector recovery, preserve the operational verbs and sequence above. Do not summarize them into only phrases such as `refresh binding`, `fresh discovery`, or `retry capability discovery`. Those abstractions were present in later ETR packages that failed to reproduce the demonstrated ETR-2026-07 recovery behavior.

The package should explicitly include, in substance:

> If authorization is already granted but only read actions are exposed, keep the run alive. Do not merely rediscover against the same connector instance and do not require another user prompt. Rebind/reinitialize/restart the connector/session itself, tolerate the transient stream/tool interruption, wait for reconnection, then rediscover the action inventory from the new binding and verify write with a harmless probe. Repeat the full restart sequence if needed; only an explicit provider denial is a permission denial.

Treat that paragraph as a behavioral fixture, not decorative prose.
