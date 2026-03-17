"""
Generate an HTML diff report with mgketer-style category filtering.

Exports:
    write_report  — write the HTML report file
"""

import difflib
import os
import re
from collections import Counter
from urllib.parse import quote
from pycmn import file_io
from pycmn import hebrew_verse_numerals as hvn
from pydiff_mpp.grapheme_diff import char_diff_spans
from pydiff_mpp.mpp_extract import _collect_template_names, _get_params
from pydiff_mpp.describe_diff import describe_change
from pydiff_mpp.mpp_nusach import nusach_body_to_html

# Keyed by the display names used in diff dicts (from mpp_extract._FILE_STEM_TO_BOOK39S).
# Each value is (OSDF key for MAM-with-doc URLs, Hebrew name for Wikisource URLs).
_BOOK_URL_INFO = {
    "Genesis": ("A1-Genesis", "\u05d1\u05e8\u05d0\u05e9\u05d9\u05ea"),
    "Exodus": ("A2-Exodus", "\u05e9\u05de\u05d5\u05ea"),
    "Leviticus": ("A3-Levit", "\u05d5\u05d9\u05e7\u05e8\u05d0"),
    "Numbers": ("A4-Numbers", "\u05d1\u05de\u05d3\u05d1\u05e8"),
    "Deuteronomy": ("A5-Deuter", "\u05d3\u05d1\u05e8\u05d9\u05dd"),
    "Joshua": ("B1-Joshua", "\u05d9\u05d4\u05d5\u05e9\u05e2"),
    "Judges": ("B2-Judges", "\u05e9\u05d5\u05e4\u05d8\u05d9\u05dd"),
    "1 Samuel": ("BA-1Samuel", "\u05e9\u05de\u05d5\u05d0\u05dc \u05d0"),
    "2 Samuel": ("BB-2Samuel", "\u05e9\u05de\u05d5\u05d0\u05dc \u05d1"),
    "1 Kings": ("BC-1Kings", "\u05de\u05dc\u05db\u05d9\u05dd \u05d0"),
    "2 Kings": ("BD-2Kings", "\u05de\u05dc\u05db\u05d9\u05dd \u05d1"),
    "Isaiah": ("C1-Isaiah", "\u05d9\u05e9\u05e2\u05d9\u05d4\u05d5"),
    "Jeremiah": ("C2-Jeremiah", "\u05d9\u05e8\u05de\u05d9\u05d4\u05d5"),
    "Ezekiel": ("C3-Ezekiel", "\u05d9\u05d7\u05d6\u05e7\u05d0\u05dc"),
    "Hosea": ("CA-Hosea", "\u05d4\u05d5\u05e9\u05e2"),
    "Joel": ("CB-Joel", "\u05d9\u05d5\u05d0\u05dc"),
    "Amos": ("CC-Amos", "\u05e2\u05de\u05d5\u05e1"),
    "Obadiah": ("CD-Obadiah", "\u05e2\u05d5\u05d1\u05d3\u05d9\u05d4"),
    "Jonah": ("CE-Jonah", "\u05d9\u05d5\u05e0\u05d4"),
    "Micah": ("CF-Micah", "\u05de\u05d9\u05db\u05d4"),
    "Nahum": ("CG-Nahum", "\u05e0\u05d7\u05d5\u05dd"),
    "Habakkuk": ("CH-Habakkuk", "\u05d7\u05d1\u05e7\u05d5\u05e7"),
    "Zephaniah": ("CI-Tsefaniah", "\u05e6\u05e4\u05e0\u05d9\u05d4"),
    "Haggai": ("CJ-Haggai", "\u05d7\u05d2\u05d9"),
    "Zechariah": ("CK-Zechariah", "\u05d6\u05db\u05e8\u05d9\u05d4"),
    "Malachi": ("CL-Malachi", "\u05de\u05dc\u05d0\u05db\u05d9"),
    "Psalms": ("D1-Psalms", "\u05ea\u05d4\u05dc\u05d9\u05dd"),
    "Proverbs": ("D2-Proverbs", "\u05de\u05e9\u05dc\u05d9"),
    "Job": ("D3-Job", "\u05d0\u05d9\u05d5\u05d1"),
    "Song of Songs": (
        "E1-Song of Songs",
        "\u05e9\u05d9\u05e8 \u05d4\u05e9\u05d9\u05e8\u05d9\u05dd",
    ),
    "Ruth": ("E2-Ruth", "\u05e8\u05d5\u05ea"),
    "Lamentations": ("E3-Lamentations", "\u05d0\u05d9\u05db\u05d4"),
    "Ecclesiastes": ("E4-Ecclesiastes", "\u05e7\u05d4\u05dc\u05ea"),
    "Esther": ("E5-Esther", "\u05d0\u05e1\u05ea\u05e8"),
    "Daniel": ("F1-Daniel", "\u05d3\u05e0\u05d9\u05d0\u05dc"),
    "Ezra": ("FA-Ezra", "\u05e2\u05d6\u05e8\u05d0"),
    "Nehemiah": ("FB-Nehemiah", "\u05e0\u05d7\u05de\u05d9\u05d4"),
    "1 Chronicles": (
        "FC-1Chronicles",
        "\u05d3\u05d1\u05e8\u05d9 \u05d4\u05d9\u05de\u05d9\u05dd \u05d0",
    ),
    "2 Chronicles": (
        "FD-2Chronicles",
        "\u05d3\u05d1\u05e8\u05d9 \u05d4\u05d9\u05de\u05d9\u05dd \u05d1",
    ),
}


def _mam_with_doc_url(book, chapter, verse):
    osdf = _BOOK_URL_INFO[book][0]
    return f"https://bdenckla.github.io/MAM-with-doc/{osdf}.html#c{chapter}v{verse}"


def _wikisource_url(book, chapter):
    he_chnu = hvn.INT_TO_STR_DIC[chapter]
    name_he = _BOOK_URL_INFO[book][1]
    page_title = quote(f"{name_he}_{he_chnu}/\u05d8\u05e2\u05de\u05d9\u05dd")
    return f"https://he.wikisource.org/wiki/{page_title}"


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
.ref-link {
  font-size: .75rem; font-weight: normal;
  color: var(--accent); text-decoration: none; margin-left: .3rem;
}
.ref-link:hover { text-decoration: underline; }
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
        old_display = _normalize_paseq_spacing(
            _display_text(diff["old_text"], diff["old_ep"])
        )
        new_display = _normalize_paseq_spacing(
            _display_text(diff["new_text"], diff["new_ep"])
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
    ref = _ref_str(diff)
    mwd_url = _mam_with_doc_url(diff["book"], diff["chapter"], diff["verse"])
    ws_url = _wikisource_url(diff["book"], diff["chapter"])
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


def _write_shared_assets(out_dir):
    """Write style.css and filter.js into out_dir if they differ or are missing."""
    css_path = os.path.join(out_dir, "style.css")
    js_path = os.path.join(out_dir, "filter.js")
    css_content = _css()
    js_content = _js()
    for path, content in ((css_path, css_content), (js_path, js_content)):
        existing = None
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = f.read()
        if existing != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


def write_report(diffs, old_rev, new_rev, out_path):
    """Write the full HTML report to out_path."""
    out_dir = os.path.dirname(out_path)
    _write_shared_assets(out_dir)
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
