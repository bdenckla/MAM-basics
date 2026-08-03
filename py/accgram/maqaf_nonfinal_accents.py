r"""Survey: accents on the NON-FINAL atom of a maqaf compound, across the whole Tanakh.

An accent on a non-final atom of a maqaf compound is the phenomenon behind ``koren_dt_elyon``'s
``mun-mun`` on לא־תעשה and SimTiq's two munax-on-לא (see ``edition_transcription``).  This module
measures it mechanically so the printed-Decalogue pages' claims about how rare it is rest on a
count that can be regenerated, rather than on prose that has to be re-derived every time someone
asks.

Pure computation and a JSON writer -- no HTML.  ``maqaf_nonfinal_accents_page`` renders it, and
runs this to write the JSON, so the page's numbers can never drift from the data.

THE CRITERION is mechanical: within one whitespace-delimited chanted word, is there an accent both
before and after a maqaf?  A maqaf compound has no space in it, so splitting on whitespace really
does give chanted words, and splitting those on maqaf gives their atoms -- the two units this
module counts, and the two the question is about.  A U+05BD counts as an accent only on the
verse's last chanted word, where it is silluq (see CLAUDE.md on meteg-vs-silluq).  Read off the
Unicode verses and NOT off ``uni_to_marks``' mark bodies: ``word_to_marks`` front-loads prepositive
accents to the front of the whole COMPOUND, which would move an atom-2 telisha gedolah onto atom 1
and manufacture hits.
Prose and poetic are routed by ``prose_filter`` / ``poetic_filter`` and counted separately, since
the two systems differ here and a merged count would say nothing about either.

THE TWO ROUTES.  A single bucket of "compounds with two accents" hides the distinction that
matters, so every hit is sorted into one of two routes:

* **(a) A secondary accent the compound inherits.**  Yeivin's own term, and his prose inventory
  is a CLOSED LIST of configurations -- which accent sits on the non-final atom and which the
  compound has: metigah-zaqef (ITM §223), munax-zaqef (§221), a secondary merkha in the chanted word of a
  tipexa (§233) or of a tevir (§253), a secondary azla in that of a geresh (§268), a secondary
  munax in that of an etnaxta (§215), a revia (§236) or a pazer (§276), a secondary mahapakh in
  that of a pashta (§241), and the mayela before an etnaxta (§216) or a silluq (§210).  ("The
  mayela", never "the mayela tipexa": mayela is the name for what would otherwise be a tipexa
  there, so the pair reads as a kind of tipexa rather than as the accent's own name.  Mayela is
  to tipexa as metigah is to qadma, and nobody writes "metigah qadma".)
  ``_NAMED_CONFIGURATIONS`` is that list, plus ``(MERKHA, SILLUQ)``, which is here for ITM §357's
  sake rather than for any section of the inventory's.
  ``chanted_word_accents`` transcribes the same sections
  in full, with Yeivin's own wording and his closed verse lists, and checks them against a wider
  measurement that counts atomic chanted words too; the table here is the subset this survey's
  shape can express, which is a pair of marks with a maqaf between them.
* **(b) A maqaf written after an atom that keeps its own conjunctive.**  ITM §293: a manuscript
  habit with no grammatical trigger, "most common where the word has penultimate stress", and L
  -- WLC's own base -- is named for it (§21, §293).

A THIRD THING IS IN ROUTE (a) THAT DOES NOT BELONG TO EITHER, and this survey's shape cannot yet
put it anywhere else.  ITM §357 and Breuer CoS Ch. 1 §43 describe a maqaf written after an atom
that has its own accent and a gaʿya AFTER that accent, to say that the slowed syllable makes no
break.  A compound of this kind is a chanted word like any other, on the only test there is --
a maqaf is written in it -- and what sets it apart is only that its non-final atom keeps the
accent it has.  What the maqaf SIGNIFIES is unsettled in both books and nothing here turns on
it: Yeivin's "must be joined to the following word" reads as denying a pause rather than as
making one accented unit, since he writes these very compounds with a space at §354; Breuer CoS
Ch. 1 §43 records that "different views have been expressed" and leaves the maqaf out of the
book, while Ch. 9 §37 points the other way.
``chanted_word_accents.maqaf_after_gaya`` measures it -- thirteen of MAM's twenty-two compounds
with their accents split across atoms, one of WLC's forty-five -- and settles that MAM's four
merkha-with-tipexa, three mahapakh-with-pashta, four merkha-with-silluq, one merkha-with-pashta and
one munax-with-zaqef are all of that one kind.  A CONFIGURATION cannot tell them apart, because
WLC's hits with the same pairs are not of that kind, so the labels above say what the pair can and
cannot settle and the routing is left alone.  Giving §357 a route of its own would move counts
that no other change here moves, so it is Ben's call, not a tidy-up.  Issue wlc-utils#86.

POSITION IS EVIDENCE, NOT THE CRITERION.  Whether a non-final atom's accent sits where that atom's
own accent sits is answered exactly, with no phonology, by an in-corpus oracle: the same spelling
standing FREE elsewhere in the same corpus -- an atom that is a whole chanted word by itself, so
it has its own accent (``build_oracle``).  Key each atom by its letters and points with accents
stripped, and compare base letters after the accent.

* A **no** is decisive.  WLC's Nu 9:17 ואחרי־כן has its munax three letters from the end where
  the free ואחרי usually put theirs one from the end, so it cannot be that atom's own accent.
* A **yes is not decisive**, which is the trap.  A secondary accent can land on the atom's own
  stress anyway: MAM's שלף־חרב has its merkha where the free שלף usually have theirs, because
  nasog axor has retracted the stress before חרב, and it is still routed by its
  ``(MERKHA, SILLUQ)`` configuration.  So the CONFIGURATION decides the route and the
  oracle corroborates -- never the other way round.  (What the oracle sees at שלף־חרב is now
  read the other way as well: the merkha IS that atom's own accent, and the maqaf after it is
  ITM §357's -- see the third-thing paragraph above.)  Neither example states a figure here: the
  counts live in each occurrence's own ``oracle`` fields in the tracked JSON
  (``joined_letters_after_accent``, ``free_letters_after_accent``, ``free_occurrences``), and
  they regenerate with the survey.

Two refinements the oracle needs, both of which silently inverted verdicts before they were made:
the free side takes the LAST IMPOSITIVE accent, because a secondary accent always precedes the
main one and taking the first reads a restored secondary as the atom's own position; and
postpositive/prepositive accents are skipped entirely, since their position is a fact about the
chanted word's edge rather than about any atom's stress.

§293's further claim -- that the habit correlates with penultimate stress -- is NOT tested here.
That needs a real stress model; ``../al-hatorah/py/aht_phon/stress.py`` is the prior art.  Nothing
below changes that: ``final_stress`` answers one question about one syllable, and MAM has no
route-(b) hit for §293's claim to be tested on either way.

WHERE THE STRESS FALLS is a second measurement, and a narrow one.  The ``*_final_stress_by_pair``
fields say, of each pair whose accent written last is written on the stress, how many of its
chanted words are stressed on their last syllable.  ``final_stress`` is the rule, and its docstring
says why counting nuclei answers this without any of the phonology issue wlc-utils#48 is about.

WHAT THE SURVEY IS A SURVEY OF, which bounds every number it produces.  ``out/wlc422-kq-u`` is the
Westminster transcription of L.  ``in/UXLC-39`` is NOT a second manuscript -- its own header
records that it was produced from WLC 4.20 by WLC2XML -- so it is the same transcription plus
Kimball's corrections, and agreement between the two is not corroboration by a second hand.
MAM-simple is a CONSENSUS text rather than a diplomatic one -- no single manuscript's reading.
It largely follows Breuer, but it is not one of Breuer's own editions (Horev; and the Jerusalem
Crown, which he advised on).  There is therefore no second manuscript here at all: the
counts measure L as Westminster reads it, and what an edition does with it.  ``CORPUS_KIND``
records that so the page cannot state a corpus's standing wrongly.

THE GRAY MAQAF COUNTS AS A MAQAF, and only MAM has one.  A compound is found here by its maqaf,
and in poetic verses the maqaf after a secondary mark is customarily left unwritten while the atom
still counts as joined -- so a scan of written maqafs alone reaches only part of the poetic
phenomenon.  MAM's answer to that is the gray maqaf (מקף אפור), its mark for a maqaf the
manuscript leaves unwritten where the chanted word needs one, and MAM-simple has all 116 of them
as ``implicit-maqaf`` nodes, which ``mam_simple_verse`` puts on the atom before (issue wlc-utils#91).  Ben,
2026-07-31, on what the survey then counts: a gray maqaf is a maqaf.  That took MAM's poetic hits
from 17 to 130, while WLC's and UXLC's, those texts having no such mark, stay floors -- so MAM's
poetic figure is incomparable with theirs on top of no poetic figure being comparable with a prose
one.

``gray_maqaf_survey`` counts the mark separately all the same, and reads MAM-parsed-plus for it.
NOT because MAM-simple lacks it: the two agree exactly, 116 occurrences in the same verses, none
outside Psalms, Proverbs and Job, and MAM-basics maps the ``מ:מקף אפור`` template to the
``implicit-maqaf`` node (``../MAM-basics/py/foi/foiz_wt_rare_tmpls.py``).  Two wrong claims fell at
issue wlc-utils#91 and neither should come back.  This docstring and the tracked JSON's ``source`` string
both said MAM-simple DROPS the mark, which is what sent the survey to a second corpus for it.  And
the replacement wlc-utils#91 itself proposed -- that what MAM-simple drops is a seven-way kind distinction
MAM-parsed-plus keeps -- is wrong the same way: the ``מ:מקף אפור`` template carries no parameters
at all, so the doctrine's seven types (Breuer, Chapter 9 §§18-36, set out in MAM's Wikisource
introduction, authored at ``../MAM-basics/py/author_misc/
he_ws_intro_to_mam_gray_maqaf_*.mediawiki``) are in the prose and in neither data file.  What the
separate count is FOR is the TWO-kind split this module derives itself, only one kind of which
answers this page's question: an oleh with its yored, and a tsinnorit with its partner, are ONE
accent written across two atoms.

Run via ``main_accgram.py generate-html-maqaf-nonfinal-accents``.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

from accgram import accent_marks as am
from accgram import final_stress as fs
from accgram import poetic_filter, prose_filter, rtms_data
from wlc_cmn.wlc_book_codes import wlc_bb_codes
from mb_cmn import file_io
from mb_cmn import provenance
from mb_cmn.hebrew_accents import ATN_H
from mb_cmn.hebrew_punctuation import NU_GMAQ
from mb_cmn.str_defs import DOUB_VERT_LINE
from mb_diff_mpu.mpplus_flatten import flatten_ep_for_diff

import wlc_paths

MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
METEG = "\N{HEBREW POINT METEG}"
PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
NUN_HAFUKHA = "\N{HEBREW PUNCTUATION NUN HAFUKHA}"

# The pseudo-mark for a verse-final U+05BD.  Not an accent codepoint, so it needs its own token
# in the shape strings and in the configuration table.
SILLUQ = "silluq"

# Marks stripped when keying an atom for the free-standing oracle: two spellings of one atom must
# key alike whether or not one of them has punctuation.
_STRIPPED_FOR_KEY = frozenset((METEG, PASEQ, SOF_PASUQ, NUN_HAFUKHA))

# Accents written at a fixed EDGE of the chanted word rather than on its stress.  Their position
# says nothing about where an atom's own accent falls, so the oracle ignores them.  The set itself
# now lives in ``final_stress``, which asks the same thing of the same accents for the other
# measurement here and is the module about stress; this module had the only copy of it.

# Route (a): Yeivin's closed prose list, keyed by (accent on the non-final atom, accent the
# compound has).  Membership is a fact about the configuration, not about the mark's position -- see the
# module docstring on why position cannot be the criterion.
#
# Two citations were wrong until 2026-07-28, both settled by reading the full OCR at
# ``../masorah-books/books/itm/md-export-of-docx/`` -- that repo was ``yeivin-itm`` until it was
# renamed on 2026-07-31 (issue wlc-utils#86, which holds the Yeivin-inventory questions;
# wlc-utils#82, cited here at first, is about his two Deuteronomy 33 maqaf readings instead).
# Merkha-tevir is §253, ``Merka-tevir and the
# Servi of Tevir``, not §§233/241.  And §241 pairs a secondary mahapakh with PASHTA, not with
# tevir -- which is why the ``(MAHAPAKH, TEVIR)`` entry it licensed had never fired in any corpus,
# in either genre, since the survey was written.  A third citation fell on 2026-07-30:
# ``(MERKHA, SILLUQ)`` borrowed §233 too, and §233 is tipexa-only -- no section of ITM names a
# secondary merkha in the silluq's chanted word (§209 gives the silluq one conjunctive and no
# secondary), so that entry's label stopped citing a section on 2026-07-30.  Two more fell on
# 2026-08-03, both settled in ``chanted_word_accents.maqaf_after_gaya``.  Metigah-zaqef is DEFINED
# at §223; §224 is the retraction of metigah, which discusses the combination without being where
# it is given.  And the four MAM compounds ``(MERKHA, SILLUQ)`` covers are all שלף־חרב, where the
# merkha is that atom's own accent with a gaʿya after it and then ITM §357's maqaf -- so the label
# now names §357 rather than reporting that no section covers it.  The four MAM ``(MERKHA,
# TIPEXA)`` compounds and the three ``(MAHAPAKH, PASHTA)`` ones are §357's too, but WLC's are not,
# so those two labels stay as the pair-level statements they are and say what the pair can and
# cannot settle.
_NAMED_CONFIGURATIONS: dict[tuple[str, str], str] = {
    (am.QADMA, am.ZAQEF_QATAN): "metigah-zaqef (ITM §223)",
    (am.MUNAX, am.ZAQEF_QATAN): "munax-zaqef (ITM §221)",
    (am.TIPEXA, am.ATNAX): "mayela before an etnaxta (ITM §216)",
    (am.TIPEXA, SILLUQ): "mayela before a silluq (ITM §210)",
    (
        am.MERKHA,
        am.TIPEXA,
    ): "secondary merkha in the tipexa's chanted word (ITM §233), or ITM §357's maqaf after gaʿya",
    (
        am.MERKHA,
        SILLUQ,
    ): "ITM §357's maqaf after gaʿya (no section names a secondary merkha with silluq)",
    (am.MERKHA, am.TEVIR): "secondary merkha in the tevir's chanted word (ITM §253)",
    (
        am.MAHAPAKH,
        am.PASHTA,
    ): "secondary mahapakh in the pashta's chanted word (ITM §241), or ITM §357's maqaf after gaʿya",
    (am.QADMA, am.GERESH): "secondary azla in the geresh's chanted word (ITM §268)",
    (am.MUNAX, am.ATNAX): "secondary munax in the etnaxta's chanted word (ITM §215)",
    (am.MUNAX, am.REVIA): "secondary munax in the revia's chanted word (ITM §236)",
    (am.MUNAX, am.PAZER): "secondary munax in the pazer's chanted word (ITM §276)",
}

# TWO MARKS ARE NOT ALWAYS TWO ACCENTS, and on a SIMPLE chanted word the difference has to be
# made mechanically, this scan having no accent tokenization to lean on.  Two kinds of pair are
# set aside, each by a rule that reads the word rather than a list of references:
#
# * A stress-helper pair, where one accent is written twice under two codepoints.  Six accents
#   can need a stress helper, and for five of them the helper shares its accent's codepoint, so
#   a repeated mark never reaches here: that is one accent already, the same rule the compound
#   side applies.  The zarqa is the sole exception, and only because Unicode's two names are in
#   effect swapped -- U+0598 "HEBREW ACCENT ZARQA" is the HELPER and U+05AE "HEBREW ACCENT
#   ZINOR" is the zarqa.  So in a prose verse U+0598 before U+05AE is the zarqa written at the
#   chanted word's edge and again on the stressed syllable: one accent and its helper.  In a
#   POETIC verse the same two codepoints are the genuine and distinct tsinnorit and tsinnor,
#   which is why this rule is stated of prose -- and no poetic chanted word in any of the three
#   corpora carries the pair, so the exclusion has never had to decide a poetic case.
#   ``simple_exclusion`` asserts as much, so that stays true by construction rather than by
#   luck (item 15 of ``doc/review-findings-2026-07-29.md``).  See
#   ``_ZARQA_HELPER`` below for why ``accent_marks`` still spells them after the poetic sense.
# * Two marks on ONE LETTER.  Whatever such a pair is, it is not two accents on two syllables,
#   and the six in MAM's prose verses are of two kinds that a reader would want kept apart from
#   the rest either way -- five a geresh or gershayim with a telisha gedola, one (Ezekiel 20:31)
#   a mahapakh with a qadma.  MAM-basics' own sec-merk FOI profiles mark the same configuration,
#   with a ``+`` for two accents sharing a letter.
#
# The counts of each land in the survey, so a page can say what it leaves out and how much.
SIMPLE_EXCL_ONE_LETTER = "the two marks are on one letter"
SIMPLE_EXCL_STRESS_HELPER = "a stress-helper pair: one accent written twice"

# ``accent_marks`` spells these two constants after the poetic sense, where the tsinnorit and
# the tsinnor are distinct accents; ``mb_cmn`` has the honest names, ZSH_OR_TSIT and Z_OR_TSOR.
# Renaming them in ``accent_marks`` would reach the poetic scanner and its tests, so it is left
# to issue wlc-utils#85 and aliased here, at the one place in this module that reads them as prose.  The
# ``_ACCENT_SHORTHAND`` table below deliberately does NOT follow: its "tsit" and "tsor" label
# poetic rows too, where the poetic names are the right ones.
_ZARQA_HELPER = am.TSINNORIT  # U+0598
_ZARQA = am.TSINNOR  # U+05AE

_ONE_ACCENT_WRITTEN_TWICE = frozenset((frozenset((_ZARQA_HELPER, _ZARQA)),))

ROUTE_SECONDARY = "a: a secondary accent the compound inherits"
ROUTE_HABIT = "b: a maqaf after an atom that keeps its own conjunctive (ITM §293)"
ROUTE_UNDECIDED = "?: undecided -- the non-final atom never stands free"
# The poetic corpus is deliberately left unrouted; see ``classify``.
ROUTE_NOT_ATTEMPTED = "(not attempted -- the route split is prose doctrine)"

# Each corpus's standing, which the page must state and must not overstate.
CORPUS_KIND = {
    "wlc422": "diplomatic: the Westminster transcription of the Leningrad Codex",
    "uxlc": "produced from WLC 4.20 by WLC2XML -- the same transcription, corrected",
    "mam_simple": "consensus, not diplomatic; largely follows Breuer, but not an edition of his",
}

_ACCENT_SHORTHAND = {
    am.ATNAX: "etn",
    am.SEGOLTA: "seg",
    am.SHALSHELET: "shal",
    am.ZAQEF_QATAN: "zaq",
    am.ZAQEF_GADOL: "zaqg",
    am.TIPEXA: "tip",
    am.REVIA: "rev",
    am.TSINNORIT: "tsit",
    am.PASHTA: "pash",
    am.YETIV: "yet",
    am.TEVIR: "tev",
    am.GERESH: "ger",
    am.GERESH_MUQDAM: "germ",
    am.GERSHAYIM: "ger2",
    am.QARNEY_PARA: "qar",
    am.TELISHA_GEDOLA: "telg",
    am.PAZER: "paz",
    # U+05A2 (mb_cmn's ``ATN_H``) has no ``accent_marks`` alias: the mark is poetic-only, and
    # the WLC scanners never meet it -- the LC has galgal (U+05AA) where MAM and UXLC have
    # atnax-hafukh as the oleh-weyored servus (see ``mam_poetic_accents``).  Poetic keys in
    # ``simple_by_pair`` reach it all the same; without this entry, ``shape_of``'s fallback
    # leaked the bare combining mark itself into the tracked JSON keys, against the repo's
    # no-orphan-combining-marks rule (item 11 of ``doc/review-findings-2026-07-29.md``).
    ATN_H: "atnh",
    am.MUNAX: "mun",
    am.MAHAPAKH: "mah",
    am.MERKHA: "mer",
    am.MERKHA_KEFULA: "mer2",
    am.DARGA: "dar",
    am.QADMA: "qad",
    am.TELISHA_QETANA: "telq",
    am.YERAX: "yby",
    am.OLE: "ole",
    am.ILUY: "ilu",
    am.DEXI: "dex",
    am.TSINNOR: "tsor",
    SILLUQ: "sil",
}


# --- low-level predicates -----------------------------------------------------


def is_accent(ch: str) -> bool:
    """An accent (U+0591..U+05AE); U+05BD (meteg/silluq) excluded."""
    return "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW ACCENT ZINOR}"


def is_base_letter(ch: str) -> bool:
    return "א" <= ch <= "ת"


# --- reading the three corpora into {bcv: [chanted word, ...]} ----------------


def _join_on_maqaf(atoms: list[str]) -> list[str]:
    """Fold a flat atom list into CHANTED WORDS, an atom ending in a maqaf continuing into
    the next.

    Mirrors ``uni_to_marks.verse_to_marks``' boundary logic, which is what makes a maqaf
    compound one chanted word here as it is there.  Every ``words``-named local and every
    ``[word, ...]`` value in this module is a list of chanted words in this sense; the
    identifiers keep the shorter name, as the wlc-utils#81 sweep left the repo's others.
    """
    words: list[str] = []
    pending = ""
    for atom in atoms:
        pending += atom
        if not pending.endswith(MAQAF):
            words.append(pending)
            pending = ""
    if pending:
        words.append(pending)
    return words


def wlc_words(kq_u_dir: Path) -> dict[str, list[str]]:
    index = rtms_data.load_wlc422_index(kq_u_dir)
    return {
        bcv: _join_on_maqaf(
            [a for vel in (verse.get("vels") or []) for a in _wlc_vel_atoms(vel)]
        )
        for bcv, verse in index.items()
    }


def _wlc_vel_atoms(vel: object) -> list[str]:
    """The pointed atoms of one verse element; the ketiv is dropped, the qere kept.

    A ketiv is unpointed and never accented, so it can only add spurious unaccented atoms;
    the qere is the side that has the marks the scanners read.
    """
    if isinstance(vel, str):
        return [vel]
    if not isinstance(vel, dict):
        return []
    if isinstance(vel.get("sam_pe_inun"), str):
        return []
    kq = vel.get("kq")
    if kq is not None:
        _ketiv, qere = (
            kq if isinstance(kq, (list, tuple)) and len(kq) == 2 else ([], [])
        )
        return [a for sub in qere for a in _wlc_vel_atoms(sub)]
    word = vel.get("word")
    return [word] if isinstance(word, str) else []


def mam_words(
    refs_by_book: dict[str, set[tuple[int, int]]], mam_simple_dir: Path | None = None
) -> dict[str, list[str]]:
    """MAM-simple's chanted words for the given refs.

    ``mam_simple_dir`` defaults to the BHS versification, which is the one this survey wants:
    every corpus here is keyed to WLC's refs, so all three read alike.  A caller comparing against
    another MAM-derived text passes MAM's native versification instead.
    """
    from accgram import mam_simple_verse

    loaded = mam_simple_verse.load_mam_simple_for_refs(
        mam_simple_dir or wlc_paths.require_mam_simple_dir(), refs_by_book
    )
    return {
        bcv: _join_on_maqaf(
            [v for v in payload["mam_simple_verse"]["vels"] if isinstance(v, str)]
        )
        for bcv, payload in loaded.items()
    }


# UXLC ships one XML per book under its own English filename; map those onto the WLC 2-char
# book codes the genre filters and the bcv keys use.  Public, with ``uxlc_text`` below, because
# ``chanted_word_accents`` reads the same files a different way -- it needs the ATOMS, where this
# module needs them already folded into chanted words -- and a second copy of the filename map
# would be a second thing to keep right.
UXLC_FILE_TO_BB = dict(
    zip(
        (
            "Genesis Exodus Leviticus Numbers Deuteronomy Joshua Judges Samuel_1 Samuel_2"
            " Kings_1 Kings_2 Isaiah Jeremiah Ezekiel Hosea Joel Amos Obadiah Jonah Micah"
            " Nahum Habakkuk Zephaniah Haggai Zechariah Malachi Psalms Proverbs Job"
            " Song_of_Songs Ruth Lamentations Ecclesiastes Esther Daniel Ezra Nehemiah"
            " Chronicles_1 Chronicles_2"
        ).split(),
        wlc_bb_codes(),
    )
)


def uxlc_words(uxlc_dir: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for path in sorted(uxlc_dir.glob("*.xml")):
        bb = UXLC_FILE_TO_BB.get(path.stem)
        if bb is None:
            raise ValueError(f"unmapped UXLC book file: {path.name}")
        for chapter in ET.parse(path).getroot().iter("c"):
            chnu = int(chapter.get("n"))
            for verse in chapter.iter("v"):
                vrnu = int(verse.get("n"))
                atoms = [uxlc_text(el) for el in verse if el.tag in ("w", "q")]
                out[f"{bb}{chnu}:{vrnu}"] = _join_on_maqaf(atoms)
    return out


def uxlc_text(el) -> str:
    """The Hebrew of one UXLC ``<w>``/``<q>``, with ``<x>`` note markers dropped.

    An ``<x>`` holds a Latin note letter, not text; left in, it lands mid-word and splits an
    atom that has no business being split.
    """
    parts = [el.text or ""]
    for child in el:
        if child.tag != "x":
            parts.append(uxlc_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def split_bcv(bcv: str) -> tuple[str, int, int]:
    bb = bcv[:2]
    chnu, _colon, vrnu = bcv[2:].partition(":")
    return bb, int(chnu), int(vrnu)


# --- the scan -----------------------------------------------------------------


def atom_accents(word: str, verse_final: bool) -> list[list[str]]:
    """Accents per atom of one chanted word, silluq included when it is the verse's last.

    Elsewhere a U+05BD is an ordinary meteg and is dropped: it is not an accent, and counting
    it would turn every non-final atom that has ITM §337's ga'ya into a false hit.
    """
    atoms = word.split(MAQAF)
    per_atom = [[c for c in atom if is_accent(c)] for atom in atoms]
    if verse_final and _last_atom_has_silluq(atoms[-1]):
        per_atom[-1].append(SILLUQ)
    return per_atom


def _last_atom_has_silluq(atom: str) -> bool:
    """Whether the verse-final chanted word's last atom has a silluq: a U+05BD with no accent
    after it, before the atom's own sof pasuq if it has one.

    The same immediately-before-sof-pasuq rule the scanners apply (``prose_scanner``'s SILLUQ
    lookahead; ``meteg_silluq_context.u05bd_is_silluq``); the chanted-word survey inherits it
    by counting tokens.  A bare ``METEG in atom`` containment stood here until 2026-07-30 and
    would have counted a hypothetical early meteg followed by an accent as the silluq (item 16
    of ``doc/review-findings-2026-07-29.md``).  No corpus has such an atom today, which the
    regeneration diff is the check on: this change moves no classification.
    """
    last_mark_is_u05bd = False
    for ch in atom:
        if ch == SOF_PASUQ:
            break
        if ch == METEG:
            last_mark_is_u05bd = True
        elif is_accent(ch):
            last_mark_is_u05bd = False
    return last_mark_is_u05bd


def stress_mark_letter(word: str, verse_final: bool) -> int | None:
    """Ordinal of the base letter bearing the chanted word's main accent, counting base letters
    from 1 across the whole chanted word; None when the mark written last is not one that marks
    the stress.

    ``final_stress`` needs the letter and deliberately declines to find it, two things this
    module knows and it does not standing between the mark and the letter.  A U+05BD is the
    silluq only on the verse's last chanted word, by the same ``_last_atom_has_silluq`` rule
    ``atom_accents`` applies, and it marks the stress where it is; elsewhere it is a meteg, which
    the shapes do not count and neither does this.  And where the last mark is a
    postpositive or a prepositive one, its position is a fact about the chanted word's edge, so
    there is no answer to give rather than a wrong one.
    """
    silluq = verse_final and _last_atom_has_silluq(word.split(MAQAF)[-1])
    last_mark = None
    last_letter = 0
    seen = 0
    for ch in word:
        if is_base_letter(ch):
            seen += 1
        elif is_accent(ch) or (silluq and ch == METEG):
            last_mark, last_letter = ch, seen
    if last_mark is None or last_mark in fs.NOT_IMPOSITIVE:
        return None
    return last_letter


def final_stress(word: str, verse_final: bool) -> bool | None:
    """Whether this chanted word is stressed on its last syllable; None when no mark says."""
    letter = stress_mark_letter(word, verse_final)
    if letter is None:
        return None
    return fs.is_final_stress(word, letter)


def shape_of(per_atom: list[list[str]]) -> str:
    """``mun-mun``, ``qad-zaq``, ``0-mer-sil`` -- one field per atom, ``0`` for an unaccented
    one, the dash standing for the maqaf, as in the edition transcriptions' own notation.
    """
    return "-".join(
        "+".join(_ACCENT_SHORTHAND.get(a, a) for a in atom) or "0" for atom in per_atom
    )


def scan(
    words_by_bcv: dict[str, list[str]], keep, *, prose: bool
) -> tuple[list[dict], int, int, list, list]:
    """(hits, verses, maqaf compounds, simple two-accent words, concentrators) for one corpus
    and genre.  ``prose`` says which genre ``keep`` selects; ``simple_exclusion`` needs it.

    The fourth return is what a chanted word that is a LONE atom does with two accents, which
    the first three know nothing about: they are the compound survey, and a compound is what
    the maqaf makes.  A page saying two accents can appear on a chanted word whether it is
    compound or simple was making half that claim with nothing behind it (Ben, 2026-07-28: "it
    would be useful to know how many of these pairs appear on a compound chanted word, and how
    many appear on a simple chanted word"), so the same pass counts the simple ones.

    The fifth return is the two-accent compounds the hits criterion excludes: both accents on
    the FINAL atom, none on a non-final one.  The scan used to drop these silently, so the
    page could count the compounds that spread their two accents across two atoms but not the
    ones that concentrate both on the last atom (Ben, 2026-07-29, naming the two kinds
    "spreaders" and "concentrators").  Each record mirrors a simple one -- a lone final atom
    holds its two marks just as a simple chanted word does, so the same rules read them.

    A field of REPEATS is one accent written twice, not two accents -- the same rule the
    compound side applies -- so an atom counts here only when its accents are two DIFFERENT
    marks.  Order is the written order, which is the order the shapes are read in throughout.
    Two different marks are still not always two accents, so each simple and each concentrator
    record carries an ``excluded`` reason or ``None``; see ``SIMPLE_EXCL_ONE_LETTER`` above
    for the two rules.
    """
    hits: list[dict] = []
    simple: list[dict] = []
    concentrators: list[dict] = []
    n_verses = n_compounds = 0
    for bcv, words in words_by_bcv.items():
        if not keep(*split_bcv(bcv)):
            continue
        n_verses += 1
        last = len(words) - 1
        for i, word in enumerate(words):
            if MAQAF not in word:
                accents = atom_accents(word, i == last)[0]
                if len(set(accents)) > 1:
                    simple.append(
                        {
                            "bcv": bcv,
                            "word": word,
                            "shape": shape_of([accents]),
                            "pair": [
                                _ACCENT_SHORTHAND.get(a, a) for a in _distinct(accents)
                            ],
                            "excluded": simple_exclusion(word, accents, prose=prose),
                            "final_stress": final_stress(word, i == last),
                        }
                    )
                continue
            n_compounds += 1
            per_atom = atom_accents(word, i == last)
            if not any(per_atom[:-1]):
                final = per_atom[-1]
                if len(set(final)) > 1:
                    concentrators.append(
                        {
                            "bcv": bcv,
                            "word": word,
                            "shape": shape_of(per_atom),
                            "pair": [
                                _ACCENT_SHORTHAND.get(a, a) for a in _distinct(final)
                            ],
                            "excluded": simple_exclusion(word, final, prose=prose),
                            "final_stress": final_stress(word, i == last),
                        }
                    )
                continue
            hits.append({"bcv": bcv, "word": word, "atoms": per_atom})
    return hits, n_verses, n_compounds, simple, concentrators


def simple_exclusion(word: str, accents: list[str], *, prose: bool) -> str | None:
    """Why this chanted word's two marks are not two accents, or None if they are.

    Both rules read the word itself rather than a list of references; see the two
    ``SIMPLE_EXCL_*`` constants above for what each is and why it is set aside.  The one-letter
    rule is applied first, so a word that is both keeps the sharper reason.

    ``prose`` is the stress-helper rule's genre guard: in a poetic verse U+0598 and U+05AE are
    the genuine and distinct tsinnorit and tsinnor -- two accents, not one written twice -- so
    the label would be wrong there.  No poetic chanted word in any of the three corpora has
    the pair; the assert keeps that a checked fact (item 15 of
    ``doc/review-findings-2026-07-29.md``), so a corpus bump that produced one stops the build
    for a decision instead of inheriting a prose-only label.

    Named for the simple records, which were its only callers first, but the concentrator
    records take their reason here too: ``accents`` is then the final atom's, and ``word``
    stays the whole compound, which the one-letter rule may rightly read whole -- every accent
    of a concentrator is in its final atom.
    """
    if _accents_share_a_letter(word):
        return SIMPLE_EXCL_ONE_LETTER
    if frozenset(accents) in _ONE_ACCENT_WRITTEN_TWICE:
        assert prose, f"U+0598 with U+05AE on a poetic chanted word: {word!r}"
        return SIMPLE_EXCL_STRESS_HELPER
    return None


def _accents_share_a_letter(word: str) -> bool:
    """True when one base letter of the word has two DIFFERENT accents on it."""
    on_letter: dict[int, set[str]] = defaultdict(set)
    seen = 0
    for ch in word:
        if is_base_letter(ch):
            seen += 1
        elif is_accent(ch):
            on_letter[seen].add(ch)
    return any(len(accents) > 1 for accents in on_letter.values())


def _distinct(accents: list[str]) -> list[str]:
    """The accents in written order, a run of the same mark collapsed to one occurrence."""
    out: list[str] = []
    for accent in accents:
        if accent not in out:
            out.append(accent)
    return out


# --- the free-standing oracle -------------------------------------------------


def oracle_key(atom: str) -> str:
    """The atom's letters and points, accents and punctuation stripped, so a joined and a
    free occurrence of one atom key alike."""
    return "".join(c for c in atom if not is_accent(c) and c not in _STRIPPED_FOR_KEY)


def letters_after_accent(atom: str, *, main_only: bool = False) -> int | None:
    """Base letters strictly after the letter that has the accent; None if there is no accent.

    ``main_only`` takes the last IMPOSITIVE accent, which is the atom's own: a secondary
    accent always precedes the main one, so taking the first would read a restored secondary
    as the atom's own position -- which is exactly what MAM's שלף does.  Without it, take the
    sole accent, which is all a non-final atom ever has.
    """
    letters_before: list[int] = []
    seen = 0
    for ch in atom:
        if is_base_letter(ch):
            seen += 1
        elif is_accent(ch) and not (main_only and ch in fs.NOT_IMPOSITIVE):
            letters_before.append(seen)
    if not letters_before:
        return None
    return seen - (letters_before[-1] if main_only else letters_before[0])


def build_oracle(words_by_bcv: dict[str, list[str]], keep) -> dict[str, Counter]:
    """key -> Counter of letters-after-accent, over atoms standing FREE -- that is, over
    chanted words of one atom, which therefore have that atom's own accent.

    Verse-final ones are excluded along with the joined: there the U+05BD is a silluq that
    this counter does not see, so such an atom would look unaccented or mis-positioned.
    """
    oracle: dict[str, Counter] = defaultdict(Counter)
    for bcv, words in words_by_bcv.items():
        if not keep(*split_bcv(bcv)):
            continue
        last = len(words) - 1
        for i, word in enumerate(words):
            if MAQAF in word or i == last:
                continue
            n = letters_after_accent(word, main_only=True)
            if n is not None:
                oracle[oracle_key(word)][n] += 1
    return oracle


# --- classification -----------------------------------------------------------


def _accented_nonfinal_atom(hit: dict) -> str:
    return next(
        a for a in hit["word"].split(MAQAF)[:-1] if any(is_accent(c) for c in a)
    )


def _single(accents: list[str]) -> str | None:
    return accents[0] if len(accents) == 1 else None


def classify(hit: dict, oracle: dict[str, Counter], *, routed: bool) -> dict:
    """Route, configuration and oracle evidence for one hit.

    The returned record is what lands in the tracked JSON, so its keys are read by people, not
    only by code: ``word`` is the whole CHANTED WORD (the maqaf compound, joined atoms and all),
    ``shape`` its per-atom accents, and the oracle fields count base letters, not syllables.
    The key keeps the short name, as wlc-utils#81 left the repo's other ``word``-named identifiers.

    ``routed`` is false for the poetic corpus, where the route split is NOT attempted: both
    halves of it are prose doctrine.  ``_NAMED_CONFIGURATIONS`` is Yeivin's PROSE inventory,
    and the poetic counterpart is a different list (his §372 tsinnorit -- ITM spells it with
    an s, this repo with ts; Breuer's Chapter 9 §§23-26 secondary mahapakh/merkha, the span he
    cites for it himself in §27, checkable in
    ``../masorah-books/books/cos/md-export-of-docx/C09-S021.md``),
    which is not encoded here.  Running the prose list
    over poetic verses would label a poetic secondary as unnamed and read it as §293's habit,
    which is why the poetic side reports shapes and counts only.
    """
    per_atom = hit["atoms"]
    atom = _accented_nonfinal_atom(hit)
    joined = letters_after_accent(atom)
    free = oracle.get(oracle_key(atom))
    free_usual = free.most_common(1)[0][0] if free else None
    evidence = {
        "joined_letters_after_accent": joined,
        "free_letters_after_accent": free_usual,
        "free_occurrences": sum(free.values()) if free else 0,
    }

    if not routed:
        route, named = ROUTE_NOT_ATTEMPTED, None
    else:
        nonfinal_accent = _single([a for atom_ in per_atom[:-1] for a in atom_])
        compound_accent = _single(per_atom[-1])
        named = _NAMED_CONFIGURATIONS.get((nonfinal_accent, compound_accent))
        if named is not None:
            route = ROUTE_SECONDARY
        elif free_usual is None:
            route = ROUTE_UNDECIDED
        elif joined != free_usual:
            route, named = (
                ROUTE_SECONDARY,
                "unnamed -- not at the atom's own accent position",
            )
        else:
            route, named = ROUTE_HABIT, "unnamed"

    return {
        "bcv": hit["bcv"],
        "word": hit["word"],
        "shape": shape_of(per_atom),
        "route": route,
        "configuration": named,
        "oracle": evidence,
    }


# --- MAM's gray maqaf ---------------------------------------------------------

# MAM-parsed-plus' three poetic books, keyed by the book code ``bcv`` uses.  There is no prose
# file to read: the gray maqaf occurs in poetic verses only, which the survey checks rather than
# assumes -- ``gray_maqaf_survey`` raises if a prose-cantillated verse of Job carries one.
_GRAY_MAQAF_BOOKS = (
    ("ps", "D1-Psalms.json"),
    ("pr", "D2-Proverbs.json"),
    ("jb", "D3-Job.json"),
)

# An oleh with its yored, and a tsinnorit with its partner mahapakh or merkha, are ONE accent
# written across two atoms rather than two accents on one chanted word.  A gray maqaf joining such
# a pair says nothing about the question this page asks, so the two kinds are counted apart and
# the prose quotes the kind that answers it.
_ONE_ACCENT_ACROSS_TWO_ATOMS = frozenset((am.OLE, am.TSINNORIT))

GRAY_KIND_SPREAD = "one accent written across the two atoms (an oleh-we-yored, or a tsinnorit and its partner)"
GRAY_KIND_SECOND = "a second accent on the joined atom"

# Where a chanted word ends in the flattened MAM-parsed-plus text.  A space is the ordinary
# boundary; ``flatten_ep_for_diff`` renders מ:פסק as ``DOUB_VERT_LINE`` and legarmeh as a PASEQ
# with no space around either, so a whitespace split alone would run Ps 5:5's רשע and אתה
# together into one chanted word and manufacture an accent for the atom after a gray maqaf.
_CHANTED_WORD_END = frozenset((" ", PASEQ, DOUB_VERT_LINE, SOF_PASUQ))


def _around_gray_maqaf(text: str, idx: int) -> tuple[str, str, bool]:
    """The atom a gray maqaf joins, the rest of the chanted word, and whether that is verse-final.

    ``idx`` indexes the ``NU_GMAQ`` sentinel in a flattened verse.  The far side is the REST of
    the chanted word rather than one atom, because the atom immediately after a gray maqaf need
    not be the one with the accent: Ps 5:5 לא~אל־חפץ joins לא to a compound whose accent is on
    its second atom, so an atom-to-atom reading would report the compound's own accent missing.
    Verse-finality comes back because a verse-final U+05BD is the silluq, and Ps 18:20's בי has
    nothing else -- the same rule ``atom_accents`` applies, and applied by it below.
    """
    before = text[:idx].replace(NU_GMAQ, " ")
    end = idx + 1
    while end < len(text) and text[end] not in _CHANTED_WORD_END:
        end += 1
    verse_final = end < len(text) and text[end] == SOF_PASUQ
    return before.split()[-1].split(MAQAF)[-1], text[idx + 1 : end], verse_final


def _gray_maqaf_hits(plus_dir: Path) -> list[dict]:
    """Every מ:מקף אפור in MAM-parsed-plus, with the atoms it joins and their accents."""
    hits: list[dict] = []
    for bb, filename in _GRAY_MAQAF_BOOKS:
        with (plus_dir / filename).open(encoding="utf-8") as f_in:
            chapters = json.load(f_in)["book39s"][0]["chapters"]
        for chnu, chapter in chapters.items():
            for vrnu, verse in chapter.items():
                text = flatten_ep_for_diff(verse[2])
                idx = text.find(NU_GMAQ)
                while idx >= 0:
                    joined, rest, verse_final = _around_gray_maqaf(text, idx)
                    word = joined + MAQAF + rest.replace(NU_GMAQ, MAQAF)
                    per_atom = atom_accents(word, verse_final)
                    kind = (
                        GRAY_KIND_SPREAD
                        if set(per_atom[0]) & _ONE_ACCENT_ACROSS_TWO_ATOMS
                        else GRAY_KIND_SECOND
                    )
                    hits.append(
                        {
                            "bcv": f"{bb}{int(chnu)}:{int(vrnu)}",
                            "joined_atom": joined,
                            "rest_of_chanted_word": rest,
                            "shape": shape_of(per_atom),
                            "kind": kind,
                        }
                    )
                    idx = text.find(NU_GMAQ, idx + 1)
    return hits


def gray_maqaf_survey() -> dict:
    """MAM's gray maqafs: the compounds its poetic verses join without a written maqaf.

    Not a fourth corpus beside the three above -- a second MEASURE, of the part of the poetic
    phenomenon the maqaf scan cannot reach.  See the module docstring on why it has to be, and
    on why it alone reads MAM-parsed-plus.
    """
    hits = _gray_maqaf_hits(wlc_paths.require_mam_parsed_plus_dir())
    # The claims the prose rests on, pinned where the data is rather than in the page: that the
    # mark is confined to poetic verses, so it can be described as belonging to that system; that
    # the joined atom always has exactly one accent, which is what makes it worth a gray maqaf at
    # all; and that another accent always falls later in the same chanted word, without which
    # "two marks in one chanted word" -- the whole reason the count is worth quoting -- would be
    # false of some of them.  The atom right after the gray maqaf is NOT pinned: Ps 5:5 is a real
    # case where it has no accent and the compound's accent is one atom further on.
    for hit in hits:
        bb, chnu, vrnu = split_bcv(hit["bcv"])
        assert poetic_filter.should_keep_line(bb, chnu, vrnu), hit
        fields = hit["shape"].split("-")
        assert fields[0] != "0" and "+" not in fields[0], hit
        assert any(field != "0" for field in fields[1:]), hit
    return {
        "what": (
            "MAM's מקף אפור: a maqaf the manuscript leaves unwritten where the chanted word"
            " needs one. The doctrine is Breuer, Chapter 9 §§18-36, set out in MAM's Wikisource"
            " introduction; the two atoms are one chanted word, and the joined one is often"
            " pointed as though the maqaf were there."
        ),
        "source": (
            "MAM-parsed-plus (the מ:מקף אפור template). MAM-simple has the same 116, in the"
            " same verses, as its implicit-maqaf node, and the corpus counts above read them"
            " as maqafs; this count is here for the two-kind split beside them, not because"
            " one of the two texts has the mark and the other has not."
        ),
        "total": len(hits),
        "by_book": dict(Counter(h["bcv"][:2] for h in hits).most_common()),
        "by_kind": dict(Counter(h["kind"] for h in hits).most_common()),
        "by_shape": dict(Counter(h["shape"] for h in hits).most_common()),
        "occurrences": sorted(hits, key=lambda h: (h["kind"], h["shape"], h["bcv"])),
    }


# --- the survey ---------------------------------------------------------------


def _examples(simple: list[dict]) -> dict[str, dict]:
    """One chanted word per pair -- the first in corpus order, so a run cannot shuffle them.

    The reference comes with the word (2026-07-29): a page showing an example is showing one
    place out of many, and a reader who wants to look it up should not have to go find it.
    """
    out: dict[str, dict] = {}
    for record in simple:
        out.setdefault(
            "-".join(record["pair"]), {"word": record["word"], "bcv": record["bcv"]}
        )
    return out


def _final_stress_counts(records: list[dict]) -> dict[str, int]:
    """pair -> how many of its chanted words are stressed on their last syllable.

    A pair appears here only when the last accent of the pair is one that marks the stress, so an
    absent pair is one no mark answers for rather than one whose answer is zero -- and a pair
    that IS here has every one of its chanted words measured, the accent written last being the
    same accent throughout the pair.  Read a count against the pair's own entry in
    ``simple_by_pair`` or ``concentrator_by_pair``: equal counts mean every one of them is
    stressed on its last syllable.

    A pashta's or a telisha qetana's position is a fact about the chanted word's edge rather than
    about its stress, which is why those pairs are left out instead of counted at zero; see
    ``final_stress.NOT_IMPOSITIVE``.
    """
    counts: Counter = Counter()
    for record in records:
        if record["final_stress"] is None:
            continue
        counts["-".join(record["pair"])] += 1 if record["final_stress"] else 0
    return dict(counts.most_common())


def _genre_survey(words_by_bcv, keep, oracle, *, routed: bool, prose: bool) -> dict:
    hits, n_verses, n_compounds, simple, concentrators = scan(
        words_by_bcv, keep, prose=prose
    )
    counted = [s for s in simple if s["excluded"] is None]
    conc_counted = [c for c in concentrators if c["excluded"] is None]
    classified = [classify(h, oracle, routed=routed) for h in hits]
    return {
        "verses": n_verses,
        "maqaf_compounds": n_compounds,
        "hits": len(classified),
        # Simple chanted words with two accents: the other half of "compound or simple".  Only
        # the counts per pair are kept, not the occurrences -- there are far more of these than
        # of the compound hits, and no page asks which verses they are.  One EXAMPLE per pair is
        # kept, though, since a table of pairs is much easier to read with a form beside each,
        # and a page must never retype an accent.  The example is the first in corpus order, so
        # it is stable across runs.
        #
        # ``simple_two_accent_words`` counts every word with two different marks; the pair counts
        # cover the ones whose two marks are two ACCENTS, and ``simple_excluded`` holds the rest,
        # by reason and then by pair, so a page can say what it left out and how much.
        "simple_two_accent_words": len(simple),
        "simple_by_pair": dict(
            Counter("-".join(s["pair"]) for s in counted).most_common()
        ),
        "simple_example_by_pair": _examples(counted),
        # Whether each pair's chanted words are stressed on their last syllable, which the marks
        # answer wherever the accent written last is written on the stress rather than at the
        # chanted word's edge.  Ben, 2026-07-31, reversing an earlier decision to leave stress
        # alone: whether the geresh of a qadma-geresh chanted word is one some traditions would
        # call an azla turns on it, azla being the name a geresh takes on a chanted word stressed
        # on its last syllable.  ``final_stress`` is the rule, and its docstring is why the rule
        # is a narrow one rather than issue wlc-utils#48's phonology.
        #
        # COUNTS AND NOT THE WORDS, unlike ``simple_excluded_words`` below.  Listing every chanted
        # word that is NOT stressed on its last syllable ran to 2423 records across the three
        # corpora and doubled this file, and nothing reads them: no page states the exceptions,
        # since the qadma-geresh ones turned out to be ordinary penultimately-stressed forms
        # (``maqaf_nonfinal_accents_page._geresh_or_azla_note`` records that decision).  Rerun the
        # scan to name them.
        "simple_final_stress_by_pair": _final_stress_counts(counted),
        "simple_excluded": {
            reason: dict(
                Counter(
                    "-".join(s["pair"]) for s in simple if s["excluded"] == reason
                ).most_common()
            )
            for reason in sorted({s["excluded"] for s in simple if s["excluded"]})
        },
        # The excluded words THEMSELVES, which the counts above cannot show (Ben, 2026-07-29,
        # asking the page to link the sentence that reports them to "an appendix that shows
        # these in a table").  Kept where the counted simple words' occurrences are not,
        # because these are the ones a reader is invited to check: a count of what a page
        # leaves out is a claim about six particular chanted words, and MAM's prose has six of
        # them.  The poetic genres are far longer -- revia mugrash is a geresh and a revia on
        # one letter, 145 of them -- so this list is written for the prose page and is not a
        # promise that every genre's is short.
        "simple_excluded_words": [
            {
                "bcv": s["bcv"],
                "word": s["word"],
                "pair": s["pair"],
                "reason": s["excluded"],
            }
            for s in simple
            if s["excluded"]
        ],
        # Concentrators: the two-accent compounds ``hits`` excludes, both accents on the final
        # atom.  Aggregates only, as for the simple words and for the same reason -- no page
        # asks which verses they are, and one example per pair, first in corpus order, is what
        # a page shows.  ``concentrator_by_shape`` is kept where the simple side has no
        # analogue because a page pin re-derives from it that every counted concentrator has
        # exactly two distinct accents and all of them on the final atom.  ``concentrators``
        # counts the pairs that are two ACCENTS; ``concentrator_excluded`` holds the rest, by
        # reason and then by pair, exactly as ``simple_excluded`` does.
        "concentrators": len(conc_counted),
        "concentrator_by_shape": dict(
            Counter(c["shape"] for c in conc_counted).most_common()
        ),
        "concentrator_by_pair": dict(
            Counter("-".join(c["pair"]) for c in conc_counted).most_common()
        ),
        "concentrator_example_by_pair": _examples(conc_counted),
        "concentrator_final_stress_by_pair": _final_stress_counts(conc_counted),
        "concentrator_excluded": {
            reason: dict(
                Counter(
                    "-".join(c["pair"])
                    for c in concentrators
                    if c["excluded"] == reason
                ).most_common()
            )
            for reason in sorted(
                {c["excluded"] for c in concentrators if c["excluded"]}
            )
        },
        "by_route": dict(Counter(c["route"] for c in classified).most_common()),
        "by_configuration": dict(
            Counter(c["configuration"] for c in classified).most_common()
        ),
        "by_shape": dict(Counter(c["shape"] for c in classified).most_common()),
        "occurrences": sorted(
            classified, key=lambda c: (c["route"], c["shape"], c["bcv"])
        ),
    }


def build_survey() -> dict:
    """The whole survey: three corpora x two genres, every hit classified."""
    wlc = wlc_words(wlc_paths.out_dir() / "wlc422-kq-u")
    refs: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for bcv in wlc:
        bb, chnu, vrnu = split_bcv(bcv)
        refs[bb].add((chnu, vrnu))

    corpora = {
        "wlc422": wlc,
        "uxlc": uxlc_words(wlc_paths.in_dir() / "UXLC-39"),
        "mam_simple": mam_words(dict(refs)),
    }
    genres = (("prose", prose_filter, True), ("poetic", poetic_filter, False))

    survey: dict[str, object] = {
        "criterion": (
            "Within one whitespace-delimited chanted word, an accent both before and after a"
            " maqaf -- that is, on an atom the maqaf joins to the next as well as on the atom"
            " that has the compound's own accent. A U+05BD counts as an accent only on the"
            " verse's last chanted word, where it is silluq. The concentrator_* fields count"
            " the two-accent compounds this criterion excludes: two different accents both on"
            " the final atom, none on a non-final one."
        ),
        "poetic_caveat": (
            "No poetic count under ``corpora`` is comparable with a prose one, and MAM's is"
            " not comparable with WLC's or UXLC's either. Breuer (Chapter 9 §§27, 37) records"
            " that in the Three Books the maqaf after a secondary mahapakh, merkha or"
            " tsinnorit is customarily omitted in writing while the atom still counts as"
            " joined -- so a scan that finds compounds by a written maqaf misses most of the"
            " poetic phenomenon. His own 'few cases where the hyphen is not omitted' bear this"
            " out from the other side: Job 6:10 and Prov 25:20 are written WITHOUT a maqaf in"
            " WLC and UXLC, and with one only in MAM. MAM supplies the rest as its gray maqaf,"
            " and the counts here read those as maqafs -- so MAM's poetic hits below count"
            " gray-maqaf compounds alongside written-maqaf ones, while WLC and UXLC, having no"
            " such mark, keep poetic counts that are floors. ``gray_maqaf`` counts the mark on"
            " its own and splits it by kind. The routes are not attempted here either; see"
            " ``classify``."
        ),
        "gray_maqaf": gray_maqaf_survey(),
        "corpora": {},
    }
    for name, words_by_bcv in corpora.items():
        per_genre = {}
        for genre, module, routed in genres:
            keep = module.should_keep_line
            oracle = build_oracle(words_by_bcv, keep)
            per_genre[genre] = _genre_survey(
                words_by_bcv, keep, oracle, routed=routed, prose=genre == "prose"
            )
        survey["corpora"][name] = {"kind": CORPUS_KIND[name], **per_genre}
    return survey


def default_json_out_path() -> Path:
    return wlc_paths.out_dir() / "accgram" / "maqaf-nonfinal-accents.json"


def write_json(survey: dict, path: Path) -> None:
    payload = provenance.with_json_provenance(survey, __file__)
    # Through file_io for the temp-file write and the PermissionError retry; it makes
    # the directory too. LF survives the move: the repo's line-ending policy is LF in
    # the workdir as well as in git (.gitattributes, issue wlc-utils#50), and a plain text-mode
    # write would translate to CRLF on Windows and leave every regeneration looking
    # like a whole-file diff. file_io's default newline="" translates nothing, so it
    # holds the line the old explicit newline="\n" held.
    file_io.json_dump_to_file_path(payload, str(path), indent=1)
