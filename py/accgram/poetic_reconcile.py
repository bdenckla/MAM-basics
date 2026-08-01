r"""Reconcile the poetic scanner's token stream with two corrections WLC's
Michigan-Claremont source cannot express on its own.

The poetic scanner (``poetic_scanner``) reads each verse from the M-C accent
codes alone.  Two distinctions are simply not *in* that encoding, so the scanner
makes a blanket guess that this module corrects before the grammar sees the tokens:

1. **legarmeh vs paseq.**  A conjunctive (azla 63 / mahapakh 70) followed by a paseq
   (05) is written identically whether it is a legarmeh (a disjunctive) or a
   narrow-sense paseq (the conjunctive stays a servus and the bar is a bare pause).  The scanner
   emits ``LEGARMEH`` for *every* such sequence.  MAM-simple, by contrast, encodes the
   distinction structurally (``lp-legarmeih`` vs ``lp-paseq`` nodes), so we treat MAM
   as the oracle: where MAM has a narrow-sense paseq we demote the scanner's ``LEGARMEH``
   back to its underlying conjunctive servus (the paseq is then swallowed, as such a
   paseq always is).  This is the poetic counterpart of the prose scanner's
   has_legarmeh rule+exception list, but data-driven from MAM rather than hardcoded.
   (A future project, gh issue, may replace the MAM oracle with a poetic rule that
   needs only a small hardcoded exception list -- see doc / the issue.)

2. **the unmarked oleh-we-yored** (Yeivin ITM #363).  L sometimes writes the yored of
   an oleh-we-yored as a bare merkha (71) with the upper ole sign dropped, so the
   scanner reads a conjunctive merkha and misses the divider.  ``poetic_scanner``
   already recovers the cases its galgal-servus heuristic can see; the rest are
   recovered here by *charitable parsing*: if a verse does not parse, but reinterpreting
   exactly one of its merkhas as an (unmarked) yored makes it parse, adopt that reading.
   This consults no oracle -- only the grammar -- and touches only verses that would
   otherwise be NO_PARSE, so it can never change a verse that already parses.

The two passes run in order (demotion first, then charitable parsing): at Ps 68:20 and
Pr 30:15 both corrections are needed, and the merkha the charitable pass promotes is the
word immediately after the demoted legarmeh -- independently reproducing MAM's reading.
"""

from __future__ import annotations

import difflib
import re

from accgram import accent_marks as am
from accgram import poetic_accent_names as pan
from accgram.poetic_ply_grammar import parse_tokens
from accgram.poetic_accent_names import POETIC_DISJUNCTIVES

# A conjunctive (azla/qadma or mahapakh/mahapakh) followed eventually by a paseq within
# one whitespace-delimited chanted word -- the legarmeh the scanner emits.  Mirrors the
# scanner's leftmost-longest legarmeh rule, so group(1) is the servus mark the legarmeh
# sits on (issue #9, Phase 2: matched over the Unicode mark alphabet).
_LEGARMEH_WORD_RE = re.compile(
    r"(" + am.QADMA + r"|" + am.MAHAPAKH + r")" + am.TEXT + am.PASEQ
)
_SERVUS_FOR_CODE = {am.QADMA: pan.AZLA, am.MAHAPAKH: pan.MAHAPAKH}


def reconcile_tokens(
    reference: str,
    body: str,
    tokens: list[tuple[str, str]],
    mam_disjunctives: list[str] | None,
    parser: object,
) -> list[tuple[str, str]]:
    """Return ``tokens`` with the two M-C-inexpressible corrections applied.

    ``mam_disjunctives`` is MAM-simple's ordered disjunctive skeleton for this verse
    (None if the verse is absent from MAM); ``parser`` is a built poetic LALR parser.
    """
    tokens = _demote_mam_paseq(body, tokens, mam_disjunctives)
    if parse_tokens(parser, tokens) is None:
        recovered = _charitable_oleh(tokens, parser)
        if recovered is not None:
            tokens = recovered
    return tokens


def _demote_mam_paseq(
    body: str,
    tokens: list[tuple[str, str]],
    mam_disjunctives: list[str] | None,
) -> list[tuple[str, str]]:
    """Demote each scanner ``LEGARMEH`` MAM does not read as a legarmeh.

    A WLC legarmeh that the disjunctive-skeleton alignment (the same ``difflib`` engine
    ``poetic_xcheck`` uses) does not pair with a MAM legarmeh is, per MAM, a plain
    paseq: replace the ``LEGARMEH`` token with its underlying conjunctive servus (the
    paseq is dropped).  No-op when the verse is absent from MAM or carries no legarmeh.
    """
    if mam_disjunctives is None:
        return tokens
    wlc_disj = [t for t, _ in tokens if t in POETIC_DISJUNCTIVES]
    if pan.LEGARMEH not in wlc_disj:
        return tokens

    demote = _legarmeh_positions_to_demote(wlc_disj, mam_disjunctives)
    if not demote:
        return tokens

    servi = _legarmeh_underlying_servi(body)
    out: list[tuple[str, str]] = []
    disj_i = -1
    leg_i = -1
    for ttype, leaf in tokens:
        if ttype in POETIC_DISJUNCTIVES:
            disj_i += 1
            if ttype == pan.LEGARMEH:
                leg_i += 1
                if disj_i in demote:
                    servus = servi[leg_i] if leg_i < len(servi) else pan.MAHAPAKH
                    out.append((servus, _SERVUS_LEAF[servus]))
                    continue
        out.append((ttype, leaf))
    return out


def _legarmeh_positions_to_demote(wlc_disj: list[str], mam_disj: list[str]) -> set[int]:
    """Indices (into ``wlc_disj``) of WLC legarmehs not matched to a MAM legarmeh."""
    matcher = difflib.SequenceMatcher(a=wlc_disj, b=mam_disj, autojunk=False)
    demote: set[int] = set()
    for tag, i1, i2, _j1, _j2 in matcher.get_opcodes():
        if tag in ("replace", "delete"):
            for k in range(i1, i2):
                if wlc_disj[k] == pan.LEGARMEH:
                    demote.add(k)
    return demote


def _legarmeh_underlying_servi(body: str) -> list[str]:
    """The conjunctive servus under each scanner legarmeh, in left-to-right order."""
    servi: list[str] = []
    for word in body.split():
        match = _LEGARMEH_WORD_RE.search(word)
        if match is not None:
            servi.append(_SERVUS_FOR_CODE[match.group(1)])
    return servi


def _charitable_oleh(
    tokens: list[tuple[str, str]], parser: object
) -> list[tuple[str, str]] | None:
    """Reinterpret one ambiguous merkha as an unmarked yored if that uniquely parses.

    Tries promoting each ``MERKHA`` to ``OLEH_WEYORED`` in turn; returns the promoted
    token list iff exactly one such promotion yields a parse (an ambiguous or empty
    result leaves the verse NO_PARSE, returning None).  The caller invokes this only on
    verses that do not already parse.
    """
    solutions: list[list[tuple[str, str]]] = []
    for i, (ttype, _leaf) in enumerate(tokens):
        if ttype != pan.MERKHA:
            continue
        candidate = list(tokens)
        candidate[i] = (pan.OLEH_WEYORED, _OLEH_LEAF)
        if parse_tokens(parser, candidate) is not None:
            solutions.append(candidate)
    return solutions[0] if len(solutions) == 1 else None


# Display leaf names for the tokens this module introduces, matching
# poetic_scanner._LEAF (kept local to avoid importing the scanner's private map).
_SERVUS_LEAF = {pan.AZLA: "azla", pan.MAHAPAKH: "mahapakh"}
_OLEH_LEAF = "oleh we-yored"
