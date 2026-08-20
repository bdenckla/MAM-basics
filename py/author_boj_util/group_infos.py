"""Human-friendly group info dicts for groups that previously used bare string keys."""

from author_boj.m_contributions_base import contributions_base
from author_boj.m_reiterations_base import reiterations_base
from author_boj.m_implications_base import implications_base
from author_boj.m_bad_news_1_base import bad_news_1_base
from author_boj_util import author


def contributions_group_info(the_len):
    return {
        "gi:group_key": "g:nbhq_and_x3",
        "gi:group_heading": "$BHQ contributions",
        "gi:group_title": "BHQ contributions",
        "gi:group_intro": [author.para(contributions_base("The", the_len))],
    }


def reiterations_group_info(the_len):
    return {
        "gi:group_key": "g:nbhq_and_n3",
        "gi:group_heading": "$BHQ reiterations",
        "gi:group_title": "BHQ reiterations",
        "gi:group_intro": [author.para(reiterations_base("The", the_len))],
    }


def implications_group_info(the_len):
    return {
        "gi:group_key": "g:tbhq_and_n3",
        "gi:group_heading": "$BHQ implications",
        "gi:group_title": "BHQ implications",
        "gi:group_intro": [author.para(implications_base("The", the_len))],
    }


def xbhq_and_n3_group_info(the_len):
    return {
        "gi:group_key": "g:xbhq_and_n3",
        "gi:group_heading": "Quirks not transcribed by $BHQ",
        "gi:group_title": "Quirks not transcribed by BHQ",
        "gi:group_intro": [author.para(bad_news_1_base("The", the_len))],
    }


def xbhq_and_nuxlc_group_info(the_len):
    return {
        "gi:group_key": "g:xbhq_and_nuxlc",
        "gi:group_heading": "Quirks missed by $BHQ flagged by $UXLC",
        "gi:group_title": "Quirks missed by BHQ flagged by UXLC",
        "gi:group_intro": [],
    }


def tbhq_and_zuxlc_group_info(the_len):
    return {
        "gi:group_key": "g:tbhq_and_zuxlc",
        "gi:group_heading": "Quirks in $BHQ flagged as likely false by $UXLC",
        "gi:group_title": "Quirks in BHQ flagged as likely false by UXLC",
        "gi:group_intro": [],
    }


def adm_group_info(the_len):
    return {
        "gi:group_key": "g:adm",
        "gi:group_heading": "Quirks in μA reported by $DM",
        "gi:group_title": "Quirks in μA reported by DM",
        "gi:group_intro": [],
    }
