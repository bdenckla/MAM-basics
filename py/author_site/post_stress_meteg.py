r"""MAM's metegs after the primary stress: the main page and three case tables.

The page for ``accgram.post_stress_meteg``'s survey.  That module measures; this one renders,
and takes every figure it prints from the survey rather than from a constant of its own.
``pin_claims`` re-derives each figure the prose states and raises on drift, which is the shape
``maqaf_nonfinal_accents_page.pin_claims`` established.

A LOOSE PAGE AT THE DEPLOY ROOT, beside ``index.html`` and ``unicode-proposals.html``, which
is Ben's decision of 2026-09-03 (``doc/PLAN-post-stress-meteg-page-and-holman-m23.md``).  Not
under ``gh-pages/wlc/``: that prefix exists so wlc-utils' frozen redirect stubs can rewrite
onto ``MAM-basics/wlc/<path>``, a page published here after the 2026-08-17 move earns no stub,
and this page's corpus is MAM rather than WLC.

IT LINKS TWO STYLESHEETS, and the second is the accgram one.  ``gh-pages/style.css`` is the
deploy root's own, whose whole job is the light/dark switching; ``gh-pages/wlc/style.css``
supplies the ``lang="hbo"`` font at the size that makes accents legible, the italic for a
romanized accent name, and the numeric-cell alignment.  A stylesheet's ``@font-face`` URL
resolves against the stylesheet, so ``woff2/Taamey_D.woff2`` reaches the font from here too.

WHY THIS PAGE SHOWS POINTED HEBREW where the accgram pages show letters and accents alone.
``accents_and_letters`` drops U+05BD along with the vowels, and U+05BD is this page's whole
subject; and what the page is about is which SYLLABLE a mark falls in, which a reader cannot
see without the vowels that make the syllables.  Both of the page's three structural types
are named for a vowel or a syllable shape, so the vowel is the point of the comparison here in
the sense the house rule allows for.  Every form is lifted from its labelled text at generation
time -- MAM forms through ``mam_form`` -- and none is typed here.

THE PAGE QUOTES NEITHER YEIVIN NOR BREUER.  The plan permits bounded excerpts and does not
require them; the sections are cited by number and their content paraphrased, so no private
source text reaches a public page.  ``_EXCERPTS`` is empty and ``_excerpt_accounting`` asserts
that it is, which is the plan's requirement for a page with no excerpts.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from accgram import final_stress
from accgram import post_stress_meteg as psm
from accgram.almost_errors_html_shared import ref_abbrev, wrap_hebrew_runs
from accgram import rtms_report
from author_site import site_data
from mb_cmn import hebrew_letters as hl
from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html
from py_uxlc import my_uxlc
from py_wlc_json_and_unicode import wlc_uword
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id
from mb_cmn import bib_locales as tbn

_FNAME = site_data.POST_STRESS_METEG_FNAME
_TITLE = site_data.POST_STRESS_METEG_TITLE
_CASES_FNAME = site_data.POST_STRESS_METEG_CASES_FNAME
_CASES_TITLE = site_data.POST_STRESS_METEG_CASES_TITLE
_TYPE_2_FNAME = site_data.POST_STRESS_METEG_TYPE_2_FNAME
_TYPE_2_TITLE = site_data.POST_STRESS_METEG_TYPE_2_TITLE
_MISC_FNAME = site_data.POST_STRESS_METEG_MISC_FNAME
_MISC_TITLE = site_data.POST_STRESS_METEG_MISC_TITLE
_DUAL_CANTILLATION_APPENDIX_ID = "dually-cantillated-passages"

# The M23 card's link lands here, so the identifier is half of that card's href and cannot be
# renamed alone: py/py_render/rt_suggestion_context.py builds the other half from the same
# site_data constant.
M23_SECTION_ID = site_data.POST_STRESS_METEG_M23_ID
_HOLMAN_M23_RECORD_HREF = "holman/table_data_findings_suppressed.html#mam023"

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

# The two verses the page names outside its tables.  The survey records their chanted words as
# MAM has them today, under ``currency.focus_verses``, so the forms shown here are lifted like
# every other form on the page.
_M23_VERSE = "is23:12"
_POST_SILLUQ_VERSE = "1s17:5"
_POST_SILLUQ_LC_CROP_URL = (
    "https://github.com/user-attachments/assets/" "2983ebc8-df3f-4215-a009-23a33e2a8321"
)
_POST_SILLUQ_LC_CROP_SOURCE_URL = "https://github.com/bdenckla/phonetic-hbo/issues/78"

_ITM_GLOSS = "Yeivin's Introduction to the Tiberian Masorah"
_COS_GLOSS = "Breuer's The Cantillation of Scripture"
_ITM_ADAPTATION_URL_BY_SECTION = {
    308: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-307_310.html#ns308",
    325: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns325",
    332: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns332",
    338: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-318_344.html#ns338",
    354: "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns354",
}
_ITM_SECTION_REFERENCE = re.compile(r"§(?P<section>[0-9]+)")

# Yeivin and Breuer on each of the three types, and how each book grades it.  The pairing is
# the M23 evidence note's, doc/holman-meteg-m23-isaiah-23-12.md; both books are cited for
# every type, so no row rests on one source.
_TYPE_SOURCES = {
    psm.TYPE_OPEN: ("§332", "§3(j), §§46-47", "optional in both books"),
    psm.TYPE_GUTTURAL: ("§354", "§3(b), §§9-10", "obligatory in Breuer"),
    psm.TYPE_CLOSED_TSERE: (
        "§338, fed by §308",
        "§3(a), §§5-8",
        "obligatory in both books",
    ),
}

_TYPE_CODES = {
    psm.TYPE_OPEN: ("1", "an open syllable"),
    psm.TYPE_GUTTURAL: (
        "2",
        "a syllable closed by a guttural at the end of the chanted word",
    ),
    psm.TYPE_CLOSED_TSERE: ("3", "a final closed syllable whose vowel is tsere"),
}
_CASE_TABLE_ID = "post-stress-meteg-cases"
_CASE_TYPE_FILTER_ID = "post-stress-meteg-type-filter"
_CASE_SELECTED_COUNT_ID = "post-stress-meteg-selected-count"
_CASE_TABLE_CLASS = "post-stress-meteg-cases-table"
_CASE_STRIPED_ROW_CLASS = "post-stress-meteg-cases-striped-row"
_FOLLOWING_CHANTED_WORD_CLASS = "post-stress-meteg-following-chanted-word"
_HEBREW_SPACING_CHECKBOX_ID = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_BODY_CLASS = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_STORAGE_KEY = "post-stress-meteg-expanded-hebrew"
_HEBREW_SPACING_INDIVIDUAL_EXPANDED_CLASS = (
    "post-stress-meteg-individually-expanded-hebrew"
)
_HEBREW_SPACING_INDIVIDUAL_NORMAL_CLASS = "post-stress-meteg-individually-normal-hebrew"
_TYPE_2_TABLE_ID = "post-stress-meteg-type-2-cases"
_MISC_TABLE_ID = "post-stress-meteg-misc-cases"
_TYPE_2_FOLLOWING_FILTER_ID = "post-stress-meteg-type-2-following-filter"
_TYPE_2_SELECTED_COUNT_ID = "post-stress-meteg-type-2-selected-count"
_TYPE_2_FOLLOWING_GROUPS = ("lamed", "nun", "misc")
_TYPE_2_FOLLOWING_GROUP_BY_INITIAL = {
    hl.LAMED: "lamed",
    hl.NUN: "nun",
}
_HEBREW_SPACING_OPTION = f"""<p><label><input type="checkbox" id="{_HEBREW_SPACING_CHECKBOX_ID}" checked>
This checkbox controls whether Hebrew letter spacing is expanded.</label> Or click a Hebrew word to
toggle only that word's spacing.</p>
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
    const isSelected = typeFilter.value === "all" || row.dataset.type === typeFilter.value;
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
_TYPE_2_FILTER_SCRIPT = f"""<script>
const followingFilter = document.getElementById("{_TYPE_2_FOLLOWING_FILTER_ID}");
const type2Rows = document.querySelectorAll("#{_TYPE_2_TABLE_ID} tr[data-following-initial]");
const type2SelectedCount = document.getElementById("{_TYPE_2_SELECTED_COUNT_ID}");

function updateType2Rows() {{
  let visibleCount = 0;
  for (const row of type2Rows) {{
    const isSelected = followingFilter.value === "all" ||
      row.dataset.followingInitial === followingFilter.value;
    row.hidden = !isSelected;
    row.classList.toggle(
      "{_CASE_STRIPED_ROW_CLASS}",
      isSelected && visibleCount % 2 === 1,
    );
    if (isSelected) {{
      visibleCount += 1;
    }}
  }}
  type2SelectedCount.textContent = "Showing " + visibleCount + " row" +
    (visibleCount === 1 ? "" : "s") + ".";
}}

followingFilter.addEventListener("change", () => {{
  updateType2Rows();
}});
updateType2Rows();
</script>
"""


def gen_html_files(
    out_dir: Path | None = None, *, trust_survey: bool = False
) -> tuple[str, str, str, str]:
    """Write the main page and the three case pages.  Returns all four paths.

    ``trust_survey`` reads the tracked ``out/accgram/post-stress-meteg.json`` instead of
    recomputing, which is how ``main_0_mega.py`` renders this page without the MAM-private
    clone the survey needs.  Off by hand, so a standalone run still derives the page from the
    corpus rather than from a file.
    """
    survey = psm.load_survey() if trust_survey else psm.build_survey()
    pin_claims(survey)
    top_dir = paths.gh_pages_dir() if out_dir is None else Path(out_dir)
    return (
        _write_page(top_dir / _FNAME, _TITLE, build_body(survey)),
        _write_page(top_dir / _CASES_FNAME, _CASES_TITLE, build_cases_body(survey)),
        _write_page(top_dir / _TYPE_2_FNAME, _TYPE_2_TITLE, build_type_2_body(survey)),
        _write_page(top_dir / _MISC_FNAME, _MISC_TITLE, build_misc_body(survey)),
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


def gen_html_file(out_dir: Path | None = None, *, trust_survey: bool = False) -> str:
    """Write all four pages and return the main page's path for older callers."""
    return gen_html_files(out_dir, trust_survey=trust_survey)[0]


def build_body(survey: dict) -> list:
    """The page, section by section, every figure in it read off ``survey``."""
    return [
        mb_html.heading_level_1(_TITLE),
        *_opening(survey),
        *_census(survey),
        *_by_type(survey),
        *_case_list_link(survey),
        *_m23(survey),
        *_post_silluq(survey),
        *_overlapping_diagnostic(survey),
        *_dual_cantillation_appendix(survey),
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


def _type_1_records_with_nonfinal_meteg_syllable(survey: dict) -> list[dict]:
    """Type-1 records where a further final syllable follows the meteg's syllable."""
    return [
        record
        for record in survey["post_stress"]
        if record["structural_type"] == psm.TYPE_OPEN
        and not record["is_the_last_syllable"]
    ]


def _by_subtype_count(survey: dict, subtype: str) -> int:
    return sum(
        survey["post_stress_by_subtype"][system][subtype]
        for system in (_PROSE, _POETIC)
    )


def _subtype_records(survey: dict, subtype: str) -> list[dict]:
    """The post-stress records whose finer classification is ``subtype``."""
    return [one for one in survey["post_stress"] if one["subtype"] == subtype]


def _following_example(record: dict, kind: str) -> tuple:
    """The following MAM chanted word where the source-derived type requires it."""
    if kind not in (psm.TYPE_OPEN, psm.TYPE_GUTTURAL):
        return _hebrew_cell(None)
    following = record["following_mam_form"]
    assert (
        following is not None
    ), f"{record['bcv']}: no MAM form for the following chanted word of {kind}"
    return _hebrew_cell(following)


def _example_of(survey: dict, kind: str) -> dict:
    """The first record of a type, in the corpus's order, as that type's specimen.

    First rather than chosen: a hand-picked specimen is a claim with nothing behind it, and
    the whole set is on the page below anyway.
    """
    for record in survey["post_stress"]:
        if record["structural_type"] == kind:
            return record
    raise AssertionError(f"no post-stress record of type {kind!r} to show")


def _misc_almost_type_1_inaugural(survey: dict) -> dict:
    """The Jeremiah 46:14 record that starts the strict-type-1 subtype."""
    records = [
        one
        for one in _subtype_records(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_1)
        if one["bcv"] == "je46:14"
    ]
    assert len(records) == 1, records
    return records[0]


def _misc_almost_type_2_inaugural(survey: dict) -> dict:
    """The Job 15:35 record that fits Breuer's type (a), but not Yeivin's type 3."""
    records = [
        one
        for one in _subtype_records(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_2)
        if one["bcv"] == "jb15:35"
    ]
    assert len(records) == 1, records
    return records[0]


def pin_claims(survey: dict) -> None:
    """Re-derive every figure the prose states, and raise on drift.

    The page's sentences say things like "231 chanted words"; each such figure is computed
    from the survey here as well as where it is rendered, so a corpus that moves under the
    page fails the build rather than publishing a stale number.
    """
    post_stress = survey["post_stress"]
    assert len(post_stress) == _both(
        survey, "meteg after the stressed syllable"
    ), "the post-stress records and the post-stress count disagree"
    by_type = sum(_by_type_count(survey, kind) for kind in _TYPE_SOURCES)
    assert by_type + _by_type_count(survey, psm.TYPE_UNCLASSIFIED) == len(
        post_stress
    ), "the structural types do not partition the post-stress records"
    misc_records = _misc_records(survey)
    assert len(misc_records) == _by_type_count(survey, psm.TYPE_UNCLASSIFIED)
    assert all(one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in misc_records)
    for subtype in (
        psm.SUBTYPE_MISC_ALMOST_TYPE_1,
        psm.SUBTYPE_MISC_VAYOMER,
        psm.SUBTYPE_MISC_ALMOST_TYPE_2,
    ):
        subtype_records = _subtype_records(survey, subtype)
        assert len(subtype_records) == _by_subtype_count(survey, subtype)
        assert all(
            one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in subtype_records
        )
    _misc_almost_type_1_inaugural(survey)
    misc_almost_type_2 = _misc_almost_type_2_inaugural(survey)
    assert _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_2) == 1
    assert (
        misc_almost_type_2["vowel"] == "ḥolam"
        and misc_almost_type_2["is_the_last_syllable"]
        and not misc_almost_type_2["syllable_is_open"]
        and not misc_almost_type_2["closes_on_a_guttural"]
    )
    misc_vayomer_records = _subtype_records(survey, psm.SUBTYPE_MISC_VAYOMER)
    assert len(misc_vayomer_records) == 4, misc_vayomer_records
    assert [
        one for one in post_stress if one.get("intervening_punctuation")
    ] == misc_vayomer_records
    assert all(
        one.get("intervening_punctuation") == [psm.PASEQ]
        and one.get("intervening_mam_punctuation") == [psm.PASEQ]
        and one["following_mam_form"] is not None
        for one in misc_vayomer_records
    )
    type_2_records = _type_2_records(survey)
    assert len(type_2_records) == _by_type_count(survey, psm.TYPE_GUTTURAL)
    assert all(
        record["closes_on_a_guttural"]
        and not record["syllable_is_open"]
        and record["vowel"] == "pataḥ"
        for record in type_2_records
    ), "the type-2/type-3 non-overlap claim has moved"
    assert all(
        record["syllables_after_the_stress"] == 1 for record in type_2_records
    ), "the type-2 penultimate-stress fact has moved"
    type_1_nonfinal_meteg_syllable_records = (
        _type_1_records_with_nonfinal_meteg_syllable(survey)
    )
    assert [record["bcv"] for record in type_1_nonfinal_meteg_syllable_records] == [
        "is63:12",
        "pr1:19",
        "pr11:26",
        "jb5:10",
    ]
    assert all(
        record["syllables_after_the_stress"] == 1
        and record["syllable_is_open"]
        and final_stress.ends_in_furtive_patax(record["chanted_word"])
        for record in type_1_nonfinal_meteg_syllable_records
    ), "the type-1 qualification for final furtive pataḥ has moved"
    type_2_type_3_overlap = _type_2_type_3_overlap(survey)
    assert type_2_type_3_overlap["chanted_words"] == 154
    assert type_2_type_3_overlap["by_book"] == {"da": 136, "er": 18}
    assert type_2_type_3_overlap["by_final_letter"] == {"ה": 154}
    assert {_type_2_following_group(record) for record in type_2_records} <= set(
        _TYPE_2_FOLLOWING_GROUPS
    )
    assert survey["post_silluq"]["in_mam"] == sum(
        1 for one in post_stress if one["has_sof_pasuq"]
    ), "the post-silluq count and the records disagree"
    post_silluq_forms = dict(_post_silluq_comparison(survey))
    assert post_silluq_forms["MAM"].count(psm.METEG) == 1
    assert post_silluq_forms["UXLC 3.9"].count(psm.METEG) == 2
    assert post_silluq_forms["WLC 4.22"].count(psm.METEG) == 2
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
    for bcv in (_M23_VERSE, _POST_SILLUQ_VERSE):
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


def itm() -> object:
    """The abbreviated book name, with Yeivin's title on hover."""
    return mb_html.abbr("ITM", {"title": _ITM_GLOSS})


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


def cos() -> object:
    """The abbreviated book name, with Breuer's title on hover."""
    return mb_html.abbr("CoS", {"title": _COS_GLOSS})


def _para(text: str) -> object:
    """One paragraph, its pointed Hebrew runs wrapped so they take the Hebrew font."""
    return mb_html.para(wrap_hebrew_runs(text))


def _hebrew_cell(form: str | None) -> tuple:
    """A pointed Hebrew form wrapped as an hbo run for an RTL table cell."""
    return wrap_hebrew_runs(form or "")


def _ref_link(bcv: str) -> object:
    """The reference, linked to the verse in MAM with doc."""
    bb, chnu, vrnu = _split(bcv)
    return mb_html.anchor_h(
        ref_abbrev(bcv), rtms_report.mam_with_doc_url(bb=bb, chnu=chnu, vrnu=vrnu)
    )


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


def _hebrew_spacing_option() -> object:
    """The page-wide control for the pointed Hebrew's letter spacing."""
    return mb_html.raw_html(_HEBREW_SPACING_OPTION)


# --- the sections --------------------------------------------------------------


def _opening(survey: dict) -> list:
    """Section 1: what is counted, and where the silluq boundary falls."""
    total = _both(survey, "meteg after the stressed syllable")
    return [
        mb_html.para(
            (
                "A meteg almost always comes before the stressed syllable of its chanted",
                " word, but it can also come after the stress. Both",
                *[" ", itm(), " and ", cos()],
                " discuss MAS (meteg after the stress). Neither book says how often MAS",
                " happens; we find that MAM has ",
                f"{total:,} of them.",
            )
        ),
        _para(
            "First, some definitions:"
            " a chanted word can be either a simple word"
            " (a word of just one atom)"
            " or it can be a compound word"
            " (a word of two or more atoms connected by maqaf marks)."
            " An atom is a sequence of letters uninterrupted by space, maqaf, or any other punctuation."
        ),
        _para(
            "The location of stress is not always obvious. For our survey of MAS, we"
            " locate stress using Phonetic MAM, an edition"
            " of MAM that marks the stressed syllable of every chanted word."
        ),
    ]


def _census(survey: dict) -> list:
    """Section 2: the counts, prose verses beside poetic verses."""
    categories = (
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    )
    before_category = "meteg before the stressed syllable"
    after_category = "meteg after the stressed syllable"
    headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation system"}),
        mb_html.abbr("c-words", {"title": "count of chanted words"}),
        mb_html.abbr("MBS", {"title": "Meteg before the stress"}),
        mb_html.abbr("MAS", {"title": "meteg after the stress"}),
        mb_html.abbr(
            "% MAS", {"title": "percentage of meteg marks that are after the stress"}
        ),
    )
    numeric = (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL)
    labels = {_PROSE: "prose", _POETIC: "poetic"}
    counts_by_system = {
        system: {category: _count(survey, system, category) for category in categories}
        for system in (_PROSE, _POETIC)
    }
    all_counts = {category: _both(survey, category) for category in categories}

    def row(label: str, counts: dict[str, int]) -> object:
        before = counts[before_category]
        after = counts[after_category]
        return mb_html.table_row_of_data(
            (
                label,
                *[f"{counts[category]:,}" for category in categories],
                f"{after / (before + after):.1%}",
            ),
            numeric,
        )

    rows = [
        row(labels[system], counts_by_system[system]) for system in (_PROSE, _POETIC)
    ]
    rows.append(row("all", all_counts))
    before = all_counts[before_category]
    after = all_counts[after_category]
    return [
        mb_html.heading_level_2("MAS census by cantillation system"),
        _table(headers, rows),
        _para(
            f"So a meteg comes before the stress {before:,} times and after it {after:,}"
            " times."
        ),
        mb_html.para(
            (
                "The prose row in the table above is for the 21 books plus the verses of"
                " Job's prose frame; the poetic row is for the verses of Job's main, poetic"
                " section plus all Psalms and the whole book of Proverbs. See the ",
                mb_html.anchor_h(
                    "appendix on dually-cantillated passages",
                    f"#{_DUAL_CANTILLATION_APPENDIX_ID}",
                ),
                " for how this census handles them.",
            )
        ),
    ]


def _by_type(survey: dict) -> list:
    """Section 3: the three types the two books describe, and what is left over."""
    headers = (
        "Type",
        "Prose",
        "Poetic",
        "Example",
    )
    type_2_count = _by_type_count(survey, psm.TYPE_GUTTURAL)
    type_1_nonfinal_meteg_syllable_records = (
        _type_1_records_with_nonfinal_meteg_syllable(survey)
    )
    type_2_type_3_overlap = _type_2_type_3_overlap(survey)
    chanted_word_count = _both(survey, "chanted words checked")
    overlap_count = type_2_type_3_overlap["chanted_words"]
    overlap_by_book = type_2_type_3_overlap["by_book"]
    rows = []
    for kind, (yeivin, breuer, _grading) in _TYPE_SOURCES.items():
        example = _example_of(survey, kind)
        rows.append(
            mb_html.table_row_of_data(
                (
                    _case_type_cell(kind),
                    str(survey["post_stress_by_structural_type"][_PROSE][kind]),
                    str(survey["post_stress_by_structural_type"][_POETIC][kind]),
                    _case_chanted_word_cell(example),
                ),
                (
                    None,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    _HEBREW_CELL,
                ),
            )
        )
    unclassified = psm.TYPE_UNCLASSIFIED
    rows.append(
        mb_html.table_row_of_data(
            (
                "misc",
                str(survey["post_stress_by_structural_type"][_PROSE][unclassified]),
                str(survey["post_stress_by_structural_type"][_POETIC][unclassified]),
                _case_chanted_word_cell(_example_of(survey, unclassified)),
            ),
            (
                None,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                _HEBREW_CELL,
            ),
        )
    )
    source_rows = [
        mb_html.table_row_of_data(
            (_case_type_cell(kind), itm_sections(yeivin), breuer),
            (None, None, None),
        )
        for kind, (yeivin, breuer, _grading) in _TYPE_SOURCES.items()
    ]
    return [
        mb_html.heading_level_2("MAS by structural type"),
        mb_html.para(
            (
                "Three types of MAS are described in both ",
                itm(),
                " and ",
                cos(),
                ". Each type has a condition on the syllable where the meteg falls;"
                " type 1 also has a condition on the following chanted word:",
            )
        ),
        mb_html.ordered_list(
            (
                "An open syllable before an initially-stressed word.",
                "A final syllable closed by a guttural.",
                "A final closed syllable whose vowel is tsere.",
            )
        ),
        _para(
            f"Types 2 and 3 could in principle overlap. In this survey, however, every one"
            f" of the {type_2_count} type-2 records has pataḥ rather than tsere, so no"
            " type-2 record also meets the type-3 condition."
        ),
        _para(
            f"Only {overlap_count:,} of all {chanted_word_count:,} chanted words surveyed"
            " have a final tsere syllable closed by a guttural. All "
            f"{overlap_count:,} occur in Aramaic and end in a mappiq he: "
            f"{overlap_by_book['da']:,} are in Daniel and {overlap_by_book['er']:,} are in Ezra."
        ),
        _hebrew_spacing_option(),
        _table(headers, rows),
        mb_html.heading_level_3("Sources for types 1–3"),
        _table(("Type", itm(), cos()), source_rows),
        mb_html.para(
            (
                "For the open-syllable type, ",
                itm(),
                " ",
                *itm_sections("§332"),
                " describes a chanted word stressed on its penultimate syllable,"
                " ending in an open syllable, before a chanted word whose first syllable is"
                " stressed."
                " Yeivin calls it rarely marked, commonest in early manuscripts and absent"
                " from printed texts, and ",
                cos(),
                " Ch. 8 grades it optional — which for Breuer means that no tradition"
                " settles it and each naqdan decided for himself.",
            )
        ),
        mb_html.para(
            "The survey counts a final furtive pataḥ as a syllable. On that syllable count,"
            " the survey's type 1 includes four chanted words that Yeivin's type 1 excludes:"
        ),
        mb_html.ordered_list(
            tuple(
                (
                    _ref_link(record["bcv"]),
                    " — ",
                    *_hebrew_cell(record["mam_form"] or record["chanted_word"]),
                    ".",
                )
                for record in type_1_nonfinal_meteg_syllable_records
            )
        ),
        mb_html.para(
            "In all four chanted words, the meteg follows the antepenultimate stress and"
            " falls on the penultimate open syllable. Yeivin's type 1 instead requires"
            " penultimate stress and a final open syllable. The four records belong to the"
            " survey's type 1 but not to Yeivin's type 1."
        ),
        mb_html.para(
            (
                "The guttural type is described in ",
                itm(),
                " ",
                *itm_sections("§354"),
                " and ",
                cos(),
                " Ch. 8 type (b), where the last syllable of the chanted word ends in ḥet,"
                " ayin or he. A furtive pataḥ counts as a separate syllable here, as it"
                " is in Phonetic MAM, so a meteg on that guttural comes out after the stress"
                " rather than in it. All ",
                str(type_2_count),
                " type-2 chanted words surveyed have penultimate stress, matching Yeivin's"
                " description. Penultimate stress is a fact about the ",
                str(type_2_count),
                " type-2 chanted words, not a further type-2 condition. Breuer calls the type"
                " obligatory; Yeivin's statement is"
                " narrower, that the mark is sometimes used when the chanted word after it"
                " begins with lamed or nun.",
            )
        ),
        mb_html.para(
            (
                "Type 3 follows Yeivin's tsere type, described in ",
                itm(),
                " ",
                *itm_sections("§338, fed by §308"),
                "'s account of retracted stress: where the stress retracts"
                " and a final closed syllable keeps its tsere, that syllable takes the mark,"
                " and Yeivin says it is marked in manuscripts and printed texts alike. ",
                cos(),
                " Ch. 8's corresponding type (a) is wider: it has a long vowel in a"
                " closed syllable. The one current record in Breuer's type (a) but not"
                " Yeivin's type has subtype ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_2,
                "; the ",
                mb_html.anchor_h("misc cases page", _MISC_FNAME),
                " lists that record.",
            )
        ),
    ]


def _case_list_link(survey: dict) -> list:
    """The main page's link to the long list of individual cases."""
    type_2_count = _by_type_count(survey, psm.TYPE_GUTTURAL)
    misc_count = _by_type_count(survey, psm.TYPE_UNCLASSIFIED)
    return [
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    f"{len(survey['post_stress']):,} individual cases", _CASES_FNAME
                ),
                " are listed separately and can be filtered by type.",
            )
        ),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(f"{misc_count:,} misc cases", _MISC_FNAME),
                " have a separate table and descriptions of the named misc subtypes.",
            )
        ),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(f"{type_2_count:,} type 2 cases", _TYPE_2_FNAME),
                " have a separate table whose filter uses the following chanted word's"
                " initial consonant.",
            )
        ),
    ]


def _case_type_code(kind: str) -> str:
    return _TYPE_CODES.get(kind, ("other", ""))[0]


def _case_type_cell(kind: str) -> object:
    if kind in _TYPE_CODES:
        code, gloss = _TYPE_CODES[kind]
        return mb_html.abbr(code, {"title": f"Type {code}: {gloss}"})
    return mb_html.abbr("—", {"title": "Not one of types 1, 2, or 3."})


def _case_subtype_cell(subtype: str | None) -> object:
    """The subtype only where a misc record has a named nearer condition."""
    if subtype is None:
        return ""
    gloss_by_subtype = {
        psm.SUBTYPE_MISC_ALMOST_TYPE_1: (
            "An open-syllable type-1 candidate whose following chanted word has no stress"
            " on its first syllable."
        ),
        psm.SUBTYPE_MISC_VAYOMER: (
            "A Vayomer case with one intervening paseq before the following chanted word."
        ),
        psm.SUBTYPE_MISC_ALMOST_TYPE_2: (
            "A final closed ḥolam syllable: Breuer's long-vowel type (a), but not"
            " Yeivin's tsere type 3."
        ),
    }
    return mb_html.abbr(
        subtype,
        {"title": gloss_by_subtype[subtype]},
    )


def _following_chanted_word_matters(record: dict) -> bool:
    """Whether the following chanted word supplies a type condition for this record."""
    return record["structural_type"] in (psm.TYPE_OPEN, psm.TYPE_GUTTURAL) or (
        record["subtype"] in (psm.SUBTYPE_MISC_ALMOST_TYPE_1, psm.SUBTYPE_MISC_VAYOMER)
    )


def _case_chanted_word_cell(record: dict) -> tuple:
    """The MAM form, with required following context demoted.

    The shared routine displays zero or more paseq marks and then the following chanted word.
    At present only the four ``misc-vayomer`` records have a paseq, but survey validation makes
    another kind of intervening material a reviewable failure rather than silently dropping it.
    """
    current = _hebrew_cell(record["mam_form"] or record["chanted_word"])
    if not _following_chanted_word_matters(record):
        return current
    following = record["following_mam_form"]
    assert following is not None, f"{record['bcv']}: no following MAM chanted word"
    punctuation = record.get("intervening_mam_punctuation", ())
    demoted = []
    for mark in punctuation:
        demoted.extend((*_hebrew_cell(mark), " "))
    demoted.extend(_hebrew_cell(following))
    return (
        *current,
        " ",
        mb_html.span(
            tuple(demoted),
            {"class": _FOLLOWING_CHANTED_WORD_CLASS},
        ),
    )


def _case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_case_type_cell(record["structural_type"])),
            mb_html.table_datum(_case_subtype_cell(record["subtype"])),
        ),
        {"data-type": _case_type_code(record["structural_type"])},
    )


def _case_type_filter(case_count: int) -> object:
    options = (
        ("all", "All types"),
        *((code, f"Type {code}") for code, _gloss in _TYPE_CODES.values()),
        ("other", "Not types 1, 2, or 3"),
    )
    option_html = "".join(
        f'<option value="{value}">{label}</option>' for value, label in options
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


def _type_2_following_group(record: dict) -> str:
    """The type-2 filter group set by the following chanted word's first consonant."""
    following = record["following_mam_form"]
    assert following is not None, f"{record['bcv']}: no following MAM chanted word"
    letters = hl.letters(following)
    assert letters, f"{record['bcv']}: no Hebrew letter in following MAM chanted word"
    initial = letters[0]
    return _TYPE_2_FOLLOWING_GROUP_BY_INITIAL.get(initial, "misc")


def _type_2_case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(
                _hebrew_cell(record["mam_form"] or record["chanted_word"]),
                _HEBREW_CELL,
            ),
            mb_html.table_datum(
                _following_example(record, psm.TYPE_GUTTURAL), _HEBREW_CELL
            ),
        ),
        {"data-following-initial": _type_2_following_group(record)},
    )


def _misc_case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_case_subtype_cell(record["subtype"])),
        )
    )


def _type_2_following_filter(case_count: int) -> object:
    options = (
        ("all", "All type 2 cases"),
        ("lamed", "Followed by lamed"),
        ("nun", "Followed by nun"),
        ("misc", "Followed by another consonant"),
    )
    option_html = "".join(
        f'<option value="{value}">{label}</option>' for value, label in options
    )
    return mb_html.raw_html(
        f'<p><label for="{_TYPE_2_FOLLOWING_FILTER_ID}">Show </label>'
        f'<select id="{_TYPE_2_FOLLOWING_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_TYPE_2_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def build_type_2_body(survey: dict) -> list:
    """The type-2 cases, grouped by the following chanted word's initial consonant."""
    rows = [_type_2_case_row(record) for record in _type_2_records(survey)]
    return [
        mb_html.heading_level_1(_TYPE_2_TITLE),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_TITLE, _FNAME),
                " or the ",
                mb_html.anchor_h(_CASES_TITLE.lower(), _CASES_FNAME),
                ".",
            )
        ),
        mb_html.heading_level_2("Every type 2 case in MAM"),
        _para(
            "Every row has a final guttural closing the last syllable of the first"
            " chanted word. The following chanted word has a separate column because its"
            " initial consonant selects the filter group."
        ),
        mb_html.para(
            (
                "Yeivin ",
                *itm_sections("§354"),
                " says this mark is sometimes used when the following chanted word begins"
                " with lamed or nun. The filter separates those two initial consonants from"
                " all others.",
            )
        ),
        _type_2_following_filter(len(rows)),
        _hebrew_spacing_option(),
        _table(
            ("Verse", "Chanted word", "Following chanted word"),
            rows,
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _TYPE_2_TABLE_ID,
            },
        ),
        mb_html.raw_html(_TYPE_2_FILTER_SCRIPT),
    ]


def build_misc_body(survey: dict) -> list:
    """The misc cases and the named subsets that remain outside types 1–3."""
    records = _misc_records(survey)
    almost_type_1_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_1)
    almost_type_1_inaugural = _misc_almost_type_1_inaugural(survey)
    misc_almost_type_2_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_2)
    misc_almost_type_2_inaugural = _misc_almost_type_2_inaugural(survey)
    vayomer_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_VAYOMER)
    return [
        mb_html.heading_level_1(_MISC_TITLE),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_TITLE, _FNAME),
                " or the ",
                mb_html.anchor_h(_CASES_TITLE.lower(), _CASES_FNAME),
                ".",
            )
        ),
        mb_html.heading_level_2("Every misc case in MAM"),
        _para(
            "Each chanted word in the table has MAS but does not meet the definition of"
            " types 1, 2, or 3. Gray following context appears where it is relevant to a"
            " named misc subtype."
        ),
        _hebrew_spacing_option(),
        _table(
            ("Verse", "Chanted word", "Subtype"),
            [_misc_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _MISC_TABLE_ID,
            },
        ),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_1,
                f" has {almost_type_1_count} record",
                "s" if almost_type_1_count != 1 else "",
                ". Its initial member is ",
                _ref_link(almost_type_1_inaugural["bcv"]),
                ": the MAS syllable is open, but the following chanted word's first"
                " syllable is unstressed. An opening simple vocal sheva or xataf vowel"
                " belongs to that first syllable for the type-1 condition.",
            )
        ),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_2,
                f" has {misc_almost_type_2_count} record",
                "s" if misc_almost_type_2_count != 1 else "",
                ". Its initial member is ",
                _ref_link(misc_almost_type_2_inaugural["bcv"]),
                ": its chanted word ",
                *_hebrew_cell(misc_almost_type_2_inaugural["mam_form"]),
                " has a final closed syllable with ḥolam, a long vowel. It fits Breuer's"
                " broader type (a), but not Yeivin's tsere type 3.",
            )
        ),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_VAYOMER,
                f" has {vayomer_count} record",
                "s" if vayomer_count != 1 else "",
                ". Each has one paseq between the meteg-bearing chanted word and the"
                " following chanted word: the gaʿya-before-paseq pattern described in ",
                itm(),
                " ",
                *itm_sections("§325"),
                ". The table above shows that context.",
            )
        ),
    ]


def build_cases_body(survey: dict) -> list:
    """The individual cases, outside the main page's explanatory sections."""
    headers = ("Verse", "Chanted word", "Type", "Subtype")
    rows = [_case_row(record) for record in survey["post_stress"]]
    return [
        mb_html.heading_level_1(_CASES_TITLE),
        mb_html.para(("← Back to ", mb_html.anchor_h(_TITLE, _FNAME), ".")),
        mb_html.heading_level_2("Every MAS in MAM"),
        _para(
            "In the order the corpus has them, prose verses and poetic verses together. Each"
            " reference links to the verse in MAM with doc, and each chanted word is MAM's"
            " text."
        ),
        _para(
            "For types 1 and 2, the following chanted word is shown in gray."
            " The same is true of misc-almost-type-1, because the following chanted"
            " word's stress keeps that row out of type 1. For misc-vayomer, the"
            " intervening paseq is gray with the following chanted word."
        ),
        mb_html.para(
            (
                "Type 2 has a ",
                mb_html.anchor_h("separate table", _TYPE_2_FNAME),
                " filtered by the following chanted word's initial consonant.",
            )
        ),
        _case_type_filter(len(rows)),
        _hebrew_spacing_option(),
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


def _m23(survey: dict) -> list:
    """Section 4: the Isaiah 23:12 suggestion, and what kind of meteg it added."""
    qumi = _focus_word(survey, _M23_VERSE, ("קומי",))
    yanuax = _record_at(survey, _M23_VERSE)
    same_shape = _same_shape_as_qumi(survey)
    open_count = _by_type_count(survey, psm.TYPE_OPEN)
    return [
        mb_html.heading_level_2(
            "A new MAS in MAM at Isaiah 23:12", {"id": M23_SECTION_ID}
        ),
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h("Holman M23 record", _HOLMAN_M23_RECORD_HREF),
                *wrap_hebrew_runs(
                    " has the MAM form Holman received on 2026-08-31, without a meteg where"
                    " the Aleppo Codex form has one. The suggestion was taken, so current MAM"
                    f" has the meteg under the mem of the chanted word {qumi} at Isaiah 23:12."
                ),
            )
        ),
        _para(
            f"The mark is of the open-syllable type: {qumi} is stressed on its first"
            " syllable, ends in an open syllable, and the chanted word after it is stressed"
            " on its first syllable. That is the type both books call optional, and"
            f" at {open_count} occurrences it is also the commonest of the three in MAM."
        ),
        _para(
            "The same verse already had another MAS:"
            f" {yanuax['mam_form']}, whose last syllable a guttural closes. So Isaiah 23:12"
            " now has two of them, one of each of the two commonest types."
        ),
        _para(
            "MAM has one other chanted word of exactly this shape, and the individual-cases"
            f" page names it: {same_shape['mam_form']} at {ref_abbrev(same_shape['bcv'])},"
            " with the same open final syllable and the same kind of chanted word after it."
        ),
        _para(
            f"The counts above do not include the meteg of {qumi}. They are taken from the"
            " Phonetic MAM edition, which has not been regenerated since MAM gained it, so"
            " Isaiah 23:12 is one of the verses where the two texts have parted."
        ),
    ]


def _record_at(survey: dict, bcv: str) -> dict:
    """The one post-stress record at a verse the page names, or a failure saying so."""
    records = [one for one in survey["post_stress"] if one["bcv"] == bcv]
    assert len(records) == 1, f"{bcv} has {len(records)} post-stress records, not one"
    return records[0]


def _same_shape_as_qumi(survey: dict) -> dict:
    """MAM's other open-syllable post-stress meteg on a chanted word whose letters are קומי.

    Found rather than named, so the sentence that calls it the only other one is checked by
    the search that produces it: two hits, or none, stop the build.
    """
    hits = [
        one
        for one in survey["post_stress"]
        if one["structural_type"] == psm.TYPE_OPEN
        and _letters_of(one["mam_form"] or one["chanted_word"]) == ("קומי",)
    ]
    assert len(hits) == 1, f"{len(hits)} chanted words of the M23 shape, not one"
    return hits[0]


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
    rows_at_verse = []
    for json_path in (paths.out_dir() / "wlc422").glob("1verses_*.json"):
        rows = json.loads(json_path.read_text(encoding="utf-8"))
        assert isinstance(rows, list), f"Expected a list in {json_path}"
        rows_at_verse.extend(
            row for row in rows if isinstance(row, dict) and row.get("bcv") == bcv
        )
    assert len(rows_at_verse) == 1, f"WLC 4.22: {len(rows_at_verse)} rows for {bcv}"
    vels = rows_at_verse[0].get("vels")
    assert isinstance(vels, list) and all(
        isinstance(atom, str) for atom in vels
    ), f"WLC 4.22 {bcv}: non-string vels"
    return [wlc_uword.uword(atom) for atom in vels]


def _post_silluq_comparison(survey: dict) -> tuple[tuple[str, str], ...]:
    """The three source-derived forms relevant to 1 Samuel 17:5's post-silluq question."""
    letters = ("נחשת",)
    return (
        (
            "MAM",
            _focus_word(survey, _POST_SILLUQ_VERSE, letters, must_have=psm.SOF_PASUQ),
        ),
        (
            "UXLC 3.9",
            _source_focus_word(
                _uxlc_words(_POST_SILLUQ_VERSE),
                _POST_SILLUQ_VERSE,
                letters,
                must_have=psm.SOF_PASUQ,
                source="UXLC 3.9",
            ),
        ),
        (
            "WLC 4.22",
            _source_focus_word(
                _wlc_words(_POST_SILLUQ_VERSE),
                _POST_SILLUQ_VERSE,
                letters,
                must_have=psm.SOF_PASUQ,
                source="WLC 4.22",
            ),
        ),
    )


def _post_silluq_lc_crop() -> object:
    """The directly inspectable LC line for 1 Samuel 17:5's post-silluq question."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_POST_SILLUQ_LC_CROP_URL}"'
        ' alt="Leningrad Codex, F159A, column 3, line 8: 1 Samuel 17:5."'
        ' loading="lazy"></a><figcaption>Leningrad Codex, F159A, column 3, line 8'
        " (1 Samuel 17:5); crop attached to "
        f'<a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">phonetic-hbo #78</a>.</figcaption></figure>'
    )


def _post_silluq(survey: dict) -> list:
    """Section 5: a meteg after the silluq, which MAM does not have."""
    comparison = _post_silluq_comparison(survey)
    comparison_rows = [
        mb_html.table_row_of_data((source, _hebrew_cell(form)), (None, _HEBREW_CELL))
        for source, form in comparison
    ]
    return [
        mb_html.heading_level_2("The post-silluq case at 1 Samuel 17:5"),
        _para(
            "A meteg after a silluq would be hard to identify in Unicode, since the two"
            " marks are one codepoint."
        ),
        _para(
            "MAM has no MAS on a silluq word, but 1 Samuel 17:5 does raise this issue in"
            " some BHS-derived editions."
        ),
        _table(("source", "verse-final chanted word"), comparison_rows),
        _para(
            "UXLC 3.9 and WLC 4.22 are BHS-derived transcriptions, and each has a second"
            " U+05BD on the final syllable. Their forms are evidence about UXLC and WLC."
            " The corresponding Leningrad Codex line, F159A, column 3, line 8, is"
            " reproduced below so that the manuscript marking can be inspected directly."
        ),
        _post_silluq_lc_crop(),
        _para(
            "Two of the three types could not occur on a silluq word: types 1 and 2 each"
            " require a following chanted word, which a verse-final chanted word does not"
            " have. Only type 3 could occur there."
        ),
    ]


def _overlapping_diagnostic(survey: dict) -> list:
    """The diagnostic that overlaps the positional categories."""
    overlap = _both(survey, "meteg sharing a letter with a non-stress-marking accent")
    return [
        mb_html.heading_level_2("A diagnostic overlapping the three positions"),
        _para(
            "One diagnostic overlaps the three positions rather than adding a fourth: a meteg"
            " can share a letter with an accent that marks no stress, which the prepositives,"
            " the postpositives, ole and geresh muqdam all do. There are"
            f" {overlap} such meteg marks, and each is counted in the group its syllable puts it"
            " in, before or after the stress, rather than beside them."
        ),
    ]


def _dual_cantillation_appendix(survey: dict) -> list:
    """The template-only comparison for Phonetic MAM's dual cantillation."""
    dual_cantillation = _dual_cantillation(survey)
    template_comparison = dual_cantillation["template_counts"]
    alef = template_comparison[psm.CANT_ALEF]
    bet = template_comparison[psm.CANT_BET]
    difference = dual_cantillation["meteg_before_stress_difference"]
    chanted_word_difference = dual_cantillation["chanted_word_count_difference"]
    headers = (
        "count",
        "cant-alef",
        "cant-bet",
    )
    categories = (
        ("Chanted words", "chanted words checked"),
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
    difference_headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation strand"}),
        mb_html.abbr("c-words", {"title": "the two relevant chanted words"}),
        mb_html.abbr("MBS", {"title": "meteg before the stress"}),
    )
    difference_rows = [
        mb_html.table_row_of_data(
            (
                psm.CANT_ALEF,
                _hebrew_cell(" ".join(difference[psm.CANT_ALEF]["chanted_words"])),
                "none",
            ),
            (None, _HEBREW_CELL, _NUMERIC_CELL),
        ),
        mb_html.table_row_of_data(
            (
                psm.CANT_BET,
                _hebrew_cell(" ".join(difference[psm.CANT_BET]["chanted_words"])),
                "one",
            ),
            (None, _HEBREW_CELL, _NUMERIC_CELL),
        ),
    ]
    chanted_word_difference_headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation strand"}),
        mb_html.abbr("c-words", {"title": "the relevant chanted words"}),
        "c-word count",
    )
    chanted_word_difference_rows = [
        mb_html.table_row_of_data(
            (
                cantillation,
                _hebrew_cell(
                    " ".join(
                        psm._bare(word)
                        for word in chanted_word_difference[cantillation][
                            "chanted_words"
                        ]
                    )
                ),
                str(len(chanted_word_difference[cantillation]["chanted_words"])),
            ),
            (None, _HEBREW_CELL, _NUMERIC_CELL),
        )
        for cantillation in (psm.CANT_ALEF, psm.CANT_BET)
    ]
    return [
        mb_html.heading_level_2(
            "Appendix: dually-cantillated passages",
            {"id": _DUAL_CANTILLATION_APPENDIX_ID},
        ),
        _para(
            "MAM has dual-cantillation templates in the two Decalogues and"
            " Genesis 35:22."
            " The analyses presented in this document use only the cant-alef"
            " branch of each template."
            " The table counts only the chanted words inside those templates, not every"
            " chanted word in the numbered verses that contain them."
            " The table below shows that this choice has no effect on the MAS count and"
            " changes the other two counts only by 1."
        ),
        _table(headers, rows),
        mb_html.para(
            (
                "Only ",
                _ref_link(chanted_word_difference["bcv"]),
                " differs in the number of chanted words. Cant-alef has two chanted words"
                " where cant-bet has one maqaf compound.",
            )
        ),
        _table(chanted_word_difference_headers, chanted_word_difference_rows),
        mb_html.para(
            (
                "Only ",
                _ref_link(difference["bcv"]),
                " differs in metegs before the stress. Cant-bet has one meteg before the"
                " stress in the chanted word below; cant-alef has the two chanted words"
                " below, neither with a meteg.",
            )
        ),
        _table(difference_headers, difference_rows),
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
