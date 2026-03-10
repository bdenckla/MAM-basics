from pycmn import str_defs as sd
from pycmn import bib_locales as tbn
from pycmn import uni_heb as uh
from pycmn import uni_heb_2 as u2
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from py_misc import wt_qere
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map


def find_fois_wt(mroge):
    bcvt = mroge["mroge-bcvt"]
    if tbn.is_poetcant(bcvt):
        return []
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
    run_els = []
    last = None
    for wordstr in verse:
        run_els.append(_get_run_el_from_word(last, wordstr))
        last = run_els[-1]
    runsdic = _runsdic(run_els)
    features = sum_of_map((_feature, verse), runsdic.items())
    features = _cant_qualify(qual_str, features)
    return features


def _runsdic(run_els):
    accum = []
    last = None
    for idx, run_el in enumerate(run_els):
        if run_el is not None:
            if last is None or _run_el_is_final(last):
                accum.append([])
            accum[-1].append((idx, run_el))
        last = run_el
    simplified = dict(sl_map(_simplify, accum))
    return simplified


def _simplify(irps):  # irp: idx/run_el pair; irps: many irp
    return irps[0][0], list(pair[1] for pair in irps)


def _revia(mid):
    return _feat("⅃-leg", u2.REV, mid)


def _non_revia(stop, mid):
    return _feat("⅃-leg", f"non-revia ({stop})", mid)


def _munpas_pazer(mid):
    return _feat("⅃-pas", u2.PAZ, mid)


def _feat(start, stop, mid):
    return f"{start}...{stop} with {mid} intervening"


_RUN_TO_FEATURE = {
    ("sh-leg",): "shalshelet",
    #
    ("⅃-leg", u2.REV): _revia("0"),
    ("⅃-leg", u2.MUN, u2.REV): _revia("1 ⅃"),
    ("⅃-leg", "⅃-leg", u2.MUN, u2.REV): _revia("2 (⅃-leg,⅃)"),
    ("⅃-leg", u2.DAR, u2.MUN, u2.REV): _revia("2 (da,⅃)"),
    #
    ("⅃-leg", u2.MAH, u2.PASH): _non_revia("p", "1 " + u2.MAH),
    ("⅃-leg", u2.MAH, u2.PASH, u2.PASH): _non_revia("p", "1 " + u2.MAH),
    #
    ("⅃-leg", u2.QOM, u2.DAR, u2.TEV): _non_revia(u2.TEV, "2 (qa,da)"),
    #
    ("⅃-leg", u2.QOM, u2.GER): _non_revia("ge", "1 qa"),
    #
    ("⅃-leg", u2.PAZ): _non_revia(u2.PAZ, "0"),
    (u2.MER, "⅃-leg", u2.PAZ): _non_revia(u2.PAZ, "0"),
    #
    ("⅃-pas", u2.REV): "⅃-pas," + u2.REV,
    #
    ("⅃-pas", u2.MUN, u2.MUN, u2.PAZ): _munpas_pazer("2 (⅃,⅃)"),
    ("⅃-pas", u2.MUN, "⅃-pas", u2.PAZ): _munpas_pazer("2 (⅃,⅃-pas)"),
    ("⅃-pas", "⅃-pas", u2.MUN, u2.YBY): "⅃-pas-⅃",
    ("⅃-pas", u2.MUN, u2.TEL_Q): "⅃-pas-⅃",
    #
    ("⅃-pas", u2.PAZ): _munpas_pazer("0"),
    ("⅃-pas", u2.ATN): None,
    ("⅃-pas", u2.SEG_A): None,
    ("⅃-pas", u2.Z_OR_TSOR): None,
    ("⅃-pas", u2.ZAQ_Q): None,
    ("⅃-pas", u2.YBY): None,
    ("⅃-pas", u2.MAH): None,
    ("⅃-pas", u2.TEL_Q): None,
    ("⅃-pas", u2.QOM): None,
    ("⅃-pas", u2.GER_2): None,
    ("⅃-pas", u2.ZSH_OR_TSIT, u2.Z_OR_TSOR): None,
    ("⅃-pas", u2.TEL_G, u2.TEL_G): None,
    ("⅃-pas", u2.SEG_A, u2.SEG_A): None,
    ("⅃-pas", u2.TEL_Q, u2.TEL_Q): None,
    ("⅃-pas", "⅃-pas", u2.PAZ): _munpas_pazer("⅃-pas"),
    ("⅃-pas", "⅃-pas", u2.YBY): None,
    ("⅃-pas", "⅃-pas", u2.TEL_G, u2.TEL_G): None,
}


def _feature(verse, runsdic_item):
    idx, run = runsdic_item
    acc_names = sum_of_map(_run_el_get_accent_names, run)
    if feat := _RUN_TO_FEATURE[tuple(acc_names)]:
        foi_path = "pasoleg-1", feat
        foi_target = " ".join(verse[idx : idx + len(run)])
        return [(foi_path, foi_target)]
    return []


_MUNBAR = {"legarmeih": "⅃-leg", "paseq": "⅃-pas"}
_PASOLEG = {hpu.PASOLEG: "legarmeih", sd.DOUB_VERT_LINE: "paseq"}


def _get_run_el_from_word(last, wordstr):
    ans = uh.accent_names(uh.rm_mtgoslq(wordstr))
    pasoleg = _PASOLEG.get(wordstr[-1])
    if pasoleg and ans and ans[-1] == u2.MUN:
        munbar = _MUNBAR.get(pasoleg)
        tweaked_ans = *ans[:-1], munbar
        return _run_el_mk_nonfinal(munbar, tweaked_ans)
    if pasoleg == "legarmeih":
        assert len(ans) == 1 and ans[0] == u2.SHA
        tweaked_ans = ("sh-leg",)  # shalshelet
        return _run_el_mk_final(tweaked_ans)
    if last != None and not _run_el_is_final(last):
        return _misc_run_el(last, ans)
    return None


_LEG_TERMINATORS = frozenset(
    (
        u2.REV,
        u2.PASH,
        u2.TEV,
        u2.GER,
        u2.PAZ,
    )
)
_IS_FINAL_FN = {
    "⅃-pas": lambda an: an != u2.MUN,
    "⅃-leg": lambda an: an in _LEG_TERMINATORS,
}


def _misc_run_el(last, ans):
    type_of_run = _run_el_get_run_type(last)  # ⅃-pas or ⅃-leg
    is_final_fn = _IS_FINAL_FN[type_of_run]
    if any(map(is_final_fn, ans)):
        return _run_el_mk_final(ans)
    return _run_el_mk_nonfinal(type_of_run, ans)


def _run_el_mk_final(accent_names):
    # The type of run doesn't matter for a final run_el.
    # So we just use None.
    return "run_el-final", (None, accent_names)


def _run_el_mk_nonfinal(run_type, accent_names):
    return "run_el-nonfinal", (run_type, accent_names)


def _run_el_get_run_type(run_el):
    _f_nf, (run_type, _accent_names) = run_el
    return run_type


def _run_el_get_accent_names(run_el):
    _f_nf, (_run_type, accent_names) = run_el
    return accent_names


def _run_el_is_final(run_el):
    f_nf, (_run_type, _accent_names) = run_el
    return f_nf == "run_el-final"


def jacobson_features():
    shorts = (
        _revia("2 (da,⅃)"),
        _munpas_pazer("2 (⅃,⅃)"),
        _munpas_pazer("2 (⅃,⅃-pas)"),
        "⅃-pas-⅃",
    )
    longs = tuple(("pasoleg-1", short) for short in shorts)
    return longs


_HANDLERS = {
    **wt_qere.HANDLERS,
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
