"""Render the comparison with both printed editions from checked readings and crops."""

from __future__ import annotations

from collections import Counter
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


def _crop(item, edition, reference, label):
    src = escape(item, quote=True)
    alt = escape(f"{edition} scan crop for {reference}", quote=True)
    return (
        f'<a href="{src}">{label}<img src="{src}" alt="{alt}" '
        'loading="lazy" decoding="async"></a>'
    )


def _row(sources, filter_value):
    record = next(iter(sources.values()))
    shared = len(sources) > 1
    edition_names = [_EDITIONS[key] for key in sources]
    reading_label = " / ".join(short for _, short in edition_names)
    edition = "both printed editions" if shared else edition_names[0][0]
    reference = f'{BOOK_ABBREVS[record["book"]]} {record["chapter"]}:{record["verse"]}'
    verse_href = escape(record["verse_href"], quote=True)
    label = f'<a href="{verse_href}">{escape(reference)}</a>'
    crops = []
    for key, source in sources.items():
        edition_name, short = _EDITIONS[key]
        scan = escape(source["scan"], quote=True)
        page_prefix = f"{short} " if shared else ""
        label += f'<br><span class="source" title="{scan}">{page_prefix}p. {source["page"]}</span>'
        crop_label = f'<span class="source">{short}</span><br>' if shared else ""
        crops.extend(
            _crop(item, edition_name, reference, crop_label) for item in source["crops"]
        )
    if instance := record.get("instance"):
        label += f"<br><small>Instance {instance}</small>"
    if strand := record.get("strand"):
        label += f'<br><bdi lang="hbo">{escape(strand)}</bdi>'
    row_label, _ = CATEGORIES[record["category"]]
    name = _marked_label(row_label.format(edition=edition))
    notes = "".join(
        dict.fromkeys(
            _linked_note(note)
            for source in sources.values()
            for note in source.get("notes", ())
        )
    )
    reading = _reading("MAM", record["mam"]) + _reading(
        reading_label, record["printed"]
    )
    return (
        f'<tr data-filter="{filter_value}">'
        f'<td class="readings" dir="rtl">{reading}</td>'
        f'<th scope="row">{label}</th>'
        f'<td class="difference"><strong>{name}</strong>{notes}</td>'
        f'<td class="scan" hidden>{"".join(crops)}</td></tr>'
    )


def _comparison_key(record):
    return (
        bib_locales.get_bknu(record["book"]),
        record["chapter"],
        record["verse"],
        record.get("strand"),
        record.get("instance"),
        record["mam"],
        record["printed"],
    )


def _document(common, inputs, generated_comment):
    comparisons = {}
    for edition_id, data in inputs.items():
        for record in data["differences"]:
            key = (*_comparison_key(record), record["verse_href"], record["category"])
            comparisons.setdefault(key, {})[edition_id] = record
    counts = Counter()
    rows = []
    for key in sorted(comparisons, key=lambda key: key[:3]):
        sources = comparisons[key]
        category = key[-1]
        edition = _FILTER_EDITIONS[tuple(sources)]
        filter_value = f"{category}-{edition}"
        counts[filter_value] += 1
        rows.append(_row(sources, filter_value))
    choices = [f'<option value="">All differences ({len(rows)})</option>']
    for category, (_, template) in CATEGORIES.items():
        for edition in _FILTER_EDITIONS.values():
            filter_value = f"{category}-{edition}"
            if count := counts[filter_value]:
                label = escape(template.format(edition=edition))
                choices.append(
                    f'<option value="{filter_value}">{label} ({count})</option>'
                )
    body = "\n".join(rows)
    coverage = "\n".join(f"<p>{_romanize(line)}</p>" for line in common["coverage"])
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
<label>Filter <select id="filter" title="SH means stress helper. Gerstar means geresh or gershayim. Tel. g. means {accent_names.ROM_TELISHA_GEDOLAH}.">{"".join(choices)}</select></label>
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
        key = _comparison_key(record)
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
