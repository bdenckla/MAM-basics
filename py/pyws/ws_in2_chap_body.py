""" Exports reorg """

from dataclasses import dataclass
from pyws import ws_in2_tree_node as etn
from pycmn import hebrew_verse_numerals as hvn
from pycmn import my_utils


def reorg(chap_body: list):
    """Reorganize the chapter body into ExtendedVerse objects."""
    state = _ChapterBodyState()
    for chap_body_el in chap_body:
        _process_cbe(state, chap_body_el)
    state.assert_is_initial()
    nodes = list(map(_to_node, state.verse_accum))
    return {node.name: node for node in nodes}


@dataclass
class _ExtendedVerse:
    """Verse prefix, location, and body."""

    prefix: list  # corresponds to column C
    location: list = None  # corresponds to column D
    body: list = None  # corresponds to column E

    def __init__(self):
        self.prefix = []


@dataclass
class _ChapterBodyState:
    verse_accum: list[_ExtendedVerse]
    cur_verse: _ExtendedVerse
    name: str = "prefix-star-siman-0"

    def __init__(self):
        self.verse_accum = []
        self.cur_verse = _ExtendedVerse()

    def assert_is_initial(self):
        """Are we in an initial state (other than verse_accum)?"""
        assert self.name == "prefix-star-siman-0", self.name
        assert self.cur_verse == _ExtendedVerse(), self.cur_verse


def _to_node(verse: _ExtendedVerse):
    node = etn.TreeNode(verse.body.name)
    node.named_children = {
        "prefix": etn.TreeNode(children=verse.prefix),
        "location": verse.location,
        "verse-body": verse.body,
        # We qualify with "verse" because there is also "chapter-body"
    }
    return node


def _process_cbe(state: _ChapterBodyState, chap_body_el):
    if state.name in ("prefix-star-siman-0", "prefix-star-siman-n"):
        if _is_siman(chap_body_el):
            cbe_children = chap_body_el.children
            state.cur_verse.location = my_utils.first_and_only(cbe_children)
            state.name = "verse-body-expected"
            return
        state.cur_verse.prefix.append(chap_body_el)
        state.name = "prefix-star-siman-n"
        return
    if state.name == "verse-body-expected":
        assert _is_verse_body(chap_body_el)
        state.cur_verse.body = chap_body_el
        state.verse_accum.append(state.cur_verse)
        state.cur_verse = _ExtendedVerse()
        state.name = "prefix-star-siman-0"


def _is_siman(obj):
    if not isinstance(obj, etn.TreeNode):
        return False
    return obj.name == "סימן"


def _is_verse_body(obj):
    if not isinstance(obj, etn.TreeNode):
        return False
    return obj.name in hvn.STR_TO_INT_DIC
