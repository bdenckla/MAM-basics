"""Reading and writing a stroke-SVG under the profile.

The reader accepts the profile's elements, classes and attributes and nothing
else, so that a misspelt class cannot silently drop a stroke.  It ignores the
Inkscape and Sodipodi namespaces a vector editor adds, and the writer, which
always writes the same text for the same content, drops them.
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from pen_stroke import geometry as geo
from pen_stroke import level1
from pen_stroke import level3
from pen_stroke import level5
from pen_stroke.nib import Nib

PROFILE = "pen-stroke 1"
_SVG = "http://www.w3.org/2000/svg"
_XLINK = "http://www.w3.org/1999/xlink"
_EDITOR_NAMESPACES = (
    "http://www.inkscape.org/namespaces/inkscape",
    "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
)

# The provenance and parameters on the root, in the order they are written.
PROVENANCE_KEYS = (
    "manuscript",
    "page",
    "column",
    "line",
    "line-read-by",
    "mam-verse",
    "uxlc-verse",
    "combined-chanted-word",
    "combined-source",
    "taxton-chanted-word",
    "elyon-chanted-word",
    "crop-note",
    "source-url",
    "source-size",
    "source-sha256",
    "crop-box",
    "strokes-by",
)
NIB_CLASSES = (level5.LETTERS, level5.MARKS)
CONFIDENCES = ("high", "medium", "low")

STYLE = """
.fills path { fill: #000; fill-opacity: 0.2 }
.image-residual, .pen-residual, .groups, .median { display: none }
.stroke .ink { fill: #c0392b; fill-opacity: 0.4 }
.frame line { stroke: #2471a3; stroke-width: 0.5 }
"""


@dataclass
class Fill:
    id: str
    d: str
    judged: str | None = None


@dataclass
class Piece:
    id: str
    source: str
    judged: str
    d: str


@dataclass
class Stroke:
    id: str
    nib: str
    median: str
    ink: str = ""
    shape: str = ""
    confidence: str = "high"
    note: str = ""
    override: Nib | None = None


@dataclass
class Group:
    id: str
    kind: str
    members: list
    note: str = ""


@dataclass
class Frame:
    baseline: tuple
    letter_height: float


@dataclass
class StrokeFile:
    width: int
    height: int
    image: str
    provenance: dict
    threshold: int
    speck_size: int
    halo_band: int
    nibs: dict
    tracer: str = level1.TRACER
    fills: list = field(default_factory=list)
    pieces: list = field(default_factory=list)
    smoothing: str = ""
    halo: str = ""
    strokes: list = field(default_factory=list)
    unexplained: str = ""
    overshoot: str = ""
    frame: Frame | None = None
    groups: list = field(default_factory=list)

    def nib_of(self, stroke):
        return stroke.override or self.nibs[stroke.nib]


class ProfileError(ValueError):
    pass


def _tag(el):
    tag = el.tag
    if tag.startswith("{" + _SVG + "}"):
        return tag[len(_SVG) + 2 :]
    return None


def _is_editor(name):
    return any(name.startswith("{" + ns + "}") for ns in _EDITOR_NAMESPACES)


def _attrs(el, where, allowed):
    out = {}
    for name, value in el.attrib.items():
        if _is_editor(name):
            continue
        if name == "{" + _XLINK + "}href":
            name = "href"
        if name not in allowed:
            raise ProfileError(f"{where}: attribute {name!r} is not in the profile")
        out[name] = value
    return out


def _require(attrs, key, where):
    if key not in attrs:
        raise ProfileError(f"{where}: missing {key!r}")
    return attrs[key]


def _children(el):
    out = []
    for child in el:
        if _is_editor(child.tag):
            continue
        tag = _tag(child)
        if tag in ("defs", "metadata", "title", "desc"):
            continue
        if tag is None:
            raise ProfileError(f"element {child.tag!r} is not SVG")
        out.append((tag, child))
    return out


def _nib_attrs(a, prefix):
    return Nib(
        width=float(a[f"{prefix}-width"]),
        angle=float(a[f"{prefix}-angle"]),
        edge=float(a[f"{prefix}-edge"]),
    )


def read(path):
    """The stroke-SVG at path, checked against the profile's structure."""
    root = ET.parse(path).getroot()
    if _tag(root) != "svg":
        raise ProfileError(f"{path}: root is not svg")
    nib_keys = {
        f"data-nib-{c}-{p}" for c in NIB_CLASSES for p in ("width", "angle", "edge")
    }
    allowed = {"viewBox", "width", "height", "version", "data-profile", "data-channel"}
    allowed |= {f"data-{k}" for k in PROVENANCE_KEYS}
    allowed |= {"data-threshold", "data-speck-size", "data-halo-band", "data-tracer"}
    allowed |= nib_keys
    a = _attrs(root, "root", allowed)
    if a.get("data-profile") != PROFILE:
        raise ProfileError(f"{path}: data-profile is not {PROFILE!r}")
    if a.get("data-channel") != "luminance":
        raise ProfileError(f"{path}: data-channel is not 'luminance'")
    vb = [float(v) for v in _require(a, "viewBox", "root").split()]
    if vb[:2] != [0, 0] or vb[2] != int(vb[2]) or vb[3] != int(vb[3]):
        raise ProfileError(
            f"{path}: viewBox must be 0 0 <width> <height> in whole pixels"
        )
    sf = StrokeFile(
        width=int(vb[2]),
        height=int(vb[3]),
        image="",
        provenance={k: a[f"data-{k}"] for k in PROVENANCE_KEYS if f"data-{k}" in a},
        threshold=int(_require(a, "data-threshold", "root")),
        speck_size=int(_require(a, "data-speck-size", "root")),
        halo_band=int(_require(a, "data-halo-band", "root")),
        nibs={
            level5.LETTERS: _nib_attrs(a, "data-nib-letters"),
            level5.MARKS: _nib_attrs(a, "data-nib-marks"),
        },
        tracer=_require(a, "data-tracer", "root"),
    )
    seen = []
    for tag, el in _children(root):
        cls = el.attrib.get("class", "")
        key = f"{tag}.{cls}" if cls else tag
        seen.append(key)
        if key == "style":
            continue
        if key == "image.crop":
            ia = _attrs(el, "image", {"class", "href", "x", "y", "width", "height"})
            sf.image = _require(ia, "href", "image")
        elif key == "g.fills":
            _read_fills(el, sf)
        elif key == "g.image-residual":
            _read_image_residual(el, sf)
        elif key == "g.strokes":
            _read_strokes(el, sf)
        elif key == "g.pen-residual":
            _read_pen_residual(el, sf)
        elif key == "g.frame":
            _read_frame(el, sf)
        elif key == "g.groups":
            _read_groups(el, sf)
        else:
            raise ProfileError(f"{path}: element {key!r} is not in the profile")
    for needed in (
        "image.crop",
        "g.fills",
        "g.image-residual",
        "g.strokes",
        "g.groups",
    ):
        if needed not in seen:
            raise ProfileError(f"{path}: missing {needed}")
    return sf


def _read_fills(g, sf):
    for tag, el in _children(g):
        if tag != "path":
            raise ProfileError(f"fills: {tag} is not a path")
        a = _attrs(el, "fill", {"id", "d", "data-judged"})
        judged = a.get("data-judged")
        if judged is not None and judged not in level1.JUDGMENTS:
            raise ProfileError(f"fill {a.get('id')}: unknown judgment {judged!r}")
        sf.fills.append(
            Fill(_require(a, "id", "fill"), _require(a, "d", "fill"), judged)
        )


def _read_image_residual(g, sf):
    for tag, el in _children(g):
        cls = el.attrib.get("class", "")
        if tag != "path":
            raise ProfileError(f"image-residual: {tag} is not a path")
        if cls == "piece":
            a = _attrs(el, "piece", {"class", "id", "d", "data-source", "data-judged"})
            source = _require(a, "data-source", "piece")
            judged = _require(a, "data-judged", "piece")
            if source not in level1.PIECE_SOURCES:
                raise ProfileError(f"piece {a.get('id')}: unknown source {source!r}")
            if judged not in level1.JUDGMENTS:
                raise ProfileError(f"piece {a.get('id')}: unknown judgment {judged!r}")
            sf.pieces.append(
                Piece(
                    _require(a, "id", "piece"),
                    source,
                    judged,
                    _require(a, "d", "piece"),
                )
            )
        elif cls in ("smoothing", "halo"):
            a = _attrs(el, cls, {"class", "d"})
            setattr(sf, cls, a.get("d", ""))
        else:
            raise ProfileError(f"image-residual: class {cls!r} is not in the profile")


def _read_strokes(g, sf):
    for tag, el in _children(g):
        if tag != "g" or el.attrib.get("class") != "stroke":
            raise ProfileError("strokes: every child is a g.stroke")
        nib_keys = {f"data-nib-{p}" for p in ("width", "angle", "edge")}
        a = _attrs(
            el,
            "stroke",
            {"class", "id", "data-nib", "data-shape", "data-confidence", "data-note"}
            | nib_keys,
        )
        sid = _require(a, "id", "stroke")
        nib = _require(a, "data-nib", sid)
        if nib not in NIB_CLASSES:
            raise ProfileError(f"{sid}: unknown nib {nib!r}")
        conf = a.get("data-confidence", "high")
        if conf not in CONFIDENCES:
            raise ProfileError(f"{sid}: unknown confidence {conf!r}")
        shape = a.get("data-shape", "")
        if shape and shape not in level3.SHAPES:
            raise ProfileError(f"{sid}: unknown shape {shape!r}")
        override = None
        if any(k in a for k in nib_keys):
            if not all(k in a for k in nib_keys):
                raise ProfileError(f"{sid}: a nib override gives width, angle and edge")
            override = _nib_attrs(a, "data-nib")
        st = Stroke(
            sid,
            nib,
            "",
            shape=shape,
            confidence=conf,
            note=a.get("data-note", ""),
            override=override,
        )
        for ctag, child in _children(el):
            cls = child.attrib.get("class", "")
            if ctag != "path" or cls not in ("median", "ink"):
                raise ProfileError(f"{sid}: child {ctag}.{cls} is not in the profile")
            # A vector editor gives every path an id and a style; neither means anything here.
            ca = _attrs(child, f"{sid} {cls}", {"class", "d", "id", "style"})
            setattr(st, cls, ca.get("d", ""))
        if not st.median:
            raise ProfileError(f"{sid}: no median")
        sf.strokes.append(st)


def _read_pen_residual(g, sf):
    for tag, el in _children(g):
        cls = el.attrib.get("class", "")
        if tag != "path" or cls not in ("unexplained", "overshoot"):
            raise ProfileError(f"pen-residual: {tag}.{cls} is not in the profile")
        a = _attrs(el, cls, {"class", "d"})
        setattr(sf, cls, a.get("d", ""))


def _read_frame(g, sf):
    a = _attrs(g, "frame", {"class", "data-letter-height"})
    lines = []
    for tag, el in _children(g):
        if tag != "line" or el.attrib.get("class") != "baseline":
            raise ProfileError("frame: its one child is a line.baseline")
        la = _attrs(el, "baseline", {"class", "x1", "y1", "x2", "y2"})
        lines.append(tuple(float(la[k]) for k in ("x1", "y1", "x2", "y2")))
    if len(lines) != 1:
        raise ProfileError("frame: exactly one baseline")
    sf.frame = Frame(lines[0], float(_require(a, "data-letter-height", "frame")))


def _read_groups(g, sf):
    for tag, el in _children(g):
        if tag != "g" or el.attrib.get("class") != "group":
            raise ProfileError("groups: every child is a g.group")
        a = _attrs(el, "group", {"class", "id", "data-kind", "data-note"})
        gid = _require(a, "id", "group")
        kind = _require(a, "data-kind", gid)
        level5.nib_class(kind)
        members = []
        for ctag, child in _children(el):
            if ctag != "use":
                raise ProfileError(f"{gid}: child {ctag} is not a use")
            ua = _attrs(child, f"{gid} use", {"href"})
            href = _require(ua, "href", gid)
            if not href.startswith("#"):
                raise ProfileError(
                    f"{gid}: href {href!r} is not a fragment of this file"
                )
            members.append(href[1:])
        sf.groups.append(Group(gid, kind, members, a.get("data-note", "")))


def _esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _nib_text(prefix, nib):
    return [
        f'{prefix}-width="{geo.fmt(nib.width, 2)}"',
        f'{prefix}-angle="{geo.fmt(nib.angle, 1)}"',
        f'{prefix}-edge="{geo.fmt(nib.edge, 2)}"',
    ]


def dumps(sf):
    """The stroke-SVG's text: the same content always gives the same text."""
    root = [
        f'xmlns="{_SVG}"',
        f'viewBox="0 0 {sf.width} {sf.height}"',
        f'width="{sf.width}"',
        f'height="{sf.height}"',
        f'data-profile="{PROFILE}"',
    ]
    for k in PROVENANCE_KEYS:
        if k in sf.provenance:
            root.append(f'data-{k}="{_esc(sf.provenance[k])}"')
    root += [
        'data-channel="luminance"',
        f'data-threshold="{sf.threshold}"',
        f'data-speck-size="{sf.speck_size}"',
        f'data-halo-band="{sf.halo_band}"',
        f'data-tracer="{_esc(sf.tracer)}"',
    ]
    root += _nib_text("data-nib-letters", sf.nibs[level5.LETTERS])
    root += _nib_text("data-nib-marks", sf.nibs[level5.MARKS])
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<svg " + "\n     ".join(root) + ">",
    ]
    lines.append(f"  <style>{STYLE}  </style>")
    lines.append(
        f'  <image class="crop" href="{_esc(sf.image)}" x="0" y="0"'
        f' width="{sf.width}" height="{sf.height}"/>'
    )
    lines.append('  <g class="fills">')
    for f in sf.fills:
        judged = f' data-judged="{f.judged}"' if f.judged else ""
        lines.append(f'    <path id="{f.id}"{judged} d="{f.d}"/>')
    lines.append("  </g>")
    lines.append('  <g class="image-residual">')
    for p in sf.pieces:
        lines.append(
            f'    <path class="piece" id="{p.id}" data-source="{p.source}"'
            f' data-judged="{p.judged}" d="{p.d}"/>'
        )
    lines.append(f'    <path class="smoothing" d="{sf.smoothing}"/>')
    lines.append(f'    <path class="halo" d="{sf.halo}"/>')
    lines.append("  </g>")
    lines.append('  <g class="strokes">')
    for s in sf.strokes:
        attrs = ['class="stroke"', f'id="{s.id}"', f'data-nib="{s.nib}"']
        if s.override is not None:
            attrs += _nib_text("data-nib", s.override)
        if s.shape:
            attrs.append(f'data-shape="{s.shape}"')
        if s.confidence != "high":
            attrs.append(f'data-confidence="{s.confidence}"')
        if s.note:
            attrs.append(f'data-note="{_esc(s.note)}"')
        lines.append(f"    <g {' '.join(attrs)}>")
        lines.append(f'      <path class="median" d="{s.median}"/>')
        lines.append(f'      <path class="ink" d="{s.ink}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    lines.append('  <g class="pen-residual">')
    lines.append(f'    <path class="unexplained" d="{sf.unexplained}"/>')
    lines.append(f'    <path class="overshoot" d="{sf.overshoot}"/>')
    lines.append("  </g>")
    if sf.frame is not None:
        x1, y1, x2, y2 = (geo.fmt(v, 1) for v in sf.frame.baseline)
        lines.append(
            f'  <g class="frame" data-letter-height="{geo.fmt(sf.frame.letter_height, 1)}">'
        )
        lines.append(
            f'    <line class="baseline" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
        )
        lines.append("  </g>")
    lines.append('  <g class="groups">')
    for g in sf.groups:
        note = f' data-note="{_esc(g.note)}"' if g.note else ""
        lines.append(
            f'    <g class="group" id="{g.id}" data-kind="{_esc(g.kind)}"{note}>'
        )
        for m in g.members:
            lines.append(f'      <use href="#{m}"/>')
        lines.append("    </g>")
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def write(sf, path):
    with open(path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write(dumps(sf))
