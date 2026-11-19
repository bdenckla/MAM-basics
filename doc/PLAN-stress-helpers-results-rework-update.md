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

## 2026-11-18: Kor, Sim and KorSim, "p. A38", bare letters, and "the printed tradition"

Recorded by Claude (Opus 5.5), in the commit that makes the edits. Ben typed this list in the
commander session on 2026-11-18, at 14:15 New York time:

> start (or, more likely, queue) a session that will do these edits to the Kor-Sim-MAM document (I say more likely queue because another session is currently editing the Kor-Sim-MAM stress helper document):
>
> In text like this:
>
> > Koren has munaḥ on יִהְיֶה and a space where MAM has maqaf. The telisha qetanna on לְךָ agrees, and neither has a helper.
> >
> > MAM’s note reports MAM’s compound in the printed editions too, with a meteg on the second yod of יִהְיֶה
>
> remove all pointing if it is not needed by the reader to understand the matter at hand.\
> ====
> Change "appendix p. 38" and the like to "p. A38" with a hover-explanation of what "A38" means
> ====
> In individual rows, change "Koren / SimTan" to "KorSim", hover explained to mean "both Koren and Simanim".
> ====
> Change things like
> > Koren p. 10
> > SimTan p. 366
> to
> > Kor p. 10
> > Sim p. 366
> ====
> Change
> SH in both printed editions only
> to
> SH in KorSim only
> with "KorSim" hover-explained
> ====
> Change "Both editions have ..."
> to "Kor and Sim have ..." when that's what you mean
> ====
> When translating MAM doc-notes, in this document and elsewhere
> (so make a note in whatever skill and/or other documents help with MAM doc-note translation)
> for דפסים or whatever the word is you sometimes translate as "printed editions",
> please instead use "the printed tradition"
> (this means, typically, the 2nd Venice MG and its descendents, which is pretty much
> all printed traditions before some 20th century editions such as BHS started being manuscript-based.
> Note that there were plenty of 20th century editions, even late into the 20th century,
> that resisted this trend towards being manuscript-based, and are still in the 2nd Venice MG tradition,
> i.e. the "printed tradition") (admittedly a slightly confusing term now).
> Another way of putting this is that by "the printed tradition" we mean "editions in the lineage of traditional printed editions")
> perhaps consult our git-tracked mirror of the mam introduction and see if it is discussed there. And/or maybe in Yeivin ITM.

A session that researched the list, writing nothing, put six decisions to him on its decision page.
He answered on 2026-11-18, at 15:06 New York time:

> Follow your recommendations for all 6 decisions. As the commander for a fresh session to do it, I'd advise.
>
> In "the accepted text of the widespread editions in the lineage of the second Venice Mikraot Gedolot, chosen from the 19th and early 20th centuries.",
>
> I don't like "accepted" and "chosen".
>
> I don't like "accepted" because it makes it sound like it is authoritative. Can we just drop "accepted" rather than figure out what you meant by it? Or was this your translation of a Hebrew word from MAM's introduction, and thus we should try harder to translate it without implying authority (or without implying too much authority).
>
> I don't know what "chosen" is trying to express, so can we drop it? Again, let's not drop it (and let's try to find something better) if this reflects an attempt to translate a Hebrew word.
>
> Oh, and I prefer Miqraot to Mikraot, as in general I prefer to transliterate qof with a q. Unless you have specific reason to use 'k' here.

- **1A, bare letters.** The eight notes that named a word in pointed Hebrew name it in bare letters,
  which keep the surrounding font: in each, the Hebrew only says which word the note is about.
- **2A, Kor, Sim and KorSim.** A row names its editions KorSim, Kor or Sim beside the printed word
  and in its difference's label, as in "SH in KorSim only", "SH in Kor only" and "no SH in Sim", and
  a row of both editions names each on its page labels, as in "Kor p. 10" and "Sim p. 366", and on
  its crops. Notes that said "Both editions have" or "Both printed editions have" say "Kor and Sim
  have", Ben's sixth item. Each abbreviation has a hover, his words: Kor "Koren", Sim "Simanim" and
  KorSim "both Koren and Simanim". The Filter menu's hover gives all three.
- **3A, "p. A38".** Koren's appendix pages are "p. A38" and "p. A39", whose hovers read "Koren’s
  appendix, page 38, numbered apart from its main text", and likewise for page 39.
- **4A, a hover on each "the printed tradition".** The seven notes that render MAM's דפוסים say "the
  printed tradition", or "part of the printed tradition" at Exod 20:9, and at Lev 23:17, where MAM's
  note has בדפוסים וקורן, "the printed tradition and Koren". Ben's answer questioned two words of
  the hover's draft. Both translated MAM's introduction, so both were retranslated rather than
  dropped: "accepted", for המקובל in הנוסח המקובל בדפוסים (`in/mam-ws-intro/ch3.mediawiki`, lines
  728 and 730), became "customary", and "chosen", for נבחרות in מהדורות מקרא נבחרות
  (`appendices.mediawiki`, line 272), became "a selection of". His later wording of the hover is
  below.
- **5A.** The renderings of MAM's דפוסים outside this page are left to a separate sweep. Until it
  lands, the hebrew-prose skill's new section lists them as not yet changed.
- **6A.** The hebrew-prose skill's `references/core-rules.md` gives the rule behind 1A. Its
  `references/terminology.md` records Ben's instruction behind 4A, with his words, in the section
  “MAM's דפוסים is "the printed tradition"”, and `doc/sigil-decoding.md` decodes the sigil the same
  way.
- **Miqraot.** Ben's preference for qof as q, as in "Miqraot", is in the skill's
  `references/terminology.md`, "Transliteration (accgram)".

Three notes also lost a verb that the skill's "Just say has" bans: "prints" at Isa 47:1 and 47:5,
and "bearing" at Ruth 2:9. The crops' credit names Koren and the Simanim Tanakh.

Ben then wrote, in the session that made these edits, of the hover's text:

> Will you be responsible for implementing the following hover-text for דפוסים ("the printed tradition")?
>
> If so, I like the new text:
>
> In MAM’s notes, the customary text of a selection of widespread editions from the 19th and early 20th centuries, in the lineage of the second Venice Miqraot Gedolot. The notes cite that Venice edition, and Koren, apart.
>
> but I would like it to reiterate what it is talking about, i.e. if it is hover-explaining "the printed tradition", I'd like it to say something like
>
> In MAM’s notes, דפוסים, which we usually translate as "the printed tradition" means the customary text of a selection of widespread editions from the 19th and early 20th centuries, in the lineage of the second Venice Miqraot Gedolot. The notes cite that Venice edition, and Koren, apart.

The hover follows his wording, with curly quotation marks and a comma closing its clause:

> In MAM’s notes, דפוסים, which we usually translate as “the printed tradition”, means the customary text of a selection of widespread editions from the 19th and early 20th centuries, in the lineage of the second Venice Miqraot Gedolot. The notes cite that Venice edition, and Koren, apart.

## 2026-11-19: the rows that MAM's Wikisource refresh resolved, removed

Recorded by Claude (Opus 5.5), in the commit that removes them. MAM-basics' Wikisource refresh of
2026-11-19, `9e364a70`, took Avi Kadish's edits that give MAM the printed editions' stress helper
at 14 verses where this page had a row, and `ed5c5633` regenerated MAM's products from it. Ben
chose on 2026-11-19:

> I choose 1B: git history shows what was found. I choose that the document only show what currently exists, after Avi's fixes.

Of the crop at Deut 33:21 he wrote:

> The file koren-deuter-33-21-A5-D-326-note-1.png shows tsere under yod and segol under tav.

- **The 14 verses' rows are gone.** `koren.json` lost 14 of its 88 records and
  `simanim-tanakh.json` 14 of its 37, 28 records in all, after a check by script that MAM's text
  in `MAM-parsed/plus/` now has, at each of the 14 verses, the printed word's stress helper where
  the printed word has it. Thirteen were batch 2's rows with a helper in both printed editions
  only, at Josh 7:7, 1Sam 17:37, 17:39 and 26:15, 2Sam 19:31, 2Kgs 9:36, Isa 10:16 and 39:2,
  Jer 21:10 and 40:15, Ezek 13:19 and 14:16, and Amos 6:10. The fourteenth, batch 1's row at
  2Chr 20:27, had MAM's telisha gedolah helper on bet, where both editions have it on shin. MAM
  now has it on shin, the correction that #371 documents, and the page no longer links that issue.
  At 2Sam 19:31 both editions still have a meteg on alef that MAM lacks, a difference that none of
  the page's categories covers. The 28 crops of the removed records, which nothing else in the
  repository referenced, are deleted. The table has 79 rows, 36 of batch 1 and 43 of batch 2,
  where it had 93, 37 and 56, and the Filter menu no longer offers "SH in KorSim only" or
  "Different SH placement — KorSim", which had no other rows.
- **Deut 33:21.** The row's Koren word had a segol under yod and a tsere under tav, as MAM's
  earlier note gave Koren's word. A script swapped those two vowels, keeping every other mark, so
  that the word is now וַיֵּ֙תֶא֙, where it was וַיֶּ֙תֵא֙. The new word is, code point for code point, the
  word that MAM's rewritten note gives Koren. The row's sentence, which reported the earlier note's
  Koren clause and added that the scan shows a dagesh in yod, now reads: "MAM’s note reports final
  stress in MAM. For Koren, as for Heidenheim’s edition, which follows Ein HaQore, the note
  reports a tsere under yod with the pashta’s stress helper and a segol under tav, as the crop
  shows." The row keeps its category, "SH in Kor only": Koren has the pashta's stress helper on
  yod, where MAM has a single pashta.
- **Judg 18:19 and Ezek 19:9.** MAM's notes there now name Koren, and each of the two Koren rows
  gains a sentence on its note, with a "MAM doc-note" link. At Judg 18:19 the sentence is "MAM’s
  note gives final stress for the printed tradition and Koren." At Ezek 19:9 the sentence is
  "MAM’s note gives final stress for the Leningrad Codex and other manuscripts, and for the
  printed tradition and Koren.", and its link goes to MAM-with-doc's Ezekiel big-doc page, which
  holds that note.
