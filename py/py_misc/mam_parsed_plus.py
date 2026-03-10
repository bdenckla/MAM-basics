""" Exports add_plus_stuff """

from pycmn import hebrew_verse_numerals as hvn
from pycmn import ws_tmpl2 as wtp
from pycmn import ws_tmpl1 as wtp1
from pympp import mpp_scrdfftar
from pympp import mpp_slh_words
from pympp import mpp_boring_tmpls
from pycmn.minirow import Minirow


def add_plus_stuff(section):
    """
    Add "plus stuff" (extras) to the "section" argument.
    Also remove some stuff.
    See note on add_plus_stuff below.
    """
    out_section = dict(section)
    out_section["book39s"] = []
    # Above, to allow mutation, we create a singleton list.
    # Its first and only element is, initially, None.
    # Can we get rid of this "for" loop?
    # Search for ^[^#]*\bfor\b.*[:]$
    for bk39 in section["book39s"]:
        out_section["book39s"].append(_aps_to_bk39(bk39))
    out_section["header"] = _add_he_to_int(
        section["header"], out_section["book39s"]
    )
    return out_section


def _add_he_to_int(header, book39s):
    """
    Add a "he_to_int" mapping to the header. This allows consumers to
    navigate chapters and verses using integer keys without needing to
    "know" Hebrew numerals.
    The mapping is built from the Hebrew-numeral keys that actually appear
    as chapter or verse keys in the data.
    """
    he_keys = set()
    for bk39 in book39s:
        for he_chnu, ch_contents in bk39["chapters"].items():
            he_keys.add(he_chnu)
            for he_vrnu in ch_contents:
                he_keys.add(he_vrnu)
    he_to_int = {he: hvn.STR_TO_INT_DIC[he] for he in sorted(he_keys, key=hvn.STR_TO_INT_DIC.get)}
    out_header = dict(header)
    out_header["he_to_int"] = he_to_int
    return out_header


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
    for he_chnu, ch_contents in chapters.items():
        out_bk39["chapters"][he_chnu] = _aps_to_chapter(ch_contents)
    return out_bk39


def _aps_to_chapter(chapter):
    """
    Add "plus stuff" (extras) to the "chapter" argument.
    The "chapter" argument is a dict that maps a psv_psn to a minirow.
    A psv_psn is a pseudo-verse pseudo-number (0, 1..N, תתת).
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
    new_cp = mpp_scrdfftar.add(minirow.CP)  # we also do this to EP
    new_cp = mpp_boring_tmpls.evaluate(new_cp)  # we also do this to EP
    #
    new_dp = _drop_uninteresting_dp(minirow.DP)
    #
    new_ep = mpp_scrdfftar.add(minirow.EP)  # we also do this to CP
    new_ep = mpp_slh_words.mark(new_ep)
    new_ep = mpp_boring_tmpls.evaluate(new_ep)  # we also do this to CP
    return new_cp, new_dp, new_ep


def _drop_uninteresting_dp(minirow_dp):
    assert len(minirow_dp) == 1
    dp0 = minirow_dp[0]
    is_pasuq = wtp.is_template_with_name(dp0, "מ:פסוק")
    if is_pasuq and wtp.template_len(dp0) == 4:
        return tuple()
    return minirow_dp


def _make_good_ending_entry(he_chnu, he_vrnu, wtel):
    return {
        "last_chapnver": [he_chnu, he_vrnu],
        "wikitext_element": wtp.use_tmpl2(wtel),
    }


def _good_ending(chapters):
    last_he_chnu = tuple(chapters.keys())[-1]
    last_chapter = chapters[last_he_chnu]
    last_he_vrnu = tuple(last_chapter.keys())[-2]
    # Good endings are always wrapped in doc templates,
    # and they are the only thing in the CP of a triple-tav row
    # that is wrapped in a doc template.
    # Can we get rid of this "for" loop?
    for wtel in last_chapter["תתת"].CP:
        if wtp1.is_doc_template(wtel):
            return _make_good_ending_entry(last_he_chnu, last_he_vrnu, wtel)
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
