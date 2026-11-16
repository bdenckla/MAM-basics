"""The body sections of gh-pages/morphhb-corrections/index.html.

Written by Claude (Opus 5.5) on 2026-11-14, a sub-agent of the session that built the page, as
an untracked scratch script, and tracked since 2026-11-15.  morphhb_corrections_index's
docstring says what each section holds; morphhb_corrections_lib holds the page's rules.  The
generator imports SECTIONS and departures from here, assembles the page, runs self_test on the
sections it built, and lints the page.

Every Hebrew form is copied by script, from the report folder F's out/ files or from
out/morphhb-corrections/review-links.json; this file holds no Hebrew character (a letter or mark
that must be named is named by its Unicode name in an escape).  Each parse of one of F's .txt
files asserts how many times its pattern matches, and each count the page states is checked
against F's data where F's data hold it.
"""

import ast
import html
import json
import re
import unicodedata
from collections import Counter
from functools import lru_cache

from author_misc import morphhb_corrections_lib as L
from author_misc.morphhb_corrections_lib import (
    H,
    code,
    commit,
    form_td,
    heading,
    heb,
    here,
    ht,
    issue,
    letters,
    mnorm,
    morph,
    note_td,
    ol,
    p,
    q,
    review_stripped,
    stack,
    strong,
    table,
    td,
    vcell,
    vref,
    word,
)

FO = L.F / "out"
MAQAF = L.MAQAF
EM = "\N{EM DASH}"
AL = "\N{HEBREW LETTER ALEF}\N{HEBREW LETTER LAMED}"
H_DOT = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"
HATAF = H_DOT + "ataf"
HATAF_PATAH = H_DOT + "ataf pata" + H_DOT
HET = H_DOT + "et"
QADMA = "\N{HEBREW ACCENT QADMA}"
PASHTA = "\N{HEBREW ACCENT PASHTA}"
MAPIQ = "\N{HEBREW POINT DAGESH OR MAPIQ}"
LETTER_HE = "\N{HEBREW LETTER HE}"


# ---------------------------------------------------------------- reading F


@lru_cache(maxsize=None)
def ftext(name):
    return (FO / name).read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def fjson(name):
    return json.loads(ftext(name))


def found(rx, text, n):
    """The matches of rx (multiline) in text, which must number exactly n."""
    ms = list(re.finditer(rx, text, re.M))
    assert len(ms) == n, (rx, len(ms), n)
    return ms


def one(rx, text):
    return found(rx, text, 1)[0]


def between(text, start, end):
    """text from the one line that starts with start up to the next line that starts with end."""
    a = one("^" + re.escape(start), text).start()
    b = text.index("\n" + end, a)
    return text[a:b]


def block_after(text, head):
    """The block of text that the one line starting with head opens, up to the next '-- ' line."""
    a = one("^" + re.escape(head) + ".*$", text).start()
    m = re.compile(r"^-- ", re.M).search(text, a + 1)
    return text[a : m.start() if m else len(text)]


@lru_cache(maxsize=None)
def commits():
    """morphhb's commits by their first 8 hex digits: (date, the message's first line)."""
    out = {}
    for sha, c in fjson("04-commits.json").items():
        assert sha[:8] not in out, sha
        out[sha[:8]] = (c["committed"][:10], c["message"].split("\n")[0].strip())
    return out


def cm(sha, msg=False):
    """A morphhb commit with its date, and with its message too if msg."""
    date, message = commits()[sha]
    return commit(sha, date, message if msg else None)


def cmc(sha):
    """A morphhb commit and its date, for use inside parentheses."""
    return ht(commit(sha), ", ", commits()[sha][0])


# ---------------------------------------------------------------- small helpers


def dq(s):
    return "\N{LEFT DOUBLE QUOTATION MARK}" + s + "\N{RIGHT DOUBLE QUOTATION MARK}"


def hj(parts, sep):
    out = []
    for k, x in enumerate(parts):
        if k:
            out.append(sep)
        out.append(x)
    return ht(*out)


def and_list(parts, conj="and"):
    parts = list(parts)
    if len(parts) == 1:
        return ht(parts[0])
    return ht(hj(parts[:-1], ", "), f" {conj} ", parts[-1])


def vlist(refs, ws=None, conj="and"):
    ws = ws or [None] * len(refs)
    return and_list([vref(r, w) for r, w in zip(refs, ws)], conj)


def num(n):
    return f"{n:,}"


def cap(s):
    """s with its first letter capitalized, except the name morphhb, which is lowercase."""
    return s if s.startswith("morphhb") else s[:1].upper() + s[1:]


def joined(ws):
    """morphhb's <w> records as morphhb writes them: each word's text, a maqaf where a maqqef
    seg follows it, a space between words otherwise."""
    s = ""
    for w in ws:
        if s and not s.endswith(MAQAF):
            s += " "
        s += w["text"] + (MAQAF if w.get("maqaf_after") else "")
    return s


def chanted(atoms):
    """A chanted word's atoms as one string: no space after a maqaf."""
    s = ""
    for a in atoms:
        if s and not s.endswith(MAQAF):
            s += " "
        s += a
    return s


def atoms_of(form):
    return re.findall("[^ " + MAQAF + "]+" + MAQAF + "?", form)


def first_atom(form):
    return mnorm(atoms_of(form)[0])


def fkey(s):
    """A form's units, each with its marks sorted and invisible marks dropped, morphhb's '/'
    dropped first: equal keys mean the same letters with the same marks."""
    return [L.unit_key(u) for u in L.units(s.replace("/", ""))]


def unk(s):
    """A display form with F's [k] and [q] markers dropped."""
    return re.sub(r"\[[kq]\]", "", s).strip()


def wtd(s):
    """morphhb's own word(s) in a cell, as morphhb writes them."""
    return td(word(s), cls="form", rtl=True)


def name(ch):
    return unicodedata.name(ch)


SHA = re.compile(r"[0-9a-f]{8}")


def coded(s, codes):
    """Plain text with each of morphhb's morph codes named in codes shown by morph()."""
    if not codes:
        return ht(s)
    rx = re.compile(
        r"(?<![\w/])("
        + "|".join(re.escape(c) for c in sorted(set(codes), key=len, reverse=True))
        + r")(?![\w/])"
    )
    out, pos = [], 0
    for m in rx.finditer(s):
        out += [s[pos : m.start()], morph(m.group(1))]
        pos = m.end()
    out.append(s[pos:])
    return ht(*out)


def rich(s, codes=()):
    """F's prose, whose backticked spans are commits (linked) or morph codes.  Its straight
    double quotes, around commit messages, are drawn as curly ones, as the page's own are.
    """
    parts = s.split("`")
    assert len(parts) % 2 == 1, s
    out = []
    for k, part in enumerate(parts):
        if k % 2 == 0:
            part = re.sub(
                '"([^"]*)"',
                "\N{LEFT DOUBLE QUOTATION MARK}\\1\N{RIGHT DOUBLE QUOTATION MARK}",
                part,
            )
            out.append(coded(part, codes))
        elif SHA.fullmatch(part):
            out.append(commit(part))
        else:
            out.append(morph(part))
    return ht(*out)


@lru_cache(maxsize=None)
def wlc_note_rows():
    """60-wlc-notes.txt's table of WLC's note letters, by letter."""
    sec = between(ftext("60-wlc-notes.txt"), "== 2. Counts", "== 3.")
    rows = found(
        r"^(\S)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S.*)$", sec, 22
    )
    keys = ("notes", "chanted", "differ", "by_letters", "flagged", "backoff")
    return {
        m.group(1): dict(
            zip(keys, (int(m.group(k)) for k in range(2, 8))),
            meaning=m.group(8).strip(),
        )
        for m in rows
    }


def note(n):
    """A WLC note letter, its meaning (as morphhb's files give it) on hover."""
    title = f"WLC's note {n}: {wlc_note_rows()[n]['meaning']}"
    return H(f'<abbr title="{html.escape(title)}">{html.escape(n)}</abbr>')


def notes_list(ns):
    return hj([note(n) for n in ns], ", ")


def wlc_versions(vs, conj):
    names = ["WLC " + vs[0]] + list(vs[1:])
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + f" {conj} " + names[-1]


def notes_phrase(by_version):
    """{"4.18": [...], "4.20": [...], "4.22": [...]} in words, e.g. "none in WLC 4.18 or 4.20;
    note 1 in WLC 4.22"."""
    groups = []
    for v, ns in by_version.items():
        t = tuple(ns)
        for g in groups:
            if g[0] == t:
                g[1].append(v)
                break
        else:
            groups.append((t, [v]))
    parts = []
    for t, vs in groups:
        if not t:
            parts.append(ht("none in ", wlc_versions(vs, "or")))
        else:
            parts.append(
                ht(
                    "note " if len(t) == 1 else "notes ",
                    notes_list(t),
                    " in ",
                    wlc_versions(vs, "and"),
                )
            )
    return hj(parts, "; ")


# ---------------------------------------------------------------- the review's cases


@lru_cache(maxsize=None)
def cases():
    """F's 56 cases (12-part1-table.json), each with the review's own forms (review-links.json):
    the page shows the Israel Bible's forms only as the review shows them.  F's copies equal the
    review's by the review's own key (F keeps Isaiah 49:23's sof pasuq, and MAM's qamats qatan
    at Exodus 20:9 and Deuteronomy 5:13, which the review's forms do not show)."""
    t = fjson("12-part1-table.json")
    assert t["counts"] == {"a": 1, "b": 5, "c": 46, "d": 4}, t["counts"]
    rows = L.links()["rows"]
    assert len(t["rows"]) == len(rows) == 56
    used, out = set(), []
    for r in t["rows"]:
        key = list(L.parse_ref(r["key"]))
        same = [
            i
            for i, x in enumerate(rows)
            if i not in used
            and x["verse"] == key
            and L.ib.key(x["ib"]) == L.ib.key(r["ib"])
        ]
        assert len(same) == 1, r["key"]
        x = rows[same[0]]
        used.add(same[0])
        assert L.ib.key(x["mam"]) == L.ib.key(r["mam"]), r["key"]
        assert x["page"] == r["page"], r["key"]
        out.append(dict(r, ib_form=x["ib"], mam_form=x["mam"]))
    return out


def kind(k):
    return [r for r in cases() if r["class"] == k]


@lru_cache(maxsize=None)
def census():
    d = fjson("50-alel-census.json")
    assert len(d["words"]) == 4930 and len(d["mismatches"]) == 17
    by_id = {w["id"]: w for w in d["words"]}
    assert len(by_id) == 4930
    return d, by_id


NINE_HEAD = [
    "Verse",
    "morphhb id",
    "WLC 4.20",
    "MAM",
    "morphhb's lemma",
    "morphhb's morph",
    "Reads MAM's form",
    "WLC notes at the chanted word",
    "Lemma's number since",
    "Morph since",
]


@lru_cache(maxsize=None)
def nine():
    """The nine corrections, from 80-part2-corrections-table.md."""
    lines = [
        ln
        for ln in ftext("80-part2-corrections-table.md").splitlines()
        if ln.startswith("|")
    ]
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    assert cells[0] == NINE_HEAD, cells[0]
    out = []
    for c in cells[2:]:
        assert len(c) == 10, c
        since = []
        for s in (c[8], c[9]):
            m = re.fullmatch(r"`([0-9a-f]{8})` (\d{4}-\d\d-\d\d)", s)
            assert m and commits()[m.group(1)][0] == m.group(2), s
            since.append(m.group(1))
        out.append(
            dict(
                verse=c[0],
                id=re.fullmatch(r"`(\w{5})`", c[1]).group(1),
                wlc=c[2],
                mam=c[3],
                lemma=c[4],
                morph=re.fullmatch(r"`([^`]+)`", c[5]).group(1),
                reads=c[6],
                notes=c[7],
                lemma_since=since[0],
                morph_since=since[1],
            )
        )
        # The table's forms are shown as the review shows forms.
        assert review_stripped(c[2]) == mnorm(c[2]), c[0]
        assert review_stripped(c[3]) == mnorm(c[3]), c[0]
    assert len(out) == 9
    return out


@lru_cache(maxsize=None)
def check63():
    """63-check-new-corrections.txt: each word's form in every source, and the counts."""
    blocks = re.split(r"^== ", ftext("63-check-new-corrections.txt"), flags=re.M)[1:]
    assert len(blocks) == 7
    out = {}
    for b in blocks:
        ref = b.splitlines()[0].strip()
        ms = list(
            re.finditer(
                r"^   morphhb (\w{5}): (\S+) lemma=(.+?) morph=(\S+) notes=(\[.*\])$",
                b,
                re.M,
            )
        )
        if not ms:
            assert ref == "Dan 3:15", ref
            continue
        assert len(ms) == 1
        m = ms[0]
        src = {}
        for nm in ("WLC 4.18", "WLC 4.20", "WLC 4.22", "UXLC 2.6", "MAM"):
            src[nm] = one(r"^   " + re.escape(nm) + r"\s+(\S+)$", b).group(1)
        own = one(r"^   morphhb's words of this form \(review key\): (\{.*\})$", b)
        mams = one(r"^   morphhb's words of MAM's form \S+: (\{.*\})$", b)
        out[m.group(1)] = dict(
            ref=ref,
            word=m.group(2),
            lemma=m.group(3),
            morph=m.group(4),
            notes=ast.literal_eval(m.group(5)),
            src=src,
            own=ast.literal_eval(own.group(1)),
            mam_form=ast.literal_eval(mams.group(1)),
        )
    assert sorted(out) == sorted(["28sYk", "01oc4", "05ENP", "03caE", "24JqK", "249Bc"])
    return out


LEMMA_GLOSS = {"408": "the negative", "413": "the preposition"}
MORPH_GLOSS = {"HTn": "the negative", "HR": "the preposition"}
# The form each analysis reads: the negative is the patah form, the preposition the segol form.
READS_VOWEL = {"408": "patah", "413": "segol", "HTn": "patah", "HR": "segol"}


@lru_cache(maxsize=None)
def five():
    """The five corrections: the case, morphhb's corrected word, its census record and its row
    of the nine corrections' table."""
    _d, by_id = census()
    rows9 = {r["id"]: r for r in nine()}
    out = []
    n_422_only = 0
    for c in kind("b"):
        w = c["morphhb"][0]
        assert letters(w["text"]) == AL, c["key"]
        rec = by_id[w["id"]]
        assert rec["verdict"][0] == "correction", c["key"]
        assert (rec["lemma"], rec["morph"]) == (w["lemma"], w["morph"]), c["key"]
        assert {rec["vowel"], rec["mam_vowel"]} == {"segol", "patah"}, c["key"]
        assert READS_VOWEL[w["lemma"]] == rec["mam_vowel"], c["key"]
        morph_mam = READS_VOWEL[w["morph"]] == rec["mam_vowel"]
        n9 = rows9[w["id"]]
        assert n9["reads"] == ("lemma and morph" if morph_mam else "lemma"), c["key"]
        assert (n9["lemma"], n9["morph"]) == (w["lemma"], w["morph"]), c["key"]
        # WLC 4.18, 4.20 and 4.22 and UXLC 2.6 have one atom here, which morphhb has too.
        srcs = ("WLC 4.18", "WLC 4.20", "WLC 4.22", "UXLC 2.6")
        a = [rec["sources"][s]["atoms"] for s in srcs]
        assert all(x == a[0] for x in a) and len(a[0]) == 1, c["key"]
        assert fkey(a[0][0]) == fkey(w["text"] + MAQAF), c["key"]
        # morphhb carries WLC 4.20's notes.
        assert rec["morphhb_notes"] == rec["sources"]["WLC 4.20"]["notes"], c["key"]
        if rec["sources"]["WLC 4.22"]["notes"] == ["1"]:
            assert rec["sources"]["WLC 4.20"]["notes"] == []
            n_422_only += 1
        out.append(dict(case=c, w=w, rec=rec, nine=n9, morph_mam=morph_mam))
    assert n_422_only == 3
    assert [x["w"]["id"] for x in out] == [r["id"] for r in nine()[:5]]
    assert [x["w"]["id"] for x in out] == fjson("50-alel-census.json")[
        "vowel_differences"
    ][:5]
    return out


def notes_by_version(rec):
    return {v: rec["sources"]["WLC " + v]["notes"] for v in ("4.18", "4.20", "4.22")}


# ---------------------------------------------------------------- verses of 13-verses.txt


def block13(short_ref):
    blocks = re.split(r"^== ", ftext("13-verses.txt"), flags=re.M)[1:]
    same = [b for b in blocks if b.splitlines()[0].strip() == short_ref]
    assert len(same) == 1, short_ref
    return same[0]


def morphhb_tokens(line):
    """13-verses.txt's morphhb line: each word's text, lemma, morph and whether a maqaf follows."""
    out = []
    for m in re.finditer(r"(\S+?)\{([^}]*)\}( " + MAQAF + ")?", line):
        lemma, _, mo = m.group(2).rpartition(" ")
        out.append(dict(text=m.group(1), lemma=lemma, morph=mo, maqaf=bool(m.group(3))))
    return out


@lru_cache(maxsize=None)
def josh2219():
    """Joshua 22:19's three al/el atoms: morphhb's token and MAM's atom, in verse order."""
    b = block13("Josh 22:19")
    toks = morphhb_tokens(one(r"^morphhb: (.+)$", b).group(1))
    mine = [t for t in toks if letters(t["text"]) == AL]
    assert len(mine) == 3 and all(t["maqaf"] for t in mine)
    wlc = [
        a
        for a in one(r"^WLC 4\.18: (.+)$", b).group(1).split(" | ")
        if letters(a) == AL
    ]
    assert [fkey(a) for a in wlc] == [fkey(t["text"] + MAQAF) for t in mine]
    sec3 = between(ftext("51-general-test.txt"), "== 3. Calibration", "== 4.")
    mam_verse = one(
        r"^   MAM's verse:\s+(.+)$", block_after(sec3, "-- Josh 22:19  id 06Umo")
    ).group(1)
    mam = [a for a in atoms_of(mam_verse) if letters(a) == AL]
    assert len(mam) == 3
    assert [(t["lemma"], t["morph"]) for t in mine] == [
        ("413", "HR"),
        ("408", "HTn"),
        ("408", "HR"),
    ]
    return list(zip(mine, mam))


# ---------------------------------------------------------------- the stress helper


@lru_cache(maxsize=None)
def helper_lines():
    sec = between(
        ftext("43-text-class-lists.txt"),
        "######## qadma (class",
        "######## divided-accents/accents (class",
    )
    found(r"^\S+ \d+:\d+\s+morphhb: ", sec, 3811)
    return sec


def helper_example(ref):
    """morphhb's atom and WLC 4.20's at a verse of the stress-helper class (one unit there)."""
    m = one(
        r"^"
        + re.escape(ref)
        + r"\s+morphhb: (\S+)  \|  WLC 4\.20: (\S+)  "
        + r"\[morphhb \+accent qadma; WLC \+accent pashta\]$",
        helper_lines(),
    )
    mine, wlc = m.group(1), m.group(2)
    check_helper(mine, wlc, ref)
    return mine, wlc


def check_helper(mine, wlc, where):
    """WLC has the pashta twice, the second on the atom's last letter; morphhb writes the
    first with HEBREW ACCENT QADMA on the same letter, and the atoms are otherwise equal.
    """
    um, uw = L.units(mnorm(mine)), L.units(mnorm(wlc))
    assert [u[0] for u in um] == [u[0] for u in uw], where
    at_w = [k for k, u in enumerate(uw) if PASHTA in u]
    at_m = [k for k, u in enumerate(um) if QADMA in u]
    assert len(at_w) == 2 and at_w[1] == len(uw) - 1 and at_m == at_w[:1], where
    assert not any(QADMA in u for u in uw), where
    fixed = [u.replace(QADMA, PASHTA) for u in um]
    assert [L.unit_key(u) for u in fixed] == [L.unit_key(u) for u in uw], where


# ---------------------------------------------------------------- 41-text-residuals.json


@lru_cache(maxsize=None)
def units41():
    d = fjson("41-text-residuals.json")
    assert d["residuals"] == [] and len(d["other_units_shown"]) == 24
    return d["other_units_shown"]


def units_labelled(label):
    return [u for u in units41() if u["label"] == label]


def atom_marks(form):
    """One atom's letters, each with its marks (invisible ones dropped), and its maqaf."""
    us = L.units(mnorm(form))
    maqaf = bool(us) and us[-1] == MAQAF
    if maqaf:
        us = us[:-1]
    assert us and all(letters(u[0]) for u in us), ascii(form)
    return [
        (u[0], Counter(c for c in u[1:] if c not in L.INVISIBLE)) for u in us
    ], maqaf


def union_diff(main, alt, wlc):
    """What WLC 4.20's atom has that the union of morphhb's main text and its alternative note
    lacks (missing), what the union has beyond it (extra), each as (letter index, mark name),
    and how the maqaf differs."""
    m, mq = atom_marks(main)
    a, aq = atom_marks(alt)
    w, wq = atom_marks(wlc)
    assert [x[0] for x in m] == [x[0] for x in a] == [x[0] for x in w], ascii(main)
    missing, extra = [], []
    for k, ((_b, cm_), (_b2, ca), (_b3, cw_)) in enumerate(zip(m, a, w)):
        u = cm_ | ca
        missing += [(k, name(ch)) for ch in (cw_ - u).elements()]
        extra += [(k, name(ch)) for ch in (u - cw_).elements()]
    maq = None if (mq or aq) == wq else ("extra" if (mq or aq) else "missing")
    return sorted(missing), sorted(extra), maq


# What differs at each Decalogue unit of 41-text-residuals.json, by morphhb id, in the order the
# page's table gives them, with what union_diff must find there.  Letter indices count from the
# atom's first letter.
DECALOGUE_UNITS = [
    (
        "02p5S",
        "marks",
        ([(1, "HEBREW POINT PATAH")], [], None),
        "A vowel: WLC 4.20's atom has a patah beside its qamats under the tav, which neither "
        "morphhb's main text nor its alternative note has.",
    ),
    (
        "02Feh",
        "marks",
        ([(3, "HEBREW POINT SHEVA")], [(3, "HEBREW POINT HATAF PATAH")], None),
        f"A vowel: morphhb's main text and its alternative note have a {HATAF_PATAH} under "
        f"the {HET} where WLC 4.20's atom has a sheva; MAM has the {HATAF_PATAH}.",
    ),
    (
        "05HcR",
        "maqaf",
        ([], [], "extra"),
        "The maqaf: morphhb's main text has a maqaf after the atom, which WLC 4.20's atom "
        "lacks; MAM has it.",
    ),
    (
        "02dor",
        "marks",
        ([(0, "HEBREW POINT METEG")], [], None),
        "A meteg: WLC 4.20's atom has a meteg under the vav, which neither morphhb's main text "
        "nor its alternative note has.",
    ),
    (
        "02xhV",
        "marks",
        ([(2, "HEBREW ACCENT GERESH")], [(2, "HEBREW ACCENT QADMA")], None),
        "An accent: on the bet, morphhb's alternative note has HEBREW ACCENT QADMA where WLC "
        "4.20's atom has HEBREW ACCENT GERESH.",
    ),
    (
        "05Lzv",
        "marks",
        ([], [(2, "HEBREW ACCENT TIPEHA")], None),
        "An accent: morphhb's alternative note has HEBREW ACCENT TIPEHA on the tsade, which "
        "WLC 4.20's atom lacks; UXLC 2.6 and MAM have it.",
    ),
    (
        "059vS",
        "ok",
        ([], [], None),
        "Nothing, taken together: morphhb's main text lacks WLC 4.20's maqaf after the atom, "
        "and its alternative note has it.",
    ),
    (
        "05fou",
        "ok",
        ([], [], None),
        "Nothing, taken together: morphhb's main text lacks WLC 4.20's maqaf after the atom, "
        "and its alternative note has it.",
    ),
]
# The two units whose union is WLC 4.20's atom although the main text alone is not: the main
# text lacks the maqaf that the alternative note and WLC 4.20's atom have.
MAQAF_ONLY_IN_NOTE = ("059vS", "05fou")


@lru_cache(maxsize=None)
def decalogue_units():
    """The eight Decalogue units of 41-text-residuals.json, each checked against
    DECALOGUE_UNITS."""
    us = [u for u in units41() if u["label"].startswith("divided-accents/")]
    assert len(us) == 8
    by_id = {}
    for u in us:
        assert len(u["morphhb_ids"]) == 1 and len(u["morphhb"]) == 1
        by_id[u["morphhb_ids"][0]] = u
    assert sorted(by_id) == sorted(x[0] for x in DECALOGUE_UNITS)
    out = []
    for id_, test, (missing, extra, maq), what in DECALOGUE_UNITS:
        u = by_id[id_]
        assert u["union_test"] == test, id_
        main, alt = u["_display"]["morphhb"], u["alternative"]["text"]
        wlc = u["_display"]["4.20"]
        got = union_diff(main, alt, wlc)
        assert got == (missing, extra, maq), (id_, got)
        if id_ in MAQAF_ONLY_IN_NOTE:
            assert (atom_marks(main)[1], atom_marks(alt)[1], atom_marks(wlc)[1]) == (
                False,
                True,
                True,
            ), id_
        out.append(dict(u, id=id_, what=what, main=main, alt=alt, wlc=wlc))
    # The five units labelled divided-accents/pointing: their review keys differ from WLC 4.20's
    # (a vowel or the maqaf); two of them pass the union test.
    pointing = [x for x in out if x["label"] == "divided-accents/pointing"]
    assert (
        len(pointing)
        == 5
        == fjson("40-text-compare-data.json")["label_units"]["4.20"][
            "divided-accents/pointing"
        ]
    )
    assert sorted(x["union_test"] for x in pointing) == [
        "maqaf",
        "marks",
        "marks",
        "ok",
        "ok",
    ]
    for x in out:
        assert (
            L.ib.key(x["main"]) != L.ib.key(x["wlc"])
            if x["label"] == "divided-accents/pointing"
            else L.ib.key(x["main"]) == L.ib.key(x["wlc"])
        ), x["id"]
    # Deuteronomy 5:17's tipexa is UXLC 2.6's and MAM's too.
    t = [x for x in out if x["id"] == "05Lzv"][0]
    assert all("\N{HEBREW ACCENT TIPEHA}" in t["_display"][s] for s in ("UXLC", "MAM"))
    return out


# ---------------------------------------------------------------- section 1: the answer


def section_answer():
    fv = five()
    seg = first_atom(fv[0]["case"]["ib_form"])
    pat = first_atom(fv[0]["case"]["mam_form"])
    neg = [x["case"] for x in fv if x["w"]["lemma"] == "408"]
    prep = [x["case"] for x in fv if x["w"]["lemma"] == "413"]
    assert len(neg) == 3 and len(prep) == 2
    for c in neg:
        assert (first_atom(c["ib_form"]), first_atom(c["mam_form"])) == (seg, pat), c[
            "key"
        ]
    for c in prep:
        assert (first_atom(c["ib_form"]), first_atom(c["mam_form"])) == (pat, seg), c[
            "key"
        ]
    n9 = nine()
    hos, *mappiq = n9[5:]
    assert hos["verse"] == "Hosea 13:15" and len(mappiq) == 3
    assert all(r["lemma_since"] == "c299c30a" for r in n9)
    return ht(
        heading(2, "The answer in brief", "answer"),
        ol(
            [
                ht(
                    strong("Of the review's 56 cases, morphhb corrects 5"),
                    ", all five of its al/el rows. At ",
                    vlist([c["key"] for c in neg], [c["ib_form"] for c in neg]),
                    ", WLC 4.18, 4.20 and 4.22 have the segol form ",
                    heb(seg),
                    ", the preposition ",
                    dq("to"),
                    ", where MAM has the patah form ",
                    heb(pat),
                    ", the negative ",
                    dq("do not"),
                    "; morphhb's text keeps WLC's form, and its lemma is 408, the negative. "
                    "At ",
                    vlist([c["key"] for c in prep], [c["ib_form"] for c in prep]),
                    " WLC has ",
                    heb(pat),
                    " where MAM has ",
                    heb(seg),
                    ", and morphhb's lemma is 413, the preposition.",
                ),
                ht(
                    strong("In all of morphhb there are nine corrections"),
                    ": those five; ",
                    vref(hos["verse"]),
                    ", where WLC 4.20 has ",
                    heb(hos["wlc"]),
                    ", ",
                    dq("son"),
                    ", and MAM ",
                    heb(hos["mam"]),
                    ", ",
                    dq("between"),
                    ", and morphhb's lemma reads MAM's word; and three words that differ only "
                    "by a mappiq, where the morph reads MAM's form: ",
                    and_list(
                        [
                            ht(
                                vref(r["verse"]),
                                " (WLC 4.20 ",
                                heb(r["wlc"]),
                                ", MAM ",
                                heb(r["mam"]),
                                ")",
                            )
                            for r in mappiq
                        ]
                    ),
                    ". Each of the nine lemmas' numbers is already in morphhb's first GitHub "
                    "commit, ",
                    cm("c299c30a"),
                    ", and no record of morphhb's own describes any of the nine.",
                ),
                ht(
                    strong("morphhb's text is WLC 4.20's"),
                    ", apart from systematic differences of encoding, the divided accents of "
                    "the Decalogues and ",
                    vref("Genesis 35:22"),
                    ", 12 words that morphhb divides for exegesis, and one ketiv and qere at ",
                    vref("Daniel 2:39"),
                    ".",
                ),
            ]
        ),
    )


# ---------------------------------------------------------------- section 2: the review's cases


def lemma_cell(w):
    return td(
        ht(
            w["lemma"],
            ", ",
            LEMMA_GLOSS[w["lemma"]],
            ", reads MAM's form",
        )
    )


def five_table():
    rows = []
    for x in five():
        c, w, rec, n9 = x["case"], x["w"], x["rec"], x["nine"]
        rows.append(
            [
                wtd(joined(c["morphhb"])),
                form_td(c["ib_form"], c["mam_form"]),
                vcell(c["key"], w=c["ib_form"]),
                lemma_cell(w),
                td(
                    ht(
                        morph(w["morph"]),
                        ", ",
                        MORPH_GLOSS[w["morph"]],
                        ", reads ",
                        "MAM's form" if x["morph_mam"] else "WLC's form",
                    )
                ),
                td(notes_phrase(notes_by_version(rec))),
                td(cm(n9["lemma_since"])),
                td(cm(n9["morph_since"])),
            ]
        )
    return table(
        [
            "morphhb's words",
            "Israel Bible above MAM",
            "Verse",
            "Lemma",
            "Morph",
            "WLC's notes at the chanted word",
            "Lemma since",
            "Morph since",
        ],
        rows,
    )


def josh_table():
    rows = []
    for t, mam_atom in josh2219():
        rows.append(
            [
                form_td(t["text"] + MAQAF, mam_atom),
                td(t["lemma"] + ", " + LEMMA_GLOSS[t["lemma"]]),
                td(ht(morph(t["morph"]), ", ", MORPH_GLOSS[t["morph"]])),
            ]
        )
    return table(
        ["morphhb's atom above MAM's", "Lemma", "Morph"],
        rows,
        caption=ht(
            vref("Joshua 22:19"), ": its three al/el atoms, in the verse's order"
        ),
    )


def subsection_five():
    fv = five()
    by_verse = {x["case"]["key"]: x for x in fv}
    morph_since = {x["case"]["key"]: x["nine"]["morph_since"] for x in fv}
    assert morph_since == {
        "Exodus 10:28": "f0b4e882",
        "Deuteronomy 2:9": "f0b4e882",
        "Joshua 22:19": "f0b4e882",
        "Judges 19:23": "097d0e42",
        "Jeremiah 47:6": "097d0e42",
    }, morph_since
    assert by_verse["Exodus 10:28"]["morph_mam"]
    assert not any(x["morph_mam"] for x in fv[1:])
    return ht(
        heading(3, "The five corrections", "five-corrections"),
        p(
            "At each of the five, morphhb's text keeps WLC's atom while its lemma reads MAM's; "
            "at ",
            vref("Exodus 10:28"),
            " its morph, ",
            morph("HTn"),
            ", reads MAM's form too. In each row the Israel Bible's form, which is WLC "
            "4.18's, stands above MAM's; morphhb's words are as morphhb writes them, accents "
            "included.",
        ),
        five_table(),
        ol(
            [
                ht(
                    strong("The texts."),
                    " WLC 4.18, 4.20 and 4.22 and UXLC 2.6 have the same atom at each of the "
                    "five places, and morphhb's text has it too. morphhb carries WLC's notes as "
                    "WLC 4.20 has them: note ",
                    note("U"),
                    " where WLC 4.20 has it, and none of the three notes ",
                    note("1"),
                    " that WLC 4.22 has where WLC 4.20 has none.",
                ),
                ht(
                    strong("The lemmas."),
                    " Each lemma is the same in morphhb's first GitHub commit, ",
                    cm("c299c30a", msg=True),
                    ", as now, and in every version probed between them. So each correction "
                    "is at least as old as the files that David Troidl kept in Google's SVN "
                    "before 2009-12-28, which were not read.",
                ),
                ht(
                    strong("The morphs."),
                    " ",
                    cm("097d0e42", msg=True),
                    " gave Judges and Jeremiah their morphs; ",
                    cm("f0b4e882", msg=True),
                    " gave Exodus, Deuteronomy and Joshua theirs. Every version probed after "
                    "those commits has the same morph.",
                ),
                ht(
                    strong("Context."),
                    " Where the verse has other al/el atoms, at ",
                    vlist(["Deuteronomy 2:9", "Joshua 22:19", "Judges 19:23"]),
                    ", morphhb gives them the lemma and morph that their own vowels call for. "
                    "The next table shows ",
                    vref("Joshua 22:19"),
                    "'s three; in each row morphhb's atom, which is WLC 4.18's, stands above "
                    "MAM's.",
                ),
            ]
        ),
        josh_table(),
    )


def subsection_wlc_analysis():
    (c,) = kind("a")
    assert c["key"] == "Judges 19:4"
    assert re.findall(r"`([0-9a-f]{8})`", c["since"]) == ["097d0e42"], c["since"]
    ws = c["morphhb"]
    return ht(
        heading(3, "The one analysis of WLC's form", "wlc-analysis"),
        p(
            "At ",
            vref(c["key"], c["ib_form"]),
            " the morph analyses WLC's form where MAM's form differs. In the row the Israel "
            "Bible's form, which is WLC 4.18's, stands above MAM's.",
        ),
        table(
            [
                "morphhb's words",
                "Israel Bible above MAM",
                "Verse",
                "Lemma",
                "Morph",
                "Note",
            ],
            [
                [
                    wtd(joined(ws)),
                    form_td(c["ib_form"], c["mam_form"]),
                    vcell(c["key"], w=c["ib_form"]),
                    td(hj([w["lemma"] for w in ws], "; ")),
                    td(hj([morph(w["morph"]) for w in ws], "; ")),
                    note_td(
                        rich(cap(c["what"]) + "."),
                        " The morph has been so since ",
                        cm("097d0e42"),
                        ".",
                    ),
                ]
            ],
        ),
    )


def subsection_text_changes():
    rows = []
    ds = kind("d")
    assert [c["key"] for c in ds] == [
        "Judges 15:14",
        "Eccl 2:23",
        "Exod 20:4",
        "Deut 5:8 (Decalogue row 6)",
    ]
    for c in ds:
        mine = review_stripped(joined(c["morphhb"]))
        assert L.ib.key(mine) != L.ib.key(c["ib_form"]), c["key"]
        rows.append(
            [
                form_td(c["ib_form"], c["mam_form"], mine),
                vcell(c["key"], w=c["ib_form"]),
                note_td(rich(cap(c["what"]) + ". " + cap(c["since"]) + ".")),
            ]
        )
    # At Deuteronomy 5:8's first row, morphhb's alternative-accent note is MAM's form as the
    # review shows it (46-text-divided-accents.txt, the catchWord line).
    x_accent = catchword()["x_accent"]
    assert mnorm(review_stripped(x_accent)) == mnorm(ds[3]["mam_form"])
    return ht(
        heading(3, "The four text changes", "text-changes"),
        p(
            "At four cases morphhb's text is not WLC 4.18's. In each row the Israel Bible's "
            "form, which is WLC 4.18's, stands above MAM's, and morphhb's text stands below "
            "them, all three as the review shows forms.",
        ),
        table(
            ["Israel Bible above MAM above morphhb", "Verse", "What changed, and when"],
            rows,
        ),
    )


def subsection_both_forms():
    rows = []
    cs = kind("c")
    assert len(cs) == 46
    for c in cs:
        ws = c["morphhb"]
        if c["n"] == 23:
            # F's note says "on the first syllable"; the qadma is on the stressed one (DEPARTURES).
            assert "on the first syllable" in c["what"] and "`380f4219`" in c["what"]
            mine, _wlc = helper_example("Isa 23:8")
            k = [i for i, u in enumerate(L.units(mnorm(mine))) if QADMA in u]
            assert (
                len(k) == 1
                and L.units(mnorm(mine))[k[0]][0] == "\N{HEBREW LETTER RESH}"
            )
            nt = note_td(
                "Outside the form: on the stressed syllable morphhb has HEBREW ACCENT QADMA "
                "where WLC has a second HEBREW ACCENT PASHTA, since ",
                cm("380f4219", msg=True),
                ".",
            )
        elif c["what"]:
            nt = note_td(rich(cap(c["what"]) + "."))
        else:
            nt = td("")
        rows.append(
            [
                wtd(joined(ws)),
                form_td(c["ib_form"], c["mam_form"]),
                vcell(
                    c["key"],
                    w=c["ib_form"],
                    extra="qere" if c["side"] == "qere" else None,
                ),
                td(hj([w["lemma"] for w in ws], "; ")),
                td(hj([morph(w["morph"]) for w in ws], "; ")),
                nt,
            ]
        )
    return ht(
        heading(3, "The 46 analyses that fit both forms", "both-forms"),
        p(
            "At 46 of the review's cases, WLC's form and MAM's differ only in pointing that "
            "neither the lemma nor the morph records, and morphhb's text is WLC 4.18's by the "
            "review's key, which compares forms without their accents, meteg and rafeh. In "
            "each row the Israel Bible's form, which is WLC "
            "4.18's, stands above MAM's; morphhb's words are as morphhb writes them, and where "
            "it has two or more, their lemmas and morphs are listed in the words' order.",
        ),
        table(
            [
                "morphhb's words",
                "Israel Bible above MAM",
                "Verse",
                "Lemma",
                "Morph",
                "Note",
            ],
            rows,
        ),
    )


@lru_cache(maxsize=None)
def hataf_rows():
    d = fjson("11-part1-hataf-ng.json")
    assert len(d) == 11
    by_ref = {}
    for e in d:
        by_ref.setdefault(e["reference"], []).append(e)
    assert len(by_ref) == 6 == fjson("12-part1-table.json")["hataf_rows"]
    out = []
    for ref, es in by_ref.items():
        rest = [{k: v for k, v in e.items() if k != "side"} for e in es]
        assert all(x == rest[0] for x in rest), ref
        assert all(e["skey_morphhb_eq_wlc418"] for e in es), ref
        assert len(es[0]["morphhb"]) == 1, ref
        out.append(dict(es[0], qere_only=[e["side"] for e in es] == ["qere"]))
    fns = [f for f in L.links()["footnotes"] if f["anchor"] == "fn-mam-hataf-ng"]
    assert len(fns) == 1
    assert [list(L.parse_ref(r["reference"])) for r in out] == fns[0]["verses"]
    return out


def subsection_hataf():
    rows = []
    for r in hataf_rows():
        w = r["morphhb"][0]
        rows.append(
            [
                wtd(w["text"]),
                form_td(review_stripped(r["wlc418"]), review_stripped(r["mam"])),
                vcell(r["reference"], extra="qere" if r["qere_only"] else None),
                td(w["lemma"]),
                td(morph(w["morph"])),
            ]
        )
    sam = [r for r in hataf_rows() if r["reference"] == "1 Samuel 26:10"][0]
    code_ = sam["morphhb"][0]["morph"]
    assert code_ == "HVqi3ms/Sp1cp"
    return ht(
        heading(
            3,
            f"The six verses of the review's footnote on MAM's {HATAF} vowels",
            "hataf",
        ),
        p(
            f"At each of the six verses that the review's footnote on MAM's {HATAF} vowels "
            f"names, morphhb's text has WLC's vowel where MAM has a {HATAF}, and the lemma and "
            "morph are the same for both: all six are analyses that fit both forms. In each "
            "row WLC 4.18's form stands above MAM's, both as the review shows forms; at ",
            vref("Ezra 4:9"),
            " only the qere has the form.",
        ),
        table(
            ["morphhb's word", "WLC 4.18 above MAM", "Verse", "Lemma", "Morph"], rows
        ),
        p(
            "Outside the question asked here, Claude notes that morphhb's morph at ",
            vref("1 Samuel 26:10"),
            ", ",
            morph(code_),
            ", gives the suffix as first person plural, while the energic suffix with a dagesh "
            "in the nun is third person masculine singular.",
        ),
    )


def helper_table(refs):
    rows = []
    for ref in refs:
        mine, wlc = helper_example(ref)
        rows.append([form_td(mine, wlc), vcell(ref, w=wlc)])
    return table(["morphhb above WLC 4.20", "Verse"], rows)


def subsection_cases_show():
    (ex4,) = [c for c in cases() if c["key"] == "Exod 20:4"]
    (dt8,) = [c for c in cases() if c["key"] == "Deut 5:8 (Decalogue row 6)"]
    assert ex4["class"] == dt8["class"] == "d"
    return ht(
        heading(3, "What the cases show about morphhb's text", "cases-show"),
        p(
            "morphhb's text is WLC 4.20's, not WLC 4.18's or 4.22's. At ",
            vref("Judges 15:14"),
            " and ",
            vref("Ecclesiastes 2:23"),
            " it has WLC 4.20's forms; at ",
            vref("2 Samuel 11:1"),
            " it keeps the rafeh that WLC 4.22 lacks; and its notes are WLC 4.20's: note ",
            note("1"),
            " at ",
            vref("Genesis 32:18"),
            ", where WLC 4.22 has ",
            note("U"),
            "; notes ",
            notes_list(["c", "n"]),
            " at ",
            vref("2 Kings 18:27"),
            ", without WLC 4.18's ",
            note("v"),
            "; none at ",
            vref("Ecclesiastes 2:23"),
            ", where WLC 4.18 has three; and none of the notes ",
            note("1"),
            " that WLC 4.22 has at ",
            vlist(["Exodus 10:28", "Joshua 22:19", "Jeremiah 47:6"]),
            ". morphhb's history names its updates to WLC 4.12 (",
            cmc("57e5e441"),
            "), 4.14 (",
            cmc("57206c9b"),
            "), 4.16 (",
            cmc("11626b6f"),
            "), 4.18 (",
            cmc("d1325011"),
            ") and 4.20 (",
            cmc("2201c6a7"),
            "), and none later.",
        ),
        p(
            "At ",
            vlist(["Deuteronomy 2:9", "Exodus 10:28", "Isaiah 23:8"]),
            ", WLC has a pashta twice in one atom: the pashta itself on the atom's last "
            "letter and its ",
            strong("stress helper"),
            ", a second pashta on the first letter of the stressed syllable. morphhb writes the "
            "helper with HEBREW ACCENT QADMA, the pashta's look-alike, where WLC has "
            "HEBREW ACCENT PASHTA, and has done so since ",
            cm("380f4219", msg=True),
            ". The review's forms carry no accents, so the review does not show this. In each "
            "row morphhb's atom stands above WLC 4.20's, accents shown.",
        ),
        helper_table(["Deut 2:9", "Exod 10:28", "Isa 23:8"]),
        p(
            "Since ",
            cm("73784451", msg=True),
            ", the main text of each Decalogue in morphhb has one of WLC's two accentuations, "
            "and a note of type alternative gives the other's reading of each word that "
            "differs. In the review's eight Decalogue rows, morphhb's main text keeps WLC "
            "4.18's form six times and changes it twice, at ",
            vref("Exodus 20:4", ex4["ib_form"]),
            " and at the first of the two rows of ",
            vref("Deuteronomy 5:8", dt8["ib_form"]),
            ". David Troidl described the division in a comment on ",
            issue(30),
            " (2017-03-04).",
        ),
    )


def section_review_cases():
    t = fjson("12-part1-table.json")["counts"]
    dec = [c for c in cases() if c["source"].startswith("review.md Decalogue")]
    assert len(dec) == 8 and sorted(c["class"] for c in dec) == ["c"] * 6 + ["d"] * 2
    return ht(
        heading(2, "The review's 56 cases", "review-cases"),
        p(
            "Of the review's 56 cases, morphhb corrects 5, all five of its al/el rows. Each "
            "case's form of the Israel Bible matches WLC 4.18 at exactly one place, and by "
            "Claude's reading of morphhb's text, lemma and morph there, each case is one of "
            "four kinds:"
        ),
        ol(
            [
                ht(
                    strong("A correction"),
                    f" ({t['b']} cases): the lemma, the morph or both fit only MAM's form.",
                ),
                ht(
                    strong("An analysis of WLC's form"),
                    f" ({t['a']} case): the lemma and the morph fit only WLC's form.",
                ),
                ht(
                    strong("An analysis that fits both forms"),
                    f" ({t['c']} cases): WLC's form and MAM's differ only in pointing that "
                    "neither the lemma nor the morph records.",
                ),
                ht(
                    strong("A text change"),
                    f" ({t['d']} cases): morphhb's text there is not WLC 4.18's.",
                ),
            ]
        ),
        subsection_five(),
        subsection_wlc_analysis(),
        subsection_text_changes(),
        subsection_both_forms(),
        subsection_hataf(),
        subsection_cases_show(),
    )


# ---------------------------------------------------------------- section 3: all of morphhb


def nine_words():
    """morphhb's word for each of the nine, as morphhb writes it."""
    out = {}
    for x in five():
        out[x["w"]["id"]] = x["w"]["text"] + (MAQAF if x["w"]["maqaf_after"] else "")
    c63 = check63()
    for r in nine()[5:]:
        w = c63[r["id"]]
        assert (w["lemma"], w["morph"]) == (r["lemma"], r["morph"]), r["verse"]
        # The table's forms are WLC 4.20's and MAM's as 63-check gives them, stripped.
        assert mnorm(review_stripped(w["src"]["WLC 4.20"])) == mnorm(r["wlc"]), r[
            "verse"
        ]
        assert mnorm(review_stripped(w["src"]["MAM"])) == mnorm(r["mam"]), r["verse"]
        out[r["id"]] = w["word"]
    return out


def nine_table():
    words = nine_words()
    rows = []
    for r in nine():
        rows.append(
            [
                wtd(words[r["id"]]),
                form_td(r["wlc"], r["mam"]),
                vcell(r["verse"], w=r["wlc"]),
                td(r["lemma"]),
                td(morph(r["morph"])),
                td(r["reads"]),
                td(
                    "none"
                    if r["notes"] == "none"
                    else notes_list([x.strip() for x in r["notes"].split(",")])
                ),
                td(cm(r["lemma_since"])),
                td(cm(r["morph_since"])),
            ]
        )
    return table(
        [
            "morphhb's word",
            "WLC 4.20 above MAM",
            "Verse",
            "Lemma",
            "Morph",
            "Reads MAM's form",
            "WLC's notes at the chanted word",
            "Lemma's number since",
            "Morph since",
        ],
        rows,
    )


def subsection_hosea():
    r = [x for x in nine() if x["verse"] == "Hosea 13:15"][0]
    w = check63()[r["id"]]
    src = w["src"]
    assert len({src[s] for s in ("WLC 4.18", "WLC 4.20", "WLC 4.22", "UXLC 2.6")}) == 1
    assert fkey(src["WLC 4.20"]) == fkey(w["word"]) and src["MAM"] != src["WLC 4.20"]
    assert w["notes"] == ["U"] and (w["lemma"], w["morph"]) == ("996", "HNcmsc")
    own = dict(w["own"])
    assert own.pop((w["lemma"], w["morph"])) == 1  # this word itself
    assert own == {("1121 a", "HNcmsa"): 83, ("1122", "HNp"): 1}, own
    mams = w["mam_form"]
    assert mams == {("996", "HR"): 167, ("997", "AR"): 1}, mams
    return ht(
        heading(3, "Hosea 13:15", "hosea"),
        p(
            "At ",
            vref("Hosea 13:15"),
            ", WLC 4.18, 4.20 and 4.22, UXLC 2.6 and morphhb's text have ",
            heb(src["WLC 4.20"]),
            ", ",
            dq("son"),
            ", without a yod, under WLC's note ",
            note("U"),
            "; MAM has ",
            heb(src["MAM"]),
            ", ",
            dq("between"),
            ". morphhb's lemma, 996, is ",
            dq("between"),
            ", the word MAM has, but its morph, ",
            morph(w["morph"]),
            ", a noun in the construct, fits ",
            dq("son"),
            ".",
        ),
        p(
            "morphhb gives lemma 996 to ",
            num(mams[("996", "HR")]),
            " of the ",
            num(sum(mams.values())),
            " other words with MAM's form, always with the morph ",
            morph("HR"),
            ", the preposition (the other is Aramaic, lemma 997), and it gives lemma 1121 a, ",
            dq("son"),
            ", to ",
            num(own[("1121 a", "HNcmsa")]),
            " of the ",
            num(sum(own.values())),
            " other words spelled as WLC spells this one (the other is a name, lemma 1122). "
            "Read as a defective spelling of ",
            dq("between"),
            ", the word would be an anomaly instead of a correction.",
        ),
    )


@lru_cache(maxsize=None)
def reasons61():
    """61-summary.txt's section 1: Claude's class and reason for each of the four further
    corrections, by morphhb id."""
    sec = between(ftext("61-summary.txt"), "== 1.", "== 2.")
    heads = found(r"^-- (.+?), morphhb id (\w{5})$", sec, 4)
    rs = found(r"^   Claude's class and reason: (\w+): (.+)$", sec, 4)
    out = {}
    for h, r in zip(heads, rs):
        assert r.group(1) == "correction"
        out[h.group(2)] = r.group(2)
    return out


def subsection_mappiq():
    rows = []
    c63 = check63()
    for r in nine()[6:]:
        w = c63[r["id"]]
        wlc, mam = w["src"]["WLC 4.20"], w["src"]["MAM"]
        # The two forms differ only by a mappiq in the last letter, a he.
        uw, um = L.units(mnorm(wlc)), L.units(mnorm(mam))
        assert [u[0] for u in uw] == [u[0] for u in um] and uw[-1][0] == LETTER_HE
        assert [L.unit_key(u) for u in uw[:-1]] == [L.unit_key(u) for u in um[:-1]]
        assert {uw[-1].replace(MAPIQ, ""), um[-1].replace(MAPIQ, "")} == {LETTER_HE}
        assert (MAPIQ in uw[-1]) != (MAPIQ in um[-1]), r["verse"]
        mam_suffix = MAPIQ in um[-1]
        # morphhb's division of the word and its morph follow MAM's form.
        assert ("/" in w["word"]) == mam_suffix == ("/Sp3fs" in w["morph"]), r["verse"]
        rows.append(
            [
                wtd(w["word"]),
                form_td(wlc, mam),
                vcell(r["verse"], w=wlc),
                td(morph(w["morph"])),
                td(L.morph_words(w["morph"])),
                note_td(coded(cap(reasons61()[r["id"]]) + ".", [w["morph"]])),
            ]
        )
    return ht(
        heading(3, "The three mappiq corrections", "mappiq"),
        p(
            "At each, WLC 4.20's form and MAM's differ only by a mappiq in the last letter, "
            "and that mappiq alone decides whether the word has a suffix: morphhb's text has "
            "WLC's form, but its division of the word, the ",
            code("/"),
            " before a suffix, and its morph follow MAM's form. In each row WLC 4.20's form "
            "stands above MAM's, accents shown; morphhb's word is as morphhb writes it.",
        ),
        table(
            [
                "morphhb's word",
                "WLC 4.20 above MAM",
                "Verse",
                "Morph",
                "What the morph says",
                "Claude's reason",
            ],
            rows,
        ),
    )


def subsection_suffix_cases():
    rows = []
    want = ["Genesis 34:11", "Isaiah 23:8", "Hosea 2:4", "Proverbs 31:12"]
    cs = [c for c in cases() if c["key"] in want]
    assert [c["key"] for c in cs] == want and all(c["class"] == "c" for c in cs)
    for c in cs:
        (w,) = c["morphhb"]
        assert re.search("/" + LETTER_HE + "[^/]*$", w["text"]), c["key"]
        assert w["morph"].endswith("/Sp3fs"), c["key"]
        rows.append(
            [
                wtd(w["text"]),
                form_td(c["ib_form"], c["mam_form"]),
                vcell(c["key"], w=c["ib_form"]),
                td(morph(w["morph"])),
            ]
        )
    return ht(
        heading(
            3, "Why the review's four suffix cases are not like these", "suffix-cases"
        ),
        p(
            "Four of the review's analyses that fit both forms end in a suffix, at ",
            vlist(want, [c["ib_form"] for c in cs]),
            ". There WLC's letters still show the suffix and only a vowel is missing, so one "
            "analysis fits both forms. In the three mappiq corrections the mappiq alone marks "
            "the suffix, so having it or not changes the analysis. In each row the Israel "
            "Bible's form, which is WLC 4.18's, stands above MAM's.",
        ),
        table(["morphhb's word", "Israel Bible above MAM", "Verse", "Morph"], rows),
    )


VERDICT = {
    "correction": "A correction",
    "slip": "A slip of morphhb's own",
    "anomaly": "An anomaly",
    "defensible": "Defensible",
    "noise": "Noise",
}
GROUPS = ("correction", "slip", "anomaly", "defensible")


def census_reason(r):
    """Claude's reason for a census verdict, as the census gives it, with its references to
    other ids and to the known cases put in the page's words."""
    s = r["verdict"][1]
    edits = {
        "02ubY": [(" (known case)", "")],
        "057a3": [(" (known case)", "")],
        "06Umo": [(" (known case)", "")],
        "07HwX": [(" (known case)", "")],
        "242CG": [(" (known case)", "")],
        "01bhs": [(" particle (lo), a slip", " particle, a slip")],
        "24JqK": [
            ("the patah form 249Bc carries", "the patah form of the next row carries")
        ],
        "249Bc": [("; see 24JqK", "; see the row above")],
    }
    for old, new in edits.get(r["id"], []):
        assert s.count(old) == 1, (r["id"], old)
        s = s.replace(old, new)
    return s


def census_counts():
    sec = between(ftext("50-alel-census.txt"), "== 1. Counts", "== 2.")
    n = int(
        one(r"^morphhb words whose last morpheme is alef-lamed: (\d+)$", sec).group(1)
    )
    m = one(
        r"^  of them aligned one to one with a MAM atom of the same letters: (\d+); "
        r"not: (\d+)$",
        sec,
    )
    mis = int(
        one(r"^mismatches: (\d+) \(the known five among them: 5\)$", sec).group(1)
    )
    by = one(
        r"^  by Claude's class: anomaly (\d+), correction (\d+), defensible (\d+), "
        r"slip (\d+)$",
        sec,
    )
    other = int(
        one(
            r"^alef-lamed words whose alef has another vowel in MAM's atom: (\d+)$", sec
        ).group(1)
    )
    out = dict(
        words=n,
        aligned=int(m.group(1)),
        not_aligned=int(m.group(2)),
        mismatches=mis,
        anomaly=int(by.group(1)),
        correction=int(by.group(2)),
        defensible=int(by.group(3)),
        slip=int(by.group(4)),
        other_vowel=other,
    )
    assert out == dict(
        words=4930,
        aligned=4924,
        not_aligned=6,
        mismatches=17,
        anomaly=1,
        correction=5,
        defensible=8,
        slip=3,
        other_vowel=6,
    ), out
    return out


def census_table():
    d, by_id = census()
    recs = [by_id[i] for i in d["mismatches"]]
    recs = sorted(recs, key=lambda r: GROUPS.index(r["verdict"][0]))
    reasons = [census_reason(r) for r in recs]
    codes = {r["morph"] for r in recs} | {"HR", "HTn", "ATn"}
    rows = []
    k = 0
    while k < len(recs):
        j = k
        while j + 1 < len(recs) and (recs[j + 1]["verdict"][0], reasons[j + 1]) == (
            recs[k]["verdict"][0],
            reasons[k],
        ):
            j += 1
        for i in range(k, j + 1):
            r = recs[i]
            cells = [
                wtd(chanted(r["morphhb_chanted_word"])),
                form_td(
                    chanted(r["sources"]["WLC 4.20"]["chanted_word"]),
                    chanted(r["sources"]["MAM"]["chanted_word"]),
                ),
                vcell(r["reference"], w=r["sources"]["WLC 4.20"]["atoms"][0]),
                td(r["lemma"]),
                td(morph(r["morph"])),
            ]
            if i == k:
                cells.append(
                    td(
                        ht(
                            VERDICT[r["verdict"][0]],
                            ": ",
                            coded(reasons[k], codes),
                            ".",
                        ),
                        cls="note",
                        rowspan=j - k + 1,
                    )
                )
            rows.append(cells)
        k = j + 1
    return table(
        [
            "morphhb's chanted word",
            "WLC 4.20 above MAM",
            "Verse",
            "Lemma",
            "Morph",
            "Claude's verdict",
        ],
        rows,
    )


def subsection_census():
    n = census_counts()
    d, by_id = census()
    ps = by_id["19HTT"]
    assert d["vowel_differences"] == [x["w"]["id"] for x in five()] + ["19HTT"]
    assert ps["reference"] == "Ps 35:22" and ps["verdict"][0] == "anomaly"
    return ht(
        heading(3, "The al/el census", "alel-census"),
        p(
            "No other correction of the al/el kind exists. Of morphhb's ",
            num(n["words"]),
            " words whose last morpheme has the letters alef and lamed, ",
            num(n["aligned"]),
            " align one to one with an atom of MAM's with the same letters, and ",
            str(n["mismatches"]),
            " have a vowel, lemma and morph that disagree: the ",
            str(n["correction"]),
            " corrections, ",
            str(n["slip"]),
            " slips of morphhb's own, ",
            str(n["anomaly"]),
            " anomaly and ",
            str(n["defensible"]),
            " defensible analyses, by Claude's verdicts. A slip is an inconsistency of "
            "morphhb's own, a lemma or morph that fits neither WLC's form nor MAM's where the "
            "two agree; an anomaly is a form of WLC's that is no regular word in its place, "
            "analysed as the word both transcriptions mean; a defensible analysis is a "
            "homograph's, or one that WLC's form admits as written. In each row WLC 4.20's "
            "chanted word stands above MAM's; morphhb's chanted word is shown with its "
            "accents.",
        ),
        census_table(),
        p(
            "Only six of the ",
            num(n["words"]),
            " have another vowel under the alef in MAM's atom than morphhb's text has: the "
            "five corrections and the anomaly at ",
            vref(ps["reference"]),
            ", where WLC 4.20 has ",
            heb(ps["sources"]["WLC 4.20"]["atoms"][0]),
            " and MAM ",
            heb(ps["sources"]["MAM"]["atoms"][0]),
            ".",
        ),
    )


def c61(label):
    return int(
        one(r"^   " + re.escape(label) + r"\s+(\d+)$", ftext("61-summary.txt")).group(1)
    )


@lru_cache(maxsize=None)
def flagged51():
    """51-general-test.txt's section 4: the eight pairs that the general test flags."""
    sec = between(ftext("51-general-test.txt"), "== 4. A1:", "== 5.")
    found(r"^-- ", sec, 8)
    out = []
    for b in re.split(r"^(?=-- )", sec, flags=re.M)[1:]:
        h = one(r"^-- (\S+ \d+:\d+)  id (\w{5})  sides \S+(.*)$", b)
        m = one(r"^   morphhb: (\S+)  lemma (.+?)  morph (\S+)$", b)
        v = one(r"^   verdict: (\w+): (.+)$", b)
        out.append(
            dict(
                ref=h.group(1),
                id=h.group(2),
                known="(known correction)" in h.group(3),
                word=m.group(1),
                lemma=m.group(2),
                morph=m.group(3),
                mam=one(r"^   MAM:     (\S+)$", b).group(1),
                wlc=one(r"^   WLC 4\.20: (\S+)   chanted word: .*$", b).group(1),
                verdict=v.group(1),
                reason=v.group(2),
            )
        )
    assert len(out) == 8
    return out


def x_counts():
    sec = between(ftext("51-general-test.txt"), "== 2. Counts", "== 3.")
    xs = found(r"^   X   (\S.*?)\s+(\d+)$", sec, 4)
    return {m.group(1): int(m.group(2)) for m in xs}


def subsection_general():
    a = c61("A. pairs (deduped by morphhb id and MAM's form key)")
    a1 = c61("A1. pairs whose own form has at least 5 other occurrences")
    a1_untestable = c61("A1.  of them, MAM's form absent from morphhb (untestable)")
    a1_flagged = c61("A1.  of them, flagged")
    a2 = c61("A2. pairs whose own form is rare (inconclusive)")
    a2_flagged = c61("A2.  of them, flagged by A or B")
    b = c61("B. letters-differ pairs (one-to-one non-equal blocks)")
    b_flagged = c61("B.  of them, flagged") + c61(
        "B.  of them, rare own form, flagged by back-off A or B"
    )
    hol = one(
        r"(\d,\d{3}) pairs differ only by a holam in MAM's form,\s+(\d,\d{3}) of them the "
        r"Tetragrammaton",
        ftext("61-summary.txt"),
    )
    xs = x_counts()
    assert (a, a1, a1_untestable, a1_flagged, a2, a2_flagged, b, b_flagged) == (
        7757,
        6892,
        49,
        8,
        865,
        54,
        1017,
        27,
    )
    assert xs == {"anomaly": 4, "correction": 2, "defensible": 1, "reads WLC": 6}, xs
    fl = flagged51()
    known = [x for x in fl if x["known"]]
    others = [x for x in fl if not x["known"]]
    assert [x["id"] for x in known] == [x["w"]["id"] for x in five()]
    assert [(x["ref"], x["verdict"]) for x in others] == [
        ("Exod 12:27", "noise"),
        ("Dan 3:15", "anomaly"),
        ("1Chr 29:16", "noise"),
    ]
    nr = wlc_note_rows()
    notes_total = one(
        r"^WLC notes in morphhb: (\d+); chanted words: (\d+)$",
        ftext("60-wlc-notes.txt"),
    )
    assert (int(notes_total.group(1)), int(notes_total.group(2))) == (1072, 800)
    assert (nr["U"]["chanted"], nr["U"]["differ"], nr["U"]["flagged"]) == (79, 59, 3)
    assert {k: v["flagged"] for k, v in nr.items() if v["flagged"]} == {"U": 3, "1": 1}
    rows = []
    for x in others:
        rows.append(
            [
                wtd(x["word"]),
                form_td(x["wlc"], x["mam"]),
                vcell(x["ref"], w=x["wlc"]),
                td(x["lemma"]),
                td(morph(x["morph"])),
                note_td(
                    VERDICT[x["verdict"]],
                    ": ",
                    coded(x["reason"], [x["morph"]]),
                    ".",
                ),
            ]
        )
    return ht(
        heading(3, "The general test and WLC's notes", "general-test"),
        p(
            "A general test of lemmas and morphs flags the review's five corrections and two of "
            "the four others; Claude's reading of pairs that no test flags found the other two, "
            "and WLC's notes point to no further correction. The test aligned morphhb's atoms "
            "with MAM's by letters, ketiv side with ketiv side and qere side with qere side, "
            "and took the ",
            num(a),
            " one-to-one pairs whose letters agree and whose forms differ by the review's key; ",
            hol.group(1),
            " of them differ only by a holam in MAM's form, ",
            hol.group(2),
            " of those in the Tetragrammaton. A word is flagged when its lemma, its morph or "
            "both are common among the other occurrences of MAM's form (at least 50%) and rare "
            "among those of its own form (at most 10% of at least 5).",
        ),
        ol(
            [
                ht(
                    "Of the ",
                    num(a1),
                    " pairs testable so, ",
                    str(a1_flagged),
                    " are flagged: the five corrections, an anomaly at ",
                    vref("Dan 3:15"),
                    " and two that are noise, at ",
                    vref("Exod 12:27"),
                    " and ",
                    vref("1 Chr 29:16"),
                    "; a looser grid of thresholds flags nothing more. The test flags all five "
                    "corrections and not ",
                    vref("Judges 19:4"),
                    ".",
                ),
                ht(
                    "Of the ",
                    num(a2),
                    " pairs whose own form is rarer, a back-off test flags ",
                    str(a2_flagged),
                    ", among which ",
                    vref("Genesis 39:19"),
                    " is the one correction.",
                ),
                ht(
                    "Of the ",
                    num(b),
                    " pairs whose letters differ, ",
                    str(b_flagged),
                    " are flagged, among which ",
                    vref("Hosea 13:15"),
                    " is the one correction.",
                ),
                ht(
                    "Claude's reading of ",
                    str(sum(xs.values())),
                    " pairs that no test flags found ",
                    vref("Deuteronomy 22:29"),
                    " and ",
                    vref("Leviticus 4:35"),
                    ".",
                ),
            ]
        ),
        p(
            "The three flagged words that are not corrections are these. In each row WLC "
            "4.20's form stands above MAM's, accents shown; morphhb's word is as morphhb "
            "writes it.",
        ),
        table(
            [
                "morphhb's word",
                "WLC 4.20 above MAM",
                "Verse",
                "Lemma",
                "Morph",
                "Claude's verdict",
            ],
            rows,
        ),
        p(
            "morphhb carries ",
            num(int(notes_total.group(1))),
            " of WLC's notes, on ",
            num(int(notes_total.group(2))),
            " chanted words. Of the ",
            str(nr["U"]["chanted"]),
            " chanted words under note ",
            note("U"),
            ", ",
            str(nr["U"]["differ"]),
            " differ from MAM, and the general test flags ",
            str(nr["U"]["flagged"]),
            ": ",
            vlist(["Deuteronomy 2:9", "Judges 19:23", "Hosea 13:15"]),
            ". Under the other letters it flags only ",
            vref("Daniel 3:15"),
            ", under note ",
            note("1"),
            ".",
        ),
    )


def section_all_morphhb():
    n9 = nine()
    deut = [r for r in n9 if r["verse"] == "Deuteronomy 22:29"][0]
    assert deut["lemma_since"] == "c299c30a"
    hist = ftext("71-history.txt")
    one(
        r"^   text: arrived between v24 and v25, i\.e\. with 57206c9b \(2011-01-22T00:01:58Z\): "
        r"Updated to WLC version 4\.14\.$",
        hist,
    )
    return ht(
        heading(2, "All of morphhb: nine corrections", "all-morphhb"),
        p(
            "morphhb has nine corrections in all: the review's five and four more. In each row "
            "WLC 4.20's form stands above MAM's, both as the review shows forms; morphhb's word "
            "is as morphhb writes it, its ",
            code("/"),
            " between morphemes included.",
        ),
        nine_table(),
        p(
            "The lemma's number is what the table dates: morphhb's augment letters and "
            "prefixes came in January 2011 (",
            cmc("b17c7e6e"),
            "; ",
            cmc("a52c1012"),
            "; ",
            cmc("fe661292"),
            "). At ",
            vref("Deuteronomy 22:29"),
            " morphhb's own text had the mappiq until its update to WLC 4.14 (",
            cmc("57206c9b"),
            ") brought WLC's form; the other eight texts have been as now since the first "
            "commit.",
        ),
        subsection_hosea(),
        subsection_mappiq(),
        subsection_suffix_cases(),
        subsection_census(),
        subsection_general(),
    )


# ---------------------------------------------------------------- section 4: the text


@lru_cache(maxsize=None)
def summary40():
    return ftext("40-text-compare-summary.txt")


def class_verses():
    sec = between(
        summary40(),
        "Verses with at least one unit of the class, against WLC 4.20:",
        "== 5.",
    )
    rows = found(r"^   (\S.*?)\s+(\d+)$", sec, 7)
    return {m.group(1): int(m.group(2)) for m in rows}


CLASSES = [
    (
        "qadma-for-first-pashta",
        "The pashta's stress helper written as a qadma",
        "text-helper",
    ),
    ("Decalogue/divided accents", "The divided accents", "text-divided"),
    ("mark encoding only", "Encoding only", "text-encoding"),
    (
        "word division",  # prose-ok: the report's label, quoted from its data
        "Atoms divided in two",
        "text-division",
    ),
    ("ketiv/qere representation", "Ketiv and qere", "text-kq"),
    ("paseq", "Paseq alone", None),
    ("residual", "Anything else", None),
]


def subsection_version():
    t = summary40()
    v18 = one(
        r"^morphhb vs WLC 4\.18: (\d+) residual units .*; WLC 4\.20 has morphhb's reading in "
        r"full at (\d+)\.$",
        t,
    )
    v22 = one(
        r"^morphhb vs WLC 4\.22: (\d+) residual units .*; WLC 4\.20 has morphhb's reading in "
        r"full at (\d+)\.$",
        t,
    )
    assert (v18.groups(), v22.groups()) == (("16", "16"), ("38", "36"))
    nl = one(
        r"verses that differ from morphhb: WLC 4\.18 (\d+),\s+WLC 4\.20 (\d+), WLC 4\.22 (\d+)",
        t,
    )
    t45 = ftext("45-text-version-evidence.txt")
    lev = one(
        r"^  Lev 13:3\s+\[residual/pointing\] morphhb: (\S+) \| WLC 4\.22: (\S+) \| "
        r"WLC 4\.20: (\S+) \[skey\]$",
        t45,
    )
    dan = one(
        r"^  Dan 2:39\s+\[residual/accents\] morphhb: \[q\](\S+) \| WLC 4\.22: \[q\](\S+) \| "
        r"WLC 4\.20: \(nothing\) \[no\]$",
        t45,
    )
    # Leviticus 13:3: morphhb differs from WLC 4.20 only by the stress helper's qadma, and WLC
    # 4.22 has a segol where both have a patah.
    lev_m, lev_22, lev_20 = lev.groups()
    check_helper(lev_m, lev_20, "Lev 13:3")
    u20, u22 = L.units(mnorm(lev_20)), L.units(mnorm(lev_22))
    diff = [(a, b) for a, b in zip(u20, u22) if L.unit_key(a) != L.unit_key(b)]
    assert len(u20) == len(u22) and len(diff) == 1
    assert (
        "\N{HEBREW POINT PATAH}" in diff[0][0]
        and "\N{HEBREW POINT SEGOL}" in diff[0][1]
    )
    # Daniel 2:39: morphhb's qere has no accent where WLC 4.22's has a munax.
    dan_m, dan_22 = dan.groups()
    assert fkey(dan_m) == fkey(dan_22.replace("\N{HEBREW ACCENT MUNAH}", ""))
    assert "\N{HEBREW ACCENT MUNAH}" in dan_22
    return ht(
        heading(3, "Which version", "text-version"),
        p(
            "Once the systematic classes are taken out, nothing is left against WLC 4.20. "
            "Against WLC 4.18, ",
            v18.group(1),
            " units are left, and WLC 4.20 has morphhb's reading at all ",
            v18.group(2),
            "; against WLC 4.22, ",
            v22.group(1),
            " are left, and WLC 4.20 has morphhb's reading at ",
            v22.group(2),
            ". WLC's notes agree: morphhb's note letters differ from WLC 4.18's in ",
            nl.group(1),
            " verses, from WLC 4.20's in ",
            nl.group(2),
            " and from WLC 4.22's in ",
            nl.group(3),
            ". The two places where WLC 4.20 does not have morphhb's reading in full are "
            "these. "
            "In the first row morphhb's atom stands above WLC 4.20's and WLC 4.22's; in the "
            "second, morphhb's qere stands above WLC 4.22's, since WLC 4.20 has no qere there. "
            "Accents are shown.",
        ),
        table(
            ["Forms", "Verse", "What differs"],
            [
                [
                    form_td(lev_m, lev_20, lev_22),
                    vcell("Lev 13:3"),
                    note_td(
                        "WLC 4.22 has a segol where morphhb and WLC 4.20 have a patah; "
                        "morphhb's atom differs from WLC 4.20's only in writing the pashta's "
                        "stress helper as a qadma, so the two are equal by the review's key."
                    ),
                ],
                [
                    form_td(dan_m, dan_22),
                    vcell("Dan 2:39", extra="qere"),
                    note_td(
                        "morphhb's qere has no accent where WLC 4.22's has HEBREW ACCENT "
                        "MUNAH; WLC 4.20 has one atom here and no qere."
                    ),
                ],
            ],
        ),
    )


def subsection_classes():
    d40 = fjson("40-text-compare-data.json")
    cu = d40["class_units"]["4.20"]
    assert cu == {
        "qadma-for-first-pashta": 3811,
        "Decalogue/divided accents": 122,
        "mark encoding only": 82,
        "word division": 12,  # prose-ok: the report's label, quoted from its data
        "ketiv/qere representation": 1,
    }, cu
    vs = class_verses()
    assert list(vs) == [k for k, _n, _i in CLASSES], vs
    rows = []
    for k, title, id_ in CLASSES:
        rows.append(
            [
                td(here(id_, title) if id_ else title),
                td(num(cu.get(k, 0)), cls="num"),
                td(num(vs[k]), cls="num"),
            ]
        )
    return ht(
        heading(3, "The classes against WLC 4.20", "text-classes"),
        p(
            "Every unit that differs falls into one of these classes, counted in units, a unit "
            "being a differing pair of atoms or a group of atoms that differ together, and in "
            "the verses that have one:"
        ),
        table(["Class", "Units", "Verses"], rows),
    )


def subsection_helper():
    d40 = fjson("40-text-compare-data.json")
    q4 = d40["qstats"]
    other = q4[
        "morphhb differs, qadma_test=qadma, divided-accents verse=False; WLC: 2 pashtas, the "
        "last on the atom's last letter=True"
    ]
    inside = q4[
        "morphhb differs, qadma_test=qadma, divided-accents verse=True; WLC: 2 pashtas, the "
        "last on the atom's last letter=True"
    ]
    assert (other, inside) == (3807, 4)
    one(
        r"^   Every WLC 4\.20 atom with two pashtas or more has exactly two, the last on the "
        r"atom's last$",
        summary40(),
    )
    vs = class_verses()["qadma-for-first-pashta"]
    return ht(
        heading(3, "The pashta's stress helper written as a qadma", "text-helper"),
        p(
            "Where WLC 4.20 writes a pashta twice in an atom, its stress helper on the "
            "stressed syllable and the pashta itself on the last letter, morphhb writes the "
            "helper with HEBREW ACCENT QADMA: ",
            num(d40["label_units"]["4.20"]["qadma"]),
            " units in ",
            num(vs),
            " verses. Every WLC 4.20 atom with two pashta accents or more has exactly two, the "
            "last "
            "on the atom's last letter, and outside the verses with divided accents every one "
            "is such a unit. In each row morphhb's atom stands above WLC 4.20's.",
        ),
        helper_table(["Gen 1:2", "Exod 10:28", "Deut 2:9", "Isa 23:8"]),
        p(
            "morphhb has written the helper so since ",
            cm("380f4219", msg=True),
            ". The versions of each book that the report fetched date this exactly in "
            "Deuteronomy, the one book with a fetched version just before that commit, and "
            "bracket it in seven other books.",
        ),
    )


@lru_cache(maxsize=None)
def catchword():
    t = ftext("46-text-divided-accents.txt")
    one(r"^catchWord atoms whose marks differ from the main text they name: 1$", t)
    m = one(
        r"^  Deut 5:8\s+main text: (\S+) \| catchWord atom: (\S+)\s+"
        r"\(catchWord (.+?); x-accent (.+)\)$",
        t,
    )
    main, atom, whole, x_accent = m.groups()
    a, _aq = atom_marks(main)
    b, _bq = atom_marks(atom)
    lack = [
        name(ch) for (_l, ca), (_l2, cb) in zip(a, b) for ch in (ca - cb).elements()
    ]
    assert lack == ["HEBREW ACCENT MUNAH"] and all(
        not (cb - ca) for (_l, ca), (_l2, cb) in zip(a, b)
    )
    return dict(main=main, atom=atom, whole=whole, x_accent=x_accent)


def subsection_divided():
    d40 = fjson("40-text-compare-data.json")
    lu = d40["label_units"]["4.20"]
    ds = d40["dstats"]
    with_note = {k: v for k, v in ds.items() if "alternative note: yes" in k}
    assert sum(with_note.values()) == 123 == d40["alt_cover"]["alternative-note atoms"]
    not_union = sum(v for k, v in with_note.items() if not k.endswith(": ok"))
    assert not_union == 6
    assert (
        lu["divided-accents/accents"],
        lu["divided-accents/accents+paseq"],
        lu["divided-accents/pointing"],
    ) == (108, 9, 5)
    vs = class_verses()["Decalogue/divided accents"]
    rows = []
    for x in decalogue_units():
        rows.append(
            [
                form_td(x["main"], x["alt"]),
                form_td(x["wlc"], x["_display"]["MAM"]),
                vcell(x["reference"], w=x["wlc"]),
                note_td(x["what"]),
            ]
        )
    cw = catchword()
    return ht(
        heading(
            3, "The divided accents of the Decalogues and Genesis 35:22", "text-divided"
        ),
        p(
            "In the ",
            str(vs),
            " verses of the Decalogues and ",
            vref("Genesis 35:22"),
            ", where WLC 4.20 writes two accentuations at once, morphhb's main text has one of "
            "them and a note of type alternative gives the other's reading of each word that "
            "differs. These verses have ",
            str(d40["class_units"]["4.20"]["Decalogue/divided accents"]),
            " units: ",
            str(lu["divided-accents/accents"]),
            " differ only in accents, ",
            str(lu["divided-accents/accents+paseq"]),
            " also in a paseq, which belongs to the other accentuation and stands in the "
            "alternative note, and ",
            str(lu["divided-accents/pointing"]),
            " in a vowel or the maqaf.",
        ),
        p(
            "The union test asks whether WLC 4.20's atom has, letter by letter, the marks of "
            "morphhb's main text and of its alternative note together, a maqaf if either has "
            "one, and no others. Of the ",
            str(sum(with_note.values())),
            " atoms that carry an alternative note, WLC 4.20's atom is that union at all but "
            "six. Of those six, three differ in a vowel or the maqaf, one in a meteg and two in "
            "an accent. At two more atoms morphhb's main text lacks WLC 4.20's maqaf and the "
            "alternative note has it, so that at five atoms in all the main text differs from "
            "WLC 4.20 in a vowel or the maqaf. The table's first six rows are the six atoms, "
            "and its last two rows the two. In each row the first cell has morphhb's main text "
            "above its alternative note, and the second WLC 4.20's atom above MAM's; accents "
            "are shown.",
        ),
        table(
            [
                "morphhb's main text above its alternative note",
                "WLC 4.20 above MAM",
                "Verse",
                "What differs",
            ],
            rows,
        ),
        p(
            "At ",
            vref("Deuteronomy 5:8", cw["main"]),
            " one alternative note's catchWord, which quotes the words of the main text that "
            "the note's reading replaces, does not match them: in its first atom it lacks the "
            "HEBREW ACCENT MUNAH of the main text's atom. In the row the main text's atom "
            "stands above the catchWord's.",
        ),
        table(
            ["Main text above catchWord", "Verse", "The note"],
            [
                [
                    form_td(cw["main"], cw["atom"]),
                    vcell("Deut 5:8", w=cw["main"]),
                    note_td(
                        "The catchWord is ",
                        heb(cw["whole"]),
                        "; the note's reading is ",
                        heb(cw["x_accent"]),
                        ".",
                    ),
                ]
            ],
        ),
    )


def zwj_lines():
    sec = between(
        ftext("43-text-class-lists.txt"),
        "######## zwj (class",
        "######## word-division (class",  # prose-ok: the report's heading, quoted
    )
    ms = found(
        r"^\S+ \d+:\d+\s+morphhb: (\S+(?: \S+)?)  \|  WLC 4\.20: (\S+(?: \S+)?)  "
        r"\[morphhb \+-; WLC \+zero width joiner\]$",
        sec,
        79,
    )
    for m in ms:
        assert L.ZWJ + "\N{HEBREW POINT METEG}" in m.group(2) and L.ZWJ not in m.group(
            1
        )
    return ms


def subsection_encoding():
    lu = fjson("40-text-compare-data.json")["label_units"]["4.20"]
    assert (lu["zwj"], lu["final-form"]) == (79, 3)
    zwj_lines()
    a = ftext("78-check-zwj-qadma-history.txt")
    one(
        r"^   TOTAL          zwj=    0 qadma=11369 pashta=20647 cgj=    0 zwnj=    0$",
        a,
    )
    ff = units_labelled("final-form")
    assert [u["reference"] for u in ff] == ["Isa 9:6", "Job 38:1", "Job 40:6"]
    rows = []
    for u in ff:
        mine, w18, w20 = (unk(u["_display"][k]) for k in ("morphhb", "4.18", "4.20"))
        w22 = unk(u["_display"]["4.22"])
        assert (
            u["agree_with_morphhb"]["4.18"] == u["agree_with_morphhb"]["UXLC"] == "full"
        )
        assert u["agree_with_morphhb"]["4.22"] == "no"
        assert u["agree_with_wlc_4.20"]["4.22"] == "full" and w22 == w20
        if u["reference"] == "Isa 9:6":
            assert "\N{HEBREW LETTER FINAL MEM}" in mine[:-1]
            assert "\N{HEBREW LETTER FINAL MEM}" not in w20
        else:
            assert mine.endswith("\N{HEBREW LETTER NUN}")
            assert w20.endswith("\N{HEBREW LETTER FINAL NUN}")
        (ns,) = [x["notes"] for x in u["wlc_4.20"]]
        assert len(ns) == 1
        rows.append(
            [
                form_td(mine, w18, w20),
                vcell(u["reference"], extra="ketiv"),
                td(ht("note ", note(ns[0]))),
            ]
        )
    return ht(
        heading(3, "Encoding only", "text-encoding"),
        p(
            "Encoding accounts for ",
            str(lu["zwj"] + lu["final-form"]),
            " units: ",
            str(lu["zwj"]),
            " are a ZERO WIDTH JOINER, which WLC 4.18, 4.20 and 4.22 have before a medial "
            "meteg and morphhb lacks; morphhb's files have no joiner anywhere. The joiner is "
            "invisible, so no form here shows it. The versions of each book that the report "
            "fetched date its removal exactly only in Deuteronomy and Hosea, to ",
            cm("56b51322", msg=True),
            ", and bracket it in Jeremiah, Judges and Leviticus.",
        ),
        p(
            "The other three are the letter forms of ketiv words: at ",
            vref("Isaiah 9:6"),
            " a final mem inside the word, and at ",
            vref("Job 38:1"),
            " and ",
            vref("Job 40:6"),
            " a medial nun at its end, which WLC 4.20's notes ",
            note("F"),
            " and ",
            note("M"),
            " mark. morphhb, WLC 4.18 and UXLC 2.6 have these letter forms; MAM-basics' "
            "conversions of WLC 4.20 and 4.22 give every letter at the end of a word its final "
            "form and no other letter one. In each row morphhb's ketiv stands above WLC 4.18's "
            "and WLC 4.20's.",
        ),
        table(
            ["morphhb above WLC 4.18 above WLC 4.20", "Verse", "WLC 4.20's note"], rows
        ),
    )


def subsection_division():
    us = units_labelled("word-division")  # prose-ok: the report's label, quoted
    assert len(us) == 12
    rows = []
    texts = set()
    for u in us:
        mine, w20, mam = (u["_display"][k] for k in ("morphhb", "4.20", "MAM"))
        kinds = {x["kind"] for x in u["morphhb"]}
        assert len(u["morphhb"]) == 2 and len(u["wlc_4.20"]) == 1
        assert letters(unk(mine)) == letters(unk(w20)), u["reference"]
        (en,) = u["exegesis_notes"]
        assert en["rdg"] is None
        texts.add(en["text"])
        rows.append(
            [
                form_td(unk(mine), unk(w20), unk(mam)),
                vcell(u["reference"], extra="ketiv" if kinds == {"ketiv"} else None),
                note_td(q(en["text"])),
            ]
        )
    assert len(texts) == 1
    return ht(
        heading(3, "Atoms divided in two", "text-division"),
        p(
            "At 12 places morphhb divides one of WLC 4.20's atoms in two, each with a note of "
            "type exegesis. In each row morphhb's two atoms stand above WLC 4.20's one and "
            "above MAM's form, accents shown.",
        ),
        table(
            ["morphhb above WLC 4.20 above MAM", "Verse", "morphhb's exegesis note"],
            rows,
        ),
    )


def subsection_kq():
    (u,) = units_labelled("kq-structure")
    assert u["reference"] == "Dan 2:39"
    srcs = [
        ("morphhb", u["morphhb"]),
        ("WLC 4.18", u["others"]["4.18"]),
        ("WLC 4.20", u["wlc_4.20"]),
        ("WLC 4.22", u["others"]["4.22"]),
        ("UXLC 2.6", u["others"]["UXLC"]),
        ("MAM", u["others"]["MAM"]),
    ]
    rows = []
    for nm, atoms in srcs:
        ks = [x["kind"] for x in atoms]
        if len(atoms) == 2:
            assert ks[1] == "qere" and ks[0] in ("ketiv", "plain"), (nm, ks)
            what = "its ketiv above its qere"
        else:
            assert ks == ["plain"], (nm, ks)
            what = "one atom, with no ketiv or qere"
        rows.append(
            [
                td(
                    stack(*[x["text"] for x in atoms], highlight=False),
                    cls="form",
                    rtl=True,
                ),
                td(ht(nm, ": ", what)),
            ]
        )
    (en,) = u["exegesis_notes"]
    qere = u["morphhb"][1]["text"]
    assert not any("ACCENT" in name(ch) for ch in qere), ascii(qere)
    assert any("ACCENT" in name(ch) for ch in u["others"]["4.22"][1]["text"])
    probes = ftext("72-dan239-probes.txt")
    for sha, kq in (("019b22f6", "True"), ("bc20b79b", "True"), ("f0b4e882", "False")):
        one(r"^v\d+ \S+ " + sha + r" ketiv/qere=" + kq + " ", probes)
    one(r"^v55 \S+ 456c54c6 ketiv/qere=True ", probes)
    return ht(
        heading(3, "Ketiv and qere", "text-kq"),
        p(
            "At ",
            vref("Daniel 2:39"),
            " morphhb has a ketiv and a qere for WLC 4.20's single atom, as WLC 4.22, UXLC 2.6 "
            "and MAM do; morphhb's qere has no accent. Its note of type exegesis there says ",
            q(en["text"]),
            " Each row gives one source's form, accents shown.",
        ),
        table(["Form", "Source"], rows),
        p(
            "morphhb's ketiv and qere arrived with ",
            cm("019b22f6", msg=True),
            ", were undone and redone, and have stood since ",
            cm("456c54c6", msg=True),
            ".",
        ),
    )


def subsection_checks():
    t48 = ftext("48-check-marks.txt")
    other = between(t48, "== other verses", "== divided-accent verses")
    pat = r"^   {} pashta\s+(\d+)  qadma\s+(\d+)  pashta\+qadma\s+(\d+)  zwj\s+(\d+)"
    mine = [int(x) for x in one(pat.format("morphhb "), other).groups()]
    w20 = [int(x) for x in one(pat.format(r"WLC 4\.20"), other).groups()]
    assert w20[0] - mine[0] == mine[1] - w20[1] == 3807 and mine[2] == w20[2]
    assert (mine[3], w20[3]) == (0, 79)
    one(
        r"^qadma-class units by verse kind: \{'other': 3807, 'divided': 4\}$",
        ftext("48-check-qadma-units.txt"),
    )
    return ht(
        heading(3, "Checks", "text-checks"),
        p(
            "A rerun of the comparison reproduced its summary byte for byte. Independently, "
            "outside the 24 verses with divided accents, morphhb has ",
            num(w20[0] - mine[0]),
            " fewer pashta accents and ",
            num(mine[1] - w20[1]),
            " more qadma accents than WLC 4.20, with the same total of the two, and the units "
            "of the "
            "stress-helper class number 3,807 there and 4 inside them. WLC 4.18, 4.20 and 4.22 "
            "each have 79 zero width joiners and morphhb none; morphhb's files at ",
            commit("d4265dfa"),
            ", notes and headers included, have no ZERO WIDTH JOINER, COMBINING GRAPHEME "
            "JOINER or ZERO WIDTH NON-JOINER. No commit message, issue or comment of morphhb's "
            "mentions the joiners of its WLC files.",
        ),
    )


def section_text():
    return ht(
        heading(2, "morphhb's text against WLC 4.20", "text"),
        p(
            "morphhb's text is WLC 4.20's. Compared atom by atom over all ",
            num(fjson("40-text-compare-data.json")["kstats"]["4.20"]["verses"]),
            " verses, every difference falls into a systematic class and none is left over. "
            "Beyond accents and encoding, morphhb's text differs from WLC 4.20 only at five "
            "atoms of the Decalogues, in a vowel or the maqaf (at three of them morphhb's "
            "alternative-accent note does not supply WLC 4.20's reading); at ",
            vref("Daniel 2:39"),
            ", where morphhb has a ketiv and a qere for WLC 4.20's one atom; and at 12 words "
            "that morphhb divides for exegesis.",
        ),
        p(
            "The comparison turned every verse of every source into atoms, with morphhb's ",
            code("/"),
            ", sof pasuq and white space dropped, a maqaf kept and a paseq as a flag; keyed "
            "them with every mark kept and each letter's marks sorted; aligned them by "
            "letters; and gave each difference one class by an explicit test.",
        ),
        subsection_version(),
        subsection_classes(),
        subsection_helper(),
        subsection_divided(),
        subsection_encoding(),
        subsection_division(),
        subsection_kq(),
        subsection_checks(),
    )


# ---------------------------------------------------------------- section 5: the records


@lru_cache(maxsize=None)
def text_places():
    """73-text-places.txt: the five places where a commit whose message names a correction
    changed the text."""
    t = ftext("73-text-places.txt")
    heads = found(r"^-- (\S+) \[(\w+)\]$", t, 5)
    out = []
    for h in heads:
        b = block_after(t, h.group(0))
        old = one(r"^   old \(before (\w+)\)\s+(\S+)  \[", b)
        new = one(r"^   new \(from (\w+)\)\s+(\S+)  \[", b)
        w18 = one(r"^   WLC 4\.18\s+(\S+)  \[", b).group(1)
        w20 = one(r"^   WLC 4\.20\s+(\S+)  \[", b).group(1)
        assert old.group(1) == new.group(1)
        assert fkey(new.group(2)) == fkey(w20), h.group(1)
        out.append(
            dict(
                osis=h.group(1),
                kind=h.group(2),
                sha=old.group(1),
                old=old.group(2),
                new=new.group(2),
                w18=w18,
            )
        )
    for x in out:
        if x["sha"] == "c8f43473":
            assert fkey(x["old"]) == fkey(x["w18"]), x["osis"]
    assert [(x["osis"], x["sha"], x["kind"]) for x in out] == [
        ("Job.19.2", "6887dd0a", "letters"),
        ("Prov.1.28", "6887dd0a", "letters"),
        ("2Kgs.21.26", "c8f43473", "vowel"),
        ("Gen.5.29", "c8f43473", "accent"),
        ("Zeph.2.15", "c8f43473", "accent"),
    ]
    return out


KIND_WORDS = {"letters": "a letter", "vowel": "a vowel", "accent": "an accent"}


def section_records():
    rows = []
    for x in text_places():
        rows.append(
            [
                form_td(x["old"], x["new"]),
                vcell(x["osis"]),
                td(cm(x["sha"])),
                td(KIND_WORDS[x["kind"]]),
            ]
        )
    rd = one(
        r"^# revisionDesc entries: (\d+) in (\d+) books; (\d+) distinct",
        ftext("74-revisiondesc.txt"),
    )
    assert rd.groups() == ("273", "39", "12")
    one(
        r"^== Entries that describe a correction of the text or of the analysis\n   none$",
        ftext("74-revisiondesc.txt"),
    )
    ex = ftext("74-exegesis-notes.txt")
    one(r"^# exegesis notes: 21\.", ex)
    one(r"^   9 x WLC has this word divided as <rdg>\.: ", ex)
    one(r"^   12 x A single word in the text has been divided for exegesis\.: ", ex)
    t75 = ftext("75-issues.txt")
    counts = one(
        r"\((\d+) issues and PRs,\s*#?\s*(\d+) comments, (\d+) review comments\)", t75
    )
    assert counts.groups() == ("117", "390", "6")
    quote = one(r"Troidl \(2017-02-03\): '([^']+)'", t75).group(1).rstrip(".")
    assert len(quote.split()) < 15
    return ht(
        heading(2, "morphhb's own records", "records"),
        p(
            "No record of morphhb's own describes any of the nine corrections: no commit "
            "message, header revision entry, exegesis note, issue, pull request or comment."
        ),
        p(
            "Of the commits whose messages name a correction without saying what it is, only "
            "two change the text, and both bring it to WLC's: ",
            cm("6887dd0a", msg=True),
            " removed a letter that morphhb's own text had added at ",
            vref("Job 19:2"),
            " and at ",
            vref("Proverbs 1:28"),
            ", and ",
            cm("c8f43473", msg=True),
            " changed a vowel at ",
            vref("2 Kings 21:26"),
            " and an accent at ",
            vref("Genesis 5:29"),
            " and ",
            vref("Zephaniah 2:15"),
            " from WLC 4.18's readings to WLC 4.20's. The other such commits change lemmas, "
            "morphs, the n attribute or markup, and none touches the nine words. In each row "
            "morphhb's form before the commit stands above its form from the commit on, which "
            "is WLC 4.20's; accents shown.",
        ),
        table(["morphhb before above after", "Verse", "Commit", "What changed"], rows),
        p(
            "The files' headers have ",
            rd.group(1),
            " revision entries in ",
            rd.group(2),
            " books, ",
            rd.group(3),
            " of them distinct: the conversion of 2008, the updates to WLC 4.14 to 4.20 and "
            "the releases of the morphology. None names a correction.",
        ),
        p(
            "Of morphhb's 21 exegesis notes, 12 mark the atoms divided in two, and the other "
            "9 say ",
            q("WLC has this word divided as"),
            " and give WLC's form, ",
            vref("Daniel 2:39"),
            "'s among them.",
        ),
        p(
            "No issue, pull request or comment of openscriptures/morphhb mentions any of the "
            "nine verses, ",
            vref("Jeremiah 51:3"),
            " or ",
            vref("Daniel 2:39"),
            ": ",
            counts.group(1),
            " issues and pull requests, ",
            counts.group(2),
            " comments and ",
            counts.group(3),
            " review comments, fetched on 2026-11-13, were searched for each verse in several "
            "spellings and for the words' ids. In ",
            issue(27),
            ", David Troidl wrote on 2017-02-03 that ",
            q(quote),
            ". In ",
            issue(30),
            " he described the Decalogues' division (2017-03-04). The open ",
            issue(113),
            " reports swapped lemmas at ",
            vref("1 Chronicles 12:39"),
            " and ",
            vref("2 Chronicles 3:17"),
            "; the two words at ",
            vref("Jeremiah 51:3"),
            " that carry each other's lemmas are reported nowhere.",
        ),
    )


# ---------------------------------------------------------------- section 6: the limits


def section_limits():
    t58 = ftext("58-ketiv-qere-analyses.txt")
    k = one(r"^  different lemma main number\s+(\d+)$", t58).group(1)
    assert k == "205"
    untestable = c61("A1.  of them, MAM's form absent from morphhb (untestable)")
    xs = sum(x_counts().values())
    return ht(
        heading(2, "What these methods cannot find", "limits"),
        p("Six kinds of correction are beyond these methods:"),
        ol(
            [
                "A correction where WLC and MAM agree, or where the lemma and morph are the "
                "same for both forms.",
                "A correction carried by marks that the review's key strips, such as accents.",
                ht(
                    "A correction at a word whose own form is too rare for the general test, "
                    "beyond what the back-off test and Claude's reading of ",
                    str(xs),
                    " pairs caught, and at the ",
                    str(untestable),
                    " pairs whose MAM form never occurs in morphhb.",
                ),
                "A letter difference outside a one-to-one block of the alignment.",
                ht(
                    "A ketiv analysed by its qere: at ",
                    vref("Isaiah 52:5"),
                    " the ketiv carries the qere's lemma, while ",
                    k,
                    " other ketiv words carry their own.",
                ),
                "Anything about the Leningrad Codex itself: no image was consulted.",
            ]
        ),
    )


# ---------------------------------------------------------------- departures


def departures():
    decalogue = {x["id"]: x for x in decalogue_units()}
    v1, v2 = decalogue["059vS"], decalogue["05fou"]
    readme = (L.F / "README.md").read_text(encoding="utf-8")
    d1_quote = (
        "Changes of letters, vowels or maqaf are confined to three words of the Decalogues, "
        "Daniel 2:39's ketiv and qere and the 12 words that morphhb divides for exegesis."
    )
    assert " ".join(readme.split()).count(d1_quote) == 1
    d2_quote = "where morphhb agrees with WLC 4.18 and only MAM-basics' conversion of WLC 4.20 differs"
    assert " ".join(readme.split()).count(d2_quote) == 1
    d3_quote = "morphhb has HEBREW ACCENT QADMA on the first syllable where WLC has a second pashta"
    assert readme.count(d3_quote) == 1
    assert (
        " ".join(readme.split()).count("HEBREW ACCENT QADMA on the stressed syllable")
        == 1
    )
    for heading_ in (
        "## Part 2: all other such corrections in morphhb",
        "### Method 3: morphhb's text against WLC 4.18, 4.20 and 4.22",
        "### What the cases show about morphhb's text",
        "### Every case",
    ):
        assert readme.count("\n" + heading_ + "\n") == 1, heading_
    # The README's table counts Deuteronomy 5:8's first row as a text change for its maqaf.
    (d8,) = [c for c in cases() if c["key"] == "Deut 5:8 (Decalogue row 6)"]
    assert d8["class"] == "d" and "no maqaf after the second atom" in d8["what"]
    # In 41-text-residuals.json WLC 4.22's conversion has WLC 4.20's letter forms (encoding).
    ff = units_labelled("final-form")
    assert all(u["agree_with_morphhb"]["4.22"] == "no" for u in ff)
    return [
        ht(
            strong("The Decalogues' vowels and maqaf."),
            " The report's README, under ",
            q("Part 2: all other such corrections in morphhb"),
            ", ",
            q("The answer"),
            ", item 4, says: ",
            q(d1_quote),
            " Its three are the atoms where WLC 4.20's atom is not the union of morphhb's main "
            "text and its alternative-accent note and the difference is a vowel or the maqaf. "
            "But the report's ",
            code("out/41-text-residuals.json"),
            " has five units labelled ",
            code("divided-accents/pointing"),
            " (the label's count in ",
            code("out/40-text-compare-data.json"),
            " is 5), and at two of them, the verb ",
            heb(v1["main"]),
            " at ",
            vref("Deuteronomy 5:7", v1["main"]),
            " and the verb ",
            heb(v2["main"]),
            " at ",
            vref("Deuteronomy 5:8", v2["main"]),
            ", morphhb's main text lacks WLC 4.20's maqaf while its alternative note has it, "
            "so that the union test passes there. The README's own table of the review's "
            "cases, under ",
            q("Every case"),
            ", counts the second as a text change for that missing maqaf. This page says both: "
            "at five atoms morphhb's main text differs from WLC 4.20 in a vowel or the maqaf, "
            "and at three of them the alternative note does not make it good.",
        ),
        ht(
            strong("Three ketiv words' letter forms."),
            " The README, under ",
            q("Method 3: morphhb's text against WLC 4.18, 4.20 and 4.22"),
            ", item 2.3, says of the three ketiv words' letter forms ",
            q(d2_quote),
            ". In the report's ",
            code("out/41-text-residuals.json"),
            " MAM-basics' conversion of WLC 4.22 has WLC 4.20's letter forms at all three, and "
            "UXLC 2.6 has morphhb's. This page names both conversions.",
        ),
        ht(
            strong("A stress helper's syllable."),
            " The README's table of the review's cases, ",
            q("Every case"),
            ", says at ",
            vref("Isaiah 23:8"),
            ": ",
            q(d3_quote),
            ". In the report's ",
            code("out/43-text-class-lists.txt"),
            " morphhb's HEBREW ACCENT QADMA there is on the resh, which begins the stressed "
            "syllable, not the first; the README itself says ",
            q("on the stressed syllable"),
            " of the same place under ",
            q("What the cases show about morphhb's text"),
            ". This page says the stressed syllable.",
        ),
    ]


# ---------------------------------------------------------------- exports

SECTIONS = [
    ("answer", "The answer in brief", section_answer),
    ("review-cases", "The review's 56 cases", section_review_cases),
    ("all-morphhb", "All of morphhb: nine corrections", section_all_morphhb),
    ("text", "morphhb's text against WLC 4.20", section_text),
    ("records", "morphhb's own records", section_records),
    ("limits", "What these methods cannot find", section_limits),
]


def self_test(built, departures_):
    """The checks of the scratch script's self-test, on the sections as the generator built
    them, each an (id, title, section) triple: each section opens with its heading, no id is
    used twice, and each departure is HTML."""
    ids = []
    for id_, title, sec in built:
        assert isinstance(sec, H), id_
        assert sec.startswith(heading(2, title, id_)), id_
        ids += re.findall(r'\bid="([^"]+)"', sec)
    assert [b[0] for b in built] == [s[0] for s in SECTIONS]
    assert len(ids) == len(set(ids)), sorted(i for i in ids if ids.count(i) > 1)
    for d in departures_:
        assert isinstance(d, H)
