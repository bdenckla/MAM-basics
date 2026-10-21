"""UXLC accent-change grammar test: do the changes move a verse across the
WLC-4.22 / UXLC grammaticality boundary, and in which direction?

The change records (uxlc_accent_changes.json) partition on `prose_st_ref`:

  * the OUT set -- changes NOT linked to a prose ungrammatical note; and
  * the IN  set -- changes that ARE so linked (i.e. that the prose ungrammatical
    notes flagged and the UXLC then adopted).

Both sets are evaluated by the same `evaluate()` and reported in two sections of
the same output file.  The interesting result was a directional asymmetry: in the
OUT set only degradation crossed the boundary (WLC-gram -> UXLC-ungram, never the
reverse); in the IN set only fixes crossed it (WLC-ungram -> UXLC-gram, never the
reverse).  Whether it still holds is now DERIVED, by `_asymmetry_verdict`, rather
than asserted here or in the report -- the sentence used to be pinned, and on
2026-08-04 the file printed "only DEGRADATION crosses" three lines under its own
count of one fix that crossed (#219).

For each grammar-relevant accent change that lies in the PROSE corpus the checker
can evaluate, we:

  1. Transcode the real WLC 4.22 verse to its scanner-ready mark body from the
     canonical `-kq-u` Unicode source (issue wlc-utils#9 retired the old wlc422_ps.txt
     text input; the body is now built straight from the `-kq-u` JSON).
  2. Locate the changed word by the citation's word index, which counts a verse's
     graphical objects as tanach.us counts them (`numbered_atoms`): each word, ketiv
     word and qere word, and each petuxah, setumah and nun inversum.  A reference
     reading with a word boundary inside it spans two (`words_spanned`).
  3. VALIDATE: synthesize the WLC reading of that word from `refuni` (Unicode token
     names -> accent marks) and confirm that scanning the synthesized word
     yields the SAME token stream as scanning the real word.  This certifies,
     per case, that our name->mark synthesis is faithful for this accent content
     (it auto-excludes stress-helper / ordering cases we can't reproduce).  The
     scanner cannot see a maqaf, so the synthesized word must also end with a maqaf
     exactly where the real one does.
     An ADD-accent change is additionally cross-checked against the real UXLC-39
     XML word (`uxlc39_word_marks`): a prepositive/postpositive accent that is
     written twice in the manuscript (graphical edge mark + inner stress-helper/yated) is
     fused/de-duped by the real `uni_to_marks` pipeline but not by our name->mark
     synthesis, so such a case is marked unreliable and excluded (e.g. Josh 2:3.7's
     doubled telisha gedola).
  4. If validated, synthesize the UXLC reading from `changeuni`, splice it into the
     verse body, and re-run the existing checker on both the original (WLC) and edited
     (UXLC) verse.  The UXLC word's own maqaf decides what follows it (`splice_atoms`),
     so a change that removes a maqaf is judged without it, the atom after it a chanted
     word of its own, and one that adds a maqaf is judged with the two atoms one
     chanted word.  Until 2026-10-20 the splice kept the body's maqaf marks and spaces
     whatever the change did to them.  Classify each as grammatical / ungrammatical.  The checker is the one
     `prose_run` applies: the lexical layer (`lexical_validation.lexical_ungrammatical`)
     first, then the scanner and grammar.  The lexical layer is what sees a change that
     leaves a chanted word with no accent, such as UXLC 2.6's meteg for WLC 4.22's merkha at
     Exodus 38:12: the scanner emits no token for such a chanted word, so the grammar alone
     reads the verse as if the chanted word were not there.

Output: per-set WLC-vs-UXLC 2x2s, coverage (how many validated), the excluded
verses with reasons, and the directional-asymmetry conclusion, written to
out/accgram/uxlc_grammar_test.txt.  Console output is ASCII only.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass

from accgram import accent_marks as am
from accgram import lexical_validation
from accgram import rtms_data
from accgram import rtms_rows
from accgram import uni_to_marks
from accgram.prose_ply_grammar import (
    LOCATION_ONLY,
    build_parser,
    parse_tokens,
)
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from accgram.tree import print_tree
from accgram import prose_filter
from wlc_cmn.wlc_book_codes import bk39id_to_wlc_bb
from py_uxlc import my_uxlc
from py_uxlc.my_uxlc_book_abbreviations import expand_citation
from mb_cmn import paths

WLC_KQ_U = paths.out_dir() / "wlc422-kq-u"
SRC = paths.in_dir() / "accgram" / "uxlc_accent_changes.json"
OUT = paths.out_dir() / "accgram" / "uxlc_grammar_test.txt"

MAQAF_CP = "־"  # HEBREW PUNCTUATION MAQAF
PASEQ_CP = "׀"  # HEBREW PUNCTUATION PASEQ

# Unicode accent NAME (as used in refuni/changeuni) -> its scanner mark (accent_marks).
# These are the prose te'amim; poetic-only accents (atnax-hafukh, etc.) have no prose
# mark and simply will not validate if they appear.
NAME2MARK = {
    "etnachta": am.ATNAX,  # translit-ok: UXLC name
    "etnahta": am.ATNAX,  # translit-ok: UXLC name
    "zarqa": am.TSINNOR,
    "zinor": am.TSINNOR,  # translit-ok: UXLC name
    "pashta": am.PASHTA,
    "yetiv": am.YETIV,
    "tevir": am.TEVIR,
    "geresh": am.GERESH,
    "geresh-muqdam": am.GERESH_MUQDAM,
    "gereshayim": am.GERSHAYIM,
    "gershayim": am.GERSHAYIM,
    "telisha-gedola": am.TELISHA_GEDOLA,
    "telisha-qetana": am.TELISHA_QETANA,
    "pazer": am.PAZER,
    "munah": am.MUNAX,  # translit-ok: UXLC name
    "mahapakh": am.MAHAPAKH,
    "makhapakh": am.MAHAPAKH,
    "merkha": am.MERKHA,
    "darga": am.DARGA,
    "qadma": am.QADMA,
    "yerah-ben-yomo": am.YERAX,  # translit-ok: UXLC name
    "ole": am.OLE,
    "iluy": am.ILUY,
    "dehi": am.DEXI,  # translit-ok: UXLC name
    "revia": am.REVIA,
    "zaqef-qatan": am.ZAQEF_QATAN,
    "zaqef-gadol": am.ZAQEF_GADOL,
    "tipeha": am.TIPEXA,  # translit-ok: UXLC name
    "shalshelet": am.SHALSHELET,
}
# Non-accent tokens that still carry meaning for the scanner.
_METEGISH = {"meteg", "silluq"}
# The placeholders ``uni_to_marks._kq_to_marks`` writes for a ketiv-qere's empty side, and
# the ``]N`` note markers it writes after a word, which follow its maqaf where it has one.
_PLACEHOLDERS = frozenset(("*kk", "**qq"))
_NOTES_RE = re.compile(r"(?:\][A-Za-z0-9])+")


def synth_word(uni_tokens: list[str]) -> str | None:
    """Synthesize a scanner-readable mark word from refuni/changeuni token names.

    Letters -> a filler placeholder (the scanner swallows letters; they only serve
    as non-terminator TEXT).  Vowels/points are dropped.  Accents/meteg/sof-pasuq/
    paseq/maqaf become their marks/delimiters, in order.  A space is a word boundary,
    and stays one, unless it is a paseq's or follows a maqaf (`words_spanned`).  Returns
    None if a token has no known prose mark (e.g. a poetic accent) -> case is unsupported.
    """
    out: list[str] = []
    for i, tok in enumerate(uni_tokens):
        if tok in NAME2MARK:
            out.append(NAME2MARK[tok])
        elif tok in _METEGISH:
            out.append(am.METEG)
        elif tok == "sof-pasuq":
            out.append(am.SOF_PASUQ)
        elif tok == "paseq":
            out.append(am.PASEQ)
        elif tok == "maqaf":
            out.append(am.MAQAF)
        elif tok == "space":
            # The flanking space of a paseq attaches the paseq to its word, and the space
            # after a maqaf is the maqaf's word boundary, written twice; neither is a space
            # of the body (a real space there would spuriously split the word in two).
            if not _is_word_boundary_space(uni_tokens, i):
                continue
            out.append(" ")
        else:
            # consonant or vowel/point -> a placeholder filler letter.
            out.append(am.LETTER)
    return "".join(out)


def words_spanned(uni_tokens: list[str]) -> int:
    """How many of tanach.us's words a refuni/changeuni reading spans.

    One, and one more for each word boundary inside it: a maqaf with more of the reading after
    it, and a space that is neither a paseq's nor the one after a maqaf.  A reference reading
    spans two words where a change merges them (2 Samuel 6:7.1, 8:1.2) or joins them with a
    maqaf (Exodus 5:22.11).
    """
    n = 1
    for i, tok in enumerate(uni_tokens):
        if tok == "maqaf" and any(t != "space" for t in uni_tokens[i + 1 :]):
            n += 1
        elif tok == "space" and _is_word_boundary_space(uni_tokens, i):
            n += 1
    return n


def scan_word_tokens(word: str, bb: str, ch: int, vs: int) -> tuple[str, ...]:
    """Scan a single word body to its accent-token TYPE tuple (terminator included)."""
    toks = scan_accents(word, bb, ch, vs, HasLegarmeh())
    return tuple(t.type for t in toks)


@dataclass(frozen=True)
class NumberedAtom:
    """One of a verse's graphical objects, numbered as tanach.us numbers them, in its mark body.

    ``text`` is the object's own marks, a qere's ``**`` or a ketiv's ``*`` and its note markers
    included, its maqaf not.  ``tail`` is all the body has after it before the next numbered
    object: its own maqaf where it has one, the maqaf that joins one ketiv atom to the next, note
    markers written after a maqaf, an empty side's placeholder, and a space.
    """

    text: str
    tail: str
    in_ketiv: bool

    @property
    def has_maqaf(self) -> bool:
        """Whether the object ends with a maqaf of its own."""
        if not self.in_ketiv:
            return self.tail.startswith(am.MAQAF)
        # A ketiv is one run, a maqaf joining each of its atoms to the next, so a tail of that
        # one maqaf alone is the join; any longer tail that opens with a maqaf has the atom's own.
        return self.tail.startswith(am.MAQAF) and self.tail != am.MAQAF


def numbered_atoms(body: str) -> tuple[str, list[NumberedAtom]]:
    """A verse's mark body as tanach.us's graphical objects, and what stands before the first.

    tanach.us numbers each word of a verse, each ketiv word and each qere word among them, and
    each petuxah, setumah and nun inversum: its list of the differences between WLC 4.14 and
    4.16, quoted in ``in/mam-ws-intro/westminster-typing.mediawiki``, defines the graphical
    object so, and a change record's citation counts them.  None of the pieces the body has
    besides is one: an empty side's ``*kk`` or ``**qq`` placeholder, the empty piece a ketiv
    leaves between two maqaf marks or before a space, and note markers written after a maqaf.
    Each belongs to the tail of the object before it.  The body is ``head`` followed by each
    object's ``text`` and ``tail``.
    """
    head = ""
    atoms: list[NumberedAtom] = []
    runs = body.split(" ")
    for r, run in enumerate(runs):
        in_ketiv = run.startswith("*") and not run.startswith("**")
        pieces = run.split(am.MAQAF)
        for k, piece in enumerate(pieces):
            # A preceding read atom's maqaf can put the ketiv opener inside this run.
            if piece.startswith("*"):
                in_ketiv = not piece.startswith("**")
            if k < len(pieces) - 1:
                sep = am.MAQAF
            elif r < len(runs) - 1:
                sep = " "
            else:
                sep = ""
            numbered = (
                piece != ""
                and piece not in _PLACEHOLDERS
                and not (k > 0 and _NOTES_RE.fullmatch(piece))
            )
            if numbered:
                atoms.append(NumberedAtom(piece, sep, in_ketiv))
            elif atoms:
                last = atoms[-1]
                # Tail material keeps its object's role even if this run has another.
                atoms[-1] = NumberedAtom(
                    last.text, last.tail + piece + sep, last.in_ketiv
                )
            else:
                head += piece + sep
    return head, atoms


def splice_atoms(
    atoms: list[NumberedAtom], first: int, last: int, new_word: str
) -> None:
    """Put the synthesized ``new_word`` in place of ``atoms[first]`` to ``atoms[last]``.

    ``new_word`` is the UXLC reading of those objects, and a maqaf at its end is its own, so it
    decides what follows it, as the maqaf decides it in ``uni_to_marks``.  Where the WLC object
    has a maqaf and the UXLC word none, a space takes the maqaf's place, and the atom after it
    is a chanted word of its own; where the UXLC word has a maqaf the WLC object lacks, the
    maqaf takes the space's place and the two are one chanted word; where both have one, it
    stays one.  A ketiv keeps the maqaf that joins its atoms either way.  The objects after the
    first are emptied, so the numbering of every other object stands.
    """
    if any(atoms[i].in_ketiv != atoms[first].in_ketiv for i in range(first, last + 1)):
        raise ValueError("a change spans a ketiv and what is read beside it")
    opener = atoms[first].text[
        : len(atoms[first].text) - len(atoms[first].text.lstrip("*"))
    ]
    tail = _tail_for(atoms[last], new_word.endswith(am.MAQAF))
    atoms[first] = NumberedAtom(
        opener + new_word.removesuffix(am.MAQAF), tail, atoms[first].in_ketiv
    )
    for i in range(first + 1, last + 1):
        atoms[i] = NumberedAtom("", "", atoms[i].in_ketiv)


def joined_atoms(head: str, atoms: list[NumberedAtom]) -> str:
    """The mark body ``numbered_atoms`` read, or that ``splice_atoms`` made of it."""
    return head + "".join(atom.text + atom.tail for atom in atoms)


def is_ungrammatical(parser, body: str, bb: str, ch: int, vs: int) -> bool:
    if lexical_validation.lexical_ungrammatical(body):
        # The lexical layer fires first and decides the verse, as in prose_run.
        return True
    toks = [Token("TILDE", "")] + scan_accents(body, bb, ch, vs, HasLegarmeh())
    tree = parse_tokens(parser, toks)
    if tree is None:
        # No recovery: a residual gap.  Treat as ungrammatical but flag via caller.
        return True
    if tree is LOCATION_ONLY:
        return True
    return "ERROR" in print_tree(tree, 0)


def _mark_count(uni_tokens: list[str]) -> int:
    """Count the *mark-bearing* tokens (accents PLUS meteg/silluq).

    Meteg/silluq must count: a meteg->accent change (e.g. "change meteg to merkha")
    is a 1:1 substitution, not an addition, so it must not be tallied as a net
    accent gain (which would mislabel it 'add_accent')."""
    return sum(1 for t in uni_tokens if t in NAME2MARK or t in _METEGISH)


def _kind(r) -> str:
    """Categorize a change for confidence bucketing.

    - 'remove_terminator': the change drops sof-pasuq (degenerate: necessarily
      errors regardless of accentuation).
    - 'add_accent': nets a new mark-bearing token (coding-sensitive: an added
      prepositive/postpositive accent could be the inner stress-helper we code as
      a main accent -- see the UXLC-39 cross-check in `evaluate`).
    - 'substitution': 1:1 accent swap / removal / meteg<->accent not touching
      sof-pasuq (robust: validated structurally on the WLC side).
    """
    ref = (r.get("refuni_gen") or r.get("refuni") or "").split()
    chg = (r.get("changeuni_gen") or r.get("changeuni") or "").split()
    if "sof-pasuq" in ref and "sof-pasuq" not in chg:
        return "remove_terminator"
    if _mark_count(chg) > _mark_count(ref):
        return "add_accent"
    return "substitution"


def _lexical_findings(body: str) -> list[tuple[str, str]]:
    """What the lexical layer finds in ``body``, each finding as its code and its atom."""
    return [
        (mark.code, mark.atom)
        for mark in lexical_validation.lexical_ungrammatical(body)
    ]


def _is_word_boundary_space(uni_tokens: list[str], i: int) -> bool:
    """Whether the ``space`` at ``uni_tokens[i]`` stands between two of tanach.us's words.

    Not a paseq's flanking space, which attaches the paseq to the word before it, nor the space
    after a maqaf, which is the same boundary as the maqaf.
    """
    following = uni_tokens[i + 1] if i + 1 < len(uni_tokens) else None
    preceding = uni_tokens[i - 1] if i > 0 else None
    return following not in (None, "paseq") and preceding != "maqaf"


def _tail_for(atom: NumberedAtom, gains_maqaf: bool) -> str:
    """``atom``'s tail once it does or does not end with a maqaf, as ``splice_atoms`` says.

    A maqaf that goes takes the note markers written after it with it, as the object's own note
    markers go with its text, the synthesized word having none.
    """
    tail = atom.tail
    if atom.has_maqaf == gains_maqaf:
        return tail
    if gains_maqaf:
        if atom.in_ketiv:
            return am.MAQAF + tail
        if not tail.startswith(" "):
            raise ValueError(f"a maqaf added where no space follows: {atom!r}")
        return am.MAQAF + tail[1:]
    rest = tail[1:]
    notes = _NOTES_RE.match(rest)
    if notes is not None:
        rest = rest[notes.end() :]
    if atom.in_ketiv or rest.startswith(" "):
        return rest
    return " " + rest


def _transcoded_bodies(
    keys,
) -> dict[tuple[str, int, int], str]:
    """The scanner-ready mark body for each ``(bb, ch, vs)``, transcoded from the
    canonical ``-kq-u`` Unicode source (issue wlc-utils#9 retired ``wlc422_ps.txt``)."""
    index = rtms_data.load_wlc422_index(WLC_KQ_U)
    bodies: dict[tuple[str, int, int], str] = {}
    for bb, ch, vs in keys:
        verse = index.get(rtms_rows.to_compact_bcv(bb, ch, vs))
        if isinstance(verse, dict):
            bodies[(bb, ch, vs)] = uni_to_marks.verse_to_marks(verse)
    return bodies


_UXLC_BOOK_CACHE: dict[str, list] = {}


def _uxlc_book(bk_id: str) -> list:
    """Read (and cache) one UXLC-39 book's chapters via ``my_uxlc.read``."""
    if bk_id not in _UXLC_BOOK_CACHE:
        _UXLC_BOOK_CACHE[bk_id] = my_uxlc.read(bk_id)
    return _UXLC_BOOK_CACHE[bk_id]


def _uxlc_maqaf_units(verse_words: list[str]) -> list[str]:
    """Flatten one UXLC-39 verse (a list of ``<w>``/``<q>`` word strings) into
    maqaf-units, matching tanach.us word numbering where the verse has no ketiv, petuxah,
    setumah or nun inversum (and our M-C ``numbered_atoms``, which counts those too).

    Two reconciliations against the raw ``<w>`` order are needed:

    * a ``<w>`` ending in a maqaf joins (no space) to the next ``<w>`` -- the two
      sit in one maqaf chain, so splitting on maqaf re-creates the chain's units;
    * a paseq, written in UXLC-39 as a space-separated ``׀``, attaches to its
      preceding word (tanach.us / the M-C source count it as part of that word),
      so the flanking space is dropped to avoid spawning a spurious unit.
    """
    parts: list[str] = []
    for w in verse_words:
        if parts and not parts[-1].endswith(MAQAF_CP):
            parts.append(" ")
        parts.append(w)
    text = "".join(parts).replace(" " + PASEQ_CP, PASEQ_CP)
    units: list[str] = []
    for sp in text.split(" "):
        units.extend(sp.split(MAQAF_CP))
    return units


def uxlc39_word_marks(
    bk_id: str, ch: int, vs: int, wd: int, n_mc_units: int
) -> tuple[str, ...] | None:
    """Scan-token tuple of the real UXLC-39 word at maqaf-unit ``wd``, or None.

    Returns None when the UXLC-39 maqaf-unit count differs from the M-C count
    (``n_mc_units``): the two sources then number words differently, so ``wd`` does
    not transfer and the cross-check must abstain rather than mis-compare.  Also
    None if the word index is out of range.
    """
    units = _uxlc_maqaf_units(_uxlc_book(bk_id)[ch - 1][vs - 1])
    if len(units) != n_mc_units:
        return None
    if not (1 <= wd <= len(units)):
        return None
    bb = bk39id_to_wlc_bb(bk_id)
    return scan_word_tokens(uni_to_marks.word_to_marks(units[wd - 1]), bb, ch, vs)


def evaluate(records: list[dict], parser) -> dict:
    """Run the per-verse validate-then-classify pipeline over one set of change
    records and return the collected results (stats, 2x2 grids, the broke/fixed
    verse lists, and the excluded verses with reasons).

    Pure function of its inputs -- the OUT and IN sets are evaluated by identical
    code; only the input record set differs.
    """
    # Group prose-corpus changes by verse, so a verse with several changes is
    # tested as ONE coherent UXLC reading (not a per-word chimera).
    by_verse: dict[tuple[str, int, int], list[tuple[int, dict, str]]] = {}
    for r in records:
        bk, ch, vs, wd = expand_citation(r["citation"])
        bb = bk39id_to_wlc_bb(bk)
        if not prose_filter.should_keep_line(bb, ch, vs):
            continue
        by_verse.setdefault((bb, ch, vs), []).append((wd, r, bk))

    bodies = _transcoded_bodies(by_verse)

    stat = Counter()
    grid = Counter()  # (wlc, uxlc) -> n verses (all validated)
    grid_visible = Counter()  # (wlc, uxlc) -> n verses (checker-visible only)
    cell_by_kind = Counter()  # (kind, wlc, uxlc) over individual changes in solo verses
    broke = []  # verses: WLC-gram -> UXLC-ungram
    fixed = []  # verses: WLC-ungram -> UXLC-gram
    excluded = []  # (ref, [citations], reason)

    for (bb, ch, vs), changes in by_verse.items():
        stat["prose_verses"] += 1
        stat["prose_changes"] += len(changes)
        body = bodies.get((bb, ch, vs))
        if body is None:
            stat["no_body"] += 1
            continue
        head, atoms = numbered_atoms(body)
        if joined_atoms(head, atoms) != body:
            raise ValueError(
                f"{bb} {ch}:{vs}: the numbered atoms do not rebuild {body!r}"
            )

        # Validate every change in the verse; apply them all to build UXLC body.
        uxlc_atoms = list(atoms)
        reason = ""
        for wd, r, bk in changes:
            ref_tokens = (r.get("refuni_gen") or r.get("refuni") or "").split()
            first, last = wd - 1, wd - 2 + words_spanned(ref_tokens)
            if not (0 <= first and last < len(atoms)):
                reason = "word-index out of range"
                break
            ref_syn = synth_word(ref_tokens)
            chg_syn = synth_word(
                (r.get("changeuni_gen") or r.get("changeuni") or "").split()
            )
            if ref_syn is None or chg_syn is None:
                reason = "unsupported accent (no prose mark)"
                break
            wlc_word = joined_atoms("", atoms[first:last]) + atoms[last].text
            if scan_word_tokens(ref_syn, bb, ch, vs) != scan_word_tokens(
                wlc_word, bb, ch, vs
            ):
                reason = "ref-mismatch: synth WLC word != real M-C word"
                break
            # The maqaf is invisible to the token comparison above, and the reference
            # reading's maqaf is the one a change keeps or removes, so it must be WLC 4.22's.
            if ref_syn.endswith(am.MAQAF) != atoms[last].has_maqaf:
                reason = "ref-mismatch: synth WLC word's maqaf != real M-C word's"
                break
            # ADD-accent cross-check against the real UXLC-39 XML: a doubled
            # prepositive/postpositive accent (graphical edge mark + inner
            # stress-helper) is fused/de-duped by the real uni_to_marks pipeline
            # but not by our name->mark synth, so exclude such a change.
            if _kind(r) == "add_accent":
                real = uxlc39_word_marks(bk, ch, vs, wd, len(atoms))
                if real is not None and scan_word_tokens(chg_syn, bb, ch, vs) != real:
                    reason = "UXLC-39 cross-check: doubled stress-helper accent"
                    break
            splice_atoms(uxlc_atoms, first, last, chg_syn)
        uxlc_body = joined_atoms(head, uxlc_atoms)
        if reason:
            stat["unreliable_verses"] += 1
            stat["unreliable_changes"] += len(changes)
            excluded.append(
                ((bb, ch, vs), [r["citation"] for _, r, _ in changes], reason)
            )
            continue
        stat["validated_verses"] += 1
        stat["validated_changes"] += len(changes)

        # A change is "checker-visible" only if it alters the accent-token stream or what
        # the lexical layer finds; otherwise (meteg reorder, collapsed sub-distinction, ...)
        # the checker cannot possibly react and the verse is a trivial neutral.  A change
        # that removes or adds a maqaf and touches no accent alters the token stream only
        # where a rule reads across a maqaf (the metigah-zaqef fuse, the mayela lookahead),
        # but the lexical layer sees the chanted word with no accent it leaves or ends.
        wlc_stream = tuple(
            t.type for t in scan_accents(body, bb, ch, vs, HasLegarmeh())
        )
        uxlc_stream = tuple(
            t.type for t in scan_accents(uxlc_body, bb, ch, vs, HasLegarmeh())
        )
        visible = wlc_stream != uxlc_stream or _lexical_findings(
            body
        ) != _lexical_findings(uxlc_body)
        stat["visible" if visible else "noop"] += 1

        wlc_bad = is_ungrammatical(parser, body, bb, ch, vs)
        uxlc_bad = is_ungrammatical(parser, uxlc_body, bb, ch, vs)
        cell = (
            "WLC-ungram" if wlc_bad else "WLC-gram",
            "UXLC-ungram" if uxlc_bad else "UXLC-gram",
        )
        if visible:
            grid_visible[cell] += 1
        grid[cell] += 1
        # The cut description is stripped, since a cut that ends on a space would leave
        # trailing whitespace in the report.
        descs = [
            (
                r["citation"],
                r["accent_change_reason"],
                _kind(r),
                r["description"][:55].rstrip(),
            )
            for _, r, _ in changes
        ]
        # Attribute by-kind only for solo-change verses (clean attribution).
        if len(changes) == 1:
            cell_by_kind[(descs[0][2], cell[0], cell[1])] += 1
        if not wlc_bad and uxlc_bad:
            broke.append(((bb, ch, vs), descs))
        elif wlc_bad and not uxlc_bad:
            fixed.append(((bb, ch, vs), descs))

    return {
        "stat": stat,
        "grid": grid,
        "grid_visible": grid_visible,
        "cell_by_kind": cell_by_kind,
        "broke": broke,
        "fixed": fixed,
        "excluded": excluded,
    }


def report_section(res: dict, title: str, p) -> None:
    """Emit one set's report section through the line-printer ``p``."""
    stat = res["stat"]
    grid, grid_visible = res["grid"], res["grid_visible"]
    broke, fixed = res["broke"], res["fixed"]
    p(f"=== {title} ===")
    p()
    p(
        f"prose-corpus verses          : {stat['prose_verses']}  ({stat['prose_changes']} changes)"
    )
    p(
        f"  validated                  : {stat['validated_verses']} verses ({stat['validated_changes']} changes)"
    )
    p(
        f"  excluded                   : {stat['unreliable_verses']} verses ({stat['unreliable_changes']} changes)"
    )
    p()
    p(f"  of validated: checker-VISIBLE change {stat['visible']}, no-op {stat['noop']}")
    p()
    p("2x2 over validated VERSES (all):")
    for w in ("WLC-gram", "WLC-ungram"):
        for u in ("UXLC-gram", "UXLC-ungram"):
            p(f"  {w:11s} -> {u:12s}: {grid[(w, u)]}")
    p()
    p("2x2 over checker-VISIBLE verses (the meaningful denominator):")
    for w in ("WLC-gram", "WLC-ungram"):
        for u in ("UXLC-gram", "UXLC-ungram"):
            p(f"  {w:11s} -> {u:12s}: {grid_visible[(w, u)]}")
    p()
    p(f"WLC-gram -> UXLC-ungram (degradation): {len(broke)} verses")
    for ref, descs in sorted(broke):
        for cit, reason, kind, desc in descs:
            p(f"    {cit:16s} [{reason}/{kind}] {desc}")
    p()
    p(f"WLC-ungram -> UXLC-gram (fix): {len(fixed)} verses")
    for ref, descs in sorted(fixed):
        for cit, reason, kind, desc in descs:
            p(f"    {cit:16s} [{reason}/{kind}] {desc}")
    p()
    p("Excluded verses (synth could not be validated):")
    for ref, cits, reason in sorted(res["excluded"]):
        p(f"    {', '.join(cits):28s} {reason}")
    p()
    cell_by_kind = res["cell_by_kind"]
    p("By-kind breakdown of solo-change verses (confidence buckets):")
    kinds = sorted({k for (k, _, _) in cell_by_kind})
    for k in kinds:
        gg = cell_by_kind[(k, "WLC-gram", "UXLC-gram")]
        gb = cell_by_kind[(k, "WLC-gram", "UXLC-ungram")]
        ug = cell_by_kind[(k, "WLC-ungram", "UXLC-gram")]
        ub = cell_by_kind[(k, "WLC-ungram", "UXLC-ungram")]
        p(
            f"  {k:18s}: WLC-gram->[g {gg:3d} / u {gb:3d}]   WLC-ungram->[g {ug:3d} / u {ub:3d}]"
        )


def _asymmetry_verdict(out_res: dict, in_res: dict) -> list[str]:
    """The closing paragraph, derived from the two sets rather than written down.

    A leak is a crossing in the direction its set is not supposed to produce: a fix in the
    OUT set, a degradation in the IN set.  With none of either the original finding stands
    and is stated; with any, the file names them instead of asserting a universal its own
    counts contradict.  It reports rather than raises, because a leak can be a note that has
    not been written yet -- ne 9:20 became one on 2026-08-04 (#218 item 1), and
    will leave the OUT set for the IN set when its research note names its `uxlc_change`.
    """
    leaks = (
        ("OUT", "WLC-ungram->UXLC-gram, a fix", out_res["fixed"]),
        ("IN ", "WLC-gram->UXLC-ungram, a degradation", in_res["broke"]),
    )
    if not any(verses for _, _, verses in leaks):
        return [
            "  The changes the prose ungrammatical notes flagged (IN set) only ever repair",
            "  ungrammaticality; the changes they did not flag (OUT set) only ever",
            "  introduce it.  No fix leaks into OUT and no degradation leaks into IN.",
        ]
    lines = ["  The asymmetry does NOT hold as stated. Crossing the wrong way:"]
    for label, direction, verses in leaks:
        for (bb, ch, vs), descs in sorted(verses):
            for cit, _reason, _kind, _desc in descs:
                lines.append(f"    {label} set: {bb} {ch}:{vs} ({cit}) -- {direction}")
    return lines


def main() -> None:
    data = json.load(open(SRC, encoding="utf-8"))
    out_set = [r for r in data if not r["prose_st_ref"]]
    in_set = [r for r in data if r["prose_st_ref"]]

    parser = build_parser()
    out_res = evaluate(out_set, parser)
    in_res = evaluate(in_set, parser)

    lines = []

    def p(s=""):
        lines.append(s)
        # Console is ASCII-only (the file keeps the full UTF-8 text); a few change
        # descriptions embed a Hebrew accent glyph that a cp1252 console cannot encode.
        print(s.encode("ascii", "replace").decode("ascii"))

    report_section(
        out_res,
        "OUT set: WLC-4.22 vs UXLC grammaticality (changes NOT in prose output)",
        p,
    )
    p()
    p()
    report_section(
        in_res,
        "IN set: WLC-4.22 vs UXLC grammaticality (changes IN prose output)",
        p,
    )
    p()
    p()
    p("=== Directional asymmetry across the grammaticality boundary ===")
    p()
    p(
        f"  OUT set: WLC-gram->UXLC-ungram {len(out_res['broke'])}, "
        f"WLC-ungram->UXLC-gram {len(out_res['fixed'])}."
    )
    p(
        f"  IN  set: WLC-ungram->UXLC-gram {len(in_res['fixed'])}, "
        f"WLC-gram->UXLC-ungram {len(in_res['broke'])}."
    )
    p()
    for line in _asymmetry_verdict(out_res, in_res):
        p(line)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nWrote report to {OUT}")


if __name__ == "__main__":
    main()
