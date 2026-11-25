# Answer key for the labs

The answers to each lab's questions and its "Check yourself" list. The numbers come from the
solution scripts in this folder, run on the course's synthetic data when the course was built
(`run_all.sh`: every starting state failed its check and every solution passed). Lab solutions
are public on purpose: the labs are practice. The supervised check, its key and the oral
questions are not in this repository.

Each lab also has a "Who does what" line. In this course the person who makes a change is never
the only person who accepts it: the reviewer approves a pull request, the key's owner revokes a
key, a peer reproduces a capstone. The line names that split for each lab.

## 1.1 Find your way round the project folder (addition)

Answers in `answers.md`: 12 November log files; the largest October log is ST07 (its lines end in
CRLF, one byte more per line); `notes.txt` is writable by every user; `make_report.sh` has no `x`
bit, fixed with `chmod u+x make_report.sh`; `portal.env` is readable by its owner only.

1. The original script breaks on its `cd` to a fixed folder on one machine and on the unquoted
   path with a space. The fixed script uses `cd "$(dirname "$0")/..."` and quotes, so moving the
   whole folder breaks nothing.
2. Unquoted, the shell splits it at the space into two words, `field` and
   `notes/visit-checklist.txt`, and the command looks for two files that do not exist.
3. Only its owner (`-rw-------`). A key in a file anyone can read is a key anyone on the machine
   can copy.

Who does what: the workspace owner sets permissions on files holding keys; other users of the
machine read the shared files and nothing else.

## 1.2 A counting pipeline over synthetic logs (entry lab)

October answers: Q1 8,892 reading lines. Q2 OK 8,728, WARN 103, ERR 61. Q3 ST05 26, ST09 17,
ST12 8. Q4 E11 8, E21 26, E34 11, E40 16. Q5 12 duplicate lines (the restart of ST03). Q6 three
stations for each of the four clients. Without `tr -d '\r'`, Q2 counts the ST07 statuses apart
(`OK` 7,993 and `OK^M` 735; `WARN` 94 and 9).

1. `uniq -c` counts runs of equal neighbouring lines; only sorted input puts equal lines together.
2. Line endings: ST07 ends in CRLF. Git Bash's `grep` drops the carriage return in its output and
   Linux's does not, so the status field holds `OK\r` on Linux. `tr -d '\r'` makes both agree.
3. `>` replaces the file each run; `>>` appends, so a second run doubles every answer.

Who does what: the analyst writes the counts; a second person runs the unchanged script on their
own copy before the counts go into a client report.

## 1.3 The counting script on a second folder, and a practice key (addition)

November answers from the same script, unchanged: Q1 8,646. Q2 OK 8,523, WARN 78, ERR 45. Q3
ST05 18, ST09 14, ST12 8. Q4 E11 6, E21 20, E34 10, E40 9. Q5 6. Q6 three per client.

1. Without `pipefail`, `$?` is the status of the last command, usually 0, so the failure is
   hidden. With `pipefail`, it is the status of the last command that failed, non-zero.
2. Standard output is the result and may be redirected to a file; an error on standard error
   still reaches the person at the terminal and does not corrupt the result file.
3. The `.pub` file may be pasted into a host's form; the private key never leaves the machine.

Who does what: the participant generates the key pair; the host's administrator registers the
public key. Neither ever handles the private key of the other.

## 1.4 Draw the graph, then check it (addition)

Answers in `graphs.md`: 3, 5, 7, main.

1. New files that were never added: `-a` stages changes to tracked files only.
2. At `review-notes`; a commit moves `review-notes` (the branch HEAD names), and `main` stays.
3. A branch is a small file holding one commit id; nothing is copied.

Who does what: one person works alone in this lab; the practice for review starts in 2.2.

## 2.1 Merge two branches and resolve a conflict alone (addition)

The first merge is a fast-forward, the second makes a merge commit after a conflict on the
threshold line; the resolution keeps the sector line and both changes the brief asks for.

1. For the first, `main` had not moved since the branch started, so `main` could simply move
   forward. For the second, both had new commits, so Git needed a commit with two parents.
2. `main`'s side of the conflict: the threshold wording that the first merge brought into
   `main`. The sector line comes from the branch being merged, so it would stay.
3. Two parents.

Who does what: alone here; in a team the person who resolves the conflict is not the person who
approves the result (lab 2.2).

## 2.2 Branch, review and resolve a conflict in teams of three (entry lab)

Two pull requests; the reviewer comments with a line and a reason, approves, merges the first;
the second no longer merges until its author merges `main` into the branch and resolves.

1. `main` is protected: changes arrive only through an approved pull request, so nobody's
   unreviewed work reaches the shared branch.
2. The author knows what their change means and owns the branch; a reviewer who resolves it
   would then be approving their own edit.
3. The resolution is new code nobody has reviewed; the earlier approval was for other content.

Who does what: author A and author B write; reviewer C comments, approves and merges; nobody
approves their own pull request.

## 2.3 Undo five mistakes (addition)

`git restore --staged` then delete the scratch file; `git restore` the stray line; `git reset
--hard HEAD~1` for the local debug commit; `git commit --amend` for the message and the forgotten
file; `git revert` for the pushed threshold change, then push; the deleted branch from
`git reflog` with `git branch <name> <id>`.

1. `--staged` takes the file out of the index and keeps the change in the folder; without it,
   the change in the folder is discarded.
2. The debug commit was never pushed, so nobody else has it. The threshold commit is on the hub:
   rewriting it would break every teammate's history, so it is undone with a new commit.
3. By default 90 days for reachable entries and 30 for commits no branch reaches
   (`gc.reflogExpire`, `gc.reflogExpireUnreachable`); only on that clone.

Who does what: the author undoes their own local mistakes; a pushed change is undone with a
revert that goes through review like any other change.

## 2.4 Rescue a project that fails on a second machine (entry lab)

The four failures and the fix are on the Day 3 debrief slide. The lock resolves
python-dateutil 4.0.0 (which needs tzdata) and tabulate 0.10.0; the rebuilt report's checksum
starts `e04d6927`.

1. Exact versions of every package, including indirect ones, with their hashes.
2. A lock that disagrees with `pyproject.toml` means someone changed the requirements without
   locking; updating silently would build something nobody reviewed.
3. Data has its own home and rules and changes each month; the README says where it is and
   which variable or argument points to it.

Who does what: the analyst changes dependencies and commits the new lock; the second machine's
user rebuilds from the lock and reports what failed, never edits it to make it work.

## 3.1 One command, and data kept out of the code (addition)

Reference files: `labs/kit/projects/v3/` (`rebuild.sh`, `expected/october.sha256`, the README's
Reproduce section). The clean clone prints `output/report.csv: OK`.

1. `.gitignore` applies to untracked files only; tracked files stay until `git rm --cached`.
2. That the output is the same bytes as the expected one, not merely that a program ran.
3. Anything the laptop holds that the README does not state: uv itself, Git Bash, network
   access, a cached package, a variable in a shell profile.

Who does what: the author writes the README; a different person follows it in a clean clone.

## 3.2 Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace (entry lab)

Reference definition: `labs/kit/files/3.2/Containerfile.solution`. Not run when the course was
built (no engine was running): rehearse it on the provided workspace.

1. The image is the built, read-only file system; a container is one run of it with a thin
   writable layer.
2. One image then serves every month, the data never travels inside an image, and its own rules
   on storage stay with the data folder.
3. Writing to the input folder; without it, a bug could change or delete the raw logs.

Who does what: the author writes the definition; the workspace administrator sets up the
rootless engine and its user id ranges; nobody runs the engine as root to get round a problem.

## 3.3 The key out of the code (addition)

Reference: `labs/kit/files/3.3/report.solution.py`.

1. `.env.example` tells a reader which variable to set; `.env` holds the value and stays on one
   machine.
2. A run that skips the upload looks successful; exit 2 and a sentence say what is missing.
3. Every process in that container, and anyone allowed to inspect it.

Who does what: the portal's owner issues the key; the developer only reads it from the
environment and never sees it in the code.

## 3.4 Remediate a seeded leaked key with a scanner and a commit hook (entry lab)

Leak: key K-0002 in `settings.toml`, added in "Add the portal settings", removed in "Read the
portal key from the environment". Order: rotate (revoke K-0002, issue a new key into `.env`),
write `ROTATION.md`, clean with `git filter-repo --replace-text`, force-push, scan again, install
the hook.

1. Cleaning removes the key from the hub, not from clones, forks and caches made since; only
   revoking makes every copy useless.
2. Clone again. Pushing from the old clone would put the old commits, key included, back on the
   hub.
3. A finding is itself written to logs and terminals; printing the whole key would leak it again.

Who does what: the developer who found the leak reports it; the operations lead who owns the
portal account revokes and issues; the data protection officer is told; the history clean-up is
reviewed by someone other than the person who made the leak.
