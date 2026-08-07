"""Read the leaf texts of a parsed ``ErrorTree``, for tests that assert on leaf order.

Not a test module -- a helper two test modules import, like ``tests/mc_marks.py``, and named
so pytest's ``test_*.py`` / ``*_test.py`` patterns do not collect it.

This lived in ``accgram/ob_tree_parse.py`` as a public function until 2026-08-07, when a sweep
for production functions whose only callers are tests found it had none of its own.  Nothing
in the program reads a tree this way; only ``test_almost_errors`` and ``test_poetic_oddballs``
do, and they use it to say what a parse produced rather than to test the walker itself.
"""

from accgram.ob_tree_parse import ErrorTree, TreeBranch, TreeLeaf


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
