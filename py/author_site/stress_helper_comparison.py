"""Render the comparison with both printed editions from checked forms and crops.

index.html is the comparison, from in/stress-helpers/common.json, koren.json and
simanim-tanakh.json; each of its rows shows MAM's form above the printed edition's form,
the printed page and a scan crop.  Each record names its batch: batch 1 is the original
set of comparisons, and batch 2 has the differences that a census of five accents found
beyond batch 1.  Rows of different batches never merge, and the page's Batch control
shows either batch or both.  Every record must have the printed word, page, scan and
crops.
"""

from __future__ import annotations

from collections import Counter
from html import escape
from itertools import chain
import json
from pathlib import Path
import re

from accgram import printed_decalogue_strands as accent_names
from mb_author import author
from mb_cmn import bib_locales, paths, provenance, site_links, uni_denorm
from mb_misc.osis_book_abbrevs import BOOK_ABBREVS

DIRECTORY = "stress-helpers"
_FNAME = "index.html"
HREF = f"{DIRECTORY}/{_FNAME}"
# The page's <title> and <h1>, and its link text on the site's index.  Ben asked on
# 2026-11-14 for the title "Stress helpers in MAM, Koren Classic Tanakh, and Feldheim
# Simanim Tanakh" to be shortened to "Stress helpers in MAM, Koren, and Simanim".  His
# words govern this title's bare "Simanim", which the hebrew-prose skill's checklist
# item 7 otherwise avoids; other mentions of the two editions keep their own names.
TITLE = "Stress helpers in MAM, Koren, and Simanim"
_EDITIONS = {
    "koren": ("Koren", "Koren"),
    "simanim-tanakh": ("the Simanim Tanakh", "SimTan"),
}
_FILTER_EDITIONS = {
    ("koren", "simanim-tanakh"): "KorSim",
    ("koren",): "Kor",
    ("simanim-tanakh",): "Sim",
}
# Each category has a row label and a filter label.
CATEGORIES = {
    "no-helper": ("no SH in {edition}", "No SH in {edition}"),
    "gerstar-telg": (
        "Geresh or gershayim + telisha gedolah",
        "Gerstar + tel. g. — {edition}",
    ),
    "redundant-mam": ("redundant SH in MAM", "Redundant SH in MAM — {edition}"),
    "redundant-edition": ("redundant SH in {edition}", "Redundant SH in {edition}"),
    "extra-helper": ("SH in {edition} only", "SH in {edition} only"),
    "different-placement": (
        "Different SH placement",
        "Different SH placement — {edition}",
    ),
    "different-accent": ("Different accent", "Different accent — {edition}"),
    "different-grouping": ("Different grouping", "Different grouping — {edition}"),
}
# A record's batch and the batch's label in the Batch control.  Ben, 2026-11-18, when
# results.html was merged into this page: "add another filter control, with options
# batch 1, batch 2, all batches. where batch 1 is pre-merge index.html and batch 2 is
# pre-merge results.html. Default all batches."
_BATCHES = {1: "Batch 1", 2: "Batch 2"}
# A record's strand key, for a word of the Decalogues, and the strand's name in Hebrew
# letters, which keeps the surrounding font (the hebrew-prose skill's rendered-prose
# reference).
_STRANDS = {"taxton": accent_names.TAHTON, "elyon": accent_names.ELYON}
# A record's page section, for a page outside an edition's main text, and the words that
# name it before the page number.  Koren's appendix Decalogues are on pages numbered apart
# from its main text.
_PAGE_SECTIONS = {"appendix": "appendix "}
DEFAULT_SIZE = 30
_TELISHA_QETANNA = "telisha qetanna"
_ZARQA = "zarqa"
_ACCENT_NAME_RE = re.compile(
    r"(?<!\w)("
    + "|".join(
        map(
            re.escape,
            (
                accent_names.ROM_TELISHA_GEDOLAH,
                _TELISHA_QETANNA,
                accent_names.ROM_GERSHAYIM,
                accent_names.ROM_GERESH,
                accent_names.ROM_QADMA,
                accent_names.ROM_TEVIR,
                accent_names.ROM_SEGOLTA,
                accent_names.ROM_REVIA,
                accent_names.ROM_METEG,
                accent_names.ROM_PASHTA,
                accent_names.ROM_MERKHA,
                accent_names.ROM_MAHAPAKH,
                "yetiv",
                accent_names.ROM_MUNAX,
                _ZARQA,
                accent_names.ROM_TIPEHA,
                accent_names.ROM_ZAQEF_QATAN,
                accent_names.ROM_MAQAF,
            ),
        )
    )
    + r")(?!\w)",
    re.IGNORECASE,
)
# A run of Hebrew -- letters, points, accents, maqaf, sof pasuq, and the CGJ that MAM puts
# between an accent and a meteg -- with the spaces between its words, as accgram's
# wrap_hebrew_runs takes one.
_HEBREW = (
    "\N{COMBINING GRAPHEME JOINER}"
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW PUNCTUATION GERSHAYIM}"
)
_HEBREW_RUN_RE = re.compile(f"[{_HEBREW}]+(?: +[{_HEBREW}]+)*")


def _romanize(text):
    return _ACCENT_NAME_RE.sub(r'<span class="romanized">\1</span>', escape(text))


def _prose(text):
    """Prose with its romanized names italic and its Hebrew isolated for direction:
    pointed Hebrew in the pointed-Hebrew font, and unpointed Hebrew, such as a strand's
    name, in the surrounding font (the hebrew-prose skill's rendered-prose reference,
    "Unpointed Hebrew keeps the surrounding font")."""
    pieces = []
    cursor = 0
    for match in _HEBREW_RUN_RE.finditer(text):
        run = match.group(0)
        lang = "" if author.is_unpointed_hebrew(run) else ' lang="hbo"'
        pieces.append(_romanize(text[cursor : match.start()]))
        pieces.append(f"<bdi{lang}>{escape(run)}</bdi>")
        cursor = match.end()
    pieces.append(_romanize(text[cursor:]))
    return "".join(pieces)


def _marked_label(label):
    return _romanize(label).replace("SH", '<abbr title="stress helper">SH</abbr>')


def _linked_note(note):
    # The input carries authored prose and an optional source link.
    prose = _prose(note["text"])
    href = note.get("href")
    if href:
        href = escape(href, quote=True)
        source = escape(note.get("label", "MAM doc-note"))
        prose += f' <a href="{href}">{source}</a>'
    return f"<p>{prose}</p>"


def _reading(edition, word):
    return (
        f'<div class="reading"><span class="edition" dir="ltr">{escape(edition)}</span>'
        f'<span class="hebrew" dir="rtl" lang="hbo">{escape(word)}</span></div>'
    )


def _crop(item, edition_id, reference, labeled):
    edition, short = _EDITIONS[edition_id]
    src = escape(item, quote=True)
    alt = escape(f"{edition} scan crop for {reference}", quote=True)
    label = f'<span class="source">{short}</span><br>' if labeled else ""
    return (
        f'<a href="{src}">{label}<img src="{src}" alt="{alt}" '
        'loading="lazy" decoding="async"></a>'
    )


def _notes(sources):
    """The row's notes, each once.  The row names its editions beside their printed word,
    so a note that the editions share needs no names before it."""
    return "".join(
        dict.fromkeys(
            _linked_note(note)
            for source in sources.values()
            for note in source.get("notes", ())
        )
    )


def _row(sources, filter_value, *, with_scans):
    record = next(iter(sources.values()))
    shared = len(sources) > 1
    edition_names = [_EDITIONS[key] for key in sources]
    reading_label = " / ".join(short for _, short in edition_names)
    edition = "both printed editions" if shared else edition_names[0][0]
    reference = f'{BOOK_ABBREVS[record["book"]]} {record["chapter"]}:{record["verse"]}'
    location = record.get("location")
    crop_reference = f"{reference}, {location.lower()}" if location else reference
    verse_href = escape(record["verse_href"], quote=True)
    label = f'<a href="{verse_href}">{escape(reference)}</a>'
    for key, source in sources.items():
        _, short = _EDITIONS[key]
        scan = escape(source["scan"], quote=True)
        page_prefix = f"{short} " if shared else ""
        if section := source.get("page_section"):
            page_prefix += _PAGE_SECTIONS[section]
        label += f'<br><span class="source" title="{scan}">{page_prefix}p. {source["page"]}</span>'
    if location:
        label += f"<br><small>{escape(location)}</small>"
    if strand := record.get("strand"):
        label += f"<br><bdi>{_STRANDS[strand]}</bdi>"
    row_label, _ = CATEGORIES[record["category"]]
    name = _marked_label(row_label.format(edition=edition))
    reading = _reading("MAM", record["mam"])
    reading += _reading(reading_label, record["printed"])
    cells = (
        f'<tr data-filter="{filter_value}" data-batch="{record["batch"]}">'
        f'<td class="readings" dir="rtl">{reading}</td>'
        f'<th scope="row">{label}</th>'
        f'<td class="difference"><strong>{name}</strong>{_notes(sources)}</td>'
    )
    if not with_scans:
        return cells + "</tr>"
    crops_by_edition = {key: list(source["crops"]) for key, source in sources.items()}
    for source in sources.values():
        for edition_id, items in source.get("comparison_crops", {}).items():
            crops_by_edition.setdefault(edition_id, []).extend(items)
    crops = "".join(
        _crop(item, edition_id, crop_reference, len(crops_by_edition) > 1)
        for edition_id in _EDITIONS
        for item in crops_by_edition.get(edition_id, ())
    )
    return cells + f'<td class="scan" hidden>{crops}</td></tr>'


def _comparison_key(record):
    return (
        bib_locales.get_bknu(record["book"]),
        record["chapter"],
        record["verse"],
        record.get("atom"),
        record.get("strand"),
        record.get("location"),
        record["mam"],
        record.get("printed"),
    )


def _rows(records_by_edition, *, with_scans):
    """The table's rows, with an edition's record merged into another's row where the two
    match in the same batch, and each row's filter value and batch counted."""
    comparisons = {}
    for edition_id, records in records_by_edition.items():
        for record in records:
            key = (
                *_comparison_key(record),
                record["verse_href"],
                record["category"],
                record["batch"],
            )
            comparisons.setdefault(key, {})[edition_id] = record
    counts = Counter()
    batch_counts = Counter()
    rows = []
    # By verse, then by atom where the records give one; otherwise in input order.
    for key in sorted(comparisons, key=lambda key: (*key[:3], key[3] or 0)):
        sources = comparisons[key]
        *_, category, batch = key
        edition = _FILTER_EDITIONS[tuple(sources)]
        filter_value = f"{category}-{edition}"
        counts[filter_value] += 1
        batch_counts[batch] += 1
        rows.append(_row(sources, filter_value, with_scans=with_scans))
    return rows, counts, batch_counts


def _option(value, label, count):
    """A menu choice showing its count of rows, with its label also kept apart from the
    count.  controls.js recounts each menu's choices for the other menu's choice, as Ben
    chose on 2026-11-18 (his answer "2A"), and writes each label anew from data-label.
    """
    label = escape(label)
    return f'<option value="{value}" data-label="{label}">{label} ({count})</option>'


def _filter_choices(rows, counts):
    choices = [_option("", "All differences", len(rows))]
    for category, (_, template) in CATEGORIES.items():
        for edition in _FILTER_EDITIONS.values():
            filter_value = f"{category}-{edition}"
            if count := counts[filter_value]:
                label = template.format(edition=edition)
                choices.append(_option(filter_value, label, count))
    return "".join(choices)


def _batch_choices(rows, batch_counts):
    choices = [_option("", "All batches", len(rows))]
    for batch, label in _BATCHES.items():
        choices.append(_option(batch, label, batch_counts[batch]))
    return "".join(choices)


def _controls(choices, batch_choices, filter_title, *, with_images):
    images = (
        '<button id="toggle-images" type="button" aria-controls="observations"'
        ' aria-expanded="false">Show images</button>\n'
        if with_images
        else ""
    )
    return f"""<div class="controls">
<div class="size-control">
<label for="hebrew-size">Hebrew size <output id="size-value" for="hebrew-size">{DEFAULT_SIZE} px</output></label>
<input id="hebrew-size" type="range" min="20" max="48" step="1" value="{DEFAULT_SIZE}">
<button id="size-reset" type="button">Reset</button>
</div>
<label>Search <input id="find" type="search" placeholder="Verse or Hebrew"></label>
<label>Filter <select id="filter" title="{filter_title}">{choices}</select></label>
<label>Batch <select id="batch">{batch_choices}</select></label>
{images}<output id="visible" aria-live="polite"></output>
</div>"""


def _table_head(*, with_scans):
    scan = '<th scope="col" class="scan" hidden>Scan crop</th>' if with_scans else ""
    return (
        '<thead><tr><th></th><th scope="col">Verse</th>\n'
        f'<th scope="col">Difference</th>{scan}</tr></thead>'
    )


def _mam_credit(page):
    mam_href = site_links.site_href(page, "MAM-with-doc/index.html")
    return f"""<p class="credit">MAM text from <a href="{mam_href}">MAM-with-doc</a>, based on
Miqra according to the Masorah at Hebrew Wikisource, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>"""


def _credits(inputs, page):
    """The page's credits: each printed edition's, the crops', and MAM's."""
    editions = "\n".join(
        f'<p class="credit">{escape(data["edition_credit"])}</p>'
        for data in inputs.values()
    )
    return f"""{editions}
<p class="credit">The crops show the printed editions at the locations compared in the table.</p>
{_mam_credit(page)}"""


def _document(common, inputs, generated_comment):
    rows, counts, batch_counts = _rows(
        {edition_id: data["differences"] for edition_id, data in inputs.items()},
        with_scans=True,
    )
    choices = _filter_choices(rows, counts)
    batch_choices = _batch_choices(rows, batch_counts)
    filter_title = (
        "SH means stress helper. Gerstar means geresh or gershayim."
        f" Tel. g. means {accent_names.ROM_TELISHA_GEDOLAH}."
    )
    body = "\n".join(rows)
    coverage = "\n".join(f"<p>{_prose(line)}</p>" for line in common["coverage"])
    return f"""<!doctype html>
<!-- {escape(generated_comment)} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<link rel="stylesheet" href="../document.css">
<link rel="stylesheet" href="../wlc/style.css">
<link rel="stylesheet" href="style.css">
<script src="controls.js" defer></script>
</head>
<body>
<main>
<h1>{TITLE}</h1>
{coverage}
{_controls(choices, batch_choices, filter_title, with_images=True)}
<div class="comparison-table">
<table id="observations">
{_table_head(with_scans=True)}
<tbody>
{body}
</tbody>
</table>
</div>
{_credits(inputs, HREF)}
</main>
</body>
</html>
"""


def _check_record(record, key):
    if record["category"] not in CATEGORIES:
        raise ValueError(f"Unknown comparison category: {record}")
    if record.get("batch") not in _BATCHES:
        raise ValueError(f"Missing or unknown batch: {key}")
    if not record["mam"] or not uni_denorm.has_std_mark_order(record["mam"]):
        raise ValueError(f"Missing or out-of-order mam: {key}")
    if "strand" in record and record["strand"] not in _STRANDS:
        raise ValueError(f"Unknown strand: {key}")
    if "atom" in record and not (
        isinstance(record["atom"], int) and record["atom"] > 0
    ):
        raise ValueError(f"Invalid atom: {key}")


def _check_evidence(record, key, output_dir):
    """Check the printed word, page, scan and crops that every row shows."""
    printed = record["printed"]
    if not printed or not uni_denorm.has_std_mark_order(printed):
        raise ValueError(f"Missing or out-of-order printed: {key}")
    if not (isinstance(record["page"], int) and record["page"] > 0):
        raise ValueError(f"Invalid page: {key}")
    if not (isinstance(record["scan"], str) and record["scan"]):
        raise ValueError(f"Invalid scan: {key}")
    if "page_section" in record and record["page_section"] not in _PAGE_SECTIONS:
        raise ValueError(f"Unknown page section: {key}")
    if not record["crops"]:
        raise ValueError(f"Comparison lacks image evidence: {key}")
    comparison_crops = record.get("comparison_crops", {})
    for edition_id, items in comparison_crops.items():
        if edition_id not in _EDITIONS or not items:
            raise ValueError(f"Invalid comparison crops for {edition_id}: {key}")
    for item in chain(record["crops"], *comparison_crops.values()):
        crop = Path(item)
        if len(crop.parts) != 2 or crop.parts[0] != "img":
            raise ValueError(f"Unexpected crop path: {item}")
        if not (output_dir / crop).is_file():
            raise FileNotFoundError(output_dir / crop)


def _check(edition_id, data, output_dir):
    """Check an edition's records: every batch-2 record has notes, and none repeats a
    batch-1 record's verse and MAM form."""
    refs = set()
    for record in data["differences"]:
        key = _comparison_key(record)
        if key in refs:
            raise ValueError(f"Duplicate comparison: {key}")
        refs.add(key)
        _check_record(record, key)
        _check_evidence(record, key, output_dir)
        if record["batch"] == 2 and not record.get("notes"):
            raise ValueError(f"Batch-2 record lacks notes: {edition_id} {key}")
    batch_1 = {
        (r["book"], r["chapter"], r["verse"], r["mam"])
        for r in data["differences"]
        if r["batch"] == 1
    }
    for record in data["differences"]:
        identity = (record["book"], record["chapter"], record["verse"], record["mam"])
        if record["batch"] == 2 and identity in batch_1:
            raise ValueError(f"Batch 2 repeats batch 1: {edition_id} {identity}")


def render(input_dir, output_dir, *, generated_comment):
    """Write the combined report, with crops already in output_dir."""
    common = json.loads((input_dir / "common.json").read_text(encoding="utf-8"))
    inputs = {
        key: json.loads((input_dir / f"{key}.json").read_text(encoding="utf-8"))
        for key in _EDITIONS
    }
    for edition_id, data in inputs.items():
        _check(edition_id, data, output_dir)
    target = output_dir / _FNAME
    page = _document(common, inputs, generated_comment)
    target.write_text(page, encoding="utf-8", newline="\n")
    return [str(target)]


def gen_html_files():
    root = paths.repo_root()
    return render(
        root / "in" / DIRECTORY,
        paths.gh_pages_dir() / DIRECTORY,
        generated_comment=provenance.generated_html_comment(__file__),
    )
