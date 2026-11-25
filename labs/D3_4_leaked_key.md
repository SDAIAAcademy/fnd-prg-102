---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "3.4"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_4_leaked_key.html"
---

# Lab 3.4 · Remediate a seeded leaked key with a scanner and a commit hook

A key leaked in an old commit: scan, rotate, write the note, clean the history, and add a hook that blocks the next one

Day 3 · Session 4: Scanning, and after a leak

### Goal

A report-portal key was committed in a settings file, then removed two commits later; the hub still serves it to anyone who clones. Find it with a scan of the whole history, rotate it first, record what happened, clean it out of every commit, and install a hook so the next one never gets committed.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 3.4`: `air-report/` with its history and hub, `portal/` (the key portal stand-in) and `ROTATION-template.md`
- The project ships `tools/scan_secrets.py` (the course's small scanner), `.gitleaks.toml` (the same rule for gitleaks) and `.pre-commit-config.yaml`
- uv's `uvx` runs git-filter-repo and pre-commit without installing them
- AI policy: **off** for the first attempt

### Scan the whole history and find the key 5 min

```bash
# file: terminal
uv run lab.py start 3.4
cd 3.4/air-report
uv run --no-project python tools/scan_secrets.py            # today's files: clean
uv run --no-project python tools/scan_secrets.py --history  # every commit
```

Which commit added it, which removed it, and since when could anyone with a clone read it?

### Rotate first 7 min

Until the old key is revoked, every copy of the history can still use it. Revoke it at the portal, issue a new one, and keep the new one only in `.env`.

```bash
# file: terminal
cd ../.. && uv run lab.py keys list 3.4
uv run lab.py keys revoke 3.4 K-0002
uv run lab.py keys issue 3.4          # shown once: copy it into 3.4/air-report/.env
cd 3.4/air-report && git check-ignore -v .env
```

### Write ROTATION.md 6 min

Copy `../ROTATION-template.md` to `ROTATION.md` and fill its four sections: what leaked, rotated, history cleaned, who was told (the operations lead who owns the portal account, the data protection officer). Name keys by their id, never by their value.

### Clean the history, force-push, scan again 10 min

```bash
# file: terminal
pwd        # must end in 3.4/air-report: filter-repo rewrites the repository you are in
printf '%s==>REMOVED\n' '<the old key>' > ../replacements.txt   # outside the repository
uvx git-filter-repo --replace-text ../replacements.txt --force
rm ../replacements.txt
git remote add origin ../hub/air-report.git     # filter-repo removes the remote on purpose
git push --force origin main
uv run --no-project python tools/scan_secrets.py --history
```

Every commit from the leak onwards has a new id now. Everyone with an old clone must clone again.

### Install the hook, see it block a key, and check 7 min

```bash
# file: terminal
uvx pre-commit install
git add ROTATION.md && git commit -m "Add the rotation note" && git push origin main
printf 'key = "fprg102_demo_%s"\n' cdcdcdcdcdcdcdcdcdcdcdcd > probe.toml
git add probe.toml && git commit -m "probe"     # refused
git reset -q -- probe.toml && rm probe.toml
cd ../.. && uv run lab.py check 3.4
```

If `pre-commit install` refuses because `core.hooksPath` is set on your machine, use the plain hook instead, from the workspace folder: `cp _kit/files/3.4/pre-commit-hook 3.4/air-report/.git/hooks/pre-commit`, then `git -C 3.4/air-report config core.hooksPath .git/hooks` so that this repository alone uses it. It runs the same scan.

### ✱ Stretch

Where gitleaks is allowed: run `gitleaks git` on a copy of the history from before the clean-up, with the repository's `.gitleaks.toml`, and compare what it finds with the course scanner. Or push a test key to a class host with push protection switched on and read its refusal.

## Check yourself

1. Why is rotating first, before cleaning the history?
2. After the force-push, what must a teammate with an old clone do, and what happens if they push from it?
3. Why does the scanner print only the first characters of a key it finds?
