r"""Generate gh-pages/accgram/wlc-chanted-word-residue.html -- WLC's unnamed accent pairs.

A SNEAK PEEK, AND DELIBERATELY UNLINKED.  Ben asked for this on 2026-08-03: the residue that
``chanted_word_accents`` measures for WLC, on a page of its own, reachable only by its URL.
Nothing links to it -- not ``gh-pages/index.html``, which is hand-written and lists seven pages,
and not ``goerwitz.html``, whose ungrammatical-verse report is where a WLC accent problem is
read today.  Folding it into that report is a decision nobody has made and may never make;
linking to it from there is the smaller step that may come first.  Until then the page says
what it is at the top, so a reader who has the URL cannot mistake it for a verdict.

WHAT IT SHOWS.  ``chanted_word_accents`` counts every chanted word -- an atom, or a whole maqaf
compound -- with two or more accent TOKENS, and names each pair with the section of Yeivin's ITM
prose inventory that covers it.  ``NAMED_TOKEN_SEQUENCES`` is that inventory reduced to the token
sequences the checker's whitelist is keyed on.  The residue is what is left: the pairs no section
names.  MAM's residue is in the survey JSON as ``mam_residue`` and is a claim about the
accentuation.  WLC's residue is a claim about the Westminster transcription of the Leningrad
Codex, which is a different and smaller thing, and saying which is which is most of what the
prose here does.

NO COUNT IS WRITTEN DOWN HERE.  Every figure the page prints is spliced from the survey by
``_counts``, and both residues shrink whenever a section joins the inventory -- ITM §256 took
the qadma darga rows out on 2026-08-03, and this docstring went on quoting the sizes from before
it, silently, because a number in a docstring has nothing under it.  Read the sizes off the
regenerated page, or off out/accgram/chanted-word-accents.json.

THE MAM COLUMN HAS ONE CAVEAT, AND IT IS DERIVED RATHER THAN PINNED TO A VERSE.  Where WLC's
sequence has a legarmeh and its MAM counterpart does not, ``_mam_cell`` marks the MAM cell and
``_stroke_caveat`` says why below the table: WLC has the Unicode PASEQ on the chanted word, and
MAM has the same Unicode PASEQ standing apart from it with a space on each side, so the scanner
reads a legarmeh in the one and not in the other.  That is #215, whose fix Ben sequenced before
Phase 4 of wlc-utils/doc/PLAN-two-accents-on-one-chanted-word.md; when it lands the marker and
the paragraph drop out of the page on their own, the way ``_accounted_for``'s groups do.  Hence
also what ``pin_claims`` asserts here -- the shape of the argument, that the scanner reads no
legarmeh anywhere in MAM, rather than a count of marked rows that a fix would falsify.  The
mechanism was checked against MAM-parsed-plus on 2026-08-04: at Nehemiah 8:7 the stroke is a
``מ:לגרמיה-2`` template, which MAM-simple renders as a vel of its own, and WLC 4.22's vel there
has the U+05C0 attached to the word.

NOTHING HERE IS A VERDICT, and the page has no way to make one.  ``classify_verse`` already
writes an additive ``chanted_word_accents`` field beside each verse's ``status`` and ``tree``,
and Ben ruled on 2026-08-03 that MAM's divergences from Yeivin and Breuer keep being recorded
and stay grammatical.  The ``Verdict today`` column reads the verdict ``run-prose`` has already
written, so a reader can see which rows stand in verses it calls clean and which stand in verses
it already calls ungrammatical -- and that the ungrammatical ones are ungrammatical for reasons
that have nothing to do with having two accents.

THE JSON IS NOT WRITTEN HERE.  ``survey-chanted-word-accents`` is the only writer of
``out/accgram/chanted-word-accents.json``, restored to that role when the earlier
chanted-word-accents page was withdrawn on 2026-07-29.  This page calls ``build_survey`` and
renders it, so page and data are derived from one function and cannot disagree; what it must not
do is give that file a second writer.

Run via ``main_accgram.py generate-html-wlc-chanted-word-residue``, or as part of
``generate-html``.  ``run-prose`` must have run first, for the verdict column.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from accgram import chanted_word_accents as cwa
from accgram import rtms_report
from accgram.almost_errors_html_shared import (
    hbo,
    itm,
    link,
    ref_abbrev,
    text_para,
)
from accgram.printed_decalogue_strands import (
    ROM_DARGA,
    ROM_ETNAHTA,
    ROM_GERESH,
    ROM_GERSHAYIM,
    ROM_LEGARMEH,
    ROM_MAHAPAKH,
    ROM_MERKHA,
    ROM_MUNAX,
    ROM_PASHTA,
    ROM_QADMA,
    ROM_REVIA,
    ROM_SILLUQ,
    ROM_TELISHA_GEDOLAH,
    ROM_TEVIR,
    ROM_TIPEHA,
    ROM_ZAQEF_QATAN,
)
from accgram.uni_to_marks import is_accent
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import provenance
from py_html import wlc_utils_html as H

import wlc_paths

PAGE_TITLE = "Two Accents on One Chanted Word: What WLC Has Left Over"
_WIDTH_CLASS = "goerwitz-tms-width-limited"
_TABLE_CLASS = "centered-table accent-pair-table"

# A cell holding Hebrew says so, and right-justifies as a consequence of having said it.
_HEBREW_CELL = {"dir": "rtl"}

# The four token sequences that pair a telisha gedolah with a geresh-family mark, in either
# order.  Derived from the pair rather than listed by verse, so the count below is measured.
# These are the five words ``lexical_validation`` already whitelists as a legitimate same-letter
# pair, set out in the telisha gedolah exhibit of almost-errors.html.
_TELISHA_GERESH_PAIRS = frozenset(
    (
        "geresh telishagedola",
        "telishagedola geresh",
        "gershayim telishagedola",
        "telishagedola gershayim",
    )
)

# THE STROKE MARKER, and the hover that has to stand on its own for a reader who never reaches
# the note.  A dagger rather than a hover alone: the caveat is what keeps the MAM cell from being
# read as "MAM has nothing there", which is too much to hang on a mouse.
_STROKE_MARK = "†"
_STROKE_HOVER = (
    "MAM has the same Unicode PASEQ, standing apart from the word rather than on it;"
    " see the note below the table"
)

# How many of the inventory's configurations the opening sentence names before it counts the
# rest ("a munax before a zaqef, a mahapakh before a pashta, an azla before a geresh, and N
# more").  Spliced rather than written into the prose, because ITM §256 joined the inventory on
# 2026-08-03 and the sentence went on saying ten.
_NAMED_SPELLED_OUT = 3

# WLC's book code for Job, for the rows that are in its prose frame.
_JOB_BB = "jb"

# ``run-prose``'s statuses that mean the verse carries an ERROR leaf, as ``prose_oddballs``
# spells them, and how each reads on a page written for Hebrew-Bible readers.  The raw status
# is the hover text, since it is what a reader would grep the JSON for and nothing else here
# says it.
_ERROR_STATUSES = frozenset(("error", "illegal_mark"))
_STATUS_DISPLAY = {
    "clean": "clean",
    "error": "ungrammatical",
    "illegal_mark": "ungrammatical",
}

# The prose scanner's leaf names, which are ASCII and internal, against the single-sourced
# romanizations the rendered pages share.  Only the leaves a residue row can have are here; an
# unmapped leaf raises rather than printing its ASCII, which is the drift this would otherwise
# hide.  ``atnax`` takes ROM_ETNAHTA: the leaf name and the accent's name differ, and the page
# says the accent's.
_ROM_BY_LEAF = {
    "atnax": ROM_ETNAHTA,
    "darga": ROM_DARGA,
    "geresh": ROM_GERESH,
    "gershayim": ROM_GERSHAYIM,
    "legarmeh": ROM_LEGARMEH,
    "mahapakh": ROM_MAHAPAKH,
    "merkha": ROM_MERKHA,
    "munax": ROM_MUNAX,
    "pashta": ROM_PASHTA,
    "qadma": ROM_QADMA,
    "revia": ROM_REVIA,
    "silluq": ROM_SILLUQ,
    "telishagedola": ROM_TELISHA_GEDOLAH,
    "tevir": ROM_TEVIR,
    "tipexa": ROM_TIPEHA,
    "zaqef": ROM_ZAQEF_QATAN,
}


def rom_sequence(sequence: str) -> str:
    """A token sequence as the page prints it -- "merkha, silluq" for ``merkha silluq``."""
    leaves = sequence.split(" ")
    missing = [leaf for leaf in leaves if leaf not in _ROM_BY_LEAF]
    if missing:
        raise AssertionError(
            f"no romanization for the prose leaf {missing}; add it to _ROM_BY_LEAF"
            " rather than letting the page print the scanner's ASCII"
        )
    return ", ".join(_ROM_BY_LEAF[leaf] for leaf in leaves)


def default_html_out_path(repo_root: Path) -> Path:
    del repo_root
    return wlc_paths.gh_pages_dir() / "accgram" / "wlc-chanted-word-residue.html"


def default_prose_dir() -> Path:
    return wlc_paths.out_dir() / "accgram" / "prose"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the WLC chanted-word residue page.",
    )
    parser.add_argument(
        "--prose-dir",
        type=Path,
        default=default_prose_dir(),
        help="Directory of run-prose *_ag.json outputs, for the verdict column.",
    )


# --- the data -----------------------------------------------------------------


def residue(corpus: dict) -> list[dict]:
    """One corpus's chanted words whose token sequence no section of the inventory names.

    Keyed on ``NAMED_TOKEN_SEQUENCES``, the same whitelist ``classify_verse`` consults, so this
    page and the flagging path can never disagree about what counts as named.
    """
    return [
        h
        for h in corpus["occurrences"]
        if h["sequence"] not in cwa.NAMED_TOKEN_SEQUENCES
    ]


def _skeleton(chanted_word: str) -> str:
    """A chanted word's letters and maqafs, with the accents dropped.

    The maqafs stay in, so two corpora match here only when they also group the atoms the same
    way.  That is the strict reading and the one the MAM column wants: a compound MAM splits
    into two chanted words is not the same chanted word, and should not be reported as one.
    """
    return "".join(ch for ch in chanted_word if not is_accent(ch))


def _mam_index(mam: dict) -> dict[tuple[str, str], str]:
    """(bcv, letters-and-maqafs) -> MAM's token sequence, for every MAM chanted word with two."""
    return {
        (h["bcv"], _skeleton(h["chanted_word"])): h["sequence"]
        for h in mam["occurrences"]
    }


def mam_reads_no_legarmeh(row: dict) -> bool:
    """True where WLC's sequence for the row has a legarmeh and its MAM counterpart has none.

    The whole condition for the stroke caveat, kept in one place so the marker in the cell, the
    paragraph below the table and the assertion in ``pin_claims`` cannot answer it differently.
    A row with no MAM counterpart takes a dash and is out of scope: what is being caveated is a
    MAM cell that names accents, not one that names nothing.
    """
    mam = row["mam_sequence"]
    if not mam:
        return False
    leaf = "legarmeh"
    return leaf in row["sequence"].split(" ") and leaf not in mam.split(" ")


def verse_statuses(prose_dir: Path, wanted: set[str]) -> dict[str, str]:
    """The ``run-prose`` verdict of each wanted verse, read off the committed ``*_ag.json``.

    Raises if a verse is missing rather than showing a blank: an absent record means the prose
    run has not been made or does not cover the book, and a column that quietly reads empty
    there would say "clean" to every reader.
    """
    found: dict[str, str] = {}
    for path in sorted(prose_dir.glob("wlc_422_ps_*_ag.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for verse in payload.get("verses", []):
            bcv = verse.get("bcv")
            if bcv in wanted:
                found[bcv] = str(verse.get("status"))
    missing = sorted(wanted - set(found))
    if missing:
        raise AssertionError(
            f"no run-prose record for {missing} under {prose_dir};"
            " run `main_accgram.py run-prose` before this page"
        )
    return found


def build_rows(survey: dict, prose_dir: Path) -> list[dict]:
    """One row per WLC residue occurrence, grouped by token sequence, canonical order within.

    ``scan_corpus`` walks the corpus in canonical order, so an occurrence's position in the
    survey's list already is its place in the Tanakh; sorting on that index keeps canonical
    order inside each group without a second book-order table to fall out of step with the one
    ``chanted_word_accents`` has.
    """
    wlc_left = residue(survey["corpora"]["wlc422"])
    mam_by_word = _mam_index(survey["corpora"]["mam_simple"])
    statuses = verse_statuses(prose_dir, {h["bcv"] for h in wlc_left})
    rows = [
        {
            **hit,
            "status": statuses[hit["bcv"]],
            "mam_sequence": mam_by_word.get(
                (hit["bcv"], _skeleton(hit["chanted_word"]))
            ),
            "order": index,
        }
        for index, hit in enumerate(wlc_left)
    ]
    return sorted(rows, key=lambda r: (r["sequence"], r["order"]))


def pin_claims(survey: dict, rows: list[dict]) -> None:
    """Fail the build if the data stops supporting a sentence the prose states in words.

    Every count the page prints is spliced from the survey, so those cannot drift.  What can
    drift is the shape of the argument: that the whitelist is the checker's and not this page's,
    that MAM's residue is the smaller set, and that the telisha gedolah words are already
    accounted for elsewhere.  Raise rather than warn -- a warning in a generator's output is a
    warning nobody reads.
    """
    named = set(cwa.NAMED_TOKEN_SEQUENCES)
    assert named == {
        seq for entry in cwa.YEIVIN_ENTRIES for seq in entry.sequences
    }, "the whitelist has parted company with Yeivin's inventory"
    assert not (
        named & {r["sequence"] for r in rows}
    ), "a residue row has a sequence the inventory names"
    mam_left = residue(survey["corpora"]["mam_simple"])
    assert len(mam_left) == survey["mam_residue"]["total"], (
        "this page and the survey compute MAM's residue differently:"
        f" {len(mam_left)} against {survey['mam_residue']['total']}"
    )
    assert len(mam_left) < len(rows), (
        "the page says MAM's residue is the smaller set, and it is no longer:"
        f" MAM {len(mam_left)}, WLC {len(rows)}"
    )
    telisha = [r for r in rows if r["sequence"] in _TELISHA_GERESH_PAIRS]
    assert len(telisha) == 5, (
        "the page says five of the rows are the already-whitelisted telisha gedolah words;"
        f" the data now has {len(telisha)}"
    )
    assert all(
        r["status"] == "clean" for r in telisha
    ), "a whitelisted telisha gedolah word is no longer clean"
    # The opening list names three configurations and then counts the rest, so it has to be able
    # to name three.  Everything past that is spliced.
    assert len(named) > _NAMED_SPELLED_OUT, (
        f"the inventory is down to {len(named)} sequences, and the opening list names"
        f" {_NAMED_SPELLED_OUT} of them before counting the remainder"
    )
    # The opening states three magnitudes in words, and a word does not splice.  The clause
    # these three replace said "a few dozen in the Tanakh", false from the page's first commit
    # and with nothing under it -- prose with no oracle is how that survives.
    wlc = survey["corpora"]["wlc422"]
    munax_zaqef = wlc["by_sequence"].get("munax zaqef", 0)
    assert wlc["hits"] * 20 < wlc["chanted_words"], (
        "the opening says a chanted word has two accents in a small minority of cases;"
        f" the survey now has {wlc['hits']} of {wlc['chanted_words']}"
    )
    assert len(rows) * 10 < wlc["hits"], (
        "the opening says Yeivin's inventory names the pair for nearly all of the two-accent"
        f" chanted words; it now leaves {len(rows)} of {wlc['hits']} unnamed"
    )
    assert munax_zaqef * 2 > wlc["hits"], (
        "the opening says a munaḥ before a zaqef is most of the two-accent chanted words by"
        f" itself; it is now {munax_zaqef} of {wlc['hits']}"
    )
    # The stroke caveat's argument, not its size.  It explains a marked row by the scanner
    # reading no legarmeh anywhere in MAM, so a MAM sequence that has one means the explanation
    # no longer covers the row and the paragraph has to be rewritten.  Asserting instead that
    # some row is marked would fail the build on the day #215 is fixed, which is the one day the
    # page is meant to shed the caveat quietly.
    if any(mam_reads_no_legarmeh(r) for r in rows):
        mam_legarmeh = sorted(
            seq
            for seq in survey["corpora"]["mam_simple"]["by_sequence"]
            if "legarmeh" in seq.split(" ")
        )
        assert not mam_legarmeh, (
            "the stroke caveat explains a marked row by the scanner reading no legarmeh in MAM;"
            f" MAM's survey now has {mam_legarmeh}, so the caveat needs rewriting"
        )


# --- the page -----------------------------------------------------------------


# Small counts read better spelled out, and a sentence never opens on a numeral.  Only the
# range the page actually needs; anything else raises rather than printing a digit mid-word.
_NUMBER_WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
)


def _number_word(count: int) -> str:
    if not 0 <= count < len(_NUMBER_WORDS):
        raise AssertionError(f"no spelled-out form for {count}; widen _NUMBER_WORDS")
    return _NUMBER_WORDS[count]


def _counts(survey: dict, rows: list[dict]) -> dict[str, int]:
    wlc = survey["corpora"]["wlc422"]
    return {
        "verses": wlc["verses"],
        "chanted_words": wlc["chanted_words"],
        "hits": wlc["hits"],
        "residue": len(rows),
        "sequences": len({r["sequence"] for r in rows}),
        "named": len(cwa.NAMED_TOKEN_SEQUENCES),
        "named_unspelled": len(cwa.NAMED_TOKEN_SEQUENCES) - _NAMED_SPELLED_OUT,
        "mam_residue": survey["mam_residue"]["total"],
        "flagged": sum(1 for r in rows if r["status"] in _ERROR_STATUSES),
        "clean": sum(1 for r in rows if r["status"] not in _ERROR_STATUSES),
        "telisha": sum(1 for r in rows if r["sequence"] in _TELISHA_GERESH_PAIRS),
        "job_frame": sum(1 for r in rows if r["bcv"].startswith(_JOB_BB)),
        "shared_with_mam": sum(1 for r in rows if r["mam_sequence"] is not None),
    }


def _accounted_for(counts: dict[str, int]) -> str:
    """The paragraph naming the groups of rows that are accounted for elsewhere already.

    Built rather than written out, because both of its groups have already gone stale once: the
    Job sentence stood after ITM §256 named ``qadma darga`` and took every Job row out of the
    table with it, and nothing raised, the claim having been prose with no assertion under it.
    A group with no rows now drops out of the sentence instead.
    """
    groups = [
        f"the {_number_word(counts['telisha'])} words on which a telisha gedolah and a geresh"
        " or gershayim share a base letter — a legitimate pair, whitelisted by the checker's"
        " alphabet layer and set out in the telisha gedolah exhibit of the almost-errors page"
        " — where the two marks count as two accents here because the scanner does not fuse"
        " them"
    ]
    if counts["job_frame"]:
        groups.append(
            f"the {_number_word(counts['job_frame'])} Job rows, which are in Job's prose frame:"
            " poetically booked and prose cantillated, so they belong in a prose survey however"
            " the reference reads"
        )
    if len(groups) == 1:
        return f"One group of rows is accounted for elsewhere already: {groups[0]}."
    return (
        f"{_number_word(len(groups)).capitalize()} groups of rows are accounted for elsewhere"
        f" already. The first is {groups[0]}. The second is {groups[1]}."
    )


def _intro(counts: dict[str, int]) -> tuple[object, ...]:
    return (
        H.heading_level_1(PAGE_TITLE),
        # THE OPENING IS THE MAQAF-NONFINAL-ACCENTS PAGE'S, WORD FOR WORD WHERE IT CAN BE (Ben,
        # 2026-08-03: "the introductory material should be phrased similarly to (perhaps in some
        # cases exactly the same as in) maqaf-nonfinal-accents.html").  Its first three sentences
        # are a claim about the prose system rather than about a corpus, so they transfer intact;
        # what cannot is the counting sentence below, MAM being that page's corpus and WLC this
        # one's.  Its statement of how many accents a chanted word has is also the better one --
        # it says never zero and never more than two, which a bare "normally has one" left out --
        # and it leaves a chanted word undefined rather than glossing it as an atom or a whole
        # maqaf compound, which is what Ben asked for here: "better to leave it somewhat
        # undefined".
        H.para(
            (
                "In the prose system a chanted word always has at least one accent,"
                " and usually only one."
                " In a small minority of cases, a chanted word has two accents,"
                " but never more than two."
                " Some of the two-accent words are simple and some are compounds."
                " For nearly all of the two-accent words, Yeivin's ",
                itm(),
                " names the pair:",
            )
        ),
        # A LIST, NOT A SENTENCE (Ben, same day, of the three named pairs and the count of the
        # rest: "better as a bulleted list").  The last item is the remainder rather than a
        # fourth pair, which is how he wrote it out.
        H.unordered_list(
            (
                "a munaḥ before a zaqef",
                "a mahapakh before a pashta",
                "an azla before a geresh",
                f"{_number_word(counts['named_unspelled'])} more configurations besides",
            )
        ),
        text_para(
            "The first of those, a munaḥ before a zaqef, is most of the two-accent chanted"
            " words by itself."
            f" This page is the remainder. In WLC's {counts['verses']:,} prose verses there are"
            f" {counts['chanted_words']:,} chanted words, of which {counts['hits']:,} have two"
            f" accents; {counts['residue']} of those have a pair that no section of Yeivin's"
            f" inventory names, in {counts['sequences']} distinct combinations."
        ),
        text_para(
            "WLC is the Westminster transcription of the Leningrad Codex, so what is below is a"
            " fact about that transcription of that manuscript. It is not a claim about what"
            " the accentuation does, which takes MAM, a consensus text: MAM has a remainder of"
            f" {counts['mam_residue']}, a different and smaller set, and the survey's JSON keeps"
            " it separately for that reason. Where a row's chanted word is in MAM's remainder as"
            " well, the last column says what MAM has there."
        ),
        H.para(
            (
                "Nothing here is a verdict, and this page has no way to make one. The",
                *[
                    " ",
                    link("ungrammatical-verse report", "goerwitz.html"),
                    " is where WLC's accent problems are read;",
                ],
                f" of these {counts['residue']} chanted words, {counts['clean']} stand in verses"
                f" it calls clean, and the other {counts['flagged']} in verses it already calls"
                " ungrammatical for reasons that have nothing to do with two accents. Whether an"
                " unnamed pair should be an error at all is an open question, and neither this"
                " page nor the survey behind it answers it.",
            )
        ),
        text_para(_accounted_for(counts)),
    )


def _headers() -> object:
    return H.table_row(
        (
            H.table_header("Verse"),
            H.table_header("Chanted word"),
            H.table_header("Accents"),
            H.table_header("Atom or compound"),
            H.table_header(
                H.abbr("Verdict today", "The status run-prose gives the verse")
            ),
            H.table_header(H.abbr("MAM", "What MAM has on the same chanted word")),
        )
    )


_KIND_SHORT = {
    "an atomic chanted word": "atom",
    "a maqaf compound, its accents split across atoms": "compound, split",
    "a maqaf compound, its accents all on the final atom": "compound, last atom",
}

_CELL_ATTRS = (None, _HEBREW_CELL, None, None, None, None)


def _mam_cell(row: dict) -> object:
    if not row["mam_sequence"]:
        return "—"
    named = rom_sequence(row["mam_sequence"])
    if not mam_reads_no_legarmeh(row):
        return named
    return (named, " ", H.sup(H.abbr(_STROKE_MARK, _STROKE_HOVER)))


def _row(row: dict) -> object:
    return H.table_row_of_data(
        (
            ref_abbrev(row["bcv"]),
            hbo(row["chanted_word"]),
            rom_sequence(row["sequence"]),
            H.abbr(_KIND_SHORT[row["kind"]], row["kind"]),
            H.abbr(
                _STATUS_DISPLAY[row["status"]], f"run-prose status: {row['status']}"
            ),
            _mam_cell(row),
        ),
        _CELL_ATTRS,
    )


def _table(rows: list[dict]) -> object:
    return H.table(
        (_headers(), *[_row(row) for row in rows]),
        {"class": _TABLE_CLASS},
    )


def _stroke_caveat(rows: list[dict]) -> tuple[object, ...]:
    """The note the marked MAM cells point at, or nothing at all when no row is marked.

    Built the way ``_accounted_for`` builds its groups, and for the same reason: the rows this
    covers exist because of #215, so the day that is fixed the note has to leave the page without
    anyone remembering it is here.  Naming the verses by splice rather than in the sentence is
    what makes that possible.
    """
    marked = [row for row in rows if mam_reads_no_legarmeh(row)]
    if not marked:
        return ()
    where = "; ".join(
        f"{ref_abbrev(row['bcv'])}, where the Accents column says"
        f" {rom_sequence(row['sequence'])} and the MAM column"
        f" {rom_sequence(row['mam_sequence'])}"
        for row in marked
    )
    lead = (
        f"One row is marked {_STROKE_MARK} in the MAM column: {where}."
        if len(marked) == 1
        else f"{_number_word(len(marked)).capitalize()} rows are marked {_STROKE_MARK} in the"
        f" MAM column: {where}."
    )
    return (
        text_para(
            f"{lead} WLC has a Unicode PASEQ on the chanted word, with nothing between the word"
            " and the stroke, and the scanner reads that stroke as the legarmeh. MAM has the"
            " same Unicode PASEQ standing apart from the word, a space on each side, and the"
            " scanner reads only the marks on the letters. So the MAM column there says what the"
            " scanner reads of MAM's chanted word, and is not a report that MAM has nothing"
            " after the word. Neither text's Hebrew above has the stroke: the Chanted word"
            " column is letters, accents and maqafs."
        ),
    )


def _closing(counts: dict[str, int]) -> tuple[object, ...]:
    return (
        text_para(
            "A dash in the MAM column means MAM has no chanted word of those letters, grouped"
            " that way, with two accents at that verse — which covers both MAM having one accent"
            " there and MAM setting the atoms as two chanted words rather than as one maqaf"
            f" compound. Of the {counts['residue']} rows, {counts['shared_with_mam']} have a"
            " counterpart in MAM; the rest are WLC's alone, and are where the transcription and"
            " the consensus text part company."
        ),
        text_para(
            "The pairs the inventory does name, and which therefore do not appear above, are"
            f" the {counts['named']} the checker's whitelist is keyed on, read straight off the"
            " sections transcribed in the survey: they are in"
            " out/accgram/chanted-word-accents.json, each beside Yeivin's wording, his verse"
            " list where he gives a closed one, and what MAM measures against it."
        ),
    )


def render_body_contents(survey: dict, rows: list[dict]) -> tuple[object, ...]:
    counts = _counts(survey, rows)
    wrapper = H.div(
        (*_intro(counts), _table(rows), *_stroke_caveat(rows), *_closing(counts)),
        {"class": _WIDTH_CLASS},
    )
    return (wrapper,)


def run(args: argparse.Namespace) -> None:
    survey = cwa.build_survey()
    prose_dir: Path = getattr(args, "prose_dir", None) or default_prose_dir()
    rows = build_rows(survey, prose_dir)
    pin_claims(survey, rows)

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(survey, rows),
        write_ctx=H.WriteCtx(
            title=PAGE_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out} (WLC residue: {len(rows)})")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
