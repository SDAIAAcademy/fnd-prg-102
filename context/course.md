---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/"
---

# Command Line, Git and Reproducible Environments

Set up work that another person can rebuild from a clean machine: shell scripts, a reviewed Git history, locked environments, a container and no secrets in history

Participants set up work that another person can rebuild from a clean machine. They script the shell, use Git with branches, pull requests and review on a shared repository, resolve a merge conflict, lock dependencies, run a project in a container without administrator rights, and keep secrets out of history.

- **Audience:** Beginners. Graduates and career changers heading for analysis, data science, data engineering or AI engineering courses, and computing graduates whose degree did not require testing, version control or reproducible environments.
- **Prerequisites:** Writes and runs a short program in Python or another language
- **Case study:** The air-quality monitoring company: A private contractor (fictional, unnamed) that runs twelve dust and particle sensor stations, ST01 to ST12, at four clients' sites in one unnamed city; its monthly client report is a Python project that only runs on the analyst's laptop. Every lab works on synthetic hourly logs for October and November 2026 generated with a fixed seed, with planted traps (comment lines, Windows line endings, duplicate lines after a logger restart, a two-day gap), and on a seeded report-portal key whose prefix is the course's own; people appear only as roles.

## Outcomes

- LO1 (Awareness): Explain how Git records history as commits, branches and remotes, and what each everyday command changes, given diagrams of a repository and sequences of commands
- LO2 (Applied): Use the shell to inspect and transform files, combining commands with pipes and a short script, given a folder of synthetic log and comma-separated files
- LO3 (Applied): Apply a branch, pull request and review workflow, including resolving a merge conflict, given a team repository with a protected main branch
- LO4 (Applied): Configure an isolated environment with locked dependencies and run the project in a container without administrator rights, given an analysis project that fails on a second machine
- LO5 (Applied): Prepare a repository that keeps secrets out of history, and carry out the response when one leaks, given a project needing an API key, with a seeded leaked key in an old commit
- LO6 (Performance): Deliver a repository that a peer reproduces on a clean machine using only its README, given the participant's own small project

## Day 1: The shell and the commit graph

Find, count and script in the shell, then draw what Git records

#### [day1#title] The shell and the commit graph

*SDAIA Academy · Command Line, Git and Reproducible Environments*

Day 1: Find, count and script in the shell, then draw what Git records

Data & AI Foundations Track · 3 teaching days + capstone day · 4 sessions · 4 labs · FND-PRG-102

#### [day1#agenda] The shell and the commit graph

*Today*

- **Session 1 · Paths and permissions**: Where you are, how a path is read, and who may read, change or run a file
- **Session 2 · Pipes, redirection and filters**: Small programs joined by pipes answer counting questions over thousands of lines
- **Session 3 · Variables, exit codes and SSH**: A script that takes its input from outside, says when it failed, and a key pair to log in elsewhere
- **Session 4 · Commits, staging and history**: A commit is a snapshot with a parent; a branch is a name that points at one

#### [day1#the-case] The monthly client report runs on one laptop only

*The case for three days*

- An **air-quality monitoring company** runs twelve dust and particle stations, **ST01 to ST12**, at four clients' sites
- Each station writes **one line an hour** to a log
- The analyst turns a month of logs into each client's report, by a Python project on their laptop
- Nobody else can rebuild it: no history, no declared packages, a key in the code

- **By the capstone day.** A peer rebuilds your own small project on a clean workspace, using only your README. Every lab practises one step of that.

> **Synthetic.** Company, clients and logs are invented; people appear as roles only.

#### [day1#setup-check] Three tools and one command prove the laptop is ready

*Setup check*

```bash
# file: terminal
git --version
bash --version | head -n 1
uv --version
git config user.name
uv run labs/kit/setup.py --to ../air-labs
cd ../air-labs && uv run lab.py list
```

- **Git** with a name and an email set (yours, or a neutral one such as `Participant A`)
- **Bash**: Git Bash on Windows, the terminal on macOS or Linux
- **uv**, from the pre-work
- The last command lists the twelve labs

> **No admin rights on your laptop?** Every lab except 3.2 runs without them; lab 3.2 also runs on the provided Linux workspace.

### Session 1: Paths and permissions

#### [day1#s1] Paths and permissions

*Session 1*

- Tell an absolute path from a relative one and predict where each points after a move
- Read a permission string and say who may read, write or run the file
- Make a script independent of the folder it is run from

#### [day1#shell-reads-a-line] The shell reads a line, splits it into words and runs the first one

*What the shell does*

1. **1 · Read** `ls -l logs`
2. **2 · Split** on spaces: `ls`, `-l`, `logs`
3. **3 · Expand** `*`, `$VAR`, `~`
4. **4 · Run** the program `ls` with two words

> **What goes wrong.** A space splits words: `cat field notes.txt` asks for two files. Quotes keep one word: `cat "field notes.txt"`.

#### [day1#where-you-are] A relative path starts where you are; an absolute one starts at the root

*Paths*

| You are in | You type | It means |
| --- | --- | --- |
| `/srv/air` | `logs/ST01.log` | `/srv/air/logs/ST01.log` |
| `/srv/air/logs` | `../stations.csv` | `/srv/air/stations.csv` |
| anywhere | `/srv/air/logs` | the same folder, always |
| anywhere | `~/notes.md` | your home folder, then `notes.md` |

Commands to know: `pwd` (where am I), `ls -a` (what is here), `cd` (go), `.` (here), `..` (one up).

#### [day1#find-and-du] find lists what matches, ls -S orders by size, du adds sizes up

*Looking round without a file browser*

```bash
# file: terminal
find visits -name '*.csv'            # every CSV under visits/, at any depth
find visits -name '*.csv' | wc -l    # how many
ls -S visits/*.csv | head -n 3       # the three largest
du -h visits                          # the size of the folder, human-readable
```

> **Quote the pattern.** `'*.csv'` in quotes reaches `find` as a pattern; without quotes the shell may expand it first, in the current folder.

#### [day1#permission-string] Ten characters say who may read, write or run a file

*Permissions*

```
# file: ls -l on Linux
-rw-r-----  1 analyst field  612 visits.csv
drwxr-xr-x  2 analyst field 4096 archive
```

| Part | In `-rw-r-----` |
| --- | --- |
| Type | `-` a file (`d` a folder) |
| Owner | `rw-` read, write |
| Group | `r--` read |
| Everyone else | `---` nothing |

- **r** read, **w** change, **x** run a file or enter a folder
- `chmod u+x run.sh` lets the owner run it as `./run.sh`
- `chmod go-r secret.env` takes reading away from group and others
- A key file is readable by its owner only

#### [day1#script-tied-to-a-folder] A script that names your folder works on your computer only

*A script that works here only*

- **Tied to one computer.**
  ```bash
  cd /mnt/share/visits
  wc -l *.csv
  ```
  Runs only where that folder exists.
- **Tied to itself.**
  ```bash
  cd "$(dirname "$0")/visits"
  wc -l *.csv
  ```
  `$0` is the script's own path; `dirname` keeps its folder.

> **Single quotes stop the substitution.** `'$(dirname "$0")'` is printed as it is; double quotes let `$( )` run and still keep spaces in one word.

#### [day1#check-paths] Which line still works after the folder moves?

*Checkpoint*

**Question:** A script `tally.sh` sits in `reports/` beside a folder `visits/`. The whole `reports/` folder is copied to a colleague's laptop. Which first line lets the script find `visits/` there, from whatever folder it is started?

- A. cd visits
- B. cd "$(dirname "$0")/visits"
- C. cd /mnt/share/reports/visits
- D. cd '$(dirname "$0")/visits'

#### [day1#lab-1-1] Find your way round the project folder

Lab 1.1 · 35 min

Addition: map the report folder, read permission strings, and fix a script that ran on one computer only

[D1_1_project_folder.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_1_project_folder.html)

- [ ] Start the lab and see where you are: pwd, ls -a (4 min)
- [ ] Map the logs with find, ls -S and du (8 min)
- [ ] Read the permission strings of listing.txt and answer in answers.md (8 min)
- [ ] Fix run_counts.sh: its own folder, and quotes round a folder name with a space (10 min)
- [ ] Run it from the workspace folder and check the lab (5 min)
- [ ] ✱ Stretch: On a Linux workspace, chmod u+x the script, run it as ./run_counts.sh, and say why bash never needed that

### Session 2: Pipes, redirection and filters

#### [day1#s2] Pipes, redirection and filters

*Session 2*

- Chain head, grep, cut, sort, uniq and wc into a pipeline that answers one question
- Redirect output and errors to files
- Find a hidden character or a repeated line that skews a count

#### [day1#three-streams] Every program has one input and two outputs

*Streams*

- **stdin (0).** What the program reads: the keyboard, a file after `<`, or the previous program after `|`.
- **stdout (1).** The result. `>` writes it to a file, `>>` adds to the end, `|` hands it on.
- **stderr (2).** Errors and progress. `2>` sends them to a file; they do not go down a pipe.

```bash
# file: terminal
wc -l visits/*.csv > lines.txt 2> errors.txt
```

#### [day1#small-tools] Six small programs cover most counting questions

*The filters*

| Command | Does one thing |
| --- | --- |
| `grep 'ERR'` · `grep -v '^#'` | keeps the lines that match · that do not match |
| `cut -d' ' -f2` | keeps field 2 of each line, fields split by a space |
| `sort` · `sort -rn` | orders lines · by number, largest first |
| `uniq -c` · `uniq -d` | counts runs of equal neighbours · prints each repeated line once |
| `wc -l` · `grep -c .` | counts lines · counts lines that are not empty |
| `head -n 3` · `tail -n +2` | the first three lines · everything from line 2 (skip a header) |

#### [day1#pipeline-built-up] Add one stage, look at the output, then add the next

*Build it one stage at a time*

```bash
# file: terminal
cat visits.log | head -n 3                           # 1 · look first
grep -v '^#' visits.log | head -n 3                  # 2 · drop comments
grep -v '^#' visits.log | cut -d' ' -f3 | head -n 3  # 3 · keep the technician code
grep -v '^#' visits.log | cut -d' ' -f3 | sort | uniq -c | sort -rn | head -n 3
```

> **Read a pipeline left to right** as a sentence: "lines that are not comments, their third field, sorted, counted, largest count first, top three".

#### [day1#sort-before-uniq] uniq only sees neighbours, so sort first

*The rule people forget*

- **Without sort.**
  ```
  T1
  T2
  T1
  $ uniq -c
    1 T1
    1 T2
    1 T1
  ```
- **With sort.**
  ```
  $ sort | uniq -c
    2 T1
    1 T2
  ```

#### [day1#hidden-characters] A file written on Windows ends each line with an extra character

*What you cannot see*

- Linux and macOS end a line with **LF**; Windows programs often write **CR LF**
- The CR sticks to the last field: `OK` and `OK\r` are two words to `sort`
- `cat -A` (`cat -e` on macOS) shows it as `^M`; `file` names the line endings
- `tr -d '\r'` removes it

- **The same pipeline, two answers.** Git Bash's `grep` on Windows drops the CR from its output; `grep` on Linux keeps it. A pipeline can be right on one machine and wrong on the next: the theme of the whole course.

#### [day1#script-it] A pipeline you will run again belongs in a script

*Keep the pipelines*

```bash
# file: visit_counts.sh
#!/usr/bin/env bash
# Counts over the field visits. Run: bash visit_counts.sh > visit_counts.txt

echo "== V1 visit lines (no comments)"
grep -v '^#' visits.log | grep -c .

echo "== V2 visits per technician"
grep -v '^#' visits.log | cut -d' ' -f3 | sort | uniq -c
```

> **The echo lines are labels.** They make the output readable by a person and by a check.

#### [day1#check-uniq] Why does the count list one technician twice?

*Checkpoint*

**Question:** On a colleague's Linux machine, `cut -d' ' -f4 visits.log | sort | uniq -c` prints `12 T2` and, further down, `3 T2`. Field 4 is the last field. What is the most likely cause?

- A. sort did not group the lines
- B. uniq -c counts each run twice
- C. cut took the wrong field
- D. Some lines end in CR LF, so one T2 carries an invisible CR

#### [day1#lab-1-2] A counting pipeline over synthetic logs

Lab 1.2 · 35 min

Six counts over twelve stations' October logs, one pipeline each, kept in counts.sh

[D1_2_counting_pipeline.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_2_counting_pipeline.html)

- [ ] Look at the logs: head, tail, wc -l (4 min)
- [ ] Count the reading lines without comments or blank lines (Q1) (5 min)
- [ ] Lines per status, and the carriage-return trap (Q2) (8 min)
- [ ] The three stations with most errors, and each error code (Q3, Q4) (8 min)
- [ ] Duplicate lines after a restart, and stations per client from the CSV (Q5, Q6) (6 min)
- [ ] Save the output to counts.txt and check the lab (4 min)
- [ ] ✱ Stretch: Alert hours (PM10 above 150) per station with awk, each hour counted once

### Session 3: Variables, exit codes and SSH

#### [day1#s3] Variables, exit codes and SSH

*Session 3*

- Pass a folder as an argument with an environment variable as the fallback
- Make a script stop with a non-zero exit code and a message on stderr
- Create an SSH key pair, read its fingerprint and write a host entry

#### [day1#debrief-1-2] Seven lines in October were not readings, and one log hid a character

*Lab 1.2 debrief*

- **8,892** reading lines out of 8,899 in October
- **735** OK lines of ST07 that end in CR LF
- **12** lines sent twice after two logger restarts

Status counts once the CR is removed: OK 8,728 · WARN 103 · ERR 61. Most errors: ST05 (26), ST09 (17), ST12 (8).

#### [day1#arguments] A script takes its folder as an argument, with a variable as the fallback

*Input from outside*

```bash
# file: visit_counts.sh
DIR="${1:-${VISITS_DIR:-}}"     # the first argument, else $VISITS_DIR, else empty
grep -v '^#' "$DIR"/visits.log | grep -c .
```

| You run | `DIR` is |
| --- | --- |
| `bash visit_counts.sh march` | `march` |
| `VISITS_DIR=april bash visit_counts.sh` | `april` |
| `bash visit_counts.sh` (no variable set) | empty: stop and say so |

#### [day1#exit-codes] Every command ends with a number: 0 means it worked

*Did it work?*

```bash
# file: terminal
grep -q T9 visits.log; echo $?  # 1: no match
ls nowhere; echo $?     # 2: an error
false | true; echo $?   # 0: last counts
set -o pipefail
false | true; echo $?   # 1: any failure
```

- `$?` holds the code of the last command
- **set -e** stops the script at the first failing command
- **set -u** stops on a variable that was never set
- **set -o pipefail** makes a pipeline fail when any stage fails

> **Pick your own code for "bad input".** Many tools use 2; say it in the script's usage line.

#### [day1#fail-clearly] Stop early, say what is missing on stderr, and return a non-zero code

*A clear failure*

```bash
# file: visit_counts.sh
#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-${VISITS_DIR:-}}"
if [ -z "$DIR" ] || [ ! -f "$DIR/visits.log" ]; then
  echo "usage: bash visit_counts.sh <folder> (or set VISITS_DIR)" >&2
  exit 2
fi
```

> **Why it matters for reproduction.** A peer following your README sees "set VISITS_DIR" instead of an empty result that looks like zero visits.

#### [day1#ssh-key-pair] An SSH key pair: the public half opens the door, the private half never leaves you

*Remote login*

1. **1 · Make** `ssh-keygen -t ed25519` writes `key` and `key.pub`
2. **2 · Give** the `.pub` file to the server or the Git host
3. **3 · Prove** the server checks a signature made with the private key
4. **4 · Check** compare fingerprints: `ssh-keygen -lf key.pub`

> **The private key is a secret.** Protect it with a passphrase, readable by you only, never in a repository.

#### [day1#ssh-config] One entry in a config file saves typing and picks the right key

*A host entry*

```
# file: ssh_config
Host field-server
    HostName 198.51.100.7
    User technician
    IdentityFile keys/field_key
    IdentitiesOnly yes
```

`ssh -F ssh_config field-server` now logs in as `technician` with that key only. `192.0.2.0/24` and `198.51.100.0/24` are address ranges reserved for examples.

#### [day1#check-exit-code] What does the caller see?

*Checkpoint*

**Question:** A script without `set -o pipefail` ends with `grep -h ERR "$DIR"/*.log | wc -l`. `DIR` names a folder that does not exist. What exit code does the script return, and what does it print?

- A. 0, after printing 0 and an error from grep on stderr
- B. 2, the code of the failed grep
- C. 1, and it prints nothing at all
- D. The script stops before wc runs

#### [day1#lab-1-3] The counting script on a second folder, and a practice key

Lab 1.3 · 35 min

Addition: the counting script runs unchanged on November and fails clearly; then a practice SSH key and host entry

[D1_3_second_folder_key.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_3_second_folder_key.html)

- [ ] Take the folder as $1, with AIR_LOGS as the fallback (8 min)
- [ ] Stop with exit code 2 and a message on stderr; set -euo pipefail (7 min)
- [ ] Run it unchanged on the November folder (5 min)
- [ ] Make a practice Ed25519 key pair in keys/ and save its fingerprint (6 min)
- [ ] Write the ssh_config entry and check the lab (9 min)
- [ ] ✱ Stretch: Log in to the provided Linux workspace with the key and run counts.sh there

### Session 4: Commits, staging and history

#### [day1#s4] Commits, staging and history

*Session 4*

- Draw the commit graph that a sequence of commands produces
- Tell what is changed, what is staged and what is committed
- Read git log --graph and match it to a drawing

#### [day1#three-places] A change moves through three places: the folder, the staging area, the history

*Where a change lives*

1. **Working folder** files as you edit them
2. **Staging area** `git add` picks what the next commit holds
3. **History** `git commit` records a snapshot

| Command | Compares |
| --- | --- |
| `git diff` | working folder with the staging area: what is not staged |
| `git diff --staged` | staging area with the last commit: what the next commit holds |
| `git status --short` | both, one line per file |

#### [day1#commit-is-snapshot] A commit is a snapshot with a parent, an author, a message and an id

*What a commit is*

- The **snapshot**: every tracked file as it was
- The **parent**: the commit it follows (two for a merge)
- The **id** is a hash of all of it: change anything, get a new id
- So history is a chain you can check, and rewriting it changes every id after the change

```bash
# file: terminal
git log --format='%h %p %s'
# id      parent   message
```

#### [day1#branch-is-pointer] A branch is a name that points at one commit, and HEAD says which name you are on

*What a branch is*

```
# file: a graph
o---o---o   <- main <- HEAD
         \
          o   <- draft
```

- Pro Git calls a branch "a lightweight movable pointer" to a commit
- A new commit moves the branch HEAD points at, and only that one
- Creating a branch writes one small reference: it is cheap
- `git switch draft` moves HEAD; the next commit moves `draft`

#### [day1#draw-a-sequence] Draw first, run second, compare third

*Worked example*

```bash
# file: sequence
git commit -m "A"        # on main
git branch notes
git commit -m "B"        # still on main
git switch notes
git commit -m "C"
```

```
# file: the graph
        B   <- main
       /
o--A--+
       \
        C   <- notes <- HEAD
```

main reaches 3 commits (the first, A, B); notes reaches 3 (the first, A, C); 4 commits in all.

#### [day1#read-log-graph] git log --graph draws the same graph on its side

*Reading Git's drawing*

```bash
# file: terminal
git log --oneline --graph --all
* 3c1d0e2 (HEAD -> notes) C
| * 9b7a4f1 (main) B
|/
* 5e2a8c3 A
* 1f0b6d9 First commit
```

- Newest at the top; each `*` is a commit; the lines are parent links
- `--all` shows every branch, not only the one you are on

#### [day1#check-graph] How many commits does main reach?

*Checkpoint*

**Question:** A new repository gets one commit on `main`. Then: `git branch fix`, two commits on `main`, `git switch fix`, one commit. How many commits does `main` reach, and how many does the repository hold?

- A. main 4, the repository 4
- B. main 2, the repository 3
- C. main 3, the repository 4
- D. main 3, the repository 5

#### [day1#lab-1-4] Draw the graph, then check it

Lab 1.4 · 35 min

Addition: predict the graphs of three command sequences on paper, run them, compare with git log --graph

[D1_4_draw_the_graph.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_4_draw_the_graph.html)

- [ ] Predict, then run sequence 1 (6 min)
- [ ] Compare with git log --graph and correct your drawing (4 min)
- [ ] Sequence 2: stage one change of two and read both diffs (9 min)
- [ ] Sequence 3: a branch that moves while main moves too (10 min)
- [ ] Answer the four questions and check the lab (6 min)
- [ ] ✱ Stretch: Predict what git commit --amend does to your drawing, then try it and compare the ids

#### [day1#wrap-up] Three things to keep

*Day 1 · wrap-up*

- **Paths travel badly.** A script finds its files from its own folder and takes data folders as arguments.
- **Look at every stage.** Build pipelines one stage at a time; a hidden character or a repeat changes the count.
- **History is a graph.** Commits point to parents; branches and HEAD are names that point to commits.

#### [day1#next] Day 2: Working together on one history

*Next*

Tonight, 30 minutes: the commit-graph practice in `labs/practice/commit_graphs.md`, drawn on paper. Bring a laptop with the workspace; unfinished labs can be finished at home with `uv run lab.py check`.

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

## Day 3: Rebuild anywhere, leak nothing

One documented command, a container with mounted data, and keys kept out of history

#### [day3#title] Rebuild anywhere, leak nothing

*SDAIA Academy · Command Line, Git and Reproducible Environments*

Day 3: One documented command, a container with mounted data, and keys kept out of history

Data & AI Foundations Track · 3 teaching days + capstone day · 4 sessions · 4 labs · FND-PRG-102

#### [day3#agenda] Rebuild anywhere, leak nothing

*Today*

- **Session 1 · One command to rebuild and run**: A reader rebuilds the result with one documented command, and the repository holds code, not data or outputs
- **Session 2 · Images, containers and volumes**: An image is built once from a short definition; each run is a container that sees only what you mount
- **Session 3 · What a container shares**: A container shares the kernel, the mounts and every variable you pass it; a key belongs in the environment, never in the code
- **Session 4 · Scanning, and after a leak**: Scan before every commit; after a leak, rotate first, then clean the history and report

#### [day3#review-day2] Which command leaves your own main where it was?

*Review of Day 2*

**Question:** A teammate pushed to the hub. You want to see their commits before anything in your clone changes. Which command?

- A. git pull
- B. git merge origin/main
- C. git push
- D. git fetch

#### [day3#debrief-2-4] The second machine failed four times before the lock fixed it

*Lab 2.4 debrief*

| Attempt | Last line of the error |
| --- | --- |
| Nothing installed | `ModuleNotFoundError: No module named 'dateutil'` |
| With requirements.txt | the same: the file listed tabulate only |
| With both packages | `FileNotFoundError` on the analyst's absolute path |
| With the path fixed | `FileNotFoundError` on `output/report.csv` |
| From the lock, fresh | 12 stations written; checksum as expected |

### Session 1: One command to rebuild and run

#### [day3#s1] One command to rebuild and run

*Session 1*

- Keep data and outputs out of the repository and say where they come from
- Write one documented command that rebuilds and checks the result
- Test a README by following it in a clean clone

#### [day3#what-belongs] Code and the recipe go in; data, outputs and environments stay out

*What a repository holds*

- **In the repository.** Source, `pyproject.toml` and the lock, the container definition, the rebuild command, the README, small expected checksums, a `.env.example`.
- **Out of it.** Raw data (it has its own home and its own rules), outputs (rebuilt), `.venv/` (rebuilt), `.env` (secret), caches.

> **.gitignore does not untrack.** A file already committed stays tracked until `git rm --cached` removes it from the index.

#### [day3#data-path-outside] The code asks where the data is; the README says where to get it

*Where the data comes from*

```python
# file: planner.py
ap.add_argument("--data", default=os.environ.get("VISITS_DIR"))
...
if not args.data:
    print("error: give --data <folder> or set VISITS_DIR", file=sys.stderr)
    return 2
```

- No default path that exists on one computer only
- A clear stop beats a silent empty result

#### [day3#one-command] One documented command rebuilds, runs and checks

*One command*

```bash
# file: rebuild.sh (a field-visit planner)
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${VISITS_DIR:?set VISITS_DIR to the folder of visit logs}"
uv sync --locked --quiet
uv run --quiet python planner.py --data "$VISITS_DIR" --out output
sha256sum -c expected/march.sha256
```

> **The last line is the test.** `sha256sum -c` prints `OK` or `FAILED` and sets the exit code.

#### [day3#checksum] A checksum turns "it ran" into "it gave the same bytes"

*Did it reproduce?*

- Running without an error proves little: an empty input also runs
- A checksum of the expected output, committed, is a precise answer
- When it fails, compare the first rows to see where the difference starts
- Outputs that hold a date or a random number need those fixed first

**64** hexadecimal characters in a SHA-256 checksum: one changed byte changes them all

#### [day3#readme-reproduce] A Reproduce section answers four questions and assumes nothing

*The README*

- **The four answers.**
  - Which tools, and which versions at least
  - Where the data comes from
  - The one command
  - What success looks like
- **What a peer cannot know.**
  - A folder on your laptop
  - A package you installed once
  - A variable in your shell profile
  - A step you always do without thinking

#### [day3#check-data-path] Where does the data path belong?

*Checkpoint*

**Question:** A planner project reads its visit logs from a folder. A peer will rebuild it on a clean workspace. Where should the folder's location come from?

- A. A default path in the code, the author's own folder
- B. An argument or a variable, with the README saying where to get the data
- C. The repository itself, in a data/ folder
- D. A chat message to the peer before the rebuild

#### [day3#lab-3-1] One command, and data kept out of the code

Lab 3.1 · 35 min

Addition: data and output out of the repository, one rebuild command with a checksum, a README tested in a clean clone

[D3_1_one_command.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_1_one_command.html)

- [ ] List what the repository carries with git ls-files (4 min)
- [ ] Stop tracking data and output: git rm --cached and .gitignore (7 min)
- [ ] Write rebuild.sh: sync the lock, run, compare with the expected checksum (9 min)
- [ ] Write the README's Reproduce section (6 min)
- [ ] Clone to a clean folder, follow the README only, and check the lab (9 min)
- [ ] ✱ Stretch: Make rebuild.sh print the versions it ran with, for the reproduction log

### Session 2: Images, containers and volumes

#### [day3#s2] Images, containers and volumes

*Session 2*

- Tell an image from a container and a layer from a mount
- Write a short container definition that installs from the lock
- Run a container without administrator rights with data mounted read-only

#### [day3#image-container] An image is a packed file system; a container is one run of it

*Two words*

- **Image.** Built once from a definition: a base system, your packages, your code, in layers. Read-only.
- **Container.** A process started from an image, with a thin writable layer that disappears with `--rm`.
- **Volume or bind mount.** A folder from outside, mounted in: where data comes in and results go out.

> **It is still a process.** Docker's own explanation: "every container on a machine shares that machine's kernel".

#### [day3#containerfile] Six instructions describe the whole image

*A short definition*

```dockerfile
# file: Containerfile (a field-visit planner)
FROM docker.io/library/python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY planner.py .
ENTRYPOINT ["python", "planner.py", "--data", "/data"]
```

- `requirements.txt` is exported from the lock, with hashes: `uv export --frozen --format requirements.txt`
- Packages before code: a code change reuses the cached package layer

#### [day3#layers] Each instruction is a layer, rebuilt only when it or one above it changes

*Layers and the cache*

1. **FROM** the base image, pulled once
2. **COPY requirements.txt, RUN pip install** changes when the lock changes
3. **COPY planner.py** changes with every code edit

#### [day3#mounts] Mount the input read-only and the output writable

*Data in, results out*

```bash
# file: terminal
podman run --rm \
  -v "$PWD/visits:/data:ro" \
  -v "$PWD/output:/out" \
  visit-planner
```

- The image never holds the data, so one image serves every month
- `:ro` means a bug cannot change the raw logs (Docker: "prevent the container from writing to the mount")
- Results appear on your disk because `/out` is your folder

#### [day3#rootless] A rootless engine runs containers as you, inside a range of user ids lent to you

*No administrator rights*

- **Podman** is rootless by design; it needs a range of user ids for you in `/etc/subuid` and `/etc/subgid`
- **Docker rootless mode** runs the daemon and containers as a non-root user
- "root" inside the container is your own user outside, not the machine's root
- `podman run --userns=keep-id` maps your user id to the same id inside

- **On the provided workspace.** The trainer has set up the user id ranges and pulled the base image. On a laptop without administrator rights, this is the place to do lab 3.2.

#### [day3#check-mount] Why does the report appear on your disk?

*Checkpoint*

**Question:** You run the planner image with `-v "$PWD/output:/out"` and `--rm`. The container is gone afterwards, yet `output/plan.csv` is on your disk. Why?

- A. --rm copies the container's files out before deleting it
- B. The file was written into the image
- C. /out inside the container is your own output/ folder, mounted
- D. The engine syncs every container folder back to the host

#### [day3#lab-3-2] Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace

Lab 3.2 · 35 min

Complete a container definition that installs from the lock, build it rootless, run it on read-only logs

[D3_2_container.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_2_container.html)

- [ ] Check the engine runs without administrator rights (4 min)
- [ ] Export the lock as hashed requirements (5 min)
- [ ] Fill the five numbered gaps of the Containerfile (10 min)
- [ ] Build the image (6 min)
- [ ] Run it with the logs mounted read-only and the output mounted; compare and check (10 min)
- [ ] ✱ Stretch: Change report.py, rebuild, and see which layers are rebuilt

### Session 3: What a container shares

#### [day3#s3] What a container shares

*Session 3*

- Name what a container shares with its host
- Read a key from the environment and stop clearly when it is missing
- Keep the key out of the output and the repository, with an example file in its place

#### [day3#not-isolated] A container isolates a process, not everything around it

*What a container shares*

| Shared with the host | What it means |
| --- | --- |
| The kernel | A kernel flaw reaches every container; it is not a virtual machine |
| Every mounted folder | The container can read, and without `:ro` change, what you mount |
| Every variable you pass | `--env-file .env` hands the key to whatever runs in the image |
| The network, by default | The program can reach what your machine can reach |
| The image's contents | Anyone with the image can read a key that was copied into it |

#### [day3#key-in-code] A key in the code travels with every copy of the code

*The key in the code*

- **Where it goes.**
  - Every clone and every fork
  - Every backup and every image built from it
  - A screenshot of the editor in a chat
  - An assistant you pasted the file into
- **Where it belongs.**
  - The environment of the process that needs it
  - A `.env` file that git ignores, on one machine
  - The host's or the workplace's secret store

#### [day3#read-from-env] Read the key from a variable, stop clearly without it, and never print it whole

*Reading it from the environment*

```python
# file: planner.py
def booking_key() -> str:
    key = os.environ.get("VISITS_BOOKING_KEY", "")
    if not key:
        print("error: set VISITS_BOOKING_KEY (see .env.example)", file=sys.stderr)
        raise SystemExit(2)
    return key

key = booking_key()
print(f"booking with the key ending ...{key[-4:]}")
```

#### [day3#env-example] .env holds the value and stays home; .env.example holds the name and is committed

*Two files*

```
# file: .env.example (committed)
VISITS_BOOKING_KEY=
```

```
# file: .gitignore (committed)
.env
.env.*
!.env.example
```

```bash
# file: terminal
git check-ignore -v .env                   # proves the rule matches
uv run --env-file .env python planner.py   # loads .env for this run only
```

#### [day3#check-env-file] What does --env-file still expose?

*Checkpoint*

**Question:** You run a planner image with `--env-file .env`; the key is no longer in the code or the image. Who can still read the key?

- A. Any program running in that container, and anyone who can inspect it
- B. Nobody: variables passed at run time are encrypted
- C. Anyone who pulls the image from the registry
- D. Nobody, because /data is mounted read-only

#### [day3#lab-3-3] The key out of the code

Lab 3.3 · 35 min

Addition: move the portal key from the code to the environment, with .env.example committed and the key masked

[D3_3_key_out_of_code.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_3_key_out_of_code.html)

- [ ] Find the key in the code and in the output of a run (5 min)
- [ ] Read it from AIR_PORTAL_KEY; stop with exit 2 when it is missing (10 min)
- [ ] Write .env.example, keep .env ignored, run with uv run --env-file (8 min)
- [ ] Print only the key's last four characters (5 min)
- [ ] Commit, find the key still in history with git log -S, and check the lab (7 min)
- [ ] ✱ Stretch: Run the container with --env-file .env and list what it can see

### Session 4: Scanning, and after a leak

#### [day3#s4] Scanning, and after a leak

*Session 4*

- Run a secret scan over files, staged changes and the whole history
- Carry out the leak response in order: rotate, clean, report
- Install a commit hook that refuses a commit holding a key

#### [day3#three-scans] Scan three places: the files, the next commit, and the whole history

*Scanning*

- **Files.** What is in the folder now. Clean files can still have a dirty history.
- **The next commit.** A hook runs the scan on staged changes and refuses the commit.
- **The history.** Every commit on every branch: what anyone who clones can read.

Tools: gitleaks (`gitleaks git` scans a repository's history), run from pre-commit; hosts add their own: GitHub push protection "blocks pushes that contain secrets", GitLab has secret push protection.

#### [day3#custom-rule] Default rules know public key formats; your own keys need your own rule

*Rules*

```toml
# file: .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "booking-service-key"
description = "Key of the visit booking service"
regex = '''vbk_[a-z]+_[0-9a-f]{24}'''
keywords = ["vbk_"]
```

#### [day3#hook] A pre-commit hook stops the key before it enters history

*Before each commit*

```yaml
# file: .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: secret-scan
        name: secret scan
        entry: uv run --no-project python tools/scan_secrets.py --staged
        language: system
        pass_filenames: false
```

- `uvx pre-commit install` once per clone; every `git commit` then runs the scan
- A hook lives in your clone only: the host's push protection is the second net

#### [day3#leak-order] Rotate first, then clean the history, then report

*After a leak*

1. **1 · Rotate** revoke the key where it was issued; issue a new one
2. **2 · Clean** rewrite every commit that holds it; force-push
3. **3 · Tell** the key's owner and the data protection officer; check the access log
4. **4 · Prevent** the hook, the rule, push protection

> **Why rotation comes first.** GitHub's guidance: "as a first step you need to revoke and/or rotate that secret". Cleaning cannot reach the copies already made.

#### [day3#filter-repo] git filter-repo replaces the value in every commit, and every id after it changes

*Cleaning the history*

```bash
# file: terminal (a field-visit planner)
printf '%s==>REMOVED\n' "$OLD_KEY" > ../replacements.txt    # outside the repository
uvx git-filter-repo --replace-text ../replacements.txt --force
git remote add origin <the hub>          # filter-repo removes it on purpose
git push --force origin main
```

- "Rewriting history will change the hashes of the commits" (GitHub): every teammate clones again
- The scan of the whole history must come back clean, on your clone and on the hub

#### [day3#check-leak] What do you do first?

*Checkpoint*

**Question:** A scan of the planner's history finds a booking-service key in a commit from three weeks ago. The repository has been public since. What is the first action?

- A. Rewrite the history with git filter-repo
- B. Delete the file in a new commit
- C. Make the repository private
- D. Revoke the key at the booking service and issue a new one

#### [day3#lab-3-4] Remediate a seeded leaked key with a scanner and a commit hook

Lab 3.4 · 35 min

A key leaked in an old commit: scan, rotate, write the note, clean the history, and add a hook that blocks the next one

[D3_4_leaked_key.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_4_leaked_key.html)

- [ ] Scan the whole history and find the key (5 min)
- [ ] Rotate first: revoke the old key and issue a new one into .env (7 min)
- [ ] Write ROTATION.md (6 min)
- [ ] Clean the history with git filter-repo, force-push, scan again (10 min)
- [ ] Install the hook, see it block a key, and check the lab (7 min)
- [ ] ✱ Stretch: Run gitleaks with .gitleaks.toml, or the host's push protection, and compare

#### [day3#capstone-kickoff] Tomorrow a peer rebuilds your project from its README alone

*Capstone kickoff*

- Your own small project, on synthetic or public data
- A README with a Reproduce section, a lock file, a container definition, a clean scan of the history
- Your peer follows only the README, on a clean workspace, and logs every step
- Then you fix every step they could not follow; they reproduce it again

- **Tonight, 60 minutes.** Run your own rebuild in a fresh clone, then read your README as a stranger would. The brief and the checklist: `labs/capstone/`.

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **One command.** A reader rebuilds and checks the result with one documented command; data and outputs live elsewhere.
- **A container is a process.** It shares the kernel, the mounts and the variables you give it.
- **Rotate, clean, tell.** A leaked key is revoked first; then history, then the people who need to know.

#### [day3#next] The capstone day: peer reproduction

*Next*

Bring your repository link and its README. The supervised check on shell commands and commit graphs opens the day, AI off.

## Capstone: Capstone: peer reproduction

A peer rebuilds your repository from its README on a clean workspace; then a short oral on one failed step

#### [capstone#title] Capstone: peer reproduction

*SDAIA Academy · Command Line, Git and Reproducible Environments*

Capstone: A peer rebuilds your repository from its README on a clean workspace; then a short oral on one failed step

Data & AI Foundations Track · 3 teaching days + capstone day · 3 min talk and demo · 4 min Q&A · FND-PRG-102

#### [capstone#agenda] A peer rebuilds your project from its README alone

*Capstone*

- **Supervised check, AI off**: shell commands and five commit graphs
- **Rubric, pairs and a self-test**: your own rebuild in a fresh clone, one last time
- **Peer reproduction**: on a clean workspace, following only the README, logging every step
- **Log, handback and fix clinic**: the log as a pull request; you start fixing what failed
- **Trainer review, then the follow-up**: a second reproduction and a seven-minute oral

#### [capstone#check] Supervised check · 45 minutes

*Assessment · AI off*

Paper only: no laptop, no assistant. Shell commands, then five commit graphs to draw.

#### [capstone#rubric] The rubric, out of 100

*How the peer reproduction is scored*

| Item | Value |
| --- | --- |
| **README**: tools, data source, one command | 20% |
| **Clean rebuild** on the peer's workspace | 30% |
| **Container**: locked, rootless, mounted data | 15% |
| **Hygiene**: no secret or data in history | 15% |
| **History**: reviewed pull requests | 10% |
| **Follow-up**: second reproduction passes | 10% |

#### [capstone#pairs] You reproduce one peer's project; a different peer reproduces yours

*Pairs*

- Pairs run in a ring: A reproduces B, B reproduces C, and so on, so no two people check each other
- The reproducer works on a clean workspace, never on the author's laptop
- The author does not help during the reproduction: the README speaks for them

- **Self-test first, 35 minutes.** Clone your own repository into an empty folder, follow your README word for word, and fix what you find. After this, no more commits until the handback.

#### [capstone#running-order] Who reproduces whom

*Running order*

| # | Author | Reproduced by |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Self-test · 35 minutes

*Before the reproduction*

Clone your own repository into an empty folder and follow the README word for word. Then post the commit id.

#### [capstone#reproduce-flow] Follow the README exactly, and write down every step as it happened

*The peer reproduction · 150 minutes*

1. **Clone** the commit the author posted, on a clean workspace
2. **Rebuild** the one command; does the checksum match?
3. **Container** build and run, data mounted read-only
4. **Scan** the whole history, and look for committed data

> **Do not repair it for them.** When a step fails, record the exact command and the last line of the error, then try the smallest guess and record that too.

#### [capstone#reproduce-timer] Reproduce · 150 minutes

*Peer reproduction*

Only the README. Log every step. Ask the trainer, never the author.

#### [capstone#handback] The log arrives as a pull request, and the author merges it after review

*Log and handback · 40 minutes*

- The reproducer adds `reproduction/peer-1.md` on a branch and opens a pull request
- The author reviews it: questions in comments, no edits to the peer's findings
- Merged by pull request, the log is part of the history the rubric reads

- **Fix clinic, 70 minutes.** Each author starts on the failed steps, one small commit per fix, each through a pull request. The trainer takes questions at the front.

#### [capstone#format] Seven minutes: three on one failed step and its fix, four of questions

*After the follow-up · the oral*

- **1 · What failed.** The step from the peer's log, and the last line of the error.
- **2 · Why.** What the README assumed that the clean workspace did not have.
- **3 · The fix.** The commit that fixed it, and the line of the second log that proves it.

> **Your own words.** The capstone is AI-full: you may have used an assistant, and you explain every step yourself.

#### [capstone#now-presenting] Talk

*Now presenting*

##### Questions

#### [capstone#review] What the reproductions showed

*Trainer review*

- **What rebuilt first time.** The habits behind the projects that reproduced at once.
- **The common failures.** The steps most READMEs left out.
- **One surprise.** Something nobody expected to fail.

#### [capstone#what-next] Keep going

*After the course*

- **Your project stays yours:** finish the follow-up, then keep every new project rebuildable from its README
- **Next Academy courses:** FND-PRG-104 Software Testing, Code Review and Documentation; FND-PRG-105 Computer Systems and Cloud Essentials for AI Work; and DEV-SWE-201 Software Engineering with Coding Agents, which all build on this one

#### [capstone#thanks] Thank you

*SDAIA Academy*

Command Line, Git and Reproducible Environments
