# Near-Aleppo qere-without-ketiv manuscript readings

State: live

The maintained study is generated at
[`gh-pages/near-aleppo/foi/qere-without-ketiv.html`](../../gh-pages/near-aleppo/foi/qere-without-ketiv.html).
It is linked from the near-Aleppo FOI index and the existing ketiv/qere guide.
Ben approved this first draft on 2026-10-08: “what you propose seems fine, at least as a first draft.”
Implementation and further discussion of the readings proceed together.

## Maintained inputs and rendering

[`in/near-aleppo/qere-without-ketiv-readings.json`](../../in/near-aleppo/qere-without-ketiv-readings.json)
owns the selected references, Ben's dated image observations, their qualifications,
and crop provenance, together with the intended encoding assessments. Update that
file as Ben supplies further readings or revises an assessment. A case without an
image reading has `reading`, `observation`, and `crop` set to `null`; the page
states that an image reading has not yet been recorded.

The primary `crop` records the body-text image. It may also contain the explicitly
named `marginal_qere_note` crop, with its own filename and supplied screenshot.
The renderer validates both crop records and displays the body text and marginal
note with separate captions.

[`py/near_aleppo/foi_qere_without_ketiv.py`](../../py/near_aleppo/foi_qere_without_ketiv.py)
renders the study through the existing HTML build. The shared renderer supplies
current NAEE Scripture from `out/near-aleppo/plus/`, and current qere and attached
MAM doc-notes from `MAM-parsed/plus/`. It owns closed template dispatch. The FOI
selects semantic qere-only render elements and notes whose rendered lemma contains
that element. The existing closed dataset walk also selects the current qere-only
source fragment from Scripture, excluding note bodies and copied MAM lemmas.
The study validates that fragment's two literal parameters and agreement of its
whole qere with MAM, then shows both parameters in complete curly-brace notation.
The ordinary HTML writer escapes the notation as text.

An image reading's subject is its whole recorded qere, including every letter
and mark. A changed current qere requires reconciling that reading's subject.
There are no input hashes or fixed-population gates. The dated Samuel comparisons
identify the MAM notes reviewed on 2026-10-08; their verbatim quotations remain in
the reading records even if the current notes later change.

The study's observations do not change the near-Aleppo source text or decide a
template design. Actual near-Aleppo source decisions remain in their existing
maintained inputs and procedures.

## Encoding presentation, 2026-10-11

Ben requested that the encoding choices be prominent, then selected readable
summaries followed by source notation and a document-only revision. Each entry
now starts with “Near-Aleppo encoding”, before the full verse and manuscript
discussion. Current encoding and pending intended encoding have separate labels.
All current source fragments are read afresh from `out/near-aleppo/plus/`; they
are not copied into the study metadata.

The study's v2 record format adds `intended_encoding`: either `null` for an
entry awaiting a manuscript-based assessment, or an object with `kind` and
`explanation`. The three closed kinds are `marks-with-space`,
`marks-without-space` and `empty-body`. These are document assessments, not build
instructions. All six reviewed cases have pending assessments; the three entries
awaiting image readings have `null`. Existing observations and crop provenance
are preserved.

The introduction explains the near-Aleppo-specific templates `ניקוד בלי אות`
and `ניקוד בלי אות ובלי רווח`, including the artificial carrier convention.
Judges 20:13, 2 Kings 19:31 and 2 Kings 19:37 take the intended template with
space above the marks. The tentative holam reading at 2 Kings 19:31 leaves its
payload unsettled.
The intended template without space above the marks at 2 Samuel 18:20 still
awaits its own variant and implementation. The intended body text is empty at
2 Samuel 16:23 and Jeremiah 31:37. Complete notation is shown only for current
encodings; no pending carrier payload is invented. Dataset implementation remains
separate.

## Link presentation trial, 2026-10-11

Ben requested research and implementation of an alternative to ordinary link
underlines on this page. On 2026-10-11 Ben approved the presentation and requested
its adoption across the near-Aleppo pages. The rollout is recorded below.
Trial development and integration used `C:/Users/BenDe/GitRepos/MAM-basics`, a clean
full clone on main at `79c923957188007a2ffd70dd6ece60103cbeec97` before editing.
Codex owns implementation, focused regeneration, verification, commit and push.

The [Wikimedia link guide](https://doc.wikimedia.org/codex/latest/style-guide/using-links-and-buttons.html)
uses un-underlined links by default, underlines on hover, and an external-link
icon alongside the label. A live inspection of
[Wikisource's editing help](https://en.wikisource.org/wiki/Help:Editing) confirmed
that its named external-link example is one anchor with no ordinary underline and
a trailing SVG arrow supplied as a CSS background. The arrow is not a separate link.

Other systems make different choices.
[GOV.UK](https://design-system.service.gov.uk/styles/links/) keeps default
underlines and reserves their removal for contexts where links are already clear.
[GitHub's Primer](https://primer.style/accessibility/patterns/primer-components/links/)
also permits an icon, background shape or outline as a visual link cue.
[W3C's guidance](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
requires information conveyed by color to have a visible alternative to color.

Current MAM-basics precedents include hover-only underlines for references and
note targets in `gh-pages/uxlc/style.css`, bordered navigation links in
`gh-pages/report.css`, and compact reference links in
`py/mb_diff_mpu/mpplus_assets.py`. The permalink anchors in
`py/accgram/poetic_oddballs.py` use an icon with an accessible label. The research
found no current authored trailing external-arrow presentation.

The trial uses un-underlined labels with trailing markers: a down arrow for a
same-page jump, a right arrow for another MAM-basics page, and a boxed outward
arrow for the mgketer.org and masoretica-aleppo destinations. The label and marker
remain one clickable link. Link colors distinguish visited destinations; hover
adds a background and keyboard focus adds an outline. This intentionally keeps
underlines off on hover as well, using the marker and highlight as the cues.
The empty decorative pseudo-elements do not alter accessible names or copied text.

The trial's link rules were initially embedded from
[`py/near_aleppo/foi_qere_without_ketiv.css`](../../py/near_aleppo/foi_qere_without_ketiv.css).
That file now owns only the study's layout. The small geometric SVGs are authored
locally and use no remote asset. Offline body comparison, SVG validation and
declared-color contrast checks covered the preserved content and self-contained
assets. Browser security policy blocked automated local visual and keyboard
verification because it disallows `file:` URLs. Ben subsequently reviewed and
approved the presentation; no automated browser pass is claimed.

## Shared near-Aleppo link presentation, 2026-10-11

The shared rules now cover all 77 HTML pages under `gh-pages/near-aleppo/`,
including documentation, FOI pages, edition pages and their long notes. The
completed standalone final-punctuation review extract also received these rules
before its retirement on 2026-10-11. The authored sources are
[`py/near_aleppo/link_presentation.py`](../../py/near_aleppo/link_presentation.py)
and [`py/near_aleppo/link_presentation.css`](../../py/near_aleppo/link_presentation.css).
The HTML build writes one shared stylesheet. The top-level MAM-basics index
also uses this stylesheet.

Same-page links use an up arrow when the target precedes the link in document
order, and a down arrow when the target follows it. This direction is assigned
during generation and needs no browser script. Links to other MAM-basics pages
retain the right arrow; links outside MAM-basics retain the boxed outward arrow.
The three backward section links under “Notes for applications” in
[`reading-json.html`](../../gh-pages/near-aleppo/reading-json.html) demonstrate the
up arrow. Labels and arrows remain one link, with the trial's hover, focus,
visited, forced-color and print behavior.

The rollout preserves Hebrew order, RTL markup, page text, link labels and URLs,
observations, crops, datasets and template policy. Verification compares every
page's body byte-for-byte after removing only the presentation attributes,
checks every local fragment and arrow direction, validates the self-contained
SVGs, and runs the real HTML comparison. Automated visual and keyboard checks
retain the browser-policy limitation described above.

## Reproduction

Run from the MAM-basics repository root in PowerShell 7:

```powershell
& "$HOME/GitRepos/MAM-basics/.venv/Scripts/python.exe" "$HOME/GitRepos/MAM-basics/py/main_near_aleppo.py" --html
```

The corresponding read-only comparison is:

```powershell
& "$HOME/GitRepos/MAM-basics/.venv/Scripts/python.exe" "$HOME/GitRepos/MAM-basics/py/main_near_aleppo.py" --html --check
```

## Crop provenance

Ben supplied and interpreted the first four Aleppo manuscript crops below on
2026-10-08, and the 2 Kings 19:37 and Jeremiah 31:37 crops on 2026-10-11.
Codex inspected the supplied crops. The canonical PNG files are under
[`in/near-aleppo/img/qere-without-ketiv/`](../../in/near-aleppo/img/qere-without-ketiv/),
and the HTML build copies their unchanged bytes under
`gh-pages/near-aleppo/img/qere-without-ketiv/` for inline display. These small crops
follow the established manuscript-crop fair-use convention recorded in
[`doc/meteg-after-silluq-snips/README.md`](../meteg-after-silluq-snips/README.md).
The supplied screenshot names identify the captures; no manuscript page, column,
or line coordinate is inferred from a screenshot filename.

| Entry | Canonical crop | Supplied screenshot |
| --- | --- | --- |
| Judges 20:13 | [aleppo-Ju20-13.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-Ju20-13.png) | `Screenshot 2026-10-08 105138.png` |
| 2 Samuel 16:23 | [aleppo-2S16-23.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2S16-23.png) | `Screenshot 2026-10-08 105548.png` |
| 2 Samuel 18:20 | [aleppo-2S18-20.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2S18-20.png) | `Screenshot 2026-10-08 110056.png` |
| 2 Kings 19:31 | [aleppo-2K19-31.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2K19-31.png) | `Screenshot 2026-10-08 110419.png` |
| 2 Kings 19:37 | [aleppo-2K19-37.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2K19-37.png) | `Screenshot 2026-10-11 120243.png` |
| Jeremiah 31:37, body text | [aleppo-Je31-37.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-Je31-37.png) | `Screenshot 2026-10-11 121352.png` |
| Jeremiah 31:37, marginal qere note | [aleppo-Je31-37-marginal-qere.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-Je31-37-marginal-qere.png) | `Screenshot 2026-10-11 121420.png` |

## Judges 20:13

Ben read the below-marks of בְּנֵ֣י: sheva, tsere, and munaḥ, without letters or
dagesh, with space above the marks. The orphan marks are at the end of a manuscript
line. Ben's hypothesis is that the line ending may have provided that space,
possibly accidentally.

Ben also reported a masorah circle above the marks. The circle is documented but
not encoded in the written-form record. The historical review page,
`qere-without-ketiv-all-cases.html` in the Downloads editing bundle, displayed
each group of combining marks on an ASCII space (U+0020). The spaces' count and
width are display conventions, not measurements of physical manuscript spacing
or a proposed template design. The record preserves that display text and its
mark order as historical documentation.

## 2 Samuel 16:23

Ben read a fairly generous space even after the maqaf, with no pointing for
אִ֖ישׁ. The space is insufficient for the letters of איש, but ample for its
below-marks, ḥiriq and tipeḥa. Available room does not establish the marks as present.
Ben questions whether “narrow” fits the space described in the MAM note reviewed
on 2026-10-08. That dated quotation is stored in `reading.reviewed_mam_note`.

## 2 Samuel 18:20

Ben agrees with the MAM note reviewed on 2026-10-08. The tsere and merkha of
כֵּ֥ן are present below, between the surrounding written atoms, without the qere
letters or dagesh. In particular, no space lies above the marks. The dated MAM
quotation is stored in `reading.reviewed_mam_note`.

## 2 Kings 19:31

Ben read very generous spacing for צְבָא֖וֹת, with all its below-marks present:
sheva, qamats, and tipeḥa. Perhaps the qere letters could have fit. A ḥolam male dot
also seems to be represented. The letter-fit assessment and the dot reading remain
tentative; the record does not promote the dot to a confirmed manuscript reading.

## 2 Kings 19:37

Ben read the marks of בָּנָיו֙: qamats, qamats, and pashta, without letters,
with space above the marks. The marks occupy a large horizontal space between
the surrounding written atoms. Ben's hypothesis is that the letter-scribe
presumably left this space intentionally. The intended encoding assessment uses
the template with space above the marks; dataset implementation remains pending.

## Jeremiah 31:37

Ben read a rather generous horizontal space for בָּאִ֖ים between the surrounding
written atoms, with no qere letters or niqqud. A masorah circle is present in
that space. The marginal qere note is partly cut off by damage, so some of its
letters are inferred. Both supplied crops are preserved and displayed separately.
The intended body encoding assessment is empty; dataset implementation remains
pending.

## Entries awaiting image readings

The study also includes Jeremiah 50:29, Ruth 3:5,
and Ruth 3:17. Their current NAEE verses, qere, and any attached MAM notes are
displayed. No new image reading or crop has yet been supplied for these entries.

## Historical standalone review

The Downloads editing bundle remains a historical snapshot. Its frozen source
packets, delivered HTML, reconstructed generator, and later local edits were not
deleted. Ongoing manuscript observations are now maintained in the tracked FOI
records and this source note. The standalone generator's README points here.
