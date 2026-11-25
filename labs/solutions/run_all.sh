#!/usr/bin/env bash
# Run every lab twice: its starting state must NOT pass the check, its solution must.
#   bash labs/solutions/run_all.sh <a new workspace folder>
set -uo pipefail
SOL="$(cd "$(dirname "$0")" && pwd)"
export WS="${1:?give a folder for a fresh workspace}"
uv run -q "$SOL/../kit/setup.py" --to "$WS" > /dev/null || exit 1
fail=0
for s in 1_1 1_2 1_3 1_4 2_1 2_2 2_3 2_4 3_1 3_2 3_3 3_4; do
  id="${s/_/.}"
  (cd "$WS" && uv run --no-project -q python lab.py start "$id" --discard > /dev/null && \
   uv run --no-project -q python lab.py check "$id" > /dev/null 2>&1)
  if [ $? -eq 0 ]; then echo "FAIL $id: the starting state already passes"; fail=1; fi
  if bash "$SOL/S$s.sh" > "$WS/S$s.log" 2>&1 && grep -q "^PASS lab $id" "$WS/S$s.log"; then
    echo "PASS $id"
  else
    echo "FAIL $id (see S$s.log)"; fail=1
  fi
done
exit $fail
