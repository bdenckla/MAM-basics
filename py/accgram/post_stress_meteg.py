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
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from accgram import maqaf_nonfinal_accents as mna
from accgram import poetic_filter
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.uni_to_marks import is_accent
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import provenance
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

METEG = hpo.MTGOSLQ
SOF_PASUQ = hpu.SOPA
MAQAF = hpu.MAQ

SILLUQ_RULE = (
    "A U+05BD is the silluq when it is in the stressed syllable of a chanted word that"
    " has sof pasuq. Both conditions are required and there is no third: the sof pasuq"
    " is what makes the chanted word the last of its chanted verse, so nothing here rests on"
    " an entry's position in a list."
)

# Phonetic MAM spells MAM's gray maqaf as a tilde and its ordinary maqaf as U+05BE; both are
# atom boundaries inside one chanted word, and neither is a nucleus.
_BOUNDARIES = frozenset((MAQAF, hpu.NU_GMAQ))

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

SYSTEM_PROSE = "prose verses"
SYSTEM_POETIC = "poetic verses"

# The three types the page attributes to Yeivin and Breuer, each keyed on a mechanical
# signature and never on a verse reference.  A post-stress meteg meeting none of them is
# recorded as unclassified rather than pushed into the nearest.
TYPE_GUTTURAL = "guttural at the end of the chanted word"
TYPE_CLOSED_TSERE = "closed syllable with tsere"
TYPE_OPEN = "open syllable"
TYPE_UNCLASSIFIED = "none of the three"

_TYPES = (TYPE_CLOSED_TSERE, TYPE_GUTTURAL, TYPE_OPEN, TYPE_UNCLASSIFIED)

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


def _syllable_is_open(syllable: str) -> bool:
    return syllable[-1] in _JTA_VOWELS


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


def _structural_type(*, closes_on_a_guttural: bool, is_open: bool, vowel: str) -> str:
    """Which of the three source-anchored types a post-stress meteg's syllable meets.

    Mechanical, off the syllable Phonetic MAM divided and the letters and points MAM has:

    * an open syllable is ITM §332 and CoS Ch. 8 type (j), the קוּמִי rule;
    * a closed syllable at the end of a chanted word whose last letter is a guttural is ITM
      §354 and CoS Ch. 8 type (b) -- which is where a furtive patax lands; and
    * a closed syllable whose nucleus is a ṣere is ITM §338, and the ṣere case of CoS Ch. 8
      type (a), whose scope is the big vowels rather than the ṣere alone.

    Anything else -- a closed syllable with some other vowel, the segol of וַיֹּאמֶר above all
    -- is left unclassified and stays visible as itself.

    OPENNESS IS ASKED FIRST, and the order is the rule rather than a tidying: a final ה is a
    mater in פַּדֶּנָה, whose last syllable is open, and a guttural in וְנֹגַהּ, whose last
    syllable the same letter closes.  Asking about the letter first files פַּדֶּנָה under §354,
    where both books put it under §332 and type (j) by name.
    """
    if is_open:
        return TYPE_OPEN
    if closes_on_a_guttural:
        return TYPE_GUTTURAL
    if vowel == hpo.TSERE:
        return TYPE_CLOSED_TSERE
    return TYPE_UNCLASSIFIED


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
) -> dict:
    """One classified U+05BD, with everything the page's tables and counts derive from."""
    nuclei = parsed["nuclei"]
    letters = parsed["letters"]
    syllables = parsed["syllables"]
    syllable = syllables[syllable_index]
    is_last_syllable = syllable_index == len(syllables) - 1
    is_open = _syllable_is_open(syllable)
    vowel = nuclei[syllable_index][1]
    stress_letter = nuclei[parsed["stressed"]][0]
    stress_accents = [mark for mark in letters[stress_letter][1] if is_accent(mark)]
    closes_on_a_guttural = is_last_syllable and letters[-1][0] in _GUTTURAL_HOSTS
    return {
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
        "closes_on_a_guttural": closes_on_a_guttural,
        "has_sof_pasuq": parsed["has_sof_pasuq"],
        "accent_on_the_stressed_letter": (
            ", ".join(_accent_name(one) for one in stress_accents)
            if stress_accents
            else "(none)"
        ),
        "shares_its_letter_with": [_accent_name(one) for one in accents_here],
        "structural_type": _structural_type(
            closes_on_a_guttural=closes_on_a_guttural, is_open=is_open, vowel=vowel
        ),
        "atom": 1 + sum(1 for one in letters[:letter_index] if one[2]),
    }


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


def _scan(phon_dir: Path, cantillation: str = CANT_ALEF) -> dict:
    """Every U+05BD of the Phonetic MAM standard set in one cantillation strand."""
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
    }
    bb_of_stem = _bb_of_stem()
    for path in sorted(phon_dir.glob("*.json")):
        bb = bb_of_stem[path.stem]
        data = json.loads(path.read_text(encoding="utf-8"))
        for vkey, verse in data.items():
            chnu, vrnu = (int(one) for one in _VERSE_KEY.match(vkey).groups())
            dual = _has_dual_cantillation(verse)
            _one_verse(
                f"{bb}{chnu}:{vrnu}",
                bb,
                chnu,
                vrnu,
                _select_cantillation_strand(verse, cantillation),
                found,
                dual_cantillation=dual,
                dual_facts=_dual_cantillation_facts(verse) if dual else None,
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
    dual_cantillation: bool | None = None,
    dual_facts: dict | None = None,
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
    entries: list[dict] = []
    _chanted_words(verse, entries)
    usable = [one for one in entries if one.get("jta") and one.get("fva")]
    found["entries_without_jta_or_fva"] += len(entries) - len(usable)
    if not usable:
        return
    if dual:
        found["dual_cantillation_chanted_words"][bcv] = [
            one["fva"].split(" ")[0] for one in usable
        ]
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
    for index, entry in enumerate(usable):
        word = entry["fva"].split(" ")[0]
        jta = entry["jta"]
        following_chanted_word = (
            usable[index + 1]["fva"].split(" ")[0] if index + 1 < len(usable) else None
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
        _classify_one_word(
            bcv=bcv,
            system=system,
            word=word,
            jta=jta,
            parsed=parsed,
            found=found,
            before_qere=entry.get("before_qfikq"),
            following_chanted_word=following_chanted_word,
        )
    found["metegs_by_verse"][bcv] = metegs


# The verses the page names outside its tables, whose chanted words it therefore has to show
# as MAM has them TODAY rather than as the surveyed snapshot has them.  Isaiah 23:12 is
# where the two differ -- suggestion M23 added a meteg there after the snapshot was taken --
# and 1 Samuel 17:5 is the post-silluq case, where the page's claim is about what MAM lacks.
# Named here rather than in the page module so the form is lifted from the corpus at
# generation time and reaches the page through the tracked JSON, as every other form does.
_FOCUS_VERSES = ("is23:12", "1s17:5")


def _mam_words_by_bcv() -> dict[str, list[str]]:
    """MAM-simple's chanted words per verse, in MAM's versification.

    MAM's numbering rather than the BHS one this repo's other surveys read, because Phonetic
    MAM numbers its verses MAM's way; ``test_final_stress_vs_phonetic_mam._measured`` reaches
    for the same tree for the same reason.
    """
    from accgram import mam_simple_verse

    mam_dir = paths.require_mam_simple_vtrad_mam_dir()
    return mna.mam_words(mam_simple_verse.mam_simple_refs(mam_dir), mam_dir)


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


def _following_mam_form(record: dict, words: list[str]) -> str | None:
    """The MAM form of ``record``'s next chanted word, if the pair resolves uniquely.

    The page's open-syllable and guttural examples need the following chanted word to show
    the condition that classifies them. A form is shown only after the complete adjacent
    pair matches MAM, so both Hebrew forms remain lifted from MAM rather than one being a
    Phonetic-MAM fallback.
    """
    following = record["following_chanted_word"]
    if following is None:
        return None
    next_record = {"chanted_word": following}
    candidates = []
    for index, word in enumerate(words[:-1]):
        current_matches, _current_matched_by = _matching_mam_words(record, [word])
        next_matches, _next_matched_by = _matching_mam_words(
            next_record, [words[index + 1]]
        )
        if current_matches and next_matches:
            candidates.extend(next_matches)
    settled, _settled_by = _settle(candidates, following)
    return settled


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
        record["following_mam_form"] = (
            _following_mam_form(record, words_by_bcv.get(record["bcv"], []))
            if settled is not None
            else None
        )
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


def _dually_cantillated_passage_counts(found: dict) -> dict[str, int]:
    """The three appendix counts restricted to the numbered verses with two strands."""
    dual_bcv = found["dual_cant_verses"]
    return {
        "chanted words checked": sum(
            found["checked_chanted_words_by_bcv"][bcv] for bcv in dual_bcv
        ),
        "meteg before the stressed syllable": sum(
            one["bcv"] in dual_bcv for one in found["pre_stress"]
        ),
        "meteg after the stressed syllable": sum(
            one["bcv"] in dual_bcv for one in found["post_stress"]
        ),
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
    found_alef: dict, found_bet: dict, words_by_bcv: dict[str, list[str]]
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
    return {
        "bcv": bcv,
        CANT_ALEF: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                alef_counterparts, words_by_bcv, bcv
            )
        },
        CANT_BET: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                [bet_record["chanted_word"]], words_by_bcv, bcv
            )
        },
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
    assert found["dual_cant_verses"] == found_bet["dual_cant_verses"]
    words_by_bcv = _mam_words_by_bcv()
    unjoined = _attach_mam_forms(
        found["post_stress"] + found["in_stressed"] + found["overlaps"], words_by_bcv
    )
    problems = _problems(found) + _problems(found_bet)
    if problems:
        raise SurveyProblem("; ".join(problems))
    counts = found["counts"]
    post_stress = found["post_stress"]
    by_type = Counter((one["system"], one["structural_type"]) for one in post_stress)
    by_accent = Counter(
        (one["system"], one["accent_on_the_stressed_letter"]) for one in post_stress
    )
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
            "dually_cantillated_passage_counts": {
                CANT_ALEF: _dually_cantillated_passage_counts(found),
                CANT_BET: _dually_cantillated_passage_counts(found_bet),
            },
            "meteg_before_stress_difference": _meteg_before_stress_difference(
                found, found_bet, words_by_bcv
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
        "post_stress_by_accent_on_the_stressed_letter": {
            system: dict(
                sorted(
                    (
                        (accent, n)
                        for (one_system, accent), n in by_accent.items()
                        if one_system == system
                    ),
                    key=lambda pair: (-pair[1], pair[0]),
                )
            )
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
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
