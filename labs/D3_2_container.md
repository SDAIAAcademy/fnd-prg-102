---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "3.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_2_container.html"
---

# Lab 3.2 · Containerise the project with a mounted data folder, on a laptop or a provided Linux workspace

Complete a container definition that installs from the lock, build it rootless, run it on read-only logs

Day 3 · Session 2: Images, containers and volumes

### Goal

Run the report project in a container that installs exactly the locked packages, runs as a user that is not root, and reads the month's logs from a folder mounted read-only, with an engine that needs no administrator rights.

## What you need

- A container engine in rootless mode: Podman, or Docker in rootless mode, on your laptop or on the provided Linux workspace
- The base image `docker.io/library/python:3.13-alpine`, about 17 MB compressed for amd64 on Docker Hub (its tags page, November 2026): the trainer pulls it on the provided workspace before the session
- The lab workspace; this lab starts with `uv run lab.py start 3.2`: `air-report/` with a `Containerfile` to complete, and `data/` beside it
- AI policy: **off** for the first attempt

### Check the engine runs without administrator rights 4 min

```bash
# file: terminal
podman info | grep -i rootless          # rootless: true
docker info 2>/dev/null | grep -i rootless   # with Docker: "rootless" under Security Options
```

### Export the lock as hashed requirements 5 min

```bash
# file: terminal
uv run lab.py start 3.2
cd 3.2/air-report
uv export --frozen --format requirements.txt -o requirements.txt
grep -c -- '--hash=sha256:' requirements.txt
```

The image installs with plain `pip` from this file; `--require-hashes` makes pip refuse any package whose hash is not the locked one.

### Fill the five numbered gaps of the Containerfile 10 min

Open `Containerfile`. Fill the numbered gaps: the base image, copying and installing `requirements.txt` before the code, a `USER` that is not root, and an `ENTRYPOINT` that runs the report on `/data` into `/out`.

### Build the image 6 min

```bash
# file: terminal
git add requirements.txt Containerfile
git commit -m "Complete the container definition"
podman build -t air-report .
```

### Run it with mounted folders, compare and check 10 min

```bash
# file: terminal
mkdir -p output
podman run --rm --userns=keep-id \
  -v "$PWD/../data:/data:ro" -v "$PWD/output:/out" air-report
sha256sum output/report.csv
cd ../.. && uv run lab.py check 3.2
```

With Docker in rootless mode, use the same command without `--userns=keep-id`. On Git Bash for Windows, put `MSYS_NO_PATHCONV=1` before the command so the paths after `:` are not rewritten. If the container cannot write to `output/`, the user inside and the owner outside differ: keep that for session 3.

**No engine at all** (neither on your laptop nor on the provided workspace): complete and commit the definition and `requirements.txt` anyway. `uv run lab.py check 3.2` then checks the definition and says plainly that the run was not done; the trainer records the lab as checked without a run. This lab's build and run have not yet been executed on any machine (see the trainer's note below).

### ✱ Stretch

Change one line of `report.py`, build again and read which steps the engine reuses from its cache. Why does `requirements.txt` come before the code?

## Check yourself

1. What is the difference between the image and the container?
2. Why is the data mounted rather than copied into the image?
3. What does `:ro` prevent, and what would happen without it if the program had a bug?
