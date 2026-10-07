# Reading MAM-simple

This document describes the XML and JSON formats used in MAM-simple and how to extract text from them.

## File Layout

<!-- sync: folder table also appears in README.md -->
folder | format | versification
---- | ---- | ----
`xml-vtrad-bhs` | XML | BHS
`xml-vtrad-sef` | XML | Sefaria
`xml-vtrad-mam` | XML | MAM native
`json-vtrad-bhs` | JSON | BHS
`json-vtrad-sef` | JSON | Sefaria
`json-vtrad-mam` | JSON | MAM native

Each file is named for one `book24` (e.g., `1Sam-2Sam.xml`, `Gen.xml`, `Hos-Mal.xml`).
A `book24` corresponds to one of the 24 books of the Hebrew Bible; some of them span more than one `book39`, i.e. some of them span more than one book in the system that divides the Hebrew Bible up into 39 rather than 24 books.

### The BHS and Sefaria folders are incremental, with the MAM ones as the base

Since 2026-09-12, the two `-vtrad-mam` folders hold all 24 book-group files and the four
others hold only the book groups whose cv-labels that versification places somewhere
other than where MAM places them. That is six of the 24 for BHS — `1Sam-2Sam`, `Deut`,
`Exod`, `Jer`, `Josh`, `Num` — and the same five less `Num` for Sefaria. The incremental-folder
deletion removed 24.3 MB on 2026-09-12. The same commit removed another 1.3 MB by dropping
`yeivinID` from the 48 MAM files, taking the product from 63.3 MB to 37.6 MB.

**To read book group `X` in versification `V`: read `<fmt>-vtrad-<V>/X`, and if it is not
there, read `<fmt>-vtrad-mam/X` instead.** In Python, that is one `try`:

```python
from pathlib import Path


def book_group_path(fmt: str, vtrad: str, stem: str) -> Path:
    """The file to read for one book group in one versification.

    fmt is "xml" or "json"; vtrad is "mam", "bhs" or "sef"; stem is a book24
    name such as "Gen" or "1Sam-2Sam".
    """
    suffix = "." + fmt
    asked = Path(f"{fmt}-vtrad-{vtrad}") / (stem + suffix)
    if asked.exists():
        return asked
    return Path(f"{fmt}-vtrad-mam") / (stem + suffix)
```

Every cv-label and every byte of text in the file the fallback returns is what
versification `V` calls for, which is exactly why it is not stored twice. **And the file
says so itself**: its root's `versification-tradition` holds a comma-separated set naming
every tradition it is correct for, so a `Ruth` read this way says
`versification-tradition="vtmam,vtbhs,vtsef"` and a `Num` says
`versification-tradition="vtmam,vtsef"`. A reader can therefore check the file it landed
on rather than trust the fallback rule — see
[the XML guide's root element](reading-mam-simple-xml.md#xml-element-hierarchy).

For a full description of where and how the three versifications differ, see [Versification Differences](versification-differences.md).

## Consumer notice

MAM-simple is a projected extract of MAM, not a complete representation of the
MAM-parsed source. Every JSON file embeds a `consumer_notice` immediately after its
`provenance` field, and every XML file places the same structured notice in a comment
before the `<book24>` root. The notice points back to this section.

The following rules protect distinctions that a generic tree walk would erase:

- Use the incremental-folder fallback above. An absent BHS or Sefaria book-group file
  is not an absent book.
- Dispatch explicitly on every documented element role and fail on an unknown element.
  Choose one branch where alternatives remain, including `<kq>` and
  `<cant-all-three>`; do not concatenate alternatives, a `<scrdfftar>` target with its
  note, or a `<good-ending>` repetition with running text. MAM-simple has already
  resolved or removed some choices retained by MAM-parsed, so absence here does not
  establish absence in MAM-parsed.
- The children of `<slh-word>` spell one atom-form. Its `slhw-desc-0` attribute repeats
  the uninterrupted atom-form without the letter formatting; the attribute is not
  additional Scripture.
- Select the required Scripture branches and reassemble adjacent fragments in source
  order before segmentation. An atom is one written form between spaces or maqafs. A
  chanted word is one atom or a complete maqaf compound. A template, fragment,
  punctuation, or structural-node boundary defines neither unit; in particular, a
  separate `<lp-legarmeih>` or `<lp-paseq>` node represents a mark that belongs with
  the preceding atom.
- Narpas (narrow-sense paseq, מ:פסק) forms no compound of any kind; only maqaf joins atoms
  into a chanted word. MAM encodes no text whitespace before or after narpas to avoid
  prescribing display spacing, not to group the surrounding text. An edition decides
  whether to display spacing before and/or after narpas; an analytical consumer need
  not make a display-spacing decision.
- The free parashah marker and the adjacent `starts-with-sampe` and
  `ends-with-sampe` attributes describe one break. Do not count the same break three
  times.
- MAM stores Hebrew combining marks in MAM order, not Unicode-normal order. A literal
  search using normalized input can miss equivalent-looking MAM text, and normalization
  can change bytes. Preserve MAM order when a byte-for-byte round trip or MAM-compatible
  output is required; a consumer with a different output contract may transform both
  sides deliberately.

## Format Details

- **[XML format](reading-mam-simple-xml.md)** — element hierarchy, verse text storage, child element types, verse attributes, and versification attributes.
- **[JSON format](reading-mam-simple-json.md)** — JSON object structure mirroring the XML hierarchy.

## Reading MAM-simple from Python

Nothing beyond the standard library is needed. Run from the MAM-simple directory, this
program writes the plain text of Job 34 to `py-examples-out/job-34.txt`. It handles only
the elements Job 34 has, and raises on any other rather than guess:

```python
import xml.etree.ElementTree as ET

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"

# What each element of Job 34 other than <text> contributes to a verse's plain text.
# This program handles only the elements Job 34 has, and raises on any other.
_CONTRIBUTION = {
    "lp-legarmeih": PASEQ,  # the text after it starts with a space
    "implicit-maqaf": MAQAF,  # MAM's gray maqaf, with no space on either side
}


def verse_text(verse):
    """The plain text of one verse of Job 34."""
    if "text" in verse.attrib:  # a text attribute and children never co-occur
        return verse.attrib["text"]
    parts = []
    for el in verse:
        if el.tag == "text":
            parts.append(el.attrib["text"])
        elif el.tag in _CONTRIBUTION:
            parts.append(_CONTRIBUTION[el.tag])
        else:
            raise ValueError(f"{verse.attrib['osisID']}: unhandled <{el.tag}>")
    return "".join(parts)


def main():
    book = ET.parse("xml-vtrad-mam/Job.xml")
    chapter = book.find("book39/chapter[@osisID='Job.34']")
    with open("py-examples-out/job-34.txt", "w", encoding="utf-8") as out:
        for verse in chapter:
            if verse.tag != "verse":
                raise ValueError(f"Job.34: unhandled <{verse.tag}>")
            out.write(f"{verse.attrib['osisID']}: {verse_text(verse)}\n")


if __name__ == "__main__":
    main()
```

Two points in it are easy to get wrong:

- **An element without text can still contribute.** `<lp-legarmeih>` contributes the
  glyph U+05C0, and `<implicit-maqaf>` MAM's gray maqaf as an ordinary maqaf. MAM
  encodes no space around `<implicit-maqaf>`, so a program that gives it nothing runs
  two atoms together: Job 34:10 would read שִׁמְע֫וּלִ֥י instead of שִׁמְע֫וּ־לִ֥י.
- **Write non-ASCII to a file, not to stdout.** On Windows, Python encodes a redirected
  stdout with the locale code page, and printing Hebrew there raises
  `UnicodeEncodeError`. If you do want it on stdout, call
  `sys.stdout.reconfigure(encoding="utf-8")` first.

To read another chapter, add a branch for each element the program raises on;
[Extracting the plain text of a verse](reading-mam-simple-xml.md#extracting-the-plain-text-of-a-verse)
says which elements need recursion and which hold alternatives to choose among.

## The `py-examples/` Program, and the Two That Were Retired

The `py-examples/` directory contains one complete working example:

<!-- sync: bullet list of example programs also appears in README.md -->
- **[`main_letter_small_job_example.py`](../py-examples/main_letter_small_job_example.py)** — reports all of the `<letter-small>` elements in `Job.xml`, writing output to `py-examples-out/letter-small-job.txt`.

It iterates directly over XML elements, without the handler pattern described below.

Two further examples, `main_mam4sef_example.py` and `main_mam_osis_example.py`, were
retired on 2026-09-12. They created the Sefaria and OSIS editions of MAM from this
product — the first from the JSON format, the second from the XML format — and they were
written when MAM-simple, MAM-for-Sefaria and MAM-OSIS were separate repositories. Both editions
are still produced by MAM-basics' `py/main_mam4sef.py` and `py/main_mam_osis.py`. Both generators
follow the incremental-folder rule above: read the requested versification file when present and
the MAM file otherwise.

## The Recursive Handler Pattern

The Sefaria and OSIS generators both use a recursive handler pattern, in which each
element type has a registered handler function. It remains the fullest worked answer to
"how do I process the full range of MAM-simple element types", so it is described here,
and the modules named are in
[MAM-basics](https://github.com/bdenckla/MAM-basics) rather than in this product.

For the Sefaria generator the relevant modules are:

- **`py/mb_sefaria/mam4sef_or_ajf.py`** — reads JSON, walks the tree with `_handle()`
- **`py/mb_sefaria/mam4sef_handlers.py`** — handler functions for every element type, keyed by `(tag, class)` tuple

The OSIS generator uses the same pattern over XML elements, with handler
functions in `py/osis/osis_handlers.py` and the walk itself in
`py/osis/osis_runner.py`. Its `_handle()` is where to look to see the pattern
whole. It processes one element by first processing that element's children, and then
calling the element's handler with three arguments:

- `etel` — the element itself
- `ofc1` — output for all children, summed together
- `ofc2` — output for all children, per child

When the element has a `text` attribute, `ofc1` is that attribute instead, which works
because a `text` attribute and children never co-occur. Handlers are keyed by
`(tag, class)`, so `("kq", "sep-maqaf")` gets a different handler from `("kq", None)`.
The `ofc2` argument is what lets a handler choose among its children rather than take
them all: `<scrdfftar>`'s handler uses it to tell the target from the note.

Together, MAM-basics' Sefaria and OSIS generators are the canonical
reference for how to process the full range of MAM-simple element types.
