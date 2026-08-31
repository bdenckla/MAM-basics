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
  already name joined ``_WLC``, and the whole file is authored now, with no derived half.
* **Flat.**  Ben, 2026-08-31, asked for "a 'misc' section with links to those 10
  documents" rather than a link to ``MAM-with-doc/misc/index.html``, so that reaching any
  of his documents takes one click from here and not two.  ``_MISC`` is that section.

THE FOUR NEW WLC ENTRIES CARRY ``gh-pages/wlc/index.html``'s OWN LINK TEXT, verbatim, down
to its em dashes -- that hand-written page is where Ben had already named each of them for
a reader, so distributing them is a move rather than a rewrite.  Two of the four therefore
read differently from the page's ``<title>``; that is deliberate, and it is why no lint
compares them, unlike the ten Misc titles below.

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

THE TEN MISC TITLES ARE THE PAGES' OWN.  They are copies of ``_TITLE`` in the matching
``py/author_misc/`` module, and ``py/tests/test_site_index_links.py`` fails if a copy drifts
from its original.  Do not edit one here without editing the module -- and do not retype
one: two carry Hebrew and several carry a curly apostrophe.
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

# The stylesheet both pages at the deploy root link, hand-written and tracked as
# gh-pages/style.css -- a sibling of both, so the href needs no prefix.  Its whole job is
# the light/dark switching every other page generated here already had through
# gh-pages/wlc/style.css, which these two could not simply share: that file's @font-face
# names woff2/Taamey_D.woff2 relative to itself, and it carries a hundred rules for
# accgram tables that no link index has any use for.  Ben asked for the switching on
# 2026-08-31, having noticed these two pages staying white on a dark display.
CSS_HREF = "style.css"

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
            "https://bdenckla.github.io/book-of-job/jobn/job2_main_article.html",
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
        _entry(
            "Are the printed Decalogue cantillations grammatical?",
            "wlc/accgram/printed-decalogue.html",
        ),
        _entry(
            "What printed editions have at ובנך",
            "wlc/accgram/printed-decalogue-uvinkha.html",
        ),
        _entry(
            f"Psalms 17:14 {_EM_DASH} the double tsinnor",
            "wlc/accgram/ps17v14-double-tsinnor.html",
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

# The ten documents under MAM-with-doc/misc/ that document-index did not carry.  Its own
# seven from that directory are above, under Reviews and Undoing and redoing.
_MISC = Section(
    heading="Misc",
    entries=(
        _mwd_misc(
            "Tsinnorit & Oleh on Initial Vocal Shewa", "tsinnorit_and_oleh_on_ivs.html"
        ),
        _mwd_misc("About Tsinnorit & Oleh", "tsinnorit_and_oleh_facts.html"),
        _mwd_misc("Tsinnorit in Psalm 32:5 ועוני", "tsinnorit_in_psalm_32v5.html"),
        _mwd_misc(
            "Tsinnorit and the Ḥolam Ḥaser dot in BHS",
            "tsinnorit_and_the_xxd_in_bhs.html",
        ),
        _mwd_misc(
            "On the Provenance of Chabad’s CTR", "rocc_1_on_the_provenance_of_ctr.html"
        ),
        _mwd_misc(
            "Pre-vowel Accents in Chabad’s CTR", "rocc_2_pre_vowel_accents_in_ctr.html"
        ),
        _mwd_misc(
            "CTR Psalm 32: Where Other Sources Stand",
            "rocc_3_where_other_sources_stand.html",
        ),
        _mwd_misc("Mid-word געיה with Shewa", "rocc_4_mid_word_ga3ya_with_shewa.html"),
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

# The ten Misc entries copy these modules' _TITLE constants; the lint checks each copy.
MISC_SOURCE_MODULES = tuple(
    entry.anchor.href[len(_MWD_MISC) :].removesuffix(".html") for entry in _MISC.entries
)
