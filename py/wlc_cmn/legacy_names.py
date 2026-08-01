"""Legacy human-readable names for selected Unicode code points."""

import unicodedata

from mb_diff_mpu.describe_diff import ACCENT_NAMES
from mb_diff_mpu.describe_diff import LETTER_NAMES
from mb_diff_mpu.describe_diff import POINT_NAMES


def legacy_name(string_len_1):
    """Return the legacy human-readable Unicode name for a code point."""
    if name := _VENDORED_NAME_SHORTS.get(string_len_1):
        return name
    return _LEGACY_NAME_SHORTS.get(string_len_1) or unicodedata.name(string_len_1)


_LEGACY_NAME_SHORTS = {
    "\N{SPACE}": "space",
    "\N{COMBINING GRAPHEME JOINER}": "combining-grapheme-joiner",
    "\N{ZERO WIDTH JOINER}": "zero-width-joiner",
    "\N{HEBREW PUNCTUATION MAQAF}": "maqaf",
    "\N{HEBREW PUNCTUATION PASEQ}": "paseq/legarmeih",
    "\N{HEBREW PUNCTUATION SOF PASUQ}": "sof-pasuq",
    "\N{HEBREW MARK UPPER DOT}": "upper-dot",
    "\N{HEBREW MARK LOWER DOT}": "lower-dot",
    "\N{HEBREW PUNCTUATION NUN HAFUKHA}": "nun-hafukha",
}


_VENDORED_NAME_SHORTS = {
    **LETTER_NAMES,
    **ACCENT_NAMES,
    **POINT_NAMES,
}
