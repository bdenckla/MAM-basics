"""
Generate the MAM-with-doc HTML output — two-column pages showing the MAM
text alongside its Wikisource documentation notes, one HTML file per book.
"""

from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import ren_tag_survey as rts
from py_misc import mwd_utils as mwdu
from pycmn import bib_locales as tbn
from pycmn import read_books_from_mam_parsed_plus as plus
from pymwd import mwd_write_index_dot_html as mwdwidh
from pymwd import mwd_write_book as mwdwb
from py_misc import two_col_css_styles as tcstyles


def _out_path(filename):
    # Below, the “docs” folder name is for GitHub pages purposes. I.e. GitHub
    # considers all of “MAM with doc” to be “docs” since that what GitHub
    # pages is often used for (documentation for software whose sources are
    # versioned in the same repo). In other words, the “doc” in “docs” below
    # is different from the “doc” in “MAM with doc”.
    return f"../MAM-with-doc/docs/{filename}"


def _handle_survey_results(bkids, survey):
    if bkids != tbn.ALL_BK39_IDS:
        return
    ren_tags_seen = rts.get_ren_tags_seen(survey)
    ren_tags_wets = set(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC)
    _survey_results_helper(ren_tags_seen, ren_tags_wets, "render tags")


def _survey_results_helper(seen, wets, name):
    diff = wets - seen
    if diff:
        print(f"{name} expected but not seen: ", sorted(diff))
    assert not diff


def _get_out_paths(bkid):
    path_for_main = _out_path(mwdu.filename_for_bkid(bkid))
    path_for_bido = _out_path(mwdu.filename_for_bkid_for_bido(bkid))
    return path_for_main, path_for_bido


def almost_main(bkids=None):
    """Create a version of MAM intended for deployment to
    MAM-with-doc public GitHub repo"""
    if bkids is None:
        bkids = tbn.ALL_BK39_IDS
    books_mpp = plus.read_parsed_plus_bk39s(bkids)
    edition = "MAM with doc"
    css_href = "two_col_style.css"
    tcstyles.make_css_file_for_mwd(_out_path(css_href))
    if bkids == tbn.ALL_BK39_IDS:
        mwdwidh.write_index_dot_html(edition, (css_href,), _out_path("index.html"))
    survey_for_all_bks = rts.make()
    for bkid in bkids:
        ecb = edition, (css_href,), bkid
        survey_for_one_bk = mwdwb.write_book(ecb, books_mpp, _get_out_paths(bkid))
        survey_for_all_bks = rts.add(survey_for_all_bks, survey_for_one_bk)
    _handle_survey_results(bkids, survey_for_all_bks)


def main():
    """Create a version of MAM intended for deployment to
    MAM-with-doc public GitHub repo"""
    bkids = my_utils_fm.get_bk39_tuple_from_argparse()
    almost_main(bkids)


if __name__ == "__main__":
    main()
