"""The English introduction's section map: each English section and the Hebrew it translates.

WHAT THE MAP IS.  ``in/mam-ws-intro-en-section-map.json`` takes each section of the English
mirror, ``in/mam-ws-intro-en/``, in page order, and names the sections of the Hebrew mirror,
``in/mam-ws-intro/``, that it translates, each by its heading, with its coverage of them:
full, partial or none.  Phase 6 of ``doc/PLAN-english-intro.md`` plans it, and
``in/mam-ws-intro-en/README.md``, "The section map", says what each field means and how the
map is kept.  ``py/tests/test_intro_en_section_map.py`` is its lint, and ``drift`` below is
the drift list that ``py/main_download.py fr-ws-intro`` prints.

WHAT A SECTION IS.  A heading's section is its own text: the heading's line and every line
after it up to the next heading of any level.  So a subsection is a section of its own, and a
change in it is not a change in its parent.  A page's lead, the lines before its first
heading, is a section too, whose heading is ``None``.

HOW A HEADING IS NAMED.  By its text as a reader sees it, which ``_plain_text`` reads with a
closed dispatch.  It recognizes runs of two, three or five apostrophes, which format text and
are dropped; an internal link, ``[[target|label]]`` or ``[[target]]``, which shows its label
or its target; and an external link with a label, ``[url label]``, which shows its label.  It
recognizes no template, tag or HTML entity in a heading, and raises on any of them, and on any
other bracket, brace or pipe.  Hebrew in a heading's name is in MAM's mark order: the name is
``give_std_mark_order`` of the text that the mirror's heading shows, since the mirrors are
captures in Unicode's mark order and the map is authored.

WHAT THE PAGE READER REFUSES.  ``sections`` raises on a page holding anything that could hide
a heading from it or show it a heading that is not one: a comment, a ``pre``,
``syntaxhighlight``, ``source``, ``math`` or ``includeonly`` element, a ``nowiki`` element that
does not close on its own line, a line beginning with ``=`` inside a ``ref``, a template, a
table or a ``poem``, and a line beginning with ``=`` that is not a balanced heading of levels 1
to 6.  On 2026-11-22 the fourteen pages that the map reads, seven in each mirror, held none of
these.

THE DRIFT LIST.  ``drift`` compares the Hebrew mirror's text before a refresh with its text
after it, and lists each mapped English section whose Hebrew counterpart changed: its own
text differs, or its heading is gone or now occurs more than once.  Those are the candidates
for the translation to follow.  It raises if a counterpart's heading is not on its page exactly
once before the refresh, since the lint holds the map to the mirror as committed.
"""

import dataclasses
import difflib
import json
import re

from mb_cmn import paths
from mb_cmn import uni_denorm

COVERAGES = ("full", "partial", "none")


class SectionMapError(Exception):
    """The map, or a page that it reads, is not what this module handles."""


@dataclasses.dataclass(frozen=True)
class Counterpart:
    """A section of the Hebrew mirror: its page's slug and its heading, None for the lead."""

    page: str
    heading: str | None


@dataclasses.dataclass(frozen=True)
class Entry:
    """One section of the English mirror, and what it translates."""

    english: str | None
    hebrew: tuple[Counterpart, ...]
    coverage: str
    evaluation_slices: tuple[str, ...]
    note: str | None


@dataclasses.dataclass(frozen=True)
class SectionMap:
    """The whole map: the evaluation it cites, and each English page's entries in order."""

    evaluation: str
    pages: dict[str, tuple[Entry, ...]]


@dataclasses.dataclass(frozen=True)
class Section:
    """A section's own text, lines[start:end] of its page; level 0 for the lead."""

    heading: str | None
    level: int
    start: int
    end: int


@dataclasses.dataclass(frozen=True)
class Drift:
    """A mapped English section whose Hebrew counterpart changed in a refresh."""

    english_page: str
    english_heading: str | None
    coverage: str
    counterpart: Counterpart
    kind: str
    lines_removed: int
    lines_added: int


def map_path():
    """The tracked section map."""
    return paths.in_dir() / "mam-ws-intro-en-section-map.json"


def load():
    """The section map, its English pages and their entries in page order.

    It fails unless the file has exactly the shape that the README describes, so that a
    mistyped key or coverage fails rather than being ignored.
    """
    with open(map_path(), "r", encoding="utf-8") as map_fp:
        data = json.load(map_fp)
    _expect_keys(data, {"about", "evaluation", "pages"}, set(), "the map")
    for key in ("about", "evaluation"):
        if not _is_trimmed_text(data[key]):
            raise SectionMapError(f"the map's {key}: {data[key]!r}")
    pages = data["pages"]
    if not isinstance(pages, dict) or not pages:
        raise SectionMapError(f"the map's pages: {pages!r}")
    return SectionMap(
        data["evaluation"],
        {slug: _entries(slug, entries) for slug, entries in pages.items()},
    )


def _entries(slug, entries):
    if not isinstance(entries, list) or not entries:
        raise SectionMapError(f"the map's entries for {slug}: {entries!r}")
    return tuple(_entry(slug, entry) for entry in entries)


def _entry(slug, entry):
    where = f"an entry of {slug}"
    _expect_keys(
        entry, {"english", "hebrew", "coverage", "evaluation_slices"}, {"note"}, where
    )
    english = entry["english"]
    if english is not None and not _is_trimmed_text(english):
        raise SectionMapError(f"{where}: english {english!r}")
    if not isinstance(entry["hebrew"], list):
        raise SectionMapError(f"{where}: hebrew {entry['hebrew']!r}")
    hebrew = tuple(_counterpart(where, counterpart) for counterpart in entry["hebrew"])
    if len(set(hebrew)) != len(hebrew):
        raise SectionMapError(f"{where}: a counterpart named twice, {hebrew!r}")
    coverage = entry["coverage"]
    if coverage not in COVERAGES:
        raise SectionMapError(f"{where}: coverage {coverage!r}")
    if coverage != "none" and not hebrew:
        raise SectionMapError(f"{where}: coverage {coverage!r} of no counterpart")
    slices = entry["evaluation_slices"]
    if not isinstance(slices, list) or not slices:
        raise SectionMapError(f"{where}: evaluation_slices {slices!r}")
    for slice_name in slices:
        if not _is_trimmed_text(slice_name):
            raise SectionMapError(f"{where}: evaluation slice {slice_name!r}")
    note = entry.get("note")
    if note is not None and not _is_trimmed_text(note):
        raise SectionMapError(f"{where}: note {note!r}")
    return Entry(english, hebrew, coverage, tuple(slices), note)


def _counterpart(where, counterpart):
    _expect_keys(counterpart, {"page", "heading"}, set(), f"{where}, a counterpart")
    page, heading = counterpart["page"], counterpart["heading"]
    if not _is_trimmed_text(page):
        raise SectionMapError(f"{where}: counterpart page {page!r}")
    if heading is not None and not _is_trimmed_text(heading):
        raise SectionMapError(f"{where}: counterpart heading {heading!r}")
    return Counterpart(page, heading)


def _expect_keys(obj, required, optional, where):
    if not isinstance(obj, dict):
        raise SectionMapError(f"{where} is not an object: {obj!r}")
    keys = set(obj)
    if not required <= keys or not keys <= required | optional:
        raise SectionMapError(
            f"{where} has keys {sorted(keys)}; it needs {sorted(required)}"
            f" and may have {sorted(optional)}"
        )


def _is_trimmed_text(value):
    return isinstance(value, str) and value != "" and value == value.strip()


def sections(wikitext):
    """Every section of a page, its lead first, then one for each heading in page order."""
    lines = wikitext.split("\n")
    _refuse_hiding_constructs(wikitext)
    headings = []
    depths = _Depths()
    for index, line in enumerate(lines):
        if line.startswith("="):
            depths.refuse_heading_inside(index, line)
            level, text = _heading_level_and_text(line)
            headings.append((index, level, text))
        depths.update(index, line)
    depths.refuse_unclosed()
    starts = [index for index, _level, _text in headings] + [len(lines)]
    result = [Section(None, 0, 0, starts[0])]
    for (index, level, text), end in zip(headings, starts[1:]):
        result.append(Section(text, level, index, end))
    return tuple(result)


def matching_sections(wikitext, heading):
    """The sections of a page whose heading is the given name; for None, the lead."""
    return [section for section in sections(wikitext) if section.heading == heading]


def section_lines(wikitext, section):
    """A section's own text, as a list of lines."""
    return wikitext.split("\n")[section.start : section.end]


def drift(section_map, before, after):
    """Each mapped English section whose Hebrew counterpart changed from before to after.

    before and after map a Hebrew page's slug to its whole wikitext.  A counterpart whose
    heading is not on its page exactly once before is a map out of step with the mirror,
    and raises.  After, a heading that is gone or repeated is a drift of its own kind.
    """
    drifts = []
    for english_page, entries in section_map.pages.items():
        for entry in entries:
            for counterpart in entry.hebrew:
                found = _drift_of(counterpart, before, after)
                if found is not None:
                    kind, removed, added = found
                    drifts.append(
                        Drift(
                            english_page,
                            entry.english,
                            entry.coverage,
                            counterpart,
                            kind,
                            removed,
                            added,
                        )
                    )
    return drifts


def _drift_of(counterpart, before, after):
    old_text, new_text = before[counterpart.page], after[counterpart.page]
    if old_text is None:
        raise SectionMapError(
            f"the section map names {counterpart}, whose page had no text before this"
            " refresh"
        )
    old_sections = matching_sections(old_text, counterpart.heading)
    if len(old_sections) != 1:
        raise SectionMapError(
            "the section map is out of step with the Hebrew mirror as it stood before"
            f" this refresh: {counterpart} is on its page {len(old_sections)} times"
        )
    new_sections = matching_sections(new_text, counterpart.heading)
    old_lines = section_lines(old_text, old_sections[0])
    if not new_sections:
        return "gone", len(old_lines), 0
    if len(new_sections) > 1:
        return "repeated", 0, 0
    new_lines = section_lines(new_text, new_sections[0])
    if new_lines == old_lines:
        return None
    removed = added = 0
    for line in difflib.ndiff(old_lines, new_lines):
        removed += line.startswith("- ")
        added += line.startswith("+ ")
    return "changed", removed, added


def drift_report(drifts):
    """The drift list as lines of text, for a refresh to print."""
    if not drifts:
        return ["Drift list: no mapped Hebrew section changed in this refresh."]
    report = [
        "Drift list: each mapped English section whose Hebrew counterpart changed in"
        " this refresh, a candidate for the translation to follow:"
    ]
    for item in drifts:
        english = _shown_heading(item.english_heading)
        hebrew = _shown_heading(item.counterpart.heading)
        if item.kind == "changed":
            out = f"{item.lines_removed} line{'' if item.lines_removed == 1 else 's'}"
            what = f"changed, {out} out and {item.lines_added} in"
        elif item.kind == "gone":
            what = "its heading is gone; the section map needs updating"
        elif item.kind == "repeated":
            what = (
                "its heading now occurs more than once; the section map needs updating"
            )
        else:
            raise SectionMapError(f"a drift of unknown kind: {item!r}")
        report.append(
            f"- English {item.english_page} {english} (coverage {item.coverage})"
            f" <- Hebrew {item.counterpart.page} {hebrew}: {what}"
        )
    return report


def _shown_heading(heading):
    return "(lead)" if heading is None else f'"{heading}"'


def _heading_level_and_text(line):
    match = _HEADING_LINE.fullmatch(line)
    if (
        match is None
        or len(match["open"]) != len(match["close"])
        or len(match["open"]) > 6
    ):
        raise SectionMapError(
            f"a line that begins with = and is not a balanced heading: {line!r}"
        )
    text = _plain_text(match["content"], links_allowed=True).strip()
    if not text:
        raise SectionMapError(f"a heading with no text: {line!r}")
    return len(match["open"]), uni_denorm.give_std_mark_order(text)


def _plain_text(markup, links_allowed):
    """The text that a heading's markup shows; it raises on what it does not recognize."""
    parts = []
    position = 0
    for match in _TOKEN.finditer(markup):
        if match.start() != position:
            raise SectionMapError(f"unread heading markup at {position}: {markup!r}")
        position = match.end()
        kind = match.lastgroup
        if kind == "text":
            parts.append(match["text"])
        elif kind == "quotes":
            if len(match["quotes"]) not in (2, 3, 5):
                raise SectionMapError(f"an apostrophe run in a heading: {markup!r}")
        elif kind == "internal" and links_allowed:
            label = match["label"]
            if label is None:
                parts.append(match["target"].lstrip(":"))
            else:
                parts.append(_plain_text(label, links_allowed=False))
        elif kind == "external" and links_allowed:
            parts.append(_plain_text(match["xlabel"], links_allowed=False))
        else:
            raise SectionMapError(
                f"a heading holds {match.group()!r}, which this reader does not"
                f" recognize: {markup!r}"
            )
    if position != len(markup):
        raise SectionMapError(f"unread heading markup at {position}: {markup!r}")
    return "".join(parts)


def _refuse_hiding_constructs(wikitext):
    match = _HIDING_CONSTRUCT.search(wikitext)
    if match is not None:
        line_number = wikitext.count("\n", 0, match.start()) + 1
        raise SectionMapError(
            f"line {line_number} holds {match.group()!r}, which could hide a heading"
            " from this reader"
        )


class _Depths:
    """How many refs, templates, tables and poems are open at the start of each line."""

    def __init__(self):
        self.ref = self.template = self.table = self.poem = 0

    def refuse_heading_inside(self, index, line):
        if self.ref or self.template or self.table or self.poem:
            raise SectionMapError(
                f"line {index + 1} begins with = inside a ref, template, table or poem:"
                f" {line!r}"
            )

    def update(self, index, line):
        visible = _NOWIKI_ELEMENT.sub("", line)
        if _NOWIKI_TAG.search(visible):
            raise SectionMapError(
                f"line {index + 1} has a nowiki element that does not close on it"
            )
        self.ref += len(_REF_OPEN.findall(visible)) - len(_REF_CLOSE.findall(visible))
        self.poem += len(_POEM_OPEN.findall(visible)) - len(
            _POEM_CLOSE.findall(visible)
        )
        self.template += visible.count("{{") - visible.count("}}")
        self.table += bool(_TABLE_OPEN.match(visible)) - bool(
            _TABLE_CLOSE.match(visible)
        )
        if min(self.ref, self.template, self.table, self.poem) < 0:
            raise SectionMapError(f"line {index + 1} closes what was not open")

    def refuse_unclosed(self):
        if self.ref or self.template or self.table or self.poem:
            raise SectionMapError(
                "the page ends with a ref, template, table or poem open"
            )


_HEADING_LINE = re.compile(r"(?P<open>=+)(?P<content>.*?)(?P<close>=+)[ \t]*")
_TOKEN = re.compile(
    r"(?P<internal>\[\[(?P<target>[^\[\]{}<>|]+)(?:\|(?P<label>[^\[\]{}<>|]+))?\]\])"
    r"|(?P<external>\[(?P<url>(?:https?:)?//[^\s\[\]{}<>]+)[ \t]+"
    r"(?P<xlabel>[^\[\]{}<>]+?)\])"
    r"|(?P<quotes>'{2,})"
    r"|(?P<refused>[\[\]{}<>&|]|~~~|__)"
    r"|(?P<text>[^\[\]{}<>&|'~_]+|['~_])"
)
_HIDING_CONSTRUCT = re.compile(
    r"<!--|<(?:pre|syntaxhighlight|source|math|includeonly)\b", re.IGNORECASE
)
_NOWIKI_ELEMENT = re.compile(r"<nowiki\s*>.*?</nowiki\s*>|<nowiki\s*/>", re.IGNORECASE)
_NOWIKI_TAG = re.compile(r"</?nowiki\b", re.IGNORECASE)
_REF_OPEN = re.compile(r"<ref\b(?:[^>/]|/(?!>))*>", re.IGNORECASE)
_REF_CLOSE = re.compile(r"</ref\s*>", re.IGNORECASE)
_POEM_OPEN = re.compile(r"<poem\b[^>]*>", re.IGNORECASE)
_POEM_CLOSE = re.compile(r"</poem\s*>", re.IGNORECASE)
_TABLE_OPEN = re.compile(r"[ \t:]*\{\|")
# Not |}} at a line's start, which closes a template whose last parameter is empty.
_TABLE_CLOSE = re.compile(r"[ \t]*\|\}(?!\})")
