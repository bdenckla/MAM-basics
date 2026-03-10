"""
Parse downloaded Google Sheets MAM data into increasingly structured formats.

Also exports do_one_section, which is called directly by
main_download_fr_google.py as part of the download pipeline.
"""

import collections

from py_misc import mam_csv_in
from py_misc import mam_parsed_plus
from pycmn import bib_locales as tbn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import file_io
from py_misc import my_utils_for_mainish as my_utils_fm


def _add_header(light_books):
    he_bns = {}  # we use a dict as a set that preserves insertion order
    he_sbns = collections.defaultdict(list)
    chap_cnts = []
    book39s = []
    for (he_bn, he_sbn), chapters in light_books.items():
        he_bns[he_bn] = True  # True is a dummy ("don't care") value
        if he_sbn is not None:
            he_sbns[he_bn].append(he_sbn)
        basic = {"book24_name": he_bn, "sub_book_name": he_sbn}
        chap_cnts.append(dict(basic, chapter_count=len(chapters)))
        book39s.append(dict(basic, chapters=chapters))
    header = {
        "book24_names": tuple(he_bns.keys()),
        "sub_book_names": he_sbns,
        "chapter_counts": chap_cnts,
    }
    return {"header": header, "book39s": book39s}


def do_one_section(secid, outfolder, mam_info=None):
    """
    For the CSV for the section with ID secid, this function parses the
    Wikitext inside the CSV and outputs that to a JSON file.
    """
    my_utils_fm.show_progress_g(__file__, outfolder, "section", secid)
    light_books = mam_csv_in.read_section_from_csv_lightly(secid, mam_info)
    bk24s = {}
    for he_bn_sbn, light_book_contents in light_books.items():
        bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
        bk24id = tbn.bk24id(bk39id)
        if bk24id not in bk24s:
            bk24s[bk24id] = {}
        assert he_bn_sbn not in bk24s[bk24id]
        bk24s[bk24id][he_bn_sbn] = light_book_contents
    out_paths_for_section = []
    for bk24id, light_books_in_bk24 in bk24s.items():
        out_paths_for_bk24 = _do_light_books_in_bk24(
            outfolder, bk24id, light_books_in_bk24
        )
        out_paths_for_section.append(out_paths_for_bk24)
    return out_paths_for_section


def _do_light_books_in_bk24(outfolder, bk24id, light_books):
    lb_with_hdr = _add_header(light_books)
    lb_with_hdr_plus = mam_parsed_plus.add_plus_stuff(lb_with_hdr)
    osdf24 = tbn.ordered_short_dash_full_24(bk24id)
    out_path_plain = f"{outfolder}/plain/{osdf24}.json"
    out_path_plus = f"{outfolder}/plus/{osdf24}.json"
    file_io.json_dump_to_file_path(lb_with_hdr, out_path_plain)
    file_io.json_dump_to_file_path(lb_with_hdr_plus, out_path_plus)
    return {"plus": out_path_plus, "plain": out_path_plain}


def main():
    """
    For each of the 6 CSVs (one per section), this program parses the
    Wikitext inside the CSV and outputs that to a JSON file.
    """
    outfolder = "../MAM-parsed"
    all_plus_paths = []
    for secid in tbn.ALL_SECIDS:
        out_paths_for_section = do_one_section(secid, outfolder)
        for out_paths_for_bk24 in out_paths_for_section:
            all_plus_paths.append(out_paths_for_bk24["plus"])
    return all_plus_paths


if __name__ == "__main__":
    main()
