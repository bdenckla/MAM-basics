"""
CSS and JS asset generation for MPP diff reports.

Exports:
    CATEGORY_INFO       — category key → (display label, color)
    css                 — return the full CSS string
    js                  — return the full JS string
    write_shared_assets — write style.css and filter.js into a directory
"""

import os
import shutil

CATEGORY_INFO = {
    "meteg-removal": ("Meteg removal", "#1565c0"),
    "meteg-addition": ("Meteg addition", "#1e88e5"),
    "rafe": ("Rafe", "#2e7d32"),
    "varika": ("Varika", "#00695c"),
    "accent-change": ("Accent change", "#ef6c00"),
    "accent-addition": ("Accent addition", "#e65100"),
    "accent-removal": ("Accent removal", "#f57c00"),
    "vowel-change": ("Vowel change", "#6a1b9a"),
    "legarmeih-paseq": ("Legarmeh / paseq", "#ad1457"),
    "maqaf-afor": ("Gray maqaf", "#78909c"),
    "dehi-removal": ("Dehi removal", "#c62828"),
    "tsinnor-removal": ("Tsinnor removal", "#0097a7"),
    "template-change": ("Template change", "#795548"),
    "misc": ("Miscellaneous", "#37474f"),
}


def css():
    """Return the full CSS string for diff reports."""
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
table.subtitle {
  border-collapse: collapse; margin-bottom: .5rem; max-width: 420px;
}
table.subtitle th, table.subtitle td {
  text-align: left; padding: .2rem .75rem; border-bottom: 1px solid var(--border);
}
table.subtitle th { background: #f0f0f0; font-weight: 600; }
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
  font-family: "Taamey D WOFF2", "SBL Hebrew", "Ezra SIL", "David", "Times New Roman", serif;
  font-size: 20pt; direction: rtl; unicode-bidi: embed;
  font-feature-settings: 'ss01';
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
.change-desc { font-size: .85rem; color: #555; }
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
  font-family: "Taamey D WOFF2", "SBL Hebrew", "Ezra SIL", "David", "Times New Roman", serif;
  font-size: 20pt;
  font-feature-settings: 'ss01';
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
}
ruby.kq-pair rt {
  font-size: 20pt;
  font-family: "Taamey D WOFF2", "SBL Hebrew", "Ezra SIL", "David", "Times New Roman", serif;
  font-feature-settings: 'ss01';
}
.kq-k { color: #6a1b9a; }
.kq-q { color: #1565c0; }
.gray-maqaf { color: gray; }""")
    for cat in CATEGORY_INFO:
        lines.append(f".cat-{cat} {{ background: var(--cat-{cat}); }}")
    lines.append("""@font-face {
    font-family: "Taamey D WOFF2";
    src: url("woff2/Taamey_D.woff2");
}""")
    return "\n".join(lines)


def js():
    """Return the full JS string for diff reports."""
    return """(function() {
  var activeFilters = new Set();
  var cards = document.querySelectorAll('.diff-card');
  var buttons = document.querySelectorAll('.filter-btn');
  var summaryRows = document.querySelectorAll('table.summary tr[data-cat]');
  var bookHeaders = document.querySelectorAll('.book-header');
  var catLabels = {};
  summaryRows.forEach(function(r) {
    var cat = r.getAttribute('data-cat');
    var td = r.querySelectorAll('td')[1];
    if (cat && td) catLabels[cat] = td.textContent;
  });
  function filterSuffix() {
    if (activeFilters.size === 0) return '';
    if (activeFilters.size === 1) {
      var cat = activeFilters.values().next().value;
      var label = catLabels[cat] || cat;
      return ' diffs are of type \u201c' + label + '\u201d';
    }
    return ' diffs are of the selected categories';
  }
  function update() {
    var suffix = filterSuffix();
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
          span.textContent = visCount + ' of ' + total + suffix;
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


def _copy_woff2(out_dir):
    """Copy Taamey_D.woff2 into out_dir/woff2/ from a sibling docs folder."""
    woff2_dir = os.path.join(out_dir, "woff2")
    dst = os.path.join(woff2_dir, "Taamey_D.woff2")
    # Source: sibling "misc" folder's copy (same docs tree)
    src = os.path.join(out_dir, "..", "misc", "woff2", "Taamey_D.woff2")
    src = os.path.normpath(src)
    if not os.path.isfile(src):
        return  # font not available in this tree
    if os.path.isfile(dst) and os.path.getsize(dst) == os.path.getsize(src):
        return  # already up to date
    os.makedirs(woff2_dir, exist_ok=True)
    shutil.copy2(src, dst)


def write_shared_assets(out_dir):
    """Write style.css, filter.js, and woff2 font into out_dir."""
    css_path = os.path.join(out_dir, "style.css")
    js_path = os.path.join(out_dir, "filter.js")
    css_content = css()
    js_content = js()
    for path, content in ((css_path, css_content), (js_path, js_content)):
        existing = None
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = f.read()
        if existing != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
    _copy_woff2(out_dir)
