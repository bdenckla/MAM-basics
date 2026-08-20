"""Exports gen_html_file and anchor"""

from author_boj_util import author
from author_boj_util.all_quirks import AllQuirks
from author_boj_util.para_and_table import para_and_table
from author_boj_util.group_infos import (
    xbhq_and_nuxlc_group_info,
    tbhq_and_zuxlc_group_info,
)
from author_boj_util.common_titles_etc import D3_TITLE, D3_H1_CONTENTS, D3_FNAME


def gen_html_file(aq: AllQuirks):
    author.assert_stem_eq(__file__, D3_FNAME)
    cbody = _make_cbody(aq)
    author.help_gen_html_file(aq.tdm_ch, D3_FNAME, D3_TITLE, cbody)


def _make_cbody(aq: AllQuirks):
    cbody = [
        author.heading_level_1(D3_H1_CONTENTS),
        para_and_table(
            aq,
            _cpara_xn,
            xbhq_and_nuxlc_group_info(len(aq.qr_groups["g:xbhq_and_nuxlc"])),
        ),
        para_and_table(
            aq,
            _cpara_tz,
            tbhq_and_zuxlc_group_info(len(aq.qr_groups["g:tbhq_and_zuxlc"])),
        ),
    ]
    return cbody


def _cpara_xn(the_len):
    """xn: xbhq_and_nuxlc"""
    return [
        ["$BHQ does not transcribe ", str(the_len)],
        [" quirks in μL that are noted"],
        [" in $UXLC. They are as follows:"],
    ]


def _cpara_tz(the_len):
    """tz: tbhq_and_zuxlc"""
    return [
        ["$BHQ transcribes but does not note ", str(the_len)],
        [" quirks in μL that are noted"],
        [" as likely false by $UXLC. They are as follows:"],
    ]
