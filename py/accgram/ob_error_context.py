from __future__ import annotations

import json
import re
from pathlib import Path

from accgram import ob_tree_parse

_OUTPUT_FILE_BB_RE = re.compile(r"^wlc_422_ps_([A-Za-z0-9]+)_ag\.json$")
_NODE_LINE_RE = re.compile(r"^\s*(\d+)\s+(\S(?:.*\S)?)\s*$")
_ERROR_TOKEN_RE = re.compile(r"\bERROR\b")


ErrorTree = ob_tree_parse.ErrorTree


def collect_error_trees_by_ref(
    rows: list[dict[str, object]],
    base_dir: Path,
) -> dict[str, ErrorTree | None]:
    """Map each ungrammatical row's ref to its ERROR tree, read from the JSON outputs.

    Each row carries an ``output_file`` (a ``wlc_422_ps_<bb>_ag.json`` under
    ``base_dir``, issue #20); the per-verse ``tree`` field is the nested image
    written by ``tree.tree_to_obj``, converted here to an ``ErrorTree`` (or None
    when the verse has no ERROR leaf -- e.g. a row that is no longer an ungrammatical verse).
    """
    refs_by_file: dict[str, set[str]] = {}
    for row in rows:
        refs_by_file.setdefault(_row_output_file(row), set()).add(_row_ref(row))

    out: dict[str, ErrorTree | None] = {}
    for output_file, refs in refs_by_file.items():
        bb = _bb_from_output_file(output_file)
        trees_by_ref = (
            {} if bb is None else _book_tree_objs_by_ref(base_dir / output_file, bb)
        )
        for ref in refs:
            out[ref] = ob_tree_parse.error_tree_from_obj(trees_by_ref.get(ref))
    return out


def _book_tree_objs_by_ref(output_path: Path, bb: str) -> dict[str, dict | None]:
    """ref ("ob 1:2") -> the verse's ``tree`` object, for one book's JSON file."""
    if not output_path.is_file():
        return {}
    with output_path.open("r", encoding="utf-8") as f_in:
        payload = json.load(f_in)
    out: dict[str, dict | None] = {}
    for verse in payload.get("verses", []):
        bcv = verse.get("bcv", "")
        # bcv ("ob1:2") -> the row-style ref ("ob 1:2") the ungrammatical rows key on.
        out[f"{bb} {bcv[len(bb):]}"] = verse.get("tree")
    return out


def parse_error_tree_from_text(tree_text: str) -> ErrorTree | None:
    """Parse an already-rendered ERROR tree (e.g. poetic ``print_tree`` output)
    into an ``ErrorTree``, single-sourcing the node/ERROR line regexes.

    Returns None when the text holds no ERROR leaf (so a clean tree, or a
    non-tree line such as the poetic ``NO_PARSE: ...`` form, yields None).
    """
    return _extract_error_tree(tree_text.splitlines())


def parse_tree_from_text(tree_text: str) -> ErrorTree | None:
    """Parse a rendered ``print_tree`` -- clean OR ERROR -- into an ``ErrorTree``.

    Unlike :func:`parse_error_tree_from_text` (which yields None for an
    error-free tree), this returns the parsed tree regardless of whether it
    holds an ERROR leaf, so a clean parse can still be rendered as a table by
    ``ob_tree_table.render_error_tree_table`` (error cells are simply absent).
    Returns None only when the text has no tree node lines at all.
    """
    lines = tree_text.splitlines()
    if not lines:
        return None
    tree = ob_tree_parse.parse_verse_tree(
        verse_lines=lines,
        node_line_re=_NODE_LINE_RE,
        error_token_re=_ERROR_TOKEN_RE,
    )
    return tree if tree.roots else None


def _extract_error_tree(verse_lines: list[str]) -> ErrorTree | None:
    if not verse_lines:
        return None

    tree = ob_tree_parse.parse_verse_tree(
        verse_lines=verse_lines,
        node_line_re=_NODE_LINE_RE,
        error_token_re=_ERROR_TOKEN_RE,
    )
    if not tree.has_error_leaf:
        return None
    return tree


def _bb_from_output_file(output_file: str) -> str | None:
    match = _OUTPUT_FILE_BB_RE.match(output_file)
    if match is None:
        return None
    return match.group(1).lower()


def _row_ref(row: dict[str, object]) -> str:
    ref = row.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError("Ungrammatical row is missing non-empty string field 'ref'")
    return ref.strip()


def _row_output_file(row: dict[str, object]) -> str:
    output_file = row.get("output_file")
    if not isinstance(output_file, str) or not output_file.strip():
        raise ValueError(
            "Ungrammatical row is missing non-empty string field 'output_file'"
        )
    return output_file.strip()
