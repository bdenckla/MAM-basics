r"""Generate gh-pages/wlc/accgram/supplied-marks.html -- the supplied-mark inventory (wlc-utils#36).

A *supplied mark* is a third kind of editorial charity, distinct from the two on the
almost-errors page.  Those *reinterpret* a mark the manuscript already has (a prose
geresh muqdam read as a plain geresh; a poetic plain geresh promoted to revia mugrash).
A supplied mark instead *adds* a mark WLC lacks: when WLC's dual cantillation drops
one reading's accent on a chanted word (it committed to the other reading's grouping), the
dual-cantillation detangler supplies that one accent from MAM so the reading's chanted
verse parses.  Because it is a new kind of charity, it gets its own page rather than a row
in "Editorial charities".

A supplied-mark chanted word parses clean -- the supply is exactly what lets it parse -- so it is
surfaced ONLY here, never counted as a prose ungrammatical verse.  (A genuine WLC dual-cantillation
*error*, where WLC has an accent neither reading explains, is the opposite case: it is
not supplied but flagged, and appears in the prose ungrammatical-verse report.)

The page has two inventories, both generated live from the detangling run
(accgram.dual_cant_run) so they can never drift from the checker's real behaviour:

  * "Supplied accents": each of the five supplied accents in turn -- its reading, the
    accent supplied, what WLC has instead, and the LC manuscript image; and
  * "Supplied and suppressed punctuation": the punctuation marks (maqaf, sof pasuq,
    legarmeh) each reading supplies or suppresses relative to WLC's tangled form
    (narrow-sense paseq is not part of the accent grammar and is not tracked).

Run via ``main_accgram.py generate-html``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import accent_marks as am
from accgram import dual_cant_run
from accgram import uni_to_marks
from accgram.dual_cant_detangle import display_real_marks
from accgram import rtms_report
from accgram import rtmsr_media
from accgram.almost_errors_html_shared import (
    link,
    ref_display,
    ref_short,
    wrap_hebrew_runs,
)
from accgram.mam_simple_verse import default_mam_simple_dir
from accgram import rtms_data
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import paths
from mb_cmn import provenance
from py_html import my_html_for_img
from py_html import wlc_utils_html as H

REPORT_TITLE = "Supplied and suppressed marks"
_WIDTH_CLASS = "goerwitz-tms-width-limited"

# het is transliterated X in the detangler's ASCII labels and precomposed U+1E25
# (never plain h) in the page's Unicode prose -- see the repo transliteration standard.
_XET = "ḥ"
_TAXTON = "ta" + _XET + "ton"
_ELYON = "elyon"
_TIPEXA = "tipe" + _XET + "a"

# X-form (ASCII) label -> the page's real-glyph display form.
_TRANSLIT = {"taxton": _TAXTON, "tipexa": _TIPEXA, "atnax": "atna" + _XET}

_UXLC_DT58_NOTE = "https://tanach.us/Notes/Deuteronomy/Deuteronomy.5.8.2-t.html"

# Each supplied accent, paired with its manuscript image.  Keyed by (bcv, strand, accent
# codepoint) and cross-checked at render time against the live supplies, so it cannot drift.
# Four are LC crops (the LC-... names carry their own Sefaria source link/caption); dt 5:8
# has no clean LC line of its own here, so we borrow the crop from its UXLC note.
_LC, _UXLC_NOTE = "lc", "uxlc-note"
_CASE_IMAGE: dict[tuple[str, str, str], tuple[str, str]] = {
    ("dt5:6", "bet", am.TIPEXA): ("LC-102A-col-3-line-19-Deut-5v6.png", _LC),
    ("dt5:6", "bet", am.ATNAX): ("LC-102A-col-3-line-20-Deut-5v6.png", _LC),
    ("dt5:8", "alef", am.QADMA): ("Deut-5v8-uxlc-note.jpg", _UXLC_NOTE),
    ("dt5:17", "alef", am.TIPEXA): ("LC-102B-col-2-line-9-Deut-5v17.png", _LC),
    ("ex20:3", "alef", am.MERKHA): ("LC-043A-col-2-line-19-Exod-20-v3.png", _LC),
}

_PASSAGE_RANK = {"gn": 0, "ex": 1, "dt": 2}

# The punctuation glyph each tracked mark contributes -- coloured in the Word column to show what
# was supplied or suppressed.  A legarmeh is shown by its broad-sense paseq bar -- the visible
# punctuation it adds over its bare accent.
_MARK_GLYPH = {
    "maqaf": uni_to_marks.MAQAF,
    "sof pasuq": am.SOF_PASUQ,
    "legarmeh": am.PASEQ,
}

_SORTABLE_TH_CLASS = "goerwitz-tms-sortable"
# The table ships in canonical (Verse-ascending) order, so the Verse header carries this
# initial aria-sort to show its arrow on load; the JS toggles it from there.
_DEFAULT_SORT_COL = "Verse"


def default_html_out_path(repo_root: Path) -> Path:
    return paths.wlc_pages_dir() / "accgram" / "supplied-marks.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--wlc422-kq-u-dir",
        type=Path,
        default=rtms_data.default_wlc422_kq_u_dir(repo_root),
        help="Directory of WLC 4.22 ketiv/qere Unicode 1verses_*.json files.",
    )
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=default_mam_simple_dir(repo_root),
        help="Directory of MAM-simple json-vtrad-bhs book files.",
    )
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the supplied-marks page.",
    )


def _translit(text: str) -> str:
    """Render the detangler's ASCII het (X) labels in the page's real-glyph form."""
    for ascii_form, uni_form in _TRANSLIT.items():
        text = text.replace(ascii_form, uni_form)
    return text


def _comment(contents) -> object:
    return H.para(contents, {"class": "goerwitz-tms-comment"})


def _intro() -> tuple[object, ...]:
    return (
        H.heading_level_1(REPORT_TITLE),
        H.heading_level_2("Introduction"),
        H.para(
            (
                "WLC, like the LC itself, has three dually-cantillated prose passages:"
                " the two Decalogues (Exodus 20, Deuteronomy 5)"
                " and the Reuben/Bilhah verse (Genesis 35:22)."
                " Before attempting to grammar-check one of these passages we"
                " detangle"
                " it into its two single-cantillation strands, guided by MAM’s"
                " strands."
                " After detangling a passage, we feed each strand’s chanted verses to"
                " the ordinary prose accent grammar checker."
                " The accents checked are WLC’s own, except for the cases described below.",
            )
        ),
        H.para(
            (
                "Sometimes WLC leaves a chanted word without an accent in one strand."
                " In these cases, the detangler ",
                H.bold("supplies"),
                " that one accent from MAM, making that strand’s chanted verse grammatical."
                " These charitably-supplied accents are recorded below."
                " This is a third kind of charity, distinct from the two reinterpretations on the",
                *[" ", link("almost-errors page", "almost-errors.html"), ":"],
                " those reinterpret the type of geresh present in WLC,"
                " whereas a supplied mark adds a mark not present in WLC.",
            )
        ),
        H.para(
            (
                "A verse with a supplied mark parses cleanly,"
                " so it is listed here since it will not be"
                " listed among the ungrammatical verses."
                f" One verse, Deuteronomy 5:8, gets a supplied accent that fixes the {_TAXTON} strand, but the {_ELYON} strand’s accent is ungrammatical."
                " Therefore, the beleaguered chanted word of that verse is listed both here and among",
                *[" ", link("the ungrammatical verses", "goerwitz.html#obdt5v8"), "."],
            )
        ),
    )


# --------------------------------------------------------------------------- #
# "Supplied accents": each supply in turn, with explanatory text and its image.
# --------------------------------------------------------------------------- #
def _image_block(img_file: str, kind: str) -> object:
    if kind == _LC:
        # rtmsr_media builds the "Image source: <page> column N line N" caption + Sefaria link.
        figures = rtmsr_media.render_image_paragraphs(
            {"img": img_file}, structured_text_lookup=lambda row, key: row.get(key)
        )
        return figures[0]
    # The UXLC-note crop: credit the note (an LC image, served via Sefaria).
    para = my_html_for_img.html_for_single_img(
        img_file, img_para_attr={"class": "goerwitz-tms-image"}, img_base="img/"
    )
    caption = H.figcaption(
        (
            "Image source: ",
            H.anchor("tanach.us note", {"href": _UXLC_DT58_NOTE}),
            " (Leningrad Codex, via Sefaria.org).",
        ),
        {"class": "goerwitz-tms-image-caption"},
    )
    return H.figure((para, caption), {"class": "goerwitz-tms-figure"})


_DUAL_UNDER_BARS_PAGE = "dual-under-bars-in-leningrad-decalogues.html"
_DUAL_UNDER_BARS_CASES = {("ex20:3", "alef", am.MERKHA), ("dt5:17", "alef", am.TIPEXA)}


def _case_extra(s) -> tuple[object, ...]:
    """Extra prose for Deuteronomy 5:8's ungrammatical-verse cross-reference."""
    key = (s.bcv, s.strand, s.accent)
    extra: list[object] = []
    if key == ("dt5:8", "alef", am.QADMA):
        extra.append(
            _comment(
                (
                    "This chanted word is further discussed",
                    *[" ", link("here", "goerwitz.html#obdt5v8"), ","],
                    " among the ungrammatical verses.",
                )
            )
        )
    return tuple(extra)


def _aside_paragraph(s) -> object:
    """The under-bar Aside paragraph for the two cases (dt5:17, ex20:3) whose WLC mark is
    itself part of the identity-ambiguous under-bar family: ``dual_cant_detangle``'s
    ``_under_bar_note`` leaves the sentence open, and this closes it with a link to the
    "Dual Under-Bars" evidence page."""
    assert (s.bcv, s.strand, s.accent) in _DUAL_UNDER_BARS_CASES
    pieces = list(wrap_hebrew_runs(_translit(s.aside)))
    pieces += [
        " ",
        link("Dual Under-Bars in the Leningrad Decalogues", _DUAL_UNDER_BARS_PAGE),
        ".)",
    ]
    return _comment(tuple(pieces))


def _anchor_id(s) -> str:
    """A stable ASCII fragment id for this supplied-accent block, so other pages can
    deep-link straight to one case -- notably UXLC-utils's CLC long-notes, whose
    grammar-checker-corroborated notes point here.  Keyed by the same (bcv, strand, accent)
    triple as ``_CASE_IMAGE``, so it is unique per block even when a verse has two supplies
    (Deuteronomy 5:6 supplies both a tipeḥa and an atnaḥ).  The bcv's colon becomes ``v``
    (``dt5:6`` -> ``dt5v6``); the accent keeps the repo's ASCII het-as-X spelling
    (``tipexa``, ``atnax``), so the whole id stays plain ASCII."""
    return f"supplied-{s.bcv.replace(':', 'v')}-{s.strand}-{s.accent_name}"


def _supplied_case(s) -> tuple[object, ...]:
    img_file, kind = _CASE_IMAGE[(s.bcv, s.strand, s.accent)]
    header = H.para(
        f"{ref_display(s.bcv)}: the detangler supplies the {_translit(s.strand_label)}’s"
        f" {_translit(s.accent_name)}",
        {"class": "goerwitz-tms-reading-label", "id": _anchor_id(s)},
    )
    reason = _comment(wrap_hebrew_runs(_translit(s.reason)))
    aside = (_aside_paragraph(s),) if s.aside else ()
    return (header, _image_block(img_file, kind), reason, *aside, *_case_extra(s))


def _supplied_section(supplies: list) -> tuple[object, ...]:
    blocks: list[object] = [H.heading_level_2("Supplied accents")]
    if not supplies:
        blocks.append(H.para("No marks were supplied."))
        return tuple(blocks)
    for s in supplies:
        if (s.bcv, s.strand, s.accent) not in _CASE_IMAGE:
            raise KeyError(
                f"supplied-marks page has no image/case for {s.bcv} {s.strand}"
                f" {s.accent_name}; add it to _CASE_IMAGE."
            )
    for s in sorted(supplies, key=_reading_order_key):
        blocks.extend(_supplied_case(s))
    return tuple(blocks)


def _reading_order_key(s) -> tuple:
    bb = s.bcv[:2]
    chnu, vrnu = (int(p) for p in s.bcv[2:].split(":"))
    # alef strand (taxton/pashut) before bet (elyon/midrashit) within a verse
    return (_PASSAGE_RANK.get(bb, 9), chnu, vrnu, 0 if s.strand == "alef" else 1)


# --------------------------------------------------------------------------- #
# "Supplied and suppressed punctuation": the maqaf / sof pasuq / legarmeh inventory.
# --------------------------------------------------------------------------- #
def _punct_intro() -> tuple[object, ...]:
    """The two-paragraph intro: punctuation detangling flows directly from accent
    detangling, then a pointer to the table."""
    return (
        H.para(
            "In addition to suppressing (and sometimes supplying) accents, the detangler also"
            " suppresses and supplies three accent-coupled punctuation marks: maqaf, sof pasuq,"
            " and legarmeh. This punctuation work flows directly from the accent detangling."
            " Indeed, these marks are so tightly coupled to their accents — or, in the case of"
            " maqaf, to the lack of an accent — that detangling accents and detangling"
            " punctuation can be regarded as one and the same activity."
        ),
        H.para(
            "The table below — sortable by clicking its header cells — lists every punctuation"
            " change the detangler makes, both suppressed and supplied."
        ),
    )


def _punct_sort_key(d) -> tuple:
    chnu, vrnu = (int(p) for p in d.bcv[2:].split(":"))
    return (
        _PASSAGE_RANK.get(d.bcv[:2], 9),
        0 if d.strand == "alef" else 1,
        chnu,
        vrnu,
        d.mark,
        d.delta,
    )


def _delta_class(delta: str) -> str:
    return "goerwitz-tms-supplied" if delta == "supplied" else "goerwitz-tms-suppressed"


def _verse_sort_key(bcv: str) -> str:
    """A canonical, lexically-sortable verse key (passage rank + zero-padded chapter:verse) for the
    table's client-side sort, e.g. ``gn35:22`` -> ``0-035-022``."""
    chnu, vrnu = (int(p) for p in bcv[2:].split(":"))
    return f"{_PASSAGE_RANK.get(bcv[:2], 9)}-{chnu:03d}-{vrnu:03d}"


def _word_cell(d) -> object:
    """The Word cell: the strand word (MAM stress-helpers stripped) with only the changed
    punctuation coloured.  A supplied mark sits inside normal-colour square brackets (the
    editorial-supply convention), the brackets wrapping just the mark; a suppressed mark is
    appended, coloured, after the clean word."""
    cls = _delta_class(d.delta)
    body = display_real_marks(d.mam_word, d.wlc_word)
    glyph = _MARK_GLYPH[d.mark]
    if d.delta == "supplied":
        before, _, after = body.partition(glyph)
        pieces = (before, "[", H.span_c(glyph, cls), "]", after)
    else:
        pieces = (body, H.span_c(glyph, cls))
    return H.span(pieces, {"lang": "hbo"})


def _sortable_th_attrs(name: str) -> dict:
    attrs = {"class": _SORTABLE_TH_CLASS, "scope": "col"}
    if name == _DEFAULT_SORT_COL:
        attrs["aria-sort"] = "ascending"
    return attrs


def _punct_table(changes: list) -> object:
    sortable = tuple(
        H.table_header(name, _sortable_th_attrs(name))
        for name in ("Verse", "Strand", "Mark", "Change")
    )
    header = H.table_row(sortable + (H.table_header("Word", {"scope": "col"}),))
    rows = [header]
    for d in sorted(changes, key=_punct_sort_key):
        rows.append(
            H.table_row_of_data(
                (
                    ref_short(d.bcv),
                    _translit(d.strand_label),
                    d.mark,
                    H.span_c(d.delta, _delta_class(d.delta)),
                    _word_cell(d),
                ),
                tdattrs=({"data-sort": _verse_sort_key(d.bcv)}, None, None, None, None),
            )
        )
    return H.table(tuple(rows), {"class": "goerwitz-obs-tree-table"})


def _punct_observation(changes: list) -> object:
    """An observation drawn from the table: WLC's Decalogue punctuation sits far closer to
    the elyon (only suppressions needed) than to the taxton (supplies plus suppressions).  The
    counts are tallied live from the changes so they track the checker, not a hard-coded number.
    """
    elyon_supplied = sum(
        1 for d in changes if d.strand_label == "elyon" and d.delta == "supplied"
    )
    elyon_suppressed = sum(
        1 for d in changes if d.strand_label == "elyon" and d.delta == "suppressed"
    )
    taxton_supplied = sum(
        1 for d in changes if d.strand_label == "taxton" and d.delta == "supplied"
    )
    taxton_suppressed = sum(
        1 for d in changes if d.strand_label == "taxton" and d.delta == "suppressed"
    )
    # The prose claims the elyon needs only suppressions ("all that is needed is to suppress");
    # check that against the live counts so the text can't drift from the checker.
    assert (
        elyon_supplied == 0
    ), f"prose says no elyon marks are supplied, but {elyon_supplied} are"
    return H.para(
        "Sorting by “Strand” reveals that the Decalogues are largely punctuated according to the"
        f" {_ELYON}: to correctly punctuate the {_ELYON} all that is needed is to suppress"
        f" {elyon_suppressed} punctuation marks that are {_TAXTON}-only. Correctly punctuating the"
        f" {_TAXTON}, by contrast, takes much more work: {taxton_supplied} marks must be supplied"
        f" and {taxton_suppressed} {_ELYON}-only marks suppressed."
    )


def _punct_section(changes: list) -> tuple[object, ...]:
    heading = H.heading_level_2("Supplied and suppressed punctuation")
    if not changes:
        return (heading, H.para("No punctuation was supplied or suppressed."))
    return (
        heading,
        *_punct_intro(),
        _punct_observation(changes),
        _punct_table(changes),
    )


def render_body_contents(
    supplies: list, punctuation_changes: list
) -> tuple[object, ...]:
    sections: list[object] = [
        *_intro(),
        *_supplied_section(supplies),
        *_punct_section(punctuation_changes),
    ]
    wrapper = H.div(tuple(sections), {"class": _WIDTH_CLASS})
    script = H.htel_mk("script", {"src": "supplied-marks-sort.js"})
    return (wrapper, script)


def run(args: argparse.Namespace) -> None:
    results = dual_cant_run.detangle_results(args.wlc422_kq_u_dir, args.mam_simple_dir)
    supplies = [s for pr in results for s in pr.supplied_marks]
    punctuation_changes = [d for pr in results for d in pr.punctuation_changes]

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(supplies, punctuation_changes),
        write_ctx=H.WriteCtx(
            title=REPORT_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(
        f"HTML: {html_out} ({len(supplies)} supplied marks, "
        f"{len(punctuation_changes)} punctuation changes)"
    )


def main() -> None:
    force_utf8_io()
    repo_root = paths.repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
