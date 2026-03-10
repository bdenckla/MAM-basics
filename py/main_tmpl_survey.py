"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

import os

from pytmpl_survey import survey_dot
from pytmpl_survey import survey_plain
from pytmpl_survey import survey_plus
from pytmpl_survey import survey_xlsx
from pycmn import file_io

_OUT_DIR = "out/MAM-tmpl-survey"
_XLSX_DIR = f"{_OUT_DIR}/.novc"
_SVG_DIR = "../MAM-parsed/doc"


def _write_outputs(result, raw_stack_counts, stem, deeply_discard=False, svg_stem=None):
    os.makedirs(os.path.dirname(stem), exist_ok=True)
    file_io.json_dump_to_file_path(result, f"{stem}.json")
    xlsx_stem = f"{_XLSX_DIR}/{os.path.basename(stem)}"
    os.makedirs(_XLSX_DIR, exist_ok=True)
    survey_xlsx.write_xlsx(result, f"{xlsx_stem}.xlsx")
    dot_path = f"{stem}-call-graph.dot"
    if svg_stem is None:
        svg_stem = stem
    svg_path = f"{svg_stem}-call-graph.svg"
    survey_dot.write_dot_file(raw_stack_counts, dot_path, deeply_discard)
    survey_dot.render_svg(dot_path, svg_path)
    survey_dot.write_focused_dot_files(
        raw_stack_counts, stem, deeply_discard, svg_stem=svg_stem
    )


def almost_main():
    """Survey the use of templates in MAM plain and plus."""
    plain_result, plain_raw_sc = survey_plain.survey()
    _write_outputs(
        plain_result,
        plain_raw_sc,
        f"{_OUT_DIR}/plain",
        svg_stem=f"{_SVG_DIR}/plain",
    )
    plus_result, plus_raw_sc = survey_plus.survey(plain_result["mpasuq"])
    _write_outputs(
        plus_result,
        plus_raw_sc,
        f"{_OUT_DIR}/plus",
        deeply_discard=True,
        svg_stem=f"{_SVG_DIR}/plus",
    )


def main():
    """Survey the use of templates in MAM plain and plus."""
    almost_main()


if __name__ == "__main__":
    main()
