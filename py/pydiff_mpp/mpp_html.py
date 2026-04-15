"""
Generate an HTML diff report with mgketer-style category filtering.

Exports:
    write_report  — write the HTML report file
"""

import difflib
from collections import Counter

from pydiff_mpp.grapheme_diff import char_diff_spans
from pydiff_mpp.mpp_structure import _template_name_multiset_delta
from pydiff_mpp.describe_diff import describe_change, add_name_tooltips
from pydiff_mpp.mpp_nusach import nusach_body_to_html
from pydiff_mpp.mpp_assets import CATEGORY_INFO, write_shared_assets
from pydiff_mpp.mpp_expand import split_structural_diff
from pydiff_mpp.mpp_template_change_desc import kq_if_template_addition_parts
from pydiff_mpp.mpp_display import (
    display_text,
    normalize_paseq_spacing,
    postprocess_gray_maqaf_html,
    postprocess_paseq_html,
    postprocess_kq_html,
)
from pydiff_mpp.mpp_book_urls import mam_with_doc_url, wikisource_url, ref_str
from pydiff_mpp.mpp_subtitle import render_subtitle_table


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


def _format_template_name_changes(names):
    """Format template-name deltas, collapsing duplicates as xN counts."""
    counts = Counter(names)
    parts = []
    for name in sorted(counts):
        count = counts[name]
        if count == 1:
            parts.append(name)
        else:
            parts.append(f"{name} x{count}")
    return ", ".join(parts)


def _note_bodies(notes):
    return [note if isinstance(note, str) else note["param2"] for note in notes]


def _expand_diffs(diffs):
    """Expand multi-change verse diffs into one diff per contiguous change group."""
    expanded = []
    for diff in diffs:
        if not diff["text_changed"]:
            split = split_structural_diff(diff)
            if split:
                for sub in split:
                    out = dict(sub)
                    out["nusach_notes"] = _note_bodies(sub.get("nusach_notes", []))
                    expanded.append(out)
                continue
            out = dict(diff)
            out["nusach_notes"] = _note_bodies(diff.get("nusach_notes", []))
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
        tmpl_added, tmpl_removed = _template_name_multiset_delta(
            diff["old_ep"], diff["new_ep"]
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
                "old_ep": diff["old_ep"],
                "new_ep": diff["new_ep"],
                "nusach_notes": notes_per_pair[idx],
            }
            if tmpl_added:
                sub["templates_added"] = tmpl_added
            if tmpl_removed:
                sub["templates_removed"] = tmpl_removed
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
            f"{_esc(label)}</button>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def _render_card(diff):
    cat = diff["category"]
    label, _ = CATEGORY_INFO.get(cat, (cat, "#888"))
    ref = ref_str(diff)
    mwd_url = mam_with_doc_url(diff["book"], diff["chapter"], diff["verse"])
    ws_url = wikisource_url(diff["book"], diff["chapter"])
    desc_html = ""
    # Compute description first so it can go on the top line
    if diff["text_changed"]:
        old_narrow = diff["narrowed_old"]
        new_narrow = diff["narrowed_new"]
        eng_desc = describe_change(
            old_narrow,
            new_narrow,
            cat,
            diff["book"],
            diff["chapter"],
            diff["verse"],
            diff.get("old_ep"),
            diff.get("new_ep"),
        )
        tmpl_added = diff.get("templates_added", [])
        tmpl_removed = diff.get("templates_removed", [])
        if tmpl_added or tmpl_removed:
            tmpl_parts = []
            if tmpl_added:
                tmpl_parts.append("added: " + _format_template_name_changes(tmpl_added))
            if tmpl_removed:
                tmpl_parts.append(
                    "removed: " + _format_template_name_changes(tmpl_removed)
                )
            eng_desc = (
                (eng_desc or "") + "; Template change (" + "; ".join(tmpl_parts) + ")"
            )
    else:
        added = diff.get("templates_added")
        removed = diff.get("templates_removed")
        if added is None or removed is None:
            calc_added, calc_removed = _template_name_multiset_delta(
                diff["old_ep"], diff["new_ep"]
            )
            if added is None:
                added = calc_added
            if removed is None:
                removed = calc_removed

        # For dedicated template-removal categories, use the category's
        # specific template name rather than computing from old_ep/new_ep
        # (which may reflect the full verse change when a diff was split).
        _CAT_TEMPLATE = {"dehi-removal": "מ:דחי", "tsinnor-removal": "מ:צינור"}
        if cat in _CAT_TEMPLATE:
            eng_desc = f"Template change (removed: {_CAT_TEMPLATE[cat]})"
        else:
            parts = diff.get("kq_if_template_addition")
            if parts is None and added == ['קו"כ-אם'] and not removed:
                parts = kq_if_template_addition_parts(diff)
            if parts is not None:
                desc_html = (
                    ' <span class="change-desc">&mdash; Template change '
                    f"(added: {_esc(parts['template_name'])}; "
                    "arg1: "
                    f'<span class="pointed-heb" dir="rtl">{_esc(parts["arg1_text"])}</span>; '
                    "arg2: "
                    f'<span class="pointed-heb" dir="rtl">{_esc(parts["arg2_text"])}</span>; '
                    "previously only the raw text of what is now arg1 was there)"
                    "</span>"
                )
                eng_desc = None
            else:
                desc_parts = []
                if added:
                    desc_parts.append("added: " + _format_template_name_changes(added))
                if removed:
                    desc_parts.append(
                        "removed: " + _format_template_name_changes(removed)
                    )
                detail = (
                    "; ".join(desc_parts) if desc_parts else "template restructured"
                )
                eng_desc = f"Template change ({detail})"
    if eng_desc:
        esc_desc = add_name_tooltips(_esc(eng_desc))
        desc_html = f' <span class="change-desc">&mdash; {esc_desc}</span>'
    lines = [f'<div class="diff-card" data-categories="{_esc(cat)}">']
    lines.append(
        f'<div class="verse-ref"><span class="ref-text">{_esc(ref)}'
        f' <a class="ref-link" href="{_esc(mwd_url)}" target="_blank" rel="noopener">MwD</a>'
        f' <a class="ref-link" href="{_esc(ws_url)}" target="_blank" rel="noopener">WS</a>'
        f"</span>"
        f'<span class="cat-badge cat-{cat}">{_esc(label)}</span>'
        f"{desc_html}</div>"
    )
    if diff["text_changed"]:
        old_html, new_html = char_diff_spans(old_narrow, new_narrow)
        old_html = postprocess_gray_maqaf_html(old_html)
        new_html = postprocess_gray_maqaf_html(new_html)
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
    for note in diff.get("nusach_notes", []):
        body_html = nusach_body_to_html(note)
        lines.append(
            '<div class="nusach-note">'
            '<span class="nusach-label">נוסח</span>'
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


def write_report(diffs, old_rev, new_rev, out_path, old_date="", new_date=""):
    """Write the full HTML report to out_path."""
    import os

    out_dir = os.path.dirname(out_path)
    write_shared_assets(out_dir)
    diffs = _expand_diffs(diffs)
    counts = Counter(d["category"] for d in diffs)
    total = len(diffs)
    subtitle_table = render_subtitle_table(old_rev, new_rev, old_date, new_date, total)
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{_esc(new_date)} (MPP diff)</title>",
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        "<h1>MAM Body Text Changes</h1>",
        '<p class="subtitle"><a href="index.html">Up to MAM Change Logs</a></p>',
        subtitle_table,
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
    return total
