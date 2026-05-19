"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

import os

from tmpl_survey import survey_dot
from tmpl_survey import survey_plain
from tmpl_survey import survey_plus
from mb_cmn import file_io

_OUT_DIR = "out/MAM-tmpl-survey"
_SVG_DIR = "../MAM-parsed/gh-pages"
_PLAIN_TMPL_NAME_NORMALIZATION_NOTE = (
    "In the plain survey, template names are normalized: ASCII double quote "
    '(") is converted to Hebrew gershayim (U+05F4). This applies to both '
    "stmpl and tmpl template forms in plain data."
)


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
    survey_dot.write_focused_dot_files(
        raw_stack_counts,
        stem,
        svg_stem=svg_stem,
        generator_file=__file__,
        discarded=discarded,
    )


def almost_main():
    """Survey the use of templates in MAM plain and plus."""
    plain_result, plain_raw_sc, plain_discarded = survey_plain.survey()
    _write_outputs(
        plain_result,
        plain_raw_sc,
        f"{_OUT_DIR}/plain",
        svg_stem=f"{_SVG_DIR}/plain",
        normalization_note=_PLAIN_TMPL_NAME_NORMALIZATION_NOTE,
        discarded=plain_discarded,
    )
    plus_result, plus_raw_sc, plus_discarded = survey_plus.survey(
        plain_result["mpasuq"]
    )
    _write_outputs(
        plus_result,
        plus_raw_sc,
        f"{_OUT_DIR}/plus",
        svg_stem=f"{_SVG_DIR}/plus",
        discarded=plus_discarded,
    )


def main():
    """Survey the use of templates in MAM plain and plus."""
    almost_main()


if __name__ == "__main__":
    main()
