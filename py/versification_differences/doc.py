"""Render the generated versification differences HTML document."""

import re
from html import escape
from pathlib import Path

from mb_cmn import provenance
from versification_differences import combined
from versification_differences import case_data
from versification_differences import extract

_GENERATOR_FILE = Path(__file__).with_name("generate_doc.py")
_TITLE = "Versification Differences: MAM, BHS, and Sefaria"


class _Headings:
    """Preserve the former GitHub heading fragments, including duplicate suffixes."""

    def __init__(self):
        self.seen = {}

    def render(self, level, title, anchor_id=None):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = self.seen.get(slug, 0)
        self.seen[slug] = count + 1
        legacy_id = slug + (f"-{count}" if count else "")
        anchor = f'<a id="{anchor_id}"></a>\n' if anchor_id else ""
        return anchor + f'<h{level} id="{legacy_id}">{escape(title)}</h{level}>'


def render_intro_overview_summary_html(headings):
    lines = [
        headings.render(1, _TITLE),
        "<p>MAM-simple provides three versification traditions (vtrad), that is, three",
        "ways of placing cv-labels (chapter/verse labels) across the same Hebrew text:</p>",
        "<ul>",
        "<li><strong>vtrad-mam</strong> — MAM versification</li>",
        "<li><strong>vtrad-bhs</strong> — BHS versification (Biblia Hebraica Stuttgartensia)</li>",
        "<li><strong>vtrad-sef</strong> — Sefaria versification</li>",
        "</ul>",
        "<p>In most of the Bible, all three traditions place the same cv-labels at the",
        "same points in the text. This document describes every place where cv-labels",
        "differ in location and/or contents.</p>",
        headings.render(2, "Overview"),
        "<p>There are three main kinds of difference:</p>",
        "<ol>",
    ]
    for item in case_data.OVERVIEW_CLASSIFICATIONS:
        lines.append(f"<li><strong>{escape(item.display_title)}</strong> —")
        lines.extend(item.body_lines)
        lines.append("</li>")
    lines.extend(
        (
            "</ol>",
            '<p>Within <em>this</em> document, "verse" means only the span of text between cv-labels.',
            "How these spans are cantillated is not relevant to this document.",
            "So, we could say that this document is only concerned with the boundaries of numbered verses,",
            "not the boundaries of chanted verses. For example, this document is not concerned with",
            'where <span class="romanized">sof pasuq</span> falls.',
            "Nonetheless, in five of the eight cases below — the four Decalogue splits and the Num. 25/26 boundary —",
            "cantillation can help explain why the versification difference arose.",
            'The role of cantillation in those five cases is discussed in <a href="versification-and-cantillation.html">versification-and-cantillation.html</a>.</p>',
            "<p>The eight cases where differences occur are:</p>",
            "<table>",
            "<thead><tr><th>Book</th><th>Passage</th><th>Classification</th></tr></thead>",
            "<tbody>",
        )
    )
    for case in case_data.CASES:
        lines.append(
            f"<tr><td>{escape(case_data.doc_book_label(case.book_id))}</td>"
            f"<td>{escape(case.summary_passage_label)}</td>"
            f"<td>{escape(case.classification)}</td></tr>"
        )
    lines.extend(("</tbody></table>", "<hr>"))
    return "\n".join(lines)


def render_bhs_generated_sections_html(books_mpu, headings):
    sections = (
        extract.extract_bhs_simple_shift_sections(books_mpu)
        + extract.extract_bhs_early_one_vs_many_sections(books_mpu)
        + extract.extract_bhs_late_one_vs_many_sections(books_mpu)
        + extract.extract_bhs_complex_boundary_sections(books_mpu)
        + extract.extract_bhs_present_vs_absent_sections(books_mpu)
    )
    lines = [headings.render(2, "BHS Versification")]
    for section in sorted(sections, key=lambda section: section.heading):
        lines.extend(
            (
                headings.render(3, section.heading, section.anchor_id),
                "<p>" + "\n".join(section.intro_lines) + "</p>",
                "<table>",
                "<thead><tr><th>Hebrew range</th><th>MAM</th>"
                f"<th>{escape(section.other_vtrad_label)}</th></tr></thead>",
                "<tbody>",
            )
        )
        for row in section.rows:
            lines.append(
                f'<tr><td dir="rtl" lang="hbo">{escape(row.hebrew_range)}</td>'
                f'<td class="cv">{row.mam_label}</td>'
                f'<td class="cv">{row.other_label}</td></tr>'
            )
        lines.append("</tbody></table>")
        if section.note_lines:
            lines.append(
                "<blockquote><p>" + "\n".join(section.note_lines) + "</p></blockquote>"
            )
    lines.append("<hr>")
    return "\n".join(lines)


def render_sef_generated_sections_html(headings):
    sections = (
        extract.extract_sef_simple_shift_sections()
        + extract.extract_sef_early_one_vs_many_sections()
        + extract.extract_sef_present_vs_absent_sections()
    )
    lines = [
        headings.render(2, "Sefaria Versification"),
        "<p>Sefaria has the same simple chapter-boundary shifts as BHS in 1 Samuel and",
        "Jeremiah, the same one-vs-many cases as BHS at the start of both Decalogues,",
        "and the same present-vs-absent case in Joshua 21. It does <strong>not</strong> adopt the",
        "BHS one-vs-many cases in the late Decalogue passages, nor the Numbers",
        "one-vs-many case with a complex chapter-boundary shift.</p>",
    ]
    for section in sorted(sections, key=lambda section: section.heading):
        lines.extend(
            (
                headings.render(3, section.heading),
                "<p>" + "\n".join(section.body_lines) + "</p>",
            )
        )
    lines.append("<hr>")
    return "\n".join(lines)


def render_how_mam_simple_records_these_differences_html(headings):
    example = """<!-- Chapter-boundary shift: 1 Sam 23:29 (MAM) → 1 Sam 24:1 (BHS/Sef) -->
<verse osisID="1Sam.24.1"
       contents-corresponds-to="a full verse in MAM"
       osisID-of-MAM-src="1Sam.23.29" .../>

<!-- Decalogue split: MAM Deut 5:6 → BHS/Sef 5:6 (first part) -->
<verse osisID="Deut.5.6"
       contents-corresponds-to="less than a full verse in MAM"
       osisID-of-MAM-src="Deut.5.6" .../>

<!-- Joshua 21: verse number inserted where MAM has no text -->
<verse osisID="Josh.21.36"
       contents-corresponds-to="no verse in MAM"
       text="—"/>
"""
    return headings.render(2, "How MAM-simple Records These Differences") + """
<p>The tables above treat the Hebrew span as primary. Internally, however, the
<code>vtrad-bhs</code> and <code>vtrad-sef</code> output files (XML and JSON) still record these
differences relative to MAM, because MAM is the underlying source text. Every
non-MAM verse whose label diverges from its MAM source has two attributes:</p>
<ul>
<li><strong><code>contents-corresponds-to</code></strong> — one of:
<ul>
<li><code>"a full verse in MAM"</code> — shifted verse; the content is identical to a complete MAM verse</li>
<li><code>"less than a full verse in MAM"</code> — partial verse; the content is a portion of one MAM verse (splits)</li>
<li><code>"no verse in MAM"</code> — the verse has no corresponding content in MAM (the two absent Joshua 21 verses)</li>
</ul>
</li>
<li><strong><code>osisID-of-MAM-src</code></strong> — the OSIS ID of the MAM source verse (present for
the first two cases above, absent for the third)</li>
</ul>
<p>For example:</p>
<pre><code class="language-xml">""" + escape(example) + "</code></pre>"


def render_full_html(books_mpu):
    headings = _Headings()
    parts = (
        render_intro_overview_summary_html(headings),
        render_bhs_generated_sections_html(books_mpu, headings),
        render_sef_generated_sections_html(headings),
        headings.render(2, "Combined Table: All Differences"),
        combined.render_combined_table_html(books_mpu),
        render_how_mam_simple_records_these_differences_html(headings),
    )
    comment = provenance.generated_html_comment(_GENERATOR_FILE)
    body = "\n\n".join(parts)
    return f"""<!doctype html>
<!-- {comment} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_TITLE}</title>
<link rel="stylesheet" href="../document.css">
<link rel="stylesheet" href="documentation.css">
</head>
<body>
<nav aria-label="Documentation"><a href="index.html">MAM-simple</a> · <a href="reading-mam-simple.html">Overview</a> · <a href="reading-mam-simple-xml.html">XML</a> · <a href="reading-mam-simple-json.html">JSON</a> · <a href="versification-and-cantillation.html">Versification and cantillation</a></nav>
{body}
</body>
</html>
"""
