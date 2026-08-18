"""Search mpu (MAM-parsed-plus) qere readings for holam-he word endings.

This is now a thin wrapper around the reusable ending-pattern search engine.
To create another ending-pattern search, copy this file and adjust SEARCH_SPEC.
"""

from __future__ import annotations

import json
import sys

from mb_cmn.hebrew_points import XOLAM
from hkq_cmn.qere_ending_search import (
    DEFAULT_MAM_BASICS_QERE_WORDS_PATH,
    DEFAULT_MAM_PARSED_PLUS_DIR,
    DEFAULT_OUTPUT_DIR,
    QereEndingSearchSpec,
    build_ending_pattern_report,
    load_mpu_hits_for_spec,
    load_wordlist_hits_for_spec,
    write_ending_pattern_report,
)

# mpu = MAM-parsed-plus.
SEARCH_SPEC = QereEndingSearchSpec(
    slug="holam_he",
    label="Holam-he qere endings",
    output_file_name="holam_he_qere_report.json",
    vowel_only_suffixes=(XOLAM + "ה",),
)
MAM_PARSED_PLUS_DIR = DEFAULT_MAM_PARSED_PLUS_DIR
MAM_BASICS_QERE_WORDS_PATH = DEFAULT_MAM_BASICS_QERE_WORDS_PATH
OUTPUT_PATH = DEFAULT_OUTPUT_DIR / SEARCH_SPEC.output_file_name


def is_holam_he_word(word: str) -> bool:
    return SEARCH_SPEC.matches_word(word)


def load_mpu_hits() -> list[dict[str, object]]:
    return load_mpu_hits_for_spec(SEARCH_SPEC)


def load_wordlist_hits() -> list[dict[str, str]]:
    return load_wordlist_hits_for_spec(SEARCH_SPEC)


def build_report() -> dict[str, object]:
    return build_ending_pattern_report(SEARCH_SPEC)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    output_path, report = write_ending_pattern_report(SEARCH_SPEC)
    print(str(output_path))
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
