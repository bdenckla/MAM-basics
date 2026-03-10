"""
Exports:
    render
    map_over_verafs
"""

from pyrender import render_wikitext_handlers as handlers
from pyrender import render_wikitext_helpers as wt_help
from py_misc import verse_and_friends as vaf
from pycmn import my_utils

# renopts: options as to what the verse bodies should contain.
#     ro_cantillation:
#         'rv-cant-combined': combined cantillation (the default)
#         'rv-cant-alef': alef cantillation
#         'rv-cant-bet': bet cantillation
#         'rv-cant-all-three': all three of the above
#         There are 3 passages with dualcant phrases.
#         These 3 passages are Reuben, Ex Dec, & Deut Dec.
#             dualcant: dually (doubly) cantillated
#             Reuben: Gen 35:22
#             Ex Dec: Exodus Decalogue
#             Deut Dec: Deuteronomy Decalogue
#         Each dualcant phrase has an alef & bet cant as well as a combined cant.
#             For Reuben: alef=פשוטה & bet=מדרשית
#             For Decalogues: alef=taxton & bet=elyon


def render(bkid, books_mpp, renopts=None, io_renlog=None):
    """
    * bkid: book ID from my_locales
    * books_mpp: maps a book ID to parsed Wikitext book contents
    * renopts: see above
    * io_renlog: ?

    Given these inputs, this function returns a dict mapping a cvt to a verse body.

    * A cvt is a chapter and verse qualified by vtrad.
    * The verse body is a tuple of text elements.
    * A text element is either:
        * A string.
        * A dict with a '_ren_tag' key and 0 or more other keys.
    * The other keys of a dict text element often include a 'contents' key,
    holding a tuple of text elements.
    """
    verses = books_mpp[bkid]["verses_plus"]
    bbr = bkid, books_mpp, renopts
    return {
        bcvt: _render_minirow(bbr, bcvt, minirow, io_renlog)
        for bcvt, minirow in verses.items()
    }


def map_over_verafs(fun, verafs):
    """Map fun over verafs."""
    return my_utils.sl_map((_map_over_veraf, fun), verafs)


def _map_over_veraf(fun, veraf: vaf.VerseAndFriends):
    """
    Make a new veraf by mapping fun over the fields of the given veraf.
    """
    return veraf.map_over(fun)


def _render_minirow(bbr, bcvt, minirow, io_renlog=None):
    if minirow is None:  # possibly Joshua 21:36 & 21:37
        return vaf.VerseAndFriends(("\N{EM DASH}",), tuple(), tuple())
    bkid, books_mpp, renopts = bbr
    hctx = handlers.default_hctx(bcvt, renopts, io_renlog)
    ep_renseq = wt_help.render_wtseq(hctx, minirow.EP)
    ncp_renseq = wt_help.render_wtseq(handlers.col_c_hctx(hctx), minirow.next_CP)
    ge_renseq = wt_help.render_wtseq(hctx, _good_ending_wtseq(bkid, books_mpp, bcvt))
    return vaf.VerseAndFriends(ep_renseq, ncp_renseq, ge_renseq)


def _good_ending_wtseq(bkid, books_mpp, bcvt):
    good_ending = books_mpp[bkid]["good_ending_with_bcvt"]
    if good_ending and bcvt == good_ending["last_bcvt"]:
        wtel = good_ending["wikitext_element"]
        return (wtel,)
    return tuple()
