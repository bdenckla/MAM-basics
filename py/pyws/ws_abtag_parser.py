from pycmn import ws_tmpl1 as wtp1


def parse(strs_and_tmpls):
    return _smt(_parse_str_or_tmpl, strs_and_tmpls)


def _smt(mapfn, mapels):
    return sum(map(mapfn, mapels), tuple())


def _parse_str_or_tmpl(wikitext_element):
    if isinstance(wikitext_element, dict):
        assert wtp1.is_template(wikitext_element)
        return (wikitext_element,)
    assert isinstance(wikitext_element, str)
    plainstr = wikitext_element
    if _has_lt_and_then_a_known_abtag(plainstr):
        return _parse_tagful_str(plainstr)
    return (wikitext_element,)


_KNOWN_WTABTAGS = (
    "קטע" + " ",
    "noinclude",
    "/noinclude",
    "references/",
)


def _has_lt_and_then_a_known_abtag(plainstr):
    for known_abtag in _KNOWN_WTABTAGS:
        ltkt = "<" + known_abtag
        if ltkt in plainstr:
            return True
    return False


def _startswith_a_known_abtag(plainstr):
    for known_abtag in _KNOWN_WTABTAGS:
        if plainstr.startswith(known_abtag):
            return True
    return False


def _parse_tagful_str(in_str):
    pre, *rest = in_str.split("<")
    return _tupify(pre) + _smt(_parse2, rest)


def _parse2(in_str):
    inside, post = in_str.split(">")
    assert _startswith_a_known_abtag(inside)
    return {"custom_tag": inside}, *_tupify(post)


def _tupify(in_str):  # tuple, but with empty string to empty tuple
    return tuple() if in_str == "" else (in_str,)
