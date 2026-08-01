"""Smoke tests for the poetic (Three Books) PLY grammar.

The poetic grammar (accgram.poetic_ply_grammar) is derived from Yeivin ITM
#358-374, not from a C oracle, so these tests pin two things:

  1. the LALR table builds with no shift/reduce or reduce/reduce conflicts;
  2. hand-built poetic verse token streams parse into trees whose nesting matches
     Yeivin's disjunctive hierarchy (oleh-we-yored > atnax > revia mugrash >
     silluq; revia gadol / dexi / tsinnor / revia qatan under them; pazer and
     legarmeh as the lesser dividers).

These are structural, not corpus-validated; they exercise the grammar, not a
golden oracle output.  Token-type names come from accgram.poetic_accent_names so
the (variable) transliterations are never re-typed as literals here.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_poetic_ply_grammar.py -v
"""

from accgram import poetic_accent_names as pan
from accgram.poetic_ply_grammar import (
    build_parser,
    collapse_repeated_tsinnor,
    parse_tokens,
    parse_tokens_accepting_repeats,
    parse_tokens_diagnostic,
)
from accgram.tree import print_tree


def _verse(*accents):
    """Build a (type, leaf) token stream: TILDE, accents..., SOFPASUQ.

    The leaf is just the lowercased token type (these grammar tests don't run the
    scanner, so the display string is arbitrary).
    """
    toks = [(pan.TILDE, "")]
    toks += [(a, a.lower()) for a in accents]
    toks.append((pan.SOFPASUQ, "sof pasuq"))
    return toks


def test_builds_without_conflicts():
    _parser, warnings = build_parser(capture_warnings=True)
    assert warnings.strip() == ""


def test_silluq_only():
    parser = build_parser()
    tree = parse_tokens(parser, _verse(pan.MUNAX, pan.SILLUQ))
    assert tree is not None
    assert print_tree(tree, 0) == "0 silluq_phrase\n  munax silluq \n"


def test_atnax_divided_verse():
    """A short verse: atnax is the great divider, silluq ends it."""
    parser = build_parser()
    tree = parse_tokens(parser, _verse(pan.MERKHA, pan.ATNAX, pan.MERKHA, pan.SILLUQ))
    assert tree is not None
    assert print_tree(tree, 0) == (
        "0 silluq_clause\n"
        "  1 atnax_phrase\n"
        "    merkha atnax \n"
        "  1 silluq_phrase\n"
        "    merkha silluq \n"
    )


def test_revia_mugrash_before_silluq():
    """Revia mugrash is the near divider before silluq, under atnax (#366)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.MUNAX,
            pan.ATNAX,
            pan.MERKHA,
            pan.REVIA_MUGRASH,
            pan.TARXA,
            pan.MUNAX,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    assert "revia_mugrash_phrase" in out
    # revia mugrash nests inside the second-half silluq_clause, below atnax
    assert out.index("atnax_phrase") < out.index("revia_mugrash_phrase")


def test_oleh_weyored_is_topmost_divider():
    """oleh-we-yored divides the whole verse; atnax divides its second half (#361)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.REVIA_GADOL,
            pan.MERKHA,
            pan.REVIA_QATAN,
            pan.GALGAL,
            pan.OLEH_WEYORED,
            pan.MUNAX,
            pan.ATNAX,
            pan.MERKHA,
            pan.REVIA_MUGRASH,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    # top node is the verse silluq_clause; its left child is the oleh clause
    assert tree.label == "silluq_clause"
    assert tree.left.label == "oleh_weyored_clause"
    out = print_tree(tree, 0)
    # revia qatan stands immediately before oleh-we-yored
    assert "revia_qatan_phrase" in out
    assert "oleh_weyored_phrase" in out


def test_full_hierarchy_pazer_legarmeh_dexi_tsinnor():
    """A verse exercising every rank: pazer/legarmeh under revia gadol, tsinnor
    before oleh, dexi under atnax."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.PAZER,
            pan.LEGARMEH,
            pan.REVIA_GADOL,
            pan.MERKHA,
            pan.TSINNOR,
            pan.GALGAL,
            pan.OLEH_WEYORED,
            pan.MUNAX,
            pan.DEXI,
            pan.MERKHA,
            pan.ATNAX,
            pan.MERKHA,
            pan.REVIA_MUGRASH,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    for label in (
        "pazer_phrase",
        "legarmeh_phrase",
        "revia_gadol_clause",
        "tsinnor_phrase",
        "oleh_weyored_phrase",
        "dexi_phrase",
        "atnax_phrase",
        "revia_mugrash_phrase",
        "silluq_phrase",
    ):
        assert label in out, label


def test_conj_absorbs_metsunnar_and_shalshelet_qetannah():
    """Plan C: the fused-tsinnorit servi (mahapakh/merkha metsunnar) and the
    conjunctive shalshelet qetannah are ordinary servi -- absorbed by the permissive
    `conj` chain before a disjunctive, with no effect on the disjunctive skeleton."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.MAHAPAKH_METSUNNAR,
            pan.MERKHA_METSUNNAR,
            pan.SHALSHELET_QETANNAH,
            pan.ATNAX,
            pan.MERKHA,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    # the three new servi sit inside the atnax phrase; skeleton is still atnax | silluq
    assert "atnax_phrase" in out
    assert tree.label == "silluq_clause"
    # dropping the three servi leaves the same disjunctive skeleton (servus-neutral)
    bare = parse_tokens(parser, _verse(pan.ATNAX, pan.MERKHA, pan.SILLUQ))
    assert [n.label for n in (tree.left, tree.right)] == [
        bare.left.label,
        bare.right.label,
    ]


def test_merkha_azla_bang_is_unparseable():
    """Plan D (revised): the same-letter merkha!azla bang is a lexical anomaly, NOT a
    licit servus -- two primary conjunctives on one letter.  The scanner emits it
    faithfully, but the grammar has no `conj` terminal for it, so any verse carrying one
    dead-ends to NO_PARSE (the poetic lexical-error surface, like STRAY_ACCENT)."""
    parser = build_parser()
    tree, error = parse_tokens_diagnostic(
        parser, _verse(pan.MERKHA_AZLA, pan.ATNAX, pan.MERKHA, pan.SILLUQ)
    )
    assert tree is None
    assert error is not None and error.token_type == pan.MERKHA_AZLA


def test_stray_accent_is_unparseable():
    """Plan C fail-fast: STRAY_ACCENT has no grammar terminal, so any verse carrying
    one is a NO_PARSE (the poetic-native error surface)."""
    parser = build_parser()
    tree, error = parse_tokens_diagnostic(parser, _verse(pan.STRAY_ACCENT, pan.SILLUQ))
    assert tree is None
    assert error is not None and error.token_type == pan.STRAY_ACCENT


def test_shalshelet_gedolah_before_silluq():
    parser = build_parser()
    tree = parse_tokens(
        parser, _verse(pan.SHALSHELET_GEDOLAH, pan.TARXA, pan.MUNAX, pan.SILLUQ)
    )
    assert tree is not None
    assert "shalshelet_gedolah_phrase" in print_tree(tree, 0)


# --- Phase 3: lower disjunctives directly subdividing higher domains ------------
# L (MAM-confirmed) uses a lower disjunctive directly within a higher domain when
# the unit is short, exactly as the prose silluq/atnax domains admit their lower
# dividers.  These pin the rank-ordered near-divider cascades added in Phase 3.


def test_legarmeh_directly_under_atnax():
    """legarmeh subdivides the atnax domain directly (Ps 31:15)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.LEGARMEH,
            pan.MUNAX,
            pan.MUNAX,
            pan.ATNAX,
            pan.REVIA_MUGRASH,
            pan.MERKHA,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    # legarmeh nests as a subdivider inside the atnax clause, above atnax's phrase
    assert "atnax_clause" in out
    assert out.index("legarmeh_phrase") < out.index("atnax_phrase")


def test_legarmeh_directly_before_silluq_under_revia_mugrash():
    """revia mugrash near-divides silluq, then legarmeh divides the final unit
    (Ps 3:1, ATNAX REVIA_MUGRASH LEGARMEH SILLUQ)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.MERKHA,
            pan.ATNAX,
            pan.REVIA_MUGRASH,
            pan.LEGARMEH,
            pan.ILLUY,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    # legarmeh is the last divider, immediately above the silluq phrase
    assert out.index("revia_mugrash_phrase") < out.index("legarmeh_phrase")
    assert out.index("legarmeh_phrase") < out.index("silluq_phrase")


def test_dexi_directly_before_silluq():
    """dexi may stand directly before silluq (Ps, ATNAX DEXI SILLUQ -- faithful to
    L; an L/MAM divergence the xcheck flags separately)."""
    parser = build_parser()
    tree = parse_tokens(
        parser, _verse(pan.MERKHA, pan.ATNAX, pan.DEXI, pan.MUNAX, pan.SILLUQ)
    )
    assert tree is not None
    out = print_tree(tree, 0)
    assert out.index("atnax_phrase") < out.index("dexi_phrase")
    assert out.index("dexi_phrase") < out.index("silluq_phrase")


def test_pazer_directly_before_silluq():
    """pazer directly before silluq in a short superscription (Ps 18:2, 30:1)."""
    parser = build_parser()
    tree = parse_tokens(parser, _verse(pan.PAZER, pan.TARXA, pan.MUNAX, pan.SILLUQ))
    assert tree is not None
    out = print_tree(tree, 0)
    assert "pazer_phrase" in out
    assert out.index("pazer_phrase") < out.index("silluq_phrase")


def test_tsinnor_subdivides_revia_qatan_before_oleh():
    """When tsinnor and revia qatan both precede oleh-we-yored, revia qatan is the
    near divider and tsinnor subdivides its domain (Ps 13:6,
    LEGARMEH TSINNOR REVIA_QATAN OLEH_WEYORED ...)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.LEGARMEH,
            pan.TSINNOR,
            pan.REVIA_QATAN,
            pan.OLEH_WEYORED,
            pan.MERKHA,
            pan.ATNAX,
            pan.MERKHA,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    # revia_qatan_clause contains a tsinnor subdivision, which contains legarmeh
    assert "revia_qatan_clause" in out
    assert out.index("tsinnor_phrase") < out.index("revia_qatan_phrase")
    assert out.index("legarmeh_phrase") < out.index("tsinnor_phrase")


def test_revia_qatan_requires_merkha_servant():
    """Breuer Ch 11 §17, confirmed by both witnesses (servi_before oracle): the
    servant adjacent to a small revia' is merkha (a mahapakh may precede it).  A
    merkha-served small revia parses; a non-merkha adjacent servant (here munax) does
    not, even though the position is otherwise valid.  This rule is faithful but
    currently inert on the corpus (L marks merkha in 125/125 cases)."""
    parser = build_parser()
    tail = (pan.OLEH_WEYORED, pan.MERKHA, pan.ATNAX, pan.MERKHA, pan.SILLUQ)
    # merkha adjacent, with a mahapakh before it ("a [mahapakh] precedes it") -> parses
    ok = parse_tokens(parser, _verse(pan.MAHAPAKH, pan.MERKHA, pan.REVIA_QATAN, *tail))
    assert ok is not None
    assert "revia_qatan_phrase" in print_tree(ok, 0)
    # munax adjacent to the small revia -> rejected (no parse)
    bad = parse_tokens(parser, _verse(pan.MUNAX, pan.REVIA_QATAN, *tail))
    assert bad is None


def test_missing_silluq_recovers_as_error_tree():
    """Category A: a verse with no silluq code (servi then sof pasuq) recovers into
    a tree whose silluq_phrase is ERROR, preserving the rest of the structure
    (Ps 37:31, MUNAX MUNAX ATNAX TARXA MUNAX)."""
    parser = build_parser()
    tree = parse_tokens(
        parser, _verse(pan.MUNAX, pan.MUNAX, pan.ATNAX, pan.TARXA, pan.MUNAX)
    )
    assert tree is not None
    out = print_tree(tree, 0)
    assert "atnax_phrase" in out  # the rest of the verse is preserved
    assert "ERROR" in out  # the absent silluq is flagged
    assert "silluq_phrase" in out


def test_misplaced_disjunctive_stays_no_parse():
    """The *raw* scanner reading of Ps 68:20 (tsinnor before a legarmeh) is a hierarchy
    violation the grammar must NOT mask by error recovery -- parse_tokens returns None.

    In the live pipeline this verse no longer surfaces as NO_PARSE: poetic_reconcile
    corrects the scanner's blanket legarmeh to MAM's paseq and recovers the unmarked
    oleh-we-yored, and the reconciled tokens parse (see test_poetic_reconcile).  This
    test pins the grammar property on the *unreconciled* sequence."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.MAHAPAKH,
            pan.MUNAX,
            pan.TSINNOR,
            pan.LEGARMEH,
            pan.MERKHA,
            pan.REVIA_MUGRASH,
            pan.MAHAPAKH,
            pan.ILLUY,
            pan.SILLUQ,
        ),
    )
    assert tree is None


_PS_17_14_ACCENTS = [
    pan.MERKHA,
    pan.LEGARMEH,
    pan.PAZER,
    pan.ILLUY,
    pan.REVIA_GADOL,
    pan.MERKHA,
    pan.TSINNOR,
    pan.TSINNOR,
    pan.GALGAL,
    pan.OLEH_WEYORED,
    pan.MERKHA,
    pan.ATNAX,
    pan.MERKHA,
    pan.REVIA_MUGRASH,
    pan.SILLUQ,
]


def test_diagnostic_pinpoints_the_stall_token():
    """parse_tokens_diagnostic reports WHERE a NO_PARSE verse dead-ends, not just
    that it failed.  Ps 17:14's shape (double tsinnor + galgal then oleh-we-yored)
    parses through the GALGAL and stalls at the OLEH_WEYORED that follows it -- the
    1-based ordinal among the verse's accents (TILDE excluded).

    This is the *raw* grammar verdict; the live pipeline accepts the verse via
    parse_tokens_accepting_repeats (see the next test), which keeps this diagnostic
    pure and the stall locus inspectable."""
    parser = build_parser()
    accents = _PS_17_14_ACCENTS
    tree, error = parse_tokens_diagnostic(parser, _verse(*accents))
    assert tree is None
    assert error is not None
    assert error.token_type == pan.OLEH_WEYORED
    assert error.accent_index == 10  # the 10th accent (1-based); accents[9]
    assert accents[error.accent_index - 1] == pan.OLEH_WEYORED


def test_repeated_tsinnor_accepted_as_single_divider():
    """Ps 17:14's double tsinnor is accepted by parse_tokens_accepting_repeats: a
    repeated divider counts once, so collapsing the run to a single TSINNOR lets the
    existing tsinnor productions parse it cleanly -- even though the raw grammar (the
    test above) stalls at the following oleh-we-yored.  The canonical token list is
    left untouched (both tsinnor marks remain), so the disjunctive cross-check is
    unaffected."""
    parser = build_parser()
    toks = _verse(*_PS_17_14_ACCENTS)
    tree, error = parse_tokens_accepting_repeats(parser, toks)
    assert tree is not None  # accepted: a clean parse
    assert error is None
    # the input is not mutated -- both tsinnor marks still present
    assert sum(1 for t, _ in toks if t == pan.TSINNOR) == 2
    # the mechanism: a run of consecutive TSINNOR collapses to one
    collapsed = [t for t, _ in collapse_repeated_tsinnor(toks)]
    assert collapsed.count(pan.TSINNOR) == 1


def test_accepting_repeats_leaves_other_no_parse_untouched():
    """With no repeated tsinnor there is nothing to collapse, so the accepting path
    returns the raw NO_PARSE verdict unchanged -- it rescues only repeated dividers.
    Uses the raw (unreconciled) Ps 68:20 sequence, a single-tsinnor hierarchy
    violation that must stay NO_PARSE."""
    parser = build_parser()
    toks = _verse(
        pan.MAHAPAKH,
        pan.MUNAX,
        pan.TSINNOR,
        pan.LEGARMEH,
        pan.MERKHA,
        pan.REVIA_MUGRASH,
        pan.MAHAPAKH,
        pan.ILLUY,
        pan.SILLUQ,
    )
    assert parse_tokens_diagnostic(parser, toks)[0] is None
    assert parse_tokens_accepting_repeats(parser, toks)[0] is None


def test_diagnostic_returns_no_error_on_clean_parse():
    parser = build_parser()
    tree, error = parse_tokens_diagnostic(parser, _verse(pan.MUNAX, pan.SILLUQ))
    assert tree is not None
    assert error is None


def test_pazer_directly_under_atnax():
    """pazer subdivides the atnax domain directly, with legarmeh below it
    (LEGARMEH PAZER ATNAX REVIA_MUGRASH SILLUQ)."""
    parser = build_parser()
    tree = parse_tokens(
        parser,
        _verse(
            pan.LEGARMEH,
            pan.PAZER,
            pan.ATNAX,
            pan.REVIA_MUGRASH,
            pan.SILLUQ,
        ),
    )
    assert tree is not None
    out = print_tree(tree, 0)
    assert "atnax_clause" in out
    assert out.index("pazer_phrase") < out.index("atnax_phrase")
    assert out.index("legarmeh_phrase") < out.index("pazer_phrase")
