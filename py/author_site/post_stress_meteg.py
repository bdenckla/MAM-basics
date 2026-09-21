r"""MAM's meteg marks after the stress: the main page and eight supporting pages.

The pages for ``accgram.post_stress_meteg``'s survey take every census figure from that survey
rather than from a separate constant. The maintained meteg-after-silluq page instead joins its
two validated JSON ledgers to forms lifted from MAM-simple or UXLC. ``pin_claims`` checks the
survey's internal consistency and re-derives the categorical and relational claims in the prose,
which is the shape
``maqaf_nonfinal_accents_page.pin_claims`` established.

A LOOSE PAGE AT THE DEPLOY ROOT, beside ``index.html`` and ``unicode-proposals.html``, which
is Ben's decision of 2026-09-03 (``doc/PLAN-post-stress-meteg-page-and-holman-m23.md``).  Not
under ``gh-pages/wlc/``: that prefix exists so wlc-utils' frozen redirect stubs can rewrite
onto ``MAM-basics/wlc/<path>``, a page published here after the 2026-08-17 move earns no stub,
and this page's corpus is MAM rather than WLC.

IT LINKS TWO STYLESHEETS, and the second is the accgram one.  ``gh-pages/style.css`` is the
deploy-root stylesheet, whose whole job is the light/dark switching; ``gh-pages/wlc/style.css``
supplies the ``lang="hbo"`` font at the size that makes accents legible, the italic for a
romanized accent name, and the numeric-cell alignment.  A stylesheet's ``@font-face`` URL
resolves against the stylesheet, so ``woff2/Taamey_D.woff2`` reaches the font from here too.

WHY THIS PAGE SHOWS POINTED HEBREW where the accgram pages show letters and accents alone.
``accents_and_letters`` drops U+05BD along with the vowels, and U+05BD is this page's whole
subject; and what the page is about is which SYLLABLE a mark falls in, which a reader cannot
see without the vowels that make the syllables.  All three of the page's structural types
are named for a vowel or a syllable shape, so the vowel is the point of the comparison here in
the sense the house rule allows for. Reader-facing forms begin with MAM's data at generation
time except where the meteg-after-silluq ledger explicitly requests the UXLC transcription.
The Fit-for-MAS lack page uses each record's ``mam_form`` and ``next_mam_form``; analysis-only
annotations are omitted before HTML is written. None is typed here.

THESE PAGES SAY PLAIN "word", AND THAT IS A DECISION RATHER THAN AN OVERSIGHT.  The
``hebrew-prose`` skill's first rule is "Never a loose 'word'"; Ben exempted this document and
its sub-documents on 2026-09-08, and the skill allows for it -- plain "word" survives "wherever
the context already settles which sense is meant". The main page defines both "word" and "atom"
in its second expository paragraph; the opening sentence already uses "word". **Do not qualify "word" as
"chanted word" in anything these pages render**, prose, heading, tooltip and alt text alike;
``py/tests/test_post_stress_meteg_plain_word.py`` fails if you do, and its docstring records why
a lint rather than a comment or a helper function is what defends this.  The survey's own
vocabulary is untouched by that rule: ``census_chanted_word_summary``,
``chanted_word_difference`` and ``_case_chanted_word_cell`` keep their names.

THE PAGE QUOTES NEITHER YEIVIN NOR BREUER.  The plan permits bounded excerpts and does not
require them; the sections are cited by number and their content paraphrased, so no private
source text reaches a public page.  ``_EXCERPTS`` is empty and ``_excerpt_accounting`` asserts
that it is, which is the plan's requirement for a page with no excerpts.

CoS CH. 14 §8 IS WHERE BREUER TREATS THE POETIC SYSTEM'S GA'AYA, cited here since 2026-09-07.
Read that day off ``C14-S001.md`` in the CoS export at
``MAM-private/masorah-books/books/cos/md-export-of-docx/``, anchor ``<!-- §8 -->``, and off
the scans.  Chapters 9 through 15 discuss a ga'aya after the stressed syllable there and
nowhere else: Chs. 10, 12 and 15 name no ga'aya at all, and the Ch. 9, 11 and 13 hits are the
"syllable fit for a light ga'aya" position yardstick for placing a secondary servant, plus
Ch. 8 §4's ga'aya standing in place of an omitted accent, which is the opposite of MAS.
§8's opening sentence is the premise the rest rests on -- the Eme"t books' ga'aya "only
differs from the ga'aya of the 21 books in the following types."  The rendered table reports
only item (b), which is type 2 outright, and leaves the other Ch. 14 cells blank.  The printed
pages are read off the scan filenames -- C547, C548
and ``C549-P2-C14-Pas-Hyph-Ga.jpg`` for §8, ``C354-P1-C8-Ga-aya.jpg`` for Ch. 8 §46 -- and the
four claims are pinned in masorah-books' ``py/cos/check_cos_claims.py``.  ITM states nothing
poetic-specific about a ga'aya after the stress, so the page claims nothing about ITM in
either direction.

MAM AGREES WITH ITEM (b), AND THAT MEASUREMENT IS RECORDED HERE RATHER THAN RENDERED.  Ben's
decision of 2026-09-07 is references only: the page gets the Ch. 14 citations, their printed
pages and a paraphrase, and no page renders a MAM count for this.  Measured 2026-09-07 from
the tracked ``out/accgram/post-stress-meteg.json`` at ``11fb9c24``: of the 17 type-2 MAS whose
next chanted word begins with a guttural, seven are prose verses -- nu35:16, nu35:17, nu35:18,
nu35:21, dt4:33, 1s22:17 and ec1:5, exactly the exceptions Ch. 8 §9 lists as its Examples II
-- and ten are poetic verses: ps10:11, ps18:45, ps19:3, ps94:9, ps105:28, pr28:2, pr29:2,
pr29:6, pr29:18 and jb22:13.  The one type-2 MAS whose next chanted word begins with ר is
poetic, ps19:14, which is one of item (b)'s four cantillated-word examples; all four of those
examples are type-2 MAS records here.  Re-derive current counts by grouping the tracked JSON's
``TYPE_GUTTURAL`` records by
``(record["system"], psm.type_2_next_filter_group(record["next_mam_form"]))``.  The grouping
must partition the type-2 records, but its populations are not source-code constants.
"""

from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from accgram import final_stress
from accgram import mam_simple_verse
from accgram import post_stress_meteg as psm
from accgram import printed_decalogue_strands as pds
from accgram.almost_errors_html_shared import ref_abbrev, wrap_hebrew_runs
from accgram import rtms_report
from author_site import site_data
from author_site import post_stress_meteg_annotations
from mb_author import author
from mb_cmn import paths
from mb_cmn import provenance
from mb_cmn import hebrew_accents as ha
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn
from py_uxlc import my_uxlc
from py_wlc_json_and_unicode import wlc_uword
from uxlc_misc import my_uxlc as uxlc_source
from wlc_cmn.wlc_book_codes import wlc_bb_codes, wlc_bb_to_bk39id

_FNAME = site_data.POST_STRESS_METEG_FNAME
_TITLE = site_data.POST_STRESS_METEG_TITLE
_METHODS_FNAME = site_data.POST_STRESS_METEG_METHODS_FNAME
_METHODS_TITLE = site_data.POST_STRESS_METEG_METHODS_TITLE
_CASES_FNAME = site_data.POST_STRESS_METEG_CASES_FNAME
_CASES_TITLE = site_data.POST_STRESS_METEG_CASES_TITLE
_MISC_FNAME = site_data.POST_STRESS_METEG_MISC_FNAME
_MISC_TITLE = site_data.POST_STRESS_METEG_MISC_TITLE
_LACKS_MAS_FNAME = site_data.POST_STRESS_METEG_LACKS_MAS_FNAME
_LACKS_MAS_TITLE = site_data.POST_STRESS_METEG_LACKS_MAS_TITLE
_NOT_FIT_FNAME = site_data.POST_STRESS_METEG_NOT_FIT_FNAME
_NOT_FIT_TITLE = site_data.POST_STRESS_METEG_NOT_FIT_TITLE
_POST_SILLUQ_FNAME = site_data.POST_STRESS_METEG_POST_SILLUQ_FNAME
_POST_SILLUQ_TITLE = site_data.POST_STRESS_METEG_POST_SILLUQ_TITLE
_CHRONICLES_8_11_FNAME = site_data.POST_STRESS_METEG_2CHRONICLES_8_11_FNAME
_CHRONICLES_8_11_TITLE = site_data.POST_STRESS_METEG_2CHRONICLES_8_11_TITLE
_NEXT_CONJUNCTIVE_FNAME = site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_FNAME
_NEXT_CONJUNCTIVE_TITLE = site_data.POST_STRESS_METEG_NEXT_CONJUNCTIVE_TITLE
_PHONETIC_MAM_URL = "https://bdenckla.github.io/phonetic-hbo/"
_POST_SILLUQ_FOOTNOTE_ID = "footnote-1"
_NONFINAL_MAS_FOOTNOTE_ID = "footnote-2"
_JEREMIAH_FOOTNOTE_ID = "footnote-3"
_NEXT_CONJUNCTIVE_FOOTNOTE_ID = "footnote-4"
_SOURCES_FOR_TYPES_FOOTNOTE_ID = "footnote-5"
_TYPE_2_TYPE_3_FOOTNOTE_ID = "footnote-6"
_VOCAL_SHEWA_FOOTNOTE_ID = "footnote-7"
_PASHTA_STRESS_HELPER_FOOTNOTE_ID = "footnote-8"
_FIT_TYPE_2_NO_IVS_FOOTNOTE_ID = "footnote-9"
_FIT_FOR_MAS_SECTION_ID = "fit-for-mas"


def _author_romanization(key: str) -> object:
    """One standard author-wide dollar substitution, already wrapped as romanized text."""
    (rendered,) = author.dollar_sub(f"${key}")
    return rendered


# Each visible romanization is a module-level HTML node, so the shared ``romanized`` class
# italicizes it.  Existing ``ROM_*`` spellings stay single-sourced; the author-wide dollar
# substitutions supply the additional standard spellings this page needs.
_ROM_METEG = rmn(pds.ROM_METEG)
_ROM_METEG_MERKHA = rmn(f"{pds.ROM_METEG}/{pds.ROM_MERKHA}")
_ROM_METEG_CAP = rmn(pds.ROM_METEG.capitalize())
_ROM_METSIL = rmn("metsil")
_ROM_SILLUQ = rmn(pds.ROM_SILLUQ)
_ROM_PASEQ = rmn(pds.ROM_PASEQ)
_ROM_PATAH = rmn(pds.ROM_PATAX)
_ROM_MAQAF = rmn(pds.ROM_MAQAF)
_ROM_TSERE = _author_romanization("tsere")
_ROM_HOLAM = _author_romanization("xolam")
_ROM_GAYA = _author_romanization("gaya_with_half_ring_for_ayin")
_ROM_OLEH = _author_romanization("oleh")
_ROM_ALEF = _author_romanization("alef")
_ROM_BET = _author_romanization("bet")
_ROM_HE = _author_romanization("hehe")
_ROM_MAPPIQ = rmn("mappiq")
_ROM_VAYOMER = rmn("vayomer")
_ROM_SHEWA = rmn("shewa")
_ROM_PASHTA = rmn(pds.ROM_PASHTA)


def _visible_title(title: str, *, lowercase: bool = False) -> tuple:
    """A page title whose visible meteg and silluq take the standard italics."""
    assert title.startswith("Meteg "), title
    rest = title.removeprefix("Meteg")
    head = _ROM_METEG if lowercase else _ROM_METEG_CAP
    before, silluq, after = rest.partition(pds.ROM_SILLUQ)
    if silluq:
        return (head, before, _ROM_SILLUQ, after)
    return (head, rest)


# Every Hebrew cell says so, whatever else it says.  The whole-column rule: blank cells
# included, the English heading left alone, no class and no stylesheet rule.
_HEBREW_CELL = {"dir": "rtl"}
_NUMERIC_CELL = {"class": "numeric"}
_POST_SILLUQ_BCV_CELL = {"class": "post-silluq-bcv"}

# No excerpt from either book appears on this page.  Kept as a structure rather than as a bare
# absence so the accounting below has something to count, and so an excerpt added later is
# added in one place with its source beside it.
_EXCERPTS: tuple[tuple[str, str], ...] = ()

_MAX_WORDS_PER_EXCERPT = 150
_MAX_WORDS_IN_ALL_EXCERPTS = 300

_PROSE = psm.SYSTEM_PROSE
_POETIC = psm.SYSTEM_POETIC
_MBS_O_CENSUS_GLOSS = (
    "count of words with one or more meteg marks before the stress and none after it"
)
_MAS_CENSUS_GLOSS = (
    "count of words with one or more meteg marks after the stress and any number"
    " (including zero) before it"
)
# This page names each book's author in the hover title, where the accgram pages that share
# ``almost_errors_html_shared``'s ITM_TITLE and COS_TITLE do not.  Ben's decision, 2026-09-08,
# after the divergence was put to him with the option of ending it either way: "that slight
# divergence (author's names shown in some cases, not shown in other cases) is acceptable to me."
# So do not unify the four pages on either spelling; the difference is chosen, not overlooked.
_ITM_GLOSS = "Yeivin's Introduction to the Tiberian Masorah"
_COS_GLOSS = "Breuer's The Cantillation of Scripture"

# The one verse the page names outside its tables.  The survey records its chanted words as MAM
# has them today, under ``currency.focus_verses``, so the form shown here is lifted like every
# other form on the page.
_POST_SILLUQ_VERSE = "1s17:5"
_MAM_POST_SILLUQ_VERSE = "1k7:37"
# Every visible spelling of these two references comes from ``ref_abbrev``, the
# short-but-not-super-short prose form built on ``mb_misc/osis_book_abbrevs.py``'s
# OSIS list -- "Gen. 2:7", "1 Sam. 17:5", "1 Kgs. 7:37".  Ben's rule of 2026-09-08:
# no reference is typed out, here or in a figure caption or an alt text.
_POST_SILLUQ_REF = ref_abbrev(_POST_SILLUQ_VERSE)
_MAM_POST_SILLUQ_REF = ref_abbrev(_MAM_POST_SILLUQ_VERSE)
_POST_SILLUQ_LC_CROP_URL = "img/LC-159A-col-3-line-8-1S-17v5.png"
_POST_SILLUQ_LC_CROP_SOURCE_URL = "https://github.com/bdenckla/phonetic-hbo/issues/78"
_POST_SILLUQ_ALEPPO_CROP_URL = "img/Aleppo-Codex-1S-17v5-no-post-silluq-meteg.png"
_MAM_POST_SILLUQ_ALEPPO_CROP_URL = "img/Aleppo-Codex-1K-7v37.png"
_MAM_POST_SILLUQ_LENINGRAD_CROP_URL = "img/Leningrad-Codex-1K-7v37.png"
_POST_SILLUQ_CASES_JSON = "meteg_after_silluq_cases.json"
_POST_SILLUQ_KOREN_JSON = "meteg_after_silluq_koren_readings.json"
_POST_SILLUQ_CASE_STATUSES = frozenset({"last-metsil-contrast", "open-candidate"})
_POST_SILLUQ_FORM_SOURCES = frozenset({"mam", "uxlc"})
_POST_SILLUQ_SOURCE_STATES = frozenset(
    {
        "later-meteg",
        "no-later-mark",
        "both-strokes",
        "first-position-only",
        "tracked-observation",
        "not-recorded",
    }
)
_POST_SILLUQ_SOURCES = ("mam", "aleppo", "leningrad", "koren")
_POST_SILLUQ_IMAGE_REFS = {
    "lc-1s17-5": "1 Samuel 17:5",
    "aleppo-1s17-5": "1 Samuel 17:5",
    "aleppo-1k7-37": "1 Kings 7:37",
    "leningrad-1k7-37": "1 Kings 7:37",
}
_POST_SILLUQ_IMAGE_IDS = frozenset(_POST_SILLUQ_IMAGE_REFS)
_KOREN_STATUSES = frozenset({"complete", "incomplete", "deferred", "skipped-family"})
_KOREN_POSITIONS = frozenset({"first", "last", "both"})
_KOREN_SHEVA_STATES = frozenset({"vocal", "silent"})
_FULL_REF = re.compile(r"(?P<book>.+) (?P<chapter>[0-9]+):(?P<verse>[0-9]+)")
_CHRONICLES_8_11_VERSE = "2c8:11"
_CHRONICLES_8_11_REF = ref_abbrev(_CHRONICLES_8_11_VERSE)
# site_data spells this page title by hand, being a plain data module with no accgram import.
# This assertion keeps its reference at ref_abbrev's form.
assert _CHRONICLES_8_11_REF in _CHRONICLES_8_11_TITLE, (
    _CHRONICLES_8_11_TITLE,
    _CHRONICLES_8_11_REF,
)
_CHRONICLES_8_11_ALEPPO_CROP_URL = "img/Aleppo-Codex-2Chr-8v11.png"
_CHRONICLES_8_11_LENINGRAD_CROP_URL = "img/Leningrad-Codex-2Chr-8v11.png"
_CHRONICLES_8_11_L1 = "אֲשֶׁר־בָּ֥אָֽה"
_CHRONICLES_8_11_L2 = "אֲשֶׁר־בָּֽאָ֥ה"
_CHRONICLES_8_11_LENINGRAD_NEXT_WORD = "אֲלֵיהֶ֖ם"
_CHRONICLES_8_11_LENINGRAD_GLOSSES = {
    "L-1": "merkha-meteg interpretation of Leningrad",
    "L-2": "meteg-merkha interpretation of Leningrad",
}

_ITM_ADAPTATION_URL_BY_SECTION = {
    325: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns325",
    332: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns332",
    338: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns338",
    354: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns354",
}
_ITM_SECTION_REFERENCE = re.compile(r"§(?P<section>[0-9]+)")

# A section range takes an en dash, matching the ranges already rendered on these
# pages.  Spelled by name so it stays legible in source.
_EN_DASH = "\N{EN DASH}"

# Yeivin and Breuer on each of the three types, and how each book grades it.  The pairing is
# the M23 evidence note's, doc/holman-meteg-m23-isaiah-23-12.md; both books are cited for
# every type, so no row rests on one source.  The Ch. 14 pairing below was added 2026-09-07
# and is CoS's alone: ITM states nothing poetic-specific about a gaʿya after the stress, so
# the ITM column stays as it was and the page claims nothing about ITM in either direction.
_TYPE_SOURCES = {
    psm.TYPE_OPEN: ("§332", f"§3(j), §§46{_EN_DASH}47"),
    psm.TYPE_GUTTURAL: ("§354", f"§3(b), §§9{_EN_DASH}10"),
    psm.TYPE_CLOSED_TSERE: ("§338", f"§3(a), §§5{_EN_DASH}8"),
}

# Each number is the printed page on which the cited Ch. 8 section begins.  How to read one
# off the scans, recorded 2026-09-07 because nothing recorded it when 14023ae4 added these
# numbers on 2026-09-05: the 719 images at ~/OneDrive/Documents/ScansOfBooks/The Cantillation
# of Scripture - English/ carry the printed page number in the filename, so
# C354-P1-C8-Ga-aya.jpg is p. 354, which is where §46's heading stands.  A roman-numbered
# page is a B name, B16.jpg being p. xvi; py/cos/fix_diacritics.py's SCAN_REPAIRS in
# masorah-books already relies on the same convention.
_COS_PAGE_STARTS_BY_TYPE = {
    psm.TYPE_OPEN: "300; 354; 355",
    psm.TYPE_GUTTURAL: "299; 308; 309",
    psm.TYPE_CLOSED_TSERE: "299; 301; 302; 306; 307",
}
_COS_CH_8_PAGE_GLOSS = (
    "printed page in Wengrov's English translation of CoS on which the cited Ch. 8 section"
    " begins"
)

# Ch. 14 §8's item (b) concerns type 2.  The source table reports that item and leaves the
# other Ch. 14 cells blank.  Read off C14-S001.md's <!-- §8 --> anchor and off the scans,
# 2026-09-07.
_COS_CH_14_BY_TYPE = {
    psm.TYPE_OPEN: "",
    psm.TYPE_GUTTURAL: "(b)",
    psm.TYPE_CLOSED_TSERE: "",
}
# §8 runs from the Ga'aya heading on p. 547 to the closing "On rare occasions" sentence on
# p. 549; p. 550 is blank, C551 and C552 are the Part III title leaves, and Ch. 15 opens on
# p. 553.  Item (b) is on p. 547.
_COS_CH_14_PAGES_BY_TYPE = {
    psm.TYPE_OPEN: "",
    psm.TYPE_GUTTURAL: "547",
    psm.TYPE_CLOSED_TSERE: "",
}

_TYPE_CODES = {
    psm.TYPE_OPEN: ("1", "the MAS syllable is open and final"),
    psm.TYPE_GUTTURAL: ("2", "the MAS word is closed by a guttural"),
    psm.TYPE_CLOSED_TSERE: (
        "3",
        "the MAS syllable is closed, final, and tsere-voweled",
    ),
}
_TYPE_1_SUBTYPE_CODES = {
    psm.TYPE_1_SUBTYPE_A: "1A",
    psm.TYPE_1_SUBTYPE_B: "1B",
    psm.TYPE_1_SUBTYPE_C: "1C",
    None: "1D",
}
_TYPE_2_SUBTYPE_SPECS = (
    ("lamed", "2A", "2A: The next word begins with ל (lamed)."),
    ("guttural", "2B", "2B: The next word begins with a guttural."),
    (
        "not-lamed-or-guttural",
        "2C",
        "2C: The next word begins with neither ל nor a guttural.",
    ),
)
_TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP = {
    group: code for group, code, _description in _TYPE_2_SUBTYPE_SPECS
}
# Each subtype tooltip restates its visible bullet, as the type tooltips do.  The type-2
# descriptions are taken from the spec tuple the subtype table itself renders, so those two
# cannot drift apart; the type-1 bullets carry a romanized span, which a title attribute
# cannot hold, so their plain-text spellings are written out here.
_TYPE_1_SUBTYPE_DESCRIPTIONS = {
    "1A": "1A: The next word has initial stress and an initial vocal shewa.",
    "1B": "1B: The next word has a pashta stress helper on its first letter.",
    "1C": "1C: Like 1B, but with some accent other than pashta.",
    "1D": "1D: The next word does not have initial stress.",
}
_SUBTYPE_DESCRIPTIONS = {
    **_TYPE_1_SUBTYPE_DESCRIPTIONS,
    **{code: description for _group, code, description in _TYPE_2_SUBTYPE_SPECS},
}
_CASE_FILTER_OPTIONS = (
    ("all", "All types"),
    ("1", "Type 1 (all subtypes)"),
    ("1A", "Subtype 1A"),
    ("1B", "Subtype 1B"),
    ("1C", "Subtype 1C"),
    ("1D", "Subtype 1D"),
    ("2", "Type 2 (all subtypes)"),
    ("2A", "Subtype 2A"),
    ("2B", "Subtype 2B"),
    ("2C", "Subtype 2C"),
    ("3", "Type 3"),
    ("other", "misc"),
)
_LACKS_MAS_FILTER_OPTIONS = tuple(
    (fit_type, f"Subtype {fit_type}")
    for fit_type in (
        psm.FIT_TYPE_1_A,
        psm.FIT_TYPE_1_B,
        psm.FIT_TYPE_2_AF,
        psm.FIT_TYPE_2_BF,
    )
)
_NOT_FIT_FILTER_OPTIONS = (
    ("all", "All (sub)types"),
    *_CASE_FILTER_OPTIONS[1:],
)
_CASE_TABLE_ID = "post-stress-meteg-cases"
_CASE_TYPE_FILTER_ID = "post-stress-meteg-type-filter"
_CASE_SELECTED_COUNT_ID = "post-stress-meteg-selected-count"
_CASE_TABLE_CLASS = "post-stress-meteg-cases-table"
_CASE_STRIPED_ROW_CLASS = "post-stress-meteg-cases-striped-row"
_NEXT_WORD_CLASS = "post-stress-meteg-next-word"
_LACKS_MAS_TABLE_ID = "post-stress-meteg-lacks-mas-cases"
_LACKS_MAS_SUBTYPE_FILTER_ID = "post-stress-meteg-lacks-mas-subtype-filter"
_LACKS_MAS_SELECTED_COUNT_ID = "post-stress-meteg-lacks-mas-selected-count"
_NOT_FIT_FAILURE_CLASS = "post-stress-meteg-not-fit-failure"
_NOT_FIT_TABLE_ID = "post-stress-meteg-not-fit-cases"
_NOT_FIT_TYPE_FILTER_ID = "post-stress-meteg-not-fit-type-filter"
_NOT_FIT_SELECTED_COUNT_ID = "post-stress-meteg-not-fit-selected-count"
_HEBREW_SPACING_CHECKBOX_ID = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_BODY_CLASS = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_STORAGE_KEY = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_INDIVIDUAL_EXPANDED_CLASS = (
    "post-stress-meteg-individually-expanded-hebrew"
)
_HEBREW_SPACING_INDIVIDUAL_NORMAL_CLASS = "post-stress-meteg-individually-normal-hebrew"
_MISC_TABLE_ID = "post-stress-meteg-misc-cases"
_FIT_FOR_MAS_TYPE_CRITERION = (
    "The next word conforms to (sub)type 1A, 1B, 2Af, 2Bf, or 3"
)
_FIT_FOR_MAS_CRITERIA = (
    "Its word has penultimate stress from a conjunctive accent.",
    "The next word has initial stress from a disjunctive accent.",
    f"{_FIT_FOR_MAS_TYPE_CRITERION}.",
)
_RED_X = "\N{CROSS MARK}"
_HEBREW_SPACING_OPTION = f"""<p class="post-stress-meteg-spacing-control"><label><input type="checkbox" id="{_HEBREW_SPACING_CHECKBOX_ID}" checked>
__SPACING_TEXT__</label> __TOGGLE_TEXT__</p>
<script>
(() => {{
  const checkbox = document.getElementById("{_HEBREW_SPACING_CHECKBOX_ID}");
  const bodyClass = "{_HEBREW_SPACING_BODY_CLASS}";
  const storageKey = "{_HEBREW_SPACING_STORAGE_KEY}";
  const individualExpandedClass = "{_HEBREW_SPACING_INDIVIDUAL_EXPANDED_CLASS}";
  const individualNormalClass = "{_HEBREW_SPACING_INDIVIDUAL_NORMAL_CLASS}";
  const hebrewSelector = '[lang="hbo"]';
  let saved = null;
  try {{
    saved = localStorage.getItem(storageKey);
  }} catch (_error) {{
    // The checkbox still works for the open page if its browser has no page storage.
  }}
  if (saved !== null) {{
    checkbox.checked = saved === "true";
    document.body.classList.toggle(bodyClass, checkbox.checked);
  }}
  checkbox.addEventListener("change", () => {{
    for (const hebrew of document.querySelectorAll(hebrewSelector)) {{
      hebrew.classList.remove(individualExpandedClass, individualNormalClass);
    }}
    document.body.classList.toggle(bodyClass, checkbox.checked);
    try {{
      localStorage.setItem(storageKey, String(checkbox.checked));
    }} catch (_error) {{
      // The page's in-memory preference remains usable without page storage.
    }}
  }});
  document.addEventListener("click", (event) => {{
    if (!(event.target instanceof Element)) {{
      return;
    }}
    const hebrew = event.target.closest(hebrewSelector);
    if (hebrew === null) {{
      return;
    }}
    event.preventDefault();
    const isExpanded = hebrew.classList.contains(individualExpandedClass) ||
      (!hebrew.classList.contains(individualNormalClass) &&
       document.body.classList.contains(bodyClass));
    hebrew.classList.toggle(individualExpandedClass, !isExpanded);
    hebrew.classList.toggle(individualNormalClass, isExpanded);
  }});
}})();
</script>
"""
_CASE_FILTER_SCRIPT = f"""<script>
const typeFilter = document.getElementById("{_CASE_TYPE_FILTER_ID}");
const caseRows = document.querySelectorAll("#{_CASE_TABLE_ID} tr[data-type]");
const selectedCount = document.getElementById("{_CASE_SELECTED_COUNT_ID}");

function updateCaseRows() {{
  let visibleCount = 0;
  for (const row of caseRows) {{
    const isSelected = typeFilter.value === "all" ||
      row.dataset.type === typeFilter.value ||
      row.dataset.subtype === typeFilter.value;
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  selectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

typeFilter.addEventListener("change", () => {{
  updateCaseRows();
}});
updateCaseRows();
</script>
"""
_LACKS_MAS_FILTER_SCRIPT = f"""<script>
const lacksMasSubtypeFilter = document.getElementById("{_LACKS_MAS_SUBTYPE_FILTER_ID}");
const lacksMasRows = document.querySelectorAll("#{_LACKS_MAS_TABLE_ID} tr[data-subtype]");
const lacksMasSelectedCount = document.getElementById("{_LACKS_MAS_SELECTED_COUNT_ID}");

function updateLacksMasRows() {{
  let visibleCount = 0;
  for (const row of lacksMasRows) {{
    const isSelected = lacksMasSubtypeFilter.value === "all" ||
      row.dataset.subtype === lacksMasSubtypeFilter.value;
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  lacksMasSelectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

lacksMasSubtypeFilter.addEventListener("change", () => {{
  updateLacksMasRows();
}});
updateLacksMasRows();
</script>
"""
_NOT_FIT_FILTER_SCRIPT = f"""<script>
const notFitTypeFilter = document.getElementById("{_NOT_FIT_TYPE_FILTER_ID}");
const notFitRows = document.querySelectorAll("#{_NOT_FIT_TABLE_ID} tr[data-type-codes]");
const notFitSelectedCount = document.getElementById("{_NOT_FIT_SELECTED_COUNT_ID}");

function updateNotFitRows() {{
  let visibleCount = 0;
  for (const row of notFitRows) {{
    const isSelected = notFitTypeFilter.value === "all" ||
      row.dataset.typeCodes.split(" ").includes(notFitTypeFilter.value);
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  notFitSelectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

notFitTypeFilter.addEventListener("change", () => {{
  updateNotFitRows();
}});
updateNotFitRows();
</script>
"""


def gen_html_files(
    out_dir: Path | None = None, *, trust_survey: bool = False
) -> tuple[str, str, str, str, str, str, str, str, str]:
    """Write the main page and its supporting pages.

    ``trust_survey`` reads the tracked ``out/accgram/post-stress-meteg.json`` instead of
    recomputing.  ``main_0_mega.py`` passes it because its survey step has just written that
    JSON, or in a cloud session has skipped the survey and left the tracked JSON unchanged.
    Off by hand, so a standalone run still derives the page from the corpus rather than from a
    file.
    """
    survey = psm.load_survey() if trust_survey else psm.build_survey()
    pin_claims(survey)
    post_silluq_cases = load_post_silluq_cases()
    koren_observations = load_post_silluq_koren_observations()
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    out_paths = (
        _write_page(top_dir / _FNAME, _TITLE, build_body(survey)),
        _write_page(
            top_dir / _METHODS_FNAME, _METHODS_TITLE, build_methods_body(survey)
        ),
        _write_page(top_dir / _CASES_FNAME, _CASES_TITLE, build_cases_body(survey)),
        _write_page(top_dir / _MISC_FNAME, _MISC_TITLE, build_misc_body(survey)),
        _write_page(
            top_dir / _LACKS_MAS_FNAME,
            _LACKS_MAS_TITLE,
            build_lacks_mas_body(survey),
        ),
        _write_page(
            top_dir / _NOT_FIT_FNAME,
            _NOT_FIT_TITLE,
            build_not_fit_body(survey),
        ),
        _write_page(
            top_dir / _POST_SILLUQ_FNAME,
            _POST_SILLUQ_TITLE,
            build_post_silluq_body(survey, post_silluq_cases, koren_observations),
        ),
        _write_page(
            top_dir / _CHRONICLES_8_11_FNAME,
            _CHRONICLES_8_11_TITLE,
            build_chronicles_8_11_body(survey),
        ),
        _write_page(
            top_dir / _NEXT_CONJUNCTIVE_FNAME,
            _NEXT_CONJUNCTIVE_TITLE,
            build_next_conjunctive_body(survey),
        ),
    )
    assert_no_phonetic_mam_annotations(out_paths, survey, post_silluq_cases)
    return out_paths


def assert_no_phonetic_mam_annotations(page_paths, survey, post_silluq_cases=None):
    """Validate every complete page against current MAM and the comparison source."""
    if post_silluq_cases is None:
        post_silluq_cases = load_post_silluq_cases()
    expected = {
        value
        for name, value in vars(site_data).items()
        if name.startswith("POST_STRESS_METEG") and name.endswith("_FNAME")
    }
    if (
        len(page_paths) != len(expected)
        or {Path(path).name for path in page_paths} != expected
    ):
        raise ValueError("MAS annotation validation requires every declared page")
    bhs_form = dict(_post_silluq_comparison(survey))["BHS"]
    uxlc_case_forms = {
        case["bcv"]: _verse_final_word(
            _uxlc_words(case["bcv"]), bcv=case["bcv"], source="UXLC 3.9"
        )
        for case in post_silluq_cases
        if case["form_source"] == "uxlc"
    }
    extra_sources = {
        f"{paths.in_dir() / 'UXLC-39'} {bcv}; case-ledger form": form
        for bcv, form in uxlc_case_forms.items()
    }
    extra_sources[
        f"{paths.in_dir() / 'UXLC-39'} {_POST_SILLUQ_VERSE}; BHS-labelled form, "
        "asserted equal to WLC 4.22"
    ] = bhs_form
    return post_stress_meteg_annotations.validate_pages(
        page_paths,
        survey,
        Path(__file__),
        extra_sources=extra_sources,
    )


def _write_page(path: Path, title: str, body: list) -> str:
    write_ctx = mb_html.WriteCtx(
        title,
        str(path),
        css_hrefs=(site_data.CSS_HREF, site_data.ACCGRAM_CSS_HREF),
        body_class=(
            "centered-page post-stress-meteg-page " f"{_HEBREW_SPACING_BODY_CLASS}"
        ),
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(body, write_ctx)
    return str(path)


def build_body(survey: dict) -> list:
    """The page, section by section, every figure in it read off ``survey``."""
    return [
        mb_html.heading_level_1(_visible_title(_TITLE)),
        _hebrew_spacing_option(),
        *_opening(survey),
        *_census(survey),
        *_mas_facts(survey),
        *_by_type(survey),
        *_case_list_link(survey),
        *_type_1_subtypes(survey),
        *_type_2_facts(survey),
        *_fit_for_mas_facts(survey),
        *_footnotes(survey),
    ]


def build_methods_body(survey: dict) -> list:
    """The source and scope details kept out of the main explanatory page."""
    return [
        mb_html.heading_level_1(_visible_title(_METHODS_TITLE)),
        _hebrew_spacing_option(),
        mb_html.heading_level_2("Use of Phonetic MAM"),
        mb_html.para(
            (
                "The location of a word's stress is not always obvious. In the"
                " research we present here, we locate stress using ",
                mb_html.anchor_h("Phonetic MAM", _PHONETIC_MAM_URL),
                ", which marks the stress of every word.",
            )
        ),
        mb_html.heading_level_2("Prose and poetic verses"),
        mb_html.para(
            "In the research we present here, we define "
            f"{author.dquote('prose')} and {author.dquote('poetic')} as follows:"
        ),
        mb_html.unordered_list(
            (
                "Prose verses are all verses of the 21 books plus the verses of Job's prose"
                " frame.",
                "Poetic verses are the verses of Job's main, poetic section plus all verses"
                " of Psalms and Proverbs.",
            )
        ),
        mb_html.heading_level_2(
            (_ROM_METEG_CAP, " after ", _ROM_SILLUQ, " in the census")
        ),
        mb_html.para(_mam_post_silluq_statement(survey)),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    ("comprehensive ", _ROM_METEG, "-after-", _ROM_SILLUQ, " page"),
                    _POST_SILLUQ_FNAME,
                ),
                " gives the comparative evidence, known cases, and unresolved candidates.",
            )
        ),
        *_census_definitions(survey),
        *_dually_cantillated_passages(survey),
        *_oleh_meteg_overlap(survey),
    ]


# --- the numbers, all of them read off the survey ------------------------------


def _count(survey: dict, system: str, category: str) -> int:
    return survey["counts"][system][category]


def _both(survey: dict, category: str) -> int:
    return _count(survey, _PROSE, category) + _count(survey, _POETIC, category)


def _type_2_type_3_overlap(survey: dict) -> dict:
    """The all-corpus set that could satisfy both type-2 and type-3 conditions."""
    return survey["type_2_type_3_overlap"]


def _dual_cantillation_facts(survey: dict, bcv: str) -> dict:
    """The source-derived facts for one numbered verse with both cantillation strands."""
    return survey["dual_cantillation"]["facts_by_numbered_verse"][bcv]


def _dual_cantillation(survey: dict) -> dict:
    """The one-reading method and cant-alef/cant-bet comparison."""
    return survey["dual_cantillation"]


def _by_type_count(survey: dict, kind: str) -> int:
    return sum(
        survey["post_stress_by_structural_type"][system][kind]
        for system in (_PROSE, _POETIC)
    )


def _fit_for_mas(survey: dict) -> dict:
    """The survey's candidate analysis of syllables fit for MAS."""
    return survey["fit_for_mas"]


def _actual_type_1_mas(survey: dict) -> dict:
    """The survey's complete structural type-1 MAS analysis."""
    return survey["actual_type_1_mas"]


def _lacks_mas_records(survey: dict) -> list[dict]:
    """Every chanted-word pair fit for MAS but lacking MAS, in corpus order."""
    return [
        record for record in _fit_for_mas(survey)["records"] if not record["has_mas"]
    ]


def _not_fit_for_mas_records(survey: dict) -> list[dict]:
    """Every MAS chanted word not fit for MAS, in corpus order."""
    return _fit_for_mas(survey)["not_fit_records"]


def _nonfinal_mas_syllable_records(survey: dict) -> list[dict]:
    """MAS records where a further final syllable follows the MAS syllable."""
    return [
        record for record in survey["post_stress"] if not record["is_the_last_syllable"]
    ]


def _noninitial_next_stress_records(survey: dict) -> list[dict]:
    """MAS records whose next chanted word does not have initial stress."""
    return [
        record
        for record in survey["post_stress"]
        if not record["next_chanted_word_is_initially_stressed"]
    ]


def _next_conjunctive_records(survey: dict) -> list[dict]:
    """MAS records whose next chanted word has a conjunctive accent."""
    records = [
        record
        for record in survey["post_stress"]
        if record["next_chanted_word_accent_classification"] == "conjunctive"
    ]
    assert all(record["next_chanted_word"] for record in records)
    return records


def _by_subtype_count(survey: dict, subtype: str) -> int:
    return sum(
        survey["post_stress_by_subtype"][system][subtype]
        for system in (_PROSE, _POETIC)
    )


def _subtype_records(survey: dict, subtype: str) -> list[dict]:
    """The post-stress records whose finer classification is ``subtype``."""
    return [one for one in survey["post_stress"] if one["subtype"] == subtype]


def _example_of(survey: dict, kind: str) -> dict:
    """The first record of a type, in the corpus's order, as that type's specimen.

    First rather than chosen: a hand-picked specimen is a claim with nothing behind it, and
    the whole set is on the page below anyway.
    """
    for record in survey["post_stress"]:
        if record["structural_type"] == kind:
            return record
    raise AssertionError(f"no post-stress record of type {kind!r} to show")


def _misc_almost_type_3_only_member(survey: dict) -> dict:
    """The only chanted word that fits CoS type (a), but not this survey's tsere-restricted type 3: Job 15:35."""
    records = [
        one
        for one in _subtype_records(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3)
        if one["bcv"] == "jb15:35"
    ]
    assert len(records) == 1, records
    return records[0]


def _assert_exact_keys(mapping: dict, expected_keys: set[str], label: str) -> None:
    """Require a summary mapping to name every category and no unknown category."""
    actual_keys = set(mapping)
    assert actual_keys == expected_keys, (label, actual_keys, expected_keys)


def pin_claims(survey: dict) -> None:
    """Validate the survey and every categorical or relational statement in the prose."""
    _check_survey_consistency(survey)
    _pin_prose_claims(survey)


def _check_survey_consistency(survey: dict) -> None:
    """Reconcile computed summaries without freezing their current populations."""
    systems = {_PROSE, _POETIC}
    count_categories = {
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg in the stressed syllable, no sof pasuq",
        "meteg after the stressed syllable",
        "silluq",
        "meteg sharing a letter with a non-stress-marking accent",
    }
    counts = survey["counts"]
    _assert_exact_keys(counts, systems, "count systems")
    for system in systems:
        _assert_exact_keys(
            counts[system], count_categories, f"{system} count categories"
        )

    post_stress = survey["post_stress"]
    assert len(post_stress) == _both(
        survey, "meteg after the stressed syllable"
    ), "the post-stress records and the post-stress count disagree"
    assert all(record["system"] in systems for record in post_stress)

    census = survey["census_chanted_word_summary"]
    _assert_exact_keys(census["by_system"], systems, "census systems")
    for system in systems:
        system_census = census["by_system"][system]
        _assert_exact_keys(system_census, {"mbs_only", "mas"}, f"{system} census")
        mas_records = sum(record["system"] == system for record in post_stress)
        assert system_census["mas"] == mas_records
    assert (
        census["mbs_only_chanted_words_with_more_than_two_mbs"]
        <= census["mbs_only_chanted_words_with_multiple_mbs"]
    )

    qamats = survey["qamats_variant_census"]
    _assert_exact_keys(qamats["by_system"], systems, "qamats-variant systems")
    grouping_entry_differences = Counter()
    for record in qamats["distinct_phonetic_groupings"]:
        assert record["system"] in systems
        grouping_entry_differences[record["system"]] += len(record["qamats-sam"]) - len(
            record["qamats-dal"]
        )
    qamats_categories = {
        "source_entries",
        "variant_rows",
        "duplicate_phonetic_reading_entries",
        "mam_chanted_words_counted",
    }
    for system in systems:
        system_qamats = qamats["by_system"][system]
        _assert_exact_keys(
            system_qamats, qamats_categories, f"{system} qamats-variant census"
        )
        assert system_qamats["source_entries"] == (
            system_qamats["mam_chanted_words_counted"]
            + system_qamats["duplicate_phonetic_reading_entries"]
        )
        assert system_qamats["duplicate_phonetic_reading_entries"] == (
            system_qamats["variant_rows"] + grouping_entry_differences[system]
        )
        assert (
            system_qamats["mam_chanted_words_counted"]
            == counts[system]["chanted words checked"]
        )

    structural_types = {*_TYPE_SOURCES, psm.TYPE_UNCLASSIFIED}
    by_type = survey["post_stress_by_structural_type"]
    _assert_exact_keys(by_type, systems, "structural-type systems")
    for system in systems:
        _assert_exact_keys(
            by_type[system], structural_types, f"{system} structural types"
        )
    assert Counter(
        (record["system"], record["structural_type"]) for record in post_stress
    ) == Counter(
        {
            (system, kind): by_type[system][kind]
            for system in systems
            for kind in structural_types
        }
    )

    subtypes = {psm.SUBTYPE_MISC_VAYOMER, psm.SUBTYPE_MISC_ALMOST_TYPE_3}
    by_subtype = survey["post_stress_by_subtype"]
    _assert_exact_keys(by_subtype, systems, "subtype systems")
    for system in systems:
        _assert_exact_keys(by_subtype[system], subtypes, f"{system} subtypes")
    assert Counter(
        (record["system"], record["subtype"])
        for record in post_stress
        if record["subtype"] is not None
    ) == Counter(
        {
            (system, subtype): by_subtype[system][subtype]
            for system in systems
            for subtype in subtypes
        }
    )

    actual_type_1_mas = _actual_type_1_mas(survey)
    type_1_patterns = {
        psm.TYPE_1_SUBTYPE_A,
        psm.TYPE_1_SUBTYPE_B,
        psm.TYPE_1_SUBTYPE_C,
        "not_initially_stressed",
    }
    pattern_counts = actual_type_1_mas["by_initial_stress_pattern"]
    _assert_exact_keys(pattern_counts, type_1_patterns, "type-1 patterns")
    for pattern, pattern_count in pattern_counts.items():
        _assert_exact_keys(
            pattern_count, {"cases", "by_system"}, f"type-1 pattern {pattern}"
        )
        _assert_exact_keys(
            pattern_count["by_system"], systems, f"type-1 pattern {pattern} systems"
        )
        assert pattern_count["cases"] == sum(pattern_count["by_system"].values())
        assert pattern_count["cases"] > 0
    assert actual_type_1_mas["cases"] == sum(
        pattern_count["cases"] for pattern_count in pattern_counts.values()
    )
    assert actual_type_1_mas["cases"] == _by_type_count(survey, psm.TYPE_OPEN)
    example_keys = actual_type_1_mas["example_keys_by_initial_stress_pattern"]
    _assert_exact_keys(example_keys, type_1_patterns, "type-1 example patterns")
    assert all(
        set(example_key) == {"bcv", "chanted_word", "jta"}
        for example_key in example_keys.values()
    )

    fit_for_mas = _fit_for_mas(survey)
    type_1_subtypes = {
        psm.TYPE_1_SUBTYPE_A,
        psm.TYPE_1_SUBTYPE_B,
        psm.TYPE_1_SUBTYPE_C,
    }
    _assert_exact_keys(
        fit_for_mas["by_type_1_subtype"], type_1_subtypes, "fit type-1 subtypes"
    )
    for subtype, counts_by_subtype in fit_for_mas["by_type_1_subtype"].items():
        _assert_exact_keys(
            counts_by_subtype,
            {"candidates", "with_mas", "without_mas", "with_mas_by_system"},
            f"fit type-1 subtype {subtype}",
        )
        _assert_exact_keys(
            counts_by_subtype["with_mas_by_system"],
            systems,
            f"fit type-1 subtype {subtype} systems",
        )
        assert counts_by_subtype["candidates"] == (
            counts_by_subtype["with_mas"] + counts_by_subtype["without_mas"]
        )
        assert counts_by_subtype["with_mas"] == sum(
            counts_by_subtype["with_mas_by_system"].values()
        )

    fit_types = {
        psm.FIT_TYPE_1_A,
        psm.FIT_TYPE_1_B,
        psm.FIT_TYPE_2_AF,
        psm.FIT_TYPE_2_BF,
        psm.FIT_TYPE_3,
    }
    by_fit_type = fit_for_mas["by_fit_type"]
    _assert_exact_keys(by_fit_type, fit_types, "fit types")
    for fit_type, fit_counts in by_fit_type.items():
        _assert_exact_keys(
            fit_counts,
            {"candidates", "with_mas", "without_mas"},
            f"fit type {fit_type}",
        )
        assert fit_counts["candidates"] == (
            fit_counts["with_mas"] + fit_counts["without_mas"]
        )
    assert fit_for_mas["fitting_any_type"] == sum(
        fit_counts["candidates"] for fit_counts in by_fit_type.values()
    )
    assert fit_for_mas["with_mas"] == sum(
        fit_counts["with_mas"] for fit_counts in by_fit_type.values()
    )
    assert fit_for_mas["without_mas"] == sum(
        fit_counts["without_mas"] for fit_counts in by_fit_type.values()
    )
    assert (
        fit_for_mas["with_mas"] + fit_for_mas["without_mas"]
        == fit_for_mas["fitting_any_type"]
    )
    assert (
        fit_for_mas["candidate_chanted_words"]
        >= fit_for_mas["non_type_specific_conditions"]
        >= fit_for_mas["fitting_any_type"]
    )
    assert (
        sum(fit_for_mas["accent_grammar_token_counts"].values())
        == fit_for_mas["candidate_chanted_words"]
    )

    fitting_records = fit_for_mas["records"]
    assert len(fitting_records) == fit_for_mas["fitting_any_type"]
    expected_fit_record_counts = Counter()
    for fit_type, fit_counts in by_fit_type.items():
        expected_fit_record_counts[(fit_type, True)] = fit_counts["with_mas"]
        expected_fit_record_counts[(fit_type, False)] = fit_counts["without_mas"]
    assert (
        Counter((record["fit_type"], record["has_mas"]) for record in fitting_records)
        == expected_fit_record_counts
    )
    assert len(_lacks_mas_records(survey)) == fit_for_mas["without_mas"]

    mas_not_in_the_table = fit_for_mas["mas_not_in_the_table"]
    _assert_exact_keys(
        mas_not_in_the_table,
        {
            "outside_the_three_types",
            "stress_not_penultimate",
            "next_word_not_disjunctive",
            "next_word_not_initially_stressed",
            "type_1_subtype_C",
            "type_2_subtype_C",
        },
        "MAS outside the fit table",
    )
    not_fit_records = _not_fit_for_mas_records(survey)
    assert sum(mas_not_in_the_table.values()) == len(not_fit_records)
    assert fit_for_mas["with_mas"] + len(not_fit_records) == len(post_stress)
    assert len(not_fit_records) == len(post_stress) - fit_for_mas["with_mas"]

    mas_with_mbs = census["mas_chanted_words_with_mbs"]
    mas_with_mbs_keys = {(record["bcv"], record["mam_form"]) for record in mas_with_mbs}
    assert len(mas_with_mbs_keys) == len(mas_with_mbs)
    post_stress_keys = {(record["bcv"], record["mam_form"]) for record in post_stress}
    assert len(post_stress_keys) == len(post_stress)
    assert mas_with_mbs_keys <= post_stress_keys

    type_2_groups = Counter(
        _type_2_filter_group(record) for record in _type_2_records(survey)
    )
    _assert_exact_keys(
        type_2_groups,
        {group for group, _code, _description in _TYPE_2_SUBTYPE_SPECS},
        "type-2 subtypes",
    )
    assert sum(type_2_groups.values()) == _by_type_count(survey, psm.TYPE_GUTTURAL)


def _pin_prose_claims(survey: dict) -> None:
    """Raise when corpus movement falsifies a statement rather than changing a figure."""
    post_stress = survey["post_stress"]
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    assert (
        census_chanted_word_summary["mbs_only_chanted_words_with_more_than_two_mbs"]
        == 0
    )
    mbs_only = sum(
        counts["mbs_only"]
        for counts in census_chanted_word_summary["by_system"].values()
    )
    mas = sum(
        counts["mas"] for counts in census_chanted_word_summary["by_system"].values()
    )
    assert mbs_only > mas, "the prose says a meteg almost always precedes the stress"
    qamats_grouping_differences = survey["qamats_variant_census"][
        "distinct_phonetic_groupings"
    ]
    assert {record["bcv"] for record in qamats_grouping_differences} == {
        "ps35:10",
        "pr19:7",
    }
    assert len(qamats_grouping_differences) == 2
    assert all(
        len(record["qamats-dal"]) == 1 and len(record["qamats-sam"]) == 2
        for record in qamats_grouping_differences
    )
    assert _both(survey, "meteg in the stressed syllable, no sof pasuq") == 0
    stress_accent_classification = survey["stress_accent_classification"]
    assert stress_accent_classification["counts"] == {
        "conjunctive": len(post_stress),
        "disjunctive": 0,
    }
    assert (
        stress_accent_classification["conclusion"]
        == "Every MAS has a conjunctive accent on that stress letter."
    )
    assert all(record["syllables_after_the_stress"] == 1 for record in post_stress)
    next_accent_classification = Counter(
        record["next_chanted_word_accent_classification"] for record in post_stress
    )
    assert set(next_accent_classification) <= {"disjunctive", "conjunctive"}
    assert sum(next_accent_classification.values()) == len(post_stress)
    fit_for_mas = _fit_for_mas(survey)
    mbs_and_mas = census_chanted_word_summary["mas_chanted_words_with_mbs"]
    assert all(
        record["mam_form"] is not None and record["mam_form"].count(psm.METEG) == 2
        for record in mbs_and_mas
    )
    not_fit_for_mas_records = _not_fit_for_mas_records(survey)
    assert all(
        record["chanted_word"]
        and record["next_chanted_word"]
        and record["mam_form"]
        and record["next_mam_form"]
        and not (
            record["meets_first_fit_for_mas_criterion"]
            and record["meets_second_fit_for_mas_criterion"]
            and record["meets_third_fit_for_mas_criterion"]
        )
        for record in not_fit_for_mas_records
    )
    fitting_records = fit_for_mas["records"]
    assert all(
        record["stress_syllable_has_conjunctive_accent"]
        and record["next_chanted_word_is_initially_stressed"]
        and record["next_chanted_word_has_disjunctive_accent"]
        and (
            record["fit_type"] not in {psm.FIT_TYPE_2_AF, psm.FIT_TYPE_2_BF}
            or not record["next_chanted_word_starts_with_a_vocal_shewa"]
        )
        and len(record["types"]) == 1
        and record["chanted_word"]
        and record["next_chanted_word"]
        and record["mam_form"]
        and record["next_mam_form"]
        for record in fitting_records
    )
    lacks_mas_records = _lacks_mas_records(survey)
    assert all(record["chanted_word"] for record in lacks_mas_records)
    misc_records = _misc_records(survey)
    assert all(one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in misc_records)
    for subtype in (
        psm.SUBTYPE_MISC_VAYOMER,
        psm.SUBTYPE_MISC_ALMOST_TYPE_3,
    ):
        subtype_records = _subtype_records(survey, subtype)
        assert all(
            one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in subtype_records
        )
    misc_almost_type_3 = _misc_almost_type_3_only_member(survey)
    assert _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3) == 1
    assert (
        misc_almost_type_3["vowel"] == "ḥolam"
        and misc_almost_type_3["is_the_last_syllable"]
        and not misc_almost_type_3["syllable_is_open"]
        and not misc_almost_type_3["chanted_word_is_closed_by_a_guttural"]
    )
    misc_vayomer_records = _subtype_records(survey, psm.SUBTYPE_MISC_VAYOMER)
    assert [
        one for one in post_stress if one.get("intervening_punctuation")
    ] == misc_vayomer_records
    # Both punctuation fields are normalized before comparison because a freshly built survey
    # carries tuples where a JSON round trip carries lists, and this routine has to accept
    # either: gen_html_files reads the tracked JSON only when trust_survey is on.
    assert all(
        tuple(one.get("intervening_punctuation", ())) == (psm.PASOLEG,)
        and list(one.get("intervening_mam_punctuation") or ())
        == [{"kind": "paseq", "glyph": psm.PASOLEG}]
        and one["next_mam_form"] is not None
        for one in misc_vayomer_records
    )
    type_2_records = _type_2_records(survey)
    assert all(
        record["chanted_word_is_closed_by_a_guttural"]
        and record["next_chanted_word_is_initially_stressed"]
        and not record["next_chanted_word_starts_with_a_vocal_shewa"]
        for record in type_2_records
    ), "the type-2 guttural, next-word-stress, or no-IVS fact has moved"
    assert all(
        record["syllables_after_the_stress"] == 1 for record in type_2_records
    ), "the type-2 penultimate-stress fact has moved"
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert {record["bcv"] for record in nonfinal_mas_syllable_records} == {
        "is63:12",
        "pr1:19",
        "pr11:26",
        "jb5:10",
    }
    assert len(nonfinal_mas_syllable_records) == 4
    assert all(
        record["syllables_after_the_stress"] == 1
        and record["structural_type"] == psm.TYPE_GUTTURAL
        and record["syllable_is_open"]
        and record["vowel"] == "tsere"
        and record["chanted_word_is_closed_by_a_guttural"]
        and final_stress.ends_in_furtive_patax(record["chanted_word"])
        for record in nonfinal_mas_syllable_records
    ), "the four nonfinal-MAS type-2 cases have moved"
    type_2_final_mas_records = [
        record for record in type_2_records if record["is_the_last_syllable"]
    ]
    assert all(
        not record["syllable_is_open"] and record["vowel"] == "pataḥ"
        for record in type_2_final_mas_records
    ), "the final-MAS type-2 cases have moved"
    type_3_records = [
        record
        for record in post_stress
        if record["structural_type"] == psm.TYPE_CLOSED_TSERE
    ]
    assert all(
        record["is_the_last_syllable"]
        and not record["syllable_is_open"]
        and record["vowel"] == "tsere"
        and record["next_chanted_word_is_initially_stressed"]
        for record in type_3_records
    ), "the type-3 finality or next-chanted-word-stress fact has moved"
    type_1_records = [
        record for record in post_stress if record["structural_type"] == psm.TYPE_OPEN
    ]
    assert all(record["is_the_last_syllable"] for record in type_1_records)
    noninitial_next_stress_records = _noninitial_next_stress_records(survey)
    assert len(noninitial_next_stress_records) == 1
    assert noninitial_next_stress_records[0]["bcv"] == "je46:14"
    assert noninitial_next_stress_records[0]["structural_type"] == psm.TYPE_OPEN
    type_2_type_3_overlap = _type_2_type_3_overlap(survey)
    assert type_2_type_3_overlap["chanted_words"] == sum(
        type_2_type_3_overlap["by_book"].values()
    )
    assert type_2_type_3_overlap["chanted_words"] == sum(
        type_2_type_3_overlap["by_final_letter"].values()
    )
    assert set(type_2_type_3_overlap["by_book"]) == {"da", "er"}
    assert set(type_2_type_3_overlap["by_final_letter"]) == {"\N{HEBREW LETTER HE}"}
    assert type_2_type_3_overlap["example"]["mam_form"] is not None
    assert _split(type_2_type_3_overlap["example"]["bcv"])[0] in {"da", "er"}
    assert survey["post_silluq"]["in_mam"] == sum(
        1 for one in post_stress if one["has_sof_pasuq"]
    ), "the post-silluq count and the records disagree"
    post_silluq_forms = dict(_post_silluq_comparison(survey))
    assert post_silluq_forms["MAM"].count(psm.METEG) == 1
    assert post_silluq_forms["BHS"].count(psm.METEG) == 2
    exodus = _dual_cantillation_facts(survey, "ex20:2")
    assert exodus["same_chanted_word_group_count"]
    assert all(len(branch) == 1 for branch in exodus["first_same_chanted_word_group"])
    genesis = _dual_cantillation_facts(survey, "gn35:22")
    assert genesis["same_chanted_word_group_count"] == 5
    dual_cantillation = _dual_cantillation(survey)
    whole_census_comparison = dual_cantillation["whole_census_comparison_counts"]
    template_comparison = dual_cantillation["template_counts"]
    cantillations = {psm.CANT_ALEF, psm.CANT_BET}
    comparison_categories = {
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    }
    _assert_exact_keys(
        whole_census_comparison, cantillations, "whole-census cantillations"
    )
    _assert_exact_keys(template_comparison, cantillations, "template cantillations")
    for cantillation in cantillations:
        _assert_exact_keys(
            whole_census_comparison[cantillation],
            comparison_categories,
            f"{cantillation} whole-census comparison",
        )
        _assert_exact_keys(
            template_comparison[cantillation],
            comparison_categories,
            f"{cantillation} template comparison",
        )
    assert dual_cantillation["counted_cantillation"] == psm.CANT_ALEF
    for category in comparison_categories:
        assert whole_census_comparison[psm.CANT_ALEF][category] == _both(
            survey, category
        )
    assert (
        whole_census_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"]
        == whole_census_comparison[psm.CANT_BET]["meteg after the stressed syllable"]
    )
    assert template_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"] == 0
    assert template_comparison[psm.CANT_BET]["meteg after the stressed syllable"] == 0
    for category in (
        "chanted words checked",
        "meteg before the stressed syllable",
    ):
        assert (
            abs(
                template_comparison[psm.CANT_ALEF][category]
                - template_comparison[psm.CANT_BET][category]
            )
            == 1
        )
    assert survey["post_silluq"]["in_mam"] == 0
    difference = dual_cantillation["meteg_before_stress_difference"]
    assert difference["bcv"] == "dt5:6"
    assert len(difference[psm.CANT_ALEF]["chanted_words"]) == 2
    assert len(difference[psm.CANT_BET]["chanted_words"]) == 2
    chanted_word_difference = dual_cantillation["chanted_word_count_difference"]
    assert chanted_word_difference["bcv"] == "dt5:14"
    assert len(chanted_word_difference[psm.CANT_ALEF]["chanted_words"]) == 2
    assert len(chanted_word_difference[psm.CANT_BET]["chanted_words"]) == 1
    for kind in (*_TYPE_SOURCES, psm.TYPE_UNCLASSIFIED):
        if _by_type_count(survey, kind):
            _example_of(survey, kind)
    for bcv in (
        _POST_SILLUQ_VERSE,
        _MAM_POST_SILLUQ_VERSE,
        _CHRONICLES_8_11_VERSE,
    ):
        assert bcv in survey["currency"]["focus_verses"], (
            f"{bcv} is named in the page's prose but the survey records no chanted word"
            " for it; add it to post_stress_meteg._FOCUS_VERSES"
        )
    _excerpt_accounting()


def _excerpt_accounting() -> tuple[int, int]:
    """The page's quotation accounting: every excerpt's length, and the sum of them.

    The plan's decision 2 caps one excerpt at 150 words and all of them together at 300, and
    requires the generator to enforce both whenever it has excerpts.  This page has none, so
    what is enforced is that the list is empty and the accounting reads zero.
    """
    lengths = [len(text.split()) for _source, text in _EXCERPTS]
    for (source, _text), length in zip(_EXCERPTS, lengths):
        assert length <= _MAX_WORDS_PER_EXCERPT, f"{source}: {length} words"
    assert sum(lengths) <= _MAX_WORDS_IN_ALL_EXCERPTS, sum(lengths)
    assert not _EXCERPTS, "this page quotes neither book; see the module docstring"
    return len(_EXCERPTS), sum(lengths)


# --- rendering helpers ---------------------------------------------------------


def itm_sections(reference: str) -> tuple:
    """An ITM reference whose adapted section numbers open the corresponding section."""
    out = []
    end = 0
    for match in _ITM_SECTION_REFERENCE.finditer(reference):
        out.append(reference[end : match.start()])
        section = int(match["section"])
        url = _ITM_ADAPTATION_URL_BY_SECTION[section]
        out.extend(
            (
                "§",
                mb_html.anchor(
                    str(section),
                    {"href": url, "target": "_blank", "rel": "noopener"},
                ),
            )
        )
        end = match.end()
    out.append(reference[end:])
    return tuple(out)


def itm() -> object:
    """The abbreviated book name, with Yeivin's title on hover."""
    return mb_html.abbr("ITM", {"title": _ITM_GLOSS})


def cos() -> object:
    """The abbreviated book name, with Breuer's title on hover."""
    return mb_html.abbr("CoS", {"title": _COS_GLOSS})


def _para(text: str) -> object:
    """One paragraph, its pointed Hebrew runs wrapped so they take the Hebrew font."""
    return mb_html.para(wrap_hebrew_runs(text))


def _spelled(count: int) -> str:
    """A count in prose: spelled out below five, a numeral from five up."""
    return {1: "one", 2: "two", 3: "three", 4: "four"}.get(count, f"{count:,}")


def _hebrew_cell(form: str | None) -> tuple:
    """A pointed reader-facing Hebrew form wrapped as an hbo run for an RTL table cell."""
    return wrap_hebrew_runs((form or "").replace(psm.hpu.NU_GMAQ, psm.MAQAF))


def _ref_link(bcv: str, text: str | None = None) -> object:
    """The reference, linked to the verse in MAM with doc."""
    bb, chnu, vrnu = _split(bcv)
    return mb_html.anchor_h(
        text or ref_abbrev(bcv),
        rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu),
    )


def _footnote_callout(number: int, footnote_id: str) -> object:
    """The in-line phi marker that links down to one footnote."""
    return mb_html.anchor_h(f"φ{number}", f"#{footnote_id}")


def _split(bcv: str) -> tuple[str, int, int]:
    bb = bcv[:2]
    chnu, _colon, vrnu = bcv[2:].partition(":")
    return bb, int(chnu), int(vrnu)


def _table(headers: tuple, rows: list, attr: dict | None = None) -> object:
    return mb_html.table(
        [mb_html.table_row_of_headers(headers), *rows],
        attr or {"class": "limited-width post-stress-meteg-table"},
    )


def _singleton_example_table(bcv: str, form: tuple) -> object:
    """One example displayed in the same two-column table as a multi-row example set."""
    return mb_html.table(
        [
            mb_html.table_row_of_data(
                (_ref_link(bcv), form),
                (None, _HEBREW_CELL),
            )
        ],
        {"class": "limited-width post-stress-meteg-table"},
    )


def _cantillation_label(cantillation: str) -> tuple:
    """One visible cantillation-branch label, with its Hebrew letter name italicized."""
    by_cantillation = {
        psm.CANT_ALEF: _ROM_ALEF,
        psm.CANT_BET: _ROM_BET,
    }
    return ("cant-", by_cantillation[cantillation])


def _hebrew_spacing_option() -> object:
    """The page-wide control for the pointed Hebrew's letter spacing."""
    return mb_html.raw_html(
        _HEBREW_SPACING_OPTION.replace(
            "__SPACING_TEXT__",
            "This checkbox controls whether Hebrew letter spacing is expanded in this"
            " document.",
        ).replace(
            "__TOGGLE_TEXT__",
            "Alternatively, you can click on an individual Hebrew word to toggle only that word's"
            " spacing.",
        )
    )


# --- the sections --------------------------------------------------------------


def _opening(survey: dict) -> list:
    """Section 1: what is counted, and where the silluq boundary falls."""
    total = _both(survey, "meteg after the stressed syllable")
    example = _example_of(survey, psm.TYPE_OPEN)
    return [
        mb_html.para(
            (
                "A ",
                _ROM_METEG,
                " almost always comes before the stressed syllable of its word, but it can"
                " also come after the stress. MAM has ",
                f"{total:,} cases of ",
                _ROM_METEG,
                " after the stress (MAS). For example:",
            )
        ),
        _singleton_example_table(example["bcv"], _case_chanted_word_cell(example)),
        mb_html.para(
            (
                "In this document, by "
                f"{author.dquote('word')} we mean either a simple word (having just one"
                " atom) or a compound word (having two or more atoms"
                " connected by ",
                _ROM_MAQAF,
                " marks). By "
                f"{author.dquote('atom')} we mean a sequence of pointed letters uninterrupted by"
                " space, ",
                _ROM_MAQAF,
                ", or any other punctuation.",
            )
        ),
    ]


def _census(survey: dict) -> list:
    """Section 2: the counts, prose verses beside poetic verses."""
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation system"}),
        mb_html.abbr("words", {"title": "count of words"}),
        mb_html.abbr(
            "MBS_O",
            {"title": _MBS_O_CENSUS_GLOSS},
        ),
        mb_html.abbr(
            "MAS",
            {"title": _MAS_CENSUS_GLOSS},
        ),
        mb_html.abbr(
            "% MAS",
            {"title": "MAS/(MAS+MBS_O)"},
        ),
    )
    numeric = (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL)
    labels = {_PROSE: "prose", _POETIC: "poetic"}
    counts_by_system = {
        system: {
            "chanted_words": _count(survey, system, "chanted words checked"),
            **census_chanted_word_summary["by_system"][system],
        }
        for system in (_PROSE, _POETIC)
    }
    all_counts = {
        category: sum(counts[category] for counts in counts_by_system.values())
        for category in ("chanted_words", "mbs_only", "mas")
    }

    def row(label: str, counts: dict[str, int]) -> object:
        mbs_only = counts["mbs_only"]
        mas = counts["mas"]
        return mb_html.table_row_of_data(
            (
                label,
                f"{counts['chanted_words']:,}",
                f"{mbs_only:,}",
                f"{mas:,}",
                f"{mas / (mbs_only + mas):.1%}",
            ),
            numeric,
        )

    rows = [
        row(labels[system], counts_by_system[system]) for system in (_PROSE, _POETIC)
    ]
    rows.append(row("all", all_counts))
    mbs_only = all_counts["mbs_only"]
    mas = all_counts["mas"]
    return [
        mb_html.heading_level_2("MAS census by cantillation system"),
        _table(headers, rows),
        mb_html.para(
            (
                "So, among words with at least one ",
                _ROM_METEG,
                " mark, there are ",
                f"{mas:,}",
                " words where one of the ",
                _ROM_METEG,
                " marks is after the stress and ",
                f"{mbs_only:,}",
                " words where none of the ",
                _ROM_METEG,
                " marks is after the stress. (There is never more than one ",
                _ROM_METEG,
                " mark after the stress.) See the ",
                mb_html.anchor_h("Methods", _METHODS_FNAME),
                " page for more details.",
            )
        ),
    ]


def _census_definitions(survey: dict) -> list:
    """The chanted-word definitions that govern the main census table."""
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    multiple_mbs = census_chanted_word_summary[
        "mbs_only_chanted_words_with_multiple_mbs"
    ]
    more_than_two_mbs = census_chanted_word_summary[
        "mbs_only_chanted_words_with_more_than_two_mbs"
    ]
    assert more_than_two_mbs == 0
    records = census_chanted_word_summary["mas_chanted_words_with_mbs"]
    # The (sub)type column shows the structural taxonomy, so the label comes off the
    # post-stress record; the census section makes no Fit-for-MAS claim.
    post_stress_by_bcv_and_mam_form = {
        (one["bcv"], one["mam_form"]): one for one in survey["post_stress"]
    }
    assert len(post_stress_by_bcv_and_mam_form) == len(survey["post_stress"])
    assert {(record["bcv"], record["mam_form"]) for record in records} <= set(
        post_stress_by_bcv_and_mam_form
    )
    return [
        mb_html.heading_level_2("Census definitions"),
        mb_html.para(
            (
                mb_html.abbr("MBS_O", {"title": _MBS_O_CENSUS_GLOSS}),
                " counts words that have one or more ",
                _ROM_METEG,
                " marks before the"
                f" stress and none after it. The {author.dquote('O')} means"
                f" {author.dquote('only')}. ",
                mb_html.abbr("MAS", {"title": _MAS_CENSUS_GLOSS}),
                " counts words that have one or more ",
                _ROM_METEG,
                " marks after the stress, whether the word has zero or more ",
                _ROM_METEG,
                " marks before the stress.",
            )
        ),
        mb_html.para(
            "The % MAS column is the MAS count divided by the sum of the MBS_O and MAS counts.",
        ),
        mb_html.para(
            (
                f"{multiple_mbs:,} MBS_O words have more than one ",
                _ROM_METEG,
                " mark. Every such MBS_O word has exactly two ",
                _ROM_METEG,
                " marks.",
            )
        ),
        mb_html.para(
            (
                "No MAS word has more than one ",
                _ROM_METEG,
                " mark after the stress: every MAS word has exactly one ",
                _ROM_METEG,
                " mark after the stress.",
            ),
        ),
        mb_html.para(
            (
                f"There are {_spelled(len(records))} MAS words that also have one ",
                _ROM_METEG,
                " mark before the stress. They are listed below. (There are no MAS words with more than one ",
                _ROM_METEG,
                " before the stress.)",
            ),
        ),
        _table(
            ("", "", "(sub)types"),
            [
                mb_html.table_row_of_data(
                    (
                        _ref_link(record["bcv"]),
                        _case_chanted_word_cell(
                            post_stress_by_bcv_and_mam_form[
                                (record["bcv"], record["mam_form"])
                            ]
                        ),
                        _structural_subtype_cell(
                            post_stress_by_bcv_and_mam_form[
                                (record["bcv"], record["mam_form"])
                            ]
                        ),
                    ),
                    (None, _HEBREW_CELL, None),
                )
                for record in records
            ],
        ),
    ]


def _mas_facts(survey: dict) -> list:
    """Section 3: the facts shared by every MAS, before structural classification."""
    exceptions = _noninitial_next_stress_records(survey)
    assert len(exceptions) == 1
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert len(nonfinal_mas_syllable_records) == 4
    next_conjunctive = _next_conjunctive_records(survey)
    total = len(survey["post_stress"])
    assert (
        len(next_conjunctive)
        + sum(
            record["next_chanted_word_accent_classification"] == "disjunctive"
            for record in survey["post_stress"]
        )
        == total
    )
    return [
        mb_html.heading_level_2("Facts about MAS"),
        mb_html.unordered_list(
            (
                (
                    "In every MAS case, the stressed syllable has a conjunctive accent (",
                    _footnote_callout(1, _POST_SILLUQ_FOOTNOTE_ID),
                    ").",
                ),
                "In every MAS case, the MAS syllable comes right after the stressed syllable.",
                (
                    "In every MAS case except four (",
                    _footnote_callout(2, _NONFINAL_MAS_FOOTNOTE_ID),
                    "), the MAS syllable is final.",
                ),
                (
                    "In every MAS case but one (",
                    _footnote_callout(3, _JEREMIAH_FOOTNOTE_ID),
                    "), the next word has initial stress.",
                ),
                (
                    f"In {(total - len(next_conjunctive)) / total:.1%} of MAS cases (",
                    _footnote_callout(4, _NEXT_CONJUNCTIVE_FOOTNOTE_ID),
                    "), the next word has a disjunctive accent.",
                ),
            )
        ),
    ]


def _by_type(survey: dict) -> list:
    """Section 4: the three types the two books describe, and what is left over."""
    headers = (
        "Type",
        "Prose",
        "Poetic",
        "All",
        "Example",
    )
    unclassified = psm.TYPE_UNCLASSIFIED
    unclassified_count = _by_type_count(survey, unclassified)
    rows = []
    for kind, (yeivin, breuer) in _TYPE_SOURCES.items():
        example = _example_of(survey, kind)
        rows.append(
            mb_html.table_row_of_data(
                (
                    _case_type_cell(kind),
                    str(survey["post_stress_by_structural_type"][_PROSE][kind]),
                    str(survey["post_stress_by_structural_type"][_POETIC][kind]),
                    str(_by_type_count(survey, kind)),
                    _case_chanted_word_cell(example),
                ),
                (
                    None,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    _HEBREW_CELL,
                ),
            )
        )
    rows.append(
        mb_html.table_row_of_data(
            (
                "misc",
                str(survey["post_stress_by_structural_type"][_PROSE][unclassified]),
                str(survey["post_stress_by_structural_type"][_POETIC][unclassified]),
                str(unclassified_count),
                _case_chanted_word_cell(_example_of(survey, unclassified)),
            ),
            (
                None,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                _HEBREW_CELL,
            ),
        )
    )
    all_prose_count = sum(survey["post_stress_by_structural_type"][_PROSE].values())
    all_poetic_count = sum(survey["post_stress_by_structural_type"][_POETIC].values())
    all_count = all_prose_count + all_poetic_count
    assert all_count == len(survey["post_stress"])
    rows.append(
        mb_html.table_row_of_data(
            (
                mb_html.abbr("all", {"title": "All cases: types 1, 2, 3, and misc."}),
                str(all_prose_count),
                str(all_poetic_count),
                str(all_count),
                "",
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
        )
    )
    return [
        mb_html.heading_level_2("The three types of MAS"),
        mb_html.para(
            (
                f"All but {unclassified_count} cases of MAS can be sorted into one of the three"
                " following types: (",
                _footnote_callout(5, _SOURCES_FOR_TYPES_FOOTNOTE_ID),
                ")",
            )
        ),
        mb_html.ordered_list(
            (
                "The MAS syllable is open and final.",
                "The MAS word is closed by a guttural.",
                (
                    "The MAS syllable is closed, final, and ",
                    _ROM_TSERE,
                    "-voweled. (",
                    _footnote_callout(6, _TYPE_2_TYPE_3_FOOTNOTE_ID),
                    ")",
                ),
            )
        ),
        _table(headers, rows),
    ]


def _sources_for_types_footnote() -> list:
    """Footnote 5: sources for the three types."""
    source_rows = [
        mb_html.table_row_of_data(
            (
                _case_type_cell(kind),
                itm_sections(yeivin),
                breuer,
                _COS_CH_14_BY_TYPE[kind],
            ),
            (None, None, None, None),
        )
        for kind, (yeivin, breuer) in _TYPE_SOURCES.items()
    ]
    cos_page_rows = [
        mb_html.table_row_of_data(
            (
                _case_type_cell(kind),
                _COS_PAGE_STARTS_BY_TYPE[kind],
                _COS_CH_14_PAGES_BY_TYPE[kind],
            ),
            (None, None, None),
        )
        for kind in _TYPE_SOURCES
    ]
    return [
        mb_html.heading_level_3(
            "φ5 — Sources for types 1–3", {"id": _SOURCES_FOR_TYPES_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                "The three types of MAS are described in both ",
                itm(),
                " and ",
                cos(),
                ". Exactly what words are included in and excluded from these three types"
                " varies among ITM, CoS, and our document here, but they broadly agree.",
            )
        ),
        _table(
            (
                "Type",
                itm(),
                (cos(), " Ch. 8"),
                (cos(), " Ch. 14 §8"),
            ),
            source_rows,
        ),
        mb_html.para(
            (
                "For those using the Wengrov translation of ",
                cos(),
                ", below is a table of the page numbers corresponding to the section"
                " identifiers in the table above:",
            )
        ),
        _table(
            (
                "Type",
                mb_html.abbr("CoS Ch. 8 pg", {"title": _COS_CH_8_PAGE_GLOSS}),
                mb_html.abbr(
                    "CoS Ch. 14 §8 pg",
                    {
                        "title": (
                            "printed page in Wengrov's English translation of CoS on which"
                            " the cited Ch. 14 §8 item begins"
                        )
                    },
                ),
            ),
            cos_page_rows,
        ),
    ]


def _case_list_link(survey: dict) -> list:
    """The main page's link to the long list of individual cases."""
    misc_count = _by_type_count(survey, psm.TYPE_UNCLASSIFIED)
    return [
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    f"{len(survey['post_stress']):,} individual cases", _CASES_FNAME
                ),
                " are listed separately and can be filtered by (sub)type. The ",
                mb_html.anchor_h(f"{misc_count:,} misc cases", _MISC_FNAME),
                " appear in that large list, but are also further discussed on a page of"
                " their own.",
            )
        )
    ]


def _type_2_facts(survey: dict) -> list:
    """The type-2 subtype section."""
    return _type_2_subtypes(survey)


def _type_1_example(survey: dict, example_key: dict) -> dict:
    """The MAM-backed post-stress record identified by a type-1 summary example key."""
    matches = [
        record
        for record in survey["post_stress"]
        if all(record[key] == value for key, value in example_key.items())
    ]
    assert len(matches) == 1, (example_key, matches)
    return matches[0]


def _type_1_subtypes(survey: dict) -> list:
    """The complete structural type-1 MAS population by next-chanted-word-stress subtype."""
    type_1_mas = _actual_type_1_mas(survey)
    pattern_counts = type_1_mas["by_initial_stress_pattern"]
    example_keys = type_1_mas["example_keys_by_initial_stress_pattern"]
    headers = (
        "Subtype",
        "Prose",
        "Poetic",
        "All",
        "Example",
    )
    labels = {
        psm.TYPE_1_SUBTYPE_A: "1A",
        psm.TYPE_1_SUBTYPE_B: "1B",
        psm.TYPE_1_SUBTYPE_C: "1C",
        "not_initially_stressed": "1D",
    }
    rows = [
        mb_html.table_row_of_data(
            (
                labels[pattern],
                str(counts["by_system"][_PROSE]),
                str(counts["by_system"][_POETIC]),
                str(counts["cases"]),
                _case_chanted_word_cell(_type_1_example(survey, example_keys[pattern])),
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
        )
        for pattern, counts in pattern_counts.items()
    ]
    total = sum(counts["cases"] for counts in pattern_counts.values())
    assert total == type_1_mas["cases"]
    return [
        mb_html.heading_level_2("The four subtypes of MAS type 1"),
        mb_html.para(
            "Based on properties of the next word, all cases of MAS type 1 can be sorted"
            " into one of the four following subtypes:"
        ),
        mb_html.unordered_list(
            (
                (
                    "1A: The next word has initial stress and an initial vocal ",
                    _ROM_SHEWA,
                    ". (",
                    _footnote_callout(7, _VOCAL_SHEWA_FOOTNOTE_ID),
                    ")",
                ),
                (
                    "1B: The next word has a ",
                    _ROM_PASHTA,
                    " stress helper on its first letter. (",
                    _footnote_callout(8, _PASHTA_STRESS_HELPER_FOOTNOTE_ID),
                    ")",
                ),
                ("1C: Like 1B, but with some accent other than ", _ROM_PASHTA, "."),
                "1D: The next word does not have initial stress.",
            )
        ),
        _table(headers, rows),
    ]


def _type_2_subtypes(survey: dict) -> list:
    """The complete structural type-2 MAS population by next-chanted-word initial consonant."""
    records_by_group = {
        group: [] for group, _code, _description in _TYPE_2_SUBTYPE_SPECS
    }
    for record in _type_2_records(survey):
        records_by_group[_type_2_filter_group(record)].append(record)
    rows = []
    for group, code, _description in _TYPE_2_SUBTYPE_SPECS:
        records = records_by_group[group]
        assert records, group
        rows.append(
            mb_html.table_row_of_data(
                (
                    code,
                    str(sum(record["system"] == _PROSE for record in records)),
                    str(sum(record["system"] == _POETIC for record in records)),
                    str(len(records)),
                    _case_chanted_word_cell(records[0]),
                ),
                (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
            )
        )
    total = sum(len(records) for records in records_by_group.values())
    assert total == _by_type_count(survey, psm.TYPE_GUTTURAL)
    return [
        mb_html.heading_level_2("The three subtypes of MAS type 2"),
        mb_html.para(
            "Based on properties of the next word, all cases of MAS type 2 can be sorted"
            " into one of the three following subtypes:"
        ),
        mb_html.unordered_list(
            tuple(description for _group, _code, description in _TYPE_2_SUBTYPE_SPECS)
        ),
        _table(("Subtype", "Prose", "Poetic", "All", "Example"), rows),
    ]


def _case_type_code(kind: str) -> str:
    return _TYPE_CODES.get(kind, ("other", ""))[0]


def _case_type_cell(kind: str, *, misc_label: bool = False) -> object:
    """A type label, with the subpages' shorter vocabulary and misc label when requested."""
    if kind in _TYPE_CODES:
        code, gloss = _TYPE_CODES[kind]
        return mb_html.abbr(code, {"title": f"Type {code}: {gloss}."})
    if misc_label:
        return "misc"
    return mb_html.abbr("—", {"title": "Not one of types 1, 2, or 3."})


def _fit_type_cell(fit_type: str) -> object:
    """One Fit-for-MAS table label, including the two admitted type-1 subtypes."""
    titles = {
        psm.FIT_TYPE_1_A: (
            "Type 1A: type 1 where the next word has initial stress and an initial"
            " vocal shewa."
        ),
        psm.FIT_TYPE_1_B: (
            "Type 1B: type 1 where the next word has a pashta stress helper on its"
            " first letter, and so no initial vocal shewa."
        ),
        psm.FIT_TYPE_2_AF: (
            "Fit for MAS type 2Af: the word is closed by a guttural; the next word"
            " begins with ל (lamed) and does not begin with vocal shewa."
        ),
        psm.FIT_TYPE_2_BF: (
            "Fit for MAS type 2Bf: the word is closed by a guttural; the next word"
            " begins with a guttural and does not begin with vocal shewa."
        ),
        psm.FIT_TYPE_3: "Type 3: the MAS syllable is closed, final, and tsere-voweled.",
    }
    return mb_html.abbr(fit_type, {"title": titles[fit_type]})


def _structural_subtype_cell(record: dict) -> object:
    """One structural (sub)type label, the taxonomy the cases page's Subtype column uses.

    Ben's decision of 2026-09-08, on the Methods page's table of MAS words that also have a
    meteg before the stress: the fit-for-MAS codes 2Af and 2Bf are reserved for a fit-for-MAS
    context, and that table sits under Census definitions, which never mentions fitness.  Only
    1 Samuel 22:17 shows the difference -- the rest of that table is 1A and 3, which read the
    same in either taxonomy.
    """
    subtype = _case_filter_subtype(record)
    if subtype is None:
        return _case_type_cell(record["structural_type"], misc_label=True)
    return mb_html.abbr(subtype, {"title": _SUBTYPE_DESCRIPTIONS[subtype]})


def _case_subtype_cell(subtype: str | None) -> object:
    """The subtype only where a misc record has a named nearer condition."""
    if subtype is None:
        return ""
    gloss_by_subtype = {
        psm.SUBTYPE_MISC_VAYOMER: (
            "A vayomer case with one intervening paseq before the next word."
        ),
        psm.SUBTYPE_MISC_ALMOST_TYPE_3: (
            "A final closed ḥolam syllable: CoS's long-vowel type (a), but not"
            " our type 3, which is restricted to tsere."
        ),
    }
    visible_label: object = subtype
    if subtype == psm.SUBTYPE_MISC_VAYOMER:
        visible_label = ("misc-", _ROM_VAYOMER)
    return mb_html.abbr(visible_label, {"title": gloss_by_subtype[subtype]})


def _next_chanted_word_span(
    next_word: str, punctuation: tuple[dict[str, str], ...] | list[dict[str, str]] = ()
) -> object:
    """The next chanted word and each preceding native narrow-sense paseq."""
    demoted = []
    for marker in punctuation:
        assert marker["kind"] == "paseq", marker
        demoted.extend((*_hebrew_cell(marker["glyph"]), " "))
    demoted.extend(_hebrew_cell(next_word))
    return mb_html.span(
        tuple(demoted),
        {"class": _NEXT_WORD_CLASS},
    )


def _native_mam_punctuation_parts(
    punctuation: tuple[dict[str, str], ...] | list[dict[str, str]],
) -> tuple[list[str], list[dict[str, str]]]:
    """The marks MAM attaches visually to the preceding and the next chanted words."""
    preceding = []
    next_marks = []
    for marker in punctuation:
        kind = marker["kind"]
        if kind == "legarmeh":
            preceding.append(marker["glyph"])
        elif kind == "paseq":
            next_marks.append(marker)
        else:
            raise AssertionError(
                f"unclassified MAM punctuation in page data: {marker!r}"
            )
    return preceding, next_marks


def _paired_chanted_word_cell(
    current_form: str,
    next_form: str,
    punctuation: tuple[dict[str, str], ...] | list[dict[str, str]] = (),
) -> tuple:
    """One MAM chanted-word pair, with punctuation placed by MAM's native category."""
    preceding_punctuation, next_punctuation = _native_mam_punctuation_parts(punctuation)
    return (
        *_hebrew_cell(current_form),
        *[part for glyph in preceding_punctuation for part in _hebrew_cell(glyph)],
        " ",
        _next_chanted_word_span(
            next_form,
            next_punctuation,
        ),
    )


def _mam_form(record: dict) -> str:
    """The record's MAM form, from the survey and from nowhere else.

    RENDERING NEVER READS MAM-PRIVATE, so a displayed record with no ``mam_form`` stops the
    render instead of being given a substitute spelling.  The survey lists such records under
    ``diagnostics.records_without_a_mam_form``.  Until 2026-09-10 this module looked a spelling
    up in MAM-private's Phonetic MAM for them, which made a render from the tracked survey
    depend on the private clone whenever such a record was displayed.  CLAUDE.md's section "A
    code path reads MAM-private every time it runs, or never" states the rule that retired it.
    """
    mam_form = record["mam_form"]
    if not mam_form:
        raise psm.SurveyProblem(
            f"{record['bcv']}: a displayed record has no mam_form (listed under the survey's"
            " diagnostics.records_without_a_mam_form); the page does not look one up in"
            " MAM-private"
        )
    return mam_form


def _case_chanted_word_cell(record: dict) -> tuple:
    """The MAM MAS form followed by its next chanted word."""
    # _mam_form first: a record with no MAM form has no next MAM form either, so the
    # assertion below would otherwise fire first and name the wrong cause.
    mam_form = _mam_form(record)
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
    return _paired_chanted_word_cell(
        mam_form,
        next_word,
        record.get("intervening_mam_punctuation", ()),
    )


def _oleh_chanted_word_cell(record: dict) -> tuple:
    """The oleh context, extending into the next chanted word only for a yored there."""
    current_form = _mam_form(record)
    if ha.MER in current_form:
        return _hebrew_cell(current_form)
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no MAM form after oleh"
    assert ha.MER in next_word, f"{record['bcv']}: no yored after oleh"
    return _paired_chanted_word_cell(
        current_form,
        next_word,
        record.get("intervening_mam_punctuation", ()),
    )


def _case_row(record: dict) -> object:
    subtype = _case_filter_subtype(record)
    attrs = {"data-type": _case_type_code(record["structural_type"])}
    if subtype is not None:
        attrs["data-subtype"] = subtype
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(
                _case_type_cell(record["structural_type"], misc_label=True)
            ),
            mb_html.table_datum(
                subtype
                if subtype is not None
                else _case_subtype_cell(record["subtype"])
            ),
        ),
        attrs,
    )


def _case_type_filter(case_count: int) -> object:
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in _CASE_FILTER_OPTIONS
    )
    return mb_html.raw_html(
        f'<p><label for="{_CASE_TYPE_FILTER_ID}">Show </label>'
        f'<select id="{_CASE_TYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_CASE_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _type_2_records(survey: dict) -> list[dict]:
    """The survey's type-2 records, in the corpus's order."""
    return [
        record
        for record in survey["post_stress"]
        if record["structural_type"] == psm.TYPE_GUTTURAL
    ]


def _misc_records(survey: dict) -> list[dict]:
    """The survey's misc records, in the corpus's order."""
    return [
        record
        for record in survey["post_stress"]
        if record["structural_type"] == psm.TYPE_UNCLASSIFIED
    ]


def _type_2_next_group(record: dict) -> str:
    """The detailed type-2 group set by the next chanted word's first consonant."""
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
    return psm.type_2_next_filter_group(next_word)


def _type_2_filter_group(record: dict) -> str:
    """The coarser type-2 filter group shown on the cases page."""
    detailed_group = _type_2_next_group(record)
    if detailed_group in ("lamed", "guttural"):
        return detailed_group
    return "not-lamed-or-guttural"


def _type_1_subtype_code(record: dict) -> str:
    """The reader-facing subtype code for one structural type-1 record."""
    assert record["structural_type"] == psm.TYPE_OPEN, record
    return _TYPE_1_SUBTYPE_CODES[record["type_1_subtype"]]


def _case_filter_subtype(record: dict) -> str | None:
    """The subtype used by the all-cases page's flat filter list."""
    structural_type = record["structural_type"]
    if structural_type == psm.TYPE_OPEN:
        return _type_1_subtype_code(record)
    if structural_type == psm.TYPE_GUTTURAL:
        return _TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP[_type_2_filter_group(record)]
    return None


def _lacks_mas_case_row(record: dict) -> object:
    """One MAM chanted-word pair fit for MAS but lacking MAS."""
    fit_type = record["fit_type"]
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_fit_type_cell(fit_type)),
        ),
        {"data-subtype": fit_type},
    )


def _misc_case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_case_subtype_cell(record["subtype"])),
        )
    )


def _lacks_mas_subtype_filter(case_count: int) -> object:
    """The unified lacks-MAS table's subtype filter."""
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in (("all", "All subtypes"), *_LACKS_MAS_FILTER_OPTIONS)
    )
    return mb_html.raw_html(
        f'<p><label for="{_LACKS_MAS_SUBTYPE_FILTER_ID}">Show </label>'
        f'<select id="{_LACKS_MAS_SUBTYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_LACKS_MAS_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _not_fit_for_mas_type_filter(case_count: int) -> object:
    """The not-fit-for-MAS table's (sub)type filter."""
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in _NOT_FIT_FILTER_OPTIONS
    )
    return mb_html.raw_html(
        f'<p><label for="{_NOT_FIT_TYPE_FILTER_ID}">Show </label>'
        f'<select id="{_NOT_FIT_TYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_NOT_FIT_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _back_to_fit_for_mas_table() -> object:
    """A standard return link for the unified Fit-for-MAS case page."""
    return mb_html.para(
        (
            "← Back to ",
            mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
            " and the ",
            mb_html.anchor_h(
                f"{author.dquote('fit for MAS')} table",
                f"{_FNAME}#{_FIT_FOR_MAS_SECTION_ID}",
            ),
            ".",
        )
    )


def build_lacks_mas_body(survey: dict) -> list:
    """Every chanted-word pair fit for MAS but lacking MAS, filterable by subtype."""
    records = _lacks_mas_records(survey)
    return [
        mb_html.heading_level_1(_visible_title(_LACKS_MAS_TITLE)),
        _hebrew_spacing_option(),
        _back_to_fit_for_mas_table(),
        mb_html.heading_level_2("Every case fit for MAS that lacks MAS"),
        _para(f"The table lists all {len(records):,} cases fit for MAS that lack MAS."),
        _lacks_mas_subtype_filter(len(records)),
        _table(
            ("Verse", "Word", "Subtype"),
            [_lacks_mas_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _LACKS_MAS_TABLE_ID,
            },
        ),
        mb_html.raw_html(_LACKS_MAS_FILTER_SCRIPT),
    ]


def _not_fit_for_mas_criterion_cell(meets_criterion: bool, criterion: str) -> object:
    """A blank cell for a met criterion or a column-specific red-cross gloss."""
    return (
        ""
        if meets_criterion
        else mb_html.span(
            _RED_X,
            {
                "class": _NOT_FIT_FAILURE_CLASS,
                "title": f"does not meet: {criterion}",
            },
        )
    )


def _not_fit_for_mas_type_codes(record: dict) -> tuple[str, ...]:
    """Every (sub)type that makes one not-fit-for-MAS chanted word selectable."""
    structural_types = record["types"]
    codes = []
    if psm.TYPE_OPEN in structural_types:
        codes.extend(("1", _TYPE_1_SUBTYPE_CODES[record["type_1_subtype"]]))
    if psm.TYPE_GUTTURAL in structural_types:
        codes.extend(
            (
                "2",
                _TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP[_type_2_filter_group(record)],
            )
        )
    if psm.TYPE_CLOSED_TSERE in structural_types:
        codes.append("3")
    if not codes:
        codes.append("other")
    assert set(structural_types) <= set(_TYPE_CODES), record
    return tuple(codes)


def _not_fit_for_mas_case_row(record: dict) -> object:
    """One MAS chanted word, with a result for each Fit-for-MAS criterion."""
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_first_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[0],
                ),
                {"class": "centered"},
            ),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_second_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[1],
                ),
                {"class": "centered"},
            ),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_third_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[2],
                ),
                {"class": "centered"},
            ),
        ),
        {"data-type-codes": " ".join(_not_fit_for_mas_type_codes(record))},
    )


def build_not_fit_body(survey: dict) -> list:
    """Every MAS chanted word that is not fit for MAS, with each failed criterion marked."""
    records = _not_fit_for_mas_records(survey)
    criterion_headers = tuple(
        mb_html.abbr(str(number), {"title": criterion})
        for number, criterion in enumerate(_FIT_FOR_MAS_CRITERIA, start=1)
    )
    return [
        mb_html.heading_level_1(_visible_title(_NOT_FIT_TITLE)),
        _hebrew_spacing_option(),
        _back_to_fit_for_mas_table(),
        mb_html.heading_level_2("Every MAS case not fit for MAS"),
        _para(
            f"The table lists all {len(records):,} MAS cases that are not fit for MAS."
        ),
        _para(
            f"The columns headed 1–3 correspond to the three {author.dquote('fit for MAS')}"
            " criteria. A red"
            f" {_RED_X} marks each criterion that a word does not meet; blank cells mark"
            " criteria that the word meets."
        ),
        _not_fit_for_mas_type_filter(len(records)),
        _table(
            ("Verse", "Word", *criterion_headers),
            [_not_fit_for_mas_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _NOT_FIT_TABLE_ID,
            },
        ),
        mb_html.raw_html(_NOT_FIT_FILTER_SCRIPT),
    ]


def build_misc_body(survey: dict) -> list:
    """The misc cases and the named subsets that remain outside types 1–3."""
    records = _misc_records(survey)
    unnamed_misc = [record for record in records if record["subtype"] is None]
    assert len(unnamed_misc) == 2, unnamed_misc
    misc_almost_type_3_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3)
    misc_almost_type_3_only_member = _misc_almost_type_3_only_member(survey)
    vayomer_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_VAYOMER)
    return [
        mb_html.heading_level_1(_visible_title(_MISC_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
                " or the ",
                mb_html.anchor_h(
                    f"{len(survey['post_stress']):,} individual cases", _CASES_FNAME
                ),
                ".",
            )
        ),
        mb_html.heading_level_2("Every misc case in MAM"),
        _para(
            "Each word in the table has MAS but does not meet the definition of"
            " types 1, 2, or 3."
        ),
        _table(
            ("Verse", "Word", "Subtype"),
            [_misc_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _MISC_TABLE_ID,
            },
        ),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_3,
                f" has {_spelled(misc_almost_type_3_count)} word",
                "s" if misc_almost_type_3_count != 1 else "",
                ", at ",
                _ref_link(misc_almost_type_3_only_member["bcv"]),
                ": ",
                *_case_chanted_word_cell(misc_almost_type_3_only_member),
                ", whose MAS syllable is final and closed with ",
                _ROM_HOLAM,
                ", a long vowel. That syllable fits ",
                cos(),
                "'s long-vowel type (a), but not our type 3, which is restricted to ",
                _ROM_TSERE,
                ".",
            )
        ),
        mb_html.para(
            (
                "Within misc, misc-",
                _ROM_VAYOMER,
                f" has {_spelled(vayomer_count)} word",
                "s" if vayomer_count != 1 else "",
                ". Each has a ",
                _ROM_PASEQ,
                " between the MAS word and the next word. This is the ",
                _ROM_GAYA,
                "-before-",
                _ROM_PASEQ,
                " pattern described in ",
                itm(),
                " ",
                *itm_sections("§325"),
                ".",
            )
        ),
        mb_html.para(
            (
                "The remaining ",
                _spelled(len(unnamed_misc)),
                " misc cases, at ",
                _ref_link(unnamed_misc[0]["bcv"]),
                " and ",
                _ref_link(unnamed_misc[1]["bcv"]),
                ", belong to no named subset. There is not much to say about them beyond their having MAS without meeting the definition of type 1, 2, or 3.",
            )
        ),
    ]


def build_cases_body(survey: dict) -> list:
    """The individual cases, outside the main page's explanatory sections."""
    headers = ("Verse", "Word", "Type", "Subtype")
    rows = [_case_row(record) for record in survey["post_stress"]]
    return [
        mb_html.heading_level_1(_visible_title(_CASES_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            ("← Back to ", mb_html.anchor_h(_visible_title(_TITLE), _FNAME), ".")
        ),
        mb_html.heading_level_2("Every MAS in MAM"),
        _case_type_filter(len(rows)),
        _table(
            headers,
            rows,
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _CASE_TABLE_ID,
            },
        ),
        mb_html.raw_html(_CASE_FILTER_SCRIPT),
    ]


def _letters_of(word: str) -> tuple[str, ...]:
    """The base letters of each atom of a chanted word, as a tuple, one string per atom.

    The house pattern for finding a form without retyping its accents: search by letters,
    render what the corpus has.  ``maqaf_nonfinal_accents_page._find_span`` is the other
    instance.
    """
    atoms = word.replace(psm.MAQAF, " ").split(" ")
    return tuple(
        "".join(char for char in atom if "א" <= char <= "ת") for atom in atoms if atom
    )


def _focus_word(
    survey: dict, bcv: str, letters: tuple[str, ...], *, must_have: str = ""
) -> str:
    """The one chanted word of a focus verse whose atoms have these letters.

    A focus verse is one the page names outside its tables, and the survey records its
    chanted words as MAM has them today.  Searching by letters is what keeps the accents
    lifted from the corpus rather than typed here, and the exactly-one assertion is what
    makes the search a check rather than a guess.

    ``must_have`` narrows a verse that has the same letters twice: 1 Samuel 17:5 has נחשת
    both in the middle and at the end, and it is the verse-final one -- the one with sof
    pasuq -- that the post-silluq section is about.
    """
    return _source_focus_word(
        survey["currency"]["focus_verses"][bcv]["chanted_words"],
        bcv,
        letters,
        must_have=must_have,
        source="MAM",
    )


def _source_focus_word(
    words: list[str],
    bcv: str,
    letters: tuple[str, ...],
    *,
    must_have: str,
    source: str,
) -> str:
    """The one source form at a page-named verse that has these letters and mark."""
    hits = [
        word for word in words if _letters_of(word) == letters and must_have in word
    ]
    assert (
        len(hits) == 1
    ), f"{source} {bcv}: {len(hits)} chanted words with letters {letters} and {must_have!r}"
    return hits[0]


def _uxlc_words(bcv: str) -> list[str]:
    """The UXLC atoms at one verse, lifted from its vendored XML source."""
    bb, chnu, vrnu = _split(bcv)
    bk39id = wlc_bb_to_bk39id(bb)
    xml_name = f"{my_uxlc._UXLC_BOOK_FILE_NAMES[bk39id]}.xml"
    xml_path = paths.in_dir() / "UXLC-39" / xml_name
    root = ET.parse(xml_path).getroot()
    chapters = [node for node in root.iter("c") if node.attrib.get("n") == str(chnu)]
    assert len(chapters) == 1, f"{xml_path}: {len(chapters)} chapter {chnu} elements"
    verses = [
        node
        for node in chapters[0]
        if node.tag == "v" and node.attrib.get("n") == str(vrnu)
    ]
    assert len(verses) == 1, f"{xml_path}: {len(verses)} verse {chnu}:{vrnu} elements"
    return [
        atom.text.strip()
        for atom in verses[0]
        if atom.tag in {"w", "q"} and atom.text is not None
    ]


def _wlc_words(bcv: str) -> list[str]:
    """The WLC 4.22 atoms at one verse, decoded from its vendored M-C source."""
    assert bcv.startswith("1s"), bcv
    json_path = paths.out_dir() / "wlc422" / "1verses_03_jsju1s.json"
    rows = json.loads(json_path.read_text(encoding="utf-8"))
    assert isinstance(rows, list), f"Expected a list in {json_path}"
    rows_at_verse = [
        row for row in rows if isinstance(row, dict) and row.get("bcv") == bcv
    ]
    assert len(rows_at_verse) == 1, f"WLC 4.22: {len(rows_at_verse)} rows for {bcv}"
    vels = rows_at_verse[0].get("vels")
    assert isinstance(vels, list) and all(
        isinstance(atom, str) for atom in vels
    ), f"WLC 4.22 {bcv}: non-string vels"
    return [wlc_uword.uword(atom) for atom in vels]


def _require_exact_keys(
    record: dict, *, required: set[str], allowed: set[str], where: str
) -> None:
    """Reject missing and unknown keys in one authored JSON object."""
    missing = sorted(required - set(record))
    unknown = sorted(set(record) - allowed)
    if missing or unknown:
        raise ValueError(f"{where}: missing keys {missing}; unknown keys {unknown}")


def _require_nonempty_string(value: object, *, where: str) -> str:
    """Return one nonempty authored string, or fail with its JSON location."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where}: expected a nonempty string")
    return value


def _full_ref_to_bcv(ref: str) -> str:
    """Convert the tracked full-English reference to the survey's compact BCV."""
    match = _FULL_REF.fullmatch(ref)
    if match is None:
        raise ValueError(f"Malformed reference: {ref!r}")
    english_to_bb = {}
    for bb in wlc_bb_codes():
        parts = uxlc_source.book_basename(wlc_bb_to_bk39id(bb)).split("_")
        english_name = (
            f"{parts[-1]} {' '.join(parts[:-1])}"
            if parts[-1] in {"1", "2"}
            else " ".join(parts)
        )
        english_to_bb[english_name] = bb
    try:
        bb = english_to_bb[match["book"]]
    except KeyError as exc:
        raise ValueError(f"Unknown book in reference: {ref!r}") from exc
    return f"{bb}{int(match['chapter'])}:{int(match['verse'])}"


def _validate_iso_date(value: object, *, where: str) -> str:
    """Validate one historical observation date without generating a clock date."""
    text = _require_nonempty_string(value, where=where)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{where}: expected an ISO date, got {text!r}") from exc
    if parsed.isoformat() != text:
        raise ValueError(f"{where}: date is not canonical ISO form: {text!r}")
    return text


def _validate_string_list(
    value: object, *, where: str, allow_empty: bool = False
) -> list[str]:
    """Validate a duplicate-free list of nonempty strings."""
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ValueError(
            f"{where}: expected a {'possibly empty' if allow_empty else 'nonempty'} list"
        )
    strings = [
        _require_nonempty_string(item, where=f"{where}[{index}]")
        for index, item in enumerate(value)
    ]
    if len(strings) != len(set(strings)):
        raise ValueError(f"{where}: duplicate entries")
    return strings


def load_post_silluq_cases() -> list[dict]:
    """Load and validate the curated cross-source case ledger."""
    path = paths.in_dir() / _POST_SILLUQ_CASES_JSON
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a root object")
    _require_exact_keys(
        payload,
        required={"about", "cases"},
        allowed={"about", "cases"},
        where=str(path),
    )
    _require_nonempty_string(payload["about"], where=f"{path}#about")
    cases = payload["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"{path}#cases: expected a nonempty list")

    seen_refs: set[str] = set()
    seen_bcvs: set[str] = set()
    for index, case in enumerate(cases):
        where = f"{path}#cases/{index}"
        if not isinstance(case, dict):
            raise ValueError(f"{where}: expected an object")
        required = {"ref", "bcv", "status", "form_source", "reports", "images"}
        allowed = required | {"sources", "additional_sources", "transcriptions"}
        _require_exact_keys(case, required=required, allowed=allowed, where=where)

        ref = _require_nonempty_string(case["ref"], where=f"{where}/ref")
        bcv = _require_nonempty_string(case["bcv"], where=f"{where}/bcv")
        if _full_ref_to_bcv(ref) != bcv:
            raise ValueError(f"{where}: ref {ref!r} does not match bcv {bcv!r}")
        if ref in seen_refs or bcv in seen_bcvs:
            raise ValueError(f"{where}: duplicate reference {ref!r} or bcv {bcv!r}")
        seen_refs.add(ref)
        seen_bcvs.add(bcv)

        status = case["status"]
        if status not in _POST_SILLUQ_CASE_STATUSES:
            raise ValueError(f"{where}/status: unknown status {status!r}")
        if case["form_source"] not in _POST_SILLUQ_FORM_SOURCES:
            raise ValueError(
                f"{where}/form_source: unknown source {case['form_source']!r}"
            )

        reports = _validate_string_list(case["reports"], where=f"{where}/reports")
        for report in reports:
            report_path = Path(report)
            if (
                report_path.is_absolute()
                or "\\" in report
                or not report.startswith("doc/")
                or not (paths.repo_root() / report_path).is_file()
            ):
                raise ValueError(f"{where}/reports: invalid report path {report!r}")

        images = _validate_string_list(
            case["images"], where=f"{where}/images", allow_empty=True
        )
        unknown_images = sorted(set(images) - _POST_SILLUQ_IMAGE_IDS)
        if unknown_images:
            raise ValueError(f"{where}/images: unknown identifiers {unknown_images}")
        mismatched_images = [
            image_id for image_id in images if _POST_SILLUQ_IMAGE_REFS[image_id] != ref
        ]
        if mismatched_images:
            raise ValueError(
                f"{where}/images: identifiers belong to another reference: "
                f"{mismatched_images}"
            )

        if status == "open-candidate":
            if "sources" in case or "additional_sources" in case:
                raise ValueError(
                    f"{where}: open candidates do not take source conclusions"
                )
            _validate_string_list(
                case.get("transcriptions"), where=f"{where}/transcriptions"
            )
        else:
            if "transcriptions" in case or "sources" not in case:
                raise ValueError(
                    f"{where}: known cases require sources, not transcriptions"
                )
            sources = case["sources"]
            if not isinstance(sources, dict) or set(sources) != set(
                _POST_SILLUQ_SOURCES
            ):
                raise ValueError(
                    f"{where}/sources: expected exactly {_POST_SILLUQ_SOURCES}"
                )
            for source, state in sources.items():
                if state not in _POST_SILLUQ_SOURCE_STATES:
                    raise ValueError(
                        f"{where}/sources/{source}: unknown state {state!r}"
                    )
            additions = case.get("additional_sources", [])
            if not isinstance(additions, list):
                raise ValueError(f"{where}/additional_sources: expected a list")
            addition_names: set[str] = set()
            for add_index, addition in enumerate(additions):
                add_where = f"{where}/additional_sources/{add_index}"
                if not isinstance(addition, dict):
                    raise ValueError(f"{add_where}: expected an object")
                _require_exact_keys(
                    addition,
                    required={"source", "state"},
                    allowed={"source", "state"},
                    where=add_where,
                )
                source = _require_nonempty_string(
                    addition["source"], where=f"{add_where}/source"
                )
                if source in addition_names:
                    raise ValueError(f"{add_where}: duplicate source {source!r}")
                addition_names.add(source)
                if addition["state"] not in _POST_SILLUQ_SOURCE_STATES:
                    raise ValueError(
                        f"{add_where}/state: unknown state {addition['state']!r}"
                    )
    return cases


def load_post_silluq_koren_observations() -> list[dict]:
    """Load Koren observations, preserving incomplete states as non-results.

    Missing ``status`` is the backward-compatible spelling of ``complete``. A completed
    observation has a closed ``koren`` classification; an incomplete, deferred or skipped
    observation must not have one. Additional marks and notes remain separate from that
    classification.
    """
    path = paths.in_dir() / _POST_SILLUQ_KOREN_JSON
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a root object")
    _require_exact_keys(
        payload,
        required={"about", "readings"},
        allowed={"about", "readings"},
        where=str(path),
    )
    _require_nonempty_string(payload["about"], where=f"{path}#about")
    readings = payload["readings"]
    if not isinstance(readings, list) or not readings:
        raise ValueError(f"{path}#readings: expected a nonempty list")

    normalized = []
    seen_refs: set[str] = set()
    seen_bcvs: set[str] = set()
    allowed = {
        "ref",
        "bcv",
        "status",
        "koren",
        "sheva",
        "additional_marks",
        "note",
        "date",
    }
    for index, raw in enumerate(readings):
        where = f"{path}#readings/{index}"
        if not isinstance(raw, dict):
            raise ValueError(f"{where}: expected an object")
        _require_exact_keys(
            raw,
            required={"ref", "date"},
            allowed=allowed,
            where=where,
        )
        ref = _require_nonempty_string(raw["ref"], where=f"{where}/ref")
        bcv = _full_ref_to_bcv(ref)
        if "bcv" in raw and raw["bcv"] != bcv:
            raise ValueError(f"{where}/bcv: does not match {ref!r}")
        if ref in seen_refs or bcv in seen_bcvs:
            raise ValueError(f"{where}: duplicate reference {ref!r}")
        seen_refs.add(ref)
        seen_bcvs.add(bcv)

        status = raw.get("status", "complete")
        if status not in _KOREN_STATUSES:
            raise ValueError(f"{where}/status: unknown status {status!r}")
        if status == "complete":
            if raw.get("koren") not in _KOREN_POSITIONS:
                raise ValueError(
                    f"{where}/koren: completed observation needs a position"
                )
        elif "koren" in raw:
            raise ValueError(
                f"{where}/koren: non-complete observation cannot be classified"
            )

        if "sheva" in raw and raw["sheva"] not in _KOREN_SHEVA_STATES:
            raise ValueError(f"{where}/sheva: unknown state {raw['sheva']!r}")
        if "additional_marks" in raw:
            _validate_string_list(
                raw["additional_marks"], where=f"{where}/additional_marks"
            )
        if "note" in raw:
            _require_nonempty_string(raw["note"], where=f"{where}/note")
        _validate_iso_date(raw["date"], where=f"{where}/date")
        normalized.append({**raw, "bcv": bcv, "status": status})
    return normalized


def _verse_final_word(words: list[str], *, bcv: str, source: str) -> str:
    """Locate one verse-final source form without placing pointed Hebrew in the ledger."""
    hits = [word for word in words if psm.SOF_PASUQ in word]
    if len(hits) != 1:
        raise ValueError(
            f"{source} {bcv}: expected one verse-final word, found {len(hits)}"
        )
    return hits[0]


def _mam_final_forms(bcvs: set[str]) -> dict[str, str]:
    """Lift each requested verse-final form from the tracked MAM-simple product."""
    refs_by_book: dict[str, set[tuple[int, int]]] = {}
    for bcv in bcvs:
        bb, chnu, vrnu = _split(bcv)
        refs_by_book.setdefault(bb, set()).add((chnu, vrnu))
    loaded = mam_simple_verse.load_mam_simple_for_refs(
        paths.require_mam_simple_dir(), refs_by_book
    )
    missing = sorted(bcvs - set(loaded))
    if missing:
        raise ValueError(f"MAM-simple lacks requested references: {missing}")
    return {
        bcv: _verse_final_word(
            [
                word
                for word in payload["mam_simple_verse"]["vels"]
                if isinstance(word, str)
            ],
            bcv=bcv,
            source="MAM-simple",
        )
        for bcv, payload in loaded.items()
    }


def _case_forms(cases: list[dict], mam_forms: dict[str, str]) -> dict[str, str]:
    """Lift each case form from the ledger-declared tracked corpus."""
    forms = {}
    for case in cases:
        bcv = case["bcv"]
        if case["form_source"] == "mam":
            forms[bcv] = mam_forms[bcv]
        elif case["form_source"] == "uxlc":
            forms[bcv] = _verse_final_word(_uxlc_words(bcv), bcv=bcv, source="UXLC 3.9")
        else:  # closed validation above makes this unreachable
            raise ValueError(f"Unknown case form source: {case['form_source']!r}")
    return forms


def _post_silluq_comparison(survey: dict) -> tuple[tuple[str, str], ...]:
    """The MAM and BHS forms relevant to 1 Samuel 17:5's post-silluq question.

    The row labelled "BHS" is UXLC 3.9's form, asserted equal to WLC 4.22's; no BHS
    text is read here. The page's claim that BHS has the form rests on Ben's reading of
    the printed BHS on 2026-09-09, which confirms the two marks, meteg after silluq.
    Ben's decision, the same day: the page's wording stands and takes no "checked"
    clause; this docstring and the review records are where the reading is recorded
    (doc/review-findings-2026-09-08.md, finding 3 and its State line).
    """
    letters = ("נחשת",)
    bhs_form_from_uxlc = _source_focus_word(
        _uxlc_words(_POST_SILLUQ_VERSE),
        _POST_SILLUQ_VERSE,
        letters,
        must_have=psm.SOF_PASUQ,
        source="UXLC 3.9",
    )
    bhs_form_from_wlc = _source_focus_word(
        _wlc_words(_POST_SILLUQ_VERSE),
        _POST_SILLUQ_VERSE,
        letters,
        must_have=psm.SOF_PASUQ,
        source="WLC 4.22",
    )
    assert (
        bhs_form_from_uxlc == bhs_form_from_wlc
    ), "the two BHS-derived transcriptions differ at 1 Samuel 17:5"
    return (
        (
            "MAM",
            _focus_word(survey, _POST_SILLUQ_VERSE, letters, must_have=psm.SOF_PASUQ),
        ),
        ("BHS", bhs_form_from_uxlc),
    )


def _mam_post_silluq_form(survey: dict) -> str:
    """MAM's verse-final form at 1 Kings 7:37, lifted from the survey."""
    return _focus_word(
        survey,
        _MAM_POST_SILLUQ_VERSE,
        ("לכלהנה",),
        must_have=psm.SOF_PASUQ,
    )


def _mam_post_silluq_statement(survey: dict, *, starts_sentence: bool = True) -> tuple:
    """The 1 Kings 7:37 MAM case, and what "ignore" means there.

    The definition is Ben's wording of 2026-09-09: the research deliberately reads the
    word as meteg-then-silluq, which is what the survey's stress oracle does, so the
    word counts as MBS_O and ``post_silluq.in_mam`` stays 0.
    """
    return (
        "At " if starts_sentence else "at ",
        _ref_link(_MAM_POST_SILLUQ_VERSE),
        ", in MAM, there is a ",
        _ROM_METEG,
        " after ",
        _ROM_SILLUQ,
        " in ",
        wrap_hebrew_runs(_mam_post_silluq_form(survey)),
        ". We ignore it for the purposes of this research. ",
        author.dquote("Ignore"),
        " means treat this word as a ",
        _ROM_METEG,
        "-then-",
        _ROM_SILLUQ,
        " word, i.e. deliberately misinterpret the marks. How we treat this mark has"
        " little effect on our census and no effect on the bulk of the results of this"
        " research, since they concern ",
        _ROM_METEG,
        " immediately after a conjunctive on the primary stress of the word.",
    )


def _mam_post_silluq_aleppo_crop() -> object:
    """The Aleppo Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_MAM_POST_SILLUQ_REF};'
        ' it has a meteg after the silluq."'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, {_MAM_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _mam_post_silluq_leningrad_crop() -> object:
    """The Leningrad Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_MAM_POST_SILLUQ_REF};'
        ' it lacks a meteg after the silluq."'
        ' loading="lazy" style="width: 300px; max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, {_MAM_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _post_silluq_lc_crop() -> object:
    """The directly inspectable LC line for 1 Samuel 17:5's post-silluq question."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_POST_SILLUQ_LC_CROP_URL}"'
        f' alt="Leningrad Codex, F159A, column 3, line 8: {_POST_SILLUQ_REF}."'
        ' loading="lazy"></a><figcaption>Leningrad Codex, F159A, column 3, line 8'
        f" ({_POST_SILLUQ_REF}); crop attached to "
        f'<a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">phonetic-hbo #78</a>.</figcaption></figure>'
    )


def _post_silluq_aleppo_crop() -> object:
    """The Aleppo crop showing no meteg after the silluq in 1 Samuel 17:5."""
    return mb_html.raw_html(
        f'<figure><img src="{_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word in {_POST_SILLUQ_REF}; it has'
        ' no meteg after the silluq." loading="lazy">'
        f"<figcaption>Aleppo Codex, {_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _post_silluq_table_row(contents: tuple, attrs: tuple) -> object:
    """Build one row without the shared helper's silent ``zip`` truncation."""
    if len(contents) != len(attrs):
        raise ValueError(
            f"post-silluq table row has {len(contents)} cells and {len(attrs)} attributes"
        )
    return mb_html.table_row_of_data(contents, attrs)


def _post_silluq_source_state(state: str) -> object:
    """The visible, exhaustive source-state dispatch."""
    if state == "later-meteg":
        return ("later ", _ROM_METEG)
    if state == "no-later-mark":
        return "no later mark"
    if state == "both-strokes":
        return "both strokes"
    if state == "first-position-only":
        return "first position only"
    if state == "not-recorded":
        return "not recorded"
    if state == "tracked-observation":
        raise ValueError("tracked-observation needs the Koren observation dispatch")
    raise ValueError(f"Unknown post-silluq source state: {state!r}")


def _koren_position_label(position: str) -> str:
    """The visible, exhaustive Koren two-position classification."""
    labels = {
        "first": "first position only",
        "last": "last position only",
        "both": "both positions",
    }
    try:
        return labels[position]
    except KeyError as exc:
        raise ValueError(f"Unknown Koren position: {position!r}") from exc


def _complete_koren_by_ref(observations: list[dict]) -> dict[str, dict]:
    """Index only completed observations for case-register joins."""
    return {
        observation["ref"]: observation
        for observation in observations
        if observation["status"] == "complete"
    }


def _case_source_cell(
    case: dict, source: str, complete_koren_by_ref: dict[str, dict]
) -> object:
    """One source cell, joining Koren only when the case ledger requests it."""
    state = case["sources"][source]
    if state != "tracked-observation":
        return _post_silluq_source_state(state)
    if source != "koren":
        raise ValueError(f"{case['ref']}: tracked observation assigned to {source}")
    observation = complete_koren_by_ref.get(case["ref"])
    if observation is None:
        raise ValueError(f"{case['ref']}: missing completed Koren observation")
    return _koren_position_label(observation["koren"])


def _case_last_metsil_positions(
    case: dict, complete_koren_by_ref: dict[str, dict]
) -> set[str]:
    """Derive whether each recorded source's last metsil is first or last.

    ``first`` and ``last`` name the two U+05BD positions under comparison, not a
    grammatical identification of either mark.
    """
    positions = set()
    source_states = list(case["sources"].items()) + [
        (addition["source"], addition["state"])
        for addition in case.get("additional_sources", [])
    ]
    for source, state in source_states:
        if state in {"later-meteg", "both-strokes"}:
            positions.add("last")
        elif state in {"no-later-mark", "first-position-only"}:
            positions.add("first")
        elif state == "not-recorded":
            continue
        elif state == "tracked-observation" and source == "koren":
            observation = complete_koren_by_ref.get(case["ref"])
            if observation is None:
                raise ValueError(f"{case['ref']}: missing completed Koren observation")
            positions.add("first" if observation["koren"] == "first" else "last")
        else:
            raise ValueError(
                f"{case['ref']}: cannot compare the last metsil for {source}: {state!r}"
            )
    return positions


def _post_silluq_case_register(
    cases: list[dict], forms: dict[str, str], observations: list[dict]
) -> list:
    """The cross-source position contrasts, with source distinctions visible."""
    known = [case for case in cases if case["status"] == "last-metsil-contrast"]
    complete_koren_by_ref = _complete_koren_by_ref(observations)
    for case in known:
        if _case_last_metsil_positions(case, complete_koren_by_ref) != {
            "first",
            "last",
        }:
            raise ValueError(
                f"{case['ref']}: sources do not establish a last-metsil position contrast"
            )
    headers = (
        "Form",
        "Reference",
        "MAM",
        "Aleppo Codex",
        "Leningrad Codex",
        "Koren",
    )
    attrs = (
        _HEBREW_CELL,
        _POST_SILLUQ_BCV_CELL,
        None,
        None,
        None,
        None,
    )
    rows = [
        _post_silluq_table_row(
            (
                _hebrew_cell(forms[case["bcv"]]),
                _ref_link(case["bcv"]),
                *(
                    _case_source_cell(case, source, complete_koren_by_ref)
                    for source in _POST_SILLUQ_SOURCES
                ),
            ),
            attrs,
        )
        for case in known
    ]
    return [
        mb_html.heading_level_2("Case register"),
        mb_html.para(
            (
                "Each case below has at least one source—a manuscript or printed edition—"
                "whose last ",
                _ROM_METSIL,
                " (a neutral name here for a U+05BD that may be ",
                _ROM_METEG,
                " or ",
                _ROM_SILLUQ,
                ") is later than the last ",
                _ROM_METSIL,
                " in at least one other source.",
            )
        ),
        _table(
            headers,
            rows,
            {"class": "post-stress-meteg-table post-silluq-register"},
        ),
    ]


def _post_silluq_additional_sources(cases: list[dict]) -> list:
    """Curated observations outside the four main source columns."""
    cases_with_additions = [case for case in cases if case.get("additional_sources")]
    if not cases_with_additions:
        return []
    contents = [mb_html.heading_level_2("Additional source observations")]
    for case in cases_with_additions:
        contents.extend(
            (
                mb_html.heading_level_3(_ref_link(case["bcv"])),
                mb_html.unordered_list(
                    tuple(
                        (
                            addition["source"],
                            ": ",
                            _post_silluq_source_state(addition["state"]),
                            ".",
                        )
                        for addition in case["additional_sources"]
                    )
                ),
            )
        )
    return contents


def _post_silluq_image_nodes(image_id: str) -> list:
    """The fixed claim and existing deployed figure for one known image identifier."""
    if image_id == "lc-1s17-5":
        return [
            mb_html.para(
                (
                    "The Leningrad Codex has a ",
                    _ROM_METEG,
                    " after its ",
                    _ROM_SILLUQ,
                    f" at {_POST_SILLUQ_REF}.",
                )
            ),
            _post_silluq_lc_crop(),
        ]
    if image_id == "aleppo-1s17-5":
        return [
            mb_html.para(
                (
                    "The Aleppo Codex lacks the later ",
                    _ROM_METEG,
                    f" at {_POST_SILLUQ_REF}.",
                )
            ),
            _post_silluq_aleppo_crop(),
        ]
    if image_id == "aleppo-1k7-37":
        return [
            mb_html.para(
                (
                    "The Aleppo Codex has a later ",
                    _ROM_METEG,
                    f" at {_MAM_POST_SILLUQ_REF}.",
                )
            ),
            _mam_post_silluq_aleppo_crop(),
        ]
    if image_id == "leningrad-1k7-37":
        return [
            mb_html.para(
                (
                    "The Leningrad Codex lacks the later ",
                    _ROM_METEG,
                    f" at {_MAM_POST_SILLUQ_REF}.",
                )
            ),
            _mam_post_silluq_leningrad_crop(),
        ]
    raise ValueError(f"Unknown post-silluq image identifier: {image_id!r}")


def _post_silluq_image_evidence(cases: list[dict]) -> list:
    """Reuse only the four already deployed manuscript crops."""
    with_images = [case for case in cases if case["images"]]
    if not with_images:
        return []
    contents = [mb_html.heading_level_2("Image evidence")]
    for case in with_images:
        contents.append(mb_html.heading_level_3(_ref_link(case["bcv"])))
        for image_id in case["images"]:
            contents.extend(_post_silluq_image_nodes(image_id))
    return contents


def _post_silluq_open_candidates(cases: list[dict], forms: dict[str, str]) -> list:
    """The transcription-derived cases awaiting a Leningrad Codex image reading."""
    open_cases = [case for case in cases if case["status"] == "open-candidate"]
    attrs = (_HEBREW_CELL, _POST_SILLUQ_BCV_CELL, None, None)
    rows = [
        _post_silluq_table_row(
            (
                _hebrew_cell(forms[case["bcv"]]),
                _ref_link(case["bcv"]),
                ", ".join(case["transcriptions"]),
                "unresolved",
            ),
            attrs,
        )
        for case in open_cases
    ]
    return [
        mb_html.heading_level_2("Unresolved Leningrad Codex candidates"),
        mb_html.para(
            (
                "The named transcriptions have a second U+05BD after MAM's ",
                _ROM_SILLUQ,
                ". A transcription is not a manuscript image; these rows remain open until"
                " the Leningrad Codex itself is read.",
            )
        ),
        _table(
            ("Form", "Reference", "Transcriptions", "Leningrad Codex"),
            rows,
            {"class": "post-stress-meteg-table post-silluq-register"},
        ),
    ]


def build_post_silluq_body(
    survey: dict, cases: list[dict], observations: list[dict]
) -> list:
    """The maintained page for cases and candidates of meteg after silluq."""
    mam_bcvs = {case["bcv"] for case in cases if case["form_source"] == "mam"}
    mam_forms = _mam_final_forms(mam_bcvs)
    forms = _case_forms(cases, mam_forms)
    return [
        mb_html.heading_level_1(_visible_title(_POST_SILLUQ_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(
                    _visible_title(_TITLE), f"{_FNAME}#{_POST_SILLUQ_FOOTNOTE_ID}"
                ),
                ".",
            )
        ),
        mb_html.para(
            (
                "The same Unicode code point, U+05BD, represents both ",
                _ROM_SILLUQ,
                " and ",
                _ROM_METEG,
                ". In a verse-final word, U+05BD on the stressed syllable is ",
                _ROM_SILLUQ,
                "; a later U+05BD is ",
                _ROM_METEG,
                " only when the stress has been established on an earlier syllable.",
            )
        ),
        *_post_silluq_case_register(cases, forms, observations),
        *_post_silluq_additional_sources(cases),
        *_post_silluq_image_evidence(cases),
        *_post_silluq_open_candidates(cases, forms),
    ]


def _post_silluq_footnote(survey: dict) -> list:
    """Footnote 1: the census treatment and a link to the maintained register."""
    return [
        mb_html.heading_level_3(
            ("φ1 — ", _ROM_METEG_CAP, " after ", _ROM_SILLUQ),
            {"id": _POST_SILLUQ_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "As noted on the ",
                mb_html.anchor_h("Methods", _METHODS_FNAME),
                " page, ",
                *_mam_post_silluq_statement(survey, starts_sentence=False),
            )
        ),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    ("maintained ", _ROM_METEG, "-after-", _ROM_SILLUQ, " register"),
                    _POST_SILLUQ_FNAME,
                ),
                " gives the known cases, evidence, and unresolved candidates.",
            )
        ),
    ]


def _chronicles_8_11_mam_compound(survey: dict) -> str:
    """MAM's three-atom compound at the site of 2 Chronicles 8:11's possible LC case."""
    words = survey["currency"]["focus_verses"][_CHRONICLES_8_11_VERSE]["chanted_words"]
    hits = [word for word in words if _letters_of(word) == ("אשר", "באה", "אליהם")]
    assert len(hits) == 1, hits
    return hits[0]


def _chronicles_8_11_crop(codex: str, image_url: str) -> object:
    """One supplied manuscript crop, kept at a readable width on every screen."""
    return mb_html.raw_html(
        f'<figure><img src="{image_url}"'
        f' alt="{codex} crop of {_CHRONICLES_8_11_REF}."'
        ' loading="lazy" style="max-width: 100%; height: auto;"><figcaption>'
        f"{codex}, {_CHRONICLES_8_11_REF}.</figcaption></figure>"
    )


def _chronicles_8_11_leningrad_label(label: str) -> object:
    """One short table label, with the complete Leningrad interpretation on hover."""
    return mb_html.abbr(label, {"title": _CHRONICLES_8_11_LENINGRAD_GLOSSES[label]})


def _chronicles_8_11_meteg_position_label(label: str) -> object:
    """The MBS or MAS classification of one 2 Chronicles 8:11 interpretation."""
    titles = {
        "MBS": "meteg before the stress",
        "MAS": "meteg after the stress",
    }
    return mb_html.abbr(label, {"title": titles[label]})


def build_chronicles_8_11_body(survey: dict) -> list:
    """The manuscript evidence behind the possible extra MAS case in 2 Chronicles 8:11."""
    mam_compound = _chronicles_8_11_mam_compound(survey)
    return [
        mb_html.heading_level_1(_visible_title(_CHRONICLES_8_11_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(
                    _visible_title(_TITLE), f"{_FNAME}#{_JEREMIAH_FOOTNOTE_ID}"
                ),
                ".",
            )
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(_CHRONICLES_8_11_VERSE),
                ", in the Leningrad Codex, the word after a MAS lacks initial stress, at least"
                " according to one interpretation of the ambiguous ",
                _ROM_METEG_MERKHA,
                " marks in the manuscript.",
            )
        ),
        mb_html.table(
            [
                mb_html.table_row_of_data(
                    (
                        "MAM",
                        _chronicles_8_11_meteg_position_label("MBS"),
                        _hebrew_cell(mam_compound),
                    ),
                    (None, None, _HEBREW_CELL),
                ),
                mb_html.table_row_of_data(
                    (
                        _chronicles_8_11_leningrad_label("L-1"),
                        _chronicles_8_11_meteg_position_label("MAS"),
                        _paired_chanted_word_cell(
                            _CHRONICLES_8_11_L1,
                            _CHRONICLES_8_11_LENINGRAD_NEXT_WORD,
                        ),
                    ),
                    (None, None, _HEBREW_CELL),
                ),
                mb_html.table_row_of_data(
                    (
                        _chronicles_8_11_leningrad_label("L-2"),
                        _chronicles_8_11_meteg_position_label("MBS"),
                        _paired_chanted_word_cell(
                            _CHRONICLES_8_11_L2,
                            _CHRONICLES_8_11_LENINGRAD_NEXT_WORD,
                        ),
                    ),
                    (None, None, _HEBREW_CELL),
                ),
            ],
            {"class": "limited-width post-stress-meteg-table"},
        ),
        mb_html.para(
            "The following table gives each Leningrad interpretation's MBS/MAS"
            " classification and lists the printed editions that have that Leningrad"
            " interpretation."
        ),
        mb_html.table(
            [
                mb_html.table_row_of_data(
                    (
                        _chronicles_8_11_leningrad_label("L-1"),
                        _chronicles_8_11_meteg_position_label("MAS"),
                        "Breuer (Da-at Miqra), Dotan (BHL)",
                    )
                ),
                mb_html.table_row_of_data(
                    (
                        _chronicles_8_11_leningrad_label("L-2"),
                        _chronicles_8_11_meteg_position_label("MBS"),
                        "BHS",
                    )
                ),
            ],
            {"class": "limited-width post-stress-meteg-table"},
        ),
        mb_html.heading_level_2(f"Manuscript crops of {_CHRONICLES_8_11_REF}"),
        _chronicles_8_11_crop("Aleppo Codex", _CHRONICLES_8_11_ALEPPO_CROP_URL),
        _chronicles_8_11_crop("Leningrad Codex", _CHRONICLES_8_11_LENINGRAD_CROP_URL),
    ]


def _oleh_meteg_overlap(survey: dict) -> list:
    """The meteg marks that share oleh's letter."""
    oleh_overlaps = [
        record
        for record in survey["diagnostics"][
            "sharing_a_letter_with_a_non_stress_marking_accent"
        ]
        if "ole" in record["shares_its_letter_with"]
    ]
    assert oleh_overlaps
    position_by_syllables_after_stress = {
        -1: mb_html.abbr("MBS", {"title": "meteg before the stress"}),
        1: mb_html.abbr("MAS", {"title": "meteg after the stress"}),
    }
    assert {
        record["syllables_after_the_stress"] for record in oleh_overlaps
    } <= position_by_syllables_after_stress.keys()
    oleh_overlaps.sort(key=lambda record: record["syllables_after_the_stress"])
    rows = [
        mb_html.table_row_of_data(
            (
                _ref_link(record["bcv"]),
                _oleh_chanted_word_cell(record),
                position_by_syllables_after_stress[
                    record["syllables_after_the_stress"]
                ],
            ),
            (None, _HEBREW_CELL, None),
        )
        for record in oleh_overlaps
    ]
    return [
        mb_html.heading_level_2((_ROM_METEG_CAP, " sharing a letter with ", _ROM_OLEH)),
        mb_html.para(
            (
                "In MAM, ",
                f"{len(oleh_overlaps)} ",
                _ROM_METEG,
                " marks share a letter with ",
                _ROM_OLEH,
                ". The table below labels each such ",
                _ROM_METEG,
                " as MBS or MAS.",
            )
        ),
        mb_html.table(rows, {"class": "limited-width post-stress-meteg-table"}),
        mb_html.para(
            (
                "We count each such ",
                _ROM_METEG,
                " as if the ",
                _ROM_OLEH,
                " were not there, because ",
                _ROM_OLEH,
                " is not an accent indicating stress, even when it is the last accent in"
                " the word, as it is in the MAS rows above. In other words, a MAS"
                " word whose ",
                _ROM_METEG,
                " shares a letter with ",
                _ROM_OLEH,
                " might at first look like some weird ",
                *author.dquote((_ROM_METEG, " on the stress")),
                " (neither before nor after), but it is not!",
            )
        ),
    ]


def _footnotes(survey: dict) -> list:
    """The exceptions and methods the page marks with its phi callouts."""
    exceptions = _noninitial_next_stress_records(survey)
    assert len(exceptions) == 1
    exception = exceptions[0]
    return [
        mb_html.heading_level_2("Footnotes"),
        *_post_silluq_footnote(survey),
        *_nonfinal_mas_syllable_footnote(survey),
        mb_html.heading_level_3(
            "φ3 — Next word lacking initial stress",
            {"id": _JEREMIAH_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(exception["bcv"]),
                ", the word after the MAS lacks initial stress: ",
                *_case_chanted_word_cell(exception),
                ".",
            )
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(_CHRONICLES_8_11_VERSE),
                ", in the Leningrad Codex, the word after a MAS lacks initial stress. See ",
                mb_html.anchor_h(
                    f"the ambiguous marks in {_CHRONICLES_8_11_REF}",
                    _CHRONICLES_8_11_FNAME,
                ),
                ".",
            )
        ),
        *_next_conjunctive_footnote(survey),
        *_sources_for_types_footnote(),
        *_type_2_type_3_footnote(survey),
        *_vocal_shewa_footnote(),
        *_pashta_stress_helper_footnote(),
        *_fit_type_2_no_ivs_footnote(),
    ]


def _dually_cantillated_passages(survey: dict) -> list:
    """The template-only comparison for Phonetic MAM's dual cantillation."""
    dual_cantillation = _dual_cantillation(survey)
    template_comparison = dual_cantillation["template_counts"]
    alef = template_comparison[psm.CANT_ALEF]
    bet = template_comparison[psm.CANT_BET]
    difference = dual_cantillation["meteg_before_stress_difference"]
    chanted_word_difference = dual_cantillation["chanted_word_count_difference"]
    headers = (
        "count",
        _cantillation_label(psm.CANT_ALEF),
        _cantillation_label(psm.CANT_BET),
    )
    categories = (
        ("Words", "chanted words checked"),
        (
            mb_html.abbr("MBS", {"title": "meteg before the stress"}),
            "meteg before the stressed syllable",
        ),
        (
            mb_html.abbr("MAS", {"title": "meteg after the stress"}),
            "meteg after the stressed syllable",
        ),
    )
    rows = [
        mb_html.table_row_of_data(
            (label, f"{alef[category]:,}", f"{bet[category]:,}"),
            (None, _NUMERIC_CELL, _NUMERIC_CELL),
        )
        for label, category in categories
    ]
    difference_rows = [
        mb_html.table_row_of_data(
            (
                _cantillation_label(psm.CANT_ALEF),
                _hebrew_cell(" ".join(difference[psm.CANT_ALEF]["chanted_words"])),
                ("no ", _ROM_METEG),
            ),
            (None, _HEBREW_CELL, None),
        ),
        mb_html.table_row_of_data(
            (
                _cantillation_label(psm.CANT_BET),
                _hebrew_cell(" ".join(difference[psm.CANT_BET]["chanted_words"])),
                mb_html.abbr("MBS", {"title": "meteg before the stress"}),
            ),
            (None, _HEBREW_CELL, None),
        ),
    ]
    chanted_word_difference_rows = [
        mb_html.table_row_of_data(
            (
                _cantillation_label(cantillation),
                _hebrew_cell(
                    " ".join(chanted_word_difference[cantillation]["chanted_words"])
                ),
            ),
            (None, _HEBREW_CELL),
        )
        for cantillation in (psm.CANT_ALEF, psm.CANT_BET)
    ]
    return [
        mb_html.heading_level_2("Dually cantillated passages"),
        mb_html.para(
            (
                "The Masoretic tradition records two cantillations for three passages. Those"
                " three passages are the two Decalogues and Genesis 35:22. The analyses"
                " presented in this document use only MAM's ",
                _cantillation_label(psm.CANT_ALEF),
                " cantillation. The table below shows that this choice has no effect on the"
                " MAS count and changes the other two counts only by 1. (We have not analyzed"
                " what effect the choice has on the “fit for MAS” analysis, but I think it is"
                " safe to assume that the choice has little or no effect.)",
            )
        ),
        _table(headers, rows),
        mb_html.para(
            (
                "The difference in the number of words between ",
                _cantillation_label(psm.CANT_ALEF),
                " and ",
                _cantillation_label(psm.CANT_BET),
                " is due to the different pointing of two atoms in ",
                _ref_link(chanted_word_difference["bcv"]),
                ": ",
                _cantillation_label(psm.CANT_ALEF),
                " has two simple words where ",
                _cantillation_label(psm.CANT_BET),
                " has one compound word.",
            )
        ),
        mb_html.table(
            chanted_word_difference_rows,
            {"class": "limited-width post-stress-meteg-table"},
        ),
        mb_html.para(
            (
                "The difference in the MBS count between ",
                _cantillation_label(psm.CANT_ALEF),
                " and ",
                _cantillation_label(psm.CANT_BET),
                " is due to the different pointing of three atoms in ",
                _ref_link(difference["bcv"]),
                ": ",
                _cantillation_label(psm.CANT_ALEF),
                " has no ",
                _ROM_METEG,
                " among those three atoms; ",
                _cantillation_label(psm.CANT_BET),
                " has one ",
                _ROM_METEG,
                " before the stress among those three atoms.",
            )
        ),
        mb_html.table(
            difference_rows, {"class": "limited-width post-stress-meteg-table"}
        ),
    ]


def _type_2_type_3_footnote(survey: dict) -> list:
    """Footnote 6: why types 2 and 3 do not overlap in the current survey."""
    type_2_records = _type_2_records(survey)
    type_2_count = _by_type_count(survey, psm.TYPE_GUTTURAL)
    type_2_final_mas_count = sum(
        record["is_the_last_syllable"] for record in type_2_records
    )
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    overlap = _type_2_type_3_overlap(survey)
    overlap_count = overlap["chanted_words"]
    overlap_by_book = overlap["by_book"]
    overlap_example = overlap["example"]
    return [
        mb_html.heading_level_3(
            "φ6 — Do types 2 and 3 overlap?", {"id": _TYPE_2_TYPE_3_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                f"Types 2 and 3 could in principle overlap. However, {type_2_final_mas_count}"
                f" of the {type_2_count} type-2 MAS syllables have ",
                _ROM_PATAH,
                ", and while the other ",
                f"{_spelled(len(nonfinal_mas_syllable_records))} have ",
                _ROM_TSERE,
                ", those syllables are not only open but also nonfinal. Thus no type-2 MAS meets the"
                " type-3 condition. Indeed, words with a final ",
                _ROM_TSERE,
                " syllable closed by a guttural are quite rare even without a ",
                _ROM_METEG,
                ". Only ",
                f"{overlap_count:,} words have a final ",
                _ROM_TSERE,
                " syllable closed by a guttural. All ",
                f"{overlap_count:,} occur in Aramaic and end in a ",
                _ROM_MAPPIQ,
                " ",
                _ROM_HE,
                f": {overlap_by_book['da']:,} are in Daniel and "
                f"{overlap_by_book['er']:,} are in Ezra. For example:",
            )
        ),
        _singleton_example_table(
            overlap_example["bcv"],
            wrap_hebrew_runs(overlap_example["mam_form"]),
        ),
    ]


def _vocal_shewa_footnote() -> list:
    """Footnote 7: an initial vocal shewa does not block initial stress."""
    return [
        mb_html.heading_level_3(
            ("φ7 — Vocal ", _ROM_SHEWA, " and initial stress"),
            {"id": _VOCAL_SHEWA_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "We do not consider vocal ",
                _ROM_SHEWA,
                " to be a syllable, so a word with an initial vocal ",
                _ROM_SHEWA,
                " can still have initial stress.",
            )
        ),
    ]


def _pashta_stress_helper_footnote() -> list:
    """Footnote 8: a pashta helper on the first letter excludes initial vocal shewa."""
    return [
        mb_html.heading_level_3(
            ("φ8 — A ", _ROM_PASHTA, " stress helper on the first letter"),
            {"id": _PASHTA_STRESS_HELPER_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "In subtype 1B, the next word has a ",
                _ROM_PASHTA,
                " stress helper on its first letter, which tells us that it does not"
                " have an initial vocal ",
                _ROM_SHEWA,
                ".",
            )
        ),
    ]


def _fit_type_2_no_ivs_footnote() -> list:
    """Footnote 9: how Fit-for-MAS types 2Af and 2Bf differ from 2A and 2B."""
    return [
        mb_html.heading_level_3(
            "φ9 — Fit for MAS types 2Af and 2Bf",
            {"id": _FIT_TYPE_2_NO_IVS_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                f"For {author.dquote('fit for MAS')}, 2Af and 2Bf are subtypes 2A and"
                " 2B with one added"
                " condition: the next word does not begin with vocal ",
                _ROM_SHEWA,
                f". (The f stands for {author.dquote('fit for MAS')}.) Every type-2 MAS"
                " case already has a next word without vocal ",
                _ROM_SHEWA,
                ", so the condition removes no type-2 MAS case, and narrows only the"
                " set of syllables deemed fit for MAS.",
            )
        ),
    ]


def _nonfinal_mas_syllable_footnote(survey: dict) -> list:
    """Footnote 2: the four nonfinal MAS syllables."""
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert len(nonfinal_mas_syllable_records) == 4
    assert all(
        _case_filter_subtype(record) == "2C" for record in nonfinal_mas_syllable_records
    )
    # How nearly the four exhaust subtype 2C is the point of the second clause below, so the
    # remainder is counted here rather than stated as a constant.  Ben's ask of 2026-09-08.
    two_c_records = [
        record
        for record in survey["post_stress"]
        if _case_filter_subtype(record) == "2C"
    ]
    other_two_c_count = len(two_c_records) - len(nonfinal_mas_syllable_records)
    return [
        mb_html.heading_level_3(
            "φ2 — The four nonfinal MAS syllables", {"id": _NONFINAL_MAS_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                "The four exceptions are all of subtype 2C; indeed, subtype 2C has only ",
                _spelled(other_two_c_count),
                " other case. Each of the four exceptions has an open penultimate ",
                _ROM_TSERE,
                " MAS syllable before a final furtive-",
                _ROM_PATAH,
                " syllable.",
            )
        ),
        mb_html.table(
            [
                mb_html.table_row_of_data(
                    (
                        _ref_link(record["bcv"]),
                        _case_chanted_word_cell(record),
                    ),
                    (None, _HEBREW_CELL),
                )
                for record in nonfinal_mas_syllable_records
            ],
            {"class": "limited-width post-stress-meteg-table"},
        ),
    ]


def _fit_for_mas_facts(survey: dict) -> list:
    """Every syllable fit for MAS, including the ones lacking MAS."""
    fit_for_mas = _fit_for_mas(survey)
    total_mas = len(survey["post_stress"])
    not_fit_for_mas_count = total_mas - fit_for_mas["with_mas"]
    assert not_fit_for_mas_count == len(_not_fit_for_mas_records(survey))
    type_3_counts = fit_for_mas["by_fit_type"][psm.FIT_TYPE_3]
    type_3_yield = type_3_counts["with_mas"] / type_3_counts["candidates"]

    def has_mas_percentage(with_mas: int, without_mas: int) -> str:
        candidates = with_mas + without_mas
        assert candidates > 0
        return f"{with_mas / candidates:.1%}"

    headers = ("Type", "Fit for MAS", "Has MAS", "% has MAS", "Lacks MAS")
    rows = [
        mb_html.table_row_of_data(
            (
                _fit_type_cell(kind),
                f"{counts['candidates']:,}",
                f"{counts['with_mas']:,}",
                has_mas_percentage(counts["with_mas"], counts["without_mas"]),
                f"{counts['without_mas']:,}",
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL),
        )
        for kind, counts in fit_for_mas["by_fit_type"].items()
    ]
    rows.append(
        mb_html.table_row_of_data(
            (
                mb_html.abbr("any", {"title": "Any of types 1A, 1B, 2Af, 2Bf, or 3."}),
                f"{fit_for_mas['fitting_any_type']:,}",
                f"{fit_for_mas['with_mas']:,}",
                has_mas_percentage(fit_for_mas["with_mas"], fit_for_mas["without_mas"]),
                f"{fit_for_mas['without_mas']:,}",
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL),
        )
    )
    return [
        mb_html.heading_level_2("Fit for MAS", {"id": _FIT_FOR_MAS_SECTION_ID}),
        mb_html.para(
            (
                "How often does MAS appear in a syllable that seems fit for MAS? According to"
                f" our definition of {author.dquote('fit for MAS')}, it appears ",
                f"{fit_for_mas['with_mas'] / fit_for_mas['fitting_any_type']:.1%}",
                f" of the time, but the {author.dquote('yield')} varies widely among"
                f" (sub)types. Notably, the type 3 {author.dquote('yield')} is ",
                f"{type_3_yield:.0%}",
                ".",
            )
        ),
        mb_html.para(
            (
                f"The idea of a syllable {author.dquote('fit for MAS')} is part of the broader idea of a syllable fit for a ",
                _ROM_METEG,
                ". We deem a syllable fit for MAS when:",
            )
        ),
        mb_html.ordered_list(
            (
                *_FIT_FOR_MAS_CRITERIA[:2],
                (
                    _FIT_FOR_MAS_TYPE_CRITERION,
                    " (",
                    _footnote_callout(9, _FIT_TYPE_2_NO_IVS_FOOTNOTE_ID),
                    ").",
                ),
            )
        ),
        mb_html.para(
            "The table below records how often MAS does and does not appear in syllables fit for it."
        ),
        _table(headers, rows),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    f"{fit_for_mas['without_mas']:,} cases fit for MAS that lack MAS",
                    _LACKS_MAS_FNAME,
                ),
                " are listed separately and can be filtered by subtype.",
            )
        ),
        mb_html.para(
            (
                f"The final-row {author.dquote('Has MAS')} count is ",
                f"{fit_for_mas['with_mas']:,}",
                f", rather than the total of {total_mas:,} MAS cases, because "
                f"{not_fit_for_mas_count:,} cases, though they do have MAS, are deemed"
                " not fit for MAS by our criteria. The ",
                mb_html.anchor_h(
                    f"{not_fit_for_mas_count:,} MAS cases not fit for MAS",
                    _NOT_FIT_FNAME,
                ),
                " are listed separately, with the criteria each one fails.",
            )
        ),
        mb_html.para(
            f"A good way to think about the {author.dquote('fit for MAS')} criteria is as"
            " a predictor. Like most predictors, this one has both false positives and"
            " false negatives. Its false positives are cases fit for MAS that lack MAS;"
            " its false negatives are cases not fit for MAS that nonetheless have MAS."
        ),
    ]


def build_next_conjunctive_body(survey: dict) -> list:
    """The cases of MAS whose next word has a conjunctive accent."""
    records = _next_conjunctive_records(survey)
    total = len(survey["post_stress"])
    assert (
        len(records)
        + sum(
            record["next_chanted_word_accent_classification"] == "disjunctive"
            for record in survey["post_stress"]
        )
        == total
    )
    rows = [
        mb_html.table_row_of_data(
            (
                _ref_link(record["bcv"]),
                _case_chanted_word_cell(record),
                _case_filter_subtype(record)
                or _case_type_code(record["structural_type"]),
            ),
            (None, _HEBREW_CELL, None),
        )
        for record in records
    ]
    return [
        mb_html.heading_level_1(_visible_title(_NEXT_CONJUNCTIVE_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(
                    _visible_title(_TITLE),
                    f"{_FNAME}#{_NEXT_CONJUNCTIVE_FOOTNOTE_ID}",
                ),
                ".",
            )
        ),
        mb_html.heading_level_2(
            "Every MAS case whose next word has a conjunctive accent"
        ),
        mb_html.para(
            f"Here are the {len(records):,} cases of MAS in which the next word has a"
            " conjunctive accent:"
        ),
        _table(("", "", mb_html.abbr("(sub)type", {"title": "type or subtype"})), rows),
    ]


def _next_conjunctive_footnote(survey: dict) -> list:
    """Footnote 4: a pointer to MAS cases whose next word has a conjunctive accent."""
    records = _next_conjunctive_records(survey)
    return [
        mb_html.heading_level_3(
            "φ4 — Next words with a conjunctive accent",
            {"id": _NEXT_CONJUNCTIVE_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    f"{len(records):,} cases of MAS whose next word has a conjunctive"
                    " accent",
                    _NEXT_CONJUNCTIVE_FNAME,
                ),
                " are listed separately.",
            )
        ),
    ]
