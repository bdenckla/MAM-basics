from pycmn import my_utils
from pycmn import ws_tmpl1 as wtp1


def unparse(obj):
    """Invert obj back to a Wikitext string."""
    if isinstance(obj, (tuple, list)):
        return "".join(tuple(map(unparse, obj)))
    if wtp1.is_template(obj):
        return _invert_tmpl_back_to_wikitext(obj)
    if isinstance(obj, dict):
        key = my_utils.first_and_only(tuple(obj.keys()))
        assert key == "custom_tag"
        return _invert_abtag_back_to_wikitext(obj[key])
    assert isinstance(obj, str)
    return obj


def _invert_tmpl_back_to_wikitext(tmpl):
    mapped = tuple(map(unparse, wtp1.template_elements(tmpl)))
    barsep = "|".join(mapped)
    return "{{" + barsep + "}}"


def _invert_abtag_back_to_wikitext(val):
    # val == 'קטע סוף=שורה 5 לפני השיר/', for example
    return "<" + val + ">"
