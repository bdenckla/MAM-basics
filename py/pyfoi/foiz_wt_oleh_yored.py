import re
from pycmn import bib_locales as tbn
from pycmn import uni_heb as uh
from pycmn import uni_heb_2 as u2
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map
from pyfoi import regexp_helpers as rh
from py_misc import wt_qere


def find_fois_wt(mroge):
    if not tbn.is_poetcant(mroge["mroge-bcvt"]):
        return []
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    run_els = sl_map(_get_run_el_from_word, verse)
    runsdic = _runsdic(run_els)
    features = sum_of_map((_feature, verse), runsdic.items())
    return features


def _runsdic(run_els):
    # run_els looks something like this:
    # [None, 'a', None, 'b', 'c', None, 'd', None]
    accum = []
    last = None
    for idx, run_el in enumerate(run_els):
        if run_el is not None:
            if last is None:
                accum.append([])
            accum[-1].append((idx, run_el))
        last = run_el
    # accum looks something like this:
    # [
    #    [(1, 'a')],
    #    [(3, 'b'), (4, 'c')],
    #    [(6, 'd')],
    # ]
    simplified = dict(sl_map(_simplify, accum))
    # simplified looks something like this:
    # {
    #    1: ['a'],
    #    3: ['b', 'c'],
    #    6: ['d']
    # }
    return simplified


def _simplify(irps):  # irp: idx/run_el pair; irps: many irp
    # turns [(3, 'a'), (4, 'b')]
    # into this: (3, ['a', 'b'])
    return irps[0][0], list(pair[1] for pair in irps)


def _feature(verse, runsdic_item):
    idx, run = runsdic_item
    tuprun = tuple(run)
    assert tuprun in _RUN_TO_FEATURE, tuprun
    feat = _RUN_TO_FEATURE[tuprun]
    if feat is None:
        return []
    start = feat[0]
    stop = len(run) + feat[1]
    foi_target = " ".join(verse[idx + start : idx + stop])
    feature_name = " ".join(run[start:stop])
    foi_path = "oleh-yored", feature_name
    return [(foi_path, foi_target)]


def _sharing_letter(accents: list[str]):
    return "+".join(accents)


def _across_letters(accents: list[str]):
    return ",".join(accents)


def _across_atoms(accents: list[str]):
    return "-".join(accents)


def _clus_patt_for_mark(mark):
    return rh.LETT + rh.ZM_NL + mark + rh.ZM_NL


_OLE_CLUS_PATT = _clus_patt_for_mark(ha.OLE)
_MER_CLUS_PATT = _clus_patt_for_mark(ha.MER)


def _get_run_el_from_word(wordstr):
    ole_match = re.search(_OLE_CLUS_PATT, wordstr)
    if ole_match:
        start = ole_match.start()
        cw_frag = wordstr[start:]
        return _accent_names_in_cw_frag(cw_frag)
    if re.search(_KILLERS_PATT, wordstr):
        # "Killers" are accents that cause us to ignore an ha.MER
        # on their word.
        # I.e. we take the presence of a "killer" to mean that
        # any ha.MER on its word is a merkha, not a yored.
        return None
    mer_match = re.search(_MER_CLUS_PATT, wordstr)
    if mer_match:
        end = mer_match.end()
        cw_frag = wordstr[:end]
        return _accent_names_in_cw_frag(cw_frag)
    return None


def _accent_names_in_cw_frag(cw_frag: str):
    """Return accent names in the given chanted word fragment."""
    cw_no_mos = uh.rm_mtgoslq(cw_frag)
    atoms = cw_no_mos.split(hpu.MAQ)
    return _across_atoms(sl_map(_accent_names_in_atom_frag, atoms))


def _accent_names_in_atom_frag(atom: str):
    clusters = re.findall(rh.LETT + rh.ZM_NL, atom)
    anic = sl_map(_accent_names_in_cluster, clusters)
    anic_filtered = list(filter(None, anic))
    return _across_letters(anic_filtered)


def _accent_names_in_cluster(cluster: str):
    accent_names = uh.accent_names(cluster)
    return _sharing_letter(accent_names)


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    #
    "מ:פסק": wt_qere.hnd_return_plain_space,
}
_SC_MER_OLE = _sharing_letter([u2.MER, u2.OLE])
_SA_OLE_MER = _across_letters([u2.OLE, u2.MER])
_AM_OLE_MER = _across_atoms([u2.OLE, u2.MER])
_AM_E_MER = _across_atoms(["", u2.MER])
_AM_E_E_MER = _across_atoms(["", "", u2.MER])
_RUN_TO_FEATURE = {
    (_SC_MER_OLE,): (0, 0),
    (_SC_MER_OLE, u2.MER): (0, -1),
    (_SC_MER_OLE, _AM_E_MER): (0, -1),
    #
    (_SA_OLE_MER,): (0, 0),
    (_AM_OLE_MER,): (0, 0),
    #
    (_SA_OLE_MER, u2.MER): (0, -1),
    (_AM_OLE_MER, u2.MER): (0, -1),
    #
    (_SA_OLE_MER, _AM_E_MER): (0, -1),
    (_AM_OLE_MER, _AM_E_MER): (0, -1),
    #
    (_SA_OLE_MER, _AM_E_E_MER): (0, -1),
    (_SA_OLE_MER, u2.MER, u2.MER): (0, -2),
    #
    (u2.MER, _SA_OLE_MER): (1, 0),
    (u2.MER, _AM_OLE_MER): (1, 0),
    #
    (u2.MER, _SA_OLE_MER, u2.MER): (1, -1),
    (u2.MER, u2.OLE, u2.MER): (1, 0),
    #
    #
    (u2.OLE, u2.MER): (0, 0),
    (u2.OLE, u2.MER, u2.MER): (0, -1),
    (u2.OLE, u2.MER, _AM_E_MER): (0, -1),
    (u2.MER, u2.OLE, u2.MER): (1, 0),
    #
    (u2.MER,): None,
    (_AM_E_MER,): None,
    (_AM_E_E_MER,): None,
    (u2.MER, u2.MER): None,
    (_AM_E_MER, _AM_E_MER): None,
    (u2.MER, _AM_E_MER): None,
    (_AM_E_MER, u2.MER): None,
}
_KILLERS = ha.ZSH_OR_TSIT, ha.GER_M, ha.DEX, ha.MAH
_KILLERS_PATT = "[" + "".join(_KILLERS) + "]"
