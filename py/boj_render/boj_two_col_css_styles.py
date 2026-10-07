from mb_misc.styles_mam_with_doc import make_css_file_for_mwd as make_css_file_for_mwd
from boj_render.two_col_css_styles_a import AUTHORED_STYLES_STR


def make_css_file_for_authored(out_path):
    with open(out_path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write(AUTHORED_STYLES_STR.lstrip())


def make_css_file_for_authored_wide(out_path):
    with open(out_path, "w", encoding="utf-8", newline="") as out_fp:
        out_fp.write(_AUTHORED_STYLES_STR_WIDE.lstrip())


_AUTHORED_STYLES_STR_WIDE = AUTHORED_STYLES_STR + "\nbody { max-width: 80em; }\n"
