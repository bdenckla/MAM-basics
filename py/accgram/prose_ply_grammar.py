"""PLY yacc grammar: full port of acc2tre.y (Phase E — error recovery included).

Stage 1.  Translates every production of acc2tre.y one-to-one, including the
`error`-token recovery rules that build the 51 ungrammatical ERROR-node trees.

Non-error productions (Phases B–D) cover all clean verses:
  - segolta family (segolta_phrase incl. SHALSHELET, segolta_clause, zarqa/
    pashta/revia_segolta_clause) and its wiring into silluq_clause /
    atnax_clause via segolta_silluq_clause / segolta_atnax_clause;
  - zarqa family (zarqa_phrase, zarqa_clause, legarmeh/geresh/big_telisha/
    pazer_zarqa_clause);
  - METHIGAZAQEF as a zaqef_phrase; MAYELA variants in tipexa_phrase;
  - the remaining pashta_phrase and tevir_phrase servus combinations.

Error productions (Phase E) reproduce yacc's recovery (see the error-recovery
section below): every `error`-token rule builds the same ERROR leaf / ERROR
clause the C action builds and calls p.parser.errok() to mirror yacc's
`yyerrok`.  The two pasuq-level `error` rules (no tree, location line only)
return the LOCATION_ONLY sentinel; they do not fire on the parity corpus (all 51
ungrammatical reduce via `TILDE silluq_clause SOFPASUQ` with ERROR leaves inside).

Grammar actions build trees with tree.make_node / add_leaves, exactly as the
C actions call make_node / add_leaves.  Token values carry the leaf-name string
(yylval.leaf), so add_leaves uses p[i] verbatim.

Deliberate correction (diverging from the C oracle, like MISSING_SOFPASUQ): the C
actions for `MAHAPAKH MAHAPAKH PASHTA` and `MAHAPAKH MERKHA PASHTA` call add_leaves
with count 2 (only $1,$2), an off-by-one that drops the trailing PASHTA leaf -- the
phrase's own disjunctive head.  Every sibling servus+pashta rule keeps all leaves,
so these now pass p[1],p[2],p[3] too (affects Judg 15:13, 1Sam 30:9, Exod 10:13).

Deliberate omission, the third such divergence (#221): acc2tre.y's bare `pasuq : error`
alternative -- no TILDE, no sof pasuq, one `error` symbol and nothing else -- is not ported.
See p_pasuq_error below for the cycle it drives PLY into and for the measurements that say
it has no other reachable effect.
"""

from __future__ import annotations

import sys

from ply import yacc

from accgram.prose_scanner import Token
from accgram.tree import add_leaves, make_node

# All 33 grammar tokens (declared even when unused by subsets, to mirror
# acc2tre.y's %token list and keep the token namespace stable).
tokens = (
    "TILDE",
    "SOFPASUQ",
    # Synthetic end-of-verse marker the scanner appends to a verse missing its sof
    # pasuq (code 00); see p_pasuq_missing_sofpasuq.  Not in acc2tre.y's %token list.
    "MISSING_SOFPASUQ",
    "SILLUQ",
    "ATNAX",
    "SEGOLTA",
    "SHALSHELET",
    "ZAQEF",
    "METHIGAZAQEF",
    "ZAQEFGADOL",
    "REVIA",
    "TIPEXA",
    "ZARQA",
    "PASHTA",
    "YETIV",
    "TEVIR",
    "GERESH",
    "GERSHAYIM",
    "PAZER",
    "PAZERGADOL",
    "TELISHAGEDOLA",
    "LEGARMEH",
    "MUNAX",
    "MAHAPAKH",
    "MAHAPAKHQADMA",
    "MERKHA",
    "MERKHAKEFULA",
    "DARGA",
    "QADMA",
    "AZLA",
    "TELISHAQETANNA",
    "GALGAL",
    "MAYELA",
    "UNKNOWN_ACCENT",
)

start = "pasuq"


# --- pasuq ---------------------------------------------------------------------
def p_pasuq(p):
    "pasuq : TILDE silluq_clause SOFPASUQ"
    p[0] = p[2]


def p_pasuq_missing_sofpasuq(p):
    "pasuq : TILDE silluq_clause MISSING_SOFPASUQ"
    # Extension beyond acc2tre.y: a verse missing its sof pasuq (Unicode SOF PASUQ /
    # code 00) parses normally, but is flagged distinctly with a sof_pasuq_phrase
    # ERROR leaf -- making it an ungrammatical verse rather than a no-output troublemaker.  The
    # ERROR is separate from the silluq_phrase ERROR used for a missing silluq, so
    # the marker correctly identifies the sof pasuq as the absent mark.
    p[0] = make_node("silluq_clause", p[2], add_leaves("sof_pasuq_phrase", "ERROR"))


# --- silluq --------------------------------------------------------------------
def p_silluq_phrase_silluq(p):
    "silluq_phrase : SILLUQ"
    p[0] = add_leaves("silluq_phrase", p[1])


def p_silluq_phrase_merkha(p):
    "silluq_phrase : MERKHA SILLUQ"
    p[0] = add_leaves("silluq_phrase", p[1], p[2])


def p_silluq_clause(p):
    """silluq_clause : silluq_phrase
    | tipexa_silluq_clause
    | zaqef_silluq_clause
    | segolta_silluq_clause
    | atnax_silluq_clause"""
    p[0] = p[1]


def p_tipexa_silluq_clause(p):
    "tipexa_silluq_clause : tipexa_clause silluq_phrase"
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_zaqef_silluq_clause(p):
    """zaqef_silluq_clause : zaqef_clause silluq_phrase
    | zaqef_clause tipexa_silluq_clause
    | zaqef_clause zaqef_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


# Necessitated by one anomalous verse, Ezra 7:13, where atnax does not occur and
# segolta serves as the main clause divider (Yeivin, par. 228).  That verse has no
# zaqef either, oddly enough.
def p_segolta_silluq_clause(p):
    """segolta_silluq_clause : segolta_clause silluq_phrase
    | segolta_clause tipexa_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_atnax_silluq_clause(p):
    """atnax_silluq_clause : atnax_clause silluq_phrase
    | atnax_clause tipexa_silluq_clause
    | atnax_clause zaqef_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


# --- atnax --------------------------------------------------------------------
def p_atnax_phrase_atnax(p):
    "atnax_phrase : ATNAX"
    p[0] = add_leaves("atnax_phrase", p[1])


def p_atnax_phrase_munax(p):
    "atnax_phrase : MUNAX ATNAX"
    p[0] = add_leaves("atnax_phrase", p[1], p[2])


def p_atnax_phrase_munax2(p):
    "atnax_phrase : MUNAX MUNAX ATNAX"
    p[0] = add_leaves("atnax_phrase", p[1], p[2], p[3])


def p_atnax_clause(p):
    """atnax_clause : atnax_phrase
    | tipexa_atnax_clause
    | zaqef_atnax_clause
    | segolta_atnax_clause"""
    p[0] = p[1]


def p_tipexa_atnax_clause(p):
    "tipexa_atnax_clause : tipexa_clause atnax_phrase"
    p[0] = make_node("atnax_clause", p[1], p[2])


def p_zaqef_atnax_clause(p):
    """zaqef_atnax_clause : zaqef_clause atnax_phrase
    | zaqef_clause tipexa_atnax_clause
    | zaqef_clause zaqef_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


def p_segolta_atnax_clause(p):
    """segolta_atnax_clause : segolta_clause atnax_phrase
    | segolta_clause tipexa_atnax_clause
    | segolta_clause zaqef_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


# --- zaqef ---------------------------------------------------------------------
# Revia may precede a zaqef-clause with pashta; if another revia precedes, it may
# be converted to pashta.  Yetiv seems only to be able to substitute for the
# non-revia-replacing pashta.
def p_zaqef_phrase_zaqef(p):
    "zaqef_phrase : ZAQEF"
    p[0] = add_leaves("zaqef_phrase", p[1])


def p_zaqef_phrase_methigazaqef(p):
    # Methiga zaqef looks just like QADMA ZAQEF in the M-C BHS text.
    "zaqef_phrase : METHIGAZAQEF"
    p[0] = add_leaves("zaqef_phrase", p[1])


def p_zaqef_phrase_zaqefgadol(p):
    "zaqef_phrase : ZAQEFGADOL"
    p[0] = add_leaves("zaqef_phrase", p[1])


# See Yeivin on shofar illuy and shofar mekarbel: these signs are often pointed
# differently than plain munax zaqef and munax+munax zaqef in some MSS, but
# here in L they are pointed the same as munaxs before zaqef.
def p_zaqef_phrase_munax(p):
    "zaqef_phrase : MUNAX ZAQEF"
    p[0] = add_leaves("zaqef_phrase", p[1], p[2])


def p_zaqef_phrase_munax2(p):
    "zaqef_phrase : MUNAX MUNAX ZAQEF"
    p[0] = add_leaves("zaqef_phrase", p[1], p[2], p[3])


def p_zaqef_clause(p):
    """zaqef_clause : zaqef_phrase
    | pashta_zaqef_clause
    | revia_zaqef_clause"""
    p[0] = p[1]


def p_pashta_zaqef_clause(p):
    """pashta_zaqef_clause : pashta_clause zaqef_phrase
    | pashta_clause pashta_zaqef_clause
    | pashta_clause revia_zaqef_clause"""
    p[0] = make_node("zaqef_clause", p[1], p[2])


def p_revia_zaqef_clause(p):
    """revia_zaqef_clause : revia_clause zaqef_phrase
    | revia_clause pashta_zaqef_clause
    | revia_clause revia_zaqef_clause"""
    p[0] = make_node("zaqef_clause", p[1], p[2])


# --- segolta -------------------------------------------------------------------
# Pashta below = converted revia.  Segolta is like a strong zaqef.  Shalshelet
# is treated as a segolta_phrase variant (see segolta_phrase below).
def p_segolta_phrase_segolta(p):
    "segolta_phrase : SEGOLTA"
    p[0] = add_leaves("segolta_phrase", p[1])


def p_segolta_phrase_shalshelet(p):
    "segolta_phrase : SHALSHELET"
    p[0] = add_leaves("segolta_phrase", p[1])


def p_segolta_phrase_munax(p):
    "segolta_phrase : MUNAX SEGOLTA"
    p[0] = add_leaves("segolta_phrase", p[1], p[2])


def p_segolta_phrase_munax2(p):
    "segolta_phrase : MUNAX MUNAX SEGOLTA"
    p[0] = add_leaves("segolta_phrase", p[1], p[2], p[3])


def p_segolta_clause(p):
    """segolta_clause : segolta_phrase
    | zarqa_segolta_clause
    | pashta_segolta_clause
    | revia_segolta_clause"""
    p[0] = p[1]


def p_zarqa_segolta_clause(p):
    """zarqa_segolta_clause : zarqa_clause segolta_phrase
    | zarqa_clause zarqa_segolta_clause"""
    p[0] = make_node("segolta_clause", p[1], p[2])


def p_pashta_segolta_clause(p):
    """pashta_segolta_clause : pashta_clause segolta_phrase
    | pashta_clause zarqa_segolta_clause
    | pashta_clause pashta_segolta_clause
    | pashta_clause revia_segolta_clause"""
    p[0] = make_node("segolta_clause", p[1], p[2])


def p_revia_segolta_clause(p):
    """revia_segolta_clause : revia_clause segolta_phrase
    | revia_clause zarqa_segolta_clause
    | revia_clause pashta_segolta_clause
    | revia_clause revia_segolta_clause"""
    p[0] = make_node("segolta_clause", p[1], p[2])


# --- tipexa --------------------------------------------------------------------
def p_tipexa_phrase_tipexa(p):
    "tipexa_phrase : TIPEXA"
    p[0] = add_leaves("tipexa_phrase", p[1])


def p_tipexa_phrase_merkha(p):
    "tipexa_phrase : MERKHA TIPEXA"
    p[0] = add_leaves("tipexa_phrase", p[1], p[2])


def p_tipexa_phrase_darga_merkhakefula(p):
    "tipexa_phrase : DARGA MERKHAKEFULA TIPEXA"
    p[0] = add_leaves("tipexa_phrase", p[1], p[2], p[3])


# Mayela is a variant of tipexa: it can take a tevir before it (Jer 2:31) and
# qadma before it (Dan 4:9,18), unlike a plain conjunctive.
def p_tipexa_phrase_mayela(p):
    "tipexa_phrase : MAYELA"
    p[0] = add_leaves("tipexa_phrase", p[1])


def p_tipexa_phrase_merkha_mayela(p):
    "tipexa_phrase : MERKHA MAYELA"
    p[0] = add_leaves("tipexa_phrase", p[1], p[2])


def p_tipexa_phrase_qadma_mayela(p):
    "tipexa_phrase : QADMA MAYELA"
    p[0] = add_leaves("tipexa_phrase", p[1], p[2])


def p_tipexa_clause(p):
    """tipexa_clause : tipexa_phrase
    | tevir_tipexa_clause
    | pashta_tipexa_clause
    | revia_tipexa_clause"""
    p[0] = p[1]


def p_tevir_tipexa_clause(p):
    """tevir_tipexa_clause : tevir_clause tipexa_phrase
    | tevir_clause tevir_tipexa_clause"""
    p[0] = make_node("tipexa_clause", p[1], p[2])


def p_pashta_tipexa_clause(p):
    """pashta_tipexa_clause : pashta_clause tipexa_phrase
    | pashta_clause tevir_tipexa_clause
    | pashta_clause pashta_tipexa_clause
    | pashta_clause revia_tipexa_clause"""
    p[0] = make_node("tipexa_clause", p[1], p[2])


def p_revia_tipexa_clause(p):
    """revia_tipexa_clause : revia_clause tipexa_phrase
    | revia_clause tevir_tipexa_clause
    | revia_clause pashta_tipexa_clause
    | revia_clause revia_tipexa_clause"""
    p[0] = make_node("tipexa_clause", p[1], p[2])


# --- tevir ---------------------------------------------------------------------
def p_tevir_phrase_tevir(p):
    "tevir_phrase : TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1])


def p_tevir_phrase_darga(p):
    "tevir_phrase : DARGA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2])


def p_tevir_phrase_merkha(p):
    "tevir_phrase : MERKHA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2])


def p_tevir_phrase_qadma_darga(p):
    "tevir_phrase : QADMA DARGA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3])


def p_tevir_phrase_qadma_merkha(p):
    "tevir_phrase : QADMA MERKHA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3])


def p_tevir_phrase_munax_darga(p):
    "tevir_phrase : MUNAX DARGA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3])


def p_tevir_phrase_munax_merkha(p):
    "tevir_phrase : MUNAX MERKHA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3])


def p_tevir_phrase_telq_qadma_darga(p):
    "tevir_phrase : TELISHAQETANNA QADMA DARGA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3], p[4])


def p_tevir_phrase_telq_qadma_merkha(p):
    "tevir_phrase : TELISHAQETANNA QADMA MERKHA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3], p[4])


def p_tevir_phrase_munax_telq_qadma_darga(p):
    "tevir_phrase : MUNAX TELISHAQETANNA QADMA DARGA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3], p[4], p[5])


def p_tevir_phrase_munax_telq_qadma_merkha(p):
    "tevir_phrase : MUNAX TELISHAQETANNA QADMA MERKHA TEVIR"
    p[0] = add_leaves("tevir_phrase", p[1], p[2], p[3], p[4], p[5])


def p_tevir_clause(p):
    """tevir_clause : tevir_phrase
    | legarmeh_tevir_clause
    | geresh_tevir_clause
    | big_telisha_tevir_clause
    | pazer_tevir_clause"""
    p[0] = p[1]


def p_legarmeh_tevir_clause(p):
    """legarmeh_tevir_clause : legarmeh_phrase tevir_phrase
    | legarmeh_phrase legarmeh_tevir_clause"""
    p[0] = make_node("tevir_clause", p[1], p[2])


# Yeivin says the order is big telisha, then geresh, then pashta, but that is not
# right.  Big telisha often follows geresh, but normally by itself, or with just
# one servus (Gen 13:1).  See also geresh_pashta_clause above.
def p_geresh_tevir_clause(p):
    """geresh_tevir_clause : geresh_clause tevir_phrase
    | geresh_clause legarmeh_tevir_clause
    | geresh_clause geresh_tevir_clause
    | geresh_clause big_telisha_tevir_clause"""
    p[0] = make_node("tevir_clause", p[1], p[2])


def p_big_telisha_tevir_clause(p):
    """big_telisha_tevir_clause : big_telisha_clause tevir_phrase
    | big_telisha_clause legarmeh_tevir_clause
    | big_telisha_clause geresh_tevir_clause
    | big_telisha_clause big_telisha_tevir_clause"""
    p[0] = make_node("tevir_clause", p[1], p[2])


def p_pazer_tevir_clause(p):
    """pazer_tevir_clause : pazer_clause tevir_phrase
    | pazer_clause legarmeh_tevir_clause
    | pazer_clause geresh_tevir_clause
    | pazer_clause big_telisha_tevir_clause
    | pazer_clause pazer_tevir_clause"""
    p[0] = make_node("tevir_clause", p[1], p[2])


# --- zarqa ---------------------------------------------------------------------
# Before segolta (with only one exception - Isa 45:1).  Zarqa is probably a
# specially converted pashta, used before segolta.
def p_zarqa_phrase_zarqa(p):
    "zarqa_phrase : ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1])


def p_zarqa_phrase_munax(p):
    "zarqa_phrase : MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2])


def p_zarqa_phrase_merkha(p):
    "zarqa_phrase : MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2])


# The leading merkha here is rare.
def p_zarqa_phrase_merkha_munax(p):
    "zarqa_phrase : MERKHA MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_merkha_merkha(p):
    "zarqa_phrase : MERKHA MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_munax_munax(p):
    "zarqa_phrase : MUNAX MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_munax_merkha(p):
    "zarqa_phrase : MUNAX MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_qadma_munax(p):
    "zarqa_phrase : QADMA MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_qadma_merkha(p):
    "zarqa_phrase : QADMA MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3])


def p_zarqa_phrase_telq_qadma_munax(p):
    "zarqa_phrase : TELISHAQETANNA QADMA MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3], p[4])


def p_zarqa_phrase_telq_qadma_merkha(p):
    "zarqa_phrase : TELISHAQETANNA QADMA MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3], p[4])


def p_zarqa_phrase_munax_telq_qadma_munax(p):
    "zarqa_phrase : MUNAX TELISHAQETANNA QADMA MUNAX ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3], p[4], p[5])


def p_zarqa_phrase_munax_telq_qadma_merkha(p):
    "zarqa_phrase : MUNAX TELISHAQETANNA QADMA MERKHA ZARQA"
    p[0] = add_leaves("zarqa_phrase", p[1], p[2], p[3], p[4], p[5])


def p_zarqa_clause(p):
    """zarqa_clause : zarqa_phrase
    | legarmeh_zarqa_clause
    | geresh_zarqa_clause
    | big_telisha_zarqa_clause
    | pazer_zarqa_clause"""
    p[0] = p[1]


# Not actually attested, but theoretically possible.
def p_legarmeh_zarqa_clause(p):
    """legarmeh_zarqa_clause : legarmeh_phrase zarqa_phrase
    | legarmeh_phrase legarmeh_zarqa_clause"""
    p[0] = make_node("zarqa_clause", p[1], p[2])


# Yeivin says the order is big telisha, then geresh, then zarqa, but that is not
# right.  Big telisha once follows geresh before zarqa (Neh 3:15).  This works
# basically like geresh_pashta_clause (on which, see above).
def p_geresh_zarqa_clause(p):
    """geresh_zarqa_clause : geresh_clause zarqa_phrase
    | geresh_clause legarmeh_zarqa_clause
    | geresh_clause big_telisha_zarqa_clause
    | geresh_clause geresh_zarqa_clause"""
    p[0] = make_node("zarqa_clause", p[1], p[2])


def p_big_telisha_zarqa_clause(p):
    """big_telisha_zarqa_clause : big_telisha_clause zarqa_phrase
    | big_telisha_clause legarmeh_zarqa_clause
    | big_telisha_clause geresh_zarqa_clause
    | big_telisha_clause big_telisha_zarqa_clause"""
    p[0] = make_node("zarqa_clause", p[1], p[2])


def p_pazer_zarqa_clause(p):
    """pazer_zarqa_clause : pazer_clause zarqa_phrase
    | pazer_clause legarmeh_zarqa_clause
    | pazer_clause geresh_zarqa_clause
    | pazer_clause big_telisha_zarqa_clause
    | pazer_clause pazer_zarqa_clause"""
    p[0] = make_node("zarqa_clause", p[1], p[2])


# --- pashta --------------------------------------------------------------------
# Problem: the Michigan-Claremont texts occasionally mistake mahapakh before pashta
# for yetiv; since pashta can be repeated, this comes out as a legal combination.
# See Jer 34:3, 37:7, 50:11; Job 3:16.
def p_pashta_phrase_yetiv(p):
    "pashta_phrase : YETIV"
    p[0] = add_leaves("pashta_phrase", p[1])


def p_pashta_phrase_pashta(p):
    "pashta_phrase : PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1])


def p_pashta_phrase_mahapakh(p):
    "pashta_phrase : MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2])


def p_pashta_phrase_merkha(p):
    "pashta_phrase : MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2])


def p_pashta_phrase_munax_mahapakh(p):
    "pashta_phrase : MUNAX MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_munax_merkha(p):
    "pashta_phrase : MUNAX MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_qadma_mahapakh(p):
    "pashta_phrase : QADMA MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_qadma_merkha(p):
    "pashta_phrase : QADMA MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_mahapakh_mahapakh(p):
    # Correction (Judg 15:13): the C action was add_leaves(2, ..., $1, $2), an
    # off-by-one that dropped the trailing PASHTA leaf -- the very disjunctive the
    # phrase is built around.  Every sibling servus+pashta rule keeps all leaves;
    # we now do too (diverging from the C oracle, like MISSING_SOFPASUQ).
    "pashta_phrase : MAHAPAKH MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_mahapakh_merkha(p):
    # Correction (1Sam 30:9; Exod 10:13): the C action dropped the trailing PASHTA
    # leaf (same off-by-one as MAHAPAKH MAHAPAKH PASHTA); we keep it.
    "pashta_phrase : MAHAPAKH MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_telq_qadma_mahapakh(p):
    "pashta_phrase : TELISHAQETANNA QADMA MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4])


def p_pashta_phrase_telq_qadma_merkha(p):
    "pashta_phrase : TELISHAQETANNA QADMA MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4])


def p_pashta_phrase_telq_mahapakhqadma(p):
    # Ezekiel 20:31: mahapakh and qadma fused on one letter (see the scanner's
    # MAHAPAKHQADMA rule).  The fused cluster fills the single servus slot before
    # pashta -- the same slot the QADMA MAHAPAKH *pair* fills on separate letters --
    # so this is the one-token analogue of TELISHAQETANNA QADMA MAHAPAKH PASHTA.  Only
    # this exact context is attested; the MUNAX-prefixed siblings of the QADMA MAHAPAKH
    # family are deliberately not mirrored until a real occurrence calls for one.
    "pashta_phrase : TELISHAQETANNA MAHAPAKHQADMA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


def p_pashta_phrase_m_telq_qadma_mahapakh(p):
    "pashta_phrase : MUNAX TELISHAQETANNA QADMA MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5])


def p_pashta_phrase_m_telq_qadma_merkha(p):
    "pashta_phrase : MUNAX TELISHAQETANNA QADMA MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5])


def p_pashta_phrase_m2_telq_qadma_mahapakh(p):
    "pashta_phrase : MUNAX MUNAX TELISHAQETANNA QADMA MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


def p_pashta_phrase_m2_telq_qadma_merkha(p):
    "pashta_phrase : MUNAX MUNAX TELISHAQETANNA QADMA MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


def p_pashta_phrase_m3_telq_qadma_mahapakh(p):
    "pashta_phrase : MUNAX MUNAX MUNAX TELISHAQETANNA QADMA MAHAPAKH PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_pashta_phrase_m3_telq_qadma_merkha(p):
    "pashta_phrase : MUNAX MUNAX MUNAX TELISHAQETANNA QADMA MERKHA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3], p[4], p[5], p[6], p[7])


# Yeivin's scheme is, by and large, good, but it misses a number of cases where
# telisha qetanna precedes pashta with no intervening accents.
def p_pashta_phrase_telq(p):
    "pashta_phrase : TELISHAQETANNA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2])


def p_pashta_phrase_munax_telq(p):
    "pashta_phrase : MUNAX TELISHAQETANNA PASHTA"
    p[0] = add_leaves("pashta_phrase", p[1], p[2], p[3])


# Problem: if qadma is mistaken for pashta, Accents will not pick up the problem
# when a geresh comes next and then eventually a revia and a zaqef; rather, it
# parses the qadma as a well-formed pashta clause/phrase.  See, e.g., Ezek 38:4.
def p_pashta_clause(p):
    """pashta_clause : pashta_phrase
    | legarmeh_pashta_clause
    | geresh_pashta_clause
    | big_telisha_pashta_clause
    | pazer_pashta_clause"""
    p[0] = p[1]


def p_legarmeh_pashta_clause(p):
    """legarmeh_pashta_clause : legarmeh_phrase pashta_phrase
    | legarmeh_phrase legarmeh_pashta_clause"""
    p[0] = make_node("pashta_clause", p[1], p[2])


# Yeivin says the order is big telisha, then geresh, then pashta, but that is not
# right.  Big telisha often follows geresh, but normally by itself, or with just
# one servus.
def p_geresh_pashta_clause(p):
    """geresh_pashta_clause : geresh_clause pashta_phrase
    | geresh_clause legarmeh_pashta_clause
    | geresh_clause big_telisha_pashta_clause
    | geresh_clause geresh_pashta_clause"""
    p[0] = make_node("pashta_clause", p[1], p[2])


def p_big_telisha_pashta_clause(p):
    """big_telisha_pashta_clause : big_telisha_clause pashta_phrase
    | big_telisha_clause legarmeh_pashta_clause
    | big_telisha_clause geresh_pashta_clause
    | big_telisha_clause big_telisha_pashta_clause"""
    p[0] = make_node("pashta_clause", p[1], p[2])


def p_pazer_pashta_clause(p):
    """pazer_pashta_clause : pazer_clause pashta_phrase
    | pazer_clause legarmeh_pashta_clause
    | pazer_clause geresh_pashta_clause
    | pazer_clause big_telisha_pashta_clause
    | pazer_clause pazer_pashta_clause"""
    p[0] = make_node("pashta_clause", p[1], p[2])


# --- revia ---------------------------------------------------------------------
def p_revia_phrase_revia(p):
    "revia_phrase : REVIA"
    p[0] = add_leaves("revia_phrase", p[1])


def p_revia_phrase_munax(p):
    "revia_phrase : MUNAX REVIA"
    p[0] = add_leaves("revia_phrase", p[1], p[2])


def p_revia_phrase_darga_munax(p):
    "revia_phrase : DARGA MUNAX REVIA"
    p[0] = add_leaves("revia_phrase", p[1], p[2], p[3])


# Yeivin says this combo only occurs in Isa 45:1, but in fact it occurs in two
# other passages as well.
def p_revia_phrase_munax_munax(p):
    "revia_phrase : MUNAX MUNAX REVIA"
    p[0] = add_leaves("revia_phrase", p[1], p[2], p[3])


def p_revia_phrase_munax_darga_munax(p):
    "revia_phrase : MUNAX DARGA MUNAX REVIA"
    p[0] = add_leaves("revia_phrase", p[1], p[2], p[3], p[4])


def p_revia_clause(p):
    """revia_clause : revia_phrase
    | legarmeh_revia_clause
    | geresh_revia_clause
    | big_telisha_revia_clause
    | pazer_revia_clause"""
    p[0] = p[1]


def p_legarmeh_revia_clause(p):
    """legarmeh_revia_clause : legarmeh_phrase revia_phrase
    | legarmeh_phrase legarmeh_revia_clause"""
    p[0] = make_node("revia_clause", p[1], p[2])


def p_geresh_revia_clause(p):
    """geresh_revia_clause : geresh_clause revia_phrase
    | geresh_clause legarmeh_revia_clause
    | geresh_clause geresh_revia_clause"""
    p[0] = make_node("revia_clause", p[1], p[2])


def p_big_telisha_revia_clause(p):
    """big_telisha_revia_clause : big_telisha_clause revia_phrase
    | big_telisha_clause legarmeh_revia_clause
    | big_telisha_clause geresh_revia_clause
    | big_telisha_clause big_telisha_revia_clause"""
    p[0] = make_node("revia_clause", p[1], p[2])


def p_pazer_revia_clause(p):
    """pazer_revia_clause : pazer_clause revia_phrase
    | pazer_clause legarmeh_revia_clause
    | pazer_clause geresh_revia_clause
    | pazer_clause big_telisha_revia_clause
    | pazer_clause pazer_revia_clause"""
    p[0] = make_node("revia_clause", p[1], p[2])


# --- geresh --------------------------------------------------------------------
def p_geresh_phrase_gershayim(p):
    "geresh_phrase : GERSHAYIM"
    p[0] = add_leaves("geresh_phrase", p[1])


def p_geresh_phrase_munax_gershayim(p):
    "geresh_phrase : MUNAX GERSHAYIM"
    p[0] = add_leaves("geresh_phrase", p[1], p[2])


def p_geresh_phrase_geresh(p):
    "geresh_phrase : GERESH"
    p[0] = add_leaves("geresh_phrase", p[1])


def p_geresh_phrase_munax_geresh(p):
    "geresh_phrase : MUNAX GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2])


# See the pashta clauses above for how mistaking an azla for a pashta might not
# result in a bad parse, as, e.g., in Ezek 38:4.
def p_geresh_phrase_azla_geresh(p):
    "geresh_phrase : AZLA GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2])


def p_geresh_phrase_telq_azla(p):
    "geresh_phrase : TELISHAQETANNA AZLA GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2], p[3])


def p_geresh_phrase_munax_telq_azla(p):
    "geresh_phrase : MUNAX TELISHAQETANNA AZLA GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2], p[3], p[4])


def p_geresh_phrase_munax2_telq_azla(p):
    "geresh_phrase : MUNAX MUNAX TELISHAQETANNA AZLA GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2], p[3], p[4], p[5])


# Judg 11:17 & about 6 other passages have this many munaxs.
def p_geresh_phrase_munax3_telq_azla(p):
    "geresh_phrase : MUNAX MUNAX MUNAX TELISHAQETANNA AZLA GERESH"
    p[0] = add_leaves("geresh_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


def p_geresh_clause(p):
    """geresh_clause : geresh_phrase
    | legarmeh_geresh_clause"""
    p[0] = p[1]


def p_legarmeh_geresh_clause(p):
    """legarmeh_geresh_clause : legarmeh_phrase geresh_phrase
    | legarmeh_phrase legarmeh_geresh_clause"""
    p[0] = make_node("geresh_clause", p[1], p[2])


# --- big_telisha ---------------------------------------------------------------
def p_big_telisha_phrase_telg(p):
    "big_telisha_phrase : TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1])


def p_big_telisha_phrase_munax(p):
    "big_telisha_phrase : MUNAX TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1], p[2])


def p_big_telisha_phrase_munax2(p):
    "big_telisha_phrase : MUNAX MUNAX TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1], p[2], p[3])


def p_big_telisha_phrase_munax3(p):
    "big_telisha_phrase : MUNAX MUNAX MUNAX TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1], p[2], p[3], p[4])


def p_big_telisha_phrase_munax4(p):
    "big_telisha_phrase : MUNAX MUNAX MUNAX MUNAX TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1], p[2], p[3], p[4], p[5])


def p_big_telisha_phrase_munax5(p):
    "big_telisha_phrase : MUNAX MUNAX MUNAX MUNAX MUNAX TELISHAGEDOLA"
    p[0] = add_leaves("big_telisha_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


def p_big_telisha_clause(p):
    """big_telisha_clause : big_telisha_phrase
    | legarmeh_big_telisha_clause"""
    p[0] = p[1]


# Not attested, but theoretically possible.
def p_legarmeh_big_telisha_clause(p):
    """legarmeh_big_telisha_clause : legarmeh_phrase big_telisha_phrase
    | legarmeh_phrase legarmeh_big_telisha_clause"""
    p[0] = make_node("big_telisha_clause", p[1], p[2])


# --- pazer ---------------------------------------------------------------------
def p_pazer_phrase_pazer(p):
    "pazer_phrase : PAZER"
    p[0] = add_leaves("pazer_phrase", p[1])


def p_pazer_phrase_munax(p):
    "pazer_phrase : MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2])


def p_pazer_phrase_munax2(p):
    "pazer_phrase : MUNAX MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3])


def p_pazer_phrase_munax3(p):
    "pazer_phrase : MUNAX MUNAX MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4])


def p_pazer_phrase_munax4(p):
    "pazer_phrase : MUNAX MUNAX MUNAX MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5])


def p_pazer_phrase_munax5(p):
    "pazer_phrase : MUNAX MUNAX MUNAX MUNAX MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


def p_pazer_phrase_munax6(p):
    "pazer_phrase : MUNAX MUNAX MUNAX MUNAX MUNAX MUNAX PAZER"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_pazer_phrase_galgal(p):
    "pazer_phrase : MUNAX GALGAL PAZERGADOL"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3])


def p_pazer_phrase_munax_galgal2(p):
    "pazer_phrase : MUNAX MUNAX GALGAL PAZERGADOL"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4])


def p_pazer_phrase_munax3_galgal(p):
    "pazer_phrase : MUNAX MUNAX MUNAX GALGAL PAZERGADOL"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5])


def p_pazer_phrase_munax4_galgal(p):
    "pazer_phrase : MUNAX MUNAX MUNAX MUNAX GALGAL PAZERGADOL"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5], p[6])


# Not in Yeivin - Ezek 48:21, Ezra 6:9.
def p_pazer_phrase_munax5_galgal(p):
    "pazer_phrase : MUNAX MUNAX MUNAX MUNAX MUNAX GALGAL PAZERGADOL"
    p[0] = add_leaves("pazer_phrase", p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_pazer_clause(p):
    """pazer_clause : pazer_phrase
    | legarmeh_pazer_clause"""
    p[0] = p[1]


def p_legarmeh_pazer_clause(p):
    """legarmeh_pazer_clause : legarmeh_phrase pazer_phrase
    | legarmeh_phrase legarmeh_pazer_clause"""
    p[0] = make_node("pazer_clause", p[1], p[2])


# --- legarmeh ------------------------------------------------------------------
def p_legarmeh_phrase_legarmeh(p):
    "legarmeh_phrase : LEGARMEH"
    p[0] = add_leaves("legarmeh_phrase", p[1])


def p_legarmeh_phrase_merkha(p):
    "legarmeh_phrase : MERKHA LEGARMEH"
    p[0] = add_leaves("legarmeh_phrase", p[1], p[2])


def p_legarmeh_phrase_qadma_merkha(p):
    "legarmeh_phrase : QADMA MERKHA LEGARMEH"
    p[0] = add_leaves("legarmeh_phrase", p[1], p[2], p[3])


def p_legarmeh_phrase_munax_merkha(p):
    "legarmeh_phrase : MUNAX MERKHA LEGARMEH"
    p[0] = add_leaves("legarmeh_phrase", p[1], p[2], p[3])


def p_legarmeh_phrase_munax_munax(p):
    "legarmeh_phrase : MUNAX MUNAX LEGARMEH"
    p[0] = add_leaves("legarmeh_phrase", p[1], p[2], p[3])


# --- error recovery productions (Phase E) --------------------------------------
# Faithful translation of every `error`-token production in acc2tre.y.  Each
# phrase/clause-level rule builds the same ERROR-leaf / ERROR-clause tree the C
# recovery action builds, and calls p.parser.errok() to mirror yacc's `yyerrok`
# (resume normal error reporting immediately, so a second error in the same verse
# can also be recovered).  These rules fire only on a genuine syntax error, so
# clean verses reduce via the normal rules unchanged; on the 51 ungrammatical they
# reproduce the C binary's ERROR-node trees byte-for-byte.
#
# The two pasuq-level rules build no tree (the C actions print the location and
# call free_nodes without print_tree); they return LOCATION_ONLY so the driver
# emits the reference line only.  They do not fire on the parity corpus.

# Sentinel for a verse whose only output is its reference line (no tree).
LOCATION_ONLY = object()


def p_pasuq_error(p):
    # acc2tre.y has a third alternative here, the bare `pasuq : error`, and it is
    # deliberately NOT ported -- the module docstring lists this with MISSING_SOFPASUQ
    # and the two add_leaves off-by-ones as a divergence from the C oracle (#221).
    #
    # In PLY it does not reject a bad stream, it hangs on one.  With pasuq on the stack
    # (state 1) and a live lookahead, PLY pops pasuq, shifts an error symbol in state 0,
    # and reduces this alternative WITHOUT consuming a token, which puts pasuq back in
    # state 1 with the same lookahead waiting: the state that just errored.  So any
    # stream with a token left over once pasuq has reduced never terminates, and four
    # tokens are enough -- TILDE SILLUQ SOFPASUQ REVIA, whose first three reduce by the
    # ordinary p_pasuq rule.  Measured 2026-08-07 over every token stream of length 1-3
    # and every TILDE-prefixed stream of length 4, 79,798 in all: with the bare
    # alternative in place 7,253 of them never terminate.
    #
    # Dropping it costs no reachable behavior.  PLY returns (yacc.py:1242) before ever
    # making an error symbol out of an end-of-input lookahead, so a real token is always
    # waiting when this reduction finishes, and a real token in state 1 is the cycle.
    # Over those same 79,798 streams the bare alternative fired on 0 parses that
    # returned, and the grammar with it and the grammar without it return the same thing
    # on every stream that terminates at all.
    """pasuq : TILDE error UNKNOWN_ACCENT SOFPASUQ
    | TILDE silluq_clause error"""
    p[0] = LOCATION_ONLY


def p_silluq_phrase_error(p):
    # e.g. Gen 32:24, missing silluq.
    """silluq_phrase : error
    | error SILLUQ"""
    p.parser.errok()
    p[0] = add_leaves("silluq_phrase", "ERROR")


def p_atnax_phrase_error(p):
    "atnax_phrase : error ATNAX"
    p.parser.errok()
    p[0] = add_leaves("atnax_phrase", "ERROR")


def p_zaqef_atnax_clause_error(p):
    # Missing atnax in Exod 4:10 (Leningrad MS).
    "zaqef_atnax_clause : zaqef_clause tevir_clause MERKHA ATNAX error"
    p.parser.errok()
    p[0] = make_node("atnax_clause", p[1], add_leaves("atnax_phrase", "ERROR"))


def p_zaqef_phrase_error(p):
    "zaqef_phrase : error ZAQEF"
    p.parser.errok()
    p[0] = add_leaves("zaqef_phrase", "ERROR")


def p_segolta_phrase_error(p):
    "segolta_phrase : error SEGOLTA"
    p.parser.errok()
    p[0] = add_leaves("segolta_phrase", "ERROR")


def p_zarqa_segolta_clause_error(p):
    # Isa 45:1 (MUNAX MUNAX error); a BHS error at 2Chr 7:5 (MUNAX error REVIA).
    """zarqa_segolta_clause : zarqa_clause MUNAX MUNAX error
    | zarqa_clause MUNAX error REVIA"""
    p.parser.errok()
    p[0] = make_node("segolta_clause", p[1], add_leaves("segolta_phrase", "ERROR"))


def p_tipexa_phrase_error(p):
    """tipexa_phrase : error TIPEXA
    | geresh_clause error TIPEXA"""
    p.parser.errok()
    p[0] = add_leaves("tipexa_phrase", "ERROR")


def p_tevir_tipexa_clause_error(p):
    # Extension beyond acc2tre.y (cf. p_pasuq_missing_sofpasuq): recover a
    # tevir_clause whose required following tipexa is absent -- e.g. Obadiah 1:1,
    # "... ZAQEF TEVIR MERKHA SILLUQ", a tevir illegally before silluq.  Without
    # this, PLY's recovery stalls in the tevir_clause context (its only error
    # production, tipexa_phrase : error TIPEXA, needs a TIPEXA that never comes)
    # and the verse yields no output -- a troublemaker.  Completing the
    # tipexa_clause with an ERROR leaf lets tipexa_silluq_clause consume the
    # trailing silluq, so the verse becomes an ERROR-tree ungrammatical instead.
    "tevir_tipexa_clause : tevir_clause error"
    p.parser.errok()
    p[0] = make_node("tipexa_clause", p[1], add_leaves("tipexa_phrase", "ERROR"))


def p_tipexa_silluq_clause_error(p):
    # Extension beyond acc2tre.y (cf. p_tevir_tipexa_clause_error above): recover a
    # verse-final tevir_clause with no silluq at all before the sof pasuq -- e.g.
    # Judges 13:18, "... ATNAX TEVIR SOFPASUQ", where the silluq is transcribed as
    # a tevir (a speck in the manuscript).  Same RHS as the tevir_tipexa_clause
    # error rule but reduced on the end-of-verse SOFPASUQ lookahead (disjoint from
    # that rule's silluq-starter lookaheads, so no conflict): close the verse with
    # the absent silluq flagged ERROR, keeping the stray tevir.  Without this the
    # verse yields no output -- a troublemaker.
    "tipexa_silluq_clause : tevir_clause error"
    p.parser.errok()
    p[0] = make_node("silluq_clause", p[1], add_leaves("silluq_phrase", "ERROR"))


def p_revia_phrase_error(p):
    "revia_phrase : error REVIA"
    p.parser.errok()
    p[0] = add_leaves("revia_phrase", "ERROR")


def p_pashta_phrase_error(p):
    """pashta_phrase : error PASHTA
    | error YETIV"""
    p.parser.errok()
    p[0] = add_leaves("pashta_phrase", "ERROR")


def p_tevir_phrase_error(p):
    "tevir_phrase : error TEVIR"
    p.parser.errok()
    p[0] = add_leaves("tevir_phrase", "ERROR")


def p_zarqa_phrase_error(p):
    "zarqa_phrase : error ZARQA"
    p.parser.errok()
    p[0] = add_leaves("zarqa_phrase", "ERROR")


def p_geresh_phrase_error(p):
    "geresh_phrase : error GERESH"
    p.parser.errok()
    p[0] = add_leaves("geresh_phrase", "ERROR")


def p_big_telisha_phrase_error(p):
    "big_telisha_phrase : error TELISHAGEDOLA"
    p.parser.errok()
    p[0] = add_leaves("big_telisha_phrase", "ERROR")


def p_pazer_phrase_error(p):
    "pazer_phrase : error PAZER"
    p.parser.errok()
    p[0] = add_leaves("pazer_phrase", "ERROR")


def p_legarmeh_phrase_error(p):
    "legarmeh_phrase : error LEGARMEH"
    p.parser.errok()
    p[0] = add_leaves("legarmeh_phrase", "ERROR")


# --- error callback ------------------------------------------------------------
def p_error(p):  # noqa: D401  (PLY callback)
    # On a syntax error, do nothing here and let PLY perform automatic
    # error-token recovery via the productions above (yacc's recovery, which
    # builds the ERROR-leaf trees).  Manual recovery (parser.errok here) would
    # tell PLY the user already recovered and skip the error productions.
    pass


class _LexToken:
    """Minimal PLY-compatible token object."""

    __slots__ = ("type", "value", "lineno", "lexpos", "lexer")

    def __init__(self, ttype: str, value: str):
        self.type = ttype
        self.value = value
        self.lineno = 0
        self.lexpos = 0
        self.lexer = None


class _TokenStream:
    """Adapts a list[Token] to PLY's lexer interface (input/token)."""

    def __init__(self, toks: list[Token]):
        self._it = iter(toks)

    def input(self, _s):  # PLY may call this; we ignore it.
        pass

    def token(self):
        try:
            t = next(self._it)
        except StopIteration:
            return None
        return _LexToken(t.type, t.leaf)


def build_parser():
    """Build the PLY parser (no table files, warnings silenced)."""
    return yacc.yacc(
        module=sys.modules[__name__],
        write_tables=False,
        debug=False,
        errorlog=yacc.NullLogger(),
    )


def parse_tokens(parser, toks: list[Token]):
    """Parse one verse's token stream.

    Returns the tree (TN) for a normal or error-recovered verse, the
    LOCATION_ONLY sentinel for a pasuq-level error verse (reference line only),
    or None if the parse fails with no recovery possible.
    """
    return parser.parse(lexer=_TokenStream(toks))
