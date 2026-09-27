# Updates to turn 01 of the 2026-09-26 dual-agent review

State: open, first entry 2026-09-27. Every entry here corrects or supplements
`doc/dual-agent-review-2026-09-26-turn-01-claude.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit. A
correction, later decision or later disposition goes in a sibling file named `<stem>-update.md`,
which is what this file is for turn 01 of the September 26 review.

## Ben's first close-out decisions and a finding he added, 2026-09-27

Recorded by a Claude session on 2026-09-27, New York time: the session that wrote turn 05 of the
round. The alternating exchange was then waiting for Codex's turn 06, which records an
acknowledgment of turn 05 or an objection to it, and close-out step 1 had not begun. Ben answered
every question that turn 05's section "Close-out step 1's list after this turn" put to him, and he
added a finding of his own. He also asked where his answers were kept: "I don't like that my
decision is recorded here. How will Codex know to record it?" This entry is the record. It records
decisions and executes no remediation.

1. **Finding 30.3, the Cairo captions: standardize on "digital page".** Turn 05 said that only Ben
   could say whether the CSIC viewer's "digital image" and "digital page" name the same field. Ben,
   2026-09-27:

   > Yes, both descriptions are acceptable (though of course it is preferable to standardize on
   > one of the two; I am indifferent between them). In other words, this is not one of those sets
   > of manuscript images where the image is of a page-spread instead of a page. That is the main
   > way I'm aware of in which images do not correspond to pages.

   The session suggested "digital page", which the 1 Kings 7:37 Cairo caption and both EVR
   captions already use, and Ben replied:

   > I agree to the term "digital page."

   At `f4d81285` the change reaches two captions: "Cairo, digital image 204"
   (`gh-pages/post-stress-meteg-post-silluq-1k14v14.html:23`, from
   `py/author_site/post_stress_meteg_post_silluq_page.py:282`) and "Cairo, manuscript page 110,
   digital image 103" (`gh-pages/post-stress-meteg-post-silluq-1s17v5.html:25`, from line 229 of
   the same module). The decision concerns the published captions, which are finding 30.3's
   subject. Whether the provenance records and the image file names, which also say "digital
   image" or "image", follow is for the remediation plan to propose.
2. **Finding 4.2: restore the `@media` prohibition.** Ben chose, on 2026-09-27, to restore the
   sentence that `4e30b0f4` deleted, answering "I concur." to the session's option "Restore the
   sentence (recommended).", which proposed this wording for the CSS rule in `holman/WORKFLOW.md`:

   > Every authored CSS theme declares `color-scheme: light dark` on `:root`, and every theme
   > custom property that stores a color uses a `light-dark(<light>, <dark>)` pair. Fixed badge
   > foregrounds and backgrounds remain literal colors. Do not add an
   > `@media (prefers-color-scheme: dark)` block.

   The comma after `` `:root` `` repairs finding 4.2's textual defect. The session's reasons for
   recommending the restoration: the two authored Holman stylesheets handle dark mode only through
   `color-scheme: light dark` and `light-dark()` pairs, and neither has a dark-mode `@media` block;
   `py/py_render/rt_assets.py:8–10` keeps the same prohibition for generated report assets; and
   the one dark-mode `@media` block on the site, `gh-pages/wlc/style.css:413–418`, sets a
   `filter` on opted-in scans, which `light-dark()` cannot express because it chooses only colors.
3. **Finding 36, added by Ben: `holman/assets/table_data_findings.css` has too generic a name.**
   Ben, 2026-09-27:

   > That has become a terrible (too generic) file name BTW. Since a CSS file isn't really going
   > to be used in a URL, I think we are free to change it to something better, no? Let's record,
   > as part of this review, that "bad name" as a human-generated finding.

   The file lies outside the window's diff: no commit in `71f96ca3..f4d81285` changed it or its
   published copy. The facts a rename needs, at `f4d81285`:
   1. In the tree, the published copy `gh-pages/holman/table_data_findings.css` is requested only
      by the stylesheet links of the two pages that use it,
      `gh-pages/holman/table_data_findings.html:17` and
      `gh-pages/holman/table_data_findings_suppressed.html:17`.
   2. Its JavaScript twin, `holman/assets/table_data_findings.js`, has the same name; both
      template paths are set at `py/py_render/rt_assets.py:43–44`.
   3. The published CSS and JavaScript names are derived from the page's name, by
      `output_html_path.with_suffix(".css")` and `.with_suffix(".js")`
      (`py/py_render/rt_html.py:120–121`), and the page's name is fixed on purpose. A comment
      beside Ben's decision of 2026-09-03 on the page's title says "The FILENAME is unchanged,
      deliberately: table_data_findings.html is the URL index.html links and the one Ben has
      already sent to correspondents" (`py/py_render/rt_html.py:58–60`). A new name for the
      published copies therefore has to be decoupled from
      the page's name; renaming only the authored templates in `holman/assets/` needs no such
      change. `py/main_0_mega.py:572` describes the step's outputs as "the
      gh-pages/holman/table_data_findings* pages with their CSS and JS".
   4. Finished records that cite the old path, among them
      `doc/dual-agent-review-2026-09-16-turn-01-claude.md:1085`, stay as written under D12.

   The new name, and whether the JavaScript twin and the published copies take it too, are Ben's
   choice in remediation, as an editorial change under D7.
4. **Finding 30.3, the Leningrad captions: a side-lettered designation names a page, and the
   "folio 159A" form is avoided.** The session asked whether the 1 Samuel 17:5 caption should say
   "folio 159A", like the five other Leningrad captions, or keep "F159A". Ben, 2026-09-27:

   > Call it ither page F159A or just call it F159A. Do not call F159A. By our
   > newly-decided-upon terminology, F159 is the folio, it has an A and a B page (a recto and a
   > verso) that belong to it.

   Later the same day he added how the avoided form is to be read where others use it:

   > One more note regarding phrases like "folio 57a". I think we should avoid them, but they are
   > common in existing references in published books and web sites. They should be taken to
   > imply a parenthesized meaning of "(folio 57)a" meaning, somewhat visually
   > counterintuitively, that the "folio operator" binds more tightly than the a/b operator.

   The quotations are exact; the third sentence of the first says why "folio 159A" is excluded.
   The caption's "F159A" is therefore one of the two forms Ben allows, "page F159A" is the other,
   and the session's suggestion of "folio 159A" is withdrawn. The tree already defines a page as
   one side of a folio (`doc/meteg-after-silluq-snips/README.md:52`, `evr-ii-b-55/README.md:163`).
   Read as "(folio 57)a", the "folio 57a" form states nothing false, but it is the form this
   repository's own prose avoids. The captions that use it, or its "leaf" variant, are the five
   other Leningrad captions, "folio 195B", "folio 398A", "folio 377B", "folio 379B" and "folio
   380A"; the EVR caption's "folio 57a" (`gh-pages/post-stress-meteg-post-silluq-1s17v5.html:33`);
   and the five Aleppo captions that write "leaf", as in "leaf 83r"
   (`gh-pages/post-stress-meteg-post-silluq-1k14v14.html:17`). Cambridge's "page 0073B" already
   follows the terminology. The remediation plan proposes the wording for each caption, and for
   the tree's own records that use the form, such as "folio 159A" and "folio 195B" at
   `doc/meteg-after-silluq-in-uxlc-and-wlc.md:84–85`, for Ben's approval under D7. A quotation or
   citation of a published source keeps that source's wording. The terminology has no standing
   home in the repository's instructions or skills yet; whether to give it one is for the
   remediation plan to ask.

With this entry, every question that turns 03 to 05 put on close-out step 1's list has Ben's
answer. Every other finding reaches close-out step 1 as the reconciliation table and turns 03 to
05 leave it, and finding 36 joins that list.
