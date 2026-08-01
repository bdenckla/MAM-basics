"""Test helper: convert a legacy Michigan-Claremont accent body into the Unicode
mark body the Phase-2 scanners consume (issue #9).

Several scanner/grammar regression tests pin behaviour with real verse bodies that
were originally written in the M-C 2-digit-code encoding.  Rather than hand-rewrite
those long fixtures, `mc_to_marks` substitutes each 2-digit code with its
`accent_marks` mark (letters / maqaf / ``]N`` notes pass through), so the fixtures
stay readable while exercising the mark-based scanner.  It mirrors `uni_to_marks`
for everything these fixtures contain; it does *not* reproduce prepositive
front-relocation (none of the fixtures depend on the exact prepositive position --
the scanner rules only need the accents' relative order within a word).
"""

from __future__ import annotations

import re

from accgram import accent_marks as am

_MAP: dict[str, str] = {
    "92": am.ATNAX,
    "01": am.SEGOLTA,
    "65": am.SHALSHELET,
    "80": am.ZAQEF_QATAN,
    "85": am.ZAQEF_GADOL,
    "73": am.TIPEXA,
    "81": am.REVIA,
    "82": am.TSINNORIT,
    "03": am.PASHTA,
    "33": am.PASHTA,
    "10": am.YETIV,
    "11": am.GERESH_MUQDAM,
    "91": am.TEVIR,
    "61": am.GERESH,
    "62": am.GERSHAYIM,
    "12": am.GERSHAYIM,
    "84": am.QARNEY_PARA,
    "14": am.TELISHA_GEDOLA,
    "44": "",
    "83": am.PAZER,
    "74": am.MUNAX,
    "70": am.MAHAPAKH,
    "71": am.MERKHA,
    "72": am.MERKHA_KEFULA,
    "94": am.DARGA,
    "63": am.QADMA,
    "04": am.TELISHA_QETANA,
    "24": am.TELISHA_QETANA,
    "93": am.YERAX,
    "60": am.OLE,
    "64": am.ILUY,
    "13": am.DEXI,
    "02": am.TSINNOR,
    "35": am.METEG,
    "75": am.METEG,
    "95": am.METEG,
    "05": am.PASEQ,
    "00": am.SOF_PASUQ,
    "52": am.UPPER_DOT,
    "53": am.LOWER_DOT,
}

_CODE_RE = re.compile(r"\d\d")


def mc_to_marks(mc: str) -> str:
    """Substitute every 2-digit M-C code in ``mc`` with its mark (issue #9, Phase 2)."""
    return _CODE_RE.sub(lambda m: _MAP[m.group()], mc)
