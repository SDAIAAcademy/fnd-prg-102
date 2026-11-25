# Monthly client report

The monthly client report of the air-quality monitoring company (a synthetic case). It reads one
month of hourly sensor logs and writes one row per station to `output/report.csv`.

## Rebuild and run

With uv installed, from this folder:

    uv sync --locked
    uv run python report.py --data <the folder of logs and stations.csv>

`uv.lock` pins every package; `--locked` refuses to run when it is out of date.
