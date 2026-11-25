#!/usr/bin/env bash
# Count the October reading lines, then show the start of the visit checklist.
# Written on the analyst's laptop: it only works there. Make it work from any folder.
cd /mnt/team-share/air-reports/logs/2026-10      # academy:example (a folder on one computer only)
cat *.log | grep -v '^#' | grep -c .
head -n 3 ../../field notes/visit-checklist.txt
