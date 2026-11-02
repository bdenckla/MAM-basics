"""The library of glyphs that a fitted word places on a crop's ink.

doc/pen-stroke-snips/glyphs.svg is the font that the ink-region work evolves,
under the profile in doc/ink-region-representation.md, "The library of glyphs":
one glyph-source for each glyph, of a kind of pen_stroke.level5 and one of its
written parts, of two sorts.  A glyph of the scribe's, whose data-from names a
crop and a group, is the ink that the draft of that crop's region-SVG gives the
group's regions, traced as a region is, in that crop's pixels, y down; its
outline is derived (pen_stroke.region_derive).  A glyph of Taamey D's, whose
data-from names Taamey D and a character's Unicode name, is the outline to which
Taamey-D/font-m-TaD/Taamey_D.ttf maps that character, flattened, in font units,
y up; these are copied into the library only when ``copy_taamey_d`` is asked
for, with the font file's SHA-256, so that a new build of the font changes
nothing here until then.  Nothing under Taamey-D/ is written.

GLYPHS, a closed table keyed by every kind of pen_stroke.level5, gives each
kind's written parts, each part's name and Taamey D's character for it, and how
a group's regions are matched to its parts; or says that the kind is not
fitted, and why.  The module raises if the table's counts and level5.PARTS
disagree.
"""

import hashlib
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

from pen_stroke import geometry as geo
from pen_stroke import level5
from pen_stroke import stroke_svg as ssvg

PROFILE = "glyph-library 1"
LIBRARY = "glyphs.svg"
_SVG = "http://www.w3.org/2000/svg"
TAAMEY_D = "Taamey D"
TAAMEY_D_FONT = Path("Taamey-D") / "font-m-TaD" / "Taamey_D.ttf"
# Each quadratic or cubic piece of Taamey D's outlines is cut into this many
# straight segments, as the trial of 2026-11-01 cut them.
CURVE_STEPS = 8
# Taamey D's points, so flattened, are multiples of 1/128 of a font unit, which
# this many decimals write exactly; copy_taamey_d raises on any that is not.
FONT_PLACES = 7
OUTLINE_PLACES = 3
# How the library shows itself when opened: Taamey D's font units and the scribe's
# crop pixels at about the same size, each glyph in a cell of its own.
TAAMEY_D_SHOW_SCALE = 0.05
SHOW_COLUMNS = 10
SHOW_MARGIN = 6
LABEL_SIZE = 2.5

# How a group's regions are matched to its kind's written parts, in the table's
# order: by the mean row of each region's ink, or by its mean column from the
# right, or the leftmost region first and the rest by mean row.
TOP_TO_BOTTOM = "top to bottom"
RIGHT_TO_LEFT = "right to left"
BAR_AT_LEFT = "the bar at the left, then top to bottom"
ORDERS = (TOP_TO_BOTTOM, RIGHT_TO_LEFT, BAR_AT_LEFT)

_HIRIQ = "HEBREW POINT HIRIQ"
_PATAH = "HEBREW POINT PATAH"
_GERESH = "HEBREW ACCENT GERESH"


@dataclass(frozen=True)
class Part:
    # Empty for a sign of one part.
    name: str
    # The Unicode name of Taamey D's character for the part, or None where Taamey D
    # has none.
    char: str | None


@dataclass(frozen=True)
class Entry:
    parts: tuple = ()
    order: str = TOP_TO_BOTTOM
    # Why a kind is not fitted; empty for a fitted kind.
    unfitted: str = ""

    @property
    def fitted(self):
        return not self.unfitted


def _one(char):
    return Entry((Part("", char),))


def _dots(*names, order=TOP_TO_BOTTOM):
    return Entry(tuple(Part(n, _HIRIQ) for n in names), order)


# A bar is Taamey D's patax and a dot its xiriq, so a qamats is a patax over a
# xiriq, as this manuscript writes it, and a segol three xiriq dots.
_MARK_GLYPHS = {
    "sheva mark": _dots("top dot", "bottom dot"),
    "ḥiriq vowel": _one(_HIRIQ),
    "tsere vowel": _dots("right dot", "left dot", order=RIGHT_TO_LEFT),
    # Two dots above and one below, between them.
    "segol vowel": _dots("right dot", "lower dot", "left dot", order=RIGHT_TO_LEFT),
    "pataḥ vowel": _one(_PATAH),
    "qamats vowel": Entry((Part("bar", _PATAH), Part("dot", _HIRIQ))),
    "ḥolam dot": _one("HEBREW POINT HOLAM"),
    "qubuts vowel": _dots("top dot", "middle dot", "bottom dot"),
    # A bar and, to its right, the two dots of a sheva, as page F043A's line 4 writes
    # the only one in the six crops.
    "ḥataf pataḥ vowel": Entry(
        (Part("bar", _PATAH), Part("top dot", _HIRIQ), Part("bottom dot", _HIRIQ)),
        BAR_AT_LEFT,
    ),
    "dagesh mark": _one("HEBREW POINT DAGESH OR MAPIQ"),
    "shuruq dot": _one("HEBREW POINT DAGESH OR MAPIQ"),
    "shin dot": _one("HEBREW POINT SHIN DOT"),
    "sin dot": _one("HEBREW POINT SIN DOT"),
    "meteg mark": _one("HEBREW POINT METEG"),
    "silluq accent": _one("HEBREW POINT METEG"),
    "maqaf mark": _one("HEBREW PUNCTUATION MAQAF"),
    "sof pasuq mark": _dots("top dot", "bottom dot"),
    "paseq mark": _one("HEBREW PUNCTUATION PASEQ"),
    "atnaḥ accent": _one("HEBREW ACCENT ETNAHTA"),
    "revia accent": _one("HEBREW ACCENT REVIA"),
    "geresh accent": _one(_GERESH),
    "gershayim accent": Entry(
        (Part("right stroke", _GERESH), Part("left stroke", _GERESH)), RIGHT_TO_LEFT
    ),
    "darga accent": _one("HEBREW ACCENT DARGA"),
    "pashta accent": _one("HEBREW ACCENT PASHTA"),
    "qadma accent": _one("HEBREW ACCENT QADMA"),
    "tevir accent": Entry(
        (Part("stroke", None), Part("dot", _HIRIQ)),
        RIGHT_TO_LEFT,
        "Taamey D has no character for a tevir's stroke alone",
    ),
    "tipeḥa accent": _one("HEBREW ACCENT TIPEHA"),
    "munaḥ accent": _one("HEBREW ACCENT MUNAH"),
    "merkha accent": _one("HEBREW ACCENT MERKHA"),
    "mahapakh accent": _one("HEBREW ACCENT MAHAPAKH"),
    "zaqef accent": _dots("top dot", "bottom dot"),
    "masora circle mark": Entry(unfitted="a masora circle is ink set aside"),
    "bar under the letter": _one(_PATAH),
    "bar over the letter": _one(_PATAH),
    "dot under the letter": _one(_HIRIQ),
    "dot over the letter": _one(_HIRIQ),
    "unidentified mark": Entry(unfitted="it leaves the mark undetermined"),
    "stray mark": Entry(unfitted="stray ink is set aside"),
}

GLYPHS = {
    kind: _one(uni)
    for kind, (uni, nib) in level5.KINDS.items()
    if nib == level5.LETTERS and uni is not None
}
GLYPHS["unidentified letter"] = Entry(unfitted="it leaves the letter undetermined")
GLYPHS.update(_MARK_GLYPHS)


def _table_problems():
    """Where the table and level5's kinds and parts disagree."""
    out = []
    if set(GLYPHS) != set(level5.KINDS):
        out.append("the table of glyphs and the kinds disagree")
    for kind, entry in GLYPHS.items():
        if entry.order not in ORDERS:
            out.append(f"{kind}: unknown order {entry.order!r}")
        count = level5.PARTS.get(kind)
        if count is None:
            want = 1 if entry.fitted else 0
        else:
            want = count
        if len(entry.parts) != want:
            out.append(
                f"{kind}: the table gives {len(entry.parts)} written parts, the parts"
                f" rule {count}"
            )
        names = [p.name for p in entry.parts]
        if len(set(names)) != len(names) or (len(names) > 1 and "" in names):
            out.append(f"{kind}: its parts' names are not distinct")
        if entry.fitted and any(p.char is None for p in entry.parts):
            out.append(f"{kind}: a fitted kind whose part has no character")
        for p in entry.parts:
            if p.char is not None:
                unicodedata.lookup(p.char)
    return out


TABLE_PROBLEMS = _table_problems()
if TABLE_PROBLEMS:
    raise ValueError("; ".join(TABLE_PROBLEMS))


def entry_of(kind):
    """The table's entry for a kind; an unknown kind raises."""
    if kind not in GLYPHS:
        raise ValueError(f"unknown kind {kind!r}")
    return GLYPHS[kind]


def slug(text):
    """ASCII for an id: lower case, ḥ as h, every other run of non-letters a hyphen."""
    text = text.lower().replace("ḥ", "h")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def taamey_d_id(kind, part):
    return "taamey-d-" + slug(kind) + (f"-{slug(part)}" if part else "")


def taamey_d_source(char):
    return f"{TAAMEY_D} {char}"


@dataclass
class GlyphSource:
    id: str
    kind: str
    # Empty for a sign of one part.
    part: str
    # "Taamey D <Unicode name>", or "<crop> <group>" for a glyph of the scribe's.
    source: str
    # Path data: crop pixels, y down, for the scribe's; font units, y up, for Taamey
    # D's.  The scribe's is derived.
    outline: str = ""
    # Why a letter of the scribe's serves though it is not clean: its ink touches
    # another group's ink.
    clean_note: str = ""

    @property
    def is_taamey_d(self):
        return self.source.startswith(TAAMEY_D + " ")

    def scribe_source(self):
        """The crop's stem and the group's id of a glyph of the scribe's."""
        crop, sep, gid = self.source.rpartition(" ")
        if self.is_taamey_d or not sep or not crop or " " in crop:
            raise ValueError(f"{self.id}: data-from is not a crop and a group")
        return crop, gid


@dataclass
class Library:
    sources: list = field(default_factory=list)
    taamey_d_sha256: str = ""

    def by_id(self):
        return {s.id: s for s in self.sources}

    def default_for(self, kind, part):
        """The glyph a new glyph of this kind and part takes: the first of the
        scribe's, in the library's order, or else Taamey D's."""
        own = [
            s
            for s in self.sources
            if s.kind == kind and s.part == part and not s.is_taamey_d
        ]
        if own:
            return own[0]
        tid = taamey_d_id(kind, part)
        for s in self.sources:
            if s.id == tid:
                return s
        raise ValueError(f"the library has no glyph for {kind!r}, part {part!r}")


def library_path(snips_dir):
    return Path(snips_dir) / LIBRARY


def contours(src):
    """The glyph-source's contours as arrays of points, y up, as a font's are: Taamey
    D's as the library has them, and the scribe's flattened and turned over, as the
    trial of 2026-11-01 took them."""
    polys = geo.flatten(geo.parse_path(src.outline))
    if src.is_taamey_d:
        return [np.array(p, dtype=float) for p in polys]
    return [np.array([(x, -y) for x, y in p], dtype=float) for p in polys]


class _FlatPen(BasePen):
    """Contours as polylines, each quadratic and cubic piece cut into CURVE_STEPS
    straight segments."""

    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.contours = []
        self.cur = None

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for k in range(1, CURVE_STEPS + 1):
            t = k / CURVE_STEPS
            a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
            self.cur.append(
                (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])
            )

    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for k in range(1, CURVE_STEPS + 1):
            t = k / CURVE_STEPS
            a, b = (1 - t) ** 3, 3 * (1 - t) ** 2 * t
            c, e = 3 * (1 - t) * t * t, t**3
            self.cur.append(
                (
                    a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1],
                )
            )

    def _closePath(self):
        if len(self.cur) > 1 and self.cur[0] == self.cur[-1]:
            self.cur.pop()
        self.contours.append([(float(x), float(y)) for x, y in self.cur])
        self.cur = None

    _endPath = _closePath


def _exact(v):
    s = geo.fmt(v, FONT_PLACES)
    if float(s) != v:
        raise ValueError(f"Taamey D's point {v!r} is not exact in {FONT_PLACES} places")
    return s


def font_outline(font, char):
    """Path data, in font units, y up, for the glyph to which the font maps the
    character named, flattened."""
    cmap = font.getBestCmap()
    cp = ord(unicodedata.lookup(char))
    if cp not in cmap:
        raise ValueError(f"Taamey D has no glyph for {char}")
    pen = _FlatPen(font.getGlyphSet())
    font.getGlyphSet()[cmap[cp]].draw(pen)
    out = []
    for c in pen.contours:
        pts = [f"{_exact(x)} {_exact(y)}" for x, y in c]
        out.append("M" + " L".join(pts) + " Z")
    return " ".join(out)


def copy_taamey_d(lib, font_path):
    """A copy of the library whose glyphs of Taamey D's are copied afresh from the
    font, one for each written part of each kind the table fits, after the
    scribe's, in the table's order; and the font file's SHA-256."""
    data = Path(font_path).read_bytes()
    font = TTFont(font_path)
    sources = [s for s in lib.sources if not s.is_taamey_d]
    for kind, entry in GLYPHS.items():
        if not entry.fitted:
            continue
        for p in entry.parts:
            sources.append(
                GlyphSource(
                    taamey_d_id(kind, p.name),
                    kind,
                    p.name,
                    taamey_d_source(p.char),
                    font_outline(font, p.char),
                )
            )
    return Library(sources, hashlib.sha256(data).hexdigest().upper())


def read(path):
    """The library at path, checked against its profile's structure."""
    root = ET.parse(path).getroot()
    if ssvg.svg_tag(root) != "svg":
        raise ssvg.ProfileError(f"{path}: root is not svg")
    a = ssvg.profile_attrs(
        root,
        "root",
        {"viewBox", "width", "height", "data-profile", "data-taamey-d-sha256"},
    )
    if a.get("data-profile") != PROFILE:
        raise ssvg.ProfileError(f"{path}: data-profile is not {PROFILE!r}")
    lib = Library(taamey_d_sha256=a.get("data-taamey-d-sha256", ""))
    for tag, el in ssvg.svg_children(root):
        cls = el.attrib.get("class", "")
        if tag == "style" or (tag == "g" and cls == "labels"):
            continue
        if tag != "g" or cls != "glyph-source":
            raise ssvg.ProfileError(
                f"{path}: element {tag}.{cls} is not in the profile"
            )
        ga = ssvg.profile_attrs(
            el,
            "glyph-source",
            {
                "class",
                "id",
                "data-kind",
                "data-part",
                "data-from",
                "data-clean-note",
                "transform",
            },
        )
        gid = ssvg.require(ga, "id", "glyph-source")
        kind = ssvg.require(ga, "data-kind", gid)
        level5.pass_of(kind)
        paths = []
        for ctag, child in ssvg.svg_children(el):
            if ctag != "path" or child.attrib.get("class") != "outline":
                raise ssvg.ProfileError(f"{gid}: its one child is a path.outline")
            ca = ssvg.profile_attrs(child, f"{gid} outline", {"class", "d"})
            paths.append(ca.get("d", ""))
        if len(paths) != 1:
            raise ssvg.ProfileError(f"{gid}: its one child is a path.outline")
        lib.sources.append(
            GlyphSource(
                gid,
                kind,
                ga.get("data-part", ""),
                ssvg.require(ga, "data-from", gid),
                paths[0],
                ga.get("data-clean-note", ""),
            )
        )
    return lib


def _show_box(src):
    """The glyph's box as the library shows it, and the scale it is shown at."""
    pts = [q for p in geo.flatten(geo.parse_path(src.outline)) for q in p]
    if not pts:
        return None, 1.0
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    scale = TAAMEY_D_SHOW_SCALE if src.is_taamey_d else 1.0
    if src.is_taamey_d:
        # Font units are y up: shown turned over.
        return (min(xs), -max(ys), max(xs), -min(ys)), scale
    return (min(xs), min(ys), max(xs), max(ys)), scale


def dumps(lib):
    """The library's text: the same content always gives the same text."""
    boxes = [_show_box(s) for s in lib.sources]
    cell = SHOW_MARGIN
    for box, scale in boxes:
        if box:
            cell = max(cell, (box[2] - box[0]) * scale, (box[3] - box[1]) * scale)
    cell += SHOW_MARGIN
    cols = SHOW_COLUMNS
    rows = max(1, -(-len(lib.sources) // cols))
    row_h = cell + 2 * LABEL_SIZE
    w, h = cols * cell, rows * row_h
    root = [
        f'xmlns="{_SVG}"',
        f'viewBox="0 0 {geo.fmt(w, 2)} {geo.fmt(h, 2)}"',
        f'width="{geo.fmt(3 * w, 2)}"',
        f'height="{geo.fmt(3 * h, 2)}"',
        f'data-profile="{PROFILE}"',
    ]
    if lib.taamey_d_sha256:
        root.append(f'data-taamey-d-sha256="{lib.taamey_d_sha256}"')
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<svg " + "\n     ".join(root) + ">",
        "  <style>.outline { fill: #000 } .labels { font: 2.5px sans-serif;"
        " fill: #555 }</style>",
    ]
    labels = []
    for k, (s, (box, scale)) in enumerate(zip(lib.sources, boxes)):
        cx = (k % cols) * cell + cell / 2
        cy = (k // cols) * row_h + cell / 2
        transform = ""
        if box:
            mx, my = (box[0] + box[2]) / 2 * scale, (box[1] + box[3]) / 2 * scale
            flip = -scale if s.is_taamey_d else scale
            transform = (
                f' transform="translate({geo.fmt(cx - mx, 3)} {geo.fmt(cy - my, 3)})'
                f' scale({geo.fmt(scale, 4)} {geo.fmt(flip, 4)})"'
            )
        part = f' data-part="{ssvg.esc(s.part)}"' if s.part else ""
        note = f' data-clean-note="{ssvg.esc(s.clean_note)}"' if s.clean_note else ""
        lines.append(
            f'  <g class="glyph-source" id="{s.id}" data-kind="{ssvg.esc(s.kind)}"{part}'
            f' data-from="{ssvg.esc(s.source)}"{note}{transform}>'
        )
        lines.append(f'    <path class="outline" d="{s.outline}"/>')
        lines.append("  </g>")
        labels.append(
            f'    <text x="{geo.fmt(cx, 2)}" y="{geo.fmt(cy + cell / 2 + LABEL_SIZE, 2)}"'
            f' text-anchor="middle">{ssvg.esc(s.id)}</text>'
        )
    lines.append('  <g class="labels">')
    lines += labels
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def write(lib, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(dumps(lib))


def structural_problems(lib):
    """What the library gets wrong, whatever the crops."""
    out = list(TABLE_PROBLEMS)
    ids = [s.id for s in lib.sources]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        out.append(f"glyph ids used more than once: {dupes}")
    for s in lib.sources:
        entry = GLYPHS[s.kind]
        if not entry.fitted:
            out.append(f"{s.id}: a glyph of {s.kind!r}, which is not fitted")
            continue
        parts = {p.name: p for p in entry.parts}
        if s.part not in parts:
            out.append(f"{s.id}: {s.part!r} is no written part of a {s.kind}")
            continue
        if s.is_taamey_d:
            want = taamey_d_source(parts[s.part].char)
            if s.source != want:
                out.append(f"{s.id}: data-from is not {want!r}")
            if s.id != taamey_d_id(s.kind, s.part):
                out.append(
                    f"{s.id}: Taamey D's glyph's id is not its kind's and part's"
                )
        else:
            try:
                s.scribe_source()
            except ValueError as exc:
                out.append(str(exc))
        if s.clean_note and s.is_taamey_d:
            out.append(f"{s.id}: a glyph of Taamey D's takes no data-clean-note")
        if not s.outline:
            out.append(f"{s.id}: no outline")
    if any(s.is_taamey_d for s in lib.sources) and not lib.taamey_d_sha256:
        out.append("glyphs of Taamey D's but no data-taamey-d-sha256 on the root")
    have = {(s.kind, s.part) for s in lib.sources if s.is_taamey_d}
    for kind, entry in GLYPHS.items():
        if entry.fitted:
            for p in entry.parts:
                if (kind, p.name) not in have:
                    out.append(
                        f"no glyph of Taamey D's for {kind!r}"
                        + (f", part {p.name!r}" if p.name else "")
                    )
    return out
