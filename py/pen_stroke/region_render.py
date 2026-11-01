"""The region page: every region-SVG's ink drawn in layers that serve its uses.

For each crop: its provenance and transcriptions, and one image with
checkboxes beside it that act on that image alone, a size menu, and the
photograph drawn smoothly, never as squares of pixels.  The layers, as
doc/ink-region-representation.md's "The page" gives them: the photograph; the
ink, black on pure white; the ink by meaning; the ink by group, translucent, so
that an overlap shows the colour of each group that holds it; the ink by
region, an overlap being a region; supplied ink, a supplied mark in orange
(decision 15) and restored ink in teal (decision 25), and supplied vellum, each
filled with its colour alone (decision 26), a colour no other layer uses; and,
for checking, level 1's residual, the cuts, overlaps' outlines, vellum lines
and every seed, and the regions' and overlaps' ids.  Ink that is not the crop's
subject's is slate in every layer (decision 17), and two checkboxes hide it,
and masora circles and stray ink, in every layer.  Writes
doc/pen-stroke-snips/regions.html.
"""

import html
from collections import Counter
from pathlib import Path

from pen_stroke import geometry as geo
from pen_stroke import region_derive as rdv
from pen_stroke import region_svg as rsvg
from pen_stroke import render
from pen_stroke import stroke_svg as ssvg
from pen_stroke import tools

PAGE = "regions.html"
ZOOMS = (1, 1.5, 2, 3, 4, 6, 8)
OTHER_INK_COLOUR = ssvg.OTHER_INK_COLOUR
# Kinds whose ink is set aside rather than read (decisions 21 and 22).
SET_ASIDE_KINDS = ("masora circle mark", "stray mark")
# The ink by meaning, strongest first: a region in groups of several meanings
# takes the strongest.  The colours are Claude's, as the first demonstration of
# regions drew them, for Ben's review.
MEANINGS = ("letter", "mark", "set-aside", "other")
MEANING_COLOURS = {
    "letter": "#000000",
    "mark": "#143caa",
    "set-aside": "#d7c8eb",
    "other": "#c4d2d9",
}
MEANING_LABELS = {
    "letter": "the subject's letters",
    "mark": "its marks",
    "set-aside": "masora circles and stray ink",
    "other": "other words' and lines' ink",
}
# Supplied ink is filled with its colour alone, with no hatching, stipple or dashed or
# dotted outline (decision 26): a supplied mark in decision 15's orange, and restored
# ink in decision 25's teal.  No other layer uses either colour.
SUPPLIED_COLOUR = render.SUPPLIED_COLOUR
SUPPLIED_SWATCH = f"background: {SUPPLIED_COLOUR}"
RESTORED_COLOUR = "#00897b"
RESTORED_SWATCH = f"background: {RESTORED_COLOUR}"
VELLUM_SWATCH = f"background: {rsvg.VELLUM_COLOUR}"
# The ink by region: a palette without decision 15's orange, the restored ink's
# teal or decision 17's slate.
REGION_COLOURS = (
    "#e6194b",
    "#3cb44b",
    "#4363d8",
    "#911eb4",
    "#f032e6",
    "#bcf60c",
    "#9a6324",
    "#800000",
    "#808000",
    "#000075",
    "#fabebe",
    "#ffe119",
)
CUT_COLOUR = "#e91e63"
# (layer, label, on at first, the swatch's style or None)
LAYERS = (
    ("photo", "the photograph", False, None),
    ("black", "the ink, black on white", False, "background: #000"),
    ("meaning", "the ink by meaning", True, None),
    (
        "groups",
        "the ink by group, translucent: ink in two groups shows both colours",
        False,
        None,
    ),
    (
        "regions",
        "the ink by region, each region and overlap in a colour of its own",
        False,
        None,
    ),
    ("supplied", "supplied ink and supplied vellum", True, None),
    (
        "others",
        "other words' and lines' ink",
        True,
        f"background: {OTHER_INK_COLOUR}",
    ),
    (
        "set-aside",
        "masora circles and stray ink",
        True,
        f"background: {MEANING_COLOURS['set-aside']}",
    ),
    ("pieces", "level 1: residual pieces, by judgment", False, None),
    (
        "cuts",
        "the cuts, overlaps' outlines and vellum lines, and every seed",
        False,
        f"background: {CUT_COLOUR}",
    ),
    ("labels", "region and overlap ids", False, None),
)

_CSS = """
.layered select { margin: 0.4em 0 0.2em 0; }
td.hint { color: #444; font-size: 0.9em; }
"""

_ZOOM_JS = """
for (const menu of document.querySelectorAll('.layered select[data-zoom]')) {
  const svg = menu.closest('.layered').querySelector('svg.overlay');
  menu.addEventListener('change', () => {
    const z = Number(menu.value);
    svg.setAttribute('width', Number(svg.dataset.w) * z);
    svg.setAttribute('height', Number(svg.dataset.h) * z);
  });
}
"""


def _e(s):
    return html.escape(str(s), quote=True)


def _swatch(style):
    return f'<span class="swatch" style="{style}"></span>'


def _hide_rules():
    return "\n".join(
        f".hide-{name} .layer-{name} {{ display: none; }}" for name, _, _, _ in LAYERS
    )


def group_meaning(g, me):
    """What a group's ink means on the page: a letter or a mark of the crop's
    subject, ink set aside, or other words' or lines' ink."""
    if g.kind in SET_ASIDE_KINDS:
        return "set-aside"
    if g.ink_of != me:
        return "other"
    return "letter" if g.kind.endswith(" letter") else "mark"


def meaning_of(groups, me):
    """The strongest meaning among the groups that hold a region."""
    found = {group_meaning(g, me) for g in groups}
    return next((m for m in MEANINGS if m in found), "other")


def hide_classes(groups, me):
    """The classes that let a checkbox hide ink: other ink is ink of which no
    group is the subject's, and ink set aside is ink all of whose groups are."""
    out = []
    if all(g.ink_of != me for g in groups):
        out.append("layer-others")
    if all(g.kind in SET_ASIDE_KINDS for g in groups):
        out.append("layer-set-aside")
    return f' class="{" ".join(out)}"' if out else ""


def supplied_ink(s):
    """Supplied ink's added ink, filled with the one colour its kind allows: a
    supplied mark in orange and restored ink in teal (decision 26)."""
    colour = RESTORED_COLOUR if s.supplied == rsvg.RESTORED else SUPPLIED_COLOUR
    return f'<path d="{s.added}" fill="{colour}"/>'


def _kinds(groups):
    return ", ".join(f"{g.id} {g.kind}" for g in groups)


def _inks(rf):
    """Each region's and overlap's id and ink, regions first: an overlap is a
    region that two groups or more hold."""
    return [(r.id, r.d) for r in rf.regions] + [(o.id, o.ink) for o in rf.overlaps]


def _centre(d):
    """The mean of a closed outline's points, where its id is drawn."""
    pts = [p for poly in geo.flatten(geo.parse_path(d)) for p in poly]
    return (sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts))


def _svg(rf, groups_of, zoom):
    w, h = rf.width, rf.height
    me = ssvg.subject(rf)
    inks = _inks(rf)
    outline = dict(inks)
    out = [
        f'<svg class="overlay" width="{geo.fmt(w * zoom, 1)}" height="{geo.fmt(h * zoom, 1)}"'
        f' data-w="{w}" data-h="{h}" viewBox="0 0 {w} {h}"'
        ' xmlns="http://www.w3.org/2000/svg">',
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>',
        f'<image class="layer-photo" href="{_e(rf.image)}" x="0" y="0" width="{w}" height="{h}"/>',
    ]
    out.append('<g class="layer-black">')
    for rid, d in inks:
        gs = groups_of.get(rid, [])
        cls = hide_classes(gs, me)
        fill = OTHER_INK_COLOUR if "layer-others" in cls else "#000"
        out.append(f'<path{cls} fill="{fill}" d="{d}"/>')
    out.append("</g>")
    out.append('<g class="layer-meaning">')
    for rid, d in inks:
        gs = groups_of.get(rid, [])
        colour = MEANING_COLOURS[meaning_of(gs, me)]
        out.append(
            f'<path{hide_classes(gs, me)} fill="{colour}" d="{d}">'
            f"<title>{_e(rid)}: {_e(_kinds(gs))}</title></path>"
        )
    out.append("</g>")
    out.append('<g class="layer-groups" fill-opacity="0.45">')
    k = 0
    for g in rf.groups:
        if g.ink_of == me:
            colour = render.stroke_colour(k)
            k += 1
        else:
            colour = OTHER_INK_COLOUR
        for m in g.members:
            if m in outline:
                out.append(
                    f'<path{hide_classes([g], me)} fill="{colour}" d="{outline[m]}">'
                    f"<title>{_e(g.id)} {_e(g.kind)}: {_e(m)}</title></path>"
                )
    out.append("</g>")
    out.append('<g class="layer-regions" fill-opacity="0.85">')
    k = 0
    for rid, d in inks:
        gs = groups_of.get(rid, [])
        cls = hide_classes(gs, me)
        if "layer-others" in cls:
            colour = OTHER_INK_COLOUR
        else:
            colour = REGION_COLOURS[k % len(REGION_COLOURS)]
            k += 1
        out.append(
            f'<path{cls} fill="{colour}" d="{d}">'
            f"<title>{_e(rid)}: {_e(_kinds(gs))}</title></path>"
        )
    out.append("</g>")
    out.append('<g class="layer-supplied">')
    vellum_ink = rdv.vellum_ink(rf)
    for v in rf.vellum:
        out.append(
            f'<path fill="{rsvg.VELLUM_COLOUR}" d="{vellum_ink.get(v.id, "")}">'
            f"<title>{_e(v.id)}, supplied vellum: {_e(v.why)}</title></path>"
        )
    for s in rf.supplied:
        gs = groups_of.get(s.id, [])
        what = "restored ink" if s.supplied == rsvg.RESTORED else "a supplied mark"
        out.append(
            f"<g{hide_classes(gs, me)}><title>{_e(s.id)}, {what} ({_e(s.supplied)}):"
            f" {_e(_kinds(gs))}. {_e(s.supplied_why)}</title>{supplied_ink(s)}</g>"
        )
    out.append("</g>")
    out.append('<g class="layer-pieces">')
    for p in rf.pieces:
        out.append(
            f'<path fill="{render.JUDGED_COLOURS[p.judged]}" fill-opacity="0.85" d="{p.d}">'
            f"<title>{_e(p.id)}: {_e(p.source)}, judged {_e(p.judged)}</title></path>"
        )
    for f in rf.fills:
        if f.judged not in (None, "ink"):
            out.append(
                f'<path fill="{render.JUDGED_COLOURS[f.judged]}" fill-opacity="0.85" d="{f.d}">'
                f"<title>{_e(f.id)}: a fill judged {_e(f.judged)}</title></path>"
            )
    out.append("</g>")
    out.append('<g class="layer-cuts" fill="none">')
    # Each one thin line, with no white band beneath it, which would read as paper.
    lines = [(c.id, c.note, c.d) for c in rf.cuts]
    lines += [(o.id, o.note, o.outline) for o in rf.overlaps]
    lines += [(v.id, v.why, v.d) for v in rf.vellum]
    for lid, note, d in lines:
        title = f"{lid}: {note}" if note else lid
        out.append(
            f'<path d="{d}" stroke="{CUT_COLOUR}" stroke-width="1.5" stroke-linejoin="round"'
            f' vector-effect="non-scaling-stroke"><title>{_e(title)}</title></path>'
        )
    for r in rf.regions:
        for x, y in r.seeds:
            out.append(
                f'<circle cx="{geo.fmt(x, 2)}" cy="{geo.fmt(y, 2)}" r="{geo.fmt(2.5 / zoom, 2)}"'
                f' fill="#fff" stroke="{CUT_COLOUR}" stroke-width="1.5"'
                f' vector-effect="non-scaling-stroke"><title>a seed of {_e(r.id)}</title></circle>'
            )
    out.append("</g>")
    size = geo.fmt(11 / zoom, 2)
    halo = geo.fmt(3 / zoom, 2)
    out.append(
        f'<g class="layer-labels" font-size="{size}" font-weight="bold" fill="#000"'
        f' stroke="#fff" stroke-width="{halo}" paint-order="stroke">'
    )
    places = [(r.id, r.seeds[0]) for r in rf.regions]
    places += [(o.id, _centre(o.outline)) for o in rf.overlaps]
    for lid, (x, y) in places:
        out.append(f'<text x="{geo.fmt(x, 2)}" y="{geo.fmt(y, 2)}">{_e(lid)}</text>')
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def layer_controls(zoom):
    """The checkboxes that switch one image's layers, with what each layer's colours
    mean, and the menu that sets the image's size."""
    out = ["<fieldset><legend>This image's layers</legend>"]
    for name, label, on, swatch in LAYERS:
        mark = _swatch(swatch) + " " if swatch else ""
        out.append(
            f'<label><input type="checkbox" data-layer="{name}"{" checked" if on else ""}>'
            f" {mark}{_e(label)}</label>"
        )
        if name == "meaning":
            out.append(
                "<p>"
                + " ".join(
                    f"{_swatch('background:' + MEANING_COLOURS[m])} {_e(MEANING_LABELS[m])}"
                    for m in MEANINGS
                )
                + "</p>"
            )
        elif name == "supplied":
            out.append(
                f"<p>{_swatch(SUPPLIED_SWATCH)} a supplied mark"
                f" {_swatch(RESTORED_SWATCH)} restored ink"
                f" {_swatch(VELLUM_SWATCH)} supplied vellum</p>"
            )
        elif name == "set-aside":
            out.append(
                "<p>Faint in the ink by meaning; unchecking either box hides that ink"
                " in every layer.</p>"
            )
        elif name == "pieces":
            out.append(
                "<p>"
                + " ".join(
                    f"{_swatch('background:' + c)} {_e(j)}"
                    for j, c in render.JUDGED_COLOURS.items()
                )
                + "</p>"
            )
    zooms = "".join(
        f'<option value="{z:g}"{" selected" if z == zoom else ""}>{z:g}×</option>'
        for z in ZOOMS
    )
    out.append(f"<label>Size: <select data-zoom>{zooms}</select></label>")
    out.append("</fieldset>")
    return "\n".join(out)


def _section(svg_path):
    rf = rsvg.read(svg_path)
    me = ssvg.subject(rf)
    groups_of = {}
    for g in rf.groups:
        for m in g.members:
            groups_of.setdefault(m, []).append(g)
    zoom = render.scale_of(rf)
    out = [f'<section id="{_e(Path(svg_path).name)}">']
    out.append(f"<h2>{_e(render.title(rf.provenance))}</h2>")
    out.append("<table>")
    out += render.provenance_rows(rf.provenance)
    if "regions-by" in rf.provenance:
        out.append(
            f"<tr><th>Regions</th><td>{_e(rf.provenance['regions-by'])}</td></tr>"
        )
    out.append("</table>")
    out.append('<div class="layered">')
    out.append(f'<div class="scroll">{_svg(rf, groups_of, zoom)}</div>')
    out.append(layer_controls(zoom))
    out.append("</div>")
    seeds = sum(len(r.seeds) for r in rf.regions)
    judged = Counter(p.judged for p in rf.pieces)
    pieces = ", ".join(f"{n} {k}" for k, n in sorted(judged.items())) or "none"
    out.append("<table>")
    out.append(
        f"<tr><th>Threshold</th><td>luminance below {rf.threshold}; specks of up to"
        f" {rf.speck_size} pixels dropped; halo &#177;{rf.halo_band}</td></tr>"
    )
    out.append(
        f"<tr><th>Regions</th><td>{len(rf.regions)}, from {seeds} seeds;"
        f" {len(rf.overlaps)} overlaps; {len(rf.vellum)} strips of supplied vellum;"
        f" {len(rf.cuts)} cuts</td></tr>"
    )
    out.append(f"<tr><th>Groups</th><td>{len(rf.groups)}</td></tr>")
    if rf.supplied:
        kinds = Counter(s.supplied for s in rf.supplied)
        out.append(
            f"<tr><th>Supplied ink</th><td>{len(rf.supplied)}: "
            + _e(", ".join(f"{n} {k}" for k, n in sorted(kinds.items())))
            + "</td></tr>"
        )
    out.append(
        f"<tr><th>Residual pieces</th><td>{len(rf.pieces)}: {_e(pieces)}</td></tr>"
    )
    out.append("</table>")
    out.append(
        "<table><tr><th>Group</th><th>Kind</th><th>Ink of</th><th>Meaning</th>"
        "<th>Regions and supplied ink</th><th>Note</th></tr>"
    )
    for g in rf.groups:
        meaning = group_meaning(g, me)
        out.append(
            f"<tr><td>{_e(g.id)}</td><td>{_e(g.kind)}</td><td>{_e(g.ink_of)}</td>"
            f"<td>{_swatch('background:' + MEANING_COLOURS[meaning])}"
            f" {_e(MEANING_LABELS[meaning])}</td>"
            f"<td>{_e(' '.join(g.members))}</td><td>{_e(g.note)}</td></tr>"
        )
    out.append("</table>")
    if rf.supplied:
        out.append(
            "<table><tr><th>Supplied ink</th><th>Groups</th><th>Supplied</th>"
            "<th>Why</th></tr>"
        )
        for s in rf.supplied:
            swatch = RESTORED_SWATCH if s.supplied == rsvg.RESTORED else SUPPLIED_SWATCH
            out.append(
                f"<tr><td>{_swatch(swatch)} {_e(s.id)}</td>"
                f"<td>{_e(_kinds(groups_of.get(s.id, [])))}</td>"
                f"<td>{_e(s.supplied)}</td><td>{_e(s.supplied_why)}</td></tr>"
            )
        out.append("</table>")
    notes = [(o.id, "overlap", o.note) for o in rf.overlaps]
    notes += [(v.id, "supplied vellum", v.why) for v in rf.vellum]
    notes += [(c.id, "cut", c.note) for c in rf.cuts]
    if notes:
        out.append(
            "<table><tr><th>Overlap, vellum or cut</th><th>Groups</th><th>Note</th></tr>"
        )
        for nid, what, note in notes:
            out.append(
                f"<tr><td>{_e(nid)}, {_e(what)}</td>"
                f"<td>{_e(_kinds(groups_of.get(nid, [])))}</td><td>{_e(note)}</td></tr>"
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
<title>Regions of ink</title>
<style>{render.CSS}{_CSS}{_hide_rules()}
</style>
</head>
<body>
<h1>Regions of ink</h1>
<p class="ai-caveat"><strong>Regions drafted by an AI model, and only partly reviewed by a human so
far.</strong> Claude, an AI model, placed the seeds, cuts, overlaps and strips of supplied
vellum on this page, made the groups, and judged every residual piece of level 1; the regions
come from the seeds by a watershed on the photograph's luminance. Ben has begun to review them:
each place changed from his answers has a note that says so, shown when the pointer rests on it
in the layer of cuts or in the tables. Read the rest as a draft.</p>
<p>Each crop of the Leningrad Codex is drawn with its region-SVG: its ink as regions, one or
more for each sign, each in one group, and overlaps, ink that two signs are proposed to share,
each in two groups or more. The checkboxes beside each image switch that image's layers, and
its menu sets its size. The profile, and what each layer means, are in
<a href="../ink-region-representation.md">doc/ink-region-representation.md</a>; this page
is generated by <code>py/main_pen_stroke.py regions-render</code>.</p>
<p>{_swatch(SUPPLIED_SWATCH)} <strong>Orange: a supplied mark.</strong> The crop shows
little or no ink of it; it is there because the transcription or the layout implies it.
{_swatch(RESTORED_SWATCH)} <strong>Teal: restored ink,</strong> proposed where the image
shows the ink has flaked. {_swatch(VELLUM_SWATCH)} <strong>Tan: supplied vellum,</strong> a
strip of the page between two signs that the photograph's blur joins, taken out of the ink.
None of the three is ever drawn in black or in a group's or a region's colour, and no other
layer uses any of them.</p>
<p>{_swatch(f"background: {OTHER_INK_COLOUR}")} <strong>Slate: ink of another word or
line,</strong> which the crop holds but is not its subject, in every layer; in the ink by
meaning it is a faint tint of slate.</p>
{sections}
<script>{render.LAYER_JS}{_ZOOM_JS}</script>
</body>
</html>
"""


def write_page(svg_paths, out_dir=tools.SNIPS_DIR):
    if not svg_paths:
        raise ValueError("no region-SVGs to render")
    out = Path(out_dir) / PAGE
    text = page(svg_paths)
    with open(out, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(text)
    return out
