"""Text normalization, so both sides of the differential check compare.

Google Docs prose arrives with NBSPs, zero-width characters, soft hyphens,
double-space-after-period, and Latin diacritics in whichever composition the
author's keyboard happened to produce. None of that carries meaning in Ben's
prose, and every one of it would otherwise read as a word-level difference
between the frozen source text and the generated page. Both sides go through
here, so a difference that survives is a real one.

The Latin composition rule deliberately is *not* a blanket
``unicodedata.normalize("NFC", ...)``: a blanket NFC pass reorders Hebrew
combining marks against this repo's own deliberate non-Unicode-standard mark
order (see ``mb_cmn/uni_denorm.py`` ``give_std_mark_order``). Only Latin
base + diacritic clusters get composed, matching the rule that
``py/tests/test_h_dot_below_nfc.py`` enforces over the tree.
"""

import unicodedata

# Codepoints that carry no meaning in Ben's prose and only break the word
# diff. Spelled with named escapes rather than pasted: every one of them is
# invisible in a source file.
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
# authored on purpose in Hebrew (author.py has a $ZWJ key), so dropping them
# here would hide a page that had gained or lost one.

_HEBREW_RANGES = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))

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
    ``_find_decomposed_latin_clusters`` in ``py/tests/test_h_dot_below_nfc.py``:
    the vendored source text is this function's output, which is why that lint
    passes over ``src/`` though Google supplied the diacritics decomposed.
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
