"""Rendered-prose lint for plural inflections of romanized Hebrew words.

Vocabulary comes from the maintained Unicode/diff display names, with spelling
aliases for prose and source quotations. This never rewrites or normalizes input.
HTML extraction preserves adjacent inline text and its original line numbers.
Suggested nouns follow the default nouns that the hebrew-prose skill's terminology
reference tables under "Plurals of romanized Hebrew words".
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
_ACCENT_ALIASES = (
    "legarmeh legarmeih etnaxta atnax atnah atnach atnakh atnahta etnahta etnachta "  # translit-ok
    "athnah munax munah munach munakh dexi dehi dekhi tipexa tipeha tiphcha tifcha "  # translit-ok
    "tifha tarxa tarha tarkha tsinnor tsinnorit tsinor zinor sinnor tzinnor segolta "  # translit-ok
    "segol zaqef zakef revia rebia geresh azla metigah metiga oleh ole illuy iluy "
    "yored galgal yerax yerah merka merkha merekha mahpakh mahapakh mehuppak mayela "  # translit-ok
    "ta'am taʿam taam"
).split()
_MARK_ALIASES = (
    "sheva shewa metheg meteg maqaf maqqef makaf makkeph dagesh dages mapiq mappiq "
    "shuruq shureq rafe rafeh paseq pasuq pasoleg hiriq hireq xiriq holam xolam "
    "patah patax qamets qamats qames qamatz kamats qubuts qibbuts qibbus qumus "
    "tsere sere hataf xataf ga'ya gaʿya ga'aya gaya"
).split()

# Ben's default plural nouns, approved 2026-10-14, are tabled in the hebrew-prose
# skill's terminology reference. A letter takes "letters", an accent "accents" and
# any other mark "marks", except for the names below. Each suggestion is still an
# editorial default: the sentence decides, and "marks" fits any written sign.
_LETTERS, _ACCENTS, _MARKS = ("letters",), ("accents",), ("marks",)
_VOWELS, _DOTS = ("vowels",), ("dots",)
_NAME_NOUNS = {
    # A homonym takes the noun of each sense, so that the noun is never ambiguous.
    "segol": ("accents", "vowels"),
    "geresh": ("accents", "marks"),
    "gershayim": ("accents", "marks"),
    # Ben accepts either noun for xiriq.
    **dict.fromkeys(("hiriq", "hireq", "xiriq"), ("vowels", "dots")),
    **dict.fromkeys(("holam", "xolam"), _DOTS),
    **dict.fromkeys(
        "patah patax qamats qamets qames qamatz kamats tsere sere qubuts qibbuts "
        "qibbus qumus shuruq shureq hataf xataf".split(),
        _VOWELS,
    ),
    **dict.fromkeys(("legarmeh", "legarmeih", "ole", "oleh", "yored"), _MARKS),
    "silluq": _ACCENTS,  # shares U+05BD with meteg, which takes "marks"
}
# A compound vowel name takes the noun of its first component: hataf-segol,
# holam-haser-for-vav and qamats-qatan.
_COMPOUND_NOUNS = {
    "hataf": _VOWELS,
    "xataf": _VOWELS,
    "holam": _DOTS,
    "xolam": _DOTS,
    "qamats": _VOWELS,
}
# The kind of mark a Unicode name gives, for a name not in _NAME_NOUNS.
_PREFIX_NOUNS = (
    ("HEBREW LETTER ", _LETTERS),
    ("HEBREW ACCENT ", _ACCENTS),
    ("HEBREW POINT ", _MARKS),
    ("HEBREW PUNCTUATION ", _MARKS),
    ("HEBREW MARK ", _MARKS),
)

# The noun is a default suggestion; an editor chooses words, atoms or another
# context-specific noun from the sentence, not from this lint.
_PROSE_NOUNS = {
    "ketiv": ("words",),
    "ketib": ("words",),
    "qere": ("words",),
    "masorah": ("notes",),
    "aliyah": ("portions",),
    "parashah": (),
    "setumah": ("sections",),
    "petuḥah": ("sections",),
    "petuxah": ("sections",),
    "ḥilluf": ("variants",),
}
# Ben chose parashot as the accepted Hebrew plural in our own prose, so an
# English or Hebrew plural of parashah suggests it.
_ACCEPTED_PLURALS = {"parashah": "parashot"}
_HEBREW_PLURALS = {
    "masorot": ("masorah", ("notes",)),
    "aliyot": ("aliyah", ("portions",)),
    "parashiyot": ("parashot", ()),
    "setumot": ("setumah", ("sections",)),
    "petuḥot": ("petuḥah", ("sections",)),
    "petuxot": ("petuxah", ("sections",)),
    "te'amim": ("ta'am", _ACCENTS),
    "teʿamim": ("taʿam", _ACCENTS),
    "teamim": ("taam", _ACCENTS),
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


def _nouns(name: str, kind_nouns: tuple[str, ...]) -> tuple[str, ...]:
    """The table's nouns for a name, else the nouns of its kind of mark."""
    key = _latin_key(name)
    head = re.split("[- ]", key)[0]
    return _NAME_NOUNS.get(key) or _COMPOUND_NOUNS.get(head) or kind_nouns


def _kind_nouns(character: str) -> tuple[str, ...]:
    """The nouns of a character's kind of mark, read from its Unicode name."""
    full = unicode_data.name(character, "")
    for prefix, nouns in _PREFIX_NOUNS:
        if full.startswith(prefix):
            return nouns
    raise ValueError(f"no plural noun for U+{ord(character):04X} {full!r}")


@lru_cache(maxsize=1)
def vocabulary() -> dict[str, tuple[str, tuple[str, ...]]]:
    """Plural spelling -> (singular spelling, English nouns), derived live."""
    names = {}
    for character, name in diff_mm_uni_name._SHORT_NAMES.items():
        cp = ord(character)
        if 0x591 <= cp <= 0x5EA or cp == 0xFB1E:
            for part in name.split("/"):
                names[part] = _nouns(part, _kind_nouns(character))
    for table in (
        describe_diff.LETTER_NAMES,
        describe_diff.ACCENT_NAMES,
        describe_diff.POINT_NAMES,
        describe_diff.POETIC_ACCENTS,
    ):
        for character, name in table.items():
            names[name] = _nouns(name, _kind_nouns(character))
    for cp in range(0x591, 0x5EA + 1):
        full = unicode_data.name(chr(cp), "")
        for prefix, nouns in _PREFIX_NOUNS:
            if full.startswith(prefix):
                name = full.removeprefix(prefix).lower()
                names[name] = _nouns(name, nouns)
    names.update((name, _LETTERS) for name in _LETTER_ALIASES)
    names.update((name, _nouns(name, _ACCENTS)) for name in _ACCENT_ALIASES)
    names.update((name, _nouns(name, _MARKS)) for name in _MARK_ALIASES)
    names.update(_PROSE_NOUNS)
    # Generic English tails (dot, helper, accent) already pluralize correctly.
    names = {
        name: nouns
        for name, nouns in names.items()
        if not name.endswith(("dot", "helper", "accent", "circle", "vowel", "-sh"))
    }
    # A compound's final name component is checked too: final-kafs, zaqef-qatans,
    # and sof-pasuqs, across hyphens or inline formatting. A full name keeps its
    # own noun (vav is a letter, whatever holam-haser-for-vav takes), and a
    # component whose compounds disagree, as qatan does, takes "marks".
    full_keys = {_latin_key(name) for name in names}
    components = {}
    for name, nouns in names.items():
        component = name.split("-")[-1]
        if component not in (name, "na") and _latin_key(component) not in full_keys:
            components.setdefault(component, set()).add(nouns)
    spellings = dict(names)
    for component, nouns in components.items():
        spellings[component] = nouns.pop() if len(nouns) == 1 else _MARKS
    result = {}
    for spelling, nouns in spellings.items():
        value = (spelling, nouns)
        if spelling in _ACCEPTED_PLURALS:
            value = (_ACCEPTED_PLURALS[spelling], ())
        for suffix in ("s", "es", "im", "ot"):
            result[_latin_key(spelling + suffix)] = value
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
        singular, nouns = names[key]
        if key.startswith(_latin_key(singular)):
            suffix = key.removeprefix(_latin_key(singular))
            singular = term[: -len(suffix)]
        elif term.isupper():
            singular = singular.upper()
        elif term[0].isupper():
            singular = singular[0].upper() + singular[1:]
        # A name with two default nouns suggests both: "segol accents or segol vowels".
        preferred = " or ".join(f"{singular} {noun}" for noun in nouns) or singular
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
