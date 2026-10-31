"""The overlay page: every stroke-SVG drawn over its crop, with its numbers.

The strokes are filled translucently, each in the next of the five colours
Collidoscope's draw_overlaps gives glyphs (green, red, purple, blue, yellow),
so that where two strokes overlap their colours mix; the other layers can be
switched on and off, by checkboxes beside each image that act on that image
alone.  One layer draws the strokes black, so that with the crop off they show
the page unaged, black on white (decision 11 of the profile's note).  A
supplied stroke (decision 15) is drawn in one style only, in every view: hatched
and outlined in a colour no other layer of the page uses, never filled solid
and never in a stroke's colour or black.  The crop is drawn smoothly, not as
squares, unless its image's checkbox asks for squares.  Writes
doc/pen-stroke-snips/overlays.html.
"""

import html
from collections import Counter
from pathlib import Path

import numpy as np

from pen_stroke import curve
from pen_stroke import derive as dv
from pen_stroke import geometry as geo
from pen_stroke import level5
from pen_stroke import stroke_svg as ssvg
from pen_stroke import tools

SCALE = 4
STROKE_COLOURS = ("green", "red", "purple", "blue", "yellow")
# Decision 15: a supplied stroke is never drawn as other strokes are.  This
# colour is reserved for it on the page, with the hatching SUPPLIED_DEFS gives.
SUPPLIED_COLOUR = "#ff6d00"
SUPPLIED_HATCH = "supplied-hatch"
SUPPLIED_DEFS = (
    f'<pattern id="{SUPPLIED_HATCH}" patternUnits="userSpaceOnUse" width="2" height="2"'
    ' patternTransform="rotate(45)">'
    f'<rect x="0" y="0" width="1" height="2" fill="{SUPPLIED_COLOUR}"/></pattern>'
)
SUPPLIED_SWATCH = (
    f"background: repeating-linear-gradient(45deg, {SUPPLIED_COLOUR} 0 2px,"
    f" transparent 2px 4px); border: 1px dashed {SUPPLIED_COLOUR}"
)
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
HALO_COLOUR = "#2e86c1"
SMOOTHING_COLOUR = "#cddc39"
UNEXPLAINED_COLOUR = "#e91e63"
OVERSHOOT_COLOUR = "#00acc1"
FRAME_COLOUR = "#1f618d"
# (layer, label, on at first, the swatch's style or None)
LAYERS = (
    ("crop", "crop", True, None),
    ("fills", "level 1: fills", False, "background: #000; opacity: 0.3"),
    ("halo", "level 1: threshold halo", False, f"background: {HALO_COLOUR}"),
    (
        "smoothing",
        "level 1: smoothing slivers",
        False,
        f"background: {SMOOTHING_COLOUR}",
    ),
    ("pieces", "level 1: residual pieces, by judgment", False, None),
    ("strokes", "level 2: strokes", True, None),
    (
        "black",
        "level 2: strokes in black, for the page unaged",
        False,
        "background: #000",
    ),
    (
        "supplied",
        "level 2: supplied strokes, of which the crop shows little or no ink",
        True,
        SUPPLIED_SWATCH,
    ),
    ("medians", "level 2: medians", True, None),
    (
        "unexplained",
        "level 2: ink no stroke explains",
        False,
        f"background: {UNEXPLAINED_COLOUR}",
    ),
    (
        "overshoot",
        "level 2: sweep beyond the ink",
        False,
        f"background: {OVERSHOOT_COLOUR}",
    ),
    ("frame", "level 4: frame", False, f"background: {FRAME_COLOUR}"),
    ("groups", "level 5: groups, by kind", False, None),
    ("labels", "stroke ids", False, None),
)

_CSS = """
body { font-family: system-ui, sans-serif; margin: 1.5em; max-width: 72em; background: #fff; color: #111; }
p.ai-caveat { border: 3px solid #b00020; padding: 0.6em 0.8em; }
.layered { display: flex; flex-wrap: wrap; gap: 0.8em; align-items: flex-start; margin: 0.6em 0; }
.layered fieldset { margin: 0; padding: 0.3em 0.7em; max-width: 21em; font-size: 0.9em; }
.layered fieldset label { display: block; white-space: nowrap; }
.layered fieldset p { margin: 0.2em 0 0.2em 1.4em; font-size: 0.9em; white-space: normal; }
svg.overlay { border: 1px solid #999; background: #fff; display: block; }
svg.overlay image { image-rendering: auto; }
.squares svg.overlay image { image-rendering: pixelated; }
table { border-collapse: collapse; margin: 0.6em 0; }
td, th { border: 1px solid #bbb; padding: 0.15em 0.5em; text-align: left; vertical-align: middle; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
td[dir=rtl] { font-size: 1.6em; line-height: 1.8; }
.swatch { display: inline-block; width: 0.9em; height: 0.9em; vertical-align: -0.1em; border: 1px solid #555; }
"""


def _hide_rules():
    return "\n".join(
        f".hide-{name} .layer-{name} {{ display: none; }}" for name, _, _, _ in LAYERS
    )


_JS = """
for (const box of document.querySelectorAll('.layered input[data-layer]')) {
  const fig = box.closest('.layered');
  const apply = () => fig.classList.toggle('hide-' + box.dataset.layer, !box.checked);
  box.addEventListener('change', apply);
  apply();
}
for (const box of document.querySelectorAll('.layered input[data-squares]')) {
  const fig = box.closest('.layered');
  const apply = () => fig.classList.toggle('squares', box.checked);
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


def _swatch(style):
    return f'<span class="swatch" style="{style}"></span>'


def _crop_metrics(sf):
    w, h = sf.width, sf.height
    ink_px = geo.rasterize(
        [p for d in dv.ink_fill_ds(sf) for p in geo.flatten(geo.parse_path(d))], w, h
    )
    rows = []
    seen = np.zeros_like(ink_px)
    supplied = np.zeros_like(ink_px)
    for st in sf.strokes:
        polys = geo.flatten(geo.parse_path(st.ink))
        mask = geo.rasterize(polys, w, h)
        if st.supplied:
            supplied |= mask
        else:
            seen |= mask
        length = curve.length(dv.median_segments(st))
        area = int(mask.sum())
        over = int((mask & ~ink_px).sum())
        rows.append((st, length, area, over))
    unexplained = int(geo.path_mask(sf.unexplained, w, h).sum())
    overshoot = int(geo.path_mask(sf.overshoot, w, h).sum())
    return {
        "ink": int(ink_px.sum()),
        "swept": int(seen.sum()),
        "supplied": int(supplied.sum()),
        "unexplained": unexplained,
        "overshoot": overshoot,
        "strokes": rows,
    }


def stroke_colour(k):
    """The colour of the stroke at index k among a file's strokes that are not supplied."""
    return STROKE_COLOURS[k % len(STROKE_COLOURS)]


def supplied_ink(st, scale):
    """A supplied stroke's ink in the one style decision 15 allows it."""
    return (
        f'<path d="{st.ink}" fill="url(#{SUPPLIED_HATCH})" stroke="{SUPPLIED_COLOUR}"'
        f' stroke-width="{geo.fmt(1.5 / scale, 3)}"'
        f' stroke-dasharray="{geo.fmt(4 / scale, 3)} {geo.fmt(3 / scale, 3)}"/>'
    )


def _svg(sf, groups_of):
    w, h = sf.width, sf.height
    seen = [st for st in sf.strokes if not st.supplied]
    supplied = [st for st in sf.strokes if st.supplied]
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
        f'<path class="layer-halo" fill="{HALO_COLOUR}" fill-opacity="0.35" d="{sf.halo}"/>'
    )
    out.append(
        f'<path class="layer-smoothing" fill="{SMOOTHING_COLOUR}" fill-opacity="0.8" d="{sf.smoothing}"/>'
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
    for k, st in enumerate(seen):
        kinds = ", ".join(groups_of.get(st.id, []))
        out.append(
            f'<path fill="{stroke_colour(k)}" d="{st.ink}">'
            f"<title>{_e(st.id)}: {_e(kinds)}</title></path>"
        )
    out.append("</g>")
    out.append('<g class="layer-groups" fill-opacity="0.55">')
    for st in seen:
        kinds = groups_of.get(st.id, [])
        family = kind_family(kinds[0]) if kinds else "undetermined"
        out.append(
            f'<path fill="{KIND_COLOURS[family]}" d="{st.ink}"><title>{_e(", ".join(kinds))}</title></path>'
        )
    out.append("</g>")
    out.append('<g class="layer-black" fill="#000">')
    out += [f'<path d="{st.ink}"/>' for st in seen]
    out.append("</g>")
    out.append('<g class="layer-supplied">')
    for st in supplied:
        kinds = ", ".join(groups_of.get(st.id, []))
        out.append(
            f"<g><title>{_e(st.id)}, supplied ({_e(st.supplied)}): {_e(kinds)}."
            f" {_e(st.supplied_why)}</title>{supplied_ink(st, SCALE)}</g>"
        )
    out.append("</g>")
    out.append('<g class="layer-medians" fill="none" stroke-width="0.5">')
    for st in sf.strokes:
        segs = dv.median_segments(st)
        colour = SUPPLIED_COLOUR if st.supplied else "#000"
        dash = ' stroke-dasharray="1.5 1"' if st.supplied else ""
        out.append(f'<path stroke="{colour}"{dash} d="{st.median}"/>')
        out += [
            f'<circle cx="{geo.fmt(x, 2)}" cy="{geo.fmt(y, 2)}" r="0.6" fill="{colour}"/>'
            for x, y in [segs[0][0]] + [seg[3] for seg in segs]
        ]
    out.append("</g>")
    out.append(
        f'<path class="layer-unexplained" fill="{UNEXPLAINED_COLOUR}" fill-opacity="0.8" d="{sf.unexplained}"/>'
    )
    out.append(
        f'<path class="layer-overshoot" fill="{OVERSHOOT_COLOUR}" fill-opacity="0.8" d="{sf.overshoot}"/>'
    )
    if sf.frame is not None:
        x1, y1, x2, y2 = sf.frame.baseline
        lh = sf.frame.letter_height
        out.append(
            f'<g class="layer-frame" stroke="{FRAME_COLOUR}" stroke-width="0.6">'
        )
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
        out.append(
            f'<line x1="{x1}" y1="{y1 - lh}" x2="{x2}" y2="{y2 - lh}" stroke-dasharray="2 1.5"/>'
        )
        out.append("</g>")
    out.append('<g class="layer-labels" font-size="4" fill="#000">')
    for st in sf.strokes:
        x, y = dv.median_segments(st)[0][0]
        out.append(
            f'<text x="{geo.fmt(x + 0.8, 2)}" y="{geo.fmt(y - 0.8, 2)}">{_e(st.id)}</text>'
        )
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def layer_controls():
    """The checkboxes that switch one image's layers, with what each layer's colours mean."""
    out = ["<fieldset><legend>This image's layers</legend>"]
    for name, label, on, swatch in LAYERS:
        mark = _swatch(swatch) + " " if swatch else ""
        out.append(
            f'<label><input type="checkbox" data-layer="{name}"{" checked" if on else ""}>'
            f" {mark}{_e(label)}</label>"
        )
        if name == "pieces":
            out.append(
                "<p>"
                + " ".join(
                    f"{_swatch('background:' + c)} {_e(j)}"
                    for j, c in JUDGED_COLOURS.items()
                )
                + "</p>"
            )
        elif name == "groups":
            out.append(
                "<p>"
                + " ".join(
                    f"{_swatch('background:' + c)} {_e(k)}"
                    for k, c in KIND_COLOURS.items()
                )
                + "</p>"
            )
    out.append(
        '<label><input type="checkbox" data-squares> the crop\'s pixels as squares</label>'
    )
    out.append("</fieldset>")
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
    out.append('<div class="layered">')
    out.append(_svg(sf, groups_of))
    out.append(layer_controls())
    out.append("</div>")
    swept = m["swept"] or 1
    ink = m["ink"] or 1
    judged = Counter(p.judged for p in sf.pieces)
    nsupplied = sum(1 for st in sf.strokes if st.supplied)
    out.append("<table>")
    out.append(
        f"<tr><th>Threshold</th><td>luminance below {sf.threshold}; specks of up to"
        f" {sf.speck_size} pixels dropped; halo &#177;{sf.halo_band}</td></tr>"
    )
    out.append(
        f"<tr><th>Ink</th><td>{m['ink']} pixels in the fills judged ink</td></tr>"
    )
    out.append(
        f"<tr><th>Strokes</th><td>{len(sf.strokes) - nsupplied} that model ink the crop"
        f" shows, sweeping {m['swept']} pixels</td></tr>"
    )
    if nsupplied:
        out.append(
            f"<tr><th>Supplied strokes</th><td>{nsupplied}, covering {m['supplied']}"
            " pixels</td></tr>"
        )
    out.append(
        f"<tr><th>Ink no stroke explains</th><td>{m['unexplained']} pixels,"
        f" {100 * m['unexplained'] / ink:.1f}% of the ink</td></tr>"
    )
    out.append(
        f"<tr><th>Sweep beyond the ink</th><td>{m['overshoot']} pixels,"
        f" {100 * m['overshoot'] / swept:.1f}% of the area the strokes that are not"
        " supplied sweep</td></tr>"
    )
    pieces = ", ".join(f"{n} {k}" for k, n in sorted(judged.items())) or "none"
    out.append(
        f"<tr><th>Residual pieces</th><td>{len(sf.pieces)}: {_e(pieces)}</td></tr>"
    )
    out.append("</table>")
    out.append(
        "<table><tr><th>Stroke</th><th>Groups</th><th>Pass</th><th>Ends</th>"
        "<th>Shape</th><th>Segments</th><th>Length (px)</th><th>Width (px)</th>"
        "<th>Area (px)</th><th>Beyond the ink (px)</th><th>Confidence</th>"
        "<th>Supplied</th><th>Note</th></tr>"
    )
    k = 0
    for st, length, area, over in m["strokes"]:
        if st.supplied:
            swatch = _swatch(SUPPLIED_SWATCH)
            supplied = f"{_e(st.supplied)}: {_e(st.supplied_why)}"
        else:
            swatch = f'<span class="swatch" style="background:{stroke_colour(k)};opacity:0.6"></span>'
            supplied = ""
            k += 1
        share = f"{over} ({100 * over / area:.0f}%)" if area else "0"
        nseg = len(dv.median_segments(st))
        widths = f"{min(st.widths):.1f} to {max(st.widths):.1f}"
        out.append(
            f"<tr><td>{swatch} {_e(st.id)}</td><td>{_e(', '.join(groups_of.get(st.id, [])))}</td>"
            f"<td>{_e(st.pass_name)}</td><td>{_e(st.ends)}</td><td>{_e(st.shape)}</td>"
            f'<td class="num">{nseg}</td><td class="num">{length:.1f}</td>'
            f'<td class="num">{widths}</td><td class="num">{area}</td>'
            f'<td class="num">{share}</td><td>{_e(st.confidence)}</td>'
            f"<td>{supplied}</td><td>{_e(st.note)}</td></tr>"
        )
    out.append("</table>")
    out.append("</section>")
    return "\n".join(out)


def page(svg_paths):
    sections = "\n".join(_section(p) for p in svg_paths)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Pen-stroke overlays</title>
<style>{_CSS}{_hide_rules()}
</style>
</head>
<body>
<svg width="0" height="0" style="position: absolute" aria-hidden="true"><defs>{SUPPLIED_DEFS}</defs></svg>
<h1>Pen-stroke overlays</h1>
<p class="ai-caveat"><strong>Strokes traced by an AI model, not yet reviewed by a human.</strong>
Claude, an AI model, placed every stroke's median on this page by eye, had a script smooth it
into curves and fit its widths and ends to the ink, and judged every residual piece, so read the
strokes as a draft.</p>
<p>Each crop of the Leningrad Codex is drawn four times its size, with its stroke-SVG over it.
The checkboxes beside each image switch that image's layers. The profile, and what each layer
means, are in <a href="../pen-stroke-representation.md">doc/pen-stroke-representation.md</a>;
this page is generated by <code>py/main_pen_stroke.py render</code>.</p>
<p>{_swatch(SUPPLIED_SWATCH)} <strong>Hatched orange, outlined with dashes: a supplied
stroke.</strong> The crop shows little or no ink of it; it is there because the transcription
or the layout implies it. No other stroke is ever drawn this way, and a supplied stroke is never
drawn in a stroke's colour or in black.</p>
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
