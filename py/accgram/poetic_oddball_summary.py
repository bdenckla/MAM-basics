"""Auto-derive the tentative WLC-vs-MAM-simple summary for one poetic ungrammatical verse.

Split out of ``poetic_oddballs`` (which owns the ungrammatical collection + HTML shell);
this module is just the per-verse summary line shown under each ungrammatical verse.

The summary is computed by aligning the two verses *chanted word by chanted word* -- the
letter skeleton as the key, via the same ``difflib`` engine ``mb_cmn.my_diffs``
wraps for the prose page -- and reporting each chanted word whose divider differs.  This
replaced an earlier diff of the conjunctive-stripped *disjunctive skeletons*, which
dropped every conjunctive and so conflated a divider that merely shifted to the
neighbouring chanted word into a phantom like-for-like substitution (Ps 68:20 / Pr 30:15:
WLC's legarmeh and MAM's oleh-we-yored sit on different chanted words).  The disjunctive
skeleton remains the persisted datum and the table on the page; only the human-
readable summary uses the chanted-word alignment.

CHANTED WORD, NOT ATOM (issue #81).  The unit here is the maqaf compound where there is one
-- Job 31:15's clause names הלא־בבטן whole, never a bare בבטן -- because that is the unit a
divider sits on.  ``_wlc_chanted_words`` builds it by joining each maqaf-terminated atom to
the atom after it; this module said "accent-word" for the same thing before #81.

The WLC side pairs the wlc422 Unicode letters (the shared alignment key, grouped
into chanted words) with the M-C scanner's resolved disjunctives; the MAM side comes
from ``mam_poetic_accents.load_poetic_word_disj``.  When the two WLC views cannot be
reconciled 1:1 the summary falls back to the disjunctive-skeleton diff, flagged as
the weaker comparison.
"""

from __future__ import annotations

import difflib

from accgram.mam_poetic_accents import base_letters
from accgram.poetic_accent_names import POETIC_DISJUNCTIVES
from accgram.poetic_scanner import scan_accents
from mb_cmn import hebrew_punctuation as hpunc


def derive_tentative_summary(row: dict[str, object]) -> str:
    if row["mam_disjunctives"] is None:
        return (
            "Not in MAM-simple, so no disjunctive oracle is available "
            "for comparison."
        )
    if row["wlc_disjunctives"] == row["mam_disjunctives"]:
        return (
            "WLC and MAM-simple agree on the disjunctive skeleton, yet the verse does "
            "not parse — so the anomaly is below the disjunctive skeleton (a conjunctive "
            "or lexical matter), not a disjunctive divergence. This skeleton-level oracle "
            "does not look beneath the skeleton, so it cannot say whether WLC and MAM "
            "diverge there (they may well: e.g. Ps 56:10's extra merkha)."
        )
    clauses = _word_aligned_clauses(row)
    if clauses is None:
        # Chanted-word alignment could not be reconciled (e.g. the WLC chanted-word and
        # wlc422 atom counts disagree); fall back to the conjunctive-stripped
        # skeleton diff, flagged so the reader knows it is the weaker comparison.
        skeleton = _describe_disjunctive_diff(
            row["wlc_disjunctives"], row["mam_disjunctives"]
        )
        return (
            "Relative to the MAM-simple oracle (disjunctive skeleton only — chanted words "
            "could not be aligned), " + "; ".join(skeleton) + "."
        )
    if not clauses:
        return (
            "Aligned chanted word by chanted word, the dividers fall on the same "
            "ones; the skeleton-level difference is an artifact of segmentation, not a "
            "real divergence in which chanted word each divider sits on."
        )
    return "Chanted-word-aligned against MAM-simple, " + "; ".join(clauses) + "."


def _word_aligned_clauses(row: dict[str, object]) -> list[str] | None:
    """Per-chanted-word divider differences between WLC and MAM, or None if unalignable.

    Aligns the two verses *by chanted word* (letter skeleton as the key, the same
    ``difflib`` engine ``mb_cmn.my_diffs`` wraps for the prose page) and reports each
    chanted word whose divider differs.  This replaces the old disjunctive-skeleton diff, which
    dropped every conjunctive and so conflated a divider that merely *shifted to the
    neighbouring chanted word* into a phantom like-for-like substitution (see Ps 68:20 / Pr
    30:15: WLC's legarmeh and MAM's oleh-we-yored sit on different chanted words)."""
    if row["mam_words"] is None:
        return None
    wlc_words = _wlc_chanted_words(row)
    if wlc_words is None:
        return None
    mam_words = [(letters, (d,) if d else ()) for letters, d in row["mam_words"]]

    # The WLC chanted-word strings keep their maqaf for display ("הלא־בבטן"); the MAM side's
    # base_letters drops it, so strip it back out for the alignment key only -- the
    # opcode indices below still address the maqaf-bearing wlc_words for phrasing.
    matcher = difflib.SequenceMatcher(
        a=[letters.replace(hpunc.MAQ, "") for letters, _ in wlc_words],
        b=[letters for letters, _ in mam_words],
        autojunk=False,
    )
    clauses: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                letters, wlc_disj = wlc_words[i1 + k]
                _mam_letters, mam_disj = mam_words[j1 + k]
                if wlc_disj != mam_disj:
                    clauses.append(_phrase_word_diff(letters, wlc_disj, mam_disj))
        else:
            clauses.append(_phrase_segment_diff(wlc_words[i1:i2], mam_words[j1:j2]))
    return clauses


def _wlc_chanted_words(
    row: dict[str, object],
) -> list[tuple[str, tuple[str, ...]]] | None:
    """``(base_letters, disjunctives)`` for the WLC verse, chanted word by chanted
    word: the wlc422 Unicode letters (the shared alignment key) zipped with
    the M-C scanner's resolved disjunctives.  None if the two cannot be reconciled
    1:1 (different chanted-word counts)."""
    letter_words = _wlc_letter_words(row["wlc422_kq_u_verse"])
    if letter_words is None:
        return None
    disj_words = _wlc_disjunctives_per_word(row["body"])
    if len(letter_words) != len(disj_words):
        return None
    return list(zip(letter_words, disj_words))


# Named for what it returns (letters), not for its unit: the unit is the CHANTED word, since
# the loop below joins each maqaf-terminated atom to the atom after it.
def _wlc_letter_words(wlc_verse: object) -> list[str] | None:
    """Group the wlc422 ``vels`` into chanted words and return each one's letters.

    A maqaf-terminated atom joins the atom after it into one chanted word (matching the
    M-C scanner's whitespace-delimited words, since a compound has no space in it); the
    maqaf itself is kept in the returned
    string so a compound displays as "הלא־בבטן" rather than the run-together
    "הלאבבטן" (the alignment key strips it back out -- see _word_aligned_clauses --
    since the MAM side's base_letters drops the maqaf).  Punctuation-only tokens
    (paseq) drop out.  None if the verse carries no ``vels``."""
    if not isinstance(wlc_verse, dict):
        return None
    vels = wlc_verse.get("vels")
    if not isinstance(vels, list):
        return None
    words: list[str] = []
    current = ""
    for token in vels:
        text = _token_text(token)  # a vel may be a {"word", "notes"} dict, not a str
        if not text:
            continue
        letters = base_letters(text)
        if not letters:  # punctuation-only token (paseq, etc.)
            continue
        current += letters
        if hpunc.MAQ in text:  # maqaf joins this atom to the next
            current += hpunc.MAQ
            continue
        words.append(current)
        current = ""
    if current:
        words.append(current)
    return words


def _wlc_disjunctives_per_word(body: str) -> list[tuple[str, ...]]:
    """The M-C scanner's resolved disjunctives, partitioned per chanted word.

    The scanner runs verse-level passes (unmarked-ole recovery, revia
    reclassification) that need context beyond one chanted word, so we keep the whole-verse
    resolved stream and slice it by each chanted word's own token count (the passes relabel
    tokens but never change their count)."""
    resolved = [t for t, _leaf in scan_accents(body)]
    words: list[tuple[str, ...]] = []
    pos = 0
    for mc_word in body.split():
        count = len(scan_accents(mc_word))
        segment = resolved[pos : pos + count]
        pos += count
        words.append(tuple(t for t in segment if t in POETIC_DISJUNCTIVES))
    return words


def _phrase_word_diff(
    letters: str, wlc_disj: tuple[str, ...], mam_disj: tuple[str, ...]
) -> str:
    return (
        f"on {letters}, WLC has {_disj_phrase(wlc_disj)} "
        f"where MAM has {_disj_phrase(mam_disj)}"
    )


def _phrase_segment_diff(
    wlc_seg: list[tuple[str, tuple[str, ...]]],
    mam_seg: list[tuple[str, tuple[str, ...]]],
) -> str:
    """Phrase an insert/delete/replace block: the two witnesses segment the stretch
    differently (e.g. Pr 30:15 WLC ``הב`` vs MAM ``ה ב``), so the dividers there are
    not word-comparable."""
    wlc_part = _phrase_word_list(wlc_seg)
    mam_part = _phrase_word_list(mam_seg)
    if not wlc_seg:
        return f"MAM has {mam_part} with no aligned WLC word"
    if not mam_seg:
        return f"WLC has {wlc_part} with no aligned MAM word"
    return f"WLC segments this stretch as {wlc_part} where MAM has {mam_part}"


def _phrase_word_list(seg: list[tuple[str, tuple[str, ...]]]) -> str:
    return ", ".join(
        letters + (f" [{_humanize_disjunctives(disj)}]" if disj else "")
        for letters, disj in seg
    )


def _disj_phrase(disj: tuple[str, ...]) -> str:
    return _humanize_disjunctives(disj) if disj else "no divider (a conjunctive)"


def _describe_disjunctive_diff(wlc: tuple[str, ...], mam: tuple[str, ...]) -> list[str]:
    """Phrase each edit between the WLC and MAM disjunctive skeletons from WLC's
    side (MAM is the oracle), e.g. "WLC omits silluq that MAM has".  Fallback only
    (see _word_aligned_clauses); the disjunctive-only skeleton drops conjunctives and
    so cannot tell which word each divider sits on."""
    matcher = difflib.SequenceMatcher(a=wlc, b=mam, autojunk=False)
    clauses: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        wlc_part = _humanize_disjunctives(wlc[i1:i2])
        mam_part = _humanize_disjunctives(mam[j1:j2])
        if tag == "delete":
            clauses.append(f"WLC has an extra {wlc_part} not in MAM")
        elif tag == "insert":
            clauses.append(f"WLC omits {mam_part} that MAM has")
        else:  # replace
            clauses.append(f"WLC has {wlc_part} where MAM has {mam_part}")
    return clauses


def _humanize_disjunctives(tokens: tuple[str, ...]) -> str:
    return ", ".join(token.lower().replace("_", " ") for token in tokens)


def _token_text(token: object) -> str:
    """The base text of a wlc422 ``vels`` token, which may be a str or a
    ``{"word", "notes"}`` dict (as several accgram modules each define privately)."""
    if isinstance(token, str):
        return token
    if isinstance(token, dict):
        for key in ("word", "text"):
            value = token.get(key)
            if isinstance(value, str):
                return value
    return ""
