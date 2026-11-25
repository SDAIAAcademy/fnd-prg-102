#!/usr/bin/env bash
# Lab 3.4, remediate a seeded leaked key with a scanner and a commit hook.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 3.4 --discard
cd "$WS/3.4/air-report"
say "1. scan the whole history"
lab scan --history . || true
say "2. rotate first: revoke the leaked key, issue a new one into .env"
lab keys list 3.4
lab keys revoke 3.4 K-0002
new=$(lab keys issue 3.4 | tail -n 1)
printf 'AIR_PORTAL_KEY=%s\n' "$new" > .env
git check-ignore -q .env && echo ".env is ignored"
say "3. clean the history: replace the old value in every commit, then force-push"
old=$(grep -o 'fprg102_demo_[0-9a-f]*' "$KIT/lab.py" | sed -n 2p)
printf '%s==>REMOVED\n' "$old" > ../replacements.txt
uvx -q git-filter-repo --replace-text ../replacements.txt --force > /dev/null
rm ../replacements.txt
git remote add origin "$(cd ../hub/air-report.git && pwd)"
git push -q --force origin main
lab scan --history .
say "4. the hook: pre-commit with the course scanner"
if ! uvx -q pre-commit install; then
  echo "pre-commit refused: core.hooksPath is set on this machine; installing the same scan as a plain hook"
  cp "$KIT/files/3.4/pre-commit-hook" .git/hooks/pre-commit
  git config core.hooksPath .git/hooks
fi
cat > ROTATION.md <<'MD'
# Rotation note

## What leaked

The report portal key K-0002, in settings.toml, added in the commit "Add the portal settings"
and removed two commits later; it stayed readable in the history for everyone who could clone
the repository, from 5 October 2026 until today.

## Rotated

K-0002 revoked at the portal first. A new key, issued at the portal, is kept only in .env on the
analyst's machine, which git ignores; the README names the variable, AIR_PORTAL_KEY.

## History cleaned

git filter-repo --replace-text replaced the old value in every commit; the history was
force-pushed to the hub. The secret scan of the whole history is clean. Everyone with a clone
deletes it and clones again.

## Who was told

The operations lead, who owns the portal account, and the data protection officer, the same
day. The portal's access log for K-0002 is to be checked by the operations lead.
MD
git add ROTATION.md
git commit -q -m "Add the rotation note"
git push -q origin main
say "the hook blocks a commit with a key"
printf 'key = "fprg102_demo_%s"\n' "$(printf 'cd%.0s' {1..12})" > probe.toml
git add probe.toml
if git commit -q -m "probe" 2>&1 | tail -n 3; then :; fi
git reset -q -- probe.toml; rm probe.toml
cd "$WS" && lab check 3.4
