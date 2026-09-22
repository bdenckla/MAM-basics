"""Data shapes and low-level analysis for the post-stress-meteg survey."""

from __future__ import annotations

import re
from collections import Counter

from accgram import poetic_accent_names as pan
from accgram import poetic_scanner
from accgram import prose_scanner
from accgram import uni_to_marks
from accgram import chanted_word_accents as cwa
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.uni_to_marks import is_accent
from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

METEG = hpo.MTGOSLQ

SOF_PASUQ = hpu.SOPA

MAQAF = hpu.MAQ

PASOLEG = hpu.PASOLEG

SILLUQ_RULE = (
    "A U+05BD is the silluq when it is in the stressed syllable of a chanted word that"
    " has sof pasuq. Both conditions are required and there is no third. Sof pasuq identifies"
    " the last chanted word directly; a parsed entry's position within a numbered verse is"
    " not evidence of silluq."
)

# Phonetic MAM spells MAM's gray maqaf as a tilde and its ordinary maqaf as U+05BE; both are
# atom boundaries inside one chanted word, and neither is a nucleus.
_BOUNDARIES = frozenset((MAQAF, hpu.NU_GMAQ))

# Phonetic MAM puts this token between two chanted words at a paseq/legarmeh glyph. It is
# converted to MAM's U+05C0 only after the survey has located it structurally, never by treating
# the label as Hebrew text to display. Phonetic MAM does not encode the grammatical distinction;
# MAM-simple supplies that distinction when the survey attaches the current forms.
_PHONETIC_MAM_PASOLEG = (
    "\N{HEBREW LETTER MEM}:\N{HEBREW LETTER PE}\N{HEBREW LETTER SAMEKH}"
    "\N{HEBREW LETTER QOF}"
)

_CB_QAMATS_MARKER = "cb-qamats"

_PHONETIC_MAM_SETUMA_MARKERS = frozenset(("סס", "ססס"))

_PHONETIC_MAM_PETUXA_MARKERS = frozenset(("פפ", "פפפ"))

_PHONETIC_MAM_NON_PUNCTUATION_MATERIAL = (
    frozenset((None, _CB_QAMATS_MARKER))
    | _PHONETIC_MAM_SETUMA_MARKERS
    | _PHONETIC_MAM_PETUXA_MARKERS
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

# The Type 2 page filters every next word into one of these five groups.  The initial
# letters are named exhaustively rather than putting unexpected initials in a catchall: a
# changed corpus must stop the survey until its new group has been considered.
TYPE_2_NEXT_WORD_FILTER_GROUPS = ("bet", "guttural", "lamed", "mem", "resh")

_TYPE_2_NEXT_WORD_FILTER_GROUP_BY_INITIAL = {
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
    hpo.TSERE: "tsere",
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
# sides are compared over the syllables that do NOT have this marker.
_VOCAL_SHEVA = "^"

# ``jta``'s vowel letters, uppercase for the long vowels and lowercase for the short.  Only
# ONE question is asked of them: a syllable ending in a vowel letter is open and one ending
# in anything else is closed.  What the closing consonant IS cannot be read here -- ``kash``
# ends in the h of a shin and ``lakh`` in the h of a kaf -- so the guttural test below reads
# the Hebrew instead.
_JTA_VOWELS = frozenset("aeiouAEIOU860")

# A simple vocal sheva or xataf vowel at the opening of a chanted word belongs to the next
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
# disjunctive tokens among them; a next chanted word can also have conjunctive or secondary tokens,
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

TYPE_1_SUBTYPE_A = "A"

TYPE_1_SUBTYPE_B = "B"

TYPE_1_SUBTYPE_C = "C"

_TYPE_1_SUBTYPES = (TYPE_1_SUBTYPE_A, TYPE_1_SUBTYPE_B, TYPE_1_SUBTYPE_C)

# Fit for MAS distinguishes the two admitted type-1 subtypes from the structural types 2 and
# 3.  The short labels are also the labels used in the reader-facing Fit-for-MAS table.
FIT_TYPE_1_A = "1A"

FIT_TYPE_1_B = "1B"

FIT_TYPE_2_AF = "2Af"

FIT_TYPE_2_BF = "2Bf"

FIT_TYPE_3 = "3"

_FIT_TYPES = (FIT_TYPE_1_A, FIT_TYPE_1_B, FIT_TYPE_2_AF, FIT_TYPE_2_BF, FIT_TYPE_3)

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


def type_2_next_filter_group(next_word: str) -> str:
    """The Type 2 filter group for a next MAM chanted word.

    This intentionally raises for an unexpected initial.  A catchall filter would let the
    page continue to claim complete coverage while concealing a corpus change that needs a
    human choice about the filters.
    """
    letters = _letters(next_word)
    assert letters, f"no Hebrew letter in next MAM chanted word: {next_word!r}"
    initial = letters[0][0]
    assert initial in _TYPE_2_NEXT_WORD_FILTER_GROUP_BY_INITIAL, (
        "Type 2 next-chanted-word initial is outside the page filters: "
        f"{initial!r} in {next_word!r}"
    )
    return _TYPE_2_NEXT_WORD_FILTER_GROUP_BY_INITIAL[initial]


def _assert_type_2_next_filter_coverage(records: list[dict]) -> None:
    """Require the Type 2 filters to classify every Type 2 record this run finds."""
    type_2_records = [
        record for record in records if record["structural_type"] == TYPE_GUTTURAL
    ]
    group_count = Counter()
    for record in type_2_records:
        next_word = record["next_mam_form"]
        assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
        group_count[type_2_next_filter_group(next_word)] += 1
    assert sum(group_count.values()) == len(type_2_records)
    assert set(group_count) <= set(TYPE_2_NEXT_WORD_FILTER_GROUPS)


def _has_a_vowel(marks: str) -> bool:
    return any(mark in _NUCLEUS_POINTS for mark in marks)


def _nuclei(letters: list[tuple[str, str, bool]]) -> list[tuple[int, str]]:
    """``(index of the letter with each nucleus, the point that is the nucleus)``.

    A FURTIVE PATAX COUNTS, unlike in ``final_stress``: Phonetic MAM has it as a syllable of
    separately, the two sides' syllable counts are compared here, so it has to count on this
    side too.  A xolam male and a shuruq are written on a vav that is a mater, so each belongs
    to the consonant before it -- unless that consonant already has a vowel, where the vav
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
    """Whether a next chanted word meets Yeivin's type-1 stress condition.

    An opening simple vocal sheva or xataf vowel belongs to the next segment as the first
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


def _starts_with_a_vocal_shewa(jta: str) -> bool:
    """Whether a chanted word's first JTA segment is a simple or xataf vocal shewa."""
    first_segment = _SYLLABLE_BREAK.split(jta)[0]
    return _VOCAL_SHEVA in first_segment or bool(set(first_segment) & _XATAF_JTA_VOWELS)


def _type_1_subtype(next_chanted_word: str | None, next_jta: str | None) -> str | None:
    """The next chanted word's type-1 initial-stress subtype, if it has initial stress."""
    if next_chanted_word is None or next_jta is None:
        return None
    if not _first_syllable_is_stressed(next_jta):
        return None
    if _starts_with_a_vocal_shewa(next_jta):
        return TYPE_1_SUBTYPE_A
    next_parsed = _parse(next_chanted_word, next_jta)
    has_pashta_stress_helper = next_chanted_word.count(
        ha.PASH
    ) == 2 and ha.PASH in _stress_letter_accents(next_parsed)
    return TYPE_1_SUBTYPE_B if has_pashta_stress_helper else TYPE_1_SUBTYPE_C


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
    * a closed syllable whose nucleus is a tsere is ITM §338. This is the narrower condition this
      survey uses for type 3; CoS Ch. 8 type (a) is wider, covering a long vowel in a closed
      syllable.

    Anything else -- a closed syllable with some other vowel, the segol of vayomer above all --
    is left unclassified and stays visible as itself.  A final closed ḥolam syllable is the
    ``misc-almost-type-3`` subtype: it fits CoS's wider long-vowel condition but not ITM's tsere
    type.
    """
    if is_open and is_last_syllable:
        return TYPE_OPEN, None
    if chanted_word_is_closed_by_a_guttural:
        return TYPE_GUTTURAL, None
    if is_last_syllable and not is_open and vowel == hpo.TSERE:
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
        and intervening_punctuation == (PASOLEG,)
    ):
        return SUBTYPE_MISC_VAYOMER
    return None


_PHONETIC_WORD_REQUIRED_FIELDS = frozenset({"fva", "jta", "udl"})

_PHONETIC_WORD_STRING_FIELDS = frozenset(
    {
        "adl",
        "before_qfikq",
        "before_rm_kol_cgj",
        "before_rm_misc",
        "fva",
        "jta",
        "phi",
        "phonrec-musical-gaya",
        "phonrec-musical-gaya-acc",
        "phonrec-musical-gaya-fine",
        "phonrec-qamats",
        "phonrec-shureq-xxx-shewa",
        "rep",
        "udl",
    }
)

_PHONETIC_WORD_ALLOWED_FIELDS = _PHONETIC_WORD_STRING_FIELDS | {
    "phonrec-musical-gaya-ogc",
    "phonrec-varika-but-silent",
}


def _validate_phonetic_word(node: dict) -> None:
    """Validate one current Phonetic MAM chanted-word record."""
    actual = set(node)
    if not _PHONETIC_WORD_REQUIRED_FIELDS <= actual:
        missing = sorted(_PHONETIC_WORD_REQUIRED_FIELDS - actual)
        raise SurveyProblem(
            f"Phonetic MAM chanted word lacks fields {missing}: {node!r}"
        )
    if not actual <= _PHONETIC_WORD_ALLOWED_FIELDS:
        unexpected = sorted(actual - _PHONETIC_WORD_ALLOWED_FIELDS)
        raise SurveyProblem(
            f"Phonetic MAM chanted word has unclassified fields {unexpected}: {node!r}"
        )
    for field in actual & _PHONETIC_WORD_STRING_FIELDS:
        if not isinstance(node[field], str):
            raise SurveyProblem(
                f"Phonetic MAM chanted-word field {field!r} is not text: {node!r}"
            )
    if (
        "phonrec-musical-gaya-ogc" in node
        and type(node["phonrec-musical-gaya-ogc"]) is not int
    ):
        raise SurveyProblem(
            "Phonetic MAM chanted-word field 'phonrec-musical-gaya-ogc' is not an"
            f" integer: {node!r}"
        )
    if (
        "phonrec-varika-but-silent" in node
        and node["phonrec-varika-but-silent"] is not True
    ):
        raise SurveyProblem(
            "Phonetic MAM chanted-word field 'phonrec-varika-but-silent' is not true:"
            f" {node!r}"
        )


def _chanted_words(node: object, out: list[dict]) -> None:
    """Every chanted-word entry of one verse, the ``cb`` structures flattened.

    A ``cb`` is Phonetic MAM's bracket for something other than a plain run of chanted words
    -- a paseq, a setuma or petuxa, a qamats note, a dual-cantillation span. The census projects
    each dual span onto one strand before calling this walk. The same walk
    ``test_final_stress_vs_phonetic_mam._chanted_words`` makes.
    """
    if isinstance(node, dict):
        _validate_phonetic_word(node)
        out.append(node)
    elif isinstance(node, list):
        for sub in node[1:] if node and node[0] == "cb" else node:
            _chanted_words(sub, out)
    elif node is None:
        # Phonetic MAM uses null as named non-punctuation material between entries.
        return
    elif not isinstance(node, str):
        raise TypeError(f"unclassified Phonetic MAM node: {node!r}")


def _chanted_word_events(node: object, out: list[object]) -> None:
    """The same chanted-word sequence, retaining material between its entries.

    ``_chanted_words`` is the broad census walk, intentionally omitting everything other than
    entries. The individual-case page needs narrower context for a post-stress record: an
    intervening paseq/legarmeh glyph is part of the reason its ``vayomer`` cases are distinct.
    Retaining all other material here makes an unexpected future gap a survey failure rather than
    an omission.
    """
    if isinstance(node, dict):
        _validate_phonetic_word(node)
        out.append(node)
    elif isinstance(node, list):
        for sub in node[1:] if node and node[0] == "cb" else node:
            _chanted_word_events(sub, out)
    elif isinstance(node, str) or node is None:
        out.append(node)
    else:
        raise TypeError(f"unclassified Phonetic MAM node: {node!r}")


def _compound_marker(payload: object) -> str | None:
    """The marker at the head of a Phonetic MAM compound-bracket payload."""
    if (
        isinstance(payload, list)
        and payload
        and isinstance(payload[0], list)
        and len(payload[0]) == 1
        and isinstance(payload[0][0], str)
    ):
        return payload[0][0]
    return None


def _qamats_variant_branches(payload: object) -> list[object]:
    """The two validated phonetic readings in one qamats-variant row."""
    assert _compound_marker(payload) == _CB_QAMATS_MARKER, payload
    assert isinstance(payload, list)
    branches = payload[1:]
    assert len(branches) == 2, payload
    entries_by_branch = []
    for branch in branches:
        entries: list[dict] = []
        _chanted_words(branch, entries)
        assert entries and all(
            one.get("fva") and one.get("jta") for one in entries
        ), payload
        entries_by_branch.append(entries)
    assert {one.get("phonrec-qamats") for one in entries_by_branch[0]} == {
        "qamats-dal"
    }, payload
    assert {one.get("phonrec-qamats") for one in entries_by_branch[1]} == {
        "qamats-sam"
    }, payload
    atom_keys_by_branch = [
        tuple(
            atom_key
            for entry in entries
            for atom_key in _atom_keys(entry["fva"].split(" ")[0])
        )
        for entries in entries_by_branch
    ]
    assert atom_keys_by_branch[0] == atom_keys_by_branch[1], payload
    if len(entries_by_branch[0]) == len(entries_by_branch[1]):
        for first, second in zip(*entries_by_branch, strict=True):
            first_word = first["fva"].split(" ")[0]
            second_word = second["fva"].split(" ")[0]
            assert _fold_qamats_qatan(
                _phonetic_mam_join_key(first_word)
            ) == _fold_qamats_qatan(_phonetic_mam_join_key(second_word)), payload
            assert (
                _jta_syllables(first["jta"])[1] == _jta_syllables(second["jta"])[1]
            ), payload
    return branches


def _select_qamats_reading(node: object) -> object:
    """Project each qamats-variant row onto its qamats-dal reading for the MAM census.

    The public Phonetic MAM page presents the two phonetic readings in one row for one MAM
    chanted-word sequence. The census counts that sequence once. The marker is retained as an
    event so context handling still knows that an annotation stood between neighboring entries.

    Ben's decision, 2026-09-08: select exactly one of the מ:קמץ parameters, ד or ס, never
    both. The choice need not receive a separate effect analysis; selecting ד here is
    acceptable, analogous to selecting cant-alef for dual-cantillation templates.
    """
    if not isinstance(node, list):
        return node
    if node and node[0] == "cb":
        out = ["cb"]
        for payload in node[1:]:
            if _compound_marker(payload) == _CB_QAMATS_MARKER:
                first_branch = _qamats_variant_branches(payload)[0]
                out.append(
                    [
                        "cb",
                        [[_CB_QAMATS_MARKER]],
                        _select_qamats_reading(first_branch),
                    ]
                )
            else:
                out.append(_select_qamats_reading(payload))
        return out
    return [_select_qamats_reading(one) for one in node]


def _qamats_variant_facts(node: object) -> Counter:
    """Counts that prove qamats alternatives are rows, not additional MAM words."""
    facts = Counter()
    if not isinstance(node, list):
        return facts
    if node and node[0] == "cb":
        for payload in node[1:]:
            if _compound_marker(payload) == _CB_QAMATS_MARKER:
                branches = _qamats_variant_branches(payload)
                entries_by_branch = []
                for branch in branches:
                    entries: list[dict] = []
                    _chanted_words(branch, entries)
                    entries_by_branch.append(entries)
                facts["rows"] += 1
                facts["source_entries"] += sum(map(len, entries_by_branch))
                facts["mam_chanted_words"] += len(entries_by_branch[0])
                facts["duplicate_entries"] += sum(
                    len(entries) for entries in entries_by_branch[1:]
                )
            else:
                facts.update(_qamats_variant_facts(payload))
        return facts
    for item in node:
        facts.update(_qamats_variant_facts(item))
    return facts


def _qamats_variant_grouping_differences(node: object) -> list[dict]:
    """Qamats rows whose two readings divide the atoms into different chanted words."""
    out = []
    if not isinstance(node, list):
        return out
    if node and node[0] == "cb":
        for payload in node[1:]:
            if _compound_marker(payload) == _CB_QAMATS_MARKER:
                branches = _qamats_variant_branches(payload)
                entries_by_branch = []
                for branch in branches:
                    entries: list[dict] = []
                    _chanted_words(branch, entries)
                    entries_by_branch.append(entries)
                if len(entries_by_branch[0]) != len(entries_by_branch[1]):
                    out.append(
                        {
                            "qamats-dal": [
                                entry["fva"].split(" ")[0]
                                for entry in entries_by_branch[0]
                            ],
                            "qamats-sam": [
                                entry["fva"].split(" ")[0]
                                for entry in entries_by_branch[1]
                            ],
                        }
                    )
            else:
                out.extend(_qamats_variant_grouping_differences(payload))
        return out
    for item in node:
        out.extend(_qamats_variant_grouping_differences(item))
    return out


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
            word = _phonetic_mam_scanner_word(event["fva"].split(" ")[0])
            entries.append(event)
            fragments.append(cwa.Frag(word, uni_to_marks.word_to_marks(word), True))
        elif event == _PHONETIC_MAM_PASOLEG:
            assert fragments, (bb, chnu, vrnu)
            prior = fragments[-1]
            fragments[-1] = cwa.Frag(prior.text, prior.marks + PASOLEG, True)
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
    """The paseq/legarmeh glyphs between two entries, with annotations omitted.

    Phonetic MAM's source token does not distinguish paseq from legarmeh. MAM-simple supplies
    that category later. Setuma and petuxa markers describe layout, while a qamats marker
    introduces alternative phonetic readings of one MAM template row; none of those
    three annotation kinds is punctuation between the chanted words. Anything else is a new
    source shape and remains fatal.
    """
    punctuation = []
    for item in material:
        if item == _PHONETIC_MAM_PASOLEG:
            punctuation.append(PASOLEG)
        elif item not in _PHONETIC_MAM_NON_PUNCTUATION_MATERIAL:
            raise SurveyProblem(
                f"{bcv} {chanted_word!r}: unclassified material before the next chanted"
                f" word: {material!r}"
            )
    return tuple(punctuation)


_DUALCANT_MARKER = "cb-dualcant"

CANT_ALEF = "cant-alef"

CANT_BET = "cant-bet"

_CANTILLATION_BRANCH_INDEX = {CANT_ALEF: 0, CANT_BET: 1}


def _has_dual_cantillation(node: object) -> bool:
    """Whether the numbered verse has Phonetic MAM's dual-cantillation bracket.

    Structural rather than a list of references: both strands' chanted words reach one entry
    list. The two Decalogues have most of the dual-cantillation numbered verses, and Genesis
    35:22 has the other one. A last entry need not have sof pasuq: the numbered-verse boundary
    need not end both chanted verses.
    """
    if isinstance(node, str):
        return node == _DUALCANT_MARKER
    if isinstance(node, list):
        return any(_has_dual_cantillation(sub) for sub in node)
    if isinstance(node, dict):
        _validate_phonetic_word(node)
        return False
    if node is None:
        return False
    raise TypeError(f"unclassified Phonetic MAM node: {node!r}")


def _select_cantillation_strand(node: object, cantillation: str) -> object:
    """Replace each dual span with its cant-alef or cant-bet cantillation strand.

    Phonetic MAM's source writes the alef branch before the bet branch when it emits a
    ``cb-dualcant`` structure. The explicit names here keep that ordering from becoming an
    anonymous positional convention in this census.
    """
    branch_index = _CANTILLATION_BRANCH_INDEX[cantillation]
    if isinstance(node, dict):
        _validate_phonetic_word(node)
        return node
    if isinstance(node, str):
        return node
    if node is None:
        return None
    if not isinstance(node, list):
        raise TypeError(f"unclassified Phonetic MAM node: {node!r}")
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
                    _chanted_words(_select_qamats_reading(branch), entries)
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
        first = tuple(
            _phonetic_mam_join_key(one["fva"].split(" ")[0]) for one in group[0]
        )
        second = tuple(
            _phonetic_mam_join_key(one["fva"].split(" ")[0]) for one in group[1]
        )
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
# one it stands for: the accents, the masora circle, meteg, rafe, the punctuation and puncta
# that can sit inside a chanted word, and the two invisibles.  What is left is letters and
# points -- which is what the two sides have to agree on, the marks this survey is about being
# exactly what it must not match on.  The same set
# ``test_final_stress_vs_phonetic_mam._NOT_IN_THE_JOIN_KEY`` drops, and written as numeric
# escapes for the same two reasons: a character class wants range endpoints, and a bare
# combining mark in a literal is unreadable.
_NOT_IN_THE_JOIN_KEY = re.compile(
    "[\u0591-\u05af\u05bd\u05bf\u05c0\u05c3-\u05c5\u034f\ufb1e]"
)

_LEGACY_PHONETIC_MAM_ANNOTATIONS = (
    hpo.SHEVA + hpu.MCIRC,
    hpo.DAGOMOSD + hpu.UPDOT,
)


def _fold_phonetic_mam_annotations(word: str) -> str:
    """Fold Unicode 18 Phonetic MAM annotations to their generic points."""
    if any(pair in word for pair in _LEGACY_PHONETIC_MAM_ANNOTATIONS):
        raise SurveyProblem("legacy Phonetic MAM annotation pair")
    return word.replace(hpo.SHEVA_NA, hpo.SHEVA).replace(hpo.DAGESH_XAZAQ, hpo.DAGOMOSD)


def _phonetic_mam_scanner_word(word: str) -> str:
    """Give the accent scanner the same mark stream as the retired annotations did.

    ``uni_to_marks.word_to_marks`` dropped the old U+05B0 and U+05AF pair but retained the
    old pair's U+05C4 as a punctum while dropping its U+05BC.  Preserve that established
    scanner input without accepting or reconstructing either retired source pair.
    """
    _fold_phonetic_mam_annotations(word)
    return word.replace(hpo.SHEVA_NA, hpo.SHEVA).replace(hpo.DAGESH_XAZAQ, hpu.UPDOT)


def _phonetic_mam_join_key(word: str) -> str:
    """``word`` reduced to what both texts must agree on: letters, points, and the maqafs.

    Phonetic MAM's tilde for MAM's gray maqaf is folded onto the maqaf it stands for, so a
    compound joined by one matches the compound MAM has.
    """
    generic = _fold_phonetic_mam_annotations(word)
    return _NOT_IN_THE_JOIN_KEY.sub("", generic).replace(hpu.NU_GMAQ, MAQAF)


def _mam_join_key(word: str) -> str:
    """A MAM form reduced without treating genuine extraordinary dots as annotations."""
    return _NOT_IN_THE_JOIN_KEY.sub("", word).replace(hpu.NU_GMAQ, MAQAF)


def _parse(word: str, jta: str) -> dict:
    """Everything the classification of one chanted word's U+05BDs rests on.

    Raises ``SurveyProblem`` where the two sides' syllable counts disagree, which is the check
    that makes reading a syllable off the ``jta`` and a nucleus off the Hebrew safe.
    """
    letters = _letters(_fold_phonetic_mam_annotations(word))
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


def _stress_letter_accent_from_parsed(*, bcv: str, parsed: dict) -> str:
    """The one accent on the primary-stress letter of a parsed chanted word.

    The stress letter is the initial Hebrew letter of the nucleus whose Phonetic MAM ``jta``
    syllable has ``!``.  A meteg later in the chanted word does not participate in the selection.
    """
    accents = _stress_letter_accents(parsed)
    if len(accents) != 1:
        raise SurveyProblem(
            f"{bcv}: the stress letter has {len(accents)} accents, not one"
        )
    return accents[0]


def _stress_letter_accents(parsed: dict) -> list[str]:
    """The accents on the primary-stress letter of a parsed chanted word."""
    stress_letter_index, _stress_vowel = parsed["nuclei"][parsed["stressed"]]
    stress_letter_marks = parsed["letters"][stress_letter_index][1]
    return [mark for mark in stress_letter_marks if is_accent(mark)]


def _stress_syllable_has_conjunctive_accent(system: str, parsed: dict) -> bool:
    """Whether the primary-stress letter has exactly one regular conjunctive accent."""
    accents = _stress_letter_accents(parsed)
    return len(accents) == 1 and accents[0] in _STRESS_ACCENT_CONJUNCTIVES[system]


def _stress_letter_accent(record: dict) -> str:
    """The one accent on the legacy table's exact stress letter for ``record``."""
    return _stress_letter_accent_from_parsed(
        bcv=record["bcv"], parsed=_parse(record["chanted_word"], record["jta"])
    )


def _fold_qamats_qatan(key: str) -> str:
    """``key`` with U+05C7 read as an ordinary qamats.

    MAM spells qamats qatan U+05C7 and Phonetic MAM does not always agree with it about
    which qamats a chanted word has -- Job 11:17 is where the two spellings stand side by side, as a
    qamats note offering both.  A fold is tried only after the unfolded key has failed, and
    a record that needed it says so in ``matched_by``.
    """
    return key.replace(hpo.QAMATS_Q, hpo.QAMATS)


def _consonant_key(text: str) -> str:
    """The Hebrew letters of a chanted word, ignoring vowels, accents, and punctuation."""
    return re.sub("[\u0591-\u05c9\u034f]", "", text)


def _atom_keys(word: str) -> tuple[str, ...]:
    """The consonant keys of a chanted word's atoms, in their written order."""
    return tuple(
        _consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    )
