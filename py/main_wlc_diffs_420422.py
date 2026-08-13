"""Exports main."""

from wlc_cmn.utf8_io import force_utf8_io
import py_html.wlc_utils_html as wlc_utils_html
import py_wlc_diffs_420422.my_word_diffs_420422 as my_word_diffs_420422
import py_wlc_diffs_420422.my_word_diffs_420422_add_fields as my_word_diffs_420422_add_fields
import py_wlc_diffs_420422.my_word_diffs_420422_full as my_word_diffs_420422_full
import py_wlc_diffs_420422.my_word_diffs_420422_summary as my_word_diffs_420422_summary

_NOTE_DIFFS_JSON_URL = (
    "https://github.com/bdenckla/MAM-basics/blob/main/out/" "diff_mm_wlc420_wlc422.json"
)


def almost_main():
    """Writes 420-to-422 word diff survey to HTML files."""
    records = my_word_diffs_420422.RECORDS
    #
    my_word_diffs_420422_add_fields.add(records)  # mutates, i.e. modifies in-place
    #
    records = sorted(records, key=_sort_key_for_rec)
    #
    _set_prev_and_next(records, "prev", "next")
    #
    # Now we write various HTML files in a bottom-up (leaves first) fashion
    #
    my_word_diffs_420422_full.write(records)  # fills in path-to-full fields
    #
    records_r = list(filter(_is_reject, records))
    patiin_r = _path_and_title_and_intro_for_rejects(len(records_r))
    my_word_diffs_420422_summary.write(records_r, *patiin_r)
    #
    patiin_m = _path_and_title_and_intro_for_main(len(records), patiin_r[0])
    my_word_diffs_420422_summary.write(records, *patiin_m)


def _is_reject(record):
    return record.get("UXLC-rejected")


def _sort_key_for_rec(record):
    dity = record["diff-type"]
    return (1, "misc") if dity == "misc" else (0, dity)


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


def _path_and_title_and_intro_for_main(nrecs, rejects_path):
    para1_contents = (
        f"This page lists the {nrecs} words that differ between WLC 4.20 and 4.22."
    )
    link_to_rejects = [
        "Here is a similar ",
        wlc_utils_html.anchor(
            "page listing only those 4.22 changes rejected by UXLC",
            {"href": rejects_path},
        ),
        ".",
    ]
    # The word changes shown here are not the only 4.20-to-4.22 differences.
    # There are also note (bracket-note) changes, recorded but not surfaced on
    # any page. The count below is taken from the "notes differences" array of
    # the diff JSON named in _NOTE_DIFFS_JSON_URL; update it if that file is
    # regenerated.
    caveat = [
        "These word changes are not the only differences between WLC 4.20 "
        "and 4.22: there are also 196 note (bracket-note) changes, which can "
        "be seen in the ",
        wlc_utils_html.anchor(
            "notes differences section of diff_mm_wlc420_wlc422.json",
            {"href": _NOTE_DIFFS_JSON_URL},
        ),
        ".",
    ]
    intro = [
        wlc_utils_html.para(para1_contents),
        wlc_utils_html.para(link_to_rejects),
        wlc_utils_html.para(caveat),
    ]
    title = "WLC 4.22 Changes"
    return "index.html", title, intro


def _path_and_title_and_intro_for_rejects(nrecs):
    para1_contents = (
        f"This page lists the {nrecs} WLC 4.22 changes that were rejected by UXLC."
    )
    intro = [wlc_utils_html.para(para1_contents)]
    title = "WLC 4.22 Changes Rejected by UXLC"
    return "index-rejects.html", title, intro


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
