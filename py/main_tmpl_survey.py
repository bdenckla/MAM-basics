"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

import argparse
import json
import os

from tmpl_survey import nesting_normal_form
from tmpl_survey import survey_dot
from tmpl_survey import survey_plain
from tmpl_survey import survey_plus
from mb_cmn import file_io

_PLAIN_OUT_DIR = "out/tmpl-survey-plain"
_PLUS_OUT_DIR = "out/tmpl-survey-plus"
_PLAIN_SVG_DIR = "../MAM-parsed/gh-pages/plain/svg"
_PLUS_SVG_DIR = "../MAM-parsed/gh-pages/plus/svg"
_PLAIN_EXPANDED_STACK_GRAMMAR_LOCK_PATH = (
    "py/tmpl_survey/expanded_stack_grammar_plain.lock.json"
)
_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH = (
    "py/tmpl_survey/expanded_stack_grammar_plus.lock.json"
)
_PLAIN_TMPL_NAME_NORMALIZATION_NOTE = (
    "In the plain survey, template names are normalized: ASCII double quote "
    '(") is converted to Hebrew gershayim (U+05F4). This applies to both '
    "stmpl and tmpl template forms in plain data."
)


def _default_case_rank_groups():
    default_groups = nesting_normal_form.default_rank_groups()

    plus_e_group_names = {
        label: set(names) for label, names in default_groups
    }
    # plus-E custom normal order relative to defaults:
    # - add targeted note template to dehi rank (rank 5 in 1-based numbering)
    # - add plus-only ketiv/qere variants to the ketiv/qere rank (rank 3)
    plus_e_group_names["e"].add("מ:הערה-2")
    plus_e_group_names["c"].update({"מ:כו״ק מיוחד", "מ:קו״כ-אם-2", "קו״כ"})
    plus_e_groups = tuple(
        (label, frozenset(plus_e_group_names[label]))
        for label, _names in default_groups
    )

    return {
        "plain-C": default_groups,
        "plain-D": default_groups,
        "plain-E": default_groups,
        "plus-C": default_groups,
        "plus-D": default_groups,
        "plus-E": plus_e_groups,
    }


_NORMAL_FORM_CASE_RANK_GROUPS = _default_case_rank_groups()


def _case_rank_maps(case_rank_groups):
    return {
        case_key: nesting_normal_form.build_rank_map(rank_groups)
        for case_key, rank_groups in case_rank_groups.items()
    }


def _with_tmpl_name_normalization_note(result, note_text):
    note_key = "template_name_normalization_note"
    assert note_key not in result
    return {note_key: note_text, **result}


def _write_outputs(
    result,
    raw_stack_counts,
    stem,
    svg_stem=None,
    normalization_note=None,
    discarded=None,
):
    os.makedirs(os.path.dirname(stem), exist_ok=True)
    if svg_stem is not None:
        os.makedirs(os.path.dirname(svg_stem), exist_ok=True)
    result_with_note = result
    if normalization_note is not None:
        result_with_note = _with_tmpl_name_normalization_note(
            result, normalization_note
        )
    file_io.json_dump_to_file_path(
        result_with_note,
        f"{stem}.json",
        generator_file=__file__,
    )
    dot_path = f"{stem}-call-graph.dot"
    if svg_stem is None:
        svg_stem = stem
    svg_path = f"{svg_stem}-call-graph.svg"
    survey_dot.write_dot_file(
        raw_stack_counts,
        dot_path,
        discarded=discarded,
        generator_file=__file__,
    )
    survey_dot.render_svg(dot_path, svg_path, generator_file=__file__)
    edge_mode_dot_path = f"{stem}-call-graph-templates-as-edges.dot"
    edge_mode_svg_path = f"{svg_stem}-call-graph-templates-as-edges.svg"
    survey_dot.write_edge_template_dot_file(
        raw_stack_counts,
        edge_mode_dot_path,
        discarded=discarded,
        generator_file=__file__,
    )
    survey_dot.render_svg(
        edge_mode_dot_path,
        edge_mode_svg_path,
        generator_file=__file__,
    )
    survey_dot.write_focused_dot_files(
        raw_stack_counts,
        stem,
        svg_stem=svg_stem,
        generator_file=__file__,
        discarded=discarded,
    )


def _read_json_file(path):
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def _write_expanded_stack_grammar_locks(plain_grammar, plus_grammar):
    file_io.json_dump_to_file_path(
        plain_grammar,
        _PLAIN_EXPANDED_STACK_GRAMMAR_LOCK_PATH,
        generator_file=__file__,
    )
    file_io.json_dump_to_file_path(
        plus_grammar,
        _PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH,
        generator_file=__file__,
    )


def _assert_with_expanded_stack_grammar_locks(
    plain_raw_sc,
    plus_raw_sc,
    write_expanded_stack_grammar_locks=False,
):
    plain_inferred_grammar = nesting_normal_form.infer_expanded_stack_grammar(plain_raw_sc)
    plus_inferred_grammar = nesting_normal_form.infer_expanded_stack_grammar(plus_raw_sc)

    if write_expanded_stack_grammar_locks:
        _write_expanded_stack_grammar_locks(
            plain_inferred_grammar,
            plus_inferred_grammar,
        )

    missing_paths = [
        path
        for path in (
            _PLAIN_EXPANDED_STACK_GRAMMAR_LOCK_PATH,
            _PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH,
        )
        if not os.path.exists(path)
    ]
    if missing_paths:
        missing = ", ".join(missing_paths)
        raise FileNotFoundError(
            "Expanded stack grammar lock file(s) not found at "
            f"{missing}. "
            "Run py/main_tmpl_survey.py --write-expanded-stack-grammar-lock "
            "to create/update both plain and plus locks."
        )

    plain_grammar_lock = _read_json_file(_PLAIN_EXPANDED_STACK_GRAMMAR_LOCK_PATH)
    plus_grammar_lock = _read_json_file(_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH)

    nesting_normal_form.assert_stack_counts_follow_expanded_grammar(
        plain_raw_sc,
        plain_grammar_lock,
        dataset_name="plain survey (plain expanded stack grammar lock)",
    )
    nesting_normal_form.assert_stack_counts_follow_expanded_grammar(
        plus_raw_sc,
        plus_grammar_lock,
        dataset_name="plus survey (plus expanded stack grammar lock)",
    )


def almost_main(write_expanded_stack_grammar_lock=False):
    """Survey the use of templates in MAM plain and plus."""
    case_rank_maps = _case_rank_maps(_NORMAL_FORM_CASE_RANK_GROUPS)
    plain_result, plain_raw_sc, plain_discarded = survey_plain.survey(
        case_rank_maps=case_rank_maps
    )
    plus_result, plus_raw_sc, plus_discarded = survey_plus.survey(
        plain_result["mpasuq"],
        case_rank_maps=case_rank_maps,
    )
    _assert_with_expanded_stack_grammar_locks(
        plain_raw_sc,
        plus_raw_sc,
        write_expanded_stack_grammar_locks=write_expanded_stack_grammar_lock,
    )

    _write_outputs(
        plain_result,
        plain_raw_sc,
        f"{_PLAIN_OUT_DIR}/plain",
        svg_stem=f"{_PLAIN_SVG_DIR}/plain",
        normalization_note=_PLAIN_TMPL_NAME_NORMALIZATION_NOTE,
        discarded=plain_discarded,
    )
    _write_outputs(
        plus_result,
        plus_raw_sc,
        f"{_PLUS_OUT_DIR}/plus",
        svg_stem=f"{_PLUS_SVG_DIR}/plus",
        discarded=plus_discarded,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-expanded-stack-grammar-lock",
        action="store_true",
        help=(
            "Infer expanded stack grammar separately for plain and plus surveys, "
            "write/update both lock files, and validate the current run against "
            "the matching lock for each dataset."
        ),
    )
    return parser


def main():
    """Survey the use of templates in MAM plain and plus."""
    parser = build_parser()
    args = parser.parse_args()
    almost_main(
        write_expanded_stack_grammar_lock=args.write_expanded_stack_grammar_lock
    )


if __name__ == "__main__":
    main()
