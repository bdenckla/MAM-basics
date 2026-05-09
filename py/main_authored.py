"""
Generate miscellaneous authored HTML documents (notes, reviews, analyses)
that are written by the repo owner and rendered from Python source data.

Subcommands:
  gen-misc             (default) Write misc authored HTML docs to
                       MAM-with-doc/gh-pages/misc/.
  gen-mam-parsed-docs  Write reading_mam_parsed_plain.html and
                       reading_mam_parsed_plus.html to MAM-parsed/gh-pages/.
                       Run this after editing py/author/reading_mam_parsed_plain.py,
                       py/author/reading_mam_parsed_plus.py, or
                       py/author/reading_mam_parsed_plus_body.py.
"""

import argparse
import pathlib

from mb_misc import mb_html
from mb_misc import styles_authored
from mb_misc import styles_mam_parsed
from mb_cmn import provenance
from author import notes_on_aliyot
from author import tsinnorit_and_oleh_on_ivs
from author import tsinnorit_and_oleh_facts
from author import tsinnorit_in_psalm_32v5
from author import tsinnorit_and_the_xxd_in_bhs
from author import rocc_0_review_of_ctr
from author import rocc_1_on_the_provenance_of_ctr
from author import rocc_2_pre_vowel_accents_in_ctr
from author import rocc_3_where_other_sources_stand
from author import rocc_4_mid_word_ga3ya_with_shewa
from author import he_ws_intro_to_mam_gray_maqaf_1 as gray_maqaf
from author import he_ws_intro_to_mam_pasleg as pasleg
from author import the_next_700_bibles
from author import reading_mam_parsed_plain
from author import reading_mam_parsed_plus
from author import reading_mam_parsed_plus_aot
from author import reading_mam_parsed_plus_kq_special
from author import reading_mam_parsed_plus_haarah_2
from author import reading_mam_parsed_plus_kaful
from author import reading_mam_parsed_plus_good_ending


def _gen_index_html(top_dir_misc, index_entries):
    items = [mb_html.anchor_h(title, fname) for fname, title in index_entries]
    cbody = [
        mb_html.heading_level_1("Miscellaneous Documents"),
        mb_html.unordered_list(items),
    ]
    write_ctx = mb_html.WriteCtx(
        "Miscellaneous Documents",
        f"{top_dir_misc}/index.html",
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(cbody, write_ctx)


def almost_main():
    # XXX TODO: rm *.html (to avoid stale files when output names change)
    pages_dir = "../MAM-with-doc/gh-pages"
    top_dir_misc = f"{pages_dir}/misc"
    top_dir_old = f"{pages_dir}/tsinnorit_oleh"
    #
    css_href = "style.css"
    styles_authored.make_css_file_for_authored(f"{top_dir_misc}/{css_href}")
    #
    tdm_ch = top_dir_misc, css_href
    tdm_ch_aliyot = top_dir_misc, "aliyot-styles.css"
    #
    # notes_on_aliyot is linked from the top level, not from misc/index.html
    notes_on_aliyot.gen_html_file(tdm_ch_aliyot)  # return intentionally ignored
    index_entries = [
        tsinnorit_and_oleh_on_ivs.gen_html_file(tdm_ch, top_dir_old),
        tsinnorit_and_oleh_facts.gen_html_file(tdm_ch),
        tsinnorit_in_psalm_32v5.gen_html_file(tdm_ch),
        tsinnorit_and_the_xxd_in_bhs.gen_html_file(tdm_ch),
        rocc_0_review_of_ctr.gen_html_file(tdm_ch),
        rocc_1_on_the_provenance_of_ctr.gen_html_file(tdm_ch),
        rocc_2_pre_vowel_accents_in_ctr.gen_html_file(tdm_ch),
        rocc_3_where_other_sources_stand.gen_html_file(tdm_ch),
        rocc_4_mid_word_ga3ya_with_shewa.gen_html_file(tdm_ch),
        gray_maqaf.gen_html_file(tdm_ch, body_class="wide"),
        pasleg.gen_html_file(tdm_ch, body_class="wide"),
        the_next_700_bibles.gen_html_file(tdm_ch),
    ]
    _gen_index_html(top_dir_misc, index_entries)


def cmd_gen_misc(_args):
    almost_main()


def cmd_gen_mam_parsed_docs(_args):
    out_dir = pathlib.Path("../MAM-parsed/gh-pages")
    # Write CSS
    styles_mam_parsed.make_css_file_for_mam_parsed(str(out_dir / "style.css"))
    # Write HTML docs
    tdm_ch = str(out_dir), "style.css"
    reading_mam_parsed_plain.gen_html_file(tdm_ch)
    reading_mam_parsed_plus.gen_html_file(tdm_ch)
    reading_mam_parsed_plus_aot.gen_html_file(tdm_ch)
    reading_mam_parsed_plus_kq_special.gen_html_file(tdm_ch)
    reading_mam_parsed_plus_haarah_2.gen_html_file(tdm_ch)
    reading_mam_parsed_plus_kaful.gen_html_file(tdm_ch)
    reading_mam_parsed_plus_good_ending.gen_html_file(tdm_ch)
    print(f"Generated MAM-parsed docs in {out_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="subcommand")
    sub.add_parser("gen-misc", help="Generate miscellaneous authored HTML documents")
    sub.add_parser(
        "gen-mam-parsed-docs",
        help="Generate reading-MAM-parsed-plain/plus HTML docs in MAM-parsed/gh-pages/",
    )
    args = parser.parse_args()
    if args.subcommand == "gen-mam-parsed-docs":
        cmd_gen_mam_parsed_docs(args)
    else:
        # Default (no subcommand, or explicit gen-misc) runs gen-misc.
        cmd_gen_misc(args)


if __name__ == "__main__":
    main()
