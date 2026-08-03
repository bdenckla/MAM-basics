r"""Generate gh-pages/accgram/maqaf-nonfinal-accents.html, and the JSON behind it.

The rendered account of ``maqaf_nonfinal_accents``' survey, narrowed to one question: how often a
non-final atom of a compound has an accent of its own in MAM, and what that means for
``koren_dt_elyon``'s ``mun-mun`` on לא־תעשה.  Every number on the page is spliced from the survey
this run computes, and the same run writes ``out/accgram/maqaf-nonfinal-accents.json``, so page
and data cannot drift.

The survey is wider than the page: three corpora, both genres, and a route (a)/(b) split telling
an inherited secondary accent from a maqaf written after an atom that keeps its own conjunctive.
The page rendered all of that until 2026-07-27 and now renders MAM's prose alone -- see issue wlc-utils#83
for what was cut and why, and wlc-utils#82 for the Yeivin citations that must be settled before the
route-(b) material is rendered anywhere again.

Rendered-prose conventions are ``printed_decalogue_strands``' module docstring; the romanizations
come from its ``ROM_*`` constants and are never retyped here.

Run via ``main_accgram.py generate-html-maqaf-nonfinal-accents``.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from pathlib import Path

from accgram import accent_marks as am
from accgram import maqaf_nonfinal_accents as mpa
from accgram import printed_decalogue as pd
from accgram import rtms_report
from accgram.almost_errors_html_shared import (
    accents_and_letters,
    hbo,
    link,
    ref_abbrev,
    text_para,
)
from accgram.printed_decalogue_strands import (
    ELYON,
    ROM_DARGA,
    ROM_AZLA,
    ROM_ETNAHTA,
    ROM_GERESH,
    ROM_GERSHAYIM,
    ROM_MAHAPAKH,
    ROM_MAQAF,
    ROM_MERKHA,
    ROM_MUNAX,
    ROM_PASHTA,
    ROM_PAZER,
    ROM_QADMA,
    ROM_REVIA,
    ROM_SILLUQ,
    ROM_TELISHA_GEDOLAH,
    ROM_TEVIR,
    ROM_TIPEHA,
    ROM_ZAQEF_QATAN,
    TAHTON,
)
from accgram.uni_to_marks import is_base_letter
from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import provenance
from py_html import my_html_for_img as mhi
from py_html import wlc_utils_html as H

import wlc_paths

# "Non-final atom of a compound", not "proclitic" and not "maqaf-joined atom".  "Proclitic"  # prose-ok: names the rejected term
# asserted a grammatical role the scan never checks -- route (b) is precisely an atom that keeps
# its own conjunctive, so it is proclitic by position only.  And a lone atom is never "maqaf-joined"  # prose-ok: names the rejected term
# full stop: it is joined TO the next one, or else the two of them are joined to each other.
# Naming the atom by its POSITION in the compound says what the scan measures and nothing more,
# and it matches the module basenames.  (wlc-utils#81's sweep settled "atom" as a reader-facing term,
# which is what lets it stand bare in the body.)
#
# THE TITLE NAMES THE QUESTION, NOT THE SCAN (Ben, 2026-07-30).  It was "Accents on a Non-Final
# Atom" -- the survey's own subject, the thing the tables count.  But the survey is the means:
# the intro asks whether Tanakh has anything like the three strange spreaders of Koren's
# Deuteronomy and the Simanim Tiqqun's Exodus, and every table under it is answering that.  So
# the title says what the page is FOR.  ("Accents on a Non-Final Atom" had itself dropped "of a
# maqaf compound" for space earlier the same day, an atom being non-final only within one.)
# The basenames -- this module, the survey, the HTML, the JSON -- keep the scan's name, which is
# what they are named for.
#
# THE BARE "SIMANIM" IS DELIBERATE; DO NOT "FIX" IT TO "the Simanim Tiqqun".  Raising it was
# right and Ben settled it, 2026-07-30: "I consider it an acceptable breaking of the rule on the
# basis of the need for brevity in a title", and then, more exactly, "it is a strange spreader in
# a simanim edition" -- the word is the PUBLISHER here, one of the senses that survive bare.  He
# also stated the governing test: distinguishing the Tiqqun from the Tanakh "is only critical ...
# where there would be possibility of confusion, e.g. in a document discussing both", and this
# page's Simanim material is the Tiqqun's alone.  Even a document that DID discuss both would
# keep the exception "where from context it is clear or, as in a title, where context *will* make
# it clear" -- a title is read with the page under it.  The body prose still names it in full.
PAGE_TITLE = "Strange Spreaders in Koren and Simanim"
_WIDTH_CLASS = "goerwitz-tms-width-limited"

# The one text this page counts.  It used to count three, WLC and UXLC beside MAM, and carry a
# section warning that those two were not two independent readings -- UXLC being WLC 4.20 with
# Kimball's corrections, so a column agreeing with its neighbor was one hand agreeing with itself.
# Ben, 2026-07-27: "Ditch WLC and UXLC; I don't think I ever asked for that scope.  MAM='The
# Tanakh', for the purposes of this document."  A claim about what the accentuation DOES wants a
# consensus text anyway, which is what the caveat section had been working around rather than
# acting on.  The survey behind the page still computes all three, so the tracked JSON is
# unchanged and the other two remain a query away.
_CORPUS = "mam_simple"


# Accent names for the shorthand the survey's shapes are written in -- ``qad-zaq``, ``mer-sil``.
# The shapes are code identifiers and spell ח with an x, as the transliteration standard requires
# of code and of the tracked JSON alike; rendered prose takes the ROM_* romanizations instead.
# ``_pair_of`` raises on a shorthand not here, so a corpus bump that produces a new pair fails
# the build rather than printing a code identifier at a reader.
_ACCENT_DISPLAY = {
    "qad": ROM_QADMA,
    "zaq": ROM_ZAQEF_QATAN,
    "tip": ROM_TIPEHA,
    "etn": ROM_ETNAHTA,
    "mer": ROM_MERKHA,
    "sil": ROM_SILLUQ,
    "mah": ROM_MAHAPAKH,
    "pash": ROM_PASHTA,
    "mun": ROM_MUNAX,
    "tev": ROM_TEVIR,
    # Reached only by the simple side, which since 2026-07-28 covers every pair that occurs on
    # a chanted word of MAM's prose verses rather than only the eight the compound side has.
    "ger": ROM_GERESH,
    "dar": ROM_DARGA,
    "rev": ROM_REVIA,
    "paz": ROM_PAZER,
    # Reached only by the one-letter appendix, which shows the chanted words the simple counts
    # set aside rather than counting them, and so names marks no pair row does.
    "ger2": ROM_GERSHAYIM,
    "telg": ROM_TELISHA_GEDOLAH,
}

# GONE with the classification (Ben, 2026-07-28): _CONFIG_DISPLAY, which rendered Yeivin's
# category names, and the two labels for the rows that held the cases the categories could not
# name or could not reach.  The unnamed one read "no named configuration: the mark is simply not
# at that atom's own accent position" -- "too long for a cell, and anyway I have no idea what
# [it means], and it features your favorite, usually meaningless word: own".  Both faults are
# moot now: with the rows gone there is no cell, and a table of observed pairs has nothing to
# say about where an accent would otherwise have fallen.
#
# The naming rules those labels carried are worth keeping even though the labels are not:
#   * "the mayela", never "the mayela tipexa" -- mayela IS the name for what would otherwise be
#     a tipexa there, so the pair reads as a kind of tipexa.  Mayela is to tipexa as metigah is
#     to qadma, and nobody writes "metigah qadma".
#   * No "secondary" in a rendered label: unexplained, the page never saying what a secondary
#     accent is, and arguably unwarranted, Yeivin calling every mark on his list secondary where
#     Breuer (CoS ch. 9 §§21-23) reserves the word for pairs that cannot stand in that order
#     across two separate words.  Naming the two marks asserts neither view, which is the point.

# Where an accent has a name of its own in the position the pair puts it in, the row uses that
# name.  A tipexa in the chanted word of an etnaxta or of a silluq is the MAYELA; a qadma in the
# chanted word of a zaqef qatan is the METIGAH.  Ben's own analogy -- mayela is to tipexa as
# metigah is to qadma -- and he asked the same question of both rows in turn: "what happened to
# the terminology of mayela?", then the same of metigah.  The intro still glosses metigah-zaqef
# as a qadma before a zaqef qatan, which is what tells a reader which mark the row means.
#
# Single-sourced, because the prose under the table names them too, in the sentence that gives
# Breuer's rule for which pairs a maqaf can stand after: a cell and a sentence spelling the same
# position differently is the drift the ROM_* constants exist to stop, and these two names are
# not among them (they are positions a mark takes, not marks).
_MAYELA = "mayela"
_METIGAH = "metigah"
_PAIR_FIRST_NAME = {
    ("tip", "etn"): _MAYELA,
    ("tip", "sil"): _MAYELA,
    ("qad", "zaq"): _METIGAH,
}

# The SECOND accent's cell, where one mark goes by two names and the row cannot choose between
# them (Ben, 2026-07-29: 'name the cell "ger./az." and explain either right before or right after
# the table what that means').  A geresh on a chanted word stressed on its last syllable is
# called an azla, so the qadma-geresh row's 99 may be of both kinds -- and unlike metigah and
# mayela above, which are conditioned on the neighbouring ACCENT, this one is conditioned on
# STRESS.  Hence both names in the cell rather than a choice, and ``_geresh_or_azla_note`` under
# the table.  The stress is now known, and the cell still names both: see that note's docstring
# for the count and for why the page says nothing about it.
#
# WHAT THE THREE BOOKS ACTUALLY SAY, settled 2026-07-29 over two passes of the full OCR corpora
# and recorded here rather than left in a session transcript.  The question was Ben's: is the
# qadma of a qadma-geresh chanted word "usually called azla", narrowly, in that context?  He then
# corrected himself from his own copy of Jacobson -- it is the GERESH that is sometimes called
# azla -- and the search bore that out:
#
#   * JACOBSON, "Chanting the Hebrew Bible" (2nd expanded ed.), is the ONLY one of the three that
#     conditions the name on stress.  Glossary: azla is (1) another name for geresh, when the word
#     it is on is stressed on the last syllable, and (2) another name for kadma.  Body, p. 187:
#     strictly only mille'el words take a geresh, so some call the combination "kadma azla" when
#     the second word is millera'; and in some traditions kadma azla is sung to a different melody
#     from kadma geresh.  His own footnotes cite Binder, Abraham W., "Biblical Chant", New York:
#     Sacred Music Press, 1959, 52-53; and once, for Esther, Zeitlin, Shneur Zalman, and Haim
#     Bar-Dayan, "Miqraey qodesh: The Megillah of Esther and Its Cantillation" (in Hebrew),
#     Jerusalem: Kiryat Sefer, 1974, 88-91.  NOTE his worked example is the
#     combination across TWO words (Numbers 7:11); the glossary sense is stated of the mark
#     generally, which is what covers this row.
#   * YEIVIN, ITM, draws a stress distinction but names its two sides GERESH and GERSHAYIM, not
#     azla (§265): geresh on a word with penultimate stress, or on any word preceded by azla
#     (Genesis 11:31 penultimate, Genesis 22:6 final); gershayim on a final-stress word preceded
#     by no servus or by munax.  His standing name for the conjunctive is azla throughout, and he
#     never uses "qadma" as an English name.
#   * BREUER, CoS, states no stress condition on azla at all.  His geresh entry (§26.d) says some
#     call it azla, on shape grounds; §39.e explains azla against pashta by shape and by tune, and
#     kadma as the servant that "precedes" the azla.  His own stress-conditioned rule in this area
#     is geresh vs gershayim (ch. 5 §9), where "azla" does not appear.  His standing name is kadma.
#
# So the three do not CONFLICT: Jacobson adds a distinction the other two do not make, which is
# why "in some traditions" is in the rendered note and why the note cites him alone.  Ben:
# "I'm comfortable resting on Jacobson's terminology; to me it doesn't contradict Yeivin or
# Breuer; it just adds a distinction that they don't make."
#
# AND NO SURVEY OF MARKS CAN DECIDE IT.  Unicode has no geresh-versus-azla distinction: its only
# geresh flavors are plain geresh (U+059B, which INCLUDES azla), geresh muqdam (U+059D, poetic --
# in MAM the revia mugrash component), and gershayim (U+059C).  Neither Yeivin nor Breuer uses
# the term "geresh muqdam" anywhere.  MAM's prose verses have no ``qad-germ``, so this row is
# entirely plain geresh -- which settles the codepoint and never the name.
_GERESH_OR_AZLA = "ger./az."
_PAIR_SECOND_NAME = {
    ("qad", "ger"): _GERESH_OR_AZLA,
}

# A cell holding a number is right-justified, so the digits line up on the units column.  The
# rule is in gh-pages/style.css; the class goes on the count column's header too, or the heading
# sits over nothing.
_NUMERIC_CELL = {"class": "numeric"}

# A cell holding Hebrew is declared right-to-left, which right-justifies it as a consequence of
# saying what the cell holds.  Ben, 2026-07-29: "probably declaring the cells dir='rtl' would do
# it, arguably at a better, more semantic level than a literal setting of the text-align
# property".  It works because table.centered-table centers the TABLE and not its cells, so a
# cell's text still starts at its start edge -- which dir="rtl" moves to the right.  No
# stylesheet rule is needed, and none is added: a class here would be a second place to look.
#
# EVERY Hebrew cell on the page gets it, not just the one Ben happened to be looking at.  He had
# asked only about the one-letter appendix's "Chanted word" column, then: "this problem afflicts
# the other tables in the document as well, and indeed is something I find myself telling you
# about frequently ... this should just be sort of obvious, that (unless the whole table is
# dir=rtl) Hebrew cells should be dir=rtl".  So it is a standing rule, now written into the
# ``hebrew-prose`` skill's rendered-prose reference rather than left to be re-noticed per table.
_HEBREW_CELL = {"dir": "rtl"}

# The printed-case table's short-label rows, centered under their row label (Ben, 2026-07-30).
# A transposed table's data cells are three parallel answers to one row's question -- three
# edition names, three book names, three added marks -- and a short answer left-aligned in a wide
# cell reads as the start of a line of text rather than as one of three things being compared.
# The class is in gh-pages/style.css beside th.numeric/td.numeric, and centering is the one
# alignment that has no semantic attribute to declare it with: dir="rtl" says what a cell HOLDS
# and right-justifies as a consequence, which is why _HEBREW_CELL above needs no class at all.
_CENTERED_CELL = {"class": "centered"}
# The strand row holds Hebrew AND is centered, so it carries both -- the declaration of what the
# cell holds, and the explicit alignment that overrides the right-justification that declaration
# would otherwise give it.
_CENTERED_HEBREW_CELL = _HEBREW_CELL | _CENTERED_CELL

# One attributes tuple per table, so a table's body rows and its Total row cannot come to align
# their columns differently -- each was spelled out twice before the Hebrew cells were declared.
# The Total row's example cells are empty, and are declared right-to-left all the same: the
# declaration says what the COLUMN holds, and an exception for the blank one would be a second
# rule to keep in step.
_PAIR_CELL_ATTRS = (
    None,
    None,
    _NUMERIC_CELL,
    _HEBREW_CELL,
    _NUMERIC_CELL,
    _NUMERIC_CELL,
    _HEBREW_CELL,
)
_SIMPLE_ONLY_CELL_ATTRS = (None, None, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL)

# Accent names too long for a cell, abbreviated there with the romanization on hover (Ben,
# 2026-07-29: "In the 'Acc2' column, abbreviate 'telisha gedolah' to 'TG' and expand it with
# hover-text").  Same trade the C/S/Acc1/Acc2 headings make: a fifteen-character name sets the
# column's width and pushes the rest of the row apart.  The hover text is the ROM_* constant
# itself, never a retyped copy, so the abbreviation cannot come to expand to something the page
# does not otherwise say.  Keyed by DISPLAY NAME, so it reaches all three tables; only the
# one-letter appendix has a telisha gedolah today, and the other two are unchanged by it.
_ACCENT_CELL_ABBR = {ROM_TELISHA_GEDOLAH: "TG"}

# The same trade for a book name in the printed-case table's Decalogue row (Ben, 2026-07-30:
# 'abbreviate "Deuteronomy" as "Deut."').  Only the long one: "Exodus" is shorter than the row
# label above it and abbreviating it would buy the table nothing.  The short form is the OSIS
# abbreviation ``_ref_abbrev`` already writes for that book, so the page names Deuteronomy the
# same way in a cell as it does in a verse reference.
_BOOK_CELL_ABBR = {"Deuteronomy": "Deut."}


def _cell_abbr(name: str, table: dict[str, str]) -> object:
    """One name for a table cell, abbreviated with the full form on hover if it is a long one."""
    short = table.get(name)
    return H.abbr(short, name) if short else name


def _accent_cell(name: str) -> object:
    """One accent name for a table cell, abbreviated if it is one of the long ones."""
    return _cell_abbr(name, _ACCENT_CELL_ABBR)


_SMALL_NUMBERS = (
    "no",
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
)


# Route (b) is the RESIDUE left when no named configuration fits, so nothing in the classifier
# guarantees its mark is the conjunctive the route is named for.  The page used to disclose that
# in the bullet, with a ``_HABIT_MARKS`` tuple and a ``pin_claims`` assertion keeping the
# disclosure honest -- but every counterexample was WLC's or UXLC's (WLC's Jeremiah 48:12, UXLC's
# Jeremiah 48:12 and Ezekiel 16:37, a tipexa on the non-final atom in each), and MAM has no
# route-(b) hit at all.  With those two corpora off the page there is nothing left to disclose,
# so the sentence, the tuple and the assertion all went (2026-07-27).  Should a corpus bump ever
# give MAM a route-(b) hit, the disclosure has to come back with it.
#
# The half-sentence that had led into the disclosure -- "it is named for what it mostly holds
# rather than for what it is sifted by" -- went too, on the same reasoning: with route (b) empty
# on the page, it was a methodological remark about a bucket the reader cannot see into.


# GONE with the intro's running prose (2026-07-29): ``_emph``, a bold ``em.emphasis`` wrapper --
# the page's one use of it was the "both" of "a munax on both of its atoms", and the table shows
# both accents instead of insisting on them.  ``em.emphasis`` stays in the stylesheet, and the
# rule it stood for is worth keeping if emphasis is ever wanted again: bold, never italic, italic
# being ``span.romanized``'s for accent names.


def _n(survey: dict, corpus: str, genre: str, field: str) -> int:
    return survey["corpora"][corpus][genre][field]


def _gray(survey: dict, kind: str | None = None) -> int:
    """The gray-maqaf total, or the count of one of its two kinds."""
    gray = survey["gray_maqaf"]
    return gray["total"] if kind is None else gray["by_kind"][kind]


def _route_count(survey: dict, corpus: str, genre: str, route: str) -> int:
    return survey["corpora"][corpus][genre]["by_route"].get(route, 0)


def _occurrences(survey: dict, corpus: str, genre: str) -> list[dict]:
    return survey["corpora"][corpus][genre]["occurrences"]


def _occurrence(survey: dict, corpus: str, genre: str, bcv: str) -> dict:
    """The single occurrence record a sentence names, or a build failure.

    The two worked examples splice their oracle counts out of these records, so a corpus bump
    that drops the verse -- or that splits it in two -- must stop the build rather than leave
    a sentence standing beside a number that no longer describes it.
    """
    found = [o for o in _occurrences(survey, corpus, genre) if o["bcv"] == bcv]
    if len(found) != 1:
        raise AssertionError(
            f"{corpus}/{genre} {bcv}: expected exactly one occurrence, found {len(found)}"
        )
    return found[0]


def _pair_of(shape: str) -> tuple[str, str]:
    """The two accents a shape holds, as romanized names, non-final atom's first.

    A shape is one field per atom -- ``qad-zaq``, ``0-mer-sil`` -- and every hit has exactly
    two accented atoms, which ``pin_claims`` also asserts.  A field of repeats is one accent
    written twice (MAM's Ezekiel 16:12 נֶ֙זֶם֙ has ``pash+pash``), so it collapses to one name.
    """
    accented = []
    for atom in shape.split("-"):
        if atom == "0":
            continue
        marks = set(atom.split("+"))
        assert len(marks) == 1, f"more than one accent on an atom of {shape}"
        accented.append(marks.pop())
    assert len(accented) == 2, f"not two accented atoms in {shape}"
    first, second = accented
    return first, second


# The pair columns, single-sourced so the three tables cannot come to head them differently.
# Written order is the only thing the split-off "before" used to say, so the hover text says it.
# Every column of Hebrew forms carries its verse on hover, and says so in its heading (Ben,
# 2026-07-29: "advertise book-chapter-verse hoverability in the hover-text of the header of all
# columns whose data cells have book-chapter-verse hover-text").  The heading is the only place
# that CAN advertise it: the forms themselves deliberately take no dotted underline, since it
# would be drawn right where a mark under the last letter sits (see ``_example_cell``), so
# nothing in the column's own appearance invites the hover.  The headings do carry the dotted
# rule, being ``abbr[title]``, so this is a hover a reader is already invited to make.  One
# string, spliced into all four titles, so they cannot come to promise different things.
_BCV_ON_HOVER = "hover one for its book, chapter and verse"


def _example_header(short: str, on_what: str) -> object:
    """One "Example" heading, named for the count column it exemplifies.

    Ben, 2026-07-29: "why not qualify the 'Example' header cells of the table with 'C' and 'S'
    counts as 'C-Example' and 'S-Example'?"  Two columns both headed "Example" left a reader to
    infer from position which count each one draws its example from, and position is exactly what
    a wide table makes hard to hold.  The prefix is the neighbouring column's own heading, so the
    pairing is stated rather than implied, and the hover text expands the letter as that column's
    does.  ``_simple_only_table`` takes it too: it has only one example column and so nothing to
    disambiguate, but "S-Example" over an S count reads the same in both tables, and an unprefixed
    one there would suggest a distinction that is not there.
    """
    return H.table_header(
        H.abbr(
            f"{short}-Example",
            f"An example of the pair on a {on_what}; {_BCV_ON_HOVER}",
        )
    )


_ACC_HEADERS = (
    H.table_header(
        H.abbr("Acc1", "The first of the two accents, in the written order")
    ),
    H.table_header(
        H.abbr("Acc2", "The second of the two accents, in the written order")
    ),
)

# The three kinds a two-accent chanted word of MAM's prose verses can be, each glossed once and
# spliced into every heading and hover text that names it -- the count columns, the example
# columns, and both tables at that.  Three columns whose headings are one letter apiece were
# fine while there were two of them and "C" could stand for the compound side outright; with a
# second kind of compound counted (Ben, 2026-07-30) a single letter would have to be read off
# the hover text every time, so the headings are the first three letters of the page's own three
# nouns instead.  All three are the same width, which keeps the counts from drifting apart --
# the width complaint that got the headings abbreviated in the first place.
_SPR, _CNC, _SIM = "Spr", "Cnc", "Sim"
_SPREADER_GLOSS = (
    "spreader — a compound chanted word with an accent on a non-final atom"
)
_CONC_GLOSS = (
    "concentrator — a compound chanted word with both of its accents on its last atom"
)
_SIMPLE_GLOSS = "simple chanted word"


def _count_header(short: str, gloss: str) -> object:
    """One count column's heading: the short form, with what it counts on hover."""
    return H.table_header(H.abbr(short, f"On a {gloss}"), _NUMERIC_CELL)


# In-page anchor for the appendix listing the chanted words whose two marks sit on one letter,
# single-sourced as both the note's link target and the appendix heading's id.
_ONE_LETTER_ID = "one-letter"
# The same anchor as an href, so the note's splice line stays one line: with the ``f"#{...}"``
# spelled inline it ran past 88 and black broke the group across four lines, which is the
# opposite of what the idiom is for.
_ONE_LETTER_HREF = f"#{_ONE_LETTER_ID}"

# MAM's own features-of-interest lists, generated in MAM-basics and published from MAM-with-doc,
# linked where each one is about the very thing the paragraph beside it reports (Ben, 2026-07-29:
# "yes please do that linking").  Same URL shape ``prose_ob_notes_is`` already uses for
# foi-pasoleg-1.  NO COUNTS ARE QUOTED from them: they are another repo's numbers, regenerated on
# another schedule, and this page splices only its own survey.
_FOI = "https://bdenckla.github.io/MAM-with-doc/foi/foi-{}.html"

# sec-merk and sec-misc are the two that catalogue this page's phenomenon per instance -- a
# merkha, and a mahapakh, standing beside the chanted word's other accent.  Their sibling
# sec-star-breuer-cos regroups the same examples by the CoS section cited for each, which is a
# level of detail this page has no room for.  What they do NOT cover is metigah-zaqef,
# munax-zaqef, mayela and azla-geresh -- the four prose pairs the table's own rows are mostly
# made of; ``foiz_wt_sec_merk_and_friends.py`` carries that as an explicit TODO at its top, and
# for metigah and mayela it could hardly do otherwise, each sharing a codepoint with the accent
# it is a positional name for.  So the sentence claims coverage of two accents, not of the table.
_FOI_SEC_MERK = _FOI.format("sec-merk")
_FOI_SEC_MISC = _FOI.format("sec-misc")
# The ``unicode`` list has "geresh plus telisha gedolah" and the gershayim counterpart as two of
# its rare-sequence sections -- the very words the one-letter appendix shows.
_FOI_UNICODE = _FOI.format("unicode")
# The gray maqaf is the ``implicit-maqaf`` section of ``rare-tmpls``.
_FOI_RARE_TMPLS = _FOI.format("rare-tmpls")


def _split_pair(pair: str) -> tuple[str, str]:
    """A survey pair key as its two accents, or a build failure on any other shape.

    The poetic simple data has three-accent keys (``germ-mer-rev``, ``tsit-mah-rev``), so a
    bare ``pair.split("-")[0], pair.split("-")[1]`` would render such a key truncated rather
    than raise (item 12 of ``doc/review-findings-2026-07-29.md``).  This page reads MAM's
    prose data, which has none -- ``pin_claims`` asserts that too -- and a corpus bump that
    produced one must stop the build rather than show two accents of a three-accent key.
    """
    parts = pair.split("-")
    assert len(parts) == 2, f"not a two-accent pair key: {pair!r}"
    return parts[0], parts[1]


def _pair_rows(genre: dict, occurrences: list) -> list[dict]:
    """Every accent pair that occurs on a spreader, a concentrator or a simple chanted word of
    MAM's prose verses, in the order both tables below use, each with its three counts and an
    example of the spreader and simple ones.

    A CONCENTRATOR COUNT, NOT A THIRD TABLE (Ben, 2026-07-30: "the concentrators seem to belong
    to neither of these tables ... Which table would they fit into most seamlessly ... Or should
    they have their own table?").  A column, and in BOTH tables, because it costs neither of them
    a single row: all nine pairs a concentrator has already had one, three of them in the
    spreader table and six in the appendix.  A table of their own would have restated nine rows
    that are already on the page and split one pair's three counts across two places.  The
    ``concentrator_by_pair`` keys are in the row set all the same, so a corpus bump that produced
    a pair NO spreader and NO simple chanted word has gets a row of its own rather than vanishing
    from a total -- which the two tables' concentrator totals then assert.

    Rows are what the data holds, not a list from anywhere: the page reports the pairs that
    occur and no longer says which of Yeivin's categories each case falls under (Ben,
    2026-07-28).  Every compound hit lands in exactly one row, which ``_pair_table``'s total
    asserts.

    THE SIMPLE COUNT COVERS EVERY PAIR, since 2026-07-28.  It used to be restricted to the
    eight pairs the compound side has, because two marks on a chanted word are not always two
    accents and this scan has no accent tokenization to tell them apart.  ``simple_exclusion``
    now does tell them apart, mechanically and in the survey rather than here, so the count
    can be honest and complete at once: what it leaves out is counted, and ``_exclusion_note``
    says what and how much.  Ben's rule for the widening: leave out the pairs that are not
    meaningful -- a stress helper is not a second accent -- and disclose the exclusions.

    ONE ORDER FOR BOTH TABLES, settled here so the split cannot make them disagree.  Pairs
    sharing a first accent stay together rather than scattering by count (Ben, 2026-07-28, of
    the two mayela rows: "these should be listed together instead of strictly ordering by # of
    occurrences").  Groups run commonest-group-first, rows within a group commonest-first.  The
    count that orders them is the ROW TOTAL, all three counts together: ordering by the spreader
    count alone would put the commonest pair on a chanted word -- munax before zaqef qatan, 1,374
    of them -- last, on the strength of its single spreader.  The concentrator count joined that
    total when it joined the rows: a row now shows three counts, and ordering by two of them
    would be a rule nothing on the page states.
    """
    simple_by_pair = genre["simple_by_pair"]
    simple_examples = genre["simple_example_by_pair"]
    conc_by_pair = genre["concentrator_by_pair"]
    counts = Counter(_pair_of(o["shape"]) for o in occurrences)
    compound_examples: dict[tuple[str, str], dict] = {}
    for occurrence in occurrences:
        compound_examples.setdefault(
            _pair_of(occurrence["shape"]),
            {"word": occurrence["word"], "bcv": occurrence["bcv"]},
        )
    pairs = (
        set(counts)
        | {_split_pair(pair) for pair in simple_by_pair}
        | {_split_pair(pair) for pair in conc_by_pair}
    )

    def total_of(pair: tuple[str, str]) -> int:
        return (
            counts.get(pair, 0)
            + conc_by_pair.get("-".join(pair), 0)
            + simple_by_pair.get("-".join(pair), 0)
        )

    group_max = Counter()
    for pair in pairs:
        group_max[pair[0]] = max(group_max[pair[0]], total_of(pair))
    rows = []
    for pair in sorted(
        pairs,
        key=lambda p: (-group_max[p[0]], p[0], -total_of(p), p[1]),
    ):
        first, second = pair
        rows.append(
            {
                # TWO COLUMNS, not one reading "metigah before zaqef" (Ben, 2026-07-29: "let's
                # split this whole column into two: Acc1 and Acc2 (and hence 'before' is
                # dropped)").  The order is still the written order, which is what the headings'
                # hover text says; nothing but the word "before" carried that, and a column
                # named Acc1 beside one named Acc2 carries it without spending the width.
                "first": _PAIR_FIRST_NAME.get(pair, _ACCENT_DISPLAY[first]),
                "second": _PAIR_SECOND_NAME.get(pair, _ACCENT_DISPLAY[second]),
                "compound": counts.get(pair, 0),
                "compound_example": _example_cell(compound_examples.get(pair), pair),
                "conc": conc_by_pair.get("-".join(pair), 0),
                "simple": simple_by_pair.get("-".join(pair), 0),
                "simple_example": _example_cell(
                    simple_examples.get("-".join(pair)), pair
                ),
            }
        )
    # EVERY CONCENTRATOR IS IN ONE OF THE TWO TABLES.  The two split these rows on the spreader
    # count, so a row is in exactly one of them, and this says the rows between them account for
    # every concentrator the survey counted -- both that no ``concentrator_by_pair`` key fell out
    # of the row set and that the by-pair breakdown adds up to the whole.  It is the concentrator
    # counterpart of ``_pair_table``'s "rows sum to the hits", and it is here rather than in
    # either table because neither table can see the other's half.
    conc_total = sum(row["conc"] for row in rows)
    assert conc_total == genre["concentrators"], (
        f"rows sum to {conc_total} concentrators,"
        f" not the {genre['concentrators']} counted"
    )
    return rows


def _pair_table(rows: list[dict], hits: int) -> object:
    """The accent pairs that occur on a spreader -- a compound with an accent on a non-final
    atom -- with an example of each and how often each occurs on a simple chanted word as well.

    ONLY THE PAIRS A SPREADER HAS (Ben, 2026-07-29: "make the big ... table less big by
    banishing, to an appendix, rows with compound count equal to zero").  Widening the simple
    column to every pair had taken the table from eight rows to eighteen, and ten of those
    eighteen were an empty compound cell beside an empty example cell.  Those ten are
    ``_simple_only_table``, at the foot of the page.  The eight that stay are the ones the
    page's question is about, and every compound hit is still in one of them, which the total
    asserts.

    ONLY the column headings are ``th``.  The pair column is data, so it is ``td``: a ``th``
    there is bold and centered by browser default, which is what Ben asked about -- a bold
    centered first column claims the pair names are headings for their counts, and they are
    not.  Its rows are also then striped like any other data row.

    THE HEADINGS ARE ABBREVIATED, with the full wording on hover (Ben, 2026-07-28: "Use
    shorter headings ... because they are making the columns too wide", and 2026-07-29:
    "shorten 'Compound' and 'Simple' to 'C' and 'S' or something that doesn't artificially
    inflate the width of the row").  A count column is as wide as its heading when the heading
    is the longest thing in it, and three digits under the word "Compound" left the counts
    spread across the page; a single letter costs the column nothing, and the hover text says
    what it stands for.
    """
    body = [
        H.table_row(
            (
                *_ACC_HEADERS,
                # The spreader column is glossed "with an accent on a non-final atom" and never
                # as a bare "compound": the survey counts a compound here only when an accent
                # sits on a NON-FINAL atom, so a pair whose two accents both sit on the final
                # atom is invisible to it (item 2 of ``doc/review-findings-2026-07-29.md``).
                # That is what the Cnc column beside it now counts, so the two together do
                # cover the compounds -- which is why the gloss has to keep saying which one
                # each is.
                _count_header(_SPR, _SPREADER_GLOSS),
                _example_header(_SPR, _SPREADER_GLOSS),
                # THE CONCENTRATOR COLUMN TAKES NO EXAMPLE COLUMN.  Two more columns is the one
                # thing this table cannot afford -- its headings were abbreviated, twice, for
                # width alone -- and the page is not short of a concentrator to look at: the
                # intro shows one as a specimen, drawn from the commonest concentrator pair,
                # which is this column's own top row.
                _count_header(_CNC, _CONC_GLOSS),
                _count_header(_SIM, _SIMPLE_GLOSS),
                _example_header(_SIM, _SIMPLE_GLOSS),
            )
        )
    ]
    compound_total = conc_total = simple_total = 0
    for row in rows:
        if not row["compound"]:
            continue
        compound_total += row["compound"]
        conc_total += row["conc"]
        simple_total += row["simple"]
        body.append(
            H.table_row_of_data(
                (
                    _accent_cell(row["first"]),
                    _accent_cell(row["second"]),
                    str(row["compound"]),
                    row["compound_example"],
                    str(row["conc"]),
                    str(row["simple"]),
                    row["simple_example"],
                ),
                _PAIR_CELL_ATTRS,
            )
        )
    assert (
        compound_total == hits
    ), f"table rows sum to {compound_total}, not the {hits} hits"
    body.append(
        H.table_row_of_data(
            ("Total", "", str(hits), "", str(conc_total), str(simple_total), ""),
            _PAIR_CELL_ATTRS,
        )
    )
    return H.table(tuple(body), {"class": "centered-table accent-pair-table"})


def _simple_only_table(rows: list[dict]) -> object:
    """The pairs no spreader has, counted on concentrators and on simple chanted words.

    NOT "the pairs that occur on a simple chanted word only", which this docstring and the
    appendix's heading and sentence all said until 2026-07-30 (item 2 of
    ``doc/review-findings-2026-07-29.md``): six of these ten pairs do occur on maqaf
    compounds -- as concentrators, both accents on the final atom -- which the spreader
    criterion cannot see.  What is true of all ten is that no compound has one with its first
    accent on a non-final atom, and that is what the appendix now claims.

    NO SPREADER COLUMN AND NO SPREADER EXAMPLE COLUMN.  A spreader column of zeros beside an
    example column of blanks is what got these rows banished; carrying the two columns down
    here would carry the width down with them.

    A CONCENTRATOR COLUMN, THOUGH (Ben, 2026-07-30), and it is the column that makes the
    appendix's own claim readable: six of these ten pairs do occur on a maqaf compound, with
    both accents on its last atom, and until this column there was nothing on the page a reader
    could see that in.  It costs no row, every concentrator pair already having one.
    """
    body = [
        H.table_row(
            (
                *_ACC_HEADERS,
                _count_header(_CNC, _CONC_GLOSS),
                _count_header(_SIM, _SIMPLE_GLOSS),
                _example_header(_SIM, _SIMPLE_GLOSS),
            )
        )
    ]
    conc_total = simple_total = 0
    for row in rows:
        if row["compound"]:
            continue
        conc_total += row["conc"]
        simple_total += row["simple"]
        body.append(
            H.table_row_of_data(
                (
                    _accent_cell(row["first"]),
                    _accent_cell(row["second"]),
                    str(row["conc"]),
                    str(row["simple"]),
                    row["simple_example"],
                ),
                _SIMPLE_ONLY_CELL_ATTRS,
            )
        )
    body.append(
        H.table_row_of_data(
            ("Total", "", str(conc_total), str(simple_total), ""),
            _SIMPLE_ONLY_CELL_ATTRS,
        )
    )
    return H.table(tuple(body), {"class": "centered-table accent-pair-table"})


def _example_cell(example: dict | None, pair: tuple[str, str]) -> object:
    """One example form for a table cell, or an empty cell where the pair does not occur.

    Letters and accents only, as everywhere on these pages, and lifted from the survey rather
    than retyped.  The maqaf ``accents_and_letters`` drops is put back, so a compound example
    reads as the one chanted word it is.

    WHERE THE FORM IS FROM, on hover, and with NO dotted underline (Ben, 2026-07-29: "provide
    biblical locations (book-chapter-verse) as hover text but avoid dotted-underline styling
    since I think it will likely interfere with seeing the word properly (in particular ... the
    word's under-accents (if any)").  So the title goes on the ``hbo`` span itself rather than
    on an ``abbr``: the dotted rule in gh-pages/style.css is scoped to ``th abbr[title]``, and
    a mark under the last letter would sit right where that underline is drawn.

    ONE U+05BD SURVIVES IN THE SILLUQ ROWS, and none anywhere else.  ``accents_and_letters``
    drops the codepoint, rightly: it is not an accent, and in any other row it would be a meteg
    the pair says nothing about.  But in a row whose second accent IS the silluq, dropping it
    leaves an example showing one mark where the row promises two -- which is what the first
    pass of this table did.  The one kept is the LAST in the chanted word, which is the silluq;
    an earlier one is an ordinary meteg, and ש֥לֽף־חֽרב showed both until this narrowed.  Same
    rule ``atom_accents`` applies, and the pair is what says the rule applies at all.
    """
    if not example:
        return ""
    return _hebrew_at(example, silluq_second=_ACCENT_DISPLAY[pair[1]] == ROM_SILLUQ)


def _hebrew_at(example: dict, *, silluq_second: bool = False) -> object:
    """The example's letters and accents, titled with the verse it is from.

    The title goes through ``_ref_abbrev``, as the intro's e.g. sentences do: hover text is
    prose, and ``ref_display``'s raw mb_cmn book names ("Levit 21:4", "2Chronicles 8:11") are
    not how prose names a verse (item 7 of ``doc/review-findings-2026-07-29.md``).
    """
    return H.span(
        _form_at(example, silluq_second=silluq_second),
        {"lang": "hbo", "title": _ref_abbrev(example["bcv"])},
    )


def _form_at(example: dict, *, silluq_second: bool = False) -> str:
    """The example's letters, accents and maqafs -- and one U+05BD when it is a silluq."""
    chanted_word = example["word"]
    silluq_at = chanted_word.rfind(mpa.METEG) if silluq_second else -1
    return "".join(
        ch
        for i, ch in enumerate(chanted_word)
        if is_base_letter(ch)
        or mpa.is_accent(ch)
        or i == silluq_at
        or ch == "\N{HEBREW PUNCTUATION MAQAF}"
    )


def _exclusion_note(genre: dict) -> object:
    """The one exclusion from the simple column worth telling a reader about, with its figures
    spliced.

    Ben, 2026-07-28, asking for the widened column: "perhaps put a sort of footnote (not
    literally a footnote) listing these exclusions, for transparency".  So it is an ordinary
    paragraph under a table, in the page's voice, and each count comes out of the survey.

    WHICH TABLE it goes under is ``_appendix_section``'s docstring; it stopped being the prose
    section's on 2026-07-29.

    IT IS SYNCHRONIZED WITH THE APPENDIX'S OWN OPENING, Ben having merged the two wordings on
    2026-07-30 -- "two accents on the same letter" (which is what the exclusion is keyed on,
    where "two accents graphically" left the reader to guess what the graphical fact was) and
    "both accents likely belong to the same syllable" (which is why, stated once rather than as
    a doubt about what is not clear).  ``_one_letter_appendix_section`` says the same in the
    shorter form the appendix can afford, having just named the words.  Reword one and reword
    the other.

    IT NO LONGER NAMES THE MARKS, since the same day.  It used to spell out how many of the
    words were a geresh or gershayim with a telisha gedolah and how many a mahapakh with a
    qadma, which is now the appendix's Acc1/Acc2 columns and its Type column; a sentence that
    itemizes a table two sections down is a sentence a reader has to hold in their head.

    THE STRESS-HELPER EXCLUSION IS NOT MENTIONED, though ``simple_exclusion`` applies it and
    the survey counts it.  A first pass opened this paragraph with it -- so many words in which
    the two marks are a stress helper and the accent it helps, one accent written twice.  Ben:
    that is "a deep implementation detail that should not be mentioned.  No one would think,
    'oh how would you deal with zarqa stress helpers? were there none in MAM, or just not
    included in this table?  Of course they are not included in this table, that is obvious and
    therefore you don't have to make a methodological note'."  A reader takes a stress helper
    for granted; what they would not take for granted is two marks on ONE letter, which is why
    that one keeps its sentence.  (He also rejected the naming: the pair is conceptually a
    zarqa stress helper before a zarqa, the ``tsinnorit``/``tsinnor`` names being Unicode's
    misnaming rather than the accents'.)

    The total the paragraph used to open with went with the stress-helper sentence.  It was
    every simple chanted word with two different marks, so quoting it would leave a reader to
    subtract, find a remainder this paragraph does not explain, and go looking for the very
    detail Ben cut.
    """
    one_letter = genre["simple_excluded"][mpa.SIMPLE_EXCL_ONE_LETTER]
    words = _one_letter_words(genre)
    telisha = one_letter["ger-telg"] + one_letter["ger2-telg"]
    mahapakh = one_letter["mah-qad"]
    assert telisha + mahapakh == len(words), (one_letter, len(words))
    return H.para(
        (
            f"The simple counts on this page leave out {_count(telisha + mahapakh)} chanted"
            " words that have two accents on the same letter, because both accents likely"
            " belong to the same syllable.",
            *[" ", link("They are listed in an appendix below", _ONE_LETTER_HREF), "."],
        )
    )


def _one_letter_words(genre: dict) -> list[dict]:
    """The chanted words the one-letter rule sets aside, in corpus order.

    The counts beside them in ``simple_excluded`` are by pair, so they cannot say WHICH words
    these are; ``_exclusion_note`` asserts the two derivations agree in number, which is what
    stops the appendix and the sentence above it from drifting apart.
    """
    return [
        w
        for w in genre["simple_excluded_words"]
        if w["reason"] == mpa.SIMPLE_EXCL_ONE_LETTER
    ]


def _count(n: int) -> str:
    """A small count spelled out, a large one in digits -- for prose, not for table cells."""
    return _SMALL_NUMBERS[n] if n < len(_SMALL_NUMBERS) else f"{n:,}"


# GONE with the classification: _case_parts and _case_table, which listed the four cases the
# categories could not name or reach, verse by verse.  With the rows themselves gone there is
# nothing to list.  Their leading-numeral fix for mb_cmn's "2Samuel" went with them and is back
# inside ``_ref_abbrev`` -- which every book name out of a bcv now goes through.  The intro's
# e.g. sentences are one consumer; ``_hebrew_at``'s hover titles are the other, and they were
# left on the raw mb_cmn names ("Levit 21:4", "2Chronicles 8:11") while an earlier version of
# this comment called the case tables "the only thing that ever needed a book name out of a
# bcv" (item 7 of ``doc/review-findings-2026-07-29.md``).


def _specimen(example: dict, *, silluq_second: bool = False) -> object:
    """A pointed Hebrew form on a centered line of its own, nothing beside it.

    Ben, 2026-07-28: "why would you only describe in words what can be shown in Unicode?";
    2026-07-29, of the intro's two e.g. forms: "lately I'm preferring to show pointed hebrew
    specimens as a separately displayed element (centered, with line breaks)".  The verse is
    neither hover text ("rather than hidden as hover-text", same day) nor in parens on the
    specimen's own line: it is in the sentence above, in parens right after the "e.g." (his
    third form of the same day, superseding the other two) -- so unlike the table cells'
    forms, a specimen has no hover title, and the sentence is what names its verse.

    A first ``_specimen`` went with the three printed cases when they became a table -- a
    form is a cell there, ``_render_span``'s job -- along with the running sentence that
    flowed through three of them.  This one differs from that one in taking a survey record
    rather than a string: the form is lifted, like every other example the page shows.
    """
    return H.para(
        hbo(_form_at(example, silluq_second=silluq_second)),
        {"class": "hebrew-specimen"},
    )


def _ref_abbrev(bcv: str) -> str:
    """The bcv as visible prose names a verse -- "Gen. 2:7", "1 Chr. 15:17".

    Written here and moved to ``almost_errors_html_shared`` when
    ``wlc_chanted_word_residue_page`` wanted the same spelling.  The name stays as this page's
    call sites have it."""
    return ref_abbrev(bcv)


# The letters the three printed cases are found by -- bare letters, no marks, the marks being
# exactly what must not be retyped here.  A search PATTERN is one tuple per chanted word, holding
# that word's atoms in order, so it fixes the grouping as well as the letters.
_LO = "לא"
_TAASE = "תעשה"
_YIHYE = "יהיה"
_LEKHA = "לך"
# What follows the Sabbath commandment's לא־תעשה, and tells it from the one at Deuteronomy 5:8.
_KOL_MELAKHA = ("כל", "מלאכה")
_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"


def _letters(chanted_word: str) -> str:
    return "".join(ch for ch in chanted_word if is_base_letter(ch))


def _atom_letters(chanted_word: str) -> tuple[str, ...]:
    return tuple(_letters(atom) for atom in chanted_word.split(_MAQAF))


def _accents(atom: str) -> list[str]:
    return [ch for ch in atom if mpa.is_accent(ch)]


@lru_cache(maxsize=None)
def _p_trad_strand(book: str, reading: str) -> dict:
    """The one vendored p-trad strand for a book and a strand name.

    Cached because ``load_source`` re-reads and re-parses the whole vendored file every call, and
    the four strands here are asked for once per case and once per claim pinned.

    EVERY strand this page reads is the p-trad one, which is why the tradition is fixed here
    rather than passed in.  The intro says that once, and the individual mentions then carry the
    book and the strand name alone (Ben, 2026-07-29: "noting, in introducing the whole thing,
    that everything is p-trad (no need to redundantly qualify everything as p-trad)").  That
    supersedes the per-mention "the p-trad עליון" of earlier the same day.
    """
    return next(
        v
        for v in pd.load_source()["versions"]
        if (v["book"], v["reading"], v["tradition"]) == (book, reading, "printed")
    )


def _find_span(
    version: dict, pattern: tuple[tuple[str, ...], ...], show: int
) -> list[str]:
    """The one run of chanted words in a strand whose atoms are ``pattern``, less its context.

    ``pattern`` fixes the GROUPING as well as the letters: ``((_LO,), (_TAASE, _LEKHA))`` is לא
    standing by itself before the compound תעשה־לך, and matches neither a strand that has
    לא־תעשה as one compound nor one that has תעשה by itself.  ``show`` is how many of the matched
    words the caller displays; any beyond that are in the pattern only to tell two sites apart.
    A strand's two לא־תעשה compounds are byte-identical, so what tells them apart is what
    follows -- לך at Exodus 20:4 and Deuteronomy 5:8, כל־מלאכה at the Sabbath commandment.

    Raising on anything but one match is the whole point.  The matches were collected into a SET
    until 2026-07-29, which deduped those two byte-identical sites away and let the assertion
    pass without distinguishing them (item 14 of ``doc/review-findings-2026-07-29.md``).
    """
    hits = []
    for chanted_verse in version["chanted_verses"]:
        words = chanted_verse.split()
        for start in range(len(words) - len(pattern) + 1):
            run = words[start : start + len(pattern)]
            if tuple(_atom_letters(word) for word in run) == pattern:
                hits.append(run[:show])
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


def _render_span(words: list[str]) -> str:
    """A run of chanted words as a table cell shows it: letters and accents, maqafs kept.

    The cells ARE the comparison, so nothing is described in words that can be shown (Ben,
    2026-07-28: "why would you only describe in words what can be shown in Unicode?", and
    2026-07-29: "I need to just see this using actual unicode").  ``accents_and_letters`` reduces
    each atom to its letters and accents -- no vowels, and no meteg, which is not an accent --
    and the maqafs it drops go back between the atoms they joined, so a compound reads as the one
    chanted word it is.

    A span runs to whatever length keeps every chanted word in it WHOLE in all three columns.
    The two Exodus cases therefore carry לך: the עליון joins it to the second atom, and half of
    a compound is not a thing this page shows.  The Deuteronomy case ends at תעשה, no column
    joining that atom to anything further on.
    """
    return " ".join(
        _MAQAF.join(accents_and_letters(atom) for atom in word.split(_MAQAF))
        for word in words
    )


def _sole_accent(atom: str) -> str:
    """The one accent on an atom the page shows, or a build failure."""
    accents = _accents(atom)
    assert len(accents) == 1, atom
    return accents[0]


_KOREN = "Koren"
_KOREN_HREF = "printed-decalogue-koren.html"
# NO DETERMINER IN THE TABLE CELL (Ben, 2026-07-30: 'In the "Edition" row, drop "the" from "the
# Simanim Tiqqun"').  This is not the bare "Simanim" the standing rule bans -- both words are
# here, so the cell still names which of Feldheim's two editions it is.  What it drops is the
# article, and the rule that asks for one is a rule about PROSE: a cell in an Edition row is a
# label beside "Koren", not a sentence, and "the Simanim Tiqqun" in a column of names reads as
# though the article were part of the name.  Running prose on this page still writes "the
# Simanim Tiqqun", which is why this constant is not simply reused there.
_SIMTIQ = "Simanim Tiqqun"
_SIMTIQ_HREF = "printed-decalogue-simanim.html"


def _koren_case() -> dict:
    """Koren's לא־תעשה, beside both Deuteronomy strands.

    An accent typed by hand into a page module is a claim with no oracle behind it, and this one
    is the page's whole subject, so every form here is lifted from a vendored strand.  Koren's
    own cell is CONSTRUCTED: the עליון has the two atoms as two chanted words at the Sabbath
    commandment (Deuteronomy 5:14), Koren's appendix page has the same two atoms with the same
    two accents as one maqaf compound, and the maqaf is the whole of the difference -- so the
    two words are joined with a maqaf, and nothing else is touched.

    The תחתון has those atoms as one compound at that same commandment, which is what lets the
    prose raise a carry-over, and its own accent is asserted here: the compound's joined לא has
    no accent and its תעשה a qadma.  A re-vendoring that moved either mark fails the build rather
    than put a cell on the page that no longer contrasts with the cells beside it.

    The accented-alike answer the intro gives rests on Koren's two accents being ONE accent
    twice, so that is asserted too rather than left to the reader of ``unprecedented_pairs``.
    """
    elyon = _find_span(_p_trad_strand("dt", "elyon"), ((_LO,), (_TAASE,)), 2)
    lo, taase = (accents_and_letters(word) for word in elyon)
    pair = (_sole_accent(lo), _sole_accent(taase))
    assert pair[0] == pair[1], pair
    taxton = _find_span(
        _p_trad_strand("dt", "taxton"), ((_LO, _TAASE), _KOL_MELAKHA), 1
    )
    joined_lo, joined_taase = taxton[0].split(_MAQAF)
    assert not _accents(joined_lo), taxton
    assert _accents(joined_taase) == [am.QADMA], taxton
    return {
        "edition": _KOREN,
        "href": _KOREN_HREF,
        "book": "Deuteronomy",
        "strand": ELYON,
        "printed": f"{lo}{_MAQAF}{taase}",
        "same": _render_span(elyon),
        "other": _render_span(taxton),
        "pair": pair,
    }


# The Simanim Tiqqun's two cases: the second atom of each compound, and the accent that atom has.
# The two accents differ, which is what makes these two cases rather than one.
_SIMTIQ_CASES = ((_YIHYE, am.MERKHA), (_TAASE, am.QADMA))


def _simtiq_case(second_letters: str, second_accent: str) -> dict:
    """One of the Simanim Tiqqun's two compounds, beside both Exodus strands.

    THE EDITION'S CELL IS CONSTRUCTED, and the construction is the page's own claim about the
    edition, so it is worth stating exactly.  A hand transcription records the printed ACCENTS
    and nothing else (``edition_transcription``), so there is no Unicode anywhere in the repo for
    what the Simanim Tiqqun's page has; what there is, is the strand it is compared against and a
    transcription that differs from it in one mark per compound -- a munaḥ on the joined לא where
    the strand has a meteg.  So the strand's compound is read, the meteg is replaced by that
    munaḥ where it stands, and everything else -- the letters, the accent on the second atom -- is
    the strand's.  The transcription's own tokens for these two compounds are ``mun-mer`` and
    ``mun-qad``, on printed line 14 of ``simtiq_ex_taxton``, and the ``mun-qad`` is Exodus 20:4's
    לא־תעשה: the Sabbath commandment's is ``qad`` alone, with no munaḥ.  That is why the pattern
    below runs on to לך.

    ONE STRAND, NAMED, not "every strand".  Ben, 2026-07-29: "Really? 'Every strand' from what
    'universe' of strands?"  Two things were wrong with the sentence that stood here.  The
    universe was undefined -- this page is not about the printed Decalogues, so unlike the trio it
    has no established set for "every" to range over.  And the claim was FALSE on the wider
    reading it invited: of the eight transcribed versions, the Deuteronomy תחתון pair has לא־יהיה
    with no meteg on the joined לא at all.  The table names the two strands each case is set
    beside, and the assertions below cover exactly those two.

    THE OTHER STRAND IS WHERE THE MUNAḤ ALREADY IS, which is the observation the whole reframe
    turns on and the reason the עליון is asserted rather than merely displayed: the Exodus עליון
    has לא as a chanted word by itself with a munaḥ on it, the very mark the Simanim Tiqqun has
    on its joined לא.  Same shape as Koren's carry-over, running the other way -- Koren's maqaf
    is what the other Deuteronomy strand has, and this munaḥ is what the other Exodus strand has.
    """
    taxton = _find_span(
        _p_trad_strand("ex", "taxton"), ((_LO, second_letters), (_LEKHA,)), 2
    )
    lo, second = taxton[0].split(_MAQAF)
    assert mpa.METEG in lo, taxton
    assert not _accents(lo), taxton
    assert _accents(second) == [second_accent], taxton
    printed = [f"{lo.replace(mpa.METEG, am.MUNAX)}{_MAQAF}{second}", *taxton[1:]]
    elyon = _find_span(
        _p_trad_strand("ex", "elyon"), ((_LO,), (second_letters, _LEKHA)), 2
    )
    assert _sole_accent(elyon[0]) == am.MUNAX, elyon
    return {
        "edition": _SIMTIQ,
        "href": _SIMTIQ_HREF,
        "book": "Exodus",
        "strand": TAHTON,
        "printed": _render_span(printed),
        "same": _render_span(taxton),
        "other": _render_span(elyon),
        "pair": (am.MUNAX, second_accent),
    }


def printed_cases() -> tuple[dict, ...]:
    """The three printed cases the intro is about, one row each.

    THREE CASES, TWO COMPOUNDS, TWO BOOKS -- Ben's own question, 2026-07-29: "are there really
    three words/word-pairs, since לא־תעשה has issues in both Koren and SimTiq".  There are three
    rows: לא־תעשה is one compound but two cases, Koren's in Deuteronomy and the Simanim Tiqqun's
    in Exodus, and a row is what one edition has at one place in one book.  Merging the two
    לא־תעשה cases into a row would have to merge two editions, two books and two strands with
    them.

    KOREN AND THE SIMANIM TIQQUN ARE ON A PAR (Ben, same day: the Simanim Tiqqun "really on a par
    with Koren, i.e. the document isn't primarily Koren with SimTiq as an afterthought").  What
    that replaced was a Koren paragraph in running prose followed by a shorter one opening "Koren's
    is not the only such compound in print" -- the afterthought framing in one clause.  Same
    columns, same derivations, one table: neither edition is the other's footnote.  Koren stays
    the first row only because the prose above names it first and the answer below answers it
    first.
    """
    return (_koren_case(), *(_simtiq_case(*case) for case in _SIMTIQ_CASES))


def unprecedented_pairs() -> tuple[tuple[str, str], ...]:
    """The accent pair of each of the three printed compounds the page asks about.

    Derived from the very forms the table shows -- Koren's from the two atoms it joins, the
    Simanim Tiqqun's from the munaḥ that construction puts on the joined לא and the accent
    ``_SIMTIQ_CASES`` names on the second atom.  So a re-vendoring that changed any of the three
    would change what ``pin_claims`` looks for, rather than leaving the page asserting the absence
    of a pair it no longer shows.
    """
    return tuple(case["pair"] for case in printed_cases())


def _mark_display(mark: str) -> str:
    """One mark codepoint as the page's own romanization -- ``maqaf``, ``munaḥ``.

    An accent goes through ``_ACCENT_DISPLAY``, the same route ``_pair_in_words`` takes, so a
    re-vendoring that changed which accent an edition adds renders that accent's real name
    rather than a name typed in beside it -- and an accent the page has no romanization for
    raises rather than reaching a reader as a code identifier.  The maqaf is not an accent and
    so is not in that table; ``ROM_MAQAF`` is its single source, as ``ROM_*`` is for the rest.
    """
    if mark == _MAQAF:
        return ROM_MAQAF
    return _ACCENT_DISPLAY[mpa.shape_of([[mark]])]


def _added_mark(case: dict) -> str:
    """The one mark the printed compound has that its Wikisource strand of the same name lacks.

    Ben, 2026-07-30, asking for the row: “+maqaf” (meaning, “maqaf added”) and “+munaḥ”
    (meaning “munaḥ added”) as appropriate.  Which of the two a case takes is DERIVED from the
    two forms the table already shows rather than typed in per case: the Strange row's cell and
    the Reference row's cell, differenced as multisets of characters.  So the row cannot come to
    disagree with the two rows it summarizes, and a re-vendoring that changed either form fails
    the build here rather than leaving a “+maqaf” standing over a column that no longer has one.

    SPACES ARE DROPPED BEFORE DIFFERENCING, which is what makes Koren's case come out as an
    addition at all: its Wikisource עליון has לא and תעשה as two chanted words, Koren has them as
    one compound, and the maqaf is exactly the mark that difference consists of.  Adding a maqaf
    IS replacing the space with one, so the space is not a mark the row would want to name.

    THE DIFFERENCE IS OVER THE FORMS THE READER SEES -- letters and accents, no vowels and no
    meteg, ``_render_span``'s reduction.  For the Simanim Tiqqun's two that is the whole of the
    honesty of “+munaḥ”: the strand's joined לא has a meteg there, which is not an accent and is
    not shown in either cell, so what the column adds to what the reader can see is the munaḥ and
    nothing else.  ``_simtiq_case``'s docstring is where the meteg it stands in place of is
    recorded.

    The assertions are the point.  Nothing removed, and exactly one thing added, is what lets the
    row say “+X” at all; a case that differed in two marks, or that dropped one, would need a
    cell this row has no way to write, and the build stops instead.
    """
    printed = Counter(case["printed"].replace(" ", ""))
    same = Counter(case["same"].replace(" ", ""))
    added, removed = printed - same, same - printed
    assert not removed, (case["edition"], case["book"], removed)
    assert sum(added.values()) == 1, (case["edition"], case["book"], added)
    return f"+{_mark_display(next(iter(added)))}"


def _pair_key(pair: tuple[str, str]) -> str:
    """A pair of accent codepoints as the survey writes it -- ``mun-mer``."""
    return "-".join(mpa.shape_of([[accent]]) for accent in pair)


def _pair_in_words(pair: tuple[str, str]) -> str:
    """A pair of accent codepoints in the page's own romanizations, dash-joined.

    ``munaḥ–munaḥ``, not "a munaḥ before a munaḥ", which is what this returned until
    2026-07-30.  The answer paragraph now names three pairs in one sentence instead of two,
    and three of the longer form is a sentence a reader has to parse rather than read.  Ben's
    own sketch of the rewrite writes them dash-joined, and the page has the form already --
    ``printed_decalogue_strands``' ``ROM_TIPEHA_ETNAHTA`` joins an accent pair with the same
    en dash.  The order is the written order, as everywhere else on this page.
    """
    first, second = (_ACCENT_DISPLAY[mpa.shape_of([[a]])] for a in pair)
    return f"{first}–{second}"


def pin_claims(survey: dict) -> None:
    """Fail the build if the data stops supporting a claim the prose states in words.

    The counts on this page are spliced from the survey, so they cannot drift.  Its
    ARGUMENT cannot be spliced, and every sentence of it rests on a handful of facts that a
    re-vendoring or a corpus bump could quietly overturn.  So they are pinned here, and this
    raises rather than warns -- the same build-fails-on-data-drift behavior
    ``printed_decalogue_strands.resolve_readings`` has, and for the same reason: a warning in
    a generator's output is a warning nobody reads.
    """
    # GONE with the classification (2026-07-28): two assertions that pinned sentences the page
    # no longer makes -- that MAM's prose has no bare-habit (route (b)) case, and that exactly
    # one route-(a) case falls under no named configuration.  Both were about which of Yeivin's
    # categories a case belongs to, and the page now reports the pairs that occur without
    # placing any case in a category.  The survey still computes the routes; nothing on the page
    # depends on them, so nothing here defends them.

    # The oleh-we-yored assertions that stood here went with the poetic section's detail (wlc-utils#83).
    # They defended a sentence counting how many poetic hits were one oleh-we-yored spread across
    # a compound rather than two accents; the section now says only that the poetic system is a
    # different matter, and pins nothing beyond the spliced hit count.

    # The intro speaks for MAM, and its spreader sentence says the two accents of a spreader
    # sit on two atoms -- one accent each, never a stacked pair.  That is also the spreader
    # half of "but never more than two" (Ben's wording, 2026-07-28): exactly two accented
    # atoms and no stacked pair is what "never more than two" amounts to for a spreader.  None
    # of that is spliced, so it is pinned: one atom with a stacked pair, or one hit with a
    # single accent, would leave those words quietly wrong -- and each of those does occur
    # elsewhere in the survey (WLC's Joshua 20:4 has the single accent, the poetic corpus has
    # revia mugrash), so neither is a hypothetical.  A field of REPEATS is the one thing
    # allowed: MAM's Ezekiel 16:12 נֶ֙זֶם֙ has ``pash+pash``, one accent written twice.
    #
    # ``atoms[-1] != "0"`` pins the intro's parenthetical, "(One of the two is always on the
    # last atom.)".  An accented final atom is nothing the scan requires -- a non-final accent
    # alone is enough to count a compound -- and other corpora do have hits with a blank final
    # field, WLC's Joshua 20:4 among them, so this is the one claim on the page that only the
    # data can keep true and it is not a hypothetical.
    #
    # BACK with the spreader table (2026-07-30): ``len(atoms) in (2, 3)``, which had GONE with
    # the spreaders-vs-concentrators rewrite the day before, its sentence ("the compound itself
    # having two atoms, or occasionally three") having gone with it.  What needs it now is a
    # claim made in Unicode rather than in words: the table's three rows are one per KIND of
    # spreader -- two atoms, three with the first accented, three with the middle accented --
    # and a four-atom compound would leave those three a tour of part of the field, with
    # nothing on the page saying so.  A table is as much a claim as a sentence, and is pinned
    # like one.
    #
    # MIND THE SCOPE: the survey scans maqaf compounds, so the pins here cover compounds only.
    # A chanted word that is a lone atom is never scanned, and "never more than two" speaks for
    # those too.
    for o in _occurrences(survey, "mam_simple", "prose"):
        atoms = o["shape"].split("-")
        assert len([a for a in atoms if a != "0"]) == 2, o
        assert all(len(set(a.split("+"))) == 1 for a in atoms), o
        assert atoms[-1] != "0", o
        assert len(atoms) in (2, 3), o

    # THE CONCENTRATOR HALF of the same sentence pair (2026-07-29): "some concentrate both of
    # those two accents on the last atom", and with it that kind's half of "but never more
    # than two".  Re-derived from the shapes rather than trusted to the scan: every counted
    # concentrator shape has all of its non-final fields empty and exactly two different
    # accents in its final field.  The scan's own criterion is merely "more than one", so a
    # compound whose final atom had three different accents would land here and stop the
    # build, as it should: it would falsify both sentences.
    # THE BREUER SENTENCE under the spreader table (2026-07-31), which says that the three rows
    # CoS ch. 9 §37 licenses on a compound -- the metigah, and the mayela under each of the two
    # emperors it serves -- are N of the M spreaders.  Both numbers are spliced, so neither can
    # drift; what cannot be spliced is that all THREE rows are still there to be summed, and that
    # the sum is a part rather than the whole.  A corpus bump that emptied one of them would
    # leave the sentence naming a pair the table no longer has, and one that emptied the other
    # thirteen would leave "those three pairs are 233 of the 233" reading as a rule with no
    # exceptions -- which is exactly what Breuer's §37 claims and this page does not.
    spreaders = _spreaders_by_pair(survey)
    for pair in _BREUER_MAQAF_SURVIVING:
        assert spreaders[pair], f"no spreader left with the pair {pair}"
    maqaf_surviving = sum(spreaders[pair] for pair in _BREUER_MAQAF_SURVIVING)
    hits = _n(survey, _CORPUS, "prose", "hits")
    assert 0 < maqaf_surviving < hits, f"{maqaf_surviving} of {hits} is not a part"

    genre = survey["corpora"][_CORPUS]["prose"]
    for shape in genre["concentrator_by_shape"]:
        fields = shape.split("-")
        assert all(field == "0" for field in fields[:-1]), shape
        assert len(set(fields[-1].split("+"))) == 2, shape

    # THE SIMPLE HALF of the same "but never more than two" (item 12 of
    # ``doc/review-findings-2026-07-29.md``).  The intro's sentence speaks of the prose
    # system's chanted words whether compound or simple; the spreader and concentrator pins
    # above cover the compounds, and this covers the rest: every pair the survey records for
    # MAM's prose verses -- counted or excluded, simple or concentrator -- is exactly two
    # accents.  PROSE ONLY, deliberately, matching the sentence's own scope: the poetic
    # simple data has three-accent keys (``germ-mer-rev``, ``tsit-mah-rev``), and the
    # sentence says nothing of the poetic system, so those keys falsify nothing --
    # ``_split_pair`` is what keeps them off the page.
    for key in (
        *genre["simple_by_pair"],
        *genre["concentrator_by_pair"],
        *(k for by_pair in genre["simple_excluded"].values() for k in by_pair),
        *(k for by_pair in genre["concentrator_excluded"].values() for k in by_pair),
    ):
        assert len(key.split("-")) == 2, f"not a two-accent pair key: {key!r}"

    # GONE with the answer's Koren half (Ben, 2026-07-30): the assertion that no compound in
    # MAM's prose verses is accented alike twice.  It pinned a sentence the page no longer makes
    # -- "No maqaf compound in MAM's prose verses has the same accent on both atoms, not once,
    # which disposes of Koren's" -- and Ben dropped that sentence in favor of answering Koren's
    # munax-munax as one pair among the three, "even though it is a stronger claim, and arguably
    # more interesting".  Koren's own pair is still pinned, by the loop below, which is where all
    # three are now defended alike; what is no longer defended is the wider sameness claim,
    # because nothing on the page states it.  The module's rule holds either way: an assertion
    # here exists to defend a sentence, and outlives it only as a trap for a later reader.
    #
    # Two facts it carried are worth keeping even though the assertion is not:
    #   * It was PROSE ONLY, deliberately.  The intro once said "not in poetic ones" too, and
    #     the poetic verses do bear it out -- but only among compounds whose maqaf is WRITTEN,
    #     and Breuer has the poetic maqaf after a secondary mark customarily left unwritten, so
    #     a compound accented alike twice with an unwritten maqaf is invisible to this scan.
    #     Ben, 2026-07-27: drop the clause rather than qualify it.
    #   * Two assertions about Isaiah 40:7 had stood beside it, that it is the single compound
    #     whose non-final atom has a munax and that it pairs that munax with a zaqef qatan.  The
    #     verse is still on the page, as the compound example in the table's munax-before-zaqef
    #     row, spliced rather than named in prose, so the row is what defends it now.

    # THE THREE PRINTED COMPOUNDS, all pinned alike (Ben, 2026-07-29, on being told that the
    # Simanim Tiqqun's two are unprecedented by the same test: "please reframe the page like
    # that"; and 2026-07-30, folding Koren's into the same frame).  Each pair occurs on no
    # chanted word of MAM's prose verses at all -- not on a spreader, not on a concentrator (a
    # place this check could not look before the survey recorded them, 2026-07-29), not on a
    # simple chanted word, and not among the words the exclusion rules set aside.  Since the
    # intro stopped answering Koren's separately this loop IS the answer, all of it, for all
    # three -- there is no longer a second half for it to meet.
    for pair in unprecedented_pairs():
        key = _pair_key(pair)
        assert key not in genre["simple_by_pair"], key
        assert key not in genre["concentrator_by_pair"], key
        for excluded in (genre["simple_excluded"], genre["concentrator_excluded"]):
            for by_pair in excluded.values():
                assert key not in by_pair, key
        assert not [
            o
            for o in _occurrences(survey, _CORPUS, "prose")
            if "-".join(_pair_of(o["shape"])) == key
        ], key


def _intro(survey: dict) -> tuple[object, ...]:
    # The headline frequency is MAM's, not WLC's.  A claim about what the accentuation DOES
    # wants a consensus text; WLC is one manuscript as one transcription reads it, and its
    # blemishes are visible in this very count (Joshua 20:4 זקני־העיר, whose compound has its
    # only accent on the non-final atom because the mark on העיר is a mid-verse meteg).  WLC and
    # UXLC keep their table columns, which are about the texts themselves; what they no longer do
    # is answer the page's question.  Ben, 2026-07-26: "let's leave WLC (and indeed the LC) out of
    # this" -- so the two WLC compounds with a munax on each atom (2 Chr 1:11, 1 Chr 27:14), and
    # the paragraphs that read them as Koren's nearest precedent, are gone rather than demoted.
    mam_prose = survey["corpora"]["mam_simple"]["prose"]
    pct = 100.0 * mam_prose["hits"] / mam_prose["maqaf_compounds"]
    conc_pct = 100.0 * mam_prose["concentrators"] / mam_prose["maqaf_compounds"]
    # THE LIFTED EXAMPLES, one kind of spreader per row of the table below and one concentrator
    # beside it (Ben, 2026-07-29, asking for the spreaders-vs-concentrators framing "e.g."
    # each).  The first spreader is the first two-atom metigah-zaqef in the survey's order --
    # the commonest spreader kind in its plainest shape -- and the concentrator is the stored
    # example of the commonest concentrator pair.  Every lookup stops the build rather than let
    # a sentence stand beside a form that is no longer there.
    spreader_qad_zaq = [
        o for o in _occurrences(survey, _CORPUS, "prose") if o["shape"] == "qad-zaq"
    ]
    assert spreader_qad_zaq, "no two-atom metigah-zaqef spreader to show"
    conc_by_pair = mam_prose["concentrator_by_pair"]
    assert conc_by_pair, "no concentrator pair to show"
    conc_pair = next(iter(conc_by_pair))  # the commonest: the survey orders by count
    conc_example = mam_prose["concentrator_example_by_pair"][conc_pair]
    # THE OTHER TWO ROWS: the three-atom spreaders, which come in two kinds and so take a row
    # each.  Where the accent that is not on the last atom falls has no single answer -- it is
    # the first atom in nine of the eleven three-atom compounds and the middle atom in the other
    # two -- and the table shows that in Unicode rather than counting it in prose (Ben,
    # 2026-07-30: "just fold this all together as a table of 3 examples of spreaders").  The
    # split is asserted rather than assumed, and the sum is the assertion that matters: a
    # compound accented on TWO non-final atoms would land in both lists and make the two counts
    # sum to more than the whole, leaving the table a tour of two kinds out of three.  Each
    # example is the first of its list in the survey's own order, the idiom
    # ``spreader_qad_zaq`` above already uses.
    three_atom = [
        o
        for o in _occurrences(survey, _CORPUS, "prose")
        if len(o["shape"].split("-")) == 3
    ]
    first_atom = [o for o in three_atom if o["shape"].split("-")[0] != "0"]
    middle_atom = [o for o in three_atom if o["shape"].split("-")[1] != "0"]
    assert first_atom and middle_atom, three_atom
    assert len(first_atom) + len(middle_atom) == len(three_atom), three_atom
    spreader_examples = (spreader_qad_zaq[0], first_atom[0], middle_atom[0])
    # The three printed cases, derived once and used both for the table and for the answer,
    # which now names ALL THREE pairs -- the same derivation ``pin_claims`` checks the absence
    # of, through ``unprecedented_pairs``.  Koren's used to be answered separately, so only the
    # Simanim Tiqqun's two were spelled out here.
    cases = printed_cases()
    koren_pair, *simtiq_pairs = [case["pair"] for case in cases]
    # GONE (Ben, 2026-07-30): the metigah-zaqef count, and the sentence it was spliced into --
    # "Of the 233 prose cases, 211 are a single grammatical category, metigah-zaqef: a qadma
    # before a zaqef."  It closed the intro's answer, and the answer is about the three printed
    # compounds having no precedent; a tally of what the OTHER 233 mostly are answers a question
    # nobody has been asked yet at that point.  Ben: "This sentence seems out of place, and I
    # don't think it has a place any longer."  It is no loss: the prose section's own table has
    # the 211 in its top row, under the heading that says what those rows count, which is where a
    # reader meets the figure with something to do with it.
    return (
        H.heading_level_1(PAGE_TITLE),
        text_para(
            "In the prose system a chanted word always has at least one accent,"
            " and usually only one."
            " In a small minority of cases, a chanted word has two accents,"
            " but never more than two."
            " Some of the two-accent words are simple and some are compounds."
            " Among the two-accent compounds,"
            " some spread those two accents across two atoms, e.g.:"
        ),
        # THREE SPREADERS AS A TABLE (Ben, 2026-07-30: "just fold this all together as a table
        # of 3 examples of spreaders", with the shape drawn out -- form, then verse, no heading
        # row).  What it folds together is a specimen and, from earlier the same day, a
        # negative-claims paragraph with two more specimens under it: three sentences that
        # counted the three-atom compounds and said which atom each kind accents.  The rows say
        # it instead, which is this page's own doctrine (show it in Unicode, not only in words)
        # and leaves one parenthetical of prose where a paragraph had been.
        #
        # THE PARENTHETICAL IS THE CLAIM THAT SURVIVED, and it is the one with content.  Its
        # companion -- that a compound with both accents on one atom always has them on the
        # last -- went with the paragraph: it is nearly the tautology it is easy to mistake it
        # for, the scan defining a concentrator as a compound with no accent on any non-final
        # atom, so the sentence just above it already tells a reader where those two accents
        # are.  ``pin_claims`` keeps the surviving one honest.
        _spreader_example_table(spreader_examples),
        # "THE REMAINING", NOT A SECOND "SOME" (Ben, 2026-07-30: "instead of just hedging with
        # another 'some' ... can't we say the stronger claim").  We can: the two kinds are
        # exhaustive of the two-accent compounds, and saying so is what tells a reader there is
        # no third kind waiting.  A compound with no accent on any non-final atom has both of
        # them on its final atom, there being nowhere else left, so what the sentence rests on
        # is that a two-accent compound is a spreader or a concentrator and nothing else --
        # pinned above by the hit loop's "exactly two accented atoms" and by
        # ``concentrator_by_shape``'s "every non-final field empty".
        #
        # The 45 MAM prose compounds ``concentrator_excluded`` sets aside are no exception to
        # it.  Their two marks are a zarqa's stress helper and the zarqa, one accent written
        # twice, so they are not two-accent compounds at all -- and their marks are on the last
        # atom in any case, which is where the sentence would put them.
        text_para(
            "(One of the two is always on the last atom.)"
            " The remaining two-accent compounds instead concentrate both of those two"
            f" accents on the last atom, e.g. ({_ref_abbrev(conc_example['bcv'])}):"
        ),
        _specimen(
            conc_example,
            silluq_second=_ACCENT_DISPLAY[_split_pair(conc_pair)[1]] == ROM_SILLUQ,
        ),
        text_para(
            f"Of the {mam_prose['maqaf_compounds']:,} maqaf compounds in the prose"
            f" verses of MAM, {mam_prose['hits']} ({pct:.2f}%) are “spreaders” and"
            f" {mam_prose['concentrators']} ({conc_pct:.2f}%) are “concentrators.”"
            " Here we are primarily interested in “spreaders”, i.e. two-accent maqaf"
            " compounds where one of those accents is on a non-final atom. This page"
            " studies MAM's spreaders"
            " to see if they shed any light on some strange spreaders"
            " in the Decalogues of two editions:"
        ),
        # THE THREE PRINTED CASES, AS A TABLE (Ben, 2026-07-29).  What stood here was running
        # prose for Koren -- a sentence flowing through two specimens -- and then a shorter
        # paragraph for the Simanim Tiqqun opening "Koren's is not the only such compound in
        # print", which is the afterthought framing in one clause.  His two asks: put the two
        # editions on a par, and show the comparison as "tables showing, for each
        # word/word-pair ... what the edition has/editions have, what the Wikisource reference
        # has, and what the other-height wikisource reference has".  A table does both at once,
        # every cell a form rather than a description of one.
        #
        # TABLE FIRST, PARAGRAPH AFTER (Ben, 2026-07-30).  The count paragraph ends on a colon
        # and the table follows it directly; the paragraph that had introduced the table now
        # stands after it.  Trimmed the same day to what the table does not already say: the
        # sentence naming the two editions (locating the cases in the appendices was its only
        # addition) and the below-each-spreader tour of the rows are gone, and the links to the
        # two edition pages live in the table's Edition row.  What survives is the p-trad
        # qualification, parenthesized and first, and the two-distinct-compounds sentence,
        # since לא־תעשה appearing in two of the three cases may confuse.
        _printed_case_table(cases),
        # P-TRAD SAID ONCE, in the parenthetical below, and dropped from the individual
        # mentions -- which UNDOES the per-mention "the p-trad עליון" and "the p-trad תחתון" of
        # earlier the same day.  ``_p_trad_strand`` is where the tradition is fixed for every
        # strand this page reads, so the one sentence is the whole of the qualification and
        # cannot come to disagree with the derivations.
        # BOTH SENTENCES PARENTHESIZED (Ben, 2026-07-30).  Each is an aside about how to read
        # the table rather than a step in the page's argument -- one saying which tradition every
        # strand named here is, the other heading off the confusion of meeting לא־תעשה in two of
        # the three columns -- and the parens say so, leaving the argument to run from the count
        # paragraph above the table straight into the carry-over paragraph below.
        text_para(
            "(Every strand named on this page is a p-trad one.)"
            " (Both Koren and the Tiqqun have strange spreaders on לא־תעשה,"
            " so there are only two distinct compounds among these three cases:"
            " לא־תעשה and לא־יהיה.)"
        ),
        # THE CARRY-OVER, STILL BEFORE THE QUESTION (Ben, 2026-07-28), and now for all three
        # rather than for Koren alone.  The cheap explanation is disposed of first, and the
        # question is then asked of marks taken as they stand -- which is what the rest of the
        # page does.  Put after the answer, it read as an afterthought undercutting the count it
        # followed.
        #
        # TWO SENTENCES, THE TABLE CARRYING THE REST.  A first pass at the Koren half spread the
        # same suggestion over two paragraphs and was "way too belabored regarding speculation
        # about the source of the error"; the columns now show which mark is where, so the prose
        # says only what a reader cannot read off them.
        #
        # NEITHER IS CALLED AN ERROR.  Ben's own framing, 2026-07-29, is that he assumes the
        # Simanim Tiqqun's is one -- "though I'd prefer not to state that in the document" -- and
        # asks whether it "may have its source in cross-height 'contamination'".  So the page
        # shows the correspondence and offers the carry-over, and names no fault in either
        # edition.
        #
        # ONE SENTENCE, THE TABLE CARRYING THE REST (Ben, 2026-07-30, supplying the wording).
        # What it replaces named each edition's mark in prose -- Koren's maqaf, and the munax on
        # the joined לא of the Simanim Tiqqun's two -- which is now the Diff. fr. Ref. row, cell
        # by cell and derived from the forms rather than typed out.  A sentence that itemizes the
        # row directly above it is a sentence a reader has already read.
        text_para(
            "Each strange spreader differs from the Wikisource reference by the"
            f" addition of a mark (either {ROM_MAQAF} or {ROM_MUNAX}) that might have been"
            " accidentally carried over from the other strand."
        ),
        text_para(
            "But if we take the three as they stand, is there anything in Tanakh like any of"
            " them?"
        ),
        # ONE CLAIM FOR ALL THREE (Ben, 2026-07-30): none of the three pairs occurs on any
        # chanted word of MAM's prose verses.  What went is the sentence's Koren half -- that no
        # maqaf compound has the same accent on both atoms -- and Ben cut it knowing what it
        # cost: "even though it is a stronger claim, and arguably more interesting".  The fault
        # was that it framed Koren's case and the Simanim Tiqqun's two in two different ways in
        # one sentence, so a reader met a claim about SAMENESS beside a claim about two named
        # PAIRS and had to work out that the two halves answered the same question.  Koren's
        # munax-munax is a pair like the other two, and answering it as one costs a clause and
        # buys a sentence that says one thing.
        #
        # ``pin_claims`` already checked exactly this, for all three pairs, through
        # ``unprecedented_pairs`` -- the wider accented-alike assertion it also carried has gone
        # with the wider claim.
        text_para(
            "There is not. None of the three pairs occurs on any chanted word of MAM's prose"
            f" verses, compound or simple: not Koren's {_pair_in_words(koren_pair)}, and not"
            f" the Simanim Tiqqun's {_pair_in_words(simtiq_pairs[0])} or"
            f" {_pair_in_words(simtiq_pairs[1])}."
        ),
    )


# One tuple per ROW of the transposed table: the row's label cell, the function fetching its
# value from a case, and its data cells' attributes -- together, so a label and its values
# cannot come to disagree.  "Strange" and "Reference" are Ben's 2026-07-30 relabels of
# "Printed" ("a poor choice BTW") and "Same strand"; the hover texts still say what each row
# holds.  "Wikisource" is in the two hover texts and in the carry-over paragraph, so the
# short labels say which strand a row is without also saying where the strand is from three
# times over.  The strand name and the three forms are Hebrew, so those four rows' data cells
# are declared right-to-left, blank cells included if a case ever lacks one.
#
# THE SHORT-LABEL ROWS ARE CENTERED and the form rows are not (Ben, 2026-07-30, of the first
# three; the Diff. fr. Ref. row he asked for is a fourth of the same kind).  A row whose cells
# are an edition name, a book name, a strand name or a "+maqaf" is three short parallel answers,
# and centering is what makes them read as three answers to one question.  The three form rows
# stay right-to-left alone: they are the comparison itself, read down a column, and a Hebrew
# form left to start at its own start edge is where a reader's eye already is.
_PRINTED_CASE_ROWS = (
    (
        H.table_header("Edition"),
        lambda case: link(case["edition"], case["href"]),
        _CENTERED_CELL,
    ),
    # "Decalogue", not "Book" (Ben, 2026-07-30).  Every case is a Decalogue, and what the cell
    # names is which of the two -- Exodus' or Deuteronomy's.  "Book" was true of the value and
    # said nothing about why a page on MAM's spreaders is showing two of them.
    (
        H.table_header("Decalogue"),
        lambda case: _cell_abbr(case["book"], _BOOK_CELL_ABBR),
        _CENTERED_CELL,
    ),
    (
        H.table_header(
            H.abbr("Strand", "The strand of that book the edition's page is")
        ),
        lambda case: case["strand"],
        _CENTERED_HEBREW_CELL,
    ),
    (
        H.table_header(H.abbr("Strange", "What the printed edition has")),
        lambda case: hbo(case["printed"]),
        _HEBREW_CELL,
    ),
    (
        H.table_header(
            H.abbr(
                "Reference",
                "What that book's Wikisource strand of the same name has",
            )
        ),
        lambda case: hbo(case["same"]),
        _HEBREW_CELL,
    ),
    # RIGHT UNDER THE TWO ROWS IT DIFFERENCES, so a reader who has just compared the Strange and
    # Reference cells of a column meets the one-mark answer in the next cell down rather than
    # having to carry the comparison to the end of the table.  The cell says what was ADDED and
    # nothing about where the mark then turns up; the Other strand row below is what answers
    # that, and the paragraph after the table is what joins the two.
    (
        H.table_header(
            H.abbr(
                "Diff. fr. Ref.",
                "The one mark the printed edition has that its Wikisource strand of the"
                " same name does not",
            )
        ),
        _added_mark,
        _CENTERED_CELL,
    ),
    (
        H.table_header(
            H.abbr("Other strand", "What that book's other Wikisource strand has")
        ),
        lambda case: hbo(case["other"]),
        _HEBREW_CELL,
    ),
)


def _spreader_example_table(examples: tuple[dict, ...]) -> object:
    """One spreader per row -- its form, then its verse -- and no heading row.

    Ben's own sketch, 2026-07-30, is the shape: two columns, the form first and the verse
    beside it, nothing above them.  The sentence that ends on the table's colon says what the
    rows are, so a heading would label a two-column table whose columns a reader has already
    been told about.

    THE ROWS ARE ONE PER KIND, not three arbitrary examples: a two-atom compound, a three-atom
    one accented on its first atom, and a three-atom one accented on its middle atom.  That is
    a claim, made in Unicode rather than in words, and ``pin_claims`` defends it the same way
    it defends a sentence -- ``len(atoms) in (2, 3)`` there is what stops a four-atom compound
    from leaving these three a tour of part of the field.  ``_intro`` picks them, and asserts
    the split its middle two rows rest on.
    """
    return H.table(
        tuple(
            H.table_row_of_data(
                (hbo(_form_at(o)), _ref_abbrev(o["bcv"])),
                (_HEBREW_CELL, None),
            )
            for o in examples
        ),
        {"class": "centered-table"},
    )


def _printed_case_table(cases: tuple[dict, ...]) -> object:
    """The three printed cases, each above the two Wikisource strands of its book.

    SHOW IT IN UNICODE (Ben, 2026-07-29: "I can't process all the verbosity, I need to just see
    this using actual unicode. You've fallen into the trap of not giving me Unicode").  Every
    cell of the three form rows is a form lifted or constructed from a vendored strand,
    letters and accents only; naming an accent in prose is not a substitute for showing the form,
    which is why the paragraphs this replaced are down to two sentences.

    WHAT THE OTHER-STRAND ROW IS FOR.  Ben's ask names it as "what the other-height wikisource
    reference has (which is probably what the editions have)" -- that is, the suggestion that a
    printed oddity came across from the other strand of the same book.  Read down a column: the
    mark the printed cell has and the same-strand cell lacks is in the other-strand cell.  For
    Koren that mark is the maqaf, and for the Simanim Tiqqun's two the munaḥ on the joined לא, so
    the correspondence runs in opposite directions in the two editions and the row holds both.
    Since 2026-07-30 the Diff. fr. Ref. row NAMES that mark, so the reading-down is stated rather
    than left to be performed: "+maqaf" or "+munaḥ" in one cell, and the cell below it is where
    that mark already is.  ``_added_mark`` derives it from the two form rows above it.

    A COLUMN PER (EDITION, COMPOUND) CASE -- a row per case until Ben's transpose ask the same
    day ("rows become columns") -- and ``printed_cases`` says why there are three of them.
    """
    return H.table(
        tuple(
            H.table_row(
                (label, *(H.table_datum(value_of(case), attr) for case in cases))
            )
            for label, value_of, attr in _PRINTED_CASE_ROWS
        ),
        {"class": "centered-table"},
    )


# The scans behind the table above: TWO figures for the three cases, because the Simanim Tiqqun's
# two compounds sit on the same two printed lines (line 14 of its transcription holds לא־יהיה לך
# whole, and the לא־ that opens the לא־תעשה compound).  Each crop is one whole printed line, or
# two where the compound spans a line break, cut by ``main_edition_transcription.py scan-page``
# from the same source scans the transcriptions are pinned to.
_KOREN_P39_IMG = "img/Koren-appendix-p-39-Dt-Dec-p-trad-elyon-lo-taase.png"
_SIMTIQ_P246_IMG = "img/Simanim-Tiqqun-p-246-Ex-Dec-p-trad-taxton-spreaders.png"

# The viewBox literals must equal each committed PNG's own natural size, since mhi.Box coordinates
# are in that pixel space, so these are the sizes `scan-page` reported when it wrote the two
# files, not sizes derived by eye.  Getting one wrong is silent at build time -- the page still
# renders and the highlights just land elsewhere -- so `tests/test_scan_overlay_viewboxes.py`
# lints every rendered figure's viewBox against its scan's real size.  Take the pair from what
# `scan-page` prints all the same: the lint tells you the numbers disagree, not which one is right.
#
# BOTH CROPS WERE RE-CUT to leave equal margins either side of the ink (Ben, 2026-07-31: "both of
# their crops are a little lopsided").  The first pair left 303px of margin against 93px on
# Koren's strip and 72px against 172px on the Tiqqun's.  The re-cut trims only the fat side, at a
# scale chosen to leave pixels-per-source-unit unchanged, so every box below moved by a pure
# translation -- Koren's by -210 in x, the Tiqqun's by nothing at all -- rather than needing to be
# picked again.  Each box was then cropped back out of its new PNG and checked to be on the same
# word.
_KOREN_P39_VIEWBOX = (1390, 160)
_SIMTIQ_P246_VIEWBOX = (1500, 293)

# One box, on the לא־תעשה compound of the middle printed line.
_KOREN_P39_BOXES: tuple[mhi.Box, ...] = (mhi.Box(x=889, y=39, w=249, h=96),)

# THREE boxes for TWO compounds: לא־יהיה whole on the first line, and then the לא־תעשה compound in
# two pieces, its לא ending the first line and its תעשה opening the second.  Two boxes for one
# chanted word is new here.  The Koren page's _P281_BOXES and _PA38_BOXES box only the
# accent-bearing half of a word the printing wrapped; here both halves are accent-bearing, which
# is the very thing this page is about, so boxing one of them would hide the finding.
# Listed in READING order, which is not the order the picker emitted them in.  The rects are
# siblings in one overlay and are drawn independently, so their order changes nothing on the page;
# reading order is for whoever next has to match a literal here against a mark on the scan.
_SIMTIQ_P246_BOXES: tuple[mhi.Box, ...] = (
    # לא־יהיה, whole, on the upper printed line -- munax on לא, merkha on יהיה.
    mhi.Box(x=926, y=66, w=290, h=96),
    # The לא־ that ends that same upper line, with its munax: the first atom of לא־תעשה.
    mhi.Box(x=52, y=63, w=148, h=100),
    # The תעשה that opens the lower line, with its qadma: the second atom of that לא־תעשה.
    mhi.Box(x=1230, y=166, w=226, h=102),
)


def _scans_appendix_section() -> tuple[object, ...]:
    """The scans behind the intro's table, as an appendix at the page's foot.

    Every cell of that table is lifted or constructed from a vendored Wikisource strand, so the
    table states the page's claim about each edition without ever showing the printing.  These two
    figures are the printing those claims are read off -- each a crop of one or two printed lines,
    with the strange spreaders boxed.  The heading says "cropped, highlighted scans" for that
    reason: it was "the printed pages" (Ben, 2026-07-31), which promised whole pages.

    AN APPENDIX, not part of the intro (Ben, 2026-07-31: "let's banish these two new images to an
    appendix").  They sat directly under the printed-case table when they were first rendered.
    The table is the intro's answer and the scans are its evidence, and evidence set apart from
    the argument it supports is what an appendix is for.

    NOTHING CUES IT.  The intro does not link down to this section, matching the two prevalence
    sections, whose comments say why: a rendered section that previews a later one is the hub
    sentence Ben has cut from these pages before, and an appendix heading announces itself.  The
    one link that does run down the page, from the prose section to the one-letter appendix, is
    the exception rather than the pattern.

    ``img_class="ink-on-white"`` on both: each is black ink on white paper and wants the
    stylesheet's dark-mode inversion.

    ONE CLAUSE PER CAPTION (Ben, 2026-07-31): which edition, which Decalogue, which strand, which
    page, and what is highlighted.  Each caption used to splice the forms themselves out of the
    vendored strands and then say in prose that each has an accent on both atoms, and the Tiqqun's
    added a sentence about the printed line break falling inside its לא־תעשה.  All of that is
    already in front of the reader: the intro's printed-case table shows the same forms, derived
    the same way, and the boxes on the scan show where they are and that one of them is in two
    pieces.  So this is NOT a place to reinstate the "show it in Unicode, not only in words" rule
    -- the Unicode is shown, one section up and in the image, and the captions are the labels on
    the evidence.  Nothing here derives anything, which is why ``printed_cases()`` is no longer
    called: the "re-derived rather than handed down" guard the call carried belongs to the table,
    which still has it.

    THE TWO PAGE CITATIONS ARE DELIBERATELY NOT PARALLEL, and "appendix p. 246" would be wrong.
    Koren's appendix restarts its own page numbering, so "p. 39" names nothing unless "appendix"
    qualifies it.  The Simanim Tiqqun's p. 246 is an ordinary number in the book's one overall
    sequence, and its appendix is merely where in the book that page falls -- hence the aside.
    """
    return (
        H.heading_level_2("Appendix: cropped, highlighted scans"),
        mhi.scan_figure(
            _KOREN_P39_IMG,
            "Koren appendix p. 39: the Deuteronomy Decalogue's לא־תעשה in the p-trad"
            " elyon, with an accent on each atom",
            (
                "Koren's Deuteronomy Decalogue ",
                ELYON,
                " (appendix p. 39), with its strange spreader highlighted.",
            ),
            img_class="ink-on-white",
            boxes=_KOREN_P39_BOXES,
            viewbox=_KOREN_P39_VIEWBOX,
        ),
        mhi.scan_figure(
            _SIMTIQ_P246_IMG,
            "Simanim Tiqqun p. 246: the Exodus appendix Decalogue's לא־יהיה and"
            " לא־תעשה in the p-trad taḥton, each with an accent on both atoms",
            (
                "The Simanim Tiqqun's Exodus Decalogue ",
                TAHTON,
                " (p. 246, in an appendix), with its two strange spreaders highlighted.",
            ),
            img_class="ink-on-white",
            boxes=_SIMTIQ_P246_BOXES,
            viewbox=_SIMTIQ_P246_VIEWBOX,
        ),
    )


# GONE: "What is counted", whittled to one sentence over two days and then cut outright (Ben,
# 2026-07-28: "I question the value of this whole, small section").  What that last sentence
# said -- the question is whether a compound has an accent other than the one on its last atom
# -- the intro already says, in the same words, as the thing the page counts.  A section that
# restates the intro is not a definition, it is an echo.
#
# What went before it, each cut for a reason worth keeping:
#   * A paragraph calling the space-delimited unit a chanted word and then arguing that
#     splitting on spaces gives chanted words -- assuming the premise and proving it.  It also
#     taught a shape notation (qad-zaq, 0-mer-sil) used nowhere else on the page.
#   * A paragraph saying a meteg and a silluq are one sign and that it counts as an accent only
#     verse-finally.  "Useless internal implementation explanation.  Also, super obvious.
#     Basically saying: I'm not an idiot."  The rule lives in atom_accents' docstring, where a
#     reader of the code needs it and a reader of the page does not.
#   * A sentence saying a compound counts once however many of its atoms are accented, and is
#     counted against every maqaf compound in those verses.  "Nitty-gritty details of counting
#     at a level of detail not of concern to my model of who the reader is."  It lives in
#     ``scan``.
# Every rule they stated still governs the count; none of them was ever page text's job.


# GONE: "Which text this page counts", the last remnant of a section that once compared three
# corpora (Ben, 2026-07-28).  Its final paragraph told the reader that MAM is a consensus text
# rather than a diplomatic one and is not one of Breuer's editions -- true, and every word of it
# an answer to something that happened in the drafting rather than to anything on the page.  Ben:
# "I had to explain all that to you because you kept saying wacky stuff about MAM being a Breuer
# edition, and initially framing this whole page against WLC, but that's dirty laundry/internal
# history the reader doesn't need to know about.  Elsewhere it is clear that MAM is the
# reference."  The rule it stands for: a paragraph that exists because a discussion went a
# certain way is internal history, not page text, however accurate it is.  The corpus is named
# where the counts are, which is where a reader meets it.


# The three rows Breuer's CoS ch. 9 §37 licenses on a compound: the metigah in the chanted word
# of a small zaqef, and the mayela in that of an etnaxta or of a silluq.  Those are the two marks
# his §37 names -- the only ones of the 21 books, he says, that a maqaf stands after -- and the
# table has each of them under whichever mafsik it serves, so the rule reaches three rows and not
# two.  Keyed by the survey's shape shorthand, so a pair that stopped occurring would drop out
# of the sum silently; ``pin_claims`` is what stops that.
_BREUER_MAQAF_SURVIVING = (("qad", "zaq"), ("tip", "etn"), ("tip", "sil"))


def _spreaders_by_pair(survey: dict) -> Counter:
    """Spreader counts per accent pair, the same tally ``_pair_rows`` builds its rows from."""
    return Counter(_pair_of(o["shape"]) for o in _occurrences(survey, _CORPUS, "prose"))


def _prose_section(survey: dict, rows: list[dict]) -> tuple[object, ...]:
    # This section absorbed two that used to precede it, "Two routes, and why they must be
    # counted apart" and "How a hit is assigned to a route" (Ben, 2026-07-27: keep the page to
    # one weird thing in Koren and whether it ever happens in MAM, "with at most one passing
    # remark about things being more complicated in L, as Yeivin points out").  Both were built
    # around route (b), the maqaf written after an atom that keeps its own conjunctive -- a
    # habit of a particular naqdan, which MAM, not being a manuscript, has no instance of.  The
    # material they carried is issue wlc-utils#83, which links to wlc-utils#82.
    #
    # What survives of them here: the closed-list sentence, because "Koren's shape is not in the
    # list" is only worth saying of a list that is closed; the passing L remark; and ONE worked
    # example.  The example is kept against a page that would otherwise assert its category
    # names and never show one being decided -- Judges 7:13, because metigah-zaqef is the
    # category the overwhelming majority of the hits fall into.  Judges 8:10 שלף־חרב went with
    # the section: it made the subtler point that a mark AT the atom's own stress can still be
    # secondary, which needs the route machinery to be worth making.
    #
    # "usual place", not "all N": the survey records only the MODE of letters-after-accent per
    # atom, so the mode is the whole of what a spliced number can defend.  The unanimity that in
    # fact holds here is not in the JSON, and prose must not claim more than the build re-derives.
    #
    # The one-row table went too.  Its two surviving columns restated the intro's own sentence,
    # and the other three were route counts.
    hits = _n(survey, _CORPUS, "prose", "hits")
    spreaders = _spreaders_by_pair(survey)
    maqaf_surviving = sum(spreaders[pair] for pair in _BREUER_MAQAF_SURVIVING)
    return (
        # "Spreader-pair prevalence", Ben's own wording, 2026-07-30 ("These headings are all
        # poor").  "The prose verses" named the section's SCOPE and left its subject to the
        # paragraph under it, which is the fault: every section of the page is about MAM's prose
        # verses, so the one heading that said so said nothing that distinguished it.  What this
        # section holds is how common each accent pair is, which is what the heading now says.
        # It gives up the parallel with "The poetic verses" below, and that parallel was part of
        # what made it uninformative.
        H.heading_level_2("Spreader-pair prevalence"),
        # THE OPENING SENTENCE, rewritten 2026-07-28.  It used to read "A mark on a non-final
        # atom is there because the compound is one chanted word, and a mark belonging to that
        # chanted word as a whole has landed short of its last atom" -- Ben: "one of the least
        # comprehensible things you've ever written, while of course sounding erudite and
        # certain."  Three faults, kept here so none of them comes back:
        #   * The "because" ran backwards.  Being one chanted word is why a compound normally
        #     has exactly ONE accent -- the reason these cases are rare (233 of 36,786), not the
        #     reason the mark is there.
        #   * "landed short of its last atom" pictured a mark that missed.  A secondary accent
        #     has its own position, in front of the main accent; nothing aimed at the last atom
        #     and fell short.  Transformative framing of exactly the banned kind.
        #   * It asserted of all 233 what holds of the 230 routed ones; the three undecided are
        #     undecided precisely because this cannot be checked for them.
        # What replaces it is the point MAQAF_IS_THE_LAST_RUNG stands for: these marks are not a
        # phenomenon of compounds.  The list is Yeivin's list of accents that can come first of
        # two on an ordinary word, which is why Koren's two identical accents are not on it.
        # JUST THE PAIRS THAT OCCUR (Ben, 2026-07-28).  The table used to be Yeivin's closed
        # list, with each case placed in one of his categories, plus two rows for the cases the
        # placement could not name or could not reach.  All of that machinery exists to answer
        # a question this page does not need: whether the maqaf is optional -- a manuscript
        # joining two atoms that each keep their own accent -- or whether the pair is one only
        # a single chanted word can carry.  Ben: "this is an interesting research question, and
        # gets to the more restricted definition of secondary that I think Breuer uses, but can
        # we just avoid the whole thing and say these are the pairs that are known to occur?"
        # So the rows are now observed pairs, every case lands in one, and the undecided and
        # unnamed rows and their four-case table are gone with the question they belonged to.
        #
        # Gone with them (same day, same reason -- "I'm really trying to narrow the scope of
        # this document, and get out alive"): a closing paragraph reporting Yeivin §§293, 357 on
        # manuscripts that have a maqaf after an atom keeping its own conjunctive, and MAM
        # having no case of it.  That paragraph WAS the optional-maqaf question, stated as an
        # aside; with the classification gone the page can no longer support its "no case of
        # it", which was a route count.  Issue wlc-utils#83 holds the material.
        #
        # The sentence says "on a compound" since 2026-07-29, the pairs no compound has having
        # gone to the appendix.  It used to say "the pairs that occur", full stop, which the
        # table no longer is.  It does NOT cue the appendix: a rendered section that previews a
        # later one is the hub sentence Ben has cut from these pages before, and an appendix
        # heading announces itself.
        #
        # And since 2026-07-30 it says "on a spreader", with the intro's gloss repeated, rather
        # than "on a compound" (item 2 of ``doc/review-findings-2026-07-29.md``): the survey
        # counts a compound only when an accent sits on a NON-FINAL atom, so a pair whose two
        # accents both sit on the final atom -- a concentrator -- is invisible to the table,
        # and ``concentrator_by_pair`` has such compounds for six of the appendix's ten pairs
        # and hundreds for munax before zaqef qatan.  "The pairs that occur on a compound"
        # claimed a corpus-level fact the table does not measure.
        # A LEAD-IN AND THREE BULLETS, not a sentence carrying all three counts and both glosses
        # (Ben, 2026-07-30, supplying the shape: "because a lot of this is covered at the start
        # of the document, we can (and should) simplify").  What the paragraph before it did was
        # re-teach the intro -- that a chanted word can have two accents, what a spreader is,
        # what a concentrator is -- inside the sentence that introduces the table, so a reader
        # who had just read all three met them again as parentheses in a sentence they were
        # trying to get to the end of.  The intro defines both terms, with a specimen apiece and
        # the two percentages; a bullet per count column is then all this needs.
        #
        # The lead-in still says the rows are the SPREADERS' pairs, which is the one thing the
        # bullets cannot say: a bare "the pairs that occur ... on a spreader, on a concentrator,
        # on a simple chanted word" would claim the ten in the appendix below as rows too.  And
        # it does not cue that appendix -- a section that previews a later one is the hub
        # sentence Ben has cut from these pages before, and an appendix heading announces itself.
        #
        # "Simple chanted word", where Ben's sketch has "simple word": the bullets contrast
        # three kinds of chanted word, and wlc-utils#81 asks for the qualifier exactly where the sense is
        # in doubt.  Beside two bullets that are compounds, a bare "word" invites the atom
        # reading.
        H.para(
            "The table below shows the accent pairs that occur on a spreader, in the prose"
            " verses of MAM, and how often each of them occurs:"
        ),
        H.unordered_list(
            (
                "on a spreader",
                "on a concentrator",
                "on a simple chanted word",
            )
        ),
        _pair_table(rows, hits),
        # Yeivin in one sentence after the table, not a column in it (Ben, 2026-07-28: "no need
        # to put Yeivin section numbers in the table, just mention most of these pairs are
        # covered in Yeivin ITM sections blah").  "Most", not all.  The count follows the rows
        # the sentence stands under: eight, of which the six cited sections cover six -- §210
        # the mayela before a silluq, §216 the mayela before an etnaxta, §221 munax-zaqef, §224
        # metigah-zaqef, §233 the merkha before a tipexa, §241 the mahapakh before a pashta.
        # The two rows left over, merkha before pashta and merkha before silluq, are on no list
        # of his: §233 is tipexa-only, and §209 gives the silluq one conjunctive and no
        # secondary (issue wlc-utils#86).  Until 2026-07-30 this comment leaned on the wrong
        # §233-names-the-silluq-row citation and counted "every one but merkha before pashta";
        # six of eight still holds "Most" up, so the sentence itself stands (item 3 of
        # ``doc/review-findings-2026-07-29.md``).
        # "Most" was "Several" for one day (2026-07-29), while the table also held the ten
        # pairs no spreader has, five of which Yeivin covers in sections this sentence does not
        # cite (§§215, 236, 253, 268, 276); the appendix those ten went to says nothing about
        # him.
        #
        # BREUER BESIDE HIM since 2026-07-31 (Ben: "find the relevant sections of Breuer CoS, to
        # complement the listing of Yeivin ITM sections"), read off
        # ``../masorah-books/books/cos/md-export-of-docx/`` rather than recalled, and pinned in
        # that repo's ``py/cos/check_cos_claims.py``.  That one repo holds both books, so the ITM
        # sections above and the CoS ones here are one clone apart, not two.
        # CoS organizes the same ground per mafsik, under a
        # heading that recurs through its Chapter 3 -- "Two cantillation marks in the same word",
        # before §2, §6, §10, §20, §25, §28, §30, §37 and §40 -- with the metigah held back to
        # Chapter 5, where the zaqef alternates are.  Row by row:
        #   * munax-zaqef -- ch. 3 §30, "The servant of zakef appears in its word".
        #   * metigah-zaqef -- ch. 5 §§4-6, the span ch. 3's note 130 cites for the methiga.
        #     §5 is the one that reaches a compound: the metigah goes at the beginning of the
        #     chanted word "provided there is there a hyphenated tiny word".
        #   * the merkha before a tipexa -- ch. 3 §28, "In eight places, the servant of
        #     tipekha appears with it in its word".  # translit-ok: quotes CoS's spelling
        #   * the mahapakh before a pashta -- ch. 3 §20, whose servant "is
        #     mahpakh".  # translit-ok: quotes CoS's spelling
        #   * the mayela before an etnaxta -- ch. 3 §38, "In eleven places".
        #   * the mayela before a silluq -- ch. 3 §40, "In five places".
        # THE SAME SIX, AND THE SAME TWO LEFT OVER, which is why one sentence can carry both
        # books and the second sentence is worth its space: ch. 3 §20 gives the pashta's same-word
        # servant as a mahapakh only, and ch. 3 §39 gives the silluq's servant as a merkha across
        # two words with no same-word section for it, §40 being the mayela's.  So Breuer is silent
        # exactly where Yeivin is, which is a second book agreeing with issue wlc-utils#86's suspicion
        # rather than a failed search -- and the negative is guarded in ``check_cos_claims.py`` by
        # pinning what those two sections DO say.
        #
        # Two of his counts fall out of this survey exactly -- eleven for the mayela in the
        # etnaxta's chanted word (8 spreaders + 3 simple), five for the mayela in the silluq's
        # (1 + 4) -- and one does not: his eight for the merkha in the tipexa's against this
        # survey's twelve, and his ch. 3 §30 examples of munax-zaqef are all concentrators where
        # this survey has one spreader.  NONE of that is on the page; it is comment on issue wlc-utils#86,
        # where the same kind of Yeivin question already lives.  A count of Breuer's that the
        # survey cannot re-derive is not a claim a generated page may make.
        H.para(
            (
                "Most of these pairs are covered in Yeivin's ",
                _itm(),
                " §§210, 216, 221, 224, 233 and 241, and in Breuer's ",
                _cos(),
                " ch. 3 §§20, 28, 30, 38 and 40 and ch. 5 §§4–6. The two that neither"
                f" of them covers are the same two: a {ROM_MERKHA} before a"
                f" {ROM_PASHTA}, and a {ROM_MERKHA} before a {ROM_SILLUQ}.",
            )
        ),
        # The rule, in the section the poetic appendix below already cites for the other half of
        # it: ch. 9 §37 states the 21 books' side before turning to the Three Books, and it names
        # the same two marks whichever mafsik they serve.  Its two examples are this page's
        # material -- Isaiah 8:17 וקויתי־לו is the mayela-silluq spreader in the table above.
        # No "secondary" in the rendered sentence, for the reason the labels above give: the page
        # never says what a secondary accent is, and Yeivin and Breuer do not mean the same thing
        # by it.  Naming the two positions says what §37 says without taking either view.
        # "Cancels" is Breuer's term and is marked as his, transformative framing being
        # otherwise banned; the quotation marks are the page's usual curly ones.
        # The two numbers are spliced, never typed -- ``pin_claims`` defends the three rows they
        # are summed from.
        H.para(
            (
                "Breuer's ",
                _cos(),
                " ch. 9 §37 says which of these pairs a maqaf can stand after at"
                f" all: after the {_METIGAH} and after the {_MAYELA}, while a mark of"
                " the ordinary order “cancels” it — Breuer's word. Those three pairs"
                f" are {maqaf_surviving} of the {hits} spreaders above.",
            )
        ),
        # Ben's own lists, in his own voice (2026-07-30) -- they are generated in MAM-basics and
        # published from MAM-with-doc, so "MAM catalogues ... in its lists" attributed them to
        # the text rather than to their author.  Claimed for the two accents they cover, not for
        # the table, and stated as the pairs each one selects: ``foiz_wt_sec_merk_and_friends``
        # puts a chanted word in sec-merk when a merkha stands before the word's other accent
        # (rejecting the word whose merkha is its only accent, and the one whose merkha follows a
        # mahapakh), and in sec-misc on the same footing for a mahapakh.  "Include", not "are",
        # because sec-misc also holds the poetic tipexa pairs, which this page's prose verses
        # cannot reach.
        H.para(
            (
                "My “features of interest” lists include all cases of accent pairs starting"
                " with ",
                link(ROM_MERKHA, _FOI_SEC_MERK),
                " and starting with ",
                link(ROM_MAHAPAKH, _FOI_SEC_MISC),
                ".",
            )
        ),
    )


# The two books this page cites, each written short with the full title on hover (Ben,
# 2026-07-28: "'Breuer, Chapter 9' doesn't say what breuer book ... use CoS and ITM
# respectively, and make these hover-reveal the full title").  Single-sourced here, so the two
# sections cannot come to cite them differently.
_ITM_TITLE = "Introduction to the Tiberian Masorah"
_COS_TITLE = "The Cantillation of Scripture"
# The third book, cited once, for the one distinction on this page that neither of the other two
# makes: the geresh/azla naming.  Ben, 2026-07-29, having read all three: "I'm comfortable
# resting on Jacobson's terminology; to me it doesn't contradict Yeivin or Breuer; it just adds a
# distinction that they don't make."  Jacobson's own footnote there leans on Binder, Biblical
# Chant 52-53, and his own wording is hedged -- "In some traditions" -- which the note keeps,
# that hedge being exactly what makes the other two books' silence not a contradiction.
_CHB_TITLE = "Chanting the Hebrew Bible"


def _itm() -> object:
    return H.abbr("ITM", _ITM_TITLE)


def _cos() -> object:
    return H.abbr("CoS", _COS_TITLE)


def _chb() -> object:
    return H.abbr("CHB", _CHB_TITLE)


def _poetic_section(survey: dict) -> tuple[object, ...]:
    # Cut to one paragraph (Ben, 2026-07-27: "roughly speaking just say things are different in
    # the poetic system, without getting into details").  The page is about the prose system,
    # and this section is here only so a reader is not left wondering what happens in the other
    # one.  Gone with the details: the table, Breuer's short list of poetic verses where the
    # maqaf IS written (Job 6:10, Proverbs 25:20), the oleh-we-yored overshoot with Psalms 70:6,
    # and the note that the route split was never run over poetic verses -- the last of which
    # went with the routes themselves.  All of it is issue wlc-utils#83.
    #
    # The two facts that survive are the two that make the count meaningless here rather than
    # merely different, so neither is a detail: the unwritten maqaf (which puts most of the
    # phenomenon out of the scan's reach) and the poetic system's readiness to accent one
    # chanted word twice (which is the asymmetry a prose-trained reader would get wrong).
    #
    # The gray maqaf closes the first of those with a figure instead of a hedge (2026-07-27):
    # the sentence used to call the poetic count "a floor" and stop, which told a reader the
    # number was wrong without telling them by how much.  It stays inside the one paragraph wlc-utils#83
    # cut this section down to, and it names no accent -- spelling out what the spread ones are
    # would want oleh-we-yored and tsinnorit in prose, which is the detail that was cut.
    #
    # The two figures are no longer two disjoint parts, and the sentence that made them so had
    # to go (issue wlc-utils#91): MAM-simple has every gray maqaf as an ``implicit-maqaf`` node, the
    # loader puts each on the atom before it, and Ben settled on 2026-07-31 that the survey
    # counts one as a maqaf.  So the hits figure ALREADY includes the gray-maqaf compounds, and
    # a paragraph offering the gray total as "the other part of the measure" would count them
    # twice.  What the gray count adds beside the hits is its split by kind, which is what it is
    # quoted for here.
    hits = _n(survey, _CORPUS, "poetic", "hits")
    return (
        # Ben's own word, 2026-07-30: "call it an Appendix".  The scope-naming that made "The
        # prose verses" a poor heading is no fault here -- an appendix IS material set apart by
        # its scope, and this one's scope, the poetic system, is the whole of what it has to
        # say.  So the heading gains "Appendix:" and nothing else changes.
        H.heading_level_2("Appendix: the poetic verses"),
        H.para(
            (
                "The poetic system is a different matter, and different enough that the same"
                " count would not mean the same thing there. It puts two marks on one chanted"
                " word readily and systematically (Breuer, ",
                _cos(),
                " ch. 9 §§20–26), where the prose system does so rarely, and in the few pairs"
                " above. And many of its maqafs are not written at all: Breuer (§§27, 37)"
                " records that in poetic verses the maqaf after a secondary mark is customarily"
                " left unwritten while the atom still counts as joined, so a survey that looks"
                " for a written maqaf reaches only part of what is there. MAM supplies the"
                " rest: it has ",
                link(f"{_gray(survey)} gray maqafs", _FOI_RARE_TMPLS),
                ", its mark for a maqaf the manuscript leaves unwritten where the chanted word"
                " needs one, and this survey reads a gray maqaf as a maqaf. On that reckoning"
                f" MAM's poetic verses have {hits} cases. Of the gray maqafs,"
                f" {_gray(survey, mpa.GRAY_KIND_SECOND)} join an atom that has an accent"
                " alongside the compound's accent; the other"
                f" {_gray(survey, mpa.GRAY_KIND_SPREAD)} have one accent written across the"
                " two atoms. No figure here belongs beside a prose one.",
            )
        ),
    )


def _appendix_section(survey: dict, rows: list[dict]) -> tuple[object, ...]:
    """The pairs banished from the prose section's table (Ben, 2026-07-29), at the page's foot.

    They are here rather than gone because the simple count was widened to every pair on
    purpose, one day earlier, and dropping ten of the eighteen would take back most of that.
    The prose section keeps the pairs its question is about; a reader who wants every pair
    counted on a spreader or a simple chanted word of MAM's prose verses reads on.

    THE EXCLUSION NOTE BELONGS HERE, under this table, and it used to sit under the prose
    section's instead.  Ben, 2026-07-29: "it seems we should put this where these words would
    have been included, which would have been in the 'simple alone section'".  That is what the
    data says too: the pairs those words carry are geresh-or-gershayim with a telisha gedolah and
    Ezekiel 20:31's mahapakh with a qadma, and no compound has any of the three -- so had they
    been counted, they would have added their rows to THIS table and to no other.  The note
    speaks of "the simple counts on this page" all the same, both tables' simple counts leaving
    the same words out, and it links down to ``_one_letter_appendix_section``, the next section,
    which is where those words are.  (The earlier docstring here argued the opposite, from the
    same fact about both tables; Ben overruled it.)
    """
    return (
        # "NON-SPREADER-PAIR PREVALENCE", parallel to "Spreader-pair prevalence" above, which
        # is the parallel the section wants: these are the pairs that table has not got.  Ben,
        # 2026-07-30, proposed "Appendix: Simple-only pair prevalence" for the unwieldy
        # "Appendix: the pairs whose first accent is never on a non-final atom" -- "or similar",
        # and "simple-only" is the one word of it that cannot stand.  It is what the heading
        # said until earlier that day, and the survey's own ``concentrator_by_pair`` refutes it:
        # six of these ten pairs occur on a maqaf compound, both accents on its last atom (item
        # 2 of ``doc/review-findings-2026-07-29.md``).  With those six now visible in the table's
        # own Cnc column, a heading calling them simple-only would be contradicted three columns
        # below it.  What IS true of all ten is that no spreader has them, so that is the name.
        H.heading_level_2("Appendix: non-spreader-pair prevalence"),
        # And the sentence says what the Cnc column shows rather than leaving a reader to notice
        # it: the count is spliced, so a corpus bump that gave a seventh pair a concentrator
        # moves the word with the column.
        _appendix_para(rows),
        _simple_only_table(rows),
        _geresh_or_azla_note(rows),
        _exclusion_note(survey["corpora"][_CORPUS]["prose"]),
    )


def _appendix_para(rows: list[dict]) -> object:
    """What the appendix's rows are, with both of its figures spliced from those rows.

    Every count in the sentence comes off the very rows the table below is built from, so the
    two cannot come to disagree -- the idiom the rest of the page's spliced sentences use.

    THE ASSERTION IS WHAT LETS IT SAY "ALL".  These pairs are here because no spreader has
    them, which leaves a concentrator or a simple chanted word as the only places a pair can
    have been seen at all; a pair seen ONLY on a concentrator would falsify the sentence's
    "all", and would be a genuinely new thing on the page rather than a wording problem, so the
    build stops instead of quietly counting it in.
    """
    appendix_rows = [row for row in rows if not row["compound"]]
    simple_less = [row for row in appendix_rows if not row["simple"]]
    assert not simple_less, simple_less
    on_conc = [row for row in appendix_rows if row["conc"]]
    return H.para(
        f"No spreader has any of these pairs. All {_count(len(appendix_rows))} of them occur"
        " in MAM's prose verses on simple chanted words, and"
        f" {_count(len(on_conc))} of them on concentrators as well."
    )


def _geresh_or_azla_note(rows: list[dict]) -> object:
    """What the ``ger./az.`` cell means, under the table that has it.

    Ben, 2026-07-29, having established the naming across Jacobson, Breuer and Yeivin: azla "is
    not a synonym for geresh, it is the name for geresh when geresh is used on the last
    syllable, i.e. when geresh is used on a chanted word with final stress".  So the row cannot
    pick one name without asserting a stress fact of all of its cases, and the count is spliced
    here to say plainly that both kinds are in it.

    The count is looked up rather than passed, so the sentence and the row it explains cannot
    come to disagree; a missing row fails the build rather than printing a sentence about
    nothing.

    WHAT IT MUST NOT SAY: that both kinds are among the 99.  A first pass said exactly that with
    nothing behind it.  The stress has since been measured, and both kinds ARE among them -- but
    the sentence still must not say so, for the reason below.

    ASKED AND ANSWERED, AND DELIBERATELY NOT RENDERED (2026-07-31).  Ben reversed an earlier
    decision to leave stress alone, expecting every one of these to be stressed on its last
    syllable and so to be an azla in the traditions that use the name.  ``final_stress`` settles
    it from the pointing, and the survey's ``*_final_stress_by_pair`` fields carry the answer:
    122 of the row's 126, 96 of the 99 simple chanted words and 26 of the 27 concentrators.  The
    four that are not are 1 Kings 18:42 and 2 Kings 2:9 ואליהו, 1 Chronicles 15:18 ואליפלהו, and
    Deuteronomy 25:19 מכל־איביך.  Ben, seeing them: "although the exceptions ... are few, they
    are not weird or interesting and therefore not worth noting."  So the page is unchanged and
    the cell still names both -- DO NOT publish the count, and do not re-derive it and conclude
    that it wants publishing.

    WHAT NO SURVEY OF MARKS COULD HAVE DECIDED is narrower than a first pass here claimed, and
    the correction is worth keeping because it is what made the question look closed.  The
    CODEPOINT settles nothing: Unicode has no geresh-versus-azla distinction, its only geresh
    flavors being plain geresh (which INCLUDES azla), geresh muqdam and gershayim, and MAM's
    prose verses have no ``qad-germ`` at all, so this row is entirely plain geresh.  But where
    the mark SITS is also a fact about marks, and that is what decides the name.

    OFFERED, NOT ANSWERED, NOT ADOPTED: one further clause, that in some traditions a qadma azla
    is sung to a different melody from a qadma geresh (Jacobson, CHB p. 187 again -- the same
    page as the naming above).  It was put to Ben on 2026-07-29 and he did not answer either
    way, so the note stands without it.  Recorded here so the offer is neither lost nor silently
    taken up: DO NOT add it unasked, and do not re-offer it as though it were new.
    """
    (row,) = [r for r in rows if r["second"] == _GERESH_OR_AZLA]
    return H.para(
        (
            f"One row is written {_GERESH_OR_AZLA} because its second accent goes by two names:"
            f" in some traditions a {ROM_GERESH} on a chanted word stressed on its last syllable"
            f" is called an {ROM_AZLA} (Jacobson, ",
            _chb(),
            f" p. 187). Which name each of the {row['simple']} takes turns on that stress, which"
            " this table does not record.",
        )
    )


# The type column's values, as Ben named them (2026-07-29: "'type' takes value 'gerstar-tg' for
# 'the five' and takes value '?' (literally, question mark) for Ezekiel 20:31").  ``gerstar`` is
# a glob: ``ger*`` covers geresh and gershayim alike, which is what lets one type name cover rows
# whose Acc1 column differs.
#
# THERE IS EXACTLY ONE NAMED KIND, so the question mark's hover text cannot speak of "the named
# kinds" -- a first pass had it read "Neither of the named kinds" and Ben asked which two those
# were.  What the question mark means is that Ezekiel 20:31 is alone, and nothing more is known
# of it than that it is not a gerstar-tg.  It is also the RESIDUE: any pair that is not a
# gerstar-tg takes it, so a corpus bump producing a second odd kind lands here and is visible in
# the table rather than mislabelled -- and the hover text would then be wrong about "one of a
# kind", which is the signal to name the new kind rather than to soften the wording.
_ONE_LETTER_TYPE_GERSTAR_TG = "gerstar-tg"
_ONE_LETTER_TYPE_UNNAMED = "?"
_ONE_LETTER_TYPE_TITLE = {
    _ONE_LETTER_TYPE_GERSTAR_TG: (
        f"A {ROM_GERESH} or {ROM_GERSHAYIM} with a {ROM_TELISHA_GEDOLAH}"
    ),
    _ONE_LETTER_TYPE_UNNAMED: (
        f"A one-of-a-kind case, hard to classify except to say that it is not a"
        f" {_ONE_LETTER_TYPE_GERSTAR_TG}"
    ),
}
# The named kind first, the residue last.  Sorting on the strings themselves would put the
# question mark first, "?" being below "g" in codepoint order, which is backwards for a residue.
_ONE_LETTER_TYPE_ORDER = (_ONE_LETTER_TYPE_GERSTAR_TG, _ONE_LETTER_TYPE_UNNAMED)


def _one_letter_type(word: dict) -> str:
    first, second = word["pair"]
    if first in ("ger", "ger2") and second == "telg":
        return _ONE_LETTER_TYPE_GERSTAR_TG
    return _ONE_LETTER_TYPE_UNNAMED


def _accented_letters(chanted_word: str) -> int:
    """How many base letters of the chanted word have a mark on them.

    Two of the one-letter words have each of their two accents written twice, on two letters, so
    four accents are visible; the paragraph BELOW the table says so, and this is what derives the
    "two" rather than letting the page state a count it does not compute.  Same keying as
    ``maqaf_nonfinal_accents._accents_share_a_letter``: a mark counts against the letter it
    follows.
    """
    letters: set[int] = set()
    seen = 0
    for ch in chanted_word:
        if is_base_letter(ch):
            seen += 1
        elif mpa.is_accent(ch):
            letters.add(seen)
    return len(letters)


def _mwd_link(bcv: str) -> object:
    """An anchor to the chanted word's verse in the MAM-with-doc edition, where MAM's notes are.

    Ben, 2026-07-29: "add a column with a link to the MAM with doc edition, (text 'Mwd') where
    the reader can see the notes for each of these words".  The URL comes from
    ``rtms_report.mam_with_doc_url``, which the poetic ungrammatical-verse report already labels
    "Mwd" too, and which carries the one-time Numbers 25:19 -> 26:1 remap; building the URL here
    would get that wrong.
    """
    bb, chnu, vrnu = mpa.split_bcv(bcv)
    return link("Mwd", rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu))


def _one_letter_appendix_section(survey: dict) -> tuple[object, ...]:
    """The chanted words whose two marks sit on one letter, shown rather than counted.

    Ben, 2026-07-29, of the sentence that reports them: "provide a link to an appendix that
    shows these in a table".  A count of what a page leaves out is a claim about particular
    chanted words, and six is few enough to print, so a reader can see what was set aside and
    judge it -- which a count alone never lets them do.

    The forms are lifted from the survey, letters and accents only, with the verse on hover, as
    the pair tables' examples are.  Where one row reads geresh then telisha gedolah and another
    reads gershayim then telisha gedolah, that is the written order of the two marks on the
    letter and the two marks themselves.

    WHY "THE LATER PAIR" IS THE STRESS HELPER, which the paragraph asserts flatly and which a
    first pass hedged to "one of its two copies", on the ground that telisha gedolah is
    prepositive but geresh and gershayim are not, so nothing said which copy helped.  Ben,
    2026-07-29, settling it -- and it is a claim about MAM's treatment, not about the truth of
    the matter: "In MAM we treat gerstar-telg as a single accent, much in the way we treat
    merkha kefulah or gershayim as a single accent despite consisting of two discontiguous
    glyphs.  (So gershayim-tg is a single accent consisting of 3 discontiguous glyphs.)  So I
    stand by the assertion ... that the later pair is considered to be a stress helper, despite
    geresh and gershayim, when they appear elsewhere, in normal, alone cases, not being
    prepositive.  It is as if the conglomerate inherits the prepositivity of telg."  None of
    that reasoning goes on the page -- he said so in the same breath -- so it lives here, and
    the page carries the assertion alone, attributed to MAM rather than left agentless.

    THE TYPE COLUMN is the one thing here that groups: it puts those two rows together, geresh
    and gershayim being one thing for this purpose, and it separates out Ezekiel 20:31, whose
    mahapakh with a qadma is on no list.  See ``_ONE_LETTER_TYPE_GERSTAR_TG`` and its
    neighbours.  The rows are sorted by it, so the five stand together and the odd one last.

    "WORD", NOT "CHANTED WORD", IS RIGHT IN THIS HEADING, and is not the loose "word" wlc-utils#81 bans.
    Ben, 2026-07-29: it "can just say 'word' since there are no compounds so by any/either
    definition of 'word', these are words".  Not one of the six is a maqaf compound, so atom and
    chanted word name the same six things and the reader has nothing to disambiguate.

    AND THE RULE IS WIDER THAN THAT, lest a later pass read this heading as licensed only by the
    absence of compounds.  Ben, same day, correcting a first version of this paragraph that said
    so: "even a column having only compound words, or simple and compound words, might still be
    labelled word since what definition of 'word' is active is clear from the contents of the
    column!  Also in many contexts it is unnecessary to qualify a word as chanted because it is
    clear from context."  So a column of compounds may say "word" too -- the forms in it show
    which sense is meant, and a heading is read with its column, not alone.  What wlc-utils#81 bans is a
    loose "word" the reader must resolve from nothing; the qualifier is owed where the sense is
    genuinely in doubt, and is noise where the context settles it.  The hover text here says
    "chanted word" anyway, which costs nothing.
    """
    genre = survey["corpora"][_CORPUS]["prose"]
    words = sorted(
        _one_letter_words(genre),
        key=lambda w: _ONE_LETTER_TYPE_ORDER.index(_one_letter_type(w)),
    )
    gerstar = [w for w in words if _one_letter_type(w) == _ONE_LETTER_TYPE_GERSTAR_TG]
    doubled = [w for w in words if _accented_letters(w["word"]) == 2]
    body = [
        H.table_row(
            (
                *_ACC_HEADERS,
                H.table_header(H.abbr("Type", "Which kind of pair the two marks are")),
                H.table_header(H.abbr("Word", f"The chanted word; {_BCV_ON_HOVER}")),
                H.table_header(H.abbr("Mwd", "The verse in the MAM-with-doc edition")),
            )
        )
    ]
    for word in words:
        first, second = word["pair"]
        kind = _one_letter_type(word)
        body.append(
            H.table_row_of_data(
                (
                    _accent_cell(_ACCENT_DISPLAY[first]),
                    _accent_cell(_ACCENT_DISPLAY[second]),
                    H.abbr(kind, _ONE_LETTER_TYPE_TITLE[kind]),
                    _hebrew_at(word),
                    _mwd_link(word["bcv"]),
                ),
                # Only the chanted word is Hebrew; the heading over it stays as it is, Ben
                # having asked for the VALUES to be right-justified and "Chanted word" being
                # English, which an rtl declaration would misdescribe.
                (None, None, None, _HEBREW_CELL, None),
            )
        )
    return (
        # Ben's wording, verbatim, 2026-07-30.  It says "accents" where the old heading said
        # "marks" and "words" where it said "chanted words" -- both fine here, and neither a
        # slip: the two marks of one of these words ARE accents (that they may belong to one
        # syllable is the paragraph's point, not a doubt about what they are), and the context
        # settles the sense of "words", which is exactly when wlc-utils#81 leaves plain "word" standing.
        H.heading_level_2(
            "Appendix: words with two accents on the same letter",
            {"id": _ONE_LETTER_ID},
        ),
        # ITS SECOND SENTENCE IS THE SHORT FORM of the one ``_exclusion_note`` opens with, the
        # two having been synchronized on 2026-07-30 -- that docstring holds the reasoning, and
        # a reword here is a reword there.  The lists are named in Ben's own voice for the same
        # reason as the merkha/mahapakh sentence above: they are generated in MAM-basics and
        # published from MAM-with-doc, so "MAM's lists" attributed them to the text.
        H.para(
            (
                f"These {_count(len(words))} chanted words are in none of the tables above."
                " Each has two accents on one letter, so both accents likely belong to the"
                " same syllable. My “features of interest” lists include the"
                f" {_count(len(gerstar))} with a",
                *[" ", link(f"{ROM_TELISHA_GEDOLAH} among them", _FOI_UNICODE), "."],
            )
        ),
        H.table(tuple(body), {"class": "centered-table accent-pair-table"}),
        # BELOW THE TABLE ON PURPOSE (Ben, 2026-07-31: "let's move that discussion to after the
        # table, and let's fill that discussion out"), and his wording verbatim.  What used to be
        # the tail of the paragraph above pointed at rows nobody had looked at yet -- a reader met
        # "they look at first like four accents" before meeting the four accents.  The paragraph
        # above keeps the section's before-the-table job, saying what these chanted words are and
        # why no earlier table has them; this one has the after-the-table job, reading the rows.
        #
        # "THE TABLE ABOVE" STANDS, deliberately.  Put to Ben that his opener doubles the earlier
        # paragraph's "in none of the tables above", each of a different table, he chose verbatim
        # over naming the referent: this paragraph sits directly under the table it means.
        #
        # "ALL WORDS" AND "OF THEM" ARE THE WIDE READING OF wlc-utils#81 the docstring's `"WORD", NOT
        # "CHANTED WORD"` paragraph already argues -- the column's own forms settle the sense, and
        # not one of these six is a maqaf compound anyway.  Not a slip to be tightened later.
        #
        # TWO CLAIMS HERE ARE BEN'S OWN and have no oracle in the survey behind them: that this
        # presentation is unique to MAM, and what MAM's notes on the doubled words cover.  Do not
        # go hunting for data to pin them, and do not drop the "as far as I know" -- it is the
        # scope of the uniqueness claim, not a hedge over a bounded doubt.  The stress-helper
        # sentence is the same kind of claim, attributed to MAM; the docstring's WHY "THE LATER
        # PAIR" IS THE STRESS HELPER paragraph holds the reasoning that stays off the page.
        #
        # The count is spliced from ``doubled`` as it was before, mid-sentence now, so no
        # ``.capitalize()``.
        H.para(
            f"In the table above, all words are shown as they appear in MAM. In particular,"
            f" {_count(len(doubled))} of them have each of their two accents written twice, so"
            " they look at first like they have four accents rather than two. But, MAM intends"
            " the later pair of accents to be interpreted as a stress helper. This presentation"
            " is, as far as I know, unique to MAM. The Mwd column links each chanted word to"
            " MAM's notes on it. For the words with stress helpers, MAM's notes discuss the wide"
            " variety of ways these words appear in important manuscripts and printed editions."
        ),
    )


def render_body_contents(survey: dict) -> tuple[object, ...]:
    pin_claims(survey)
    # Both tables are cut from one ordered list, so the split cannot reorder or double-count.
    rows = _pair_rows(
        survey["corpora"][_CORPUS]["prose"], _occurrences(survey, _CORPUS, "prose")
    )
    sections: list[object] = [
        *_intro(survey),
        *_prose_section(survey, rows),
        *_appendix_section(survey, rows),
        *_one_letter_appendix_section(survey),
        # THE SCANS SIT HERE, and the slot is forced rather than chosen.  Two constraints already
        # bind: "Spreader-pair prevalence" and "Appendix: non-spreader-pair prevalence" are a
        # named pair and must stay adjacent, and the poetic appendix is last by Ben's own ask.
        # That leaves exactly this place.
        *_scans_appendix_section(),
        # THE POETIC SECTION IS LAST, and an appendix (Ben, 2026-07-30: "float 'poetic verses'
        # down to the bottom and call it an Appendix").  It sat between the prose section and
        # the first appendix, where a heading naming a whole other system interrupted the run
        # of prose-verse tables that answer the page's question -- and, once the two around it
        # were renamed to "…prevalence", it was the odd heading in the middle rather than at
        # the edge.  Nothing in it points forward, and the appendix above it links to the
        # one-letter appendix still below it, so the move breaks no reference.
        *_poetic_section(survey),
    ]
    return (H.div(tuple(sections), {"class": _WIDTH_CLASS}),)


def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / "maqaf-nonfinal-accents.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the maqaf-nonfinal-accents page.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=mpa.default_json_out_path(),
        help="Output JSON path for the survey behind the page.",
    )


def run(args: argparse.Namespace) -> None:
    survey = mpa.build_survey()
    mpa.write_json(survey, args.json_out)

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(survey),
        write_ctx=H.WriteCtx(
            title=PAGE_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    prose_hits = _n(survey, _CORPUS, "prose", "hits")
    print(f"JSON: {args.json_out}")
    print(f"HTML: {html_out} (MAM prose hits: {prose_hits})")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
