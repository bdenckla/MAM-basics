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

## Arrow links

All generated near-Aleppo documentation, FOI and edition pages load
`gh-pages/near-aleppo/link-presentation.css` after their existing styles.
Its authored source is `py/near_aleppo/link_presentation.css`;
`py/near_aleppo/link_presentation.py` supplies the generated banner and inserts
link attributes without reserializing page text. Relative stylesheet paths
follow each page's directory depth.

The shared rules remove link underlines and add decorative arrows. Same-page
targets earlier in document order get an up arrow; later targets get a down
arrow. Other MAM-basics pages get a right arrow, and destinations outside
MAM-basics get a boxed outward arrow. Hover backgrounds, focus outlines and
visited colors retain visible interaction cues. The rules apply only to links
marked by this link helper.

The top-level `gh-pages/index.html` also loads this stylesheet and uses the same
link helper with the website root as its page directory. Its source remains
`py/author_site/site_index.py`; regenerate it with `py/main_authored.py gen-site`.
Other deploy-root pages retain their existing link presentation.

Regenerate the near-Aleppo pages with `py/main_near_aleppo.py --html` when
changing these rules, and regenerate the top-level index with
`py/main_authored.py gen-site`. The completed offline final-punctuation review
extract was retired on 2026-10-11.

## Reports and standalone bundles

`gh-pages/report.css` is the hand-authored report base, shared by the Holman
reports and MAM change logs. Family sheets retain specialized displays, controls
and category colors. `py/mb_misc/report_stylesheet.py` supplies asset routing.

Published reports link to the root base. Temporary differential generation uses
the same logical hrefs as publication. Explicit standalone outputs copy the base
into `report-assets/report.css` inside their output directory. The separate
directory keeps the base clear of specialty sheets even when several standalone
reports share an output directory. The font follows the same routing: a published
report's stylesheet loads the site's one copy beside the root base, and an
explicit standalone output copies that pinned file into `woff2/` inside its
output directory.

CSS font and image URLs resolve from the stylesheet's directory, not from the
HTML page. Keep family-specific font URLs in their extensions when sharing a
base across directories.

## Hebrew font

Every page that sets Hebrew in Taamey D loads one file,
`gh-pages/woff2/Taamey_D.woff2`, through a relative URL from its stylesheet:
`../woff2/Taamey_D.woff2` from a family directory such as `gh-pages/wlc/`, and
`../../woff2/Taamey_D.woff2` from one level deeper. Like the root base, the font
lives directly in the published tree, and no code writes it.
`py/py_html/taamey_d_assets.py` pins its SHA-256. The Phonetic MAM and Yeivin ITM
publishers write its `FONT-NOTICE.txt`, `GPL-2.0.txt` and `SOURCE.txt` beside it,
and their landing pages link that `SOURCE.txt`. Pages under `doc/` that use the
font reach the same file by a relative path into `gh-pages/woff2/`.

## Regeneration and verification

Run the affected generators, then the mega and suite required by `AGENTS.md`.
Changes to the hand-run OSIS generator also require `py/main_mam_osis.py`.
`py/tests/test_shared_html_styles.py` checks local stylesheet and font references,
requires every published font reference and file to be the one Taamey D copy,
and requires each shared base to load before its registered family extensions.
Report differential checks also cover complete standalone asset bundles.
