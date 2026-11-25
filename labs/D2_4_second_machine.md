---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "2.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_4_second_machine.html"
---

# Lab 2.4 · Rescue a project that fails on a second machine

Clone the report project as a second machine, read why it fails, then declare, lock and rebuild it to the expected output

Day 2 · Session 4: Virtual environments and lock files

### Goal

The analyst's report project runs on their laptop. Clone it as a second machine, read each reason it fails, then declare and lock its dependencies, take the data folder from outside the code, and rebuild it in a fresh environment until it writes the expected October report.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 2.4`: `first-machine/air-report` (the analyst's repository) and `data/` (the October logs, outside the repository)
- uv, and a network connection for the first download of two small packages
- AI policy: **off** for the first attempt

### Clone to a second machine, run it, read each failure 7 min

```bash
# file: terminal
uv run lab.py start 2.4
cd 2.4
git clone first-machine/air-report second-machine
cd second-machine
cat README.md requirements.txt
uv run --isolated --no-project python report.py                 # nothing installed
uv run --isolated --no-project --with-requirements requirements.txt python report.py
```

`--isolated` runs in a fresh, empty environment: the closest thing to another machine on your own laptop. Write down the last line of each error.

### Name the causes 5 min

Read `report.py`. List every reason it ran on the analyst's laptop and not here: a package it imports that nothing declares, a path that exists on one computer, versions nobody wrote down, a folder it writes to without creating it.

### Declare, pin Python, lock 8 min

```bash
# file: terminal
uv init --bare --name air-report --python 3.11     # writes pyproject.toml
uv add tabulate python-dateutil                    # declares both and writes uv.lock
uv python pin 3.13                                 # writes .python-version
git rm requirements.txt
cat pyproject.toml
```

### Take the data folder from outside; rebuild fresh and compare 10 min

Change `report.py`: read the folder from a `--data` argument (default: the `AIR_LOGS` variable), stop with a clear message when neither is given, and create the output folder before writing. Then rebuild from the lock in a fresh environment:

```bash
# file: terminal
rm -rf .venv output
uv sync --locked
uv run python report.py --data ../data
sha256sum output/report.csv
```

The trainer gives the expected checksum. If yours differs, compare the first rows with the trainer's.

### Commit the declaration and the lock; check 5 min

```bash
# file: terminal
git add pyproject.toml uv.lock .python-version report.py
git commit -m "Declare and lock the dependencies; take the data folder as an argument"
cd ../.. && uv run lab.py check 2.4
```

The check clones your repository a third time, runs `uv sync --locked` and the report, and compares the result.

### ✱ Stretch

Lock the same project with pip-tools: write `requirements.in` with the two packages, run `uvx --from pip-tools pip-compile --generate-hashes requirements.in`, and compare its pins with `uv.lock`.

## Check yourself

1. What does `uv.lock` record that `pyproject.toml` does not?
2. Why does `uv sync --locked` refuse to run when the lock is out of date, instead of updating it?
3. Why is the data folder not in the repository, and how does a newcomer find out where it is?
