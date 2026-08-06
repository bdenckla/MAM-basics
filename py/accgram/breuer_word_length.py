r"""Survey: does Breuer's long/short/tiny predict how a two-chanted-word zaqef unit is accented?

THE RULE.  Breuer, *The Cantillation of Scripture*, Ch. 4 §7
(``../masorah-books/books/cos/md-export-of-docx/C04-S001.md``): a simple unit comprising the
whole realm of a zaqef has a mafsik on its first chanted word if the zaqef's chanted word is
long, and a servant if it is short.  §8 adds that the exceptions are few and are commoner when
the first chanted word is tiny, and that in the opposite direction there are hardly any.  §12
(``C04-S011.md``) marks this rule consistent, against the merely optional one of §9.  Yeivin,
*Introduction to the Tiberian Masorah* §226 (``books/itm/md-export-of-docx/N0221.md``), states
it with the same minimal pairs -- Gen 21:24 ויאמר אברהם against Gen 15:3 ויאמר אברם, Num 16:28
בזאת תדעון against Ex 7:17 בזאת תדע -- and calls the exceptions many.  Which of the two is
right about the exceptions is the thing this survey measures.

A SIMPLE UNIT is one both of whose parts are chanted words rather than units (CoS Ch. 1 §7),
so the measured set is the zaqef realms spanning exactly two chanted words.  A realm is an
outermost zaqef-labelled node of a committed prose parse tree: a zaqef node inside another
zaqef node governs part of that zaqef's realm rather than the whole of it.

TWO CHANTED WORDS, NOT TWO LEAVES, and the difference is not small.  A tree leaf is an accent
TOKEN, and a chanted word can carry two of them -- munaḥ-zaqef above all, ITM §219's fourth
variant of the zaqef melody.  Counting leaves puts 299 realms in the set whose two accents
stand on ONE chanted word, and leaves out 342 whose two chanted words carry three or more
tokens between them.  Both counts are in the JSON, because 5,948-by-leaf-count is the figure
this survey was first sized against and the two must not be confused.

SYLLABLES ARE BREUER'S, WHICH ARE THE FAT ONES, and he says so outright rather than leaving it
to be inferred: "A consonant vocalized with a *sheva na'* does not form a syllable, but rather
joins the syllable that follows it; therefore לְהַבְדִּיל, שָׁרְצוּ, וּמָלְאוּ, לְמַאֲכָל -- all these are words
consisting of two syllables" (Instructions for the Reader, ``C00-S000.md``, page [xvi] of the
scan).  His *sheva na'* covers a simple mobile shewa, every ḥataf, AND a connective vav pointed
with shuruq that is not itself followed by a shewa.  The thin count -- one syllable per vowel
however short -- is computed beside it, and reported, because the two answer differently: on
the thin count four of Breuer's six SHORT examples come out long and three of his six TINY
examples come out short.

THE ORACLE IS PHONETIC MAM, al-hatorah's ``io/a01-phonetic-std-set``, whose ``jta`` field marks
the syllable boundaries and the stress.  Issue wlc-utils#48 asks for syllabification, open and
closed syllables and vowel length derived from the pointing, and says to reuse that output
rather than build one; this is that second path.  ``jta`` alone will not do for Breuer's big
and small vowels -- it writes both patax and qamats gadol ``a``, and both qubuts and shuruq
``u`` -- so the ``udl`` field, which keeps them apart, is lined up against it nucleus by
nucleus.  The alphabets are read off al-hatorah's ``py/aht_phon/jtech_ascii.py`` and
``deep_latin.py``.

THE CORPUS MISMATCH is the design hazard and is reported rather than smoothed over.  The parse
trees are over WLC 4.22, a transcription of the Leningrad Codex; Phonetic MAM is MAM.  Verses
are aligned by reference through MAM-basics' own BHS-to-MAM verse map (``py_misc/vtrad_data``'s
declared spans), chanted words by index with the letters checked and a by-letters fallback, and
a unit that will not align is COUNTED AND NAMED, never dropped quietly.  Where the two texts
have different accents on either chanted word the unit is flagged, and the cross-tabulation is
given twice: over everything, and over the units where MAM has the same accents.  The second is
the one a claim about the accentuation takes, MAM being the consensus text and WLC a
transcription of one manuscript.

WRITES TO ``.novc/``, not to ``out/``.  This is a measurement, not a generated artifact of the
corpus, and nothing here regenerates anything committed.  Run via
``main_accgram.py survey-breuer-zaqef-units``.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from accgram import chanted_word_accents as cwa
from accgram import maqaf_nonfinal_accents as mna
from accgram.prose_scanner import HasLegarmeh, scan_accents
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import provenance
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

import wlc_paths

# ---------------------------------------------------------------------------
# The two phonetic alphabets, read off al-hatorah's py/aht_phon.
# ---------------------------------------------------------------------------

# jta nucleus characters (jtech_ascii.py's _JTECH_SEFARAD_FROM_UDL).  No consonant maps to any
# of them, so a jta syllable holds exactly one and that one is its nucleus.
JTA_VOWELS = frozenset("^680iEeaoOuI")
JTA_HATAF = frozenset("680")  # hataf segol, hataf patax, hataf qamats
JTA_REDUCED = JTA_HATAF | frozenset(
    "^"
)  # Breuer's sheva na': a simple one, and every hataf

# udl nucleus characters (deep_latin.py), written as named escapes and \u form because a bare
# combining or exotic literal is unreadable in source.
SHEVA_NA = "ə"  # LATIN SMALL LETTER SCHWA
VARIKA_CW = "^"
VARIKA_AW = "Ə"  # LATIN CAPITAL LETTER SCHWA
XSEGOL, XPATAX, XQAMATS = "e", "a", "\U0001d4b6"  # MATHEMATICAL SCRIPT SMALL A
XIRIQ_Q, TSERE, SEGOL_V, PATAX = "i", "ë", "E", "A"
QAMATS_G = "\U0001d49c"  # MATHEMATICAL SCRIPT CAPITAL A
QAMATS_Q = "ℴ"  # SCRIPT SMALL O
XOLAM_HASER, QUBUTS, XIRIQ_G = "o", "u", "ì"
VAV_XOLAM, SHURUQ = "O", "U"
SHURUQ_DIPH, XOLAM_DIPH, ALEF_SHURUQ = "Ù", "Ò", "Ú"
FPP_HE, FPP_XET, FPP_AYIN = "ḣ", "ẋ", "_"  # the furtive patax pairs

# SHEVA_NAX ':' and SHEVA_AMB ';' are deliberately NOT here.  Both translate to the empty
# string in jta, so neither is a nucleus, and counting them would throw the udl nuclei out of
# step with the jta syllables they are lined up against.
UDL_NUCLEI = frozenset(
    SHEVA_NA
    + VARIKA_CW
    + VARIKA_AW
    + XSEGOL
    + XPATAX
    + XQAMATS
    + XIRIQ_Q
    + TSERE
    + SEGOL_V
    + PATAX
    + QAMATS_G
    + QAMATS_Q
    + XOLAM_HASER
    + QUBUTS
    + XIRIQ_G
    + VAV_XOLAM
    + SHURUQ
    + SHURUQ_DIPH
    + XOLAM_DIPH
    + ALEF_SHURUQ
    + FPP_HE
    + FPP_XET
    + FPP_AYIN
)

# The classical big/small split Breuer's criteria 2 and 3 turn on: qamats gadol, tsere, hiriq
# gadol, holam and shuruq are big; patax, segol, hiriq qatan, qamats qatan and qubuts small.
UDL_BIG = frozenset(
    {
        TSERE,
        QAMATS_G,
        XIRIQ_G,
        VAV_XOLAM,
        XOLAM_HASER,
        SHURUQ,
        SHURUQ_DIPH,
        XOLAM_DIPH,
        ALEF_SHURUQ,
    }
)
UDL_SMALL = frozenset(
    {SEGOL_V, PATAX, QAMATS_Q, XIRIQ_Q, QUBUTS, FPP_HE, FPP_XET, FPP_AYIN}
)
UDL_HATAF_TYPE = {XSEGOL: "segol", XPATAX: "patax", XQAMATS: "qamats"}
UDL_VOWEL_TYPE = {
    SEGOL_V: "segol",
    TSERE: "segol",
    PATAX: "patax",
    QAMATS_G: "qamats",
    QAMATS_Q: "qamats",
    XIRIQ_Q: "hiriq",
    XIRIQ_G: "hiriq",
    QUBUTS: "shuruq",
    SHURUQ: "shuruq",
    VAV_XOLAM: "holam",
    XOLAM_HASER: "holam",
}
UDL_NAME = {
    SHEVA_NA: "sheva na",
    VARIKA_CW: "varika",
    VARIKA_AW: "varika",
    XSEGOL: "hataf segol",
    XPATAX: "hataf patax",
    XQAMATS: "hataf qamats",
    XIRIQ_Q: "hiriq qatan",
    TSERE: "tsere",
    SEGOL_V: "segol",
    PATAX: "patax",
    QAMATS_G: "qamats gadol",
    QAMATS_Q: "qamats qatan",
    XOLAM_HASER: "holam haser",
    QUBUTS: "qubuts",
    XIRIQ_G: "hiriq gadol",
    VAV_XOLAM: "holam male",
    SHURUQ: "shuruq",
    SHURUQ_DIPH: "shuruq",
    XOLAM_DIPH: "holam",
    ALEF_SHURUQ: "shuruq",
    FPP_HE: "furtive patax",
    FPP_XET: "furtive patax",
    FPP_AYIN: "furtive patax",
}

# ---------------------------------------------------------------------------
# Syllables
# ---------------------------------------------------------------------------


class Syllable:
    """One jta syllable of a chanted word, with the udl nucleus that says which vowel it is."""

    __slots__ = ("jta", "vowel", "udl", "stressed", "closed")

    def __init__(self, jta: str, vowel: str, stressed: bool, closed: bool) -> None:
        self.jta, self.vowel, self.stressed, self.closed = jta, vowel, stressed, closed
        self.udl: str | None = None

    @property
    def is_reduced(self) -> bool:
        return self.vowel in JTA_REDUCED

    @property
    def is_hataf(self) -> bool:
        return self.vowel in JTA_HATAF


def syllabify(jta: str, udl: str) -> list[Syllable]:
    """Phonetic MAM's syllables for one chanted word, each with its true vowel.

    ``jta`` carries the syllable boundaries -- ``.`` within an atom, ``-`` between the atoms of
    a maqaf compound -- and the stress, ``!`` immediately before the stressed syllable.  What it
    does not carry is the difference between patax and qamats gadol, or between qubuts and
    shuruq, and Breuer's criteria 2 and 3 turn on exactly that.  ``udl`` keeps them apart, and
    jta is generated from udl nucleus by nucleus, so the two hold the same nuclei in the same
    order and are lined up here.  A count that does not line up RAISES: a silent mis-pairing
    would attribute the wrong vowel to the syllable the verdict is read off.
    """
    syllables: list[Syllable] = []
    for piece in re.split(r"[.\-]", jta):
        if not piece:
            continue
        stressed = piece.startswith("!")
        body = piece[1:] if stressed else piece
        vowels = [c for c in body if c in JTA_VOWELS]
        assert len(vowels) == 1, f"{jta!r}: syllable {piece!r} has {len(vowels)} nuclei"
        after = body[body.index(vowels[0]) + 1 :]
        syllables.append(Syllable(body, vowels[0], stressed, bool(after)))
    nuclei = [c for c in udl if c in UDL_NUCLEI]
    assert len(nuclei) == len(
        syllables
    ), f"{jta!r} / {udl!r}: {len(nuclei)} udl nuclei against {len(syllables)} syllables"
    for syllable, nucleus in zip(syllables, nuclei):
        syllable.udl = nucleus
    assert (
        sum(1 for s in syllables if s.stressed) == 1
    ), f"{jta!r}: stress not marked once"
    return syllables


def _is_connective_vav_shuruq(syllables: list[Syllable]) -> bool:
    """A word-initial vav pointed with shuruq -- Breuer's connective vav (C00-S000.md:281)."""
    return bool(syllables) and syllables[0].udl == SHURUQ and syllables[0].jta == "u"


def fat_groups(syllables: list[Syllable], breuer_vav: bool) -> list[list[Syllable]]:
    """Breuer's syllables: a *sheva na'* joins the syllable after it (C00-S000.md:289).

    Each group is a run of jta syllables ending in the one full vowel that heads it, so the
    number of groups is Breuer's syllable count.  ``breuer_vav`` adds the rest of his *sheva
    na'* (C00-S000.md:281): a connective vav pointed with shuruq counts as one too, unless a
    shewa follows it.  That clause is what makes וּמִגְדָּל short, as his own list has it, and
    וּמָלְאוּ a word of two syllables.
    """
    reduced = [s.is_reduced for s in syllables]
    if (
        breuer_vav
        and _is_connective_vav_shuruq(syllables)
        and len(syllables) > 1
        and not syllables[1].is_reduced
    ):
        reduced[0] = True
    groups: list[list[Syllable]] = []
    pending: list[Syllable] = []
    for syllable, is_reduced in zip(syllables, reduced):
        pending.append(syllable)
        if not is_reduced:
            groups.append(pending)
            pending = []
    if (
        pending
    ):  # a word ending in a reduced vowel, with nothing left to join forward to
        groups.append(pending)
    return groups


# Breuer's three ways of being long, Instructions for the Reader (C00-S000.md:313).  The fourth
# key ``classify`` fills is not one of them: it records what criterion 3 would say with its
# "not of the same type as the vowel that precedes it" restriction dropped, which is the one
# reading his own example בַּעֲלֵי needs and his wording does not license.
LONG_CRITERIA = ("two syllables", "big vowel", "small vowel before hataf")
CRITERION_3_ANY_TYPE = "small vowel before hataf (any type)"
CRITERION_2_ANY_SYLLABLE = "big vowel (any syllable)"


def classify(
    syllables: list[Syllable], groups: list[list[Syllable]]
) -> tuple[str, dict, str | None]:
    """long / short / tiny, the criteria that fired, and the vowel the word is accented after.

    Tiny  -- accentuated at its first syllable.
    Long  -- (1) accentuated after at least two syllables; or (2) after a big vowel that is in
             a closed syllable or stands before a shewa; or (3) after a small vowel in an open
             syllable before a ḥataf not of the same type as the vowel that precedes it.
    Short -- what is left: not long, accentuated at its second syllable.

    Criteria 2 and 3 ask about the syllable the word is accentuated AFTER, which is the head of
    the last group before the stressed one.  They can decide nothing where there are two such
    groups, since two already satisfy criterion 1, so "the" group is never ambiguous.
    """
    stressed_group = next(i for i, g in enumerate(groups) if any(s.stressed for s in g))
    criteria = {c: False for c in LONG_CRITERIA}
    criteria[CRITERION_3_ANY_TYPE] = False
    criteria[CRITERION_2_ANY_SYLLABLE] = False
    criteria["two syllables"] = stressed_group >= 2
    head_vowel = None
    if stressed_group >= 1:
        head = groups[stressed_group - 1][-1]
        lead = [s for s in groups[stressed_group] if s.is_reduced]
        head_vowel = head.udl
        big, small = head.udl in UDL_BIG, head.udl in UDL_SMALL
        if (
            _is_connective_vav_shuruq(syllables)
            and stressed_group == 1
            and len(groups[0]) == 1
            and lead
        ):
            # C00-S000.md:285 -- a connective vav with shuruq standing before a shewa is small.
            big, small = False, True
        criteria[CRITERION_2_ANY_SYLLABLE] = big
        if big and (head.closed or lead):
            criteria["big vowel"] = True
        if small and not head.closed and lead and lead[0].is_hataf:
            criteria[CRITERION_3_ANY_TYPE] = True
            if UDL_HATAF_TYPE[lead[0].udl] != UDL_VOWEL_TYPE.get(head.udl):
                criteria["small vowel before hataf"] = True
    if stressed_group == 0:
        return "tiny", criteria, head_vowel
    if any(criteria[c] for c in LONG_CRITERIA):
        return "long", criteria, head_vowel
    return "short", criteria, head_vowel


# The three syllable counts, and what each is.  ``thin`` is Phonetic MAM's own, one syllable
# per vowel however short; ``fat`` is the task's formulation of Breuer's, every shewa or ḥataf
# syllable merged forward; ``fat_breuer_vav`` is Breuer's in full, with the connective vav of
# C00-S000.md:281 merged forward as well.
CONVENTIONS = ("thin", "fat", "fat_breuer_vav")


def analyse(jta: str, udl: str) -> dict:
    """Every count and every verdict for one chanted word."""
    syllables = syllabify(jta, udl)
    out: dict = {"jta": jta, "syllables_thin": len(syllables)}
    out["before_stress_thin"] = next(i for i, s in enumerate(syllables) if s.stressed)
    for name, groups in (
        ("thin", [[s] for s in syllables]),
        ("fat", fat_groups(syllables, breuer_vav=False)),
        ("fat_breuer_vav", fat_groups(syllables, breuer_vav=True)),
    ):
        verdict, criteria, head = classify(syllables, groups)
        out[name] = {
            "verdict": verdict,
            "syllables": len(groups),
            "before_stress": next(
                i for i, g in enumerate(groups) if any(s.stressed for s in g)
            ),
            "criteria": criteria,
            "accented_after": UDL_NAME.get(head),
        }
    return out


# ---------------------------------------------------------------------------
# Phonetic MAM
# ---------------------------------------------------------------------------

# Phonetic MAM's verse keys name the book too -- G1:1, E20:2, 1S12:3 -- and the book part can
# itself start with a digit, so the chapter and verse come off the END.
_VERSE_KEY = re.compile(r"^.+?(\d+):(\d+)$")
# Numeric escapes because a character class wants range endpoints and because a bare combining
# mark in a literal is unreadable and un-diffable.  U+05D0..U+05EA is alef through tav, the
# five final forms included; U+05BE is maqaf; U+0591..U+05AE are the accents proper, which is
# where meteg (U+05BD) is deliberately not.
_NOT_A_LETTER = re.compile("[^\u05d0-\u05ea\u05be]")
_ACCENT = re.compile("[\u0591-\u05ae]")


def letters_and_maqaf(word: str) -> str:
    """What two texts must agree on for a chanted word to be the same one.

    Maqaf is kept, so a compound one text writes as one chanted word and the other as two does
    NOT join -- which is right: maqaf is the last rung of the accents' own scale, so a maqaf
    difference is an accentuation difference and belongs in the reported residue rather than
    being matched through.
    """
    return _NOT_A_LETTER.sub("", word)


def accents_of(word: str) -> str:
    return "".join(_ACCENT.findall(word))


def _flatten(node: object, out: list[dict]) -> None:
    """Every chanted-word entry of one verse, Phonetic MAM's ``cb`` brackets flattened.

    A ``cb`` brackets something other than a plain run of chanted words -- a paseq, a setuma, a
    qamats note, a dual-cantillation span -- and holds chanted words like any other branch.
    """
    if isinstance(node, dict):
        out.append(node)
    elif isinstance(node, list):
        for sub in node[1:] if node and node[0] == "cb" else node:
            _flatten(sub, out)


def load_phonetic_book(bb: str, cache: dict) -> dict:
    if bb not in cache:
        osdf = tbn.ordered_short_dash_full_39(wlc_bb_to_bk39id(bb))
        path = wlc_paths.require_al_hatorah_phonetic_dir() / f"{osdf}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        per_verse: dict[tuple[int, int], list[dict]] = {}
        for key, verse in data.items():
            chnu, vrnu = _VERSE_KEY.match(key).groups()
            entries: list[dict] = []
            _flatten(verse, entries)
            per_verse[(int(chnu), int(vrnu))] = [
                e for e in entries if e.get("jta") and e.get("fva") and e.get("udl")
            ]
        cache[bb] = per_verse
    return cache[bb]


# WLC 4.22 numbers its verses BHS's way and Phonetic MAM numbers them MAM's way.  The map is
# this repo's own declaration, py_misc/vtrad_data.py's _SHIFTED_SPAN_RECS_FOR_BHS and the
# one-to-many records beside it, transcribed as (first BHS verse, last BHS verse, shift) within
# one chapter.  It is not taken on trust: every hit is confirmed by the chanted word's letters,
# and a unit that does not confirm is reported.  Joshua 21:36-37 are deliberately absent -- MAM
# has no verse there, so those units cannot align and are counted as such.
_VERSE_SHIFTS = {
    ("1s", 24): ((2, 23, -1),),
    ("je", 31): ((2, 40, -1),),
    ("ex", 20): ((4, 12, -1), (17, 26, -4)),
    ("dt", 5): ((8, 16, -1), (21, 33, -4)),
    ("js", 21): ((38, 45, -2),),
}
_MERGED_VERSES = {
    ("ex", 20, 2): (20, 2),
    ("ex", 20, 3): (20, 2),
    ("ex", 20, 13): (20, 12),
    ("ex", 20, 14): (20, 12),
    ("ex", 20, 15): (20, 12),
    ("ex", 20, 16): (20, 12),
    ("dt", 5, 6): (5, 6),
    ("dt", 5, 7): (5, 6),
    ("dt", 5, 17): (5, 16),
    ("dt", 5, 18): (5, 16),
    ("dt", 5, 19): (5, 16),
    ("dt", 5, 20): (5, 16),
    ("1s", 24, 1): (23, 29),
    ("je", 31, 1): (30, 25),
}


def mam_verse_ref(bb: str, chnu: int, vrnu: int) -> tuple[int, int]:
    if (bb, chnu, vrnu) in _MERGED_VERSES:
        return _MERGED_VERSES[(bb, chnu, vrnu)]
    for lo, hi, shift in _VERSE_SHIFTS.get((bb, chnu), ()):
        if lo <= vrnu <= hi:
            return (chnu, vrnu + shift)
    return (chnu, vrnu)


# ---------------------------------------------------------------------------
# The parse trees
# ---------------------------------------------------------------------------


def zaqef_realms(tree: dict) -> list[tuple[str, int, int]]:
    """Outermost zaqef-labelled nodes as (label, first leaf, one past the last leaf).

    A zaqef node whose parent is also zaqef-labelled governs part of that zaqef's realm rather
    than the whole of it, so only the outermost one is "a simple unit which comprises the whole
    realm of a zaqef" (CoS Ch. 4 §7).
    """
    out: list[tuple[str, int, int]] = []

    def walk(node: dict, pos: int, parent_is_zaqef: bool) -> int:
        mine = node["label"].startswith("zaqef")
        if "leaves" in node:
            end = pos + len(node["leaves"])
            if mine and not parent_is_zaqef:
                out.append((node["label"], pos, end))
            return end
        begin = pos
        for child in node["children"]:
            pos = walk(child, pos, mine)
        if mine and not parent_is_zaqef:
            out.append((node["label"], begin, pos))
        return pos

    walk(tree, 0, False)
    return sorted(out, key=lambda t: t[1])


def tree_leaves(tree: dict) -> list[str]:
    out: list[str] = []

    def walk(node: dict) -> None:
        if "leaves" in node:
            out.extend(node["leaves"])
        else:
            for child in node["children"]:
                walk(child)

    walk(tree)
    return out


def leaf_to_token(leaves: list[str], token_leaves: list[str]) -> list[int | None]:
    """Which accent token each tree leaf is, ``None`` where the leaf is an ERROR.

    A verse the grammar could not parse has a run of its tokens standing in the tree as ERROR
    leaves, so leaf index and token index part company from there.  Matched by longest common
    prefix and suffix, with the leftover required to be ERROR leaves and nothing else: a wrong
    alignment would attribute an accent to the wrong chanted word, so it RAISES rather than
    guessing.
    """
    if leaves == token_leaves:
        return list(range(len(leaves)))
    pre = 0
    while (
        pre < len(leaves)
        and pre < len(token_leaves)
        and leaves[pre] == token_leaves[pre]
    ):
        pre += 1
    suf = 0
    while (
        suf < len(leaves) - pre
        and suf < len(token_leaves) - pre
        and leaves[len(leaves) - 1 - suf] == token_leaves[len(token_leaves) - 1 - suf]
    ):
        suf += 1
    middle = leaves[pre : len(leaves) - suf]
    assert middle and set(middle) == {"ERROR"}, (leaves, token_leaves)
    tail_start = len(token_leaves) - suf
    assert tail_start >= pre, (leaves, token_leaves)
    return (
        list(range(pre))
        + [None] * len(middle)
        + list(range(tail_start, len(token_leaves)))
    )


# ---------------------------------------------------------------------------
# The scan
# ---------------------------------------------------------------------------

# Yetiv is pashta's alternate form -- prose_ply_grammar's own rule is ``pashta_phrase : YETIV``
# -- so a yetiv divides the unit exactly as a pashta does.  Everything a two-chanted-word zaqef
# realm can put on its first chanted word is here or is a servant.
MAFSIK_LEAVES = frozenset(
    {
        "pashta",
        "yetiv",
        "revia",
        "zaqef",
        "tevir",
        "geresh",
        "gershayim",
        "tipexa",
        "pazer",
        "telishagedola",
        "legarmeh",
        "segolta",
        "zarqa",
        "atnax",
        "silluq",
        "shalshelet",
        "qarnepara",
    }
)


def is_divided(row: dict) -> bool:
    """Does the unit's first chanted word carry a mafsik, i.e. is the unit divided?"""
    return any(a in MAFSIK_LEAVES for a in row["first_accents"])


# Breuer's own exceptions to the rule, CoS Ch. 4 §8 (C04-S001.md, the two example groups after
# "This rule has not many exceptions").  His sixteen are a closed list of places where the
# zaqef's chanted word is long and the first chanted word has a servant all the same, which is
# exactly the residue this survey measures -- so they are the differential check on it, a
# source outside this repo saying what a right answer contains.  ``pin_breuer_s8`` RAISES on a
# miss rather than warning: a warning in a generator's output is a warning nobody reads.
#
# Which of the two groups each example is in -- I where the first chanted word is tiny, II
# where it is not -- is NOT pinned.  The OCR interleaves the two right-to-left columns, so the
# group each reference belongs to cannot be read off it reliably; the measured verdict for each
# first chanted word is reported instead, and §8's claim about the tiny ones is tested against
# the whole residue rather than against his grouping.
BREUER_S8_EXCEPTIONS = (
    "gn2:13",
    "gn5:15",
    "gn7:10",
    "gn24:44",
    "lv8:27",
    "lv14:52",
    "nu13:7",
    "nu30:2",
    "1s15:14",
    "1k13:3",
    "1k14:2",
    "ek21:19",
    "es9:25",
    "1c25:16",
    "2c30:7",
    "2c34:14",
)


def pin_breuer_s8(residue: list[dict]) -> list[dict]:
    """Breuer's sixteen §8 exceptions, each beside what the measurement found there."""
    found = {r["bcv"]: r for r in residue}
    missing = [bcv for bcv in BREUER_S8_EXCEPTIONS if bcv not in found]
    assert not missing, (
        f"{len(missing)} of Breuer's {len(BREUER_S8_EXCEPTIONS)} Ch. 4 §8 exceptions are"
        f" not in the measured long-but-servant residue: {', '.join(missing)}"
    )
    return [
        {
            "bcv": bcv,
            "first_word": found[bcv]["first_word"],
            "zaqef_word": found[bcv]["zaqef_word"],
            "first_chanted_word_is": found[bcv]["first_word_is"],
        }
        for bcv in BREUER_S8_EXCEPTIONS
    ]


def scan_units(stats: Counter, notes: dict) -> list[dict]:
    """Every zaqef realm of the committed prose trees that spans exactly two chanted words."""
    prose = wlc_paths.out_dir() / "accgram" / "prose"
    # Private names of a sibling module in this package, deliberately: ``_verse_units`` is the
    # unit derivation ``chanted_word_accents`` asserts equal to ``uni_to_marks.verse_to_marks``
    # on every verse of three corpora, and a second copy here could answer differently about
    # which chanted word an accent stands on.
    frags_by_bcv = cwa.wlc_frags(wlc_paths.out_dir() / "wlc422-kq-u")
    rows: list[dict] = []
    for path in sorted(prose.glob("wlc_422_ps_*_ag.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        # One HasLegarmeh per book, as prose_scanner.scan_book holds one: its 17-passage list
        # is walked monotonically and its 1 Samuel 14:47 counter resets per book.
        has_legarmeh = HasLegarmeh()
        for rec in data["verses"]:
            bcv = rec["bcv"]
            bb, chnu, vrnu = mna.split_bcv(bcv)
            body, units = cwa._verse_units(frags_by_bcv[bcv])
            tokens = scan_accents(body, bb, chnu, vrnu, has_legarmeh)
            stats["verses"] += 1
            stats[f"verses {rec['status']}"] += 1
            if [t.type for t in tokens] != rec["input"]["tokens"][1:]:
                # prose_run detangles the dually cantillated verses before scanning, and the
                # body rebuilt here is the tangled one, so its token positions would attribute
                # accents to the wrong chanted words.  Named and counted, not passed over.
                stats["verses excluded, token stream not the committed one"] += 1
                notes["token_stream_differs"].append(bcv)
                stats["zaqef realms"] += len(zaqef_realms(rec["tree"]))
                continue
            accents = [t for t in tokens if t.type not in cwa._NOT_AN_ACCENT_TOKEN]
            of_leaf = leaf_to_token(tree_leaves(rec["tree"]), [t.leaf for t in accents])
            unit_of_token = [cwa._unit_at(units, t.start) for t in accents]
            word_units = [u for u in units if u.is_word]
            starts = [u.start for u in word_units]
            for label, lo, hi in zaqef_realms(rec["tree"]):
                stats["zaqef realms"] += 1
                two_leaves = hi - lo == 2
                stats["realms with exactly 2 leaves"] += two_leaves
                span: list = []
                has_error = False
                for leaf_index in range(lo, hi):
                    token_index = of_leaf[leaf_index]
                    if token_index is None:
                        has_error = True
                        continue
                    unit = unit_of_token[token_index]
                    if unit is not None and (not span or span[-1] is not unit):
                        span.append(unit)
                if has_error:
                    stats["realms holding an ERROR leaf"] += 1
                    stats["  ... of them with exactly 2 leaves"] += two_leaves
                    continue
                stats[f"realms spanning {min(len(span), 9)} chanted words"] += 1
                if len(span) != 2:
                    stats[
                        "2-leaf realms spanning other than 2 chanted words"
                    ] += two_leaves
                    continue
                stats["2-chanted-word realms with more than 2 leaves"] += not two_leaves
                first, zaqef = span
                rows.append(
                    {
                        "bcv": bcv,
                        "label": label,
                        "status": rec["status"],
                        "verse_initial": starts.index(first.start) == 0,
                        "first_word": cwa._display(first),
                        "first_word_pointed": first.text,
                        "first_accents": [
                            t.leaf for t, u in zip(accents, unit_of_token) if u is first
                        ],
                        "zaqef_word": cwa._display(zaqef),
                        "zaqef_word_pointed": zaqef.text,
                        "zaqef_accents": [
                            t.leaf for t, u in zip(accents, unit_of_token) if u is zaqef
                        ],
                        "index_first": starts.index(first.start),
                        "index_zaqef": starts.index(zaqef.start),
                    }
                )
    return rows


def join_phonetic_mam(rows: list[dict], stats: Counter) -> list[dict]:
    """Attach Phonetic MAM's syllabification to each unit; return the units that will not join.

    Aligned by verse reference through ``mam_verse_ref``, then by chanted-word index with the
    letters checked at that index, then -- where the index does not land, which is what a maqaf
    grouping or a verse merge does -- by the letters over the whole verse, nearest index
    winning.  A unit whose chanted word is nowhere in the verse is a place where WLC's text and
    MAM's genuinely differ; it is returned rather than dropped, so the caller can report it.
    """
    cache: dict = {}
    unaligned: list[dict] = []
    for row in rows:
        bb, chnu, vrnu = mna.split_bcv(row["bcv"])
        words = load_phonetic_book(bb, cache).get(mam_verse_ref(bb, chnu, vrnu))
        if words is None:
            row["mam"] = "Phonetic MAM has no such verse"
            unaligned.append(row)
            continue
        found = []
        for which in ("first", "zaqef"):
            want = letters_and_maqaf(row[f"{which}_word_pointed"])
            index = row[f"index_{which}"]
            hit = None
            if (
                index < len(words)
                and letters_and_maqaf(words[index]["fva"].split(" ")[0]) == want
            ):
                hit = words[index]
            else:
                candidates = [
                    (abs(j - index), j, entry)
                    for j, entry in enumerate(words)
                    if letters_and_maqaf(entry["fva"].split(" ")[0]) == want
                    or (
                        entry.get("before_qfikq")
                        and letters_and_maqaf(entry["before_qfikq"]) == want
                    )
                ]
                if candidates:
                    hit = min(candidates)[2]
            found.append(hit)
        if found[0] is None or found[1] is None:
            row["mam"] = "Phonetic MAM has no such chanted word in that verse"
            unaligned.append(row)
            continue
        row["mam_first"] = found[0]["fva"].split(" ")[2]
        row["mam_zaqef"] = found[1]["fva"].split(" ")[2]
        row["mam_zaqef_pointed"] = found[1]["fva"].split(" ")[0]
        row["mam_agrees"] = bool(
            accents_of(row["first_word_pointed"])
            == accents_of(found[0]["fva"].split(" ")[0])
            and accents_of(row["zaqef_word_pointed"])
            == accents_of(found[1]["fva"].split(" ")[0])
        )
        row["first_analysis"] = analyse(found[0]["jta"], found[0]["udl"])
        row["analysis"] = analyse(found[1]["jta"], found[1]["udl"])
        stats["units joined to Phonetic MAM"] += 1
        stats["units where MAM has the same accents"] += row["mam_agrees"]
    return unaligned


def cross_tabulate(rows: list[dict], convention: str) -> dict:
    """long/short/tiny against mafsik/servant, for one syllable count."""
    table: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        table[row["analysis"][convention]["verdict"]][
            "mafsik" if is_divided(row) else "servant"
        ] += 1
    out: dict = {}
    for verdict in ("long", "short", "tiny"):
        counts = table[verdict]
        total = counts["mafsik"] + counts["servant"]
        as_predicted = counts["mafsik"] if verdict == "long" else counts["servant"]
        out[verdict] = {
            "mafsik": counts["mafsik"],
            "servant": counts["servant"],
            "total": total,
            "as_the_rule_predicts": as_predicted,
            "share_as_predicted": round(as_predicted / total, 4) if total else None,
        }
    return out


def build_survey() -> dict:
    stats: Counter = Counter()
    notes: dict[str, list] = defaultdict(list)
    rows = scan_units(stats, notes)
    unaligned = join_phonetic_mam(rows, stats)
    joined = [r for r in rows if "analysis" in r]
    agreeing = [r for r in joined if r["mam_agrees"]]
    residue: dict[str, list] = {}
    for name, wanted, divided in (
        ("long_but_servant", "long", False),
        ("short_but_mafsik", "short", True),
        ("tiny_but_mafsik", "tiny", True),
    ):
        residue[name] = [
            {
                "bcv": r["bcv"],
                "first_word": r["first_word"],
                "first_accents": r["first_accents"],
                "zaqef_word": r["zaqef_word"],
                "zaqef_word_jta": r["analysis"]["jta"],
                "syllables_before_the_stress": r["analysis"]["fat"]["before_stress"],
                "first_word_is": r["first_analysis"]["fat"]["verdict"],
            }
            for r in agreeing
            if r["analysis"]["fat"]["verdict"] == wanted and is_divided(r) == divided
        ]
    return {
        "the_rule": (
            "Breuer, The Cantillation of Scripture, Ch. 4 §7: a simple unit comprising the"
            " whole realm of a zaqef has a mafsik on its first chanted word if the zaqef's"
            " chanted word is long, and a servant if it is short. §8: the exceptions are few,"
            " and commoner when the first chanted word is tiny; in the opposite direction"
            " there are hardly any. Yeivin ITM §226 states the same rule and calls the"
            " exceptions many."
        ),
        "counts": dict(sorted(stats.items())),
        "corpus_mismatch": {
            "units": len(rows),
            "joined_to_phonetic_mam": len(joined),
            "not_joinable": len(unaligned),
            "where_mam_has_the_same_accents": len(agreeing),
            "where_mam_has_different_accents": len(joined) - len(agreeing),
            "not_joinable_units": [
                {
                    "bcv": r["bcv"],
                    "first_word": r["first_word"],
                    "zaqef_word": r["zaqef_word"],
                    "why": r["mam"],
                }
                for r in unaligned
            ],
            "different_accents_units": [
                {
                    "bcv": r["bcv"],
                    "wlc": f"{r['first_word']} {r['zaqef_word']}",
                    "mam": f"{r['mam_first']} {r['mam_zaqef']}",
                }
                for r in joined
                if not r["mam_agrees"]
            ],
            "verses_excluded": dict(notes),
        },
        "first_chanted_word_accents": dict(
            Counter(" ".join(r["first_accents"]) for r in rows).most_common()
        ),
        "first_chanted_word_accents_verse_initial": dict(
            Counter(
                " ".join(r["first_accents"]) for r in rows if r["verse_initial"]
            ).most_common()
        ),
        "cross_tabulation": {
            convention: {
                "all_joined_units": cross_tabulate(joined, convention),
                "where_mam_has_the_same_accents": cross_tabulate(agreeing, convention),
            }
            for convention in CONVENTIONS
        },
        "breuer_s8_exceptions": {
            "quote": (
                "This rule has not many exceptions. ... An exception of this type is more"
                " frequent, if the first word is tiny (examples I); and it is rare in other"
                " cases (examples II). On the other hand, there are hardly any exceptions in"
                " the opposite direction; and if the word of the zakef is short, then the word"
                " that precedes it is almost always cantillated with a servant."
            ),
            "source": "Breuer, The Cantillation of Scripture, Ch. 4 §8",
            "all_sixteen_are_in_the_measured_residue": pin_breuer_s8(
                residue["long_but_servant"]
            ),
        },
        "residue": {
            "measured_on": "the fat count, over the units where MAM has the same accents",
            "first_chanted_word_of_the_long_but_servant_units": dict(
                Counter(r["first_word_is"] for r in residue["long_but_servant"])
            ),
            "first_chanted_word_of_every_unit": dict(
                Counter(r["first_analysis"]["fat"]["verdict"] for r in agreeing)
            ),
            **{k: v for k, v in residue.items()},
        },
        "sensitivity": {
            "criterion_3_without_the_same_type_restriction": sum(
                1
                for r in agreeing
                if r["analysis"]["fat"]["verdict"] == "short"
                and r["analysis"]["fat"]["criteria"][CRITERION_3_ANY_TYPE]
            ),
            "criterion_2_widened_to_any_big_vowel": sum(
                1
                for r in agreeing
                if r["analysis"]["fat"]["verdict"] == "short"
                and r["analysis"]["fat"]["criteria"][CRITERION_2_ANY_SYLLABLE]
            ),
        },
        "units": rows,
    }


def default_json_out_path() -> Path:
    return wlc_paths.novc_dir() / "breuer-zaqef-units.json"


def add_args(parser: argparse.ArgumentParser, *, repo_root: Path) -> None:
    del repo_root  # the default composes off wlc_paths, as chanted_word_accents' does
    parser.add_argument(
        "--json-out",
        type=Path,
        default=default_json_out_path(),
        help="Where to write the survey JSON (default: wlc-utils/.novc/).",
    )


def run(args: argparse.Namespace) -> None:
    survey = build_survey()
    out_path = getattr(args, "json_out", None) or default_json_out_path()
    file_io.json_dump_to_file_path(
        provenance.with_json_provenance(survey, __file__), str(out_path), indent=1
    )
    print(f"wrote {out_path}")
