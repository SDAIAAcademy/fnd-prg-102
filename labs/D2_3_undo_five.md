---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "2.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_3_undo_five.html"
---

# Lab 2.3 · Undo five mistakes

Addition: five mistakes in one repository, each with its own undo, one of them already pushed

Day 2 · Session 3: Undoing mistakes

### Goal

A repository with five mistakes in it, one of them already pushed. Undo each with the command made for it, and leave a history that nobody who pulled yesterday has to repair.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 2.3`: `report-repo/` and its hub
- The five mistakes: a scratch file staged by accident and a stray line in `client_report.md`; a local commit "Add debug output" that should not exist; the commit under it says "Add sectr line" and forgot `sectors.md`; a pushed commit "Change the threshold to 100" that was wrong; the branch `draft/winter-notes`, deleted by mistake
- AI policy: **off** for the first attempt

### Read the state 4 min

```bash
# file: terminal
uv run lab.py start 2.3
cd 2.3/report-repo
git status --short
git log --oneline --graph --all
git log --oneline origin/main       # what the hub already has
```

Mark on paper which commits are only on your laptop and which are on the hub. That decides which undo is safe.

### Unstage a file and discard a stray change 6 min

```bash
# file: terminal
git restore --staged scratch.txt    # out of the next commit; the file stays
rm scratch.txt
git restore client_report.md        # back to the last commit's version
```

### Drop a local commit, then fix the last one 9 min

"Add debug output" was never pushed: move `main` back one commit and drop it. Then the last commit is "Add sectr line": stage the forgotten file and amend the commit with the right message.

```bash
# file: terminal
git reset --hard HEAD~1
git add sectors.md
git commit --amend -m "Add sector line"
```

### Undo the pushed commit with revert 8 min

Others have pulled "Change the threshold to 100": do not rewrite it. Record a new commit that reverses it, and push.

```bash
# file: terminal
git log --oneline --grep 'threshold'
git revert <its id>
git push origin main
```

### Bring back the deleted branch and check 8 min

```bash
# file: terminal
git reflog | grep -i winter
git branch draft/winter-notes <the id the reflog shows>
git log --oneline --graph --all
cd ../.. && uv run lab.py check 2.3
```

### ✱ Stretch

For each of the five, write whether the same undo would be safe after a push, and why.

## Check yourself

1. What is the difference between `git restore --staged` and `git restore`?
2. Why is `reset --hard` fine for the debug commit and wrong for the threshold commit?
3. How long does the reflog keep a commit that no branch points at?
