import unittest

from pydiff_mpp import mpp_classify, mpp_extract, mpp_json, mpp_structure


def _ezek_40_26_old_ep():
    return [
        "וּמַעֲל֤וֹת שִׁבְעָה֙ ",
        {
            "tmpl_name": 'קו"כ-אם',
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
            "tmpl_name": 'קו"כ-אם',
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
                    "tmpl_name": 'קו"כ-אם',
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


class TemplateMultiplicityDiffTests(unittest.TestCase):
    def test_multiset_delta_preserves_duplicate_template_additions(self):
        added, removed = mpp_structure._template_name_multiset_delta(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep()
        )

        self.assertEqual(added, ['קו"כ-אם'])
        self.assertEqual(removed, [])

    def test_diff_ep_detects_duplicate_template_addition(self):
        diff = mpp_extract._diff_ep(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep(), "Ezekiel", 40, 26
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpp_classify.classify_diffs([diff])
        self.assertEqual(diff["category"], "template-change")

    def test_json_serialization_reports_duplicate_template_addition(self):
        diff = mpp_extract._diff_ep(
            _ezek_40_26_old_ep(), _ezek_40_26_new_ep(), "Ezekiel", 40, 26
        )

        mpp_classify.classify_diffs([diff])
        serialized = mpp_json._serialize_diff(diff)
        self.assertEqual(serialized["templates_added"], ['קו"כ-אם'])
        self.assertNotIn("templates_removed", serialized)

    def test_diff_ep_detects_same_count_template_reorder(self):
        diff = mpp_extract._diff_ep(
            _same_count_reorder_old_ep(),
            _same_count_reorder_new_ep(),
            "Genesis",
            1,
            1,
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])
        mpp_classify.classify_diffs([diff])
        self.assertEqual(diff["category"], "template-change")

    def test_json_serialization_marks_same_count_structural_change(self):
        diff = mpp_extract._diff_ep(
            _same_count_reorder_old_ep(),
            _same_count_reorder_new_ep(),
            "Genesis",
            1,
            1,
        )

        mpp_classify.classify_diffs([diff])
        serialized = mpp_json._serialize_diff(diff)
        self.assertTrue(serialized["template_structure_changed"])
        self.assertNotIn("templates_added", serialized)
        self.assertNotIn("templates_removed", serialized)

    def test_diff_ep_detects_nested_same_count_relocation(self):
        diff = mpp_extract._diff_ep(
            _nested_relocation_old_ep(),
            _nested_relocation_new_ep(),
            "Genesis",
            1,
            2,
        )

        self.assertIsNotNone(diff)
        self.assertFalse(diff["text_changed"])

    def test_diff_ep_ignores_equivalent_historical_param_formats(self):
        diff = mpp_extract._diff_ep(
            _format_equivalent_old_ep(),
            _format_equivalent_new_ep(),
            "Genesis",
            1,
            3,
        )

        self.assertIsNone(diff)

    def test_diff_ep_ignores_new_note_wrapping_existing_structure(self):
        diff = mpp_extract._diff_ep(
            _new_note_only_old_ep(),
            _new_note_only_new_ep(),
            "Genesis",
            1,
            4,
        )

        self.assertIsNone(diff)

    def test_diff_ep_ignores_existing_note_scope_expansion(self):
        diff = mpp_extract._diff_ep(
            _expanded_note_scope_old_ep(),
            _expanded_note_scope_new_ep(),
            "Genesis",
            1,
            5,
        )

        self.assertIsNone(diff)


if __name__ == "__main__":
    unittest.main()
