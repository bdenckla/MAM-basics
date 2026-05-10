"""Exports add_plus_stuff"""

from mb_cmn import hebrew_verse_numerals as hvn
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
    out_section["header"] = _plus_header(section["header"])
    return out_section


def _plus_header(header):
    """Return a plus-format header with normalized header fields."""
    out_header = dict(header)
    sbns = header["sub_book_names"]
    if isinstance(sbns, dict):
        if len(sbns) == 0:
            out_header["sub_book_names"] = []
            out_header["chapter_counts"] = _plus_chapter_counts(header)
            return out_header
        assert len(sbns) == 1
        only_key = tuple(sbns.keys())[0]
        assert only_key == header["book24_name"]
        out_header["sub_book_names"] = sbns[only_key]
        out_header["chapter_counts"] = _plus_chapter_counts(header)
        return out_header
    assert isinstance(sbns, list)
    out_header["sub_book_names"] = sbns
    out_header["chapter_counts"] = _plus_chapter_counts(header)
    return out_header


def _plus_chapter_counts(header):
    chapter_counts = header["chapter_counts"]
    has_bk24_name = ["book24_name" in entry for entry in chapter_counts]
    out_counts = []
    if any(has_bk24_name):
        assert all(has_bk24_name)
        for entry in chapter_counts:
            assert entry["book24_name"] == header["book24_name"]
            out_entry = dict(entry)
            del out_entry["book24_name"]
            out_counts.append(out_entry)
        return out_counts
    assert not any(has_bk24_name)
    for entry in chapter_counts:
        out_counts.append(dict(entry))
    return out_counts


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
    # Source may use Hebrew numerals or numeric strings; plus uses numeric strings.
    for he_chnu, ch_contents in chapters.items():
        out_bk39["chapters"][_he_to_numeric_str_or_keep(he_chnu)] = _aps_to_chapter(
            ch_contents
        )
    return out_bk39


def _aps_to_chapter(chapter):
    """
    Add "plus stuff" (extras) to the "chapter" argument.
    The "chapter" argument is a dict that maps a psv_psn to a minirow.
    A psv_psn is a pseudo-verse pseudo-number (0, 1..N, תתת).
    In plus output, true verse numbers are numeric strings ("1", "2", ...).
    Pseudo-verses ("0", "תתת") are omitted.
    """
    out_chapter = {}
    # Can we get rid of this "for" loop?
    for he_psv_psn, minirow in chapter.items():
        if _is_truly_a_verse(he_psv_psn):
            minirow1 = _aps_to_minirow_phase_1(minirow)
            out_chapter[_he_to_numeric_str_or_keep(he_psv_psn)] = (
                _aps_to_minirow_phase_2(minirow1)
            )
    return out_chapter


def _he_to_numeric_str_or_keep(he_num):
    """Convert Hebrew numeral strings to numeric strings for plus output.

    If a key is already a numeric string (for example, "21"), keep it as-is.
    """
    if he_num in ("0", "תתת"):
        return he_num
    if he_num.isdigit():
        return he_num
    return str(hvn.STR_TO_INT_DIC[he_num])


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
    # Source chapters may be Hebrew numerals or numeric strings.
    last_he_chnu = tuple(chapters.keys())[-1]
    last_chapter = chapters[last_he_chnu]
    last_he_vrnu = tuple(last_chapter.keys())[-2]
    # Good endings are always wrapped in doc templates,
    # and they are the only thing in the CP of a triple-tav row
    # that is wrapped in a doc template.
    # Can we get rid of this "for" loop?
    for wtel in last_chapter["תתת"].CP:
        if wtp1.is_doc_template(wtel):
            return _make_good_ending_entry(
                _he_to_numeric_str_or_keep(last_he_chnu),
                _he_to_numeric_str_or_keep(last_he_vrnu),
                wtel,
            )
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
# The chapters key is assumed to point to a dict that maps a chapter key
# (numeric string in current output) to the contents of a chapter.
