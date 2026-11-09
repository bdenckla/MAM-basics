"""Show the marks that FOI pages show gray.

A FOI page shows two kinds of mark gray, each in a span of a class that the shared
stylesheet shows gray.  It gives a row that shows one a cell naming its kind, whose
title explains it on hover, and gives the row's JSON a flag of the same name.  Ben
Denckla asked for both on 2026-11-09.

GM, a gray maqaf, is MAM's own gray maqaf, the template מ:מקף אפור.  The FOIs that read
MAM's text by forms take it as a maqaf joining the atoms on either side of it into one
form, and foi_wikitext_helpers.with_attached_marks writes it as the stand-in
GRAY_MAQAF, a Private Use code point.  That function raises on meeting a stand-in in
MAM's text, and none leaves the FOIs: a FOI finds its features in a form's text, in
which each stand-in is the mark it stands for, and records the form as a target in
which each such mark is a span.  A gray maqaf is part of the text, so a row's JSON
keeps it, as a maqaf.

GSP, a gray sof pasuq, is a sof pasuq that a FOI listing a template's argument adds
after that argument, for context, where the sof pasuq follows the template.  Ben asked
for it "for cases where, narrowly speaking, the phenomenon in question does not
include sof pasuq (e.g. the argument of a template being "studied" (listed))", and
foi_wikitext_helpers.templates_before_sof_pasuq finds those templates.  A gray sof
pasuq is not part of the argument, so a row's JSON leaves it out of the argument's
text.  The same day he approved, "proceed as you recommend", a GSP in every FOI that
lists a template's argument, wherever a sof pasuq follows that template and is no
part of the FOI's feature.  So foi-kq-simple, foi-qamats-variants, foi-slh-word and
foi-rare-tmpls add one.  foi-kq-complex already showed such a sof pasuq, black,
where one ends its run of two ketiv/qere templates, and now shows it gray.  It keeps
black the sof pasuq of a k1q1-qk-sp, whose feature is a qere-first ketiv/qere
template before a sof pasuq.
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
    # Whether a row's JSON keeps the mark in the text that shows it.
    in_json_text: bool


_GSP = _Kind(
    hpu.SOPA,
    "foi-gray-sof-pasuq",
    "GSP",
    "Gray sof pasuq: this page adds it, in gray, for context. It follows the template"
    " whose argument this row lists, rather than belonging to that argument.",
    False,
)
_GM = _Kind(
    hpu.MAQ,
    "mam-implicit-maqaf",
    "GM",
    "Gray maqaf: a maqaf that MAM itself shows in gray. This page reads it as a"
    " maqaf, joining the atoms on either side of it into one form.",
    True,
)
_KINDS = _GSP, _GM  # In the order of the columns that name them
_KIND_OF_STAND_IN = {GRAY_MAQAF: _GM}
_KIND_OF_SPAN_CLASS = {kind.span_class: kind for kind in _KINDS}
_TEXT_TABLE = str.maketrans(
    {stand_in: kind.mark for stand_in, kind in _KIND_OF_STAND_IN.items()}
)


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
        if (kind := _KIND_OF_STAND_IN.get(char)) is None:
            run.append(char)
            continue
        if run:
            htseq.append("".join(run))
            run = []
        htseq.append(_span(kind))
    if run:
        htseq.append("".join(run))
    return tuple(htseq)


def gray_sof_pasuq(lang=None):
    """Return a gray sof pasuq, a span to follow an argument that a FOI lists.

    Give lang where the cell that shows the span has no lang of its own, so that the
    span has the font of the pointed Hebrew it follows.
    """
    return _span(_GSP, lang)


def is_gray_mark(html_el):
    """Return whether html_el is a gray mark."""
    return _kind_of(html_el) is not None


def is_left_out_of_json_text(html_el):
    """Return whether html_el is a gray mark that a row's JSON text leaves out."""
    kind = _kind_of(html_el)
    return kind is not None and not kind.in_json_text


def labels(*contents):
    """Return the labels of the gray marks that any of contents show, in order."""
    found = set()
    for item in contents:
        _collect_labels(item, found)
    return tuple(kind.label for kind in _KINDS if kind.label in found)


def labels_of_table(rows_labels):
    """Return the labels of the gray marks that any of a table's rows show."""
    found = set().union(*rows_labels)
    return tuple(kind.label for kind in _KINDS if kind.label in found)


def json_flags(*contents):
    """Return the flags that a row's JSON gets for the gray marks it shows."""
    return {label.lower(): True for label in labels(*contents)}


def cells(row_labels, table_labels):
    """Return a row's cells in its table's columns of gray marks."""
    return tuple(
        mb_html.table_datum(_ABBRS[table_label] if table_label in row_labels else None)
        for table_label in table_labels
    )


def _span(kind, lang=None):
    attr = {"class": kind.span_class}
    if lang is not None:
        attr["lang"] = lang
    return mb_html.span(kind.mark, attr)


def _kind_of(html_el):
    if not mb_html.is_htel(html_el):
        return None
    return _KIND_OF_SPAN_CLASS.get(html_el.get("attr", {}).get("class"))


def _collect_labels(contents, found):
    if mb_html.is_htel(contents):
        if (kind := _kind_of(contents)) is not None:
            found.add(kind.label)
        _collect_labels(contents.get("contents"), found)
    elif isinstance(contents, (list, tuple)):
        for item in contents:
            _collect_labels(item, found)


_ABBRS = {
    kind.label: mb_html.abbr(kind.label, {"title": kind.explanation}) for kind in _KINDS
}
