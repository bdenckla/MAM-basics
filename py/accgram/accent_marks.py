r"""The Unicode mark alphabet the scanners consume (issue #9, Phase 2).

Phase 1 transcoded each ``-kq-u`` Unicode verse into a Michigan-Claremont (M-C)
2-digit-accent *body* and fed it to scanners written against that legacy code
vocabulary.  Phase 2 retires the M-C codes: the extraction layer
(``uni_to_marks``) now emits each accent as its own Unicode codepoint,
and the scanners match directly over that **mark sequence**.

A "mark body" is a string of single-character marks, one per structural element:

* each **accent** is its own Unicode codepoint (U+0591..U+05AE);
* **meteg/silluq** (U+05BD), **paseq** (U+05C0), **sof pasuq** (U+05C3) and the
  upper/lower **puncta** (U+05C4/U+05C5) are likewise their own codepoints;
* every base letter becomes a single placeholder ``LETTER`` -- opaque
  scanner filler, exactly as in Phase 1 -- and vowels/points are dropped;
* **maqaf** is ``-`` and the gaps between atoms are a space, the two ATOM boundaries the
  ``TEXT`` class and the lexical layer key on.  (An *atom* is one written word, between
  spaces or maqafs; a maqaf joins two of them into one CHANTED WORD, which is the unit an
  accent marks.  This module's alphabet sees only atoms -- issue #81.)
* ketiv ``*``/``**`` markers and ``]N`` note markers are kept verbatim.

The five M-C codepoint conflations (pashta ``33``/``03``, telisha qetana ``24``/
``04``, telisha gedola ``14``/``44``, gershayim ``12``/``62``, meteg ``35``/``75``/
``95``) no longer need distinct codes: the helper/main *merge* is expressed natively
in the scanner (adjacent same-accent within an atom -> one token), and the swallowed
secondaries (telisha gedola ``44``, gershayim ``12``) are dropped by ``uni_to_marks``'
positional/cluster resolution.

``negated_class`` rebuilds the four trailing-context lookaheads (silluq, mayela,
legarmeh, methiga-zaqef) over this alphabet.  tnk2acc.l expressed them as
character classes over the *digits* of the 2-digit codes (e.g. ``[^ 379...]`` =
"no code-digit 3, 7 or 9 here"); since a flex char-class consumes a 2-digit code
one digit at a time, a code *blocks* such a class iff either of its digits is
excluded.  We reproduce that exactly per *mark*: a mark blocks iff its
representative code's digit set intersects the excluded set (`_MARK_DIGITS`).  The
literal excluded digits are kept too, so the digit of a ``]N`` note marker still
blocks identically.
"""

from __future__ import annotations

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpu

# --- accent marks (their own Unicode codepoints) ------------------------------
#
# The codepoints themselves live in `mb_cmn.hebrew_accents` (named via `\N{...}`,
# the single source of truth).  Here we only alias them to the descriptive
# spellings the scanners use; the trailing comment is the legacy M-C 2-digit code.

ATNAX = ha.ATN  # etnaxta             (M-C 92)
SEGOLTA = ha.SEG_A  # segol (accent)      (01)
SHALSHELET = ha.SHA  # shalshelet          (65)
ZAQEF_QATAN = ha.ZAQ_Q  # zaqef qatan         (80)
ZAQEF_GADOL = ha.ZAQ_G  # zaqef gadol         (85)
TIPEXA = ha.TIP  # tipexa              (73)
REVIA = ha.REV  # revia               (81)
TSINNORIT = ha.ZSH_OR_TSIT  # zarqa stress-helper / tsinnorit (82)
PASHTA = ha.PASH  # pashta              (03 main / 33 helper)
YETIV = ha.YET  # yetiv               (10)
TEVIR = ha.TEV  # tevir               (91)
GERESH = ha.GER  # geresh              (61)
GERESH_MUQDAM = ha.GER_M  # geresh muqdam       (11)
GERSHAYIM = ha.GER_2  # gershayim           (62 main / 12 secondary)
QARNEY_PARA = ha.QAR  # qarney para (pazer gadol) (84)
TELISHA_GEDOLA = ha.TEL_G  # telisha gedola      (14 main / 44 secondary)
PAZER = ha.PAZ  # pazer               (83)
MUNAX = ha.MUN  # munax               (74)
MAHAPAKH = ha.MAH  # mahapakh            (70)
MERKHA = ha.MER  # merkha              (71)
MERKHA_KEFULA = ha.MER_2  # merkha kefula       (72)
DARGA = ha.DAR  # darga               (94)
QADMA = (
    ha.QOM
)  # qadma / azla        (63)  prose=qadma, poetic=azla (prose azla only before geresh)
TELISHA_QETANA = ha.TEL_Q  # telisha qetana      (04 main / 24 helper)
YERAX = ha.YBY  # yerax ben yomo / galgal (93)
OLE = ha.OLE  # ole                 (60)
ILUY = ha.ILU  # iluy                (64)
DEXI = ha.DEX  # dexi                (13)
TSINNOR = ha.Z_OR_TSOR  # tsinnor (zarqa/tsinnor main) (02)

# --- non-accent marks ---------------------------------------------------------

METEG = hp.MTGOSLQ  # meteg / silluq      (35 / 75 / 95)
PASEQ = hpu.PASOLEG  # paseq               (05)
SOF_PASUQ = hpu.SOPA  # sof pasuq           (00)
UPPER_DOT = hpu.UPDOT  # upper punctum       (52)
LOWER_DOT = hpu.LODOT  # lower punctum       (53)

MAQAF = "-"  # the boundary inside a chanted word (joins two atoms into one)
# Placeholder base letter (opaque scanner filler).  Alef -- a real Hebrew base, so a
# combining accent sits on it legibly and the scan body needs no re-basing for display.
# (It was a Latin "X" through issue #9; nothing keys on its identity -- every rule treats
# it as filler consumed by the catch-all -- so the mark bodies now read as Hebrew throughout.)
LETTER = "א"

# `TEXT` = a run that stays within one maqaf/space-delimited ATOM (as in tnk2acc.l's
# `{TEXT}` = `[^ \r\n\-]*`): everything except the two atom boundaries.
TEXT = r"[^ \r\n\-]*"

# Each mark -> the digit set of the M-C code it stands for, for `negated_class`.
# Conflated marks list every code that maps to them, except where `uni_to_marks`
# only ever emits one variant: meteg is always emitted as ``75`` (never ``35``/
# ``95``), and the swallowed secondaries (telisha gedola ``44``, gershayim ``12``)
# are dropped, so telisha gedola is always ``14`` and gershayim always ``62``.
_MARK_DIGITS: dict[str, str] = {
    ATNAX: "92",
    SEGOLTA: "01",
    SHALSHELET: "65",
    ZAQEF_QATAN: "80",
    ZAQEF_GADOL: "85",
    TIPEXA: "73",
    REVIA: "81",
    TSINNORIT: "82",
    PASHTA: "03",  # helper 33 shares digit 3 -> same blocking set
    YETIV: "10",
    TEVIR: "91",
    GERESH: "61",
    GERESH_MUQDAM: "11",
    GERSHAYIM: "62",
    QARNEY_PARA: "84",
    TELISHA_GEDOLA: "14",
    PAZER: "83",
    MUNAX: "74",
    MAHAPAKH: "70",
    MERKHA: "71",
    MERKHA_KEFULA: "72",
    DARGA: "94",
    QADMA: "63",
    TELISHA_QETANA: "024",  # main 04 + helper 24
    YERAX: "93",
    OLE: "60",
    ILUY: "64",
    DEXI: "13",
    TSINNOR: "02",
    METEG: "75",
    PASEQ: "05",
    SOF_PASUQ: "00",
    UPPER_DOT: "52",
    LOWER_DOT: "53",
}


def _escape_in_class(ch: str) -> str:
    return "\\" + ch if ch in "-]^\\" else ch


def negated_class(literals: str, digits: str) -> str:
    r"""A regex negated character class equivalent to one of tnk2acc.l's digit
    classes, lifted onto the mark alphabet.

    ``digits`` is the set of code-digits the original class excluded (e.g. ``"379"``
    for the silluq class ``[^ 379...]``); ``literals`` is any extra literal chars it
    excluded (space, CR, LF, maqaf, ``?``/``~``).  The result excludes those literals
    and digits *and* every mark whose representative code shares a digit with
    ``digits`` -- exactly the marks the original class could not consume.
    """
    excluded = set(digits)
    blockers = "".join(
        mark for mark, mdigits in _MARK_DIGITS.items() if excluded & set(mdigits)
    )
    body = "".join(_escape_in_class(c) for c in (literals + digits)) + blockers
    return "[^" + body + "]"
