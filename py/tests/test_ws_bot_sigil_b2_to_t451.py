"""Pin the ב2-to-ת451 edit payload before it is sent to Wikisource (MAM-basics#260).

This is the ws_bot exception CLAUDE.md grants to the testing rule: a Wikisource
edit is irreversible and outward-facing, and there is no regeneratable artifact
to diff after the fact, so pinning the payload before it is sent is worth its
cost here in a way an example-based unit test generally is not.

The synthetic fixtures below cover the shapes the sigil takes -- a comma list, the two
uncertainty-marker forms, an occurrence followed by "=" -- one shape at a time, and exercise
the two guards, which real data cannot exercise because real data does not violate them.

Phase 3 of the retired doc/PLAN-replace-sigil-b2-with-t451.md, whose last version is at
https://github.com/bdenckla/MAM-basics/blob/4f3fed2dcb1e21835ad73a31ea8e5e472f4960d7/doc/PLAN-replace-sigil-b2-with-t451.md,
sent the edit, and a31d0ec9 committed the six re-downloaded chapters of
in/mam-ws/F1-Daniel.json. Each later download's diff of that file shows any change to them,
so no test here reads the corpus.
"""

import unittest

from mb_cmn import bib_locales as tbn
from ws import ws_bot_edit_sigil_b2_to_t451 as mod

_B2 = "\N{HEBREW LETTER BET}2"
_T451 = "\N{HEBREW LETTER TAV}451"

# Real fragments, lifted from in/mam-ws/F1-Daniel.json. The chapter each is fed
# to below is chosen for its expected COUNT, not because the fragment is that
# chapter's own text -- the claim under test is about the shape the sigil takes.
_COMMA_LIST = "{{נוסח|מִיְּשֵׁנֵ֥י|2==ל?,ק-מ,ב1,ב2,ש2 ובדפוסים"
_FOLLOWED_BY_SPACE = "{{נוסח|וְלֵ֨הּ|2==ש1,ק-מ,ב1,ב2 ובדפוסים"
_QUESTION_MARK = '{{נוסח|לְיַצָּבָ֗א|2==ש1,ק-מ,ב2? (בטעם רביע), וכן בתנ"ך ליסבון'
_QUESTION_MARK_BRACKET = "{{נוסח|עָבְדָ֥ה|2==ל,ב1,ב2?[נכתבה בו א' ונמחקה!],ש2"
_FOLLOWED_BY_EQUALS = 'ובדפוסים{{ש}}ל!,ק-מ,ב2=הַגְּדוֹלָ֔ה (כתיב מלא וי"ו)}}'

# The aliyah template's named parameter -- the same two characters, and NOT the
# sigil. 216 of these stand in the five Torah books.
_ALIYAH_CALL = "{{מ:עלייה|א=בראשית|ב0=בראשית|ב1=ראשון|ב2=כהן}}"

# Chapters picked off the count table by how many occurrences each expects.
_CHAPTER_EXPECTING_1 = "יב"
_CHAPTER_EXPECTING_2 = "ח"


class WsBotSigilB2ToT451Tests(unittest.TestCase):
    def test_expected_table_is_six_chapters_totalling_32(self):
        table = mod.expected_counts(tbn.BK_DANIEL)
        self.assertEqual(len(table), 6)
        self.assertEqual(sum(table.values()), 32)
        self.assertEqual(mod.expected_total(), 32)

    def test_comma_list_occurrence_is_replaced(self):
        out = mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, _COMMA_LIST)

        self.assertNotIn(_B2, out)
        self.assertIn(f",{_T451},", out)
        self.assertEqual(out, _COMMA_LIST.replace(_B2, _T451))

    def test_uncertainty_marker_forms_are_replaced(self):
        page_text = f"{_QUESTION_MARK}\n{_QUESTION_MARK_BRACKET}"

        out = mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_2, page_text)

        self.assertNotIn(_B2, out)
        self.assertIn(f"{_T451}? ", out)
        self.assertIn(f"{_T451}?[", out)

    def test_occurrence_followed_by_equals_is_replaced(self):
        out = mod.edit_page_text(
            tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, _FOLLOWED_BY_EQUALS
        )

        self.assertNotIn(_B2, out)
        self.assertIn(f"{_T451}=", out)

    def test_replacement_is_strictly_in_place(self):
        """ת451 lands where ב2 stood, mid-list, rather than being reordered."""
        out = mod.edit_page_text(
            tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, _FOLLOWED_BY_SPACE
        )

        self.assertTrue(out.endswith(f"{_T451} ובדפוסים"))

    def test_a_replaced_chapter_records_its_count_in_the_warnings(self):
        before = len(mod.get_warnings())

        mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, _COMMA_LIST)

        after = mod.get_warnings()
        self.assertEqual(len(after), before + 1)
        self.assertEqual(after[-1]["bk39id"], tbn.BK_DANIEL)
        self.assertEqual(after[-1]["he_chnu"], _CHAPTER_EXPECTING_1)
        self.assertEqual(after[-1]["chapter"], 12)
        self.assertEqual(after[-1]["count"], 1)

    def test_a_book_outside_the_table_passes_through_untouched(self):
        """Guard 1. A Torah page's aliyah parameter must survive verbatim."""
        page_text = f"{_ALIYAH_CALL} בְּרֵאשִׁ֖ית"

        out = mod.edit_page_text(tbn.BK_GENESIS, "א", page_text)

        self.assertEqual(out, page_text)
        self.assertIn(_ALIYAH_CALL, out)
        self.assertNotIn(_T451, out)

    def test_a_chapter_outside_the_table_passes_through_untouched(self):
        """Guard 1 again, within the one book the table does name."""
        page_text = _COMMA_LIST

        out = mod.edit_page_text(tbn.BK_DANIEL, "א", page_text)

        self.assertEqual(out, page_text)

    def test_a_table_chapter_carrying_an_aliyah_parameter_raises(self):
        """Guard 2. Not a skip: such a page is not one this transform may touch."""
        page_text = f"{_ALIYAH_CALL} {_COMMA_LIST}"

        with self.assertRaises(AssertionError) as caught:
            mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, page_text)

        self.assertIn("aliyah parameter", str(caught.exception))

    def test_a_count_below_the_table_raises(self):
        with self.assertRaises(AssertionError) as caught:
            mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_2, _COMMA_LIST)

        self.assertIn("found 1", str(caught.exception))

    def test_a_count_above_the_table_raises(self):
        page_text = f"{_COMMA_LIST}\n{_FOLLOWED_BY_SPACE}"

        with self.assertRaises(AssertionError) as caught:
            mod.edit_page_text(tbn.BK_DANIEL, _CHAPTER_EXPECTING_1, page_text)

        self.assertIn("found 2", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
