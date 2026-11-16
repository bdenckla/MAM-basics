"""Write gh-pages/morphhb-corrections/index.html, "Where morphhb defies or resolves WLC", and
lint it.

WHAT THE PAGE IS

The page shows where morphhb, the Open Scriptures Hebrew Bible, defies WLC 4.20, the version of
WLC that its text is, and where it resolves WLC, as Ben framed the two on 2026-11-16.  A Claude
session wrote a report on 2026-11-13 in an untracked folder, which asked which of WLC's readings
morphhb corrects, first at the cases of Ben's review of the Israel Bible and then in all of
morphhb, and another wrote this page from it on 2026-11-14.  On 2026-11-15 Ben asked for the
page and its sources to be tracked, "as long as they are not large": the report's README, the 27
out/ files that the page then read and out/fetch_log.jsonl were copied byte for byte into
in/morphhb-corrections-2026-11-13/, whose what-is-left-out.md lists the report's other files.

On 2026-11-16 Ben asked for the page's present form ("Ben's framing", which intro() quotes),
and, on a decision page of that day, decided:

1A. The page's two verbs, each defined once (intro): morphhb defies WLC, and morphhb resolves
    WLC, the verb of decision 8.  Counts name words; the page has no nouns such as "defiance",
    and "correction" survives only in its address and in names inside the repository.
2B. A sub-agent applied those definitions to every word that the report judged and to the 178
    rare pairs that it listed but did not judge; its verdicts, with the report's beside them,
    are in in/morphhb-verdicts-2026-11-16/verdicts.json, from which the page takes every list
    and count of words.
3A. Isaiah 66:22 is among the words where morphhb defies WLC, with its history untraced.
4A. The links into the review and the build's tie to it went: the module that wrote them,
    morphhb_corrections_review_links, and its output folder, out/morphhb-corrections/, were
    deleted.
5A. morphhb's text defies WLC 4.20 at the Decalogue atoms where its main text and its
    alternative-accent note together do not have WLC 4.20's marks, at the atoms that it has as
    two and at Daniel 2:39's ketiv and qere; it resolves WLC at the other atoms of the two
    accentuations of the Decalogues and Genesis 35:22; its other differences are encoding only.
6A. The title, with decision 8's verb; the page keeps its address, and the modules and the
    report's folder keep their names.
7A. UXLC 2.6 is named only at a word on the page where it differs from WLC 4.20.
8A. The second verb is "resolves" ("8A, resolves is good"), which morphhb_corrections_lib's
    RESOLVE holds, the one place that another choice would change.

and he asked that the page have no framing by the review, name WLC 4.18 nowhere, and name WLC
4.22 only in passing where it changes the word, or the note on the word, in question.

A fresh review of the page, written on 2026-11-16 in a scratch folder of the session that
rewrote it (review-page.md), made 22 findings, which a sub-agent applied that day: among them
the definition of "resolves" now has decision 9's option A, the words that verdicts.json's own
definition has (Ben had not yet answered decision 9); the page has its own stylesheet; no
sentence opens with the lowercase name morphhb; and the defies table gives the notes at each
word.

THE BUILD

gen_html_file, which py/main_authored.py gen-morphhb-corrections and the mega's step
morphhb-corrections run, builds the sections of morphhb_corrections_sections from verdicts.json
and the report's tracked files, adds the caveat box, the introduction, the contents and the
sources, writes the page and its stylesheet, style.css (morphhb_corrections_lib.STYLESHEET,
under a banner naming this generator), and lints the written page (lint below).  It raises on
any failed check, so that the step fails.

THE SECTIONS, IN ORDER

1. The caveat and the introduction, which quotes Ben's framing and his gloss of the second verb,
   defines the two verbs, and defines an atom, a chanted word and an alternative note.
2. "The answer in brief", with the headline counts and the verdicts that are counted, not
   listed ("fits both", "ketiv", "same", "text").
3. "Where morphhb defies WLC": by its analysis, a table of the words with their notes; by its
   text, the atoms of decision 5A.
4. "Where morphhb resolves WLC": by its analysis, a table of the words; by its text, the two
   accentuations.
5. "Where morphhb follows WLC, and its slips", the last of them in an alternative note.
6. "The text of morphhb against WLC 4.20": which version it is, by morphhb's history; the
   classes of difference; the two that are encoding only and the final letters that differ
   only from MAM-basics' conversion of WLC 4.20; the checks.
7. "What morphhb's records say".
8. "What these methods cannot find", which first says what the methods were.
9. "Where this page departs from the report", with how the verdicts here differ from the
   report's; then the sources, with the rebuild command.

THE RULES

1. Every Hebrew form is copied by script, never typed, from verdicts.json or the report's out/
   files; a parse of one of the report's .txt files asserts how many times its pattern
   matches.  Every form goes through the lib's helpers (stack, word, heb, prose), which put it
   in MAM-normal mark order.  The lint fails if any of the three modules holds a Hebrew
   character.
2. Names.  The page's reader has not seen the brief that the report followed, so the page never
   says "Part 1", "Part 2", "class a" to "class d" or "method 1" to "method 4", except in a
   quotation, drawn by q().  The verbs are used only as defined, the second with "WLC" as its
   object; the report's names for its verdicts appear only as code, as verdicts.json records
   them.  An edition is named with its version: WLC 4.20, WLC 4.22, UXLC 2.6.
3. Attribution.  Every form is a transcription's: WLC's, with its version, the UXLC's or
   MAM's.  The page says nothing about what the Leningrad Codex has: no image was consulted.
   morphhb's lemmas and morphs are morphhb's analyses, and the verdicts and their reasons are
   Claude's.  No sentence, list item, caption or heading, and no clause after a colon or a
   semicolon, opens with the lowercase name morphhb (the title is Ben's), which the lint
   checks.
4. Hebrew prose follows the hebrew-prose skill: an atom and a chanted word are named as such;
   a text is said to have a mark, and no accent becomes another; the pashta's stress helper is
   one, which morphhb has as HEBREW ACCENT QADMA where WLC 4.20 has HEBREW ACCENT PASHTA; no
   English sentence, list item or cell's prose opens with a Hebrew word; a real em dash; and
   unpointed Hebrew in prose keeps the surrounding font.
5. Forms in tables.  The forms that a row compares stand one above the other in one cell
   (form_td), and the table's lead says which form stands where.  The columns run, left to
   right: further Hebrew columns; the compared forms; the verse (vcell); then Latin columns.  A
   table of words shows its forms without accents, meteg or a maqaf after the atom (the lib's
   analysis_form), with morphhb's "/" between morphemes; elsewhere forms keep their accents.
6. Versions.  WLC 4.18 and the review appear nowhere.  WLC 4.22 and UXLC 2.6 appear only in a
   paragraph, list item or table row that names a verse that
   morphhb_corrections_sections.allowed_versions allows.
7. Links.  A verse is named in plain text (vref in prose, vcell in a table) and linked nowhere.
   Morph codes are drawn with morph(), whose hover spells the code out; commits with commit();
   issues with issue().
8. Style.  Each section leads with its finding.  A heading or sentence that announces a count is
   followed by a numbered list.  Bold marks only a defined term or a list item's label.  No
   previews of later sections, no sentence that only insists, and both sides of a comparison
   are named.
"""

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from author_misc import morphhb_corrections_lib as L
from author_misc import morphhb_corrections_sections as S
from author_misc.morphhb_corrections_lib import H, ht, p
from mb_cmn import provenance

R = L.RESOLVE
TITLE = f"Where morphhb defies or {R['s']} WLC"
PAGE = L.PAGE_DIR / "index.html"
# The report's README, as tracked, on GitHub: a published page links a tracked file outside
# gh-pages/ there, as py/intro_doc_audit/human_review.py does.
README_URL = (
    "https://github.com/bdenckla/MAM-basics/blob/main/in/morphhb-corrections-2026-11-13/"
    "README.md"
)
# The three modules that build the page, which the lint requires to hold no Hebrew character.
MODULES = (Path(__file__), Path(L.__file__), Path(S.__file__))

# Ben's framing, as the decision page of 2026-11-16 quotes it from the session in which he
# asked for the page's present form, and his gloss of the second verb, from his answer to
# decisions 1 to 7 on that page: copied exactly.
BEN_FRAMING_WHEN = "Ben, 2026-11-16, 12:52, New York time"
BEN_FRAMING = (
    "start a session that will help me work on the HTML document (and supporting files) "
    'showing where morphhb has had to "defy" (or "correct") WLC, by providing an '
    "alternatively-pointed (or I suppose alternatively-spelled!) word and/or by providing "
    "metadata (morphology, strong's, etc.) that defies the WLC (or, if not defies, chooses a "
    "specific interpretation of an ambiguous or, in some cases, undefined pointing (e.g. a "
    'shuruq with a xiriq dot has undefined meaning). (So, perhaps better that "corrected" '
    'is "defies (if defined) or defines (if undefined)".)'
)
# The page quotes the framing from where it speaks of morphhb, after an ellipsis, since its
# opening words ask for the session that made the page (the review of 2026-11-16, finding
# 22).  Ben's "xiriq" is the house's ASCII spelling of the vowel's name, with x for an h with a
# dot below, which the page's prose spells out; hebrew-prose's rendered-prose.md, "Quoting a
# source that romanizes differently", puts the page's name in square brackets in its place, and
# the page says once what its brackets are (BRACKETS_NOTE), which holds for the "[sic]" that
# morphhb_corrections_sections.SIC adds to a commit message too.
BEN_FRAMING_FROM = "where morphhb has had to"
BEN_FRAMING_SPELLING = (
    "xiriq",
    "[\N{LATIN SMALL LETTER H WITH DOT BELOW}iriq]",
)
BRACKETS_NOTE = (
    "A word in square brackets in a quotation on this page is this page's: here its spelling "
    "of the vowel's name, in place of Ben's."
)
BEN_GLOSS_WHEN = "Ben, 2026-11-16"
BEN_GLOSS = (
    'I was suggesting "defines" to mean something like "makes legal", "resolves ambiguity", '
    "etc."
)


def framing_shown():
    """Ben's framing as the page quotes it: from BEN_FRAMING_FROM, after an ellipsis, with the
    page's spelling of the vowel's name in square brackets in place of his."""
    start = BEN_FRAMING.index(BEN_FRAMING_FROM)
    assert BEN_FRAMING.count(BEN_FRAMING_FROM) == 1
    old, new = BEN_FRAMING_SPELLING
    assert BEN_FRAMING.count(old) == 1
    return "\N{HORIZONTAL ELLIPSIS} " + BEN_FRAMING[start:].replace(old, new)


def caveat():
    return H(
        '<p class="ai-caveat"><em>AI-generated page, not yet reviewed by a human.</em> '
        "Claude, an AI model, wrote this page on 2026-11-14 and rewrote it on 2026-11-16, New "
        "York time, from a report that another Claude session wrote on 2026-11-13 and from "
        "Claude's verdicts of 2026-11-16. No human has reviewed any of them, so read it as a "
        "draft.</p>\n"
    )


def intro():
    assert (L.F / "README.md").is_file()
    return ht(
        p(
            "This page shows where morphhb, the Open Scriptures Hebrew Bible, defies WLC and "
            f"where it {R['s']} WLC, as Ben framed the two on 2026-11-16:"
        ),
        L.blockquote(BEN_FRAMING_WHEN, framing_shown()),
        p(
            BRACKETS_NOTE,
            " Of the second verb, which his framing calls ",
            L.q("defines"),
            ", he wrote the same day:",
        ),
        L.blockquote(BEN_GLOSS_WHEN, BEN_GLOSS),
        p(
            "He chose ",
            L.q(R["s"]),
            " as the verb for that sense. This page gives each verb one definition, and in "
            "both ",
            L.q("WLC"),
            " is short for WLC 4.20's form, WLC 4.20 being the version of WLC that "
            "morphhb's text is:",
        ),
        L.ol(
            [
                ht(
                    "Where WLC 4.20's form, as written, is a regular spelling of some word or "
                    "inflection, and morphhb's text, lemma or morph reads another, morphhb ",
                    L.strong("defies"),
                    " WLC.",
                ),
                # The words after "or of more than one" are decision 9's option A, which the
                # verdicts applied (verdicts.json's own definition of "resolves"), with "or
                # letters", since at Deuteronomy 25:7 and Malachi 3:16 a letter makes it so.
                ht(
                    "Where WLC 4.20's form, as written, is a regular spelling of no word or "
                    "inflection in its place (a mark is missing, contradicts another or "
                    "stands where none can), or of more than one, where the marks or letters "
                    "in which it differs from MAM's form make it so, and morphhb's text, lemma or "
                    "morph reads it as one, morphhb ",
                    L.strong(R["s"]),
                    " WLC.",
                ),
            ]
        ),
        p(
            "In morphhb (",
            L.a(L.MORPHHB_URL, "openscriptures/morphhb", "external"),
            "), each word of WLC's text has a lemma, an augmented Strong's number with a "
            "letter for each prefix, and a morph, a code for its part of speech and form "
            "(hover over a morph on this page to read it spelled out). The report read "
            "morphhb at ",
            L.commit("d4265dfa"),
            ", the head of its master branch on 2026-11-13.",
        ),
        p(
            "An ",
            L.strong("atom"),
            " is a written word between spaces or maqaf marks; a ",
            L.strong("chanted word"),
            " is an atom or a whole maqaf compound. Each of morphhb's words is an atom. "
            "Where WLC has the marks of two accentuations in one text, in the Decalogues and "
            "at Genesis 35:22, morphhb has one accentuation's marks in its main text and the "
            "other's in notes on the atoms whose marks differ, which this page calls its ",
            L.strong("alternative notes"),
            ".",
        ),
        p(
            "The verdict on each word and its reason are Claude's, in ",
            L.code("in/morphhb-verdicts-2026-11-16/verdicts.json"),
            ". The forms, morphhb's data and the counts of its text's differences are from a "
            "report that another Claude session wrote on 2026-11-13, whose ",
            L.a(README_URL, L.code("README.md"), "external"),
            " and the files of it that this page reads are tracked in ",
            L.code("in/morphhb-corrections-2026-11-13/"),
            ". Every form is attributed to the transcription that has it, with its "
            "version; nothing here says what the Leningrad Codex has.",
        ),
        p(
            "Forms that are compared stand one above the other in one cell: each letter whose "
            "marks differ is highlighted, and an atom with no difference is gray; MAM's HEBREW "
            "POINT QAMATS QATAN counts there as HEBREW POINT QAMATS, which WLC has for both "
            "qamats vowels. Every form is copied by script from the data and is in MAM-normal "
            "mark order."
        ),
    )


SOURCES_TITLE = "Sources, and how to rebuild this page"


def contents():
    items = [L.here(id_, title) for id_, title, _b in S.SECTIONS]
    items.append(L.here("sources", SOURCES_TITLE))
    return H(
        '<nav class="contents"><h2 id="contents">Contents</h2>\n'
        + L.ol(items)
        + "</nav>\n"
    )


def sources():
    return ht(
        L.heading(2, SOURCES_TITLE, "sources"),
        p(
            "The verdicts, with their definitions and reasons, are in ",
            L.code("in/morphhb-verdicts-2026-11-16/verdicts.json"),
            ". The report's tracked files are in ",
            L.code("in/morphhb-corrections-2026-11-13/"),
            ": its README, which names every input and output; the ",
            L.code("out/"),
            " files that this page shows; and ",
            L.code("out/fetch_log.jsonl"),
            ", the report's log of what it fetched. A note beside them, ",
            L.code("what-is-left-out.md"),
            ", lists the report's other files, which are not tracked.",
        ),
        p("The page is rebuilt, from the MAM-basics root, by:"),
        H(
            "<pre><code>./.venv/Scripts/python.exe py/main_authored.py "
            "gen-morphhb-corrections</code></pre>\n"
        ),
    )


def body():
    parts = [caveat(), intro(), contents()]
    built = []
    for id_, title, builder in S.SECTIONS:
        sec = builder()
        assert isinstance(sec, H), id_
        assert f'id="{id_}"' in sec, id_
        built.append((id_, title, sec))
        parts.append(sec)
    S.self_test(built)
    parts.append(sources())
    return ht(*parts)


# ---------------------------------------------------------------- lint

# The blocks whose own text the banned phrases are sought in (a phrase in a cell is not sought
# again in its row and table).
LEAF_BLOCKS = {"p", "li", "td", "th", "caption", "h1", "h2", "h3", "h4", "summary"}
VOID = {"br", "meta", "link", "img", "hr", "input"}
QUOTED = ("q", "blockquote")
# The elements whose text the phrase checks do not read: quotations, and code, which holds the
# repository's paths and names.
UNREAD = QUOTED + ("code",)
# The elements whose text joins its parent's with a space on each side, so that a row's cells
# do not run together.
SPACED = LEAF_BLOCKS | {
    "tr",
    "thead",
    "tbody",
    "table",
    "ol",
    "ul",
    "blockquote",
    "pre",
}
BANNED = [
    re.compile(r"\bPart [12]\b"),
    re.compile(r"\bclass(?:es)? [abcd]\b", re.I),
    re.compile(r"\bmethods? [1-4]\b", re.I),
    re.compile(r" -- "),
    # Ben's decision 1A: "correction" survives only in the page's address and in names inside
    # the repository, which the page writes as code; and counts name words, so no noun of
    # either verb.
    re.compile(r"\bcorrect", re.I),
    re.compile(r"\bdefian", re.I),
    re.compile(r"\b" + R["noun"], re.I),
]
# The second verb's forms, each of which must have "WLC" as its object.
VERB = re.compile(
    r"\b("
    + "|".join(
        sorted({R[k] for k in ("base", "s", "ing", "ed")}, key=len, reverse=True)
    )
    + r")\b",
    re.I,
)
# The versions that the page names only at the verses that allowed_versions allows.
VERSIONS = (
    ("WLC 4.22", re.compile(r"\b4\.22\b")),
    ("UXLC 2.6", re.compile(r"\bUXLC\b")),
)


# The blocks in which no sentence may open with the lowercase name morphhb (rendered-prose.md:
# "Never open a sentence with an abbreviation that cannot be capitalized", which the review of
# 2026-11-16, finding 17, applied to the name), nor a clause after a colon or a semicolon,
# which that review counted among the openings: the title, h1, is Ben's and is not read, and
# a quotation is not read.
SENTENCE_BLOCKS = {"p", "li", "caption", "h2", "h3", "h4"}
LOWERCASE_OPENING = re.compile(r"(?:^|[.!?:;]\s|[.!?]\)\s)\s*morphhb\b")


class Lint(HTMLParser):
    def __init__(self, allowed):
        super().__init__(convert_charrefs=True)
        self.allowed = allowed
        self.stack = []  # (tag, attrs dict, its text, its text outside UNREAD)
        self.errors = []
        self.ids = []
        self.hrefs = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k, v in attrs:
            if v and L.HEB_ANY.search(v):
                self.errors.append(
                    f"Hebrew in the attribute {k} of <{tag}>: {ascii(v)}"
                )
            if k == "title" and v and re.search(r"\bcorrect", v, re.I):
                self.errors.append(f"a banned word in a hover: {v!r}")
        if "id" in d:
            self.ids.append(d["id"])
        if tag == "a" and "href" in d:
            self.hrefs.append(d["href"])
        if tag == "link" and d.get("rel") == "stylesheet":
            self.stylesheets.append(d.get("href", ""))
        if tag in VOID:
            return
        self.stack.append((tag, d, [], []))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, d, text, plain = self.stack.pop()
            text, plain = "".join(text), "".join(plain)
            self._close(t, d, text, plain)
            if t in SPACED:
                text, plain = f" {text} ", f" {plain} "
            if self.stack:
                self.stack[-1][2].append(text)
                if t not in UNREAD:
                    self.stack[-1][3].append(plain)
            if t == tag:
                break

    def handle_data(self, data):
        if not self.stack:
            return
        if L.HEB_ANY.search(data):
            ok = any(
                d.get("lang") == "hbo" or t == "bdi" for t, d, _x, _y in self.stack
            )
            if not ok:
                self.errors.append(f"Hebrew outside lang=hbo or bdi: {ascii(data)}")
        self.stack[-1][2].append(data)
        self.stack[-1][3].append(data)

    def _inside(self, *tags):
        return any(t in tags for t, _d, _x, _y in self.stack)

    def _close(self, tag, d, text, plain):
        if d.get("lang") == "hbo":
            if not L.uni_denorm.has_std_mark_order(text):
                self.errors.append(f"not in MAM-normal order: {ascii(text)}")
        if tag == "bdi" and "lang" not in d and L.is_pointed(text):
            self.errors.append(f"pointed Hebrew in a bare bdi: {ascii(text)}")
        if tag == "td" and L.HEB_ANY.search(text) and d.get("dir") != "rtl":
            if "form" in d.get("class", "") or not re.search("[A-Za-z]", text):
                self.errors.append(f"a Hebrew cell without dir=rtl: {ascii(text[:40])}")
        if tag in ("p", "li", "caption") or (
            tag == "td" and "note" in d.get("class", "")
        ):
            first = re.search(r"[^\W\d_]", text)
            if first and L.HEB_ANY.match(first.group(0)):
                self.errors.append(f"<{tag}> opens with Hebrew: {ascii(text[:40])}")
        if tag in UNREAD or self._inside(*QUOTED):
            return
        if tag in SENTENCE_BLOCKS and LOWERCASE_OPENING.search(plain.strip()):
            self.errors.append(
                f"a sentence that opens with lowercase morphhb in <{tag}>: {plain[:60]!r}"
            )
        if tag in LEAF_BLOCKS:
            for rx in BANNED:
                m = rx.search(plain)
                if m:
                    self.errors.append(
                        f"banned phrase {m.group(0)!r} in <{tag}>: {plain[:60]!r}"
                    )
            for m in VERB.finditer(plain):
                if not plain[m.end() :].startswith(" WLC"):
                    self.errors.append(
                        f"the verb {m.group(0)!r} without WLC as its object in <{tag}>: "
                        f"{plain[max(0, m.start() - 40) : m.end() + 20]!r}"
                    )
        if tag == "caption":
            tables = [e for e in self.stack if e[0] == "table"]
            if tables:
                tables[-1][1]["_caption"] = plain
        if tag in ("p", "li", "tr") and not self._inside("thead"):
            caption = ""
            if tag == "tr":
                tables = [e for e in self.stack if e[0] == "table"]
                caption = tables[-1][1].get("_caption", "") if tables else ""
            context = f"{plain} {caption}".replace(L.NBSP, " ")
            for label, rx in VERSIONS:
                if rx.search(plain) and not any(
                    v in context for v in self.allowed[label]
                ):
                    self.errors.append(
                        f"{label} named in a <{tag}> that names no verse where the page may "
                        f"name it: {plain[:80]!r}"
                    )


def lint(page_text):
    errors = []
    for src in MODULES:
        if L.HEB_ANY.search(src.read_text(encoding="utf-8")):
            errors.append(f"typed Hebrew in {src.name}")
    # Ben, 2026-11-16: no framing by the review of the Israel Bible, and no WLC 4.18.
    if "4.18" in page_text:
        errors.append("WLC 4.18 named on the page")
    if re.search(r"israel\s+bible", page_text, re.I):
        errors.append("the Israel Bible named on the page")
    # The review's folder, named anywhere: its page or its stylesheet (finding 16).
    if "israel-bible-review" in page_text:
        errors.append("the review's folder named on the page")
    lp = Lint(S.allowed_versions())
    lp.feed(page_text)
    lp.close()
    errors += lp.errors
    dup = sorted({i for i in lp.ids if lp.ids.count(i) > 1})
    if dup:
        errors.append(f"ids used twice: {dup}")
    if lp.stylesheets != list(L.CSS_HREFS):
        errors.append(f"the stylesheets loaded are not CSS_HREFS: {lp.stylesheets}")
    for href in lp.stylesheets:
        if not (L.PAGE_DIR / href).resolve().is_file():
            errors.append(f"a stylesheet that is no file: {href}")
    for href in lp.hrefs:
        if "israel-bible-review" in href:
            errors.append(f"a link into the review: {href}")
        parts = urlsplit(href)
        if parts.scheme in ("http", "https"):
            continue
        if href.startswith("#"):
            if href[1:] not in lp.ids:
                errors.append(f"a link to no id of this page: {href}")
            continue
        target = (L.PAGE_DIR / unquote(parts.path)).resolve()
        if not target.is_file():
            errors.append(f"a link to no file: {href}")
    return errors, len(lp.hrefs)


def stylesheet():
    """The page's stylesheet as gen_html_file publishes it: a banner naming this generator, as
    doc/html-styles.md asks of a generated sheet, then morphhb_corrections_lib's STYLESHEET.
    """
    banner = "/* " + provenance.generated_html_comment(__file__) + " */"
    return banner + "\n" + L.STYLESHEET


def gen_html_file():
    """Write the page and its stylesheet, and lint the page as written; return the page's
    path.  Raises on any failed check, so that the mega's step fails."""
    text = L.page(TITLE, body())
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    css = PAGE.parent / L.STYLESHEET_NAME
    css.write_text(stylesheet(), encoding="utf-8", newline="\n")
    PAGE.write_text(text, encoding="utf-8", newline="\n")
    errors, n_links = lint(PAGE.read_text(encoding="utf-8"))
    print(f"{len(text.encode('utf-8'))} bytes; links: {n_links}")
    if errors:
        for e in errors:
            print("LINT:", e)
        raise ValueError(f"{len(errors)} lint errors in {PAGE}")
    return PAGE
