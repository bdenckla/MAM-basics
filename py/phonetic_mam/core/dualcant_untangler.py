import re
import mb_cmn.hebrew_punctuation as hpu
import mb_cmn.hebrew_points as hpo
import phonetic_mam.core.distinguished as disting


def untangle(dtx, word):
    lookup_keys = dtx.get("dtx-untangler-lookup-keys", {})
    mamified_word = lookup_keys.get(word) or disting.to_generic_points(word)
    untanglers = dtx["dtx-dualcant-untanglers"]
    if otwords_for_aab := untanglers.get(mamified_word):  # aab alef and bet
        use_counts = dtx["dtx-out-dualcant-untanglers-use-counts"]
        use_counts[mamified_word] += 1
        otword_for_alef_wd = _impose_distinctions(word, otwords_for_aab[0])
        otword_for_bet_wd = _impose_distinctions(word, otwords_for_aab[1])
        utrec = {
            "utrec-mam-superimposed": mamified_word,
            "utrec-mam-alef": otword_for_alef_wd,
            "utrec-mam-bet": otword_for_bet_wd,
        }
        return utrec
    return None


def _impose_distinctions(word_with_d, otword_sans_d):
    clusters_wd = _split_into_clusters(word_with_d)
    clus_otword_sd = list(map(_split_into_clusters, otword_sans_d))
    clusters_sd = sum(clus_otword_sd, [])
    assert len(clusters_wd) == len(clusters_sd)
    clusters_id = list(map(_impose_on_clus, zip(clusters_wd, clusters_sd)))
    # id: [with] imposed distinctions
    idx = 0
    otword_with_d = []
    for clus_word_sd in clus_otword_sd:
        clus_word_len = len(clus_word_sd)
        clus_word_id = clusters_id[idx : idx + clus_word_len]
        str_word_id = "".join(clus_word_id)
        otword_with_d.append(str_word_id)
        idx += clus_word_len
    return otword_with_d


def _split_into_clusters(string):
    att = "א-ת"
    patclu_wm = f"[{att}{hpu.MAQ}]" + hpo.RE_APCV_STAR
    # pattern for a cluster with maqaf
    # Attach maqaf to its preceding letter rather than making it a cluster of its own!
    clusters = re.findall(patclu_wm, string)
    return clusters


def _impose_on_clus(cl_pair):
    cl_wd_in, cl_sd = cl_pair
    cl_wd_out = cl_sd
    if disting.DAGESH_XAZAQ in cl_wd_in:
        cl_wd_out = cl_wd_out.replace(hpo.DAGOMOSD, disting.DAGESH_XAZAQ)
    if disting.SHEVA_NA in cl_wd_in:
        cl_wd_out = cl_wd_out.replace(hpo.SHEVA, disting.SHEVA_NA)
    return cl_wd_out
