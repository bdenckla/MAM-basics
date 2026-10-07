# Shared HTML styles

State: runbook

The published tree shares styles through relative links. Directory depth changes
the link prefix; it does not require a stylesheet copy in every family.

## Prose documents

`gh-pages/document.css` is the hand-authored prose base. It supplies the ordinary
English typography and common document helpers. English uses the browser's
default family, and inline code uses the browser's default monospace family.
MAM abbreviations do not use small caps.

Load `document.css` before a family's extension. Extensions retain the family's
Hebrew display, examples, tables and emphasis conventions. Root pages preserve
their browser-default text size; specialized wide pages retain their width.
Phonetic MAM loads the Yeivin ITM extension before its pronunciation controls and
print styles. Book of Job prose pages share `book-of-job/style.css`.

The base lives directly in the published tree and has no deployment copy.
Family extensions have their existing source locations: authored CSS under
`py/`, or hand-authored sheets in `gh-pages/` for root, WLC and UXLC pages.
Generated sheets identify their source in their banner.

## Edition pages

MAM-with-doc, FOI, MAM-OSIS documentation and near-Aleppo editions load
`gh-pages/MAM-with-doc/two_col_style.css`. Its source remains
`py/mb_misc/styles_mam_with_doc.css`. The stylesheet and the independent
near-Aleppo MAM-mode oracle are unchanged by consolidation. Edition pages retain
their specialized layout rather than loading the prose base.

## Reports and standalone bundles

`gh-pages/report.css` is the hand-authored report base, shared by the Holman
reports and MAM change logs. Family sheets retain specialized displays, controls
and category colors. `py/mb_misc/report_stylesheet.py` supplies asset routing.

Published reports link to the root base. Temporary differential generation uses
the same logical hrefs as publication. Explicit standalone outputs copy the base
into `report-assets/report.css` inside their output directory. The separate
directory keeps the base clear of specialty sheets even when several standalone
reports share an output directory. Report fonts come
from `doc/woff2/`, with a missing source treated as an error and full-byte
comparison before copying.

CSS font and image URLs resolve from the stylesheet's directory, not from the
HTML page. Keep family-specific font URLs in their extensions when sharing a
base across directories.

## Regeneration and verification

Run the affected generators, then the mega and suite required by `AGENTS.md`.
Changes to the hand-run OSIS generator also require `py/main_mam_osis.py`.
`py/tests/test_shared_html_styles.py` checks local stylesheet and font references
and requires each shared base to load before its registered family extensions.
Report differential checks also cover complete standalone asset bundles.
