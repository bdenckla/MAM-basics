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
`Exod`, `Jer`, `Josh`, `Num` — and the same five less `Num` for Sefaria. The change
removed 24.3 MB of near-duplicate files, taking the product from 63.3 MB to 39.0 MB.

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
- Narpas (narrow-sense paseq, ׀) forms no compound of any kind; only maqaf joins atoms
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

Nothing beyond the standard library is needed. This program writes the plain text of
Job 34 to a file, and it handles every element type MAM-simple has:

```python
import xml.etree.ElementTree as ET

# Elements whose children are alternatives rather than a stretch of running text.
_CHOOSE = {"kq": "kq-q", "cant-all-three": "cant-combined", "scrdfftar": "sdt-target"}
_SKIP = ("good-ending",)  # a repetition after the last verse, not running text


def element_text(el):
    """The plain text of one element, assembled recursively."""
    if "text" in el.attrib:  # a text attribute and children never co-occur
        return el.attrib["text"]
    chosen = _CHOOSE.get(el.tag)
    if chosen is not None:
        return element_text(el.find(chosen))
    return "".join(element_text(k) for k in el if k.tag not in _SKIP)


def verses_of(xml_path):
    """Yield (osisID, plain text) for each verse of one MAM-simple XML file."""
    for book39 in ET.parse(xml_path).getroot():
        if book39.tag != "book39":
            continue  # a parashah marker between books
        for chapter in book39:
            if chapter.tag != "chapter":
                continue  # a parashah marker between chapters
            for verse in chapter:
                if verse.tag != "verse":
                    continue  # a parashah marker between verses
                yield verse.attrib["osisID"], element_text(verse)


def main():
    with open("py-examples-out/job-34.txt", "w", encoding="utf-8") as out:
        for osis_id, text in verses_of("xml-vtrad-mam/Job.xml"):
            if osis_id.startswith("Job.34."):
                out.write(f"{osis_id}: {text}\n")
```

Three points in it are easy to get wrong:

- **The recursion is not optional.** Plain text sits below `<kq>`, `<slh-word>` and
  others, so a walk that reads only the `<text>` children of a verse drops every
  ketiv/qere and every suspended-letter word, and drops them silently.
- **`_CHOOSE` picks among alternatives.** Concatenating the children of `<kq>` would
  give you the ketiv and the qere run together. Which child to choose is the caller's
  decision; `kq-q` above is one reasonable answer, not the only one.
- **Write non-ASCII to a file, not to stdout.** On Windows, Python encodes a redirected
  stdout with the locale code page, and printing Hebrew there raises
  `UnicodeEncodeError`. If you do want it on stdout, call
  `sys.stdout.reconfigure(encoding="utf-8")` first.

For the element and attribute names the program relies on, see
[the XML format](reading-mam-simple-xml.md).

## The `py-examples/` Program, and the Two That Were Retired

The `py-examples/` directory contains one complete working example:

<!-- sync: bullet list of example programs also appears in README.md -->
- **[`main_letter_small_job_example.py`](../py-examples/main_letter_small_job_example.py)** — reports all of the `<letter-small>` elements in `Job.xml`, writing output to `py-examples-out/letter-small-job.txt`.

It iterates directly over XML elements, without the handler pattern described below.

Two further examples, `main_mam4sef_example.py` and `main_mam_osis_example.py`, were
retired on 2026-09-12. They created the Sefaria and OSIS editions of MAM from this
product — the first from the JSON format, the second from the XML format — and they were
written when MAM-simple, MAM-for-Sefaria and MAM-OSIS were separate repositories. Both
editions are still produced, by MAM-basics' own `py/main_mam4sef.py` and
`py/main_mam_osis.py`, which read this product exactly as the retired examples did.

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
