"""Supporting pages and footnotes for the post-stress-meteg pages."""

from __future__ import annotations


from accgram import post_stress_meteg_model as psm
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from mb_author import author
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _CHRONICLES_8_11_ALEPPO_CROP_URL,
    _CHRONICLES_8_11_FNAME,
    _CHRONICLES_8_11_L1,
    _CHRONICLES_8_11_L2,
    _CHRONICLES_8_11_LENINGRAD_CROP_URL,
    _CHRONICLES_8_11_LENINGRAD_GLOSSES,
    _CHRONICLES_8_11_LENINGRAD_NEXT_WORD,
    _CHRONICLES_8_11_REF,
    _CHRONICLES_8_11_TITLE,
    _CHRONICLES_8_11_VERSE,
    _FIT_FOR_MAS_CRITERIA,
    _FIT_FOR_MAS_SECTION_ID,
    _FIT_FOR_MAS_TYPE_CRITERION,
    _FIT_TYPE_2_NO_IVS_FOOTNOTE_ID,
    _FNAME,
    _HEBREW_CELL,
    _JEREMIAH_FOOTNOTE_ID,
    _LACKS_MAS_FNAME,
    _METHODS_FNAME,
    _NEXT_CONJUNCTIVE_FNAME,
    _NEXT_CONJUNCTIVE_FOOTNOTE_ID,
    _NEXT_CONJUNCTIVE_TITLE,
    _NONFINAL_MAS_FOOTNOTE_ID,
    _NOT_FIT_FNAME,
    _NUMERIC_CELL,
    _PASHTA_STRESS_HELPER_FOOTNOTE_ID,
    _POST_SILLUQ_FNAME,
    _POST_SILLUQ_FOOTNOTE_ID,
    _ROM_HE,
    _ROM_MAPPIQ,
    _ROM_METEG,
    _ROM_METEG_CAP,
    _ROM_METEG_MERKHA,
    _ROM_OLEH,
    _ROM_PASHTA,
    _ROM_PATAH,
    _ROM_SHEWA,
    _ROM_SILLUQ,
    _ROM_TSERE,
    _TITLE,
    _TYPE_2_TYPE_3_FOOTNOTE_ID,
    _VOCAL_SHEWA_FOOTNOTE_ID,
    _cantillation_label,
    _footnote_callout,
    _hebrew_cell,
    _hebrew_spacing_option,
    _ref_link,
    _singleton_example_table,
    _spelled,
    _table,
    _visible_title,
)

from author_site.post_stress_meteg_survey import (
    _by_type_count,
    _dual_cantillation,
    _fit_for_mas,
    _next_conjunctive_records,
    _nonfinal_mas_syllable_records,
    _noninitial_next_stress_records,
    _not_fit_for_mas_records,
    _type_2_type_3_overlap,
)

from author_site.post_stress_meteg_cases import (
    _case_chanted_word_cell,
    _case_filter_subtype,
    _case_type_code,
    _fit_type_cell,
    _oleh_chanted_word_cell,
    _paired_chanted_word_cell,
    _type_2_records,
)

from author_site.post_stress_meteg_post_silluq_data import (
    _letters_of,
    _mam_post_silluq_statement,
)

from author_site.post_stress_meteg_overview import (
    _sources_for_types_footnote,
)


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
