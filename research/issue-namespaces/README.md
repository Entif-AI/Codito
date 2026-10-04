# Issue namespace census and candidate registry

Owner discussion: [Codito #67](https://github.com/Entif-AI/Codito/issues/67).
Publication posture: public process tooling. These files are a candidate analysis
copy. Codito has no authority to allocate organization namespaces.

The 2026-10-04 census paginated every issue, open and closed, excluding PRs, in
all 47 accessible public Entif-AI repositories. It inspected 1,129 issues and
matched 340 explicit leading numbered keys in 119 namespaces. Ten exact or
case-normalized full keys recur within a repository. Their issue references are
in `census.json`. Repeated keys are review candidates, not proof that their
meanings conflict. No cross-repository prefix reuse was found by this extractor.

Extraction accepts leading ASCII mnemonics with a separator and two or more
digits, including bracketed compound keys. It does not infer mnemonic families
from descriptive prose, unnumbered tags, issue bodies, spreadsheets or chats.
Thus unparsed titles and unknown protected repositories remain coverage gaps.
Public issue titles/bodies are not copied into the published census. Only
numbered keys and public issue references are retained.

`candidate-registry.json` records slug, scope, owner reference, status, meaning,
allocation posture, aliases, source references and collision notes. Observed
use is `historical` and `unreviewed`; it is not an approved active allocation.
ADI and MCA are provisional organization reservation candidates, as requested
by #67. Neither has been globally allocated.

Statuses are `active`, `reserved`, `deprecated`, `alias`, `historical`, and
`protected-withheld`. Protected reservations may withhold owner and meaning.
Unknown owners conservatively overlap every scope. This census contains no
invented protected reservation and establishes no protected inventory.

Run offline validation and proposed-key preflight from the repository root:

```sh
python -m codito.namespace_registry validate research/issue-namespaces/candidate-registry.json
python -m codito.namespace_registry preflight research/issue-namespaces/candidate-registry.json ADI --repository Entif-AI/Codito --scope organization
```

Preflight exits 1 on occupied exact/case-normalized names or aliases, 2 when
ownership is unresolved or input is invalid, and always returns
`allocation_authorized: false`. A free-looking candidate copy cannot authorize
allocation. Repository namespaces can coexist in different repositories;
organization namespaces overlap all repositories. Deprecated and historical
names stay occupied until an authorized owner resolves reuse explicitly.

Groomers, generators and graph tools should consult the selected canonical
registry before creating numbered keys. During this unresolved transition,
they may use this copy to find collisions, then use descriptive titles and
GitHub issue numbers without a mnemonic. They must report unavailable or stale
coverage, and must not treat a spreadsheet/chat-local list as allocation authority.

Migration preserves historical issue titles. Reserve a new name through the
eventual owner, add an alias to the old name or an alias record with `alias_of`,
retain provenance, and deprecate future use of the old name. Alias targets must
resolve uniquely; cycles and overlapping records fail validation. Do not bulk
rename issues or silently transfer a repository allocation to global scope.

Refresh inputs through `collect.py`, then inspect the conservative extraction
before replacing the analysis files. The collector uses authenticated `gh`,
reads public repositories only, and makes no issue mutations. The raw title
input should remain outside the public tree. Record the actual read timestamp
and every repository's success/failure; failed reads must not become absence.

## Canonical-home decision packet

Disposition: `NEEDS_HUMAN_DECISION` for the canonical-home acceptance item.
No established organization governance home was found in the accessible
repository inventory or Codito/Rosetta authority entrypoints. Protected access
is insufficient to rule out an existing protected owner.

An authorized organization maintainer must choose the home, accountable owner,
allocation approver, protected-reservation ingestion path, freshness rules and
consultation interface. Options are an existing authorized organization process
repository if one exists, a deliberately established organization governance
home, or an explicitly delegated existing repository. A Codito analysis copy
or a Rosetta semantic schema location does not acquire that authority by use.

After the decision, retain this census as evidence, transfer the reviewed
records without inferring allocations, resolve the ten historical key-reuse
groups, and document the canonical lookup path. Only the owning authority may
approve ADI/MCA. The other tooling/census acceptance items are independently
reviewable now; #67 remains open for this decision and protected coverage.
