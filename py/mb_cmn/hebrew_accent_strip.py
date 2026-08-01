"""Strip a Hebrew token down to letters, accents, and the
accent-coupled punctuation (maqaf, sof pasuq, legarmeh) — dropping vowel points,
dagesh, shin/sin dots, rafe, and (per policy) meteg.

This is the reusable kernel for "keep only what carries the cantillation signal"
displays. wlc-utils has a near-identical private ``_sanitize_hebrew_token`` in
``accgram/hebrew_verse_sanitize.py`` (same keep-sets, same silluq-vs-meteg rule)
plus a JSON-payload walker and a MAM stress-helper dedup around it; this module is
the vendorable common core that that code could eventually delegate to. It lives in
the vendorable ``mb_cmn`` namespace and depends only on sibling ``mb_cmn`` constants.
"""

from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpunc

# Hebrew letters block: ALEF (U+05D0) .. TAV (U+05EA), including the final forms.
_LETTER_LO, _LETTER_HI = 0x05D0, 0x05EA
# Accents (te'amim): ETNAHTA (U+0591) .. the last accent (U+05AE).
# The block ends at U+05AE on purpose: U+05AF (MASORA CIRCLE) is an editorial mark,
# not an accent, so it is *not* kept. (U+05BD / meteg-or-silluq sits just past this
# range and is handled separately by the keep_meteg policy below.)
_ACCENT_LO, _ACCENT_HI = 0x0591, 0x05AE

# Accent-coupled punctuation that survives the strip: maqaf, sof pasuq, and the
# paseq/legarmeh glyph (kept as legarmeh — the narrow-sense separating paseq is the
# same codepoint and cannot be told apart here by codepoint alone).
_KEEP_PUNCT = frozenset({hpunc.MAQ, hpunc.SOPA, hpunc.PASOLEG})

# keep_meteg policy for U+05BD (meteg-or-silluq, hp.MTGOSLQ):
#   "none"   — drop every U+05BD (treat all as ordinary meteg)
#   "silluq" — keep only the token's *last* U+05BD (the silluq), drop earlier metegs
#   "all"    — keep every U+05BD
METEG_DROP = "none"
METEG_SILLUQ = "silluq"
METEG_ALL = "all"
_METEG_POLICIES = frozenset({METEG_DROP, METEG_SILLUQ, METEG_ALL})


def strip_to_accents(token, *, keep_meteg=METEG_SILLUQ):
    """Return ``token`` reduced to letters + accents + accent-coupled punctuation.

    ``keep_meteg`` governs U+05BD (see the policy constants above). The default,
    ``METEG_SILLUQ``, keeps only the last U+05BD: correct for a verse-final token,
    where that mark is the silluq (an accent). Pass ``METEG_DROP`` for a token that
    is *not* verse-final, where every U+05BD is an ordinary meteg. The caller owns
    the verse-finality decision (e.g. "does this token carry sof pasuq?") since it
    depends on context this function cannot see.
    """
    if keep_meteg not in _METEG_POLICIES:
        raise ValueError(f"keep_meteg must be one of {sorted(_METEG_POLICIES)}")
    silluq_idx = token.rfind(hp.MTGOSLQ) if keep_meteg == METEG_SILLUQ else -1
    kept = []
    for idx, ch in enumerate(token):
        codepoint = ord(ch)
        if _LETTER_LO <= codepoint <= _LETTER_HI:
            kept.append(ch)  # letter (incl. final form)
        elif _ACCENT_LO <= codepoint <= _ACCENT_HI:
            kept.append(ch)  # accent (te'amim)
        elif ch in _KEEP_PUNCT:
            kept.append(ch)  # maqaf / sof pasuq / legarmeh
        elif ch == hp.MTGOSLQ and (keep_meteg == METEG_ALL or idx == silluq_idx):
            kept.append(ch)  # silluq (an accent) — or every meteg, under METEG_ALL
    return "".join(kept)
