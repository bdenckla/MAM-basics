"""Focused differential and guard checks for actual helper inputs and census output."""

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

from lxml import html
import pytest

from foi import foi_finals, foi_struct
from foi import foiz_wt_dexi_stress_meteg as dsm
from mb_cmn import bib_locales as tbn, paths, ws_tmpl2 as wtp
from mb_cmn.minirow import MinirowExt
from mwd import mwd_write_book as mwd
from near_aleppo import foi_qere_without_ketiv as near_foi
from render_wt import render_wikitext as rwt
from render_wt import render_wikitext_handlers as handlers
from render_wt import render_wikitext_helpers as helpers

ROOT = paths.repo_root()
OUT = ROOT / ".novc/hourly"
LIGHT = json.loads((OUT / "lightweight-result.json").read_text())
DEHI = "\N{HEBREW ACCENT DEHI}"
METEG = "\N{HEBREW POINT METEG}"
SLH = "מ:אות-מיוחדת-במילה"
PAIR = LIGHT["raw_meteg_replacement_cases"][0]
BCVT = tbn.mk_bcvtmam("Psalms", 44, 27)
KEPT = {
    (case["parameter_1"], case["parameter_2"]): case["independent_kept_form"]
    for case in LIGHT["raw_meteg_replacement_cases"]
}


def context(option):
    return handlers.default_hctx(BCVT, {"ro_stress_helper": option}, {})


def helper():
    return {
        "tmpl_name": "מ:דחי",
        "tmpl_params": {"1": PAIR["parameter_1"], "2": PAIR["parameter_2"]},
    }


def note(target, label="INNER", body=None):
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


def row_targets(found):
    return [target for path, target in found if path == dsm.ROWS_FOI_PATH]


def flatten(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return "".join(map(flatten, value))
    return flatten(value.get("contents", ()))


@pytest.fixture(scope="module")
def actual_helpers():
    result = []

    def walk(value):
        if isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, dict):
            if value.get("tmpl_name") in {"מ:דחי", "מ:צינור"}:
                result.append(value)
            for child in value.values():
                walk(child)

    for name in ("D1-Psalms", "D2-Proverbs", "D3-Job"):
        walk(json.loads((ROOT / f"MAM-parsed/plus/{name}.json").read_text()))
    assert len(result) == 2373
    return result


def test_every_actual_helper_in_every_option(actual_helpers):
    checked, changed, special = 0, 0, 0
    for template in actual_helpers:
        one, two = (wtp.template_param_val(template, key) for key in ("1", "2"))
        pair = (
            (one[0], two[0])
            if len(one) == len(two) == 1
            and isinstance(one[0], str)
            and isinstance(two[0], str)
            else None
        )
        third = [KEPT[pair]] if pair in KEPT else two
        changed += pair in KEPT
        special += isinstance(one[0], dict)
        original = deepcopy(template)
        for option, expected in (
            (None, one),
            ("rv-without-stress-helper", one),
            ("rv-with-stress-helper", two),
            ("rv-with-stress-helper-keeping-meteg", third),
        ):
            ctx = context(option)
            assert helpers.render_wtseq(ctx, [template]) == helpers.render_wtseq(
                ctx, expected
            )
            checked += 1
        assert template == original
    assert changed == 9 and special == 3
    (OUT / "actual-helper-options-result.json").write_text(
        json.dumps(
            {
                "raw_helper_calls": len(actual_helpers),
                "option_comparisons": checked,
                "kept_form_changes": changed,
                "special_letter_calls_preserved": special,
                "raw_inputs_unchanged": True,
            },
            indent=2,
        )
        + "\n"
    )


@pytest.mark.parametrize(
    "mutation",
    (
        "missing",
        "extra",
        "empty_selected",
        "empty_unselected",
        "unknown_option",
        "letters",
        "length",
        "no_change",
        "wrong_added_mark",
        "extra_removed_mark",
        "two_letters",
        "orphan_mark",
        "unsupported_wrapper",
        "nontext_wrapper",
    ),
)
def test_malformed_forms_reject(mutation):
    template = helper()
    params = template["tmpl_params"]
    option = "rv-with-stress-helper-keeping-meteg"
    if mutation == "missing":
        del params["2"]
    elif mutation == "extra":
        params["3"] = "א"
    elif mutation == "empty_selected":
        params["2"] = []
    elif mutation == "empty_unselected":
        params["1"] = ""
    elif mutation == "unknown_option":
        option = "unknown"
    elif mutation == "letters":
        params["2"] = params["2"].replace("ה", "א")
    elif mutation == "length":
        params["2"] += "א"
    elif mutation == "no_change":
        params["2"] = params["1"]
    elif mutation == "wrong_added_mark":
        params["2"] = params["1"].replace(METEG, "\N{HEBREW ACCENT MUNAH}")
    elif mutation == "extra_removed_mark":
        params["2"] = params["2"].replace("\N{HEBREW POINT QAMATS}", "")
    elif mutation == "two_letters":
        params["2"] += DEHI
    elif mutation == "orphan_mark":
        params["1"] = METEG + params["1"]
    elif mutation == "unsupported_wrapper":
        params["1"] = {"tmpl_name": "מודגש", "tmpl_params": {"1": params["1"]}}
        params["2"] = {"tmpl_name": "מודגש", "tmpl_params": {"1": params["2"]}}
    else:
        params["1"] = {
            "tmpl_name": SLH,
            "tmpl_params": {
                "1": params["1"],
                "2": {"tmpl_name": "מודגש", "tmpl_params": {"1": params["1"]}},
            },
        }
        params["2"] = deepcopy(params["1"])
    with pytest.raises((ValueError, AssertionError)):
        helpers.render_wtseq(context(option), [template])


def test_special_letter_classification_and_refusal(actual_helpers):
    specials = [
        t for t in actual_helpers if isinstance(wtp.template_param_val(t, "1")[0], dict)
    ]
    assert len(specials) == 3
    for template in specials:
        found = find([template])
        assert len(found) == 1 and found[0][0] == dsm.CENSUS_FOI_PATHS[dsm.NO_METEG]
    # Existing special-letter records may be compared through their uninterrupted
    # text, but keeping a removed meteg inside one is explicitly unsupported.
    template = deepcopy(specials[0])
    for key in ("1", "2"):
        value = wtp.template_param_val(template, key)[0]
        value["tmpl_params"]["2"] = PAIR["parameter_" + key]
    with pytest.raises(ValueError, match="meteg to keep"):
        helpers.render_wtseq(context("rv-with-stress-helper-keeping-meteg"), [template])
    with pytest.raises(ValueError, match="row with a special-letter"):
        find([note([template])])


def test_nested_note_body_and_population_boundaries():
    inner = note([helper()])
    outer = note([inner], "OUTER")
    targets = row_targets(find([outer]))
    assert len(targets) == 1
    text = flatten(foi_struct.qtar_qual(targets[0])["note"])
    assert (
        "INNER:" in text
        and "OUTER:" not in text
        and PAIR["independent_kept_form"] in text
    )
    assert len(row_targets(find([inner], cp=[inner], dp=[inner], next_cp=[inner]))) == 3
    ending = dsm.find_fois_wt(
        {"mroge-bcvt": BCVT, "mroge-good-ending": {"wikitext_element": inner}}
    )
    assert len(row_targets(ending)) == 1
    with pytest.raises(ValueError, match="in no note's target"):
        find([note("א", body=[helper()])])
    with pytest.raises(ValueError, match="note lacks"):
        find([note([helper()], body="missing quotation")])


def test_census_html_examples_and_empty_rows(tmp_path, monkeypatch):
    all_fois = foi_struct.make_empty_all_fois()
    foi_struct.declare_foi_paths(all_fois, dsm.FOI_PATHS)
    for kind, example in LIGHT["first_raw_examples"].items():
        if kind == dsm.METEG_ON_HELPER_LETTER:
            continue
        target = foi_struct.make_qtarget(
            example["parameter_1"], {"parameter_2": example["parameter_2"]}
        )
        # Keep the two required example populations larger than the listed one.
        foi_struct.record_fois_for_1_verse(
            all_fois, BCVT, [(dsm.CENSUS_FOI_PATHS[kind], target)]
        )
    monkeypatch.setattr(foi_finals, "_OUT_DIR_PATH", str(tmp_path))
    foi_finals.write("args-foi-dexi-stress-meteg", all_fois)
    assert json.loads((tmp_path / "foi-dexi-stress-meteg.json").read_text()) == []
    document = html.fromstring((tmp_path / "foi-dexi-stress-meteg.html").read_bytes())
    assert "In none is a meteg" in " ".join(document.text_content().split())
    assert len(document.xpath('//p[contains(@style,"text-align: center")]')) == 2
    assert not document.xpath("//table") and document.xpath('//*[@id="intro"]')
    assert not (tmp_path / "index.html").exists()


def test_near_aleppo_foi_option_does_not_inherit_kept_meteg(monkeypatch):
    calls = []
    original = rwt.render
    options = deepcopy(mwd.RENOPTS_MAM_WITH_DOC)

    def observe(book, books, renopts, log):
        calls.append(deepcopy(renopts))
        return original(book, books, renopts, log)

    monkeypatch.setattr(rwt, "render", observe)
    rows = near_foi.records()
    result = near_foi.mam_examples(rows)
    assert (
        result
        and calls
        and all(
            option["ro_stress_helper"] == "rv-without-stress-helper" for option in calls
        )
    )
    assert mwd.RENOPTS_MAM_WITH_DOC == options
    (OUT / "near-foi-isolation-result.json").write_text(
        json.dumps(
            {
                "study_rows": len(rows),
                "book_calls": len(calls),
                "all_use_parameter_1": True,
                "mwd_options_unchanged": True,
            },
            indent=2,
        )
        + "\n"
    )
