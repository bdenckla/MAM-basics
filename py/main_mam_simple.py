"""Make a simple but incomplete extract of MAM in XML and JSON formats.

The XML format is not OSIS, but is informed by OSIS; the JSON format mirrors
the XML structure.  Both are written for each of the three versification
variants (BHS, Sefaria, MAM's own).

Subcommands:
    all
                Run the core MAM-simple export and then regenerate the docs
                this repo writes under MAM-simple/.  This is what runs when no
                subcommand is given at all, so the bare command line is the
                whole job.
    core-only
    core
                Run only the core MAM-simple export, leaving the versification
                docs alone.  `core` is an alias for `core-only`.
    doc-only
    doc
                Regenerate only the docs -- the versification differences doc,
                the versification-and-cantillation doc, and the gh-pages index
                -- each rewritten only if its content changed.  `doc` is an
                alias for `doc-only`.
    copy-support-files
    copy
                Copy the support files into MAM-simple/py-examples/, without
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
from pathlib import Path

from mb_misc import my_utils_for_mainish as my_utils_fm
from py_misc import mam_simple_copy_py_files
from mb_cmn import paths
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
from py_misc import mam_simple_index


def _do_not_convert(_bkids, books_mpu):
    return books_mpu


_VARIANT_COMMON = {
    "variant-output-root": paths.repo_root() / "MAM-simple",
    "variant-file-format": "vff-xml",
}
_VARIANT_VTBHS = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": vtrad.convert_to_bhs,
    "variant-path-qual": "vpq-vtrad-bhs",
    "variant-vtrad": tbn.VT_BHS,
}
_VARIANT_VTSEF = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": vtrad.convert_to_sef,
    "variant-path-qual": "vpq-vtrad-sef",
    "variant-vtrad": tbn.VT_SEF,
}
_VARIANT_VTMAM = {
    **_VARIANT_COMMON,
    "variant-convert-vtrad": _do_not_convert,
    "variant-path-qual": "vpq-vtrad-mam",
    "variant-vtrad": tbn.VT_MAM,
    # The only variant that gets a Unicode-names rendering, and the only one that
    # ever did after 2026-09-12.  Ben's decision that day: "ditch the -bhs and -sef
    # versions of this 'unicode names' pseudo-edition", and, on being asked whether
    # that meant the data alone, "by 'ditch' I mean not only remove the data, but
    # make the code cease to generate them".  The two retired trees were
    # MAM-simple/misc/unicode-names-vtrad-bhs/ and -sef/, 9.78 MB each.  They were
    # near-duplicates of the -mam tree: measured that day, 18 of the 24 bhs book
    # groups and 19 of the 24 sef ones were identical to their -mam counterpart but
    # for the vtrad token in each verse's header line.
    "variant-writes-unicode-names": True,
}
# NO ORDER IS LOAD-BEARING.  For a few hours on 2026-09-12 vtmam had to come first,
# because the incremental storage below was implemented by writing every bhs and sef
# file and then deleting the ones a comparison with the vtmam file showed to be
# redundant.  Ben rejected that: "It feels like your plan generates entire editions and
# asks where they differ in terms of versification, whereas the only question that needs
# answering is how the versifications differ."  vtrad.bk24s_differing_from_mam answers
# that question from the versification tables, so each variant now knows its own file
# list before anything is written and no variant reads another's output.
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
    # The variant declares its vtrad and the rendered verses carry it; a mismatch would
    # mean variant-convert-vtrad and variant-vtrad had come apart.
    assert _get_vtrad(bkg_rendered) == variant["variant-vtrad"]
    xml_path = write_utils.bkg_path(variant, bkg["bkg-name"], out_subdir="")
    json_path = write_utils.bkg_path(
        variant, bkg["bkg-name"], fmt_override="vff-json", out_subdir=""
    )
    if _stores_own_file(bkg, variant):
        vtrads = _vtrads_served(bkg, variant)
        write_utils_xml.write_root_in_xml_fmt(
            xml_path,
            xml_root_from_bksams.root(bksams, vtrads, variant),
            generator_file=__file__,
        )
        write_utils_json.write_root_in_json_fmt(
            json_path,
            json_root_from_bksams.root(bksams, vtrads, variant),
            generator_file=__file__,
        )
    else:
        _remove_stale(xml_path)
        _remove_stale(json_path)
    if variant.get("variant-writes-unicode-names"):
        verses_for_write = {"rv-cant-all-three": bkg_rendered}
        write_utils.write_bkg_in_un_fmt(
            variant,
            bkg["bkg-name"],
            verses_for_write,
            "rv-cant-all-three",
            out_subdir="misc",
            generator_file=__file__,
        )


def _stores_own_file(bkg, variant):
    """Whether this variant keeps this book group in a file of its own.

    THE BHS AND SEF CORPORA ARE STORED INCREMENTALLY AGAINST THE MAM ONE, on Ben's
    instruction of 2026-09-12: "move to a system where -bhs and -sef versions only exist
    for books whose files differ from the -mam version.  I.e. move to an 'incremental'
    storage system, with -mam as the base."  A book group absent from xml-vtrad-bhs/ or
    json-vtrad-sef/ is one whose cv-labels that tradition places exactly where MAM
    places them, and the vtmam file is the one to read; MAM-simple's README and
    doc/reading-mam-simple.md state that reading rule for a consumer.
    """
    vtrad_val = variant["variant-vtrad"]
    if vtrad_val == tbn.VT_MAM:
        return True
    return _bk24id(bkg) in vtrad.bk24s_differing_from_mam(vtrad_val)


def _vtrads_served(bkg, variant):
    """The root's versification-tradition value: every tradition these labels are right for.

    A COMMA-SEPARATED SET, not a single tradition, since 2026-09-12.  Ben's decision that
    day, on being told that a consumer falling back to a vtmam file would find it saying
    versification-tradition="vtmam" rather than naming the versification it asked for:
    "What do you think of, for these files, being clear about what they are by saying
    versification-tradition='vtmam,vtbhs,vtsef'?"

    So 18 of the 24 vtmam files say vtmam,vtbhs,vtsef; Numbers says vtmam,vtsef, Sefaria
    agreeing with MAM there where BHS does not; and the five whose labels both other
    traditions place differently say vtmam alone.  A bhs or sef file says its own
    tradition, which is the same rule with a one-element answer.

    EVERY VALUE EVER WRITTEN STAYS TRUTHFUL under this reading, which is why it is a
    widening rather than a redefinition: before the incremental storage each variant had
    its own file for every book group, and "vtmam" did then mean {vtmam} for that file.
    """
    vtrad_val = variant["variant-vtrad"]
    if vtrad_val != tbn.VT_MAM:
        return vtrad_val
    bk24id = _bk24id(bkg)
    also_served = [
        other
        for other in (tbn.VT_BHS, tbn.VT_SEF)
        if bk24id not in vtrad.bk24s_differing_from_mam(other)
    ]
    return ",".join([tbn.VT_MAM, *also_served])


def _bk24id(bkg):
    return tbn.bk24id(bkg["bkg-bkids"][0])


def _remove_stale(path):
    """Remove a file this variant no longer stores, if an earlier run left one.

    Not a write-then-delete: nothing here writes the path first.  It fires only when the
    versification tables have changed such that a book group this variant used to differ
    on now agrees with MAM, which would otherwise leave a stale file that no diff would
    show, the file being unchanged.
    """
    Path(path).unlink(missing_ok=True)


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
    books_mpu = plus.read_parsed_plus_bk39s(bkids, paths.mam_parsed_path())
    bkgs = osis_book_abbrevs.bk24_bkgs(bkids)
    survey_for_all_bkgs = rts.make()
    for variant in _VARIANTS:
        for bkg in bkgs:
            _show_progress(variant, bkg["bkg-name"])
            survey_for_one_bkg = _do_one_book_group(bkg, books_mpu, variant)
            survey_for_all_bkgs = rts.add(survey_for_all_bkgs, survey_for_one_bkg)
    xml_render.handle_survey_results(bkids, survey_for_all_bkgs)
    mam_simple_copy_py_files.copy_support_files()


def write_generated_docs():
    """Rewrite each doc this program generates, only where its content changed.

    The doc-only half of this program: MAM-simple/doc/versification-differences.md,
    gh-pages/MAM-simple/versification-and-cantillation.html with its CSS and font,
    and gh-pages/MAM-simple/index.html.  Public since 2026-09-10, when
    py/main_0_mega.py's mam-simple-docs step began calling it; that module's
    mam-simple step runs almost_main, which does not reach these docs.
    """
    # Named for the docs generally rather than for versification: mam_simple_index
    # writes the gh-pages root pointer, which is about neither versification nor
    # cantillation.
    for gen in (generate_doc, vc_generate_doc, mam_simple_index):
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
            help="Run the core MAM-simple export and then regenerate the docs.",
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
        help="Regenerate only the docs, leaving the export alone.",
    )
    subparsers.add_parser(
        "copy-support-files",
        aliases=["copy"],
        help="Copy support files to the MAM-simple product directory.",
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
        write_generated_docs()
        return
    if args.command in {"copy-support-files", "copy"}:
        mam_simple_copy_py_files.copy_support_files()
        return
    bkids = _bkids_from_args(args)
    almost_main(bkids)
    if args.command == "all":
        write_generated_docs()


if __name__ == "__main__":
    main()
