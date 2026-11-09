"""Show the marks that the FOIs reading by forms show gray.

foi_wikitext_helpers.with_attached_marks writes a stand-in for each mark that these
FOIs show gray.  The one such mark is MAM's gray maqaf, the template מ:מקף אפור,
which the reading takes as a maqaf joining the atoms on either side of it into one
form; GRAY_MAQAF stands for it.  A stand-in is a Private Use code point, which
with_attached_marks raises on meeting in MAM's text, and none leaves the FOIs: a FOI
finds its features in a form's text, in which each stand-in is the mark it stands
for, and records the form as a target in which each such mark is a span that the
shared stylesheet shows gray.  The FOI pages then give a row that shows such a mark a
cell naming it, GM, whose title explains it on hover, and give its JSON row a flag of
the same name.  Ben Denckla asked for this on 2026-11-09, as the docstring of
foi_wikitext_helpers.with_attached_marks records.
"""

from typing import NamedTuple

from mb_cmn import hebrew_punctuation as hpu
from mb_misc import mb_html

GRAY_MAQAF = "\U0000e001"  # A Private Use code point
STAND_INS = GRAY_MAQAF


class _Kind(NamedTuple):
    mark: str
    span_class: str
    label: str
    explanation: str


# In the order of the columns that name them.
_KINDS = {
    GRAY_MAQAF: _Kind(
        hpu.MAQ,
        "mam-implicit-maqaf",
        "GM",
        "Gray maqaf: a maqaf that MAM itself shows in gray. This page reads it as a"
        " maqaf, joining the atoms on either side of it into one form.",
    ),
}
_KIND_OF_SPAN_CLASS = {kind.span_class: kind for kind in _KINDS.values()}
_TEXT_TABLE = str.maketrans({stand_in: kind.mark for stand_in, kind in _KINDS.items()})


def text(form):
    """Return form with each stand-in replaced by the mark it stands for."""
    return form.translate(_TEXT_TABLE)


def target(form):
    """Return what a FOI row shows for form.

    That is form itself, unless it holds a stand-in.  Then it is an htseq in which the
    mark that each stand-in stands for is a span of that mark's class.
    """
    if not any(stand_in in form for stand_in in STAND_INS):
        return form
    htseq = []
    run = []
    for char in form:
        if (kind := _KINDS.get(char)) is None:
            run.append(char)
            continue
        if run:
            htseq.append("".join(run))
            run = []
        htseq.append(mb_html.span(kind.mark, {"class": kind.span_class}))
    if run:
        htseq.append("".join(run))
    return tuple(htseq)


def labels(html_contents):
    """Return the labels of the gray marks that a row's target shows, in order."""
    found = set()
    _collect_labels(html_contents, found)
    return tuple(kind.label for kind in _KINDS.values() if kind.label in found)


def labels_of_table(rows_labels):
    """Return the labels of the gray marks that any of a table's rows show."""
    found = set().union(*rows_labels)
    return tuple(kind.label for kind in _KINDS.values() if kind.label in found)


def json_flags(html_contents):
    """Return the flags that a row's JSON gets for the gray marks its target shows."""
    return {label.lower(): True for label in labels(html_contents)}


def cells(row_labels, table_labels):
    """Return a row's cells in its table's columns of gray marks."""
    return tuple(
        mb_html.table_datum(_ABBRS[table_label] if table_label in row_labels else None)
        for table_label in table_labels
    )


def _collect_labels(contents, found):
    if isinstance(contents, str):
        return
    for item in contents:
        if not mb_html.is_htel(item):
            continue
        kind = _KIND_OF_SPAN_CLASS.get(item.get("attr", {}).get("class"))
        if kind is not None:
            found.add(kind.label)
        _collect_labels(item.get("contents", ()), found)


_ABBRS = {
    kind.label: mb_html.abbr(kind.label, {"title": kind.explanation})
    for kind in _KINDS.values()
}
