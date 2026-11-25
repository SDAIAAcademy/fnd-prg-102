# Command Line, Git and Reproducible Environments: labs

Twelve 35-minute labs for the SDAIA Academy course **FND-PRG-102 Command Line, Git and
Reproducible Environments (سطر الأوامر وGit والبيئات القابلة لإعادة الإنتاج)**. Every lab works
on the monthly client report of **the air-quality monitoring company**, a fictional contractor
that runs twelve sensor stations (ST01 to ST12) for four clients. All data is synthetic. Each lab
starts from its own starting folder, written by the lab kit, so no lab depends on another.

The labs are done in a terminal: Git, Bash (Git Bash on Windows) and uv. No model, key or paid
account is needed. Lab 3.2 also needs a container engine that runs without administrator rights
(Podman or Docker in rootless mode), on your laptop or on the provided Linux workspace.

## Set up once

```bash
git --version                       # 2.40 or later
uv --version
git config user.name                # must print something
uv run labs/kit/setup.py            # from the course folder: writes ../air-labs
cd ../air-labs
uv run lab.py list
```

`setup.py --to <folder>` writes the workspace somewhere else (keep the path short on Windows).
The workspace holds `lab.py`, the kit's files in `_kit/`, and `AGENTS.md`, the hint-only
instruction for any coding assistant you use for an extension.

## Each lab

```bash
uv run lab.py start 2.3             # a fresh folder 2.3/ with the lab's starting state
uv run lab.py check 2.3             # is the evidence there? PASS or what is missing
uv run lab.py start 2.3 --discard   # start again; the old folder moves to _discarded/
```

Labs with a Git host use a local stand-in: a bare repository in `hub/` beside the lab's
folders. In lab 2.2 its `main` is protected and `uv run lab.py pr ...` plays the pull requests
(open, comment, resolve, approve, merge). With a class host (Forgejo, Gitea, GitLab or GitHub),
do the same steps there. In labs 3.3 and 3.4, `uv run lab.py keys ...` plays the report
portal that issues and revokes keys. Every practice commit the kit makes has a role as its author
and a fixed date, so commit ids are the same on every machine.

On Windows, Git converts line endings to CR LF on checkout by default. The kit's practice
repositories set `core.autocrlf=false`, and the report project carries a `.gitattributes` that keeps
scripts and checksum files in LF, so `bash` and `sha256sum` read a fresh clone the same way on
every machine. Lab 3.4 unsets `core.hooksPath` in its practice repository so that `pre-commit
install` works; the lab page gives a plain hook for machines that set it for every repository.

| Lab | What you do | Entry lab or addition |
|---|---|---|
| 1.1 | Map a folder, read permission strings, fix a script tied to one computer | addition |
| 1.2 | A counting pipeline over synthetic logs | entry |
| 1.3 | The counting script on a second folder, exit codes, a practice SSH key | addition |
| 1.4 | Draw commit graphs, then check them | addition |
| 2.1 | Merge two branches and resolve a conflict alone | addition |
| 2.2 | Branch, review and resolve a conflict in teams of three | entry |
| 2.3 | Undo five mistakes | addition |
| 2.4 | Rescue a project that fails on a second machine | entry |
| 3.1 | One command, and data kept out of the code | addition |
| 3.2 | Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace | entry |
| 3.3 | The key out of the code | addition |
| 3.4 | Remediate a seeded leaked key with a scanner and a commit hook | entry |

"Entry" labs are the five the catalog entry lists, in its words; the seven additions each
practise a topic of the entry that no entry lab covers.

## Other folders

- `practice/commit_graphs.md`: the commit-graph practice for the evening of Day 1.
- `prework/README.md`: the guided pre-work.
- `capstone/`: the capstone brief, the reproduction log template and the README checklist.
- `solutions/`: one script per lab that does its steps and runs its check (`S1_1.sh` to
  `S3_4.sh`), `run_all.sh` that runs them all on a fresh workspace, and `answer_key.md`.
- `kit/`: the lab tool, the starting files, the report project in its versions, the course's
  secret scanner and the synthetic data. `_tools/make_data.py` wrote the data and the reference
  values (`kit/reference.json`) with a fixed seed.
