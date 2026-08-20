from boj_render import boj_html
from author_boj_util import author

_BHQ_HAS_TAR = "$BHQ has טרחא but should probably have דחי"


def bad_news_2(len_dexi, len_misc):
    len_total = len_dexi + len_misc
    return [
        "Finally, we present some more bad news: some $WLC notes help us identify that",
        f" the Job fascicle of $BHQ transcribes but does not note at least {str(len_total)}",
        " quirks in μL that,",
        [" ", boj_html.bold("for good reason"), ","],
        " are not noted in any of the other three editions.",
        #
        " The good reason is that all of these are unlikely to be the scribe’s intention,",
        " i.e. are more likely quirks in $BHQ than quirks in μL.",
        #
        f" These {str(len_total)} likely-false quirks can be divided into two groups:",
        f" a group of {str(len_dexi)} cases where {_BHQ_HAS_TAR} and",
        f" a group of {str(len_misc)} cases not concerning a טרחא in $BHQ.",
    ]


def wlc_dexi_group_intro(len_dexi):
    return [author.para(_wlc_dexi_core(len_dexi) + ".")]


def wlc_misc_group_intro(len_misc):
    return [author.para("Here are the " + _wlc_misc_core(len_misc) + ".")]


def wlc_dexi(len_dexi):
    return [
        _wlc_dexi_core(len_dexi),
        " (note that $link_18_6 and $link_22_28 could also be considered to be in this group):",
    ]


def wlc_misc(len_misc):
    return [
        "Then there are the",
        [" ", _wlc_misc_core(len_misc), "."],
        #
        f" (One of those {str(len_misc)},",
        " the one in $link_22_12 goes in the opposite direction:",
        " $BHQ has דחי but should probably have טרחא.)",
        #
        f" Here are those {str(len_misc)} cases:",
    ]


def wlc_dexi_group_info(len_dexi):
    return {
        "gi:group_key": "g:tbhq_and_zdw",
        "gi:group_intro": wlc_dexi_group_intro(len_dexi),
        "gi:group_heading": _wlc_dexi_group_toh("$WLC", "$BHQ"),
        "gi:group_title": _wlc_dexi_group_toh("WLC", "BHQ"),
    }


def wlc_misc_group_info(len_misc):
    return {
        "gi:group_key": "g:tbhq_and_zmw",
        "gi:group_intro": wlc_misc_group_intro(len_misc),
        "gi:group_heading": _wlc_misc_group_toh("$WLC", "$BHQ"),
        "gi:group_title": _wlc_misc_group_toh("WLC", "BHQ"),
    }


def _wlc_dexi_group_toh(wlc, bhq):
    """toh: title or heading"""
    return f"Group: {wlc} corrects {bhq} טרחא"


def _wlc_misc_group_toh(wlc, bhq):
    """toh: title or heading"""
    return f"Group: {wlc} corrects {bhq} various (non-טרחא)"


def _wlc_dexi_core(len_dexi):
    return f"Here are the {str(len_dexi)} cases noted in $WLC where {_BHQ_HAS_TAR}"


def _wlc_misc_core(len_misc):
    return (
        f"{str(len_misc)} cases noted in $WLC where $BHQ is probably in error"
        + " but that error does not concern a טרחא in $BHQ"
    )
