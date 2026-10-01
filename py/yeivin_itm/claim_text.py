"""Deferred numerical text, resolved only from the renderer's validated claims.

The content modules remain declarative and perform no input reads at import time.
Formatting is applied once to the exact fraction, avoiding double rounding.
"""

import re

from yeivin_itm.claim_schema import APPROVED_FRACTIONS

_TOKEN = re.compile(r"\{\{meteg:([A-Za-z0-9.-]+)\|([a-z]+)\|([a-z]+)\}\}")
_FIELDS = ("numerator", "denominator", "percentage")
_STYLES = ("integer", "comma", "word", "percent", "decimal")
_SMALL_NUMBERS = ("zero", "one", "two", "three", "four", "five", "six")


def claim_text(name, field, style="integer"):
    """Return a strict named placeholder, without reading or calculating data."""
    if name not in APPROVED_FRACTIONS or field not in _FIELDS or style not in _STYLES:
        raise ValueError(f"Unknown Yeivin claim reference: {name}/{field}/{style}")
    if field == "percentage" and style not in ("integer", "percent", "decimal"):
        raise ValueError("Percentage claims require numerical percentage formatting")
    return f"{{{{meteg:{name}|{field}|{style}}}}}"


def resolve(text, claims):
    """Substitute each declared reference; reject any unresolved claim marker."""

    def replacement(match):
        name, field, style = match.groups()
        claim_text(name, field, style)
        value = claims["measurements"][name][field]
        if style == "integer":
            return f"{value:.0f}"
        if style == "comma":
            return f"{value:,}"
        if style == "word":
            if type(value) is not int or not 0 <= value < len(_SMALL_NUMBERS):
                raise ValueError(f"Claim no longer has a supported word form: {name}")
            return _SMALL_NUMBERS[value]
        if style == "percent":
            return f"{value:.0f}%"
        if style == "decimal":
            return f"{value:.1f}"
        raise ValueError(f"Unknown claim format: {style}")

    result = _TOKEN.sub(replacement, text)
    if "{{meteg:" in result:
        raise ValueError("Unresolved Yeivin meteg claim")
    return result
