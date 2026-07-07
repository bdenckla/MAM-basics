import unittest

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from versification_and_cantillation import doc as vc_doc
from versification_and_cantillation import generate_doc as vc_generate_doc

_CURRENT_DOC_PATH = (
    paths.sibling_repo("MAM-simple") / "gh-pages" / "versification-and-cantillation.html"
)


class TestVersificationAndCantillationDoc(unittest.TestCase):
    maxDiff = None

    def test_full_generated_doc_matches_current_doc(self):
        expected = _CURRENT_DOC_PATH.read_text(encoding="utf-8")
        books_mpu = plus.read_parsed_plus_bk39s(
            (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER)
        )

        self.assertEqual(vc_doc.render_full_html(books_mpu), expected)

    def test_generate_doc_reports_up_to_date(self):
        # The checked-in file must already match what the generator produces.
        self.assertTrue(vc_generate_doc.check_output_matches())


if __name__ == "__main__":
    unittest.main()
