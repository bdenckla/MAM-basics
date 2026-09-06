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
_CASES_FNAME = site_data.POST_STRESS_METEG_CASES_FNAME
_CASES_TITLE = site_data.POST_STRESS_METEG_CASES_TITLE
_TYPE_2_FNAME = site_data.POST_STRESS_METEG_TYPE_2_FNAME
_TYPE_2_TITLE = site_data.POST_STRESS_METEG_TYPE_2_TITLE
_MISC_FNAME = site_data.POST_STRESS_METEG_MISC_FNAME
_MISC_TITLE = site_data.POST_STRESS_METEG_MISC_TITLE
_JEREMIAH_FOOTNOTE_ID = "footnote-1"
_DUAL_CANTILLATION_FOOTNOTE_ID = "footnote-2"
_TYPE_2_TYPE_3_FOOTNOTE_ID = "footnote-3"
_NONFINAL_MAS_FOOTNOTE_ID = "footnote-4"


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


def _visible_title(title: str, *, lowercase: bool = False) -> tuple:
    """A page title whose visible meteg is the standard italic romanization."""
    assert title.startswith("Meteg "), title
    return (_ROM_METEG if lowercase else _ROM_METEG_CAP, title.removeprefix("Meteg"))


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

# The one verse the page names outside its tables.  The survey records its chanted words as MAM
# has them today, under ``currency.focus_verses``, so the form shown here is lifted like every
# other form on the page.
_POST_SILLUQ_VERSE = "1s17:5"
_POST_SILLUQ_LC_CROP_URL = "img/LC-159A-col-3-line-8-1S-17v5.png"
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

_COS_PAGE_STARTS_BY_TYPE = {
    psm.TYPE_OPEN: "300; 354; 355",
    psm.TYPE_GUTTURAL: "299; 308; 309",
    psm.TYPE_CLOSED_TSERE: "299; 301; 302; 306; 307",
}
_COS_PAGE_GLOSS = "page number in Wengrov's English translation of CoS"

_TYPE_CODES = {
    psm.TYPE_OPEN: ("1", "the MAS is on an open final syllable"),
    psm.TYPE_GUTTURAL: ("2", "the word is closed by a guttural"),
    psm.TYPE_CLOSED_TSERE: (
        "3",
        "the MAS is on a closed, final, tsere-vowelled syllable",
    ),
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
_HEBREW_SPACING_OPTION = f"""<p><label><input type="checkbox" id="{_HEBREW_SPACING_CHECKBOX_ID}" checked>
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
        mb_html.heading_level_1(_visible_title(_TITLE)),
        *_opening(survey),
        *_census(survey),
        *_general_mas_facts(survey),
        *_by_type(survey),
        *_case_list_link(survey),
        *_post_silluq(survey),
        *_oleh_meteg_overlap(survey),
        *_sources_for_types(),
        *_footnotes(survey),
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


def _nonfinal_mas_syllable_records(survey: dict) -> list[dict]:
    """MAS records where a further final syllable follows the MAS syllable."""
    return [
        record for record in survey["post_stress"] if not record["is_the_last_syllable"]
    ]


def _noninitial_following_stress_records(survey: dict) -> list[dict]:
    """MAS records whose following chanted word does not have initial stress."""
    return [
        record
        for record in survey["post_stress"]
        if not record["following_chanted_word_is_initially_stressed"]
    ]


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
    """The only word that fits CoS's type (a), but not our tsere-restricted type 3: Job 15:35."""
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
    assert all(
        one.get("intervening_punctuation") == [psm.PASEQ]
        and one.get("intervening_mam_punctuation") == [psm.PASEQ]
        and one["following_mam_form"] is not None
        for one in misc_vayomer_records
    )
    type_2_records = _type_2_records(survey)
    assert len(type_2_records) == _by_type_count(survey, psm.TYPE_GUTTURAL)
    assert all(
        record["chanted_word_is_closed_by_a_guttural"]
        and record["following_chanted_word_is_initially_stressed"]
        for record in type_2_records
    ), "the type-2 guttural or following-stress fact has moved"
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
        and record["vowel"] == "ṣere"
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
        and record["vowel"] == "ṣere"
        and record["following_chanted_word_is_initially_stressed"]
        for record in type_3_records
    ), "the type-3 finality or following-stress fact has moved"
    type_1_records = [
        record for record in post_stress if record["structural_type"] == psm.TYPE_OPEN
    ]
    assert all(record["is_the_last_syllable"] for record in type_1_records)
    noninitial_following_stress_records = _noninitial_following_stress_records(survey)
    assert [
        (
            record["bcv"],
            record["mam_form"],
            record["following_mam_form"],
            record["structural_type"],
        )
        for record in noninitial_following_stress_records
    ] == [
        (
            "je46:14",
            "וְהַשְׁמִ֣יעֽוּ",
            "בְמִגְדּ֔וֹל",
            psm.TYPE_OPEN,
        )
    ], "the noninitial-following-stress exception has moved"
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
    type_2_following_group_counts = Counter(
        _type_2_following_group(record) for record in type_2_records
    )
    assert type_2_following_group_counts == Counter(
        lamed=38, guttural=17, resh=1, bet=2, mem=2
    )
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
    for bcv in (_POST_SILLUQ_VERSE,):
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
            "This checkbox controls whether Hebrew letter spacing is expanded in the table above"
            " as well as the whole document.",
        ).replace(
            "__TOGGLE_TEXT__",
            "Alternately, you can click on an individual Hebrew word to toggle only that word's"
            " spacing.",
        )
    )


# --- the sections --------------------------------------------------------------


def _opening(survey: dict) -> list:
    """Section 1: what is counted, and where the silluq boundary falls."""
    total = _both(survey, "meteg after the stressed syllable")
    return [
        mb_html.para(
            (
                "A ",
                _ROM_METEG,
                " almost always comes before the stressed syllable of its word, but it can"
                " also come after the stress. MAM has ",
                f"{total:,} cases of ",
                _ROM_METEG,
                " after the stress (MAS).",
            )
        ),
        mb_html.para(
            (
                'In this document, by "word" we mean a chanted word, which is either a simple'
                " word (having just one atom) or a compound word (having two or more atoms"
                " connected by ",
                _ROM_MAQAF,
                ' marks). By "atom", we mean a sequence of pointed letters uninterrupted by'
                " space, ",
                _ROM_MAQAF,
                ", or any other punctuation.",
            )
        ),
        _para(
            "The location of a word's stress is not always obvious. In this document, we locate"
            " stress using Phonetic MAM, an edition of MAM that marks the stress of every word"
            " in MAM."
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
        mb_html.para(
            (
                "So a ",
                _ROM_METEG,
                f" comes before the stress {before:,} times and after it {after:,} times.",
            )
        ),
        mb_html.para(
            (
                "The prose row in the table above is for the 21 books plus the verses of"
                " Job's prose frame; the poetic row is for the verses of Job's main, poetic"
                " section plus all Psalms and the whole book of Proverbs. Only one"
                " cantillation (",
                _footnote_callout(2, _DUAL_CANTILLATION_FOOTNOTE_ID),
                ") of dually cantillated passages participates in every analysis on this"
                " page, including the census above.",
            )
        ),
    ]


def _general_mas_facts(survey: dict) -> list:
    """Section 3: the facts shared by every MAS, before structural classification."""
    exceptions = _noninitial_following_stress_records(survey)
    assert len(exceptions) == 1
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert len(nonfinal_mas_syllable_records) == 4
    return [
        mb_html.heading_level_2("General facts about MAS"),
        mb_html.unordered_list(
            (
                "In every MAS case, the MAS immediately follows the stress syllable, which"
                " has a conjunctive accent.",
                (
                    "In every MAS case but one (",
                    _footnote_callout(1, _JEREMIAH_FOOTNOTE_ID),
                    "), the following chanted word has initial stress.",
                ),
                (
                    "In every MAS case except four (",
                    _footnote_callout(4, _NONFINAL_MAS_FOOTNOTE_ID),
                    "), the MAS syllable is final.",
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
    for kind, (yeivin, breuer, _grading) in _TYPE_SOURCES.items():
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
    return [
        mb_html.heading_level_2("MAS by structural type"),
        mb_html.para(
            f"All but {unclassified_count} cases of MAS can be sorted into one of the three"
            " following types:"
        ),
        mb_html.unordered_list(
            (
                "In type 1, the MAS is on an open final syllable.",
                "In type 2, the word is closed by a guttural.",
                (
                    "In type 3, the MAS is on a closed, final, ",
                    _ROM_TSERE,
                    "-vowelled syllable. (",
                    _footnote_callout(3, _TYPE_2_TYPE_3_FOOTNOTE_ID),
                    ")",
                ),
            )
        ),
        _table(headers, rows),
        _hebrew_spacing_option(),
    ]


def _sources_for_types() -> list:
    """The references for the three types, kept at the main page's end."""
    source_rows = [
        mb_html.table_row_of_data(
            (
                _case_type_cell(kind),
                itm_sections(yeivin),
                breuer,
                _COS_PAGE_STARTS_BY_TYPE[kind],
            ),
            (None, None, None, None),
        )
        for kind, (yeivin, breuer, _grading) in _TYPE_SOURCES.items()
    ]
    return [
        mb_html.heading_level_3("Sources for types 1–3"),
        mb_html.para(
            (
                "The three types of MAS are described in both ",
                itm(),
                " and ",
                cos(),
                ". Exactly what words are included and excluded in these three types vary"
                " between ITM, CoS, and our document here, but they broadly agree.",
            )
        ),
        _table(
            (
                "Type",
                itm(),
                cos(),
                mb_html.abbr("CoS-pg", {"title": _COS_PAGE_GLOSS}),
            ),
            source_rows,
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


def _case_type_cell(
    kind: str, *, unqualified_word: bool = False, misc_label: bool = False
) -> object:
    """A type label, with the subpages' shorter vocabulary and misc label when requested."""
    if kind in _TYPE_CODES:
        code, gloss = _TYPE_CODES[kind]
        if unqualified_word:
            gloss = gloss.replace("chanted word", "word")
        return mb_html.abbr(code, {"title": f"Type {code}: {gloss}"})
    if misc_label:
        return "misc"
    return mb_html.abbr("—", {"title": "Not one of types 1, 2, or 3."})


def _case_subtype_cell(subtype: str | None) -> object:
    """The subtype only where a misc record has a named nearer condition."""
    if subtype is None:
        return ""
    gloss_by_subtype = {
        psm.SUBTYPE_MISC_VAYOMER: (
            "A Vayomer case with one intervening paseq before the following word."
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


def _following_chanted_word_span(
    following: str, punctuation: tuple[str, ...] | list[str] = ()
) -> object:
    """The following chanted word, and any preceding punctuation, in gray."""
    demoted = []
    for mark in punctuation:
        demoted.extend((*_hebrew_cell(mark), " "))
    demoted.extend(_hebrew_cell(following))
    return mb_html.span(
        tuple(demoted),
        {"class": _FOLLOWING_CHANTED_WORD_CLASS},
    )


def _case_chanted_word_cell(record: dict) -> tuple:
    """The MAM MAS form followed by its next chanted word in gray."""
    current = _hebrew_cell(record["mam_form"] or record["chanted_word"])
    following = record["following_mam_form"]
    assert following is not None, f"{record['bcv']}: no following MAM chanted word"
    return (
        *current,
        " ",
        _following_chanted_word_span(
            following,
            record.get("intervening_mam_punctuation", ()),
        ),
    )


def _oleh_chanted_word_cell(record: dict) -> tuple:
    """The oleh context, extending into the next chanted word only for a yored there."""
    current_form = record["mam_form"] or record["chanted_word"]
    current = _hebrew_cell(current_form)
    if ha.MER in current_form:
        return current
    following = record["following_mam_form"]
    assert following is not None, f"{record['bcv']}: no MAM form following oleh"
    assert ha.MER in following, f"{record['bcv']}: no yored after oleh"
    return (
        *current,
        " ",
        _following_chanted_word_span(
            following, record.get("intervening_mam_punctuation", ())
        ),
    )


def _case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(
                _case_type_cell(
                    record["structural_type"], unqualified_word=True, misc_label=True
                )
            ),
            mb_html.table_datum(_case_subtype_cell(record["subtype"])),
        ),
        {"data-type": _case_type_code(record["structural_type"])},
    )


def _case_type_filter(case_count: int) -> object:
    options = (
        ("all", "All types"),
        *((code, f"Type {code}") for code, _gloss in _TYPE_CODES.values()),
        ("other", "misc"),
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
    """The detailed type-2 group set by the following chanted word's first consonant."""
    following = record["following_mam_form"]
    assert following is not None, f"{record['bcv']}: no following MAM chanted word"
    return psm.type_2_following_filter_group(following)


def _type_2_filter_group(record: dict) -> str:
    """The coarser type-2 filter group shown on the cases page."""
    detailed_group = _type_2_following_group(record)
    if detailed_group in ("lamed", "guttural"):
        return detailed_group
    return "not-lamed-or-guttural"


def _type_2_case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(
                _case_chanted_word_cell(record),
                _HEBREW_CELL,
            ),
        ),
        {"data-following-initial": _type_2_filter_group(record)},
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
        ("lamed", "Followed by ל"),
        ("guttural", "Followed by guttural"),
        ("not-lamed-or-guttural", "Not followed by ל or a gutt."),
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
    records = _type_2_records(survey)
    rows = [_type_2_case_row(record) for record in records]
    return [
        mb_html.heading_level_1(_visible_title(_TYPE_2_TITLE)),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
                " or the ",
                mb_html.anchor_h(
                    _visible_title(_CASES_TITLE, lowercase=True), _CASES_FNAME
                ),
                ".",
            )
        ),
        mb_html.heading_level_2("Every type 2 case in MAM"),
        _type_2_following_filter(len(rows)),
        _table(
            ("Verse", "Word"),
            rows,
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _TYPE_2_TABLE_ID,
            },
        ),
        _hebrew_spacing_option(),
        mb_html.raw_html(_TYPE_2_FILTER_SCRIPT),
    ]


def build_misc_body(survey: dict) -> list:
    """The misc cases and the named subsets that remain outside types 1–3."""
    records = _misc_records(survey)
    misc_almost_type_3_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3)
    misc_almost_type_3_only_member = _misc_almost_type_3_only_member(survey)
    vayomer_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_VAYOMER)
    return [
        mb_html.heading_level_1(_visible_title(_MISC_TITLE)),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
                " or the ",
                mb_html.anchor_h(
                    _visible_title(_CASES_TITLE, lowercase=True), _CASES_FNAME
                ),
                ".",
            )
        ),
        mb_html.heading_level_2("Every misc case in MAM"),
        _para(
            "Each word in the table has MAS but does not meet the definition of"
            " types 1, 2, or 3. The next chanted word is gray."
        ),
        _table(
            ("Verse", "Word", "Subtype"),
            [_misc_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _MISC_TABLE_ID,
            },
        ),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_3,
                f" has {misc_almost_type_3_count} word",
                "s" if misc_almost_type_3_count != 1 else "",
                ". Its only member is ",
                _ref_link(misc_almost_type_3_only_member["bcv"]),
                ": its word ",
                *_case_chanted_word_cell(misc_almost_type_3_only_member),
                " has a final closed syllable with ",
                _ROM_HOLAM,
                ", a long vowel. It fits ",
                cos(),
                "'s broader type (a), but not our type 3, which is restricted to ",
                _ROM_TSERE,
                ".",
            )
        ),
        mb_html.para(
            (
                "Within misc, the ",
                _ROM_VAYOMER,
                " subset",
                f" has {vayomer_count} word",
                "s" if vayomer_count != 1 else "",
                ". Each has one ",
                _ROM_PASEQ,
                " between the ",
                _ROM_METEG,
                "-bearing word and the following word: the ",
                _ROM_GAYA,
                "-before-",
                _ROM_PASEQ,
                " pattern described in ",
                itm(),
                " ",
                *itm_sections("§325"),
                ". The table above shows that context.",
            )
        ),
    ]


def build_cases_body(survey: dict) -> list:
    """The individual cases, outside the main page's explanatory sections."""
    headers = ("Verse", "Word", "Type", "Subtype")
    rows = [_case_row(record) for record in survey["post_stress"]]
    return [
        mb_html.heading_level_1(_visible_title(_CASES_TITLE)),
        mb_html.para(
            ("← Back to ", mb_html.anchor_h(_visible_title(_TITLE), _FNAME), ".")
        ),
        mb_html.heading_level_2("Every MAS in MAM"),
        _para(
            "In the order the corpus has them, prose verses and poetic verses together. Each"
            " reference links to the verse in MAM with doc, and each word is MAM's"
            " text followed by the next chanted word in gray."
        ),
        mb_html.para(
            (
                "For misc-",
                _ROM_VAYOMER,
                ", the intervening ",
                _ROM_PASEQ,
                " is gray with the following word.",
            )
        ),
        mb_html.para(
            (
                "Type 2 has a ",
                mb_html.anchor_h("separate table", _TYPE_2_FNAME),
                " filtered by the following word's initial consonant.",
            )
        ),
        _case_type_filter(len(rows)),
        _table(
            headers,
            rows,
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _CASE_TABLE_ID,
            },
        ),
        _hebrew_spacing_option(),
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
    """The MAM and BHS forms relevant to 1 Samuel 17:5's post-silluq question."""
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
    """A Leningrad meteg after silluq, which the MAM form does not have."""
    comparison = _post_silluq_comparison(survey)
    comparison_rows = [
        mb_html.table_row_of_data((source, _hebrew_cell(form)), (None, _HEBREW_CELL))
        for source, form in comparison
    ]
    return [
        mb_html.heading_level_2(
            ("A ", _ROM_METEG, " after ", _ROM_SILLUQ, " in Leningrad")
        ),
        mb_html.para(
            (
                "In the Leningrad Codex, the last chanted word of 1 Samuel 17:5 seems to"
                " have a ",
                _ROM_METEG,
                " after its ",
                _ROM_SILLUQ,
                ".",
            )
        ),
        _post_silluq_lc_crop(),
        mb_html.para(
            (
                "Although that ",
                _ROM_METEG,
                " is pretty surprising, we deem it less surprising than if we interpret the"
                " marks in ",
                _ROM_METEG,
                "-",
                _ROM_SILLUQ,
                " order. In ",
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
        mb_html.heading_level_2(
            ("The ", _ROM_METEG, " sharing a letter with ", _ROM_OLEH)
        ),
        mb_html.para(
            (
                f"{len(oleh_overlaps)} ",
                _ROM_METEG,
                " marks share a letter with ",
                _ROM_OLEH,
                ". The table labels each ",
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
                " the chanted word, as it is in the MAS rows above. In other words, a MAS"
                " chanted word with a ",
                _ROM_METEG,
                ' might at first look like some weird "',
                _ROM_METEG,
                ' on the stress" (neither before nor after), but it is not!',
            )
        ),
    ]


def _footnotes(survey: dict) -> list:
    """The exceptions and methods the page marks with its phi callouts."""
    exceptions = _noninitial_following_stress_records(survey)
    assert len(exceptions) == 1
    exception = exceptions[0]
    return [
        mb_html.heading_level_2("Footnotes"),
        mb_html.heading_level_3(
            ("φ1 — ", _ref_link(exception["bcv"])), {"id": _JEREMIAH_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(exception["bcv"]),
                ", the following chanted word lacks initial stress: ",
                *_case_chanted_word_cell(exception),
                ".",
            )
        ),
        *_dual_cantillation_footnote(survey),
        *_type_2_type_3_footnote(survey),
        *_nonfinal_mas_syllable_footnote(survey),
    ]


def _dual_cantillation_footnote(survey: dict) -> list:
    """Footnote 2: the template-only comparison for Phonetic MAM's dual cantillation."""
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
                    " ".join(
                        psm._bare(word)
                        for word in chanted_word_difference[cantillation][
                            "chanted_words"
                        ]
                    )
                ),
            ),
            (None, _HEBREW_CELL),
        )
        for cantillation in (psm.CANT_ALEF, psm.CANT_BET)
    ]
    return [
        mb_html.heading_level_3(
            "φ2 — Dually cantillated passages",
            {"id": _DUAL_CANTILLATION_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "MAM has dual-cantillation templates in the two Decalogues and Genesis"
                " 35:22. The analyses presented in this document use only the ",
                _cantillation_label(psm.CANT_ALEF),
                " branch of each template. The table below shows that this choice has no"
                " effect on the MAS count and changes the other two counts only by 1.",
            )
        ),
        _table(headers, rows),
        mb_html.para(
            (
                "Only ",
                _ref_link(chanted_word_difference["bcv"]),
                " differs in the number of chanted words. ",
                _cantillation_label(psm.CANT_ALEF),
                " has two chanted words where ",
                _cantillation_label(psm.CANT_BET),
                " has one ",
                _ROM_MAQAF,
                " compound.",
            )
        ),
        mb_html.table(
            chanted_word_difference_rows,
            {"class": "limited-width post-stress-meteg-table"},
        ),
        mb_html.para(
            (
                "Only ",
                _ref_link(difference["bcv"]),
                " differs in ",
                _ROM_METEG,
                "s before the stress. ",
                _cantillation_label(psm.CANT_BET),
                " has one ",
                _ROM_METEG,
                " before the stress in the chanted word below; ",
                _cantillation_label(psm.CANT_ALEF),
                " has the two chanted words below, neither with a ",
                _ROM_METEG,
                ".",
            )
        ),
        mb_html.table(
            difference_rows, {"class": "limited-width post-stress-meteg-table"}
        ),
    ]


def _type_2_type_3_footnote(survey: dict) -> list:
    """Footnote 3: why types 2 and 3 do not overlap in the current survey."""
    type_2_records = _type_2_records(survey)
    type_2_count = _by_type_count(survey, psm.TYPE_GUTTURAL)
    type_2_final_mas_count = sum(
        record["is_the_last_syllable"] for record in type_2_records
    )
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    overlap = _type_2_type_3_overlap(survey)
    chanted_word_count = _both(survey, "chanted words checked")
    overlap_count = overlap["chanted_words"]
    overlap_by_book = overlap["by_book"]
    overlap_example = overlap["example"]
    return [
        mb_html.heading_level_3(
            "φ3 — Types 2 and 3", {"id": _TYPE_2_TYPE_3_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                f"Types 2 and 3 could in principle overlap. In this survey, however, {type_2_final_mas_count}"
                f" of the {type_2_count} type-2 MAS syllables have ",
                _ROM_PATAH,
                ", while the other ",
                f"{len(nonfinal_mas_syllable_records)} have ",
                _ROM_TSERE,
                " and are not only open but also nonfinal. Thus no type-2 MAS meets the"
                " type-3 condition. Indeed, chanted words with a final ",
                _ROM_TSERE,
                " syllable closed by a guttural are quite rare even without a ",
                _ROM_METEG,
                ". Only ",
                f"{overlap_count:,} of all {chanted_word_count:,} chanted words surveyed have"
                " a final ",
                _ROM_TSERE,
                " syllable closed by a guttural. All ",
                f"{overlap_count:,} occur in Aramaic and end in a ",
                _ROM_MAPPIQ,
                " ",
                _ROM_HE,
                f": {overlap_by_book['da']:,} are in Daniel and "
                f"{overlap_by_book['er']:,} are in Ezra. An example is as follows:",
            )
        ),
        mb_html.para(
            (
                _ref_link(overlap_example["bcv"]),
                " — ",
                *wrap_hebrew_runs(overlap_example["mam_form"]),
            ),
            {"class": "center"},
        ),
    ]


def _nonfinal_mas_syllable_footnote(survey: dict) -> list:
    """Footnote 4: the four nonfinal MAS syllables."""
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert len(nonfinal_mas_syllable_records) == 4
    return [
        mb_html.heading_level_3(
            "φ4 — The four nonfinal MAS syllables", {"id": _NONFINAL_MAS_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                "The other four records are type 2: each has an open penultimate ",
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
