"""Exports refine"""

from pycmn import hebrew_punctuation as hpu
from pydiff_mm import diff_mm_separators as seps
from pydiff_mm import diff_mm_diffs_description as description
from pycmn import template_names as tmpln


def refine(vala, valb):
    """Process a diff prior to reduction (refinement)"""
    funs = (
        _preproc_q_of_kq,
        _preproc_kq_triv_to_kq_real,
        _preproc_added_qamats_variation,
        _preproc_wordsep_change,
    )
    for fun in funs:
        if desc := fun(vala, valb):
            return desc
    return description.get2(vala, valb)


def _preproc_q_of_kq(vala, valb):
    qvala = _get_q_of_kq(vala)
    qvalb = _get_q_of_kq(valb)
    return qvala and qvalb and description.get2(qvala, qvalb)


def _preproc_kq_triv_to_kq_real(vala, valb):
    qere_a = _get_kq_triv(vala)
    kq_b = _get_kq_of_kq(valb)
    if not qere_a or not kq_b:
        return None
    ketiv_b, qere_b = kq_b
    dide = description.get1(qere_a, qere_b)
    refine_str = (
        "trivial kq converted to kq with k "
        + ketiv_b
        + " and new q differing from old q by "
        + str(dide)
    )
    return refine_str, "trivial kq to kq"


def _preproc_added_qamats_variation(vala, valb):
    vb_qvs = _get_qamats_variants(valb)
    if vb_qvs is None:
        return None
    qvi = vala, vb_qvs
    return _qv_desc(qvi, "dalet") or _qv_desc(qvi, "samekh")


def _qv_desc(qvi, vna):
    vala, vb_qvs = qvi
    # sl_vb_qv_vna : singleton list [whose one element is]
    # the valb qamats variant with name vna
    sl_vb_qv_vna = [vb_qvs[vna]]
    if vala == sl_vb_qv_vna:
        return _qv_add_equal(vb_qvs, vna), "qamats variation added"
    return None


def _qv_add_equal(vb_qvs, vna):
    desc = description.get1(vb_qvs["dalet"], vb_qvs["samekh"])
    # We introduce "long" variant names because otherwise it
    # can be confusing to see, for example "dalet" used to describe
    # both a variant and the actual letter, e.g.
    #
    #    To change the dalet into the samekh, on dalet,
    #    replace qamats-qatan with qamats
    #
    d_var = "d-variant"
    s_var = "s-variant"
    long_vna_dic = {"dalet": d_var, "samekh": s_var}
    long_vna = long_vna_dic[vna]
    return " ".join(
        (
            "Added qamats variation where only the",
            long_vna,
            "variant was present before.",
            f"To change the {d_var} into the {s_var},",
            desc[0] + ".",
        )
    )


def _preproc_wordsep_change(vala, valb):
    qsep_a = _get_qualified_separator(vala)
    qsep_b = _get_qualified_separator(valb)
    if qsep_a is not None and qsep_b is not None:
        _sep_a, words_separated_a = qsep_a
        _sep_b, words_separated_b = qsep_b
        if words_separated_a == words_separated_b:
            details = _preproc_wordsep_change_desc(qsep_a, qsep_b)
            return details, "separator changed"
    return None


def _preproc_wordsep_change_desc(qsep_a, qsep_b):
    sep_a = qsep_a[0]
    sep_b = qsep_b[0]
    return _desc0(sep_a, sep_b) + _desc1(qsep_a, qsep_b) + _explanation(sep_a, sep_b)


def _desc0(sep_a, sep_b):
    sep_name_a = _SEP_INFOS[sep_a][0]
    sep_name_b = _SEP_INFOS[sep_b][0]
    return f"separator changed from {sep_name_a} to {sep_name_b}"


def _desc1(qsep_a, qsep_b):
    sep_a, words_separated_a = qsep_a
    sep_b, words_separated_b = qsep_b
    sep2_a = _SEP_INFOS[sep_a][1]
    sep2_b = _SEP_INFOS[sep_b][1]
    phrase_a = sep2_a.join(words_separated_a)
    phrase_b = sep2_b.join(words_separated_b)
    return f", changing {phrase_a} to {phrase_b}"


def _explanation(sep_a, sep_b):
    exps = []
    if exp_a := _SEP_INFOS[sep_a][2]:
        exps.append(exp_a)
    if exp_b := _SEP_INFOS[sep_b][2]:
        exps.append(exp_b)
    if and_str := " and where ".join(exps):
        return " where " + and_str
    return ""


def _get_q_of_kq(side):
    if isinstance(side, list) and len(side) == 1:
        if tyod := _triple_yod(side[0], 'כו"ק:2'):
            return [tyod]
        if tyod := _triple_yod(side[0], tmpln.K2Q2 + ":2"):
            return [tyod]
        if tyod := _triple_yod(side[0], tmpln.K3Q3 + ":2"):
            return [tyod]
    return None


def _get_kq_of_kq(side):
    if isinstance(side, list) and len(side) == 2:
        if ketiv := _triple_yod(side[0], 'כו"ק:1'):
            if qere := _triple_yod(side[1], 'כו"ק:2'):
                return ketiv, qere
    return None


def _get_kq_triv(side):
    if isinstance(side, list) and len(side) == 1:
        if qere := _triple_yod(side[0], 'קו"כ-אם:1'):
            return qere
    return None


def _get_qualified_separator(side):
    if isinstance(side, list) and len(side) == 1:
        if isinstance(side[0], tuple) and len(side[0]) == 3:
            if side[0][0] in seps.SEPARATORS:
                return side[0][0], (side[0][1], side[0][2])
    return None


def _get_qamats_variants(side):
    if isinstance(side, list) and len(side) == 2:
        if tyod1 := _triple_yod(side[0], "מ:קמץ:1"):
            dalet = _strip_prefix("ד=", tyod1)
            if tyod2 := _triple_yod(side[1], "מ:קמץ:2"):
                samekh = _strip_prefix("ס=", tyod2)
                return {"dalet": dalet, "samekh": samekh}
    return None


def _strip_prefix(prefix, string):
    assert string.startswith(prefix)
    return string[len(prefix) :]


def _triple_yod(siden, argspec):
    if not isinstance(siden, tuple):
        return None
    if siden[0] != "ייי":
        return None
    if siden[2] == (argspec,):
        return siden[1]
    return None


_DOUBLE_MAQAF_EXPLANATION = "double maqaf represents gray maqaf"
_DOUBLE_PASEQ_EXPLANATION = (
    "double Unicode PASEQ represents true paseq (as opposed to legarmeih)"
)
_SEP_INFOS = {
    " ": ("space", " ", None),
    hpu.MAQ: ("maqaf", hpu.MAQ, None),
    "מ:לגרמיה": ("legarmeih", hpu.PASOLEG + " ", None),
    "מ:מקף אפור": ("gray maqaf", hpu.MAQ + hpu.MAQ, _DOUBLE_MAQAF_EXPLANATION),
    "מ:פסק": ("paseq", hpu.PASOLEG + hpu.PASOLEG, _DOUBLE_PASEQ_EXPLANATION),
    "ר0": ("resh-0", "{0}", None),
    "ר1": ("resh-1", "{1}", None),
    "ר2": ("resh-2", "{2}", None),
    "ר3": ("resh-3", "{3}", None),
}
