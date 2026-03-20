"""
Generate miscellaneous authored HTML documents (notes, reviews, analyses)
that are written by the repo owner and rendered from Python source data.
"""

from py_misc import two_col_css_styles as tcstyles
from pyauthor import notes_on_aliyot
from pyauthor import tsinnorit_and_oleh_on_ivs
from pyauthor import tsinnorit_and_oleh_facts
from pyauthor import tsinnorit_in_psalm_32v5
from pyauthor import tsinnorit_and_the_xxd_in_bhs
from pyauthor import rocc_0_review_of_ctr
from pyauthor import rocc_1_on_the_provenance_of_ctr
from pyauthor import rocc_2_pre_vowel_accents_in_ctr
from pyauthor import rocc_3_where_other_sources_stand
from pyauthor import rocc_4_mid_word_ga3ya_with_shewa
from pyauthor import gray_maqaf
from pyauthor import the_next_700_bibles


def almost_main():
    # XXX TODO: rm *.html (to avoid stale files when output names change)
    docs_dir = "../MAM-with-doc/docs"
    top_dir_misc = f"{docs_dir}/misc"
    top_dir_old = f"{docs_dir}/tsinnorit_oleh"
    top_dir_aliyot = f"{docs_dir}/aliyot"
    #
    css_href = "style.css"
    css_href_wide = "style_wide.css"
    tcstyles.make_css_file_for_authored(f"{top_dir_misc}/{css_href}")
    tcstyles.make_css_file_for_authored_wide(f"{top_dir_misc}/{css_href_wide}")
    #
    tdm_ch = top_dir_misc, css_href
    tdm_ch_wide = top_dir_misc, css_href_wide
    #
    tdm_ch_aliyot = top_dir_aliyot, "aliyot-styles.css"
    notes_on_aliyot.gen_html_file(tdm_ch_aliyot)
    tsinnorit_and_oleh_on_ivs.gen_html_file(tdm_ch, top_dir_old)
    tsinnorit_and_oleh_facts.gen_html_file(tdm_ch)
    tsinnorit_in_psalm_32v5.gen_html_file(tdm_ch)
    tsinnorit_and_the_xxd_in_bhs.gen_html_file(tdm_ch)
    rocc_0_review_of_ctr.gen_html_file(tdm_ch)
    rocc_1_on_the_provenance_of_ctr.gen_html_file(tdm_ch)
    rocc_2_pre_vowel_accents_in_ctr.gen_html_file(tdm_ch)
    rocc_3_where_other_sources_stand.gen_html_file(tdm_ch)
    rocc_4_mid_word_ga3ya_with_shewa.gen_html_file(tdm_ch)
    gray_maqaf.gen_html_file(tdm_ch_wide)
    the_next_700_bibles.gen_html_file(tdm_ch)


def main():
    almost_main()


if __name__ == "__main__":
    main()
