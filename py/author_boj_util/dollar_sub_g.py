import re

from boj_render import boj_html
from mb_cmn.my_utils import sl_map


def dollar_sub_g(dispatch, contents):
    """Perform dollar-sign substitution on HTML contents.

    Args:
        dispatch: dict mapping dollar-prefixed keys (e.g. "$tsinnorit")
            to zero-argument callables that return an HTML element
            (usually a span).
        contents: HTML content tree (strings and nested lists) to
            process.
    """
    flat_1 = boj_html.flatten(contents)
    assert flat_1 is not None
    _check_no_undollared(dispatch, flat_1)
    _check_no_bare_cv(flat_1)
    return sl_map((_dollar_sub_flat_el, dispatch), flat_1)


def _check_no_undollared(dispatch, flat_list):
    """Check that un-dollared identifiers don’t appear in the input.

    Args:
        dispatch: the dollar-substitution dispatch dict (keys are
            dollar-prefixed strings like "$tsinnorit").
        flat_list: flattened list of strings and HTML elements to scan.
    """
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


def _check_no_bare_cv(flat_list):
    """Assert that no bare chapter:verse references appear in display text.

    All verse references must use explicit $-dispatch entries like
    $link_C_V, $plain_C_V, $Ps_C_V, $Isaiah_C_V, etc.
    Matches inside $-tokens are excluded by scrubbing them first.
    """
    strings = [el for el in flat_list if isinstance(el, str)]
    full_text = "".join(strings)
    # Remove all $-tokens first so their internal digits aren't matched
    scrubbed = re.sub(r"\$[a-zA-Z0-9_]+", "", full_text)
    m = re.search(r"\d+:\d+", scrubbed)
    if m:
        snippet = full_text[:200] if len(full_text) > 200 else full_text
        assert False, (
            f"Bare verse reference '{m.group()}' found in display text. "
            f"Use a $link_C_V or $plain_C_V entry instead.\n"
            f"Context: {snippet!r}"
        )


def _dollar_sub_str(dispatch, str):
    parts = re.split(
        r"([$][a-zA-Z0-9_]+|%[\u05d0-\u05ea\u05be]+)",
        str,
    )
    return sl_map((_dollar_sub_str_part, dispatch), parts)


def _dollar_sub_str_part(dispatch, part):
    if part.startswith("$"):
        return dispatch[part]
    if part.startswith("%"):
        # Wrap in a span so the spell checker can skip Hebrew words.
        # See check_spelling_in_html.py which excludes "unpointed-tanakh" spans.
        return boj_html.span_c(part[1:], "unpointed-tanakh")
    return part
