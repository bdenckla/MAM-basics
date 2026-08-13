"""Exports add."""

import json
import mb_cmn.my_diffs as my_diffs
import mb_cmn.my_utils as my_utils
import py_uxlc.my_uxlc_book_abbreviations as u_bk_abbr
import py_uxlc.my_uxlc_location as my_uxlc_location
import py_wlc.my_wlc_bcv_str as my_wlc_bcv_str
import py_wlc_diffs_420422.my_dd_diffs_description as diffs_desc
import py_wlc_diffs_420422.my_word_diffs_420422 as my_word_diffs_420422
import py_wlc_diffs_420422.my_word_diffs_420422_utils as wd_utils
from mb_cmn import paths


def add(io_records):
    uxlc, pbi = my_uxlc_location.prep()
    all_ucps = _read_in_all_ucps()
    for recidx, io_record in enumerate(io_records):
        _add1(uxlc, pbi, all_ucps, recidx, io_record)


def _add1(uxlc, pbi, all_ucps, recidx, io_record):
    io_record["original-order"] = recidx + 1
    io_record["std-bcv-triple"] = _std_bcv_triple(io_record)
    io_record["diff-type"] = _diff_type(io_record)
    io_record["diff-desc"] = _diff_detail(io_record)
    io_record["descs-for-ucps"] = _descs_for_ucps(all_ucps, io_record)
    _add_page_and_guesses(io_record, uxlc, pbi, _std_bcvp_quad(io_record))


def _descs_for_ucps(all_ucps, record):
    ucps_for_this_record = wd_utils.uxlc_change_proposals(record)
    if not ucps_for_this_record:
        wlc_bcv_str = record["wlc_bcv_str"]
        raw_ucps = all_ucps["by-wbs"].get(wlc_bcv_str)
        if raw_ucps and not record.get("Decalogue-rafeh"):
            ab_uword = record["ab-uword"]
            a_uword, _b_uword = ab_uword.split("\n")
            print(f"bcv {wlc_bcv_str} {a_uword} has ucp candidates as follows:")
            for raw_ucp in raw_ucps:
                release_and_id = _release_and_id(raw_ucp)
                reftext = raw_ucp["reftext"]
                print(f"{reftext}")
                print(f"'UXLC-change-proposals': {release_and_id},")
            print("")
    return my_utils.sl_map((_desc_from_ucp, all_ucps), ucps_for_this_record)


def _desc_from_ucp(all_ucps, release_and_id):
    return all_ucps["by-rai"][release_and_id]["description"]


def _add_page_and_guesses(io_record, uxlc, pbi, std_bcvp_quad):
    pg_and_gs = my_uxlc_location.page_and_guesses(uxlc, pbi, std_bcvp_quad)
    for key, val in pg_and_gs.items():
        io_record[key] = val


def _diff_detail(record):
    diff_detail, _category = diffs_desc.get1(*_ab_uwords_pair(record))
    return diff_detail


def _read_in_all_ucps():
    """Read in lci_recs.json, raw"""
    path = paths.in_dir() / "UXLC-misc" / "all_changes.json"
    with open(path, encoding="utf-8") as in_fp:
        raw_ucps = json.load(in_fp)
    by_rai = {_release_and_id(raw_ucp): raw_ucp for raw_ucp in raw_ucps}
    by_wbs = {}
    for raw_ucp in raw_ucps:
        wbs = _wlc_bcv_str(raw_ucp)
        if wbs not in by_wbs:
            by_wbs[wbs] = []
        by_wbs[wbs].append(raw_ucp)
    return {"by-rai": by_rai, "by-wbs": by_wbs}


def _wlc_bcv_str(raw_ucp):
    std_bcvp_quad = u_bk_abbr.expand_citation(raw_ucp["citation"])
    std_bcv_triple = std_bcvp_quad[:-1]
    return my_wlc_bcv_str.make_wbs_from_std_bcv_triple(std_bcv_triple)


def _release_and_id(raw_ucp):
    release_date = raw_ucp["release"]
    changeset_date = raw_ucp["changeset"]
    number_within_changest = raw_ucp["n"]
    change_id = changeset_date + "-" + str(number_within_changest)
    return release_date, change_id


def _ab_uwords_pair(record):
    return record["ab-uword"].split("\n")


_CUSTOM = {
    ((".", None),): "-dms",
    ((None, "."),): "+dms",
    ((",", None),): "-rfh",
    (("03", None),): "-pashta",
    ((None, "81"),): "+rev",
    ((None, "05"),): "+psq",
    ((None, "-"),): "+mqf",
    ((":", None),): "-shoḥ",
    ((None, ":"),): "+shoḥ",
    (("A", "E"),): "vow-chng",
    (("F", "A"),): "vow-chng",
    (("I", ":"),): "vow-chng",
    (("0", "1"),): "acc-chng",
    (("1", "0"),): "acc-chng",
    (("1", "3"),): "acc-chng",
    (("3", "1"),): "acc-chng",
    (("3", "6"),): "acc-chng",
    (("7", "9"),): "acc-chng",
    (("63", "81"),): "acc-chng",
    (("92", "70"),): "acc-chng",
}


def _diff_type(record):
    pair = record["ab-word"].split("\n")
    generic_diffs = my_diffs.get(*pair)
    if custom := _CUSTOM.get(tuple(generic_diffs)):
        return custom
    return "misc"


def _std_bcvp_quad(record):
    return *_std_bcv_triple(record), _pos(record)


def _pos(record):
    wlc_bcv_str, ab_word = record["wlc_bcv_str"], record["ab-word"]
    a_word, _b_word = ab_word.split("\n")
    poskey = wlc_bcv_str + "!" + a_word
    return my_word_diffs_420422.WORD_POSITIONS[poskey]


def _std_bcv_triple(record):
    wlc_bcv_str = record["wlc_bcv_str"]
    return my_wlc_bcv_str.get_std_bcv_triple(wlc_bcv_str)
