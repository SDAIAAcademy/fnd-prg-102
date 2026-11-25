---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
deck: "capstone"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/slides/capstone.html"
---

# Command Line, Git and Reproducible Environments

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
