---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "3.3"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D3_3_key_out_of_code.html"
---

# Lab 3.3 · The key out of the code

Addition: move the portal key from the code to the environment, with .env.example committed and the key masked

Day 3 · Session 3: What a container shares

### Goal

The report project now uploads each report to the client portal, with the portal key written into the code and printed in full on every run. Move the key into an environment variable, document its name without its value, stop clearly when it is missing, and print only its last four characters.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 3.3`: `air-report/`, `data/`, and `portal/`, the course's local stand-in for the report portal (its `keys.json` lists the keys it accepts)
- The key in this lab is a practice key of the course (prefix `fprg102_demo_`); it opens nothing but the stand-in
- AI policy: **off** for the first attempt. Never paste a key into an assistant, even a practice one: treat the habit as real

### Find the key in the code and in the output 5 min

```bash
# file: terminal
uv run lab.py start 3.3
cd 3.3/air-report
grep -rn 'fprg102_' --include='*.py' .
export AIR_PORTAL_DIR="$PWD/../portal"
uv run python report.py --data ../data --upload | tail -n 2
```

Where could that printed line end up? (A terminal scrollback, a log file, a screenshot in a chat.)

### Read it from AIR_PORTAL_KEY; stop when it is missing 10 min

In `report.py`, remove the constant. Write a function that reads `AIR_PORTAL_KEY` from the environment and, when it is empty, prints one line to standard error naming the variable and exits with code 2. Call it in `upload()`.

### Example file in, real file out 8 min

```bash
# file: terminal
printf 'AIR_PORTAL_KEY=\n' > .env.example    # the name, never the value
git check-ignore -v .env                    # .env must be ignored
# put the key in .env (copy it from the old line of report.py), then:
uv run --env-file .env python report.py --data ../data --upload
```

### Print only the key's last four characters 5 min

Change the upload message so that it names the key by its end (`...9d1c`), enough to tell which key was used and useless to anyone who reads the log.

### Commit, and find the key still in history; check 7 min

```bash
# file: terminal
git add report.py .env.example
git commit -m "Read the portal key from the environment"
git grep -c 'fprg102_demo_' || echo "no file holds a key"
git log --oneline -S 'fprg102_demo_' --all
cd ../.. && uv run lab.py check 3.3
```

The key is gone from the files and still in the commit that added it. Lab 3.4 is what to do about that.

### ✱ Stretch

With a container engine: run the image of lab 3.2 with `--env-file .env` and list, from inside (`env`, `ls /data`), what the container can see. Which of those would a different image also see if you passed the same options?

## Check yourself

1. Why is `.env.example` committed and `.env` not?
2. Why exit with a non-zero code when the key is missing, instead of skipping the upload?
3. Who can read the key after you pass it to a container with `--env-file`?
