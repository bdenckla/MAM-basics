"""Unit tests for the continuous-grammaticality PCFG core (issue #11).

Hermetic: builds tiny trees by hand (no committed corpus needed) and pins the
production extraction, add-lambda smoothing, and tree scoring.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_grammaticality.py -v
"""

import math

import pytest

from accgram import grammaticality as g
from accgram.tree import add_leaves, make_node, tree_to_obj


def _two_leaf_obj():
    """Minimal verse: silluq_clause -> (merkha tipexa) (silluq)."""
    return tree_to_obj(
        make_node(
            "silluq_clause",
            add_leaves("tipexa_phrase", "merkha", "tipexa"),
            add_leaves("silluq_phrase", "silluq"),
        )
    )


def test_iter_productions_covers_start_internal_and_leaf():
    obj = _two_leaf_obj()
    prods = set(g.iter_productions(obj))
    assert prods == {
        ("START", ("ROOT", "silluq_clause")),
        ("silluq_clause", ("BIN", "tipexa_phrase", "silluq_phrase")),
        ("tipexa_phrase", ("LEX", ("merkha", "tipexa"))),
        ("silluq_phrase", ("LEX", ("silluq",))),
    }


def test_accent_count_sums_leaf_names():
    # two leaves carrying 2 + 1 accent names
    assert g.accent_count(_two_leaf_obj()) == 3


def test_logprob_add_lambda_on_seen_production():
    pcfg = g.estimate_pcfg([_two_leaf_obj()])
    # silluq_clause has exactly one rhs seen once: p = (1+lambda)/(1 + lambda*(1+1))
    expected = math.log((1 + g.LAMBDA) / (1 + g.LAMBDA * 2))
    got = pcfg.logprob("silluq_clause", ("BIN", "tipexa_phrase", "silluq_phrase"))
    assert got == pytest.approx(expected)


def test_logprob_unseen_rhs_is_finite_and_smaller():
    """A never-attested-but-grammatical production scores low-but-finite (repairs)."""
    pcfg = g.estimate_pcfg([_two_leaf_obj()])
    seen = pcfg.logprob("silluq_clause", ("BIN", "tipexa_phrase", "silluq_phrase"))
    unseen = pcfg.logprob("silluq_clause", ("BIN", "zaqef_phrase", "silluq_phrase"))
    assert math.isfinite(unseen)
    assert unseen < seen


def test_logprob_unknown_lhs_floors():
    pcfg = g.estimate_pcfg([_two_leaf_obj()])
    assert pcfg.logprob("no_such_clause", ("BIN", "a", "b")) == pytest.approx(
        math.log(0.5)
    )


def test_rarer_production_scores_lower():
    """Estimate from a corpus where one rhs dominates; the rare rhs must score lower."""
    common = tree_to_obj(add_leaves("zaqef_phrase", "munax", "zaqef"))
    rare = tree_to_obj(add_leaves("zaqef_phrase", "zaqefgadol"))
    pcfg = g.estimate_pcfg([common, common, common, rare])
    lp_common = pcfg.logprob("zaqef_phrase", ("LEX", ("munax", "zaqef")))
    lp_rare = pcfg.logprob("zaqef_phrase", ("LEX", ("zaqefgadol",)))
    assert lp_common > lp_rare


def test_score_obj_sums_per_node_logprobs():
    obj = _two_leaf_obj()
    pcfg = g.estimate_pcfg([obj])
    total, per_node = g.score_obj(pcfg, obj)
    assert total == pytest.approx(math.fsum(lp for _, _, lp in per_node))
    assert len(per_node) == 4  # START + internal + 2 leaves


def test_bigram_baseline_scores_finite():
    model = g.estimate_bigram([["A", "B", "C"], ["A", "B"]])
    assert math.isfinite(g.score_bigram(model, ["A", "B"]))
    # an unseen transition is still finite (smoothed), not -inf
    assert math.isfinite(g.score_bigram(model, ["Z", "Q"]))
