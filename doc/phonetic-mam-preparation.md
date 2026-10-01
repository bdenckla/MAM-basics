# Phonetic MAM preparation

The modules under `py/phonetic_mam/` prepare a unified rendering of the existing
public Phonetic MAM pages. They are not yet a release exporter or a publishing
command. No tracked `Phonetic-MAM/data/` release is present in this preparation.

## Public display contract

The candidate contract holds each book's ordered chapters, verses, and displayed
table rows. Each row has generic Hebrew cells and Sephardic and Ashkenazic
transcription alternatives. Inline tokens are limited to literal displayed text,
superscript e, stress highlighting, implicit maqaf, and the existing reading labels.
The contract has no source annotations, source-position tables, or analysis-only
phonological fields. Analyses must derive their working facts from the public
display and public MAM rather than extend the release with a private record.

The independent `legacy_projection` module reads only the frozen public HTML.
It supplies a whole-output comparison for the candidate contract. A future exporter
must also prove equality of its complete release with that public-only witness;
matching rendered HTML alone is insufficient. No release data is approved here.

Existing alternatives can occupy different numbers of transcription columns in
the two pronunciations. The model preserves those visible column counts. It does
not silently select one pronunciation's layout or duplicate Hebrew to build two
separate page trees.

## Unified renderer

The pure renderer returns a single `tnkh/` tree, with both transcription alternatives
in shared rows. Its maintained CSS and JavaScript are separate source assets.
The native radio group defaults to Sephardic. With JavaScript, the exact query
values `sephardic` and `ashkenazic` control initialization and navigation, while
unrelated query parameters and fragments survive. Missing or invalid values are
normalized to Sephardic. No hidden stored preference is used.

Without JavaScript, the radio control changes the current page; navigation retains
the explicit Sephardic fallback. Browser-level CSS, printing, and no-JavaScript
verification remains outstanding in this preparation. The corpus DOM differential
and standalone JavaScript contract checks do not substitute for those checks.

## Font support

`in/font-support/taamey-d-0.921/` holds the immutable source archive, license,
copyright notice, and provenance for the frozen font. The pure
`py_html.taamey_d_assets.product_font_assets` helper returns the font and its complete
same-host support mapping together, without writing files. Each product publisher
must copy the whole mapping and expose its font's `woff2/SOURCE.txt` link.

The support package's input closure and source identities have been checked.
An exact font rebuild has not been established, and no new font copy or served
source-support tree is added by this preparation.
