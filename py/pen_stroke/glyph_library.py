"""The library of glyphs that a fitted word places on a crop's ink.

doc/pen-stroke-snips/glyphs.svg is the font that the ink-region work evolves,
under the profile in doc/ink-region-representation.md, "The library of glyphs":
one glyph-source for each glyph, of a kind of pen_stroke.level5 and one of its
written parts, of three sorts.  A glyph of the scribe's, whose data-from names a
crop and a group, is the ink that the draft of that crop's region-SVG gives the
group's regions, traced as a region is, in that crop's pixels, y down; or, whose
data-from names a glyph crop, the ink inside a lasso round one letter of a small
crop of a page image, darker than a threshold, traced the same way; either
outline is derived (pen_stroke.region_derive).  A glyph of Taamey D's, whose
data-from names Taamey D and a character's Unicode name, is the outline to which
Taamey-D/font-m-TaD/Taamey_D.ttf maps that character, flattened, in font units,
y up; these are copied into the library only when ``copy_taamey_d`` is asked
for, with the font file's SHA-256, so that a new build of the font changes
nothing here until then.  Nothing under Taamey-D/ is written.  A drawn glyph,
whose data-from names a shape of SHAPES, is that shape's outline in a unit box,
y down, made here after Ben's descriptions of the manuscript's marks.

Profile 1 holds the scribe's glyphs of crops' groups and Taamey D's.  Profile 2
adds the drawn glyphs and the glyph crops, and requires of each glyph of the
scribe's data-judged: who judged it well preserved and well written, beside the
photograph, and when; or else a break, data-break="preserved: ...", which lets
it serve only a group that breaks that guideline too.

GLYPHS, a closed table keyed by every kind of pen_stroke.level5, gives each
kind's written parts, each part's name, Taamey D's character for it and its
drawn shape, and how a group's regions are matched to its parts; or says that
the kind is not fitted, and why.  The table has two views.  Under the
region-SVGs' profile 3 a kind is fitted when Taamey D has a character for each
of its written parts; under profile 4, when each has a drawn shape or Taamey D's
character.  The module raises if the table's counts and level5.PARTS disagree.
"""

import hashlib
import math
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

PROFILE_1 = "glyph-library 1"
# Profile 2: drawn glyphs, glyph crops, and the scribe's glyphs judged.
PROFILE = "glyph-library 2"
PROFILES = (PROFILE_1, PROFILE)
LIBRARY = "glyphs.svg"
# The glyph crops' directory, beside the library.
GLYPH_CROPS = "glyph-crops"
_SVG = "http://www.w3.org/2000/svg"
TAAMEY_D = "Taamey D"
TAAMEY_D_FONT = Path("Taamey-D") / "font-m-TaD" / "Taamey_D.ttf"
DRAWN = "drawn"
GLYPH_CROP = "glyph crop"
# Each quadratic or cubic piece of Taamey D's outlines is cut into this many
# straight segments, as the trial of 2026-11-01 cut them.
CURVE_STEPS = 8
# Taamey D's points, so flattened, are multiples of 1/128 of a font unit, which
# this many decimals write exactly; copy_taamey_d raises on any that is not.
FONT_PLACES = 7
OUTLINE_PLACES = 3
# How the library shows itself when opened: Taamey D's font units, the drawn
# glyphs' unit box and the scribe's crop pixels at about the same size, each glyph
# in a cell of its own.
TAAMEY_D_SHOW_SCALE = 0.05
DRAWN_SHOW_SCALE = 20
SHOW_COLUMNS = 10
SHOW_MARGIN = 6
LABEL_SIZE = 2.5

# The drawn shapes, after Ben's descriptions of the manuscript's marks (2026-11-02,
# sections 80 and 82 of his statements): each an outline in a unit box, y down, to
# which the fit's move, scales, turn and shear give its place, size, proportions
# and slant.  A dot is a circle; a bar a rectangle with rounded ends, lying flat;
# a stroke the same, standing; munax's bent stroke one stroke curving through its
# corner, down its right side and along its foot to the left; and atnax's
# inverted V two strokes meeting in a rounded top.
DOT = "dot"
BAR = "bar"
STROKE = "stroke"
BENT_STROKE = "bent stroke"
INVERTED_V = "inverted V"
SHAPES = (DOT, BAR, STROKE, BENT_STROKE, INVERTED_V)
# A bar's and a stroke's thickness, of their length; the bent stroke's and the
# inverted V's, of their boxes before the box is made a unit one.
BAR_THICKNESS = 0.25
BENT_THICKNESS = 0.2
# The bent stroke's corner and the inverted V's top: the radius of their
# centrelines' curve.
BENT_RADIUS = 0.3
APEX_RADIUS = 0.12
# A full circle's points, and the largest step along a centreline.
CIRCLE_POINTS = 48
CENTRELINE_STEP = 0.02
DRAWN_PLACES = 4
# A judgment, or a break's reason, ends with whose word it is and when.
WHO_WHEN = re.compile(r".*\S \(([^(),]+), (\d{4}-\d{2}-\d{2})\)", re.S)

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
    # The Unicode name of Taamey D's character for the part, or None where the
    # library has no glyph of Taamey D's for it.
    char: str | None
    # The part's drawn shape, one of SHAPES; None for a letter, and for a mark that
    # keeps Taamey D's glyph until Ben describes its shape.
    shape: str | None = None


@dataclass(frozen=True)
class Entry:
    parts: tuple = ()
    order: str = TOP_TO_BOTTOM
    # Why a kind is never fitted; empty for a fitted kind.
    unfitted: str = ""
    # Why a fitted kind is not fitted under the region-SVGs' profile 3, whose
    # glyphs are only the scribe's and Taamey D's: some part of it has no character
    # of Taamey D's.  Empty where each has one.
    unprinted: str = ""

    def why_not(self, drawn):
        """Why the kind is not fitted, or empty where it is: under the region-SVGs'
        profile 4 when drawn is true, and under profile 3 otherwise."""
        return self.unfitted or ("" if drawn else self.unprinted)

    def fitted(self, drawn):
        return not self.why_not(drawn)


def _one(char, shape=None):
    return Entry((Part("", char, shape),))


def _dots(*names, order=TOP_TO_BOTTOM):
    return Entry(tuple(Part(n, _HIRIQ, DOT) for n in names), order)


# A bar is Taamey D's patax and a dot its xiriq, so a qamats is a patax over a
# xiriq, as this manuscript writes it, and a segol three xiriq dots.  Each mark's
# drawn shape follows Ben's descriptions; darga, pashta, qadma, mahapakh and paseq,
# which he has not described and the six crops do not fit, keep Taamey D's glyphs.
_MARK_GLYPHS = {
    "sheva mark": _dots("top dot", "bottom dot"),
    "ḥiriq vowel": _one(_HIRIQ, DOT),
    "tsere vowel": _dots("right dot", "left dot", order=RIGHT_TO_LEFT),
    # Two dots above and one below, between them.
    "segol vowel": _dots("right dot", "lower dot", "left dot", order=RIGHT_TO_LEFT),
    "pataḥ vowel": _one(_PATAH, BAR),
    "qamats vowel": Entry((Part("bar", _PATAH, BAR), Part("dot", _HIRIQ, DOT))),
    "ḥolam dot": _one("HEBREW POINT HOLAM", DOT),
    "qubuts vowel": _dots("top dot", "middle dot", "bottom dot"),
    # A bar and, to its right, the two dots of a sheva, as page F043A's line 4 writes
    # the only one in the six crops.
    "ḥataf pataḥ vowel": Entry(
        (
            Part("bar", _PATAH, BAR),
            Part("top dot", _HIRIQ, DOT),
            Part("bottom dot", _HIRIQ, DOT),
        ),
        BAR_AT_LEFT,
    ),
    "dagesh mark": _one("HEBREW POINT DAGESH OR MAPIQ", DOT),
    "shuruq dot": _one("HEBREW POINT DAGESH OR MAPIQ", DOT),
    "shin dot": _one("HEBREW POINT SHIN DOT", DOT),
    "sin dot": _one("HEBREW POINT SIN DOT", DOT),
    "meteg mark": _one("HEBREW POINT METEG", STROKE),
    "silluq accent": _one("HEBREW POINT METEG", STROKE),
    "maqaf mark": _one("HEBREW PUNCTUATION MAQAF", BAR),
    "rafe mark": Entry(
        (Part("", None, BAR),),
        unprinted="a kind of profile 4, whose bar is drawn",
    ),
    "sof pasuq mark": _dots("top dot", "bottom dot"),
    "paseq mark": _one("HEBREW PUNCTUATION PASEQ"),
    "atnaḥ accent": _one("HEBREW ACCENT ETNAHTA", INVERTED_V),
    "revia accent": _one("HEBREW ACCENT REVIA", DOT),
    "geresh accent": _one(_GERESH, STROKE),
    "gershayim accent": Entry(
        (Part("right stroke", _GERESH, STROKE), Part("left stroke", _GERESH, STROKE)),
        RIGHT_TO_LEFT,
    ),
    "darga accent": _one("HEBREW ACCENT DARGA"),
    "pashta accent": _one("HEBREW ACCENT PASHTA"),
    "qadma accent": _one("HEBREW ACCENT QADMA"),
    # A stroke and, to its left, a dot, as page F102A's line 2 writes the only one in
    # the six crops.
    "tevir accent": Entry(
        (Part("stroke", None, STROKE), Part("dot", _HIRIQ, DOT)),
        RIGHT_TO_LEFT,
        unprinted="Taamey D has no character for a tevir's stroke alone",
    ),
    "tipeḥa accent": _one("HEBREW ACCENT TIPEHA", STROKE),
    "munaḥ accent": _one("HEBREW ACCENT MUNAH", BENT_STROKE),
    "merkha accent": _one("HEBREW ACCENT MERKHA", STROKE),
    "mahapakh accent": _one("HEBREW ACCENT MAHAPAKH"),
    "zaqef accent": _dots("top dot", "bottom dot"),
    "masora circle mark": Entry(unfitted="a masora circle is ink set aside"),
    "bar under the letter": _one(_PATAH, BAR),
    "bar over the letter": _one(_PATAH, BAR),
    "dot under the letter": _one(_HIRIQ, DOT),
    "dot over the letter": _one(_HIRIQ, DOT),
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
    """Where the table and level5's kinds and parts disagree, or its two views."""
    out = []
    if set(GLYPHS) != set(level5.KINDS):
        out.append("the table of glyphs and the kinds disagree")
    for kind, entry in GLYPHS.items():
        if entry.order not in ORDERS:
            out.append(f"{kind}: unknown order {entry.order!r}")
        count = level5.PARTS.get(kind)
        if count is None:
            want = 0 if entry.unfitted else 1
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
        if not entry.unfitted:
            if any(p.char is None and p.shape is None for p in entry.parts):
                out.append(f"{kind}: a part with neither a character nor a shape")
            if bool(entry.unprinted) != any(p.char is None for p in entry.parts):
                out.append(
                    f"{kind}: unprinted must say why exactly when a part has no"
                    " character"
                )
        for p in entry.parts:
            if p.char is not None:
                unicodedata.lookup(p.char)
            if p.shape is not None and p.shape not in SHAPES:
                out.append(f"{kind}: unknown shape {p.shape!r}")
        if level5.pass_of(kind) == level5.LETTERS and any(p.shape for p in entry.parts):
            out.append(f"{kind}: a letter has no drawn shape")
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


def drawn_id(kind, part):
    return "drawn-" + slug(kind) + (f"-{slug(part)}" if part else "")


def drawn_source(shape):
    return f"{DRAWN} {shape}"


def glyph_crop_source(stem):
    return f"{GLYPH_CROP} {stem}"


# ---------------------------------------------------------------- the guidelines

# The five guidelines of the font of the manuscript's shapes, by their short names,
# which a break names (Ben, 2026-11-02, section 84: guidelines, since "we'll often
# want to break them, at least on a per-word basis").
PRESERVED = "preserved"
AREA = "area"
LIMBS = "limbs"
DRAWN_MARKS = "drawn"
RAFE = "rafe"
GUIDELINES = (PRESERVED, AREA, LIMBS, DRAWN_MARKS, RAFE)
BREAK_SEPARATOR = "; "


def parse_breaks(text):
    """A data-break's breaks, each (guideline, why), and what is wrong with it: a
    break that names no guideline, or gives no reason ending with whose word it is
    and when, as in "area: the ink has flaked (Claude, 2026-11-03)"."""
    out, problems = [], []
    if not text:
        return out, problems
    for item in text.split(BREAK_SEPARATOR):
        name, sep, why = item.partition(": ")
        if not sep or name not in GUIDELINES:
            problems.append(f"a break that names no guideline: {item!r}")
            continue
        if not WHO_WHEN.fullmatch(why):
            problems.append(
                f"a break of {name!r} that gives no reason with whose word it is and"
                f" when: {item!r}"
            )
            continue
        out.append((name, why))
    return out, problems


def breaks_named(text):
    """The guidelines that a data-break names, malformed breaks left out."""
    return {name for name, _ in parse_breaks(text)[0]}


@dataclass
class GlyphSource:
    id: str
    kind: str
    # Empty for a sign of one part.
    part: str
    # "Taamey D <Unicode name>", "drawn <shape>", "glyph crop <stem>", or "<crop>
    # <group>" for a glyph of the scribe's from a crop's group.
    source: str
    # Path data: pixels, y down, for the scribe's, a crop's or a glyph crop's; font
    # units, y up, for Taamey D's; a unit box, y down, for the drawn.  All but
    # Taamey D's are derived.
    outline: str = ""
    # Why a letter of the scribe's serves though it is not clean: its ink touches
    # another group's ink.
    clean_note: str = ""
    # Profile 2: who judged a glyph of the scribe's well preserved and well
    # written, beside the photograph, and when; or a break of the guideline
    # preserved, which lets it serve only a group that breaks it too.
    judged: str = ""
    brk: str = ""
    # A glyph crop's box in its page image, x0 y0 x1 y1; the page image's SHA-256;
    # the lasso round its letter's ink, x and y in the glyph crop's pixels for each
    # of its points; and the threshold and speck size of its page's line crop, as
    # level 1 takes them.
    box: tuple = ()
    source_sha256: str = ""
    lasso: tuple = ()
    threshold: int = 0
    speck_size: int = 0

    @property
    def is_taamey_d(self):
        return self.source.startswith(TAAMEY_D + " ")

    @property
    def is_drawn(self):
        return self.source.startswith(DRAWN + " ")

    @property
    def is_glyph_crop(self):
        return self.source.startswith(GLYPH_CROP + " ")

    @property
    def is_scribes(self):
        return not (self.is_taamey_d or self.is_drawn)

    @property
    def unjudged(self):
        """Whether a glyph of the scribe's serves only a group that breaks the
        guideline preserved."""
        return PRESERVED in breaks_named(self.brk)

    def scribe_source(self):
        """The crop's stem and the group's id of a glyph of the scribe's."""
        crop, sep, gid = self.source.rpartition(" ")
        if not self.is_scribes or self.is_glyph_crop or not sep or not crop:
            raise ValueError(f"{self.id}: data-from is not a crop and a group")
        if " " in crop:
            raise ValueError(f"{self.id}: data-from is not a crop and a group")
        return crop, gid

    def glyph_crop_stem(self):
        """A glyph crop's stem: its PNG is GLYPH_CROPS/<stem>.png."""
        stem = self.source[len(GLYPH_CROP) + 1 :]
        if not self.is_glyph_crop or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9-]*", stem
        ):
            raise ValueError(f"{self.id}: data-from is not a glyph crop's ASCII stem")
        return stem

    def shape(self):
        """A drawn glyph's shape."""
        shape = self.source[len(DRAWN) + 1 :]
        if not self.is_drawn or shape not in SHAPES:
            raise ValueError(f"{self.id}: data-from is not a drawn shape")
        return shape


@dataclass
class Library:
    sources: list = field(default_factory=list)
    taamey_d_sha256: str = ""
    profile: str = PROFILE

    @property
    def drawn(self):
        """Whether the library has drawn glyphs and glyph crops: profile 2."""
        return self.profile == PROFILE

    def by_id(self):
        return {s.id: s for s in self.sources}

    def default_for(self, kind, part, drawn=False):
        """The glyph a new glyph of this kind and part takes: the first of the
        scribe's, in the library's order, that serves every group; or else, under
        the region-SVGs' profile 4 (drawn true), the drawn glyph of the part's
        shape; or else Taamey D's."""
        own = [
            s
            for s in self.sources
            if s.kind == kind and s.part == part and s.is_scribes and not s.unjudged
        ]
        if own:
            return own[0]
        ids = [taamey_d_id(kind, part)]
        if drawn:
            ids.insert(0, drawn_id(kind, part))
        sources = self.by_id()
        for i in ids:
            if i in sources:
                return sources[i]
        raise ValueError(f"the library has no glyph for {kind!r}, part {part!r}")


def library_path(snips_dir):
    return Path(snips_dir) / LIBRARY


def glyph_crop_path(snips_dir, src):
    return Path(snips_dir) / GLYPH_CROPS / f"{src.glyph_crop_stem()}.png"


def contours(src):
    """The glyph-source's contours as arrays of points, y up, as a font's are: Taamey
    D's as the library has them, and the scribe's and the drawn flattened and turned
    over, as the trial of 2026-11-01 took the scribe's."""
    polys = geo.flatten(geo.parse_path(src.outline))
    if src.is_taamey_d:
        return [np.array(p, dtype=float) for p in polys]
    return [np.array([(x, -y) for x, y in p], dtype=float) for p in polys]


# ---------------------------------------------------------------- drawn shapes


def _line_points(a, b):
    """Points along a segment, the end left out, no farther apart than
    CENTRELINE_STEP."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    n = max(1, math.ceil(np.hypot(*(b - a)) / CENTRELINE_STEP))
    return [a + (b - a) * k / n for k in range(n)]


def _arc_points(c, r, a0, a1):
    """Points along an arc round c, from angle a0 to a1 in radians, y down, the end
    left out, no farther apart than CENTRELINE_STEP."""
    n = max(1, math.ceil(abs(a1 - a0) * r / CENTRELINE_STEP))
    return [
        np.array(c) + r * np.array([math.cos(a), math.sin(a)])
        for a in (a0 + (a1 - a0) * k / n for k in range(n))
    ]


def _thick(centre, r):
    """The closed outline of a centreline drawn with half-width r and round ends:
    its left side, the end's half circle, its right side back and the start's half
    circle."""
    p = np.array(centre, dtype=float)
    t = np.gradient(p, axis=0)
    t /= np.linalg.norm(t, axis=1)[:, None]
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    half = CIRCLE_POINTS // 2
    ks = np.arange(1, half)

    def cap(c, a0):
        a = a0 - math.pi * ks / half
        return c + r * np.stack([np.cos(a), np.sin(a)], 1)

    end = math.atan2(n[-1, 1], n[-1, 0])
    start = math.atan2(-n[0, 1], -n[0, 0])
    return np.vstack([p + r * n, cap(p[-1], end), (p - r * n)[::-1], cap(p[0], start)])


def _centreline(shape):
    """A shape's centreline and half-width, in units of its own, or None for a dot."""
    if shape == BAR:
        return _line_points((0, 0), (1, 0)) + [np.array((1.0, 0.0))], BAR_THICKNESS / 2
    if shape == STROKE:
        return _line_points((0, 0), (0, 1)) + [np.array((0.0, 1.0))], BAR_THICKNESS / 2
    if shape == BENT_STROKE:
        # Down its right side, round its corner, and along its foot to the left.
        r, top, right, foot, left = BENT_RADIUS, 0.0, 0.65, 0.8, 0.0
        pts = _line_points((right, top), (right, foot - r))
        pts += _arc_points((right - r, foot - r), r, 0.0, math.pi / 2)
        pts += _line_points((right - r, foot), (left, foot))
        return pts + [np.array((left, foot))], BENT_THICKNESS / 2
    if shape == INVERTED_V:
        # Up its left leg, round its top, and down its right leg: legs meeting at
        # (0.5, 0) from (0, 0.9) and (1, 0.9), their corner rounded.
        apex, foot_l, foot_r = np.array((0.5, 0.0)), (0.0, 0.9), (1.0, 0.9)
        up = apex - np.array(foot_l)
        up /= np.linalg.norm(up)
        down = np.array(foot_r) - apex
        down /= np.linalg.norm(down)
        half_angle = math.acos(float(np.dot(-up, down))) / 2
        reach = APEX_RADIUS / math.tan(half_angle)
        a, b = apex - reach * up, apex + reach * down
        # The corner's centre lies below the apex; its arc runs over the top, from
        # up and to the left of the centre to up and to its right.
        c = apex + np.array((0.0, APEX_RADIUS / math.sin(half_angle)))
        a0 = math.atan2(a[1] - c[1], a[0] - c[0])
        a1 = math.atan2(b[1] - c[1], b[0] - c[0])
        pts = _line_points(foot_l, a)
        pts += _arc_points(c, APEX_RADIUS, a0, a1)
        pts += _line_points(b, foot_r)
        return pts + [np.array(foot_r)], BENT_THICKNESS / 2
    if shape == DOT:
        return None
    raise ValueError(f"unknown shape {shape!r}")


def drawn_outline(shape):
    """A drawn shape's outline: path data in a unit box, y down, the shape's larger
    side 1 and centred."""
    line = _centreline(shape)
    if line is None:
        a = 2 * math.pi * np.arange(CIRCLE_POINTS) / CIRCLE_POINTS
        poly = 0.5 + 0.5 * np.stack([np.cos(a), np.sin(a)], 1)
    else:
        poly = _thick(*line)
    lo, hi = poly.min(0), poly.max(0)
    size = (hi - lo).max()
    poly = (poly - (lo + hi) / 2) / size + 0.5
    return geo.polygon_path([[(float(x), float(y)) for x, y in poly]], DRAWN_PLACES)


def drawn_glyphs():
    """A drawn glyph for each written part with a shape of each kind that the table
    fits, in the table's order."""
    out = []
    for kind, entry in GLYPHS.items():
        if not entry.fitted(True):
            continue
        for p in entry.parts:
            if p.shape is not None:
                out.append(
                    GlyphSource(
                        drawn_id(kind, p.name),
                        kind,
                        p.name,
                        drawn_source(p.shape),
                        drawn_outline(p.shape),
                    )
                )
    return out


def with_drawn(lib):
    """A copy of a profile-2 library whose drawn glyphs are made afresh from the
    table: after the scribe's and before Taamey D's."""
    scribes = [s for s in lib.sources if s.is_scribes]
    taamey_d = [s for s in lib.sources if s.is_taamey_d]
    return Library(
        scribes + drawn_glyphs() + taamey_d, lib.taamey_d_sha256, lib.profile
    )


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
    font, one for each written part of each kind that the table fits under the
    region-SVGs' profile 3, after the scribe's and the drawn, in the table's order;
    and the font file's SHA-256."""
    data = Path(font_path).read_bytes()
    font = TTFont(font_path)
    sources = [s for s in lib.sources if not s.is_taamey_d]
    for kind, entry in GLYPHS.items():
        if not entry.fitted(False):
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
    return Library(sources, hashlib.sha256(data).hexdigest().upper(), lib.profile)


def _numbers(text, gid, what, count=None):
    try:
        nums = tuple(float(v) for v in text.split())
    except ValueError as exc:
        raise ssvg.ProfileError(f"{gid}: {what} is numbers") from exc
    if count is not None and len(nums) != count:
        raise ssvg.ProfileError(f"{gid}: {what} holds {count} numbers")
    return nums


def _int(text, gid, what):
    try:
        return int(text)
    except ValueError as exc:
        raise ssvg.ProfileError(f"{gid}: {what} is a whole number") from exc


# A glyph crop's attributes, which profile 2 alone has, and all of which it needs.
_CROP_ATTRS = (
    "data-box",
    "data-source-sha256",
    "data-lasso",
    "data-threshold",
    "data-speck-size",
)


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
    if a.get("data-profile") not in PROFILES:
        raise ssvg.ProfileError(
            f"{path}: data-profile is not one of {', '.join(map(repr, PROFILES))}"
        )
    lib = Library(
        taamey_d_sha256=a.get("data-taamey-d-sha256", ""), profile=a["data-profile"]
    )
    allowed = {
        "class",
        "id",
        "data-kind",
        "data-part",
        "data-from",
        "data-clean-note",
        "transform",
    }
    if lib.drawn:
        allowed |= {"data-judged", "data-break"} | set(_CROP_ATTRS)
    for tag, el in ssvg.svg_children(root):
        cls = el.attrib.get("class", "")
        if tag == "style" or (tag == "g" and cls == "labels"):
            continue
        if tag != "g" or cls != "glyph-source":
            raise ssvg.ProfileError(
                f"{path}: element {tag}.{cls} is not in the profile"
            )
        ga = ssvg.profile_attrs(el, "glyph-source", allowed)
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
        src = GlyphSource(
            gid,
            kind,
            ga.get("data-part", ""),
            ssvg.require(ga, "data-from", gid),
            paths[0],
            ga.get("data-clean-note", ""),
            ga.get("data-judged", ""),
            ga.get("data-break", ""),
        )
        crop = [k for k in _CROP_ATTRS if k in ga]
        if src.is_glyph_crop:
            missing = [k for k in _CROP_ATTRS if k not in ga]
            if missing:
                raise ssvg.ProfileError(f"{gid}: a glyph crop needs {missing}")
            src.box = _numbers(ga["data-box"], gid, "data-box", 4)
            src.source_sha256 = ga["data-source-sha256"]
            src.lasso = _numbers(ga["data-lasso"], gid, "data-lasso")
            src.threshold = _int(ga["data-threshold"], gid, "data-threshold")
            src.speck_size = _int(ga["data-speck-size"], gid, "data-speck-size")
        elif crop:
            raise ssvg.ProfileError(f"{gid}: {crop} belong to a glyph crop")
        lib.sources.append(src)
    return lib


def _show_box(src):
    """The glyph's box as the library shows it, and the scale it is shown at."""
    pts = [q for p in geo.flatten(geo.parse_path(src.outline)) for q in p]
    if not pts:
        return None, 1.0
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    scale = 1.0
    if src.is_taamey_d:
        scale = TAAMEY_D_SHOW_SCALE
    elif src.is_drawn:
        scale = DRAWN_SHOW_SCALE
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
        f'data-profile="{lib.profile}"',
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
        if s.judged:
            note += f' data-judged="{ssvg.esc(s.judged)}"'
        if s.brk:
            note += f' data-break="{ssvg.esc(s.brk)}"'
        if s.is_glyph_crop:
            note += (
                f' data-box="{" ".join(str(int(v)) for v in s.box)}"'
                f' data-source-sha256="{s.source_sha256}"'
                f' data-lasso="{" ".join(geo.fmt(v, 2) for v in s.lasso)}"'
                f' data-threshold="{s.threshold}" data-speck-size="{s.speck_size}"'
            )
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


def _sort_problems(s, part, drawn):
    """What a glyph-source gets wrong for its sort, given the table's part."""
    out = []
    if s.is_taamey_d:
        if part.char is None:
            out.append(f"{s.id}: Taamey D has no character in the table for its part")
        elif s.source != taamey_d_source(part.char):
            out.append(f"{s.id}: data-from is not {taamey_d_source(part.char)!r}")
        if s.id != taamey_d_id(s.kind, s.part):
            out.append(f"{s.id}: Taamey D's glyph's id is not its kind's and part's")
    elif s.is_drawn:
        if not drawn:
            out.append(f"{s.id}: a drawn glyph in a library of profile {PROFILE_1!r}")
        elif part.shape is None or s.source != drawn_source(part.shape):
            out.append(f"{s.id}: data-from is not its part's drawn shape")
        if s.id != drawn_id(s.kind, s.part):
            out.append(f"{s.id}: a drawn glyph's id is not its kind's and part's")
    elif s.is_glyph_crop:
        if not drawn:
            out.append(f"{s.id}: a glyph crop in a library of profile {PROFILE_1!r}")
        try:
            s.glyph_crop_stem()
        except ValueError as exc:
            out.append(str(exc))
        if len(s.lasso) < 6 or len(s.lasso) % 2:
            out.append(f"{s.id}: data-lasso is three points or more, each x and y")
        if not re.fullmatch(r"[0-9A-F]{64}", s.source_sha256):
            out.append(f"{s.id}: data-source-sha256 is not a SHA-256 in hexadecimal")
    else:
        try:
            s.scribe_source()
        except ValueError as exc:
            out.append(str(exc))
    if s.is_scribes and drawn:
        if bool(s.judged) == s.unjudged:
            out.append(
                f"{s.id}: a glyph of the scribe's needs data-judged, or else a break"
                " of the guideline preserved, and not both"
            )
        elif s.judged and not WHO_WHEN.fullmatch(s.judged):
            out.append(
                f"{s.id}: data-judged does not end with whose judgment it is and when"
            )
        out += [f"{s.id}: {p}" for p in parse_breaks(s.brk)[1]]
        if breaks_named(s.brk) - {PRESERVED}:
            out.append(f"{s.id}: a glyph of the library breaks only preserved")
    elif s.judged or s.brk:
        out.append(f"{s.id}: only a glyph of the scribe's is judged")
    if s.clean_note and (not s.is_scribes or s.is_glyph_crop):
        out.append(f"{s.id}: only a glyph of a crop's group takes data-clean-note")
    return out


def structural_problems(lib):
    """What the library gets wrong, whatever the crops: under profile 2 its glyphs
    are fitted as the region-SVGs' profile 4 fits them, and under profile 1 as
    profile 3 does."""
    out = list(TABLE_PROBLEMS)
    drawn = lib.drawn
    ids = [s.id for s in lib.sources]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        out.append(f"glyph ids used more than once: {dupes}")
    for s in lib.sources:
        entry = GLYPHS[s.kind]
        if not entry.fitted(drawn):
            out.append(f"{s.id}: a glyph of {s.kind!r}, which is not fitted")
            continue
        parts = {p.name: p for p in entry.parts}
        if s.part not in parts:
            out.append(f"{s.id}: {s.part!r} is no written part of a {s.kind}")
            continue
        out += _sort_problems(s, parts[s.part], drawn)
        if not s.outline:
            out.append(f"{s.id}: no outline")
    if any(s.is_taamey_d for s in lib.sources) and not lib.taamey_d_sha256:
        out.append("glyphs of Taamey D's but no data-taamey-d-sha256 on the root")
    have = {(s.kind, s.part) for s in lib.sources if s.is_taamey_d}
    have_drawn = {(s.kind, s.part) for s in lib.sources if s.is_drawn}
    for kind, entry in GLYPHS.items():
        for p in entry.parts:
            name = f"{kind!r}" + (f", part {p.name!r}" if p.name else "")
            if entry.fitted(False) and (kind, p.name) not in have:
                out.append(f"no glyph of Taamey D's for {name}")
            if drawn and entry.fitted(True) and p.shape:
                if (kind, p.name) not in have_drawn:
                    out.append(f"no drawn glyph for {name}")
    return out
