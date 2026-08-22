"""
Generate an interactive HTML editor for adding/editing line-break
markers in flat-stream JSON files.

Reads a flat-stream JSON from line-breaks/<page>.json,
produces a self-contained HTML file with:
  - Left panel: clickable ground-truth words (RTL) with existing
    line-break markers shown
  - Right panel: Aleppo Codex page image (from aleppo-pages/)

Click the last word of each line to toggle line-end markers.
"Export" downloads the updated flat-stream JSON (with line-start/line-end
markers inserted) as <page_id>.json via the browser's download mechanism.
Move the downloaded file into line-breaks/ to replace the original.

Supports 2-column (poetic) and 3-column (prose) layouts. Use the
col toggle button to cycle between columns (1 → 2 → 3 → 1).

Usage:
    python py_ac_loc/gen_line_break_editor.py 270v 1   # column 1 (right)
    python py_ac_loc/gen_line_break_editor.py 270v 2   # column 2 (left)
    python py_ac_loc/gen_line_break_editor.py 001r 1   # 3-col prose page
"""

import json
import sys

import ac_paths

LB_DIR = ac_paths.line_breaks_dir()
CC_DIR = ac_paths.col_coords_dir()
OUT_DIR = ac_paths.novc_dir()


def _image_relpath(page_id):
    """Return relative path to the local page image (from .novc/)."""
    return f"../aleppo-pages/{page_id}.jpg"


def load_stream(page_id):
    """Load the flat-stream JSON for a page."""
    path = LB_DIR / f"{page_id}.json"
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_words_and_markers(stream):
    """Extract word list and pre-existing line-end indices from a flat stream.

    Args:
        stream: flat stream list (strings and marker dicts) as loaded
            from a line-break JSON file.

    Returns:
        words: list of dicts describing each word/parashah token.
        line_ends: list of (word_index, col, line_num) for existing
            line-end markers.
        page_start_idx: word index of the first word on the page (from
            line-start col 1 line-num 1), or None if not yet set.
        blank_lines: dict mapping word_index to blank-line count for
            pre-existing blank-line markers.
    """
    words = []
    line_ends = []
    blank_lines = {}
    page_start_idx = None
    current_verse = None
    word_idx = 0
    last_line_end_word_idx = None

    for item in stream:
        if isinstance(item, str):
            is_first = current_verse is not None and (
                len(words) == 0
                or words[-1].get("verse_label") != current_verse
                or words[-1].get("is_parashah")
            )
            words.append(
                {
                    "text": item,
                    "is_verse_start": is_first,
                    "verse_label": current_verse,
                    "is_parashah": False,
                }
            )
            word_idx += 1
        elif isinstance(item, dict):
            if "verse-start" in item:
                current_verse = item["verse-start"]
            elif "verse-fragment-start" in item:
                current_verse = item["verse-fragment-start"]
            elif "verse-end" in item:
                pass
            elif "verse-fragment-end" in item:
                pass
            elif "parashah" in item:
                words.append(
                    {
                        "text": item["parashah"],
                        "is_verse_start": False,
                        "verse_label": current_verse,
                        "is_parashah": True,
                        "parashah_value": item["parashah"],
                    }
                )
                word_idx += 1
            elif "line-start" in item:
                ls = item["line-start"]
                col_val = ls["col"]
                is_col1 = col_val == 1 or (
                    isinstance(col_val, str) and col_val.startswith("1of")
                )
                if is_col1 and ls["line-num"] == 1:
                    page_start_idx = word_idx
            elif "line-end" in item:
                if word_idx > 0:
                    last_line_end_word_idx = word_idx - 1
                    line_ends.append(
                        (
                            last_line_end_word_idx,
                            item["line-end"]["col"],
                            item["line-end"]["line-num"],
                        )
                    )
            elif "blank-line" in item:
                if last_line_end_word_idx is not None:
                    blank_lines[last_line_end_word_idx] = (
                        blank_lines.get(last_line_end_word_idx, 0) + 1
                    )
            # page-start, page-end: skip

    return words, line_ends, page_start_idx, blank_lines


def _parse_col_spec(col_spec):
    """Parse a NofM column spec like '1of2' into (n, m) ints."""
    parts = col_spec.split("of")
    return int(parts[0]), int(parts[1])


# CSS crop values keyed by NofM col spec.
# Each entry: (wide_css, skinny_css).
# "Skinny" shows approx 30% of the page centered on the column;
# "wide" shows approx 60% including some neighboring area.
#
# TODO: Some pages have asymmetric 2-column layouts (one column approx
# 2/3 width, the other 1/3). These may need additional col specs like
# "1of2w" / "2of2w" to distinguish wide/narrow columns. See GitHub issue.
_COL_CSS = {
    # 1-column layout
    "1of1": (
        "width: 100%; max-width: none; margin-left: 0;",
        "width: 100%; max-width: none; margin-left: 0;",
    ),
    # 2-column (poetic) layout
    "1of2": (
        "width: 166%; max-width: none; margin-left: -66%;",
        "width: 333%; max-width: none; margin-left: -167%;",
    ),
    "2of2": (
        "width: 166%; max-width: none; margin-left: 0;",
        "width: 333%; max-width: none; margin-left: 0;",
    ),
    # 3-column (prose) layout
    "1of3": (
        "width: 166%; max-width: none; margin-left: -66%;",
        "width: 333%; max-width: none; margin-left: -167%;",
    ),
    "2of3": (
        "width: 142%; max-width: none; margin-left: -28%;",
        "width: 250%; max-width: none; margin-left: -62%;",
    ),
    "3of3": (
        "width: 166%; max-width: none; margin-left: 0;",
        "width: 333%; max-width: none; margin-left: 0;",
    ),
}

# Display labels for each col spec
_COL_LABELS = {
    "1of1": "1of1",
    "1of2": "1of2 (right)",
    "2of2": "2of2 (left)",
    "1of3": "1of3 (right)",
    "2of3": "2of3 (center)",
    "3of3": "3of3 (left)",
}


def _col_cycle(col_spec):
    """Return the next col spec in the toggle cycle."""
    n, m = _parse_col_spec(col_spec)
    next_n = (n % m) + 1
    return f"{next_n}of{m}"


def generate_editor_html(page_id, col_spec):
    """Generate the HTML editor file for a page, cropped to a column.

    Args:
        page_id: leaf identifier, e.g. "270r" or "001r".
        col_spec: NofM column spec, e.g. "1of2" or "2of3".
    """
    stream = load_stream(page_id)
    words, line_ends, page_start_idx, blank_lines = _extract_words_and_markers(stream)
    image_url = _image_relpath(page_id)

    n, m = _parse_col_spec(col_spec)

    # Build CSS lookup for all columns in this layout
    all_col_specs = [f"{i}of{m}" for i in range(1, m + 1)]
    css_json_entries = []
    for cs in all_col_specs:
        wide, skinny = _COL_CSS[cs]
        css_json_entries.append(f'    "{cs}": {{ wide: "{wide}", skinny: "{skinny}" }}')
    css_json = "{\n" + ",\n".join(css_json_entries) + "\n  }"

    # Build JS data
    js_words = []
    for w in words:
        entry = {
            "text": w["text"],
            "isVerseStart": w["is_verse_start"],
            "verseLabel": w["verse_label"] or "",
            "isParashah": w["is_parashah"],
        }
        js_words.append(entry)

    # Pre-existing line-end word indices with col/line info
    js_line_ends = []
    for widx, col_val, lnum in line_ends:
        js_line_ends.append({"idx": widx, "col": col_val, "lineNum": lnum})

    # Build the stream without line/blank-line markers for export reconstruction
    stream_no_lines = [
        item
        for item in stream
        if not (
            isinstance(item, dict)
            and ("line-start" in item or "line-end" in item or "blank-line" in item)
        )
    ]

    words_json = json.dumps(js_words, ensure_ascii=False, indent=None)
    line_ends_json = json.dumps(js_line_ends, ensure_ascii=False)
    blank_lines_json = json.dumps(blank_lines, ensure_ascii=False)
    stream_json = json.dumps(stream_no_lines, ensure_ascii=False, indent=2)
    page_start_js = "null" if page_start_idx is None else str(page_start_idx)

    # Build JS labels and cycle maps for all cols in this layout
    labels_json_entries = [f'"{cs}": "{_COL_LABELS[cs]}"' for cs in all_col_specs]
    labels_json = "{" + ", ".join(labels_json_entries) + "}"
    cycle_json_entries = [f'"{cs}": "{_col_cycle(cs)}"' for cs in all_col_specs]
    cycle_json = "{" + ", ".join(cycle_json_entries) + "}"

    _, skinny = _COL_CSS[col_spec]

    # Load quad data for image-side sync (gracefully missing)
    cc_path = CC_DIR / f"{page_id}.json"
    if cc_path.exists():
        quad_json = cc_path.read_text(encoding="utf-8").strip()
    else:
        quad_json = "null"

    html = _HTML_TEMPLATE.format(
        page_id=page_id,
        image_url=image_url,
        img_css=skinny,
        css_json=css_json,
        col_label=_COL_LABELS[col_spec],
        col_spec=col_spec,
        next_col=_col_cycle(col_spec),
        labels_json=labels_json,
        cycle_json=cycle_json,
        ncols=m,
        words_json=words_json,
        line_ends_json=line_ends_json,
        blank_lines_json=blank_lines_json,
        stream_json=stream_json,
        page_start_idx_js=page_start_js,
        quad_json=quad_json,
    )

    out_path = OUT_DIR / f"lb_editor_{page_id}_{col_spec}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8", newline="")
    print(f"Wrote {out_path}")
    return out_path


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Line Break Editor — {page_id}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Segoe UI', sans-serif; background: #1e1e1e; color: #d4d4d4; }}
h1 {{ text-align: center; padding: 10px; font-size: 17px; background: #252526; border-bottom: 1px solid #444; direction: ltr; }}
h1 button {{
    padding: 4px 12px; margin: 0 4px; cursor: pointer;
    background: #0e639c; color: #fff; border: none; border-radius: 4px;
    font-size: 13px; vertical-align: middle;
}}
h1 button:hover {{ background: #1177bb; }}
#status {{
    display: inline-block; margin-left: 12px;
    font-size: 13px; color: #888;
}}
.container {{ display: flex; height: calc(100vh - 45px); }}
.col-words {{
    overflow-y: auto; padding: 16px; direction: rtl;
    font-size: 22px;
    font-family: 'SBL Hebrew', 'Ezra SIL', 'Times New Roman', serif;
}}
.divider {{
    width: 6px;
    cursor: col-resize;
    background: transparent;
    transition: background 0.15s;
    flex-shrink: 0;
}}
.divider:hover, .divider.active {{
    background: #0e639c;
}}
.col-image {{
    overflow-x: hidden; overflow-y: auto;
    padding: 8px; direction: ltr;
}}
.col-image img {{ {img_css} cursor: crosshair; transition: width 0.2s, margin-left 0.2s; }}
.word {{
    display: inline-block;
    padding: 3px 5px;
    margin: 1px;
    cursor: pointer;
    border-radius: 3px;
    border: 1px solid transparent;
    user-select: none;
    transition: background 0.12s;
    line-height: 1.8;
}}
.word:hover {{ background: #333; }}
.word.line-end {{
    background: #264f2a;
    border-color: #4ec94e;
    border-left: 3px solid #4ec94e;
}}
.word.parashah {{
    color: #e07040;
    font-size: 16px;
    font-family: monospace;
    cursor: pointer;
}}
.word.lead-in {{
    opacity: 0.35;
    cursor: default;
}}
.word.page-start {{
    background: #3a2a5f;
    border-color: #9a7adf;
    border-right: 3px solid #9a7adf;
}}
.page-start-label {{
    display: inline-block;
    color: #9a7adf;
    font-size: 11px;
    font-family: monospace;
    direction: ltr;
    margin-left: 4px;
}}
.word.verse-start {{
    border-bottom: 2px solid #5a5a8a;
}}
.word.maqaf-end {{
    margin-left: 0; padding-left: 0;
}}
.word.after-maqaf {{
    margin-right: 0; padding-right: 0;
}}
.line-num {{
    display: inline-block;
    color: #888;
    font-size: 12px;
    font-family: monospace;
    min-width: 40px;
    text-align: center;
    direction: ltr;
    margin-left: 4px;
}}
.col-label {{
    display: inline-block;
    color: #cc0;
    font-size: 11px;
    font-family: monospace;
    direction: ltr;
    margin-left: 2px;
    vertical-align: super;
}}
.line-num {{
    cursor: pointer;
}}
.line-num:hover {{
    color: #e0e040;
    text-decoration: underline;
}}
.blank-line {{
    display: block;
    height: 20px;
    border: 1px dashed #666;
    border-radius: 3px;
    margin: 2px 0;
    background: #2a2a2a;
    cursor: pointer;
    text-align: center;
    color: #666;
    font-size: 11px;
    font-family: monospace;
    direction: ltr;
    line-height: 20px;
}}
.blank-line:hover {{
    border-color: #c44;
    color: #c44;
    background: #3a2020;
}}
#syncIndicator {{
    display: inline-block;
    margin-left: 8px;
    font-size: 12px;
    font-family: monospace;
    padding: 2px 8px;
    border-radius: 3px;
    vertical-align: middle;
}}
#syncIndicator.on {{
    background: #264f2a;
    color: #4ec94e;
}}
#syncIndicator.off {{
    background: #3a2a2a;
    color: #666;
}}
.sync-fade-top, .sync-fade-bottom {{
    position: absolute;
    pointer-events: none;
    z-index: 10;
    display: none;
    left: 0;
    right: 0;
}}

</style>
</head>
<body>

<h1>Line Break Editor — {page_id} — <span id="colLabel">{col_label}</span>
    <button onclick="exportJSON()">Export</button>
    <button id="colBtn" onclick="toggleCol()">Go to <span id="colBtnNum">{next_col}</span></button>
    <button id="skinnyBtn" onclick="toggleSkinnyMode()">Go wide</button>
    <span id="syncIndicator" class="on">sync: ON [s]</span>
    <span id="status"></span>
</h1>
<div class="container" id="container">
    <div class="col-words" id="wordsPanel"></div>
    <div class="divider" id="divider"></div>
    <div class="col-image" id="imagePanel" style="position:relative">
        <div id="fadeTop" class="sync-fade-top"></div>
        <div id="fadeBottom" class="sync-fade-bottom"></div>
        <img src="{image_url}" alt="Aleppo Codex {page_id}">
    </div>
</div>

<script>
const PAGE_ID = "{page_id}";
const NCOLS = {ncols};
const MAQAF = '\־';
// Image crop CSS keyed by NofM col spec
const IMG_CSS = {css_json};
let isSkinnyMode = true; // skinny is default
const LINES_PER_COL = 28;
const quadData = {quad_json};
const allWords = {words_json};
const preExistingLineEnds = {line_ends_json};
const preExistingBlankLines = {blank_lines_json};
const baseStream = {stream_json};

// State: Map<wordIdx, {{col, lineNum}}> where col is a NofM string
let lineEndMap = new Map();

// Blank lines after a given line-end word index.
// Map<wordIdx, count> — how many blank lines follow this line-end.
let blankLinesAfter = new Map();

let syncMode = true;

// Page-start: index of the first word actually on this page.
// Words before this are lead-in from the previous page.
// null means not set (or page starts at word 0).
let pageStartIdx = {page_start_idx_js};

// Initialize from pre-existing line ends
preExistingLineEnds.forEach(le => {{
    lineEndMap.set(le.idx, {{col: le.col, lineNum: le.lineNum}});
}});

// Initialize from pre-existing blank lines
for (const [k, v] of Object.entries(preExistingBlankLines)) {{
    blankLinesAfter.set(parseInt(k), v);
}}

const PARASHAH_DISPLAY = {{
    'spi-pe2': '{{פפ}}',
    'spi-pe1': '{{פ}}',
    'spi-sm1': '{{ס}}',
    'spi-samekh2': '{{סס}}',
}};

const COL_LABELS = {labels_json};
const COL_CYCLE = {cycle_json};

let currentColSpec = "{col_spec}";
function currentCol() {{
    return currentColSpec;
}}

function toggleCol() {{
    currentColSpec = COL_CYCLE[currentColSpec];
    applyImageCrop();
    document.getElementById('colLabel').textContent = COL_LABELS[currentColSpec];
    document.getElementById('colBtnNum').textContent = COL_CYCLE[currentColSpec];
    if (syncMode) {{
        applySyncScroll();
    }}
}}

function toggleSyncMode() {{
    syncMode = !syncMode;
    const ind = document.getElementById('syncIndicator');
    ind.className = syncMode ? 'on' : 'off';
    ind.textContent = syncMode ? 'sync: ON [s]' : 'sync: off [s]';
    if (syncMode) {{
        applySyncScroll();
    }} else {{
        // Hide fade overlays when sync is off
        document.getElementById('fadeTop').style.display = 'none';
        document.getElementById('fadeBottom').style.display = 'none';
    }}
}}

// --- Image-side sync (quad-based fade overlays) ---

function getColQuad(colSpec) {{
    if (!quadData) return null;
    const colNum = colSpec.split('of')[0];
    const colKey = 'col' + colNum;
    const col = quadData.columns[colKey];
    return col ? col.rel : null;
}}

function getLineYRange(colSpec, lineNum) {{
    const q = getColQuad(colSpec);
    if (!q) return null;
    const topY = (q.tl[1] + q.tr[1]) / 2;
    const botY = (q.bl[1] + q.br[1]) / 2;
    // Weighted line heights: top=1.5x, bottom=1.25x, middle=1x
    const TOP_W = 1.5, BOT_W = 1.25;
    const MID = LINES_PER_COL - 2;
    const total = TOP_W + MID + BOT_W;
    // Compute cumulative t for dividers
    const dividers = [0];
    for (let i = 0; i < LINES_PER_COL; i++) {{
        const w = i === 0 ? TOP_W : i === LINES_PER_COL - 1 ? BOT_W : 1;
        dividers.push(dividers[i] + w / total);
    }}
    const t0 = dividers[lineNum - 1];
    const t1 = dividers[lineNum];
    const colH = botY - topY;
    const y0 = topY + t0 * colH;
    const y1 = topY + t1 * colH;
    const lineH = y1 - y0;
    return {{ y0, y1, topY, botY, lineH }};
}}

function getNextLineNum(col) {{
    const colEnds = [...lineEndMap.values()].filter(v => v.col === col);
    if (colEnds.length === 0) return 1;
    const maxLine = Math.max(...colEnds.map(v => v.lineNum));
    const lastEndIdx = [...lineEndMap.entries()]
        .filter(([_, v]) => v.col === col && v.lineNum === maxLine)
        .map(([k, _]) => k)[0];
    const blanksAfterLast = blankLinesAfter.get(lastEndIdx) || 0;
    return maxLine + blanksAfterLast + 1;
}}

function applySyncScroll() {{
    if (!syncMode) return;
    const col = currentColSpec;
    const nextLine = getNextLineNum(col);
    const fadeTop = document.getElementById('fadeTop');
    const fadeBot = document.getElementById('fadeBottom');
    const yr = getLineYRange(col, Math.min(nextLine, LINES_PER_COL));

    // If no quad data or column done, hide fades but still sync words panel
    if (!yr || nextLine > LINES_PER_COL) {{
        fadeTop.style.display = 'none';
        fadeBot.style.display = 'none';
        syncWordsPanel();
        return;
    }}

    const img = document.querySelector('#imagePanel img');
    const panel = document.getElementById('imagePanel');

    requestAnimationFrame(() => {{
        const imgRect = img.getBoundingClientRect();
        const panelRect = panel.getBoundingClientRect();
        const imgNatH = img.naturalHeight || 1966;
        const imgNatW = img.naturalWidth || 1654;
        const imgAR = imgNatH / imgNatW;

        const imgDispW = imgRect.width;
        const imgDispH = imgDispW * imgAR;

        // Clear zone: line +/- 0.25 line-height buffer
        const buf = yr.lineH * 0.25;
        const clearTop = (yr.y0 - buf) * imgDispH;
        const clearBot = (yr.y1 + buf) * imgDispH;
        const lineHpx = yr.lineH * imgDispH;

        const imgTopInPanel = imgRect.top - panelRect.top + panel.scrollTop;

        const dk = 'rgba(0,0,0,0.6)';
        const makeGrad = (dir, totalH) => {{
            if (totalH <= 0) return dk;
            const s = Math.min(lineHpx, totalH);
            const p = (frac) => {{
                const alpha = Math.pow(frac, 0.6) * 0.6;
                return `rgba(0,0,0,${{alpha.toFixed(3)}})`;
            }};
            const pcts = [
                `${{dk}} 0px`,
                `${{dk}} ${{Math.max(0, totalH - s).toFixed(1)}}px`,
                `${{p(0.75)}} ${{(totalH - s * 0.25).toFixed(1)}}px`,
                `${{p(0.5)}} ${{(totalH - s * 0.5).toFixed(1)}}px`,
                `rgba(0,0,0,0) ${{totalH.toFixed(1)}}px`,
            ];
            return `linear-gradient(${{dir}}, ${{pcts.join(', ')}})`;
        }};

        const topH = Math.max(0, clearTop);
        fadeTop.style.display = 'block';
        fadeTop.style.top = imgTopInPanel + 'px';
        fadeTop.style.height = topH + 'px';
        fadeTop.style.background = makeGrad('to bottom', topH);

        const botH = Math.max(0, imgDispH - clearBot);
        fadeBot.style.display = 'block';
        fadeBot.style.top = (imgTopInPanel + clearBot) + 'px';
        fadeBot.style.height = botH + 'px';
        fadeBot.style.background = makeGrad('to top', botH);

        // Scroll panel to center the clear zone
        const clearMid = imgTopInPanel + (clearTop + clearBot) / 2;
        const panelH = panelRect.height;
        const targetScroll = clearMid - panelH / 2;
        panel.scrollTop = Math.max(0, targetScroll);

        syncWordsPanel();
    }});
}}

function syncWordsPanel() {{
    if (!syncMode) return;
    const col = currentColSpec;
    const sorted = [...lineEndMap.entries()]
        .filter(([_, v]) => v.col === col)
        .sort((a, b) => a[0] - b[0]);
    let targetIdx;
    if (sorted.length === 0) {{
        const curN = parseInt(col.split('of')[0]);
        if (curN > 1) {{
            const prevEnds = [...lineEndMap.entries()]
                .filter(([_, v]) => {{
                    const vn = parseInt(v.col.split('of')[0]);
                    return vn < curN;
                }})
                .sort((a, b) => a[0] - b[0]);
            if (prevEnds.length > 0) {{
                targetIdx = prevEnds[prevEnds.length - 1][0] + 1;
            }} else {{
                targetIdx = pageStartIdx !== null ? pageStartIdx : 0;
            }}
        }} else {{
            targetIdx = pageStartIdx !== null ? pageStartIdx : 0;
        }}
    }} else {{
        const lastEndIdx = sorted[sorted.length - 1][0];
        targetIdx = lastEndIdx + 1;
    }}
    const el = document.querySelector(`.word[data-idx="${{targetIdx}}"]`);
    if (!el) return;
    const wp = document.getElementById('wordsPanel');
    const elRect = el.getBoundingClientRect();
    const wpRect = wp.getBoundingClientRect();
    const elTopInWp = elRect.top - wpRect.top + wp.scrollTop;
    wp.scrollTop = elTopInWp - wp.clientHeight / 2;
}}

function recalcLineNums() {{
    // Flat-order assignment: sort all line-ends by word index,
    // assign first LINES_PER_COL to col 1, next to col 2, etc.
    const sorted = [...lineEndMap.entries()].sort((a, b) => a[0] - b[0]);
    let flatLine = 1;
    sorted.forEach(([idx, _]) => {{
        const colIdx = Math.min(Math.floor((flatLine - 1) / LINES_PER_COL), NCOLS - 1);
        const colN = colIdx + 1;
        const colSpec = colN + 'of' + NCOLS;
        const lineNum = flatLine - colIdx * LINES_PER_COL;
        const entry = lineEndMap.get(idx);
        entry.col = colSpec;
        entry.lineNum = lineNum;
        flatLine++;
        // Account for blank lines after this line-end
        const blanks = blankLinesAfter.get(idx) || 0;
        flatLine += blanks;
    }});
}}

function addBlankLine(wordIdx) {{
    const count = blankLinesAfter.get(wordIdx) || 0;
    blankLinesAfter.set(wordIdx, count + 1);
    recalcLineNums();
    render();
    applySyncScroll();
}}

function removeBlankLine(wordIdx) {{
    const count = blankLinesAfter.get(wordIdx) || 0;
    if (count <= 1) {{
        blankLinesAfter.delete(wordIdx);
    }} else {{
        blankLinesAfter.set(wordIdx, count - 1);
    }}
    recalcLineNums();
    render();
    applySyncScroll();
}}

function render() {{
    const panel = document.getElementById('wordsPanel');
    panel.innerHTML = '';

    const isLeadIn = (idx) => pageStartIdx !== null && idx < pageStartIdx;

    allWords.forEach((entry, idx) => {{
        const span = document.createElement('span');
        span.className = 'word';
        span.textContent = entry.isParashah
            ? (PARASHAH_DISPLAY[entry.text] || entry.text)
            : entry.text;
        span.dataset.idx = idx;

        const endsMaqaf = entry.text.endsWith(MAQAF);
        const prevEndsMaqaf = idx > 0 && allWords[idx - 1].text.endsWith(MAQAF);
        if (endsMaqaf) span.classList.add('maqaf-end');
        if (prevEndsMaqaf) span.classList.add('after-maqaf');

        if (isLeadIn(idx)) {{
            span.classList.add('lead-in');
        }} else if (entry.isParashah) {{
            span.classList.add('parashah');
            span.addEventListener('click', () => toggleLineEnd(idx));
        }} else {{
            if (entry.isVerseStart) {{
                span.classList.add('verse-start');
                span.title = entry.verseLabel;
            }}
            span.addEventListener('click', () => toggleLineEnd(idx));
        }}

        // Page-start marker
        if (pageStartIdx === idx) {{
            span.classList.add('page-start');
        }}

        // Right-click to set/clear page-start
        span.addEventListener('contextmenu', (e) => {{
            e.preventDefault();
            togglePageStart(idx);
        }});

        const leInfo = lineEndMap.get(idx);
        if (leInfo && !isLeadIn(idx)) {{
            span.classList.add('line-end');
            span.title = `Col ${{leInfo.col}}, Line ${{leInfo.lineNum}}`;
        }}

        panel.appendChild(span);

        // Page-start label
        if (pageStartIdx === idx) {{
            const lbl = document.createElement('span');
            lbl.className = 'page-start-label';
            lbl.textContent = '◀ page start';
            panel.appendChild(lbl);
        }}

        if (leInfo && !isLeadIn(idx)) {{
            const colLbl = document.createElement('span');
            colLbl.className = 'col-label';
            colLbl.textContent = leInfo.col;

            const ln = document.createElement('span');
            ln.className = 'line-num';
            ln.textContent = leInfo.lineNum;
            ln.title = 'Click to add blank line after this line';
            ln.addEventListener('click', () => addBlankLine(idx));

            panel.appendChild(colLbl);
            panel.appendChild(ln);
            panel.appendChild(document.createElement('br'));

            // Render blank-line placeholders after this line-end
            const blanks = blankLinesAfter.get(idx) || 0;
            for (let b = 0; b < blanks; b++) {{
                const blankDiv = document.createElement('div');
                blankDiv.className = 'blank-line';
                const blankLineNum = leInfo.lineNum + 1 + b;
                blankDiv.textContent = `— blank line ${{blankLineNum}} (${{leInfo.col}}) — click to remove`;
                blankDiv.addEventListener('click', () => {{
                    removeBlankLine(idx);
                }});
                panel.appendChild(blankDiv);
            }}
        }}
    }});

    updateStatus();
}}

function toggleLineEnd(idx) {{
    if (lineEndMap.has(idx)) {{
        blankLinesAfter.delete(idx);
        lineEndMap.delete(idx);
    }} else {{
        // Col and lineNum will be assigned by recalcLineNums
        lineEndMap.set(idx, {{col: '', lineNum: 0}});
    }}
    recalcLineNums();
    render();

    // Auto-switch when current column fills up
    const curN = parseInt(currentColSpec.split('of')[0]);
    if (curN < NCOLS) {{
        const curColSpec = currentColSpec;
        const colEnds = [...lineEndMap.values()].filter(v => v.col === curColSpec);
        const colBlanks = [...lineEndMap.entries()]
            .filter(([_, v]) => v.col === curColSpec)
            .reduce((sum, [k, _]) => sum + (blankLinesAfter.get(k) || 0), 0);
        if (colEnds.length + colBlanks >= LINES_PER_COL) {{
            toggleCol();
            return;
        }}
    }}
    applySyncScroll();
}}

function togglePageStart(idx) {{
    if (pageStartIdx === idx) {{
        pageStartIdx = null;  // clear it
    }} else {{
        pageStartIdx = idx;
        // Remove any line-end markers on lead-in words
        for (const [k, _] of lineEndMap) {{
            if (k < idx) lineEndMap.delete(k);
        }}
        recalcLineNums();
    }}
    render();
}}

function updateStatus() {{
    const counts = {{}};
    lineEndMap.forEach(info => {{
        counts[info.col] = (counts[info.col] || 0) + 1;
    }});
    const parts = Object.entries(counts)
        .sort()
        .map(([c, n]) => `${{c}}: ${{n}} lines`);
    const totalBlanks = [...blankLinesAfter.values()].reduce((a, b) => a + b, 0);
    const blankInfo = totalBlanks > 0 ? ` | ${{totalBlanks}} blank` : '';
    const psInfo = pageStartIdx !== null ? `Page start: word ${{pageStartIdx}}` : 'No page start set';
    document.getElementById('status').textContent =
        psInfo + (parts.length ? ' | ' + parts.join(' | ') : '') + blankInfo;
}}

function buildExportStream() {{
    // Rebuild the stream: take baseStream and insert line-start/line-end
    // around the words according to lineEndMap.
    const sorted = [...lineEndMap.entries()].sort((a, b) => a[0] - b[0]);
    const endSet = new Map();
    sorted.forEach(([idx, info]) => endSet.set(idx, info));

    // Compute line-start indices for each column
    const byCols = {{}};
    sorted.forEach(([idx, info]) => {{
        if (!byCols[info.col]) byCols[info.col] = [];
        byCols[info.col].push(idx);
    }});

    const startSet = new Map(); // wordIdx -> {{col, lineNum}}
    for (const col in byCols) {{
        const ends = byCols[col];
        for (let i = 0; i < ends.length; i++) {{
            let startIdx;
            if (i === 0) {{
                if (col === '1of' + NCOLS && pageStartIdx !== null) {{
                    // Col 1 line 1 starts at the page-start word
                    startIdx = pageStartIdx;
                }} else {{
                    // First line of this col: after the last line-end
                    // from another col that comes before this col's first end
                    const allEndsBefore = sorted.filter(([eidx, _]) => eidx < ends[i]);
                    if (allEndsBefore.length > 0) {{
                        startIdx = allEndsBefore[allEndsBefore.length - 1][0] + 1;
                    }} else {{
                        startIdx = pageStartIdx !== null ? pageStartIdx : 0;
                    }}
                }}
            }} else {{
                startIdx = ends[i - 1] + 1;
            }}
            const lineNum = lineEndMap.get(ends[i]).lineNum;
            startSet.set(startIdx, {{col: col, lineNum: lineNum}});
        }}
    }}

    const result = [];
    let wordIdx = 0;

    for (const item of baseStream) {{
        if (typeof item === 'string' || (typeof item === 'object' && item !== null && 'parashah' in item)) {{
            if (startSet.has(wordIdx)) {{
                const info = startSet.get(wordIdx);
                result.push({{"line-start": {{"col": info.col, "line-num": info.lineNum}}}});
            }}
            result.push(item);
            if (endSet.has(wordIdx)) {{
                const info = endSet.get(wordIdx);
                result.push({{"line-end": {{"col": info.col, "line-num": info.lineNum}}}});
                // Insert blank lines after this line-end
                const blanks = blankLinesAfter.get(wordIdx) || 0;
                for (let b = 0; b < blanks; b++) {{
                    const blankNum = info.lineNum + 1 + b;
                    result.push({{"blank-line": {{"col": info.col, "line-num": blankNum}}}});
                }}
            }}
            wordIdx++;
        }} else {{
            result.push(item);
        }}
    }}

    return trimPageBoundaryContent(result);
}}

function trimPageBoundaryContent(stream) {{
    // Find the first line-start and last line-end indices in the stream.
    let firstLineStart = -1;
    let lastLineEnd = -1;
    for (let i = 0; i < stream.length; i++) {{
        const item = stream[i];
        if (typeof item === 'object' && item !== null) {{
            if ('line-start' in item && firstLineStart === -1) firstLineStart = i;
            if ('line-end' in item) lastLineEnd = i;
        }}
    }}
    if (firstLineStart === -1 || lastLineEnd === -1) return stream;

    // --- Trim pre-content (words before first line-start) ---
    // Check if there are any words before firstLineStart
    let hasPreWords = false;
    for (let i = 0; i < firstLineStart; i++) {{
        if (typeof stream[i] === 'string') {{ hasPreWords = true; break; }}
    }}
    if (hasPreWords) {{
        // Remove words, convert last verse-start before firstLineStart
        // to verse-fragment-start
        const kept = [];
        let lastVsIdx = -1;
        for (let i = 0; i < firstLineStart; i++) {{
            const item = stream[i];
            if (typeof item === 'object' && item !== null && 'verse-start' in item) {{
                lastVsIdx = kept.length;
                kept.push(item);
            }} else if (typeof item === 'string') {{
                // skip pre-content word
            }} else {{
                kept.push(item);
            }}
        }}
        if (lastVsIdx !== -1) {{
            const vs = kept[lastVsIdx]['verse-start'];
            kept[lastVsIdx] = {{'verse-fragment-start': vs}};
        }}
        stream = [...kept, ...stream.slice(firstLineStart)];
    }}

    // --- Trim post-content (words after last line-end) ---
    // Recalculate lastLineEnd after possible pre-content trim
    lastLineEnd = -1;
    for (let i = 0; i < stream.length; i++) {{
        if (typeof stream[i] === 'object' && stream[i] !== null && 'line-end' in stream[i]) {{
            lastLineEnd = i;
        }}
    }}
    let hasPostWords = false;
    for (let i = lastLineEnd + 1; i < stream.length; i++) {{
        if (typeof stream[i] === 'string') {{ hasPostWords = true; break; }}
    }}
    if (hasPostWords) {{
        const kept = [];
        let firstVeIdx = -1;
        for (let i = lastLineEnd + 1; i < stream.length; i++) {{
            const item = stream[i];
            if (typeof item === 'object' && item !== null && 'verse-end' in item) {{
                if (firstVeIdx === -1) firstVeIdx = kept.length;
                kept.push(item);
            }} else if (typeof item === 'string') {{
                // skip post-content word
            }} else {{
                kept.push(item);
            }}
        }}
        if (firstVeIdx !== -1) {{
            const ve = kept[firstVeIdx]['verse-end'];
            kept[firstVeIdx] = {{'verse-fragment-end': ve}};
        }}
        stream = [...stream.slice(0, lastLineEnd + 1), ...kept];
    }}

    return stream;
}}

function applyImageCrop() {{
    const img = document.querySelector('.col-image img');
    const mode = isSkinnyMode ? 'skinny' : 'wide';
    const css = IMG_CSS[currentColSpec][mode];
    img.style.cssText = css + ' cursor: crosshair;';
}}

function toggleSkinnyMode() {{
    isSkinnyMode = !isSkinnyMode;
    applyImageCrop();
    document.getElementById('skinnyBtn').textContent =
        isSkinnyMode ? 'Go wide' : 'Go skinny';
}}

function exportJSON() {{
    const stream = buildExportStream();
    const jsonStr = JSON.stringify(stream, null, 2) + '\\n';
    const blob = new Blob([jsonStr], {{type: 'application/json'}});
    const a = document.createElement('a');
    a.download = 'line-breaks-' + PAGE_ID + '.json';
    a.href = URL.createObjectURL(blob);
    a.click();
    URL.revokeObjectURL(a.href);
    document.getElementById('status').textContent = 'Downloaded line-breaks-' + PAGE_ID + '.json';
    setTimeout(updateStatus, 2000);
}}

render();
applySyncScroll();

// Keyboard shortcut: 's' to toggle sync mode
document.addEventListener('keydown', (e) => {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 's' || e.key === 'S') {{
        e.preventDefault();
        toggleSyncMode();
    }}
}});

// --- Resizable divider ---
(function() {{
    const container = document.getElementById('container');
    const words = document.getElementById('wordsPanel');
    const divider = document.getElementById('divider');
    const image = document.getElementById('imagePanel');
    // Default 45/55
    let wordsPct = 45;
    words.style.flex = '0 0 ' + wordsPct + '%';
    image.style.flex = '1 1 0%';
    let dragging = false;
    divider.addEventListener('mousedown', (e) => {{
        e.preventDefault();
        dragging = true;
        divider.classList.add('active');
    }});
    document.addEventListener('mousemove', (e) => {{
        if (!dragging) return;
        const rect = container.getBoundingClientRect();
        // RTL layout: words panel is on the right, image on the left
        let pct = ((rect.right - e.clientX) / rect.width) * 100;
        pct = Math.max(10, Math.min(pct, 80));
        wordsPct = pct;
        words.style.flex = '0 0 ' + pct + '%';
    }});
    document.addEventListener('mouseup', () => {{
        if (dragging) {{
            dragging = false;
            divider.classList.remove('active');
        }}
    }});
}})();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 3:
        print("Usage: python py_ac_loc/gen_line_break_editor.py <page_id> <col_spec>")
        print("  e.g. python py_ac_loc/gen_line_break_editor.py 270v 1of2")
        print("       python py_ac_loc/gen_line_break_editor.py 001r 1of3")
        print("  NofM format: N=column number, M=total columns on page")
        print("  2-col (poetic): 1of2=right, 2of2=left")
        print("  3-col (prose):  1of3=right, 2of3=center, 3of3=left")
        sys.exit(1)
    page_id = sys.argv[1]
    col_spec = sys.argv[2]
    if "of" not in col_spec:
        print(f"ERROR: col must be NofM format (e.g. 1of2, 2of3), got: {col_spec}")
        sys.exit(1)
    if col_spec not in _COL_CSS:
        print(f"ERROR: unknown col spec '{col_spec}' (known: {list(_COL_CSS)})")
        sys.exit(1)
    out_path = generate_editor_html(page_id, col_spec)
    import webbrowser

    webbrowser.open(str(out_path))


if __name__ == "__main__":
    main()
