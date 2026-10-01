import re

import phonetic_mam.core.qere_from_implicit_kq as qfikq
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.trans_tables as tt
import phonetic_mam.core.resolve_ambiguities as ra
import phonetic_mam.core.vowar_and_accar as va
import phonetic_mam.core.distinguished as disting
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.str_defs as sd


def get_eudlcw_from_cw_ndns(cw_ndns_h):
    # cw_ndns_h: a string containing a chanted word in nDnS-H format
    # nDnS: Dagesh [distinctions]? No. Sheva [distinctions]? No.
    # (ambiguous sheva and ambiguous dagesh)
    # nDnS-H: nDnS represented in the Hebrew Unicode block (as opposed to deeplat)
    audit = {}
    fva = _get_fva_from_cw_h(cw_ndns_h, audit)
    vowar = fva[1]
    adlcw = deeplat.get_deeplat_from_cw_ndns_h(vowar)  # adl: ambiguous deeplat
    udlcw = _audited_tweak(ra.resolve_ndns_ambiguities_in_adlcw, adlcw, audit, "adl")
    eudlcw = mk_eudlcw(udlcw, audit, fva)
    if concerns := ra.find_concerns(udlcw):
        eudlcw["eudlcw-concerns"] = concerns
    return eudlcw


def get_eudlcw_from_cw_ydys(cw_ydys_h):
    """
    Get an extended unambiguous-deeplat chanted word (eudlcw)
    from a chanted word in yDyS format.
    An extended udlcw is a dict consisting of:
        udlcw (a string)
        audit (a dict)
        fva (a triple: (full, vowar, accar))
    """
    audit = {}
    fva = _get_fva_from_cw_h(cw_ydys_h, audit)
    vowar = fva[1]
    adlcw = deeplat.get_deeplat_from_cw_ydys(vowar)  # adl: ambiguous deeplat
    udlcw = _audited_tweak(ra.resolve_ydys_ambiguities_in_adlcw, adlcw, audit, "adl")
    eudlcw = mk_eudlcw(udlcw, audit, fva)
    return eudlcw


def mk_eudlcw(udlcw, audit, fva):
    full = fva[0]
    repeated = disting.convert_to_repeated_form(full)
    return {
        "eudlcw-udlcw": udlcw,
        "eudlcw-audit": audit,
        "eudlcw-fva": fva,
        "eudlcw-repeated": repeated,
    }


def _get_fva_from_cw_h(cw_h, io_audit):
    full = _audited_tweak(
        qfikq.get_qere_from_implicit_kq, cw_h, io_audit, "before_qfikq"
    )
    full = _audited_tweak(_rm_cgj_from_kol, full, io_audit, "before_rm_kol_cgj")
    full = _audited_tweak(_rm_misc, full, io_audit, "before_rm_misc")
    #
    assert not re.search(_RE_NOT_HEBREW_OR_NU_GMAQ, full)  # assert only Hebrew-ish
    vowar, accar = va.vowar_and_accar(full)
    return full, vowar, accar


def accar(eudlcw):
    return eudlcw["eudlcw-fva"][2]


_KO_MER_L = "כׇּ֥ל"
_KO_CGJ_MER_L = _KO_MER_L[:-2] + sd.CGJ + _KO_MER_L[-2:]
_RE_NOT_HEBREW_OR_NU_GMAQ = f"[^{hpo.RECC_HEBR}{hpu.NU_GMAQ}]"


def _rm_cgj_from_kol(word_str):
    return word_str.replace(_KO_CGJ_MER_L, _KO_MER_L)


def _rm_misc(word_str):
    return word_str.translate(tt.TRANS_TABLE_TO_RM_MISC)


def _audited_tweak(tweak, word_str, io_audit, audit_label):
    new_word_str = tweak(word_str)
    if new_word_str != word_str:
        io_audit[audit_label] = word_str
    return new_word_str
