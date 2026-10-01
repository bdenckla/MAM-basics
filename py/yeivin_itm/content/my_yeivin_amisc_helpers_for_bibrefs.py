import yeivin_itm.content.my_yeivin_amisc_traverse as tra
import yeivin_itm.content.my_yeivin_amisc_helpers_for_locales as loc
import py_html.legacy_html as aht_html
import mb_cmn.my_utils as my_utils

_ISE_RECORDS = {
    "@Dt 5:22": "5:18 or 19",  # 5:18 in MAM
    "@Jer 31:19": "31:18",  # 31:18 in MAM
    "@Jer 31:20": "31:19",  # 31:19 in MAM
    "@Jer 31:26": "31:25",  # 31:25 in MAM
    "@Jer 31:33": "31:32",  # 31:32 in MAM
}
_ISE_QUAL = "in some editions; others have it as"


def title_for_sloc(sloc):
    sloc_s = strip_at_sign_prefix(sloc)
    if alt := _ISE_RECORDS.get(sloc):
        return f"{sloc_s} {_ISE_QUAL} {alt}"
    return sloc_s


def title_for_dloc(sloc_1, sloc_2):
    assert sloc_1 not in _ISE_RECORDS
    assert sloc_2 not in _ISE_RECORDS
    sloc_1_s = strip_at_sign_prefix(sloc_1)
    sloc_2_s = strip_at_sign_prefix(sloc_2)
    return f"{sloc_1_s} and {sloc_2_s}"


def title_for_aeloc(sloc):
    assert sloc not in _ISE_RECORDS
    sloc_s = strip_at_sign_prefix(sloc)
    return f"{sloc_s} and elsewhere"


def make_html_for_bibrefs(contents_of_sec):
    tag_handlers = {"bdi": _find_bibrefs_in_htel}
    bibrefs_found = tra.traverse_html(tag_handlers, contents_of_sec)
    if not bibrefs_found:
        return []
    bibrefs_found = _get_uniques(bibrefs_found)
    html_for_bibrefs = list(map(_make_html_for_bibref, bibrefs_found))
    html_for_bibrefs = my_utils.intersperse([", "], html_for_bibrefs)
    html_for_bibrefs = my_utils.sum_of_seqs(html_for_bibrefs)
    ref_or_refs = "references" if len(bibrefs_found) > 1 else "reference"
    intro = f"Biblical {ref_or_refs} in this section: "
    return (aht_html.horizontal_rule(), aht_html.para([intro, *html_for_bibrefs, "."]))


def strip_at_sign_prefix(sloc):
    assert isinstance(sloc, str)
    assert sloc[0] == "@"
    return sloc[1:]


def _find_bibrefs_in_htel(htel):
    if attr := htel.get("attr"):
        if sloc1 := attr.get("data-bk-ch-vr"):
            if sloc2 := attr.get("data-bk-ch-vr-2"):
                dloc = loc.make_dloc(sloc1, sloc2)
                return [(dloc, htel)]
            elif is_aeloc := attr.get("data-bk-ch-vr-is-aeloc"):
                assert is_aeloc == "is-aeloc-yes"
                aeloc = loc.make_aeloc(sloc1)
                return [(aeloc, htel)]
            return [(sloc1, htel)]
    return []


def _get_uniques(bibrefs):
    the_dic = {str(_important(br)): br for br in bibrefs}
    return list(the_dic.values())


def _important(bibref):
    # Get the important parts of a bibref, i.e. the parts
    # we consider to make it unique or not
    # (to decide whether it is a duplicate)
    xloc, htel = bibref
    if contents_for_lob := htel["attr"].get("data-contents-for-list-of-bibrefs"):
        cfl = contents_for_lob
    else:
        contents = htel["contents"]
        assert isinstance(contents, (list, tuple))
        assert len(contents) == 1
        cfl = contents[0]
    return xloc, cfl


def _make_html_for_bibref(bibref):
    xloc, htel = bibref
    if pair_inside_dloc := loc.get_pair_inside_dloc(xloc):
        string_for_xloc = title_for_dloc(*pair_inside_dloc)
    elif sloc_inside_aeloc := loc.get_sloc_inside_aeloc(xloc):
        string_for_xloc = title_for_aeloc(sloc_inside_aeloc)
    else:
        string_for_xloc = title_for_sloc(xloc)
    if contents_for_lob := htel["attr"].get("data-contents-for-list-of-bibrefs"):
        htel_for_lob = aht_html.bdi(contents_for_lob, htel["attr"])
    else:
        htel_for_lob = htel
    return [htel_for_lob, " ", aht_html.bdi(string_for_xloc)]
