# Updates to the Job 4:12 meteg-after-silluq report

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/meteg-after-silluq-job-4-12.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written. A correction or later disposition goes in a
sibling file named `<stem>-update.md`, which is what this file is for that report.

## Finding 11.4: the five possession verbs should read “has”

Recorded by ChatGPT-Codex on 2026-09-12. All five cited sites are the report's analytic prose rather than
protected quotations. The passages should be read with these five corrections:

1. The clause “MAM copies the meteg as the Aleppo Codex has it wherever that manuscript survives”
   should read “MAM has the meteg as the Aleppo Codex has it wherever that manuscript survives”.
2. The sentence containing “In all four rows MAM marks the stress” should read “In all four rows
   MAM has the stress on the syllable before the suffix, and Phonetic MAM's `jta` puts it there
   too.”
3. The clause “UXLC codes the Leningrad Codex's stroke on the mem as a leading meteg” should read
   “UXLC has the Leningrad Codex's stroke on the mem as a leading meteg.”
4. The clause “MAM puts every meteg to the left” should read “MAM has every meteg to the left.”
5. The clause “where the Aleppo Codex puts a meteg” should read “where the Aleppo Codex has a
   meteg.”

The finished Job 4:12 report remains unchanged. The corrections replace only the five possession
verbs and do not change any claim.

## Finding 11.5: narrative romanizations should use `pataḥ` and `ḥataf`

Recorded by ChatGPT-Codex on 2026-09-13. A fresh census of the finished Job 4:12 report found three
`patah` sites and three `hataf` sites. The corrected readings are:

1. In summary item 7, “before a hataf” should read “before a ḥataf.”
2. In section 4's item about the Leningrad Codex at Psalms 72:15, “the note is about the hataf”
   should read “the note is about the ḥataf.”
3. In section 6's paragraph beginning “UXLC 3.9 records a leading meteg in 727 atoms,” the
   sequence “patah 412, qamats 184, segol 59, tsere 37, hiriq 28, sheva 4, hataf patah 2 and
   qubuts 1” should read “pataḥ 412, qamats 184, segol 59, tsere 37, hiriq 28, sheva 4, ḥataf
   pataḥ 2 and qubuts 1”; later in that paragraph, “371 of the 412 on a patah” should read “371
   of the 412 on a pataḥ.”

The finished Job 4:12 report's substantive bytes match historical blob
`b8fc419f43970d94dd96330074da6c3489eeb839`; its only additional line is the authorized update
pointer.

## 2026-09-16: the crop paths moved after the finished report

The crop paths named in the finished Job 4:12 report are historical. Since commit `a8e4790e`, the
live crops and their source notes are under `doc/meteg-after-silluq-snips/`; the finished report's
pre-move wording was restored under the receipt policy.

## 2026-09-21: the manuscript crops moved to the published image directory

The source notes remain in `doc/meteg-after-silluq-snips/README.md`. The live crops are now
`gh-pages/img/aleppo-271r-col2-line5-Job4v12-menhu.png` and
`gh-pages/img/leningrad-398A-Job4v12-menhu.png`, where the generated post-silluq page publishes
them. The unpublished Second Rabbinic Bible crop remains under `doc/meteg-after-silluq-snips/`.
The finished report remains unchanged under the receipt policy.

## 2026-09-22: Cambridge Add. 1753 crop and stroke placement

Ben supplied `Screenshot 2026-09-22 171050.png` as a crop of the verse-final word at Job 4:12
in Cambridge Add. 1753. The screenshot's SHA-256 is
`7FBEA62B6781874F4295041C3BA1DFF32CF3FB8787C6D166D41680CE673445F2`; its byte-identical
published copy is `gh-pages/img/cam1753-0073B-col2-line13-Job4v12-MNHV.png`. The manuscript
locator, page 0073B, column 2, line 13, is recorded in the finished report.

Ben reads both metsil marks in the crop: the silluq under the mem and a meteg after it. Unlike
the Aleppo and Leningrad codices, Cambridge Add. 1753 has its silluq to the left of its segol,
in the normal position rather than the “early” position. The case ledger already classified
Cambridge Add. 1753 as having both strokes; this later observation adds the crop and the
placement contrast without changing that classification. ChatGPT-Codex did not independently inspect
the pointed-Hebrew image.

## 2026-09-25: St. Petersburg Evr. II B 55 has the silluq alone

Ben supplied `Screenshot 2026-09-25 080758.png` as a crop of the verse-final word at Job 4:12 in
the manuscript MAM identifies by the siglum ל-א. The screenshot's SHA-256 is
`CD1F5CFF0296E25F0B8F839EDBF2551A5B6C8D73AD8448EDC391BE3F58D89A09`; its byte-identical
published copy is `gh-pages/img/st-petersburg-evr-ii-b-55-Job4v12-MNHV.png`.

The local `doc/sigil-decoding.md` and cached MAM introduction identify ל-א as St. Petersburg
Evr. II B 55, a manuscript of the Prophets and Writings close to the Aleppo Codex. The NLI
presents B 55 together with its direct continuation, Evr. II B 247; they are separate shelfmarks,
not former and current names. The cached introduction records Job 1:1–9:19 among its surviving
text. ChatGPT-Codex directly inspected the crop and saw the silluq under the mem and no later mark under
the he. St. Petersburg Evr. II B 55 is the only manuscript represented on the published Job 4:12
crop page that has this silluq-only form.

## 2026-09-26: the page images that section 3 read left the checkout

Recorded by a Claude Code session on 2026-09-26, when `doc/PLAN-retire-codex-index-image-work.md`
retired the codex-index image work. The report's section 3 read two page images, and neither is
in the checkout now:

1. `aleppo/aleppo-pages/271r.jpg` was removed with the other Aleppo page scans. The last commit
   that holds it is `1fba91fed6f22cd5aeb4d56d836cf109de48b8ad`, so
   `git show 1fba91fe:aleppo/aleppo-pages/271r.jpg` recovers it.
2. `cam1753/cam1753-pages/0073B.jpg` was an ignored file split from the spread
   `cam1753/cam1753-spreads/cam1753-page-0078.jpg`. That spread was removed with the other
   Cambridge spreads, and `1fba91fe` is also the last commit that holds it. Nothing regenerates
   the split page now.

The readings section 3 records stand, and the line-break and column data it cites are retained.
