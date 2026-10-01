# Yeivin ITM selected excerpts

This product contains Ben Denckla's editable adaptation of selected excerpts from
Israel Yeivin's *Introduction to the Tiberian Masorah*, translated and edited by
E. J. Revell. The Python-shaped adaptation is under `py/yeivin_itm/content/`;
the renderer and its helpers are under `py/yeivin_itm/`.

## Permission and authorship

Adapted, by permission, from Israel Yeivin, *Introduction to the Tiberian Masorah*,
translated and edited by E. J. Revell. Copyright © 1980 by the Society of Biblical
Literature.

This is Ben Denckla's loose adaptation of Yeivin and Revell. Some sections are
faithfully rendered; others take substantial liberties. Ben's own ideas are
generally placed in footnotes, but that distinction is not exhaustive.

Ben's decision of 2026-09-19 treats the existing permission to publish the adapted
excerpts as extending to their editable source. That decision does not establish
a GPL sublicense or grant additional reuse rights over the adapted material.
The exact `py/yeivin_itm/content/` subtree is excluded from the repository's
blanket GPL statement. [`../DATA-LICENSES.md`](../DATA-LICENSES.md) records the
path-specific terms. The renderer outside that subtree remains repository code
under GPL-3.0.

## Bibliographic scope

These three publications are distinct:

1. Yeivin's Hebrew course booklet for the course *Introduction to the Tiberian
   Masorah*, issued by Academon in 1971/72
2. The expanded English *Introduction to the Tiberian Masorah*, translated by
   E. J. Revell and published in 1980
3. The updated Hebrew *The Biblical Masorah*, edited and reorganized by Yosef
   Ofer and published in 2003

The comment block labelled `Yeivin Keter 5729 (1968)` in
`py/yeivin_itm/content/my_yeivin_sec_320.py` identifies section 12.9, page 99, of Yeivin's
separate 1968 Hebrew study *כתר ארם־צובה: ניקודו וטעמיו*. It is not an edition of
ITM. Ben accepted this small comment-only passage with the editable adaptation.
The selected adaptation is not the full OCR or a full transcription of any book.

## Public rendering and claim data

The preparation preserves the adaptation's Python module basenames and existing
page names, links, anchors, permission notice, and authorship caveat. Source-internal
comments are omitted where necessary; the adaptation's MAM remarks are preserved. Its source
is pinned to MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`.
Line-local `translit-ok` annotations preserve the adaptation's established
romanizations under the repository's external-vocabulary lint exception.

The canonical page destination is `gh-pages/yeivin-itm/`, with
`yeivin_itm.html` as the landing page. All 17 existing filenames, internal links,
and anchors are preserved. The maintained entry point is `py/main_yeivin_itm.py`:

- `survey-meteg-claims` reads only `out/accgram/meteg-before-stress.json` and writes
  `Yeivin-ITM/meteg-claims.json`
- `render` reads the adaptation and tracked claim data and writes the pages,
  the unchanged historical stylesheet, and the complete Taamey D font/source notices
- `check` verifies the claim projection, prose pins, source lint, page bytes, and
  complete asset mapping without writing

All three commands run from the repository root without private inputs. The meteg
analysis is independently owned by accgram and consumes the tracked public
Phonetic MAM release; it is not run by the Yeivin renderer.

`meteg-claims.json` follows the closed schema in
`schema/meteg-claims-v1.schema.json`. It records the exact input identity and
SHA-256, named populations and exclusions, integer numerators and denominators,
and percentages derived directly from those fractions. Existing examples remain
in the adaptation; no new source excerpts or examples are included in the data.
The counts retain the analysis's cantillation and qamats projection, with no
extra filters invented to reproduce historical workbook figures.

Ben approved correction of his added claims and their explanatory prose on
2026-10-01. The prose pins in `py/yeivin_itm/claim_schema.py` fix the reviewed
fractions and input hash, so a changed corpus or population requires a fresh
review. Numerical text is inserted from named claim references before HTML line
wrapping. Percentages are rounded once from the original fractions.

The exact legacy-page differential is recorded in
`in/yeivin_itm_legacy_differential.json` against phonetic-hbo commit
`8da90513df1c759d8db34b135d007e79686715d3`. It permits only Ben's approved numerical
and explanatory corrections in three pages and the landing page's font-source
link. Every page now also links to the shared favicon; the differential removes
only that exact common header line before reconstructing the original bytes. The
original page hashes and correction ranges remain unchanged. The differential also
pins all unchanged adaptation modules to their mechanically moved public source. This records branch output,
not a claim that Pages has been deployed.

## Data and asset terms

The claim data's path-specific terms are recorded in `../DATA-LICENSES.md`.
The adaptation and its rendered pages retain the permission scope above;
the data file makes no new grant over Yeivin's text. Taamey D is distributed under
GPL version 2 with its font-embedding exception. The landing page links to the
font's complete license notice and same-host corresponding-source package.
No Jacobson image crops are part of this product.
