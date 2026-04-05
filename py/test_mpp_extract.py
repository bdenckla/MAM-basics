import unittest

from pydiff_mpp import mpp_classify, mpp_extract, mpp_json


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


class TemplateMultiplicityDiffTests(unittest.TestCase):
    def test_multiset_delta_preserves_duplicate_template_additions(self):
        added, removed = mpp_extract._template_name_multiset_delta(
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


if __name__ == "__main__":
    unittest.main()
