---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/slides/day1.html"
---

# Command Line, Git and Reproducible Environments

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
