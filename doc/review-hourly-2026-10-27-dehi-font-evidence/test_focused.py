"""Focused differential/guard checks for the committed dehi FOI and font assets."""

from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil

from lxml import etree, html
import pytest

from foi import foi_finals, foi_struct
from foi import foiz_wt_dexi_stress_meteg as dsm
from mb_cmn import bib_locales as tbn, paths
from mb_cmn.minirow import MinirowExt
from py_html import taamey_d_assets as assets

ROOT = paths.repo_root()
BCVT = tbn.mk_bcvtmam("Psalms", 44, 27)
ROWS = json.loads(
    (ROOT / "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg.json").read_text()
)
PAIR = ROWS[0]


def helper():
    return {
        "tmpl_name": "מ:דחי",
        "tmpl_params": {"1": PAIR["r"], "2": PAIR["parameter_2"]},
    }


def note(target, label="inner", body=None):
    return {
        "tmpl_name": "נוסח",
        "tmpl_params": {
            "1": target,
            "2": body if body is not None else f"{label}: {dsm.NOTE_WORDS}",
        },
    }


def find(sequence, *, cp=(), dp=(), next_cp=()):
    return dsm.find_fois_wt(
        {
            "mroge-bcvt": BCVT,
            "mroge-minirow": MinirowExt(
                tuple(cp), tuple(dp), tuple(sequence), tuple(next_cp)
            ),
        }
    )


def rows_only(found):
    return [target for path, target in found if path == dsm.ROWS_FOI_PATH]


def flatten(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (tuple, list)):
        return "".join(map(flatten, value))
    return flatten(value.get("contents", ()))


def test_nested_note_selection_and_body_boundaries():
    inner = note([helper()], "INNER")
    outer = note([inner], "OUTER")
    found = rows_only(find([outer]))
    assert len(found) == 1
    selected = flatten(foi_struct.qtar_qual(found[0])["note"])
    assert "INNER:" in selected and "OUTER:" not in selected
    inside_body = note("א", "OUTER", [inner])
    found = rows_only(find([inside_body]))
    assert len(found) == 1 and "INNER:" in flatten(
        foi_struct.qtar_qual(found[0])["note"]
    )
    with pytest.raises(ValueError, match="in no note's target"):
        find([note("א", body=[helper()])])
    with pytest.raises(ValueError, match="in no note's target"):
        find([helper()])
    with pytest.raises(ValueError, match="note lacks"):
        find([note([helper()], body="missing required quotation")])


def test_all_cells_good_ending_and_nested_parameters():
    n = note([helper()])
    found = find([n], cp=[n], dp=[n], next_cp=[n])
    assert len(rows_only(found)) == 3
    assert (
        Counter(path for path, _ in found)[
            dsm.CENSUS_FOI_PATHS[dsm.METEG_ON_HELPER_LETTER]
        ]
        == 3
    )
    good = dsm.find_fois_wt(
        {"mroge-bcvt": BCVT, "mroge-good-ending": {"wikitext_element": n}}
    )
    assert len(rows_only(good)) == 1
    nested = {"tmpl_name": "מ:דחי", "tmpl_params": {"1": helper(), "2": helper()}}
    found = find([note([nested])])
    counts = Counter(path for path, _ in found)
    assert counts[dsm.CENSUS_FOI_PATHS[dsm.TEMPLATE_IN_PARAMETER]] == 1
    assert counts[dsm.CENSUS_FOI_PATHS[dsm.METEG_ON_HELPER_LETTER]] == 2
    assert len(rows_only(found)) == 2


@pytest.mark.parametrize(
    "mutation", ("letters", "unchanged", "different_added_mark", "extra_removed_mark")
)
def test_classification_refuses_changed_claim_inputs(mutation):
    template = helper()
    params = template["tmpl_params"]
    if mutation == "letters":
        params["2"] += "א"
    elif mutation == "unchanged":
        params["2"] = params["1"]
    elif mutation == "different_added_mark":
        params["2"] = params["1"].replace(
            "\N{HEBREW POINT METEG}", "\N{HEBREW ACCENT MUNAH}"
        )
    else:
        params["2"] = params["2"].replace("\N{HEBREW POINT QAMATS}", "")
    with pytest.raises(ValueError):
        find([note([template])])


def test_counted_paths_stay_out_of_rows_and_empty_section_remains(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(foi_finals, "_OUT_DIR_PATH", str(tmp_path))
    all_fois = foi_struct.make_empty_all_fois()
    foi_struct.declare_foi_paths(all_fois, dsm.FOI_PATHS)
    # Use real census proportions, but remove the listed population to check the
    # existing empty-section contract without claiming an empty corpus.
    counts = {
        dsm.NO_METEG: 2050,
        dsm.METEG_ON_EARLIER_ATOM: 161,
        dsm.METEG_EARLIER_IN_STRESSED_ATOM: 94,
        dsm.METEG_ON_HELPER_LETTER: 0,
        dsm.TEMPLATE_IN_PARAMETER: 3,
    }
    for kind, count in counts.items():
        all_fois[dsm.CENSUS_FOI_PATHS[kind]] = [None] * count
    foi_finals.write("args-foi-dexi-stress-meteg", all_fois)
    assert json.loads((tmp_path / "foi-dexi-stress-meteg.json").read_text()) == []
    page = (tmp_path / "foi-dexi-stress-meteg.html").read_text()
    text = " ".join(html.fromstring(page).text_content().split())
    assert "In none is a meteg" in text and 'id="intro"' in page
    assert "<table" not in page
    assert "census/" not in page
    assert not (tmp_path / "index.html").exists()


def test_nine_notes_match_mam_with_doc_cells():
    files = {"Ps": "D1-Psalms", "Pr": "D2-Proverbs", "Jb": "D3-Job"}
    books = {}
    for row in ROWS:
        match = re.fullmatch(r"(Ps|Pr|Jb)(\d+):(\d+)", row["bcv_short"])
        prefix, chapter, verse = match.groups()
        if prefix not in books:
            books[prefix] = html.fromstring(
                (ROOT / f"gh-pages/MAM-with-doc/{files[prefix]}.html").read_bytes()
            )
        (anchor,) = books[prefix].xpath(f'//*[@id="c{chapter}v{verse}"]')
        cell = anchor.getparent().xpath("./td")[-1]
        normalize = lambda text: "".join((text or "").split())
        candidates = [
            n
            for n in cell.xpath('.//span[@class="mam-doc-lemma"]')
            if normalize("".join(n.itertext())) == normalize(row["parameter_2"])
        ]
        assert len(candidates) == 1, row["bcv_short"]
        lemma = candidates[0]
        if lemma.getnext().tag == "a":
            page, fragment = lemma.getnext().get("href").split("#")
            large = html.fromstring(
                (ROOT / "gh-pages/MAM-with-doc" / page).read_bytes()
            )
            (part,) = large.xpath(f'//*[@id="{fragment}"]')
            lemma = part.getprevious()

        def from_json(value):
            node = etree.Element(value["_htel_tag"], value.get("attr", {}))
            previous = None
            for child in value.get("contents", []):
                if isinstance(child, str):
                    if previous is None:
                        node.text = (node.text or "") + child
                    else:
                        previous.tail = (previous.tail or "") + child
                else:
                    previous = from_json(child)
                    node.append(previous)
            return node

        def signature(node):
            node = deepcopy(node)
            etree.strip_tags(node, "wbr")
            return (
                node.tag,
                sorted((key, val) for key, val in node.attrib.items() if key != "id"),
                normalize(node.text),
                [(signature(child), normalize(child.tail)) for child in node],
            )

        expected = [
            from_json(value) for value in row["note"] if isinstance(value, dict)
        ]
        actual = []
        for _ in expected:
            actual.append(lemma)
            lemma = lemma.getnext()
        assert [signature(node) for node in actual] == [
            signature(node) for node in expected
        ], row["bcv_short"]


def test_site_asset_mapping_is_exact():
    result = assets.site_font_assets()
    assert len(result) == 9
    assert all(
        (ROOT / "gh-pages" / name).read_bytes() == data for name, data in result.items()
    )


@pytest.mark.parametrize(
    "corruption", ("font", "archive", "support", "inventory_members")
)
def test_production_hash_and_member_guards(tmp_path, monkeypatch, corruption):
    root = tmp_path / "root"
    support = root / "in/font-support/taamey-d-1.0"
    shutil.copytree(ROOT / "in/font-support/taamey-d-1.0", support)
    font = root / "font.woff2"
    font.write_bytes(assets.font_bytes())
    monkeypatch.setattr(assets, "font_path", lambda: font)
    monkeypatch.setattr(assets.paths, "repo_root", lambda: root)
    if corruption == "font":
        font.write_bytes(font.read_bytes() + b"corrupt")
        pattern = "pinned Taamey D"
    elif corruption == "archive":
        archive = support / "Taamey_D-1.0-sources.zip"
        archive.write_bytes(archive.read_bytes() + b"corrupt")
        pattern = "source archive differs"
    elif corruption == "support":
        (support / "BUILD.txt").write_bytes(b"corrupt")
        pattern = "BUILD.txt differs"
    else:
        path = support / "SOURCE-INVENTORY.json"
        data = json.loads(path.read_text())
        data["source_archive"]["members"].pop()
        path.write_text(json.dumps(data))
        monkeypatch.setattr(
            assets,
            "_SUPPORT_SHA256",
            {
                **assets._SUPPORT_SHA256,
                "SOURCE-INVENTORY.json": sha256(path.read_bytes()).hexdigest(),
            },
        )
        pattern = "archive members differ"
    with pytest.raises(ValueError, match=pattern):
        assets.site_font_assets()
