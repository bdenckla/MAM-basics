"""Render the generated versification differences Markdown document."""

from pathlib import Path

from mb_cmn import provenance
from versification_differences import combined
from versification_differences import case_data
from versification_differences import extract

_GENERATOR_FILE = Path(__file__).with_name("generate_doc.py")


def render_intro_overview_summary_markdown():
    lines = [
        f"<!-- {provenance.generated_html_comment(_GENERATOR_FILE)} -->",
        "",
        "# Versification Differences: MAM, BHS, and Sefaria",
        "",
        "MAM-simple provides three versification traditions (vtrad), that is, three",
        "ways of placing cv-labels (chapter/verse labels) across the same Hebrew text:",
        "",
        "- **vtrad-mam** — MAM versification",
        "- **vtrad-bhs** — BHS versification (Biblia Hebraica Stuttgartensia)",
        "- **vtrad-sef** — Sefaria versification",
        "",
        "In most of the Bible, all three traditions place the same cv-labels at the",
        "same points in the text. This document describes every place where cv-labels",
        "differ in location and/or contents.",
        "",
        "## Overview",
        "",
        "There are three main kinds of difference:",
        "",
    ]
    lines.extend(_render_overview_items())
    lines.extend(
        (
            "",
            "Note that here in this document, we are not concerned with the notion of a *chanted verse*;",
            "that is, we are not concerned with where *sof pasuq* and/or *silluq* falls. Here, when we say",
            '"verse", we mean only the span of text between cv-labels. The fact that this span',
            "usually corresponds to a chanted verse is irrelevant here.",
            "",
            "The eight cases where differences occur are:",
            "",
            "| Book | Passage | Classification |",
            "|------|---------|----------------|",
        )
    )
    lines.extend(_render_summary_rows())
    lines.extend(("", "---", ""))
    return "\n".join(lines)


def render_bhs_simple_shift_sections_markdown(books_mpu):
    sections = extract.extract_bhs_simple_shift_sections(books_mpu)
    return _render_bhs_sections_markdown(sections, include_bhs_heading=True)


def render_bhs_generated_sections_markdown(books_mpu):
    sections = (
        extract.extract_bhs_simple_shift_sections(books_mpu)
        + extract.extract_bhs_early_one_vs_many_sections(books_mpu)
        + extract.extract_bhs_late_one_vs_many_sections(books_mpu)
        + extract.extract_bhs_complex_boundary_sections(books_mpu)
        + extract.extract_bhs_present_vs_absent_sections(books_mpu)
    )
    sections = tuple(sorted(sections, key=lambda section: section.heading))
    return _render_bhs_sections_markdown(sections, include_bhs_heading=True) + "\n---\n"


def render_bhs_early_one_vs_many_sections_markdown(books_mpu):
    sections = extract.extract_bhs_early_one_vs_many_sections(books_mpu)
    return _render_bhs_sections_markdown(sections, include_bhs_heading=False)


def render_bhs_late_one_vs_many_sections_markdown(books_mpu):
    sections = extract.extract_bhs_late_one_vs_many_sections(books_mpu)
    return _render_bhs_sections_markdown(sections, include_bhs_heading=False)


def render_bhs_complex_boundary_sections_markdown(books_mpu):
    sections = extract.extract_bhs_complex_boundary_sections(books_mpu)
    return _render_bhs_sections_markdown(sections, include_bhs_heading=False)


def render_bhs_present_vs_absent_sections_markdown(books_mpu):
    sections = extract.extract_bhs_present_vs_absent_sections(books_mpu)
    return (
        _render_bhs_sections_markdown(sections, include_bhs_heading=False) + "\n---\n"
    )


def render_sef_generated_sections_markdown(books_mpu):
    prose_sections = (
        extract.extract_sef_simple_shift_sections()
        + extract.extract_sef_early_one_vs_many_sections()
        + extract.extract_sef_present_vs_absent_sections()
    )
    prose_sections = tuple(sorted(prose_sections, key=lambda section: section.heading))
    lines = ["## Sefaria Versification", ""]
    lines.extend(
        (
            "Sefaria has the same simple chapter-boundary shifts as BHS in 1 Samuel and",
            "Jeremiah, the same one-vs-many cases as BHS at the start of both Decalogues,",
            "and the same present-vs-absent case in Joshua 21. It does **not** adopt the",
            "BHS one-vs-many cases in the late Decalogue passages, nor the Numbers",
            "one-vs-many case with a complex chapter-boundary shift.",
            "",
        )
    )
    for section in prose_sections:
        lines.extend(_render_prose_section_lines(section))
    return "\n".join(lines).rstrip() + "\n\n---\n"


def render_combined_table_markdown(books_mpu):
    return combined.render_combined_table_markdown(books_mpu)


def render_how_mam_simple_records_these_differences_markdown():
    lines = [
        "## How MAM-simple Records These Differences",
        "",
        "The tables above treat the Hebrew span as primary. Internally, however, the",
        "`vtrad-bhs` and `vtrad-sef` output files (XML and JSON) still record these",
        "differences relative to MAM, because MAM is the underlying source text. Every",
        "non-MAM verse whose label diverges from its MAM source carries two attributes:",
        "",
        "- **`contents-corresponds-to`** — one of:",
        '  - `"a full verse in MAM"` — shifted verse; the content is identical to a',
        "    complete MAM verse",
        '  - `"less than a full verse in MAM"` — partial verse; the content is a',
        "    portion of one MAM verse (splits)",
        '  - `"no verse in MAM"` — the verse has no corresponding content in MAM',
        "    (the two absent Joshua 21 verses)",
        "- **`osisID-of-MAM-src`** — the OSIS ID of the MAM source verse (present for",
        "  the first two cases above, absent for the third)",
        "",
        "For example:",
        "",
        "```xml",
        "<!-- Chapter-boundary shift: 1 Sam 23:29 (MAM) → 1 Sam 24:1 (BHS/Sef) -->",
        '<verse osisID="1Sam.24.1"',
        '       contents-corresponds-to="a full verse in MAM"',
        '       osisID-of-MAM-src="1Sam.23.29" .../>',
        "",
        "<!-- Decalogue split: MAM Deut 5:6 → BHS/Sef 5:6 (first part) -->",
        '<verse osisID="Deut.5.6"',
        '       contents-corresponds-to="less than a full verse in MAM"',
        '       osisID-of-MAM-src="Deut.5.6" .../>',
        "",
        "<!-- Joshua 21: verse number inserted where MAM has no text -->",
        '<verse osisID="Josh.21.36"',
        '       contents-corresponds-to="no verse in MAM"',
        '       text="—"/>',
        "```",
    ]
    return "\n".join(lines) + "\n"


def render_full_markdown(books_mpu):
    parts = (
        render_intro_overview_summary_markdown(),
        render_bhs_generated_sections_markdown(books_mpu),
        render_sef_generated_sections_markdown(books_mpu),
        render_combined_table_markdown(books_mpu),
        render_how_mam_simple_records_these_differences_markdown(),
    )
    return "\n\n".join(part.rstrip("\n") for part in parts) + "\n"


def _render_overview_items():
    lines = []
    for idx, overview_item in enumerate(case_data.OVERVIEW_CLASSIFICATIONS, start=1):
        lines.append(f"{idx}. **{overview_item.display_title}** —")
        lines.extend(f"  {line}" for line in overview_item.body_lines)
    return lines


def _render_summary_rows():
    rows = []
    for case_rec in case_data.CASES:
        book_label = case_data.doc_book_label(case_rec.book_id)
        rows.append(
            "| "
            + book_label
            + " | "
            + case_rec.summary_passage_label
            + " | "
            + case_rec.classification
            + " |"
        )
    return rows


def _render_bhs_sections_markdown(sections, include_bhs_heading):
    lines = []
    if include_bhs_heading:
        lines.extend(("## BHS Versification", ""))
    for section in sections:
        lines.extend(_render_vtrad_section_lines(section))
    return "\n".join(lines).rstrip() + "\n"


def _render_vtrad_section_lines(section):
    lines = []
    if getattr(section, "anchor_id", None):
        lines.extend((f'<a id="{section.anchor_id}"></a>', ""))
    lines.extend((section.heading, ""))
    lines.extend(section.intro_lines)
    lines.append("")
    lines.extend(
        (
            f"| Hebrew range | MAM | {section.other_vtrad_label} |",
            section.table_separator,
        )
    )
    lines.extend(
        "|"
        + (" " + row.hebrew_range if row.hebrew_range else "")
        + " | "
        + row.mam_label
        + " | "
        + row.other_label
        + " |"
        for row in section.rows
    )
    if section.note_lines:
        lines.append("")
        lines.extend(section.note_lines)
    lines.append("")
    return lines


def _render_prose_section_lines(section):
    return [section.heading, "", *section.body_lines, ""]
