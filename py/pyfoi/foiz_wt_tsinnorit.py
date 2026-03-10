from pycmn import bib_locales as tbn
from pycmn import uni_heb as uh
from pycmn import uni_heb_2 as u2
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pycmn import hebrew_points as hpo
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map
from py_misc import wt_qere


def find_fois_wt(mroge):
    if not tbn.is_poetcant(mroge["mroge-bcvt"]):
        return []
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    #
    word_summaries = sl_map(_get_word_summary, verse)
    features = sum_of_map((_feature, verse), enumerate(word_summaries))
    #
    word_summaries_pre = sl_map(_get_word_summary_pre, verse)
    features_pre = sum_of_map((_feature_pre, verse), enumerate(word_summaries_pre))
    #
    return features + features_pre


def _feature(verse, indexed_word_summary):
    idx, word_summary = indexed_word_summary
    if word_summary is None:
        return []
    assert word_summary in _EXPECTED_WORD_SUMMARIES, word_summary
    foi_path = "tsinnorit", word_summary
    foi_target = verse[idx]
    return [(foi_path, foi_target)]


def _feature_pre(verse, indexed_word_summary):
    idx, word_summary = indexed_word_summary
    if word_summary is None:
        return []
    assert word_summary in _EXPECTED_WORD_SUMMARIES_R, word_summary
    foi_path = "tsinnorit", "pre", word_summary
    foi_target = verse[idx]
    return [(foi_path, foi_target)]


def _across_letters(accents: list[str]):
    return ",".join(accents)


def _across_atoms(accents: list[str]):
    return "-".join(accents)


def _get_word_summary(wordstr):
    tsit_idx = wordstr.find(ha.ZSH_OR_TSIT)
    if tsit_idx != -1:
        start = tsit_idx + 1
        cw_frag = wordstr[start:]
        return _accent_names_in_cw_frag(cw_frag)
    return None


def _get_word_summary_pre(wordstr):
    tsit_idx = wordstr.find(ha.ZSH_OR_TSIT)
    if tsit_idx != -1:
        stop = tsit_idx
        cw_frag = wordstr[:stop]
        out = _accent_names_in_cw_frag(cw_frag)
        return out or None
    return None


def _accent_names_in_cw_frag(cw_frag: str):
    """Return accent names in the given chanted word fragment."""
    atoms = cw_frag.split(hpu.MAQ)
    return _across_atoms(sl_map(_accent_names_in_atom, atoms))


def _accent_names_in_atom(atom: str):
    return _across_letters(uh.accent_names(atom))


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    #
    "מ:פסק": wt_qere.hnd_return_plain_space,
}
#
_EXPECTED_WORD_SUMMARIES = {
    u2.MER,
    u2.MAH,
    #
    _across_letters([u2.MAH, u2.REV]),
    _across_letters([u2.MAH, u2.MTGOSLQ]),
    #
    _across_atoms(["", u2.MER]),
    _across_atoms(["", u2.MAH]),
    #
    _across_atoms(["", _across_letters([u2.MER, u2.MTGOSLQ]), u2.MTGOSLQ]),
}
#
_EXPECTED_WORD_SUMMARIES_R = {
    u2.MTGOSLQ,
    #
    _across_atoms(["", ""]),
    _across_atoms([u2.MTGOSLQ, ""]),
    _across_atoms([u2.MER, ""]),
    _across_atoms([u2.MAH, u2.MTGOSLQ, ""]),
    #
}
