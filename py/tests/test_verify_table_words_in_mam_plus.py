from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from py_render.rt_mam_uxlc_diff_descriptions import simple_row_diff_note_lines
from hkq_cmn.json_io import write_json
from hkq_cmn.supported_qere_wrapper import (
    supported_qere_wrapper_for_matching_args,
)
from hkq_cmn.verify_table_words_in_mam_plus import (
    contains_word_as_hebrew_token,
    matching_mpu_surface_words_in_verse_text,
    matching_template_args_for_word,
    normalize_mpu_match_text,
    verify_table_words_in_mam_plus,
)


class HebrewTokenMatcherTests(unittest.TestCase):
    def test_exact_match(self) -> None:
        self.assertTrue(contains_word_as_hebrew_token("אֵילָו֙", "אֵילָו֙"))

    def test_no_match_when_embedded_in_larger_hebrew_token(self) -> None:
        self.assertFalse(contains_word_as_hebrew_token("וְאֵילָו֙ם", "אֵילָו֙"))

    def test_space_boundaries_match(self) -> None:
        self.assertTrue(contains_word_as_hebrew_token("לפני אֵילָו֙ אחרי", "אֵילָו֙"))

    def test_ascii_punctuation_boundaries_match(self) -> None:
        self.assertTrue(contains_word_as_hebrew_token("(אֵילָו֙),", "אֵילָו֙"))

    def test_maqaf_boundary_counts_as_separator(self) -> None:
        self.assertTrue(contains_word_as_hebrew_token("אֵילָו֙־וְאֵילָיו", "אֵילָו֙"))

    def test_sof_pasuq_boundary_counts_as_separator(self) -> None:
        self.assertTrue(contains_word_as_hebrew_token("אֵילָו֙׃", "אֵילָו֙"))

    def test_cgj_inside_adjacent_token_does_not_create_false_boundary(self) -> None:
        self.assertFalse(contains_word_as_hebrew_token("עֲבָדִ֑͏ֽים", "דִ֑"))

    def test_normalize_mpu_match_text_strips_rafe(self) -> None:
        self.assertEqual(normalize_mpu_match_text("וַיֹּר֨אֿוּ"), "וַיֹּר֨אוּ")

    def test_rafe_in_text_does_not_block_token_match(self) -> None:
        self.assertTrue(
            contains_word_as_hebrew_token("וְנִרְפּ֥אֿוּ הַמָּֽיִם", "וְנִרְפּ֥אוּ")
        )


class VerifyTableWordsInMamPlusTests(unittest.TestCase):
    def test_diff_note_lines_ignore_json_only_qere_sof_pasuq_strip(self) -> None:
        self.assertIn(
            (
                "MAM vs UXLC qere:",
                "replace qubuts with shuruq",
            ),
            simple_row_diff_note_lines(
                {
                    "row_number": 39,
                    "verse": "Jeremiah 5:6.21",
                    "word": "מְשֻׁבוֹתֵיהֶֽם",
                    "word_orig": "מְשֻׁבוֹתֵיהֶֽם׃",
                    "notes-UXLC": "משבותיהם מְשׁוּבוֹתֵיהֶֽם",
                    "notes-UXLC_orig": "משבותיהם מְשׁוּבוֹתֵיהֶֽם׃",
                },
                issue_tags=[],
            ),
        )

    def test_matching_mpu_surface_words_in_verse_text_preserves_trailing_sof_pasuq(
        self,
    ) -> None:
        self.assertEqual(
            matching_mpu_surface_words_in_verse_text(
                "לפני מַעֲלָֽו׃ אחרי",
                "מַעֲלָֽו",
            ),
            ["מַעֲלָֽו׃"],
        )

    def test_trailing_non_token_punctuation_does_not_block_exact_template_arg_match(
        self,
    ) -> None:
        for word, argument_text in [
            ("מַעֲלָֽו׃", "מַעֲלָֽו"),
            ("בְּתוֹכֹֽה׃", "בְּתוֹכֹֽה"),
        ]:
            with self.subTest(word=word, argument_text=argument_text):
                template_args = [
                    {
                        "template_name": 'מ:קו"כ-אם-2',
                        "argument_key": "1",
                        "argument_text": argument_text,
                    }
                ]
                self.assertEqual(
                    matching_template_args_for_word(template_args, word),
                    template_args,
                )

    def test_prefers_exact_template_arg_match_over_wrapper_match(self) -> None:
        template_args = [
            {
                "template_name": 'כו"ק',
                "argument_key": "1",
                "argument_text": "ההלכוא",
            },
            {
                "template_name": "נוסח",
                "argument_key": "1",
                "argument_text": '{{כו"ק|ההלכוא|הֶהָלְכ֣וּ}}',
            },
            {
                "template_name": 'כו"ק',
                "argument_key": "2",
                "argument_text": "הֶהָלְכ֣וּ",
            },
        ]

        self.assertEqual(
            matching_template_args_for_word(template_args, "הֶהָלְכ֣וּ"),
            [
                {
                    "template_name": 'כו"ק',
                    "argument_key": "2",
                    "argument_text": "הֶהָלְכ֣וּ",
                }
            ],
        )

    def test_supported_qere_wrapper_detects_new_four_arg_trivial_wrapper(self) -> None:
        template_args = [
            {
                "template_name": 'מ:קו"כ-אם-2',
                "argument_key": "1",
                "argument_text": "וּבֵנָ֔יו",
            },
            {
                "template_name": 'מ:קו"כ-אם-2',
                "argument_key": "2",
                "argument_text": "ובניו",
            },
            {
                "template_name": 'מ:קו"כ-אם-2',
                "argument_key": "3",
                "argument_text": "וּבֵינָ֔יו",
            },
            {
                "template_name": 'מ:קו"כ-אם-2',
                "argument_key": "מקורות",
                "argument_text": "ל-קרי",
            },
        ]

        self.assertEqual(
            supported_qere_wrapper_for_matching_args(
                [template_args[0]],
                template_args,
            ),
            {
                "template_name": 'מ:קו"כ-אם-2',
                "ketiv": "וּבֵנָ֔יו",
                "qere": "וּבֵינָ֔יו",
            },
        )

    def test_known_docx_word_bug_uses_latest_mpu_word_for_verification(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            table_json_path = tmp_path / "table_data.json"
            plus_dir = tmp_path / "MAM-parsed" / "plus"
            plus_dir.mkdir(parents=True, exist_ok=True)

            write_json(
                table_json_path,
                {
                    "table": {
                        "rows": [
                            {
                                "row_number": 2,
                                "verse": "Joshua 10:24.19",
                                "word": "הֶהָלְכ֣וּא",
                            }
                        ]
                    }
                },
            )
            write_json(
                plus_dir / "B1-Joshua.json",
                {
                    "book39s": [
                        {
                            "chapters": {
                                "10": {
                                    "24": [
                                        {
                                            "tmpl_name": 'כו"ק',
                                            "tmpl_params": {
                                                "1": "ההלכוא",
                                                "2": "הֶהָלְכ֣וּ",
                                            },
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                },
            )

            with patch(
                "hkq_cmn.verify_table_words_in_mam_plus.EXPECTED_ROW_COUNT",
                1,
            ):
                report = verify_table_words_in_mam_plus(
                    table_json_path=table_json_path,
                    mam_parsed_path=tmp_path / "MAM-parsed",
                )

        self.assertEqual(report["summary"]["missing_any_plus_count"], 0)
        self.assertEqual(report["summary"]["missing_mpu_verse_text_count"], 0)
        self.assertEqual(
            report["summary"]["rows_matching_mpu_verse_template_arg_count"],
            1,
        )
        self.assertEqual(report["missing_any_plus"], [])
        self.assertEqual(report["missing_mpu_verse_text_rows"], [])
        self.assertEqual(
            report["rows_matching_mpu_verse_template_arg"][0][
                "matching_template_args_in_mpu_verse"
            ],
            [
                {
                    "template_name": 'כו"ק',
                    "argument_key": "2",
                    "argument_text": "הֶהָלְכ֣וּ",
                }
            ],
        )
        self.assertTrue(report["rows"][0]["found_via_known_docx_mpu_word"])

    def test_verify_report_records_matching_mpu_surface_word_with_external_sof_pasuq(
        self,
    ) -> None:
        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            table_json_path = tmp_path / "table_data.json"
            plus_dir = tmp_path / "MAM-parsed" / "plus"
            plus_dir.mkdir(parents=True, exist_ok=True)

            write_json(
                table_json_path,
                {
                    "table": {
                        "rows": [
                            {
                                "row_number": 1,
                                "verse": "Joshua 10:24.19",
                                "word": "מַעֲלָֽו",
                            }
                        ]
                    }
                },
            )
            write_json(
                plus_dir / "B1-Joshua.json",
                {
                    "book39s": [
                        {
                            "chapters": {
                                "10": {
                                    "24": [
                                        {
                                            "tmpl_name": 'מ:קו"כ-אם-2',
                                            "tmpl_params": {
                                                "1": "מַעֲלָֽו",
                                                "2": "מעלו",
                                                "3": "מַעֲלָֽיו",
                                                "מקורות": "ל-קרי",
                                            },
                                        },
                                        "׃",
                                    ]
                                }
                            }
                        }
                    ],
                },
            )

            with patch(
                "hkq_cmn.verify_table_words_in_mam_plus.EXPECTED_ROW_COUNT",
                1,
            ):
                report = verify_table_words_in_mam_plus(
                    table_json_path=table_json_path,
                    mam_parsed_path=tmp_path / "MAM-parsed",
                )

        self.assertEqual(
            report["rows_matching_mpu_verse_template_arg"][0][
                "matching_mpu_surface_words_in_mpu_verse"
            ],
            ["מַעֲלָֽו׃"],
        )


if __name__ == "__main__":
    unittest.main()
