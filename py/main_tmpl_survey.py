"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

import os

from pytmpl_survey import survey_dot
from pytmpl_survey import survey_plain
from pytmpl_survey import survey_plus
from pytmpl_survey import survey_xlsx
from pycmn import file_io


def _write_outputs(result, raw_stack_counts, stem):
    os.makedirs(os.path.dirname(stem), exist_ok=True)
    file_io.json_dump_to_file_path(result, f"{stem}.json")
    survey_xlsx.write_xlsx(result, f"{stem}.xlsx")
    dot_path = f"{stem}-call-graph.dot"
    svg_path = f"{stem}-call-graph.svg"
    survey_dot.write_dot_file(raw_stack_counts, dot_path)
    survey_dot.render_svg(dot_path, svg_path)


_OUT_DIR = "out/MAM-tmpl-survey"


def almost_main():
    """Survey the use of templates in MAM plain and plus."""
    plain_result, plain_raw_sc = survey_plain.survey()
    _write_outputs(plain_result, plain_raw_sc, f"{_OUT_DIR}/plain")
    plus_result, plus_raw_sc = survey_plus.survey(plain_result["mpasuq"])
    _write_outputs(plus_result, plus_raw_sc, f"{_OUT_DIR}/plus")


def main():
    """Survey the use of templates in MAM plain and plus."""
    almost_main()


if __name__ == "__main__":
    main()
