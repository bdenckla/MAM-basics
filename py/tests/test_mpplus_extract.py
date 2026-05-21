import unittest

from mb_cmn import bib_locales as tbn
from mb_cmn import retired_kq_special_templates as rkqst
from mb_cmn import retired_template_names as rtmpln
from mb_diff_mpu import (
    mpplus_classify,
    mpplus_expand,
    mpplus_extract,
    mpplus_json,
    mpplus_structure,
)
from mb_diff_mpu.mpplus_book_urls import mam_with_doc_url, ref_str, wikisource_url
from mb_diff_mpu.mpplus_flatten import flatten_ep


def _ezek_40_26_old_ep():
    return [
        "וּמַעֲל֤וֹת שִׁבְעָה֙ ",
        {
            "tmpl_name": "קו״כ-אם",
            "tmpl_params": {
                "1": "עֹֽלוֹתָ֔ו",
                "2": "א-קרי=עֹֽלוֹתָ֔יו",
            },
        },
        " וְאֵלַמָּ֖ו לִפְנֵיהֶ֑ם וְתִמֹרִ֣ים ל֗וֹ אֶחָ֥ד מִפּ֛וֹ וְאֶחָ֥ד מִפּ֖וֹ אֶל־אֵילָֽו׃",
    ]


def _ezek_40_26_new_ep():
    return [
        "וּמַעֲל֤וֹת שִׁבְעָה֙ ",
        {
            "tmpl_name": "קו״כ-אם",
            "tmpl_params": {
                "1": "עֹֽלוֹתָ֔ו",
                "2": "א-קרי=עֹֽלוֹתָ֔יו",
            },
        },
        " ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": {
                    "tmpl_name": "קו״כ-אם",
                    "tmpl_params": {
                        "1": "וְאֵלַמָּ֖ו",
                        "2": "ל-קרי=וְאֵֽלַמָּ֖יו",
                    },
                },
                "2": "(הערת קרי מפורשת)",
            },
        },
        " לִפְנֵיהֶ֑ם וְתִמֹרִ֣ים ל֗וֹ אֶחָ֥ד מִפּ֛וֹ וְאֶחָ֥ד מִפּ֖וֹ אֶל־אֵילָֽו׃",
    ]


def _same_count_reorder_old_ep():
    return [
        "א",
        {"tmpl_name": "מ:לגרמיה", "tmpl_params": {}},
        "ב",
        {"tmpl_name": "מ:פסק", "tmpl_params": {}},
        "ג",
    ]


def _same_count_reorder_new_ep():
    return [
        "א",
        {"tmpl_name": "מ:פסק", "tmpl_params": {}},
        "ב",
        {"tmpl_name": "מ:לגרמיה", "tmpl_params": {}},
        "ג",
    ]


def _nested_relocation_old_ep():
    return [
        {
            "tmpl_name": "עטיפה",
            "tmpl_params": {
                "1": [
                    "א",
                    {"tmpl_name": "מ:לגרמיה", "tmpl_params": {}},
                ]
            },
        },
        {"tmpl_name": "מ:פסק", "tmpl_params": {}},
    ]


def _nested_relocation_new_ep():
    return [
        {
            "tmpl_name": "עטיפה",
            "tmpl_params": {
                "1": [
                    "א",
                    {"tmpl_name": "מ:פסק", "tmpl_params": {}},
                ]
            },
        },
        {"tmpl_name": "מ:לגרמיה", "tmpl_params": {}},
    ]


def _format_equivalent_old_ep():
    return [
        {
            "tmpl_name": "עטיפה",
            "tmpl_params": {
                "1": {"tmpl_name": "מ:פסק", "tmpl_params": {}},
            },
        }
    ]


def _format_equivalent_new_ep():
    return [
        {
            "tmpl_name": "עטיפה",
            "tmpl_args": [
                {"tmpl_name": "מ:פסק", "tmpl_params": {}},
            ],
        }
    ]


def _new_note_only_old_ep():
    return [
        "א",
        {"tmpl_name": "מ:פסק", "tmpl_params": {}},
        "ב",
    ]


def _new_note_only_new_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "א",
                    {"tmpl_name": "מ:פסק", "tmpl_params": {}},
                ],
                "2": "הערת נוסח חדשה",
            },
        },
        "ב",
    ]


def _expanded_note_scope_old_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": "א",
                "2": "הערת נוסח קיימת",
            },
        },
        {"tmpl_name": "מ:פסק", "tmpl_params": {}},
        "ב",
    ]


def _expanded_note_scope_new_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "א",
                    {"tmpl_name": "מ:פסק", "tmpl_params": {}},
                ],
                "2": "הערת נוסח קיימת",
            },
        },
        "ב",
    ]


def _neighbor_note_old_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": "אֵילָו֙",
                "2": "הערה קיימת על התיבה הראשונה",
            },
        },
        " ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": "וְאֵ֣ילַמָּ֔ו",
                "2": "הערה על התיבה השנייה",
            },
        },
    ]


def _neighbor_note_new_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": "אֵילָו֙",
                "2": "הערה קיימת על התיבה הראשונה",
            },
        },
        " ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": {
                    "tmpl_name": "קו״כ-אם",
                    "tmpl_params": {
                        "1": "וְאֵ֣ילַמָּ֔ו",
                        "2": "ל-קרי=וְאֵ֣ילַמָּ֔יו",
                    },
                },
                "2": "הערה על התיבה השנייה",
            },
        },
    ]


def _lam_4_3_old_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": {
                    "tmpl_name": "מ:כו״ק כתיב תרתין מילין וקרי מילה חדה",
                    "tmpl_params": {
                        "1": "כי ענים",
                        "2": "כַּיְעֵינִ֖ים",
                    },
                },
                "2": "הערה ישנה",
            },
        }
    ]


def _lam_4_3_new_ep():
    return [
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": {
                    "tmpl_name": "מ:כו״ק כתיב תרתין מילין וקרי מילה חדה",
                    "tmpl_params": {
                        "1": "כי ענים",
                        "2": "כַּיְעֵנִ֖ים",
                    },
                },
                "2": "הערה חדשה",
            },
        }
    ]


def _qvq_oldstyle_same_old_ep():
    return [
        "כַּאֲשֶׁ֥ר ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "יִשְׁאַל־",
                    {
                        "tmpl_name": "קרי ולא כתיב",
                        "tmpl_args": ["[אִ֖ישׁ]"],
                    },
                ],
                "2": "הערת נוסח",
            },
        },
        " בִּדְבַ֣ר הָאֱלֹהִ֑ים",
    ]


def _qvq_oldstyle_same_new_ep():
    return [
        "כַּאֲשֶׁ֥ר ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "יִשְׁאַל־",
                    {
                        "tmpl_name": "קרי ולא כתיב",
                        "tmpl_args": ["[אִ֖ישׁ]", "אִ֖ישׁ"],
                    },
                ],
                "2": "הערת נוסח",
            },
        },
        " בִּדְבַ֣ר הָאֱלֹהִ֑ים",
    ]


def _qvq_oldstyle_changed_old_ep():
    return [
        "כַּאֲשֶׁ֥ר ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "יִשְׁאַל־",
                    {
                        "tmpl_name": "קרי ולא כתיב",
                        "tmpl_args": ["[אִ֖ישׁ]"],
                    },
                ],
                "2": "הערת נוסח",
            },
        },
        " בִּדְבַ֣ר הָאֱלֹהִ֑ים",
    ]


def _qvq_oldstyle_changed_new_ep():
    return [
        "כַּאֲשֶׁ֥ר ",
        {
            "tmpl_name": "נוסח",
            "tmpl_params": {
                "1": [
                    "יִשְׁאַל־",
                    {
                        "tmpl_name": "קרי ולא כתיב",
                        "tmpl_args": ["[אֵ֖ישׁ]", "אֵ֖ישׁ"],
                    },
                ],
                "2": "הערת נוסח",
            },
        },
        " בִּדְבַ֣ר הָאֱלֹהִ֑ים",
    ]


class TemplateMultiplicityDiffTests(unittest.TestCase):
    def test_flatten_ep_uses_visible_qere_for_standard_kq(self):
        self.assertEqual(flatten_ep(_lam_4_3_old_ep()), "כַּיְעֵינִ֖ים")

    def test_json_serialization_does_not_concatenate_standard_kq_args(self):
        diff = mpplus_extract._diff_ep(
            _lam_4_3_old_ep(), _lam_4_3_new_ep(), tbn.BK_LAMENT, 4, 3
        )

        self.assertIsNotNone(diff)
        self.assertTrue(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertEqual(
            serialized["changes"],
            [{"old": "כַּיְעֵינִ֖ים", "new": "כַּיְעֵנִ֖ים"}],
        )

    def test_diff_ep_normalizes_oldstyle_qere_velo_ketiv(self):
        diff = mpplus_extract._diff_ep(
            _qvq_oldstyle_same_old_ep(),
            _qvq_oldstyle_same_new_ep(),
            tbn.BK_SND_SAM,
            16,
            23,
        )

        self.assertIsNone(diff)

    def test_json_serialization_scopes_qere_velo_ketiv_without_neighbor_word(self):
        diff = mpplus_extract._diff_ep(
            _qvq_oldstyle_changed_old_ep(),
            _qvq_oldstyle_changed_new_ep(),
            tbn.BK_SND_SAM,
            16,
            23,
        )

        self.assertIsNotNone(diff)
        self.assertTrue(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertEqual(serialized["changes"], [{"old": "אִ֖ישׁ", "new": "אֵ֖ישׁ"}])

    def test_multiset_delta_preserves_duplicate_template_additions(self):
        added, removed = mpplus_structure.template_name_multiset_delta(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep()
        )

        self.assertEqual(added, ["קו״כ-אם"])
        self.assertEqual(removed, [])

    def test_diff_ep_detects_duplicate_template_addition(self):
        diff = mpplus_extract._diff_ep(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep(), tbn.BK_EZEKIEL, 40, 26
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])
        self.assertEqual(diff["category"], "template-change")

    def test_json_serialization_reports_duplicate_template_addition(self):
        diff = mpplus_extract._diff_ep(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep(), tbn.BK_EZEKIEL, 40, 26
        )

        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertEqual(serialized["templates_added"], ["קו״כ-אם"])
        self.assertNotIn("templates_removed", serialized)

    def test_split_structural_kq_if_addition_scopes_neighboring_note(self):
        diff = mpplus_extract._diff_ep(
            _neighbor_note_old_ep(), _neighbor_note_new_ep(), tbn.BK_EZEKIEL, 40, 24
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])

        split = mpplus_expand.split_structural_diff(diff)
        self.assertIsNotNone(split)
        self.assertEqual(len(split), 1)
        self.assertEqual(split[0]["templates_added"], ["קו״כ-אם"])
        self.assertEqual(
            [note["param2"] for note in split[0]["docnote_notes"]],
            ["הערה על התיבה השנייה"],
        )

    def test_json_serialization_uses_scoped_note_for_split_kq_if_addition(self):
        diff = mpplus_extract._diff_ep(
            _neighbor_note_old_ep(), _neighbor_note_new_ep(), tbn.BK_EZEKIEL, 40, 24
        )

        mpplus_classify.classify_diffs([diff])
        split = mpplus_expand.split_structural_diff(diff)
        serialized = mpplus_json._serialize_diff(split[0])

        self.assertEqual(serialized["templates_added"], ["קו״כ-אם"])
        self.assertEqual(
            serialized["docnote_notes"][0]["param2"],
            "הערה על התיבה השנייה",
        )

    def test_diff_ep_detects_same_count_template_reorder(self):
        diff = mpplus_extract._diff_ep(
            _same_count_reorder_old_ep(),
            _same_count_reorder_new_ep(),
            tbn.BK_GENESIS,
            1,
            1,
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])
        self.assertEqual(diff["category"], "template-change")

    def test_json_serialization_marks_same_count_structural_change(self):
        diff = mpplus_extract._diff_ep(
            _same_count_reorder_old_ep(),
            _same_count_reorder_new_ep(),
            tbn.BK_GENESIS,
            1,
            1,
        )

        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertTrue(serialized["template_structure_changed"])
        self.assertNotIn("templates_added", serialized)
        self.assertNotIn("templates_removed", serialized)

    def test_diff_ep_detects_nested_same_count_relocation(self):
        diff = mpplus_extract._diff_ep(
            _nested_relocation_old_ep(),
            _nested_relocation_new_ep(),
            tbn.BK_GENESIS,
            1,
            2,
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])

    def test_diff_ep_ignores_equivalent_historical_param_formats(self):
        diff = mpplus_extract._diff_ep(
            _format_equivalent_old_ep(),
            _format_equivalent_new_ep(),
            tbn.BK_GENESIS,
            1,
            3,
        )

        self.assertIsNone(diff)

    def test_diff_ep_ignores_new_note_wrapping_existing_structure(self):
        diff = mpplus_extract._diff_ep(
            _new_note_only_old_ep(),
            _new_note_only_new_ep(),
            tbn.BK_GENESIS,
            1,
            4,
        )

        self.assertIsNone(diff)

    def test_diff_ep_ignores_existing_note_scope_expansion(self):
        diff = mpplus_extract._diff_ep(
            _expanded_note_scope_old_ep(),
            _expanded_note_scope_new_ep(),
            tbn.BK_GENESIS,
            1,
            5,
        )

        self.assertIsNone(diff)


def _std_kq_addition_old_ep():
    # Tsefaniah 2:9 pattern: bare qere text, no כו״ק wrapper
    return ["גּוֹיִ֖"]


def _std_kq_addition_new_ep():
    # A כו״ק template is added and the qere text also changes (alef added)
    return [
        {
            "tmpl_name": "כו״ק",
            "tmpl_params": {
                "1": "גוי",
                "2": "גּוֹיִ֖י",
            },
        }
    ]


class StdKqAdditionInTextChangedDiffTests(unittest.TestCase):
    def test_diff_ep_detects_text_changed(self):
        diff = mpplus_extract._diff_ep(
            _std_kq_addition_old_ep(),
            _std_kq_addition_new_ep(),
            tbn.BK_TSEF,
            2,
            9,
        )

        self.assertIsNotNone(diff)
        self.assertTrue(diff["text_changed"])

    def test_json_serialization_includes_both_changes_and_templates_added(self):
        diff = mpplus_extract._diff_ep(
            _std_kq_addition_old_ep(),
            _std_kq_addition_new_ep(),
            tbn.BK_TSEF,
            2,
            9,
        )

        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertIn("changes", serialized)
        self.assertEqual(serialized["templates_added"], ["כו״ק"])
        self.assertNotIn("templates_removed", serialized)

    def test_json_serialization_does_not_emit_templates_added_for_pure_text_change(
        self,
    ):
        # Existing כו״ק template where only param 2 changes: text changed, no structural
        # addition — templates_added should not appear (כו״ק count is unchanged).
        diff = mpplus_extract._diff_ep(
            _lam_4_3_old_ep(), _lam_4_3_new_ep(), tbn.BK_LAMENT, 4, 3
        )

        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertNotIn("templates_added", serialized)
        self.assertNotIn("templates_removed", serialized)


# ---------------------------------------------------------------------------
# Fixtures and tests for מ:קו״כ-אם-2 (new trivial-kq format)
# ---------------------------------------------------------------------------


def _kq_triv2_old_ep():
    """EP where a plain word will gain a מ:קו״כ-אם-2 template (new format)."""
    return [
        "עֹֽלוֹתָ֔ו ",
        "וְאֵלַמָּ֖ו לִפְנֵיהֶ֑ם׃",
    ]


def _kq_triv2_new_ep():
    """EP where the first word is now wrapped in a מ:קו״כ-אם-2 template."""
    return [
        {
            "tmpl_name": "מ:קו״כ-אם-2",
            "tmpl_params": {
                "1": "עֹֽלוֹתָ֔ו",
                "2": "עלותו",
                "3": "עֹֽלוֹתָ֔יו",
                "מקורות": "א",
            },
        },
        " ",
        "וְאֵלַמָּ֖ו לִפְנֵיהֶ֑ם׃",
    ]


def _kq_triv_rename_old_ep():
    """EP using the old קו״כ-אם template (pre-bot-edit)."""
    return [
        "אַ ",
        {
            "tmpl_name": "קו״כ-אם",
            "tmpl_params": {
                "1": "עֹֽלוֹתָ֔ו",
                "2": "א-קרי=עֹֽלוֹתָ֔יו",
            },
        },
        " ב׃",
    ]


def _kq_triv_rename_new_ep():
    """Same content but renamed to מ:קו״כ-אם-2 (post-bot-edit)."""
    return [
        "אַ ",
        {
            "tmpl_name": "מ:קו״כ-אם-2",
            "tmpl_params": {
                "1": "עֹֽלוֹתָ֔ו",
                "2": "עלותו",
                "3": "עֹֽלוֹתָ֔יו",
                "מקורות": "א",
            },
        },
        " ב׃",
    ]


def _special_kq_old_ep(old_name):
    return [
        {
            "tmpl_name": old_name,
            "tmpl_params": {
                "1": "כתיב",
                "2": "קְרִי",
            },
        }
    ]


def _special_kq_new_ep(old_name):
    return [
        {
            "tmpl_name": "מ:כו״ק מיוחד",
            "tmpl_params": {
                "1": "כתיב",
                "2": "קְרִי",
                "סוג": rkqst.sug_text_for_old_special_kq_template_name(old_name),
            },
        }
    ]


class KqTrivial2Tests(unittest.TestCase):
    def test_multiset_delta_detects_kq_triv2_addition(self):
        added, removed = mpplus_structure.template_name_multiset_delta(
            _kq_triv2_old_ep(), _kq_triv2_new_ep()
        )

        self.assertEqual(added, ["מ:קו״כ-אם-2"])
        self.assertEqual(removed, [])

    def test_diff_ep_detects_kq_triv2_addition(self):
        diff = mpplus_extract._diff_ep(
            _kq_triv2_old_ep(), _kq_triv2_new_ep(), tbn.BK_EZEKIEL, 40, 26
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpplus_classify.classify_diffs([diff])
        self.assertEqual(diff["category"], "template-change")

    def test_json_serialization_reports_kq_triv2_addition(self):
        diff = mpplus_extract._diff_ep(
            _kq_triv2_old_ep(), _kq_triv2_new_ep(), tbn.BK_EZEKIEL, 40, 26
        )

        mpplus_classify.classify_diffs([diff])
        serialized = mpplus_json._serialize_diff(diff)
        self.assertEqual(serialized["templates_added"], ["מ:קו״כ-אם-2"])
        self.assertNotIn("templates_removed", serialized)

    def test_split_kq_triv2_addition(self):
        diff = mpplus_extract._diff_ep(
            _kq_triv2_old_ep(), _kq_triv2_new_ep(), tbn.BK_EZEKIEL, 40, 26
        )

        mpplus_classify.classify_diffs([diff])
        split = mpplus_expand.split_structural_diff(diff)

        self.assertIsNotNone(split)
        self.assertEqual(len(split), 1)
        self.assertEqual(split[0]["templates_added"], ["מ:קו״כ-אם-2"])

    def test_kq_triv_rename_is_suppressed(self):
        """A pure bot-edit rename (קו״כ-אם → מ:קו״כ-אם-2) surfaces as no diff cards."""
        diff = mpplus_extract._diff_ep(
            _kq_triv_rename_old_ep(), _kq_triv_rename_new_ep(), tbn.BK_EZEKIEL, 40, 1
        )

        self.assertIsNotNone(diff)
        mpplus_classify.classify_diffs([diff])
        split = mpplus_expand.split_structural_diff(diff)

        self.assertEqual(split, [])

    def test_flatten_ep_is_identical_for_old_and_new_format(self):
        """flatten_ep returns the same body text for קו״כ-אם and מ:קו״כ-אם-2."""
        old_text = flatten_ep(_kq_triv_rename_old_ep())
        new_text = flatten_ep(_kq_triv_rename_new_ep())

        self.assertEqual(old_text, new_text)


class SpecialKqUnifiedDiffEquivalenceTests(unittest.TestCase):
    def test_old_vs_unified_special_kq_with_same_content_is_no_op(self):
        for old_name in (rtmpln.K1Q2_SR_KQQ, rtmpln.K2Q2, rtmpln.K3Q3):
            diff = mpplus_extract._diff_ep(
                _special_kq_old_ep(old_name),
                _special_kq_new_ep(old_name),
                tbn.BK_GENESIS,
                1,
                1,
            )

            self.assertIsNone(diff)


class CanonicalBookIdTests(unittest.TestCase):
    def test_mam_with_doc_url_accepts_canonical_book_id(self):
        url = mam_with_doc_url(tbn.BK_FST_SAM, 3, 4)

        self.assertEqual(
            url,
            "https://bdenckla.github.io/MAM-with-doc/BA-1Samuel.html#c3v4",
        )

    def test_wikisource_url_accepts_canonical_book_id(self):
        url = wikisource_url(tbn.BK_LEVIT, 2)

        self.assertEqual(
            url,
            "https://he.wikisource.org/wiki/%D7%95%D7%99%D7%A7%D7%A8%D7%90_%D7%91/%D7%98%D7%A2%D7%9E%D7%99%D7%9D",
        )

    def test_ref_str_uses_canonical_book_id(self):
        diff = {"book": tbn.BK_FST_SAM, "chapter": 3, "verse": 4}

        self.assertEqual(ref_str(diff), "1Samuel 3:4")


if __name__ == "__main__":
    unittest.main()

