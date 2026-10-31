"""The overlay page: every stroke-SVG drawn over its crop, with its numbers.

The strokes are filled translucently, each in the next of the five colours
Collidoscope's draw_overlaps gives glyphs (green, red, purple, blue, yellow),
so that where two strokes overlap their colours mix; the other layers can be
switched on and off.  Writes doc/pen-stroke-snips/overlays.html.
"""

import html
import math
from collections import Counter
from pathlib import Path

import numpy as np

from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import level5
from pen_stroke import stroke_svg as ssvg
from pen_stroke import tools

SCALE = 4
STROKE_COLOURS = ("green", "red", "purple", "blue", "yellow")
JUDGED_COLOURS = {
    "unjudged": "#ff00ff",
    "ink": "#1e8449",
    "speck": "#566573",
    "stain": "#a0522d",
    "bleed-through": "#7d3c98",
    "damage": "#b03a2e",
    "noise": "#95a5a6",
    "paper": "#d4ac0d",
}
KIND_COLOURS = {
    "letter": "#1f618d",
    "vowel": "#1e8449",
    "accent": "#b03a2e",
    "mark": "#7d3c98",
    "undetermined": "#566573",
}
# (layer, label, on at first)
LAYERS = (
    ("crop", "crop", True),
    ("fills", "level 1: fills", False),
    ("halo", "level 1: threshold halo", False),
    ("smoothing", "level 1: smoothing slivers", False),
    ("pieces", "level 1: residual pieces", False),
    ("strokes", "level 2: strokes", True),
    ("medians", "level 2: medians", True),
    ("unexplained", "level 2: ink no stroke explains", False),
    ("overshoot", "level 2: sweep beyond the ink", False),
    ("frame", "level 4: frame", False),
    ("groups", "level 5: groups by kind", False),
    ("labels", "stroke ids", False),
)

_CSS = """
body { font-family: system-ui, sans-serif; margin: 1.5em; max-width: 72em; background: #fff; color: #111; }
p.ai-caveat { border: 3px solid #b00020; padding: 0.6em 0.8em; }
fieldset { margin: 1em 0; }
fieldset label { margin-right: 1.2em; white-space: nowrap; }
svg.overlay { border: 1px solid #999; background: #fff; display: block; margin: 0.6em 0; }
svg.overlay image { image-rendering: pixelated; }
table { border-collapse: collapse; margin: 0.6em 0; }
td, th { border: 1px solid #bbb; padding: 0.15em 0.5em; text-align: left; vertical-align: middle; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
td[dir=rtl] { font-size: 1.6em; line-height: 1.8; }
.swatch { display: inline-block; width: 0.9em; height: 0.9em; vertical-align: -0.1em; border: 1px solid #555; }
"""


def _hide_rules():
    return "\n".join(
        f".hide-{name} .layer-{name} {{ display: none; }}" for name, _, _ in LAYERS
    )


_JS = """
for (const box of document.querySelectorAll('input[data-layer]')) {
  const apply = () => document.body.classList.toggle('hide-' + box.dataset.layer, !box.checked);
  box.addEventListener('change', apply);
  apply();
}
"""


def kind_family(kind):
    if kind.endswith(" letter"):
        return "letter"
    if level5.KINDS[kind][0] is None:
        return "undetermined"
    for family in ("vowel", "accent"):
        if kind.endswith(" " + family):
            return family
    return "mark"


def _e(s):
    return html.escape(str(s), quote=True)


def _crop_metrics(sf):
    w, h = sf.width, sf.height
    ink_px = geo.rasterize(
        [p for d in dv.ink_fill_ds(sf) for p in geo.flatten(geo.parse_path(d))], w, h
    )
    rows = []
    union = np.zeros_like(ink_px)
    for st in sf.strokes:
        polys = geo.flatten(geo.parse_path(st.ink))
        mask = geo.rasterize(polys, w, h)
        union |= mask
        pts = dv.median_points(st)
        length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        area = int(mask.sum())
        over = int((mask & ~ink_px).sum())
        rows.append((st, length, area, over))
    unexplained = int(geo.path_mask(sf.unexplained, w, h).sum())
    overshoot = int(geo.path_mask(sf.overshoot, w, h).sum())
    return {
        "ink": int(ink_px.sum()),
        "swept": int(union.sum()),
        "unexplained": unexplained,
        "overshoot": overshoot,
        "strokes": rows,
    }


def _svg(sf, groups_of):
    w, h = sf.width, sf.height
    out = [
        f'<svg class="overlay" width="{w * SCALE}" height="{h * SCALE}"'
        f' viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    ]
    out.append(
        f'<image class="layer-crop" href="{_e(sf.image)}" x="0" y="0" width="{w}" height="{h}"/>'
    )
    out.append('<g class="layer-fills" fill="#000" fill-opacity="0.3">')
    out += [f'<path d="{f.d}"/>' for f in sf.fills if f.judged in (None, "ink")]
    out.append("</g>")
    out.append(
        f'<path class="layer-halo" fill="#2e86c1" fill-opacity="0.35" d="{sf.halo}"/>'
    )
    out.append(
        f'<path class="layer-smoothing" fill="#e67e22" fill-opacity="0.8" d="{sf.smoothing}"/>'
    )
    out.append('<g class="layer-pieces">')
    for p in sf.pieces:
        out.append(
            f'<path fill="{JUDGED_COLOURS[p.judged]}" fill-opacity="0.85" d="{p.d}">'
            f"<title>{_e(p.id)}: {_e(p.source)}, judged {_e(p.judged)}</title></path>"
        )
    for f in sf.fills:
        if f.judged not in (None, "ink"):
            out.append(
                f'<path fill="{JUDGED_COLOURS[f.judged]}" fill-opacity="0.85" d="{f.d}">'
                f"<title>{_e(f.id)}: a fill judged {_e(f.judged)}</title></path>"
            )
    out.append("</g>")
    out.append('<g class="layer-strokes" fill-opacity="0.45">')
    for k, st in enumerate(sf.strokes):
        kinds = ", ".join(groups_of.get(st.id, []))
        out.append(
            f'<path fill="{STROKE_COLOURS[k % len(STROKE_COLOURS)]}" d="{st.ink}">'
            f"<title>{_e(st.id)}: {_e(kinds)}</title></path>"
        )
    out.append("</g>")
    out.append('<g class="layer-groups" fill-opacity="0.55">')
    for st in sf.strokes:
        kinds = groups_of.get(st.id, [])
        family = kind_family(kinds[0]) if kinds else "undetermined"
        out.append(
            f'<path fill="{KIND_COLOURS[family]}" d="{st.ink}"><title>{_e(", ".join(kinds))}</title></path>'
        )
    out.append("</g>")
    out.append('<g class="layer-medians" fill="none" stroke="#000" stroke-width="0.5">')
    for st in sf.strokes:
        pts = dv.median_points(st)
        out.append(
            f'<path d="{geo.format_path([(pts[0], [("L", p) for p in pts[1:]], False)], 2)}"/>'
        )
        out += [
            f'<circle cx="{geo.fmt(x, 2)}" cy="{geo.fmt(y, 2)}" r="0.6" fill="#000"/>'
            for x, y in pts
        ]
    out.append("</g>")
    out.append(
        f'<path class="layer-unexplained" fill="#e91e63" fill-opacity="0.8" d="{sf.unexplained}"/>'
    )
    out.append(
        f'<path class="layer-overshoot" fill="#00acc1" fill-opacity="0.8" d="{sf.overshoot}"/>'
    )
    if sf.frame is not None:
        x1, y1, x2, y2 = sf.frame.baseline
        lh = sf.frame.letter_height
        out.append('<g class="layer-frame" stroke="#1f618d" stroke-width="0.6">')
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        out.append(
            f'<line x1="{x1}" y1="{y1 - lh}" x2="{x2}" y2="{y2 - lh}" stroke-dasharray="2 1.5"/>'
        )
        out.append("</g>")
    out.append('<g class="layer-labels" font-size="4" fill="#000">')
    for st in sf.strokes:
        x, y = dv.median_points(st)[0]
        out.append(
            f'<text x="{geo.fmt(x + 0.8, 2)}" y="{geo.fmt(y - 0.8, 2)}">{_e(st.id)}</text>'
        )
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def _section(svg_path):
    sf = ssvg.read(svg_path)
    groups_of = {}
    for g in sf.groups:
        for m in g.members:
            groups_of.setdefault(m, []).append(g.kind)
    m = _crop_metrics(sf)
    pv = sf.provenance
    title = f"{pv.get('manuscript', '')}, page {pv.get('page', '')}, column {pv.get('column', '')}, line {pv.get('line', '')}"
    out = [f'<section id="{_e(Path(svg_path).name)}">', f"<h2>{_e(title)}</h2>"]
    out.append("<table>")
    out.append(f"<tr><th>Verse in MAM</th><td>{_e(pv.get('mam-verse', ''))}</td></tr>")
    out.append(
        f"<tr><th>Verse in the UXLC</th><td>{_e(pv.get('uxlc-verse', ''))}</td></tr>"
    )
    if "combined-chanted-word" in pv:
        out.append(
            "<tr><th>Chanted word, both strands combined: the primary transcription</th>"
            f'<td dir="rtl" lang="hbo">{_e(pv["combined-chanted-word"])}</td></tr>'
        )
        out.append(
            f"<tr><th>Its source</th><td>{_e(pv.get('combined-source', ''))}</td></tr>"
        )
    for key, label in (
        ("taxton-chanted-word", "תחתון"),
        ("elyon-chanted-word", "עליון"),
    ):
        if key in pv:
            out.append(
                f'<tr><th>Chanted word, {label}</th><td dir="rtl" lang="hbo">{_e(pv[key])}</td></tr>'
            )
    if "crop-note" in pv:
        out.append(f"<tr><th>Crop</th><td>{_e(pv['crop-note'])}</td></tr>")
    out.append(
        f"<tr><th>Source</th><td><a href=\"{_e(pv.get('source-url', ''))}\">{_e(pv.get('source-url', ''))}</a>,"
        f" box {_e(pv.get('crop-box', ''))}</td></tr>"
    )
    out.append("</table>")
    out.append(_svg(sf, groups_of))
    nl, nm = sf.nibs[level5.LETTERS], sf.nibs[level5.MARKS]
    swept = m["swept"] or 1
    ink = m["ink"] or 1
    judged = Counter(p.judged for p in sf.pieces)
    out.append("<table>")
    out.append(
        f"<tr><th>Threshold</th><td>luminance below {sf.threshold}; specks of up to"
        f" {sf.speck_size} pixels dropped; halo &#177;{sf.halo_band}</td></tr>"
    )
    for name, nb in (("letters", nl), ("marks", nm)):
        out.append(
            f"<tr><th>Nib for {name}</th><td>width {geo.fmt(nb.width, 2)} px, angle"
            f" {geo.fmt(nb.angle, 1)}&#176;, edge {geo.fmt(nb.edge, 2)} px</td></tr>"
        )
    out.append(
        f"<tr><th>Ink</th><td>{m['ink']} pixels in the fills judged ink</td></tr>"
    )
    out.append(
        f"<tr><th>Strokes</th><td>{len(sf.strokes)}, sweeping {m['swept']} pixels</td></tr>"
    )
    out.append(
        f"<tr><th>Ink no stroke explains</th><td>{m['unexplained']} pixels,"
        f" {100 * m['unexplained'] / ink:.1f}% of the ink</td></tr>"
    )
    out.append(
        f"<tr><th>Sweep beyond the ink</th><td>{m['overshoot']} pixels,"
        f" {100 * m['overshoot'] / swept:.1f}% of the swept area</td></tr>"
    )
    pieces = ", ".join(f"{n} {k}" for k, n in sorted(judged.items())) or "none"
    out.append(
        f"<tr><th>Residual pieces</th><td>{len(sf.pieces)}: {_e(pieces)}</td></tr>"
    )
    out.append("</table>")
    out.append(
        "<table><tr><th>Stroke</th><th>Groups</th><th>Nib</th><th>Shape</th>"
        "<th>Length (px)</th><th>Area (px)</th><th>Beyond the ink (px)</th>"
        "<th>Confidence</th><th>Note</th></tr>"
    )
    for k, (st, length, area, over) in enumerate(m["strokes"]):
        colour = STROKE_COLOURS[k % len(STROKE_COLOURS)]
        share = f"{over} ({100 * over / area:.0f}%)" if area else "0"
        out.append(
            f'<tr><td><span class="swatch" style="background:{colour};opacity:0.6"></span>'
            f" {_e(st.id)}</td><td>{_e(', '.join(groups_of.get(st.id, [])))}</td>"
            f"<td>{_e(st.nib)}</td><td>{_e(st.shape)}</td>"
            f'<td class="num">{length:.1f}</td><td class="num">{area}</td>'
            f'<td class="num">{share}</td><td>{_e(st.confidence)}</td><td>{_e(st.note)}</td></tr>'
        )
    out.append("</table>")
    out.append("</section>")
    return "\n".join(out)


def page(svg_paths):
    boxes = "\n".join(
        f'<label><input type="checkbox" data-layer="{name}"{" checked" if on else ""}> {_e(label)}</label>'
        for name, label, on in LAYERS
    )
    sections = "\n".join(_section(p) for p in svg_paths)
    legend = " ".join(
        f'<span class="swatch" style="background:{c}"></span> {_e(j)}'
        for j, c in JUDGED_COLOURS.items()
    )
    kinds = " ".join(
        f'<span class="swatch" style="background:{c}"></span> {_e(k)}'
        for k, c in KIND_COLOURS.items()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pen-stroke overlays</title>
<style>{_CSS}{_hide_rules()}
</style>
</head>
<body>
<h1>Pen-stroke overlays</h1>
<p class="ai-caveat"><strong>Strokes traced by an AI model, not yet reviewed by a human.</strong>
Claude, an AI model, placed every stroke's median on this page by eye and judged every residual
piece, so read the strokes as a draft.</p>
<p>Each crop of the Leningrad Codex is drawn four times its size, with its stroke-SVG over it.
The profile, and what each layer means, are in
<a href="../pen-stroke-representation.md">doc/pen-stroke-representation.md</a>; this page is
generated by <code>py/main_pen_stroke.py render</code>.</p>
<fieldset><legend>Layers</legend>
{boxes}
</fieldset>
<p>Residual pieces, by judgment: {legend}</p>
<p>Groups, by kind: {kinds}</p>
{sections}
<script>{_JS}</script>
</body>
</html>
"""


def write_overlays(svg_paths, out_dir=tools.SNIPS_DIR):
    if not svg_paths:
        raise ValueError("no stroke-SVGs to render")
    out = Path(out_dir) / "overlays.html"
    text = page(svg_paths)
    with open(out, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(text)
    return out
