"""Candidate process tooling for #67. No canonical allocation authority."""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

SLUG = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z][A-Za-z0-9]*)*\Z")
KEY = re.compile(r"^\s*\[?(?P<slug>[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z][A-Za-z0-9]*)*)"
                 r"[-_ ](?P<ordinal>\d{2,})(?=[\s:.)\]-]|$)")
STATUSES = {"active", "reserved", "deprecated", "alias", "historical", "protected-withheld"}


def extract_key(title):
    """Conservative title-prefix extraction, not inferred workstream meaning."""
    match = KEY.match(title)
    return (match["slug"], match["ordinal"]) if match else None


def census(repositories):
    groups, keys = defaultdict(list), defaultdict(list)
    count = 0
    coverage = []
    for row in repositories:
        coverage.append({"repository": row["repo"], "status": row["status"],
                         "issue_count": len(row["issues"])})
        for issue in row["issues"]:
            count += 1
            key = extract_key(issue["title"])
            if key is None:
                continue
            slug, ordinal = key
            occurrence = {"repository": row["repo"], "issue": issue["number"],
                          "source_ref": issue["url"], "state": issue["state"],
                          "observed_slug": slug, "ordinal": ordinal}
            groups[(row["repo"].casefold(), slug.casefold())].append(occurrence)
            keys[(row["repo"].casefold(), slug.casefold(), ordinal)].append(occurrence)
    namespaces = [{"repository": rows[0]["repository"], "slug": rows[0]["observed_slug"],
                   "occurrences": sorted(rows, key=lambda r: r["issue"])}
                  for _, rows in sorted(groups.items())]
    normalized = defaultdict(list)
    for namespace in namespaces:
        normalized[namespace["slug"].casefold()].append(namespace["repository"])
    return {"issue_count": count, "coverage": coverage, "namespaces": namespaces,
            "matched_issue_count": sum(len(g) for g in groups.values()),
            "cross_repository_prefix_reuse": [{"slug_normalized": k, "repositories": v}
                                               for k, v in sorted(normalized.items()) if len(v) > 1],
            "key_reuse": [v for _, v in sorted(keys.items()) if len(v) > 1]}


def _slug(value):
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        raise ValueError("slug must be an explicit ASCII mnemonic without whitespace")
    return value.casefold()


def _overlap(a, b):
    return (a["scope"] == "organization" or b["scope"] == "organization"
            or a["owner"] is None or b["owner"] is None
            or (a["owner"] or "").casefold() == (b["owner"] or "").casefold())


def validate_registry(document):
    if document.get("format_version") != 1 or document.get("authority") != "candidate":
        raise ValueError("this demonstrator validates candidate registries only")
    records = document.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    occupied = []
    for record in records:
        _slug(record.get("slug"))
        if record.get("scope") not in {"repository", "organization"}:
            raise ValueError("scope must be repository or organization")
        if record.get("status") not in STATUSES:
            raise ValueError("unknown namespace status")
        if record.get("publication_posture") not in {"public", "withheld"}:
            raise ValueError("publication posture must be explicit")
        withheld = record["status"] == "protected-withheld"
        if not withheld and (not isinstance(record.get("owner"), str) or not record["owner"]):
            raise ValueError("public namespaces require an owner reference")
        if withheld and (record.get("meaning") is not None or record["publication_posture"] != "withheld"):
            raise ValueError("protected meaning must be withheld")
        if record.get("allocation") not in {"unreviewed", "provisional", "approved"}:
            raise ValueError("allocation posture must be explicit")
        if not isinstance(record.get("source_refs"), list) or not record["source_refs"]:
            raise ValueError("namespace provenance is required")
        aliases = record.get("aliases")
        if not isinstance(aliases, list):
            raise ValueError("aliases must be a list")
        for name in [record["slug"], *aliases]:
            _slug(name)
            for old_name, old_record in occupied:
                if _slug(old_name) == _slug(name) and _overlap(old_record, record):
                    raise ValueError("overlapping exact or case-normalized namespace collision")
            occupied.append((name, record))
    for record in records:
        seen, current = set(), record
        while current["status"] == "alias":
            key = (_slug(current["slug"]), current["scope"], current["owner"])
            if key in seen:
                raise ValueError("alias cycle")
            seen.add(key)
            target = _slug(current.get("alias_of"))
            matches = [r for r in records if _slug(r["slug"]) == target and _overlap(r, current)]
            if len(matches) != 1:
                raise ValueError("alias target must resolve uniquely")
            current = matches[0]
    return document


def preflight(document, slug, repository, scope="repository"):
    validate_registry(document)
    normalized = _slug(slug)
    if scope not in {"repository", "organization"} or not repository:
        raise ValueError("a valid scope and repository are required")
    request = {"scope": scope, "owner": repository}
    conflicts = []
    for record in document["records"]:
        if _overlap(request, record):
            for name in [record["slug"], *record["aliases"]]:
                if _slug(name) == normalized:
                    conflicts.append({"slug": record["slug"], "owner": record["owner"],
                                      "status": record["status"],
                                      "match": "exact" if name == slug else "case-normalized",
                                      "source_refs": record["source_refs"]})
    return {"disposition": "collision" if conflicts else "needs-owner-decision",
            "allocation_authorized": False, "conflicts": conflicts,
            "authority": "candidate", "protected_coverage": "not-established"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "preflight", "census"):
        command = commands.add_parser(name)
        command.add_argument("input", type=Path)
        if name == "preflight":
            command.add_argument("slug")
            command.add_argument("--repository", required=True)
            command.add_argument("--scope", choices=("repository", "organization"), default="repository")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        if args.command == "validate":
            validate_registry(data)
            result, code = {"valid": True, "authority": "candidate"}, 0
        elif args.command == "census":
            result, code = census(data["repositories"]), 0
        else:
            result = preflight(data, args.slug, args.repository, args.scope)
            code = 1 if result["conflicts"] else 2
    except (ValueError, KeyError, TypeError, OSError) as error:
        result, code = {"error": str(error), "allocation_authorized": False}, 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
