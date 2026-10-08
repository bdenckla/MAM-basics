# CLC ruby final marks and the effective CSS property

State: executed 2026-10-08; isolated branch repair, awaiting main integration

**Fixed on the review branch:** CLC has the same kind of final-mark displacement
as the near-Aleppo example edition (NAEE), but its pointed qere is the ruby base.
The smallest demonstrated repair is `display: inline-block` on
`ruby.clc-kq span.clc-kq-q`. CLC already inherits `line-height: normal`; no line-height
override is needed. No Hebrew text, font, annotation rule or renderer was changed.

**Location and baseline:** CLC belongs to `bdenckla/MAM-basics`. Its renderer is
`py/clc/clc_kq.py`, driven by `py/main_clc.py`. The published pages are under
`gh-pages/uxlc/clc/`, linking `gh-pages/document.css` and the hand-authored,
authoritative `gh-pages/uxlc/style.css`. This is not the old sibling UXLC-utils
repository. Unlike NAEE, CLC puts qere below and ketiv above. Some spans have an
editorial highlight wrapper, so the selector also covers nested qere spans.

Work used the isolated saved checkout `/workspace/MAM-basics`, initially clean at
`3f476dedeee133d50cee8ea973c434d7ffeae4e6`, on `codex/clc-ruby-final-mark`.
The branch subsequently fast-forwarded to fetched main
`5eab49e09093556373054fd2a6b3458dab9b8c8b`, preserving the concurrent NAEE
documentation and JSON-header work. This task authorizes the branch push, with no
main integration or deployment.

**Controlled rendering:** Chromium `151.0.7922.173`, Linux x86_64, device scale
factor 1, RTL text, loaded Taamey D WOFF2 and independently loaded Noto Sans Hebrew
Regular TTF. Compare each complete reading's unchanged HTML with ordinary text
outside ruby, at the normal CLC size 26.133333 px and at 48 px. Equal black
foregrounds remove editorial-color threshold effects; missing-reading placeholders
retain their 70% size. Hide the other ruby side without removing its layout. Whole
glyph rasters are registered by translation, then thresholded ink is compared with
a one-pixel tolerance in both directions. The generated cells are checked for
adequate margins. These measurements establish rendering behavior in this browser;
they do not identify the browser engine's internal cause or establish other engines.

All five current main pages contain 176 ruby units; 43 qere have combining marks
after their final Hebrew letter. Two ketiv contain a combining mark, so the
annotations were checked too rather than assumed entirely unpointed. With Taamey D,
the six displaced qere occur at Genesis 13:3; 2 Samuel 1:16, 5:2, 13:8; and
Proverbs 3:27, 27:10. All six have final marks. Every one of the 176 qere and all
176 annotation slots match the ordinary controls after the repair at both sizes.

The table gives the number of reading rasters with any ink beyond the one-pixel
tolerance. `display` changes only the reading span to an inline block; `line`
changes only its line height to normal; `both` applies both declarations.

| Reading / font | Size (px) | Readings | Original | display | line | both |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLC qere / Taamey D | 26.133333 | 176 | 6 | 0 | 6 | 0 |
| CLC qere / Taamey D | 48 | 176 | 6 | 0 | 6 | 0 |
| CLC qere / Noto Sans Hebrew | 26.133333 | 176 | 17 | 0 | 17 | 0 |
| CLC qere / Noto Sans Hebrew | 48 | 176 | 18 | 0 | 18 | 0 |
| CLC ketiv / both fonts | both sizes | 176 each | 0 | 0 | 0 | 0 |
| NAEE qere / Taamey D | 26.133333 | 21 | 10 | 0 | 10 | 0 |
| NAEE qere / Taamey D | 48 | 21 | 10 | 0 | 10 | 0 |
| NAEE qere / Noto Sans Hebrew | 26.133333 | 21 | 11 | 0 | 11 | 0 |
| NAEE qere / Noto Sans Hebrew | 48 | 21 | 11 | 0 | 11 | 0 |

**Property isolation for NAEE:** The positive controls reuse actual NAEE ruby HTML
and `py/near_aleppo/edition.css`, removing only the span rule introduced at
`b2001a4bad2b455eef996bf3ae1e68ca828ec817`. The original annotation span is inline
and inherits line height 1.8. The 21 controls include 20 final combining code points
and three occurrences of the Ruth 4:5 qere קָנִ֔יתָ. Display-only matches ordinary
text in every tested control; line-height-only leaves the discrepancies. This
identifies `display: inline-block` as the effective declaration in these fixtures.
It is a new property-isolation measurement, not a repeat of the earlier 309-reading
Edge survey. The existing NAEE product code remains untouched.

**Reproduction:** `py/main_clc_ruby_review.py` writes the captured corpus, detailed
JSON measurements, self-contained comparison HTML and PNG sheets only under
`.novc/clc-ruby-final-mark/`. The corpus JSON records each source page and ruby index.
The retained instrument is deliberately manual: it requires a selected browser
executable and does not belong in product regeneration. On the cloud checkout the
verified command was:

```bash
.venv/bin/python py/main_clc_ruby_review.py --baseline 3f476dedeee133d50cee8ea973c434d7ffeae4e6 --browser /usr/bin/chromium --comparison-font /usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf
```

On Windows, from the selected checkout's root, use its interpreter and installed
Edge executable; the optional comparison font can be omitted:

```powershell
& ./.venv/Scripts/python.exe py/main_clc_ruby_review.py --baseline 3f476dedeee133d50cee8ea973c434d7ffeae4e6 --browser 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
```

**Focused checks:** CLC regeneration reproduces the tracked HTML and notes JSON
byte-for-byte; the stylesheet is an authored asset, with no generated copy. Actual
pages were loaded with original and corrected CSS at widths 1280 and 390 px, in
light and dark screen modes and print mode, with loaded fonts, identical verse/ruby
markup and no script errors. The corrected real qere spans remain full size with
normal line height. In this browser the affected apparatus boxes gain 1 px of
height; their widths stay unchanged. The comparison and representative actual-page
screenshots were inspected. Focused lint/test results and final diff checks are
recorded in the repair commit. The mega and full suite remain nightly work under
`doc/review-trial.md`; no new product-wide generation is required by this CSS change.
