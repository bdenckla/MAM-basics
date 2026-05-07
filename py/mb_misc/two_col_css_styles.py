from py_misc.two_col_css_styles_m import MWD_STYLES_STR
from py_misc.two_col_css_styles_a import AUTHORED_STYLES_STR
from py_misc.two_col_css_styles_a import MAMP_EXTRA_CSS


def make_css_file_for_mwd(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(MWD_STYLES_STR.lstrip())


def make_css_file_for_authored(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(AUTHORED_STYLES_STR.lstrip())


def make_css_file_for_mam_parsed(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(AUTHORED_STYLES_STR.lstrip())
        out_fp.write(MAMP_EXTRA_CSS.lstrip())
