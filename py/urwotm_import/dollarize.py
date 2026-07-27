"""$-substitution, driven by ``author._DOLLAR_SUB_DISPATCH`` itself.

Two different questions get asked of the dispatch, and conflating them is the
easy mistake:

1. **"Will ``dollar_sub`` raise on this text?"** ``_check_no_undollared``
   scans for the *key* with its ``$`` stripped -- so ``$ah`` makes a bare
   English "ah" illegal, and ``$xolam`` makes a bare "xolam" illegal while
   saying nothing at all about the rendered spelling "ḥolam".
   :func:`lint_hits` answers this with the identical regex, so "will this
   raise" is definitionally the same question.

2. **"Which key renders this text?"** The Google source already italicizes
   accent names, and an italic run reading "ḥolam" should become ``$xolam``.
   That is a lookup on the dispatch's rendered *value*, not on its key.
   :func:`key_for_rendered` answers this one.
"""

import re

from mb_author import author
from mb_misc import mb_html

# Keys whose undollared form is also an ordinary English word (or an
# abbreviation that collides with one). Substituting one of these silently
# italicizes an English word as a Hebrew letter name, so every hit gets
# reported with context and an "XXX REVIEW" marker for Ben rather than being
# quietly accepted. ($hehe exists in _ROMANIZED for exactly this reason: the
# Hebrew letter name "he" collided with the English pronoun.)
AMBIGUOUS_KEYS = frozenset(
    (
        # Ordinary English words.
        "$sin",
        "$ah",
        "$nun",
        "$shin",
        "$one",
        # Short letter names that read as English fragments or initials.
        "$pe",
        "$mem",
        "$vav",
        "$bet",
        "$malei",
        # Two-letter abbreviations that also occur as plain initials.
        "$TM",
        "$FS",
        "$JC",
        "$MG",
        "$AC",
        "$LC",
        "$JP",
    )
)


def dispatch_keys():
    return [k for k in author._DOLLAR_SUB_DISPATCH if k.startswith("$")]


def lint_regex(key: str):
    """The exact regex ``_check_no_undollared`` uses for this key.

    The lookbehind excludes combining marks U+0300-U+036F, which would
    otherwise create an artificial word boundary mid-cluster.
    """
    undollared = re.escape(key[1:])
    return re.compile(rf"(?<!\$)(?<![\u0300-\u036F])\b{undollared}\b")


def lint_hits(text: str):
    """Every bare occurrence that would make ``dollar_sub`` raise.

    Returns a list of ``(key, start, end)``, longest match first at a given
    position so that ``$xolam_xaser`` wins over a hypothetical ``$xolam``.
    """
    hits = []
    for key in dispatch_keys():
        for match in lint_regex(key).finditer(text):
            hits.append((key, match.start(), match.end()))
    hits.sort(key=lambda h: (h[1], -(h[2] - h[1])))
    return _drop_overlaps(hits)


def substitute(text: str) -> str:
    """Replace every lint-triggering bare occurrence with its ``$`` key."""
    out = []
    pos = 0
    for key, start, end in lint_hits(text):
        out.append(text[pos:start])
        out.append(key)
        pos = end
    out.append(text[pos:])
    return "".join(out)


def key_for_rendered(text: str):
    """The dispatch key whose rendered text equals ``text``, or None.

    Prefers a key whose name matches its own rendering (``$qadma`` over a
    hypothetical alias), then the shortest key, so the choice is stable.
    """
    candidates = _rendered_index().get(text.strip())
    if not candidates:
        return None
    return sorted(candidates, key=lambda k: (k[1:] != text.strip().lower(), len(k)))[0]


def rendered_text(key: str) -> str:
    """The plain text ``key`` renders to."""
    return _htel_text(author._DOLLAR_SUB_DISPATCH[key])


def classify(key: str, matched: str) -> str:
    """Which review bucket a bare hit falls into.

    ``"retext"`` is the dangerous one: the key renders as text *different*
    from what it matched, so substituting silently rewrites the prose. ``$AH``
    is the live example -- it renders the Unicode character name
    "ATNAH HAFUKH", while Part 4 uses a bare "AH" as its own abbreviation
    throughout.
    """
    if rendered_text(key).strip() != matched.strip():
        return "retext"
    return "ambiguous" if key in AMBIGUOUS_KEYS else "auto"


def cap_key_missing(word: str):
    """For a capitalized word, the cap key that would be needed but is absent.

    Sentence-initial "Qadma" needs a ``$Qadma`` key that ``_rom_with_cap``
    would have to create. Returns that key name when the lowercase key exists
    but its capitalized twin does not; otherwise None.
    """
    lower_key = "$" + word[:1].lower() + word[1:]
    upper_key = "$" + word[:1].upper() + word[1:]
    dispatch = author._DOLLAR_SUB_DISPATCH
    if lower_key in dispatch and upper_key not in dispatch:
        return upper_key
    return None


###########################################################

_RENDERED_INDEX = None


def _rendered_index():
    global _RENDERED_INDEX
    if _RENDERED_INDEX is None:
        index = {}
        for key in dispatch_keys():
            text = rendered_text(key).strip()
            if text:
                index.setdefault(text, []).append(key)
        _RENDERED_INDEX = index
    return _RENDERED_INDEX


def _htel_text(value) -> str:
    if isinstance(value, str):
        return value
    if mb_html.is_htel(value):
        return _htel_text(value.get("contents") or [])
    if isinstance(value, (list, tuple)):
        return "".join(_htel_text(v) for v in value)
    return ""


def _drop_overlaps(hits):
    out = []
    last_end = -1
    for key, start, end in hits:
        if start < last_end:
            continue
        out.append((key, start, end))
        last_end = end
    return out
