"""Poetic ungrammatical-verse report -- the optional Phase 4 analogue of the goerwitz.html report.

The poetic corpus run (``run-poetic``) parses 99.69% of the Three Books
cleanly; the residual splits into two documented ungrammatical kinds:

  * ``missing_silluq`` -- verses whose sof pasuq arrives with no silluq
    code, recovered by the grammar into an ERROR-leaf tree (structure preserved,
    the silluq_phrase mark is ``ERROR``).
  * ``no_parse`` -- an L anomaly for which no valid tree exists (the disjunctive
    hierarchy is violated or a token is lexically illicit), e.g. Job 31:15 and
    Psalms 56:10; emitted as a ``NO_PARSE`` token line by the driver.  (Ps
    17:14's double tsinnor was another such case until the parser began accepting
    a repeated divider as one; see poetic_ply_grammar.parse_tokens_accepting_repeats
    and gh-pages/accgram/ps17v14-double-tsinnor.html.)

This module re-scans + re-parses the poetic corpus (the same source of truth the
driver writes from), collects every ungrammatical verse, and enriches each with: the
verse's pointed-Hebrew text, the full scanned token sequence, the rendered ERROR
tree or NO_PARSE line, and -- the key review datum for accent ungrammatical verses -- the WLC vs
MAM-simple disjunctive sequences (what L's accents say versus what the MAM oracle
reads). It writes a git-tracked ``_oddballs.json`` next to the corpus outputs and
``gh-pages/accgram/poetic.html`` for review.

Each ungrammatical is one ``dict[str, object]`` row -- the single representation that
flows from collection through render to JSON serialization, sharing the prose
front-end's row shape so the shared leaf renderers consume it directly (issues
#40, #41). It carries the shared prose-shaped keys the shared renderers read
(``ref``/``output_file``/``wlc422_kq_u_verse``/``wlc_focus``, plus the SAT
``enriched_row`` payload) alongside the poetic-only keys (``kind``/``token_types``/
``wlc_disjunctives``/``mam_disjunctives``/``mam_words``/``tree_text``/``error``).

The HTML deliberately shares the prose ``goerwitz.html`` shell -- the same
``../style.css``, width-limited wrapper, single flat client-side-filterable
verse list (``poetic-filter.js``), per-verse permalinks + Mwd/UXLC links, the
parse tree rendered as an HTML table via ``ob_tree_table``, and the SAT
focus-word table via ``poetic_sat`` (which reuses the prose ``rtmsr_sat``
renderer). With issue #22 the two reports now share one page-assembly core,
``ob_page`` (the filter controls, the per-verse ``<section>`` wrapper, and the
page shell), each front-end supplying a ``CorpusDescriptor`` (see also issue
#10). It keeps one poetic-only display the prose
page has no analogue for: the WLC-vs-MAM disjunctive compare. The verse-final NO_PARSE cases,
having no valid parse, render a flat best-effort tree (each token a cell, capped
by an ERROR leaf) so they too display through the shared error-tree table.

The mechanically auto-derived WLC-vs-MAM-simple summary is the relevant oracle
for these accent-structure ungrammatical (the prose UXLC change-text enrichment
targets vowel/consonant text changes, which these do not concern); it -- with
the client-side "MAM compare" filter facet -- now carries the WLC-vs-MAM
disjunctive comparison that an earlier standalone skeleton table showed. On top
of it there is an optional hand-authored annotation layer -- the poetic analogue
of the prose ``ob_notes_*`` modules -- in ``poetic_ob_notes``: a per-ungrammatical
``st-summary`` / ``comment`` plus external links (a tanach.us ``uxlc_note_page``,
a ``github-issue``), shown only for the few cases that warrant it. The SAT
focus-word table is reproduced for missing-silluq verses (whose locus is the
verse-final chanted word); NO_PARSE verses, having no single focus word, omit it.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from accgram import ob_error_context
from accgram import ob_page
from accgram import ob_report
from accgram import ob_tree_table
from accgram import poetic_filter
from accgram import poetic_ob_notes
from accgram import poetic_sat
from accgram import research_tao
from accgram import rtms_data
from accgram import rtms_focus_diff_expand
from accgram import rtms_ref
from accgram import rtms_report
from accgram import rtmsr_media
from accgram import rtmsr_verse
from accgram import uni_to_marks
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from accgram.mam_poetic_accents import load_poetic_word_disj
from accgram.mam_simple_verse import default_mam_simple_dir
from accgram.poetic_accent_names import POETIC_DISJUNCTIVES
from accgram.poetic_ply_grammar import (
    build_parser,
    parse_tokens_accepting_repeats,
)
from accgram.poetic_scanner import scan_book
from accgram.poetic_reconcile import reconcile_tokens
from accgram.poetic_oddball_summary import derive_tentative_summary
from accgram.tree import print_tree
from accgram.poetic_run import has_error_leaf, no_parse_line
from mb_cmn import file_io
from mb_cmn import provenance
from py_html import wlc_utils_html
from py_wlc import my_wlc_bcv_str

import wlc_paths

KIND_MISSING_SILLUQ = "missing_silluq"
KIND_NO_PARSE = "no_parse"

# The prose-report-shaped (row, key) -> value lookup the shared rtmsr_* helpers
# expect; for the poetic page the row is ignored and the value comes from the
# ungrammatical's hand-authored poetic_ob_notes entry (see _structured_text_lookup).
StructuredTextLookup = Callable[[dict[str, object], str], object]

# Each poetic ungrammatical is one dict[str, object] row (issue #41), carrying:
#   ref               clean book-name reference, e.g. "Psalms 31:21"
#   bb                two-letter book code
#   kind              KIND_MISSING_SILLUQ | KIND_NO_PARSE
#   body              the Unicode mark body (source content after "ch:vr ")
#   output_file       the *_ag.json holding this verse's parse record
#   token_types       full scanned token-type sequence (tuple[str, ...])
#   wlc_disjunctives  WLC disjunctive skeleton, scanner (tuple[str, ...])
#   mam_disjunctives  MAM oracle skeleton (tuple[str, ...] | None if absent)
#   mam_words         MAM per-chanted-word (base_letters, disjunctive_or_None), the
#                     chanted-word-aligned counterpart of mam_disjunctives used to derive
#                     the summary; None if the verse is absent from MAM-simple.
#                     Not written to _oddballs.json (the skeletons are the datum).
#   tree_text         rendered ERROR tree, or the NO_PARSE line
#   error             the parse stall locus for a NO_PARSE verse (ParseError) --
#                     the offending accent's token type and its 1-based ordinal
#                     among the verse's accents; None for missing-silluq.
#   wlc422_kq_u_verse WLC 4.22 pointed-Hebrew verse (qere-interpolated +
#                     sanitized), the shared key the verse-paragraph renderer
#                     reads; None if the verse is absent from the index. Not
#                     written to _oddballs.json (the skeletons are the datum).
#   wlc_focus         the verse-final chanted word to highlight as the focus (missing-silluq
#                     only, None otherwise), the shared key the verse-paragraph
#                     renderer reads.
#   enriched_row      the build_enriched_row payload (WLC/UXLC/MAM focus-word
#                     verses + diffs) feeding the SAT focus-word table; built
#                     only for missing-silluq verses with a unique verse-final
#                     focus word, None otherwise. Not persisted to _oddballs.json.


def collect_poetic_ungrammatical(
    mam_simple_dir: Path,
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
) -> list[dict[str, object]]:
    """Re-scan + re-parse the poetic corpus and return every ungrammatical verse."""
    mam_words_by_ref = load_poetic_word_disj(mam_simple_dir)
    wlc_index = rtms_data.load_wlc422_index(wlc422_kq_u_dir)
    parser = build_parser()
    book_texts = uni_to_marks.build_book_texts(
        wlc422_kq_u_dir, keep_line_fn=poetic_filter.should_keep_line
    )

    ungrammatical: list[dict[str, object]] = []
    for bb, text in book_texts.items():
        output_file = f"wlc_422_ps_{bb}_ag.json"
        for verse in scan_book(text, bb):
            mam_words = mam_words_by_ref.get(verse.reference)
            mam = (
                [d for _cons, d in mam_words if d is not None]
                if mam_words is not None
                else None
            )
            # Apply the legarmeh-vs-paseq and unmarked-oleh corrections before parsing,
            # exactly as poetic_run does, so this report agrees with the driver's
            # trees (and the two resolved NO_PARSE verses no longer surface here).
            tokens = reconcile_tokens(
                verse.reference, verse.body, list(verse.tokens), mam, parser
            )
            tree, error = parse_tokens_accepting_repeats(parser, tokens)
            if tree is None:
                kind = KIND_NO_PARSE
                tree_text = no_parse_line(tokens, error).rstrip("\n")
            elif has_error_leaf(tree):
                kind = KIND_MISSING_SILLUQ
                error = None
                tree_text = print_tree(tree, 0).rstrip("\n")
            else:
                continue

            wlc = tuple(t for t, _ in tokens if t in POETIC_DISJUNCTIVES)
            bcv = f"{bb}{verse.reference.rpartition(' ')[2]}"
            raw_verse = wlc_index.get(bcv)
            wlc_verse = (
                rtms_data.prepare_wlc422_verse_for_render(raw_verse)
                if isinstance(raw_verse, dict)
                else None
            )
            row: dict[str, object] = {
                "ref": verse.reference,
                "bb": bb,
                "kind": kind,
                "body": verse.body,
                "output_file": output_file,
                "token_types": tuple(t for t, _ in tokens),
                "wlc_disjunctives": wlc,
                "mam_disjunctives": tuple(mam) if mam is not None else None,
                "mam_words": tuple(mam_words) if mam_words is not None else None,
                "tree_text": tree_text,
                "error": error,
                "wlc422_kq_u_verse": wlc_verse,
                "enriched_row": None,
            }
            row["wlc_focus"] = (
                _final_word_focus(row) if kind == KIND_MISSING_SILLUQ else None
            )
            ungrammatical.append(row)

    return _attach_enriched_rows(
        ungrammatical,
        wlc422_kq_u_dir=wlc422_kq_u_dir,
        uxlc_dir=uxlc_dir,
        mam_simple_dir=mam_simple_dir,
    )


def _attach_enriched_rows(
    ungrammatical: list[dict[str, object]],
    *,
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
) -> list[dict[str, object]]:
    """Enrich each missing-silluq ungrammatical with the WLC/UXLC/MAM focus-word payload
    the SAT table needs, leaving NO_PARSE verses (no localized focus) untouched."""
    refs_by_book: dict[str, set[tuple[int, int]]] = {}
    for row in ungrammatical:
        if row["kind"] != KIND_MISSING_SILLUQ:
            continue
        _bb, chnu, vrnu, _bcv = rtms_report.parse_ref_to_wlc_bcv(_bb_ref(row))
        refs_by_book.setdefault(row["bb"], set()).add((chnu, vrnu))

    wlc422_by_bcv, uxlc_by_bcv, mam_simple_by_bcv = rtms_data.load_source_indexes(
        wlc422_kq_u_dir=wlc422_kq_u_dir,
        uxlc_dir=uxlc_dir,
        mam_simple_dir=mam_simple_dir,
        refs_by_book=refs_by_book,
    )

    for row in ungrammatical:
        row["enriched_row"] = _enriched_row_for(
            row,
            wlc422_by_bcv=wlc422_by_bcv,
            uxlc_by_bcv=uxlc_by_bcv,
            mam_simple_by_bcv=mam_simple_by_bcv,
            wlc422_kq_u_dir=wlc422_kq_u_dir,
            uxlc_dir=uxlc_dir,
            mam_simple_dir=mam_simple_dir,
        )
    return ungrammatical


def _enriched_row_for(
    row: dict[str, object],
    *,
    wlc422_by_bcv: dict[str, dict[str, object]],
    uxlc_by_bcv: dict[str, dict[str, object]],
    mam_simple_by_bcv: dict[str, dict[str, object]],
    wlc422_kq_u_dir: Path,
    uxlc_dir: Path,
    mam_simple_dir: Path,
) -> dict[str, object] | None:
    """The poetic_sat focus-word payload for row's SAT table, or None.

    Only missing-silluq verses get one (their locus is the verse-final focus word);
    a missing UXLC/MAM witness or a non-unique focus degrades to None, in which case
    the verse simply renders no SAT table -- the run stays non-fatal."""
    if row["kind"] != KIND_MISSING_SILLUQ:
        return None
    wlc_focus = poetic_sat.focus_word(
        final_word=_final_word_focus(row), wlc_verse=row["wlc422_kq_u_verse"]
    )
    if not wlc_focus:
        return None
    bb_ref = _bb_ref(row)
    _bb, _chnu, _vrnu, bcv = rtms_report.parse_ref_to_wlc_bcv(bb_ref)
    return poetic_sat.build_focus_enriched_row(
        bb_ref=bb_ref,
        bcv=bcv,
        output_file=row["output_file"],
        wlc_focus=wlc_focus,
        wlc422_by_bcv=wlc422_by_bcv,
        uxlc_by_bcv=uxlc_by_bcv,
        mam_simple_by_bcv=mam_simple_by_bcv,
        wlc422_kq_u_dir=wlc422_kq_u_dir,
        uxlc_dir=uxlc_dir,
        mam_simple_dir=mam_simple_dir,
    )


def _ungrammatical_to_row(row: dict[str, object]) -> dict[str, object]:
    error = row["error"]
    return {
        "ref": row["ref"],
        "bb": row["bb"],
        "kind": row["kind"],
        "content": _unicode_text(row),
        "output_file": row["output_file"],
        "token_types": list(row["token_types"]),
        "wlc_disjunctives": list(row["wlc_disjunctives"]),
        "mam_disjunctives": (
            list(row["mam_disjunctives"])
            if row["mam_disjunctives"] is not None
            else None
        ),
        # For a NO_PARSE verse, where the parse dead-ended (the offending accent's
        # token type and its 1-based ordinal among the verse's accents); null for a
        # missing-silluq verse, which has a full ERROR-leaf tree instead.
        "stall": (
            {"accent_index": error.accent_index, "token_type": error.token_type}
            if error is not None
            else None
        ),
        "tree": row["tree_text"],
    }


def build_payload(
    ungrammatical: list[dict[str, object]], source_file: str
) -> dict[str, object]:
    kinds: dict[str, int] = {}
    for row in ungrammatical:
        kind = row["kind"]
        kinds[kind] = kinds.get(kind, 0) + 1
    payload: dict[str, object] = {
        "artifacts_description": "poetic (Three Books) ungrammatical verses for review",
        "payload_provenance_note": (
            "Each row is a poetic verse the checker could not parse cleanly: either "
            "a missing-silluq verse recovered into an ERROR-leaf tree "
            f"('{KIND_MISSING_SILLUQ}') or a structural L anomaly -- the disjunctive "
            "hierarchy is violated or a token is lexically illicit -- emitted as "
            f"a NO_PARSE line ('{KIND_NO_PARSE}'). wlc_disjunctives is the scanner's "
            "disjunctive skeleton; mam_disjunctives is the MAM-simple oracle's, for "
            "comparison. For a NO_PARSE verse, stall names the offending accent (its "
            "1-based ordinal among the verse's accents and its token type) -- where "
            "the LALR(1) parse dead-ended, i.e. every accent before it was consumable "
            "(the stall point, not necessarily the root-cause accent). output_file "
            "names the *_ag.json holding the verse's parse record."
        ),
        "summary": {
            "oddballs": len(ungrammatical),
            "missing_silluq": kinds.get(KIND_MISSING_SILLUQ, 0),
            "no_parse": kinds.get(KIND_NO_PARSE, 0),
        },
        "oddballs": [_ungrammatical_to_row(row) for row in ungrammatical],
    }
    return provenance.with_json_provenance(payload, source_file)


# The poetic page shares goerwitz.html's stylesheet + width-limited shell and
# the same single flat, client-side-filterable verse list (see
# gh-pages/accgram/poetic-filter.js); the shared page-assembly now lives in
# ob_page (issue #22). It keeps one poetic-only data display the prose page has no
# analogue for: the WLC-vs-MAM disjunctive compare (the relevant oracle for
# accent-structure ungrammatical verses). The verse text is shown as pointed Hebrew (issue #9
# retired the Michigan-Claremont body from the reports).
_REPORT_TITLE = "Poetic checker run on WLC"
_REPORT_HEADING = "Poetic checker run on WLC"
_FILTER_SCRIPT_NAME = "poetic-filter.js"
_SELF_LINK_SYMBOL = "🔗"

_KIND_LABEL = {
    KIND_MISSING_SILLUQ: "Missing silluq (ERROR-leaf recovery)",
    KIND_NO_PARSE: "NO_PARSE (L anomaly — no valid tree exists)",
}

# Short labels for the kind filter checkboxes (the headings use _KIND_LABEL).
_KIND_FILTER_LABEL = {
    KIND_MISSING_SILLUQ: "missing silluq",
    KIND_NO_PARSE: "NO_PARSE",
}

# Display labels for the book and MAM-compare filter facets, in filter order.
_BOOK_LABEL = {"ps": "Psalms", "pr": "Proverbs", "jb": "Job"}
_AGREE_LABEL = {
    "agree": "WLC = MAM",
    "differ": "WLC ≠ MAM",
    "na": "not in MAM-simple",
}


def _agree_slug(row: dict[str, object]) -> str:
    """Filter facet for the WLC-vs-MAM disjunctive compare (see _AGREE_LABEL)."""
    if row["mam_disjunctives"] is None:
        return "na"
    return "agree" if row["wlc_disjunctives"] == row["mam_disjunctives"] else "differ"


def _bb_ref(row: dict[str, object]) -> str:
    """Rebuild the two-letter bb form ("ps 31:20") the shared rtms_ref/url
    helpers expect from the clean book-name reference ("Psalms 31:20")."""
    _name, _sep, chv = str(row["ref"]).rpartition(" ")
    return f"{row['bb']} {chv}"


def _structured_text_lookup(row: dict[str, object]) -> StructuredTextLookup:
    """A ``(row, key) -> value`` lookup over this ungrammatical's hand-authored notes.

    Returns the prose-report-shaped callable the shared rtmsr_media/ rtmsr_verse
    helpers expect; ``row`` is ignored (the notes are keyed by the ungrammatical's bb
    reference, not carried on a row). Yields ``None`` for every key when the
    ungrammatical has no hand-authored entry."""
    notes = poetic_ob_notes.get_structured_text().get(_bb_ref(row))
    notes = notes if isinstance(notes, dict) else {}
    return lambda _row, key: notes.get(key)


def render_body_contents(ungrammatical: list[dict[str, object]]) -> tuple[object, ...]:
    counts = _counts(ungrammatical)
    ordered = sorted(
        ungrammatical, key=lambda row: rtms_ref.reading_order_key(_bb_ref(row))
    )

    descriptor = ob_page.CorpusDescriptor(
        heading_blocks=_build_intro(ungrammatical),
        facets=_build_facets(counts),
        count_para_class="pf-count",
        verse_sections=tuple(
            _render_ungrammatical_section(row, is_first=index == 0)
            for index, row in enumerate(ordered)
        ),
        tail_blocks=(),
        filter_script_name=_FILTER_SCRIPT_NAME,
    )
    return ob_page.build_page_body(descriptor)


def _build_intro(ungrammatical: list[dict[str, object]]) -> tuple[object, ...]:
    n_silluq = sum(1 for row in ungrammatical if row["kind"] == KIND_MISSING_SILLUQ)
    n_noparse = sum(1 for row in ungrammatical if row["kind"] == KIND_NO_PARSE)
    return (
        wlc_utils_html.heading_level_1(_REPORT_HEADING),
        wlc_utils_html.heading_level_2("Introduction"),
        wlc_utils_html.para(
            f"This page lists the {len(ungrammatical)} poetic (Three Books) WLC 4.22 "
            f"verses the poetic accent grammar cannot parse cleanly "
            f"({n_silluq} missing-silluq, {n_noparse} NO_PARSE). Use the filter "
            "below to narrow the list."
        ),
        wlc_utils_html.para(
            (
                "For the converse — the quirks the checker silently accepts rather "
                "than flags, including the poetic ps124:4 geresh charity, with the "
                "alternate readings shown as parse trees — see the ",
                wlc_utils_html.anchor("Almost errors", {"href": "almost-errors.html"}),
                " page.",
            )
        ),
        wlc_utils_html.para("Each verse falls into one of two documented kinds:"),
        wlc_utils_html.unordered_list(
            (
                "“missing silluq,” where the sof pasuq arrives with no silluq, "
                "recovered into an ERROR-leaf tree (structure preserved).",
                "“NO_PARSE,” a structural L anomaly for which no valid tree exists "
                "— whether the disjunctive hierarchy is violated or a token is "
                "lexically illicit; the offending accent (where the parse "
                "dead-ended) is marked “← stalled here” in its tree and named in "
                "the meta line.",
            )
        ),
        wlc_utils_html.para(
            (
                "Each verse shows its pointed-Hebrew text (the verse-final chanted word "
                "highlighted for missing-silluq cases) and — for missing-silluq "
                "verses — a SAT focus-word "
                "table comparing the WLC focus word against its UXLC and MAM-simple "
                "readings. The "
                "per-verse summary is mechanically auto-derived — but from an "
                "alignment of the two verses chanted word by chanted word, not from the "
                "conjunctive-stripped skeletons above, so a divider that merely "
                "sits on a different chanted word is reported as such rather than as a "
                "phantom substitution. It is labelled tentative — not a hand-vetted "
                "attribution. See ",
                wlc_utils_html.code("doc/PLAN-poetic-accent-grammar.md"),
                " for the full taxonomy.",
            )
        ),
    )


def _render_ungrammatical_section(row: dict[str, object], *, is_first: bool) -> object:
    bb, chnu, vrnu, bcv = rtms_report.parse_ref_to_wlc_bcv(_bb_ref(row))
    anchor_id = ob_report.ungrammatical_anchor_id(bcv)

    items: list[object] = [
        wlc_utils_html.heading_level_2(str(row["ref"]), {"id": anchor_id})
    ]
    items.extend(
        _render_ref_links(
            row, bb=bb, chnu=chnu, vrnu=vrnu, bcv=bcv, anchor_id=anchor_id
        )
    )
    items.append(_render_summary(row))
    hebrew_verse = _render_hebrew_verse(row)
    if hebrew_verse is not None:
        items.append(hebrew_verse)
    items.append(
        wlc_utils_html.para(
            wlc_utils_html.span(_unicode_text(row), {"lang": "hbo"}),
            {"class": "poetic-src"},
        )
    )
    sat_table = poetic_sat.render_table(row["enriched_row"], row_ref=_bb_ref(row))
    if sat_table is not None:
        items.append(sat_table)
    items.append(_render_meta(row))
    items.append(_render_tree(row))
    items.extend(
        rtmsr_media.render_comment_paragraphs(
            row, structured_text_lookup=_structured_text_lookup(row)
        )
    )
    items.extend(
        rtmsr_media.render_image_paragraphs(
            row, structured_text_lookup=_structured_text_lookup(row)
        )
    )

    return ob_page.render_verse_section(
        items,
        is_first=is_first,
        data_attrs={
            "data-kind": row["kind"],
            "data-book": row["bb"],
            "data-agree": _agree_slug(row),
        },
    )


def _render_ref_links(
    row: dict[str, object],
    *,
    bb: str,
    chnu: int,
    vrnu: int,
    bcv: str,
    anchor_id: str,
) -> tuple[object, ...]:
    lookup = _structured_text_lookup(row)
    permalink = wlc_utils_html.anchor(
        _SELF_LINK_SYMBOL,
        {
            "href": f"#{anchor_id}",
            "title": "Permalink to this section",
            "aria-label": "Permalink to this section",
        },
    )
    perma_contents: list[object] = [permalink, f" Kind: {_KIND_LABEL[row['kind']]}."]
    summary = lookup({}, "st-summary")
    if isinstance(summary, str) and summary.strip():
        perma_contents.append(" Summary: ")
        # Wrap any Hebrew word (e.g. ps56:10's אָ֥֨ז) in an hbo span for the Hebrew font.
        perma_contents.extend(wrap_hebrew_runs(summary.strip()))
    perma_para = wlc_utils_html.para(tuple(perma_contents))

    links: list[object] = [
        wlc_utils_html.anchor(
            "Mwd", {"href": rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu)}
        ),
        " | ",
        wlc_utils_html.anchor(
            "UXLC", {"href": my_wlc_bcv_str.get_tanach_dot_us_url(bcv)}
        ),
    ]
    for label, key in (
        ("UXLC note page", "uxlc_note_page"),
        ("GitHub issue", "github-issue"),
    ):
        url = lookup({}, key)
        if isinstance(url, str) and url.strip():
            links.extend((" | ", wlc_utils_html.anchor(label, {"href": url.strip()})))
    links_para = wlc_utils_html.para(tuple(links))
    return (perma_para, links_para)


def _render_summary(row: dict[str, object]) -> object:
    """A tentative, mechanically auto-derived summary (NOT hand-authored).

    It is computed by aligning the WLC and MAM-simple verses word-for-word (the
    letter skeleton as the key) and reporting each word whose divider differs;
    it is labelled tentative/auto-derived so a reader knows not to treat it as a
    vetted attribution. Earlier this diffed the conjunctive-stripped disjunctive
    skeletons, which conflated a divider that shifted to the neighbouring word into a
    phantom substitution (Ps 68:20 / Pr 30:15); word alignment fixes that. This is the
    poetic analogue of the prose page's hand-authored st-summary / the
    SAT-descriptor-derived summary (rtmsr_sat.derive_summary_from_sat_descriptors).
    """
    return wlc_utils_html.para(
        (
            wlc_utils_html.span_c(
                "Auto-derived summary (tentative): ", "poetic-auto-summary-label"
            ),
            *wrap_hebrew_runs(derive_tentative_summary(row)),
        ),
        {"class": "poetic-auto-summary"},
    )


def _render_hebrew_verse(row: dict[str, object]) -> object | None:
    """Pointed-Hebrew (RTL) verse paragraph via the shared goerwitz renderer.

    For a missing-silluq verse the locus is the verse-final chanted word (the one that
    arrives with no silluq), so highlight it; NO_PARSE is not localized to one
    chanted word, so render the plain verse. A non-unique/absent focus degrades to no
    highlight (the renderer falls back gracefully). The renderer reads the verse
    payload and focus from the row (wlc422_kq_u_verse / wlc_focus)."""
    if not isinstance(row["wlc422_kq_u_verse"], dict):
        return None
    return rtmsr_verse.render_wlc_verse_paragraph(
        row, structured_text_lookup=lambda r, key: r.get(key)
    )


def _unicode_text(row: dict[str, object]) -> str:
    """The verse's normalized pointed-Hebrew text (qere interpolated), from the
    ``-kq-u`` verse; "" if the verse is absent from the index.  Issue #9 replaced the
    Michigan-Claremont source body with this in the report display and ``content``."""
    return rtms_focus_diff_expand.normalized_wlc_verse_text_from_payload(
        row["wlc422_kq_u_verse"]
    )


def _final_word_focus(row: dict[str, object]) -> str | None:
    wlc_verse = row["wlc422_kq_u_verse"]
    vels = wlc_verse.get("vels") if isinstance(wlc_verse, dict) else None
    if not isinstance(vels, list) or not vels:
        return None
    return _token_text(vels[-1]) or None


def _token_text(token: object) -> str:
    if isinstance(token, str):
        return token
    if isinstance(token, dict):
        for key in ("word", "text"):
            value = token.get(key)
            if isinstance(value, str):
                return value
    return ""


def _render_meta(row: dict[str, object]) -> object:
    token_types = row["token_types"]
    error = row["error"]
    contents: list[object] = [f"tokens: {' '.join(token_types)} · "]
    if error is not None:
        n_accents = sum(1 for t in token_types if t not in ("TILDE", "SOFPASUQ"))
        contents.append(
            f"parser stalled at accent {error.accent_index}/{n_accents} "
            f"({error.token_type}) · "
        )
    contents.append(wlc_utils_html.code(str(row["output_file"])))
    return wlc_utils_html.para(tuple(contents), {"class": "poetic-meta"})


def _render_tree(row: dict[str, object]) -> object:
    # missing_silluq carries a real ERROR-leaf tree; NO_PARSE has no valid tree, so
    # synthesize a flat best-effort one (each token a cell, capped by an ERROR leaf)
    # -- both render through the shared error-tree table.
    error = row["error"]
    tree_text = (
        row["tree_text"]
        if row["kind"] == KIND_MISSING_SILLUQ
        else _no_parse_tree_text(
            row["token_types"],
            stall_index=error.accent_index if error is not None else None,
        )
    )
    tree = ob_error_context.parse_error_tree_from_text(tree_text)
    if tree is not None:
        return wlc_utils_html.div(
            (ob_tree_table.render_error_tree_table(tree),),
            {"class": "goerwitz-obs-tree-wrap"},
        )
    # Last-resort fallback: show the raw tree/NO_PARSE line verbatim.
    return wlc_utils_html.div(
        (wlc_utils_html.htel_mk("pre", None, str(row["tree_text"])),),
        {"class": "goerwitz-obs-tree-wrap"},
    )


def _no_parse_tree_text(
    token_types: tuple[str, ...], stall_index: int | None = None
) -> str:
    """A flat best-effort "tree" for a NO_PARSE verse, in print_tree text form.

    No valid parse exists, so this is not a real tree: a single ``no_parse`` branch
    whose leaves are the accent token types (the TILDE/SOFPASUQ structural bookends
    dropped, as in poetic_run.no_parse_line), capped by an ``ERROR`` leaf. Fed
    through the shared error-tree table it puts each token in its own cell and
    highlights the ERROR cell -- more legible than the bare NO_PARSE token line, and
    visually consistent with the missing-silluq ERROR trees.

    When ``stall_index`` (the offending accent's 1-based ordinal, from ParseError) is
    given, that leaf is annotated ``← stalled here`` so the tree pinpoints where the
    parse dead-ended."""
    accents = [t for t in token_types if t not in ("TILDE", "SOFPASUQ")]
    leaves = list(accents)
    if stall_index is not None and 1 <= stall_index <= len(leaves):
        leaves[stall_index - 1] = f"{leaves[stall_index - 1]} ← stalled here"
    leaf_lines = "".join(f"  {leaf}\n" for leaf in leaves)
    return f"0 no_parse\n{leaf_lines}  ERROR\n"


def _build_facets(counts: dict[str, int]) -> tuple[ob_page.Facet, ...]:
    """The poetic filter facets, in display order (see ob_page.build_filter_controls)."""
    return (
        ob_page.CheckboxFacet(
            "Kind",
            "pf-kind",
            tuple(
                (slug, label, counts[f"kind_{slug}"])
                for slug, label in _KIND_FILTER_LABEL.items()
            ),
        ),
        ob_page.CheckboxFacet(
            "Book",
            "pf-book",
            tuple(
                (slug, label, counts[f"book_{slug}"])
                for slug, label in _BOOK_LABEL.items()
            ),
        ),
        ob_page.CheckboxFacet(
            "MAM compare",
            "pf-agree",
            tuple(
                (slug, label, counts[f"agree_{slug}"])
                for slug, label in _AGREE_LABEL.items()
            ),
        ),
    )


def _counts(ungrammatical: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for slug in _KIND_FILTER_LABEL:
        counts[f"kind_{slug}"] = 0
    for slug in _BOOK_LABEL:
        counts[f"book_{slug}"] = 0
    for slug in _AGREE_LABEL:
        counts[f"agree_{slug}"] = 0
    for row in ungrammatical:
        counts[f"kind_{row['kind']}"] += 1
        counts[f"book_{row['bb']}"] += 1
        counts[f"agree_{_agree_slug(row)}"] += 1
    return counts


def default_ungrammatical_out_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "poetic" / "_oddballs.json"


def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / "poetic.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=default_mam_simple_dir(repo_root),
        help="Directory containing MAM-simple json-vtrad-bhs book files.",
    )
    parser.add_argument(
        "--wlc422-kq-u-dir",
        type=Path,
        default=rtms_data.default_wlc422_kq_u_dir(repo_root),
        help="Directory of WLC 4.22 ketiv/qere Unicode 1verses_*.json files "
        "(for pointed-Hebrew verse rendering).",
    )
    parser.add_argument(
        "--uxlc-dir",
        type=Path,
        default=research_tao.default_uxlc_dir(repo_root),
        help="Directory of UXLC-39 book XML files (for the SAT focus-word table).",
    )
    parser.add_argument(
        "--ungrammatical-out",
        type=Path,
        default=default_ungrammatical_out_path(repo_root),
        help="Output JSON path for the poetic ungrammatical records.",
    )
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the poetic ungrammatical-verse report.",
    )


def run(args: argparse.Namespace) -> None:
    ungrammatical = collect_poetic_ungrammatical(
        args.mam_simple_dir, args.wlc422_kq_u_dir, args.uxlc_dir
    )

    payload = build_payload(ungrammatical, __file__)
    ungrammatical_out: Path = args.ungrammatical_out
    # file_io: temp-file write, PermissionError retry, and it makes the directory.
    # build_payload already stamped provenance, so no generator_file= here.
    file_io.json_dump_to_file_path(payload, str(ungrammatical_out))

    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    wlc_utils_html.write_html_to_file(
        body_contents=render_body_contents(ungrammatical),
        write_ctx=wlc_utils_html.WriteCtx(
            title=_REPORT_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )

    n_silluq = sum(1 for row in ungrammatical if row["kind"] == KIND_MISSING_SILLUQ)
    n_noparse = sum(1 for row in ungrammatical if row["kind"] == KIND_NO_PARSE)
    print(
        f"Poetic ungrammatical: {len(ungrammatical)} "
        f"({n_silluq} missing-silluq, {n_noparse} NO_PARSE)"
    )
    print(f"JSON: {ungrammatical_out}")
    print(f"HTML: {html_out}")
