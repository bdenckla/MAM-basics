"""
    Base Usage:
    ./py/venv/Scripts/python.exe ./py/main_download_mam_fr_google.py
"""

import argparse

import requests

from pycmn import file_io
from py_misc.check_mpp import check_mpp
from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import mam_csv_in
import main_parse_go
from pycmn import bib_locales as tbn


def _download_section(secid):
    gurl_part_with_gid = f"pub?output=csv&gid={_GURL_GIDS[secid]}"
    rurl = "/".join((_GURL_BASE, _GURL_ID, gurl_part_with_gid))
    result_of_get = requests.get(rurl, timeout=10)
    result_of_get.encoding = "utf-8"
    text = result_of_get.text
    out_path = mam_csv_in.csv_path(secid)
    my_utils_fm.show_progress_g(__file__, out_path)
    file_io.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def main():
    """Download all 6 MAM sections from its Google Sheet, then parse and check."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading; just parse and check existing CSVs",
    )
    args = parser.parse_args()
    if not args.skip_download:
        for secid in tbn.ALL_SECIDS:
            _download_section(secid)
    all_plus_paths = main_parse_go.main()
    errors = check_mpp(all_plus_paths)
    if errors:
        print(f"check_mpp found {len(errors)} error(s):")
        for plus_path, error in errors:
            print(f"  {error[0]} in {plus_path}: {error[1]!r}")
        raise SystemExit(1)


# GURL: Google URL
_GURL_BASE = "https://docs.google.com/spreadsheets/d/e"
_GURL_ID = (  # ID for the (multi-tab) Google Sheets document as a whole
    "2PACX-1vQrnXDxQJ3pojK_9K4TiRwCpz-"
    "NCMmW5mWE9fH5ITpV0IF9aV4-"
    "XVtmShTyyIoB_PGRCk4o_YQYWPsU"
)
_GURL_GIDS = {  # IDs for the six individual tabs (sheets) of interest
    tbn.SEC_KET_AX: 676395561,
    tbn.SEC_XAM_MEG: 1916056224,
    tbn.SEC_SIF_EM: 1914969313,
    tbn.SEC_NEV_AX: 2069542406,
    tbn.SEC_NEV_RISH: 779581656,
    tbn.SEC_TORAH: 957434826,
}


if __name__ == "__main__":
    main()
