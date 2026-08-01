"""Unit tests for the poetic ungrammatical-verse report's NO_PARSE tree synthesis (issue #10).

NO_PARSE verses have no valid parse, so poetic_oddballs synthesizes a flat
best-effort "tree" (``_no_parse_tree_text``) that must round-trip through the
shared error-tree parser into an ERROR-leaf tree. The SAT focus-word logic lives
in poetic_sat and is tested in test_poetic_sat.py.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_poetic_oddballs.py -v
"""

from __future__ import annotations

from accgram import ob_error_context
from accgram import ob_tree_parse
from accgram import poetic_oddballs as po


def test_no_parse_tree_text_round_trips_to_error_tree() -> None:
    # TILDE/SOFPASUQ bookends are dropped; the accents become leaves under one
    # no_parse branch, capped by an ERROR leaf.
    text = po._no_parse_tree_text(("TILDE", "MERKHA", "ATNAX", "SILLUQ", "SOFPASUQ"))
    tree = ob_error_context.parse_error_tree_from_text(text)

    assert tree is not None
    assert tree.has_error_leaf
    assert len(tree.roots) == 1
    assert tree.roots[0].label == "no_parse"
    leaves = ob_tree_parse.iter_leaf_texts(tree)
    assert leaves == ["MERKHA", "ATNAX", "SILLUQ", "ERROR"]


def test_no_parse_tree_text_drops_only_bookends() -> None:
    text = po._no_parse_tree_text(("MERKHA", "SOFPASUQ", "TILDE", "ATNAX"))
    leaves = ob_tree_parse.iter_leaf_texts(
        ob_error_context.parse_error_tree_from_text(text)
    )
    assert leaves == ["MERKHA", "ATNAX", "ERROR"]
