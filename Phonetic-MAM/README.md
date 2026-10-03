# Phonetic MAM

This product represents the existing Phonetic MAM display as one public corpus.
It contains generic MAM Hebrew, the Sephardic and Ashkenazic transcriptions,
and only their displayed chapter, verse, row and reading structure. Each book is
stored in `data/` under the closed `phonetic-mam-public-v1` schema. The example
pages use a separate closed display-document format in `examples/display.json`.

The display does not contain source-quality annotations, source records,
source-position tables or an additional phonological verdict layer. A consumer
derives its needed working facts from the display; it does not receive a renamed
source intermediate. The release's complete output was compared with the pages
that phonetic-hbo published at the commit named below, and all artifacts were
assessed together; schema validation and rendered-page parity alone were not
enough. Those pages cannot be produced again, so the comparison cannot be
repeated for text that MAM has changed since. The suite compares each rendered
chapter with the old pages' frozen projection hashes only while the chapter's
MAM-parsed input matches its fingerprint in
`in/phonetic_mam_legacy_projection_inputs.json`; a chapter that a refresh changes
leaves that comparison, and its diff is reviewed instead.

## How the Hebrew differs from MAM's text

The Hebrew here is generic, this repository's term for Hebrew without the
phonetic computation's annotations. It has neither U+05C8, which marks a vocal
shewa, nor U+05C9, which marks a dagesh ḥazaq, nor either retired annotation
pair, U+05B0 U+05AF or U+05BC U+05C4: a shewa here is U+05B0 and a dagesh
U+05BC. Generic Hebrew is still not MAM's text as `MAM-simple/` has it, and a
consumer joining this release to MAM must allow for these differences:

1. **Perpetual qere.** Where MAM has a perpetual qere, such as the
   Tetragrammaton, this release has only the qere, in the form that
   `py/phonetic_mam/core/qere_from_implicit_kq.py` derives from MAM's spelling;
   that module's docstring lists the kinds. At Genesis 2:4, for example,
   `MAM-simple/` has יְהֹוָ֥ה and this release has אֲדֹנָ֥י. This release has
   the qere in place of MAM's spelling at 7,710 of MAM's chanted words. One more
   is at Deuteronomy 32:6, where MAM has two chanted words, הַ with a large he
   and לְיְהֹוָה֙, and this release has one form for both, הַלְאֲדֹנָי֙.
2. **Extraordinary points.** This release has none of MAM's extraordinary
   points, the upper dot U+05C4 and the lower dot U+05C5. The release validator,
   `py/phonetic_mam/display_schema.py`, refuses both.
3. **Stress helpers.** MAM's two stress-helper templates, `מ:דחי` and `מ:צינור`,
   give a chanted word in two forms, the second with the accent's stress helper.
   `MAM-simple/` has the first form and this release the second. At Psalms 2:6,
   for example, `MAM-simple/` has וַ֭אֲנִי and this release has וַ֭אֲנִ֭י.
4. **Varika.** This release keeps MAM's varika, U+FB1E, which `MAM-simple/`
   lacks.
5. **2 Kings 22:1.** MAM's qamats template, `מ:קמץ`, gives the verse's last
   chanted word two alternatives, מִבׇּֽצְקַֽת for its ד parameter
   and מִבָּֽצְקַֽת for its ס parameter. This release has only the second,
   as מִבָּֽצְקַֽת׃, without the labels קמץ-ד and קמץ-ס that it has at each of the
   other 356 verses where MAM has that template. Until the Wikisource refresh of
   2026-09-27, this repository's copy of MAM had only the form this release has.
6. **2 Chronicles 25:17.** MAM has the ketiv לך and the qere לְכָ֖ה. This
   release has לְךָ֖, with the ketiv's final kaf and the qere's points. MAM's
   note there reports that the Aleppo Codex has לְךָ֖ with no qere note, so this
   release has the form that MAM's note attributes to that manuscript. That is
   MAM's report; the manuscript itself has not been checked.

The transcriptions have each acute or breve vowel decomposed, as a base letter
followed by U+0301 or U+0306, while their ḥ is the precomposed U+1E25. Elsewhere
the repository keeps Latin letters with diacritics in NFC; these are the bytes
of the previously published pages, which Ben's decision of 2026-10-03, recorded
in `doc/review-findings-2026-10-02-update.md`, keeps.

## Commands

Run the repository's `py/main_phonetic_mam.py` entry point from MAM-basics:

- `export` regenerates the public display product through its private input adapter
- `render` reads this public product, its stylesheet and script in
  `py/phonetic_mam/assets/`, the five example images in
  `in/phonetic-mam-images/`, and the Taamey D font in `doc/woff2/` with its
  source support in `in/font-support/`; it writes `gh-pages/phonetic-mam/` and
  the shared font-source package in `gh-pages/font-sources/`
- `check` validates the complete public release without writing
- `compute` serves explicitly versioned, read-only computations over stdin/stdout;
  this local transport is not a release-data format and saves no inputs or results

The exporter needs the configured MAM-private checkout and its corresponding
interpreter. All rendering and ordinary public analyses run without MAM-private.
The exporter is the only routine public-pipeline step with that private dependency.

## Attribution and terms

MAM was prepared by Seth (Avi) Kadish from material developed at Hebrew Wikisource,
with major technical assistance from Erel Segal-Halevi and Benjamin Denckla.
Attribute the MAM Hebrew to
[Hebrew Wikisource](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning).
MAM and its derivative display retain
[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The existing Phonetic MAM source attribution also names
[Al-Hatorah Mikraot Gedolot](https://mg.alhatorah.org).

Ben Denckla's implementation is covered by the repository's GPL-3.0 license.
Third-party examples, five Jacobson image crops and the Taamey D font have the
separate terms in [DATA-LICENSES.md](../DATA-LICENSES.md). No new rights over
third-party material are granted. The font is accompanied by its notices, full
GPL v2 text, embedding exception and corresponding-source support.

The historical display oracle is `bdenckla/phonetic-hbo` commit
`8da90513df1c759d8db34b135d007e79686715d3`. The compact projection hashes are
tracked at `in/phonetic_mam_legacy_projection_sha256.json` in MAM-basics.
