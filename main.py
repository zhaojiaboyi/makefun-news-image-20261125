# Entry point for the 25 November 2026 news-image bounty.
# The grader runs this file with Python 3.13 and expects entry.png
# to appear in the output folder. The picture itself is committed
# next to this script, so all we do here is copy it across.
# Local test:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

base = Path(__file__).resolve().parent
picture = base / "entry.png"
target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

target_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(picture, target_dir / "entry.png")
