"""Run one focused stage synchronously, preserving its command and output."""

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path.cwd()
EVIDENCE = ROOT / ".novc/split"
STAGES = {
    "generate": ["py/main_authored.py", "gen-mam-for-sefaria-doc"],
    "maintained": [
        "py/main_test.py",
        "py/tests/test_sefaria_silluq_documentation.py",
        "py/tests/test_shared_html_styles.py",
        "py/tests/test_mega_coverage.py",
        "py/tests/test_product_scopes.py",
        "py/tests/source_hygiene_test.py",
        "py/tests/test_accent_marks_source.py",
        "py/tests/test_prose_mark_order.py",
        "-q",
        "-ra",
    ],
    "independent": ["py/main_test.py", ".novc/split/test_split.py", "-q", "-ra"],
    "listing-followup": [
        "py/main_test.py",
        ".novc/split/test_split.py::test_new_ajf_listing_trailing_space_explanation",
        "-q",
        "-ra",
    ],
}


def main():
    stage = sys.argv[1]
    command = [sys.executable, *STAGES[stage]]
    assert not (
        EVIDENCE / f"{stage}.json"
    ).exists(), "Do not duplicate a completed stage"
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    status = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"]).decode()
    (EVIDENCE / f"{stage}.log").write_text(
        result.stdout + result.stderr, encoding="utf-8"
    )
    record = {
        "command": command,
        "cwd": str(ROOT),
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "seconds": round(time.monotonic() - start, 3),
        "exit_code": result.returncode,
        "tracked_status_after": status,
    }
    (EVIDENCE / f"{stage}.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, indent=2))
    print((result.stdout + result.stderr)[-3500:])
    if status:
        raise SystemExit("Unexpected tracked changes; preserve and investigate")
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
