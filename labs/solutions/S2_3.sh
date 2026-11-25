#!/usr/bin/env bash
# Lab 2.3, undo five mistakes.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 2.3 --discard
cd "$WS/2.3/report-repo"
say "the state: what is staged, what is changed, what is pushed"
git status --short
git log --oneline --graph --all
git log --oneline origin/main
say "1. unstage scratch.txt (then delete it) and discard the stray line"
git restore --staged scratch.txt
rm scratch.txt
git restore client_report.md
say "2. drop the local debug commit (never pushed)"
git reset -q --hard HEAD~1
say "3. fix the last commit: its message and the forgotten file"
git add sectors.md
git commit -q --amend -m "Add sector line"
git show --stat --format=%s HEAD | head -n 4
say "4. undo the pushed threshold change with a new commit, then push"
bad=$(git log --format=%h --grep '^Change the threshold to 100$')
git revert --no-edit "$bad"
grep 'Alert threshold' client_report.md
git push -q origin main
say "5. bring back the deleted branch from the reflog"
git reflog | grep 'Draft the winter notes' | head -n 1
id=$(git log -g --format='%h %s' | grep 'Draft the winter notes' | head -n 1 | cut -d' ' -f1)
git branch draft/winter-notes "$id"
git log --oneline --graph --all
cd "$WS" && lab check 2.3
