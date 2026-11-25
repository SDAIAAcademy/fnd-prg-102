"""Monthly client report of the air-quality monitoring company (synthetic case).

Written on the analyst's laptop. It runs there.
"""
import csv
from pathlib import Path

from dateutil import parser as dateparser
from tabulate import tabulate

DATA = Path("/mnt/team-share/air-reports/logs/2026-10")  # academy:example (a path that exists on one computer only)
THRESHOLD = 150


def read_station(path):
    hours = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(" ")
        when = dateparser.isoparse(fields[0]).isoformat()
        hours.setdefault(when, fields)
    return hours


def station_row(station, client, hours):
    values = [int(f[2].split("=")[1]) for f in hours.values() if not f[5].startswith("ERR")]
    errors = sum(1 for f in hours.values() if f[5].startswith("ERR"))
    mean = sum(values) / len(values)
    alerts = sum(1 for v in values if v > THRESHOLD)
    return [station, client, len(values), f"{mean:.1f}", max(values), alerts, errors]


with (DATA / "stations.csv").open(encoding="utf-8", newline="") as f:
    stations = {r["station"]: r["client"] for r in csv.DictReader(f)}
rows = [station_row(st, cl, read_station(DATA / f"{st}.log")) for st, cl in sorted(stations.items())]
header = ["station", "client", "valid_hours", "mean_pm10", "max_pm10", "alert_hours", "error_hours"]
with open("output/report.csv", "w", encoding="utf-8", newline="\n") as f:
    f.write(",".join(header) + "\n")
    for r in rows:
        f.write(",".join(str(x) for x in r) + "\n")
print(tabulate(rows, headers=header))
