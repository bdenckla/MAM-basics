"""Compare all semantic fields with the parent and independently selected raw forms."""

from copy import deepcopy
from dataclasses import asdict
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mwd import mwd_write_book as mwd
from near_aleppo import edition
from render_wt import render_wikitext as rwt

ROOT = paths.repo_root()
OUT = ROOT / ".novc/hourly"
TASK = Path("/workspace/review-hourly-20261027-kept-meteg")
OLD = "46f80ecc8b29fdd7f5fdf30c40bc2b3382bbb352"
NEW = "d0cc6752d9820d3038ae0f72c2886190ed431c6e"
BOOKS = ("Psalms", "Proverbs", "Job")
HEAD = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
LIGHT = json.loads((TASK / "source/.novc/hourly/lightweight-result.json").read_text())
KEPT = {
    (row["parameter_1"], row["parameter_2"]): row["independent_kept_form"]
    for row in LIGHT["raw_meteg_replacement_cases"]
}


def canonical(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def rewritten(value):
    if isinstance(value, list):
        return [rewritten(child) for child in value]
    if not isinstance(value, dict):
        return value
    result = {key: rewritten(child) for key, child in value.items()}
    if value.get("tmpl_name") == "מ:דחי":
        params = value["tmpl_params"]
        if isinstance(params["1"], str) and isinstance(params["2"], str):
            pair = params["1"], params["2"]
            if pair in KEPT:
                result["tmpl_params"]["2"] = KEPT[pair]
    return result


def selected_loader(path):
    return rewritten(json.loads(Path(path).read_text()))


def render(books, options):
    return {
        book: {
            str(ref): asdict(value)
            for ref, value in rwt.render(book, books, options, {}).items()
        }
        for book in BOOKS
    }


def test_all_semantic_fields_and_options_against_parent():
    books = plus.read_parsed_plus_bk39s(BOOKS, paths.mam_parsed_path())
    original = deepcopy(books)
    raw_options = {
        **mwd.RENOPTS_MAM_WITH_DOC,
        "ro_stress_helper": "rv-with-stress-helper",
    }
    options_before = deepcopy(mwd.RENOPTS_MAM_WITH_DOC)
    records = {
        "default": render(books, None),
        "near": render(books, edition.NEAR_ALEPPO_MODE.renopts),
        "raw_parameter_2": render(books, raw_options),
    }
    if HEAD == OLD:
        selected = plus.read_parsed_plus_bk39s(
            BOOKS, paths.mam_parsed_path(), load_json=selected_loader
        )
        records["kept_expected"] = render(selected, raw_options)
        (OUT / "parent-render-records.json.gz").write_bytes(
            gzip.compress(canonical(records), mtime=0)
        )
        return
    assert HEAD == NEW
    records["kept_expected"] = render(books, mwd.RENOPTS_MAM_WITH_DOC)
    parent_raw = gzip.decompress(
        (TASK / "baseline/.novc/hourly/parent-render-records.json.gz").read_bytes()
    )
    assert canonical(records) == parent_raw
    assert render(books, None) == records["default"]
    assert books == original and mwd.RENOPTS_MAM_WITH_DOC == options_before
    result = {
        "parent": OLD,
        "source": NEW,
        "verses_per_mode": sum(len(value) for value in records["default"].values()),
        "modes": list(records),
        "all_semantic_and_documentation_fields_equal_to_parent_oracle": True,
        "kept_oracle": "Parent renderer with parameter 2 replaced only for exact raw pairs from the independently inspected nine replacement cases; no renderer handler patch or source-file write.",
        "default_and_raw_parameter_2_and_near_unchanged": True,
        "repeat_default_and_input_options_unchanged": True,
        "records_sha256": sha256(canonical(records)).hexdigest(),
    }
    (OUT / "render-oracle-result.json").write_text(json.dumps(result, indent=2) + "\n")
