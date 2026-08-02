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

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_mam_simple_dualcant_loader.py -v
"""

from __future__ import annotations

import pytest

from accgram import accent_marks as am
from accgram.mam_simple_verse import load_mam_simple_for_refs
import wlc_paths


def _verse(bb: str, chnu: int, vrnu: int) -> dict[str, object]:
    refs = {bb: {(chnu, vrnu)}}
    loaded = load_mam_simple_for_refs(
        wlc_paths.mam_simple_dir(), refs, include_strands=True
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


def test_strands_exposed_separately_and_differ_on_dual_word():
    verse = _verse("gn", 35, 22)
    assert set(verse) == {"vels", "vels_cant_alef", "vels_cant_bet"}

    alef = verse["vels_cant_alef"]
    bet = verse["vels_cant_bet"]

    # No longer the pre-wlc-utils#36 triple-concatenation: each strand is one word sequence
    # (single-cant prefix + its span words + single-cant suffix), 19 tokens for Gen 35:22.
    assert all(isinstance(tok, str) for tok in alef)
    assert all(isinstance(tok, str) for tok in bet)
    assert _skels(alef) == _skels(bet)  # same letters
    assert len(alef) == 19

    # The strands disagree on the dual span: ראובן carries zaqef qatan (U+0594) in the
    # alef/pashut strand but revia (U+0597) in the bet/midrashit strand.
    alef_reuven = next(
        tok for tok in alef if "ראוב" in "".join(c for c in tok if "א" <= c <= "ת")
    )
    bet_reuven = next(
        tok for tok in bet if "ראוב" in "".join(c for c in tok if "א" <= c <= "ת")
    )
    assert am.ZAQEF_QATAN in alef_reuven and am.REVIA not in alef_reuven
    assert am.REVIA in bet_reuven and am.ZAQEF_QATAN not in bet_reuven


def test_per_strand_sof_pasuq_placement_drives_segmentation():
    verse = _verse("gn", 35, 22)
    alef = [tok for tok in verse["vels_cant_alef"] if isinstance(tok, str)]
    bet = [tok for tok in verse["vels_cant_bet"] if isinstance(tok, str)]

    # alef closes a chanted verse mid–numbered-verse (on ישראל) -> two tokens carry sof pasuq.
    alef_sofs = [i for i, tok in enumerate(alef) if am.SOF_PASUQ in tok]
    assert len(alef_sofs) == 2
    assert "ישרא" in "".join(c for c in alef[alef_sofs[0]] if "א" <= c <= "ת")

    # bet runs the whole numbered verse as one chanted verse: only the final token carries
    # sof pasuq, and its ישראל (mid-verse) carries atnaX, not sof pasuq.
    bet_sofs = [i for i, tok in enumerate(bet) if am.SOF_PASUQ in tok]
    assert bet_sofs == [len(bet) - 1]
    bet_israel = bet[alef_sofs[0]]
    assert am.ATNAX in bet_israel and am.SOF_PASUQ not in bet_israel


def test_single_cantillation_verse_in_range_yields_shared_strands():
    # Exod 20:7 is single-cantillation (a flat-text verse) even though it sits inside
    # the Decalogue range: both strands must be identical (no split to invent).
    verse = _verse("ex", 20, 7)
    assert verse["vels_cant_alef"] == verse["vels_cant_bet"] == verse["vels"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-v"]))
