#!/usr/bin/env bash
# Lab 2.4, rescue a project that fails on a second machine.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 2.4 --discard
cd "$WS/2.4"
say "the second machine: a clean clone, nothing installed"
git clone -q first-machine/air-report second-machine
cd second-machine
git config user.name "Participant A"; git config user.email participant-a@example.invalid
uv run --isolated --no-project -q python report.py 2>&1 | tail -n 1 || true
uv run --isolated --no-project -q --with-requirements requirements.txt python report.py 2>&1 | tail -n 1 || true
uv run --isolated --no-project -q --with-requirements requirements.txt --with python-dateutil python report.py 2>&1 | tail -n 1 || true
say "declare, pin and lock"
uv init -q --bare --name air-report --python 3.11
uv add -q tabulate python-dateutil
uv python pin 3.13 > /dev/null
git rm -q requirements.txt
cp "$KIT/projects/v2/report.py" report.py
grep -n 'add_argument\|mkdir' report.py
cat pyproject.toml
say "rebuild in a fresh environment and compare"
rm -rf .venv output
uv sync --locked -q
uv run -q python report.py --data ../data | tail -n 2
sha256sum output/report.csv
git add pyproject.toml uv.lock .python-version report.py
git commit -q -m "Declare and lock the dependencies; take the data folder as an argument"
git log --oneline
cd "$WS" && lab check 2.4
