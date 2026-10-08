"""Closed artificial-carrier shapes used by the near-Aleppo dataset.

Both orphan names accept the original GA shape and the explicit GV variant, retaining the
chosen artificial VAV + HOLAM; neither carrier letter is a ketiv consonant.
Build validation and edition display use the same carrier validation.
"""

MARKS_WITHOUT_LETTER = "ניקוד בלי אות"
MARKS_WITHOUT_LETTER_OR_SPACE = "ניקוד בלי אות ובלי רווח"
GV_PARAMETER = "carrier"
GV_VARIANT = "holam-male-vav"
GV_CARRIER = "\N{HEBREW LETTER VAV}\N{HEBREW POINT HOLAM}"
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
    """Return validated carriers from an explicitly named GA or GV shape."""
    if set(tmpl) != {"tmpl_name", "tmpl_params"}:
        raise AssertionError(f"{label}: unexpected orphan-template fields")
    params = tmpl["tmpl_params"]
    name = tmpl["tmpl_name"]
    keysets = (
        ({"1"}, {"1", GV_PARAMETER})
        if name in (MARKS_WITHOUT_LETTER, MARKS_WITHOUT_LETTER_OR_SPACE)
        else ()
    )
    if set(params) not in keysets:
        raise AssertionError(f"{label}: unsupported orphan-template shape")
    value = params["1"]
    if GV_PARAMETER in params:
        if params[GV_PARAMETER] != GV_VARIANT or value != GV_CARRIER:
            raise AssertionError(f"{label}: GV requires exactly artificial VAV + HOLAM")
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
