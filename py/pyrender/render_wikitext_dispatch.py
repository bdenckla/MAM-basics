""" Exports make_handler_table """


def make_handler_table(wek_to_hsc: dict, eclp: str):
    """
    Given "wek_to_hsc", return a dispatch table only for handlers
    of type given by the "eclp" arg.
    wek_to_hsc: [dict from] wek to hsc, where
        wek: Wikitext element key (e.g. str, '__', 'נוסח')
        hsc: hspec, compact [version], e.g. {'ec': _handle_foo}
        hspec: handler specification
    eclp: 'e', 'c', 'l', or 'p'
    Example call: make_handler_dispatch_table(_HANDLER_SPECS, 'p')
    """
    wek_to_hse = _expand_hspecs(wek_to_hsc)
    # hse: hspec, expanded [version]
    return {
        wek: hspec_expanded[eclp]
        for wek, hspec_expanded in wek_to_hse.items()
        if eclp in hspec_expanded
    }


def _expand_hspecs(wek_to_hsc: dict):
    return {wek: _expand_hspec(hsc) for wek, hsc in wek_to_hsc.items()}


def _expand_hspec(hspec_compact: dict):
    # Expand something like {'ecp': foo, 'l': bar}
    # to {'e': foo, 'c': foo, 'l': bar, 'p': foo}
    hspec_expanded = {}
    for masklike, handler in hspec_compact.items():
        for lett in masklike:
            assert lett not in hspec_expanded
            hspec_expanded[lett] = handler
    return hspec_expanded
