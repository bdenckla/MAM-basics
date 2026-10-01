import re
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.resolve_common as pra
import phonetic_mam.core.resolve_generic as phi_pra


def resolve_ydys_ambiguities_in_adlcw(adlcw):
    """
    Resolve yDyS ambiguities in a chanted word.
    The chanted word is given as an ambiguous deeplat (adl) string.
    Ambiguities of the yDyS type are those that exist even
    when dagesh and sheva distinctions have already been made.
    These ambiguities include (but are not limited to):
       consonant vs. ML for א (alef)
       consonant vs. ML for ה (he)
       consonant vs. ML for י (yod)
       consonant vs. ML for ו (vav)
       furtive patax
       vowel-yod diphthongs
    """
    atoms = deeplat.get_atoms(adlcw)
    new_atoms = list(map(_res_ydys_amb_in_atom, atoms))
    return deeplat.BLACK_MAQAF.join(new_atoms)


def resolve_ndns_ambiguities_in_adlcw(adlcw):
    """
    Resolve ndns ambiguities in a chanted word.
    The chanted word is given as an ambiguous deeplat (adl) string.
    """
    atoms = deeplat.get_atoms(adlcw)
    new_atoms = list(map(phi_pra.res_ndns_amb_in_atom, atoms))
    return deeplat.BLACK_MAQAF.join(new_atoms)


def find_concerns(deeplat_str):
    atoms = deeplat_str.split(deeplat.BLACK_MAQAF)
    for atom in atoms:
        if con := pra.find_concerns_in_atom(atom):
            return con
    return None


def _res_ydys_amb_in_atom(deeplat_atom):
    """
    Resolve yDyS ambiguities in an atom.
    """
    out_dl_atom = deeplat_atom
    out_dl_atom = re.sub(pra.ALEF_ML_SHURUQ_PATT, pra.ALEF_ML_SHURUQ_REPL, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.ALEF_0MAPIQ_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.HE_0MAPIQ_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.YOD_0DAG_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = pra.yco_nco_sub(pra.VAV_0DAGOSD_PATTS_AND_REPLS, out_dl_atom)
    out_dl_atom = re.sub(pra.MISC_PATT, pra.misc_repl_fun, out_dl_atom)
    return out_dl_atom
