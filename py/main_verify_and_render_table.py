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

DEFAULT_MAM_PARSED_PATH = paths.mam_parsed_dir()
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


def _failing_rows(
    verify_report: dict[str, object], uxlc_verify_report: dict[str, object]
) -> list[str]:
    """One line per failed row check, naming the check, the row's verse and its word."""
    lines = []
    for check, key in (
        ("not in any MAM-parsed-plus file", "missing_any_plus"),
        ("not in its MAM-parsed-plus verse", "missing_mpu_verse_text_rows"),
        (
            "a supported qere wrapper with no matching template argument",
            "rows_supported_qere_wrapper_mismatch",
        ),
    ):
        for row in verify_report[key]:
            lines.append(
                f"row {row['row_number']}, {row['verse']}, {row['word']}: {check}"
            )
    for row in uxlc_verify_report["rows_missing_claims"]:
        lines.append(
            f"row {row['row_number']}, {row['verse']}, ketiv {row['ketiv_claim']}"
            f" and qere {row['qere_claim']}: a claim not found in UXLC"
        )
    return lines


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
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
        help="MAM-parsed product directory used for verification.",
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

    verify_summary = verify_report["summary"]
    uxlc_verify_summary = uxlc_verify_report["summary"]
    if not isinstance(verify_summary, dict) or not isinstance(
        uxlc_verify_summary, dict
    ):
        raise ValueError("review-data verification summary is invalid")
    # Verify before writing anything, so that a failed row leaves the table and page as they
    # were rather than recording the failure in both.
    failing = _failing_rows(verify_report, uxlc_verify_report)
    if failing:
        print("\n".join(failing), file=sys.stderr)
        raise ValueError(
            f"review-data verification failed for {len(failing)} row check(s);"
            " nothing was written"
        )

    persist_verify_summary(
        table_json_path=args.table_json_path,
        verify_report=verify_report,
        uxlc_verify_report=uxlc_verify_report,
    )
    render_table_data_findings_html(
        table_json_path=args.table_json_path,
        output_html_path=args.findings_html_path,
        report_css_href=(
            "../report.css"
            if args.findings_html_path.resolve().parent
            == DEFAULT_FINDINGS_HTML_PATH.resolve().parent
            else None
        ),
    )

    print(
        f"Verified and rendered the {verify_summary['row_count']}-row Holman review: "
        f"{args.findings_html_path.as_posix()}"
    )


if __name__ == "__main__":
    main()
