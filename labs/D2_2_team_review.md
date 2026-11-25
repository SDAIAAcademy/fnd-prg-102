---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "2.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_2_team_review.html"
---

# Lab 2.2 · Branch, review and resolve a conflict in teams of three

Two authors and a reviewer, a protected main: two pull requests reviewed, one conflict resolved on its branch, both merged

Day 2 · Session 2: Pull requests and review etiquette

### Goal

In teams of three, change the rules of the client report the way a team does: on branches, through pull requests that a teammate reviews, with comments answered by commits, and a merge conflict resolved by the author of the second request before it is merged into a protected `main`.

## What you need

- Roles: **Participant A** (author of request 1), **Participant B** (author of request 2), **Participant C** (reviewer and integrator). Swap roles if you redo the lab
- With a class Git host (Forgejo, Gitea, GitLab or GitHub): the trainer's team repository, whose `main` is protected and needs one approval; each person on their own laptop
- Without one: one laptop per team and the kit's hub. `uv run lab.py start 2.2` writes `hub/` (protected `main`) and three clones, `participant-a/`, `participant-b/` and `participant-c/`; take turns at the keyboard, each in their own clone. `uv run lab.py pr ...` plays the host's pull requests
- AI policy: **off** for the first attempt

### Take roles; try to push to main 4 min

```bash
# file: terminal (A)
cd 2.2/participant-a
echo "5. test" >> rules.md
git commit -am "Try to push to main"
git push origin main            # read the refusal
git reset --hard origin/main    # throw the test away
```

### Authors: one branch, one commit, one pull request each 8 min

A adds a rule 4 on comment lines in the logs; B adds a rule 4 on a station's first day of readings. Each on a branch named after the change.

```bash
# file: terminal (A, then B in its own clone)
git switch -c rules/comment-lines
echo "4. Lines that start with # are left out." >> rules.md
git commit -am "Add the rule on comment lines"
git push -u origin rules/comment-lines
cd ../.. && uv run lab.py pr open rules/comment-lines "Add the rule on comment lines" --as participant-a
```

### Reviewer comments on a line, with a reason; authors answer with a commit 9 min

C reads each request (`uv run lab.py pr show 1`) and writes one comment that names a line and a reason. Each author answers with a new commit on the branch, pushes, and only then resolves the comment.

```bash
# file: terminal
uv run lab.py pr comment 1 "rules.md line 4: say why ..." --as participant-c
uv run lab.py pr resolve 1 1 --as participant-a      # after pushing the answer
```

### Merge the first; the second author resolves the conflict 9 min

```bash
# file: terminal
uv run lab.py pr approve 1 --as participant-c
uv run lab.py pr merge 1 --as participant-c
uv run lab.py pr approve 2 --as participant-c
uv run lab.py pr merge 2 --as participant-c          # refused: a conflict
```

B brings the new `main` into the branch, keeps both rules (numbered 4 and 5), commits and pushes:

```bash
# file: terminal (B)
git fetch origin
git merge origin/main           # resolve rules.md, then git add and git commit
git push
```

### Approve the new commits, merge and check 5 min

An approval counts for the commit it was given on; the merge from `main` is new, so C reads it and approves again.

```bash
# file: terminal
uv run lab.py pr show 2
uv run lab.py pr approve 2 --as participant-c
uv run lab.py pr merge 2 --as participant-c
uv run lab.py check 2.2
```

### ✱ Stretch

Add the team's five-line review checklist through a third pull request, reviewed by A.

## Check yourself

1. Why did the host refuse the push to `main`, and why is that a good thing for a team?
2. Why does the author of the second request resolve the conflict, and not the reviewer?
3. Why must the reviewer approve again after the conflict was resolved?
