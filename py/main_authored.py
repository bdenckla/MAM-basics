"""
Generate miscellaneous authored HTML documents (notes, reviews, analyses)
that are written by the repo owner and rendered from Python source data.

Subcommands:
  gen-misc             (default) Write misc authored HTML docs to
                       MAM-with-doc/gh-pages/misc/.
  gen-mam-parsed-docs  Write mpplain.html and
                       mpplus.html to MAM-parsed/gh-pages/.
  verify-mp            Run MAM-parsed claim verification without
                       rewriting MAM-parsed authored HTML/CSS outputs.
  gen-mp-claims-index  Write doc/mp-claims.md from explicit claims and
                       available verifier functions without rewriting
                       MAM-parsed authored HTML/CSS outputs.
                       Run this after editing py/author/mpplain.py,
                       py/author/mpplain_body.py,
                       py/author/mpplus.py, or
                       py/author/mpplus_body.py.
"""

import argparse

from mb_misc import mb_html
from mb_misc import styles_authored
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
from author import mam_parsed_docs_build
from verify_mp import claims_doc
from verify_mp import driver as verify_driver
from verify_mp import survey_artifact
from verify_mp.corpus import Context, load_plus_corpus, load_plain_corpus


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


def _run_verify_mp(*, claims) -> None:
    """Run MAM-parsed claim verification against corpus + survey artifacts."""
    corpus = load_plus_corpus()
    corpus_plain = load_plain_corpus()
    survey = survey_artifact.load()
    survey_plain = survey_artifact.load_plain()
    ctx = Context(
        corpus=corpus,
        corpus_plain=corpus_plain,
        survey=survey,
        survey_plain=survey_plain,
    )
    verify_driver.run(ctx, claims=claims)


def cmd_gen_mam_parsed_docs(_args):
    out_dir = "../MAM-parsed/gh-pages"
    claims = mam_parsed_docs_build.build_docs_with_explicit_claims(out_dir)

    skip_verify = bool(getattr(_args, "skip_verify_mp", False)) if _args else False
    if not skip_verify:
        print("Running MAM-parsed verification...")
        _run_verify_mp(claims=claims)

    claims_path = claims_doc.write_output(claims)
    print(f"Generated MAM-parsed docs in {out_dir}")
    print(f"Generated claims index in {claims_path}")


def cmd_gen_mp_claims_index(_args):
    claims = mam_parsed_docs_build.collect_explicit_claims()
    out_path = claims_doc.write_output(claims)
    print(f"Generated claims index in {out_path}")


def cmd_verify_mp(_args):
    claims = mam_parsed_docs_build.collect_explicit_claims()
    _run_verify_mp(claims=claims)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="subcommand")
    sub.add_parser("gen-misc", help="Generate miscellaneous authored HTML documents")
    sub.add_parser(
        "gen-mam-parsed-docs",
        help="Generate reading-MAM-parsed-plain/plus HTML docs in MAM-parsed/gh-pages/",
    ).add_argument(
        "--skip-verify-mp",
        action="store_true",
        help="Skip running claim verification after generating MAM-parsed docs.",
    )
    sub.add_parser(
        "gen-mp-claims-index",
        help=(
            "Generate doc/mp-claims.md from explicit claims and verifier functions "
            "without regenerating MAM-parsed docs/CSS."
        ),
    )
    sub.add_parser(
        "verify-mp",
        help="Run MAM-parsed claim verification without regenerating docs/CSS.",
    )
    args = parser.parse_args()
    if args.subcommand == "gen-mam-parsed-docs":
        cmd_gen_mam_parsed_docs(args)
    elif args.subcommand == "gen-mp-claims-index":
        cmd_gen_mp_claims_index(args)
    elif args.subcommand == "verify-mp":
        cmd_verify_mp(args)
    else:
        # Default (no subcommand, or explicit gen-misc) runs gen-misc.
        cmd_gen_misc(args)


if __name__ == "__main__":
    main()
