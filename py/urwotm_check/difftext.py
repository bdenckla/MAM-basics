"""The differential verifier: frozen source text vs. generated page.

This is the check that outlived the urwotm importer (#209 item 6), and it is
the shape of test that has actually paid in these repos -- a differential
check against an independent oracle, not an example pinned by hand. Four
real defects surfaced here during the port.

* **Oracle A** is ``src/urwotm_N.gdoc.txt``: the words of the published
  Google document, frozen into the tree. It was produced from the pinned
  ``/pub`` snapshot of 2026-07-26 by ``4d8d181``'s ``fetch.py`` and the
  ``source_words()`` that stood here then -- Google's own publish chrome
  dropped, the whole ``doc-content`` div normalized and split into words.
  Both are in git history if the derivation ever needs re-reading.
* **Oracle B** is the *generated* ``MAM-with-doc`` page through the identical
  normalizer.

Oracle B is deliberately taken after ``dollar_sub`` has run, so ``$qadma``
has already become the text "qadma". A dollarization mistake therefore shows
up as an ordinary word-level difference instead of being invisible to a
check that compared Python sources.

Oracle A is frozen on purpose: it is what the pages were ported from, and
re-deriving it would let an upstream edit to a Google Doc silently redefine
what the pages are being checked against. A deliberate change to a page is
recorded in ``expected_divergences.py``, never by re-vendoring.
"""

import difflib

import lxml.html

from mb_cmn import paths
from urwotm_check import expected_divergences
from urwotm_check import normalize
from urwotm_check import parts

_CONTEXT = 8

# Elements after which a word break exists whether or not any whitespace was
# written. Google's published HTML is minified, so without this the last word
# of a paragraph and the first of the next fuse into one ("below:לֵאמֹ֨ר")
# and every paragraph boundary reads as a difference. The generated pages are
# read the same way, so the two sides stay comparable.
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


def vendored_words(part: int):
    """Oracle A: the frozen words of the published document, one per line."""
    text = parts.src_path(part).read_text(encoding="utf-8")
    return text.split()


def generated_words(part: int):
    """Oracle B: the words of the page this repo now generates."""
    from author_misc import urwotm_common

    path = (
        paths.repo_root()
        / "gh-pages"
        / "MAM-with-doc"
        / "misc"
        / urwotm_common.FNAMES[part]
    )
    doc = lxml.html.fromstring(path.read_text(encoding="utf-8"))
    body = doc.xpath("//body")
    assert len(body) == 1, len(body)
    return normalize.words(_block_separated_text(body[0]))


def unexpected_lines(part: int):
    """The differences not in ``expected_divergences``, as report lines.

    Empty when the page agrees with its source, which is the whole verdict:
    a caller asserts on emptiness and prints what it got.
    """
    a = vendored_words(part)
    b = generated_words(part)
    allowed = expected_divergences.for_part(part)
    lines = []
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        got = " ".join(a[i1:i2])
        want = " ".join(b[j1:j2])
        if expected_divergences.match(allowed, tag, got, want) is not None:
            continue
        lines += _opcode_lines(a, tag, i1, i2, got, want)
    if not lines:
        return []
    return [
        f"Part {part}: {len(a)} words in the frozen source,"
        f" {len(b)} in the generated page.",
        "",
        *lines,
    ]


###########################################################


def _opcode_lines(a, tag, i1, i2, got, want):
    before = " ".join(a[max(0, i1 - _CONTEXT) : i1])
    after = " ".join(a[i2 : i2 + _CONTEXT])
    return [
        f"UNEXPECTED -- {tag}",
        f"  context: ...{before} [HERE] {after}...",
        f"  source: {got!r}",
        f"  page:   {want!r}",
        "",
    ]


def _block_separated_text(element) -> str:
    """``text_content()``, but with a space at every block boundary."""
    for tag in _BLOCK_TAGS:
        for el in element.iter(tag):
            el.tail = (el.tail or "") + " "
            el.text = " " + (el.text or "")
    return element.text_content()
