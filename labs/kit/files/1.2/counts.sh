#!/usr/bin/env bash
# Six counts over the October logs in logs/. One pipeline per question, under its echo line.
# Keep the echo lines: the lab check reads them. Run: bash counts.sh > counts.txt

echo "== Q1 reading lines (no comment lines, no blank lines)"

echo "== Q2 reading lines per status: OK, WARN, ERR"

echo "== Q3 the three stations with the most ERR lines"

echo "== Q4 each error code and its count"

echo "== Q5 duplicate reading lines (the same station and hour twice)"

echo "== Q6 stations per client (logs/stations.csv)"
