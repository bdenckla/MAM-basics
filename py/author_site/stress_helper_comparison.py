"""Render the two printed-edition comparisons from checked readings and crops."""

from __future__ import annotations

from collections import Counter
from html import escape
import json
from pathlib import Path
import re

from accgram import printed_decalogue_strands as accent_names
from mb_cmn import paths, provenance, uni_denorm
from mb_misc.osis_book_abbrevs import BOOK_ABBREVS

DIRECTORY = "stress-helpers"
EDITIONS = {
    "koren": ("Koren", "Stress helpers in MAM and Koren Classic Tanakh"),
    "simanim-tanakh": (
        "the Simanim Tanakh",
        "Stress helpers in MAM and Feldheim Simanim Tanakh",
    ),
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


def _row(record, edition, reading_label):
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
        f'<tr data-outcome="{category}"><td class="readings" dir="rtl">{reading}</td>'
        f'<th scope="row">{label}</th>'
        f'<td class="difference"><strong>{name}</strong>{notes}</td>'
        f'<td class="scan" hidden>{crops}</td></tr>'
    )


def _document(data, edition_id, generated_comment):
    short_name, title = EDITIONS[edition_id]
    other = next(key for key in EDITIONS if key != edition_id)
    other_title = EDITIONS[other][1]
    records = data["differences"]
    outcomes = Counter(row["category"] for row in records)
    choices = "".join(
        f'<option value="{key}">{escape(_short_label(key, short_name))}</option>'
        for key in CATEGORIES
        if key in outcomes
    )
    reading_label = "SimTan" if edition_id == "simanim-tanakh" else short_name
    body = "\n".join(_row(record, short_name, reading_label) for record in records)
    coverage = "".join(f"<p>{_romanize(line)}</p>" for line in data["coverage"])
    source_notes = "".join(map(_linked_note, data.get("source_notes", ())))
    attribution = escape(data["edition_credit"])
    return f"""<!doctype html>
<!-- {escape(generated_comment)} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../document.css">
<link rel="stylesheet" href="../wlc/style.css">
<link rel="stylesheet" href="style.css">
<script src="controls.js" defer></script>
</head>
<body>
<main>
<h1>{title}</h1>
<p><a href="{other}.html">{other_title}</a></p>
{coverage}
{source_notes}
<div class="controls">
<div class="size-control">
<label for="hebrew-size">Hebrew size <output id="size-value" for="hebrew-size">{DEFAULT_SIZE} px</output></label>
<input id="hebrew-size" type="range" min="20" max="48" step="1" value="{DEFAULT_SIZE}">
<button id="size-reset" type="button">Reset</button>
</div>
<label>Search <input id="find" type="search" placeholder="Verse or Hebrew"></label>
<label>Outcome <select id="outcome" title="SH means stress helper"><option value="">All differences</option>{choices}</select></label>
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
<p class="credit">{attribution} The crops document the printed readings shown in the table.</p>
<p class="credit">MAM text from <a href="../MAM-with-doc/index.html">MAM-with-doc</a>, based on
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
    """Render a complete report pair, with all assets already in output_dir."""
    inputs = {
        key: json.loads((input_dir / f"{key}.json").read_text(encoding="utf-8"))
        for key in EDITIONS
    }
    for data in inputs.values():
        _check(data, output_dir)
    written = []
    for key, data in inputs.items():
        target = output_dir / f"{key}.html"
        page = _document(data, key, generated_comment)
        target.write_text(page, encoding="utf-8", newline="\n")
        written.append(str(target))
    return tuple(written)


def gen_html_files():
    root = paths.repo_root()
    return render(
        root / "in" / DIRECTORY,
        paths.gh_pages_dir() / DIRECTORY,
        generated_comment=provenance.generated_html_comment(__file__),
    )
