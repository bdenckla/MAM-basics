from __future__ import annotations

from pathlib import Path

from accgram import dual_cant_readings
from accgram import rtms_meteg_witness
from accgram import rtmsr_overview
from mb_cmn import file_io
import wlc_provenance as provenance


def write_ungrammatical_payload(
    *,
    ungrammatical_out_path: Path,
    ungrammatical_in_path: Path,
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
    enriched_ungrammatical_rows: list[dict[str, object]],
    source_file: str,
) -> None:
    serializable_rows = rtms_meteg_witness.strip_internal_witness_fields_from_rows(
        enriched_ungrammatical_rows
    )
    serializable_rows = dual_cant_readings.without_heavy_reading_fields(
        serializable_rows
    )
    ungrammatical_payload: dict[str, object] = {
        "artifacts_description": "enriched ungrammatical verse research records",
        "payload_provenance_note": (
            "This artifact augments existing ungrammatical rows with linked verse payloads "
            "from wlc422-kq-u, XML-ish UXLC verse nodes, and normalized MAM-simple verses."
        ),
        "input": str(ungrammatical_in_path),
        "wlc422_kq_u_dir": str(wlc422_kq_u_dir),
        "uxlc_dir": str(uxlc_dir),
        "mam_simple_dir": str(mam_simple_dir),
        "summary": {
            "oddballs": len(serializable_rows),
        },
        "oddballs": serializable_rows,
    }
    ungrammatical_payload = provenance.with_json_provenance(
        ungrammatical_payload, source_file
    )
    _write_json(ungrammatical_out_path, ungrammatical_payload)


def write_html_reports(
    html_out_path: Path,
    *,
    enriched_ungrammatical_rows: list[dict[str, object]],
    base_dir: Path | None = None,
) -> Path:
    # The page (rtmsr_overview) sorts its rows into reading order itself, so no
    # per-list sort is needed here.
    return rtmsr_overview.write_goerwitz_combined_html_report(
        html_out_path,
        enriched_ungrammatical_rows,
        base_dir,
    )


def print_run_summary(
    *,
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
    all_changes_path: Path,
    combined_html_out_path: Path,
    ungrammatical_in_path: Path,
    ungrammatical_out_path: Path,
    ungrammatical_rows_count: int,
) -> None:
    print(f"wlc422-kq-u dir: {wlc422_kq_u_dir}")
    print(f"UXLC dir: {uxlc_dir}")
    print(f"MAM-simple dir: {mam_simple_dir}")
    print(f"All changes: {all_changes_path}")
    print(f"Input ungrammatical: {ungrammatical_in_path}")
    print(f"Ungrammatical output: {ungrammatical_out_path}")
    print(f"Ungrammatical rows: {ungrammatical_rows_count}")
    print(f"Combined HTML output: {combined_html_out_path}")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    # Through file_io, so the write is atomic (temp file + os.replace) and the
    # replace retries on PermissionError. A bare path.open() here once died with
    # "OSError: [Errno 22] Invalid argument" mid-run on a transient Windows lock
    # (indexer/AV), taking the whole generate-html run with it; the same command
    # succeeded on the next try. file_io's own dump is byte-for-byte what this
    # used to write: ensure_ascii=False, indent=2, trailing "\n", newline
    # untranslated. Provenance is already on the payload (wlc_provenance, which
    # names the repo), so do not pass generator_file.
    file_io.json_dump_to_file_path(payload, str(path))
