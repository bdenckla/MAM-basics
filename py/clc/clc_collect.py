"""Exports collect_for_book: UXLC <x> notes + their note-page prose -> ClcNotes.

This is the skeleton's note source (build-order step 3). It surfaces UXLC's own
``<x>`` self-flags but does NOT yet resolve them: the genuinely under-bar codes
m/d (a vertical bar below the letter) plus the general transcription-uncertainty
catch-all t (damaged/indistinct; any mark or letter — *not* inherently under-bar,
design doc §2, issue UXLC-utils#18). There is no accent grammar and no charitable departure
here, so every note has ``is_uxlc_departure=False`` and ``clc_reading ==
uxlc_reading``. Charity layers on later (design doc §3, §7.1).

Each note's prose is the *actual* tanach.us note page, read offline from the
committed local copy (clc_note_pages; downloaded by main_clc_download_notes). The
build never touches the network, so its output is deterministic. There is no
fabricated substitute for a missing page (issue UXLC-utils#19): an atom whose note page has
not been downloaded yet shows a bare ``[note not yet downloaded]`` placeholder --
never the imperative change-log description (an instruction to the editor, not a
note) and never an invented per-code gloss. clc_changes is kept only for the
atom-letter consistency guard.
"""

import mb_cmn.hebrew_accents as acc
import mb_cmn.hebrew_letters as hl
import clc.clc_changes as clc_changes
import clc.clc_note as clc_note
import clc.clc_note_pages as clc_note_pages
import clc.clc_read as clc_read
import uxlc_misc.my_uxlc as my_uxlc

# The genuinely under-bar ambiguity codes — a vertical bar below the letter —
# that seed CLC's charitable §2a resolution (design doc §2): m (prose
# merkha/meteg) and d (poetic dexi/tarxa). NOT t: despite one
# qualifying note ("examine mark below … as possible merkha"), t is a general
# transcription-uncertainty flag (233×, the largest code) that mostly has
# nothing to do with a sub-letter mark, so selecting every t atom over-includes
# as under-bar (issue UXLC-utils#18). A per-note prose filter could later promote the
# genuinely under-bar subset of t.
UNDER_BAR_CODES = ("m", "d")

# All UXLC <x> codes CLC currently surfaces as notes: the under-bar pair leads
# (design doc §2, §7.1), followed by the general transcription-uncertainty t. This
# is the *note-surfacing* seed — a superset of the *under-bar* seed above; t is
# surfaced (and downloaded) but classified as transcription-uncertainty, not
# under-bar (see _diff_type_for).
NOTED_CODES = UNDER_BAR_CODES + ("t",)

# Placeholder shown for an atom whose tanach.us note page has not been downloaded
# yet (design doc §9 #2). Deliberately NOT a description of the note: the prose
# must come from the real page (issue UXLC-utils#19), so this only marks where that prose
# will appear once main_clc_download_notes has fetched the page. No invented text.
_NOT_YET_DOWNLOADED = "[note not yet downloaded]"

# Reviewed atom/change-log letter mismatches that are NOT atom merges/splits and
# so are accepted rather than raised by _check_atom_consistency. Keyed by
# (book, ch, v, position) with the reason. Any *unlisted* mismatch still raises.
_KNOWN_ATOM_MISMATCHES = {
    ("Jeremiah", 27, 11, 10): (
        "Current UXLC has וְהִנַּחְתִּיו (3ms suffix vav); the 2023 'severely "
        "damaged text' change recorded וְהִנַּחְתִּי (no suffix vav). Position is "
        "correct — the change-log text differs from current UXLC by one letter."
    ),
}

# Notes whose tanach.us prose is superseded by a later, more specific UXLC
# change record: rather than show the (now-outdated) prose, clc_render links to
# the change record instead (design doc §7.4). Keyed by (book, ch, v, position,
# code) -- code is included because suppression is a per-note fact (one code on
# an atom might need it while another code on the same atom doesn't), unlike
# _KNOWN_ATOM_MISMATCHES's per-atom key. Value is a (release_date, change_id)
# pair, the same shape amb_early_mtg's "existing UXLC change proposal" records
# use (py/uxlc_amb_early_mtg/amb_early_mtg.py) -- reused for consistency, no
# code dependency on that module.
_NOTES_SUPERSEDED_BY_UXLC_CHANGE = {
    # Deut 5:8.2-t: superseded by 2026.10.19 changes, change #10, "Change
    # pashta over sin to qadma" (in/UXLC-misc/2026.10.19 - Changes.xml).
    ("Deuter", 5, 8, 2, "t"): ("2026.10.19", "2026.04.10-10"),
}

# Atoms where CLC pre-emptively applies a UXLC-authored PENDING correction to its own
# reading -- CLC's first-ever real departure from UXLC's own manuscript text (design
# doc §1: "charitable but transparent" -- every departure recorded as a note). Keyed
# by (book, ch, v, position); value is (old_char, new_char, release_date, change_id).
# old_char must appear in the atom's current text exactly once. Applied to the atom's
# text in collect_for_book, immediately after clc_read.read_book(), so every
# downstream consumer (rendering, clc_dual_cant's strand split) sees the corrected
# reading automatically -- only this dict needs to change for a future such case.
_UXLC_PENDING_CHANGES_APPLIED = {
    # Deut 5:8.2 תעשה: UXLC's own pending change #10 (2026.10.19) already proposes
    # correcting a pashta mid-word on the sin (grammatically impossible -- pashta
    # must fall on a word's final letter) to a qadma, corroborated by BHL. CLC
    # applies that correction now rather than waiting for UXLC to formally adopt it.
    ("Deuter", 5, 8, 2): (acc.PASH, acc.QOM, "2026.10.19", "2026.04.10-10"),
}


def _apply_pending_uxlc_changes(book, book_id):
    """Patch book per _UXLC_PENDING_CHANGES_APPLIED; return {(ch, v, position): original_text}
    so _make_note can recover each patched atom's UXLC reading for its departure note.
    """
    originals = {}
    for (b, ch, v, position), (
        old_char,
        new_char,
        _release,
        _change_id,
    ) in _UXLC_PENDING_CHANGES_APPLIED.items():
        if b != book_id:
            continue
        atom = book[ch - 1][v - 1][position - 1]
        original_text = atom["text"]
        assert original_text.count(old_char) == 1, (
            f"CLC pending-change patch at {book_id} {ch}:{v}.{position}: expected exactly "
            f"one {old_char!r} in {original_text!r}. If UXLC has since applied this change "
            "itself, remove this entry from _UXLC_PENDING_CHANGES_APPLIED."
        )
        book[ch - 1][v - 1][position - 1] = {
            **atom,
            "text": original_text.replace(old_char, new_char, 1),
        }
        originals[(ch, v, position)] = original_text
    return originals


def iter_noted_atoms(book, codes=NOTED_CODES):
    """Yield ``(ch, v, position, atom, code)`` for each atom carrying a code.

    The single source of truth for which (atom, code) pairs carry a UXLC ``<x>``
    code, shared by collect_for_book (which keeps the ``codes=NOTED_CODES``
    default -- the note-surfacing seed) and the note-page downloader
    (main_clc_download_notes, which passes ``codes=None`` to fetch every code, not
    just the seed) so the two cannot drift on the underlying atom/code pairs.
    ``codes=None`` means no filtering: yield every ``<x>`` code an atom carries.
    ``position`` is the 1-based atom index within the verse.
    """
    for chidx, chapter in enumerate(book):
        for vridx, verse in enumerate(chapter):
            for atidx, atom in enumerate(verse):
                for code in atom["types"]:
                    if codes is None or code in codes:
                        yield chidx + 1, vridx + 1, atidx + 1, atom, code


def collect_for_book(book_id, codes=NOTED_CODES, chapters=None):
    """Read book_id and emit ClcNotes for atoms carrying one of ``codes``.

    Returns ``(book, notes)`` where ``book`` is the full read structure (chapters
    -> verses -> atoms) and ``notes`` is a list of ClcNote. Reads note prose
    offline from the committed local pages (clc_note_pages); never the network.
    ``chapters`` (a set of 1-based chapter numbers, or None) limits note
    collection to those chapters; ``book`` is still the whole book, and the render
    side applies the same limit.
    """
    book = clc_read.read_book(book_id)
    pending_change_originals = _apply_pending_uxlc_changes(book, book_id)
    descriptions = clc_changes.load_descriptions()
    notes = []
    page_prose_count = 0
    for ch, v, position, atom, code in iter_noted_atoms(book, codes):
        if chapters is not None and ch not in chapters:
            continue
        prose = clc_note_pages.local_note_prose(book_id, ch, v, position, code)
        page_prose_count += prose is not None
        notes.append(
            _make_note(
                book_id,
                ch,
                v,
                position,
                atom,
                code,
                descriptions,
                prose,
                pending_change_originals,
            )
        )
    _report_prose_coverage(page_prose_count, len(notes))
    return book, notes


def _report_prose_coverage(page_prose_count, total):
    missing = total - page_prose_count
    msg = (
        f"CLC notes: {page_prose_count}/{total} use a downloaded note page; "
        f"{missing} have no local page (shown as a placeholder)."
    )
    if missing:
        msg += " Run main_clc_download_notes to fetch the missing pages."
    print(msg)


def _make_note(
    book_id,
    ch,
    v,
    position,
    atom,
    code,
    descriptions,
    page_prose,
    pending_change_originals,
):
    atom_text = atom["text"]
    records = descriptions.get((book_id, ch, v, position), [])
    _check_atom_consistency(book_id, ch, v, position, atom_text, records)
    is_departure = (book_id, ch, v, position) in _UXLC_PENDING_CHANGES_APPLIED
    uxlc_text = (
        pending_change_originals[(ch, v, position)] if is_departure else atom_text
    )
    return clc_note.ClcNote(
        book=book_id,
        ch=ch,
        v=v,
        atom_index=position,
        atom_text=atom_text,
        note_code=code,
        # The real tanach.us prose, or a bare placeholder if the page is not yet
        # downloaded -- never an invented per-code gloss (issue UXLC-utils#19).
        note_text=page_prose or _NOT_YET_DOWNLOADED,
        source=clc_note.SOURCE_UXLC_X_NOTE,
        diff_type=(
            clc_note.DIFF_UXLC_PENDING_CHANGE_APPLIED
            if is_departure
            else _diff_type_for(code)
        ),
        is_uxlc_departure=is_departure,
        uxlc_reading=uxlc_text,
        clc_reading=atom_text,
        # Always the real note-page URL: every m/d/t note has one on tanach.us,
        # so even a not-yet-downloaded note links to where its prose lives.
        source_url=my_uxlc.note_page_url(book_id, ch, v, position, code),
        superseding_uxlc_change=_NOTES_SUPERSEDED_BY_UXLC_CHANGE.get(
            (book_id, ch, v, position, code), ()
        ),
    )


def _diff_type_for(code):
    """Classify a surfaced <x> note for the §7.9 index.

    Only the genuinely under-bar codes (m/d) are ``under-bar``; the catch-all t is
    general transcription-uncertainty, not a sub-letter mark (design doc §2, issue
    UXLC-utils#18). All notes are still ``is_uxlc_departure=False`` in the skeleton.
    """
    if code in UNDER_BAR_CODES:
        return clc_note.DIFF_UNDER_BAR
    return clc_note.DIFF_TRANSCRIPTION_UNCERTAINTY


def _check_atom_consistency(book_id, ch, v, position, atom_text, records):
    """Backup guard for the fragile position-based join (see clc_changes).

    The integer position is the join key; the letter-only atom text is the
    backup. Every change cited at this position recorded the word(s) then
    present, so the current atom should match one of them (a ketiv/qere pair
    contributes both members). If it matches none, the atomization has drifted
    (atoms merged or split) and the position no longer means what the change log
    meant — we fail loudly rather than silently mislabel the atom. Reviewed
    exceptions that are not merges/splits live in _KNOWN_ATOM_MISMATCHES.
    """
    expected = {r["letters"] for r in records if r["letters"]}
    if not expected:
        return  # no recorded letters to verify against
    actual = hl.letters(atom_text)
    if actual in expected:
        return
    accepted = (book_id, ch, v, position) in _KNOWN_ATOM_MISMATCHES
    assert accepted, (
        f"CLC atom/change-log mismatch at {book_id} {ch}:{v}.{position}: atom "
        f"letters {actual!r} match none of the change-log letters "
        f"{sorted(expected)!r}. Either atom positions shifted (atoms merged or "
        "split) since the notes were recorded, or the change log's recorded text "
        "differs from current UXLC at this position. If reviewed and acceptable, "
        "add (book, ch, v, position) to _KNOWN_ATOM_MISMATCHES."
    )
