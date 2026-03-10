"""Survey Wikisource template usage patterns across the MAM corpus (plain and plus)."""

from pytmpl_survey import survey_plain
from pytmpl_survey import survey_plus
from pycmn import file_io


def almost_main():
    """Survey the use of templates in MAM plain and plus."""
    file_io.json_dump_to_file_path(
        survey_plain.survey(), "out/MAM-tmpl-survey-plain.json"
    )
    file_io.json_dump_to_file_path(
        survey_plus.survey(), "out/MAM-tmpl-survey-plus.json"
    )


def main():
    """Survey the use of templates in MAM plain and plus."""
    almost_main()


if __name__ == "__main__":
    main()
