"""Conservative screening for cramped pointed-Hebrew text in Taamey D.

This is a typography heuristic, not a collision detector. A yod or vav with
a broad below-vowel and a below-accent can crowd neighboring ink
even after the font has avoided overlap. NAEE expands such atoms by 0.06em,
alongside the six observed advance-adding contexts in the frozen Taamey D 0.921
source and its precise preceding-yod vowel-raising context beside qof. These
font-derived contexts preserve their below-mark order and filtering conditions;
they do not enable either broad FOI trial screen wholesale.

HTML conversion sees contiguous text leaves after semantic rendering. Atoms split
by special-letter or vowel-variant spans may be missed or only partly expanded;
single-letter leaves are left alone. No source character or mark order changes.
"""

import unicodedata

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import unicode_data as ucd
from mb_misc import mb_html

CLASS = "hebrew-expanded-spacing"
NARROW_VOWEL_ACCENT = "narrow-vowel-accent"
ADJACENT_NARROW_BELOW = "adjacent-narrow-below"
QOF_PREDECESSOR_BELOW = "qof-predecessor-below"
FONT_ADDED_SPACE = "font-added-space"
YOD_BEFORE_QOF = "yod-before-qof"
_VOWEL_ACCENT_LETTERS = frozenset(
    (
        "\N{HEBREW LETTER YOD}",
        "\N{HEBREW LETTER VAV}",
    )
)
_BROAD_BELOW_VOWELS = frozenset(
    (hp.TSERE, hp.SEGOL_V, hp.XSEGOL, hp.XPATAX, hp.XQAMATS, hp.QUBUTS)
)
# The broader narrow-letter class in the frozen Taamey D source's @narlets.
_NARROW_PAIR_LETTERS = _VOWEL_ACCENT_LETTERS | frozenset(
    (
        "\N{HEBREW LETTER GIMEL}",
        "\N{HEBREW LETTER ZAYIN}",
        "\N{HEBREW LETTER NUN}",
        "\N{HEBREW LETTER FINAL NUN}",
    )
)
_BELOW_VOWELS = _BROAD_BELOW_VOWELS | frozenset(
    (hp.SHEVA, hp.SHEVA_NA, hp.XIRIQ, hp.PATAX, hp.QAMATS, hp.QAMATS_Q)
)
_BELOW_ACCENTS_OR_METEG = ha.UNI_UNDER_ACCENTS | {hp.MTGOSLQ}
_BELOW_MARKS = _BELOW_VOWELS | _BELOW_ACCENTS_OR_METEG
# Taamey D.sym.fea's @blws and @blw_wides, rather than the broader trial sets.
# Yetiv and dexi are excluded by the kern lookups' mark filtering; sheva na is
# not a glyph in this font. Patax and qamats are wide in the font's classes.
_FONT_BELOW = _BELOW_MARKS - {ha.YET, ha.DEX, hp.SHEVA_NA}
_FONT_WIDE = _FONT_BELOW - {hp.SHEVA, hp.XIRIQ, hp.MTGOSLQ}
_FONT_XATAFS = frozenset((hp.XSEGOL, hp.XPATAX, hp.XQAMATS))
_FONT_IGNORED = ha.UNI_OVER_ACCENTS | {
    ha.YET,
    ha.DEX,
    hp.DAGOMOSD,
    hp.RAFE,
    hp.SHIND,
    hp.SIND,
    hp.XOLAM,
    hp.XOLAM_XFV,
    hp.VARIKA,
    "\N{HEBREW MARK UPPER DOT}",
    "\N{HEBREW MARK LOWER DOT}",
    "\N{COMBINING GRAPHEME JOINER}",
}
_FONT_RIGHT_DESCENDERS = frozenset("ךןף")
_FONT_ULTRA_NARROW = frozenset("וי")
_QOF_PRECEDING_VOWELS = frozenset(
    (hp.TSERE, hp.PATAX, hp.QAMATS, hp.SEGOL_V, hp.QUBUTS)
)
_QOF_VOWELS = frozenset((hp.PATAX, hp.QAMATS, hp.QUBUTS))
_QOF_ACCENTS = frozenset((ha.TEV, ha.MAH, ha.DAR))


def _font_below(marks, *, include_dehi=False):
    """Project mark order for font screening, without changing any source text.

    Retained below marks follow canonical combining-class order during shaping.
    A class-zero mark such as CGJ protects the preceding sequence.
    Retain unsupported glyphs as barriers rather than skipping them as marks.
    """
    ordered = []
    segment = []
    for mark in marks:
        if unicodedata.combining(mark) == 0:
            ordered.extend(sorted(segment, key=unicodedata.combining))
            segment = []
            ordered.append(mark)
        else:
            segment.append(mark)
    ordered.extend(sorted(segment, key=unicodedata.combining))
    return tuple(
        mark
        for mark in ordered
        if mark not in _FONT_IGNORED or (include_dehi and mark == ha.DEX)
    )


def _font_added_space(clusters):
    """The five kern1AddThin contexts and the observed second kern2AddThin rule.

    Source: in/font-support/taamey-d-0.921/'s frozen source archive,
    sources/font-m-TaD/Taamey_D.sym.fea, lines 137–150. The first kern2AddThin
    rule (two below marks before a narrow letter with three) remains a trial:
    the selected-Scripture investigation found no occurrence to judge visually.
    """
    projected = [(letter, _font_below(marks)) for letter, marks in clusters]
    # ccmp06JerusalemOrphans replaces the last xiriq/sheva in these explicit
    # vowel sequences with an orphan glyph outside the below-mark filter.
    for index, (_, marks) in enumerate(projected[:-1]):
        next_letter = projected[index + 1][0]
        orphan = {"ם": hp.XIRIQ, "מ": hp.SHEVA}.get(next_letter)
        vowels = [
            (position, mark)
            for position, mark in enumerate(marks)
            if mark in {hp.PATAX, hp.QAMATS, hp.XIRIQ, hp.SHEVA}
        ]
        if (
            len(vowels) >= 2
            and vowels[-2][1] in {hp.PATAX, hp.QAMATS}
            and vowels[-1][1] == orphan
            and all(mark in _FONT_BELOW for mark in marks)
        ):
            position = vowels[-1][0]
            projected[index] = (
                projected[index][0],
                marks[:position] + marks[position + 1 :],
            )
    for index, ((first, a), (second, b)) in enumerate(zip(projected, projected[1:])):
        one_wide = len(a) == 1 and a[0] in _FONT_WIDE
        two_below_wide = len(a) == 2 and a[0] in _FONT_BELOW and a[1] in _FONT_WIDE
        wide_below = len(b) >= 2 and b[0] in _FONT_WIDE and b[1] in _FONT_BELOW
        below_wide = len(b) >= 2 and b[0] in _FONT_BELOW and b[1] in _FONT_WIDE
        # A final he/xet/ayin's patax can be a furtive glyph filtered out by
        # kern1AddThin. Omit these unjudged alternate shapes from its fifth
        # context rather than treating the raw vowel as a broad font glyph.
        fifth_context = wide_below and not (
            index + 2 == len(projected) and second in "החע" and hp.PATAX in b
        )
        if (
            # kern1AddThin's five ordered contexts.
            (
                first in _NARROW_PAIR_LETTERS
                and one_wide
                and second in _NARROW_PAIR_LETTERS
                and wide_below
            )
            or (
                first in _FONT_ULTRA_NARROW
                and one_wide
                and second in _FONT_ULTRA_NARROW
                and below_wide
            )
            or (
                first in _NARROW_PAIR_LETTERS
                and two_below_wide
                and second in _NARROW_PAIR_LETTERS
                and b
                and b[0] in _FONT_BELOW
            )
            or (
                first in _NARROW_PAIR_LETTERS
                and two_below_wide
                and second in _FONT_RIGHT_DESCENDERS
            )
            or (first in _NARROW_PAIR_LETTERS and two_below_wide and fifth_context)
            # kern2AddThin's second context.
            or (
                len(a) == 1
                and a[0] in _FONT_XATAFS
                and second in _NARROW_PAIR_LETTERS
                and wide_below
            )
        ):
            return True
    return False


def _yod_before_qof(clusters):
    """Screen the exact vowel-raising context in the font source's line 333."""
    for (first, a), (second, b) in zip(clusters, clusters[1:]):
        if first != "י" or second != "ק":
            continue
        a = _font_below(a, include_dehi=True)
        b = _font_below(b, include_dehi=True)
        if (
            len(a) == 1
            and a[0] in _QOF_PRECEDING_VOWELS
            and len(b) >= 2
            and b[0] in _QOF_VOWELS
            and b[1] in _QOF_ACCENTS
        ):
            return True
    return False


def _is_letter(char):
    return "א" <= char <= "ת"


def types_for_atom(atom):
    """Identify overlapping crowding families, including additional FOI trial types.

    The original narrow-vowel-accent and the two precise font-derived families
    opt into NAEE expansion. The broad pair families remain visual trials.
    """
    clusters = []
    for char in atom:
        if _is_letter(char):
            clusters.append((char, []))
        elif ucd.is_mark(char) and clusters:
            clusters[-1][1].append(char)
        else:
            return ()
    if len(clusters) < 2:
        return ()
    types = []
    if _font_added_space(clusters):
        types.append(FONT_ADDED_SPACE)
    if _yod_before_qof(clusters):
        types.append(YOD_BEFORE_QOF)
    clusters = [(letter, set(marks)) for letter, marks in clusters]
    if any(
        letter in _VOWEL_ACCENT_LETTERS
        and marks & _BROAD_BELOW_VOWELS
        and marks & ha.UNI_UNDER_ACCENTS
        for letter, marks in clusters
    ):
        types.append(NARROW_VOWEL_ACCENT)
    pairs = tuple(zip(clusters, clusters[1:]))
    if any(
        first in _NARROW_PAIR_LETTERS
        and second in _NARROW_PAIR_LETTERS
        and first_marks & _BELOW_MARKS
        and second_marks & _BELOW_MARKS
        and (first_marks | second_marks)
        & (_BROAD_BELOW_VOWELS | _BELOW_ACCENTS_OR_METEG)
        for (first, first_marks), (second, second_marks) in pairs
    ):
        types.append(ADJACENT_NARROW_BELOW)
    if any(
        second == "\N{HEBREW LETTER QOF}"
        and first_marks & _BELOW_MARKS
        and second_marks & _BELOW_MARKS
        for (_, first_marks), (second, second_marks) in pairs
    ):
        types.append(QOF_PREDECESSOR_BELOW)
    return tuple(types)


def needs_expansion(atom):
    """Apply the three active families, leaving the broad FOI families as trials."""
    return bool(
        {NARROW_VOWEL_ACCENT, FONT_ADDED_SPACE, YOD_BEFORE_QOF}
        & set(types_for_atom(atom))
    )


def iter_atoms(text):
    """Yield start, end and text of Hebrew atoms within a text run."""
    index = 0
    while index < len(text):
        if not _is_letter(text[index]):
            index += 1
            continue
        end = index + 1
        while end < len(text) and (_is_letter(text[end]) or ucd.is_mark(text[end])):
            end += 1
        yield index, end, text[index:end]
        index = end


def html_for_text(text):
    """Wrap selected Hebrew atoms, preserving all characters and separators.

    Spaces, maqaf marks and punctuation stay outside the spacing span. Combining marks,
    including Phonetic MAM's newer Hebrew points, stay with their base letter.
    """
    result = []
    start = 0
    for index, end, atom in iter_atoms(text):
        if needs_expansion(atom):
            if start < index:
                result.append(text[start:index])
            result.append(mb_html.span_c(atom, CLASS))
            start = end
    if not result:
        return text
    if start < len(text):
        result.append(text[start:])
    return tuple(result)
