from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

from mb_cmn import bib_locales
from mb_cmn.hebrew_points import RAFE
from mb_cmn.uni_denorm import give_std_mark_order as to_mam_mark_order
from hkq_cmn.extract_docx_notes import standard_book_name
from hkq_cmn.hebrew_text_tokens import HEBREW_TOKEN_CHAR_CLASS
from hkq_cmn.json_io import load_json
from hkq_cmn.mam_plus_verse_data import (
    verse_template_argument_records_by_location,
    verse_texts_by_location,
)
from hkq_cmn.supported_qere_wrapper import (
    supported_qere_wrapper_for_matching_args,
    supported_qere_wrapper_from_template_args,
)

# mpu = MAM-parsed-plus.
EXPECTED_ROW_COUNT = 77
KNOWN_DOCX_MPU_WORD_BY_VERSE = {
    "Joshua 10:24.19": (to_mam_mark_order("הֶהָלְכ֣וּא"), "הֶהָלְכ֣וּ"),
    "Tsefaniah 2:9.27": (to_mam_mark_order("גּוֹיִ֖"), "גּוֹיִ֖י"),
}
# Rows where the verse contains a supported qere wrapper for a DIFFERENT word than
# the docx word. Confirmed by UXLC k/q elements and neighbour-context matching.
KNOWN_DOCX_WORD_NOT_WRAPPED_IN_MPU_VERSE: frozenset[tuple[str, str]] = frozenset(
    {
        (
            "2Samuel 5:2.12",
            to_mam_mark_order("וְהַמֵּבִ֖י"),
        ),  # 3 k/q in verse; MPU templates only first two
        (
            "Job 26:14.4",
            to_mam_mark_order("דְּרָכָ֗ו"),
        ),  # 2 k/q in verse; MPU templates גבורתו
        ("Ezekiel 40:21.1", to_mam_mark_order("וְתָאָ֗ו")),  # verse k/q is וְאֵֽלַמָּו֙
        ("Ezekiel 40:31.7", to_mam_mark_order("אֵילָ֑ו")),  # verse k/q is מַעֲלָֽו
        ("Ezekiel 40:37.1", to_mam_mark_order("וְאֵילָ֗ו")),  # verse k/q is מַעֲלָֽו
        ("Ezekiel 40:37.6", to_mam_mark_order("אֵילָ֖ו")),  # verse k/q is מַעֲלָֽו
    }
)

VERSE_PATTERN = re.compile(
    r"^(?P<book_token>.*) (?P<chapter>\d+):(?P<verse>\d+)\.(?P<segment>\d+)$"
)
# Hebrew token chars: letters + pointing/cantillation marks (exclude punctuation like maqaf/sof-pasuq).
HEBREW_CHAR_CLASS = HEBREW_TOKEN_CHAR_CLASS
TRAILING_NON_TOKEN_PUNCTUATION_RE = re.compile(rf"[^{HEBREW_CHAR_CLASS}]+$")
SURFACE_WORD_WITH_TRAILING_PUNCTUATION_RE = re.compile(
    rf"(?P<word>[{HEBREW_CHAR_CLASS}]+)(?P<trailing>[\u05BE\u05C0\u05C3]*)"
)


@lru_cache(maxsize=1024)
def _word_boundary_pattern(word: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?<![{HEBREW_CHAR_CLASS}]){re.escape(word)}(?![{HEBREW_CHAR_CLASS}])"
    )


def normalize_mpu_match_text(text: str) -> str:
    return text.replace(RAFE, "")


def normalize_mpu_exact_arg_match_text(text: str) -> str:
    return TRAILING_NON_TOKEN_PUNCTUATION_RE.sub("", normalize_mpu_match_text(text))


def contains_word_as_hebrew_token(text: str, word: str) -> bool:
    if not word:
        return False
    normalized_word = normalize_mpu_match_text(word)
    if not normalized_word:
        return False
    normalized_text = normalize_mpu_match_text(text)
    return _word_boundary_pattern(normalized_word).search(normalized_text) is not None


def matching_template_args_for_word(
    template_args: list[dict[str, str]],
    word: str,
) -> list[dict[str, str]]:
    normalized_exact_word = normalize_mpu_exact_arg_match_text(word)
    exact_matches = [
        arg
        for arg in template_args
        if normalize_mpu_exact_arg_match_text(arg["argument_text"])
        == normalized_exact_word
    ]
    if exact_matches:
        return exact_matches

    return [
        arg
        for arg in template_args
        if contains_word_as_hebrew_token(arg["argument_text"], word)
    ]


def matching_mpu_surface_words_in_verse_text(verse_text: str, word: str) -> list[str]:
    normalized_exact_word = normalize_mpu_exact_arg_match_text(word)
    if not normalized_exact_word:
        return []

    matching_surface_words: list[str] = []
    for match in SURFACE_WORD_WITH_TRAILING_PUNCTUATION_RE.finditer(verse_text):
        surface_word = f'{match.group("word")}{match.group("trailing")}'
        if normalize_mpu_exact_arg_match_text(surface_word) != normalized_exact_word:
            continue
        if surface_word not in matching_surface_words:
            matching_surface_words.append(surface_word)

    return matching_surface_words


def latest_mpu_word_for_known_docx_word(verse: str, word: str) -> str | None:
    known_bug = KNOWN_DOCX_MPU_WORD_BY_VERSE.get(verse)
    if known_bug is None:
        return None

    docx_word, latest_mpu_word = known_bug
    if normalize_mpu_match_text(word) != normalize_mpu_match_text(docx_word):
        return None
    return latest_mpu_word


def parse_table_verse(verse: str) -> tuple[str, int, int]:
    match = VERSE_PATTERN.fullmatch(verse)
    if match is None:
        raise ValueError(f"unexpected verse format: {verse!r}")
    return (
        match.group("book_token"),
        int(match.group("chapter")),
        int(match.group("verse")),
    )


def standard_book_name_by_abbreviation(
    table: dict[str, object],
) -> dict[str, str]:
    verse_book_name_by_abbreviation = table.get("verse_book_name_by_abbreviation")
    if verse_book_name_by_abbreviation is None:
        return {}
    if not isinstance(verse_book_name_by_abbreviation, dict):
        raise ValueError(
            "table JSON key 'verse_book_name_by_abbreviation' must be an object when present"
        )

    normalized: dict[str, str] = {}
    for abbreviation, std_book_name in verse_book_name_by_abbreviation.items():
        if not isinstance(abbreviation, str) or not isinstance(std_book_name, str):
            raise ValueError(
                "table.verse_book_name_by_abbreviation must map strings to strings"
            )
        normalized[abbreviation] = std_book_name

    return normalized


def standard_book_name_for_table_verse(
    book_token: str,
    std_book_name_by_abbrev: dict[str, str],
    row_number: int,
) -> str:
    mapped = std_book_name_by_abbrev.get(book_token)
    if mapped is not None:
        return mapped

    try:
        return standard_book_name(book_token)
    except ValueError as exc:
        raise ValueError(
            f"unknown verse book token {book_token!r} at row {row_number}"
        ) from exc


@lru_cache(maxsize=64)
def expected_plus_location_for_standard_book_name(
    std_book_name: str,
) -> tuple[str, int]:
    try:
        bk24id = bib_locales.bk24id(std_book_name)
    except KeyError as exc:
        raise ValueError(f"unknown standard book name {std_book_name!r}") from exc

    bk39ids = bib_locales.bk39ids_of_bk24(bk24id)
    try:
        book39_index = bk39ids.index(std_book_name)
    except ValueError as exc:
        raise ValueError(
            f"standard book name {std_book_name!r} not found in bk24 {bk24id!r}"
        ) from exc

    return (
        f"{bib_locales.ordered_short_dash_full_24(bk24id)}.json",
        book39_index,
    )


def verify_table_words_in_mam_plus(
    table_json_path: Path,
    mam_parsed_path: Path,
) -> dict[str, object]:
    table_data = load_json(table_json_path)
    if not isinstance(table_data, dict):
        raise ValueError("table JSON root must be an object")

    table = table_data.get("table")
    if not isinstance(table, dict):
        raise ValueError("table JSON missing object key 'table'")

    rows = table.get("rows")
    if not isinstance(rows, list):
        raise ValueError("table JSON missing list key 'rows'")

    std_book_name_by_abbrev = standard_book_name_by_abbreviation(table)

    if len(rows) != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"expected exactly {EXPECTED_ROW_COUNT} rows, found {len(rows)}; "
            "this repository is scoped to the current fixed dataset"
        )

    plus_dir = mam_parsed_path / "plus"
    plus_files = sorted(plus_dir.glob("*.json"))
    if not plus_files:
        raise ValueError(f"no plus JSON files found at: {plus_dir}")

    plus_verse_texts_by_name = {}
    plus_verse_template_args_by_name = {}
    for path in plus_files:
        plus_json = load_json(path)
        plus_verse_texts_by_name[path.name] = verse_texts_by_location(plus_json)
        plus_verse_template_args_by_name[path.name] = (
            verse_template_argument_records_by_location(plus_json)
        )
    plus_search_text_by_name = {
        file_name: normalize_mpu_match_text("\n".join(verse_texts.values()))
        for file_name, verse_texts in plus_verse_texts_by_name.items()
    }

    row_reports: list[dict[str, object]] = []
    missing_any: list[dict[str, object]] = []
    missing_mpu_verse_text: list[dict[str, object]] = []
    mpu_verse_template_arg_rows: list[dict[str, object]] = []
    supported_qere_wrapper_rows: list[dict[str, object]] = []
    supported_qere_wrapper_mismatch_rows: list[dict[str, object]] = []

    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"row must be object, got: {type(row)}")
        row_number = row.get("row_number")
        verse = row.get("verse")
        word = row.get("word")

        if not isinstance(row_number, int):
            raise ValueError(f"row has invalid row_number: {row!r}")
        if not isinstance(verse, str):
            raise ValueError(f"row has invalid verse at row {row_number}")
        if not isinstance(word, str):
            raise ValueError(f"row has invalid word at row {row_number}")

        normalized_word = normalize_mpu_match_text(word)

        hit_files = [
            file_name
            for file_name, search_text in plus_search_text_by_name.items()
            if normalized_word in search_text
        ]

        book_token, chapter_num, verse_num = parse_table_verse(verse)
        std_book_name = standard_book_name_for_table_verse(
            book_token=book_token,
            std_book_name_by_abbrev=std_book_name_by_abbrev,
            row_number=row_number,
        )
        expected_location = expected_plus_location_for_standard_book_name(std_book_name)
        expected_file, expected_book39_index = expected_location

        expected_verse_texts = plus_verse_texts_by_name.get(expected_file)
        if expected_verse_texts is None:
            raise ValueError(f"expected plus file missing: {expected_file}")

        expected_verse_text = expected_verse_texts.get(
            (expected_book39_index, chapter_num, verse_num)
        )
        if expected_verse_text is None:
            raise ValueError(
                "expected verse missing in plus data: "
                f"file={expected_file}, book39_index={expected_book39_index}, "
                f"chapter={chapter_num}, verse={verse_num}, row={row_number}"
            )

        expected_verse_template_args = plus_verse_template_args_by_name[
            expected_file
        ].get((expected_book39_index, chapter_num, verse_num))
        if expected_verse_template_args is None:
            raise ValueError(
                "expected verse missing template arguments in plus data: "
                f"file={expected_file}, book39_index={expected_book39_index}, "
                f"chapter={chapter_num}, verse={verse_num}, row={row_number}"
            )

        found_in_any = len(hit_files) > 0
        found_in_expected = normalized_word in normalize_mpu_match_text(
            expected_verse_text
        )
        matching_template_args = matching_template_args_for_word(
            expected_verse_template_args,
            word,
        )
        surface_match_word = word
        found_in_mpu_verse_template_arg = len(matching_template_args) > 0
        found_via_known_docx_mpu_word = False

        latest_mpu_word = latest_mpu_word_for_known_docx_word(verse, word)
        if latest_mpu_word is not None:
            normalized_latest_mpu_word = normalize_mpu_match_text(latest_mpu_word)

            if not found_in_any:
                latest_hit_files = [
                    file_name
                    for file_name, search_text in plus_search_text_by_name.items()
                    if normalized_latest_mpu_word in search_text
                ]
                if latest_hit_files:
                    hit_files = latest_hit_files
                    found_in_any = True
                    found_via_known_docx_mpu_word = True

            if (
                not found_in_expected
                and normalized_latest_mpu_word
                in normalize_mpu_match_text(expected_verse_text)
            ):
                found_in_expected = True
                found_via_known_docx_mpu_word = True

            if not found_in_mpu_verse_template_arg:
                latest_matching_template_args = matching_template_args_for_word(
                    expected_verse_template_args,
                    latest_mpu_word,
                )
                if latest_matching_template_args:
                    matching_template_args = latest_matching_template_args
                    surface_match_word = latest_mpu_word
                    found_in_mpu_verse_template_arg = True
                    found_via_known_docx_mpu_word = True
        # Compute the wrapper after matching_template_args is finalized.
        # When the word was found via a template arg, use the matching args to
        # select the right wrapper even when the verse contains multiple wrappers.
        if found_in_mpu_verse_template_arg:
            supported_qere_wrapper = supported_qere_wrapper_for_matching_args(
                matching_template_args, expected_verse_template_args
            )
        else:
            supported_qere_wrapper = supported_qere_wrapper_from_template_args(
                expected_verse_template_args
            )
        if (verse, word) in KNOWN_DOCX_WORD_NOT_WRAPPED_IN_MPU_VERSE:
            supported_qere_wrapper = None
        matching_mpu_surface_words = matching_mpu_surface_words_in_verse_text(
            expected_verse_text,
            surface_match_word,
        )
        supported_qere_wrapper_word_mismatch = (
            supported_qere_wrapper is not None and not found_in_mpu_verse_template_arg
        )

        report_row = {
            "row_number": row_number,
            "verse": verse,
            "word": word,
            "mpu_file_for_verse": expected_file,
            "found_in_any_plus_file": found_in_any,
            "found_in_mpu_verse_text": found_in_expected,
            "template_args_in_mpu_verse": expected_verse_template_args,
            "supported_qere_wrapper_in_mpu_verse": supported_qere_wrapper,
            "found_in_mpu_verse_template_arg": found_in_mpu_verse_template_arg,
            "matching_template_args_in_mpu_verse": matching_template_args,
            "matching_mpu_surface_words_in_mpu_verse": matching_mpu_surface_words,
            "supported_qere_wrapper_word_mismatch": supported_qere_wrapper_word_mismatch,
            "found_via_known_docx_mpu_word": found_via_known_docx_mpu_word,
            "hit_files": hit_files,
        }
        row_reports.append(report_row)

        if not found_in_any:
            missing_any.append(report_row)
        if not found_in_expected:
            missing_mpu_verse_text.append(report_row)
        if supported_qere_wrapper is not None:
            supported_qere_wrapper_rows.append(report_row)
        if found_in_mpu_verse_template_arg:
            mpu_verse_template_arg_rows.append(report_row)
        if supported_qere_wrapper_word_mismatch:
            supported_qere_wrapper_mismatch_rows.append(report_row)

    summary = {
        "row_count": len(rows),
        "unique_word_count": len(
            {row["word"] for row in rows if isinstance(row, dict) and "word" in row}
        ),
        "missing_any_plus_count": len(missing_any),
        "missing_mpu_verse_text_count": len(missing_mpu_verse_text),
        "rows_matching_mpu_verse_template_arg_count": len(mpu_verse_template_arg_rows),
        "rows_with_supported_qere_wrapper_count": len(supported_qere_wrapper_rows),
        "rows_supported_qere_wrapper_mismatch_count": len(
            supported_qere_wrapper_mismatch_rows
        ),
    }

    return {
        "summary": summary,
        "rows": row_reports,
        "missing_any_plus": missing_any,
        "missing_mpu_verse_text_rows": missing_mpu_verse_text,
        "rows_matching_mpu_verse_template_arg": mpu_verse_template_arg_rows,
        "rows_with_supported_qere_wrapper": supported_qere_wrapper_rows,
        "rows_supported_qere_wrapper_mismatch": supported_qere_wrapper_mismatch_rows,
    }
