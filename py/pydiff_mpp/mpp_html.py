"""
Generate an HTML diff report with mgketer-style category filtering.

Exports:
    write_report  — write the HTML report file
"""

import difflib
from collections import Counter

from pydiff_mpp.grapheme_diff import char_diff_spans
from pydiff_mpp.mpp_extract import _collect_template_names
from pydiff_mpp.describe_diff import describe_change
from pydiff_mpp.mpp_nusach import nusach_body_to_html
from pydiff_mpp.mpp_assets import CATEGORY_INFO, write_shared_assets
from pydiff_mpp.mpp_display import (
    display_text,
    normalize_paseq_spacing,
    postprocess_paseq_html,
    postprocess_kq_html,
)
from pydiff_mpp.mpp_book_urls import mam_with_doc_url, wikisource_url, ref_str


def _esc(text):
    """HTML-escape a string."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _narrow_to_changed_words(old_text, new_text):
    """Return list of (old_span, new_span, new_j1, new_j2) tuples.

    Each tuple contains the old and new text spans, plus the word index
    range [j1, j2) in new_words for position tracking.

    When a 'replace' opcode has equal word counts on both sides, each
    word pair is split into its own entry so that independently changed
    words each get their own diff card.
    """
    old_words = old_text.split(" ")
    new_words = new_text.split(" ")
    sm = difflib.SequenceMatcher(None, old_words, new_words, autojunk=False)
    pairs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                ow = old_words[i1 + k]
                nw = new_words[j1 + k]
                if ow != nw:
                    pairs.append((ow, nw, j1 + k, j1 + k + 1))
        else:
            old_span = " ".join(old_words[i1:i2])
            new_span = " ".join(new_words[j1:j2])
            pairs.append((old_span, new_span, j1, j2))
    if not pairs:
        return [(old_text, new_text, 0, len(new_words))]
    return pairs


def _word_char_ranges(text):
    """Return list of (start, end) char positions for each space-separated word."""
    ranges = []
    pos = 0
    for word in text.split(" "):
        ranges.append((pos, pos + len(word)))
        pos += len(word) + 1
    return ranges


def _distribute_nusach(old_text, new_text, nusach_notes, expected_count):
    """Distribute nusach notes across sub-diffs by word-position overlap.

    Narrows on the raw (pre-display-transform) text to get word index
    ranges, converts those to character positions, and assigns each
    nusach note to the sub-diff whose character range overlaps the
    note's [start, end) span.
    """
    empty = [[] for _ in range(expected_count)]
    if not nusach_notes:
        return empty
    raw_pairs = _narrow_to_changed_words(old_text, new_text)
    if len(raw_pairs) != expected_count:
        # Display and raw narrowing diverged (e.g. paseq spacing);
        # fall back to attaching all notes to the last sub-diff.
        result = [[] for _ in range(expected_count)]
        result[-1] = [n["param2"] for n in nusach_notes]
        return result
    word_ranges = _word_char_ranges(new_text)
    result = []
    for _, _, j1, j2 in raw_pairs:
        char_start = word_ranges[j1][0]
        char_end = word_ranges[j2 - 1][1]
        matching = [
            n["param2"]
            for n in nusach_notes
            if n["end"] > char_start and n["start"] < char_end
        ]
        result.append(matching)
    return result


def _expand_diffs(diffs):
    """Expand multi-change verse diffs into one diff per contiguous change group."""
    expanded = []
    for diff in diffs:
        if not diff["text_changed"]:
            out = dict(diff)
            out["nusach_notes"] = [n["param2"] for n in diff.get("nusach_notes", [])]
            expanded.append(out)
            continue
        old_display = normalize_paseq_spacing(
            display_text(diff["old_text"], diff["old_ep"])
        )
        new_display = normalize_paseq_spacing(
            display_text(diff["new_text"], diff["new_ep"])
        )
        pairs = _narrow_to_changed_words(old_display, new_display)
        nusach_notes = diff.get("nusach_notes", [])
        notes_per_pair = _distribute_nusach(
            diff["old_text"], diff["new_text"], nusach_notes, len(pairs)
        )
        for idx, (old_narrow, new_narrow, _, _) in enumerate(pairs):
            sub = {
                "book": diff["book"],
                "chapter": diff["chapter"],
                "verse": diff["verse"],
                "category": diff["category"],
                "text_changed": True,
                "narrowed_old": old_narrow,
                "narrowed_new": new_narrow,
                "nusach_notes": notes_per_pair[idx],
            }
            expanded.append(sub)
    return expanded


def _render_summary_table(counts, total):
    rows = []
    rows.append('<table class="summary">')
    rows.append("<tr><th></th><th>Category</th><th>Count</th></tr>")
    for cat, count in counts.most_common():
        label, _ = CATEGORY_INFO.get(cat, (cat, "#888"))
        rows.append(
            f'<tr data-cat="{_esc(cat)}">'
            f'<td><span class="cat-swatch" style="background:var(--cat-{cat})"></span></td>'
            f"<td>{_esc(label)}</td><td>{count}</td></tr>"
        )
    rows.append(f'<tr class="total-row"><td></td><td>Total</td><td>{total}</td></tr>')
    rows.append("</table>")
    return "\n".join(rows)


def _render_filter_buttons(counts):
    parts = ['<div class="filter-bar">']
    parts.append('<button class="filter-btn" id="show-all-btn">Show all</button>')
    for cat, count in counts.most_common():
        label, _ = CATEGORY_INFO.get(cat, (cat, "#888"))
        parts.append(
            f'<button class="filter-btn" data-cat="{_esc(cat)}">'
            f"{_esc(label)} ({count})</button>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def _render_card(diff):
    cat = diff["category"]
    label, _ = CATEGORY_INFO.get(cat, (cat, "#888"))
    ref = ref_str(diff)
    mwd_url = mam_with_doc_url(diff["book"], diff["chapter"], diff["verse"])
    ws_url = wikisource_url(diff["book"], diff["chapter"])
    lines = [f'<div class="diff-card" data-categories="{_esc(cat)}">']
    lines.append(
        f'<div class="verse-ref"><span class="ref-text">{_esc(ref)}'
        f' <a class="ref-link" href="{_esc(mwd_url)}" target="_blank" rel="noopener">MAM</a>'
        f' <a class="ref-link" href="{_esc(ws_url)}" target="_blank" rel="noopener">WS</a>'
        f"</span>"
        f'<span class="cat-badge cat-{cat}">{_esc(label)}</span></div>'
    )
    if diff["text_changed"]:
        old_narrow = diff["narrowed_old"]
        new_narrow = diff["narrowed_new"]
        old_html, new_html = char_diff_spans(old_narrow, new_narrow)
        old_html = postprocess_paseq_html(old_html)
        new_html = postprocess_paseq_html(new_html)
        old_html = postprocess_kq_html(old_html)
        new_html = postprocess_kq_html(new_html)
        lines.append(
            '<div class="change-display">'
            f'<span class="heb old-side">{old_html}</span>'
            '<span class="arrow">&rarr;</span>'
            f'<span class="heb new-side">{new_html}</span>'
            "</div>"
        )
        eng_desc = describe_change(
            old_narrow, new_narrow, cat, diff["book"], diff["chapter"], diff["verse"]
        )
        if eng_desc:
            lines.append(f'<div class="change-desc">{_esc(eng_desc)}</div>')
    else:
        old_names = set(_collect_template_names(diff["old_ep"]))
        new_names = set(_collect_template_names(diff["new_ep"]))
        added = sorted(new_names - old_names)
        removed = sorted(old_names - new_names)
        desc_parts = []
        if added:
            desc_parts.append("added: " + ", ".join(added))
        if removed:
            desc_parts.append("removed: " + ", ".join(removed))
        detail = "; ".join(desc_parts) if desc_parts else "template restructured"
        lines.append(f'<div class="change-desc">Template change ({_esc(detail)})</div>')
    for note in diff.get("nusach_notes", []):
        body_html = nusach_body_to_html(note)
        lines.append(
            '<div class="nusach-note">'
            '<span class="nusach-label">\u05e0\u05d5\u05e1\u05d7</span>'
            f'<div class="nusach-body">{body_html}</div>'
            "</div>"
        )
    lines.append("</div>")
    return "\n".join(lines)


def _render_cards(diffs):
    book_counts = Counter(d["book"] for d in diffs)
    parts = []
    current_book = None
    for diff in diffs:
        if diff["book"] != current_book:
            current_book = diff["book"]
            n = book_counts[current_book]
            suffix = "diff" if n == 1 else "diffs"
            parts.append(
                f'<h2 class="book-header" data-books="{_esc(current_book)}"'
                f' data-total="{n}">'
                f"{_esc(current_book)} "
                f'(<span class="book-count">{n} {suffix}</span>)</h2>'
            )
        parts.append(_render_card(diff))
    return "\n".join(parts)


def write_report(diffs, old_rev, new_rev, out_path):
    """Write the full HTML report to out_path."""
    import os

    out_dir = os.path.dirname(out_path)
    write_shared_assets(out_dir)
    diffs = _expand_diffs(diffs)
    counts = Counter(d["category"] for d in diffs)
    total = len(diffs)
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>MPP Diff: {_esc(old_rev)} \u2192 {_esc(new_rev)}</title>",
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        "<h1>MAM Body Text Changes</h1>",
        f'<p class="subtitle">{_esc(old_rev)} &rarr; {_esc(new_rev)}'
        f" &mdash; {total} change{'s' if total != 1 else ''} found</p>",
        '<h2 id="summary">Summary by category</h2>',
        _render_summary_table(counts, total),
        '<h2 id="diffs">Changes (reading order)</h2>',
        _render_filter_buttons(counts),
        _render_cards(diffs),
        '<script src="filter.js"></script>',
        "</body>",
        "</html>",
    ]
    html = "\n".join(html_parts)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
