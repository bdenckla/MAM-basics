"""Ingest Holman's .eml files into the tracked derivative under emails/.

Run from repo root, with the mailbox in the default untracked location:
    .venv\\Scripts\\python.exe py/main_ingest_uxlc_emails.py

Writes, for each message: emails/<key>.txt (the body, with every email address
replaced), emails/<key>.json (subject, sender name, date, attachment list), and
each attached PNG into gh-pages/uxlc_img/.

This is the only step that touches a .eml file. Those are NOT tracked -- their
headers carry the correspondents' addresses and this repo is public -- so they
live in .novc/eml/, which .gitignore already covers. Everything tracked is
address-free, and the report regenerates from it without the mailbox.

Being untracked, the mailbox is per-machine: a machine holds whichever messages
were forwarded to it, which may be one. Ingesting a partial mailbox is the
ordinary case and writes only that message's files, leaving every other
message's derivative alone; the summary's ``mailbox_is_complete`` says whether
this run saw every message the derivative records.

After running this, rerun py/main_estimate_uxlc_locations.py, which needs the
sibling UXLC-utils clone, and then py/main_render_uxlc_corrections.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import hkq_paths
from hkq_cmn.uxlc_email_extract import ingest_eml_files

DEFAULT_EML_DIR = hkq_paths.eml_dir()
DEFAULT_EMAILS_DIR = hkq_paths.emails_dir()
DEFAULT_IMAGE_DIR = hkq_paths.email_img_dir()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--eml-dir",
        type=Path,
        default=DEFAULT_EML_DIR,
        help="Untracked directory holding the .eml files.",
    )
    parser.add_argument("--emails-dir", type=Path, default=DEFAULT_EMAILS_DIR)
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    args = parser.parse_args()

    summary = ingest_eml_files(
        eml_dir=args.eml_dir,
        emails_dir=args.emails_dir,
        image_dir=args.image_dir,
    )
    summary["emails_dir"] = args.emails_dir.as_posix()
    summary["image_dir"] = args.image_dir.as_posix()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
