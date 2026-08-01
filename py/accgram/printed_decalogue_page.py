r"""Generate gh-pages/accgram/printed-decalogue.html -- the printed-tradition Decalogue
grammaticality report (issue #52).

Companion to the dual-cantillation work of issue #36 (which grammar-checks the *manuscript*
taxton/elyon strands by detangling WLC): this page reports whether the *printed tradition*'s
(דפוסים) taxton and elyon accentuations of the two Decalogues parse under the same prose
grammar checker.  It renders live from ``printed_decalogue.check_all`` over the vendored
readings, so it can never drift from the checker's real behaviour.

It also lays out the four cantillation strands of the opening אנכי...מצותי span (manuscript /
printed x taḥton / elyon) over that span's shared frame and its two signal words, resolved by the
shared ``printed_decalogue_strands`` module.  The Simanim and Koren companion pages
(``printed_decalogue_simanim_page``, ``printed_decalogue_koren_page``) link back to that table
rather than duplicating it.

The strands are IDEALIZED, and since issue #52's transcription work the page also says, in one
paragraph, how the twelve hand-transcribed real Decalogues fare under the same checker: eleven
give their Wikisource strand's verdicts at every chanted verse -- four of them by printing the
p-trad elyon's ungrammatical merged opening verse, which is what stops that finding being an
artifact of the idealization -- and one departs.  Those counts come live from
``transcription_parse.check_all``,
and the per-Decalogue verdicts stay on the two satellite pages, which is where they are
documented; the hub must not assert what a satellite does not.

The appendix cataloguing how the two taxton strands differ states counts, and every one of them
is derived: ``printed_decalogue_taxton_diff`` re-counts the whole Deuteronomy divergence set from
the vendored words on each generation and raises unless it still decomposes as pinned there.  A
2026-07-25 claim audit found the appendix asserting "three" against a table showing seven, which
is why no number in it is typed any more.

That appendix also explains its one Exodus difference rather than only recording it: the qamats /
patax at תרצח is the pausal alternation, which the Decalogue shows working ordinarily at על־פני and
מתחת, where the two strands' own accents differ and the vowel follows them (``_pausal_paras``).
Those forms are derived and pinned by ``printed_decalogue_strands.resolve_pausal`` /
``check_tirtsax``, on the same fail-on-drift terms as everything else here.

Editorial / style conventions for the rendered prose are single-sourced in
``printed_decalogue_strands`` (bare-Hebrew strand names תחתון / עליון in output, romanized only
in ``title`` / ``alt`` attributes and internal keys; ``ROM_*`` accent names never retyped; real
em dashes; and ``MAQAF_IS_THE_LAST_RUNG``, the scale this page states on behalf of the whole
trio).

Run via ``main_accgram.py generate-html``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds
from accgram import printed_decalogue_taxton_diff as pdt
from accgram import rtms_report
from accgram import transcription_parse as tp
from accgram.almost_errors_html_shared import hbo, link
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import hebrew_accent_strip as has
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpunc
from mb_cmn import provenance

from py_html import wlc_utils_html as H
from py_html.my_html_span_romanized import rmn

import wlc_paths

REPORT_TITLE = "In the printed tradition, are the accents of the Decalogue grammatical?"

_GOERWITZ_URL = "goerwitz.html"
_SOURCE_URL = "https://he.wikisource.org/wiki/עשרת_הדברות_בסיס/טעמים"

# The two satellite pages, which document the per-Decalogue verdicts this page only totals.
_SIMANIM_PAGE = "printed-decalogue-simanim.html"
_KOREN_PAGE = "printed-decalogue-koren.html"

# Not a satellite: it reports no verdict of this repo's, only the editions MAM-basics issue #208
# cites at ובנך, where the two satellites' editions and the Wikisource p-trad עליון disagree.
_UVINKHA_PAGE = "printed-decalogue-uvinkha.html"

_CTR_REVIEW_URL = (
    "https://bdenckla.github.io/MAM-with-doc/misc/rocc_0_review_of_ctr.html"
)

# CTR (The Complete Tanach with Rashi) on Chabad.org, deep-linked to Deuteronomy 5 -- the
# Sabbath-commandment chapter whose p-trad תחתון cantillation the appendix above dissects.
_CHABAD_DT5_URL = (
    "https://www.chabad.org/torah-texts/9969/Tanakh-The-Hebrew-Bible/"
    "Torah-The-Pentateuch/Devarim-Deuteronomy/Chapter-5"
)

# In-page anchor for the appendix cataloguing the grammar-irrelevant p-trad-vs-m-trad תחתון
# differences (single-sourced: used as both the verdict-paragraph link's href fragment and the
# appendix heading's id, matching the #four-strands / #why-the-printed-elyon-fails style).
_TAHTON_DETAILS_ID = "tahton-details"

# In-page anchor for the paragraph totalling how the twelve transcribed real Decalogues fare
# under the checker -- the one thing on this page that is about editions rather than strands, and
# the target of the verdict section's forward reference to it.
_TRANSCRIPTIONS_ID = "real-editions"


# Strand names are single-sourced in printed_decalogue_strands (see its module docstring). These
# thin local aliases let the Hebrew strand words drop straight into the prose -- bare in a string
# or as {_TAHTON} / {_ELYON} inside an f-string -- rather than through a lang="he" <span> (issue
# #58), matching the Simanim companion page. Genuinely *pointed* Hebrew still goes through hbo()
# (lang="hbo" -> the Taamey pointed-text font); only bare unpointed terms are inlined this way.
_TAHTON = pds.TAHTON
_ELYON = pds.ELYON


# Romanized accent/mark names, each pre-wrapped ONCE in <span class="romanized"> (italic) so every
# prose site below is styled without a per-site rmn() call -- issue #65, finding C2; the rule and
# its exclusions are documented in printed_decalogue_strands' module docstring. These are HTML
# nodes, not strings: splice them into a contents tuple, never into an f-string. The underlying
# spellings stay single-sourced in pds -- don't retype them inline.
_ROM_ETNAHTA = rmn(pds.ROM_ETNAHTA)
_ROM_GERESH = rmn(pds.ROM_GERESH)
_ROM_LEGARMEH = rmn(pds.ROM_LEGARMEH)
_ROM_PASHTA = rmn(pds.ROM_PASHTA)
_ROM_PASEQ = rmn(pds.ROM_PASEQ)
_ROM_REVIA = rmn(pds.ROM_REVIA)
_ROM_SEGOLTA = rmn(pds.ROM_SEGOLTA)
_ROM_SILLUQ = rmn(pds.ROM_SILLUQ)
_ROM_SOF_PASUQ = rmn(pds.ROM_SOF_PASUQ)
_ROM_TIPEHA = rmn(pds.ROM_TIPEHA)
_ROM_ZAQEF_QATAN = rmn(pds.ROM_ZAQEF_QATAN)
_ROM_SILLUQ_SOF_PASUQ = rmn(pds.ROM_SILLUQ_SOF_PASUQ)

# Accent names reach the pausal table as pds.ROM_* strings derived from the data, not as one of the
# aliases above; this maps each back to its wrapped node, so a derived name renders italic like
# every typed one. Only the four accents _PAUSAL_PINS can yield need to be here -- a fifth would
# KeyError, which is the same fail-on-drift behavior the derivation itself has.
_ROM_NODE_BY_NAME: dict[str, object] = {
    pds.ROM_ETNAHTA: _ROM_ETNAHTA,
    pds.ROM_GERESH: _ROM_GERESH,
    pds.ROM_REVIA: _ROM_REVIA,
    pds.ROM_SILLUQ: _ROM_SILLUQ,
}

# The two vowel names. Single-sourced in pds like the accent names above, so the vocalization
# table, the pausal table's derived cells and the prose cannot spell them three ways. Plain str
# rather than rmn() nodes: vowel names render upright on this page, where accent names are italic
# (see _pausal_table's docstring), so these DO drop into an f-string.
_QAMATS = pds.ROM_QAMATS
_PATAX = pds.ROM_PATAX


def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / "printed-decalogue.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument("--source", type=Path, default=pd.default_source_path())
    parser.add_argument(
        "--html-out", type=Path, default=default_html_out_path(repo_root)
    )


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
# Keys into the by-key dict are prefixed (bk-/sk-/tk-) to mark them, at a glance, as internal
# lookup tokens rather than user-visible strings. The raw VersionResult fields are bare
# ("ex", "taxton", "manuscript"); this is the one place they get promoted to prefixed keys, so
# every lookup below must use the prefixed form.
def _bk(vr: pd.VersionResult) -> tuple[str, str, str]:
    return (f"bk-{vr.book}", f"sk-{vr.reading}", f"tk-{vr.tradition}")


def _by_key(
    results: list[pd.VersionResult],
) -> dict[tuple[str, str, str], pd.VersionResult]:
    return {_bk(vr): vr for vr in results}


def _intro() -> tuple[object, ...]:
    # This is the ONE full statement of the four strands in the page trio (issue #65, finding V5).
    # The two satellite pages (printed_decalogue_simanim_page, printed_decalogue_koren_page) used to
    # duplicate this paragraph verbatim; each now opens with a single "As the companion page
    # explains..." sentence linking here instead, so a reader arriving from a satellite can tell
    # reiteration from new material. Keep it that way: don't re-expand the satellites. The one
    # thing all three pages DO say verbatim is the closing pds.MOST_STRIKING sentence, single-
    # sourced there rather than retyped here -- so edit that constant, not this paragraph, to
    # restate the difference; everything else in this paragraph is the main page's alone.
    return (
        H.heading_level_1(REPORT_TITLE),
        H.heading_level_2("The question"),
        H.para(
            (
                "Roughly speaking, each Decalogue",
                " has two strands of cantillation, the טעם תחתון and the טעם עליון.",
                " Why is this only roughly true? Because in detail there are",
                *[" ", H.bold("four"), " strands: the"],
                *[" ", H.bold("printed tradition"), " (p-trad)"],
                " and the",
                *[" ", H.bold("manuscript tradition"), " (m-trad)"],
                " differ in cantillation,",
                f" yielding two different {_ELYON} strands and two different {_TAHTON} strands.",
                #
                " (The p-trad is fading in popularity,"
                " but still visible in editions like"
                " Koren's Tanakh and Simanim's Tiqqun.)",
                #
                # Single-sourced in pds and shared verbatim with the two satellite pages; see
                # pds.MOST_STRIKING for why the difference is stated over this span rather than
                # as the older yes/no question about אנכי…עבדים.
                " " + pds.MOST_STRIKING,
            )
        ),
        H.para(
            (
                "I have run Richard Goerwitz's ",
                link("accent grammar checker", _GOERWITZ_URL),
                " against the m-trad strands (as represented by WLC); this page"
                " shows what happens when the checker is run against the p-trad strands.",
            )
        ),
        H.para(
            (
                "There is no dual cantillation to detangle here. Whereas the Tiberian manuscripts (and WLC)"
                " pack both of their strands onto one set of letters, the Wikisource page ",
                link("עשרת הדברות בסיס/טעמים", _SOURCE_URL),
                " spells out all the strands separately — p-trad and m-trad alike —"
                " each as single cantillation. Every chanted verse"
                " (delimited by its own ",
                _ROM_SOF_PASUQ,
                ") is grammar-checked separately. The"
                " m-trad is the baseline — MAM's authoritative text, expected"
                " to be grammatical throughout — and the p-trad is the object of study.",
            )
        ),
    )


def _cell(vr: pd.VersionResult) -> object:
    n = len(vr.chanted_verses)
    bad = vr.ungrammatical
    if not bad:
        return H.table_datum(f"✓ all {n} clean", {"class": "clean"})
    which = ", ".join(f"verse {cv.index}" for cv in bad)
    return H.table_datum(
        f"✗ {len(bad)} of {n} ungrammatical ({which})", {"class": "ungrammatical"}
    )


# The traditional strand name for each reading (report labels only). No "upper"/"lower" gloss:
# it invites confusion with above-letter vs below-letter accents (see printed_decalogue_strands
# module docstring for the cross-page rule).
_STRAND_LABELS: dict[str, str] = {
    "sk-taxton": "תחתון",
    "sk-elyon": "עליון",
}  # sk: strand key
_BOOK_LABELS: dict[str, str] = {"bk-ex": "Ex.", "bk-dt": "Deut."}  # bk: book key


def _verdict_table(by_key: dict) -> object:
    header = H.table_row_of_headers(("", "m-trad verses", "p-trad verses"))
    rows = [header]
    for book in ("bk-ex", "bk-dt"):
        for strand in ("sk-taxton", "sk-elyon"):
            label = f"{_BOOK_LABELS[book]} {_STRAND_LABELS[strand]}"
            rows.append(
                H.table_row(
                    (
                        H.table_header(label),
                        _cell(by_key[(book, strand, "tk-manuscript")]),
                        _cell(by_key[(book, strand, "tk-printed")]),
                    )
                )
            )
    return H.table(tuple(rows), {"class": "printed-decalogue-verdict"})


def _verdict_section(by_key: dict) -> tuple[object, ...]:
    return (
        H.heading_level_2("The verdict"),
        _verdict_table(by_key),
        H.para(
            (
                f"The {_TAHTON}"
                f" is grammatical everywhere — both books, both traditions. In terms of verse"
                f" boundaries, the p-trad {_TAHTON} differs from the m-trad in only one place: the"
                f" p-trad {_TAHTON} ends its first verse at מבית עבדים (so it has one more verse"
                " than the m-trad, whose first verse runs on to על־פני instead). Both"
                " are grammatical. It also differs in some further details — several of them"
                " changes of cantillation that give the two strands genuinely different"
                " accent-grammar trees, but none that costs either its grammaticality (",
                link("catalogued in an appendix below", f"#{_TAHTON_DETAILS_ID}"),
                ").",
            )
        ),
        H.para(
            (
                f"The {_ELYON}" " is grammatical in the m-trad but ",
                H.bold("not"),
                f" in the p-trad: the p-trad {_ELYON} of ",
                H.bold("each"),
                " Decalogue has exactly one ungrammatical chanted verse — its opening one. That"
                " verse is not only an idealized strand's: real editions have it, as ",
                link("the transcription totals below", f"#{_TRANSCRIPTIONS_ID}"),
                " say.",
            )
        ),
    )


# --------------------------------------------------------------------------- #
# Word stripping and the shared range cell
# --------------------------------------------------------------------------- #
def _strip_pointing(word: str) -> str:
    """Reduce a pointed Hebrew word to letters + accents + accent-coupled
    punctuation (maqaf, sof pasuq, legarmeh), dropping vowels, dagesh, shin/sin dots, rafe,
    and ordinary meteg. A word's U+05BD is *silluq* (an accent, kept) exactly when the word is
    verse-final, i.e. carries sof pasuq; otherwise every U+05BD is an ordinary meteg (a ga'ya)
    and is dropped. Done with the shared mb_cmn.hebrew_accent_strip kernel (cf. MAM-basics
    ``versification_and_cantillation/strands.py::_strip_pointing``)."""
    keep_meteg = has.METEG_SILLUQ if hpunc.SOPA in word else has.METEG_DROP
    return has.strip_to_accents(word, keep_meteg=keep_meteg)


# The `title` text here is an ATTRIBUTE context, so it keeps the romanized "taxton"/"elyon" even
# though the visible prose names the strands in Hebrew letters. That asymmetry is deliberate and
# settled -- see the "Attribute contexts are EXEMPT" bullet in printed_decalogue_strands' module
# docstring before "correcting" any title/alt string on this page or its two satellites.
def _abbr(letter: str, title: str) -> object:
    return H.htel_mk("abbr", {"title": title}, letter)


# ── Letter-equalizing the paired taxton/elyon boundary cells (ported from MAM-basics #201) ──
# Each column shows one underlying text span read by both strands, so the two cells should share
# a letter skeleton at each boundary. They can still divide that span into chanted words
# differently -- most visibly the leading לא of a negative commandment, which the taxton
# maqaf-joins to the next atom (one chanted word, לא־תעשה) while the elyon leaves it free (לא its
# own chanted word). _balanced_sides
# pulls extra boundary words inward, one chanted word at a time, until the two sides' skeletons match, so the
# sibling cells align (e.g. taxton לא־תעשה לך … / elyon לא תעשה־לך …) instead of a bare לא sitting
# under a fuller taxton cell. It asserts equality — a guard that fires loudly on any column it
# cannot reconcile.
def _skel(word: str) -> str:
    """A chanted word's letter skeleton: only the Hebrew letters (alef…tav), dropping points,
    accents, maqaf, sof pasuq and legarmeh — so the one chanted word לא־תעשה and the two chanted
    words לא תעשה compare equal. Uses the same letter bounds as the strip kernel (private today; cf. MAM-basics #198).
    """
    return "".join(ch for ch in word if has._LETTER_LO <= ord(ch) <= has._LETTER_HI)


def _balance_boundary(
    t_words, e_words, *, grow_backward: bool, label: str
) -> tuple[int, int]:
    """How many boundary words each strand must show for their skeletons to match at one end of a
    column. Compares the taxton's and elyon's leading (or, with ``grow_backward``, trailing) run
    of words, growing the shorter-skeleton side inward one word at a time while it stays a prefix/
    suffix of the longer. Raises with the column ``label`` if the skeletons diverge or a side runs
    out of words."""

    def seg(words, take):
        chosen = words[-take:] if grow_backward else words[:take]
        return "".join(_skel(w) for w in chosen)

    t_take = e_take = 1
    while True:
        ts, es = seg(t_words, t_take), seg(e_words, e_take)
        if ts == es:
            return t_take, e_take
        short, long_ = (ts, es) if len(ts) < len(es) else (es, ts)
        aligned = long_.endswith(short) if grow_backward else long_.startswith(short)
        grow_t = len(ts) < len(es)
        room = (t_take < len(t_words)) if grow_t else (e_take < len(e_words))
        if not aligned or not room:
            raise AssertionError(
                f"cannot letter-equalize the {label} boundary — taxton skeleton {ts!r} vs"
                f" elyon skeleton {es!r}; taxton words={t_words!r}, elyon words={e_words!r}"
            )
        if grow_t:
            t_take += 1
        else:
            e_take += 1


def _balanced_sides(t_words, e_words, *, label: str):
    """Letter-balance both ends of a column, returning the displayed boundary word lists
    ``(t_first, t_last, e_first, e_last)`` — each the word(s) whose skeletons the two strands
    share after any pulling."""
    tf, ef = _balance_boundary(
        t_words, e_words, grow_backward=False, label=f"{label} first"
    )
    tl, el = _balance_boundary(
        t_words, e_words, grow_backward=True, label=f"{label} last"
    )
    return t_words[:tf], t_words[-tl:], e_words[:ef], e_words[-el:]


def _range_cell(first_words, last_words, *, start: bool, stop: bool) -> object:
    """A ``first … last`` range cell: the (already letter-balanced) boundary word(s) at each end,
    stripped to letters + accents and joined by an ellipsis. The verse-initial chanted word is green
    when ``start`` and the verse-final chanted word red when ``stop``; any word pulled in only for
    letter-alignment renders plain. ``lang="hbo"`` → Taamey font (issue #58)."""
    fw = [_strip_pointing(w) for w in first_words]
    lw = [_strip_pointing(w) for w in last_words]
    fw[0] = H.span_c(fw[0], "vc-start") if start else fw[0]
    lw[-1] = H.span_c(lw[-1], "vc-stop") if stop else lw[-1]
    # fw words (space-separated), then the ellipsis, then lw words (space-separated).
    nodes: list[object] = []
    for i, node in enumerate(fw):
        if i:
            nodes.append(" ")
        nodes.append(node)
    nodes.append("…")
    for i, node in enumerate(lw):
        if i:
            nodes.append(" ")
        nodes.append(node)
    return H.table_datum(tuple(nodes), {"lang": "hbo"})


# --------------------------------------------------------------------------- #
# The four-strands table (issue #52)
# --------------------------------------------------------------------------- #
# Two-char row-header abbreviations for the four strands, coherent with the nesting tables'
# single E/T letters below; the dotted-underline title spells each out (the romanized form is
# fine in an attribute). m/p = m-trad/p-trad, T/E = taxton/elyon strand. The titles
# say NO "upper"/"lower" -- that gloss invites confusion with above-letter vs below-letter accents
# (see printed_decalogue_strands module docstring; same rule on both printed-Decalogue pages).
_STRAND_ABBRS: dict[str, tuple[str, str]] = {
    "m-trad taḥton": ("mT", "manuscript-tradition taḥton"),
    "m-trad elyon": ("mE", "manuscript-tradition elyon"),
    "p-trad taḥton": ("pT", "printed-tradition taḥton"),
    "p-trad elyon": ("pE", "printed-tradition elyon"),
}

# The four words the אנכי…מצותי span is laid out over, in verse order (rtl: אנכי rightmost →
# מצותי leftmost): the span's shared frame — אנכי, where every strand starts, and מצותי, where
# every strand closes a chanted verse — wrapped around its two signal words, עבדים and על־פני.
# Every strand shows its OWN pointed word in all four columns; no cell is ever empty. A cell is
# red exactly where that strand ends a chanted verse, so the strands' differing chanted-verse
# boundaries — the thing the signal accents decide — read straight down the columns.
#
# The table does NOT show every boundary in the span: the two תחתון strands end two further
# chanted verses between על־פני and מצותי, at לארץ and at לשנאי, which fall between columns. The
# prose says so; don't let a rewrite imply the four columns are the whole story.
#
# Skeletons are letters-only (base_skeleton form), single-sourced from pds so a column can't drift
# from the constants the data layer locates its words by.
_SPAN_COLUMNS: tuple[str, ...] = (pds.ANOKHI, pds.AVADIM, pds.AL_PENEI, pds.MITSVOTAI)


def _word_at(r: pds.Reading, skeleton: str) -> str:
    """The strand's own pointed word at one column, matched by letter skeleton within the
    אנכי…מצותי span. Each strand keeps ITS OWN accent on a shared word (e.g. עבדים is
    etnaḥta / silluq / revia across strands), which is the structure-deciding signal, so the cell
    must show the per-strand form rather than one canonical word per column.

    First match wins, which matters at exactly one column: אנכי occurs TWICE in the span — once as
    the span's opening word and again in כי אנכי. The opening one is the one the table means, and
    it is the one this finds. Don't change the search to last-match or all-matches."""
    for word in r.span_words:
        if pds.base_skeleton(word) == skeleton:
            return word
    raise AssertionError(
        f"{r.name}: no word with skeleton {skeleton!r} in its אנכי…מצותי span"
        " -- the vendored readings drifted"
    )


def _span_cells(r: pds.Reading) -> list[object]:
    """One strand's row of cells over the shared _SPAN_COLUMNS: its own pointed word in every
    column, green at the shared start (אנכי) and red wherever the word ends one of that strand's
    chanted verses."""
    cells: list[object] = []
    for i, skel in enumerate(_SPAN_COLUMNS):
        word = _word_at(r, skel)
        ends_verse = skel in r.span_end_skels
        # The structural fact (this skeleton ends one of the strand's span verses) and the glyph
        # (this word carries sof pasuq) must agree; if they ever don't, the data drifted.
        if ends_verse != (hpunc.SOPA in word):
            raise AssertionError(
                f"{r.name}: {skel!r} ends a chanted verse = {ends_verse}, but its sof pasuq"
                f" says otherwise -- the vendored readings drifted"
            )
        # Column 0 is אנכי, the shared start, and is never verse-final in any strand -- so the
        # green start and a red stop can never collide in one cell.
        cls = "vc-start" if i == 0 else "vc-stop" if ends_verse else "vc-mid"
        cells.append(
            H.table_datum((H.span_c(_strip_pointing(word), cls),), {"lang": "hbo"})
        )
    return cells


def _four_strands_table(readings: list[pds.Reading]) -> object:
    rows: list[object] = []
    for r in readings:
        letter, title = _STRAND_ABBRS[r.name]
        rows.append(
            H.table_row((H.table_header(_abbr(letter, title)), *_span_cells(r)))
        )
    return H.table(tuple(rows), {"class": "strand-table", "dir": "rtl"})


_UL_ITEM_1 = (
    H.bold("The signal pair identifies which strand a text has."),
    " No two strands share the accent pair on the two signal words, so the pair alone says"
    " which strand a text has. Neither one suffices by itself: עבדים cannot tell the m-trad ",
    _ELYON,
    f" from the p-trad {_TAHTON} (both close a chanted verse there), and על־פני cannot tell"
    f" the two {_TAHTON} strands apart, nor the two {_ELYON} strands.",
)

_UL_ITEM_2 = (
    H.bold("Everything else in the span is coupled to the signal accents."),
    " אנכי has a ",
    _ROM_PASHTA,
    " in exactly the two strands whose עבדים runs on mid-verse, and a ",
    _ROM_TIPEHA,
    " in the two whose עבדים ends its verse; מצותי has a ",
    _ROM_SILLUQ_SOF_PASUQ,
    f" in all four — the shared end signals nothing. Between the columns nothing new happens:"
    f" the two {_TAHTON} strands end two further chanted verses between על־פני and מצותי, at"
    " לארץ and at לשנאי — the same two chanted words in both — so strands that agree at a signal"
    " word agree at every chanted word over the stretch that signal governs.",
)

_UL_ITEM_3 = (
    H.bold(f"P-trad {_TAHTON} = m-trad {_ELYON} — but only through עבדים."),
    " Over אנכי…עבדים the two are identical at every chanted word, each giving that stretch its own"
    " chanted verse. They part at על־פני: the p-trad ",
    _TAHTON,
    f" ends another chanted verse there, while the m-trad {_ELYON} has a ",
    _ROM_REVIA,
    " and runs on to מצותי — which is why each has its own row. Over the whole Decalogue the"
    " p-trad ",
    _TAHTON,
    " has ",
    H.bold("13"),
    f" chanted verses, the m-trad {_ELYON} only ",
    H.bold("10"),
    ".",
)


# --------------------------------------------------------------------------- #
# What the twelve real editions do under the checker (issue #52)
# --------------------------------------------------------------------------- #
# The hub states only the TOTALS; the per-Decalogue verdicts are the satellite pages', which is
# where they are documented. Every number below is counted from the checker's own results rather
# than written out, and the one claim the prose makes about WHICH transcriptions share their
# Wikisource strand's failure is checked rather than trusted -- the drift-fails-the-build habit of
# printed_decalogue_strands, applied to a sentence instead of a table cell.
def _strand_ungrammatical(
    verdicts: list[tp.TranscriptionResult],
) -> list[tp.TranscriptionResult]:
    """The transcriptions that agree with their Wikisource strand AND are ungrammatical somewhere.

    Being ungrammatical is then the strand's doing, not the edition's, so the prose says these
    editions PRINT the p-trad עליון's merged opening verse.  That is only worth saying if they
    really do all follow a p-trad עליון, so this raises rather than let the sentence outlive the
    fact.
    """
    shared = [r for r in verdicts if not r.departures and r.ungrammatical]
    odd = [r.stem for r in shared if r.key[1:] != ("elyon", "printed")]
    if odd:
        raise AssertionError(
            f"{odd} share their Wikisource strand's ungrammaticality without following a p-trad"
            f" {pds.ELYON} -- the prose here no longer describes the data"
        )
    return shared


def _transcription_grammar_para(verdicts: list[tp.TranscriptionResult]) -> object:
    shared = _strand_ungrammatical(verdicts)
    departing = [r for r in verdicts if r.departures]
    return H.para(
        (
            "The twelve transcribed Decalogues have been through this same checker, chanted verse"
            " by chanted verse, and what that shows first is that following a strand and parsing"
            " are separate things. ",
            H.bold(f"{len(verdicts) - len(departing)} of the {len(verdicts)}"),
            " give their Wikisource strand's verdicts at every chanted verse — which for the ",
            H.bold(str(len(shared))),
            f" of them that follow a p-trad {_ELYON} means printing that ungrammatical opening"
            " verse. Simanim's Tiqqun does, in both of its main Decalogues, and Koren in both of"
            " its appendix ones: the merged first two commandments are in books in print, not only"
            " in an idealized strand. The remaining"
            " one is the Simanim Tiqqun's Exodus appendix Decalogue, which is ungrammatical at a"
            " chanted verse where its Wikisource strand is clean, over a single added"
            " conjunctive; the ",
            link("Simanim page", _SIMANIM_PAGE),
            " has it.",
        ),
        {"id": _TRANSCRIPTIONS_ID},
    )


def _four_strands_section(
    readings: list[pds.Reading], verdicts: list[tp.TranscriptionResult]
) -> tuple[object, ...]:
    return (
        H.heading_level_2("The four strands of אנכי…מצותי", {"id": "four-strands"}),
        H.para(
            (
                "Every p-trad strand accents the Decalogue's אנכי…מצותי span differently from"
                " every m-trad strand. Two chanted words in the span do all the deciding — its ",
                H.bold("signal words"),
                ", עבדים and על־פני. Where a signal word has a ",
                _ROM_SILLUQ_SOF_PASUQ,
                ", that strand ends a chanted verse there; where it instead has an ",
                _ROM_ETNAHTA,
                " or a ",
                _ROM_REVIA,
                ", it runs on. The table below lays all four strands over four shared"
                " chanted words — ",
                H.bdi("אנכי"),
                " (the span's shared start), then ",
                # bdi_multi isolates each RTL item so the LTR list order survives however a viewer
                # resolves the bidirectional text (else the items merge across the commas).
                *H.bdi_multi(
                    "עבדים",
                    "על־פני",
                    "מצותי",
                ),
                " (the two signal words and the span's shared end). Each row shows that strand's"
                " pointing at all four; a cell is red where its chanted word ends one of that strand's"
                " chanted verses. So every row starts green at אנכי and ends red at מצותי, and"
                " the reds between them are the signal accents at work — the strands' differing"
                " chanted-verse boundaries, read straight down the columns:",
            )
        ),
        _four_strands_table(readings),
        H.unordered_list(
            (
                _UL_ITEM_1,
                _UL_ITEM_2,
                _UL_ITEM_3,
            )
        ),
        H.para(
            (
                "These are facts about the four strands as Wikisource defines them — idealized"
                " strands, each pure by construction. An actual edition need"
                " not follow one strand purely, and where it strays, the two signal words above"
                " cannot catch it. Simanim's Tiqqun, for instance, follows the p-trad ",
                _TAHTON,
                "'s chanted-verse boundaries throughout, yet has the m-trad accents at the"
                " Shabbat commandment of its Deuteronomy appendix Decalogue. Catching that"
                " departure requires giving the Shabbat commandment its own signal words — three"
                " disjunctively accented chanted words, ",
                link("catalogued in the appendix below", f"#{_TAHTON_DETAILS_ID}"),
                ", where the two traditions differ in accents while agreeing on every"
                " chanted-verse boundary. The two sets of signal words have complementary jobs:"
                " עבדים and על־פני place a text among the four strands within אנכי…מצותי, while the"
                " Shabbat trio tells p-trad accents from m-trad accents at a commandment where a"
                " real edition can stray from its nominal tradition.",
            )
        ),
        # The transcription basis (issue #69). The hub states only what is a fact about the
        # STRANDS; the per-Decalogue verdicts live on the two satellite pages, and this page must
        # not assert what they do not document. The ובנך־ובתך sentence is here rather than there
        # precisely because neither satellite can tell it alone: it takes both editions.
        H.para(
            (
                "That departure by the Simanim Tiqqun is checked, not supposed. ",
                H.bold("Twelve"),
                " printed Decalogues — four each from Simanim's Tiqqun, Simanim's Tanakh and"
                " Koren's Classic Tanakh — have been checked accent by accent against the"
                " Wikisource strand each follows; the two satellite pages linked below report the"
                " verdicts, which are per Decalogue rather than per edition. Two results belong"
                " here instead, being facts about the strands rather than about one edition. All"
                " twelve follow their Wikisource strand's chanted verse boundaries ",
                H.bold("without exception"),
                f", whatever else they do. And at ובנך־ובתך, Simanim's Tiqqun and Koren each have"
                f" two separately accented chanted words where the Wikisource p-trad {_ELYON} has"
                " one — two editions exchanging the same maqaf for a conjunctive, and against the"
                " Wikisource strand they otherwise follow.",
            )
        ),
        # The hub is where a reader of the trio first meets a maqaf difference, so it is where the
        # scale that every verdict on all three pages is written against is stated.  Single-sourced
        # in pds and shared verbatim with both satellites; see the guardrail comment at that
        # constant for the self-contradiction on the Koren page that first made it necessary, and
        # for why the convention it originally carried was replaced.
        H.para((pds.MAQAF_IS_THE_LAST_RUNG,)),
        H.para(
            (
                f"Of these four strands, only the p-trad {_ELYON} is ungrammatical — the"
                " verdict above already said so — and the ",
                link("section below", "#why-the-printed-elyon-fails"),
                " dissects its merged opening verse.",
            )
        ),
        # And what the twelve do under the same checker, which is the one thing on this page that
        # is about editions rather than strands. It follows the sentence above rather than
        # preceding it, since its point is that the strand's failure is in books too.
        _transcription_grammar_para(verdicts),
    )


# --------------------------------------------------------------------------- #
# The nesting tables (issues #59, #62)
# --------------------------------------------------------------------------- #
# Two transposed strand tables over the SAME opening region (commandments 1-2, the 51 words
# אנכי...מצותי): one for the printed tradition (pE/pT), one for the manuscript tradition (mE/mT),
# so the reader can compare how each tradition's elyon and taxton verses nest. The layout echoes
# the table in MAM-simple/gh-pages/versification-and-cantillation.html (the source of the analogy,
# not of the text), but with no M/B verse-number rows. Each cell is a first…last range (letters
# + accents; vowels/dagesh/ordinary-meteg stripped), green where a column begins one of the
# strand's verses and red where it ends one. The columns are the finest common subdivision: the
# union of both strands' verse boundaries. Because the p-trad taxton breaks at every boundary
# either m-trad strand uses, BOTH tables end up with the same five columns (widths 9,5,14,17,6);
# what differs is which column edges are true verse starts/stops. Where a verse straddles a column
# edge of the other strand (the m-trad taxton's אנכי...על־פני crossing the elyon's break after
# עבדים) the cell shows a start with no matching stop, or vice versa — the "straddling" that makes
# the m-trad nesting less tidy than the p-trad's clean five-in-one. (M/B numbering is dropped because the two traditions
# split this region differently, so no single verse-number row aligns with the columns; issue #59.)


def _leading_verses(
    version: pd.VersionResult, n_words: int
) -> list[pd.ChantedVerseResult]:
    """The leading chanted verses of ``version`` whose words together cover the first ``n_words``
    (the opening region). The strands are the same word sequence, differing only in vocalization/
    accents, so this splits the shared region consistently for each strand."""
    out: list[pd.ChantedVerseResult] = []
    total = 0
    for cv in version.chanted_verses:
        out.append(cv)
        total += len(cv.words)
        if total >= n_words:
            break
    return out


def _verse_ends(verses: list[pd.ChantedVerseResult]) -> list[int]:
    """The cumulative word-offset at which each verse ends, e.g. ``[9, 51]`` for a 9- then
    42-word pair."""
    ends: list[int] = []
    total = 0
    for v in verses:
        total += len(v.words)
        ends.append(total)
    return ends


def _columns(*verse_lists: list[pd.ChantedVerseResult]) -> list[tuple[int, int]]:
    """Column ``(start, end)`` word-offsets = the segments delimited by the union of every
    strand's verse boundaries, so within a column no strand breaks."""
    cuts = sorted({0, *(e for verses in verse_lists for e in _verse_ends(verses))})
    return list(zip(cuts, cuts[1:]))


def _labeled_row(letter: str, title: str, cells: list[object]) -> object:
    return H.table_row((H.table_header(_abbr(letter, title)), *cells))


def _grad_row(
    letter: str,
    title: str,
    verses: list[pd.ChantedVerseResult],
    columns: list[tuple[int, int]],
) -> object:
    """A strand's schematic gradient bar: one cell per verse, colspanned across the columns that
    verse covers (a verse spanning k columns is one k-wide green→red bar)."""
    ends = _verse_ends(verses)
    spans = list(zip([0, *ends[:-1]], ends))
    cells = []
    for vs, ve in spans:
        k = sum(1 for a, b in columns if vs <= a and b <= ve)
        attr = {"class": "vc-grad", **({"colspan": str(k)} if k > 1 else {})}
        cells.append(H.table_datum("", attr))
    return H.table_row((H.table_header(_abbr(letter, title)), *cells))


def _nesting_table(
    elyon: pd.VersionResult, taxton: pd.VersionResult, n_words: int, *, pfx: str
) -> object:
    """The transposed strand table for one tradition over the opening ``n_words``-word region.
    ``pfx`` ("p" / "m") prefixes the row labels — pE/pT and the gradient rows pe/pt (mE/mT, me/mt) —
    matching the four-strands table's mT/pE convention. Both traditions land on the same columns.
    """
    trad = {"p": "printed", "m": "manuscript"}[pfx]
    e_verses = _leading_verses(elyon, n_words)
    t_verses = _leading_verses(taxton, n_words)
    e_words = tuple(w for cv in e_verses for w in cv.words)
    t_words = tuple(w for cv in t_verses for w in cv.words)
    columns = _columns(e_verses, t_verses)
    e_ends, t_ends = _verse_ends(e_verses), _verse_ends(t_verses)
    e_starts, e_stops = {0, *e_ends[:-1]}, set(e_ends)
    t_starts, t_stops = {0, *t_ends[:-1]}, set(t_ends)
    # Build the two text rows together, column by column: each column's elyon and taxton slices
    # are letter-balanced against each other (issue #201) before rendering, so sibling cells align.
    e_cells: list[object] = []
    t_cells: list[object] = []
    for a, b in columns:
        t_first, t_last, e_first, e_last = _balanced_sides(
            t_words[a:b], e_words[a:b], label=f"{pfx} {a}:{b}"
        )
        e_cells.append(
            _range_cell(e_first, e_last, start=a in e_starts, stop=b in e_stops)
        )
        t_cells.append(
            _range_cell(t_first, t_last, start=a in t_starts, stop=b in t_stops)
        )
    rows = (
        _labeled_row(pfx + "E", f"{trad}-tradition elyon", e_cells),
        _labeled_row(pfx + "T", f"{trad}-tradition taḥton", t_cells),
        _grad_row(
            pfx + "e",
            f"schematic color gradient for the {trad} elyon verse(s)",
            e_verses,
            columns,
        ),
        _grad_row(
            pfx + "t",
            f"schematic color gradient for the {trad} taḥton verse(s)",
            t_verses,
            columns,
        ),
    )
    return H.table(rows, {"class": "strand-table", "dir": "rtl"})


def _finding_section(by_key: dict) -> tuple[object, ...]:
    ex_ms = by_key[("bk-ex", "sk-elyon", "tk-manuscript")]
    ms_cmd1, ms_cmd2 = ex_ms.chanted_verses[0], ex_ms.chanted_verses[1]
    merged = by_key[("bk-ex", "sk-elyon", "tk-printed")].ungrammatical[0]
    n_words = len(merged.words)
    p_table = _nesting_table(
        by_key[("bk-ex", "sk-elyon", "tk-printed")],
        by_key[("bk-ex", "sk-taxton", "tk-printed")],
        n_words,
        pfx="p",
    )
    m_table = _nesting_table(
        ex_ms,
        by_key[("bk-ex", "sk-taxton", "tk-manuscript")],
        n_words,
        pfx="m",
    )
    return (
        H.heading_level_2(
            f"Why the p-trad {_ELYON} fails: the merged first verse",
            {"id": "why-the-printed-elyon-fails"},
        ),
        H.para(
            (
                "As the ",
                link("four-strands table above", "#four-strands"),
                f" laid out, in the m-trad {_ELYON} the first commandment אנכי…עבדים is its"
                " own chanted verse, and לא יהיה לך אלהים אחרים begins the next — two"
                " separate verses, ",
                H.bold("both of which are grammatical"),
                ". The p-trad instead merges the first two commandments into a single"
                " verse. That one"
                " merged verse is what the grammar rejects. Shown stripped to letters and"
                f" accents and divided at the p-trad {_TAHTON}'s verse boundaries — one p-trad"
                f" {_ELYON} verse (pE) spanning the five ordinary p-trad {_TAHTON} verses (pT)"
                " it merges:",
            )
        ),
        p_table,
        H.para(
            (
                "The single ",
                _ROM_ETNAHTA,
                " falls at לשנאי, leaving a first half crowded with a ",
                _ROM_SEGOLTA,
                " plus three separate ",
                _ROM_REVIA,
                " domains (at ",
                *H.bdi_multi("עבדים", "על־פני", "לארץ"),
                "); the prose grammar cannot build it and returns a ",
                H.code("pashta_phrase"),
                " error — the same failure, at the same structural point, in both Decalogues.",
            )
        ),
        H.para(
            (
                "The cause is the merged ",
                H.bold("structure"),
                f", not sheer length: Deuteronomy's p-trad {_ELYON} Sabbath verse runs 55"
                " chanted words and parses clean, while this merged verse (51) does not. Keeping"
                " the two commandments as the m-trad's two separate verses (",
                f"{len(ms_cmd1.words)} and {len(ms_cmd2.words)})",
                " is exactly what lets them parse.",
            )
        ),
        H.heading_level_3("A tidier nesting — until you scrutinize it"),
        H.para(
            (
                f"It is tempting to call the p-trad's arrangement the neater one. Its five"
                f" {_TAHTON} verses nest perfectly inside a single {_ELYON} verse — a clean"
                " five-in-one — whereas the m-trad divides the very same chanted words into ",
                H.bold("two"),
                f" {_ELYON} verses and ",
                H.bold("four"),
                f" {_TAHTON} verses that do not nest cleanly at all: the m-trad",
                f" {_TAHTON}'s opening verse אנכי…על־פני straddles the {_ELYON}'s break"
                f" after עבדים, so neither strand's verses sit wholly inside the other's. In"
                " the gradient"
                " bars below, mE's first break lands inside mT's first verse, which runs on to"
                " על־פני — that is the straddle:",
            )
        ),
        m_table,
        H.para(
            (
                "But the p-trad's tidiness is bought with an ungrammatical cantillation — the"
                " very one dissected above. Once you see the accents that buy the five-in-one,"
                " its neatness evaporates. This is ",
                H.bold("not"),
                " to say the tidier nesting could not have been cantillated grammatically;"
                " perhaps some other accentuation would have carried it off. That is a"
                " theoretical question I am not prepared to settle here.",
            )
        ),
    )


def _provenance_section(source: dict) -> tuple[object, ...]:
    prov = source.get("provenance", {})
    oldid = prov.get("oldid")
    ts = prov.get("revision_timestamp", "")
    return (
        H.heading_level_2("Source"),
        H.para(
            (
                f"All eight strands (two books × {_TAHTON}/{_ELYON} × m-trad/p-trad) are"
                " taken from the Wikisource base page ",
                link("עשרת הדברות בסיס/טעמים", _SOURCE_URL),
                f" (revision {oldid}, {ts[:10]}), which every p-trad-vs-m-trad comparison"
                " table there transcludes. A handful of wiki templates are resolved to plain"
                " pointed text for accent-grammar parsing (",
                _ROM_LEGARMEH,
                " and ",
                _ROM_PASEQ,
                " both conflated down to a Unicode PASEQ, ketiv dropped from ketiv-qere, setumah"
                " and petuḥah divisions dropped); the chanted"
                " verses are split at ",
                _ROM_SOF_PASUQ,
                ".",
            )
        ),
        H.para(
            (
                "See also ",
                link(
                    "this document on the Decalogues in the Simanim Tiqqun",
                    "printed-decalogue-simanim.html",
                ),
                f" — its main Decalogues follow the p-trad {_ELYON} and its appendix"
                f" Decalogues the p-trad {_TAHTON}. It follows the p-trad's chanted verse"
                " boundaries without exception, and its Deuteronomy main Decalogue follows the"
                " p-trad in every accent; what it does not follow is every cantillation detail"
                " elsewhere — most consequentially at the Shabbat commandment, where its"
                " Deuteronomy appendix Decalogue has the m-trad accents. That page also covers"
                " the separately published Simanim Tanakh, which is m-trad in all four of its"
                " Decalogues: the same publishing house, the opposite tradition.",
            )
        ),
        # GUARDRAIL (2026-07-25 claim audit, finding 3). This paragraph used to say "Three of its
        # four follow their strand in every accent; the fourth differs only in how it divides two
        # chanted words" -- the Koren page's own summary, repeated here, and wrong on the count:
        # TWO of the four have a maqaf difference, the Exodus appendix splitting two compounds and
        # the Deuteronomy appendix joining one. Keep the count right and keep it on the one scale
        # stated above -- the four differences ARE differences, at its bottom rung. What must not
        # come back is the intermediate wording, which fixed the count by declaring a maqaf
        # difference not to be a difference at all.
        H.para(
            (
                "See also ",
                link(
                    "this document on the Decalogues in the Koren Tanakh",
                    "printed-decalogue-koren.html",
                ),
                f" — it has the p-trad {_TAHTON} in its main Decalogues and the p-trad"
                f" {_ELYON} in its appendix ones, in Exodus and Deuteronomy alike. Two of its four"
                " Decalogues match their Wikisource strand mark for mark; the other two differ"
                " from theirs at the last rung only, where a maqaf on one side faces a"
                " conjunctive on the other.",
            )
        ),
        # The ובנך־ובתך sentence above says two editions have a conjunctive where the Wikisource
        # p-trad עליון has a maqaf, and stops there -- which strand is right is not this page's
        # question and is not decided here. It is decided, or at least argued, in MAM-basics
        # issue #208, and the page linked here is only a record of the editions that issue cites.
        H.para(
            (
                "See also ",
                link(
                    "this record of the printed editions cited at ובנך",
                    _UVINKHA_PAGE,
                ),
                " — the one word above at which two editions and the Wikisource p-trad"
                f" {_ELYON} disagree. Whether Wikisource or the editions have it right is"
                " asked at MAM-basics issue #208, and that page holds the editions the"
                " issue's reply cites, with a crop of each page where one has been taken.",
            )
        ),
    )


# --------------------------------------------------------------------------- #
# Appendix: the grammaticality-irrelevant תחתון differences
# --------------------------------------------------------------------------- #
# Spun out of the verdict paragraph's parenthetical (which now just links here): a plain-prose
# catalogue of how the p-trad and m-trad תחתון differ WITHOUT touching grammaticality (several DO
# change the parse tree — e.g. a disjunctive-rank accent swap — but leave both strands well-formed).
# Both strands are grammatical everywhere, so none of this bears on the page's question; it is here only
# to substantiate the verdict's point that these differences never cost either strand its
# grammaticality. The prose is hand-written documentary colour, not part of the live grammaticality
# result; but the Hebrew it displays for the Deuteronomy differences — where the תחתון cantillation
# differences cluster, in the Sabbath commandment — is pulled live from the data and reduced, again
# live, to just the stretch the two strands accent differently (_sabbath_diff_table), so it can't
# drift from the text the page grammar-checks. The verse-boundary difference (p-trad first verse
# ending at מבית עבדים) and the boundary accents it drags along are the verdict's own point and are
# deliberately NOT repeated here.

# The prose books' conjunctive accents (Yeivin ITM §194, encoded once in mb_cmn.hebrew_accents);
# every other accent is disjunctive. Used only to verify, live, that each displayed
# line really does end on a disjunctive.
_PROSE_CONJUNCTIVES = set(ha.CONJUNCTIVES_BCC["cant-sys-prose"])
_ACCENT_LO = ord("\N{HEBREW ACCENT ETNAHTA}")  # U+0591, first accent
_ACCENT_HI = ord("\N{HEBREW ACCENT ZINOR}")  # U+05AE, last (meteg U+05BD is excluded)

# The three shared boundaries at which the differing stretch is broken into aligned line-pairs.
# Each is a letter skeleton (cf. _SPAN_COLUMNS) that ends a line in BOTH strands and carries a
# disjunctive accent in both — the only kind of point where a break keeps the m-trad and p-trad
# lines aligned. These three (of the stretch's shared disjunctive boundaries) give three ~even
# pairs. _split_into_lines asserts each lands, in order, and is genuinely disjunctive, so any drift
# in the vendored accents fails the build instead of silently mis-breaking.
_SABBATH_LINE_ENDS: tuple[str, ...] = ("כלמלאכה", "ועבדךואמתך", "וכלבהמתך")


def _ends_on_disjunctive(word: str) -> bool:
    """True if a pointed prose word's accent is disjunctive: it has an accent in the
    U+0591..U+05AE block that is not one of the prose conjunctives (Yeivin ITM §194)."""
    return any(
        _ACCENT_LO <= ord(ch) <= _ACCENT_HI and ch not in _PROSE_CONJUNCTIVES
        for ch in word
    )


def _differing_span(
    m_words: list[str], p_words: list[str]
) -> tuple[list[str], list[str]]:
    """The (m, p) sub-lists bracketing every difference between the two strands: the shared,
    byte-identical prefix and suffix are stripped, leaving the contiguous stretch where the strands
    differ. (They share the same letters, so any difference is an accent or a maqaf/paseq mark;
    the identical head and tail are common context we omit.)"""
    head = 0
    while head < min(len(m_words), len(p_words)) and m_words[head] == p_words[head]:
        head += 1
    tail = 0
    while (
        tail < min(len(m_words), len(p_words)) - head
        and m_words[-1 - tail] == p_words[-1 - tail]
    ):
        tail += 1
    return m_words[head : len(m_words) - tail], p_words[head : len(p_words) - tail]


def _split_into_lines(words: list[str], line_ends: tuple[str, ...]) -> list[list[str]]:
    """Split ``words`` into the successive line groups ending at each skeleton in ``line_ends``.
    Asserts every break lands, in order, consumes the whole stretch, and ends on a word that really
    carries a disjunctive accent — so any drift in the vendored words/accents fails the build.
    """
    lines: list[list[str]] = []
    cur: list[str] = []
    pending = list(line_ends)
    for w in words:
        cur.append(w)
        if pending and pds.base_skeleton(w) == pending[0]:
            if not _ends_on_disjunctive(w):
                raise AssertionError(
                    f"line-end {w!r} no longer carries a disjunctive accent -- readings drifted"
                )
            lines.append(cur)
            cur, pending = [], pending[1:]
    if cur or pending:
        raise AssertionError(
            f"sabbath line split: leftover words {cur!r} / unconsumed line-ends {pending!r}"
            " -- the vendored readings drifted"
        )
    return lines


def _diff_row(label: str, words: list[str]) -> object:
    """One table row: a bold m-trad/p-trad label cell, then the strand's line of words as a
    right-aligned (dir=rtl) hbo cell so the three pairs' Hebrew all line up flush-right. Each word
    is shown in the classic letters-plus-accents form (_strip_pointing: vowels, dagesh, and
    mid-verse meteg dropped), so only the cantillation differences remain -- the vowel-pointing
    differences are catalogued separately in the bullets below."""
    line = " ".join(_strip_pointing(w) for w in words)
    return H.table_row(
        (
            H.table_datum(H.bold(label)),
            H.table_datum(hbo(line), {"dir": "rtl"}),
        )
    )


def _sabbath_diff_table(results: list[pd.VersionResult]) -> object:
    """The differing stretch of the two Deuteronomy תחתון Sabbath strands, as a table of three
    line-pairs (an m-trad row directly above its p-trad row), each line a short run of words ending
    on a shared disjunctive; the head and tail the two strands share verbatim are omitted. The table
    picks up the shared centered layout and the lang="hbo" font; its lone class turns OFF the shared
    odd-row zebra, which -- the rows alternating m-trad/p-trad -- tinted exactly the three m-trad
    rows and so read as if the stripe meant "m-trad" (issue #65, finding C3). Span, breaks, and the
    disjunctive check are all derived live from the data, so nothing here can drift from the
    grammar-checked text."""
    m_span, p_span = _differing_span(
        pdt.sabbath_verse_words(results, "manuscript"),
        pdt.sabbath_verse_words(results, "printed"),
    )
    m_lines = _split_into_lines(m_span, _SABBATH_LINE_ENDS)
    p_lines = _split_into_lines(p_span, _SABBATH_LINE_ENDS)
    rows: list[object] = []
    for m_line, p_line in zip(m_lines, p_lines):
        rows.append(_diff_row("m-trad", m_line))
        rows.append(_diff_row("p-trad", p_line))
    return H.table(tuple(rows), {"class": "printed-decalogue-sabbath-diff"})


# The two strands' one vocalization difference, stacked as a table rather than run together in
# prose (Ben, 2026-07-25). The prose form put the two pointed words side by side, each followed by
# an English parenthetical: two RTL words on one line separated only by neutral characters, which
# BiDi is free to reorder, so a reader could not be sure which vowel went with which tradition.
# Stacked, the two forms sit one directly above the other and the vowel is comparable at a glance.
# Name the word bare -- תרצח, not לא תרצח: the two words are separately accented rather than one
# maqaf compound, and only this one differs, so the לא bought nothing but a second RTL word.
_VOWEL_DIFF_ROWS: tuple[tuple[str, str, str], ...] = (
    ("m-trad", "תִּרְצָ֖ח", _QAMATS),
    ("p-trad", "תִּרְצַ֖ח", _PATAX),
)


def _vowel_diff_table() -> object:
    """The one difference of vocalization, as an m-trad row above its p-trad row: label, the
    pointed word, and the vowel's name. The mirror image of ``_diff_row`` above, which strips the
    pointing off to leave the cantillation bare -- here the pointing IS the difference, and the
    two rows carry the same tipexa."""
    rows = tuple(
        H.table_row(
            (
                H.table_datum(H.bold(label)),
                H.table_datum(hbo(word), {"dir": "rtl"}),
                H.table_datum(vowel),
            )
        )
        for label, word, vowel in _VOWEL_DIFF_ROWS
    )
    return H.table(rows, {"class": "printed-decalogue-vowel-diff"})


def _pausal_table(results: list[pd.VersionResult]) -> object:
    """The pausal alternation at the appendix's two other Decalogue words, as four rows -- על־פני
    then מתחת, each strand's row labelled with the strand rather than a tradition, because these
    two words differ by strand and not by tradition (which ``pds.resolve_pausal`` checks against
    all eight readings before handing back a single form).

    Every cell is derived: the pointed word comes from the vendored data and its vowel and accent
    are read off its marks, so the table cannot claim a vowel or an accent the text does not have.
    Vowel names render plain and accent names italic, matching the vocalization table above and the
    page's prose respectively."""
    rows = tuple(
        H.table_row(
            (
                H.table_datum(H.bold(f.strand)),
                H.table_datum(hbo(f.word), {"dir": "rtl"}),
                H.table_datum(f.vowel),
                H.table_datum(_ROM_NODE_BY_NAME[f.accent]),
            )
        )
        for f in pds.resolve_pausal(results)
    )
    return H.table(rows, {"class": "printed-decalogue-pausal"})


# Why the appendix explains the תרצח vowel instead of just recording it (Ben, 2026-07-25). The
# qamats/patax pair is not a spelling accident: it is the pausal alternation, and the Decalogue
# shows that alternation working ordinarily at two OTHER words, על־פני and מתחת, where the strands'
# own accents differ and the vowel follows them. Saying so is what makes תרצח legible as the odd
# case -- same accent in both traditions, so the accent cannot be what decides the vowel.
#
# Two rules for editing this passage.
#
# (1) GLOSS THE IDEA ONCE, THEN JUST USE THE NAMES. "Pausal" and "contextual" are the standard
# terms and a reader of a published page has not met them, so the opening sentence says in plain
# words what the alternation is ("one vowel where the reading pauses and another where it runs
# on"). After that, write "the pausal form" and leave it at that. An earlier draft glossed each
# name in apposition as it arrived -- "the pause form, the pausal one" -- which Ben cut as weird
# and unnecessary (2026-07-25): once the idea is glossed, the name needs no second explanation.
#
# (1a) NO EMPHASIS WORD THAT GESTURES AT A CONTRAST THE READER HAS NOT REACHED. Three cuts on
# 2026-07-25 shared one cause: "outright", and "the two strands REALLY DO accent those words
# differently", were both leaning on the תרצח paragraph that comes AFTER them -- an emphasis
# whose contrast is still in the future reads as noise, and this is the standing no-previews rule
# in miniature. State the two words' case flatly; let the contrast land when תרצח arrives.
#
# (2) EVERY FACTUAL CLAIM IS DERIVED OR PINNED. The vowels and accents in the table come off the
# vendored marks (pds.resolve_pausal), which additionally checks all eight readings agree at both
# words -- the "by strand, not by tradition" claim. The prose's claims about תרצח in the עליון are
# pinned by pds.check_tirtsax, called below for exactly that reason: a 2026-07-25 claim audit found
# this appendix asserting things its own tables contradicted, and prose about a fourth word is
# precisely where that recurs. Do not add a further claim about the pointing here without a pin.
# The citation, in the trio's bare form -- "Yeivin §199", matching "(Yeivin §246)" on the
# almost-errors page. The section is §199 of Yeivin's *Introduction to the Tiberian Masorah*, whose
# §197 supplies the ranking the closing sentence leans on (tipexa sits one grade below etnaxta and
# silluq); §199 is where the pausal/contextual rule and its exceptions are stated.
#
# NAME BOTH ACCENTS THERE, DON'T SHORTEN TO ONE. Yeivin's §197 puts silluq and etnaxta in the SAME
# grade (his grade I), so "weaker than etnaxta" alone would set the same threshold but would imply
# a ranking between the two that he does not make. It also replaced a "weaker than those two",
# which made the reader hold two accents in mind from an earlier paragraph (Ben, 2026-07-25). The
# order matches the rule as first stated above, etnaxta before silluq, so the back-reference is
# unmistakable.
#
# "CONTEXTUAL" IS YEIVIN'S OWN TERM, NOT A COINAGE OF THIS PAGE (asked 2026-07-25; recorded so it
# is not asked twice). §199 states the rule with both words -- "contextual forms are used with the
# other accents" -- and ITM uses the pair elsewhere too ("contextual or pausal situations", and
# "contextual and pausal forms" among the topics early grammarians took from the Masorah). So the
# prose keeps "contextual" rather than falling back on a descriptive "non-pausal".
_PAUSAL_CITE = "Yeivin §199"


def _pausal_paras(results: list[pd.VersionResult]) -> tuple[object, ...]:
    # Not a display value -- called for its assertions, which stand behind the prose below.
    pds.check_tirtsax(results)
    return (
        H.para(
            (
                "Those two vowels are the two halves of a pausal alternation: a great many Hebrew"
                " words take one vowel where the reading pauses and another where it runs on. The"
                f" general rule ({_PAUSAL_CITE}) is that the pausal form goes with an ",
                _ROM_ETNAHTA,
                " or a ",
                _ROM_SILLUQ,
                ", and the contextual form with every other accent.",
            )
        ),
        H.para(
            (
                "Two other chanted words of the Decalogue alternate the same way, and at both of them what"
                f" decides is {_TAHTON} against {_ELYON}, not p-trad against m-trad: all eight"
                " strands have the pausal"
                f" {_QAMATS} in the {_TAHTON} and the contextual {_PATAX} in the {_ELYON}. There the"
                " rule accounts for the vowel, because the two strands accent"
                f" those two differently. The {_TAHTON} ends a chanted verse at על־פני and puts"
                f" its verse's main break at מתחת; the {_ELYON} runs on through both. In each pair"
                f" below the {_TAHTON} comes first:",
            )
        ),
        _pausal_table(results),
        H.para(
            (
                "With תרצח, we have that same alternation, this time splitting the two"
                " traditions. In the ",
                _ELYON,
                " it is the second and last chanted word of the chanted verse ",
                H.bdi("לא תרצח"),
                ", so it has a ",
                _ROM_SILLUQ,
                f" and both traditions have the pausal {_QAMATS} on it. In the {_TAHTON} it sits"
                " mid-verse under a ",
                _ROM_TIPEHA,
                f", which by the rule above should take the contextual {_PATAX} — and that is what"
                f" the p-trad has, while the m-trad keeps the pausal {_QAMATS}. A pausal vowel under"
                " a disjunctive weaker than either ",
                _ROM_ETNAHTA,
                " or ",
                _ROM_SILLUQ,
                " is common enough for Yeivin to catalogue it; what the two traditions differ over"
                " here is only whether to do it at this chanted word.",
            )
        ),
    )


def _appendix_section(results: list[pd.VersionResult]) -> tuple[object, ...]:
    # Every number in this appendix is DERIVED, and the derivation raises on drift: this one call
    # re-counts the whole Deuteronomy divergence set from the vendored words and fails the build
    # unless it still decomposes as printed_decalogue_taxton_diff pins it (12 = 4 boundary + 7
    # Sabbath + 1 vocalization), and unless the seven really do all fall inside the Sabbath chanted
    # verse. That last check is what licenses the prose's "a single stretch".
    counts = pdt.dt_taxton_diff_counts(results)
    return (
        H.heading_level_2(
            f"Appendix: how the two {_TAHTON} strands differ",
            {"id": _TAHTON_DETAILS_ID},
        ),
        H.para(
            (
                f"Both {_TAHTON} strands are grammatical, so the differences below do not"
                " bear on the grammaticality question this page asks, though several of"
                " these differences do change the accent-grammar tree. I gather these"
                " differences here only to make concrete the verdict's point that the"
                " strands differ in ways that never cost either strand grammaticality."
                " The one structural difference — the p-trad ending its first verse at"
                " מבית עבדים, and the boundary accents on ",
                # The four boundary words come from printed_decalogue_taxton_diff, which also
                # classifies a difference site as "boundary" by matching these skeletons -- so the
                # words named here and the four excluded from the counts below cannot come apart.
                *H.bdi_multi(*pdt.BOUNDARY_SKELETONS),
                " that follow from it — is the verdict's point and is not repeated here.",
            )
        ),
        H.para(
            (
                "In Exodus, those four chanted words aside, the two strands part at exactly one more,"
                " the vocalization of תרצח:",
            )
        ),
        _vowel_diff_table(),
        H.para(
            (
                "Both have the same ",
                _ROM_TIPEHA,
                "; only the vowel differs.",
            )
        ),
        *_pausal_paras(results),
        # GUARDRAIL (2026-07-25 claim audit, finding 1). This paragraph used to open "Deuteronomy
        # differs in more ways. Three are differences of cantillation ... and all three fall within
        # a single stretch of the Sabbath commandment" -- and the table rendered directly beneath it
        # displays SEVEN chanted-word-level differences in that stretch, so the sentence was false as
        # written. "Three" was never a count of differences: it is the number of DISJUNCTIVELY
        # ACCENTED chanted words the table's line-pairs end on, the Shabbat signal-word shorthand both
        # satellite pages correctly describe as "not the only chanted words the two traditions accent
        # differently". Two rules follow. Never state a bare count here that the table can be read
        # against without saying what it counts; and never let this page's "three" imply the table
        # shows three rows' worth of difference. Every number below is now derived (see the counts
        # call above), so the failure mode left is a WORDING one -- keep the scopes explicit.
        #
        # The paragraph now opens by RESTATING WHAT THE SECTION IS COMPARING before switching books
        # (Ben, 2026-07-25). Its old opener, a bare "Deuteronomy differs in more ways", assumed the
        # reader still had "p-trad against m-trad, within the תחתון" in mind -- and by this point
        # three paragraphs and a table of the pausal aside sit between that framing and here, with
        # the aside's own comparison running along the OTHER axis (תחתון against עליון). Naming both
        # the axis and the book at the hand-off costs a sentence and removes the ambiguity. If the
        # aside above is ever moved or dropped, this restatement should stay: the appendix's two
        # halves are far enough apart to want it regardless.
        H.para(
            (
                f"So that is how the p-trad and m-trad of the {_TAHTON} differ in Exodus. In"
                " Deuteronomy, they differ more than in Exodus. Over the whole Decalogue the two"
                " strands part at ",
                H.bold(str(counts["total"])),
                " chanted words: the four boundary words already discussed above, one that"
                " differs in vocalization alone (the same תרצח, noted again below), and ",
                H.bold(str(counts["sabbath"])),
                " that all fall within a single stretch of the Sabbath commandment. Those"
                f" {counts['sabbath']} are differences of cantillation, so unlike the Exodus"
                " vowel-swap they give the two strands genuinely different accent-grammar trees."
                " Below is that stretch — the run of chanted words the two strands accent differently,"
                " everything"
                " before and after it being identical — shown in each strand, m-trad above p-trad,"
                " stripped to letters and accents, each line ending on a disjunctive accent. The ",
                H.bold(str(len(_SABBATH_LINE_ENDS))),
                " chanted words those lines end on are the Shabbat commandment's signal words — a"
                " shorthand for the stretch, not the whole of it:",
            )
        ),
        # Just the differing stretch of the Sabbath verse, pulled and reduced live from the data (so
        # it can never drift from the accentuation the rest of the page grammar-checks), as a table
        # of three line-pairs, m-trad above p-trad, each line ending on a shared disjunctive.
        _sabbath_diff_table(results),
        H.para(
            (
                # "X / Y" is two adjacent RTL words separated only by a neutral slash, so both
                # are <bdi>-isolated (around the lang="hbo" span) to keep the pair from
                # rendering reversed. Lone hbo forms elsewhere, bounded by English, need no bdi.
                "The one difference outside that stretch is purely vocalization —"
                " vowel-pointing, not cantillation: the same ",
                H.bdi(hbo("תִּרְצָ֖ח")),
                " / ",
                H.bdi(hbo("תִּרְצַ֖ח")),
                " split as in Exodus.",
            )
        ),
        # An aside (issue #52 follow-up, corrected by issue #66): the p-trad תחתון Sabbath
        # cantillation dissected just above also turns up in CTR, the web edition my CTR review
        # judges the weirdest, and possibly worst, on the web. The aside exists for that quip.
        # Its "on the web" scoping is load-bearing, not incidental: it deliberately makes no claim
        # about which PRINT editions have the cantillation. Koren has it too, in its own
        # Deuteronomy (issue #66); an earlier draft asserted a "gap in Koren and Simanim" that was
        # simply false for Koren. Keep any rewrite of the aside scoped to the web.
        *_chabad_aside(),
    )


# --------------------------------------------------------------------------- #
# The CTR aside: a p-trad Bible on the web (see the guardrail comment at the call site above)
#
# Name BOTH signal words when placing CTR's Deuteronomy among the four strands. An earlier draft
# credited it with "the characteristic opening verse of the p-trad taxton", which contradicts this
# page's own signal-pair section: the opening verse ends at עבדים, and there the p-trad taxton and
# the m-trad elyon are word for word identical. It takes על־פני too -- one signal word never
# places a text among the four strands.
# --------------------------------------------------------------------------- #
def _chabad_aside() -> tuple[object, ...]:
    return (
        H.heading_level_3("A p-trad Bible on the web: CTR"),
        H.para(
            (
                "Possibly the only p-trad Bible on the web is ",
                link("CTR", _CHABAD_DT5_URL),
                ": a web version of The Complete Tanach with Rashi, served from Chabad.org."
                f" Its Deuteronomy 5 has not only the p-trad {_TAHTON}'s signal pair (chanted"
                " verses ending at both עבדים and על־פני), but also the p-trad"
                f" {_TAHTON} accents in the Sabbath commandment."
                f" Its whole Decalogue, in fact, is the p-trad {_TAHTON} as Wikisource"
                " defines it, down to all but one conjunctive accent.",
            )
        ),
        # CTR's Exodus (issue #69, Result 11). It stays an aside, deliberately: CTR is a curiosity
        # beside the twelve hand-transcribed Decalogues, not a thirteenth, and no claim on this
        # page or its satellites rests on it. Say the division in CHANTED VERSES only -- an earlier
        # draft called it "the ordinary numbered-verse division", which is both off-subject (these
        # pages are about chanted verse structure, never numbering) and wrong (Ex 20:13 holds four
        # sof pasuqs, which is where three of the sixteen come from).
        #
        # And do NOT call CTR's sixteen spans chanted verses (Ben, 2026-07-24).  A chanted verse
        # needs a SILLUQ, and seven of the sixteen have none, so they are SOF PASUQ SPANS -- a
        # span that, in Ben's words, "doesn't even seem to be trying to obey the rules of
        # cantillation".  The draft this replaced said "the word-accents are the elyon's, but the
        # chanted verse division belongs to neither strand", which invites the objection that
        # sinks it: silluq IS a word-accent, so a real re-division would have MOVED the silluqs
        # and the two halves could not come apart.  They come apart here only because CTR moved
        # nothing.  Its sixteen sof pasuqs are the exact UNION of the two strands' boundaries
        # (elyon 9 + taxton 13, sharing 6), laid over an untouched elyon accent stream: at the 9
        # elyon boundaries CTR has the elyon's silluq, and at the 7 taxton-only ones it has no
        # silluq at all -- the mark stands after the elyon's own mid-verse disjunctive (revia x3,
        # atnaxta, revia, segolta, zaqef, on עבדים / על־פני / לארץ / לשנאי / לקדשו / כל־מלאכתך /
        # בשעריך).  Pinned by tests/test_ctr_decalogue.py; ctr_decalogue.sof_pasuq_spans is named
        # for this.
        H.para(
            (
                "Its Exodus 20 is stranger. The accents are the ",
                _ELYON,
                "'s throughout, ",
                _ROM_SILLUQ,
                " included — but it has a ",
                _ROM_SOF_PASUQ,
                " at every boundary of both strands: the ",
                _ELYON,
                "'s nine and the ",
                _TAHTON,
                "'s thirteen, sixteen marks in all. Seven of the sixteen are the ",
                _TAHTON,
                "'s alone, and at those the ",
                _ELYON,
                " has no ",
                _ROM_SILLUQ,
                ", and neither does CTR: the seven chanted words before those marks have four ",
                _ROM_REVIA,
                ", an ",
                _ROM_ETNAHTA,
                ", a ",
                _ROM_SEGOLTA,
                ", and a ",
                _ROM_ZAQEF_QATAN,
                ". What those seven close could be called a ",
                _ROM_SOF_PASUQ,
                " span, but it could not be called a chanted verse. CTR's Exodus is the ",
                _ELYON,
                "'s nine chanted verses with the ",
                _TAHTON,
                "'s ",
                _ROM_SOF_PASUQ,
                " marks added — sixteen ",
                _ROM_SOF_PASUQ,
                " spans.",
            )
        ),
        H.para(
            (
                *["For more on CTR: see my ", link("review", _CTR_REVIEW_URL), ","],
                " which calls it"
                " “certainly the weirdest Hebrew Bible on the web, and possibly the worst.”",
            )
        ),
    )


def render_body_contents(
    results: list[pd.VersionResult],
    source: dict,
    verdicts: list[tp.TranscriptionResult],
) -> tuple[object, ...]:
    by_key = _by_key(results)
    readings = pds.resolve_readings(results)
    return (
        *_intro(),
        *_verdict_section(by_key),
        *_four_strands_section(readings, verdicts),
        *_finding_section(by_key),
        *_provenance_section(source),
        *_appendix_section(results),
    )


def run(args: argparse.Namespace) -> None:
    source = pd.load_source(args.source)
    results = pd.check_all(source)
    verdicts = tp.check_all(results)

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(results, source, verdicts),
        write_ctx=H.WriteCtx(
            title=REPORT_TITLE,
            path=str(html_out),
            centered=True,
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    n_bad = sum(len(vr.ungrammatical) for vr in results)
    print(f"HTML: {html_out} ({len(results)} versions, {n_bad} ungrammatical)")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
