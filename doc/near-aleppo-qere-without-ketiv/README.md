# Near-Aleppo qere-without-ketiv manuscript readings

State: live

The maintained study is generated at
[`gh-pages/near-aleppo/foi/qere-without-ketiv.html`](../../gh-pages/near-aleppo/foi/qere-without-ketiv.html).
It is linked from the near-Aleppo FOI index and the existing ketiv/qere guide.
Ben approved this first draft on 2026-10-08: “what you propose seems fine, at least as a first draft.”
Implementation and further discussion of the readings proceed together.

Every case of קרי ולא כתיב discussed here has the expected marginal note
containing the qere letters. Also as expected, neither qere nor ketiv letters
are present in the body text. The cases differ in whether, in the body text:

- niqqud marks are present (only four of the nine cases have niqqud)
- horizontal space is present (only 1 case lacks it: 2 Samuel 18:20)
- a masorah circle is present (only 1 case lacks it: 2 Kings 19:31)

(By definition, when niqqud marks are present, these are "orphan" niqqud,
i.e. letterless niqqud.)

The study states the common features in the opening paragraph and lists all
three varying features together.
Complete MAM quotations and translations retain their circle references.
English descriptions, encoding summaries and image captions use complete
sentences. Translations retain the source's fragments and lists.
The opening feature list completes its lead-in.
The study uses an unnamed authorial voice. Reading provenance and contribution
history remain in the source records and this maintained note.

## Maintained inputs and rendering

[`in/near-aleppo/qere-without-ketiv-readings.json`](../../in/near-aleppo/qere-without-ketiv-readings.json)
owns the selected references, Ben's dated image observations, their qualifications,
and crop provenance, together with the intended encoding assessments. Update that
file as Ben supplies further readings or revises an assessment. A case without an
image reading has `reading`, `observation`, and `crop` set to `null`; the page
states that an image reading has not yet been recorded.
The v3 record format also permits a reviewed case's `observation` to be `null`
when its remarks add nothing beyond the attached MAM note. Full structured image
readings and provenance remain in `reading`; only displayed prose is trimmed.
Cases with an attached MAM note display only additional manuscript remarks.

The linked case summary table replaces the numbered verse list. Its narrow
columns use N for niqqud presence, H for horizontal space in the line
of letters, and Pos. for position. The legend defines +/− as present/absent and
BW/EOL as between written words/end of a manuscript line. The presence values
come from the three closed `intended_encoding.kind` classifications of the
recorded manuscript readings, rather than the current dataset calls. The
position comes from each reading's explicit `line_position`; a reviewed reading
without a recognized position fails the build. Unreviewed cases show question
marks, with that meaning added to the legend only when needed. The table does
not promote the tentative ḥolam male at 2 Kings 19:31 to a confirmed reading:
the recorded below-marks already establish niqqud presence.

The primary `crop` records the body-text image. It may also contain the explicitly
named `marginal_qere_note` crop, with its own filename and supplied screenshot.
The renderer validates both crop records and displays the body text and marginal
note with separate captions. Each case starts with its image or images and their
captions, immediately after the verse heading, before any encoding summary,
NAEE excerpt, MAM note or manuscript discussion. When both images are present,
the body-text image precedes the marginal-note image.
The reading's `marginal_qere_note.inferred_lines` records an inferred vertical
layout, displayed in an RTL block with one word per line. This unpointed layout
uses ordinary prose styling, without the pointed-Hebrew font or enlargement.

[`py/near_aleppo/foi_qere_without_ketiv.py`](../../py/near_aleppo/foi_qere_without_ketiv.py)
renders the study through the existing HTML build. The shared renderer supplies
current NAEE Scripture from `out/near-aleppo/plus/`, and current qere and attached
MAM doc-notes from `MAM-parsed/plus/`. It owns closed template dispatch. The FOI
selects semantic qere-only render elements and notes whose rendered lemma contains
that element. The existing closed dataset walk also selects the current qere-only
source fragment from Scripture, excluding note bodies and copied MAM lemmas.
The study validates that fragment's two literal parameters and agreement of its
whole qere with MAM. The current source notation is omitted because every selected
call's first parameter is the bracketed qere and its second parameter is the qere.
The separate “MAM qere” displays are also omitted because they repeat the qere
in each NAEE excerpt. The excerpt renderer requires exact agreement with MAM,
including every letter and mark. Quoted MAM notes retain their original text
and brackets.
Inline Hebrew with marks uses pointed styling. Unpointed Hebrew in prose inherits
the surrounding font while retaining Hebrew language metadata and RTL isolation.
Each Hebrew phrase, including its internal spaces, has one RTL isolation.

“NAEE excerpt” retains the complete chanted word containing the QVLK
and one neighboring chanted word on each side. A maqaf compound stays whole.
A verse-initial or verse-final QVLK instead retains two chanted words on the
available side. Ellipses appear only where text has been omitted; the original
sof pasuq remains when the excerpt reaches the verse ending. The short Hebrew
excerpt is centered. The renderer selects boundaries in plain Scripture and
recognized documentation-target spans, treating the validated qere-only ruby
as an opaque display. The original Hebrew, target ink and ruby nodes are retained.
The nine current QVLKs are neither verse-initial nor verse-final. Three occur
inside maqaf compounds: 2 Samuel 16:23, 2 Samuel 18:20 and Jeremiah 50:29.

[`in/near-aleppo/qere-without-ketiv-mam-notes-en.json`](../../in/near-aleppo/qere-without-ketiv-mam-notes-en.json)
owns the English translations and explanations of attached MAM notes and the
comparisons with Ben's descriptions. The English versions expand abbreviated
wording and use the note's voice. Bibliographic fragments remain fragments, and
lists of editions remain lists. A qere's agreement with a manuscript is expressed
as agreement with the qere implied by that manuscript. The brief agreement
statements do not specify whether they concern letters in the margin, niqqud in
the body text, or both;
the study preserves that uncertainty. Each translation identifies its whole
current MAM lemma and all note parts. Each note review identifies the
current observation and documentation text it assesses. The HTML build requires these subjects to
match and raises if a note or description needs reconciliation. These readable
source quotations are the subjects of the authored translations and comparisons.

The page places the English translation and explanation below each attached
Hebrew note. Comparisons record only discrepancies between MAM's note and the
manuscript remarks; agreements and summaries of facts present in only one
description are omitted. The v2 note-review format uses a `null` comparison
when no discrepancy requires a separate entry. Discrepancy blocks and their
summary appear only when entries exist. The three cases without an attached MAM
note are labelled accordingly. Hebrew body-text examples remain in RTL blocks.
The Ruth marginal-note quotations stay inline at their source position, in
ordinary prose styling, without a separate explanatory paraphrase.
At Jeremiah 31:37, the English translation adds a bracketed translator's note
immediately after MAM's body-text illustration: “[sic, missing נְאֻם־ in MAM's
illustration]”. The original Hebrew quotation remains unchanged; the annotation
identifies an omission in MAM's illustration.
The manuscript sigla follow the mirrored introduction's source roster:
`א` is the Aleppo Codex, `ל` the Leningrad Codex, and `ק` the Cairo Codex of the
Prophets. The roster's `סימנים` is the Simanim Tanakh, as specified in
`in/mam-ws-intro/appendices.mediawiki`, “סימנים=תנ"ך סימנים”.

An image reading's subject is its whole recorded qere, including every letter
and mark. A changed current qere requires reconciling that reading's subject.
There are no input hashes or fixed-population gates. The Samuel reading records
identify the MAM notes reviewed on 2026-10-08; their verbatim quotations remain in
the reading records even if the current notes later change. Recording and review
dates remain in the source metadata and are not displayed in the study.

The study's observations do not change the near-Aleppo source text or decide a
template design. Actual near-Aleppo source decisions remain in their existing
maintained inputs and procedures.

## Additional manuscript remarks, 2026-10-11

Ben requested remarks limited to additional facts, beyond what MAM's note
already says. At 2 Samuel 16:23, retain Ben's assessment that the below-marks
could have easily fit underneath the maqaf and/or the space after it, but the
naqdan declined to provide them. MAM's “narrow”
is only a possible discrepancy because its relative measure is unspecified;
the qualification stays in the remarks, without a separate comparison entry.
At Jeremiah 31:37, retain generous inter-word spacing and the qualified damage
description and inferred marginal-note layout. At Jeremiah 50:29, retain
generous spacing and the maqaf extending into it. At Ruth 3:17, retain the
end-of-line position and possible accidental generosity. The separate remarks
at 2 Samuel 18:20 and Ruth 3:5 add nothing beyond MAM and are omitted.
The three cases without an attached MAM note retain their full remarks.

## Encoding presentation, 2026-10-11

Ben requested that the encoding choices be prominent, then selected readable
summaries followed by source notation and a document-only revision. Ben later
requested that every case begin with its images on 2026-10-11. “Near-Aleppo
encoding” now follows the images, before the NAEE excerpt and manuscript
discussion. Current encoding and pending intended additional templates have
separate labels. Ben requested removal of the repeated source-notation blocks
on 2026-10-11 because they add no independent information beyond the MAM qere.
The separate MAM qere displays were subsequently removed after a comparison
confirmed agreement with the NAEE qere in all cases.
All current source fragments are read afresh from `out/near-aleppo/plus/`; they
are not copied into the study metadata.

The study's `intended_encoding` is either `null` for an
entry awaiting a manuscript-based assessment, or an object with `kind` and
`explanation`. The three closed kinds are `marks-with-space`,
`marks-without-space` and `space-without-marks`. These are document assessments, not build
instructions. All nine selected cases now have recorded image readings and
pending encoding assessments. Existing observations and crop provenance are
preserved.

Ben clarified on 2026-10-11 that every existing `קרי ולא כתיב` call is to be
retained and supplemented with one additional template describing how the qere
site is represented in the body text. The additional template records the niqqud
present and whether horizontal space is present. The additional template does
not replace the existing call or remove the qere. The earlier “empty body text”
assessment is superseded by “horizontal space without niqqud”; an unpointed space
still needs an additional template.

The introduction describes the near-Aleppo-specific templates `ניקוד בלי אות`
and `ניקוד בלי אות ובלי רווח`, including the artificial carrier convention, as
candidates for additional templates where marks are present. Judges 20:13,
2 Kings 19:31 and 2 Kings 19:37 have horizontal space above the marks. The tentative
ḥolam male reading at 2 Kings 19:31 leaves the carrier payload unsettled. The
additional template without space above the marks at 2 Samuel 18:20 still awaits
an explicit variant for that use. The additional template at 2 Samuel 16:23,
Jeremiah 31:37, Jeremiah 50:29, Ruth 3:5 and Ruth 3:17 must record horizontal space
without niqqud. The additional template's name and syntax
remain open. Current encodings are summarized without repeated source notation;
pending names, parameter shapes and call placement remain to be designed. Dataset
implementation remains separate.

“Space above the marks” means horizontal space in the line of letters, left
between words or at the end of a manuscript line. At a line ending, the space
may have been left on purpose or may be accidental. The two end-of-line cases
are Judges 20:13 and Ruth 3:17. None of the cases in this study is at the start
of a manuscript line. The recorded observations and all nine body-text crops
were consulted for this clarification on 2026-10-11.

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
2026-10-08 and the remaining crops on 2026-10-11.
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
| Jeremiah 50:29 | [aleppo-Je50-29.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-Je50-29.png) | `Screenshot 2026-10-11 122253.png` |
| Ruth 3:5 | [aleppo-R3-5.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-R3-5.png) | `Screenshot 2026-10-11 122537.png` |
| Ruth 3:17 | [aleppo-R3-17.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-R3-17.png) | `Screenshot 2026-10-11 122806.png` |

## Judges 20:13

Ben read the below-marks of בְּנֵ֣י: sheva, tsere, and munaḥ, without letters or
dagesh, with space above the marks. The orphan marks are at the end of a manuscript
line. The line ending provided space for the marks, possibly accidentally,
as Ben clarified on 2026-10-11.

There is no dagesh for the qere in the body text, as expected. Ben's clarification
is that dagesh marks are never included in cases of qere without ketiv.

The historical review page,
`qere-without-ketiv-all-cases.html` in the Downloads editing bundle, displayed
each group of combining marks on an ASCII space (U+0020). The spaces' count and
width are display conventions, not measurements of physical manuscript spacing
or a proposed template design. The record preserves that display text and its
mark order as historical documentation.

## 2 Samuel 16:23

Ben clarified on 2026-10-11 that the below-marks of איש (ḥiriq and tipeḥa)
could have easily fit underneath the maqaf and/or the space after it, but the
naqdan declined to provide those below-marks. The reading record attributes
this assessment to Ben and preserves the earlier space and letter-fit readings.
MAM's characterization of the space as “narrow” is slightly puzzling. Perhaps
“narrow” refers to the room needed for the letters rather than the room needed
for the points alone. The dated MAM quotation is stored in
`reading.reviewed_mam_note`.

## 2 Samuel 18:20

Ben agrees with the MAM note reviewed on 2026-10-08. The tsere and merkha of
כֵּ֥ן are present below, between the surrounding written atoms, without the qere
letters or dagesh. In particular, no space lies above the marks. The dated MAM
quotation is stored in `reading.reviewed_mam_note`.

## 2 Kings 19:31

Ben clarified on 2026-10-11 that the gap is very generous compared with the
manuscript's usual small or nonexistent spaces between written atoms. The
letter-scribe clearly intended to leave a large gap; perhaps the qere letters
could have fit. All the below-marks of צְבָא֖וֹת are present: sheva, qamats, and
tipeḥa. A ḥolam male dot also seems to be represented. The letter-fit assessment
and the dot reading remain tentative; the record does not promote the dot to a
confirmed manuscript reading.

Ben clarified on 2026-10-11 that no masorah circle is present. The source reading
records that absence and its provenance; the study names this exception once
in the introduction.

## 2 Kings 19:37

Ben read the marks of בָּנָיו֙: qamats, qamats, and pashta, without letters,
with space above the marks. The marks occupy a large horizontal space between
the surrounding written atoms. Ben's hypothesis is that the letter-scribe
presumably left this space intentionally. The intended additional template records
niqqud with horizontal space above the marks; dataset implementation remains pending.

## Jeremiah 31:37

Ben read a rather generous horizontal space for בָּאִ֖ים between the surrounding
written atoms, with no qere letters or niqqud. Ben describes the marginal-note
damage as looking as if opaque tape
had been laid parallel to the right margin, obscuring approximately the first
letter of each inferred word on its own line. The cause of the damage is unknown.
The tape comparison describes how the damage looks; it does not propose a
mechanism.
Ben infers the following vertical layout, recorded exactly as supplied:

<div dir="rtl" lang="hbo">
באים<br>
קרי<br>
ולם<br>
כתב
</div>

Both supplied crops are preserved and displayed separately. The intended
additional template records horizontal space without niqqud; dataset implementation
remains pending.

## Jeremiah 50:29

Ben read a generous horizontal space for לָהּ֙ between the surrounding written
atoms, with no qere letters or niqqud. The preceding maqaf extends into that
space. The intended additional template records horizontal space without niqqud;
dataset implementation remains pending.

## Ruth 3:5

Ben read a generous horizontal space for אֵלַ֖י between the surrounding written
atoms, with no qere letters or niqqud. The intended additional template records
horizontal space without niqqud; dataset implementation remains pending.

## Ruth 3:17

Ben read a generous horizontal space for אֵלַ֔י at the end of a manuscript line,
with no qere letters or niqqud. Ben's hypothesis is that
the line ending may account for the generous space, possibly accidentally.
The intended additional template records horizontal space without niqqud; dataset
implementation remains pending.

## Historical standalone review

The Downloads editing bundle remains a historical snapshot. Its frozen source
packets, delivered HTML, reconstructed generator, and later local edits were not
deleted. Ongoing manuscript observations are now maintained in the tracked FOI
records and this source note. The standalone generator's README points here.
