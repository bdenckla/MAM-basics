import re
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_letters as hl
import mb_cmn.uni_heb as uh

import phonetic_mam.core.bccvecs_that_are_known as knowns
import phonetic_mam.core.separate_accents as sepacc
import phonetic_mam.core.summary_of_accents as accsum
import phonetic_mam.core.dtx_struct as dtxs


def get_primary_stress(dtx, syls_per_atom, accar):
    """Locate primary stress, using one transient masora-circle marker.

    An existing circle that reaches the stress calculation fails the one-marker
    assertion rather than being silently interpreted as stress.
    """
    the_cantsys = dtxs.get_cantsys(dtx)
    lomlis, bccvec = sepacc.get_sepacc(the_cantsys, accar)
    if dtxs.include_in_edition_census(dtx):
        accsum.record_bccvec(dtx, the_cantsys, bccvec)
    bcc, marked = _mark_pristress_of_accar(the_cantsys, lomlis, bccvec)
    flat_list_of_sylrecs = sum(syls_per_atom, [])
    assert _sylrecs_add_to_accar_letters(flat_list_of_sylrecs, accar)
    circles = marked.count(hpu.MCIRC)
    assert circles == 1, f"{circles} masora circles in the marked ACCAR string, not 1"
    marked_syls = syllable_split(marked, flat_list_of_sylrecs)
    for idx, marked_syl in enumerate(marked_syls):
        if hpu.MCIRC in marked_syl:
            isps = idx
            isps_two_d = _find_isps_two_d(syls_per_atom, isps)
            return bcc, isps, isps_two_d
    assert False


def _find_isps_two_d(syls_per_atom, isps):
    flat_syl_idx = 0
    for atom_idx, syls in enumerate(syls_per_atom):
        for syl_idx, _syl in enumerate(syls):
            if flat_syl_idx == isps:
                return atom_idx, syl_idx
            flat_syl_idx += 1
    assert False


def _sylrecs_add_to_accar_letters(sylrecs, accar):
    he_strs = [sylrec["sylrec-he"] for sylrec in sylrecs]
    return "".join(he_strs) == hl.letters(accar)


def syllable_split(whole, sylrecs):
    """Split pointed Hebrew by each transient syllable's unpointed letters."""
    att = "א-ת"
    # Keep maqaf flavors attached to the preceding letter-led cluster.
    # This mirrors the old gray-maqaf-aware APCV behavior locally without
    # changing vendored mb_cmn regex definitions.
    recc_apcv_mq = f"{hpo.RECC_APCV}{hpu.MAQ}{hpu.NU_GMAQ}"
    patclu_wm = f"[{att}][{recc_apcv_mq}]*"
    clusters = re.findall(patclu_wm, whole)
    syllables_out = []
    clidx = 0
    for sylrec in sylrecs:
        sylrec_he = sylrec["sylrec-he"]
        syllables_out.append("")
        for sylrec_he_lett in sylrec_he:
            cluster = clusters[clidx]
            assert cluster[0] == sylrec_he_lett
            syllables_out[-1] += cluster
            clidx += 1
    return syllables_out


def _mark_type_i(n: int, lomlis):
    part_1 = lomlis[:n]
    part_2 = lomlis[n:]
    marked = "".join(part_1) + hpu.MCIRC + "".join(part_2)
    return marked


def _mark_pristress_of_accar(the_cantsys, lomlis, bccvec):
    gsi_from_bccvec = knowns.CS_GET_STRESS_INFO_FROM_BCCVEC[the_cantsys]
    stress_idx = gsi_from_bccvec.get(bccvec)
    assert stress_idx is not None, f"Unknown bccvec: {tuple(map(uh.shunna, bccvec))}"
    stress_bcc = bccvec[stress_idx]
    return stress_bcc, _mark_type_i(stress_idx, lomlis)
