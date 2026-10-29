"""Static lint: the glyphs of one Hebrew letter agree on their mark-to-base anchors.

A letter can be drawn by several glyphs: a plain one, mapped from the letter's code point,
and variants that GSUB substitutes when a vowel, dagesh or dot is present (alef, alef.con,
alefmapiq and alef.xolam, for example). Text with accents but no vowels reaches the plain
glyphs, which pointed text seldom does. So an anchor that a variant has and the plain glyph
lacks leaves an accent unattached in accent-only text alone. Before hbofonts commit d3ecd87,
the glyph alef had no anchor for yetiv and dexi, though alef.con and alefmapiq did.

The lint reads only the compiled font. For each mark glyph that a MarkBasePos lookup of the
'mark' feature attaches, every glyph of a letter's family must have an anchor for it if any
of them does, and all at the same point. A letter's family is its cmap glyph plus every glyph
other than a mark that GSUB substitutes for a member. A whole family without an anchor is
not a sibling gap and is not reported. Deliberate differences are listed, with their
reasons, in a closed table per font, and a listed difference that no longer occurs is
reported too.
"""

from collections import Counter, defaultdict
from pathlib import Path

from fontTools.ttLib import TTFont

_HEBREW_LETTERS = range(0x05D0, 0x05EB)  # alef through tav, final forms included
# A ligature substitution's output, such as betdagesh.xazaq, has GDEF class 2, ligature.
# HarfBuzz attaches marks to it as to a base, so a family takes every glyph not a mark.
_GDEF_MARK = 3
_GSUB_EXTENSION, _GPOS_EXTENSION = 7, 9
_GPOS_MARK_TO_BASE = 4
_IGNORE_MARKS_OR_FILTER = 0x0008 | 0x0010  # lookup flags this lint does not model

# Per font stem: {(glyph, mark glyphs): (the glyph's anchor, or None for none; reason)}
_EXCEPTIONS = {
    "Taamey_D": {
        ("alef.xolam", frozenset(("dexi", "yetiv"))): (
            None,
            "alef.xolam shows the xolam of the letter before it, so it never starts an"
            " atom: it never has the prepositive yetiv, and a dexi on it is a stress"
            " helper, drawn as topmeteg",
        ),
        ("vavxolam", frozenset(("pashta", "segolta", "telishaqetana", "tsinor"))): (
            (-75, 0),
            "vavxolam's postpositive anchor is 75 units left of the other vavs', to"
            " clear its xolam male dot",
        ),
    },
}


def lint(font_fna):
    """None if this font has no exception table; otherwise (findings, summary).

    The findings are strings, and there are none when every difference among the anchors of
    a letter's glyphs is a listed exception.
    """
    exceptions = _EXCEPTIONS.get(Path(font_fna).stem)
    if exceptions is None:
        return None
    ttfont = TTFont(font_fna)
    families = _letter_families(ttfont)
    anchors = _mark_to_base_anchors(ttfont["GPOS"].table)
    if not families or not anchors:
        raise ValueError(
            f"{font_fna}: no letter family or no mark-to-base anchor found"
        )
    findings, used = [], set()
    diffs = _differences(families, anchors)
    for key in sorted(diffs, key=lambda k: (k[0], k[1], k[4])):
        lookup_index, glyph, has, expected, letter = key
        marks = diffs[key]
        exception_key = (glyph, frozenset(marks))
        if exception_key in exceptions and exceptions[exception_key][0] == has:
            used.add(exception_key)
            continue
        mark_list = ", ".join(sorted(marks))
        if has is None:
            findings.append(
                f"{glyph} has no anchor for {mark_list}, where {letter}'s family"
                f" otherwise has {expected} (lookup {lookup_index})"
            )
        else:
            findings.append(
                f"{glyph} has {has} for {mark_list}, where {letter}'s family"
                f" otherwise has {expected} (lookup {lookup_index})"
            )
    for glyph, marks in sorted(exceptions.keys() - used, key=lambda k: k[0]):
        findings.append(
            f"the listed exception for {glyph} and {', '.join(sorted(marks))}"
            " no longer occurs; remove it from the table"
        )
    summary = (
        f"{len(families)} letter families, {len(anchors)} marks in mark-to-base lookups,"
        f" {len(used)} listed exceptions, {len(findings)} unexpected differences"
    )
    return findings, summary


def _subtables(lookup, extension_type):
    for subtable in lookup.SubTable:
        if lookup.LookupType == extension_type:
            yield subtable.ExtensionLookupType, subtable.ExtSubTable
        else:
            yield lookup.LookupType, subtable


def _substitution_edges(gsub):
    """(input glyph, output glyph) pairs; a ligature's input is its first component.

    Contextual lookups are skipped: the lookups they invoke are in the list themselves.
    """
    for lookup in gsub.LookupList.Lookup:
        for lookup_type, subtable in _subtables(lookup, _GSUB_EXTENSION):
            if lookup_type == 1:
                yield from subtable.mapping.items()
            elif lookup_type in (2, 3):
                mapping = subtable.mapping if lookup_type == 2 else subtable.alternates
                for src, dsts in mapping.items():
                    for dst in dsts:
                        yield src, dst
            elif lookup_type == 4:
                for first, ligatures in subtable.ligatures.items():
                    for ligature in ligatures:
                        yield first, ligature.LigGlyph
            elif lookup_type == 8:
                yield from zip(subtable.Coverage.glyphs, subtable.Substitute)
            elif lookup_type not in (5, 6):
                raise ValueError(f"unexpected GSUB lookup type {lookup_type}")


def _letter_families(ttfont):
    """{cmap glyph of a Hebrew letter: [the glyphs of its family]}"""
    gdef_class = ttfont["GDEF"].table.GlyphClassDef.classDefs
    cmap = ttfont.getBestCmap()
    family_of = {cmap[cp]: cmap[cp] for cp in _HEBREW_LETTERS if cp in cmap}
    edges = list(_substitution_edges(ttfont["GSUB"].table))
    grew = True
    while grew:
        grew = False
        for src, dst in edges:
            if src not in family_of or gdef_class.get(dst) == _GDEF_MARK:
                continue
            if dst not in family_of:
                family_of[dst] = family_of[src]
                grew = True
            elif family_of[dst] != family_of[src]:
                raise ValueError(
                    f"{dst} is substituted for {family_of[dst]} and for {family_of[src]}"
                )
    families = defaultdict(list)
    for glyph, letter in family_of.items():
        families[letter].append(glyph)
    return families


def _mark_to_base_anchors(gpos):
    """{(lookup index, mark glyph): {base glyph: (x, y)}} for the 'mark' feature.

    For each base, the anchor is that of the first subtable that attaches the mark to it,
    which is the one HarfBuzz uses.
    """
    indices = sorted(
        {
            index
            for record in gpos.FeatureList.FeatureRecord
            if record.FeatureTag == "mark"
            for index in record.Feature.LookupListIndex
        }
    )
    anchors = {}
    for lookup_index in indices:
        lookup = gpos.LookupList.Lookup[lookup_index]
        for lookup_type, subtable in _subtables(lookup, _GPOS_EXTENSION):
            if lookup_type != _GPOS_MARK_TO_BASE:
                continue
            if lookup.LookupFlag & _IGNORE_MARKS_OR_FILTER:
                raise ValueError(
                    f"lookup {lookup_index}: mark-to-base lookup flag"
                    f" {lookup.LookupFlag:#06x} is not modelled"
                )
            bases = list(
                zip(subtable.BaseCoverage.glyphs, subtable.BaseArray.BaseRecord)
            )
            marks = zip(subtable.MarkCoverage.glyphs, subtable.MarkArray.MarkRecord)
            for mark, mark_record in marks:
                hosts = anchors.setdefault((lookup_index, mark), {})
                for base, base_record in bases:
                    anchor = base_record.BaseAnchor[mark_record.Class]
                    if anchor is not None and base not in hosts:
                        hosts[base] = (anchor.XCoordinate, anchor.YCoordinate)
    return anchors


def _differences(families, anchors):
    """{(lookup index, glyph, its anchor, its family's anchor, cmap glyph): [marks]}

    A family's anchor is its cmap glyph's, or, where that glyph has none, the most common
    anchor among the family's glyphs.
    """
    found = defaultdict(list)
    for (lookup_index, mark), hosts in sorted(anchors.items()):
        for letter, glyphs in families.items():
            present = [hosts[glyph] for glyph in glyphs if glyph in hosts]
            if not present:
                continue
            expected = hosts.get(letter) or Counter(present).most_common(1)[0][0]
            for glyph in glyphs:
                if hosts.get(glyph) != expected:
                    key = (lookup_index, glyph, hosts.get(glyph), expected, letter)
                    found[key].append(mark)
    return found
