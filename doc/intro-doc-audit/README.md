# Cached Introduction and documentation-note audit

State: live research; isolated branch, no integration scheduled

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
slider (default 30), exact source links, and cached verse contexts. The report keeps
the three existing issues separate from new research. No issues or comments were posted.

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
Psalm 150:3's first hataf specimen adds a ninth group: its Introduction quotation
has sheva while the raw/parsed note explicitly attributes hataf-patah to Aleppo.
These are nine groups covering ten verses. Neither source is
declared correct. `codepoint-proofs.json` independently matches the selected notes
back to the faithful raw chapter cache and records every codepoint. Jeremiah uses
the updated revision 3088451: the restored atom and closed issue #304 are separate
from this accent disagreement. Source chronology is retained rather than erased.

Other reviewed discrepancies include the Deuteronomy hataf roster's nine-versus-eleven
count (eleven verse entries, twelve atom forms), Lamentations 1:6's reversed one/two
description, and Proverbs 30:19's stale MAM illustration. The first has all eleven
Introduction/doc-note pairs in `deuter-roster-pairs.json`; the latter two explicitly
distinguish structural or edition evidence from a manuscript-reading conflict.
Ten independently checked locator examples are grouped as one finding. A grouped
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
all 1,643 verse-linked units or all corpus-wide rules have been semantically audited.
The added evidence assessments cover **80/80 policy/example units**, and the
24 hataf-roster plus five meteg-roster source units. The combined source-unit
ledger therefore assesses **1,468/1,468 selected units**. Assessment includes
unsupported and uncheckable claims; it is not a declaration of consistency.

All **667/667 hataf roster entries** across five Torah and nineteen later-book
rosters have individual dispositions in `hataf-rosters.json` and its manual
assessment input `roster-review.json`. Of these, 645 have central source/hataf
correspondence; 22 retain quotation, label, attribution or incidental-mark limits.
Twelve malformed locators have separately recorded intended-verse bindings.
Counts distinguish forms, alternative specimens, non-guttural hataf occurrences
and verse membership: Judges has 23 forms with 24 relevant hatafs, Psalms has
172 listed forms including one erroneous sheva specimen, and Chronicles has
63 forms in 61 verses. Aggregate totals alone hide these differences.

All **98/98 Torah meteg exception entries** were compared with complete note
targets/bodies: 86 main named-source comparisons agree, eleven retain supported
uncertain candidates, and one (Exodus 7:13) has unresolved clause scope.
`meteg-prose-proofs.json` checks four additional note-side inconsistencies against
faithful raw bodies: a PATAH specimen described as meteg, a meteg specimen labelled
no meteg, and two witness lists assigning the same named source both readings.

`policy-assessments.json` preserves bounded support and limits for the eighty
units. `torah-final-topic-assessments.json` records **154/154 read-and-routed units**,
including history, Decalogue and Reuben presentation, musical explanations, and
reading divisions. That routing is explicitly narrower than a complete semantic
audit of their embedded claims.

`review-selections.json` keeps twenty compact uncertainty groups, and the batch ledgers
retain less consequential incomplete cases without turning them into an alarm list.

The next source-boundary questions are whether incidental specimen marks assert
complete manuscript pointing, how two-versus-three qere-note descriptions delimit
their scope, and how old template rosters map to current unified special types.
The current cache does not establish the true manuscript reading at the new accent
disagreements. No manuscript scan or new source interpretation was undertaken.

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
