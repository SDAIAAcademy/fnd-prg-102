<!-- academy:title -->
# Command Line, Git and Reproducible Environments

سطر الأوامر وGit والبيئات القابلة لإعادة الإنتاج

Data & AI Foundations Track · SDAIA Academy · FND-PRG-102 · Level 100

REPLACE: one line under the title: what participants can do after the course

Participants set up work that another person can rebuild from a clean machine. They script the shell, use Git with branches, pull requests and review on a shared repository, resolve a merge conflict, lock dependencies, run a project in a container without administrator rights, and keep secrets out of history.

**Format:** Intensive: 3 teaching days and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/fnd-prg-102/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Explain how Git records history as commits, branches and remotes, and what each everyday command changes, given diagrams of a repository and sequences of commands | Awareness | commit graphs drawn correctly for four of five sequences in a supervised check |
| LO2 | Use the shell to inspect and transform files, combining commands with pipes and a short script, given a folder of synthetic log and comma-separated files | Applied | a script that produces the requested counts and runs unchanged on a second folder |
| LO3 | Apply a branch, pull request and review workflow, including resolving a merge conflict, given a team repository with a protected main branch | Applied | a merged pull request with review comments addressed and a resolved conflict in the history |
| LO4 | Configure an isolated environment with locked dependencies and run the project in a container without administrator rights, given an analysis project that fails on a second machine | Applied | a lock file, a container definition and a clean rebuild that reproduces the expected output |
| LO5 | Prepare a repository that keeps secrets out of history, and carry out the response when one leaks, given a project needing an API key, with a seeded leaked key in an old commit | Applied | configuration read from the environment, a passing secret scan and a rotation note |
| LO6 | Deliver a repository that a peer reproduces on a clean machine using only its README, given the participant's own small project | Performance | the peer's reproduction log and fixes for every step the peer could not follow |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1; REPLACE: the title of Session 2; REPLACE: the title of Session 3; REPLACE: the title of Session 4 | [`slides/day1.html`](slides/day1.html) |
| Day 2 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1; REPLACE: the title of Session 2; REPLACE: the title of Session 3; REPLACE: the title of Session 4 | [`slides/day2.html`](slides/day2.html) |
| Day 3 | REPLACE: the theme of this unit, in a few words | REPLACE: the title of Session 1; REPLACE: the title of Session 2; REPLACE: the title of Session 3; REPLACE: the title of Session 4 | [`slides/day3.html`](slides/day3.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a page in `labs/`, opened from the course page and from the lab slide of its session.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | REPLACE: what participants build in lab 1.1 | [`D1_1.html`](labs/D1_1.html) |
| 1.2 | Day 1 · Session 2 | REPLACE: what participants build in lab 1.2 | [`D1_2.html`](labs/D1_2.html) |
| 1.3 | Day 1 · Session 3 | REPLACE: what participants build in lab 1.3 | [`D1_3.html`](labs/D1_3.html) |
| 1.4 | Day 1 · Session 4 | REPLACE: what participants build in lab 1.4 | [`D1_4.html`](labs/D1_4.html) |
| 2.1 | Day 2 · Session 1 | REPLACE: what participants build in lab 2.1 | [`D2_1.html`](labs/D2_1.html) |
| 2.2 | Day 2 · Session 2 | REPLACE: what participants build in lab 2.2 | [`D2_2.html`](labs/D2_2.html) |
| 2.3 | Day 2 · Session 3 | REPLACE: what participants build in lab 2.3 | [`D2_3.html`](labs/D2_3.html) |
| 2.4 | Day 2 · Session 4 | REPLACE: what participants build in lab 2.4 | [`D2_4.html`](labs/D2_4.html) |
| 3.1 | Day 3 · Session 1 | REPLACE: what participants build in lab 3.1 | [`D3_1.html`](labs/D3_1.html) |
| 3.2 | Day 3 · Session 2 | REPLACE: what participants build in lab 3.2 | [`D3_2.html`](labs/D3_2.html) |
| 3.3 | Day 3 · Session 3 | REPLACE: what participants build in lab 3.3 | [`D3_3.html`](labs/D3_3.html) |
| 3.4 | Day 3 · Session 4 | REPLACE: what participants build in lab 3.4 | [`D3_4.html`](labs/D3_4.html) |
<!-- /academy:labs -->

## Capstone

A peer reproduces the participant's repository from the README on a clean workspace; the follow-up task fixes each failed step and records a second, successful reproduction

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- Writes and runs a short program in Python or another language

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Version control and hosting:** Git with Forgejo or Gitea, Git with GitLab or GitHub
- **Environment and lock-file manager:** uv, Poetry, pip-tools
- **Container engine that runs without administrator rights:** Podman in rootless mode, Docker in rootless mode
- **Secret scanning and hooks:** gitleaks with pre-commit, the host's built-in secret scanning
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->
