"""
Download MAM data from Sefaria and write it to JSON files.

Usage:
    .venv/Scripts/python.exe py/main_download_fr_sefaria.py
    .venv/Scripts/python.exe py/main_download_fr_sefaria.py --book "I Kings"
"""

import requests

from py_misc import my_utils_for_mainish as my_utils_fm
from pysefaria import sef_cmn
from pycmn import file_io


def _download_book(sebn):  # sebn: Sefaria English Book Name
    base = "https://www.sefaria.org/download/version"
    lang = "he"
    version = "Miqra%20according%20to%20the%20Masorah"
    csv_url = f"{base}/{sebn}%20-%20{lang}%20-%20{version}.csv"
    result_of_get = requests.get(csv_url)
    out_path = f"in/mam-from-sefaria/{sebn}.csv"
    my_utils_fm.show_progress_g(__file__, out_path)
    text = result_of_get.text
    # repls = (
    #     (sd.NBSP, '&nbsp;'),
    #     (sd.THSP, '&thinsp;'),
    #     (WIKISOURCE_URL_HE, WIKISOURCE_URL_ENG)
    # )
    # for repl in repls:
    #     text = text.replace(*repl)
    file_io.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def main():
    """Download MAM books from Sefaria"""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    for bkid in bkids:
        sef_bkna = sef_cmn.SEF_BKNA[bkid]
        _download_book(sef_bkna)


if __name__ == "__main__":
    main()
