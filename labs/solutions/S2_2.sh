#!/usr/bin/env bash
# Lab 2.2, branch, review and resolve a conflict in teams of three (one person playing all roles).
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 2.2 --discard
A="$WS/2.2/participant-a"; B="$WS/2.2/participant-b"; C="$WS/2.2/participant-c"
say "main is protected"
cd "$A"
echo "5. test" >> rules.md
git commit -q -am "Try to push to main"
out=$(git push origin main 2>&1 || true); echo "$out" | grep refused
git reset -q --hard origin/main
say "author A: a branch and a pull request"
git switch -q -c rules/comment-lines
echo "4. Lines that start with # are left out." >> rules.md
git commit -q -am "Add the rule on comment lines"
git push -q -u origin rules/comment-lines
cd "$WS" && lab pr open rules/comment-lines "Add the rule on comment lines" --as participant-a
say "author B: a branch and a pull request"
cd "$B"
git switch -q -c rules/first-day
echo "4. A station's first day of readings is left out." >> rules.md
git commit -q -am "Add the rule on a station's first day"
git push -q -u origin rules/first-day
cd "$WS" && lab pr open rules/first-day "Add the rule on a station's first day" --as participant-b
say "reviewer C: one comment each, with a line and a reason"
lab pr comment 1 "rules.md line 4: say why: a restart note is not a reading, and counting it adds an hour" --as participant-c
lab pr comment 2 "rules.md line 4: say why: the first day mixes installation tests with readings" --as participant-c
lab pr list
say "authors address the comments with a new commit, then resolve them"
cd "$A"
sed -i 's/^4\. Lines that start with # are left out\.$/4. Lines that start with # are left out: a restart note is not a reading./' rules.md
git commit -q -am "Say why comment lines are left out"
git push -q
cd "$WS" && lab pr resolve 1 1 --as participant-a
cd "$B"
sed -i "s/^4\. A station's first day of readings is left out\.$/4. A station's first day of readings is left out: it mixes installation tests with readings./" rules.md
git commit -q -am "Say why the first day is left out"
git push -q
cd "$WS" && lab pr resolve 2 1 --as participant-b
say "reviewer approves and merges the first; the second no longer merges"
lab pr approve 1 --as participant-c
lab pr merge 1 --as participant-c
lab pr approve 2 --as participant-c
if lab pr merge 2 --as participant-c; then echo "expected a conflict"; exit 1; fi
say "author B merges main into the branch and resolves"
cd "$B"
git fetch -q origin
if git merge --no-edit origin/main; then echo "expected a conflict"; exit 1; fi
git diff | head -n 20
cat > rules.md <<'MD'
# Rules of the monthly client report

1. A reading hour counts once, even when the logger sends it twice.
2. An alert hour is an hour with PM10 above 150 (the company's own rule).
3. Error hours are listed, never filled in.
4. Lines that start with # are left out: a restart note is not a reading.
5. A station's first day of readings is left out: it mixes installation tests with readings.
MD
git add rules.md
git commit -q --no-edit
git push -q
say "the reviewer reads the new commits, approves again and merges"
cd "$WS"
lab pr show 2 | head -n 6
lab pr approve 2 --as participant-c
lab pr merge 2 --as participant-c
cd "$C" && git pull -q && git log --oneline --graph | head -n 12
cd "$WS" && lab check 2.2
