""" Exports analyze_dalsam """

import re

from pycmn import ws_tmpl2 as wtp
from pyrender import render_element as renel
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pycmn import my_utils


def analyze_dalsam(dalsam):
    """
    Analyze dalet and samekh.
    Return a dict like this: {
        'dsa-dal-endpunc': seq of renobjs or seq of wtobjs,
        'dsa-sam-endpunc': seq of renobjs or seq of wtobjs,
        'dsa-undisputed-prefix': seq of strs,
        'dsa-undisputed-suffix': seq of strs,
        'dsa-disputed-part': (dalsep, samsep, accent, m2_lett, m3_zmnl)
    }
    where:
    The dalsep part is dalet separated by its qqs.
    The samsep part is samekh separated at the same indices as dalsep.
    The accent part is the accent, if any, on the disputed qamats.
    A renobj is either a str or a renel, which is a dict.
    A wtobj is either a str or a template, which is a dict.
    """
    dalseq, samseq = dalsam
    dal_main, dal_endpunc = _dal_main_and_endpunc(dalseq)
    sam_main, sam_endpunc = _sam_main_and_endpunc(samseq)
    assert isinstance(dal_main, str)
    assert isinstance(sam_main, str)
    out = {
        "dsa-dal-endpunc": dal_endpunc,
        "dsa-sam-endpunc": sam_endpunc,
        "dsa-undisputed-prefix": tuple(),
        "dsa-undisputed-suffix": tuple(),
    }
    if dal_main.count(hpo.QAMATS_Q) == 1:
        out["dsa-disputed-part"] = _analyze_disputed_part(dal_main, sam_main)
        return out
    dalatoms = _atoms_with_trailing_maqaf(dal_main)
    samatoms = _atoms_with_trailing_maqaf(sam_main)
    found = False
    for dalatom, samatom in my_utils.szip(dalatoms, samatoms):
        if dalatom != samatom:
            assert not found
            found = True
            out["dsa-disputed-part"] = _analyze_disputed_part(dalatom, samatom)
            continue
        key = "dsa-undisputed-suffix" if found else "dsa-undisputed-prefix"
        # Below, we could just as well have used samatom instead of dalatom
        # since at this point in the code, they are equal.
        out[key] += (dalatom,)
    return out


def _dal_main_and_endpunc(dalseq):
    if isinstance(dalseq[0], str):
        dalseq_2 = dalseq
    else:
        assert len(dalseq) == 1
        dalseq_2 = _first_arg_of_dexi_or_tsinnor(dalseq[0])
    if len(dalseq_2) > 1:
        assert len(dalseq_2) == 2
        tmpl_or_renel = dalseq_2[1]
        assert _is_rim_or_tgm(tmpl_or_renel)
        # aka gray maqaf, aka מקף אפור
        return dalseq_2[0], [dalseq_2[1]]
    return dalseq_2[0], []


def _is_rim_or_tgm(obj):
    """rim: renel for implicit maqaf; tgm: tmpl for gray maqaf"""
    if renel.obj_is_ren_el(obj):
        return renel.get_ren_el_tag(obj) == "mam-implicit-maqaf"
    return wtp.is_template_with_name(obj, "מ:מקף אפור")


def _first_arg_of_dexi_or_tsinnor(obj):
    if renel.obj_is_ren_el(obj):
        assert renel.get_ren_el_tag(obj) == "mam-implicit-maqaf"
    wtel = obj
    assert wtp.is_template_with_name_in(wtel, ("מ:דחי", "מ:צינור"))
    return wtp.template_element(wtel, 1)


def _sam_main_and_endpunc(samseq):
    if isinstance(samseq[0], str):
        samseq_2 = samseq
    else:
        assert len(samseq) == 1
        samseq_2 = _first_arg_of_dexi_or_tsinnor(samseq[0])
    assert len(samseq_2) == 1
    samseq_2_0 = samseq_2[0]
    assert isinstance(samseq_2_0, str)
    if samseq_2_0.endswith(" "):
        return samseq_2_0[:-1], [" "]
    return samseq_2_0, []


def _full_partition_by_qq(string):
    """
    Separate string into its parts between qqs.
    E.g.:
        Return ('a',)          for a string 'a'.
        Return ('a', 'b')      for a string 'a' + qq + 'b'.
        Return ('a', 'b', 'c') for a string 'a' + qq + 'b' + qq + 'c'.
    """
    pre, qamqat, post = string.partition(hpo.QAMATS_Q)
    if qamqat:
        out = pre, qamqat, *_full_partition_by_qq(post)
        assert "".join(out) == string
        return out
    return (pre,)


def _atoms_with_trailing_maqaf(string):
    """
    Separate string into its atoms,
    where nonfinal atoms have trailing maqaf marks.
    """
    pre, maq, post = string.partition(hpu.MAQ)
    if maq:
        out = pre + maq, *_atoms_with_trailing_maqaf(post)
        assert "".join(out) == string
        return out
    return (pre,)


def _analyze_disputed_part(dalet, samekh):
    """Separate dalet by its qqs, and separate samekh similarly."""
    dalsep = _full_partition_by_qq(dalet)
    assert len(dalsep) in (3, 5)
    samsep = _similarly_separate(dalsep, samekh)
    assert dalsep[0] == samsep[0]
    assert dalsep[1] == hpo.QAMATS_Q and samsep[1] == hpo.QAMATS
    assert dalsep[2:] == samsep[2:]
    return dalsep, samsep, *_get_accent_if_any("".join(dalsep[2:]))


_ZMNL = "([^א-ת]*)"  # zero or more non-letters
_DOTQ = f"[{hpo.SHIND+hpo.SIND}]?"
_LETT = f"([א-ת]{_DOTQ})"  # a letter and maybe a shin dot or a sin dot
_REST = "(.*)"


def _get_accent_if_any(str_a_dqq):  # string after disputed qamats qatan
    match = re.fullmatch(_ZMNL + _LETT + _ZMNL + _REST, str_a_dqq)
    assert match is not None
    m1_zmnl, m2_lett, m3_zmnl, m4_rest = match.groups()
    accent = m1_zmnl or None
    if accent:
        assert accent in {ha.GER_M, hpo.MTGOSLQ, ha.MER, ha.MUN}
    else:
        assert m4_rest  # See note on postpositive below
    return accent, m2_lett, m3_zmnl


# Note on postpositive
######################
# At this point, we know that the code point after the disputed qamats
# qatan (dqq) is a letter, not an accent. But, the syllable
# with the dqq might still be stressed, if:
#
#    This letter closes that syllable.
#    This letter is atom-final.
#    This letter has a postpositive accent.
#    That accent indicates stress, i.e. this atom has no stress helper.
#
# In the code above, we are able to rule out this situation merely using
# the atom-final requirement.  I.e., it just so happens that a letter after
# an unstressed dqq is never final.


def _similarly_separate(dalsep, samekh: str):
    lengths = map(len, dalsep)
    samsep = tuple()
    start = 0
    for length in lengths:
        stop = start + length
        samsep = *samsep, samekh[start:stop]
        start = stop
    return samsep
