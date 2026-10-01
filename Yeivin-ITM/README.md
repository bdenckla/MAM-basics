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

## Migration status

The preparation preserves the adaptation's Python module basenames and existing
page names, links, anchors, permission notice, and authorship caveat. Source-internal
comments are omitted where necessary; the adaptation's MAM remarks are preserved. Its source
is pinned to MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`.
Line-local `translit-ok` annotations preserve the adaptation's established
romanizations under the repository's external-vocabulary lint exception.

The canonical page destination is `gh-pages/yeivin-itm/`, with
`yeivin_itm.html` as the landing page. The 17-page rendering is currently verified
only in ignored migration scratch. This preparation does not publish pages or
approve the workbook-era numerical claims in sections 320 and 322. A maintained
renderer must consume approved claim data before publication is enabled.
