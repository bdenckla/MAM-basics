"""Write MAM-morphhb: today's MAM in the form of the 2014 MAPM.xml in openscriptures/morphhb.

Public entry point: almost_main(paths)

paths keys
----------
mam_simple_root : MAM-simple; BHS JSON, falling back to MAM JSON, as MAM-OSIS reads it
mam_parsed_path : MAM-parsed, for its plus/ titles, parashot and poetic line breaks
header_path     : the hand-written header element
output_path     : MAM-morphhb/MAPM.xml
xsd_path        : OSIS schema to validate against
xml_xsd_path    : local copy of the W3C xml.xsd that the OSIS schema imports

The output reproduces the 2014 file's line layout, which OpenScriptorium's importer
reads line by line: tab indentation, one prose verse per line, each break as <lb/>
lines, one poetic line per line.  MAM-morphhb/README.md describes the layout and where
it departs from the 2014 file.
"""

import xml.etree.ElementTree as ET

from mam_morphhb import morphhb_inline as inl
from mam_morphhb import morphhb_notes
from mam_morphhb import morphhb_plus
from mam_morphhb import morphhb_poetry
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals
from mb_cmn import mam_simple_json
from mb_cmn.mam_simple_book_group import resolve_book_group_path
from mb_misc import osis_book_abbrevs
from osis import osis_namespace as osisn
from osis import osis_runner

_WHOLE_TITLE = "מקרא על פי המסורה"
_TOP_GROUPS = (
    ("Gen-Deut", "תורה", ("Gen", "Exod", "Lev", "Num", "Deut")),
    (
        "Josh-Mal",
        "נביאים",
        ("Josh", "Judg", "1Sam-2Sam", "1Kgs-2Kgs", "Isa", "Jer", "Ezek", "Hos-Mal"),
    ),
    (
        "Ps-2Chr",
        "כתובים",
        (
            *("Ps", "Prov", "Job", "Song", "Ruth", "Lam", "Eccl", "Esth", "Dan"),
            *("Ezra-Neh", "1Chr-2Chr"),
        ),
    ),
)
_TORAH = _TOP_GROUPS[0][2]
_MARKERS = {
    "spi-pe2": "pe2",
    "spi-pe3": "pe3",
    "spi-samekh2": "samekh2",
    "spi-samekh3": "samekh3",
}
_LB_COUNTS = {"pe2": 2, "pe3": 1, "samekh2": 1, "samekh3": 0, None: 0}
_BREAK_LEADS = {
    "pe2": "",
    "pe3": "",
    "samekh2": inl.IDEOSP * 3,
    "samekh3": inl.TWO_EMSP,
}
_VERSE_FIELDS = {
    "osisID",
    "text",
    "starts-with-sampe",
    "ends-with-sampe",
    "contents-corresponds-to",
    "osisID-of-MAM-src",
}
_SAMPE_VALUES = {"pe2", "pe3", "samekh2", "samekh3"}


def almost_main(paths):
    """Write paths["output_path"] and validate it against the OSIS schema."""
    bkgs = osis_book_abbrevs.bk24_bkgs(tbn.ALL_BK39_IDS)
    names = [bkg["bkg-name"] for bkg in bkgs]
    if names != [name for _scope, _title, group in _TOP_GROUPS for name in group]:
        raise ValueError(f"Unexpected book groups: {names}")
    book_groups = {
        name: mam_simple_json.read_book_group(
            resolve_book_group_path(
                paths["mam_simple_root"], fmt="json", vtrad="bhs", stems=(name,)
            )
        )
        for name in names
    }
    verses = [v for root in book_groups.values() for v in mam_simple_json.verses(root)]
    notes = morphhb_notes.variant_notes(verses)
    structure = morphhb_plus.read_structure(paths["mam_parsed_path"])
    writer = _Writer(structure, notes, _scopes(verses, structure))
    writer.document(_header_lines(paths["header_path"]), book_groups)
    file_io.with_tmp_openw(paths["output_path"], {}, _write_lines, writer.out)
    osis_runner.assert_is_valid_osis_according_to_xsd(
        paths["output_path"], paths["xsd_path"], paths["xml_xsd_path"]
    )


def _write_lines(lines, out_fp):
    out_fp.write("\n".join(lines) + "\n")


def _header_lines(header_path):
    """The hand-written header, checked to be one header element, indented two tabs."""
    if ET.parse(header_path).getroot().tag != "header":
        raise ValueError(f"{header_path} is not a header element")
    with open(header_path, encoding="utf-8") as header_fp:
        text = header_fp.read()
    if "\r" in text or text.startswith("\N{ZERO WIDTH NO-BREAK SPACE}"):
        raise ValueError(f"{header_path} has a CR or a BOM")
    return ["\t\t" + line for line in text.rstrip("\n").split("\n")]


def _scopes(verses, structure):
    """Each section's scope: Torah parashot by verse, Psalms divisions by chapter."""
    by_book = {}
    for verse in verses:
        if verse.get("contents-corresponds-to") != morphhb_notes.PLACEHOLDER:
            by_book.setdefault(verse["osisID"].split(".")[0], []).append(verse)
    scopes = {}
    for book in _TORAH:
        ids = [verse["osisID"] for verse in by_book[book]]
        starts = [osis_id for osis_id in ids if osis_id in structure.parashot]
        if starts[0] != ids[0]:
            raise ValueError(f"{book} does not open with a parashah")
        ends = [ids[ids.index(start) - 1] for start in starts[1:]] + [ids[-1]]
        scopes.update(zip(starts, (f"{s}-{e}" for s, e in zip(starts, ends))))
    if sorted(scopes) != sorted(structure.parashot):
        raise ValueError("A parashah start is not a BHS verse of the Torah")
    last_psalm = int(by_book["Ps"][-1]["osisID"].split(".")[1])
    firsts = sorted(structure.psalms_divisions)
    lasts = [first - 1 for first in firsts[1:]] + [last_psalm]
    for first, last in zip(firsts, lasts):
        scopes[first] = f"Ps.{first}-Ps.{last}"
    poetic = {v["osisID"] for v in verses if morphhb_plus.is_poetic(v["osisID"])}
    if poetic != set(structure.poetic_streams):
        raise ValueError("plus/ and MAM-simple disagree on the poetic verses")
    return scopes


def _numeral(number):
    return hebrew_verse_numerals.INT_TO_STR_DIC[number]


class _Writer:
    """Accumulate the output lines, tracking the open containers and pending break."""

    def __init__(self, structure, notes, scopes):
        self.out = []
        self.structure = structure
        self.notes = notes
        self.scopes = scopes
        self.pending = None  # the break before the next verse
        self.at_line_start = True
        self.lg_open = False
        self.section_open = False
        self.section_opened_at = None

    def line(self, depth, text):
        self.out.append("\t" * depth + text)

    def document(self, header_lines, book_groups):
        self.out.append('<?xml version="1.0" encoding="utf-8"?>')
        self.out.append(
            '<osis xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            f' xmlns="{osisn.NS_URL_FOR_OSIS}"'
            f' xsi:schemaLocation="{osisn.NS_URL_FOR_OSIS} {osisn.XSD_URL_FOR_OSIS}">'
        )
        self.line(1, '<osisText xml:lang="he" osisIDWork="MAPM">')
        self.out.extend(header_lines)
        self.line(1, '<div type="bookGroup">')
        self.line(2, f"<title>{_WHOLE_TITLE}</title>")
        for group_index, (scope, title, names) in enumerate(_TOP_GROUPS):
            self.line(2, f'<div type="bookGroup" scope="{scope}">')
            self.line(2, f"<title>{title}</title>")
            for name in names:
                # The last book's closing line also closes its top group and, at the
                # end, the outer group; book24 adds its own group, if it has one.
                closers = 1
                if name == names[-1]:
                    closers += 1
                    if group_index == len(_TOP_GROUPS) - 1:
                        closers += 1
                self.book24(name, book_groups[name], closers)
        self.out[-1] += "</osisText>"
        self.out.append("</osis>")
        if self.pending is not None:
            raise ValueError(f"A {self.pending} break after the last verse")

    def book24(self, name, node, closers):
        book39s = [c for c in mam_simple_json.children(node) if c["type"] == "book39"]
        nested = len(book39s) > 1
        if nested:
            title = self.structure.book24_titles[book39s[0]["osisID"]]
            self.line(2, f'<div type="bookGroup" scope="{name}">')
            self.line(2, f"<title>{title}</title>")
        for child in mam_simple_json.children(node):
            if child["type"] != "book39":
                self.marker(child)
                continue
            osis_id = child["osisID"]
            if not nested:
                title = self.structure.book24_titles[osis_id]
            elif name == "Hos-Mal":
                title = self.structure.twelve_titles[osis_id]
            else:
                title = None
            extra = closers if child is book39s[-1] else 0
            self.book39(child, title, extra + (1 if nested and extra else 0))

    def book39(self, node, title, closers):
        osis_id = node["osisID"]
        kind = "torah" if osis_id in _TORAH else "psalms" if osis_id == "Ps" else ""
        self.line(2, f'<div type="book" osisID="{osis_id}">')
        if title is not None:
            self.line(3, f"<title>{title}</title>")
        for child in mam_simple_json.children(node):
            if child["type"] == "chapter":
                self.chapter(child, kind)
            else:
                self.marker(child)
        if self.section_open:
            if kind == "torah":
                self.line(4, "</p>")
            self.line(3, "</div>")
            self.section_open = False
        self.line(2, "</div>" * max(closers, 1))

    def chapter(self, node, kind):
        ch_id = node["osisID"]
        chnu = int(ch_id.split(".")[1])
        start = f'<chapter osisID="{ch_id}" sID="{ch_id}" n="{_numeral(chnu)}"/>'
        if kind == "torah":
            first = f"{ch_id}.1"
            if first in self.structure.parashot:
                self.open_torah_section(first)
            self.line(4, start)
        else:
            if kind == "psalms" and chnu in self.structure.psalms_divisions:
                if self.section_open:
                    self.line(3, "</div>")
                self.line(3, f'<div type="section" scope="{self.scopes[chnu]}">')
                self.line(4, f"<title>{self.structure.psalms_divisions[chnu]}</title>")
                self.section_open = True
            self.line(3, start)
            self.line(4, "<p>")
            self.at_line_start = True
        for child in mam_simple_json.children(node):
            if child["type"] == "verse":
                self.verse(child, kind)
            else:
                self.marker(child)
        if kind == "torah":
            self.line(4, f'<chapter eID="{ch_id}"/>')
        else:
            self.close_lg()
            self.line(4, "</p>")
            self.line(3, f'<chapter eID="{ch_id}"/>')

    def open_torah_section(self, first):
        if self.section_open:
            self.line(4, "</p>")
            self.line(3, "</div>")
        self.line(3, f'<div type="section" scope="{self.scopes[first]}">')
        self.line(4, f"<title>{self.structure.parashot[first]}</title>")
        self.line(4, "<p>")
        self.section_open = True
        self.section_opened_at = first
        self.at_line_start = True

    def marker(self, node):
        if node["type"] not in _MARKERS or mam_simple_json.attributes(node):
            raise ValueError(f"Unexpected structural MAM-simple node: {node}")
        if mam_simple_json.children(node):
            raise ValueError(f"Marker with children: {node}")
        self.set_pending(_MARKERS[node["type"]])

    def set_pending(self, kind):
        if self.pending is not None:
            raise ValueError(f"Two breaks between verses: {self.pending}, {kind}")
        self.pending = kind

    def verse(self, node, kind):
        attrs = mam_simple_json.attributes(node)
        if set(attrs) - _VERSE_FIELDS:
            raise ValueError(f"Unexpected verse fields: {sorted(attrs)}")
        for field in ("starts-with-sampe", "ends-with-sampe"):
            if attrs.get(field, "pe2") not in _SAMPE_VALUES:
                raise ValueError(f"Unexpected {field}: {attrs[field]}")
        osis_id = attrs["osisID"]
        if attrs.get("contents-corresponds-to") == morphhb_notes.PLACEHOLDER:
            return  # BHS's Joshua 21:36-37, which MAM lacks; its breaks carry on
        if kind == "torah" and osis_id in self.structure.parashot:
            if self.section_opened_at != osis_id:
                self.open_torah_section(osis_id)
        pending, self.pending = self.pending, None
        children = inl.verse_children(node)
        if morphhb_plus.is_poetic(osis_id):
            self.poetic_verse(osis_id, children, pending)
        else:
            self.prose_verse(osis_id, children, pending)

    def start_milestone(self, osis_id):
        vrnu = int(osis_id.split(".")[2])
        return f'<verse osisID="{osis_id}" sID="{osis_id}" n="{_numeral(vrnu)}"/>'

    def write_lbs(self, kind, depth):
        for _ in range(_LB_COUNTS[kind]):
            self.line(depth, "<lb/>")
        if _LB_COUNTS[kind]:
            self.at_line_start = True

    def close_lg(self):
        if self.lg_open:
            self.line(5, "</lg>")
            self.lg_open = False
            self.at_line_start = True

    def prose_verse(self, osis_id, children, pending):
        self.close_lg()
        self.write_lbs(pending, 5)
        if pending is None:
            lead = "" if self.at_line_start else " "
        else:
            lead = _BREAK_LEADS[pending]
        pieces = [piece for child in children for piece in inl.render(child)]
        pieces, trailing = _hoist_trailing_break(pieces)
        segments = _split_at_breaks(pieces)
        if osis_id in self.notes:
            segments[-1][1].append(inl.note("variant", [self.notes[osis_id]]))
        start = self.start_milestone(osis_id)
        end = f'<verse eID="{osis_id}"/>'
        single = len(segments) == 1
        self.line(
            5, start + lead + inl.to_xml(segments[0][1]) + (end if single else "")
        )
        for kind, seg_pieces in segments[1:]:
            self.write_lbs(kind, 5)
            self.line(5, _BREAK_LEADS[kind] + inl.to_xml(seg_pieces))
        if not single:
            self.line(5, end)
        self.at_line_start = False
        if trailing is not None:
            self.set_pending(trailing)

    def poetic_verse(self, osis_id, children, pending):
        if _LB_COUNTS[pending]:
            self.close_lg()
            self.write_lbs(pending, 5)
        if not self.lg_open:
            self.line(5, "<lg>")
            self.lg_open = True
        lead = _BREAK_LEADS[pending] if pending is not None else ""
        stream_info = self.structure.poetic_streams[osis_id]
        lines = morphhb_poetry.poetic_lines(osis_id, children, stream_info)
        last = len(lines) - 1
        for index, (level, line_children) in enumerate(lines):
            pieces = [piece for child in line_children for piece in inl.render(child)]
            if any(isinstance(piece, inl.Break) for piece in pieces):
                raise ValueError(f"A break inside poetic verse {osis_id}")
            pieces = _strip(pieces, left=index > 0, right=index < last)
            if index == last and osis_id in self.notes:
                pieces.append(inl.note("variant", [self.notes[osis_id]]))
            head = self.start_milestone(osis_id) + lead if index == 0 else ""
            tail = f'<verse eID="{osis_id}"/>' if index == last else ""
            body = head + inl.to_xml(pieces) + tail
            self.line(6, f'<l level="{level}">{body}</l>')
        self.at_line_start = False


def _hoist_trailing_break(pieces):
    """A break at a verse's end, followed by nothing but notes, becomes a break between
    verses: in Exodus 33:23 and Leviticus 7:21 and 7:27 the petuḥah is the target of a
    scroll-difference note, which stays at the end of the verse."""
    breaks = [i for i, piece in enumerate(pieces) if isinstance(piece, inl.Break)]
    if not breaks:
        return pieces, None
    last = breaks[-1]
    after = pieces[last + 1 :]
    if not all(isinstance(p, inl.Elem) and p.tag == "note" for p in after):
        return pieces, None
    return pieces[:last] + after, pieces[last].kind


def _split_at_breaks(pieces):
    """[(break kind before the segment, or None, pieces), ...], edges stripped."""
    segments = [(None, [])]
    for piece in pieces:
        if isinstance(piece, inl.Break):
            segments.append((piece.kind, []))
        else:
            segments[-1][1].append(piece)
    last = len(segments) - 1
    stripped = []
    for index, (kind, seg_pieces) in enumerate(segments):
        seg_pieces = _strip(seg_pieces, left=index > 0, right=index < last)
        if not seg_pieces:
            raise ValueError(f"Empty verse segment beside a {kind} break")
        stripped.append((kind, seg_pieces))
    return stripped


def _strip(pieces, left, right):
    """Drop the ASCII spaces at a line's cut edges."""
    pieces = list(pieces)
    if right:
        while pieces and isinstance(pieces[-1], str):
            pieces[-1] = pieces[-1].rstrip(" ")
            if pieces[-1]:
                break
            pieces.pop()
    if left:
        while pieces and isinstance(pieces[0], str):
            pieces[0] = pieces[0].lstrip(" ")
            if pieces[0]:
                break
            pieces.pop(0)
    return pieces
