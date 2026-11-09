from author_boj_util.noted_by import startswith_n, startswith_x
from author_boj_util.short_id_etc import short_id
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
    """Return the presentation group key for a quirkrec.

    The groups are a closed dispatch on the noted-by dict: a quirkrec that matches
    no group, or more than one, raises.

    Args:
        quirkrec: dict with at least a nbd (noted-by dict) field.
    """
    groups = [k for k, v in _FILTER_FNS.items() if v(quirkrec)]
    if len(groups) != 1:
        raise ValueError(
            f"{short_id(quirkrec)} matches {len(groups)} presentation groups,"
            f" not 1: {groups}; nbd={quirkrec['nbd']}"
        )
    return groups[0]


def check_every_quirkrec_presented(qr_groups, listed_groups, presented_in_prose):
    """Raise unless every quirkrec is in a listed group or is presented in prose.

    A group is listed when a page has passed it to para_and_table. Each quirkrec in a
    group that no page lists must be declared in presented_in_prose under its own
    group, and every declaration must name such a quirkrec.

    Args:
        qr_groups: dict from get_qr_groups, mapping group keys to lists of quirkrecs.
        listed_groups: set of the group keys that pages have listed.
        presented_in_prose: dict mapping the short IDs of the quirkrecs that a page
            presents in prose, rather than in a group's list, to their group keys.
    """
    unpresented = []
    in_prose = {}
    for group_key, quirkrecs in qr_groups.items():
        if group_key in listed_groups:
            continue
        for quirkrec in quirkrecs:
            sid = short_id(quirkrec)
            if presented_in_prose.get(sid) == group_key:
                in_prose[sid] = group_key
            else:
                unpresented.append(f"{sid} ({group_key})")
    if unpresented:
        raise ValueError(
            "Quirkrecs that no page lists and no page presents in prose: "
            + ", ".join(unpresented)
        )
    if in_prose != presented_in_prose:
        stale = sorted(set(presented_in_prose) - set(in_prose))
        raise ValueError(
            f"Declared as presented in prose but not in an unlisted group: {stale}"
        )


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
