from dataclasses import dataclass
from pyws import ws_in2_serialize as serialize
from pyws import ws_in2_tree_node as etn
from pyws import ws_in2_chap_body as chap_body
from pycmn import ws_tmpl1 as wtp1
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import bib_locales as tbn
from pycmn import hebrew_verse_numerals as hvn


def get_chap_in_fmt_2(parsed_lines, bacq=None):
    chapter_node = _convert_chapter(parsed_lines)
    if bacq:
        _check_chapter_node(bacq, chapter_node)
    return serialize.prep_children(chapter_node)


def _check_chapter_node(bac, node: etn.TreeNode):
    _check_noinclude_header(bac, node.named_children["ws-chap-noinclude-header"])
    _check_category(bac, node.named_children["ws-chap-category"])


_BACS_TO_SKIP = [
    (tbn.BK_EXODUS, "טו"),
    (tbn.BK_EXODUS, "כ"),
    (tbn.BK_DEUTER, "ה"),
    (tbn.BK_DEUTER, "לב"),
    (tbn.BK_JOSHUA, "יב"),
    (tbn.BK_JUDGES, "ה"),
    (tbn.BK_SND_SAM, "כב"),
    (tbn.BK_QOHELET, "ג"),
    (tbn.BK_ESTHER, "ט"),
    (tbn.BK_FST_CHR, "טז"),
]


def _check_noinclude_header(bac, node: etn.TreeNode):
    if bac in _BACS_TO_SKIP:
        return
    children_wop = _rmp(node.children)
    tels_for_children = list(map(wtp1.template_elements, children_wop))
    bkid, he_chnu = bac
    he_bk39na = mbkn_a_sbkn.he_bk39_name(bkid)
    expected_tels_for_child0 = [["ניווט טעמים"], [he_bk39na], [he_chnu]]
    assert tels_for_children[0] == expected_tels_for_child0
    assert tels_for_children[1] == [["טעמי המקרא באינטרנט"]]
    assert tels_for_children[2] == [["מ:שוליים"], ["5"]]
    assert tels_for_children[3] == [["מ:טעמי המקרא"]]


def _check_category(bac, node: etn.TreeNode):
    bkid, he_chnu = bac
    he_bk39na = mbkn_a_sbkn.he_bk39_name(bkid)
    expected = f"[[קטגוריה:{he_bk39na} {he_chnu}]]"
    assert node == expected


@dataclass
class _WspState:  # Wikisource parser state
    stack_of_start_strs: list
    stack_of_nodes: list

    def __init__(self, node: etn.TreeNode):
        self.stack_of_start_strs = []
        self.stack_of_nodes = [node]


def _is_noinclude(obj):
    if not isinstance(obj, etn.TreeNode):
        return False
    return obj.name == "noinclude"


def _is_chapter_body(obj):
    if not isinstance(obj, etn.TreeNode):
        return False
    return obj.name.startswith("פרק" + " ")


def _is_good_ending(obj):
    if not isinstance(obj, etn.TreeNode):
        return False
    return obj.name == "סיום בטוב"


def _is_category(obj):
    if not isinstance(obj, str):
        return False
    return obj.startswith("[[" + "קטגוריה" + ":")


_CCNRS = {  # chapter child name records
    0: (0, _is_noinclude, "ws-chap-noinclude-header"),
    1: (1, _is_chapter_body, "ws-chap-body"),
    2: (2, _is_good_ending, "ws-chap-good-ending"),
    -2: (-2, _is_noinclude, "ws-chap-noinclude-footer"),
    -1: (-1, _is_category, "ws-chap-category"),
}


def _is_not_pilcrow(obj):
    return obj != "¶"


def _rmp(seq):  # remove pilcrows
    return list(filter(_is_not_pilcrow, seq))


def _add_names_to_chap_children(io_chap_node: etn.TreeNode):
    # wop: without pilcrows
    children_wop = _rmp(io_chap_node.children)
    _add_named_chap_child(children_wop, io_chap_node, _CCNRS[0])
    _add_named_chap_child(children_wop, io_chap_node, _CCNRS[1])
    if len(children_wop) > 4:
        assert len(children_wop) == 5
        _add_named_chap_child(children_wop, io_chap_node, _CCNRS[2])
    _add_named_chap_child(children_wop, io_chap_node, _CCNRS[-2])
    _add_named_chap_child(children_wop, io_chap_node, _CCNRS[-1])


def _add_named_chap_child(children_wop, io_chap_node: etn.TreeNode, ccnr):
    # wop: without pilcrows
    # Example value for ccrn (idx, is_xxx, name):
    # (0, _is_noinclude, "ws-chap-noinclude-header")
    idx, is_xxx, name = ccnr
    child = children_wop[idx]
    assert is_xxx(child)  # _is_noinclude, _is_chapter_body, etc.
    io_chap_node.named_children[name] = child


def _convert_chapter(parsed_lines):
    chapter_node = etn.TreeNode()
    state = _WspState(chapter_node)
    # Can we get rid of this (nested) "for" loop?
    for line in parsed_lines:
        for line_el in line:
            assert line_el != "¶"
            _process_line_el(state, line_el)
        _process_line_el(state, "¶")
    _add_names_to_chap_children(chapter_node)
    ch_bod = chapter_node.named_children["ws-chap-body"]
    ch_bod.named_children = chap_body.reorg(ch_bod.children)
    return chapter_node


def _name_of_abtag_section_starting(obj):
    return _name_of_abtag_section_stenning("start", obj)


def _name_of_abtag_section_ending(obj):
    return _name_of_abtag_section_stenning("end", obj)


_STRADDLERS = (
    # These are sections that are "undeserving" because they straddle
    # other sections. Straddling means creating overlapping
    # sections. Normally we expect sections to be either sequential
    # or nested, not overlapping.
    "שורה 1 לפני השיר",
    "שורה 5 לפני השיר",
)
_VERSE_LEVEL_SECTIONS = (
    # These are sections that only exist at verse level.
    # To maintain compatibility with "format 2",
    # we consider them "undeserving".
    "הפסוק בלי הערה",
    "פסוק ו לפני צורת השיר",
    "פסוק י אחרי צורת השיר",
    "פסוק ט אחרי צורת השיר",
    "שורה 2 לפני השיר",
    "שורה 3 לפני השיר",
    "שורה 4 לפני השיר",
    "שורה 6 לפני השיר",
)
_NAMES_OF_UNDESERVING_SECTIONS = _STRADDLERS + _VERSE_LEVEL_SECTIONS
# "Undeserving" means "not deserving of promotion to become a real section".
# I.e., left as plain old start & stop abtags.
_NOINCLUDES = {"start": "noinclude", "end": "/noinclude"}
_QETAS = {"start": "קטע התחלה" + "=", "end": "קטע סוף" + "="}
_KNOWN_START_STRS = {"noinclude", "סימן", "סיום בטוב"}
_HEBREW_VERSE_NUMERALS = set(hvn.STR_TO_INT_DIC.keys())
_CHAPTER_START_STRS = {f"פרק {n}" for n in hvn.STR_TO_INT_DIC.keys()}


def _name_of_abtag_section_stenning(sten: str, obj):  # sten: 'start' or 'end'
    if not isinstance(obj, dict):
        return None
    if list(obj.keys()) != ["custom_tag"]:
        return None
    val = obj["custom_tag"]
    if val == _NOINCLUDES[sten]:
        return "noinclude"
    if not val.startswith(_QETAS[sten]):
        return None
    assert val.endswith("/")
    out = val[len(_QETAS[sten]) : -1]
    # e.g. out == 'פרק א' from val == 'קטע התחלה=פרק א/'
    if out in _NAMES_OF_UNDESERVING_SECTIONS:
        return None
    return out


def _process_line_el(state: _WspState, line_el):
    if start_str := _name_of_abtag_section_starting(line_el):
        assert _start_str_okay(start_str), start_str
        state.stack_of_start_strs.append(start_str)
        new_node = etn.TreeNode(start_str)
        state.stack_of_nodes[-1].children.append(new_node)
        state.stack_of_nodes.append(new_node)
        return
    if end_str := _name_of_abtag_section_ending(line_el):
        start_str = state.stack_of_start_strs.pop()
        assert end_str == start_str
        state.stack_of_nodes.pop()
        return
    state.stack_of_nodes[-1].children.append(line_el)


def _start_str_okay(start_str):
    if start_str in _HEBREW_VERSE_NUMERALS:
        return True
    if start_str in _CHAPTER_START_STRS:
        return True
    return start_str in _KNOWN_START_STRS
