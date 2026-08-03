"""Exports write_page: one "long notes" apparatus page per main page (design doc §7.3).

Design doc §7.3 sketches an "intended" MAM-with-doc-style split: short notes inline
in the doc column, long ones relegated to a separate page. MAM-with-doc decides that
split automatically, by a length threshold (> 400 rendered chars). CLC deliberately
does NOT reuse that threshold: an editor opts a specific note in by hand (clc_render's
``_LONG_NOTE_SPECS``), so this module never inspects note length or decides anything
itself -- it only lays out whatever entries it is handed.

Each main page (one per main_clc.py build job, i.e. one per ``clc_render.out_label``)
gets its own long-notes page, so it has exactly one main page to link back to -- unlike
MAM's per-book "big-doc" pages, this is one-per-job rather than one-per-book, matching
write_book's own chapter-limited granularity. A job with no long notes gets no page at
all (write_page returns None). Each entry keeps its own anchor so a short inline note
can link straight to its expanded body.
"""

import uxlc_misc.uxlc_utils_html as H
import uxlc_paths

# ASCII slug for each dual-cant strand's display short name (clc_dual_cant's own
# Strand.short values), used only to keep the anchor id / URL fragment plain ASCII --
# display text elsewhere in the page is untouched.
_STRAND_SLUG = {
    "taḥton": "tahton",
    "elyon": "elyon",
    "pashut": "pashut",
    "midrashit": "midrashit",
}

# Same idea as _STRAND_SLUG, for an omitted-accent note's "kind" (clc_dual_cant's
# describe_diff.accent_name spelling) -- needed since one (book, ch, v, strand) can carry
# more than one omitted-accent long note (e.g. Deut 5:6's elyon wants both a tipexa and an
# etnaxta), so kind must join strand in the anchor id to keep it unique.
_KIND_SLUG = {
    "pashta": "pashta",
    "meteg": "meteg",
    "merkha": "merkha",
    "tipeḥa": "tipeha",  # translit-ok: ASCII anchor-id slug
    "etnaḥta": "etnahta",  # translit-ok: ASCII anchor-id slug
    "silluq": "silluq",
    "pataḥ": "patah",  # an omitted *vowel* (Deut 5:8's elyon מתחת), not an accent
}


def anchor_id(book_id, ch, v, strand, kind):
    """The long-notes page anchor id for one (book, ch, v, strand, kind) case."""
    return f"long-{book_id}-{ch}-{v}-{_STRAND_SLUG[strand]}-{_KIND_SLUG[kind]}"


def page_href(page_label, anchor):
    """Relative link to one entry, from any page in the same gh-pages/clc/ directory."""
    return f"{page_label}-long-notes.html#{anchor}"


def entry(anchor, heading, blocks):
    """One long-note page section: ``blocks`` is a list of H element/strings."""
    return {"anchor": anchor, "heading": heading, "blocks": blocks}


def write_page(page_label, disp, entries, main_page_href):
    """Write gh-pages/clc/<page_label>-long-notes.html from ``entries`` (as built by
    clc_render.build_long_notes), linking its intro back to ``main_page_href`` (that
    job's own main page, e.g. "Deuter-5.html"). Writes nothing and returns None if
    ``entries`` is empty -- a job with no long notes gets no apparatus page."""
    if not entries:
        return None
    body = [
        H.heading_level_1(f"Charitable Leningrad Codex — {disp} — longer notes"),
        H.para(
            [
                "Notes relegated here from the ",
                H.anchor("main page", {"href": main_page_href}),
                "’s doc column.",
            ]
        ),
        *[_section(e) for e in entries],
    ]
    out_path = uxlc_paths.clc_pages_dir() / f"{page_label}-long-notes.html"
    write_ctx = H.WriteCtx(
        title=f"CLC — {disp} — longer notes", path=out_path, add_wbr=True
    )
    H.write_html_to_file(body, write_ctx, "../")
    return out_path


def _section(e):
    return H.div(
        [H.heading_level_2(e["heading"]), *e["blocks"]],
        {"id": e["anchor"], "class": "clc-long-note"},
    )
