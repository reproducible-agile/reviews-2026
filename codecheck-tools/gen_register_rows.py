#!/usr/bin/env python3
"""Generate the codecheckers/register.csv rows for this year's certificates.

Reusable across years: certificate numbers and folders come from
`gen_codecheck.data` (the record of what was written for the year); the OSF
GUID per submission comes from `fetch_report_metadata.REVIEWS`. Repository
column prefers `osf::<guid>` (the report's own OSF project) and falls back to
`github::<GITHUB_REPO>|reports/<folder>` only for submissions with no OSF node
(e.g. ResearchEquals-hosted reports) - checked with a live HEAD request against
this repo's raw GitHub content, since that fallback only resolves once the
file is actually pushed.

Writes the rows (no header) to register-rows-2026.csv - the project-local
record of what gets submitted to codecheckers/register.
"""
import os
import sys
import urllib.request

from fetch_report_metadata import REVIEWS
from gen_codecheck import data as CODECHECK_DATA

GITHUB_REPO = "reproducible-agile/reviews-2026"
TYPE = "conference"
VENUE = "AGILEGIS"
ISSUE = 186
OUT = os.path.join(os.path.dirname(__file__), "register-rows-2026.csv")


def github_path_pushed(folder):
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/reports/{folder}/codecheck.yml"
    req = urllib.request.Request(url, method="HEAD")
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception:
        return False


def main():
    rows = []
    for sid, d in sorted(CODECHECK_DATA.items()):
        _, _, guid = REVIEWS[sid]
        folder = d["folder"]
        if guid:
            repo = f"osf::{guid}"
        else:
            if not github_path_pushed(folder):
                sys.exit(
                    f"submission {folder}: no OSF node and reports/{folder}/codecheck.yml "
                    f"is not yet pushed to github.com/{GITHUB_REPO} main - push it first"
                )
            repo = f"github::{GITHUB_REPO}|reports/{folder}"
        rows.append(f"{d['cert']},{repo},{TYPE},{VENUE},{ISSUE}")

    with open(OUT, "w") as f:
        f.write("\n".join(rows) + "\n")

    print(f"wrote {OUT}:\n")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
