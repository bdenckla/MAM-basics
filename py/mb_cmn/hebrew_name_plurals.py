"""Rendered-prose lint for plural inflections of romanized Hebrew words.

Vocabulary comes from the maintained Unicode/diff display names, with spelling
aliases for prose and source quotations. This never rewrites or normalizes input.
HTML extraction preserves adjacent inline text and its original line numbers.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from html.parser import HTMLParser
import re
import unicodedata

from mb_cmn import unicode_data
from mb_diff_mpu import describe_diff
from pydiff_mm import diff_mm_uni_name

# These are spelling aliases, not recommended spellings.  # translit-ok
_LETTER_ALIASES = "aleph beth gimmel daleth heh hey waw vau yodh het chet kaph lamedh samech tsade tzadi tzade sadi sade kof quf taw".split()
_MARK_ALIASES = (
    "sheva shewa metheg meteg maqaf maqqef makaf makkeph dagesh dages mapiq mappiq "
    "shuruq shureq rafe rafeh paseq pasuq legarmeh legarmeih etnaxta atnax "
    "atnah atnach atnakh atnahta etnahta etnachta athnah munax munah munach munakh "  # translit-ok
    "dexi dehi dekhi tipexa tipeha tiphcha tifcha tifha tarxa tarha tarkha "  # translit-ok
    "hiriq hireq xiriq holam xolam patah patax qamets qamats qames qamatz kamats "
    "qubuts qibbuts qibbus qumus tsere sere tsinnor tsinnorit tsinor zinor sinnor tzinnor "  # translit-ok
    "segolta segol zaqef zakef revia rebia geresh azla metigah metiga "
    "oleh ole illuy iluy yored galgal yerax yerah merka merkha merekha mahpakh "  # translit-ok
    "mahapakh mehuppak ga'ya gaʿya ga'aya gaya mayela"  # translit-ok
).split()

# The noun is a default suggestion; an editor chooses forms/readings/words
# (and similar context-specific nouns) from the sentence, not from this lint.
_PROSE_NOUNS = {
    "ketiv": "forms",
    "ketib": "forms",
    "qere": "forms",
    "masorah": "notes",
    "aliyah": "portions",
    "parashah": "sections",
    "setumah": "sections",
    "petuḥah": "sections",
    "petuxah": "sections",
    "ḥilluf": "variants",
}
_HEBREW_PLURALS = {
    "masorot": ("masorah", "notes"),
    "aliyot": ("aliyah", "portions"),
    # Ben chose parashot as the accepted Hebrew plural in our own prose.
    "parashiyot": ("parashot", ""),
    "setumot": ("setumah", "sections"),
    "petuḥot": ("petuḥah", "sections"),
    "petuxot": ("petuxah", "sections"),
}

# Ambiguous ordinary English words require an explicit letter context. Other
# unknown transliterations remain a human review task, not a blanket suffix ban.
_AMBIGUOUS = {"bets", "hes", "heys", "nuns", "shins", "sins", "taws", "tets"}
_WORD = re.compile(
    r"[A-Za-zÀ-ɏ\u1e00-\u1effʾʿ][A-Za-zÀ-ɏ\u1e00-\u1effʾʿ\u0300-\u036f'’\-]*"
)
_INLINE_SUFFIX = re.compile(r">(?:[\s\u2009\u200a]|<[^>]+>)*(?:s|es|im|ot)\b", re.I)


@lru_cache(maxsize=8192)
def _latin_key(text: str) -> str:
    """Fold only Latin spellings for lookup; Hebrew input is never normalized."""
    pieces = []
    for char in text.lower().replace("’", "'"):
        if "LATIN" in unicodedata.name(char, ""):
            pieces.extend(
                c
                for c in unicodedata.normalize("NFD", char)
                if not unicodedata.combining(c)
            )
        elif not unicodedata.combining(char):
            pieces.append(char)
    return "".join(pieces)


@lru_cache(maxsize=1)
def vocabulary() -> dict[str, tuple[str, str]]:
    """Plural spelling -> (singular spelling, English noun), derived live."""
    names = {}
    for character, name in diff_mm_uni_name._SHORT_NAMES.items():
        cp = ord(character)
        if 0x591 <= cp <= 0x5EA or cp == 0xFB1E:
            for part in name.split("/"):
                names[part] = "letters" if 0x5D0 <= cp <= 0x5EA else "marks"
    for table, noun in (
        (describe_diff.LETTER_NAMES, "letters"),
        (describe_diff.ACCENT_NAMES, "marks"),
        (describe_diff.POINT_NAMES, "marks"),
        (describe_diff.POETIC_ACCENTS, "marks"),
    ):
        names.update((name, noun) for name in table.values())
    for cp in range(0x591, 0x5EA + 1):
        full = unicode_data.name(chr(cp), "")
        for prefix, noun in (
            ("HEBREW LETTER ", "letters"),
            ("HEBREW POINT ", "marks"),
            ("HEBREW ACCENT ", "marks"),
            ("HEBREW PUNCTUATION ", "marks"),
        ):
            if full.startswith(prefix):
                names[full.removeprefix(prefix).lower()] = noun
    names.update((name, "letters") for name in _LETTER_ALIASES)
    names.update((name, "marks") for name in _MARK_ALIASES)
    names.update(_PROSE_NOUNS)
    result = {}
    for name, noun in names.items():
        # Generic English tails (dot, helper, accent) already pluralize correctly.
        if any(
            name.endswith(tail)
            for tail in ("dot", "helper", "accent", "circle", "vowel", "-sh")
        ):
            continue
        # A compound's final name component is checked too: final-kafs,
        # zaqef-qatans, and sof-pasuqs, across hyphens or inline formatting.
        for spelling in {name, name.split("-")[-1]}:
            if spelling == "na":
                continue
            for suffix in ("s", "es", "im", "ot"):
                result[_latin_key(spelling + suffix)] = (spelling, noun)
    result.update(
        (_latin_key(plural), value) for plural, value in _HEBREW_PLURALS.items()
    )
    return result


@dataclass(frozen=True)
class Finding:
    line: int
    term: str
    preferred: str


def text_findings(text: str, lines: list[int]) -> list[Finding]:
    """Detect standalone names, allowing diacritics and an inline thin-space s."""
    names = vocabulary()
    findings = []
    for match in _WORD.finditer(text):
        term = match.group()
        key = _latin_key(term)
        if key not in names:
            continue
        # Paths, identifiers, URLs and apostrophe-s possessives are not prose plurals.
        if is_technical_reference(text, match):
            continue
        if key in _AMBIGUOUS and not re.search(
            r"\b(?:Hebrew|letters?)\b",
            text[max(0, match.start() - 40) : match.end() + 40],
            re.I,
        ):
            continue
        singular, noun = names[key]
        if key.startswith(_latin_key(singular)):
            suffix = key.removeprefix(_latin_key(singular))
            singular = term[: -len(suffix)]
        elif term.isupper():
            singular = singular.upper()
        elif term[0].isupper():
            singular = singular[0].upper() + singular[1:]
        preferred = singular + (" " + noun if noun else "")
        findings.append(Finding(lines[match.start()], term, preferred))
    return findings


def is_technical_reference(text: str, match: re.Match[str]) -> bool:
    """Exclude identifier/path tokens, not sentence-final punctuation."""
    left = text[match.start() - 1 : match.start()] if match.start() else ""
    right = text[match.end() : match.end() + 1]
    return (
        left in {"_", "/", "\\", ".", "@", "·", "-"}
        or right in {"_", "/", "\\", "·", "-"}
        or (right == "." and text[match.end() + 1 : match.end() + 2].isalnum())
    )


class _Prose(HTMLParser):
    """Read text and prose attributes, excluding explicitly scoped registers."""

    _SKIP = {"script", "style", "code", "pre", "samp", "kbd", "blockquote", "q"}
    _VOID = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
    _INLINE = {
        "a",
        "span",
        "em",
        "i",
        "b",
        "strong",
        "abbr",
        "bdi",
        "wbr",
        "sup",
        "sub",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.text = []
        self.lines = []

    def _add(self, text, line):
        # Hair/thin spaces are used between italic names and English endings.
        for char in text:
            if char not in "\u2009\u200a":
                self.text.append(char)
                self.lines.append(line)
            line += char == "\n"

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        skip_all = bool(self.stack and self.stack[-1][2]) or tag in self._SKIP
        skip = skip_all or bool(self.stack and self.stack[-1][1])
        skip |= attrs.get("lang", "").startswith("hbo")
        if "data-hebrew-plural-ok" in attrs:
            assert attrs["data-hebrew-plural-ok"], "plural exception needs a reason"
            skip = skip_all = True
        if tag not in self._INLINE or skip:
            self._add(" ", self.getpos()[0])
        # Hebrew elements can still have English hover/screen-reader prose.
        if not skip_all:
            for attr in ("alt", "title", "aria-label", "aria-description"):
                if attrs.get(attr):
                    self._add(" " + attrs[attr] + " ", self.getpos()[0])
        if tag not in self._VOID:
            self.stack.append((tag, skip, skip_all))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self._VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                skipped = self.stack[i][1]
                del self.stack[i:]
                if tag not in self._INLINE or skipped:
                    self._add(" ", self.getpos()[0])
                break

    def handle_data(self, data):
        if not self.stack or not self.stack[-1][1]:
            self._add(data, self.getpos()[0])


# Verbatim UXLC and Holman source passages, not authored explanatory commentary.
_QUOTATIONS = {
    "gh-pages/clc/Proverbs.html": (
        "five yods and no Masorah circle is present to indicate which yod is superfluous",
    ),
    "gh-pages/clc/Genesis.html": (
        "The Masora Circle over the word refers to the number '4' in the left margin.",
    ),
    "gh-pages/holman/uxlc_corrections.html": (
        "where two Merekhas serve Legarmeh",
        "Revise note that other editions read with one or two Merekhas.",
        "HUB and MAM read with two Merekhas.",
        "BREUER lists A and L as reading with two MEREKHAS on this word.",
        "Many of these Merekhas appear to be carryovers from the BHS.",
    ),
}

_SOURCE_TITLES = {
    **{
        f"gh-pages/MAM-with-doc/misc/{name}.html": ("Miqra al pi ha-Masora edition",)
        for name in (
            "he_ws_intro_to_mam_gaya_text",
            "he_ws_intro_to_mam_gray_maqaf_1",
            "he_ws_intro_to_mam_pasleg",
        )
    },
    "gh-pages/aleppo/missing_sections_torah.html": (
        "Mavo le-Miqra ʿal pi ha-Masora, Pereq Gimel",
    ),
    "gh-pages/aleppo/missing_sections_nakh.html": (
        "Mavo le-Miqra ʿal pi ha-Masora, Pereq Dalet",
    ),
}

# Ben permits aliyot in this technical document only.
_PAGE_TERM_EXCEPTIONS = {
    "gh-pages/MAM-with-doc/misc/notes_on_aliyot.html": {"aliyot"},
}


def authored_html_text(html: str, relative_path: str) -> tuple[str, list[int]]:
    """Shared quote/adaptation/code exclusions for the two rendered-prose lints."""
    if (
        relative_path.startswith("gh-pages/yeivin-itm/")
        or relative_path == "gh-pages/yeivin_itm.html"
        # Phonetic MAM's chapter pages are generated transcriptions, untagged by
        # lang, with only navigation in English. Its testsuite pages stay checked.
        or relative_path.startswith("gh-pages/phonetic-mam/tnkh/")
    ):
        return "", []
    parser = _Prose()
    parser.feed(html)
    parser.close()
    text = "".join(parser.text)
    # Narrow exceptions retain line positions instead of suppressing a whole page.
    for quotation in (
        *_QUOTATIONS.get(relative_path, ()),
        *_SOURCE_TITLES.get(relative_path, ()),
    ):
        text = text.replace(quotation, " " * len(quotation))
    return text, parser.lines


def html_findings(html: str, relative_path: str) -> list[Finding]:
    """Check plurals in authored prose, respecting narrow term exceptions."""
    # Most pages contain Scripture only. Token lookup avoids parsing those pages;
    # the second arm also admits suffixes separated from their name by markup.
    names = vocabulary()
    if not _INLINE_SUFFIX.search(html) and not any(
        _latin_key(match.group()) in names for match in _WORD.finditer(html)
    ):
        return []
    text, lines = authored_html_text(html, relative_path)
    permitted = _PAGE_TERM_EXCEPTIONS.get(relative_path, set())
    return [
        finding
        for finding in text_findings(text, lines)
        if _latin_key(finding.term) not in permitted
    ]
