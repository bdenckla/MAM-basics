"""Genre filter for the prose accent grammar.

The prose grammar cannot parse the 3-poetic-accent system, so verses using
poetic cantillation must be excluded before they reach the parser: Psalms and
Proverbs wholesale, poetically-cantillated Job verses, and a few verses the BHS
versification hard-codes (the Decalogue ranges and Gn 35:22). This is the genre
filter, extracted from the former filter_split_wlc with the (now removed)
hardcoded-troublemaker check dropped.
"""

from __future__ import annotations

from mb_cmn import bib_locales as tbn
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

_BHS_SINGLE_VERSE_EXCLUSIONS: frozenset[tuple[str, int, int]] = frozenset(
    {
        ("gn", 35, 22),
    }
)


# Intentionally hard-coded in BHS coordinates (book/chapter/verse) to keep
# filtering behavior stable without a runtime dependency on MAM-simple locale
# data. Decalogue ranges were verified from:
#   MAM-simple/json-vtrad-bhs/Exod.json  -> 20:2-17
#   MAM-simple/json-vtrad-bhs/Deut.json  -> 5:6-21
_BHS_RANGE_EXCLUSIONS: frozenset[tuple[str, int, int, int]] = frozenset(
    {
        ("ex", 20, 2, 17),
        ("dt", 5, 6, 21),
    }
)


# Within the Decalogue ranges, these verses are single-cantillation in WLC *and* MAM
# (their only doubled marks are pashta stress-helpers, not dual cantillation), so they
# are ordinary prose: they route through the normal checker rather than the
# dual-cantillation detangler (issue wlc-utils#36; established by a one-off corpus survey run in
# gitignored scratch, now gone, and cross-checked against MAM in
# ``tests/test_dual_cant_detangle.py``, which is where the finding actually lives).
# Everything else in the ranges is dual and
# stays excluded for the detangler.
_BHS_SINGLE_CANT_IN_RANGE: frozenset[tuple[str, int, int]] = frozenset(
    {
        ("ex", 20, 7),
        ("ex", 20, 11),
        ("ex", 20, 12),
        ("ex", 20, 16),
        ("ex", 20, 17),
        ("dt", 5, 11),
        ("dt", 5, 16),
        ("dt", 5, 20),
        ("dt", 5, 21),
    }
)


def _is_excluded_bhs_ref(bb: str, chnu: int, vrnu: int) -> bool:
    if (bb, chnu, vrnu) in _BHS_SINGLE_VERSE_EXCLUSIONS:
        return True
    if (bb, chnu, vrnu) in _BHS_SINGLE_CANT_IN_RANGE:
        return False  # ordinary single-cant verse; let the normal prose path keep it
    for ex_bb, ex_chnu, ex_start, ex_end in _BHS_RANGE_EXCLUSIONS:
        if bb == ex_bb and chnu == ex_chnu and ex_start <= vrnu <= ex_end:
            return True
    return False


def _wlc_bhs_to_mam_bcvt(bk39id: str, chnu: int, vrnu: int):
    """Map a WLC verse ref to a MAM-tagged locale.

    The historical py_misc-based BHS->MAM remapping layer is no longer
    available in this repository, so we currently preserve chapter/verse and
    only retag the versification marker to MAM.
    """
    return tbn.mk_bcvtmam(bk39id, chnu, vrnu)


def should_keep_line(bb: str, chnu: int, vrnu: int) -> bool:
    # Exclude Psalms and Proverbs wholesale.
    if bb in ("ps", "pr"):
        return False

    # Exclude BHS-coordinate locales intentionally hard-coded in this repo.
    if _is_excluded_bhs_ref(bb, chnu, vrnu):
        return False

    bk39id = wlc_bb_to_bk39id(bb)
    bcvtmam = _wlc_bhs_to_mam_bcvt(bk39id, chnu, vrnu)

    # Exclude Job verses that use poetic cantillation.
    if bk39id == tbn.BK_JOB and tbn.is_poetcant(bcvtmam):
        return False

    return True
