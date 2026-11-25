---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "3.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_1_one_command.html"
---

# Lab 3.1 · One command, and data kept out of the code

Addition: data and output out of the repository, one rebuild command with a checksum, a README tested in a clean clone

Day 3 · Session 1: One command to rebuild and run

### Goal

The locked report project still carries its data and its last output in the repository, and its README says too little. Take data and output out, write one documented command that rebuilds and checks the result, and test the README by following it in a clean clone.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 3.1`: `air-report/` (the project as lab 2.4 left it, plus a committed `data/` and `output/`) and `data/` beside it, where the logs belong
- The expected October checksum: `october.sha256`, in the workspace's kit under `_kit/projects/v3/expected/`, or from the trainer
- AI policy: **off** for the first attempt

### List what the repository carries 4 min

```bash
# file: terminal
uv run lab.py start 3.1
cd 3.1/air-report
git ls-files | sed 's|/.*|/|' | sort | uniq -c
```

Which of these are code, which are data, which are results? Which could the next month's run change?

### Stop tracking data and output 7 min

```bash
# file: terminal
git rm -r --cached data output      # out of git; the files stay on disk
rm -rf data output                  # the logs live in ../data now
printf 'output/\ndata/\n__pycache__/\n.venv/\n.env\n' > .gitignore
git status --short
```

`.gitignore` stops new files being added; it does nothing for files already tracked, which is why `git rm --cached` comes first.

### Write rebuild.sh 9 min

One command that a newcomer runs: it stops with a clear message when `AIR_LOGS` is not set, rebuilds the environment from the lock, runs the report into `output/`, and compares the result with a committed checksum.

```bash
# file: terminal
mkdir -p expected
cp ../../_kit/projects/v3/expected/october.sha256 expected/
# then write rebuild.sh: set -euo pipefail; uv sync --locked;
# uv run python report.py --data "$AIR_LOGS" --out output; sha256sum -c expected/october.sha256
```

### Write the README's Reproduce section 6 min

Under `## Reproduce`: the tools needed, where the data comes from, the one command, and what success looks like. Nothing that only you know.

### Follow the README in a clean clone; check 9 min

```bash
# file: terminal
git add -A
git commit -m "Keep data and outputs out of the repository; rebuild with one command"
git clone . ../clean && cd ../clean
AIR_LOGS=../data bash rebuild.sh     # ends with: output/report.csv: OK
bash rebuild.sh                      # must stop with a message, not guess
cd .. && rm -rf clean
cd .. && uv run lab.py check 3.1
```

### ✱ Stretch

Make `rebuild.sh` print the versions it ran with (`uv --version`, the Python version, `uv tree`) so a reproduction log can quote them.

## Check yourself

1. Why does adding `data/` to `.gitignore` not remove the logs already committed?
2. What does a committed checksum prove that "it ran without errors" does not?
3. Your clean clone works on your laptop. What could still fail on a peer's?
