import re

import mb_cmn.my_utils as my_utils
import mb_cmn.hebrew_punctuation as hpu
import phonetic_mam.core.stress as stress


def extend_sylrecs_with_fva_and_rep(atoms, fva, rep):
    atoms_fva = _atom_split(fva, len(atoms))
    atoms_rep = _atom_split(rep, len(atoms))
    atoms_2 = list(my_utils.szip(atoms, atoms_fva, atoms_rep))
    atoms_3 = list(map(_syllable_split, atoms_2))
    return atoms_3


def _syllable_split(atom):
    sylrecs_1, fva, rep = atom
    sylrecs_2 = _syllable_split_2(sylrecs_1, fva, "sylrec-fva")
    sylrecs_3 = _syllable_split_2(sylrecs_2, rep, "sylrec-rep")
    return sylrecs_3


def _syllable_split_2(sylrecs, fva_or_rep, sylrec_key):
    if fva_or_rep is None:
        reorganized = [None] * len(sylrecs)
    else:
        syllabified = my_utils.sl_map((_syllable_split_3, sylrecs), fva_or_rep)
        reorganized = list(my_utils.szip(*syllabified))
    extended = list(my_utils.szip(sylrecs, reorganized))
    new_sylrecs = my_utils.sl_map((_add_dic_item, sylrec_key), extended)
    return new_sylrecs


def _add_dic_item(sylrec_key, sylrec_and_fvaorep):
    sylrec, fva_or_rep = sylrec_and_fvaorep
    return {**sylrec, sylrec_key: fva_or_rep}


def _syllable_split_3(sylrecs, whole):
    return stress.syllable_split(whole, sylrecs)


def _atom_split(fva_or_rep, out_len):
    if fva_or_rep is None:
        return [None] * out_len
    atomized = tuple(map(_split_at_bog_maq, fva_or_rep))
    return list(my_utils.szip(*atomized))


def _split_at_bog_maq(string):
    maq_and_sp = hpu.MAQ + hpu.NU_GMAQ + " "
    parts = re.split(f"([{maq_and_sp}])", string)
    atoms = parts[0::2]
    atom_seps = parts[1::2]
    assert len(atoms) == 1 + len(atom_seps)
    return atoms
