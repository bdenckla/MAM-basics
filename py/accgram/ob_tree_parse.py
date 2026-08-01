from __future__ import annotations

from dataclasses import dataclass
from re import Pattern


@dataclass
class TreeLeaf:
    text: str
    has_error: bool


@dataclass
class TreeBranch:
    depth: int
    label: str
    children: list[TreeBranch | TreeLeaf]


@dataclass
class ErrorTree:
    roots: list[TreeBranch]
    has_error_leaf: bool


def parse_verse_tree(
    *,
    verse_lines: list[str],
    node_line_re: Pattern[str],
    error_token_re: Pattern[str],
) -> ErrorTree:
    roots: list[TreeBranch] = []
    stack: list[TreeBranch] = []
    has_error_leaf = False

    for line in verse_lines:
        stripped = line.strip()
        if not stripped:
            continue

        node_match = node_line_re.match(line)
        if node_match is not None:
            depth = int(node_match.group(1))
            label = node_match.group(2).strip()

            while stack and stack[-1].depth >= depth:
                stack.pop()

            branch = TreeBranch(depth=depth, label=label, children=[])
            if stack:
                stack[-1].children.append(branch)
            else:
                roots.append(branch)
            stack.append(branch)
            continue

        if not stack:
            raise ValueError(
                "Leaf line encountered before any branch node: " f"{stripped!r}"
            )

        has_error = error_token_re.search(stripped) is not None
        has_error_leaf = has_error_leaf or has_error
        stack[-1].children.append(TreeLeaf(text=stripped, has_error=has_error))

    return ErrorTree(roots=roots, has_error_leaf=has_error_leaf)


def error_tree_from_obj(tree_obj: dict | None) -> ErrorTree | None:
    """Build an ``ErrorTree`` from a ``tree.tree_to_obj`` nested dict (issue #20).

    Each node dict carries a ``label``; an internal node has ``children`` (a
    nested ``tree_to_obj`` image), a leaf node has ``leaves`` (a list of
    leaf-names).  A TN leaf node maps to a ``TreeBranch`` whose single child is
    a ``TreeLeaf`` holding the space-joined leaves -- the same shape the old
    indented-text parser produced (the leaf line printed under its label).
    ``depth`` mirrors print_tree's indent level (root 0, children +1).

    Returns ``None`` for a missing tree (location-only verse) or one with no
    ERROR leaf, matching the text-era ``_extract_error_tree`` contract.
    """
    if tree_obj is None:
        return None
    root = _branch_from_obj(tree_obj, depth=0)
    tree = ErrorTree(roots=[root], has_error_leaf=_branch_has_error(root))
    return tree if tree.has_error_leaf else None


def _branch_from_obj(node: dict, depth: int) -> TreeBranch:
    branch = TreeBranch(depth=depth, label=node["label"], children=[])
    children = node.get("children")
    if children is not None:
        for child in children:
            branch.children.append(_branch_from_obj(child, depth + 1))
    else:
        leaves = node.get("leaves", [])
        branch.children.append(
            TreeLeaf(text=" ".join(leaves), has_error="ERROR" in leaves)
        )
    return branch


def _branch_has_error(branch: TreeBranch) -> bool:
    return any(
        child.has_error if isinstance(child, TreeLeaf) else _branch_has_error(child)
        for child in branch.children
    )


def iter_leaf_texts(tree: ErrorTree) -> list[str]:
    out: list[str] = []

    def _visit_branch(branch: TreeBranch) -> None:
        for child in branch.children:
            if isinstance(child, TreeLeaf):
                out.append(child.text)
            else:
                _visit_branch(child)

    for root in tree.roots:
        _visit_branch(root)
    return out
