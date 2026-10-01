from mb_cmn.my_utils import sl_map
import phonetic_mam.core.udl_from_he as rfh
import phonetic_mam.core.deut_32_6_haladonai as haladonai
import phonetic_mam.core.dualcant_untangler as dcut
import phonetic_mam.core.distinguished as disting
import phonetic_mam.core.syllables as syl
import phonetic_mam.core.stress as stress
import phonetic_mam.core.dtx_struct as dtxs


def list_of_sods_from_phrase(dtx, phrase_ydc_ydys_h):
    #
    # phrase_ydc_ydys: a string containing a phrase in yDC, yDyS-H format
    # yDC: Dualcant? Yes. (Possibly.) (I.e. could be tangled.)
    # yDyS: Dagesh [distinctions]? Yes. Sheva [distinctions]? Yes.
    # (uses the U+05C8 and U+05C9 annotation points to make those distinctions)
    # yDyS-H: yDyS represented in the Hebrew Unicode block (as opposed to deeplat)
    # sod: sas or dualcant
    # sas: syllables and stress; a dict of
    #    'sas-eudlcw': an eudlcw
    #    'sas-syls-per-atom': a list of lists: syllables per atom
    #    'sas-isps-one-d': the (flat) index of the syllable with primary stress
    #    'sas-isps-two-d': a pair of the atom and syllable indices of the syllable with primary stress
    # dualcant-sas: dict containing a sas for alef and bet (see _make_sas_dualcant below)
    #
    chanted_words = phrase_ydc_ydys_h.split(" ")
    chanted_words = haladonai.join_haladonai(chanted_words)
    list_of_sods = sl_map((_get_sod_from_cw_ydc_ydys, dtx), chanted_words)
    return list_of_sods


def is_sas(sod):
    return "sas-eudlcw" in sod


def _get_sod_from_cw_ydc_ydys(dtx, cw_ydc_ydys):
    # cw_ydc_ydys is one of the following two things:
    #    a space-free string
    #    the haladonai string 'הַ לְיְהֹוָה֙'
    if cw_ydc_ydys == "":
        return None
    if utrec := dcut.untangle(dtx, cw_ydc_ydys):
        dualcant = _make_sas_dualcant(dtx, utrec, cw_ydc_ydys)
        return dualcant
    cw_ndc_ydys = cw_ydc_ydys  # ndc: non-dualcant (non-tangled)
    sas = _get_sas_from_cw_ndc_ydys(dtx, cw_ndc_ydys)
    return sas


def _make_sas_dualcant(dtx, utrec, orig_super):
    otword_for_alef = utrec["utrec-mam-alef"]
    otword_for_bet = utrec["utrec-mam-bet"]
    otsas_for_alef = sl_map((_get_sas_from_cw_ndc_ydys, dtx), otword_for_alef)
    # Preserve both strands in the phonetic product, but count only the alef
    # (taxton) strand in the census of an implied edition.
    dtx_without_bet_census = dtxs.suppress_edition_census(dtx)
    otsas_for_bet = sl_map(
        (_get_sas_from_cw_ndc_ydys, dtx_without_bet_census), otword_for_bet
    )
    sas_dualcant = {
        "sasdc-orig-superimposed": orig_super,
        "sasdc-mam-superimposed": utrec["utrec-mam-superimposed"],
        "sasdc-ot-alef": otsas_for_alef,
        "sasdc-ot-bet": otsas_for_bet,
    }
    return sas_dualcant


_UHCW_FMTT_YDYS = "cw_wfmtt-fmtt-ydys"
_UHCW_FMTT_NDNS = "cw_wfmtt-fmtt-ndns"


def _get_sas_from_cw_ndc_ydys(dtx, cw_ndc_ydys: str):
    cw_wfmtt = {"cw_wfmtt-str": cw_ndc_ydys, "cw_wfmtt-fmtt": _UHCW_FMTT_YDYS}
    return _get_sas_from_ndc_cw_wfmtt(dtx, cw_wfmtt)


def _is_ndns(cw_wfmtt):
    return cw_wfmtt["cw_wfmtt-fmtt"] == _UHCW_FMTT_NDNS


def _is_ydys(cw_wfmtt):
    return cw_wfmtt["cw_wfmtt-fmtt"] == _UHCW_FMTT_YDYS


def _get_str(cw_wfmtt):
    return cw_wfmtt["cw_wfmtt-str"]


def _get_eudlcw_phi_if_diff(cw_str, eudlcw_1):
    cw_str_ndns = disting.to_generic_points(cw_str)
    eudlcw_phi = rfh.get_eudlcw_from_cw_ndns(cw_str_ndns)
    u_1 = eudlcw_1["eudlcw-udlcw"]
    u_2 = eudlcw_phi["eudlcw-udlcw"]
    eudlcw_phi_if_diff = eudlcw_phi if u_1 != u_2 else None
    return eudlcw_phi_if_diff


def _get_sas_from_ndc_cw_wfmtt(dtx, cw_wfmtt):
    # ndc: non-dualcant (non-tangled)
    # (i.e. a word that either has been untangled or did not need to be untangled)
    # cw_wfmtt: a dict containing a chanted word string and a format tag string
    # (tag says whether format is yDyS or nDnS)
    cw_str = _get_str(cw_wfmtt)
    if _is_ndns(cw_wfmtt):
        eudlcw = rfh.get_eudlcw_from_cw_ndns(cw_str)
        eudlcw_phi_if_diff = None
    else:
        assert _is_ydys(cw_wfmtt)
        eudlcw = rfh.get_eudlcw_from_cw_ydys(cw_str)
        eudlcw_phi_if_diff = _get_eudlcw_phi_if_diff(cw_str, eudlcw)
    syls_per_atom = syl.get_syllables(eudlcw)
    pstress = stress.get_primary_stress(dtx, syls_per_atom, rfh.accar(eudlcw))
    bcc, isps_one_d, isps_two_d = pstress
    sas = {
        "sas-eudlcw": eudlcw,
        "sas-eudlcw-phi": eudlcw_phi_if_diff,
        "sas-syls-per-atom": syls_per_atom,
        "sas-isps-one-d": isps_one_d,
        "sas-isps-two-d": isps_two_d,
        "sas-stress-bcc": bcc,
        "sas-cantsys": dtxs.get_cantsys(dtx),
        "sas-qamats": dtxs.get_qamats(dtx),
    }
    return sas
