"""
Exports:
    isolate_trailing
    general_endswith
"""

from pyrender import render_element as renel


def isolate_trailing(renseq):
    """Isolate any trailing space from renseq."""
    if not renseq:
        return "", renseq
    last_el = renseq[-1]
    if isinstance(last_el, dict):
        if last_el_contents := renel.get_ren_el_contents(last_el):
            tr_space, newcont = isolate_trailing(last_el_contents)
            stripped_seq = renseq[:-1] + (dict(last_el, contents=newcont),)
            return tr_space, stripped_seq
        last_el_tag = renel.get_ren_el_tag(last_el)
        if last_el_tag == "lp-legarmeih":
            return "", renseq
        expected_tags = (
            "mam-br-after-pe",
            "ren-tag-octo-space",
            "ren-tag-thin-space",
            "ren-tag-no-break-space",
        )
        assert last_el_tag in expected_tags, last_el_tag
        return last_el, renseq[:-1]
    assert isinstance(last_el, str)
    if last_el.endswith(" "):
        assert not last_el[:-1].endswith(" ")
        trimmed = *renseq[:-1], last_el[:-1]
        return " ", trimmed
    return "", renseq


def general_endswith(ren_el, suffix):
    """A generalized version of "endswith", i.e. not just for strings."""
    if isinstance(ren_el, str):
        return ren_el.endswith(suffix)
    assert isinstance(ren_el, dict)
    if contents := renel.get_ren_el_contents(ren_el):
        return general_endswith(contents[-1], suffix)
    return False


def _multi_endswith(string, suffixes):
    for suffix in suffixes:
        if string.endswith(suffix):
            return suffix
    return False
