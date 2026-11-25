#!/usr/bin/env bash
# Lab 3.3, the key out of the code.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 3.3 --discard
cd "$WS/3.3/air-report"
say "where is the key?"
grep -rn 'fprg102_' --include='*.py' . | cut -c1-60
say "read it from the environment, fail clearly, print only its end"
cp "$KIT/files/3.3/report.solution.py" report.py
printf 'AIR_PORTAL_KEY=\n' > .env.example
git check-ignore -v .env
printf 'AIR_PORTAL_KEY=%s\n' "$(grep -o 'fprg102_demo_[0-9a-f]*' "$KIT/lab.py" | head -n 1)" > .env
export AIR_PORTAL_DIR="$WS/3.3/portal"
uv run -q python report.py --data ../data --upload > /dev/null 2> err.txt || true; tail -n 1 err.txt; rm err.txt
uv run -q --env-file .env python report.py --data ../data --upload | tail -n 2
git add report.py .env.example
git commit -q -m "Read the portal key from the environment"
say "the key is gone from the files, not from the history"
git grep -c 'fprg102_demo_' || echo "no file holds a key"
git log --oneline -S 'fprg102_demo_' --all
cd "$WS" && lab check 3.3
