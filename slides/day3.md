---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/slides/day3.html"
---

# Command Line, Git and Reproducible Environments

## Day 3: Rebuild anywhere, leak nothing

One documented command, a container with mounted data, and keys kept out of history

#### [day3#title] Rebuild anywhere, leak nothing

*SDAIA Academy · Command Line, Git and Reproducible Environments*

Day 3: One documented command, a container with mounted data, and keys kept out of history

Data & AI Foundations Track · 3 teaching days + capstone day · 4 sessions · 4 labs · FND-PRG-102

#### [day3#agenda] Rebuild anywhere, leak nothing

*Today*

- **Session 1 · One command to rebuild and run**: A reader rebuilds the result with one documented command, and the repository holds code, not data or outputs
- **Session 2 · Images, containers and volumes**: An image is built once from a short definition; each run is a container that sees only what you mount
- **Session 3 · What a container shares**: A container shares the kernel, the mounts and every variable you pass it; a key belongs in the environment, never in the code
- **Session 4 · Scanning, and after a leak**: Scan before every commit; after a leak, rotate first, then clean the history and report

#### [day3#review-day2] Which command leaves your own main where it was?

*Review of Day 2*

**Question:** A teammate pushed to the hub. You want to see their commits before anything in your clone changes. Which command?

- A. git pull
- B. git merge origin/main
- C. git push
- D. git fetch

#### [day3#debrief-2-4] The second machine failed four times before the lock fixed it

*Lab 2.4 debrief*

| Attempt | Last line of the error |
| --- | --- |
| Nothing installed | `ModuleNotFoundError: No module named 'dateutil'` |
| With requirements.txt | the same: the file listed tabulate only |
| With both packages | `FileNotFoundError` on the analyst's absolute path |
| With the path fixed | `FileNotFoundError` on `output/report.csv` |
| From the lock, fresh | 12 stations written; checksum as expected |

### Session 1: One command to rebuild and run

#### [day3#s1] One command to rebuild and run

*Session 1*

- Keep data and outputs out of the repository and say where they come from
- Write one documented command that rebuilds and checks the result
- Test a README by following it in a clean clone

#### [day3#what-belongs] Code and the recipe go in; data, outputs and environments stay out

*What a repository holds*

- **In the repository.** Source, `pyproject.toml` and the lock, the container definition, the rebuild command, the README, small expected checksums, a `.env.example`.
- **Out of it.** Raw data (it has its own home and its own rules), outputs (rebuilt), `.venv/` (rebuilt), `.env` (secret), caches.

> **.gitignore does not untrack.** A file already committed stays tracked until `git rm --cached` removes it from the index.

#### [day3#data-path-outside] The code asks where the data is; the README says where to get it

*Where the data comes from*

```python
# file: planner.py
ap.add_argument("--data", default=os.environ.get("VISITS_DIR"))
...
if not args.data:
    print("error: give --data <folder> or set VISITS_DIR", file=sys.stderr)
    return 2
```

- No default path that exists on one computer only
- A clear stop beats a silent empty result

#### [day3#one-command] One documented command rebuilds, runs and checks

*One command*

```bash
# file: rebuild.sh (a field-visit planner)
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${VISITS_DIR:?set VISITS_DIR to the folder of visit logs}"
uv sync --locked --quiet
uv run --quiet python planner.py --data "$VISITS_DIR" --out output
sha256sum -c expected/march.sha256
```

> **The last line is the test.** `sha256sum -c` prints `OK` or `FAILED` and sets the exit code.

#### [day3#checksum] A checksum turns "it ran" into "it gave the same bytes"

*Did it reproduce?*

- Running without an error proves little: an empty input also runs
- A checksum of the expected output, committed, is a precise answer
- When it fails, compare the first rows to see where the difference starts
- Outputs that hold a date or a random number need those fixed first

**64** hexadecimal characters in a SHA-256 checksum: one changed byte changes them all

#### [day3#readme-reproduce] A Reproduce section answers four questions and assumes nothing

*The README*

- **The four answers.**
  - Which tools, and which versions at least
  - Where the data comes from
  - The one command
  - What success looks like
- **What a peer cannot know.**
  - A folder on your laptop
  - A package you installed once
  - A variable in your shell profile
  - A step you always do without thinking

#### [day3#check-data-path] Where does the data path belong?

*Checkpoint*

**Question:** A planner project reads its visit logs from a folder. A peer will rebuild it on a clean workspace. Where should the folder's location come from?

- A. A default path in the code, the author's own folder
- B. An argument or a variable, with the README saying where to get the data
- C. The repository itself, in a data/ folder
- D. A chat message to the peer before the rebuild

#### [day3#lab-3-1] One command, and data kept out of the code

Lab 3.1 · 35 min

Addition: data and output out of the repository, one rebuild command with a checksum, a README tested in a clean clone

[D3_1_one_command.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_1_one_command.html)

- [ ] List what the repository carries with git ls-files (4 min)
- [ ] Stop tracking data and output: git rm --cached and .gitignore (7 min)
- [ ] Write rebuild.sh: sync the lock, run, compare with the expected checksum (9 min)
- [ ] Write the README's Reproduce section (6 min)
- [ ] Clone to a clean folder, follow the README only, and check the lab (9 min)
- [ ] ✱ Stretch: Make rebuild.sh print the versions it ran with, for the reproduction log

### Session 2: Images, containers and volumes

#### [day3#s2] Images, containers and volumes

*Session 2*

- Tell an image from a container and a layer from a mount
- Write a short container definition that installs from the lock
- Run a container without administrator rights with data mounted read-only

#### [day3#image-container] An image is a packed file system; a container is one run of it

*Two words*

- **Image.** Built once from a definition: a base system, your packages, your code, in layers. Read-only.
- **Container.** A process started from an image, with a thin writable layer that disappears with `--rm`.
- **Volume or bind mount.** A folder from outside, mounted in: where data comes in and results go out.

> **It is still a process.** Docker's own explanation: "every container on a machine shares that machine's kernel".

#### [day3#containerfile] Six instructions describe the whole image

*A short definition*

```dockerfile
# file: Containerfile (a field-visit planner)
FROM docker.io/library/python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt
COPY planner.py .
ENTRYPOINT ["python", "planner.py", "--data", "/data"]
```

- `requirements.txt` is exported from the lock, with hashes: `uv export --frozen --format requirements.txt`
- Packages before code: a code change reuses the cached package layer

#### [day3#layers] Each instruction is a layer, rebuilt only when it or one above it changes

*Layers and the cache*

1. **FROM** the base image, pulled once
2. **COPY requirements.txt, RUN pip install** changes when the lock changes
3. **COPY planner.py** changes with every code edit

#### [day3#mounts] Mount the input read-only and the output writable

*Data in, results out*

```bash
# file: terminal
podman run --rm \
  -v "$PWD/visits:/data:ro" \
  -v "$PWD/output:/out" \
  visit-planner
```

- The image never holds the data, so one image serves every month
- `:ro` means a bug cannot change the raw logs (Docker: "prevent the container from writing to the mount")
- Results appear on your disk because `/out` is your folder

#### [day3#rootless] A rootless engine runs containers as you, inside a range of user ids lent to you

*No administrator rights*

- **Podman** is rootless by design; it needs a range of user ids for you in `/etc/subuid` and `/etc/subgid`
- **Docker rootless mode** runs the daemon and containers as a non-root user
- "root" inside the container is your own user outside, not the machine's root
- `podman run --userns=keep-id` maps your user id to the same id inside

- **On the provided workspace.** The trainer has set up the user id ranges and pulled the base image. On a laptop without administrator rights, this is the place to do lab 3.2.

#### [day3#check-mount] Why does the report appear on your disk?

*Checkpoint*

**Question:** You run the planner image with `-v "$PWD/output:/out"` and `--rm`. The container is gone afterwards, yet `output/plan.csv` is on your disk. Why?

- A. --rm copies the container's files out before deleting it
- B. The file was written into the image
- C. /out inside the container is your own output/ folder, mounted
- D. The engine syncs every container folder back to the host

#### [day3#lab-3-2] Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace

Lab 3.2 · 35 min

Complete a container definition that installs from the lock, build it rootless, run it on read-only logs

[D3_2_container.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_2_container.html)

- [ ] Check the engine runs without administrator rights (4 min)
- [ ] Export the lock as hashed requirements (5 min)
- [ ] Fill the five numbered gaps of the Containerfile (10 min)
- [ ] Build the image (6 min)
- [ ] Run it with the logs mounted read-only and the output mounted; compare and check (10 min)
- [ ] ✱ Stretch: Change report.py, rebuild, and see which layers are rebuilt

### Session 3: What a container shares

#### [day3#s3] What a container shares

*Session 3*

- Name what a container shares with its host
- Read a key from the environment and stop clearly when it is missing
- Keep the key out of the output and the repository, with an example file in its place

#### [day3#not-isolated] A container isolates a process, not everything around it

*What a container shares*

| Shared with the host | What it means |
| --- | --- |
| The kernel | A kernel flaw reaches every container; it is not a virtual machine |
| Every mounted folder | The container can read, and without `:ro` change, what you mount |
| Every variable you pass | `--env-file .env` hands the key to whatever runs in the image |
| The network, by default | The program can reach what your machine can reach |
| The image's contents | Anyone with the image can read a key that was copied into it |

#### [day3#key-in-code] A key in the code travels with every copy of the code

*The key in the code*

- **Where it goes.**
  - Every clone and every fork
  - Every backup and every image built from it
  - A screenshot of the editor in a chat
  - An assistant you pasted the file into
- **Where it belongs.**
  - The environment of the process that needs it
  - A `.env` file that git ignores, on one machine
  - The host's or the workplace's secret store

#### [day3#read-from-env] Read the key from a variable, stop clearly without it, and never print it whole

*Reading it from the environment*

```python
# file: planner.py
def booking_key() -> str:
    key = os.environ.get("VISITS_BOOKING_KEY", "")
    if not key:
        print("error: set VISITS_BOOKING_KEY (see .env.example)", file=sys.stderr)
        raise SystemExit(2)
    return key

key = booking_key()
print(f"booking with the key ending ...{key[-4:]}")
```

#### [day3#env-example] .env holds the value and stays home; .env.example holds the name and is committed

*Two files*

```
# file: .env.example (committed)
VISITS_BOOKING_KEY=
```

```
# file: .gitignore (committed)
.env
.env.*
!.env.example
```

```bash
# file: terminal
git check-ignore -v .env                   # proves the rule matches
uv run --env-file .env python planner.py   # loads .env for this run only
```

#### [day3#check-env-file] What does --env-file still expose?

*Checkpoint*

**Question:** You run a planner image with `--env-file .env`; the key is no longer in the code or the image. Who can still read the key?

- A. Any program running in that container, and anyone who can inspect it
- B. Nobody: variables passed at run time are encrypted
- C. Anyone who pulls the image from the registry
- D. Nobody, because /data is mounted read-only

#### [day3#lab-3-3] The key out of the code

Lab 3.3 · 35 min

Addition: move the portal key from the code to the environment, with .env.example committed and the key masked

[D3_3_key_out_of_code.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_3_key_out_of_code.html)

- [ ] Find the key in the code and in the output of a run (5 min)
- [ ] Read it from AIR_PORTAL_KEY; stop with exit 2 when it is missing (10 min)
- [ ] Write .env.example, keep .env ignored, run with uv run --env-file (8 min)
- [ ] Print only the key's last four characters (5 min)
- [ ] Commit, find the key still in history with git log -S, and check the lab (7 min)
- [ ] ✱ Stretch: Run the container with --env-file .env and list what it can see

### Session 4: Scanning, and after a leak

#### [day3#s4] Scanning, and after a leak

*Session 4*

- Run a secret scan over files, staged changes and the whole history
- Carry out the leak response in order: rotate, clean, report
- Install a commit hook that refuses a commit holding a key

#### [day3#three-scans] Scan three places: the files, the next commit, and the whole history

*Scanning*

- **Files.** What is in the folder now. Clean files can still have a dirty history.
- **The next commit.** A hook runs the scan on staged changes and refuses the commit.
- **The history.** Every commit on every branch: what anyone who clones can read.

Tools: gitleaks (`gitleaks git` scans a repository's history), run from pre-commit; hosts add their own: GitHub push protection "blocks pushes that contain secrets", GitLab has secret push protection.

#### [day3#custom-rule] Default rules know public key formats; your own keys need your own rule

*Rules*

```toml
# file: .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "booking-service-key"
description = "Key of the visit booking service"
regex = '''vbk_[a-z]+_[0-9a-f]{24}'''
keywords = ["vbk_"]
```

#### [day3#hook] A pre-commit hook stops the key before it enters history

*Before each commit*

```yaml
# file: .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: secret-scan
        name: secret scan
        entry: uv run --no-project python tools/scan_secrets.py --staged
        language: system
        pass_filenames: false
```

- `uvx pre-commit install` once per clone; every `git commit` then runs the scan
- A hook lives in your clone only: the host's push protection is the second net

#### [day3#leak-order] Rotate first, then clean the history, then report

*After a leak*

1. **1 · Rotate** revoke the key where it was issued; issue a new one
2. **2 · Clean** rewrite every commit that holds it; force-push
3. **3 · Tell** the key's owner and the data protection officer; check the access log
4. **4 · Prevent** the hook, the rule, push protection

> **Why rotation comes first.** GitHub's guidance: "as a first step you need to revoke and/or rotate that secret". Cleaning cannot reach the copies already made.

#### [day3#filter-repo] git filter-repo replaces the value in every commit, and every id after it changes

*Cleaning the history*

```bash
# file: terminal (a field-visit planner)
printf '%s==>REMOVED\n' "$OLD_KEY" > ../replacements.txt    # outside the repository
uvx git-filter-repo --replace-text ../replacements.txt --force
git remote add origin <the hub>          # filter-repo removes it on purpose
git push --force origin main
```

- "Rewriting history will change the hashes of the commits" (GitHub): every teammate clones again
- The scan of the whole history must come back clean, on your clone and on the hub

#### [day3#check-leak] What do you do first?

*Checkpoint*

**Question:** A scan of the planner's history finds a booking-service key in a commit from three weeks ago. The repository has been public since. What is the first action?

- A. Rewrite the history with git filter-repo
- B. Delete the file in a new commit
- C. Make the repository private
- D. Revoke the key at the booking service and issue a new one

#### [day3#lab-3-4] Remediate a seeded leaked key with a scanner and a commit hook

Lab 3.4 · 35 min

A key leaked in an old commit: scan, rotate, write the note, clean the history, and add a hook that blocks the next one

[D3_4_leaked_key.html](https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_4_leaked_key.html)

- [ ] Scan the whole history and find the key (5 min)
- [ ] Rotate first: revoke the old key and issue a new one into .env (7 min)
- [ ] Write ROTATION.md (6 min)
- [ ] Clean the history with git filter-repo, force-push, scan again (10 min)
- [ ] Install the hook, see it block a key, and check the lab (7 min)
- [ ] ✱ Stretch: Run gitleaks with .gitleaks.toml, or the host's push protection, and compare

#### [day3#capstone-kickoff] Tomorrow a peer rebuilds your project from its README alone

*Capstone kickoff*

- Your own small project, on synthetic or public data
- A README with a Reproduce section, a lock file, a container definition, a clean scan of the history
- Your peer follows only the README, on a clean workspace, and logs every step
- Then you fix every step they could not follow; they reproduce it again

- **Tonight, 60 minutes.** Run your own rebuild in a fresh clone, then read your README as a stranger would. The brief and the checklist: `labs/capstone/`.

#### [day3#wrap-up] Three things to keep

*Day 3 · wrap-up*

- **One command.** A reader rebuilds and checks the result with one documented command; data and outputs live elsewhere.
- **A container is a process.** It shares the kernel, the mounts and the variables you give it.
- **Rotate, clean, tell.** A leaked key is revoked first; then history, then the people who need to know.

#### [day3#next] The capstone day: peer reproduction

*Next*

Bring your repository link and its README. The supervised check on shell commands and commit graphs opens the day, AI off.
