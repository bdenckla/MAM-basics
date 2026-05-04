"""Describe Hebrew text differences in English.

Adapted from mgketer's describe_accent_diff.py and describe_text_diff.py
for use in MAM-parsed-plus diff reports.  Produces human-readable descriptions like:

    "revia on tav in old, on lamed in new"
    "meteg on mem removed"
"""

import unicodedata
from collections import Counter
from difflib import SequenceMatcher

from mb_cmn import hebrew_accents as ha
from mb_cmn import retired_kq_special_templates as rkqst
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn.str_defs import DOUB_VERT_LINE
from mb_diff_mpu.mpplus_flatten import (
    is_ketiv_velo_qere_template,
    is_parashah_template,
    is_qere_velo_ketiv_template,
    is_std_kq_template,
    is_trivial_kq_template,
)
from mb_diff_mpu.mpplus_param_access import MISSING, get_param


def _single_string_param(raw_value, param_name):
    if isinstance(raw_value, str):
        return raw_value
    if isinstance(raw_value, list):
        assert len(raw_value) == 1 and isinstance(raw_value[0], str), (
            param_name,
            raw_value,
        )
        return raw_value[0]
    assert False, (param_name, raw_value)


def _validate_special_kq_if_needed(tmpl):
    name = tmpl["tmpl_name"]
    if not rkqst.is_special_kq_template_name(name):
        return
    sug_raw = get_param(tmpl, "סוג")
    sug_text = None if sug_raw is MISSING else _single_string_param(sug_raw, "סוג")
    rkqst.canonical_special_kq_type_from_name_and_sug(name, sug_text)


# ── Hebrew letter names ──────────────────────────────────────────────

LETTER_NAMES = {
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

ACCENT_NAMES = {
    ha.ATN: "etnahta",
    ha.SEG_A: "segol-accent",
    ha.SHA: "shalshelet",
    ha.ZAQ_Q: "zaqef-qatan",
    ha.ZAQ_G: "zaqef-gadol",
    ha.TIP: "tipeha",
    ha.REV: "revia",
    ha.ZSH_OR_TSIT: "zarqa-sh",
    ha.PASH: "pashta",
    ha.YET: "yetiv",
    ha.TEV: "tevir",
    ha.GER: "geresh",
    ha.GER_M: "geresh-muqdam",
    ha.GER_2: "gershayim",
    ha.QAR: "qarney-para",
    ha.TEL_G: "telisha-gedola",
    ha.PAZ: "pazer",
    ha.ATN_H: "atnah-hafukh",
    ha.MUN: "munah",
    ha.MAH: "mahapakh",
    ha.MER: "merkha",
    ha.MER_2: "merkha-kefula",
    ha.DAR: "darga",
    ha.QOM: "qadma",
    ha.TEL_Q: "telisha-qetana",
    ha.YBY: "yerakh-ben-yomo",
    ha.OLE: "ole",
    ha.ILU: "iluy",
    ha.DEX: "dehi",
    ha.Z_OR_TSOR: "zarqa",
    hpu.MCIRC: "masora-circle",
}

# ── Hebrew mark names (vowels, dagesh, meteg, rafeh, shin/sin dots) ──

POINT_NAMES = {
    hpo.SHEVA: "shewa",
    hpo.XSEGOL: "ḥataf-segol",
    hpo.XPATAX: "ḥataf-pataḥ",
    hpo.XQAMATS: "ḥataf-qamats",
    hpo.XIRIQ: "ḥiriq",
    hpo.TSERE: "tsere",
    hpo.SEGOL_V: "segol",
    hpo.PATAX: "pataḥ",
    hpo.QAMATS: "qamats",
    hpo.QAMATS_Q: "qamats-qatan",
    hpo.XOLAM: "ḥolam",
    hpo.XOLAM_XFV: "ḥolam-ḥaser-for-vav",
    hpo.QUBUTS: "qubuts",
    hpo.DAGOMOSD: "dagesh",
    hpo.MTGOSLQ: "meteg",
    hpo.RAFE: "rafeh",
    hpo.SHIND: "shin-dot",
    hpo.SIND: "sin-dot",
    hpo.VARIKA: "varika",
}


# ── Character predicates ─────────────────────────────────────────────


def is_letter(ch):
    return 0x05D0 <= ord(ch) <= 0x05EA


def is_accent(ch):
    return 0x0591 <= ord(ch) <= 0x05AF


def is_mark(ch):
    cp = ord(ch)
    return (
        (0x05B0 <= cp <= 0x05BD)
        or cp == 0x05BF
        or cp in (0x05C1, 0x05C2, 0x05C7)
        or cp == 0xFB1E
    )


def letter_name(ch):
    return LETTER_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


def ordinal(n):
    if 10 <= (n % 100) <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def letter_ref(ch, occurrence, letter_counts, force_ordinal=False):
    name = letter_name(ch)
    if force_ordinal and letter_counts.get(ch, 0) > 1:
        return f"{ordinal(occurrence)} {name}"
    return name


POETIC_ACCENTS = {
    ha.TIP: "tarha",
    ha.ZSH_OR_TSIT: "tsinnorit",
    ha.Z_OR_TSOR: "tsinnor",
}

# Names that should get an HTML tooltip (<abbr title="...">) in rendered output.
# Keys are the display name (as returned by accent_name); values are the tooltip.
_NAME_TOOLTIPS = {
    "zarqa-sh": "zarqa stress helper",
}


def accent_name(ch, poetic=False):
    if poetic:
        name = POETIC_ACCENTS.get(ch)
        if name:
            return name
    return ACCENT_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


def mark_name(ch):
    return POINT_NAMES.get(ch, unicodedata.name(ch, f"U+{ord(ch):04X}"))


# ── Qualify marks/accents with their preceding letter ────────────────


def qualify(text, pred):
    """Return [(char, letter, letter-occurrence)] for matching chars."""
    result = []
    letter = None
    letter_occurrence = 0
    seen_letters = Counter()
    for ch in text:
        if is_letter(ch):
            letter = ch
            seen_letters[ch] += 1
            letter_occurrence = seen_letters[ch]
        elif pred(ch) and letter is not None:
            result.append((ch, letter, letter_occurrence))
    return result


# ── Core diff description logic ──────────────────────────────────────


def _describe_diff(old_text, new_text, pred, name_fn, poetic=False):
    """Generic diff description for marks or accents.

    pred: function that identifies the character type (accent or mark)
    name_fn: function that returns the human name for the character
    poetic: if True, use poetic accent names (e.g. tarha for tipeha)
    """
    if poetic and name_fn is accent_name:
        _name = lambda ch: accent_name(ch, poetic=True)
    else:
        _name = name_fn
    old_letter_counts = Counter(ch for ch in old_text if is_letter(ch))
    new_letter_counts = Counter(ch for ch in new_text if is_letter(ch))
    old_qualified = qualify(old_text, pred)
    new_qualified = qualify(new_text, pred)

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
        letters = {l for _, l, _ in region}
        if len(letters) == 1:
            names = [_name(a) for a, _, _ in region]
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
            o_mark, o_let, o_occ = old_chunk[0]
            n_mark, n_let, n_occ = new_chunk[0]
            if o_mark == n_mark:
                # Same mark, different letter → moved
                force_ordinal = o_let == n_let and (
                    old_letter_counts.get(o_let, 0) > 1
                    or new_letter_counts.get(n_let, 0) > 1
                )
                descriptions.append(
                    f"{_name(o_mark)} on {letter_ref(o_let, o_occ, old_letter_counts, force_ordinal=force_ordinal)}"
                    f" in old, on {letter_ref(n_let, n_occ, new_letter_counts, force_ordinal=force_ordinal)} in new"
                )
            elif o_let == n_let and o_occ == n_occ:
                # Same letter, different mark → replaced
                descriptions.append(
                    f"on {letter_name(o_let)}, "
                    f"{_name(o_mark)} in old → "
                    f"{_name(n_mark)} in new"
                )
            else:
                descriptions.append(
                    f"{_name(o_mark)} on {letter_name(o_let)}"
                    f" (old) → {_name(n_mark)} on "
                    f"{letter_name(n_let)} (new)"
                )
        elif tag == "delete":
            for mark, let, occ in old_chunk:
                deletes.append((mark, let, occ))
        elif tag == "insert":
            for mark, let, occ in new_chunk:
                inserts.append((mark, let, occ))
        else:
            # Complex replace — fall back to generic description
            old_parts = ", ".join(
                f"{_name(m)} on {letter_name(l)}" for m, l, occ in old_chunk
            )
            new_parts = ", ".join(
                f"{_name(m)} on {letter_name(l)}" for m, l, occ in new_chunk
            )
            descriptions.append(f"old has {old_parts}; new has {new_parts}")

    # Pair delete/insert of same mark as moves
    used_inserts = set()
    for d_mark, d_let, d_occ in deletes:
        paired = False
        for idx, (i_mark, i_let, i_occ) in enumerate(inserts):
            if idx not in used_inserts and i_mark == d_mark:
                force_ordinal = d_let == i_let and (
                    old_letter_counts.get(d_let, 0) > 1
                    or new_letter_counts.get(i_let, 0) > 1
                )
                descriptions.append(
                    f"{_name(d_mark)} on {letter_ref(d_let, d_occ, old_letter_counts, force_ordinal=force_ordinal)}"
                    f" in old, on {letter_ref(i_let, i_occ, new_letter_counts, force_ordinal=force_ordinal)} in new"
                )
                used_inserts.add(idx)
                paired = True
                break
        if not paired:
            descriptions.append(f"{_name(d_mark)} on {letter_name(d_let)} removed")
    for idx, (i_mark, i_let, i_occ) in enumerate(inserts):
        if idx not in used_inserts:
            descriptions.append(f"{_name(i_mark)} on {letter_name(i_let)} added")

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


def is_poetic(book, chapter, verse):
    if book not in _POETIC_BOOKS:
        return False
    if book == "Job":
        return not _is_prose_section_of_job(chapter, verse)
    return True


# ── Public API ───────────────────────────────────────────────────────

ACCENT_CATS = {"accent-change", "accent-addition", "accent-removal"}
MARK_CATS = {
    "meteg-removal",
    "meteg-addition",
    "vowel-change",
    "rafeh",
    "varika",
}


LEG_SENTINEL = "\ufdd0"
NAR_SENTINEL = "\ufdd1"


def has_paseq(text):
    return (
        hpu.PASOLEG in text
        or DOUB_VERT_LINE in text
        or LEG_SENTINEL in text
        or NAR_SENTINEL in text
    )


def collect_paseq_types(obj, types):
    if isinstance(obj, str):
        return
    if isinstance(obj, dict):
        name = obj["tmpl_name"]
        if is_parashah_template(name):
            return
        if name in ("מ:לגרמיה-2", "מ:לגרמיה"):
            types.append("legarmeh")
            return
        if name == "מ:פסק":
            types.append("paseq")
            return
        if name == "נוסח":
            p1 = get_param(obj, "1")
            if p1 is not MISSING:
                collect_paseq_types(p1, types)
            return
        if is_std_kq_template(name) or is_qere_velo_ketiv_template(name):
            _validate_special_kq_if_needed(obj)
            p2 = get_param(obj, "2")
            if p2 is not MISSING:
                collect_paseq_types(p2, types)
            return
        if is_trivial_kq_template(name):
            p1 = get_param(obj, "1")
            if p1 is not MISSING:
                collect_paseq_types(p1, types)
            return
        if is_ketiv_velo_qere_template(name):
            return
        if name == "מ:קמץ":
            pd = get_param(obj, "ד")
            if pd is not MISSING:
                collect_paseq_types(pd, types)
            return
        if name == "מ:כפול":
            pk = get_param(obj, "כפול")
            if pk is not MISSING:
                collect_paseq_types(pk, types)
            return
        p1 = get_param(obj, "1")
        if p1 is not MISSING:
            collect_paseq_types(p1, types)
        return
    if isinstance(obj, list):
        for item in obj:
            collect_paseq_types(item, types)


def _describe_paseq_change(old_text, new_text, old_ep=None, new_ep=None):
    if old_ep is not None and new_ep is not None:
        old_types = []
        new_types = []
        collect_paseq_types(old_ep, old_types)
        collect_paseq_types(new_ep, new_types)
        old_counts = Counter(old_types)
        new_counts = Counter(new_types)
        deltas = {
            paseq_type: new_counts[paseq_type] - old_counts[paseq_type]
            for paseq_type in set(old_counts) | set(new_counts)
        }
        added = [paseq_type for paseq_type, delta in deltas.items() if delta > 0]
        removed = [paseq_type for paseq_type, delta in deltas.items() if delta < 0]
        if len(added) == 1 and not removed:
            return f"add {added[0]}"
        if len(removed) == 1 and not added:
            return f"remove {removed[0]}"
    if not has_paseq(old_text) and has_paseq(new_text):
        return "add paseq / legarmeh"
    if has_paseq(old_text) and not has_paseq(new_text):
        return "remove paseq / legarmeh"
    return None


def _describe_maqaf_afor(old_text, new_text):
    old_spaces = old_text.count(" ")
    new_spaces = new_text.count(" ")
    if old_spaces > new_spaces:
        return "add gray maqaf"
    if new_spaces > old_spaces:
        return "remove gray maqaf"
    return None


def describe_change(
    old_text, new_text, category, book, chapter, verse, old_ep=None, new_ep=None
):
    """Return an English description of the change, or None."""
    from mb_diff_mpu.change_ops_extract import extract_change_ops
    from mb_diff_mpu.change_ops_render import render_english

    ops = extract_change_ops(
        old_text, new_text, category, book, chapter, verse, old_ep, new_ep
    )
    return render_english(ops, book, chapter, verse, old_text, new_text)


def add_name_tooltips(html_escaped_desc):
    """Wrap names that have tooltips with <abbr> tags.

    Must be called AFTER HTML-escaping the description, since the name
    strings contain no HTML special characters.
    """
    result = html_escaped_desc
    for name, tip in _NAME_TOOLTIPS.items():
        result = result.replace(name, f'<abbr title="{tip}">{name}</abbr>')
    return result
