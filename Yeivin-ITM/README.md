# Yeivin ITM selected excerpts

This product contains Ben Denckla's editable adaptation of selected excerpts from
Israel Yeivin's *Introduction to the Tiberian Masorah*, translated and edited by
E. J. Revell. The Python-shaped adaptation is under `py/yeivin_itm/content/`;
the renderer and its helpers are under `py/yeivin_itm/`, apart from six
rendering-helper modules that sit beside the adaptation in
`py/yeivin_itm/content/`.

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
The adaptation and remark modules of `py/yeivin_itm/content/` are excluded from
the repository's blanket GPL statement. [`../DATA-LICENSES.md`](../DATA-LICENSES.md)
records the path-specific terms. The renderer, and the six rendering-helper modules
that `../DATA-LICENSES.md` names in that subtree, are repository code under
GPL-3.0.

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
ITM. The permission above names only the 1980 work, and the repository records no
permission for the 1968 study and no rights holder of it. Ben accepted this small
comment-only passage with the editable adaptation.
The selected adaptation is not the full OCR or a full transcription of any book.

## Public rendering and claim data

The preparation preserves the adaptation's Python module basenames and existing
page names, links, anchors, permission notice, and authorship caveat. Source-internal
comments are omitted where necessary; the adaptation's MAM remarks are preserved. The migration
took its source from MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`; no test pins
the adaptation to it now.
Line-local `translit-ok` annotations preserve the adaptation's established
romanizations under the repository's external-vocabulary lint exception.

The canonical page destination is `gh-pages/yeivin-itm/`, with
`yeivin_itm.html` as the landing page. The migration preserved all 17 existing filenames,
internal links, and anchors. The maintained entry point is `py/main_yeivin_itm.py`:

- `survey-meteg-claims` reads only `out/accgram/meteg-before-stress.json` and writes
  `Yeivin-ITM/meteg-claims.json`
- `render` reads the adaptation and tracked claim data and writes the pages,
  the unchanged historical stylesheet, and the complete Taamey D font/source notices
- `check` verifies the claim projection, prose pins, source lint, page bytes, and
  complete asset mapping without writing
- `review-claims` reports the claim population, pins, and page lines that the
  current analysis would change, without writing

All four commands run from the repository root without private inputs. The meteg
analysis is independently owned by accgram and consumes the tracked public
Phonetic MAM release; it is not run by the Yeivin renderer.

`meteg-claims.json` follows the closed schema in
`schema/meteg-claims-v1.schema.json`. The schema's `$id`,
`https://bdenckla.github.io/MAM-basics/Yeivin-ITM/schema/meteg-claims-v1.schema.json`,
identifies the schema; it is not where the schema is served, since Pages publishes
only `gh-pages/`. Read the schema from this directory. The claim file records the
exact input identity and SHA-256, named populations and exclusions, integer
numerators and denominators, and percentages derived directly from those
fractions. Existing examples remain
in the adaptation; no new source excerpts or examples are included in the data.
The counts retain the analysis's cantillation and qamats projection, with no
extra filters invented to reproduce historical workbook figures.

Ben approved correction of his added claims and their explanatory prose on
2026-10-01, and the 11 fractions that the oleh-weyored correction changed on
2026-10-03. The prose pins in `py/yeivin_itm/claim_schema.py` fix the 20 reviewed
fractions and a SHA-256 of the claim population: every record in the ordinary
population of `out/accgram/meteg-before-stress.json` whose pattern is FR1, FR2,
FR3, AFR1, AFR4 or XAFR1. A changed fraction, or a changed, added or removed
record in that population, therefore requires Ben's fresh review; a change
elsewhere in the Phonetic MAM release does not. Until he approves new pins,
`survey-meteg-claims` and `check` raise and write nothing. The claim file's input
SHA-256 identifies the whole analysis file that it was projected from; it is not a
pin. Numerical text is inserted from named claim references before HTML line
wrapping. Percentages are rounded once from the original fractions.

`in/yeivin_itm_legacy_differential.json` is the frozen record of the migration from
phonetic-hbo commit `8da90513df1c759d8db34b135d007e79686715d3`. From the pages and
adaptation modules as of `75a1127b5310f0dd4ed2827ad93c687178960f8e`, it reconstructed
each page that phonetic-hbo commit published, after removing the shared favicon line
and reversing only Ben's approved numerical and explanatory corrections in three
pages and the landing page's font-source link, and it pinned every other adaptation
module to its mechanically moved public source. No test reads it now.

## Editing the adaptation

The adaptation under `py/yeivin_itm/content/` is editable source, and Ben approves
each change to it. After editing a module, regenerate the pages and run the
product's tests from the repository root:

```powershell
./.venv/Scripts/python.exe py/main_yeivin_itm.py render
```

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_yeivin_itm.py
```

The regenerated pages are the test: read every changed line under
`gh-pages/yeivin-itm/` before committing, and name in the commit message the
approval of Ben's that the change carries out. The tests require the tracked pages
to equal regeneration, every internal link and fragment to resolve, and every
biblical reference that a page's `data-bk-ch-vr` or `data-bk-ch-vr-2` attribute
holds, or that a source string holds as its whole value, to name a verse in one of
the three versifications that MAM-simple ships. Ben's numerical claims are not edited in the pages; they come
from `meteg-claims.json` under the pins described above.

`in/yeivin_itm_published_anchors.json` lists the 345 fragment identifiers that the
17 pages had at the end of the migration, the same identifiers as the pages
phonetic-hbo published. phonetic-hbo's redirect pages forward old addresses,
fragments included, to these pages, so the tests require every listed identifier to
remain. An edit may add identifiers; removing one is Ben's decision and updates that
record in the same commit.

## Data and asset terms

The claim data's path-specific terms are recorded in `../DATA-LICENSES.md`.
The adaptation and its rendered pages retain the permission scope above;
the data file makes no new grant over Yeivin's text. Taamey D is distributed under
GPL version 2 with its font-embedding exception. The landing page links to the
font's complete license notice and same-host corresponding-source package.
No Jacobson image crops are part of this product.
