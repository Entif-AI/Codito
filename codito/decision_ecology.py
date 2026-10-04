"""Finite #70 experiment. Toy mathematics and attributed fixture judgments only."""

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def validate(fixture):
    weights = fixture["profile"].get("weights")
    criteria = fixture["profile"]["criteria"]
    if not isinstance(weights, dict) or set(weights) != set(criteria):
        raise ValueError("an explicit complete decision weight profile is required")
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or v < 0
           for v in weights.values()) or not math.isclose(sum(weights.values()), 1):
        raise ValueError("weights must be finite, nonnegative and sum to one")
    if set(fixture["dossiers"]) != set("ABCDE") or any(len(v) != 4 for v in fixture["dossiers"].values()):
        raise ValueError("five approved four-unit dossiers are required")
    options = fixture["candidates"]
    ids = {c["id"] for c in options}
    if len(ids) != len(options) or ids != set(fixture["truth"]):
        raise ValueError("unique candidates must have separate terminal outcome fixtures")
    if type(fixture["budget"]) is not int or fixture["budget"] <= 0:
        raise ValueError("budget must be a positive integer")
    for option in options:
        if type(option["cost"]) is not int or option["cost"] <= 0:
            raise ValueError("candidate costs must be positive integers")
        if not set(option["depends"]).issubset(ids) or option["id"] in option["depends"]:
            raise ValueError("invalid declared dependency")
    fact_ids = set()
    for project, facts in fixture["dossiers"].items():
        for fact in facts:
            if fact["id"] in fact_ids or fact["project"] != project or not fact["approved"]:
                raise ValueError("dossier facts require unique identity and approved local ownership")
            fact_ids.add(fact["id"])
            for candidate, scores in fact["scores"].items():
                if candidate not in ids or set(scores) != set(criteria):
                    raise ValueError("judgment criteria/candidate mismatch")
                if any(not math.isfinite(v) for v in scores.values()):
                    raise ValueError("nonfinite judgment")
    return fixture


def sample_context(fixture, aperture, seed):
    validate(fixture)
    if aperture not in (0, .25, .5, 1):
        raise ValueError("aperture must be a preregistered treatment")
    contexts = {}
    for project in sorted(fixture["dossiers"]):
        facts = list(fixture["dossiers"][project])
        for peer in sorted(fixture["dossiers"]):
            if peer != project:
                rng = random.Random(f"{seed}:{project}:{peer}")
                facts.extend(rng.sample(fixture["dossiers"][peer], int(4 * aperture)))
        contexts[project] = sorted(facts, key=lambda f: f["id"])
    return contexts


def rank(vectors, weights):
    if not weights or any(not math.isfinite(v) or v < 0 for v in weights.values()):
        raise ValueError("invalid explicit weights")
    scores = {key: sum(vector[c] * w for c, w in weights.items()) for key, vector in vectors.items()}
    if any(not math.isfinite(v) for v in scores.values()):
        raise ValueError("nonfinite rank")
    return sorted(scores, key=lambda key: (-scores[key], key))


def pareto(vectors):
    """Maximize each declared criterion; ties remain distinct candidates."""
    return {a for a, av in vectors.items() if not any(
        all(bv[k] >= av[k] for k in av) and any(bv[k] > av[k] for k in av)
        for b, bv in vectors.items() if b != a)}


def select(ranking, candidates, budget, known_dependencies=None):
    """Identical legal budget/dependency/conflict controller for every strategy."""
    options = {c["id"]: c for c in candidates}
    if len(ranking) != len(set(ranking)) or not set(ranking).issubset(options):
        raise ValueError("ranking must name unique offered candidates")
    dependencies = {c["id"]: set(c["depends"]) for c in candidates}
    for key, deps in (known_dependencies or {}).items():
        dependencies[key].update(deps)
    selected, groups, remaining = [], set(), budget
    while True:
        before = len(selected)
        for key in ranking:
            option = options[key]
            group = option.get("exclusive_group") or option.get("duplicate_group")
            if (key not in selected and option["cost"] <= remaining
                    and dependencies[key].issubset(selected) and (not group or group not in groups)):
                selected.append(key)
                remaining -= option["cost"]
                if group:
                    groups.add(group)
        if len(selected) == before:
            return selected


def evaluate(selected, fixture):
    options = {c["id"]: c for c in fixture["candidates"]}
    completed, attempts = set(), []
    quality = spent = rework = 0
    for key in selected:
        truth = fixture["truth"][key]
        spent += options[key]["cost"]
        success = set(truth["requires"]).issubset(completed)
        if success:
            completed.add(key)
            quality += truth["quality"]
        else:
            rework += options[key]["cost"]
        attempts.append({"candidate": key, "state": "completed" if success else "failed-prerequisite",
                         "quality": truth["quality"] if success else 0,
                         "source_ref": truth["source_ref"]})
    return {"spent": spent, "quality": quality, "attempts": attempts,
            "shared_dependency_unlocks": sum(k in completed and options[k]["category"] == "shared"
                                             for k in options),
            "downstream_rework_proxy": rework,
            "duplicate_proposals_avoided_proxy": sum(
                bool(c.get("duplicate_group")) and any(options[k].get("duplicate_group") == c["duplicate_group"]
                                                 for k in completed) and c["id"] not in completed
                for c in options.values()),
            "terminal_success": len(completed) == len(selected) and bool(selected)}


def _judgments(contexts, fixture, aperture):
    criteria = fixture["profile"]["criteria"]
    judgments = {}
    for project, facts in contexts.items():
        vectors = {c["id"]: dict.fromkeys(criteria, 0.0) for c in fixture["candidates"]}
        for fact in facts:
            for candidate, values in fact["scores"].items():
                for criterion, value in values.items():
                    vectors[candidate][criterion] += value
        judgments[project] = {"vectors": vectors, "evidence_refs": [f["id"] for f in facts],
                              "state": "attributed-complete" if aperture == 1 else "bounded-missing-evidence",
                              "missing_peer_units": 16 - int(16 * aperture),
                              "unknown_treatment": "zero contribution is an experimental lower-bound imputation"}
    return judgments


def _aggregate(judgments, candidates, criteria):
    return {c: {k: sum(j["vectors"][c][k] for j in judgments.values()) / len(judgments)
                for k in criteria} for c in candidates}


def _oracle(fixture):
    candidates = fixture["candidates"]
    best = 0
    for mask in range(1 << len(candidates)):
        subset = [c for i, c in enumerate(candidates) if mask & (1 << i)]
        if sum(c["cost"] for c in subset) > fixture["budget"]:
            continue
        deps = {c["id"]: fixture["truth"][c["id"]]["requires"] for c in candidates}
        chosen = select([c["id"] for c in subset], candidates, fixture["budget"], deps)
        best = max(best, evaluate(chosen, fixture)["quality"])
    return best


def run_study(fixture, seeds=(3, 11, 29)):
    started = time.perf_counter_ns()
    validate(fixture)
    options = fixture["candidates"]
    ids = [c["id"] for c in options]
    criteria, weights = fixture["profile"]["criteria"], fixture["profile"]["weights"]
    grid_digest, profile_digest = digest(options), digest(fixture["profile"])
    oracle = _oracle(fixture)
    full = _judgments(sample_context(fixture, 1, 0), fixture, 1)
    full_rank = rank(_aggregate(full, ids, criteria), weights)
    runs = []
    for seed in seeds:
        controls = [("random", 0, "weighted"), ("prerequisite", 0, "weighted"), ("local-A", 0, "weighted")]
        panels = [("panel", a, m) for a in (0, .25, .5, 1) for m in ("weighted", "pareto")]
        for strategy, aperture, method in [*controls, *panels]:
            contexts = sample_context(fixture, aperture, seed)
            if strategy == "local-A":
                contexts = {"A": contexts["A"]}
            if strategy in {"random", "prerequisite"}:
                contexts = {}
            judgments = _judgments(contexts, fixture, aperture)
            vectors = _aggregate(judgments, ids, criteria) if judgments else {}
            if strategy == "random":
                ranking = list(ids)
                random.Random(seed).shuffle(ranking)
            elif strategy == "prerequisite":
                ranking = [c["id"] for c in sorted(options, key=lambda c: (len(c["depends"]), c["id"]))]
            else:
                ranking = rank(vectors, weights)
                if method == "pareto":
                    nondominated = pareto(vectors)
                    ranking = [key for key in ranking if key in nondominated]
            known = {}
            for facts in contexts.values():
                for fact in facts:
                    for key, deps in fact.get("dependencies", {}).items():
                        known.setdefault(key, set()).update(deps)
            selected = select(ranking, options, fixture["budget"], known)
            # Independent truth is consulted only after selection and for diagnostic controls.
            outcome = evaluate(selected, fixture)
            refs = {p: [f["id"] for f in facts] for p, facts in contexts.items()}
            decision_id = digest([strategy, aperture, method, seed, refs, grid_digest, profile_digest, ranking, selected])
            outcome["decision_id"] = decision_id
            comparison = ranking + [key for key in full_rank if key not in ranking]
            positions = {key: i for i, key in enumerate(full_rank)}
            disagreements = sum(positions[a] > positions[b] for a, b in itertools.combinations(comparison, 2))
            total_pairs = max(1, len(ids) * (len(ids) - 1) // 2)
            weighted_votes = {p: {c: sum(j["vectors"][c][k] * weights[k] for k in criteria)
                                  for c in ids} for p, j in judgments.items()}
            review = sum(max(v[c] for v in weighted_votes.values()) - min(v[c] for v in weighted_votes.values())
                         > fixture["profile"]["dissent_gap"] for c in ids) if weighted_votes else 0
            myopia = sum(abs(j["vectors"][c][k] - full[p]["vectors"][c][k])
                         for p, j in judgments.items() for c in ids for k in criteria)
            runs.append({"decision_id": decision_id, "strategy": strategy, "aperture": aperture,
                         "aggregator": method, "seed": seed, "candidate_grid_digest": grid_digest,
                         "profile_digest": profile_digest, "context_refs": refs, "judgments": judgments,
                         "ranking": ranking, "selected": selected, "outcome": outcome,
                         "rejected_alternatives": [c for c in ids if c not in selected],
                         "regret_proxy": oracle - outcome["quality"], "myopia_proxy": myopia,
                         "pairwise_rank_disagreement": disagreements / total_pairs,
                         "review_items_proxy": review,
                         "context_bytes": sum(len(json.dumps(facts, sort_keys=True).encode()) for facts in contexts.values()),
                         "tokens": None, "model_calls": 0})
    sensitivity = []
    for aperture in (0, .25, .5, 1):
        for method in ("weighted", "pareto"):
            treatment = [r for r in runs if r["strategy"] == "panel" and r["aperture"] == aperture
                         and r["aggregator"] == method]
            if treatment:
                sensitivity.append({"aperture": aperture, "aggregator": method,
                                    "unique_rankings": len({tuple(r["ranking"]) for r in treatment}),
                                    "quality_min": min(r["outcome"]["quality"] for r in treatment),
                                    "quality_max": max(r["outcome"]["quality"] for r in treatment)})
    return {"format_version": 1, "role": "synthetic-research-only", "fixture_digest": digest(fixture),
            "candidate_grid_digest": grid_digest, "oracle_quality_proxy": oracle, "runs": runs,
            "seed_sensitivity": sensitivity,
            "strong_model_comparator": {"status": "not-run", "reason": "no qualified live provider in this fixture"},
            "metrics_basis": "authored toy outcome units; measured UTF-8 bytes; review/rework/regret/myopia are proxies",
            "elapsed_ns": time.perf_counter_ns() - started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_study(json.loads(args.fixture.read_text())), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
