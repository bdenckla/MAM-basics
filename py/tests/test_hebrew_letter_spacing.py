"""Compare expanded NAEE HTML with the ordinary conversion of its rendered corpus."""

from mb_cmn import bib_locales as tbn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import shrink
from mb_misc import mb_html
from near_aleppo import build_paths, edition
from py_html import hebrew_letter_spacing as spacing
from py_misc import mam_doc_utils
from py_misc import ren_html_for_renel as hfr
from render_wt import render_wikitext as rwt


def _canonical(node, wrappers):
    """Remove only spacing spans and coalesce text, retaining all other HTML."""
    if isinstance(node, str):
        return node
    if isinstance(node, (list, tuple)):
        children = [_canonical(child, wrappers) for child in node]
        return shrink.shrink(mb_html.flatten(children))
    if node.get("attr", {}).get("class") == spacing.CLASS:
        assert mb_html.htel_get_tag(node) == "span"
        assert node["attr"] == {"class": spacing.CLASS}
        wrappers.append(node)
        return _canonical(node["contents"], wrappers)
    return {
        **node,
        **(
            {"contents": _canonical(node["contents"], wrappers)}
            if "contents" in node
            else {}
        ),
    }


def test_spacing_preserves_the_complete_rendered_corpus():
    mode = edition.NEAR_ALEPPO_MODE
    plain = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    expanded = hfr.HfrCtx(mode.ht_tac_for_ren_tag, text_to_html=mode.text_to_html)
    books = plus.read_parsed_plus_bk39s(
        tbn.ALL_BK39_IDS, str(build_paths.dataset_dir().parent)
    )
    wrappers = []
    checked = 0

    def compare(sequence):
        nonlocal checked
        expected = hfr.html_for_ren_el(plain, sequence)
        actual = hfr.html_for_ren_el(expanded, sequence)
        assert _canonical(actual, wrappers) == _canonical(expected, [])
        checked += 1

    for bkid in tbn.ALL_BK39_IDS:
        for verse in rwt.render(bkid, books, mode.renopts, {}).values():
            verse.map_over(
                lambda sequence: compare(mam_doc_utils.mark_doc_targets(sequence))
            )
            notes = verse.map_over(mam_doc_utils.extract_docs)
            for sequence in (notes.verse, notes.vaf_next_cp, notes.good_ending):
                for note in sequence:
                    compare(note["doc_lemma"])
                    compare(note["doc_parts"])
    assert checked, "The rendered corpus was empty"
    assert wrappers, "The corpus exercised no expanded text"
