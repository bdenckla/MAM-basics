"""Exports read_and_parse."""

import py_wlc_json_and_unicode.wlc_utils as wlc_utils


def read_and_parse(in_path):
    parsed = {"header": [], "verses": []}
    with open(in_path, encoding="utf-8", newline="") as wlc_in_fp:
        for rawline in wlc_in_fp:
            line = rawline.rstrip()
            if line.startswith("#"):
                assert not parsed["verses"]
                parsed["header"].append(line)
            else:
                parsed_verse_line = _parse_verse_line(line)
                parsed["verses"].append(parsed_verse_line)
    return parsed


def _parse_verse_line(verse_line):
    space_sep_strs = verse_line.split(" ")
    bcv = space_sep_strs[0]
    word1s = space_sep_strs[1:]
    list_of_lists_of_veldics = list(map(_word1_to_veldics, word1s))
    veldics = _sum_of_lists(list_of_lists_of_veldics)
    for veldic in veldics:
        _validate_veldic(veldic)
    velsods = list(map(wlc_utils.veldic_to_velsod, veldics))
    return {"bcv": bcv, "vels": velsods}


def _sum_of_lists(lists):
    """Return the sum of lists."""
    accum = []
    for the_list in lists:
        accum.extend(the_list)
    return accum


def _validate_veldic(veldic):
    if wlc_utils.is_sam_pe_inun(veldic):
        return
    wn_dic = veldic
    word = wn_dic["word"]
    assert "]" not in word
    index_of_dash = word.find("-")
    assert index_of_dash in (-1, len(word) - 1)


def _word1_to_veldics(word1):
    # wn_dic: dict with keys "word" and "notes"
    # veldic: verse element dict (sam_pe_inun or wn_dic)
    wn_dic1 = {"word": word1, "notes": []}
    wn_dic2 = _extract_notes(wn_dic1)
    veldic = _distinguish_sam_pe_inun(wn_dic2)
    veldics = _isolate_atoms(veldic)
    return veldics


def _extract_notes(wn_dic):
    # wn_dic: dict with keys "word" and "notes"
    word = wn_dic["word"]
    if len(word) > 2 and word[-2] == "]":
        notes = wn_dic["notes"]
        new_notes = [word[-2:], *notes]
        new_wn_dic = {"word": word[:-2], "notes": new_notes}
        return _extract_notes(new_wn_dic)  # recurse
    return wn_dic


def _distinguish_sam_pe_inun(wn_dic):
    # wn_dic: dict with keys "word" and "notes"
    word = wn_dic["word"]
    if word in ("P", "S"):
        assert not wn_dic["notes"]
        return {"sam_pe_inun": word}
    if word == "N":
        assert wn_dic["notes"] == ["]8"]
        return {"sam_pe_inun": word}
    return wn_dic


def _isolate_atoms(veldic):
    # wn_dic: dict with keys "word" and "notes"
    if wlc_utils.is_sam_pe_inun(veldic):
        return [veldic]
    wn_dic = veldic
    word = wn_dic["word"]
    pre, sep, post = word.partition("-")
    assert pre != ""
    if post != "":
        assert sep == "-"
        assert pre != ""
        assert "-" not in pre
        pre_plus_sep = pre + sep
        wn_dic_for_pps = {"word": pre_plus_sep, "notes": []}
        wn_dic_for_post = {"word": post, "notes": wn_dic["notes"]}
        wn_dics_for_post = _isolate_atoms(wn_dic_for_post)  # recurse
        return [wn_dic_for_pps, *wn_dics_for_post]
    assert sep in ("", "-")
    return [wn_dic]
