"""Place plus/'s poetic line breaks on MAM-simple's text, raising on any misfit.

Exports poetic_lines.

plus/ holds MAM's poetic line breaks (ר1, ר2, ר3) and MAM-simple holds the text that
MAM-morphhb writes.  Both are projected to one token sequence: an atom's letters, its
marks dropped, or an opaque token for a ketiv/qere, a word with a special letter or a
silluq-before-meteg word.  The two sequences must be equal; a break before token i in
plus/ then starts a line before token i of MAM-simple's text.  A break at either edge
of a verse, or one that falls inside a MAM-simple container such as a scroll
difference's target, raises.
"""

import re

from mam_morphhb import morphhb_inline
from mam_morphhb import morphhb_plus

_LETTER = re.compile("[\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
_SEP_CHARS = frozenset(
    " "
    "\N{NO-BREAK SPACE}"
    "\N{EM SPACE}"
    "\N{IDEOGRAPHIC SPACE}"
    "\N{THIN SPACE}"
    "\N{HEBREW PUNCTUATION MAQAF}"
    "\N{HEBREW PUNCTUATION PASEQ}"
    "\N{HEBREW PUNCTUATION SOF PASUQ}"
    "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
)
_ATOMS = {
    "kq": morphhb_plus.KQ_TOKEN,
    "kq-trivial": morphhb_plus.KQ_TOKEN,
    "kq-k-velo-q": morphhb_plus.KQ_TOKEN,
    "kq-q-velo-k": morphhb_plus.KQ_TOKEN,
    "slh-word": morphhb_plus.SLH_TOKEN,
    "silluq-before-meteg": morphhb_plus.SBM_TOKEN,
}
_SEPS = {
    "lp-paseq",
    "lp-legarmeih",
    "implicit-maqaf",
    "kq-k-velo-q-maq",
    "spi-invnun",
    "spi-pe2",
    "spi-pe3",
    "spi-samekh2",
    "spi-samekh3",
    "shirah-space",
}


def poetic_lines(osis_id, children, stream_info):
    """Split a poetic verse's children into lines; return [(level, children), ...].

    ``stream_info`` is plus/'s (column C level or None, column E stream) for the verse.
    A text child cut by a break becomes two text children.
    """
    first_level, plus_items = stream_info
    plus_tokens, breaks, _plus_starts = _tokens(plus_items)
    simple_tokens, simple_breaks, starts = _tokens(_simple_items(children))
    assert not simple_breaks
    if plus_tokens != simple_tokens:
        raise ValueError(f"plus/ and MAM-simple tokens differ at {osis_id}")
    cuts, levels = [], [first_level or 1]
    for index, level in breaks:
        if index in (0, len(simple_tokens)):
            raise ValueError(f"Line break at the edge of {osis_id}")
        start = starts[index]
        if start is None:
            raise ValueError(f"Line break inside a container at {osis_id}")
        if cuts and start <= cuts[-1]:
            raise ValueError(f"Line breaks out of order at {osis_id}")
        cuts.append(start)
        levels.append(level)
    return list(zip(levels, _split(children, cuts)))


def _simple_items(children):
    """Project MAM-simple children as plus_stream projects plus/, with positions:
    (child index, offset) for a top-level text character or atom, None inside one."""
    items = []
    for index, child in enumerate(children):
        kind = child["type"]
        if kind == "text":
            items.extend(("char", ch, (index, k)) for k, ch in enumerate(child["text"]))
        elif kind in _ATOMS:
            items.append(("atom", _ATOMS[kind], (index, 0)))
        elif kind in _SEPS:
            items.append(("sep", None, None))
        elif kind == "scrdfftar":
            target = [c for c in child["contents"] if c["type"] == "sdt-target"]
            for sub in morphhb_inline.verse_children(target[0]):
                inner = _simple_items([sub])
                items.extend((k, v, None) for k, v, _pos in inner)
        else:
            raise ValueError(f"Unhandled MAM-simple type in poetry: {kind}")
    return items


def _tokens(items):
    """Return (tokens, breaks, starts) for plus_stream items or MAM-simple items.

    breaks is [(token index, level), ...], from plus/ items only; starts is each
    token's start position, from MAM-simple items only.
    """
    tokens, breaks, starts = [], [], []
    current, current_start = [], None

    def flush():
        if current:
            skeleton = "".join(_LETTER.findall("".join(current)))
            if skeleton:
                tokens.append(skeleton)
                starts.append(current_start)
            current.clear()

    for item in items:
        kind, value = item[0], item[1]
        position = item[2] if len(item) > 2 else None
        if kind in ("text", "char"):
            for ch in value:
                if ch in _SEP_CHARS:
                    flush()
                else:
                    if not current:
                        current_start = position
                    current.append(ch)
        elif kind == "sep":
            flush()
        elif kind == "atom":
            flush()
            tokens.append(value)
            starts.append(position)
        elif kind == "break":
            flush()
            breaks.append((len(tokens), value))
        else:
            raise ValueError(f"Unexpected token item kind: {kind}")
    flush()
    return tokens, breaks, starts


def _split(children, cuts):
    """Cut children before each (child index, offset) in cuts."""
    segments = [[]]
    pending = list(cuts)
    for index, child in enumerate(children):
        if child["type"] == "text":
            text, begin = child["text"], 0
            while pending and pending[0][0] == index:
                offset = pending.pop(0)[1]
                if offset > begin:
                    segments[-1].append({"type": "text", "text": text[begin:offset]})
                segments.append([])
                begin = offset
            if begin < len(text):
                segments[-1].append({"type": "text", "text": text[begin:]})
        else:
            if pending and pending[0][0] == index:
                if pending.pop(0)[1] != 0:
                    raise ValueError("A cut inside a non-text child")
                segments.append([])
            segments[-1].append(child)
    if pending:
        raise ValueError(f"Unused line cuts: {pending}")
    return segments
