"""Unit tests for the "almost errors" page generator (Plan B).

The pure-logic tests (mode-aware ``word_to_marks`` variant, clean-tree table
rendering) run anywhere; the end-to-end generation tests need the WLC 4.22 kq-u
corpus, which is committed in this repo under ``out/wlc422-kq-u`` -- not, as this said
before, a sibling repo.  Being tracked here is why its absence FAILS rather than skipping:
it can only be missing if someone deleted tracked files, and going quiet about that is going
quiet at the worst moment.  See ``wlc_paths.require_sibling`` for the argument.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_almost_errors.py -v
"""

from __future__ import annotations


from accgram import accent_marks as am
from accgram import almost_errors_html as aeh
from accgram import almost_errors_html_shared as aes
from accgram import almost_errors_oddities as aeo
from accgram import almost_errors_trees as aet
from accgram import ob_error_context
from accgram import ob_tree_parse
from accgram import rtms_data
from accgram.prose_ply_grammar import build_parser
from accgram.prose_scanner import HasLegarmeh
from py_html import wlc_utils_html as H

import wlc_paths

# A synthetic same-letter word: one base letter carrying BOTH a telisha gedola and a
# plain geresh -- the shape the companion-drop charity concerns.
_SAME_LETTER_BOTH = "א" + am.TELISHA_GEDOLA + am.GERESH


def test_build_word_variant_keep_telg_drops_geresh_keeps_telg() -> None:
    result = aet._build_word_variant(_SAME_LETTER_BOTH, "keep_telg")
    assert am.TELISHA_GEDOLA in result
    assert am.GERESH not in result


def test_build_word_variant_keep_gerstar_drops_telg_keeps_geresh() -> None:
    result = aet._build_word_variant(_SAME_LETTER_BOTH, "keep_gerstar")
    assert am.GERESH in result
    assert am.TELISHA_GEDOLA not in result


def test_build_word_variant_keep_both_keeps_both() -> None:
    result = aet._build_word_variant(_SAME_LETTER_BOTH, "keep_both")
    assert am.TELISHA_GEDOLA in result
    assert am.GERESH in result


def test_build_word_variant_only_touches_both_carrying_words() -> None:
    # A word with a telg but no geresh-family companion is transcoded untouched in
    # every mode (the variant only edits words holding BOTH marks).
    telg_only = "א" + am.TELISHA_GEDOLA
    for mode in ("keep_telg", "keep_gerstar", "keep_both"):
        assert am.TELISHA_GEDOLA in aet._build_word_variant(telg_only, mode)


def test_telg_word_forms_same_letter_splits_marks() -> None:
    forms = aet._telg_word_forms(_SAME_LETTER_BOTH)
    assert forms.word == _SAME_LETTER_BOTH  # no geresh muqdam to charitably rewrite
    assert am.TELISHA_GEDOLA in forms.keep_telg and am.GERESH not in forms.keep_telg
    assert (
        am.GERESH in forms.keep_gerstar and am.TELISHA_GEDOLA not in forms.keep_gerstar
    )
    assert forms.same_letter is True


def test_telg_word_forms_cross_letter_is_not_same_letter() -> None:
    cross = "א" + am.TELISHA_GEDOLA + "ב" + am.GERESH
    assert aet._telg_word_forms(cross).same_letter is False


def test_telg_word_forms_shows_geresh_muqdam_post_charity() -> None:
    # 2k17:13's shape: a geresh muqdam companion, which the table shows as a plain geresh.
    muqdam = "א" + am.TELISHA_GEDOLA + am.GERESH_MUQDAM
    forms = aet._telg_word_forms(muqdam)
    for form in (forms.word, forms.keep_gerstar):
        assert am.GERESH in form and am.GERESH_MUQDAM not in form
    assert forms.same_letter is True


def test_parse_tree_from_text_renders_clean_tree() -> None:
    # A clean (error-free) print_tree, the shape the telg exhibit emits, must still
    # parse into a renderable table -- unlike parse_error_tree_from_text, which yields
    # None when there is no ERROR leaf.
    clean = "0 silluq_clause\n  1 tipexa_phrase\n    tipexa \n  1 silluq_phrase\n    silluq \n"
    tree = ob_error_context.parse_tree_from_text(clean)
    assert tree is not None
    assert not tree.has_error_leaf
    assert ob_tree_parse.iter_leaf_texts(tree) == ["tipexa", "silluq"]
    assert ob_error_context.parse_error_tree_from_text(clean) is None
    # The shared table renderer accepts the error-free tree.
    assert H.is_htel(aes.render_tree(clean))


def test_parse_tree_from_text_empty_is_none() -> None:
    assert ob_error_context.parse_tree_from_text("") is None


# --------------------------------------------------------------------------- #
# Corpus-backed end-to-end generation.
# --------------------------------------------------------------------------- #
_REPO_ROOT = wlc_paths.wlc_data_root()


def _load_index():
    # No presence guard: ``load_wlc422_index`` already raises FileNotFoundError naming the
    # directory it looked in, which is the whole of what a guard here could have said.
    return rtms_data.load_wlc422_index(rtms_data.default_wlc422_kq_u_dir(_REPO_ROOT))


def test_all_five_telg_verses_parse_clean_in_all_three_readings() -> None:
    index = _load_index()
    parser, has_legarmeh = build_parser(), HasLegarmeh()
    for bcv in aeo._TELG_EXHIBIT_REFS:
        for mode, _label in aeo._TELG_MODES:
            verdict = aet._telg_verdict_for(bcv, mode, index, parser, has_legarmeh)
            assert verdict == "clean", f"{bcv} [{mode}] -> {verdict}"


def test_exactly_three_telg_exhibit_words_are_same_letter() -> None:
    # gn5:29, zp2:15 (telg + gershayim) and 2k17:13 (telg + geresh muqdam) stack both marks
    # on one base letter; lv10:4 and ek48:10 spread them across two letters of one word.
    index = _load_index()
    same_letter = sum(
        aet._telg_marks_share_letter(aet._telg_gerstar_word(index[bcv]))
        for bcv in aeo._TELG_EXHIBIT_REFS
    )
    assert same_letter == 3


def test_ek2031_tree_fuses_mahapakh_qadma() -> None:
    index = _load_index()
    parser, has_legarmeh = build_parser(), HasLegarmeh()
    text = aet._prose_verse_tree_text("ek20:31", index, parser, has_legarmeh)
    assert "mahapakh!qadma" in text
    assert "ERROR" not in text


def test_ek2031_verdict_table_only_fused_and_qadma_mah_parse() -> None:
    # The five readings of ek20:31's mahapakh + qadma pair: only the fused token and the
    # qadma-then-mahapakh sequence parse (the grammar's pashta_phrase has rules for
    # MAHAPAKHQADMA and the cross-letter QADMA MAHAPAKH pair, but not for a bare mahapakh, a
    # bare qadma, or a mahapakh-then-qadma order).
    index = _load_index()
    parser, has_legarmeh = build_parser(), HasLegarmeh()
    verdicts = {
        mode: aet._ek_verdict_for(mode, index, parser, has_legarmeh)
        for mode, _label in aeo._EK_MODES
    }
    assert verdicts["fused"] == "clean", verdicts
    assert verdicts["seq_qadma_mah"] == "clean", verdicts
    for mode in ("drop_qadma", "drop_mahapakh", "seq_mah_qadma"):
        assert verdicts[mode] != "clean", verdicts


def test_lv2520_tree_is_illegal_mark() -> None:
    index = _load_index()
    parser, has_legarmeh = build_parser(), HasLegarmeh()
    text = aet._prose_verse_tree_text("lv25:20", index, parser, has_legarmeh)
    assert "illegal_mark" in text
    assert "mahapakh!tipexa" in text


def test_render_body_contents_smoke() -> None:
    index = _load_index()
    parser, has_legarmeh = build_parser(), HasLegarmeh()
    body = aeh.render_body_contents(index, parser, has_legarmeh)
    rendered = H.el_to_str_no_wbr(body[0])
    # The two framing kinds, the MAM-confirmed non-charity, the lv25:20 contrast
    # (delegated to goerwitz.html, not re-detailed), and the exhibit trees: the two telg
    # keep-both trees (zp2:15 + lv10:4, the checker's actual output) plus ek20:31 (1).
    assert "Editorial charities" in rendered
    assert "Masoretically-blessed oddities" in rendered
    assert "mahapakh!qadma" in rendered
    assert "goerwitz.html#oblv25v20" in rendered
    # The Psalms 17:14 double-tsinnor exhibit summarizes and links out to its deep dive;
    # it carries no parse tree (the grammar can't parse the doubled mark directly), so the
    # error-table count stays at 3 (two telg keep-both trees + ek20:31).
    assert "ps17v14-double-tsinnor.html" in rendered
    assert rendered.count("goerwitz-obs-error-table") == 3
