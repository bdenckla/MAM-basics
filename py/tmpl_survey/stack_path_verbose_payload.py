"""Helpers for verbose stack-path payload construction and de-parsed Wikitext."""

from mb_cmn import ws_tmpl2 as wtp2
from ws import ws_unparse


def build_match_payload(dataset_key, stack, subtype, wtel):
    return {
        "column": stack[0],
        "stack_path": f"{'/'.join(stack)}/{subtype}",
        "subtype": subtype,
        "match_tree_json": wtel,
        "match_tree_wikitext": wtel_to_wikitext(dataset_key, wtel),
    }


def wtel_to_wikitext(dataset_key, wtel):
    if dataset_key == "plain":
        return ws_unparse.unparse(wtel)
    assert dataset_key == "plus", dataset_key
    return wtel_to_wikitext_plus(wtel)


def wtel_to_wikitext_plus(wtel):
    if isinstance(wtel, str):
        return wtel
    assert isinstance(wtel, dict)
    assert wtp2.is_template(wtel)
    name = wtp2.template_name(wtel)
    parts = [name]
    positional_key = 1
    for param_key in wtp2.template_param_keys(wtel):
        value = _wtseq_to_wikitext_plus(wtp2.template_param_val(wtel, param_key))
        if param_key == str(positional_key):
            parts.append(value)
            positional_key += 1
            continue
        parts.append(f"{param_key}={value}")
    return "{{" + "|".join(parts) + "}}"


def _wtseq_to_wikitext_plus(wtseq):
    return "".join(wtel_to_wikitext_plus(wtel) for wtel in wtseq)
