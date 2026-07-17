"""Smoke test for the Scrapy command-line entry point (offline)."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SPIDERS = {
    "bhcc.mass.edu",
    "bu.edu",
    "emerson.edu",
    "extension.harvard.edu",
    "suffolk.edu",
    "umb.edu",
}


def test_scrapy_list_discovers_all_spiders():
    proc = subprocess.run(
        [sys.executable, "-m", "scrapy", "list"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert proc.returncode == 0, proc.stderr
    assert set(proc.stdout.split()) == EXPECTED_SPIDERS
