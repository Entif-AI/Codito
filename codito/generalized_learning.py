"""Finite #69 generalization fixtures. No swarm, official schema or privacy proof."""

import dataclasses
import hashlib
import json
import time

RULES = {"verify-snapshot", "require-reminder-confirmation", "discard-third-party-retail", "verify-tool-postcondition"}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


@dataclasses.dataclass(frozen=True)
class Episode:
    local_id: str
    raw: bytes
    family: str
    rule_ref: str
    version: str
    scope: str
    purpose: str
    evidence_root: str
    consent: bool = True
    rights: bool = True
    sensitive: bool = False
    third_party: bool = False
    locally_validated: bool = True


@dataclasses.dataclass(frozen=True)
class Lesson:
    id: str
    rule_ref: str
    version: str
    scope: str
    purpose: str
    roots: tuple
    epoch: int = 0
    previous: str = None
    status: str = "active"
    counterexamples: tuple = ()


def _make(**fields):
    fields = dict(epoch=0, previous=None, status="active", counterexamples=(), **fields)
    return Lesson(id=_digest(fields), **fields)


def _verify(lesson):
    fields = dataclasses.asdict(lesson)
    fields.pop("id")
    if (lesson.id != _digest(fields) or lesson.rule_ref not in RULES
            or type(lesson.epoch) is not int or lesson.epoch < 0
            or not all((lesson.version, lesson.scope, lesson.purpose))
            or lesson.status not in {"active", "revoked"}):
        raise ValueError("lesson identity or finite fixture contract mismatch")


def export_candidate(episodes, profile):
    """Consume supplied fixture gates; never infer permission from recurrence."""
    minimum = profile.get("minimum_independent_roots")
    if type(minimum) is not int or minimum < 1 or not profile.get("purpose"):
        raise ValueError("an explicit experimental support/purpose profile is required")
    eligible, rejected = [], []
    for episode in episodes:
        reasons = []
        for field, required in (("consent", True), ("rights", True), ("sensitive", False),
                                ("third_party", False), ("locally_validated", True)):
            if getattr(episode, field) is not required:
                reasons.append(field)
        if episode.purpose != profile["purpose"]:
            reasons.append("purpose-mismatch")
        if episode.rule_ref not in RULES:
            reasons.append("unapproved-generalized-vocabulary")
        if reasons:
            rejected.append({"evidence_root": episode.evidence_root, "reasons": reasons})
        else:
            eligible.append(episode)
    roots = tuple(sorted({e.evidence_root for e in eligible}))
    signatures = {(e.rule_ref, e.version, e.scope, e.purpose) for e in eligible}
    dissent = [{"root": e.evidence_root, "rule_ref": e.rule_ref, "version": e.version} for e in eligible]
    if len(signatures) > 1:
        return {"state": "conflicting-evidence", "lesson": None, "independent_roots": len(roots),
                "dissent": dissent, "rejected": rejected}
    if len(roots) < minimum or not eligible:
        return {"state": "no-export", "lesson": None, "independent_roots": len(roots),
                "dissent": [], "rejected": rejected}
    episode = eligible[0]
    lesson = _make(rule_ref=episode.rule_ref, version=episode.version, scope=episode.scope,
                   purpose=episode.purpose, roots=roots)
    return {"state": "exported", "lesson": lesson, "independent_roots": len(roots),
            "dissent": [], "rejected": rejected}


def correct(lesson, challenge_ref):
    _verify(lesson)
    if not isinstance(challenge_ref, str) or not challenge_ref.startswith("challenge:"):
        raise ValueError("a non-reconstructive challenge reference is required")
    fields = dataclasses.asdict(lesson)
    fields.pop("id")
    fields.update(epoch=lesson.epoch + 1, previous=lesson.id, status="revoked",
                  counterexamples=tuple(lesson.counterexamples) + (challenge_ref,))
    return Lesson(id=_digest(fields), **fields)


class Recipient:
    """Local finite validator/cache; no signature or remote authority service."""

    def __init__(self, version, scope, purpose, validation, minimum_independent_roots=2):
        self.version, self.scope, self.purpose = version, scope, purpose
        self.validation, self.minimum = validation, minimum_independent_roots
        self.accepted, self.superseded = {}, set()

    def adopt(self, lesson):
        _verify(lesson)
        if lesson.id in self.superseded:
            state = "rejected-superseded"
        elif lesson.status != "active":
            state = "rejected-revoked"
        elif (lesson.version, lesson.scope, lesson.purpose) != (self.version, self.scope, self.purpose):
            state = "rejected-scope-version-purpose"
        elif len(set(lesson.roots)) < self.minimum:
            state = "rejected-independent-support"
        else:
            response = self.validation.get(lesson.rule_ref)
            state = ("accepted-local" if response is True else "rejected-local-test" if response is False
                     else "conflicting-evidence" if response == "conflict" else "insufficient-evidence")
        if state == "accepted-local":
            self.accepted[lesson.id] = lesson
        return {"state": state, "lesson_ref": lesson.id, "execution_authorized": False}

    def receive(self, correction):
        _verify(correction)
        if not correction.previous or correction.status != "revoked":
            raise ValueError("a bounded superseding correction is required")
        self.superseded.add(correction.previous)
        self.accepted.pop(correction.previous, None)
        return {"state": "correction-retained", "previous": correction.previous,
                "correction_ref": correction.id, "execution_authorized": False}


def fixtures():
    families = (("computer-use", "verify-snapshot"), ("personal-assistance", "require-reminder-confirmation"),
                ("retail", "discard-third-party-retail"), ("engineering", "verify-tool-postcondition"))
    cases = []
    for family, rule in families:
        episodes = tuple(Episode(local_id=f"local-only:{family}:{i}", raw=f"SYNTHETIC-PRIVATE-MARKER:{family}:{i}".encode(),
                                 family=family, rule_ref=rule, version="fixture-v1", scope=family,
                                 purpose="bounded-learning", evidence_root=f"opaque-root:{family}:{i}",
                                 sensitive=family == "retail", third_party=family == "retail") for i in (1, 2))
        states = {"computer-use": {"snapshot_current": False},
                  "personal-assistance": {"confirmed": False}, "retail": {"third_party": True},
                  "engineering": {"tool_postcondition_observed": False}}
        expected = {"computer-use": "inspect_more", "personal-assistance": "review",
                    "retail": "discard", "engineering": "inspect_more"}
        cases.append({"family": family, "episodes": episodes,
                      "profile": {"purpose": "bounded-learning", "minimum_independent_roots": 2,
                                  "posture": "explicit toy support criterion, no anonymity or production privacy threshold"},
                      "recipient": {"version": "fixture-v1", "scope": family, "purpose": "bounded-learning",
                                    "validation": {rule: True}},
                      "local_only_has_rule": family == "engineering",
                      "terminal_state": states[family], "expected_suggestion": expected[family]})
    return cases


def _fixture_suggestion(rule, state):
    # Conventional finite rule library supplies competence. No inferred model policy.
    if rule == "verify-snapshot":
        return "ready" if state.get("snapshot_current") else "inspect_more"
    if rule == "require-reminder-confirmation":
        return "candidate" if state.get("confirmed") else "review"
    if rule == "discard-third-party-retail":
        return "discard" if state.get("third_party") else "aggregate-candidate"
    if rule == "verify-tool-postcondition":
        return "ready" if state.get("tool_postcondition_observed") else "inspect_more"
    return None


def run_study(cases=None):
    cases, runs = fixtures() if cases is None else cases, []
    for case in cases:
        for strategy in ("local-only", "naive", "rights-safe", "correlated-copies", "stale-version", "poisoned"):
            started = time.perf_counter_ns()
            episodes = case["episodes"]
            if strategy == "correlated-copies":
                episodes = (episodes[0], dataclasses.replace(episodes[1], evidence_root=episodes[0].evidence_root))
            elif strategy == "poisoned":
                episodes = (episodes[0], dataclasses.replace(episodes[1], locally_validated=False))
            recipient_args = dict(case["recipient"])
            if strategy == "stale-version":
                recipient_args["version"] = "fixture-v2"
            recipient = Recipient(**recipient_args)
            local_validation = {"state": "no-shared-lesson", "execution_authorized": False}
            exported, correction, gate = None, None, None
            lesson = None
            if strategy == "local-only":
                export_state = "local-only"
            elif strategy == "naive":
                # Deliberately unsafe synthetic baseline: purported abstraction retains local detail.
                exported = {"rule_ref": episodes[0].rule_ref, "unscoped_summary": episodes[0].raw.decode(),
                            "evidence": "unverified", "version": "unspecified"}
                export_state = "naive-export"
                local_validation = {"state": "naive-unvalidated-transfer", "execution_authorized": False}
            else:
                gate = export_candidate(episodes, case["profile"])
                lesson, export_state = gate["lesson"], gate["state"]
                if lesson:
                    exported = dataclasses.asdict(lesson)
                    local_validation = recipient.adopt(lesson)
            encoded = json.dumps(exported, sort_keys=True).encode() if exported is not None else b""
            exposure = sum(e.raw in encoded for e in episodes)
            accepted = local_validation["state"] == "accepted-local"
            has_local_rule = strategy == "local-only" and case["local_only_has_rule"]
            suggestion = _fixture_suggestion(episodes[0].rule_ref, case["terminal_state"]) if (
                accepted or has_local_rule or strategy == "naive") else None
            expected = case.get("expected_suggestion")
            terminal = ("not-run" if suggestion is None else "not-observed" if expected is None
                        else "correct" if suggestion == expected else "wrong")
            decision_integrity = False if strategy == "naive" else True if accepted or has_local_rule else None
            utility = int(terminal == "correct")
            harm = int(exposure > 0 or (strategy == "naive" and case["family"] == "retail"))
            rejection = int(exported is not None and not accepted and strategy != "naive")
            correction_received = False
            if lesson and accepted:
                correction = correct(lesson, "challenge:authored-later-counterexample")
                recipient.receive(correction)
                correction_received = recipient.adopt(lesson)["state"] == "rejected-superseded"
            correction_bytes = len(json.dumps(dataclasses.asdict(correction), sort_keys=True).encode()) if correction else 0
            runs.append({"family": case["family"], "strategy": strategy,
                         "local_raw_refs": [e.local_id for e in episodes],
                         "local_interpretations": [{"rule_ref": e.rule_ref, "locally_validated": e.locally_validated}
                                                   for e in episodes],
                         "candidate_rule": episodes[0].rule_ref, "privacy_gate": {
                             "state": gate["state"], "rejected": gate["rejected"], "dissent": gate["dissent"]}
                             if gate else {"state": "not-applied" if strategy == "naive" else "local-only"},
                         "export_state": export_state, "exported_lesson": exported,
                         "local_validation": local_validation, "utility_proxy": utility, "harm_proxy": harm,
                         "decision_integrity": decision_integrity,
                         "terminal_outcome": {"state": terminal, "suggestion": suggestion, "expected": expected,
                                              "execution_authorized": False},
                         "joint_correctness": decision_integrity is True and terminal == "correct",
                         "raw_marker_exposure_proxy": exposure,
                         "independent_evidence_diversity": gate["independent_roots"] if gate else 0,
                         "local_rejection": rejection, "correction_propagated": correction_received,
                         "correction": dataclasses.asdict(correction) if correction else None,
                         "serialized_export_bytes": len(encoded), "serialized_correction_bytes": correction_bytes,
                         "network_bytes": 0, "model_calls": 0, "local_compute_ns": time.perf_counter_ns() - started})
    return {"format_version": 1, "role": "synthetic-research-only", "families": [c["family"] for c in cases],
            "runs": runs, "privacy_guarantee": None,
            "metric_basis": "authored local validation/utility and marker-exposure proxies; measured serialized bytes/local CPU time; no network, DP or trust proof",
            "production_federation": "not-implemented; Rosetta #84/#96/#759 remain controlling gates"}


if __name__ == "__main__":
    print(json.dumps(run_study(), indent=2))
