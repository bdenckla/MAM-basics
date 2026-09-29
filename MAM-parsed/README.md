# MAM-parsed

This MAM-basics product directory contains
[Miqra According to the Masorah](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah)
in the Wikisource-derived MAM-parsed-plus format under `plus/`.
<!-- No non-Dovi equivalent currently exists for this page on en.wikisource.org. -->

`plus/` contains one JSON file for each of the 24 books of the Miqra. Hebrew
Wikisource supplies the source data.

Each JSON file represents its corresponding book in a format that is easier for a program to read than the source Wikitext.
(It is easier for a *program* to read, that is. It is not very human-readable.)

The format of the JSON files is easier to read because it is a *parsed* format.
The source data contains Wikitext strings, including Wikitext templates such as
`{{f|a|b|c}}`.
In contrast, the JSON files represent the C and E column data as
parse trees that "know" about the Wikitext template format.

The format adds conveniences for consumers, including a `good_ending_plus` key
in each `book39` object, targeted scroll-difference notes, and an explicit
template for each atom with special letters. Source boundary records such as the
0 (zero) and תתת (triple-tav) pseudo-verses are absent.

For detailed documentation of the file structures, see:

* [Reading MAM-parsed plus](https://bdenckla.github.io/MAM-basics/MAM-parsed/plus/html/mpplus.html) — structure reference for the "plus" format

The [consumer cautions](#consumer-cautions) below cover whitespace templates and text
spacing around narpas (narrow-sense paseq, ׀).

This product directory also contains a toy sample application
[`main_tmpl_survey_toy_example.py`](py-examples/main_tmpl_survey_toy_example.py),
giving some sense of how the JSON files might be used.
It writes its output to [`py-examples-out/tmpl_survey_toy.json`](py-examples-out/tmpl_survey_toy.json).

The format of these JSON files is not yet stable. I.e. if you write an application
based on their format, be aware that their format is still subject to change at this time.

Other versions/formats of MAM (each with their tradeoffs) include:

* [MAM-simple](../MAM-simple/README.md)
* [MAM for Sefaria](../MAM-for-Sefaria/README.md)

Questions? Email maintainer@miqra.simplelogin.com.

## Historical comparisons

The [historical release inputs](historical/README.md) are tracked product data.
Named-release and current change-log comparisons use MAM-basics alone for
MAM-parsed inputs. Arbitrary pre-migration revisions require read access to
a sibling MAM-parsed clone and the explicit `--legacy-history` mode.

## Regeneration and the example

From the MAM-basics root, regenerate Wikisource-derived `plus/`, the example
support file, and the published documentation:

```powershell
.venv/Scripts/python.exe py/main_parse.py ws
```

Run the toy example from the MAM-basics root; its existing output is the
one-file differential reference:

```powershell
.venv/Scripts/python.exe MAM-parsed/py-examples/main_tmpl_survey_toy_example.py
```

## Download only this product

A sparse checkout selects this product from MAM-basics without downloading
the other product trees. Choose an unused destination for the clone:

```powershell
git clone --filter=blob:none --sparse https://github.com/bdenckla/MAM-basics.git MAM-parsed-sparse
```

```powershell
git -C MAM-parsed-sparse sparse-checkout set MAM-parsed
```

The files are under `MAM-parsed-sparse/MAM-parsed/`.
The historical inputs are included: a ZIP snapshot of `plus/`, of 13 to 15 MB,
for each boundary of a named change-log release, with one more for each release
pinned later. This sparse checkout supplies data and the self-contained toy
example; the full MAM-basics checkout supplies the product generators. No
release archive of this product, such as a packaged download of a version, is
maintained; the historical snapshots are inputs to the change log.

## Consumer cautions

Consumers use this parsed product and its supported reader rather than reconstructing Scripture
from raw Wikitext. Within MAM-basics, `mb_cmn.read_books_from_mam_parsed_plus` reads `plus/` with
the explicit product path from `mb_cmn.paths.mam_parsed_path()`. Specialized material absent
from this product uses its declared source. Pipeline implementations may read their raw inputs.

### Illustrations inside notes

A note may illustrate an overburdened letter as two copies joined by `+`. Such an illustration
is not automatically running edition text or evidence of a manuscript reading. Apply the
consumer's declared projection; a manuscript claim requires manuscript evidence.

### Whitespace templates

A whitespace template can be the only separator between adjacent Scripture strings in
the Wikisource-derived `plus/` payloads. For example, the strings before
and after `מ:ששש` or `ססס` can contain no literal whitespace at that boundary. A
plain-text projection that does not preserve layout must supply at least one separator;
a layout-preserving renderer must implement the documented space or break. Dropping
the template fuses separate atoms, while collecting a descriptive parameter such as
`פסקא באמצע פסוק` inserts documentation into Scripture. This rule does not apply to
narpas.

### Narpas and text spacing

The narrow-sense paseq template also has no text whitespace before or after it, but it
is not a whitespace template. The omission is not a grouping instruction: narpas forms no compound of any kind, and only maqaf joins atoms into
a chanted word. The omission also prescribes no display spacing. An edition decides
whether to display spacing before and/or after narpas; an analytical consumer need not
make a display-spacing decision.
