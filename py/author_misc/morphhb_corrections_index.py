"""Write gh-pages/morphhb-corrections/index.html, the HTML version of the report on morphhb's
corrections of WLC, and lint it.

WHAT THE PAGE IS

The report asks which of WLC's readings morphhb, the Open Scriptures Hebrew Bible, corrects:
first at the 56 cases of Ben's review of the Israel Bible, then in all of morphhb.  A Claude
session wrote it on 2026-11-13 in an untracked folder, and another wrote this page from it on
2026-11-14, also untracked.  Ben's words of 2026-11-14, asking for the page: "It is
approaching preposterous to explain only in prose and show no pointed hebrew, and pointed
hebrew is basically unreadable in the chat anyway. Please link to the israel bible review where
cases in this morphhb review match ones in the israel bible review".  Of the report's heading
"Why these differ from Part 1's 46 class c cases", he asked: "Am I suppoed to know what
"Part 1" (or its class c cases) are?"

On 2026-11-15 Ben asked for the page and its sources to be tracked, "as long as they are not
large", and chose, on a decision page that day, the page's place (published, not listed in the
site index), this build, the files tracked and their terms.  The tracked files are the report's
README.md, the 27 out/ files that the page reads and out/fetch_log.jsonl, copied byte for byte
into in/morphhb-corrections-2026-11-13/; its what-is-left-out.md lists the report's other
files.  The four modules began as the page's scratch scripts, build_page.py (this module),
page_lib.py, sections.py and review_links.py, and their rules, below, as a spec that the
session wrote for its sub-agent.

THE BUILD

gen_html_file, which py/main_authored.py gen-morphhb-corrections and the mega's step
morphhb-corrections run, does three things, and raises on any failed check, so that the step
fails:

1. morphhb_corrections_review_links.write_links reads the review's generated page and its
   inputs, and writes out/morphhb-corrections/review-links.json, the review's 56 rows and 10
   footnotes with a checked text-fragment link to each, and review-links-check.txt, the
   record of the check.  It raises if the page's rows and the review module's disagree, or if a
   link's first match is not its row.  The mega runs the step right after israel-bible-review,
   whose page this reads.
2. morphhb_corrections_sections builds the sections from the tracked report files and the link
   table.  Its cases() asserts that the report's copies of the review's 56 rows equal the
   review's, so an edit of the review that adds or removes a row, or changes a row's forms or
   page, fails the build until the page is brought into line.
3. This module adds the caveat box, the introduction, the contents and the two closing
   sections, writes the page, and lints the written file (lint below).

THE SECTIONS, IN ORDER

Each section says what the report's README says there, with every form it discusses shown.

1. "The answer in brief": the README's three answers, each with its forms.
2. "The review's 56 cases": the four kinds of case, defined once (rule 3); the five
   corrections; the one analysis of WLC's form; the four text changes; the 46 analyses that fit
   both forms; the six verses of the review's footnote on MAM's ḥataf vowels; and what the
   cases show about morphhb's text.
3. "All of morphhb: nine corrections": the nine; Hosea 13:15; the three mappiq corrections; why
   the review's four suffix cases are not like these; the al/el census; the general test and
   WLC's notes.
4. "morphhb's text against WLC 4.20": which version morphhb's text is; the classes of
   difference (the pashta's stress helper written as a qadma, the divided accents of the
   Decalogues and Genesis 35:22, encoding only, atoms divided in two, ketiv and qere); the README's
   checks.
5. "morphhb's own records": its commit messages, headers, exegesis notes, issues and pull
   requests.
6. "What these methods cannot find".

Then the departures, each a place where the report's data show its README to be wrong or
imprecise, and the sources, with the rebuild command.  The first departure was known when the
page was specified: the README says that changes of letters, vowels or maqaf are confined to
three words of the Decalogues, Daniel 2:39's ketiv and qere and the 12 words that morphhb
divides for exegesis, but morphhb's main text differs from WLC 4.20 in a vowel or the maqaf at
five atoms of the Decalogues, at three of which morphhb's alternative-accent note does not make
it good.

THE RULES

1. Every Hebrew form is copied by script, never typed, from the report's out/ files, from the
   link table or from MAM-basics' own readers; a parse of one of the report's .txt files
   asserts how many times its pattern matches.  Every form goes through the lib's helpers
   (stack, word, heb, prose), which put it in MAM-normal mark order.  The lint fails if any of
   the four modules holds a Hebrew character.
2. The Israel Bible's forms appear only as the review shows them
   (in/israel-bible-review/README.md, "Privacy"): from the link table's ib fields or the
   review's module, with the report's copies asserted equal to them.
3. Names.  The page's reader has not seen the brief that the report followed, so the page
   never says "Part 1", "Part 2", "class a" to "class d" or "method 1" to "method 4", except
   in a quotation of one of the README's headings, drawn by q(); the lint bans them elsewhere.
   The four kinds of case are named once each, in the section on the review's cases: a
   correction (5 cases), where the lemma, the morph or both fit only MAM's form; an analysis
   of WLC's form (1 case); an analysis that fits both forms (46 cases), where WLC's form and
   MAM's differ only in pointing that neither the lemma nor the morph records; and a text
   change (4 cases), where morphhb's text is not WLC 4.18's.  An edition is named with its
   version: WLC 4.18, WLC 4.20, WLC 4.22, UXLC 2.6.
4. Attribution.  Every reading is a transcription's: WLC's, with its version, the UXLC's or
   MAM's.  The page says nothing about what the Leningrad Codex has: no image was consulted.
   morphhb's lemmas and morphs are morphhb's analyses, and Claude's judgments are named as
   Claude's.
5. Hebrew prose follows the hebrew-prose skill: an atom and a chanted word are named as such;
   a text is said to have a mark, and no accent becomes another; what the README calls "a qadma
   for the first of two pashtas" is the pashta's stress helper, which morphhb writes with HEBREW
   ACCENT QADMA where WLC has HEBREW ACCENT PASHTA; no English sentence, list item or cell's
   prose opens with a Hebrew word; a real em dash; and unpointed Hebrew in prose keeps the
   surrounding font.
6. Forms in tables.  The forms that a row compares stand one above the other in one cell
   (form_td), and the table's lead says which form stands where.  The columns run, left to
   right: further Hebrew columns, such as morphhb's word; the compared forms; the verse
   (vcell); then Latin columns.  A form compared with the review's forms is stripped as the
   review strips its forms (review_stripped); where accents matter, forms keep them.  morphhb's
   own word, where it is shown, keeps its morpheme division "/".
7. Links.  Every verse is named with vref, in prose, or vcell, in a table, which link a verse
   that is a row of the review, or that one of the review's footnotes names, and nothing else;
   the hover says when the row is about another word of the verse.  Morph codes are drawn with
   morph(), whose hover spells the code out; commits with commit(); issues with issue().
8. Style.  Each section leads with its finding.  A heading or sentence that announces a count
   is followed by a numbered list.  Bold marks only a defined term or a list item's label.  No
   previews of later sections, no sentence that only insists, and both sides of a comparison
   are named.
"""

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from author_misc import morphhb_corrections_lib as L
from author_misc import morphhb_corrections_review_links as review_links
from author_misc import morphhb_corrections_sections as S
from author_misc.morphhb_corrections_lib import H, ht, p

TITLE = (
    "morphhb's corrections of WLC: the Israel Bible review's cases, then all of morphhb"
)
PAGE = L.PAGE_DIR / "index.html"
# The report's README, as tracked, on GitHub: a published page links a tracked file outside
# gh-pages/ there, as py/intro_doc_audit/human_review.py does.
README_URL = (
    "https://github.com/bdenckla/MAM-basics/blob/main/in/morphhb-corrections-2026-11-13/"
    "README.md"
)
# The four modules that build the page, which the lint requires to hold no Hebrew character.
MODULES = (
    Path(__file__),
    Path(L.__file__),
    Path(S.__file__),
    Path(review_links.__file__),
)
BEN_ASKED = (
    "ask the commander to start a session that will investigate all other such corrections "
    "in morphhb, or at least to start with, see whether there are corrections for all or "
    "some of the other cases identified in my israel bible review."
)


def caveat():
    return H(
        '<p class="ai-caveat"><em>AI-generated report, not yet reviewed by a human.</em> '
        "Claude, an AI model, wrote this page on 2026-11-14, New York time, from the report "
        "that another Claude session wrote on 2026-11-13. No human has reviewed either, so "
        "read it as a draft.</p>\n"
    )


def intro():
    assert (L.F / "README.md").is_file()
    return ht(
        p(
            "This page presents a report, dated 2026-11-13, which asks which of WLC's "
            "readings morphhb corrects: first at the cases of Ben's review of the Israel "
            "Bible, then in all of morphhb. The report's ",
            L.a(README_URL, L.code("README.md"), "external"),
            " and the files of the report that this page reads are tracked in ",
            L.code("in/morphhb-corrections-2026-11-13/"),
            ". Ben's request, as that report quotes it, was to ",
            H("\N{LEFT DOUBLE QUOTATION MARK}"),
            BEN_ASKED,
            H("\N{RIGHT DOUBLE QUOTATION MARK}"),
        ),
        p(
            H("<strong>morphhb</strong>"),
            " is the Open Scriptures Hebrew Bible (",
            L.a(L.MORPHHB_URL, "openscriptures/morphhb", "external"),
            "): WLC's text, word by word, with each word's lemma, an augmented Strong's "
            "number with a letter for each prefix, and its morph, a code for its part of "
            "speech and form (hover over a morph on this page to read it spelled out). The "
            "report read morphhb at ",
            L.commit("d4265dfa"),
            ", the head of its master branch on 2026-11-13.",
        ),
        p(
            "A ",
            H("<strong>correction</strong>"),
            ", as the report defines it, is a word whose text keeps WLC's reading while its "
            "lemma or its morph analyses another reading, typically MAM's. A place where "
            "morphhb changed the text itself is a separate kind, a ",
            H("<strong>text change</strong>"),
            ". Every reading is attributed to the transcription that has it: WLC, with its "
            "version, the UXLC or MAM. Nothing here says what the Leningrad Codex has.",
        ),
        p(
            "Forms that are compared stand one above the other in one cell, as in the review: "
            "each letter whose marks differ is highlighted, and an atom with no difference is "
            "gray. A form compared with the review's forms is shown as the review shows "
            "forms, without accents, meteg and rafeh; where accents matter, forms keep them. "
            "Every form is copied by script from the report's data or the review's, and is in "
            "MAM-normal mark order."
        ),
        p(
            "A verse that is a row of the review links to that row, and its hover says when "
            "the row is about another word of the verse; a verse that the review names only "
            "in a footnote links to the footnote. A link lands on its row in a browser that "
            "supports text fragments; in another it opens the review at its top.",
        ),
    )


def contents():
    items = [L.here(id_, title) for id_, title, _b in S.SECTIONS]
    items += [L.here("departures", DEPARTURES_TITLE), L.here("sources", SOURCES_TITLE)]
    return H(
        '<nav class="contents"><h2 id="contents">Contents</h2>\n'
        + L.ol(items)
        + "</nav>\n"
    )


DEPARTURES_TITLE = "Where this page departs from the report"
SOURCES_TITLE = "Sources, and how to rebuild this page"


def departures(departures_):
    head = L.heading(2, DEPARTURES_TITLE, "departures")
    if not departures_:
        return ht(head, p("Nowhere: every statement here is the report's."))
    return ht(
        head,
        p(
            "Where the report's data show its README to be wrong or imprecise, this page "
            "says what the data show. Each place:"
        ),
        L.ol(departures_),
    )


def sources():
    return ht(
        L.heading(2, SOURCES_TITLE, "sources"),
        p(
            "The report's tracked files are in ",
            L.code("in/morphhb-corrections-2026-11-13/"),
            ": its README, which names every input and output; the ",
            L.code("out/"),
            " files that this page shows; and ",
            L.code("out/fetch_log.jsonl"),
            ", the report's log of what it fetched. A note beside them, ",
            L.code("what-is-left-out.md"),
            ", lists the report's other files, which are not tracked. The review's rows and "
            "footnotes, with each link's text fragment, are in ",
            L.code("out/morphhb-corrections/review-links.json"),
            ", which ",
            L.code("py/author_misc/morphhb_corrections_review_links.py"),
            " writes from the review's inputs and checks against the review's page.",
        ),
        p("The page is rebuilt, from the MAM-basics root, by:"),
        H(
            "<pre><code>./.venv/Scripts/python.exe py/main_authored.py "
            "gen-morphhb-corrections</code></pre>\n"
        ),
    )


def body(departures_):
    parts = [caveat(), intro(), contents()]
    built = []
    for id_, title, builder in S.SECTIONS:
        sec = builder()
        assert isinstance(sec, H), id_
        assert f'id="{id_}"' in sec, id_
        built.append((id_, title, sec))
        parts.append(sec)
    S.self_test(built, departures_)
    parts += [departures(departures_), sources()]
    return ht(*parts)


# ---------------------------------------------------------------- lint

# The blocks whose own text the banned phrases are sought in (a phrase in a cell is not sought
# again in its row and table).
LEAF_BLOCKS = {"p", "li", "td", "th", "caption", "h1", "h2", "h3", "h4", "summary"}
VOID = {"br", "meta", "link", "img", "hr", "input"}
BANNED = [
    re.compile(r"\bPart [12]\b"),
    re.compile(r"\bclass(?:es)? [abcd]\b", re.I),
    re.compile(r"\bmethods? [1-4]\b", re.I),
    re.compile(r" -- "),
]


class Lint(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, attrs dict, text list)
        self.errors = []
        self.ids = []
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k, v in attrs:
            if v and L.HEB_ANY.search(v):
                self.errors.append(
                    f"Hebrew in the attribute {k} of <{tag}>: {ascii(v)}"
                )
        if "id" in d:
            self.ids.append(d["id"])
        if tag == "a" and "href" in d:
            self.hrefs.append(d["href"])
        if tag in VOID:
            return
        # (tag, attrs, its text, its text outside quotations)
        self.stack.append((tag, d, [], []))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, d, text, plain = self.stack.pop()
            text, plain = "".join(text), "".join(plain)
            self._close(t, d, text, plain)
            if self.stack:
                self.stack[-1][2].append(text)
                if t not in ("q", "blockquote"):
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
        if tag in LEAF_BLOCKS:
            for rx in BANNED:
                m = rx.search(plain)
                if m:
                    self.errors.append(
                        f"banned phrase {m.group(0)!r} in <{tag}>: {text[:60]!r}"
                    )


def lint(page_text):
    errors = []
    for src in MODULES:
        if L.HEB_ANY.search(src.read_text(encoding="utf-8")):
            errors.append(f"typed Hebrew in {src.name}")
    lp = Lint()
    lp.feed(page_text)
    lp.close()
    errors += lp.errors
    dup = sorted({i for i in lp.ids if lp.ids.count(i) > 1})
    if dup:
        errors.append(f"ids used twice: {dup}")
    review_hrefs = {r["href"] for r in L.links()["rows"]} | {
        f"{L.REVIEW_HREF}#{f['anchor']}" for f in L.links()["footnotes"]
    }
    n_review = 0
    for href in lp.hrefs:
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
        if parts.path == L.REVIEW_HREF:
            n_review += 1
            if href not in review_hrefs:
                errors.append(
                    f"a link into the review that review-links.json lacks: {href}"
                )
    return errors, n_review, len(lp.hrefs)


def gen_html_file():
    """Write the link table, then the page, and lint the page as written; return the page's
    path.  Raises on any failed check, so that the mega's step fails."""
    review_links.write_links()
    departures_ = S.departures()
    text = L.page(TITLE, body(departures_))
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(text, encoding="utf-8", newline="\n")
    errors, n_review, n_links = lint(PAGE.read_text(encoding="utf-8"))
    print(
        f"{len(text.encode('utf-8'))} bytes; links: {n_links}, into the review: {n_review};"
        f" departures: {len(departures_)}"
    )
    if errors:
        for e in errors:
            print("LINT:", e)
        raise ValueError(f"{len(errors)} lint errors in {PAGE}")
    return PAGE
