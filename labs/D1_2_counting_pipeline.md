---
course: "Command Line, Git and Reproducible Environments"
code: "FND-PRG-102"
version: "2027.1.0"
lab: "1.2"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/fnd-prg-102/labs/D1_2_counting_pipeline.html"
---

# Lab 1.2 · A counting pipeline over synthetic logs

Six counts over twelve stations' October logs, one pipeline each, kept in counts.sh

Day 1 · Session 2: Pipes, redirection and filters

### Goal

Answer six questions about one month of sensor logs from twelve stations, each with one pipeline of small commands, and keep the pipelines in a script that writes its answers to a file.

## What you need

- The lab workspace; this lab starts with `uv run lab.py start 1.2`: twelve October logs and `stations.csv` in `logs/`, and `counts.sh` with the six questions
- AI policy: **off** for the first attempt at every pipeline. After that, the hint-only assistant (`AGENTS.md` in the workspace) for the stretch only

### Look at the logs 4 min

```bash
# file: terminal
uv run lab.py start 1.2
cd 1.2
head -n 3 logs/ST01.log
tail -n 2 logs/ST03.log
wc -l logs/*.log | tail -n 1
head -n 3 logs/stations.csv
```

Each reading line has six fields separated by single spaces: the hour, the station, PM10, PM2.5, temperature and a status (`OK`, `WARN`, or `ERR-` and a code). Some lines are not readings.

### Count the reading lines (Q1) 5 min

Leave out the comment lines (they start with `#`) and the blank lines. Write the pipeline under the Q1 line of `counts.sh`, then run `bash counts.sh`.

### Lines per status, and the hidden character (Q2) 8 min

Cut out the sixth field, keep only the part before the hyphen, then `sort | uniq -c`. Pipe the result into `cat -A` (`cat -e` on macOS) to see every character. If a status appears twice, one of the logs ends its lines differently: find which with `file logs/*.log`, and remove the extra character with `tr`.

### Errors by station and by code (Q3, Q4) 8 min

Q3: the three stations with the most `ERR` lines, most first. Q4: each error code with its count (`grep -o` prints only the part that matched).

### Repeated lines and the CSV (Q5, Q6) 6 min

Q5: a logger that restarts sends its last hours again. Count the reading lines whose station and hour already appeared (`uniq -d` prints each repeated line once). Q6: stations per client from `logs/stations.csv`; skip the header line with `tail -n +2`.

### Save the answers and check 4 min

```bash
# file: terminal
bash counts.sh > counts.txt
cat counts.txt
cd .. && uv run lab.py check 1.2
```

### ✱ Stretch

Count the alert hours (PM10 above 150, the company's own rule) per station with `awk`, counting each station and hour once.

## Check yourself

1. Why must `sort` come before `uniq -c`?
2. Your Q2 output is right on your laptop and wrong on a colleague's Linux machine. What is the likely reason?
3. What is the difference between `>` and `>>` when you run `counts.sh` twice?
