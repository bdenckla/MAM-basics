import unittest

from mb_cmn import uni_heb as uh


class TestMbCmnUniHeb(unittest.TestCase):
    def test_he_to_ascii_direct_maps_canonical_examples(self):
        self.assertEqual("kpvl", uh.he_to_ascii_direct("כפול").lower())
        self.assertEqual("nvox", uh.he_to_ascii_direct("נוסח").lower())
        self.assertEqual("kv״q", uh.he_to_ascii_direct("כו״ק").lower())
        self.assertEqual("povq", uh.he_to_ascii_direct("פסוק").lower())
        self.assertEqual("dxy", uh.he_to_ascii_direct("דחי").lower())

    def test_he_to_ascii_direct_leaves_non_hebrew_chars_untouched(self):
        self.assertEqual("abg!?-", uh.he_to_ascii_direct("אבג!?-").lower())

    def test_he_ascii_slug_maps_and_normalizes(self):
        self.assertEqual("kpvl", uh.he_ascii_slug("כפול"))
        self.assertEqual("nvox", uh.he_ascii_slug("נוסח"))
        self.assertEqual("kvq", uh.he_ascii_slug("כו״ק"))
        self.assertEqual("povq", uh.he_ascii_slug("פסוק"))
        self.assertEqual("dxy", uh.he_ascii_slug("דחי"))

    def test_he_ascii_slug_strips_geresh_and_gershayim(self):
        self.assertEqual("abg", uh.he_ascii_slug("א׳ב״ג"))

    def test_he_ascii_slug_collapses_separators(self):
        self.assertEqual("kpvl-nvox", uh.he_ascii_slug("כפול + נוסח"))

    def test_he_ascii_slug_empty_and_digit_prefix_behavior(self):
        self.assertEqual("", uh.he_ascii_slug(""))
        self.assertEqual("h", uh.he_ascii_slug("", digit_prefix="h"))
        self.assertEqual("1a", uh.he_ascii_slug("1א", digit_prefix=""))
        self.assertEqual("h-1a", uh.he_ascii_slug("1א", digit_prefix="h"))


if __name__ == "__main__":
    unittest.main()
