"""Run the former diffable-pointed-hebrew product command.

The command accepts a source file and an output file.  It expands every
character in the source into the product's short Unicode name and writes JSON.
The nine short names that differ from MAM-basics' general mapping are product
data in ``diffable-pointed-hebrew/short_unicode_name_overrides.json``.
"""

from __future__ import annotations

import argparse
import json
import unicodedata
from pathlib import Path

from mb_cmn import file_io, paths, uni_heb

_SHORT_NAME_OVERRIDES_PATH = (
    paths.repo_root() / "diffable-pointed-hebrew" / "short_unicode_name_overrides.json"
)


def _short_name_overrides() -> dict[int, str]:
    with _SHORT_NAME_OVERRIDES_PATH.open(encoding="utf-8") as input_file:
        override_data = json.load(input_file)
    return {
        int(code_point): short_name
        for code_point, short_name in override_data["short_names_by_code_point"].items()
    }


def _name_record(character: str, short_name_overrides: dict[int, str]) -> tuple:
    return (
        ord(character),
        short_name_overrides.get(ord(character), uni_heb.shunna(character)),
        unicodedata.name(character, None),
    )


def _comma_join_shortened_unicode_names(
    code_point_names: dict, characters: str, short_name_overrides: dict[int, str]
) -> str:
    name_records = [
        _name_record(character, short_name_overrides) for character in characters
    ]
    for name_record in name_records:
        code_point_names[name_record[0]] = name_record[1:]
    return ",".join(name_record[1] for name_record in name_records)


def _make_lines_of_words(input_file, short_name_overrides: dict[int, str]):
    code_point_names = {}
    output_lines = []
    for source_line in input_file:
        source_words = source_line.replace("\n", "").split(" ")
        output_words = [
            _comma_join_shortened_unicode_names(
                code_point_names, source_word, short_name_overrides
            )
            for source_word in source_words
        ]
        output_lines.append(output_words)
    return code_point_names, output_lines


def _sorted_code_point_names(code_point_names: dict) -> list[tuple]:
    return [
        (code_point,) + code_point_names[code_point]
        for code_point in sorted(code_point_names)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_file", help="UTF-8 source text to expand")
    parser.add_argument("output_file", help="JSON file to write")
    args = parser.parse_args()

    short_name_overrides = _short_name_overrides()
    with Path(args.source_file).open(encoding="utf-8") as input_file:
        code_point_names, output_lines = _make_lines_of_words(
            input_file, short_name_overrides
        )
    file_io.json_dump_to_file_path(
        {
            "code_point_names": _sorted_code_point_names(code_point_names),
            "lines": output_lines,
        },
        args.output_file,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
