r"""Generate gh-pages/wlc/accgram/printed-decalogue-uvinkha.html -- the editions cited at ובנך.

A record page, not an argument page.  MAM-basics issue #208 asks whether Hebrew Wikisource's
p-trad עליון is right to have a meteg and a maqaf on ובנך in the Exodus Decalogue's Shabbat
commandment, where Koren's Classic Tanakh and the Simanim Tiqqun each have a munax instead --
the two editions transcribed for issue wlc-utils#69, whose verdicts the trio's satellite pages carry.
A reply in that thread answers it by citing eight printed editions plus Minxat Shai, each by an
archive.org or Al-Hatorah link.  This page holds those links, with a crop of each cited page, so
a reader can check a citation without opening nine scans.

The argument stays in the issue and is deliberately NOT reproduced here.  The page shows the two
pointings in letters, accents and the punctuation coupled to them (the LAP table, whose whole
derivation is pinned -- see the comment above ``_STRETCH_SKELETONS``), says in one paragraph what
each has, asks the question, and then does nothing but cite and show.  Captions are short by
design -- name the edition and say what part of the page the crop is, and let the reader look.
Do not grow them into readings of the marks; the crops are low-resolution and the issue is where
a reading belongs.

Every cited edition has a crop as of 2026-07-27.  An edition with none renders "No crop recorded
yet" rather than being silently omitted; to add one, drop the PNG in gh-pages/wlc/accgram/img/ under
the same ``<Edition>-Ex-Dec-Shabbat-uvinkha`` naming and add a ``_Crop`` to that edition's tuple.

No edition is identified by chapter and verse (Ben, 2026-07-27): the page had got that far
without one, and the Decalogue's verse numbering varies by edition, so a number picked from any
one of them would not locate the place in the others.

Run via ``main_accgram.py generate-html``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import NamedTuple

from accgram import edition_transcription as et
from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds
from accgram import rtms_report
from accgram.almost_errors_html_shared import link
from accgram.uni_to_marks import is_accent
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import hebrew_accent_strip as has
from mb_cmn import hebrew_punctuation as hpunc
from mb_cmn import paths
from mb_cmn import provenance
from py_html import wlc_utils_html as H
from py_html.my_html_span_romanized import rmn

PAGE_TITLE = "What printed editions have at ובנך"

_WIDTH_CLASS = "goerwitz-tms-width-limited"

_ISSUE_URL = "https://github.com/bdenckla/MAM-basics/issues/208"
_REPLY_URL = f"{_ISSUE_URL}#issuecomment-5092090523"

# No links back into this repository's own printed-Decalogue pages: the hub links HERE, and a
# reciprocal link only restated its navigation one page over. Nothing on this page depends on
# them, since it cites and shows rather than reporting any verdict of the checker's.

# Strand names in Hebrew letters, single-sourced in pds (see its module docstring).
_TAHTON = pds.TAHTON
_ELYON = pds.ELYON

# Romanized mark names, each pre-wrapped ONCE in <span class="romanized"> (italic), same rule as
# the rest of the printed-Decalogue pages: splice these into a contents tuple, never into an
# f-string, and never retype the spellings inline.
_ROM_LEGARMEH = rmn(pds.ROM_LEGARMEH)
_ROM_MAQAF = rmn(pds.ROM_MAQAF)
_ROM_METEG = rmn(pds.ROM_METEG)
_ROM_MUNAX = rmn(pds.ROM_MUNAX)
_ROM_PASEQ = rmn(pds.ROM_PASEQ)
_ROM_REVIA = rmn(pds.ROM_REVIA)
_ROM_TELISHA_GEDOLAH = rmn(pds.ROM_TELISHA_GEDOLAH)


# --------------------------------------------------------------------------- #
# The LAP table (letters, accents, and accent-coupled punctuation)
# --------------------------------------------------------------------------- #
# Ben, 2026-07-27: prose about this disagreement is a welcome supplement to the LAP, not a
# substitute for it -- so show the marks.  Every glyph in both rows comes out of the vendored
# strands; nothing here is typed.  The Wikisource row is one strand's own three atoms.  The
# editions' row has to be ASSEMBLED, because a transcription records which accent stands on
# which chanted word and not the pointed letters, so there is no pointed Koren or SimTiq text in
# the repo to quote.  It is assembled only from vendored atoms: the p-trad עליון's own אתה and
# ובתך (which both transcriptions match) and the p-trad תחתון's own ובנך, which is the very
# thing the transcriptions record -- a munax on ובנך standing as its own chanted word.  Every
# step is pinned in _pinned_lap_rows, which raises rather than render a row it cannot justify.
#
# Meteg is kept in the strip (METEG_ALL) although it is not an accent: it is the mark at issue
# on one side of the disagreement, and a strip that dropped it would hide the thing to look at.
_STRETCH_SKELETONS = ("אתה", "ובנך", "ובתך")

_CP_MUNAX = "\N{HEBREW ACCENT MUNAH}"
_CP_TELISHA_GEDOLA = "\N{HEBREW ACCENT TELISHA GEDOLA}"
_CP_METEG = "\N{HEBREW POINT METEG}"

# The token both transcriptions insert at this chanted word, in the accent-token vocabulary the
# transcriptions and the comparison share (edition_transcription's module docstring).
_INSERTED_TOKEN = "mun"

# The same stretch in an EDITION's token stream: כל־מלאכה, אתה, ובנך, ובתך. Four tokens because
# of the inserted munax -- the strand has three, its ובנך־ובתך being one chanted word.
_STRETCH_TOKEN_RUN = ("paz", _INSERTED_TOKEN, _INSERTED_TOKEN, "tg")

# The two hand transcriptions that raised the question: the p-trad עליון Exodus Decalogues of
# Koren's Classic Tanakh and of the Simanim Tiqqun. Both are checked, and the row is rendered
# once because they agree -- pinned, not assumed.
_EDITION_STEMS = ("koren_ex_elyon", "simtiq_ex_elyon")


class _LapRow(NamedTuple):
    """One row of the LAP table: what to call the text, and its stripped stretch."""

    label: tuple[object, ...]
    lap: str


def _atoms(chanted_verse: str) -> list[str]:
    """A chanted verse split into atoms, each keeping the maqaf that joins it to the next."""
    out: list[str] = []
    for chanted_word in chanted_verse.split():
        parts = chanted_word.split(hpunc.MAQ)
        for i, part in enumerate(parts):
            out.append(part + hpunc.MAQ if i < len(parts) - 1 else part)
    return out


def _version(source: dict, reading: str, tradition: str) -> dict:
    for version in source["versions"]:
        if (version["book"], version["reading"], version["tradition"]) == (
            "ex",
            reading,
            tradition,
        ):
            return version
    raise AssertionError(f"no ex/{reading}/{tradition} version in the vendored source")


def _stretch(version: dict) -> tuple[str, str, str]:
    """One strand's אתה / ובנך / ובתך atoms. Raises unless the Exodus Decalogue has exactly one
    such run -- so a re-vendoring that moves or duplicates the stretch fails the build.
    """
    found: list[tuple[str, str, str]] = []
    for chanted_verse in version["chanted_verses"]:
        atoms = _atoms(chanted_verse)
        skels = [pds.base_skeleton(a) for a in atoms]
        for i in range(len(skels) - 2):
            if tuple(skels[i : i + 3]) == _STRETCH_SKELETONS:
                found.append((atoms[i], atoms[i + 1], atoms[i + 2]))
    if len(found) != 1:
        raise AssertionError(
            f"{version['reading']}/{version['tradition']}: expected one"
            f" {'/'.join(_STRETCH_SKELETONS)} run, found {len(found)}"
        )
    return found[0]


def _lap(atom: str) -> str:
    return has.strip_to_accents(atom, keep_meteg=has.METEG_ALL)


def _join(atoms: tuple[str, ...]) -> str:
    """Atoms rejoined as they stand: a space between them, none after a maqaf."""
    out = ""
    for atom in atoms:
        if out and not out.endswith(hpunc.MAQ):
            out += " "
        out += atom
    return out


def _transcription(stem: str) -> et.Transcription:
    return et.load_transcription(et.transcriptions_dir() / f"{stem}.txt")


def _inserted_munax(
    source: dict, transcription: et.Transcription, compound: str
) -> et.Difference:
    """The one difference each edition's transcription has at this chanted word: an inserted
    munax. Raises if the transcription no longer says that, or says it somewhere else.
    """
    stem = transcription.path.stem
    here = [d for d in et.compare(source, transcription) if d.word == compound]
    if len(here) != 1:
        raise AssertionError(
            f"{stem}: expected one difference at {compound}, got {len(here)}"
        )
    diff = here[0]
    if (diff.kind, diff.reference, diff.transcribed) != (
        "insert",
        (),
        (_INSERTED_TOKEN,),
    ):
        raise AssertionError(f"{stem}: unexpected difference -- {diff.describe()}")
    return diff


def _no_stroke_after_atta(transcription: et.Transcription) -> None:
    """Pin that the edition has no vertical stroke between אתה and ובנך (Ben's question,
    2026-07-27).  The accent-token comparison cannot answer this: it drops the bracketed
    stroke asides entirely and folds a legarmeh onto a plain munax, so a stroke the edition
    has and its Wikisource strand lacks would leave no trace in ``et.compare``.  Both ways a
    stroke can
    be recorded are checked here -- as its own aside chunk (Koren's habit) and as a ``_leg``
    suffix on the preceding accent (the Simanim Tiqqun's) -- since the editions' row of the
    LAP table shows none.
    """
    stem = transcription.path.stem
    # The stretch in this transcription's OWN token stream: כל־מלאכה, אתה, ובנך, ובתך. The
    # edition's inserted munax is what makes the run four long here and three in the strand,
    # so the run is what locates אתה without any index arithmetic against the reference.
    toks = transcription.tokens
    starts = [
        i for i in range(len(toks) - 3) if tuple(toks[i : i + 4]) == _STRETCH_TOKEN_RUN
    ]
    if len(starts) != 1:
        raise AssertionError(
            f"{stem}: expected one {'/'.join(_STRETCH_TOKEN_RUN)} run, found {len(starts)}"
        )
    atta_i = starts[0] + 1
    # Walk the chunks as written, so a stroke aside and a `_leg` suffix are both still visible
    # (``Transcription.tokens`` has already dropped the one and folded the other).
    token_i = 0
    written_at: dict[int, str] = {}
    aside_before: dict[int, str] = {}
    for chunk in transcription.chunks:
        if chunk.startswith("["):
            if chunk in et.PASOLEG_ASIDES:
                aside_before[token_i] = chunk
            continue
        parts = et.written_accents(chunk)
        written_at[token_i] = chunk
        token_i += len(parts)
    if atta_i + 1 in aside_before:
        raise AssertionError(
            f"{stem}: a stroke aside {aside_before[atta_i + 1]} sits after אתה"
        )
    if written_at.get(atta_i) != _INSERTED_TOKEN:
        raise AssertionError(
            f"{stem}: אתה is written {written_at.get(atta_i)!r}, not a plain"
            f" {_INSERTED_TOKEN} -- a stroke may be folded into it"
        )


def _pinned_lap_rows(source: dict) -> tuple[_LapRow, _LapRow]:
    """Both rows of the LAP table, with every claim the page makes about them re-derived here.

    Raises on any drift, so the table can never outlive the data it was written against.
    """
    e_atta, e_uvinkha, e_uvitekha = _stretch(_version(source, "elyon", "printed"))
    _, t_uvinkha, _ = _stretch(_version(source, "taxton", "printed"))

    # What the two sides actually have, checked mark by mark before either row is rendered.
    if not (_CP_MUNAX in e_atta and not is_accent(e_atta[-1])):
        raise AssertionError(f"p-trad elyon אתה is not munax-accented: {e_atta!r}")
    if not e_uvinkha.endswith(hpunc.MAQ):
        raise AssertionError(f"p-trad elyon ובנך is not maqaf-joined: {e_uvinkha!r}")
    if _CP_METEG not in e_uvinkha or any(is_accent(ch) for ch in e_uvinkha):
        raise AssertionError(
            f"p-trad elyon ובנך is not meteg-and-no-accent: {e_uvinkha!r}"
        )
    if _CP_TELISHA_GEDOLA not in e_uvitekha:
        raise AssertionError(
            f"p-trad elyon ובתך has no telisha gedolah: {e_uvitekha!r}"
        )
    if hpunc.MAQ in t_uvinkha or _CP_MUNAX not in t_uvinkha:
        raise AssertionError(
            f"p-trad taxton ובנך is not a free munax word: {t_uvinkha!r}"
        )

    # Both editions' transcriptions record the same one thing here, which is why one row serves.
    compound = _join((e_uvinkha, e_uvitekha))
    transcriptions = [_transcription(stem) for stem in _EDITION_STEMS]
    diffs = [_inserted_munax(source, t, compound) for t in transcriptions]
    for transcription in transcriptions:
        _no_stroke_after_atta(transcription)
    if diffs[0] != diffs[1]:
        raise AssertionError(
            f"{_EDITION_STEMS} disagree at {compound}:"
            f" {diffs[0].describe()} / {diffs[1].describe()}"
        )

    editions = _join(tuple(_lap(a) for a in (e_atta, t_uvinkha, e_uvitekha)))
    wikisource = _join(tuple(_lap(a) for a in (e_atta, e_uvinkha, e_uvitekha)))
    # Neither label names the strand: all three texts are the p-trad עליון, so saying so in the
    # cells would repeat the paragraph above and imply the rows differ in which strand they are.
    # The two edition names are stacked rather than run together, which reads as one title.
    return (
        _LapRow(("Koren Tanakh", H.line_break(), "Simanim Tiqqun"), editions),
        _LapRow(("Hebrew Wikisource",), wikisource),
    )


def _lap_table(rows: tuple[_LapRow, ...]) -> object:
    return H.table(
        tuple(
            H.table_row(
                (
                    H.table_header(row.label),
                    H.table_datum(row.lap, {"lang": "hbo", "dir": "rtl"}),
                )
            )
            for row in rows
        ),
        {"class": "strand-table"},
    )


class _Crop(NamedTuple):
    """One scan crop: the file in gh-pages/wlc/accgram/img/, plus its alt text and caption.

    ``caption`` is a str for the ordinary case and a contents tuple where a crop needs more --
    the MG Netter composite, which has to account for its own seam.
    """

    file: str
    alt: str
    caption: object


class _Edition(NamedTuple):
    """One cited edition: its name, how the cited item identifies it, the link, and its crops.

    ``note`` is prose about this edition alone, rendered under its heading and above its crops
    so the reader has it in hand while looking at them.  Anything true of one edition goes here
    and not in its group's intro (Ben, 2026-07-27): from the intro it would sit several
    editions above the crop it describes, which is the reader-reconstruction fault the intro's
    own naming of both strands exists to avoid.
    """

    name: str
    detail: str
    url: str
    crops: tuple[_Crop, ...]
    note: tuple[object, ...] | None = None


class _Group(NamedTuple):
    """One group of editions, with the sentence that introduces it.

    ``heading`` is a contents tuple rather than a str so a romanized mark name in it goes
    through the same italic ``rmn`` wrapper as one in the prose -- a heading is prose too.
    """

    heading: tuple[object, ...]
    intro: tuple[object, ...]
    editions: tuple[_Edition, ...]


_MUNAX_ONLY = (
    _Edition(
        "Heidenheim",
        "Torah with Meor Einayim, Rödelheim, 1818–1821",
        "https://archive.org/details/"
        "heidenheim-torah-maor-enayim-rodelheim-1818-1821-images/page/n424/mode/1up",
        (
            _Crop(
                "Heidenheim-Ex-Dec-Shabbat-uvinkha.png",
                "Heidenheim: the Shabbat commandment's line at uvinkha uvitekha",
                "Heidenheim's line at the Shabbat commandment.",
            ),
        ),
    ),
    _Edition(
        "MG Netter",
        "Mikraot Gedolot, Vienna, 1859",
        "https://archive.org/details/"
        "mikraot-gedolot-vienna-1859-full-images/page/n551/mode/1up",
        (
            # One strip built from two crops, since the stretch straddles a printed line break
            # (the two sources are kept beside it as -src-unused-line1/2, as the p. 83 Simanim
            # composite's own halves are). The seam takes the brown this repo already uses for
            # a break we REMOVED -- the same #c49a6c as that composite's horizontal page-break
            # bar -- and not the blue of the p. 246 bars, which mark breaks we ADDED. Colour
            # carries that contrast; this bar is vertical only because the two pieces sit side
            # by side, line 1 on the right, which is the seam's own geometry.
            _Crop(
                "MG-Netter-Ex-Dec-Shabbat-uvinkha.png",
                "MG Netter: the stretch at uvinkha uvitekha, across a printed line break",
                (
                    "MG Netter at the Shabbat commandment.",
                    H.line_break(),
                    H.small(
                        (
                            "The bar marks a removed line break — the printed line ends at"
                            " ובנך, and ובתך picks up on the next one.",
                        )
                    ),
                ),
            ),
        ),
    ),
    _Edition(
        "Ginsburg",
        "Tanakh, 1926, volume 1 (Pentateuch)",
        "https://archive.org/details/ginsburg-tanakh-1926-images/"
        "Ginsburg_Tanakh_1926_V1_Pentateuch_images/page/n121/mode/1up",
        (
            _Crop(
                "Ginsburg-Ex-Dec-Shabbat-uvinkha-1-of-3.png",
                "Ginsburg: the main text at uvinkha uvitekha",
                "Ginsburg's main text at the Shabbat commandment.",
            ),
            # Not a "variant apparatus", which is what these captions called it before the
            # paragraph above identified the two columns: they are Ginsburg's two untangled
            # cantillations, headed מערבאי on the right and מדנחאי on the left.
            _Crop(
                "Ginsburg-Ex-Dec-Shabbat-uvinkha-2-of-3.png",
                "Ginsburg: the headings of the two untangled cantillations",
                "The headings of the two untangled cantillations on the same page:"
                " מערבאי on the right, מדנחאי on the left.",
            ),
            _Crop(
                "Ginsburg-Ex-Dec-Shabbat-uvinkha-3-of-3.png",
                "Ginsburg: this stretch in both of the untangled cantillations",
                "This stretch in both of them.",
            ),
        ),
    ),
)


_MUNAX_AND_MAQAF = (
    _Edition(
        "Hahn",
        "Biblia Hebraica",
        "https://archive.org/details/bibliahebraicaad00hahn/page/87/mode/1up",
        (
            _Crop(
                "Hahn-Ex-Dec-Shabbat-uvinkha.png",
                "Hahn: the Shabbat commandment's line at uvinkha uvitekha",
                "Hahn's line at the Shabbat commandment.",
            ),
        ),
    ),
    _Edition(
        "Leeser",
        "Tanakh, Jaquett, Philadelphia, 1878",
        "https://archive.org/details/"
        "tanakh-leeser-jaquett-philadelphia-1878-images/page/n153/mode/1up",
        (
            _Crop(
                "Leeser-Ex-Dec-Shabbat-uvinkha.png",
                "Leeser: the Shabbat commandment's line at uvinkha uvitekha",
                "Leeser's line at the Shabbat commandment.",
            ),
        ),
    ),
    _Edition(
        "MG Warsaw",
        "Mikraot Gedolot, Warsaw, 1874–1885",
        "https://archive.org/details/"
        "mikraot-gedolot-warsaw-1874-1885-full-images/page/n451/mode/1up",
        (
            _Crop(
                "MG-Warsaw-Ex-Dec-Shabbat-uvinkha.png",
                "MG Warsaw: the Shabbat commandment's line at uvinkha uvitekha",
                "MG Warsaw at the Shabbat commandment.",
            ),
        ),
    ),
    _Edition(
        "Letteris",
        "Tanakh",
        "https://archive.org/details/Letteris_Tanakh/page/n127/mode/1up",
        (
            _Crop(
                "Letteris-Ex-Dec-Shabbat-uvinkha.png",
                "Letteris: the Shabbat commandment's line at uvinkha uvitekha",
                "Letteris's line at the Shabbat commandment.",
            ),
        ),
    ),
    # Minxat Shai and MG Venice are ordinary members of this group (Ben, 2026-07-27), not a
    # section of their own. They had one when the page followed the reply's own three groups,
    # which coupled them: Minxat Shai's reading is the one the reply finds in MG Venice. That
    # coupling is the issue's argument to make, so it came out, and with it the reason to keep
    # either edition apart from the four that have the same two marks.
    _Edition(
        "Minḥat Shai",
        "in the Al-Hatorah rendering",
        "https://mg.alhatorah.org/Parshan/Minchat_Shai/Shemot/20.13#m7e_he_he_n6",
        (
            _Crop(
                "Minxat-Shai-Ex-Dec-Shabbat-uvinkha-1-of-2.png",
                "Minhat Shai: the two column headings",
                "The two column headings: לקורא ביחיד on the right, לקורא בצבור on the left.",
            ),
            _Crop(
                "Minxat-Shai-Ex-Dec-Shabbat-uvinkha-2-of-2.png",
                "Minhat Shai: the two columns' text at uvinkha uvitekha",
                "The two columns' text at the same place.",
            ),
        ),
        note=(
            # Name ובנך rather than "an atom" (Ben, 2026-07-27): the reader wants the word
            # itself at the moment the claim is made, and the generic term reads as coy. And
            # say outright that the implication is ours -- an earlier draft's "Minxat Shai's
            # maqaf is implied by ..." let it pass for something on the page.
            "Minḥat Shai has no explicit ",
            _ROM_MAQAF,
            ", but we view it as having a ",
            _ROM_MAQAF,
            " implied by ובנך with only a ",
            _ROM_METEG,
            ". It, like Ginsburg, sets the two strands out in columns, under other names than"
            " we use here, with that ",
            _ROM_METEG,
            f" on ובנך in the {_ELYON} against a ",
            _ROM_MUNAX,
            f" on ובנך in the {_TAHTON}.",
            # Same treatment as the Ginsburg mapping in the group above, and settled the same
            # way: in the second crop below, the ביחיד column has the vertical bar after אתה
            # and the בצבור column has none. That bar is a תחתון feature no עליון strand has.
            # The mapping is also the traditional division of labour the headings name -- the
            # עליון for reading to the congregation, the תחתון for reading alone.
            f" (Its אלה הטעמים לקורא בצבור is our {_ELYON} and its אלה הטעמי׳ לקורא ביחיד"
            f" is our {_TAHTON}.)",
        ),
    ),
    _Edition(
        "MG Venice",
        "the Second Rabbinic Bible, Venice, 1525",
        "https://archive.org/details/"
        "second-rabbinic-bible-venice-1525-color-full-images/page/n182/mode/1up",
        (
            _Crop(
                "MG-Venice-Ex-Dec-Shabbat-uvinkha.png",
                "MG Venice: the Shabbat commandment's line at uvinkha uvitekha",
                "MG Venice at the Shabbat commandment.",
            ),
        ),
    ),
)


def _groups() -> tuple[_Group, ...]:
    return (
        _Group(
            ("A ", _ROM_MUNAX, " and no ", _ROM_MAQAF),
            (
                # Full names in rendered prose (item 8 of doc/review-findings-2026-07-29.md):
                # the "KorTan/SimTiq" shorthand that stood here is code vocabulary --
                # transcription stems and comments -- and the page's own intro already says
                # "Koren's Classic Tanakh and the Simanim Tiqqun".
                "The following three editions agree with (or are at least consistent with)"
                " Koren's Classic Tanakh and the Simanim Tiqqun: Heidenheim, MG Netter,"
                " and Ginsburg."
                ' The reason I retreat to "are at least consistent with" is'
                ' that Heidenheim and MG Netter present manuscript-style "tangled" cantillation:'
                " two cantillations on one set of letters."
                " We interpret the vertical bar after אתה as a ",
                _ROM_LEGARMEH,
                " (not a ",
                _ROM_PASEQ,
                f") and ignore it since we assume it belongs to the {_TAHTON}."
                " Similarly we ignore the ",
                _ROM_REVIA,
                f" on the ת of ובתך since we assume it belongs to the {_TAHTON}.",
                " Although Ginsburg, too, presents tangled cantillation, that edition also"
                " provides untangled (single-strand) cantillations, albeit by slightly"
                " different names than we use here.",
                # Which column is which is not taken on trust: the two Ginsburg crops below
                # settle it twice over. The מערבאי column has לא־תעשה with a maqaf and a
                # vertical bar after אתה; the מדנחאי column has לא תעשה with neither. Both of
                # those are תחתון features that no עליון strand has.
                f" (Its מדנחאי is our {_ELYON} and its מערבאי is our {_TAHTON}.)",
            ),
            _MUNAX_ONLY,
        ),
        _Group(
            ("A ", _ROM_MUNAX, " and a ", _ROM_MAQAF),
            (
                # Name both strands rather than "one strand ... the other" (Ben, 2026-07-27):
                # leaving the reader to work out which mark went where is the same fault as
                # "the latter", and the four words it saves are not worth the work it costs.
                #
                # The same retreat the group above makes, and for the same reason (Ben,
                # 2026-07-27). A tangled book has both marks on one set of letters and so can
                # only be CONSISTENT WITH a division between the strands; agreeing with one
                # takes untangled strands, which of these six only Minxat Shai has. An earlier
                # draft said all six "divide the two marks as Wikisource does", which credits
                # five of them with a division they do not make.
                #
                # "Books", not "editions" (Ben's word): Minxat Shai is not an edition of the
                # Torah or the Tanakh, so the group above can say "editions" and this one
                # cannot.
                "The following six books agree with (or are at least consistent with)"
                " Wikisource, which has the ",
                _ROM_MUNAX,
                f" in the {_TAHTON} and the ",
                _ROM_MAQAF,
                f" in the {_ELYON}: Hahn, Leeser, MG Warsaw, Letteris, Minḥat Shai, and MG"
                " Venice."
                ' Of five of them we can say no more than "are at least consistent with",'
                " because they present tangled cantillation: both marks stand on one set of"
                " letters, which leaves open which mark belongs to which strand. Only Minḥat"
                " Shai has untangled strands, so it alone can be said to agree — and even"
                " there the ",
                _ROM_MAQAF,
                " is one we have to infer.",
            ),
            _MUNAX_AND_MAQAF,
        ),
    )


def default_html_out_path(repo_root: Path) -> Path:
    return paths.wlc_pages_dir() / "accgram" / "printed-decalogue-uvinkha.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the ובנך editions page.",
    )


def _intro(rows: tuple[_LapRow, ...]) -> tuple[object, ...]:
    return (
        H.heading_level_1(PAGE_TITLE),
        # The table leads and the prose follows it (Ben, 2026-07-27): the LAP is the thing to
        # look at, and the paragraph under it says in words what the two rows already show.
        # The lead-in names the strand, since neither row's label does any more.
        H.para(
            (
                f"In the Shabbat commandment of the printed-tradition {_ELYON} of the Exodus"
                " Decalogue, there are multiple ways to point the atom ובנך in the phrase"
                " אתה ובנך ובתך. Here are two such ways (dropping vowels and other marks not"
                " germane to our investigation):",
            )
        ),
        _lap_table(rows),
        H.para(
            (
                "Hebrew Wikisource has a ",
                _ROM_METEG,
                " and no accent on ובנך, joined by ",
                _ROM_MAQAF,
                " to ובתך, which has a ",
                _ROM_TELISHA_GEDOLAH,
                ": one chanted word. Koren's Classic Tanakh and the Simanim Tiqqun each have"
                " a ",
                _ROM_MUNAX,
                " on ובנך and no ",
                _ROM_MAQAF,
                ": two chanted words.",
            )
        ),
        # Ask the question outright. An earlier draft opened "The question is asked, and argued
        # out, at MAM-basics issue #208" without ever saying what the question was -- Ben,
        # 2026-07-27: "You can't just leave the reader hanging. Either don't introduce the
        # notion of a question, or say what the question is." "These two" are the table's two
        # rows, which is why this paragraph has to stay below it.
        H.para(
            (
                f"Which of these two cantillations best represents the printed tradition {_ELYON}?"
                " That question is discussed at ",
                link("MAM-basics issue #208", _ISSUE_URL),
                ", and this page supplements the discussion with images of the editions ",
                link("the reply there", _REPLY_URL),
                " cites by link alone.",
            )
        ),
        # Ben, 2026-07-27: note that the editions vary here, and go no further than noting it.
        # The variation is real and visible in the crops below, and a reader who spots it needs
        # to be told it is not the question -- but it is a question of its own, and this page
        # answers one. The stress helper is glossed because "stress helper" is our term, not a
        # term a reader of the printed editions arrives with.
        H.para(
            (
                "The editions below vary in whether they have the ",
                _ROM_TELISHA_GEDOLAH,
                "'s stress helper on the ת of ובתך — a second mark on the stressed syllable,"
                " the ",
                _ROM_TELISHA_GEDOLAH,
                " itself standing at the right edge of the atom wherever the stress falls."
                " This page notes that variation and does no more with it.",
            )
        ),
    )


def _figure(crop: _Crop) -> object:
    # class="ink-on-white" opts the scan into the stylesheet's dark-mode CSS inversion. Every
    # image on this page is black ink on white paper (printed pages and a screen rendering of
    # one), so it is unconditional here -- unlike the manuscript photos elsewhere in the tree,
    # which are ink on parchment and must NOT invert. See the rule's comment in style.css.
    img_node = H.img(
        {"src": f"img/{crop.file}", "alt": crop.alt, "class": "ink-on-white"}
    )
    return H.figure(
        (
            H.para(img_node, {"class": "goerwitz-tms-image"}),
            H.figcaption(crop.caption, {"class": "goerwitz-tms-image-caption"}),
        ),
        {"class": "goerwitz-tms-figure"},
    )


def _edition_block(edition: _Edition) -> tuple[object, ...]:
    out: list[object] = [
        H.heading_level_3((link(edition.name, edition.url), f" — {edition.detail}"))
    ]
    if edition.note is not None:
        out.append(H.para(edition.note))
    if edition.crops:
        out.extend(_figure(crop) for crop in edition.crops)
    else:
        out.append(H.para(H.em("No crop recorded yet.")))
    return tuple(out)


def _group_block(group: _Group) -> tuple[object, ...]:
    out: list[object] = [H.heading_level_2(group.heading), H.para(group.intro)]
    for edition in group.editions:
        out.extend(_edition_block(edition))
    return tuple(out)


def render_body_contents() -> tuple[object, ...]:
    sections: list[object] = [*_intro(_pinned_lap_rows(pd.load_source()))]
    for group in _groups():
        sections.extend(_group_block(group))
    return (H.div(tuple(sections), {"class": _WIDTH_CLASS}),)


def run(args: argparse.Namespace) -> None:
    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(),
        write_ctx=H.WriteCtx(
            title=PAGE_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    n_editions = sum(len(group.editions) for group in _groups())
    n_crops = sum(len(ed.crops) for group in _groups() for ed in group.editions)
    print(f"HTML: {html_out} ({n_editions} editions, {n_crops} crops)")


def main() -> None:
    force_utf8_io()
    repo_root = paths.repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
