---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/index.html"
---

# Command Line, Git and Reproducible Environments

سطر الأوامر وGit والبيئات القابلة لإعادة الإنتاج

Data & AI Foundations Track · 3 teaching days + capstone day · 24 hours · Level 100

Set up work that another person can rebuild from a clean machine: shell scripts, a reviewed Git history, locked environments, a container and no secrets in history

Participants set up work that another person can rebuild from a clean machine. They script the shell, use Git with branches, pull requests and review on a shared repository, resolve a merge conflict, lock dependencies, run a project in a container without administrator rights, and keep secrets out of history.

**Who it is for:** Beginners. Graduates and career changers heading for analysis, data science, data engineering or AI engineering courses, and computing graduates whose degree did not require testing, version control or reproducible environments.

**Format:** Intensive: 3 teaching days and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**The air-quality monitoring company.** A private contractor (fictional, unnamed) that runs twelve dust and particle sensor stations, ST01 to ST12, at four clients' sites in one unnamed city; its monthly client report is a Python project that only runs on the analyst's laptop. Every lab works on synthetic hourly logs for October and November 2026 generated with a fixed seed, with planted traps (comment lines, Windows line endings, duplicate lines after a logger restart, a two-day gap), and on a seeded report-portal key whose prefix is the course's own; people appear only as roles.

## The course

### Day 1: The shell and the commit graph

Slides: https://sdaiaacademy.github.io/fnd-prg-102/slides/day1.md

- **Session 1: Paths and permissions**
  - Tell an absolute path from a relative one and predict where each points after a move
  - Read a permission string and say who may read, write or run the file
  - Make a script independent of the folder it is run from
  - [Lab 1.1: Find your way round the project folder (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_1_project_folder.html)
- **Session 2: Pipes, redirection and filters**
  - Chain head, grep, cut, sort, uniq and wc into a pipeline that answers one question
  - Redirect output and errors to files
  - Find a hidden character or a repeated line that skews a count
  - [Lab 1.2: A counting pipeline over synthetic logs (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_2_counting_pipeline.html)
- **Session 3: Variables, exit codes and SSH**
  - Pass a folder as an argument with an environment variable as the fallback
  - Make a script stop with a non-zero exit code and a message on stderr
  - Create an SSH key pair, read its fingerprint and write a host entry
  - [Lab 1.3: The counting script on a second folder, and a practice key (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_3_second_folder_key.html)
- **Session 4: Commits, staging and history**
  - Draw the commit graph that a sequence of commands produces
  - Tell what is changed, what is staged and what is committed
  - Read git log --graph and match it to a drawing
  - [Lab 1.4: Draw the graph, then check it (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_4_draw_the_graph.html)

### Day 2: Working together on one history

Slides: https://sdaiaacademy.github.io/fnd-prg-102/slides/day2.md

- **Session 1: Branches, merges and conflicts**
  - Tell a fast-forward from a merge commit on a graph
  - Read conflict markers and keep both changes where both are right
  - Push, fetch and read origin/main as the hub's last known state
  - [Lab 2.1: Merge two branches and resolve a conflict alone (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_1_merge_alone.html)
- **Session 2: Pull requests and review etiquette**
  - Open a small pull request from a branch with a title that says what changes
  - Write review comments that name a line and a reason, and answer them with commits
  - Resolve a conflict on your own branch before the merge
  - [Lab 2.2: Branch, review and resolve a conflict in teams of three (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_2_team_review.html)
- **Session 3: Undoing mistakes**
  - Choose between restore, amend, reset and revert for a given mistake
  - Undo a pushed commit without rewriting what others pulled
  - Recover a lost commit or branch from the reflog
  - [Lab 2.3: Undo five mistakes (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_3_undo_five.html)
- **Session 4: Virtual environments and lock files**
  - Explain why a project runs on one machine and fails on another
  - Declare dependencies and lock them with an environment manager
  - Rebuild a fresh environment from the lock and compare the output
  - [Lab 2.4: Rescue a project that fails on a second machine (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D2_4_second_machine.html)

### Day 3: Rebuild anywhere, leak nothing

Slides: https://sdaiaacademy.github.io/fnd-prg-102/slides/day3.md

- **Session 1: One command to rebuild and run**
  - Keep data and outputs out of the repository and say where they come from
  - Write one documented command that rebuilds and checks the result
  - Test a README by following it in a clean clone
  - [Lab 3.1: One command, and data kept out of the code (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_1_one_command.html)
- **Session 2: Images, containers and volumes**
  - Tell an image from a container and a layer from a mount
  - Write a short container definition that installs from the lock
  - Run a container without administrator rights with data mounted read-only
  - [Lab 3.2: Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_2_container.html)
- **Session 3: What a container shares**
  - Name what a container shares with its host
  - Read a key from the environment and stop clearly when it is missing
  - Keep the key out of the output and the repository, with an example file in its place
  - [Lab 3.3: The key out of the code (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_3_key_out_of_code.html)
- **Session 4: Scanning, and after a leak**
  - Run a secret scan over files, staged changes and the whole history
  - Carry out the leak response in order: rotate, clean, report
  - Install a commit hook that refuses a commit holding a key
  - [Lab 3.4: Remediate a seeded leaked key with a scanner and a commit hook (35 min)](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_4_leaked_key.html)

### Capstone: Capstone: peer reproduction

Slides: https://sdaiaacademy.github.io/fnd-prg-102/slides/capstone.md

## Capstone

A peer reproduces the participant's repository from the README on a clean workspace; the follow-up task fixes each failed step and records a second, successful reproduction

**What you submit:** Individual. A link to a public GitHub repository of the participant's own small project, on synthetic or public data only: a README with a Reproduce section, a lock file, a container definition, the secret-scan configuration and a clean scan of the whole history. On the capstone day a peer reproduces it on a clean workspace and files the reproduction log as a pull request; within the follow-up task the participant fixes every failed step and the peer records a second, successful reproduction. Then a seven-minute oral: three minutes on one failed step and its fix, four of questions.

**Rubric:**

- README: prerequisites, where the data comes from, one documented rebuild command and the expected output: 20%
- Clean rebuild: on the peer's clean workspace the locked environment rebuilds and reproduces the expected output: 30%
- Container: the definition installs from the lock, runs without administrator rights and reads mounted data: 15%
- Hygiene: configuration read from the environment, a clean scan of the whole history, no data or outputs committed: 15%
- History: small commits merged through reviewed pull requests, with the peer's log merged by pull request: 10%
- Follow-up: every step the peer could not follow fixed, and the second reproduction log successful: 10%

## Outcomes

- **LO1** Explain how Git records history as commits, branches and remotes, and what each everyday command changes, given diagrams of a repository and sequences of commands (Awareness) Evidence: commit graphs drawn correctly for four of five sequences in a supervised check
- **LO2** Use the shell to inspect and transform files, combining commands with pipes and a short script, given a folder of synthetic log and comma-separated files (Applied) Evidence: a script that produces the requested counts and runs unchanged on a second folder
- **LO3** Apply a branch, pull request and review workflow, including resolving a merge conflict, given a team repository with a protected main branch (Applied) Evidence: a merged pull request with review comments addressed and a resolved conflict in the history
- **LO4** Configure an isolated environment with locked dependencies and run the project in a container without administrator rights, given an analysis project that fails on a second machine (Applied) Evidence: a lock file, a container definition and a clean rebuild that reproduces the expected output
- **LO5** Prepare a repository that keeps secrets out of history, and carry out the response when one leaks, given a project needing an API key, with a seeded leaked key in an old commit (Applied) Evidence: configuration read from the environment, a passing secret scan and a rotation note
- **LO6** Deliver a repository that a peer reproduces on a clean machine using only its README, given the participant's own small project (Performance) Evidence: the peer's reproduction log and fixes for every step the peer could not follow

## Tools

- **Version control and hosting:** Git with Forgejo or Gitea, Git with GitLab or GitHub
- **Environment and lock-file manager:** uv, Poetry, pip-tools
- **Container engine that runs without administrator rights:** Podman in rootless mode, Docker in rootless mode
- **Secret scanning and hooks:** gitleaks with pre-commit, the host's built-in secret scanning

## Prerequisites

- Writes and runs a short program in Python or another language

## Sources

### Git

- [Pro Git: Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [git-restore documentation](https://git-scm.com/docs/git-restore)
- [git-reset documentation](https://git-scm.com/docs/git-reset)
- [git-revert documentation](https://git-scm.com/docs/git-revert)
- [git-reflog documentation](https://git-scm.com/docs/git-reflog)
- [git-filter-repo manual (--replace-text)](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)

### Hosting, review and protected branches

- [Protected branches (Gitea documentation)](https://docs.gitea.com/usage/access-control/protected-branches)
- [Forgejo user guide](https://forgejo.org/docs/latest/user/)
- [Push protection (GitHub documentation)](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- [Secret detection (GitLab documentation)](https://docs.gitlab.com/user/application_security/secret_detection/)

### Environments and lock files

- [uv: structure and files (uv.lock)](https://docs.astral.sh/uv/concepts/projects/layout/)
- [uv: locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv: exporting a lockfile](https://docs.astral.sh/uv/concepts/projects/export/)
- [Poetry (project repository)](https://github.com/python-poetry/poetry)
- [pip-tools (project repository)](https://github.com/jazzband/pip-tools)

### Containers without administrator rights

- [Podman rootless tutorial](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md)
- [podman-run (--userns=keep-id)](https://docs.podman.io/en/latest/markdown/podman-run.1.html)
- [Docker rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Docker: bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
- [Docker: what is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [The official Python images](https://hub.docker.com/_/python)

### Secrets and remote login

- [Removing sensitive data from a repository (GitHub documentation)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [pre-commit](https://pre-commit.com/)
- [ssh-keygen(1)](https://man.openbsd.org/ssh-keygen)
- [ssh_config(5)](https://man.openbsd.org/ssh_config)

---

SDAIA Academy · Data & AI Foundations Track · Command Line, Git and Reproducible Environments

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-25 · commit 89bccf3
