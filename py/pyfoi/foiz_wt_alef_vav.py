from functools import reduce
from pycmn import template_names as tmpln
from pyfoi import foi_wikitext_helpers as fwh
from pyfoi import foi_alef_and_vav_helpers as avva
from pyfoi import foi_struct as fct
from pycmn.my_utils import sl_map


def find_fois_wt(mroge):
    """Find "dual mater lectionis" alef-vav and vav-alef."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _find_fois_in_string(stack, string):
    if stack and stack[-1] == "doc-part-n":
        return []
    words = string.split(" ")
    fois = reduce(_add_fois_in_str, words, [])
    qual_fois = sl_map((_qualify, stack), fois)
    return qual_fois


def _add_fois_in_str(accum, word):
    fois_in_str = avva.find_fois_in_str(word)
    return accum + fois_in_str


def _qualify(stack, unqual_foi):
    if len(unqual_foi) == 3:
        foi_path, unqual_target, found_qualifier = unqual_foi
    else:
        foi_path, unqual_target = unqual_foi
        found_qualifier = {}
    stack_summary = _stack_summary(stack)
    qualifier = {"stack_str": stack_summary}
    qualifier.update(found_qualifier)
    qual_target = fct.make_qtarget(unqual_target, qualifier)
    return foi_path, qual_target


def _stack_summary(stack):
    if stack in _STACK_SUMMARIES:
        return fwh.stack_summary(_STACK_SUMMARIES, stack)
    if stack and stack[-1] in _NOTE_STACK_PARTS:
        return stack[-1]
    return None


_FOILERS = {
    str: _find_fois_in_string,
    tmpln.SLH_WORD: fwh.find_fois_in_slh_word_arg_1,
    "נוסח": fwh.label_args_of_doc,
    tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.ignore,
}
_NOTE_STACK_PARTS = {"doc-part-n", "scrdfftar-note", tmpln.SLH_WORD}
_STACK_SUMMARIES = {
    tuple(): None,
    ("doc-target",): None,
    ('כו"ק',): None,
    ('קו"כ',): None,
    ("doc-target", 'קו"כ'): None,
    ("doc-target", 'כו"ק'): None,
    ("מ:דחי",): None,
    #
    ("doc-target", "scrdfftar-note"): -1,
    ("doc-part-n",): -1,
    ("doc-target", tmpln.SLH_WORD): -1,
}
