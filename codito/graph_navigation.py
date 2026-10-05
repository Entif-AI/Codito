"""Finite #72 navigation research. Graph facts, heat and witnesses stay separate."""

import dataclasses
import hashlib
import json
import math
import random
import time


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


@dataclasses.dataclass(frozen=True)
class Node:
    id: str
    label: str
    text: str
    evidence_root: str
    allowed: bool = True


@dataclasses.dataclass(frozen=True)
class Graph:
    family: str
    nodes: tuple
    edges: tuple

    def __post_init__(self):
        ids = {n.id for n in self.nodes}
        if len(ids) != len(self.nodes) or any(a not in ids or b not in ids for a, b, _ in self.edges):
            raise ValueError("graph identity or edge endpoint mismatch")
        if any(kind not in {"source-fact", "derived-ast", "inferred"} for _, _, kind in self.edges):
            raise ValueError("edge provenance class must be explicit")

    @property
    def digest(self):
        return _digest(dataclasses.asdict(self))

    def neighbors(self, node):
        return [b for a, b, _ in self.edges if a == node]


@dataclasses.dataclass(frozen=True)
class Visit:
    node: str
    task: str
    at: float
    success: bool
    evidence_root: str
    graph_version: str


@dataclasses.dataclass(frozen=True)
class Heat:
    visits: tuple

    def score(self, node, task, now, mode, graph_version, half_life):
        if not math.isfinite(half_life) or half_life <= 0 or not math.isfinite(now):
            raise ValueError("finite time and positive explicit half-life required")
        events = [e for e in self.visits if e.node == node]
        if any(not math.isfinite(e.at) or e.at > now for e in events):
            raise ValueError("navigation telemetry has invalid/future time")
        if mode == "frequency":
            return len(events)
        if mode == "recency":
            return max((1 / (1 + now - e.at) for e in events), default=0)
        if mode != "decayed-task":
            raise ValueError("unknown heat treatment")
        roots = {}
        for event in events:
            if event.task == task and event.graph_version == graph_version and event.success:
                roots[event.evidence_root] = max(event.at, roots.get(event.evidence_root, event.at))
        return sum(2 ** (-(now - at) / half_life) for at in roots.values())


def recruit(reports):
    """Scouts remain attributable; copied source reports do not add witnesses."""
    nodes = {}
    for report in reports:
        node = nodes.setdefault(report["node"], {"scouts": set(), "roots": set(), "claimed_useful": False})
        node["scouts"].add(report["scout"])
        node["roots"].add(report["evidence_root"])
        node["claimed_useful"] |= report["claimed_useful"]
    ranking = sorted([n for n, v in nodes.items() if v["claimed_useful"]],
                     key=lambda n: (-len(nodes[n]["roots"]), n))
    return {"ranking": ranking, "scout_count": len({r["scout"] for r in reports}),
            "independent_roots": len({r["evidence_root"] for r in reports}),
            "source_roots_by_node": {n: sorted(v["roots"]) for n, v in sorted(nodes.items())},
            "posture": "attributed hints, no truth or execution authority"}


def navigate(case, strategy, seed, budget=4, exploration=.2, half_life=3):
    started = time.perf_counter_ns()
    if strategy not in {"random", "dependency", "lexical", "recency", "frequency", "decayed-task", "scout"}:
        raise ValueError("unknown navigation strategy")
    if type(budget) is not int or budget < 0 or not 0 <= exploration <= 1:
        raise ValueError("invalid explicit inspection budget/exploration")
    graph, heat = case["graph"], case["heat"]
    # Every strategy sees only the legal source-derived candidate set, before heat/ranking.
    legal = {n.id: n for n in graph.nodes if n.allowed}
    required = set(case["targets"])
    if not required.issubset(legal):
        raise ValueError("fixture target is outside the admitted graph")
    rng = random.Random(seed)
    shuffled = sorted(legal)
    rng.shuffle(shuffled)
    trace, reports, recruitment = [], [], None
    edges_inspected = 0
    index_bytes = sum(len(n.label.encode()) for n in legal.values()) if strategy == "lexical" else 0
    telemetry_bytes = len(json.dumps([dataclasses.asdict(e) for e in heat.visits]).encode()) if strategy in {
        "recency", "frequency", "decayed-task"} else 0
    dependency_order = []
    if strategy == "dependency":
        queue = [case["start"]]
        while queue:
            node = queue.pop(0)
            if node in legal and node not in dependency_order:
                dependency_order.append(node)
                neighbors = graph.neighbors(node)
                edges_inspected += len(neighbors)
                queue.extend(n for n in neighbors if n in legal)
        dependency_order.extend(n for n in sorted(legal) if n not in dependency_order)
    while len(trace) < budget and not required.issubset(trace):
        remaining = [n for n in shuffled if n not in trace]
        if not remaining:
            break
        if strategy == "random":
            chosen = remaining[0]
        elif strategy == "dependency":
            chosen = next(n for n in dependency_order if n not in trace)
        elif strategy == "lexical":
            chosen = min(remaining, key=lambda n: (-int(case["query"].casefold() in legal[n].label.casefold()), n))
        elif strategy == "scout":
            if len(trace) < min(3, budget):
                chosen = remaining[0]
            else:
                recruitment = recruit(reports)
                followers = [n for leader in recruitment["ranking"] for n in graph.neighbors(leader)
                             if n in remaining]
                edges_inspected += len(followers)
                chosen = followers[0] if followers else remaining[0]
        else:
            scores = {n: heat.score(n, case["task"], case["now"], strategy, graph.digest, half_life)
                      for n in remaining}
            if strategy == "decayed-task" and rng.random() < exploration:
                chosen = rng.choice(remaining)
            else:
                chosen = min(remaining, key=lambda n: (-scores[n], shuffled.index(n)))
        trace.append(chosen)
        if strategy != "dependency":
            edges_inspected += len(graph.neighbors(chosen))
        if strategy == "scout" and len(trace) <= 3:
            reports.append({"scout": "scout:" + str(len(trace)), "node": chosen,
                            "evidence_root": legal[chosen].evidence_root,
                            "claimed_useful": case["query"].casefold() in legal[chosen].label.casefold()})
    if strategy == "scout":
        recruitment = recruit(reports)
    found = required.intersection(trace)
    wrong = sum(n not in required for n in trace)
    return {"fixture": case["id"], "graph_family": graph.family, "graph_digest": graph.digest,
            "heat_digest": _digest([dataclasses.asdict(e) for e in heat.visits]),
            "strategy": strategy, "seed": seed, "trace": trace, "legal_candidates": sorted(legal),
            "candidate_set_digest": _digest([graph.digest, sorted(legal)]),
            "nodes_inspected": len(trace), "edges_inspected": edges_inspected,
            "context_bytes": sum(len(legal[n].text.encode()) for n in trace) + index_bytes + telemetry_bytes,
            "index_bytes": index_bytes, "telemetry_bytes": telemetry_bytes,
            "relevant_evidence_recall": len(found) / len(required),
            "wrong_path_rate": wrong / max(1, len(trace)), "rework_visits_proxy": wrong,
            "exploration_coverage": len(trace) / len(legal), "cold_start": not heat.visits,
            "version_mismatched_heat_events": sum(e.graph_version != graph.digest for e in heat.visits),
            "independent_source_roots_inspected": len({legal[n].evidence_root for n in trace}),
            "hydration_calls": len(trace), "tool_calls": 0, "model_calls": 0,
            "scout_reports": reports, "recruitment": recruitment,
            "wall_ns": time.perf_counter_ns() - started}


def fixtures():
    nodes = tuple(Node(key, label, text, root) for key, label, text, root in (
        ("entry", "module entry", "from parser import parse", "file:entry"),
        ("hot", "popular parser", "def popular(): return legacy_path", "file:parser"),
        ("noise", "logging helper", "def debug(): return noisy_output", "file:parser"),
        ("shared", "source dependency", "def normalize(): return canonical_bytes", "file:normalize"),
        ("rare", "repair serializer boundary", "def repair(): preserve_decisive_source", "file:serializer"),
        ("unused", "unused helper", "def obsolete(): return None", "file:obsolete")))
    edges = (("entry", "hot", "derived-ast"), ("entry", "noise", "derived-ast"),
             ("entry", "shared", "source-fact"), ("shared", "rare", "source-fact"),
             ("noise", "unused", "inferred"))
    code = Graph("ast-code", nodes, edges)
    operational = Graph("operational-view", tuple(Node(key, label, text, "episode:" + key) for key, label, text in (
        ("entry", "run", "run begins at approved snapshot"),
        ("hot", "frequent tool response", "repeated stale response is not completion"),
        ("noise", "diagnostic event", "low-value status repeats"),
        ("shared", "action and observation", "postcondition must be observed"),
        ("rare", "repair receipt challenge", "decisive late failure challenges earlier success"),
        ("unused", "old evaluation", "superseded evaluation retained"),
        ("review", "review outcome", "review contradicts one preliminary result"))),
        (("entry", "hot", "source-fact"), ("hot", "noise", "source-fact"),
         ("entry", "shared", "source-fact"), ("shared", "rare", "source-fact"),
         ("rare", "review", "source-fact"), ("noise", "unused", "inferred")))
    cases = []
    for index, name in enumerate(("rare-decisive", "stale-hot", "copied-prior", "noisy-agent",
                                  "frequent-low-value", "rights-fence", "cold-start")):
        graph = code if index % 2 == 0 else operational
        if name == "rights-fence":
            graph = Graph(graph.family, tuple(dataclasses.replace(n, allowed=False) if n.id == "hot" else n
                                             for n in graph.nodes), graph.edges)
        visits = [Visit("hot", "repair", 19, False, "copied:mistake", graph.digest)] * 20
        visits += [Visit("rare", "repair", 18, True, "validated:rare", graph.digest)]
        if name == "stale-hot":
            visits = [Visit("hot", "repair", 19, True, "old:episode", "prior-graph-version")] * 20
        elif name == "noisy-agent":
            visits += [Visit("noise", "repair", 19, False, "noisy:agent", graph.digest)] * 100
        elif name == "frequent-low-value":
            visits += [Visit("noise", "other-task", 19, True, "unrelated:root", graph.digest)] * 100
        elif name == "cold-start":
            visits = []
        cases.append({"id": name, "graph": graph, "heat": Heat(tuple(visits)),
                      "targets": ("rare",), "start": "entry", "task": "repair", "query": "repair", "now": 20})
    return cases


def run_study(seeds=(3, 11, 29)):
    cases = fixtures()
    strategies = ("random", "dependency", "lexical", "recency", "frequency", "decayed-task", "scout")
    return {"format_version": 1, "role": "synthetic-research-only",
            "graph_families": sorted({c["graph"].family for c in cases}),
            "profile": {"inspection_budget": 4, "half_life": 3, "exploration": .2,
                        "posture": "explicit toy treatments, no production calibration"},
            "runs": [navigate(c, strategy, seed) for c in cases for strategy in strategies for seed in seeds],
            "semantic_vector_comparator": {"status": "not-run", "substitute": "charged lexical-label relevance baseline"},
            "metric_basis": "instrumented in-memory visits/edges and UTF-8 payload/index/telemetry bytes; actual local wall time; no remote/model savings"}


if __name__ == "__main__":
    print(json.dumps(run_study(), indent=2))
