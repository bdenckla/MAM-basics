r"""MAM's meteg marks after the stress: the main page and eight supporting pages.

The page for ``accgram.post_stress_meteg``'s survey.  That module measures; this one renders,
and takes every figure it prints from the survey rather than from a separate constant.
``pin_claims`` re-derives each figure the prose states and raises on drift, which is the shape
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
the sense the house rule allows for.  Every reader-facing form begins with MAM's data at
generation time. The Fit-for-MAS lack page uses each record's ``mam_form`` and
``next_mam_form``; analysis-only annotations are omitted before HTML is written. None is
typed here.

THESE PAGES SAY PLAIN "word", AND THAT IS A DECISION RATHER THAN AN OVERSIGHT.  The
``hebrew-prose`` skill's first rule is "Never a loose 'word'"; Ben exempted this document and
its sub-documents on 2026-09-08, and the skill allows for it -- plain "word" survives "wherever
the context already settles which sense is meant", and ``_opening``'s second paragraph defines
both "word" and "atom" before any other sentence uses either.  **Do not qualify "word" as
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
examples are type-2 MAS records here.  Re-derive by grouping that JSON's ``TYPE_GUTTURAL``
records by ``(record["system"], psm.type_2_next_filter_group(record["next_mam_form"]))``; the
groups must sum to ``pin_claims``' ungrouped lamed=38, guttural=17, resh=1, bet=2, mem=2.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from accgram import final_stress
from accgram import post_stress_meteg as psm
from accgram import printed_decalogue_strands as pds
from accgram.almost_errors_html_shared import ref_abbrev, wrap_hebrew_runs
from accgram import rtms_report
from author_site import site_data
from mb_author import author
from mb_cmn import paths
from mb_cmn import provenance
from mb_cmn import hebrew_accents as ha
from mb_misc import mb_html
from py_html.my_html_span_romanized import rmn
from py_uxlc import my_uxlc
from py_wlc_json_and_unicode import wlc_uword
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from mb_cmn import bib_locales as tbn

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
_ROM_METEG_CAP = rmn(pds.ROM_METEG.capitalize())
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
_CHRONICLES_8_11_VERSE = "2c8:11"
_CHRONICLES_8_11_REF = ref_abbrev(_CHRONICLES_8_11_VERSE)
# site_data spells these two page titles by hand, being a plain data module with no accgram
# import.  These are what keep those two spellings at ref_abbrev's form.
assert _POST_SILLUQ_REF in _POST_SILLUQ_TITLE, (_POST_SILLUQ_TITLE, _POST_SILLUQ_REF)
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
    recomputing, which is how ``main_0_mega.py`` renders this page without the MAM-private
    clone the survey needs.  Off by hand, so a standalone run still derives the page from the
    corpus rather than from a file.
    """
    survey = psm.load_survey() if trust_survey else psm.build_survey()
    pin_claims(survey)
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
            build_post_silluq_body(survey),
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
    _assert_no_phonetic_mam_annotations_in_lacks_mas_page(out_paths[4])
    return out_paths


def _assert_no_phonetic_mam_annotations_in_lacks_mas_page(path_string: str) -> None:
    """Prevent Phonetic MAM's analysis-only marks from reaching the reader page."""
    forbidden = {chr(code_point) for code_point in psm._PHONETIC_MAM_ANNOTATIONS}
    path = Path(path_string)
    present = forbidden & set(path.read_text(encoding="utf-8"))
    assert not present, (path, present)


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


def gen_html_file(out_dir: Path | None = None, *, trust_survey: bool = False) -> str:
    """Write all nine post-stress-meteg pages and return the main page's path."""
    return gen_html_files(out_dir, trust_survey=trust_survey)[0]


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
            (_ROM_METEG_CAP, " after ", _ROM_SILLUQ, f" in {_MAM_POST_SILLUQ_REF}")
        ),
        mb_html.para(_mam_post_silluq_statement(survey)),
        _mam_post_silluq_aleppo_crop(),
        mb_html.para(
            (
                "At ",
                _ref_link(_MAM_POST_SILLUQ_VERSE),
                ", the Leningrad Codex lacks the ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                ".",
            )
        ),
        _mam_post_silluq_leningrad_crop(),
        *_census_definitions(survey),
        *_dually_cantillated_passages(survey),
        *_oleh_meteg_overlap(survey),
    ]


# --- the numbers, all of them read off the survey ------------------------------


def _count(survey: dict, system: str, category: str) -> int:
    return survey["counts"][system][category]


def _post_stress(survey: dict, system: str | None = None) -> list[dict]:
    return [
        one
        for one in survey["post_stress"]
        if system is None or one["system"] == system
    ]


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


def pin_claims(survey: dict) -> None:
    """Re-derive every figure the prose states, and raise on drift.

    The page's sentences state census figures; each figure is computed from the survey here as
    well as where it is rendered, so a corpus that moves under the page fails the build rather
    than publishing a stale number.
    """
    post_stress = survey["post_stress"]
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    assert {
        "mbs_only_chanted_words_with_multiple_mbs": census_chanted_word_summary[
            "mbs_only_chanted_words_with_multiple_mbs"
        ],
        "mbs_only_chanted_words_with_more_than_two_mbs": census_chanted_word_summary[
            "mbs_only_chanted_words_with_more_than_two_mbs"
        ],
    } == {
        "mbs_only_chanted_words_with_multiple_mbs": 143,
        "mbs_only_chanted_words_with_more_than_two_mbs": 0,
    }
    assert census_chanted_word_summary["by_system"] == {
        _PROSE: {"mbs_only": 12828, "mas": 178},
        _POETIC: {"mbs_only": 1786, "mas": 54},
    }
    assert survey["qamats_variant_census"]["by_system"] == {
        _PROSE: {
            "source_entries": 233586,
            "variant_rows": 309,
            "duplicate_phonetic_reading_entries": 309,
            "mam_chanted_words_counted": 233277,
        },
        _POETIC: {
            "source_entries": 29605,
            "variant_rows": 61,
            "duplicate_phonetic_reading_entries": 63,
            "mam_chanted_words_counted": 29542,
        },
    }
    qamats_grouping_differences = survey["qamats_variant_census"][
        "distinct_phonetic_groupings"
    ]
    assert [record["bcv"] for record in qamats_grouping_differences] == [
        "ps35:10",
        "pr19:7",
    ]
    assert all(
        len(record["qamats-dal"]) == 1 and len(record["qamats-sam"]) == 2
        for record in qamats_grouping_differences
    )
    assert len(post_stress) == _both(
        survey, "meteg after the stressed syllable"
    ), "the post-stress records and the post-stress count disagree"
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
    assert next_accent_classification == {
        "disjunctive": 217,
        "conjunctive": 15,
    }
    actual_type_1_mas = _actual_type_1_mas(survey)
    assert {
        "cases": actual_type_1_mas["cases"],
        "by_initial_stress_pattern": actual_type_1_mas["by_initial_stress_pattern"],
    } == {
        "cases": 123,
        "by_initial_stress_pattern": {
            psm.TYPE_1_SUBTYPE_A: {
                "cases": 103,
                "by_system": {_PROSE: 97, _POETIC: 6},
            },
            psm.TYPE_1_SUBTYPE_B: {
                "cases": 12,
                "by_system": {_PROSE: 12, _POETIC: 0},
            },
            psm.TYPE_1_SUBTYPE_C: {
                "cases": 7,
                "by_system": {_PROSE: 3, _POETIC: 4},
            },
            "not_initially_stressed": {
                "cases": 1,
                "by_system": {_PROSE: 1, _POETIC: 0},
            },
        },
    }
    assert tuple(actual_type_1_mas["example_keys_by_initial_stress_pattern"]) == tuple(
        actual_type_1_mas["by_initial_stress_pattern"]
    )
    assert all(
        set(example_key) == {"bcv", "chanted_word", "jta"}
        for example_key in actual_type_1_mas[
            "example_keys_by_initial_stress_pattern"
        ].values()
    )
    fit_for_mas = _fit_for_mas(survey)
    assert (
        fit_for_mas["fitting_any_type"],
        fit_for_mas["with_mas"],
        fit_for_mas["without_mas"],
    ) == (377, 200, 177)
    assert (
        fit_for_mas["with_mas"] + fit_for_mas["without_mas"]
        == fit_for_mas["fitting_any_type"]
    )
    assert fit_for_mas["by_type_1_subtype"] == {
        psm.TYPE_1_SUBTYPE_A: {
            "candidates": 210,
            "with_mas": 97,
            "without_mas": 113,
            "with_mas_by_system": {_PROSE: 93, _POETIC: 4},
        },
        psm.TYPE_1_SUBTYPE_B: {
            "candidates": 43,
            "with_mas": 12,
            "without_mas": 31,
            "with_mas_by_system": {_PROSE: 12, _POETIC: 0},
        },
        psm.TYPE_1_SUBTYPE_C: {
            "candidates": 1571,
            "with_mas": 4,
            "without_mas": 1567,
            "with_mas_by_system": {_PROSE: 2, _POETIC: 2},
        },
    }
    assert fit_for_mas["by_fit_type"] == {
        psm.FIT_TYPE_1_A: {
            "candidates": 210,
            "with_mas": 97,
            "without_mas": 113,
        },
        psm.FIT_TYPE_1_B: {
            "candidates": 43,
            "with_mas": 12,
            "without_mas": 31,
        },
        psm.FIT_TYPE_2_AF: {
            "candidates": 38,
            "with_mas": 35,
            "without_mas": 3,
        },
        psm.FIT_TYPE_2_BF: {
            "candidates": 45,
            "with_mas": 15,
            "without_mas": 30,
        },
        psm.FIT_TYPE_3: {
            "candidates": 41,
            "with_mas": 41,
            "without_mas": 0,
        },
    }
    assert fit_for_mas["mas_not_in_the_table"] == {
        "outside_the_three_types": 7,
        "stress_not_penultimate": 4,
        "next_word_not_disjunctive": 15,
        "next_word_not_initially_stressed": 1,
        "type_1_subtype_C": 4,
        "type_2_subtype_C": 1,
    }
    mbs_and_mas = census_chanted_word_summary["mas_chanted_words_with_mbs"]
    assert [record["bcv"] for record in mbs_and_mas] == [
        "lv25:53",
        "1s22:17",
        "1s25:15",
        "1s29:6",
        "1k8:16",
        "is65:18",
        "je42:2",
        "mi1:12",
        "ps94:9",
        "da6:25",
    ]
    assert all(
        record["mam_form"] is not None and record["mam_form"].count(psm.METEG) == 2
        for record in mbs_and_mas
    )
    assert fit_for_mas["with_mas"] + sum(
        fit_for_mas["mas_not_in_the_table"].values()
    ) == len(post_stress)
    not_fit_for_mas_records = _not_fit_for_mas_records(survey)
    assert len(not_fit_for_mas_records) == len(post_stress) - fit_for_mas["with_mas"]
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
    assert len(fitting_records) == fit_for_mas["fitting_any_type"]
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
    assert Counter(
        (record["fit_type"], record["has_mas"]) for record in fitting_records
    ) == Counter(
        {
            (psm.FIT_TYPE_1_A, True): 97,
            (psm.FIT_TYPE_1_A, False): 113,
            (psm.FIT_TYPE_1_B, True): 12,
            (psm.FIT_TYPE_1_B, False): 31,
            (psm.FIT_TYPE_2_AF, True): 35,
            (psm.FIT_TYPE_2_AF, False): 3,
            (psm.FIT_TYPE_2_BF, True): 15,
            (psm.FIT_TYPE_2_BF, False): 30,
            (psm.FIT_TYPE_3, True): 41,
        }
    )
    assert sum(
        record["has_mas"] and record["word_has_another_meteg"]
        for record in fitting_records
    ) == len(mbs_and_mas)
    lacks_mas_records = _lacks_mas_records(survey)
    assert len(lacks_mas_records) == fit_for_mas["without_mas"]
    assert Counter(record["fit_type"] for record in lacks_mas_records) == Counter(
        {
            psm.FIT_TYPE_1_A: 113,
            psm.FIT_TYPE_1_B: 31,
            psm.FIT_TYPE_2_AF: 3,
            psm.FIT_TYPE_2_BF: 30,
        }
    )
    assert all(record["chanted_word"] for record in lacks_mas_records)
    assert (
        sum(fit_for_mas["accent_grammar_token_counts"].values())
        == fit_for_mas["candidate_chanted_words"]
    )
    by_type = sum(_by_type_count(survey, kind) for kind in _TYPE_SOURCES)
    assert by_type + _by_type_count(survey, psm.TYPE_UNCLASSIFIED) == len(
        post_stress
    ), "the structural types do not partition the post-stress records"
    misc_records = _misc_records(survey)
    assert len(misc_records) == _by_type_count(survey, psm.TYPE_UNCLASSIFIED)
    assert all(one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in misc_records)
    for subtype in (
        psm.SUBTYPE_MISC_VAYOMER,
        psm.SUBTYPE_MISC_ALMOST_TYPE_3,
    ):
        subtype_records = _subtype_records(survey, subtype)
        assert len(subtype_records) == _by_subtype_count(survey, subtype)
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
    assert len(misc_vayomer_records) == 4, misc_vayomer_records
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
    assert len(type_2_records) == _by_type_count(survey, psm.TYPE_GUTTURAL)
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
    assert [record["bcv"] for record in nonfinal_mas_syllable_records] == [
        "is63:12",
        "pr1:19",
        "pr11:26",
        "jb5:10",
    ]
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
    assert len(type_2_final_mas_records) == 56
    assert all(
        not record["syllable_is_open"] and record["vowel"] == "pataḥ"
        for record in type_2_final_mas_records
    ), "the final-MAS type-2 cases have moved"
    type_3_records = [
        record
        for record in post_stress
        if record["structural_type"] == psm.TYPE_CLOSED_TSERE
    ]
    assert len(type_3_records) == _by_type_count(survey, psm.TYPE_CLOSED_TSERE)
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
    assert Counter(
        _type_1_subtype_code(record) for record in type_1_records
    ) == Counter({"1A": 103, "1B": 12, "1C": 7, "1D": 1})
    noninitial_next_stress_records = _noninitial_next_stress_records(survey)
    assert [
        (
            record["bcv"],
            record["mam_form"],
            record["next_mam_form"],
            record["structural_type"],
        )
        for record in noninitial_next_stress_records
    ] == [
        (
            "je46:14",
            "וְהַשְׁמִ֣יעֽוּ",
            "בְמִגְדּ֔וֹל",
            psm.TYPE_OPEN,
        )
    ], "the noninitial-next-stress exception has moved"
    assert (
        len(type_1_records),
        len(type_2_records),
        len(type_3_records),
        len(misc_records),
    ) == (123, 60, 42, 7)
    type_2_type_3_overlap = _type_2_type_3_overlap(survey)
    assert type_2_type_3_overlap["chanted_words"] == 154
    assert type_2_type_3_overlap["by_book"] == {"da": 136, "er": 18}
    assert type_2_type_3_overlap["by_final_letter"] == {"ה": 154}
    assert type_2_type_3_overlap["example"]["bcv"] == "da2:5"
    assert type_2_type_3_overlap["example"]["mam_form"] is not None
    type_2_next_group_counts = Counter(
        _type_2_next_group(record) for record in type_2_records
    )
    assert type_2_next_group_counts == Counter(
        lamed=38, guttural=17, resh=1, bet=2, mem=2
    )
    assert Counter(
        _type_2_filter_group(record) for record in type_2_records
    ) == Counter(lamed=38, guttural=17, **{"not-lamed-or-guttural": 5})
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
    assert dual_cantillation["counted_cantillation"] == psm.CANT_ALEF
    for category in (
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    ):
        assert whole_census_comparison[psm.CANT_ALEF][category] == _both(
            survey, category
        )
    assert (
        whole_census_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"]
        == whole_census_comparison[psm.CANT_BET]["meteg after the stressed syllable"]
    )
    assert template_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"] == 0
    assert template_comparison[psm.CANT_BET]["meteg after the stressed syllable"] == 0
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
    return wrap_hebrew_runs(psm._as_mam_would_write_it(form or ""))


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


def _book_name(bcv: str) -> str:
    return tbn.ordered_short_dash_full_39(wlc_bb_to_bk39id(bcv[:2]))[3:]


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
                "So, among words with at least one meteg mark, there are ",
                f"{mas:,}",
                " words where one of the meteg marks is after the stress and ",
                f"{mbs_only:,}",
                " words where none of the meteg marks is after the stress. (There is never more"
                " than one meteg mark after the stress.) See the ",
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
    assert len(records) == 10
    fitting_mas_with_another_meteg = [
        record
        for record in _fit_for_mas(survey)["records"]
        if record["has_mas"] and record["word_has_another_meteg"]
    ]
    assert len(fitting_mas_with_another_meteg) == len(records)
    fit_record_by_bcv_and_mam_form = {
        (record["bcv"], record["mam_form"]): record
        for record in fitting_mas_with_another_meteg
    }
    assert len(fit_record_by_bcv_and_mam_form) == len(records)
    assert {(record["bcv"], record["mam_form"]) for record in records} == set(
        fit_record_by_bcv_and_mam_form
    )
    # The (sub)type column shows the structural taxonomy, so the label comes off the
    # post-stress record rather than off the fit-for-MAS one beside it.
    post_stress_by_bcv_and_mam_form = {
        (one["bcv"], one["mam_form"]): one for one in survey["post_stress"]
    }
    assert {(record["bcv"], record["mam_form"]) for record in records} <= set(
        post_stress_by_bcv_and_mam_form
    )
    return [
        mb_html.heading_level_2("Census definitions"),
        mb_html.para(
            (
                mb_html.abbr("MBS_O", {"title": _MBS_O_CENSUS_GLOSS}),
                " counts words that have one or more meteg marks before the"
                f" stress and none after it. The {author.dquote('O')} means"
                f" {author.dquote('only')}. ",
                mb_html.abbr("MAS", {"title": _MAS_CENSUS_GLOSS}),
                " counts words that have one or more meteg marks after the"
                " stress, whether the word has zero or more meteg marks"
                " before the stress.",
            )
        ),
        mb_html.para(
            "The % MAS column is the MAS count divided by the sum of the MBS_O and MAS counts.",
        ),
        mb_html.para(
            (
                f"{multiple_mbs:,} MBS_O words have more than one meteg mark. Every"
                " such MBS_O word has exactly"
                " two meteg marks.",
            )
        ),
        mb_html.para(
            "No MAS word has more than one meteg mark after the stress: every MAS word has exactly one meteg mark after the stress.",
        ),
        mb_html.para(
            f"There are {_spelled(len(records))} MAS words that also have one meteg mark before the stress. They are listed below. (There are no MAS words with more than one meteg before the stress.)",
        ),
        _table(
            ("", "", "(sub)types"),
            [
                mb_html.table_row_of_data(
                    (
                        _ref_link(record["bcv"]),
                        _case_chanted_word_cell(
                            fit_record_by_bcv_and_mam_form[
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
    assert total == type_1_mas["cases"] == 123
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
    assert total == _by_type_count(survey, psm.TYPE_GUTTURAL) == 60
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


def _case_chanted_word_cell(record: dict) -> tuple:
    """The MAM MAS form followed by its next chanted word."""
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
    return _paired_chanted_word_cell(
        record["mam_form"] or record["chanted_word"],
        next_word,
        record.get("intervening_mam_punctuation", ()),
    )


def _oleh_chanted_word_cell(record: dict) -> tuple:
    """The oleh context, extending into the next chanted word only for a yored there."""
    current_form = record["mam_form"] or record["chanted_word"]
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


def _post_silluq_leningrad_form(survey: dict) -> str:
    """The BHS transcription of the Leningrad Codex form at 1 Samuel 17:5."""
    forms = dict(_post_silluq_comparison(survey))
    return forms["BHS"]


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


def _post_silluq_details(survey: dict) -> list:
    """The evidence and discussion for 1 Samuel 17:5's post-silluq meteg."""
    comparison = _post_silluq_comparison(survey)
    comparison_rows = [
        mb_html.table_row_of_data((source, _hebrew_cell(form)), (None, _HEBREW_CELL))
        for source, form in comparison
    ]
    return [
        mb_html.para(
            (
                f"In the Leningrad Codex, the last word of {_POST_SILLUQ_REF} has a ",
                _ROM_METEG,
                " after its ",
                _ROM_SILLUQ,
                ".",
            )
        ),
        _post_silluq_lc_crop(),
        mb_html.para(
            (
                "That ",
                _ROM_METEG,
                " is surprising, but we deem the ",
                _ROM_SILLUQ,
                "-",
                _ROM_METEG,
                " reading less surprising than the ",
                _ROM_METEG,
                "-",
                _ROM_SILLUQ,
                " reading. In ",
                _ROM_SILLUQ,
                "-",
                _ROM_METEG,
                " order, only the presence of the ",
                _ROM_METEG,
                " is surprising; in ",
                _ROM_METEG,
                "-",
                _ROM_SILLUQ,
                " order, the location of the stress is surprising. We find a ",
                _ROM_METEG,
                " surprise far more likely than a stress surprise.",
            )
        ),
        mb_html.para(
            (
                "This surprising ",
                _ROM_METEG,
                " is correctly recorded in BHS and in BHS-derived editions such as UXLC and"
                " WLC:",
            )
        ),
        mb_html.table(
            comparison_rows,
            {"class": "limited-width post-stress-meteg-table"},
        ),
        mb_html.para(
            (
                "A ",
                _ROM_METEG,
                " after a ",
                _ROM_SILLUQ,
                " is hard to identify in Unicode, since the two marks share one codepoint.",
            )
        ),
    ]


def build_post_silluq_body(survey: dict) -> list:
    """The independent page about a meteg after silluq in 1 Samuel 17:5."""
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
        *_post_silluq_details(survey),
        mb_html.para(
            (
                "As one would expect, the Aleppo Codex has this word with no ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                ":",
            )
        ),
        _post_silluq_aleppo_crop(),
    ]


def _post_silluq_footnote(survey: dict) -> list:
    """Footnote 1: the MAM and Leningrad Codex post-silluq cases."""
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
                f"At {_POST_SILLUQ_REF}, in the Leningrad Codex, there is a ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                " in ",
                wrap_hebrew_runs(_post_silluq_leningrad_form(survey)),
                ". See ",
                mb_html.anchor_h(
                    (
                        "the crops and why we read the marks as ",
                        _ROM_SILLUQ,
                        "-",
                        _ROM_METEG,
                    ),
                    _POST_SILLUQ_FNAME,
                ),
                ".",
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
                " according to one interpretation of the ambiguous meteg/merkha marks in the"
                " manuscript.",
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
    assert other_two_c_count == 1, two_c_records
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
        mb_html.unordered_list(
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


def add_args(parser, *, repo_root: Path) -> None:
    del repo_root
    parser.add_argument(
        "--html-out-dir",
        type=Path,
        default=None,
        help="Directory to write the page into (default: this repo's gh-pages).",
    )
    parser.add_argument(
        "--trust-survey",
        action="store_true",
        help=(
            "Read out/accgram/post-stress-meteg.json instead of recomputing the survey."
            " Only for a caller that cannot reach the MAM-private clone."
        ),
    )


def run(args) -> None:
    out_paths = gen_html_files(
        getattr(args, "html_out_dir", None),
        trust_survey=bool(getattr(args, "trust_survey", False)),
    )
    for out_path in out_paths:
        print(f"Generated {out_path}")
