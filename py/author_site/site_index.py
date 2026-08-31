"""The site's landing page, ``gh-pages/index.html``.

WHAT THIS PAGE IS.  The manifest of what this repository publishes -- and, from Phase 2 of
``doc/PLAN-unify-the-document-index.md``, Ben's index of the documents he has written,
which lived in its own repo as ``document-index/README.md`` until 2026-08-31.

TWO HALVES, AND THE DIFFERENCE IS THE POINT.  The document entries are AUTHORED: they name
work of Ben's wherever it lives, on this site or on hakirah.org, and no program can derive
them.  The publication manifest is DERIVED, one entry per tracked
``gh-pages/<subtree>/index.html``, per the 2026-08-22 decision recorded in
``doc/PLAN-evacuate-python-programme.md``; only its per-subtree descriptions are authored.
Keeping them apart is what lets that clause hold for the half it was written for without
forcing the other half through a derivation that cannot express it.

NOT ``author.dollar_sub``.  Every other authored page here runs its text through
``mb_author.author``, whose ``_check_no_undollared`` RAISES on an un-``$``-prefixed
romanization key.  This page's link text is full of them -- tsinnorit, maqaf, qadma,
paseq, shewa -- because the titles are other pages' titles, lifted verbatim.  So this
module renders with bare ``mb_html``, exactly as ``main_authored.py``'s own
``_gen_index_html`` does for the misc index, and for the same reason.

WHAT THE FIRST GENERATED PAGE CHANGED, so a later reader does not go looking for a bug.
This file replaced a hand-written ``gh-pages/index.html`` that said so in a comment.  The
generated page says the same things in the same order; what moved is whitespace, because
``mb_html``'s serializer indents nothing and puts ``<title>`` on one line, where the
hand-written page indented and split it.  See the plan's Phase 1.
"""

from __future__ import annotations

from pathlib import Path
import re

from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html

from author_site import published_subtrees
from author_site import site_data
from author_site.entries import Anchor, Entry, Italic, Part, Text

_FNAME = "index.html"
_TITLE = "Documents by Ben Denckla"

_REPO_URL = "https://github.com/bdenckla/MAM-basics"
_README_URL = f"{_REPO_URL}/blob/main/README.md"

_EM_DASH = "\N{EM DASH}"

# The Hebrew block and its presentation forms.  A "run" is a maximal stretch of them
# together with the spaces and Hebrew punctuation inside it.
_HEBREW_RUN_RE = re.compile(r"([\u0590-\u05FF\uFB1D-\uFB4F]+)")

# The link text the hand-written page used for wlc/, kept so that generating the page for
# the first time changed nothing a reader sees.  Deliberately NOT derived from the subtree
# id: "wlc" reads as a directory name, and this list is read by people.
_MANIFEST_LINK_TEXTS = {
    "wlc": "wlc-utils web pages",
}


def gen_html_file(out_dir: Path | None = None) -> str:
    """Write the landing page.  Returns the path written."""
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    out_path = str(top_dir / _FNAME)
    write_ctx = mb_html.WriteCtx(
        _TITLE,
        out_path,
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(build_body(), write_ctx)
    return out_path


def build_body():
    """The page's body contents, top to bottom."""
    return [
        mb_html.heading_level_1(_TITLE),
        mb_html.para(site_data.LEAD_IN),
        *_sections(site_data.BY_ME),
        mb_html.para(site_data.LEAD_IN_NOT_MINE),
        *_sections(site_data.NOT_BY_ME),
        *_headed_list(site_data.MANIFEST_HEADING, _manifest_liconts()),
        _readme_pointer(),
    ]


def _sections(sections):
    """Every authored section, flattened: heading, list, heading, list."""
    return [
        el
        for one in sections
        for el in _headed_list(one.heading, [_entry_licont(e) for e in one.entries])
    ]


def _headed_list(heading: str, liconts):
    """The page's one repeated shape: an ``<h2>`` and the ``<ul>`` under it."""
    return [mb_html.heading_level_2(heading), mb_html.unordered_list(liconts)]


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


def _manifest_liconts():
    """The derived publication manifest: what this repository publishes."""
    subtrees = published_subtrees.published_subtrees(paths.repo_root())
    return [_manifest_licont(one) for one in subtrees]


def _manifest_licont(subtree):
    link_text = _MANIFEST_LINK_TEXTS[subtree.subtree_id]
    return [
        _anchor(Anchor(link_text, subtree.href)),
        f" {_EM_DASH} ",
        *[_part(one) for one in subtree.description],
    ]


def _readme_pointer():
    """The closing pointer the hand-written page ended with, kept word for word."""
    return mb_html.para(
        [
            "For the project itself, see the ",
            _anchor(Anchor("README", _README_URL)),
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

    Two of the ten Misc titles embed a Hebrew word in an English phrase, and one Latin
    title does not.  Declaring the direction of the Hebrew run says what the fragment is,
    which is what CLAUDE.md asks for; declaring it on the whole list item would be a claim
    about the English too.  Doing it here rather than in the data keeps site_data.py free
    of rendering, and makes the rule apply to any Hebrew that arrives later.
    """
    parts = [
        mb_html.span(run, {"dir": "rtl"}) if _is_hebrew(run) else run
        for run in _HEBREW_RUN_RE.split(text)
        if run
    ]
    return parts if len(parts) > 1 else text


def _is_hebrew(run: str) -> bool:
    return bool(_HEBREW_RUN_RE.fullmatch(run))
