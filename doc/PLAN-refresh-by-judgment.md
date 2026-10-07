# Judge a Wikisource refresh by its diffs, not by pinned hashes

State: live; approved by Ben on 2026-10-07; executing since 2026-10-07 on his instruction.

Written on 2026-10-07, New York time, by a Claude session (Claude Opus 5.5 in the Claude desktop
app). The session worked in the full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, whose clean
`main` it fast-forwarded from `cfb3a284` to `08fcae33e43da502fb4ab5a0dd48668b259751d0`, equal to
`origin/main` after a fetch. Ben opened the session by pasting a prompt that another Claude session
(Claude Opus 5.5) wrote the same day: the session that ran the post-maqaf ketiv/qere bot, commits
`0067293b` to `cfb3a284`. That prompt quotes four of Ben's messages to it and says that the rest is
its own reconstruction; this plan attributes none of that reconstruction to Ben. Ben's words in
this session are quoted under "Ben's decisions".

**What is approved and what is not.** Ben approved the rule, the dispositions and the skill text
below on 2026-10-07 and asked for this plan. Writing, committing or pushing this plan implements
none of it. Execution begins only when Ben explicitly says to execute. He did so the same day, in a
fresh Claude Code session (Claude Opus 5.5) in the same clone: "Yes, execute waves 0 to 8 as
written."

**How it was prepared.** Twelve read-only sub-agents, some with read-only helpers of their own,
worked under the session's scratch directory, outside the checkout, each reporting
`git status --porcelain` empty at its start and end: four verified the gates that the opening
prompt named and took a census of the rest; seven wrote
implementation briefs (near-Aleppo pointings; near-Aleppo ledger, census and populations; Phonetic
MAM; Yeivin ITM; test pins; statement checks; runbook and documentation); one inventoried the
input hashes that products record. Their prototypes ran in memory or on scratch copies. The root
session re-read the passages that each adopted claim rests on, among them the digest and import
code of `py/near_aleppo/frozen_ketiv.py` (`:27-32`, `:128-177`), the census refusal
(`py/near_aleppo/build_expectations.py:104-110`), the mega's near-Aleppo sequence
(`py/main_0_mega.py:121-124`), the replay test's helper
(`py/tests/test_near_aleppo_note_content.py:189-218`), the Yeivin pins
(`py/yeivin_itm/claim_schema.py`), the marker-label corrections
(`py/phonetic_mam/display_projection.py:190-205`), and `py/main_diff.py mpplus`'s acceptance of
any MAM-basics revision (`py/mb_diff_mpu/mpplus_revisions.py:247-354`); and it re-ran, read-only,
the comparison showing that the bot run's four chapters still match the legacy Phonetic MAM
hashes in both pronunciations.

**Citations.** Line numbers are those of `08fcae33`, where the investigation measured. Before this
plan was committed, `origin/main` moved to `3bd11204`; of the files it cites, that move changed
`AGENTS.md`, `Phonetic-MAM/README.md`, `py/main_0_mega.py`, `py/near_aleppo/doc_page.py`,
`py/author_misc/mp_cmn_rows_other.py` and `py/product_scopes.py`, and this plan's citations of
those six were rechecked at `3bd11204` and give its line numbers. Each citation also quotes or
names a passage so that it survives line drift. This plan names no path inside a private
repository.

**Verification follows the trial.** `doc/review-trial.md` (approved by Ben on 2026-10-07, after
this plan's dispositions) governs verification while it lasts: each change gets focused checks
matched to its surface, including formatting and the relevant regeneration and comparison; the
full suite and the mega run nightly; a broad check runs at once only for a stated consequence that
cannot wait; and plans add no blanket checks or proof ceremony. Its section "Focused work and
nightly checks" names this work: "Ben's separate Claude sessions own the near-Aleppo sealing
simplification and the lighter Wikisource-update process", and "Do not preserve or reintroduce
retired hash/sealing/replay gates." Each wave's checks below are the focused ones.

**Asking Ben.** Ben said on 2026-10-07 that Claude Code's multiple-choice dialog may hide the
context of a question from him. Put any decision this plan leaves to him in the chat message
itself, with what raises it and what each choice would do, and ask him to answer in his own words.

## Ben's decisions

All on 2026-10-07, in this session.

1. **The pointed-ketiv check covers the whole qere.** Of a proposal to check only that a pointing's
   target keeps its ketiv letters: "In particular, why not extend the check to include the entire
   qere word? Just checking that the ketiv letters haven't changed is an overreaction, careening
   from (a) complete way too heavy hashes insisting on identical MAM sources, down to millions
   (literally) of irrelevant details to (b) casually creating a pointed ketiv that doesn't have the
   points of the qere, a logical contradiction." (His next message corrected "way to" to
   "way too", which this quotation applies.)
2. **The rule and its dispositions.** The session's report "Taking a Wikisource update without
   seals" proposed the rule, ten dispositions for the near-Aleppo, Phonetic MAM and Yeivin ITM
   checks, dispositions for the rest of the repository, a section for the refresh skill and a
   sentence for `AGENTS.md`. Ben replied: "I accept all and yes write a plan".
3. **Three answers, later confirmed in prose.** Asked through the dialog, Ben chose to keep the
   approved wording and retire both the Phonetic MAM legacy comparison and the input hashes that
   products record; to say "Each regeneration commit's message"; and to move every reader of the
   vendored Decalogue capture to the download mirror. After the session restated the three in
   prose, he wrote: "I reviewed your review of decisions made under the suspect interface and those
   all look fine to me ... I confirm my approvals."
4. **`AGENTS.md`: guidance by suggestion; false statements fixed.** Ben first wrote: "for the
   moment I've soured on any changes to agents.md. I think they're a waste of time and tokens."
   He then added: "Absolutely fix false things in AGENTS.md. You are over-generalizing my
   pessimism about whether it is wortg putting advice/guidance into AGENTS.md. It feels to me like
   fixing false statements is quite another thing, and should obviously be done (either by
   removing them or correcting them, whichever seems most appropriate on a case-by-case basis)";
   and then: "I wouldn't say "no new guidance". I was just venting. Please suggest guidance,
   although I may reject a lot of those suggestions." The `AGENTS.md` sentence of decision 2 was
   therefore suggested to him again, and he accepted it the same day ("accept 1, 2 and 3"). It
   says that products derived from MAM's text have no hashes of their inputs, which is false until
   this plan has run, so wave 7 adds it. If executing this plan makes a statement in `AGENTS.md`
   false, correct or remove it in the same wave.
5. **A changed ketiv or qere at a stored pointed ketiv waits for Ben.** "Just let's go with the
   more invasive thing that if any [qere] changes in MAM, just stop the whole world and bug me about
   it. It is more work to design a process to try to be smart than to just be dumb and give me the
   incremental work period. Or at least that's what we should try to do for now." (The transcript
   reads "array" for "qere".)
6. **Git, not software over old commits, is the test.** "Git is the basic test of most of these
   programs. including near Aleppo, but you don't have to literally write tests based on Git. ...
   The point is that you scrutinize the diffs in a kind of non-deterministic, almost human-like,
   AI-assisted way upon committing. You don't actually write software that uses old commits and
   makes sure nothing changed." So both near-Aleppo checks that read old commits are retired.
7. **A detail left to the session.** Of whether the Yeivin claim file keeps its constant
   `input.identity` once its hash goes: "I really don't care. This is beneath the level of detail I
   care about." This plan keeps it (wave 4).

**Earlier decisions this plan keeps:** the parser-stage grammar lock (Ben, 2026-09-30) and the
plus-survey grammar lock (accepted 2026-09-10), both recorded in `py/tests/test_mega_coverage.py`;
the 20 Yeivin fractions he approved; the Phonetic MAM display corrections he approved on
2026-10-06, which the exporter applies; that a bot run's record takes its special-page changes
(2026-10-01); that a text refresh does not oblige rerunning MAM-for-Sefaria, MAM-OSIS (2026-09-30)
or `py/main_hbce_psalms.py compare` (2026-09-26); that the mega writes nothing outside this
repository (2026-09-11). **Earlier decisions this plan supersedes:** Gate B (the Yeivin
claim-population hash) and Oracle A (the legacy comparison's skip rule), both of 2026-10-03, which
it retires; the re-seal of 2026-10-06, whose mechanism it removes.

## The rule

Products derived from MAM's Wikisource text take a refresh through the agent's judgment of every
diff (decision 6 states the same for code changes). No check pins hashes, fingerprints or
populations of their inputs, and no product records hashes of its inputs. The checks that remain
are closed dispatch (an unrecognized template or shape raises) and checks that a hand-made
statement about the data still holds, covering exactly what the statement depends on: a stored
pointed ketiv's check covers its ketiv and its whole qere, letters and every mark, and not its
template's name.

Checks that compare a tracked output with what the code regenerates from the current tree, such
as `py/main_near_aleppo.py --census --check`, `py/main_diff.py mpplus --check` and
`py/main_yeivin_itm.py check`, stay: they read no old commit, and they are the mechanical side of
the same diff review.

Approved for `dot-claude/skills/mam-wikisource-refresh/SKILL.md`, verbatim except for decision 3's
"Each regeneration commit's message" in its step 4:

```markdown
## Judge every diff: the expected changes, and only them

The agent's judgment keeps a refresh honest; no hash, fingerprint or pinned population
does. Ben chose this standard on 2026-10-07 as "a good use of AI's approximate
not-quite-reasoning".

1. **Commit the source change first.** Commit the download's chapters, revisions and
   reparse, or a saving bot run's record, before the mega runs.
2. **Predict.** Read the change verse by verse with `py/main_diff.py mpplus --old
   <starting HEAD> --new HEAD --output <scratch path>`. Write down what it should cause:
   which verses, in which products, of what kind (a renamed template, a reordered
   ketiv/qere pair, a changed accent), and which counts move, by how much.
3. **Judge.** After each regeneration, read every tracked diff and check (a) that every
   predicted change is present and (b) that nothing else changed. Explain anything else,
   or stop.
4. **Record.** Each regeneration commit's message states the prediction and confirms (a)
   and (b), product by product.

The checks that remain are closed dispatch, and checks that a hand-made statement about
the data still holds: a prose claim, a quoted form, a stored pointed ketiv. Such a
statement does not change when the data does, so no diff shows it going stale. When one
fails, repair the statement, or the derived record and what it records, in one
reviewable edit. When the statement is Ben's published claim, stop for his approval and
let the rest of the refresh proceed.
```

The quotation "a good use of AI's approximate not-quite-reasoning" comes from the opening prompt's
quotation of Ben's message to the bot-run session; Ben approved this text with it.

## Checkouts, interpreter and integration

1. **Source.** `origin/main` of `bdenckla/MAM-basics` at or after the commit that adds this plan.
2. **Development checkout.** The full clone `C:/Users/BenDe/GitRepos2/MAM-basics` on `main`, when
   no other session is writing in it; otherwise a linked worktree of it, under the user-level
   linked-worktree safeguards, with the home clone's interpreter by absolute path. Before the first
   edit, record `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch and
   `git status --porcelain`, and require this plan's commit to be `HEAD` or its ancestor.
3. **Interpreter.** `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe`, run from the
   development checkout's root.
4. **MAM-private.** `C:/Users/BenDe/GitRepos2/MAM-private` on `main`, equal to its `origin/main`.
   This plan writes nothing there; the mega's `phonetic-mam-export` step reads its adapter
   read-only. Near-Aleppo's original research, including the tool that made the frozen pointings,
   lives in MAM-private's near-Aleppo research tree; name it in public files only by its existence.
5. **Integration.** The executing session owns it. Push `main` after each wave once its focused
   checks pass: fetch, merge a moved `origin/main` and rerun the focused checks the merge owes,
   read every tracked diff, push. The nightly run supplies the full suite and the mega
   (`doc/review-trial.md`); push near-Aleppo's waves 1 and 2 promptly, since other sessions work
   there.
6. **Skills.** Load `hebrew-prose` with its `references/mam-basics.md` before writing prose about
   ketiv/qere, accents or meteg, and `iterative-document-editing` for this plan's State and ledger.

## Coordination

1. **2 Kings 14:7.** Near-Aleppo's stored pointed ketiv at 2 Kings 14:7 (frozen record
   `BD-2Kings:14:7:0`) has two pashtas, which appear to contradict the Aleppo reading that
   near-Aleppo applies to that qere. Ben asked the planning session for a prompt to take it up in
   a session in `C:/Users/BenDe/GitRepos3/MAM-basics`, and the planning session wrote one, but no
   session took it up: when execution began, that clone held nothing beyond `origin/main`, and no
   session but the planning session's had named the record. Wave 2's conversion runs on the tree
   current at execution; whoever later takes up 2 Kings 14:7 edits the converted record. Ben chose
   the same day that the executing session write a fresh prompt for it once wave 2 is pushed:
   "Yes, wait for a fresh prompt."
2. **`unicodedata.normalize`.** `d66a3faf` reworded `AGENTS.md`'s rule on it and closed review
   item 8.10 without changing `py/tests/test_decalogue_m_trad.py` (`:113-115`, `:124`) or
   `py/accgram/decalogue_m_trad.py:154`. Leave those calls as they are.
3. **One writer.** Other sessions edited near-Aleppo as recently as `20d2c7bd` and `e5cd5997`.
   Fetch before each wave and before each push.

## Wave 0. Preflight

Verify the checkouts as above. Record the current `origin/main` commit and list the commits since
`3bd11204` that touch any path this plan edits; re-measure the figures this plan quotes in the
waves those commits affect.

## Wave 1. Near-Aleppo: the note-review ledger, the census and the population file

Dispositions 4, 5 and 6, and the fixed counts. Lands before wave 2, so that wave 2's edits move no
ledger hash. Two or three commits (ledger; census and population file; mega steps). Every
near-Aleppo output stays byte-identical: the 24 `out/near-aleppo/plus/*.json`, all of
`gh-pages/near-aleppo/`, and the five census `.txt` files under `in/near-aleppo/census/`.

Measured at `08fcae33` in read-only scratch runs: the census reproduces every census-backed count;
an in-memory build equals `in/near-aleppo/build-populations.json` on every shared label and site
list; the ketiv/qere apparatus removes exactly one qamats qatan at each of Isaiah 44:17,
Ezekiel 24:2 and Psalms 89:29 and none at its other 20 calls; the ledger has 1,548 reviewed rows
and round-trips byte-identically.

1. **The ledger keeps its per-note evidence and loses its whole-file hashes.**
   `py/near_aleppo/doc_note_review.py`: delete `input_hashes()` (`:40-66`) and `import hashlib`;
   `refresh()` writes `{"version": 2, "inventory_sha256", "notes"}`; `load()` replaces its refusal
   "Doc-note review inputs changed" (`:303-306`) with a closed shape check (keys exactly `version`,
   `inventory_sha256`, `notes`; version 2). Keep the per-note evidence (`:258-259`, `:271-280`,
   `:284`, `:307-336`, `:394-403`). `refresh()` reads only `old["notes"]` (`:268-269`), so the
   first refresh carries every review over. Afterwards a comment edit in a near-Aleppo module, or a
   change to `build-populations.json`, no longer moves the ledger, and the two-mega settling of
   `3b8e84d4` disappears. Expected diff: `in/near-aleppo/doc-note-review.json` loses its 37
   `input_sha256` entries and its version becomes 2.
2. **The census loses its provenance; its agreement with the build becomes a differential.**
   - `py/main_near_aleppo.py` `_census` (`:30-76`) only writes or, under `--check`, byte-compares
     the five `.txt` files: drop `:35-37`, `:47-50` and `:64-75`; `git rm
     in/near-aleppo/census/provenance.md`.
   - `py/near_aleppo/build_expectations.py`: delete `_git`, `_provenance_prefix`,
     `current_census_input_ids` (whose refusal "The near-Aleppo build inputs have uncommitted
     changes" at `:104-110` stopped the bot run's mega), `is_current`, `_CENSUS_INPUTS`,
     `_CENSUS_PROVENANCE` and `refreshed`. Keep the census parsers (`_single_int`,
     `_template_inventory`, `_CENSUS_PHASE2_LABELS`) in a new
     `assert_census_agrees(resolver, policies, readings, mam_targets)`, raising one combined error
     unless: each `_CENSUS_PHASE2_LABELS` count equals the census's settled column;
     `_QAMATS_QATAN` equals the census's "taking ד" count less the apparatus removals (item 4);
     `_ELOHIM_SHEVA` and `_ELOHIM_BARE_YOD` equal their census rows; Adonai stripped plus kept,
     and title stripped plus kept, equal their census totals; `_NOT_TITLE` equals the total less
     the title count; pashta stripped equals the census's second-to-last-letter row, and each
     accent's stripped, between, kept-by-codex and kept-by-ל counts sum to its total; phase 5's
     `_NOTES` and phase 6's notes reached equal the settled counts of נוסח and מ:הערה-2.
   - `py/near_aleppo/main_build.py:186-194` (the provenance call and its stale-ids refusal) gives
     way to a call of `assert_census_agrees`.
3. **The build writes `in/near-aleppo/build-populations.json`.**
   - Remove `assert_expected_counts` from `phase2_templates.py:210-218`,
     `phase3_policies.py:773-786`, `phase5_readings.py:515-542` (including its rejection of a
     label the file lacks, a population pin that becomes vacuous), `phase6_mam_targets.py:118-125`
     and `phase6_flags.py:215-228`, and their callers at `main_build.py:200-210`. Keep the Renames
     check (`phase6_rename.py:52-63`), comparing with `mam_targets.counts` of the same run.
   - Delete `write()`'s refusal to change the three site maps and its splicing of the text read
     with `git show HEAD:` (`build_expectations.py:335-371`). The build renders the whole file
     after every check passes and writes it with the dataset; under `--check` it byte-compares the
     file too. Remove `--refresh-expectations` (`py/main_near_aleppo.py:94-98`, `:115`;
     `main_build.py:174-183`, `:188-197`, `:214-215`).
   - Format: `schema_version` 5; no `census_input_ids`; each site on its own line as
     `["book", "c", "v"]`. Seed each phase's counter and site map with a declared tuple of today's
     labels, zeros included (the documentation pages read five zeros by key: pashta and segolta
     kept by the codex or by ל, and zarqa kept by ל), then append every other tallied label in
     sorted order, which adds phase 2's 12 counters the file omits today.
   - Expected diff: this one-time rewrite (about −568/+501 lines of layout, +12 lines of counters,
     schema 4 to 5, `census_input_ids` gone), with identical values; prove that in a scratch
     comparison of the old and new JSON.
4. **Named-site statements that replace pins.**
   - `_KQ_QAMATS_QATAN_REMOVALS = 3` (`build_expectations.py:35-40`) becomes
     `_KQ_QAMATS_QATAN_REMOVED_VERSES = (("C1-Isaiah", "44", "17"), ("C3-Ezekiel", "24", "2"),
     ("D1-Psalms", "89", "29"))` beside `_KQ_FORM_FROM_NOTE_VERSES` in `phase3_policies.py`; at
     the apparatus call (`:815-817`) count the qamats qatan before and after; `apply_e_cell` raises
     unless the count drops by one at each named verse and by none elsewhere.
   - `_NAMED_DOUBT_VERSES` and `_AGREEING_BANG_VERSES` (`phase6_flags.py:163-168`) lose their only
     found-once guard with the population file: add a found-exactly-once check like
     `_SILENCE_SITES`'s (`:207-212`).
   - The sentence that `py/near_aleppo/doc_changes.py:697-698` renders ("where the codex is lost
     … in the Leningrad Codex, at") rests on sites that only the population file guarded: check
     them against `doc_figures._CodexIndex().extant`, or reword the sentence to state only what the
     data shows. Comments that state a data-derived fact as fixed, such as "at Psalms 110:5 alone",
     are reworded to state the rule.
   - Keep, as statement checks: phase 3's `_KQ_SITES` (`:664`, checked at `:759-765`) and the
     tables checked at `:734-770`; phase 5's `_TABLES` (`:507-512`); `_SILENCE_SITES`
     (`phase6_flags.py:88`, checked at `:207-212`).
5. **Fixed counts.** Drop `_VERSE_COUNT` (`main_build.py:41`), the `verses` counter (`:66`, `:108`)
   and its check (`:119-120`). `_BOOK_FILE_COUNT` (`:40`, `:53-56`) becomes closed dispatch over
   the book set: the input file stems equal
   `{tbn.ordered_short_dash_full_24(b) for b in tbn.ALL_BK24_IDS}`, raising with the missing or
   unknown stems.
6. **The mega's near-Aleppo steps** (`py/main_0_mega.py:121-124`) become `--refresh-note-review`
   then `--build`; the build already runs `doc_note_review.check()` (`main_build.py:47-50`), so
   `--check-note-review` leaves the mega and is declared in `py/tests/test_mega_coverage.py`'s
   `NOT_IN_MEGA`. Update the build step's note (at `3bd11204`, `py/main_0_mega.py:728`, "local MAM
   plus sealed pointings"). `3bd11204` already says, in the mega's docstring and its comment at
   `:606`, that the present step named `near-aleppo-census` is the local census of 2026-10-05, not
   MAM-private's step deleted on 2026-09-11; say the same in `py/mb_cmn/graphviz_pin.py:63` ("until
   that step was deleted on 2026-09-11") and `py/tests/test_mega_coverage.py:548-549`.
7. **Texts.** `main_build.py:1-17` (its docstring says "sensitive site lists and added-target
   populations stay pinned and require review when they move"), `:176-178`, `:190-193`;
   `build_expectations.py:1-10`, `:35-45`; `doc_note_review.py:3-6`; `main_html_pages.py:11-17`,
   `:185` ("provenance-pinned"); `main_near_aleppo.py:1-10`, `:97`; `phase3_policies.py:43`,
   `:170-173`, `:444-450`, `:681-694`; `phase5_readings.py:447-451`, `:1020-1021`;
   `phase6_mam_targets.py:51-64`; `phase6_flags.py:52-55`; `doc_html.py:15-18`, `doc_page.py:5`,
   `doc_changes.py:4-5` ("asserted snapshot"); `note_content.py:26`; `phase6_rename.py:8`;
   `doc/near-aleppo-build.md:23-24`, `:46-58` (including its unchecked "1,548", which becomes a
   description); `out/near-aleppo/README.md:36-38` ("changed input identities", "moved
   populations"). The rendered "asserted snapshot" at `gh-pages/near-aleppo/choices.html:586` comes
   from a dated choice record in `doc_choices.py` (`:647`); leave it.
8. **Verify** after each command with `git diff --stat`, explaining every path:

   ```powershell
   ./.venv/Scripts/python.exe py/main_near_aleppo.py --census
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_near_aleppo.py --refresh-note-review
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_near_aleppo.py --build
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_near_aleppo.py --html
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_near_aleppo.py --check
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_test.py py/tests/test_near_aleppo.py py/tests/test_near_aleppo_note_content.py py/tests/test_mega_coverage.py py/tests/test_product_scopes.py
   ```

   Then run `--census`, `--refresh-note-review` and `--build` a second time and require no diff:
   the property item 1 restores.

## Wave 2. Near-Aleppo: readable pointing records, and no software over old commits

Dispositions 1, 2, 3 and 7, decisions 1, 5 and 6. Every near-Aleppo output stays byte-identical
except the generated documentation that item 6 names.

Measured at `08fcae33` in read-only scratch runs: an in-memory replay captured each record's target
at its check point, and every old digest matched it (723 frozen records, before and after, 236
reviewed, 5 editorial); readable importers then rebuilt all 24 `out/near-aleppo/plus` books
byte-identical. Only one frozen record's target differs between its two check points:
`BD-2Kings:14:7:0`, whose qere a phase-5 reading changes.

1. **The check.** A shared helper in `py/near_aleppo/frozen_ketiv.py` resolves the record's `path`
   (raising, with the record's id, if it does not resolve), requires the template's name to be in
   `phase2.POINTED_KETIV_FAMILIES` (closed dispatch) and no pointed ketiv to be present, then
   requires `target["tmpl_params"] == row["tmpl_params"]`; otherwise it raises
   `"<id>: target parameters differ from the record"`, showing the recorded and current parameters
   as sorted JSON. The template's name is not compared, so a rename such as the bot run's from
   כו״ק to קו״כ passes; any change to the ketiv, to the qere's letters or marks, or to סוג fails.
   The check runs once, where the pointing is written (`apply`); delete `check_source` and its
   calls (`main_build.py:89`; `doc_note_review.py:204`).
2. **Conversion of the three manifests**, with the importers of the tree current at execution, in a
   scratch script, before editing them: subclass `FrozenPointing`, `EditorialPointing` and
   `ReviewedPointing` so that `apply` asserts `digest(at_path(cell, row["path"]))` equals the
   record's `after_sha256` or `expected_sha256`, records a deep copy of that target's
   `tmpl_params`, and calls `super().apply`; assign the subclasses into `main_build`; call
   `main_build.build(bake_notes=False)` (it runs every stage and writes nothing); write each record
   with keys `id, verse, path, tmpl_params, value` (editorial: `id, verse, path, tmpl_params, ga,
   value`), through `json.dumps(data, ensure_ascii=False, indent=2) + "\n"` with LF endings. Formats
   become `near-aleppo-frozen-pointing-v2`, `near-aleppo-reviewed-pointing-v2` and
   `near-aleppo-editorial-pointing-v2`. Drop `before_sha256`, `after_sha256`, `expected_sha256`,
   `canonical_sha256` (only syntax-checked; its derivation is unknown), `atoms` (unread once
   `ATOMS` goes), `input_sha256` and `target_mam_commit`; keep the frozen manifest's
   `algorithm_commit` and `mam_input_commit` as inert provenance of the values. The scratch run at
   `08fcae33` converted 723 + 236 + 5 records with no failure. If MAM-parsed has changed since the
   last re-seal, the importers' `input_sha256` comparison refuses to start: skip it in the
   subclasses, since this wave retires it and the per-record assertions still prove each target.
   A record whose digest no longer matches is one whose ketiv or qere changed after it was sealed:
   stop and ask Ben about that record, as decision 5 says, before converting it.
3. **Code.**
   - `frozen_ketiv.py`: delete the comment and constants at `:17-22` (`MANIFEST_SHA256`, `SITES`,
     `ATOMS`), `_HEX` and `check_source`; `validate_manifest` takes the closed v2 schema
     (`tmpl_params` holds "1" and "2", may hold only "1", "2" and `סוג`, all strings); keep
     `_FORBIDDEN`, the duplicate-id and duplicate-address checks and `validate_value`; `load()`
     drops the hash check; `__init__` drops `input_dir` and its `input_sha256` comparison. Keep
     every "applied exactly once" check (`finish`).
   - `reviewed_ketiv.py`: the same changes (`:9`, `:17-19`, `:25`, `:32-37`, `:51-52`, `:58-59`,
     `:64-71`, `:85-89`).
   - `editorial_ketiv.py`: drop `:4`, `:12`, `:26-27` and the count check at `:34-35`; add a
     duplicate id and verse check, since `by_verse` (`:46`) is keyed by verse and the count of 5
     was the only guard against two records in one verse. Keep `ga`, a statement checked against
     the value.
   - `main_build.py:63`, `:65` and `doc_note_review.py:192`, `:194` stop passing `input_dir`;
     `doc_note_review.py:21` imports `digest` for its per-note hashes, so keep `digest` where it is.
4. **Two hashes of hand-made dependencies become readable.**
   - `py/near_aleppo/doc_genesis_ketiv.py`: `NOTE_SHA256` (`:18`, used at `:33`) hashes the whole
     Genesis 43:28 note. Replace it with a check that the note's name is נוסח, its parameters are
     exactly "1" and "2", and its body equals a `NOTE_BODY` copied from the data by script, as
     `doc_daniel_sheva.py:34-47` already does for Daniel 5:21; drop `:8` and `:18`; keep `:34`.
   - `py/near_aleppo/consumer_notice.py`: `_MAM_NOTICE_SHA256` (`:28-33`, `:150-157`) forces
     near-Aleppo's NOTICE, which adapts MAM-parsed-plus's notice, to be re-derived when that notice
     changes. Replace it with a readable copy `_MAM_NOTICE` in the module, compared by equality,
     whose error names the book and says to carry the change into NOTICE and then update the copy.
5. **Retire near-Aleppo's two checks over old commits** (decision 6).
   - The MAM-mode differential: `py/near_aleppo/edition.py`'s `PIN` (`:34-36`), `check_mam_mode`
     and its helpers (`:278-397`, including `_git` and `_blobs_at_pin`), and `MAM_MODE` (`:185`)
     with any code reachable only from it; its call in `py/near_aleppo/main_html_pages.py`
     (`:99-103`); and, in `py/tests/test_near_aleppo.py`,
     `test_shared_renderer_matches_independent_mam_with_doc_files` (`:16-19`, which also pins a
     count of 62). The `--html` step then reads no old commit, so it also works in a shallow clone.
   - The baseline replay: `py/tests/test_near_aleppo_note_content.py`'s
     `test_dataset_only_renderer_matches_prior_edition_from_the_same_baseline_inputs`
     (`:132-186`) with `_BASELINE`, `_names`, `_blobs` and `_baseline_pointing_order_corrections`
     (`:189-218`) and the imports only they use. Keep the module's other two tests.
   - Texts: `edition.py:1-4` ("must match the independent tracked MAM-with-doc files at PIN on
     every HTML run"), `main_html_pages.py:7`, `doc/near-aleppo-build.md:61`,
     `out/near-aleppo/README.md:41-43`, and the test module's docstring (`:1`). The choice record
     rendered at `gh-pages/near-aleppo/choices.html:575-577` is dated; leave it.
6. **Texts that describe the digests.** `frozen_ketiv.py:3`; `reviewed_ketiv.py:1`, `:23`;
   `main_build.py:1`, `:5-6`; `consumer_notice.py:3-6`; `phase5_readings.py:87`;
   `py/render_wt/render_wikitext_kq.py:141`; `py/main_0_mega.py:728` (at `3bd11204`, unless
   wave 1 reworded it); `doc/near-aleppo-build.md:5`, `:28-29` ("Sealed file hashes and per-site
   source guards reject drift": describe the recorded parameters and the error that names the
   record), `:62`; `doc/PLAN-near-aleppo.md:19`; `out/near-aleppo/README.md:19`. Change the
   rendered sentence of
   `doc_changes.py:925-931` ("includes only the sealed pointings and target guards", reaching
   `gh-pages/near-aleppo/editorial-policies.html:417-420`) to say what the build now checks:
   expected diff, that page only. Leave "sealed reviewed portable decision"
   (`consumer_notice.py:84`), which names the review's fixity, not a hash; changing it would
   rewrite all 24 distributed books.
7. **Verify** as in wave 1, plus `git diff --check` and Black on every changed Python file.
   Expected diffs: the three manifests (smaller, readable), the code, the texts, the one generated
   page in item 6. Check the new check's two behaviours in memory: renaming a target's template
   from כו״ק to קו״כ passes; changing one mark of a target's qere fails with both parameter sets
   shown.

## Wave 3. Phonetic MAM: retire the legacy display comparison

Decision 3 (retire it). One commit. Product reach: `Phonetic-MAM/` is distributed data, and only
its README's text changes; no generated output changes.

1. **Delete** `in/phonetic_mam_legacy_projection_sha256.json`,
   `in/phonetic_mam_legacy_projection_inputs.json` and `py/phonetic_mam/projection_check.py`
   (only `py/main_phonetic_mam.py` and that test use it). The test
   `test_complete_release_and_unified_projection`
   (`py/tests/test_phonetic_display_release.py:18-37`) keeps `release.validate_complete_release()`
   and `display_corrections.read()`; `py/main_phonetic_mam.py check` (`:51-56`) keeps the release
   validation and drops `report_chapters_left`.
2. **Keep `in/phonetic_mam_display_corrections.json` unchanged.** The exporter applies its
   `marker_labels` (`py/phonetic_mam/exporter.py:258`, `display_projection.py:190-205`, each
   correction checked against the label it was made for), and its `chapters` map records Ben's
   approval of each corrected chapter. Remove only the code that used that map to excuse a chapter
   from the comparison (`corrected_chapters`) and keep `display_corrections`'s shape validation.
3. **The page-count pin.** `test_unified_site_controls_and_public_output_boundary`
   (`py/tests/test_phonetic_display_release.py:43`, `assert len(pages) == 974`) becomes set
   equality between the pages found and `{"index.html", *example_display.PAGE_NAMES}` plus, for
   each book of `release.iter_books()`, the book page and chapter pages the renderer's naming
   produces (`py/phonetic_mam/renderer.py:78-86`); this also catches stale pages, which
   `publication.render` never deletes.
4. **Texts.** `py/phonetic_mam/display_schema.py:3-8`, `py/phonetic_mam/display_corrections.py:3-7`,
   `py/main_phonetic_mam.py:9-10`, `:27-28`, `Phonetic-MAM/README.md` (at `3bd11204`, `:16-25`,
   "with the old pages' frozen projection hashes only while the chapter's MAM-parsed input matches
   its fingerprint"; `:104`, "chapters that have left the legacy projection comparison"; `:131`,
   "tracked at `in/phonetic_mam_legacy_projection_sha256.json`"),
   `doc/phonetic-mam-preparation.md:21-31` (say that the frozen hashes and their input record were
   retired on the execution date by Ben's decision of 2026-10-07, and that `c17de175` and this
   wave's parent hold their last copies), and `py/tests/test_mega_coverage.py:176` if it names the
   comparison. Wave 7 removes the refresh reference's item.
5. **Verify.**

   ```powershell
   ./.venv/Scripts/python.exe py/main_test.py py/tests/test_phonetic_display_release.py py/tests/test_entry_point_subcommands.py py/tests/test_mega_coverage.py
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_phonetic_mam.py check
   ```

## Wave 4. Yeivin ITM: hashes out, Ben's quoted forms checked

Dispositions 9 and 10, decisions 3 and 7. Product reach: `Yeivin-ITM/` is distributed data; its
claim file moves to a v2 schema. The 17 pages under `gh-pages/yeivin-itm/` stay byte-identical.

1. **Remove the claim-population hash.** `py/yeivin_itm/claim_schema.py`: the module docstring
   (`:1-6`), the comment and `APPROVED_POPULATION_SHA256` (`:13-20`) and `pin_population`
   (`:113-116`); the 20 `APPROVED_FRACTIONS` and `pin_claims` stay, as Ben's approval of his
   published numbers. `py/yeivin_itm/claims.py`: the call at `:41`, the docstrings at `:38` and
   `:46-50`, the second return value at `:60` and `population_sha256` (`:63-77`).
   `py/yeivin_itm/publication.py`: `:69`, `:74`, `:76-80`. `py/main_yeivin_itm.py:10-12`.
2. **Remove the recorded input hashes.**
   - `py/accgram/meteg_before_stress.py`: the `input` block (`:409`, `:432-443`, with the parameter
     at `:369` and `:449` and the import at `:26`), about 163 lines of
     `out/accgram/meteg-before-stress.json`; remove "input" from the key set in
     `py/tests/test_meteg_before_stress.py:89-96`. A Phonetic-MAM change that moves no meteg case
     then leaves the file unchanged.
   - `Yeivin-ITM/meteg-claims.json`'s `input.sha256` (`py/yeivin_itm/claims.py:57`, `:270`): the
     claim file keeps `input.identity`, the constant path of the analysis file, and loses `sha256`.
     That needs a v2 schema: a new schema file beside `meteg-claims-v1.schema.json` with its own
     `$id`, the schema string `yeivin-meteg-claims-v2` (`claim_schema.py:10`, `claims.py:269`), the
     allowlist in `claims.read` (`claims.py:19-24`), `_keys(claims["input"], ...)` and its regex
     (`claim_schema.py:63-71`), and the tests that name the v1 schema
     (`py/tests/test_yeivin_itm.py:158-165`, `:161`; `py/tests/test_meteg_before_stress.py:256`).
     Remove the v1 schema file only if nothing else names it; its README passage says which file a
     reader should use.
3. **Add the quoted-form check.** The two footnote modules of `source_lint.FOOTNOTE_MODULES`
   (`py/yeivin_itm/source_lint.py:7-10`) quote 13 forms by hand, each with a category that the
   analysis computes. (The other located citations on the 17 pages quote Yeivin's manuscript
   readings or partial atoms and claim no category from the analysis; like §385's list of
   exceptions and the ketiv notes, they stay unchecked, as today.)
   - New module `py/yeivin_itm/quoted_forms.py`: a frozen `QuotedForm(module, sloc, form, pattern,
     member_of, not_member_of=(), enumerates=None)` and a tuple `QUOTED_FORMS` of the 13, each form
     copied from its footnote module by script, never retyped. At import it rejects a measurement
     name that `APPROVED_FRACTIONS` lacks and an empty table. The two Psalms citations of §320
     (Ps 2:2 and Ps 137:1) carry
     `enumerates="fully-regular.disjunctive-without-target-meteg.merkha-with-azla-legarmeh"`: the
     footnote's hand-written list beside that measurement's generated count, "two".
   - `claims.py`: factor the population selections out of `compute`, so one ordered list feeds the
     claim file and the check; add `quoted_form_failures(survey)`, which requires exactly one
     ordinary record at each citation's verse whose `hebrew` equals the form, and checks its
     `pattern`, its membership in `member_of` and not in `not_member_of`, and, for each
     `enumerates`, that the table's declared (verse, form) set equals the measurement's numerator
     records exactly. Compare both sides through `uni_denorm.give_std_mark_order`; read the
     analysis record's gray maqaf `~` (`hebrew_punctuation.py:13`, `NU_GMAQ`) as U+05BE, since
     Ps 137:1's footnote quotes an ordinary maqaf there; keep the paseq glyph. `projection()`
     returns `(result, failures)`; `from_analysis()` raises on a failure, where `pin_population`
     raised (the mega step `yeivin-itm-survey-meteg-claims`, `survey-meteg-claims`, `check`, and
     the tests at `test_yeivin_itm.py:180` and `test_meteg_before_stress.py:254`). Not in the render
     step: `claims.read` must keep working "without reading the analysis" (`claims.py:18`).
   - `source_lint.check()`: the multiset of `hlp.hboloc(...)` calls in `FOOTNOTE_MODULES` equals
     `QUOTED_FORMS` (resolve `sub.FK_6_22[i]` by literal evaluation of `substitutions.py:955`), and
     any other located helper in those modules (`lhbo`, `some_hi`, `lns`, `hbo_loc_ms`,
     `sub.irrelevant_ketiv`) raises.
4. **`review-claims`** prints each changed fraction pin (`publication.py:81-87`), one line per
   failing quoted form (module, reference, form, failure, and the records now at that verse when
   the form is missing), an enumerated measurement's set mismatch, and the page-line diff;
   otherwise "No approved pin, quoted form or page line would change."
5. **Texts.** `Yeivin-ITM/README.md:62-69`, `:75-82`, `:89-98`, `:128-129`; `DATA-LICENSES.md:51`
   stays true, since `input.identity` stays; `py/tests/test_mega_coverage.py:170-175`.
6. **Verify.**

   ```powershell
   ./.venv/Scripts/python.exe py/main_yeivin_itm.py check
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_yeivin_itm.py review-claims
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_test.py py/tests/test_yeivin_itm.py py/tests/test_meteg_before_stress.py
   ```

   Then run the mega's steps from `accgram-survey-meteg-before-stress` through `yeivin-itm-render`
   and read the diffs: the analysis file loses its `input` block, the claim file its `sha256` and
   its schema string; nothing else under `Yeivin-ITM/`, `gh-pages/yeivin-itm/` or `out/accgram/`
   changes. The new check's focused evidence: at `HEAD` all 13 forms hold and the lint finds 13;
   in memory, Ps 137:1's form changed fails the check.

## Wave 5. Test pins of selected verses: the rule each encodes, or deletion

Accepted disposition: replace each test that pins selected verses with the rule it encodes, or
delete it. Every replacement below was prototyped read-only at `08fcae33` and passes there. No
commit or `doc/` record shows Ben asking for any of these pins.

1. **`py/tests/test_meteg_before_stress.py`.** `:220` requires the disagreements to equal 18
   declared verse-keyed rows (`:38-57`). The rule, from the test's own comment (`:34-37`): a chanted
   word whose scanner tokens include the bang pair that a dexi and its stress helper make is
   disjunctive. Define `_DEXI_WITH_HELPER = poetic_scanner._bang_pair_token(am.DEXI + am.DEXI)[0]`
   (importing `accent_marks as am`), count a word with that token as disjunctive, assert no
   disagreement, delete the 18 rows and reword `:34-37`.
2. **`py/tests/test_decalogue_m_trad.py` and the vendored capture** (decision 3).
   - Delete `EXPECTED` (`:44-53`) and its test (`:94-100`); set
     `STRAND_KEYS = tuple((b, r) for b in dmt.BOOKS for r in dmt.READINGS)`.
   - Replace `:132-133` and `:145-147` with one parametrized test of the rule that each call
     `{{כו"ק|K|Q}}` reads as Q and each call `{{מ:קמץ|ד=X|ס=Y}}` as X in both readers, taking
     K, Q, X and Y from `faithful_chanted_verses` by regular expression.
   - Delete `:160-163`: "Text outside any מ:כפול is shared by both strands"
     (`py/accgram/decalogue_m_trad.py:20-21`) holds by construction.
   - Keep `:83` and `:90`, a differential between two separately edited pages.
   - Move every reader of `in/accgram/printed_decalogue_teamim.json` to the mirror
     `in/mam-ws-special/decalogue-base.mediawiki` (the same page at the same revision 3025606):
     `py/accgram/printed_decalogue.py`'s `default_source_path()` points at the mirror and
     `load_source()` verifies the mirror's SHA-256 against its manifest record and returns
     `printed_decalogue_fetch.build_payload(text, {source_page, url, pageid, oldid,
     revision_timestamp})` from that record. Delete the JSON file, the network half of
     `printed_decalogue_fetch` (`_fetch`, `fetch_wikitext_and_revision`, `run`, `add_args`,
     `default_out_path`), the `vendor-printed-decalogue` subcommand (`py/main_accgram.py:262`,
     `:524-532`) and `DATA-LICENSES.md:80` (its row 65 covers the mirror); update
     `py/main_0_mega.py:474` and every docstring that says "vendored". Expected diff: one
     `resolution_notes` line of `out/accgram/printed-decalogue/_printed_decalogue.json`, whose
     citation of wlc-utils issue 74 gains its repository prefix, as the current code writes it;
     no page.
3. **`py/tests/test_dual_cant_detangle.py`.** `:62-63`: each strand has one chanted verse per sof
   pasuq, over all three passages. `:71-82`: `assert keyed == set(supplied_marks._CASE_IMAGE)` and
   `assert len(keyed) == len(supplies)`. Delete `:96-100`, `:141` and `:190-202`, and lint instead
   that every `href="<page>.html#<fragment>"` in the rendered supplied-marks page resolves to an
   `id` in the tracked target page. Keep `:171`. `:214-226`: `len(supplies)` for the literal 5 and
   `set(clc_render._SUPPLIED_MARKS_ANCHOR.values()) <= ids` for the anchor literals. Rewrite the
   docstring's "this test is now their record" (`:10-19`) to name the tracked outputs.
4. **`py/tests/test_mam_simple_dualcant_loader.py`** (`:58-94`): replace with (a) over every verse
   of Genesis, Exodus and Deuteronomy, a verse without a `cant-all-three` span has
   `alef == bet == vels` and a verse with one has `alef != bet` with equal letters, asserting that
   spans exist; and (b) each Decalogue strand from MAM-simple over the ranges in
   `prose_filter._BHS_RANGE_EXCLUSIONS`, joined without whitespace, equals
   `dmt.from_mam_plus(...)` after `give_std_mark_order`.
5. **`py/tests/test_versification_and_cantillation_doc.py`.** Replace `:62-67` and `:77-81` with:
   for every Exodus, Numbers or Deuteronomy verse holding a מ:כפול unit, every `_strand_words` token
   in both strands has a non-empty `_skel` (do not widen it to whole books, where a top-level נוסח
   projection still awaits Ben's decision in
   `doc/PLAN-deferred-template-projection-decisions.md` §7). `:106` becomes `assertTrue(columns)`;
   delete `:115-127`.
6. **`py/tests/test_phonetic_untangler_preparation.py`** (`:29-37`): delete the test,
   `_collect_shapes` and the unused import; the closed dispatch over shapes already runs over every
   book (`py/phonetic_mam/core/dualcant_templates.py:61-65`). Reword that module's `:11` ("These
   are the current EP shapes") to say that any other shape raises.
7. **`py/tests/test_ws_bot_sigil_b2_to_t451.py`**: delete `:152-170`, `:172-183`,
   `_daniel_chapters` and the unused imports, and rewrite the docstring (`:8-24`); the synthetic
   payload tests stay (the `AGENTS.md` `ws_bot` exception).
8. **`py/tests/test_sigil_b2_not_a_sigil_anywhere.py`**: list files with
   `git ls-files -z -- in/mam-ws` split on NUL; remove the `except UnicodeDecodeError: continue`
   (`:69-72`); assert the list is non-empty; delete `_MIN_ALIYAH_PARAMS` and its test.
9. **`py/tests/test_h_dot_below_nfc.py`** (`:174-209`): add `"in/mam-ws-special/"` beside
   `"in/mam-ws-bot-edits/"` with the comment "Byte-verbatim captures that downloads rewrite;
   AGENTS.md: never repair them", and exclude `in/mam-ws-intro/manifest.json`, each
   `in/mam-ws-intro/<slug>.mediawiki` that manifest lists, and
   `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki`. None holds a decomposed cluster today.

Verify each item with its own test file through `py/main_test.py`; item 2 also reruns the
printed-Decalogue generators and reads their diffs.

## Wave 6. Statement checks, unchecked figures and render-tag reports

Accepted disposition: keep every statement check, but where one freezes an exact count, list or
population that its prose does not state, rewrite it to test the statement; generate or check the
hand-typed figures. The model is `py/author_site/post_stress_meteg_validation.py`'s
`_check_survey_consistency` (`:65-66`), which reconciles "computed summaries without freezing their
current populations". Measured at `08fcae33` as testing exactly what their prose states, and kept
as they are: 34 of the 48 MAM-parsed claim verifiers; the accgram checks at
`maqaf_nonfinal_accents_page.py:1266-1308`, `:1333-1335`, `:1366-1377`,
`maqaf_nonfinal_accents.py:1050-1055`, `wlc_chanted_word_residue_page.py:361-369`, `:406-415`,
`printed_decalogue_koren_page.py:619-625`, `supplied_marks.py:268-272`, `rtms_report.py:189-196`;
the post-stress-meteg checks other than those item 3 names; every check in
`py/accgram/chanted_word_accents.py`; Holman's per-row word checks and exception tables.

1. **MAM-parsed's C-column claim.** The prose (`py/author_misc/mp_body_shared.py:314`, `:327`) says
   `__` is "by far the most common value" and that other common values are calls to ר4, פפ and סס;
   the check (`py/verify_mp/verifiers_plus.py:110-115`, data at
   `py/author_misc/mpplus_body.py:388-389`) requires the ordered top four exactly. Test the
   statement: `__` is the most common value and outnumbers all other values together (15,184 to
   8,020 at `08fcae33`; this plan reads "by far" that way), and the next three, in any order, are
   ר4, פפ and סס. Expected diff: that verifier's cell in `doc/mp-claims.md`.
2. **Template-presence verifiers that read last run's survey.** The nine `templates.*.set`
   verifiers, `templates.note`, `all-groups-cover-all-observed` and
   `docs.common-templates.templates-in-plus-survey` read `out/tmpl-survey-plus/plus.json`
   (`py/verify_mp/survey_artifact.py:7`), which the download never rewrites and the mega rewrites
   only after `parse-ws`. Take the observed template names from the loaded corpus
   (`iter_all_template_objects` with `good_ending_plus`), after checking that the two sets agree at
   the tree current at execution. Drop the count-and-set check that `book39.fields` repeats
   (`mpplus_body.py:254-255`). Expected diff: `doc/mp-claims.md` cells only.
3. **Post-stress-meteg.** In `py/author_site/post_stress_meteg_validation.py`, drop the checks no
   page states (`:330-338`, `:477`, `:495-499`); where the page splices a value rather than stating
   it, drop the pinned value (`:435-440`, keeping `:441`'s stated count of four; `:476`; `:548`,
   `:552`); replace `:533-534` with the stated "no effect on the MAS count" (cant-alef's count
   equals cant-bet's), and `:549-550` with `py/accgram/post_stress_meteg_survey.py:558`, `:571` by
   the stated "three atoms" (each strand's difference has three atoms; cant-alef's has no U+05BD
   and cant-bet's exactly one). Add a check for the one statement nothing checks: the "MBS" label
   of 2 Chronicles 8:11 (`post_stress_meteg_appendices.py:175`) requires the compound to have a
   meteg and no `post_stress` record for "2c8:11". Delete `_LEGACY_BASELINE`
   (`py/accgram/post_stress_meteg_model.py:333-351`) and the `legacy_baseline` entry that
   `post_stress_meteg_survey.py:399-421` writes, which nothing reads and every refresh that moves a
   count rewrites. Expected diff: `out/accgram/post-stress-meteg.json` loses that entry.
4. **accgram.** `maqaf_nonfinal_accents_page.py:1322`: replace
   `set(spreaders) == inventoried | after_gaya` with what the prose (`:2134-2138`, `:2143-2150`)
   states: every cited pair and both named rows are present, and the inventoried pairs are more
   than half; update the comment at `:1880-1881`. `wlc_chanted_word_residue_page.py:371`:
   `len(telisha) == 5` becomes `len(telisha) >= 2`, since the count is spliced into the page.
5. **Hand-typed figures.** `py/accgram/maqaf_nonfinal_accents.py:1064` ("MAM-simple has the same
   116"): count MAM-simple's implicit-maqaf nodes by verse, require equality with the hits, and
   splice `len(hits)`; the docstring's "116" (`:135`, `:143`) becomes a description.
   `py/main_explicit_xataf.py:90-91`: raise on a manual override that matches no current failure.
   MAM-parsed figures that nothing checks (`mp_cmn_rows_core.py:279` "In 2 cases (Ps 70, 108)",
   `mp_cmn_rows_other.py:66` "10 cases" and `:90` "8 shirah", `mp_cmn_groups_misc.py:31` "each of
   the 24 books" and `:77` "Gen 47:28", `mpplus_haarah_2.py:63` "only Deut 22:6"): splice each
   computed value where the sentence allows, otherwise add a verifier to the MAM-parsed registry.
   Expected diff: `doc/mp-claims.md` rows for new verifiers; no page change where the spliced value
   equals the typed one.
6. **Check before writing.** `py/main_verify_and_render_table.py` rewrites Holman's table JSON
   (`:101-105`) and page (`:106-115`) before raising on a failed row (`:124-136`): verify first,
   print each failing row's verse and word, and write only when every row passes. Do the same for
   `py/main_authored.py`'s MAM-parsed documentation (`:204-215`) if the documents can be generated
   in memory before the verifiers run without restructuring the generator; otherwise leave it and
   say why in the commit message.
7. **Render tags.** The dead-entry checks (`py/main_mam_with_doc.py:25-37`,
   `py/mb_xml/xml_render.py:22-35`, and `py/near_aleppo/edition.py:53-57` unless wave 2 removed
   it with `MAM_MODE`) stop a generator when MAM no longer uses a tag. Demote each to a report: a
   helper writes the sorted unused tags to
   `out/render-tags-unused/mam-with-doc.json`, `mam-simple.json` and `near-aleppo.json` through
   `file_io.json_dump_to_file_path`, so that a change appears in the refresh's diff. The handled
   tag sets stay closed (an unknown tag still raises). `py/near_aleppo/edition.py:60-103`'s
   `_EDITION_RENDER_TAGS`, an exact set "measured on 2026-09-25 … and pinned", becomes the rule its
   comment states: `set(hfrm.HT_TAC_FOR_RT_FOR_MAM_WITH_DOC) | {"near-aleppo-english",
   "near-aleppo-label"}`. Expected diff: three new files, each listing no tag if every tag is used.

Verify each item by rerunning the generators it touches and their tests, reading every tracked
diff. The render-tag item touches `mam-with-doc` and `mam-simple`, which run their check only on a
full-corpus run (`py/main_mam_with_doc.py:26`, `py/mb_xml/xml_render.py:24`): run those two
generators over the full corpus.

## Wave 7. The refresh skill and the texts that describe the old checks

`AGENTS.md` gains the sentence Ben accepted (decision 4); a statement there that this plan has made
false is corrected or removed.

1. **`dot-claude/skills/mam-wikisource-refresh/SKILL.md`.**
   - Insert the approved section "Judge every diff: the expected changes, and only them" (above,
     verbatim) between "## After a Wikisource bot run" (its last paragraph ends "says whether the
     bot saved it.") and "## Complete the dependent refresh".
   - Replace the opening paragraph's "A changed chapter refresh is committed before dependent
     regeneration" with: "The source change is committed before the mega runs, as "Judge every
     diff: the expected changes, and only them" says, and MAM change logs are committed only after
     the dependency loop returns to its final MAM-basics state."
   - In "After a Wikisource bot run", replace "Its first commit is the bot run's own record, the
     saved chapters' regenerated outputs with a new entry in `py/ws/ws_bot_edit_history.md`" and
     the rest of that sentence with: "Its first commit is the bot run's own record, rather than a
     separate `Refresh MAM from Wikisource`: the post-run download's chapters, revisions and
     reparse, with a new entry in `py/ws/ws_bot_edit_history.md`. That record is the source change
     that "Judge every diff: the expected changes, and only them" commits before the mega runs; the
     mega's products follow in commits of their own."
   - Replace "Any unexplained diff, failed gate, stale input, changed recorded `HEAD`, or ambiguous
     ownership stops the workflow before pushing;" with "Any unexplained diff, unresolved failed
     check, stale input, changed recorded `HEAD`, or ambiguous ownership stops the workflow before
     pushing; a check that awaits Ben's approval holds only the push;".
2. **`dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md`.**
   - Step 1 ("**Commit the public refresh locally.**", `:27-39`) becomes "**Commit the source
     change, then run the public mega.**": commit the source change (`Refresh MAM from Wikisource`,
     or the saving bot run's own record), which also takes every change the download made under
     `in/mam-ws-special/`, as a bot run's record does; write the prediction, reading the change
     with `py/main_diff.py mpplus --old <starting HEAD> --new HEAD --output <absolute .html path in
     a scratch directory>` (a bare filename raises, and the report covers only MAM-parsed plus, so
     predict special-page and revision-metadata changes from `git diff`); run the mega; judge every
     diff against the prediction; commit the explained products as `Regenerate MAM products from the
     Wikisource refresh`, with the prediction and its confirmation in the message. The mega's
     `diff-mpplus` step rewrites `gh-pages/MAM-with-doc/change-log/` from committed `HEAD`, which
     now holds the source change: after the product commit, restore those paths
     (`git restore -- gh-pages/MAM-with-doc/change-log/`) so that the public checkout is clean for
     steps 2 and 3, as it is today; step 4's mega rewrites them and step 5 commits them. Between
     the source commit and step 5, `py/tests/test_diff_mpplus_unpinned_latest.py` and
     `py/tests/test_mpplus_alternative_oracle.py` fail by design.
   - Steps 3 and 4: "Audit every diff" becomes "Judge every diff"; step 4 judges against step 1's
     prediction.
   - The section "Gates that a text change can trip" (`:106-149`) becomes "Checks that a text change
     can trip", opening: "A refresh is judged by its diffs, as `SKILL.md`'s "Judge every diff: the
     expected changes, and only them" says. These checks remain, and a refresh that changes MAM's
     text can trip each of them. Approval of the refresh approves nothing that they protect." Then:
     1. **Closed dispatch.** A parser, renderer, survey or build raises on a template or shape that
        it does not recognize. Stop: the repair is code, a new case in the named dispatch whose
        semantics come from an existing explicit policy or from Ben. If the download's parse stops
        at `py/ws/ws_get_bk_in_fmt_2.py`'s header or category assertion, a chapter page no longer
        names the chapter it was fetched as: inspect the page, then record a deliberate layout
        change in a reviewed commit of its own, or report the page on Wikisource and download again
        once it is fixed; commit nothing from the stopped run.
     2. **The two grammar locks**, closed dispatch over template nesting: the parser-stage lock
        (`py/verify_mp/expanded_stack_grammar_parser_stage.lock.json`, Ben, 2026-09-30) and the
        plus-survey lock (`py/tmpl_survey/expanded_stack_grammar_plus.lock.json`, accepted
        2026-09-10). When one stops on an edge: read the edge and its example stack from the error
        (for the plus lock, `--find-stack-path <stack>` lists where it occurs); decide whether the
        nesting is legitimate MAM markup that every dispatcher handles; if it is, rewrite that lock
        with `./.venv/Scripts/python.exe py/main_parse.py ws --write-parser-stage-grammar-lock` or
        `./.venv/Scripts/python.exe py/main_tmpl_survey.py --write-expanded-stack-grammar-lock`,
        confirm that the lock's diff adds only that edge, commit it on its own with the reason, and
        rerun; if it is not, report the page on Wikisource.
     3. **Statement checks**: the MAM-parsed claims that `doc/mp-claims.md` indexes, the
        accgram and post-stress-meteg page checks, Holman's table, and the like. Repair the
        statement, or the derived record and what it records, in one reviewable edit, naming in the
        commit message the change in MAM's text that made it false.
     4. **Ben's published claims wait for him.** (a) The Yeivin fraction pins and quoted forms: if
        the mega stops at `yeivin-itm-survey-meteg-claims`, leave `claim_schema.py`,
        `quoted_forms.py`, the footnote modules, `Yeivin-ITM/meteg-claims.json` and
        `gh-pages/yeivin-itm/` unchanged, give Ben `py/main_yeivin_itm.py review-claims`'s report,
        and finish the refresh locally with
        `./.venv/Scripts/python.exe py/main_0_mega.py --resume-from yeivin-itm-render`; until he
        approves new pins or footnote edits in his own message, `check` and four Yeivin tests fail
        and nothing is pushed; with his approval, change only what he approved, rerun with
        `--resume-from yeivin-itm-survey-meteg-claims`, and commit those changes on their own,
        quoting his approval. (b) Near-Aleppo's stored pointed ketivs (Ben, 2026-10-07): when the
        build stops because a target's ketiv or qere differs from its record, ask Ben, giving the
        verse, the recorded and current ketiv and qere, the stored pointed ketiv, and the Aleppo
        Codex links that the `verse-links` skill produces. Do not write a new pointed ketiv
        yourself. After his decision, change the record's value and parameters as he says, in a
        commit of their own quoting him, and resume from `near-aleppo-build`.
   - Remove the item "**The legacy display projection.**" (wave 3 retired it) and update the
     citations of the old section title at `:36-37`, `:71-72` and
     `py/tests/test_mega_coverage.py:171-174`.
   - "Required scenario behavior": item 6 becomes "A moved Yeivin fraction, a broken quoted form in
     Ben's footnotes, or a changed ketiv or qere at a stored near-Aleppo pointed ketiv waits for
     Ben's approval before the push; the rest of the refresh proceeds." Add item 7: "A failed
     statement check on a record that is not Ben's published claim is repaired, with what it
     records, in one reviewable edit, and the refresh continues."
3. **`py/ws/pywikibot-setup.md`** (`:63-65`, "the public mega and Phonetic-MAM release"): the
   dependent refresh now begins with the source commit.
4. **`AGENTS.md`** (decision 4): in "What this repository's products are, and which check a change
   owes", add as its own paragraph, after "Product reach and whether an act is hard to undo are
   separate risk axes, as the user-level instructions explain.":

   > A product derived from MAM's text takes each Wikisource refresh through the
   > `mam-wikisource-refresh` runbook's judgment of every diff, so it gets no hashes, fingerprints
   > or pinned populations of its inputs. A deterministic check is closed dispatch, or it tests
   > that a hand-made statement about the data still holds and covers exactly what that statement
   > depends on: a stored pointed ketiv's check covers its ketiv and its whole qere, letters and
   > every mark, and not its template's name.
5. **Verify:** `git diff --check`, and `py/main_test.py` on `test_mega_coverage`,
   `test_receipt_update_links` and `test_prose_mark_order`. After the push, deploy the skill (wave
   8).

## Wave 8. Deployment and record

1. The nightly run supplies the full suite and the mega (`doc/review-trial.md`); its failures go
   through that run's triage. A broad check runs at once only for a stated consequence that
   cannot wait for it.
2. Deploy the changed canonical skill from the full clone, after the push of wave 7, then compare:

   ```powershell
   ./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
   ```

   ```powershell
   ./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
   ```

   The deployment fetches `origin` and installs only from `refs/remotes/origin/main`
   (`dot-claude/README.md:70-93`); it writes outside the repository, into both live skill homes,
   and redeploying from `origin` reverses it.
3. Set this plan's State to `executed <date>` in the commit of the last wave's work, with the
   ledger below reconciled.

## Expected unchanged outputs

Unless a wave names it: `MAM-parsed/`, `MAM-simple/`, `MAM-with-doc/`, `Phonetic-MAM/data/`,
`out/near-aleppo/plus/`, `gh-pages/` (except `gh-pages/near-aleppo/editorial-policies.html` in
wave 2), `Yeivin-ITM/` (except the claim file's `input.sha256`, schema string and schema file in
wave 4), and every other generated file. Any other diff is a finding.

## Requirement ledger

| Id | Requirement | Wave | Status |
|---|---|---|---|
| R1 | Ledger loses its whole-file hashes; per-note evidence stays | 1 | implemented |
| R2 | Census provenance and uncommitted-input refusal go; census agrees with build | 1 | implemented |
| R3 | The build writes the population file | 1 | implemented |
| R4 | Named-site statements replace population pins | 1 | implemented |
| R5 | Verse-count pin goes; book set becomes closed dispatch | 1 | implemented |
| R6 | Mega near-Aleppo steps and their texts | 1 | implemented |
| R7 | Readable pointing records; digests and manifest constants go | 2 | implemented |
| R8 | Genesis 43:28 and consumer-notice hashes become readable | 2 | implemented |
| R9 | Near-Aleppo's two checks over old commits are retired | 2 | implemented |
| R10 | Phonetic MAM legacy comparison retired; page set replaces the 974 pin | 3 | implemented |
| R11 | Yeivin population hash goes; quoted-form check added | 4 | active |
| R12 | Recorded input hashes go (analysis file, claim file v2) | 4 | active |
| R13 | Test pins replaced by rules or deleted | 5 | active |
| R14 | Every reader of the Decalogue capture moves to the mirror | 5 | active |
| R15 | Statement checks, figures, check-before-write, render-tag reports | 6 | active |
| R16 | Refresh skill and reference rewritten | 7 | active |
| R17 | Skill deployment and this plan's record | 8 | active |
| R18 | `AGENTS.md` sentence, accepted by Ben on 2026-10-07 | 7 | active |

## Noticed, not acted on

1. **2 Kings 14:7** is outside this plan (Coordination, item 1).
2. **Fixed after this plan was first pushed:** `AGENTS.md`'s products section ended with the false
   "MAM-private runs its own near-Aleppo census", and `py/main_0_mega.py`'s docstring said
   "MAM-private's own mega runs the census now", though near-Aleppo's census has run in this
   repository since 2026-10-05. The commit that recorded Ben's clarification of decision 4
   removed the first and corrected the second.
