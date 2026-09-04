"""The landing page's authored content: Ben's index of the documents he has written.

WHERE THIS CAME FROM.  ``document-index/README.md``, a repo of its own until 2026-08-31,
transcribed entry for entry.  ``doc/PLAN-unify-the-document-index.md`` is the record of the
move and of the three decisions Ben took when it was proposed.  Two of those decisions are
visible in the shape of this file:

* **One page.**  The publication manifest that used to be the whole of the landing page
  became this page's last section, headed "Pages published from this repository", and was
  DERIVED rather than listed, by an ``author_site/published_subtrees.py`` this file's
  docstring pointed at.  Ben deleted that section on 2026-08-31, having disliked it, and
  asked that the pages it reached through ``gh-pages/wlc/index.html`` be distributed to
  the top-level sections instead -- so the four of that page's seven the index did not
  already name were added, and the whole file is authored now, with no derived half.  All
  four went to ``_WLC`` first; the same day Ben moved three of them to ``_MISC``, not
  being WLC-specific, and that section's own comment has the counts behind it.
* **Flat, then trimmed.**  Ben, 2026-08-31, asked for "a 'misc' section with links to
  those 10 documents" rather than a link to ``MAM-with-doc/misc/index.html``, so that
  reaching any of his documents took one click from here and not two.  Later the same day
  he asked for the section to be trimmed "down to documents not reachable from another,
  document already listed", which cut eleven of its thirteen entries.  ``_MISC``'s own
  comment names each of the eleven and the page that reaches it.

THE FOUR PAGES DISTRIBUTED ON 2026-08-31 CARRIED ``gh-pages/wlc/index.html``'s OWN LINK
TEXT, verbatim, down to its em dashes -- that hand-written page is where Ben had already
named each of them for a reader, so distributing them was a move rather than a rewrite.
Only ``almost-errors``, in ``_WLC``, still is on this page: the trim later that day cut the
other three, ``printed-decalogue``, ``printed-decalogue-uvinkha`` and
``ps17v14-double-tsinnor``, all of which ``goerwitz.html`` or ``almost-errors.html``
reaches.  So no entry here reads differently from the page's ``<title>`` any more, and
every ``_MISC`` entry copies a ``py/author_misc/`` module's ``_TITLE``.

THE HEADINGS ARE NOT INVENTED.  document-index's top-level list mixed four category
bullets with two lone documents.  Rendering categories as ``<h2>`` sections is flatter than
nesting lists, and the two lone documents get a heading that is the NAME OF THE THING THEY
POINT AT -- "Unicode and ISO Proposals" is that page's own title, "Taamey D" the font's.
So every heading here is either document-index's own category name or a name it used.

WHAT WAS DELIBERATELY CHANGED, and it is exactly two hrefs.  document-index sent both of
its gist-hosted reviews to gists that were cut down to forwarding stubs on 2026-08-31, when
``15a09ae`` and ``9086da4`` moved their text into ``py/author_misc/``.  Following either
link reached a page whose only content was a pointer.  Both now name the generated page
directly, and no gist link survives on this page.  Everything else is document-index's,
including its ordering, its parentheticals and its two lead-in sentences.

THE MISC TITLES ARE THE PAGES' OWN.  They are copies of ``_TITLE`` in the matching
``py/author_misc/`` module, and ``py/tests/test_site_index_links.py`` fails if a copy drifts
from its original.  Do not edit one here without editing the module -- and do not retype
one: the two that survived the trim carry no Hebrew, but the modules' titles elsewhere in
``py/author_misc/`` do, along with curly apostrophes.
"""

from __future__ import annotations

from mb_cmn import str_defs as sd

from author_site.entries import Anchor, Entry, Italic, Section

_RSQM = "\N{RIGHT SINGLE QUOTATION MARK}"
_EM_DASH = "\N{EM DASH}"
_ELLIPSIS = "\N{HORIZONTAL ELLIPSIS}"

_MWD = "https://bdenckla.github.io/MAM-with-doc/"
_MWD_MISC = f"{_MWD}misc/"
_PHONETIC = "https://bdenckla.github.io/phonetic-hbo/"
_TAAMEY_D = "https://bdenckla.github.io/Taamey_D/"
_GDOC = "https://docs.google.com/document/d/e"

UNICODE_PROPOSALS_FNAME = "unicode-proposals.html"
UNICODE_PROPOSALS_TITLE = "Unicode and ISO Proposals"

POST_STRESS_METEG_FNAME = "post-stress-meteg.html"
POST_STRESS_METEG_TITLE = "Meteg after the primary stress in MAM"

# The stylesheet both pages at the deploy root link, hand-written and tracked as
# gh-pages/style.css -- a sibling of both, so the href needs no prefix.  Its whole job is
# the light/dark switching every other page generated here already had through
# gh-pages/wlc/style.css, which these two could not simply share: that file's @font-face
# names woff2/Taamey_D.woff2 relative to itself, and it carries a hundred rules for
# accgram tables that no link index has any use for.  Ben asked for the switching on
# 2026-08-31, having noticed these two pages staying white on a dark display.
CSS_HREF = "style.css"

# The accgram stylesheet, linked BESIDE the one above by the one deploy-root page that shows
# pointed Hebrew and accent-name romanizations: post-stress-meteg.html.  It supplies the
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


LEAD_IN = "Links to public documents of which I am the author (or an author):"

LEAD_IN_NOT_MINE = (
    "Documents of which I am neither the author nor an author, but are"
    f" {sd.LDQM}mine{sd.RDQM} in some sense:"
)

_UNICODE = Section(
    heading=UNICODE_PROPOSALS_TITLE,
    entries=(_entry("Unicode proposals I have submitted", UNICODE_PROPOSALS_FNAME),),
)

_MAM = Section(
    heading="MAM",
    entries=(
        _entry(
            "Miqra as Oral Torah, Written Torah and Digital Torah",
            "https://hakirah.org/vol36Kadish.pdf",
            subs=("in Ḥakirah volume 36", "co-author Seth (Avi) Kadish"),
        ),
        _entry(
            f"MAM and UXLC {_EM_DASH} two Hebrew Bible datasets",
            "https://t.co/YmM3Wj9RVr",
            note=(" (presented at the 2023 SBL Annual Meeting in San Antonio)",),
        ),
        _entry("MAM FOI (Features of Interest) Lists", f"{_MWD}foi/index.html"),
        _entry(POST_STRESS_METEG_TITLE, POST_STRESS_METEG_FNAME),
        _entry(
            ("Notes on Torah ", Italic("aliyot")),
            f"{_MWD_MISC}notes_on_aliyot.html",
        ),
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

_WLC = Section(
    heading="WLC",
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
        _entry(
            f"Almost errors {_EM_DASH} editorial charities the checker applies",
            "wlc/accgram/almost-errors.html",
        ),
    ),
)

_URWOTM = Section(
    heading="Undoing and redoing the work of the Masoretes",
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

# The two documents that NOTHING ELSE ON THIS PAGE REACHES.  Ben, 2026-08-31: trim this
# section "down to documents not reachable from another, document already listed".
#
# WHAT THAT REVERSES, since it was decided the same day.  This section opened as the ten
# documents under MAM-with-doc/misc/ that document-index did not carry, so that reaching
# any document of Ben's took one click from here rather than two; three accgram pages
# published from this repo joined them when the manifest section was retired.  Eleven of
# those thirteen are reachable by following links from a document this page already names,
# and are cut on that ground:
#
# * rocc_0_review_of_ctr.html, this page's "Review of Chabad's web Tanakh", links the four
#   rocc_1..rocc_4 pages and tsinnorit_and_oleh_on_ivs.html directly.
# * tsinnorit_and_oleh_on_ivs.html then links tsinnorit_and_oleh_facts.html and
#   tsinnorit_in_psalm_32v5.html, which links tsinnorit_and_the_xxd_in_bhs.html.
# * wlc/accgram/goerwitz.html and wlc/accgram/almost-errors.html, both named under WLC,
#   link printed-decalogue.html and ps17v14-double-tsinnor.html; printed-decalogue.html
#   links printed-decalogue-uvinkha.html.
#
# Gray maqaf and Paseq and legarmeh survive because no page anywhere in this site or in
# MAM-with-doc links either one: cut from here, they would be reachable by no number of
# clicks, which is the thing Ben objects to.  MAM-with-doc/gh-pages/misc/index.html names
# them but is itself linked from nothing, so it rescues neither.
#
# Re-establish the whole finding by crawling both gh-pages trees from the documents this
# page names; the counts above were measured 2026-08-31 against MAM-basics 027acc3.
_MISC = Section(
    heading="Misc",
    entries=(
        _mwd_misc("Gray maqaf", "he_ws_intro_to_mam_gray_maqaf_1.html"),
        _mwd_misc("Paseq and legarmeh", "he_ws_intro_to_mam_pasleg.html"),
    ),
)

_TAAMEY = Section(
    heading="Taamey D",
    entries=(
        _entry(
            f"Documentation for my Biblical Hebrew font, {sd.LDQM}Taamey D{sd.RDQM}",
            _TAAMEY_D,
            note=(
                " (",
                Anchor(
                    "latest release of that font",
                    "https://github.com/bdenckla/Taamey_D/releases/latest",
                ),
                ")",
            ),
        ),
    ),
)

_EDITIONS = Section(
    heading="Editions of MAM",
    entries=(
        _entry("Phonetic MAM", _PHONETIC),
        _entry("MAM with doc", _MWD),
    ),
)

_EXCERPTS = Section(
    heading="Excerpts",
    entries=(
        _entry(
            (
                "Excerpts from ",
                Italic("Introduction to the Tiberian Masorah"),
                " by Israel Yeivin",
            ),
            f"{_PHONETIC}yeivin_itm.html",
        ),
    ),
)

# document-index's order, which is Ben's.
BY_ME = (_UNICODE, _MAM, _REVIEWS, _WLC, _URWOTM, _MISC, _TAAMEY)
NOT_BY_ME = (_EDITIONS, _EXCERPTS)

# The MAM-with-doc half of the Misc section, and the modules whose _TITLE each entry copies.
# Paired rather than derived twice, so the lint cannot zip an entry against another entry's
# module.  The whole section is MAM-with-doc since the 2026-08-31 trim, so the href filter
# selects everything today; it stays because an entry naming a page published from this repo
# copies no module's _TITLE, and Misc has twice held such entries.
MISC_MWD_ENTRIES = tuple(
    entry for entry in _MISC.entries if entry.anchor.href.startswith(_MWD_MISC)
)
MISC_SOURCE_MODULES = tuple(
    entry.anchor.href[len(_MWD_MISC) :].removesuffix(".html")
    for entry in MISC_MWD_ENTRIES
)
