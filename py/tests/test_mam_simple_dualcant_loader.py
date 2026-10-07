"""Stage-1 of issue wlc-utils#36: the MAM-simple loader exposes the two detangled strands.

A ``cant-all-three`` span carries three single-cantillation projections
(``cant-combined`` / ``cant-alef`` / ``cant-bet``).  The loader must surface
``cant-alef`` and ``cant-bet`` as their own position-correct token streams,
interleaved with the single-cant ``text`` around the span -- not naively concatenate
all three (the pre-wlc-utils#36 behaviour, which tripled the dual span).

Gen 35:22 is the canonical mid-verse span: a single-cant prefix, the dual span, then a
single-cant suffix.  Its alef strand closes a chanted verse mid–numbered-verse (silluq +
sof pasuq on ישראל) and opens a second on the suffix; its bet strand runs the whole
numbered verse as one chanted verse (atnaX on ישראל, no sof pasuq).  This is exactly what
the detangler segments on.

The tests check two rules.  Over every verse of Genesis, Exodus and Deuteronomy, a verse has
two strand streams exactly where it has a ``cant-all-three`` span, and those two streams share
their letters.  And each Decalogue strand MAM-simple loads is MAM-parsed-plus's, mark for mark.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_mam_simple_dualcant_loader.py -v
"""

from __future__ import annotations

import json

import pytest

from accgram import decalogue_m_trad as dmt
from accgram import prose_filter
from accgram.mam_simple_verse import load_mam_simple_for_refs, mam_simple_json_path
from mb_cmn import paths
from mb_cmn.uni_denorm import give_std_mark_order
from mb_misc import osis_book_abbrevs as oba
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

# The books of issue wlc-utils#36's three dually-cantillated loci.
_BOOKS = ("gn", "ex", "dt")


def _verse(bb: str, chnu: int, vrnu: int) -> dict[str, object]:
    refs = {bb: {(chnu, vrnu)}}
    loaded = load_mam_simple_for_refs(
        paths.mam_simple_dir(), refs, include_strands=True
    )
    bcv = f"{bb}{chnu}:{vrnu}"
    assert bcv in loaded, f"{bcv} not loaded"
    return loaded[bcv]["mam_simple_verse"]


def _skels(vels: list[object]) -> list[str]:
    return [
        "".join(c for c in tok if "א" <= c <= "ת")
        for tok in vels
        if isinstance(tok, str)
    ]


def _nodes(value: object):
    """Every dictionary in a raw MAM-simple structure, at any depth."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _nodes(child)


def _raw_verses(bb: str) -> dict[tuple[int, int], dict]:
    """Every verse node of one book in its MAM-simple file, by (chapter, verse)."""
    bk39id = wlc_bb_to_bk39id(bb)
    prefix = f"{oba.BOOK_ABBREVS[bk39id]}."
    path = mam_simple_json_path(paths.mam_simple_dir(), bk39id)
    verses: dict[tuple[int, int], dict] = {}
    for node in _nodes(json.loads(path.read_text(encoding="utf-8"))):
        osis_id = node.get("osisID")
        if node.get("type") == "verse" and str(osis_id).startswith(prefix):
            _, chnu, vrnu = osis_id.split(".")
            verses[(int(chnu), int(vrnu))] = node
    assert verses, f"{path}: no {bb} verse"
    return verses


def test_strands_exposed_separately():
    verse = _verse("gn", 35, 22)
    assert set(verse) == {"vels", "vels_cant_alef", "vels_cant_bet"}

    alef = verse["vels_cant_alef"]
    bet = verse["vels_cant_bet"]

    # No longer the pre-wlc-utils#36 triple-concatenation: each strand is one word sequence
    # (single-cant prefix + its span words + single-cant suffix).
    assert all(isinstance(tok, str) for tok in alef)
    assert all(isinstance(tok, str) for tok in bet)
    assert _skels(alef) == _skels(bet)  # same letters


@pytest.mark.parametrize("bb", _BOOKS)
def test_strands_differ_exactly_where_a_verse_has_a_dual_span(bb):
    """Without a ``cant-all-three`` span a verse has one stream; with one, two.

    Without a span, the two strands and ``vels`` are the same stream.  With one, the strands
    differ, but their letters, joined across the verse, are the same.
    """
    raw = _raw_verses(bb)
    loaded = load_mam_simple_for_refs(
        paths.mam_simple_dir(), {bb: set(raw)}, include_strands=True
    )
    spans = 0
    for (chnu, vrnu), node in sorted(raw.items()):
        verse = loaded[f"{bb}{chnu}:{vrnu}"]["mam_simple_verse"]
        alef, bet = verse["vels_cant_alef"], verse["vels_cant_bet"]
        where = f"{bb} {chnu}:{vrnu}"
        if any(n.get("type") == "cant-all-three" for n in _nodes(node)):
            spans += 1
            assert alef != bet, where
            assert "".join(_skels(alef)) == "".join(_skels(bet)), where
        else:
            assert alef == bet == verse["vels"], where
    assert spans, f"{bb}: no cant-all-three span"


@pytest.mark.parametrize(
    "bb, chnu, start, end", sorted(prose_filter._BHS_RANGE_EXCLUSIONS)
)
@pytest.mark.parametrize(
    "reading, key", (("taxton", "vels_cant_alef"), ("elyon", "vels_cant_bet"))
)
def test_decalogue_strands_are_mam_parsed_plus_strands(
    bb, chnu, start, end, reading, key
):
    """Each Decalogue strand MAM-simple loads is MAM-parsed-plus's, mark for mark.

    Over the BHS range ``prose_filter`` excludes, joined without whitespace, which sets aside
    where each source breaks its text into tokens, and with both put in MAM's standard mark
    order by ``give_std_mark_order``.
    """
    refs = {(chnu, vrnu) for vrnu in range(start, end + 1)}
    loaded = load_mam_simple_for_refs(
        paths.mam_simple_dir(), {bb: refs}, include_strands=True
    )
    simple = "".join(
        tok
        for vrnu in range(start, end + 1)
        for tok in loaded[f"{bb}{chnu}:{vrnu}"]["mam_simple_verse"][key]
    )
    plus = "".join(dmt.from_mam_plus(bb, reading).words)
    assert give_std_mark_order(simple) == give_std_mark_order(plus)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-v"]))
