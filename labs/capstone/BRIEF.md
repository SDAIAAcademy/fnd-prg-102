# Capstone brief: peer reproduction

Your own small project, made rebuildable by a stranger. On the capstone day a peer clones it on a
clean workspace and follows only your README. Everything they could not follow, you fix in the
follow-up task; then they reproduce it a second time.

## The project

- Small and your own: a script or two that read some files and write a result (a table, a
  chart, a summary). Ten minutes of running at most.
- **Synthetic or public data only.** Nothing personal, internal, classified or under a
  licence that forbids copying. If the data is public, link to where it is published; do not
  commit it. If it is synthetic, commit the script that generates it with a fixed seed, not the
  generated files.
- No key that opens anything real. If your project needs a key, make it a variable read from the
  environment and write how to get one in the README; the peer may skip that step.

## What the repository holds when you hand it over

Use `README_CHECKLIST.md`. In short:

1. A README with a `## Reproduce` section: the tools and their versions, where the data comes
   from, one command, and what success looks like (a checksum, a row count, a known first line).
2. A lock file committed with the project file (`uv.lock` with `pyproject.toml`, or the lock of
   the tool you chose).
3. A container definition that installs from the lock, runs as a user that is not root, and reads
   data from a mounted folder.
4. A secret-scan configuration and a hook (the course's `.pre-commit-config.yaml` and
   `.gitleaks.toml` are a starting point), and a scan of the whole history that comes back clean.
5. No data, no outputs, no `.venv/`, no `.env` in any commit.
6. History made of small commits, merged into `main` through pull requests that someone reviewed.

## Time

| When | Minutes | What |
|---|---|---|
| Evening of Day 2 | 60 | Choose the project, make it a repository with a lock, write the first README |
| Evening of Day 3 | 60 | One rebuild command, the container definition, the scan; then follow your own README in a fresh clone |
| Capstone day | | Self-test, then a peer reproduces it; the log arrives as a pull request; the fix clinic |
| Follow-up task | 60 | Fix every failed step, one small commit each; the peer reproduces it again |

## On the capstone day

1. Post the link to your public repository and the commit id to be reproduced.
2. Self-test (35 minutes): clone into an empty folder and follow the README word for word.
3. Your peer reproduces it (150 minutes) on a clean workspace, filling `REPRODUCTION_LOG.md`.
   You do not help: the README speaks for you.
4. The peer adds the log as `reproduction/peer-1.md` on a branch and opens a pull request. You
   review it and merge it; you do not edit the peer's findings.
5. Fix clinic: start fixing the failed steps.

## The follow-up task, and the oral

Fix every step the peer marked failed or guessed, one small commit per fix, each merged by a
pull request. The same peer then reproduces the project again from a clean workspace and files
`reproduction/peer-2.md`. Then a seven-minute oral: three minutes on one failed step and its fix,
four minutes of questions.

## AI policy

AI-full for the capstone: you may use an assistant for any part of it. You explain every step
yourself in the oral. Never paste a key or anyone's data into an assistant.

## How it is scored

The peer reproduction is 40% of the course, on the rubric in the course README: README 20, clean
rebuild 30, container 15, hygiene 15, history 10, follow-up 10. The oral (10%) is scored apart.
A successful reproduction after the follow-up task is required for the certificate.
