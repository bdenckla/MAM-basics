# Updates to the meteg-after-silluq report for UXLC and WLC

State: open, first entry 2026-09-13. Every entry here corrects or supplements
`doc/meteg-after-silluq-in-uxlc-and-wlc.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written. A correction or later disposition goes in a
sibling file named `<stem>-update.md`, which is what this file is for that report.

## Finding 11.5: narrative romanizations should use `pataḥ` and `ḥataf`

Recorded by Codex on 2026-09-13. A fresh census found two `patah` sites and two `hataf` sites in
the finished report. The corrected readings are:

1. In the opening **Terms** paragraph, “a furtive patah” should read “a furtive pataḥ,” and “a
   sheva or a hataf” should read “a sheva or a ḥataf.”
2. In section 8's **Syllables** item, “a furtive patah” should read “a furtive pataḥ,” and “a
   sheva or a hataf” should read “a sheva or a ḥataf.”

The finished report's substantive bytes match historical blob
`fad8f1836286e3fbb76ce0da39918f23cdb9e4b9`; its only additional line is the authorized update
pointer.

## 1 Samuel 17:5: Koren and the Simanim Tanakh have the silluq alone

Recorded from Ben's readings on 2026-09-21. Koren and the Simanim Tanakh each have only one
metsil in **נְחֹֽשֶׁת׃**. Because this verse-final word has only one metsil, the mark is the
silluq. The silluq is on **ח** (xet), as expected. This establishes both printed editions on the
no-later-metsil side of the contrast with the Leningrad Codex.

## 1 Kings 14:14: Koren and the Simanim Tanakh have the silluq alone

Recorded from Ben's readings on 2026-09-21. Koren and the Simanim Tanakh each have only one
metsil in **גַּם־עָֽתָּה׃**: the silluq on **ע** (ayin), as expected.

UXLC 3.9 acquired its second metsil through Daniel Holman's
[change proposal 2022.08.31-17](https://tanach.us/Changes/2022.12.07%20-%20Changes/2022.12.07%20-%20Changes.html?2022.08.31-17).
The record proposes adding a meteg under the tav and changes the complete chanted word from
**גַּם־עָֽתָּה׃** to **גַּם־עָֽתָּֽה׃**. Ben independently inspected the manuscript image supplied
with the change record on 2026-09-21 and concludes that UXLC's form is the content of the
Leningrad Codex. The second metsil is likely a meteg after silluq; Breuer also notes this second
metsil in *Da'at Miqra*.

The Leningrad Codex is therefore classified on the later-metsil side, and Koren and the Simanim
Tanakh are classified on the no-later-metsil side. WLC remains a transcription that records only
the earlier mark; WLC's form is not evidence against Ben's independent reading of the manuscript.

The finished report's summary item 3 should now say that three of the five class 1 cases are
settled from manuscript images: 1 Samuel 17:5, 1 Kings 14:14 and Psalms 72:15. The remaining two
cases for manuscript inspection are Psalms 60:10 and Psalms 70:2. The lead of section 6 should
likewise say “the other two,” not “the other three.”

## Complete chanted-word forms in the seven-case register

Audited by Codex on 2026-09-21 against the tracked MAM-simple and UXLC 3.9 data. Six of the seven
case-register forms were already complete chanted words. Only 1 Kings 14:14 had been reduced to
its final atom in the generated page.

Two atom-only forms in the finished report should also be read as complete chanted words:

1. In section 3, item 2, “It changes **עָֽתָּה׃** to **עָֽתָּֽה׃**” should read “It changes
   **גַּם־עָֽתָּה׃** to **גַּם־עָֽתָּֽה׃**.”
2. In section 6, the column heading “MAM's final atom” should read “MAM's verse-final chanted
   word,” and the 1 Kings 14:14 form should be **גַּם־עָֽתָּה׃**, not **עָֽתָּה׃**.

The maintained generator now takes the final atom together with every preceding atom joined to
it by maqaf, so a future case-register form cannot silently lose the beginning of a compound.
