#!/usr/bin/env bash
# Lab 3.1, one command, and data kept out of the code.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 3.1 --discard
cd "$WS/3.1/air-report"
say "what the repository carries now"
git ls-files | sed 's|/.*|/|' | sort | uniq -c
say "stop tracking data and output, and ignore them"
git rm -r -q --cached data output
rm -rf data output
printf 'output/\ndata/\n__pycache__/\n.venv/\n.env\n' > .gitignore
say "the one command, the expected checksum and the README"
cp "$KIT/projects/v3/rebuild.sh" rebuild.sh
mkdir -p expected && cp "$KIT/projects/v3/expected/october.sha256" expected/
cp "$KIT/projects/v3/README.md" README.md
cat rebuild.sh
git add -A
git commit -q -m "Keep data and outputs out of the repository; rebuild with one command"
say "a clean clone, following the README only"
rm -rf ../clean && git clone -q . ../clean && cd ../clean
AIR_LOGS="$WS/3.1/data" bash rebuild.sh | tail -n 1
bash rebuild.sh 2>&1 | tail -n 1 || true
cd .. && rm -rf clean
cd "$WS" && lab check 3.1
