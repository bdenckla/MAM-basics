""" Exports prep_children """

from pyws import ws_in2_tree_node as etn
from pycmn import ws_tmpl1 as wtp1
from pycmn.my_utils import dv_map


def prep_children(node: etn.TreeNode):
    """
    Prepare the children of the node for serialization by converting them
    to consist only of serializable (JSON-dumpable) structures, (dicts, etc.)
    """
    if nach := node.named_children:
        return dv_map(_prep_nl_value, nach)
    return list(map(_prep_nl, node.children))


def _prep_nl(node_or_leaf):  # nl: node or leaf
    assert not isinstance(node_or_leaf, etn.TreeNode)
    return wtp1.simplify_wtel(node_or_leaf)


def _prep_nl_value(node_or_leaf):  # nl: node or leaf
    if isinstance(node_or_leaf, etn.TreeNode):
        return prep_children(node_or_leaf)
    return wtp1.simplify_wtel(node_or_leaf)
