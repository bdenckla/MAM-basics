"""Render the suggested-UXLC-corrections report from the emails under emails/.

Run from repo root:
    .venv\\Scripts\\python.exe py/main_render_uxlc_corrections.py

Writes gh-pages/uxlc_corrections.{html,css,js}, the extracted attachments under
gh-pages/uxlc_img/, and the extract itself to
docs-not-served/uxlc_corrections.json. The JSON is tracked so that regenerating
and reading the diff is the test: a parse that changes silently cannot.

Reads only what is tracked, so a fresh clone can run it. The manuscript
locations it shows come from data/uxlc_atom_locations.json, which
py/main_estimate_uxlc_locations.py writes and which needs the sibling
UXLC-utils clone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import hkq_paths
from py_render.uc_html import render_uxlc_corrections_html

DEFAULT_EMAILS_DIR = hkq_paths.emails_dir()
DEFAULT_OUTPUT_HTML = hkq_paths.uxlc_corrections_html_path()
DEFAULT_IMAGE_DIR = hkq_paths.email_img_dir()
DEFAULT_ASSETS_DIR = hkq_paths.assets_dir()
DEFAULT_DATA_DIR = hkq_paths.data_dir()
DEFAULT_JSON_OUTPUT = hkq_paths.uxlc_corrections_json_path()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emails-dir", type=Path, default=DEFAULT_EMAILS_DIR)
    parser.add_argument("--output-html-path", type=Path, default=DEFAULT_OUTPUT_HTML)
    parser.add_argument("--image-dir", type=Path, default=DEFAULT_IMAGE_DIR)
    parser.add_argument("--assets-dir", type=Path, default=DEFAULT_ASSETS_DIR)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--json-output-path", type=Path, default=DEFAULT_JSON_OUTPUT)
    args = parser.parse_args()

    summary = render_uxlc_corrections_html(
        emails_dir=args.emails_dir,
        output_html_path=args.output_html_path,
        image_dir=args.image_dir,
        assets_dir=args.assets_dir,
        data_dir=args.data_dir,
        json_output_path=args.json_output_path,
    )
    summary["output_html_path"] = args.output_html_path.as_posix()
    summary["json_output_path"] = args.json_output_path.as_posix()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
