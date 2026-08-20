from mb_cmn import hebrew_points as hpo
from author_boj_util.short_id_etc import short_id
from pydiff_mm.diff_mm_diffs_description import get1 as get_diff_description
from author_boj_util.proposed import proposed


def enrich_one_qr_by_adding_auto_diff(quirkrec):
    """Add qr-auto-diff field describing how proposed differs from consensus.

    Args:
        quirkrec: partially-enriched quirkrec dict (must have
            qr-consensus or qr-intermediate, and a proposed field).
    """
    pro = proposed(quirkrec).replace(_CGJ, "")
    con_key, con_or_int = _con_or_int(quirkrec)
    if _ignore_g3yh_diff(quirkrec, con_key):
        pro, con_or_int = _strip_g3yh_meteg(pro, con_or_int)
    con_or_int_wo_cgj = con_or_int.replace(_CGJ, "")
    auto_diff = get_diff_description(con_or_int_wo_cgj, pro)
    return {**quirkrec, "qr-auto-diff": auto_diff}


def _con_or_int(quirkrec):
    for con_key in ("qr-intermediate", "qr-consensus"):
        if val := quirkrec.get(con_key):
            return con_key, val
    assert False, f"No consensus or intermediate in {short_id(quirkrec)}"


def _ignore_g3yh_diff(quirkrec, con_key):
    gval = quirkrec.get("qr-ignore-g3yh-diff")
    sval = quirkrec.get(_SPECIFIC[con_key])
    assert not (gval and sval), f"Conflicting g3yh ignore flags in {short_id(quirkrec)}"
    return gval or sval


def _strip_g3yh_meteg(pro, consensus):
    pro_count = pro.count(_G3YA)
    con_count = consensus.count(_G3YA)
    assert (pro_count, con_count) in ((1, 0), (0, 1)), (
        f"Expected exactly one meteg in exactly one of proposed/consensus, "
        f"got pro={pro_count}, con={con_count}"
    )
    return pro.replace(_G3YA, ""), consensus.replace(_G3YA, "")


_CGJ = "\u034f"  # combining grapheme joiner
_SPECIFIC = {
    "qr-intermediate": "qr-ignore-g3yh-diff-in-intermediate",
    "qr-consensus": "qr-ignore-g3yh-diff-in-consensus",
}
_G3YA = hpo.MTGOSLQ
