# Reproduction log

Copy this file to `reproduction/peer-1.md` (or `peer-2.md` for the second reproduction) in the
author's repository, fill it, and open a pull request. Record what happened, not what should
have happened. A step you had to guess is marked **guessed**: the README did not say it.

## The run

- Repository: <the link>
- Commit reproduced: <the full commit id>
- Reproduced by: <your coded label, for example Participant B>
- Workspace: <the provided Linux workspace, or a fresh user account on which system>
- Tool versions: `git --version`: … ; `uv --version`: … ; container engine and version: …
- Started at: … ; finished at: …

## Steps

One row per step of the README, in its order. Result: **passed**, **failed** or **guessed**.

| # | What the README said | The command you ran | Result | Last line of any error, or what you guessed |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

## The four checks

| Check | Result | Evidence |
|---|---|---|
| The environment rebuilt from the lock | | the command and its last line |
| The output matches the expected one | | the checksum line, or the first rows compared |
| The container built and ran rootless, data mounted read-only | | the run command and the output file |
| A scan of the whole history is clean; no data or output in any commit | | the scan's last line; `git log --stat --all` checked |

## For the author

The one change that would have helped most:

Anything else the author should know (no edits to the author's files; write it here):
