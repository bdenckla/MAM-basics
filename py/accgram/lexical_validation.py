"""Prose lexical validation: flag unpaired stress-helper accents (alphabet errors).

This is a *prose-only* layer that sits on top of the faithful C-port scanner/
grammar (prose_scanner / prose_ply_grammar) and intentionally **diverges from the
goerwitz C oracle**, in the same documented spirit as the MISSING_SOFPASUQ and
tevir/tipexa recoveries: where the C lexer silently swallows a malformed accent,
we surface it as an ungrammatical verse.

The one helper handled today is accent ``82``.  In the prose accent system, ``82``
is well-formed *only* as the left half of a ``82{TEXT}02`` pair fused onto a single
maqaf/space-delimited atom, where the scanner reads it as one ZARQA token
(prose_scanner ``(?:82{TEXT}02)?02``; TEXT = ``[^ \\r\\n-]*`` keeps the pair inside
one atom).  When there is no ``02`` later in the same atom, the C lexer's
``35|75|95|44|05|82|52 -> None`` rule swallows the ``82`` and the intended accent
simply vanishes -- so whether the verse becomes an ungrammatical verse is left to downstream
parse luck.  All 12 such prose verses (a stray zarqa mis-encoded before a lamed
ascender) are equally wrong; this layer flags them uniformly.

A second, sibling check (``illegal_same_letter_pairs``) flags an impossible
*same-letter* configuration rather than an unpaired helper: two accents stacked on one
base letter.  This is a WHITELIST guard, the prose analogue of the poetic
``poetic_scanner`` bang guard (Plan D / Plan E): two masoretically-blessed clusters
may legitimately share a letter -- the MAM-confirmed ek20:31 ``mahapakh!qadma`` (fused to
one token, grammar-accepted) and the telisha gedola + geresh-family pair (gn5:29, zp2:15,
2k17:13), spared as a two-token *sequence* (the telg and the geresh, in manuscript order --
gerstar-then-telg for these same-letter words) -- so ANY other two adjacent
accents (no base-letter ``LETTER`` between -> same letter) is an alphabet error.  The sole
attested illicit pair is mahapakh + tipexa (lv25:20); two accents stacked on one letter
make the fault intrinsic to the letter -- an alphabet error, not an illegal grammatical
sequence (which the grammar would otherwise flag as ``tipexa_phrase -> ERROR``, the
wrong rationale).  The general guard supersedes the earlier mahapakh+tipexa-only check
(output-neutral today, but future-proof; cf. memory parse-rate-not-a-goal).

Prose-only is intentional and burns no bridge: a bare ``82`` is *valid* in the
poetic accent system (tsinnorit, >200 uses), but the genre split already happens
upstream (accgram.prose_filter strips Psalms/Proverbs/poetic-Job before scanning),
so within this prose pipeline a bare ``82`` is unconditionally illegal.  A future
poetic checker is expected to have its own lexer where ``82`` is a first-class
token; this module therefore hard-codes prose semantics with no genre parameter.

A third check (``nonfinal_telisha_qetannas``) flags the lone medial telisha qetanna
(M-C ``24``) of je 44:17.  In M-C this is an unpaired stress-helper exactly like ``82``:
a ``24`` (medial telisha qetanna, written on a non-final letter) is well-formed only
as the helper of a following ``04`` (the real, postpositive telisha qetanna), the pair
``24{TEXT}04`` -- which the scanner fuses into one TELISHAQETANNA token.  But the
grammar checker reads the *Unicode-converted* source, where M-C ``24`` and ``04`` are
the **same** codepoint (telisha qetanna, U+05A9): the helper/main code distinction has
been erased, so the only checker-visible defect is *placement* -- a telisha qetanna
sitting on a non-final letter (here the kaf of כִּי) rather than on the word-final
letter (the yod).  This is therefore phrased as a word-internal placement rule: a
telisha qetanna on a non-final letter, with no following telisha qetanna to absorb it
as a stress-helper, is illegal.  (It is one instance of a broader, not-yet-implemented
family of word-level rules -- every postpositive accent must fall on the final letter,
every prepositive on the first.)

The module is self-contained: it reads the per-atom Unicode mark stream straight from
the verse body (the scanner-ready marks ``uni_to_marks`` produces), with no dependency
on the scanner internals.  It is kept general enough that other unpaired stress-helpers
could be added later; today ``82`` and the lone ``24`` are wired up (the remaining
siblings -- standalone ``44`` and the codes ``11``/``12`` -- were judged moot after the
Phase-2 Unicode port; see the tracking GitHub issue).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from accgram import accent_marks as am

# Atoms are delimited by spaces and maqaf (``-``), mirroring the scanner's TEXT
# class ``[^ \r\n\-]*`` which keeps a fused helper...zarqa pair inside one atom.
_ATOM_SPLIT_RE = re.compile(r"[ \t\r\n\-]+")

# stress-helper mark -> (fusion-partner mark, M-C code label) where the partner must
# follow the helper later in the same atom for the helper to be well-formed.  Only the
# zarqa's stress helper (U+0598, M-C 82) -- whose partner is the zarqa itself (U+05AE,
# M-C 02) -- is active today.  These verses are prose, so U+0598 and U+05AE can only be the
# zarqa's helper and the zarqa; the ``am`` constants spell them TSINNORIT and TSINNOR after
# the separate poetic accents that share the two codepoints (wlc-utils#85).  The label is the original M-C code, kept so the
# ``illegal_mark`` report reads identically to the pre-Phase-2 output.
_STRESS_HELPER_PARTNER: dict[str, tuple[str, str]] = {am.TSINNORIT: (am.TSINNOR, "82")}

# Accents occupy U+0591..U+05AE; meteg/silluq (U+05BD), paseq, sof pasuq
# and the puncta are NOT accents and so never count toward a same-letter accent pair.
_ACCENT_LO = "\N{HEBREW ACCENT ETNAHTA}"  # U+0591
_ACCENT_HI = "\N{HEBREW ACCENT ZINOR}"  # U+05AE


def _is_accent(ch: str) -> bool:
    return _ACCENT_LO <= ch <= _ACCENT_HI


# Same-letter accent pairs are a WHITELIST, not a blacklist -- the prose analogue of the
# poetic ``poetic_scanner._WHITELISTED_ADJACENT_PAIRS`` (Plan D / Plan E).  Two
# masoretically-blessed configurations may legitimately share one base letter:
#
#   * mahapakh (U+05A4) + qadma (U+05A8) -- the MAM-confirmed ek20:31 ``נִטְמְאִ֤֨ים`` (both
#     witnesses keep both marks), which the scanner fuses into one ``mahapakh!qadma`` token
#     and the grammar accepts (a fused-legal-token entry); and
#   * telisha gedola (U+05A0) + a geresh-family mark -- gershayim (U+059E; gn5:29, zp2:15)
#     or a prose geresh muqdam (U+059D; 2k17:13, which the scanner normalizes to a plain
#     geresh).  This is the prose analogue of poetic's dexi + munax whitelist entry: a
#     legitimate same-letter pair spared as a two-token *sequence* (telg then geresh), not
#     fused.  Plain geresh (U+059C) is whitelisted alongside the muqdam codepoint because
#     the guard runs on raw codepoints, pre-scanner, before muqdam->geresh normalization.
#
# ANY other two accents on one letter is an alphabet error.  Order-less (a frozenset of
# frozensets): the within-letter order of two stacked accents is not meaningful.  The sole
# attested illicit pair is mahapakh (U+05A4) + tipexa (U+0596) (lv25:20, word נֹּאכַל -- WLC
# keeps a mahapakh MAM drops, tagging the word anomalous via ]n), flagged by this general
# rule.  The label uses the order-preserving same-letter-pair bang convention.
_WHITELISTED_SAME_LETTER: frozenset[frozenset[str]] = frozenset(
    (
        frozenset((am.MAHAPAKH, am.QADMA)),
        frozenset((am.TELISHA_GEDOLA, am.GERSHAYIM)),
        frozenset((am.TELISHA_GEDOLA, am.GERESH)),
        frozenset((am.TELISHA_GEDOLA, am.GERESH_MUQDAM)),
    )
)

# Per-accent prose leaf names, for building a same-letter pair's bang label; reuse the
# scanner's spellings (prose_scanner._LEAF -- qadma's standalone prose leaf is "qadma").  A codepoint
# fallback (``U+XXXX``) covers any unforeseen mark so the label is always populated.
_ACCENT_LEAF_NAME: dict[str, str] = {
    am.ATNAX: "atnax",
    am.SEGOLTA: "segolta",
    am.SHALSHELET: "shalshelet",
    am.ZAQEF_QATAN: "zaqef",
    am.ZAQEF_GADOL: "zaqefgadol",
    am.TIPEXA: "tipexa",
    am.REVIA: "revia",
    am.PASHTA: "pashta",
    am.YETIV: "yetiv",
    am.TEVIR: "tevir",
    am.GERESH: "geresh",
    am.GERESH_MUQDAM: "geresh",
    am.GERSHAYIM: "gershayim",
    am.QARNEY_PARA: "pazergadol",
    am.TELISHA_GEDOLA: "telishagedola",
    am.PAZER: "pazer",
    am.MUNAX: "munax",
    am.MAHAPAKH: "mahapakh",
    am.MERKHA: "merkha",
    am.MERKHA_KEFULA: "merkhakefula",
    am.DARGA: "darga",
    am.QADMA: "qadma",
    am.TELISHA_QETANA: "telishaqetanna",
    am.YERAX: "galgal",
    am.TSINNORIT: "tsinnorit",
    am.TSINNOR: "zarqa",
}


def _accent_leaf(mark: str) -> str:
    return _ACCENT_LEAF_NAME.get(mark, f"U+{ord(mark):04X}")


@dataclass(frozen=True)
class LexicalUngrammaticalMark:
    """A lexically illegal mark configuration confined to one atom.

    Covers both a stress-helper left without its fusion partner (unpaired 82) and a
    non-whitelisted same-letter accent pair (e.g. mahapakh!tipexa); ``code``
    distinguishes them.  ``rep_char`` is a representative codepoint of the offending
    word, used by prose_run to locate the pointed-Hebrew word for the report.
    """

    code: str  # M-C code label ("82"), bang pair label ("mahapakh!tipexa"), or a
    # placement descriptor ("medial telisha qetanna")
    atom: str  # the maqaf/space-delimited atom that contains it
    rep_char: str  # a mark of the offending word, for locating its Unicode word


def unpaired_stress_helpers(body: str) -> list[LexicalUngrammaticalMark]:
    """Return every unpaired stress-helper in a prose verse body.

    A stress-helper (today only the tsinnorit, M-C ``82``) is *unpaired* when its
    fusion partner (the tsinnor, M-C ``02``) does not occur later in the same maqaf/
    space-delimited atom.  Such a mark is an intrinsic lexical ("alphabet") error
    independent of surrounding context.
    """
    unpaired: list[LexicalUngrammaticalMark] = []
    for atom in _ATOM_SPLIT_RE.split(body):
        if not atom:
            continue
        for i, ch in enumerate(atom):
            entry = _STRESS_HELPER_PARTNER.get(ch)
            if entry is None:
                continue
            partner, code = entry
            if partner not in atom[i + 1 :]:
                # The unpaired helper itself locates the offending word (U+0598).
                unpaired.append(
                    LexicalUngrammaticalMark(code=code, atom=atom, rep_char=ch)
                )
    return unpaired


def illegal_same_letter_pairs(body: str) -> list[LexicalUngrammaticalMark]:
    """Return every non-whitelisted same-letter accent pair in a prose verse body.

    Two accents are on one base letter iff they are *adjacent* in the body (no
    base-letter ``LETTER`` -- nor any other non-accent -- between them).  Such a stacking is
    an alphabet error unless it is a whitelisted cluster: mahapakh + qadma (ek20:31,
    MAM-confirmed; the scanner fuses it to one ``mahapakh!qadma`` token before the grammar
    and it never reaches here) or telisha gedola + a geresh-family mark (gn5:29, zp2:15,
    2k17:13; kept as a two-token gerstar-then-telg sequence, the manuscript order).  Everything else two-on-a-letter is
    illicit -- today only mahapakh + tipexa (lv25:20), formerly handled by a pair-specific
    check, now flagged by this general guard (the prose analogue of the poetic Plan D bang
    guard).

    Reported with the order-preserving bang label ``a!b`` (body order; e.g.
    ``mahapakh!tipexa``), keyed for word location on the first (here, distinguishing)
    mark -- mahapakh, NOT the tipexa that recurs elsewhere in lv25:20.
    """
    illegal: list[LexicalUngrammaticalMark] = []
    for atom in _ATOM_SPLIT_RE.split(body):
        if not atom:
            continue
        for i in range(len(atom) - 1):
            a, b = atom[i], atom[i + 1]
            if not (_is_accent(a) and _is_accent(b)):
                continue
            if frozenset((a, b)) in _WHITELISTED_SAME_LETTER:
                continue
            code = f"{_accent_leaf(a)}!{_accent_leaf(b)}"
            illegal.append(LexicalUngrammaticalMark(code=code, atom=atom, rep_char=a))
    return illegal


def nonfinal_telisha_qetannas(body: str) -> list[LexicalUngrammaticalMark]:
    """Return every misplaced telisha qetanna in a prose verse body (today: je 44:17).

    A telisha qetanna (U+05A9) is *postpositive*: it belongs on the word-final letter.
    A copy on a non-final letter is the medial stress-helper variant (M-C ``24``), which
    is well-formed *only* when a second telisha qetanna (the real, postpositive ``04``)
    follows it in the same atom -- the ``24{TEXT}04`` pair the scanner fuses into one
    token.  A non-final telisha qetanna with **no** following telisha qetanna is the
    unpaired helper of je 44:17 (כִּי, the mark on the kaf with nothing on the yod) -- an
    intrinsic word-internal error independent of surrounding context.

    "Non-final" is read positionally: a base-letter ``LETTER`` follows the mark later in the
    atom.  This is the only checker-visible defect, because in the Unicode source M-C
    ``24`` and ``04`` collapse to one codepoint -- the helper/main distinction is gone and
    only the placement (kaf vs. yod) survives.
    """
    unpaired: list[LexicalUngrammaticalMark] = []
    for atom in _ATOM_SPLIT_RE.split(body):
        if not atom:
            continue
        for i, ch in enumerate(atom):
            if ch != am.TELISHA_QETANA:
                continue
            rest = atom[i + 1 :]
            if am.LETTER not in rest:
                continue  # word-final -> a legitimate (postpositive) telisha qetanna
            if am.TELISHA_QETANA in rest:
                continue  # the medial helper of a well-formed 24...04 pair (fused)
            # The telisha qetanna itself (U+05A9) locates the offending word.
            unpaired.append(
                LexicalUngrammaticalMark(
                    code="medial telisha qetanna", atom=atom, rep_char=ch
                )
            )
    return unpaired


def lexical_ungrammatical(body: str) -> list[LexicalUngrammaticalMark]:
    """Every prose lexical / word-placement ungrammatical in ``body``, in one pass.

    The union of this module's three checks, each an ``illegal_mark`` ERROR that diverges
    from the goerwitz C oracle in the documented MISSING_SOFPASUQ spirit:

      * an unpaired stress-helper (`unpaired_stress_helpers`, M-C ``82``);
      * a non-whitelisted same-letter accent pair (`illegal_same_letter_pairs`,
        mahapakh!tipexa, lv25:20); and
      * a telisha qetanna misplaced on a non-final letter (`nonfinal_telisha_qetannas`,
        the lone M-C ``24`` of je 44:17).

    This is the single entry point the prose consumers share -- prose_run (the corpus
    output), almost_errors_trees (the exhibit page), and fix_tester (the fix harness) --
    so a verse is classified identically everywhere and the set can never drift between
    them.  A verse with any result here is flagged with a fixed ERROR tree and the grammar
    is skipped entirely.
    """
    return (
        unpaired_stress_helpers(body)
        + illegal_same_letter_pairs(body)
        + nonfinal_telisha_qetannas(body)
    )
