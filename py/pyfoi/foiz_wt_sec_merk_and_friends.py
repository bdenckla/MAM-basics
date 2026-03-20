import re
from pycmn import str_defs as sd
from pycmn import bib_locales as tbn
from pycmn import uni_heb_2 as u2
from pycmn import hebrew_accents as ha
from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_seqs
from py_misc import wt_qere
from pyfoi import foi_struct as fct
from pyfoi import foi_accent_tree as fat
from pyfoi import sec_yyy_qualifier as smq
from pyfoi import sec_yyy_shewa as smsh
from pyfoi import regexp_helpers as rh

# XXX TODO: related prose phenomenon such as the following:
#
#     azla-geresh
#     metigah-zaqef
#     mayela-silluq & mayela-atnax
#


def find_fois_wt(mroge):
    """
    This returns FOIs with paths starting with sec-merk and four friends.
    The four friends are as follows:
        sec-misc
        sec-merk-shewa
        sec-misc-shewa
        sec-star-breuer-cos
    """
    is_poca = tbn.is_poetcant(mroge["mroge-bcvt"])
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    word_summaries = sl_map((_get_word_summary, is_poca), _with_prev(verse))
    closure = _features_for_word, is_poca, verse
    features_per_word = sl_map(closure, enumerate(word_summaries))
    return filter(None, sum_of_seqs(features_per_word))


def _with_prev(lst: list):
    return zip([None] + lst, lst)


def _features_for_word(is_poca, verse, indexed_word_summary):
    idx, word_summary = indexed_word_summary
    if word_summary is None:
        return (None, None)
    ws_fp_lvl_1 = word_summary["fp_lvl_1"]  # FOI path level 1, e.g. "sec-merk"
    ws_acc_str = word_summary["acc_str"]
    ws_psg_class = word_summary["psg_class"]
    if ws_acc_str in _ACC_STRS_TO_REJECT[ws_fp_lvl_1]:
        return (None, None)
    fp_lvl_3 = _fp_lvl_3(ws_acc_str, ws_psg_class)  # FOI path level 3, e.g. "(atn)"
    cantsys = _get_cantsys_short_str(is_poca)  # "poetic" or "prose"
    foi_path = ws_fp_lvl_1, cantsys, fp_lvl_3, ws_acc_str
    qualkey, foi_target_proper = _target_proper(fp_lvl_3, verse, idx)
    foi_qualifier = smq.sec_yyy_qualifier(qualkey)
    foi_target = fct.make_qtarget(foi_target_proper, foi_qualifier)
    feature_for_main = foi_path, foi_target
    if ws_psg_class:
        feature_for_shewa = None
    else:
        feature_for_shewa = smsh.shewa_feature(feature_for_main, verse[idx])
    ffr = _features_for_refs(foi_target, foi_qualifier)
    return feature_for_main, feature_for_shewa, *ffr


def _features_for_refs(foi_target_for_main, foi_qualifier):
    closure = _feature_for_ref, foi_target_for_main, foi_qualifier
    return sl_map(closure, ("ref_1", "ref_2"))


def _feature_for_ref(foi_target_for_main, foi_qualifier, ref_key):
    if ref := foi_qualifier.get(ref_key):
        foi_path = "sec-star-breuer-cos", ref
        return foi_path, foi_target_for_main
    return None


_DVL = sd.DOUB_VERT_LINE
_DVL_SP = _DVL + " "
_NBSP_DVL_SP = sd.NBSP + _DVL_SP


def _target_proper(ender, verse, idx):
    if ender in _PSG_ENDINGS:
        idx_stop = idx + 2
        tphrase = " ".join(verse[idx:idx_stop])
        return tphrase, _tweak_dvl(tphrase)
    tword = verse[idx]
    sinfo = smq.servant_info(tword)
    if sinfo:
        bwd = sinfo.get("bwd-context") or 0
        fwd = sinfo.get("fwd-context") or 0
        assert bwd or fwd, "Servant info must have non-zero context."
        idx_start = idx - bwd
        idx_stop = idx + fwd + 1
        tphrase = " ".join(verse[idx_start:idx_stop])
        return tword, _tweak_dvl(tphrase)
    return tword, _tweak_dvl(tword)


def _tweak_dvl(phrase: str):
    if phrase.endswith(_DVL):
        out = phrase[: -len(_DVL)]
    else:
        out = phrase
    out = out.replace(_DVL_SP, _NBSP_DVL_SP)
    return out


def _get_cantsys_short_str(is_poca):
    return "poetic" if is_poca else "prose"


def _get_word_summary(is_poca, prevw_and_curw):
    """Get the summary of the current word given the previous word and the current word."""
    prevw, curw = prevw_and_curw
    if ha.OLE in curw or (prevw and ha.OLE in prevw and ha.MER not in prevw):
        return None
    if ha.MER in curw and not _early_rejects_for_mer(curw):
        acc_str = _acc_str_from_cword(is_poca, curw)
        return _mk_word_summary_1("sec-merk", acc_str, curw)
    if ha.MAH in curw or is_poca and ha.TIP in curw:
        if _early_rejects_for_misc(curw):
            return None
        acc_str = _acc_str_from_cword(is_poca, curw)
        return _mk_word_summary_1("sec-misc", acc_str, curw)
    return None


_NON_ACC_PATTERN = f"[^{ha.ACCENTS_AND_MTG}]+"
_EARLY_REJECTS_FOR_MER_1 = f"{hpo.MTGOSLQ_RE}*{ha.ZSH_OR_TSIT_RE}?{ha.MER_RE}"
_EARLY_REJECTS_FOR_MER_2 = f"{ha.MAH_RE}.*{ha.MER_RE}"
_MAH_OR_TIP = rh.sqb(f"{ha.MAH_RE}{ha.TIP_RE}")
_EARLY_REJECTS_FOR_MISC = f"{hpo.MTGOSLQ_RE}*{ha.ZSH_OR_TSIT_RE}?{_MAH_OR_TIP}"


def _rm_all_exc_accents_and_mtg(cword: str):
    """Remove all characters except accents and mtg."""
    return re.sub(_NON_ACC_PATTERN, "", cword)


def _early_rejects_for_mer(cword: str):
    acc_and_mtg = _rm_all_exc_accents_and_mtg(cword)
    if re.fullmatch(_EARLY_REJECTS_FOR_MER_1, acc_and_mtg):
        return True
    if re.fullmatch(_EARLY_REJECTS_FOR_MER_2, acc_and_mtg):
        return True
    return False


def _early_rejects_for_misc(cword: str):
    return re.fullmatch(_EARLY_REJECTS_FOR_MISC, _rm_all_exc_accents_and_mtg(cword))


def _acc_str_from_cword(is_poca, cword: str):
    return fat.str_from_acc_node(fat.acc_node_from_cword(is_poca, cword))


def _mk_word_summary_1(fp_lvl_1: str, acc_str: str, cword: str):
    if acc_str.endswith("(ümtg)"):
        psg_class = _psg_class(cword)
        return _mk_word_summary_2(fp_lvl_1, acc_str, psg_class)
    return _mk_word_summary_2(fp_lvl_1, acc_str, "")


def _mk_word_summary_2(fp_lvl_1: str, acc_str: str, psg_class: str):
    return {
        "fp_lvl_1": fp_lvl_1,
        "acc_str": acc_str,
        "psg_class": psg_class,
    }


def _psg_class(cword):
    for psge in _PSG_ENDING_FR_WORD_ENDING:
        if re.search(psge[0] + r"$", cword):
            return psge[1]
    return _PSG_MISC


# See Yeivin ITM sections:
#    #325: Gaʿya before Paseq
#    #332: Gaʿya on an Open, Post-stress Syllable
#    #338: Gaʿya on a Closed, Ṣere-vowelled, Post-stress Syllable
#    #354: Gaʿya on a Guttural-closed Syllable
_PSG_CLOSED_AFTER_TSERE = "psg-closed-after-tsere"
_PSG_CLOSED_BY_GUTTURAL = "psg-closed-by-guttural"
_PSG_BEFORE_PASEQ = "psg-before-paseq"
_PSG_OPEN = "psg-open"
_PSG_MISC = "psg-misc"
_PSG_ENDINGS = [
    _PSG_CLOSED_AFTER_TSERE,
    _PSG_CLOSED_BY_GUTTURAL,
    _PSG_BEFORE_PASEQ,
    _PSG_OPEN,
    _PSG_MISC,
]
_PSG_ENDING_FR_WORD_ENDING = [
    (hpo.TSERE + hpo.MTGOSLQ + rh.LETT, _PSG_CLOSED_AFTER_TSERE),
    #
    (rh.sqb("חע") + hpo.PATAX + hpo.MTGOSLQ + r"?", _PSG_CLOSED_BY_GUTTURAL),
    (hpo.PATAX + hpo.MTGOSLQ + rh.ncpar("הּ|ח|ע"), _PSG_CLOSED_BY_GUTTURAL),
    #
    (hpo.XIRIQ + hpo.MTGOSLQ + "י", _PSG_OPEN),
    (hpo.QAMATS + hpo.MTGOSLQ + rh.sqbq("ה|א"), _PSG_OPEN),
    ("וֹ", _PSG_OPEN),
    ("וּ", _PSG_OPEN),
    #
    (sd.DOUB_VERT_LINE, _PSG_BEFORE_PASEQ),
]


def _fp_lvl_3(ws_acc_str: str, ws_psg_class: str):
    if ws_psg_class:
        return ws_psg_class
    for ender in _ENDERS:
        if ws_acc_str.endswith(ender):
            return ender
    return "a-misc"


def _hnd_return_nu_gmaq_str(_1, tmpl):
    return [hpu.NU_GMAQ]


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,
    "מ:פסק": wt_qere.hnd_return_doub_vert_line_plus_space,
    "מ:כפול": wt_qere.hnd_recurse_on_param_alef,
    "מ:מקף אפור": _hnd_return_nu_gmaq_str,
}
_ENDERS = [
    #
    *_PSG_ENDINGS,
    #
    u2.REV,
    u2.MUN,
    u2.MER,
    u2.MAH,
    u2.ATN,
    u2.Z_OR_TSOR,
    u2.PAZ,
    #
    u2.NU_SLQ,
    u2.NU_MTG,
    u2.NU_AZL,
    u2.NU_AZL_LEG,
    u2.NU_TAR,
    u2.NU_TIP,
    u2.NU_REV_IRM,
    #
    u2.TEV,
    u2.PASH,
]
_ACC_STRS_TO_REJECT_FR_SEC_MERK_T = [
    fat.across_atoms(
        [u2.ZSH_OR_TSIT, fat.across_letters([u2.MER, u2.NU_MTG]), u2.NU_SLQ],
        [hpu.NU_GMAQ, hpu.NU_GMAQ],
    ),
]
_ACC_STRS_TO_REJECT_FR_SEC_MERK = set(
    sl_map(fat.str_from_acc_node, _ACC_STRS_TO_REJECT_FR_SEC_MERK_T)
)
_ACC_STRS_TO_REJECT = {
    "sec-merk": _ACC_STRS_TO_REJECT_FR_SEC_MERK,
    "sec-misc": set(),
}
