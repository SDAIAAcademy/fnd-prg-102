---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "2.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_1_merge_alone.html"
---

# Lab 2.1 · Merge two branches and resolve a conflict alone

Addition: merge two branches into main, keep both changes on the conflicting line, push to the hub

Day 2 · Session 1: Branches, merges and conflicts

### Goal

Two branches changed the report template: the analyst's says the threshold is the company's own rule, the field technician's adds a sector line and says the threshold is an hourly mean. Bring both into `main` so that every change survives, then push to the hub.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 2.1`: `report-repo/` with `main` and two branches, and `hub/report.git`, the stand-in for the class Git host (its `origin`)
- AI policy: **off** for the first attempt. Resolving a conflict by reading it is the skill

### Read the graph and both branches 5 min

```bash
# file: terminal
uv run lab.py start 2.1
cd 2.1/report-repo
git log --oneline --graph --all
git diff main fix/threshold-wording
git diff main feature/sector-line
```

Draw the graph on paper. Predict: which of the two merges will be a fast-forward, and which will make a merge commit?

### Merge the first branch 5 min

```bash
# file: terminal
git merge fix/threshold-wording
git log --oneline --graph --all
```

Read the first line of the output. What did Git do to `main`, and did it make a new commit?

### Merge the second and read the conflict 7 min

```bash
# file: terminal
git merge feature/sector-line
git status --short
cat client_report.md
```

Between `<<<<<<< HEAD` and `=======` is `main` as it is now; between `=======` and `>>>>>>>` is the branch. Neither side is wrong: each changed the same line for a different reason.

### Resolve so both changes survive, and commit 10 min

Edit `client_report.md`: keep the sector line, and write one threshold line that says both things. Remove every marker line.

```bash
# file: terminal
grep -n '^<<<<<<<\|^=======\|^>>>>>>>' client_report.md   # prints nothing when done
git add client_report.md
git commit --no-edit
```

### Push, fetch and check 8 min

```bash
# file: terminal
git push origin main
git fetch origin
git log --oneline --graph --all | head -n 8
cd ../.. && uv run lab.py check 2.1
```

Find `origin/main` in the graph. It is your clone's record of where `main` was on the hub at the last fetch or push.

### ✱ Stretch

In a copy of the starting state (`uv run lab.py start 2.1 --discard`, after copying your folder away), put the second branch on top of `main` with `git rebase main` instead of merging, and compare the two graphs. Which tells a reviewer more?

## Check yourself

1. Why was the first merge a fast-forward and the second not?
2. What would `git checkout --theirs client_report.md` have thrown away?
3. What does a merge commit have that an ordinary commit does not?
