#!/usr/bin/env python3
"""Generate the codecheckers/register.csv rows for this year's certificates.

Reusable across years: certificate numbers and folders come from
`gen_codecheck.data` (the record of what was written for the year); the OSF
GUID per submission comes from `fetch_report_metadata.REVIEWS`. Repository
column prefers `osf::<guid>` (the report's own OSF project) but only when a
live check confirms `codecheck.yml` is actually present there - `upload_to_osf.py`
can only write to projects where the maintainer is an OSF contributor, so many
GUIDs exist without a usable upload. Everything else (no OSF node at all, e.g.
ResearchEquals-hosted reports, or an OSF node the upload couldn't reach) falls
back to `github::<GITHUB_REPO>|reports/<folder>` - checked with a live HEAD
request against this repo's raw GitHub content, since that fallback only
resolves once the file is actually pushed.

Writes the rows (no header) to register-rows-2026.csv - the project-local
record of what gets submitted to codecheckers/register.
"""
import json
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


def osf_has_codecheck_yml(guid):
    url = f"https://api.osf.io/v2/nodes/{guid}/files/osfstorage/"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
    except Exception:
        return False
    return any(f["attributes"]["name"] == "codecheck.yml" for f in d["data"])


def main():
    rows = []
    for sid, d in sorted(CODECHECK_DATA.items()):
        _, _, guid = REVIEWS[sid]
        folder = d["folder"]
        if guid and osf_has_codecheck_yml(guid):
            repo = f"osf::{guid}"
        else:
            if not github_path_pushed(folder):
                sys.exit(
                    f"submission {folder}: no usable OSF codecheck.yml and reports/{folder}/codecheck.yml "
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
