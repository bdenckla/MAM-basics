"""Differential checks for validation and scanner fast paths."""

import json
import sys
from unittest.mock import patch

from accgram import poetic_scanner
from mb_cmn import paths
from phonetic_mam import display_schema


def test_forbidden_pattern_matches_set_membership_over_unicode():
    for codepoint in range(sys.maxunicode + 1):
        text = chr(codepoint)
        assert bool(display_schema._FORBIDDEN_PATTERN.search(text)) == bool(
            display_schema._FORBIDDEN & set(text)
        )


def test_poetic_fast_path_matches_full_rule_loop():
    files = sorted((paths.repo_root() / "out/accgram/poetic").glob("*_ag.json"))
    assert files
    count = 0
    for path in files:
        verses = json.loads(path.read_text(encoding="utf-8"))["verses"]
        assert verses
        for verse in verses:
            body = verse["input"]["marks"]
            actual = poetic_scanner.scan_accent_tokens(body)
            with patch.object(poetic_scanner, "_alternation_for", return_value=None):
                expected = poetic_scanner.scan_accent_tokens(body)
            assert actual == expected, verse["ref"]
            count += 1
    assert count
