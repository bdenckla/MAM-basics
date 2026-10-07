# Phonetic MAM preparation

The modules under `py/phonetic_mam/` implement the unified rendering of the existing
public Phonetic MAM pages. The source-independent algorithm core, read-only
computation interface, exporter, closed display release, public consumers and
generated target were integrated and pushed to `main` on 2026-10-01 in
`2b92117ab909f74481cd0be4dbbc9d85204295ee`. The Pages run for `38c0116f`, a
descendant of that merge, deployed the generated site; it finished at 15:39:45 New
York time on 2026-10-01.

## Public display contract

The candidate contract holds each book's ordered chapters, verses, and displayed
table rows. Each row has generic Hebrew cells and Sephardic and Ashkenazic
transcription alternatives. Inline tokens are limited to literal displayed text,
superscript e, stress highlighting, implicit maqaf, and the existing reading labels.
The contract has no source annotations, source-position tables, or analysis-only
phonological fields. Analyses must derive their working facts from the public
display and public MAM rather than extend the release with a private record.

Until 2026-10-03, the independent `legacy_projection` module projected the frozen
public HTML of phonetic-hbo commit `8da90513` into the release schema, and the
source-driven exporter had to produce the same complete display corpus; matching
rendered HTML alone was insufficient. The 2026-10-02 review ran that module by hand
and found all 39 books equal. The module was removed on 2026-10-03 because it reads
only the two old page families, which no generator can now produce and no
maintained clone holds; Git history keeps it at
`c17de1756c785682162f805e27600c9c67462990`. For chapters whose MAM-parsed input was
unchanged, the frozen projection hashes in
`in/phonetic_mam_legacy_projection_sha256.json` remained the comparison with those
pages until 2026-10-07, when they were retired, with their input record
`in/phonetic_mam_legacy_projection_inputs.json`, by Ben's decision of that day;
`9972e6c076cc3e5844258e176ccc4266571f5a69` holds their last copies. Review also
covers the combined code, metadata, example pages, analyses, fixtures and joins;
the closed validator is only the mechanical part of that boundary.

The five example pages have their own closed display-document format. Their input
is normalized from the exact rendered HTML rather than retaining calculation
fixtures or source-code string boundaries. The public renderer reproduces those
pages byte-for-byte apart from their explicit shared favicon link. The source
adapter remains a migration dependency for their calculation, so later private
retirement must account for that adapter.

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
the explicit Sephardic fallback. Local Edge acceptance on 2026-10-01 passed
the browser-level CSS, printing, no-JavaScript, navigation, focus, font/image,
and console/network checks after the explicit favicon links were added. At a
390-pixel viewport, wider tables require horizontal scrolling. These results
verify the integrated local pages, not the deployed site.

## Font support

`in/font-support/taamey-d-0.921/` holds the immutable source archive, license,
copyright notice, and provenance for the frozen font. The pure
`py_html.taamey_d_assets.product_font_assets` helper returns the font and its complete
same-host support mapping together, without writing files. Each product publisher
must copy the whole mapping and expose its font's `woff2/SOURCE.txt` link.

The support package's input closure and source identities have been checked.
An exact font rebuild has not been established. The Phonetic target includes the
unchanged font and its complete same-host source-support tree together.

## Public consumers and independent analysis

The post-stress-meteg and Breuer analyses, and the final-stress differential,
consume only the tracked public display and public MAM. Decoded working facts
remain transient. Output forms use the generic Hebrew already displayed publicly.
The independent pre-stress-meteg analysis lives under `py/accgram/` and
`out/accgram/`; it is not a Phonetic MAM field or product component.

Ben approved correcting his added claims to the reproducible public-MAM analysis.
The independent analysis feeds the minimized `Yeivin-ITM/meteg-claims.json` product,
which the Yeivin renderer validates before rendering the selected excerpts.
The Phonetic index links to the separate Yeivin target. Both targets are on
integrated `main`, and the Pages run for `38c0116f` deployed them on 2026-10-01.
The coordinated legacy redirect cutover followed that day: phonetic-hbo's
redirects, from its commit `2ca51088`, deployed at 17:10:52 New York time.
