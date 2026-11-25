---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/slides/day2.html"
---

# Command Line, Git and Reproducible Environments

## Day 2: Working together on one history

Branches, reviewed pull requests, conflicts, undoing, and an environment that rebuilds

#### [day2#title] Working together on one history

*SDAIA Academy · Command Line, Git and Reproducible Environments*

Day 2: Branches, reviewed pull requests, conflicts, undoing, and an environment that rebuilds

Data & AI Foundations Track · 3 teaching days + capstone day · 4 sessions · 4 labs · FND-PRG-102

#### [day2#agenda] Working together on one history

*Today*

- **Session 1 · Branches, merges and conflicts**: Two lines of work join in a merge; when both changed the same lines, a person decides
- **Session 2 · Pull requests and review etiquette**: Main changes only through small, reviewed requests; a good comment names a line and a reason
- **Session 3 · Undoing mistakes**: Each mistake has its own undo, and a pushed commit is undone with a new one
- **Session 4 · Virtual environments and lock files**: Declare what the project needs, lock the exact versions, and rebuild from the lock

#### [day2#review-day1] Where does HEAD point, and what does the next commit move?

*Review of Day 1*

**Question:** On `main`, someone runs `git branch notes` and then commits once. Which name moved?

- A. notes, because it is the newest branch
- B. Both main and notes
- C. main, because HEAD still points at it
- D. Neither: the commit has no branch

### Session 1: Branches, merges and conflicts

#### [day2#s1] Branches, merges and conflicts

*Session 1*

- Tell a fast-forward from a merge commit on a graph
- Read conflict markers and keep both changes where both are right
- Push, fetch and read origin/main as the hub's last known state

#### [day2#two-kinds-of-merge] If main has not moved, Git just slides it forward; if it has, Git makes a merge commit

*Two kinds of merge*

- **Fast-forward.**
  ```
  before:  o--o  main
                \
                 a--b  topic
  after:   o--o--a--b  main, topic
  ```
  No new commit; main points where topic does.
- **Merge commit.**
  ```
  before:  o--o--m  main
                \
                 a--b  topic
  after:   o--o--m---M  main
                \   /
                 a-b   topic
  ```
  M has two parents: m and b.

#### [day2#remotes] origin/main is your clone's memory of the hub, updated only when you talk to it

*Remotes*

| Command | Your `main` | `origin/main` | Working files |
| --- | --- | --- | --- |
| `git fetch` | stays | moves to the hub's | stay |
| `git merge origin/main` | moves | stays | change |
| `git pull` | moves | moves | change |
| `git push` | stays | moves to yours | stay |

`git pull` is `fetch` followed by `merge` (or rebase, if configured). Fetch first when you want to look before anything changes.

#### [day2#conflict-why] A conflict means both sides changed the same lines, and only a person knows the answer

*When Git stops*

- Git merges changes to different lines by itself
- When both sides changed the **same or touching lines**, it writes both and stops
- The merge waits, half done, until you resolve, `git add` and `git commit`
- `git merge --abort` puts everything back as it was

- **Not an error.** A conflict is a question: "both of you changed this, which text is right?" The answer is often a third text that keeps both intentions.

#### [day2#read-markers] Between the markers, the top is your branch, the bottom is the one coming in

*Reading the markers*

```
# file: visit_plan.md (during a merge)
Visits: every two weeks
<<<<<<< HEAD
Inlet cleaned at every visit, photo before and after
=======
Inlet cleaned at every visit; fan checked
>>>>>>> field-checks
```

- **A resolution that keeps both.** `Inlet cleaned at every visit; fan checked; photo before and after`
- **A resolution that loses one.** Taking one side whole (`--ours` or `--theirs`) when both changes were wanted.

#### [day2#conflict-steps] Five steps resolve any conflict

*Step by step*

1. **1 · See** `git status` lists the files
2. **2 · Read** both sides and why each changed
3. **3 · Write** the text that keeps both intentions
4. **4 · Test** no markers left; it still runs
5. **5 · Record** `git add`, `git commit`

#### [day2#check-fast-forward] What does this merge leave behind?

*Checkpoint*

**Question:** A branch `fix` has three commits. Nobody committed to `main` since `fix` started. On `main` you run `git merge fix`. What is in the history now?

- A. The same three commits; main now points at the last one
- B. Three commits and a new merge commit with two parents
- C. One new commit holding the three changes together
- D. Six commits: the three, and a copy of each on main

#### [day2#lab-2-1] Merge two branches and resolve a conflict alone

Lab 2.1 · 35 min

Addition: merge two branches into main, keep both changes on the conflicting line, push to the hub

[D2_1_merge_alone.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_1_merge_alone.html)

- [ ] Read the graph and both branches (5 min)
- [ ] Merge the first branch: a fast-forward (5 min)
- [ ] Merge the second and read the conflict markers (7 min)
- [ ] Resolve so both changes survive, and commit (10 min)
- [ ] Push to the hub, fetch, read origin/main and check the lab (8 min)
- [ ] ✱ Stretch: In a copy, rebase the second branch onto main instead and compare the graphs

### Session 2: Pull requests and review etiquette

#### [day2#s2] Pull requests and review etiquette

*Session 2*

- Open a small pull request from a branch with a title that says what changes
- Write review comments that name a line and a reason, and answer them with commits
- Resolve a conflict on your own branch before the merge

#### [day2#protected-main] On a team, main changes only through a reviewed pull request

*A team's main*

1. **1 · Branch** one change, one branch
2. **2 · Push** the branch to the host
3. **3 · Request** open a pull request with a clear title
4. **4 · Review** comments, answers, approval
5. **5 · Merge** into a protected main

> **Protected branch.** The host refuses direct pushes and merges without the required approvals (Gitea and Forgejo call it branch protection; GitLab and GitHub have the same).

#### [day2#small-requests] A small request gets a real review; a large one gets a rubber stamp

*Size*

- **One purpose** per request: "Add the rule on comment lines", not "various fixes"
- A title that says what changes; a description that says why and how to check it
- Commits that each make sense on their own
- Open it early as a draft when you want direction, not approval

- **For the reviewer.** If you cannot say in one sentence what a request changes, ask the author to split it before you review line by line.

#### [day2#good-comment] A useful comment names a line, a reason and a way forward

*Review etiquette*

| Comment | Why it helps or not |
| --- | --- |
| "Looks good" | Says nothing the author can act on |
| "This is wrong" | No line, no reason, no suggestion |
| "visit_plan.md line 6: the photo rule repeats line 2; keep one, so they cannot disagree" | Line, reason and a fix the author can accept or answer |
| "Question: is the fan check every visit or monthly?" | Marked as a question, not a demand |

#### [day2#answer-with-commit] Answer a comment with a commit on the branch, then mark it resolved

*Answering a review*

```bash
# file: terminal (the author)
git switch field-checks
# edit visit_plan.md as the comment asked
git commit -am "Keep one photo rule, as the review asked"
git push                     # the request shows the new commit
```

> **An approval belongs to a commit.** When the branch changes after an approval, the reviewer reads the new commits and approves again; hosts can be set to dismiss stale approvals.

#### [day2#update-the-branch] The author brings main into the branch and resolves the conflict there

*When the request no longer merges*

```bash
# file: terminal (the author)
git fetch origin
git merge origin/main
# resolve, then:
git add visit_plan.md
git commit
git push
```

- The author knows the change best, so the author resolves
- main never holds a half-resolved state
- The reviewer sees the resolution as a commit and reviews it
- Some teams rebase the branch instead; never rebase a branch others share

#### [day2#check-review] Which comment should the author act on first?

*Checkpoint*

**Question:** A request changes how the field team's visit plan is checked. Four comments arrive. Which is the most useful review comment?

- A. "LGTM, merging"
- B. "I don't like this approach"
- C. "While you are here, please rewrite the whole planner"
- D. "Line 12: the visit interval is set here and in the README; read it from one place"

#### [day2#lab-2-2] Branch, review and resolve a conflict in teams of three

Lab 2.2 · 35 min

Two authors and a reviewer, a protected main: two pull requests reviewed, one conflict resolved on its branch, both merged

[D2_2_team_review.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_2_team_review.html)

- [ ] Take roles; try to push to main and read the refusal (4 min)
- [ ] Authors: one branch, one commit and one pull request each (8 min)
- [ ] Reviewer comments on a line, with a reason; authors answer with a commit (9 min)
- [ ] Merge the first; the second author merges main into the branch and resolves (9 min)
- [ ] Reviewer approves the new commits; merge and check the lab (5 min)
- [ ] ✱ Stretch: Write the team's five-line review checklist and add it through a third pull request

### Session 3: Undoing mistakes

#### [day2#s3] Undoing mistakes

*Session 3*

- Choose between restore, amend, reset and revert for a given mistake
- Undo a pushed commit without rewriting what others pulled
- Recover a lost commit or branch from the reflog

#### [day2#debrief-2-2] The second request had to change after the first was merged

*Lab 2.2 debrief*

```
# file: git log --oneline --graph (the hub, from the solution run)
*   9cd2132 Merge pull request #2: Add the rule on a station's first day
|\
| *   95f7f91 Merge remote-tracking branch 'origin/main' into rules/first-day
| |\
| |/
|/|
* |   e90c3f8 Merge pull request #1: Add the rule on comment lines
```

The merge of main into the branch (95f7f91) holds the resolution the reviewer approved.

#### [day2#which-undo] Pick the undo by where the mistake is

*Undoing*

| The mistake is | Undo with | Changes history? |
| --- | --- | --- |
| in a file, not staged | `git restore file` | no |
| staged by mistake | `git restore --staged file` | no |
| in the last commit, not pushed | `git commit --amend` | yes, one commit |
| in commits not pushed | `git reset` to an earlier commit | yes |
| in a commit already pushed | `git revert` its id | no: adds a commit |

#### [day2#reset-modes] reset moves the branch; the flag decides what happens to your files

*reset, three ways*

- **--soft.** The branch moves back; the undone changes stay staged.
- **--mixed (default).** The branch moves back; the changes stay in your files, unstaged.
- **--hard.** The branch moves back; your files are made to match. Uncommitted work is lost.

> **Before --hard,** run `git status`. A file you never committed cannot come back from the reflog.

#### [day2#reflog] The reflog remembers where your branches and HEAD have been

*The safety net*

```bash
# file: terminal
git branch -D field-checks          # deleted by mistake
git reflog | head -n 5
# 4c2e9a1 HEAD@{2}: commit: Check the fan at every visit
git branch field-checks 4c2e9a1     # back
```

- Local only: each clone has its own reflog, and the hub's is not yours
- Entries expire after a while (`gc.reflogExpire`): a net, not a backup

#### [day2#check-undo] Which undo keeps everyone's clone working?

*Checkpoint*

**Question:** Yesterday you pushed a commit that set the visit interval to 90 days instead of 14. Three teammates have pulled since. How do you undo it?

- A. git reset --hard to the commit before it, then push --force
- B. git revert the commit, then push
- C. git commit --amend, then push
- D. git restore the file, then tell the team

#### [day2#lab-2-3] Undo five mistakes

Lab 2.3 · 35 min

Addition: five mistakes in one repository, each with its own undo, one of them already pushed

[D2_3_undo_five.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_3_undo_five.html)

- [ ] Read the state: status, log and what is pushed (4 min)
- [ ] Unstage a file and discard a stray change with restore (6 min)
- [ ] Drop a local commit with reset and fix the last one with amend (9 min)
- [ ] Undo the pushed commit with revert, and push (8 min)
- [ ] Bring back the deleted branch from the reflog and check the lab (8 min)
- [ ] ✱ Stretch: For each of the five, write whether the same undo is safe after a push, and why

### Session 4: Virtual environments and lock files

#### [day2#s4] Virtual environments and lock files

*Session 4*

- Explain why a project runs on one machine and fails on another
- Declare dependencies and lock them with an environment manager
- Rebuild a fresh environment from the lock and compare the output

#### [day2#it-runs-here] "It runs on my laptop" means the laptop holds something the repository does not

*Why it ran here*

- A package installed once, long ago, and never written down
- A version that happened to be current that month
- A folder that exists on one disk
- An output folder created by hand
- A Python version, a setting, a variable in a profile

- **The test.** A clean clone in a fresh environment. `uv run --isolated` builds a fresh environment from the declaration alone on your own laptop; a colleague's machine or a container gives the real thing.

#### [day2#declare-then-lock] The declaration says what is acceptable; the lock says exactly what was installed

*Two files, two jobs*

```toml
# file: pyproject.toml
[project]
name = "visit-planner"
requires-python = ">=3.11"
dependencies = [
    "tabulate>=0.9",
]
```

- **pyproject.toml**: the packages and the range of versions you accept
- **uv.lock**: every package, indirect ones included, at one exact version, with hashes
- uv's documentation calls the lock universal and says it "should be checked into version control"

#### [day2#environment] A virtual environment keeps one project's packages away from every other project

*Environments*

1. **System Python** shared by everything; never install into it
2. **.venv/ per project** its own packages, rebuilt from the lock
3. **Ignored by git** the folder is rebuilt, never committed

`uv sync` makes `.venv/` match the lock; `uv run` runs a command inside it.

#### [day2#uv-commands] Five commands take a project from undeclared to locked

*The commands*

```bash
# file: terminal
uv init --bare --name visit-planner --python 3.11   # a pyproject.toml, nothing else
uv add tabulate                                    # declare it, resolve, write uv.lock
uv python pin 3.13                                 # .python-version
uv sync --locked                                   # build .venv exactly from the lock
uv run python planner.py                           # run inside it
```

> **--locked refuses to change the lock.** uv's documentation: "If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile."

#### [day2#check-lock] What does the lock add?

*Checkpoint*

**Question:** A planner project declares `tabulate>=0.9`. A colleague installs it a year later from the declaration only and gets different output. What would a committed lock file have given them?

- A. The exact versions and hashes the author installed, indirect packages included
- B. A second list of the same package names
- C. A copy of the packages' code inside the repository
- D. The newest versions at the time of installing

#### [day2#lab-2-4] Rescue a project that fails on a second machine

Lab 2.4 · 35 min

Clone the report project as a second machine, read why it fails, then declare, lock and rebuild it to the expected output

[D2_4_second_machine.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_4_second_machine.html)

- [ ] Clone to a second machine, run it and read each failure (7 min)
- [ ] Name the causes: an undeclared package, a path on one computer, no versions (5 min)
- [ ] Declare with uv init and uv add, pin Python, lock (8 min)
- [ ] Take the data folder as an argument; rebuild fresh and compare (10 min)
- [ ] Commit pyproject.toml and uv.lock; check the lab (5 min)
- [ ] ✱ Stretch: Lock the same project with pip-tools (pip-compile --generate-hashes) and compare

#### [day2#wrap-up] Three things to keep

*Day 2 · wrap-up*

- **Small and reviewed.** One purpose per request; comments name a line and a reason; answers are commits.
- **Rewrite only what is yours.** Amend and reset before a push; revert after it.
- **Declare, lock, rebuild.** If a fresh environment from the lock does not reproduce the result, the repository is missing something.

#### [day2#next] Day 3: Rebuild anywhere, leak nothing

*Next*

Tonight, 60 minutes: choose your capstone project (`labs/capstone/BRIEF.md`), put it under Git and lock its environment. Lab 3.2 needs a container engine without administrator rights, or the provided Linux workspace: check yours.
