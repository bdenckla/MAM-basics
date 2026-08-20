"""Exports gen_html_file and anchor"""

from author_boj_util import author
from author_boj_util.all_quirks import AllQuirks
from author_boj_util.para_and_table import para_and_table
from author_boj_util.group_infos import adm_group_info
from author_boj_util.common_titles_etc import D4_TITLE, D4_H1_CONTENTS, D4_FNAME


def gen_html_file(aq: AllQuirks):
    author.assert_stem_eq(__file__, D4_FNAME)
    cbody = _make_cbody(aq)
    author.help_gen_html_file(aq.tdm_ch, D4_FNAME, D4_TITLE, cbody)


def _make_cbody(aq: AllQuirks):
    cbody = [
        author.heading_level_1(D4_H1_CONTENTS),
        para_and_table(aq, _cpara_adm, adm_group_info(len(aq.qr_groups["g:adm"]))),
    ]
    return cbody


def _cpara_adm(the_len):
    return ["The following quirks in μA are reported by $DM but not by $BHQ."]
