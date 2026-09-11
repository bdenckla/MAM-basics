"""MAM-parsed-plus template parameter access helpers.

Exports:
    MISSING   — sentinel for absent parameters
    get_param — read a template parameter across historical formats
    param_items — read every semantic parameter across historical formats
"""

MISSING = object()


def _extract_named_arg(arg):
    if isinstance(arg, str) and "=" in arg:
        return tuple(arg.split("=", 1))
    if isinstance(arg, list) and arg and isinstance(arg[0], str) and "=" in arg[0]:
        key, head = arg[0].split("=", 1)
        tail = arg[1:]
        if not head and len(tail) == 1:
            value = tail[0]
        else:
            value = ([head] if head else []) + tail
        return key, value
    return None


def param_items(tmpl):
    """Return every semantic ``(key, value)`` pair across historical formats.

    Handles all historical formats:
      - tmpl_params dict  (current: {"1": ..., "ד": ...})
      - tmpl_args_dic dict (transitional, same shape)
      - tmpl_args list (oldest: positional for integer keys,
        "key=value" strings for named keys like "ד=...",
        or ["key=", value] lists when value is complex)

    Positional indices advance only for positional arguments; named arguments keep
    their written keys.  The original order is preserved.
    """
    for dict_key in ("tmpl_params", "tmpl_args_dic"):
        d = tmpl.get(dict_key)
        if d is not None:
            return list(d.items())
    args = tmpl.get("tmpl_args")
    if args is None:
        return []
    items = []
    positional_index = 1
    for arg in args:
        named = _extract_named_arg(arg)
        if named is not None:
            items.append(named)
            continue
        items.append((str(positional_index), arg))
        positional_index += 1
    return items


def get_param(tmpl, key):
    """Look up one semantic parameter, returning ``MISSING`` when absent."""
    for item_key, value in param_items(tmpl):
        if item_key == key:
            return value
    return MISSING
