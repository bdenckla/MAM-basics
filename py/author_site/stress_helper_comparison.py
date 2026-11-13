"""Render the comparison with both printed editions from checked readings and crops."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re

from accgram import printed_decalogue_strands as accent_names
from mb_cmn import bib_locales, paths, provenance, site_links, uni_denorm
from mb_misc.osis_book_abbrevs import BOOK_ABBREVS

DIRECTORY = "stress-helpers"
_FNAME = "index.html"
HREF = f"{DIRECTORY}/{_FNAME}"
TITLE = "Stress helpers in MAM, Koren Classic Tanakh, and Feldheim Simanim Tanakh"
_EDITIONS = {
    "koren": ("Koren Classic Tanakh", "Koren", "Koren"),
    "simanim-tanakh": ("Feldheim Simanim Tanakh", "the Simanim Tanakh", "SimTan"),
}
CATEGORIES = {
    "no-helper": "no SH in {edition}",
    "gerstar-telg": "Geresh or gershayim + telisha gedolah",
    "redundant-mam": "redundant SH in MAM",
    "redundant-edition": "redundant SH in {edition}",
    "extra-helper": "SH in {edition} only",
    "different-placement": "Different SH placement",
    "different-accent": "Different accent",
}
DEFAULT_SIZE = 30
_ACCENT_NAME_RE = re.compile(
    r"(?<!\w)("
    + "|".join(
        map(
            re.escape,
            (
                accent_names.ROM_TELISHA_GEDOLAH,
                "telisha qetanna",
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
                "zarqa",
            ),
        )
    )
    + r")(?!\w)",
    re.IGNORECASE,
)


def _short_label(category, edition):
    return CATEGORIES[category].format(edition=edition)


def _romanize(text):
    return _ACCENT_NAME_RE.sub(r'<span class="romanized">\1</span>', escape(text))


def _marked_label(label):
    return _romanize(label).replace("SH", '<abbr title="stress helper">SH</abbr>')


def _linked_note(note):
    # The input carries authored prose and an optional source link.
    prose = _romanize(note["text"])
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


def _crop(item, edition, reference):
    src = escape(item, quote=True)
    alt = escape(f"{edition} scan crop for {reference}", quote=True)
    return (
        f'<a href="{src}"><img src="{src}" alt="{alt}" '
        'loading="lazy" decoding="async"></a>'
    )


def _row(record, edition_id):
    _, edition, reading_label = _EDITIONS[edition_id]
    reference = f'{BOOK_ABBREVS[record["book"]]} {record["chapter"]}:{record["verse"]}'
    verse_href = escape(record["verse_href"], quote=True)
    page = record["page"]
    scan = escape(record["scan"], quote=True)
    label = (
        f'<a href="{verse_href}">{escape(reference)}</a><br>'
        f'<span class="source" title="{scan}">p. {page}</span>'
    )
    if instance := record.get("instance"):
        label += f"<br><small>Instance {instance}</small>"
    if strand := record.get("strand"):
        label += f'<br><bdi lang="hbo">{escape(strand)}</bdi>'
    category = record["category"]
    name = _marked_label(_short_label(category, edition))
    notes = "".join(map(_linked_note, record.get("notes", ())))
    reading = _reading("MAM", record["mam"]) + _reading(
        reading_label, record["printed"]
    )
    crops = "".join(_crop(item, edition, reference) for item in record["crops"])
    return (
        f'<tr data-edition="{edition_id}" data-outcome="{category}">'
        f'<td class="readings" dir="rtl">{reading}</td>'
        f'<th scope="row">{label}</th>'
        f'<td class="difference"><strong>{name}</strong>{notes}</td>'
        f'<td class="scan" hidden>{crops}</td></tr>'
    )


def _verse_key(item):
    record, _ = item
    return bib_locales.get_bknu(record["book"]), record["chapter"], record["verse"]


def _document(common, inputs, generated_comment):
    records = [
        (record, edition_id)
        for edition_id, data in inputs.items()
        for record in data["differences"]
    ]
    outcomes = {record["category"] for record, _ in records}
    edition_choices = "".join(
        f'<option value="{key}">{escape(title)}</option>'
        for key, (title, _, _) in _EDITIONS.items()
    )
    outcome_choices = "".join(
        f'<option value="{key}">{escape(_short_label(key, "the printed edition"))}</option>'
        for key in CATEGORIES
        if key in outcomes
    )
    body = "\n".join(
        _row(record, key) for record, key in sorted(records, key=_verse_key)
    )
    coverage = "\n".join(
        f"<p>{_romanize(line)}</p>"
        for data in (common, *inputs.values())
        for line in data["coverage"]
    )
    source_notes = "\n".join(map(_linked_note, common["source_notes"]))
    credits = "\n".join(
        f'<p class="credit">{escape(data["edition_credit"])}</p>'
        for data in inputs.values()
    )
    mam_href = site_links.site_href(HREF, "MAM-with-doc/index.html")
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
{source_notes}
<div class="controls">
<div class="size-control">
<label for="hebrew-size">Hebrew size <output id="size-value" for="hebrew-size">{DEFAULT_SIZE} px</output></label>
<input id="hebrew-size" type="range" min="20" max="48" step="1" value="{DEFAULT_SIZE}">
<button id="size-reset" type="button">Reset</button>
</div>
<label>Search <input id="find" type="search" placeholder="Verse or Hebrew"></label>
<label>Edition <select id="edition"><option value="">Both editions</option>{edition_choices}</select></label>
<label>Outcome <select id="outcome" title="SH means stress helper"><option value="">All differences</option>{outcome_choices}</select></label>
<button id="toggle-images" type="button" aria-controls="observations" aria-expanded="false">Show images</button>
<output id="visible" aria-live="polite"></output>
</div>
<div class="comparison-table">
<table id="observations">
<thead><tr><th></th><th scope="col">Verse</th>
<th scope="col">Difference</th><th scope="col" class="scan" hidden>Scan crop</th></tr></thead>
<tbody>
{body}
</tbody>
</table>
</div>
{credits}
<p class="credit">The crops document the printed readings shown in the table.</p>
<p class="credit">MAM text from <a href="{mam_href}">MAM-with-doc</a>, based on
Miqra according to the Masorah at Hebrew Wikisource, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>
</main>
</body>
</html>
"""


def _check(data, output_dir):
    refs = set()
    for record in data["differences"]:
        key = (
            record["book"],
            record["chapter"],
            record["verse"],
            record.get("strand"),
            record.get("instance"),
            record["mam"],
            record["printed"],
        )
        if key in refs:
            raise ValueError(f"Duplicate comparison: {key}")
        refs.add(key)
        for field in ("mam", "printed"):
            value = record[field]
            if not value or not uni_denorm.has_std_mark_order(value):
                raise ValueError(f"Missing or out-of-order {field}: {key}")
        if record["category"] not in CATEGORIES:
            raise ValueError(f"Unknown comparison category: {record}")
        if not record["crops"]:
            raise ValueError(f"Comparison lacks image evidence: {key}")
        for item in record["crops"]:
            crop = Path(item)
            if len(crop.parts) != 2 or crop.parts[0] != "img":
                raise ValueError(f"Unexpected crop path: {item}")
            if not (output_dir / crop).is_file():
                raise FileNotFoundError(output_dir / crop)


def render(input_dir, output_dir, *, generated_comment):
    """Write the combined report, with crops already in output_dir."""
    common = json.loads((input_dir / "common.json").read_text(encoding="utf-8"))
    inputs = {
        key: json.loads((input_dir / f"{key}.json").read_text(encoding="utf-8"))
        for key in _EDITIONS
    }
    for data in inputs.values():
        _check(data, output_dir)
    target = output_dir / _FNAME
    page = _document(common, inputs, generated_comment)
    target.write_text(page, encoding="utf-8", newline="\n")
    return str(target)


def gen_html_file():
    root = paths.repo_root()
    return render(
        root / "in" / DIRECTORY,
        paths.gh_pages_dir() / DIRECTORY,
        generated_comment=provenance.generated_html_comment(__file__),
    )
