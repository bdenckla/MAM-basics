"""Shared page-assembly core for the prose (goerwitz.html) and poetic (poetic.html)
ungrammatical-verse reports.

Both reports are a single flat, client-side-filterable list of ungrammatical verses under a
width-limited wrapper, with a per-option-count filter-control block and a trailing
filter ``<script>``. They differ only in their *acquisition* (prose reads classified
rows from disk; poetic re-scans live) and in each verse section's content/shape -- which
stay in the two front-ends (``rtmsr_overview``, ``poetic_oddballs``). This module owns
the parts they share: the filter-control builder (driven by a declarative facet list),
the per-verse ``<section>`` wrapper, and the page-body shell. See issue wlc-utils#22.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from py_html import wlc_utils_html

# Both reports wrap their body in this width-limited div, tag each verse <section> with
# this class (the filter scripts select on it), and wrap their fieldsets in this filter
# div.
_WIDTH_CLASS = "goerwitz-tms-width-limited"
_VERSE_SECTION_CLASS = "goerwitz-verse"
_FILTER_WRAPPER_CLASS = "goerwitz-filter"
# The class every live per-option count span carries, shared with both filter scripts so
# they can find a control's count span and rewrite it to the visible-verse count. A zero
# count renders empty (no "(0)").
_COUNT_CLASS = "gf-opt-count"


@dataclass(frozen=True)
class CheckboxFacet:
    """A group of independent checkbox filters (e.g. "Source", "Book")."""

    legend: str
    css_class: str  # the shared class on every checkbox in the group, e.g. "gf-source"
    options: tuple[tuple[str, str, int], ...]  # (value, label, no-JS fallback count)


@dataclass(frozen=True)
class TristateFacet:
    """A has / doesn't-have / don't-care radio group, ANDed with the other facets.

    Defaults to "don't care" so the page opens unfiltered on this axis. The has /
    doesn't-have counts are the no-JS fallback; the filter script recomputes them live.
    """

    legend: str
    group_name: str  # the radio group's shared name/class, e.g. "gf-uchange"
    has_count: int
    total: int


Facet = CheckboxFacet | TristateFacet


@dataclass(frozen=True)
class CorpusDescriptor:
    """Everything build_page_body needs that differs by corpus.

    The heading/intro blocks, verse sections, and tail blocks are pre-built by the
    front-end (each owns its corpus-specific content + order); this descriptor carries
    them plus the declarative facet list the shared filter-control builder consumes."""

    heading_blocks: tuple[object, ...]  # h1 + intro (+ citation), already built
    facets: tuple[Facet, ...]
    count_para_class: (
        str  # the filter's running-total para class ("gf-count"/"pf-count")
    )
    verse_sections: tuple[object, ...]  # already built via render_verse_section
    tail_blocks: tuple[object, ...]  # prose bracket-notes glossary; () for poetic
    filter_script_name: str  # "goerwitz-filter.js" | "poetic-filter.js"


def build_page_body(desc: CorpusDescriptor) -> tuple[object, ...]:
    """The full page body: the width-limited wrapper (heading, filter controls, verse
    sections, tail) plus the trailing filter ``<script>``."""
    sections: list[object] = [
        *desc.heading_blocks,
        build_filter_controls(desc.facets, desc.count_para_class),
        *desc.verse_sections,
        *desc.tail_blocks,
    ]
    wrapper = wlc_utils_html.div(tuple(sections), {"class": _WIDTH_CLASS})
    script = wlc_utils_html.htel_mk("script", {"src": desc.filter_script_name})
    return (wrapper, script)


def render_verse_section(
    items: Sequence[object], *, is_first: bool, data_attrs: dict[str, str]
) -> object:
    """Wrap one verse's content in a filterable ``<section>``.

    The separating rule lives inside the section (omitted on the first one) so it hides
    with its verse when the filter removes it. ``data_attrs`` are the corpus's filter
    dimensions (e.g. data-category/-source or data-kind/-book/-agree)."""
    body: list[object] = []
    if not is_first:
        body.append(wlc_utils_html.horizontal_rule())
    body.extend(items)
    return wlc_utils_html.htel_mk(
        "section", {"class": _VERSE_SECTION_CLASS, **data_attrs}, tuple(body)
    )


def build_filter_controls(facets: Sequence[Facet], count_para_class: str) -> object:
    """The filter-control block: one fieldset per facet, then a running-total para."""
    fieldsets: list[object] = []
    for facet in facets:
        if isinstance(facet, CheckboxFacet):
            labels = tuple(
                _checkbox(facet.css_class, value, label, count)
                for value, label, count in facet.options
            )
            fieldsets.append(_fieldset(facet.legend, labels))
        else:
            fieldsets.append(
                _tristate_fieldset(
                    facet.legend, facet.group_name, facet.has_count, facet.total
                )
            )
    count_para = wlc_utils_html.para("", {"class": count_para_class})
    return wlc_utils_html.div(
        (*fieldsets, count_para), {"class": _FILTER_WRAPPER_CLASS}
    )


def _fieldset(legend_text: str, labels: tuple[object, ...]) -> object:
    legend = wlc_utils_html.htel_mk("legend", None, legend_text)
    return wlc_utils_html.htel_mk("fieldset", None, (legend, *labels))


def _tristate_fieldset(
    legend_text: str, group_name: str, has_count: int, total: int
) -> object:
    return _fieldset(
        legend_text,
        (
            _radio_with_count(group_name, "yes", "has", has_count),
            _radio_with_count(group_name, "no", "doesn't have", total - has_count),
            _radio(group_name, "any", "don't care", checked=True),
        ),
    )


def _checkbox(css_class: str, value: str, label_text: str, count: int) -> object:
    input_el = wlc_utils_html.htel_mk(
        "input",
        {
            "type": "checkbox",
            "class": css_class,
            "value": value,
            "checked": "checked",
        },
    )
    return wlc_utils_html.htel_mk(
        "label", None, (input_el, f" {label_text}", _count_span(count))
    )


def _radio(group_name: str, value: str, label_text: str, *, checked: bool) -> object:
    input_el = _radio_input(group_name, value, checked=checked)
    return wlc_utils_html.htel_mk("label", None, (input_el, f" {label_text}"))


def _radio_with_count(
    group_name: str, value: str, prefix_text: str, count: int
) -> object:
    """A radio whose label ends in a "(N)" count the filter script keeps live."""
    input_el = _radio_input(group_name, value, checked=False)
    return wlc_utils_html.htel_mk(
        "label", None, (input_el, f" {prefix_text}", _count_span(count))
    )


def _radio_input(group_name: str, value: str, *, checked: bool) -> object:
    attrs: dict[str, str] = {
        "type": "radio",
        "class": group_name,
        "name": group_name,
        "value": value,
    }
    if checked:
        attrs["checked"] = "checked"
    return wlc_utils_html.htel_mk("input", attrs)


def _count_span(count: int) -> object:
    return wlc_utils_html.span_c(f" ({count})" if count else "", _COUNT_CLASS)
