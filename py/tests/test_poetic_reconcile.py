"""Unit tests for accgram.poetic_reconcile.

Two corrections the M-C source cannot express, applied before the grammar parses:

  1. legarmeh-vs-paseq: a scanner LEGARMEH that MAM has as a narrow-sense paseq is demoted to
     its underlying conjunctive servus (azla 63 / mahapakh 70), the paseq swallowed.
  2. the unmarked oleh-we-yored (Yeivin #363): a charitable, parse-driven pass reads
     one ambiguous merkha as a yored iff that uniquely makes the verse parse.

The two named ungrammatical (Ps 68:20, Pr 30:15) need *both* corrections; the two unrelated
NO_PARSE verses (Ps 17:14, Job 31:15) must stay NO_PARSE under reconciliation.  (Ps
17:14's double tsinnor is separately accepted one layer up, at the parse boundary, by
parse_tokens_accepting_repeats -- not here; reconcile leaves it NO_PARSE.)

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_poetic_reconcile.py -v
"""

from accgram import poetic_accent_names as pan
from accgram import poetic_reconcile as pr
from accgram.poetic_ply_grammar import build_parser, parse_tokens
from accgram.poetic_scanner import scan_verse
from tests.mc_marks import mc_to_marks

# Bodies are written in the legacy M-C encoding for readability and converted to the
# Phase-2 mark alphabet (issue wlc-utils#9) at each use.


def _types(tokens):
    return [t for t, _leaf in tokens]


# --- legarmeh -> servus demotion (MAM oracle) ---------------------------------


def test_underlying_servi_reads_the_conjunctive_under_each_legarmeh():
    # azla(63)+paseq(05), then mahapakh(70)+paseq(05): azla then mahapakh servus.
    assert pr._legarmeh_underlying_servi(mc_to_marks("QF63H05 HA70B05")) == [
        pan.AZLA,
        pan.MAHAPAKH,
    ]


def test_demote_when_mam_reads_no_legarmeh():
    # One mahapakh-legarmeh word; MAM has no disjunctive there (a narrow-sense paseq).
    tokens = [(pan.TILDE, ""), (pan.LEGARMEH, "legarmeh"), (pan.SOFPASUQ, "sof pasuq")]
    out = pr._demote_mam_paseq(mc_to_marks("YO70WM05"), tokens, mam_disjunctives=[])
    # The legarmeh becomes its underlying mahapakh servus; the paseq is dropped.
    assert _types(out) == [pan.TILDE, pan.MAHAPAKH, pan.SOFPASUQ]


def test_no_demotion_when_mam_also_reads_legarmeh():
    tokens = [(pan.TILDE, ""), (pan.LEGARMEH, "legarmeh"), (pan.SOFPASUQ, "sof pasuq")]
    out = pr._demote_mam_paseq(
        mc_to_marks("QF63H05"), tokens, mam_disjunctives=[pan.LEGARMEH]
    )
    assert _types(out) == [pan.TILDE, pan.LEGARMEH, pan.SOFPASUQ]


def test_demotion_keeps_the_legarmeh_mam_confirms_and_drops_the_one_it_does_not():
    # Pr 30:15 shape: first legarmeh (azla) is a real legarmeh in MAM; the second
    # (mahapakh) is a paseq + an oleh-we-yored MAM puts on the next word.
    tokens = [
        (pan.TILDE, ""),
        (pan.LEGARMEH, "legarmeh"),
        (pan.TSINNOR, "tsinnor"),
        (pan.LEGARMEH, "legarmeh"),
        (pan.SOFPASUQ, "sof pasuq"),
    ]
    out = pr._demote_mam_paseq(
        mc_to_marks("QF63H05 BFNOWT02 HA70B05"),
        tokens,
        mam_disjunctives=[pan.LEGARMEH, pan.TSINNOR, pan.OLEH_WEYORED],
    )
    assert _types(out) == [
        pan.TILDE,
        pan.LEGARMEH,
        pan.TSINNOR,
        pan.MAHAPAKH,
        pan.SOFPASUQ,
    ]


def test_demote_is_a_noop_when_verse_is_absent_from_mam():
    tokens = [(pan.TILDE, ""), (pan.LEGARMEH, "legarmeh"), (pan.SOFPASUQ, "sof pasuq")]
    out = pr._demote_mam_paseq(mc_to_marks("YO70WM05"), tokens, mam_disjunctives=None)
    assert out is tokens


# --- charitable oleh recovery (parse-driven) ----------------------------------


def test_charitable_oleh_uniquely_recovers_an_unmarked_yored():
    # Ps 68:20 after legarmeh->mahapakh demotion: NO_PARSE until the bare merkha of the
    # unmarked oleh-we-yored is read as a yored.  Exactly one promotion parses.
    parser = build_parser()
    tokens = [
        (pan.TILDE, ""),
        (pan.MAHAPAKH, "mahapakh"),
        (pan.MUNAX, "munax"),
        (pan.TSINNOR, "tsinnor"),
        (pan.MAHAPAKH, "mahapakh"),
        (pan.MERKHA, "merkha"),
        (pan.REVIA_MUGRASH, "revia mugrash"),
        (pan.MAHAPAKH, "mahapakh"),
        (pan.ILLUY, "illuy"),
        (pan.SILLUQ, "silluq"),
        (pan.SOFPASUQ, "sof pasuq"),
    ]
    assert parse_tokens(parser, tokens) is None
    recovered = pr._charitable_oleh(tokens, parser)
    assert recovered is not None
    assert parse_tokens(parser, recovered) is not None
    assert recovered[5][0] == pan.OLEH_WEYORED


def test_charitable_oleh_is_none_when_no_promotion_parses():
    parser = build_parser()
    # A verse with no merkha cannot be repaired by promoting a merkha.
    tokens = [
        (pan.TILDE, ""),
        (pan.ATNAX, "atnax"),
        (pan.SILLUQ, "silluq"),
        (pan.SOFPASUQ, ""),
    ]
    assert pr._charitable_oleh(tokens, parser) is None


# --- end to end ---------------------------------------------------------------

# The bodies of the two named ungrammatical (M-C source, converted to marks) and their MAM
# disjunctive skeletons.
_PS_68_20 = mc_to_marks(
    "B.F70R74W.K: ):ADON/FY02 YO70WM05 YO71WM YA75(:AMFS-L/F81NW. "
    'HF82/)"70L Y:75$W.(FT/"64NW. SE75LFH00'
)
_PS_68_20_MAM = [pan.TSINNOR, pan.OLEH_WEYORED, pan.REVIA_MUGRASH, pan.SILLUQ]
_PR_30_15 = mc_to_marks(
    'LA95/(:ALW.QF63H05 $:T."71Y BFNOWT02 HA70B05 HA71B $FLO74W$ 13H"N.FH '
    "LO74) TI&:B.A92(:NFH 11)AR:B.A81( LO)-)F71M:RW. HO75WN00"
)
_PR_30_15_MAM = [
    pan.LEGARMEH,
    pan.TSINNOR,
    pan.OLEH_WEYORED,
    pan.DEXI,
    pan.ATNAX,
    pan.REVIA_MUGRASH,
    pan.SILLUQ,
]


def _reconcile(reference, body, mam):
    parser = build_parser()
    verse = scan_verse(reference, body)
    assert parse_tokens(parser, verse.tokens) is None  # NO_PARSE before reconciliation
    tokens = pr.reconcile_tokens(reference, body, list(verse.tokens), mam, parser)
    return parser, tokens


def test_ps_68_20_reconciles_and_matches_mam():
    parser, tokens = _reconcile("Psalms 68:20", _PS_68_20, _PS_68_20_MAM)
    assert parse_tokens(parser, tokens) is not None
    disj = [t for t in _types(tokens) if t in pan.POETIC_DISJUNCTIVES]
    assert disj == _PS_68_20_MAM


def test_pr_30_15_reconciles_and_matches_mam():
    parser, tokens = _reconcile("Proverbs 30:15", _PR_30_15, _PR_30_15_MAM)
    assert parse_tokens(parser, tokens) is not None
    disj = [t for t in _types(tokens) if t in pan.POETIC_DISJUNCTIVES]
    assert disj == _PR_30_15_MAM
