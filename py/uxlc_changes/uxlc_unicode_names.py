"""Exports name, names."""

import unicodedata

import uxlc_misc.my_unicode as my_unicode


def names(string):
    """
    Return a string with the space-separated the UXLC names
    for the Unicode code points in the given string.
    """
    names_list = list(map(name, string))
    return " ".join(names_list)


def name(string_len_1):
    """Return the UXLC name for the given Unicode code point."""
    my_un = my_unicode.name(string_len_1)
    # ndb: no dot below — strip the combining dot below (U+0323) so x → h,
    # robust to either normalization of the source name. E.g. etnaxta → etnahta.  # translit-ok: UXLC's own accent names
    my_un_ndb = unicodedata.normalize("NFD", my_un).replace(
        "\N{COMBINING DOT BELOW}", ""
    )
    my_un_ndb_fn = my_un_ndb.split("/")[0]  # first name in a slash seq
    # E.g., meteg/siluq becomes just meteg
    uxlc_un = _UXLC_UNS.get(my_un_ndb_fn) or my_un_ndb_fn
    return uxlc_un


_UXLC_UNS = {
    "zarqa-stress-helper": "zarqa",
    "segol-vowel": "segol",
    "holam-haser-for-vav": "holam-haser",
    "tsinor": "zinor",  # translit-ok: UXLC's own accent names
    "rafeh": "rafe",
}
