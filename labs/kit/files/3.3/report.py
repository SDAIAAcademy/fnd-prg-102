"""Monthly client report of the air-quality monitoring company (synthetic case).

Reads the hourly sensor logs of one month and writes one row per station:
valid hours, mean and maximum PM10, alert hours (PM10 above 150, the company's own rule)
and error hours. A reading hour counts once, even when a logger sends it twice.

    uv run python report.py --data <logs folder> --out output
"""
from __future__ import annotations

import argparse
import json
import csv
import os
import shutil
import sys
from pathlib import Path

from dateutil import parser as dateparser
from tabulate import tabulate

PORTAL_KEY = "fprg102_demo_7f3ab9e1c4d2a8f05b6e9d1c"

THRESHOLD = 150


def read_station(path: Path) -> dict[str, list[str]]:
    """Unique reading hours of one log: comments, blank lines and repeats left out."""
    hours: dict[str, list[str]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(" ")
        when = dateparser.isoparse(fields[0]).isoformat()
        hours.setdefault(when, fields)
    return hours


def station_row(station: str, client: str, hours: dict[str, list[str]]) -> list[object]:
    values = [int(f[2].split("=")[1]) for f in hours.values() if not f[5].startswith("ERR")]
    errors = sum(1 for f in hours.values() if f[5].startswith("ERR"))
    mean = sum(values) / len(values)
    alerts = sum(1 for v in values if v > THRESHOLD)
    return [station, client, len(values), f"{mean:.1f}", max(values), alerts, errors]


def upload(report: Path) -> None:
    """Send the report to the client portal."""
    # Stand-in for the portal: a local folder ($AIR_PORTAL_DIR) with keys.json and an inbox.
    portal = Path(os.environ.get("AIR_PORTAL_DIR", "portal"))
    keys = json.loads((portal / "keys.json").read_text(encoding="utf-8"))
    print(f"uploading {report} with key {PORTAL_KEY}")
    if keys.get(PORTAL_KEY, {}).get("state") != "active":
        raise SystemExit("error: the portal rejected the key")
    (portal / "inbox").mkdir(exist_ok=True)
    shutil.copyfile(report, portal / "inbox" / "report.csv")
    print("uploaded")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=os.environ.get("AIR_LOGS"), help="folder of STxx.log files and stations.csv (default: $AIR_LOGS)")
    ap.add_argument("--out", default="output", help="folder for report.csv (default: output)")
    ap.add_argument("--upload", action="store_true", help="send the report to the client portal")
    args = ap.parse_args()
    if not args.data:
        print("error: give --data <folder> or set AIR_LOGS", file=sys.stderr)
        return 2
    data, out = Path(args.data), Path(args.out)
    if not (data / "stations.csv").is_file():
        print(f"error: no stations.csv in {data}", file=sys.stderr)
        return 2
    with (data / "stations.csv").open(encoding="utf-8", newline="") as f:
        stations = {r["station"]: r["client"] for r in csv.DictReader(f)}
    rows = [station_row(st, cl, read_station(data / f"{st}.log")) for st, cl in sorted(stations.items())]
    out.mkdir(parents=True, exist_ok=True)
    header = ["station", "client", "valid_hours", "mean_pm10", "max_pm10", "alert_hours", "error_hours"]
    with (out / "report.csv").open("w", encoding="utf-8", newline="\n") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    print(tabulate(rows, headers=header))
    print(f"wrote {out / 'report.csv'} ({len(rows)} stations)")
    if args.upload:
        upload(out / "report.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
