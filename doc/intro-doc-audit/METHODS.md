# Methods and evidence for MAM Introduction and doc-note discrepancies

Open [review.html](review.html) for the readable comparisons. This appendix retains
the technical inventory, source versions, coverage limits and supporting evidence.

The presentation is maintained in [human-review.json](human-review.json).
It contains 152 concrete comparisons: 90 discrepancies, 55 interpretation or source
questions, three resolved vowel-function comparisons, and four verse comparisons
for the three tracked issues. These are
presentation entries, not 137 independent manuscript findings. Paired verses and
grouped note wording were separated where the reader needs a distinct decision;
duplicate reference results were merged.

[human-review-coverage.json](human-review-coverage.json) maps all 63/63 retained
finding, question and tracked groups, accounts for all 10/10 additional case records,
and maps all 32/32 verse-reference records and 6/6 section-link records. The verse
records include one exact duplicate. Agreement controls and the nine resolved
unsigned ḥataf comparisons stay in this appendix and their original data.

The renderer validates 666 source passages against literal stored strings,
including the ketiv/qere pairs in the complete chapter 2/appendix comparison and the new source/function examples.
Selected MAM words use explicit target pointers; the four unannotated verse
examples use declared literal pieces with exact parsed-file pointers. These are
displayed as current MAM body text, not as invented doc-notes. Link syntax and formatting
are hidden for readability while captured Hebrew codepoints remain unchanged.
The report addresses an expert reader: it uses ketiv/qere directly and translates
explanatory Hebrew prose while retaining cited Scripture in Hebrew. Scripture-only
panels have no translation; lexical glosses are omitted. MAM body text, MAM ketiv and
MAM qere labels identify the actual selected source rather than treating “reading”
as qere. Each comparison and remaining question precedes its source quotations in
one block. Raw-file and JSON “Source passage” links are omitted from the reader page;
the technical source pointers remain in the research data and this appendix.
Bracketed Hebrew quotations in English translations use one explicit RTL-isolated
node, including their gaps and orphan marks; English labels and sentence punctuation
remain outside it. The quotation strings and source captures retain their codepoints.

Ben’s 2026-10-14 Jeremiah 31:37 adjudication is recorded in
[jeremiah-31-37-adjudication.md](jeremiah-31-37-adjudication.md) and
[adjudications.json](adjudications.json). The readable case keeps the cached quotation
and shows his exact proposed correction separately. Ben also confirmed the
[Numbers 9:7 wording correction](numbers-9-7-adjudication.md) and its inverse,
[Deuteronomy 32:34](deuteronomy-32-34-adjudication.md), retaining the stored
punctuation in both before/after comparisons. Ben subsequently adjudicated
[Deuteronomy 6:21](deuteronomy-6-21-adjudication.md): remove only bare ל from the
opening list, retaining ל1. The original complete note and translation stay visible;
the manuscript assessment is Ben’s and damage/erasure causes remain uncertain.
The renderer checks eleven proposed
quotations against their declared edits, separately from source-passage validation.
The three contextual facts, local screenshot observations and bounded restoration
history are retained with attribution. The copying theory remains a hypothesis;
the screenshot itself is neither included in the repository nor published.

Explanatory translations and questions were reread against their evidence; literal
validation alone does not establish translation accuracy or manuscript truth.
The Deuteronomy 6:21 comparison includes its entire four-clause doc-note and full
English translation, including the correction/interlinear qualifiers, Breuer’s
uncertainty and enlarged-inspection statement, and the final edition list. Hebrew
sigils remain visible with established decoding. The renderer validates the complete
note and its per-clause translation bindings; the faithful raw note was checked
separately, retaining its original mark order.
Dedicated word comparisons and proposed before/after quotations are stacked
vertically, following Ben’s 2026-10-14 Hebrew-prose guidance.

Ben selects **12 words** as the Deuteronomy list’s item count. The report shows
all twelve Introduction/doc-note word pairs and the exact proposed heading.
[deuter-hataf-scope.md](deuter-hataf-scope.md) and
[deuter-hataf-scope.json](deuter-hataf-scope.json) account for 955/955 verses,
365/365 doc-notes, 7/7 ketiv/qere templates and 14/14 candidate notes. All twelve
definite Aleppo/Leningrad vocal-sheva words are listed; Deuteronomy 3:22 remains
one uncertain possible omission. Four edition-text occurrences are concretely
classified outside that scope, and the nine varika words and three plain-sheva
words are recorded. Reproduce this finite check with
`py/main_intro_doc_audit.py deuter-hataf-scope`.

[Lamentations 1:6](lamentations-1-6-proposal.md) now has the exact before/after
sentence and the actual MAM ketiv/qere words. Its source-based proposal preserves
the Introduction’s assignments and corrects only its one/two counts. Ben approved
this correction on 2026-10-15 as a contradiction within the Introduction; the report
now has eleven user-adjudicated comparisons.
[report-prose-revision.json](report-prose-revision.json) records the authored
classifier and transliteration corrections. Existing report-scoped plural and
transliteration lint rules were applied, supplemented by a manual ḥataf/ḥet scan;
source quotations, adaptations, identifiers, paths and official Unicode names
retain their wording. Superfluous “parsed” and “displayed” qualifiers were removed
where they did not establish a distinction; link-label/target distinctions remain.

The 2026-10-14 all-book extension has saved five independently verified list
omissions at Genesis 30:27, Numbers 10:9, 2 Samuel 8:10, Proverbs 30:17 and Song of
Songs 1:6 in [all-books-hataf-findings.json](all-books-hataf-findings.json). The
Proverbs question is now a verified discrepancy; the four other verse cases are
new reader entries. [all-books-hataf-census.json](all-books-hataf-census.json) covers
39/39 books, 23,202/23,202 verses, 3,905/3,905 canonical doc-notes and all ketiv/qere
parameters. Its selected-body count agrees independently with MAM-simple and the
checker’s separate enumeration: 536 literal non-guttural vowel occurrences.
The [all-book findings and evidence](all-books-hataf.md) retain all candidate
dispositions, source/function controls, word-count distinctions and the nine
reading/function/source-object uncertainties. The census alone is not a consistency
verdict. Reproduce enumeration and assessment with `py/main_intro_doc_audit.py
all-books-hataf` and `py/main_intro_doc_audit.py all-books-hataf-review`.
Ben approves the Song of Songs 1:6 and 2 Samuel 8:10 additions for proposal to Avi;
the seven-word Song heading, 31-word Samuel heading, exact insertions and approvals
are in adjudications.json. No proposal
has been submitted or applied. The report’s individual findings state substantive
source/word/vowel evidence; specific validation procedures are retained here.

Regenerate the readable review and its presentation coverage record with
`py/main_intro_doc_audit.py review`, using the interpreter and low-priority workflow
specified below. No semantic census needs to be rerun for a presentation edit.

State: finite reference and productive cached prose passes accounted for; external and editorial evidence boundaries retained.
Isolated research branch, no integration scheduled.

This audit uses the repository snapshot at `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`.
It changes no Scripture input, edition, published page, or manuscript interpretation.
`source-pin.json` preserves exact Git objects and the current full bodies/comments of
MAM-basics #304-307. `topics.json` covers all thirteen Introduction cache pages;
`claims.json` preserves every nonblank source unit with its topic and source pointer.
Source units include table cells and navigation: their count is not a semantic claim count.

The first inventory contains 340 titled spans, 8,984 source units, and 1,643 units
with explicit canonical verse links. Those units produce 3,125 verse-evidence joins;
2,608 joins have documentation notes, and four link targets name nonexistent verses.
The complete chapter walk discovers 3,905 notes. Four further note copies are in
good-ending metadata outside that walk; their locations are recorded in `summary.json`.
These are research census figures, not a consistency verdict.

Run from the isolated worktree root with the home clone's interpreter:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py
```

The script lowers its own process priority, reads the 24 parsed book files
sequentially, and writes only this research directory. It uses the current
`explicit_xataf.extract.find_docnote_tmpls` closed inventory, the current sigil
inventory's visible-note renderer, canonical book and Hebrew numeral maps, and
the existing verse-link builders. Sigil meanings and operators come from
`doc/sigil-decoding.md`; `!=` means surprising equality, and a leading `=` has
MAM as its implicit subject. A bare “in the manuscript” does not supply Aleppo
attribution. Structured note targets without the existing survey's text projection
remain complete nodes with an explicit projection limitation.

Hebrew quotation fields are copied directly from source files. Nothing normalizes
the captures. Literal form search and MAM-order comparison are separate triage
categories; neither proves that the named source supports the matched form.
`form-triage.json` is internal routing data, not an alarm list. Source chronology,
the exact source relation, annotation scope, and any disagreement must be reviewed
before assigning a semantic result. Introduction transclusions remain unexpanded
and are explicitly counted. No live Wikisource request was made.

Open [review.html](review.html) for the compact comparison, with the 20–48 px Hebrew
slider (default 30) and cached verse contexts. Exact source links and pointers remain
in the supporting data. The report keeps the three existing issues separate from
new research. No issues or comments were posted.

The bounded list ledgers account for **1,359/1,359 selected source units**, including
**846/846 selected pointing rows**. Four initial pointing batches reviewed 838 rows:
69 lines containing the Aleppo ketiv sigil, and 200 other pointing/list rows.
Chapter 3 contributes 323 rows and chapter 4 contributes 246 rows.
`ketiv-batch.json`, `nonketiv-batch.json`, `ch3-pointing-batch.json`,
`ch4-pointing-batch.json`, and `claim-dispositions.json` preserve their exhaustive
populations and semantic dispositions; eight Joshua pointing rows are in
`ch5-earlier-batch.json`. Of the initial 269 chapter 5 lines, 237 have
corroborated phenomena or representation differences, four are already tracked,
four contain the newly supported attributed-form disagreements, nine have locator
problems, one has a scope ambiguity, and fourteen have incomplete attribution or
form evidence. These line counts do not imply independent manuscript verification.

New attributed-form disagreements occur at Jeremiah 31:37; Psalm 108:11; and the
paired secondary-reading alternatives at Psalms 57:9 and 108:3; Daniel 2:17's
meteg specimen; Daniel 5:7's ketiv spelling; Psalm 39:13's exchanged meteg/merkha
positions; Psalm 17:14's maqaf candidates; and Isaiah 10:15's missing-yod position.
Psalm 150:3's first ḥataf specimen adds a ninth group: its Introduction quotation
has sheva while the raw/parsed note explicitly attributes ḥataf-pataḥ to Aleppo.
Two subsequent passes add Isaiah 59:19’s nearby-witness maqaf attribution and
Psalm 31:12’s omitted-ḥataf classification. These are eleven groups covering twelve verses.
Ben’s later Jeremiah adjudication selects the doc-note correction; the other groups
retain their recorded source boundaries. `codepoint-proofs.json` independently matches the selected notes
back to the faithful raw chapter cache and records every codepoint. Jeremiah uses
the updated revision 3088451: the restored atom and closed issue #304 are separate
from this accent disagreement. Source chronology is retained rather than erased.

Other reviewed discrepancies include the Deuteronomy ḥataf roster's nine-versus-twelve
word count (eleven verse entries), Lamentations 1:6's reversed one/two
description, and Proverbs 30:19's stale MAM illustration. The first retains all eleven
verse pairs in `deuter-roster-pairs.json`, with the complete later word census linked
above; the latter two explicitly
distinguish structural or edition evidence from a manuscript-reading conflict.
The initial thirty-one independently checked locator examples are grouped as one finding. A grouped
description review covers four letter/accent-name disagreements, including a
Deuteronomy 28:27 note that says TAV where the Introduction correctly says TET.
The raw-cache quotations agree, so this is a prose-label discrepancy, not an
alternative manuscript reading. Daniel 7:9's selected spelling also reverses
between two Introduction lists while the note's Leningrad claim agrees.

The complete spelling/join batches cover **145/145 chapter 3 rows** and **205/205
chapter 4 units**. Their ledgers preserve unsupported provenance details and
incidental pointing separately. Chapter 4's decision-list coverage family has 26
orange cross-references but 17 decision verse entries: nine cross-references have
no counterpart, including three independently checked cases that fit its stated
three-witness inclusion rule.

`ch5-earlier-batch.json` accounts for **79/79 finite entry anchors**, covering 133
source units and 89 verse instances (88 distinct verses). It includes 24 spelling
table rows, three joining rows, 34 size rows, five dotted rows, one reversed-nun
roster, four suspended-letter rows, and eight Joshua pointing rows. All 24 spelling
selections, all seven joining verse selections, and all 34 size choices match the
current structure. Joshua 14:7's starred meteg differs from the current selection
and the note's retained uncertainty. Two notes call selected small letters large;
the raw and parsed special-letter templates confirm the Introduction's size labels.

Three Torah note-prose findings run in the opposite direction from the Introduction
quotation errors: Numbers 9:7 says full VAV for a full-YOD atom, Deuteronomy 32:34
says full YOD for a full-VAV atom, and Deuteronomy 6:21 assigns Leningrad to two
conflicting spelling clauses. `spelling-prose-proofs.json` independently checks
the raw bodies and selected forms. `letter-size-proofs.json` checks the two size
labels against faithful raw templates.

`ch2-secondary-batch.json` reviews **38/38 secondary-accent rows**. Three rows
(two distinct verse cases) have supported source quotation differences; three
have corroborated source relations; four establish only the Aleppo subclaim; one
matches a qualified Leningrad candidate. Twenty-seven primary manuscript claims
have no corresponding local note statement. Note presence at a verse is not enough
when the note describes a different atom.

`catalogue-comparison.json` checks **19/19 finite catalogue lines** against current
typed populations: fifteen memberships match and four differ. The differences
are retained as template/scope drift; a traditional masorah count is not assumed
to count the same objects as the current edition templates.

`topic-coverage.json` routes all **340/340 titled spans** to their evidence boundaries.
It inventories every topic, including general rules, completeness claims, historical
quotations, policy, manuscript locators, and proposals. It does **not** claim that
all corpus-wide rules, historical statements or physical readings have been certified.
All **1,643/1,643 verse-linked source units** now have bounded reviewer assessments.
The added evidence assessments cover **210/210 policy/example units**, and the
24 ḥataf-roster plus five meteg-roster source units. The combined source-unit
ledger originally assessed **1,859 distinct selected source units**. Assessment includes
unsupported and uncheckable claims; it is not a declaration of consistency.

All **667/667 ḥataf roster entries** across five Torah and nineteen later-book
rosters have individual dispositions in `hataf-rosters.json` and its manual
assessment input `roster-review.json`. Of these, 645 have central source/ḥataf
correspondence; 22 retain quotation, label, attribution or incidental-mark limits.
Twelve malformed locators have separately recorded intended-verse bindings.
Counts distinguish forms, alternative specimens, non-guttural ḥataf occurrences
and verse membership: Judges has 23 forms with 24 relevant hatafs, Psalms has
172 listed forms including one erroneous sheva specimen, and Chronicles has
63 forms in 61 verses. Aggregate totals alone hide these differences.

All **98/98 Torah meteg exception entries** were compared with complete note
targets/bodies: 86 main named-source comparisons agree, eleven retain supported
uncertain candidates, and one (Exodus 7:13) has unresolved clause scope.
`meteg-prose-proofs.json` checks four additional note-side inconsistencies against
faithful raw bodies: a PATAH specimen described as meteg, a meteg specimen labelled
no meteg, and two witness lists assigning the same named source both readings.

`policy-assessments.json` preserves bounded support and limits for the 210
units. `torah-final-topic-assessments.json` records **154/154 read-and-routed units**,
including history, Decalogue and Reuben presentation, musical explanations, and
reading divisions. That routing is explicitly narrower than a complete semantic
audit of their embedded claims.

`review-selections.json` keeps 25 compact uncertainty groups, and the batch ledgers
retain less consequential incomplete cases without turning them into an alarm list.

The next source-boundary questions are whether incidental specimen marks assert
complete manuscript pointing, how two-versus-three qere-note descriptions delimit
their scope, and how old template rosters map to current unified special types.
The current cache does not establish the true manuscript reading at the new accent
disagreements. No manuscript scan or new source interpretation was undertaken.

## Incremental cached pass, 2026-10-14

The previous broad audit is commit `46b40fcace6382be94ebdee0fee761a349eedcaa`.
The source remains `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`; no cache was refreshed.
This separate batch revisits **24/24 uncertainty groups** and reads **643/643 additional
prose units**: 179 numeric/universal routing selections, all 460 remaining ordinary
units, and four historical-WLC source-framing units. Root reconciled the
read-only reviewers' disjoint ledgers and independently checked material findings.
The selected assessed ledger now has **2,502/8,984 source units**. All **1,643/1,643
explicit-reference units** remain accounted for. Assessment includes unsupported
claims and framing; neither fraction measures universal semantic consistency.
Of 847 initially routed Westminster units, the four source-framing paragraphs now
receive bounded checks; **843 historical table units** remain routed without individual
semantic assessment. Remaining headings, markup, metadata, tables, transclusions and
historical prose keep the boundaries in the 340-topic map; they have no blanket verdict.

`next-pass-census.json` records current source and consumer commits, exact pointers,
three closed EP projection choices and an independent current MAM-simple extractor.
All choices reproduce **2,679 DEHI / 423 OLEH verses out of 4,465 poetic verses**.
Doubled helpers change mark-instance counts without changing verse membership.
The complete selected atom predicate partitions OLEH into **368 same-atom + 55 two-atom
cases, zero unmatched**. All **55/55** two-atom verse memberships exactly match the
Introduction's three lists; 38 are maqaf-joined and 17 spaced. This resolves current
MAM roster completeness under that predicate. It does not certify a physical manuscript
population. The Introduction's **2,685/421** totals still have no cached source-membership
or counting contract. Neither cached WLC 4.20 nor 4.22 reproduces them; both give the
same compared memberships (2,682 literal DEHI verses, 407 literal OLEH verses). Their
limited scanner recovery is not asserted as a complete grammatical count.

The same closed walk finds **371 qamats-alternative parent templates in 357 verses**
out of 23,202 canonical verses. The Introduction's “about 350” lacks an approximation
tolerance or historical count basis, so this is numerical drift. All **1,010/1,010
ordinary ketiv/qere objects** have unpointed selected ketiv (880 ketiv-first, 130
qere-first). Special types, implicit reading-mother families, colour and live layout
are outside that predicate. Lamentations 1's three explicit cases are independently
accounted for at 1:6, 1:11 and 1:18, including its special first case and post-maqaf third.

`next-pass-assessments.json` retains **21 independent raw-note comparisons**, including
the **nine unsigled ḥataf entries** now matched to explicit Aleppo counterparts.
This overlay raises central source/ḥataf correspondence from 645 to **654/667**;
13 item-level quotation/source-scope limits remain. The original roster ledger is
retained and linked to the incremental proof, without rerunning the completed roster.
It clarifies 2 Kings 14:7's explicit Aleppo pashta clause, Daniel 2:41's expressly
possible digital candidate, Deuteronomy 32:6's literal yod-sheva difference, and four
design specimens that differ from other Introduction passages agreeing with their notes.
Central spelling/size/design agreement remains separate from complete quotation intent.
The maintained legarmeh explanation is corrected: **two** of six existing selected
absences resolve by locator correction; four remain. A repaired nonexistent target
was not a third member of those six. No source or historical commit is rewritten.

The four differing catalogue lines reduce to **two underlying verse cases**, plus the
repeated Jeremiah locator error. The chapter-2 different-qere list has three entries
and the appendix four, adding 2 Samuel 8:3. This is a classification/counting-scope
question. Both passages discuss templates and use Masorah-note denominators; neither
establishes a manuscript-note versus template-use distinction. Chapter 2 describes
a difference especially in the first qere word, with pointing outside or compressed
into ketiv. Samuel retains בנהר and adds פרת, so that criterion could explain its
exclusion. Both passages also list Samuel under qere without ketiv. The note
distinguishes Aleppo from the other named sources, but chapter 2 names no manuscript
for its total. Establish the category, source basis and exclusion rule before
proposing three to four. The separate 2 Samuel 21:12 two-word/three-word qere-note
scope also remains unresolved.

The incremental review presents **four new internal count/wording/date/metadata groups**:
ordinary-Hebrew-year wording against its own
solar-year arithmetic; Isaiah's first-three-types/four-cases grouping; and an incompatible
Hebrew/Gregorian date pair; and a source label saying WLC 4.14 before its own WLC 4.16
quotation. The two quoted legend totals add exactly to 1,034 and 945. The historical
versions are explicitly named, but matching machine-readable legacy inputs and physical
source controls are unavailable. The 4.12/4.14 summary covers all 39 books and retains
category counts whose overlap/filtering does not define unique-change majority.
Local calendar conversion establishes that 7 Tevet 5774
is 2013-12-10, while the text pairs it with 10.12.14. The historical event date remains
unknown. A Job prose reference reverses 9:10 to 10:9, increasing the verse-locator
family to **32 checked examples**. **Six further internal fragment targets** differ
from current cached headings and explicit anchors; live template aliases were not checked.
`next-pass-prose-findings.json` preserves the exact evidence and remaining limits.
These additions make **no new central attributed-form disagreement groups**: the
previous eleven groups and the separately tracked #305–307 remain distinct.

`general-prose-input.json` and `general-prose-assessments.json` preserve all 643 IDs,
human dispositions, exact source captures and narrower claim-to-note/code relations.
Successful census execution is not the evidence for those semantic judgments.
Productive local checks are exhausted for the declared populations. Further resolution
needs an editorial decision about quotation/list scope, an explicit historical counting
population, an unavailable manuscript/source-book report, or live rendering evidence.
Those are concrete evidence boundaries, not execution failures. No such additional
source work or correction is authorized by this audit.

Regenerate this incremental batch sequentially, at the entry point's low priority:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py census-scope
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py next-pass
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py prose-findings
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py general-prose
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py review
```

The prose-finding command adds the checked Job example idempotently to the research
navigation ledger. Every command writes only research data/report files. No new testing
gate, full suite, manuscript scan, external issue/comment, source correction, main
integration or deployment was performed.

Final focused verification matched all 8,984 captured Introduction units and 3,905
retained note nodes to their cached inputs, confirmed the declared populations and
research-only diff, and passed Black on the seven changed Python files and `git diff --check`.
The final compact Hebrew comparison was rendered and inspected at 30 px; the report
retains the 20–48 px slider and no copy/print/save controls. These checks do not turn
the remaining evidence boundaries into consistency findings.

Additional research commands use the same interpreter from the worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py proofs
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py structures
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py catalogues
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py rosters
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py review
```

The supplemental structural census scans 23,202/23,202 verses through the repository's
existing closed EP projection. It counts a template before choosing its documented
child, excludes documentation bodies, and retains every counted node and JSON pointer.
Typed populations alone do not prove the semantic completeness of an Introduction
list. In particular, traditional masorah populations and current template identity
can differ. The survey-only note target field likewise is **not** a complete rendering:
it may omit structural legarmeh or spacing. The complete `target_node` is the evidence.

Focused verification includes regeneration, raw/parsed codepoint checks, exhaustive
batch-ledger coverage, and a headless local visual inspection. All research writes
stay under `doc/intro-doc-audit/` and its code under `py/intro_doc_audit/` plus the one
entrypoint. No production generator or testing gate was added; mega/full-suite work
was not run, preserving nightly priority.


The final finite passes
-----------------------

`scoped-assessments.json` adds **273/273 bounded source-unit assessments**,
including the remaining 118 Torah units, 59 Chapter 2 units, remaining Chapter 5
example paragraphs, appendix/index metadata and poetic-roster source units.
The distinct combined ledger is 1,859 units; overlapping assessments of the
Deuteronomy ḥataf roster are retained under `additional_assessments`, counted once.
All 8,984 original source units remain available, including layout, table cells,
navigation and non-reference prose. A source unit is not an independent claim.
Topic routing explicitly preserves limits on the broader remaining prose; the
finished finite passes do not establish universal semantic consistency.

`poetic-rosters.json` and its manual input `poetic-roster-review.json` account for
**385/385 items in 14 source units**:125 explicit design examples and 260 implicit
revia examples. All have the reviewed selected-edition feature;286 have central
named-source correspondence, one has a qualification/representation concern,
and 98 have only current-feature evidence because a pertinent source statement is
absent. The55 two-word oleh examples have32 gray maqafs, six ordinary maqafs and
17 spaces after independently accented words. Every one of the 260 selected revia
examples has GERESH MUQDAM U+059D and REVIA U+0597 in one Unicode letter cluster,
through the current closed EP projection. This is a representation check, not a
claim about physical manuscript positions.

The compact report has **11 attributed-form disagreement groups**, **24 other
reviewed groups**, the 31-example locator family, and the three already tracked
issues. The later other groups include opposite-direction note prose errors,
2Samuel 21:12’s two-versus-three qere-note scope, Numbers 22:5’s Sapir-versus-Cassuto
attribution, Genesis 2:10’s older-transcription chronology, an internal small/large
label, and an Amos–Micah three-versus-four missing-page count. The latter remains
historical metadata conflict; neither page count is declared physically correct.

`semantic-controls.json` preserves seven additional independently matched raw
note bodies; `source-boundary-proofs.json` preserves four attribution/chronology,
locator and size controls. Source quotes, uncertainty markers and current decoder
meanings are retained. `poetic-description-proofs.json` checks Psalm 30:12’s omitted
OLEH, which the note calls REVIA. Psalm 53:6’s note also names a resh absent from
its described atom. These checks substantiate the reviewed cached statements;
successful regeneration alone is not a semantic consistency verdict.

The closed corpus census reproduces 4,465 poetic verses, but 2,679 DEHI verses versus
the Introduction’s2,685, and 423 OLEH verses versus 421. Count definitions and source
chronology remain unresolved. The55 semantic two-word cases were reviewed as a
finite list but not rederived as a full-corpus semantic partition. Physical readings,
source-book claims, pronunciation theory, original typography, unreported correction
history and universal list completeness cannot all be settled from these caches.
The24 uncertainty groups and per-item ledgers make those limitations explicit.

Regenerate the poetic item evidence with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py poetic-rosters
```

Every research subcommand now lowers its process priority. The final batch used
small sequential reads and research-only checks; no nightly or production gate
was added. No external issue/comment, merge, deployment or manuscript interpretation
change was made.

The reader typography follows the shared document.css default-serif and
`color-scheme: light dark` / `light-dark()` pattern. The Hebrew font and captured
strings remain unchanged. Local Times New Roman regular and bold both contain
U+1E25; bounded light/dark Edge previews show consistent ḥ rendering, readable
30px Hebrew, and vertically stacked forms. The slider retains20–48px/default30.
Ben requested removal of the three open defaults on 2026-10-14
(`Sentinel_5729358219cc819184bea60bbddef656`). All case sections now start
collapsed. The report has no open/closed persistence code; only the font slider
is scripted. The earlier local Edge reload check returned the old defaults;
that historical observation does not describe the new all-collapsed initial state.

On 2026-10-15, Ben approved the Numbers 10:9 and Genesis 30:27 additions for proposal to
Avi; the exact entries, count changes (18→19 and 33→34), source forms and insertion
neighbors are retained in adjudications.json. The authored entries are built from
retained source-form lookups and checked for MAM mark order, following owner-main
guidance at `7cd619ad101dc40e5636342f4af7336ee204415f`; historical source captures
remain unchanged. Ben’s Numbers 10:9 phonetic question is separately attributed and
unresolved in both the case and the all-book ledger. It is not one of the nine
pre-existing manuscript/function/source-object uncertainties.

The reader puts 140 unevaluated cases first and the twelve cases with recorded substantive
Ben decisions in a collapsed **Reviewed** section at the bottom. Membership is derived
from linked adjudication authority and status; an independently verified proposal or a
wording comment does not qualify. Ben’s 2026-10-15 Lamentations 1:6 approval
(`Sentinel_d0a73e635cc48191afb8ad0bf4fa6a4f`, 15:03 UTC) moves that case into Reviewed.
It resolves a contradiction within the Introduction; no doc-note exists at that verse.
Numbers 10:9 belongs in Reviewed while retaining its unresolved phonetic question. All
152 cases and the Reviewed wrapper start collapsed; stable anchors, source quotations
and prior decisions are retained. No persistence or tracking system was added.

The 2026-10-15 Proverbs 30:19 wording review names the Introduction’s layout example
and MAM body text directly, and removes the redundant discrepancy sentence. Initial
context review left intentional use of the printed-edition form unresolved, so the case
was placed under Questions. The section link is derived from the unique cached
heading at chapter 2 line 915; its live rendered anchor was not checked. Source and
wording details are retained in report-prose-revision.json. Other MAM body-text labels
identify their selected source form, including the deḥi and qamats-qatan forms.

The subsequent [Proverbs 30:19 history check](proverbs-30-19-history.md) locates
the actual 2013-05-27 example insertion and the 2020-11-08 chapter change from
space to maqaf. All 41 visible chapter revisions and 22 linked-draft revisions
were read; the larger Introduction histories have complete metadata and selected
content evidence. This establishes an older MAM form retained by the example.
Ben approved the exact space-to-maqaf proposal on 2026-10-15 at 16:11 UTC
(`Sentinel_a0613408f38c8191804afc8c85a5733c`), moving the settled case into Reviewed.
The other approvals and historical evidence are preserved. The supplemental
live-history evidence is separate from the original cached audit inputs.

The supplemental history inventory accounts for all 152 reader cases: 94 applicable
comparisons and 58 excluded internal contradictions or controls. Ben explicitly included
the omitted-oleh count despite its internal Introduction comparison. Pending entries
are unanswered chronology questions, not findings of staleness. Regenerate the routing
with `py/main_intro_doc_audit.py history-inventory`; completed evidence is indexed in
`revision-history-results.json`. History requests are sequential, ten seconds apart,
and stop on rate limiting while retaining completed captures.

The [omitted-oleh evidence](oleh-count-evidence.json), regenerated by
`py/main_intro_doc_audit.py oleh-count`, distinguishes thirteen listed verses and MAM
body forms from twelve pertinent notes: eleven explicitly name omitted oleh, while
Psalm 30:12 names revia. Psalm 42:3 has no doc-note. Six of the eighteen candidate notes
concern other features. Psalm 30:12's exact form difference is U+05AB OLE; U+0597 REVIA
occurs in neither form. Its terminology correction is filed as #309, and the absent
Psalm 42:3 note as #310. Ben approved the chapter 2 count reconciliation on
2026-10-15 at 16:48 UTC; the proposed source correction remains unapplied.
No manuscript scan interpretation is asserted.

The [count history](oleh-count-history.json) retains five selected snapshots and their
[literal source excerpts](oleh-count-history-sources.json). The exact
[2021-09-26 count edit](https://he.wikisource.org/w/index.php?diff=1194335&oldid=1194333)
changes eleven to thirteen without changing the thirteen entries. Chapter 2 still says
eleven in revisions 1194327 (05:14:43 UTC) and 1220669 (20:12:28 UTC), surrounding that
05:32:43 UTC correction. This dates the requested sequence, not the list's first
creation or earliest incorrect total.

The missing parenthesis in the Isaiah type-2 category was introduced by excerpting
chapter 5 line 48 inside a balanced parenthetical. Its Hebrew and English now include
the complete category; the similarly truncated summary paragraph is also complete.
The source cache and the case's disposition are unchanged.

The first four-case [history batch](history-batch1-results.json) reads all 136
visible canonical chapter contents for Numbers 9, Deuteronomy 32, Psalms 1 and 18.
The [retained evidence](history-batch1-sources.json) includes selected literal
verse excerpts, Introduction insertions and their adaptive-search traces. The
optional `py/main_intro_doc_audit.py history-batch1` command rebuilds these records
from the local read-only API cache without network calls; its selected revision IDs
are retained in the evidence file. It is not part of a production or testing gate.

Numbers 9:7's incorrect vav label entered revision 2826807 on 2023-12-24;
Deuteronomy 32:34's incorrect yod label entered revision 2835959 on 2024-01-28.
Both selected spellings are unchanged immediately across those edits. Psalm 1:3's
layout example entered revision 486875 on 2013-05-30, matching linked MAM draft
486873 from nine minutes earlier; the canonical chapter added the grey maqaf in
revision 998046 on 2020-11-10. Psalm 18:2's explicit Aleppo attribution entered the
Introduction on 2023-03-09, before the explanatory chapter note on 2023-03-10 and
the consulted-manuscript list in 2025. That history leaves the attribution in the
missing Aleppo section unresolved. All existing approvals and source quotations
remain unchanged. The current history inventory records completed and pending
cases separately rather than classifying unexamined history.

The [second history batch](history-batch2-results.json) records four cases from
61 complete chapter histories, with Jeremiah 31 reused for two different questions.
Deuteronomy 6:21's bare-Leningrad source-list conflict is introduced by the 2023
list expansion, while the current Song of Songs list omits 1:6 when created in
March 2023. Jeremiah 31:37's wrong quotation mark is already in the first canonical
MAM note of 2015; the 2026 restoration does not change it. The exact earlier draft
origin remains unestablished. A February 2023 spacing edit is explicitly rejected
as the substantive example's origin.

The separate Jeremiah 31:27 source-specificity question remains unresolved:
the stable Introduction names Masorah Parva while the historical notes name
the Aleppo Masorah generally. The broader attribution is compatible with the
narrower one; it does not establish a contradiction. The particular marginal
note or scholarly attribution remains a concrete support gap. Literal source
evidence is in [history-batch2-sources.json](history-batch2-sources.json); the
optional `history-batch2` command rebuilds from the local API cache without
network access. All twelve Ben approvals and the original source excerpts remain
unchanged.

The [third history batch](history-batch3-results.json) accounts for fifteen more
cases, using all 317 visible chapter revisions across ten distinct chapters
(including previously captured chapters). Twenty-five of 94 applicable histories
were recorded at this checkpoint; 69 remained pending. The [literal evidence](history-batch3-sources.json)
retains complete chapter metadata, grouped exact note states and selected
before/after verse and Introduction excerpts. The optional `history-batch3`
command rebuilds this research evidence from the separate local API cache.

Deuteronomy 32:6 became stale after the January 2024 note correction. Psalm 17:14
and 18:7's candidate-attribution tensions coexist with their March 2023
Introduction additions. The Samuel, Genesis and Numbers omissions predate later
canonical note changes; Genesis and Numbers were already absent when numeric
list counts were assigned, while the Torah section still carried its work marker.
Numbers 10:8's conflicting source code enters in December 2023. The March 2024
2 Samuel 21:12 update adds the three-word appendix entry but retains the older
two-word catalogue. The two Samuel 24 ketiv vowels remain function questions,
and Psalm 17's later narrowed caption retains the earlier Sassoon entry.
These bounded histories do not independently settle manuscripts or list scope.

Ben separately requested a concrete Psalm 42:3 note in a comment to #310
(`Sentinel_8c127574c44881918a6c47e6c61684e3`). The exact note, analogous examples,
posted comment and subsequent explicit-parameter syntax correction are retained
in [the comment receipt](issue310-concrete-note-comment.json). Both comments were
read back character for character; the original issue body was unchanged. No
Wikisource source edit was made.

The [fourth history batch](history-batch4-results.json) accounts for all eight
Daniel cases from 85/85 canonical chapter revisions. The November 2023 Daniel 2:17
meteg correction and April 2023 Daniel 7:9 selection change establish two stale
Introduction details. Six other cases retain explicit uncertainty about first
insertion, manuscript interpretation, source qualification, illustration scope,
or an uncertain vowel. The [literal evidence](history-batch4-sources.json) keeps
the source distinctions and before/after snapshots. Thirty-three of 94 applicable
histories are recorded; 61 remain pending. Rebuild this batch with
`py/main_intro_doc_audit.py history-batch history-batch4`.
