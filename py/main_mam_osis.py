"""Convert MAM data to OSIS (Open Scripture Information Standard) XML format."""

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_misc import my_utils_for_mainish as my_utils_fm
from osis import osis_runner

_PATHS = {
    "input_xml_dir": str(paths.sibling_repo("MAM-simple") / "xml-vtrad-bhs"),
    "output_book_dir": str(paths.sibling_repo("MAM-OSIS") / "MAPM-24"),
    "header_path": str(paths.sibling_repo("MAM-OSIS") / "header.xml"),
    "osis_output_path": str(paths.sibling_repo("MAM-OSIS") / "mapm.osis.xml"),
    "xsd_path": str(paths.repo_root() / "in" / "osisCore.2.1.1-cw6.xsd"),
    # The XSD above imports the XML namespace's schema from w3.org by absolute URL.
    # Pointing that import at our vendored copy is what lets OSIS validation run with
    # no network at all; see osis_runner._XmlNamespaceXsdResolver for the failure it
    # replaces.
    "xml_xsd_path": str(paths.repo_root() / "in" / "xml.xsd"),
    "index_html_dir": str(paths.sibling_repo("MAM-OSIS") / "gh-pages"),
}


def almost_main(bkids=None):
    """Create MAM-OSIS from MAM-XML."""
    if bkids is None:
        bkids = tbn.ALL_BK39_IDS
    osis_runner.almost_main(_PATHS, bkids)


def main():
    """Create MAM-OSIS from MAM-XML."""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    almost_main(bkids)


if __name__ == "__main__":
    main()
