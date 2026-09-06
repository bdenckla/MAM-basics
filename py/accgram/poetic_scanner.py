r"""Hand-written scanner for the POETIC (Three Books) accent system.

The poetic counterpart of accgram.prose_scanner.  Where the prose scanner ports
tnk2acc.l's GG-state table verbatim, there is no poetic flex source, so the rule
table here is built from the *poetic* (Tabula Accentuum column II) readings of the
accents, as tabulated in ``in/wlc420/supplmt.wts`` and cross-checked
against decoded L verses.  The rule table matches over the Unicode mark alphabet
(``accent_marks``, the ``am.*`` patterns below); each accent is its own codepoint.

accent -> poetic reading (the accents that matter in the Three Books):

  disjunctives
    sof pasuq
    silluq        a meteg/silluq immediately before sof pasuq              II.1
    atnax                                                                  II.3
    oleh-we-yored ole sign (above, pre-stress) plus the yored = merkha     II.2
                  below the stress; the merkha is consumed into the one
                  OLEH_WEYORED token, not emitted as a servus.  WLC 4.22 writes
                  the pair cross-letter (ole then, later, the yored merkha);
                  MAM stacks both on one base letter (stored merkha-then-ole)
                  when the stress is word-initial -- both shapes fuse here.
    revia mugrash geresh muqdam (preposed) plus revia; if the revia dot    II.5
                  is omitted because it would fall on the same letter as
                  the geresh muqdam, it is implied
    revia         gadol or qatan -- same sign; disambiguated in a second   II.4=8
                  pass: a revia whose next disjunctive is oleh-we-yored
                  is qatan, otherwise gadol
    dexi                                                                   II.9
    tsinnor       (no zarqa exists in the poetic system)                   II.7
    pazer                                                                  II.10
    shalshelet gedolah  shalshelet sign + paseq                           II.6
    legarmeh      azla legarmeh / mahapakh legarmeh, i.e. a conjunctive    II.12
                  (azla or mahapakh) followed by paseq, as prose munax+paseq

  conjunctive servi
    munax   merkha   mahapakh   azla   illuy   tarxa
    galgal (yerax; also the servus of oleh-we-yored and of pazer)

  fused / emitted (Plan C -- stop swallowing real accents)
    tsinnorit     fused onto its mahapakh / merkha partner in the same
                  chanted word -> one MAHAPAKH_METSUNNAR / MERKHA_METSUNNAR conjunctive
    shalshelet qetannah  bare shalshelet (no following paseq) -> emitted as a servus
    two adjacent accents on one letter that are not a WHITELISTED pair (revia+geresh
                  muqdam, ole+yored, dexi+munax) -> one order-less a!b bang-pair (e.g.
                  merkha + azla -> merkha!azla); faithfully emitted but NOT a grammar
                  token (a non-whitelisted same-letter stack is a lexical anomaly ->
                  NO_PARSE)

  swallowed (secondary / meteg / separators, not structural accents)
    meteg (not before sof pasuq)   narrow-sense paseq   upper/lower puncta

  fail-fast (Plan C): any other stray accent (U+0591..U+05AE) no rule consumes is
  emitted as STRAY_ACCENT (the grammar has no terminal for it -> NO_PARSE), never
  silently swallowed.  Zero live customers (the lone ps124:4 geresh is consumed by the
  same-letter revia mugrash charity).

Note: "revia mugrash without geresh" (#367 = Breuer Ch 10 §14) -- a bare revia
acting as the main verse divider when the verse has no atnax -- is NOT a gap: it is
the last disjunctive before silluq, so _reclassify_revia maps it to REVIA_MUGRASH
(see that function's docstring), and the rich revia_mugrash_clause then carries its
viceroys (dexi etc.), parsing Breuer's revia-substitute-for-atnax verses (Ps
105:45, 119:4, Job 14:4) without verse-level context.

Known gaps (deferred to the validation pass, see the module's tests / notes):
  - oleh-we-yored whose ole is unmarked (only the yored merkha is written -- #363):
    recovered when the galgal servus immediately precedes it (see
    _recover_unmarked_oleh, MAM-cross-checked); the rarer "when a revia precedes"
    variant is still read as a servus (its signal is ambiguous -- see that helper).

The scanner returns a list of (token_type, leaf_name) pairs ready for
accgram.poetic_ply_grammar.parse_tokens; the verse begins with ('TILDE','') and
ends with ('SOFPASUQ', 'sof pasuq').
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from accgram import accent_marks as am
from accgram import poetic_accent_names as pan
from mb_cmn import hebrew_accents as ha
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

_TEXT = am.TEXT  # within one maqqef/space-delimited atom (as in prose)

# The run of letters after a tsinnorit, up to its partner, in the metsunnar rules:
# like _TEXT but also excluding every accent (U+0591..U+05AE), so the partner is the
# FIRST accent after the tsinnorit.  Intra-atom, this keeps the fusion from reaching
# across an intervening divider (an ole, a mahapakh-legarmeh) to a later conjunctive;
# in the omitted-maqaf rule it additionally enforces a tsinnorit-*only* first atom (no
# main accent of its own -- the cue that the chanted word continues across the hyphen).
_TSINNORIT_ATOM_TAIL = r"[^ \r\n֑-֮-]*"

# silluq right context (as in prose prose_scanner): meteg/silluq immediately before
# sof pasuq, rebuilt over the mark alphabet (issue wlc-utils#9, Phase 2).
_SILLUQ_LA = r"(?=" + am.negated_class(" \r\n-?~", "379") + r"*" + am.SOF_PASUQ + r")"

# Verse-structure line pattern, as in accgram.prose_scanner.scan_book: a verse line
# is "ch:vr <accent codes>".
_VERSE_RE = re.compile(r"^([1-9][0-9]*):([1-9][0-9]*)[ \t](.*)$")

# Disjunctive token types, for the revia gadol/qatan second-pass lookahead.
_POETIC_DISJUNCTIVES = pan.POETIC_DISJUNCTIVES

# Same-letter accent pairs: a WHITELIST, not a blacklist (Plan D).  Only a few accent
# pairs may legitimately share one base letter; ANY other two adjacent accents (no
# ``LETTER`` between -> same letter) is a lexical anomaly emitted as a bang.  The whitelist:
#   - revia + geresh muqdam   -> revia mugrash      (fused by the rule above)
#   - revia + (plain) geresh  -> revia mugrash      (the ps124:4 charity, fused above)
#   - oleh   + yored (merkha) -> oleh-we-yored      (fused above; cross-letter in WLC
#                                                    as ole...merkha, same-letter in MAM
#                                                    as merkha+ole -- each consumed by its
#                                                    own fusion rule, neither reaches here)
#   - dexi   + munax          -> a legit *sequence* (a prepositive dexi visually on its
#                                munax servus's letter, not a shared syllable)
# The first three are CONSUMED by the specific fusion rules above, so they never reach
# the guard; only dexi+munax reaches it as two adjacent marks, and is spared by name
# (_WHITELISTED_ADJACENT_PAIRS).  Everything else -> bang.  (This whitelist supersedes an
# earlier "two impositive accents" blacklist, which leaned on contested positional
# classifications of marks -- tsinnorit, ole -- that, per the corpus, never share a letter
# anyway; the whitelist is the honest rule and is also stricter.)
_ANY_ACCENT = (
    "[֑-֮]"  # U+0591..U+05AE (as the stray-accent class; meteg U+05BD excluded)
)

# Legit same-letter pairs that survive to the guard as two adjacent marks (i.e. are NOT
# fused by an earlier rule), spared from the bang via negative lookahead.  Order is the
# post-relocation body order (dexi, a prepositive, is moved to the front).
_WHITELISTED_ADJACENT_PAIRS = (am.DEXI + am.MUNAX,)

# Display names for building a bang's per-pair (type, leaf); covers the poetic accents,
# with a codepoint fallback for anything unforeseen.
_ACCENT_LEAF_NAME: dict[str, str] = {
    am.ATNAX: "atnax",
    am.SHALSHELET: "shalshelet",
    am.TIPEXA: "tarxa",
    am.REVIA: "revia",
    am.PAZER: "pazer",
    am.MUNAX: "munax",
    am.MAHAPAKH: "mahapakh",
    am.MERKHA: "merkha",
    am.QADMA: "azla",
    am.YERAX: "galgal",
    am.ILUY: "illuy",
    am.OLE: "ole",
    am.DEXI: "dexi",
    am.TSINNOR: "tsinnor",
    am.GERESH: "geresh",
    am.GERESH_MUQDAM: "geresh muqdam",
}


def _bang_pair_token(marks: str) -> tuple[str, str]:
    """(token_type, leaf) for two adjacent same-letter accents not on the whitelist.

    The leaf is the order-less bang ``a!b`` (e.g. ``merkha!azla``); the token type is its
    uppercased ``A_B`` form (e.g. ``MERKHA_AZLA``) -- informative in the NO_PARSE line and
    ParseError, and, for merkha+azla, exactly ``pan.MERKHA_AZLA``.  The grammar has no
    terminal for any such type, so the verse dead-ends to NO_PARSE (the poetic lexical-
    error surface)."""
    a = _ACCENT_LEAF_NAME.get(marks[0], f"U+{ord(marks[0]):04X}")
    b = _ACCENT_LEAF_NAME.get(marks[1], f"U+{ord(marks[1]):04X}")
    return f"{a}_{b}".upper(), f"{a}!{b}"


# The guard regex: any two adjacent accents EXCEPT a whitelisted sequence pair.
_BANG_GUARD = (
    "(?!" + "|".join(_WHITELISTED_ADJACENT_PAIRS) + ")" + _ANY_ACCENT + _ANY_ACCENT
)

# Rule table: (regex anchored at scan position, token type or None to swallow).
# Longest match wins; ties broken by order (mirrors flex / the prose scanner).
# The rule table matches over the Unicode mark alphabet (accent_marks): each accent
# is its own codepoint, and the merge rules below fuse a stress-helper / preposed
# sign onto its main accent.
_POETIC_GG_RULES: list[tuple[re.Pattern[str], str | None]] = [
    (re.compile(am.SOF_PASUQ), pan.SOFPASUQ),
    # silluq: meteg/silluq sign immediately before sof pasuq.
    (re.compile(am.METEG + _SILLUQ_LA), pan.SILLUQ),
    (re.compile(am.ATNAX), pan.ATNAX),
    # oleh-we-yored: ole plus its yored merkha in the same word; the merkha is
    # consumed here so it is not also emitted as a servus.  Bare ole (yored on
    # the next word, or unmarked) still yields the accent.  Two graphical shapes:
    #   - cross-letter (WLC 4.22): the ole sits on the pre-stress letter and the yored
    #     merkha on a later (stress) letter of the same word, so the ole's codepoint comes
    #     first -> OLE ... MERKHA, matched by the first rule (its _TEXT spans the letters
    #     between).  This is the ONLY shape WLC 4.22 uses (corpus-wide: 0 same-letter).
    #   - same-letter (MAM, and any edition that stacks the pair): when the stress is on the
    #     word's first syllable the yored merkha and the ole land on ONE base letter, stored
    #     merkha-THEN-ole (no ``LETTER`` between) -> matched by the MERKHA+OLE rule.  13 verses
    #     across Ps/Prov/Job in MAM-simple (e.g. Ps 30:12 לִ֥֫י), none in WLC 4.22.
    # Both shapes fuse to the one OLEH_WEYORED disjunctive -- the merkha is the yored, not a
    # servus.  Without the same-letter rule MAM's merkha+ole would fall through to the bang
    # guard and be flagged merkha!ole -> NO_PARSE; this keeps the checker faithful to a wider
    # range of texts (issue wlc-utils#42) while leaving WLC 4.22 output unchanged (the rule never fires
    # there).  The MERKHA+OLE rule must precede both the bare MERKHA servus rule and the bang
    # guard, which it does (longest-match ties to the bang guard but wins by earlier order).
    (re.compile(am.OLE + _TEXT + am.MERKHA), pan.OLEH_WEYORED),
    (re.compile(am.MERKHA + am.OLE), pan.OLEH_WEYORED),
    (re.compile(am.OLE), pan.OLEH_WEYORED),
    # revia mugrash: geresh muqdam plus revia in the same word; the revia is
    # consumed.  Bare geresh muqdam = implied revia (omitted because it would share
    # the geresh muqdam's letter).
    (re.compile(am.GERESH_MUQDAM + _TEXT + am.REVIA), pan.REVIA_MUGRASH),
    (re.compile(am.GERESH_MUQDAM), pan.REVIA_MUGRASH),
    # revia mugrash by same-letter charity (ps124:4): a *plain* geresh is illegal
    # in the Three Books -- it has no poetic rule and is the lone accent the catch-all
    # silently swallows (corpus-wide, exactly once).  The sole charitable exception is a
    # plain geresh sharing one letter with a revia: read it as revia mugrash.  Mechanism
    # = within-letter order-normalize (revia+geresh, the storage order, is equivalent to
    # geresh+revia -- we are liberal about mark order *within* a letter, never across)
    # then promote the geresh to geresh muqdam, which the rule above fuses; expressed
    # here directly as one REVIA+GERESH fusion.  Adjacency (no ``LETTER`` between) keeps it
    # same-letter only.  (Failing fast on any *other* stray accent is deferred to the
    # poetic "stop swallowing" work, Plan C; geresh is the only attested case.)
    (re.compile(am.REVIA + am.GERESH), pan.REVIA_MUGRASH),
    (re.compile(am.DEXI), pan.DEXI),
    (re.compile(am.TSINNOR), pan.TSINNOR),
    (re.compile(am.PAZER), pan.PAZER),
    # shalshelet gedolah = shalshelet followed by paseq.  Longer than the bare
    # shalshelet (qetannah) rule below, so the paseq case wins by longest-match.
    (re.compile(am.SHALSHELET + _TEXT + am.PASEQ), pan.SHALSHELET_GEDOLAH),
    # shalshelet qetannah = bare shalshelet (no following paseq): a real conjunctive
    # servus (#371) in eight verses, emitted rather than swallowed.
    (re.compile(am.SHALSHELET), pan.SHALSHELET_QETANNAH),
    # legarmeh = azla (qadma) or mahapakh followed by paseq.  Must precede
    # the bare AZLA / MAHAPAKH rules so the longer paseq-terminated match wins.
    (
        re.compile(r"(?:" + am.QADMA + r"|" + am.MAHAPAKH + r")" + _TEXT + am.PASEQ),
        pan.LEGARMEH,
    ),
    # mahapakh / merkha metsunnar = a tsinnorit (U+0598) fused onto its mahapakh /
    # merkha partner in the same chanted word, the secondary tsinnorit consumed into
    # one conjunctive token instead of swallowed (Plan C).  Two graphical shapes:
    #   - intra-atom: tsinnorit and its partner in one space/maqaf-delimited atom;
    #   - omitted-maqaf: a tsinnorit-only atom (no main accent of its own -- the cue),
    #     then a single space (the omitted hyphen, Breuer §22), then the next atom that
    #     completes the chanted word and carries the partner.  Must precede the bare
    #     MAHAPAKH / MERKHA rules.  Both shapes use _TSINNORIT_ATOM_TAIL (no accent
    #     between the tsinnorit and its partner): the partner is the FIRST accent after
    #     the tsinnorit (Yeivin §372 "immediately before the stress"; corpus-confirmed
    #     for all 198), so the rule cannot reach across an intervening divider (an ole,
    #     a mahapakh-legarmeh) to steal it, and the two shapes stay disjoint.
    (
        re.compile(am.TSINNORIT + _TSINNORIT_ATOM_TAIL + am.MAHAPAKH),
        pan.MAHAPAKH_METSUNNAR,
    ),
    (re.compile(am.TSINNORIT + _TSINNORIT_ATOM_TAIL + am.MERKHA), pan.MERKHA_METSUNNAR),
    (
        re.compile(am.TSINNORIT + _TSINNORIT_ATOM_TAIL + " " + _TEXT + am.MAHAPAKH),
        pan.MAHAPAKH_METSUNNAR,
    ),
    (
        re.compile(am.TSINNORIT + _TSINNORIT_ATOM_TAIL + " " + _TEXT + am.MERKHA),
        pan.MERKHA_METSUNNAR,
    ),
    # revia (gadol/qatan) -- reclassified in the second pass.
    (re.compile(am.REVIA), pan.REVIA),
    # bang guard = any two adjacent accents on one base letter (no ``LETTER`` between -> same
    # letter) that are NOT a whitelisted pair: a lexical anomaly, fused into one order-less
    # `a!b` bang (Plan D) rather than emitted as a reorderable sequence.  Type/leaf per
    # pair via _bang_pair_token (merkha+qadma -> MERKHA_AZLA / merkha!azla, the poetic
    # sibling of prose ek20:31's mahapakh!azla).  The 2-mark match beats the bare
    # single-mark rules by longest-match.  The legit same-letter pairs are either FUSED by
    # a rule above (revia+geresh muqdam / revia+geresh -> revia mugrash; ole+merkha and
    # the MAM same-letter merkha+ole -> oleh-we-yored) and so never reach here, or are the dexi+munax sequence, which
    # _BANG_GUARD's lookahead spares.  The bang has no grammar terminal -> NO_PARSE ungrammatical verse.
    # Corpus-wide this fires only at Ps 56:10 (merkha+azla); the generality guards any
    # other / future same-letter stack.
    (re.compile(_BANG_GUARD), pan.BANG_PAIR),
    # conjunctive servi
    (re.compile(am.MUNAX), pan.MUNAX),
    (re.compile(am.MERKHA), pan.MERKHA),
    (re.compile(am.MAHAPAKH), pan.MAHAPAKH),
    (re.compile(am.QADMA), pan.AZLA),
    # MAM has the oleh-we-yored servus with atnax hafux. The Leningrad
    # transcription writes galgal in the same structural slot, so both emit GALGAL.
    (re.compile(ha.ATN_H), pan.GALGAL),
    (re.compile(am.ILUY), pan.ILLUY),
    (re.compile(am.TIPEXA), pan.TARXA),
    (re.compile(am.YERAX), pan.GALGAL),
    # swallowed: meteg, narrow-sense paseq (a separator), and the
    # upper/lower puncta -- genuine secondaries/separators, not structural accents.
    # (tsinnorit and bare shalshelet, formerly swallowed here, are now emitted above
    # as metsunnar / shalshelet qetannah.)
    (re.compile("[" + am.METEG + am.PASEQ + am.UPPER_DOT + am.LOWER_DOT + "]"), None),
    # Fail-fast guard: any *accent* (U+0591..U+05AE) no rule above consumed is a stray
    # mark.  Emit STRAY_ACCENT (which the grammar cannot parse -> NO_PARSE) rather than
    # let the catch-all swallow it silently.  Placed above the catch-all so a 1-char
    # accent match beats the equally-long `.`; the catch-all keeps swallowing the
    # structural junk (``LETTER`` placeholders, spaces, maqaf, `]N` note markers).  Zero live
    # customers today -- the only attested catch-all accent (the ps124:4 geresh) is
    # consumed by the same-letter revia mugrash charity above.
    (re.compile("[֑-֮]"), pan.STRAY_ACCENT),
    (re.compile(r"\*\*"), None),
    (re.compile(r"\*[^* \r\n\-]+"), None),
    (re.compile(r".", re.DOTALL), None),
]

# Display leaf names (lowercase, shown in printed trees), keyed by token type.
_LEAF: dict[str, str] = {
    pan.SOFPASUQ: "sof pasuq",
    pan.SILLUQ: "silluq",
    pan.ATNAX: "atnax",
    pan.OLEH_WEYORED: "oleh we-yored",
    pan.REVIA_MUGRASH: "revia mugrash",
    pan.REVIA_GADOL: "revia gadol",
    pan.REVIA_QATAN: "revia qatan",
    pan.DEXI: "dexi",
    pan.TSINNOR: "tsinnor",
    pan.PAZER: "pazer",
    pan.LEGARMEH: "legarmeh",
    pan.SHALSHELET_GEDOLAH: "shalshelet gedolah",
    pan.SHALSHELET_QETANNAH: "shalshelet qetannah",
    pan.MAHAPAKH_METSUNNAR: "mahapakh metsunnar",
    pan.MERKHA_METSUNNAR: "merkha metsunnar",
    # NB: the impositive-pair bang (e.g. merkha!azla) has no static entry here -- its
    # `!`-joined leaf is computed per pair by _impositive_pair_token and supplied directly
    # in scan_accents.  `!` (not a space) marks two distinct accents on one letter with no
    # natural order, as the prose mahapakh!azla / mahapakh!tipexa (see prose_scanner._LEAF).
    pan.STRAY_ACCENT: "stray accent",
    pan.MUNAX: "munax",
    pan.MERKHA: "merkha",
    pan.MAHAPAKH: "mahapakh",
    pan.AZLA: "azla",
    pan.ILLUY: "illuy",
    pan.TARXA: "tarxa",
    pan.GALGAL: "galgal",
}


@dataclass(frozen=True)
class Token:
    """One poetic grammar token and its starting offset in the scanned mark body."""

    type: str
    leaf: str
    start: int


def _recover_unmarked_oleh(types: list[str]) -> list[str]:
    """Recover an oleh-we-yored whose ole sign L leaves unmarked (ITM #363).

    In the Leningrad codex the ole (the upper sign of oleh-we-yored) is sometimes
    omitted, leaving only the yored -- a merkha -- written below the stress;
    MAM-simple always supplies the ole, and the user confirms L/LC drops it.  Read
    literally the lone merkha looks like a conjunctive servus, so the scanner misses
    the divider (the verse then fails to parse).

    The reliable, MAM-cross-checked signal is the oleh-we-yored's own servus: the
    galgal (yerax-ben-yomo, the "v"-shaped sign) standing immediately before
    it.  A GALGAL directly followed by a bare MERKHA is that servus + an unmarked
    yored, so the MERKHA is reclassified to OLEH_WEYORED.  Validated against the MAM
    disjunctive oracle (accgram.poetic_xcheck): this recovers 9 Psalms/Job verses
    and introduces no new disagreements across the corpus.

    The other unmarked-ole context #363 notes -- a *revia* preceding the yored --
    is deliberately NOT recovered here: a revia followed by a merkha servus is an
    extremely common ordinary sequence, so that signal is unusable without
    word-level information (it breaks ~1400 verses against the oracle).  Those few
    verses remain flagged divergences for a later, narrower pass.
    """
    out = list(types)
    for i in range(1, len(out)):
        if out[i] == pan.MERKHA and out[i - 1] == pan.GALGAL:
            out[i] = pan.OLEH_WEYORED
    return out


def _reclassify_revia(types: list[str]) -> list[str]:
    """Resolve each generic REVIA (no geresh muqdam) to its role.

    The three revias share signs: revia mugrash carries a geresh muqdam (handled in
    the rule table); revia gadol and revia qatan are a bare dot, and a
    *bare* revia before silluq is revia mugrash "without the geresh" (Yeivin
    #367).  Disambiguation is by the next disjunctive in the stream:

      - next is OLEH_WEYORED  -> revia qatan (it stands only there, #368);
      - next is SILLUQ        -> revia mugrash without geresh (the last
        disjunctive before silluq; when two revias precede silluq the first is
        gadol and the second mugrash, #391 -- handled automatically since the
        first revia's next disjunctive is the second revia, not silluq);
      - otherwise (next is atnax, oleh, or another revia) -> revia gadol.
    """
    out = list(types)
    for i, t in enumerate(out):
        if t != pan.REVIA:
            continue
        nxt = next(
            (out[j] for j in range(i + 1, len(out)) if out[j] in _POETIC_DISJUNCTIVES),
            None,
        )
        if nxt == pan.OLEH_WEYORED:
            out[i] = pan.REVIA_QATAN
        elif nxt == pan.SILLUQ:
            out[i] = pan.REVIA_MUGRASH
        else:
            out[i] = pan.REVIA_GADOL
    return out


def scan_accent_tokens(body: str) -> list[Token]:
    """Scan one poetic verse body into positioned grammar tokens.

    The positions make the grammar's accent tokens attributable to their chanted words.
    ``scan_accents`` remains the pair-returning interface for the grammar callers.
    """
    raw_tokens: list[Token] = []
    # Leaves for the impositive-pair bang tokens, whose type/leaf are computed per pair
    # (not in the static _LEAF map); keyed by index in raw_types.  The reclassify passes
    # below preserve length and index order, so these stay aligned.
    pos = 0
    n = len(body)
    while pos < n:
        best_len = 0
        best_type: str | None = None
        matched = False
        for regex, ttype in _POETIC_GG_RULES:
            m = regex.match(body, pos)
            if m is None:
                continue
            length = m.end() - m.start()
            if length > best_len:
                best_len = length
                best_type = ttype
                matched = True
        assert matched, f"no rule matched at position {pos} in {body!r}"
        if best_type is not None:
            if best_type == pan.BANG_PAIR:
                bang_type, bang_leaf = _bang_pair_token(body[pos : pos + best_len])
                raw_tokens.append(Token(bang_type, bang_leaf, pos))
            else:
                raw_tokens.append(Token(best_type, _LEAF.get(best_type, ""), pos))
                if best_type == "SOFPASUQ":
                    break
        pos += max(best_len, 1)

    resolved = _reclassify_revia(_recover_unmarked_oleh([t.type for t in raw_tokens]))
    return [
        Token(
            token_type,
            token.leaf if token_type == token.type else _LEAF[token_type],
            token.start,
        )
        for token, token_type in zip(raw_tokens, resolved, strict=True)
    ]


def scan_accents(body: str) -> list[tuple[str, str]]:
    """Scan one poetic verse body into the grammar's ``(type, leaf)`` pairs."""
    return [(token.type, token.leaf) for token in scan_accent_tokens(body)]


@dataclass(frozen=True)
class Verse:
    reference: str
    tokens: list[tuple[str, str]]  # ('TILDE',''), accents..., ('SOFPASUQ',...)
    body: str


def scan_verse(reference: str, body: str) -> Verse:
    """Scan one verse body into a grammar-ready token stream."""
    tokens: list[tuple[str, str]] = [("TILDE", "")]
    tokens += scan_accents(body)
    return Verse(reference=reference, tokens=tokens, body=body)


def scan_book(text: str, bb: str) -> list[Verse]:
    """Scan a whole book text into per-verse poetic token streams.

    Mirrors accgram.prose_scanner.scan_book's line walk -- each ``ch:vr <accents>``
    line becomes one Verse via scan_verse.  The reference's book label comes from
    the WLC code's bk39id ("Psalms", "Proverbs", "Job"), since the poetic output
    has no C oracle to match.
    """
    book = wlc_bb_to_bk39id(bb)
    verses: list[Verse] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r\n")
        mv = _VERSE_RE.match(line)
        if mv is not None:
            ch, vs, rest = mv.group(1), mv.group(2), mv.group(3)
            verses.append(scan_verse(f"{book} {ch}:{vs}", rest))
    return verses
