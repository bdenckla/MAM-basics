from pycmn import ws_tmpl2 as wtp
from pycmn import str_defs as sd
from pycmn import bib_locales as tbn
from py_misc import wt_qere
from pycmn import hebrew_punctuation as hpu
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
    wtels = wt_qere.get_verse(handlers, mroge)
    run_els = sl_map(_get_run_el_from_wtel, wtels)
    runsdic = _runsdic(run_els)
    renverse = _render_wtseq(wtels)
    features = sum_of_map((_feature, renverse), runsdic.items())
    features = _cant_qualify(qual_str, features)
    return features


def _render_wtseq(wtseq):
    return sl_map(_render_wtel, wtseq)


def _render_wtel(wtel):
    if isinstance(wtel, str):
        return wtel
    renderer = _RENDERERS[wtp.template_name(wtel)]
    return renderer(wtel)


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


def _feature(verse, runsdic_item):
    idx, run = runsdic_item
    if foi_path := _FEATURES[tuple(run)]:
        foi_target = "".join(verse[idx : idx + len(run)])
        if foi_target.startswith(sd.NBSP + sd.DOUB_VERT_LINE):
            foi_target = foi_target[1:]
        return [(foi_path, foi_target)]
    return []


def _get_run_el_from_wtel(wtel):
    if isinstance(wtel, str):
        return wtel if wtel in _INTERESTING_STRS else None
    return _TMPL_NAME_REMAPS[wtp.template_name(wtel)]


def _paren(seq):
    return "".join(["(", *seq, ")"])


def _sqbrac(seq):
    return "".join(["[", *seq, "]"])


def _ren_k1q1_kq(tmpl):
    inside = _hlp_k1q1(tmpl)
    return "".join(inside)


def _ren_k1q1_qk(tmpl):
    inside = list(reversed(_hlp_k1q1(tmpl)))
    return "".join(inside)


def _hlp_k1q1(tmpl):
    return (
        _paren(wtp.template_element(tmpl, 1)),
        " ",
        _sqbrac(wtp.template_element(tmpl, 2)),
    )


_INTERESTING_STRS = {" ", hpu.SOPA}
_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    #
    "מ:פסק": wt_qere.hnd_identity,
    'כו"ק': wt_qere.mktmpl_mp,
    'קו"כ': wt_qere.mktmpl_mp,
}
_HANDLERS_A = {
    **_HANDLERS,
    "מ:כפול": wt_qere.hnd_recurse_on_param_alef,
}
_HANDLERS_B = {
    **_HANDLERS,
    "מ:כפול": wt_qere.hnd_recurse_on_param_bet,
}
_RENDERERS = {
    "מ:פסק": lambda w: sd.NBSP + sd.DOUB_VERT_LINE + " ",
    'כו"ק': _ren_k1q1_kq,
    'קו"כ': _ren_k1q1_qk,
}
_TMPL_NAME_REMAPS = {
    "מ:פסק": "paseq",
    'כו"ק': "k1q1-kq",
    'קו"כ': "k1q1-qk",
}
_KQ0 = "kq-complex"
_FEATURES = {
    ("paseq",): None,
    ("paseq", "paseq"): None,
    ("paseq", "paseq", "paseq"): None,
    #
    (hpu.SOPA,): None,
    #
    ("paseq", "k1q1-kq"): (_KQ0, "k1q1-after-paseq"),
    ("paseq", "k1q1-qk"): (_KQ0, "k1q1-qk-after-paseq"),
    ("paseq", "paseq", "k1q1-kq"): (_KQ0, "k1q1-after-paseq"),
    # Above, we ignore the ×2 paseq, lumping it in a
    # single category, k1q1-after-paseq.
    ("k1q1-kq", " ", "k1q1-kq"): (_KQ0, "k1q1×2"),
    ("k1q1-kq", " ", "k1q1-kq", hpu.SOPA): (_KQ0, "k1q1×2"),
    ("k1q1-kq", " ", "k1q1-kq", " ", "k1q1-kq"): (_KQ0, "k1q1×3"),
    ("k1q1-qk", hpu.SOPA): (_KQ0, "k1q1←sp"),
    #
    ("k1q1-kq", hpu.SOPA): None,
    ("k1q1-kq",): None,
    ("k1q1-kq", "paseq"): None,
    ("k1q1-kq", "paseq", "paseq"): None,
    ("k1q1-qk",): None,
}
