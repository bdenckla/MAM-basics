"""Exports ClcNote, the single note schema all CLC note sources flow into.

The skeleton only sources UXLC's own ``<x>`` self-flags (the under-bar codes m/d
plus the general transcription-uncertainty catch-all t — see design doc §2, issue
UXLC-utils#18), but the schema is deliberately source-agnostic: bracket notes, change
records, FOIs,
dagesh restorations, etc. all feed this same record (design doc §8, "one
renderer, many sources"). Records are plain data (JSON-serializable) so the same
notes can later drive the §7.9 differences-from-UXLC index.
"""

from dataclasses import dataclass, asdict

# --- source tags (the "source" field) ---
SOURCE_UXLC_X_NOTE = "uxlc-x-note"  # UXLC <x> note + its tanach.us note-page prose
SOURCE_DUAL_CANT_ADDITION = (
    "dual-cant-addition"  # punctuation supplied to clarify one strand
)
SOURCE_DUAL_CANT_OMITTED_ACCENT = (
    "dual-cant-omitted-accent"  # accent a strand wants but UXLC omitted
)
# The two strands harden/soften a בגדכפת letter differently (dagesh vs. rafe/bare, §7.7).
SOURCE_DUAL_CANT_RAFE_DAGESH = "dual-cant-rafe-dagesh"
# The two strands have different vowels (patax vs. qamats) on one shared letter (QUPO, §7.7).
SOURCE_DUAL_CANT_QUPO_VOWEL = "dual-cant-qupo-vowel"
# A vowel one strand's chanting wants but UXLC omitted, leaving that strand's letter bare
# while the other strand keeps its own vowel (the asymmetric sibling of QUPO; Deut 5:8 מתחת).
SOURCE_DUAL_CANT_OMITTED_VOWEL = "dual-cant-omitted-vowel"

# --- difference types (the "diff_type" field, for the §7.9 index) ---
DIFF_UNDER_BAR = "under-bar"  # a vertical bar below the letter: m (prose), d (poetic)
# UXLC's catch-all t <x> flag: general transcription uncertainty (damaged/indistinct;
# any mark or letter — NOT inherently under-bar, design doc §2, issue UXLC-utils#18). Surfaced
# as a note but distinct from the genuinely under-bar m/d.
DIFF_TRANSCRIPTION_UNCERTAINTY = "transcription-uncertainty"
# UXLC's own change log already proposes this exact correction (a pending, not-yet-
# applied change record) -- CLC applies it pre-emptively. Distinct from some future
# departure with no UXLC change-log backing, which will need its own diff_type.
DIFF_UXLC_PENDING_CHANGE_APPLIED = "uxlc-pending-change-applied"
DIFF_DUAL_CANT_ADDED_PUNCT = (
    "dual-cant-added-punct"  # charitable additive divergence mark (§7.7)
)
# An accent a strand's chanting calls for but UXLC left untangled — NOTED, never supplied
# (CLC supplies only punctuation; §7.7). Not a CLC departure from UXLC's text, just an
# annotation, so it carries no green/bracketed mark.
DIFF_DUAL_CANT_OMITTED_ACCENT = "dual-cant-omitted-accent"
# A rafe/dagesh divergence between the two dual-cant strands: one hardens a בגדכפת letter
# (dagesh), the other softens it (rafe, or bare where UXLC marks none) — driven by the previous
# word's disjunctive vs. conjunctive accent (§7.7, faithful Policy 1). Shares §8's general
# `dagesh` bucket, already anticipated there, rather than a dual-cant-specific string.
DIFF_DUAL_CANT_DAGESH = "dagesh"
# A QUPO two-vowels-on-one-letter split: the two strands have different vowels (patax vs.
# qamats) on one shared letter, each its own (§7.7). A new §8 enum value alongside dagesh.
DIFF_DUAL_CANT_QUPO_VOWEL = "dual-cant-qupo-vowel"
# A vowel a strand's chanting calls for but UXLC left untangled — NOTED, never supplied,
# exactly like an omitted accent (§7.7). The strand's letter is shown bare; the other
# strand keeps its own (differing) vowel. Deut 5:8's elyon מתחת wants a patax where UXLC
# wrote only the taxton's qamats — the asymmetric sibling of the QUPO split.
DIFF_DUAL_CANT_OMITTED_VOWEL = "dual-cant-omitted-vowel"


@dataclass
class ClcNote:
    """One CLC note about one atom. Plain data; see design doc §8 for fields."""

    book: str  # bk39 id, e.g. "Proverbs"
    ch: int  # chapter number (1-based)
    v: int  # verse number (1-based)
    atom_index: int  # atom position within the verse (1-based; counts w/q/k)
    atom_text: str  # the pointed Hebrew atom text
    note_code: str  # UXLC one-letter <x> code, e.g. "m", "d", "t"
    note_text: str  # the tanach.us note-page prose (downloaded; see clc_note_pages)
    source: str  # provenance of the note (see SOURCE_* above)
    diff_type: str  # classification for the §7.9 index (see DIFF_* above)
    is_uxlc_departure: bool  # does CLC depart from UXLC here?
    uxlc_reading: str  # what UXLC has at this atom
    clc_reading: str  # what CLC has at this atom
    source_url: str = ""  # tanach.us note page this note's prose came from ("" if none)
    # (release_date, change_id) of a pending/accepted UXLC change record that
    # supersedes this note's tanach.us prose, or () if none. Orthogonal to
    # is_uxlc_departure/diff_type (those describe CLC's own charitable-reading
    # decision; this describes UXLC's own change-log state). When set, clc_render
    # links to the change record instead of showing note_text -- the real prose
    # stays in note_text/source_url for provenance (issue UXLC-utils#19 is about never
    # fabricating note text, not about what gets displayed).
    superseding_uxlc_change: tuple = ()

    def as_dict(self):
        """Return a plain JSON-serializable dict of this note."""
        return asdict(self)
