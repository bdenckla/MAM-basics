"""The declarative pieces the site's authored pages are written in.

WHY A DATA TYPE RATHER THAN ``mb_html`` CALLS.  The landing page is a link index: almost
every one of its ~34 entries is a title, a URL, and some connective text.  Writing those
as ``mb_html`` elements directly would put the URLs inside rendered markup, where nothing
but a regex over generated HTML could find them again.  Held as data, they can be walked
-- which is what ``py/tests/test_site_index_links.py`` does, checking that every URL
pointing back into this repo's own ``gh-pages/`` names a file that exists.

So the rule is: **authored pages under ``py/author_site/`` describe themselves in these
types, and only the body builder turns them into HTML.**  A URL written straight into an
``anchor_h`` call is invisible to the lint.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Anchor:
    """One link: its visible text and its destination."""

    text: str
    href: str


# A "part" is a string or an Anchor.  A run of parts is the connective-text-and-links
# shape every entry in this index needs: "…, published here from the [MAM-basics]
# repository" is three parts.
Part = str | Anchor


@dataclass(frozen=True)
class Entry:
    """One document in the index, in the four shapes document-index actually uses.

    ``label``    leading text before the link, e.g. "Part 1: ".
    ``anchor``   the document itself.
    ``note``     trailing parts after the link: a parenthetical, or a second anchor.
    ``subs``     plain-text sub-bullets, e.g. the Hakirah volume and co-author lines.
    """

    anchor: Anchor
    label: str = ""
    note: tuple[Part, ...] = ()
    subs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Section:
    """A heading and the entries under it. A section with no heading is a bare list."""

    entries: tuple[Entry, ...]
    heading: str = ""
    intro: tuple[Part, ...] = field(default_factory=tuple)


def anchors_in_parts(parts: tuple[Part, ...]) -> list[Anchor]:
    """Every Anchor in a run of parts, in order."""
    return [part for part in parts if isinstance(part, Anchor)]


def anchors_in_entry(entry: Entry) -> list[Anchor]:
    """Every Anchor an entry carries: its own, then any in its note."""
    return [entry.anchor, *anchors_in_parts(entry.note)]
