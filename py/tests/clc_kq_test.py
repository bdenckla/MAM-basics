"""Test for clc_kq (CLC ketiv/qere ruby builder).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/clc_kq_test.py

Synthetic atom lists exercise the unit-grouping rule and the ruby HTML shape
(standard pair, both "without" cases, the note always-link). Real UXLC verses
pin the grouping against the data: Gen 30:11 (k1q2 — one ketiv read as two
words), 2 Sam 21:12 (a standard pair adjacent to a grouped k2q2 unit), and the
two "without" cases in 2 Samuel. XML is read directly (paths from uxlc_paths) so
the test is independent of cwd and of the my_uxlc reader, like clc_dual_cant_test.
"""

import xml.etree.ElementTree as ET

import clc.clc_kq as kq
import uxlc_misc.uxlc_utils_html as H
import uxlc_paths

_GEN_XML = uxlc_paths.uxlc_39_dir() / "Genesis.xml"
_SAM2_XML = uxlc_paths.uxlc_39_dir() / "Samuel_2.xml"


def _a(kind, text):
    return {"kind": kind, "text": text, "types": []}


def _atom_text(el):
    """Mirror clc_read: own text + non-<x> children (descend <s>) + tails."""
    parts = [el.text or ""]
    for child in el:
        if child.tag != "x":  # an <x> note code is not part of the word
            parts.append(_atom_text(child))
        parts.append(child.tail or "")
    return "".join(parts).strip()


def _read_verse_atoms(xml_path, chap, verse):
    """The verse's w/k/q atoms in clc_read shape, parsed straight from the XML."""
    root = ET.parse(xml_path).getroot()
    for c in root.iter("c"):
        if c.get("n") != str(chap):
            continue
        for v in c.iter("v"):
            if v.get("n") != str(verse):
                continue
            return [
                {"kind": el.tag, "text": _atom_text(el), "types": []}
                for el in v
                if el.tag in ("w", "k", "q")
            ]
    raise AssertionError(f"{xml_path} {chap}:{verse} not found")


def test_grouping_synthetic():
    # Standard pair: w, (k q), w -> Word, KqUnit(1,1), Word.
    units = list(
        kq.iter_render_units([_a("w", "α"), _a("k", "K"), _a("q", "Q"), _a("w", "β")])
    )
    assert [type(u).__name__ for u in units] == ["Word", "KqUnit", "Word"]
    assert units[0] == kq.Word(1, "α") and units[2] == kq.Word(4, "β")
    assert units[1].ketivs == (kq.Word(2, "K"),) and units[1].qeres == (
        kq.Word(3, "Q"),
    )

    # qere-without-ketiv: lone q -> KqUnit with empty ketivs.
    units = list(kq.iter_render_units([_a("w", "α"), _a("q", "Q")]))
    assert isinstance(units[1], kq.KqUnit)
    assert units[1].ketivs == () and units[1].qeres == (kq.Word(2, "Q"),)

    # ketiv-without-qere: lone k -> KqUnit with empty qeres.
    units = list(kq.iter_render_units([_a("k", "K"), _a("w", "β")]))
    assert units[0].ketivs == (kq.Word(1, "K"),) and units[0].qeres == ()

    # Interleaved k,q,k,q -> TWO (1,1) units (the "kqkq" case).
    units = list(
        kq.iter_render_units(
            [_a("k", "K1"), _a("q", "Q1"), _a("k", "K2"), _a("q", "Q2")]
        )
    )
    assert [type(u).__name__ for u in units] == ["KqUnit", "KqUnit"]
    assert units[0].ketivs == (kq.Word(1, "K1"),) and units[0].qeres == (
        kq.Word(2, "Q1"),
    )
    assert units[1].ketivs == (kq.Word(3, "K2"),) and units[1].qeres == (
        kq.Word(4, "Q2"),
    )

    # Grouped k,k,q,q -> ONE (2,2) unit (the "kkqq" case).
    units = list(
        kq.iter_render_units(
            [_a("k", "K1"), _a("k", "K2"), _a("q", "Q1"), _a("q", "Q2")]
        )
    )
    assert len(units) == 1 and isinstance(units[0], kq.KqUnit)
    assert units[0].ketivs == (kq.Word(1, "K1"), kq.Word(2, "K2"))
    assert units[0].qeres == (kq.Word(3, "Q1"), kq.Word(4, "Q2"))


def test_ruby_standard():
    html = H.el_to_str_no_wbr(
        kq.kq_ruby(kq.KqUnit((kq.Word(2, "KKK"),), (kq.Word(3, "QQQ"),)), {}, 1, 1)
    )
    assert '<ruby class="clc-kq">' in html
    assert '<span class="clc-kq-q">QQQ</span>' in html
    assert '<span class="clc-kq-k">KKK</span>' in html
    # qere on the baseline (before <rt>), ketiv inside the annotation.
    assert html.index("clc-kq-q") < html.index("<rt") < html.index("clc-kq-k")
    assert "clc-kq-none" not in html


def test_ruby_qere_without_ketiv():
    # Read but not written: qere on base, "[אין כתיב]" in the annotation.
    html = H.el_to_str_no_wbr(kq.kq_ruby(kq.KqUnit((), (kq.Word(2, "QQQ"),)), {}, 1, 1))
    assert '<span class="clc-kq-q">QQQ</span>' in html
    assert "[אין כתיב]" in html and "[אין קרי]" not in html
    assert "clc-kq-none" in html
    assert html.index("<rt") < html.index(
        "clc-kq-none"
    )  # placeholder is the annotation


def test_ruby_ketiv_without_qere():
    # Written but not read: "[אין קרי]" on the baseline, ketiv full-size above.
    html = H.el_to_str_no_wbr(kq.kq_ruby(kq.KqUnit((kq.Word(2, "KKK"),), ()), {}, 1, 1))
    assert '<span class="clc-kq-k">KKK</span>' in html
    assert "[אין קרי]" in html and "[אין כתיב]" not in html
    assert html.index("clc-kq-none") < html.index(
        "<rt"
    )  # placeholder is on the baseline


def test_note_highlight():
    notes_by_atom = {(4, 7, 3): ["a note"]}  # only membership matters
    html = H.el_to_str_no_wbr(
        kq.kq_ruby(
            kq.KqUnit((kq.Word(2, "KKK"),), (kq.Word(3, "QQQ"),)), notes_by_atom, 4, 7
        )
    )
    # Noted → highlighted (clc-doc-target), but NOT a same-page link: the note sits in
    # the same row's doc cell beside it (clc_render dropped same-page note anchors).
    assert 'class="clc-doc-target"' in html and "href" not in html
    assert (
        "QQQ" in html
    )  # the noted qere is still rendered, now wrapped in the highlight span


def test_join_text():
    assert (
        kq.join_text(kq.KqUnit((kq.Word(1, "K־"),), (kq.Word(2, "Q־"),))) == "Q־"
    )  # qere governs
    assert (
        kq.join_text(kq.KqUnit((kq.Word(1, "K־"),), ())) == ""
    )  # no qere -> space follows


def test_xml_gen_30_11_k1q2():
    # בגד (ketiv) read as two words בָּא גָד (qere): one unit, 1 ketiv, 2 qeres.
    units = list(kq.iter_render_units(_read_verse_atoms(_GEN_XML, 30, 11)))
    kqs = [u for u in units if isinstance(u, kq.KqUnit)]
    assert len(kqs) == 1, f"expected one K/Q unit, got {len(kqs)}"
    unit = kqs[0]
    assert len(unit.ketivs) == 1 and unit.ketivs[0].text == "בגד"
    assert len(unit.qeres) == 2


def test_xml_sam2_21_12_adjacent_standard_then_grouped():
    # ...תְּלָאוּם (standard pair) immediately followed by grouped שם הפלשתים.
    units = list(kq.iter_render_units(_read_verse_atoms(_SAM2_XML, 21, 12)))
    kqs = [u for u in units if isinstance(u, kq.KqUnit)]
    standard = [u for u in kqs if len(u.ketivs) == 1 and len(u.qeres) == 1]
    grouped = [u for u in kqs if len(u.ketivs) == 2 and len(u.qeres) == 2]
    assert standard, "expected a standard (1,1) pair"
    assert grouped, "expected a grouped (2,2) unit"
    assert grouped[0].ketivs[0].text == "שם" and grouped[0].ketivs[1].text == "הפלשתים"


def test_xml_sam2_without_cases():
    # 8:3 is qere-without-ketiv; 13:33 is ketiv-without-qere.
    u83 = [
        u
        for u in kq.iter_render_units(_read_verse_atoms(_SAM2_XML, 8, 3))
        if isinstance(u, kq.KqUnit)
    ]
    assert any(
        u.ketivs == () and len(u.qeres) >= 1 for u in u83
    ), "8:3 should have a qere-without-ketiv unit"
    u1333 = [
        u
        for u in kq.iter_render_units(_read_verse_atoms(_SAM2_XML, 13, 33))
        if isinstance(u, kq.KqUnit)
    ]
    assert any(
        u.qeres == () and len(u.ketivs) >= 1 for u in u1333
    ), "13:33 should have a ketiv-without-qere unit"
