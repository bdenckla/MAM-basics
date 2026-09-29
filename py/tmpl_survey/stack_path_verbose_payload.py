"""Helpers for verbose plus stack-path payloads and de-parsed Wikitext."""

from mb_cmn import ws_tmpl2 as wtp2


def _path_template_context(template_chain):
    assert template_chain
    subtypes = [subtype for subtype, _wtel in template_chain]
    root_subtype, root_wtel = template_chain[0]
    root_ctx = {
        "path_template_subtypes": subtypes,
        "path_root_subtype": root_subtype,
        "path_root_wikitext": wtel_to_wikitext_plus(root_wtel),
    }
    if len(template_chain) == 1:
        return {
            **root_ctx,
            "path_parent_subtype": None,
            "path_parent_wikitext": None,
        }
    parent_subtype, parent_wtel = template_chain[-2]
    return {
        **root_ctx,
        "path_parent_subtype": parent_subtype,
        "path_parent_wikitext": wtel_to_wikitext_plus(parent_wtel),
    }


def build_root_payload(template_chain):
    assert template_chain
    _root_subtype, root_wtel = template_chain[0]
    return {
        "path_root_wikitext": wtel_to_wikitext_plus(root_wtel),
        "path_root_json": root_wtel,
    }


def build_match_payload(stack, subtype, wtel, template_chain):
    return {
        "column": stack[0],
        "stack_path": f"{'/'.join(stack)}/{subtype}",
        "subtype": subtype,
        "match_tree_json": wtel,
        "match_tree_wikitext": wtel_to_wikitext_plus(wtel),
        **_path_template_context(template_chain),
    }


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
