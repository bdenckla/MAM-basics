from mb_cmn import my_utils
from mb_cmn import ws_tmpl1 as wtp1


def parse(string):
    """Parse the wikitext in string"""
    assert "'''" not in string, (string, _USE_MUDGASH_TMPL)
    return _argsep(_dcs_to_tuples(string))


def _dcs_to_tuples(string):
    # dcs: double-curlies, i.e. templates set off by
    # double opening curly brackets &
    # double closing curly brackets.
    doc = string.find("{{")  # doc: double opening curlies
    if doc == -1:
        return tuple() if string == "" else (string,)
    dcc = _find_closing(string, doc + 2)  # dcc: double closing curlies
    pre = _dcs_to_tuples(string[:doc])
    mid = _dcs_to_tuples(string[doc + 2 : dcc])
    post = _dcs_to_tuples(string[dcc + 2 :])
    return *pre, mid, *post


def _find_closing(string, idx):
    doc = string.find("{{", idx)  # doc: double opening curlies
    dcc = string.find("}}", idx)  # dcc: double closing curlies
    assert dcc != -1
    if doc != -1 and doc < dcc:
        dcc2 = _find_closing(string, doc + 2)
        return _find_closing(string, dcc2 + 2)
    return dcc


def _argsep(els):
    none_sep = _bars_to_none(els)
    gathered = _gather_elements_btwn_nones(none_sep)
    return my_utils.first_and_only(gathered)


def _bars_to_none(els):
    mapped = map(_bars_to_none_one_el, els)
    return my_utils.sum_of_tuples(mapped)


def _bars_to_none_one_el(element):
    if isinstance(element, str):
        args = tuple(element.split("|"))
        isp = my_utils.intersperse(None, args)
        if isp[-1] == "":
            isp = isp[:-1]
        if isp and isp[0] == "":
            isp = isp[1:]
        return isp
    assert isinstance(element, tuple)
    return ({"bars-to-none": _bars_to_none(element)},)


def _gather_elements_btwn_nones(els):
    out = [[]]
    for element in els:
        if element is None:
            out.append([])
            continue
        out[-1].append(_none_helper(element))
    return out


def _none_helper(element):
    if isinstance(element, str):
        return element
    return wtp1.mktmpl(_gather_elements_btwn_nones(element["bars-to-none"]))


# Below, I do "x" + "y" rather than "xy" just to avoid some BiDi display problems in my editor
_USE_MUDGASH_TMPL = "Use {{מודגש|אאא}} not " + "''''אאא'''"
