---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "1.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_3_second_folder_key.html"
---

# Lab 1.3 · The counting script on a second folder, and a practice key

Addition: the counting script runs unchanged on November and fails clearly; then a practice SSH key and host entry

Day 1 · Session 3: Variables, exit codes and SSH

### Goal

Turn the counting script into a tool: it takes the folder to count from outside, runs unchanged on November's logs, and fails with a clear message and exit code. Then make a practice SSH key pair and the host entry you would use to log in to the lab workspace.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 1.3`: `data/october/`, `data/november/`, an empty `keys/` and `counts.sh`, the six counts of lab 1.2 tied to a folder named `logs/`
- `ssh-keygen` (it comes with Git for Windows, macOS and Linux)
- AI policy: **off** for the first attempt; the hint-only assistant after that

### Take the folder as $1, with AIR_LOGS as the fallback 8 min

At the top of `counts.sh`, set `DIR` to the first argument, or to `$AIR_LOGS` when there is no argument, and replace every `logs/` with `"$DIR"/`. Quote it: a folder name may hold a space.

```bash
# file: counts.sh
DIR="${1:-${AIR_LOGS:-}}"
```

### Stop with exit code 2 and a message on stderr 7 min

Add `set -euo pipefail` as the first command. When `DIR` is empty or holds no `.log` file, print one line to standard error (`>&2`) and `exit 2`. Try it and read the code:

```bash
# file: terminal
bash counts.sh data/missing; echo "exit code: $?"
```

### Run it unchanged on November 5 min

```bash
# file: terminal
bash counts.sh data/november
AIR_LOGS=data/october bash counts.sh | head -n 2
```

### Make a practice key pair and read its fingerprint 6 min

The key stays in this lab folder: it is for practice and is never committed or copied to your own `.ssh` folder.

```bash
# file: terminal
ssh-keygen -t ed25519 -C "participant-a practice key" -f keys/practice_key
ssh-keygen -lf keys/practice_key.pub > keys/fingerprint.txt
cat keys/practice_key.pub
```

Give the key a passphrase when you will use it for real; for this practice key an empty one is allowed.

### Write the host entry and check 9 min

Create `ssh_config` with a `Host lab-workspace` entry: `HostName` (the trainer gives the address; use `192.0.2.10` otherwise, an address reserved for examples), `User`, `IdentityFile keys/practice_key` and `IdentitiesOnly yes`.

```bash
# file: terminal
cd .. && uv run lab.py check 1.3
```

### ✱ Stretch

Log in to the provided Linux workspace with the key (`ssh -F ssh_config lab-workspace`, after the trainer adds your public key) and run `counts.sh` there on its copy of the logs.

## Check yourself

1. What does `$?` hold after a pipeline whose first command failed, with and without `pipefail`?
2. Why does the error message go to standard error and not to standard output?
3. Which of the two key files may you paste into a web form, and which never leaves your machine?
