import phonetic_mam.core.dualcant_arguments as gdc


def get_untanglers(aligned_cantillations):
    # sab: superimposed, alef, & bet
    sab_words, log = _get_sab_words(aligned_cantillations)
    sab_va_words = list(map(_add_vowar_and_accar_to_sab_word, sab_words))
    return sab_va_words, log


def _get_sab_words(aligned_cantillations):
    # sab_word: a word represented as a triple of superimposed, alef, & bet
    unique_sab_words = {}
    log = {"log-already_recorded": [], "log-does_not_vary": []}
    for ac_dic in aligned_cantillations:
        ac_triple = tuple(ac_dic.values())  # assumes dic is in the expected order
        for sab_word in zip(*ac_triple):
            super_word, alef_word, bet_word = sab_word
            hsuper_word = _hashable_super(super_word)
            if existing_sab_word := unique_sab_words.get(hsuper_word):
                assert sab_word == existing_sab_word
                log["log-already_recorded"].append(super_word)
            elif alef_word == bet_word:
                assert super_word == alef_word["word-simple"]
                log["log-does_not_vary"].append(super_word)
            else:
                unique_sab_words[hsuper_word] = sab_word
    return list(unique_sab_words.values()), log


def _hashable_super(obj):
    if isinstance(obj, str):
        return obj
    if gdc.is_dcargs_qamats(obj):
        return gdc.dcargs_qamats_dalet(obj)


def _add_vowar_and_accar_to_sab_word(sab_word):
    assert isinstance(sab_word, tuple) and len(sab_word) == 3
    return {
        "sab-word-cant-superimposed": sab_word[0],
        "sab-word-cant-alef": sab_word[1],
        "sab-word-cant-bet": sab_word[2],
    }
