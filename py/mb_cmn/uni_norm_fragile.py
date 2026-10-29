"""Fragile Hebrew mark orders, under Unicode normalization and under HarfBuzz.

A string's mark order is fragile if something between the text and a font may
change it in a way a reader could see. Two such reorderings are checked:

1. Normalization to NFC, which sorts each run of combining marks by Unicode's
   canonical combining classes.
2. HarfBuzz's mark reordering, which sorts each run by HarfBuzz's own
   permutation of those classes, and then applies one Hebrew rule, before a
   font sees the marks. hb_mark_order models HarfBuzz 15.0.0's reordering.

Both reorderings are applied to the string without the marks in _DROP_TABLE.
The string is fragile if either of them changes it in any way except this:
within one run of marks, a mark below a letter moves past a mark above it.
Fonts place the marks below a letter independently of the marks above it, so
the marks below a letter must keep their relative order, and so must the marks
above it. Any other change is fragile, including a composition by NFC.
_ZONES says which marks are below a letter and which are above it.

A CGJ has class 0, so it ends a run of marks in both reorderings and keeps the
order of the marks on either side of it.
"""

import functools
import re
import unicodedata

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu

__all__ = [
    "get_fragile_comps",
    "hb_mark_order",
    "is_fragile",
    "is_hb_fragile",
    "is_nfc_fragile",
]


_DROP_TABLE = str.maketrans(
    {
        hpo.DAGOMOSD: None,
        hpo.RAFE: None,
        hpo.SHIND: None,
        hpo.SIND: None,
        hpu.LODOT: None,  # See "Note on lower dot"
        "\N{COMBINING ACUTE ACCENT}": None,
        # COMBINING ACUTE ACCENT is used in í in Martín in a documentation note.
        # We drop it because otherwise the string is fragile: NFC composes the
        # i and the accent into one character, and every change NFC makes is
        # fragile except a mark below a letter moving past a mark above it.
    }
)


def get_fragile_comps(string):
    """Get the strings used in fragile comparison.

    They are the string without the marks in _DROP_TABLE, that string
    normalized to NFC, and that string in HarfBuzz's mark order.
    """
    dropped = string.translate(_DROP_TABLE)
    dropped_n = unicodedata.normalize("NFC", dropped)
    dropped_hb = hb_mark_order(dropped)
    return dropped, dropped_n, dropped_hb


def is_fragile(string):
    """Return whether the string's mark order is fragile under NFC or HarfBuzz."""
    dropped, dropped_n, dropped_hb = get_fragile_comps(string)
    return _is_fragile_change(
        dropped, dropped_n, unicodedata.combining
    ) or _is_fragile_change(dropped, dropped_hb, _hb_class)


def is_nfc_fragile(string):
    """Return whether the string's mark order is fragile under NFC."""
    dropped = string.translate(_DROP_TABLE)
    dropped_n = unicodedata.normalize("NFC", dropped)
    return _is_fragile_change(dropped, dropped_n, unicodedata.combining)


def is_hb_fragile(string):
    """Return whether the string's mark order is fragile under HarfBuzz."""
    dropped = string.translate(_DROP_TABLE)
    return _is_fragile_change(dropped, hb_mark_order(dropped), _hb_class)


def hb_mark_order(string):
    """Return the string with its marks in the order HarfBuzz gives a font.

    This models the reorder round of HarfBuzz 15.0.0's normalization,
    src/hb-ot-shape-normalize.cc lines 372-402: each run of marks with a
    nonzero class is sorted stably by _hb_class, unless it is longer than 32
    marks, and then the Hebrew shaper's _hb_reorder_marks_hebrew applies to it.
    Other shapers' reorderings are not modeled.
    https://github.com/harfbuzz/harfbuzz/blob/15.0.0/src/hb-ot-shape-normalize.cc#L372-L402
    """
    return _hb_mark_run_pattern().sub(_hb_reorder_run_match, string)


def _is_fragile_change(original, changed, class_of):
    """Return whether changed differs from original other than across zones.

    The one change allowed is a permutation, within a run of marks, that keeps
    the relative order of the marks below the letter and of the marks above it.
    """
    if changed == original:
        return False
    if len(changed) != len(original):
        return True
    for start, end in _runs(original, class_of):
        run, new_run = original[start:end], changed[start:end]
        if run == new_run:
            continue
        if end - start == 1 or sorted(run) != sorted(new_run):
            return True
        if _zone_orders(run) != _zone_orders(new_run):
            return True
    return False


def _runs(string, class_of):
    """Yield the span of each run of marks and of each other character."""
    start = 0
    while start < len(string):
        end = start + 1
        if class_of(string[start]):
            while end < len(string) and class_of(string[end]):
                end += 1
        yield start, end
        start = end


def _zone_orders(run):
    """Return the run's marks below the letter and its marks above it, in order."""
    zones = {_BELOW: [], _ABOVE: []}
    for mark in run:
        zone = _ZONES.get(mark)
        if zone is None:
            uname = unicodedata.name(mark, "an unnamed character")
            raise ValueError(f"No zone for U+{ord(mark):04X} {uname}")
        zones[zone].append(mark)
    return zones[_BELOW], zones[_ABOVE]


# The zone of each mark that a fragile comparison can see: below the letter or
# above it. The table is closed: _zone_orders raises on any other mark in a run
# that NFC or HarfBuzz reorders. The marks in _DROP_TABLE need no zone. Neither
# does dagesh xazaq, which sits inside the letter like the dagesh; whether to
# drop it like the dagesh or give it a zone is undecided, so a reordered run
# that holds it raises.
_BELOW = "below"
_ABOVE = "above"
_ZONES = {
    hpo.SHEVA: _BELOW,
    hpo.SHEVA_NA: _BELOW,
    hpo.XSEGOL: _BELOW,
    hpo.XPATAX: _BELOW,
    hpo.XQAMATS: _BELOW,
    hpo.XIRIQ: _BELOW,
    hpo.TSERE: _BELOW,
    hpo.SEGOL_V: _BELOW,
    hpo.PATAX: _BELOW,
    hpo.QAMATS: _BELOW,
    hpo.QAMATS_Q: _BELOW,
    hpo.QUBUTS: _BELOW,
    hpo.MTGOSLQ: _BELOW,
    **dict.fromkeys(ha.UNI_UNDER_ACCENTS, _BELOW),  # the accents of class 220 or 222
    hpo.XOLAM: _ABOVE,
    hpo.XOLAM_XFV: _ABOVE,
    hpo.VARIKA: _ABOVE,
    hpu.UPDOT: _ABOVE,
    hpu.MCIRC: _ABOVE,
    **dict.fromkeys(ha.UNI_OVER_ACCENTS, _ABOVE),  # the accents of class 228 or 230
}


def _hb_class(char):
    """Return the class by which HarfBuzz 15.0.0 sorts char among its marks."""
    if char in _HB_CLASSES_BY_MARK:
        return _HB_CLASSES_BY_MARK[char]
    unicode_class = _UNICODE_18_CLASSES.get(char) or unicodedata.combining(char)
    return _HB_CLASSES.get(unicode_class, unicode_class)


# HarfBuzz sorts marks by its own permutation of Unicode's combining classes,
# the table _hb_modified_combining_class, in HarfBuzz 15.0.0's
# src/hb-unicode.cc lines 499-609, built from src/hb-unicode.hh lines 316-401.
# Its comment there, lines 320-332, derives the order of the Hebrew points from
# the SBL Hebrew Font User Manual and Mozilla bug 662055. Every class not listed
# here maps to itself, among them the accents' classes 220, 222, 228 and 230
# (hb-unicode.cc lines 573-608), so the sort puts every vowel and meteg before
# every accent, and only _hb_reorder_marks_hebrew moves an accent back.
# https://github.com/harfbuzz/harfbuzz/blob/15.0.0/src/hb-unicode.hh#L316-L401
_HB_CLASSES = {
    24: 10,  # shin dot
    25: 11,  # sin dot
    21: 12,  # dagesh or mapiq, and dagesh xazaq
    23: 13,  # rafeh
    19: 14,  # xolam, and xolam xaser for vav
    11: 15,  # xataf segol
    12: 16,  # xataf patax
    13: 17,  # xataf qamats
    15: 18,  # tsere
    16: 19,  # segol
    17: 20,  # patax
    18: 21,  # qamats, and qamats qatan
    10: 22,  # sheva, and sheva na
    14: 23,  # xiriq
    20: 24,  # qubuts
    22: 25,  # meteg
    26: 26,  # varika
    27: 28,  # Arabic fathatan
    28: 29,  # Arabic dammatan
    29: 30,  # Arabic kasratan
    30: 31,  # Arabic fatha
    31: 32,  # Arabic damma
    32: 33,  # Arabic kasra
    33: 27,  # Arabic shadda
    84: 4,  # Telugu length mark
    91: 5,  # Telugu ai length mark
    103: 3,  # Thai sara u and sara uu
    130: 132,  # Tibetan sign i
    132: 131,  # Tibetan sign u
}
# Three marks get a class by code point, hb-unicode.hh lines 105-116.
_HB_CLASSES_BY_MARK = {
    "\N{TAI THAM SIGN SAKOT}": 254,
    "\N{TIBETAN SYMBOL PADMA GDAN}": 254,
    "\N{TIBETAN MARK TSA -PHRU}": 127,
}
# HarfBuzz 15.0.0 has Unicode 18.0.0's character data (src/hb-ucd-table.hh
# line 7), which gives sheva na class 10 and dagesh xazaq class 21, so HarfBuzz
# sorts them with the sheva and the dagesh. Python 3.13's unicodedata has
# Unicode 15.1.0, which lacks both characters, so they are named here.
_UNICODE_18_CLASSES = {hpo.SHEVA_NA: 10, hpo.DAGESH_XAZAQ: 21}

_HB_MAX_COMBINING_MARKS = 32  # src/hb-ot-shaper.hh line 42

# The classes that _hb_reorder_marks_hebrew looks for. Class 220 is Unicode's
# class for marks below, HarfBuzz's HB_UNICODE_COMBINING_CLASS_BELOW.
_HB_PATAX_OR_QAMATS = {_HB_CLASSES[17], _HB_CLASSES[18]}
_HB_SHEVA_OR_XIRIQ = {_HB_CLASSES[10], _HB_CLASSES[14]}
_HB_METEG_OR_BELOW = {_HB_CLASSES[22], 220}


@functools.cache
def _hb_mark_run_pattern():
    """Compile a pattern matching each run of two or more marks."""
    marks = set(_UNICODE_18_CLASSES)
    marks.update(c for c in map(chr, range(0x110000)) if unicodedata.combining(c))
    ranges = []
    for code in sorted(map(ord, marks)):
        if ranges and ranges[-1][1] == code - 1:
            ranges[-1][1] = code
        else:
            ranges.append([code, code])
    char_class = "".join(
        f"{re.escape(chr(lo))}-{re.escape(chr(hi))}" for lo, hi in ranges
    )
    return re.compile(f"[{char_class}]{{2,}}")


def _hb_reorder_run_match(match):
    return _hb_reorder_run(match.group())


# Bounded, since the HarfBuzz test sends every triple of Hebrew marks through it.
@functools.lru_cache(maxsize=1 << 14)
def _hb_reorder_run(run):
    if len(run) > _HB_MAX_COMBINING_MARKS:
        return run
    marks = sorted(run, key=_hb_class)
    _hb_reorder_marks_hebrew(marks)
    return "".join(marks)


def _hb_reorder_marks_hebrew(marks):
    """Swap the last two marks of the run's first Jerusalem triple, in place.

    This is reorder_marks_hebrew, in HarfBuzz 15.0.0's
    src/hb-ot-shaper-hebrew.cc lines 165-190, first released in 5.0.0 (2022)
    from https://github.com/harfbuzz/harfbuzz/issues/2947. A Jerusalem triple
    is three consecutive marks of the sorted run: a patax or qamats, then a
    sheva or xiriq, then a meteg or a mark of class 220. The swap puts the
    meteg or class-220 mark before the sheva or xiriq.
    https://github.com/harfbuzz/harfbuzz/blob/15.0.0/src/hb-ot-shaper-hebrew.cc#L165-L190
    """
    classes = list(map(_hb_class, marks))
    for i in range(2, len(marks)):
        if (
            classes[i - 2] in _HB_PATAX_OR_QAMATS
            and classes[i - 1] in _HB_SHEVA_OR_XIRIQ
            and classes[i] in _HB_METEG_OR_BELOW
        ):
            marks[i - 1], marks[i] = marks[i], marks[i - 1]
            return


###########################################################
# Note on lower dot:
#
# For the one word that uses lower dot, in Ps27:13, MAM uses
# a "Unicode-abnormal" order on one letter:
#
#    lamed, tsere, revia, lower dot, upper dot
#
# This has a certain logic to it:
#
#    letter, vowel, accent, [really weird stuff]
#
# i.e.
#
#    letter, vowel, accent, lower dot, upper dot
#
# But both Unicode and SBL normal orders specify that all lower
# marks, including lower dot, should appear before any upper accents.
# This would make the order:
#
#    lamed, tsere, lower dot, revia, upper dot
#
# Below, we sidestep the issue by dropping lower dot.
# This "admits" that our ordering of lower dot is abnormal.
# This puts lower dot in the same category as dagesh, rafeh, shin dot,
# and sin dot.
# That category being, marks for which we "admit" that our ordering
# is Unicode-abnormal.
# Note that Unicode normal order is not *insane* for lower dot, as it is
# for the other four marks.
# We just happen to not want to use Unicode order for lower dot.
#
# MAM's text no longer has the order above: on 2026-10-28, Ps27:13 in
# MAM-parsed has lamed, tsere, lower dot, revia, upper dot, Unicode's
# order, which NFC and HarfBuzz leave alone even with lower dot kept.
# And now that fragility ignores a mark below a letter moving past a
# mark above it, the older order would not be fragile either: NFC and
# HarfBuzz move lower dot, a mark below the letter, only past revia, a
# mark above it. So dropping lower dot is redundant, but it stays in
# _DROP_TABLE, and so it needs no entry in _ZONES.
#
###########################################################
# Note on QUPO, LAOI, and LAOE
#
# We encode QUPO as QUcPO so that,
# even in the face of Unicode normalization,
# the Q, U, P, & O marks appear in QUPO order, albeit with a CGJ in the middle.
#
# We prefer QUPO order because it obeys the general principle:
#
#    Undermarks first, in RTL order (QUP), followed by overmark(s) (O).
#
# That's why the underlying spreadsheet sources are encoded in QUPO order.
#
# Note that, despite our preference for QUPO, we prefer LAOI & LAOE.
#
# I.e., despite the fact that LAOI & LAOE violate the principle above,
# we prefer them.
#
# LAOI & LAOE violate the principle above because they have "O" (an overmark)
# between two undermarks. Those undermarks are:
#
#    1. "A", meaning qamats or patax
#    2. "I" or "E", meaning xiriq or sheva
#
# We prefer LAOI & LAOE for two reasons:
#
#    1. Analogy with LAUI & LAUE
#    2. "Implicit yod" interpretation, e.g. LAOI "stands for" LAO[Y]I where
#       "[Y]" represents an implicit yod.
