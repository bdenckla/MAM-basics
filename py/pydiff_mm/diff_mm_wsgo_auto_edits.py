"""Exports get_srrps, self_test"""

import re
import difflib
from pyws import ws_unparse


def get_srrps(ws_wtseq, go_wtseq):
    """Get diffs suitable for srrp (search and replace) (auto-edits)"""
    # if (ws_wtseq, go_wtseq) == (["__"], tuple()):
    #     return [{"ws": ["__"], "go": [""]}]
    ws_wtseq_str = ws_unparse.unparse(ws_wtseq)
    go_wtseq_str = ws_unparse.unparse(go_wtseq)
    return _get_diffs(ws_wtseq_str, go_wtseq_str)


def self_test():
    """Perform a very basic self-test."""
    ws_wtseq_str = "a b c d e"
    go_wtseq_str = "a b c d e".replace("b ", "").replace("d ", "d + ")
    # Below, we rely on the assert in _get_diffs to do our testing
    _get_diffs(ws_wtseq_str, go_wtseq_str)


def _get_diffs(ws_wtseq_str, go_wtseq_str):
    ws_segs = _make_segments(ws_wtseq_str)
    go_segs = _make_segments(go_wtseq_str)
    seqmat = difflib.SequenceMatcher(a=ws_segs, b=go_segs, autojunk=False)
    opcodes = seqmat.get_opcodes()
    edits = [_op_to_edit(op, ws_segs, go_segs) for op in opcodes]
    merged_edits = _merge_edits(go_wtseq_str, edits)
    replaces = tuple(filter(_is_replace, merged_edits))
    if ws_wtseq_str == _apply(replaces, go_wtseq_str):
        return tuple(map(_strip_tag, replaces))
    print("Reverting to whole Wikitext sequence as diff")
    the_one_diff = {"ws": [ws_wtseq_str], "go": [go_wtseq_str]}
    return (the_one_diff,)


def _apply(replaces, go_wtseq_str):
    work_str = go_wtseq_str
    for replace in replaces:
        work_str = work_str.replace("".join(replace["go"]), "".join(replace["ws"]))
    return work_str


def _op_to_edit(seqmat_opcode, ws_segs, go_segs):
    tag, as0, as1, bs0, bs1 = seqmat_opcode
    simple_tag = "replace" if tag != "equal" else "equal"
    # Insert and delete are just replaces where one or the
    # other side is empty. For our purposes, it is easier
    # to tag inserts and deletes as replaces.
    return {"ws": ws_segs[as0:as1], "go": go_segs[bs0:bs1], "tag": simple_tag}


def _merge_edits(go_wtseq_str, edits):
    new_edits = []
    for edit in edits:
        if edit["tag"] == "equal":
            new_edits.append(edit)
        else:
            new_edits = _append_or_merge(go_wtseq_str, new_edits, edit)
    return new_edits


def _append_or_merge(go_wtseq_str, edits, replace):
    # If the search string exists and is unique, append this replace to
    # the list of edits.
    # Otherwise, merge this replace into the tail of the list of edits.
    #
    # (The search string does not exist for an insert.)
    # (A non-existent search string is indicated by an empty segment list.)
    #
    # We are replacing the go string with the ws one, i.e.,
    # we are framing the edit as an instruction to search for replace['go']
    # and replace it with replace['ws'].
    # So the search string is replace['go'].
    #
    # TODO: what should we do about search strings that become non-unique
    # as a result of a previous replace?
    #
    rgo = replace["go"]
    if rgo and -1 == _find_2nd(go_wtseq_str, "".join(rgo)):
        return edits + [replace]
    if edits == []:
        # if there's no tail to merge onto, bail
        # (returning an empty edit list will cause a bail at a higher level)
        # (See "Reverting to whole Wikitext sequence as diff".)
        return []
    new_edits = _merge(edits, replace)
    return _append_or_merge(go_wtseq_str, new_edits[:-1], new_edits[-1])


def _merge(edits, replace):
    neg1 = edits[-1]
    if neg1["tag"] == "replace":
        new_neg1_ws = []
        new_neg1_go = []
        new_ws = neg1["ws"] + replace["ws"]
        new_go = neg1["go"] + replace["go"]
    else:
        new_neg1_ws = neg1["ws"][:-1]
        new_neg1_go = neg1["go"][:-1]
        new_ws = neg1["ws"][-1:] + replace["ws"]
        new_go = neg1["go"][-1:] + replace["go"]
    new_neg1 = {"ws": new_neg1_ws, "go": new_neg1_go, "tag": neg1["tag"]}
    new_replace = {"ws": new_ws, "go": new_go, "tag": "replace"}
    if not new_neg1["ws"] and not new_neg1["go"]:
        return edits[:-1] + [new_replace]
    assert new_neg1["ws"] and new_neg1["go"]
    return edits[:-1] + [new_neg1, new_replace]


def _find_2nd(haystack, needle):
    idx_of_1st_instance = haystack.find(needle)
    assert idx_of_1st_instance != -1
    return haystack.find(needle, idx_of_1st_instance + len(needle))


def _is_replace(edit_record):
    return edit_record["tag"] == "replace"


def _strip_tag(edit_record):
    assert edit_record["tag"] == "replace"
    new_er = dict(edit_record)
    del new_er["tag"]
    assert tuple(new_er.keys()) == ("ws", "go")
    return new_er


def _make_segments(string):
    # This is different than plain string.split(' ')
    # because the separators (spaces) are returned as well,
    # interspersed with the words (runs of non-spaces).
    return re.split(r"([^ ]+)", string)
