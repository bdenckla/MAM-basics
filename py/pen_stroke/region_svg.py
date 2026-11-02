"""Reading and writing a region-SVG under the ink-region profile.

A region-SVG describes a crop's ink as regions, under the profile in
doc/ink-region-representation.md: level 1, the ink as filled outlines with the
image residual, exactly as a stroke-SVG has it; strips of supplied vellum,
authored lines that take the ink they cross out of it; cuts, authored paths of
straight segments that correct where the regions meet; regions, each an
authored id and one seed point or more, whose outline is derived; overlaps,
authored outlines of ink that two signs are proposed to share, whose ink is
derived; supplied ink, authored outlines of ink the crop does not show, whose
added ink is derived; and groups, as a stroke-SVG has them, holding regions,
overlaps and supplied ink in place of strokes.  Profile 3 adds glyphs: for each
written part of each fitted group, a glyph of the library
(pen_stroke.glyph_library) and the fit's parameters, which only the fit writes,
with its placed outline and its ink derived; and the overlaps of glyphs, whose
ink is derived.  The reader accepts profiles 2 and 3, their elements, classes
and attributes and nothing else, as pen_stroke.stroke_svg's does, and the writer
always writes the same text for the same content.
"""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import stroke_svg as ssvg

PROFILE = "ink-region 2"
# Profile 3: regions from fitted glyphs, its derivation beginning with profile 2's.
PROFILE_3 = "ink-region 3"
PROFILES = (PROFILE, PROFILE_3)
SUFFIX = ".regions.svg"
_SVG = "http://www.w3.org/2000/svg"
# The provenance on the root, in the order it is written: the stroke-SVG's, with who
# drew the cuts and seeds and made the groups in place of who traced the strokes.
PROVENANCE_KEYS = tuple(k for k in ssvg.PROVENANCE_KEYS if k != "strokes-by") + (
    "regions-by",
)
# Supplied ink (decision 15): ink the crop shows none of, or only faint traces of; and
# restored ink, where the image shows the ink has flaked (decision 25).
RESTORED = "flaked"
SUPPLIED = ssvg.SUPPLIED + (RESTORED,)
# A region's id is rg and a number: removed samples go back to the region of lowest
# number (pen_stroke.region_derive), and the residual pieces already use r.
REGION_ID = re.compile(r"rg([1-9][0-9]*)")
GLYPH_ID = re.compile(r"gl([1-9][0-9]*)")
GROUP_ID = re.compile(r"g([1-9][0-9]*)")
SEED_PLACES = 2
# A group of another word or line is fitted when it says so (profile 3).
FIT_YES = "yes"
# A glyph's data-fit, each number to this many decimals.
FIT_PLACES = 4
# A strip of supplied vellum is 1 pixel wide unless its data-width says otherwise.
VELLUM_WIDTH = 1.0
WIDTH_PLACES = 2
# Supplied vellum is drawn in this colour alone (decision 26), which no other layer
# of the region page uses.
VELLUM_COLOUR = "#e6cf9c"

STYLE = f"""
.fills, .image-residual, .groups {{ display: none }}
.region path {{ fill: #c0392b; fill-opacity: 0.4 }}
.overlap .ink {{ fill: #7d3c98; fill-opacity: 0.6 }}
.overlap .outline {{ fill: none; stroke: #7d3c98; stroke-width: 0.3 }}
.cut {{ fill: none; stroke: #1f618d; stroke-width: 0.5 }}
.vellum {{ fill: none; stroke: {VELLUM_COLOUR} }}
.supplied-ink .outline {{ display: none }}
.supplied-ink .added {{ fill: #ff6d00 }}
.supplied-ink[data-supplied="flaked"] .added {{ fill: #00897b }}
"""
# Profile 3's additions to the file's own style: each glyph's ink, its outline thin,
# and the overlaps of glyphs.
STYLE_3 = """.glyph .ink { fill: #1f618d; fill-opacity: 0.5 }
.glyph .outline { fill: none; stroke: #555; stroke-width: 0.2 }
.glyph-overlap { fill: #7d3c98; fill-opacity: 0.6 }
"""


@dataclass
class Vellum:
    id: str
    d: str
    why: str
    width: float = VELLUM_WIDTH


@dataclass
class Cut:
    id: str
    d: str
    note: str = ""


@dataclass
class Region:
    id: str
    # One seed or more, each (x, y) in crop pixels.
    seeds: tuple
    # Derived: the outline of the region's ink.
    d: str = ""


@dataclass
class Overlap:
    id: str
    outline: str
    note: str = ""
    # Derived: the ink inside the outline.
    ink: str = ""


@dataclass
class SuppliedInk:
    id: str
    supplied: str
    supplied_why: str
    outline: str
    # Derived: the outline less the ink the image shows.
    added: str = ""


@dataclass
class Glyph:
    id: str
    # Its group's id, and its written part: empty for a sign of one part.
    group: str
    part: str
    # Its glyph-source's id in the library.
    glyph: str
    # The fit's parameters: a move, two scales, a turn and a shear, and for a
    # letter a warp of 18 numbers (pen_stroke.glyph_fit).
    fit: tuple
    # Derived: the library's glyph placed by the parameters, and its ink.
    outline: str = ""
    ink: str = ""


@dataclass
class GlyphOverlap:
    id: str
    # The glyphs inside each of which some of its ink lies deep.
    glyphs: tuple
    # Derived: its ink.
    d: str = ""


@dataclass
class RegionFile:
    width: int
    height: int
    image: str
    provenance: dict
    threshold: int
    speck_size: int
    halo_band: int
    tracer: str = level1.TRACER
    profile: str = PROFILE
    fills: list = field(default_factory=list)
    pieces: list = field(default_factory=list)
    smoothing: str = ""
    halo: str = ""
    vellum: list = field(default_factory=list)
    cuts: list = field(default_factory=list)
    regions: list = field(default_factory=list)
    overlaps: list = field(default_factory=list)
    supplied: list = field(default_factory=list)
    glyphs: list = field(default_factory=list)
    glyph_overlaps: list = field(default_factory=list)
    groups: list = field(default_factory=list)


def all_svgs(directory):
    return sorted(Path(directory).glob("*" + SUFFIX))


def region_number(rid):
    """The number in a region's id."""
    m = REGION_ID.fullmatch(rid)
    if not m:
        raise ssvg.ProfileError(f"{rid}: a region's id is rg and a number")
    return int(m.group(1))


def glyph_number(gid):
    """The number in a glyph's id."""
    m = GLYPH_ID.fullmatch(gid)
    if not m:
        raise ssvg.ProfileError(f"{gid}: a glyph's id is gl and a number")
    return int(m.group(1))


def group_number(gid):
    """The number in a group's id, or None for an id not g and a number."""
    m = GROUP_ID.fullmatch(gid)
    return int(m.group(1)) if m else None


def owners(rf):
    """Each region's, overlap's and supplied ink's ink-of values, from the groups
    that hold it."""
    return ssvg.ink_of_strokes(rf)


def other_ink_ids(rf):
    """The ids of the regions, overlaps and supplied ink of which no group is the
    crop's subject's."""
    me = ssvg.subject(rf)
    held = owners(rf)
    ids = [r.id for r in rf.regions] + [o.id for o in rf.overlaps]
    ids += [s.id for s in rf.supplied]
    return [i for i in ids if me not in held.get(i, {me})]


def style(rf):
    """The region-SVG's own style: STYLE, each strip of vellum its width, and the
    regions and overlaps of other ink in their own colour (decision 17)."""
    out = STYLE
    for v in rf.vellum:
        out += f"#{v.id} {{ stroke-width: {geo.fmt(v.width, WIDTH_PLACES)} }}\n"
    supplied = {s.id for s in rf.supplied}
    overlaps = {o.id for o in rf.overlaps}
    others = [i for i in other_ink_ids(rf) if i not in supplied]
    if others:
        sel = ", ".join(f"#{i} .ink" if i in overlaps else f"#{i} path" for i in others)
        out += f"{sel} {{ fill: {ssvg.OTHER_INK_COLOUR}; fill-opacity: 0.55 }}\n"
    if rf.profile == PROFILE_3:
        out += STYLE_3
    return out


def read(path):
    """The region-SVG at path, checked against the profile's structure."""
    root = ET.parse(path).getroot()
    if ssvg.svg_tag(root) != "svg":
        raise ssvg.ProfileError(f"{path}: root is not svg")
    allowed = {"viewBox", "width", "height", "version", "data-profile", "data-channel"}
    allowed |= {f"data-{k}" for k in PROVENANCE_KEYS}
    allowed |= {"data-threshold", "data-speck-size", "data-halo-band", "data-tracer"}
    a = ssvg.profile_attrs(root, "root", allowed)
    if a.get("data-profile") not in PROFILES:
        raise ssvg.ProfileError(
            f"{path}: data-profile is not one of {', '.join(map(repr, PROFILES))}"
        )
    if a.get("data-channel") != "luminance":
        raise ssvg.ProfileError(f"{path}: data-channel is not 'luminance'")
    vb = [float(v) for v in ssvg.require(a, "viewBox", "root").split()]
    if vb[:2] != [0, 0] or vb[2] != int(vb[2]) or vb[3] != int(vb[3]):
        raise ssvg.ProfileError(
            f"{path}: viewBox must be 0 0 <width> <height> in whole pixels"
        )
    rf = RegionFile(
        width=int(vb[2]),
        height=int(vb[3]),
        image="",
        provenance={k: a[f"data-{k}"] for k in PROVENANCE_KEYS if f"data-{k}" in a},
        threshold=int(ssvg.require(a, "data-threshold", "root")),
        speck_size=int(ssvg.require(a, "data-speck-size", "root")),
        halo_band=int(ssvg.require(a, "data-halo-band", "root")),
        tracer=ssvg.require(a, "data-tracer", "root"),
        profile=a["data-profile"],
    )
    third = rf.profile == PROFILE_3
    seen = []
    for tag, el in ssvg.svg_children(root):
        cls = el.attrib.get("class", "")
        key = f"{tag}.{cls}" if cls else tag
        seen.append(key)
        if key == "style":
            continue
        if key == "image.crop":
            ia = ssvg.profile_attrs(
                el, "image", {"class", "href", "x", "y", "width", "height"}
            )
            rf.image = ssvg.require(ia, "href", "image")
        elif key == "g.fills":
            ssvg.read_fills(el, rf)
        elif key == "g.image-residual":
            ssvg.read_image_residual(el, rf)
        elif key == "g.vellum":
            _read_vellum(el, rf)
        elif key == "g.cuts":
            _read_cuts(el, rf)
        elif key == "g.regions":
            _read_regions(el, rf)
        elif key == "g.overlaps":
            _read_overlaps(el, rf)
        elif key == "g.supplied":
            _read_supplied(el, rf)
        elif key == "g.glyphs" and third:
            _read_glyphs(el, rf)
        elif key == "g.glyph-overlaps" and third:
            _read_glyph_overlaps(el, rf)
        elif key == "g.groups":
            ssvg.read_groups(el, rf, parts_notes=True, fit_flags=True)
        else:
            raise ssvg.ProfileError(
                f"{path}: element {key!r} is not in profile {rf.profile!r}"
            )
    needed = [
        "image.crop",
        "g.fills",
        "g.image-residual",
        "g.vellum",
        "g.cuts",
        "g.regions",
        "g.overlaps",
        "g.supplied",
        "g.groups",
    ]
    if third:
        needed += ["g.glyphs", "g.glyph-overlaps"]
    for key in needed:
        if key not in seen:
            raise ssvg.ProfileError(f"{path}: missing {key}")
    for g in rf.groups:
        if g.fit not in ("", FIT_YES):
            raise ssvg.ProfileError(f"{g.id}: data-fit is {FIT_YES!r} or absent")
    return rf


def _read_vellum(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "path" or el.attrib.get("class") != "vellum":
            raise ssvg.ProfileError("vellum: every child is a path.vellum")
        a = ssvg.profile_attrs(
            el, "vellum", {"class", "id", "d", "data-width", "data-why", "style"}
        )
        vid = ssvg.require(a, "id", "vellum")
        why = ssvg.require(a, "data-why", vid)
        if not why:
            raise ssvg.ProfileError(f"{vid}: data-why says nothing")
        try:
            width = float(a.get("data-width", VELLUM_WIDTH))
        except ValueError as exc:
            raise ssvg.ProfileError(f"{vid}: data-width is a number") from exc
        if not width > 0:
            raise ssvg.ProfileError(f"{vid}: data-width is more than 0")
        rf.vellum.append(Vellum(vid, ssvg.require(a, "d", vid), why, width))


def _read_cuts(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "path" or el.attrib.get("class") != "cut":
            raise ssvg.ProfileError("cuts: every child is a path.cut")
        # A vector editor gives every path a style; it means nothing here.
        a = ssvg.profile_attrs(el, "cut", {"class", "id", "d", "data-note", "style"})
        cid = ssvg.require(a, "id", "cut")
        rf.cuts.append(Cut(cid, ssvg.require(a, "d", cid), a.get("data-note", "")))


def _read_regions(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "g" or el.attrib.get("class") != "region":
            raise ssvg.ProfileError("regions: every child is a g.region")
        a = ssvg.profile_attrs(el, "region", {"class", "id", "data-seed"})
        rid = ssvg.require(a, "id", "region")
        region_number(rid)
        try:
            nums = [float(v) for v in ssvg.require(a, "data-seed", rid).split()]
        except ValueError as exc:
            raise ssvg.ProfileError(f"{rid}: data-seed is numbers") from exc
        if not nums or len(nums) % 2:
            raise ssvg.ProfileError(
                f"{rid}: data-seed is one point or more, each x and y"
            )
        seeds = tuple(zip(nums[0::2], nums[1::2]))
        paths = []
        for ctag, child in ssvg.svg_children(el):
            if ctag != "path" or "class" in child.attrib:
                raise ssvg.ProfileError(f"{rid}: its one child is a path, its outline")
            ca = ssvg.profile_attrs(child, f"{rid} path", {"d", "id", "style"})
            paths.append(ca.get("d", ""))
        if len(paths) > 1:
            raise ssvg.ProfileError(f"{rid}: its one child is a path, its outline")
        rf.regions.append(Region(rid, seeds, paths[0] if paths else ""))


def _read_overlaps(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "g" or el.attrib.get("class") != "overlap":
            raise ssvg.ProfileError("overlaps: every child is a g.overlap")
        a = ssvg.profile_attrs(el, "overlap", {"class", "id", "data-note"})
        oid = ssvg.require(a, "id", "overlap")
        parts = _parts(el, oid, ("outline", "ink"))
        if not parts.get("outline"):
            raise ssvg.ProfileError(f"{oid}: no outline")
        rf.overlaps.append(
            Overlap(oid, parts["outline"], a.get("data-note", ""), parts.get("ink", ""))
        )


def _parts(el, where, classes):
    """The path data of an element's children, one path of each class given."""
    parts = {}
    for ctag, child in ssvg.svg_children(el):
        cls = child.attrib.get("class", "")
        if ctag != "path" or cls not in classes or cls in parts:
            raise ssvg.ProfileError(
                f"{where}: its children are "
                + " and ".join(f"one path.{c}" for c in classes)
            )
        ca = ssvg.profile_attrs(child, f"{where} {cls}", {"class", "d", "id", "style"})
        parts[cls] = ca.get("d", "")
    return parts


def _read_supplied(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "g" or el.attrib.get("class") != "supplied-ink":
            raise ssvg.ProfileError("supplied: every child is a g.supplied-ink")
        a = ssvg.profile_attrs(
            el, "supplied-ink", {"class", "id", "data-supplied", "data-supplied-why"}
        )
        sid = ssvg.require(a, "id", "supplied-ink")
        supplied = ssvg.require(a, "data-supplied", sid)
        if supplied not in SUPPLIED:
            raise ssvg.ProfileError(f"{sid}: unknown data-supplied {supplied!r}")
        why = ssvg.require(a, "data-supplied-why", sid)
        if not why:
            raise ssvg.ProfileError(f"{sid}: data-supplied-why says nothing")
        parts = _parts(el, sid, ("outline", "added"))
        if not parts.get("outline"):
            raise ssvg.ProfileError(f"{sid}: no outline")
        rf.supplied.append(
            SuppliedInk(sid, supplied, why, parts["outline"], parts.get("added", ""))
        )


def _read_glyphs(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "g" or el.attrib.get("class") != "glyph":
            raise ssvg.ProfileError("glyphs: every child is a g.glyph")
        a = ssvg.profile_attrs(
            el,
            "glyph",
            {"class", "id", "data-group", "data-part", "data-glyph", "data-fit"},
        )
        gid = ssvg.require(a, "id", "glyph")
        glyph_number(gid)
        try:
            fit = tuple(float(v) for v in ssvg.require(a, "data-fit", gid).split())
        except ValueError as exc:
            raise ssvg.ProfileError(f"{gid}: data-fit is numbers") from exc
        parts = _parts(el, gid, ("outline", "ink"))
        rf.glyphs.append(
            Glyph(
                gid,
                ssvg.require(a, "data-group", gid),
                a.get("data-part", ""),
                ssvg.require(a, "data-glyph", gid),
                fit,
                parts.get("outline", ""),
                parts.get("ink", ""),
            )
        )


def _read_glyph_overlaps(g, rf):
    for tag, el in ssvg.svg_children(g):
        if tag != "path" or el.attrib.get("class") != "glyph-overlap":
            raise ssvg.ProfileError(
                "glyph-overlaps: every child is a path.glyph-overlap"
            )
        a = ssvg.profile_attrs(el, "glyph-overlap", {"class", "id", "data-glyphs", "d"})
        oid = ssvg.require(a, "id", "glyph-overlap")
        glyphs = tuple(ssvg.require(a, "data-glyphs", oid).split())
        rf.glyph_overlaps.append(GlyphOverlap(oid, glyphs, a.get("d", "")))


def fit_text(fit):
    """A glyph's data-fit as the profile writes it."""
    return " ".join(geo.fmt(v, FIT_PLACES) for v in fit)


def dumps(rf):
    """The region-SVG's text: the same content always gives the same text."""
    root = [
        f'xmlns="{_SVG}"',
        f'viewBox="0 0 {rf.width} {rf.height}"',
        f'width="{rf.width}"',
        f'height="{rf.height}"',
        f'data-profile="{rf.profile}"',
    ]
    for k in PROVENANCE_KEYS:
        if k in rf.provenance:
            root.append(f'data-{k}="{ssvg.esc(rf.provenance[k])}"')
    root += [
        'data-channel="luminance"',
        f'data-threshold="{rf.threshold}"',
        f'data-speck-size="{rf.speck_size}"',
        f'data-halo-band="{rf.halo_band}"',
        f'data-tracer="{ssvg.esc(rf.tracer)}"',
    ]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<svg " + "\n     ".join(root) + ">",
    ]
    lines.append(f"  <style>{style(rf)}  </style>")
    lines.append(
        f'  <image class="crop" href="{ssvg.esc(rf.image)}" x="0" y="0"'
        f' width="{rf.width}" height="{rf.height}"/>'
    )
    lines += ssvg.level1_lines(rf)
    lines.append('  <g class="vellum">')
    for v in rf.vellum:
        width = ""
        if v.width != VELLUM_WIDTH:
            width = f' data-width="{geo.fmt(v.width, WIDTH_PLACES)}"'
        lines.append(
            f'    <path class="vellum" id="{v.id}"{width}'
            f' data-why="{ssvg.esc(v.why)}" d="{v.d}"/>'
        )
    lines.append("  </g>")
    lines.append('  <g class="cuts">')
    for c in rf.cuts:
        note = f' data-note="{ssvg.esc(c.note)}"' if c.note else ""
        lines.append(f'    <path class="cut" id="{c.id}"{note} d="{c.d}"/>')
    lines.append("  </g>")
    lines.append('  <g class="regions">')
    for r in rf.regions:
        lines.append(
            f'    <g class="region" id="{r.id}" data-seed="{seeds_text(r.seeds)}">'
        )
        lines.append(f'      <path d="{r.d}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    lines.append('  <g class="overlaps">')
    for o in rf.overlaps:
        note = f' data-note="{ssvg.esc(o.note)}"' if o.note else ""
        lines.append(f'    <g class="overlap" id="{o.id}"{note}>')
        lines.append(f'      <path class="outline" d="{o.outline}"/>')
        lines.append(f'      <path class="ink" d="{o.ink}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    lines.append('  <g class="supplied">')
    for s in rf.supplied:
        lines.append(
            f'    <g class="supplied-ink" id="{s.id}" data-supplied="{s.supplied}"'
            f' data-supplied-why="{ssvg.esc(s.supplied_why)}">'
        )
        lines.append(f'      <path class="outline" d="{s.outline}"/>')
        lines.append(f'      <path class="added" d="{s.added}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    if rf.profile == PROFILE_3:
        lines.append('  <g class="glyphs">')
        for gl in rf.glyphs:
            part = f' data-part="{ssvg.esc(gl.part)}"' if gl.part else ""
            lines.append(
                f'    <g class="glyph" id="{gl.id}" data-group="{gl.group}"{part}'
                f' data-glyph="{gl.glyph}" data-fit="{fit_text(gl.fit)}">'
            )
            lines.append(f'      <path class="outline" d="{gl.outline}"/>')
            lines.append(f'      <path class="ink" d="{gl.ink}"/>')
            lines.append("    </g>")
        lines.append("  </g>")
        lines.append('  <g class="glyph-overlaps">')
        for o in rf.glyph_overlaps:
            lines.append(
                f'    <path class="glyph-overlap" id="{o.id}"'
                f' data-glyphs="{" ".join(o.glyphs)}" d="{o.d}"/>'
            )
        lines.append("  </g>")
    lines += ssvg.group_lines(rf.groups)
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def seeds_text(seeds):
    """A region's seeds as the profile writes them: x and y in crop pixels, for
    each seed."""
    return " ".join(
        f"{geo.fmt(x, SEED_PLACES)} {geo.fmt(y, SEED_PLACES)}" for x, y in seeds
    )


def write(rf, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(dumps(rf))
