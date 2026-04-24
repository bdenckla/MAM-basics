from pycmn import str_defs as sd
from pycmn import bib_locales as tbn
from pycmn import hebrew_punctuation as hpu
from py_misc import wt_qere
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map


def find_fois_wt(mroge):
    bcvt = mroge["mroge-bcvt"]
    if tbn.has_dualcant(bcvt):
        features_a = _find_in_one_cant(_HANDLERS_A, "lower", mroge)
        features_b = _find_in_one_cant(_HANDLERS_B, "upper", mroge)
        return features_a + features_b
    features = _find_in_one_cant(_HANDLERS, None, mroge)
    return features


def _cant_qualify(qual, features):
    if not qual:
        return features
    return sl_map((_cant_qualify_one, qual), features)


def _cant_qualify_one(qual, feature):
    foi_path, foi_target = feature
    new_foi_path = foi_path[0], "dualcant", qual, *foi_path[1:]
    return new_foi_path, foi_target


def _find_in_one_cant(handlers, qual_str, mroge):
    verse = wt_qere.get_verse_as_wordstrs(handlers, mroge)
    run_els = sl_map(_get_run_el_from_word, verse)
    runsdic = _runsdic(run_els)
    features = sum_of_map((_feature, verse), runsdic.items())
    features = _cant_qualify(qual_str, features)
    return features


def _runsdic(run_els):
    accum = []
    last = None
    for idx, run_el in enumerate(run_els):
        if run_el is not None:
            if last is None:
                accum.append([])
            accum[-1].append((idx, run_el))
        last = run_el
    simplified = dict(sl_map(_simplify, accum))
    return simplified


def _simplify(irps):  # irp: idx/run_el pair; irps: many irp
    return irps[0][0], list(pair[1] for pair in irps)


_FEATURE_PATH = {
    ("paseq",): ("lp-paseq",),
    ("paseq", "paseq"): ("lp-paseq×2",),
    ("paseq", "paseq", "paseq"): ("lp-paseq×3",),
    ("legarmeih",): ("lp-legarmeih",),
    ("legarmeih", "legarmeih"): ("lp-legarmeih×2",),
    ("legarmeih", "paseq"): ("lp-legarmeih", "paseq-after"),
    ("paseq", "legarmeih"): ("lp-paseq", "legarmeih-after"),
}
_PASOLEG = {hpu.PASOLEG: "legarmeih", sd.DOUB_VERT_LINE: "paseq"}


def _feature(verse, runsdic_item):
    idx, run = runsdic_item
    if feat := _FEATURE_PATH[tuple(run)]:
        foi_path = "pasoleg-2", *feat
        foi_target = " ".join(verse[idx : idx + len(run)])
        return [(foi_path, foi_target)]
    return []


def _get_run_el_from_word(wordstr):
    return _PASOLEG.get(wordstr[-1])


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    #
    "מ:פסק": wt_qere.hnd_return_doub_vert_line_plus_space,
}
_HANDLERS_A = {
    **_HANDLERS,
    "מ:כפול": wt_qere.hnd_recurse_on_param_alef,
}
_HANDLERS_B = {
    **_HANDLERS,
    "מ:כפול": wt_qere.hnd_recurse_on_param_bet,
}
