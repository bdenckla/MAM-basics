"""Closed artificial-carrier shapes used by the near-Aleppo dataset.

Both carrier names accept the original GA shape and the GV payload,
retaining the chosen artificial VAV + HOLAM. The explicit GD variant uses a dalet
for the final-nun marks at Isaiah 54:16, without a space. The mixed alef/vav variant
at 2 Kings 19:31 retains three alef carriers followed by VAV + HOLAM under the
original carrier name only. No carrier is a ketiv consonant.
Build validation and edition display use the same carrier validation.
An alef payload has tsere and merkha without space
at 2 Samuel 18:20. A separate parameterless template records space without marks.
"""

MARKS_WITHOUT_LETTER = "ניקוד בלי אות"
MARKS_WITHOUT_LETTER_OR_SPACE = "ניקוד בלי אות ובלי רווח"
SPACE_WITHOUT_MARKS = "רווח בלי ניקוד"
ORPHAN_ALEF_CARRIER = (
    "\N{HEBREW LETTER ALEF}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MERKHA}"
)
GD_CARRIER = (
    "\N{HEBREW LETTER DALET}\N{HEBREW POINT DAGESH OR MAPIQ}"
    "\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MAHAPAKH}"
)
GV_CARRIER = "\N{HEBREW LETTER VAV}\N{HEBREW POINT HOLAM}"
GAV_CARRIER = "אְאָא֖וֹ"
_ALEF = "\N{HEBREW LETTER ALEF}"
_DAGESH = "\N{HEBREW POINT DAGESH OR MAPIQ}"
_MARKS = (
    frozenset(chr(c) for c in range(0x0591, 0x05C8))
    - {
        "\N{HEBREW PUNCTUATION MAQAF}",
        "\N{HEBREW PUNCTUATION PASEQ}",
        "\N{HEBREW PUNCTUATION SOF PASUQ}",
        "\N{HEBREW PUNCTUATION NUN HAFUKHA}",
        _DAGESH,
    }
) | {"\N{COMBINING GRAPHEME JOINER}"}


def carriers(tmpl, label):
    """Return validated GA, GV, GD, mixed alef/vav or no-space alef carriers."""
    if set(tmpl) != {"tmpl_name", "tmpl_params"}:
        raise AssertionError(f"{label}: unexpected orphan-template fields")
    params = tmpl["tmpl_params"]
    name = tmpl["tmpl_name"]
    if name not in (
        MARKS_WITHOUT_LETTER,
        MARKS_WITHOUT_LETTER_OR_SPACE,
    ) or set(
        params
    ) != {"1"}:
        raise AssertionError(f"{label}: unsupported orphan-template shape")
    value = params["1"]
    allowed = {GV_CARRIER}
    if name == MARKS_WITHOUT_LETTER:
        allowed.add(GAV_CARRIER)
    elif name == MARKS_WITHOUT_LETTER_OR_SPACE:
        allowed.add(GD_CARRIER)
    if isinstance(value, str) and value in allowed:
        return value
    if not isinstance(value, str) or not value.startswith(_ALEF):
        raise AssertionError(f"{label}: GA does not open with a carrier alef")
    for index, char in enumerate(value):
        if char == _ALEF:
            if index + 1 == len(value) or value[index + 1] == _ALEF:
                raise AssertionError(f"{label}: a carrier alef with no marks")
        elif char == _DAGESH:
            raise AssertionError(f"{label}: a dagesh on a carrier alef")
        elif char not in _MARKS:
            raise AssertionError(
                f"{label}: {char!r} is neither a carrier alef nor a mark"
            )
    return value


def validate_space(tmpl, label):
    """The body-space template has no marks, carrier or child Scripture."""
    if tmpl != {"tmpl_name": SPACE_WITHOUT_MARKS}:
        raise AssertionError(f"{label}: unexpected space-without-marks shape")


def validate_body(tmpl, label):
    """Validate one explicitly selected qere-without-ketiv body template."""
    name = tmpl["tmpl_name"]
    if name == SPACE_WITHOUT_MARKS:
        validate_space(tmpl, label)
    elif name == MARKS_WITHOUT_LETTER:
        carriers(tmpl, label)
    elif name == MARKS_WITHOUT_LETTER_OR_SPACE:
        carriers(tmpl, label)
        if tmpl["tmpl_params"]["1"] != ORPHAN_ALEF_CARRIER:
            raise AssertionError(
                f"{label}: a no-space qere-without-ketiv body requires {ORPHAN_ALEF_CARRIER!r}"
            )
    else:
        raise AssertionError(f"{label}: unknown body template {name!r}")
