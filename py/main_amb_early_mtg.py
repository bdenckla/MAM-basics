"""Exports main."""

import sys

import uxlc_amb_early_mtg.amb_early_mtg as amb_early_mtg
import uxlc_amb_early_mtg.amb_early_mtg_full as amb_early_mtg_full
import uxlc_amb_early_mtg.amb_early_mtg_summary as amb_early_mtg_summary
import uxlc_amb_early_mtg.amb_early_mtg_extend as amb_early_mtg_extend
import uxlc_amb_early_mtg.amb_early_mtg_three_and_beyond as amb_early_mtg_three_and_beyond
import uxlc_misc.uxlc_utils_html as uxlc_utils_html


def main():
    """Writes amb-early-mtg records to HTML files."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    records = amb_early_mtg.RECORDS
    #
    amb_early_mtg_three_and_beyond.find()
    #
    amb_early_mtg_extend.extend_records(records)  # mutates, i.e. modifies in-place
    #
    _set_prev_and_next(records, "prev", "next")
    #
    dubious_recs = list(filter(_has_dem, records))
    #
    _set_prev_and_next(dubious_recs, "prev-dubious", "next-dubious")
    #
    # Now we write varies HTML files in a bottom-up (leaves first) fashion
    #
    amb_early_mtg_full.write(records)  # fills in path-to-full fields
    #
    dubious_path = "dubious.html"
    dubious_title = "Words with dubious early meteg letter"
    amb_early_mtg_summary.write(dubious_recs, dubious_path, dubious_title)
    #
    intro = _intro(records, dubious_recs, dubious_path, dubious_title)
    title = "Words with ambiguous early meteg"
    amb_early_mtg_summary.write(records, "index.html", title, intro)


def _set_prev_and_next(io_records, prevkey, nextkey):
    prev_record = None
    for io_record in io_records:
        if prev_record:
            io_record[prevkey] = prev_record
        prev_record = io_record
    next_record = None
    for io_record in reversed(io_records):
        if next_record:
            io_record[nextkey] = next_record
        next_record = io_record


def _intro(records, dubious_recs, dubious_path, dubious_title):
    anch_attr = {"href": dubious_path}
    nrecs = len(records)
    ndrecs = len(dubious_recs)
    para1_contents = (
        f"This page lists all {nrecs} words in UXLC that have an ambiguous early meteg."
    )
    anch_contents = (
        f"a version of that list filtered down to the {ndrecs} cases that seem dubious"
    )
    para2_contents = ["Here is ", uxlc_utils_html.anchor(anch_contents, anch_attr), "."]
    return [
        uxlc_utils_html.para(para1_contents),
        uxlc_utils_html.para(para2_contents),
    ]


def _has_dem(record):
    return record.get("dubious early mtg")


if __name__ == "__main__":
    main()
