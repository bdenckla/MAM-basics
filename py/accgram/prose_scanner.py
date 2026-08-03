r"""Hand-written scanner: reproduces the GG-state token stream of tnk2acc.l.

Stage 1 / Phase D (full scanner including the four trailing-context rules).
Handles the new-format verse structure (bookname -> chapter -> verse -> accent
scan) and the complete GG-state accent table, including the four lex
*trailing-context* rules that a generated lexer cannot express.  Phase 2 of issue wlc-utils#9
retired the Michigan-Claremont 2-digit-code alphabet: the rule table now matches
directly over the Unicode mark alphabet (`accent_marks`), and the trailing-context
digit classes are rebuilt onto it by `am.negated_class`.  The original M-C-code
shapes are shown below for reference (each code is now its own mark):

  - silluq    35|75|95/[^ 379...]*00        (a true silluq is a metheg/silluq
              immediately before sof pasuq)
  - mayela    73/<allowed>*(00|92)          (tipexa variant before atnax/silluq)
  - legarmeh  74{TEXT}05/[^12368]*...81      (munax+paseq before revia)
  - chapter   ^[1-9][0-9]*:/[1-9]            (new-format verse lookahead; handled
              by the line-oriented _VERSE_RE below)

plus the stateful `has_legarmeh` special case (17-passage list + 1Sam 14:47
"second occurrence only" counter), ported verbatim from tnk2acc.l.

Faithfulness notes (flex semantics reproduced):
  - longest match wins; ties are broken by rule order (the order of _GG_RULES
    below mirrors the order of the rules in tnk2acc.l's GG block);
  - lex trailing context (`r/s`) is expressed as a regex lookahead `(?=s)`, so
    only `r` is consumed, exactly as flex consumes only the left part;
  - flex's `{TEXT}` (= `[^ \r\n\-]*`) is greedy and stays within one
    maqqef/space-delimited atom; Python `re` greediness reproduces the longest
    match (backtracking to the rightmost terminator).

Divergence from the goerwitz C oracle (metigah-zaqef): the C lexer's methiga-zaqef body class
`[^01234680]*` excludes no literal space, so its qadma...zaqef span runs across a space as
readily as across a maqaf.  `_METHIGA_MID` adds the space, stopping the fuse at a chanted-word
boundary while it still crosses a maqaf.  ITM §223 and CoS Ch. 5 §§4-6 both restrict the metigah
to the chanted word of the zaqef, so a qadma one chanted word earlier is not a metigah under either
book; see the comment at `_METHIGA_MID` for the citations and for the 1k19:11 control.  The
divergence moves five WLC verses and three UXLC verses out of METHIGAZAQEF and leaves MAM
untouched -- the counts live in `chanted_word_accents`' survey, not here.

Divergence from the goerwitz C oracle (`has_legarmeh`): the C `passages[]` list
keys on book *abbreviations* ("Gen 28:9", "Lev 10:6", "Dan 3:2"), but in the new
format the C lexer's `location` carries the **full** bookname header ("Genesis",
"Levit", "Daniel"), so the two coincide only for "Ruth" -- the C binary silently
mis-fired and legarmeh fired for Ruth 1:2 alone.  That was a latent upstream
defect driven by bad input data, not the author's intent (the tnk2acc.l comment
says all 17 munax+paseq-not-before-revia passages are legarmeh).  We therefore
key the 17 passages on **structured book refs** -- `(wlc_bb, chnu, vrnu)` tuples
threaded from the caller -- so detection is decoupled from header spelling and
all 17 passages fire as intended.  See doc/PLAN-fix-has-legarmeh-booknames.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from accgram import accent_marks as am
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id


@dataclass(frozen=True)
class Token:
    """A grammar token: parser token type plus the leaf-name string (yylval.leaf).

    ``start`` is where the token's marks begin in the body ``scan_accents`` read, which is what
    lets a caller attribute a token to a chanted word: the grammar consumes accent types alone
    and can see no boundary at all (``chanted_word_accents``).  It is deliberately outside
    ``__eq__``, ``__hash__`` and ``__repr__``, so two tokens of the same type and leaf stay equal
    and interchangeable wherever this repo already treats them so; nothing but the position layer
    should ever read it.  The default is ``-1`` for the tokens built positionally by callers
    (``Token("TILDE", "")``), which stand outside the body.
    """

    type: str
    leaf: str
    start: int = field(default=-1, compare=False, repr=False)


# --- verse-structure line patterns (new format), from tnk2acc.l ----------------
# A verse line: chapter ':' verse ' ' accent-codes.  The flex lexer splits this
# across the EE (chapter, returns TILDE) and FF (verse number) start states; in
# the line-oriented new format we can recover chapter/verse directly.  Note the
# chapter rule's trailing context `:/[1-9]` requires a digit after the colon,
# which the explicit `:([1-9][0-9]*)` below reproduces.
_VERSE_RE = re.compile(r"^([1-9][0-9]*):([1-9][0-9]*)[ \t](.*)$")


# --- GG-state accent rules -----------------------------------------------------
# Each entry: (compiled regex anchored at the scan position, token type or None).
# token type None == "swallow" (consume, emit nothing).  The sentinel
# "_LEGARMEH_OR_MUNAX" is resolved at emit time via has_legarmeh(location).
# Trailing context is a lookahead so it is not consumed.  Phase 2 (issue wlc-utils#9) matches
# over the Unicode mark alphabet (accent_marks); the four trailing-context digit
# classes are rebuilt onto it by `am.negated_class` (see that function).  TEXT keeps
# a match within one maqaf/space-delimited atom.
_TEXT = am.TEXT

# silluq right context:  35|75|95 / [^ 379\r\n\-?~]* 00
_SILLUQ_LA = r"(?=" + am.negated_class(" \r\n-?~", "379") + r"*" + am.SOF_PASUQ + r")"
# mayela right context:  73 / (([^ 0123468\r\n\-]|\-[^ 0123468]*)*(\][0-9])?)* (00|92)
_MAYELA_LA = (
    r"(?=(?:(?:"
    + am.negated_class(" \r\n-", "0123468")
    + r"|-"
    + am.negated_class(" ", "0123468")
    + r"*)*(?:\][0-9])?)*(?:"
    + am.SOF_PASUQ
    + r"|"
    + am.ATNAX
    + r"))"
)
# legarmeh right context:  74{TEXT}05 / [^12368]*(\][0-9])?[^12368]* 81
_LEGARMEH_LA = (
    r"(?="
    + am.negated_class("", "12368")
    + r"*(?:\][0-9])?"
    + am.negated_class("", "12368")
    + r"*"
    + am.REVIA
    + r")"
)
# methiga-zaqef body:  63 [^01234680]* 80, plus a space added to the excluded literals.
# The span CROSSES A MAQAF, deliberately: ITM §223's leading example is Ex 35:9 ואבני־שהם, a
# maqaf compound with the metigah on the non-final atom, and CoS Ch. 5 §5 allows the metigah at
# the start of the word "provided there is there a hyphenated tiny word" -- so a metigah-zaqef
# written across a maqaf is one token, as it is one chanted word.
# It STOPS AT A SPACE, which is the divergence from tnk2acc.l recorded in the module docstring.
# Both books restrict the metigah to the chanted word of the zaqef: ITM §223 has "the
# word bearing zaqef", and CoS Ch. 5 §4 "A methiga will appear in the word of the small zakef",
# restated at Ch. 5 §6.  Two atoms with a space between them are two chanted words, so a qadma
# before the space cannot be the zaqef's metigah, whatever it is instead.
# The control is WLC's 1k19:11, where a ``]1`` note marker between הרוח and רעש already blocks the
# fuse and the grammar already reports the zaqef phrase an error -- while 1k19:12's parallel
# mahapakh-pashta-zaqef parses clean.  Before the space went in, the same configuration was clean
# at gn18:18 and an error at 1k19:11, on nothing but an unrelated note marker.
_METHIGA_MID = am.negated_class(" ", "0123468")
# qadma-before-geresh lookahead: U+05A8 is named AZLA when a geresh is the *next
# accent token* (cross-letter), QADMA otherwise.  Like METHIGAZAQEF, the span is the
# cross-letter run between the two -- NOT a literal ``LETTER`` separator -- so a
# (non-occurring, non-whitelisted) same-letter qadma+geresh adjacency can't accidentally
# depend on letter-adjacency.  But unlike METHIGAZAQEF (which never crosses a paseq), an
# azla-geresh pair can be separated by scanner-*swallowed* marks (paseq, meteg, tsinnorit,
# puncta) and even a word boundary -- e.g. 1Chr 12:19's ``qadma LETTER LETTER paseq SPACE
# LETTER LETTER geresh``, where the swallowed paseq leaves AZLA and GERESH token-adjacent.  So
# the intervening class is "anything that is not itself a tokenizing accent": it permits the
# swallowed marks and the structural filler (the ``LETTER`` placeholder, maqaf, space, ``]N``
# note, ``*`` ketiv) but stops at any accent -- the geresh that follows, or any other accent
# that would mean geresh is NOT the next token.
# geresh-muqdam edge cases (lv1:3, 2k17:13) normalize to plain geresh and never co-occur with
# a preceding qadma.
# The marks the scanner swallows between two accent tokens (see the swallow rule near the
# end of _GG_RULES): meteg/silluq, paseq, tsinnorit, and the upper/lower puncta.
_SWALLOWED_MARKS = am.METEG + am.PASEQ + am.TSINNORIT + am.UPPER_DOT + am.LOWER_DOT
# Everything that is NOT a tokenizing accent: the swallowed marks plus structural filler.
# Built as the negation of the accent codepoints (every _MARK_DIGITS key that is not a
# swallowed mark -- this still blocks at sof pasuq and at any other accent), so the run
# halts at the geresh (or any accent) ahead.
_GERESH_MID = (
    "[^"
    + "".join(
        am._escape_in_class(mark)
        for mark in am._MARK_DIGITS
        if mark not in _SWALLOWED_MARKS
    )
    + "]"
)
_GERESH_LA = r"(?=" + _GERESH_MID + r"*" + am.GERESH + r")"

_GG_RULES: list[tuple[re.Pattern[str], str | None]] = [
    (re.compile(am.SOF_PASUQ), "SOFPASUQ"),
    # silluq: meteg/silluq immediately before sof pasuq, excluding mayela etc.
    (re.compile(am.METEG + _SILLUQ_LA), "SILLUQ"),
    (re.compile(am.ATNAX), "ATNAX"),
    (re.compile(r"(?:" + am.SEGOLTA + _TEXT + r")?" + am.SEGOLTA), "SEGOLTA"),
    (re.compile(am.SHALSHELET + _TEXT + am.PASEQ), "SHALSHELET"),
    (re.compile(am.QADMA + _METHIGA_MID + r"*" + am.ZAQEF_QATAN), "METHIGAZAQEF"),
    (re.compile(am.ZAQEF_QATAN), "ZAQEF"),
    (re.compile(am.ZAQEF_GADOL), "ZAQEFGADOL"),
    (re.compile(am.REVIA), "REVIA"),
    # mayela (trailing context): tipexa before sof-pasuq/atnax, only meteg intervening.
    (re.compile(am.TIPEXA + _MAYELA_LA), "MAYELA"),
    (re.compile(am.TIPEXA), "TIPEXA"),
    # zarqa: optional tsinnorit stress-helper fused onto the tsinnor (one token).
    (re.compile(r"(?:" + am.TSINNORIT + _TEXT + r")?" + am.TSINNOR), "ZARQA"),
    # pashta: a stress-helper pashta fused onto the main pashta (one token).
    (re.compile(r"(?:" + am.PASHTA + _TEXT + r")?" + am.PASHTA), "PASHTA"),
    (re.compile(am.YETIV), "YETIV"),
    (re.compile(am.TEVIR), "TEVIR"),
    (re.compile(am.GERESH), "GERESH"),
    # geresh muqdam (U+059D) is a poetic-only sign (the preposed geresh of revia
    # mugrash).  In WLC it appears in the 21 prose books only twice -- a property
    # (arguably a bug) of WLC, not a statement about the wider Masoretic tradition --
    # both a typographic device for what is abstractly a plain geresh, normalized to one
    # here: Lev 1:3 (alone); and 2 Kings 17:13 (sharing a word, and a base letter, with a
    # telisha gedola), where the resulting telg + geresh same-letter pair is whitelisted by
    # lexical_validation and parses as a two-token geresh-then-telg sequence (the manuscript
    # order the scanner now preserves).  (The poetic scanner keeps its own revia mugrash
    # handling.)
    # See the tanach.us changes
    # Lev 1:3:       https://tanach.us/Changes/2020.10.19%20-%20Changes/2020.10.19%20-%20Changes.xml?2020.09.22-1
    # 2 Kings 17:13: https://tanach.us/Changes/2020.10.19%20-%20Changes/2020.10.19%20-%20Changes.xml?2020.09.22-2
    (re.compile(am.GERESH_MUQDAM), "GERESH"),
    (re.compile(am.GERSHAYIM), "GERSHAYIM"),
    (re.compile(am.PAZER), "PAZER"),
    (re.compile(am.QARNEY_PARA), "PAZERGADOL"),
    (re.compile(am.TELISHA_GEDOLA), "TELISHAGEDOLA"),
    # legarmeh (trailing context): munax+paseq before a subsequent revia.
    (re.compile(am.MUNAX + _TEXT + am.PASEQ + _LEGARMEH_LA), "LEGARMEH"),
    # munax+paseq NOT before revia: legarmeh only inside a has_legarmeh passage.
    (re.compile(am.MUNAX + _TEXT + am.PASEQ), "_LEGARMEH_OR_MUNAX"),
    (re.compile(am.MUNAX), "MUNAX"),
    # mahapakh + qadma on one base letter (adjacent in the mark string, no ``LETTER``
    # between -> same letter): an impositive above-accent and below-accent share a
    # letter, so the pair has no right-to-left (graphical) order -- one sits above the
    # letter and one below -- even though it has a chanting order (qadma before mahapakh;
    # cf. the ek20:31 MAM note).  Fused into one unitary token rather than judged as a
    # servus *sequence*; the genuine cross-letter `qadma...mahapakhh` chain still tokenizes
    # as QADMA then MAHAPAKH.  Stored mahapakh-then-qadma (U+05A4 < U+05A8).  Outside the
    # (ungrammar-checked) decalogues this occurs only at Ezekiel 20:31; the qadma is not
    # before a geresh, so it stays qadma (not azla).
    (re.compile(am.MAHAPAKH + am.QADMA), "MAHAPAKHQADMA"),
    (re.compile(am.MAHAPAKH), "MAHAPAKH"),
    (re.compile(am.MERKHA), "MERKHA"),
    (re.compile(am.MERKHA_KEFULA), "MERKHAKEFULA"),
    (re.compile(am.DARGA), "DARGA"),
    # U+05A8: AZLA before a (cross-letter, within-word) geresh -- the azla-geresh
    # pairing -- else QADMA (the standalone prose name).  Both rules match the single
    # U+05A8 mark (the lookahead consumes nothing), so rule order breaks the tie:
    # the geresh-context AZLA rule is listed first.
    (re.compile(am.QADMA + _GERESH_LA), "AZLA"),
    (re.compile(am.QADMA), "QADMA"),
    # telisha qetanna: a stress-helper telisha fused onto the main (one token).
    (re.compile(am.TELISHA_QETANA + _TEXT + am.TELISHA_QETANA), "TELISHAQETANNA"),
    (re.compile(am.TELISHA_QETANA), "TELISHAQETANNA"),
    (re.compile(am.YERAX), "GALGAL"),
    # leftover medial meteg/paseq/tsinnorit/puncta -> swallowed
    (
        re.compile(
            "[" + am.METEG + am.PASEQ + am.TSINNORIT + am.UPPER_DOT + am.LOWER_DOT + "]"
        ),
        None,
    ),
    # "**" and "*<non-space>+" -> swallowed
    (re.compile(r"\*\*"), None),
    (re.compile(r"\*[^* \r\n\-]+"), None),
    # catch-all: any other single char (``LETTER`` placeholder, maqaf, space, ]N digit)
    # -> swallowed
    (re.compile(r".", re.DOTALL), None),
]

# leaf-name (yylval.leaf) for each token type, from tnk2acc.l.
_LEAF: dict[str, str] = {
    "SOFPASUQ": "sof pasuq",
    # Synthetic terminator for a verse missing its sof pasuq (never printed: the
    # grammar production discards it and emits a distinct sof_pasuq_phrase ERROR).
    "MISSING_SOFPASUQ": "",
    "SILLUQ": "silluq",
    "ATNAX": "atnax",
    "SEGOLTA": "segolta",
    "SHALSHELET": "shalshelet",
    "METHIGAZAQEF": "methiga-zaqef",
    "ZAQEF": "zaqef",
    "ZAQEFGADOL": "zaqefgadol",
    "REVIA": "revia",
    "MAYELA": "mayela",
    "TIPEXA": "tipexa",
    "ZARQA": "zarqa",
    "PASHTA": "pashta",
    "YETIV": "yetiv",
    "TEVIR": "tevir",
    "GERESH": "geresh",
    "GERSHAYIM": "gershayim",
    "PAZER": "pazer",
    "PAZERGADOL": "pazergadol",
    "TELISHAGEDOLA": "telishagedola",
    "LEGARMEH": "legarmeh",
    "MUNAX": "munax",
    "MAHAPAKH": "mahapakh",
    # ``!`` (not ``_``) joins the fused cluster: these are two distinct accents under
    # duress on one letter, not one accent with a space in its name -- and the cluster
    # is extraordinary, sometimes even illegal (cf. the mahapakh!tipexa of Lev 25:20).
    "MAHAPAKHQADMA": "mahapakh!qadma",
    "MERKHA": "merkha",
    "MERKHAKEFULA": "merkhakefula",
    "DARGA": "darga",
    "QADMA": "qadma",
    "AZLA": "azla",
    "TELISHAQETANNA": "telishaqetanna",
    "GALGAL": "galgal",
}


class HasLegarmeh:
    """Port of tnk2acc.l::has_legarmeh (the 17-passage list + 1Sam 14:47 rule).

    Keyed on structured `(wlc_bb, chnu, vrnu)` book refs rather than the C list's
    abbreviated location strings, so all 17 passages fire regardless of how the
    chapter-head bookname is spelled (see the module docstring / the PLAN).  The
    wlc_bb codes are `wlc_cmn.wlc_book_codes`' 2-char codes; the book order matches
    the C list (which is "Jewish order").

    Stateful: `count` tracks munax+paseq occurrences at 1Sam 14:47 (only the
    second is legarmeh), and `old_i` advances monotonically through the list
    (the C comment: "this old_i stuff assumes the books are in Jewish order").
    One instance per book file reproduces the C `static` per-process reset.
    """

    _PASSAGES = (
        ("gn", 28, 9),
        ("lv", 10, 6),
        ("lv", 21, 10),
        ("1s", 14, 3),
        ("1s", 14, 47),
        ("2s", 13, 32),
        ("2k", 18, 17),
        ("is", 36, 2),
        ("je", 4, 19),
        ("je", 38, 11),
        ("je", 40, 11),
        ("ek", 9, 2),
        ("hg", 2, 12),
        ("ru", 1, 2),
        ("da", 3, 2),
        ("ne", 8, 7),
        ("2c", 26, 15),
    )

    def __init__(self) -> None:
        self._count = 0
        self._old_i = 0

    def __call__(self, bb: str, chnu: int, vrnu: int) -> bool:
        # Mirrors the C short-circuit `(i != 4) || (++count == 2)`: count is
        # bumped only when we land on 1Sam 14:47 (index 4).
        ref = (bb, chnu, vrnu)
        for i in range(self._old_i, len(self._PASSAGES)):
            if ref == self._PASSAGES[i]:
                if i != 4 or self._bump_is_second():
                    self._old_i = i
                    return True
        return False

    def _bump_is_second(self) -> bool:
        self._count += 1
        return self._count == 2


def scan_accents(
    body: str, bb: str, chnu: int, vrnu: int, has_legarmeh: HasLegarmeh
) -> list[Token]:
    """Scan the GG-state accent codes of one verse body into a token list.

    Emits accent tokens followed by a terminating SOFPASUQ.  Mirrors flex:
    at each position pick the longest match; break ties by rule order.  Stops
    after the first 00 (sof pasuq), which in flex returns to the EE state.

    The structured book ref `(bb, chnu, vrnu)` and `has_legarmeh` resolve the
    74{TEXT}05-not-before-revia rule to LEGARMEH or MUNAX.
    """
    tokens: list[Token] = []
    pos = 0
    n = len(body)
    saw_sofpasuq = False
    # Insertion index for recovering a *verse-final* silluq when the verse turns
    # out to be missing its sof pasuq (see the post-loop block below).  Set when a
    # meteg/silluq code (35|75|95) is swallowed; reset whenever any later accent is
    # emitted, so only a trailing (verse-final) silluq survives.
    pending_silluq: tuple[int, int] | None = None
    while pos < n:
        best_len = 0
        best_type: str | None = None
        best_is_rule = False
        for regex, ttype in _GG_RULES:
            m = regex.match(body, pos)
            if m is None:
                continue
            length = m.end() - m.start()
            if length > best_len:
                best_len = length
                best_type = ttype
                best_is_rule = True
        # The catch-all `.` guarantees best_is_rule is always True for pos < n.
        assert best_is_rule, f"no rule matched at position {pos} in {body!r}"
        advance = max(best_len, 1)
        if best_type == "_LEGARMEH_OR_MUNAX":
            best_type = "LEGARMEH" if has_legarmeh(bb, chnu, vrnu) else "MUNAX"
        if best_type is not None:
            tokens.append(Token(best_type, _LEAF[best_type], pos))
            pending_silluq = None
            if best_type == "SOFPASUQ":
                saw_sofpasuq = True
                break
        elif body[pos] == am.METEG:
            # A swallowed meteg/silluq mark; remember where its SILLUQ token would
            # go if it proves to be the verse-final silluq of a sof-pasuq-less verse,
            # and where in the body that mark stands.
            pending_silluq = (len(tokens), pos)
        pos += advance

    # Extension beyond tnk2acc.l: tolerate a verse missing its sof pasuq (Unicode
    # SOF PASUQ / code 00).  Such a verse loses *both* end-of-verse markers -- with
    # no 00, the trailing silluq's SILLUQ rule (which requires a following 00) does
    # not fire either, so the stream ends with nothing for the grammar to reduce.
    # Recover the verse-final silluq as a real SILLUQ (so the anomaly is attributed
    # to the sof pasuq, not misread as a missing silluq) and append a distinct
    # MISSING_SOFPASUQ terminator that the grammar flags as a sof_pasuq ERROR.
    if not saw_sofpasuq:
        if pending_silluq is not None:
            at, mark_pos = pending_silluq
            tokens.insert(at, Token("SILLUQ", _LEAF["SILLUQ"], mark_pos))
        tokens.append(Token("MISSING_SOFPASUQ", _LEAF["MISSING_SOFPASUQ"], n))
    return tokens


@dataclass(frozen=True)
class Verse:
    reference: str
    tokens: list[Token]  # TILDE, accent tokens..., SOFPASUQ
    body: str  # the raw accent-code body (after "ch:vs "), for lexical validation


def scan_book(text: str, bb: str) -> list[Verse]:
    """Scan a whole new-format book file into per-verse token streams.

    Each verse is delimited by TILDE (emitted by the chapter rule at the head of
    every verse line) and SOFPASUQ (the 00 accent code).  A single HasLegarmeh
    instance is held for the whole book, reproducing the C `static` state that
    resets per process (the harness runs one process per book file).

    `bb` is the `wlc_cmn.wlc_book_codes` 2-char code for this book; it (with the
    parsed chapter/verse numbers) is what `has_legarmeh` keys on, and its
    `bk39id` ("Genesis", "Job", ...) spells the human-readable `Verse.reference`.
    """
    book = wlc_bb_to_bk39id(bb)
    has_legarmeh = HasLegarmeh()
    verses: list[Verse] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r\n")
        mv = _VERSE_RE.match(line)
        if mv is not None:
            ch, vs, rest = mv.group(1), mv.group(2), mv.group(3)
            reference = f"{book} {ch}:{vs}"
            tokens = [Token("TILDE", "")] + scan_accents(
                rest, bb, int(ch), int(vs), has_legarmeh
            )
            verses.append(Verse(reference=reference, tokens=tokens, body=rest))
    return verses
