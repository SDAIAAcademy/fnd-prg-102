#!/usr/bin/env bash
# Rebuild the environment from the lock file, run the report, and check the result.
#   AIR_LOGS=<folder of the October logs> bash rebuild.sh
set -euo pipefail
cd "$(dirname "$0")"
: "${AIR_LOGS:?set AIR_LOGS to the folder of logs and stations.csv}"
uv sync --locked --quiet
uv run --quiet python report.py --data "$AIR_LOGS" --out output
sha256sum -c expected/october.sha256
