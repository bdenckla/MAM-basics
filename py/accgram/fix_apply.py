"""Apply a MAM-simple fix to a WLC verse at the Unicode-word level, for re-testing.

The fix-tester wants to ask: *if we adopt the MAM-simple value here, does the
ungrammatical clear?*  The fix is a Unicode word-diff (``diff_wlc_mam``) and the scanner
reads a Unicode mark body, so this module bridges the two the
direct way (issue #9): it locates the single changed word in the verse's
``vels`` by index-aligning to the WLC word tokens, substitutes the MAM Unicode word
in place (keeping the surrounding structure -- ketiv-qere wrappers, ``notes``,
section markers), and re-transcodes the modified verse to a mark body
(``uni_to_marks``) for re-scanning.  No accent-name->code bridge is involved; the
transcoder owns the helper/main split and every mark emission.

An adjacent run of words (a multi-word ``wlc_focus``) is substituted word by word.
A change the grammar cannot see -- a vowel- or medial-meteg-only edit -- is returned
as an ``UntestableFix`` (it would re-transcode to the same body), as is a non-adjacent /
mismatched-count multi-word diff or a word/atom misalignment.  Nothing is guessed.

An accent that *moves* to a different letter (je 44:17: a telisha qetanna shifting from
the kaf to the yod) keeps the per-word accent multiset but is grammar-visible -- it is
exactly what ``lexical_validation`` keys on -- so it is treated as a real, testable
change: the whole-word substitution carries the mark to its new letter and the
re-transcoded body re-scans with the move applied (``AppliedFix.moved_accents`` records
the from/to letters for the report).
"""

from __future__ import annotations

import copy
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass

from accgram import uni_to_marks
from mb_cmn import uni_heb

# A Hebrew letter (used to tell a real word token from punctuation/markers).
_HEB_LETTER_RE = re.compile(r"[א-ת]")
# Sof pasuq punctuation (U+05C3).  A MAM value that merely adds it is the "missing
# sof pasuq" fix -- grammar-visible (the transcoder emits 00, the scanner terminates).
_SOF_PASUQ = "׃"

# Accent abbreviations as ``uni_heb.accent_names`` returns them.  ``(mos)`` is the
# meteg/silluq glyph (U+05BD); a *medial* meteg difference is invisible to the
# grammar, so it is stripped before diffing.  ``(sil)`` is the synthetic verse-final
# silluq promoted from a ``(mos)`` that lands on a sof-pasuq-bearing word.
_MOS_ABBREV = "(mos)"
_SILLUQ_ABBREV = "(sil)"


@dataclass(frozen=True)
class AppliedFix:
    new_body: str  # the re-transcoded M-C body to re-scan
    word_index: int  # index (in wlc_words) of the first *changed* word
    old_word: str  # the WLC Unicode word (first, for a multi-word focus)
    new_word: str  # the MAM Unicode word it was replaced with
    removed_accents: tuple[str, ...]  # accent abbreviations, WLC side
    added_accents: tuple[str, ...]  # accent abbreviations, MAM side
    # Pre-formatted descriptions of any accent that *moved* to a different letter
    # (same accent multiset, different skeleton -- je 44:17's telisha qetanna shifting
    # from the kaf to the yod).  Empty unless this fix is a pure/partial move.
    moved_accents: tuple[str, ...] = ()
    # Pre-formatted transform descriptions for any *additional* changed words in a
    # multi-word (adjacent wlc_focus) splice; empty for the common single-word case.
    extra_transforms: tuple[str, ...] = ()

    def transformation(self) -> str:
        # A pure accent move has empty removed/added multisets; describe it as a move
        # rather than "(none) -> (none)".
        if self.moved_accents and not self.removed_accents and not self.added_accents:
            inner = "; ".join(self.moved_accents)
            base = f'word "{self.old_word}" -> "{self.new_word}" ({inner})'
        else:
            rm = " ".join(self.removed_accents) or "(none)"
            ad = " ".join(self.added_accents) or "(none)"
            base = f'word "{self.old_word}" -> "{self.new_word}" ({rm} -> {ad})'
            if self.moved_accents:
                base = f"{base} [moved: {'; '.join(self.moved_accents)}]"
        if self.extra_transforms:
            return "; ".join((base, *self.extra_transforms))
        return base


@dataclass(frozen=True)
class UntestableFix:
    reason: str  # machine code, see module docstring
    detail: str = ""


def apply_mam_fix(
    verse: object,
    wlc_words: list[str],
    diff_entry: object,
) -> AppliedFix | UntestableFix:
    """Substitute the MAM value of ``diff_entry`` into ``verse`` and re-transcode.

    ``verse`` is the raw ``-kq-u`` verse (``{vels: [...]}``); ``wlc_words`` is its WLC
    word list (``verse_words`` of the display verse), used to locate the changed
    word(s) by index.  A ``wlc_focus``-expanded entry may carry several *adjacent*
    words on each side (space-joined); the substitution then replaces each word's vel
    in place.  The common case is a single word.
    """
    wlc_word = _diff_side_word(diff_entry, "wlc422")
    mam_word = _diff_side_word(diff_entry, "mam_simple")
    if wlc_word is _MULTI or mam_word is _MULTI:
        return UntestableFix("multi_word", "diff spans more than one word")
    if not isinstance(wlc_word, str) or not isinstance(mam_word, str):
        return UntestableFix("bad_diff_shape", repr(diff_entry))

    wlc_tokens = wlc_word.split()
    mam_tokens = mam_word.split()
    if len(wlc_tokens) != len(mam_tokens):
        return UntestableFix(
            "multi_word",
            f"diff word counts differ ({len(wlc_tokens)} vs {len(mam_tokens)})",
        )
    if not wlc_tokens:
        return UntestableFix("bad_diff_shape", "empty diff word")

    # --- grammar visibility gate (per word) ---
    removed_first: list[str] = []
    added_first: list[str] = []
    moved_first: list[str] = []
    extra_transforms: list[str] = []
    any_visible = False
    for offset, (wlc_tok, mam_tok) in enumerate(zip(wlc_tokens, mam_tokens)):
        removed, added = _accent_name_diff(wlc_tok, mam_tok)
        sof_added = _SOF_PASUQ in mam_tok and _SOF_PASUQ not in wlc_tok
        if sof_added:
            added = [*added, "(sof pasuq)"]
        # An accent that moves to a different letter keeps the name multiset (so the
        # name diff is empty) yet IS grammar-visible (je 44:17: lexical_validation keys
        # on which letter the telisha qetanna sits on).  Treat such a move as visible.
        moved = _accent_moves(wlc_tok, mam_tok)
        if removed or added or moved:
            any_visible = True
        if offset == 0:
            removed_first, added_first, moved_first = removed, added, moved
        elif removed or added or moved:
            rm = " ".join(removed) or "(none)"
            ad = " ".join(added) or "(none)"
            if moved and not removed and not added:
                desc = "; ".join(moved)
            else:
                desc = f"{rm} -> {ad}"
                if moved:
                    desc = f"{desc} [moved: {'; '.join(moved)}]"
            extra_transforms.append(f'word "{wlc_tok}" -> "{mam_tok}" ({desc})')
    if not any_visible:
        # The per-word accent-name multiset is unchanged AND every accent sits on the
        # same letter as before, so the change is a vowel- or (medial) meteg-only edit:
        # truly invisible to the grammar (the scanner swallows vowels and meteg).  A
        # mark that *moved* letters (je 44:17) is handled above as visible and falls
        # through to the substitution path below.
        reason = _no_accent_change_reason(wlc_tokens, mam_tokens)
        return UntestableFix(reason, _NO_CHANGE_MESSAGE[reason])

    # --- locate the changed run, by index, in the WLC word list ---
    span = len(wlc_tokens)
    starts = [
        i
        for i in range(len(wlc_words) - span + 1)
        if wlc_words[i : i + span] == wlc_tokens
    ]
    if not starts:
        return UntestableFix("alignment_failure", f"WLC run {wlc_tokens!r} not in vels")
    if len(starts) > 1:
        return UntestableFix("ambiguous_word", f"WLC run {wlc_tokens!r} not unique")
    start = starts[0]

    # --- substitute the MAM word(s) into a copy of the verse and re-transcode ---
    new_verse = copy.deepcopy(verse)
    setters = _word_unit_setters(new_verse)
    if len(setters) != len(wlc_words):
        return UntestableFix(
            "alignment_failure",
            f"{len(setters)} verse word-units vs {len(wlc_words)} WLC words",
        )
    for offset in range(span):
        setters[start + offset](mam_tokens[offset])
    new_body = uni_to_marks.verse_to_marks(new_verse)

    return AppliedFix(
        new_body=new_body,
        word_index=start,
        old_word=wlc_tokens[0],
        new_word=mam_tokens[0],
        removed_accents=tuple(removed_first),
        added_accents=tuple(added_first),
        moved_accents=tuple(moved_first),
        extra_transforms=tuple(extra_transforms),
    )


def verse_words(wlc_verse: object) -> list[str]:
    """Return the WLC verse's word tokens (those carrying a Hebrew letter)."""
    if not isinstance(wlc_verse, dict):
        return []
    vels = wlc_verse.get("vels")
    if not isinstance(vels, list):
        return []
    words: list[str] = []
    for token in vels:
        text = _token_text(token)
        if text is not None and _HEB_LETTER_RE.search(text):
            words.append(text)
    return words


# --- helpers -----------------------------------------------------------------

_MULTI = object()  # sentinel: a diff side that is a multi-word list


def _token_text(token: object) -> str | None:
    if isinstance(token, str):
        return token
    if isinstance(token, dict):
        for key in ("word", "text"):
            value = token.get(key)
            if isinstance(value, str):
                return value
    return None


def _diff_side_word(diff_entry: object, key: str) -> object:
    if not isinstance(diff_entry, dict):
        return None
    value = diff_entry.get(key)
    if isinstance(value, list):
        if len(value) != 1:
            return _MULTI
        value = value[0]
    return _token_text(value)


def _accent_name_diff(wlc_word: str, mam_word: str) -> tuple[list[str], list[str]]:
    """The accents the fix removes vs adds, by abbreviation.

    Used only as the grammar-visibility gate and for the human-readable transform
    description; the actual fix is the whole-word substitution.  A *medial* meteg
    (``(mos)``) is stripped from both sides (invisible to the grammar), but a
    ``(mos)`` that *replaces* a real accent on a sof-pasuq-bearing word -- or is added
    to a sof-pasuq word that carried no silluq -- is the verse-final silluq, a real
    grammar-visible accent, so it is promoted to ``(sil)``.
    """
    wlc_accs = Counter(uni_heb.accent_names(wlc_word))
    mam_accs = Counter(uni_heb.accent_names(mam_word))
    wlc_mos = wlc_accs.pop(_MOS_ABBREV, 0)
    mam_mos = mam_accs.pop(_MOS_ABBREV, 0)
    removed = list((wlc_accs - mam_accs).elements())
    added = list((mam_accs - wlc_accs).elements())
    if mam_mos and not added and _SOF_PASUQ in mam_word and (removed or wlc_mos == 0):
        added.append(_SILLUQ_ABBREV)
    return removed, added


_NO_CHANGE_MESSAGE = {
    "vowel_only": "no accent/punctuation difference -- invisible to the grammar",
    "meteg_only": "no accent/punctuation difference -- invisible to the grammar",
}


def _accent_associations(word: str) -> list[tuple[str, str | None]]:
    """Each real accent paired with the base letter it sits on, in document order.

    The base letter is the most recent one preceding the mark (``None`` if a word
    somehow opens with an accent).  Vowels, points and meteg are ignored.
    """
    associations: list[tuple[str, str | None]] = []
    current: str | None = None
    for char in word:
        if uni_to_marks.is_base_letter(char):
            current = char
        elif uni_to_marks.is_accent(char):
            associations.append((char, current))
    return associations


def _accent_moves(wlc_word: str, mam_word: str) -> list[str]:
    """Descriptions of every accent that *moved* to a different letter.

    The two words share an accent multiset (the name diff is empty) but an accent's
    letter changed -- je 44:17's telisha qetanna shifting from the kaf to the yod.
    Pairs each removed ``(accent, letter)`` with an added one of the same accent and
    formats it ``"telisha qetana: kaf -> yod"``; only genuine moves (the accent stays,
    only its letter changes) are reported, so a vowel/meteg-only edit yields none.
    """
    wlc_assoc = Counter(_accent_associations(wlc_word))
    mam_assoc = Counter(_accent_associations(mam_word))
    removed = list((wlc_assoc - mam_assoc).elements())
    added = list((mam_assoc - wlc_assoc).elements())
    moves: list[str] = []
    for accent, from_letter in removed:
        match = next((i for i, (acc, _) in enumerate(added) if acc == accent), None)
        if match is None:
            continue
        _, to_letter = added.pop(match)
        if to_letter == from_letter:
            continue
        moves.append(
            f"{_accent_label(accent)}: "
            f"{_letter_label(from_letter)} -> {_letter_label(to_letter)}"
        )
    return moves


def _accent_label(char: str) -> str:
    """A readable accent name, e.g. ``"telisha qetana"`` (the unicode name minus its
    ``HEBREW ACCENT`` prefix), falling back to the codepoint if unnamed."""
    name = unicodedata.name(char, "")
    return name.removeprefix("HEBREW ACCENT ").lower() if name else f"U+{ord(char):04X}"


def _letter_label(char: str | None) -> str:
    """A readable base-letter name, e.g. ``"kaf"`` (the unicode name minus its
    ``HEBREW LETTER`` prefix)."""
    if char is None:
        return "(word start)"
    name = unicodedata.name(char, "")
    return name.removeprefix("HEBREW LETTER ").lower() if name else f"U+{ord(char):04X}"


def _no_accent_change_reason(wlc_tokens: list[str], mam_tokens: list[str]) -> str:
    """Classify a grammar-inert change the accent-name multiset cannot see.

    Reached only when the accent-name diff is empty *and* no accent moved to a different
    letter (an accent move is grammar-visible -- je 44:17 -- and is handled by the
    substitution path before we get here).  What remains is a niqqud-only edit or a
    *medial* meteg-only edit, both invisible to the grammar; we label which.
    """
    wlc_mos = sum(Counter(uni_heb.accent_names(w))[_MOS_ABBREV] for w in wlc_tokens)
    mam_mos = sum(Counter(uni_heb.accent_names(w))[_MOS_ABBREV] for w in mam_tokens)
    return "meteg_only" if wlc_mos != mam_mos else "vowel_only"


def _word_unit_setters(verse: object):
    """Setters for each word-bearing unit in ``verse['vels']``, in WLC word order.

    Each setter replaces one word's Unicode text in place (preserving any ``notes``
    and the ketiv-qere wrapper), so the list is 1:1 with ``verse_words`` of the
    display verse: maqaf-joined sub-words are separate vels (hence separate units),
    ketiv-qere descends into the qere side, and lone section markers contribute none.
    """
    setters: list = []
    vels = verse.get("vels") if isinstance(verse, dict) else None
    if not isinstance(vels, list):
        return setters
    _collect_unit_setters(vels, setters)
    return setters


def _collect_unit_setters(container: list, setters: list) -> None:
    """Append a setter for every word-bearing unit reachable from ``container`` (a
    vels list, or a qere list inside a ketiv-qere wrapper), in order."""
    for index, vel in enumerate(container):
        if isinstance(vel, str):
            if _HEB_LETTER_RE.search(vel):
                setters.append(
                    lambda new_word, c=container, i=index: c.__setitem__(i, new_word)
                )
            continue
        if not isinstance(vel, dict):
            continue
        kq = vel.get("kq")
        if isinstance(kq, (list, tuple)) and len(kq) == 2 and isinstance(kq[1], list):
            _collect_unit_setters(kq[1], setters)
            continue
        word = vel.get("word")
        if isinstance(word, str) and _HEB_LETTER_RE.search(word):
            setters.append(lambda new_word, d=vel: d.__setitem__("word", new_word))
