"""The landing page's ordered topical index.

``SECTIONS`` is the sole source for ``build_body`` in ``author_site.site_index``.  The
index distinguishes published MAM editions from repository datasets, then groups related
studies, excerpts, technical resources, and reviews by subject.  The structure stays flat
except for the named four-part Masoretes series.  Unicode and Taamey D are linked headings
because each heading is itself the sole destination for that topic.

Every internal href is relative so the generated page works both in a local checkout and
at the site root.  ``py/tests/test_site_index_links.py`` walks all typed anchors, including
heading links and grouped entries, to verify tracked targets and deploy-root reachability.

The two translated excerpts from the Introduction to MAM copy the ``_TITLE`` constants of
their ``py/author_misc/`` renderers.  The same lint compares those copies mechanically, so
edit the source page title and this index entry together rather than retyping one side.

``gh-pages/wlc/index.html`` remains deliberately absent.  The index names the useful WLC
destinations directly, while the frozen redirect manifest preserves the old wlc-utils
route.  The Almost-errors page is likewise not a top-level entry because Goerwitz Run on
WLC links to it.
"""

from __future__ import annotations

from mb_cmn import str_defs as sd

from author_site.entries import Anchor, Entry, EntryGroup, Italic, Section

_RSQM = "\N{RIGHT SINGLE QUOTATION MARK}"
_EM_DASH = "\N{EM DASH}"
_ELLIPSIS = "\N{HORIZONTAL ELLIPSIS}"

_MWD = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/"
_MWD_MISC = f"{_MWD}misc/"
_PHONETIC = "https://bdenckla.github.io/phonetic-hbo/"
_TAAMEY_D = "https://bdenckla.github.io/hbofonts/Taamey_D.html"
_GDOC = "https://docs.google.com/document/d/e"
_REPO = "https://github.com/bdenckla/MAM-basics"
_REPO_MAIN = f"{_REPO}/blob/main"

UNICODE_PROPOSALS_FNAME = "unicode-proposals.html"
UNICODE_PROPOSALS_TITLE = "Unicode and ISO Proposals"

POST_STRESS_METEG_FNAME = "post-stress-meteg.html"
POST_STRESS_METEG_TITLE = "Meteg after the stress"
POST_STRESS_METEG_METHODS_FNAME = "post-stress-meteg-methods.html"
POST_STRESS_METEG_METHODS_TITLE = "Meteg after the stress: methods"
POST_STRESS_METEG_CASES_FNAME = "post-stress-meteg-cases.html"
POST_STRESS_METEG_CASES_TITLE = "Meteg after the stress: individual cases"
POST_STRESS_METEG_MISC_FNAME = "post-stress-meteg-misc.html"
POST_STRESS_METEG_MISC_TITLE = "Meteg after the stress: misc cases"
POST_STRESS_METEG_LACKS_MAS_FNAME = "post-stress-meteg-lacks-mas.html"
POST_STRESS_METEG_LACKS_MAS_TITLE = (
    "Meteg after the stress: syllables fit for it, but lacking it"
)
POST_STRESS_METEG_NOT_FIT_FNAME = "post-stress-meteg-not-fit.html"
POST_STRESS_METEG_NOT_FIT_TITLE = "Meteg after the stress: cases not fit for MAS"
POST_STRESS_METEG_POST_SILLUQ_FNAME = "post-stress-meteg-post-silluq.html"
POST_STRESS_METEG_POST_SILLUQ_TITLE = "Meteg after silluq"
POST_STRESS_METEG_2CHRONICLES_8_11_FNAME = "post-stress-meteg-2chr-8-11.html"
POST_STRESS_METEG_2CHRONICLES_8_11_TITLE = "Meteg in 2 Chr. 8:11"
POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME = "post-stress-meteg-next-conjunctive.html"
POST_STRESS_METEG_NEXT_CONJUNCTIVE_TITLE = (
    "Meteg after the stress: next words with a conjunctive accent"
)

# The stylesheet all eleven pages at the deploy root link, written by Ben and tracked as
# gh-pages/style.css -- a sibling of every page, so the href needs no prefix.  Its whole job is
# the light/dark switching every other page generated here already had through
# gh-pages/wlc/style.css, which the deploy-root pages cannot simply share: that file's @font-face
# names woff2/Taamey_D.woff2 relative to itself, and it carries a hundred rules for
# accgram tables that no link index has any use for.  Ben asked for the switching on
# 2026-08-31, having noticed the two deploy-root pages that existed then staying white on a
# dark display.
CSS_HREF = "style.css"

# The accgram stylesheet, linked BESIDE the one above by the nine post-stress-meteg pages that show
# pointed Hebrew and accent-name romanizations. It supplies the
# lang="hbo" font at the size that makes accents legible, the italic for span.romanized, and
# the numeric-cell alignment, none of which a page of links has any use for and none of which
# is therefore in style.css.  Its @font-face URL is relative to the stylesheet, so the font
# resolves from the deploy root as it does from gh-pages/wlc/.
ACCGRAM_CSS_HREF = "wlc/style.css"

# Every href below that stays inside this site is written RELATIVE, because this page is
# published at the site root and a relative link works in a local checkout too.
# py/tests/test_site_index_links.py resolves each one against gh-pages/.
#
# AND IT NAMES index.html EXPLICITLY where document-index wrote a bare directory URL.
# GitHub Pages serves both, but py/check_html_syntax_and_sanity.py does not resolve a
# trailing slash and reports "wlc/420422/" as a broken link.  Spelling the file out costs
# nothing, matches the manifest entry below, and keeps that lint clean without teaching a
# shared linter a new rule for this one page's sake.


def _entry(text, href, **kwargs) -> Entry:
    return Entry(Anchor(text, href), **kwargs)


def _mwd_misc(title: str, fname: str) -> Entry:
    """A page under MAM-with-doc/misc/, named by the title that page carries."""
    return _entry(title, _MWD_MISC + fname)


INTRO = (
    "This page contains links to editions and datasets of MAM, together with related "
    "studies, excerpts, reviews, and technical resources."
)

_EDITIONS = Section(
    heading="MAM editions",
    entries=(
        _entry(
            "MAM on Hebrew Wikisource",
            "https://he.wikisource.org/wiki/מקרא_על_פי_המסורה",
        ),
        _entry("Phonetic MAM", _PHONETIC),
        _entry(
            "MAM on Sefaria",
            "https://www.sefaria.org/Genesis.1?lang=bi&vhe=hebrew%7C"
            "Miqra_according_to_the_Masorah",
        ),
        _entry("MAM with doc", _MWD),
        _entry(
            "MAM for SWORD (CrossWire MapM)",
            "https://ftp.crosswire.org/sword/modules/ModInfo.jsp?modName=MapM",
        ),
    ),
)

_DATASETS = Section(
    heading="MAM datasets and technical documentation",
    entries=(
        _entry("MAM-parsed", f"{_REPO_MAIN}/MAM-parsed/README.md"),
        _entry("MAM-simple", f"{_REPO_MAIN}/MAM-simple/README.md"),
        _entry("MAM-for-Sefaria", f"{_REPO_MAIN}/MAM-for-Sefaria/README.md"),
        _entry("MAM-OSIS", f"{_REPO_MAIN}/MAM-OSIS/README.md"),
    ),
)

_ABOUT_MAM = Section(
    heading="About MAM",
    entries=(
        _entry(
            "Miqra as Oral Torah, Written Torah and Digital Torah",
            "https://hakirah.org/vol36Kadish.pdf",
            note=(" (in Ḥakirah volume 36; co-author Seth (Avi) Kadish)",),
        ),
        _entry(
            f"MAM and UXLC {_EM_DASH} two Hebrew Bible datasets",
            "https://1drv.ms/p/s!AgRN8M0NNCoaiP0oo3o1BMXeqb7PIQ",
            note=(" (presented at the 2023 SBL Annual Meeting in San Antonio)",),
        ),
        _entry("MAM FOI (Features of Interest) Lists", f"{_MWD}foi/index.html"),
        _entry(
            ("Notes on Torah ", Italic("aliyot")),
            f"{_MWD_MISC}notes_on_aliyot.html",
        ),
        _entry(
            f"Daniel Holman{_RSQM}s change proposals for MAM",
            "holman/table_data_findings.html",
        ),
    ),
)

_INTRODUCTION_EXCERPTS = Section(
    heading="Excerpts from the Introduction to MAM",
    entries=(
        _mwd_misc("Gray maqaf", "he_ws_intro_to_mam_gray_maqaf_1.html"),
        _mwd_misc("Paseq and legarmeh", "he_ws_intro_to_mam_pasleg.html"),
        _entry(f"Aleppo Codex {_EM_DASH} Missing Sections", "aleppo/index.html"),
    ),
)

_URWOTM = EntryGroup(
    label="Undoing and redoing the work of the Masoretes",
    entries=(
        _entry(
            "The tale of the qadma",
            f"{_MWD_MISC}urwotm_1_tale_of_the_qadma.html",
            label="Part 1: ",
        ),
        _entry(
            "Saying the quiet part out loud",
            f"{_MWD_MISC}urwotm_2_saying_the_quiet_part_out_loud.html",
            label="Part 2: ",
        ),
        _entry(
            "Extra verses",
            f"{_MWD_MISC}urwotm_3_extra_verses.html",
            label="Part 3: ",
        ),
        _entry(
            "Atnaḥ hafukh",
            f"{_MWD_MISC}urwotm_4_atnax_hafukh.html",
            label="Part 4: ",
        ),
    ),
)

_POINTING_AND_CANTILLATION = Section(
    heading="Pointing and cantillation",
    entries=(
        _entry(POST_STRESS_METEG_TITLE, POST_STRESS_METEG_FNAME),
        _entry(
            (
                "Excerpts from ",
                Italic("Introduction to the Tiberian Masorah"),
                " by Israel Yeivin",
            ),
            f"{_PHONETIC}yeivin_itm.html",
        ),
        _URWOTM,
    ),
)

_REVIEWS = Section(
    heading="Reviews",
    entries=(
        _entry(
            f"Review of ArtScroll{_RSQM}s Transliterated Linear Siddur (Ashkenaz)",
            f"{_MWD_MISC}review_of_artscroll_transliterated_linear_siddur.html",
        ),
        _entry(
            f"Review of Hebrew World{_RSQM}s Phonetic Bible",
            f"{_MWD_MISC}review_of_hebrew_worlds_phonetic_bible.html",
        ),
        _entry(
            f"Review of Mitchell{_RSQM}s {sd.LDQM}The Songs of Ascents{sd.RDQM}",
            f"{_GDOC}/2PACX-1vRahgc2mWcB5AVwJp7XYcTpmohdh8X3eeAadN0Ute7QbfLMjP9g82wICDi7"
            "CWaEfyLKtkn-GzE5j6wx/pub",
        ),
        _entry(
            f"Review of {sd.LDQM}Textual Variants {_ELLIPSIS} B19a {_ELLIPSIS}{sd.RDQM}",
            f"{_GDOC}/2PACX-1vSD53ZHZQOOu9oppVN3k19zdaOPhvR97tCFdJT1q9WJXze1gzAMfPeAbQao"
            "-k2EYgzOK2MtyLweOn5h/pub",
        ),
        _entry(
            f"Review of Chabad{_RSQM}s web Tanakh",
            f"{_MWD_MISC}rocc_0_review_of_ctr.html",
        ),
        _entry(
            "Review of A Hebrew Reader for the Pentateuch",
            f"{_GDOC}/2PACX-1vQ6QyxCbui3JRF2II6QYnF4ZMbjCDXGsQQ3qCheRAKCGvvdp1_TYeXTIies"
            "DNmM-KWxvmW3dlM2ipV8/pub",
        ),
        _entry(
            "Review of the Job fascicle of BHQ",
            "book-of-job/jobn/job2_main_article.html",
        ),
    ),
)

_WLC_AND_UXLC = Section(
    heading="WLC and UXLC",
    entries=(
        _entry(
            "All changes in Westminster Leningrad Codex (WLC) version 4.22",
            "wlc/420422/index.html",
        ),
        _entry(
            "One particular change in Ezra 4:12 in WLC 4.22",
            "wlc/420422/full-record/420422-54.html",
        ),
        _entry("All WLC a-notes", "wlc/wlc-a-notes/index.html"),
        _entry("Goerwitz Run on WLC", "wlc/accgram/goerwitz.html"),
        _entry("UXLC-utils web pages", "uxlc/index.html"),
        _entry(
            f"Daniel Holman{_RSQM}s change proposals for UXLC",
            "holman/uxlc_corrections.html",
        ),
    ),
)

_UNICODE = Section(
    heading=Anchor(UNICODE_PROPOSALS_TITLE, UNICODE_PROPOSALS_FNAME),
    entries=(),
)

_TAAMEY = Section(
    heading=Anchor("Taamey D", _TAAMEY_D),
    entries=(),
)

# Ben's 2026-09-18 topical order.
SECTIONS = (
    _EDITIONS,
    _DATASETS,
    _ABOUT_MAM,
    _INTRODUCTION_EXCERPTS,
    _POINTING_AND_CANTILLATION,
    _WLC_AND_UXLC,
    _REVIEWS,
    _UNICODE,
    _TAAMEY,
)

# The two translated Introduction-to-MAM entries and the source modules whose titles they
# copy.  Keeping both ordered tuples lets the lint compare each entry with its own source.
INTRO_MAM_MWD_ENTRIES = tuple(
    entry
    for entry in _INTRODUCTION_EXCERPTS.entries
    if entry.anchor.href.startswith(_MWD_MISC)
)
INTRO_MAM_SOURCE_MODULES = tuple(
    entry.anchor.href[len(_MWD_MISC) :].removesuffix(".html")
    for entry in INTRO_MAM_MWD_ENTRIES
)
