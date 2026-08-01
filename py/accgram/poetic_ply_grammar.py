"""PLY yacc grammar for the POETIC (Three Books) accent system.

This is the poetic counterpart of accgram.prose_ply_grammar (which ports acc2tre.y, the
prose / Twenty-One Books grammar).  There is no Goerwitz C oracle for the poetic
books; the productions here are derived from Yeivin, *Introduction to the Tiberian
Masorah* (ITM), the section "The Accents of the Three Books" (Psalms, Proverbs,
and the poetic core of Job), paragraphs 358-374.  Section numbers are cited
inline.  See also mb_cmn.hebrew_accents, whose poetic conjunctive list cites ITM
#358 / #361.

Breuer, *Ta'amei ha-Miqra*, Ch 10 (English trans. "Cantillation of Scripture,
Ch 10", the systematic theory of the Eme"t hierarchy: Emperor siluk -> Kings
[oleh-we-yored, atnax, revia'] -> additional mafsiqim [revia mugrash, big
shalshelet, mahapakh legarmeih] -> Viceroys [big revia, tsinnor, small revia, dexi]
-> military secretaries [pazer, legarmeih]) is the parallel systematic source, and
confirms this same skeleton term-for-term: dexi as the final viceroy of
atnax/revia only (never under oleh-we-yored); tsinnor and small revia only
under oleh-we-yored; and revia mugrash / big shalshelet as additional mafsiqim that
"can only divide the left side of [atnax]" (the silluq-near second part) -- which
is exactly why a revia mugrash in atnax's own realm (Job 31:15, L-only) is rejected.
Ch 10 §9 on the doubled tsinnor is cited at collapse_repeated_tsinnor below.

Design: rank-ordered clause hierarchy, permissive servus chains.
  The *clause* rules encode Yeivin's disjunctive hierarchy by RANK: a domain headed
  by disjunctive D admits, as its near subdividers, the disjunctives of any lower
  rank -- not merely the one rank immediately below.  (Phase 3 relaxed an earlier
  "immediate-sub only" form: L freely uses a lower divider directly when a unit is
  too short for the intermediate one -- legarmeh straight under atnax, dexi or
  legarmeh straight before silluq -- exactly as the prose grammar's silluq/atnax
  domains admit their lower dividers.  Every such case here is MAM-confirmed.)  The
  *phrase* rules, by contrast, accept any run of conjunctive servi before a
  disjunctive, because Yeivin describes the poetic servi only loosely -- "up to N
  servi", "various combinations", "governed by intricate rules" -- and there is no
  oracle to pin exact patterns against.  So every ``D_phrase`` is just ``D``
  optionally preceded by a ``servi`` chain; the particular servus counts/orders
  Yeivin documents (munax/merkha before silluq, galgal+mahapakh/azla before pazer, the
  galgal "v"-servus of oleh-we-yored, etc.) are admitted but not required.

  Error recovery is limited to one rule (p_silluq_phrase_error): a verse missing
  its silluq entirely (category A) recovers into an ERROR-leaf silluq_phrase,
  mirroring the prose grammar.  p_error gates this to the verse-final-SOFPASUQ case
  so genuine mid-verse anomalies still surface as NO_PARSE (parse_tokens -> None).

Hierarchy of disjunctives (each lists its CANONICAL near subdivider(s); per the
rank-ordered design above, a domain also admits any lower-ranked divider directly
when a unit is too short for the intermediate one):

  silluq (verse end, #359)
    great division: oleh-we-yored (distant) OR atnax (close)             (#361)
    near division before silluq: revia mugrash / shalshelet gedolah  (#366, #371);
      also dexi / pazer / legarmeh directly when the final unit is short
  oleh-we-yored (the main verse divider, #363)
    main subdivider: revia gadol; immediately preceded by revia qatan
    (no servus) or tsinnor (with servus)                          (#363, #365, #368)
  atnax (#362)               -> dexi (near) / revia gadol (distant)  (#362, #364);
                                also pazer / legarmeh directly
  revia gadol (#363)         -> pazer / legarmeh; also dexi / tsinnor directly
  revia qatan (#368)         -> legarmeh; also tsinnor (TSINNOR REVIA_QATAN OLEH)
  revia mugrash (#366-367)   -> pazer / legarmeh (with geresh, tipexa-like);
                                also dexi / revia gadol when "without geresh" it
                                acts as the main verse divider like atnax (#367)
  dexi (#364)                -> pazer / legarmeh
  tsinnor (#365)              -> pazer / legarmeh
  pazer (#369)               -> legarmeh only
  legarmeh (#370)            -> (terminal lowest disjunctive)

Token disambiguation that the scanner (accgram.poetic_scanner) performs and
this grammar relies on: the three revias share signs but are distinct tokens here
(REVIA_GADOL / REVIA_QATAN / REVIA_MUGRASH); the scanner separates them by the
geresh muqdam (mugrash) and by position (qatan only before oleh-we-yored, a bare
revia before silluq = mugrash without geresh, #391).

Grammar actions build trees with tree.make_node / add_leaves, as the prose
grammar does, so accgram.tree.print_tree renders poetic trees identically.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from ply import yacc

from accgram import poetic_accent_names as pan
from accgram.tree import add_leaves, make_node

# Token-type names come from poetic_accent_names (the single source of truth).  The
# terminals are still spelled literally in the p_* rule docstrings below because
# PLY parses those textually; this tuple keeps them pinned to the constants, and
# the parse / zero-conflict tests fail if a docstring terminal ever drifts.
#
tokens = (
    # structure
    pan.TILDE,
    pan.SOFPASUQ,
    # disjunctives (greatest -> least)
    pan.SILLUQ,
    pan.OLEH_WEYORED,
    pan.ATNAX,
    pan.REVIA_GADOL,
    pan.REVIA_MUGRASH,
    pan.REVIA_QATAN,
    pan.DEXI,
    pan.TSINNOR,
    pan.PAZER,
    pan.LEGARMEH,
    pan.SHALSHELET_GEDOLAH,
    # conjunctive servi (ITM #358; GALGAL also serves oleh-we-yored, #363)
    pan.MUNAX,
    pan.MERKHA,
    pan.MAHAPAKH,
    pan.AZLA,
    pan.GALGAL,
    pan.ILLUY,
    pan.TARXA,
    # fused-tsinnorit servi (Plan C): a mahapakh/merkha carrying a secondary tsinnorit;
    # and the conjunctive shalshelet qetannah (#371), a real servus the scanner now
    # emits (eight verses) instead of swallowing.  All three join the `conj` chain, so
    # they are absorbed exactly like the seven primary servi -- no skeleton change.
    pan.MAHAPAKH_METSUNNAR,
    pan.MERKHA_METSUNNAR,
    pan.SHALSHELET_QETANNAH,
)
# NB: a same-letter bang (e.g. pan.MERKHA_AZLA, Plan D) is deliberately NOT a grammar
# token.  The scanner still *emits* it (faithful representation), but a same-letter accent
# pair outside the whitelist (revia+geresh muqdam, ole+yored, dexi+munax) is a lexical
# anomaly, not a licit servus: with no terminal for it the parser dead-ends -> NO_PARSE
# (the poetic-native lexical-error surface, as STRAY_ACCENT), so ps56:10 surfaces as a
# flagged ungrammatical rather than a silently-clean parse.  See poetic_ob_notes["ps 56:10"].

start = "pasuq"


# --- conjunctive servi (permissive chain, see module docstring) ----------------
def p_conj(p):
    """conj : MUNAX
    | MERKHA
    | MAHAPAKH
    | AZLA
    | GALGAL
    | ILLUY
    | TARXA
    | MAHAPAKH_METSUNNAR
    | MERKHA_METSUNNAR
    | SHALSHELET_QETANNAH"""
    p[0] = p[1]  # the leaf-name string


# #46 -- chain STRUCTURE (servus count + order) stays permissive BY DESIGN.
# Issue #18 closed servant ADJACENCY (which one conjunctive sits immediately before
# each disjunctive); the slice it left open was the CHAIN itself: how many servi, in
# what order, may stack before a disjunctive.  Richter's poetic-conjunctive prose
# (#24; syntax.htm, "Conjunctive Marks In The 3 Books" -- note he gives the poetic
# servi as PROSE, not the per-rank charts the issue title hoped for; only the
# distinctive marks are charted) is the natural oracle: he names TARXA, AZLA (=qadma)
# and MAHAPAKH as the conjunctives that "precede other conjunctive marks", his only
# chain examples being the 2-servus MAHAPAKH-MUNAX before DEXI and TARXA-MUNAX before
# SILLUQ.  Read strictly that is a chartable restriction: a NON-FINAL chain slot (one
# followed by another conjunctive) admits only {TARXA, AZLA, MAHAPAKH (+ the metsunnar
# variant)}, never the generic servi.
#
# REFUTED -- by the #18 disqualifier, and at the first gate (L itself).  The strict
# reading is contradicted in L directly (1028 of 2267 multi-servus chains carry an
# out-of-set non-final servus) and MAM agrees verse-for-verse, so these are genuine
# two-witness constructions, not L quirks.  The bulk is the utterly ordinary
# double-MUNAX before ATNAX (MUNAX non-final 874x in L / 853x in MAM -- e.g. Ps 2:4,
# 2:11, 2:12, 3:8, marked identically on both witnesses), plus MERKHA-MERKHA (102/137)
# and ILLUY-headed chains (42/39).  Richter himself hedges ("among those marks"; "not
# very frequent"; the 3-books rules are "fuzzier ... cover a smaller portion"), so his
# list is illustrative, not exhaustive.  Encoding non-final-subset-{TARXA,AZLA,MAHAPAKH}
# would NO_PARSE ~1000 clean verses; the escape hatch is again the generic MUNAX / MERKHA
# family standing where the loose rule did not enumerate it.  So the chain remains
# any-conj-in-any-order, exactly as the module docstring's permissive-chain paragraph says.
#
# Two facts noted for the record but deliberately NOT encoded, by #46's own criterion
# (encode only a restriction that flags REAL divergences):
#   * GALGAL is never a chain-PRECEDER (0 of 236 non-final in L, 0 in MAM) -- always the
#     adjacent servus, matching Richter "Galgal serves Pazer".  A "GALGAL never non-final"
#     guard would flag nothing (inert, like revia_qatan_servi), so it is left out.
#   * Chain LENGTH stays uncapped: Richter charts no maximum and the corpus max is 5
#     (L: len2 2055, len3 198, len4 13, len5 1), so any cap would be arbitrary, not
#     Richter-grounded.  Measured via scratchpad chain_measure.py / chain_measure_mam.py.
def p_servi_one(p):
    "servi : conj"
    p[0] = [p[1]]


def p_servi_many(p):
    "servi : servi conj"
    p[0] = p[1] + [p[2]]


# --- pasuq ---------------------------------------------------------------------
def p_pasuq(p):
    "pasuq : TILDE silluq_clause SOFPASUQ"
    p[0] = p[2]


# --- phrases (disjunctive + optional servus chain) -----------------------------
# One uniform pair of productions per disjunctive: the bare sign, or a servus
# chain followed by the sign.
# Permissive servi before SILLUQ.  NB: Breuer Ch 9 §11 limits the servant of silluq
# (and ATNAX, below) to merkha or MUNAX.  Vetted via servi_xcheck (2026-06-17) and
# REFUTED at the token level: L marks ILLUY before silluq in 43 verses (plus Job 12:15
# TARXA), and MAM agrees in all but the lone one-sided Prov 21:29.  ILLUY is a
# MUNAX-family conjunctive Breuer counts as MUNAX, but the scanner emits it as a
# distinct token -- so a MERKHA|MUNAX-only constraint would flag 43 two-witness-
# confirmed verses.  The single in-set type-conflict (Ps 60:3 MERKHA -> MAM MUNAX) is a
# phonological MUNAX/merkha swap, not a structural divergence.  Not encoded.  See issue #18.
def p_silluq_phrase(p):
    """silluq_phrase : SILLUQ
    | servi SILLUQ"""
    _phrase(p, "silluq_phrase")


def p_silluq_phrase_error(p):
    # Category A: 13 verses lack any silluq code in L (e.g. Ps 37:31,
    # "...):A$URFY/W00" -- the sof pasuq directly follows the last servus, no
    # silluq).  Mirror the prose grammar's missing-silluq recovery
    # (prose_ply_grammar.p_silluq_phrase_error): on the syntax error PLY reduces the
    # absent silluq to a silluq_phrase whose mark is ERROR and errok() resumes
    # normal reporting, so the verse becomes a flagged ungrammatical *tree* (the rest of
    # its structure preserved and visible) instead of a no-output NO_PARSE line.
    # This is the only poetic error-recovery rule: there is no poetic C oracle, so
    # recovery is deliberately limited to this one well-understood shape.
    """silluq_phrase : error
    | error SILLUQ"""
    p.parser.errok()
    p[0] = add_leaves("silluq_phrase", "ERROR")


def p_oleh_weyored_phrase(p):
    """oleh_weyored_phrase : OLEH_WEYORED
    | servi OLEH_WEYORED"""
    # The characteristic servus is the "v"-shaped sign, coded as galgal in L (the
    # same sign as pazer's servus; #363); mahapakh/merkha also occur.  The yored
    # (merkha below the stress) is part of the oleh-we-yored sign and is folded into
    # the OLEH_WEYORED token by the scanner, not a servus.
    _phrase(p, "oleh_weyored_phrase")


# Permissive servi before ATNAX.  NB: Breuer Ch 9 §11 limits the servant of ATNAX
# (and silluq, above) to merkha or MUNAX.  Vetted via servi_xcheck (2026-06-17) and
# REFUTED at the token level: the seven L outliers are MAHAPAKH (Ps 14:3, 53:4, Prov
# 6:3, 24:29) and ILLUY (Prov 1:9, 6:27) -- all MAM-confirmed two-witness constructions
# -- plus the one genuine servant-type conflict Prov 3:4 (L TARXA -> MAM MERKHA), where
# L alone uses an out-of-set tarxa (a sign-choice illegality, not rule material).  A
# MERKHA|MUNAX-only constraint would flag six correct verses, so it is not encoded.  See issue #18.
def p_atnax_phrase(p):
    """atnax_phrase : ATNAX
    | servi ATNAX"""
    _phrase(p, "atnax_phrase")


# Permissive servi before REVIA_GADOL.  Breuer Ch 11 §32-33 gives a phonology-dependent
# 3-set -- mahapakh | merkha | illuy -- and servi_xcheck (2026-06-17) confirms it: L's
# distribution is exactly those three (108 / 65 / 32) with ZERO servant-type conflicts vs
# MAM.  The only out-of-set L servant is AZLA in three verses (Ps 72:17, Job 32:11, 34:33),
# and those are NOT a two-witness azla servant: L has a bare azla (no paseq) where MAM marks
# azla-LEGARMEH (azla + paseq), i.e. a near-divider, not a servant.  The disjunctive cross-
# check already flags all three (MAM has an extra LEGARMEH that L lacks), so a servant-
# set constraint here would be redundant -- and, by requiring the adjacent servant in
# {mahapakh, merkha, illuy}, would turn three clean parses into NO_PARSE for a paseq-omission
# divergence already surfaced elsewhere.  Not encoded.  See issue #18.
def p_revia_gadol_phrase(p):
    """revia_gadol_phrase : REVIA_GADOL
    | servi REVIA_GADOL"""
    _phrase(p, "revia_gadol_phrase")


# Breuer Ch 11 §17: "the servant next to a small revia' is [merkha], and a [mahapakh]
# precedes it."  So the servus immediately adjacent to REVIA_QATAN must be MERKHA;
# any earlier servi (e.g. the preceding mahapakh) are free.  Unlike the refuted
# dexi<-munax rule, this is CONFIRMED by both witnesses via the servi_before oracle
# (mam_poetic_accents): L marks merkha before small revia in 125/125 cases and MAM
# agrees on merkha wherever it too has a servant there, with ZERO servant-type
# conflicts.  NOTE: precisely because both witnesses already agree, this rule does
# NOT currently fire -- it flags 0 verses in the present corpus.  It is encoded as a
# faithful, evidence-backed constraint and a guard against future / other-text
# deviations (e.g. UXLC), not as a live diagnostic.  A bare REVIA_QATAN (no servant)
# stays allowed.
def p_revia_qatan_servi(p):
    """revia_qatan_servi : MERKHA
    | servi MERKHA"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_revia_qatan_phrase(p):
    """revia_qatan_phrase : REVIA_QATAN
    | revia_qatan_servi REVIA_QATAN"""
    _phrase(p, "revia_qatan_phrase")


# Permissive servi before REVIA_MUGRASH.  NB: Breuer Ch 11 §38 says the servant is merkha
# (with a mahapakh before it).  Vetted via servi_xcheck (2026-06-17) and REFUTED at the
# token level: against 1185 merkha, L marks MAHAPAKH in 9 verses (Ps 31:16, 34:8, 68:15,
# 79:3, 116:19, 135:21, Prov 7:7, 27:1, 27:19) and ILLUY in 1 (Ps 137:9), and MAM agrees in
# every one -- genuine two-witness constructions of the same phonological servant-type family
# that refuted DEXI / PAZER / TSINNOR.  A merkha-only constraint would flag 10 correct verses.
# Not encoded.  See issue #18.
# Open, 2026-07-27: §38 states the rule of TWO servants -- "The two servants next to revia'
# mugrash are merkha marks, and a [mahapakh] precedes them" -- so the singular wording above is
# that rule read for a lone servant, which §38's own Examples I bear out.  Left singular;
# whether the plural is worth spelling out here is unresolved.
def p_revia_mugrash_phrase(p):
    """revia_mugrash_phrase : REVIA_MUGRASH
    | servi REVIA_MUGRASH"""
    _phrase(p, "revia_mugrash_phrase")


# Permissive servi before dexi (same shape as the other phrases).  NB: Breuer
# Ch 11 §11 states "the servant next to the [dexi] is ALWAYS a [munax]", which would
# justify forcing the adjacent servus to MUNAX.  That tightening was tried (commit
# fc9c0d7) and REFUTED: a MAM-simple cross-check of the servant sign (not just the
# disjunctive skeleton) shows MAM independently agrees with L on *merkha* before dexi
# in all 16 merkha cases and has munax in NONE of them -- so merkha-served dexi is a
# real, two-witness construction and Breuer's flat "always" is an oversimplification
# (the munax/merkha choice is phonological, hence out of scope for a token grammar).
# Enforcing munax-only would flag 16 correct verses.  See issue #18.
def p_dexi_phrase(p):
    """dexi_phrase : DEXI
    | servi DEXI"""
    _phrase(p, "dexi_phrase")


# Permissive servi before TSINNOR.  NB: Breuer Ch 11 §23 limits the servant to MUNAX or
# MERKHA only.  servi_xcheck found two L outliers; an FOI cross-check (2026-06-17) shows
# neither is a clean primary counter-example, so the rule effectively HOLDS for PRIMARY
# servants -- but it is still not worth encoding:
#   - Ps 31:20 (L MAHAPAKH): MAM's FOI catalog classifies this mahapakh as a METZUNAR
#     (secondary) mark + secondary meteg at the tsinnor slot (foi-sec-misc), and it is
#     CoS-CONTESTED (foi-sec-star-breuer-cos, Breuer 9.31) -- not a settled primary
#     mahapakh; L merely keeps a sign the scanner did not treat as secondary.
#   - Ps 79:6 (L AZLA): one-sided -- MAM has a REVIA_GADOL divider on that word, so the
#     DISJUNCTIVE cross-check already flags the verse (MAM has an extra REVIA_GADOL).
# Encoding MUNAX|MERKHA-only would fire on just these two -- one CoS-contested, one already
# surfaced by the disjunctive xcheck -- while turning two clean L parses into NO_PARSE.  Not
# encoded (confirmed-but-inert/redundant, like revia gadol).  See issue #18.
def p_tsinnor_phrase(p):
    """tsinnor_phrase : TSINNOR
    | servi TSINNOR"""
    _phrase(p, "tsinnor_phrase")


# Permissive servi before pazer.  NB: Breuer Ch 11 §7-9 says the servant before pazer is
# "always galgal" (yerax-ben-yomo), which would justify forcing the adjacent servus to
# GALGAL.  REFUTED by the servant cross-check (servi_xcheck) once it learned to read a
# SAME-WORD servant: galgal often sits on the pazer's own word (e.g. Ps 32:5, 65:10), and
# those "GALGAL vs MAM-qadma" mismatches were a measurement artifact -- they actually
# CONFIRM galgal.  But three verses keep a primary merkha on the word right before pazer in
# BOTH witnesses -- Ps 4:3, 59:6, 71:3 -- and MAM's own FOI catalog does NOT flag those as
# secondary merkha, so merkha-served pazer is a real two-witness construction (the same
# shape as the refuted dexi<-munax rule; the galgal/merkha choice is phonological, hence out
# of a token grammar's scope).  Two further non-galgal cases are not counter-evidence but
# also not galgal: Ps 28:5 is a plain L-vs-MAM sign divergence (L mahapakh, MAM galgal), and
# Ps 89:20's merkha is a CoS-contested secondary merkha (stays non-galgal even if dropped).
# Enforcing galgal-only would flag the three correct merkha verses.  See issue #18.
def p_pazer_phrase(p):
    """pazer_phrase : PAZER
    | servi PAZER"""
    _phrase(p, "pazer_phrase")


def p_legarmeh_phrase(p):
    """legarmeh_phrase : LEGARMEH
    | servi LEGARMEH"""
    _phrase(p, "legarmeh_phrase")


def p_shalshelet_gedolah_phrase(p):
    """shalshelet_gedolah_phrase : SHALSHELET_GEDOLAH
    | servi SHALSHELET_GEDOLAH"""
    _phrase(p, "shalshelet_gedolah_phrase")


def _phrase(p, label):
    """Shared action: build a phrase leaf from optional servi + the disjunctive."""
    if len(p) == 2:  # bare disjunctive
        p[0] = add_leaves(label, p[1])
    else:  # servi (a list) + disjunctive
        p[0] = add_leaves(label, *p[1], p[2])


# --- silluq clause (#359, #361, #366, #371) ------------------------------------
# The silluq domain is the whole verse.  Its great divider is atnax or
# oleh-we-yored; oleh-we-yored, when present, is the topmost divider and may
# contain an atnax-divided remainder before silluq.
#
# Below the great dividers, the near divider before silluq is most often revia
# mugrash or shalshelet gedolah, but L (faithful to it, MAM-confirmed) freely uses
# a *lower* disjunctive directly when the final unit is short: dexi, pazer, or
# legarmeh may stand immediately before silluq with no revia mugrash, exactly as
# the prose silluq domain admits its lower dividers (tipexa -> ... directly).  So
# the silluq domain admits a rank-ordered chain of near dividers --
# revia_mugrash / shalshelet (highest), then dexi, then pazer, then legarmeh --
# each of which may be followed (toward silluq) by any lower one.  This is the
# poetic analogue of the prose tipexa/zaqef_silluq cascade in prose_ply_grammar.py.
def p_silluq_clause(p):
    """silluq_clause : silluq_phrase
    | revia_mugrash_silluq_clause
    | shalshelet_silluq_clause
    | dexi_silluq_clause
    | pazer_silluq_clause
    | legarmeh_silluq_clause
    | atnax_silluq_clause
    | oleh_silluq_clause"""
    p[0] = p[1]


def p_legarmeh_silluq_clause(p):
    """legarmeh_silluq_clause : legarmeh_clause silluq_phrase
    | legarmeh_clause legarmeh_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_pazer_silluq_clause(p):
    """pazer_silluq_clause : pazer_clause silluq_phrase
    | pazer_clause legarmeh_silluq_clause
    | pazer_clause pazer_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_dexi_silluq_clause(p):
    """dexi_silluq_clause : dexi_clause silluq_phrase
    | dexi_clause legarmeh_silluq_clause
    | dexi_clause pazer_silluq_clause
    | dexi_clause dexi_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_revia_mugrash_silluq_clause(p):
    """revia_mugrash_silluq_clause : revia_mugrash_clause silluq_phrase
    | revia_mugrash_clause legarmeh_silluq_clause
    | revia_mugrash_clause pazer_silluq_clause
    | revia_mugrash_clause dexi_silluq_clause
    | revia_mugrash_clause revia_mugrash_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_shalshelet_silluq_clause(p):
    """shalshelet_silluq_clause : shalshelet_gedolah_clause silluq_phrase
    | shalshelet_gedolah_clause legarmeh_silluq_clause
    | shalshelet_gedolah_clause pazer_silluq_clause
    | shalshelet_gedolah_clause dexi_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_atnax_silluq_clause(p):
    """atnax_silluq_clause : atnax_clause silluq_phrase
    | atnax_clause revia_mugrash_silluq_clause
    | atnax_clause shalshelet_silluq_clause
    | atnax_clause dexi_silluq_clause
    | atnax_clause pazer_silluq_clause
    | atnax_clause legarmeh_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


def p_oleh_silluq_clause(p):
    """oleh_silluq_clause : oleh_clause silluq_phrase
    | oleh_clause revia_mugrash_silluq_clause
    | oleh_clause shalshelet_silluq_clause
    | oleh_clause dexi_silluq_clause
    | oleh_clause pazer_silluq_clause
    | oleh_clause legarmeh_silluq_clause
    | oleh_clause atnax_silluq_clause"""
    p[0] = make_node("silluq_clause", p[1], p[2])


# --- oleh-we-yored clause (#363, #365, #368) -----------------------------------
# Immediately preceded by revia qatan (no servus) or tsinnor (with servus); the
# main subdivider of its domain is revia gadol, standing before that.
def p_oleh_clause(p):
    """oleh_clause : oleh_weyored_phrase
    | revia_qatan_oleh_clause
    | tsinnor_oleh_clause
    | revia_gadol_oleh_clause"""
    p[0] = p[1]


def p_revia_qatan_oleh_clause(p):
    "revia_qatan_oleh_clause : revia_qatan_clause oleh_weyored_phrase"
    p[0] = make_node("oleh_weyored_clause", p[1], p[2])


def p_tsinnor_oleh_clause(p):
    "tsinnor_oleh_clause : tsinnor_clause oleh_weyored_phrase"
    p[0] = make_node("oleh_weyored_clause", p[1], p[2])


def p_revia_gadol_oleh_clause(p):
    """revia_gadol_oleh_clause : revia_gadol_clause oleh_weyored_phrase
    | revia_gadol_clause revia_qatan_oleh_clause
    | revia_gadol_clause tsinnor_oleh_clause
    | revia_gadol_clause revia_gadol_oleh_clause"""
    p[0] = make_node("oleh_weyored_clause", p[1], p[2])


# --- atnax clause (#362, #364) -------------------------------------------------
# Subdivided by revia gadol (distant) or dexi (near); and, like the silluq domain
# (and as L attests, MAM-confirmed), directly by a lower disjunctive -- pazer or
# legarmeh -- when the unit is too short for a dexi.  Rank order of near dividers:
# revia gadol (highest), dexi, pazer, legarmeh; each may be followed (toward
# atnax) by any lower one.
def p_atnax_clause(p):
    """atnax_clause : atnax_phrase
    | dexi_atnax_clause
    | revia_gadol_atnax_clause
    | pazer_atnax_clause
    | legarmeh_atnax_clause"""
    p[0] = p[1]


def p_legarmeh_atnax_clause(p):
    """legarmeh_atnax_clause : legarmeh_clause atnax_phrase
    | legarmeh_clause legarmeh_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


def p_pazer_atnax_clause(p):
    """pazer_atnax_clause : pazer_clause atnax_phrase
    | pazer_clause legarmeh_atnax_clause
    | pazer_clause pazer_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


def p_dexi_atnax_clause(p):
    """dexi_atnax_clause : dexi_clause atnax_phrase
    | dexi_clause legarmeh_atnax_clause
    | dexi_clause pazer_atnax_clause
    | dexi_clause dexi_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


def p_revia_gadol_atnax_clause(p):
    """revia_gadol_atnax_clause : revia_gadol_clause atnax_phrase
    | revia_gadol_clause dexi_atnax_clause
    | revia_gadol_clause pazer_atnax_clause
    | revia_gadol_clause legarmeh_atnax_clause
    | revia_gadol_clause revia_gadol_atnax_clause"""
    p[0] = make_node("atnax_clause", p[1], p[2])


# --- revia gadol clause (#363) -------------------------------------------------
# Its subdividers, in rank order: dexi (highest), pazer, legarmeh.  Yeivin names
# pazer and legarmeh; L also attests dexi directly subdividing revia gadol (e.g.
# DEXI REVIA_GADOL ATNAX ...), the same near-divider relation dexi has under atnax.
def p_revia_gadol_clause(p):
    """revia_gadol_clause : revia_gadol_phrase
    | legarmeh_revia_gadol_clause
    | pazer_revia_gadol_clause
    | dexi_revia_gadol_clause
    | tsinnor_revia_gadol_clause"""
    p[0] = p[1]


# Tsinnor (a second-degree divider, rank with dexi) also subdivides revia gadol
# directly where L has no oleh-we-yored (e.g. Ps 55:20, TSINNOR REVIA_GADOL ATNAX;
# MAM has REVIA_QATAN OLEH_WEYORED there -- an L/MAM divergence the xcheck flags,
# parsed faithfully to L here).
def p_tsinnor_revia_gadol_clause(p):
    """tsinnor_revia_gadol_clause : tsinnor_clause revia_gadol_phrase
    | tsinnor_clause legarmeh_revia_gadol_clause
    | tsinnor_clause tsinnor_revia_gadol_clause"""
    p[0] = make_node("revia_gadol_clause", p[1], p[2])


def p_legarmeh_revia_gadol_clause(p):
    """legarmeh_revia_gadol_clause : legarmeh_clause revia_gadol_phrase
    | legarmeh_clause legarmeh_revia_gadol_clause"""
    p[0] = make_node("revia_gadol_clause", p[1], p[2])


def p_pazer_revia_gadol_clause(p):
    """pazer_revia_gadol_clause : pazer_clause revia_gadol_phrase
    | pazer_clause legarmeh_revia_gadol_clause
    | pazer_clause pazer_revia_gadol_clause"""
    p[0] = make_node("revia_gadol_clause", p[1], p[2])


def p_dexi_revia_gadol_clause(p):
    """dexi_revia_gadol_clause : dexi_clause revia_gadol_phrase
    | dexi_clause legarmeh_revia_gadol_clause
    | dexi_clause pazer_revia_gadol_clause
    | dexi_clause dexi_revia_gadol_clause"""
    p[0] = make_node("revia_gadol_clause", p[1], p[2])


# --- revia qatan clause (#368) -------------------------------------------------
# Its subdividers are tsinnor (higher) and legarmeh.  Yeivin treats revia qatan and
# tsinnor as alternatives immediately before oleh-we-yored, but when both occur
# (TSINNOR REVIA_QATAN OLEH_WEYORED, ~12 verses) revia qatan is the one adjacent to
# oleh and tsinnor subdivides its remaining span -- so tsinnor heads a clause within
# the revia qatan domain, with legarmeh below it.
def p_revia_qatan_clause(p):
    """revia_qatan_clause : revia_qatan_phrase
    | legarmeh_revia_qatan_clause
    | tsinnor_revia_qatan_clause"""
    p[0] = p[1]


def p_legarmeh_revia_qatan_clause(p):
    """legarmeh_revia_qatan_clause : legarmeh_clause revia_qatan_phrase
    | legarmeh_clause legarmeh_revia_qatan_clause"""
    p[0] = make_node("revia_qatan_clause", p[1], p[2])


def p_tsinnor_revia_qatan_clause(p):
    """tsinnor_revia_qatan_clause : tsinnor_clause revia_qatan_phrase
    | tsinnor_clause legarmeh_revia_qatan_clause
    | tsinnor_clause tsinnor_revia_qatan_clause"""
    p[0] = make_node("revia_qatan_clause", p[1], p[2])


# --- revia mugrash clause (#366-367) -------------------------------------------
# With the geresh stroke: the last disjunctive before silluq, like prose tipexa,
# subdivided by the lesser dividers pazer / legarmeh.  "Without the geresh" (a bare
# revia before silluq when the verse has no atnax) it acts as the main verse
# divider "like atnax", so it is also subdivided by dexi (near) and revia gadol
# (distant).  Both roles share the REVIA_MUGRASH token, so all four are allowed.
def p_revia_mugrash_clause(p):
    """revia_mugrash_clause : revia_mugrash_phrase
    | legarmeh_revia_mugrash_clause
    | pazer_revia_mugrash_clause
    | dexi_revia_mugrash_clause
    | revia_gadol_revia_mugrash_clause"""
    p[0] = p[1]


def p_legarmeh_revia_mugrash_clause(p):
    """legarmeh_revia_mugrash_clause : legarmeh_clause revia_mugrash_phrase
    | legarmeh_clause legarmeh_revia_mugrash_clause"""
    p[0] = make_node("revia_mugrash_clause", p[1], p[2])


def p_pazer_revia_mugrash_clause(p):
    """pazer_revia_mugrash_clause : pazer_clause revia_mugrash_phrase
    | pazer_clause legarmeh_revia_mugrash_clause
    | pazer_clause pazer_revia_mugrash_clause"""
    p[0] = make_node("revia_mugrash_clause", p[1], p[2])


def p_dexi_revia_mugrash_clause(p):
    """dexi_revia_mugrash_clause : dexi_clause revia_mugrash_phrase
    | dexi_clause dexi_revia_mugrash_clause"""
    p[0] = make_node("revia_mugrash_clause", p[1], p[2])


def p_revia_gadol_revia_mugrash_clause(p):
    """revia_gadol_revia_mugrash_clause : revia_gadol_clause revia_mugrash_phrase
    | revia_gadol_clause legarmeh_revia_mugrash_clause
    | revia_gadol_clause pazer_revia_mugrash_clause
    | revia_gadol_clause dexi_revia_mugrash_clause
    | revia_gadol_clause revia_gadol_revia_mugrash_clause"""
    p[0] = make_node("revia_mugrash_clause", p[1], p[2])


# --- dexi clause (#364) --------------------------------------------------------
def p_dexi_clause(p):
    """dexi_clause : dexi_phrase
    | legarmeh_dexi_clause
    | pazer_dexi_clause"""
    p[0] = p[1]


def p_legarmeh_dexi_clause(p):
    """legarmeh_dexi_clause : legarmeh_clause dexi_phrase
    | legarmeh_clause legarmeh_dexi_clause"""
    p[0] = make_node("dexi_clause", p[1], p[2])


def p_pazer_dexi_clause(p):
    """pazer_dexi_clause : pazer_clause dexi_phrase
    | pazer_clause legarmeh_dexi_clause
    | pazer_clause pazer_dexi_clause"""
    p[0] = make_node("dexi_clause", p[1], p[2])


# --- tsinnor clause (#365) ------------------------------------------------------
def p_tsinnor_clause(p):
    """tsinnor_clause : tsinnor_phrase
    | legarmeh_tsinnor_clause
    | pazer_tsinnor_clause"""
    p[0] = p[1]


# NOTE: tsinnor may repeat before oleh-we-yored (Ps 17:14, ...TSINNOR TSINNOR GALGAL
# OLEH_WEYORED; MAM-confirmed).  It is intentionally NOT modeled as a grammar
# production: the repeated tsinnor before an oleh that itself carries a servus is
# beyond LALR(1) -- the servus is ambiguous between the next repeated tsinnor's
# servi prefix and oleh's own servi, and the merged lookahead dead-ends.  Adding
# it parsed no verse.  Instead the repeat is accepted at the parse boundary by
# collapsing it to a single TSINNOR before parsing (collapse_repeated_tsinnor /
# parse_tokens_accepting_repeats, below): a repeated divider counts once, so the
# existing tsinnor productions parse it, with no LALR distortion of the servus
# handling.  parse_tokens_diagnostic itself stays the raw, uncollapsed verdict.


def p_legarmeh_tsinnor_clause(p):
    """legarmeh_tsinnor_clause : legarmeh_clause tsinnor_phrase
    | legarmeh_clause legarmeh_tsinnor_clause"""
    p[0] = make_node("tsinnor_clause", p[1], p[2])


def p_pazer_tsinnor_clause(p):
    """pazer_tsinnor_clause : pazer_clause tsinnor_phrase
    | pazer_clause legarmeh_tsinnor_clause
    | pazer_clause pazer_tsinnor_clause"""
    p[0] = make_node("tsinnor_clause", p[1], p[2])


# --- pazer clause (#369) -------------------------------------------------------
# The only subordinate disjunctive is legarmeh.
def p_pazer_clause(p):
    """pazer_clause : pazer_phrase
    | legarmeh_pazer_clause"""
    p[0] = p[1]


def p_legarmeh_pazer_clause(p):
    """legarmeh_pazer_clause : legarmeh_clause pazer_phrase
    | legarmeh_clause legarmeh_pazer_clause"""
    p[0] = make_node("pazer_clause", p[1], p[2])


# --- legarmeh clause (#370) ----------------------------------------------------
# The lowest disjunctive: no subordinate disjunctive, but legarmeh may repeat.
def p_legarmeh_clause(p):
    """legarmeh_clause : legarmeh_phrase
    | legarmeh_clause legarmeh_phrase"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = make_node("legarmeh_clause", p[1], p[2])


# --- shalshelet gedolah clause (#371) ------------------------------------------
# A disjunctive in the second half before silluq (revia mugrash rank); distinct from the
# conjunctive shalshelet qetannah.  Its servant is merkha: Breuer Ch 11 §37 (merkha, with a
# tarxa before it), confirmed by servi_xcheck (2026-06-17) -- all 3 poetic occurrences
# carry a merkha servant in both L and MAM (uniform, zero conflicts), like small revia'.
# (This corrects an earlier "as a rule it has no servi" note, which holds for the prose
# shalshelet gedolah but not the poetic one.)  Left permissive; a merkha constraint would
# fire on nothing.  See issue #18.
def p_shalshelet_gedolah_clause(p):
    "shalshelet_gedolah_clause : shalshelet_gedolah_phrase"
    p[0] = p[1]


# --- error callback ------------------------------------------------------------
@dataclass(frozen=True)
class ParseError:
    """Where a NO_PARSE verse's parse dead-ended -- the pinpoint for an ungrammatical verse.

    ``token_type`` is the offending lookahead: the first token the LALR(1) parser
    could not shift onto any valid prefix.  ``accent_index`` is its 1-based position
    among the verse's accent tokens (the TILDE/SOFPASUQ bookends excluded), so index
    k means "every accent through k-1 was consumable; accent k is where the grammar
    stalled."

    This is the stall point, not necessarily the root-cause accent: a hierarchy
    violation a few accents earlier can leave a still-valid prefix that only
    dead-ends here.  Ps 17:14 is the canonical case -- its double tsinnor (#7-8) plus
    galgal (#9) parse fine, and the parse only fails at the OLEH_WEYORED (#10) that
    follows them, because that oleh has nowhere to attach after the repeated tsinnor.
    So the locus narrows the failure to a region ("valid through GALGAL, stalled at
    OLEH_WEYORED") rather than blaming the whole verse, even though the reader must
    still look just left of the stall for the cause.
    """

    token_type: str
    accent_index: int


class _PoeticUnrecoverable(Exception):
    """Raised from p_error to abort error recovery for non-category-A failures.

    Carries the offending PLY lookahead token (always a real accent -- p_error
    raises this only for a non-SOFPASUQ token), so parse_tokens_diagnostic can
    report the stall locus instead of a bare None.
    """

    def __init__(self, token):
        super().__init__()
        self.token = token


def p_error(p):  # noqa: D401  (PLY callback)
    # Recovery is allowed ONLY for the missing-silluq shape (category A): the
    # syntax error must be the verse-final sof pasuq arriving where the silluq was
    # due (p.type == SOFPASUQ).  In that one case, do nothing and let PLY recover
    # via p_silluq_phrase_error, producing an ERROR-leaf silluq_phrase while
    # preserving the rest of the verse's structure.
    #
    # Every other syntax error is a genuine non-parse -- a disjunctive standing
    # where the hierarchy forbids it (the handful of L anomalies where MAM
    # differs).  There, PLY's generic error-token recovery would pop the stack
    # to the silluq_phrase context and swallow the whole tail into one ERROR leaf,
    # destroying the diagnostic token sequence.  Abort instead, so parse_tokens
    # returns None and the driver records an informative NO_PARSE line.
    if p is not None and p.type != pan.SOFPASUQ:
        raise _PoeticUnrecoverable(p)
    # else (mid-verse EOF, or the verse-final SOFPASUQ): let PLY recover.


class _LexToken:
    """Minimal PLY-compatible token object (mirrors prose_ply_grammar._LexToken)."""

    __slots__ = ("type", "value", "lineno", "lexpos", "lexer")

    def __init__(self, ttype: str, value: str):
        self.type = ttype
        self.value = value
        self.lineno = 0
        self.lexpos = 0
        self.lexer = None


class _TokenStream:
    """Adapts a list of (type, leaf) pairs to PLY's lexer interface.

    Each emitted token carries its 0-based position in the stream as ``lexpos`` so
    that, on a syntax error, p_error's offending lookahead token pinpoints where the
    parse stalled (see ParseError).  TILDE is index 0, so an accent's 1-based ordinal
    among the accents equals its lexpos.
    """

    def __init__(self, toks):
        self._it = iter(enumerate(toks))

    def input(self, _s):  # PLY may call this; we ignore it.
        pass

    def token(self):
        try:
            index, (ttype, leaf) = next(self._it)
        except StopIteration:
            return None
        tok = _LexToken(ttype, leaf)
        tok.lexpos = index
        return tok


def build_parser(*, capture_warnings: bool = False):
    """Build the poetic PLY parser.

    With ``capture_warnings=True`` the LALR construction log (shift/reduce and
    reduce/reduce conflict warnings) is returned alongside the parser, for grammar
    development; otherwise warnings are silenced like the prose grammar.
    """
    if capture_warnings:
        import io
        import logging

        buf = io.StringIO()
        handler = logging.StreamHandler(buf)
        log = logging.getLogger("poetic_ply_grammar")
        log.handlers = [handler]
        log.setLevel(logging.WARNING)
        parser = yacc.yacc(
            module=sys.modules[__name__],
            write_tables=False,
            debug=False,
            errorlog=log,
        )
        return parser, buf.getvalue()
    return yacc.yacc(
        module=sys.modules[__name__],
        write_tables=False,
        debug=False,
        errorlog=yacc.NullLogger(),
    )


def parse_tokens_diagnostic(parser, toks):
    """Parse one poetic verse, returning ``(tree, error)``.

    On success ``tree`` is the parse tree (tree.TN) -- including a missing-silluq
    ERROR-leaf tree for category A -- and ``error`` is None.  On an unrecoverable
    failure (NO_PARSE) ``tree`` is None and ``error`` is a ParseError naming the
    offending token and its accent ordinal, so the caller can pinpoint the stall
    rather than flag the whole verse.

    ``toks`` is a list of (token_type, leaf_name) pairs beginning with
    ('TILDE', '') and ending with ('SOFPASUQ', 'sof pasuq').
    """
    try:
        return parser.parse(lexer=_TokenStream(toks)), None
    except _PoeticUnrecoverable as exc:
        tok = exc.token
        # tok.lexpos is the offending token's 0-based index in the full stream;
        # TILDE occupies index 0, so the 1-based accent ordinal equals lexpos.
        return None, ParseError(token_type=tok.type, accent_index=tok.lexpos)


def parse_tokens(parser, toks):
    """Parse one poetic verse's token stream, returning the tree or None.

    Thin wrapper over parse_tokens_diagnostic for the many callers that only need
    the tree (and a None / not-None test); use parse_tokens_diagnostic when the
    NO_PARSE stall locus is wanted.
    """
    return parse_tokens_diagnostic(parser, toks)[0]


def collapse_repeated_tsinnor(toks):
    """Return ``toks`` with each run of consecutive TSINNOR collapsed to one.

    A repeated disjunctive is the same divider written twice (Yeivin on the
    repeatable zarqa; Breuer Ch. 10 §9 on the doubled tsinnor, with Wickes p. 81
    n. 4) -- for grammaticality it counts once.  Collapsing the run lets the
    existing tsinnor productions parse it without a dedicated grammar rule the
    LALR(1) table cannot express (see the tsinnor-clause NOTE).

    Motivated by, and ONLY by, Ps 17:14.  That verse is the sole place in the
    Three Books where two tsinnor occur consecutively (of the 250 tsinnor-bearing
    poetic verses), so this rule fires on exactly one verse and exists only
    because of it.  It is phrased as a pattern (any consecutive-TSINNOR run)
    rather than a "ps 17:14" reference whitelist on principle -- a repeated
    divider counts once, wherever it occurs -- not because any other verse needs
    it; should the corpus ever change, this is the only verse it currently
    affects.

    Returns a new list with adjacent duplicate TSINNOR tokens dropped, or a list
    equal to the input when there is no such repeat.  This is a parse-only
    normalization: callers pass the canonical token list and must NOT let the
    result replace it, so the WLC-vs-MAM disjunctive cross-check keeps counting
    every tsinnor.
    """
    out: list[tuple[str, str]] = []
    prev = None
    for ttype, leaf in toks:
        if ttype == pan.TSINNOR and prev == pan.TSINNOR:
            continue
        out.append((ttype, leaf))
        prev = ttype
    return out


def parse_tokens_accepting_repeats(parser, toks):
    """Parse, accepting a repeated TSINNOR divider as a single divider.

    First parses ``toks`` as-is -- the grammar's raw verdict, which keeps
    parse_tokens_diagnostic pure and the stall-locus diagnostics intact.  Only if
    that is a NO_PARSE *and* the verse repeats a TSINNOR does it retry on a copy
    with the repeat collapsed (collapse_repeated_tsinnor), returning that result
    when it parses.  So Ps 17:14's double tsinnor (the lone case in the Three
    Books) is accepted without distorting the servus handling, while every other
    verse takes the raw verdict unchanged.

    Returns ``(tree, error)`` like parse_tokens_diagnostic.  The collapse is
    internal and never mutates ``toks``.
    """
    tree, error = parse_tokens_diagnostic(parser, toks)
    if tree is not None:
        return tree, error
    collapsed = collapse_repeated_tsinnor(toks)
    if collapsed == toks:
        return tree, error
    tree2, error2 = parse_tokens_diagnostic(parser, collapsed)
    if tree2 is not None:
        return tree2, error2
    return tree, error
