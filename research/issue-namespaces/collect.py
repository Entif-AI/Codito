"""Read public Entif-AI issue-title census into a host-local file, using gh."""

import argparse
import datetime
import json
import subprocess
from pathlib import Path


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], text=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    repos = gh("repo", "list", "Entif-AI", "--limit", "1000", "--json", "nameWithOwner,isPrivate")
    if len(repos) >= 1000:
        raise SystemExit("repository limit reached; coverage cannot be claimed complete")
    rows = []
    for repo in sorted(repos, key=lambda r: r["nameWithOwner"]):
        if repo["isPrivate"]:
            continue
        name = repo["nameWithOwner"]
        try:
            pages = gh("api", "--paginate", "--slurp", f"repos/{name}/issues?state=all&per_page=100")
            issues = [{"number": i["number"], "title": i["title"], "url": i["html_url"], "state": i["state"]}
                      for page in pages for i in page if "pull_request" not in i]
            rows.append({"repo": name, "status": "complete", "issues": issues})
        except subprocess.CalledProcessError:
            rows.append({"repo": name, "status": "unavailable", "issues": []})
    data = {"observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "scope": "accessible-public-repositories-only", "protected_inventory": "not-established",
            "repositories": rows}
    args.output.write_text(json.dumps(data, indent=2) + "\n")


if __name__ == "__main__":
    main()
