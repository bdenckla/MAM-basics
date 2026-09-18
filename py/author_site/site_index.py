"""Render the topical landing page at ``gh-pages/index.html``.

``build_body`` renders the single ordered ``site_data.SECTIONS`` collection.  Most
sections are an ``<h2>`` followed by one flat list.  A linked heading is its own sole
destination and therefore has no empty list, while the Masoretes series is the page's one
deliberate nested list.

The page remains fully authored rather than derived from the deployment tree.  The
mechanical lint in ``py/tests/test_site_index_links.py`` checks every typed internal link
and the deploy-root reachability rule.  The frozen ``gh-pages/wlc/index.html`` remains an
intentional non-entry: old wlc-utils links redirect to it, while the topical index names
the useful WLC destinations directly.

This renderer deliberately uses bare ``mb_html`` rather than ``author.dollar_sub``.
Several copied document titles contain ordinary romanization words such as maqaf, qadma,
and paseq; treating those titles as author-source markup would reject them.
"""

from __future__ import annotations

from pathlib import Path
import re

from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html

from author_site import site_data
from author_site.entries import Anchor, Entry, EntryGroup, Italic, Part, Text

_FNAME = "index.html"
_TITLE = "The Miqra according to Denckla."

_REPO_URL = "https://github.com/bdenckla/MAM-basics"
_README_URL = f"{_REPO_URL}/blob/main/README.md"

# The Hebrew block and its presentation forms.  A "run" is a maximal stretch of them
# together with the spaces and Hebrew punctuation inside it.
_HEBREW_RUN_RE = re.compile(r"([\u0590-\u05FF\uFB1D-\uFB4F]+)")


def gen_html_file(out_dir: Path | None = None) -> str:
    """Write the landing page.  Returns the path written."""
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    out_path = str(top_dir / _FNAME)
    write_ctx = mb_html.WriteCtx(
        _TITLE,
        out_path,
        css_hrefs=(site_data.CSS_HREF,),
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(build_body(), write_ctx)
    return out_path


def build_body():
    """The page's body contents, top to bottom."""
    return [
        mb_html.heading_level_1(_TITLE),
        mb_html.para(site_data.INTRO),
        *_sections(site_data.SECTIONS),
        _readme_pointer(),
    ]


def _sections(sections):
    """Every topical section, flattened into its heading and optional list."""
    return [element for section in sections for element in _section(section)]


def _section(section):
    """Render one section, omitting the list for a linked-heading destination."""
    heading = (
        _anchor(section.heading)
        if isinstance(section.heading, Anchor)
        else section.heading
    )
    rendered = [mb_html.heading_level_2(heading)]
    if section.entries:
        rendered.append(
            mb_html.unordered_list([_list_item(item) for item in section.entries])
        )
    return rendered


def _list_item(item: Entry | EntryGroup):
    """Render an ordinary entry or the page's one named group of entries."""
    if isinstance(item, EntryGroup):
        return [
            item.label,
            mb_html.unordered_list([_entry_licont(entry) for entry in item.entries]),
        ]
    return _entry_licont(item)


def _entry_licont(entry: Entry):
    """One document: an optional leading label, the link, a note, then any sub-bullets."""
    head = [
        *([entry.label] if entry.label else []),
        _anchor(entry.anchor),
        *[_part(one) for one in entry.note],
    ]
    if not entry.subs:
        return head
    subs = mb_html.unordered_list([_rtl_split(one) for one in entry.subs])
    return [*head, subs]


def _readme_pointer():
    """The closing pointer to the MAM-basics repository documentation."""
    return mb_html.para(
        [
            "For the MAM-basics source code and project documentation, see the ",
            _anchor(Anchor("repository README", _README_URL)),
            ".",
        ]
    )


def _anchor(anchor: Anchor):
    return mb_html.anchor_h(_text(anchor.text), anchor.href)


def _text(text: Text):
    """An anchor's visible text: a plain string, or a run mixing strings and Italic."""
    if isinstance(text, str):
        return _rtl_split(text)
    return [_part(one) for one in text]


def _part(part: Part):
    if isinstance(part, Anchor):
        return _anchor(part)
    if isinstance(part, Italic):
        return mb_html.emphasis(_rtl_split(part.text))
    return _rtl_split(part)


def _rtl_split(text: str):
    """Wrap each Hebrew run of ``text`` in a ``dir="rtl"`` span, leaving the rest alone.

    Declaring the direction on a Hebrew fragment says what that fragment is, while
    declaring it on an entire English list item would misdescribe the surrounding text.
    Keeping the split here leaves ``site_data.py`` free of rendering details and applies
    the rule to any Hebrew that arrives later.
    """
    parts = [
        mb_html.span(run, {"dir": "rtl"}) if _is_hebrew(run) else run
        for run in _HEBREW_RUN_RE.split(text)
        if run
    ]
    return parts if len(parts) > 1 else text


def _is_hebrew(run: str) -> bool:
    return bool(_HEBREW_RUN_RE.fullmatch(run))
