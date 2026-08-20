import re
from mb_cmn.my_utils import sl_map

_STARTSWITH_N = {
    "e:BHQ": "nBHQ",
    "e:BHL": "nBHL",
    "e:DM": "nDM",
    "e:WLC": "nWLC",
    "e:UXLC": "nUXLC",
}
_STARTSWITH_X = {
    "e:BHQ": "xBHQ",
    "e:BHL": "xBHL",
    "e:DM": "xDM",
    "e:WLC": "xWLC",
    "e:UXLC": "xUXLC",
}
_DEFAULT = _STARTSWITH_X
_EDITIONS = tuple(_DEFAULT)


def nb_dict(quirkrec):
    """Build the noted-by dict for a quirkrec.

    Args:
        quirkrec: dict with a qr-noted-by field (hyphen-separated
            string like "nBHQ-nDM" or empty string).

    Returns:
        Dict mapping edition keys (e.g. "e:BHQ") to notation strings
        (e.g. "nBHQ", "xBHQ", "tBHQ").
    """
    nb_str = quirkrec["qr-noted-by"]
    parts = nb_str.split("-") if nb_str else []
    pairs = sl_map(_nb_pair, parts)
    sparse_dict = dict(pairs)
    full_dict = _fill_in(sparse_dict)
    _do_asserts(full_dict)
    return full_dict


def startswith_n(nbd, edition_key):
    return nbd[edition_key] == _STARTSWITH_N[edition_key]


def startswith_x(nbd, edition_key):
    return nbd[edition_key] == _STARTSWITH_X[edition_key]


def x_uclc(quirkrec):
    nbd = nb_dict(quirkrec)
    return nbd["e:UXLC"] == "xUXLC"


def _do_asserts(nbd):
    bhq, bhl, dm, wlc, uxlc = (nbd[e] for e in _EDITIONS)
    _do_solo_asserts(bhq, bhl, dm, wlc, uxlc)
    _do_combo_asserts(bhq, bhl, dm, wlc, uxlc)


def _do_solo_asserts(bhq, bhl, dm, wlc, uxlc):
    assert bhq in ("nBHQ", "xBHQ", "tBHQ")
    assert bhl in ("nBHL", "xBHL")
    assert dm in ("nDM", "xDM", "aDM")
    assert wlc in ("nWLC", "xWLC", "tWLC", "zmiscWLC", "zdexiWLC")
    assert uxlc in ("nUXLC", "xUXLC", "zUXLC")


def _do_combo_asserts(bhq, bhl, dm, wlc, uxlc):
    if wlc in ("zmiscWLC", "zdexiWLC"):
        assert (bhq, bhl, dm, uxlc) == ("tBHQ", "xBHL", "xDM", "xUXLC")
    if uxlc == "zUXLC":
        assert (bhq, bhl, dm, wlc) == ("tBHQ", "xBHL", "xDM", "xWLC")
    if uxlc == "nUXLC":
        assert (bhq, bhl, dm, wlc) == ("xBHQ", "xBHL", "xDM", "xWLC")
    if dm == "aDM":
        assert (bhq, bhl, wlc, uxlc) == ("xBHQ", "xBHL", "xWLC", "xUXLC")


def _fill_in(nb_dict):
    full = {e: nb_dict.get(e) or _DEFAULT[e] for e in _EDITIONS}
    return full


def _nb_pair(part):
    """Turns e.g. "xBHL" into ("e:BHL", "xBHL")"""
    match = re.match(r"^([a-z]+)([A-Z].*)$", part)
    assert match is not None, f"part={part}"
    assert len(match.groups()) == 2
    _lower, upper = match.groups()
    return f"e:{upper}", part
