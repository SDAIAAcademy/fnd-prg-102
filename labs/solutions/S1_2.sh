#!/usr/bin/env bash
# Lab 1.2, a counting pipeline over synthetic logs.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 1.2 --discard
cd "$WS/1.2"
say "look first"
head -n 3 logs/ST01.log
wc -l logs/*.log | tail -n 1
say "the trap: one status counted twice before tr -d '\r'"
# grep -U: Git Bash's grep then keeps the carriage return, as grep on Linux always does
cat logs/*.log | grep -U -v '^#' | grep -U . | cut -d' ' -f6 | cut -d- -f1 | sort | uniq -c | cat -A
cat > counts.sh <<'SH'
#!/usr/bin/env bash
# Six counts over the October logs in logs/. One pipeline per question, under its echo line.

echo "== Q1 reading lines (no comment lines, no blank lines)"
cat logs/*.log | grep -v '^#' | grep -c .

echo "== Q2 reading lines per status: OK, WARN, ERR"
cat logs/*.log | grep -v '^#' | grep . | tr -d '\r' | cut -d' ' -f6 | cut -d- -f1 | sort | uniq -c

echo "== Q3 the three stations with the most ERR lines"
grep -h 'ERR-' logs/*.log | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 3

echo "== Q4 each error code and its count"
grep -ho 'ERR-E[0-9]*' logs/*.log | sort | uniq -c

echo "== Q5 duplicate reading lines (the same station and hour twice)"
cat logs/*.log | grep -v '^#' | grep . | awk '{print $1, $2}' | sort | uniq -d | wc -l

echo "== Q6 stations per client (logs/stations.csv)"
tail -n +2 logs/stations.csv | cut -d, -f2 | sort | uniq -c
SH
bash counts.sh > counts.txt
cat counts.txt
say "stretch: alert hours (PM10 above 150) per station"
cat logs/*.log | grep -v '^#' | grep . | tr -d '\r' | awk '!seen[$1 $2]++' | awk '{split($3, v, "="); if (v[2] != "NA" && v[2] + 0 > 150) n[$2]++} END {for (s in n) print n[s], s}' | sort -k2 | head -n 12
cd "$WS" && lab check 1.2
