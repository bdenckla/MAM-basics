"""Unit tests for the fix-tester's Unicode substitution (accgram.fix_apply).

Issue wlc-utils#9 retired the M-C splice: ``apply_mam_fix`` now substitutes the MAM Unicode
word into a copy of the ``-kq-u`` verse and re-transcodes it (``uni_to_marks``) to
a Unicode mark body to re-scan.  These tests pin that behavior -- a 1->1 accent swap, an
accent deletion, the missing-sof-pasuq add, the verse-final silluq, ketiv-qere
descent, lone section-marker exclusion, adjacent multi-word foci, and the UNTESTABLE
bailouts -- each re-scanned through the real scanner to confirm it tokenizes as
intended, and each confirming the input verse is not mutated.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_fix_apply.py -v
"""

from __future__ import annotations

from accgram import fix_apply, lexical_validation
from accgram.fix_apply import AppliedFix, UntestableFix, apply_mam_fix
from accgram.prose_scanner import HasLegarmeh, scan_accents


def _types(body: str) -> list[str]:
    return [t.type for t in scan_accents(body, "zz", 1, 1, HasLegarmeh())]


def test_swap_munax_to_merkha():
    # 1c 1:53-style: munax -> merkha on the first word.
    verse = {"vels": ["אל֣וף", "בעם"]}
    result = apply_mam_fix(
        verse,
        ["אל֣וף", "בעם"],
        {"wlc422": "אל֣וף", "mam_simple": "אל֥וף"},
    )
    assert isinstance(result, AppliedFix)
    assert "MERKHA" in _types(result.new_body)
    assert "MUNAX" not in _types(result.new_body)
    assert result.word_index == 0
    # The caller's verse is never mutated (apply works on a deep copy).
    assert verse == {"vels": ["אל֣וף", "בעם"]}


def test_delete_accent():
    # je 10:3-style: drop a merkha (71) entirely.
    result = apply_mam_fix(
        {"vels": ["יד֥י", "זה"]},
        ["יד֥י", "זה"],
        {"wlc422": "יד֥י", "mam_simple": "ידי"},
    )
    assert isinstance(result, AppliedFix)
    assert "MERKHA" not in _types(result.new_body)


def test_unpaired_zarshit_swapped_to_zarqa():
    # The unpaired-82 family (ex 6:6 etc.): a medial zarqa stress-helper (zarshit,
    # U+0598) with no fusion partner is the WLC error; MAM has a proper zarqa
    # (zarnor, U+05AE).  Substituting the whole MAM word clears the unpaired mark and
    # the word now scans as a real ZARQA.
    wlc = "ישרא" + "֘" + "ל"  # medial zarqa stress-helper (zarshit)
    mam = "ישראל" + "֮"  # postpositive zarqa (zarnor)
    result = apply_mam_fix(
        {"vels": [wlc, "׃"]},
        [wlc],
        {"wlc422": wlc, "mam_simple": mam},
    )
    assert isinstance(result, AppliedFix)
    assert "ZARQA" in _types(result.new_body)
    assert not lexical_validation.unpaired_stress_helpers(result.new_body)


def test_missing_sof_pasuq_append():
    # A MAM value that only adds the sof pasuq punctuation: the substituted word
    # carries the sof pasuq, so the re-transcoded body terminates (silluq + sof pasuq
    # both scan).
    result = apply_mam_fix(
        {"vels": ["ויאמר", "אלהיֽם"]},  # final meteg -> verse-final silluq
        ["ויאמר", "אלהיֽם"],
        {"wlc422": "אלהיֽם", "mam_simple": "אלהיֽם׃"},
    )
    assert isinstance(result, AppliedFix)
    assert _types(result.new_body)[-2:] == ["SILLUQ", "SOFPASUQ"]


def test_verse_final_silluq_swap_applies():
    # A speck made BHQ transcribe a verse-final silluq as a tevir (ju 13:18).  MAM
    # restores the silluq (U+05BD).  Substituting the MAM word, the transcoder emits a
    # 75 before the sof pasuq, which the scanner reads as SILLUQ.
    result = apply_mam_fix(
        {"vels": ["פל֛אי׃"]},
        ["פל֛אי׃"],
        {"wlc422": "פל֛אי׃", "mam_simple": "פֽלאי׃"},
    )
    assert isinstance(result, AppliedFix)
    assert _types(result.new_body) == ["SILLUQ", "SOFPASUQ"]


def test_meteg_added_to_word_that_already_has_silluq_stays_inert():
    # When the WLC word *already* bears a (mos) (its verse-final silluq), a further
    # (mos) MAM adds is a genuine medial meteg -- grammar-inert.
    result = apply_mam_fix(
        {"vels": ["הֽזה׃"]},
        ["הֽזה׃"],
        {"wlc422": "הֽזה׃", "mam_simple": "הֽזֽה׃"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "meteg_only"


def test_ketiv_qere_substitutes_the_qere_side():
    # The ketiv is swallowed by the scanner and dropped from vels; the WLC word is the
    # qere, so the substitution descends into the qere side and the ketiv wrapper is
    # preserved.  2 word-units (qere + last) align to 2 WLC words.
    verse = {"vels": [{"kq": [["הנצבים"], ["הנציב֣ים"]]}, "זז׃"]}
    result = apply_mam_fix(
        verse,
        ["הנציב֣ים", "זז׃"],
        {"wlc422": "הנציב֣ים", "mam_simple": "הנציב֥ים"},
    )
    assert isinstance(result, AppliedFix)
    assert "MERKHA" in _types(result.new_body)
    assert "MUNAX" not in _types(result.new_body)
    # The ketiv is still swallowed (emitted as a *<ketiv> atom).
    assert result.new_body.startswith("*")
    assert verse["vels"][0]["kq"][1] == ["הנציב֣ים"]  # source qere untouched


def test_section_marker_excluded_from_alignment():
    # A lone setumah/petuhah/nun-inversum stands as its own vel but is not a word
    # (no Hebrew letter via _token_text), so it must not count during alignment:
    # 1 real word-unit aligns to 1 WLC word despite the trailing section marker.
    result = apply_mam_fix(
        {"vels": ["פל֛אי׃", {"sam_pe_inun": "S"}]},
        ["פל֛אי׃"],  # one WLC word; the S marker is not a word
        {"wlc422": "פל֛אי׃", "mam_simple": "פל֥אי׃"},
    )
    assert isinstance(result, AppliedFix)
    assert "MERKHA" in _types(result.new_body)


def test_adjacent_two_word_substitution():
    # A wlc_focus spanning two adjacent words: munax->merkha on the first and
    # tipexa->munax on the second; both vels are substituted.
    result = apply_mam_fix(
        {"vels": ["א֣", "ב֖"]},
        ["א֣", "ב֖"],
        {"wlc422": "א֣ ב֖", "mam_simple": "א֥ ב֣"},
    )
    assert isinstance(result, AppliedFix)
    assert _types(result.new_body)[:2] == ["MERKHA", "MUNAX"]
    assert result.word_index == 0
    assert len(result.extra_transforms) == 1


def test_adjacent_two_word_one_word_is_noop():
    # Second word differs only by a vowel: a no-op for the grammar, first word still
    # substitutes cleanly and no extra transform is recorded.
    result = apply_mam_fix(
        {"vels": ["אל֣וף", "בעם"]},
        ["אל֣וף", "בעם"],
        {"wlc422": "אל֣וף בעם", "mam_simple": "אל֥וף בעם"},
    )
    assert isinstance(result, AppliedFix)
    assert "MERKHA" in _types(result.new_body)
    assert result.extra_transforms == ()


def test_vowel_only_is_untestable():
    result = apply_mam_fix(
        {"vels": ["בָא"]},
        ["בָא"],
        {"wlc422": "בָא", "mam_simple": "בָּא"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "vowel_only"


def test_meteg_only_is_untestable():
    # The sole difference is a medial meteg (U+05BD) -- grammar-inert and labeled
    # distinctly from a pure-niqqud diff.
    result = apply_mam_fix(
        {"vels": ["יד֥י", "זה"]},
        ["יד֥י", "זה"],
        {"wlc422": "יד֥י", "mam_simple": "ידֽ֥י"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "meteg_only"


def test_accent_move_applies_and_clears_misplaced_telisha():
    # je 44:17: a telisha qetanna (U+05A9) shifts from the kaf to the yod.  The accent
    # multiset is unchanged (one telisha qetanna either way), but the move IS
    # grammar-visible -- lexical_validation flags a non-final telisha qetanna on the WLC
    # value and clears it on the MAM value.  fix_apply now treats the move as a real
    # change: the substitution carries the mark to the yod, and the re-scanned body has
    # no misplaced telisha qetanna.
    wlc_body = fix_apply.uni_to_marks.verse_to_marks({"vels": ["כ֩י"]})
    assert lexical_validation.nonfinal_telisha_qetannas(wlc_body)  # the WLC defect
    result = apply_mam_fix(
        {"vels": ["כ֩י"]},
        ["כ֩י"],
        {"wlc422": "כ֩י", "mam_simple": "כי֩"},
    )
    assert isinstance(result, AppliedFix)
    assert not lexical_validation.nonfinal_telisha_qetannas(result.new_body)
    # The move is recorded for the report (kaf -> yod), not framed as a name diff.
    assert result.moved_accents == ("telisha qetana: kaf -> yod",)
    assert result.removed_accents == ()
    assert result.added_accents == ()
    assert "kaf -> yod" in result.transformation()


def test_multi_word_diff_list_is_untestable():
    result = apply_mam_fix(
        {"vels": ["x"]},
        ["x"],
        {"wlc422": ["a", "b"], "mam_simple": ["c"]},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "multi_word"


def test_multi_word_unequal_counts_is_untestable():
    result = apply_mam_fix(
        {"vels": ["א֣", "ב֖"]},
        ["א֣", "ב֖"],
        {"wlc422": "א֣ ב֖", "mam_simple": "א֥"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "multi_word"


def test_alignment_failure_when_counts_differ():
    # Two verse word-units vs one WLC word -> the alignment guard fires.
    result = apply_mam_fix(
        {"vels": ["א֣", "ב֖"]},
        ["א֣"],
        {"wlc422": "א֣", "mam_simple": "א֥"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "alignment_failure"


def test_ambiguous_word_is_untestable():
    # The focus word occurs twice -> the splice refuses to guess which.
    result = apply_mam_fix(
        {"vels": ["א֣", "א֣"]},
        ["א֣", "א֣"],
        {"wlc422": "א֣", "mam_simple": "א֥"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "ambiguous_word"


def test_synthetic_segolta_fix_applies():
    # is 45:1-style: the speculated fix is the segol *accent* (segolta, U+0592), not
    # the segol vowel -- a real munax -> segolta change the grammar sees.
    result = apply_mam_fix(
        {"vels": ["לכ֣ורש"]},
        ["לכ֣ורש"],
        {"wlc422": "לכ֣ורש", "mam_simple": "לכ֒ורש"},
    )
    assert isinstance(result, AppliedFix)
    assert "SEGOLTA" in _types(result.new_body)


def test_synthetic_vowel_fix_is_inert():
    # A synth_fix that adds only a vowel (segol point, U+05B6) is grammar-inert.
    result = apply_mam_fix(
        {"vels": ["לכ֣ורש"]},
        ["לכ֣ורש"],
        {"wlc422": "לכ֣ורש", "mam_simple": "לכֶ֣ורש"},
    )
    assert isinstance(result, UntestableFix)
    assert result.reason == "vowel_only"
