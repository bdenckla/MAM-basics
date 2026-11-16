"""Check the study's page against its outputs and the page rules.

Written by Claude (Opus 5.5) on 2026-11-15 for morphhb-on-mam.html, which build_page.py
writes, and moved into this package on 2026-11-16, when the study was put on ice
(morphhb-on-mam/README.md).  check(work_dir) reads the page, its visible text
(40-page-text.txt), the outputs beside them and the work directory's records, computes its
expectations afresh from them, prints what it checked and every problem it found, and
returns the problems; py/main_morphhb_on_mam.py page exits non-zero on any.

1. Every number in the visible text is a figure of 30-figures.json, of a breakdown file,
   of an example list or of morphhb-on-mam/README.md, a figure of a record shown on the
   page, or a sum, difference or share computed here from those.  The parts spliced in from
   in/page-fragment.html, which the study's root session wrote from the research reports,
   are checked against those reports and research/CHECKED.md as well.  References are left
   out: dates, years, verses, versions, file names, codes in backticks, section numbers and
   list numbers.
2. The headline figures appear as in/page-spec.md states them, computed here from
   out/30-figures.json and the breakdown files.
3. Every pointed Hebrew run is inside lang="hbo"; an unpointed run is inside lang="hbo" in a
   stack of compared forms, or in a <bdi> without lang; no Hebrew is inside a link; every
   table cell holding Hebrew has dir="rtl".
4. No English block or sentence begins with a Hebrew letter.
5. The page's head and caveat are as in/page-spec.md says; build_page.py holds no Hebrew
   character and no decomposed letter with a dot below; the files have LF line endings.
"""

import collections
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

from morphhb_on_mam import page_text
from morphhb_on_mam import record_paths

HERE = Path(__file__).resolve().parent
OUT = record_paths.out_dir()
PAGE = record_paths.page_path()
TEXT = record_paths.page_text_path()
FRAGMENT = record_paths.fragment_path()
README = record_paths.readme_path()
RESEARCH = [
    record_paths.research_dir() / "upstream" / "FINDINGS.md",
    record_paths.research_dir() / "upkeep-shape" / "FINDINGS.md",
    record_paths.research_dir() / "CHECKED.md",
]

BREAKDOWNS = [
    "01-mam-census.txt",
    "12-align-summary.txt",
    "20-coverage.txt",
    "22-refine.txt",
    "25-strands.txt",
    "26-kq-ids-slashes.txt",
]
EXAMPLE_LISTS = ["21-examples.json", "23-lists.json", "27-kq-ids-slashes.json"]
HEB_LETTER = re.compile("[\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
HEB_ANY = re.compile("[\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW LETTER TAV}]")
NOT_POINTS = {
    "\N{HEBREW PUNCTUATION MAQAF}",
    "\N{HEBREW PUNCTUATION PASEQ}",
    "\N{HEBREW PUNCTUATION SOF PASUQ}",
    "\N{HEBREW PUNCTUATION NUN HAFUKHA}",
}

PROBLEMS = []


def problem(msg):
    PROBLEMS.append(msg)


def numbers_in(text):
    """Every number written in a text, as a value: '306,525' and '99.64' included."""
    out = set()
    for m in re.finditer(r"\d[\d,]*(?:\.\d+)?", text):
        tok = m.group().rstrip(",")
        for piece in [tok] + tok.split(","):
            try:
                out.add(float(piece.replace(",", "")))
            except ValueError:
                pass
    return out


def walk(obj, out):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            walk(v, out)


def section(name, n):
    lines, cur = [], None
    for line in (OUT / name).read_text(encoding="utf-8").splitlines():
        m = re.match(r"== (\d+)\. ", line)
        if m:
            cur = int(m.group(1))
        if cur == n:
            lines.append(line)
    return lines


def counts(lines):
    out = {}
    for line in lines:
        m = re.match(r"^ +(\d+)  (\S.*)$", line)
        if m:
            out[m.group(2)] = int(m.group(1))
    return out


def derived(F):
    """Sums, differences and shares that the page states, computed here."""
    t, tbc = F["tiers"], F["tier_by_class"]
    total = F["mam_atoms"]
    good = t["same"] + t["supported"]
    rest = t["untested"] + t["flagged"] + t["structural"]
    d = {
        "same + supported, share": round(100.0 * good / total, 2),
        "untested + flagged + structural": rest,
        "untested + flagged + structural, share": round(100.0 * rest / total, 2),
        "flagged + structural": t["flagged"] + t["structural"],
        "Tetragrammaton bare + prefixed": F["a2_holam_only"]["bare"]
        + F["a2_holam_only"]["prefixed"],
        "holam only, all": sum(F["a2_holam_only"].values()),
        "B, all": sum(F["b_by_letters"].values()),
        "Rd, all": sum(F["rd_words_by_class"].values()),
    }
    # The spelling pairs' flagged atoms by kind (out/20-coverage.txt, section 6).
    kind = None
    flagged = collections.Counter()
    for line in section("20-coverage.txt", 6):
        m = re.match(r"^( +)(\d+)  (\S.*)$", line)
        if not m:
            continue
        if len(m.group(1)) + len(m.group(2)) == 8:
            kind = m.group(3)
        elif m.group(3).startswith("contradicted"):
            flagged[kind] += int(m.group(2))
    for k, n in flagged.items():
        d["B flagged, " + k] = n
    # The xolam-only atoms by tier (section 2).
    kind, holam = None, collections.Counter()
    for line in section("20-coverage.txt", 2):
        m = re.match(r"^( +)(\d+)  (\S.*)$", line)
        if not m:
            continue
        if len(m.group(1)) + len(m.group(2)) == 8:
            kind = m.group(3)
        elif len(m.group(1)) + len(m.group(2)) == 16 and kind.startswith(
            "holam in MAM"
        ):
            holam[m.group(3).split(":")[0]] += int(m.group(2))
    for k, n in holam.items():
        d["holam only, " + k] = n
    # MAM's one form against morphhb's ketiv and qere (26-, section 1).
    one = collections.Counter()
    for label, n in counts(section("26-kq-ids-slashes.txt", 1)).items():
        parts = label.split("; ")
        one["kind " + parts[0]] += n
        one["analyses " + parts[1]] += n
        one[parts[0] + " / " + parts[1]] += n
        if len(parts) == 3:
            one["one ketiv and one qere"] += n
            one["letters " + parts[2]] += n
    for k, n in one.items():
        d["one form, " + k] = n
    # MAM's ketiv and qere against one plain word (section 2).
    two = collections.Counter()
    for label, n in counts(section("26-kq-ids-slashes.txt", 2)).items():
        two[label.split(",")[0]] += n
    for k, n in two.items():
        d["kq against one word, " + k] = n
    # Qamats qatan on perfect and participle pieces by stem (22-, section 2).
    stems = collections.Counter()
    for line in section("22-refine.txt", 2):
        m = re.match(r"^    (V\S\S)\s+(\d+)$", line)
        if m and m.group(1)[2] in "pqr":
            stems[m.group(1)[1]] += int(m.group(2))
    for k, n in stems.items():
        d["qatan perfect, stem " + k] = n
    # The nine corrections by tier (22-, section 3).
    tiers = collections.Counter()
    nine = 0
    for line in section("22-refine.txt", 3):
        m = re.match(r"^  \S+ \[.+?\] class \w+; cons (.+)$", line)
        if m:
            nine += 1
            c = eval(m.group(1), {"__builtins__": {}}, {"None": None})
            tiers[
                "untested" if c["n"] == 0 else "supported" if c["pair"] else "flagged"
            ] += 1
    d["corrections"] = nine
    d["corrections fitting"] = tiers["supported"] + tiers["untested"]
    d["corrections flagged"] = tiers["flagged"]
    return d


def record_figures(ids, work_dir):
    """The test figures of the records whose morphhb ids the page shows."""
    out = set()
    keys = ['"id": "%s"' % i for i in ids]
    for name in (
        "10-atoms.jsonl",
        "10-atoms-cant-alef.jsonl",
        "10-atoms-cant-bet.jsonl",
    ):
        with open(work_dir / name, encoding="utf-8") as f:
            for line in f:
                if any(k in line for k in keys):
                    rec = json.loads(line)
                    walk(rec.get("cons", {}), out)
    return out


SKIP = [
    r"\d{4}-\d{2}-\d{2}",  # dates
    r"\b(?:19|20)\d\d\b",  # years: every count of a thousand or more has a comma
    r"\d+:\d+(?:[\N{EN DASH}-]\d+)?",  # verses
    r"\b(?:WLC|Opus|OSIS) \d+(?:\.\d+)+",  # versions
    r"\b[12] (?=Samuel|Kings|Chronicles)",  # book names
    r"\bMethod \d+",
    r"\bsections? \d+(?: and \d+)?",
    r"#\d+",  # issue numbers
    r"\b\d+-character\b",
    r"\b\d+-digit\b",
    r"\b(?:two|\d+)-digit number",
]


def scan(text):
    """{number as written: count} in a text, references left out."""
    stripped = re.sub(r"`[^`]*`", " ", text)  # code
    stripped = re.sub(r"(?m)^#+ \d+\. ", "", stripped)  # numbered headings
    stripped = re.sub(r"(?m)^(?:- )?\d+\. ", "", stripped)  # list numbers
    stripped = re.sub(r"https?://\S+", " ", stripped)
    for pattern in SKIP:
        stripped = re.sub(pattern, " ", stripped)
    found = collections.Counter()
    for m in re.finditer(
        r"(?<![\w.,/#-])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(%?)", stripped
    ):
        found[m.group(1) + (m.group(2) or "") + m.group(3)] += 1
    return found


def check_numbers(text, known, d):
    frag_lines = set()
    if FRAGMENT.exists():
        frag_lines = set(
            page_text.visible_text(FRAGMENT.read_text(encoding="utf-8")).splitlines()
        )
    lines = text.splitlines()
    mine = "\n".join(line for line in lines if line not in frag_lines)
    theirs = "\n".join(line for line in lines if line in frag_lines)
    research = set()
    for path in RESEARCH:
        if path.exists():
            research |= numbers_in(path.read_text(encoding="utf-8"))
    allowed = known | {float(v) for v in d.values()}
    for label, part, extra, source in (
        ("this script's parts", mine, set(), "no output gives"),
        (
            "the fragment's parts",
            theirs,
            research,
            "neither the outputs nor the research reports give",
        ),
    ):
        found = scan(part)
        print(
            "numbers in %s: %d distinct, %d in all"
            % (label, len(found), sum(found.values()))
        )
        for tok in sorted(found):
            if float(tok.rstrip("%").replace(",", "")) not in allowed | extra:
                problem("a number in %s that %s: %s" % (label, source, tok))


def check_headlines(text, F):
    """The figures that page-spec.md names, as the page must state them."""
    t, tbc, tp = F["tiers"], F["tier_by_class"], F["tiers_percent"]
    total = F["mam_atoms"]
    good = t["same"] + t["supported"]
    rest = t["untested"] + t["flagged"] + t["structural"]
    flat = " ".join(text.split())
    sl = F["slashes"]
    expect = [
        "%.2f%% of MAM's %s atoms" % (100.0 * good / total, "{:,}".format(total)),
        "other %s atoms (%.2f%%)" % ("{:,}".format(rest), 100.0 * rest / total),
        "the %s flagged and structural atoms" % (t["flagged"] + t["structural"]),
        "for the %s untested ones" % t["untested"],
        "%s are flagged: %s that differ in pointing and %s in spelling"
        % (t["flagged"], tbc["flagged/A2"], tbc["flagged/B"]),
        "%s are untested" % t["untested"],
        "%s have no one-to-one partner" % t["structural"],
        "%s slashes in %s words"
        % (
            "{:,}".format(sl["letters-equal slashes"]),
            "{:,}".format(sl["letters-equal words with a slash"]),
        ),
        "%s of their %s slashes"
        % (
            sl["slashes placed by letter count or letter alignment"]
            - sl["letters-equal slashes"],
            sl["slashes"] - sl["letters-equal slashes"],
        ),
        "%s bare Tetragrammata and %s with a prefix"
        % ("{:,}".format(F["a2_holam_only"]["bare"]), F["a2_holam_only"]["prefixed"]),
        "%s are supported" % "{:,}".format(F["a2_holam_only_supported"]),
    ]
    for name, label in (
        ("same", "the same form"),
        ("supported", "supported"),
        ("untested", "untested"),
        ("flagged", "flagged"),
        ("structural", "structural"),
    ):
        expect.append("%s | %s | %.2f%%" % (label, "{:,}".format(t[name]), tp[name]))
    for k, n in F["maqaf"].items():
        expect.append("| %s" % "{:,}".format(n))
    other = F["a2_other_than_holam_by_tier"]
    expect.append(
        "%s are supported, %s untested and %s flagged"
        % (other["supported"], other["untested"], other["flagged"])
    )
    bt = F["b_by_tier"]
    expect.append(
        "%s are supported, %s untested and %s flagged"
        % (bt["supported"], bt["untested"], bt["flagged"])
    )
    for s in expect:
        if s not in flat:
            problem("a headline figure is missing: %r" % s)
    print("headline figures checked: %d" % len(expect))


class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.cells = []  # [attrs, text] of each open td/th
        self.blocks = []  # [tag, attrs, text, rtl] of each open block
        self.block_texts = []
        self.runs = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "meta", "link", "img", "hr"):
            if tag == "br":
                for b in self.blocks:
                    b[2].append(" ")
            return
        a = dict(attrs)
        self.stack.append((tag, a))
        if tag in ("td", "th"):
            self.cells.append([a, []])
        if tag in ("p", "li", "caption", "th", "td", "h1", "h2", "h3", "h4"):
            rtl = a.get("dir") == "rtl"
            self.blocks.append([tag, a, [], rtl])

    def handle_endtag(self, tag):
        if tag in ("br", "meta", "link", "img", "hr"):
            return
        while self.stack:
            t, a = self.stack.pop()
            if t == tag:
                break
        if tag in ("td", "th") and self.cells:
            a, text = self.cells.pop()
            if HEB_LETTER.search("".join(text)) and a.get("dir") != "rtl":
                problem(
                    "a table cell with Hebrew lacks dir=rtl: %r" % "".join(text)[:60]
                )
        if tag in ("p", "li", "caption", "th", "td", "h1", "h2", "h3", "h4"):
            for i in range(len(self.blocks) - 1, -1, -1):
                if self.blocks[i][0] == tag:
                    b = self.blocks.pop(i)
                    self.block_texts.append((b[0], b[3], "".join(b[2])))
                    break

    def handle_data(self, data):
        if not self.stack or self.stack[-1][0] in ("style", "script", "title"):
            return
        for c in self.cells:
            c[1].append(data)
        for b in self.blocks:
            b[2].append(data)
        for m in re.finditer(
            "[\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW LETTER TAV}/]+", data
        ):
            run = m.group()
            if not HEB_ANY.search(run):
                continue
            self.runs += 1
            pointed = any(
                "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW POINT QAMATS QATAN}"
                and ch not in NOT_POINTS
                for ch in run
            )
            in_hbo = any(a.get("lang") == "hbo" for _t, a in self.stack)
            in_stack = any(
                t == "td" and "stack" in a.get("class", "").split()
                for t, a in self.stack
            )
            in_bdi = any(t == "bdi" and "lang" not in a for t, a in self.stack)
            if any(t in ("a", "u") for t, _a in self.stack):
                problem("Hebrew inside a link: %r" % run)
            if pointed and not in_hbo:
                problem("pointed Hebrew outside lang=hbo: %r" % run)
            if not pointed and not ((in_hbo and in_stack) or in_bdi):
                problem("unpointed Hebrew outside a stack or a bare bdi: %r" % run)


def first_strong(s):
    for ch in s:
        bidi = unicodedata.bidirectional(ch)
        if bidi == "L":
            return "L"
        if bidi in ("R", "AL"):
            return "R"
    return None


def check_starts(blocks):
    n = 0
    for tag, rtl, text in blocks:
        if rtl:
            continue
        text = " ".join(text.split())
        if not text:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            n += 1
            if first_strong(sentence) == "R":
                problem(
                    "a %s or sentence begins with Hebrew: %r" % (tag, sentence[:60])
                )
    print("English blocks and sentences checked: %d" % n)


def check_page(page):
    head = page.split("<body>")[0]
    for s in (
        "<!doctype html>",
        '<html lang="en">',
        '<meta charset="utf-8">',
        '<meta name="viewport"',
        "<title>",
        'href="../../gh-pages/document.css"',
        'href="../../gh-pages/MAM-with-doc/misc/style.css"',
        'href="../../gh-pages/near-aleppo/link-presentation.css"',
        "table.breakout",
        "td.form",
        "td.bcv",
    ):
        if s not in head:
            problem("the head lacks %r" % s)
    m = re.search(r"</h1>\s*(<[^>]+>)", page)
    if not m or m.group(1) != '<p class="ai-caveat">':
        problem("the caveat is not directly under the h1")
    caveat = re.search(r'<p class="ai-caveat">(.*?)</p>', page, re.S).group(1)
    for s in (
        "Not reviewed by a human",
        "Claude (Opus 5.5)",
        "2026-11-15",
        "Ben Denckla's request",
        "WLC 4.20",
        "MAM-simple",
        "BHS versification",
        "Leningrad Codex itself",
    ):
        if s not in caveat:
            problem("the caveat lacks %r" % s)
    if (
        "text-decoration" in page.split("</style>")[0]
        and "underline" in page.split("</style>")[0]
    ):
        problem("the page's style underlines something")


def check_files():
    src = (HERE / "build_page.py").read_text(encoding="utf-8")
    if HEB_ANY.search(src):
        problem("build_page.py holds a Hebrew character")
    if "\N{COMBINING DOT BELOW}" in src:
        problem("build_page.py holds a decomposed letter with a dot below")
    for path in (
        HERE / "build_page.py",
        HERE / "page_text.py",
        HERE / "page_check.py",
        PAGE,
        TEXT,
    ):
        if b"\r\n" in path.read_bytes():
            problem("%s has CRLF line endings" % path.name)
    extra = sorted({ch for ch in src if ord(ch) > 127})
    print(
        "non-ASCII characters in build_page.py: %s"
        % ", ".join("%s (%s)" % (ch, unicodedata.name(ch)) for ch in extra)
    )


def check(work_dir):
    """Check the page; print what was checked and every problem; return the problems."""
    PROBLEMS.clear()
    page = PAGE.read_text(encoding="utf-8")
    text = TEXT.read_text(encoding="utf-8")
    F = json.loads((OUT / "30-figures.json").read_text(encoding="utf-8"))
    known = set()
    walk(F, known)
    for name in BREAKDOWNS:
        known |= numbers_in((OUT / name).read_text(encoding="utf-8"))
    for name in EXAMPLE_LISTS:
        walk(json.loads((OUT / name).read_text(encoding="utf-8")), known)
    known |= numbers_in(README.read_text(encoding="utf-8"))
    ids = set(re.findall(r"id `([0-9A-Za-z]{5})`", text))
    known |= record_figures(ids, Path(work_dir))
    print("morphhb ids shown on the page: %d" % len(ids))
    d = derived(F)
    check_numbers(text, known, d)
    check_headlines(text, F)
    parser = Markup()
    parser.feed(page)
    parser.close()
    print("Hebrew runs checked: %d" % parser.runs)
    check_starts(parser.block_texts)
    check_page(page)
    check_files()
    if PROBLEMS:
        print("\n%d problems:" % len(PROBLEMS))
        for p in PROBLEMS:
            print("  " + p)
        return list(PROBLEMS)
    print("no problems")
    return []
