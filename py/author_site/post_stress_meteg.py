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

from pathlib import Path

from accgram import post_stress_meteg as psm
from author_site import site_data
from author_site import post_stress_meteg_annotations
from author_site import post_stress_meteg_appendices as _appendices_module
from author_site import post_stress_meteg_cases as _cases_module
from author_site import post_stress_meteg_overview as _overview_module
from author_site import post_stress_meteg_post_silluq_data as _post_silluq_data_module
from author_site import post_stress_meteg_post_silluq_page as _post_silluq_page_module
from author_site import post_stress_meteg_shared as _shared_module
from author_site import post_stress_meteg_survey as _survey_module
from author_site import post_stress_meteg_validation as _validation_module
from mb_author import author
from mb_cmn import paths
from mb_cmn import provenance
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _CASES_FNAME,
    _CASES_TITLE,
    _CHRONICLES_8_11_FNAME,
    _CHRONICLES_8_11_TITLE,
    _FNAME,
    _HEBREW_SPACING_BODY_CLASS,
    _LACKS_MAS_FNAME,
    _LACKS_MAS_TITLE,
    _METHODS_FNAME,
    _METHODS_TITLE,
    _MISC_FNAME,
    _MISC_TITLE,
    _NEXT_CONJUNCTIVE_FNAME,
    _NEXT_CONJUNCTIVE_TITLE,
    _NOT_FIT_FNAME,
    _NOT_FIT_TITLE,
    _PHONETIC_MAM_URL,
    _POST_SILLUQ_FNAME,
    _POST_SILLUQ_TITLE,
    _POST_SILLUQ_VERSE,
    _ROM_METEG,
    _ROM_METEG_CAP,
    _ROM_SILLUQ,
    _TITLE,
    _hebrew_spacing_option,
    _visible_title,
    chb,
    cos,
    itm,
    itm_sections,
)

from author_site.post_stress_meteg_cases import (
    build_cases_body,
    build_lacks_mas_body,
    build_misc_body,
    build_not_fit_body,
)

from author_site.post_stress_meteg_post_silluq_data import (
    _mam_post_silluq_statement,
    _post_silluq_comparison,
    _uxlc_words,
    _verse_final_chanted_word,
    load_post_silluq_cases,
    load_post_silluq_koren_observations,
)

from author_site.post_stress_meteg_post_silluq_page import (
    build_post_silluq_body,
)

from author_site.post_stress_meteg_validation import (
    pin_claims,
)

from author_site.post_stress_meteg_overview import (
    _by_type,
    _case_list_link,
    _census,
    _census_definitions,
    _mas_facts,
    _opening,
    _type_1_subtypes,
    _type_2_facts,
)

from author_site.post_stress_meteg_appendices import (
    _dually_cantillated_passages,
    _fit_for_mas_facts,
    _footnotes,
    _oleh_meteg_overlap,
    build_chronicles_8_11_body,
    build_next_conjunctive_body,
)

__all__ = (
    "assert_no_phonetic_mam_annotations",
    "build_body",
    "build_cases_body",
    "build_chronicles_8_11_body",
    "build_lacks_mas_body",
    "build_methods_body",
    "build_misc_body",
    "build_next_conjunctive_body",
    "build_not_fit_body",
    "build_post_silluq_body",
    "chb",
    "cos",
    "gen_html_files",
    "itm",
    "itm_sections",
    "load_post_silluq_cases",
    "load_post_silluq_koren_observations",
    "pin_claims",
)


_AUTHOR_SOURCE_PATHS = (
    Path(__file__),
    *(
        Path(module.__file__)
        for module in (
            _shared_module,
            _survey_module,
            _cases_module,
            _post_silluq_data_module,
            _post_silluq_page_module,
            _validation_module,
            _overview_module,
            _appendices_module,
        )
    ),
)


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
        case["bcv"]: _verse_final_chanted_word(
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
        _AUTHOR_SOURCE_PATHS,
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
