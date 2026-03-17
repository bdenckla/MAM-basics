"""Describe Hebrew text differences in English.

Adapted from mgketer's describe_accent_diff.py and describe_text_diff.py
for use in MPP diff reports.  Produces human-readable descriptions like:

    "revia on tav in old, on lamed in new"
    "meteg on mem removed"
"""

import unicodedata
from collections import Counter
from difflib import SequenceMatcher

# ── Hebrew letter names ──────────────────────────────────────────────

_LETTER_NAMES = {
    "א": "alef",
    "ב": "bet",
    "ג": "gimel",
    "ד": "dalet",
    "ה": "he",
    "ו": "vav",
    "ז": "zayin",
    "ח": "het",
    "ט": "tet",
    "י": "yod",
    "ך": "final-kaf",
    "כ": "kaf",
    "ל": "lamed",
    "ם": "final-mem",
    "מ": "mem",
    "ן": "final-nun",
    "נ": "nun",
    "ס": "samekh",
    "ע": "ayin",
    "ף": "final-pe",
    "פ": "pe",
    "ץ": "final-tsadi",
    "צ": "tsadi",
    "ק": "qof",
    "ר": "resh",
    "ש": "shin",
    "ת": "tav",
}

# ── Hebrew accent names (U+0591–U+05AF) ─────────────────────────────

_ACCENT_NAMES = {
    "\N{HEBREW ACCENT ETNAHTA}": "etnahta",
    "\N{HEBREW ACCENT SEGOL}": "segol-accent",
    "\N{HEBREW ACCENT SHALSHELET}": "shalshelet",
    "\N{HEBREW ACCENT ZAQEF QATAN}": "zaqef-qatan",
    "\N{HEBREW ACCENT ZAQEF GADOL}": "zaqef-gadol",
    "\N{HEBREW ACCENT TIPEHA}": "tipeha",
    "\N{HEBREW ACCENT REVIA}": "revia",
    "\N{HEBREW ACCENT ZARQA}": "zarqa-sh",
    "\N{HEBREW ACCENT PASHTA}": "pashta",
    "\N{HEBREW ACCENT YETIV}": "yetiv",
    "\N{HEBREW ACCENT TEVIR}": "tevir",
    "\N{HEBREW ACCENT GERESH}": "geresh",
    "\N{HEBREW ACCENT GERESH MUQDAM}": "geresh-muqdam",
    "\N{HEBREW ACCENT GERSHAYIM}": "gershayim",
    "\N{HEBREW ACCENT QARNEY PARA}": "qarney-para",
    "\N{HEBREW ACCENT TELISHA GEDOLA}": "telisha-gedola",
    "\N{HEBREW ACCENT PAZER}": "pazer",
    "\N{HEBREW ACCENT ATNAH HAFUKH}": "atnah-hafukh",
    "\N{HEBREW ACCENT MUNAH}": "munah",
    "\N{HEBREW ACCENT MAHAPAKH}": "mahapakh",
    "\N{HEBREW ACCENT MERKHA}": "merkha",
    "\N{HEBREW ACCENT MERKHA KEFULA}": "merkha-kefula",
    "\N{HEBREW ACCENT DARGA}": "darga",
    "\N{HEBREW ACCENT QADMA}": "qadma",
    "\N{HEBREW ACCENT TELISHA QETANA}": "telisha-qetana",
    "\N{HEBREW ACCENT YERAH BEN YOMO}": "yerakh-ben-yomo",
    "\N{HEBREW ACCENT OLE}": "ole",
    "\N{HEBREW ACCENT ILUY}": "iluy",
    "\N{HEBREW ACCENT DEHI}": "dehi",
    "\N{HEBREW ACCENT ZINOR}": "zarqa",
    "\N{HEBREW MARK MASORA CIRCLE}": "masora-circle",
}

# ── Hebrew mark names (vowels, dagesh, meteg, rafe, shin/sin dots) ──

_MARK_NAMES = {
    "\N{HEBREW POINT SHEVA}": "shva",
    "\N{HEBREW POINT HATAF SEGOL}": "hataf-segol",
    "\N{HEBREW POINT HATAF PATAH}": "hataf-patah",
    "\N{HEBREW POINT HATAF QAMATS}": "hataf-qamats",
    "\N{HEBREW POINT HIRIQ}": "hiriq",
    "\N{HEBREW POINT TSERE}": "tsere",
    "\N{HEBREW POINT SEGOL}": "segol",
    "\N{HEBREW POINT PATAH}": "patah",
    "\N{HEBREW POINT QAMATS}": "qamats",
    "\N{HEBREW POINT HOLAM}": "holam",
    "\N{HEBREW POINT HOLAM HASER FOR VAV}": "holam-haser-for-vav",
    "\N{HEBREW POINT QUBUTS}": "qubuts",
    "\N{HEBREW POINT DAGESH OR MAPIQ}": "dagesh",
    "\N{HEBREW POINT METEG}": "meteg",
    "\N{HEBREW POINT RAFE}": "rafe",
    "\N{HEBREW POINT SHIN DOT}": "shin-dot",
    "\N{HEBREW POINT SIN DOT}": "sin-dot",
    "\N{HEBREW POINT JUDEO-SPANISH VARIKA}": "varika",
}


# ── Character predicates ─────────────────────────────────────────────


def _is_letter(ch):
    return 0x05D0 <= ord(ch) <= 0x05EA


def _is_accent(ch):
    return 0x0591 <= ord(ch) <= 0x05AF


def _is_mark(ch):
    cp = ord(ch)
    return (
        (0x05B0 <= cp <= 0x05BD)
        or cp == 0x05BF
        or cp in (0x05C1, 0x05C2)
        or cp == 0xFB1E
    )


def _letter_name(ch):
    return _LETTER_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


_POETIC_ACCENT_NAMES = {
    "\N{HEBREW ACCENT TIPEHA}": "tarha",
    "\N{HEBREW ACCENT ZARQA}": "tsinnorit",
    "\N{HEBREW ACCENT ZINOR}": "tsinnor",
}

# Names that should get an HTML tooltip (<abbr title="...">) in rendered output.
# Keys are the display name (as returned by _accent_name); values are the tooltip.
_NAME_TOOLTIPS = {
    "zarqa-sh": "zarqa stress helper",
}


def _accent_name(ch, poetic=False):
    if poetic:
        name = _POETIC_ACCENT_NAMES.get(ch)
        if name:
            return name
    return _ACCENT_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


def _mark_name(ch):
    return _MARK_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


# ── Qualify marks/accents with their preceding letter ────────────────


def _qualify(text, pred):
    """Return [(char, letter)] for each char in text matching pred."""
    result = []
    letter = None
    for ch in text:
        if _is_letter(ch):
            letter = ch
        elif pred(ch) and letter is not None:
            result.append((ch, letter))
    return result


# ── Core diff description logic ──────────────────────────────────────


def _describe_diff(old_text, new_text, pred, name_fn, poetic=False):
    """Generic diff description for marks or accents.

    pred: function that identifies the character type (accent or mark)
    name_fn: function that returns the human name for the character
    poetic: if True, use poetic accent names (e.g. tarha for tipeha)
    """
    if poetic and name_fn is _accent_name:
        _name = lambda ch: _accent_name(ch, poetic=True)
    else:
        _name = name_fn
    old_qualified = _qualify(old_text, pred)
    new_qualified = _qualify(new_text, pred)

    # Pure reorder: same items in a different order on the same letter
    if (
        Counter(old_qualified) == Counter(new_qualified)
        and old_qualified != new_qualified
    ):
        start = 0
        while old_qualified[start] == new_qualified[start]:
            start += 1
        end = len(old_qualified) - 1
        while old_qualified[end] == new_qualified[end]:
            end -= 1
        region = old_qualified[start : end + 1]
        letters = {l for _, l in region}
        if len(letters) == 1:
            names = [_name(a) for a, _ in region]
            order_word = "opposite" if len(names) == 2 else "different"
            return (
                f"{','.join(names)} in old" f" appears in the {order_word} order in new"
            )

    sm = SequenceMatcher(None, old_qualified, new_qualified, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]

    if not ops:
        return None

    deletes = []
    inserts = []
    descriptions = []

    for tag, i1, i2, j1, j2 in ops:
        old_chunk = old_qualified[i1:i2]
        new_chunk = new_qualified[j1:j2]

        if tag == "replace" and len(old_chunk) == 1 and len(new_chunk) == 1:
            o_mark, o_let = old_chunk[0]
            n_mark, n_let = new_chunk[0]
            if o_mark == n_mark:
                # Same mark, different letter → moved
                descriptions.append(
                    f"{_name(o_mark)} on {_letter_name(o_let)}"
                    f" in old, on {_letter_name(n_let)} in new"
                )
            elif o_let == n_let:
                # Same letter, different mark → replaced
                descriptions.append(
                    f"on {_letter_name(o_let)}, "
                    f"{_name(o_mark)} in old \u2192 "
                    f"{_name(n_mark)} in new"
                )
            else:
                descriptions.append(
                    f"{_name(o_mark)} on {_letter_name(o_let)}"
                    f" (old) \u2192 {_name(n_mark)} on "
                    f"{_letter_name(n_let)} (new)"
                )
        elif tag == "delete":
            for mark, let in old_chunk:
                deletes.append((mark, let))
        elif tag == "insert":
            for mark, let in new_chunk:
                inserts.append((mark, let))
        else:
            # Complex replace — fall back to generic description
            old_parts = ", ".join(
                f"{_name(m)} on {_letter_name(l)}" for m, l in old_chunk
            )
            new_parts = ", ".join(
                f"{_name(m)} on {_letter_name(l)}" for m, l in new_chunk
            )
            descriptions.append(f"old has {old_parts}; new has {new_parts}")

    # Pair delete/insert of same mark as moves
    used_inserts = set()
    for d_mark, d_let in deletes:
        paired = False
        for idx, (i_mark, i_let) in enumerate(inserts):
            if idx not in used_inserts and i_mark == d_mark:
                descriptions.append(
                    f"{_name(d_mark)} on {_letter_name(d_let)}"
                    f" in old, on {_letter_name(i_let)} in new"
                )
                used_inserts.add(idx)
                paired = True
                break
        if not paired:
            descriptions.append(f"{_name(d_mark)} on {_letter_name(d_let)} removed")
    for idx, (i_mark, i_let) in enumerate(inserts):
        if idx not in used_inserts:
            descriptions.append(f"{_name(i_mark)} on {_letter_name(i_let)} added")

    return "; ".join(descriptions) if descriptions else None


# ── Poetic verse detection ───────────────────────────────────────────

_POETIC_BOOKS = {"Psalms", "Proverbs", "Job"}


def _is_prose_section_of_job(chapter, verse):
    if chapter in (1, 2):
        return True
    if chapter == 3 and verse < 2:
        return True
    if chapter == 42 and verse > 6:
        return True
    return False


def _is_poetic(book, chapter, verse):
    if book not in _POETIC_BOOKS:
        return False
    if book == "Job":
        return not _is_prose_section_of_job(chapter, verse)
    return True


# ── Public API ───────────────────────────────────────────────────────

_ACCENT_CATS = {"accent-change", "accent-addition", "accent-removal"}
_MARK_CATS = {
    "meteg-removal",
    "meteg-addition",
    "vowel-change",
    "rafe-reuveni",
    "varika",
}


_PASEQ = "\u05c0"
_LEG_SENTINEL = "\ufdd0"
_NAR_SENTINEL = "\ufdd1"


def _has_paseq(text):
    return _PASEQ in text or _LEG_SENTINEL in text or _NAR_SENTINEL in text


def _describe_paseq_change(old_text, new_text):
    if not _has_paseq(old_text) and _has_paseq(new_text):
        return "add legarmeh"
    if _has_paseq(old_text) and not _has_paseq(new_text):
        return "remove legarmeh"
    return None


def _describe_maqaf_afor(old_text, new_text):
    old_spaces = old_text.count(" ")
    new_spaces = new_text.count(" ")
    if old_spaces > new_spaces:
        return "add gray maqaf"
    if new_spaces > old_spaces:
        return "remove gray maqaf"
    return None


def describe_change(old_text, new_text, category, book, chapter, verse):
    """Return an English description of the change, or None."""
    poetic = _is_poetic(book, chapter, verse)
    if category == "maqaf-afor":
        return _describe_maqaf_afor(old_text, new_text)
    if category == "legarmeih-paseq":
        return _describe_paseq_change(old_text, new_text)
    if category in _ACCENT_CATS:
        return _describe_diff(old_text, new_text, _is_accent, _accent_name, poetic)
    if category in _MARK_CATS:
        return _describe_diff(old_text, new_text, _is_mark, _mark_name, poetic)
    # For misc, try accents first, then marks
    if category == "misc":
        desc = _describe_diff(old_text, new_text, _is_accent, _accent_name, poetic)
        if desc:
            return desc
        return _describe_diff(old_text, new_text, _is_mark, _mark_name, poetic)
    return None


def add_name_tooltips(html_escaped_desc):
    """Wrap names that have tooltips with <abbr> tags.

    Must be called AFTER HTML-escaping the description, since the name
    strings contain no HTML special characters.
    """
    result = html_escaped_desc
    for name, tip in _NAME_TOOLTIPS.items():
        result = result.replace(name, f'<abbr title="{tip}">{name}</abbr>')
    return result
