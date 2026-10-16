"""Lint preferred spellings in every registered Near-Aleppo documentation page.

The source denylist in test_transliterations.py does not cover every vowel name.
This check reads rendered prose, including headings and prose attributes, so
source literals, interpolated values and the shared consumer notice are covered.
The vocabulary includes Ben's preference for rafeh. ASCII identifiers,
literal Unicode names and source quotations retain their own
spellings. Prose compounds remain checked, including names joined by hyphens.
This scope does not claim to audit other products' legacy prose.
"""

import re

from mb_cmn import hebrew_name_plurals as html_prose
from mb_cmn import paths, unicode_data
from mb_diff_mpu import describe_diff
from near_aleppo import doc_pages


def _variants():
    names = {"tarḥa", "ḥumash", "taḥton", *html_prose._PROSE_NOUNS}
    for table in (
        describe_diff.LETTER_NAMES,
        describe_diff.ACCENT_NAMES,
        describe_diff.POINT_NAMES,
        describe_diff.POETIC_ACCENTS,
    ):
        names.update(part for name in table.values() for part in name.split("-"))
    return {
        name.replace("ḥ", replacement): name
        for name in names
        if "ḥ" in name
        for replacement in ("h", "x", "h" + "\N{COMBINING DOT BELOW}")
    }


_VARIANTS = {**_variants(), "rafe": "rafeh"}
_PATTERN = re.compile(
    r"(?<!\w)(?:" + "|".join(map(re.escape, _VARIANTS)) + r")(?!\w)", re.I
)
# A complete Unicode name is literal vocabulary. A short name is exempt only
# inside a carrier formula or the bounded payload citations below.
_UNICODE_NAMES = set()
_LETTER_NAMES = set()
_MARK_NAMES = set()
for _cp in range(0x0590, 0x0600):
    _name = unicode_data.name(chr(_cp), "")
    if _name:
        _UNICODE_NAMES.add(_name)
        if _name.startswith("HEBREW LETTER "):
            _LETTER_NAMES.add(_name.removeprefix("HEBREW LETTER "))
        for _prefix in ("HEBREW ACCENT ", "HEBREW POINT "):
            if _name.startswith(_prefix):
                _MARK_NAMES.update(_name.removeprefix(_prefix).split(" OR "))
_UNICODE_PATTERN = re.compile(
    r"\b(?:"
    + "|".join(map(re.escape, sorted(_UNICODE_NAMES, key=len, reverse=True)))
    + r")\b"
)
_SOURCE_TITLES = {
    "reading-json.html": ("Holam Male and Holam Haser",),
}
_SHORT_NAME_CITATIONS = {
    "reading-json.html": (
        "with exactly MAHAPAKH, MUNAH or ETNAHTA (GD)",
        "With MUNAH at Ezekiel 14:14 and 14:20",
        "or ETNAHTA at 28:3",
    ),
}


def _alternation(names):
    return "(?:" + "|".join(map(re.escape, sorted(names, key=len, reverse=True))) + ")"


_FORMULA_PATTERN = re.compile(
    r"\b"
    + _alternation(_LETTER_NAMES)
    + r"\s*\+\s*"
    + _alternation(_MARK_NAMES)
    + r"(?:\s*\+\s*"
    + _alternation(_MARK_NAMES)
    + r")*\b"
)
_UNICODE_LABEL_PATTERN = re.compile(
    r"\bUnicode\s+" + _alternation(_LETTER_NAMES | _MARK_NAMES) + r"\b"
)


def findings(html, name):
    """Return spelling failures in authored text; preserve original line numbers."""
    text, lines = html_prose.authored_html_text(html, "gh-pages/near-aleppo/" + name)
    text = _FORMULA_PATTERN.sub(lambda match: " " * len(match[0]), text)
    text = _UNICODE_PATTERN.sub(lambda match: " " * len(match[0]), text)
    text = _UNICODE_LABEL_PATTERN.sub(lambda match: " " * len(match[0]), text)
    for title in _SOURCE_TITLES.get(name, ()):
        text = text.replace(title, " " * len(title))
    for citation in _SHORT_NAME_CITATIONS.get(name, ()):
        pattern = re.compile(r"\s+".join(map(re.escape, citation.split())))
        text = pattern.sub(lambda match: " " * len(match[0]), text)
    found = []
    for match in _PATTERN.finditer(text):
        left = text[match.start() - 1 : match.start()] if match.start() else ""
        right = text[match.end() : match.end() + 1]
        if (
            left in {"_", "/", "\\", ".", "@", "·"}
            or right in {"_", "/", "\\", "·"}
            or (right == "." and text[match.end() + 1 : match.end() + 2].isalnum())
        ):
            continue
        preferred = _VARIANTS[match[0].lower()]
        if match[0].isupper():
            preferred = preferred.upper()
        elif match[0][0].isupper():
            preferred = preferred.capitalize()
        found.append(html_prose.Finding(lines[match.start()], match[0], preferred))
    return found


def test_near_aleppo_documentation_uses_preferred_transliterations():
    root = paths.repo_root() / "gh-pages/near-aleppo"
    assert doc_pages._PAGES, "Near-Aleppo documentation lint has no registered pages"
    offenders = []
    for name in doc_pages._PAGES:
        for finding in findings((root / name).read_text(encoding="utf-8"), name):
            offenders.append(
                f"gh-pages/near-aleppo/{name}:{finding.line}: "
                f"{finding.term} -> {finding.preferred}"
            )
    assert (
        not offenders
    ), "Use preferred transliterations in rendered prose:\n" + "\n".join(offenders)
