"""
Exports main

Usage (run from repo root):
    cd ~/GitRepos/MAM-basics && PYTHONUTF8=1 .venv/Scripts/python.exe py/main_mam_simple.py
    cd ~/GitRepos/MAM-basics && PYTHONUTF8=1 .venv/Scripts/python.exe py/main_mam_simple.py --book39 Ruth
"""

from py_misc import my_utils_for_mainish as my_utils_fm
from pycmn import read_books_from_mam_parsed_plus as plus
from py_misc import write_utils_xml
from py_misc import write_utils_json
from py_misc import osis_book_abbrevs
from py_misc import vtrad
from py_misc import write_utils
from py_misc import ren_tag_survey as rts
from pycmn import bib_locales as tbn
from pyxml import xml_render
from pyxml import xml_root_from_bksams
from pyxml import xml_distribute_sampe as xml_sampe
from pyjson import json_root_from_bksams


def _do_not_convert(_bkids, books_mpp):
    return books_mpp


_VARIANT_COMMON = {
    "variant-mam-for-xxx": "MAM-simple",
    "variant-file-format": "vff-xml",
}
_VARIANT_VTBHS = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": vtrad.convert_to_bhs,
    "variant-path-qual": "vpq-vtrad-bhs",
}
_VARIANT_VTSEF = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": vtrad.convert_to_sef,
    "variant-path-qual": "vpq-vtrad-sef",
}
_VARIANT_VTMAM = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": _do_not_convert,
    "variant-path-qual": "vpq-vtrad-mam",
    "variant-alt-id": "variant-alt-id-value-yeivin",
}
_VARIANTS = _VARIANT_VTBHS, _VARIANT_VTSEF, _VARIANT_VTMAM


def _do_one_book_group(bkg, books_mpp, variant):
    """Do one book group (do one bkg)"""
    convert_vtrad = variant["variant-convert-vtrad"]
    books_mpp_tx = convert_vtrad(bkg["bkg-bkids"], books_mpp)
    bkg_rendered = []
    survey_for_all_bks = rts.make()
    for bkid in bkg["bkg-bkids"]:
        book_rendered, survey_for_one_bk = xml_render.render_to_xml(books_mpp_tx, bkid)
        bkg_rendered.extend(book_rendered)
        survey_for_all_bks = rts.add(survey_for_all_bks, survey_for_one_bk)
    _finish_one_book_group(bkg, bkg_rendered, variant)
    return survey_for_all_bks


def _finish_one_book_group(bkg, bkg_rendered, variant):
    bksams = xml_sampe.distribute_sampe(bkg_rendered)
    vtrad_val = _get_vtrad(bkg_rendered)
    xml_root = xml_root_from_bksams.root(bksams, vtrad_val, variant)
    xml_path = write_utils.bkg_path(variant, bkg["bkg-name"])
    write_utils_xml.write_root_in_xml_fmt(xml_path, xml_root)
    json_root = json_root_from_bksams.root(bksams, vtrad_val, variant)
    json_path = write_utils.bkg_path(variant, bkg["bkg-name"], fmt_override="vff-json")
    write_utils_json.write_root_in_json_fmt(json_path, json_root)
    verses_for_write = {"rv-cant-all-three": bkg_rendered}
    write_utils.write_bkg_in_un_fmt(
        variant, bkg["bkg-name"], verses_for_write, "rv-cant-all-three"
    )


def _get_vtrad(verses):
    bcvt = verses[0][0]
    vtrad_val = tbn.bcvt_get_vtrad(bcvt)
    return vtrad_val


def _show_progress(variant, bkg_name):
    path_qual = variant["variant-path-qual"]
    rest = path_qual, "book group", bkg_name
    my_utils_fm.show_progress_g(__file__, *rest)


def main():
    """
    Make a simple but incomplete extract of MAM in XML and JSON formats.
    The XML format is not OSIS, but is informed by OSIS.
    The JSON format mirrors the XML structure.
    """
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    books_mpp = plus.read_parsed_plus_bk39s(bkids)
    bkgs = osis_book_abbrevs.bk24_bkgs(bkids)
    survey_for_all_bkgs = rts.make()
    for variant in _VARIANTS:
        for bkg in bkgs:
            _show_progress(variant, bkg["bkg-name"])
            survey_for_one_bkg = _do_one_book_group(bkg, books_mpp, variant)
            survey_for_all_bkgs = rts.add(survey_for_all_bkgs, survey_for_one_bkg)
    xml_render.handle_survey_results(bkids, survey_for_all_bkgs)


if __name__ == "__main__":
    main()
