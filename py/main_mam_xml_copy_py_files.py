""" Exports main """

import shutil
import os

_PY_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_DIR = os.path.dirname(_PY_DIR)


def main():
    """
    Copy files to the MAM-simple repo.
    """
    mam_xml_pyex = os.path.join(_REPO_DIR, MAM_XML_PYEX)
    if os.path.exists(mam_xml_pyex):
        shutil.rmtree(mam_xml_pyex)
    os.makedirs(mam_xml_pyex)
    os.makedirs(f"{mam_xml_pyex}/py_misc")
    os.makedirs(f"{mam_xml_pyex}/pycmn")
    os.makedirs(f"{mam_xml_pyex}/pysefaria")
    os.makedirs(f"{mam_xml_pyex}/pyws")
    for pyfile_relpath in PYFILE_RELPATHS:
        src = os.path.join(_PY_DIR, pyfile_relpath)
        dst = f"{mam_xml_pyex}/{pyfile_relpath}"
        shutil.copy(src, dst)


MAM_XML_PYEX = "../MAM-simple/py-example"
PYFILE_RELPATHS = (
    "./main_mam4sef.py",
    #
    "pycmn/cantsys.py",
    "pycmn/hebrew_accents.py",
    "pycmn/hebrew_letters.py",
    "pycmn/hebrew_points.py",
    "pycmn/hebrew_punctuation.py",
    "pycmn/bib_locales.py",
    "pycmn/file_io.py",
    "pycmn/shrink.py",
    "pycmn/str_defs.py",
    "pycmn/uni_heb.py",
    "pycmn/my_utils.py",
    #
    "py_misc/my_html.py",
    "py_misc/my_html_get_lines.py",
    "py_misc/my_utils_for_mainish.py",
    "py_misc/osis_book_abbrevs.py",
    "py_misc/two_col_css_styles.py",
    "py_misc/verse_and_friends.py",
    "py_misc/write_utils.py",
    "py_misc/ws_urls.py",
    #
    "pysefaria/sef_header.py",
    "pysefaria/mam4sef_handlers.py",
    "pysefaria/mam4sef_or_ajf.py",
    "pysefaria/sef_cmn.py",
    "pysefaria/write_utils_sef_or_ajf.py",
)


if __name__ == "__main__":
    main()
