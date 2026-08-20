"""Generate paragraph and table of quirks for a group."""

from author_boj_util import author
from author_boj_util.all_quirks import AllQuirks
from author_boj_util.introduce_quirkrec_table import qr_table_intro
from author_boj_util.job_ov_and_de import row_id
from author_boj_util.is_lop import is_lop

__all__ = ["para_and_table"]


def para_and_table(aq: AllQuirks, para_func, group_info):
    """Generate intro paragraph(s) and a linked quirk table for a group.

    Args:
        aq: AllQuirks dataclass holding all quirkrec data.
        para_func: callable that takes a record count and returns
            paragraph content (or a list of paras).
        group_info: group info dict (with gi:group_key, etc.) or a
            bare group key string.
    """
    group_key = _group_key(group_info)
    group_of_quirkrecs = aq.qr_groups[group_key]
    record_count = len(group_of_quirkrecs)
    link = _table_of_quirks(aq.tdm_ch, group_info, aq.ov_and_de, group_of_quirkrecs)
    pf_out = para_func(record_count)
    lop = pf_out if is_lop(pf_out) else [author.para(pf_out)]
    return [*lop, author.para(link)]


def _group_key(group_info):
    if isinstance(group_info, str):
        return group_info
    else:
        return group_info["gi:group_key"]


def _group_intro(group_info):
    if isinstance(group_info, str):
        return []
    else:
        return group_info.get("gi:group_intro", [])


def _group_heading(group_info):
    default = f"Group: {_group_key(group_info)}"
    if isinstance(group_info, str):
        return default
    else:
        return group_info.get("gi:group_heading", default)


def _group_title(group_info):
    default = _group_heading(group_info)
    if isinstance(group_info, str):
        return default
    else:
        return group_info.get("gi:group_title", default)


def _overview(ov_and_de, quirkrec):
    the_row_id = row_id(quirkrec)
    return ov_and_de[the_row_id]["od-overview"]


_FILE_BASENAMES = {
    "g:nbhq_and_x3": "grp_nbhq_and_x3",
    "g:nbhq_and_n3": "grp_nbhq_and_n3",
    "g:tbhq_and_n3": "grp_tbhq_and_n3",
    "g:xbhq_and_n3": "grp_xbhq_and_n3",
    "g:tbhq_and_zdw": "grp_tbhq_and_zdw",
    "g:tbhq_and_zmw": "grp_tbhq_and_zmw",
    "g:xbhq_and_nuxlc": "grp_xbhq_and_nuxlc",
    "g:tbhq_and_zuxlc": "grp_tbhq_and_zuxlc",
    "g:adm": "grp_adm",
}
assert all(v == k.replace("g:", "grp_") for k, v in _FILE_BASENAMES.items())


def _table_of_quirks(tdm_ch, group_info, ov_and_de, group_of_quirkrecs):
    rows = [_overview(ov_and_de, rec) for rec in group_of_quirkrecs]
    table = author.table_c(rows)
    group_key_sanitized = _FILE_BASENAMES[_group_key(group_info)]
    fname = f"{group_key_sanitized}.html"
    cbody = [
        author.heading_level_1(_group_heading(group_info)),
        *_group_intro(group_info),
        *qr_table_intro("intro-header-only"),
        table,
    ]
    title = _group_title(group_info)
    author.help_gen_html_file(tdm_ch, fname, title, cbody)
    record_count = len(group_of_quirkrecs)
    link_text = f"View {record_count} entries"
    return author.anc_h(link_text, fname)
