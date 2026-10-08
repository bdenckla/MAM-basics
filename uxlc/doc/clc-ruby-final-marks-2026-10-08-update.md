# CLC ruby final marks: later status

State: open; first entry 2026-10-08

## 2026-10-08 — Align annotation spacing with near-Aleppo

**Implemented on the same isolated branch:** Ben requested near-Aleppo's line
height and clearance between ketiv and qere, both to improve mark clearance and
to keep their formatting in sync. This follow-up starts at
`6b4f388d5442bbc0352ae0de3d5d24bce9874f3d` in `/workspace/MAM-basics`, on
`codex/clc-ruby-final-mark`. The earlier receipt's “no line-height override is
needed” concerns the final-mark repair. The annotation spacing now changes by this
separate request; that original property-isolation finding still stands.

In the authoritative `gh-pages/uxlc/style.css`, CLC now follows
`py/near_aleppo/edition.css`'s annotation structure:

```css
ruby.clc-kq {
    ruby-position: over;
    white-space: nowrap;
}
ruby.clc-kq > rt {
    font-size: 100%;
    line-height: 1.8;
    font-weight: normal;
    padding-bottom: 0.2em;
}
ruby.clc-kq > rt > span {
    display: inline-block;
    line-height: normal;
}
```

The existing `ruby.clc-kq span.clc-kq-q { display: inline-block; }` remains in
place. The lower qere keeps normal line height. CLC's upper ketiv receives the
same outer line height, padding and normal inner text line that NAEE gives its
upper qere. NAEE's `white-space: nowrap` also keeps each reading and absence
placeholder together. Without it, the newly blocked upper `[אין כתיב]` span
wraps onto two lines even in a wide page; the rule prevents that observed side
effect without changing a text space. The readings' roles, Hebrew text, font
bytes and renderer are unchanged; no near-Aleppo product or concurrent
documentation work is edited.

**Measured clearance:** Chromium `151.0.7922.173` on Linux, loaded Taamey D,
device scale factor 1, all 176 existing CLC units. Before/after fixtures preserve
the actual pair's HTML and RTL direction. The two reading rasters are captured
separately without removing either reading's layout; black pixels below threshold
170 determine the empty horizontal strip between the closest ink rows. This is
an ink-clearance measurement, not simply the declared padding or text-line boxes.

| Reading size (px) | Minimum ink gap before (px) | Minimum ink gap after (px) |
| ---: | ---: | ---: |
| 20 | 1 | 10 |
| 26.133333 | 2 | 12 |
| 48 | 3 | 24 |

The closest pair at all sizes is 2 Samuel 3:25. No thresholded ink overlap was
detected before or after in this corpus. The observations establish increased
clearance in the tested browser and sizes, rather than proving that prior
collisions occurred or that every possible font/browser/corpus is collision-free.
CLC's ketiv annotations are mostly unpointed; hypothetical upper below-marks are
not asserted to be present. Dense pointed-base cases at Genesis 13:3 and
2 Samuel 13:8 and the closest pair were inspected. A formatting control using
the same CLC pair under the existing NAEE annotation rules gives the same minimum
gaps and text-line geometry; it does not swap CLC's readings or edit NAEE.

**Final-mark regression evidence:** The retained
`py/main_clc_ruby_review.py` now includes a `current` column rendered with the
working checkout's complete stylesheet, including its new spacing. All 176 lower
qere and all 176 upper reading/placeholder slots match ordinary-text controls
within one pixel at 20, 26.133333 and 48 px, for both Taamey D and Noto Sans Hebrew
Regular. The original/display-only/line-height-only/both comparisons remain;
adding spacing has not revived the displacement.

```bash
.venv/bin/python py/main_clc_ruby_review.py --baseline 3f476dedeee133d50cee8ea973c434d7ffeae4e6 --browser /usr/bin/chromium --comparison-font /usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf --sizes 20 26.1333333333 48
```

The complete current stylesheet is embedded in each generated review HTML. Local
spacing sheets, detailed gap results, inspected screenshots and the scratch
reproduction script are retained under `.novc/clc-ruby-spacing/`; the ordinary-text
regression evidence remains under `.novc/clc-ruby-final-mark/`.

**Actual pages and checks:** Original and updated CSS were compared on all seven
existing CLC HTML pages, at widths 1280 and 390 px and all three reading sizes.
Readings remain full size and RTL, the outer annotation has the requested line
height and padding, verse and ruby markup is identical, fonts are loaded and no
script errors occurred in the 84 page loads. Every nonempty reading text node
occupies one fragment after the change. The inspection includes dense-case
screenshots in both viewport widths and the actual absence-placeholder case at
2 Samuel 16:23.

**Measured layout limit:** Apparatus widths are unchanged in the wide pages and
the narrow pages at 20 and 26.133333 px. At 48 px in the narrow page, the
2 Samuel 21:12 multiword pair stays together and is 2.125 px wider; its box
height falls from 224 to 133.59375 px because the readings no longer split across
lines. Other boxes grow by up to 34.59375 px for the added vertical clearance.
Across all seven pages, the maximum narrow-page body width is 351 px at the
two smaller sizes, unchanged. At 48 px it was already 459 px before and is
461 px after, so horizontal scrolling remains necessary at that extreme size.
This change supplies clearance and keeps the apparatus together; it does not
promise that enlarged text fits every viewport.

**Focused checks passed:** `.venv/bin/python py/main_clc.py all` regenerated all
five main pages, their notes JSON and the two long-note pages byte-identically.
`.venv/bin/python py/main_test.py py/tests/clc_kq_test.py
py/tests/test_shared_html_styles.py py/tests/test_mega_coverage.py -q` passed all
14 tests. Black at its defaults left the modified Python file unchanged, and
`git diff --check` passed. Full mega and suite remain nightly checks under the
approved trial.

Concurrent main commit `eb0f9c1b1eaeb4d373f098740a4acdb277c78db4` was merged
unchanged into this review branch. Its near-Aleppo boxing work retains the same
outer line-height/padding declarations used here; its annotation adds explicit
`nowrap`, which CLC inherits from its ruby. The follow-up's owned diff contains
only CLC CSS, the existing manual review instrument and this receipt family.
The branch is pushed for review; main integration and deployment remain outside
this task's authorization.
