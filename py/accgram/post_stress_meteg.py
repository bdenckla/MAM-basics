r"""Survey: MAM's metegs by position relative to the chanted word's one primary stress.

A meteg normally stands BEFORE the stress.  Both Yeivin and Breuer describe a meteg after it
as a named class -- ITM §§332, 338 and 354, CoS Ch. 8 types (a), (b) and (j) -- and neither
book gives a count.  This module supplies one, over every chanted word of MAM, and records
each occurrence so the page can list them rather than assert a total.  Issue #260's M23 at
Isaiah 23:12 is one such meteg, which is the occasion for the survey and not its subject.

Pure computation and a JSON writer -- no HTML.  ``author_site/post_stress_meteg`` renders it,
and ``main_accgram.py survey-post-stress-meteg`` runs it standalone.

THE STRESS ORACLE IS PHONETIC MAM, whose ``jta`` field marks the one stressed syllable with
``!``.  ``py/tests/test_final_stress_vs_phonetic_mam.py`` reads the same files for the same
reason: which syllable the stress falls on is not derivable from the pointing without a real
stress model, and al-hatorah's ``py/aht_phon`` has one.  A U+05BD's position is NEVER used to
infer the stress -- that would make the survey's question answer itself.

THE CORPUS IS PHONETIC MAM'S OWN TEXT, and it is a SNAPSHOT of MAM rather than MAM's current
state.  Phonetic MAM is regenerated in al-hatorah, on its own schedule, so the standard set
here can be older than the MAM-simple beside it -- and on 2026-09-04 it was, the thirty Holman
meteg suggestions of ``doc/PLAN-holman-meteg-rollout-programme.md`` among the differences.
``currency`` below MEASURES that rather than assuming it away: it counts U+05BD per verse on
both sides and names every verse where the two disagree, so the page can say which MAM its
figures describe.  Refreshing the oracle is al-hatorah's business; re-running this survey
afterwards is one command.

NUCLEI, AND WHERE THIS PARTS FROM ``final_stress``.  A syllable's nucleus is a point written
in the text, so the Hebrew's syllable count can be had without syllabifying it: a full vowel
or a xataf is a nucleus, a sheva is not, and a xolam male or shuruq written on a vav belongs
to the consonant before it.  ``accgram.final_stress`` counts NO nucleus for a furtive patax,
because it asks only whether the stress is final; this module counts one, because Phonetic
MAM does -- מזבח is ``miz.!bE.ax`` there, three syllables -- and a meteg on the guttural of
יָנ֥וּחַֽ is after the stress only under that convention.  ``final_stress``'s public
``ends_in_furtive_patax`` is where the other convention is stated, and the differential test
holds the two steady against each other.

THE TWO SIDES ARE CHECKED AGAINST EACH OTHER, per chanted word: the number of nuclei found in
the Hebrew must equal the number of non-sheva syllables in the ``jta``.  A chanted word where
they disagree is recorded as a MISMATCH and left out of every count, rather than being
classified against a syllable division the two sides do not share.

THE SILLUQ BOUNDARY IS TWO CONDITIONS, BOTH OF THEM, AND NO THIRD.  A U+05BD is the silluq
when it is in the stressed syllable of a chanted word that has sof pasuq; the sof pasuq is
what makes that chanted word the last of its CHANTED verse, so nothing here needs a separate
test of finality and nothing rests on an entry's position in a list.  The untracked census
script this module replaces (``doc/post-stress-meteg-census-2026-09-03.md`` is its report)
treated the last parsed entry of a NUMBERED verse as verse-final whether or not it had sof
pasuq, which is a silluq fallback rather than a test.

A NUMBERED VERSE AND A CHANTED VERSE ARE NOT THE SAME UNIT, and dual-cantillation numbered
verses are where they come apart -- which is exactly where that fallback could have gone wrong.
Genesis 35:22 has five duplicate chanted-word groups within its numbered verse. The risk here
comes from twelve numbered verses in the two Decalogues: each entry list ends with the two
strands' forms of one chanted word standing adjacent, one with silluq and sof pasuq, whose
chanted verse ends at the numbered verse's boundary, and one with an ordinary accent and no sof
pasuq, whose chanted verse runs on into the next numbered verse. Measured 2026-09-04 over all
twelve such numbered verses -- Exodus 20:2, 3, 4, 7, 8
and 9 and Deuteronomy 5:6, 7, 8, 11, 12 and 13 in MAM's versification -- the pattern is
exceptionless: the sof pasuq is on the second-to-last entry every time.  A rule that read
finality off the position would call that trailing mid-chanted-verse word verse-final, and any
U+05BD in its stressed syllable a silluq.  ``numbered_verses_whose_last_entry_lacks_sof_pasuq``
records all twelve, the run fails on a thirteenth that dual cantillation does not account for,
and no reading of them is needed anyway: none of the twelve has a meteg.

A METEG AND AN ACCENT ON ONE LETTER HAVE NO DEFINED ORDER (Ben, 2026-09-03), so the run fails
rather than guessing -- except where the accent sharing the letter marks no stress, since then
nothing about the stress turns on which mark came first.  The prepositives, the postpositives,
ole and geresh muqdam are written at a fixed edge of the chanted word rather than on its
stress, which is what ``final_stress.NOT_IMPOSITIVE`` says of the same set; such a meteg is
classified by its syllable like any other and tallied separately as an overlap.

Prose verses and poetic verses are routed by ``poetic_filter.should_keep_line``, so Job's
prose frame goes with the 21 books. For a dual-cantillation passage, this census selects the
cant-alef strand and counts the passage as though it were read once. A second scan over
cant-bet is retained in the JSON for the rendered appendix.

THE STRESS-LETTER ACCENT CHECK retains one result from the 2026-09-03 census table.  The
table read the accents on the initial Hebrew letter of the one ``jta`` syllable marked ``!``;
``stress_accent_classification`` implements that exact rule and establishes only that every
MAS has a conjunctive accent there.  The four ``misc-vayomer`` records have a narrow-sense
paseq after the chanted word, so that stroke leaves the underlying accent conjunctive.  In a
poetic verse, U+05A5 can be yored only in an oleh-we-yored chanted word.  The check refuses a
future U+05A5 case with ole, rather than silently calling it either merkha or yored.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from random import Random

from accgram import maqaf_nonfinal_accents as mna
from accgram import poetic_accent_names as pan
from accgram import poetic_filter
from accgram import poetic_scanner
from accgram import prose_scanner
from accgram import uni_to_marks
from accgram import chanted_word_accents as cwa
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.uni_to_marks import is_accent
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import provenance
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

METEG = hpo.MTGOSLQ
SOF_PASUQ = hpu.SOPA
MAQAF = hpu.MAQ
PASEQ = hpu.PASOLEG

SILLUQ_RULE = (
    "A U+05BD is the silluq when it is in the stressed syllable of a chanted word that"
    " has sof pasuq. Both conditions are required and there is no third: the sof pasuq"
    " is what makes the chanted word the last of its chanted verse, so nothing here rests on"
    " an entry's position in a list."
)

# Phonetic MAM spells MAM's gray maqaf as a tilde and its ordinary maqaf as U+05BE; both are
# atom boundaries inside one chanted word, and neither is a nucleus.
_BOUNDARIES = frozenset((MAQAF, hpu.NU_GMAQ))

# Phonetic MAM puts this token between the two chanted words at a narrow-sense paseq.  It is
# converted to MAM's U+05C0 only after the survey has located it structurally, never by treating
# the label as Hebrew text to display.
_PHONETIC_MAM_PASEQ = (
    "\N{HEBREW LETTER MEM}:\N{HEBREW LETTER PE}\N{HEBREW LETTER SAMEKH}"
    "\N{HEBREW LETTER QOF}"
)

_VAV = "\N{HEBREW LETTER VAV}"
_ALEF = "\N{HEBREW LETTER ALEF}"
_TAV = "\N{HEBREW LETTER TAV}"

# The three letters that can close a chanted word as a guttural, and the three a furtive patax
# is written on -- the same three.  ``final_stress._FURTIVE_HOSTS`` is the other copy; it is
# private, and this module's furtive rule is deliberately the opposite of that module's.
_GUTTURAL_HOSTS = frozenset(
    (
        "\N{HEBREW LETTER HET}",
        "\N{HEBREW LETTER AYIN}",
        "\N{HEBREW LETTER HE}",
    )
)

# The Type 2 page filters every following word into one of these five groups.  The initial
# letters are named exhaustively rather than putting unexpected initials in a catchall: a
# changed corpus must stop the survey until its new group has been considered.
TYPE_2_FOLLOWING_FILTER_GROUPS = ("bet", "guttural", "lamed", "mem", "resh")
_TYPE_2_FOLLOWING_FILTER_GROUP_BY_INITIAL = {
    hl.BET: "bet",
    hl.LAMED: "lamed",
    hl.ALEF: "guttural",
    hl.HE: "guttural",
    hl.XET: "guttural",
    hl.AYIN: "guttural",
    hl.MEM: "mem",
    hl.RESH: "resh",
}

_FULL_VOWELS = (
    hpo.XIRIQ,
    hpo.TSERE,
    hpo.SEGOL_V,
    hpo.PATAX,
    hpo.QAMATS,
    hpo.QAMATS_Q,
    hpo.XOLAM,
    hpo.XOLAM_XFV,
    hpo.QUBUTS,
)
_XATAFS = (hpo.XSEGOL, hpo.XPATAX, hpo.XQAMATS)
_NUCLEUS_POINTS = frozenset(_FULL_VOWELS + _XATAFS)

# Accents written at a fixed EDGE of the chanted word rather than on its stress.  The set
# ``final_stress.NOT_IMPOSITIVE`` names, plus ole, which is an Emet mark whose position says
# nothing about this chanted word's stress either.  A meteg sharing a letter with one of these
# is classified rather than refused: the order of the two marks decides nothing.
_NON_STRESS_ACCENTS = frozenset(
    (
        ha.TEL_G,
        ha.DEX,
        ha.YET,
        ha.SEG_A,
        ha.PASH,
        ha.TEL_Q,
        ha.Z_OR_TSOR,
        ha.OLE,
        ha.GER_M,
    )
)

# Every accent, named as the pages name it.  ``_accent_name`` raises on one that is not here,
# so a corpus that grows a new pair fails the build rather than printing a codepoint at a
# reader.  The romanizations are ``printed_decalogue_strands``' ROM_* spellings wherever it
# has one; the marks it has no constant for are spelled here in the same style.
_ACCENT_NAMES = {
    ha.MUN: "munaḥ",
    ha.MER: "merkha",
    ha.MAH: "mahapakh",
    ha.QOM: "qadma",
    ha.DAR: "darga",
    ha.TIP: "tipeḥa",
    ha.TEL_Q: "telisha qetanah",
    ha.TEL_G: "telisha gedolah",
    ha.ATN: "etnaḥta",
    ha.ATN_H: "atnaḥ hafukh",
    ha.YBY: "yeraḥ ben yomo",
    ha.ILU: "iluy",
    ha.OLE: "ole",
    ha.DEX: "deḥi",
    ha.GER_M: "geresh muqdam",
    ha.REV: "revia",
    ha.ZAQ_Q: "zaqef",
    ha.ZAQ_G: "zaqef gadol",
    ha.TEV: "tevir",
    ha.PASH: "pashta",
    ha.SEG_A: "segolta",
    ha.YET: "yetiv",
    ha.GER: "geresh",
    ha.GER_2: "gershayim",
    ha.PAZ: "pazer",
    ha.QAR: "qarney para",
    ha.SHA: "shalshelet",
    ha.MER_2: "merkha kefula",
    ha.Z_OR_TSOR: "tsinnor",
    ha.ZSH_OR_TSIT: "tsinnorit",
}

# The vowel a syllable's nucleus is written with, named for the page's tables.  Indexed
# strictly for the same reason ``_ACCENT_NAMES`` is: a point with no name here stops the run.
_VOWEL_NAMES = {
    hpo.XIRIQ: "ḥiriq",
    hpo.TSERE: "ṣere",
    hpo.SEGOL_V: "segol",
    hpo.PATAX: "pataḥ",
    hpo.QAMATS: "qamats",
    hpo.QAMATS_Q: "qamats qatan",
    hpo.XOLAM: "ḥolam",
    hpo.XOLAM_XFV: "ḥolam",
    hpo.QUBUTS: "qubuts",
    hpo.XSEGOL: "ḥataf segol",
    hpo.XPATAX: "ḥataf pataḥ",
    hpo.XQAMATS: "ḥataf qamats",
    hpo.DAGOMOSD: "shuruq",
}

# What separates one syllable of a ``jta`` form from the next: ``.`` within an atom and ``-``
# between the atoms of a maqaf compound.  The same split
# ``test_final_stress_vs_phonetic_mam`` makes, and for the same reason.
_SYLLABLE_BREAK = re.compile(r"[.\-]")

# Phonetic MAM's verse keys name the book too -- ``G1:1``, ``1S12:3`` -- and the book part can
# itself start with a digit, so the chapter and verse are taken off the END.
_VERSE_KEY = re.compile(r"^.+?(\d+):(\d+)$")

# A vocal sheva is a syllable in ``jta`` and no nucleus in the Hebrew, so the two
# sides are compared over the syllables that do NOT carry this marker.
_VOCAL_SHEVA = "^"

# ``jta``'s vowel letters, uppercase for the long vowels and lowercase for the short.  Only
# ONE question is asked of them: a syllable ending in a vowel letter is open and one ending
# in anything else is closed.  What the closing consonant IS cannot be read here -- ``kash``
# ends in the h of a shin and ``lakh`` in the h of a kaf -- so the guttural test below reads
# the Hebrew instead.
_JTA_VOWELS = frozenset("aeiouAEIOU860")

# A simple vocal sheva or xataf vowel at the opening of a chanted word belongs to the following
# segment as the chanted word's first syllable for Yeivin's open-syllable type.
_XATAF_JTA_VOWELS = frozenset("680")

SYSTEM_PROSE = "prose verses"
SYSTEM_POETIC = "poetic verses"

# The regular conjunctives in the two cantillation systems.  The exceptions that concern the
# stress-letter check are handled in ``stress_accent_classification``: narrow-sense paseq does
# not change the accent that precedes it, and poetic U+05A5 with ole requires an explicit
# oleh-we-yored analysis.
_STRESS_ACCENT_CONJUNCTIVES = {
    SYSTEM_PROSE: frozenset(
        (
            ha.MUN,
            ha.MAH,
            ha.MER,
            ha.DAR,
            ha.QOM,
            ha.TEL_Q,
            ha.YBY,
            ha.MER_2,
        )
    ),
    SYSTEM_POETIC: frozenset(
        (
            ha.MUN,
            ha.MER,
            ha.ILU,
            ha.TIP,
            ha.YBY,
            ha.MAH,
            ha.QOM,
            ha.SHA,
            ha.ATN_H,
        )
    ),
}

# The prose scanner exposes token names rather than raw marks.  This set identifies the
# disjunctive tokens among them; a following word can also have conjunctive or secondary tokens,
# so the fit-for-MAS screen asks whether at least one of its grammar tokens is disjunctive.
_PROSE_DISJUNCTIVE_TOKENS = frozenset(
    (
        "SILLUQ",
        "ATNAX",
        "SEGOLTA",
        "SHALSHELET",
        "METHIGAZAQEF",
        "ZAQEF",
        "ZAQEFGADOL",
        "REVIA",
        "TIPEXA",
        "ZARQA",
        "PASHTA",
        "YETIV",
        "TEVIR",
        "GERESH",
        "GERSHAYIM",
        "PAZER",
        "PAZERGADOL",
        "TELISHAGEDOLA",
        "LEGARMEH",
    )
)


def _has_a_disjunctive_accent(
    system: str, accent_grammar_tokens: tuple[str, ...]
) -> bool:
    """Whether the accent grammar gives a chanted word a disjunctive token."""
    disjunctives = (
        _PROSE_DISJUNCTIVE_TOKENS if system == SYSTEM_PROSE else pan.POETIC_DISJUNCTIVES
    )
    return bool(set(accent_grammar_tokens) & disjunctives)


# The three types the page attributes to Yeivin and Breuer, each keyed on a mechanical
# signature and never on a verse reference.  A post-stress meteg meeting none of them is
# recorded as unclassified rather than pushed into the nearest.
TYPE_GUTTURAL = "chanted word closed by a guttural"
TYPE_CLOSED_TSERE = "closed tsere-vowelled syllable"
TYPE_OPEN = "open final syllable"
TYPE_UNCLASSIFIED = "none of the three"

SUBTYPE_MISC_VAYOMER = "misc-vayomer"
SUBTYPE_MISC_ALMOST_TYPE_3 = "misc-almost-type-3"

_TYPES = (TYPE_CLOSED_TSERE, TYPE_GUTTURAL, TYPE_OPEN, TYPE_UNCLASSIFIED)
_SUBTYPES = (
    SUBTYPE_MISC_VAYOMER,
    SUBTYPE_MISC_ALMOST_TYPE_3,
)

_VAYOMER_CONSONANTS = (
    "\N{HEBREW LETTER VAV}"
    "\N{HEBREW LETTER YOD}"
    "\N{HEBREW LETTER ALEF}"
    "\N{HEBREW LETTER MEM}"
    "\N{HEBREW LETTER RESH}"
)

# The 2026-09-03 census, whose report is ``doc/post-stress-meteg-census-2026-09-03.md``.  Its
# script is untracked and defective at the silluq boundary, so these are a comparison baseline
# and not a second measurement: ``legacy_baseline`` below reports every difference from them.
_LEGACY_BASELINE = {
    SYSTEM_PROSE: {
        "chanted words checked": 233715,
        "meteg before the stressed syllable": 13131,
        "meteg after the stressed syllable": 177,
        "silluq": 18779,
        "meteg sharing a letter with a non-stress-marking accent": 27,
    },
    SYSTEM_POETIC: {
        "chanted words checked": 29605,
        "meteg before the stressed syllable": 1814,
        "meteg after the stressed syllable": 54,
        "silluq": 4486,
        "meteg sharing a letter with a non-stress-marking accent": 119,
    },
}

_COUNT_CATEGORIES = (
    "chanted words checked",
    "meteg before the stressed syllable",
    "meteg in the stressed syllable, no sof pasuq",
    "meteg after the stressed syllable",
    "silluq",
    "meteg sharing a letter with a non-stress-marking accent",
)

_DUAL_CANTILLATION_COMPARISON_CATEGORIES = (
    "chanted words checked",
    "meteg before the stressed syllable",
    "meteg after the stressed syllable",
)


class SurveyProblem(Exception):
    """A survey that cannot honestly finish: bad input, or a mark it must not classify."""


def _is_base_letter(char: str) -> bool:
    return _ALEF <= char <= _TAV


def _letters(word: str) -> list[tuple[str, str, bool]]:
    """``[base letter, the marks on it, whether it ends its atom]``, one per base letter.

    Atom boundaries are consumed rather than kept, the way ``final_stress._letters`` consumes
    them: what a later rule needs of a boundary is the atom-final flag on the letter before
    it, since a furtive patax can close a non-final atom as readily as a whole compound.
    """
    out: list[list] = []
    for char in word:
        if char in _BOUNDARIES:
            if out:
                out[-1][2] = True
        elif char == SOF_PASUQ:
            continue
        elif _is_base_letter(char):
            out.append([char, "", False])
        elif out:
            out[-1][1] += char
        else:
            raise SurveyProblem(f"a mark before any letter: {word!r}")
    if out:
        out[-1][2] = True
    return [(letter, marks, atom_final) for letter, marks, atom_final in out]


def type_2_following_filter_group(following_word: str) -> str:
    """The Type 2 filter group for a following MAM chanted word.

    This intentionally raises for an unexpected initial.  A catchall filter would let the
    page continue to claim complete coverage while concealing a corpus change that needs a
    human choice about the filters.
    """
    letters = _letters(following_word)
    assert (
        letters
    ), f"no Hebrew letter in following MAM chanted word: {following_word!r}"
    initial = letters[0][0]
    assert initial in _TYPE_2_FOLLOWING_FILTER_GROUP_BY_INITIAL, (
        "Type 2 following initial is outside the page filters: "
        f"{initial!r} in {following_word!r}"
    )
    return _TYPE_2_FOLLOWING_FILTER_GROUP_BY_INITIAL[initial]


def _assert_type_2_following_filter_coverage(records: list[dict]) -> None:
    """Require the Type 2 filters to classify every Type 2 record this run finds."""
    type_2_records = [
        record for record in records if record["structural_type"] == TYPE_GUTTURAL
    ]
    group_count = Counter()
    for record in type_2_records:
        following = record["following_mam_form"]
        assert following is not None, f"{record['bcv']}: no following MAM chanted word"
        group_count[type_2_following_filter_group(following)] += 1
    assert sum(group_count.values()) == len(type_2_records)
    assert set(group_count) <= set(TYPE_2_FOLLOWING_FILTER_GROUPS)


def _has_a_vowel(marks: str) -> bool:
    return any(mark in _NUCLEUS_POINTS for mark in marks)


def _nuclei(letters: list[tuple[str, str, bool]]) -> list[tuple[int, str]]:
    """``(index of the letter carrying each nucleus, the point that is the nucleus)``.

    A FURTIVE PATAX COUNTS, unlike in ``final_stress``: Phonetic MAM has it as a syllable of
    its own, the two sides' syllable counts are compared here, so it has to count on this
    side too.  A xolam male and a shuruq are written on a vav that is a mater, so each belongs
    to the consonant before it -- unless that consonant has a vowel of its own, where the vav
    is consonantal and the dagesh doubles it.
    """
    out: list[tuple[int, str]] = []
    for index, (letter, marks, _atom_final) in enumerate(letters):
        vowels = [mark for mark in marks if mark in _NUCLEUS_POINTS]
        atom_initial = index == 0 or letters[index - 1][2]
        previous_vowelled = (not atom_initial) and _has_a_vowel(letters[index - 1][1])
        if not vowels:
            if letter == _VAV and hpo.DAGOMOSD in marks and not previous_vowelled:
                out.append((index if atom_initial else index - 1, hpo.DAGOMOSD))
            continue
        if (
            letter == _VAV
            and vowels == [hpo.XOLAM]
            and not previous_vowelled
            and not atom_initial
            and hpo.DAGOMOSD not in marks
        ):
            out.append((index - 1, hpo.XOLAM))
            continue
        out.append((index, vowels[0]))
    return out


def _jta_syllables(jta: str) -> tuple[list[str], int]:
    """The ``jta``'s syllables that have a nucleus, and which of them is stressed.

    Raises rather than guessing on a form with no stress marker or with more than one, on a
    stressed syllable that is a vocal sheva, and on a syllable with no vowel letter in it --
    each of which would leave the comparison below comparing something other than syllables
    with nuclei.
    """
    syllables = _SYLLABLE_BREAK.split(jta)
    stressed = [i for i, one in enumerate(syllables) if "!" in one]
    if len(stressed) != 1:
        raise SurveyProblem(f"jta without exactly one stress marker: {jta!r}")
    kept = [i for i, one in enumerate(syllables) if _VOCAL_SHEVA not in one]
    if stressed[0] not in kept:
        raise SurveyProblem(f"jta whose stressed syllable is a vocal sheva: {jta!r}")
    out = [syllables[i] for i in kept]
    for syllable in out:
        if not set(syllable) & _JTA_VOWELS:
            raise SurveyProblem(f"a jta syllable with no vowel letter: {jta!r}")
    return out, kept.index(stressed[0])


def _first_syllable_is_stressed(jta: str) -> bool:
    """Whether a following chanted word meets Yeivin's type-1 stress condition.

    An opening simple vocal sheva or xataf vowel belongs to the following segment as the first
    syllable for this condition. The stress is therefore initial when it falls on the first
    segment after all such opening segments. The normal syllable check still runs first: this
    test adds a source-specific reading of an already-valid ``jta`` form; it does not loosen the
    survey's validation.
    """
    _jta_syllables(jta)
    syllables = _SYLLABLE_BREAK.split(jta)
    stressed = [i for i, one in enumerate(syllables) if "!" in one]
    assert len(stressed) == 1, jta
    first_syllable_stress_segment = 0
    while first_syllable_stress_segment < len(syllables) and (
        _VOCAL_SHEVA in syllables[first_syllable_stress_segment]
        or set(syllables[first_syllable_stress_segment]) & _XATAF_JTA_VOWELS
    ):
        first_syllable_stress_segment += 1
    return stressed[0] == first_syllable_stress_segment


def _syllable_is_open(syllable: str) -> bool:
    return syllable[-1] in _JTA_VOWELS


def _has_final_tsere_syllable_closed_by_guttural(parsed: dict) -> bool:
    """Whether a chanted word could meet both the type-2 and type-3 conditions."""
    return (
        not _syllable_is_open(parsed["syllables"][-1])
        and parsed["nuclei"][-1][1] == hpo.TSERE
        and parsed["letters"][-1][0] in _GUTTURAL_HOSTS
    )


def _chanted_word_is_closed_by_a_guttural(parsed: dict) -> bool:
    """Whether the final syllable is phonetically closed by a consonantal guttural.

    A final mater he leaves a final syllable open; a final guttural after furtive patax closes
    that syllable.  The syllable boundary, rather than merely the final letter, makes that
    distinction mechanical.
    """
    return (
        not _syllable_is_open(parsed["syllables"][-1])
        and parsed["letters"][-1][0] in _GUTTURAL_HOSTS
    )


def _accent_name(accent: str) -> str:
    name = _ACCENT_NAMES.get(accent)
    if name is None:
        raise SurveyProblem(f"no name for accent U+{ord(accent):04X}")
    return name


def _vowel_name(point: str) -> str:
    name = _VOWEL_NAMES.get(point)
    if name is None:
        raise SurveyProblem(f"no name for vowel U+{ord(point):04X}")
    return name


def _structural_type(
    *,
    chanted_word_is_closed_by_a_guttural: bool,
    is_last_syllable: bool,
    is_open: bool,
    vowel: str,
) -> tuple[str, str | None]:
    """Which source-anchored type and subtype a post-stress meteg's syllable meets.

    Mechanical, off the syllable Phonetic MAM divided and the letters and points MAM has:

    * an open final syllable is ITM §332 and CoS Ch. 8 type (j), the qumi rule;
    * a chanted word phonetically closed by a guttural is ITM §354 and CoS Ch. 8 type (b);
      a final mater he is not a guttural closing for this purpose; and
    * a closed syllable whose nucleus is a ṣere is ITM §338. This is the narrower condition this
      survey uses for type 3; CoS Ch. 8 type (a) is wider, covering a long vowel in a closed
      syllable.

    Anything else -- a closed syllable with some other vowel, the segol of vayomer above all --
    is left unclassified and stays visible as itself.  A final closed ḥolam syllable is the
    ``misc-almost-type-3`` subtype: it fits CoS's wider long-vowel condition but not ITM's ṣere
    type.
    """
    if is_open and is_last_syllable:
        return TYPE_OPEN, None
    if chanted_word_is_closed_by_a_guttural:
        return TYPE_GUTTURAL, None
    if not is_open and vowel == hpo.TSERE:
        return TYPE_CLOSED_TSERE, None
    if is_last_syllable and vowel in (hpo.XOLAM, hpo.XOLAM_XFV):
        return TYPE_UNCLASSIFIED, SUBTYPE_MISC_ALMOST_TYPE_3
    return TYPE_UNCLASSIFIED, None


def _misc_subtype(
    *, structural_type: str, chanted_word: str, intervening_punctuation: tuple[str, ...]
) -> str | None:
    """A named subdivision of misc where the form and punctuation make one useful set."""
    if (
        structural_type == TYPE_UNCLASSIFIED
        and "".join(letter for letter, _marks, _atom_final in _letters(chanted_word))
        == _VAYOMER_CONSONANTS
        and intervening_punctuation == (PASEQ,)
    ):
        return SUBTYPE_MISC_VAYOMER
    return None


def _chanted_words(node: object, out: list[dict]) -> None:
    """Every chanted-word entry of one verse, the ``cb`` structures flattened.

    A ``cb`` is Phonetic MAM's bracket for something other than a plain run of chanted words
    -- a paseq, a setuma or petuxa, a qamats note, a dual-cantillation span. The census projects
    each dual span onto one strand before calling this walk. The same walk
    ``test_final_stress_vs_phonetic_mam._chanted_words`` makes.
    """
    if isinstance(node, dict):
        out.append(node)
    elif isinstance(node, list):
        for sub in node[1:] if node and node[0] == "cb" else node:
            _chanted_words(sub, out)


def _chanted_word_events(node: object, out: list[object]) -> None:
    """The same chanted-word sequence, retaining material between its entries.

    ``_chanted_words`` is the broad census walk, intentionally omitting everything other than
    entries. The individual-case page needs narrower context for a post-stress record: an
    intervening PASEQ is part of the reason its ``vayomer`` cases are distinct. Retaining all
    other material here makes an unexpected future gap a survey failure rather than an omission.
    """
    if isinstance(node, dict):
        out.append(node)
    elif isinstance(node, list):
        for sub in node[1:] if node and node[0] == "cb" else node:
            _chanted_word_events(sub, out)
    else:
        out.append(node)


def _accent_grammar_tokens_by_entry(
    *,
    bb: str,
    chnu: int,
    vrnu: int,
    system: str,
    events: list[object],
    has_legarmeh: prose_scanner.HasLegarmeh,
) -> dict[int, tuple[str, ...]]:
    """The complete accent-grammar token sequence of every chanted-word entry.

    The candidate survey needs Phonetic MAM's independently supplied primary-stress position,
    not a count of the raw marks on its stress letter.  The prose and poetic scanners instead
    resolve helpers, fixed-edge accents, silluq/meteg context, and genuine secondary accents
    into grammar tokens.  A candidate still is not discarded because its chanted word has zero
    or several tokens: the three MAS types are structural conditions on the syllable after the
    one ``jta`` stress.
    """
    entries: list[dict] = []
    fragments: list[cwa.Frag] = []
    for event in events:
        if isinstance(event, dict) and event.get("fva"):
            word = event["fva"].split(" ")[0]
            entries.append(event)
            fragments.append(cwa.Frag(word, uni_to_marks.word_to_marks(word), True))
        elif event == _PHONETIC_MAM_PASEQ:
            assert fragments, (bb, chnu, vrnu)
            prior = fragments[-1]
            fragments[-1] = cwa.Frag(prior.text, prior.marks + PASEQ, True)
    body, units = cwa._verse_units(fragments)
    assert len(entries) == len(units), (bb, chnu, vrnu, len(entries), len(units))
    tokens = (
        prose_scanner.scan_accents(body, bb, chnu, vrnu, has_legarmeh)
        if system == SYSTEM_PROSE
        else poetic_scanner.scan_accent_tokens(body)
    )
    by_chanted_word = cwa._by_chanted_word(units, tokens)
    assert len(by_chanted_word) == len(entries), (bb, chnu, vrnu)
    return {
        id(entry): tuple(token.type for token in word_tokens)
        for entry, (_unit, word_tokens, _unfolded) in zip(
            entries, by_chanted_word, strict=True
        )
    }


def _intervening_punctuation(
    *, bcv: str, chanted_word: str, material: tuple[object, ...]
) -> tuple[str, ...]:
    """The punctuation between one post-stress record and its following chanted word.

    The current corpus has only Phonetic MAM's narrow-sense paseq token here. A different
    token is a new display case to classify, not something the page may silently drop.
    """
    if not material:
        return ()
    if all(one == _PHONETIC_MAM_PASEQ for one in material):
        return (PASEQ,) * len(material)
    raise SurveyProblem(
        f"{bcv} {chanted_word!r}: intervening material before the following chanted word"
        f" is not a PASEQ: {material!r}"
    )


_CB_QAMATS_MARKER = "cb-qamats"
_FIT_FOR_MAS_NON_PUNCTUATION_MATERIAL = frozenset(
    (None, _CB_QAMATS_MARKER, "סס", "פפ", "ססס", "פפפ")
)


def _fit_for_mas_intervening_punctuation(
    *, bcv: str, chanted_word: str, material: tuple[object, ...]
) -> tuple[str, ...]:
    """The displayed candidate's punctuation, omitting only known non-text metadata."""
    if not material or all(one == _PHONETIC_MAM_PASEQ for one in material):
        return _intervening_punctuation(
            bcv=bcv, chanted_word=chanted_word, material=material
        )
    if all(one in _FIT_FOR_MAS_NON_PUNCTUATION_MATERIAL for one in material):
        return ()
    raise SurveyProblem(
        f"{bcv} {chanted_word!r}: unclassified intervening material before a"
        f" Fit-for-MAS candidate's following chanted word: {material!r}"
    )


_DUALCANT_MARKER = "cb-dualcant"
CANT_ALEF = "cant-alef"
CANT_BET = "cant-bet"
_CANTILLATION_BRANCH_INDEX = {CANT_ALEF: 0, CANT_BET: 1}


def _has_dual_cantillation(node: object) -> bool:
    """Whether the numbered verse has Phonetic MAM's dual-cantillation bracket.

    Structural rather than a list of references: both strands' chanted words reach one entry
    list. The two Decalogues have most of the dual-cantillation numbered verses, and Genesis
    35:22 has the other one. A last entry need not be the one with sof pasuq -- one strand's
    chanted verse can end at the numbered verse's boundary and the other can run on past it.
    """
    if isinstance(node, str):
        return node == _DUALCANT_MARKER
    if isinstance(node, list):
        return any(_has_dual_cantillation(sub) for sub in node)
    if isinstance(node, dict):
        return any(_has_dual_cantillation(value) for value in node.values())
    return False


def _select_cantillation_strand(node: object, cantillation: str) -> object:
    """Replace each dual span with its cant-alef or cant-bet cantillation strand.

    Phonetic MAM's source writes the alef branch before the bet branch when it emits a
    ``cb-dualcant`` structure. The explicit names here keep that ordering from becoming an
    anonymous positional convention in this census.
    """
    branch_index = _CANTILLATION_BRANCH_INDEX[cantillation]
    if not isinstance(node, list):
        return node
    if node and node[0] == "cb":
        out = ["cb"]
        for payload in node[1:]:
            if (
                isinstance(payload, list)
                and payload
                and payload[0] == [_DUALCANT_MARKER]
            ):
                branches = payload[1:]
                assert len(branches) == 2, len(branches)
                out.append(
                    _select_cantillation_strand(branches[branch_index], cantillation)
                )
            else:
                out.append(_select_cantillation_strand(payload, cantillation))
        return out
    return [_select_cantillation_strand(one, cantillation) for one in node]


def _dual_cantillation_groups(node: object) -> list[list[list[dict]]]:
    """The two branches of each dual-cantillation group in a numbered verse."""
    out = []
    if not isinstance(node, list):
        return out
    if node and node[0] == "cb":
        for payload in node[1:]:
            if (
                isinstance(payload, list)
                and payload
                and payload[0] == [_DUALCANT_MARKER]
            ):
                branches = []
                for branch in payload[1:]:
                    entries: list[dict] = []
                    _chanted_words(branch, entries)
                    branches.append(entries)
                out.append(branches)
            else:
                out.extend(_dual_cantillation_groups(payload))
    else:
        for item in node:
            out.extend(_dual_cantillation_groups(item))
    return out


def _dual_template_entry_ids(verse: object, cantillation: str) -> set[int]:
    """The selected branch's entries that sit inside dual-cantillation templates.

    Entry identity, rather than a spelling key, keeps two equal-looking chanted words distinct
    when a numbered verse repeats them.  The selected branch remains made of the source
    dictionaries, so its entries have these same identities after
    ``_select_cantillation_strand`` projects the whole numbered verse.
    """
    assert cantillation in _CANTILLATION_BRANCH_INDEX, cantillation
    branch_index = _CANTILLATION_BRANCH_INDEX[cantillation]
    template_entries = [
        entry
        for group in _dual_cantillation_groups(verse)
        for entry in group[branch_index]
    ]
    assert template_entries, "a dual-cantillation verse has no template entries"
    return {id(entry) for entry in template_entries}


def _dual_cantillation_facts(verse: object) -> dict:
    """Counts and one source-derived duplicate for a dual-cantillation numbered verse."""
    groups = _dual_cantillation_groups(verse)
    same_groups = []
    for group in groups:
        assert len(group) == 2, len(group)
        first = tuple(_join_key(one["fva"].split(" ")[0]) for one in group[0])
        second = tuple(_join_key(one["fva"].split(" ")[0]) for one in group[1])
        if first == second:
            same_groups.append(group)
    assert (
        same_groups
    ), "a dual-cantillation verse has no repeated chanted-word sequence"
    first_group = same_groups[0]
    return {
        "dual_group_count": len(groups),
        "same_chanted_word_group_count": len(same_groups),
        "first_same_chanted_word_group": [
            [one["fva"].split(" ")[0] for one in branch] for branch in first_group
        ],
    }


def _bb_of_stem() -> dict[str, str]:
    """Phonetic MAM's per-book filename stem -> this repo's two-character book code."""
    return {
        tbn.ordered_short_dash_full_39(wlc_bb_to_bk39id(bb)): bb
        for bb in wlc_bb_codes()
    }


def _bare(word: str) -> str:
    """The chanted word in letters and accents alone, its maqafs put back.

    ``accents_and_letters`` drops the maqaf along with the vowels, so a compound is reduced
    atom by atom and rejoined, as ``chanted_word_accents._display`` does it.  Phonetic MAM
    spells MAM's gray maqaf as a tilde, restored here as the maqaf it stands for.

    NOT what the page shows, and it cannot be: ``accents_and_letters`` drops U+05BD with the
    vowels, and U+05BD is this survey's whole subject.  The page shows ``mam_form``, MAM's
    fully pointed text; this reduction is kept because a bare skeleton is what a reader wants
    beside it when the question is which accent the chanted word has.
    """
    atoms = re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    return MAQAF.join(accents_and_letters(atom) for atom in atoms)


# What a join key drops, so that a Phonetic MAM chanted word can be matched to the MAM-simple
# one it stands for: the accents, the masora circle and the puncta Phonetic MAM adds to mark
# a sheva or a dagesh it has resolved, meteg, rafe, the punctuation that can sit inside a
# chanted word, and the two invisibles.  What is left is letters and points -- which is what
# the two sides have to agree on, the marks this survey is about being exactly what it must
# not match on.  The same set ``test_final_stress_vs_phonetic_mam._NOT_IN_THE_JOIN_KEY``
# drops, and written as numeric escapes for the same two reasons: a character class wants
# range endpoints, and a bare combining mark in a literal is unreadable.
_NOT_IN_THE_JOIN_KEY = re.compile(
    "[\u0591-\u05af\u05bd\u05bf\u05c0\u05c3-\u05c5\u034f\ufb1e]"
)


def _join_key(word: str) -> str:
    """``word`` reduced to what both texts must agree on: letters, points, and the maqafs.

    Phonetic MAM's tilde for MAM's gray maqaf is folded onto the maqaf it stands for, so a
    compound joined by one matches the compound MAM has.
    """
    return _NOT_IN_THE_JOIN_KEY.sub("", word).replace(hpu.NU_GMAQ, MAQAF)


def _parse(word: str, jta: str) -> dict:
    """Everything the classification of one chanted word's U+05BDs rests on.

    Raises ``SurveyProblem`` where the two sides' syllable counts disagree, which is the check
    that makes reading a syllable off the ``jta`` and a nucleus off the Hebrew safe.
    """
    letters = _letters(word)
    nuclei = _nuclei(letters)
    syllables, stressed = _jta_syllables(jta)
    if len(nuclei) != len(syllables):
        raise SurveyProblem(
            f"{len(syllables)} jta syllables against {len(nuclei)} Hebrew nuclei"
        )
    return {
        "letters": letters,
        "nuclei": nuclei,
        "syllables": syllables,
        "stressed": stressed,
        "has_sof_pasuq": SOF_PASUQ in word,
    }


def _stress_letter_accent(record: dict) -> str:
    """The one accent on the legacy table's exact stress letter for ``record``.

    The stress letter is the initial Hebrew letter of the nucleus whose Phonetic MAM ``jta``
    syllable has ``!``.  The 2026-09-03 census table selected its accent with this rule; the
    record's meteg can occur later in the same chanted word and does not participate in the
    selection.
    """
    parsed = _parse(record["chanted_word"], record["jta"])
    stress_letter_index, _stress_vowel = parsed["nuclei"][parsed["stressed"]]
    stress_letter_marks = parsed["letters"][stress_letter_index][1]
    accents = [mark for mark in stress_letter_marks if is_accent(mark)]
    if len(accents) != 1:
        raise SurveyProblem(
            f"{record['bcv']}: the stress letter has {len(accents)} accents, not one"
        )
    return accents[0]


def stress_accent_classification(post_stress: list[dict]) -> dict:
    """The legacy table's weak, reproducible conclusion about MAS stress accents.

    The classification deliberately stops at conjunctive versus disjunctive.  A raw U+05C0
    cannot distinguish a narrow-sense paseq from legarmeh, so only the structurally identified
    ``misc-vayomer`` records are allowed to carry it.  A poetic U+05A5 with ole is likewise
    refused as an oleh-we-yored question instead of being guessed to be normal merkha.
    """
    for record in post_stress:
        punctuation = record.get("intervening_punctuation", ())
        if punctuation:
            if not (
                record["subtype"] == SUBTYPE_MISC_VAYOMER and punctuation == (PASEQ,)
            ):
                raise SurveyProblem(
                    f"{record['bcv']}: the stress-accent check cannot classify its U+05C0"
                )
        elif record["subtype"] == SUBTYPE_MISC_VAYOMER:
            raise SurveyProblem(
                f"{record['bcv']}: misc-vayomer lacks its narrow-sense paseq"
            )

        accent = _stress_letter_accent(record)
        if (
            record["system"] == SYSTEM_POETIC
            and accent == ha.MER
            and ha.OLE in record["chanted_word"]
        ):
            raise SurveyProblem(
                f"{record['bcv']}: poetic U+05A5 with ole needs an oleh-we-yored analysis"
            )
        if accent not in _STRESS_ACCENT_CONJUNCTIVES[record["system"]]:
            raise SurveyProblem(
                f"{record['bcv']}: stress-letter accent is not a regular conjunctive"
            )

    return {
        "exact_rule": (
            "Read the accents on the initial Hebrew letter of the one jta syllable marked !, "
            "the rule used by the 2026-09-03 census table."
        ),
        "conclusion": "Every MAS has a conjunctive accent on that stress letter.",
        "counts": {"conjunctive": len(post_stress), "disjunctive": 0},
    }


def _syllable_of(nuclei: list[tuple[int, str]], letter_index: int) -> int:
    """Which syllable a mark on ``letter_index`` is in: the last nucleus at or before it."""
    return max(
        (i for i, (onset, _point) in enumerate(nuclei) if onset <= letter_index),
        default=0,
    )


def _record(
    *,
    bcv: str,
    system: str,
    word: str,
    jta: str,
    parsed: dict,
    syllable_index: int,
    letter_index: int,
    accents_here: list[str],
    before_qere: str | None,
    following_chanted_word: str | None,
    following_jta: str | None,
    intervening_punctuation: tuple[str, ...],
) -> dict:
    """One classified U+05BD, with everything the page's tables and counts derive from."""
    nuclei = parsed["nuclei"]
    letters = parsed["letters"]
    syllables = parsed["syllables"]
    syllable = syllables[syllable_index]
    is_last_syllable = syllable_index == len(syllables) - 1
    is_open = _syllable_is_open(syllable)
    vowel = nuclei[syllable_index][1]
    chanted_word_is_closed_by_a_guttural = _chanted_word_is_closed_by_a_guttural(parsed)
    structural_type, subtype = _structural_type(
        chanted_word_is_closed_by_a_guttural=chanted_word_is_closed_by_a_guttural,
        is_last_syllable=is_last_syllable,
        is_open=is_open,
        vowel=vowel,
    )
    if subtype is None:
        subtype = _misc_subtype(
            structural_type=structural_type,
            chanted_word=word,
            intervening_punctuation=intervening_punctuation,
        )
    record = {
        "bcv": bcv,
        "system": system,
        "chanted_word": word,
        "following_chanted_word": following_chanted_word,
        "snapshot_before_qere": before_qere,
        "accents_and_letters": _bare(word),
        "jta": jta,
        "syllables_after_the_stress": syllable_index - parsed["stressed"],
        "syllable": syllable,
        "syllable_is_open": is_open,
        "vowel": _vowel_name(vowel),
        "is_the_last_syllable": is_last_syllable,
        "chanted_word_is_closed_by_a_guttural": (chanted_word_is_closed_by_a_guttural),
        "following_chanted_word_is_initially_stressed": (
            _first_syllable_is_stressed(following_jta)
            if following_jta is not None
            else None
        ),
        "has_sof_pasuq": parsed["has_sof_pasuq"],
        "shares_its_letter_with": [_accent_name(one) for one in accents_here],
        "structural_type": structural_type,
        "subtype": subtype,
        "atom": 1 + sum(1 for one in letters[:letter_index] if one[2]),
    }
    if intervening_punctuation:
        record["intervening_punctuation"] = intervening_punctuation
    return record


def _classify_one_word(
    *,
    bcv: str,
    system: str,
    word: str,
    jta: str,
    parsed: dict,
    found: dict,
    before_qere: str | None,
    following_chanted_word: str | None,
    following_jta: str | None,
    intervening_material: tuple[object, ...],
) -> None:
    """Classify every U+05BD of one chanted word, filling the tallies and the lists."""
    counts = found["counts"]
    stressed = parsed["stressed"]
    for letter_index, (_letter, marks, _atom_final) in enumerate(parsed["letters"]):
        if METEG not in marks:
            continue
        syllable_index = _syllable_of(parsed["nuclei"], letter_index)
        accents_here = [mark for mark in marks if is_accent(mark)]
        if syllable_index == stressed and parsed["has_sof_pasuq"]:
            counts[(system, "silluq")] += 1
            continue
        if accents_here and (
            syllable_index == stressed
            or not all(one in _NON_STRESS_ACCENTS for one in accents_here)
        ):
            found["same_letter_failures"].append(
                {
                    "bcv": bcv,
                    "chanted_word": word,
                    "jta": jta,
                    "accents_on_that_letter": [_accent_name(a) for a in accents_here],
                    "where": (
                        "in the stressed syllable"
                        if syllable_index == stressed
                        else "outside the stressed syllable"
                    ),
                }
            )
            continue
        record = _record(
            bcv=bcv,
            system=system,
            word=word,
            jta=jta,
            parsed=parsed,
            syllable_index=syllable_index,
            letter_index=letter_index,
            accents_here=accents_here,
            before_qere=before_qere,
            following_chanted_word=following_chanted_word,
            following_jta=following_jta,
            intervening_punctuation=(
                _intervening_punctuation(
                    bcv=bcv,
                    chanted_word=word,
                    material=intervening_material,
                )
                if syllable_index > stressed
                else ()
            ),
        )
        if accents_here:
            key = "meteg sharing a letter with a non-stress-marking accent"
            counts[(system, key)] += 1
            found["overlaps"].append(record)
        if syllable_index < stressed:
            counts[(system, "meteg before the stressed syllable")] += 1
            found["pre_stress"].append(record)
        elif syllable_index == stressed:
            counts[(system, "meteg in the stressed syllable, no sof pasuq")] += 1
            found["in_stressed"].append(record)
        else:
            counts[(system, "meteg after the stressed syllable")] += 1
            found["post_stress"].append(record)


def _fit_for_mas_candidate(
    *,
    bcv: str,
    system: str,
    word: str,
    jta: str,
    parsed: dict,
    before_qere: str | None,
    following_chanted_word: str | None,
    following_jta: str | None,
    following_accent_grammar_tokens: tuple[str, ...],
    accent_grammar_tokens: tuple[str, ...],
    intervening_punctuation: tuple[str, ...],
) -> dict | None:
    """One potential MAS syllable, or ``None`` when no syllable follows the stress.

    Phonetic MAM's ``jta`` supplies the chanted word's one primary-stress position; a raw
    Unicode accent count cannot supply that information.  The potential syllable is directly
    after a nonfinal stress.  The table calls it fit for MAS only when the following chanted word
    has initial stress and the accent grammar gives that following chanted word a disjunctive
    token, in addition to meeting one or more of the three source-derived structural types.
    """
    stressed = parsed["stressed"]
    if stressed == len(parsed["syllables"]) - 1:
        return None
    potential_syllable = stressed + 1
    is_open = _syllable_is_open(parsed["syllables"][potential_syllable])
    vowel = parsed["nuclei"][potential_syllable][1]
    types = []
    if is_open and potential_syllable == len(parsed["syllables"]) - 1:
        types.append(TYPE_OPEN)
    if _chanted_word_is_closed_by_a_guttural(parsed):
        types.append(TYPE_GUTTURAL)
    if not is_open and vowel == hpo.TSERE:
        types.append(TYPE_CLOSED_TSERE)
    has_u05bd = any(
        METEG in marks
        for letter_index, (_letter, marks, _atom_final) in enumerate(parsed["letters"])
        if _syllable_of(parsed["nuclei"], letter_index) == potential_syllable
    )
    candidate = {
        "bcv": bcv,
        "system": system,
        "chanted_word": word,
        "jta": jta,
        "snapshot_before_qere": before_qere,
        "following_chanted_word": following_chanted_word,
        "intervening_punctuation": intervening_punctuation,
        "structural_types": types,
        "has_u05bd": has_u05bd,
        "following_chanted_word_is_initially_stressed": (
            _first_syllable_is_stressed(following_jta)
            if following_jta is not None
            else False
        ),
        "following_chanted_word_has_disjunctive_accent": _has_a_disjunctive_accent(
            system, following_accent_grammar_tokens
        ),
        "accent_grammar_token_count": len(accent_grammar_tokens),
    }
    return candidate


_TYPE_1_PROSE_LACKS_MAS_SAMPLE_SIZE = 100
_TYPE_1_POETIC_LACKS_MAS_SAMPLE_SIZE = 10
_LACKS_MAS_SAMPLE_SEED = 20260906


def _has_following_word_conditions_for_mas(candidate: dict) -> bool:
    """Whether the following chanted word has the two Fit-for-MAS properties."""
    return (
        candidate["following_chanted_word_is_initially_stressed"]
        and candidate["following_chanted_word_has_disjunctive_accent"]
    )


def _is_fit_for_mas(candidate: dict) -> bool:
    """Whether one candidate meets the following-word conditions and a MAS type."""
    return _has_following_word_conditions_for_mas(candidate) and bool(
        candidate["structural_types"]
    )


def _sample_in_corpus_order(
    candidates: list[dict], count: int, random: Random
) -> list[dict]:
    """A fixed random sample, restored to the corpus order for the rendered table."""
    assert len(candidates) >= count, (len(candidates), count)
    return [
        candidates[index]
        for index in sorted(random.sample(range(len(candidates)), count))
    ]


def _fit_for_mas_record(candidate: dict) -> dict:
    """The complete public-data record for one chanted-word pair fit for MAS."""
    assert _is_fit_for_mas(candidate), candidate
    return {
        "bcv": candidate["bcv"],
        "system": candidate["system"],
        "chanted_word": candidate["chanted_word"],
        "jta": candidate["jta"],
        "following_chanted_word": candidate["following_chanted_word"],
        "intervening_punctuation": candidate["intervening_punctuation"],
        "types": candidate["structural_types"],
        "has_mas": candidate["has_mas"],
        "following_chanted_word_is_initially_stressed": candidate[
            "following_chanted_word_is_initially_stressed"
        ],
        "following_chanted_word_has_disjunctive_accent": candidate[
            "following_chanted_word_has_disjunctive_accent"
        ],
    }


def _lacks_mas_case_lists(records: list[dict]) -> dict:
    """The all-type-2 and selected type-1 tables extracted from complete Fit-for-MAS data."""

    def lacking(kind: str, system: str | None = None) -> list[dict]:
        return [
            record
            for record in records
            if (
                kind in record["types"]
                and not record["has_mas"]
                and (system is None or record["system"] == system)
            )
        ]

    random = Random(_LACKS_MAS_SAMPLE_SEED)
    return {
        "type_2_all": lacking(TYPE_GUTTURAL),
        "type_1_random_sample": {
            SYSTEM_PROSE: _sample_in_corpus_order(
                lacking(TYPE_OPEN, SYSTEM_PROSE),
                _TYPE_1_PROSE_LACKS_MAS_SAMPLE_SIZE,
                random,
            ),
            SYSTEM_POETIC: _sample_in_corpus_order(
                lacking(TYPE_OPEN, SYSTEM_POETIC),
                _TYPE_1_POETIC_LACKS_MAS_SAMPLE_SIZE,
                random,
            ),
        },
    }


def _fit_for_mas_summary(candidates: list[dict], post_stress: list[dict]) -> dict:
    """The fit-for-MAS candidates, their type membership, and whether each has MAS."""
    mas_keys = {
        (record["bcv"], record["chanted_word"], record["jta"])
        for record in post_stress
        if record["syllables_after_the_stress"] == 1
    }
    for candidate in candidates:
        key = (candidate["bcv"], candidate["chanted_word"], candidate["jta"])
        candidate["has_mas"] = key in mas_keys
        assert candidate["has_u05bd"] == candidate["has_mas"], candidate
    following_word_conditions = [
        candidate
        for candidate in candidates
        if _has_following_word_conditions_for_mas(candidate)
    ]
    fitting = [
        candidate
        for candidate in following_word_conditions
        if candidate["structural_types"]
    ]
    by_type = {}
    for kind in (TYPE_OPEN, TYPE_GUTTURAL, TYPE_CLOSED_TSERE):
        members = [
            candidate for candidate in fitting if kind in candidate["structural_types"]
        ]
        with_mas = sum(candidate["has_mas"] for candidate in members)
        by_type[kind] = {
            "candidates": len(members),
            "with_mas": with_mas,
            "without_mas": len(members) - with_mas,
        }
    with_mas = sum(candidate["has_mas"] for candidate in fitting)
    mas_outside_the_three_types = [
        candidate
        for candidate in candidates
        if candidate["has_mas"] and not candidate["structural_types"]
    ]
    mas_with_non_disjunctive_following_word = [
        candidate
        for candidate in candidates
        if (
            candidate["has_mas"]
            and not candidate["following_chanted_word_has_disjunctive_accent"]
        )
    ]
    mas_with_noninitial_following_word = [
        candidate
        for candidate in candidates
        if candidate["has_mas"]
        and not candidate["following_chanted_word_is_initially_stressed"]
    ]
    excluded_mas = (
        mas_outside_the_three_types
        + mas_with_non_disjunctive_following_word
        + mas_with_noninitial_following_word
    )
    assert len(
        {
            (candidate["bcv"], candidate["chanted_word"], candidate["jta"])
            for candidate in excluded_mas
        }
    ) == len(excluded_mas), excluded_mas
    assert with_mas + len(excluded_mas) == len(mas_keys), (with_mas, excluded_mas)
    return {
        "what": (
            "Every syllable immediately after a nonfinal primary stress whose following"
            " chanted word has initial stress and a disjunctive accent-grammar token,"
            " classified by the three MAS structural predicates and checked for U+05BD."
            " Primary-stress position comes independently from Phonetic MAM's jta field."
        ),
        "records_what": (
            "Every chanted-word pair fit for MAS. Each record has the chanted word whose"
            " post-stress syllable is classified, the following chanted word, the applicable"
            " types, and whether the first chanted word has MAS."
        ),
        "candidate_chanted_words": len(candidates),
        "following_word_conditions": len(following_word_conditions),
        "fitting_any_type": len(fitting),
        "with_mas": with_mas,
        "without_mas": len(fitting) - with_mas,
        "by_structural_type": by_type,
        "candidates_meeting_multiple_types": sum(
            len(candidate["structural_types"]) > 1 for candidate in fitting
        ),
        "mas_not_in_the_table": {
            "outside_the_three_types": len(mas_outside_the_three_types),
            "following_word_not_disjunctive": len(
                mas_with_non_disjunctive_following_word
            ),
            "following_word_not_initially_stressed": len(
                mas_with_noninitial_following_word
            ),
        },
        "accent_grammar_token_counts": dict(
            sorted(
                Counter(
                    candidate["accent_grammar_token_count"] for candidate in candidates
                ).items()
            )
        ),
        "records": [_fit_for_mas_record(candidate) for candidate in fitting],
    }


def _scan(
    phon_dir: Path, cantillation: str = CANT_ALEF, *, dual_templates_only: bool = False
) -> dict:
    """Every U+05BD of one cantillation strand, optionally only inside its templates."""
    assert cantillation in _CANTILLATION_BRANCH_INDEX, cantillation
    found = {
        "counts": Counter(),
        "checked_chanted_words_by_bcv": Counter(),
        "pre_stress": [],
        "post_stress": [],
        "in_stressed": [],
        "overlaps": [],
        "mismatches": [],
        "same_letter_failures": [],
        "entries_without_jta_or_fva": 0,
        "last_entry_lacks_sof_pasuq": [],
        "metegs_by_verse": {},
        "dual_cant_verses": set(),
        "dual_cantillation": {},
        "dual_cantillation_chanted_words": {},
        "dual_template_entries": {},
        "type_2_type_3_overlap_by_book": Counter(),
        "type_2_type_3_overlap_by_final_letter": Counter(),
        "type_2_type_3_overlap_example": None,
        "fit_for_mas_candidates": [],
    }
    bb_of_stem = _bb_of_stem()
    for path in sorted(phon_dir.glob("*.json")):
        bb = bb_of_stem[path.stem]
        has_legarmeh = prose_scanner.HasLegarmeh()
        data = json.loads(path.read_text(encoding="utf-8"))
        for vkey, verse in data.items():
            chnu, vrnu = (int(one) for one in _VERSE_KEY.match(vkey).groups())
            dual = _has_dual_cantillation(verse)
            if dual_templates_only and not dual:
                continue
            _one_verse(
                f"{bb}{chnu}:{vrnu}",
                bb,
                chnu,
                vrnu,
                _select_cantillation_strand(verse, cantillation),
                found,
                has_legarmeh=has_legarmeh,
                dual_cantillation=dual,
                dual_facts=_dual_cantillation_facts(verse) if dual else None,
                template_entry_ids=(
                    _dual_template_entry_ids(verse, cantillation)
                    if dual_templates_only
                    else None
                ),
            )
    return found


def _one_verse(
    bcv: str,
    bb: str,
    chnu: int,
    vrnu: int,
    verse,
    found: dict,
    *,
    has_legarmeh: prose_scanner.HasLegarmeh,
    dual_cantillation: bool | None = None,
    dual_facts: dict | None = None,
    template_entry_ids: set[int] | None = None,
) -> None:
    system = (
        SYSTEM_POETIC
        if poetic_filter.should_keep_line(bb, chnu, vrnu)
        else SYSTEM_PROSE
    )
    dual = (
        _has_dual_cantillation(verse)
        if dual_cantillation is None
        else dual_cantillation
    )
    if dual:
        found["dual_cant_verses"].add(bcv)
        found["dual_cantillation"][bcv] = (
            _dual_cantillation_facts(verse) if dual_facts is None else dual_facts
        )
    events: list[object] = []
    _chanted_word_events(verse, events)
    accent_grammar_tokens = _accent_grammar_tokens_by_entry(
        bb=bb,
        chnu=chnu,
        vrnu=vrnu,
        system=system,
        events=events,
        has_legarmeh=has_legarmeh,
    )
    entries = [one for one in events if isinstance(one, dict)]
    scoped_entries = (
        entries
        if template_entry_ids is None
        else [one for one in entries if id(one) in template_entry_ids]
    )
    usable = [one for one in scoped_entries if one.get("jta") and one.get("fva")]
    all_usable = [one for one in entries if one.get("jta") and one.get("fva")]
    found["entries_without_jta_or_fva"] += len(scoped_entries) - len(usable)
    if not usable:
        return
    if dual:
        found["dual_cantillation_chanted_words"][bcv] = [
            one["fva"].split(" ")[0] for one in usable
        ]
    if template_entry_ids is not None:
        found["dual_template_entries"][bcv] = usable
    if template_entry_ids is None:
        last_word = usable[-1]["fva"].split(" ")[0]
        if SOF_PASUQ not in last_word:
            found["last_entry_lacks_sof_pasuq"].append(
                {
                    "bcv": bcv,
                    "chanted_word": last_word,
                    "dual_cantillation": dual,
                    "carries_a_meteg": METEG in last_word,
                }
            )
    metegs = 0
    event_index_by_entry_id = {
        id(entry): index
        for index, entry in enumerate(events)
        if isinstance(entry, dict)
    }
    for index, entry in enumerate(all_usable):
        if template_entry_ids is not None and id(entry) not in template_entry_ids:
            continue
        word = entry["fva"].split(" ")[0]
        jta = entry["jta"]
        following_entry = all_usable[index + 1] if index + 1 < len(all_usable) else None
        following_chanted_word = (
            following_entry["fva"].split(" ")[0]
            if following_entry is not None
            else None
        )
        following_jta = following_entry["jta"] if following_entry is not None else None
        following_accent_grammar_tokens = (
            accent_grammar_tokens[id(following_entry)]
            if following_entry is not None
            else ()
        )
        intervening_material = (
            tuple(
                events[
                    event_index_by_entry_id[id(entry)]
                    + 1 : event_index_by_entry_id[id(following_entry)]
                ]
            )
            if following_entry is not None
            else ()
        )
        metegs += word.count(METEG)
        try:
            parsed = _parse(word, jta)
        except SurveyProblem as problem:
            found["mismatches"].append(
                {"bcv": bcv, "chanted_word": word, "jta": jta, "why": str(problem)}
            )
            continue
        found["counts"][(system, "chanted words checked")] += 1
        found["checked_chanted_words_by_bcv"][bcv] += 1
        if _has_final_tsere_syllable_closed_by_guttural(parsed):
            found["type_2_type_3_overlap_by_book"][bb] += 1
            found["type_2_type_3_overlap_by_final_letter"][
                parsed["letters"][-1][0]
            ] += 1
            if found["type_2_type_3_overlap_example"] is None:
                found["type_2_type_3_overlap_example"] = {
                    "bcv": bcv,
                    "chanted_word": word,
                    "following_chanted_word": None,
                    "snapshot_before_qere": entry.get("before_qfikq"),
                }
        fit_for_mas_candidate = _fit_for_mas_candidate(
            bcv=bcv,
            system=system,
            word=word,
            jta=jta,
            parsed=parsed,
            before_qere=entry.get("before_qfikq"),
            following_chanted_word=following_chanted_word,
            following_jta=following_jta,
            following_accent_grammar_tokens=following_accent_grammar_tokens,
            accent_grammar_tokens=accent_grammar_tokens[id(entry)],
            intervening_punctuation=_fit_for_mas_intervening_punctuation(
                bcv=bcv,
                chanted_word=word,
                material=intervening_material,
            ),
        )
        if fit_for_mas_candidate is not None:
            found["fit_for_mas_candidates"].append(fit_for_mas_candidate)
        _classify_one_word(
            bcv=bcv,
            system=system,
            word=word,
            jta=jta,
            parsed=parsed,
            found=found,
            before_qere=entry.get("before_qfikq"),
            following_chanted_word=following_chanted_word,
            following_jta=following_jta,
            intervening_material=intervening_material,
        )
    found["metegs_by_verse"][bcv] = metegs


# The verses the page names outside its tables, whose chanted words it therefore has to show
# as MAM has them TODAY rather than as the surveyed snapshot has them.  Isaiah 23:12 is
# where the two differ -- suggestion M23 added a meteg there after the snapshot was taken --
# and 1 Samuel 17:5 is the post-silluq case, where the page's claim is about what MAM lacks.
# Named here rather than in the page module so the form is lifted from the corpus at
# generation time and reaches the page through the tracked JSON, as every other form does.
_FOCUS_VERSES = ("is23:12", "1s17:5")


def _mam_words_by_bcv(cantillation: str | None = None) -> dict[str, list[str]]:
    """MAM-simple's chanted words per verse, in MAM's versification.

    MAM's numbering rather than the BHS one this repo's other surveys read, because Phonetic
    MAM numbers its verses MAM's way; ``test_final_stress_vs_phonetic_mam._measured`` reaches
    for the same tree for the same reason. ``cantillation`` selects an individual
    dual-cantillation projection; otherwise this returns MAM-simple's combined representation.
    """
    from accgram import mam_simple_verse

    mam_dir = paths.require_mam_simple_vtrad_mam_dir()
    refs_by_book = mam_simple_verse.mam_simple_refs(mam_dir)
    if cantillation is None:
        return mna.mam_words(refs_by_book, mam_dir)
    return mna.mam_words_for_cantillation(refs_by_book, cantillation, mam_dir)


def _fold_qamats_qatan(key: str) -> str:
    """``key`` with U+05C7 read as an ordinary qamats.

    MAM spells qamats qatan U+05C7 and Phonetic MAM does not always agree with it about
    which qamats a word has -- Job 11:17 is where the two spellings stand side by side, as a
    qamats note offering both.  A fold is tried only after the unfolded key has failed, and
    a record that needed it says so in ``matched_by``.
    """
    return key.replace(hpo.QAMATS_Q, hpo.QAMATS)


# The marks Phonetic MAM adds that MAM's text does not have: a masora circle where it has
# resolved a sheva, an upper dot on a dagesh it takes as xazaq, and a varika where it reads an
# implicit xataf.  Dropped only to ask whether a candidate is the very chanted word the
# snapshot has -- never to build a displayed form, which is always MAM's.  U+05C5 goes with
# U+05C4 because the two puncta are one notation; a chanted word with a genuine extraordinary
# point simply fails this test and is settled by the test after it.
_PHONETIC_MAM_ANNOTATIONS = str.maketrans(
    {
        hpu.MCIRC: None,
        hpu.UPDOT: None,
        hpu.LODOT: None,
        hpo.VARIKA: None,
        hpu.NU_GMAQ: MAQAF,
    }
)


def _as_mam_would_write_it(word: str) -> str:
    return word.translate(_PHONETIC_MAM_ANNOTATIONS)


def _settle(matches: list[str], snapshot: str) -> tuple[str | None, str]:
    """Which of several candidate MAM chanted words a record's is, or none.

    A verse can hold two chanted words with the same letters and points -- Proverbs 12:1's two
    אֹהֵב, Psalms 135:1's two הללו, one with a deḥi and one with a geresh muqdam -- and the
    join key cannot tell them apart, since what separates them is exactly what it drops.  Two
    tests do: the candidate identical to the snapshot's, annotations aside, and
    failing that the one candidate whose meteg count agrees.  Neither test assumes an answer;
    both ask which chanted word this is, of the ones MAM has in that verse.
    """
    forms = list(dict.fromkeys(matches))
    if not forms:
        return None, "no match"
    if len(forms) == 1:
        return forms[0], "one candidate in the verse"
    written = _as_mam_would_write_it(snapshot)
    if written in forms:
        return written, f"the one of {len(forms)} identical to the snapshot"
    agreeing = [one for one in forms if one.count(METEG) == snapshot.count(METEG)]
    if len(agreeing) == 1:
        return agreeing[0], f"the one of {len(forms)} whose metegs agree"
    return None, f"{len(forms)} candidates, none of them settled"


def _matching_mam_words(record: dict, words: list[str]) -> tuple[list[str], str]:
    """The MAM chanted words a record's spelling can be matched to, and how it matched."""
    keys = [_join_key(record["chanted_word"])]
    if record.get("snapshot_before_qere"):
        keys.append(_join_key(record["snapshot_before_qere"]))
    for index, key in enumerate(keys):
        matches = [word for word in words if _join_key(word) == key]
        if matches:
            return matches, "the qere it stands for" if index else "as written"
    for key in keys:
        folded = _fold_qamats_qatan(key)
        matches = [
            word for word in words if _fold_qamats_qatan(_join_key(word)) == folded
        ]
        if matches:
            return matches, "with qamats qatan read as qamats"
    return [], "no match"


def _following_mam_context(
    record: dict, stream: list[str]
) -> tuple[str | None, tuple[str, ...] | None]:
    """The following MAM chanted word and intervening punctuation, if the context resolves.

    The MAM stream keeps a PASEQ as a standalone token. This makes the usual two-chanted-word
    context and the four ``vayomer`` contexts one routine: the current chanted word, zero or
    more punctuation tokens, then the following chanted word. A context is shown only after the
    complete sequence matches MAM, so every rendered form and punctuation mark comes from MAM.
    """
    following = record["following_chanted_word"]
    if following is None:
        return None, None
    next_record = {"chanted_word": following}
    source_punctuation = tuple(record.get("intervening_punctuation", ()))
    candidates: list[tuple[str, tuple[str, ...]]] = []
    for index, word in enumerate(stream):
        current_matches, _current_matched_by = _matching_mam_words(record, [word])
        if not current_matches:
            continue
        punctuation = []
        following_index = index + 1
        while following_index < len(stream) and stream[following_index] == PASEQ:
            punctuation.append(stream[following_index])
            following_index += 1
        if tuple(punctuation) != source_punctuation or following_index == len(stream):
            continue
        next_matches, _next_matched_by = _matching_mam_words(
            next_record, [stream[following_index]]
        )
        for next_match in next_matches:
            candidates.append((next_match, tuple(punctuation)))
    settled = list(dict.fromkeys(candidates))
    return settled[0] if len(settled) == 1 else (None, None)


def _attach_mam_forms(
    records: list[dict], words_by_bcv: dict[str, list[str]]
) -> list[dict]:
    """Give each record the form MAM has today, found by join key, or say why it has none.

    THE PAGE SHOWS ``mam_form`` AND NOT ``chanted_word``, and this is where the difference is
    made.  Phonetic MAM's own text carries two annotations MAM does not write -- a masora
    circle on a resolved sheva and an upper dot on a dagesh it reads as ḥazaq -- so a page
    showing its forms verbatim would put marks in front of a reader that MAM's text does not
    have.  The join key drops exactly what the two sides may legitimately differ in, this
    survey's own subject included, so a chanted word that has GAINED or LOST a meteg since
    the snapshot still matches, and the record says so in ``metegs_in_mam_today``.

    TWO IDENTICAL CANDIDATES ARE ONE ANSWER, and are accepted: a verse with two byte-identical
    chanted words -- Proverbs 12:1's two אֹהֵב, Psalms 135:1's two הללו -- leaves the position
    ambiguous and the FORM certain, which is all the page shows.  Two candidates that differ
    are refused, since then the form is a choice.

    A record with no form is named in ``records_without_a_mam_form``, and the page falls back
    to the snapshot's spelling for it, marked as such.
    """
    out = []
    for record in records:
        matches, keyed_by = _matching_mam_words(
            record, words_by_bcv.get(record["bcv"], [])
        )
        settled, settled_by = _settle(matches, record["chanted_word"])
        record["mam_form"] = settled
        record["mam_form_matched_by"] = f"{keyed_by}; {settled_by}"
        record["mam_form_candidates"] = len(set(matches))
        record["metegs_in_mam_today"] = settled.count(METEG) if settled else None
        record["metegs_in_the_snapshot"] = record["chanted_word"].count(METEG)
        following_mam_form, intervening_mam_punctuation = (
            _following_mam_context(record, words_by_bcv.get(record["bcv"], []))
            if settled is not None
            else (None, None)
        )
        record["following_mam_form"] = following_mam_form
        if intervening_mam_punctuation:
            record["intervening_mam_punctuation"] = intervening_mam_punctuation
        if settled is not None:
            # Recomputed off MAM's own form, so that every Hebrew string the page can render
            # from this record comes from one text rather than two.
            record["accents_and_letters"] = _bare(settled)
        else:
            out.append(record)
    return out


def _focus_verses(words_by_bcv: dict[str, list[str]]) -> dict:
    """Each focus verse's chanted words, as MAM has them today."""
    return {
        bcv: {
            "chanted_words": list(words_by_bcv[bcv]),
            "metegs": sum(word.count(METEG) for word in words_by_bcv[bcv]),
        }
        for bcv in _FOCUS_VERSES
    }


def _currency(found: dict, words_by_bcv: dict[str, list[str]]) -> dict:
    """How far the surveyed snapshot of MAM stands from the MAM-simple beside it.

    A per-verse U+05BD count on each side, in MAM's own versification so the verse keys line
    up, and every verse where the two disagree.  This needs no word-by-word alignment and so
    survives the places where the two texts group atoms differently.

    DUAL-CANTILLATION VERSES ARE LEFT OUT, and would otherwise dominate the list: Phonetic MAM
    has both strands where MAM-simple's loader yields the combined stream once, so the two
    counts differ there for a structural reason rather than because either text moved.
    """
    today = {
        bcv: sum(word.count(METEG) for word in words)
        for bcv, words in words_by_bcv.items()
    }
    surveyed = found["metegs_by_verse"]
    compared = sorted((set(surveyed) & set(today)) - found["dual_cant_verses"])
    differences = [
        {
            "bcv": bcv,
            "surveyed_snapshot": surveyed[bcv],
            "mam_simple_today": today[bcv],
        }
        for bcv in compared
        if surveyed[bcv] != today[bcv]
    ]
    return {
        "what": (
            "The Phonetic MAM standard set is regenerated in al-hatorah, on its own"
            " occasions, so it is a snapshot of MAM rather than MAM's current state. This"
            " counts U+05BD per numbered verse on both sides and names every numbered verse"
            " where they differ, so the page can say which MAM its figures describe."
        ),
        "how": (
            "Per NUMBERED verse, in MAM's own versification, which is the numbering both"
            " sides use. Nothing here aligns words, so it survives the places where the two"
            " texts group atoms differently. Dual-cantillation numbered verses are left out:"
            " Phonetic MAM has both strands where MAM-simple's loader yields the combined"
            " stream once. Every other numbered verse ends on a chanted word with sof pasuq,"
            " measured 2026-09-04, so no chanted verse in the comparison runs past a"
            " numbered verse's end."
        ),
        "surveyed_snapshot": paths.display_path(paths.al_hatorah_phonetic_dir()),
        "compared_against": paths.display_path(paths.mam_simple_vtrad_mam_dir()),
        "focus_verses": _focus_verses(words_by_bcv),
        "verses_compared": len(compared),
        "verses_on_one_side_only": sorted(set(surveyed) ^ set(today)),
        "dual_cantillation_verses_left_out": len(found["dual_cant_verses"]),
        "metegs_in_the_surveyed_snapshot": sum(surveyed[bcv] for bcv in compared),
        "metegs_in_mam_simple_today": sum(today[bcv] for bcv in compared),
        "verses_differing": len(differences),
        "differences": differences,
    }


def _legacy_baseline(counts: Counter) -> dict:
    """Every difference between this run and the 2026-09-03 census, category by category."""
    differences = [
        {
            "system": system,
            "category": category,
            "census_2026_09_03": baseline,
            "measured": counts[(system, category)],
            "difference": counts[(system, category)] - baseline,
        }
        for system, categories in _LEGACY_BASELINE.items()
        for category, baseline in categories.items()
        if counts[(system, category)] != baseline
    ]
    return {
        "what": (
            "The 2026-09-03 census, doc/post-stress-meteg-census-2026-09-03.md, whose script"
            " is untracked and treats a verse's last parsed entry as verse-final whether or"
            " not it carries sof pasuq. A comparison baseline, not a second measurement."
        ),
        "baseline": _LEGACY_BASELINE,
        "differences": differences,
    }


def _problems(found: dict) -> list[str]:
    """What makes a run unable to finish honestly, all of it, rather than the first of it."""
    out = []
    if found["same_letter_failures"]:
        refs = [one["bcv"] for one in found["same_letter_failures"][:20]]
        out.append(
            f"{len(found['same_letter_failures'])} metegs share a letter with a"
            f" stress-bearing accent, whose order is undefined: {refs}"
        )
    if found["mismatches"]:
        refs = [one["bcv"] for one in found["mismatches"][:20]]
        out.append(
            f"{len(found['mismatches'])} chanted words where the jta and the Hebrew count"
            f" syllables differently: {refs}"
        )
    unexplained = [
        one
        for one in found["last_entry_lacks_sof_pasuq"]
        if not one["dual_cantillation"] or one["carries_a_meteg"]
    ]
    if unexplained:
        refs = [one["bcv"] for one in unexplained[:20]]
        out.append(
            f"{len(unexplained)} verses whose last chanted word lacks sof pasuq outside a"
            f" dual-cantillation span, or lacks it while carrying a meteg: {refs}"
        )
    return out


def _total_counts(found: dict, categories: tuple[str, ...]) -> dict[str, int]:
    """The two verse systems' totals for the specified census categories."""
    return {
        category: sum(
            found["counts"][(system, category)]
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        )
        for category in categories
    }


def _dual_template_counts(found: dict) -> dict[str, int]:
    """The three appendix counts restricted to dual-cantillation templates."""
    return {
        "chanted words checked": sum(found["checked_chanted_words_by_bcv"].values()),
        "meteg before the stressed syllable": len(found["pre_stress"]),
        "meteg after the stressed syllable": len(found["post_stress"]),
    }


def _consonant_key(text: str) -> str:
    """The Hebrew letters of a chanted word, ignoring vowels, accents, and punctuation."""
    return re.sub("[\u0591-\u05c7\u034f]", "", text)


def _mam_form_for_dual_cantillation_atom(raw_atom: str, mam_atoms: list[str]) -> str:
    """The MAM atom with only the cantillation marks of ``raw_atom``'s branch.

    Phonetic MAM marks a resolved sheva with a masora circle that MAM's text does not have.
    The raw atom therefore decides only which accent and meteg marks its cantillation branch
    selects; its letters and points never reach the reader-facing form.
    """
    candidates = [
        atom for atom in mam_atoms if _consonant_key(atom) == _consonant_key(raw_atom)
    ]
    assert len(candidates) == 1, (raw_atom, candidates)
    selected_marks = {char for char in raw_atom if is_accent(char) or char == METEG}
    return "".join(
        char
        for char in candidates[0]
        if not (is_accent(char) or char == METEG) or char in selected_marks
    )


def _mam_forms_for_dual_cantillation_difference(
    raw_words: list[str], words_by_bcv: dict[str, list[str]], bcv: str
) -> list[str]:
    """The MAM forms selected by one branch's Phonetic-MAM grouping and accents."""
    mam_atoms = [
        atom
        for word in words_by_bcv[bcv]
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    ]
    return [
        MAQAF.join(
            _mam_form_for_dual_cantillation_atom(atom, mam_atoms)
            for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", raw_word)
        )
        for raw_word in raw_words
    ]


def _extra_metegs_before_stress(records: list[dict], other: list[dict]) -> list[dict]:
    """The before-stress records in ``records`` that have no matching chanted word in ``other``."""
    unmatched = Counter(_consonant_key(one["chanted_word"]) for one in other)
    out = []
    for record in records:
        key = _consonant_key(record["chanted_word"])
        if unmatched[key]:
            unmatched[key] -= 1
        else:
            out.append(record)
    return out


def _meteg_before_stress_difference(
    found_alef: dict,
    found_bet: dict,
    words_by_cantillation: dict[str, dict[str, list[str]]],
) -> dict:
    """The single dually-cantillated chanted-word difference in meteg-before-stress count."""
    dual_bcv = found_alef["dual_cant_verses"]
    assert dual_bcv == found_bet["dual_cant_verses"]
    alef_by_bcv = Counter(
        one["bcv"] for one in found_alef["pre_stress"] if one["bcv"] in dual_bcv
    )
    bet_by_bcv = Counter(
        one["bcv"] for one in found_bet["pre_stress"] if one["bcv"] in dual_bcv
    )
    different_bcv = [bcv for bcv in dual_bcv if alef_by_bcv[bcv] != bet_by_bcv[bcv]]
    assert len(different_bcv) == 1, different_bcv
    bcv = different_bcv[0]
    assert bet_by_bcv[bcv] == alef_by_bcv[bcv] + 1
    alef_records = [one for one in found_alef["pre_stress"] if one["bcv"] == bcv]
    bet_records = [one for one in found_bet["pre_stress"] if one["bcv"] == bcv]
    extra_bet = _extra_metegs_before_stress(bet_records, alef_records)
    assert not _extra_metegs_before_stress(alef_records, bet_records)
    assert len(extra_bet) == 1, extra_bet
    bet_record = extra_bet[0]
    assert bet_record["bcv"] == bcv
    target_atom_keys = {
        _consonant_key(atom)
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", bet_record["chanted_word"])
    }
    alef_counterparts = [
        word
        for word in found_alef["dual_cantillation_chanted_words"][bcv]
        if target_atom_keys
        & {_consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)}
    ]
    assert len(alef_counterparts) == 2, alef_counterparts
    assert all(METEG not in word for word in alef_counterparts), alef_counterparts
    counterpart_atom_keys = {
        _consonant_key(atom)
        for word in alef_counterparts
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    }
    bet_counterparts = [
        word
        for word in found_bet["dual_cantillation_chanted_words"][bcv]
        if counterpart_atom_keys
        & {_consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)}
    ]
    assert len(bet_counterparts) == 2, bet_counterparts
    assert bet_record["chanted_word"] in bet_counterparts, bet_counterparts
    return {
        "bcv": bcv,
        CANT_ALEF: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                alef_counterparts, words_by_cantillation[CANT_ALEF], bcv
            )
        },
        CANT_BET: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                bet_counterparts, words_by_cantillation[CANT_BET], bcv
            )
        },
    }


def _template_mam_forms(
    entries: list[dict], words_by_bcv: dict[str, list[str]], bcv: str
) -> list[str]:
    """The selected template span's chanted words, as MAM has them today.

    A template can include a qere, so the raw Phonetic-MAM form alone cannot identify MAM's
    form.  ``_attach_mam_forms`` already settles that relation, including its qere spelling,
    and refuses an ambiguous match.
    """
    records = [
        {
            "bcv": bcv,
            "chanted_word": entry["fva"].split(" ")[0],
            "following_chanted_word": None,
            "snapshot_before_qere": entry.get("before_qfikq"),
        }
        for entry in entries
    ]
    unjoined = _attach_mam_forms(records, words_by_bcv)
    assert not unjoined, unjoined
    forms = [record["mam_form"] for record in records]
    assert all(forms), forms
    return forms


def _atom_keys(word: str) -> tuple[str, ...]:
    """The consonant keys of a chanted word's atoms, in their written order."""
    return tuple(
        _consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    )


def _different_chanted_word_spans(
    alef_words: list[str], bet_words: list[str]
) -> list[tuple[slice, slice]]:
    """The aligned spans whose atom grouping differs between two template branches."""
    alef_index = 0
    bet_index = 0
    out = []
    while alef_index < len(alef_words) and bet_index < len(bet_words):
        if _atom_keys(alef_words[alef_index]) == _atom_keys(bet_words[bet_index]):
            alef_index += 1
            bet_index += 1
            continue
        alef_start = alef_index
        bet_start = bet_index
        alef_atoms: list[str] = []
        bet_atoms: list[str] = []
        while not alef_atoms or not bet_atoms or alef_atoms != bet_atoms:
            if len(alef_atoms) <= len(bet_atoms):
                assert alef_index < len(alef_words), (alef_words, bet_words)
                alef_atoms.extend(_atom_keys(alef_words[alef_index]))
                alef_index += 1
            else:
                assert bet_index < len(bet_words), (alef_words, bet_words)
                bet_atoms.extend(_atom_keys(bet_words[bet_index]))
                bet_index += 1
        out.append((slice(alef_start, alef_index), slice(bet_start, bet_index)))
    assert alef_index == len(alef_words), (alef_words, bet_words)
    assert bet_index == len(bet_words), (alef_words, bet_words)
    return out


def _chanted_word_count_difference(
    found_alef: dict,
    found_bet: dict,
    words_by_cantillation: dict[str, dict[str, list[str]]],
) -> dict:
    """The template grouping that makes cant-alef's chanted-word count one larger."""
    dual_bcv = found_alef["dual_cant_verses"]
    assert dual_bcv == found_bet["dual_cant_verses"]
    different_bcv = [
        bcv
        for bcv in dual_bcv
        if (
            found_alef["checked_chanted_words_by_bcv"][bcv]
            != found_bet["checked_chanted_words_by_bcv"][bcv]
        )
    ]
    assert len(different_bcv) == 1, different_bcv
    bcv = different_bcv[0]
    alef_words = found_alef["dual_cantillation_chanted_words"][bcv]
    bet_words = found_bet["dual_cantillation_chanted_words"][bcv]
    spans = _different_chanted_word_spans(alef_words, bet_words)
    assert len(spans) == 1, spans
    alef_span, bet_span = spans[0]
    assert (alef_span.stop - alef_span.start) == (bet_span.stop - bet_span.start) + 1
    alef_forms = _template_mam_forms(
        found_alef["dual_template_entries"][bcv][alef_span],
        words_by_cantillation[CANT_ALEF],
        bcv,
    )
    bet_forms = _template_mam_forms(
        found_bet["dual_template_entries"][bcv][bet_span],
        words_by_cantillation[CANT_BET],
        bcv,
    )
    return {
        "bcv": bcv,
        CANT_ALEF: {"chanted_words": alef_forms},
        CANT_BET: {"chanted_words": bet_forms},
    }


def build_survey() -> dict:
    """The whole survey: every U+05BD of the Phonetic MAM standard set, classified.

    Raises ``SurveyProblem`` at the END of the scan rather than at the first offending mark,
    so a run that cannot finish still says everything it found.  Collecting before failing is
    what makes the list usable: a run that raises on first sight can never enumerate the rest.
    """
    phon_dir = paths.require_al_hatorah_phonetic_dir()
    found = _scan(phon_dir, CANT_ALEF)
    found_bet = _scan(phon_dir, CANT_BET)
    template_found = _scan(phon_dir, CANT_ALEF, dual_templates_only=True)
    template_found_bet = _scan(phon_dir, CANT_BET, dual_templates_only=True)
    assert found["dual_cant_verses"] == found_bet["dual_cant_verses"]
    assert template_found["dual_cant_verses"] == found["dual_cant_verses"]
    assert template_found_bet["dual_cant_verses"] == found["dual_cant_verses"]
    words_by_bcv = _mam_words_by_bcv()
    words_by_cantillation = {
        CANT_ALEF: _mam_words_by_bcv(CANT_ALEF),
        CANT_BET: _mam_words_by_bcv(CANT_BET),
    }
    unjoined = _attach_mam_forms(
        found["post_stress"] + found["in_stressed"] + found["overlaps"], words_by_bcv
    )
    problems = _problems(found) + _problems(found_bet)
    if problems:
        raise SurveyProblem("; ".join(problems))
    counts = found["counts"]
    post_stress = found["post_stress"]
    _assert_type_2_following_filter_coverage(post_stress)
    fit_for_mas = _fit_for_mas_summary(found["fit_for_mas_candidates"], post_stress)
    by_type = Counter((one["system"], one["structural_type"]) for one in post_stress)
    by_subtype = Counter(
        (one["system"], one["subtype"])
        for one in post_stress
        if one["subtype"] is not None
    )
    type_2_type_3_overlap_by_book = found["type_2_type_3_overlap_by_book"]
    type_2_type_3_overlap_by_final_letter = found[
        "type_2_type_3_overlap_by_final_letter"
    ]
    type_2_type_3_overlap_count = sum(type_2_type_3_overlap_by_book.values())
    assert type_2_type_3_overlap_count == sum(
        type_2_type_3_overlap_by_final_letter.values()
    )
    type_2_type_3_overlap_example = found["type_2_type_3_overlap_example"]
    assert type_2_type_3_overlap_example is not None
    unjoined_overlap_example = _attach_mam_forms(
        [type_2_type_3_overlap_example], words_by_bcv
    )
    assert not unjoined_overlap_example, unjoined_overlap_example
    assert type_2_type_3_overlap_example["mam_form"] is not None
    return {
        "what": (
            "Every U+05BD in MAM, classified by whether its syllable falls before, in, or"
            " after the chanted word's one primary stress. A U+05BD in the stressed syllable"
            " of a chanted word carrying sof pasuq is the silluq, and is counted as that"
            " rather than as a meteg."
        ),
        "stress_oracle": (
            "Phonetic MAM's jta field, whose ! marks the one stressed syllable. A U+05BD's"
            " own position is never used to infer the stress. The Hebrew's nuclei are counted"
            " independently and the two counts must agree per chanted word, a furtive patax"
            " counting as a syllable on both sides."
        ),
        "silluq_boundary": SILLUQ_RULE,
        "scope": (
            "Every chanted word of every verse. Prose verses and poetic verses are routed by"
            " accgram.poetic_filter, so Job's prose frame goes with the 21 books. A dual"
            " cantillation passage is counted with the cant-alef cantillation strand, as"
            " though it were read once."
        ),
        "dual_cantillation": {
            "counted_cantillation": CANT_ALEF,
            "numbered_verses": sorted(found["dual_cant_verses"]),
            "facts_by_numbered_verse": found["dual_cantillation"],
            "whole_census_comparison_counts": {
                CANT_ALEF: _total_counts(
                    found, _DUAL_CANTILLATION_COMPARISON_CATEGORIES
                ),
                CANT_BET: _total_counts(
                    found_bet, _DUAL_CANTILLATION_COMPARISON_CATEGORIES
                ),
            },
            "template_counts": {
                CANT_ALEF: _dual_template_counts(template_found),
                CANT_BET: _dual_template_counts(template_found_bet),
            },
            "meteg_before_stress_difference": _meteg_before_stress_difference(
                template_found, template_found_bet, words_by_cantillation
            ),
            "chanted_word_count_difference": _chanted_word_count_difference(
                template_found, template_found_bet, words_by_cantillation
            ),
        },
        "counts": {
            system: {one: counts[(system, one)] for one in _COUNT_CATEGORIES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "post_stress_by_structural_type": {
            system: {one: by_type[(system, one)] for one in _TYPES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "post_stress_by_subtype": {
            system: {one: by_subtype[(system, one)] for one in _SUBTYPES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "fit_for_mas": fit_for_mas,
        "stress_accent_classification": stress_accent_classification(post_stress),
        "type_2_type_3_overlap": {
            "chanted_words": type_2_type_3_overlap_count,
            "by_book": dict(sorted(type_2_type_3_overlap_by_book.items())),
            "by_final_letter": dict(
                sorted(type_2_type_3_overlap_by_final_letter.items())
            ),
            "example": {
                "bcv": type_2_type_3_overlap_example["bcv"],
                "mam_form": type_2_type_3_overlap_example["mam_form"],
            },
        },
        "post_stress": post_stress,
        "post_silluq": {
            "what": (
                "A meteg on a syllable AFTER the silluq, which would put two U+05BD in one"
                " verse-final chanted word and make telling the meteg from the silluq a"
                " question about syllables rather than about position."
            ),
            "in_mam": sum(1 for one in post_stress if one["has_sof_pasuq"]),
            "how_it_is_counted": (
                "A post-stress record whose chanted word carries sof pasuq is one: the"
                " silluq is in the stressed syllable and this mark is after it. The census"
                " of 2026-09-03 could not support this count, its verse-final test having"
                " been position-based, and the claim was withdrawn from"
                " doc/holman-meteg-m23-isaiah-23-12.md on that ground."
            ),
        },
        "diagnostics": {
            "meteg_in_the_stressed_syllable_without_sof_pasuq": found["in_stressed"],
            "sharing_a_letter_with_a_non_stress_marking_accent": found["overlaps"],
            "entries_without_jta_or_fva": found["entries_without_jta_or_fva"],
            "numbered_verses_whose_last_entry_lacks_sof_pasuq": found[
                "last_entry_lacks_sof_pasuq"
            ],
            "records_without_a_mam_form": [
                {
                    "bcv": one["bcv"],
                    "chanted_word": one["chanted_word"],
                    "candidate_forms_in_mam_simple": one["mam_form_candidates"],
                }
                for one in unjoined
            ],
        },
        "legacy_baseline": _legacy_baseline(counts),
        "currency": _currency(found, words_by_bcv),
    }


def default_json_out_path() -> Path:
    return paths.out_dir() / "accgram" / "post-stress-meteg.json"


def load_survey(path: Path | None = None) -> dict:
    """The tracked JSON, for a caller rendering the page without the MAM-private clone."""
    json_path = path or default_json_out_path()
    if not json_path.exists():
        raise SurveyProblem(
            f"{json_path} is absent; run `main_accgram.py survey-post-stress-meteg` to"
            " write it, which needs the MAM-private clone"
        )
    return json.loads(json_path.read_text(encoding="utf-8"))


def write_json(survey: dict, path: Path) -> None:
    payload = provenance.with_json_provenance(survey, __file__)
    # Through file_io for the temp-file write and the PermissionError retry; it makes the
    # directory too, and its default newline="" translates nothing, which is what keeps a
    # regeneration from looking like a whole-file diff on Windows.
    file_io.json_dump_to_file_path(payload, str(path), indent=1)


def add_args(parser, *, repo_root: Path) -> None:
    # repo_root is unused: the default comes from ``default_json_out_path``, which composes
    # off ``paths.out_dir()``, so the flag's default and its absence cannot answer
    # differently.  The parameter is kept because the entry point wires every subcommand the
    # same way.
    del repo_root
    parser.add_argument(
        "--json-out",
        type=Path,
        default=default_json_out_path(),
        help="Where to write the survey JSON.",
    )


def run(args) -> None:
    survey = build_survey()
    out_path = getattr(args, "json_out", None) or default_json_out_path()
    write_json(survey, out_path)
    print(f"wrote {out_path}")
