from author_boj_util.english_list import english_list
from author_boj_util.get_qr_groups import says_who
from mb_cmn.my_utils import sl_map


def says(quirkrec):
    says_str_or_fn = _SAYS_HANDLERS[quirkrec["pgroup"]]
    if isinstance(says_str_or_fn, str):
        return [says_str_or_fn]
    return says_str_or_fn(quirkrec)


def _says_fn_for_xbhq_and_n3(quirkrec):
    # yes, the double list, i.e. [[x, y, z]], is intentional below
    return [["says ", _english_says_who(quirkrec), " but not $BHQ"]]


_SAYS_HANDLERS = {
    "g:nbhq_and_x3": "says $BHQ’s contribution",
    "g:nbhq_and_n3": "says $BHQ’s reiteration",
    "g:tbhq_and_n3": "says $BHQ’s implication",
    "g:xbhq_and_n3": _says_fn_for_xbhq_and_n3,
    "g:tbhq_and_zdw": "says $BHQ but not $WLC",
    "g:tbhq_and_zmw": "says $BHQ but not $WLC",
    "g:xbhq_and_nuxlc": "says $UXLC but not $BHQ",
    "g:tbhq_and_zuxlc": "says $BHQ but not $UXLC",
    "g:adm": "says $DM",
    "g:tbhq_and_twlc": "says $BHQ and $WLC",
    "g:xbhq_and_twlc": "says $WLC but not $BHQ",
}


def _english_says_who(quirkrec):
    dsw = sl_map(_dollar_editions, says_who(quirkrec))
    return english_list(dsw)


def _dollar_editions(e_colon_edition):
    return _DOLLAR[e_colon_edition]


_DOLLAR = {
    "e:BHL": "$BHL",
    "e:DM": "$DM",
    "e:WLC": "$WLC",
}
