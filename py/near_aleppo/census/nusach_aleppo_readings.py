"""Read MAM apparatus clause heads and their Aleppo source relations.

Split only outside balanced parentheses and brackets. Preserve source and doubt
qualifiers, testimony sigla and prose-led heads; ambiguous or unparsed heads are
reported separately. A leading equals sign denotes source agreement, while a
head before equals names a source alternative. Quoted forms retain source text.
"""

import re
import sys
from collections import Counter

from mb_cmn import bib_locales as tbn
from near_aleppo.census import census_paths
from near_aleppo.census.edition_projection import (
    EDITION_SEPARATOR_TEMPLATE_NAMES,
    edition_parameter_keys,
    edition_parameter_keys_for,
)
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import ws_tmpl2 as wtp

sys.stdout.reconfigure(encoding="utf-8")

NUSACH = "נוסח"
ALEF = "א"

# Section 3 rule 4, spelled out.  The codex's TEXT:
CODEX_TEXT = {
    "א",
    "א-צילום",
    "א-כתיב",
    "א-קרי",
    "א-תיקון",
    "א[לאחר תיקון]",
}
# Testimony to its lost parts, which rule 4 also counts as Aleppo:
CODEX_TESTIMONY = {"א(ו)", "א(ס)", "א(ע)", "א(ק)", "א(ר)", "א(צילום)"}
# Not the text: an inference, and the margin.
NOT_THE_TEXT = {"שיטת-א", "מסורת-א", 'א-מ"ק', 'מ"ק-א'}

HEBREW = re.compile(r"[א-ת]")
PAREN_LIST = re.compile(r"^א\(([^)]*)\)$")
# Points and accents.  Written as codepoint escapes because a bare combining mark in a
# character class is an invisible literal, which the user-level instructions ban outright.
# U+0591..U+05BD accents through meteg, U+05BF rafe, U+05C1/U+05C2 the shin and sin dots,
# U+05C4/U+05C5 the upper and lower dots, U+05C7 qamats qatan.  DELIBERATELY EXCLUDED:
# U+05BE maqaf, U+05C0 paseq, U+05C3 sof pasuq and U+05C6 nun hafukha, each of which a
# prose description can carry without quoting a form.
POINTED = re.compile("[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7]")
BRACKETED = re.compile(r"<([^>]*)>")


def reading_head(reading):
    """The quoted form a clause offers, before its parenthetical description.

    MAM has either ``<form>`` in angle brackets or a bare form followed by
    ``" ("`` and a description.
    """
    inner = BRACKETED.findall(reading)
    if inner:
        return " ".join(inner)
    cut = reading.find(" (")
    return reading[:cut] if cut >= 0 else reading


def ref(bcvt):
    return f"{tbn.bcvt_get_bk39id(bcvt)} {tbn.bcvt_get_chnu(bcvt)}:{tbn.bcvt_get_vrnu(bcvt)}"


def each_nusach(wtel, out):
    """Every נוסח template reachable under the edition projection."""
    if isinstance(wtel, str):
        return
    if isinstance(wtel, (list, tuple)):
        for x in wtel:
            each_nusach(x, out)
        return
    if not wtp.is_template(wtel):
        return
    name = wtp.template_name(wtel)
    if name == NUSACH:
        out.append(wtel)
        return  # step 31 measured no נוסח nested inside another
    for k in edition_parameter_keys(wtel):
        each_nusach(wtp.template_param_val(wtel, k), out)


def keys_for(name, keys):
    """Compatibility entry point for apparatus surveys that reuse this walk."""
    return edition_parameter_keys_for(name, keys)


def flatten(wtel, out, *, projected):
    if isinstance(wtel, str):
        out.append(wtel)
    elif isinstance(wtel, (list, tuple)):
        for x in wtel:
            flatten(x, out, projected=projected)
    elif wtp.is_template(wtel):
        name = wtp.template_name(wtel)
        if name in EDITION_SEPARATOR_TEMPLATE_NAMES:
            out.append(" ")
            if projected:
                return
        keys = (
            edition_parameter_keys(wtel) if projected else wtp.template_param_keys(wtel)
        )
        for k in keys:
            flatten(wtp.template_param_val(wtel, k), out, projected=projected)


def text_of(val):
    out = []
    flatten(val, out, projected=True)
    return "".join(out).strip()


def clauses(val):
    """The note body split at its ש separators; each clause flattened to a string."""
    items = val if isinstance(val, (list, tuple)) else [val]
    out = [""]
    for it in items:
        if isinstance(it, str):
            out[-1] += it
        elif wtp.is_template(it) and wtp.template_name(it) == "ש":
            out.append("")
        else:
            body = []
            flatten(it, body, projected=True)
            out[-1] += "".join(body)
    return [c for c in out if c.strip()]


def split_clause(clause):
    """(shape, head, reading) for one clause.

    shape is 'agree' for a clause opening with '=', whose sigla run to the first space
    and which asserts agreement with MAM; 'differ' for 'sigla=reading'; 'none' for a
    clause with no '=' at all.
    """
    c = clause.strip()
    if c.startswith("="):
        cut = first_space_outside_brackets(c[1:])
        return "agree", c[1 : 1 + cut], c[1 + cut :]
    if "=" in c:
        head, _, rest = c.partition("=")
        return "differ", head, rest
    return "none", "", c


def first_space_outside_brackets(s):
    """Index of the first space not inside () or [] -- a siglum can hold one.

    An 'agree' clause's sigla run to the first space, but א(צילום ויקס),
    ק3[לאחר תיקון] and ל3[טפחא וקמץ וסילוק] each carry a space inside brackets.
    """
    depth = 0
    for i, ch in enumerate(s):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == " " and depth <= 0:
            return i
    return len(s)


def split_outside_brackets(head):
    """Split a siglum list on commas that are NOT inside () or []."""
    out, buf, depth = [], "", 0
    for ch in head:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth <= 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [s.strip() for s in out if s.strip()]


def normalize(siglum):
    """(base, qualifier) with the doubt marks split off and א(x,y) expanded by caller."""
    s = siglum.strip()
    qual = ""
    while s and s[-1] in "?!":
        qual = s[-1] + qual
        s = s[:-1]
    return s, qual


def expand(siglum):
    """One head element to the list of sigla it names.

    א(ס,ק,ר) is one element naming three testimonies; א(צילום ויקס) is the photograph.
    """
    base, qual = normalize(siglum)
    m = PAREN_LIST.match(base)
    if not m:
        return [(base, qual)]
    inner = m.group(1)
    if inner.startswith("צילום"):
        return [("א(צילום)", qual)]
    parts = [p.strip() for p in inner.split(",") if p.strip()]
    out = []
    for p in parts:
        p = p.split("[")[0].strip()  # א(ע[עזרא]) names ע with a gloss
        out.append((f"א({p})", qual))
    return out


def classify(base):
    if base in CODEX_TEXT:
        return "codex-text"
    if base in CODEX_TESTIMONY:
        return "codex-testimony"
    if base in NOT_THE_TEXT:
        return "not-the-text"
    if base.startswith(ALEF):
        return "unparsed-alef"
    return "other"


def head_is_prose(head):
    """A head that opens with prose rather than with a siglum list.

    The test is a space OUTSIDE brackets: a siglum list is free to carry spaces
    inside them, and a first pass that tested for any space at all discarded 72
    perfectly good heads.
    """
    h = head.strip()
    return first_space_outside_brackets(h) < len(h)


def prose_head_last_siglum(head):
    """The last whitespace-separated token of a prose-led head.

    A clause can open with prose and reach its siglum only at the end.  Such a
    head is reported in a bucket of its own rather than folded into the
    population, the head not being a siglum list at all.
    """
    parts = head.strip().split()
    return parts[-1] if parts else ""


def collect():
    """The walk, and the buckets it fills."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=census_paths.mam_parsed_path())

    n_nusach = 0
    n_clauses = 0
    shape_counts = Counter()
    alef_heads = Counter()
    kind_counts = Counter()
    qual_counts = Counter()
    differ_hits = []  # (bcvt, target, siglum, qualifier, reading)
    agree_hits = 0
    agree_verses = set()
    differ_verses = set()
    unparsed = []
    prose_with_alef = []
    malformed = []
    # Every verse carrying a נוסח at all, whatever its clauses cite.  Reported by no
    # section of main() below; step 40's manual_suppression_outcome.py wants it, to tell
    # "MAM has no note here" from "MAM has a note that cites no codex reading".
    nusach_verses = set()

    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books:
            continue
        for bcvt, mr in books[bkid]["verses_plus"].items():
            found = []
            each_nusach(list(mr.EP), found)
            if found:
                nusach_verses.add(bcvt)
            for t in found:
                n_nusach += 1
                keys = sorted(wtp.template_param_keys(t))
                if keys != ["1", "2"]:
                    # A נוסח whose second parameter is NAMED rather than positional: the
                    # wikitext wrote א=<reading> at the head of the body, and MediaWiki
                    # read א as a parameter name.  Reported, never skipped silently --
                    # the reading is unreachable to any reader of parameter 2, which is
                    # this step's whole subject.
                    malformed.append((bcvt, keys, wtp.template_param_val(t, "1")))
                    continue
                target = text_of(wtp.template_param_val(t, "1"))
                for clause in clauses(wtp.template_param_val(t, "2")):
                    n_clauses += 1
                    shape, head, reading = split_clause(clause)
                    shape_counts[shape] += 1
                    if head_is_prose(head):
                        base, _q = normalize(prose_head_last_siglum(head))
                        if classify(base) in ("codex-text", "codex-testimony"):
                            prose_with_alef.append((bcvt, shape, head, clause[:150]))
                        continue
                    for element in split_outside_brackets(head):
                        for base, qual in expand(element):
                            if ALEF in base:
                                alef_heads[base + qual] += 1
                            kind = classify(base)
                            if kind == "unparsed-alef":
                                unparsed.append(
                                    (bcvt, shape, base + qual, clause[:130])
                                )
                            if kind in ("codex-text", "codex-testimony"):
                                kind_counts[(shape, kind)] += 1
                                qual_counts[(shape, qual or "(none)")] += 1
                                if shape == "differ":
                                    differ_hits.append(
                                        (bcvt, target, base, qual, reading)
                                    )
                                    differ_verses.add(bcvt)
                                elif shape == "agree":
                                    agree_hits += 1
                                    agree_verses.add(bcvt)

    return {
        "n_nusach": n_nusach,
        "n_clauses": n_clauses,
        "shape_counts": shape_counts,
        "alef_heads": alef_heads,
        "kind_counts": kind_counts,
        "qual_counts": qual_counts,
        "differ_hits": differ_hits,
        "agree_hits": agree_hits,
        "agree_verses": agree_verses,
        "differ_verses": differ_verses,
        "unparsed": unparsed,
        "prose_with_alef": prose_with_alef,
        "malformed": malformed,
        "nusach_verses": nusach_verses,
    }
