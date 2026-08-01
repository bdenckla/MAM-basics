"""Build-time authoring tool: pick word-highlight rectangles on a committed scan.

Emits a self-contained, dependency-free HTML+JS page that shows one of the
gh-pages scans with a draggable, multi-rectangle SVG overlay, then opens it in
the browser (``--no-open`` prints the URL and launches nothing, for handing the
picker to someone who will open it themselves). The <img> uses a relative path, so the page works as a plain
``file://`` URL with no server (the default); pass ``--serve`` to run a local
HTTP server instead. Drag one box per word you want highlighted; export the boxes
as JSON (and/or copy a ready-to-paste ``mhi.Box(...)`` snippet), then paste the
``px`` boxes into the page generator (e.g. ``_P83_BOXES`` in
``printed_decalogue_simanim_page.py``).

This tool NEVER ships to gh-pages and is not referenced by any generated page; it
exists only so highlight coordinates are measured, not eyeballed. The overlay
geometry is normalized 0-1 (viewBox="0 0 1 1"), so it is resolution-independent;
the exported ``px`` form is those coordinates multiplied by the scan's own
naturalWidth/naturalHeight (read in the browser -- so no Pillow dependency), which
maps 1:1 onto the scan-pixel-space overlay used at render time and onto
``mhi.Box(x, y, w, h)``.

Run via ``main_edition_transcription.py highlight-picker`` (from the repo root; PowerShell):
    .venv\\Scripts\\python.exe py\\main_edition_transcription.py highlight-picker \\
        Simanim-Tiqqun-p-083-Ex-Dec-elyon.png
The .png suffix is optional. The image is resolved under gh-pages/accgram/img/.
Add --serve to run a local http server (then Ctrl+C to stop it) instead of the
default file:// open. Add --no-open to print the URL without launching anything.
This module is not independently runnable, and had its own hand-rolled ``sys.argv``
scanning and ``main()`` until 2026-08-01 -- the last of the six such modules
``doc/PLAN-sys-path-insert.md`` retired, which escaped that pass only because it never
had a ``sys.path`` prelude to find it by.

Priming (start from existing boxes instead of blank): pass ``--boxes-file <path>``,
a JSON file holding either a bare list of px boxes ``[{"x":..,"y":..,"w":..,"h":..}]``
(the same px form stored as ``mhi.Box`` in the page generators) or a whole prior
``highlight-boxes-*.json`` export from this tool. The seed boxes appear on load, ready
to nudge; export as usual when done. Without it, the editor opens blank as before.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import socket
import sys
import threading
import webbrowser
from pathlib import Path

import wlc_paths

# Off wlc_paths like every other module here, never the cwd.  This file computed its own
# ``Path(__file__).resolve().parents[2]`` until 2026-08-01 -- the one module in the tree that
# bypassed wlc_paths entirely, so a change to how the repo locates itself would have missed it.
_IMG_DIR = wlc_paths.gh_pages_dir() / "accgram" / "img"
_OUT_DIR = wlc_paths.novc_dir()


def serve_and_open(directory: Path, rel_url: str, *, open_browser: bool = True) -> None:
    """Start an HTTP server rooted at *directory*, open *rel_url*, block on Ctrl+C.

    With ``open_browser=False`` (``--no-open``) the URL is printed and nothing is
    launched -- see ``generate``.
    """
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(directory)
    )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = http.server.HTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{port}/{rel_url}"
    print(f"Serving at http://127.0.0.1:{port}/ -- opening {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    try:
        thread.join()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.shutdown()


def _resolve_img(arg: str) -> str:
    """Return the validated scan filename (adds a .png suffix if omitted)."""
    name = arg if arg.lower().endswith(".png") else arg + ".png"
    img_path = _IMG_DIR / name
    if not img_path.exists():
        print(f"Error: image not found: {img_path}")
        available = sorted(p.name for p in _IMG_DIR.glob("*.png"))
        if available:
            print("Available scans:")
            for a in available:
                print(f"  {a}")
        sys.exit(1)
    return name


def _px_boxes_from_arg(data: object) -> list[dict]:
    """Normalize a --boxes-file payload to a list of ``{x, y, w, h}`` px dicts.

    Accepts either a bare list of px boxes (``[{"x":..,"y":..,"w":..,"h":..}, ...]``)
    or a whole prior export from this tool (``{"boxes": [{"px": {...}, "rel": {...}}]}``),
    so a saved ``highlight-boxes-*.json`` can be re-opened and tweaked rather than
    re-dragged. Missing/extra keys are the caller's problem; we only pluck ``px``.
    """
    if isinstance(data, dict) and "boxes" in data:
        return [b["px"] for b in data["boxes"]]
    assert isinstance(data, list), "boxes payload must be a list or an export dict"
    return data


def _build_html(img_name: str, init_boxes_px: list[dict] | None = None) -> str:
    """Return the self-contained picker HTML for the given scan.

    The <img> uses a RELATIVE path (../gh-pages/accgram/img/<name>) from the
    picker's own .novc/ location, so it resolves identically whether the page is
    opened as a file:// URL (no server) or served over http://.

    ``init_boxes_px`` (px ``{x, y, w, h}`` dicts in the scan's own pixel space) seeds
    the editor so it opens with boxes to tweak rather than blank. They are injected as
    px and converted to the editor's normalized 0-1 form in-browser on image load
    (using naturalWidth/Height), so this stays Pillow-free like the rest of the tool.
    """
    img_url = f"../gh-pages/accgram/img/{img_name}"
    init_json = json.dumps(init_boxes_px or [])
    return (
        _HTML_TEMPLATE.replace("__IMG_NAME__", img_name)
        .replace("__IMG_URL__", img_url)
        .replace("__INIT_BOXES_PX__", init_json)
    )


def generate(
    arg: str,
    *,
    serve: bool = False,
    open_browser: bool = True,
    init_boxes_px: list[dict] | None = None,
) -> None:
    img_name = _resolve_img(arg)
    html = _build_html(img_name, init_boxes_px)
    _OUT_DIR.mkdir(exist_ok=True)
    out_path = _OUT_DIR / f"highlight-picker-{img_name}.html"
    out_path.write_text(html, encoding="utf-8", newline="")
    print(f"Picker written to: {out_path}")
    if serve:
        # Serve from the repo root so both .novc/ HTML and gh-pages/accgram/img/ resolve.
        serve_and_open(
            wlc_paths.wlc_data_root(),
            f".novc/{out_path.name}",
            open_browser=open_browser,
        )
    else:
        # No server needed: the img path is relative, so file:// works directly.
        file_url = out_path.as_uri()
        print(f"Open this in your browser:\n  {file_url}")
        # --no-open prints the URL and stops there, for the common case where the picker
        # is generated by one person and opened by another (or where the page is already
        # up in a browser and a launched copy would only be a duplicate tab).
        if open_browser:
            webbrowser.open(file_url)


# The whole editor is vanilla JS/CSS with no external dependencies, mirroring the
# codex-index-aleppo box/quad editors. Placeholders __IMG_NAME__ / __IMG_URL__ are
# substituted by _build_html; there is no other templating, so { and } are literal.
_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Highlight Picker &mdash; __IMG_NAME__</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #222; color: #eee; font-family: system-ui, sans-serif; }
  #toolbar {
    position: sticky; top: 0; z-index: 100;
    background: #333; border-bottom: 1px solid #555;
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    padding: 8px 12px; font-size: 13px;
  }
  #toolbar button {
    padding: 5px 12px; cursor: pointer; font-size: 13px;
    border: 1px solid #888; border-radius: 4px; background: #444; color: #eee;
  }
  #toolbar button:hover { background: #555; }
  #toolbar button.active { background: #070; border-color: #0a0; }
  #toolbar button.export { background: #046; border-color: #08f; }
  .info { color: #aaa; font-size: 12px; }
  #status { color: #aaa; font-size: 12px; margin-left: auto; }
  #stage { padding: 16px; text-align: center; }
  .img-wrapper { position: relative; display: inline-block; line-height: 0; }
  .img-wrapper img { display: block; max-width: 100%; max-height: calc(100vh - 90px); }
  .img-wrapper svg { position: absolute; inset: 0; width: 100%; height: 100%; }
  .box-fill { pointer-events: none; }
  .box-outline { pointer-events: none; }
  .handle { pointer-events: all; }
  .handle:hover { fill-opacity: 1; }
  .toast {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: #070; color: #fff; padding: 8px 24px; border-radius: 4px;
    font-size: 14px; z-index: 200; opacity: 0; transition: opacity 0.3s;
  }
  .toast.show { opacity: 1; }
</style>
</head>
<body>

<div id="toolbar">
  <span><b>Highlight Picker</b> &mdash; __IMG_NAME__</span>
  <button onclick="addBox()">Add box</button>
  <button onclick="deleteActive()">Delete active</button>
  <button id="fine-btn" onclick="toggleFine()" class="active">Fine: ON</button>
  <button onclick="resetAll()">Reset</button>
  <button class="export" onclick="exportJSON()">Export JSON</button>
  <button class="export" onclick="copyPython()">Copy Python boxes</button>
  <span class="info">Tab: cycle boxes &middot; 1-5: pick handle &middot; arrows: nudge &middot; f: fine</span>
  <span id="status"></span>
</div>

<div id="stage">
  <div class="img-wrapper" id="wrapper">
    <img id="img" src="__IMG_URL__" alt="__IMG_NAME__">
    <svg id="svg" viewBox="0 0 1 1" preserveAspectRatio="none"></svg>
  </div>
</div>

<div id="toast" class="toast"></div>

<script>
"use strict";

const SVGNS = "http://www.w3.org/2000/svg";
const IMG_NAME = "__IMG_NAME__";
// Optional seed boxes in scan-pixel space ([{x,y,w,h}, ...] or []), injected by
// _build_html. Converted to normalized 0-1 boxes once the image is measured (seedFromInit).
const INIT_BOXES_PX = __INIT_BOXES_PX__;
const FINE_SCALE = 0.2;
const MIN = 0.01;

// Each box is normalized 0-1: {left, top, right, bottom}. Resolution-independent.
let boxes = [];
let active = -1;
let lastSide = "right";
let fineMode = true;

const svg = document.getElementById("svg");
const img = document.getElementById("img");
const statusEl = document.getElementById("status");
const toastEl = document.getElementById("toast");

function showToast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add("show");
  setTimeout(() => toastEl.classList.remove("show"), 1800);
}

function newBoxDefault() {
  // A modest box near the center; the user drags it onto the target word.
  const n = boxes.length;
  const off = (n % 5) * 0.03;
  return { left: 0.40 + off, top: 0.42 + off, right: 0.60 + off, bottom: 0.52 + off };
}

function addBox() {
  boxes.push(newBoxDefault());
  active = boxes.length - 1;
  lastSide = "move";
  draw();
  updateStatus();
}

function deleteActive() {
  if (active < 0) return;
  boxes.splice(active, 1);
  active = boxes.length ? Math.min(active, boxes.length - 1) : -1;
  draw();
  updateStatus();
}

function resetAll() {
  boxes = [];
  active = -1;
  draw();
  updateStatus();
}

function toggleFine() {
  fineMode = !fineMode;
  const btn = document.getElementById("fine-btn");
  btn.textContent = fineMode ? "Fine: ON" : "Fine: OFF";
  btn.classList.toggle("active", fineMode);
}

// --- Drawing ---------------------------------------------------------------

function mkEl(tag, attrs) {
  const el = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);

  boxes.forEach((b, i) => {
    const isActive = i === active;
    const color = isActive ? "#ffcc00" : "#40a0ff";
    const bw = b.right - b.left;
    const bh = b.bottom - b.top;

    svg.appendChild(mkEl("rect", {
      class: "box-fill",
      x: b.left, y: b.top, width: bw, height: bh,
      fill: color, "fill-opacity": isActive ? 0.28 : 0.16,
    }));
    svg.appendChild(mkEl("rect", {
      class: "box-outline",
      x: b.left, y: b.top, width: bw, height: bh,
      fill: "none", stroke: color, "stroke-width": 0.003,
    }));

    // Index label at the top-left corner.
    const label = mkEl("text", {
      x: b.left + 0.006, y: b.top + 0.03,
      "font-size": 0.028, "font-weight": "bold", fill: color,
    });
    label.textContent = String(i + 1);
    svg.appendChild(label);

    if (!isActive) return;

    const midX = (b.left + b.right) / 2;
    const midY = (b.top + b.bottom) / 2;
    const handles = [
      { s: "left",   cx: b.left,  cy: midY,  cur: "ew-resize" },
      { s: "right",  cx: b.right, cy: midY,  cur: "ew-resize" },
      { s: "top",    cx: midX,    cy: b.top, cur: "ns-resize" },
      { s: "bottom", cx: midX,    cy: b.bottom, cur: "ns-resize" },
      { s: "move",   cx: midX,    cy: midY,  cur: "move" },
    ];
    for (const h of handles) {
      const r = h.s === "move" ? 0.014 : 0.011;
      const fill = h.s === lastSide ? "#ffff00" : h.s === "move" ? "#40ff90" : color;
      const c = mkEl("circle", {
        class: "handle",
        cx: h.cx, cy: h.cy, r: r,
        fill: fill, "fill-opacity": 0.85, stroke: "#fff", "stroke-width": 0.002,
        style: "cursor:" + h.cur,
      });
      c.dataset.side = h.s;
      svg.appendChild(c);
    }
  });
}

// --- Dragging --------------------------------------------------------------

let dragSide = null;
let dragStartMouse = null;
let dragStartBox = null;

function svgCoords(e) {
  const r = svg.getBoundingClientRect();
  return { x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height };
}

svg.addEventListener("mousedown", (e) => {
  const t = e.target;
  if (!t.classList || !t.classList.contains("handle")) return;
  if (active < 0) return;
  e.preventDefault();
  dragSide = t.dataset.side;
  lastSide = dragSide;
  dragStartMouse = svgCoords(e);
  dragStartBox = Object.assign({}, boxes[active]);
});

window.addEventListener("mousemove", (e) => {
  if (dragSide === null || active < 0) return;
  const m = svgCoords(e);
  let dx = m.x - dragStartMouse.x;
  let dy = m.y - dragStartMouse.y;
  if (fineMode) { dx *= FINE_SCALE; dy *= FINE_SCALE; }
  const b0 = dragStartBox;
  const b = boxes[active];

  if (dragSide === "move") {
    const bw = b0.right - b0.left;
    const bh = b0.bottom - b0.top;
    let nl = Math.max(0, Math.min(1 - bw, b0.left + dx));
    let nt = Math.max(0, Math.min(1 - bh, b0.top + dy));
    b.left = nl; b.right = nl + bw; b.top = nt; b.bottom = nt + bh;
  } else if (dragSide === "left") {
    b.left = Math.max(0, Math.min(b0.right - MIN, b0.left + dx));
  } else if (dragSide === "right") {
    b.right = Math.min(1, Math.max(b0.left + MIN, b0.right + dx));
  } else if (dragSide === "top") {
    b.top = Math.max(0, Math.min(b0.bottom - MIN, b0.top + dy));
  } else if (dragSide === "bottom") {
    b.bottom = Math.min(1, Math.max(b0.top + MIN, b0.bottom + dy));
  }
  draw();
  updateStatus();
});

window.addEventListener("mouseup", () => {
  if (dragSide !== null) { dragSide = null; draw(); }
});

// --- Keyboard --------------------------------------------------------------

const STEP = 0.004;

window.addEventListener("keydown", (e) => {
  if (e.key === "f" || e.key === "F") { toggleFine(); return; }

  if (e.key === "Tab") {
    e.preventDefault();
    if (boxes.length) active = (active + 1) % boxes.length;
    draw();
    updateStatus();
    return;
  }

  if ("12345".includes(e.key)) {
    lastSide = ["left", "right", "top", "bottom", "move"][parseInt(e.key, 10) - 1];
    draw();
    updateStatus();
    return;
  }

  if (!["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) return;
  if (active < 0) return;
  e.preventDefault();
  const step = fineMode ? STEP * FINE_SCALE : STEP;
  const b = boxes[active];

  if (lastSide === "move") {
    const bw = b.right - b.left, bh = b.bottom - b.top;
    if (e.key === "ArrowLeft")  { b.left = Math.max(0, b.left - step); }
    if (e.key === "ArrowRight") { b.left = Math.min(1 - bw, b.left + step); }
    if (e.key === "ArrowUp")    { b.top = Math.max(0, b.top - step); }
    if (e.key === "ArrowDown")  { b.top = Math.min(1 - bh, b.top + step); }
    b.right = b.left + bw; b.bottom = b.top + bh;
  } else if (lastSide === "left") {
    if (e.key === "ArrowLeft")  b.left = Math.max(0, b.left - step);
    if (e.key === "ArrowRight") b.left = Math.min(b.right - MIN, b.left + step);
  } else if (lastSide === "right") {
    if (e.key === "ArrowLeft")  b.right = Math.max(b.left + MIN, b.right - step);
    if (e.key === "ArrowRight") b.right = Math.min(1, b.right + step);
  } else if (lastSide === "top") {
    if (e.key === "ArrowUp")   b.top = Math.max(0, b.top - step);
    if (e.key === "ArrowDown") b.top = Math.min(b.bottom - MIN, b.top + step);
  } else if (lastSide === "bottom") {
    if (e.key === "ArrowUp")   b.bottom = Math.max(b.top + MIN, b.bottom - step);
    if (e.key === "ArrowDown") b.bottom = Math.min(1, b.bottom + step);
  }
  draw();
  updateStatus();
});

// --- Status ----------------------------------------------------------------

function naturalSize() {
  return [img.naturalWidth || 0, img.naturalHeight || 0];
}

function updateStatus() {
  const [w, h] = naturalSize();
  if (active < 0) {
    statusEl.textContent = boxes.length
      ? boxes.length + " box(es); none active"
      : "No boxes yet -- click 'Add box'";
    return;
  }
  const b = boxes[active];
  const px = toPx(b, w, h);
  statusEl.textContent =
    "box " + (active + 1) + "/" + boxes.length + " [" + lastSide + "]  " +
    "px x=" + px.x + " y=" + px.y + " w=" + px.w + " h=" + px.h +
    (fineMode ? "  [FINE]" : "");
}

// --- Export ----------------------------------------------------------------

function round4(v) { return Math.round(v * 10000) / 10000; }

function toPx(b, w, h) {
  const x = Math.round(b.left * w);
  const y = Math.round(b.top * h);
  const x2 = Math.round(b.right * w);
  const y2 = Math.round(b.bottom * h);
  return { x: x, y: y, w: x2 - x, h: y2 - y };
}

function toRel(b) {
  return {
    x: round4(b.left), y: round4(b.top),
    w: round4(b.right - b.left), h: round4(b.bottom - b.top),
  };
}

function buildExport() {
  const [w, h] = naturalSize();
  return {
    image: IMG_NAME,
    image_size: [w, h],
    boxes: boxes.map((b) => ({ rel: toRel(b), px: toPx(b, w, h) })),
  };
}

function exportJSON() {
  if (!boxes.length) { showToast("No boxes to export"); return; }
  const jsonStr = JSON.stringify(buildExport(), null, 2) + "\\n";
  const blob = new Blob([jsonStr], { type: "application/json" });
  const a = document.createElement("a");
  a.download = "highlight-boxes-" + IMG_NAME + ".json";
  a.href = URL.createObjectURL(blob);
  a.click();
  URL.revokeObjectURL(a.href);
  showToast("Exported " + a.download);
}

function pythonSnippet() {
  const [w, h] = naturalSize();
  const lines = boxes.map((b) => {
    const p = toPx(b, w, h);
    return "    mhi.Box(x=" + p.x + ", y=" + p.y + ", w=" + p.w + ", h=" + p.h + "),";
  });
  return "(\\n" + lines.join("\\n") + "\\n)";
}

async function copyPython() {
  if (!boxes.length) { showToast("No boxes to copy"); return; }
  const text = pythonSnippet();
  try {
    await navigator.clipboard.writeText(text);
    showToast("Copied " + boxes.length + " mhi.Box(...) line(s)");
  } catch (err) {
    // Clipboard API can be blocked; fall back to a prompt for manual copy.
    window.prompt("Copy the Python boxes:", text);
  }
}

// --- Init ------------------------------------------------------------------

// Seed the editor from INIT_BOXES_PX exactly once, once the image has a measured
// natural size (needed to normalize px -> 0-1). Runs on load, and immediately if the
// image is already complete (cached), where the load event may have fired earlier.
let seeded = false;
function seedFromInit() {
  if (seeded) return;
  const [w, h] = naturalSize();
  if (!w || !h) return;
  seeded = true;
  if (!INIT_BOXES_PX.length) return;
  boxes = INIT_BOXES_PX.map((b) => ({
    left: b.x / w, top: b.y / h,
    right: (b.x + b.w) / w, bottom: (b.y + b.h) / h,
  }));
  active = 0;
  lastSide = "move";
  draw();
  updateStatus();
}

img.addEventListener("load", () => { seedFromInit(); updateStatus(); });
if (img.complete && img.naturalWidth) seedFromInit();
draw();
updateStatus();
</script>
</body>
</html>
"""


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: _IMG_DIR and _OUT_DIR are module constants off wlc_paths.  The
    # parameter is here so the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument(
        "image",
        help="scan filename under gh-pages/accgram/img/, with or without the .png",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="run a local http server instead of opening a file:// URL",
    )
    parser.add_argument(
        "--no-open",
        dest="open_browser",
        action="store_false",
        help="print the URL only; launch no browser",
    )
    parser.add_argument(
        "--boxes-file",
        type=Path,
        help=(
            "seed the editor with boxes to tweak, rather than opening blank: JSON holding"
            " a list of {x,y,w,h} px boxes, or a prior highlight-boxes-*.json export"
        ),
    )


def run(args: argparse.Namespace) -> None:
    init_boxes_px = None
    if args.boxes_file:
        init_boxes_px = _px_boxes_from_arg(
            json.loads(args.boxes_file.read_text(encoding="utf-8"))
        )
    generate(
        args.image,
        serve=args.serve,
        open_browser=args.open_browser,
        init_boxes_px=init_boxes_px,
    )
