"""Exports name, names."""

from wlc_cmn import legacy_names

# Precomposed het forms (U+1E25 / U+1E24), built from \N{...} names so this
# source stays plain ASCII.  Used to strip het from vendored accent names
# down to the ASCII 'h'/'H' the UXLC name table keys on.
H_LOWER = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"
H_UPPER = "\N{LATIN CAPITAL LETTER H WITH DOT BELOW}"


def names(string):
    """
    Return a string with the space-separated the UXLC names
    for the Unicode code points in the given string.
    """
    names_list = list(map(name, string))
    return " ".join(names_list)


def name(string_len_1):
    """Return the UXLC name for the given Unicode code point."""
    my_un = legacy_names.legacy_name(string_len_1)
    # ndb: no dot below.  legacy_name draws accent names from the vendored
    # mb_diff_mpu.describe_diff, which now spells het PRECOMPOSED (a single
    # codepoint, U+1E25) -- matching the rest of this repo (issue #49).  The
    # UXLC names we resolve against are plain ASCII, so strip the precomposed
    # het to ASCII 'h' (and its capital to 'H').  E.g. etnaxta (vendored form,
    # with a precomposed het) becomes just etnahta.  # translit-ok: illustrates UXLC output
    my_un_ndb = my_un.replace(H_LOWER, "h").replace(H_UPPER, "H")
    my_un_ndb_fn = my_un_ndb.split("/")[0]  # first name in a slash seq
    # E.g., meteg/siluq becomes just meteg
    uxlc_un = _UXLC_UNS.get(my_un_ndb_fn) or my_un_ndb_fn
    return uxlc_un


_UXLC_UNS = {
    "zarqa-stress-helper": "zarqa",
    "segol-vowel": "segol",
    "holam-haser-for-vav": "holam-haser",
    "tsinor": "zinor",  # translit-ok: UXLC name
    "rafeh": "rafe",
}
