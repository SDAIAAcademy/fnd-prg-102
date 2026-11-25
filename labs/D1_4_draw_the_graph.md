---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "1.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_4_draw_the_graph.html"
---

# Lab 1.4 · Draw the graph, then check it

Addition: predict the graphs of three command sequences on paper, run them, compare with git log --graph

Day 1 · Session 4: Commits, staging and history

### Goal

Draw, before you run it, the commit graph that each of three short command sequences produces; then run them in a practice repository and compare your drawing with what Git recorded.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 1.4`: `practice/`, a repository with one commit, `sequences.md` and `graphs.md`
- Paper and a pen: the supervised check asks for graphs drawn by hand
- AI policy: **off**. The prediction is the exercise

### Predict, then run sequence 1 6 min

Draw the graph you expect after sequence 1: one circle per commit, an arrow from each commit to its parent, a label for each branch and for `HEAD`. Answer question 1 of `graphs.md`. Then run the sequence inside `practice/`.

### Compare and correct your drawing 4 min

```bash
# file: terminal
git log --oneline --graph --all
git log --format='%h %p %s'      # each commit with its parent
```

### Sequence 2: stage one change of two 9 min

Before you run `git commit`, read `git status --short`, `git diff` and `git diff --staged`, and say which file each one shows. Answer question 2 first.

### Sequence 3: a branch that moves while main moves too 10 min

Answer questions 3 and 4 and draw the graph, then run the sequence and compare with `git log --oneline --graph --all`. Which commits do the two branches share?

### Write the answers and check 6 min

Keep your first drawing even when it was wrong; put the right numbers on the answer lines.

```bash
# file: terminal
cd ../.. && uv run lab.py check 1.4
```

### ✱ Stretch

Predict what `git commit --amend` does to the last circle of your drawing, then try it on `main` and compare the commit id before and after.

## Check yourself

1. What does `git commit -am` leave out that `git add -A` would have staged?
2. Where does `HEAD` point after `git switch review-notes`, and what moves when you commit?
3. Why does a branch cost almost nothing to create?
