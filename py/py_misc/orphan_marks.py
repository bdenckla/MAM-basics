"""Closed artificial-carrier shapes used by the near-Aleppo dataset.

The original GA shape remains unchanged. The explicit GV variant retains the
chosen artificial VAV + HOLAM. The explicit GD variant uses a dalet for the
final-nun marks at Isaiah 54:16, without a space. No carrier is a ketiv consonant.
Build validation and edition display use the same carrier validation.
"""

MARKS_WITHOUT_LETTER = "ניקוד בלי אות"
MARKS_WITHOUT_LETTER_OR_SPACE = "ניקוד בלי אות ובלי רווח"
GV_PARAMETER = "carrier"
GD_VARIANT = "final-nun-dalet"
GD_CARRIER = (
    "\N{HEBREW LETTER DALET}\N{HEBREW POINT DAGESH OR MAPIQ}"
    "\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MAHAPAKH}"
)
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
    """Return validated carriers from an explicitly named GA, GV or GD shape."""
    if set(tmpl) != {"tmpl_name", "tmpl_params"}:
        raise AssertionError(f"{label}: unexpected orphan-template fields")
    params = tmpl["tmpl_params"]
    if tmpl["tmpl_name"] == MARKS_WITHOUT_LETTER_OR_SPACE:
        if (
            set(params) != {"1", GV_PARAMETER}
            or params[GV_PARAMETER] != GD_VARIANT
            or params["1"] != GD_CARRIER
        ):
            raise AssertionError(
                f"{label}: GD requires final-nun-dalet and exactly "
                "artificial DALET + DAGESH + TSERE + MAHAPAKH"
            )
        return GD_CARRIER
    if tmpl["tmpl_name"] != MARKS_WITHOUT_LETTER or set(params) not in (
        {"1"},
        {"1", GV_PARAMETER},
    ):
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
