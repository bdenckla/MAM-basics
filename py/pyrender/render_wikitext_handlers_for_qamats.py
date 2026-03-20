"""Exports handle"""

from pyrender import render_wikitext_helpers as wt_help
from pyrender import render_element as renel
from py_misc import analyze_qamats_variant as aqv
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import ws_tmpl2 as wtp
from pycmn import uni_heb as uh


def handle(hctx, tmpl):
    """
    Handle the מ:קמץ template by tagging the dalet variant with the
    appropriate dqq (disputed qamats qatan) tag: stressed or unstressed.
    This not only indicates that qamats variation exists but also
    indicates whether small meteg should be used or not.
    """
    #
    # We tag the dalet variant to record whether the syllable of the
    # disputed qamats already has a stress marker. See note above.
    #
    dalseq = _dal_qamats_variation(hctx, tmpl)
    if wt_help.get_renopt(hctx, "ro_qamats_var") == "rv-dalet":
        return dalseq
    samseq = _sam_qamats_variation(hctx, tmpl)
    dalsam = dalseq, samseq
    dsa = aqv.analyze_dalsam(dalsam)
    out = (
        *dsa["dsa-undisputed-prefix"],
        *_handle_disputed(dsa["dsa-disputed-part"]),
        *dsa["dsa-undisputed-suffix"],
        *dsa["dsa-dal-endpunc"],
    )
    return out


def _handle_disputed(dsa_disputed_part):
    dalsep, _samsep, accent, _m2_lett, _m3_zmnl = dsa_disputed_part
    tag = None
    if accent is not None and accent != ha.GER_M:
        assert accent in {hpo.MTGOSLQ, ha.MER, ha.MUN}, uh.shunna(accent)
        tag = "mam-dqq-stressed"
    elif len(dalsep) == 3:
        tag = "mam-dqq-unstressed"
    if tag:
        return (renel.mk_ren_el_tc(tag, "".join(dalsep)),)
    assert len(dalsep) == 5
    dal0 = "".join(dalsep[0:2])
    dal1 = "".join(dalsep[2:5])
    dal0_renel = renel.mk_ren_el_tc("mam-dqq-unstressed", dal0)
    return dal0_renel, dal1


# I can say "THE syllable of THE disputed qamats" because luckily there is
# never more than one disputed qamats per word.
#
# I define a stress marker as a meteg or an accent indicating stress.
#
# A syllable has an accent indicating stress if one of the
# following is true of that syllable:
#
#    1. It has an impositive accent.
#    2. It has a stress helper accent.
#    3. It has a stressed non-impositive accent.
#
# (A non-impositive accent is stressed if its word neither has nor needs
# a stress helper.)
#
# Note that we consider revia to be the stress helper for geresh muqdam.
#
# It is unclear what to do about dexi since MAM doesn’t have dexi stress
# helpers. To determine whether a MAM dexi indicates stress, we have to
# determine whether the word NEEDS a stress helper, since we know it won't
# HAVE a stress helper! Dexi never appears on a syllable with qamats qatan,
# but I don't know if qamats qatan ever appears on a syllable that needs
# a dexi stress helper. I guess it is okay to have small meteg on such
# a syllable though.


def _dal_qamats_variation(hctx, tmpl):
    """Return the dalet variant."""
    # {{מ:קמץ|ד=אאא|ס=בבב}}
    #
    # The dalet argument is the "theoretical" variant.
    # The samekh argument is the Sephardic variant.
    #
    assert wtp.template_len(tmpl) == 3
    return wt_help.render_named_param_val(hctx, tmpl, "ד")


def _sam_qamats_variation(hctx, tmpl):
    """Return the samekh variant."""
    assert wtp.template_len(tmpl) == 3
    return wt_help.render_named_param_val(hctx, tmpl, "ס")
