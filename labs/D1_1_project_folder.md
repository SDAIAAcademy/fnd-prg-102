---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "1.1"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_1_project_folder.html"
---

# Lab 1.1 · Find your way round the project folder

Addition: map the report folder, read permission strings, and fix a script that ran on one computer only

Day 1 · Session 1: Paths and permissions

### Goal

Find your way round the report folder of the air-quality monitoring company without a file browser, read who may do what to each file, and make a script that only worked on the analyst's laptop run from any folder.

## What you need

- A terminal with Bash: Git Bash on Windows, the terminal on macOS or Linux, or the provided Linux workspace
- The lab workspace (`labs/README.md`, "Set up once"); this lab starts with `uv run lab.py start 1.1`
- AI policy: **off** for this lab. Use `man`, `--help` and the slides

### Start the lab and see where you are 4 min

```bash
# file: terminal
uv run lab.py start 1.1
cd 1.1/air-reports
pwd
ls -a
```

`pwd` prints the absolute path of the folder you are in. Every relative path you type starts from there.

### Map the logs with find, ls -S and du 8 min

```bash
# file: terminal
find logs -name '*.log' | head
find logs/2026-11 -name '*.log' | wc -l
ls -S logs/2026-10/*.log | head -n 3
du -h logs/2026-10 logs/2026-11
```

Write the answers to questions 1 and 2 of `answers.md`. Look at the sizes: why might one station's log be larger than the others when it has the same number of lines?

### Read the permission strings of listing.txt 8 min

```bash
# file: terminal
cat listing.txt
```

The listing comes from a Linux workspace. Read each string as four parts: the type (`d` or `-`), then three letters each for the owner, the group and everyone else. Answer questions 3 to 5 of `answers.md`.

### Fix run_counts.sh 10 min

```bash
# file: terminal
cat run_counts.sh
bash run_counts.sh          # read the first error, then the second
```

Two faults. The script changes into a folder that exists on one computer only: make it change into the `logs/2026-10` folder beside the script, wherever the script is (`"$(dirname "$0")"` is the script's own folder). The last line names a folder with a space in it: quote the path.

### Run it from the workspace folder and check 5 min

```bash
# file: terminal
cd ../..
bash 1.1/air-reports/run_counts.sh
uv run lab.py check 1.1
```

### ✱ Stretch

On a Linux workspace, make `run_counts.sh` executable with `chmod u+x`, run it as `./run_counts.sh` from its folder, and explain why `bash run_counts.sh` never needed that.

## Check yourself

1. You move the whole `air-reports` folder to another disk. Which lines of the original script break, and which of your fixed script?
2. What does the shell do with `field notes/visit-checklist.txt` when it is not quoted?
3. Who can read `portal.env` in the listing, and why does that matter for a key?
