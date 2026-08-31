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

from dataclasses import dataclass, field, fields, is_dataclass


@dataclass(frozen=True)
class Italic:
    """Emphasised text: a book title inside a link, mostly."""

    text: str


# What an anchor's visible text may be: a plain string, or a run mixing strings and
# Italic, for the two entries naming a book -- "Excerpts from [Introduction to the
# Tiberian Masorah] by Israel Yeivin" and "Notes on Torah [aliyot]".
Text = str | tuple[str | Italic, ...]


@dataclass(frozen=True)
class Anchor:
    """One link: its visible text and its destination."""

    text: Text
    href: str


# A "part" is a string, an Italic or an Anchor.  A run of parts is the
# connective-text-and-links shape every entry in this index needs: "…, published here
# from the [MAM-basics] repository" is three parts.
Part = str | Italic | Anchor


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


def anchors_in(value) -> list[Anchor]:
    """Every Anchor reachable from a value, in order, whatever shape holds it.

    Field-driven rather than hand-written per type, so a link added to a NEW field of any
    of these dataclasses is walked without this function being edited.  That matters
    because the one caller is ``py/tests/test_site_index_links.py``, and a link the walk
    misses is a link the lint silently does not check.
    """
    if isinstance(value, Anchor):
        return [*anchors_in(value.text), value]
    if isinstance(value, (str, Italic)) or value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [anchor for one in value for anchor in anchors_in(one)]
    if is_dataclass(value):
        return [
            anchor
            for one in fields(value)
            for anchor in anchors_in(getattr(value, one.name))
        ]
    raise TypeError(f"anchors_in does not know how to walk {type(value).__name__}")
