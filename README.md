<!-- academy:title -->
# Command Line, Git and Reproducible Environments

سطر الأوامر وGit والبيئات القابلة لإعادة الإنتاج

Data & AI Foundations Track · SDAIA Academy · FND-PRG-102 · Level 100

Set up work that another person can rebuild from a clean machine: shell scripts, a reviewed Git history, locked environments, a container and no secrets in history

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
| Day 1 | The shell and the commit graph | Paths and permissions; Pipes, redirection and filters; Variables, exit codes and SSH; Commits, staging and history | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Working together on one history | Branches, merges and conflicts; Pull requests and review etiquette; Undoing mistakes; Virtual environments and lock files | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Rebuild anywhere, leak nothing | One command to rebuild and run; Images, containers and volumes; What a container shares; Scanning, and after a leak | [`slides/day3.html`](slides/day3.html) |
| Capstone | Capstone: peer reproduction |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**The air-quality monitoring company** (fictional, and unnamed on purpose). A private contractor
runs twelve dust and particle sensor stations, coded ST01 to ST12, at four clients' sites (Client A
to Client D) in one unnamed city; each station writes one line an hour to a log. Its monthly client
report is a small Python project that only runs on the analyst's laptop: no history, undeclared
packages, a data path on one computer and a report-portal key in the code. Over three days the
participants make it rebuildable by someone else.

All data is synthetic, written by `labs/_tools/make_data.py` with a fixed seed: hourly logs for
October and November 2026 (about 8,900 lines a month), with planted traps (comment lines, one
station's logs with Windows line endings, lines sent twice after a logger restart, a two-day gap).
The alert threshold the report uses, PM10 above 150 for an hour, is the company's own rule, not a
national standard. People appear only as roles (the analyst, the field technician, the reviewer,
Participant A to C); the seeded keys carry the prefix `fprg102_demo_`, the course's own, and open
nothing but the course's local stand-in for the portal.

## How the course runs

Three teaching days of four 60-minute sessions: about 25 minutes of teaching, demonstration and a
checkpoint, then a 35-minute lab. The capstone day is a peer reproduction. The minutes add up to
the catalog's hours:

| Hours in the catalog | Minutes | How they are spent |
|---|---|---|
| Instruction, 5 | 300 | 12 sessions × 25 minutes of teaching, demonstration and checkpoint |
| Lab, 7 | 420 | 12 labs × 35 minutes |
| Guided self-study, 5 | 300 | pre-work 90 (`labs/prework/README.md`); commit-graph practice 30 (`labs/practice/commit_graphs.md`); capstone preparation 2 × 60 after Days 2 and 3 (`labs/capstone/BRIEF.md`); the follow-up task 60 |
| Assessment, 1 | 60 | check briefing 5; the supervised AI-off check 45; the oral 7 and its changeover 3 |
| Capstone, 6 | 360 | kickoff at the end of Day 3, 10; on the capstone day: rubric and pairing 15, self-test on a clean folder 35, changeover to the peer's workspace 10, peer reproduction 150, writing the reproduction log 20, handback 20, fix clinic 70, trainer review 30 |

The five lab lines of the catalog entry are labs 1.2, 2.2, 2.4, 3.2 and 3.4, in its words and its
order. The other seven labs are additions, each marked so in its summary: each practises a topic
the entry lists that no entry lab covers (paths and permissions, scripts and SSH keys, the commit
graph, a merge alone, undoing mistakes, one rebuild command, keys in the environment).

<!-- academy:labs -->
## Labs

Every lab is a page in `labs/`, opened from the course page and from the lab slide of its session.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Find your way round the project folder | [`D1_1_project_folder.html`](labs/D1_1_project_folder.html) |
| 1.2 | Day 1 · Session 2 | A counting pipeline over synthetic logs | [`D1_2_counting_pipeline.html`](labs/D1_2_counting_pipeline.html) |
| 1.3 | Day 1 · Session 3 | The counting script on a second folder, and a practice key | [`D1_3_second_folder_key.html`](labs/D1_3_second_folder_key.html) |
| 1.4 | Day 1 · Session 4 | Draw the graph, then check it | [`D1_4_draw_the_graph.html`](labs/D1_4_draw_the_graph.html) |
| 2.1 | Day 2 · Session 1 | Merge two branches and resolve a conflict alone | [`D2_1_merge_alone.html`](labs/D2_1_merge_alone.html) |
| 2.2 | Day 2 · Session 2 | Branch, review and resolve a conflict in teams of three | [`D2_2_team_review.html`](labs/D2_2_team_review.html) |
| 2.3 | Day 2 · Session 3 | Undo five mistakes | [`D2_3_undo_five.html`](labs/D2_3_undo_five.html) |
| 2.4 | Day 2 · Session 4 | Rescue a project that fails on a second machine | [`D2_4_second_machine.html`](labs/D2_4_second_machine.html) |
| 3.1 | Day 3 · Session 1 | One command, and data kept out of the code | [`D3_1_one_command.html`](labs/D3_1_one_command.html) |
| 3.2 | Day 3 · Session 2 | Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace | [`D3_2_container.html`](labs/D3_2_container.html) |
| 3.3 | Day 3 · Session 3 | The key out of the code | [`D3_3_key_out_of_code.html`](labs/D3_3_key_out_of_code.html) |
| 3.4 | Day 3 · Session 4 | Remediate a seeded leaked key with a scanner and a commit hook | [`D3_4_leaked_key.html`](labs/D3_4_leaked_key.html) |
<!-- /academy:labs -->

## Capstone

A peer reproduces the participant's repository from the README on a clean workspace; the follow-up task fixes each failed step and records a second, successful reproduction

The project is the participant's own small one, on synthetic or public data. The brief, the
README checklist and the reproduction log template are in `labs/capstone/`.

**Submission:** individual. A link to a public GitHub repository holding a README with a Reproduce
section, a lock file, a container definition, the secret-scan configuration and a clean scan of the
whole history. On the capstone day a peer reproduces it on a clean workspace and files the
reproduction log as a pull request. In the follow-up task the participant fixes every step the
peer could not follow, and the peer records a second, successful reproduction. Then a seven-minute
oral: three minutes on one failed step and its fix, four of questions.

The peer reproduction is scored out of 100 on this rubric:

| Criterion | Weight |
|---|---|
| README: prerequisites, where the data comes from, one documented rebuild command and the expected output | 20 |
| Clean rebuild: on the peer's clean workspace the locked environment rebuilds and reproduces the expected output | 30 |
| Container: the definition installs from the lock, runs without administrator rights and reads mounted data | 15 |
| Hygiene: configuration read from the environment, a clean scan of the whole history, no data or outputs committed | 15 |
| History: small commits merged through reviewed pull requests, with the peer's log merged by pull request | 10 |
| Follow-up: every step the peer could not follow fixed, and the second reproduction log successful | 10 |

The oral and the labs are graded on their own, so nothing in the table is counted twice. The
supervised check paper with its key, the oral questions and the detailed marking guide are kept by
the Academy outside this public repository.

## Assessment

- Supervised AI-off check on shell commands and commit graphs (20%)
- Labs (30%)
- Peer reproduction of the capstone, on a rubric (40%)
- Short oral on one failed step (10%)

**Passing:** 65% overall, at least 60% on the supervised check, and a successful reproduction after the follow-up task

**Authenticity:** Supervised check without assistance; inspection of commit history and the peer's reproduction log; an oral on the participant's own fix

**Certificate:** completion with assessed work

The practice questions in `assessments/bank.json` cover every outcome; the checkpoints in the decks
add one per session.

## AI policy

AI-off for the first attempt at each lab's core commands and for the supervised check. AI-tutor
for extensions, through a repository instruction file telling the assistant to hint, not solve.
AI-full for the capstone, defended in the oral.

The instruction file is `AGENTS.md` in the lab workspace (`labs/kit/tutor/AGENTS.md`). It was not
tested against a model when the course was built.

## Responsible use

Covers never committing secrets, personal or classified data, and the duty to rotate and report a
leaked credential, which the leak lab rehearses. All repositories use synthetic data.

The course's own rule for the labs and the capstone: only synthetic or public data goes into a
repository or to any AI assistant, and a key that appears in a conversation or a commit is treated
as leaked and rotated.

## Running the labs

```bash
uv run labs/kit/setup.py            # writes the lab workspace ../air-labs
cd ../air-labs
uv run lab.py start 1.1             # each lab's starting folder
uv run lab.py check 1.1             # PASS, or what is still missing
```

`labs/README.md` has the details. `labs/solutions/run_all.sh <a new folder>` starts every lab,
confirms that its starting state does not pass, runs its solution script and confirms that it
passes.

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
<!-- /academy:sources -->
