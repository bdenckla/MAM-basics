"""Survey template usage patterns across the MAM-parsed-plus corpus."""

import argparse
import json
import os
import sys

from tmpl_survey import nesting_normal_form
from tmpl_survey import stack_path_lookup
from tmpl_survey import survey_dot
from tmpl_survey import survey_plus
from mb_cmn import file_io
from mb_cmn import paths

_PLUS_OUT_DIR = "out/tmpl-survey-plus"
_PLUS_SVG_DIR = str(paths.gh_pages_dir() / "MAM-parsed" / "plus" / "svg")
_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH = (
    "py/tmpl_survey/expanded_stack_grammar_plus.lock.json"
)
_PLUS_FULL_GRAPH_COLLAPSE_NODE_GROUPS = (("כו״ק", "קו״כ", "מ:קו״כ-אם-2"),)
_PLUS_FULL_GRAPH_PREFERRED_REPRESENTATIVES = ("סס",)
_PLUS_FULL_GRAPH_PREFER_SHORTEST_REPRESENTATIVE = True


_NORMAL_FORM_CASE_RANK_GROUPS = {
    "plus-C": nesting_normal_form.RANK_GROUPS_FOR_PLUS_C,
    "plus-D": nesting_normal_form.RANK_GROUPS_FOR_PLUS_D,
    "plus-E": nesting_normal_form.RANK_GROUPS_FOR_PLUS_E,
}


def _case_rank_maps(case_rank_groups):
    return {
        case_key: nesting_normal_form.build_rank_map(rank_groups)
        for case_key, rank_groups in case_rank_groups.items()
    }


def _write_outputs(
    result,
    raw_stack_counts,
    stem,
    svg_stem,
    full_graph_collapse_node_groups=None,
    full_graph_preferred_representatives=None,
    full_graph_prefer_shortest_representative=False,
):
    os.makedirs(os.path.dirname(stem), exist_ok=True)
    os.makedirs(os.path.dirname(svg_stem), exist_ok=True)
    file_io.json_dump_to_file_path(
        result,
        f"{stem}.json",
        generator_file=__file__,
    )
    dot_path = f"{stem}-call-graph.dot"
    if svg_stem is None:
        svg_stem = stem
    svg_path = f"{svg_stem}-call-graph.svg"
    survey_dot.write_dot_and_svg_files(
        raw_stack_counts,
        dot_path,
        svg_path,
        generator_file=__file__,
        collapse_node_groups=full_graph_collapse_node_groups,
        preferred_representatives=full_graph_preferred_representatives,
        prefer_shortest_representative=full_graph_prefer_shortest_representative,
    )
    survey_dot.write_focused_dot_files(
        raw_stack_counts,
        stem,
        svg_stem=svg_stem,
        generator_file=__file__,
    )


def _read_json_file(path):
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def _write_expanded_stack_grammar_lock(plus_grammar):
    file_io.json_dump_to_file_path(
        plus_grammar,
        _PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH,
        generator_file=__file__,
    )


def _assert_with_expanded_stack_grammar_lock(
    plus_raw_sc,
    write_expanded_stack_grammar_lock=False,
):
    plus_inferred_grammar = nesting_normal_form.infer_expanded_stack_grammar(
        plus_raw_sc
    )

    if write_expanded_stack_grammar_lock:
        _write_expanded_stack_grammar_lock(plus_inferred_grammar)

    if not os.path.exists(_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH):
        raise FileNotFoundError(
            "Expanded stack grammar lock file not found at "
            f"{_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH}. "
            "Run py/main_tmpl_survey.py --write-expanded-stack-grammar-lock "
            "to create/update the plus lock."
        )

    plus_grammar_lock = _read_json_file(_PLUS_EXPANDED_STACK_GRAMMAR_LOCK_PATH)

    nesting_normal_form.assert_stack_counts_follow_expanded_grammar(
        plus_raw_sc,
        plus_grammar_lock,
        dataset_name="plus survey (plus expanded stack grammar lock)",
    )


def almost_main(write_expanded_stack_grammar_lock=False):
    """Survey the use of templates in MAM-parsed-plus."""
    case_rank_maps = _case_rank_maps(_NORMAL_FORM_CASE_RANK_GROUPS)
    plus_result, plus_raw_sc = survey_plus.survey(case_rank_maps=case_rank_maps)
    _assert_with_expanded_stack_grammar_lock(
        plus_raw_sc,
        write_expanded_stack_grammar_lock=write_expanded_stack_grammar_lock,
    )

    plus_result["normal_order_cov_counts_by_case"] = (
        nesting_normal_form.summarize_rank_coverage_by_case(
            plus_raw_sc,
            case_rank_maps=case_rank_maps,
        )
    )
    plus_result["normal_order_cov_top_paths_by_case"] = (
        nesting_normal_form.summarize_rank_coverage_top_paths_by_case(
            plus_raw_sc,
            case_rank_maps=case_rank_maps,
            max_paths=10,
        )
    )

    _write_outputs(
        plus_result,
        plus_raw_sc,
        f"{_PLUS_OUT_DIR}/plus",
        svg_stem=f"{_PLUS_SVG_DIR}/plus",
        full_graph_collapse_node_groups=_PLUS_FULL_GRAPH_COLLAPSE_NODE_GROUPS,
        full_graph_preferred_representatives=_PLUS_FULL_GRAPH_PREFERRED_REPRESENTATIVES,
        full_graph_prefer_shortest_representative=_PLUS_FULL_GRAPH_PREFER_SHORTEST_REPRESENTATIVE,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-expanded-stack-grammar-lock",
        action="store_true",
        help=(
            "Infer the plus survey's expanded stack grammar, write/update its "
            "lock file, and validate the current run against that lock."
        ),
    )
    stack_path_lookup.add_parser_args(parser)
    return parser


def main():
    """Survey the use of templates in MAM-parsed-plus."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    if stack_path_lookup.maybe_handle_cli(parser, args):
        return
    almost_main(
        write_expanded_stack_grammar_lock=args.write_expanded_stack_grammar_lock
    )


if __name__ == "__main__":
    main()
