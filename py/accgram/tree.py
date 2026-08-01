"""Python port of accutil.c: make_node, add_leaves, print_tree.

Reproduces the display_tree==1 path only.  Node layout mirrors the C `tn`
struct; output format is byte-for-byte identical to the C print_tree().
"""

from __future__ import annotations

from dataclasses import dataclass

INDENT_STRING = "  "


@dataclass
class TN:
    label: str
    left: TN | None = None
    right: TN | None = None
    leaves: tuple[str, ...] = ()


def make_node(label: str, left: TN, right: TN) -> TN:
    return TN(label=label, left=left, right=right)


def add_leaves(label: str, *leaf_names: str) -> TN:
    """Build a leaf node holding its leaf-names verbatim.

    The names are kept as a tuple (faithful, even for a multi-word leaf such as
    "sof pasuq"); print_tree re-appends the trailing space per name that the C
    strcat loop produced, and tree_to_obj serializes the tuple as a JSON list.
    """
    return TN(label=label, left=None, right=None, leaves=tuple(leaf_names))


def print_tree(tree: TN | None, indent_level: int = 0) -> str:
    """Return the C print_tree() output as a string.

    Internal node: <indent><level> <label>\\n, then recurse left then right.
    Leaf node: same header line, then <indent+1><leaves>\\n.
    """
    if tree is None:
        return ""
    indent = INDENT_STRING * indent_level
    out: list[str] = [f"{indent}{indent_level} {tree.label}\n"]
    if tree.left is not None:
        out.append(print_tree(tree.left, indent_level + 1))
        out.append(print_tree(tree.right, indent_level + 1))
    else:
        leaf_indent = INDENT_STRING * (indent_level + 1)
        leaves = "".join(name + " " for name in tree.leaves)
        out.append(f"{leaf_indent}{leaves}\n")
    return "".join(out)


def tree_to_obj(tree: TN | None) -> dict | None:
    """Serialize a TN into a JSON-ready nested dict (issue #20).

    Internal node -> ``{"label", "children": [left, right]}``; leaf node ->
    ``{"label", "leaves": [name, ...]}``.  Mirrors print_tree's internal/leaf
    split (``left is not None`` == internal) so the JSON is a lossless image of
    the binary tree.  ``None`` (a location-only verse) serializes to ``None``.
    """
    if tree is None:
        return None
    if tree.left is not None:
        return {
            "label": tree.label,
            "children": [tree_to_obj(tree.left), tree_to_obj(tree.right)],
        }
    return {"label": tree.label, "leaves": list(tree.leaves)}
