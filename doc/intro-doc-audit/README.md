# Cached Introduction and documentation-note audit

State: live research; isolated branch, no integration scheduled

This audit uses the repository snapshot at `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`.
It changes no Scripture input, edition, published page, or manuscript interpretation.
`source-pin.json` preserves exact Git objects and the current full bodies/comments of
MAM-basics #305–307. `topics.json` covers all thirteen Introduction cache pages;
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

Two complete bounded chapter 5 batches reviewed **269/269 selected source lines**:
69 lines containing the Aleppo ketiv sigil, and 200 other pointing/list rows.
`ketiv-batch.json`, `nonketiv-batch.json`, and `claim-dispositions.json` preserve
their exhaustive populations and semantic dispositions. Of these lines, 237 have
corroborated phenomena or representation differences, four are already tracked,
four contain the newly supported attributed-form disagreements, nine have locator
problems, one has a scope ambiguity, and fourteen have incomplete attribution or
form evidence. These line counts do not imply independent manuscript verification.

New attributed-form disagreements occur at Jeremiah 31:37; Psalm 108:11; and the
paired secondary-reading alternatives at Psalms 57:9 and 108:3. Neither source is
declared correct. `codepoint-proofs.json` independently matches the selected notes
back to the faithful raw chapter cache and records every codepoint. Jeremiah uses
the updated revision 3088451: the restored atom and closed issue #304 are separate
from this accent disagreement. Source chronology is retained rather than erased.

Other reviewed discrepancies include the Deuteronomy hataf roster's nine-versus-eleven
count (eleven verse entries, twelve atom forms), Lamentations 1:6's reversed one/two
description, and Proverbs 30:19's stale MAM illustration. The first has all eleven
Introduction/doc-note pairs in `deuter-roster-pairs.json`; the latter two explicitly
distinguish structural or edition evidence from a manuscript-reading conflict.
Eight independently checked locator examples are grouped as one finding.

`topic-coverage.json` routes all **340/340 titled spans** to their evidence boundaries.
It inventories every topic, including general rules, completeness claims, historical
quotations, policy, manuscript locators, and proposals. It does **not** claim that
all 1,643 verse-linked units or all corpus-wide rules have been semantically audited.
`review-selections.json` keeps nine compact uncertainty groups, and the batch ledgers
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
