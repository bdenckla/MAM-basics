from pycmn import my_utils
from pycmn import ws_tmpl1 as wtp1


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
            return isp[:-1]
        if isp[0] == "":
            return isp[1:]
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


_TEST_CASES_1 = (
    ("b", ("b",)),
    ("{{c}}", (("c",),)),
    ("b{{c}}", ("b", ("c",))),
    ("{{c}}d", (("c",), "d")),
    ("b{{c}}d", ("b", ("c",), "d")),
    ("a{{b{{c}}d}}e", ("a", ("b", ("c",), "d"), "e")),
    ("a{{b}}{{c}}{{d}}e", ("a", ("b",), ("c",), ("d",), "e")),
)
_TEST_CASE_2_2_INP = "A{{f|C{{g|c|d}}D|b}}B"
_TEST_CASE_2_2_OUT = [
    "A",
    {"tmpl": [["f"], ["C", {"tmpl": [["g"], ["c"], ["d"]]}, "D"], ["b"]]},
    "B",
]
_TEST_CASES_2 = (
    ("{{f|a|b}}", [{"tmpl": [["f"], ["a"], ["b"]]}]),
    (_TEST_CASE_2_2_INP, _TEST_CASE_2_2_OUT),
    ("{{C{{g}}|b}}", [{"tmpl": [["C", {"tmpl": [["g"]]}], ["b"]]}]),
    ("{{a|b|{{c|d}}}}", [{"tmpl": [["a"], ["b"], [{"tmpl": [["c"], ["d"]]}]]}]),
)


def _do_quick_test():
    for test_case in _TEST_CASES_1:
        inp = test_case[0]
        act_out = _dcs_to_tuples(inp)
        print(f"input: {inp} output: {act_out}")
        exp_out = test_case[1]
        assert act_out == exp_out
    for test_case in _TEST_CASES_2:
        inp = test_case[0]
        act_out = parse(inp)
        print(f"input: {inp} output: {act_out}")
        exp_out = test_case[1]
        assert act_out == exp_out


if __name__ == "__main__":
    _do_quick_test()
