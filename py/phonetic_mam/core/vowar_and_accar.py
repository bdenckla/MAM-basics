import phonetic_mam.core.trans_tables as tt


def vowar_and_accar(word_str):
    vowels_and_related = word_str.translate(tt.TRANS_TABLE_TO_RM_ACCENTS_AR)
    accents_and_related = word_str.translate(tt.TRANS_TABLE_TO_RM_VOWELS_AR)
    assert " " not in word_str
    assert " " not in vowels_and_related
    assert " " not in accents_and_related
    return vowels_and_related, accents_and_related


def remove_both_vowar_and_accar(word_str):
    stripped = word_str
    stripped = stripped.translate(tt.TRANS_TABLE_TO_RM_ACCENTS_AR)
    stripped = stripped.translate(tt.TRANS_TABLE_TO_RM_VOWELS_AR)
    return stripped
