# Monthly client report

The monthly client report of the air-quality monitoring company (a synthetic case). It reads one
month of hourly sensor logs and writes one row per station to `output/report.csv`.

## Reproduce

You need git, Bash (Git Bash on Windows) and uv. The data is not in this repository: get the
folder of October logs (with its `stations.csv`) from the course workspace. Then, from this
folder, one command:

    AIR_LOGS=<the folder of October logs> bash rebuild.sh

It installs the locked packages, writes `output/report.csv` and prints `output/report.csv: OK`
when the result matches `expected/october.sha256`.
