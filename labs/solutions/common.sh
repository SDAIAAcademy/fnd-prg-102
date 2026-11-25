#!/usr/bin/env bash
# Shared by the solution scripts. WS is the lab workspace (uv run labs/kit/setup.py --to <WS>).
set -euo pipefail
SOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT="$(cd "$SOL/../kit" && pwd)"
: "${WS:?set WS to the lab workspace folder}"
unset VIRTUAL_ENV UV_PROJECT_ENVIRONMENT
lab() { uv run --no-project -q python "$WS/lab.py" "$@"; }
say() { printf '\n## %s\n' "$*"; }
