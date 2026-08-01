"""Guard: the scanner mark alphabet stays a thin alias over mb_cmn.

`accgram.accent_marks` must not re-declare cantillation codepoints as raw
diacritic literals -- that path drifts from `mb_cmn` (the single source of
truth) and puts unreadable bare combining marks in quotes.  Two checks:

* every accent/mark constant is value-identical to its `mb_cmn` source;
* the module's *own* source text carries no raw Hebrew combining mark inside a
  string literal (force `\\N{...}` or an `mb_cmn` alias instead).

This only guards `accent_marks.py`; textual fixtures elsewhere (note bodies,
diff corpora) legitimately contain real Hebrew text and are out of scope. The
tree-wide NFC/precomposed guard (#49) covers this file too, via
`test_transliterations.py::test_no_decomposed_composites_tree_wide`.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_accent_marks_source.py -v
"""

from __future__ import annotations

import inspect
import re

from accgram import accent_marks as am
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpu

# accent_marks name -> its single-source-of-truth origin in mb_cmn.
_SOURCE = {
    "ATNAX": ha.ATN,
    "SEGOLTA": ha.SEG_A,
    "SHALSHELET": ha.SHA,
    "ZAQEF_QATAN": ha.ZAQ_Q,
    "ZAQEF_GADOL": ha.ZAQ_G,
    "TIPEXA": ha.TIP,
    "REVIA": ha.REV,
    "TSINNORIT": ha.ZSH_OR_TSIT,
    "PASHTA": ha.PASH,
    "YETIV": ha.YET,
    "TEVIR": ha.TEV,
    "GERESH": ha.GER,
    "GERESH_MUQDAM": ha.GER_M,
    "GERSHAYIM": ha.GER_2,
    "QARNEY_PARA": ha.QAR,
    "TELISHA_GEDOLA": ha.TEL_G,
    "PAZER": ha.PAZ,
    "MUNAX": ha.MUN,
    "MAHAPAKH": ha.MAH,
    "MERKHA": ha.MER,
    "MERKHA_KEFULA": ha.MER_2,
    "DARGA": ha.DAR,
    "QADMA": ha.QOM,
    "TELISHA_QETANA": ha.TEL_Q,
    "YERAX": ha.YBY,
    "OLE": ha.OLE,
    "ILUY": ha.ILU,
    "DEXI": ha.DEX,
    "TSINNOR": ha.Z_OR_TSOR,
    "METEG": hp.MTGOSLQ,
    "PASEQ": hpu.PASOLEG,
    "SOF_PASUQ": hpu.SOPA,
    "UPPER_DOT": hpu.UPDOT,
    "LOWER_DOT": hpu.LODOT,
}

# Hebrew accents (U+0591..U+05AE), meteg (U+05BD), paseq/sof-pasuq/puncta.
_RAW_MARK = re.compile(r"[֑-ֽ֮׀׃-ׅ]")


def test_constants_match_mb_cmn() -> None:
    for name, expected in _SOURCE.items():
        assert getattr(am, name) == expected, f"{name} drifted from mb_cmn"


def test_no_raw_diacritics_in_source() -> None:
    src = inspect.getsource(am)
    offenders = [
        (i, line.strip())
        for i, line in enumerate(src.splitlines(), 1)
        if _RAW_MARK.search(line) and ('"' in line or "'" in line)
    ]
    assert not offenders, (
        "accent_marks.py must alias mb_cmn / use \\N{...}, not raw diacritics: "
        f"{offenders}"
    )
