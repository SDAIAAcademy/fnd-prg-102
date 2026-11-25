# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Write the synthetic sensor logs of the air-quality monitoring company, and the answers.

    uv run labs/_tools/make_data.py            # from the course folder

Writes labs/kit/data/ (october/ and november/ with one log per station, stations.csv,
listing.txt) and labs/kit/reference.json (the counts every lab check compares with). Python
standard library only, fixed seed: the same bytes on every run and every system.

Everything is invented: twelve stations coded ST01 to ST12, four clients coded Client A to D, five
generic sectors. The alert threshold (PM10 above 150) is the company's own rule for its client
report, not a national standard.

Planted, and found by a named lab:
- comment lines starting with "#" in ST03 and ST09 (lab 1.2)
- Windows line endings in every ST07 log (lab 1.2: "OK" is counted twice)
- duplicate lines after two logger restarts of ST03 in October, one in November (lab 1.2)
- a blank line in ST04 (lab 1.2)
- a two-day gap in ST11 in October (the report's valid hours)
"""
from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

LABS = Path(__file__).resolve().parents[1]
OUT = LABS / "kit" / "data"
TZ = timezone(timedelta(hours=3))
STATIONS = [f"ST{i:02d}" for i in range(1, 13)]
CLIENTS = ["Client A", "Client A", "Client A", "Client B", "Client B", "Client B",
           "Client C", "Client C", "Client C", "Client D", "Client D", "Client D"]
SECTORS = ["North", "North", "East", "East", "Central", "South", "South", "West", "West", "Central", "North", "East"]
MODELS = ["Model P", "Model P", "Model Q", "Model P", "Model Q", "Model P",
          "Model Q", "Model P", "Model Q", "Model P", "Model Q", "Model P"]
BASE = [52, 61, 48, 75, 66, 58, 83, 55, 70, 45, 62, 68]
ERR_RATE = {"ST02": 0.006, "ST05": 0.035, "ST08": 0.004, "ST09": 0.022, "ST12": 0.012}
ERR_CODES = {"ST02": ["E40"], "ST05": ["E21", "E21", "E21", "E11"], "ST08": ["E40"],
             "ST09": ["E34", "E34", "E21"], "ST12": ["E11", "E40"]}
WARN_RATE = 0.01
THRESHOLD = 150
MONTHS = {
    "october": (datetime(2026, 10, 1, tzinfo=TZ), 31, [(12, 4), (19, 15), (20, 9)],
                {"ST03": [(datetime(2026, 10, 12, 7, tzinfo=TZ), 6), (datetime(2026, 10, 23, 14, tzinfo=TZ), 6)]},
                {"ST11": (datetime(2026, 10, 17, tzinfo=TZ), datetime(2026, 10, 19, tzinfo=TZ))}),
    "november": (datetime(2026, 11, 1, tzinfo=TZ), 30, [(6, 11), (25, 13)],
                 {"ST03": [(datetime(2026, 11, 9, 16, tzinfo=TZ), 6)]}, {}),
}


def stamp(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M") + "+03:00"


def month_logs(name: str, seed: int) -> dict[str, list[str]]:
    start, days, dust, restarts, gaps = MONTHS[name]
    rng = random.Random(seed)
    logs: dict[str, list[str]] = {}
    for i, st in enumerate(STATIONS):
        lines: list[str] = []
        for h in range(days * 24):
            t = start + timedelta(hours=h)
            gap = gaps.get(st)
            if gap and gap[0] <= t < gap[1]:
                continue
            day, hour = t.day, t.hour
            diurnal = 1 + 0.35 * (1 if 10 <= hour <= 17 else -0.2)
            pm10 = BASE[i] * diurnal * rng.uniform(0.75, 1.25)
            for dday, peak in dust:
                if day == dday and abs(hour - peak) <= 4:
                    pm10 += rng.uniform(110, 190) * (1 - abs(hour - peak) / 6)
            pm10 = round(pm10)
            pm25 = round(pm10 * rng.uniform(0.38, 0.52))
            temp = round(24 + 9 * (1 if 9 <= hour <= 18 else 0) + rng.uniform(-2.5, 2.5) - (3 if name == "november" else 0), 1)
            r = rng.random()
            if r < ERR_RATE.get(st, 0.0):
                code = rng.choice(ERR_CODES[st])
                line = f"{stamp(t)} {st} pm10=NA pm25=NA temp=NA ERR-{code}"
            elif r < ERR_RATE.get(st, 0.0) + WARN_RATE:
                line = f"{stamp(t)} {st} pm10={pm10} pm25={pm25} temp={temp} WARN"
            else:
                line = f"{stamp(t)} {st} pm10={pm10} pm25={pm25} temp={temp} OK"
            lines.append(line)
            for when, back in restarts.get(st, []):
                if t == when:
                    lines.append("# logger restart, resending the last 6 hours")
                    lines.extend(lines[-1 - back:-1])
            if st == "ST09" and t.weekday() == 0 and hour == 6:
                lines.append("# weekly calibration check passed")
            if st == "ST04" and day == 15 and hour == 12:
                lines.append("")
        logs[st] = lines
    return logs


def count(logs: dict[str, list[str]]) -> dict:
    readings = [ln for st in STATIONS for ln in logs[st] if ln and not ln.startswith("#")]
    status: dict[str, int] = {}
    errs_by_station: dict[str, int] = {}
    codes: dict[str, int] = {}
    alert: dict[str, int] = {}
    seen: set[tuple[str, str]] = set()
    dups = 0
    for ln in readings:
        f = ln.split(" ")
        st, s = f[1], f[5].split("-")[0]
        if (f[0], st) in seen:
            dups += 1
        seen.add((f[0], st))
        status[s] = status.get(s, 0) + 1
        if s == "ERR":
            errs_by_station[st] = errs_by_station.get(st, 0) + 1
            codes[f[5]] = codes.get(f[5], 0) + 1
    top3 = sorted(errs_by_station.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    return {"reading_lines": len(readings), "status": dict(sorted(status.items())),
            "top3_err_stations": [[k, v] for k, v in top3],
            "error_codes": dict(sorted(codes.items())), "duplicate_lines": dups}


def report_rows(logs: dict[str, list[str]]) -> str:
    """The client report the project writes: one row per station, the rules of the README."""
    out = ["station,client,valid_hours,mean_pm10,max_pm10,alert_hours,error_hours"]
    for i, st in enumerate(STATIONS):
        seen: dict[str, str] = {}
        for ln in logs[st]:
            if ln and not ln.startswith("#"):
                seen.setdefault(ln.split(" ")[0], ln)
        vals, errs = [], 0
        for ln in seen.values():
            f = ln.split(" ")
            if f[5].startswith("ERR"):
                errs += 1
            else:
                vals.append(int(f[2].split("=")[1]))
        mean = sum(vals) / len(vals)
        out.append(f"{st},{CLIENTS[i]},{len(vals)},{mean:.1f},{max(vals)},{sum(v > THRESHOLD for v in vals)},{errs}")
    return "\n".join(out) + "\n"


def main() -> None:
    ref: dict = {"threshold_pm10": THRESHOLD}
    (OUT).mkdir(parents=True, exist_ok=True)
    stations_csv = "station,client,sector,installed,model\n" + "".join(
        f"{st},{CLIENTS[i]},{SECTORS[i]},2025-{(i % 9) + 2:02d}-{(i * 7) % 27 + 1:02d},{MODELS[i]}\n" for i, st in enumerate(STATIONS))
    clients: dict[str, int] = {}
    for c in CLIENTS:
        clients[c] = clients.get(c, 0) + 1
    ref["stations_per_client"] = clients
    for k, (name, seed) in enumerate([("october", 1026), ("november", 1126)]):
        logs = month_logs(name, seed)
        folder = OUT / name
        folder.mkdir(exist_ok=True)
        (folder / "stations.csv").write_bytes(stations_csv.encode())
        for st, lines in logs.items():
            nl = "\r\n" if st == "ST07" else "\n"
            (folder / f"{st}.log").write_bytes((nl.join(lines) + nl).encode())
        c = count(logs)
        c["stations_per_client"] = clients
        rep = report_rows(logs)
        c["report_sha256"] = hashlib.sha256(rep.encode()).hexdigest()
        c["report_first_rows"] = rep.splitlines()[:4]
        ref[name] = c
        (LABS / "kit" / f"expected_report_{name}.csv").write_bytes(rep.encode())
    (OUT / "listing.txt").write_bytes((
        "# A long listing of the report folder on the provided Linux workspace.\n"
        "# Synthetic: written for lab 1.1, in the shape that ls -l prints on Linux.\n"
        "# Owner and group are role accounts, not people.\n"
        "drwxr-x---  2 analyst field  4096 logs\n"
        "-rw-r--r--  1 analyst field   612 stations.csv\n"
        "-rw-------  1 analyst field    58 portal.env\n"
        "-rwxr-xr-x  1 analyst field  1180 run_counts.sh\n"
        "-rw-r--r--  1 analyst field   934 make_report.sh\n"
        "-rw-rw-rw-  1 analyst field   201 notes.txt\n").encode())
    ref["listing"] = {"world_writable": "notes.txt", "not_executable_script": "make_report.sh",
                      "owner_only": "portal.env", "group_can_enter": "logs"}
    (LABS / "kit" / "reference.json").write_bytes((json.dumps(ref, indent=2) + "\n").encode())
    print(json.dumps({m: {k: ref[m][k] for k in ("reading_lines", "status", "top3_err_stations", "error_codes", "duplicate_lines")} for m in ("october", "november")}, indent=1))


if __name__ == "__main__":
    main()
