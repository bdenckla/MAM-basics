import re
from pycmn.my_utils import sl_map
from pycmn import uni_heb as uh
from pycmn import uni_heb_2 as u2
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pyfoi import regexp_helpers as rh


def acc_node_from_cword(is_poca, cword: str):
    """Return accent names in the given chanted word."""
    split_result = re.split(_BOG_MAQ, cword)
    atoms = split_result[::2]  # skip maqaf positions
    bog_maqs = split_result[1::2]
    assert len(bog_maqs) == len(atoms) - 1
    anias = sl_map(_accent_names_in_atom, atoms)
    anias_u = _disambiguate(is_poca, cword, anias)
    assert len(anias_u) != 0
    if len(anias_u) == 1:
        return anias_u[0]
    return across_atoms(anias_u, bog_maqs)


_BOG_MAQ = rh.par(rh.sqb(hpu.MAQ + hpu.NU_GMAQ))  # black or gray maqaf


def _disambiguate(is_poca, cword: str, anias: list[dict]):
    if cword[-1] == hpu.SOPA:
        out = _slq(anias)
    elif cword[-1] == hpu.PASOLEG:
        out = _azl_leg(anias)
    elif ha.GER_M in cword:
        out = _rev_irm(anias)
    else:
        out = anias
    out = _mtg(out)
    out = _tartip(is_poca, out)
    out = _azlqom(is_poca, out)
    return out


def _slq(nodes: list[dict]):
    return nodes[:-1] + [_slq_3(nodes[-1])]


def _slq_3(node: dict):
    sub_nodes, accent_str = _node_get(node)
    if sub_nodes:
        return _nsn(node, _slq(sub_nodes))
    if accent_str == u2.MTGOSLQ:
        return _LEAF_NU_SLQ
    assert accent_str
    return node


def _rev_irm(nodes: list[dict]):
    return _nu_acc_a_3((u2.REV, _LEAF_NU_REV_IRM), nodes)


def _azl_leg(nodes: list[dict]):
    return _nu_acc_a_3((u2.QOM, _LEAF_NU_AZL_LEG), nodes)


def _azl(nodes: list[dict]):
    return _nu_acc_a_3((u2.QOM, _LEAF_NU_AZL), nodes)


def _mtg(nodes: list[dict]):
    return _nu_acc_a_3((u2.MTGOSLQ, _LEAF_NU_MTG), nodes)


def _tartip(is_poca, nodes: list[dict]):
    leaf_nu_yyy = _LEAF_NU_TAR if is_poca else _LEAF_NU_TIP
    return _nu_acc_a_3((u2.TIP, leaf_nu_yyy), nodes)


def _azlqom(is_poca, nodes: list[dict]):
    leaf_nu_yyy = _LEAF_NU_AZL if is_poca else _LEAF_NU_QOM
    return _nu_acc_a_3((u2.QOM, leaf_nu_yyy), nodes)


def _nu_acc_a_3(remaps, nodes: list[dict]):
    return sl_map((_nu_acc_a_4, remaps), nodes)


def _nu_acc_a_4(remap, node):
    sub_nodes, accent_str = _node_get(node)
    if sub_nodes:
        return _nsn(node, _nu_acc_a_3(remap, sub_nodes))
    if accent_str == remap[0]:
        return remap[1]
    return node


def _node_get(node):
    if sub_nodes := node.get("acc-node-sub-nodes"):
        return sub_nodes, None
    if accent_str := node.get("acc-node-acc-str"):
        assert node["acc-node-type"] == "ant-leaf-acc"
        return None, accent_str
    assert node["acc-node-type"] == "ant-leaf-null"
    return None, None


def _accent_names_in_atom(atom: str):
    clusters = re.findall(rh.LETT + rh.ZM_NL, atom)
    anic = sl_map(_accent_names_in_cluster, clusters)
    anic_filtered = list(filter(None, anic))
    if len(anic_filtered) == 0:
        return _mk_acc_tree_leaf_null()
    if len(anic_filtered) == 1:
        return anic_filtered[0]
    return across_letters(anic_filtered)


def _accent_names_in_cluster(cluster: str):
    accent_names = uh.accent_names(cluster)
    if len(accent_names) == 0:
        return None
    if len(accent_names) == 1:
        return mk_acc_tree_leaf_acc(accent_names[0])
    return mk_acc_seq_sharing_letter(accent_names)


def str_from_acc_node(node):
    sub_nodes, accent_str = _node_get(node)
    if sub_nodes:
        recursion_result = sl_map(str_from_acc_node, sub_nodes)
        ant = node["acc-node-type"]
        return _JOINER[ant].join(recursion_result)
    if accent_str:
        return accent_str
    return ""


def mk_acc_seq_sharing_letter(flex_contents: list):
    return _mk_acc_tree_branch("ant-branch-sharing-letter", flex_contents)


def across_letters(flex_contents: list):
    # loa: letters of atom
    return _mk_acc_tree_branch("ant-branch-across-loa", flex_contents)


def across_atoms(flex_contents: list, bog_maqs: list):
    # aoc: atoms of compound
    if len(flex_contents) == 2:
        rhs = flex_contents[1]
    else:
        rhs = across_atoms(flex_contents[1:], bog_maqs[1:])
    ant = _ANT_BRANCH_ACROSS_AOC[bog_maqs[0]]
    return _mk_acc_tree_branch(ant, [flex_contents[0], rhs])


_ANT_BRANCH_ACROSS_AOC = {
    hpu.MAQ: "ant-branch-across-aoc-black",
    hpu.NU_GMAQ: "ant-branch-across-aoc-gray",
}


def mk_acc_tree_leaf_acc(accent_str: str):
    assert accent_str != ""
    return {
        "acc-node-type": "ant-leaf-acc",
        "acc-node-acc-str": accent_str,
    }


def _mk_acc_tree_leaf_null():
    return {
        "acc-node-type": "ant-leaf-null",
    }


def _mk_acc_tree_branch(ant: str, sub_node_inputs: list):
    assert len(sub_node_inputs) > 1
    return {
        "acc-node-type": ant,
        "acc-node-sub-nodes": sl_map(_mk_acc_tree_node, sub_node_inputs),
    }


def _nsn(node: dict, new_sub_nodes: list):
    """Make a new node like the given one but with new sub-nodes."""
    return _mk_acc_tree_branch(node["acc-node-type"], new_sub_nodes)


def _mk_acc_tree_node(node_input):
    if node_input is None:
        return _mk_acc_tree_leaf_null()
    if isinstance(node_input, str):
        return mk_acc_tree_leaf_acc(node_input)
    assert "acc-node-type" in node_input
    return node_input


_LEAF_NU_SLQ = mk_acc_tree_leaf_acc(u2.NU_SLQ)
_LEAF_NU_MTG = mk_acc_tree_leaf_acc(u2.NU_MTG)
_LEAF_NU_AZL_LEG = mk_acc_tree_leaf_acc(u2.NU_AZL_LEG)
_LEAF_NU_AZL = mk_acc_tree_leaf_acc(u2.NU_AZL)
_LEAF_NU_QOM = mk_acc_tree_leaf_acc(u2.NU_QOM)
_LEAF_NU_TAR = mk_acc_tree_leaf_acc(u2.NU_TAR)
_LEAF_NU_TIP = mk_acc_tree_leaf_acc(u2.NU_TIP)
_LEAF_NU_REV_IRM = mk_acc_tree_leaf_acc(u2.NU_REV_IRM)
_JOINER = {
    "ant-branch-sharing-letter": "+",
    "ant-branch-across-loa": ",",
    "ant-branch-across-aoc-black": "-",
    "ant-branch-across-aoc-gray": hpu.NU_GMAQ,
}
