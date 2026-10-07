import unittest

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import ws_tmpl2 as wtp
from versification_and_cantillation import doc as vc_doc
from versification_and_cantillation import generate_doc as vc_generate_doc
from versification_and_cantillation import strands as vc_strands

_CURRENT_DOC_PATH = (
    paths.repo_root()
    / "gh-pages"
    / "MAM-simple"
    / "versification-and-cantillation.html"
)


def _joined_skel(words):
    return "".join(vc_strands._skel(w) for w in words)


class TestVersificationAndCantillationDoc(unittest.TestCase):
    maxDiff = None

    def test_full_generated_doc_matches_current_doc(self):
        expected = _CURRENT_DOC_PATH.read_text(encoding="utf-8")
        books_mpu = plus.read_parsed_plus_bk39s(
            (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER),
            paths.mam_parsed_path(),
        )

        self.assertEqual(vc_doc.render_full_html(books_mpu), expected)

    def test_generate_doc_reports_up_to_date(self):
        # The checked-in file must already match what the generator produces.
        self.assertTrue(vc_generate_doc.check_output_matches())


class TestStrandWordExtraction(unittest.TestCase):
    """Issue #199: _strand_word_text must not drop a top-level non-מ:כפול template (e.g. a
    ketiv/qere) from the flat strand — Deut 5:9 carries its last word inside a top-level כו״ק,
    and dropping it made first/last-word extraction return the bare sof pasuq that follows.
    """

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.books = plus.read_parsed_plus_bk39s(
            (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER), paths.mam_parsed_path()
        )

    def test_every_strand_word_of_a_dual_cant_verse_has_letters(self):
        # The rule that failure broke: a dropped word leaves a token with no letters, such as
        # that bare sof pasuq.  Checked in both strands of every verse that holds a מ:כפול
        # unit, and no wider: elsewhere a top-level נוסח still awaits Ben's projection decision
        # (doc/PLAN-deferred-template-projection-decisions.md, "7. Versification-and-cantillation
        # page Scripture projection").
        dual_verses = 0
        for book in self.books.values():
            vp = book["verses_plus"]
            for bcvt, minirow in vp.items():
                if not any(
                    wtp.is_template_with_name(wtel, vc_strands._DUALCANT)
                    for wtel in minirow.EP
                ):
                    continue
                dual_verses += 1
                bk, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvt)
                for param in (vc_strands._TAXTON, vc_strands._ELYON):
                    with self.subTest(verse=(bk, chnu, vrnu), param=param):
                        words = vc_strands._strand_words(vp, bk, chnu, vrnu, param)
                        self.assertTrue(words)
                        self.assertEqual(
                            [w for w in words if not vc_strands._skel(w)], []
                        )
        self.assertTrue(dual_verses)


class TestStrandBalancer(unittest.TestCase):
    """The letter-equalizing pass of issue #201: every taxton/elyon column the doc emits
    must be letter-equal at both boundaries after balancing, and the balancer must fail
    loudly on an input it cannot reconcile."""

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.books = plus.read_parsed_plus_bk39s(
            (tbn.BK_EXODUS, tbn.BK_NUMBERS, tbn.BK_DEUTER),
            paths.mam_parsed_path(),
        )

    def test_every_column_pair_is_letter_equal(self):
        # The umbrella guard: walk *every* T/E column pair (early, late, Sabbath, and both
        # Deuteronomy-appendix tables), balance its boundaries, and assert the displayed
        # taxton and elyon sides share a letter skeleton at each end. This is the same
        # check gather_examples' balanced_pair enforces inline; running it here over the whole
        # column list makes any future silent letter-inequality a test failure.
        columns = vc_strands.build_columns(self.books)
        self.assertTrue(columns)
        for col in columns:
            with self.subTest(column=col["label"]):
                t_first, t_last, e_first, e_last = vc_strands._balanced_sides(
                    col["t_words"], col["e_words"], label=col["label"]
                )
                self.assertEqual(_joined_skel(t_first), _joined_skel(e_first))
                self.assertEqual(_joined_skel(t_last), _joined_skel(e_last))

    def test_balancer_raises_loudly_on_irreconcilable_input(self):
        # Two strands that share no letter prefix cannot be letter-equalized by pulling;
        # the balancer must raise (not silently emit an unequal pair), naming the column.
        with self.assertRaises(AssertionError) as ctx:
            vc_strands.balanced_pair(
                ["אָב"],
                ["גָּד"],
                label="stub column",
                t_render=lambda first, last: "",
                e_render=lambda first, last: "",
            )
        self.assertIn("stub column", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
