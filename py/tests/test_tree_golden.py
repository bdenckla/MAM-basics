"""Golden test: output contract for tree.print_tree() and tree.tree_to_obj().

Pins the exact byte output for Obadiah 1:2 — the simplest multi-level tree
in the oracle — so any change to indentation, label format, leaf trailing-
space (print_tree), or the JSON node shape (tree_to_obj, issue #20) is caught
immediately.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_tree_golden.py -v
"""

from accgram.tree import add_leaves, make_node, print_tree, tree_to_obj


def _ob_1_2_tree():
    """Hand-built tree for Obadiah 1:2 (from oracle wlc_422_ps_ob_ag.json)."""
    return make_node(
        "silluq_clause",
        make_node(
            "atnax_clause",
            make_node(
                "tipexa_clause",
                add_leaves("tevir_phrase", "merkha", "tevir"),
                add_leaves("tipexa_phrase", "tipexa"),
            ),
            add_leaves("atnax_phrase", "atnax"),
        ),
        make_node(
            "silluq_clause",
            add_leaves("tipexa_phrase", "merkha", "tipexa"),
            add_leaves("silluq_phrase", "silluq"),
        ),
    )


_OB_1_2_EXPECTED_TREE = (
    "0 silluq_clause\n"
    "  1 atnax_clause\n"
    "    2 tipexa_clause\n"
    "      3 tevir_phrase\n"
    "        merkha tevir \n"
    "      3 tipexa_phrase\n"
    "        tipexa \n"
    "    2 atnax_phrase\n"
    "      atnax \n"
    "  1 silluq_clause\n"
    "    2 tipexa_phrase\n"
    "      merkha tipexa \n"
    "    2 silluq_phrase\n"
    "      silluq \n"
)

_OB_1_2_EXPECTED_VERSE = "Obadiah 1:2\n" + _OB_1_2_EXPECTED_TREE


def test_print_tree_ob_1_2():
    """print_tree() output matches the oracle byte-for-byte."""
    got = print_tree(_ob_1_2_tree(), indent_level=0)
    assert got == _OB_1_2_EXPECTED_TREE


def test_verse_output_ob_1_2():
    """Reference line + print_tree() matches the full oracle verse block."""
    ref_line = "Obadiah 1:2"
    verse_output = f"{ref_line}\n" + print_tree(_ob_1_2_tree(), indent_level=0)
    assert verse_output == _OB_1_2_EXPECTED_VERSE


_OB_1_2_EXPECTED_OBJ = {
    "label": "silluq_clause",
    "children": [
        {
            "label": "atnax_clause",
            "children": [
                {
                    "label": "tipexa_clause",
                    "children": [
                        {"label": "tevir_phrase", "leaves": ["merkha", "tevir"]},
                        {"label": "tipexa_phrase", "leaves": ["tipexa"]},
                    ],
                },
                {"label": "atnax_phrase", "leaves": ["atnax"]},
            ],
        },
        {
            "label": "silluq_clause",
            "children": [
                {"label": "tipexa_phrase", "leaves": ["merkha", "tipexa"]},
                {"label": "silluq_phrase", "leaves": ["silluq"]},
            ],
        },
    ],
}


def test_tree_to_obj_ob_1_2():
    """tree_to_obj() nested-binary JSON image matches the pinned shape (issue #20)."""
    assert tree_to_obj(_ob_1_2_tree()) == _OB_1_2_EXPECTED_OBJ


def test_tree_to_obj_none_is_none():
    """A location-only verse (no tree) serializes to None."""
    assert tree_to_obj(None) is None


def test_leaf_names_kept_verbatim():
    """add_leaves() keeps its leaf-names as a tuple (faithful, multi-word safe)."""
    assert add_leaves("test_phrase", "merkha", "tipexa").leaves == ("merkha", "tipexa")
    assert add_leaves("silluq_phrase", "silluq").leaves == ("silluq",)


def test_internal_node_structure():
    """make_node() sets left/right children and has no leaves."""
    left = add_leaves("a_phrase", "foo")
    right = add_leaves("b_phrase", "bar")
    parent = make_node("ab_clause", left, right)
    assert parent.left is left
    assert parent.right is right
    assert parent.label == "ab_clause"
    assert parent.leaves == ()
