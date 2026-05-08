"""Convert MAM data to OSIS (Open Scripture Information Standard) XML format."""

from mb_cmn import bib_locales as tbn
from mb_misc import my_utils_for_mainish as my_utils_fm
from osis import osis_runner

_PATHS = {
    "input_xml_dir": "../MAM-simple/xml-vtrad-bhs",
    "output_book_dir": "../MAM-OSIS/MAPM-24",
    "header_path": "../MAM-OSIS/header.xml",
    "osis_output_path": "../MAM-OSIS/mapm.osis.xml",
    "xsd_path": "in/osisCore.2.1.1-cw6.xsd",
    "index_html_dir": "../MAM-OSIS/gh-pages",
}


def almost_main(bkids=None):
    """Create MAM-OSIS from MAM-XML."""
    if bkids is None:
        bkids = tbn.ALL_BK39_IDS
    osis_runner.almost_main(bkids, _PATHS)


def main():
    """Create MAM-OSIS from MAM-XML."""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    almost_main(bkids)


if __name__ == "__main__":
    main()
