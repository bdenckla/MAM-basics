# MAM-parsed

This MAM-basics product directory contains
[Miqra According to the Masorah](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah)
in two Wikisource-derived primary parsed formats, `plain/` and `plus/`, plus a
Google-derived comparison product in `google/` that uses the plain schema.
<!-- No non-Dovi equivalent currently exists for this page on en.wikisource.org. -->

Each of `plain/`, `plus/`, and `google/` contains a JSON file for each of the 24
books of the Miqra.

Hebrew Wikisource supplies `plain/` and `plus/`. The
[MAM Google Sheet](https://purl.org/mam/google-sheet#gid=920165745) supplies only
`google/`, the independent Google input to `py/main_diff.py wsgo`.

Each JSON file represents its corresponding book in a format that is easier for a program to read than the source Wikitext.
(It is easier for a *program* to read, that is. It is not very human-readable.)

The format of the JSON files is easier to read because it is a *parsed* format.
The source data contains Wikitext strings, including Wikitext templates such as
`{{f|a|b|c}}`.
In contrast, the JSON files represent the C and E column data as
parse trees that "know" about the Wikitext template format.

The contents of the `plain/` files stay close to the Wikisource Wikitext after
the source-page structure is converted to the 24-book schema. The `plus/` files
diverge from `plain/` in the following ways:

* Compared to `plain/`, the `plus/` format adds:
    * A `good_ending_plus` key to the `book39` header.
    * A targeted version of each מ:הערה template call.
    * A template marking each word with special letters.
* Compared to `plain/`, the `plus/` format removes:
    * custom XML tags
    * 0 (zero) and תתת (triple-tav) pseudo-verses

For detailed documentation of the file structures, see:

* [Reading MAM-parsed plain](https://bdenckla.github.io/MAM-basics/MAM-parsed/plain/html/mpplain.html) — structure reference for the "plain" format
* [Reading MAM-parsed plus](https://bdenckla.github.io/MAM-basics/MAM-parsed/plus/html/mpplus.html) — structure reference for the "plus" format

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

From the MAM-basics root, regenerate Wikisource-derived `plain/` and `plus/`, the
example support file, and the published documentation:

```powershell
.venv/Scripts/python.exe py/main_parse.py ws
```

Regenerate the independent Google comparison product separately:

```powershell
.venv/Scripts/python.exe py/main_parse.py go
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
The historical inputs are included. This sparse checkout supplies data and
the self-contained toy example; the full MAM-basics checkout supplies the
product generators. No release archive is maintained.
