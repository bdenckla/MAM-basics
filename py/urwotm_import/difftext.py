"""The differential verifier: source Google Doc vs. generated page.

This is the check that survives the emitter (the plan's Phase 8 keeps it),
and it is the shape of test that has actually paid in these repos -- a
differential check against an independent oracle, not an example pinned by
hand.

* **Oracle A** is the pinned Google ``/pub`` snapshot, with Google's own
  publish chrome dropped, normalized and split into words.
* **Oracle B** is the *generated* ``MAM-with-doc`` page through the identical
  normalizer.

Oracle B is deliberately taken after ``dollar_sub`` has run, so ``$qadma`` has
already become the text "qadma". A dollarization mistake therefore shows up
as an ordinary word-level difference instead of being invisible to a check
that compared Python sources.
"""

import difflib

import lxml.html

from mb_cmn import paths
from urwotm_import import expected_divergences
from urwotm_import import normalize

# Google appends its own banner to every published document.
_GOOGLE_CHROME = ("Published using Google Docs", "Report abuse", "Learn more")

_CONTEXT = 8

# Elements after which a word break exists whether or not any whitespace was
# written. Google's published HTML is minified, so without this the last word
# of a paragraph and the first of the next fuse into one ("below:לֵאמֹ֨ר")
# and every paragraph boundary reads as a difference.
_BLOCK_TAGS = (
    "p",
    "li",
    "ul",
    "ol",
    "div",
    "br",
    "tr",
    "td",
    "th",
    "table",
    "blockquote",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
)


def source_words(html: str):
    """Oracle A: the words of the published document itself."""
    doc = lxml.html.fromstring(html)
    content = doc.xpath("//div[contains(@class, 'doc-content')]")
    assert len(content) == 1, len(content)
    for bad in content[0].xpath(".//style | .//script"):
        bad.getparent().remove(bad)
    # div#title and div#subtitle are Google's banner copies of paragraphs that
    # are already inside doc-content; counting both would double the title.
    return normalize.words(_drop_chrome(_block_separated_text(content[0])))


def generated_words(part: int):
    """Oracle B: the words of the page this repo now generates."""
    from author_misc import urwotm_common

    path = (
        paths.sibling_repo("MAM-with-doc")
        / "gh-pages"
        / "misc"
        / urwotm_common.FNAMES[part]
    )
    doc = lxml.html.fromstring(path.read_text(encoding="utf-8"))
    body = doc.xpath("//body")
    assert len(body) == 1, len(body)
    return normalize.words(_block_separated_text(body[0]))


def diff_report(part: int, html: str):
    """Every non-equal opcode, and whether it is allowed. (lines, ok)."""
    a = source_words(html)
    b = generated_words(part)
    allowed = expected_divergences.for_part(part)
    lines = [
        f"# Part {part}: source vs. generated",
        "",
        f"{len(a)} words in the Google Doc, {len(b)} in the generated page.",
        "",
    ]
    unexpected = 0
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        got = " ".join(a[i1:i2])
        want = " ".join(b[j1:j2])
        why = expected_divergences.match(allowed, tag, got, want)
        if why is None:
            unexpected += 1
        lines += _opcode_lines(a, tag, i1, i2, got, want, why)
    if unexpected == 0:
        lines += ["All differences are in `expected_divergences.py`.", ""]
    lines.insert(3, f"**{unexpected} unexpected difference(s).**")
    return lines, unexpected == 0


###########################################################


def _opcode_lines(a, tag, i1, i2, got, want, why):
    before = " ".join(a[max(0, i1 - _CONTEXT) : i1])
    after = " ".join(a[i2 : i2 + _CONTEXT])
    head = "## OK" if why else "## UNEXPECTED"
    return [
        f"{head} -- {tag}",
        "",
        f"- context: ...{before} **[here]** {after}...",
        f"- doc: `{got}`",
        f"- page: `{want}`",
        *([f"- allowed: {why}"] if why else []),
        "",
    ]


def _block_separated_text(element) -> str:
    """``text_content()``, but with a space at every block boundary."""
    for tag in _BLOCK_TAGS:
        for el in element.iter(tag):
            el.tail = (el.tail or "") + " "
            el.text = " " + (el.text or "")
    return element.text_content()


def _drop_chrome(text: str) -> str:
    for marker in _GOOGLE_CHROME:
        text = text.replace(marker, " ")
    return text
