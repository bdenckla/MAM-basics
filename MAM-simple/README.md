# MAM-simple
This product contains a version of MAM that is simple but not complete.
(See [MAM-parsed](../MAM-parsed/README.md) for complete versions).
Its source is MAM's Hebrew Wikisource text, through the Wikisource-derived
`MAM-parsed/plus/` product in this repository.
This product's simple version of MAM is available in both XML and JSON formats.
Each of these two formats is, in turn, available in three versifications.
This yields a total of six flavors of MAM-simple:

<!-- sync: folder table also appears in doc/reading-mam-simple.md ##File-Layout -->
folder | format | versification
---- | ---- | ----
`xml-vtrad-bhs` | XML | BHS
`xml-vtrad-sef` | XML | Sefaria
`xml-vtrad-mam` | XML | MAM native
`json-vtrad-bhs` | JSON | BHS
`json-vtrad-sef` | JSON | Sefaria
`json-vtrad-mam` | JSON | MAM native

**The BHS and Sefaria folders are stored incrementally against the MAM one, and are
therefore far from complete.**
The MAM folders hold all 24 book-group files.
A BHS or Sefaria folder holds only the book groups whose cv-labels that versification
places somewhere other than where MAM places them — six for BHS, five for Sefaria:
`1Sam-2Sam`, `Deut`, `Exod`, `Jer`, `Josh`, and, for BHS alone, `Num`.

**So, to read book group `X` in versification `V`: read `<fmt>-vtrad-<V>/X`, and if it
is not there, read `<fmt>-vtrad-mam/X` instead.**
Every cv-label and every byte of text in that file is what versification `V` calls for,
which is exactly why the file is not stored twice.
**And the file says so itself**: its root's `versification-tradition` names every
tradition it is correct for, so a `Ruth` read this way says
`versification-tradition="vtmam,vtbhs,vtsef"` and a `Num` says
`versification-tradition="vtmam,vtsef"`.

This replaced six complete folders on 2026-09-12 and removed 24.3 MB, taking the
product from 63.3 MB to 39.0 MB.

The JSON format mirrors the XML structure: it has the same hierarchy and element types.

For a detailed guide to the hierarchy and element types of both formats,
see [Reading MAM-simple](doc/reading-mam-simple.md).

For the versification and cantillation choices behind this extract, the two Decalogues
above all, see
[Versification and cantillation](https://bdenckla.github.io/MAM-basics/MAM-simple/versification-and-cantillation.html),
a page served from MAM-basics' `gh-pages/MAM-simple/` directory.

## Sparse checkout

MAM-simple is a product tree inside the
[MAM-basics repository](https://github.com/bdenckla/MAM-basics). To check out only this
product from a fresh clone, run:

```text
git clone --filter=blob:none --sparse https://github.com/bdenckla/MAM-basics.git
git -C MAM-basics sparse-checkout set MAM-simple
```

In an existing sparse MAM-basics checkout, add the product with
`git sparse-checkout add MAM-simple`.

One property of the text is worth knowing before you write any code against it:
**the Hebrew is in neither NFC nor NFD.**
The combining marks of a letter are in MAM's order, in which shin dot, sin dot, dagesh
and rafe come first — so a dagesh comes before its vowel, where Unicode's canonical
order puts the vowel first.
The two orders render identically, so literal search with normalized input can miss MAM
text and normalization can change bytes without a visible signal. Preserve MAM order
when byte-for-byte round trips or MAM-compatible output are required. A consumer with a
different output contract may transform deliberately, but should transform both sides
before comparison.
For the full statement, including what the guarantee does and does not cover, see
[Three invariants worth relying on](doc/reading-mam-simple-xml.md#three-invariants-worth-relying-on).

This product also has an example program. It is found under `py-examples/`:

<!-- sync: bullet list of example programs also appears in doc/reading-mam-simple.md ##The-py-examples-Programs -->
* The [`main_letter_small_job_example.py`](py-examples/main_letter_small_job_example.py) program
reports all of the `<letter-small>` elements in `Job.xml`,
writing output to `py-examples-out/letter-small-job.txt`.

Two further example programs, `main_mam4sef_example.py` and `main_mam_osis_example.py`,
were retired on 2026-09-12.
They created the Sefaria and OSIS editions of MAM from this product,
and they were written when MAM-simple, MAM-for-Sefaria and MAM-OSIS were separate repositories.
Both editions are still produced, by
[MAM-basics](https://github.com/bdenckla/MAM-basics)'s own `py/main_mam4sef.py` and
`py/main_mam_osis.py`, and the retired programs remain in that repository's history.

As I said above, MAM-simple is not complete.
It is an extract of MAM, not a full version of MAM.
For versions of MAM that are complete (but therefore far from simple),
see [MAM-parsed](../MAM-parsed/README.md).

MAM-simple is available under CC BY-SA 4.0.
See [LICENSE.md](LICENSE.md) for the licence text and for the attribution it asks for,
which differs between Hebrew and every other language.

Questions? Email maintainer@miqra.simplelogin.com.
