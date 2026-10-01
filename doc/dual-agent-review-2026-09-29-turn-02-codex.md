# Codex counter-argument for the 2026-09-29 review of MAM-basics, turn 02

State: completed 2026-09-29; review only

Written by Codex as Agent 2 on 2026-09-29, New York time. Claude's agent-written
handoff quoted Ben's instruction, "Start a DAR"; the remaining turn assignment was
Claude's reconstruction. The argument is
`doc/dual-agent-review-2026-09-29-turn-01-claude.md` at `27999316`. The reviewed
MAM-basics window remains `f4d81285..7549ebf7`. The procedure changes on
`origin/main` at `89c001ba` postdate that window and govern this turn's checkout.

The development checkout was the clean full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on its existing local carrier
`dar-2026-09-29` at `27999316`. A fresh fetch showed
`origin/dar-2026-09-29` at exactly `27999316`, and `origin/main` at
`73bb4a7b`; the latter contains `89c001ba`. Three read-only sub-agents worked
through findings 1–12, 13–24 and 25–35 against the frozen public tree, with
selected checks of item 36's questions. Codex checked
the shared procedure, central qualifications, the omission below and the
reconciliation. No MAM-private content, manuscript image or legal source was
read. This turn changes only this file and the specified reconciliation append
to turn 01. It fixes no reviewed defect and makes no issue or product change.

## Assessment of the argument

Turn 01 identifies substantial unfixed work at `7549ebf7`: the lost merge
changes, incomplete close-out records, validation gaps, stale retirement
documentation, and contradictory instructions survive this check. One narrow
omission concerns the special-page downloader's atomicity promise. Several
other findings need narrower classifications or evidence limits. In
particular, a documented fetch does not make a configuration check's
"read-only" label an undisclosed operation, and public tracked evidence cannot
establish the present contents of an untracked proposal or private input.

The table appended to turn 01 assesses every numbered finding. "Confirmed"
means a cited condition survives checking, not that it has been fixed.
"Qualified" preserves a supported condition while narrowing its cause,
scope or consequence. A subclaim marked "unchecked" is left for a later turn or
Ben's decision. Every accepted defect remains unfixed by this review.

## C1. The special-page mirror is not replaced as one atomic unit

**Omitted, unfixed documentation claim.** `py/ws/ws_special_page_download.py:441`
says `download()` will "atomically replace the special-page mirror". The
function validates the complete response before writing, as the approved
`doc/PLAN-retire-google-sheet.md` requires, but then replaces each fetched
`.mediawiki` file separately (`:499–500`) and writes `manifest.json` last
(`:501–508`). `py/mb_cmn/file_io.py:22–36` makes each file replacement atomic;
there is no whole-directory transaction. A write failure after one replacement
can leave a mixed set of pages with the old manifest until a subsequent run
repairs it. The planned validation-before-write and manifest-last sequence is
implemented; the docstring alone promises more than that sequence provides.
This wording was introduced with the new downloader by `a41fbcdd`.

## C2. Finding 11 overstates the test-shape verdict for one test

**Qualified.** Four fault-injection tests in
`py/tests/test_wikisource_special_page_download.py:193–259` are selected
scenarios, and the inventory check at `:131–132` is lint-shaped. The remaining
full-inventory round trip at `:135–190` compares all 36 emitted page bytes to
content supplied independently by its stub API, including reuse and forced
download. A stub does not make that comparison automatically invalid as a
differential test. Whether the stub supplies an independent enough oracle for
the repository's test rule is a judgment; the categorical "neither
differential nor lint-shaped" description of all five stub tests is too broad.
All six tests pass, and this review proposes no test edit.

## C3. Findings 14 and 23 include accurate historical wording

**Finding 14.3 is qualified.** The current-header wording in
`py/py_misc/mam_parsed_plus.py:33–34` and the shared-snippet heading in
`py/author_misc/mp_cmn_examples_and_file_naming.py:12` remain stale after the
plain product's retirement. The statements in
`py/hkq_cmn/mam_plus_verse_data.py:52–57` and
`py/hkq_cmn/qere_projection.py:412–415` call a sentinel a "plain-file
concern" precisely to distinguish it from plus data; they do not claim that
plain files remain a current product. `py/ws/ws_plain.py` still performs a
transient conversion. Those passages should not all be classified as false
current-product claims. The dead lint entries, import, constant and bare
deleted-file citations in finding 14 remain.

**Finding 23 is qualified.** The bot's post-run path in
`py/subcommands/ws_bot_real.py:270` calls
`py/subcommands/download_wikisource.py:27–34`, which force-downloads all 36
special pages as well as the modified chapters. The refresh skill and
`py/ws/pywikibot-setup.md:55–57` describe only the chapter results. Their
account is incomplete about the new special-page side effect; neither passage
literally says "only chapters". The side effect became current when
`a41fbcdd` and `86132514` met in the window's merge.

## C4. Findings 17, 22 and 24 need precise coverage limits

**Finding 17 is qualified.** `py/verify_mp/parser_stage.py:242–249` compares
the parser-stage and plus aliyah or `mpasuq` records. The two collectors skip
other D-column labels, including `סדר`
(`py/tmpl_survey/column_d_0_store_the_mpasuq_call.py:59–61`). The validation therefore
does not establish equivalence of every D-column label. The narrower question
is whether the plan's "labels" requirement meant every label; the old plain
verifier did not cover that broader set either.

**Finding 22 is qualified.** The refresh added a 2 Kings 22:1 qamats variant
to MAM-parsed plus (`97c4aff5`); the public phonetic-hbo page and the tracked
survey still reflect the older variant set. The survey module says its
Phonetic MAM corpus is a snapshot that may lag MAM-simple
(`py/accgram/post_stress_meteg.py:18–24`). Thus the public evidence establishes
a specific lag after a survey refresh attempt, not the private input's cause or
a general promise of complete currency. This review did not read Phonetic MAM
or determine an expected replacement count from it.

**Finding 24.2 is confirmed with a broader scope limit.** Explicit `--old`
and `--new` runs reach `generate_report` without the stored-boundary guard
(`py/subcommands/diff_mpplus.py:597–605`). A no-argument run guards only the
latest release's end (`:317–324`), while `--all` and `--check` inspect the full
boundary list. The README's "Every change-log run" claim must name those
different paths. Finding 24.1's two dates describe different objects and also
remains.

## C5. Findings 29–34 need narrower conclusions from public evidence

**Finding 29 is an editorial ambiguity, not a hidden fetch.** Both
`dot-Codex/README.md:116–127` and `dot-claude/README.md:79–92` expressly say
that synchronization fetches `origin` before presenting `--check` as the
"read-only form". The check does write local Git metadata, but it leaves live
configuration destinations unchanged. Turn 01 proves a possible ambiguity in
"read-only", not that the README conceals a fetch or contradicts its own
description. More exact wording would help a reader who treats all local writes
as outside read-only work.

**Findings 30–32 are qualified.** The tracked plan names a `.novc/` proposal
and does not preserve its P01–P26, N01–N08 and A01–A02 list in tracked text;
routine maintenance can delete `.novc/`. That is a durable-record risk, but a
public-only review cannot establish that the proposal is the sole surviving
copy, that it is still present, or what it contains. Two live source passages
still point to retired auto-memory names (finding 31); the tracked retirement
record supports the concern, while the deleted store was not inspected. The
rule and code differ over how the scan archive is discovered (finding 32), but
current machine environment settings are not public evidence. The conflict
between the tracked rule and the tracked default is the reviewable claim.

**Finding 33 is confirmed as a scope ambiguity.** The general rule about
fetching and merging before a full clone pushes `main` can be read to include a
worktree's home clone. The more specific worktree rule permits only a verified
fast-forward there (`dot-Codex/user-wide-AGENTS.md:83–84,123–126,165–166`).
The specific rule can resolve an execution, but the common body should state
the exception so a reader does not choose the wrong merge location.

**Finding 34 is partly qualified.** "Manual document retirement" exists in
`mam-repository-topology`'s `references/repository-maintenance.md`, and its
skill routes maintenance readers there. The four citations omit the reference
name, making discovery harder rather than pointing to a nonexistent section.
The GitHub-issues reference's open-or-closed review-State shorthand is
substantively wrong. The omitted old worktree-ban quotation is a weaker
historical navigation problem: the reference identifies the withdrawn ban and
Git history retains its exact words.

## C6. Finding 36 preserves decisions that belong to Ben

**The twelve items remain questions, not approved remediation.** Item 36.2
has a concrete policy conflict: `AGENTS.md:163–164` and
`py/product_scopes.py:51–53` require rerunning affected hand-run generators,
while the MAM-for-Sefaria and MAM-OSIS READMEs explicitly permit lag. Ben must
decide which rule governs the two stale verses before a later phase treats a
rerun as required or exempt. The public record cannot decide the legal clarity
of a licence grant (36.1) or whether the account and private metadata listed in
36.5 is acceptable. This turn asks no such decision and changes no product.

## Verification and remaining limits

The fetched review branch was exactly the promised handoff commit. The frozen
window has 91 commits, and `origin/main` had eight later commits at the first
fetch; those counts reproduce with `git rev-list --count`. The read-only checks
covered the principal cited sources for findings 1–35 and selected sources
for item 36, but did not rerun
turn 01's suite, mega, full generated-artifact census, GitHub issue census or
all of its large numeric measurements. Some counts and outside-account claims
therefore remain dependent on turn 01's preserved evidence. No review finding
was fixed here. Claude's next turn can accept or contest the qualifications
and C1 against the cited public sources; close-out owns Ben's decisions and
later remediation.
