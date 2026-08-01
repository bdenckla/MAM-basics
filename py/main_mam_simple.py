"""Make a simple but incomplete extract of MAM in XML and JSON formats.

The XML format is not OSIS, but is informed by OSIS; the JSON format mirrors
the XML structure.  Both are written for each of the three versification
variants (BHS, Sefaria, MAM's own).

Subcommands:
    all
                Run the core MAM-simple export and then regenerate the
                versification docs.  This is what runs when no subcommand is
                given at all, so the bare command line is the whole job.
    core-only
    core
                Run only the core MAM-simple export, leaving the versification
                docs alone.  `core` is an alias for `core-only`.
    doc-only
    doc
                Regenerate only the versification docs -- the versification
                differences doc and the versification-and-cantillation doc --
                each rewritten only if its content changed.  `doc` is an alias
                for `doc-only`.
    copy-support-files
    copy
                Copy the support files into the MAM-simple repo, without
                exporting anything.  `copy` is an alias for
                `copy-support-files`; the `all` and `core-only` exports finish
                by doing this themselves.

`all`, `core-only` and `core` accept --book39 or --section6 to restrict the
export to one book or one section; the default is all 39 books.

Usage (run from repo root):
    .venv/Scripts/python.exe py/main_mam_simple.py
    .venv/Scripts/python.exe py/main_mam_simple.py --book39 Ruth
    .venv/Scripts/python.exe py/main_mam_simple.py core-only --book39 Ruth
    .venv/Scripts/python.exe py/main_mam_simple.py doc-only
    .venv/Scripts/python.exe py/main_mam_simple.py copy-support-files
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
from versification_and_cantillation import generate_doc as vc_generate_doc


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
    xml_path = write_utils.bkg_path(variant, bkg["bkg-name"], out_subdir="")
    write_utils_xml.write_root_in_xml_fmt(xml_path, xml_root, generator_file=__file__)
    json_root = json_root_from_bksams.root(bksams, vtrad_val, variant)
    json_path = write_utils.bkg_path(
        variant, bkg["bkg-name"], fmt_override="vff-json", out_subdir=""
    )
    write_utils_json.write_root_in_json_fmt(
        json_path, json_root, generator_file=__file__
    )
    verses_for_write = {"rv-cant-all-three": bkg_rendered}
    write_utils.write_bkg_in_un_fmt(
        variant,
        bkg["bkg-name"],
        verses_for_write,
        "rv-cant-all-three",
        out_subdir="misc",
        generator_file=__file__,
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
    for gen in (generate_doc, vc_generate_doc):
        did_write = gen.write_output_if_changed()
        status = "updated" if did_write else "already up to date"
        print(f"{status}: {gen.output_path()}")


def build_parser():
    """The fully-configured parser, so a test can read the subcommands off it."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    subparsers.add_parser(
        "copy-support-files",
        aliases=["copy"],
        help="Copy support files to the MAM-simple repo.",
    )
    return parser


def _add_core_args(parser):
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument("--book39")
    mutex.add_argument("--section6")
    return parser


_SUBCOMMAND_NAMES = frozenset(
    {
        "all",
        "core-only",
        "core",
        "doc-only",
        "doc",
        "copy-support-files",
        "copy",
    }
)


def _parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    # A command line that does not open with a subcommand name means `all`, so that the
    # bare command line is the whole job.  A help flag is the exception: prepending
    # `all` to it answers with the `all` subparser's own help, and the module docstring
    # -- the only place the subcommands are listed -- would then have no spelling that
    # displays it at all.
    if not argv or (
        argv[0] not in _SUBCOMMAND_NAMES and argv[0] not in ("-h", "--help")
    ):
        argv = ["all", *argv]
    return build_parser().parse_args(argv)


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
    if args.command in {"copy-support-files", "copy"}:
        mam_simple_copy_py_files.copy_support_files()
        return
    bkids = _bkids_from_args(args)
    almost_main(bkids)
    if args.command == "all":
        _write_versification_doc()


if __name__ == "__main__":
    main()
