#!/usr/bin/env bash
# Lab 1.1, find your way round the project folder.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 1.1 --discard
cd "$WS/1.1/air-reports"
say "where am I, what is here"
pwd | sed 's|.*/1.1/|.../1.1/|'
ls -a
say "November logs, largest October log"
find logs/2026-11 -name '*.log' | wc -l
ls -S logs/2026-10/*.log | head -n 1
du -h logs/2026-10/ST07.log logs/2026-10/ST01.log
say "the permission strings"
grep -v '^#' listing.txt
say "fix the script: its own folder, and quotes round the folder with a space"
# sed writes to a new file and mv replaces the old one: sed -i differs between GNU and macOS
sed -e 's|^cd /mnt/.*|cd "$(dirname "$0")/logs/2026-10"|' \
    -e 's|^head -n 3 ../../field notes/visit-checklist.txt|head -n 3 "../../field notes/visit-checklist.txt"|' \
    run_counts.sh > run_counts.new && mv run_counts.new run_counts.sh   # academy:example (the faulty line)
cat run_counts.sh
cd "$WS" && bash 1.1/air-reports/run_counts.sh
cd "$WS/1.1/air-reports"
largest=$(ls -S logs/2026-10/*.log | head -n 1 | xargs basename | cut -d. -f1)
cat > answers.md <<ANS
# Lab 1.1: answers

1. How many log files are there for November 2026?
   answer: 12

2. Which October log file is the largest? (its station code)
   answer: $largest

3. In listing.txt, which file can every user of the workspace change?
   answer: notes.txt

4. In listing.txt, which script cannot be run as ./name, and which one command fixes that?
   answer: make_report.sh, chmod u+x make_report.sh

5. In listing.txt, which file can only its owner read?
   answer: portal.env
ANS
cd "$WS" && lab check 1.1
