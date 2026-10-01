"""Corpus-shaped checks for the closed, file-free untangler preparation boundary."""

import copy
import json
from collections import defaultdict

import pytest

from mb_cmn import bib_locales, paths, read_books_from_mam_parsed_plus
from phonetic_mam import compute
from phonetic_mam.core import dualcant_prepare, dualcant_templates


def _books():
    for book in bib_locales.BK39IDS_OF_BOOKS_WITH_DUALCANT:
        parsed = read_books_from_mam_parsed_plus.read_parsed_plus_bk24(
            bib_locales.bk24id(book), str(paths.mam_parsed_dir())
        )
        yield [list(verse.EP) for verse in parsed[book]["verses_plus"].values()]


def _collect_shapes(value, shapes):
    if isinstance(value, (tuple, list)):
        for element in value:
            _collect_shapes(element, shapes)
    elif isinstance(value, dict):
        shapes[value["tmpl_name"]].add(tuple(value.get("tmpl_params", {})))
        for child in value.get("tmpl_params", {}).values():
            _collect_shapes(child, shapes)


def test_preparation_shape_roster_matches_current_public_inputs():
    observed = defaultdict(set)
    for verses in _books():
        for verse in verses:
            dualcant_templates.validate_sequence(verse, allow_dual=True)
        _collect_shapes(verses, observed)
    assert dict(observed) == {
        name: set(shapes) for name, shapes in dualcant_templates._SHAPES.items()
    }


def test_preparation_operation_matches_direct_core_without_file_access(monkeypatch):
    books = list(_books())
    direct = [dualcant_prepare.prepare(verses) for verses in books]

    def denied(*_args, **_kwargs):
        raise AssertionError("computation attempted file access")

    monkeypatch.setattr("builtins.open", denied)
    monkeypatch.setattr("pathlib.Path.open", denied)
    for verses, expected in zip(books, direct):
        actual = compute.execute(
            {
                "schema": compute.SCHEMA,
                "operation": "prepare-untanglers",
                "arguments": {"verses": verses},
            }
        )
        assert actual == expected
        assert json.loads(json.dumps(actual)) == json.loads(json.dumps(expected))


def test_preparation_rejects_unclassified_template_shapes():
    dual = next(
        copy.deepcopy(element)
        for verses in _books()
        for verse in verses
        for element in verse
        if isinstance(element, dict) and element["tmpl_name"] == "מ:כפול"
    )
    unknown_name = {**dual, "tmpl_name": "unknown-template"}
    unknown_field = {**dual, "unknown-field": ""}
    unknown_parameter = copy.deepcopy(dual)
    unknown_parameter["tmpl_params"]["unknown-parameter"] = ""
    nested = {"tmpl_name": "נוסח", "tmpl_params": {"1": dual, "2": ""}}
    for malformed in (unknown_name, unknown_field, unknown_parameter, nested):
        with pytest.raises(ValueError):
            dualcant_prepare.prepare([[malformed]])
