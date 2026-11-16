"""The body sections of gh-pages/morphhb-corrections/index.html.

Written by Claude (Opus 5.5) on 2026-11-14, a sub-agent of the session that built the page, as
an untracked scratch script; tracked since 2026-11-15; rewritten on 2026-11-16 to Ben's
decisions of that day, which morphhb_corrections_index's docstring lists.
morphhb_corrections_lib holds the page's rules and the verb of Ben's decision 8, RESOLVE.  The
generator imports SECTIONS from here, assembles the page, runs self_test on the sections it
built, and lints the page with the verses that allowed_versions() returns.

Every list and count of words comes from verdicts.json (L.VERDICTS), so that a new verdicts
file changes the page's data alone; every other form and count comes from the report folder F's
out/ files.  This file holds no Hebrew character (a letter or mark that must be named is named
by its Unicode name in an escape).  Each parse of one of F's .txt files asserts how many times
its pattern matches, and each count the page states is read from the data.
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
    stack,
    strong,
    table,
    td,
    vcell,
    vref,
)

FO = L.F / "out"
MAQAF = L.MAQAF
R = L.RESOLVE
H_DOT = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"
HATAF_PATAH = H_DOT + "ataf pata" + H_DOT
HET = H_DOT + "et"
QADMA = "\N{HEBREW ACCENT QADMA}"
PASHTA = "\N{HEBREW ACCENT PASHTA}"


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


@lru_cache(maxsize=None)
def readme_flat():
    """The report's README, its white space collapsed."""
    return " ".join((L.F / "README.md").read_text(encoding="utf-8").split())


def readme_says(phrase):
    """Assert that the README says phrase, once: a statement of the README's that the page
    repeats, with its counts, is checked so."""
    assert readme_flat().count(phrase) == 1, phrase


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


# A word misspelled in a commit message that the page quotes, by commit: the quotation keeps it
# and flags it "[sic]" (Ben, 2026-11-06, of a misspelled label: "In no world do we keep,
# silently, 'fascimile'"), and the introduction says once that square brackets in a quotation
# hold the page's words.
SIC = {"c299c30a": "mantaining"}


def cm(sha, msg=False):
    """A morphhb commit with its date, and with its message too if msg."""
    date, message = commits()[sha]
    if msg and sha in SIC:
        assert message.count(SIC[sha]) == 1, (sha, message)
        message = message.replace(SIC[sha], SIC[sha] + " [sic]")
    return commit(sha, date, message if msg else None)


def cmc(sha):
    """A morphhb commit and its date, for use inside parentheses or a cell."""
    return ht(commit(sha), ", ", commits()[sha][0])


# ---------------------------------------------------------------- small helpers


def hj(parts, sep):
    out = []
    for k, x in enumerate(parts):
        if k:
            out.append(sep)
        out.append(x)
    return ht(*out)


def and_list(parts, conj="and"):
    parts = list(parts)
    assert parts
    if len(parts) == 1:
        return ht(parts[0])
    return ht(hj(parts[:-1], ", "), f" {conj} ", parts[-1])


def vlist(refs, conj="and"):
    return and_list([vref(r) for r in refs], conj)


def num(n):
    return f"{n:,}"


SMALL = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def numword(n):
    """n as a word below 10, else in digits: "nine", "10", "3,811"."""
    return SMALL[n] if n < len(SMALL) else num(n)


def counted(n, noun, plural=None):
    """n with its noun: "one word", "nine words", "10 words", "3,811 units"."""
    return f"{numword(n)} {noun if n == 1 else plural or noun + 's'}"


def cap(s):
    """s with its first letter capitalized, except the name morphhb, which is lowercase."""
    return s if s.startswith("morphhb") else s[:1].upper() + s[1:]


def fkey(s):
    """A form's units, each with its marks sorted and invisible marks dropped, morphhb's '/'
    dropped first: equal keys mean the same letters with the same marks."""
    return [L.unit_key(u) for u in L.units(s.replace("/", ""))]


def unk(s):
    """A display form with F's [k] and [q] markers dropped."""
    return re.sub(r"\[[kq]\]", "", s).strip()


def name(ch):
    return unicodedata.name(ch)


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


def notes_words(ns):
    """WLC's note letters in words: "no note", "note 1", "notes Q, n and p"."""
    if not ns:
        return ht("no note")
    return ht("note " if len(ns) == 1 else "notes ", and_list([note(n) for n in ns]))


# ---------------------------------------------------------------- the verdicts

# The verdicts that the page lists, in tables, and those that it counts only.
LISTED = ("defies", "resolves", "follows", "slip")
COUNTED = ("fits both", "ketiv", "same", "text")
# The report's verdicts, as verdicts.json's "report" fields name them, and the values for a word
# that the report did not judge: "unjudged" in the provisional file, "none" in the re-judging's.
# Closed dispatch: any other value raises.
REPORT_VERDICTS = (
    "correction",
    "anomaly",
    "reads WLC",
    "slip",
    "both fit",
    "noise",
    "defensible",
    "ketiv",
)
NOT_JUDGED = ("unjudged", "none")
# The page's verdict that each of the report's corresponds to, as the decision page of
# 2026-11-16 sorted them ("How the words sort").
COUNTERPART = {
    "correction": "defies",
    "anomaly": "resolves",
    "reads WLC": "follows",
    "slip": "slip",
    "both fit": "fits both",
    "noise": "fits both",
    "defensible": "fits both",
    "ketiv": "ketiv",
}


@lru_cache(maxsize=None)
def verdicts():
    """verdicts.json, checked: its verdicts are LISTED and COUNTED, each word's verdict is one
    of them and its report verdict one of the report's or NOT_JUDGED, and every listed word has
    its verse, both forms, its lemma, its morph and a reason."""
    d = json.loads(L.VERDICTS.read_text(encoding="utf-8"))
    assert set(d) == {"about", "verdicts", "words"}, list(d)
    assert set(d["verdicts"]) == set(LISTED + COUNTED), list(d["verdicts"])
    seen = set()
    for w in d["words"]:
        assert w["id"] not in seen, w["id"]
        seen.add(w["id"])
        assert w["verdict"] in LISTED + COUNTED, (w["id"], w["verdict"])
        assert w["report"] in REPORT_VERDICTS + NOT_JUDGED, (w["id"], w["report"])
        # How the word came to be judged: the report's methods found it, its brief named it,
        # or its general test listed it as a rare pair that the report did not judge.
        assert w["source"] in ("methods", "brief", "rare list"), (
            w["id"],
            w.get("source"),
        )
        if w["verdict"] in LISTED:
            for k in ("osisID", "morphhb", "mam", "lemma", "morph", "reason"):
                assert w.get(k), (w["id"], k)
            L.parse_ref(w["osisID"])
            L.morph_words(w["morph"])
    return d


def words(verdict):
    assert verdict in LISTED + COUNTED, verdict
    return [w for w in verdicts()["words"] if w["verdict"] == verdict]


def verdict_name(v):
    """A verdict as the page names it, the second verb from L.RESOLVE; a verb with its object."""
    assert v in LISTED + COUNTED, v
    return {"defies": "defies WLC", "resolves": f"{R['s']} WLC"}.get(
        v, "follows WLC" if v == "follows" else v
    )


def definition(v):
    """verdicts.json's definition of a verdict, as prose."""
    return verdicts()["verdicts"][v].strip()


_MORPH_TOKEN = re.compile(r"(?<![\w/])([HA][A-Za-z0-9]+(?:/[A-Za-z0-9]+)*)(?![\w/])")
_SINGLE_QUOTED = re.compile(r"(?<!\w)'([^']+)'(?!\w)")
_DOUBLE_QUOTED = re.compile(r'"([^"]*)"')


def is_morph_code(s):
    try:
        L.morph_words(s)
    except ValueError:
        return False
    return True


def with_codes(s):
    """Plain text with each of morphhb's morph codes in it drawn by morph()."""
    out, pos = [], 0
    for m in _MORPH_TOKEN.finditer(s):
        if is_morph_code(m.group(1)):
            out += [s[pos : m.start()], morph(m.group(1))]
            pos = m.end()
    out.append(s[pos:])
    return ht(*out)


def curly(s):
    """Straight quotation marks drawn as curly ones, as the page's own are."""
    s = _DOUBLE_QUOTED.sub(
        "\N{LEFT DOUBLE QUOTATION MARK}\\1\N{RIGHT DOUBLE QUOTATION MARK}", s
    )
    return _SINGLE_QUOTED.sub(
        "\N{LEFT SINGLE QUOTATION MARK}\\1\N{RIGHT SINGLE QUOTATION MARK}", s
    )


def reason(w):
    """The word's reason as verdicts.json gives it, as one sentence, its morph codes drawn by
    morph()."""
    s = w["reason"].strip()
    s = cap(s)
    if not s.endswith((".", "?", "!")):
        s += "."
    return with_codes(curly(s))


# ---------------------------------------------------------------- the report's tables of words


@lru_cache(maxsize=None)
def traced_cells():
    """80-part2-corrections-table.md's rows, each a list of its ten cells."""
    lines = [
        ln
        for ln in ftext("80-part2-corrections-table.md").splitlines()
        if ln.startswith("|")
    ]
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    assert len(cells[0]) == 10 and cells[0][1] == "morphhb id", cells[0]
    assert cells[0][7] == "WLC notes at the chanted word", cells[0]
    return cells[2:]


@lru_cache(maxsize=None)
def traced_notes():
    """The WLC notes at each traced word's chanted word, by morphhb id, as the report's table of
    those words gives them."""
    out = {}
    for c in traced_cells():
        id_ = re.fullmatch(r"`(\w{5})`", c[1]).group(1)
        out[id_] = [] if c[7] == "none" else c[7].split(", ")
    assert len(out) == 9
    return out


@lru_cache(maxsize=None)
def traced():
    """80-part2-corrections-table.md, the report's table of the nine words whose history it
    traced: for each morphhb id, the commits since which its lemma's number and its morph have
    been as now, with the lemma and morph checked against verdicts.json's where it has the
    word."""
    by_id = {w["id"]: w for w in verdicts()["words"]}
    out = {}
    for c in traced_cells():
        assert len(c) == 10, c
        since = []
        for s in (c[8], c[9]):
            m = re.fullmatch(r"`([0-9a-f]{8})` (\d{4}-\d\d-\d\d)", s)
            assert m and commits()[m.group(1)][0] == m.group(2), s
            since.append(m.group(1))
        id_ = re.fullmatch(r"`(\w{5})`", c[1]).group(1)
        lemma, morph_ = c[4], re.fullmatch(r"`([^`]+)`", c[5]).group(1)
        if id_ in by_id:
            assert (by_id[id_]["lemma"], by_id[id_]["morph"]) == (lemma, morph_), id_
        out[id_] = (c[0], since[0], since[1])
    assert len(out) == 9
    return out


@lru_cache(maxsize=None)
def census():
    d = fjson("50-alel-census.json")
    assert len(d["words"]) == 4930 and len(d["mismatches"]) == 17
    by_id = {w["id"]: w for w in d["words"]}
    assert len(by_id) == 4930
    return d, by_id


@lru_cache(maxsize=None)
def check63():
    """63-check-new-corrections.txt: each word's form in every source, by morphhb id."""
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
        for nm in ("WLC 4.20", "WLC 4.22", "UXLC 2.6", "MAM"):
            src[nm] = one(r"^   " + re.escape(nm) + r"\s+(\S+)$", b).group(1)
        out[m.group(1)] = dict(
            ref=ref, word=m.group(2), notes=ast.literal_eval(m.group(5)), src=src
        )
    return out


# ---------------------------------------------------------------- WLC 4.22 at a listed word


@lru_cache(maxsize=None)
def residuals_422():
    """45-text-version-evidence.txt's residual units of morphhb against WLC 4.22: (verse,
    morphhb's form, WLC 4.22's, WLC 4.20's)."""
    t = ftext("45-text-version-evidence.txt")
    head = one(r"^######## morphhb vs WLC 4\.22: (\d+) residual units", t)
    ms = found(
        r"^  (\S+ \d+:\d+)\s+\[[^\]]+\] morphhb: (\S+) \| WLC 4\.22: (\S+) \| "
        r"WLC 4\.20: (\S+) \[\w+\]$",
        t[head.start() :],
        int(head.group(1)),
    )
    return [m.groups() for m in ms]


def later_forms(ws):
    """(word, WLC 4.20's form, WLC 4.22's) for each word of ws at which WLC 4.22 has another
    form, found by verse and by morphhb's form."""
    out = []
    for w in ws:
        key = L.parse_ref(w["osisID"])
        for ref, mine, w22, w20 in residuals_422():
            if L.parse_ref(ref) == key and fkey(unk(mine)) == fkey(w["morphhb"]):
                assert fkey(unk(w20)) == fkey(w["morphhb"]), ref
                out.append((w, unk(w20), unk(w22)))
    return out


def parse_notes(s):
    """A list of note letters as the report's files print it: "none" or "['Q', 'n', 'p']"."""
    return [] if s == "none" else ast.literal_eval(s)


@lru_cache(maxsize=None)
def summary61():
    """61-summary.txt's section 1, the four words beyond the al/el census that the report's
    methods found: for each morphhb id, each version's form and WLC note letters at the chanted
    word, as the census records them (sources), and morphhb's notes there."""
    sec = between(ftext("61-summary.txt"), "== 1.", "== 2.")
    out = {}
    for h in found(r"^-- (\S+ \d+:\d+), morphhb id (\w{5})$", sec, 4):
        b = block_after(sec, h.group(0))
        mine = one(
            r"^   morphhb: \S+  lemma .+?  morph \S+; WLC notes at the chanted word in "
            r"morphhb: (none|\[.*\])$",
            b,
        )
        sources = {}
        for nm in ("WLC 4.20", "WLC 4.22", "UXLC 2.6"):
            m = one(
                r"^   " + re.escape(nm) + r": (\S+)  notes (none|\[.*\])$",
                b,
            )
            sources[nm] = dict(atoms=[m.group(1)], notes=parse_notes(m.group(2)))
        out[h.group(2)] = dict(
            ref=h.group(1), sources=sources, morphhb_notes=parse_notes(mine.group(1))
        )
    return out


@lru_cache(maxsize=None)
def by_version_all():
    """The words whose forms and WLC notes the report's data record by version, by morphhb id:
    the al/el census's and summary61's, each with its sources (WLC 4.20, WLC 4.22 and UXLC 2.6,
    each with its atoms and its note letters at the chanted word) and morphhb's notes.
    """
    _d, census_ids = census()
    out = dict(census_ids)
    for id_, rec in summary61().items():
        assert id_ not in out, id_
        out[id_] = rec
    return out


def by_version(id_):
    """by_version_all's record of a word, or None, checked: morphhb's notes at it are WLC
    4.20's, and at a word whose history the report traced, WLC 4.20's notes are those of the
    report's table of those words (traced_notes)."""
    rec = by_version_all().get(id_)
    if rec is not None:
        n20 = rec["sources"]["WLC 4.20"]["notes"]
        assert rec["morphhb_notes"] == n20, id_
        assert traced_notes().get(id_, n20) == n20, id_
    return rec


def at_chanted_word(w):
    """WLC's note letters at a word's chanted word, and whose they are: WLC 4.20's, where the
    report's data record them by version (by_version), and otherwise morphhb's copy of WLC's
    notes (morphhb_notes)."""
    rec = by_version(w["id"])
    if rec is not None:
        return "WLC 4.20", rec["sources"]["WLC 4.20"]["notes"]
    assert w["id"] not in traced_notes(), w["id"]
    return "morphhb", morphhb_notes(w)


@lru_cache(maxsize=None)
def morphhb_note_lines():
    """60-wlc-notes.txt's section 5, every chanted word that differs from MAM under each of
    WLC's note letters as morphhb has them: (letter, verse, morphhb's words in the line), each
    word as (form, lemma, morph)."""
    t = ftext("60-wlc-notes.txt")
    sec = t[one(r"^== 5\. Every chanted word that differs from MAM", t).start() :]
    out = []
    for h in found(r"^-- note (\S): (\d+)$", sec, 22):
        b = block_after(sec, h.group(0))
        lines = found(r"^   (\S+ \d+:\d+)\s+(.+?) \| MAM .*$", b, int(h.group(2)))
        for m in lines:
            ws = re.findall(r"(\S+?)\{(.+?) (\S+) (?:same|skey|letters)\}", m.group(2))
            assert ws, m.group(0)
            out.append((h.group(1), m.group(1), ws))
    return out


def morphhb_notes(w):
    """The note letters that morphhb has at a word's chanted word, from 60-wlc-notes.txt's
    section 5, which lists every chanted word that differs from MAM under each of its letters:
    a word whose form differs from MAM's and that no letter lists has no note."""
    assert fkey(w["morphhb"]) != fkey(w["mam"]), w["id"]
    key = L.parse_ref(w["osisID"])
    out = []
    for letter, ref, ws in morphhb_note_lines():
        if L.parse_ref(ref) != key:
            continue
        mine = [
            x
            for x in ws
            if fkey(x[0]) == fkey(w["morphhb"]) and x[1:] == (w["lemma"], w["morph"])
        ]
        assert len(mine) <= 1, (w["id"], ref)
        if mine:
            out.append(letter)
    return out


def later_notes(ws):
    """(word, WLC 4.20's notes, WLC 4.22's) for each word of ws that by_version records and at
    whose chanted word WLC 4.22 has other notes; morphhb has WLC 4.20's."""
    out = []
    for w in ws:
        rec = by_version(w["id"])
        if rec is None:
            continue
        n20 = rec["sources"]["WLC 4.20"]["notes"]
        n22 = rec["sources"]["WLC 4.22"]["notes"]
        if n20 != n22:
            out.append((w, n20, n22))
    return out


def uxlc_differs(ws):
    """{word's id: what UXLC 2.6 lacks there} for each word of ws that by_version records and
    whose form UXLC 2.6 has otherwise than WLC 4.20.  Closed dispatch: the one difference
    described is a final he without WLC 4.20's mapiq; any other raises."""
    out = {}
    for w in ws:
        rec = by_version(w["id"])
        if rec is None:
            continue
        a20 = "".join(rec["sources"]["WLC 4.20"]["atoms"])
        aux = "".join(rec["sources"]["UXLC 2.6"]["atoms"])
        if fkey(a20) == fkey(aux):
            continue
        m20, _q20 = atom_marks(a20)
        mux, _qux = atom_marks(aux)
        assert [x[0] for x in m20] == [x[0] for x in mux], w["id"]
        lacks = [
            (k, name(ch))
            for k, ((_b, c20), (_b2, cux)) in enumerate(zip(m20, mux))
            for ch in (c20 - cux).elements()
        ]
        extra = [
            k for k, ((_b, c20), (_b2, cux)) in enumerate(zip(m20, mux)) if cux - c20
        ]
        last = len(m20) - 1
        if (
            lacks == [(last, "HEBREW POINT DAGESH OR MAPIQ")]
            and not extra
            and m20[last][0] == "\N{HEBREW LETTER HE}"
        ):
            out[w["id"]] = "no mapiq there"
            continue
        raise ValueError(f"UXLC 2.6 differs at {w['osisID']}: {lacks}, {extra}")
    return out


def later_versions(ws):
    """What WLC 4.22, a later version than morphhb's text, and UXLC 2.6 have at words of ws
    where they differ from WLC 4.20, in paragraphs and a table, or nothing."""
    parts = []
    groups = {}
    ux = uxlc_differs(ws)
    told = set()
    for w, n20, n22 in later_notes(ws):
        groups.setdefault((tuple(n20), tuple(n22)), []).append(w)
    for (n20, n22), g in groups.items():
        tail = ["."]
        if len(g) == 1 and g[0]["id"] in ux:
            tail = ["; UXLC 2.6 has ", ux[g[0]["id"]], "."]
            told.add(g[0]["id"])
        parts.append(
            p(
                "At ",
                vlist([w["osisID"] for w in g]),
                ", WLC 4.22, a later version than morphhb's text, has ",
                notes_words(n22),
                " at the chanted word, where WLC 4.20 and morphhb have ",
                notes_words(n20),
                *tail,
            )
        )
    for w in ws:
        if w["id"] in ux and w["id"] not in told:
            parts.append(
                p("At ", vref(w["osisID"]), ", UXLC 2.6 has ", ux[w["id"]], ".")
            )
    forms = later_forms(ws)
    if forms:
        parts.append(
            p(
                "At ",
                vlist([w["osisID"] for w, _a, _b in forms]),
                ", WLC 4.22, a later version than morphhb's text, has another form. In "
                "each row WLC 4.20's form, which is morphhb's, stands above WLC 4.22's, "
                "accents shown.",
            )
        )
        parts.append(
            table(
                ["WLC 4.20 above WLC 4.22", "Verse"],
                [[form_td(a, b), vcell(w["osisID"])] for w, a, b in forms],
            )
        )
    return ht(*parts)


# ---------------------------------------------------------------- the tables of words

TABLE_LEAD = (
    "In each row morphhb's word, which is WLC 4.20's form with morphhb's "
    "\N{LEFT DOUBLE QUOTATION MARK}/\N{RIGHT DOUBLE QUOTATION MARK} between morphemes, "
    "stands above MAM's atom, both without accents, meteg or a maqaf after the atom; the reason "
    "is Claude's, from verdicts.json."
)


def history_cell(w):
    t = traced().get(w["id"])
    if t is None:
        return td("not traced")
    _verse, lemma_since, morph_since = t
    return td(ht("lemma since ", cmc(lemma_since), "; morph since ", cmc(morph_since)))


def notes_cell(w):
    """The note letters at the word's chanted word, with whose they are (at_chanted_word)."""
    whose, ns = at_chanted_word(w)
    return td(ht(whose, ": ", notes_words(ns)))


def word_table(ws, history=False, notes=False):
    head = ["morphhb above MAM", "Verse", "Lemma", "Morph"]
    head += ["History"] if history else []
    head += ["Notes at the chanted word"] if notes else []
    head += ["Claude's reason"]
    rows = []
    for w in ws:
        cells = [
            form_td(L.analysis_form(w["morphhb"]), L.analysis_form(w["mam"])),
            vcell(w["osisID"]),
            td(w["lemma"]),
            td(morph(w["morph"])),
        ]
        if history:
            cells.append(history_cell(w))
        if notes:
            cells.append(notes_cell(w))
        cells.append(note_td(reason(w)))
        rows.append(cells)
    return table(head, rows)


def words_part(ws, lead, none, history=False, notes=False):
    """A lead, the table of ws and what WLC 4.22 and UXLC 2.6 have at them; or, if ws is empty,
    none."""
    if not ws:
        return p(none)
    return ht(
        p(*lead, " ", TABLE_LEAD),
        word_table(ws, history, notes),
        later_versions(ws),
    )


# ---------------------------------------------------------------- the report's text data


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
    """WLC has the pashta twice, the second on the atom's last letter; morphhb has HEBREW
    ACCENT QADMA for the first, on the same letter, and the atoms are otherwise equal.
    """
    um, uw = L.units(mnorm(mine)), L.units(mnorm(wlc))
    assert [u[0] for u in um] == [u[0] for u in uw], where
    at_w = [k for k, u in enumerate(uw) if PASHTA in u]
    at_m = [k for k, u in enumerate(um) if QADMA in u]
    assert len(at_w) == 2 and at_w[1] == len(uw) - 1 and at_m == at_w[:1], where
    assert not any(QADMA in u for u in uw), where
    fixed = [u.replace(QADMA, PASHTA) for u in um]
    assert [L.unit_key(u) for u in fixed] == [L.unit_key(u) for u in uw], where


def helper_table(refs):
    rows = []
    for ref in refs:
        mine, wlc = helper_example(ref)
        rows.append([form_td(mine, wlc), vcell(ref)])
    return table(["morphhb above WLC 4.20", "Verse"], rows)


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


MUNAH = f"muna{H_DOT}"
# What differs at each Decalogue unit of 41-text-residuals.json, by morphhb id, in the order the
# page's tables give them, with what union_diff must find there and the kind of difference.
# Letter indices count from the atom's first letter.  Each "What differs" names both markings,
# morphhb's and WLC 4.20's (hebrew-prose: a maqaf difference is an exchange with both marks
# named), and check_named asserts each mark that it names.
DECALOGUE_UNITS = [
    (
        "02p5S",
        "marks",
        ([(1, "HEBREW POINT PATAH")], [], None),
        "a vowel or the maqaf",
        "A vowel: under the tav, WLC 4.20's atom has a qamats and a patah, and morphhb's main "
        "text and its alternative note the qamats alone.",
    ),
    (
        "02Feh",
        "marks",
        ([(3, "HEBREW POINT SHEVA")], [(3, "HEBREW POINT HATAF PATAH")], None),
        "a vowel or the maqaf",
        f"A vowel: under the {HET}, morphhb's main text and its alternative note have a "
        f"{HATAF_PATAH} where WLC 4.20's atom has a shewa; MAM has the {HATAF_PATAH}.",
    ),
    (
        "05HcR",
        "maqaf",
        ([], [], "extra"),
        "a vowel or the maqaf",
        "The maqaf: morphhb's main text has a maqaf after the atom and no accent, where WLC "
        f"4.20's atom and morphhb's alternative note have a {MUNAH} and no maqaf; MAM has both "
        f"the {MUNAH} and the maqaf.",
    ),
    (
        "02dor",
        "marks",
        ([(0, "HEBREW POINT METEG")], [], None),
        "a meteg",
        "A meteg: under the vav, WLC 4.20's atom has a patah and a meteg, and morphhb's main "
        "text and its alternative note the patah alone.",
    ),
    (
        "02xhV",
        "marks",
        ([(2, "HEBREW ACCENT GERESH")], [(2, "HEBREW ACCENT QADMA")], None),
        "an accent",
        "An accent: on the bet, morphhb's alternative note has HEBREW ACCENT QADMA where WLC "
        "4.20's atom has HEBREW ACCENT GERESH.",
    ),
    (
        "05Lzv",
        "marks",
        ([], [(2, "HEBREW ACCENT TIPEHA")], None),
        "an accent",
        "An accent: on the tsadi, morphhb's main text has HEBREW POINT METEG and its "
        "alternative note HEBREW ACCENT TIPEHA, where WLC 4.20's atom has HEBREW POINT METEG "
        "alone; UXLC 2.6 and MAM have HEBREW ACCENT TIPEHA there.",
    ),
    (
        "059vS",
        "ok",
        ([], [], None),
        "the maqaf",
        "The maqaf: morphhb's main text has a merkha and no maqaf after the atom, and its "
        "alternative note a maqaf and no accent; WLC 4.20's atom has both the merkha and the "
        "maqaf.",
    ),
    (
        "05fou",
        "ok",
        ([], [], None),
        "the maqaf",
        "The maqaf: morphhb's main text has a merkha and no maqaf after the atom, and its "
        "alternative note a maqaf and no accent; WLC 4.20's atom has both the merkha and the "
        "maqaf.",
    ),
]
# The two units whose union is WLC 4.20's atom although the main text alone is not: the main
# text lacks the maqaf that the alternative note and WLC 4.20's atom have.
MAQAF_ONLY_IN_NOTE = ("059vS", "05fou")


def letter_marks(form, k):
    """The names of the marks of an atom's letter k, invisible marks dropped."""
    us, _maqaf = atom_marks(form)
    return {name(ch) for ch in us[k][1].elements()}


def accents_and_maqaf(form):
    """The names of an atom's accents, and whether a maqaf follows it."""
    us, maqaf = atom_marks(form)
    accents = {name(ch) for _b, c in us for ch in c.elements() if "ACCENT" in name(ch)}
    return accents, maqaf


def check_named(x):
    """Assert the marks that a Decalogue unit's "What differs" names (DECALOGUE_UNITS): closed
    dispatch by morphhb id."""
    main, alt, wlc, mam = x["main"], x["alt"], x["wlc"], x["_display"]["MAM"]
    morphhb_sides = (main, alt)
    id_ = x["id"]
    if id_ == "02p5S":
        assert {"HEBREW POINT QAMATS", "HEBREW POINT PATAH"} <= letter_marks(wlc, 1)
        for s in morphhb_sides:
            assert "HEBREW POINT QAMATS" in letter_marks(s, 1)
            assert "HEBREW POINT PATAH" not in letter_marks(s, 1)
    elif id_ == "02Feh":
        assert "HEBREW POINT SHEVA" in letter_marks(wlc, 3)
        for s in morphhb_sides + (mam,):
            assert "HEBREW POINT HATAF PATAH" in letter_marks(s, 3)
    elif id_ == "05HcR":
        assert accents_and_maqaf(main) == (set(), True)
        assert accents_and_maqaf(alt) == ({"HEBREW ACCENT MUNAH"}, False)
        assert accents_and_maqaf(wlc) == ({"HEBREW ACCENT MUNAH"}, False)
        assert accents_and_maqaf(mam) == ({"HEBREW ACCENT MUNAH"}, True)
    elif id_ == "02dor":
        assert {"HEBREW POINT PATAH", "HEBREW POINT METEG"} <= letter_marks(wlc, 0)
        for s in morphhb_sides:
            assert "HEBREW POINT PATAH" in letter_marks(s, 0)
            assert "HEBREW POINT METEG" not in letter_marks(s, 0)
    elif id_ == "02xhV":
        assert "HEBREW ACCENT QADMA" in letter_marks(alt, 2)
        assert "HEBREW ACCENT GERESH" in letter_marks(wlc, 2)
    elif id_ == "05Lzv":
        assert "HEBREW POINT METEG" in letter_marks(main, 2)
        assert "HEBREW ACCENT TIPEHA" in letter_marks(alt, 2)
        assert "HEBREW POINT METEG" in letter_marks(wlc, 2)
        assert "HEBREW ACCENT TIPEHA" not in letter_marks(wlc, 2)
        for s in ("UXLC", "MAM"):
            assert "HEBREW ACCENT TIPEHA" in letter_marks(x["_display"][s], 2)
    elif id_ in MAQAF_ONLY_IN_NOTE:
        assert accents_and_maqaf(main) == ({"HEBREW ACCENT MERKHA"}, False)
        assert accents_and_maqaf(alt) == (set(), True)
        assert accents_and_maqaf(wlc) == ({"HEBREW ACCENT MERKHA"}, True)
    else:
        raise ValueError(f"a Decalogue unit with no check: {id_}")


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
    for id_, test, (missing, extra, maq), kind, what in DECALOGUE_UNITS:
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
        x = dict(u, id=id_, kind=kind, what=what, main=main, alt=alt, wlc=wlc)
        check_named(x)
        out.append(x)
    # Deuteronomy 5:17's tipexa is UXLC 2.6's and MAM's too, and not WLC 4.20's.
    t = [x for x in out if x["id"] == "05Lzv"][0]
    tip = "\N{HEBREW ACCENT TIPEHA}"
    assert all(tip in t["_display"][s] for s in ("UXLC", "MAM"))
    assert tip not in t["_display"]["4.20"]
    return out


@lru_cache(maxsize=None)
def divided():
    """The divided accents' counts: the class's units and verses against WLC 4.20, and the
    atoms with an alternative note whose union with the main text is WLC 4.20's atom (ok), by
    label, and those whose union is not (failing)."""
    d40 = fjson("40-text-compare-data.json")
    ds = d40["dstats"]
    with_note = {k: v for k, v in ds.items() if "alternative note: yes" in k}
    assert sum(with_note.values()) == d40["alt_cover"]["alternative-note atoms"]
    prefix = "; alternative note: yes; WLC = main + alternative: ok"
    ok = {
        label: ds.get(label + prefix, 0)
        for label in (
            "divided-accents/accents",
            "divided-accents/accents+paseq",
            "divided-accents/pointing",
        )
    }
    failing = [x for x in decalogue_units() if x["union_test"] != "ok"]
    not_union = sum(v for k, v in with_note.items() if not k.endswith(": ok"))
    assert not_union == len(failing)
    units = d40["class_units"]["4.20"]["Decalogue/divided accents"]
    assert sum(ok.values()) + len(failing) == units, (ok, len(failing), units)
    assert ok["divided-accents/pointing"] == len(MAQAF_ONLY_IN_NOTE)
    # An atom whose main text alone already has WLC 4.20's marks differs in nothing, so it is no
    # unit of the class, though it has an alternative note.
    equal = sum(v for k, v in with_note.items() if k.startswith("equal to WLC;"))
    assert sum(with_note.values()) == equal + units, (with_note, units)
    assert equal == 1, equal  # the sentence that names it is in the singular
    return dict(
        units=units,
        verses=class_verses()["Decalogue/divided accents"],
        atoms_with_note=sum(with_note.values()),
        equal_with_note=equal,
        ok=ok,
        n_ok=sum(ok.values()),
        failing=failing,
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


PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
DIVIDED_LINE = (
    r"^(\S+ \d+:\d+)\s+(.+?)\s+main: (.*?) \| alternative: (.*?) \| WLC 4\.20: (.*?) \| "
    r"union: (\S+)$"
)


@lru_cache(maxsize=None)
def divided_lines():
    """46-text-divided-accents.txt's line for each atom of the Decalogues and Genesis 35:22
    that differs from WLC 4.20 or has an alternative note, in the verses' order: (verse,
    label, main text, alternative note, WLC 4.20, union test).  The atoms that equal WLC
    4.20's and have no alternative note are not listed, so two lines in a row need not be two
    atoms in a row."""
    ds = fjson("40-text-compare-data.json")["dstats"]
    unlisted = "equal to WLC, no alternative note"
    assert sum(1 for k in ds if k.startswith(unlisted)) == 1, list(ds)
    n = sum(v for k, v in ds.items() if not k.startswith(unlisted))
    out = [
        m.groups() for m in found(DIVIDED_LINE, ftext("46-text-divided-accents.txt"), n)
    ]
    ok = Counter(x[1] for x in out if x[5] == "ok")
    for label, k in divided()["ok"].items():
        assert ok[label] == k, (label, ok[label], k)
    return out


def split_paseq(form):
    """An atom as 46-text-divided-accents.txt writes it, without the Unicode PASEQ after it,
    and whether one is there."""
    if form.endswith(" " + PASEQ):
        return form[: -len(" " + PASEQ)], True
    assert PASEQ not in form, ascii(form)
    return form, False


def other_marks(form):
    """An atom's marks other than its accents and HEBREW POINT METEG, as {(letter index, mark
    name)}, whether a maqaf follows it, and whether a Unicode PASEQ does."""
    atom, paseq = split_paseq(form)
    us, maqaf = atom_marks(atom)
    marks = {
        (k, name(ch))
        for k, (_b, c) in enumerate(us)
        for ch in c.elements()
        if "ACCENT" not in name(ch) and ch != "\N{HEBREW POINT METEG}"
    }
    return marks, maqaf, paseq


@lru_cache(maxsize=None)
def dagesh_rafeh_atoms():
    """The union test's passes labelled divided-accents/accents at which morphhb's main text or
    alternative note differs from WLC 4.20's atom in a mark other than an accent or HEBREW
    POINT METEG, which is each accentuation's verse-final silluq there.  At each, WLC 4.20's
    first letter has the dagesh and the rafeh, the main text's the dagesh alone and the
    alternative note's the rafeh alone, and nothing else differs but, where the note lacks it,
    the maqaf that WLC 4.20 and the main text have after the atom.  Each as (verse, the
    alternative note's atom, whether the note lacks the maqaf)."""
    dg, rf = (0, "HEBREW POINT DAGESH OR MAPIQ"), (0, "HEBREW POINT RAFE")
    out = []
    for verse, label, main, alt, wlc, union in divided_lines():
        if (label, union) != ("divided-accents/accents", "ok"):
            continue
        (am, aq, ap), (bm, bq, bp), (wm, wq, wp) = (
            other_marks(s) for s in (main, alt, wlc)
        )
        if (am, aq, ap) == (bm, bq, bp) == (wm, wq, wp):
            continue
        assert {dg, rf} <= wm and am == wm - {rf} and bm == wm - {dg}, verse
        assert aq == wq and (bq == wq or (wq and not bq)), verse
        assert ap == bp == wp, verse
        out.append((verse, alt, wq and not bq))
    return out


@lru_cache(maxsize=None)
def paseq_atoms():
    """The verses of the union test's passes labelled divided-accents/accents+paseq: at each,
    WLC 4.20's atom and morphhb's alternative note have a Unicode PASEQ after the atom and the
    main text none, and the note's one accent is HEBREW ACCENT MUNAH, so that the PASEQ follows
    a munax."""
    out = []
    for verse, label, main, alt, wlc, union in divided_lines():
        if label != "divided-accents/accents+paseq":
            continue
        assert union == "ok", verse
        (m, pm), (a, pa), (_w, pw) = (split_paseq(s) for s in (main, alt, wlc))
        assert (pm, pa, pw) == (False, True, True), verse
        assert accents_and_maqaf(a)[0] == {"HEBREW ACCENT MUNAH"}, verse
        assert accents_and_maqaf(m)[0], verse
        out.append(verse)
    return out


def chanted_words(text):
    """A text's chanted words: its runs between spaces, a maqaf compound being one."""
    return text.split(" ")


@lru_cache(maxsize=None)
def deut58_compounds():
    """At Deuteronomy 5:8, the chanted words that hold the atom of unit 05fou in WLC 4.20, in
    morphhb's main text and in its alternative note.  The alternative note whose catchWord
    differs from the main text (catchword) quotes three atoms of the main text in a row; the
    listing's lines for those three atoms (divided_lines), whose main-text letters are the
    quotation's, give WLC 4.20's three atoms and the main text's, and the note's own text gives
    its chanted words."""
    cw = catchword()
    unit = [x for x in decalogue_units() if x["id"] == "05fou"][0]
    quoted = [a for part in chanted_words(cw["whole"]) for a in part.split(MAQAF)]
    want = [letters(a) for a in quoted]
    rows = [x for x in divided_lines() if L.parse_ref(x[0]) == L.parse_ref("Deut 5:8")]
    starts = [
        k
        for k in range(len(rows) - len(want) + 1)
        if [letters(r[2]) for r in rows[k : k + len(want)]] == want
    ]
    assert len(starts) == 1 and len(want) == 3, (starts, len(want))
    three = rows[starts[0] : starts[0] + 3]
    assert three[1][2] == unit["main"] and three[1][4] == unit["wlc"]
    wlc_atoms = [r[4] for r in three]
    main_atoms = [r[2] for r in three]
    assert [a.endswith(MAQAF) for a in wlc_atoms] == [True, True, False]
    assert [a.endswith(MAQAF) for a in main_atoms] == [True, False, False]
    (alt_word,) = [
        cwd
        for cwd in chanted_words(cw["x_accent"])
        if letters(cwd).startswith(letters(unit["alt"]))
    ]
    assert alt_word.startswith(unit["alt"]) and letters(alt_word) == "".join(want[1:])
    return dict(
        wlc="".join(wlc_atoms), main="".join(main_atoms[:2]), alt=alt_word, unit=unit
    )


@lru_cache(maxsize=None)
def division_units():
    us = units_labelled("word-division")  # prose-ok: the report's label, quoted
    assert len(us) == 12
    texts = set()
    for u in us:
        assert len(u["morphhb"]) == 2 and len(u["wlc_4.20"]) == 1
        assert letters(unk(u["_display"]["morphhb"])) == letters(
            unk(u["_display"]["4.20"])
        ), u["reference"]
        (en,) = u["exegesis_notes"]
        assert en["rdg"] is None
        texts.add(en["text"])
    (text,) = texts
    return us, text


def defies_by_text_count():
    us, _text = division_units()
    (kq,) = units_labelled("kq-structure")
    return len(divided()["failing"]) + len(us) + 1


# ---------------------------------------------------------------- the versions named


def allowed_versions():
    """The verses at which the page may name WLC 4.22 and UXLC 2.6, each in its long and short
    name.  WLC 4.22: Ben's list of 2026-11-16 (notes 1 at Exodus 10:28, Joshua 22:19 and
    Jeremiah 47:6, note U at Genesis 39:19, the ketiv and qere at Daniel 2:39, the rafeh at
    2 Samuel 11:1), with every listed word at which later_notes or later_forms finds WLC 4.22
    different.  UXLC 2.6: Genesis 39:19, where it lacks WLC 4.20's mapiq, Deuteronomy 5:17,
    where it has a tipexa that WLC 4.20's atom lacks, and Daniel 2:39, where it has a ketiv and
    a qere for WLC 4.20's one atom, each checked here."""
    listed = [w for v in LISTED for w in words(v)]
    v22 = [
        "Exodus 10:28",
        "Joshua 22:19",
        "Jeremiah 47:6",
        "Genesis 39:19",
        "Daniel 2:39",
        "2 Samuel 11:1",
    ]
    v22 += [w["osisID"] for w, _a, _b in later_notes(listed)]
    v22 += [w["osisID"] for w, _a, _b in later_forms(listed)]
    gen = [x for x in check63().values() if x["ref"] == "Gen 39:19"]
    assert len(gen) == 1 and gen[0]["src"]["UXLC 2.6"] != gen[0]["src"]["WLC 4.20"]
    (kq,) = units_labelled("kq-structure")
    assert len(kq["others"]["UXLC"]) == 2 and len(kq["wlc_4.20"]) == 1
    vux = ["Genesis 39:19", "Deuteronomy 5:17", "Daniel 2:39"]

    def names(refs):
        out = set()
        for r in refs:
            out |= {L.verse_name(r), L.verse_short(r).replace(L.NBSP, " ")}
        return frozenset(out)

    return {"WLC 4.22": names(v22), "UXLC 2.6": names(vux)}


# ---------------------------------------------------------------- section: the answer


def text_words_shown():
    """The words whose verdict is "text" whose atoms are rows of the tables of morphhb's text
    (the Decalogue units that the page shows), in verdicts.json's order."""
    shown = {x["id"] for x in decalogue_units()}
    return [w for w in words("text") if w["id"] in shown]


def counted_item(v, n):
    """A verdict that the page counts, not lists, with its count and its definition; at "text",
    the words whose atoms the tables of morphhb's text show."""
    parts = [
        strong(cap(verdict_name(v))),
        f" ({counted(n, 'word')}), where ",
        definition(v),
    ]
    if v == "text":
        shown = text_words_shown()
        if shown:
            parts += [
                " The tables of morphhb's text show ",
                (
                    "its atom"
                    if len(shown) == 1
                    else f"the atoms of {numword(len(shown))}"
                ),
                " of them, at ",
                vlist([w["osisID"] for w in shown]),
                ".",
            ]
    return ht(*parts)


def section_answer():
    n = Counter(w["verdict"] for w in verdicts()["words"])
    by_source = Counter(w["source"] for w in verdicts()["words"])
    dv = divided()
    return ht(
        heading(2, "The answer in brief", "answer"),
        p(
            "This page judges ",
            counted(len(verdicts()["words"]), "word"),
            " of morphhb, the ",
            num(by_source["methods"] + by_source["brief"]),
            " that the report judged and ",
            num(by_source["rare list"]),
            " that its general test listed as too rare for it to judge, and it judges "
            "morphhb's text against WLC 4.20 as a whole:",
        ),
        ol(
            [
                ht(
                    strong(
                        f"At {counted(n['defies'], 'word')} morphhb defies WLC by its "
                        "analysis"
                    ),
                    ", and at ",
                    counted(defies_by_text_count(), "atom"),
                    " of WLC 4.20 by its text (",
                    here("defies", "where morphhb defies WLC"),
                    ").",
                ),
                ht(
                    strong(
                        f"At {counted(n['resolves'], 'word')} morphhb {R['s']} WLC by its "
                        "analysis"
                    ),
                    ", and at ",
                    counted(dv["n_ok"], "atom"),
                    " of the Decalogues and Genesis 35:22 by its text (",
                    here(R["s"], f"where morphhb {R['s']} WLC"),
                    ").",
                ),
                ht(
                    strong(f"At {counted(n['follows'], 'word')} morphhb follows WLC"),
                    " where MAM's form would be analysed otherwise, and at ",
                    counted(n["slip"], "word"),
                    " it has a slip (",
                    here("follows", "where morphhb follows WLC, and its slips"),
                    ").",
                ),
                ht(
                    strong(
                        f"The other {counted(sum(n[v] for v in COUNTED), 'word')} are "
                        "counted, not listed"
                    ),
                    ":",
                    ol([counted_item(v, n[v]) for v in COUNTED if n[v]]),
                ),
                ht(
                    strong("The text of morphhb is WLC 4.20's"),
                    ", apart from the atoms where morphhb defies or ",
                    R["s"],
                    " WLC, differences of encoding only, and final letters that differ only "
                    "from MAM-basics' conversion of WLC 4.20 (",
                    here("text", "the text of morphhb against WLC 4.20"),
                    ").",
                ),
            ]
        ),
    )


# ---------------------------------------------------------------- section: defies


def decalogue_table(units):
    rows = []
    for x in units:
        rows.append(
            [
                form_td(x["main"], x["alt"]),
                form_td(x["wlc"], x["_display"]["MAM"]),
                vcell(x["reference"]),
                note_td(x["what"]),
            ]
        )
    return table(
        [
            "morphhb's main text above its alternative note",
            "WLC 4.20 above MAM",
            "Verse",
            "What differs",
        ],
        rows,
    )


def subsection_defies_analysis():
    ws = words("defies")
    tr = [w for w in ws if w["id"] in traced()]
    untraced = [w for w in ws if w["id"] not in traced()]
    unfound = [w for w in untraced if w["report"] in NOT_JUDGED]
    history = []
    if tr:
        lemma_since = {traced()[w["id"]][1] for w in tr}
        if lemma_since == {"c299c30a"}:
            history.append(
                p(
                    "The report traced the history of ",
                    counted(len(tr), "word"),
                    ". Each lemma's number is already in morphhb's first GitHub commit, ",
                    cm("c299c30a", msg=True),
                    ", so it is at least as old as the files that David Troidl kept in "
                    "Google's SVN before 2009-12-28, which were not read.",
                )
            )
        else:
            history.append(
                p("The report traced the history of ", counted(len(tr), "word"), ".")
            )
    if untraced:
        sentence = ["It did not trace the history of the word"]
        sentence += ["s" if len(untraced) > 1 else "", " at "]
        sentence += [vlist([w["osisID"] for w in untraced])]
        # A word that the report did not judge came to the verdicts here from its general
        # test's list of the words too rare for it to judge (verdicts() checks the source).
        assert all(w["source"] == "rare list" for w in unfound)
        if unfound:
            sentence += ["; its general test listed the word"]
            sentence += ["s" if len(unfound) > 1 else "", " at "]
            sentence += [vlist([w["osisID"] for w in unfound])]
            sentence += [" as too rare for it to judge"]
        history.append(p(*sentence, "."))
    return ht(
        heading(3, "By its analysis", "defies-analysis"),
        words_part(
            ws,
            [
                "At ",
                counted(len(ws), "word"),
                " morphhb defies WLC by its analysis. The history column gives, where the "
                "report traced it, the commits since which the lemma's number and the morph "
                "have been as now, and the notes column the note letters at the chanted word: "
                "WLC 4.20's, where the report's data record them, and otherwise those of "
                "morphhb's copy of WLC's notes (hover over a letter to read its meaning).",
            ],
            "At no word does morphhb defy WLC by its analysis.",
            history=True,
            notes=True,
        ),
        *history,
    )


def subsection_defies_text():
    dv = divided()
    failing = dv["failing"]
    kinds = Counter(x["kind"] for x in failing)
    assert set(kinds) <= {"a vowel or the maqaf", "a meteg", "an accent"}, kinds
    division, exegesis_text = division_units()
    (kq,) = units_labelled("kq-structure")
    assert kq["reference"] == "Dan 2:39"
    return ht(
        heading(3, "By its text", "defies-text"),
        p(
            "At ",
            counted(defies_by_text_count(), "atom"),
            " of WLC 4.20, morphhb's text defies WLC:",
        ),
        ol(
            [
                ht(
                    counted(len(failing), "atom"),
                    " of the Decalogues, where morphhb's main text and its alternative note "
                    "together do not have WLC 4.20's marks, ",
                    and_list(
                        [
                            f"{numword(kinds[k])} in {k}"
                            for k in ("a vowel or the maqaf", "a meteg", "an accent")
                            if kinds[k]
                        ]
                    ),
                    ";",
                ),
                ht(
                    counted(len(division), "atom"),
                    " of WLC 4.20 for each of which morphhb has two atoms;",
                ),
                ht(
                    "the atom at ",
                    vref("Daniel 2:39"),
                    ", for which morphhb has a ketiv and a qere.",
                ),
            ]
        ),
        p(
            "In the ",
            counted(dv["verses"], "verse"),
            " of the Decalogues and ",
            vref("Genesis 35:22"),
            ", the union test asks of each atom that has an alternative note whether WLC "
            "4.20's atom has, letter by letter, the marks of morphhb's main text and of its "
            "alternative note together, a maqaf if either has one, and no others. Of the ",
            num(dv["atoms_with_note"]),
            " atoms that have an alternative note, ",
            numword(dv["equal_with_note"]),
            " already has WLC 4.20's marks in morphhb's main text alone; at all but ",
            numword(len(failing)),
            " of the other ",
            num(dv["units"]),
            ", WLC 4.20's atom is that union. In each row the first cell has morphhb's main "
            "text above its alternative note, and the second WLC 4.20's atom above MAM's; "
            "accents are shown.",
        ),
        decalogue_table(failing),
        p(
            "At ",
            counted(len(division), "place"),
            " morphhb has two atoms where WLC 4.20 has one, and a note of morphhb's at each "
            "says ",
            q(exegesis_text),
            " In each row morphhb's two atoms stand above WLC 4.20's one and above MAM's "
            "form, accents shown.",
        ),
        division_table(division),
        kq_part(kq),
    )


def division_table(us):
    rows = []
    for u in us:
        mine, w20, mam = (u["_display"][k] for k in ("morphhb", "4.20", "MAM"))
        kinds = {x["kind"] for x in u["morphhb"]}
        rows.append(
            [
                form_td(unk(mine), unk(w20), unk(mam)),
                vcell(u["reference"], extra="ketiv" if kinds == {"ketiv"} else None),
            ]
        )
    return table(["morphhb above WLC 4.20 above MAM", "Verse"], rows)


def kq_part(u):
    srcs = [
        ("morphhb", u["morphhb"]),
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
        p(
            "At ",
            vref("Daniel 2:39"),
            " morphhb has a ketiv and a qere for WLC 4.20's one atom, as WLC 4.22, a later "
            "version, UXLC 2.6 and MAM do, but its qere has no accent. A note of morphhb's "
            "there says ",
            q(en["text"]),
            " Each row gives one source's form, accents shown.",
        ),
        table(["Form", "Source"], rows, caption=vref("Daniel 2:39")),
        p(
            "At ",
            vref("Daniel 2:39"),
            ", morphhb's ketiv and qere arrived with ",
            cm("019b22f6", msg=True),
            ", were undone and redone, and have stood since ",
            cm("456c54c6", msg=True),
            ".",
        ),
    )


# Each count of "Where morphhb defies WLC" and "Where morphhb resolves WLC" is stated once, in
# its subsection, and not again under the section's heading (the review of 2026-11-16, finding
# 22); "The answer in brief" states them all.
def section_defies():
    return ht(
        heading(2, "Where morphhb defies WLC", "defies"),
        subsection_defies_analysis(),
        subsection_defies_text(),
    )


# ---------------------------------------------------------------- section: the second verb


def subsection_second_analysis():
    ws = words("resolves")
    return ht(
        heading(3, "By its analysis", f"{R['s']}-analysis"),
        words_part(
            ws,
            [
                "At ",
                counted(len(ws), "word"),
                f" morphhb {R['s']} WLC by its analysis. The methods that found them looked "
                "for places where morphhb defies WLC, so these are not every word where "
                f"morphhb {R['s']} WLC.",
            ],
            f"At no word does morphhb {R['base']} WLC by its analysis.",
        ),
    )


def subsection_second_text():
    dv = divided()
    ok = dv["ok"]
    by_id = {x["id"]: x for x in decalogue_units()}
    maqaf_units = [by_id[i] for i in MAQAF_ONLY_IN_NOTE]
    six = dagesh_rafeh_atoms()
    no_maqaf = [(verse, alt) for verse, alt, lacks in six if lacks]
    assert len(no_maqaf) == 1
    nine = paseq_atoms()
    assert len(nine) == ok["divided-accents/accents+paseq"]
    return ht(
        heading(3, "By its text", f"{R['s']}-text"),
        # The definition's "reads it as one" at these atoms: WLC 4.20's atom has the marks of
        # two accentuations, which contradict each other, and morphhb's main text has the
        # atom as one of them has it (the review of 2026-11-16, finding 22).
        p(
            "In the ",
            counted(dv["verses"], "verse"),
            " of the Decalogues and ",
            vref("Genesis 35:22"),
            ", at ",
            num(dv["n_ok"]),
            " of the atoms that have an alternative note, morphhb's main text and its "
            "alternative note together have WLC 4.20's marks, and no others. There morphhb "
            f"{R['s']} WLC by its text: WLC 4.20's one atom has the marks of two "
            "accentuations, which contradict each other, and morphhb's main text reads the "
            "atom as one accentuation has it, with the other's marks in its alternative note. "
            "These ",
            num(dv["n_ok"]),
            " atoms differ from WLC 4.20 thus:",
        ),
        ol(
            [
                ht(
                    num(ok["divided-accents/accents"]),
                    " only in accents or, at ",
                    numword(len(six)),
                    " of them, at ",
                    vlist([verse for verse, _a, _l in six]),
                    ", also in the dagesh and rafeh of their first letter, which WLC 4.20's "
                    "atom has together and morphhb has apart, the dagesh in its main text "
                    "and the rafeh in its alternative note (at ",
                    vref(no_maqaf[0][0]),
                    " the alternative note's ",
                    heb(no_maqaf[0][1]),
                    " also lacks the maqaf that the main text and WLC 4.20 have after the "
                    "atom);",
                ),
                ht(
                    numword(len(nine)),
                    f" also in the PASEQ code point, which follows a {MUNAH} in the "
                    "alternative note;",
                ),
                ht(
                    numword(ok["divided-accents/pointing"]),
                    " in the maqaf, which the main text lacks and the alternative note has. "
                    "In each row of the table the first cell has morphhb's main text above "
                    "its alternative note, and the second WLC 4.20's atom above MAM's; "
                    "accents are shown.",
                ),
            ]
        ),
        decalogue_table(maqaf_units),
    )


def section_second():
    return ht(
        heading(2, f"Where morphhb {R['s']} WLC", R["s"]),
        subsection_second_analysis(),
        subsection_second_text(),
    )


# ---------------------------------------------------------------- section: follows, slips


def catchword_part():
    """The slip in one of morphhb's alternative notes at Deuteronomy 5:8, whose quotation of the
    main text (morphhb's catchWord attribute) lacks a mark of the main text's atom: a paragraph
    and a table, at the end of the slips (the review of 2026-11-16, finding 22)."""
    cw = catchword()
    return ht(
        p(
            "One of morphhb's alternative notes has a slip of another kind. At ",
            vref("Deuteronomy 5:8"),
            " the note quotes, in morphhb's ",
            code("catchWord"),
            " attribute, the words of the main text for which it gives the other "
            "accentuation, and in the first atom the quotation lacks the HEBREW ACCENT MUNAH "
            "that the main text's atom has. In the row the main text's atom stands above "
            "the quotation's.",
        ),
        table(
            ["Main text above the note's quotation", "Verse", "The note"],
            [
                [
                    form_td(cw["main"], cw["atom"]),
                    vcell("Deut 5:8"),
                    note_td(
                        "The quotation is ",
                        heb(cw["whole"]),
                        "; the note has ",
                        heb(cw["x_accent"]),
                        " in its place.",
                    ),
                ]
            ],
        ),
    )


def section_follows():
    fw, sw = words("follows"), words("slip")
    return ht(
        heading(2, "Where morphhb follows WLC, and its slips", "follows"),
        heading(3, "Where morphhb follows WLC", "follows-wlc"),
        words_part(
            fw,
            [
                "At ",
                counted(len(fw), "word"),
                " morphhb ",
                strong("follows"),
                " WLC; that is, ",
                definition("follows"),
            ],
            "At no word does morphhb follow WLC where MAM's form would be analysed otherwise.",
        ),
        heading(3, "Where morphhb has a slip", "slips"),
        words_part(
            sw,
            [
                "At ",
                counted(len(sw), "word"),
                " morphhb has a ",
                strong("slip"),
                "; that is, ",
                definition("slip"),
            ],
            "Among the words judged here, morphhb has no slip.",
        ),
        catchword_part(),
    )


# ---------------------------------------------------------------- section: the text

CLASSES = [
    # (the report's class, the page's name for it, which of the page's verdicts it is)
    ("qadma-for-first-pashta", "The pashta's stress helper", "helper"),
    (
        "Decalogue/divided accents",
        "The two accentuations of the Decalogues and Genesis 35:22",
        "divided",
    ),
    ("mark encoding only", None, "encoding"),  # its name counts its two labels
    ("word division", "Two atoms for one", "defies"),  # prose-ok: the report's label
    ("ketiv/qere representation", "A ketiv and a qere for one atom", "defies"),
    ("paseq", "Unicode PASEQ alone", None),
    ("residual", "Anything else", None),
]


# The ids of the subsections on the kinds of difference that are of encoding only (Ben's
# decision 5A): the pashta's stress helper and the ZERO WIDTH JOINERs.  The final letters in
# three ketiv words, which decision 5A also counted as neither defying nor resolving WLC, are a
# difference only from MAM-basics' conversion of WLC 4.20, not of encoding (the review of
# 2026-11-16, finding 12), in their own subsection, FINAL_LETTERS.
ENCODING_ONLY = ("text-helper", "text-zwj")
FINAL_LETTERS = "text-final"


def class_verdict(kind):
    dv = divided()
    if kind is None:
        return ""
    if kind == "helper":
        return here("text-helper", "encoding only")
    if kind == "encoding":
        return ht(
            here("text-zwj", "encoding only"),
            " for the ZERO WIDTH JOINERs; ",
            here(FINAL_LETTERS, "a difference only from MAM-basics' conversion"),
            " for the final letters",
        )
    if kind == "divided":
        return ht(
            here(f"{R['s']}-text", f"{R['s']} WLC at {num(dv['n_ok'])}"),
            "; ",
            here("defies-text", f"defies WLC at {num(len(dv['failing']))}"),
        )
    if kind == "defies":
        return here("defies-text", "defies WLC")
    raise ValueError(kind)


def subsection_version():
    # morphhb's history names its update to WLC 4.20, and none to a later version.  The count
    # of verses whose note letters differ, which was evidence only beside WLC 4.18's and WLC
    # 4.22's, and the comparison's result, which the section's opening states, are not
    # repeated here (the review of 2026-11-16, findings 11 and 20).
    named = {}
    for sha, (_date, message) in commits().items():
        for v in re.findall(r"\bWLC (?:version )?4\.(\d+)", message):
            named.setdefault(int(v), []).append(sha)
    assert max(named) == 20 and named[20] == ["2201c6a7"], named
    return ht(
        heading(3, "Which version", "text-version"),
        p(
            "The history of morphhb names its update to WLC 4.20, ",
            cm("2201c6a7", msg=True),
            ", and no update to a later version.",
        ),
    )


def subsection_classes():
    d40 = fjson("40-text-compare-data.json")
    cu = d40["class_units"]["4.20"]
    assert set(cu) <= {k for k, _t, _v in CLASSES}, cu
    vs = class_verses()
    assert list(vs) == [k for k, _t, _v in CLASSES], vs
    lu = d40["label_units"]["4.20"]
    assert lu["zwj"] + lu["final-form"] == cu["mark encoding only"]
    rows = []
    for k, title, kind in CLASSES:
        if title is None:
            title = (
                f"ZERO WIDTH JOINERs ({num(lu['zwj'])}), and final letters in ketiv words "
                f"({num(lu['final-form'])})"
            )
        rows.append(
            [
                td(title),
                td(num(cu.get(k, 0)), cls="num"),
                td(num(vs[k]), cls="num"),
                td(class_verdict(kind)),
            ]
        )
    ff = units_labelled("final-form")
    return ht(
        heading(3, "The classes of difference", "text-classes"),
        p(
            "Every unit that differs falls into one of these classes, counted in units, a unit "
            "being a differing pair of atoms or a group of atoms that differ together, and in "
            f"the verses that have one. {cap(numword(len(ENCODING_ONLY)))} kinds of "
            "difference are of encoding only: they differ in code points, not in the marks "
            "that a reader sees. A third, the final letters of ",
            counted(len(ff), "ketiv word"),
            ", is a difference only from MAM-basics' conversion of WLC 4.20: WLC 4.20's notes ",
            note("F"),
            " and ",
            note("M"),
            " mark the letter forms that morphhb has. At none of the ",
            numword(len(ENCODING_ONLY) + 1),
            f" does morphhb defy or {R['base']} WLC.",
        ),
        table(["Class", "Units", "Verses", "This page"], rows),
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
    readme_says(
        "exactly so in Deuteronomy, the one book whose saved versions include its version "
        "just before that commit, and within the saved versions' brackets in the seven other "
        "books with saved history"
    )
    return ht(
        heading(3, "Encoding only: the pashta's stress helper", "text-helper"),
        p(
            "Where WLC 4.20 has a pashta twice in an atom, its stress helper on the first "
            "letter of the stressed syllable and the pashta itself on the last letter, "
            "morphhb has HEBREW ACCENT QADMA for the helper: ",
            num(d40["label_units"]["4.20"]["qadma"]),
            " units in ",
            num(vs),
            " verses. Every WLC 4.20 atom with two pashta marks or more has exactly two, "
            "the last on the atom's last letter, and outside the Decalogues and ",
            vref("Genesis 35:22"),
            " every one is such a unit. In each row morphhb's atom stands above WLC 4.20's.",
        ),
        helper_table(["Gen 1:2", "Exod 10:28", "Deut 2:9", "Isa 23:8"]),
        p(
            "Since ",
            cm("380f4219", msg=True),
            ", morphhb has had HEBREW ACCENT QADMA for the helper. The versions of each book "
            "that the report fetched date this exactly in Deuteronomy, the one book with a "
            "fetched version just before that commit, and bracket it in seven other books.",
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


def subsection_zwj():
    lu = fjson("40-text-compare-data.json")["label_units"]["4.20"]
    assert lu["zwj"] == len(zwj_lines())
    a = ftext("78-check-zwj-qadma-history.txt")
    one(
        r"^   TOTAL          zwj=    0 qadma=11369 pashta=20647 cgj=    0 zwnj=    0$",
        a,
    )
    readme_says(
        "the saved versions date the removal exactly only in Deuteronomy and Hosea, to "
        '`56b51322` (2013-12-12, "First release of morphology"), and bracket it in Jeremiah, '
        "Judges and Leviticus"
    )
    return ht(
        heading(3, "Encoding only: ZERO WIDTH JOINERs", "text-zwj"),
        p(
            "At ",
            num(lu["zwj"]),
            " units the difference is a ZERO WIDTH JOINER, which WLC 4.20 has before a "
            "medial meteg and morphhb lacks: no file of morphhb's has a ZERO WIDTH JOINER. "
            "A ZERO WIDTH JOINER is invisible, so no form here shows it. Only in Deuteronomy "
            "and Hosea do the versions of each book that the report fetched date exactly when "
            "morphhb's text came to lack them: with ",
            cm("56b51322", msg=True),
            ". In Jeremiah, Judges and Leviticus they only bracket that commit.",
        ),
    )


def subsection_final():
    lu = fjson("40-text-compare-data.json")["label_units"]["4.20"]
    ff = units_labelled("final-form")
    assert len(ff) == lu["final-form"]
    assert [u["reference"] for u in ff] == ["Isa 9:6", "Job 38:1", "Job 40:6"]
    rows = []
    for u in ff:
        mine, w20 = (unk(u["_display"][k]) for k in ("morphhb", "4.20"))
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
                form_td(mine, w20),
                vcell(u["reference"], extra="ketiv"),
                td(ht("note ", note(ns[0]))),
            ]
        )
    return ht(
        heading(
            3, cap(f"final letters in {counted(len(ff), 'ketiv word')}"), FINAL_LETTERS
        ),
        p(
            "At ",
            counted(len(ff), "ketiv word"),
            " morphhb's letter forms differ from those of MAM-basics' conversion of WLC "
            "4.20: at ",
            vref("Isaiah 9:6"),
            " morphhb has a final mem inside the word, and at ",
            vref("Job 38:1"),
            " and ",
            vref("Job 40:6"),
            " a medial nun at its end, which WLC 4.20's notes ",
            note("F"),
            " and ",
            note("M"),
            " mark. That conversion, from WLC 4.20's Michigan-Claremont files, gives every "
            "letter at the end of a word its final form and no other letter one. In each row "
            "morphhb's ketiv stands above WLC 4.20's, as that conversion has it.",
        ),
        table(["morphhb above WLC 4.20", "Verse", "WLC 4.20's note"], rows),
    )


def subsection_checks():
    t48 = ftext("48-check-marks.txt")
    other = between(t48, "== other verses", "== divided-accent verses")
    pat = r"^   {} pashta\s+(\d+)  qadma\s+(\d+)  pashta\+qadma\s+(\d+)  zwj\s+(\d+)"
    mine = [int(x) for x in one(pat.format("morphhb "), other).groups()]
    w20 = [int(x) for x in one(pat.format(r"WLC 4\.20"), other).groups()]
    assert w20[0] - mine[0] == mine[1] - w20[1] == 3807 and mine[2] == w20[2]
    assert (mine[3], w20[3]) == (0, 79)
    q48 = one(
        r"^qadma-class units by verse kind: \{'other': (\d+), 'divided': (\d+)\}$",
        ftext("48-check-qadma-units.txt"),
    )
    # The pashta and qadma counts are of code points, a pashta and its stress helper being two
    # pashta marks but one accent (hebrew-prose, terminology.md, "Default nouns", rule 3).
    return ht(
        heading(3, "Checks", "text-checks"),
        p(
            "Counted apart from the comparison, outside the ",
            num(divided()["verses"]),
            " verses of the Decalogues and ",
            vref("Genesis 35:22"),
            ", morphhb has ",
            num(w20[0] - mine[0]),
            " fewer HEBREW ACCENT PASHTA marks and ",
            num(mine[1] - w20[1]),
            " more HEBREW ACCENT QADMA marks than WLC 4.20, with the same total of the two, "
            "and the units of the stress-helper class number ",
            num(int(q48.group(1))),
            " there and ",
            num(int(q48.group(2))),
            " inside them. WLC 4.20 has ",
            num(w20[3]),
            " ZERO WIDTH JOINERs and morphhb none: at ",
            commit("d4265dfa"),
            ", no file of morphhb's, notes and headers included, has a ZERO WIDTH JOINER, "
            "COMBINING GRAPHEME JOINER or ZERO WIDTH NON-JOINER. No commit message, issue or "
            "comment of morphhb's mentions the ZERO WIDTH JOINERs of its WLC files.",
        ),
    )


def section_text():
    verses = fjson("40-text-compare-data.json")["kstats"]["4.20"]["verses"]
    sec = section_text_parts(verses)
    assert all(f'id="{i}"' in sec for i in ENCODING_ONLY + (FINAL_LETTERS,))
    return sec


def section_text_parts(verses):
    return ht(
        heading(2, TEXT_TITLE, "text"),
        p(
            "Apart from the classes below, morphhb's text is WLC 4.20's. Compared atom by "
            "atom over all ",
            num(verses),
            " verses, every difference falls into a systematic class and none is left over.",
        ),
        p(
            "The comparison split every verse of both texts into atoms, with morphhb's ",
            code("/"),
            ", sof pasuq and white space dropped, a maqaf kept and Unicode PASEQ as a flag; "
            "compared the atoms with every mark kept, each letter's marks taken in one fixed "
            "order; aligned them by letters; and gave each difference one class by an "
            "explicit test.",
        ),
        subsection_version(),
        subsection_classes(),
        subsection_helper(),
        subsection_zwj(),
        subsection_final(),
        subsection_checks(),
    )


# ---------------------------------------------------------------- section: the records


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
            )
        )
    assert [(x["osis"], x["sha"], x["kind"]) for x in out] == [
        ("Job.19.2", "6887dd0a", "letters"),
        ("Prov.1.28", "6887dd0a", "letters"),
        ("2Kgs.21.26", "c8f43473", "vowel"),
        ("Gen.5.29", "c8f43473", "accent"),
        ("Zeph.2.15", "c8f43473", "accent"),
    ]
    return out


KIND_WORDS = {"letters": "a letter", "vowel": "a vowel", "accent": "an accent"}


@lru_cache(maxsize=None)
def wlc_divisions():
    """74-exegesis-notes.txt's notes that say "WLC has this word divided as" and give a form:
    each as (verse, the note's form, morphhb's word).  Each note's form is morphhb's word, mark
    for mark, with WLC's "/" between morphemes in place of morphhb's: the note gives WLC's
    division of the word into morphemes, not another form (the review of 2026-11-16, finding
    21)."""
    ex = ftext("74-exegesis-notes.txt")
    out = []
    head = r"^-- (\S+): WLC has this word divided as (.+?)\.  \[rdg: (.+?)\]$"
    n = int(one(r"^   (\d+) x WLC has this word divided as <rdg>\.: ", ex).group(1))
    for m in found(head, ex, n):
        verse, said, rdg = m.groups()
        assert said == rdg, verse
        before = one(r"^      before: (.*)$", ex[m.end() :].split("\n-- ")[0]).group(1)
        mine = [
            x
            for x in re.findall(r"w\[([^|\]]+)\|", before)
            if letters(x) == letters(rdg)
        ]
        assert len(mine) == 1, verse
        assert fkey(mine[0]) == fkey(rdg) and mine[0] != rdg, verse
        out.append((verse, rdg, mine[0]))
    return out


@lru_cache(maxsize=None)
def book_numbers():
    """morphhb's number for each book, from the first two digits of its words' ids in
    verdicts.json: the order of morphhb's books, which the page's tables follow."""
    out = {}
    for w in verdicts()["words"]:
        book = L.parse_ref(w["osisID"])[0]
        k = int(w["id"][:2])
        assert out.setdefault(book, k) == k, (book, w["id"])
    assert len(set(out.values())) == len(out)
    return out


def book_order_key(ref):
    """A verse's place in morphhb's order of books."""
    book, c, v = L.parse_ref(ref)
    return book_numbers()[book], c, v


def unsearched_sentence(refs):
    """The verses where morphhb defies WLC that the report's search of morphhb's issues did not
    cover, since it searched before the verdicts here were made; or nothing."""
    if not refs:
        return ""
    return ht(
        "That search, made for the report, did not cover ",
        vlist(refs),
        ", where morphhb defies WLC by the verdicts here. ",
    )


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
    one(
        r"^== Entries that describe a correction of the text or of the analysis\n   none$",
        ftext("74-revisiondesc.txt"),
    )
    ex = ftext("74-exegesis-notes.txt")
    n_ex = int(one(r"^# exegesis notes: (\d+)\.", ex).group(1))
    n_rdg = int(one(r"^   (\d+) x WLC has this word divided as <rdg>\.: ", ex).group(1))
    division, exegesis_text = division_units()
    n_div = int(one(r"^   (\d+) x " + re.escape(exegesis_text) + ": ", ex).group(1))
    assert n_div == len(division) and n_div + n_rdg == n_ex
    assert len(wlc_divisions()) == n_rdg
    t75 = ftext("75-issues.txt")
    counts = one(
        r"\((\d+) issues and PRs,\s*#?\s*(\d+) comments, (\d+) review comments\)", t75
    )
    quote = one(r"Troidl \(2017-02-03\): '([^']+)'", t75).group(1).rstrip(".")
    assert len(quote.split()) < 15
    defies = {w["id"] for w in words("defies")}
    # The verses that the report searched morphhb's issues for: the nine whose history it
    # traced, Jeremiah 51:3 and Daniel 2:39, as its README says; in the order of the page's
    # tables, which is morphhb's order of books.
    readme_says("none mentions any of the nine verses, Jeremiah 51:3 or Daniel 2:39.")
    searched = sorted(
        [v for id_, (v, _l, _m) in traced().items()] + ["Jeremiah 51:3", "Daniel 2:39"],
        key=book_order_key,
    )
    unsearched = [
        w["osisID"]
        for w in words("defies")
        if L.parse_ref(w["osisID"]) not in {L.parse_ref(v) for v in searched}
    ]
    traced_defies = [id_ for id_ in traced() if id_ in defies]
    if len(traced_defies) == len(traced()):
        which = ", all of them words where morphhb defies WLC"
    elif traced_defies:
        which = (
            f", {numword(len(traced_defies))} of them words where morphhb defies WLC"
        )
    else:
        which = ""
    return ht(
        heading(2, RECORDS_TITLE, "records"),
        p(
            "None of morphhb's records describes any of the ",
            counted(len(traced()), "word"),
            " whose history the report traced",
            which,
            ": no commit message, revision entry in a file's header, note in morphhb's "
            "text, issue, pull request or comment.",
        ),
        p(
            "Of the commits whose messages say, with a form of the word ",
            q("correct"),
            ", that something changed without saying what, only ",
            numword(len({x["sha"] for x in text_places()})),
            " change the text, and both give it WLC 4.20's forms: ",
            cm("6887dd0a", msg=True),
            " removed a letter that morphhb's text had added at ",
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
            ". The other such commits change lemmas, morphs, other attributes of the words or "
            "markup, and none touches the words whose history the report traced. In each row "
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
            " of them distinct: the conversion of 2008, the updates to later versions of "
            "WLC, the last to WLC 4.20, and the releases of the morphology. None names a "
            "change at any particular word of the text or of the analysis.",
        ),
        p(
            "Of the ",
            str(n_ex),
            " notes that morphhb marks as exegesis, ",
            str(n_div),
            " are at the places where morphhb has two atoms for one of WLC 4.20's, and the "
            "other ",
            numword(n_rdg),
            ", ",
            vref("Daniel 2:39"),
            "'s among them, say ",
            q("WLC has this word divided as"),
            " and give WLC's division of the word into morphemes, which differs from "
            "morphhb's.",
        ),
        p(
            "No issue, pull request or comment of openscriptures/morphhb mentions any of the "
            "verses ",
            vlist(searched),
            ": ",
            counts.group(1),
            " issues and pull requests, ",
            counts.group(2),
            " comments and ",
            counts.group(3),
            " review comments, fetched on 2026-11-13, were searched for each verse in several "
            "spellings and for the words' ids. ",
            unsearched_sentence(unsearched),
            "In ",
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
            " that have each other's lemmas are reported nowhere.",
        ),
    )


# ---------------------------------------------------------------- section: the limits


def c61(label):
    return int(
        one(r"^   " + re.escape(label) + r"\s+(\d+)$", ftext("61-summary.txt")).group(1)
    )


def x_counts():
    sec = between(ftext("51-general-test.txt"), "== 2. Counts", "== 3.")
    xs = found(r"^   X   (\S.*?)\s+(\d+)$", sec, 4)
    return {m.group(1): int(m.group(2)) for m in xs}


def census_words():
    sec = between(ftext("50-alel-census.txt"), "== 1. Counts", "== 2.")
    n = int(
        one(r"^morphhb words whose last morpheme is alef-lamed: (\d+)$", sec).group(1)
    )
    assert n == len(census()[1])
    return n


def section_limits():
    t58 = ftext("58-ketiv-qere-analyses.txt")
    k = one(r"^  different lemma main number\s+(\d+)$", t58).group(1)
    a = c61("A. pairs (deduped by morphhb id and MAM's form key)")
    a2 = c61("A2. pairs whose own form is rare (inconclusive)")
    b = c61("B. letters-differ pairs (one-to-one non-equal blocks)")
    untestable = c61("A1.  of them, MAM's form absent from morphhb (untestable)")
    hol = one(
        r"(\d,\d{3}) pairs differ only by a holam in MAM's form,\s+(\d,\d{3}) of them the "
        r"Tetragrammaton",
        ftext("61-summary.txt"),
    )
    nr = wlc_note_rows()
    xs = sum(x_counts().values())
    by_source = Counter(w["source"] for w in verdicts()["words"])
    beyond = beyond_methods(k, untestable)
    return ht(
        heading(2, "What these methods cannot find", "limits"),
        p(
            "The report judged ",
            counted(by_source["methods"] + by_source["brief"], "word"),
            ": ",
            num(by_source["methods"]),
            " that its methods found and ",
            num(by_source["brief"]),
            " more that its brief, the request that it answered, named. The verdicts here "
            "also judge the ",
            num(by_source["rare list"]),
            " words that its general test listed as too rare for it to judge. Its methods:",
        ),
        ol(
            [
                ht(
                    "A general test of lemmas and morphs. It aligned morphhb's atoms with "
                    "MAM's by letters, ketiv side with ketiv side and qere side with qere "
                    "side, and took the ",
                    num(a),
                    " one-to-one pairs whose letters agree and whose forms differ once "
                    "accents, meteg and rafeh are set aside (",
                    hol.group(1),
                    " of them differ only by a holam in MAM's form, ",
                    hol.group(2),
                    " of those in the Tetragrammaton), and the ",
                    num(b),
                    " pairs whose letters differ. It flags a word when its lemma, its morph "
                    "or both are common among the other occurrences of MAM's form (at least "
                    "50%) and rare among those of its own form (at most 10% of at least 5). "
                    "For the ",
                    num(a2),
                    " pairs whose own form is rarer, two further tests do the same with "
                    "other occurrences in place of its own form's: those of the other forms "
                    "with the same letters, and those of morphhb's words where MAM has the "
                    "word's form.",
                ),
                ht(
                    "A census of morphhb's ",
                    num(census_words()),
                    " words whose last morpheme has the letters alef and lamed.",
                ),
                ht(
                    "WLC's notes: the ",
                    num(nr["U"]["differ"]),
                    " chanted words under note ",
                    note("U"),
                    " whose forms differ from MAM's.",
                ),
                ht("The report's reading of ", num(xs), " pairs that no test flags."),
            ]
        ),
        p(cap(numword(len(beyond))), " kinds of place are beyond these methods:"),
        ol(beyond),
    )


def beyond_methods(k, untestable):
    """The kinds of place that the report's methods cannot find, as list items."""
    return [
        "A word whose form in WLC 4.20 and in MAM is the same: the methods compare "
        "the two.",
        "A difference in accents, meteg or rafeh, which the general test sets aside.",
        ht(
            "A word whose own form is too rare for the general test, or one of the ",
            num(untestable),
            " pairs whose form in MAM never occurs in morphhb, unless another "
            "method found it.",
        ),
        "A letter difference outside a one-to-one block of the alignment.",
        ht(
            "A ketiv analysed by its qere: at ",
            vref("Isaiah 52:5"),
            " the ketiv has the qere's lemma, while ",
            k,
            " other ketiv words have their own.",
        ),
        "Anything about the Leningrad Codex itself: no image was consulted.",
    ]


# ---------------------------------------------------------------- section: the departures


def report_label(v):
    """A verdict of the report's, as verdicts.json's "report" field names it."""
    if v in NOT_JUDGED:
        return ht("not judged")
    return code(v)


def semicolon_list(parts):
    """Parts joined by semicolons, the last after "and"."""
    parts = list(parts)
    if len(parts) == 1:
        return ht(parts[0])
    return ht(hj(parts[:-1], "; "), "; and ", parts[-1])


def departure_verdicts():
    ws = verdicts()["words"]
    pairs = Counter((w["report"], w["verdict"]) for w in ws)
    order = REPORT_VERDICTS + NOT_JUDGED
    rows = []
    for (rv, v), n in sorted(
        pairs.items(),
        key=lambda x: (order.index(x[0][0]), (LISTED + COUNTED).index(x[0][1])),
    ):
        rows.append([td(report_label(rv)), td(verdict_name(v)), td(num(n), cls="num")])
    # The words that the report judged whose verdict here is not the one corresponding to the
    # report's: those whose departure brings them onto this page's lists, takes them off, or
    # moves them from one list to another (changed), and those that stay off the lists
    # (off).  Words that the report did not judge are counted in the table above.
    departed = [
        w
        for w in ws
        if w["report"] in COUNTERPART and COUNTERPART[w["report"]] != w["verdict"]
    ]
    changed = [
        w
        for w in departed
        if w["verdict"] in LISTED or COUNTERPART[w["report"]] in LISTED
    ]
    off = [w for w in departed if w not in changed]
    moved = [
        w
        for w in changed
        if w["verdict"] in LISTED and COUNTERPART[w["report"]] in LISTED
    ]
    parts = [
        heading(3, "The verdicts", "departures-verdicts"),
        p(
            "The verdicts here are those of ",
            code("in/morphhb-verdicts-2026-11-16/verdicts.json"),
            ", which Claude wrote on 2026-11-16 by this page's definitions, not the "
            "report's. The file records each word's verdict in the report beside its verdict "
            "here, and the report's verdicts correspond to this page's thus: ",
            semicolon_list(
                [
                    ht(
                        and_list(
                            [code(rv) for rv in REPORT_VERDICTS if COUNTERPART[rv] == v]
                        ),
                        " to ",
                        verdict_name(v),
                    )
                    for v in dict.fromkeys(COUNTERPART.values())
                ]
            ),
            ". For each verdict of the report's, the words and their verdicts here:",
        ),
        table(["The report's verdict", "This page's verdict", "Words"], rows),
    ]
    assert changed, "the sentences below assume that some words change lists"
    if changed:
        parts.append(
            p(
                "The verdict here departs from the one that corresponds to the report's at ",
                counted(len(departed), "word"),
                ". At ",
                numword(len(changed)),
                " of them the word comes onto this page's lists, leaves them, or moves from "
                "one to another",
                moved_clause(moved),
                "; each word's reason is in its table above or, for a word that leaves the "
                "lists, in ",
                code("verdicts.json"),
                ", and the words are below.",
            )
        )
        parts.append(
            table(
                ["Verse", "The report's verdict", "This page's verdict"],
                [
                    [
                        vcell(w["osisID"]),
                        td(report_label(w["report"])),
                        td(verdict_name(w["verdict"])),
                    ]
                    for w in changed
                ],
            )
        )
    if off:
        parts.append(
            p(
                "At the other ",
                numword(len(off)),
                " the word stays off the lists, and its reason is in ",
                code("verdicts.json"),
                ": ",
                off_list(off),
                ".",
            )
        )
    return ht(*parts)


def moved_clause(moved):
    """The words that move from one of this page's lists to another, each with its two
    verdicts, as a parenthesis; or nothing."""
    if not moved:
        return ""
    return ht(
        " (",
        and_list(
            [
                ht(
                    "at ",
                    vref(w["osisID"]),
                    " from ",
                    verdict_name(COUNTERPART[w["report"]]),
                    " to ",
                    verdict_name(w["verdict"]),
                )
                for w in moved
            ]
        ),
        ")",
    )


def verses_with_counts(ws):
    """The verses of ws, each once, in their order, a verse with more than one word followed by
    how many."""
    n = Counter(w["osisID"] for w in ws)
    out = []
    for ref in dict.fromkeys(w["osisID"] for w in ws):
        out.append(ht(vref(ref), f" ({counted(n[ref], 'word')})" if n[ref] > 1 else ""))
    return and_list(out)


def off_list(off):
    """The words whose verdict departs from the report's without bringing them onto this
    page's lists, grouped by the report's verdict and this page's."""
    groups = {}
    for w in off:
        groups.setdefault((w["report"], w["verdict"]), []).append(w)
    order = REPORT_VERDICTS + NOT_JUDGED
    keys = sorted(
        groups, key=lambda k: (order.index(k[0]), (LISTED + COUNTED).index(k[1]))
    )
    return semicolon_list(
        [
            ht(
                "from ",
                report_label(rv),
                " to ",
                verdict_name(v),
                " at ",
                verses_with_counts(groups[(rv, v)]),
            )
            for rv, v in keys
        ]
    )


def departure_decalogues():
    by_id = {x["id"]: x for x in decalogue_units()}
    v1, v2 = by_id["059vS"], by_id["05fou"]
    readme = (L.F / "README.md").read_text(encoding="utf-8")
    quote = (
        "Changes of letters, vowels or maqaf are confined to three words of the Decalogues, "
        "Daniel 2:39's ketiv and qere and the 12 words that morphhb divides for exegesis."
    )
    assert " ".join(readme.split()).count(quote) == 1
    assert readme.count("\n### The answer\n") >= 1
    pointing = fjson("40-text-compare-data.json")["label_units"]["4.20"][
        "divided-accents/pointing"
    ]
    shown = [x for x in decalogue_units() if x["label"] == "divided-accents/pointing"]
    assert len(shown) == pointing == 5
    n_fail = len([x for x in shown if x["union_test"] != "ok"])
    n_ok = len([x for x in shown if x["union_test"] == "ok"])
    assert (n_fail, n_ok) == (3, 2)
    # The chanted words that hold Deuteronomy 5:8's atom, which the tracked data give; they do
    # not give Deuteronomy 5:7's, since the report's listing of those verses' atoms omits an
    # atom that equals WLC 4.20's and has no alternative note (divided_lines), so the page
    # names that one as an atom (hebrew-prose: name a compound whole where it can be shown).
    c8 = deut58_compounds()
    assert c8["unit"]["main"] == v2["main"]
    return ht(
        heading(3, "The Decalogues' vowels and maqaf", "departures-decalogues"),
        p(
            "The report's README, in its answer for all of morphhb, item 4, says: ",
            q(quote),
            " Its three are the atoms where WLC 4.20's atom is not the union of morphhb's "
            "main text and its alternative note and the difference is a vowel or the maqaf. "
            "But the report's ",
            code("out/41-text-residuals.json"),
            " has ",
            counted(pointing, "unit"),
            " labelled ",
            code("divided-accents/pointing"),
            " (the label's count in ",
            code("out/40-text-compare-data.json"),
            "), and at two of them morphhb's main text lacks WLC 4.20's maqaf after the "
            "atom while its alternative note has it, so that the union test passes there: "
            "the atom ",
            heb(v1["main"]),
            " at ",
            vref("Deuteronomy 5:7"),
            ", and the atom ",
            heb(v2["main"]),
            " at ",
            vref("Deuteronomy 5:8"),
            ", which WLC 4.20 has in the chanted word ",
            heb(c8["wlc"]),
            ", morphhb's main text in ",
            heb(c8["main"]),
            " and its alternative note in ",
            heb(c8["alt"]),
            ". This page says both: at ",
            counted(pointing, "atom"),
            " morphhb's main text differs from WLC 4.20 in a vowel or the maqaf; at ",
            numword(n_fail),
            " of them morphhb defies WLC, and at ",
            numword(n_ok),
            f" it {R['s']} WLC.",
        ),
    )


def section_departures():
    return ht(
        heading(2, "Where this page departs from the report", "departures"),
        p(
            "Where the report's verdicts or its README differ from what this page says, "
            "this page says what its data show, and why."
        ),
        departure_verdicts(),
        departure_decalogues(),
    )


# ---------------------------------------------------------------- exports

TEXT_TITLE = "The text of morphhb against WLC 4.20"
RECORDS_TITLE = "What morphhb's records say"
SECTIONS = [
    ("answer", "The answer in brief", section_answer),
    ("defies", "Where morphhb defies WLC", section_defies),
    (R["s"], f"Where morphhb {R['s']} WLC", section_second),
    ("follows", "Where morphhb follows WLC, and its slips", section_follows),
    ("text", TEXT_TITLE, section_text),
    ("records", RECORDS_TITLE, section_records),
    ("limits", "What these methods cannot find", section_limits),
    ("departures", "Where this page departs from the report", section_departures),
]


def self_test(built):
    """The checks of the scratch script's self-test, on the sections as the generator built
    them, each an (id, title, section) triple: each section opens with its heading, and no id
    is used twice."""
    ids = []
    for id_, title, sec in built:
        assert isinstance(sec, H), id_
        assert sec.startswith(heading(2, title, id_)), id_
        ids += re.findall(r'\bid="([^"]+)"', sec)
    assert [b[0] for b in built] == [s[0] for s in SECTIONS]
    assert len(ids) == len(set(ids)), sorted(i for i in ids if ids.count(i) > 1)
