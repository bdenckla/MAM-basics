from author_boj_util.noted_by import startswith_n, startswith_x
from mb_cmn.my_utils import my_groupby


def get_qr_groups(quirkrecs):
    """Group quirkrecs by their presentation group key.

    Args:
        quirkrecs: list of enriched quirkrec dicts (must have pgroup).

    Returns:
        Dict mapping group key strings to lists of quirkrecs.
    """
    groups = my_groupby(quirkrecs, lambda qr: get_pgroup(qr))
    return groups


def get_pgroup(quirkrec):
    """Return the presentation group key for a quirkrec, or None.

    Args:
        quirkrec: dict with at least a nbd (noted-by dict) field.
    """
    groups = [k for k, v in _FILTER_FNS.items() if v(quirkrec)]
    assert len(groups) <= 1, f"Multiple groups for {quirkrec['qr-cv']}: {groups}"
    return groups[0] if groups else None


def says_who(quirkrec):
    nbd = quirkrec["nbd"]
    return list(e for e in _T30 if startswith_n(nbd, e))


def nbhq_and_n3(quirkrec):
    return _foobhq_and_n3("nBHQ", quirkrec["nbd"])


def nbhq_and_x3(quirkrec):
    return _foobhq_and_x3("nBHQ", quirkrec["nbd"])


def xbhq_and_n3(quirkrec):
    return _foobhq_and_n3("xBHQ", quirkrec["nbd"])


def tbhq_and_n3(quirkrec):
    return _foobhq_and_n3("tBHQ", quirkrec["nbd"])


def tbhq_and_x3(quirkrec):
    return _foobhq_and_x3("tBHQ", quirkrec["nbd"])


def tbhq_and_zdw(quirkrec):
    return quirkrec["nbd"]["e:WLC"] == "zdexiWLC"


def tbhq_and_zmw(quirkrec):
    return quirkrec["nbd"]["e:WLC"] == "zmiscWLC"


def xbhq_and_nuxlc(quirkrec):
    return quirkrec["nbd"]["e:UXLC"] == "nUXLC"


def tbhq_and_zuxlc(quirkrec):
    return quirkrec["nbd"]["e:UXLC"] == "zUXLC"


def adm(quirkrec):
    return quirkrec["nbd"]["e:DM"] == "aDM"


def xbhq_and_twlc(quirkrec):
    nbd = quirkrec["nbd"]
    return (nbd["e:BHQ"], nbd["e:WLC"]) == ("xBHQ", "tWLC")


def tbhq_and_twlc(quirkrec):
    nbd = quirkrec["nbd"]
    return (nbd["e:BHQ"], nbd["e:WLC"]) == ("tBHQ", "tWLC")


#####################################################################


def _foobhq_and_n3(foobhq, nbd):
    return nbd["e:BHQ"] == foobhq and any(startswith_n(nbd, e) for e in _T30)


def _foobhq_and_x3(foobhq, nbd):
    return nbd["e:BHQ"] == foobhq and all(
        startswith_x(nbd, e) for e in ("e:BHL", "e:DM", "e:WLC")
    )


_T30 = ("e:BHL", "e:DM", "e:WLC")
_FILTER_FNS = {
    "g:nbhq_and_x3": nbhq_and_x3,
    "g:nbhq_and_n3": nbhq_and_n3,
    "g:tbhq_and_n3": tbhq_and_n3,
    "g:xbhq_and_n3": xbhq_and_n3,
    "g:tbhq_and_zdw": tbhq_and_zdw,
    "g:tbhq_and_zmw": tbhq_and_zmw,
    "g:xbhq_and_nuxlc": xbhq_and_nuxlc,
    "g:tbhq_and_zuxlc": tbhq_and_zuxlc,
    "g:adm": adm,
    "g:xbhq_and_twlc": xbhq_and_twlc,
    "g:tbhq_and_twlc": tbhq_and_twlc,
}
# nbhq: noted (as a quirk) in BHQ
# xbhq: not noted (as a quirk) in BHQ
# n3, noted (as a quirk) in one of "the three"
# x3: not noted (as a quirk) in one of "the three"
# zw (zmiscWLC): noted (as consensus) by WLC (combined with MAM):
#     flagged as a change in WLC relative to BHS, e.g. a bracket-c or bracket-v note.
#     comparison with MAM revealed that it is a change back towards consensus,
#     i.e. this is BHS/BHQ proposing a quirk that is not in μL (according to WLC at least)
