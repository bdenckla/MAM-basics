from __future__ import annotations

# MAM template names historically used ASCII quotes as an internal shorthand,
# but MAM-parsed now emits the typographically-correct Hebrew punctuation:
# gershayim (U+05F4) for the double quote and geresh (U+05F3) for the single.
# The hardcoded template-name literals throughout this repo are still written
# with the ASCII forms, so we fold the Hebrew punctuation back to ASCII *for
# comparison only*. Callers keep the original (gershayim) name for any stored
# or rendered value, preserving fidelity to the upstream representation.
_GERSHAYIM = "\N{HEBREW PUNCTUATION GERSHAYIM}"  # U+05F4 -> ASCII '"'
_GERESH = "\N{HEBREW PUNCTUATION GERESH}"  # U+05F3 -> ASCII "'"


def canonical_template_name(name: str | None) -> str | None:
    """Fold Hebrew gershayim/geresh in a template name to ASCII quotes so it
    matches this repo's ASCII-quote template-name literals.

    Use only for comparison; the returned value must not be stored back into
    output, so that emitted names keep upstream's Hebrew-punctuation spelling.
    ``None`` passes through unchanged.
    """
    if name is None:
        return None
    return name.replace(_GERSHAYIM, '"').replace(_GERESH, "'")
