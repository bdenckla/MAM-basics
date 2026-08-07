import unittest

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from versification_and_cantillation import doc as vc_doc
from versification_and_cantillation import generate_doc as vc_generate_doc
from versification_and_cantillation import strands as vc_strands

_CURRENT_DOC_PATH = (
    paths.sibling_repo("MAM-simple")
    / "gh-pages"
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
        books = plus.read_parsed_plus_bk39s(
            (tbn.BK_EXODUS, tbn.BK_DEUTER), paths.mam_parsed_path()
        )
        cls.exo = books[tbn.BK_EXODUS]["verses_plus"]
        cls.deu = books[tbn.BK_DEUTER]["verses_plus"]

    def _last(self, vp, bk, ch, vr, param):
        # _strand_words already returns a word list (see _strand_word_text().split()).
        return vc_strands._strand_words(vp, bk, ch, vr, param)[-1]

    def test_deut_5_9_last_word_is_the_qere_not_the_sof_pasuq(self):
        # Before the fix this returned the bare "׃": the top-level כו״ק holding the qere
        # מִצְוֺתָֽי fell through _strand_word_text and vanished from the strand.
        expected = "מִצְוֺתָֽי׃"  # qere מִצְוֺתָֽי + the trailing sof pasuq
        for param in (vc_strands._TAXTON, vc_strands._ELYON):
            with self.subTest(param=param):
                self.assertEqual(
                    self._last(self.deu, tbn.BK_DEUTER, 5, 9, param), expected
                )

    def test_exodus_20_5_and_deut_5_9_agree_at_the_verse_end(self):
        # The whole point of the bug report: the two Decalogues in fact agree at this endpoint
        # (both read the qere), so a correct extraction makes them equal — the earlier "Exodus
        # vs Deuteronomy differ" was purely the dropped-template artifact.
        for param in (vc_strands._TAXTON, vc_strands._ELYON):
            with self.subTest(param=param):
                ex_last = self._last(self.exo, tbn.BK_EXODUS, 20, 5, param)
                de_last = self._last(self.deu, tbn.BK_DEUTER, 5, 9, param)
                self.assertEqual(de_last, ex_last)
                self.assertEqual(
                    vc_strands._strip_pointing(de_last),
                    vc_strands._strip_pointing(ex_last),
                )


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
        # early 5 + Sabbath 4 + late 4 + Deut-Sabbath 4 + Deut-late 4 = 21 columns.
        self.assertEqual(len(columns), 21)
        for col in columns:
            with self.subTest(column=col["label"]):
                t_first, t_last, e_first, e_last = vc_strands._balanced_sides(
                    col["t_words"], col["e_words"], label=col["label"]
                )
                self.assertEqual(_joined_skel(t_first), _joined_skel(e_first))
                self.assertEqual(_joined_skel(t_last), _joined_skel(e_last))

    def test_balancer_pulls_the_leading_lo_columns(self):
        # The two columns that actually diverge (MAM Exod 20:2b and 20:3): each pulls one word
        # inward on both sides so the taxton's maqaf-joined לֹא and the elyon's free לֹא align.
        columns = {c["label"]: c for c in vc_strands.build_columns(self.books)}
        for label in ("early 20:2b", "early 20:3"):
            with self.subTest(column=label):
                col = columns[label]
                t_first, _, e_first, _ = vc_strands._balanced_sides(
                    col["t_words"], col["e_words"], label=label
                )
                self.assertEqual(len(t_first), 2)
                self.assertEqual(len(e_first), 2)
                self.assertEqual(_joined_skel(t_first), _joined_skel(e_first))

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
