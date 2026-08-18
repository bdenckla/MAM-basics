from __future__ import annotations

import unittest

from mb_cmn.hebrew_points import XOLAM
from hkq_cmn.qere_ending_search import QereEndingSearchSpec
from hkq_cmn.qere_projection import to_vowel_only_form


class QereEndingSearchHelpersTests(unittest.TestCase):
    def test_to_vowel_only_form_strips_accent_and_meteg(self) -> None:
        self.assertEqual(to_vowel_only_form("כֹּ֣ה"), "כֹּה")
        self.assertEqual(to_vowel_only_form("אָֽהֳלֹה"), "אָהֳלֹה")

    def test_to_vowel_only_form_strips_joiners(self) -> None:
        self.assertEqual(to_vowel_only_form("עֲבָדִ֑͏ֽים"), "עֲבָדִים")

    def test_suffix_search_matches_vowel_only_suffix(self) -> None:
        spec = QereEndingSearchSpec(
            slug="holam_he",
            label="Holam-he qere endings",
            output_file_name="unused.json",
            vowel_only_suffixes=(XOLAM + "ה",),
        )

        self.assertTrue(spec.matches_word("כֹּ֣ה"))
        self.assertTrue(spec.matches_word("אָֽהֳלֹה"))
        self.assertFalse(spec.matches_word("כִּ֤י"))


if __name__ == "__main__":
    unittest.main()
