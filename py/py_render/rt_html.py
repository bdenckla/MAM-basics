from __future__ import annotations

from collections import Counter
from html import escape
import os
from pathlib import Path
from typing import Any

from py_render.rt_assets import write_report_assets
from py_render.rt_issue_tags import (
    HOLAM_HE_TAG,
    QYV_TAG,
)
from py_render.rt_matching_tmpl_args import (
    matching_template_arguments_in_mpu_verse_by_row_number,
    supported_qere_wrapper_by_row_number,
)
from py_render.rt_record_card import record_card_html
from py_render.rt_render_utils import (
    as_text,
    row_fragment_id,
    suppressed_output_path as build_suppressed_output_path,
)
from py_render.rt_summary import (
    filter_categories,
    summary_rows_html,
)
from py_render.rt_validate_holam_he import (
    evaluate_holam_he_row,
    require_holam_he_row_match,
)
from py_render.rt_validate_qyv import evaluate_qyv_row, require_qyv_row_match
from hkq_cmn.json_io import load_json
from hkq_cmn.table_row_github_issues import require_row_github_issue_metadata

MAIN_NAV_LABEL = "Active"
SUPPRESSED_NAV_LABEL = "Suppressed"
# The nav reaches this report's own two pages and the hand-written landing page,
# and stops there. It used to carry a fourth link, to the suggested-UXLC-changes
# report; Ben had it removed on 2026-08-11, the two bodies of work being separate
# and not to be cross-linked. index.html is where both are reachable from.
INDEX_PAGE = "index.html"
INDEX_NAV_LABEL = "Index"
MAIN_PAGE_TITLE = "Holman k/q"
SUPPRESSED_PAGE_TITLE = "Holman k/q - Suppressed"
MAIN_PAGE_HEADING = "Holman ketiv/qere review"
SUPPRESSED_PAGE_HEADING = "Suppressed"


def render_table_data_findings_html(
    table_json_path: Path, output_html_path: Path
) -> Path:
    payload = load_json(table_json_path)
    if not isinstance(payload, dict):
        raise ValueError("table_data.json root must be an object")
    table = payload.get("table")
    if not isinstance(table, dict):
        raise ValueError("table_data.json missing table object")
    rows_obj = table.get("rows")
    if not isinstance(rows_obj, list):
        raise ValueError("table_data.json table.rows must be a list")

    rows = [row for row in rows_obj if isinstance(row, dict)]
    if len(rows) != len(rows_obj):
        raise ValueError("table_data.json table.rows must contain only objects")

    _validate_issue_tag_definitions(rows)

    matching_template_arguments_by_row_number = (
        matching_template_arguments_in_mpu_verse_by_row_number(payload)
    )
    supported_qere_wrappers = supported_qere_wrapper_by_row_number(payload)
    finding_counts = Counter(as_text(row.get("finding", "")) for row in rows)
    sorted_findings = sorted(
        finding_counts.items(), key=lambda item: (-item[1], item[0])
    )
    finding_ids = {
        finding: f"f{idx:02d}" for idx, (finding, _count) in enumerate(sorted_findings)
    }

    css_output_path = output_html_path.with_suffix(".css")
    js_output_path = output_html_path.with_suffix(".js")
    write_report_assets(
        css_output_path=css_output_path,
        js_output_path=js_output_path,
        finding_ids=list(finding_ids.values()),
    )

    active_rows, suppressed_rows = _partition_rows(rows)
    suppressed_output_path = build_suppressed_output_path(output_html_path)

    _write_report_page(
        page_title=MAIN_PAGE_TITLE,
        page_heading=MAIN_PAGE_HEADING,
        page_subtitle="",
        rows=active_rows,
        sorted_findings=sorted_findings,
        finding_ids=finding_ids,
        matching_template_arguments_by_row_number=matching_template_arguments_by_row_number,
        supported_qere_wrappers=supported_qere_wrappers,
        output_html_path=output_html_path,
        css_output_path=css_output_path,
        js_output_path=js_output_path,
        repo_root=table_json_path.parent.parent,
        main_output_path=output_html_path,
        suppressed_output_path=suppressed_output_path,
        active_nav_label=MAIN_NAV_LABEL,
        records_heading="Records",
    )
    _write_report_page(
        page_title=SUPPRESSED_PAGE_TITLE,
        page_heading=SUPPRESSED_PAGE_HEADING,
        page_subtitle="Closed issues only",
        rows=suppressed_rows,
        sorted_findings=sorted_findings,
        finding_ids=finding_ids,
        matching_template_arguments_by_row_number=matching_template_arguments_by_row_number,
        supported_qere_wrappers=supported_qere_wrappers,
        output_html_path=suppressed_output_path,
        css_output_path=css_output_path,
        js_output_path=js_output_path,
        repo_root=table_json_path.parent.parent,
        main_output_path=output_html_path,
        suppressed_output_path=suppressed_output_path,
        active_nav_label=SUPPRESSED_NAV_LABEL,
        records_heading="Suppressed Records",
    )
    return output_html_path


def _write_report_page(
    *,
    page_title: str,
    page_heading: str,
    page_subtitle: str,
    rows: list[dict[str, Any]],
    sorted_findings: list[tuple[str, int]],
    finding_ids: dict[str, str],
    matching_template_arguments_by_row_number: dict[str, list[dict[str, str]]],
    supported_qere_wrappers: dict[str, dict[str, str]],
    output_html_path: Path,
    css_output_path: Path,
    js_output_path: Path,
    repo_root: Path,
    main_output_path: Path,
    suppressed_output_path: Path,
    active_nav_label: str,
    records_heading: str,
) -> None:
    categories = filter_categories(
        rows=rows,
        sorted_findings=sorted_findings,
        finding_ids=finding_ids,
        matching_template_arguments_by_row_number=matching_template_arguments_by_row_number,
    )
    summary_rows = summary_rows_html(categories)
    cards = "\n".join(
        record_card_html(
            row=row,
            finding_id=finding_ids[as_text(row.get("finding", ""))],
            output_html_path=output_html_path,
            repo_root=repo_root,
            matching_template_arguments_by_row_number=matching_template_arguments_by_row_number,
            supported_qere_wrappers=supported_qere_wrappers,
        )
        for row in rows
    )

    css_href = escape(
        os.path.relpath(css_output_path, output_html_path.parent).replace("\\", "/")
    )
    js_src = escape(
        os.path.relpath(js_output_path, output_html_path.parent).replace("\\", "/")
    )
    nav_html = _top_nav_html(
        current_output_path=output_html_path,
        main_output_path=main_output_path,
        suppressed_output_path=suppressed_output_path,
        active_nav_label=active_nav_label,
    )
    page_total = len(rows)
    summary_html = f'<div class="summary-columns">\n{summary_rows}\n</div>'
    page_subtitle_html = (
        "" if not page_subtitle else f'<p class="subtitle">{escape(page_subtitle)}</p>'
    )
    row_ids_on_page = sorted(
        row_fragment_id(as_text(row.get("row_number", ""))) for row in rows
    )
    other_page_href = (
        suppressed_output_path.name
        if output_html_path == main_output_path
        else main_output_path.name
    )
    row_ids_js = ", ".join(f'"{rid}"' for rid in row_ids_on_page)
    redirect_script_html = "\n".join(
        [
            "<script>",
            "(function () {",
            "  var h = window.location.hash;",
            "  if (!h) return;",
            "  var id = h.slice(1);",
            r"  if (!/^row\d+$/.test(id)) return;",
            f"  var here = new Set([{row_ids_js}]);",
            f'  if (!here.has(id)) window.location.replace("{other_page_href}" + h);',
            "})();",
            "</script>",
        ]
    )

    html = f"""<!DOCTYPE html>
<html lang=\"he\" dir=\"ltr\">
<head>
<meta charset=\"utf-8\">
{redirect_script_html}
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>{escape(page_title)}</title>
<link rel=\"stylesheet\" href=\"{css_href}\">
</head>
<body>
{nav_html}
<h1>{escape(page_heading)}</h1>
{page_subtitle_html}
<div class="meta-grid">
    <div class="meta-box">
        <div class="meta-label">Total Records</div>
        <div class="meta-value">{page_total}</div>
    </div>
    <div class="meta-box">
        <div class="meta-label">Visible/Filtered-out records</div>
        <div class="meta-value" id="visible-filtered-count">{page_total}/0</div>
    </div>
</div>
{summary_html}
<h2 class="section-title">{escape(records_heading)}</h2>
<div class="records">
{cards}
</div>
<script src=\"{js_src}\" defer></script>
</body>
</html>
"""

    output_html_path.parent.mkdir(parents=True, exist_ok=True)
    output_html_path.write_text(html, encoding="utf-8", newline="")


def _validate_issue_tag_definitions(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        row_number = as_text(row.get("row_number", ""))
        metadata = require_row_github_issue_metadata(row_number)

        holam_he_evaluation = evaluate_holam_he_row(row)
        if HOLAM_HE_TAG in metadata.tags:
            require_holam_he_row_match(
                row,
                context="tagged holam-he in findings renderer",
            )
        elif holam_he_evaluation.matches:
            raise ValueError(
                f"row {holam_he_evaluation.row_number} {holam_he_evaluation.verse} matches the holam-he definition but is missing the holam-he tag (findings renderer coverage check)"
            )

        evaluation = evaluate_qyv_row(row)
        if QYV_TAG in metadata.tags:
            require_qyv_row_match(row, context="tagged QyV in findings renderer")
            continue
        if evaluation.matches:
            raise ValueError(
                f"row {evaluation.row_number} {evaluation.verse} matches the QyV definition but is missing the qyv tag (findings renderer coverage check)"
            )


def _partition_rows(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active_rows: list[dict[str, Any]] = []
    suppressed_rows: list[dict[str, Any]] = []
    for row in rows:
        row_number = as_text(row.get("row_number", ""))
        metadata = require_row_github_issue_metadata(row_number)
        if metadata.is_closed:
            suppressed_rows.append(row)
        else:
            active_rows.append(row)
    return active_rows, suppressed_rows


def _top_nav_html(
    *,
    current_output_path: Path,
    main_output_path: Path,
    suppressed_output_path: Path,
    active_nav_label: str,
) -> str:
    main_href = escape(
        os.path.relpath(main_output_path, current_output_path.parent).replace("\\", "/")
    )
    suppressed_href = escape(
        os.path.relpath(suppressed_output_path, current_output_path.parent).replace(
            "\\", "/"
        )
    )
    main_class = "nav-link active" if active_nav_label == MAIN_NAV_LABEL else "nav-link"
    suppressed_class = (
        "nav-link active" if active_nav_label == SUPPRESSED_NAV_LABEL else "nav-link"
    )
    return (
        '<nav class="top-nav">\n'
        f'<a class="nav-link" href="{INDEX_PAGE}">{INDEX_NAV_LABEL}</a>\n'
        f'<a class="{main_class}" href="{main_href}">{MAIN_NAV_LABEL}</a>\n'
        f'<a class="{suppressed_class}" href="{suppressed_href}">{SUPPRESSED_NAV_LABEL}</a>\n'
        "</nav>"
    )
