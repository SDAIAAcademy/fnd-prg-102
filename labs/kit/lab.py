# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""The lab tool of FND-PRG-102: start a lab, check it, and stand in for a Git host and a key portal.

    uv run lab.py list                      the labs
    uv run lab.py start 1.2                 a fresh folder 1.2/ with the lab's starting state
    uv run lab.py start 1.2 --discard       start again; the old folder moves to _discarded/
    uv run lab.py check 1.2                 is the evidence of the lab there?
    uv run lab.py pr open <branch> "<title>" --as participant-a     (lab 2.2, the local hub)
    uv run lab.py pr list | show N | comment N "<text>" --as R | resolve N C --as R
    uv run lab.py pr approve N --as R | merge N --as R
    uv run lab.py keys list 3.4 | revoke 3.4 K-0002 | issue 3.4      (the key portal stand-in)
    uv run lab.py scan [--staged | --history] [folder]                (the course's secret scanner)

Python standard library and git only. Every practice commit the kit makes has a fixed author
(a role, never a person) and a fixed date, so commit ids are the same on every machine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE / "_kit" if (HERE / "_kit").is_dir() else HERE
WS = HERE if (HERE / "_kit").is_dir() else Path.cwd()
DATA = KIT / "data"
FILES = KIT / "files"
PROJECTS = KIT / "projects"
REF = json.loads((KIT / "reference.json").read_text(encoding="utf-8"))
TZ = timezone(timedelta(hours=3))
T0 = datetime(2026, 10, 5, 9, 0, tzinfo=TZ)

ROLES = {
    "analyst": ("The analyst", "analyst@example.invalid"),
    "technician": ("The field technician", "technician@example.invalid"),
    "reviewer": ("The reviewer", "reviewer@example.invalid"),
    "participant-a": ("Participant A", "participant-a@example.invalid"),
    "participant-b": ("Participant B", "participant-b@example.invalid"),
    "participant-c": ("Participant C", "participant-c@example.invalid"),
}
LEAKED_33 = "fprg102_demo_7f3ab9e1c4d2a8f05b6e9d1c"
LEAKED_34 = "fprg102_demo_e5a1d07bc93f4e28a6b1f0d4"

LABS = {
    "1.1": "Find your way round the project folder",
    "1.2": "A counting pipeline over synthetic logs",
    "1.3": "The counting script on a second folder, and a practice key",
    "1.4": "Draw the graph, then check it",
    "2.1": "Merge two branches and resolve a conflict alone",
    "2.2": "Branch, review and resolve a conflict in teams of three",
    "2.3": "Undo five mistakes",
    "2.4": "Rescue a project that fails on a second machine",
    "3.1": "One command, and data kept out of the code",
    "3.2": "Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace",
    "3.3": "The key out of the code",
    "3.4": "Remediate a seeded leaked key with a scanner and a commit hook",
}


# ---------------------------------------------------------------- helpers

def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, check: bool = True,
        stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, input=stdin)
    if check and done.returncode != 0:
        raise SystemExit(f"{' '.join(cmd)} failed in {cwd.name}:\n{done.stdout}{done.stderr}")
    return done


def git(repo: Path, *args: str, check: bool = True, env: dict[str, str] | None = None) -> str:
    return run(["git", "-c", "core.autocrlf=false", *args], repo, env=env, check=check).stdout.strip()


def who(role: str, when: datetime) -> dict[str, str]:
    name, mail = ROLES[role]
    stamp = when.strftime("%Y-%m-%dT%H:%M:%S+03:00")
    return dict(os.environ, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=mail, GIT_AUTHOR_DATE=stamp,
                GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=mail, GIT_COMMITTER_DATE=stamp)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def remove(path: Path) -> None:
    def onerror(func, p, _):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    if path.is_dir():
        shutil.rmtree(path, onerror=onerror)
    elif path.exists():
        os.chmod(path, stat.S_IWRITE)
        path.unlink()


def copy(src: Path, dst: Path) -> None:
    if src.is_dir():
        for f in sorted(src.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                out = dst / f.relative_to(src)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(f.read_bytes())
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())


def project(version: str, dst: Path) -> None:
    """Copy a version of the report project; 'gitignore' becomes '.gitignore', 'gitattributes' '.gitattributes'."""
    copy(PROJECTS / version, dst)
    for name in ("gitignore", "gitattributes"):
        if (dst / name).exists():
            (dst / name).replace(dst / f".{name}")


class Repo:
    """A practice repository whose commits have fixed roles and dates."""

    def __init__(self, path: Path, minutes: int = 0) -> None:
        self.path = path
        self.when = T0 + timedelta(minutes=minutes)
        path.mkdir(parents=True, exist_ok=True)
        git(path, "init", "-q", "-b", "main")
        git(path, "config", "core.autocrlf", "false")
        git(path, "config", "core.hooksPath", ".git/hooks")
        git(path, "config", "commit.gpgsign", "false")

    def commit(self, message: str, role: str, files: dict[str, str | None] | None = None) -> str:
        for rel, text in (files or {}).items():
            if text is None:
                git(self.path, "rm", "-q", rel)
            else:
                write(self.path / rel, text)
                git(self.path, "add", rel)
        self.when += timedelta(minutes=47)
        git(self.path, "commit", "-q", "--allow-empty-message", "-m", message, env=who(role, self.when))
        return git(self.path, "rev-parse", "--short", "HEAD")

    def merge(self, branch: str, message: str, role: str) -> None:
        self.when += timedelta(minutes=47)
        git(self.path, "merge", "-q", "--no-ff", "-m", message, branch, env=who(role, self.when))

    def identity(self, role: str) -> None:
        name, mail = ROLES[role]
        git(self.path, "config", "user.name", name)
        git(self.path, "config", "user.email", mail)


def bare_hub(path: Path, protected: bool = False) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "--bare", "-b", "main")
    git(path, "config", "core.hooksPath", "hooks")
    if protected:
        write(path / "hooks" / "pre-receive",
              "#!/bin/sh\n"
              "# Stands in for a protected main branch on the class Git host.\n"
              "while read old new ref; do\n"
              "  if [ \"$ref\" = refs/heads/main ] && [ \"$HUB_MERGE\" != 1 ]; then\n"
              "    echo \"refused: main is protected. Push a branch and open a pull request:\" >&2\n"
              "    echo \"  uv run ../../lab.py pr open <branch> \\\"<title>\\\" --as <role>\" >&2\n"
              "    exit 1\n"
              "  fi\n"
              "done\n")
        os.chmod(path / "hooks" / "pre-receive", 0o755)
    return path


def push_all(repo: Path, hub: Path) -> None:
    git(repo, "remote", "add", "origin", hub.resolve().as_posix())
    git(repo, "push", "-q", "--all", "origin", env=dict(os.environ, HUB_MERGE="1"))
    git(repo, "fetch", "-q", "origin")
    git(repo, "branch", "-q", "--set-upstream-to=origin/main", "main")


def bash() -> str:
    """Git's own Bash on Windows (never the WSL launcher); 'bash' elsewhere."""
    if os.name == "nt":
        exec_path = Path(run(["git", "--exec-path"], Path.cwd()).stdout.strip())
        for cand in (exec_path.parents[2] / "bin" / "bash.exe", exec_path.parents[2] / "usr" / "bin" / "bash.exe"):
            if cand.exists():
                return str(cand)
    return shutil.which("bash") or "bash"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


class Check:
    def __init__(self, lab: str) -> None:
        self.lab, self.missing = lab, 0

    def __call__(self, ok: bool, what: str, hint: str = "") -> bool:
        print(("  ok       " if ok else "  not yet  ") + what + ("" if ok or not hint else f"  ({hint})"))
        self.missing += 0 if ok else 1
        return ok

    def done(self) -> int:
        print(f"PASS lab {self.lab}" if not self.missing else f"NOT YET lab {self.lab}: {self.missing} to fix")
        return 0 if not self.missing else 1


# ---------------------------------------------------------------- Day 1

def start_11(d: Path) -> None:
    root = d / "air-reports"
    copy(DATA / "october", root / "logs" / "2026-10")
    copy(DATA / "november", root / "logs" / "2026-11")
    copy(FILES / "1.1", root)
    (root / "field notes").mkdir(exist_ok=True)
    (root / "visit-checklist.txt").replace(root / "field notes" / "visit-checklist.txt")
    copy(DATA / "listing.txt", root / "listing.txt")


def answers(path: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    if path.is_file():
        for m in re.finditer(r"(?m)^(\d+)\..*?\n\s*answer:\s*(.*)$", path.read_text(encoding="utf-8")):
            out[int(m.group(1))] = m.group(2).strip().lower()
    return out


def check_11(d: Path, c: Check) -> None:
    root = d / "air-reports"
    script = root / "run_counts.sh"
    text = script.read_text(encoding="utf-8") if script.exists() else ""
    c("/mnt/" not in text, "run_counts.sh no longer names a folder on one computer", "use the script's own folder")
    res = run([bash(), str(script.resolve())], cwd=d.parent, check=False) if text else None
    first = res.stdout.splitlines()[0].strip() if res and res.stdout else ""
    c(res is not None and res.returncode == 0 and first == str(REF["october"]["reading_lines"]),
      "run_counts.sh runs from another folder and prints the October reading lines first",
      res.stderr.strip().splitlines()[-1] if res and res.stderr.strip() else "run it from the workspace folder")
    c(res is not None and "checklist" in res.stdout.lower(), "it also prints the start of the visit checklist", "quote the folder with a space")
    a = answers(root / "answers.md")
    sizes = sorted(((p.stat().st_size, p.name) for p in (root / "logs" / "2026-10").glob("*.log")), reverse=True)
    c(a.get(1, "") == "12", "answer 1: the number of November logs")
    c(sizes and sizes[0][1].lower().removesuffix(".log") in a.get(2, ""), "answer 2: the largest October log")
    lst = REF["listing"]
    c(lst["world_writable"] in a.get(3, ""), "answer 3: the file every user can change")
    c(lst["not_executable_script"] in a.get(4, "") and "chmod" in a.get(4, ""), "answer 4: the script that will not run as ./name, and the command")
    c(lst["owner_only"] in a.get(5, ""), "answer 5: the file only its owner can read")


COUNT_RX = {
    2: re.compile(r"(\d+)\s+(OK|WARN|ERR)\b|\b(OK|WARN|ERR)\s+(\d+)"),
    3: re.compile(r"(\d+)\s+(ST\d\d)\b|\b(ST\d\d)\s+(\d+)"),
    4: re.compile(r"(\d+)\s+(ERR-E\d+)\b|\b(ERR-E\d+)\s+(\d+)"),
    6: re.compile(r"(\d+)\s+(Client [A-D])\b|\b(Client [A-D])\s+(\d+)"),
}


def parse_counts(out: str) -> dict[int, object]:
    sections: dict[int, list[str]] = {}
    cur = 0
    for line in out.replace("\r", "").splitlines():
        m = re.match(r"==\s*Q(\d)", line)
        if m:
            cur = int(m.group(1))
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    got: dict[int, object] = {}
    for q, lines in sections.items():
        text = "\n".join(lines)
        if q in (1, 5):
            m = re.search(r"\d+", text)
            got[q] = int(m.group(0)) if m else None
        else:
            pairs = {}
            for m in COUNT_RX[q].finditer(text):
                n, label = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
                pairs[label] = int(n)
            got[q] = pairs
    return got


def compare_counts(c: Check, got: dict[int, object], month: str, where: str) -> None:
    r = REF[month]
    c(got.get(1) == r["reading_lines"], f"{where} Q1 reading lines", "leave out comments and blank lines")
    c(got.get(2) == r["status"], f"{where} Q2 lines per status", "one of the logs has Windows line endings")
    c(got.get(3) == {k: v for k, v in r["top3_err_stations"]}, f"{where} Q3 the three stations with most ERR lines")
    c(got.get(4) == r["error_codes"], f"{where} Q4 error codes and their counts")
    c(got.get(5) == r["duplicate_lines"], f"{where} Q5 duplicate reading lines", "same station and hour seen twice")
    c(got.get(6) == r["stations_per_client"], f"{where} Q6 stations per client")


def start_12(d: Path) -> None:
    copy(DATA / "october", d / "logs")
    copy(FILES / "1.2" / "counts.sh", d / "counts.sh")


def check_12(d: Path, c: Check) -> None:
    res = run([bash(), "counts.sh"], cwd=d, check=False)
    c(res.returncode == 0, "counts.sh runs to the end", res.stderr.strip()[-200:])
    compare_counts(c, parse_counts(res.stdout), "october", "October:")
    saved = d / "counts.txt"
    c(saved.is_file() and parse_counts(saved.read_text(encoding="utf-8")) == parse_counts(res.stdout),
      "counts.txt holds the same output", "bash counts.sh > counts.txt")


def start_13(d: Path) -> None:
    copy(DATA / "october", d / "data" / "october")
    copy(DATA / "november", d / "data" / "november")
    copy(FILES / "1.3" / "counts.sh", d / "counts.sh")
    (d / "keys").mkdir(exist_ok=True)


def check_13(d: Path, c: Check) -> None:
    res = run([bash(), "counts.sh", "data/november"], cwd=d, check=False)
    c(res.returncode == 0, "bash counts.sh data/november runs", res.stderr.strip()[-200:])
    compare_counts(c, parse_counts(res.stdout), "november", "November:")
    env = dict(os.environ, AIR_LOGS="data/october")
    res = run([bash(), "counts.sh"], cwd=d, env=env, check=False)
    got = parse_counts(res.stdout)
    c(got.get(1) == REF["october"]["reading_lines"], "with no argument it reads the folder in AIR_LOGS")
    res = run([bash(), "counts.sh", "data/missing"], cwd=d, check=False)
    c(res.returncode == 2 and res.stderr.strip() != "", "a missing folder ends with exit code 2 and a message on stderr")
    pub = d / "keys" / "practice_key.pub"
    c(pub.is_file() and pub.read_text(encoding="utf-8").startswith("ssh-ed25519 "), "keys/practice_key.pub is an Ed25519 public key")
    fp = d / "keys" / "fingerprint.txt"
    c(fp.is_file() and "SHA256:" in fp.read_text(encoding="utf-8"), "keys/fingerprint.txt holds its fingerprint")
    cfg = (d / "ssh_config").read_text(encoding="utf-8") if (d / "ssh_config").exists() else ""
    c(all(k in cfg for k in ("Host ", "HostName ", "User ", "IdentityFile ")), "ssh_config has Host, HostName, User and IdentityFile")


def start_14(d: Path) -> None:
    r = Repo(d / "practice")
    r.commit("Start the settings notes", "analyst", {"settings.txt": "# Settings of the client report\n"})
    r.identity("participant-a")
    copy(FILES / "1.4" / "sequences.md", d / "sequences.md")
    copy(FILES / "1.4" / "graphs.md", d / "graphs.md")


def check_14(d: Path, c: Check) -> None:
    p = d / "practice"
    count = lambda ref: int(git(p, "rev-list", "--count", ref, check=False) or 0)  # noqa: E731
    branches = git(p, "branch", "--format=%(refname:short)").split()
    c(count("main") == 6, "main reaches 6 commits after the three sequences", f"it reaches {count('main')}")
    c("review-notes" in branches and count("review-notes") == 6, "review-notes reaches 6 commits")
    c(int(git(p, "rev-list", "--count", "--all")) == 7, "7 commits in all: the two branches share 5")
    c(git(p, "symbolic-ref", "--short", "HEAD") == "main", "HEAD points at main")
    c(git(p, "status", "--porcelain") == "", "nothing left unstaged or uncommitted")
    a = answers(d / "graphs.md")
    c(a.get(1) == "3" and a.get(2) == "5", "predictions 1 and 2 written and right", "count the commits main reaches")
    c(a.get(3) == "7" and "main" in a.get(4, ""), "predictions 3 and 4 written and right")


# ---------------------------------------------------------------- Day 2

REPORT_MD = ("# Monthly air-quality report\n\nClient: {client}\nAlert threshold: PM10 above 150\n"
             "Stations: {stations}\n\nOne row per station follows.\n")


def start_21(d: Path) -> None:
    r = Repo(d / "report-repo")
    r.commit("Add the report template", "analyst", {"client_report.md": REPORT_MD})
    git(r.path, "switch", "-q", "-c", "fix/threshold-wording")
    r.commit("Say that the threshold is the company's own rule", "analyst",
             {"client_report.md": REPORT_MD.replace("Alert threshold: PM10 above 150", "Alert threshold: PM10 above 150 (the company's own rule)")})
    git(r.path, "switch", "-q", "main")
    git(r.path, "switch", "-q", "-c", "feature/sector-line")
    r.commit("Add the sector line and say the threshold is an hourly mean", "technician",
             {"client_report.md": REPORT_MD.replace("Client: {client}\n", "Client: {client}\nSector: {sector}\n")
              .replace("Alert threshold: PM10 above 150", "Alert threshold: hourly mean PM10 above 150")})
    git(r.path, "switch", "-q", "main")
    push_all(r.path, bare_hub(d / "hub" / "report.git"))
    r.identity("participant-a")


def check_21(d: Path, c: Check) -> None:
    p = d / "report-repo"
    text = (p / "client_report.md").read_text(encoding="utf-8")
    c(not re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M), "no conflict markers left")
    c("Sector: {sector}" in text, "the technician's sector line survived")
    c("own rule" in text and "hourly mean" in text, "both changes to the threshold line survived in one line")
    parents = git(p, "log", "-1", "--format=%P", "main").split()
    c(len(parents) == 2, "the last commit on main is a merge commit with two parents")
    for b in ("fix/threshold-wording", "feature/sector-line"):
        ok = run(["git", "merge-base", "--is-ancestor", b, "main"], p, check=False).returncode == 0
        c(ok, f"{b} is part of main")
    git(p, "fetch", "-q", "origin", check=False)
    c(git(p, "rev-parse", "main") == git(p, "rev-parse", "origin/main", check=False), "main is pushed to the hub")


RULES_MD = ("# Rules of the monthly client report\n\n"
            "1. A reading hour counts once, even when the logger sends it twice.\n"
            "2. An alert hour is an hour with PM10 above 150 (the company's own rule).\n"
            "3. Error hours are listed, never filled in.\n")


def start_22(d: Path) -> None:
    seed = Repo(d / "_seed")
    seed.commit("Add the report rules", "analyst", {"rules.md": RULES_MD})
    hub = bare_hub(d / "hub" / "team-report.git", protected=True)
    push_all(seed.path, hub)
    remove(seed.path)
    (d / "hub" / "pulls").mkdir(parents=True, exist_ok=True)
    for role in ("participant-a", "participant-b", "participant-c"):
        target = d / role
        # -c applies before the checkout: on Windows, Git's default core.autocrlf=true would
        # otherwise check rules.md out with CR LF and every edit would rewrite all its lines
        run(["git", "clone", "-q", "-c", "core.autocrlf=false", hub.resolve().as_posix(), str(target)], d)
        git(target, "config", "core.hooksPath", ".git/hooks")
        name, mail = ROLES[role]
        git(target, "config", "user.name", name)
        git(target, "config", "user.email", mail)


def pulls_dir() -> Path:
    p = WS / "2.2" / "hub" / "pulls"
    if not p.is_dir():
        raise SystemExit("no hub: run  uv run lab.py start 2.2  first")
    return p


def load_pr(n: int) -> dict:
    f = pulls_dir() / f"{n:03d}.json"
    if not f.exists():
        raise SystemExit(f"no pull request #{n}")
    return json.loads(f.read_text(encoding="utf-8"))


def save_pr(pr: dict) -> None:
    write(pulls_dir() / f"{pr['number']:03d}.json", json.dumps(pr, indent=2) + "\n")


def hub_git(*args: str, check: bool = True) -> str:
    return git(WS / "2.2" / "hub" / "team-report.git", *args, check=check)


def cmd_pr(a: argparse.Namespace) -> int:
    role = a.as_role
    if a.action == "list":
        for f in sorted(pulls_dir().glob("*.json")):
            pr = json.loads(f.read_text(encoding="utf-8"))
            print(f"#{pr['number']}  {pr['state']:<7} {pr['branch']:<28} {pr['title']}  ({ROLES[pr['author']][0]})")
        return 0
    if a.action == "open":
        branch, title = a.args[0], " ".join(a.args[1:]) or a.args[0]
        if not hub_git("rev-parse", "--verify", "-q", f"refs/heads/{branch}", check=False):
            raise SystemExit(f"the hub has no branch {branch}: push it first (git push -u origin {branch})")
        n = len(list(pulls_dir().glob("*.json"))) + 1
        save_pr({"number": n, "branch": branch, "title": title, "author": role, "state": "open",
                 "comments": [], "approved_at": None, "approved_by": None})
        print(f"opened pull request #{n}: {branch} into main")
        return 0
    pr = load_pr(int(a.args[0]))
    tip = hub_git("rev-parse", f"refs/heads/{pr['branch']}")
    if a.action == "show":
        print(f"#{pr['number']} {pr['title']}  [{pr['state']}]  by {ROLES[pr['author']][0]}")
        print(hub_git("log", "--oneline", f"main..{pr['branch']}"))
        print(hub_git("diff", f"main...{pr['branch']}"))
        for i, cm in enumerate(pr["comments"], 1):
            print(f"  comment {i} by {ROLES[cm['by']][0]}{' (resolved)' if cm['resolved'] else ''}: {cm['text']}")
        if pr["approved_by"]:
            print(f"  approved by {ROLES[pr['approved_by']][0]} at {pr['approved_at'][:7]}")
        return 0
    if pr["state"] != "open":
        raise SystemExit(f"pull request #{pr['number']} is {pr['state']}")
    if a.action == "comment":
        text = " ".join(a.args[1:])
        pr["comments"].append({"by": role, "text": text, "at": tip, "resolved": False})
        save_pr(pr)
        print(f"comment {len(pr['comments'])} on #{pr['number']}")
        return 0
    if a.action == "resolve":
        i = int(a.args[1]) - 1
        cm = pr["comments"][i]
        if role != pr["author"]:
            raise SystemExit("only the author of the pull request resolves a comment, after addressing it")
        if cm["at"] == tip:
            raise SystemExit("push a commit that addresses the comment first: the branch has not changed since it was written")
        cm["resolved"] = True
        save_pr(pr)
        print(f"comment {i + 1} resolved")
        return 0
    if a.action == "approve":
        if role == pr["author"]:
            raise SystemExit("an author cannot approve their own pull request")
        if any(not cm["resolved"] for cm in pr["comments"]):
            raise SystemExit("unresolved comments: the author addresses and resolves them first")
        pr["approved_by"], pr["approved_at"] = role, tip
        save_pr(pr)
        print(f"#{pr['number']} approved at {tip[:7]}")
        return 0
    if a.action == "merge":
        if pr["approved_at"] != tip:
            raise SystemExit("not approved at the branch's last commit: ask for a review of the new commits")
        work = Path(tempfile.mkdtemp(prefix="merge-", dir=WS / "2.2" / "hub"))
        try:
            hub = (WS / "2.2" / "hub" / "team-report.git").resolve().as_posix()
            run(["git", "clone", "-q", "-c", "core.autocrlf=false", hub, str(work / "w")], WS)
            w = work / "w"
            env = who(role, T0 + timedelta(days=1, minutes=10 * pr["number"]))
            res = run(["git", "-c", "core.autocrlf=false", "merge", "--no-ff", "-m",
                       f"Merge pull request #{pr['number']}: {pr['title']}", f"origin/{pr['branch']}"], w, env=env, check=False)
            if res.returncode != 0:
                raise SystemExit("conflict: this branch no longer merges cleanly into main.\n"
                                 "The author merges main into the branch, resolves, commits and pushes; then review again.")
            run(["git", "push", "-q", "origin", "main"], w, env=dict(os.environ, HUB_MERGE="1"))
        finally:
            remove(work)
        pr["state"] = "merged"
        save_pr(pr)
        print(f"#{pr['number']} merged into main")
        return 0
    raise SystemExit(f"unknown action {a.action}")


def check_22(d: Path, c: Check) -> None:
    hub = d / "hub" / "team-report.git"
    prs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((d / "hub" / "pulls").glob("*.json"))]
    merged = [p for p in prs if p["state"] == "merged"]
    c(len(merged) >= 2, "two pull requests merged", f"{len(merged)} merged")
    c(all(p["comments"] for p in merged), "every merged request has at least one review comment")
    c(all(cm["resolved"] for p in merged for cm in p["comments"]), "every comment addressed and resolved")
    c(all(p["approved_by"] and p["approved_by"] != p["author"] for p in merged), "each approved by someone other than its author")
    merges_on_branches = 0
    for p in merged:
        for line in git(hub, "log", "--format=%H %P", f"main^1..{p['branch']}", check=False).splitlines():
            if len(line.split()) == 3:
                merges_on_branches += 1
    c(merges_on_branches >= 1, "a branch carries the merge of main that resolved the conflict")
    text = git(hub, "show", "main:rules.md", check=False)
    c(not re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.M), "no conflict markers on main")
    c(len(re.findall(r"(?m)^\d+\. ", text)) >= 5, "main's rules.md keeps both new rules", "five numbered rules or more")


def start_23(d: Path) -> None:
    r = Repo(d / "report-repo")
    r.commit("Add the report template", "analyst", {"client_report.md": REPORT_MD})
    r.commit("Add the stations list", "analyst", {"stations.md": "".join(f"- ST{i:02d}\n" for i in range(1, 13))})
    r.commit("Change the threshold to 100", "analyst",
             {"client_report.md": REPORT_MD.replace("PM10 above 150", "PM10 above 100")})
    git(r.path, "switch", "-q", "-c", "draft/winter-notes")
    r.commit("Draft the winter notes", "analyst", {"winter.md": "Dust events are rarer from December.\n"})
    git(r.path, "switch", "-q", "main")
    push_all(r.path, bare_hub(d / "hub" / "report.git"))
    git(r.path, "push", "-q", "origin", "--delete", "draft/winter-notes")
    git(r.path, "branch", "-q", "-D", "draft/winter-notes")
    r.commit("Add sectr line", "analyst",
             {"client_report.md": REPORT_MD.replace("PM10 above 150", "PM10 above 100").replace("\nClient: {client}\n", "\nSector: {sector}\nClient: {client}\n")})
    write(r.path / "sectors.md", "North, South, East, West, Central\n")
    r.commit("Add debug output", "analyst", {"debug.txt": "DEBUG: rows read 8892\n"})
    write(r.path / "scratch.txt", "notes to self, not for the repository\n")
    git(r.path, "add", "scratch.txt")
    with (r.path / "client_report.md").open("a", encoding="utf-8", newline="\n") as f:
        f.write("TEMPORARY LINE: delete me\n")
    r.identity("participant-a")


def check_23(d: Path, c: Check) -> None:
    p = d / "report-repo"
    tracked = git(p, "ls-files").split()
    status = git(p, "status", "--porcelain")
    c("scratch.txt" not in tracked and "A  scratch.txt" not in status, "scratch.txt is not staged or tracked")
    c("TEMPORARY LINE" not in (p / "client_report.md").read_text(encoding="utf-8"), "the stray line in client_report.md is gone")
    subjects = git(p, "log", "--format=%s", "main").splitlines()
    c("Add debug output" not in subjects, "the local debug commit is gone from main")
    c("Add sector line" in subjects and "Add sectr line" not in subjects, "the sector commit has the right message")
    c("sectors.md" in git(p, "show", "--name-only", "--format=", ":/Add sector line", check=False), "the sector commit includes sectors.md")
    c(any(s.startswith('Revert "Change the threshold to 100"') for s in subjects), "the pushed threshold change is reverted with a new commit")
    c("PM10 above 150" in (p / "client_report.md").read_text(encoding="utf-8"), "the threshold reads 150 again")
    git(p, "fetch", "-q", "origin", check=False)
    c(git(p, "rev-parse", "main") == git(p, "rev-parse", "origin/main", check=False), "main is pushed: the revert is on the hub")
    c(git(p, "log", "-1", "--format=%s", "draft/winter-notes", check=False) == "Draft the winter notes", "draft/winter-notes is back")


def start_24(d: Path) -> None:
    r = Repo(d / "first-machine" / "air-report")
    project("v1", r.path)
    git(r.path, "add", "-A")
    r.when += timedelta(minutes=47)
    git(r.path, "commit", "-q", "-m", "Add the monthly client report", env=who("analyst", r.when))
    copy(DATA / "october", d / "data")


def check_24(d: Path, c: Check) -> None:
    p = d / "second-machine"
    c(p.is_dir() and (p / ".git").is_dir(), "second-machine/ is a clone of the project")
    if not p.is_dir():
        return
    py = (p / "pyproject.toml").read_text(encoding="utf-8") if (p / "pyproject.toml").exists() else ""
    c("tabulate" in py and "python-dateutil" in py, "pyproject.toml declares both dependencies")
    tracked = git(p, "ls-files").split()
    c("uv.lock" in tracked, "uv.lock is committed")
    c("/mnt/" not in (p / "report.py").read_text(encoding="utf-8"), "report.py takes its data folder from outside the code")
    with tempfile.TemporaryDirectory(dir=d) as tmp:
        clone = Path(tmp) / "third-machine"
        run(["git", "clone", "-q", str(p), str(clone)], d)
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV" and k != "UV_PROJECT_ENVIRONMENT"}
        ok = run(["uv", "sync", "--locked", "-q"], clone, env=env, check=False)
        c(ok.returncode == 0, "a fresh clone rebuilds with uv sync --locked", ok.stderr.strip()[-200:])
        res = run(["uv", "run", "-q", "python", "report.py", "--data", str((d / "data").resolve())], clone, env=env, check=False)
        c(sha(clone / "output" / "report.csv") == REF["october"]["report_sha256"],
          "the fresh clone writes the expected October report", (res.stderr.strip() or "no output/report.csv")[-300:])


# ---------------------------------------------------------------- Day 3

def locked_project(d: Path, version: str = "v2") -> Path:
    project(version, d)
    return d


def start_31(d: Path) -> None:
    r = Repo(d / "air-report")
    project("v2", r.path)
    write(r.path / ".gitignore", "__pycache__/\n.venv/\n")
    copy(FILES / "3.1" / "README.md", r.path / "README.md")
    copy(DATA / "october", r.path / "data")
    copy(PROJECTS / ".." / "expected_report_october.csv", r.path / "output" / "report.csv")
    git(r.path, "add", "-A")
    r.when += timedelta(minutes=47)
    git(r.path, "commit", "-q", "-m", "Add the locked report project with its data and output", env=who("analyst", r.when))
    copy(DATA / "october", d / "data")
    r.identity("participant-a")


def check_31(d: Path, c: Check) -> None:
    p = d / "air-report"
    tracked = git(p, "ls-files").splitlines()
    c(not any(t.startswith(("data/", "output/")) for t in tracked), "no data or output file is tracked")
    ign = (p / ".gitignore").read_text(encoding="utf-8") if (p / ".gitignore").exists() else ""
    c("output" in ign and "data" in ign, ".gitignore keeps data/ and output/ out")
    c("rebuild.sh" in tracked, "rebuild.sh is committed")
    readme = (p / "README.md").read_text(encoding="utf-8") if (p / "README.md").exists() else ""
    c("## Reproduce" in readme and "rebuild.sh" in readme, "README has a Reproduce section naming the one command")
    c("expected/october.sha256" in tracked, "the expected checksum is committed")
    c(git(p, "status", "--porcelain") == "", "everything is committed")
    with tempfile.TemporaryDirectory(dir=d) as tmp:
        clone = Path(tmp) / "clean"
        run(["git", "clone", "-q", str(p), str(clone)], d)
        env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT")}
        env["AIR_LOGS"] = str((d / "data").resolve())
        res = run([bash(), "rebuild.sh"], clone, env=env, check=False) if (clone / "rebuild.sh").exists() else None
        c(res is not None and res.returncode == 0 and sha(clone / "output" / "report.csv") == REF["october"]["report_sha256"],
          "a clean clone rebuilds with AIR_LOGS set and its checksum matches",
          (res.stdout + res.stderr).strip()[-300:] if res else "no rebuild.sh")
        bad = run([bash(), "rebuild.sh"], clone, env={k: v for k, v in env.items() if k != "AIR_LOGS"}, check=False) if res else None
        c(bad is not None and bad.returncode != 0, "without AIR_LOGS it stops with an error instead of guessing")


def start_32(d: Path) -> None:
    r = Repo(d / "air-report")
    project("v3", r.path)
    copy(FILES / "3.2" / "Containerfile", r.path / "Containerfile")
    copy(FILES / "3.2" / "containerignore", r.path / ".containerignore")
    git(r.path, "add", "-A")
    r.when += timedelta(minutes=47)
    git(r.path, "commit", "-q", "-m", "Add a container definition to complete", env=who("analyst", r.when))
    copy(DATA / "october", d / "data")
    r.identity("participant-a")


def engine() -> str | None:
    for e in ("podman", "docker"):
        if shutil.which(e) and run([e, "info"], Path.cwd(), check=False).returncode == 0:
            return e
    return None


def check_32(d: Path, c: Check) -> None:
    p = d / "air-report"
    cf = (p / "Containerfile").read_text(encoding="utf-8") if (p / "Containerfile").exists() else ""
    lines = [ln.strip() for ln in cf.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    c(any(ln.startswith("FROM ") for ln in lines), "a FROM line names the base image")
    c(any(ln.startswith("COPY ") and "requirements.txt" in ln for ln in lines), "the locked requirements are copied before the code")
    c(any(ln.startswith("RUN ") and "--require-hashes" in ln for ln in lines), "packages install with --require-hashes from the lock")
    c(any(ln.startswith("USER ") and ln.split()[1] not in ("root", "0") for ln in lines), "the program runs as a user that is not root")
    c(any(ln.startswith(("ENTRYPOINT", "CMD")) and "/data" in ln for ln in lines), "the program reads the mounted /data folder")
    req = p / "requirements.txt"
    c(req.is_file() and "--hash=sha256:" in req.read_text(encoding="utf-8"), "requirements.txt is exported from uv.lock with hashes")
    c("requirements.txt" in git(p, "ls-files"), "requirements.txt is committed")
    out = p / "output" / "report.csv"
    eng = engine()
    if eng:
        c(sha(out) == REF["october"]["report_sha256"], f"output/report.csv written by the container ({eng}) matches")
    else:
        print("  note     no container engine answers here: the definition was checked, the run was not")


def start_33(d: Path) -> None:
    r = Repo(d / "air-report")
    project("v3", r.path)
    copy(FILES / "3.2" / "Containerfile.solution", r.path / "Containerfile")
    copy(FILES / "3.3" / "report.py", r.path / "report.py")
    git(r.path, "add", "-A")
    r.when += timedelta(minutes=47)
    git(r.path, "commit", "-q", "-m", "Upload the report to the client portal", env=who("analyst", r.when))
    copy(DATA / "october", d / "data")
    write(d / "portal" / "keys.json", json.dumps({LEAKED_33: {"id": "K-0003", "state": "active"}}, indent=2) + "\n")
    r.identity("participant-a")


def check_33(d: Path, c: Check) -> None:
    p = d / "air-report"
    hits = scan_paths(p, [Path(f) for f in git(p, "ls-files").splitlines()])
    c(not hits, "no key in any tracked file", hits[0] if hits else "")
    ex = p / ".env.example"
    c(ex.is_file() and re.search(r"(?m)^AIR_PORTAL_KEY=\s*$", ex.read_text(encoding="utf-8")) is not None,
      ".env.example names AIR_PORTAL_KEY with no value")
    c(run(["git", "check-ignore", "-q", ".env"], p, check=False).returncode == 0, ".env is ignored by git")
    c(".env.example" in git(p, "ls-files"), ".env.example is committed")
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "UV_PROJECT_ENVIRONMENT", "AIR_PORTAL_KEY")}
    env["AIR_PORTAL_DIR"] = str((d / "portal").resolve())
    res = run(["uv", "run", "-q", "python", "report.py", "--data", str((d / "data").resolve()), "--upload"], p, env=env, check=False)
    c(res.returncode == 2 and "AIR_PORTAL_KEY" in res.stderr, "without the variable it stops with exit 2 and names AIR_PORTAL_KEY")
    env["AIR_PORTAL_KEY"] = LEAKED_33
    res = run(["uv", "run", "-q", "python", "report.py", "--data", str((d / "data").resolve()), "--upload"], p, env=env, check=False)
    c(res.returncode == 0 and any((d / "portal" / "inbox").glob("*.csv")), "with the variable set the upload works", res.stderr.strip()[-200:])
    c(LEAKED_33 not in res.stdout + res.stderr, "the key is never printed in full")
    found = git(p, "log", "--all", "--format=%h", "-S", LEAKED_33)
    c(bool(found), "the key is still in an old commit: lab 3.4 deals with that", "")


def start_34(d: Path) -> None:
    r = Repo(d / "air-report")
    project("v3", r.path)
    copy(FILES / "3.2" / "Containerfile.solution", r.path / "Containerfile")
    git(r.path, "add", "-A")
    r.commit("Add the reproducible report project", "analyst")
    r.commit("Add the portal settings", "analyst",
             {"settings.toml": f'[portal]\nurl = "https://portal.example.invalid/upload"\nkey = "{LEAKED_34}"\n'})
    r.commit("Upload the report to the client portal", "analyst",
             {"report.py": (FILES / "3.3" / "report.solution.py").read_text(encoding="utf-8")})
    r.commit("Read the portal key from the environment", "analyst",
             {"settings.toml": None, ".env.example": "AIR_PORTAL_KEY=\n"})
    r.commit("Add the secret scanner and its rules", "analyst",
             {"tools/scan_secrets.py": (KIT / "scan_secrets.py").read_text(encoding="utf-8"),
              ".gitleaks.toml": (FILES / "3.4" / "gitleaks.toml").read_text(encoding="utf-8"),
              ".pre-commit-config.yaml": (FILES / "3.4" / "pre-commit-config.yaml").read_text(encoding="utf-8")})
    r.commit("Describe the portal upload in the README", "analyst",
             {"README.md": (PROJECTS / "v3" / "README.md").read_text(encoding="utf-8") +
              "\n## Upload\n\nSet `AIR_PORTAL_KEY` (see `.env.example`), then add `--upload`.\n"})
    push_all(r.path, bare_hub(d / "hub" / "air-report.git"))
    write(d / "portal" / "keys.json", json.dumps({LEAKED_34: {"id": "K-0002", "state": "active"}}, indent=2) + "\n")
    copy(DATA / "october", d / "data")
    copy(FILES / "3.4" / "ROTATION.md", d / "ROTATION-template.md")
    r.identity("participant-a")
    # pre-commit refuses to install while core.hooksPath is set, so this repository goes back
    # to Git's default hooks folder; a hooksPath set for the whole machine still applies
    git(r.path, "config", "--unset", "core.hooksPath")


def check_34(d: Path, c: Check) -> None:
    p = d / "air-report"
    hist = scan_history(p)
    c(not hist, "the secret scan of the whole history passes", hist[0] if hist else "")
    keys = json.loads((d / "portal" / "keys.json").read_text(encoding="utf-8"))
    c(keys.get(LEAKED_34, {}).get("state") == "revoked", "the leaked key K-0002 is revoked")
    active = [k for k, v in keys.items() if v["state"] == "active"]
    c(len(active) == 1, "exactly one new key is active")
    envf = p / ".env"
    c(bool(active) and envf.is_file() and active[0] in envf.read_text(encoding="utf-8"), "the new key is in .env")
    c(run(["git", "check-ignore", "-q", ".env"], p, check=False).returncode == 0 and ".env" not in git(p, "ls-files").split(),
      ".env is ignored and untracked")
    rot = git(p, "show", "HEAD:ROTATION.md", check=False)
    c(all(h in rot for h in ("## What leaked", "## Rotated", "## History cleaned", "## Who was told")), "ROTATION.md is committed with its four sections")
    c(LEAKED_34 not in rot and (not active or active[0] not in rot), "ROTATION.md names the key by its id, never by its value")
    git(p, "fetch", "-q", "origin", check=False)
    c(git(p, "rev-parse", "main") == git(p, "rev-parse", "origin/main", check=False), "the cleaned history is pushed to the hub")
    hub_hist = scan_history(d / "hub" / "air-report.git")
    c(not hub_hist, "the hub's history is clean too")
    hook = p / ".git" / "hooks" / "pre-commit"
    c(hook.is_file(), "a pre-commit hook is installed")
    if hook.is_file():
        probe = p / "probe_settings.toml"
        write(probe, 'key = "fprg102_demo_' + "ab" * 12 + '"\n')
        git(p, "add", probe.name)
        res = run(["git", "commit", "-q", "-m", "probe"], p, check=False)
        blocked = res.returncode != 0
        if not blocked:
            git(p, "reset", "-q", "--soft", "HEAD~1")
        git(p, "reset", "-q", "--", probe.name)
        probe.unlink()
        c(blocked, "the hook blocks a commit that holds a key")


# ---------------------------------------------------------------- scanner and keys

def _scanner():
    sys.path.insert(0, str(KIT))
    import scan_secrets  # noqa: PLC0415
    return scan_secrets


def scan_paths(root: Path, files: list[Path]) -> list[str]:
    return _scanner().scan_files(root, files)


def scan_history(repo: Path) -> list[str]:
    return _scanner().scan_history(repo)


def cmd_keys(a: argparse.Namespace) -> int:
    f = WS / a.lab / "portal" / "keys.json"
    if not f.exists():
        raise SystemExit(f"no portal for lab {a.lab}: start the lab first")
    keys = json.loads(f.read_text(encoding="utf-8"))
    if a.action == "list":
        for k, v in keys.items():
            print(f"{v['id']}  {v['state']:<8} {k[:13]}...{k[-4:]}")
    elif a.action == "revoke":
        hit = [k for k, v in keys.items() if v["id"] == a.key_id]
        if not hit:
            raise SystemExit(f"no key {a.key_id}")
        keys[hit[0]]["state"] = "revoked"
        print(f"{a.key_id} revoked: the portal refuses it from now on")
    elif a.action == "issue":
        new = "fprg102_demo_" + secrets.token_hex(12)
        keys[new] = {"id": f"K-{len(keys) + 1:04d}", "state": "active"}
        print(f"issued {keys[new]['id']}; copy this value into .env now, it is shown once:\n{new}")
    write(f, json.dumps(keys, indent=2) + "\n")
    return 0


# ---------------------------------------------------------------- command line

STARTS = {k: globals()[f"start_{k.replace('.', '')}"] for k in LABS}
CHECKS = {k: globals()[f"check_{k.replace('.', '')}"] for k in LABS}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lab.py", description="Start and check the labs of FND-PRG-102.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("start")
    s.add_argument("lab", choices=LABS)
    s.add_argument("--discard", action="store_true")
    s = sub.add_parser("check")
    s.add_argument("lab", choices=LABS)
    s = sub.add_parser("pr")
    s.add_argument("action", choices=["open", "list", "show", "comment", "resolve", "approve", "merge"])
    s.add_argument("args", nargs="*")
    s.add_argument("--as", dest="as_role", choices=ROLES, default="participant-a")
    s = sub.add_parser("keys")
    s.add_argument("action", choices=["list", "revoke", "issue"])
    s.add_argument("lab", choices=["3.3", "3.4"])
    s.add_argument("key_id", nargs="?")
    s = sub.add_parser("scan")
    s.add_argument("folder", nargs="?", default=".")
    s.add_argument("--staged", action="store_true")
    s.add_argument("--history", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "list":
        for k, v in LABS.items():
            print(f"{k}  {v}{'  (started)' if (WS / k).exists() else ''}")
        return 0
    if a.cmd == "start":
        d = WS / a.lab
        if d.exists():
            if not a.discard:
                raise SystemExit(f"{a.lab}/ exists. To start again, add --discard (it moves to _discarded/).")
            n = 1
            while (WS / "_discarded" / f"{a.lab}-{n}").exists():
                n += 1
            (WS / "_discarded").mkdir(exist_ok=True)
            shutil.move(str(d), str(WS / "_discarded" / f"{a.lab}-{n}"))
        d.mkdir(parents=True)
        STARTS[a.lab](d)
        print(f"lab {a.lab} ready in {a.lab}/: {LABS[a.lab]}")
        return 0
    if a.cmd == "check":
        d = WS / a.lab
        if not d.exists():
            raise SystemExit(f"lab {a.lab} not started: uv run lab.py start {a.lab}")
        print(f"lab {a.lab}: {LABS[a.lab]}")
        c = Check(a.lab)
        CHECKS[a.lab](d, c)
        return c.done()
    if a.cmd == "pr":
        return cmd_pr(a)
    if a.cmd == "keys":
        return cmd_keys(a)
    if a.cmd == "scan":
        return _scanner().main(["--staged"] * a.staged + ["--history"] * a.history + [a.folder])
    return 1


if __name__ == "__main__":
    sys.exit(main())
