"""CLC(vtrad-BHS) <-> MAM(vtrad-MAM) Decalogue verse map (design doc §7.8).

CLC's primary versification is **vtrad-BHS**. §7.8 optionally surfaces where MAM's
versification (vtrad-MAM) differs. In the whole Bible that difference is confined to the
two Decalogue passages (Exodus 20, Deuteronomy 5); everywhere else MAM and BHS number
verses identically, so this module is identity outside those two chapters.

**What MAM's Decalogue numbering is (verified, not assumed).** MAM's merged-elyon verse
numbering — the numbering MAM-with-doc's HTML anchors use (``#c{ch}v{v}``) — coincides
**exactly with the taḥton (alef) strand's verse boundaries** of the §7.7 split, NOT the
elyon strand's. BHS (CLC's primary) is the *finer* division: it places a verse boundary
wherever *either* strand ends, so BHS = taḥton-boundaries ∪ elyon-boundaries. MAM keeps
only the taḥton boundaries, so relative to BHS it *merges* exactly the runs the elyon
strand chants as one verse while taḥton reads through:

    early split (elyon reads each of "I am" / "no other gods" as one commandment-verse):
        MAM Ex 20:2  = BHS Ex 20:2 + 20:3
        MAM Dt  5:6  = BHS Dt  5:6 + 5:7
    late split (elyon reads each short commandment — murder/adultery/steal/false-witness —
        as its own verse; taḥton and MAM run them together):
        MAM Ex 20:12 = BHS Ex 20:13 + 20:14 + 20:15 + 20:16
        MAM Dt  5:16 = BHS Dt  5:17 + 5:18 + 5:19 + 5:20

The BHS-only "late" 4-way splits are absent from Sefaria's numbering; the early splits are
shared with Sefaria. This module maps BHS↔MAM only (the §7.8 overlay); the Sefaria contrast
lives in ``.novc/mam_decalogue_versemap.json``'s ``mam_to_sef`` block if ever wanted.

**Where §7.8 is rendered: it already is, by §7.7.** Because MAM's versification *is* the
taḥton strand, and §7.7 renders both strands side by side for every diverging Decalogue
verse, the vtrad-MAM boundary overlay is already visible — every place MAM merges is an
atom where §7.7 shows the elyon strand ending a verse (silluq + sof-pasuq) that the taḥton
strand (= MAM) reads through. So UXLC-utils#45 adds **no new rendered surface** (Ben's
call): §7.8 is **validation-only**, the same shape as the MAM cross-checks of §7.7
(issues UXLC-utils#42/UXLC-utils#43/UXLC-utils#44). ``clc_versification_test`` asserts
the two accounts agree 1:1 (the taḥton reads-through points from this module's merge
groups == the elyon-ends atoms of ``clc_dual_cant._ORACLE``).

**Source-path (why hand-encoded).** The authoritative converter lives in MAM-basics'
``py_misc.vtrad_data`` / ``versification_differences`` — a **non-``mb_`` dir**, so neither
importable nor vendorable into official CLC code (only ``mb_*`` dirs are; see the repo
CLAUDE.md). A throwaway harvest script (since retired) reached into it to emit a ``.novc/``
versemap dump; the tiny result (four merge groups) is **hand-encoded here once**, validated
against that dump, with **nothing of MAM-basics imported at runtime**
— the same "MAM consulted as signal, embedded nowhere" discipline as §7.7's ``_ORACLE`` and
the Unit A/B cross-checks. Moving the general converter upstream into an ``mb_*`` entry point
was the alternative; not worth it for four facts fully known here.

**Reuse.** The ``clc_to_mam`` map is the CLC-verse → MAM-verse helper issue
UXLC-utils#38 also needs (to link a CLC verse to its MAM-with-doc doc-note anchor) —
built once here, not a UXLC-utils#45-only hack.
"""

# The Decalogue BHS verse runs MAM collapses into a single MAM verse, by (book_id, chapter).
# Each tuple is consecutive BHS verse numbers sharing one MAM (merged-elyon) verse; the MAM
# verse takes the number of the run's first BHS member (after the running -1/-3 shift the
# earlier runs induce). Everything not covered here maps 1:1 (same chapter, same verse).
_MERGE_GROUPS = {
    ("Exodus", 20): ((2, 3), (13, 14, 15, 16)),
    ("Deuter", 5): ((6, 7), (17, 18, 19, 20)),
}


def _groups(book_id, ch):
    return _MERGE_GROUPS.get((book_id, ch), ())


def clc_to_mam(book_id, ch, v):
    """Map a CLC (vtrad-BHS) verse to its MAM (vtrad-MAM merged-elyon) ``(chapter, verse)``.

    Identity outside the two Decalogue chapters. Inside them, every BHS verse of a merge
    group maps to that group's single MAM verse, and all later verses shift down by the
    verses the earlier groups absorbed (−1 per 2-way early split, −3 per 4-way late split).
    """
    absorbed = 0
    for group in _groups(book_id, ch):
        lo, hi = group[0], group[-1]
        if v > hi:
            absorbed += (
                len(group) - 1
            )  # the whole run before v collapsed to one MAM verse
        elif lo <= v <= hi:
            absorbed += v - lo  # v collapses onto its run's first member
        # v < lo: this run is after v, no effect
    return (ch, v - absorbed)


def mam_merge_group(book_id, ch, v):
    """The BHS verse numbers sharing ``v``'s MAM verse, as a tuple in verse order.

    A single-element ``(v,)`` when MAM does not merge ``v`` with any neighbor (the common
    case — including every verse outside the two Decalogue chapters). A multi-element tuple
    exactly at the four merge runs, where MAM draws no internal boundary that BHS does.
    """
    for group in _groups(book_id, ch):
        if group[0] <= v <= group[-1]:
            return group
    return (v,)


def mam_boundary_after(book_id, ch, v):
    """Does vtrad-MAM place a verse boundary at the END of BHS verse ``v``?

    True everywhere BHS and MAM agree (which is everywhere except inside a merge run).
    False exactly when MAM runs through the BHS boundary after ``v`` — i.e. ``v`` is a
    non-final member of a merge group. Those ``False`` points are the vtrad-MAM overlay:
    the boundaries BHS draws that MAM does not (rendered already by §7.7 as the elyon
    strand ending a verse the taḥton strand reads through).
    """
    group = mam_merge_group(book_id, ch, v)
    return v == group[-1]


def mam_differs_from_bhs(book_id, ch, v):
    """Does vtrad-MAM treat CLC verse ``(ch, v)`` any differently from vtrad-BHS?

    True if ``v``'s MAM number differs from its BHS number (the shift) or ``v`` is merged
    with a neighbor (a boundary difference) — i.e. anything the §7.8 overlay would flag.
    """
    mam_ch, mam_v = clc_to_mam(book_id, ch, v)
    return (mam_ch, mam_v) != (ch, v) or len(mam_merge_group(book_id, ch, v)) > 1


def decalogue_chapters():
    """The (book_id, chapter) pairs whose versification differs between MAM and BHS."""
    return tuple(_MERGE_GROUPS)
