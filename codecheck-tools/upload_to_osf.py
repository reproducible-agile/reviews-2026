#!/usr/bin/env python3
"""Upload each reports/<id>/codecheck.yml to the root of its OSF project.

Reusable across years: the submission -> OSF node GUID mapping comes from
`fetch_report_metadata.REVIEWS` (entries with GUID `None`, e.g. ResearchEquals-
hosted reports, are skipped - their codecheck.yml stays only in this GitHub repo).

Always shows a full review listing first: for every target it prints the
project's OSF title, the current root `osfstorage` file listing (so an
existing codecheck.yml - and that this would overwrite it - is visible), and
the exact local file content that would be uploaded. Only after all of that is
printed does it ask for one explicit go-ahead; nothing is ever uploaded
silently. `--dry-run` stops after the listing. `--confirm` skips the
interactive prompt for non-interactive use, but still shows the listing first.

Needs `OSF_PAT` (read from this directory's ../.env, or the environment) and
the `osfclient` package (see requirements.txt).
"""
import argparse
import json
import os
import sys
import urllib.request

from fetch_report_metadata import REVIEWS, REPORTS_DIR, UA

from osfclient.api import OSF

ENV_FILE = os.path.join(os.path.dirname(__file__), os.pardir, ".env")


def load_osf_pat():
    token = os.environ.get("OSF_PAT")
    if token:
        return token
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OSF_PAT="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def osf_node_title(guid):
    req = urllib.request.Request(f"https://api.osf.io/v2/nodes/{guid}/", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return data["data"]["attributes"]["title"]


def targets():
    for sid, (art, report_doi, guid) in sorted(REVIEWS.items()):
        if not guid:
            continue
        folder = os.path.join(REPORTS_DIR, f"{sid:03d}")
        local_path = os.path.join(folder, "codecheck.yml")
        yield sid, guid, local_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="show the review listing, never upload")
    p.add_argument("--confirm", action="store_true", help="skip the interactive prompt (still shows the listing)")
    args = p.parse_args()

    token = load_osf_pat()
    if not token:
        sys.exit("OSF_PAT not found in environment or ../.env")

    listing = list(targets())
    missing = [t for t in listing if not os.path.isfile(t[2])]
    if missing:
        sys.exit(f"missing local codecheck.yml for: {[os.path.basename(os.path.dirname(t[2])) for t in missing]}")

    print(f"=== review: {len(listing)} OSF targets ===\n")
    for sid, guid, local_path in listing:
        title = osf_node_title(guid)
        print(f"--- submission {sid:03d} -> osf::{guid} ({title}) ---")
        try:
            osf = OSF(token=token)
            storage = osf.project(guid).storage()
            existing = sorted(f.path.lstrip("/") for f in storage.files)
        except Exception as e:
            existing = [f"<error listing files: {e}>"]
        print(f"current root files: {existing}")
        overwrite = "codecheck.yml" in existing
        print(f"would {'OVERWRITE' if overwrite else 'CREATE'} codecheck.yml\n")
        with open(local_path) as f:
            print(f.read())
        print("-" * 60)

    if args.dry_run:
        print("\n--dry-run: stopping before any upload.")
        return

    if not args.confirm:
        answer = input(f"\nUpload the {len(listing)} files listed above to OSF now? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted, nothing uploaded.")
            return

    osf = OSF(token=token)
    results = []
    for sid, guid, local_path in listing:
        try:
            storage = osf.project(guid).storage()
            with open(local_path, "rb") as f:
                storage.create_file("codecheck.yml", f, update=True)
            # osfclient's create_file only checks for status 409; a 403 (no
            # write access - Daniel not a contributor on that OSF project)
            # returns just as quietly, so verify the file actually landed.
            names = [f.path.lstrip("/") for f in storage.files]
            if "codecheck.yml" in names:
                results.append((f"{sid:03d}", guid, "uploaded"))
            else:
                results.append((f"{sid:03d}", guid, "FAILED: not present after upload (likely no write access)"))
        except Exception as e:
            results.append((f"{sid:03d}", guid, f"error: {e}"))

    print("\n=== summary ===")
    for folder, guid, status in results:
        print(f"{folder}  osf::{guid}  {status}")


if __name__ == "__main__":
    main()
