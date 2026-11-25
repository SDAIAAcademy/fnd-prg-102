#!/usr/bin/env bash
# The six counts of lab 1.2, working, but tied to one folder named logs/.
# Lab 1.3: take the folder as an argument, fall back to AIR_LOGS, and fail clearly.

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

echo "== Q6 stations per client (stations.csv)"
tail -n +2 logs/stations.csv | cut -d, -f2 | sort | uniq -c
