# Book-of-Job review data in MAM-basics

This product directory holds the data and reading procedures for the BHQ Job review. The published site starts at [bdenckla.github.io/MAM-basics/book-of-job/](https://bdenckla.github.io/MAM-basics/book-of-job/); its main document and its per-record detail pages let a reader inspect the relevant manuscript image crops.

MAM-basics owns the generators. The published files are under [`../gh-pages/book-of-job/`](../gh-pages/book-of-job/), while this product directory holds:

- `out/` — review JSON, including `enriched-quirkrecs.json`, plus the hand-made Cambridge 1753 crop coordinates in `cam1753-crops.json`
- `doc/` — procedures for opening the published files and reading the MAM-simple input

The many image crops, the web fonts, and `out/cam1753-crops.json` are retained source data. Regeneration does not recreate those files.
