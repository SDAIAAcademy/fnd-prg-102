"""A small secret scanner, the course's own stand-in for a tool such as gitleaks.

    uv run --no-project python tools/scan_secrets.py [folder]      tracked and new files
    uv run --no-project python tools/scan_secrets.py --staged      what the next commit adds
    uv run --no-project python tools/scan_secrets.py --history     every commit on every branch

Exit 1 when anything is found, so it works as a pre-commit hook. It prints where a secret is and
its first characters, never the whole value. The rules mirror .gitleaks.toml: the report
portal's keys (prefix fprg102_), private key blocks, and a quoted value of 16 characters or more
given to a name such as key, token, secret or password. Python standard library only.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RULES = {
    "portal-key": re.compile(r"fprg102_[a-z]+_[0-9a-f]{24}"),
    "private-key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "assigned-secret": re.compile(r"(?i)\b(?:api[_-]?key|key|token|secret|password)\b\s*[:=]\s*[\"']([A-Za-z0-9_\-+/=]{16,})[\"']"),
}


def mask(value: str) -> str:
    return value[:13] + "..." if len(value) > 13 else value[:4] + "..."


def find(text: str) -> list[tuple[str, str]]:
    out = []
    for name, rx in RULES.items():
        for m in rx.finditer(text):
            out.append((name, mask(m.group(0))))
    return out


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def scan_files(root: Path, files: list[Path]) -> list[str]:
    hits = []
    for rel in files:
        p = root / rel
        if p.is_file():
            for name, what in find(p.read_text(encoding="utf-8", errors="replace")):
                hits.append(f"{name}: {rel.as_posix()}: {what}")
    return hits


def scan_staged(repo: Path) -> list[str]:
    hits = []
    for rel in git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines():
        blob = git(repo, "show", f":{rel}")
        for name, what in find(blob):
            hits.append(f"{name}: {rel} (staged): {what}")
    return hits


def scan_history(repo: Path) -> list[str]:
    hits, commit, subject, path = [], "", "", ""
    log = git(repo, "log", "--all", "-p", "--format=COMMIT %h %s", "--no-color", "--no-ext-diff")
    for line in log.splitlines():
        if line.startswith("COMMIT "):
            _, commit, *rest = line.split(" ")
            subject = " ".join(rest)
        elif line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            for name, what in find(line):
                hits.append(f"{name}: {path} in commit {commit} ({subject}): {what}")
    return hits


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    folder = Path(next((a for a in args if not a.startswith("--")), ".")).resolve()
    if "--history" in args:
        hits, what = scan_history(folder), "history"
    elif "--staged" in args:
        hits, what = scan_staged(folder), "staged changes"
    else:
        files = [Path(f) for f in git(folder, "ls-files", "-co", "--exclude-standard").splitlines()]
        hits, what = scan_files(folder, files), "files"
    for h in hits:
        print("LEAK " + h)
    print(f"secret scan of the {what}: {len(hits)} found" + ("" if hits else ", clean"))
    if hits and "--staged" in args:
        print("commit refused: take the secret out of the file and read it from the environment")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
