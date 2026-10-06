# Updates to the 2026-10-04 review of MAM-basics

State: open; first entries 2026-10-05.

Every entry here corrects or supplements `doc/review-findings-2026-10-04.md`, which is left as
written apart from its line-4 pointer to this file.

## The fixes that needed no decision, and every item's disposition, 2026-10-05

Recorded on 2026-10-05, New York time, by a Claude session (Claude Opus 5.5 in the Claude desktop
app) working in the full clone `C:/Users/BenDe/GitRepos/MAM-basics` on `main`, from `eacb3312`, the
commit that added the review.

**Ben's instruction.** The session that wrote the review records Ben's instruction to it, on
2026-10-05, as: "Can some fixes be made without answering questions? If so, please give a prompt
for a session that will do those fixes." That session wrote such a prompt, naming the items it
judged to need no decision and the items it left for Ben, and Ben opened this session with it. This
session re-measured each item on the current tree before changing it. An item that turned out to
admit more than one reasonable fix, or to need wording beyond the correction itself in text Ben
approved, was to be left for him with the reason; none of the items the prompt named as fixes
turned out so, though item 9.11's correction differs from the wording the prompt presumed, as its
entry explains.

**How each disposition was established.** "Fixed" is written only after the item's own measurement
was re-run on the changed tree; each fix's commit message records that evidence. A replay that
needed code ran from the ignored `.novc/` scratch directory, and no example-based test was added.
Two read-only sub-agents re-measured the figures behind items 4.1 and 9.11 and the record facts
behind items 9.17 and 9.28 to 9.33; their results were re-read before use, as each entry says.
Nothing in MAM-private, hbofonts or `bdenckla/trope` was read; the mega reads MAM-private through
tracked code.

**Commits.** Finding 1.1's fix went to `origin/main` alone, as `ba5bf456`. The rest followed:
`4a5a12c5` (checks), `f8a05c70` (Phonetic MAM tools), `b100ae79` (Book of Job), `14981cc8`
(published pages), `04bca43e` (reader-facing documents), `3ad2ada2` (maintained documents,
docstrings, skills and attributes), `59816fe9` (Phonetic MAM's departures), `2aca5816` (the
survey's paseq comments) and `f1a8189e` (records); `379f046a` merged the `origin/main` that had
moved meanwhile, and went to `origin` with them; then the commit that adds this entry.

### Finding 1: the change log and the narpas label

1. **1.1 Fixed in `ba5bf456`, pushed alone.** `./.venv/Scripts/python.exe py/main_diff.py mpplus
   --all` rewrote only `gh-pages/MAM-with-doc/change-log/unpinned-latest.json` and `.html`, on three
   lines in all, each now `f5b2c69f61d2ef48af855ae39c3db560977ad73a`, the value of
   `git rev-parse HEAD:MAM-parsed/plus`. `test_registered_outputs_match_real_regeneration` passes,
   and the full suite passed with 1,048 passed, 5 skipped and 60 subtests passed. The commit's
   message records the judged skip of the mega: the review's mega run at `139e2d63` had left this
   same diff and no other. Ben's later notice change moved the tree id again, and his `d8435412`
   refreshed the two files to match; the test passes on the merged tree, and the two megas below
   left them unchanged.
2. **1.2 Fixed for MAM-parsed in `04bca43e`; awaiting Ben's decision for MAM-simple.**
   `MAM-parsed/README.md` now says "(narrow-sense paseq, מ:פסק)", as the shared notice does.
   `MAM-simple/README.md:44` keeps the glyph until question 1.3 is answered.
3. **1.3 Awaiting Ben's decision:** whether MAM-simple's notices, reading guides and README should
   name MAM-simple's own `lp-paseq` rather than the template `מ:פסק`, which MAM-simple does not
   contain.
4. **1.4 Already resolved; no change.** The review's own runs of `py/main_mam4sef.py`, both halves,
   and `py/main_mam_osis.py` on the extracted start and end trees showed no product change; the
   lapse was one of procedure.

### Finding 2: `DATA-LICENSES.md`'s CC0 row and WLC/UXLC credit

**Awaiting Ben's decision, both items.** Each changes licence and attribution wording, an
editorial proposal under D7 (`doc/periodic-review.md`, "Separate defects from editorial
proposals").

### Finding 3: public files that carry private-repository material

**Awaiting Ben's decision, all five items,** pending his answer on which governs: the 2026-08-27
rule in `in/repo_maintenance_policy.json`'s `repo_visibility` comment, or the governing document
inside MAM-private that the same file's `MAM-private` entry names, which a public-only session
cannot read. Item 3.5 is itself that question.

### Finding 4: Phonetic MAM's documents and two Decalogue verses

1. **4.1 Fixed in `59816fe9`, apart from its question.** `Phonetic-MAM/README.md` keeps its six
   departures as they were and adds two as items 7 and 8: the release's book files have none of
   MAM's rafe, U+05BF, which `MAM-simple/` has; and at a `kq` pair the release has only the qere,
   apart from item 6's verse, and none of the 8 ketivs that MAM writes but does not read.
   Re-measured here by a generic walk of the JSON: 0 U+05BF in the 39 book files, 3 in
   `examples/display.json`, at two atoms, which is why the item speaks of the book files, and 94 in
   `MAM-simple/json-vtrad-mam/`; 1,047 `kq` and 8 `kq-k-velo-q` elements. A read-only sub-agent
   compared every verse's consonant skeleton with MAM-simple's under each branch choice, by two
   independent methods: the release has the qere at 1,046 `kq` pairs and the ketiv's letters only
   at 2 Chronicles 25:17, and none of the 8 unread ketivs; a spot check of six Genesis pairs here
   agrees. The review's figure of 84 rafe at 84 chanted words holds when one cantillation strand is
   chosen; the README gives no count. **Awaiting Ben's decision:** the item's question, whether the
   release's lack of MAM-simple's 9 inverted nuns is a third departure that the README owes.
2. **4.2 Fixed in `04bca43e`.** `Phonetic-MAM/README.md` and the refresh procedure
   (`dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md`) now say that a
   change to a chapter's first or last verse also makes the chapter before or after it leave the
   comparison, and the procedure accepts that neighbour among the listed chapters. Re-measured on a
   scratch copy of `MAM-parsed/plus` against the tracked input record: a change to Ruth 2:1 or to
   Ruth 1:22 makes Ruth 1 and Ruth 2 leave, and a change to Ruth 2:10 makes Ruth 2 alone leave.
3. **4.3 Fixed in `04bca43e`.** The README's command list and the `check` subcommand's help now name
   the listing of chapters that have left the legacy projection comparison, in the module
   docstring's words; `py/main_phonetic_mam.py --help` prints it.
4. **4.4 Awaiting Ben's decision:** what a refresh does when every chapter has left the comparison.
5. **4.5 Awaiting Ben's decision; latent:** whether the exporter's time limit must also bound a
   child of the adapter that holds its stderr. Public code cannot show whether the private adapter
   starts one.
6. **4.6 Awaiting Ben's decision:** whether the README's list of departures should name the two
   Decalogue verses whose narrow-sense paseqs the release has in both strands, and whether the
   display contract should be able to say which strand a marker belongs to.
7. **4.7 Awaiting Ben's decision:** whether the legacy projection's freeze is intended, and what
   path past it a deliberate display correction takes.

### Finding 5: texts that `AGENTS.md`'s new push rule left behind

1. **5.1 Fixed in `3ad2ada2`.** The live plan
   `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md` no longer prescribes the
   removed exemption: "Apply the current content-based verification exemption and full-suite
   cadence; Markdown-only work owes no full suite or mega" now reads "Apply `AGENTS.md`'s current
   rule for when a push of `main` runs the mega and the suite, and the full-suite cadence", and "A
   linked worktree receives the repository's mandatory final mega unless its branch is
   content-exempt" now reads "A linked worktree's integration runs the mega and the suite as
   `AGENTS.md`'s rule for a push of `main` decides". A `git grep` for "content-exempt" and
   "content-based" now finds them only in the review that quotes them.
2. **5.2 Awaiting Ben's decision:** whether D11's final integration should run the suite or record
   a skip, which changes his approved procedure wording.
3. **5.3 Awaiting Ben's decision:** where a skip note goes when the decision follows the last
   commit pushed.
4. **5.4 Awaiting Ben's decision:** `py/product_scopes.py`'s "does not restate" beside its restated
   hand-run rule; the remedy is either deleting the claim or the restatement.
5. **5.5 Awaiting Ben's decision:** whether a change to tracked product files is excluded from the
   judged skip.

### Finding 6: the review procedure documents

**Awaiting Ben's decision, all five items.** Items 6.1 and 6.3 are questions, and the wording of
items 6.2, 6.4 and 6.5 is his approved wording of 2026-10-03, so changing it is an editorial
proposal under D7.

### Finding 7: checks and tools that do less than they say

1. **7.1 Fixed in `4a5a12c5`.** `validate_plus_conversion` now checks each book's
   `good_ending_plus` as well as its verse cells. Replayed on Lamentations' in-memory plus: `tmpl`,
   `stmpl` and `custom_tag` injected as the whole good-ending element or into its parameter 1, six
   cases, all pass the check at `eacb3312` and all raise now; the clean plus passes both.
2. **7.2 Awaiting Ben's decision.** Closing the lint's two gaps needs either a lint that reads every
   branch of the classifier and the refusal's body, or the injection test that the approved plan
   ruled out ("No example-based injection test is added"); that is more than one reasonable fix.
3. **7.3 Fixed in `4a5a12c5`.** The pipeline-graph lint now also requires each program node to list
   every `_STEPS` step that runs its program. The current graph passes, so neither the spec nor the
   generated graph changed; a node without `mam-simple-docs` passes the lint at `eacb3312` and fails
   it now.
4. **7.4 Awaiting Ben's decision.** Making `review-claims` print its report when a word-form claim
   would reach 7, or when a denominator empties, is a choice of reporting design with more than one
   reasonable form.
5. **7.5 First half fixed in `3ad2ada2`; second half awaiting Ben's decision.**
   `doc/clone-forests.md` now says that a calling session working in a linked worktree under the
   clone also counts as that worktree's occupancy, so the write form refuses the clone; the code
   (`py/repo_util/forest_sync.py`, `_runtime`) re-read confirms it. The question, whether a dirty,
   off-`main`, mid-operation or locked clone that only the caller occupies should be skipped, as the
   code does, or refused, as `doc/clone-forests.md:38–39` and the module docstring say, stays Ben's.
6. **7.6 Awaiting Ben's decision.** A repair for a `relocation_failed` sidecar is new procedure, and
   the remedy that the code admits, deleting the sidecar, is one that
   `repository-maintenance.md` forbids.
7. **7.7 Fixed in `3ad2ada2`.** The forest launch lint's docstring now names the import forms it
   recognizes and says that a name a star import binds, and a module reached through `getattr`,
   `__import__` or `importlib`, are not recognized; re-read against `_imported_names` and
   `_call_target`.
8. **7.8 Awaiting Ben's decision.** Either the docstring's "Seven independent steps" changes or
   step 2's `RetirementError` stops ending the run; more than one reasonable fix.
9. **7.9 Fixed in `f8a05c70`.** The compute command's standard input now ends lines only at LF. By
   subprocess, four request lines, one with a bare carriage return between tokens, one
   LF-terminated, one CRLF-terminated and one unterminated, got five replies at `eacb3312`, two of
   them errors, and get four results now.
10. **7.10 Fixed in `f8a05c70`.** The test-page run reads both pipes as bytes: a failing adapter's
    non-UTF-8 stderr now shows its tail with replacement characters where `eacb3312` showed
    "(nothing)", on failure and on timeout, and non-UTF-8 stdout after exit 0 raises
    `UnicodeDecodeError` where `eacb3312` raised `TypeError`. Shown with fake adapters replacing
    `_adapter_command` in memory, nothing reaching MAM-private.
11. **7.11 Awaiting Ben's decision.** The review's census of echo routes is incomplete, and the
    remedy, whether to escape, replace or reject, chooses what a reply may echo.

### Finding 8: questions for Ben

**Awaiting Ben's decision, all ten items,** each the question its entry asks.

### Finding 9: one-line items

1. **9.1 Fixed in `b100ae79`.** Recounted with `git ls-tree`: the Book-of-Job artifact
   set has 703 files and the generator's 183 leave 520; 7 PNGs sit directly under `jobn/img/`; 517
   of `gh-pages/book-of-job/`'s 696 files are PNGs; `jobn/img/` holds 487 tracked PNGs. The four
   sites now say so.
2. **9.2 Awaiting Ben's decision:** which name the footnote's two comparison cases take.
3. **9.3 Fixed in `04bca43e`.** `DATA-LICENSES.md` names the crops' sources as facsimiles of the
   four manuscripts "and from the Jerusalem Crown edition".
4. **9.4 Awaiting Ben's decision:** licence wording, under D7.
5. **9.5 Fixed in `3ad2ada2`.** "WHAT IT CHECKS" lists the licence lint as item 4.
6. **9.6 Fixed in `3ad2ada2`.** `py/mb_cmn/paths.py` lists all seven landed products.
7. **9.7 Fixed in `3ad2ada2`.** The wlc-utils comment heads only the four lines `30f985b7` copied;
   the five binary files that had no attribute, found with `git ls-files --eol` and
   `git check-attr`, now have `binary` through four path-scoped lines, and none of their blobs
   changed (`git hash-object --path`). A re-run of the same census finds no binary file without the
   attribute.
8. **9.8 Page half fixed in `14981cc8`; README half awaiting Ben's decision.** The MAM-with-doc
   index has a period after the licence link, regenerated by `py/main_mam_with_doc.py`. The README
   half is licence wording, under D7.
9. **9.9 Fixed in `04bca43e`.** `Yeivin-ITM/README.md` lists `review-claims` and says "All four
   commands".
10. **9.10 Fixed in `04bca43e`.** The lint's docstring and the README name the references that the
    lint reads.
11. **9.11 Fixed in `2aca5816`, though not as the handoff prompt worded it.** The prompt presumed
    that the data the survey reads lacks the distinction between narrow-sense paseq and legarmeh.
    It does not. In the release, which the survey reads through
    `py/phonetic_mam/analysis_reader.py`, a legarmeh is U+05C0 inside the chanted word's Hebrew and
    a narrow-sense paseq is a row of its own labelled `מ:פסק`. In the survey's selection all 1,781
    of MAM-simple's `lp-legarmeih` match an in-word U+05C0 and all 504 `lp-paseq` match a `מ:פסק`
    row, and no legarmeh has one (a sub-agent's census; the release's 1,789 in-word U+05C0 were
    recounted here). The survey's own code loses the distinction: `_accent_grammar_tokens_by_entry`
    appends U+05C0 to the preceding chanted word for each `מ:פסק` row. The comment and the
    docstring now say so, and keep their account of the structural conversion and of MAM-simple
    supplying the category.
12. **9.12 Awaiting Ben's decision:** which name the notice's audience takes.
13. **9.13 Awaiting Ben's decision.** The two sentences are the plan's approved C7 text, so
    narrowing them is an editorial proposal under D7.
14. **9.14 Fixed in `3ad2ada2`.** The bot guide and the help say that the special pages are
    refetched only when the run changed a chapter, as `_download_modified_chapters` does.
15. **9.15 Fixed in `14981cc8`.** The mpplus guide says "a book24 that has no sub-books",
    regenerated by `py/main_authored.py gen-mam-parsed-docs` (its claims 50 passed).
16. **9.16 Fixed in `3ad2ada2`.** `doc/clone-forests.md` names the five lock files of
    `_snapshot`.
17. **9.17 Fixed in `f1a8189e`** by a dated entry appended to
    `doc/review-findings-2026-10-02-update.md`: the reason given for skipping the mega at `b246e05e`
    is false for the 11 lines whose `main()` the mega runs in process as a step's runner, which the
    entry names; the conclusion stands, since each makes the same stderr change as
    `force_utf8_io`'s.
18. **9.18 Awaiting Ben's decision:** the review asks it as a question.
19. **9.19 Fixed in `3ad2ada2`.** A write's failure line now gives only "environment drift", since
    `_sync_repo` in write mode returns False only from `synchronize_environments`.
20. **9.20 Fixed in `f8a05c70`.** The `phonetic-mam-render` record names its stylesheet and script,
    the five example images, the frozen font inputs and the shared font-sources package, checked
    against `py/phonetic_mam/publication.py` and `py/py_html/taamey_d_assets.py`.
21. **9.21 Awaiting Ben's decision:** renaming an entry point.
22. **9.22 Awaiting Ben's decision:** the replacement wording, which C15.24 put to him.
23. **9.23 Fixed in `3ad2ada2`.** The trackers reference says the routing section records one
    number collision, phonetic-hbo#78; both issues numbered 78 exist (`gh issue view`, read-only).
24. **9.24 Fixed in `f1a8189e`** by a dated entry appended to
    `holman/doc/uxlc-email-count-disagreements-update.md`: the text that the 2026-10-03 entry calls
    the sentence's "second half" is the whole second sentence of its paragraph (`cb5bcda1`'s diff).
25. **9.25 Fixed in `3ad2ada2`.** `hebrew-prose`'s `mam-basics.md` says `9a67d51b` rewrote "the
    docstrings and the one comment"; the merge's diff replaces the comment at
    `py/accgram/breuer_word_length.py:105`.
26. **9.26 Fixed in `3ad2ada2`.** The reference names `py/main_redirect_stubs.py`, through
    `source_pages_dir`, as what raises with the clone command.
27. **9.27 Fixed in `f1a8189e`, in place.** `doc/dual-agent-review.md` calls the relay software
    what Ben "then hoped to discard soon", and points to D13's record of its removal.
28. **9.28 Fixed in `f1a8189e`, in place in both files.** `doc/dual-agent-review.md` calls
    `cbd405b1` "the parent of the commit that removed them", which "holds them all", and the
    October 1 update says that it "holds every removed file": `d168e22e`, whose parent is also
    `074af13a` and which `f0c50473` merged, holds all ten as well (`git ls-tree` here).
29. **9.29 Fixed in `f1a8189e`** by a dated entry appended to the October 1 update: every cited
    path resolves at `cbd405b1`, but 303 of the round's 311 line citations into the removed files
    point at other text there; each holds where its record measured it.
30. **9.30 Fixed in `f1a8189e`, in place.** The October 1 round is the relay's "only production
    round", beside the isolated rehearsal round and two synthetic probe rounds that the runbook
    at `cbd405b1` records.
31. **9.31 Fixed in `f1a8189e`.** The turn-file lint's docstring names both checks it dropped:
    the census comparison and `lint_automated_round_headers` (read at `cbd405b1`).
32. **9.32 Fixed in `f1a8189e`, in place.** D10's item 4 preserves the October 1 round's `Next:`
    lines in a clause of their own, no longer among filenames and State lines.
33. **9.33 Fixed in `f1a8189e`, in place.** The October 1 update says that the close-out's
    evidence was retained in the development worktree until that worktree, with its `.novc`, was
    removed on 2026-10-04.
34. **9.34 Fixed in `b100ae79`.** Both alt texts say "pataḥ"; the regenerated details page and
    `book-of-job/out/enriched-quirkrecs.json` changed on those two strings alone.
35. **9.35 Fixed in `b100ae79`.** `qr-footnotes` is in `doc/boj-quirkrec-comments.md`'s list and
    among the fields that the μY-mentions page reads, and `flatten_qrs.py` flattens it: its content
    is a list of HTML elements, the shape `_flatten_yyycom` flattens, and flattening leaves it
    unchanged, so the regenerated outputs differ only by item 9.34's two alt texts.
36. **9.36 Awaiting Ben's decision.** It is reasoned for POSIX only, and a fix could not be run on
    this Windows machine.
37. **9.37 Fixed in `3ad2ada2`.** The module docstring says a candidate is refused only after an
    unpaired oleh, as `_accent_class` does.
38. **9.38 Awaiting Ben's decision:** the review asks it as a question.
39. **9.39 Awaiting Ben's decision:** the review asks it as a question.
40. **9.40 Fixed in `4a5a12c5`.** The guard also denies `io.open` and `os.open`, and the lint
    catches attribute calls. An operation wrapped in memory to call either first, and `compute.py`
    with either call appended, pass the checks at `eacb3312` and fail them now.
41. **9.41 Fixed in `04bca43e`.** `README.md` describes a solid box in the legend's words and names
    Hebrew Wikisource among the drawn stores.
42. **9.42 Awaiting Ben's decision.** Making the test able to fail on the import-cache half needs
    either a different test design or a narrower claim; more than one reasonable fix.
43. **9.43 Fixed in `14981cc8`.** Both alt texts say "Minḥat Shai", regenerated by
    `py/main_accgram.py generate-html-printed-decalogue-uvinkha`.

### The review's "Noticed outside the diff" and declared open ends

**Awaiting Ben's decision, all three noticed items.** Editing issue #296 is an outward-facing act
for him; the other two are questions. The four open ends that the review lists as the window's own
are unchanged.

### Noticed while fixing, not acted on

No item names these, so this work left them as they are.

1. Two more passages carry item 9.28's claim or item 9.33's. In
   `doc/review-findings-2026-10-02-update.md`, "Remediation implemented; final gates pending,
   2026-10-03" calls `cbd405b1` "the archive commit, the last whose tree holds every file that the
   relay's removal deleted", and `4573b007`'s commit message says the same. In
   `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`, "Remediation execution by Codex,
   2026-10-01" says "Public verification evidence is retained under this worktree's ignored
   `.novc/`", of the development worktree removed on 2026-10-04.
2. The `accgram-survey-post-stress-meteg` step record in `py/main_0_mega.py` names public
   Phonetic-MAM and MAM-simple's `json-vtrad-mam` as the survey's inputs; the survey also reads
   `MAM-parsed/plus/` (`py/accgram/post_stress_meteg_sources.py`, through
   `read_books_from_mam_parsed_plus`).
3. In `MAM-simple/json-vtrad-mam/`, 129 of the 1,047 `kq` elements list `kq-q` before `kq-k`, as at
   the first in 1 Chronicles; `MAM-simple/doc/reading-mam-simple-xml.md`, "Ketiv/Qere", names the
   two children by type and does not say that their order varies.

### Verification

1. **The suite** passed at `f1a8189e`, the last fix commit, from 16:12:40 New York time: 1,048
   passed, 5 skipped and 60 subtests passed in 354.26 s, where `139e2d63` had one failure, finding
   1.1's.
2. **The mega** ran at `f1a8189e` from 16:18:55 to 16:28:54 New York time: all 57 steps exited 0 in
   592.6 s of steps, with Graphviz the pinned 16.0.0 (20260814.1018), the claims check at 50
   passed, 0 failed and 0 pending, and the `phonetic-mam-export` step re-exporting the release
   through the private adapter in 110.6 s. It left no tracked diff and no untracked file.
3. **The merge.** A fetch before the push found `origin/main` at `d8435412`: Ben's clarification of
   the parsed-plus consumer notice (`fe85cd55`, merged by `3b529f2d`) and the refreshed change log
   (`d8435412`), whose messages record that they skipped the mega and the suite. `379f046a`
   merged them without a conflict. On the merged tree the mega ran from 16:30:17 to 16:39:59 New
   York time, all 57 steps exiting 0 in 578.0 s of steps with the claims check at 50 passed and no
   tracked diff, and the suite from 16:40:20 passed with 1,048 passed, 5 skipped and 60 subtests
   passed in 353.74 s.
4. **Hand-run generators.** No change here or in the merged commits reaches `MAM-simple/` or any
   other input of `py/main_mam4sef.py` or `py/main_mam_osis.py`: from `eacb3312` to `379f046a`,
   `git diff --stat` over `MAM-simple`, `MAM-for-Sefaria`, `MAM-OSIS`, `Phonetic-MAM/data`,
   `Phonetic-MAM/examples` and `Yeivin-ITM/meteg-claims.json` prints nothing, so neither was
   rerun. The hand-run programs that the fixes changed, `py/main_ws_bot.py` (a help string) and
   the `check` and `compute` commands of `py/main_phonetic_mam.py`, write no tracked output.
5. **Lints.** Each commit had `git diff --check`, and Black and ruff on its changed Python files.
   On the final tree `py/main_repo_util.py --check-repo-standards --repos MAM-basics` reports the
   review's figures: `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`, `HEX_ESCAPES=76`,
   `ORPHAN_MARKS=0`, `NFC_H_DOT=25` and `NFC_LATIN=72`.
6. **Push and deployment.** `main` went to `origin` as `379f046a` at 16:46:32 New York time.
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config` then deployed from
   `refs/remotes/origin/main` at `379f046a` and reported `USER_CONFIG_DEPLOYED_COUNT=8`, the four
   changed skills, `github-issues`, `hebrew-prose`, `mam-repository-topology` and
   `mam-wikisource-refresh`, in both `~/.claude/skills/` and `~/.agents/skills/`; its `--check`
   reported `USER_CONFIG_PROBLEM_COUNT=0`.

**Effective base State, 2026-10-05:** partly acted on. The items that needed no decision were fixed
and pushed to `origin/main`, at `379f046a`, on 2026-10-05, as listed above; every item marked
"awaiting Ben's decision" remains for him. The base report's line 3 stays as written. This update
remains `State: open` while its base survives.

## A noticed item withdrawn: the qere-first order is MAM's own, 2026-10-05

Recorded by Claude Opus 5.5 on 2026-10-05, New York time, in the session that wrote the entry
above. **Withdrawn: item 3 of that entry's "Noticed while fixing, not acted on" reports no
defect.** Ben asked of it the same day: "Who said that's an error? Trace back to the source
templates and I think you'll see that a separate template is used for that ordering, which for
those particular words is viewed as better than the standard k-then-q ordering."

Traced: the 1,047 `kq` elements of `MAM-simple/json-vtrad-mam/` correspond, verse by verse and in
order, to the 1,047 ketiv/qere templates in the E column of `MAM-parsed/plus/`: 884 `כו״ק`, 126
`קו״כ` and 37 `מ:כו״ק מיוחד`. The 129 elements that list `kq-q` first are the 126 `קו״כ` and the
three `מ:כו״ק מיוחד` whose `סוג` names a qere-first type: at 2 Kings 18:27 and Isaiah 36:12,
`קו"כ קרי שונה מהכתיב בשתי מילים`, and at Nehemiah 2:13, `קו"כ כתיב מילה חדה וקרי תרתין מילין`.
`py/mb_cmn/template_names.py` records that `קו״כ`'s arguments are in ketiv/qere order but are
rendered qere first, and `py/render_wt/render_wikitext_kq.py`'s `_PUT_KETIV_1ST` carries that order
into MAM-simple. So the order is MAM's choice of template for those words, which by Ben's account
is viewed as better there than the standard ketiv-then-qere order. The item repeated a read-only
sub-agent's reading, that a consumer relying on the children's position would swap them, without
this trace.
