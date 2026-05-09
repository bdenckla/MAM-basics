"""Exports add_plus_stuff"""

from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import ws_tmpl1 as wtp1
from mpplus import mpplus_scrdfftar
from mpplus import mpplus_slh_words
from mpplus import mpplus_boring_tmpls
from mb_cmn.minirow import Minirow


def add_plus_stuff(section):
    """
    Add "plus stuff" (extras) to the "section" argument.
    Also remove some stuff.
    See note on add_plus_stuff below.
    """
    out_section = dict(section)
    out_section["book39s"] = []
    # Can we get rid of this "for" loop?
    # Search for ^[^#]*\bfor\b.*[:]$
    for bk39 in section["book39s"]:
        out_section["book39s"].append(_aps_to_bk39(bk39))
    out_section["header"] = section["header"]
    return out_section


def _aps_to_bk39(bk39):
    """
    Add "plus stuff" (extras) to the "bk39" argument.
    See note on _aps_to_bk39 below.
    """
    out_bk39 = dict(bk39)
    # We delete 'chapters' because we want 'good_ending_plus' to come before it.
    del out_bk39["chapters"]
    assert "good_ending_plus" not in bk39
    chapters = bk39["chapters"]
    out_bk39["good_ending_plus"] = _good_ending(chapters)
    out_bk39["chapters"] = {}
    # Can we get rid of this "for" loop?
    # Chapter numbers are now integers (from CSV conversion in Phase 1)
    for chnu, ch_contents in chapters.items():
        out_bk39["chapters"][chnu] = _aps_to_chapter(ch_contents)
    return out_bk39


def _aps_to_chapter(chapter):
    """
    Add "plus stuff" (extras) to the "chapter" argument.
    The "chapter" argument is a dict that maps a psv_psn to a minirow.
    A psv_psn is a pseudo-verse pseudo-number (0, 1..N, תתת).
    Verse numbers are integers; pseudo-verses are strings (0, תתת).
    """
    out_chapter = {}
    # Can we get rid of this "for" loop?
    for psv_psn, minirow in chapter.items():
        if _is_truly_a_verse(psv_psn):
            minirow1 = _aps_to_minirow_phase_1(minirow)
            out_chapter[psv_psn] = _aps_to_minirow_phase_2(minirow1)
    return out_chapter


def _aps_to_minirow_phase_1(minirow):
    return Minirow(
        _aps_to_cell_x(minirow.CP),
        _aps_to_cell_x(minirow.DP),
        _aps_to_cell_x(minirow.EP),
    )


def _aps_to_cell_x(cell_x):
    return _rm_misc_fr_wtseq(wtp.use_tmpl2_in_wtseq(cell_x))


def _rm_misc_fr_wtseq(wtseq):
    filtered = filter(_is_a_keeper, wtseq)
    return tuple(map(_rm_double_slash, filtered))


def _is_a_keeper(wtel):
    return not wtp1.is_abtag(wtel) and wtel != "//"


def _rm_double_slash(wtel):
    # Below, we don't have to worry about http:// & https://
    # because these never occur at top level
    # and we're only operating at top level here.
    return wtel.replace("//", "") if isinstance(wtel, str) else wtel


def _aps_to_minirow_phase_2(minirow):
    """
    Add "plus stuff" to the minirow argument,
    returning an mre (minirow, extended [version]).
    See note on _aps_to_minirow below.
    """
    new_cp = mpplus_scrdfftar.add(minirow.CP)  # we also do this to EP
    new_cp = mpplus_boring_tmpls.evaluate(new_cp)  # we also do this to EP
    #
    new_dp = _drop_uninteresting_dp(minirow.DP)
    #
    new_ep = mpplus_scrdfftar.add(minirow.EP)  # we also do this to CP
    new_ep = mpplus_slh_words.mark(new_ep)
    new_ep = mpplus_boring_tmpls.evaluate(new_ep)  # we also do this to CP
    return new_cp, new_dp, new_ep


def _drop_uninteresting_dp(minirow_dp):
    assert len(minirow_dp) == 1
    dp0 = minirow_dp[0]
    is_pasuq = wtp.is_template_with_name(dp0, "מ:פסוק")
    if is_pasuq and wtp.template_len(dp0) == 4:
        return tuple()
    return minirow_dp


def _make_good_ending_entry(chnu_str, vrnu_str, wtel):
    # Store chapter and verse as numeric strings to match JSON format
    return {
        "last_chapnver": [chnu_str, vrnu_str],
        "wikitext_element": wtp.use_tmpl2(wtel),
    }


def _good_ending(chapters):
    # Chapter and verse numbers are now numeric strings (from CSV conversion in Phase 1)
    last_chnu = tuple(chapters.keys())[-1]
    last_chapter = chapters[last_chnu]
    last_vrnu = tuple(last_chapter.keys())[-2]
    # Good endings are always wrapped in doc templates,
    # and they are the only thing in the CP of a triple-tav row
    # that is wrapped in a doc template.
    # Can we get rid of this "for" loop?
    for wtel in last_chapter["תתת"].CP:
        if wtp1.is_doc_template(wtel):
            return _make_good_ending_entry(last_chnu, last_vrnu, wtel)
    return None


def _is_truly_a_verse(psv_psn):
    return psv_psn not in ("0", "תתת")


###########################################################
# Note on add_plus_stuff
#
# The "section" argument is assumed to be a dict
# with only a "body" key assumed present.
# Any other keys (and the values they point to) are preserved.
#
# The "body" key is assumed to point to a list of bk39s.
#
# Currently, adding "plus stuff" consists of the following:
#
#     * Adding a good_ending key to the bk39 header.
#     * Adding a targeted version of each scrdff note.
#     * Marking each slh word.
#       (slh word: a word with small, large, and/or hung letters.)
#     * turning each "classic"-style template into a new-style template
#       (classic has only a list of elements; new separates name from args)
#
# In addition to adding the stuff described above,
# the following stuff is removed:
#
#     * abtags (Wikitext angle-bracket tags, i.e. XML tags)
#     * // (double forward slash) strings
#     * uninteresting calls to the מ:פסוק template
#     * 0 (zero) and תתת (triple-tav) pseudo-verses

###########################################################
# Note on _aps_to_bk39
#
# The bk39 argument is assumed to be a dict
# with only the following 3 keys assumed present:
#     book_name
#     sub_book_name
#     chapters
#
# A good_ending key is assumed to be absent from bk39.
# A good_ending key is added to the output, out_bk39.
#
# Any other keys in bk39 (and the values they point to) are preserved.
#
# The chapters key is assumed to point to a dict that maps a Hebrew
# chapter numeral to the contents of a chapter.
