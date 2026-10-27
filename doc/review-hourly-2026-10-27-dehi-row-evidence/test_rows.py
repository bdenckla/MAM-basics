"""Compare the nine FOI forms with parent data and committed MAM-with-doc verses."""

from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess

from lxml import html

from mb_cmn import paths

ROOT = paths.repo_root()
OUT = ROOT / ".novc/hourly"
OLD = "d0cc6752d9820d3038ae0f72c2886190ed431c6e"
NEW = "3b23037b7e1752fdce2f7d5fa78cc5b9a3476f77"
FOI = "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg"
ROWS = json.loads((ROOT / (FOI + ".json")).read_text())


def parent(path):
    return subprocess.check_output(["git", "show", f"{OLD}:{path}"], cwd=ROOT)


def spaced(text):
    return " ".join((text or "").split())


def signature(node):
    return (
        node.tag,
        sorted(node.attrib.items()),
        spaced(node.text),
        [(signature(child), spaced(child.tail)) for child in node],
    )


def test_endpoint_and_raw_json_preservation():
    assert (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
        == NEW
    )
    changed = (
        subprocess.check_output(
            ["git", "diff", "--name-only", "-z", OLD, NEW], cwd=ROOT
        )
        .decode()
        .split("\0")
    )
    assert set(filter(None, changed)) == {
        FOI + ".html",
        FOI + ".json",
        "py/foi/dexi_stress_meteg_explanations.py",
        "py/foi/foiz_wt_dexi_stress_meteg.py",
    }
    previous = json.loads(parent(FOI + ".json"))
    assert len(ROWS) == len(previous) == 9
    stripped = deepcopy(ROWS)
    for row in stripped:
        del row["mam_with_doc"]
    assert stripped == previous


def test_nine_forms_against_mwd_verses_and_independent_kept_forms():
    prior = Path(
        "/workspace/scratch/review-hourly-20261027-kept-meteg/source-raw/hourly/lightweight-result.json"
    )
    cases = json.loads(prior.read_text())["raw_meteg_replacement_cases"]
    expected = {case["reference"]: case for case in cases}
    names = {"Ps": "D1-Psalms", "Pr": "D2-Proverbs", "Jb": "D3-Job"}
    books, checked = {}, []
    for row in ROWS:
        case = expected[row["bcv_short"]]
        assert row["r"] == case["parameter_1"]
        assert row["parameter_2"] == case["parameter_2"]
        assert row["mam_with_doc"] == case["independent_kept_form"]
        prefix, chapter, verse = re.fullmatch(
            r"(Ps|Pr|Jb)(\d+):(\d+)", row["bcv_short"]
        ).groups()
        if prefix not in books:
            books[prefix] = html.fromstring(
                (ROOT / f"gh-pages/MAM-with-doc/{names[prefix]}.html").read_bytes()
            )
        (anchor,) = books[prefix].xpath(f'//*[@id="c{chapter}v{verse}"]')
        verse_cell = anchor.getparent().xpath("./td")[1]
        targets = verse_cell.xpath('.//span[contains(@class,"mam-doc-target")]')
        matching = [
            target
            for target in targets
            if "".join("".join(target.itertext()).split()) == row["mam_with_doc"]
        ]
        assert len(matching) == 1, row["bcv_short"]
        checked.append(
            {
                "reference": row["bcv_short"],
                "parameter_1": row["r"],
                "raw_parameter_2": row["parameter_2"],
                "mam_with_doc": row["mam_with_doc"],
                "verse_target_exact": True,
            }
        )
    (OUT / "nine-row-comparison.json").write_text(
        json.dumps(
            {
                "rows": checked,
                "parent_raw_data_and_notes_preserved": True,
                "independent_kept_forms_match": True,
                "all_nine_mwd_verse_targets_match": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


def test_html_changes_are_only_explanation_and_nine_lower_forms():
    previous = html.fromstring(parent(FOI + ".html"))
    current = html.fromstring((ROOT / (FOI + ".html")).read_bytes())
    old_rows, new_rows = previous.xpath("//table/tr"), current.xpath("//table/tr")
    assert len(old_rows) == len(new_rows) == len(ROWS) == 9
    for row, old, new in zip(ROWS, old_rows, new_rows):
        old_cell, new_cell = old.xpath("./td")[1], new.xpath("./td")[1]
        assert spaced(old_cell.text) == spaced(new_cell.text) == row["r"]
        (old_break,), (new_break,) = old_cell.xpath("./br"), new_cell.xpath("./br")
        assert spaced(old_break.tail) == row["parameter_2"]
        assert spaced(new_break.tail) == row["mam_with_doc"]
        assert old_cell.attrib == new_cell.attrib
        assert new_cell.get("lang") == "hbo" and new_cell.get("dir") == "rtl"
        old_break.tail = new_break.tail
    old_intro, new_intro = previous.xpath("/html/body/div/p"), current.xpath(
        "/html/body/div/p"
    )
    assert len(old_intro) == len(new_intro)
    assert not len(old_intro[1]) and not len(new_intro[1])
    old_intro[1].text = new_intro[1].text
    assert signature(previous) == signature(current)
    (OUT / "html-endpoint-comparison.json").write_text(
        json.dumps(
            {
                "nine_upper_forms_preserved": True,
                "nine_lower_forms_match_mwd": True,
                "all_other_markup_notes_links_examples_and_counts_unchanged": True,
                "only_other_text_change": "Second introductory paragraph explains the displayed MAM-with-doc form.",
            },
            indent=2,
        )
        + "\n"
    )
