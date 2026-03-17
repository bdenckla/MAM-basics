"""
Generate an HTML diff report with mgketer-style category filtering.

Exports:
    write_report  — write the HTML report file
"""

import difflib
import re
from collections import Counter
from pycmn import file_io
from pydiff_mpp.grapheme_diff import char_diff_spans
from pydiff_mpp.mpp_extract import _collect_template_names, _get_params
from pydiff_mpp.describe_diff import describe_change
from pydiff_mpp.mpp_nusach import nusach_body_to_html

CATEGORY_INFO = {
    "meteg-removal": ("Meteg removal", "#1565c0"),
    "meteg-addition": ("Meteg addition", "#1e88e5"),
    "rafe-reuveni": ("Rafe (ראובני)", "#2e7d32"),
    "varika": ("Varika", "#00695c"),
    "accent-change": ("Accent change", "#ef6c00"),
    "accent-addition": ("Accent addition", "#e65100"),
    "accent-removal": ("Accent removal", "#f57c00"),
    "vowel-change": ("Vowel change", "#6a1b9a"),
    "legarmeih-paseq": ("Legarmeih \u2192 paseq", "#ad1457"),
    "template-change": ("Template change", "#795548"),
    "misc": ("Miscellaneous", "#37474f"),
}

# ── Paseq display (ruby annotations for legarmeih / narpas) ──

_LEG_SENTINEL = "\ufdd0"
_NAR_SENTINEL = "\ufdd1"
_LEG_RUBY = '<ruby class="paseq-ruby">\u05c0<rt>\u05dc</rt></ruby>'
_NAR_RUBY = '<ruby class="paseq-ruby">\u05c0<rt>\u05e4</rt></ruby>'


def _collect_paseq_types(obj, types):
    """Recursively collect paseq template types, mirroring flatten_ep."""
    if isinstance(obj, str):
        return
    if isinstance(obj, dict):
        name = obj["tmpl_name"]
        if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
            types.append("legarmeih")
            return
        if name == "מ:פסק":
            types.append("narpas")
            return
        params = _get_params(obj)
        if name == "נוסח":
            if "1" in params:
                _collect_paseq_types(params["1"], types)
            return
        if name in ('קו"כ', 'כו"ק'):
            if "1" in params:
                _collect_paseq_types(params["1"], types)
            if "2" in params:
                _collect_paseq_types(params["2"], types)
            return
        if name == "מ:קמץ":
            if "ד" in params:
                _collect_paseq_types(params["ד"], types)
            return
        if "1" in params:
            _collect_paseq_types(params["1"], types)
        return
    if isinstance(obj, list):
        for item in obj:
            _collect_paseq_types(item, types)


def _display_text(text, ep):
    """Replace U+05C0 in flattened text with legarmeih/narpas sentinels."""
    types = []
    for el in ep:
        _collect_paseq_types(el, types)
    result = []
    ti = 0
    for ch in text:
        if ch == "\u05c0":
            result.append(_LEG_SENTINEL if types[ti] == "legarmeih" else _NAR_SENTINEL)
            ti += 1
        else:
            result.append(ch)
    return "".join(result)


def _normalize_paseq_spacing(text):
    """Normalize spacing around paseq sentinels for display.

    Legarmeih: tight against preceding word, regular space after.
    Narpas:    non-breaking space before, regular space after.
    """
    text = re.sub(r" ?" + _LEG_SENTINEL + r" ?", _LEG_SENTINEL + " ", text)
    text = re.sub(r" ?" + _NAR_SENTINEL + r" ?", "\u00a0" + _NAR_SENTINEL + " ", text)
    return text


def _postprocess_paseq_html(html_str):
    """Replace paseq sentinels with ruby HTML."""
    return html_str.replace(_LEG_SENTINEL, _LEG_RUBY).replace(_NAR_SENTINEL, _NAR_RUBY)


def _esc(text):
    """HTML-escape a string."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _narrow_to_changed_words(old_text, new_text):
    """Return a list of (old_span, new_span) pairs, one per contiguous change.

    Splits on spaces and uses SequenceMatcher to find each contiguous
    group of changed words, returning them as separate pairs rather than
    one large span covering all changes.
    """
    old_words = old_text.split(" ")
    new_words = new_text.split(" ")
    sm = difflib.SequenceMatcher(None, old_words, new_words, autojunk=False)
    pairs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        old_span = " ".join(old_words[i1:i2])
        new_span = " ".join(new_words[j1:j2])
        pairs.append((old_span, new_span))
    if not pairs:
        return [(old_text, new_text)]
    return pairs


def _css():
    lines = []
    lines.append(":root {")
    lines.append("  --bg: #fafafa; --card-bg: #fff; --border: #ddd;")
    lines.append("  --accent: #4a90d9; --hi-old: #fdd; --hi-new: #dfd;")
    for cat, (_, color) in CATEGORY_INFO.items():
        lines.append(f"  --cat-{cat}: {color};")
    lines.append("}")
    lines.append("""* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font: 15px/1.6 "Segoe UI", system-ui, sans-serif;
  background: var(--bg); color: #333;
  padding: 0 2rem 1.5rem; max-width: 1100px; margin: 0 auto;
}
h1 { font-size: 1.5rem; margin-bottom: .3rem; margin-top: 1rem; }
h2 { font-size: 1.2rem; margin-top: 1.5rem; margin-bottom: .5rem; }
.subtitle { color: #666; font-size: .9rem; margin-bottom: 1.5rem; }
table.summary {
  border-collapse: collapse; margin-bottom: 1.5rem; width: 100%; max-width: 500px;
}
table.summary th, table.summary td {
  text-align: left; padding: .35rem .75rem; border-bottom: 1px solid var(--border);
}
table.summary th { background: #f0f0f0; font-weight: 600; }
table.summary .cat-swatch {
  display: inline-block; width: 12px; height: 12px;
  border-radius: 2px; margin-right: 6px; vertical-align: middle;
}
table.summary tr[data-cat] { cursor: pointer; }
table.summary tr[data-cat]:hover { background: #f5f5f5; }
table.summary tr.active { background: var(--accent); color: #fff; }
table.summary tr.total-row { font-weight: 600; cursor: default; }
.filter-bar { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: 1rem; }
.filter-btn {
  font-size: .8rem; padding: .25rem .6rem;
  border: 1px solid var(--border); border-radius: 4px;
  background: #fff; cursor: pointer; transition: background .15s;
}
.filter-btn:hover { background: #eee; }
.filter-btn.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.diff-card {
  background: var(--card-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: .5rem .8rem; margin-bottom: .4rem;
}
.diff-card.hidden { display: none; }
.verse-ref { display: flex; align-items: baseline; gap: .4rem; flex-wrap: wrap; }
.ref-text { font-weight: 600; font-size: .9rem; }
.cat-badge {
  font-size: .7rem; padding: .1rem .45rem; border-radius: 3px;
  color: #fff; white-space: nowrap;
}
.heb {
  font-family: "SBL Hebrew", "Ezra SIL", "David", "Times New Roman", serif;
  font-size: 20pt; direction: rtl; unicode-bidi: embed;
}
.change-display {
  display: flex; align-items: center; gap: .5rem; margin-top: .2rem; flex-wrap: wrap;
}
.old-side, .new-side { padding: .15rem .5rem; border-radius: 4px; }
.old-side { background: var(--hi-old); }
.new-side { background: var(--hi-new); }
.old-side mark.diff-hi { background: #f9a0a0; border-radius: 2px; }
.new-side mark.diff-hi { background: #a0d8a0; border-radius: 2px; }
.arrow { font-size: 1.1rem; color: #888; }
.change-desc { font-size: .85rem; color: #555; margin-top: .15rem; }
.book-header { margin-top: 1.2rem; margin-bottom: .3rem; }
.book-header.hidden { display: none; }
.nusach-note {
  border-left: 3px solid #f9a825;
  background: #fffde7;
  padding: .3rem .6rem;
  margin-top: .3rem;
  border-radius: 4px;
}
.nusach-label {
  font-weight: 600;
  color: #f57f17;
  font-size: .8rem;
}
.nusach-body {
  direction: rtl;
  unicode-bidi: embed;
  margin-top: .1rem;
  font-size: .85rem;
}
.pointed-heb {
  font-family: "SBL Hebrew", "Ezra SIL", "David", "Times New Roman", serif;
  font-size: 20pt;
}
.letter-large { font-size: 130%; }
.letter-small { font-size: 75%; }
.letter-hung { vertical-align: super; font-size: 85%; }
@media (max-width: 700px) {
  .change-display { flex-direction: column; align-items: flex-start; }
}""")
    lines.append("""ruby.paseq-ruby {
  ruby-position: over;
}
ruby.paseq-ruby rt {
  font-size: 60%;
  font-weight: normal;
  color: #888;
}""")
    for cat in CATEGORY_INFO:
        lines.append(f".cat-{cat} {{ background: var(--cat-{cat}); }}")
    return "\n".join(lines)


def _js():
    return """(function() {
  var activeFilters = new Set();
  var cards = document.querySelectorAll('.diff-card');
  var buttons = document.querySelectorAll('.filter-btn');
  var summaryRows = document.querySelectorAll('table.summary tr[data-cat]');
  var bookHeaders = document.querySelectorAll('.book-header');
  function update() {
    cards.forEach(function(card) {
      var cat = card.getAttribute('data-categories');
      card.classList.toggle('hidden',
        activeFilters.size > 0 && !activeFilters.has(cat));
    });
    bookHeaders.forEach(function(hdr) {
      var next = hdr.nextElementSibling;
      var visCount = 0;
      while (next && !next.classList.contains('book-header')) {
        if (next.classList.contains('diff-card') && !next.classList.contains('hidden')) {
          visCount++;
        }
        next = next.nextElementSibling;
      }
      hdr.classList.toggle('hidden', visCount === 0);
      var span = hdr.querySelector('.book-count');
      if (span) {
        var total = parseInt(hdr.getAttribute('data-total'), 10);
        if (activeFilters.size === 0) {
          span.textContent = total + (total === 1 ? ' diff' : ' diffs');
        } else {
          span.textContent = visCount + ' of ' + total;
        }
      }
    });
  }
  function toggleFilter(cat) {
    if (activeFilters.has(cat)) activeFilters.delete(cat);
    else activeFilters.add(cat);
    buttons.forEach(function(b) {
      b.classList.toggle('active', activeFilters.has(b.getAttribute('data-cat')));
    });
    summaryRows.forEach(function(r) {
      r.classList.toggle('active', activeFilters.has(r.getAttribute('data-cat')));
    });
    update();
  }
  buttons.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var cat = btn.getAttribute('data-cat');
      if (cat) toggleFilter(cat);
    });
  });
  summaryRows.forEach(function(row) {
    row.addEventListener('click', function() {
      var cat = row.getAttribute('data-cat');
      if (cat) toggleFilter(cat);
    });
  });
  var showAll = document.getElementById('show-all-btn');
  if (showAll) {
    showAll.addEventListener('click', function() {
      activeFilters.clear();
      buttons.forEach(function(b) { b.classList.remove('active'); });
      summaryRows.forEach(function(r) { r.classList.remove('active'); });
      update();
    });
  }
})();"""


def _ref_str(diff):
    """Format a verse reference like 'Gen 1:1'."""
    book = diff["book"]
    # Shorten common long names
    short = {
        "Deuteronomy": "Deut",
        "Leviticus": "Lev",
        "1 Samuel": "1Sam",
        "2 Samuel": "2Sam",
        "1 Kings": "1Kgs",
        "2 Kings": "2Kgs",
        "1 Chronicles": "1Chr",
        "2 Chronicles": "2Chr",
        "Song of Songs": "Song",
        "Lamentations": "Lam",
        "Ecclesiastes": "Eccl",
        "Zephaniah": "Zeph",
        "Zechariah": "Zech",
        "Habakkuk": "Hab",
        "Nehemiah": "Neh",
    }
    bk = short.get(book, book)
    return f"{bk} {diff['chapter']}:{diff['verse']}"


def _expand_diffs(diffs):
    """Expand multi-change verse diffs into one diff per contiguous change group."""
    expanded = []
    for diff in diffs:
        if not diff["text_changed"]:
            expanded.append(diff)
            continue
        old_display = _normalize_paseq_spacing(
            _display_text(diff["old_text"], diff["old_ep"])
        )
        new_display = _normalize_paseq_spacing(
            _display_text(diff["new_text"], diff["new_ep"])
        )
        pairs = _narrow_to_changed_words(old_display, new_display)
        nusach_notes = diff.get("nusach_notes", [])
        for idx, (old_narrow, new_narrow) in enumerate(pairs):
            sub = {
                "book": diff["book"],
                "chapter": diff["chapter"],
                "verse": diff["verse"],
                "category": diff["category"],
                "text_changed": True,
                "narrowed_old": old_narrow,
                "narrowed_new": new_narrow,
                "nusach_notes": nusach_notes if idx == len(pairs) - 1 else [],
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
    ref = _ref_str(diff)
    lines = [f'<div class="diff-card" data-categories="{_esc(cat)}">']
    lines.append(
        f'<div class="verse-ref"><span class="ref-text">{_esc(ref)}</span>'
        f'<span class="cat-badge cat-{cat}">{_esc(label)}</span></div>'
    )
    if diff["text_changed"]:
        old_narrow = diff["narrowed_old"]
        new_narrow = diff["narrowed_new"]
        old_html, new_html = char_diff_spans(old_narrow, new_narrow)
        old_html = _postprocess_paseq_html(old_html)
        new_html = _postprocess_paseq_html(new_html)
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
    diffs = _expand_diffs(diffs)
    counts = Counter(d["category"] for d in diffs)
    total = len(diffs)
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>MPP Diff: {_esc(old_rev)} \u2192 {_esc(new_rev)}</title>",
        "<style>",
        _css(),
        "</style>",
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
        "<script>",
        _js(),
        "</script>",
        "</body>",
        "</html>",
    ]
    html = "\n".join(html_parts)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
