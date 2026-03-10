"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

from pytmpl_survey import survey_plain
from pytmpl_survey import survey_plus
from pytmpl_survey import survey_xlsx
from pycmn import file_io


def almost_main():
    """Survey the use of templates in MAM plain and plus."""
    plain_result = survey_plain.survey()
    file_io.json_dump_to_file_path(plain_result, "out/MAM-tmpl-survey-plain.json")
    survey_xlsx.write_xlsx(plain_result, "out/MAM-tmpl-survey-plain.xlsx")
    plus_result = survey_plus.survey(plain_result["mpasuq"])
    file_io.json_dump_to_file_path(plus_result, "out/MAM-tmpl-survey-plus.json")
    survey_xlsx.write_xlsx(plus_result, "out/MAM-tmpl-survey-plus.xlsx")


def main():
    """Survey the use of templates in MAM plain and plus."""
    almost_main()


if __name__ == "__main__":
    main()
