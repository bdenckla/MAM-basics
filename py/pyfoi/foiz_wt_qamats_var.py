import re
from pycmn import template_names as tmpln
from pycmn import ws_tmpl2 as wtp
from pycmn import uni_heb as uh
from pycmn import hebrew_points as hpo
from py_misc import analyze_qamats_variant as aqv
from pyfoi import foi_struct as fct
from pyfoi import foi_wikitext_helpers as fwh
from pyfoi import regexp_helpers as rh
from pycmn.my_utils import sl_map


def find_fois_wt(mroge):
    """Find מ:קמץ template uses: they are the feature of interest."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _record_qamats_variation_as_foi(_foilers, stack, tmpl):
    dalsam = _dalsam(tmpl)
    dsa = aqv.analyze_dalsam(dalsam)
    return _handle_qq_analysis(stack, dsa)


_PATT_XQ_WORD = r"\S*" + hpo.XQAMATS + r"\S*"


def _record_xataf_qamats(stack, string):
    words = re.findall(_PATT_XQ_WORD, string)
    if not words:
        return []
    if stack == ("doc-part-n",) or stack == ("kq-triv-doc",):
        return []
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    return sl_map((_make_xq_foi, stack_summary), words)


_DOTQ = rh.sqbq(hpo.SHIND + hpo.SIND)
_DAGQ = hpo.DAGOMOSD + r"?"
_LETT_AICAM = rh.par(rh.LETT + _DOTQ + _DAGQ)
# _LETT_AICAM:
#    a letter And Its Closely-Associated Marks, where those marks are
#    a shin dot, a sin dot, or nothing
#    a dagesh, or nothing


def _make_xq_foi(stack_summary, word):
    match = re.search(_LETT_AICAM + hpo.XQAMATS, word)
    assert match is not None
    (lett_aicam,) = match.groups()
    foi_qualifier = {
        "stack_str": stack_summary,
        "lett": lett_aicam,
    }
    foi_target = fct.make_qtarget(word, foi_qualifier)
    foi_path = ("xataf-qamats",)
    return foi_path, foi_target


def _dalsam(tmpl):
    dal_list = wtp.template_param_val(tmpl, "ד")
    sam_list = wtp.template_param_val(tmpl, "ס")
    return dal_list, sam_list


def _dalsam_htseq(dalsam):
    daleq_and_sameq = "ד=" + dalsam[0] + " " + "ס=" + dalsam[1]
    return (daleq_and_sameq,)


def _handle_qq_analysis(stack, dsa):
    dalsep, _samsep, accent, m2_lett, m3_zmnl = dsa["dsa-disputed-part"]
    qq_count = (len(dalsep) - 1) // 2
    accent_strq = uh.shunna(accent) if accent else None
    # strq: string or None
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    foi_qualifier = {
        "accent": accent_strq,
        "qq_count": str(qq_count),
        "stack_str": stack_summary,
        "m2_lett": m2_lett,
        "m3_zmnl": uh.join_shunnas(m3_zmnl),
    }
    return _finish_handling_analysis(dsa, foi_qualifier)


def _finish_handling_analysis(dsa, foi_qualifier):
    dalsep, samsep, accent, _m2_lett, _m3_zmnl = dsa["dsa-disputed-part"]
    dalsam = "".join(dalsep), "".join(samsep)
    foi_target = fct.make_qtarget(_dalsam_htseq(dalsam), foi_qualifier)
    foi1_path = "qamats-variants", _acc_qqc(accent, foi_qualifier)
    foi2_path = "qamats-variants", "all"
    foi1 = foi1_path, foi_target
    foi2 = foi2_path, foi_target
    return [foi1, foi2]


def _acc_qqc(accent, foi_qualifier):
    if accent:  # See note on Psalm 80:10
        acc = "accent-1-" + foi_qualifier["accent"]
    else:
        acc = "accent-0"
    qqc = "qq-count-" + foi_qualifier["qq_count"]
    return f"{acc}-{qqc}"


# In one case, Psalm 80:10, there is an accent but it doesn't indicate stress.
# The accent is geresh muqdam (without a coincident revia).


_FOILERS = {
    "מ:קמץ": _record_qamats_variation_as_foi,
    str: _record_xataf_qamats,
    #
    "מ:כפול": fwh.label_args_of_dualcant,
    "נוסח": fwh.label_args_of_doc,
    'קו"כ-אם': fwh.label_args_of_kq_triv,
    tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.ignore,
}
_STACK_SUMMARIES = {
    tuple(): None,
    ('כו"ק', "מ:דחי"): -1,
    ("kq-triv-target",): None,
    ("doc-target",): None,
    ("doc-target", 'קו"כ-אם'): None,
    ("doc-target", 'כו"ק'): None,
    ("doc-target", 'קו"כ'): None,
    ('קו"כ-אם',): None,
    ('כו"ק',): None,
    ('קו"כ',): None,
    (fwh.DUALCANT_ARG_COMBINED, "doc-target"): -2,
    (fwh.DUALCANT_ARG_ALEF,): -1,
    (fwh.DUALCANT_ARG_BET,): -1,
}
