from __future__ import annotations

import unittest

from hkq_cmn.hebrew_text_tokens import (
    find_hebrew_tokens,
    strip_ignorable_token_marks,
)
from main_search_final_hiriq_verse_text import (
    is_final_hiriq_token,
    strip_ignorable_marks,
)


class FinalHiriqVerseTextSearchTests(unittest.TestCase):
    def test_token_pattern_keeps_cgj_inside_word(self) -> None:
        verse_text = "מִבֵּ֥ית עֲבָדִ֑͏ֽים"
        self.assertEqual(find_hebrew_tokens(verse_text), ["מִבֵּ֥ית", "עֲבָדִ֑͏ֽים"])

    def test_strip_ignorable_marks_removes_accents_meteg_and_joiners(self) -> None:
        self.assertEqual(strip_ignorable_token_marks("עֲבָדִ֑͏ֽים"), "עֲבָדִים")
        self.assertEqual(strip_ignorable_marks("עֲבָדִ֑͏ֽים"), "עֲבָדִים")

    def test_final_hiriq_detection_matches_expected_cases(self) -> None:
        self.assertTrue(is_final_hiriq_token("גּוֹיִ֖"))
        self.assertFalse(is_final_hiriq_token("עֲבָדִ֑͏ֽים"))


if __name__ == "__main__":
    unittest.main()
