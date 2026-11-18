# Updates to the stress-helpers results rework plan

State: open, first entry 2026-11-18.

## 2026-11-18: the pages pared down, then given crops and each edition's word

Recorded by Claude (Opus 5.5). This entry and the next record what became of the base plan's
results.html after its "Execution, 2026-11-17".

**Effective base State:** executed 2026-11-17; results.html has since been merged into
index.html, as the next entry says.

Three commits of 2026-11-18, made on Ben's other computer, changed what the execution left.
MAM-private's `stress-helpers/results-page-process-2026-11-18.md` records what they took off
both pages, and why.

- `b963105d` carried out Ben's task 1 of 2026-11-17 and the eleven updates he queued that day.
  results.html lost the spelling-only table that Decision 4 (4A) had put below its differences
  table, its census tables, its definitions and its paragraphs of facts, and Koren's finding at
  1Sam 24:3, which the finding's crop showed to be spurious. index.html lost its paragraphs on
  the Decalogue comparisons and on thirteen chanted words, and its notes at 2Sam 4:6 and
  2Sam 13:20.
- `b74a9815` gave each of results.html's 74 findings its edition's word, page, scan and crop, as
  index.html's rows have them, at Ben's request of 2026-11-17. That overtook Decision 3 (R6),
  whose 3A had left results.html with MAM's word and the sentences only, and its "Crops wait for
  the merge into index.html".
- `267f4eff` corrected `doc/simanim-tanakh-signs.md`'s sentence on the Simanim Tanakh's rafe,
  from two of those crops.

## 2026-11-18: results.html merged into index.html

Recorded by Claude (Opus 5.5), in the commit that carries out the merge. A decision page put three
questions to Ben: Decision 1, whether to merge results.html into index.html now; Decision 2, which
label Ezek 16:61 takes in a merged table; and Decision 3, whether to check the dagesh ḥazaq
sentence of `doc/simanim-tanakh-signs.md`. Ben answered on 2026-11-18:

> 1A, 2A, 3A.
>
> 3A should be done in a totally separate session granted by the commander, in my opinion.
>
> 1A (the merge) should add another filter control, with options batch 1, batch 2, all batches.
> where batch 1 is pre-merge index.html and batch 2 is pre-merge results.html. Default all
> batches.

- **1A, with the batch filter.** results.json's 74 findings joined `koren.json` and
  `simanim-tanakh.json` with `"batch": 2`, after the 51 earlier records, which have
  `"batch": 1`. results.html and results.json are gone, and index.html has one table of 93 rows,
  37 of batch 1 and 56 of batch 2. Its opening sentence is "The table lists differences from MAM
  in prose verses.", and its link to results.html is gone. A second filter, "Batch", offers "All
  batches", the default, "Batch 1" and "Batch 2". The generator raises if a batch-2 record
  repeats a batch-1 record of its edition, which keeps R2's guarantee.
- **2A.** Ezek 16:61 is labeled as a redundant helper in both printed editions, like the thirteen
  rows of the same shape with pashta. Stage 1 had left that label "a question for the merge".
- **3A** went to a separate session, as Ben asked.

The requirements ledger's R3, "prepare for merging results.html into index.html in substance",
whose status said "the merge itself is later work", is now implemented: merged on 2026-11-18.

## 2026-11-18: MAM's notes at the batch-2 findings

Recorded by Claude (Opus 5.5), in the commit that adds the notes. Ben asked on 2026-11-18:

> For this "further" work, were MAM's notes consulted to see if the simanim and/or koren
> differences are noted? I think that was done for the original (batch-1) work and should be
> done for the "further" work if it was not already done.

They had not been. No batch-2 record cited or mentioned a MAM documentation note, and the census
rows behind them have no field for one, where 11 batch-1 records cite one. A read of MAM's notes
at every batch-2 finding's verse, in MAM-basics' own copy of MAM's text, found a note on the
finding's chanted word at 7 of the 74 findings: 6 of Koren's 54 and 1 of the Simanim Tanakh's 20,
in 6 notes, since one note at 2Chr 29:31 serves both editions. Of the other 67, 60 are at verses
with no documentation note, and 7 at verses whose notes concern other words. Each of the 7 now
has a sentence saying what the note reports, with a "MAM doc-note" link, as batch 1's rows have:

- At Exod 27:16, Ezek 20:31 and 2Chr 29:31 the note gives the printed editions the edition's
  word. At 2Chr 29:31 it also names BHS, Mechon Mamre and Simanim, taken as the Simanim Tanakh,
  since Chronicles has no tiqqun.
- At Exod 20:9, עליון, the note names Koren, after Heidenheim, among the printings with munaḥ
  alone on the compound's first word, as Koren's appendix has it.
- At Exod 20:2 and Deut 5:6, עליון, the note reports MAM's compound, with its maqaf, in the
  printed editions, where Koren's appendix has a space. As at Esth 6:1 in batch 1, the row gives
  what the note reports beside what the edition has.

Three of the links go to MAM-with-doc's big-doc pages, which hold those notes' text. The read's
results, one entry per finding with each bearing note's doc-parts, are in MAM-private's
`stress-helpers/mam-notes-batch2-2026-11-18.json`.

## 2026-11-18: the batches explained, and the menus' counts in step

Recorded by Claude (Opus 5.5), in the commit that carries out the two decisions. Ben typed in the
commander session on 2026-11-18, "start a session to continue work on
MAM-basics/gh-pages/stress-helpers/index.html", and the session it started put two questions to
him on its decision page: Decision 1, whether the page should say what Batch 1 and Batch 2 are,
since after the merge nothing on it did; and Decision 2, whether the Filter menu's counts should
follow the Batch choice, since they counted both batches while 4 of the menu's 13 choices have no
batch-1 rows and 7 have no batch-2 rows. Ben answered on 2026-11-18:

> 1A, 2A

- **1A.** The opening paragraph gains a sentence after its first: "Batch 1 is the original set of
  comparisons, and batch 2 adds the differences found beyond it." It reuses Ben's phrase of
  2026-11-17, "the original set of comparisons", and `in/stress-helpers/common.json` holds it.
- **2A.** Each menu's counts follow the other menu's choice, and a choice that would leave no rows
  is greyed out but keeps its place. With Batch 2 chosen, for instance, the Filter offers "All
  differences (56)" and a greyed "No SH in Kor (0)", whose 8 rows are all in batch 1. The search
  box still affects only the table and its count of visible differences. `controls.js` recounts
  from each row's `data-filter` and `data-batch`, and the generator gives each menu choice its
  label, without the count, in `data-label`.
