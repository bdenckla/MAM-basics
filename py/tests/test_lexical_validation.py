"""Unit tests for the prose lexical-validation layer (unpaired stress-helpers).

Pin the pure-function semantics of `unpaired_stress_helpers`: a prose tsinnorit
(M-C ``82``) is an alphabet error unless it is fused with a later tsinnor (M-C ``02``)
in the *same* maqaf/space-delimited atom.  These guard the fuse-vs-unpaired and
atom-boundary logic so a regression fails here rather than silently shifting the
ungrammatical corpus.  Bodies are written over the Unicode mark alphabet (issue wlc-utils#9, Phase
2); arbitrary capital letters stand in for consonant filler.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_lexical_validation.py -v
"""

from __future__ import annotations

from accgram import accent_marks as am
from accgram.lexical_validation import (
    illegal_same_letter_pairs,
    nonfinal_telisha_qetannas,
    unpaired_stress_helpers,
)

_TS = am.TSINNORIT  # M-C 82 (zarqa stress-helper)
_ZI = am.TSINNOR  # M-C 02 (tsinnor / zarqa main)
_MA = am.MAHAPAKH  # U+05A4 (below)
_TI = am.TIPEXA  # U+0596 (below)
_QA = am.QADMA  # U+05A8 (above; "azla")
_TG = am.TELISHA_GEDOLA  # U+05A0 (prepositive disjunctive)
_G2 = am.GERSHAYIM  # U+059E (gn5:29, zp2:15 companion)
_GE = am.GERESH  # U+059C
_GM = am.GERESH_MUQDAM  # U+059D (2k17:13 companion, pre-scanner-normalization)
_TQ = am.TELISHA_QETANA  # U+05A9 (M-C 04 main / 24 medial helper)
_LT = am.LETTER  # "X" consonant filler


def _codes(body: str) -> list[str]:
    return [m.code for m in unpaired_stress_helpers(body)]


def _pairs(body: str) -> list[str]:
    return [m.code for m in illegal_same_letter_pairs(body)]


def _telq(body: str) -> list[str]:
    return [m.code for m in nonfinal_telisha_qetannas(body)]


def test_bare_82_is_unpaired():
    # gn 47:29-style: a tsinnorit with no later tsinnor anywhere -> unpaired.
    assert _codes("YISRA" + _TS + "L]s") == ["82"]


def test_82_fused_with_later_02_same_atom_is_clean():
    # A real zarqa stress-helper: tsinnorit{TEXT}tsinnor on one atom fuses into one ZARQA.
    assert _codes("X" + _TS + "Y" + _ZI + "Z") == []


def test_82_two_letters_back_still_unpaired():
    # gn 17:20: the tsinnorit sits two letters before the lamed; still no tsinnor -> unpaired.
    assert _codes("W" + am.METEG + "LYISMA" + _TS + ")L]S]s") == ["82"]


def test_02_in_a_different_atom_does_not_rescue_82():
    # Maqaf/space ends the atom, so a tsinnor across the boundary cannot fuse.
    assert _codes("A" + _TS + "B-C" + _ZI + "D") == ["82"]
    assert _codes("A" + _TS + "B C" + _ZI + "D") == ["82"]


def test_02_before_82_does_not_fuse():
    # Fusion requires the tsinnor to follow the tsinnorit; an earlier tsinnor leaves it unpaired.
    assert _codes("A" + _ZI + "B" + _TS + "C") == ["82"]


def test_no_82_anywhere_is_clean():
    assert (
        _codes(
            "WAYO"
            + am.MERKHA
            + "MER"
            + am.PASHTA
            + " )ELOHI"
            + am.ATNAX
            + "YM"
            + am.SOF_PASUQ
        )
        == []
    )


def test_atom_with_both_returns_the_atom_text():
    body = "YISRA" + _TS + "L]s"
    [mark] = unpaired_stress_helpers(body)
    assert mark.code == "82"
    assert mark.atom == body


# --- non-whitelisted same-letter accent pair (general guard, Plan E) -----------


def test_mahapakh_tipexa_same_letter_is_illegal():
    # lv25:20 (word na'akhal): mahapakh + tipexa adjacent (one letter) -> illegal pair,
    # still flagged, now via the general rule.  Body order is mahapakh-then-tipexa.
    assert _pairs("XX-XXX" + _MA + _TI + "X]c]n") == ["mahapakh!tipexa"]


def test_pair_label_follows_body_order():
    # The bang label is order-preserving (body order), so the reversed stacking reads
    # tipexa!mahapakh -- still flagged, just labeled in the order it appears.
    assert _pairs("X" + _TI + _MA + "X") == ["tipexa!mahapakh"]


def test_whitelisted_mahapakh_qadma_is_not_flagged():
    # ek20:31 (word nitm'im): mahapakh + qadma is the sole whitelisted pair (MAM keeps
    # both; the scanner fuses it to mahapakh!qadma).  Not an alphabet error.
    assert _pairs("XXXX" + _MA + _QA + "XX") == []
    assert _pairs("XXXX" + _QA + _MA + "XX") == []  # whitelist is order-less


def test_whitelisted_telg_geresh_family_is_not_flagged():
    # The telisha gedola + geresh-family same-letter pairs (gn5:29 / zp2:15 gershayim,
    # 2k17:13 geresh muqdam, and plain geresh) are masoretically-blessed and kept as a
    # telg-then-geresh sequence -- not an alphabet error.  Order-less, like every entry.
    for companion in (_G2, _GE, _GM):
        assert _pairs("XX" + _TG + companion + "X") == []
        assert _pairs("XX" + companion + _TG + "X") == []


def test_geresh_muqdam_whitelisted_separately_from_plain_geresh():
    # The guard runs pre-scanner on raw codepoints, so 2k17:13's geresh muqdam (U+059D) is
    # whitelisted as its own codepoint, before the scanner normalizes it to a plain geresh.
    assert _pairs("X" + _TG + _GM + "X") == []


def test_telg_with_non_geresh_neighbor_still_flagged():
    # The whitelist is specific to the geresh family: a telisha gedola stacked on some other
    # accent (e.g. tipexa) is still an alphabet error.
    assert _pairs("X" + _TG + _TI + "X") == ["telishagedola!tipexa"]


def test_a_third_hypothetical_same_letter_pair_is_flagged():
    # The guard is general, not pair-specific: any non-whitelisted stack flags, e.g.
    # merkha + tipexa, with the reused prose leaf names.
    assert _pairs("X" + am.MERKHA + _TI + "X") == ["merkha!tipexa"]


def test_accents_on_different_letters_are_clean():
    # An X (base letter) between them => different letters => a legal sequence, not a pair.
    assert _pairs("X" + _MA + "X" + _TI + "X") == []


def test_pair_across_atom_boundary_is_clean():
    assert _pairs("X" + _MA + "-X" + _TI + "X") == []
    assert _pairs("X" + _MA + " X" + _TI + "X") == []


def test_non_accent_between_marks_does_not_pair():
    # A non-accent (meteg U+05BD) between two accents means they are not stacked.
    assert _pairs("X" + _MA + am.METEG + _TI + "X") == []


def test_no_pair_is_clean():
    assert _pairs("XX" + _MA + "X XXX" + _TI + "X" + am.SOF_PASUQ) == []
    assert (
        _pairs("YISRA" + _TS + "L]s") == []
    )  # an unpaired 82 is not a same-letter pair


# --- misplaced (non-final) telisha qetanna, M-C lone 24 (je 44:17) -------------


def test_nonfinal_telisha_qetanna_is_flagged():
    # je 44:17 (כִּי): a telisha qetanna on the kaf (a base letter still follows) with no
    # second telisha qetanna to absorb it as a stress-helper -> misplaced postpositive.
    assert _telq(_LT + _TQ + _LT) == ["medial telisha qetanna"]


def test_word_final_telisha_qetanna_is_clean():
    # The normal, postpositive 04: on the word's final letter, no base letter follows.
    assert _telq(_LT + _LT + _TQ) == []


def test_fused_24_04_pair_is_clean():
    # A well-formed 24...04 stress-helper pair: the medial telq is followed by a second
    # (postpositive) telq, which the scanner fuses -> not unpaired.
    assert _telq(_LT + _TQ + _LT + _LT + _TQ) == []


def test_nonfinal_telq_rescued_only_within_its_atom():
    # A second telisha qetanna across a maqaf/space boundary cannot rescue the medial one.
    assert _telq(_LT + _TQ + _LT + "-" + _LT + _TQ) == ["medial telisha qetanna"]
    assert _telq(_LT + _TQ + _LT + " " + _LT + _TQ) == ["medial telisha qetanna"]


def test_nonfinal_telq_followed_only_by_non_letters_is_clean():
    # "Non-final" means a base letter follows; a telq trailed only by punctuation
    # (sof pasuq) is still word-final and legitimate.
    assert _telq(_LT + _LT + _TQ + am.SOF_PASUQ) == []
