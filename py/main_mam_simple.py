"""Make a simple but incomplete extract of MAM in XML and JSON formats.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_mam_simple.py
    .venv/Scripts/python.exe py/main_mam_simple.py --book39 Ruth
    .venv/Scripts/python.exe py/main_mam_simple.py core-only --book39 Ruth
    .venv/Scripts/python.exe py/main_mam_simple.py doc-only
"""

import argparse
import sys

from mb_misc import my_utils_for_mainish as my_utils_fm
from py_misc import mam_simple_copy_py_files
from mb_cmn import read_books_from_mam_parsed_plus as plus
from py_misc import write_utils_xml
from py_misc import write_utils_json
from mb_misc import osis_book_abbrevs
from py_misc import vtrad
from mb_misc import write_utils
from py_misc import ren_tag_survey as rts
from mb_cmn import bib_locales as tbn
from mb_xml import xml_render
from mb_xml import xml_root_from_bksams
from mb_xml import xml_distribute_sampe as xml_sampe
from mb_json import json_root_from_bksams
from versification_differences import generate_doc


def _do_not_convert(_bkids, books_mpu):
    return books_mpu


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


def _do_one_book_group(bkg, books_mpu, variant):
    """Do one book group (do one bkg)"""
    convert_vtrad = variant["variant-convert-vtrad"]
    books_mpu_tx = convert_vtrad(bkg["bkg-bkids"], books_mpu)
    bkg_rendered = []
    survey_for_all_bks = rts.make()
    for bkid in bkg["bkg-bkids"]:
        book_rendered, survey_for_one_bk = xml_render.render_to_xml(books_mpu_tx, bkid)
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
    write_utils_json.write_root_in_json_fmt(
        json_path, json_root, generator_file=__file__
    )
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


def almost_main(bkids=None):
    """
    Make a simple but incomplete extract of MAM in XML and JSON formats.
    The XML format is not OSIS, but is informed by OSIS.
    The JSON format mirrors the XML structure.
    """
    if bkids is None:
        bkids = tbn.ALL_BK39_IDS
    books_mpu = plus.read_parsed_plus_bk39s(bkids)
    bkgs = osis_book_abbrevs.bk24_bkgs(bkids)
    survey_for_all_bkgs = rts.make()
    for variant in _VARIANTS:
        for bkg in bkgs:
            _show_progress(variant, bkg["bkg-name"])
            survey_for_one_bkg = _do_one_book_group(bkg, books_mpu, variant)
            survey_for_all_bkgs = rts.add(survey_for_all_bkgs, survey_for_one_bkg)
    xml_render.handle_survey_results(bkids, survey_for_all_bkgs)
    mam_simple_copy_py_files.copy_support_files()


def _write_versification_doc():
    did_write = generate_doc.write_output_if_changed()
    if did_write:
        print(f"updated: {generate_doc.output_path()}")
    else:
        print(f"already up to date: {generate_doc.output_path()}")


def _build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    _add_core_args(
        subparsers.add_parser(
            "all",
            help="Run the core MAM-simple export and then regenerate the versification doc.",
        )
    )
    _add_core_args(
        subparsers.add_parser(
            "core-only",
            aliases=["core"],
            help="Run only the core MAM-simple export.",
        )
    )
    subparsers.add_parser(
        "doc-only",
        aliases=["doc"],
        help="Regenerate only the versification differences doc.",
    )
    return parser


def _add_core_args(parser):
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument("--book39")
    mutex.add_argument("--section6")
    return parser


def _parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0] not in {"all", "core-only", "core", "doc-only", "doc"}:
        argv = ["all", *argv]
    return _build_parser().parse_args(argv)


def _bkids_from_args(args):
    if getattr(args, "book39", None):
        return (args.book39,)
    if getattr(args, "section6", None):
        return tbn.bk39s_of_sec(args.section6)
    return tbn.ALL_BK39_IDS


def main():
    args = _parse_args()
    if args.command in {"doc-only", "doc"}:
        _write_versification_doc()
        return
    bkids = _bkids_from_args(args)
    almost_main(bkids)
    if args.command == "all":
        _write_versification_doc()


if __name__ == "__main__":
    main()
