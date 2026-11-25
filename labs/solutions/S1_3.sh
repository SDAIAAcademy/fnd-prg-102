#!/usr/bin/env bash
# Lab 1.3, the counting script on a second folder, and a practice key.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 1.3 --discard
cd "$WS/1.3"
cat > counts.sh <<'SH'
#!/usr/bin/env bash
# Six counts over one month of logs.
#   bash counts.sh <folder>        or   AIR_LOGS=<folder> bash counts.sh
set -euo pipefail
DIR="${1:-${AIR_LOGS:-}}"
if [ -z "$DIR" ]; then
  echo "usage: bash counts.sh <folder of logs>   (or set AIR_LOGS)" >&2
  exit 2
fi
if [ ! -d "$DIR" ] || ! ls "$DIR"/*.log > /dev/null 2>&1; then
  echo "error: no .log files in $DIR" >&2
  exit 2
fi

echo "== Q1 reading lines (no comment lines, no blank lines)"
cat "$DIR"/*.log | grep -v '^#' | grep -c .

echo "== Q2 reading lines per status: OK, WARN, ERR"
cat "$DIR"/*.log | grep -v '^#' | grep . | tr -d '\r' | cut -d' ' -f6 | cut -d- -f1 | sort | uniq -c

echo "== Q3 the three stations with the most ERR lines"
grep -h 'ERR-' "$DIR"/*.log | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 3

echo "== Q4 each error code and its count"
grep -ho 'ERR-E[0-9]*' "$DIR"/*.log | sort | uniq -c

echo "== Q5 duplicate reading lines (the same station and hour twice)"
cat "$DIR"/*.log | grep -v '^#' | grep . | awk '{print $1, $2}' | sort | uniq -d | wc -l

echo "== Q6 stations per client (stations.csv)"
tail -n +2 "$DIR"/stations.csv | cut -d, -f2 | sort | uniq -c
SH
say "November, unchanged script"
bash counts.sh data/november
say "exit codes"
bash counts.sh data/missing || echo "exit code: $?"
say "a practice key pair, inside the lab folder only"
rm -f keys/practice_key keys/practice_key.pub
ssh-keygen -q -t ed25519 -N "" -C "participant-a practice key" -f keys/practice_key
ssh-keygen -lf keys/practice_key.pub > keys/fingerprint.txt
cut -d' ' -f1,3- keys/fingerprint.txt
cat > ssh_config <<'CFG'
# Use with: ssh -F ssh_config lab-workspace
Host lab-workspace
    HostName 192.0.2.10
    User participant-a
    IdentityFile keys/practice_key
    IdentitiesOnly yes
CFG
cd "$WS" && lab check 1.3
