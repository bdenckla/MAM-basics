"""
Generate miscellaneous authored HTML documents (notes, reviews, analyses)
that are written by the repo owner and rendered from Python source data.

Subcommands:
    gen-misc
                (default) Write misc authored HTML docs to
                MAM-with-doc/gh-pages/misc/.
    gen-site
                Write this repo's own published pages at the deploy root:
                gh-pages/index.html, gh-pages/unicode-proposals.html and
                gh-pages/post-stress-meteg.html.  --trust-surveys lets the
                last of those read the tracked
                out/accgram/post-stress-meteg.json instead of recomputing a
                survey that needs the MAM-private clone; only main_0_mega.py
                passes it.
    gen-mam-parsed-docs
                Write index.html to MAM-parsed/gh-pages, plain docs to
                MAM-parsed/gh-pages/plain/html, and plus docs to
                MAM-parsed/gh-pages/plus/html.  Runs the claim verification
                afterwards unless --skip-verify-mp says not to.
    verify-mp
                Run MAM-parsed claim verification without rewriting
                MAM-parsed authored HTML/CSS outputs.
    gen-mp-claims-index
                Write doc/mp-claims.md from explicit claims and available
                verifier functions without rewriting MAM-parsed authored
                HTML/CSS outputs.  Run this after editing
                py/author_misc/mpplain.py, py/author_misc/mpplain_body.py,
                py/author_misc/mpplus.py, or py/author_misc/mpplus_body.py.

Examples:
    .venv/Scripts/python.exe py/main_authored.py
    .venv/Scripts/python.exe py/main_authored.py gen-mam-parsed-docs
    .venv/Scripts/python.exe py/main_authored.py verify-mp
"""

import argparse

from mb_misc import mb_html
from mb_misc import styles_authored
from mb_cmn import paths
from mb_cmn import provenance
from author_misc import notes_on_aliyot
from author_misc import tsinnorit_and_oleh_on_ivs
from author_misc import tsinnorit_and_oleh_facts
from author_misc import tsinnorit_in_psalm_32v5
from author_misc import tsinnorit_and_the_xxd_in_bhs
from author_misc import rocc_0_review_of_ctr
from author_misc import rocc_1_on_the_provenance_of_ctr
from author_misc import rocc_2_pre_vowel_accents_in_ctr
from author_misc import rocc_3_where_other_sources_stand
from author_misc import rocc_4_mid_word_ga3ya_with_shewa
from author_misc import urwotm_1_tale_of_the_qadma as urwotm_1
from author_misc import urwotm_2_saying_the_quiet_part_out_loud as urwotm_2
from author_misc import urwotm_3_extra_verses as urwotm_3
from author_misc import urwotm_4_atnax_hafukh as urwotm_4
from author_misc import review_of_hebrew_worlds_phonetic_bible as hw_review
from author_misc import review_of_artscroll_transliterated_linear_siddur as as_review
from author_misc import he_ws_intro_to_mam_gray_maqaf_1 as gray_maqaf
from author_misc import he_ws_intro_to_mam_pasleg as pasleg
from author_misc import mam_parsed_docs_build
from author_site import post_stress_meteg
from author_site import site_data
from author_site import site_index
from author_site import unicode_proposals
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
    pages_dir = str(paths.sibling_repo("MAM-with-doc") / "gh-pages")
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
        urwotm_1.gen_html_file(tdm_ch),
        urwotm_2.gen_html_file(tdm_ch),
        urwotm_3.gen_html_file(tdm_ch),
        urwotm_4.gen_html_file(tdm_ch),
        hw_review.gen_html_file(tdm_ch),
        as_review.gen_html_file(tdm_ch),
        gray_maqaf.gen_html_file(tdm_ch, body_class="wide"),
        pasleg.gen_html_file(tdm_ch, body_class="wide"),
    ]
    _gen_index_html(top_dir_misc, index_entries)


def cmd_gen_misc(_args):
    almost_main()


# The deploy-root pages that can be rendered from a tracked JSON instead of recomputing their
# survey, by name.  A SET rather than the scalar py/main_accgram.py's --trust-survey routes to
# one report: this one starts with a member and is expected to grow, and a second member added
# to a scalar would have had to become this anyway.
#
# WHY ANY PAGE NEEDS IT: post-stress-meteg's survey reads Phonetic MAM, which lives in
# MAM-private, and py/main_0_mega.py must not come to require a private clone.  The mega
# therefore renders all seven pages from out/accgram/post-stress-meteg.json, which the survey
# subcommand writes and which is tracked; recomputing from the corpus is what a standalone run
# does.  The JSON's absence FAILS rather than falling back, so a mega that quietly published a
# page from nothing is not a state this can reach.
_SURVEY_READING_PAGES = frozenset(
    {
        site_data.POST_STRESS_METEG_FNAME,
        site_data.POST_STRESS_METEG_METHODS_FNAME,
        site_data.POST_STRESS_METEG_CASES_FNAME,
        site_data.POST_STRESS_METEG_TYPE_2_FNAME,
        site_data.POST_STRESS_METEG_MISC_FNAME,
        site_data.POST_STRESS_METEG_TYPE_2_LACKS_MAS_FNAME,
        site_data.POST_STRESS_METEG_TYPE_1_LACKS_MAS_FNAME,
    }
)

assert _SURVEY_READING_PAGES <= {
    site_data.POST_STRESS_METEG_FNAME,
    site_data.POST_STRESS_METEG_METHODS_FNAME,
    site_data.POST_STRESS_METEG_CASES_FNAME,
    site_data.POST_STRESS_METEG_TYPE_2_FNAME,
    site_data.POST_STRESS_METEG_MISC_FNAME,
    site_data.POST_STRESS_METEG_TYPE_2_LACKS_MAS_FNAME,
    site_data.POST_STRESS_METEG_TYPE_1_LACKS_MAS_FNAME,
    site_data.UNICODE_PROPOSALS_FNAME,
}, "a name here that no deploy-root page has would silently render nothing from its JSON"


def gen_site(*, trust_surveys: bool = False):
    """Write this repo's own published pages at the deploy root.

    ``trust_surveys`` is passed by ``main_0_mega.py``; see ``_SURVEY_READING_PAGES``.  The
    index runs last, so it sees whatever the pages before it have written.
    """
    trusted = (
        trust_surveys and site_data.POST_STRESS_METEG_FNAME in _SURVEY_READING_PAGES
    )
    for out_path in (
        unicode_proposals.gen_html_file(),
        *post_stress_meteg.gen_html_files(trust_survey=trusted),
        site_index.gen_html_file(),
    ):
        print(f"Generated {out_path}")


def cmd_gen_site(args):
    gen_site(trust_surveys=bool(getattr(args, "trust_surveys", False)))


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
    out_dir = str(paths.sibling_repo("MAM-parsed") / "gh-pages")
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


def build_parser():
    """The fully-configured parser, so a test can read the subcommands off it."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="subcommand")
    sub.add_parser("gen-misc", help="Generate miscellaneous authored HTML documents")
    sub.add_parser(
        "gen-site",
        help="Generate this repo's own published pages at the gh-pages deploy root.",
    ).add_argument(
        "--trust-surveys",
        action="store_true",
        help=(
            "Let a page that has one read its tracked survey JSON instead of recomputing it."
            " Passed by main_0_mega.py, which cannot reach MAM-private."
        ),
    )
    sub.add_parser(
        "gen-mam-parsed-docs",
        help=(
            "Generate authored MAM-parsed docs (index at gh-pages root, "
            "plain/html and plus/html for family pages)."
        ),
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
    return parser


def main():
    args = build_parser().parse_args()
    if args.subcommand == "gen-site":
        cmd_gen_site(args)
    elif args.subcommand == "gen-mam-parsed-docs":
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
