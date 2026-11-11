"""Exports gen_html_file, and, for the lint of MAM's forms in
py/tests/test_israel_bible_review_mam_forms.py, review_lines, forms, data_table_rows and
stripped.

gen_html_file writes Ben's review "The Israel Bible: this ain't no Koren edition" as
gh-pages/israel-bible-review/index.html, and its stylesheet as style.css beside it.  Ben
drafted the review elsewhere; at his word it was ported here on 2026-11-10 and is edited here
from then on.  in/israel-bible-review/README.md says which file to edit for what, and keeps the
review's decisions.

THE REVIEW'S OWN FOLDER, 2026-11-11.  Until then the page was
gh-pages/MAM-with-doc/misc/review_of_israel_bible.html and this module was
review_of_israel_bible.py.  Ben asked that day for the review to move "to its own folder in
gh-pages" (the README's Decision 2); py/main_authored.py's docstring, "WHERE A NEW PAGE GOES",
gives his note on why misc/ was an outdated precedent.  This module's name ends in "index"
because mb_author.author.help_gen_html_file asks that of the generator of an index.html.

THE INPUTS are tracked files of this repository, and this module reads nothing outside it:

* in/israel-bible-review/review.md, the review's text: its prose and footnotes, and two data
  tables, the tour's five rows whose notes are Markdown and the Decalogues' eight rows;
* in/israel-bible-review/forms.json, the forms of the tour's other 43 rows, each with its
  verse and its page in the Israel Bible, whose notes are TOP, TRANSLIT and NEXT below;
* israel_bible_review_index.css beside this module, the page's styles.

Every Hebrew form was lifted from a text by a script, the Israel Bible's from the text layer
of its PDF and MAM's from MAM-simple; none is typed.  English notes are authored here, except
those of review.md's two data tables.

Forms are shown as the Israel Bible could show them: accents, meteg, rafeh, paseq, sof pasuq,
the extraordinary dots and format characters are stripped from every form (Ben, 2026-11-07:
"strip accents from forms having accents, to make it more of an 'apples to apples' comparison
with Israel Bible"), qamats qatan is written as qamats and ḥolam ḥaser for vav as ḥolam.  The
one exception is MAM's form of the Reubenite words and of Job 31:7's word, which keeps its
rafeh on the alef (Ben, 2026-11-09; RAFEH_REFS).  Maqaf is kept, a final maqaf included.
Two forms are shown (Ben, 2026-11-07): the Israel Bible's above the consensus, MAM's.

Ben's later requests of 2026-11-07 shape the rest: the page is public-facing, with no
procedure or method; every table is in reading order, by the Israel Bible's page; the Israel
Bible column is gone and its page number sits under the verse in a Where column; and every
letter cluster (a letter with its marks) involved in a difference between a verse's two forms
is highlighted.  An atom with no such cluster is gray.

Ben, 2026-11-07, later still: "Unify the draft review with the "weird pointing" document into a
single HTML document".  review_html renders review.md, with the weird-pointing tables, the
tour, as one section in place of its marker.

Ben, 2026-11-08: one big table.  The weird-pointing section's own heading, introduction and three
tables gave way to one table under the review's "A sampling of quirks" (Ben, 2026-11-09: "A tour
of the quirks" "sounds like this might be exhaustive") and its lead.  It held the
old tables' rows, the transliterated verses' rows without their "Transliteration follows" column,
and the rows of review.md's data table after the section marker (the old "Two vowels on one letter"
and "Letters with no vowel at all"), all in the Israel Bible's order.  Every note compares the
Israel Bible's form with the consensus, MAM's; other editions are named only where they matter, and
each edition's abbreviation is explained on hover, everywhere on the page.

Ben, 2026-11-09: "propose some thematic divisions of the current one huge "Sample of Quirks"
table".  He approved six that evening (DIVISIONS): the same rows now stand in six tables, each
under its division's h3 heading, each division's rows in the Israel Bible's order.

Ben, 2026-11-09: the Decalogues too, "like a small version of the "sampling of quirks" table".
review.md's data table under "The Decalogues" holds the Israel Bible's forms and MAM's in its
elyon strand, the closer of MAM's two strands to the Israel Bible's text, and is drawn where it
stands, as the tour's tables are drawn.

THE PORT, 2026-11-10.  The draft's top-level script became gen_html_file.  The tour's 43 rows
take their forms from forms.json, each the edition's own form, stripped as stripped() strips it
and put in MAM-normal order (uni_denorm.give_std_mark_order), as Ben's decision of 2026-10-30,
recorded in doc/mam-normal-mark-order.md, asks of a quotation in authored prose.  That changed
the bytes of two shown forms, in mark order alone: the Israel Bible's at Judges 15:14, whose
shin dot now precedes the shin's ḥiriq and whose dagesh now precedes the tav's ḥiriq, and MAM's
at Nehemiah 9:14, whose dagesh now precedes its qamats.  The draft's inline styles are now
the stylesheet beside this module, which loads Taamey D from the site's one copy; the arrow
links load the shared near-aleppo/link-presentation.css, of which the draft held a copy; and
the crop of Deuteronomy 3:22 is published under an ASCII name (IMAGES).  The lint in
py/tests/test_israel_bible_review_mam_forms.py checks MAM's forms against MAM-simple, at Ben's
word of 2026-11-10.
"""

import html
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote, urlsplit

from mb_author import author
from mb_cmn import paths
from mb_cmn import provenance
from mb_cmn import site_links
from mb_cmn import uni_denorm
from mb_misc import mb_html

_TITLE = "The Israel Bible: this ain't no Koren edition"
_FNAME = "index.html"
_CSS_FNAME = "style.css"
# The review's own folder of the site, a peer of gh-pages/book-of-job/ and gh-pages/clc/.
_OUT_DIR = paths.gh_pages_dir() / "israel-bible-review"
# The page's path below the deploy root, from which its links to the site's other pages are
# computed (mb_cmn/site_links.py).
_PAGE = (_OUT_DIR / _FNAME).relative_to(paths.gh_pages_dir()).as_posix()
# The page's stylesheets, in order: the prose base first, as doc/html-styles.md asks of every
# prose page; then this page's own, written by gen_html_file from the .css beside this module;
# then the shared stylesheet of the arrow links that go marks (doc/html-styles.md, "Arrow
# links").
_CSS_HREFS = (
    "../document.css",
    _CSS_FNAME,
    "../near-aleppo/link-presentation.css",
)
_CSS_SOURCE = Path(__file__).with_suffix(".css")
_INPUT_DIR = paths.in_dir() / "israel-bible-review"


def review_lines():
    """review.md, the review's text, as its lines."""
    return (_INPUT_DIR / "review.md").read_text(encoding="utf-8").split("\n")


SHORT = {
    "Genesis": "Gen",
    "Exodus": "Exod",
    "Leviticus": "Lev",
    "Numbers": "Num",
    "Deuteronomy": "Deut",
    "Joshua": "Josh",
    "Judges": "Judg",
    "1 Samuel": "1 Sam",
    "2 Samuel": "2 Sam",
    "1 Kings": "1 Kgs",
    "2 Kings": "2 Kgs",
    "Isaiah": "Isa",
    "Jeremiah": "Jer",
    "Ezekiel": "Ezek",
    "Hosea": "Hos",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obad",
    "Jonah": "Jonah",
    "Micah": "Mic",
    "Nahum": "Nah",
    "Habakkuk": "Hab",
    "Zephaniah": "Zeph",
    "Haggai": "Hag",
    "Zechariah": "Zech",
    "Malachi": "Mal",
    "Psalms": "Ps",
    "Proverbs": "Prov",
    "Job": "Job",
    "Song of Songs": "Song",
    "Ruth": "Ruth",
    "Lamentations": "Lam",
    "Qoheleth": "Eccl",
    "Esther": "Esth",
    "Daniel": "Dan",
    "Ezra": "Ezra",
    "Nehemiah": "Neh",
    "1 Chronicles": "1 Chr",
    "2 Chronicles": "2 Chr",
}


def bcv(ref):
    m = re.match(r"^(.*?) (\d+):(\d+)", ref)
    return m.group(1), int(m.group(2)), int(m.group(3))


def short_ref(ref):
    m = re.match(r"^(.*?) (\d+:\d+)", ref)
    return f"{SHORT[m.group(1)]} {m.group(2)}".replace(" ", "\N{NO-BREAK SPACE}")


# ---------------------------------------------------------------- forms

STRIP = re.compile(
    "["
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW MARK MASORA CIRCLE}"
    "\N{HEBREW POINT METEG}"
    "\N{HEBREW POINT RAFE}"
    "\N{HEBREW PUNCTUATION PASEQ}"
    "\N{HEBREW PUNCTUATION SOF PASUQ}"
    "\N{HEBREW MARK UPPER DOT}"
    "\N{HEBREW MARK LOWER DOT}"
    "\N{COMBINING GRAPHEME JOINER}"
    "\N{ZERO WIDTH NON-JOINER}"
    "\N{ZERO WIDTH JOINER}"
    "\N{LEFT-TO-RIGHT MARK}"
    "\N{RIGHT-TO-LEFT MARK}"
    "\N{WORD JOINER}"
    "\N{ZERO WIDTH NO-BREAK SPACE}"
    "]"
)
NORM = str.maketrans(
    {
        "\N{HEBREW POINT QAMATS QATAN}": "\N{HEBREW POINT QAMATS}",
        "\N{HEBREW POINT HOLAM HASER FOR VAV}": "\N{HEBREW POINT HOLAM}",
    }
)


# Ben, 2026-11-09: "Please include the rafeh above alef in the MAM (consensus) form of all ראובני
# cases".  At the tour's six Reubenite words, MAM's form keeps its rafeh, which is on the alef;
# every other form, and MAM's form elsewhere, loses its rafeh with its accents.
STRIP_KEEP_RAFEH = re.compile(STRIP.pattern.replace("\N{HEBREW POINT RAFE}", ""))
assert STRIP_KEEP_RAFEH.pattern != STRIP.pattern
REUVENI_REFS = [
    "Numbers 26:7",
    "Deuteronomy 3:12",
    "Deuteronomy 3:16",
    "Deuteronomy 4:43",
    "Joshua 12:6",
    "2 Kings 10:33",
]
# Ben, 2026-11-09, of MAM's rafeh at Job 31:7, whose note now says that the Israel Bible lacks
# "the rafeh on alef": "I concur."  So MAM's form keeps its rafeh there too.
RAFEH_REFS = REUVENI_REFS + ["Job 31:7"]


def stripped(s, keep_rafeh=False):
    """A form reduced to the Israel Bible's marks, keeping the source's mark order; with
    keep_rafeh, its rafeh marks too (RAFEH_REFS)."""
    s = (STRIP_KEEP_RAFEH if keep_rafeh else STRIP).sub("", s).translate(NORM)
    s = (
        re.sub(r"\s+", " ", s)
        .replace("\N{HEBREW PUNCTUATION MAQAF} ", "\N{HEBREW PUNCTUATION MAQAF}")
        .strip()
    )
    return s


def is_mark(ch):
    return (
        "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW POINT QAMATS QATAN}"
        and ch != "\N{HEBREW PUNCTUATION MAQAF}"
    )


def key(s, keep_rafeh=False):
    """Comparison key: within each letter's cluster, marks sorted.  Every maqaf counts, a final
    one included (Ben, 2026-11-07: "Let's not go apples-to-apples on that one")."""
    out, cluster = [], []
    for ch in stripped(s, keep_rafeh):
        if is_mark(ch):
            cluster.append(ch)
        else:
            out.extend(sorted(cluster))
            cluster = []
            out.append(ch)
    out.extend(sorted(cluster))
    return "".join(out)


# A row of forms.json has its verse, as "Book chapter:verse" with the book named as SHORT's keys
# name it; its page in the Israel Bible; and the two forms that the page shows of its word, the
# Israel Bible's and the consensus form, MAM's (Ben, 2026-11-07), each stripped as stripped()
# strips it and in MAM-normal order.  A row may also have the label that its entry in TOP gives
# it.
_FORM_FIELDS = frozenset({"reference", "page", "israel_bible", "mam"})
_OPTIONAL_FORM_FIELDS = frozenset({"label"})


def forms():
    """forms.json's rows, each checked as _FORM_FIELDS says, in the Israel Bible's order.
    Closed dispatch: a missing or unknown field, a verse with two rows, a form other than the
    page shows, or a row whose two forms are one raises."""
    rows = json.loads((_INPUT_DIR / "forms.json").read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("forms.json holds no rows")
    for row in rows:
        if (
            not isinstance(row, dict)
            or not _FORM_FIELDS <= set(row)
            or set(row) - _FORM_FIELDS - _OPTIONAL_FORM_FIELDS
        ):
            raise ValueError(
                f"a row of forms.json with missing or unknown fields: {row}"
            )
        ref = row["reference"]
        m = re.fullmatch(r"(.+) (\d+):(\d+)", ref)
        if not (m and m.group(1) in SHORT):
            raise ValueError(f"a reference that SHORT cannot shorten: {ref!r}")
        if type(row["page"]) is not int or row["page"] < 1:
            raise ValueError(f"{ref}: a page that is no page number: {row['page']!r}")
        if "label" in row and not (isinstance(row["label"], str) and row["label"]):
            raise ValueError(f"{ref}: an empty label")
        keep = ref in RAFEH_REFS
        for field, keep_rafeh in (("israel_bible", False), ("mam", keep)):
            form = row[field]
            if (
                not isinstance(form, str)
                or not form
                or stripped(form, keep_rafeh) != form
            ):
                raise ValueError(
                    f"{ref}: {field} is not as the page shows it: {form!r}"
                )
            if not uni_denorm.has_std_mark_order(form):
                raise ValueError(f"{ref}: {field} is not in MAM-normal order: {form!r}")
        if keep:
            # MAM's form keeps one rafeh, on the alef.
            assert row["mam"].count("\N{HEBREW POINT RAFE}") == 1, ref
            assert "\N{HEBREW LETTER ALEF}\N{HEBREW POINT RAFE}" in row["mam"], ref
        # The two forms differ in a letter or a mark, not in mark order alone.
        assert key(row["israel_bible"]) != key(row["mam"], keep), ref
    refs = [row["reference"] for row in rows]
    if len(refs) != len(set(refs)):
        raise ValueError(f"forms.json gives a verse two rows: {sorted(refs)}")
    if rows != sorted(rows, key=reading_key):
        raise ValueError("forms.json's rows are not in the Israel Bible's order")
    return rows


# ---------------------------------------------------------------- highlighting


def units(form):
    """A shown form as units: a letter with its marks, a maqaf or a space."""
    out = []
    for ch in form:
        if is_mark(ch) and out and out[-1][0] not in " \N{HEBREW PUNCTUATION MAQAF}":
            out[-1] += ch
        else:
            out.append(ch)
    return out


def unit_key(unit):
    return unit[0] + "".join(sorted(unit[1:]))


def hot_units(forms):
    """For each form (a list of units), the indices of its units involved in a difference: a unit
    is hot when another form has no unit aligned with it, or one with other marks.  Units are
    aligned on their base characters."""
    hot = [set() for _ in forms]
    for i, a in enumerate(forms):
        for j, b in enumerate(forms):
            if i == j:
                continue
            sm = SequenceMatcher(
                None, [u[0] for u in a], [u[0] for u in b], autojunk=False
            )
            for tag, i1, i2, j1, _j2 in sm.get_opcodes():
                if tag != "equal":
                    hot[i].update(range(i1, i2))
                    continue
                for k in range(i2 - i1):
                    if unit_key(a[i1 + k]) != unit_key(b[j1 + k]):
                        hot[i].add(i1 + k)
    return hot


def atoms(form_units):
    """Index ranges of a form's atoms: the runs of units between spaces and maqaf marks."""
    out, start = [], 0
    for k, u in enumerate(form_units + [" "]):
        if u in (" ", "\N{HEBREW PUNCTUATION MAQAF}"):
            if k > start:
                out.append(range(start, k))
            start = k + 1
    return out


def context_units(form_units, hot):
    """The units of atoms with no hot unit, which are there only for context (Ben, 2026-11-07:
    gray and not letter-spaced).  None when no atom is hot."""
    ctx = set()
    rngs = atoms(form_units)
    for rng in rngs:
        if not any(k in hot for k in rng):
            ctx.update(rng)
    if len(ctx) == sum(len(rng) for rng in rngs):
        return set()
    return ctx


def form_html(form_units, hot):
    """One form, each hot unit in its own span, which marks it as a cluster that differs, and
    each context atom in a gray span."""
    ctx = context_units(form_units, hot)
    out, run = [], []
    for k, u in enumerate(form_units):
        text = html.escape(u)
        if k in hot:
            text = f'<span class="diff">{text}</span>'
        if k in ctx:
            run.append(text)
            continue
        if run:
            out.append(f'<span class="context">{"".join(run)}</span>')
            run = []
        out.append(text)
    if run:
        out.append(f'<span class="context">{"".join(run)}</span>')
    return f'<span class="he" lang="hbo">{"".join(out)}</span>'


# ---------------------------------------------------------------- cells and order


# Ben, 2026-11-09: "Although I like the link styling using a symbol for the link instead of
# underlining, could we still bring back link-text coloring, i.e. compared to default link
# styling, ditch the underlining but not the coloring, and add the arrow symbol to the link
# text, instead of making the arrow symbol *be* the link text?"; and then "Yes, make this
# analogous to MAM-basics links."  So every link on the page is marked as MAM-basics' link
# helper marks its links (py/near_aleppo/link_presentation.py): data-na-link says where the link
# goes, and that helper's shared stylesheet, which the page loads (_CSS_HREFS), draws the link's
# text in the link color, not underlined, followed by an arrow in the same color: right to
# another MAM-basics page, a boxed outward arrow to any other site, down to a later place on
# this page.  The arrow is drawn, not written, so it is not part of the text that a reader
# copies.  A hover title is given only where it says more than the text: the title of the page
# it links to.
#
# A link is written as its address, as review.md writes it for a reader on GitHub, and an
# address on MAM-basics' site becomes the page's relative href to it as the page is drawn
# (go): Ben, 2026-11-11, "Fix it to be a relative link and fix any other
# inappropriately-absolute links please" (mb_cmn/site_links.py).


def link_kind(href):
    """The helper's kind for a link to another page: "page" for an address on MAM-basics' site,
    as the helper's _kind has it, and "external" for any other.  The page's links within itself
    are its footnote references (footnote_ref)."""
    address = urlsplit(href)
    assert address.scheme == "https" and address.netloc, href
    return "page" if href.startswith(site_links.SITE_URL) else "external"


def go(href, text, title=None):
    """A link to ``href``, an address; one on MAM-basics' site gets the relative href."""
    hover = f' title="{html.escape(title)}"' if title else ""
    kind = link_kind(href)
    if kind == "page":
        href = site_links.site_href_from_url(_PAGE, href)
    return f'<a href="{html.escape(href)}" data-na-link="{kind}"{hover}>{text}</a>'


def where_cell(r, rowspan):
    """The verse, then its page in the Israel Bible (Ben, 2026-11-07: no "PDF" qualification;
    the PDF's page numbers are taken to be the book's).  No link (Ben, 2026-11-08)."""
    page = f"page {r['page']}"
    span = f' rowspan="{rowspan}"' if rowspan > 1 else ""
    return f'<td class="bcv first"{span}>{short_ref(r["reference"])}<br>{page}</td>'


def reading_key(r):
    """The Israel Bible's reading order: its page, then chapter and verse."""
    _book, chapter, verse = bcv(r["reference"])
    return r["page"], chapter, verse


def in_reading_order(pairs):
    """[(item, row)] sorted by the row's place in the Israel Bible (Ben, 2026-11-07: reading
    order).  Chapter and verse break a tie of pages only within one book."""
    out = sorted(pairs, key=lambda p: reading_key(p[1]))
    for (_x, r1), (_y, r2) in zip(out, out[1:]):
        if r1["page"] == r2["page"]:
            assert bcv(r1["reference"])[0] == bcv(r2["reference"])[0], (
                r1["reference"],
                r2["reference"],
            )
    return out


def spanning(cls, rowspan, content):
    span = f' rowspan="{rowspan}"' if rowspan > 1 else ""
    return f'<td class="{cls} first"{span}>{content}</td>'


N_SHOWN = 2  # the Israel Bible's form and the consensus form


def candidate_rows(r, extra=""):
    """Two <tr>s, the Israel Bible's form above the consensus form.  The first also holds the
    Where cell, which spans both, and `extra`, cells that span at least as far."""
    us = [units(r["israel_bible"]), units(r["mam"])]
    hot = hot_units(us)
    trs = []
    for k, (u, h) in enumerate(zip(us, hot)):
        first = " first" if k == 0 else ""
        cells = f'<td dir="rtl" class="form{first}">{form_html(u, h)}</td>'
        if k == 0:
            cells += where_cell(r, N_SHOWN) + extra
        trs.append(f"<tr>{cells}</tr>")
    return trs


def table(headers, trs):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    return (
        f'<table class="main"><thead><tr>{ths}</tr></thead><tbody>\n'
        + "\n".join(trs)
        + "\n</tbody></table>\n"
    )


# ---------------------------------------------------------------- the review (review.md)

SECTION_MARK = "<!-- weird-pointing -->"
HEB_CHAR = (
    "["
    "\N{COMBINING GRAPHEME JOINER}"
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW PUNCTUATION GERSHAYIM}"
    "\N{HAIR SPACE}"
    "\N{HEBREW LETTER YOD WITH HIRIQ}-\N{HEBREW LIGATURE ALEF LAMED}"
    "]"
)
HEB_RUN = re.compile(f"{HEB_CHAR}+(?: {HEB_CHAR}+)*")
# Ben, 2026-11-08: "Merge the three rows of "Two vowels on one letter" into "The weirdest forms"",
# and "Replace the section "Letters with no vowel at all" with rows in "the weirdest forms"".
# review.md holds those rows' forms in a data table after the section marker, with these headers.
TOUR_ROW_HEADERS = ("Verse", "Page", "Israel Bible", "MAM", "Note")
# Ben, 2026-11-09: "Completely overhaul the section called "The Decalogues". Present it all like a
# small version of the "sampling of quirks" table.  Make all comparisons be of IB to MAM-taxton or
# MAM-elyon, whatever minimizes differences (i.e. be charitably in your choice of taxton or elyon,
# but be consistent, i.e. don't charitably switch from word to word)."  The Israel Bible differs
# from MAM's elyon strand (MAM-simple's cant-bet) in fewer places than from its taxton strand, in
# each Decalogue, so the Decalogues' data table compares it with the elyon throughout, and its
# MAM column says so.
ELYON = (
    "\N{HEBREW LETTER AYIN}\N{HEBREW LETTER LAMED}\N{HEBREW LETTER YOD}"
    "\N{HEBREW LETTER VAV}\N{HEBREW LETTER FINAL NUN}"
)
DECALOGUE_ROW_HEADERS = ("Verse", "Page", "Israel Bible", f"MAM's {ELYON}", "Note")
# Ben asked on 2026-11-08 that the page explain its abbreviations on hover.  Every occurrence on
# the page, outside tags, of these abbreviations of editions and of the manuscript gets its
# expansion as a hover.  A name joined by a hyphen, as in MAM-basics, is not the abbreviation.
# An abbreviation that the page does not use has no entry; add one with its first use.
ABBREVIATIONS = {
    "BHL": "Biblia Hebraica Leningradensia, Aron Dotan's edition of the Leningrad Codex",
    "BHS": "Biblia Hebraica Stuttgartensia",
    # Ben, 2026-11-09: "Replace, wherever it occurs in the "Notes" column, "The Israel Bible has"
    # with "IB has", with, as one would expect, "IB" hover-explained."
    "IB": "the Israel Bible",
    "LC": "the Leningrad Codex",
    "MAM": "Miqra according to the Masorah",
    "WLC": "the Westminster Leningrad Codex",
    # Ben, 2026-11-09, of the Reubenite note: "See MAM's relevant FOI".
    "FOI": (
        "feature of interest: one of the pages of MAM-with-doc that gather MAM's words with "
        "a given feature"
    ),
    # On 2026-11-09 Ben asked, of Judges 19:4's note, for short names of the xataf vowels:
    # "xsegol" for xataf segol and "xpatax" for xataf patax.
    "ḥsegol": "ḥataf segol",
    "ḥpataḥ": "ḥataf pataḥ",
    # Ben, 2026-11-08, of Deuteronomy 3:22: "This requires a CGJ in the encoding".  By Ben's
    # decision every abbreviation keeps a hover, so this one has its expansion too.
    "CGJ": (
        "COMBINING GRAPHEME JOINER, a Unicode character that keeps the marks on either "
        "side of it in their written order"
    ),
    # Ben, 2026-11-10, of Deuteronomy 3:22's "To encode this sequence robustly": "where robustly
    # is hover-explained to mean "in a manner immune to the re-ordering that Unicode
    # normalization would otherwise impose"".  A gloss rather than an abbreviation, drawn alike.
    # That sentence went the same day ("Remove the following"); the hover serves the note's
    # "non-robustly".
    "robustly": (
        "in a manner immune to the re-ordering that Unicode normalization would otherwise "
        "impose"
    ),
    # Ben, 2026-07-28, of citing Yeivin's and Breuer's books: "use CoS and ITM respectively, and
    # make these hover-reveal the full title."  (hebrew-prose's rendered-prose.md, "Cite the two
    # books as ITM and CoS".)  "Use of xataf vowels under non-gutturals" cites ITM.
    "ITM": "Introduction to the Tiberian Masorah",
}
ABBREVIATION = re.compile(r"\b(" + "|".join(ABBREVIATIONS) + r")\b(?![-\w])")
# Footnotes (Ben, 2026-11-07: "untracked" is to have "a footnote").  The text refers to a note as
# [^label]; a line "[^label]: text", continued by lines indented four spaces, defines it.  Each
# label is defined once and referred to once, and the notes are numbered in reading order.  A blank
# line followed by an indented line starts the note's next paragraph (Ben, 2026-11-09, of the note
# on WLC's quality: "Also include the "Worse ..." paragraph in that (rather large) footnote").
# Ben, 2026-11-09: "<my review of _A Hebrew Reader for the Pentateuch_> where underscores indicate
# italics (or rather, indicate a "book-title" style, which should be implemented as italics".  A
# pair of underscores outside tags and outside a word marks a book's title, drawn as a <cite>.
BOOK_TITLE = re.compile(r"(?<![\w_])_([^_\s][^_]*?)_(?![\w_])")
FOOTNOTE_REF = re.compile(r"\[\^([a-z0-9-]+)\]")
FOOTNOTE_DEF = re.compile(r"\[\^([a-z0-9-]+)\]: (.+)")
# Each label's number, as footnote_ref gives it; emptied at the start of each build (body_html).
FOOTNOTE_NUMBERS = {}
# Ben, 2026-11-10, of the note on WLC's quality, whose "Worse ..." paragraph now ends with its
# three sources as a list: "I'm using asterisks as in markdown, to communicate that I want an
# unordered list presentation of these items."  After a blank line, a paragraph of a note may be
# such a list: each item starts with NOTE_LIST_ITEM and goes on in lines indented as far as its
# text, NOTE_LIST_MORE, and the list is drawn as a <ul>.
NOTE_LIST_ITEM = "    - "
NOTE_LIST_MORE = " " * len(NOTE_LIST_ITEM)


# Hebrew points and accents, but not maqaf, paseq or sof pasuq: bare letters with those count as
# unpointed (hebrew-prose's rendered-prose.md, "Unpointed Hebrew keeps the surrounding font").
POINT_OR_ACCENT = re.compile(
    "[\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW POINT METEG}\N{HEBREW POINT RAFE}"
    "\N{HEBREW POINT SHIN DOT}\N{HEBREW POINT SIN DOT}\N{HEBREW MARK UPPER DOT}"
    "\N{HEBREW MARK LOWER DOT}\N{HEBREW POINT QAMATS QATAN}]"
)


def isolate_hebrew(s):
    """Wrap each run of Hebrew outside tags for direction: a pointed run in the pointed-Hebrew
    span, and an unpointed one in a bare <bdi>, so that it keeps the font of the text around
    it, as Ben's rule for unpointed Hebrew asks."""
    parts = re.split(r"(<[^>]+>)", s)
    for k in range(0, len(parts), 2):
        parts[k] = HEB_RUN.sub(
            lambda m: (
                f'<span class="hi" lang="hbo" dir="rtl">{m.group(0)}</span>'
                if POINT_OR_ACCENT.search(m.group(0))
                else f"<bdi>{m.group(0)}</bdi>"
            ),
            parts[k],
        )
    return "".join(parts)


def explain_abbreviations(s):
    """Wrap each abbreviation of ABBREVIATIONS outside tags in an <abbr> with its expansion."""
    parts = re.split(r"(<[^>]+>)", s)
    for k in range(0, len(parts), 2):
        parts[k] = ABBREVIATION.sub(
            lambda m: f'<abbr title="{html.escape(ABBREVIATIONS[m.group(1)])}">'
            f"{m.group(1)}</abbr>",
            parts[k],
        )
    return "".join(parts)


def footnote_ref(m):
    """A reference to a footnote: its number in brackets, on the baseline, linked to the note.
    Ben, 2026-11-08: "don't superscript the callout. Just put "3" in brackets as normal
    (baseline-aligned) text. (Superscripts typically mess up line spacing)"."""
    label = m.group(1)
    assert label not in FOOTNOTE_NUMBERS, f"footnote referred to twice: {label}"
    FOOTNOTE_NUMBERS[label] = n = len(FOOTNOTE_NUMBERS) + 1
    # Marked as go marks a link: the notes follow every reference, so the arrow points down, as
    # MAM-basics' helper points it at a later place on the same page.
    return (
        f'<span class="fn"><a id="fnref-{label}" href="#fn-{label}" data-na-link="down">'
        f"[{n}]</a></span>"
    )


def note_html(paras):
    """A note's text: one paragraph as it stands, several each in its own <p>, and a list, a
    paragraph given as the list of its items, as a <ul>."""
    if len(paras) == 1:
        assert isinstance(paras[0], str), paras
        return inline(paras[0])
    return "".join(
        (
            f"<p>{inline(p)}</p>"
            if isinstance(p, str)
            else "<ul>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in p) + "\n</ul>"
        )
        for p in paras
    )


def footnotes_html(defs):
    """The notes, numbered as their references are, for the end of the review.  Each note is the
    list of its paragraphs."""
    assert set(defs) == set(FOOTNOTE_NUMBERS), (sorted(defs), sorted(FOOTNOTE_NUMBERS))
    assert not any(
        FOOTNOTE_REF.search(x)
        for paras in defs.values()
        for p in paras
        for x in ([p] if isinstance(p, str) else p)
    ), "a note within a note"
    if not defs:
        return ""
    lis = "\n".join(
        f'<li id="fn-{label}">{note_html(defs[label])}</li>'
        for label in sorted(defs, key=FOOTNOTE_NUMBERS.__getitem__)
    )
    return (
        f'<section class="footnotes">\n<h2>Notes</h2>\n<ol>\n{lis}\n</ol>\n</section>'
    )


# The images that review.md names, each with the name of its file in
# gh-pages/israel-bible-review/img/.  review.md names an image as the draft did; its
# published file is named as the review of A Hebrew Reader for the Pentateuch names its images,
# by its verse, its atom in consensus_to_ascii (py/author_boj_util/author.py) and its source,
# since no tracked filename holds a Hebrew letter.
IMAGES = {
    "img/deut-3-22-word.png": "Deut 3v22 FYRAV6 -- Israel Bible PDF page 457.png",
}


def image_src(src):
    """The page's src for an image that review.md names.  Closed dispatch: an image that IMAGES
    does not name raises."""
    if src not in IMAGES:
        raise ValueError(f"an image that IMAGES does not name: {src!r}")
    # The file's name has spaces, which a URL may not hold as they are.
    return quote(f"img/{IMAGES[src]}", safe="/")


def inline(text, footnotes=True):
    """The review's inline Markdown: code, footnote references, links (go), bold, italics.  With
    footnotes=False a footnote reference is left as written, for review_html to number where the
    tour's tables stand."""
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    if footnotes:
        out = FOOTNOTE_REF.sub(footnote_ref, out)
    # Ben, 2026-11-08: "yes, please track the crop".  An image, ![alt](src), before links, whose
    # pattern it contains; image_src gives its src on the page.
    out = re.sub(
        r"!\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<img class="crop" src="{image_src(m.group(2))}" alt="{m.group(1)}">',
        out,
    )
    out = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: go(html.unescape(m.group(2)), m.group(1)),
        out,
    )
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])", r"<i>\1</i>", out)
    parts = re.split(r"(<[^>]+>)", out)
    for k in range(0, len(parts), 2):
        parts[k] = BOOK_TITLE.sub(r"<cite>\1</cite>", parts[k])
    return isolate_hebrew("".join(parts))


# Ben, 2026-11-07: "stack all comparisons: many are still presented horizontally. also highlight
# the difference regions (letter-and-mark clusters) in all comparisons; many are presented without
# highlighting. "Compress" all comparisons: many have every edition enumerated, with its contents:
# stock to IB and consensus, with any other editions' contents noted either in the table or as a
# footnote".  Each of review.md's tables is drawn as the weird-pointing tables are drawn: the
# Israel Bible's form above the consensus form, MAM's, with the clusters where they differ
# highlighted and the verse just right of them (Ben's column order of 2026-09-20).  Closed
# dispatch: the tour's data table (TOUR_ROW_HEADERS) joins the tour's tables instead of being
# drawn where it stands; the Decalogues' data table (DECALOGUE_ROW_HEADERS) is drawn where it
# stands, as the tour's tables are drawn; any other table raises.  The rule for comparison tables
# with a column per edition drew nothing once the last of them, "Verse | Israel Bible | MAM |
# Koren", went with the xataf section's rewrite of 2026-11-10, and went itself at Ben's word the
# same day: "sure, go ahead and remove that unused Koren stuff".
def md_table(block, flat):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in block]
    head_, sep, body = rows[0], rows[1], rows[2:]
    assert all(c and set(c) <= set("-:") for c in sep), sep
    assert all(len(r) == len(head_) for r in body), head_
    if tuple(head_) == TOUR_ROW_HEADERS:
        return ""  # its rows are in the tour's tables (tour_md_items)
    if tuple(head_) == DECALOGUE_ROW_HEADERS:
        return decalogue_table(body, flat)
    # Ben, 2026-11-09, of the one table drawn as prose, "Step | What happened": "I advise getting
    # rid of "Where the Hebrew came from" entirely."  Any other table is unknown.
    raise ValueError(f"unknown table headers: {head_!r}")


def review_html(lines, flat, section):
    """review.md, given as its lines and as flat (review_flat), as HTML, with `section` in place
    of its marker."""
    out, k, defs = [], 0, {}
    assert lines.count(SECTION_MARK) == 1
    while k < len(lines):
        ln = lines[k]
        m = re.match(r"(#{1,3}) (.+)", ln)
        if not ln.strip():
            k += 1
        elif ln == SECTION_MARK:
            # The tour's notes may refer to a footnote (Ben, 2026-11-08: cite Golinets directly).
            # Numbering them here, where the tables stand, keeps the notes in reading order.  No
            # note referred to one from 2026-11-09, when the Golinets sentences went with Ben's
            # "the point is all the non-consensus pointings, not whether they originate in a bad
            # or a good transcription of LC", to 2026-11-10, when Deut 3:22's details and
            # Jer 3:17's note gained one each.
            out.append(FOOTNOTE_REF.sub(footnote_ref, section))
            k += 1
        elif fd := FOOTNOTE_DEF.fullmatch(ln):
            label, text = fd.groups()
            paras = [text]
            k += 1
            while k < len(lines):
                if lines[k].startswith(NOTE_LIST_ITEM) and isinstance(paras[-1], list):
                    paras[-1].append(lines[k][len(NOTE_LIST_ITEM) :])
                    k += 1
                elif (
                    lines[k].startswith(NOTE_LIST_MORE)
                    and lines[k].strip()
                    and isinstance(paras[-1], list)
                ):
                    paras[-1][-1] += " " + lines[k].strip()
                    k += 1
                elif lines[k].startswith("    ") and lines[k].strip():
                    # Text right after a list, or a list right after text, needs a blank line.
                    assert isinstance(paras[-1], str), (label, lines[k])
                    assert not lines[k].startswith(NOTE_LIST_ITEM), (label, lines[k])
                    paras[-1] += " " + lines[k].strip()
                    k += 1
                elif (
                    not lines[k].strip()
                    and k + 1 < len(lines)
                    and lines[k + 1].startswith("    ")
                    and lines[k + 1].strip()
                ):
                    nxt = lines[k + 1]
                    if nxt.startswith(NOTE_LIST_ITEM):
                        paras.append([nxt[len(NOTE_LIST_ITEM) :]])
                    else:
                        paras.append(nxt.strip())
                    k += 2
                else:
                    break
            assert label not in defs, f"footnote defined twice: {label}"
            defs[label] = paras
        elif m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            k += 1
        elif ln.startswith("|"):
            block = []
            while k < len(lines) and lines[k].startswith("|"):
                block.append(lines[k])
                k += 1
            out.append(md_table(block, flat))
        elif re.match(r"\d+\. ", ln):
            items = []
            while k < len(lines) and lines[k].strip():
                if re.match(r"\d+\. ", lines[k]):
                    items.append(re.sub(r"^\d+\. ", "", lines[k]))
                elif lines[k].startswith("   "):
                    items[-1] += " " + lines[k].strip()
                else:
                    raise ValueError(f"unexpected line in a list: {lines[k]!r}")
                k += 1
            out.append(
                "<ol>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in items) + "\n</ol>"
            )
        elif ln.startswith("- "):
            # Ben, 2026-11-08: "the other publications of mine listed as a bulleted list".  An
            # item starts with "- " and goes on in lines indented two spaces.
            items = []
            while k < len(lines) and lines[k].strip():
                if lines[k].startswith("- "):
                    items.append(lines[k][2:])
                elif lines[k].startswith("  "):
                    items[-1] += " " + lines[k].strip()
                else:
                    raise ValueError(f"unexpected line in a list: {lines[k]!r}")
                k += 1
            out.append(
                "<ul>\n" + "\n".join(f"<li>{inline(x)}</li>" for x in items) + "\n</ul>"
            )
        else:
            para = []
            while (
                k < len(lines)
                and lines[k].strip()
                and not lines[k].startswith(("|", "#", "[^", "- "))
            ):
                para.append(lines[k].strip())
                k += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    notes = footnotes_html(defs)
    if notes:
        out.append(notes)
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- the candidates

# Ben, 2026-11-08: Deuteronomy 3:22's note keeps everything after its first sentence in "some sort
# of default-collapsed "Details" section"; later the same day, of Joshua 12:6, "hiding all details
# after the first session in a collapsed-by-default "Details" section as in the Deut 3:22 row", and
# "Do the same ("hide" stuff beyond the first sentence in a "Details" section) in the Jer 3:17 row".
DETAILS_OPEN = "<details><summary>Details</summary>"
DETAILS_CLOSE = "</details>"

# Ben, 2026-11-08: "Reframe its rows, and all rows, as comparisons against consensus, where it is
# noted that we use MAM as a consensus.  Mention other editions only on the occasions where it is
# relevant".  Each note describes the Israel Bible's form against the consensus, MAM's.
TOP = [
    dict(
        ref="Isaiah 46:4",
        # Ben, 2026-11-09: "Change <IB has neither a shin dot nor a sin dot on the letter, ...> to
        # <IB lacks the shin dot that appears in the consensus, leaving it up to the reader to guess
        # whether this is a shin or a sin.>"  MAM's form has a sin dot (HEBREW POINT SIN DOT), as
        # the old note said, so the note says "sin dot".  Ben, 2026-11-10, after dropping a remark
        # on pronunciation from 2 Kgs 18:27's note: "Similarly, remove "leaving it up to the
        # reader to guess whether this is a shin or a sin.""
        note="IB lacks the sin dot that appears in the consensus.",
    ),
    dict(
        ref="Judges 15:14",
        note=("IB has a ḥiriq under the shin instead of a sheva."),
    ),
    dict(
        ref="Judges 19:4",
        note=(
            "IB has, on yod–ḥet–zayin, segol–ḥsegol–pataḥ instead of "
            "pataḥ–ḥpataḥ–segol: the vowels of the qal instead of those of the hiphil."
        ),
    ),
    dict(
        ref="Song of Songs 5:11",
        # Ben, 2026-11-09: "Change "which makes no syllable, so the reading is unclear." to "which
        # makes no sense.""
        note=(
            "IB has a shuruq dot in the first vav instead of a qubuts under it. "
            "That vav is then a shuruq, a vowel directly after the qof's sheva, which makes no "
            "sense."
        ),
    ),
    dict(
        ref="1 Samuel 27:10",
        note=("IB has, on yod–resh, pataḥ–sheva instead of the reverse."),
    ),
    dict(
        ref="Jeremiah 3:17",
        # Ben, 2026-11-09: "(a) "as well" as what? Seemed superfluous so I removed it (b) no need
        # to contrast with the consensus; ... the contrast is implied (edition X has Y implies
        # edition Z doesn't have it)".  Ben, 2026-11-10, of its details: "Make this a
        # footnote rather than a "Details" text"; they are review.md's [^vav-dot], word for word.
        # At the port, "vavs" became "vav letters", as the lint of plural Hebrew names asks
        # (Ben, 2026-11-10: "Yes that fix is good."; in/israel-bible-review/README.md,
        # Decision 1).
        note="IB has a dot in the first of the two final vav letters.[^vav-dot]",
    ),
    dict(
        ref="Proverbs 20:1",
        # Ben, 2026-11-09: "Remove "so the word loses its last syllable.""
        note="IB has no ḥiriq under the second yod.",
    ),
    dict(
        ref="Joel 2:12",
        note="IB has a sheva instead of a ḥiriq under the first bet.",
    ),
    dict(
        ref="Proverbs 12:9",
        # Ben, 2026-11-09: "No need to identify "second" in "on the second mem–tav", so please
        # remove it."  Ben, 2026-11-10: "Replace "the vowels of the hitpael participle's
        # prefix.", whose referent I find ambiguous, with a separate, parenthesized sentence
        # saying something like "(Unlike IB's vowels, the xiriq–sheva vowels of the consensus
        # make sense, being the vowels of the hitpael participle's prefix.)"", used as he gave it.
        note=(
            "IB has, on the mem–tav, sheva–pataḥ instead of ḥiriq–sheva. (Unlike IB's "
            "vowels, the ḥiriq–sheva vowels of the consensus make sense, being the vowels of "
            "the hitpael participle's prefix.)"
        ),
    ),
    dict(
        ref="2 Kings 18:27",
        label="Separate",
        # Ben, 2026-11-10: "Remove "rendering the word unpronounceable." Originally I allowed this
        # as an exception to my general policy of not commenting on pronunciation, but now it
        # seems to me to stick out as an exception, so let's remove it."
        note="IB has no tsere on the first mem of this qere.",
    ),
]

# Ben, 2026-11-08: "Don't separate out the table "Forms in verses that the Israel Bible
# transliterates", just throw its rows into the one big table and ditch its "transliteration
# follows" column".  Each note says what the transliteration follows.  Deuteronomy 2:9, which that
# table shared with the el/al group of NEXT, is now that group's alone.  Joshua 12:6 joined the
# Reubenite group of NEXT on 2026-11-09.
# Ben, 2026-11-08, of Joshua 12:6: "rather than vaguely citing both the alef-vav and vav-alef FOIs,
# cite specifically the relevant alef-vav FOI", and "introduce the question rafeh on alef (or lack
# thereof) into the discussion".  The alef-vav page's group d-alef-rafeh-shuruq holds 26 words with
# a quiescent alef just before a shuruq, the Reubenite words among them, none labeled "no rafeh";
# since 2026-11-09 the Reubenite group's note ends "See MAM's relevant FOI" with a link to it.
FOI = site_links.site_url("MAM-with-doc/foi/")
FOI_ALEF_FIRST = FOI + "foi-alef-dual-ml-alef-first.html"
FOI_ALEF_RAFEH_SHURUQ = FOI_ALEF_FIRST + "#intro-d-alef-rafeh-shuruq"
# Ben, 2026-11-09, of the Reubenite word: "which also appears in near-consensus form in IB [N]
# times. (By "near-consensus form" I mean with no qubuts, albeit with no rafeh either.)"  Of the 18
# Reubenite words, the Israel Bible has 12 so, and the six of REUVENI_REFS with the qubuts.  The
# count is authored, not computed here.
N_REUVENI_NEAR = 12
# Ben, 2026-11-09: "Yes, add it"; and later that day, in the Reubenite note, "See
# also" this word "at Job 31:7, below": mum, spelled with an alef, the one word besides the
# Reubenite words that has their notation in UXLC and in the tour.  Written by its letters' names.
MUM_WITH_ALEF = (
    "\N{HEBREW LETTER MEM}\N{HEBREW LETTER ALEF}\N{HEBREW LETTER VAV}"
    "\N{HEBREW LETTER FINAL MEM}"
)
# The Reubenite word, for Job 31:7's "See also" (Ben, 2026-11-09).  Written by its letters' names.
REUVENI = (
    "\N{HEBREW LETTER RESH}\N{HEBREW LETTER ALEF}\N{HEBREW LETTER VAV}"
    "\N{HEBREW LETTER BET}\N{HEBREW LETTER NUN}\N{HEBREW LETTER YOD}"
)
# Ben, 2026-11-08, of "the word written but not read": "use the "כתיב ולא קרי" or whatever the
# usual hebrew spelling of this phrase is".  Written by its letters' names, as MUM_WITH_ALEF is.
# Ben, 2026-11-08: "Regarding 2 Sam 15:21 and 2 Sam 13:33, are one or more of these the topic of
# my "saying the silent part out loud"? If so please link to it."  Both are: Part 2 of his series.
QUIET_PART = site_links.site_url(
    "MAM-with-doc/misc/urwotm_2_saying_the_quiet_part_out_loud.html"
)
KETIV_VELO_QERE = isolate_hebrew(
    "\N{HEBREW LETTER KAF}\N{HEBREW LETTER TAV}\N{HEBREW LETTER YOD}\N{HEBREW LETTER BET} "
    "\N{HEBREW LETTER VAV}\N{HEBREW LETTER LAMED}\N{HEBREW LETTER ALEF} "
    "\N{HEBREW LETTER QOF}\N{HEBREW LETTER RESH}\N{HEBREW LETTER YOD}"
)
TRANSLIT = [
    dict(
        ref="Daniel 2:45",
        # Ben, 2026-11-09: "Change <It transliterates this verse, and its transliteration,
        # v’-ha-DE-ket,> to <IB's transliteration, v’-ha-DE-ket,>"
        # Later that day Ben asked to remove the note's remark on IB's transliterations
        # elsewhere: "this reflects great work confirming IB's transliteration system, but we
        # don't need to "surface" this methodology to the reader".  The colon before it became a
        # period.
        note=(
            "IB has a segol under the dalet instead of a tsere. IB's transliteration, "
            "<i>v’-ha-DE-ket</i>, spells the syllable with "
            "<i>e</i>, its spelling of segol. So its transliteration follows its Hebrew here, "
            "not the consensus."
        ),
    ),
]

NEXT = [
    # Ben, 2026-11-09, of Hosea 2:17: "Change <IB has both a shuruq dot and a xiriq on the first
    # vav. ...> to <IB has an illegal/nonsensical hiriq below a shuruq>", with xiriq spelled as
    # elsewhere; of Jonah 3:2: "Change <IB has the same pattern as at Hos 2:17: ...> to have the
    # same wording I mentioned above, and cross-reference both of them."; "Change
    # "illegal/nonsensical" to just "nonsensical" wherever it is used."; and then: "For various
    # rows that are now cross-references, e.g. "IB has an illegal/nonsensical xiriq below a
    # shuruq, as at Jonah 3:2.", it occurs to me: why not move these rows next to each other and
    # do a "rowspan" single note, as we do in other cases?"  So the two verses are one group, at
    # Hosea 2:17, and their shared note needs no cross-reference.
    dict(
        refs=["Hosea 2:17", "Jonah 3:2"],
        note="IB has a nonsensical ḥiriq below a shuruq.",
    ),
    dict(
        refs=["Genesis 32:18"],
        note="IB has a ḥiriq instead of a shuruq dot.",
    ),
    dict(
        refs=["Genesis 34:11", "Isaiah 23:8", "Hosea 2:4", "Proverbs 31:12"],
        note="IB has a final he without qamats.",
    ),
    dict(
        refs=["Daniel 5:24"],
        # Ben, 2026-11-09: Remove "which gives the word an extra syllable." "since I've been
        # back-tracking on what I think was my original goal to explicitly point out pronunciation
        # implications of these quirks"; here and at Nehemiah 9:14.  Ben, 2026-11-10: "instead of
        # "IB has, on yod–xet, patax–patax instead of ∅–patax." couldn't we just say "IB has patax
        # under yod"", since only the yod differs.
        note="IB has pataḥ under yod.",
    ),
    dict(
        refs=["2 Samuel 11:1"],
        note=(
            "IB has, on mem–lamed, pataḥ–sheva instead of sheva–qamats: the "
            'vowels of "the messengers" instead of those of "the kings".'
        ),
    ),
    dict(
        refs=["Numbers 2:14", "Daniel 7:20"],
        note=("IB has a sheva instead of a shuruq dot."),
    ),
    dict(
        refs=["2 Samuel 13:33", "2 Samuel 15:21"],
        # Ben, 2026-11-09: "Sure, cut both": "; the consensus leaves it unpointed"
        # and ", where the consensus has none", which "IB has ..." implies.  Ben, 2026-11-10:
        # "Change "leaves such a word" to "leaves such a ... word"", the elided phrase being the
        # one that KETIV_VELO_QERE spells.
        note=(
            f"IB has a ḥiriq in a word that is {KETIV_VELO_QERE}, so a reader "
            "would be encouraged to read it aloud. Elsewhere "
            f"the Israel Bible leaves such a {KETIV_VELO_QERE} word unpointed (six places), "
            "with nothing else to "
            "mark it; it brackets only the qere words that it adds. At "
            "2&nbsp;Sam&nbsp;15:21 the Israel "
            "Bible also has a maqaf after it. These two words are "
            "the subject of my "
            + go(
                QUIET_PART,
                '"Saying the quiet part out loud"',
                "Undoing and redoing the work of the Masoretes, Part 2",
            )
            + "."
        ),
    ),
    dict(
        refs=["Exodus 1:3"],
        note=("IB has a sheva instead of a ḥiriq under the bet."),
    ),
    dict(
        refs=["Psalms 45:3"],
        note=("IB has a sheva instead of a ḥiriq under the sin."),
    ),
    dict(
        refs=["Judges 16:2"],
        note=("IB has a sheva instead of a pataḥ under the resh."),
    ),
    dict(
        refs=["Nehemiah 9:14"],
        # Ben, 2026-11-09: "Change "which gives the word an extra syllable, and no dagesh in the
        # tav." to "which gives the word an extra syllable. IB has no dagesh in the tav.""  Later
        # that day: Remove "which gives the word an extra syllable." (as at Daniel 5:24).
        note=(
            "IB has a pataḥ instead of a sheva under the ayin. IB has no dagesh in "
            "the tav."
        ),
    ),
    dict(
        refs=["Exodus 10:28", "Deuteronomy 2:9", "Joshua 22:19"],
        # On 2026-11-09 Ben asked to remove the note's count of IB's transliterations of these
        # atoms elsewhere: "(a great behind-the-scenes check that IB transliterates these words
        # consistently (other than this one case), but not needed (and not wanted by me) in the
        # final public-facing document)"
        note=(
            "IB has a segol instead of a pataḥ under the alef: the preposition "
            '"to" instead of the negative "do not". Judg 19:23 '
            "and Jer 47:6, below, have the reverse. The Israel Bible transliterates every verse "
            "that has "
            "a study note, 1,084 verses in all, Deut&nbsp;2:9 among them, and there its "
            "transliteration has <i>al</i> (<i>al ta-TZAR</i>, do not harass): it follows the "
            "consensus, against its own Hebrew."
        ),
    ),
    # Ben, 2026-11-08, of "Judg 19:23 and Jer 47:6 have the reverse": "so why not include them
    # in the table, as two more rows?"  Neither verse has a transliteration in the Israel Bible.
    dict(
        refs=["Judges 19:23", "Jeremiah 47:6"],
        note=(
            "IB has a pataḥ instead of a segol under the alef: the negative "
            '"do not" instead of the preposition "to", the reverse of Exod&nbsp;10:28, '
            "Deut&nbsp;2:9 and Josh&nbsp;22:19."
        ),
    ),
    dict(
        refs=["Zechariah 2:2"],
        # Ben, 2026-11-09: "Change "IB has Jerusalem without its (orphan) xiriq." to "IB has
        # Jerusalem-related word without its (orphan) xiriq."", with "the" before the word.  Ben,
        # 2026-11-10: "Remove parens from "(orphan)"."
        note="IB has the Jerusalem-related word without its orphan ḥiriq.",
    ),
    dict(
        refs=["1 Chronicles 3:1"],
        # Ben, 2026-11-09: "Change <IB has, on the vav–yod of David, ∅–xiriq instead of the
        # reverse.> to <IB has xiriq on yod rather than vav>", with a closing period.
        note="IB has ḥiriq on yod rather than vav.",
    ),
    dict(
        refs=["Isaiah 66:22"],
        note=(
            "IB has a ḥataf qamats instead of a ḥataf pataḥ under the ḥet, the "
            'vowel of "the months" instead of "the new".'
        ),
    ),
    # Ben, 2026-11-09: "Add the other 5 rows of "redundant qubuts-shuruq" spellings"; and later
    # that day: "Try to consolidate all ראובני cases, with something like: The Israel Bible not
    # only includes the LC's quirky qubuts, ..."  So the six Reubenite words with a qubuts under
    # the resh share one note, his, with its placeholders filled: the verse whose transliteration
    # it quotes, Joshua 12:6, and N_REUVENI_NEAR.  The note is whole, with no "Details": its cell
    # spans the group's twelve rows.  Ben, later that day: "Regarding "The Israel Bible not only
    # includes the LC's quirky qubuts", just use "IB", i.e. "IB not only includes the LC's quirky
    # qubuts"", here and at Job 31:7.
    dict(
        refs=REUVENI_REFS,
        # Ben, 2026-11-10: "Replace "general chaos" with "general confusing"", and, asked whether
        # he meant "general confusion": "Yes, confusion".
        note=isolate_hebrew(
            "IB not only includes the LC's quirky qubuts, it does so without the "
            "rafeh on alef that makes this quirk less confusing (though still confusing). Its "
            "transliteration of this word as <i>la-ru-vay-NEE</i> (in Josh&nbsp;12:6) is hard "
            "to justify against its Hebrew pointing. IB's 2&nbsp;Kgs&nbsp;10:33 form of this "
            "word lacks a dot in the vav; whether the word is more or less confusing this way "
            "is unclear. It certainly adds to the general confusion surrounding this word, which "
            f"also appears in near-consensus form in IB {N_REUVENI_NEAR} times. (By "
            '"near-consensus form" I mean with no qubuts, albeit with no rafeh either.) See '
            f"also {MUM_WITH_ALEF} at Job&nbsp;31:7, below. See "
            + go(
                FOI_ALEF_RAFEH_SHURUQ,
                "MAM's relevant FOI",
                "d-alef-rafeh-shuruq (MAM features of interest)",
            )
            + "."
        ),
    ),
    # Ben, 2026-11-09: "Add it too", of the word with the letters mem alef vav final mem at
    # Job 31:7 (MUM_WITH_ALEF), which has the Reubenite words' qubuts, alef, shuruq notation.
    # Ben, later on 2026-11-09: "Change "IB has a qubuts under the mem, ..." to be analogous to the
    # first sentence of the Reuveni analogies".  That sentence holds here word for word: the
    # Israel Bible's form has the qubuts and no rafeh on the alef, and MAM's has that rafeh.
    # Its cross-reference mirrors the Reubenite note's "See also ... at Job 31:7, below" (Ben:
    # "Why would you unidirectionally reference and not cross-reference?").
    dict(
        refs=["Job 31:7"],
        note=isolate_hebrew(
            "IB not only includes the LC's quirky qubuts, it does so without the "
            "rafeh on alef that makes this quirk less confusing (though still confusing). See "
            f"also {REUVENI} at Num&nbsp;26:7, above."
        ),
    ),
]

# Ben, 2026-11-09: "propose some thematic divisions of the current one huge "Sample of Quirks"
# table. With a healthy-sized "misc" section to avoid a lot of hand-wringing about categories."
# His answers that evening, to the divisions proposed: of the Reubenite words and Job 31:7, "make
# them their own section"; of that section's heading, "Call the section "Qubuts-alef-shuruq"";
# and of "each section gets an h3 heading over its own table", "I concur".  Each division is its
# heading and the verses of its rows, as the Where column names them but with plain spaces; a
# group that shares a note goes whole to one division, and Miscellaneous takes every row that
# meets no other division's criterion.
DIVISIONS = [
    (
        "Another word",
        [
            "Exod 10:28",
            "Deut 2:9",
            "Josh 22:19",
            "Judg 19:4",
            "Judg 19:23",
            "Jer 47:6",
            "2 Sam 11:1",
            "Isa 66:22",
        ],
    ),
    (
        "Two vowels on one letter",
        ["Deut 3:22", "Isa 49:23", "Lam 3:25", "Hos 2:17", "Jonah 3:2"],
    ),
    (
        "Missing vowels and dots",
        [
            "Gen 34:11",
            "Isa 23:8",
            "Hos 2:4",
            "Prov 31:12",
            "2 Kgs 18:27",
            "Isa 46:4",
            "Zech 2:2",
            "Prov 20:1",
            "Lam 4:4",
            "Eccl 2:23",
        ],
    ),
    (
        # Ben, 2026-11-10: "Change "A sheva instead of a vowel, or the reverse" to "A sheva
        # instead of a full vowel, or the reverse"", since "certainly no type of sheva is a full
        # vowel".  As he asked, each alternative to the sheva in these rows was checked: it is a
        # full vowel, a xiriq, a patax or a shuruq, and none is a xataf.
        "A sheva instead of a full vowel, or the reverse",
        [
            "Exod 1:3",
            "Num 2:14",
            "Dan 7:20",
            "Judg 15:14",
            "Judg 16:2",
            "1 Sam 27:10",
            "Joel 2:12",
            "Ps 45:3",
            "Prov 12:9",
            "Neh 9:14",
        ],
    ),
    (
        "Qubuts-alef-shuruq",
        [
            "Num 26:7",
            "Deut 3:12",
            "Deut 3:16",
            "Deut 4:43",
            "Josh 12:6",
            "2 Kgs 10:33",
            "Job 31:7",
        ],
    ),
    (
        "Miscellaneous",
        [
            "Gen 32:18",
            "2 Sam 13:33",
            "2 Sam 15:21",
            "Jer 3:17",
            "Song 5:11",
            "Dan 2:45",
            "Dan 5:24",
            "1 Chr 3:1",
        ],
    ),
]

# ---------------------------------------------------------------- page

# The page's styles are israel_bible_review_index.css beside this module, where the draft's
# inline styles went at the port.  Pointed Hebrew is in Taamey D (Ben, 2026-11-08), which that
# sheet loads from the site's one copy, gh-pages/woff2/Taamey_D.woff2, by a relative URL and
# with no local() source (doc/html-styles.md, "Hebrew font").


def stylesheet():
    """The page's stylesheet as gen_html_file publishes it: a banner naming this generator, as
    doc/html-styles.md asks of a generated sheet, then the source beside this module."""
    banner = "/* " + provenance.generated_html_comment(__file__) + " */"
    return banner + "\n" + _CSS_SOURCE.read_text(encoding="utf-8")


# Ben, 2026-11-08: "Actually in terms of transliterations let's just get out of the business of
# providing them altogether, rather than converting them to Phonetic MAM's form. Only discuss
# them when Israel Bible provides them, and in those cases of course use IB's transliteration
# scheme, not Phonetic MAM's."  So a note's italics quote only the Israel Bible's own
# transliterations as its pages print them, Daniel 2:45's on page 1875, Joshua 12:6's on page 571
# and Deuteronomy 2:9's on page 452, and its spellings in them.  The syllable highlighting of his
# earlier request went with the notes' own "X instead of Y" transliterations.
IB_TRANSLIT_QUOTES = {
    "v’-ha-DE-ket",
    "e",
    "la-ru-vay-NEE",
    "al",
    "al ta-TZAR",
}
ITALIC = re.compile(r"<i>([^<]+)</i>")


def checked_note(note):
    """The note, once its italics are found to quote only the Israel Bible's transliterations."""
    assert set(ITALIC.findall(note)) <= IB_TRANSLIT_QUOTES, note
    return note


def md_note_html(note, verse, footnotes):
    """A note of review.md's data table.  Ben, 2026-11-08: Deuteronomy 3:22's note is several
    paragraphs, and everything after its first sentence goes in "some sort of default-collapsed
    "Details" section".  A Markdown table cell is one line, so review.md separates paragraphs
    with <br><br> and marks the collapsed part with DETAILS_OPEN and DETAILS_CLOSE, both of which
    GitHub draws too; no other markup may appear in a note.  A footnote reference in it is
    numbered at once when footnotes is True and otherwise left for review_html (data_items says
    why)."""

    def paras(s):
        ps = s.split("<br><br>")
        assert all(
            p and "<" not in p.replace("<i>", "").replace("</i>", "") for p in ps
        ), (
            verse,
            s,
        )
        return "<br><br>".join(inline(p, footnotes) for p in ps)

    head, sep, rest = note.partition(DETAILS_OPEN)
    if not sep:
        return paras(note)
    assert rest.endswith(DETAILS_CLOSE), verse
    body = rest[: -len(DETAILS_CLOSE)]
    return f"{paras(head)}<details><summary>Details</summary>{paras(body)}</details>"


def data_table_rows(lines, headers):
    """The body rows of review.md's one data table with these headers, each the list of its
    cells, review.md being given as its lines."""
    head_ = "| " + " | ".join(headers) + " |"
    assert lines.count(head_) == 1, head_
    k = lines.index(head_)
    block = []
    while k < len(lines) and lines[k].startswith("|"):
        block.append(lines[k])
        k += 1
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in block]
    assert all(c and set(c) <= set("-:") for c in rows[1]), rows[1]
    return rows[2:]


def tour_md_items(lines):
    """review.md's rows for the tour's tables, from its data table with TOUR_ROW_HEADERS, as
    data_items draws them."""
    return data_items(data_table_rows(lines, TOUR_ROW_HEADERS))


def decalogue_table(body, flat):
    """review.md's Decalogues table, from its data table with DECALOGUE_ROW_HEADERS, drawn where
    it stands as the tour's tables are drawn (Ben, 2026-11-09: "like a small version of the
    "sampling of quirks" table"), its groups in the Israel Bible's order.  Its lead's count of
    rows is kept true here, as the tour's is, in review.md as flat (review_flat) gives it.
    """
    # Ben, 2026-11-10, of the footnote for Deut 5:13: "Approve as recommended".
    items = data_items(body, footnotes=True)
    keys = [item[0] for item in items]
    assert keys == sorted(keys), [item[2] for item in items]
    n_rows = sum(len(item[2].split(", ")) for item in items)
    # Ben, 2026-11-09: "Change "the Israel Bible's form is shown above MAM's form in the עליון" to
    # "the Israel Bible's form is shown above MAM's עליון form"", which now ends its sentence.
    lead = (
        f"In each of the {n_rows} rows below, the Israel Bible's form is shown above MAM's "
        f"{ELYON} form."
    )
    assert lead in flat, n_rows
    return table(["Forms", "Where", "Notes"], [tr for item in items for tr in item[3]])


def data_items(body, footnotes=False):
    """A data table's rows, each a (reading key, short book name, verses, <tr>s) item, the Israel
    Bible's form above MAM's, as in candidate_rows, with the verse and page, but no arrow, in the
    Where cell.  A row whose Note cell is empty shares the note of the row above it, as the verses
    of a NEXT group share theirs (Ben, 2026-11-09: "why not move these rows next to each other and
    do a "rowspan" single note, as we do in other cases?"), and the group stands at its first row,
    which comes first in the Israel Bible's order.  Any note may refer to a footnote, numbered in
    reading order: decalogue_table runs where its table stands in review_html, after the
    opening's notes are numbered, and numbers its notes' references at once (footnotes=True),
    while the tour's data table is drawn before review_html runs, so its notes' references are
    left for review_html to number where the tour's tables stand (footnotes=False).  Ben,
    2026-11-10, of Deut 3:22's parenthesis on the ḥataf ḥiriq: "make it a footnote rather than
    normal body text"."""
    groups = []
    for verse, page, ib, cons, note in body:
        if note:
            groups.append((note, []))
        assert groups, verse
        groups[-1][1].append((verse, page, ib, cons))
    items = []
    for note, members in groups:
        keys = []
        trs = []
        for j, (verse, page, ib, cons) in enumerate(members):
            m = re.fullmatch(r"(.+) (\d+):(\d+)", verse)
            assert m and m.group(1) in SHORT.values(), verse
            keys.append(((int(page), int(m.group(2)), int(m.group(3))), m.group(1)))
            us = [units(stripped(ib)), units(stripped(cons))]
            assert [unit_key(u) for u in us[0]] != [unit_key(u) for u in us[1]], verse
            for i, (u, h) in enumerate(zip(us, hot_units(us))):
                first = " first" if i == 0 else ""
                cells = f'<td dir="rtl" class="form{first}">{form_html(u, h)}</td>'
                if i == 0:
                    where = (
                        f"{html.escape(verse.replace(' ', NBSP))}<br>page {int(page)}"
                    )
                    cells += spanning("bcv", N_SHOWN, where)
                if i == 0 and j == 0:
                    cells += spanning(
                        "note",
                        N_SHOWN * len(members),
                        checked_note(md_note_html(note, verse, footnotes)),
                    )
                trs.append(f"<tr>{cells}</tr>")
        assert keys == sorted(keys), [v for v, *_rest in members]
        verses = ", ".join(v for v, *_rest in members)
        items.append((keys[0][0], keys[0][1], verses, trs))
    return items


def tour_items(rows, lines):
    """Every row of the tour, in the Israel Bible's order, as its one table held them (Ben,
    2026-11-08) until DIVISIONS divided them (Ben, 2026-11-09): the TOP and TRANSLIT entries, the
    NEXT groups, each at its first verse (a group that shares a note stays together), and
    review.md's rows.  `rows` are forms.json's (forms) and `lines` review.md's.  Chapter and verse
    break a tie of pages only within one book, and no verse has two rows.  Closed dispatch: an
    entry of TOP, TRANSLIT or NEXT with no row of forms.json, two entries with one row, or a row
    that no entry draws raises."""
    by_key = {(row["reference"], row.get("label")): row for row in rows}
    assert len(by_key) == len(rows), sorted(by_key)
    drawn = set()

    def row_of(ref, label=None):
        """The row of forms.json for an entry's verse and its label, if TOP gives one."""
        if (ref, label) not in by_key:
            raise ValueError(f"no row of forms.json for {ref!r} with label {label!r}")
        if (ref, label) in drawn:
            raise ValueError(f"two entries draw the row for {ref!r}")
        drawn.add((ref, label))
        return by_key[(ref, label)]

    items = []
    for x in TOP + TRANSLIT:
        r = row_of(x["ref"], x.get("label"))
        trs = candidate_rows(r, spanning("note", N_SHOWN, checked_note(x["note"])))
        book_ = SHORT[bcv(r["reference"])[0]]
        items.append((reading_key(r), book_, short_ref(r["reference"]), trs))
    for x in NEXT:
        rs = [
            r for _ref, r in in_reading_order([(ref, row_of(ref)) for ref in x["refs"]])
        ]
        trs = []
        for i, r in enumerate(rs):
            note = (
                spanning("note", N_SHOWN * len(rs), checked_note(x["note"]))
                if i == 0
                else ""
            )
            trs += candidate_rows(r, note)
        refs = ", ".join(short_ref(r["reference"]) for r in rs)
        items.append((reading_key(rs[0]), SHORT[bcv(rs[0]["reference"])[0]], refs, trs))
    undrawn = sorted(set(by_key) - drawn)
    if undrawn:
        raise ValueError(f"rows of forms.json that no entry draws: {undrawn}")
    items += tour_md_items(lines)
    verses = [
        v.replace(NBSP, " ") for _k, _b, refs, _t in items for v in refs.split(", ")
    ]
    assert len(verses) == len(set(verses)), sorted(verses)
    items.sort(key=lambda it: it[0])
    for a, b in zip(items, items[1:]):
        if a[0][0] == b[0][0]:
            assert a[1] == b[1], (a[2], b[2])
    return items


def tour_divisions(items):
    """The tour's items in DIVISIONS' divisions, as [(heading, items)] in DIVISIONS' order, each
    division's items in the order of `items`.  Closed dispatch: a heading or verse that DIVISIONS
    names twice, a verse in no division, a group whose verses fall in two divisions, a verse of
    DIVISIONS that no item has, or an empty division raises."""
    headings = [heading for heading, _verses in DIVISIONS]
    named = [v for _heading, verses in DIVISIONS for v in verses]
    if len(headings) != len(set(headings)) or len(named) != len(set(named)):
        raise ValueError(
            f"DIVISIONS names a heading or verse twice: {headings}, {named}"
        )
    division_of = {v: heading for heading, verses in DIVISIONS for v in verses}
    parts = {heading: [] for heading in headings}
    shown = set()
    for item in items:
        verses = [v.replace(NBSP, " ") for v in item[2].split(", ")]
        unnamed = [v for v in verses if v not in division_of]
        if unnamed:
            raise ValueError(f"verses in no division: {unnamed}")
        found = {division_of[v] for v in verses}
        if len(found) != 1:
            raise ValueError(f"a group in two divisions: {verses}, {sorted(found)}")
        parts[found.pop()].append(item)
        shown.update(verses)
    missing = sorted(set(named) - shown)
    if missing:
        raise ValueError(f"verses of DIVISIONS on no row: {missing}")
    empty = [heading for heading in headings if not parts[heading]]
    if empty:
        raise ValueError(f"empty divisions: {empty}")
    return [(heading, parts[heading]) for heading in headings]


NBSP = "\N{NO-BREAK SPACE}"


def review_flat(lines):
    """review.md's text with each run of spaces and line breaks, a note's indentation included,
    as one space, review.md being given as its lines."""
    return " ".join(" ".join(lines).split())


def body_html():
    """The page's body: review.md as HTML, with the tour's tables in place of its marker."""
    FOOTNOTE_NUMBERS.clear()
    lines = review_lines()
    assert lines[0] == f"# {_TITLE}", lines[0]
    flat = review_flat(lines)
    # Ben, 2026-11-08: one big table, under the review's own "A sampling of quirks" and the lead
    # that review.md gives it, with no heading or introduction of its own.  Since Ben's
    # divisions of 2026-11-09 (DIVISIONS), its rows stand in six tables, each under its
    # division's heading.
    tour = tour_items(forms(), lines)
    # Ben, 2026-11-08: "In each of the N rows below".  review.md's lead states the count, and
    # this keeps it true: one row per verse, a group that shares a note counting each of its
    # verses.
    n_rows = sum(len(refs.split(", ")) for _k, _b, refs, _t in tour)
    assert f"In each of the {n_rows} rows below," in flat, n_rows
    # Ben, 2026-11-08: "a diplomatic presentation that never expresses any surprise and/or doubt
    # just makes no sense"; and, 2026-11-09, of the opening's paragraph that says so: "Yes, add
    # it".  Later that day the paragraph moved into the note on WLC's quality ("Also include
    # the "Worse ..." paragraph in that (rather large) footnote"), which stands after the tables
    # and so names their section rather than saying "below".  Its word count is the tables',
    # kept true here.  Its other counts are authored, not computed here, and must be recounted
    # whenever the rows change.
    assert f'Of the {n_rows} words sampled in "A sampling of quirks",' in flat, n_rows
    # Ben's divisions of 2026-11-09: every row in exactly one division.
    divisions = tour_divisions(tour)
    assert (
        sum(len(item[2].split(", ")) for _heading, part in divisions for item in part)
        == n_rows
    ), [(heading, len(part)) for heading, part in divisions]
    # Ben, 2026-11-09, to "each section gets an h3 heading over its own table": "I concur".
    # Each heading is drawn as review_html draws review.md's own, with no id, and nothing
    # stands between it and its table, the old section's introduction having gone at Ben's
    # word.  Each table has the one table's header row and sizes its columns to its own rows.
    section = "".join(
        f"<h3>{inline(heading)}</h3>\n"
        + table(["Forms", "Where", "Notes"], [tr for *_rest, trs in part for tr in trs])
        for heading, part in divisions
    )
    return explain_abbreviations(review_html(lines, flat, section))


def gen_html_file():
    """Write the page and its stylesheet into the review's folder, and return the page's
    path."""
    body = body_html()
    with open(_OUT_DIR / _CSS_FNAME, "w", encoding="utf-8", newline="\n") as out_fp:
        out_fp.write(stylesheet())
    cbody = [mb_html.raw_html(body)]
    fname, _title = author.help_gen_html_file(
        __file__, (_OUT_DIR, _CSS_HREFS), _FNAME, _TITLE, cbody, viewport=True
    )
    return _OUT_DIR / fname
