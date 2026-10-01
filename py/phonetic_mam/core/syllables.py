from itertools import pairwise
import re
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.udl_char_classes as cc
import phonetic_mam.core.extend_sylrecs as es


def get_syllables(eudlcw):
    # eudlcw: extended udlcw
    # udlcw: unambiguous-deeplat chanted word
    atoms_1 = _get_atoms_as_lists_of_sylrecs(eudlcw["eudlcw-udlcw"])
    atoms_2 = es.extend_sylrecs_with_fva_and_rep(
        atoms_1, eudlcw["eudlcw-fva"], eudlcw["eudlcw-repeated"]
    )
    return atoms_2


def _my_trans(string, trans_dic):
    trans_table = str.maketrans(trans_dic)
    return string.translate(trans_table)


def _ncg(inner):
    """Non-capturing group"""
    return f"(?:{inner})"


_IU_MF_CSS = "^U" + _ncg("c:") + "?"  # initial shuruq maybe followed by a "CSS"
_FFPP = r"[ḣẋ_]$"  # final furtive patax pair
_MISC_CSS = _ncg(
    "c$|c:c:α?$|c:α$|c:"
)  # misc. patterns involving a "CSS" or a final, naked consonant
_CVM_MF_MISC_CSS = r"cvm*" + _MISC_CSS + "?"  # cvm* maybe followed by _MISC_CSS
# CSS: consonant [with a] silent sheva
PATT_OF_A_SYLLABLE = _my_trans(
    _ncg("|".join((_IU_MF_CSS, _FFPP, _CVM_MF_MISC_CSS))),
    {
        "U": deeplat.SHURUQ,
        "c": cc.RE_CLS_UNAMB_CONSONANT,
        "v": cc.RE_CLS_UNAMB_VOWEL,
        "m": cc.RE_CLS_UNAMB_ML,
        ":": deeplat.SHEVA_NAX,
        "α": deeplat.ALEF_0MAPIQ_ML,
        "ḣ": deeplat.FPP_PATAX_MAPIQ_HE,
        "ẋ": deeplat.FPP_PATAX_XET,
        "_": deeplat.FPP_PATAX_AYIN,
    },
)


def _get_atoms_as_lists_of_sylrecs(udlcw):
    """
    Divide up the chanted word first by atoms and then by syllables.
    So, return a list of lists.
    The top-level list is a list of atoms.
    Each atom is a list of syllables.
    Syllables are returned as sylrecs (syllable records).
    The chanted word is given as an unambiguous-deeplat (udl) string.
    """
    atoms = deeplat.get_atoms(udlcw)
    return list(map(_get_sylrecs_for_atom, atoms))


def _get_sylrecs_for_atom(udl_str_for_atom):
    udl_strs_for_syllables = re.findall(PATT_OF_A_SYLLABLE, udl_str_for_atom)
    assert "".join(udl_strs_for_syllables) == udl_str_for_atom
    return _make_syllable_recs(udl_strs_for_syllables)


def _make_syllable_recs(udl_strs_for_syllables):
    sylrecs_out = list(map(_make_basic_sylrec, udl_strs_for_syllables))
    for sylrec_1, sylrec_2 in pairwise(sylrecs_out):
        sylrec2_udl_0 = sylrec_2["sylrec-udl"][0]
        if sylrec2_udl_0 in deeplat.GEMINATES:
            # swp1g: starts with part 1 [of a] geminate
            # swp2g: starts with part 2 [of a] geminate
            sylrec_1["sylrec-next-syl-swp1g"] = sylrec2_udl_0
            sylrec_2["sylrec-this-syl-swp2g"] = True
    return sylrecs_out


def _make_basic_sylrec(udl_str_for_syllable):
    return {
        "sylrec-udl": udl_str_for_syllable,
        "sylrec-he": deeplat.get_he_letters_back(udl_str_for_syllable),
    }
