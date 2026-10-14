"""Characteristic spacing examples from NAEE's selected Scripture readings.

The shared renderer chooses template fields. This consumer then keeps body text,
ketiv and qere in separate streams, excluding ruby fallback text and editorial
placeholders. Notes are removed before HTML conversion. Examples resolve from
current source by consonants and must still match the stated screening family.
Atoms crossing special-letter or vowel-variant formatting are excluded so that
the isolated comparison retains the edition's glyph appearance. Family counts
use this same projection across every book, counting full pointed words and
their occurrences independently for each overlapping family.
"""

from collections import Counter
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path

from hkq_cmn import uxlc_external_links
from mb_cmn import bib_locales as tbn
from mb_cmn import provenance
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import verse_external_links as vel
from mb_misc import mb_html
from near_aleppo import build_paths, edition
from py_html import hebrew_letter_spacing as spacing
from py_misc import mam_doc_utils
from py_misc import ren_html_for_renel as hfr
from render_wt import render_wikitext as rwt

PAGE = "foi/cramped-atoms.html"
TITLE = "Cramped words and letter spacing in NAEE"


@dataclass(frozen=True)
class Example:
    reference: tuple
    reading: str
    consonants: str


@dataclass(frozen=True)
class Family:
    identifier: str
    title: str
    description: str
    examples: tuple[Example, ...]


FAMILIES = (
    Family(
        spacing.NARROW_VOWEL_ACCENT,
        "A wide vowel and accent on a narrow letter",
        "In this family of words, yod or vav carries both a wide below-vowel "
        "and a below-accent. The vowel dots and accent share a narrow letter’s "
        "space. This family is expanded automatically in NAEE.",
        (
            Example((tbn.BK_EZEKIEL, 14, 14), "qere", "דניאל"),
            Example((tbn.BK_GENESIS, 9, 11), "body", "יהיה"),
            Example((tbn.BK_JONAH, 1, 2), "body", "נינוה"),
        ),
    ),
    Family(
        spacing.FONT_ADDED_SPACE,
        "Words where Taamey D adds spacing",
        "In this family of words, Taamey D adds space in particular combinations "
        "of narrow letters and below-marks, near final descending letters, and "
        "where a ḥataf vowel precedes an accented narrow letter. NAEE gives these words its "
        "additional spacing as well. These examples show the six observed "
        "combinations selected from the font’s spacing rules.",
        (
            Example((tbn.BK_GENESIS, 29, 22), "body", "ויעש"),
            Example((tbn.BK_GENESIS, 8, 20), "body", "ויבן"),
            Example((tbn.BK_GENESIS, 31, 37), "body", "נגד"),
            Example((tbn.BK_GENESIS, 15, 1), "body", "מגן"),
            Example((tbn.BK_ISAIAH, 40, 7), "body", "נבל"),
            Example((tbn.BK_EXODUS, 14, 19), "body", "מחנה"),
        ),
    ),
    Family(
        spacing.YOD_BEFORE_QOF,
        "A raised vowel on yod before qof",
        "In this family of words, Taamey D raises yod’s vowel to make room beside "
        "the following qof’s vowel and below-accent. NAEE adds horizontal space "
        "to separate the neighboring groups of marks more clearly.",
        (
            Example((tbn.BK_JEREM, 15, 19), "body", "יקר"),
            Example((tbn.BK_GENESIS, 27, 31), "body", "יקם"),
            Example((tbn.BK_EZEKIEL, 15, 3), "body", "היקח"),
            Example((tbn.BK_GENESIS, 18, 16), "body", "ויקמו"),
            Example((tbn.BK_GENESIS, 22, 19), "body", "ויקמו"),
            Example((tbn.BK_ISAIAH, 43, 4), "body", "יקרת"),
            Example((tbn.BK_SND_CHR, 20, 19), "body", "ויקמו"),
        ),
    ),
    Family(
        spacing.ADJACENT_NARROW_BELOW,
        "Adjacent narrow letters, both with below-marks",
        "In this family of words, two adjacent narrow letters each carry below-marks. "
        "Wide vowel dots or an extra below-mark leave less room between the sets "
        "of marks. These examples "
        "include vav beside yod and nun beside vav. This family remains a visual "
        "trial; a matching word receives automatic spacing only if it also "
        "belongs to one of the first three families.",
        (
            Example((tbn.BK_GENESIS, 1, 3), "body", "ויהי"),
            Example((tbn.BK_GENESIS, 10, 11), "body", "נינוה"),
            Example((tbn.BK_GENESIS, 22, 3), "body", "וילך"),
        ),
    ),
    Family(
        spacing.QOF_PREDECESSOR_BELOW,
        "Qof and its predecessor, both with below-marks",
        "In this family of words, qof and the letter immediately before it in "
        "reading order both carry below-marks. Qof’s descending stroke adds to the crowding "
        "around those marks. The examples include wide vowel dots on the "
        "predecessor, an extra below-accent on qof, and an extra "
        "below-accent on the predecessor. This family also remains a visual "
        "trial; a matching word receives automatic spacing only if it also "
        "belongs to one of the first three families.",
        (
            Example((tbn.BK_GENESIS, 2, 14), "body", "חדקל"),
            Example((tbn.BK_GENESIS, 2, 15), "body", "ויקח"),
            Example((tbn.BK_GENESIS, 23, 16), "body", "שקל"),
        ),
    ),
)

_READING_CLASSES = {"mam-kq-k": "ketiv", "mam-kq-q": "qere"}
_GLYPH_FORMATTING = frozenset(
    (
        "mam-dqq-stressed",
        "mam-dqq-unstressed",
        "mam-letter-small",
        "mam-letter-large",
        "mam-letter-hung",
    )
)


def _chunks(node, allowed, reading="body", formatted=False):
    """Traverse only HTML tags admitted by the edition's closed render mapping."""
    if isinstance(node, str):
        yield reading, node, formatted
        return
    if isinstance(node, (tuple, list)):
        for child in node:
            yield from _chunks(child, allowed, reading, formatted)
        return
    tag = mb_html.htel_get_tag(node)
    css_class = node.get("attr", {}).get("class")
    if (tag, css_class) not in allowed:
        raise ValueError(f"Unexpected Scripture HTML: {(tag, css_class)}")
    if tag in ("rp", "br") or css_class == "near-aleppo-kq-none":
        yield "boundary", "", False
        return
    if tag == "ruby":
        yield "boundary", "", False
    reading = _READING_CLASSES.get(css_class, reading)
    formatted = formatted or css_class in _GLYPH_FORMATTING or tag == "b"
    yield from _chunks(node.get("contents") or (), allowed, reading, formatted)
    if tag == "ruby":
        yield "boundary", "", False


def _atoms(scripture, mapping):
    """Select whole atoms without joining the baseline, annotation or nearby body."""
    for reading, chunks in groupby(
        _chunks(scripture, set(mapping.values())), lambda c: c[0]
    ):
        if reading == "boundary":
            continue
        pieces = []
        formatted_ranges = []
        position = 0
        for _, text, formatted in chunks:
            pieces.append(text)
            if formatted:
                formatted_ranges.append((position, position + len(text)))
            position += len(text)
        text = "".join(pieces)
        for start, end, atom in spacing.iter_atoms(text):
            if any(start < stop and end > begin for begin, stop in formatted_ranges):
                continue
            yield reading, atom


def resolved_examples():
    """Resolve every selected example against current rendered NAEE Scripture."""
    mode = edition.NEAR_ALEPPO_MODE
    bkids = tuple(dict.fromkeys(e.reference[0] for f in FAMILIES for e in f.examples))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    rendered = {bkid: rwt.render(bkid, books, mode.renopts, {}) for bkid in bkids}
    ctx = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    resolved = {}
    for family in FAMILIES:
        for example in family.examples:
            bcvt = tbn.mk_bcvtmam(*example.reference)
            body = mam_doc_utils.mark_doc_targets(
                rendered[example.reference[0]][bcvt].verse
            )
            scripture = hfr.html_for_ren_el(ctx, body)
            matches = [
                atom
                for reading, atom in _atoms(scripture, mode.ht_tac_for_ren_tag)
                if reading == example.reading
                and "".join(c for c in atom if "א" <= c <= "ת") == example.consonants
            ]
            if len(matches) != 1 or family.identifier not in spacing.types_for_atom(
                matches[0]
            ):
                raise ValueError(
                    f"Spacing example no longer matches {family.identifier}: {example}, {matches}"
                )
            resolved[example] = matches[0]
    return resolved


def counts_by_family():
    """Count distinct pointed words and occurrences in the examples' projection."""
    mode = edition.NEAR_ALEPPO_MODE
    books = plus.read_parsed_plus_bk39s(
        tbn.ALL_BK39_IDS, str(build_paths.dataset_dir().parent)
    )
    ctx = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    counts = {family.identifier: Counter() for family in FAMILIES}
    for bkid in tbn.ALL_BK39_IDS:
        for verse in rwt.render(bkid, books, mode.renopts, {}).values():
            body = mam_doc_utils.mark_doc_targets(verse.verse)
            scripture = hfr.html_for_ren_el(ctx, body)
            for _, atom in _atoms(scripture, mode.ht_tac_for_ren_tag):
                for identifier in spacing.types_for_atom(atom):
                    counts[identifier][atom] += 1
    if not all(counts.values()):
        raise ValueError("Spacing survey found an empty example family")
    return counts


def _reference_link(reference):
    book, chapter, verse = reference
    label = f"{uxlc_external_links.TANACH_US_BOOK_CODES[book]} {chapter}:{verse}"
    return mb_html.anchor(
        label,
        {
            "href": "../" + vel.near_aleppo_href(*reference),
            "title": f"{uxlc_external_links.book_display_name(book)} {chapter}:{verse}",
        },
    )


def _family_counts_table(counts, resolved):
    rows = [
        mb_html.table_row_of_headers(
            ("Family", mb_html.abbr("Occ.", {"title": "Occurrences"}), "spacing")
        )
    ]
    for family in FAMILIES:
        expanded = {
            spacing.needs_expansion(resolved[example]) for example in family.examples
        }
        if len(expanded) != 1:
            raise ValueError(
                f"Spacing examples no longer share one spacing: {family.identifier}"
            )
        rows.append(
            mb_html.table_row_of_data(
                (
                    mb_html.anchor_h(family.title, "#" + family.identifier),
                    f"{counts[family.identifier].total():,}",
                    "expanded" if True in expanded else "usual",
                )
            )
        )
    return mb_html.div(mb_html.table(rows), {"class": "table-wrap"})


def _family_table(family, resolved):
    rows = [
        mb_html.table_row_of_headers(
            (
                "Usual spacing",
                "Added spacing",
                mb_html.abbr("bcv", {"title": "book-chapter-verse"}),
            )
        )
    ]
    for example in family.examples:
        atom = resolved[example]
        rows.append(
            mb_html.table_row_of_data(
                (
                    atom,
                    mb_html.span_c(atom, spacing.CLASS),
                    _reference_link(example.reference),
                ),
                (
                    {"dir": "rtl", "lang": "hbo", "class": "pointed spacing-atom"},
                    {"dir": "rtl", "lang": "hbo", "class": "pointed spacing-atom"},
                    {"class": "spacing-reference"},
                ),
            )
        )
    return mb_html.div(mb_html.table(rows), {"class": "table-wrap"})


def render():
    """Return the generated spacing FOI page as bytes."""
    resolved = resolved_examples()
    counts = counts_by_family()
    body = [
        mb_html.heading_level_1(TITLE),
        mb_html.para(
            [
                mb_html.anchor_h("Features of interest", "index.html"),
                " · ",
                mb_html.anchor_h("NAEE book links", "../edition/index.html"),
            ]
        ),
        mb_html.para(
            "This document shows examples of words that can look cramped in Taamey D even "
            "when no stroke overlaps."
        ),
        mb_html.para(
            "We group these words into families based on the circumstances that "
            "might cause the cramping. A word can be in more than one family. "
            "The families provide candidates for visual "
            "judgment rather than an exhaustive inventory of cramped words."
        ),
        mb_html.para(
            "The example tables compare “Usual spacing” with “Added spacing” "
            "(0.06em extra letter spacing). In the summary table, “spacing” gives "
            "the spacing NAEE uses for the examples in each family. NAEE "
            "automatically expands words in the first three families."
        ),
        mb_html.para(
            "The last two families are for visual trials: adjacent narrow letters "
            "with below-marks, and qof with below-marks on itself and its predecessor. "
            "These descriptions select many words, including ordinary-looking ones; "
            "they have not been adopted as automatic spacing rules. A word in either "
            "trial family still receives automatic spacing if it also belongs to "
            "one of the first three families."
        ),
        mb_html.para(
            "Counts cover Scripture in NAEE, including ketiv and qere. Counts "
            "distinguish different spellings and pointing, including accent marks; "
            "occurrences count each appearance. Words in notes and words with "
            "special letters (small, large, or hung) are excluded. Adding the family totals would "
            "double-count words that belong to more than one family."
        ),
        _family_counts_table(counts, resolved),
    ]
    for family in FAMILIES:
        words = counts[family.identifier]
        if family.identifier == spacing.YOD_BEFORE_QOF:
            if {resolved[example] for example in family.examples} != set(words):
                raise ValueError("Yod-before-qof examples no longer cover every word")
            count_text = f"Showing all {len(words):,} distinct pointed words "
        else:
            count_text = (
                f"Showing {len(family.examples):,} examples from "
                f"{len(words):,} distinct pointed words "
            )
        body.extend(
            (
                mb_html.heading_level_2(family.title, {"id": family.identifier}),
                mb_html.para(family.description),
                mb_html.para(
                    count_text + f"({words.total():,} occurrences).",
                    {"class": "spacing-counts"},
                ),
                _family_table(family, resolved),
            )
        )
    ctx = mb_html.WriteCtx(
        TITLE,
        PAGE,
        css_hrefs=(
            "../../document.css",
            "../../MAM-parsed/style.css",
            "../style.css",
            "../edition/ketiv-qere.css",
        ),
        html_comment=provenance.generated_html_comment(__file__),
        body_class="spacing-study",
        head_style=Path(__file__).with_suffix(".css").read_text(encoding="utf-8"),
    )
    return {PAGE: mb_html.html_text(body, ctx).encode("utf-8")}
