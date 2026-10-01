# Phonetic MAM

This product represents the existing Phonetic MAM display as one public corpus.
It contains generic MAM Hebrew, the Sephardic and Ashkenazic transcriptions,
and only their displayed chapter, verse, row and reading structure. Each book is
stored in `data/` under the closed `phonetic-mam-public-v1` schema. The example
pages use a separate closed display-document format in `examples/display.json`.

The display does not contain source-quality annotations, source records,
source-position tables or an additional phonological verdict layer. A consumer
derives its needed working facts from the display; it does not receive a renamed
source intermediate. Complete-output comparison with the previously published
pages and assessment of all artifacts together are required before a release is
approved. Schema validation and rendered-page parity alone are insufficient.

## Commands

Run the repository's `py/main_phonetic_mam.py` entry point from MAM-basics:

- `export` regenerates the public display product through its private input adapter
- `render` reads only this public product and writes `gh-pages/phonetic-mam/`
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
