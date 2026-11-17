"""Render the comparison with both printed editions from checked readings and crops, and
the census's further results beside it.

index.html is the comparison, from in/stress-helpers/common.json, koren.json and
simanim-tanakh.json; each of its rows shows MAM's form above the printed edition's form,
the printed page and a scan crop.  results.html, from in/stress-helpers/results.json, has
the census of five accents and the findings that index.html does not show, in index.html's
row form.  Its rows have no printed form, page or crop: the census material records no
printed form for most of them (doc/PLAN-stress-helpers-results-rework.md, Stage 2), and the
crops wait for the rows' move into index.html, whose own records must have them.
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
_RESULTS_FNAME = "results.html"
_RESULTS_HREF = f"{DIRECTORY}/{_RESULTS_FNAME}"
# The page's <title> and <h1>, and its link text on the site's index.  Ben asked on
# 2026-11-14 for the title "Stress helpers in MAM, Koren Classic Tanakh, and Feldheim
# Simanim Tanakh" to be shortened to "Stress helpers in MAM, Koren, and Simanim".  His
# words govern this title's bare "Simanim", which the hebrew-prose skill's checklist
# item 7 otherwise avoids; other mentions of the two editions keep their own names.
TITLE = "Stress helpers in MAM, Koren, and Simanim"
# results.html's <title> and <h1>: Ben's Decision 5 of 2026-11-17, in
# doc/PLAN-stress-helpers-results-rework.md, says "further" so that a reader sees at once
# that the page supplements index.html.
RESULTS_TITLE = "Further stress-helper results in MAM, Koren, and the Simanim Tanakh"
_EDITIONS = {
    "koren": ("Koren", "Koren"),
    "simanim-tanakh": ("the Simanim Tanakh", "SimTan"),
}
# The census tables' column headings, which take no determiner.
_COLUMN_HEADINGS = {"koren": "Koren", "simanim-tanakh": "Simanim Tanakh"}
_FILTER_EDITIONS = {
    ("koren", "simanim-tanakh"): "KorSim",
    ("koren",): "Kor",
    ("simanim-tanakh",): "Sim",
}
# Each category has a row label and a filter label.  index.html has every category but
# different-grouping; results.html's differences have extra-helper, different-accent and
# different-grouping.
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
# results.html's collapsed table, outside the filter (Ben's Decision 4, 4A, of
# 2026-11-17): places where the spelling differs and the accent and helper agree.
SPELLING_CATEGORIES = {
    "different-spelling": ("Different spelling", "Different spelling — {edition}"),
}
# A record's strand key, for a Decalogue reading, and the strand's name in Hebrew letters,
# which keeps the surrounding font (the hebrew-prose skill's rendered-prose reference).
_STRANDS = {"taxton": accent_names.TAHTON, "elyon": accent_names.ELYON}
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
# The census's five accents, in the order of its table by accent.
_CENSUS_ACCENTS = (
    accent_names.ROM_PASHTA,
    accent_names.ROM_SEGOLTA,
    accent_names.ROM_TELISHA_GEDOLAH,
    _TELISHA_QETANNA,
    _ZARQA,
)
# The census's table by edition: the outcomes, which sum to each edition's readings, then
# the counts within the first outcome's agreements, each also a record category.
_OUTCOMES = (
    "same",
    "helper-in-print-only",
    "helper-in-mam-only",
    "helper-on-different-letter",
    "different-accent",
)
_WITHIN_AGREEMENT = ("different-grouping", "different-spelling")
_TRADITIONS = ("manuscript", "printed")
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


def _editions_phrase(edition_ids):
    phrase = " and ".join(_EDITIONS[key][0] for key in edition_ids)
    return phrase[0].upper() + phrase[1:]


def _notes(sources):
    """The row's notes.  A row with a printed form names its editions in its reading; a
    row without one names them before each note."""
    if all("printed" in source for source in sources.values()):
        return "".join(
            dict.fromkeys(
                _linked_note(note)
                for source in sources.values()
                for note in source.get("notes", ())
            )
        )
    editions_by_note = {}
    for key, source in sources.items():
        for note in source.get("notes", ()):
            identity = (note["text"], note.get("href"), note.get("label"))
            editions_by_note.setdefault(identity, (note, []))[1].append(key)
    return "".join(
        _linked_note({**note, "text": f"{_editions_phrase(keys)}: {note['text']}"})
        for note, keys in editions_by_note.values()
    )


def _row(sources, filter_value, categories, *, with_scans):
    record = next(iter(sources.values()))
    shared = len(sources) > 1
    edition_names = [_EDITIONS[key] for key in sources]
    reading_label = " / ".join(short for _, short in edition_names)
    edition = "both printed editions" if shared else edition_names[0][0]
    reference = f'{BOOK_ABBREVS[record["book"]]} {record["chapter"]}:{record["verse"]}'
    instance = record.get("instance")
    location = record.get("location")
    crop_reference = f"{reference}, {location.lower()}" if location else reference
    verse_href = escape(record["verse_href"], quote=True)
    label = f'<a href="{verse_href}">{escape(reference)}</a>'
    for key, source in sources.items():
        # The checks give every index.html record a page, and a results.html record
        # either a printed form, page and scan or none of them.
        if "page" not in source:
            continue
        _, short = _EDITIONS[key]
        scan = escape(source["scan"], quote=True)
        page_prefix = f"{short} " if shared else ""
        label += f'<br><span class="source" title="{scan}">{page_prefix}p. {source["page"]}</span>'
    if atom := record.get("atom"):
        label += f"<br><small>Atom {atom}</small>"
    if instance:
        label += f"<br><small>Instance {instance}</small>"
    if location:
        label += f"<br><small>{escape(location)}</small>"
    if strand := record.get("strand"):
        label += f"<br><bdi>{_STRANDS[strand]}</bdi>"
    row_label, _ = categories[record["category"]]
    name = _marked_label(row_label.format(edition=edition))
    reading = _reading("MAM", record["mam"])
    if "printed" in record:
        reading += _reading(reading_label, record["printed"])
    cells = (
        f'<tr data-filter="{filter_value}">'
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
        record.get("instance"),
        record.get("location"),
        record["mam"],
        record.get("printed"),
    )


def _rows(records_by_edition, categories, *, with_scans):
    """The table's rows, with an edition's record merged into another's row where the two
    match, and each row's filter value counted."""
    comparisons = {}
    for edition_id, records in records_by_edition.items():
        for record in records:
            key = (*_comparison_key(record), record["verse_href"], record["category"])
            comparisons.setdefault(key, {})[edition_id] = record
    counts = Counter()
    rows = []
    # By verse, then by atom where the records give one; otherwise in input order.
    for key in sorted(comparisons, key=lambda key: (*key[:3], key[3] or 0)):
        sources = comparisons[key]
        category = key[-1]
        edition = _FILTER_EDITIONS[tuple(sources)]
        filter_value = f"{category}-{edition}"
        counts[filter_value] += 1
        rows.append(_row(sources, filter_value, categories, with_scans=with_scans))
    return rows, counts


def _filter_choices(rows, counts):
    choices = [f'<option value="">All differences ({len(rows)})</option>']
    for category, (_, template) in CATEGORIES.items():
        for edition in _FILTER_EDITIONS.values():
            filter_value = f"{category}-{edition}"
            if count := counts[filter_value]:
                label = escape(template.format(edition=edition))
                choices.append(
                    f'<option value="{filter_value}">{label} ({count})</option>'
                )
    return "".join(choices)


def _controls(choices, filter_title, *, with_images):
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


def _document(common, inputs, generated_comment):
    rows, counts = _rows(
        {edition_id: data["differences"] for edition_id, data in inputs.items()},
        CATEGORIES,
        with_scans=True,
    )
    choices = _filter_choices(rows, counts)
    filter_title = (
        "SH means stress helper. Gerstar means geresh or gershayim."
        f" Tel. g. means {accent_names.ROM_TELISHA_GEDOLAH}."
    )
    body = "\n".join(rows)
    coverage = "\n".join(f"<p>{_prose(line)}</p>" for line in common["coverage"])
    source_notes = "\n".join(map(_linked_note, common["source_notes"]))
    credits = "\n".join(
        f'<p class="credit">{escape(data["edition_credit"])}</p>'
        for data in inputs.values()
    )
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
{_controls(choices, filter_title, with_images=True)}
<div class="comparison-table">
<table id="observations">
{_table_head(with_scans=True)}
<tbody>
{body}
</tbody>
</table>
</div>
{credits}
<p class="credit">The crops show the printed editions at the locations compared in the table.</p>
{_mam_credit(HREF)}
</main>
</body>
</html>
"""


def _count_cell(value):
    return f'<td class="count">{value:,}</td>'


def _census_table(label, caption, head, body):
    return f"""<div class="comparison-table" role="region" aria-label="{escape(label, quote=True)}" tabindex="0">
<table class="census">
<caption>{_prose(caption)}</caption>
<thead><tr>{head}</tr></thead>
<tbody>
{body}
</tbody>
</table>
</div>"""


def _census(census):
    by_accent = census["by_accent"]
    head = (
        '<th scope="col">Target accent</th><th scope="col">With helper</th>'
        '<th scope="col">Without helper</th><th scope="col">Total</th>'
    )
    columns = ("with_helper", "without_helper", "total")
    body = [
        f'<tr><th scope="row">{_romanize(row["accent"])}</th>'
        + "".join(_count_cell(row[column]) for column in columns)
        + "</tr>"
        for row in by_accent["rows"]
    ]
    body.append(
        '<tr><th scope="row">Total</th>'
        + "".join(_count_cell(by_accent["total"][column]) for column in columns)
        + "</tr>"
    )
    accent_table = _census_table(
        "Readings by accent", by_accent["caption"], head, "\n".join(body)
    )
    by_edition = census["by_edition"]
    head = '<th scope="col">Result</th>' + "".join(
        f'<th scope="col">{_COLUMN_HEADINGS[key]}</th>' for key in _EDITIONS
    )

    def row(label, counts):
        cells = "".join(_count_cell(counts[key]) for key in _EDITIONS)
        return f'<tr><th scope="row">{_prose(label)}</th>{cells}</tr>'

    body = [row(item["label"], item["counts"]) for item in by_edition["outcomes"]]
    body.append(row("Total", by_edition["total"]))
    body.extend(
        row(item["label"], item["counts"]) for item in by_edition["within_agreement"]
    )
    edition_table = _census_table(
        "Results by edition", by_edition["caption"], head, "\n".join(body)
    )
    return f"{accent_table}\n{edition_table}"


def _results_document(results, generated_comment):
    editions = results["editions"]
    rows, counts = _rows(
        {edition_id: data["differences"] for edition_id, data in editions.items()},
        CATEGORIES,
        with_scans=False,
    )
    spelling_rows, _ = _rows(
        {edition_id: data["spelling"] for edition_id, data in editions.items()},
        SPELLING_CATEGORIES,
        with_scans=False,
    )
    choices = _filter_choices(rows, counts)
    intro = "\n".join(map(_linked_note, results["intro"]))
    findings = "\n".join(map(_linked_note, results["findings"]))
    spelling = results["spelling"]
    spelling_intro = "\n".join(map(_linked_note, spelling["intro"]))
    body = "\n".join(rows)
    spelling_body = "\n".join(spelling_rows)
    return f"""<!doctype html>
<!-- {escape(generated_comment)} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{RESULTS_TITLE}</title>
<link rel="stylesheet" href="../document.css">
<link rel="stylesheet" href="../wlc/style.css">
<link rel="stylesheet" href="style.css">
<script src="controls.js" defer></script>
</head>
<body>
<main>
<h1>{RESULTS_TITLE}</h1>
{intro}
{_census(results["census"])}
{findings}
{_controls(choices, "SH means stress helper.", with_images=False)}
<div class="comparison-table">
<table id="observations">
{_table_head(with_scans=False)}
<tbody>
{body}
</tbody>
</table>
</div>
<details>
<summary>{_prose(spelling["summary"])}</summary>
{spelling_intro}
<div class="comparison-table">
<table id="spelling">
{_table_head(with_scans=False)}
<tbody>
{spelling_body}
</tbody>
</table>
</div>
</details>
{_mam_credit(_RESULTS_HREF)}
</main>
</body>
</html>
"""


def _check_record(record, categories, key):
    if record["category"] not in categories:
        raise ValueError(f"Unknown comparison category: {record}")
    if not record["mam"] or not uni_denorm.has_std_mark_order(record["mam"]):
        raise ValueError(f"Missing or out-of-order mam: {key}")
    if "strand" in record and record["strand"] not in _STRANDS:
        raise ValueError(f"Unknown strand: {key}")
    if "atom" in record and not (
        isinstance(record["atom"], int) and record["atom"] > 0
    ):
        raise ValueError(f"Invalid atom: {key}")


def _check(data, output_dir):
    refs = set()
    for record in data["differences"]:
        key = _comparison_key(record)
        if key in refs:
            raise ValueError(f"Duplicate comparison: {key}")
        refs.add(key)
        _check_record(record, CATEGORIES, key)
        printed = record["printed"]
        if not printed or not uni_denorm.has_std_mark_order(printed):
            raise ValueError(f"Missing or out-of-order printed: {key}")
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


def _check_results(results, inputs):
    """Check results.json's records and census tables, and that results.html repeats
    nothing that index.html shows."""
    editions = results["editions"]
    if list(editions) != list(_EDITIONS):
        raise ValueError(f"Unexpected editions in results: {list(editions)}")
    shown = {
        edition_id: {
            (r["book"], r["chapter"], r["verse"], r["mam"]) for r in data["differences"]
        }
        for edition_id, data in inputs.items()
    }
    by_category = {edition_id: Counter() for edition_id in _EDITIONS}
    for edition_id, data in editions.items():
        if set(data) != {"differences", "spelling"}:
            raise ValueError(f"Unexpected tables for {edition_id}: {sorted(data)}")
        for table, categories in (
            ("differences", CATEGORIES),
            ("spelling", SPELLING_CATEGORIES),
        ):
            refs = set()
            for record in data[table]:
                key = _comparison_key(record)
                if key in refs:
                    raise ValueError(f"Duplicate result: {key}")
                refs.add(key)
                _check_record(record, categories, key)
                if not record.get("atom") or not record.get("notes"):
                    raise ValueError(f"Result lacks its atom or notes: {key}")
                if "crops" in record:
                    raise ValueError(f"Result has crops before its move: {key}")
                optional = {"printed", "page", "scan"} & set(record)
                if optional and optional != {"printed", "page", "scan"}:
                    raise ValueError(
                        f"Result has only some of {sorted(optional)}: {key}"
                    )
                if optional and not uni_denorm.has_std_mark_order(record["printed"]):
                    raise ValueError(f"Out-of-order printed: {key}")
                identity = (record["book"], record["chapter"], record["verse"])
                if (*identity, record["mam"]) in shown[edition_id]:
                    raise ValueError(f"Result repeats index.html: {edition_id} {key}")
                by_category[edition_id][record["category"]] += 1
    _check_census(results["census"], by_category)


def _check_census(census, by_category):
    by_accent = census["by_accent"]
    if tuple(row["accent"] for row in by_accent["rows"]) != _CENSUS_ACCENTS:
        raise ValueError("Unexpected accents in the census table by accent")
    columns = ("with_helper", "without_helper", "total")
    for row in by_accent["rows"]:
        if row["with_helper"] + row["without_helper"] != row["total"]:
            raise ValueError(f"Census row does not sum to its total: {row}")
    for column in columns:
        if sum(row[column] for row in by_accent["rows"]) != by_accent["total"][column]:
            raise ValueError(f"Census column {column} does not sum to its total")
    by_edition = census["by_edition"]
    outcomes = by_edition["outcomes"]
    within = by_edition["within_agreement"]
    if tuple(item["id"] for item in outcomes) != _OUTCOMES:
        raise ValueError("Unexpected outcomes in the census table by edition")
    if tuple(item["id"] for item in within) != _WITHIN_AGREEMENT:
        raise ValueError("Unexpected counts within the agreements")
    readings = census["decalogue_readings"]
    traditions = census["decalogue_tradition"]
    if (
        set(readings) != set(_TRADITIONS)
        or list(traditions) != list(_EDITIONS)
        or not set(traditions.values()) <= set(_TRADITIONS)
    ):
        raise ValueError("Unexpected Decalogue traditions in the census")
    for edition_id in _EDITIONS:
        total = by_edition["total"][edition_id]
        if sum(item["counts"][edition_id] for item in outcomes) != total:
            raise ValueError(f"Census outcomes do not sum to the total: {edition_id}")
        # Each edition is compared with the Decalogues of the tradition it follows, in
        # place of the manuscript tradition's that the table by accent counts.
        expected = (
            by_accent["total"]["total"]
            - readings["manuscript"]
            + readings[traditions[edition_id]]
        )
        if total != expected:
            raise ValueError(f"Census total does not fit its Decalogues: {edition_id}")
        for item in within:
            count = item["counts"][edition_id]
            if count > outcomes[0]["counts"][edition_id]:
                raise ValueError(f"More {item['id']} than agreements: {edition_id}")
            if count != by_category[edition_id][item["id"]]:
                raise ValueError(f"Census {item['id']} is not its rows: {edition_id}")


def render(input_dir, output_dir, *, generated_comment):
    """Write the combined report, with crops already in output_dir, and the census's
    further results."""
    common = json.loads((input_dir / "common.json").read_text(encoding="utf-8"))
    inputs = {
        key: json.loads((input_dir / f"{key}.json").read_text(encoding="utf-8"))
        for key in _EDITIONS
    }
    for data in inputs.values():
        _check(data, output_dir)
    results = json.loads((input_dir / "results.json").read_text(encoding="utf-8"))
    _check_results(results, inputs)
    written = []
    for fname, page in (
        (_FNAME, _document(common, inputs, generated_comment)),
        (_RESULTS_FNAME, _results_document(results, generated_comment)),
    ):
        target = output_dir / fname
        target.write_text(page, encoding="utf-8", newline="\n")
        written.append(str(target))
    return written


def gen_html_files():
    root = paths.repo_root()
    return render(
        root / "in" / DIRECTORY,
        paths.gh_pages_dir() / DIRECTORY,
        generated_comment=provenance.generated_html_comment(__file__),
    )
