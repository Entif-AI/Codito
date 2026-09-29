"""Finite C22/C23/C14 illustrations. No provider, database or effect integration.

JSON hashing here is a restricted fixture serialization, not Rosetta/JCS
conformance. Generations model a complete trusted change feed; real adapters
must separately establish that coverage. The executor is in-memory only.
"""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import PurePosixPath
from threading import Lock
from typing import Mapping
import json


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def fixture_digest(value: object) -> str:
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode())


@dataclass(frozen=True)
class Scope:
    tenant: str
    purpose: str
    policy_epoch: str

    def __post_init__(self):
        if not all((self.tenant, self.purpose, self.policy_epoch)):
            raise ValueError("All authority bindings are required")


@dataclass(frozen=True)
class QueryWitness:
    scope: Scope
    query_version: str
    predicate: tuple[tuple[str, str], ...]
    generation: int
    result_ids: tuple[str, ...]
    result_digest: str
    complete: bool

    @property
    def bounded_absence(self) -> bool:
        return self.complete and not self.result_ids


class ScopedIndex:
    """Conservative per-tenant invalidation with explicit policy comparison.

    Each authorized fixture row belongs to one tenant. This deliberately does
    not simulate arbitrary ABAC or a real provider's visibility semantics.
    """
    def __init__(self):
        self.rows: dict[tuple[str, str], dict[str, str]] = {}
        self.generations: dict[str, int] = {}

    def put(self, tenant: str, row_id: str, row: Mapping[str, str]) -> None:
        if not tenant or not row_id or not all(isinstance(k, str) and isinstance(v, str) for k, v in row.items()):
            raise ValueError("Fixture rows have nonempty identities and string fields")
        if self.rows.get((tenant, row_id)) != dict(row):
            self.rows[tenant, row_id] = dict(row)
            self.generations[tenant] = self.generations.get(tenant, 0) + 1

    def delete(self, tenant: str, row_id: str) -> None:
        if (tenant, row_id) in self.rows:
            del self.rows[(tenant, row_id)]
            self.generations[tenant] = self.generations.get(tenant, 0) + 1

    def query(self, scope: Scope, predicate: Mapping[str, str], *, authorized: bool,
              complete: bool = True, query_version: str = "fixture-query/v1") -> QueryWitness:
        if not authorized:
            raise PermissionError("No query metadata is exposed before admission")
        if not query_version or not all(isinstance(k, str) and isinstance(v, str) for k, v in predicate.items()):
            raise ValueError("A versioned string-equality predicate is required")
        rows = sorted((rid, row) for (tenant, rid), row in self.rows.items()
                      if tenant == scope.tenant and all(row.get(k) == v for k, v in predicate.items()))
        return QueryWitness(scope, query_version, tuple(sorted(predicate.items())),
                            self.generations.get(scope.tenant, 0), tuple(rid for rid, _ in rows),
                            fixture_digest(rows), complete)

    def reusable(self, witness: QueryWitness, scope: Scope, predicate: Mapping[str, str], *,
                 authorized: bool, query_version: str = "fixture-query/v1") -> bool:
        return bool(authorized and witness.complete and witness.scope == scope
                    and witness.query_version == query_version
                    and witness.predicate == tuple(sorted(predicate.items()))
                    and witness.generation == self.generations.get(scope.tenant, 0))


def safe_path(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(name and not p.is_absolute() and ".." not in p.parts and "\\" not in name
                and str(p) == name and name != ".")


def capture_manifest(files: Mapping[str, bytes], required: set[str],
                     before: Mapping[str, str], after: Mapping[str, str]) -> dict:
    if not before or before != after:
        raise ValueError("Capture has no stable declared cut")
    if not required or not required.issubset(files) or not all(safe_path(p) for p in files):
        raise ValueError("Required closure or path safety is missing")
    return {"profile": "fixture-recovery/v1", "cut": dict(before), "required": sorted(required),
            "files": {p: digest(b) for p, b in sorted(files.items())},
            "restore_authority": "reauthorize", "index_strategy": "rebuild_from_declared_edges"}


def restore_plan(manifest: Mapping, payload: Mapping[str, bytes], attempts: Mapping[str, str]) -> dict:
    if manifest.get("profile") != "fixture-recovery/v1" or not manifest.get("cut"):
        raise ValueError("Unknown or incomplete recovery profile")
    hashes = manifest.get("files", {})
    required = set(manifest.get("required", ()))
    if not required or not required.issubset(hashes) or set(hashes) != set(payload):
        raise ValueError("Manifest closure does not match payload")
    if any(not safe_path(p) or digest(payload[p]) != h for p, h in hashes.items()):
        raise ValueError("Hash or path validation failed")
    if manifest.get("restore_authority") != "reauthorize":
        raise ValueError("Historical authority cannot be reactivated")
    valid_states = {"prepared", "admitted", "submitted", "acknowledged", "ambiguous", "observed", "compensated"}
    if any(s not in valid_states for s in attempts.values()):
        raise ValueError("Unknown effect state")
    return {"reauthorize": True, "rebuild_indexes": True, "live_leases_restored": False,
            "reconcile": sorted(k for k, s in attempts.items() if s in {"submitted", "acknowledged", "ambiguous"}),
            "automatic_effect_replay": False}


class FencedIntentExecutor:
    """One-process fixture only. Lock and history do not survive process loss."""
    def __init__(self):
        self.epoch = 0
        self.intents: dict[tuple[str, str], str] = {}
        self.effects = 0
        self.lock = Lock()

    def advance_epoch(self, epoch: int) -> None:
        with self.lock:
            if epoch <= self.epoch:
                raise ValueError("Execution epoch must advance")
            self.epoch = epoch

    def execute(self, scope: str, key: str, request_digest: str, epoch: int, *, admitted: bool) -> str:
        with self.lock:
            if not admitted:
                raise PermissionError("No effect without current admission")
            if not all((scope, key, request_digest)) or epoch != self.epoch:
                raise ValueError("Missing binding or stale execution fence")
            old = self.intents.get((scope, key))
            if old is not None and old != request_digest:
                raise ValueError("Same key, different intent")
            if old is not None:
                return "duplicate"
            self.intents[(scope, key)] = request_digest
            self.effects += 1
            return "applied"