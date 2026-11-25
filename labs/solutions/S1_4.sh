#!/usr/bin/env bash
# Lab 1.4, draw the graph, then check it.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 1.4 --discard
cd "$WS/1.4/practice"
say "sequence 1"
echo "threshold: 150" >> settings.txt
git add settings.txt
git commit -q -m "Record the alert threshold"
echo "unit: ug/m3" >> settings.txt
git commit -q -am "Record the unit"
git log --oneline --graph --all --format=%s
say "sequence 2"
echo "stations: 12" > stations.txt
echo "clients: 4" >> settings.txt
git add stations.txt
git status --short
git diff --stat
git diff --staged --stat
git commit -q -m "Count the stations"
git commit -q -am "Count the clients"
git rev-list --count main
say "sequence 3"
git branch review-notes
git switch -q review-notes
echo "reviewer: check the unit line" > review.txt
git add review.txt
git commit -q -m "Add a review note"
git switch -q main
echo "sectors: 5" >> settings.txt
git commit -q -am "Count the sectors"
git log --graph --all --format='%s%d'
cd "$WS/1.4"
sed -i '0,/answer:$/s//answer: 3/; 0,/answer:$/s//answer: 5/; 0,/answer:$/s//answer: 7/; 0,/answer:$/s//answer: main/' graphs.md
cd "$WS" && lab check 1.4
