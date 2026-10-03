import itertools
import yeivin_itm.content.my_yeivin_amisc_helpers_for_bibrefs as bibrefs
import yeivin_itm.content.my_yeivin_amisc_helpers_for_locales as loc
import py_html.legacy_html as aht_html


def add_center(attr):
    new_attr = attr or {}
    new_attr_class = new_attr.get("class") or ""
    new_attr["class"] = (new_attr_class + " center").strip()
    return new_attr


def mwrom(string: str, mwcap, as_str):
    """
    mw: multi-word
    rom: romanized
    Valid values for "mwcap":
        'mwcap-type-lower-case'
        'mwcap-type-sentence-case'
        'mwcap-type-title-case'
    """
    assert isinstance(string, str)
    if mwcap == "mwcap-type-title-case":
        words = string.split(" ")
        string = " ".join(word.capitalize() for word in words)
    elif mwcap == "mwcap-type-sentence-case":
        words = string.split(" ")
        string = " ".join([words[0].capitalize(), *words[1:]])
    else:
        assert mwcap == "mwcap-type-lower-case"
    if as_str:
        return string
    return aht_html.span_c(string, "romanized")


def numbered_section_heading(num_of_sec):
    return aht_html.heading_level_3(str(num_of_sec), {"id": id_of_numsec(num_of_sec)})


def insert_numsec_selflink(num_of_sec, contents_of_sec):
    new_htobj0 = _insert_numsec_selflink_2(num_of_sec, contents_of_sec[0])
    return new_htobj0, *contents_of_sec[1:]


def id_of_numsec(num_of_sec):
    zpns = f"{num_of_sec:03}"  # zero-padded number of section
    return f"ns{zpns}"


def syllables_generic(dash_sep_word):
    list_of_strs = dash_sep_word.split("-")
    accum = []
    for a, b in itertools.pairwise(list_of_strs):
        accum.append(_maybe_gfpog(a, b))
    accum.append([list_of_strs[-1]])
    return accum


def strip_syl_stuff(dash_sep_word):
    return dash_sep_word.translate(str.maketrans({"-": "", "_": ""}))


def syn(target_syl_count, dash_sep_word, ps="", pe=""):
    """ps: pad start; pe: pad end"""
    padded = ps + dash_sep_word + pe
    assert _sy_count(padded) == target_syl_count
    return padded


def hboloc_get_contents(contents):
    if isinstance(contents, str):
        return contents, None
    for_here = contents["hboloc-contents-for-here"]
    for_lob = contents["hboloc-contents-for-list-of-bibrefs"]
    return for_here, for_lob


def parts_with_hi(norm_star):
    normal_word, starred_word = norm_star
    assert normal_word == _strip_hi_stuff(starred_word)
    parts = starred_word.split("*")
    assert len(parts) == 3
    mid = _maybe_gfpog(parts[1], parts[2])
    return parts[0], _highlighted(mid), parts[2]


def make_ftnt_struct(secnum, ftnt_index, body):
    return {
        "ftnt-secnum": secnum,
        "ftnt-index": ftnt_index,
        "ftnt-callout": f"φ{ftnt_index+1}",  # phi is short for "footnote"
        "ftnt-body": body,
    }


def make_html_for_one_ftnt_body(ftnt_struct):
    ftnt_body = ftnt_struct["ftnt-body"]
    assert not isinstance(ftnt_body, dict)
    flat = aht_html.flatten_nn(ftnt_body)
    assert flat == ftnt_body
    if _is_paragraph(flat[0]):
        fb_spc = flat[0]["contents"]
        fb_rest = flat[1:]
    else:
        assert isinstance(flat[0], str) or _is_span(flat[0])
        fb_spc = flat  # fb_spc: footnote body start paragraph contents
        fb_rest = []  # fb_rest: footnote body rest
    the_id, the_href = _id_and_href("ftnt", ftnt_struct)
    label = aht_html.anchor(ftnt_struct["ftnt-callout"], {"href": the_href})
    start_para = aht_html.para([label, " ", *fb_spc])
    return aht_html.div([start_para, *fb_rest], {"id": the_id})


def make_html_for_ftnt_callout(ftnt_struct):
    callout_string = ftnt_struct["ftnt-callout"]
    the_id, the_href = _id_and_href("callout", ftnt_struct)
    return aht_html.anchor(callout_string, {"href": the_href, "id": the_id})


def hboloc_attr(xloc):
    #
    # xloc means one of the following three types of locale:
    #     a single locale (a sloc)
    #     a double locale (a dloc)
    #     an "and elsewhere" locale (an aeloc)
    #
    if pair_inside_dloc := loc.get_pair_inside_dloc(xloc):
        return {
            "data-bk-ch-vr": pair_inside_dloc[0],
            "data-bk-ch-vr-2": pair_inside_dloc[1],
            "title": bibrefs.title_for_dloc(*pair_inside_dloc),
        }
    if sloc_inside_aeloc := loc.get_sloc_inside_aeloc(xloc):
        return {
            "data-bk-ch-vr": sloc_inside_aeloc,
            "data-bk-ch-vr-is-aeloc": "is-aeloc-yes",
            "title": bibrefs.title_for_aeloc(sloc_inside_aeloc),
        }
    sloc = xloc
    assert loc.sloc_okay(sloc)
    # we check the slocs of a dloc upon construction of the dloc
    # we check the sloc of a aeloc upon construction of the aeloc
    # we check a plain sloc here because it has no constructor
    return {"data-bk-ch-vr": sloc, "title": bibrefs.title_for_sloc(sloc)}


##########  PRIVATE  ######################################################


def _is_paragraph(flat_0):
    if not aht_html.is_htel(flat_0):
        return False
    return aht_html.htel_deref_tag(flat_0) == "p"


def _is_span(flat_0):
    if not aht_html.is_htel(flat_0):
        return False
    return aht_html.htel_deref_tag(flat_0) == "span"


def _id_and_href(foo, ftnt_struct):
    the_id = _foo_id(foo, ftnt_struct)
    complement_dic = {"ftnt": "callout", "callout": "ftnt"}
    cfoo = complement_dic[foo]
    the_href = "#" + _foo_id(cfoo, ftnt_struct)
    return the_id, the_href


def _foo_id(foo, ftnt_struct):
    secnum = ftnt_struct["ftnt-secnum"]
    ftntnum = 1 + ftnt_struct["ftnt-index"]
    return f"sec-{secnum}-{foo}-{ftntnum}"


def _maybe_gfpog(parta, partb):
    if parta.endswith("_"):
        return [parta[:-1], _gfpog(partb[0])]
    return [parta]


def _sy_count(dash_sep_word):
    return len(dash_sep_word.split("-"))


def _highlighted(inner):
    return aht_html.span(inner, {"class": "highlighted"})


def _strip_hi_stuff(starred_word):
    return starred_word.translate(str.maketrans({"*": "", "_": ""}))


def _gfpog(inner):
    return aht_html.span(inner, {"class": "ghostly-first-part-of-geminate"})


def _insert_numsec_selflink_2(num_of_sec, htobj0):
    assert _is_paragraph(htobj0)
    new_contents0 = _insert_numsec_selflink_3(num_of_sec, htobj0.get("contents"))
    return aht_html.para(new_contents0, htobj0.get("attr"))


def _insert_numsec_selflink_3(num_of_sec, contents0):
    return _numsec_selflink(num_of_sec), " ", contents0


def _numsec_selflink(num_of_sec):
    id_of_sec = id_of_numsec(num_of_sec)
    attr = {"href": f"#{id_of_sec}"}
    return aht_html.anchor("#", attr)
