"""Corpus-shaped checks for the closed, file-free untangler preparation boundary."""

import json
from collections import defaultdict

from mb_cmn import bib_locales, paths, read_books_from_mam_parsed_plus
from phonetic_mam import compute
from phonetic_mam.core import dualcant_templates


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


def test_preparation_operation_runs_without_file_access(monkeypatch):
    books = list(_books())
    assert books, "the dual-cantillation books are missing"

    def denied(*_args, **_kwargs):
        raise AssertionError("computation attempted file access")

    monkeypatch.setattr("builtins.open", denied)
    monkeypatch.setattr("pathlib.Path.open", denied)
    for verses in books:
        result = compute.execute(
            {
                "schema": compute.SCHEMA,
                "operation": "prepare-untanglers",
                "arguments": {"verses": verses},
            }
        )
        # Each reply must encode as compute.serve encodes it.
        assert json.dumps(result, ensure_ascii=False, allow_nan=False)
