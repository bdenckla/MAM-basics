"""Differential: uni_norm_fragile's model of HarfBuzz's mark order, against HarfBuzz.

WHY THIS EXISTS

``py/mb_cmn/uni_norm_fragile.py`` calls a string fragile when normalization to NFC or
HarfBuzz's mark reordering would change the order of the marks below a letter, or of
the marks above it. Its ``hb_mark_order`` models HarfBuzz's reordering from HarfBuzz
15.0.0's source. The model is worth having only if it matches HarfBuzz, so this test
shapes the same text with HarfBuzz itself, through uharfbuzz, and requires the same
order. Ben approved adding uharfbuzz for this test on 2026-10-28, among the defaults
of the same-zone definition of fragility.

HOW HARFBUZZ'S ORDER IS READ

The font is synthetic: an empty face whose only glyphs are one for each character of
the text being shaped, numbered by code point. With no glyphs for the Hebrew
presentation forms, ``compose_hebrew`` composes no letter with a mark, and with no
dotted circle HarfBuzz inserts none. The buffer keeps default ignorables, so a CGJ
stays a glyph, and its cluster level is CHARACTERS, so each glyph's cluster is the
index of its character in the text. The glyphs of a right-to-left buffer come out in
reverse, so their clusters read backwards give the order HarfBuzz hands a font. Every
text shaped must come out as one glyph per character.

WHAT IT COVERS

1. Every ordered pair and triple of the Hebrew marks on one letter, with and without
   a CGJ between two of them.
2. Every distinct atom of ``MAM-parsed/plus/``, ``out/near-aleppo/plus/`` and
   ``uxlc/out/uxlc-words.json``, as stored and without the marks fragility drops.

A third test checks the zone table against Unicode's combining classes.

A MISSING UHARFBUZZ, ANOTHER HARFBUZZ VERSION, OR A MISSING INPUT FAILS RATHER THAN
SKIPS. The model's comments cite HarfBuzz 15.0.0's source by line, so a uharfbuzz
that bundles another HarfBuzz needs those citations rechecked before
``_HARFBUZZ_VERSION`` moves.
"""

import itertools
import json
import re
import unicodedata

import uharfbuzz as hb

from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
from mb_cmn import str_defs as sd
from mb_cmn import uni_norm_fragile as unf

_HARFBUZZ_VERSION = "15.0.0"
_LETTER = "\N{HEBREW LETTER LAMED}"
# Every Hebrew mark: each character of the Hebrew blocks that has a nonzero class in
# Python's unicodedata, and the two marks that Unicode 18.0.0 added.
_MARKS = tuple(
    sorted(
        {
            char
            for char in map(chr, [*range(0x0591, 0x05C8), 0xFB1E])
            if unicodedata.combining(char)
        }
        | {hpo.SHEVA_NA, hpo.DAGESH_XAZAQ}
    )
)
_CORPORA = ("MAM-parsed/plus", "out/near-aleppo/plus", "uxlc/out/uxlc-words.json")
_HEBREW_LETTER = re.compile("[א-ת]")
_ATOM_SEPARATORS = re.compile(f"[\\s{hpu.MAQ}]+")
# Texts shaped in one buffer, joined by spaces. A space has class 0, so no run of
# marks crosses from one text to the next.
_CHUNK = 2000
# Unicode's classes for marks below a letter and above it.
_BELOW_CLASSES = {*range(10, 19), 20, 22, 220, 222}
_ABOVE_CLASSES = {19, 26, 228, 230}


class _Shaper:
    """Shape text with a font that has a glyph for each of the text's characters."""

    def __init__(self):
        self._codes = frozenset()
        funcs = hb.FontFuncs()
        funcs.set_nominal_glyph_func(self._nominal_glyph, None)
        self._font = hb.Font(hb.Face(b""))
        self._font.funcs = funcs

    def _nominal_glyph(self, _font, code, _user_data):
        return code if code in self._codes else 0

    def mark_order(self, text):
        """Return the text in the order HarfBuzz hands its characters to a font."""
        codes = list(map(ord, text))
        self._codes = frozenset(codes)
        buf = hb.Buffer()
        buf.add_codepoints(codes)
        buf.direction = "rtl"
        buf.script = "Hebr"
        buf.language = "he"
        buf.cluster_level = hb.BufferClusterLevel.CHARACTERS
        buf.flags = hb.BufferFlags.PRESERVE_DEFAULT_IGNORABLES
        hb.shape(self._font, buf, {})
        clusters = [info.cluster for info in reversed(buf.glyph_infos)]
        assert sorted(clusters) == list(range(len(text))), _describe([text])
        return "".join(text[cluster] for cluster in clusters)


def _mismatches(texts):
    """Return the texts whose order hb_mark_order and HarfBuzz disagree on."""
    shaper = _Shaper()
    out = []
    for start in range(0, len(texts), _CHUNK):
        chunk = texts[start : start + _CHUNK]
        joined = " ".join(chunk)
        if shaper.mark_order(joined) == unf.hb_mark_order(joined):
            continue
        singles = [t for t in chunk if shaper.mark_order(t) != unf.hb_mark_order(t)]
        out.extend(singles or [joined])
    return out


def _describe(texts):
    shown = [" ".join(f"{ord(char):04X}" for char in text) for text in texts[:10]]
    return f"{len(texts)} texts, the first {len(shown)} as code points: {shown}"


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _strings(value)


def _atoms(rel):
    path = paths.repo_root() / rel
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    assert files and all(file.is_file() for file in files), f"missing input: {rel}"
    atoms = set()
    for file in files:
        for string in _strings(json.loads(file.read_text(encoding="utf-8"))):
            atoms.update(
                atom
                for atom in _ATOM_SEPARATORS.split(string)
                if _HEBREW_LETTER.search(atom)
            )
    assert atoms, f"no atoms in {rel}"
    return atoms


def test_harfbuzz_is_the_version_the_model_cites():
    assert hb.version_string() == _HARFBUZZ_VERSION, (
        f"uharfbuzz bundles HarfBuzz {hb.version_string()}, but uni_norm_fragile.py"
        f" cites HarfBuzz {_HARFBUZZ_VERSION}'s source by line. Recheck the"
        " citations against the new version before changing _HARFBUZZ_VERSION."
    )


def test_mark_pairs_and_triples_on_one_letter():
    assert set(unf._ZONES) <= set(_MARKS)
    texts = []
    for first, second in itertools.product(_MARKS, repeat=2):
        texts.append(_LETTER + first + second)
        texts.append(_LETTER + first + sd.CGJ + second)
    for first, second, third in itertools.product(_MARKS, repeat=3):
        texts.append(_LETTER + first + second + third)
        texts.append(_LETTER + first + sd.CGJ + second + third)
        texts.append(_LETTER + first + second + sd.CGJ + third)
    bad = _mismatches(texts)
    assert not bad, _describe(bad)


def test_corpus_atoms():
    atoms = set()
    for rel in _CORPORA:
        atoms |= _atoms(rel)
    dropped = {unf.get_fragile_comps(atom)[0] for atom in atoms}
    bad = _mismatches(sorted(atoms | dropped))
    assert not bad, _describe(bad)


def test_zone_table_agrees_with_unicode_classes():
    """Lint: each mark's zone fits its Unicode class, and only known marks lack one.

    The marks fragility drops need no zone, and dagesh xazaq, which sits inside the
    letter, has none on purpose.
    """
    wrong = []
    for mark, zone in unf._ZONES.items():
        unicode_class = unf._UNICODE_18_CLASSES.get(mark) or unicodedata.combining(mark)
        expected = _BELOW_CLASSES if zone == unf._BELOW else _ABOVE_CLASSES
        if unicode_class not in expected:
            wrong.append(f"U+{ord(mark):04X} class {unicode_class} is not {zone}")
    unzoned = [
        f"U+{ord(mark):04X}"
        for mark in _MARKS
        if mark not in unf._ZONES
        and mark.translate(unf._DROP_TABLE)
        and mark != hpo.DAGESH_XAZAQ
    ]
    assert not wrong and not unzoned, (wrong, unzoned)
