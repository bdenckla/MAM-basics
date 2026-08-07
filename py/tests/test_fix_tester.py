"""Unit tests for the fix-tester's verse-level ``merge_next`` splice.

Every other fix the tester applies is a single-word accent edit inside one
verse's M-C body (see ``test_fix_apply``).  nu 25:19 is the lone exception: MAM
equals WLC word-for-word and the only difference is versification -- BHS maroons
a verse number mid-chanted-verse.  The fix is to append the M-C body BHS labels
as the *next* verse and re-parse; the marooned atnax then bisects a complete
verse ending in silluq + sof-pasuq.  See doc/fix-tester-remaining-untestables.md.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_fix_tester.py -v
"""

from __future__ import annotations

from accgram import fix_tester
from accgram.prose_ply_grammar import build_parser
from tests.mc_marks import mc_to_marks

# The two real verse bodies (M-C source, converted to the Phase-2 mark alphabet,
# issue wlc-utils#9).  nu 25:19 ends on an atnax (92) plus a ]1 note marker and a P petuhah --
# no silluq, no sof-pasuq (00).
_NU_2519 = mc_to_marks('WA/Y:HI73Y )AX:AR"74Y HA/M.AG."PF92H]1 P')
# nu 26:1 ends in silluq (75) + sof-pasuq (00) -- the verse's true second half.
_NU_2601 = mc_to_marks(
    "WA/Y.O70)MER Y:HWFH03 )EL-MO$E80H "
    'W:/)E94L )EL:(FZF91R B.EN-)AH:ARO71N HA/K.OH"73N L"/)MO75R00'
)


def test_merge_next_extracted_from_note():
    assert fix_tester._merge_next({"merge_next": "nu 26:1"}) == "nu 26:1"
    assert fix_tester._merge_next({"merge_next": "  nu 26:1  "}) == "nu 26:1"
    assert fix_tester._merge_next({}) is None
    assert fix_tester._merge_next({"merge_next": "   "}) is None
    assert fix_tester._merge_next("not a dict") is None


def test_nu_2519_alone_is_ungrammatical():
    # Standalone, the BHS "verse" ends on an atnax with nothing after it, so both
    # the silluq and the sof-pasuq phrases are missing.
    before = fix_tester._evaluate(_NU_2519, "nu", 25, 19, build_parser())
    assert before.status == "ERROR"
    assert before.labels == frozenset({"silluq_phrase", "sof_pasuq_phrase"})
    assert before.token_types[-2:] == ("ATNAX", "MISSING_SOFPASUQ")


def test_merge_next_concatenation_parses_clean():
    # Append nu 26:1: the atnax now bisects a complete verse that ends in
    # silluq + sof-pasuq, and the mid-verse ]1 note / P petuhah are inert.
    parser = build_parser()
    # Evaluate the pre-concatenation verse first (shares the parser); result unused here.
    fix_tester._evaluate(_NU_2519, "nu", 25, 19, parser)
    after = fix_tester._evaluate(f"{_NU_2519} {_NU_2601}", "nu", 25, 19, parser)
    assert after.status == "CLEAN"
    assert not after.labels
    assert "ATNAX" in after.token_types
    assert after.token_types[-2:] == ("SILLUQ", "SOFPASUQ")
    # No spurious token sneaks in where the mid-verse petuhah/note sit.
    assert after.token_types.count("ATNAX") == 1
