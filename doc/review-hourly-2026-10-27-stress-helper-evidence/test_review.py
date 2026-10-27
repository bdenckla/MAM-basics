"""Focused differential checks of helper selection, without changing source data."""

from collections import Counter
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import gzip
import json
from pathlib import Path
import subprocess

import pytest

from mb_cmn import paths
from mb_cmn import bib_locales as tbn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mwd import mwd_write_book as mwd
from near_aleppo import edition, foi_qere_without_ketiv as foi
from render_wt import render_wikitext as rwt
from render_wt import render_wikitext_handlers as handlers
from render_wt import render_wikitext_helpers as helpers

ROOT = paths.repo_root()
OLD = "629218d2f44c006f36eeb0dcb16e8eacdd052a41"
NEW = "9302ad04b347aa2db3ee0004962cd66202031cce"
HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
OUT = ROOT / ".novc/hourly"
BASELINE = Path("/workspace/review-hourly-20261027-stress-helper/baseline/.novc/hourly")
NAMES = {"מ:דחי", "מ:צינור"}
BOOKS = ("Psalms", "Proverbs", "Job")


def canonical(obj):
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()


def choose_input(value, parameter):
    """Feed the old renderer a selected strand in its existing parameter-1 slot."""
    if isinstance(value, list):
        return [choose_input(v, parameter) for v in value]
    if not isinstance(value, dict):
        return value
    if value.get("tmpl_name") in NAMES:
        params = value["tmpl_params"]
        return {
            "tmpl_name": value["tmpl_name"],
            "tmpl_params": {
                "1": choose_input(params[parameter], parameter),
                "2": deepcopy(params["2"]),
            },
        }
    return {key: choose_input(child, parameter) for key, child in value.items()}


def load_selected(path):
    return choose_input(json.loads(Path(path).read_text()), "2")


def render_books(books, options):
    return {
        book: {
            str(key): asdict(value)
            for key, value in rwt.render(book, books, options, {}).items()
        }
        for book in BOOKS
    }


def test_corpus_differential():
    books = plus.read_parsed_plus_bk39s(BOOKS, paths.mam_parsed_path())
    if HEAD == OLD:
        selected = plus.read_parsed_plus_bk39s(
            BOOKS, paths.mam_parsed_path(), load_json=load_selected
        )
        records = {
            "default": render_books(books, None),
            "near": render_books(books, edition.NEAR_ALEPPO_MODE.renopts),
            "mwd": render_books(selected, mwd.RENOPTS_MAM_WITH_DOC),
        }
        (OUT / "baseline-records.json.gz").write_bytes(
            gzip.compress(canonical(records), mtime=0)
        )
        return
    assert HEAD == NEW
    reference = json.loads(
        gzip.decompress((BASELINE / "baseline-records.json.gz").read_bytes())
    )
    records = {
        "default": render_books(books, None),
        "near": render_books(books, edition.NEAR_ALEPPO_MODE.renopts),
        "mwd": render_books(books, mwd.RENOPTS_MAM_WITH_DOC),
    }
    assert json.loads(canonical(records)) == reference
    without = render_books(books, {"ro_stress_helper": "rv-without-stress-helper"})
    assert json.loads(canonical(without)) == reference["default"]
    # A later default render must remain identical after the other modes ran.
    assert json.loads(canonical(render_books(books, None))) == reference["default"]
    result = {
        "parent": OLD,
        "source": NEW,
        "books": list(BOOKS),
        "verses_per_mode": sum(len(v) for v in records["default"].values()),
        "modes_compared": list(records),
        "all_render_elements_and_documentation_fields_equal_to_parent_oracle": True,
        "parent_mwd_input": "Only each selected helper's parameter 2 is supplied to the old renderer in its parameter-1 slot; no renderer handler is patched.",
        "default_explicit_without_and_repeat_equal": True,
        "render_records_sha256": sha256(canonical(records)).hexdigest(),
    }
    (OUT / "corpus-result.json").write_text(json.dumps(result, indent=2) + "\n")


@pytest.mark.skipif(
    HEAD == OLD, reason="Current-only selection/validation investigation"
)
def test_raw_inventory_and_nested_cases():
    counts, contexts, files = Counter(), Counter(), set()
    occurrences = []

    def walk(value, stack, path):
        if isinstance(value, list):
            for child in value:
                walk(child, stack, path)
        elif isinstance(value, dict):
            name = value.get("tmpl_name")
            if name in NAMES:
                counts[name] += 1
                files.add(path.name)
                contexts["/".join(stack[-3:])] += 1
                occurrences.append(value)
            for child in value.values():
                walk(child, stack + ((name,) if name else ()), path)

    for path in sorted((ROOT / "MAM-parsed/plus").glob("*.json")):
        walk(json.loads(path.read_text()), (), path)
    assert set(counts) == NAMES
    assert files == {"D1-Psalms.json", "D2-Proverbs.json", "D3-Job.json"}
    assert any("מ:קמץ" in key for key in contexts)
    checked = 0
    for template in occurrences:
        for option, parameter in (
            (None, "1"),
            ("rv-without-stress-helper", "1"),
            ("rv-with-stress-helper", "2"),
        ):
            ctx = handlers.default_hctx(
                tbn.mk_bcvtmam("Psalms", 1, 1), {"ro_stress_helper": option}, {}
            )
            # Select before the renderer, then compare every tag/field with normal dispatch.
            expected = helpers.render_wtseq(ctx, [choose_input(template, parameter)])
            actual = helpers.render_wtseq(ctx, [template])
            if parameter == "1":
                assert actual == expected
            else:
                old_ctx = handlers.default_hctx(
                    ctx.bcvt, {"ro_stress_helper": None}, {}
                )
                assert actual == helpers.render_wtseq(
                    old_ctx, [choose_input(template, parameter)]
                )
            checked += 1
    result = {
        "raw_occurrences": dict(counts),
        "files": sorted(files),
        "ancestor_contexts": dict(contexts),
        "occurrence_option_comparisons": checked,
    }
    (OUT / "inventory-result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )


@pytest.mark.skipif(
    HEAD == OLD, reason="Current-only selection/validation investigation"
)
def test_malformed_and_unselected_branches():
    counts = Counter()
    for name in sorted(NAMES):
        for params in (
            {},
            {"1": "א"},
            {"2": "ב"},
            {"1": "א", "2": "ב", "3": "ג"},
            {"1": "א", "2": "ב", "named": "ג"},
        ):
            ctx = handlers.default_hctx(tbn.mk_bcvtmam("Psalms", 1, 1), {}, {})
            with pytest.raises(ValueError, match="unexpected stress-helper parameters"):
                helpers.render_wtseq(ctx, [{"tmpl_name": name, "tmpl_params": params}])
            counts["bad_parameter_sets"] += 1
        for option, selected in (
            (None, "1"),
            ("rv-without-stress-helper", "1"),
            ("rv-with-stress-helper", "2"),
        ):
            ctx = handlers.default_hctx(
                tbn.mk_bcvtmam("Psalms", 1, 1), {"ro_stress_helper": option}, {}
            )
            other = "2" if selected == "1" else "1"
            for empty in ("", [], ["", ""]):
                params = {selected: empty, other: "א"}
                with pytest.raises(ValueError, match="empty stress-helper parameter"):
                    helpers.render_wtseq(
                        ctx, [{"tmpl_name": name, "tmpl_params": params}]
                    )
                counts["empty_selected"] += 1
            bad = {"tmpl_name": "unselected-invalid-template"}
            params = {
                selected: {
                    "tmpl_name": "מ:דחי",
                    "tmpl_params": {selected: "א", other: bad},
                },
                other: bad,
            }
            expected = helpers.render_wtseq(ctx, ["א"])
            assert (
                helpers.render_wtseq(ctx, [{"tmpl_name": name, "tmpl_params": params}])
                == expected
            )
            counts["nested_selected_and_unselected_isolation"] += 1
        ctx = handlers.default_hctx(
            tbn.mk_bcvtmam("Psalms", 1, 1), {"ro_stress_helper": "unknown"}, {}
        )
        with pytest.raises(ValueError, match="unknown ro_stress_helper value"):
            helpers.render_wtseq(
                ctx, [{"tmpl_name": name, "tmpl_params": {"1": "א", "2": "ב"}}]
            )
        counts["unknown_options"] += 1
    assert mwd.RENOPTS_MAM_WITH_DOC["ro_stress_helper"] == "rv-with-stress-helper"
    assert (
        edition.NEAR_ALEPPO_MODE.renopts["ro_stress_helper"]
        == "rv-without-stress-helper"
    )
    (OUT / "malformed-result.json").write_text(json.dumps(counts, indent=2) + "\n")


@pytest.mark.skipif(
    HEAD == OLD, reason="Current-only selection/validation investigation"
)
def test_near_aleppo_foi_uses_its_own_option(monkeypatch):
    calls = []
    real = rwt.render

    def observe(book, books, options, log):
        calls.append(deepcopy(options))
        return real(book, books, options, log)

    monkeypatch.setattr(rwt, "render", observe)
    rows = foi.records()
    result = foi.mam_examples(rows)
    assert result and calls
    assert all(
        option["ro_stress_helper"] == "rv-without-stress-helper" for option in calls
    )
    assert mwd.RENOPTS_MAM_WITH_DOC["ro_stress_helper"] == "rv-with-stress-helper"
    (OUT / "foi-result.json").write_text(
        json.dumps(
            {
                "rows": len(rows),
                "book_render_calls": len(calls),
                "all_calls_use_parameter_1": True,
                "mwd_options_not_mutated": True,
            },
            indent=2,
        )
        + "\n"
    )
