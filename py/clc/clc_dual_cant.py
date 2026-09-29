"""Exports the CLC dual-cantillation strand splitter (design doc §7.7).

A few prose loci carry **two cantillation traditions at once** — the Decalogues
(Exod 20, Deut 5) and **Genesis 35:22**, the first application here. UXLC stores
them as one *combined* form in which both strands' accents are written together on
the same words (e.g. רְאוּבֵ֔֗ן carries both zaqef ``U+0594`` and revia ``U+0597``).

This module splits that combined form into the two single-cantillation strands —
alef and bet — for side-by-side display. The split is **near-subtractive, with one
narrowly-scoped, always-marked charity (supplying punctuation only) plus, where a
strand wants an accent UXLC omitted, a note in lieu of inventing one**:

  * **Position-safe subtraction.** Each strand is UXLC's own combined word with
    only the *other* strand's **divergence cluster** resolved: an accent, its
    intimately-tracking **punctuation** (a maqaf / sof-pasuq /
    legarmeh that goes only with that strand — so a sof-pasuq is *suppressed*
    when its silluq is, and never lands on a word whose last accent is e.g.
    etnaḥta), and — where the two strands each mark one letter — the other
    strand's **vowel** (a QUPO word's patax vs. qamats) or **rafe/dagesh**. The
    cluster is replaced *by name at its exact site* (``str.replace(cluster,
    resolution, 1)``), so a mark that recurs elsewhere in the word as a *shared*
    mark is never touched. The two *one-letter* divergences — **rafe/dagesh** and
    the **QUPO vowel split**, where the two strands differ on a single shared
    letter — are no longer resolved silently (issue UXLC-utils#47): each emits ONE lightweight
    note on the **combined (``-C``) row** naming both strands and the letter
    (``_combined_divergence_notes`` → ``_rafe_dagesh_note`` / ``_vowel_split_note``),
    detected straight from the two resolutions (``_cluster_extras``) — no redundant
    oracle field to drift. (They live on the combined row, not duplicated per strand,
    because the divergence concerns both strands equally.)
  * **Marked supply — punctuation only.** A *punctuation* mark a strand needs
    but UXLC lacks may be **supplied — never silently**: it is rendered
    **bracketed and green** (CSS ``clc-added-during-detangling``) with a
    synthesized "added out of thin air" note (e.g. a sof-pasuq breaking Gen
    35:22's pashut into its two chanted verses). Only the three accent-coupled
    punctuation marks — **maqaf / sof-pasuq / legarmeh** — are ever supplied; so
    far three sof-pasuqs are (Gen 35:22 pashut, and the taḥton verse-ends of Exod
    20:8 לקדשו and 20:9 מלאכתך, where UXLC has none).
  * **Omitted accent — noted, never supplied.** Where a strand's chanting calls
    for an *accent* UXLC left untangled (it has only the other strand's accent
    on that word), CLC — a *diplomatic* edition — does **not** invent one: it
    shows the word as UXLC has it (that accent absent) and synthesizes a per-strand
    **note** instead. This is the sharpened §7.7 departure from the wlc-utils
    *detangler*, which (being a grammar-checker) *supplies* the missing accent from
    MAM so its strand parses. The Decalogue cases: Deut 5:6 (elyon's tipeḥa on אנכי
    + etnaḥta on אלהיך), 5:13 (taḥton's pashta on ימים), 5:17 (elyon's silluq on
    תרצח — UXLC has the sof-pasuq but not its silluq).

No letter is changed and no *shared* mark removed (a mark both strands keep
stays in both); only the divergent marks — accent and the punctuation that tracks
it — are subtracted. MAM (via the wlc-utils detangler) is consulted **only as the
oracle** for *which* of two combined marks belongs to which strand, where a
supplied break falls, and which accent a strand wants where UXLC has only the
other's — encoded once, by hand, in ``clc_dual_cant_oracle._ORACLE``. Nothing
of MAM's text is imported.

This is the same charitable shape as the legarmeh-vs-paseq feature (§7.16): both
improve UXLC by importing MAM's auxiliary adjudication of an ambiguity that is
grammatical, not graphical.
"""

from collections import Counter
from dataclasses import dataclass

import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import mb_diff_mpu.describe_diff as describe_diff
import clc.clc_note as clc_note
from clc.clc_dual_cant_oracle import (
    _ADDED_NAME,
    _ORACLE,
    _STRAND_ALEF,
    _STRAND_BET,
    _VOWEL_POINTS,
    _is_accent,
)

# Omitted-accent notes for which independent manuscript grounding exists (issue UXLC-utils#36):
# Ben's own editorial judgment, landed as prose in wlc-utils's supplied-marks.html
# (py/accgram/dual_cant_detangle.py's _supply_reason), that WLC's differing reading at
# this (book, chapter, verse, strand, wanted-accent) is a *reasonable transcription* of
# the LC, not a mis-transcription. Keyed by (book_id, ch, v, strand.short, kind) since a
# verse may have more than one omitted-accent note (e.g. Deut 5:6 has two). Deuteronomy
# 5:7 and 5:13 are NOT here — accgram's detangler never needed to supply anything for
# them, so no wlc-utils basis exists yet. For 5:13's taxton pashta specifically, the
# detangler had nothing to supply because that pashta is already present in WLC —
# erroneously, presumably carried over from BHS, though not yet verified (see the long
# note in clc_render._dt_5_13_taxton_extra); 5:7's elyon meteg parses clean by other means.
_LC_CORROBORATED = {
    ("Exodus", 20, 3, "taḥton", "merkha"),
    ("Deuter", 5, 6, "elyon", "tipeḥa"),
    ("Deuter", 5, 6, "elyon", "etnaḥta"),
    ("Deuter", 5, 17, "elyon", "silluq"),
}

# Omitted-accent notes with an editor-attached long note on the separate long-notes
# page (design doc §7.3, clc_long_note). Three things this flag can do, per case:
#   * License clc_render's "the LC has" wording for an *accent* note (crediting the
#     manuscript, not just CLC's own synthesis) when the long note cites independent
#     grounding -- e.g. Deut 5:13's taxton pashta cites UXLC's own note, which in turn
#     cites BHL Appendix A. See _accent_name's sibling reasoning in clc_render's
#     _omitted_note_sentence.
#   * Simply attach a "further discussion" note with no grounding role -- e.g. Deut 5:7's
#     elyon *meteg*, whose long note cites Yeivin's ITM §355 on the special gaʿya of
#     יהיה-type verbs. That note already takes softened, self-grounding wording
#     (clc_render._omitted_meteg_sentence), so this flag only adds the cross-link.
#   * Relegate a note's wlc-utils grammar-checker citation (_LC_CORROBORATED above) off
#     the main page -- the four _LC_CORROBORATED cases are ALSO here: the inline note
#     used to end with a direct "see the grammar checker's supplied accents page" link;
#     that citation now lives solely in these cases' long note, with just a "See more
#     details in this longer note" pointer left inline (clc_render._omitted_note_body).
# Keyed the same as _LC_CORROBORATED: (book_id, ch, v, strand.short, kind). The actual
# page content lives in clc_render._LONG_NOTE_SPECS (this module stays render-agnostic,
# pure data/logic only).
_HAS_LONG_NOTE = {
    ("Deuter", 5, 13, "taḥton", "pashta"),
    ("Deuter", 5, 7, "elyon", "meteg"),
    ("Exodus", 20, 3, "taḥton", "merkha"),
    ("Deuter", 5, 6, "elyon", "tipeḥa"),
    ("Deuter", 5, 6, "elyon", "etnaḥta"),
    ("Deuter", 5, 17, "elyon", "silluq"),
    (
        "Deuter",
        5,
        8,
        "elyon",
        "pataḥ",
    ),  # an omitted *vowel*, not accent (מתחת; see _omitted_vowel_note)
}


def _accent_name(ch, verse_final):
    """Display name of an accent for an omitted-accent note, taken from the canonical
    mb_diff_mpu authority (``describe_diff.accent_name`` — e.g. "tipeḥa", "zaqef-qatan",
    "munaḥ") so CLC never reinvents a spelling. One CLC override: U+05BD is named "silluq"
    only when ``verse_final`` is true — i.e. this occurrence sits on the verse's own last
    word, immediately paired with (or, if omitted, standing in for) a sof-pasuq (design doc
    §2). Silluq is defined by that verse-final position, nothing else; every other
    occurrence of U+05BD is an ordinary meteg/gaʿya — a purely metrical mark, not part of
    the cantillation system at all — which is what describe_diff already calls that
    codepoint (its ``accent_name`` falls back to the raw Unicode name there). Same glyph,
    two grammatical readings, distinguished only by context — the same shape as the
    legarmeh-vs-paseq ambiguity (§7.16). ``_validate_oracle`` guarantees every omittable
    accent has a canonical name, so this never returns a "HEBREW …" placeholder."""
    if ch == hpo.MTGOSLQ:
        return "silluq" if verse_final else "meteg"
    return describe_diff.accent_name(ch)


# Ref-label suffixes shown in the page (user-facing): combined / alef / bet.
SUFFIX_COMBINED = "C"
SUFFIX_ALEF = "א"  # HEBREW LETTER ALEF
SUFFIX_BET = "ב"  # HEBREW LETTER BET

# Hover description for the combined ref label (book-independent).
TOOLTIP_COMBINED = (
    "Combined cantillation — both strands' accents tangled together, "
    "as written in the Leningrad Codex."
)


# Each dual-cant book uses a different pair of strand traditions, so the alef/bet
# doc-labels and tooltips are per-book: Genesis 35:22 is pashut / midrashit; the
# Decalogues (Exodus 20, Deuteronomy 5) are taxton / elyon. The alef strand is always
# the verse-by-verse strand, bet the grouped/alternative one.
@dataclass(frozen=True)
class _Strand:
    doc_label: str  # short doc-column label
    tooltip: str  # hover description for the ref label
    short: str  # bare strand name (e.g. "taxton"), for the omitted-accent note prose


_PASHUT = _Strand(
    "pashut (simple) strand",
    "Strand א (pashut / simple): the verse-by-verse accentuation, "
    "separated from the combined marks using MAM as oracle — no mark "
    "subtracted but the other strand's, only a maqaf/sof-pasuq supplied.",
    "pashut",
)
_MIDRASHIT = _Strand(
    "midrashit (interpretive) strand",
    "Strand ב (midrashit / interpretive): the alternative accentuation, "
    "separated the same way.",
    "midrashit",
)
_TAXTON = _Strand(
    "taḥton strand",
    "Strand א (taḥton): the verse-by-verse cantillation that divides the "
    "Decalogue into its prose verses, separated from the combined marks using MAM as "
    "oracle — only the other strand's accents and the punctuation tracking them are "
    "subtracted (so a sof-pasuq is dropped where this strand does not end a verse).",
    "taḥton",
)
_ELYON = _Strand(
    "elyon strand",
    "Strand ב (elyon): the cantillation that chants each commandment as one "
    "verse, separated the same way.",
    "elyon",
)

# alef/bet strands per dual-cant book (bk39 id).
_STRANDS = {
    "Genesis": (_PASHUT, _MIDRASHIT),
    "Exodus": (_TAXTON, _ELYON),
    "Deuter": (_TAXTON, _ELYON),
}


@dataclass(frozen=True)
class StrandView:
    """One displayable form of a dual-cant verse: combined, alef, or bet."""

    suffix: str  # ref-label suffix: "C" / "א" / "ב"
    tooltip: str  # hover description for the ref label
    doc_label: str  # short doc-column label ("" for the combined form)
    atoms: list  # atom dicts (clc_read shape + "additions" on split atoms)
    notes: (
        tuple
    ) = ()  # synthesized strand notes: supplied-mark + omitted-accent (strand only)


def is_dual_cant(book_id, ch, v):
    """Is (book, chapter, verse) one of the dual-cantillation loci?"""
    return (ch, v) in _ORACLE.get(book_id, {})


def split_word(combined_text, entry, strand):
    """Position-safely resolve one divergence atom for ``strand`` (subtractive only).

    Replaces the FIRST occurrence of ``entry['cluster']`` with the strand's
    resolution (``entry['alef']`` or ``entry['bet']``). A constituent mark that
    recurs elsewhere in the word as a shared mark is untouched. Returns the
    strictly-subtracted text; SUPPLIED punctuation is applied separately (see
    ``_split_atom``), never folded into the returned text.
    """
    resolution = entry[strand]
    cluster = entry["cluster"]
    assert cluster in combined_text, (combined_text, cluster)
    return combined_text.replace(cluster, resolution, 1)


def strand_views(book_id, ch, v, verse_atoms):
    """Return the three displayable views (combined, alef, bet) of a dual-cant verse.

    ``verse_atoms`` is the verse's atom list from clc_read. The combined view
    reuses those atoms unchanged; each alef/bet view holds fresh atom dicts whose
    text has the other strand's divergence cluster resolved (see ``split_word``)
    plus an ``additions`` list. Notes divide by whom they concern: a **per-strand**
    note (a mark the strand supplies, or an accent it wants but UXLC omitted) rides
    its own alef/bet view; a **both-strands** divergence note (rafe/dagesh or the QUPO
    vowel split — where the two strands differ on ONE letter) rides the **combined**
    view, stated once naming both strands, rather than duplicated per strand.
    """
    oracle = _ORACLE[book_id][(ch, v)]
    alef_strand, bet_strand = _STRANDS[book_id]
    alef_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_ALEF)
    bet_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_BET)
    verse_loc = (book_id, ch, v)
    combined_notes = _combined_divergence_notes(
        verse_atoms, alef_atoms, bet_atoms, alef_strand, bet_strand
    )
    return [
        StrandView(SUFFIX_COMBINED, TOOLTIP_COMBINED, "", verse_atoms, combined_notes),
        StrandView(
            SUFFIX_ALEF,
            alef_strand.tooltip,
            alef_strand.doc_label,
            alef_atoms,
            _strand_notes(alef_atoms, bet_atoms, alef_strand, bet_strand, verse_loc),
        ),
        StrandView(
            SUFFIX_BET,
            bet_strand.tooltip,
            bet_strand.doc_label,
            bet_atoms,
            _strand_notes(bet_atoms, alef_atoms, bet_strand, alef_strand, verse_loc),
        ),
    ]


def _strand_atoms(verse_atoms, oracle, strand):
    return [
        _split_atom(atom, atom_index, oracle, strand)
        for atom_index, atom in enumerate(verse_atoms, start=1)
    ]


def _split_atom(atom, atom_index, oracle, strand):
    entry = oracle.get(atom_index)
    if entry is None:
        return atom  # shared single mark (or no mark) — unchanged
    text = split_word(atom["text"], entry, strand)
    additions = entry.get("add", {}).get(strand, [])
    omitted = entry.get("omit", {}).get(strand, [])
    omitted_vowels = entry.get("omit_vowel", {}).get(strand, [])
    rafe_dagesh = _rafe_dagesh_state(entry, strand)
    qupo_vowel = _qupo_vowel(entry, strand)
    # The base letter carrying a rafe/dagesh or QUPO divergence — shared by both strands, so it
    # is the same char whichever strand this is; ``None`` for a pure-accent atom. Named in the
    # combined-row both-strands note (e.g. "On the נ of פני …").
    marks = (
        {hpo.DAGOMOSD, hpo.RAFE}
        if rafe_dagesh
        else {hpo.QAMATS, hpo.PATAX} if qupo_vowel else None
    )
    letter = _base_letter(atom["text"], entry["cluster"], marks) if marks else None
    return {
        **atom,
        "text": text,
        "additions": list(additions),
        "omitted_accents": list(omitted),
        "omitted_vowels": list(omitted_vowels),
        "rafe_dagesh": rafe_dagesh,
        "qupo_vowel": qupo_vowel,
        "divergence_letter": letter,
    }


def _strand_notes(strand_atoms, other_strand_atoms, strand, other_strand, verse_loc):
    """Synthesize this strand's own notes, in atom order: one per SUPPLIED mark and one per accent
    it wants but UXLC OMITTED. (The rafe/dagesh and QUPO divergences concern BOTH strands equally —
    one letter the two differ on — so they ride the combined view instead; see
    ``_combined_divergence_notes``.)

    ``other_strand_atoms`` is the sibling strand's atoms — used to name the accent UXLC
    *does* have at an omitted-accent atom (the one the other strand keeps and this one
    lacks), so the note names a concrete mark rather than an abstract placeholder. ``verse_loc``
    is this verse's ``(book_id, ch, v)``, used only to look up ``_LC_CORROBORATED``.

    Lightweight, JSON-serializable dicts — NOT ClcNotes: strand rows own no
    anchors/always-links and no §7.9 departure record yet (design doc §7.7 keeps
    strands display-only). clc_render composes the prose around the snippet.
    """
    notes = []
    for atom_index, (atom, other_atom) in enumerate(
        zip(strand_atoms, other_strand_atoms), start=1
    ):
        for added_char in atom.get("additions", ()):
            notes.append(_added_note(atom["text"], added_char, atom_index))
        for omitted_char in atom.get("omitted_accents", ()):
            present = _present_accent(atom["text"], other_atom["text"])
            present_verse_final = hpu.SOPA in other_atom["text"]
            notes.append(
                _omitted_note(
                    atom["text"],
                    omitted_char,
                    present,
                    present_verse_final,
                    strand,
                    other_strand,
                    verse_loc,
                    atom_index,
                )
            )
        for omitted_vowel in atom.get("omitted_vowels", ()):
            present = _present_vowel(atom["text"], other_atom["text"])
            notes.append(
                _omitted_vowel_note(
                    atom["text"],
                    omitted_vowel,
                    present,
                    strand,
                    other_strand,
                    verse_loc,
                    atom_index,
                )
            )
    return tuple(notes)


def _combined_divergence_notes(
    verse_atoms, alef_atoms, bet_atoms, alef_strand, bet_strand
):
    """The verse's **both-strands** divergence notes, for the combined (``-C``) row: one per
    rafe/dagesh atom and one per QUPO vowel-split atom, each stated ONCE naming both strands and
    the shared letter they differ on (design doc §7.7, issue UXLC-utils#47) — rather than the same fact
    duplicated (polarity-flipped) as a per-strand note on each of alef and bet.

    Built from the two split-strand atom lists, whose ``rafe_dagesh`` / ``qupo_vowel`` /
    ``divergence_letter`` fields ``_split_atom`` already detected off the resolutions; the
    ``verse_atoms`` (combined) supply the word each note names. Lightweight JSON-serializable
    dicts, not ClcNotes (no §7.9 row yet)."""
    notes = []
    for atom_index, (combined, a_atom, b_atom) in enumerate(
        zip(verse_atoms, alef_atoms, bet_atoms), start=1
    ):
        word = combined["text"]
        if a_atom.get("rafe_dagesh"):
            notes.append(
                _rafe_dagesh_note(
                    word,
                    a_atom["divergence_letter"],
                    atom_index,
                    alef_strand,
                    a_atom["rafe_dagesh"],
                    bet_strand,
                    b_atom["rafe_dagesh"],
                )
            )
        if a_atom.get("qupo_vowel"):
            notes.append(
                _vowel_split_note(
                    word,
                    a_atom["divergence_letter"],
                    atom_index,
                    alef_strand,
                    a_atom["qupo_vowel"],
                    bet_strand,
                    b_atom["qupo_vowel"],
                )
            )
    return tuple(notes)


def _present_accent(this_text, other_text):
    """The accent UXLC has at this atom: the (single) accent the OTHER strand keeps and
    this strand lacks — i.e. the divergent accent present in UXLC. ``None`` if none."""
    this_accents = {ch for ch in this_text if _is_accent(ch)}
    return next(
        (ch for ch in other_text if _is_accent(ch) and ch not in this_accents), None
    )


def _present_vowel(this_text, other_text):
    """The vowel UXLC has at an omitted-*vowel* atom: the (single) vowel the OTHER strand
    keeps and this strand lacks — the divergent vowel present in UXLC (Deut 5:8's מתחת: the
    taḥton's qamats, where the elyon tav is left bare). ``None`` if none. The mirror of
    ``_present_accent``, restricted to genuine niqqud vowels (``_VOWEL_POINTS``) so a shared
    dagesh/meteg is never mistaken for the divergent vowel."""
    this_vowels = {ch for ch in this_text if ch in _VOWEL_POINTS}
    return next(
        (ch for ch in other_text if ch in _VOWEL_POINTS and ch not in this_vowels), None
    )


def _cluster_extras(entry, strand):
    """This strand's vs. the other strand's *net* marks within one divergence cluster: the two
    multiset differences of their resolutions (``entry[strand]`` vs. the sibling's). A mark shared
    by both — even one that also recurs, like a word's second qamats — cancels, so what remains is
    exactly the genuinely divergent marks. This is what lets the rafe/dagesh and QUPO divergences be
    *detected* straight from the oracle's own alef/bet resolutions (no redundant oracle field to
    drift), while sidestepping the whole-word-markset trap design doc §7.7 warns of: an unrelated
    *shared* copy of a diverging vowel/point cancels here instead of masking the real divergence.
    """
    other = _STRAND_BET if strand == _STRAND_ALEF else _STRAND_ALEF
    this_c, other_c = Counter(entry[strand]), Counter(entry[other])
    return this_c - other_c, other_c - this_c


def _rafe_dagesh_state(entry, strand):
    """If this atom is a rafe/dagesh divergence (§7.7), this strand's state — ``"dagesh"`` (hard),
    ``"rafe"`` (soft, UXLC's rafe kept), or ``"bare"`` (soft, UXLC marks no rafe, e.g. ex 20:9 כל);
    ``None`` if the two strands don't differ in dagesh/rafe here. Read off ``_cluster_extras``, so a
    dagesh/rafe both strands keep (or one recurring elsewhere in the word) never triggers it.
    """
    this_extra, other_extra = _cluster_extras(entry, strand)
    if not ({hpo.DAGOMOSD, hpo.RAFE} & (set(this_extra) | set(other_extra))):
        return None
    if hpo.DAGOMOSD in this_extra:
        return "dagesh"
    if hpo.RAFE in this_extra:
        return "rafe"
    # This strand carries neither divergent mark, so it is the soft, UXLC-bare side; the OTHER
    # strand must then hold the divergent dagesh (a bare *hard* letter never arises in the oracle).
    assert hpo.DAGOMOSD in other_extra, (entry, strand)
    return "bare"


def _qupo_vowel(entry, strand):
    """If this atom is a QUPO vowel split (§7.7) — the two strands have different vowels
    (patax vs. qamats) on one shared letter — this strand's own divergent vowel char; ``None``
    otherwise. The discriminator is a patax↔qamats *swap* between the two resolutions, so a lone
    divergent qamats NOT paired with the sibling's patax (dt 5:8 atom 12's מתחת) is correctly
    excluded, unlike a naive "any divergent qamats ⇒ QUPO" test."""
    this_extra, other_extra = _cluster_extras(entry, strand)
    this_has = {hpo.QAMATS, hpo.PATAX} & set(this_extra)
    other_has = {hpo.QAMATS, hpo.PATAX} & set(other_extra)
    if not (this_has and other_has and this_has != other_has):
        return None
    (vowel,) = this_has  # a QUPO letter carries exactly one divergent vowel per strand
    return vowel


def _base_letter(combined_text, cluster, marks):
    """The base letter a divergence sits on: the nearest Hebrew letter at or before the FIRST
    of ``marks`` (the divergent dagesh/rafe, or the divergent qamats/patax) inside the cluster's
    site in ``combined_text``. Restricting the search to the cluster's own span avoids a same-type
    mark elsewhere in the word (e.g. a shared qamats). Returns the letter char, or ``None``.
    """
    start = combined_text.index(cluster)
    region = combined_text[start : start + len(cluster)]
    pos = next((start + off for off, ch in enumerate(region) if ch in marks), None)
    if pos is None:
        return None
    for j in range(pos, -1, -1):  # walk back to the letter the mark hangs on
        if describe_diff.is_letter(combined_text[j]):
            return combined_text[j]
    return None


def _added_note(snippet, added_char, atom_index):
    return {
        "kind": _ADDED_NAME[added_char],  # "maqaf" / "sof pasuq"
        "char": added_char,  # the supplied mark itself
        "snippet": snippet,  # the strand word that receives it
        "atom_index": atom_index,  # 1-based atom position, for grouping in clc_render
        "source": clc_note.SOURCE_DUAL_CANT_ADDITION,
        "diff_type": clc_note.DIFF_DUAL_CANT_ADDED_PUNCT,
    }


def _omitted_note(
    snippet,
    accent_char,
    present_char,
    present_verse_final,
    strand,
    other_strand,
    verse_loc,
    atom_index,
):
    """An accent this strand wants but UXLC omitted — noted, not supplied. The snippet is
    the strand word AS SHOWN (that accent absent); no mark is rendered. ``present_char`` is
    the accent UXLC *does* have here (the other strand's), named in the note for concreteness.

    Verse-finality for a U+05BD name (silluq vs. plain meteg, see ``_accent_name``) is read
    off each side's own atom text, never assumed: for the *wanted* accent, ``snippet`` IS
    this strand's own atom text, so a sof-pasuq already there (dt 5:17's elyon) means this
    strand ends its verse here; for the *present* accent, that same check runs on the OTHER
    strand's atom text, passed in as ``present_verse_final`` (dt 5:7's elyon meteg on יהיה־
    fails it — the word is maqaf-joined, not verse-final — so it never wants a silluq).

    ``verse_loc`` is this verse's ``(book_id, ch, v)`` — looked up in ``_LC_CORROBORATED``
    (issue UXLC-utils#36) and ``_HAS_LONG_NOTE`` (design doc §7.3) to flag, respectively, whether
    independent manuscript grounding exists for this note and whether an editor has
    attached a long note on the separate long-notes page; also carried through as-is
    (``verse_loc``) so clc_render can build that long note's anchor without re-deriving
    book/ch/v from elsewhere."""
    wanted_verse_final = hpu.SOPA in snippet
    kind = _accent_name(accent_char, wanted_verse_final)
    book_id, ch, v = verse_loc
    return {
        "kind": kind,  # the wanted accent, e.g. "silluq"
        "char": accent_char,  # the wanted accent (for reference; not rendered)
        "present_kind": (
            _accent_name(present_char, present_verse_final) if present_char else None
        ),  # the accent UXLC has
        "present_char": present_char,
        "snippet": snippet,  # the strand word, shown without the accent
        "atom_index": atom_index,  # 1-based atom position, for grouping in clc_render
        "strand": strand.short,  # the strand that wants it ("elyon"/"taxton"/…)
        "other_strand": other_strand.short,  # the strand whose accent UXLC does have
        "verse_loc": verse_loc,  # (book_id, ch, v), for clc_render's long-note anchor
        "lc_corroborated": (book_id, ch, v, strand.short, kind) in _LC_CORROBORATED,
        "has_long_note": (book_id, ch, v, strand.short, kind) in _HAS_LONG_NOTE,
        "source": clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT,
        "diff_type": clc_note.DIFF_DUAL_CANT_OMITTED_ACCENT,
    }


def _omitted_vowel_note(
    snippet, vowel_char, present_char, strand, other_strand, verse_loc, atom_index
):
    """A vowel this strand wants but UXLC omitted — noted, not supplied, exactly like an
    omitted accent (``_omitted_note``) but for a niqqud vowel. The strand's letter is shown
    bare (``snippet`` already lacks the vowel); the OTHER strand keeps its own, differing
    vowel, named as ``present_char`` for concreteness. Deut 5:8's elyon מתחת wants a patax
    (as its ex 20:4 twin has) where UXLC has only the taḥton's qamats — the asymmetric
    sibling of the QUPO vowel split (``_qupo_vowel``), where BOTH strands carry a vowel.

    The dict is deliberately the SAME shape as ``_omitted_note``'s so clc_render's omitted-
    accent helpers render it unchanged (the prose "The X strand calls for a … here, but the
    LC has only the Y strand's …" is identical) — only ``kind``/``present_kind`` come from
    describe_diff's vowel names (``mark_name``) rather than accent names, and the source/diff
    tags differ. No verse-finality/silluq logic (that is accent-only) and no ``lc_corroborated``
    flag: this note's grounding is its own long note (design doc §7.3)."""
    book_id, ch, v = verse_loc
    kind = describe_diff.mark_name(vowel_char)
    return {
        "kind": kind,  # the wanted vowel, e.g. "patax"
        "char": vowel_char,  # the wanted vowel (for reference; not rendered)
        "present_kind": (
            describe_diff.mark_name(present_char) if present_char else None
        ),  # the vowel UXLC has (the other strand's)
        "present_char": present_char,
        "snippet": snippet,  # the strand word, shown without the vowel
        "atom_index": atom_index,  # 1-based atom position, for grouping in clc_render
        "strand": strand.short,  # the strand that wants it ("elyon"/"taxton"/…)
        "other_strand": other_strand.short,  # the strand whose vowel UXLC does have
        "verse_loc": verse_loc,  # (book_id, ch, v), for clc_render's long-note anchor
        "lc_corroborated": False,  # grounding is the long note, not wlc-utils (§7.3)
        "has_long_note": (book_id, ch, v, strand.short, kind) in _HAS_LONG_NOTE,
        "source": clc_note.SOURCE_DUAL_CANT_OMITTED_VOWEL,
        "diff_type": clc_note.DIFF_DUAL_CANT_OMITTED_VOWEL,
    }


def _rafe_dagesh_note(word, letter, atom_index, a_strand, a_state, b_strand, b_state):
    """A rafe/dagesh divergence (§7.7, faithful Policy 1) as ONE combined-row note naming both
    strands: on the shared ``letter`` of ``word``, each strand hardens (dagesh) or softens (rafe, or
    bare where UXLC marks none) that opening בגדכפת letter, driven by the previous word's disjunctive
    vs. conjunctive accent. ``a_state``/``b_state`` are each strand's own resolution (``"dagesh"`` /
    ``"rafe"`` / ``"bare"``). alef (verse-by-verse) is named first."""
    return {
        "word": word,  # the combined atom word the note names
        "letter": letter,  # the shared letter the two strands differ on
        "atom_index": atom_index,  # 1-based atom position, for the combined row
        "a_strand": a_strand.short,
        "a_state": a_state,  # alef strand + its hard/soft state
        "b_strand": b_strand.short,
        "b_state": b_state,  # bet strand + its state
        "source": clc_note.SOURCE_DUAL_CANT_RAFE_DAGESH,
        "diff_type": clc_note.DIFF_DUAL_CANT_DAGESH,
    }


def _vowel_split_note(
    word, letter, atom_index, a_strand, a_vowel_char, b_strand, b_vowel_char
):
    """A QUPO vowel split (§7.7) as ONE combined-row note naming both strands: on the shared
    ``letter`` of ``word`` the two strands have different vowels (patax vs. qamats), each its own.
    Vowel names come from the canonical ``describe_diff`` authority (never a reinvented spelling).
    alef first."""
    return {
        "word": word,  # the combined atom word the note names
        "letter": letter,  # the shared letter carrying the two vowels
        "atom_index": atom_index,  # 1-based atom position, for the combined row
        "a_strand": a_strand.short,
        "a_vowel": describe_diff.mark_name(a_vowel_char),
        "b_strand": b_strand.short,
        "b_vowel": describe_diff.mark_name(b_vowel_char),
        "source": clc_note.SOURCE_DUAL_CANT_QUPO_VOWEL,
        "diff_type": clc_note.DIFF_DUAL_CANT_QUPO_VOWEL,
    }
