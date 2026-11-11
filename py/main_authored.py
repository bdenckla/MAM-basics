"""
Generate miscellaneous authored HTML documents (notes, reviews, analyses)
that are written by the repo owner and rendered from Python source data.

Subcommands:
    gen-misc
                (default) Write misc authored HTML docs to
                gh-pages/MAM-with-doc/misc/.
    gen-site
                Write the published pages at the deploy root:
                gh-pages/index.html, gh-pages/unicode-proposals.html, and every
                gh-pages/post-stress-meteg*.html page, including one post-silluq
                case page per entry of
                site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES.
                --trust-surveys lets the post-stress pages that read the survey
                load it from the tracked out/accgram/post-stress-meteg.json
                instead of recomputing it from the tracked Phonetic-MAM
                release; only main_0_mega.py passes it.
    gen-mam-parsed-docs
                Write index.html to gh-pages/MAM-parsed and the plus docs to
                gh-pages/MAM-parsed/plus/html. Runs the claim verification
                first, on the docs as built in memory, and writes nothing if
                a claim fails, unless --skip-verify-mp says not to verify.
    gen-mam-for-sefaria-doc
                Write gh-pages/MAM-for-Sefaria/index.html, "The encoding of MAM
                for Sefaria", its unicode-names/index.html and ajf/index.html,
                from the tracked files of MAM-for-Sefaria/
                (py/author_misc/mam4sef_*index.py).
    gen-israel-bible-review
                Write gh-pages/israel-bible-review/index.html, Ben's review of
                the Israel Bible, and its style.css, from in/israel-bible-review/
                (py/author_misc/israel_bible_review_index.py).
    verify-mp
                Run MAM-parsed claim verification without rewriting
                MAM-parsed authored HTML/CSS outputs.
    gen-mp-claims-index
                Write doc/mp-claims.md from explicit claims and available
                verifier functions without rewriting MAM-parsed authored
                HTML/CSS outputs.  Run this after editing
                py/author_misc/mpplus.py or py/author_misc/mpplus_body.py.

Examples:
    .venv/Scripts/python.exe py/main_authored.py
    .venv/Scripts/python.exe py/main_authored.py gen-mam-parsed-docs
    .venv/Scripts/python.exe py/main_authored.py verify-mp

WHERE A NEW PAGE GOES

Not into gh-pages/MAM-with-doc/misc/ merely because the reviews and notes that gen-misc writes
are there.  Ben, 2026-11-11, asking for the review of the Israel Bible to move to a folder of
its own: "Note somewhere that though you were following existing precedent by putting the
israel bible review in MAM-with-doc/misc or whatever, that location reflects a very old
situation where MAM-with-doc was its own repo with its own gh-pages and I'm not sure MAM-basics
even had a gh-pages (and might have even pre-dated the whole existence of MAM-basics, i.e.
those reviews might date back to the "trope" repo days!)"  So the review now has
gh-pages/israel-bible-review/, a peer of gh-pages/book-of-job/ and gh-pages/clc/, which
gen-israel-bible-review writes, as gen-mam-for-sefaria-doc writes gh-pages/MAM-for-Sefaria/.

What this repository's history shows, read on 2026-11-11:

* MAM-basics' first commit, d86e5779 of 2026-03-09, is "Initial commit — history-free
  snapshot of trope repo code".  bdenckla/trope is the repository MAM-basics replaced; the
  entry for it in in/repo_maintenance_policy.json says "Discontinued 2026-03-19 in favour of
  MAM-basics, per the repo's own README".
* In that snapshot this program, then py/main_gen_misc_authored_english_documents.py, wrote
  its pages, the five of the review of Chabad's web Tanakh (rocc_0 to rocc_4) among them, into
  ../MAM-with-doc/docs/misc, in the sibling MAM-with-doc repository.  From b47f0d22
  (2026-04-10), "Update output paths to use GitHub Pages directory", it wrote them into
  ../MAM-with-doc/gh-pages/misc.
* MAM-basics had no gh-pages/ until f99996f3 (2026-08-12), when wlc-utils' pages came in.
  MAM-with-doc's pages followed on 2026-09-06 (5a28bc0e; in/mam_with_doc_redirect_pages.json
  freezes their old paths), and this program has written gh-pages/MAM-with-doc/misc/ since
  3c8c9750, that day.
* Later pages followed the precedent into misc/: the four parts of "Undoing and redoing the
  work of the Masoretes" (2026-07-27), the reviews of Hebrew World's Phonetic Bible and of
  ArtScroll's Transliterated Linear Siddur (both 2026-08-31), the review of A Hebrew Reader
  for the Pentateuch (2026-11-08) and the review of the Israel Bible (2026-11-10).

What these records cannot settle is when the misc pages began.  The first commit carries no
history, so how long before 2026-03-09 the review of Chabad's web Tanakh and its folder
existed is recorded only in trope's history and MAM-with-doc's; no clone here holds either,
and this note was written without reading them.
"""

import argparse
import sys

from mb_misc import styles_authored
from mb_cmn import paths
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
from author_misc import review_of_hebrew_reader_for_the_pentateuch as hr_review
from author_misc import israel_bible_review_index as ib_review
from author_misc import he_ws_intro_to_mam_gray_maqaf_1 as gray_maqaf
from author_misc import he_ws_intro_to_mam_pasleg as pasleg
from author_misc import he_ws_intro_to_mam_gaya_text as gaya_text
from author_misc import mam_parsed_docs_build
from author_misc import mam4sef_ajf_index
from author_misc import mam4sef_index
from author_misc import mam4sef_unicode_names_index
from author_site import post_stress_meteg
from author_site import site_data
from author_site import site_index
from author_site import unicode_proposals
from verify_mp import claims_doc
from verify_mp import driver as verify_driver
from verify_mp.corpus import Context, load_plus_corpus


def almost_main():
    # XXX TODO: rm *.html (to avoid stale files when output names change)
    pages_dir = str(paths.repo_root() / "gh-pages" / "MAM-with-doc")
    top_dir_misc = f"{pages_dir}/misc"
    top_dir_old = f"{pages_dir}/tsinnorit_oleh"
    #
    css_href = "style.css"
    styles_authored.make_css_file_for_authored(f"{top_dir_misc}/{css_href}")
    #
    tdm_ch = top_dir_misc, ("../../document.css", css_href)
    tdm_ch_aliyot = top_dir_misc, ("../../document.css", "aliyot-styles.css")
    #
    # The folder has no index page.  misc/index.html, which listed most of these pages,
    # was deleted on 2026-11-10 at Ben's word: "This misc/index.html is not important to
    # maintain".  The return values are ignored.  A new page does not join these merely by
    # their precedent: the module docstring, "WHERE A NEW PAGE GOES", says why.
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
    urwotm_1.gen_html_file(tdm_ch)
    urwotm_2.gen_html_file(tdm_ch)
    urwotm_3.gen_html_file(tdm_ch)
    urwotm_4.gen_html_file(tdm_ch)
    hw_review.gen_html_file(tdm_ch)
    as_review.gen_html_file(tdm_ch)
    hr_review.gen_html_file(tdm_ch)
    gray_maqaf.gen_html_file(tdm_ch, body_class="wide")
    pasleg.gen_html_file(tdm_ch, body_class="wide")
    gaya_text.gen_html_file(tdm_ch, body_class="wide")


def cmd_gen_misc(_args):
    almost_main()


# The deploy-root pages that can be rendered from a tracked JSON instead of recomputing their
# survey, by name.  A SET rather than the scalar py/main_accgram.py's --trust-survey routes to
# one report: this one starts with a member and is expected to grow, and a second member added
# to a scalar would have had to become this anyway.
#
# WHY ANY PAGE NEEDS IT: py/main_0_mega.py runs post-stress-meteg's survey as a step of its
# own just before gen-site, and the survey writes the tracked out/accgram/post-stress-meteg.json,
# so the mega renders all nine pages from that JSON rather than walking the corpus a second
# time.  The survey reads the tracked Phonetic-MAM release, so the mega runs it in a cloud
# session too; until 2026-10-01 it read MAM-private's Phonetic MAM, and a cloud session
# skipped it and rendered the pages from the tracked JSON unchanged.  Recomputing from the
# corpus is what a standalone run does.  The JSON's absence FAILS rather than falling back, so
# a mega that quietly published a page from nothing is not a state this can reach.
_SURVEY_READING_PAGES = frozenset(
    {
        site_data.POST_STRESS_METEG_FNAME,
        site_data.POST_STRESS_METEG_METHODS_FNAME,
        site_data.POST_STRESS_METEG_CASES_FNAME,
        site_data.POST_STRESS_METEG_MISC_FNAME,
        site_data.POST_STRESS_METEG_LACKS_MAS_FNAME,
        site_data.POST_STRESS_METEG_NOT_FIT_FNAME,
        site_data.POST_STRESS_METEG_POST_SILLUQ_FNAME,
        site_data.POST_STRESS_METEG_2CHRONICLES_8_11_FNAME,
        site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME,
    }
)

assert _SURVEY_READING_PAGES <= {
    site_data.POST_STRESS_METEG_FNAME,
    site_data.POST_STRESS_METEG_METHODS_FNAME,
    site_data.POST_STRESS_METEG_CASES_FNAME,
    site_data.POST_STRESS_METEG_MISC_FNAME,
    site_data.POST_STRESS_METEG_LACKS_MAS_FNAME,
    site_data.POST_STRESS_METEG_NOT_FIT_FNAME,
    site_data.POST_STRESS_METEG_POST_SILLUQ_FNAME,
    site_data.POST_STRESS_METEG_2CHRONICLES_8_11_FNAME,
    site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME,
    site_data.UNICODE_PROPOSALS_FNAME,
}, "a name here that no deploy-root page has would silently render nothing from its JSON"


def gen_site(*, trust_surveys: bool = False):
    """Write the pages published by this repository at the deploy root.

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


def gen_mam_for_sefaria_doc():
    """Write the three MAM-for-Sefaria documentation pages."""
    for page in (mam4sef_index, mam4sef_unicode_names_index, mam4sef_ajf_index):
        print(f"Generated {page.gen_html_file()}")


def cmd_gen_mam_for_sefaria_doc(_args):
    gen_mam_for_sefaria_doc()


def gen_israel_bible_review():
    """Write the review of the Israel Bible and its stylesheet into its own folder,
    gh-pages/israel-bible-review/."""
    print(f"Generated {ib_review.gen_html_file()}")


def cmd_gen_israel_bible_review(_args):
    gen_israel_bible_review()


def _run_verify_mp(*, claims) -> None:
    """Run MAM-parsed claim verification against the loaded plus corpus."""
    verify_driver.run(Context(corpus=load_plus_corpus()), claims=claims)


def cmd_gen_mam_parsed_docs(_args):
    out_dir = str(paths.gh_pages_dir() / "MAM-parsed")
    skip_verify = bool(getattr(_args, "skip_verify_mp", False)) if _args else False
    if not skip_verify:
        # Verify the claims of the documents as built in memory, so that a failed claim
        # leaves the written documents and claims index as they were.
        print("Running MAM-parsed verification...")
        _run_verify_mp(claims=mam_parsed_docs_build.collect_explicit_claims())

    claims = mam_parsed_docs_build.build_docs_with_explicit_claims(out_dir)
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
        help="Generate this repository's published pages at the gh-pages deploy root.",
    ).add_argument(
        "--trust-surveys",
        action="store_true",
        help=(
            "Let a page that has one read its tracked survey JSON instead of recomputing it."
            " Passed by main_0_mega.py, which runs the survey as a step of its own."
        ),
    )
    sub.add_parser(
        "gen-mam-parsed-docs",
        help=(
            "Generate authored MAM-parsed docs (index at gh-pages root and "
            "plus/html for the surviving product pages)."
        ),
    ).add_argument(
        "--skip-verify-mp",
        action="store_true",
        help="Skip the claim verification that runs before the MAM-parsed docs are written.",
    )
    sub.add_parser(
        "gen-mam-for-sefaria-doc",
        help=(
            "Generate gh-pages/MAM-for-Sefaria/index.html, unicode-names/index.html and"
            " ajf/index.html from the tracked files of MAM-for-Sefaria/."
        ),
    )
    sub.add_parser(
        "gen-israel-bible-review",
        help=(
            "Generate gh-pages/israel-bible-review/index.html, the review of the Israel"
            " Bible, and its style.css, from in/israel-bible-review/."
        ),
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
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    if args.subcommand == "gen-site":
        cmd_gen_site(args)
    elif args.subcommand == "gen-mam-parsed-docs":
        cmd_gen_mam_parsed_docs(args)
    elif args.subcommand == "gen-mam-for-sefaria-doc":
        cmd_gen_mam_for_sefaria_doc(args)
    elif args.subcommand == "gen-israel-bible-review":
        cmd_gen_israel_bible_review(args)
    elif args.subcommand == "gen-mp-claims-index":
        cmd_gen_mp_claims_index(args)
    elif args.subcommand == "verify-mp":
        cmd_verify_mp(args)
    else:
        # Default (no subcommand, or explicit gen-misc) runs gen-misc.
        cmd_gen_misc(args)


if __name__ == "__main__":
    main()
