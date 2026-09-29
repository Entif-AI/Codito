"""Small executable UCA candidate contracts; not a Rosetta implementation.

No credentials, provider calls, model calls, or real effects. The harness tests
state distinctions proposed in ETR-2026-12, not expected production performance.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from math import isfinite
from typing import FrozenSet, Mapping, Sequence


class Facet(str, Enum):
    VALUE = "value"
    EVIDENCE = "evidence"
    ADMISSION = "admission"


@dataclass(frozen=True)
class Materialization:
    value_digest: str
    evidence_digest: str
    admission_digest: str


def changed_facets(old: Materialization, new: Materialization) -> FrozenSet[Facet]:
    fields = ((Facet.VALUE, "value_digest"), (Facet.EVIDENCE, "evidence_digest"),
              (Facet.ADMISSION, "admission_digest"))
    return frozenset(facet for facet, field in fields if getattr(old, field) != getattr(new, field))


def affected(changes: FrozenSet[Facet], dependency_facets: FrozenSet[Facet]) -> bool:
    """A consumer explicitly declares the state facets on which it depends."""
    return bool(changes & dependency_facets)


def parse_instant(value: str) -> datetime:
    instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if instant.tzinfo is None:
        raise ValueError("Time basis must include an offset")
    return instant.astimezone(timezone.utc)


@dataclass(frozen=True)
class AdmissionContext:
    principal: str
    entitlement: str
    policy: str
    source_bundle: str
    source_version: str
    now: str
    expires_at: str
    revoked: bool = False


def may_serve(entry: Mapping[str, str], context: AdmissionContext | None) -> tuple[bool, str]:
    if context is None:
        return False, "MISSING_CONTEXT"
    required = ("principal", "entitlement", "policy", "source_bundle", "source_version")
    if any(not getattr(context, field) or field not in entry for field in required):
        return False, "MISSING_BINDING"
    try:
        now, expiry = parse_instant(context.now), parse_instant(context.expires_at)
    except (ValueError, TypeError):
        return False, "INVALID_TIME"
    if now >= expiry:
        return False, "EXPIRED"
    if context.revoked:
        return False, "REVOKED"
    for field in required:
        if entry[field] != getattr(context, field):
            return False, "BINDING_MISMATCH:" + field
    return True, "ELIGIBLE"


class EffectState(str, Enum):
    PROPOSED = "proposed"
    AUTHORIZED = "authorized"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    OBSERVED = "observed"
    AMBIGUOUS = "ambiguous"


TRANSITIONS = {
    EffectState.PROPOSED: {EffectState.AUTHORIZED},
    EffectState.AUTHORIZED: {EffectState.SUBMITTED},
    EffectState.SUBMITTED: {EffectState.ACKNOWLEDGED, EffectState.AMBIGUOUS},
    EffectState.ACKNOWLEDGED: {EffectState.OBSERVED, EffectState.AMBIGUOUS},
    EffectState.AMBIGUOUS: {EffectState.ACKNOWLEDGED, EffectState.OBSERVED},
    EffectState.OBSERVED: set(),
}


def transition(current: EffectState, following: EffectState, evidence_ref: str) -> EffectState:
    if not evidence_ref or following not in TRANSITIONS[current]:
        raise ValueError("Transition requires evidence and a permitted predecessor")
    return following


def may_replay(state: EffectState, idempotent: bool, reconciled_absent: bool) -> bool:
    """Replay policy is a candidate adapter rule, not universal exactly-once IO."""
    if state == EffectState.OBSERVED:
        return False
    return state in {EffectState.PROPOSED, EffectState.AUTHORIZED} or idempotent or reconciled_absent


def inheritance_losses(required: FrozenSet[str], preserved: FrozenSet[str]) -> FrozenSet[str]:
    return required - preserved


def independent_roots(lineages: Sequence[FrozenSet[str]]) -> FrozenSet[str]:
    """Only known roots count; an empty set remains unknown, not independent."""
    return frozenset().union(*lineages)


def transport_cost(model: float, updates: float, residuals: float, witnesses: float,
                   refresh: float, reuse_count: int = 1) -> float:
    terms = (model, updates, residuals, witnesses, refresh)
    if reuse_count < 1 or any(not isfinite(x) or x < 0 for x in terms):
        raise ValueError("Cost terms must be finite and nonnegative; reuse count positive")
    return model / reuse_count + updates + residuals + witnesses + refresh


def collection_complete(truncated: bool, next_page_token: str | None, all_pages_observed: bool) -> bool:
    return not truncated and not next_page_token and all_pages_observed


def advance_correction(current_epoch: int, next_epoch: int, expected: FrozenSet[str],
                       acknowledged: FrozenSet[str]) -> int:
    if next_epoch <= current_epoch or not expected.issubset(acknowledged):
        raise ValueError("Correction completion requires monotone epoch and complete declared scope")
    return next_epoch