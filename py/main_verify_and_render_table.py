"""Verify and render Holman's tracked ketiv/qere review data.

The review document was extracted once in ``holman-ketiv-qere``.  The tracked
JSON, introduction, and cropped images are now the source material; the review
document remains in that repository's Git history rather than in the live
pipeline.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import hkq_paths
from hkq_cmn.json_io import load_json, write_json
from hkq_cmn.verify_table_notes_in_uxlc import verify_table_notes_in_uxlc
from hkq_cmn.verify_table_words_in_mam_plus import verify_table_words_in_mam_plus
from mb_cmn import paths
from py_render.rt_html import render_table_data_findings_html

DEFAULT_MAM_PARSED_PATH = paths.sibling_repo("MAM-parsed")
DEFAULT_UXLC_UTILS_PATH = paths.repo_root()
DEFAULT_TABLE_JSON_PATH = hkq_paths.table_data_json_path()
DEFAULT_FINDINGS_HTML_PATH = hkq_paths.findings_html_path()


def persist_verify_summary(
    table_json_path: Path,
    verify_report: dict[str, object],
    uxlc_verify_report: dict[str, object],
) -> None:
    """Persist idempotent verification context inside the tracked review table."""
    table_data = load_json(table_json_path)
    if not isinstance(table_data, dict):
        raise ValueError("review table root must be an object")

    verify_summary = verify_report.get("summary")
    doc_note_rows = verify_report.get("rows_matching_mpu_verse_template_arg")
    wrapper_rows = verify_report.get("rows_with_supported_qere_wrapper")
    uxlc_verify_summary = uxlc_verify_report.get("summary")
    uxlc_missing_rows = uxlc_verify_report.get("rows_missing_claims")
    required_values = (
        verify_summary,
        doc_note_rows,
        wrapper_rows,
        uxlc_verify_summary,
        uxlc_missing_rows,
    )
    if any(value is None for value in required_values):
        raise ValueError("review-data verification report is invalid")

    table_data["mam_plus_verify"] = verify_summary
    table_data["mam_plus_rows_matching_mpu_verse_template_arg"] = doc_note_rows
    table_data["mam_plus_rows_with_supported_qere_wrapper"] = wrapper_rows
    table_data["uxlc_verify"] = uxlc_verify_summary
    table_data["uxlc_rows_missing_note_claims"] = uxlc_missing_rows
    write_json(table_json_path, table_data)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Verify and render Holman's tracked ketiv/qere review data."
    )
    parser.add_argument(
        "--table-json-path",
        type=Path,
        default=DEFAULT_TABLE_JSON_PATH,
        help="Tracked review-data JSON to verify and render.",
    )
    parser.add_argument(
        "--findings-html-path",
        type=Path,
        default=DEFAULT_FINDINGS_HTML_PATH,
        help="Rendered findings page to write.",
    )
    parser.add_argument(
        "--mam-parsed-path",
        type=Path,
        default=DEFAULT_MAM_PARSED_PATH,
        help="Sibling MAM-parsed repository used for verification.",
    )
    parser.add_argument(
        "--uxlc-utils-path",
        type=Path,
        default=DEFAULT_UXLC_UTILS_PATH,
        help="MAM-basics root holding the canonical UXLC XML used for verification.",
    )
    args = parser.parse_args()

    verify_report = verify_table_words_in_mam_plus(
        table_json_path=args.table_json_path,
        mam_parsed_path=args.mam_parsed_path,
    )
    uxlc_verify_report = verify_table_notes_in_uxlc(
        table_json_path=args.table_json_path,
        uxlc_utils_path=args.uxlc_utils_path,
    )
    persist_verify_summary(
        table_json_path=args.table_json_path,
        verify_report=verify_report,
        uxlc_verify_report=uxlc_verify_report,
    )
    render_table_data_findings_html(
        table_json_path=args.table_json_path,
        output_html_path=args.findings_html_path,
    )

    verify_summary = verify_report["summary"]
    uxlc_verify_summary = uxlc_verify_report["summary"]
    if not isinstance(verify_summary, dict) or not isinstance(
        uxlc_verify_summary, dict
    ):
        raise ValueError("review-data verification summary is invalid")

    failures = {
        "missing_any_plus_count": verify_summary["missing_any_plus_count"],
        "missing_mpu_verse_text_count": verify_summary["missing_mpu_verse_text_count"],
        "rows_supported_qere_wrapper_mismatch_count": verify_summary[
            "rows_supported_qere_wrapper_mismatch_count"
        ],
        "rows_missing_uxlc_claim_count": uxlc_verify_summary[
            "rows_missing_claim_count"
        ],
    }
    if any(failures.values()):
        formatted = ", ".join(f"{name}={count}" for name, count in failures.items())
        raise ValueError(f"review-data verification failed: {formatted}")

    print(
        "Verified and rendered the 77-row Holman review: "
        f"{args.findings_html_path.as_posix()}"
    )


if __name__ == "__main__":
    main()
