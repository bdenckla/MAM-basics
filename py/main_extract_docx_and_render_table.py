from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

import hkq_paths
from mb_cmn import paths
from py_render.rt_html import (
    render_table_data_findings_html,
)
from hkq_cmn.json_io import load_json, write_json
from hkq_cmn.extract_docx_pipeline import parse_docx_archive, write_extract_files
from hkq_cmn.verify_table_notes_in_uxlc import verify_table_notes_in_uxlc
from hkq_cmn.verify_table_words_in_mam_plus import verify_table_words_in_mam_plus

DEFAULT_DOCX_PATH = hkq_paths.review_docx_path()
DEFAULT_MAM_PARSED_PATH = paths.sibling_repo("MAM-parsed")
DEFAULT_UXLC_UTILS_PATH = paths.uxlc_utils_dir()
DEFAULT_SERVED_DOCS_DIR = hkq_paths.gh_pages_dir()
DEFAULT_NONSERVED_DOCS_DIR = hkq_paths.docs_not_served_dir()


def source_document_reference(docx_path: Path) -> str:
    """Return a stable, data-root-relative path when the source file is inside that repo."""
    try:
        relative = docx_path.resolve().relative_to(hkq_paths.hkq_data_root().resolve())
    except ValueError:
        return str(docx_path)
    return relative.as_posix()


def extract(
    docx_path: Path,
    served_docs_dir: Path,
    nonserved_docs_dir: Path,
) -> dict[str, object]:
    image_dir = served_docs_dir / "img"
    image_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx_path) as archive:
        parsed = parse_docx_archive(
            archive=archive,
            image_dir=image_dir,
            data_root=hkq_paths.hkq_data_root(),
        )

    intro_path, json_path = write_extract_files(
        nonserved_output_dir=nonserved_docs_dir,
        source_document=source_document_reference(docx_path),
        parsed=parsed,
    )

    image_count = sum(
        len(paths)
        for row in parsed.data_rows
        for paths in row.get("image_files", {}).values()
    )
    return {
        "introduction_path": intro_path.as_posix(),
        "json_path": json_path.as_posix(),
        "image_dir": image_dir.as_posix(),
        "row_count": len(parsed.data_rows),
        "image_count": image_count,
    }


def persist_verify_summary(
    table_json_path: Path,
    verify_report: dict[str, object],
    uxlc_verify_report: dict[str, object],
) -> None:
    """Persist verification output inside extracted table_data.json."""
    table_data = load_json(table_json_path)
    if not isinstance(table_data, dict):
        raise ValueError("extracted table_data.json root must be an object")

    verify_summary = verify_report.get("summary")
    if not isinstance(verify_summary, dict):
        raise ValueError("verification summary is invalid")

    doc_note_rows = verify_report.get("rows_matching_mpu_verse_template_arg")
    if not isinstance(doc_note_rows, list):
        raise ValueError("verification rows_matching_mpu_verse_template_arg is invalid")

    wrapper_rows = verify_report.get("rows_with_supported_qere_wrapper")
    if not isinstance(wrapper_rows, list):
        raise ValueError("verification rows_with_supported_qere_wrapper is invalid")

    uxlc_verify_summary = uxlc_verify_report.get("summary")
    if not isinstance(uxlc_verify_summary, dict):
        raise ValueError("UXLC verification summary is invalid")

    uxlc_missing_rows = uxlc_verify_report.get("rows_missing_claims")
    if not isinstance(uxlc_missing_rows, list):
        raise ValueError("UXLC verification rows_missing_claims is invalid")

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
        description="Extract the introduction, table data, and embedded images from the source DOCX."
    )
    parser.add_argument(
        "docx_path",
        type=Path,
        nargs="?",
        default=DEFAULT_DOCX_PATH,
        help="Source DOCX to extract. Defaults to the tracked repo copy at repo top level.",
    )
    parser.add_argument(
        "--served-docs-dir",
        type=Path,
        default=DEFAULT_SERVED_DOCS_DIR,
        help="Directory where served HTML, CSS, JS, and img/ assets will be written.",
    )
    parser.add_argument(
        "--docs-not-served-dir",
        type=Path,
        default=DEFAULT_NONSERVED_DOCS_DIR,
        help="Directory where introduction.md and table_data.json will be written.",
    )
    parser.add_argument(
        "--mam-parsed-path",
        type=Path,
        default=DEFAULT_MAM_PARSED_PATH,
        help="Path to sibling MAM-parsed repo used for mandatory post-extraction verification.",
    )
    parser.add_argument(
        "--uxlc-utils-path",
        type=Path,
        default=DEFAULT_UXLC_UTILS_PATH,
        help="Path to sibling UXLC-utils repo used for mandatory UXLC note verification.",
    )
    args = parser.parse_args()

    summary = extract(
        docx_path=args.docx_path,
        served_docs_dir=args.served_docs_dir,
        nonserved_docs_dir=args.docs_not_served_dir,
    )
    table_json_path = args.docs_not_served_dir / "table_data.json"
    findings_html_path = args.served_docs_dir / "table_data_findings.html"
    verify_report = verify_table_words_in_mam_plus(
        table_json_path=table_json_path,
        mam_parsed_path=args.mam_parsed_path,
    )
    uxlc_verify_report = verify_table_notes_in_uxlc(
        table_json_path=table_json_path,
        uxlc_utils_path=args.uxlc_utils_path,
    )

    verify_summary = verify_report["summary"]
    if not isinstance(verify_summary, dict):
        raise ValueError("verification summary is invalid")

    uxlc_verify_summary = uxlc_verify_report["summary"]
    if not isinstance(uxlc_verify_summary, dict):
        raise ValueError("UXLC verification summary is invalid")

    missing_any = verify_summary["missing_any_plus_count"]
    missing_mpu_verse_text = verify_summary["missing_mpu_verse_text_count"]
    supported_qere_wrapper_mismatches = verify_summary[
        "rows_supported_qere_wrapper_mismatch_count"
    ]
    missing_uxlc_claims = uxlc_verify_summary["rows_missing_claim_count"]
    summary["mam_plus_verify"] = verify_summary
    summary["uxlc_verify"] = uxlc_verify_summary
    persist_verify_summary(
        table_json_path=table_json_path,
        verify_report=verify_report,
        uxlc_verify_report=uxlc_verify_report,
    )
    render_table_data_findings_html(
        table_json_path=table_json_path,
        output_html_path=findings_html_path,
    )
    summary["findings_html_path"] = findings_html_path.as_posix()

    if (
        missing_any
        or missing_mpu_verse_text
        or supported_qere_wrapper_mismatches
        or missing_uxlc_claims
    ):
        raise ValueError(
            "post-extraction verification failed: "
            f"missing_any_plus_count={missing_any}, "
            f"missing_mpu_verse_text_count={missing_mpu_verse_text}, "
            f"rows_supported_qere_wrapper_mismatch_count={supported_qere_wrapper_mismatches}, "
            f"rows_missing_uxlc_claim_count={missing_uxlc_claims}"
        )

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
