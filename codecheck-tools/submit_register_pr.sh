#!/usr/bin/env bash
# Open a PR against codecheckers/register adding this year's certificate rows.
# Reusable across years: reads codecheck-tools/register-rows-2026.csv (produced
# by gen_register_rows.py). Uses the GitHub Contents/Git API exclusively -
# never clones the repo, which is >1 GB even at a single commit (docs/certs/
# holds rendered certificate PDFs/PNGs for every past certificate) - only
# register.csv itself is ever touched.
#
# Usage: ./submit_register_pr.sh [--dry-run]
#   --dry-run: fetch and compute the new register.csv, print the diff, but
#              don't create a branch, commit, or open a PR.
set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROWS_CSV="$HERE/register-rows-2026.csv"
YEAR_ROWS_LABEL="2026-004 to 2026-017"
BRANCH="agile-2026-certificates"
UPSTREAM="codecheckers/register"

if [[ ! -f "$ROWS_CSV" ]]; then
  echo "missing $ROWS_CSV - run gen_register_rows.py first" >&2
  exit 1
fi

DEFAULT_BRANCH="$(gh api "repos/$UPSTREAM" --jq '.default_branch')"

echo "== forking $UPSTREAM (reuses an existing fork) =="
gh repo fork "$UPSTREAM" --remote=false >/dev/null 2>&1 || true
FORK_OWNER="$(gh api user -q .login)"
FORK="$FORK_OWNER/register"

echo "== syncing $FORK's $DEFAULT_BRANCH with upstream =="
gh repo sync "$FORK" --source "$UPSTREAM" --force

echo "== fetching current register.csv from $FORK@$DEFAULT_BRANCH =="
CONTENTS_JSON="$(gh api "repos/$FORK/contents/register.csv?ref=$DEFAULT_BRANCH")"
BASE_SHA="$(echo "$CONTENTS_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["sha"])')"
OLD_CSV="$(mktemp)"
NEW_CSV="$(mktemp)"
trap 'rm -f "$OLD_CSV" "$NEW_CSV"' EXIT
echo "$CONTENTS_JSON" | python3 -c '
import json, sys, base64
d = json.load(sys.stdin)
sys.stdout.buffer.write(base64.b64decode(d["content"]))
' > "$OLD_CSV"

cp "$OLD_CSV" "$NEW_CSV"
cat "$ROWS_CSV" >> "$NEW_CSV"

echo "== diff =="
diff -u "$OLD_CSV" "$NEW_CSV" || true

echo "== saving project-local snapshot to codecheck-tools/register.csv =="
cp "$NEW_CSV" "$HERE/register.csv"

if $DRY_RUN; then
  echo "== --dry-run: not branching, committing, or opening a PR =="
  exit 0
fi

BASE_COMMIT_SHA="$(gh api "repos/$FORK/git/refs/heads/$DEFAULT_BRANCH" --jq '.object.sha')"
echo "== creating branch $BRANCH on $FORK from $DEFAULT_BRANCH ($BASE_COMMIT_SHA) =="
gh api "repos/$FORK/git/refs" -f ref="refs/heads/$BRANCH" -f sha="$BASE_COMMIT_SHA" >/dev/null \
  || echo "  (branch may already exist - continuing)"

echo "== committing updated register.csv to $FORK@$BRANCH =="
NEW_CONTENT_B64="$(python3 -c '
import base64
with open("'"$NEW_CSV"'", "rb") as f:
    print(base64.b64encode(f.read()).decode())
')"
gh api "repos/$FORK/contents/register.csv" -X PUT \
  -f message="Add AGILEGIS 2026 certificates ($YEAR_ROWS_LABEL)" \
  -f content="$NEW_CONTENT_B64" \
  -f sha="$BASE_SHA" \
  -f branch="$BRANCH" >/dev/null

echo "== opening PR against $UPSTREAM =="
gh pr create --repo "$UPSTREAM" \
  --head "$FORK_OWNER:$BRANCH" \
  --base "$DEFAULT_BRANCH" \
  --title "AGILEGIS 2026 certificates ($YEAR_ROWS_LABEL)" \
  --body "$(cat <<EOF
Adds the register.csv rows for the AGILE 2026 reproducibility reviews, certificates $YEAR_ROWS_LABEL.

Reports: https://github.com/reproducible-agile/reviews-2026/tree/main/reports

Related: codecheckers/register#186
EOF
)"

echo "== done =="
