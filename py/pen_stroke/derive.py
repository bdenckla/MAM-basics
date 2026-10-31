"""Deriving a stroke-SVG's computed parts from its crop, and checking them.

Authored: the root's provenance and parameters, each stroke's median, widths,
ends, pass, confidence and note, the frame, the groups, and the judgments of
residual pieces and of fills that are not ink.  Derived: the fills, the image
residual, each stroke's ink and shape, and the pen residual.  ``derive``
recomputes the derived parts and carries each judgment over to the piece or
fill with exactly the same pixels; ``problems`` reports every way a file
departs from its crop.
"""

from dataclasses import replace
from pathlib import Path

import numpy as np

from pen_stroke import curve
from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import level3
from pen_stroke import level5
from pen_stroke import raster
from pen_stroke import stroke_svg as ssvg

INK_PLACES = 2
# Pixels by which a re-derived mask may differ from the stored one, for float
# arithmetic that is not bit-identical on every platform.
MASK_TOLERANCE = 2
FILL_TOLERANCE = 0.002


def crop_path(svg_path, sf):
    return Path(svg_path).parent / sf.image


def median_segments(stroke):
    """The stroke's median as cubic segments; a malformed median raises."""
    return curve.segments(geo.parse_path(stroke.median))


def sweep_polys(stroke):
    """The stroke's ink: its median swept with its widths and ends."""
    return curve.ink_pieces(median_segments(stroke), stroke.widths, stroke.ends)


def ink_fill_ds(sf):
    """The fills that are ink: all but those judged otherwise."""
    return [f.d for f in sf.fills if f.judged in (None, "ink")]


def derive(sf, lum):
    """A copy of sf with every derived part recomputed from the crop's luminance."""
    h, w = lum.shape
    if (w, h) != (sf.width, sf.height):
        raise ValueError(f"crop is {w}x{h} but the viewBox is {sf.width}x{sf.height}")
    ink = lum < sf.threshold
    old_fill_judged = {
        _key(level1.fill_mask([f.d], w, h)): f.judged for f in sf.fills if f.judged
    }
    fills = []
    for k, comp in enumerate(level1.trace_fills(ink, sf.speck_size), 1):
        d = geo.format_path(comp, level1.FILL_PLACES)
        judged = old_fill_judged.get(_key(level1.fill_mask([d], w, h)))
        fills.append(ssvg.Fill(f"f{k}", d, judged))
    fills_px = level1.fill_mask([f.d for f in fills], w, h)
    old_piece_judged = {_key(geo.path_mask(p.d, w, h)): p.judged for p in sf.pieces}
    pieces = []
    found, smoothing, halo = level1.image_residual(
        lum, sf.threshold, sf.halo_band, sf.speck_size, fills_px
    )
    for k, (source, mask) in enumerate(found, 1):
        judged = old_piece_judged.get(_key(mask), "unjudged")
        pieces.append(ssvg.Piece(f"r{k}", source, judged, geo.mask_path(mask)))
    out = replace(
        sf,
        fills=fills,
        pieces=pieces,
        smoothing=geo.mask_path(smoothing),
        halo=geo.mask_path(halo),
    )
    strokes = []
    sweeps = []
    for st in sf.strokes:
        polys = sweep_polys(st)
        sweeps.extend(polys)
        shape = level3.shape_class(median_segments(st), st.widths)
        strokes.append(
            replace(st, ink=geo.polygon_path(polys, INK_PLACES), shape=shape)
        )
    out.strokes = strokes
    sweeps_px = geo.rasterize(sweeps, w, h, "nonzero")
    ink_px = level1.fill_mask(ink_fill_ds(out), w, h)
    out.unexplained = geo.mask_path(ink_px & ~sweeps_px)
    out.overshoot = geo.mask_path(sweeps_px & ~ink_px)
    return out


def _key(mask):
    ys, xs = np.nonzero(mask)
    return (mask.shape, ys.tobytes(), xs.tobytes())


def structural_problems(sf):
    """What the authored parts get wrong, whatever the crop."""
    out = []
    ids = (
        [f.id for f in sf.fills]
        + [p.id for p in sf.pieces]
        + [s.id for s in sf.strokes]
    )
    ids += [g.id for g in sf.groups]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        out.append(f"ids used more than once: {dupes}")
    strokes = {s.id: s for s in sf.strokes}
    grouped = set()
    for g in sf.groups:
        if not g.members:
            out.append(f"{g.id}: a group with no strokes")
        pass_name = level5.pass_of(g.kind)
        for m in g.members:
            if m not in strokes:
                out.append(f"{g.id}: refers to {m!r}, which is no stroke of this file")
                continue
            grouped.add(m)
            if strokes[m].pass_name != pass_name:
                out.append(
                    f"{g.id} ({g.kind}) holds {m}, which is in the"
                    f" {strokes[m].pass_name} pass, not the {pass_name} pass"
                )
    for s in sf.strokes:
        if s.id not in grouped:
            out.append(f"{s.id}: in no group")
        try:
            segs = median_segments(s)
            curve.segment_widths(s.widths, len(segs))
            for seg in segs:
                curve.tangent(seg, 0.5)
        except ValueError as exc:
            out.append(f"{s.id}: {exc}")
    for p in sf.pieces:
        if p.judged == "unjudged":
            out.append(f"{p.id}: residual piece not yet judged")
    if sf.frame is None:
        out.append("no frame")
    return out


def problems(svg_path):
    """Every way the stroke-SVG at svg_path departs from the profile and its crop."""
    try:
        sf = ssvg.read(svg_path)
    except ValueError as exc:
        return [str(exc)]
    out = structural_problems(sf)
    png = crop_path(svg_path, sf)
    if not png.exists():
        return out + [f"crop {png.name} does not exist"]
    lum = raster.load_luminance(png)
    try:
        fresh = derive(sf, lum)
    except ValueError as exc:
        return out + [str(exc)]
    w, h = sf.width, sf.height
    if len(sf.fills) != len(fresh.fills):
        out.append(f"{len(sf.fills)} fills where the crop gives {len(fresh.fills)}")
    else:
        for old, new in zip(sf.fills, fresh.fills):
            if old.id != new.id or not _same_numbers(old.d, new.d):
                out.append(f"fill {old.id} is not the tracer's outline")
    old_p = [(p.id, p.source, p.d) for p in sf.pieces]
    new_p = [(p.id, p.source, p.d) for p in fresh.pieces]
    if old_p != new_p:
        out.append("the residual pieces are not those the crop gives")
    for name in ("smoothing", "halo", "unexplained", "overshoot"):
        if _mask_diff(getattr(sf, name), getattr(fresh, name), w, h) > MASK_TOLERANCE:
            out.append(f"the {name} path is not what the crop gives")
    for old, new in zip(sf.strokes, fresh.strokes):
        if _mask_diff(old.ink, new.ink, w, h) > MASK_TOLERANCE:
            out.append(f"{old.id}: its ink is not its median swept with its widths")
        if old.shape != new.shape:
            out.append(
                f"{old.id}: shape {old.shape!r} where its median gives {new.shape!r}"
            )
    return out


def _same_numbers(a, b):
    sa, sb = geo.parse_path(a), geo.parse_path(b)
    if len(sa) != len(sb):
        return False
    for (s0, g0, c0), (s1, g1, c1) in zip(sa, sb):
        if c0 != c1 or len(g0) != len(g1) or [s[0] for s in g0] != [s[0] for s in g1]:
            return False
        pa = [s0] + [p for s in g0 for p in s[1:]]
        pb = [s1] + [p for s in g1 for p in s[1:]]
        if any(
            abs(x0 - x1) > FILL_TOLERANCE or abs(y0 - y1) > FILL_TOLERANCE
            for (x0, y0), (x1, y1) in zip(pa, pb)
        ):
            return False
    return True


def _mask_diff(d0, d1, w, h):
    return int((geo.path_mask(d0, w, h) ^ geo.path_mask(d1, w, h)).sum())
