"""Exports get_lett_words, letters_and_maqafs, pre_slash"""

import re


def get_lett_words(words):
    """
    Returns a list of strings corresponding to the chars in the given sequence
    of dict-words. These strings are instance-qualified, if needed.
    E.g. rather than returning (1) below it will return (2)
        1: [str('חת'), str('חת')]
        2: [str('חת'), str('חת/2')]
    I.e. it will specify the instance number after a slash.
    The first instance is not specified, i.e. "/1" is implicit.
    """
    lett_words = []
    for word in words:
        lett_word = letters_and_maqafs(word["chars"])
        lett_word_new = lett_word
        instance = 1
        while lett_word_new in lett_words:
            instance += 1
            lett_word_new = lett_word + "/" + str(instance)
        lett_words.append(lett_word_new)
    return lett_words


def letters_and_maqafs(string: str):
    """Return only the letters and maqaf marks in the given string"""
    # I.e. strip any the vowel points and/or accents
    # Another approach would be to filter based on
    # unicodedata.category(char) == 'Lo'.
    pattern = r"[^א-ת־]*"
    return re.sub(pattern, "", string)


def pre_slash(string):
    """Return the part of the string before the slash"""
    return string.split("/")[0]
