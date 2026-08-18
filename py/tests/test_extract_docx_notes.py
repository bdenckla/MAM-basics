from __future__ import annotations

import unicodedata
import unittest

from hkq_cmn.extract_docx_notes import (
    apply_notes_fixes,
    normalize_haketer_presentation_forms,
    split_notes_components,
    split_uxlc_pointed_prefix_atoms,
    strip_trailing_sof_pasuq_from_uxlc_qere,
)


class ExtractDocxNotesTests(unittest.TestCase):
    def test_row_2_targeted_fix_removes_buggy_uxlc_suffix(self) -> None:
        row_data = {
            "row_number": 2,
            "word": "הֶהָלְכ֣וּא",
            "notes": "MAM - No Comments | UXLC - ההלכוא הֶהָלְכ֣וְּּ\n(yatir aleph)",
        }

        apply_notes_fixes(row_data)

        self.assertEqual(
            row_data["notes"],
            "MAM - No Comments | UXLC - ההלכוא הֶהָלְכ֣וּ\n(yatir aleph)",
        )
        self.assertEqual(
            row_data["notes_orig"],
            "MAM - No Comments | UXLC - ההלכוא הֶהָלְכ֣וְּּ\n(yatir aleph)",
        )

    def test_row_37_targeted_fix_uses_explicit_ketiv_qere_pair(self) -> None:
        row_data = {
            "row_number": 37,
            "word": "",
            "notes": "MAM - No Comments | UXLC - מַה־לִּי־פֹה֙ מי־לי־",
        }

        apply_notes_fixes(row_data)

        self.assertEqual(row_data["word"], "מַה־לִּי־")
        self.assertEqual(
            row_data["notes"],
            "MAM - No Comments | UXLC - מי־לי־ מַה־לִּי־",
        )
        self.assertEqual(
            row_data["notes_orig"],
            "MAM - No Comments | UXLC - מַה־לִּי־פֹה֙ מי־לי־",
        )

    def test_split_notes_components_returns_fixed_row_37_uxlc_text(self) -> None:
        notes_uxlc, notes_uxlc_yatir, notes_haketer = split_notes_components(
            "MAM - No Comments | UXLC - מי־לי־ מַה־לִּי־"
        )

        self.assertEqual(notes_uxlc, "מי־לי־ מַה־לִּי־")
        self.assertIsNone(notes_uxlc_yatir)
        self.assertIsNone(notes_haketer)

    def test_split_notes_components_returns_fixed_row_2_uxlc_text(self) -> None:
        notes_uxlc, notes_uxlc_yatir, notes_haketer = split_notes_components(
            "MAM - No Comments | UXLC - ההלכוא הֶהָלְכ֣וּ\n(yatir aleph)"
        )

        self.assertEqual(notes_uxlc, "ההלכוא הֶהָלְכ֣וּ")
        self.assertEqual(notes_uxlc_yatir, "yatir aleph")
        self.assertIsNone(notes_haketer)

    def test_split_notes_components_expands_haketer_alphabetic_presentation_forms(
        self,
    ) -> None:
        notes_uxlc, notes_uxlc_yatir, notes_haketer = split_notes_components(
            "MAM - No Comments | UXLC - ב ב | HaKeter - בְּמַעֲלוֹתָ֑ו מָּיִם"
        )

        self.assertEqual(notes_uxlc, "ב ב")
        self.assertIsNone(notes_uxlc_yatir)
        self.assertEqual(notes_haketer, "בְּמַעֲלוֹתָ֑ו מָּיִם")

    def test_normalize_haketer_presentation_forms_expands_all_letter_forms(
        self,
    ) -> None:
        source = "".join(
            chr(codepoint)
            for codepoint in range(0xFB1D, 0xFB4F + 1)
            if unicodedata.name(chr(codepoint), "").startswith("HEBREW LETTER ")
            and unicodedata.normalize("NFKD", chr(codepoint)) != chr(codepoint)
        )

        self.assertTrue(source)
        self.assertEqual(
            normalize_haketer_presentation_forms(source),
            "".join(unicodedata.normalize("NFKD", char) for char in source),
        )

    def test_split_uxlc_pointed_prefix_atoms_strips_single_prefix_atom(self) -> None:
        notes_uxlc, pointed_prefix_atoms = split_uxlc_pointed_prefix_atoms(
            notes_uxlc="עַל־בנו בָּנָ֣יו",
            mam_word="בָּנָ֣ו",
        )

        self.assertEqual(notes_uxlc, "בנו בָּנָ֣יו")
        self.assertEqual(pointed_prefix_atoms, "עַל־")

    def test_split_uxlc_pointed_prefix_atoms_strips_multiple_prefix_atoms(self) -> None:
        notes_uxlc, pointed_prefix_atoms = split_uxlc_pointed_prefix_atoms(
            notes_uxlc="עַל־כָּל־המונה הֲמוֹנ֑וֹ",
            mam_word="הֲמוֹנֹ֑ה",
        )

        self.assertEqual(notes_uxlc, "המונה הֲמוֹנ֑וֹ")
        self.assertEqual(pointed_prefix_atoms, "עַל־כָּל־")

    def test_split_uxlc_pointed_prefix_atoms_keeps_non_prefix_ketiv_intact(
        self,
    ) -> None:
        notes_uxlc, pointed_prefix_atoms = split_uxlc_pointed_prefix_atoms(
            notes_uxlc="מי־לי־ מַה־לִּי־",
            mam_word="מַה־לִּי־",
        )

        self.assertEqual(notes_uxlc, "מי־לי־ מַה־לִּי־")
        self.assertIsNone(pointed_prefix_atoms)

    def test_strip_trailing_sof_pasuq_from_uxlc_qere_returns_original_when_changed(
        self,
    ) -> None:
        notes_uxlc, notes_uxlc_orig = strip_trailing_sof_pasuq_from_uxlc_qere(
            "אילו אֵילָֽיו׃"
        )

        self.assertEqual(notes_uxlc, "אילו אֵילָֽיו")
        self.assertEqual(notes_uxlc_orig, "אילו אֵילָֽיו׃")

    def test_strip_trailing_sof_pasuq_from_uxlc_qere_is_noop_without_sof_pasuq(
        self,
    ) -> None:
        notes_uxlc, notes_uxlc_orig = strip_trailing_sof_pasuq_from_uxlc_qere(
            "רחמו רַֽחֲמָ֔יו"
        )

        self.assertEqual(notes_uxlc, "רחמו רַֽחֲמָ֔יו")
        self.assertIsNone(notes_uxlc_orig)


if __name__ == "__main__":
    unittest.main()
