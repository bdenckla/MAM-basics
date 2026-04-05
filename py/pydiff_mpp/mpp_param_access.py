"""MPP template parameter access helpers.

Exports:
    _MISSING   — sentinel for absent parameters
    _get_param — read a template parameter across historical formats
"""

_MISSING = object()


def _get_param(tmpl, key):
    """Look up a single template parameter by key.

    Handles all historical formats:
      - tmpl_params dict  (current: {"1": ..., "ד": ...})
      - tmpl_args_dic dict (transitional, same shape)
      - tmpl_args list (oldest: positional for integer keys,
        "key=value" strings for named keys like "ד=...",
        or ["key=", value] lists when value is complex)

    Returns the value, or _MISSING if the key is absent.
    """
    for dict_key in ("tmpl_params", "tmpl_args_dic"):
        d = tmpl.get(dict_key)
        if d is not None and key in d:
            return d[key]
    args = tmpl.get("tmpl_args")
    if args is not None:
        if key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(args):
                return args[idx]
        else:
            prefix = key + "="
            for arg in args:
                if isinstance(arg, str) and arg.startswith(prefix):
                    return arg[len(prefix) :]
                if (
                    isinstance(arg, list)
                    and arg
                    and isinstance(arg[0], str)
                    and arg[0].startswith(prefix)
                ):
                    head = arg[0][len(prefix) :]
                    tail = arg[1:]
                    if not head and len(tail) == 1:
                        return tail[0]
                    return ([head] if head else []) + tail
    return _MISSING
