"""Text normalization shared by the parser, the emitter and the verifier.

Google Docs prose arrives with NBSPs, zero-width characters, soft hyphens,
double-space-after-period, and Latin diacritics in whichever composition the
author's keyboard happened to produce. ``mb_html._do_space_asserts`` forbids
leading/trailing whitespace and double spaces inside element contents, so
every one of those has to go before an ``htel_mk`` call ever sees the text.

The Latin composition rule deliberately is *not* a blanket
``unicodedata.normalize("NFC", ...)``: a blanket NFC pass reorders Hebrew
combining marks against this repo's own deliberate non-Unicode-standard mark
order (see ``mb_cmn/uni_denorm.py`` ``give_std_mark_order``). Only Latin
base + diacritic clusters get composed, matching the rule that
``py/tests/test_h_dot_below_nfc.py`` enforces over the tree.
"""

import re
import unicodedata

# Codepoints that carry no meaning in Ben's prose and only break the space
# asserts or the word diff. Spelled with named escapes rather than pasted:
# every one of them is invisible in a source file.
_TO_SPACE = (
    "\N{NO-BREAK SPACE}",
    "\N{NARROW NO-BREAK SPACE}",
)
_TO_DROP = (
    "\N{ZERO WIDTH SPACE}",
    "\N{ZERO WIDTH NO-BREAK SPACE}",  # also the UTF-8 BOM
    "\N{SOFT HYPHEN}",
    "\N{WORD JOINER}",
)
# Deliberately NOT dropped: ZWJ / ZWNJ (U+200D / U+200C). Those can be
# authored on purpose in Hebrew (author.py has a $ZWJ key), so the inventory
# reports them instead of silently deleting them.

_HEBREW_RANGES = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))
_HEBREW_RE = re.compile("[֐-׿יִ-ﭏ]")
_LATIN_LETTER_RE = re.compile("[A-Za-z]")

_TRANSLATE = {ord(c): " " for c in _TO_SPACE}
_TRANSLATE.update({ord(c): None for c in _TO_DROP})


def norm_text(text: str) -> str:
    """Normalize a run of text, preserving its leading/trailing single space.

    Interior whitespace runs collapse to one space. Whether the run started
    or ended with space is preserved, because inter-span spacing is how
    Google separates words split across ``<span>`` boundaries.
    """
    if text is None:
        return ""
    text = text.translate(_TRANSLATE)
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\t", " ")
    text = compose_latin_diacritics(text)
    if not text.strip():
        return " " if text else ""
    lead = " " if text[:1].isspace() else ""
    trail = " " if text[-1:].isspace() else ""
    return lead + " ".join(text.split()) + trail


def norm_block(text: str) -> str:
    """Normalize a whole block: as ``norm_text``, but also edge-stripped."""
    return norm_text(text).strip()


def compose_latin_diacritics(text: str) -> str:
    """NFC-compose Latin base + combining mark clusters only.

    Hebrew clusters are left byte-identical. This is the composing twin of
    ``_find_decomposed_latin_clusters`` in ``py/tests/test_h_dot_below_nfc.py``,
    which is the lint that would otherwise fail on the emitted modules.
    """
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if _is_latin_base(ch) and i + 1 < n and unicodedata.combining(text[i + 1]) != 0:
            j = i + 1
            while (
                j < n
                and unicodedata.combining(text[j]) != 0
                and not _is_hebrew_cp(text[j])
            ):
                j += 1
            cluster = text[i:j]
            nfc = unicodedata.normalize("NFC", cluster)
            use_nfc = len(nfc) < len(cluster) and not any(_is_hebrew_cp(c) for c in nfc)
            out.append(nfc if use_nfc else cluster)
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def has_hebrew(text: str) -> bool:
    return bool(_HEBREW_RE.search(text or ""))


def is_all_hebrew(text: str) -> bool:
    """True if the text has Hebrew and no Latin letters."""
    if not has_hebrew(text):
        return False
    return not _LATIN_LETTER_RE.search(text)


def words(text: str):
    """Split normalized text into a word list, for the differential diff."""
    return norm_block(text).split()


###########################################################


def _is_hebrew_cp(ch) -> bool:
    code = ord(ch)
    return any(lo <= code <= hi for lo, hi in _HEBREW_RANGES)


def _is_latin_base(ch) -> bool:
    if unicodedata.combining(ch) != 0:
        return False
    try:
        return unicodedata.name(ch).startswith("LATIN")
    except ValueError:
        return False
