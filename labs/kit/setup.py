# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Write the lab workspace of FND-PRG-102.

    uv run labs/kit/setup.py                 # into air-labs/ beside the course folder
    uv run labs/kit/setup.py --to <folder>   # somewhere else (a short path on Windows)

The workspace holds lab.py (start and check each lab), _kit/ (the data and starting files it
copies) and AGENTS.md (the hint-only instruction for any coding assistant). Your lab folders
(1.1/ to 3.4/) appear there when you start each lab. Running setup again refreshes lab.py and
_kit/ and never touches your lab folders.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
SKIP = {"setup.py", "__pycache__"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--to", default=str(KIT.parents[2] / "air-labs"))
    ws = Path(ap.parse_args().to).resolve()
    ws.mkdir(parents=True, exist_ok=True)
    if (ws / "_kit").exists():
        shutil.rmtree(ws / "_kit")
    shutil.copytree(KIT, ws / "_kit", ignore=lambda d, names: [n for n in names if n in SKIP])
    shutil.copyfile(KIT / "lab.py", ws / "lab.py")
    shutil.copyfile(KIT / "tutor" / "AGENTS.md", ws / "AGENTS.md")
    print(f"workspace ready: {ws}")
    print("next:  cd into it, then  uv run lab.py list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
