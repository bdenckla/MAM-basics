"""Build the feasibility study's page, morphhb-on-mam/out/morphhb-on-mam.html.

Written by Claude (Opus 5.5) on 2026-11-15 to morphhb-on-mam/in/page-spec.md, for the study
that morphhb-on-mam/README.md describes, and moved into this package on 2026-11-16, when the
study was put on ice.  Every figure and every Hebrew form on the page is read here from the
study's outputs: morphhb-on-mam/out/30-figures.json, the breakdown files beside it (01-, 20-,
22-, 25-, 26- and 29-), the example lists (21-, 23- and 27-), and the records of
10-atoms*.jsonl and 11-unmatched-morphhb.jsonl in the work directory; the alignment's
running time and the inputs' commits come from morphhb-on-mam/README.md.  No figure and no
Hebrew letter is typed in this file.  The judgments shown as "Claude's first reading" are
Claude's, keyed here by verse and morphhb id; the sentences that say what differs are made
from the records, except where a record's claim is checked here.

Sections 6 and 7, and the part of section 5 about what a product's generator would dispatch
on, come verbatim from morphhb-on-mam/in/page-fragment.html, which the study's root session
wrote: each is a <section> found by its id (FRAGMENT_IDS).  A part that the fragment lacks, or
all three when the file is missing, gets a pending paragraph, and the script prints a warning.

write_page(work_dir) writes the page and morphhb-on-mam/out/40-page-text.txt, the page's
visible text (page_text.py).
"""

import ast
import collections
import difflib
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

from morphhb_on_mam import align as AL
from morphhb_on_mam import analyze as AN
from morphhb_on_mam import figures as FG
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import page_text
from morphhb_on_mam import record_paths

OUT = record_paths.out_dir()
PAGE = record_paths.page_path()
TEXT = record_paths.page_text_path()
FRAGMENT = record_paths.fragment_path()
README = record_paths.readme_path()
# How the page names the record's files, and its way up from out/ to the repository root.
RECORD_SHOWN = record_paths.RECORD_NAME + "/"
OUT_SHOWN = RECORD_SHOWN + "out/"
TO_ROOT = "../../"
FRAGMENT_IDS = ("generator-dispatch", "upkeep", "shape-upstream")
PENDING = (
    "Pending: this part waits for the root session's check of the research reports."
)
NBSP = "\N{NO-BREAK SPACE}"
MAQAF = C.MAQAF
VAV = "\N{HEBREW LETTER VAV}"
HE = "\N{HEBREW LETTER HE}"
STRANDS = ("cant-combined", "cant-alef", "cant-bet")
ATOM_FILES = {
    "cant-combined": "10-atoms.jsonl",
    "cant-alef": "10-atoms-cant-alef.jsonl",
    "cant-bet": "10-atoms-cant-bet.jsonl",
}

BOOK_NAMES = {
    "Gen": "Genesis",
    "Exod": "Exodus",
    "Lev": "Leviticus",
    "Num": "Numbers",
    "Deut": "Deuteronomy",
    "Josh": "Joshua",
    "Judg": "Judges",
    "1Sam": "1 Samuel",
    "2Sam": "2 Samuel",
    "1Kgs": "1 Kings",
    "2Kgs": "2 Kings",
    "Isa": "Isaiah",
    "Jer": "Jeremiah",
    "Ezek": "Ezekiel",
    "Hos": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obad": "Obadiah",
    "Jonah": "Jonah",
    "Mic": "Micah",
    "Nah": "Nahum",
    "Hab": "Habakkuk",
    "Zeph": "Zephaniah",
    "Hag": "Haggai",
    "Zech": "Zechariah",
    "Mal": "Malachi",
    "Ps": "Psalms",
    "Prov": "Proverbs",
    "Job": "Job",
    "Song": "Song of Songs",
    "Ruth": "Ruth",
    "Lam": "Lamentations",
    "Eccl": "Ecclesiastes",
    "Esth": "Esther",
    "Dan": "Daniel",
    "Ezra": "Ezra",
    "Neh": "Nehemiah",
    "1Chr": "1 Chronicles",
    "2Chr": "2 Chronicles",
}
if set(BOOK_NAMES) != {osis for osis, _tu, _mc in C.BOOKS}:
    raise ValueError("BOOK_NAMES does not cover mhb_common.BOOKS exactly")

# The flagged examples that page-spec.md names, by verse and morphhb id, each with Claude's
# first reading.
FLAGGED = [
    (
        "Judg.19.4",
        "07GJ8",
        "A real change: MAM's form is a Hiphil, where morphhb's morph says Qal.",
    ),
    (
        "2Chr.1.5",
        "14A4a",
        "A real change: MAM's shin dot makes the word “there”; morphhb's lemma and morph "
        "are those of “he put”, which its sin dot makes.",
    ),
    (
        "2Chr.15.16",
        "144SZ",
        "A real change: MAM's vowel under the lamed implies the article, which morphhb's "
        "morph lacks.",
    ),
    (
        "Jer.11.2",
        "24Rdh",
        "A real change: MAM's form is second person plural, where morphhb's is singular "
        "with a suffix.",
    ),
    (
        "2Sam.15.3",
        "10Jp4",
        "A real change: MAM has the plural, where morphhb's morph says singular.",
    ),
    (
        "Ps.68.27",
        "19MkY",
        "A real change: MAM has another word, so morphhb's lemma and morph do not fit it.",
    ),
    (
        "Deut.2.9",
        "057a3",
        "A real change of the morph only: morphhb's lemma already fits MAM's form, the "
        "negative particle; its morph fits morphhb's own form, the preposition.",
    ),
    (
        "1Kgs.1.15",
        "11VTb",
        "Only a homograph: elsewhere MAM's form is mostly another word, and morphhb's "
        "analysis of this name fits it.",
    ),
    (
        "Num.23.25",
        "04QZ8",
        "Only a homograph: elsewhere MAM's form has another suffix, and morphhb's analysis "
        "fits it.",
    ),
]

# The two qamats qatan cases that page-spec.md names, with Claude's first reading.
QATAN = [
    (
        "2Kgs.8.6",
        "12LrY",
        "A real difference: MAM's qamats qatan makes the form an infinitive or a noun, "
        "where morphhb's morph says a third feminine singular perfect.",
    ),
    (
        "Mic.2.10",
        "33PUg",
        "A real difference: MAM's qamats qatan makes the form an infinitive or a noun, "
        "where morphhb's morph says a third feminine singular perfect.",
    ),
]

# Sentences saying what differs where the letters differ in a way that the generic
# description below does not cover.
DIFFERS = {("Ps.68.27", "19MkY"): "The two texts have different words here."}

# Examples that page-spec.md names by verse alone.
STRUCTURAL_VIDS = ("Num.2.12", "2Sam.7.22", "Dan.5.19")
KQ_VID = "Gen.49.10"
ONE_FORM_VID = "1Sam.2.9"
STRAND_VID = "Exod.20.3"
BOUNDARY_VID = "Num.23.13"
EMPTY_TARGET_VID = "Exod.26.6"
LEGARMEH_VID = "Ruth.3.13"

MARK_NAMES = {
    "shewa": "shewa",
    "hataf-segol": "ḥataf segol",
    "hataf-patah": "ḥataf pataḥ",
    "hataf-qamats": "ḥataf qamats",
    "hiriq": "ḥiriq",
    "tsere": "tsere",
    "segol": "segol",
    "patah": "pataḥ",
    "qamats": "qamats",
    "holam": "ḥolam",
    "holam-haser": "ḥolam ḥaser",
    "qubuts": "qubuts",
    "qamats-qatan": "qamats qatan",
    "shin-dot": "shin dot",
    "sin-dot": "sin dot",
}
if set(MARK_NAMES) | {"dagesh"} != set(AL.VOWELS.values()) | set(
    AL.OTHER_MARKS.values()
):
    raise ValueError("MARK_NAMES does not cover align.py's mark names exactly")
ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth"]

# analyze.cons_class's labels, by tier.
CONS_TIER = {
    "supported: MAM's form has this lemma and morph elsewhere": "supported",
    "MAM's form not elsewhere in morphhb": "untested",
    "contradicted in morph: same lemma elsewhere, never this morph": "flagged",
    "contradicted in lemma: same morph elsewhere, never this lemma": "flagged",
    "contradicted in both": "flagged",
}
TIER_NAMES = {
    "same": "the same form",
    "supported": "supported",
    "untested": "untested",
    "flagged": "flagged",
    "structural": "structural",
}
TIER_MEANINGS = {
    "same": "MAM's atom has the letters and the vowel key of its morphhb word, or is an "
    "unpointed ketiv with the letters of morphhb's ketiv",
    "supported": "the form differs, but morphhb gives MAM's form this same lemma and morph "
    "elsewhere",
    "untested": "MAM's form occurs nowhere else in morphhb",
    "flagged": "MAM's form occurs elsewhere in morphhb, never with this lemma and morph",
    "structural": "no one-to-one partner: the texts divide words differently, structure a "
    "ketiv and qere differently, or one lacks a word",
}
# analyze.letters_diff_class's labels.
B_KINDS = {
    "mater missing in MAM": "MAM lacks a vowel letter that morphhb has",
    "mater added in MAM": "MAM has a vowel letter that morphhb lacks",
    "matres both ways": "vowel letters differ both ways",
    "other letters": "other letters differ",
}
# analyze.py's shapes of class C blocks.
C_SHAPES = {
    "MAM's trivial ketiv/qere (one form) where morphhb has a ketiv and a qere": "MAM "
    "has one form, a trivial ketiv and qere, where morphhb has a ketiv and a qere",
    "MAM plain where morphhb has a ketiv and a qere": "MAM has a plain atom where morphhb "
    "has a ketiv and a qere",
    "division into atoms differs (same letters)": "the texts divide the same letters into words "
    "differently",
    "MAM ketiv/qere with another structure in morphhb": "morphhb structures MAM's ketiv and "
    "qere differently",
    "MAM atom(s) with no morphhb word": "MAM has one atom or more with no morphhb word",
    "letters and division differ": "both the letters and the division differ",
}
# analyze3.py's parts of a one-form case.
ONE_FORM_KINDS = {"kq-trivial": "a trivial ketiv and qere", "plain": "a plain atom"}
ONE_FORM_ANALYSES = {
    "analyses agree": "the same analysis",
    "same lemma, morphs differ": "the same lemma, different morphs",
    "lemmas differ": "different lemmas",
    "several ketiv or qere words": "more than one word on a side",
}
ONE_FORM_LETTERS = {
    "MAM's letters are the ketiv's": "ketiv",
    "the qere's": "qere",
    "neither's": "neither",
}
MAQAF_KINDS = {
    "none": "no maqaf",
    "maqaf": "a maqaf",
    "implicit maqaf": "a maqaf implicit in the manuscript",
}
# The morph parts that the page names, in morphhb's codes.
PART_GLOSS = {
    "Nc": "common nouns",
    "Vqw": "Qal wayyiqtol forms",
    "Np": "proper nouns",
    "Vqc": "Qal infinitives construct",
    "Vqv": "Qal imperatives",
}
# analyze.sig_class's kinds of a pointing difference other than the Tetragrammaton's xolam.
SIG_KINDS = {
    "several letters": "differences at more than one letter",
    "dagesh or mappiq only": "a dagesh or mappiq alone",
    "shin or sin dot only": "a shin or sin dot alone",
    "holam in morphhb only": "a ḥolam in morphhb alone",
}


def warn(msg):
    print("warning: " + msg, file=sys.stderr)


# ------------------------------------------------------------------ reading the outputs


def read_text(name):
    return (OUT / name).read_text(encoding="utf-8")


def read_json(name):
    return json.loads(read_text(name))


def sections(name):
    """{number: [lines]} of an analysis file whose sections begin '== N. '."""
    out, cur = {}, None
    for line in read_text(name).splitlines():
        m = re.match(r"== (\d+)\. ", line)
        if m:
            cur = int(m.group(1))
            out[cur] = [line]
        elif cur is not None:
            out[cur].append(line)
    return out


def match_one(pattern, lines):
    hits = [m for m in (re.match(pattern, line) for line in lines) if m]
    if len(hits) != 1:
        raise ValueError("%d lines match %r" % (len(hits), pattern))
    return hits[0]


def count_lines(lines, start=1):
    """{label: n} from lines '  <n>  <label>' (the first `start` lines skipped)."""
    out = collections.OrderedDict()
    for line in lines[start:]:
        m = re.match(r"^ +(\d+)  (\S.*)$", line)
        if m:
            if m.group(2) in out:
                raise ValueError("label twice: %r" % line)
            out[m.group(2)] = int(m.group(1))
    return out


def nested_counts(lines):
    """{kind: (n, {cons label: m})} from analyze.py's two-level lists: kinds end in column
    8, their breakdowns in column 16.  Reading stops at the first blank line after the list.
    """
    out, kind, started = collections.OrderedDict(), None, False
    for line in lines[1:]:
        if not line.strip():
            if started:
                break
            continue
        m = re.match(r"^( +)(\d+)  (\S.*)$", line)
        if not m:
            if started:
                raise ValueError("unparsed line %r" % line)
            continue
        width = len(m.group(1)) + len(m.group(2))
        if width == 8:
            kind = m.group(3)
            out[kind] = (int(m.group(2)), collections.OrderedDict())
            started = True
        elif width == 16:
            out[kind][1][m.group(3)] = int(m.group(2))
        else:
            raise ValueError("unexpected indentation %r" % line)
    return out


def by_tier(breakdown):
    """{tier: n} from {cons label: n}."""
    out = collections.Counter()
    for label, n in breakdown.items():
        out[CONS_TIER[label]] += n
    return out


def readme_facts():
    text = README.read_text(encoding="utf-8")

    def one(pattern):
        hits = re.findall(pattern, text)
        if len(hits) != 1:
            raise ValueError("README.md: %d matches of %r" % (len(hits), pattern))
        return hits[0]

    return {
        "seconds": int(one(r"`align\.py` takes about (\d+) seconds per strand")),
        "morphhb": one(r"\*\*morphhb\*\* `wlc/` at `([0-9a-f]+)`"),
        "morphhb_same": one(r"the same tree as `([0-9a-f]+)`'s"),
        "mam": one(r"at the checkout's `([0-9a-f]+)`"),
    }


def show_pairs_ids():
    """{vid: [morphhb ids in order]} from out/29-show-pairs.txt."""
    out = {}
    for line in read_text("29-show-pairs.txt").splitlines():
        m = re.match(r"^(\S+)  morphhb: (.+)$", line)
        if m:
            out[m.group(1)] = [tok.rsplit(" ", 1)[1] for tok in m.group(2).split(" | ")]
    return out


def rec_ids(rec):
    ids = set()
    if "w" in rec:
        ids.add(rec["w"]["id"])
    for side in rec.get("ws", {}).values():
        for w in side:
            ids.add(w["id"])
    return ids


def stream(path, vids, holam=False):
    """Every record of the verses `vids` in the file `path`, by vid in file order, read line by
    line; with holam, also the first A2 record of each kind of Tetragrammaton (bare and with
    a prefix) whose only difference is MAM's ḥolam."""
    keys = ['"vid": "%s"' % v for v in vids]
    by_vid = collections.defaultdict(list)
    first = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = None
            if any(k in line for k in keys):
                rec = json.loads(line)
                if rec["vid"] in vids:
                    by_vid[rec["vid"]].append(rec)
            if holam and len(first) < 2 and '"class": "A2"' in line:
                rec = rec or json.loads(line)
                if AN.sig_class(rec).startswith("holam in MAM only"):
                    letters = C.letters(rec["text"])
                    if letters == AN.YHWH:
                        first.setdefault("bare", rec)
                    elif letters.endswith(AN.YHWH):
                        first.setdefault("prefixed", rec)
    return by_vid, first


def find(by_vid, vid, wid):
    hits = [r for r in by_vid[vid] if wid in rec_ids(r)]
    if len(hits) != 1:
        raise ValueError("%s %s: %d records" % (vid, wid, len(hits)))
    return hits[0]


# ------------------------------------------------------------------ HTML pieces


def fmt(n):
    return "{:,}".format(n)


def pct(x):
    return "{:.2f}%".format(x)


def esc(s):
    return html.escape(s, quote=False)


def hb(form):
    return '<span lang="hbo" dir="rtl" class="big">%s</span>' % esc(C.mnorm(form))


def code(s):
    return "<code>%s</code>" % esc(s)


def ref(vid):
    book, ch, v = vid.split(".")
    return "%s%s%s:%s" % (BOOK_NAMES[book].replace(" ", NBSP), NBSP, ch, v)


def ref_range(vids):
    """Verses of one chapter, consecutive, as 'Book c:v–w'."""
    parts = [v.split(".") for v in vids]
    if len({(b, c) for b, c, _v in parts}) != 1:
        raise ValueError("not one chapter: %r" % vids)
    nums = sorted(int(v) for _b, _c, v in parts)
    if nums != list(range(nums[0], nums[-1] + 1)):
        raise ValueError("not consecutive: %r" % vids)
    first = ref(".".join(parts[0][:2] + [str(nums[0])]))
    return first if len(nums) == 1 else "%s\N{EN DASH}%d" % (first, nums[-1])


def link(href, text, kind="page"):
    return '<a href="%s" data-na-link="%s">%s</a>' % (href, kind, text)


def outf(name):
    """A link to an output file small enough to open in a browser."""
    return link(name, code(OUT_SHOWN + name))


def P(s):
    return "<p>%s</p>" % s


NUMBER_WORDS = "zero one two three four five six seven eight nine".split()


def num(n):
    """A count for running prose: a word below ten, else digits."""
    return NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else fmt(n)


def times(n):
    return {1: "once", 2: "twice"}.get(n, "%s times" % num(n))


def and_list(items):
    items = list(items)
    if len(items) < 3:
        return " and ".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def mam_form(rec):
    if rec["implicit_maqaf"]:
        raise ValueError("%s: an implicit maqaf in an example" % rec["vid"])
    return rec["text"] + (MAQAF if rec["maqaf_after"] else "")


def w_form(w):
    return w["text"] + (MAQAF if w["maqaf_after"] else "")


def join_forms(forms_and_maqafs):
    """Forms of consecutive atoms, a space after each that no maqaf ends."""
    out = ""
    for form in forms_and_maqafs:
        out += form + ("" if form.endswith(MAQAF) else " ")
    return out.strip()


def analysis(w):
    return "lemma %s<br>morph %s<br>id %s" % (
        code(w["lemma"]),
        code(w["morph"]),
        code(w["id"]),
    )


def analysis_line(w, label=None):
    s = "lemma %s, morph %s, id %s" % (
        code(w["lemma"]),
        code(w["morph"]),
        code(w["id"]),
    )
    return "%s: %s" % (label, s) if label else s


def table(caption, headers, rows, cls="compare"):
    return (
        '<table class="%s breakout"><caption>%s</caption><thead><tr>%s</tr></thead>'
        "<tbody>\n%s\n</tbody></table>"
        % (cls, caption, "".join("<th>%s</th>" % h for h in headers), "\n".join(rows))
    )


def num_row(label, *nums):
    return "<tr><td>%s</td>%s</tr>" % (
        label,
        "".join(
            '<td class="num">%s</td>' % ("" if n is None else fmt(n)) for n in nums
        ),
    )


def form_row(labels, forms, vid, analysis_html, notes):
    """One example: a cell of labels, a cell of forms one above the other, the verse,
    morphhb's analysis and the Latin notes."""
    if len(labels) != len(forms):
        raise ValueError("%s: %d labels for %d forms" % (vid, len(labels), len(forms)))
    return (
        '<tr><td class="labels">%s</td><td dir="rtl" class="stack">%s</td>'
        '<td class="bcv">%s</td><td class="analysis">%s</td>%s</tr>'
        % (
            "<br>".join(labels),
            "<br>".join(hb(f) for f in forms),
            ref(vid),
            analysis_html,
            "".join('<td class="note"><div>%s</div></td>' % n for n in notes),
        )
    )


FORM_HEADERS = ["", "forms", "verse", "morphhb's analysis"]


# ------------------------------------------------------------------ what differs


def article(name):
    return ("an " if name[0] in "aeiou" else "a ") + name


def letter_name(ch):
    name = unicodedata.name(ch)
    prefix = "HEBREW LETTER "
    if not name.startswith(prefix):
        raise ValueError("not a Hebrew letter: %r" % ch)
    words = name[len(prefix) :].lower().split()
    return " ".join("ḥet" if w == "het" else w for w in words)


def letter_ref(letters, k):
    """The name of letter k of `letters`, with an ordinal if the letter occurs twice."""
    same = [i for i, c in enumerate(letters) if c == letters[k]]
    name = letter_name(letters[k])
    return ORDINALS[same.index(k)] + " " + name if len(same) > 1 else name


def mark_phrase(names, letter, marks, last):
    words = []
    for nm in names:
        if nm == "dagesh":
            if letter == VAV and not set(marks) & set(AL.VOWELS.values()):
                words.append("shuruq dot")
            elif letter == HE and last:
                words.append("mappiq")
            else:
                words.append("dagesh")
        else:
            words.append(MARK_NAMES[nm])
    return " and ".join(article(w) for w in words)


def describe_sig(sig, text):
    """A sentence for a letters-equal pair: what MAM's and morphhb's letters have."""
    letters = C.letters(text)
    clauses = []
    for k, letter, wm, mm in sig:
        removed = sorted(set(wm) - set(mm))
        added = sorted(set(mm) - set(wm))
        last = k == len(letters) - 1
        name = letter_ref(letters, k)
        if added and removed:
            clauses.append(
                "MAM's %s has %s where morphhb's has %s"
                % (
                    name,
                    mark_phrase(added, letter, mm, last),
                    mark_phrase(removed, letter, wm, last),
                )
            )
        elif added:
            clauses.append(
                "MAM's %s has %s, which morphhb's lacks"
                % (name, mark_phrase(added, letter, mm, last))
            )
        elif removed:
            clauses.append(
                "morphhb's %s has %s, which MAM's lacks"
                % (name, mark_phrase(removed, letter, wm, last))
            )
        else:
            raise ValueError("an empty difference in %r" % text)
    return "; ".join(clauses) + "."


def letter_map(w_letters, m_letters):
    """{index in morphhb's letters: index in MAM's} for the letters that align."""
    amap = {}
    sm = difflib.SequenceMatcher(None, w_letters, m_letters, autojunk=False)
    for tag, i1, i2, j1, _j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                amap[i] = j1 + (i - i1)
    return amap


def where(letters, i):
    before = "the " + letter_ref(letters, i - 1) if i > 0 else None
    after = "the " + letter_ref(letters, i + 1) if i + 1 < len(letters) else None
    if before and after:
        return "between %s and %s" % (before, after)
    return "after " + before if before else "before " + after


def describe_letters(w_text, m_text):
    """A sentence for a spelling pair whose letters differ by single vowel letters."""
    a, b = C.letters(w_text), C.letters(m_text)
    clauses = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert" and j2 - j1 == 1 and b[j1] in AN.MATRES:
            clauses.append(
                "MAM has %s %s, which morphhb's form lacks"
                % (article(letter_name(b[j1])), where(b, j1))
            )
        elif tag == "delete" and i2 - i1 == 1 and a[i1] in AN.MATRES:
            clauses.append(
                "morphhb's form has %s %s, which MAM's lacks"
                % (article(letter_name(a[i1])), where(a, i1))
            )
        else:
            raise ValueError("no description of %r against %r" % (w_text, m_text))
    return "; ".join(clauses) + "."


def describe(rec):
    """One sentence saying what differs between MAM's atom and its morphhb word."""
    w = rec["w"]
    key = (rec["vid"], w["id"])
    if key in DIFFERS:
        return DIFFERS[key]
    if rec["class"] == "A1":
        sig = AL.signature(w["text"], rec["text"])
        if sig:
            return describe_sig(sig, rec["text"])
        if C.fkey(w["text"]) == C.fkey(rec["text"]):
            if "/" in w["text"]:
                return "The two are identical but for morphhb's slash."
            return "The two are identical."
        return "They differ only in marks that the vowel key ignores."
    if rec["class"] == "A2":
        return describe_sig(rec["sig"], rec["text"])
    if rec["class"] == "B":
        return describe_letters(w["text"], rec["text"])
    raise ValueError("%s: no description for class %s" % (key, rec["class"]))


def tm(n):
    return "never" if n == 0 else times(n)


def elsewhere(cons):
    """What the test of support found: how morphhb analyses MAM's form elsewhere."""
    n, pair = cons["n"], cons["pair"]
    if n == 0:
        return "MAM's form occurs nowhere else in morphhb."
    head = "MAM's form occurs %s elsewhere in morphhb" % times(n)
    if pair == n:
        how = {1: "with", 2: "both times with"}.get(n, "always with")
        return "%s, %s this lemma and morph." % (head, how)
    if pair:
        return "%s, %s of them with this lemma and morph." % (head, fmt(pair))
    top, k = cons["top"]
    number, morph = top.split(" | ")
    if k == n:
        has = "there it has" if n == 1 else "there it always has"
    else:
        has = "most often (%s) it has" % times(k)
    return (
        "%s, never with this lemma and morph together (this lemma %s, this morph %s); "
        "%s lemma %s and morph %s."
        % (head, tm(cons["lemma"]), tm(cons["morph"]), has, code(number), code(morph))
    )


def check_reading(rec):
    """Raise unless the record bears out the facts that Claude's first reading of it states
    (FLAGGED): the judgment is Claude's, the facts are the data's."""
    key = (rec["vid"], rec["w"]["id"])
    morph = rec["w"]["morph"]
    number = AL.lemma_number(rec["w"]["lemma"])
    top, k = rec["cons"]["top"]
    top_number, top_morph = top.split(" | ")
    sig = rec.get("sig", [])
    facts = {
        ("Judg.19.4", "07GJ8"): "/Vq" in morph and "/Vh" in top_morph,
        ("2Chr.1.5", "14A4a"): len(sig) == 1
        and "sin-dot" in sig[0][2]
        and "shin-dot" in sig[0][3]
        and top_number != number,
        ("2Chr.15.16", "144SZ"): "Rd" in top_morph and "Rd" not in morph,
        ("Jer.11.2", "24Rdh"): "2ms/S" in morph and top_morph.endswith("2mp"),
        ("2Sam.15.3", "10Jp4"): "Ncmsc" in morph and "Ncmpc" in top_morph,
        ("Ps.68.27", "19MkY"): top_number != number,
        ("Deut.2.9", "057a3"): top_number == number and top_morph != morph,
        ("1Kgs.1.15", "11VTb"): top_number != number and 2 * k > rec["cons"]["n"],
        ("Num.23.25", "04QZ8"): top_number == number
        and top_morph != morph
        and top_morph.rsplit("/", 1)[0] == morph.rsplit("/", 1)[0],
    }
    if not facts[key]:
        raise ValueError("%s %s: the record does not bear out the reading" % key)


def tier_note(rec):
    t = FG.tier(rec)
    return "<strong>%s</strong>: %s" % (TIER_NAMES[t], elsewhere(rec["cons"]))


def pair_row(rec, *extra, cons=True):
    notes = [describe(rec)]
    if cons:
        notes.append(elsewhere(rec["cons"]))
    notes.extend(extra)
    return form_row(
        ["MAM", "morphhb"],
        [mam_form(rec), w_form(rec["w"])],
        rec["vid"],
        analysis(rec["w"]),
        notes,
    )


# ------------------------------------------------------------------ the inputs


class Inputs:
    pass


def load(work_dir):
    D = Inputs()
    D.work_shown = record_paths.in_repo(work_dir) + "/"
    D.F = read_json("30-figures.json")
    D.cov = sections("20-coverage.txt")
    D.ref = sections("22-refine.txt")
    D.kq = sections("26-kq-ids-slashes.txt")
    D.strands_lines = read_text("25-strands.txt").splitlines()
    D.census = read_text("01-mam-census.txt").splitlines()
    D.ex = read_json("21-examples.json")
    D.lists = read_json("23-lists.json")
    D.kqj = read_json("27-kq-ids-slashes.json")
    D.readme = readme_facts()
    D.pairs_ids = show_pairs_ids()
    D.unmatched = [
        json.loads(line)
        for line in (work_dir / "11-unmatched-morphhb.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]

    # The examples, by verse.
    D.ex_pointing = D.ex[
        "A2 one letter: hataf-patah -> shewa / supported: MAM's form has this lemma and "
        "morph elsewhere"
    ][0]
    D.ex_missing = D.ex[
        "B mater missing in MAM / supported: MAM's form has this lemma and morph elsewhere"
    ][0]
    D.ex_added = D.ex[
        "B mater added in MAM / supported: MAM's form has this lemma and morph elsewhere"
    ][0]
    D.ex_untested = D.ex[
        "A2 one letter: hataf-patah -> shewa / MAM's form not elsewhere in morphhb"
    ][0]
    D.slash_a1 = [e for e in D.ex["slash A1 example"] if e["vid"] == "Gen.1.5"]
    D.slash_b = [e for e in D.ex["slash B example"] if e["vid"] == "Gen.19.16"]
    if len(D.slash_a1) != 1 or len(D.slash_b) != 1:
        raise ValueError("the slash examples are not in 21-examples.json")
    D.slash_a1, D.slash_b = D.slash_a1[0], D.slash_b[0]
    D.fallback = D.kqj["fallback placed"][0]
    D.ambiguous = D.kqj["still ambiguous"][0]
    D.kq_plain = D.kqj["MAM kq, morphhb plain"][0]
    D.nine = []
    for line in D.ref[3][1:]:
        m = re.match(r"^  (\S+) \[(.+?)\] class (\w+); cons (.+)$", line)
        if m:
            (wid,) = ast.literal_eval("[" + m.group(2) + "]")
            D.nine.append((m.group(1), wid, m.group(3), ast.literal_eval(m.group(4))))
    if not D.nine:
        raise ValueError("22-refine.txt section 3 has no corrections")
    contradicted = {
        (x["vid"], x["id"])
        for x in D.lists["A2 contradicted"] + D.lists["B contradicted"]
    }
    for vid, wid, _reading in FLAGGED:
        if (vid, wid) not in contradicted:
            raise ValueError("%s %s is not flagged in 23-lists.json" % (vid, wid))
    qatan_list = {
        (x["vid"], x["id"]) for x in D.lists["qatan with a perfect or participle morph"]
    }
    for vid, wid, _reading in QATAN:
        if (vid, wid) not in qatan_list:
            raise ValueError("%s %s is not in the qamats qatan list" % (vid, wid))

    vids = {"Gen.1.1", KQ_VID, ONE_FORM_VID, STRAND_VID, BOUNDARY_VID}
    vids |= set(STRUCTURAL_VIDS)
    vids |= {
        D.ex_pointing["vid"],
        D.ex_missing["vid"],
        D.ex_added["vid"],
        D.ex_untested["vid"],
        D.slash_a1["vid"],
        D.slash_b["vid"],
        D.fallback["vid"],
        D.ambiguous["vid"],
        D.kq_plain["vid"],
    }
    vids |= {vid for vid, _w, _r in FLAGGED + QATAN}
    vids |= {vid for vid, _w, _c, _cons in D.nine}
    D.recs, D.holam = stream(work_dir / "10-atoms.jsonl", vids, holam=True)
    if set(D.holam) != {"bare", "prefixed"}:
        raise ValueError("no Tetragrammaton example of each kind")
    D.strand_recs = {"cant-combined": D.recs[STRAND_VID]}
    for strand in STRANDS[1:]:
        D.strand_recs[strand] = stream(work_dir / ATOM_FILES[strand], {STRAND_VID})[0][
            STRAND_VID
        ]
    return D


# ------------------------------------------------------------------ the sections


def sec_head(D):
    return [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>morphhb's morphology on MAM: a feasibility study</title>",
        '<link rel="stylesheet" href="../../gh-pages/document.css">',
        '<link rel="stylesheet" href="../../gh-pages/MAM-with-doc/misc/style.css">',
        '<link rel="stylesheet" href="../../gh-pages/near-aleppo/link-presentation.css">',
        STYLE,
        "</head>",
        "<body>",
        "<h1>morphhb's morphology on MAM: a feasibility study</h1>",
        '<p class="ai-caveat"><strong>Not reviewed by a human.</strong> Claude (Opus 5.5) '
        "wrote this page on 2026-11-15, at Ben Denckla's request; no person has checked "
        "it. Every reading is attributed to the transcription that has it: morphhb, whose "
        "text is WLC 4.20's, or MAM, as MAM-simple gives it in the BHS versification. "
        "Nothing on this page says what the Leningrad Codex itself has.</p>",
    ]


STYLE = """<style>
span.big[lang="hbo"] { font-size: 220%; line-height: 1.6; }
span.huge[lang="hbo"] { font-size: 320%; line-height: 1.5; }
table.data, table.anatomy, table.compare { border-collapse: collapse; }
table.breakout { width: max-content; max-width: var(--breakout-table-max-width);
  margin: 1.2em 0 1.2em 50%; transform: translateX(var(--breakout-table-shift)); }
table.data td, table.data th, table.anatomy td, table.anatomy th,
table.compare td, table.compare th {
  border: 1px solid light-dark(#bbb, #555); padding: .35em .6em; vertical-align: middle; }
table caption { caption-side: top; text-align: left; padding: 0 0 .4em; }
table.anatomy td { text-align: center; }
table.anatomy th.rowlabel { text-align: left; font-weight: normal; font-style: italic; }
table.anatomy td.morpheme { padding: .1em .9em; }
td.form, td.stack { text-align: right; white-space: nowrap; }
td.bcv { white-space: nowrap; padding-left: .5em; }
td.lemma, td.morph { font-size: 95%; }
code { white-space: nowrap; }
nav.contents li { margin: .15em 0; }
/* Added for this page.  A stack of compared forms and its cell of labels share one line
   height, so that each label stands level with its form. */
td.stack, td.labels { line-height: 3.6em; }
td.labels { white-space: nowrap; }
td.analysis { font-size: 95%; white-space: nowrap; }
td.note > div { min-width: 12em; max-width: 24em; }
td.num { text-align: right; }
p.pending { font-style: italic; }
</style>"""


FRAGMENT_HEADINGS = {
    "upkeep": "6. Upkeep",
    "shape-upstream": "7. Product shape and upstream",
}


def heading_text(part):
    """The text of a fragment section's <h2>, or None."""
    m = re.search(r"<h2\b[^>]*>(.*?)</h2>", part, re.S)
    if not m:
        return None
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split())


def sec_nav(frag):
    items = [
        ("answer", "1. The answer"),
        ("method", "2. How the comparison was made"),
        ("coverage", "3. Coverage, tier by tier"),
        ("slashes", "4. Morpheme division"),
        ("markup", "5. MAM's markup"),
        ("upkeep", None),
        ("shape-upstream", None),
        ("not-established", "8. What this study could not establish"),
        ("files", "9. Files"),
    ]
    lis = []
    for anchor, text in items:
        if text is None:
            text = esc(heading_text(frag.get(anchor, "")) or FRAGMENT_HEADINGS[anchor])
        lis.append("<li>%s</li>" % link("#" + anchor, text, "down"))
    return ['<nav class="contents"><ul>', *lis, "</ul></nav>"]


def sec_answer(D):
    F = D.F
    t = F["tiers"]
    total = F["mam_atoms"]
    good = t["same"] + t["supported"]
    rest = t["untested"] + t["flagged"] + t["structural"]
    if good + rest != total or set(t) != set(TIER_NAMES):
        raise ValueError("the tiers do not add up")
    g1 = D.recs["Gen.1.1"][0]
    out = ['<h2 id="answer">1. The answer</h2>']
    out.append(
        P(
            "morphhb, the morphology of the Open Scriptures Hebrew Bible, analyses the text "
            "of the Westminster Leningrad Codex, WLC 4.20. Its unit is the "
            "<code>&lt;w&gt;</code> element, called here <strong>morphhb's word</strong>: "
            "one written form between spaces or maqaf marks, which this page calls an "
            "<strong>atom</strong>, as against a <strong>chanted word</strong>, which is an "
            "atom or a whole maqaf compound. For each word morphhb gives a "
            "<strong>lemma</strong>, the dictionary word that each of its parts belongs "
            "to, as the number of its headword in Strong's Hebrew dictionary with a letter "
            "for each prefix; a <strong>morph code</strong>, or morph, which names each "
            "part's part of speech and features, such as a verb's stem, person, gender and "
            "number; and an <strong>id</strong>, a short code that names that one word, "
            "such as %s." % code(g1["w"]["id"])
        )
    )
    out.append(
        P(
            "Applying this morphology to MAM's text, Miqra According to the Masorah, is "
            "feasible. An <strong>alignment</strong>, a pairing of each of MAM's atoms "
            "with the morphhb word that corresponds to it, found by comparing their "
            "letters, gives %s of MAM's %s atoms morphhb's lemma, morph and id with "
            "evidence that they fit: either the atom has the same form as its morphhb "
            "word, or morphhb gives MAM's form that same lemma and morph elsewhere. The "
            "other %s atoms (%s) need a rule or a person. The cost is an alignment that "
            "takes about %d seconds to run, a review queue of the %s flagged and "
            "structural atoms, and rules, or a reader, for the %s untested ones."
            % (
                pct(round(100.0 * good / total, 2)),
                fmt(total),
                fmt(rest),
                pct(round(100.0 * rest / total, 2)),
                D.readme["seconds"],
                fmt(t["flagged"] + t["structural"]),
                fmt(t["untested"]),
            )
        )
    )
    rows = []
    for tier in TIER_NAMES:
        classes = sorted(
            (
                (n, key.split("/")[1])
                for key, n in F["tier_by_class"].items()
                if key.split("/")[0] == tier
            ),
            reverse=True,
        )
        rows.append(
            '<tr><td>%s</td><td class="num">%s</td><td class="num">%s</td><td>%s</td>'
            "<td>%s</td></tr>"
            % (
                TIER_NAMES[tier],
                fmt(t[tier]),
                pct(F["tiers_percent"][tier]),
                TIER_MEANINGS[tier],
                "; ".join("%s %s" % (cls, fmt(n)) for n, cls in classes),
            )
        )
    rows.append(
        '<tr><td>all</td><td class="num">%s</td><td></td><td></td><td></td></tr>'
        % fmt(total)
    )
    out.append(
        table(
            "MAM's atoms by tier, each atom counted once (%s). The shares are rounded, so "
            "that their sum differs slightly from the whole; section 2 explains the "
            "classes." % outf("30-figures.json"),
            ["tier", "atoms", "share", "what it means", "by class"],
            rows,
            cls="data",
        )
    )
    return out


def sec_method(D):
    rd = D.readme
    out = ['<h2 id="method">2. How the comparison was made</h2>']
    out.append(
        P(
            "For each verse, %s lines up morphhb's words with MAM's atoms by their letters, "
            "once on the ketiv side of the verse and once on its qere side, as the "
            "2026-11-13 study's “Method 2” did (%s): Python's difflib finds the longest "
            "runs of atoms whose letters agree, so that a word that one text lacks or "
            "divides differently leaves a block of atoms unpaired. On the ketiv side a "
            "ketiv stands in its place, on the qere side its qere, and the plain atoms are "
            "on both sides; an atom on both sides is counted once, so that each of MAM's "
            "atoms is counted once."
            % (
                code("py/morphhb_on_mam/align.py"),
                link(
                    TO_ROOT + "in/morphhb-corrections-2026-11-13/README.md",
                    "its README",
                ),
            )
        )
    )
    out.append(
        P(
            "The <strong>vowel key</strong> of a form keeps its letters, its vowels, a "
            "dagesh or mappiq, and the shin and sin dots. It ignores the accents, meteg, "
            "rafeh, the upper and lower dots and invisible characters, and it reads a "
            "qamats qatan as a qamats and a ḥolam ḥaser as a ḥolam. Each of MAM's atoms "
            "gets a class, which the output files name:"
        )
    )
    out.append(
        "<ul>"
        "<li><strong>A1</strong>: one morphhb word with the same letters and the same "
        "vowel key;</li>"
        "<li><strong>A2</strong>: one morphhb word with the same letters and another vowel "
        "key;</li>"
        "<li><strong>K</strong>: an unpointed ketiv of MAM's with the letters of one "
        "morphhb word, morphhb's ketiv, which is unpointed too, or, in a few verses, a "
        "plain word;</li>"
        "<li><strong>B</strong>: one morphhb word whose letters differ;</li>"
        "<li><strong>C</strong>: no one-to-one partner, in a block of several atoms or "
        "words, or with no partner at all;</li>"
        "<li><strong>AX</strong>: the same letters, but a different morphhb word on the "
        "ketiv side and on the qere side.</li>"
        "</ul>"
    )
    out.append(
        P(
            "Where the forms differ (A2 and B), the test of support counts how morphhb "
            "analyses MAM's exact form, by the vowel key, everywhere else in its text, its "
            "ketiv and qere words included. If any of those occurrences has this word's "
            "lemma and morph, MAM's atom is supported; if MAM's form occurs but never with "
            "that lemma and morph, it is flagged; if MAM's form never occurs, it is "
            "untested. The test compares a lemma by its Strong's number alone, without "
            "its prefixes or the letter that marks one of several entries under one "
            "number."
        )
    )
    out.append(
        P(
            "Every Hebrew form on this page was copied from the outputs by %s and is shown "
            "in MAM-normal mark order, the order that MAM-basics gives the marks of a "
            "letter, whatever order its source has; the vowel key sorts each letter's "
            "marks, so the comparison does not depend on their order. The inputs are "
            "morphhb's <code>wlc/</code> at %s, whose files are identical to those at %s, "
            "and MAM-simple's JSON in the BHS versification at MAM-basics' %s."
            % (
                code("py/morphhb_on_mam/build_page.py"),
                code(rd["morphhb"]),
                code(rd["morphhb_same"]),
                code(rd["mam"]),
            )
        )
    )
    return out


def sec_coverage(D):
    F = D.F
    t, tbc = F["tiers"], F["tier_by_class"]
    cov2 = nested_counts(D.cov[2])
    out = ['<h2 id="coverage">3. Coverage, tier by tier</h2>']

    # The same form.
    g1 = D.recs["Gen.1.1"][0]
    if g1["class"] != "A1":
        raise ValueError("Genesis 1:1's first atom is not A1")
    out.append('<h3 id="same">The same form</h3>')
    out.append(
        P(
            "Of MAM's atoms, %s have the same form as their morphhb word: %s of class A1 "
            "and %s unpointed ketiv atoms with the letters of morphhb's ketiv. For these, "
            "morphhb's lemma, morph and id apply as they stand. Genesis 1:1's first atom "
            "is an example. Its record, one line of %s, holds MAM's atom, morphhb's word "
            "with its id, lemma and morph, the class, and MAM's atom with morphhb's slash "
            "placed."
            % (
                fmt(t["same"]),
                fmt(tbc["same/A1"]),
                fmt(tbc["same/K"]),
                code(D.work_shown + "10-atoms.jsonl"),
            )
        )
    )
    out.append(
        table(
            "Genesis 1:1's first atom, from its record.",
            FORM_HEADERS + ["what differs"],
            [pair_row(g1, cons=False)],
        )
    )

    # The Tetragrammaton's xolam.
    h = F["a2_holam_only"]
    holam_kinds = [k for k in cov2 if k.startswith("holam in MAM only")]
    holam_tiers = collections.Counter()
    for k in holam_kinds:
        holam_tiers.update(by_tier(cov2[k][1]))
    all_holam = sum(h.values())
    if (
        holam_tiers["supported"] != F["a2_holam_only_supported"]
        or sum(holam_tiers.values()) != all_holam
    ):
        raise ValueError("the ḥolam figures disagree")
    for kind in ("bare", "prefixed"):
        if FG.tier(D.holam[kind]) != "supported":
            raise ValueError("the first %s Tetragrammaton is not supported" % kind)
    out.append('<h3 id="holam">Supported: the Tetragrammaton\'s ḥolam</h3>')
    out.append(
        P(
            "In %s atoms of class A2 the only difference is a ḥolam that MAM's "
            "Tetragrammaton has and morphhb's lacks: %s bare Tetragrammata and %s with a "
            "prefix; %s other atoms, too, differ only by a ḥolam of MAM's. Of all %s, %s "
            "are supported, %s untested and %s flagged."
            % (
                fmt(h["bare"] + h["prefixed"]),
                fmt(h["bare"]),
                fmt(h["prefixed"]),
                num(h["other"]),
                fmt(all_holam),
                fmt(holam_tiers["supported"]),
                fmt(holam_tiers["untested"]),
                fmt(holam_tiers["flagged"]),
            )
        )
    )
    out.append(
        table(
            "The first bare Tetragrammaton and the first with a prefix in %s."
            % code(D.work_shown + "10-atoms.jsonl"),
            FORM_HEADERS + ["what differs", "elsewhere in morphhb"],
            [pair_row(D.holam["bare"]), pair_row(D.holam["prefixed"])],
        )
    )

    # Other pointing.
    other = F["a2_other_than_holam_by_tier"]
    if sum(other.values()) != F["a2_other_than_holam"]:
        raise ValueError("the other pointing figures disagree")
    kinds = [(k, v[0]) for k, v in cov2.items() if k not in holam_kinds]
    kinds.sort(key=lambda kv: -kv[1])
    out.append('<h3 id="pointing">Supported: other pointing</h3>')
    commonest = ["%s (%s)" % (sig_kind_phrase(k), fmt(n)) for k, n in kinds[:3]]
    out.append(
        P(
            "The other %s atoms of class A2 differ in other points. The commonest kinds "
            "are %s and %s; %s, section 2, gives every kind. Of the %s, %s are supported, "
            "%s untested and %s flagged."
            % (
                fmt(F["a2_other_than_holam"]),
                ", ".join(commonest[:-1]),
                commonest[-1],
                outf("20-coverage.txt"),
                fmt(F["a2_other_than_holam"]),
                fmt(other["supported"]),
                fmt(other["untested"]),
                fmt(other["flagged"]),
            )
        )
    )
    rec = find(D.recs, D.ex_pointing["vid"], D.ex_pointing["id"])
    out.append(
        table(
            "The first example of its kind in %s." % outf("21-examples.json"),
            FORM_HEADERS + ["what differs", "elsewhere in morphhb"],
            [pair_row(rec)],
        )
    )

    # Spelling.
    bl, bt = F["b_by_letters"], F["b_by_tier"]
    cov6 = nested_counts(D.cov[6])
    if set(cov6) != set(B_KINDS) or {k: v[0] for k, v in cov6.items()} != bl:
        raise ValueError("the spelling figures disagree")
    out.append('<h3 id="spelling">Supported: spelling</h3>')
    out.append(
        P(
            "In %s atoms (class B) MAM's letters differ from those of their one morphhb "
            "word, most often by a vowel letter, a vav or a yod: in %s MAM lacks one that "
            "morphhb has, in %s MAM has one that morphhb lacks, in %s they differ both "
            "ways, and in %s other letters differ. Of the %s, %s are supported, %s "
            "untested and %s flagged."
            % (
                fmt(sum(bl.values())),
                fmt(bl["mater missing in MAM"]),
                fmt(bl["mater added in MAM"]),
                fmt(bl["matres both ways"]),
                fmt(bl["other letters"]),
                fmt(sum(bl.values())),
                fmt(bt["supported"]),
                fmt(bt["untested"]),
                fmt(bt["flagged"]),
            )
        )
    )
    rows, sums = [], collections.Counter()
    for kind in B_KINDS:
        n, breakdown = cov6[kind]
        tiers = by_tier(breakdown)
        sums.update(tiers)
        rows.append(
            num_row(
                B_KINDS[kind],
                tiers["supported"],
                tiers["untested"],
                tiers["flagged"],
                n,
            )
        )
    if dict(sums) != bt:
        raise ValueError("the spelling tiers disagree")
    rows.append(
        num_row(
            "all",
            bt["supported"],
            bt["untested"],
            bt["flagged"],
            sum(bl.values()),
        )
    )
    out.append(
        table(
            "The spelling pairs by kind and tier (%s, section 6)."
            % outf("20-coverage.txt"),
            ["kind", "supported", "untested", "flagged", "all"],
            rows,
            cls="data",
        )
    )
    out.append(
        table(
            "The first supported example of a vowel letter that MAM lacks and of one "
            "that MAM has, in %s." % outf("21-examples.json"),
            FORM_HEADERS + ["what differs", "elsewhere in morphhb"],
            [
                pair_row(find(D.recs, e["vid"], e["id"]))
                for e in (D.ex_missing, D.ex_added)
            ],
        )
    )

    # Flagged.
    out.append('<h3 id="flagged">Flagged</h3>')
    out.append(
        P(
            "Of MAM's atoms, %s are flagged: %s that differ in pointing and %s in "
            "spelling. In each, MAM's form occurs elsewhere in morphhb, but never with "
            "this word's lemma and morph, so morphhb's analysis may not fit it. Claude's "
            "first reading counts about half of the %s as real changes, where MAM's form "
            "needs another lemma or morph, and half as homographs or interpretive "
            "choices, where morphhb's analysis can stand; no person has reviewed them. "
            "The full lists are %s's “A2 contradicted” and “B contradicted”, shown "
            "compactly in %s and %s."
            % (
                fmt(t["flagged"]),
                fmt(tbc["flagged/A2"]),
                fmt(tbc["flagged/B"]),
                fmt(t["flagged"]),
                outf("23-lists.json"),
                outf("28-show-a2-contradicted.txt"),
                outf("28-show-b-contradicted.txt"),
            )
        )
    )
    rows = []
    for vid, wid, reading in FLAGGED:
        rec = find(D.recs, vid, wid)
        if FG.tier(rec) != "flagged":
            raise ValueError("%s %s is not flagged" % (vid, wid))
        check_reading(rec)
        rows.append(pair_row(rec, reading))
    out.append(
        table(
            "Some flagged atoms. The last column is Claude's first reading, which no "
            "person has reviewed.",
            FORM_HEADERS
            + ["what differs", "elsewhere in morphhb", "Claude's first reading"],
            rows,
        )
    )

    # Untested.
    rec = find(D.recs, D.ex_untested["vid"], D.ex_untested["id"])
    if FG.tier(rec) != "untested":
        raise ValueError("the untested example is not untested")
    out.append('<h3 id="untested">Untested</h3>')
    out.append(
        P(
            "Of MAM's atoms, %s are untested: MAM's form occurs nowhere else in morphhb, "
            "so the test can neither support nor flag morphhb's analysis. Of them, %s are "
            "of class A2 and %s of class B. They need a reader, or acceptance by a rule."
            % (fmt(t["untested"]), fmt(tbc["untested/A2"]), fmt(tbc["untested/B"]))
        )
    )
    out.append(
        table(
            "The first untested example in %s." % outf("21-examples.json"),
            FORM_HEADERS + ["what differs", "elsewhere in morphhb"],
            [pair_row(rec)],
        )
    )

    out.extend(sec_structural(D))
    out.extend(sec_hidden(D))
    out.extend(sec_nine(D))
    return out


def sig_kind_phrase(kind):
    if kind in SIG_KINDS:
        return SIG_KINDS[kind]
    m = re.fullmatch(r"one letter: (\S+) -> (\S+)", kind)
    if not m:
        raise ValueError("no phrase for %r" % kind)

    def names(s):
        if s == "none":
            return None
        return " and ".join(
            article("dagesh" if n == "dagesh" else MARK_NAMES[n]) for n in s.split("+")
        )

    w, mam = names(m.group(1)), names(m.group(2))
    if w and mam:
        return "%s in MAM where morphhb has %s" % (mam, w)
    if mam:
        return "%s in MAM where morphhb has none" % mam
    return "no vowel in MAM where morphhb has %s" % w


def sec_structural(D):
    F = D.F
    t, tbc = F["tiers"], F["tier_by_class"]
    cov7, cov8 = D.cov[7], D.cov[8]
    m = match_one(r"^  blocks: (\d+), holding (\d+) MAM atoms$", cov7)
    n_blocks, n_atoms = int(m.group(1)), int(m.group(2))
    shapes = count_lines(cov7, start=2)
    if set(shapes) != set(C_SHAPES) or sum(shapes.values()) != n_blocks:
        raise ValueError("the block shapes disagree")
    if n_atoms != tbc["structural/C"] or (
        tbc["structural/C"] + tbc["structural/K"] + tbc["structural/AX"]
        != t["structural"]
    ):
        raise ValueError("the structural figures disagree")
    no_word = count_lines(D.kq[3])["C: no morphhb word at all"]
    out = ['<h3 id="structural">Structural</h3>']
    out.append(
        P(
            "Of MAM's atoms, %s have no one-to-one partner in morphhb: %s of class C, %s "
            "ketiv atoms whose morphhb partner is one plain word (class K), and %s of "
            "class AX, whose letters meet a different morphhb word on the ketiv side and "
            "on the qere side. The %s of class C lie in %s blocks. Of their atoms, %s have "
            "no morphhb word at all, and the others share a block with one morphhb word "
            "or more (%s, section 3); either way a rule or a person has to give each atom "
            "an id, one of morphhb's or a new one."
            % (
                fmt(t["structural"]),
                fmt(tbc["structural/C"]),
                fmt(tbc["structural/K"]),
                fmt(tbc["structural/AX"]),
                fmt(n_atoms),
                fmt(n_blocks),
                num(no_word),
                outf("26-kq-ids-slashes.txt"),
            )
        )
    )
    rows = [num_row(C_SHAPES[shape], n) for shape, n in shapes.items()]
    rows.append(num_row("all", n_blocks))
    out.append(
        table(
            "The blocks of class C by shape (%s, section 7). A trivial ketiv and qere is "
            "MAM-simple's <code>kq-trivial</code>, a ketiv and qere “whose two forms differ "
            "in a way that needs no separate display”, as its documentation says."
            % outf("20-coverage.txt"),
            ["shape", "blocks"],
            rows,
            cls="data",
        )
    )

    # Numbers 2:12, 2 Samuel 7:22 and Daniel 5:19.
    unm = {}
    for u in D.unmatched:
        unm.setdefault((u["vid"], u["w"]["id"]), u)
    rows = []
    num_vid, sam_vid, dan_vid = STRUCTURAL_VIDS
    (c,) = [r for r in D.recs[num_vid] if r["class"] == "C"]
    ws = c["ws"]["k"]
    if (
        c["ws"]["q"] != ws
        or len(ws) != 2
        or C.letters(c["text"]) != "".join(C.letters(w["text"]) for w in ws)
    ):
        raise ValueError("Numbers 2:12 is not one atom against two words")
    rows.append(
        form_row(
            ["MAM", "morphhb"],
            [mam_form(c), join_forms([w_form(w) for w in ws])],
            num_vid,
            "<br>".join(analysis_line(w) for w in ws),
            [
                "MAM has the name as one atom; morphhb has it as %s words joined "
                "by a maqaf, each with its own lemma." % num(len(ws))
            ],
        )
    )
    for vid in (sam_vid, dan_vid):
        lone = [r for r in D.recs[vid] if r["class"] == "C"]
        if not lone or any(any(r["ws"].values()) for r in lone):
            raise ValueError("%s: no atom without a morphhb word" % vid)
        verse_unm = [u for (v, _i), u in unm.items() if v == vid]
        order = D.pairs_ids[vid]
        # The one paired atom next to MAM's lone atoms whose morphhb word stands next to
        # the unmatched morphhb words.
        w_lo = min(order.index(u["w"]["id"]) for u in verse_unm) - 1
        w_hi = max(order.index(u["w"]["id"]) for u in verse_unm) + 1
        m_lo = min(r["j"]["k"] for r in lone) - 1
        m_hi = max(r["j"]["k"] for r in lone) + 1
        partner = [
            r
            for r in D.recs[vid]
            if "w" in r
            and r["w"]["id"] in order
            and w_lo <= order.index(r["w"]["id"]) <= w_hi
            and m_lo <= r["j"].get("k", -1) <= m_hi
        ]
        if len(partner) != 1:
            raise ValueError("%s: %d partners" % (vid, len(partner)))
        mam_span = sorted(lone + partner, key=lambda r: r["j"]["k"])
        words = [partner[0]["w"]] + [u["w"] for u in verse_unm]
        words.sort(key=lambda w: order.index(w["id"]))
        if vid == sam_vid:
            if (vid, partner[0]["w"]["id"]) not in {
                (x["vid"], x["id"]) for x in D.lists["A2 contradicted"]
            }:
                raise ValueError("2 Samuel 7:22's pair is not flagged")
            if not (
                C.letters(mam_span[0]["text"]) == AN.YHWH
                and C.letters(words[-1]["text"]) == AN.YHWH
                and len(mam_span) == len(words) == 2
            ):
                raise ValueError("2 Samuel 7:22 is not as described")
            note = (
                "MAM has the Tetragrammaton followed by another word; morphhb has another "
                "word followed by the Tetragrammaton. The alignment pairs the two "
                "Tetragrammata, so that MAM's second atom has no morphhb word and "
                "morphhb's first word no MAM atom; the pair is itself one of the flagged "
                "pointing atoms."
            )
        else:
            m_end = [C.letters(r["text"])[-1] for r in mam_span]
            w_end = [C.letters(w["text"])[-1] for w in words]
            if not (
                len(mam_span) == len(words) == 3
                and [C.letters(r["text"])[:-1] for r in mam_span]
                == [C.letters(w["text"])[:-1] for w in words]
                and m_end[0] == w_end[2]
                and m_end[2] == w_end[0]
                and m_end[0] != m_end[2]
                and C.letters(mam_span[2]["text"]) == C.letters(words[0]["text"])
                and len(lone) == len(verse_unm)
            ):
                raise ValueError("Daniel 5:19 is not as described")
            note = (
                "MAM and morphhb exchange the final %s and %s of the first and third of "
                "these atoms. The alignment pairs MAM's third atom with morphhb's first, "
                "whose letters agree, and leaves %s atoms unpaired on each side: an "
                "artifact of the alignment, not a missing word."
                % (letter_name(m_end[0]), letter_name(m_end[2]), num(len(lone)))
            )
        rows.append(
            form_row(
                ["MAM", "morphhb"],
                [
                    join_forms([mam_form(r) for r in mam_span]),
                    join_forms([w_form(w) for w in words]),
                ],
                vid,
                "<br>".join(analysis_line(w) for w in words),
                [note],
            )
        )
    out.append(
        table(
            "%s structural cases. For %s and %s the forms are a run of atoms of each text "
            "(%s)."
            % (
                num(len(rows)).capitalize(),
                ref(sam_vid),
                ref(dan_vid),
                outf("29-show-pairs.txt"),
            ),
            FORM_HEADERS + ["what happens"],
            rows,
        )
    )

    # The morphhb words that no MAM atom matches.
    m = re.search(r"side words: (\d+)$", cov8[0])
    m2 = match_one(
        r"^  distinct morphhb words: (\d+); in verses MAM lacks: (\d+)$", cov8
    )
    distinct, absent = int(m2.group(1)), int(m2.group(2))
    if (
        int(m.group(1)) != F["morphhb_side_words_unmatched"]
        or distinct != F["morphhb_words_unmatched_distinct"]
        or absent != F["morphhb_words_unmatched_in_absent_verses"]
    ):
        raise ValueError("the unmatched figures disagree")
    words = []
    for line in cov8[2:]:
        wm = re.match(r"^  (\S+) (\S+) .+ sides (\d+)$", line)
        if wm:
            words.append((wm.group(1), wm.group(2), int(wm.group(3))))
    if len(words) != distinct:
        raise ValueError("the unmatched words disagree")
    absent_vids = sorted(
        {u["vid"] for u in D.unmatched if u["absent_verse"]},
        key=lambda v: int(v.split(".")[2]),
    )
    one_side = [vid for vid, _wid, sides in words if sides == 1]
    by_vid = collections.Counter(
        vid for vid, _wid, sides in words if sides == 2 and vid not in absent_vids
    )
    never = match_one(
        r"^  morphhb words in a delete block on some side: (\d+); of them matched on no "
        r"side: (\d+)$",
        D.kq[3],
    )
    if (
        int(never.group(1)) != distinct
        or distinct - int(never.group(2)) != len(one_side)
        or sum(by_vid.values()) + absent + len(one_side) != distinct
        or set(by_vid) != {sam_vid, dan_vid}
    ):
        raise ValueError("the unmatched words are not as described")
    one_side_refs = [ref(v) for v in one_side]
    if len(one_side) == 2 and one_side[0].split(".")[0] == one_side[1].split(".")[0]:
        one_side_refs = [
            ref(one_side[0]),
            "%s:%s" % tuple(one_side[1].split(".")[1:]),
        ]
    out.append(
        P(
            "Of the %s morphhb words that no MAM atom matches (%s, section 8), %s are in "
            "%s, which MAM lacks, %s %s %s's, %s %s %s's artifact, and %s (%s) %s matched "
            "on one side only."
            % (
                fmt(distinct),
                outf("20-coverage.txt"),
                fmt(absent),
                ref_range(absent_vids),
                num(by_vid[sam_vid]),
                "is" if by_vid[sam_vid] == 1 else "are",
                ref(sam_vid),
                num(by_vid[dan_vid]),
                "is" if by_vid[dan_vid] == 1 else "are",
                ref(dan_vid),
                num(len(one_side)),
                " and ".join(one_side_refs),
                "is" if len(one_side) == 1 else "are",
            )
        )
    )
    return out


def sec_hidden(D):
    r2 = D.ref[2]
    hidden = count_lines(r2)
    qatan_n = hidden.pop("qamats->qamats-qatan")
    perf_n = hidden.pop(
        "qamats qatan where morphhb's morph part is a perfect or participle"
    )
    if hidden:
        raise ValueError("other hidden differences: %r" % hidden)
    start = r2.index(
        "  qamats qatan in MAM, qamats in morphhb, by the morph part of the piece "
        "holding it:"
    )
    parts = collections.OrderedDict()
    for line in r2[start + 1 :]:
        m = re.match(r"^    (\S+)\s+(\d+)$", line)
        if m:
            parts[m.group(1)] = int(m.group(2))
    perf = {
        p: n for p, n in parts.items() if p[0] == "V" and len(p) == 3 and p[2] in "pqr"
    }
    if sum(perf.values()) != perf_n:
        raise ValueError("the perfect and participle parts disagree")
    hophal = sum(n for p, n in perf.items() if p[1] == "H")
    pual = sum(n for p, n in perf.items() if p[1] == "P")
    top = sorted(parts.items(), key=lambda kv: -kv[1])[:5]
    listed = D.lists["qatan with a perfect or participle morph"]
    lists_len = ast.literal_eval(
        match_one(r"^== 4\. Lists in 23-lists\.json: (\{.*\})$", D.ref[4]).group(1)
    )
    if lists_len["qatan with a perfect or participle morph"] != len(listed):
        raise ValueError("the qamats qatan list disagrees")
    out = ['<h3 id="hidden">What the vowel key could hide</h3>']
    out.append(
        P(
            "The vowel key reads a qamats qatan as a qamats, so it counts %s atoms as the "
            "same form although MAM's has a qamats qatan where morphhb's has a qamats (%s, "
            "section 2); its other fold, of ḥolam ḥaser into ḥolam, hides no difference. "
            "Almost all of these qamats qatan vowels are where one is expected: %s. In %s "
            "of them the piece's morph is a perfect or a participle; the first %s are "
            "listed in %s, “qatan with a perfect or participle morph”, and shown in %s. "
            "Most of these, among them %s Hophal and %s Pual forms, are forms that have a "
            "qamats qatan, but in Claude's first reading %s look like real differences. "
            "These %s belong in the review queue, although the vowel key counts them as "
            "the same form."
            % (
                fmt(qatan_n),
                outf("22-refine.txt"),
                and_list("%s on %s" % (fmt(n), PART_GLOSS[p]) for p, n in top),
                fmt(perf_n),
                fmt(len(listed)),
                outf("23-lists.json"),
                outf("28-show-qatan.txt"),
                fmt(hophal),
                fmt(pual),
                num(len(QATAN)),
                num(len(QATAN)),
            )
        )
    )
    rows = []
    for vid, wid, reading in QATAN:
        rec = find(D.recs, vid, wid)
        if rec["class"] != "A1" or not rec["w"]["morph"].endswith("Vqp3fs"):
            raise ValueError("%s %s is not as described" % (vid, wid))
        rows.append(pair_row(rec, reading, cons=False))
    out.append(
        table(
            "The %s qamats qatan cases that Claude's first reading counts as real "
            "differences." % num(len(QATAN)),
            FORM_HEADERS + ["what differs", "Claude's first reading"],
            rows,
        )
    )
    s5 = {}
    for line in D.ref[5][1:]:
        m = re.match(r"^  (\S.*?)\s{2,}(\d+)$", line)
        if m:
            s5[m.group(1)] = int(m.group(2))
    out.append(
        P(
            "The vowel key ignores the accents too, and the place of an accent can mark "
            "the stressed syllable, which can tell two analyses apart. A screen over the "
            "atoms of the same form in which each text has exactly one accent that marks "
            "the stress found %s where that accent is on a different letter in morphhb's "
            "form than in MAM's (%s, section 5; listed in %s). In Claude's first reading "
            "of the %s whose morph has a verb, none needs a different analysis."
            % (
                fmt(s5["differ"]),
                outf("22-refine.txt"),
                outf("28-show-stress.txt"),
                fmt(s5["differ, morph has a verb"]),
            )
        )
    )
    return out


def sec_nine(D):
    rows, tiers = [], collections.Counter()
    for vid, wid, cls, cons in D.nine:
        rec = find(D.recs, vid, wid)
        if rec["class"] != cls or rec["cons"] != cons:
            raise ValueError("%s %s disagrees with 22-refine.txt" % (vid, wid))
        tier = FG.tier(rec)
        tiers[tier] += 1
        rows.append(pair_row(rec, tier_note(rec), cons=False))
    fits = tiers["supported"] + tiers["untested"]
    if fits + tiers["flagged"] != len(D.nine):
        raise ValueError("the nine corrections fall outside three tiers")
    for vid, wid, _cls, cons in D.nine:
        if FG.tier(find(D.recs, vid, wid)) == "flagged" and not cons["lemma"]:
            raise ValueError("%s: a flagged correction whose lemma does not fit" % vid)
    out = [
        '<h3 id="nine">The %s corrections of the 2026-11-13 study</h3>'
        % num(len(D.nine))
    ]
    out.append(
        P(
            "The 2026-11-13 study found %s words where morphhb's lemma or morph already "
            "fits MAM's form rather than morphhb's own (%s, section 3). Of them, %s land "
            "in “supported” or “untested”, because morphhb's analysis already fits MAM's "
            "form, and %s are flagged, because only one of the lemma and the morph fits "
            "it, in each of them the lemma: morphhb gives MAM's form this lemma "
            "elsewhere, but never together with this morph."
            % (
                num(len(D.nine)),
                outf("22-refine.txt"),
                num(fits),
                num(tiers["flagged"]),
            )
        )
    )
    out.append(
        table(
            "The %s corrections and their tiers." % num(len(D.nine)),
            FORM_HEADERS + ["what differs", "tier"],
            rows,
        )
    )
    return out


def sec_slashes(D):
    F = D.F
    sl = F["slashes"]
    if (
        sl["slash not directly before a letter"]
        or sl["morph parts differ from text pieces"]
    ):
        raise ValueError("the slash figures are not as described")
    c10 = collections.defaultdict(dict)
    for line in D.cov[10][1:]:
        m = re.match(r"^  (A1|A2|B|K)\s+(\S.*?)\s+(\d+)$", line)
        if m:
            c10[m.group(1)][m.group(2)] = int(m.group(3))
    b = c10["B"]
    k4 = count_lines(D.kq[4])
    if (
        b["slashes"] != sl["slashes"] - sl["letters-equal slashes"]
        or b["slashes placed"]
        != sl["slashes placed by letter count or letter alignment"]
        - sl["letters-equal slashes"]
        or b["words with an unplaced slash"]
        != k4["words placed by the fallback rule"] + k4["words still ambiguous"]
        or b["with slashes"]
        != k4["words placed by align.py"] + b["words with an unplaced slash"]
    ):
        raise ValueError("the slash figures disagree")
    out = ['<h2 id="slashes">4. Morpheme division</h2>']
    out.append(
        P(
            "morphhb divides a word into its morphemes with slashes, as between a prefix "
            "and the rest of the word, and its morph has one part for each piece between "
            "them. Carrying morphhb's analysis over means carrying its slashes into MAM's "
            "atom. Every one of morphhb's slashes stands directly before a letter, so in "
            "a pair whose letters are equal a slash goes before the same letter of MAM's "
            "atom, counted from its start: %s slashes in %s words (%s). In all %s matched "
            "words the morph has exactly one part for each piece."
            % (
                fmt(sl["letters-equal slashes"]),
                fmt(sl["letters-equal words with a slash"]),
                outf("30-figures.json"),
                fmt(sl["words"]),
            )
        )
    )
    out.append(
        P(
            "In the spelling pairs (class B) the letters themselves differ, so a slash is "
            "placed by aligning the two words' letters: %s of their %s slashes are placed "
            "that way (%s, section 10). Of the %s words left with a slash unplaced, a "
            "fallback rule, which puts a slash next to the one letter beside it that "
            "aligns, places %s, and %s stay ambiguous (%s, section 4)."
            % (
                fmt(b["slashes placed"]),
                fmt(b["slashes"]),
                outf("20-coverage.txt"),
                fmt(b["words with an unplaced slash"]),
                fmt(k4["words placed by the fallback rule"]),
                fmt(k4["words still ambiguous"]),
                outf("26-kq-ids-slashes.txt"),
            )
        )
    )
    rows = []
    a1 = find(D.recs, D.slash_a1["vid"], D.slash_a1["id"])
    parts = a1["w"]["morph"][1:].split("/")
    if (
        a1["class"] != "A1"
        or a1["slash"]["n"] < 2
        or "Rd" not in [p[:2] for p in parts]
    ):
        raise ValueError("the letters-equal slash example is not as described")
    rows.append(
        form_row(
            ["MAM", "morphhb", "MAM, with morphhb's slashes"],
            [mam_form(a1), w_form(a1["w"]), a1["slash"]["mam"]],
            a1["vid"],
            analysis(a1["w"]),
            [
                "The letters are equal, so each slash goes before the same letter of "
                "MAM's atom. The middle piece's morph part, Rd, is a preposition with "
                "the article, which has no letter of its own here."
            ],
        )
    )
    bb = find(D.recs, D.slash_b["vid"], D.slash_b["id"])
    if bb["slash"]["mapped"] != bb["slash"]["n"]:
        raise ValueError("the aligned slash example is not placed")
    rows.append(
        form_row(
            ["MAM", "morphhb", "MAM, with morphhb's slashes"],
            [mam_form(bb), w_form(bb["w"]), bb["slash"]["mam"]],
            bb["vid"],
            analysis(bb["w"]),
            [describe(bb) + " The slash is placed by aligning the two words' letters."],
        )
    )
    for entry, kind in ((D.fallback, "fallback"), (D.ambiguous, "ambiguous")):
        hits = [
            r
            for r in D.recs[entry["vid"]]
            if r["class"] == "B" and r["w"]["text"] == entry["morphhb"]
        ]
        if len(hits) != 1:
            raise ValueError("%s: %d records" % (entry["vid"], len(hits)))
        rec = hits[0]
        wl, ml = C.letters(rec["w"]["text"]), C.letters(rec["text"])
        amap = letter_map(wl, ml)
        pos, _ok = AL.slash_positions(rec["w"]["text"])
        unplaced = [
            i
            for i, p in enumerate(pos)
            if not (
                amap.get(p - 1) is not None
                and amap.get(p) is not None
                and amap[p] == amap[p - 1] + 1
            )
        ]
        if len(unplaced) != 1:
            raise ValueError("%s: %d unplaced slashes" % (entry["vid"], len(unplaced)))
        i = unplaced[0]
        p = pos[i]
        nth = ORDINALS[i] + " " if len(pos) > 1 else ""
        if kind == "fallback":
            if amap.get(p - 1) is None and amap.get(p) is not None:
                how = (
                    "The letter before morphhb's %sslash has no counterpart in MAM's "
                    "atom, so the fallback rule places that slash before the letter "
                    "after it." % nth
                )
            elif amap.get(p) is None and amap.get(p - 1) is not None:
                how = (
                    "The letter after morphhb's %sslash has no counterpart in MAM's "
                    "atom, so the fallback rule places that slash after the letter "
                    "before it." % nth
                )
            else:
                raise ValueError("%s: not a fallback case" % entry["vid"])
            forms = [mam_form(rec), w_form(rec["w"]), entry["mam"]]
            labels = ["MAM", "morphhb", "MAM, with morphhb's slashes"]
        else:
            if not (
                amap.get(p - 1) is not None
                and amap.get(p) is not None
                and amap[p] - amap[p - 1] == 2
            ):
                raise ValueError("%s: not one letter at the slash" % entry["vid"])
            how = (
                "That letter stands where morphhb's %sslash is, so the slash could go "
                "before it or after it." % nth
            )
            forms = [mam_form(rec), w_form(rec["w"])]
            labels = ["MAM", "morphhb"]
        rows.append(
            form_row(
                labels,
                forms,
                rec["vid"],
                analysis(rec["w"]),
                [describe(rec) + " " + how],
            )
        )
    out.append(
        table(
            "Slashes carried into MAM's atoms: by letter count, by aligning letters, by "
            "the fallback rule, and a case that stays ambiguous. The last two are the "
            "first such words in %s." % outf("27-kq-ids-slashes.json"),
            FORM_HEADERS + ["how the slashes are placed"],
            rows,
        )
    )
    rd = F["rd_words_by_class"]
    flagged_rd = [
        x
        for x in D.lists["A2 contradicted"] + D.lists["B contradicted"]
        if "Rd" in [p[:2] for p in x["morph"][1:].split("/")]
    ]
    chr_vid, chr_id, _r = FLAGGED[2]
    chr_rec = find(D.recs, chr_vid, chr_id)
    if flagged_rd or "Rd" not in chr_rec["cons"]["top"][0]:
        raise ValueError("the Rd statement does not hold")
    out.append(
        P(
            "One morph part needs no letter at all. Rd, a preposition with the article, "
            "marks a piece such as the middle one of %s's atom above, whose article "
            "has no letter of its own: its he is not written, and only the vowel under "
            "the preposition shows it. Since the part needs no letter, it travels with "
            "its piece. morphhb's morph has an Rd in %s of MAM's matched atoms: %s of the "
            "same form (A1), %s ketiv atoms, %s that differ in pointing and %s in "
            "spelling. None of the flagged atoms has an Rd in morphhb's morph. In "
            "Claude's first reading, the one flagged atom where an Rd is at issue is %s, "
            "shown among the flagged atoms above, where MAM's vowel calls for the Rd "
            "that morphhb's morph lacks."
            % (
                ref(a1["vid"]),
                fmt(sum(rd.values())),
                fmt(rd["A1"]),
                fmt(rd["K"]),
                fmt(rd["A2"]),
                fmt(rd["B"]),
                ref(chr_vid),
            )
        )
    )
    return out


def sec_markup(D, frag):
    F = D.F
    out = ['<h2 id="markup">5. MAM\'s markup</h2>']

    # Ketiv and qere.
    partners = ast.literal_eval(
        match_one(r"^  morphhb partner kinds: (\{.*\})$", D.cov[3]).group(1)
    )
    if partners["x-ketiv"] != F["tier_by_class"]["same/K"]:
        raise ValueError("the ketiv figures disagree")
    one = collections.Counter()
    letters = collections.Counter()
    for label, n in count_lines(D.kq[1]).items():
        parts = label.split("; ")
        kind, how = ONE_FORM_KINDS[parts[0]], ONE_FORM_ANALYSES[parts[1]]
        if len(parts) == 3:
            letters[ONE_FORM_LETTERS[parts[2]]] += n
        elif len(parts) != 2 or parts[1] != "several ketiv or qere words":
            raise ValueError("unexpected one-form line %r" % label)
        one[(kind, how)] += n
    pairs_n = sum(letters.values())
    out.append('<h3 id="kq">Ketiv and qere</h3>')
    out.append(
        P(
            "MAM's ketiv is unpointed, as morphhb's is, so a ketiv is compared by its "
            "letters: %s of MAM's ketiv atoms have the letters of morphhb's ketiv and take "
            "its analysis as it stands (%s, section 3)."
            % (fmt(partners["x-ketiv"]), outf("20-coverage.txt"))
        )
    )
    out.append(
        P(
            "Where MAM has one form and morphhb has a ketiv and a qere, MAM's form "
            "needs one analysis, which morphhb's ketiv and qere may not share. MAM's one "
            "form is of %s kinds: a trivial ketiv and qere (MAM-simple's "
            "<code>kq-trivial</code>), or a plain atom. In the %s cases with one ketiv "
            "and one qere in morphhb, MAM's form has the ketiv's letters in %s (%s, "
            "section 1)."
            % (
                num(len(ONE_FORM_KINDS)),
                fmt(pairs_n),
                fmt(letters["ketiv"]),
                outf("26-kq-ids-slashes.txt"),
            )
        )
    )
    cols = list(ONE_FORM_ANALYSES.values())
    rows = []
    for kind in ONE_FORM_KINDS.values():
        vals = [one[(kind, c)] for c in cols]
        rows.append(num_row(kind, *vals, sum(vals)))
    out.append(
        table(
            "MAM's one form against morphhb's ketiv and qere. Each column after the first "
            "says what morphhb's ketiv and qere have (%s, section 1)."
            % outf("26-kq-ids-slashes.txt"),
            ["MAM's one form is"] + cols + ["all"],
            rows,
            cls="data",
        )
    )
    rows = []
    g = [r for r in D.recs[KQ_VID] if r["class"] == "C" and "kq-trivial" in r["kinds"]]
    s = [r for r in D.recs[ONE_FORM_VID] if r["class"] == "C"]
    if len(g) != 1 or len(s) != 1 or "plain" not in s[0]["kinds"]:
        raise ValueError("the one-form examples are not as described")
    for rec, agree in ((g[0], True), (s[0], False)):
        (k,) = rec["ws"]["k"]
        (q,) = rec["ws"]["q"]
        if k["type"] != "x-ketiv" or not q["in_qere"]:
            raise ValueError("%s: not a ketiv and a qere" % rec["vid"])
        if C.letters(rec["text"]) != C.letters(k["text"]):
            raise ValueError("%s: MAM's letters are not the ketiv's" % rec["vid"])
        same = (k["lemma"], k["morph"]) == (q["lemma"], q["morph"])
        if same != agree:
            raise ValueError("%s: the analyses are not as described" % rec["vid"])
        if agree:
            note = (
                "MAM has one form, a trivial ketiv and qere, with the ketiv's letters; "
                "morphhb's ketiv and qere have the same lemma and morph, which therefore "
                "fit MAM's form."
            )
        else:
            diff = [i for i, (a, b) in enumerate(zip(k["morph"], q["morph"])) if a != b]
            if (
                k["lemma"] != q["lemma"]
                or len(k["morph"]) != len(q["morph"])
                or len(diff) != 1
                or (k["morph"][diff[0]], q["morph"][diff[0]]) != ("s", "p")
            ):
                raise ValueError("%s: the morphs are not as described" % rec["vid"])
            note = (
                "MAM has one form, a plain atom, with the ketiv's letters; morphhb's "
                "ketiv and qere have the same lemma but different morphs, singular in the "
                "ketiv and plural in the qere, so MAM's form needs a choice between them."
            )
        rows.append(
            form_row(
                ["MAM", "morphhb's ketiv", "morphhb's qere"],
                [mam_form(rec), w_form(k), w_form(q)],
                rec["vid"],
                "<br>".join((analysis_line(k, "ketiv"), analysis_line(q, "qere"))),
                [note],
            )
        )
    kp = D.kq_plain
    kq_recs = [r for r in D.recs[kp["vid"]] if r.get("w", {}).get("id") == kp["k"][3]]
    kq_recs.sort(key=lambda r: r["on"])
    if [r["on"] for r in kq_recs] != ["k", "q"] or C.letters(kq_recs[0]["text"]) != (
        C.letters(kq_recs[0]["w"]["text"])
    ):
        raise ValueError("the ketiv and qere against one word is not as described")
    rows.append(
        form_row(
            ["MAM's ketiv", "MAM's qere", "morphhb"],
            [mam_form(kq_recs[0]), mam_form(kq_recs[1]), w_form(kq_recs[0]["w"])],
            kp["vid"],
            analysis(kq_recs[0]["w"]),
            [
                "MAM has a ketiv and a qere where morphhb has one word, with the ketiv's "
                "letters; both of MAM's atoms meet that one word."
            ],
        )
    )
    k2 = count_lines(D.kq[2])
    verses = int(match_one(r"^  verses: (\d+)$", D.kq[2]).group(1))
    ketiv_n = sum(n for label, n in k2.items() if label.startswith("MAM ketiv atoms"))
    qere_n = sum(n for label, n in k2.items() if label.startswith("MAM qere atoms"))
    if ketiv_n + qere_n != sum(k2.values()):
        raise ValueError("unexpected lines in 26-kq-ids-slashes.txt section 2")
    out.append(
        table(
            "MAM's one form against morphhb's ketiv and qere, and MAM's ketiv and qere "
            "against morphhb's one word. The ketiv atoms are unpointed in both texts.",
            FORM_HEADERS + ["what differs"],
            rows,
        )
    )
    out.append(
        P(
            "The reverse occurs too: in %s verses MAM has a ketiv and a qere where "
            "morphhb has one plain word, and there %s of MAM's ketiv atoms and %s of its "
            "qere atoms meet morphhb's one word (%s, section 2)."
            % (fmt(verses), fmt(ketiv_n), fmt(qere_n), outf("26-kq-ids-slashes.txt"))
        )
    )

    # Maqaf.
    rows = []
    for key, n in F["maqaf"].items():
        m = re.fullmatch(r"MAM (.+) / morphhb (.+)", key)
        rows.append(
            '<tr><td>%s</td><td>%s</td><td class="num">%s</td></tr>'
            % (MAQAF_KINDS[m.group(1)], MAQAF_KINDS[m.group(2)], fmt(n))
        )
    out.append('<h3 id="maqaf">Maqaf</h3>')
    out.append(
        P(
            "MAM and morphhb mostly agree in their maqaf marks. The table counts the atoms "
            "that are on both sides of a verse and have one plain morphhb word as their "
            "partner. The analyses do not depend on the maqaf, because both texts' unit "
            "is the atom: a maqaf joins two atoms into one chanted word, and each atom "
            "keeps its own morphhb word."
        )
    )
    out.append(
        table(
            "What follows MAM's atom and its morphhb word (%s). MAM-simple marks a "
            "maqaf “implicit in the manuscript”, in its documentation's words, with an "
            "element of its own." % outf("30-figures.json"),
            ["after MAM's atom", "after morphhb's word", "atoms"],
            rows,
            cls="data",
        )
    )

    # Dual cantillation.
    st, n_verses = {}, None
    for line in D.strands_lines[1:]:
        if line.startswith("  ") or not line.strip():
            continue
        m = re.match(r"^(.*?):?\s+(\d+)$", line)
        if not m:
            raise ValueError("unparsed line %r" % line)
        st[m.group(1)] = int(m.group(2))
    n_verses = st.pop("verses with a dual cantillation")
    for absent in (
        "atoms whose letters differ between strands",
        "atoms matched to different morphhb words in different strands",
        "verses whose strands differ in atom count",
    ):
        if st.get(absent):
            raise ValueError("25-strands.txt: %s" % absent)
    if st["verses compared"] != n_verses:
        raise ValueError("not every verse was compared")
    cm = match_one(r"^verses with a dual cantillation: (\d+): (.+)$", D.census)
    cant_vids = cm.group(2).split()
    if int(cm.group(1)) != n_verses or len(cant_vids) != n_verses:
        raise ValueError("the dual-cantillation verses disagree")
    gen = [v for v in cant_vids if v.startswith("Gen.")]
    chapters = []
    for v in cant_vids:
        b, c, _v = v.split(".")
        if b != "Gen" and (b, c) not in chapters:
            chapters.append((b, c))
    if len(gen) != 1 or len(chapters) != 2:
        raise ValueError("the dual-cantillation verses are not as described")
    strand_names = {
        m.group(1) for m in (re.fullmatch(r"class \S+ in (\S+)", k) for k in st) if m
    }
    if strand_names != set(STRANDS):
        raise ValueError("25-strands.txt's strands are not MAM-simple's three")
    n_strands = num(len(STRANDS))
    out.append('<h3 id="strands">Dual cantillation</h3>')
    out.append(
        P(
            "MAM-simple gives the %s verses with a dual cantillation, %s and the "
            "Decalogues of %s and %s, in %s strands: <code>%s</code>, which has both "
            "cantillations, and <code>%s</code> and <code>%s</code>, which have one each "
            "(MAM-simple's names). The alignment was run on each strand (%s). In all %s "
            "atoms of those verses the %s strands have identical letters and meet the "
            "same morphhb word. Between the strands, %s atoms differ in their vowels and "
            "%s in the maqaf after them, and %s fall in a different class in one strand "
            "than in another; so morphhb's analysis is carried over once for all %s "
            "strands, and only an atom's tier can depend on its strand."
            % (
                fmt(n_verses),
                ref(gen[0]),
                "%s%s%s" % (BOOK_NAMES[chapters[0][0]], NBSP, chapters[0][1]),
                "%s%s%s" % (BOOK_NAMES[chapters[1][0]], NBSP, chapters[1][1]),
                n_strands,
                *STRANDS,
                outf("25-strands.txt"),
                fmt(st["atoms compared"]),
                n_strands,
                fmt(st["atoms whose vowel key differs between strands"]),
                fmt(st["atoms whose maqaf after differs between strands"]),
                fmt(st["atoms whose class differs between strands"]),
                n_strands,
            )
        )
    )
    last = {}
    for strand in STRANDS:
        recs = D.strand_recs[strand]
        last[strand] = max(recs, key=lambda r: r["j"]["k"])
    ids = {last[s]["w"]["id"] for s in STRANDS}
    if (
        len(ids) != 1
        or len({C.letters(last[s]["text"]) for s in STRANDS}) != 1
        or {last[s]["class"] for s in STRANDS} != {"A2"}
        or len({AL.vkey(last[s]["text"]) for s in STRANDS}) != len(STRANDS)
    ):
        raise ValueError("Exodus 20:3's last atom is not as described")
    w = last[STRANDS[0]]["w"]
    by = collections.OrderedDict()
    for s in STRANDS:
        by.setdefault(FG.tier(last[s]), []).append("<code>%s</code>" % s)
    tiers_note = "; ".join(
        "in %s the atom is %s" % (" and ".join(names), TIER_NAMES[t])
        for t, names in by.items()
    )
    out.append(
        table(
            "%s's last atom in MAM's %s strands (%s) and in morphhb."
            % (
                ref(STRAND_VID),
                n_strands,
                and_list(code(D.work_shown + ATOM_FILES[s]) for s in STRANDS),
            ),
            FORM_HEADERS + ["what differs"],
            [
                form_row(
                    ["MAM, <code>%s</code>" % s for s in STRANDS] + ["morphhb"],
                    [mam_form(last[s]) for s in STRANDS] + [w_form(w)],
                    STRAND_VID,
                    analysis(w),
                    [
                        "The %s strands' letters are morphhb's, and each strand's atom "
                        "meets morphhb's one word; each differs from morphhb's form in "
                        "its vowels, and they differ from one another. %s."
                        % (n_strands, tiers_note[0].upper() + tiers_note[1:])
                    ],
                )
            ],
        )
    )

    # Closed dispatch.
    boundary = int(
        match_one(r"^boundary added after \(k\)\s+(\d+)$", D.census).group(1)
    )
    (bk,) = [r for r in D.recs[BOUNDARY_VID] if r.get("boundary_added")]
    if bk["class"] != "K" or not bk["w"]["maqaf_after"]:
        raise ValueError("Numbers 23:13 is not as described")
    items = [
        "%s ketiv atoms that MAM-simple writes straight before the next atom, with no "
        "separator, where the qere ends in a maqaf, for example %s; the reader ends the "
        "ketiv atom there and flags it (%s);"
        % (fmt(boundary), ref(BOUNDARY_VID), outf("01-mam-census.txt")),
        "an empty target of a scroll-difference note at %s, a note about a place rather "
        "than a word;" % ref(EMPTY_TARGET_VID),
        "a legarmeh inside an atom with a large letter at %s, which the reader keeps "
        "with that atom." % ref(LEGARMEH_VID),
    ]
    out.append('<h3 id="dispatch">Closed dispatch</h3>')
    out.append(
        P(
            "MAM-simple's reader, %s, handles each of MAM-simple's element types by name "
            "and stops with an error on any other, so that nothing in MAM's markup is "
            "skipped unnoticed. It found %s things that a generator would have to handle:"
            % (code("py/morphhb_on_mam/mam_reader.py"), num(len(items)))
        )
    )
    out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % item for item in items))
    out.append(frag.get("generator-dispatch", '<p class="pending">%s</p>' % PENDING))
    return out


def fragment_part(frag, anchor, heading):
    if anchor in frag:
        part = frag[anchor]
        return [part] if "<h2" in part else ["<h2>%s</h2>" % heading, part]
    return [
        '<section id="%s"><h2>%s</h2><p class="pending">%s</p></section>'
        % (anchor, heading, PENDING)
    ]


def sec_not_established(D):
    t = D.F["tiers"]
    return [
        '<h2 id="not-established">8. What this study could not establish</h2>',
        "<ul>"
        "<li>Whether the analyses of the %s untested atoms fit MAM's forms: morphhb has "
        "no other occurrence of those forms to test them against.</li>"
        "<li>Whether each flagged atom is a real change: the judgments on this page are "
        "Claude's first reading only.</li>"
        "<li>Analyses that turn on an accent, beyond the stress screen of section 3.</li>"
        "<li>Anything about the Leningrad Codex itself: the comparison is of two "
        "transcriptions, and no image of the manuscript was consulted.</li>"
        "<li>Whether morphhb's maintainers want an analysed MAPM, the copy of MAM's text "
        "in morphhb's <code>MAPM/</code> folder: the only evidence is documentary.</li>"
        "<li>MACULA Hebrew's syntax and senses, which ride on the same ids: they were not "
        "studied.</li>"
        "<li>The hours that a person's review of the queue would take.</li>"
        "</ul>" % fmt(t["untested"]),
    ]


def sec_files():
    return [
        '<h2 id="files">9. Files</h2>',
        P(
            "The record folder's %s maps the study's inputs, scripts and outputs, among them the "
            "outputs that this page reads; %s builds this page from them, and the page's "
            "visible text is in %s."
            % (
                link("../README.md", code(RECORD_SHOWN + "README.md")),
                code("py/morphhb_on_mam/build_page.py"),
                outf("40-page-text.txt"),
            )
        ),
    ]


def fragment_sections():
    """{id: verbatim <section> element} from page-fragment.html."""
    if not FRAGMENT.exists():
        warn("%s is missing; pending: %s" % (FRAGMENT.name, ", ".join(FRAGMENT_IDS)))
        return {}
    text = FRAGMENT.read_text(encoding="utf-8")
    found = {}
    for m in re.finditer(r"<section\b[^>]*>", text):
        idm = re.search(r'\bid="([^"]+)"', m.group())
        if not idm or idm.group(1) not in FRAGMENT_IDS:
            continue
        depth = 0
        for tag in re.finditer(r"<section\b[^>]*>|</section\s*>", text[m.start() :]):
            depth += 1 if tag.group().startswith("<section") else -1
            if depth == 0:
                end = m.start() + tag.end()
                break
        else:
            raise ValueError(
                "%s: section %s is not closed" % (FRAGMENT.name, idm.group(1))
            )
        if idm.group(1) in found:
            raise ValueError("%s: two sections %s" % (FRAGMENT.name, idm.group(1)))
        found[idm.group(1)] = text[m.start() : end]
    for anchor in FRAGMENT_IDS:
        if anchor not in found:
            warn("%s has no section %s; pending" % (FRAGMENT.name, anchor))
    return found


def build(D):
    frag = fragment_sections()
    if any(C.HEB_LETTER.search(part) for part in frag.values()):
        warn(
            "%s has Hebrew letters, which section 2's statement that this script "
            "copied every Hebrew form from the outputs does not cover" % FRAGMENT.name
        )
    parts = sec_head(D)
    parts += sec_nav(frag)
    parts += sec_answer(D)
    parts += sec_method(D)
    parts += sec_coverage(D)
    parts += sec_slashes(D)
    parts += sec_markup(D, frag)
    for anchor, heading in FRAGMENT_HEADINGS.items():
        parts += fragment_part(frag, anchor, heading)
    parts += sec_not_established(D)
    parts += sec_files()
    parts += ["</body>", "</html>"]
    return "\n".join(parts) + "\n"


def write_page(work_dir):
    """Write the page and its visible text from the outputs and the work directory."""
    D = load(Path(work_dir))
    page = build(D)
    PAGE.write_text(page, encoding="utf-8", newline="\n")
    TEXT.write_text(page_text.visible_text(page), encoding="utf-8", newline="\n")
    print("wrote %s and %s" % (record_paths.shown(PAGE), record_paths.shown(TEXT)))
