"""Exports main."""

import sys

import uxlc_misc.my_uxlc as my_uxlc
import mb_cmn.file_io as my_open
import uxlc_fois.fois_html as fois_html
import uxlc_fois.fois_kq_foi as fois_kq_foi
import uxlc_fois.fois_mark_grammar_2_foi as fois_mark_grammar_2_foi
import uxlc_fois.fois_mark_grammar_foi as fois_mark_grammar_foi
import uxlc_fois.uni_heb_char_classes as ucc
import uxlc_paths


def _stripped_text(value):
    return value.strip() if value else ""


def _append_text(atom, value):
    text = _stripped_text(value)
    if not text:
        return
    atom[1] += text
    atom[2]["schematic"] += "".join(ch for ch in text if ch in ucc.LETTERS)


def _append_inner_text(accum, xml_element, handlers):
    _append_text(accum[-1], xml_element.text)
    for child in xml_element:
        my_uxlc.dispatch_on_tag(accum, child, handlers)
        _append_text(accum[-1], child.tail)


def _handle_vc_wqk(wqk, accum, verse_child):
    accum.append([wqk, "", {"schematic": "", "types": []}])
    _append_inner_text(accum, verse_child, _WORD_CHILD_HANDLERS)


def _handle_vc_w(accum, verse_child):
    _handle_vc_wqk("w", accum, verse_child)


def _handle_vc_q(accum, verse_child):
    _handle_vc_wqk("q", accum, verse_child)


def _handle_vc_k(accum, verse_child):
    _handle_vc_wqk("k", accum, verse_child)


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    _append_inner_text(accum, word_child_s, _WORD_CHILD_HANDLERS)


def _handle_wc_x(accum, word_child_x):
    note_type = _stripped_text(word_child_x.text)
    if not note_type:
        return
    accum[-1][2]["schematic"] += "."
    accum[-1][2]["types"].append(note_type)


_WORD_CHILD_HANDLERS = {
    "x": _handle_wc_x,
    "s": _handle_wc_s,
}
_VERSE_CHILD_HANDLERS = {
    "w": _handle_vc_w,
    "q": _handle_vc_q,
    "k": _handle_vc_k,
    "x": my_uxlc.handle_xc_ignore,
    "pe": my_uxlc.handle_xc_ignore,
    "samekh": my_uxlc.handle_xc_ignore,
    "reversednun": my_uxlc.handle_xc_ignore,
}


def main():
    """Writes UXLC features of interest to per-FOI JSON files."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    uxlc = my_uxlc.read_all_books(_VERSE_CHILD_HANDLERS)
    fois = {
        "kq": fois_kq_foi.init(),
        "mark-grammar": fois_mark_grammar_foi.init(),
        "mark-grammar-2": fois_mark_grammar_2_foi.init(),
    }
    for bkid, chapters in uxlc.items():
        for chidx, chapter in enumerate(chapters):
            for vridx, verse in enumerate(chapter):
                bcv = bkid, chidx + 1, vridx + 1
                fois_kq_foi.collect_for_verse(fois["kq"], bcv, verse)
                fois_mark_grammar_foi.collect_for_verse(
                    fois["mark-grammar"], bcv, verse
                )
                fois_mark_grammar_2_foi.collect_for_verse(
                    fois["mark-grammar-2"], bcv, verse
                )
    fois_mark_grammar_2_foi.finalize(fois["mark-grammar-2"])
    json_output_paths = {
        foi_key: uxlc_paths.fois_pages_dir() / f"features_of_interest-{foi_key}.json"
        for foi_key in fois
    }
    for foi_key, catalog in fois.items():
        my_open.json_dump_to_file_path(catalog, json_output_paths[foi_key])
    fois_html.write(fois, json_output_paths)


if __name__ == "__main__":
    main()
