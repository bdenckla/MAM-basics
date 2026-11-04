"""Render MAM-simple verse content as MAM-morphhb's inline OSIS, by closed dispatch.

Exports Elem, Break, render, verse_children, to_xml and the space constants.

Each handler returns a list of pieces: a string, an ``Elem`` (an inline OSIS element) or
a ``Break`` (a petuḥah, pe3 or setumah inside a verse, which the writer turns into
``<lb/>`` lines).  The handlers follow ``py/osis/osis_handlers.py`` except where the
2014 form of morphhb's ``MAPM/MAPM.xml`` differs, as MAM-morphhb/README.md describes:
the qere is marked, a paseq is the 2014 ``x-paseq`` seg without MAM-OSIS's note, and
the setumah, shirah and inverted-nun spaces are the 2014 file's spaces.
"""

import dataclasses
from xml.sax.saxutils import escape

from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import mam_simple_json
from mb_cmn import str_defs as sd
from mb_cmn.silluq_before_meteg import validate_silluq_before_meteg
from mb_misc import slh_description

EMSP = "\N{EM SPACE}"
IDEOSP = "\N{IDEOGRAPHIC SPACE}"
TWO_EMSP = EMSP * 2


@dataclasses.dataclass(frozen=True)
class Elem:
    """An inline OSIS element: a seg or a note."""

    tag: str
    attrs: tuple  # ((name, value), ...)
    kids: tuple


@dataclasses.dataclass(frozen=True)
class Break:
    """A break inside a verse: "pe2", "pe3" or "samekh2"."""

    kind: str


def verse_children(verse):
    """Return a verse's children, its direct text read as one text child."""
    attrs = mam_simple_json.attributes(verse)
    if "text" in attrs:
        return [{"type": "text", "text": attrs["text"]}]
    return mam_simple_json.children(verse)


def render(node, handlers=None):
    """Return the pieces for one MAM-simple node, raising on an unknown type/class."""
    handlers = HANDLERS if handlers is None else handlers
    attrs = mam_simple_json.attributes(node)
    key = node["type"], attrs.get("class")
    if key not in handlers:
        raise ValueError(f"Unhandled MAM-simple JSON type/class: {key}")
    child_handlers = _HANDLERS_INSIDE_NOTE if key == ("sdt-note", None) else HANDLERS
    per_child = [
        render(child, child_handlers) for child in mam_simple_json.children(node)
    ]
    if "text" in attrs:
        assert not per_child
        kids = [attrs["text"]]
    else:
        kids = [piece for pieces in per_child for piece in pieces]
    return handlers[key](node, kids, per_child)


def to_xml(pieces):
    """Serialize pieces; a Break must have been taken out first."""
    out = []
    for piece in pieces:
        if isinstance(piece, str):
            out.append(escape(piece))
        elif isinstance(piece, Elem):
            if not piece.kids:
                raise ValueError(f"Empty inline element: {piece}")
            attrs = "".join(f' {name}="{_attr(value)}"' for name, value in piece.attrs)
            out.append(f"<{piece.tag}{attrs}>{to_xml(piece.kids)}</{piece.tag}>")
        else:
            raise TypeError(f"Not serializable inline: {piece!r}")
    return "".join(out)


def _attr(value):
    if any(ch in value for ch in '"<&'):
        raise ValueError(f"Attribute value needs escaping: {value!r}")
    return value


def seg(seg_type, kids):
    return Elem("seg", (("type", seg_type),), tuple(kids))


def note(note_type, kids):
    return Elem("note", (("type", note_type),), tuple(kids))


# node: MAM-simple JSON node
# kids: pieces for all children, summed together
# per_child: pieces for all children, per child


def _text(node, kids, _per_child):
    return kids


def _pass_thru(_node, kids, _per_child):
    return kids


def _empty(_node, _kids, _per_child):
    return []


def _silluq_before_meteg(node, kids, _per_child):
    validate_silluq_before_meteg(node["text"], node["letters-with-silluq"])
    return [*kids, note("x-silluq-before-meteg", ["סילוק לפני געיה"])]


def _good_ending(_node, kids, _per_child):
    return [" ", seg("x-good-ending", kids)]


def _letter_small(_node, kids, _per_child):
    return [seg("x-small", kids)]


def _letter_large(_node, kids, _per_child):
    return [seg("x-big", kids)]


def _letter_hung(_node, kids, _per_child):
    # The 2014 file's name for a hung letter; MAM-OSIS has "x-hung".
    return [seg("x-suspended", kids)]


def _ketiv_qere(node, _kids, per_child):
    """A ketiv/qere pair, in MAM-simple's order."""
    kinds = [child["type"] for child in node["contents"]]
    if sorted(kinds) != ["kq-k", "kq-q"]:
        raise ValueError(f"Unexpected ketiv/qere parts: {kinds}")
    separator = {"sep-maqaf": hpu.MAQ, None: " "}[node.get("class")]
    return [*per_child[0], separator, *per_child[1]]


def _ketiv(_node, kids, _per_child):
    return [seg("x-ketiv", kids)]


def _qere(_node, kids, _per_child):
    return [seg("x-qere", kids)]


def _ketiv_velo_qere(_node, kids, _per_child):
    return [seg("x-ketiv-velo-qere", ["(", *kids, ")"])]


def _ketiv_velo_qere_maq(_node, _kids, _per_child):
    return [hpu.MAQ]


def _qere_velo_ketiv(_node, kids, _per_child):
    return [seg("x-qere-velo-ketiv", ["[", *kids, "]"])]


def _break(node, _kids, _per_child):
    kind = {"spi-pe2": "pe2", "spi-pe3": "pe3", "spi-samekh2": "samekh2"}
    return [Break(kind[node["type"]])]


def _samekh3(_node, _kids, _per_child):
    return [TWO_EMSP]


def _space_seg(_node, _kids, _per_child):
    """A shirah space, or a setumah beside Numbers 10's inverted nuns."""
    return [seg("x-space", [TWO_EMSP])]


def _invnun(node, _kids, _per_child):
    trailing = {"including-trailing-space": [" "], None: []}[node.get("class")]
    return [seg("x-reversednun", [hpu.NUN_HAF]), *trailing]


def _legarmeih(_node, _kids, _per_child):
    # The text after a legarmeh supplies its space, as in the 2014 file.
    return [sd.NBSP + hpu.PASOLEG]


def _paseq(_node, _kids, _per_child):
    return [sd.NBSP, seg("x-paseq", [hpu.PASOLEG]), " "]


def _implicit_maqaf(_node, _kids, _per_child):
    return [seg("x-implicit-maqaf", [hpu.MAQ])]


def _cant_all_three(node, kids, _per_child):
    kinds = [child["type"] for child in node["contents"]]
    if kinds != ["cant-combined", "cant-alef", "cant-bet"]:
        raise ValueError(f"Unexpected dual-cantillation parts: {kinds}")
    return kids


def _scrdfftar(node, _kids, per_child):
    kinds = [child["type"] for child in node["contents"]]
    if kinds != ["sdt-target", "sdt-note"]:
        raise ValueError(f"Unexpected scroll-difference parts: {kinds}")
    target, note_kids = per_child
    the_note = note("x-scroll-difference", note_kids)
    starpos = node["sdt-starpos"]
    if starpos == "before-word":
        return [the_note, *target]
    if starpos == "after-word":
        return [*target, the_note]
    raise ValueError(f"Unexpected sdt-starpos: {starpos}")


def _slh_word(node, kids, _per_child):
    desc3 = slh_description.desc3_decoded_from_a_str(node["slhw-desc-3"])
    desc_parts = (
        node["slhw-desc-0"],
        node["slhw-desc-1"],
        node["slhw-desc-2"],
        desc3,
    )
    desc_str = slh_description.desc_parts_shown_as_a_str(desc_parts)
    return [*kids, note("x-slh-word", [desc_str])]


HANDLERS = {
    ("text", None): _text,
    ("silluq-before-meteg", None): _silluq_before_meteg,
    #
    ("good-ending", None): _good_ending,
    ("letter-small", None): _letter_small,
    ("letter-large", None): _letter_large,
    ("letter-hung", None): _letter_hung,
    #
    ("kq-k-velo-q", None): _ketiv_velo_qere,
    ("kq-k-velo-q-maq", None): _ketiv_velo_qere_maq,
    ("kq-q-velo-k", None): _qere_velo_ketiv,
    ("kq", None): _ketiv_qere,
    ("kq", "sep-maqaf"): _ketiv_qere,
    ("kq-k", None): _ketiv,
    ("kq-q", None): _qere,
    ("kq-trivial", None): _pass_thru,
    #
    ("cant-combined", None): _pass_thru,
    ("cant-alef", None): _empty,
    ("cant-bet", None): _empty,
    ("cant-all-three", None): _cant_all_three,
    #
    ("spi-samekh2", None): _break,
    ("spi-samekh3", None): _samekh3,
    ("spi-samekh3", "nu10-invnun-neighbor"): _space_seg,
    ("spi-pe2", None): _break,
    ("spi-pe3", None): _break,
    ("spi-invnun", None): _invnun,
    ("spi-invnun", "including-trailing-space"): _invnun,
    ("shirah-space", None): _space_seg,
    ("lp-legarmeih", None): _legarmeih,
    ("lp-paseq", None): _paseq,
    ("implicit-maqaf", None): _implicit_maqaf,
    #
    ("scrdfftar", None): _scrdfftar,
    ("sdt-target", None): _pass_thru,
    ("sdt-note", None): _pass_thru,
    #
    ("slh-word", None): _slh_word,
}
_HANDLERS_INSIDE_NOTE = {
    **HANDLERS,
    # No note within a note: a special-letter word inside a scroll-difference note
    # passes through, as in MAM-OSIS.
    ("slh-word", None): _pass_thru,
}
