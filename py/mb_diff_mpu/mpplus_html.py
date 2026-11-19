"""
Generate an HTML diff report with category filtering.

Exports:
    write_report         — write the HTML report file
    credit_name_html     — a credited contributor's name as a card shows it
    credit_evidence_html — a credit's links to its evidence as a card shows them
    credit_line_html     — a card's line crediting a contributor

This subsystem builds HTML by string assembly, deliberately bypassing the repo's
`mb_misc.mb_html` tree-builder (nothing in mb_diff_mpu imports it). The choice is
intentional, not an oversight: the diff/highlight machinery this report is built on
already yields HTML *as strings* (e.g. char_diff_spans, and the postprocess_*_html
passes that rewrite Hebrew maqaf/paseq/kq spans by regex over emitted markup), so the
natural currency here is HTML text, not htel elements. Feeding those fragments through
mb_html would mean round-tripping strings back into a tree only to serialize them
again. The module keeps its own `_esc` escaper and ships its CSS/JS as external assets
(style.css, filter.js via write_shared_assets) rather than an mb_html <head>. The
sibling mpplus_index.py bypasses mb_html for the same reason.
"""

import difflib
from collections import Counter
import unicodedata

from mb_cmn.new_york_time import labelled
from mb_diff_mpu import mpplus_credits, mpplus_json
from mb_diff_mpu.grapheme_diff import char_diff_spans
from mb_diff_mpu.mpplus_structure import template_name_multiset_delta
from mb_diff_mpu.describe_diff import describe_change, add_name_tooltips
from mb_diff_mpu.mpplus_docnote import docnote_body_to_html
from mb_diff_mpu.mpplus_assets import CATEGORY_INFO, write_shared_assets
from mb_diff_mpu.mpplus_expand import split_structural_diff
from mb_diff_mpu.mpplus_template_change_desc import kq_if_template_addition_parts
from mb_diff_mpu.mpplus_display import (
    display_text,
    normalize_paseq_spacing,
    restore_gray_maqaf_text,
    postprocess_gray_maqaf_html,
    postprocess_paseq_html,
    postprocess_kq_html,
)
from mb_diff_mpu.mpplus_book_urls import mam_with_doc_href, wikisource_url, ref_str
from mb_diff_mpu.mpplus_subtitle import render_subtitle_table


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


def _distribute_docnote(old_text, new_text, docnote_notes, expected_count):
    """Distribute docnote notes across sub-diffs by word-position overlap.

    Narrows on the raw (pre-display-transform) text to get word index
    ranges, converts those to character positions, and assigns each
    docnote note to the sub-diff whose character range overlaps the
    note's [start, end) span.
    """
    empty = [[] for _ in range(expected_count)]
    if not docnote_notes:
        return empty
    raw_pairs = _narrow_to_changed_words(old_text, new_text)
    if len(raw_pairs) != expected_count:
        # Display and raw narrowing diverged (e.g. paseq spacing);
        # fall back to attaching all notes to the last sub-diff.
        result = [[] for _ in range(expected_count)]
        result[-1] = [n["param2"] for n in docnote_notes]
        return result
    word_ranges = _word_char_ranges(new_text)
    result = []
    for _, _, j1, j2 in raw_pairs:
        char_start = word_ranges[j1][0]
        char_end = word_ranges[j2 - 1][1]
        matching = [
            n["param2"]
            for n in docnote_notes
            if n["end"] > char_start and n["start"] < char_end
        ]
        result.append(matching)
    return result


def _distribute_credits(diff, expected_count):
    """Give each card of a text change the credit records whose change is its raw pair.

    As in ``_distribute_docnote``, a card's index is its raw pair's index, the pairs being
    narrowed on the raw text, as the JSON's ``changes`` are. A credit names a person, so where
    a credited pair's raw and display narrowings give different counts this raises, rather
    than fall back to the last card as ``_distribute_docnote`` does.
    """
    records = [
        credit for credit in diff.get("credit_records", ()) if credit.change is not None
    ]
    if not records:
        return [[] for _ in range(expected_count)]
    raw_pairs = _narrow_to_changed_words(diff["old_text"], diff["new_text"])
    credited = [
        [credit for credit in records if credit.change == (old, new)]
        for old, new, _, _ in raw_pairs
    ]
    if not any(credited):
        return [[] for _ in range(expected_count)]
    if len(raw_pairs) != expected_count:
        names = "; ".join(credit.describe() for credit in records)
        raise mpplus_credits.CreditError(
            f"{ref_str(diff)}: the raw text narrows to {len(raw_pairs)} changed spans and"
            f" the displayed text to {expected_count} cards, so no card can be found for"
            f" {names}"
        )
    return credited


def _structural_credits(diff):
    """The credit records of a structural card: those its JSON entry holds."""
    records = diff.get("credit_records", ())
    if not records:
        return []
    return mpplus_credits.entry_records(records, mpplus_json._serialize_diff(diff))


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
            if split is not None:
                for sub in split:
                    out = dict(sub)
                    out["docnote_notes"] = _note_bodies(sub.get("docnote_notes", []))
                    out["card_credits"] = _structural_credits(sub)
                    expanded.append(out)
                continue
            out = dict(diff)
            out["docnote_notes"] = _note_bodies(diff.get("docnote_notes", []))
            out["card_credits"] = _structural_credits(diff)
            expanded.append(out)
            continue
        old_display = normalize_paseq_spacing(
            display_text(diff["old_text"], diff["old_ep"])
        )
        new_display = normalize_paseq_spacing(
            display_text(diff["new_text"], diff["new_ep"])
        )
        pairs = _narrow_to_changed_words(old_display, new_display)
        docnote_notes = diff.get("docnote_notes", [])
        notes_per_pair = _distribute_docnote(
            diff["old_text"], diff["new_text"], docnote_notes, len(pairs)
        )
        credits_per_pair = _distribute_credits(diff, len(pairs))
        tmpl_added, tmpl_removed = template_name_multiset_delta(
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
                "docnote_notes": notes_per_pair[idx],
                "card_credits": credits_per_pair[idx],
            }
            if tmpl_added:
                sub["templates_added"] = tmpl_added
            if tmpl_removed:
                sub["templates_removed"] = tmpl_removed
            if idx == 0 and diff.get("alternative_changes"):
                sub["alternative_changes"] = diff["alternative_changes"]
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


def _render_alternative_changes(changes):
    """Render the two approved roles without calling them selected-text changes."""
    labels = {
        ("qere", "content"): "Qere alternative changed",
        ("qere", "pointing-migration"): "Pointing added to the qere alternative",
        (
            "stress-helper-alternative",
            "content",
        ): "Alternative with the stress helper changed",
    }
    paragraphs = []
    for change in changes:
        key = change["role"], change["kind"]
        if key not in labels:
            raise ValueError(f"unclassified rendered alternative change: {key!r}")
        old_html, new_html = char_diff_spans(change["old"], change["new"])
        paragraphs.append(
            '<p class="alternative-change">'
            f'{labels[key]}: <span class="pointed-heb" dir="rtl">{old_html}</span>'
            " &rarr; "
            f'<span class="pointed-heb" dir="rtl">{new_html}</span>.</p>'
        )
    return paragraphs


def credit_name_html(credit):
    """A credited contributor's name as a card shows it.

    The name is shown as given, linked to the contributor's Hebrew Wikisource user page
    when there is one. A right-to-left name, such as a Hebrew one, is isolated with a
    ``<bdi>`` that has no ``lang``, as an unpointed name in English prose is.
    """
    name_html = _esc(credit.name)
    if any(unicodedata.bidirectional(char) in ("R", "AL") for char in credit.name):
        name_html = f"<bdi>{name_html}</bdi>"
    user_page = mpplus_credits.user_page_url(credit)
    if user_page is not None:
        name_html = f'<a href="{_esc(user_page)}" target="_blank" rel="noopener">{name_html}</a>'
    return name_html


def credit_evidence_html(credit):
    """A credit's links to its evidence, comma-separated, each under its label."""
    return ", ".join(
        f'<a href="{_esc(url)}" target="_blank" rel="noopener">{_esc(label)}</a>'
        for _, label, url in credit.evidence
    )


def credit_line_html(credit):
    """The card's line crediting a contributor, with a link to each piece of evidence."""
    return (
        f'<p class="credit">Credit to {credit_name_html(credit)}:'
        f" {credit_evidence_html(credit)}.</p>"
    )


def _card_ids(diffs):
    """Each card's id, or None for a card that carries no credit.

    A credited card's id is ``mpplus_credits.card_id`` of its first credit. A later card of
    the report whose id would repeat an earlier card's, as when one verse changes the same
    form the same way twice, gets -2, -3 and so on after it. An uncredited card has no id,
    so that crediting a change alters no other card.
    """
    seen = Counter()
    ids = []
    for diff in diffs:
        card_credits = diff.get("card_credits", ())
        if not card_credits:
            ids.append(None)
            continue
        base = mpplus_credits.card_id(card_credits[0])
        seen[base] += 1
        ids.append(base if seen[base] == 1 else f"{base}-{seen[base]}")
    return ids


def _render_card(diff, card_id=None):
    cat = diff["category"]
    label, _ = CATEGORY_INFO.get(cat, (cat, "#888"))
    ref = ref_str(diff)
    mwd_href = mam_with_doc_href(diff["book"], diff["chapter"], diff["verse"])
    ws_url = wikisource_url(diff["book"], diff["chapter"])
    desc_html = ""
    # Compute description first so it can go on the top line
    if diff["text_changed"]:
        old_narrow = diff["narrowed_old"]
        new_narrow = diff["narrowed_new"]
        eng_desc = describe_change(
            restore_gray_maqaf_text(old_narrow),
            restore_gray_maqaf_text(new_narrow),
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
            template_desc = "Template change (" + "; ".join(tmpl_parts) + ")"
            eng_desc = "; ".join(part for part in (eng_desc, template_desc) if part)
    else:
        added = diff.get("templates_added")
        removed = diff.get("templates_removed")
        if added is None or removed is None:
            calc_added, calc_removed = template_name_multiset_delta(
                diff["old_ep"], diff["new_ep"]
            )
            if added is None:
                added = calc_added
            if removed is None:
                removed = calc_removed

        # For dedicated template-removal categories, use the category's
        # specific template name rather than computing from old_ep/new_ep
        # (which may reflect the full verse change when a diff was split).
        _CAT_TEMPLATE = {"dexi-removal": "מ:דחי", "tsinnor-removal": "מ:צינור"}
        if cat in _CAT_TEMPLATE:
            eng_desc = f"Template change (removed: {_CAT_TEMPLATE[cat]})"
        else:
            parts = diff.get("kq_if_template_addition")
            if (
                parts is None
                and len(added) == 1
                and added[0] in {"קו״כ-אם", "מ:קו״כ-אם-2"}
                and not removed
            ):
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
                eng_desc = (
                    None
                    if not desc_parts and diff.get("alternative_changes")
                    else f"Template change ({detail})"
                )
    if eng_desc:
        esc_desc = add_name_tooltips(_esc(eng_desc))
        desc_html = f' <span class="change-desc">&mdash; {esc_desc}</span>'
    id_attr = "" if card_id is None else f' id="{_esc(card_id)}"'
    lines = [f'<div class="diff-card"{id_attr} data-categories="{_esc(cat)}">']
    lines.append(
        f'<div class="verse-ref"><span class="ref-text">{_esc(ref)}'
        f' <a class="ref-link" href="{_esc(mwd_href)}" target="_blank" rel="noopener">MwD</a>'
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
    lines.extend(credit_line_html(credit) for credit in diff.get("card_credits", ()))
    lines.extend(_render_alternative_changes(diff.get("alternative_changes", [])))
    for note in diff.get("docnote_notes", []):
        body_html = docnote_body_to_html(note)
        lines.append(
            '<div class="docnote-note">'
            '<span class="docnote-label">נוסח</span>'
            f'<div class="docnote-body">{body_html}</div>'
            "</div>"
        )
    lines.append("</div>")
    return "\n".join(lines)


def _render_cards(diffs):
    book_counts = Counter(d["book"] for d in diffs)
    parts = []
    current_book = None
    for diff, card_id in zip(diffs, _card_ids(diffs)):
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
        parts.append(_render_card(diff, card_id))
    return "\n".join(parts)


def write_report(
    diffs,
    old_label,
    new_label,
    out_path,
    old_date="",
    new_date="",
    *,
    report_css_href: str | None = "../../report.css",
):
    """Write the full HTML report to out_path.

    ``old_label`` and ``new_label`` are ``mpplus_revisions.Revision.label`` pairs. The
    title names the new side's date with its zone, or, for a side with no date -- a
    MAM-basics ref, recorded by its tree id since 2026-09-14 -- the output file's stem,
    such as unpinned-latest.
    """
    import os

    out_dir = os.path.dirname(out_path) or "."
    base_href = write_shared_assets(out_dir, report_css_href=report_css_href)
    diffs = _expand_diffs(diffs)
    counts = Counter(d["category"] for d in diffs)
    total = len(diffs)
    subtitle_table = render_subtitle_table(
        old_label, new_label, old_date, new_date, total
    )
    title = (
        labelled(new_date)
        if new_date
        else os.path.splitext(os.path.basename(out_path))[0]
    )
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{_esc(title)} (MAM-parsed-plus diff)</title>",
        f'<link rel="stylesheet" href="{_esc(base_href)}">',
        '<link rel="stylesheet" href="style.css">',
        "</head>",
        "<body>",
        "<h1>MAM Body Text Changes</h1>",
        '<p class="subtitle"><a href="index.html">Up to MAM Change Logs</a></p>',
        subtitle_table,
        '<p class="subtitle">Includes changes to the selected body text, template '
        "structure, qere alternatives, and alternatives with the stress helper.</p>",
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
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    return total
