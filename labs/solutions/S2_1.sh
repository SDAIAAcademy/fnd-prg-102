#!/usr/bin/env bash
# Lab 2.1, merge two branches and resolve a conflict alone.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 2.1 --discard
cd "$WS/2.1/report-repo"
say "the starting graph"
git log --oneline --graph --all
say "merge 1: main has not moved since the branch started, so a fast-forward"
git merge fix/threshold-wording
git log --oneline --graph --all
say "merge 2: both branches changed the threshold line"
if git merge --no-edit feature/sector-line; then echo "expected a conflict"; exit 1; fi
git status --short
grep -n -A2 -B2 '^=======' client_report.md
say "resolve: keep the sector line and both changes to the threshold line"
cat > client_report.md <<'MD'
# Monthly air-quality report

Client: {client}
Sector: {sector}
Alert threshold: hourly mean PM10 above 150 (the company's own rule)
Stations: {stations}

One row per station follows.
MD
git add client_report.md
git commit -q --no-edit
git log --oneline --graph --all
say "push to the hub, and see origin/main move"
git push -q origin main
git fetch -q origin
git log --oneline -1 origin/main
cd "$WS" && lab check 2.1
