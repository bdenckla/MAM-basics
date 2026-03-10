from pycmn import bib_locales as tbn
from py_misc import wt_qere
from pycmn.my_utils import first_and_only_and_str


def find_fois_wt(mroge):
    """Find poetic verses of different lengths (as measured in number of chanted words)."""
    # mroge: minirow or good ending
    #
    # Note that this is currently the only find_fois_wt ("find FOIs" [function for] Wikitext)
    # that does not use my_foi_wikitext_helpers (usually imported by the alias "fwh").
    #
    if not tbn.is_poetcant(mroge["mroge-bcvt"]):
        return []
    verse = wt_qere.get_verse_as_wordstrs(_HANDLERS, mroge)
    word_count = len(verse)
    word_count_str = f"{word_count:02}"
    foi_path = "poetic-verlen", word_count_str
    foi_target = " ".join(verse)
    return [(foi_path, foi_target)]


_HANDLERS = {
    **wt_qere.HANDLERS,
    "מ:דחי": wt_qere.hnd_recurse_on_arg_0,
    "מ:צינור": wt_qere.hnd_recurse_on_arg_0,
    "מ:קמץ": wt_qere.hnd_recurse_on_param_dalet,  # See below
    "מ:פסק": wt_qere.hnd_return_plain_space,
}
# I think in one case, the arguments to a מ:קמץ call vary
# in the number of chanted words within!
#
# One of the arguments is a maqaf compound, whereas the other
# is two space separated atoms!
#
# So, technically, it is an oversimplification, to just take
# arg 0.
#
# We can "excuse" this by saying that this FOI reports the
# poetic verse lengths of the dalet (ד) variant.
#
# (The dalet variant is in arg0 of each מ:קמץ call.)
