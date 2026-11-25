#!/usr/bin/env bash
# Lab 3.2, containerise the project with a mounted data folder.
source "$(dirname "$0")/common.sh"
cd "$WS" && lab start 3.2 --discard
cd "$WS/3.2/air-report"
say "export the lock as hashed requirements for the image"
uv export --frozen --format requirements.txt -o requirements.txt -q
grep -c -- '--hash=sha256:' requirements.txt
cp "$KIT/files/3.2/Containerfile.solution" Containerfile
grep -v '^#' Containerfile | grep .
git add requirements.txt Containerfile
git commit -q -m "Complete the container definition"
ENGINE=""
for e in podman docker; do
  if command -v "$e" > /dev/null && "$e" info > /dev/null 2>&1; then ENGINE="$e"; break; fi
done
if [ -n "$ENGINE" ]; then
  say "build and run with $ENGINE"
  "$ENGINE" build -q -t air-report .
  mkdir -p output
  MSYS_NO_PATHCONV=1 "$ENGINE" run --rm -v "$(pwd)/../data:/data:ro" -v "$(pwd)/output:/out" air-report | tail -n 1
  sha256sum output/report.csv
else
  say "no container engine answers on this machine: the definition is checked, the run is not"
fi
cd "$WS" && lab check 3.2
