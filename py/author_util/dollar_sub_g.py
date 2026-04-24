import re

from py_misc import my_html
from pycmn.my_utils import sl_map


def dollar_sub_g(dispatch, contents):
    """The parameter "dispatch" is a dict.
    It maps strings like "$tsinnorit" to functions that take no
    arguments and return an HTML element (usually a span)."""
    flat_1 = my_html.flatten(contents)
    assert flat_1 is not None
    _check_no_undollared(dispatch, flat_1)
    return sl_map((_dollar_sub_flat_el, dispatch), flat_1)


def _check_no_undollared(dispatch, flat_list):
    """Check that un-dollared identifiers don't appear in the input."""
    strings = [el for el in flat_list if isinstance(el, str)]
    full_text = "".join(strings)
    for key in dispatch:
        if key.startswith("$"):
            undollared = key[1:]
            if re.search(rf"(?<!\$)\b{re.escape(undollared)}\b", full_text):
                snippet = full_text[:200] if len(full_text) > 200 else full_text
                raise ValueError(
                    f"Found '{undollared}' without '$' prefix. "
                    f"Did you mean '{key}'?\n"
                    f"Context: {snippet!r}"
                )


def _dollar_sub_flat_el(dispatch, flat_el):
    if isinstance(flat_el, str):
        return _dollar_sub_str(dispatch, flat_el)
    return flat_el


def _dollar_sub_str(dispatch, str):
    parts = re.split("([$][a-zA-Z0-9_]+)", str)
    return sl_map((_dollar_sub_str_part, dispatch), parts)


def _dollar_sub_str_part(dispatch, part):
    return dispatch[part] if part.startswith("$") else part
