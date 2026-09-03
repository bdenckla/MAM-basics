"""Exports main"""

import sys
import uxlc_misc.my_uxlc as my_uxlc
import uxlc_misc.my_uxlc_page_break_info as page_break_info
import uxlc_lci.uxlc_lci_augrec as lci_augrec
import uxlc_lci.uxlc_lci_rec_to_xml as lci_rec_to_xml
import mb_cmn.file_io as my_open
import uxlc_paths


def _write_page_break_info(pbi):
    lciars = page_break_info.get_lci_augrecs(pbi)
    lciars_f = lci_augrec.flatten_many2(lciars)
    json_output_path1 = uxlc_paths.out_uxlc_misc_dir() / "lci_augrecs.json"
    my_open.json_dump_to_file_path(lciars_f, json_output_path1)
    my_open.json_dump_to_file_path(lciars_f, uxlc_paths.data_dir() / "lci_augrecs.json")
    #
    pg_lens = page_break_info.get_page_lengths(pbi)
    pg_lens_f = lci_augrec.flatten_page_lengths(pg_lens)
    json_output_path2 = uxlc_paths.out_uxlc_misc_dir() / "page_counts.json"
    my_open.json_dump_to_file_path(pg_lens_f, json_output_path2)
    #
    lci_recs_dot_json = page_break_info.read_lci_recs_dot_json()
    xml_elementtree = lci_rec_to_xml.get_etree(lci_recs_dot_json)

    xml_out_path = uxlc_paths.out_uxlc_misc_dir() / "lci_recs.xml"
    my_open.with_tmp_openw(
        xml_out_path, {"newline": ""}, _etree_write_callback, xml_elementtree
    )


def _etree_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding="unicode")
    out_fp.write("\n")


def main():
    """
    Write page break info to files.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    uxlc = my_uxlc.read_all_books()
    pbi = page_break_info.read_in(uxlc)
    _write_page_break_info(pbi)


if __name__ == "__main__":
    main()
