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

## Ben's decisions on the open items, 2026-10-06

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-06, New York
time, in the full clone `C:/Users/BenDe/GitRepos/MAM-basics` on `main`, from `97fbec01`.

**Ben's instruction.** Ben opened this session with a prompt that the session of the two entries
above wrote at his request. That session records his instruction to it, on 2026-10-05, as: "Give
me a prompt for a session that will walk me through all the needed decisions that are needed to
proceed with acting on the findings of the review". This entry is close-out step 1 of
`doc/periodic-review.md` for every item that the first entry above marks "Awaiting Ben's
decision".

**How the decisions were taken.** The first four batches were put to Ben in the app's dialogs, in
order of public-facing risk. The option wording is this session's; Ben's part is the selection,
quoted below by the selected option's label, with any words he added. Where an option changes
wording a reader sees, the entry gives the text that the option proposed, which is the text Ben
selected. This session or one of three read-only sub-agents re-read every passage that each item
cites on the tree at `97fbec01`, and none had gone stale or been resolved; items whose files Ben's
commits of 2026-10-05 and 2026-10-06 later changed were re-read again, as their entries say.
Every fix goes to the remediation phase, the fresh-task plan of close-out step 2, unless an item
says otherwise, and nothing was implemented here.

**Ben's instruction for the rest.** Four batches of dialogs settled 16 items: 1.3, 2.1 and 2.2,
finding 4's open items, and the reader-facing items 8.1, 8.3 to 8.6, 9.2, 9.4 and the README half
of 9.8. Ben then wrote: "I had little or no idea what I was agreeing to but I don't really care.
This was not what I had in mind with "walking me through" these decisions. You always provide
either too much or too little information. In this case too little." After this session set out
item 8.1 in full, he changed that item in his own words, recorded under finding 8. Asked how to
present the remaining 40 items, and whether to keep the earlier selections with his remark
recorded, he wrote: "Is this all documentation? Just do what you recommend. I don't have time for
any of this and it feels low stakes. I need this review to end". As this session had recommended,
the 16 selections therefore stand as he made them, his remark recorded here, but they are not
considered approvals of each wording: the remediation plan puts each wording to him again. Every
disposition below that is marked "recommended, adopted", or that stands in a section saying so,
is this session's recommendation, adopted under that instruction without Ben's reading it, and
each gives its reason. Weighing "low stakes" and "I need this review to end", the
session recommended a fix where an item's text or behaviour is wrong and the fix is small, and
leaving an item as it is where the defect is latent, debatable or not worth its cost.

### Finding 1: MAM-simple's narpas label

1. **1.3, and with it the MAM-simple half of 1.2: "Name lp-paseq".** MAM-simple's notice, in all 70
   files, its two reading guides and its README name the element that MAM-simple contains, and
   MAM-parsed's notice and README keep `מ:פסק`. The selected text: the MAM-simple notice's narpas
   rule opens "Narpas (narrow-sense paseq, lp-paseq) forms no compound of any kind: only maqaf joins
   atoms into a chanted word.", the rest of the rule unchanged; the bullet in
   `MAM-simple/doc/reading-mam-simple.md` and the sentence in `reading-mam-simple-xml.md` say
   "Narpas (narrow-sense paseq, `<lp-paseq>`) forms no compound of any kind"; and
   `MAM-simple/README.md`'s pointer to its cautions ends "around narpas (narrow-sense paseq,
   `<lp-paseq>`)." The option said that the change reaches the 70 files' public data, and that the
   hand-run generators are then rerun, with no product change expected.

### Finding 2: `DATA-LICENSES.md`

1. **2.1: "Own row, CC-BY-SA".** Row 79 keeps `in/accgram/edition_transcriptions/` under CC0, as
   "Ben Denckla's hand transcriptions of the accentuation of printed Decalogue editions", and a new
   row after it reads: "| `in/accgram/printed_decalogue_teamim.json` | a capture of MAM's eight
   Decalogue versions from the Hebrew Wikisource page עשרת הדברות בסיס/טעמים, at the revision its
   `provenance` block records, with a folded form derived from it for the scanners | CC-BY-SA 4.0 —
   the statement below. It is the same page as one of `in/mam-ws-special/`'s, and what is derived
   from MAM carries MAM's terms |".
2. **2.2: "Credit each source".** The terms of row 84, `out/accgram/`, end "The biblical Hebrew
   each file quotes keeps the terms of its source above: the WLC's and the UXLC's, or, where a file
   quotes MAM, as the printed-Decalogue outputs do, MAM's CC-BY-SA 4.0", and those of row 91,
   `gh-pages/wlc/`, end "The biblical Hebrew the pages display keeps the terms of its source above:
   the WLC's and the UXLC's, or, where a page quotes MAM, as the printed-Decalogue pages do, MAM's
   CC-BY-SA 4.0".

### Finding 3: public files that carry private-repository material

Each disposition here is the session's recommendation, adopted under Ben's instruction above.

1. **The governing question: the 2026-08-27 rule governs what a public-only session judges.** The
   document inside MAM-private that `in/repo_maintenance_policy.json`'s `MAM-private` entry names
   governs sessions that may read MAM-private. A public-only session, such as one of the public
   review series, cannot read it and judges by the 2026-08-27 rule in the same file's
   `repo_visibility` comment. The `MAM-private` entry's comment gains a sentence that says so.
2. **3.5: the rule applies to text written from now on, with stated exemptions.** It does not reach
   agent routing in skills and instructions, code comments and docstrings, dated records, or the
   policy and manifest files under `in/`, which name private paths for sessions that can read them
   or record what happened. Elsewhere, existing text is left as written. The `repo_visibility`
   comment gains a sentence recording this scope. Reason: the census's hits are paths and file
   names, not findings, and a retroactive sweep of more than a hundred lines costs more than it
   protects.
3. **3.1: leave as is**, as existing text under item 3.5's disposition. What the update entry names
   of hbofonts is not sensitive, and Git history keeps it whatever the current text says.
4. **3.2: leave as is**, as existing text under item 3.5's disposition: the link into MAM-private in
   `doc/dual-agent-review.md` and the MAM-private issue link in
   `doc/PLAN-silluq-before-gaya-template.md`.
5. **3.3: leave as is**, as existing text under item 3.5's disposition; besides, the lookup that
   `py/ws/ws_bot_edit_history.md` describes cannot work without naming the files it reads.
6. **3.4: no sweep**, under item 3.5's disposition.

### Finding 4: Phonetic MAM

1. **4.1's question, the inverted nuns: "Add as item 9".** `Phonetic-MAM/README.md`'s list of
   departures gains: "9. **Inverted nuns.** This release has none of MAM's 9 inverted nuns,
   `MAM-simple/`'s `spi-invnun`, though it keeps MAM's parashah breaks and narrow-sense paseqs as
   rows of their own." Recounted here: 9 `spi-invnun` in `MAM-simple/json-vtrad-mam/`, 2 in
   Numbers and 7 in Psalms.
2. **4.6: "Correct the data".** The display contract gains a way to give a marker row its strand;
   the four marker rows, two in each verse, get the `טעם עליון` strand; and Exodus 20 and
   Deuteronomy 5 are regenerated, data and pages. The release then agrees with MAM there, so the
   README needs no note. It is a change to public data and published pages, and it takes item
   4.7's path past the frozen comparison.
3. **4.7: "Approved exception".** The freeze stays for every other chapter. A display correction
   that Ben approves is recorded in a tracked list of corrected chapters, which leave the
   comparison as refreshed chapters do, and their rendered diffs are reviewed instead.
4. **4.4: "Stop and ask Ben".** The suite's failure stays as the stop, and
   `dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md` adds, after "Never
   regenerate either file": "If every chapter has left the comparison, the suite fails with "every
   chapter left the comparison": stop, and ask Ben whether to retire the legacy projection
   comparison."
5. **4.5: "Bound it in code".** After the watchdog stops the adapter, the exporter stops waiting on
   the adapter's pipes after a short grace period, so that the limit holds whatever the adapter
   starts.

### Finding 5: texts that `AGENTS.md`'s new push rule left behind

Each disposition here is the session's recommendation, adopted under Ben's instruction above.

1. **5.2: fix.** D11's final integration in `doc/dual-agent-review.md` gains, before "Then fetch in
   the designated full integration clone": "Run the suite there too, or record a judged skip, as
   `AGENTS.md`'s rule for a push of `main` asks."
2. **5.3: fix.** `AGENTS.md`'s rule for a push of `main` gains: "If that decision follows the last
   commit, as when a worktree branch is fast-forwarded unchanged, push an empty commit
   (`git commit --allow-empty`) whose message says it, rather than amending."
3. **5.4: fix.** `py/product_scopes.py`'s docstring loses its restatement of the hand-run rule, from
   "A change to a hand-run generator" to "as their READMEs say.", so that its "this docstring does
   not restate it" is true. The restatement had already drifted: it names one exemption where
   `AGENTS.md` now has two. Re-read after Ben's commits of 2026-10-06: the item still holds.
4. **5.5: leave as is.** The judged skip stays available for a change to tracked product files. The
   consumer-notice commits of 2026-10-05, `fe85cd55` and `d8435412`, used it, and the second
   regenerated the change log that finding 1 found stale.

### Finding 6: the review procedure documents

Each disposition here is the session's recommendation, adopted under Ben's instruction above. The
wording of items 6.2, 6.4 and 6.5 is Ben's approved wording of 2026-10-03, so the plan gives each
replacement in full.

1. **6.1: fix.** Both documents say that the MAM-basics instance of the 2026-10-02 trial ran on
   2026-10-02, and that the procedure for a later two-agent window of MAM-basics is Ben's choice
   when he starts one: `doc/periodic-review.md`'s opening paragraph, and
   `doc/dual-agent-review.md`'s opening and its section "Next review: independent reviews and one
   disposition list". What they say of MAM-private's instance is unchanged.
2. **6.2: fix by narrowing.** The two sentences saying that `doc/dual-agent-review.md` records only
   what pairing adds gain an exception for D10's filename and State rules and D12's rule for
   correcting a finished document, which every review follows and which other instructions cite
   there; `doc/periodic-review.md`'s "Read `doc/dual-agent-review.md` as well only when the window
   is to be reviewed by two agents" gains the same exception. No section moves.
3. **6.3: fix.** The rule that a brief names the private repositories, in both documents, names
   beside `repo_visibility`'s list the private repositories outside the workspace that the tree
   cites, today `bdenckla/trope` and `bdenckla/al-hatorah`.
4. **6.4: fix.** `doc/periodic-review.md`'s sentence keeps "goes to Ben in chat rather than into the
   file" and credits D9 and D11 only with what they say: that such a claim stays out of a tracked
   turn.
5. **6.5: fix.** D9's gloss of "public evidence only" follows property 2 of
   `doc/periodic-review.md`: the turn reads no repository that property 2 names as private.

### Finding 7: checks and tools that do less than they say

Each disposition here is the session's recommendation, adopted under Ben's instruction above.

1. **7.2: fix the docstring only.** `py/tests/test_parser_stage_node_keys.py`'s docstring says that
   the lint reads only the classifier's top-level `if` tests and the two predicates' return
   constants, and that it does not check the refusal's body. No injection test is added, as the
   approved plan decided.
2. **7.4: leave as is.** It is latent: both word-form claims are 2, and the smallest of the
   denominators is 18. The error that ends the command names the claim, which is what the refresh
   must take to Ben in either case.
3. **7.5's second half: the code stands, and the documents follow it.** `doc/clone-forests.md` and
   `py/repo_util/forest_sync.py`'s module docstring say that the clone that only the calling
   session occupies is skipped whatever its state: the write form leaves it untouched either way,
   and that session is working in it.
4. **7.6: leave as is.** `repository-maintenance.md` already makes a failed relocation stop for
   inspection; a repair procedure can be written if a relocation ever fails.
5. **7.8: fix in code.** `py/main_repo_maintenance.py` catches step 2's `RetirementError`, reports
   the step as failed and goes on, as it does for step 1's `OSError`, so that "Seven independent
   steps" holds.
6. **7.11: fix by rejecting.** A compute reply that cannot be encoded as UTF-8 gets the ordinary
   error reply, "computation rejected", and the stream goes on, as `doc/phonetic-mam-compute.md`
   promises.

### Finding 8: questions for Ben

1. **8.1: "orphaned", in Ben's own words.** Ben first selected "Use "unattached"", which changed the
   footnote's "It is not orphaned between the two words as it is in Ezekiel." to "It is not left
   unattached between the two words, as it is in Ezekiel." After this session set out the context,
   that the same page sends its reader to his "Orphan pointing" page, he wrote: "Basically what I
   was saying is that I don't know why I restricted "orphaned" to describe the xiriq of ירושלם
   words; perhaps I had some other case or cases in mind where it was inappropriate but in that
   case I should have named those cases instead of forbidding all cases except xiriq-in-ירושלם
   ones. Nothing wrong with "unattached" except I don't like using two words for the same thing so
   I'd rather stick with "orphaned"". So the Job 38:12 footnote and its Ezekiel caption in
   `py/author_boj_qr/qr_38.py` use "orphaned" where they now say "unattached": "the פתח is
   unattached;" becomes "the פתח is orphaned;", and "The unattached פתח is visible between"
   becomes "The orphaned פתח is visible between"; the 2 Samuel sentence keeps "orphaned"; and the
   details page is regenerated. The `hebrew-prose` skill's reservation in
   `references/terminology.md`, "**orphaned** is RESERVED for the ḥiriq of the implicit yod
   in ירושלם-style spellings.", stops forbidding every other case. Its replacement is not yet
   worded. The plan drafts it for Ben's approval, naming any case in which "orphaned" is wrong
   rather than allowing a single one. This session's draft defines the word by the sense that
   both uses share: "**orphaned** = a point that belongs to no letter, such as the ḥiriq of the
   implicit yod in ירושלם-style spellings, or a point left between two written words."
2. **8.2: leave as is (recommended, adopted).** `doc/boj-image-crop-reproducibility.md`'s principles
   govern crops that a program makes, as its text says, and a crop supplied as a finished image
   records what is known of it in its commit message, as `6004709e` and `a1bbce52` do.
3. **8.3: "Add Phonetic-MAM".** The landing page's "MAM datasets and technical documentation" list
   gains an entry "Phonetic-MAM", linking
   `https://github.com/bdenckla/MAM-basics/blob/main/Phonetic-MAM/README.md`, after MAM-OSIS,
   through `py/author_site/site_data.py`. Re-read after Ben's near-Aleppo commits of 2026-10-05 and
   2026-10-06, which added a near-Aleppo entry to that list: the item still holds.
4. **8.4: "Add the prescribed credit".** Each of the eight pages keeps its link to the source it
   quotes and gains, after its existing credit, "Source attribution: Hebrew Wikisource, under
   CC-BY-SA 4.0.", with "Hebrew Wikisource" linking
   `https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning` and
   "CC-BY-SA 4.0" linking `https://creativecommons.org/licenses/by-sa/4.0/`, as the two index
   pages that C15.8 corrected attribute MAM. The same line goes on
   `gh-pages/wlc/accgram/printed-decalogue-uvinkha.html`, which names Hebrew Wikisource with no
   link, and the remediation plan's census adds any other English page that quotes MAM material.
5. **8.5: "State MAM's terms".** `Phonetic-MAM/LICENSE.md`'s third line becomes "This statement
   applies equally to the MAM text and its derivative display in `data/`, and to the MAM Hebrew
   that `examples/display.json` quotes."; the terms of `DATA-LICENSES.md`'s row for
   `Phonetic-MAM/examples/display.json` gain "The pointed Hebrew forms the tables quote are MAM's
   text and keep MAM's CC-BY-SA 4.0 terms above."; and the Phonetic-MAM clause of that file's
   preface to the MAM statement ends "the MAM text and its derivative display in
   `Phonetic-MAM/data/` and the MAM Hebrew that `Phonetic-MAM/examples/display.json` quotes".
6. **8.6: "Both to past tense".** In `Yeivin-ITM/README.md`, "Its source is pinned to MAM-private
   commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`." becomes "The migration took its source from
   MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`; no test pins the adaptation to it
   now.", and "All 17 existing filenames, internal links, and anchors are preserved." becomes "The
   migration preserved all 17 existing filenames, internal links, and anchors.", C6.2 option A's
   wording.
7. **8.7: fix (recommended, adopted).** In `doc/PLAN-mega-speedup.md`, items 1 and 3 of the list
   that the plan carries forward say that a cloud run now runs `accgram-survey-post-stress-meteg`
   and skips only `phonetic-mam-export`; the executed Phase 2 steps stay as written.
8. **8.8: fix (recommended, adopted).** The Unicode section of the common body,
   `dot-Codex/user-wide-AGENTS.md`, says that such an entry point "reconfigures stdout to UTF-8,
   and stderr to UTF-8 with `errors="backslashreplace"`, at the start of `main()`", and the change
   is deployed with `--sync-user-config`.
9. **8.9: fix (recommended, adopted).** `hebrew-prose`'s `references/rendered-prose.md` drops
   "Cross-repo rule; cf. MAM-basics `py/versification_and_cantillation/doc.py`.", so that it calls
   the strand-name rule trio-only throughout, as its SCOPE paragraph and the module it cited agree.
10. **8.10: deferred (recommended, adopted).** A separate cleanup task, outside this review's
    remediation, replaces the nine NFC calls on Hebrew text with comparisons through
    `give_std_mark_order`, and decides whether the three NFKD calls on Hebrew presentation forms, a
    different operation, become a recorded exception. None of the twelve is in the window's added
    lines; each came with copied or vendored code.

### Finding 9: one-line items

1. **9.2: ""the similar cases"".** The heading in `py/author_boj_qr/qr_38.py`, "φ1 — Attachment of
   the פתח in the parallel passages", becomes "φ1 — Attachment of the פתח in the similar cases", the
   name that the calling discussion and the footnote's body use, and the details page is
   regenerated.
2. **9.4: "Add to the README rows".** In `DATA-LICENSES.md`, row 52 becomes "|
   `Yeivin-ITM/README.md`, `Yeivin-ITM/LICENSE.md`, `Yeivin-ITM/schema/` | the product's README,
   with the adaptation's permission notice and bibliographic scope, its licence statement, and the
   closed JSON Schema of its claim data | MAM-basics' own work, so GPL-3.0. The adaptation the
   README describes keeps the terms of the `py/yeivin_itm/content/` row below |", and row 57
   becomes "| `Phonetic-MAM/README.md`, `Phonetic-MAM/LICENSE.md`, `Phonetic-MAM/schema/` | the
   product's README, its licence statement, and the closed JSON Schema of its display data |
   MAM-basics' own work, so GPL-3.0, apart from the MAM statement that `LICENSE.md` repeats
   verbatim |". `Yeivin-ITM/LICENSE.md`'s restatement of row 52 follows.
3. **9.8, its README half: "Dashes, as DATA-LICENSES".** `README.md`'s "Code: GPL-3.0" item reads
   "This covers MAM-basics' work in code and prose: everything under `py/`, `.github/` and `doc/` —
   except the adapted excerpts and their remarks under `py/yeivin_itm/content/`, the third-party
   font under `doc/woff2/`, and the page crops in `doc/*-snips/` and the Hebrew Wikisource Village
   Pump discussion captured and translated in `doc/wikisource-dagesh-discussion-*` — and the
   generated indexes and reports under `out/` that carry no corpus text.", its following sentences
   unchanged.
4. **9.12: leave as is (recommended, adopted).** The field table's "Guidance for people and programs
   using the data" describes the notice embedded in the data, and "The notes below are for writers
   of programs" describes the guide's own notes: they name the audiences of two different texts.
5. **9.13: leave as is (recommended, adopted).** The two sentences state what a dry run and a re-run
   show for a targeted edit, the case the bot guide is written for; the uncommon cases, an
   untargeted kind, a narrower selector or an edit that changes nothing, are low stakes.
6. **9.18: leave as is (recommended, adopted).** In the mega, the step's reconfiguration repeats
   what the mega's `force_utf8_io` has already set, so it changes nothing.
7. **9.21: leave as is (recommended, adopted).** `py/main_uxlc_grammar_test.py` is outside the
   default collection, and `py/repo_util/check_repo_standards.py` excludes `main_` files by name and
   names this one.
8. **9.22: fix (recommended, adopted).** Every listed block is made to parse with the least change:
   a placeholder for which one value always works takes that value, as C15.24 did; any other is
   quoted, with PowerShell's call operator where it stands for a command's path; and the unlabelled
   one-liner after "Re-establish with:" in `doc/PLAN-repo-maintenance-across-GitRepos.md` gets the
   least change that makes it parse. The plan gives each block's text.
9. **9.36: leave as is (recommended, adopted).** The handler's callers, repository maintenance and
   worktree retirement, run on Ben's Windows machines, and a POSIX change could not be run here.
10. **9.38: leave as is (recommended, adopted).** The message already names both causes, "ended
    early or exceeded its book limit"; only the exit status it adds misleads, and only on Windows.
11. **9.39: fix in the document (recommended, adopted).** `doc/phonetic-mam-compute.md`'s "A request
    line is limited to 16 Mi characters" becomes "A request line, including its line terminator, is
    limited to 16 Mi characters".
12. **9.42: leave as is (recommended, adopted).** `main()` sets `sys.dont_write_bytecode` itself,
    and the test covers the tracked files; a test that could catch import caches would need a
    different design for little gain. Re-read after Ben's commits of 2026-10-06, which changed
    `py/tests/test_yeivin_itm.py`: the item still holds.

### The review's "Noticed outside the diff"

Each disposition here is the session's recommendation, adopted under Ben's instruction above.

1. **Issue #296: leave as is, so no outward act.** The issue is a low-priority investigation note,
   its body names the Codex session that wrote it, and GitHub records when it was opened.
2. **`_reference_matches`: fix.** A `path:line`, `path:line:`, `path:first-last` or `path#Lline`
   form counts as a citation of the file. A missed citation can let a worktree's retirement treat
   cited `.novc` evidence as uncited, and widening the match only retains more.
3. **The break markers at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17: assess with item 4.6.**
   The remediation that corrects item 4.6's rows in Exodus 20 and Deuteronomy 5 compares the
   release's break markers with MAM-parsed's at these three verses. Where the release misrepresents
   MAM, a correction takes item 4.7's path, which needs Ben's approval; otherwise nothing changes.

### "Noticed while fixing", items 1 and 2

Each disposition here is the session's recommendation, adopted under Ben's instruction above.

1. **Fix in place.** Two stale claims in live update files are corrected in place, as items 9.28 and
   9.33 were elsewhere. In `doc/review-findings-2026-10-02-update.md`'s entry "Remediation
   implemented; final gates pending, 2026-10-03": "the archive commit, the last whose tree holds
   every file that the relay's removal deleted", since `d168e22e` holds them too. In
   `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`'s entry "Remediation execution by
   Codex, 2026-10-01": "Public verification evidence is retained under this worktree's ignored
   `.novc/`", since that worktree and its `.novc` were removed on 2026-10-04. `4573b007`'s commit
   message stays as written.
2. **Fix.** The `accgram-survey-post-stress-meteg` step record in `py/main_0_mega.py`, and the
   comment above it, name `MAM-parsed/plus/` among the survey's inputs. Re-read after Ben's commits
   of 2026-10-06: the record still omits it.

### Every open item has a disposition

Checked against the first entry above: every item it marks "Awaiting Ben's decision", and both of
its optional "Noticed while fixing" items, has a disposition here, 56 in all. Ben selected 16 in
the dialogs, and replaced one of those selections, item 8.1's, in his own words. The other 40
carry this session's recommendation, adopted under his instruction: 23 go to the remediation
plan, 16 are left as they are, and one, item 8.10, is deferred to the separate cleanup task that
its disposition describes.

**Effective base State, 2026-10-06:** partly acted on; close-out step 1 complete, every item
having a disposition; remediation pending. Close-out step 2 now needs a fresh-task remediation
plan, with concrete wording, for the 39 items whose disposition changes a file or assesses one:
the 16 that Ben selected and 23 of the recommended dispositions. The plan re-measures each on the
current tree, presents them by public-facing risk, and puts each wording to Ben before it is
applied. The 16 items left as they are need nothing more. Item 8.10 stays deferred until Ben
starts its cleanup task. The base report's line 3 stays as written, and this update remains
`State: open` while its base survives.

## The qere-first order: Ben's decision and the documentation, 2026-10-06

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-06, New York
time, in the full clone `C:/Users/BenDe/GitRepos/MAM-basics` on `main`. Working from a prompt
that the session of the withdrawal entry above wrote, this session discussed whether
MAM-simple's encoding or documentation should change so that no reader takes the first child of
a `kq` to be its ketiv. It set out the options: a distinct element for the 129 qere-first pairs,
an attribute or `class` value on `kq`, a fixed child order with the order in an attribute, or
documentation alone.

**Ben's decision, 2026-10-06: no change to MAM-simple's data.** He wrote: "upon thinking about
it, I don't want to make any changes to the MAM-simple data", and then, of the documentation
changes this session proposed: "Just do it all, please, using your best judgment and asking no
questions as long as this is all documentation and won't change "goldens" like MAM-with-doc HTML
files."

**Done.** The documentation now says that a pair's two children are in the order that MAM's
rendered pages on Hebrew Wikisource have, which is qere first in about one pair in eight, and
that a reader identifies them by element type:
- `MAM-simple/README.md`, in a new caution, "Ketiv/qere order";
- `MAM-simple/doc/reading-mam-simple-xml.md`, in "Ketiv/Qere", with Lamentations 1:18 as its
  example, and in its table of alternatives;
- `MAM-simple/doc/reading-mam-simple.md`, in "Consumer notice";
- `MAM-simple/doc/reading-mam-simple-json.md`, in a new section, "Ketiv/qere objects";
- `MAM-for-Sefaria/README.md`, which adds that the files under `csv-ajf/` have the ketiv first
  throughout.

The README's sentence pointing to its cautions keeps its ending, "around narpas (narrow-sense
paseq, ׀).", which item 1.3's disposition above rewrites. The notice embedded in MAM-simple's 70
data files is unchanged, being part of the data, and no generated file changed. The mega and
the suite were not run, at Ben's instruction: "Don't run the test suite and please Lord don't
run mega. This is all just documentation."

**Carried by other sessions, from prompts this session wrote at Ben's request.** MAM-parsed's
guide now says that MAM has the qere first (`9e64d3b4`, `d6b19241`). One session shows Ben the
four ketiv-first templates that directly follow a maqaf, at 2 Samuel 20:23, 2 Chronicles 13:19,
Jeremiah 48:21 and Ezekiel 39:25; another makes the example program in
`MAM-simple/doc/reading-mam-simple.md` fail on an unknown element. The effective base State
above is unchanged.

**Corrected the same day.** Ben asked whether "MAM has the qere first" made clear which MAM it
meant. It did not: MAM's wikitext and MAM-parsed list the ketiv first in every ketiv/qere
template, and only MAM's rendered pages have the qere first. The five documents now name MAM's
rendered pages on Hebrew Wikisource, and MAM-simple's README and XML guide state the
difference. MAM-parsed's guide gives the parameters' ketiv-first order in the same sentence as
its "MAM has the qere first", so its sense is clear there, and it is unchanged.

## The four post-maqaf ketiv-first templates renamed on Wikisource, 2026-10-06

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-06, New York
time, in the full clone `C:/Users/BenDe/GitRepos2/MAM-basics` on `main`. It worked from a prompt
that a read-only Claude session wrote the same day after finding the four, the work that "Carried
by other sessions" above gives to one session. That prompt quotes Ben's instruction to its
session as: "Give a prompt for a session that will write a bot to fix all four of these to use
the appropriate post-maqaf ketiv/qere template."

**Done.** BDencklaBot gave the template `קו"כ` to the four ketiv/qere whose qere directly follows
a maqaf but whose call was `כו"ק`: 2 Samuel 20:23, Jeremiah 48:21, Ezekiel 39:25 and 2 Chronicles
13:19. Ben approved the save and its edit summary in the app's dialog after seeing the dry run.
The edit file is `0067293b`, and `3c58d087` is the run's record, where
`py/ws/ws_bot_edit_history.md` describes the run and the page histories behind it. The near-Aleppo
build's sealed pointings named the four targets, and Ben chose in the same dialog to re-seal them
mechanically: `e5cd5997` re-sealed them and `a1ab20f8` regenerated near-Aleppo.

**Counts that moved.** Two measurements in the entries of 2026-10-05 were true when taken and stay
as written: "129 of the 1,047 `kq` elements list `kq-q` before `kq-k`", under "Noticed while
fixing, not acted on", and "884 `כו״ק`, 126 `קו״כ` and 37 `מ:כו״ק מיוחד`", with "The 129 elements
that list `kq-q` first", in the withdrawal entry. Since `3c58d087` the figures are 133 of 1,047,
and 880, 130 and 37. The 133 are the 130 `קו״כ` and the same three `מ:כו״ק מיוחד`.
`MAM-simple/doc/reading-mam-simple-xml.md` now says "133 of the 1,047 pairs, counted on
2026-10-06". The other documents that the entry above names say "about one pair in eight", which
remains true.

**Also fixed.** The Lamentations 1:18 example that the entry above added to
`MAM-simple/doc/reading-mam-simple-xml.md` and `reading-mam-simple-json.md` had its Hebrew in
Unicode's normal mark order, not MAM's, so `test_prose_mark_order.py` and
`test_mam_simple_mark_order.py` failed on four of its lines. `efe58d21` gave them MAM's order, and
line 491 of `doc/PLAN-remediate-review-findings-2026-10-04.md` the same.

The effective base State above is unchanged.

## Ben's approval of the remediation plan, 2026-10-06

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-06, New York
time, in the full clone `C:/Users/BenDe/GitRepos/MAM-basics` on `main`: the session that wrote
`doc/PLAN-remediate-review-findings-2026-10-04.md`, pushed as `2af21b46`, as close-out step 2.

**Ben's message**, verbatim, in reply to the session's presentation of the plan by public-facing
risk: "approved; execute". As the plan's "Ben's part" sets out, that reply approves:

1. every wording in the plan, including item 8.4's narrower scope: the credit goes on the nine pages
   that the disposition above names, and the census of the other English pages that quote MAM is
   recorded rather than acted on, for the reasons the plan's R8 gives;
2. its public data changes, including two display corrections under item 4.7's approved-exception
   path: the strand of the narrow-sense paseq rows at Exodus 20:3 and Deuteronomy 5:7 (item 4.6),
   and the break forms at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17 (the review's third item
   under "Noticed outside the diff, not findings", which the plan calls N3);
3. the execution, in the plan's waves.

**Effective base State, 2026-10-06:** partly acted on; close-out steps 1 and 2 complete, the
remediation plan approved; remediation in progress. The base report's line 3 stays as written, and
this update remains `State: open` while its base survives.

## Remediation executed, 2026-10-07

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-07, New York
time: the session that wrote `doc/PLAN-remediate-review-findings-2026-10-04.md` and the entry above,
which then executed the plan, as close-out step 3 of `doc/periodic-review.md`, under Ben's
"approved; execute" of 2026-10-06. It worked in the full clone `C:/Users/BenDe/GitRepos/MAM-basics`
on `main`. Editing began at `2af21b46`, the commit that added the plan, once `aef25641` and
`2af21b46` were confirmed ancestors of `HEAD`; since `aef25641` only the plan had changed, so every
passage that the plan quotes still read as quoted.

**Commits**, in the plan's waves:

1. wave 0, Ben's approval: `9b654fd4`;
2. wave 1, text outside the products: `e66ce85b` (procedure documents), `1ba7bfa3` (instructions,
   skills and policy comments), `72fc4097` (maintained documents and records) and `ca6f818b`
   (docstrings and comments);
3. wave 2, code: `1a2456da` (item 7.11), `3e0c383f` (7.8), `0f047b4f` (N2) and `82cab117` (4.5);
4. wave 3, reader-facing documents that no program generates: `2efd5de5`;
5. wave 4, generated pages: `e52e0e6d` (items 8.1 and 9.2), `0eb6ed17` (8.3) and `41f3d2bf` (8.4);
6. wave 5, MAM-simple's notice: `65a744d3`;
7. wave 6, the Phonetic MAM correction: `26c33edd`;
8. `03b01e85`, which merged, with no conflict, the two commits that reached `origin/main`
   meanwhile: `20d2c7bd`, which stores holam before qadma in the 2 Samuel 15:8 pointed ketiv, and
   its merge `8f225663`. They touch only near-Aleppo files and `py/render_wt/render_wikitext_kq.py`,
   none of which this remediation changed;
9. `bea27331`, which puts five lines of hand-authored Hebrew into MAM's mark order after the final
   gate's first suite run failed on them ("Checks and the final gate", item 4);
10. `41a65acb`, which added this entry and set the plan's State;
11. `a11e1dfc`, which merged the ten commits that reached `origin/main` while the gate ran,
    `0067293b` to `cfb3a284`. They rename four post-maqaf ketiv/qere templates to `קו"כ` on Hebrew
    Wikisource and regenerate what depends on them, re-seal near-Aleppo, give the same five lines
    as `bea27331` MAM's mark order (`efe58d21`), and add the entry before this session's two. The
    one conflict was this file, where both sides had appended;
12. the commit that brings this entry up to date with the gate on `a11e1dfc`, and a last commit
    that adds the push and the deployment to "Checks and the final gate".

**How each disposition was established.** Each wave's commit message records the measurement that
it re-ran for its items on the committed code, and every commit had `git diff --check` and, for its
changed Python files, Black and ruff. On the final tree, `a11e1dfc`, a scratch script read every
site that the plan names from the commit's tree, in 90 checks that include the changed lines of the
three corrected chapter pages: each site has its approved text and lacks the text it replaced, and
`git log 2af21b46..a11e1dfc` names, for each site's file, the commit given below. The release's
three changed book files and the two files that hash them are covered instead by the analysis
reader's measurement below and by the gate's mega, which regenerated them with no diff. After the
final gate, every measurement that is more than a reading was re-run on the same tree, with the
results given below; the code items' demonstrations among them reuse harnesses that the planning
sub-agents pm-code and tool-code wrote, re-read before use. No sub-agent ran during execution.
Nothing in MAM-private or hbofonts was read except by tracked code: the suite, and the megas of
wave 6 and of the final gate, whose `phonetic-mam-export` step re-exports the Phonetic MAM release
through the private adapter. A change that makes a text say what code does fixes the text, not
the behaviour, and the dispositions of items 7.2, 7.5 and 9.39 say so.

**Summary.** Of the 39 items, 34 are fixed; items 7.2, 7.5 and 9.39 have their text fixed and the
behaviour it describes unchanged, as each disposition chose; and items G and 3.5 record a policy in
the policy file's comments. No item is left unfixed.

### Finding 1: MAM-simple's narpas label

1. **1.3, with the MAM-simple half of 1.2: fixed in `65a744d3`.** MAM-simple's consumer notice
   names `lp-paseq`, and its README and two reading guides say "(narrow-sense paseq,
   `<lp-paseq>`)"; MAM-parsed's notice, README and guide keep `מ:פסק`. Re-measured at `a11e1dfc`:
   the notice's narpas rule names `lp-paseq` in all 70 of MAM-simple's data files, 35 JSON and 35
   XML, and the template in all 24 of MAM-parsed's plus files. The regeneration changed one line in
   each of the 70 files and nothing else, and the hand-run generators showed no product change
   ("Checks and the final gate", item 2).

### Finding 2: `DATA-LICENSES.md`

1. **2.1: fixed in `2efd5de5`.** `in/accgram/printed_decalogue_teamim.json` had its own CC-BY-SA
   4.0 row, and row 79 keeps Ben's hand transcriptions alone under CC0. Re-measured: the file's
   `provenance` named page id 344500 and revision 3025606, which `in/mam-ws-special/manifest.json`
   records for the same page. Later on 2026-10-07 the file and its row were deleted, and its
   readers moved to that page's mirror, `in/mam-ws-special/decalogue-base.mediawiki`, which the
   `in/mam-ws-special/` row covers ([PLAN-refresh-by-judgment.md](PLAN-refresh-by-judgment.md),
   wave 5, item 2).
2. **2.2: fixed in `2efd5de5`.** Rows 84 and 91 give MAM's CC-BY-SA 4.0 to the Hebrew that a file or
   page quotes from MAM.

### Finding 3: public files that carry private-repository material

1. **G, the governing question: recorded in `1ba7bfa3`.** The `MAM-private` entry's comment in
   `in/repo_maintenance_policy.json` says that the document it names governs a session that may
   read MAM-private, and that a public-only session judges by the 2026-08-27 rule.
2. **3.5: recorded in `1ba7bfa3`.** The `repo_visibility` comment records that rule's scope. The
   policy file parses as JSON, and `py/tests/test_repo_visibility_declared.py` passes.
3. **3.1 to 3.4: left as they are**, under item 3.5's disposition.

### Finding 4: Phonetic MAM

1. **4.1's question: fixed in `2efd5de5`.** `Phonetic-MAM/README.md` lists the inverted nuns as
   departure 9. Re-measured at `a11e1dfc`: 9 `spi-invnun` in `MAM-simple/json-vtrad-mam/`, 2 in
   Numbers and 7 in Psalms, and no U+05C6 in the release's book files.
2. **4.4: fixed in `1ba7bfa3`.** The refresh procedure, `dependent-refresh.md`, says to stop and ask
   Ben whether to retire the legacy projection comparison when the suite fails with "every chapter
   left the comparison", the message that `py/phonetic_mam/projection_check.py` gives.
3. **4.5: fixed in `82cab117`.** Re-measured at `a11e1dfc` with pm-code's fake adapters in place of
   `_adapter_command`, the limit patched to 5 s and a grandchild sleeping 20 s, nothing reaching
   MAM-private: for both the books and the test pages, a grandchild that holds stderr, stdout or
   both, or holds stdout after the adapter has written everything and exited, ends the run at 10.0
   to 10.2 s, the limit plus the grace, where `aef25641` took 20.15 to 20.19 s; an adapter that
   exits 1 at once while its grandchild holds stderr ends it at 5.1 to 5.3 s; and five normal runs
   of each return their results, leaving no thread, warning or open pipe, with the handle count back
   at its baseline. The harness's stub of `display_projection.project_book` had first to accept the
   two keyword arguments that wave 6 added.
4. **4.6: fixed in `26c33edd`.** The four narrow-sense paseq marker rows of Exodus 20:3 and
   Deuteronomy 5:7 have the strand label `טעם עליון` in both pronunciations, from the ב parameter of
   MAM-parsed's dual-cantillation template, so the analysis reader counts them in that strand
   alone. Re-measured at `a11e1dfc` through the analysis reader: at both verses the two marker rows
   have the strand `cant-bet`, the reader's name for that label, a `cant-alef` selection lists no
   narrow-sense paseq and a `cant-bet` selection lists both, and these four are the only labelled
   marker rows in the 39 books.
5. **4.7: fixed in `26c33edd`.** `in/phonetic_mam_display_corrections.json` lists the three
   corrected chapters, each with Ben's approval and the reason; `verify_site` leaves them out of the
   frozen comparison, as it does a refreshed chapter; and `check` lists them. Re-measured at
   `a11e1dfc`: `py/main_phonetic_mam.py check` lists the 3 chapters that have left the comparison
   by an approved correction, Genesis 35, Exodus 20 and Deuteronomy 5, and the 4 that the merged
   template rename made leave it by a change of MAM-parsed input, 2 Samuel 20, Jeremiah 48, Ezekiel
   39 and 2 Chronicles 13; at `bea27331`, before that merge, it listed no such chapter. The suite's
   comparison of the other 922 passes.

### Finding 5: texts that `AGENTS.md`'s new push rule left behind

1. **5.2: fixed in `e66ce85b`.** D11's final integration runs the suite there too, or records a
   judged skip.
2. **5.3: fixed in `1ba7bfa3`.** `AGENTS.md` sends a skip decision that follows the last commit to
   an empty commit rather than an amend.
3. **5.4: fixed in `ca6f818b`.** `py/product_scopes.py`'s docstring no longer restates the hand-run
   rule, so its "this docstring does not restate it" holds; `test_product_scopes.py` passes.
4. **5.5: left as it is.**

### Finding 6: the review procedure documents

1. **6.1: fixed in `e66ce85b`.** Both documents say that MAM-basics' instance of the 2026-10-02
   trial ran, and that the procedure for a later two-agent window is Ben's choice when he starts
   one.
2. **6.2: fixed in `e66ce85b`.** The two sentences saying that `doc/dual-agent-review.md` records
   only what pairing adds, and `doc/periodic-review.md`'s advice to read that document only for a
   two-agent window, make an exception of D10's filename and State rules and D12's rule for
   correcting a finished dated document.
3. **6.3: fixed in `e66ce85b`.** In both documents a brief names the private repositories outside
   the workspace that the tree cites, today `bdenckla/trope` and `bdenckla/al-hatorah`.
4. **6.4: fixed in `e66ce85b`.** `doc/periodic-review.md` credits D9 and D11 only with keeping a
   transcript-only claim out of a tracked turn.
5. **6.5: fixed in `e66ce85b`.** D9 glosses "public evidence only" by property 2 of
   `doc/periodic-review.md`: the turn reads no repository that property 2 names as private.

### Finding 7: checks and tools that do less than they say

1. **7.2: the docstring fixed in `ca6f818b`; the lint's two gaps are documented, not closed.** The
   docstring now says that the lint reads only `node_type_and_subtype`'s top-level `if` tests and
   the return constants of the two predicates, and not the refusal's body. The lint is unchanged, as
   the disposition chose.
2. **7.4: left as it is.**
3. **7.5's second half: the two texts fixed in `72fc4097` and `ca6f818b`; the code is unchanged.**
   `doc/clone-forests.md` and `py/repo_util/forest_sync.py`'s module docstring say that the clone
   that only the calling session occupies is skipped even when it is dirty, off `main`,
   mid-operation or locked, as the code's skip, which returns before those reasons are consulted,
   does.
4. **7.6: left as it is.**
5. **7.8: fixed in `3e0c383f`.** Re-measured at `a11e1dfc` in memory, every side effect stubbed: a
   missing default branch, an unreadable branch ref and a Git that cannot be launched each print
   `worktrees: FAILED (...)`, steps 1 and 3 to 7 still run, and the run exits 1, as it does when
   step 1 fails; a clean audit exits 0. The catch takes `OSError` as well as the disposition's
   `RetirementError`, as the plan records, since a Git that cannot be launched is the audit's other
   failure.
6. **7.11: fixed in `1a2456da`.** Re-measured at `a11e1dfc` by subprocess, with `PYTHONUTF8=0` and
   no `PYTHONIOENCODING`: one stream of 14 lines, seven requests that each carry the escaped lone
   surrogate `"\ud800"`, each followed by a good request, gets 14 replies and exit status 0. The two
   routes that echo it, a `phrase` request's untangler key and an `accents` value after a word's
   letters, get the error reply `UnicodeEncodeError`, "computation rejected"; every good line gets
   its result.

### Finding 8: questions for Ben

1. **8.1: fixed in `e52e0e6d`, the footnote, and `1ba7bfa3`, the skill.** The Job 38:12 footnote and
   its Ezekiel caption say "orphaned" where they said "unattached", and `hebrew-prose`'s
   `references/terminology.md` defines "orphaned" as a point that belongs to no letter, naming the
   cases in which the word is wrong. Re-measured at `a11e1dfc`: `git grep` finds "unattached" in
   none of `py/author_boj_qr/`, `gh-pages/book-of-job/` and `book-of-job/out/`, and the gate's mega
   left the regenerated page unchanged.
2. **8.2: left as it is.**
3. **8.3: fixed in `0eb6ed17`.** The landing page lists Phonetic-MAM among the MAM datasets.
4. **8.4: fixed in `41f3d2bf` on the nine pages that the disposition names, the scope Ben
   approved.** Each has the credit line once, after its existing credit. "Item 8.4's census" below
   records the other English pages that quote MAM.
5. **8.5: fixed in `2efd5de5`.** `Phonetic-MAM/LICENSE.md`, row 56 and the preface to the MAM
   statement give MAM's terms to the MAM Hebrew that `Phonetic-MAM/examples/display.json` quotes.
6. **8.6: fixed in `2efd5de5`.** `Yeivin-ITM/README.md`'s two sentences are in the past tense.
7. **8.7: fixed in `72fc4097`.** Re-measured at `a11e1dfc`: `py/main_0_mega.py` skips one step in a
   cloud session, `phonetic-mam-export`.
8. **8.8: fixed in `1ba7bfa3`.** The common body names stderr's `backslashreplace` handler, as
   `hebrew-prose`'s `references/verifying.md` requires; deployed as "Checks and the final gate"
   records.
9. **8.9: fixed in `1ba7bfa3`.** `rendered-prose.md` calls the strand-name rule trio-only
   throughout; deployed likewise.
10. **8.10: deferred**, unchanged.

### Finding 9: one-line items

1. **9.2: fixed in `e52e0e6d`.** The footnote's heading says "the similar cases"; `git grep` finds
   "parallel passages" in none of the three places that item 8.1's search covers.
2. **9.4: fixed in `2efd5de5`.** Rows 52 and 57 cover the two products' `LICENSE.md` files, and
   `Yeivin-ITM/LICENSE.md`'s restatement follows.
3. **9.8's README half: fixed in `2efd5de5`.** `README.md`'s "Code: GPL-3.0" item sets its
   exceptions between dashes.
4. **9.22: fixed in `1ba7bfa3`, `72fc4097` and `2efd5de5`.** Re-measured at `a11e1dfc`: every
   `powershell` fence in tracked Markdown, 236 in 302 files, parses with PowerShell's parser, and
   so does the unlabelled block after "Re-establish with:" in
   `doc/PLAN-repo-maintenance-across-GitRepos.md`.
5. **9.39: the document fixed in `72fc4097`; the limit is unchanged.** Re-measured by subprocess at
   `a11e1dfc`, with the limit at 16,777,216 characters: a request of that many characters is
   answered when unterminated and ends the stream when an LF ends it, and one a character shorter
   is answered when an LF ends it and ends the stream when CR and LF end it. So the limit counts
   the line terminator, as the document now says.
6. **9.12, 9.13, 9.18, 9.21, 9.36, 9.38 and 9.42: left as they are.**

### The review's "Noticed outside the diff"

1. **Issue #296: left as it is**, with no outward act.
2. **N2, `_reference_matches`: fixed in `0f047b4f`.** Re-measured at `a11e1dfc` in memory, against
   `aef25641`'s copy, with tool-code's 29 cases in relative and absolute spellings: `path:3`,
   `path:3:`, `path:3-5`, `path:3–5` and `path#L3`, bare or followed by text or punctuation, now
   count as citations; every near miss, such as `path:3:7`, a longer name, `:3x`, `#L`,
   `#section` or `::3`, stays rejected; all 58 results match their expectations; a directory
   reference followed by `:3` stays rejected; and lines 488 and 489 of
   `doc/dual-agent-review-comparison-2026-10-01.md` now count as citations of their `.novc` file.
3. **N3, the break markers: assessed, and corrected in `26c33edd` under item 4.7's path.** The
   plan's D3 found that at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17 the release had the
   same kind of break as MAM-parsed, MAM-simple and MAM's special page, but not MAM's form of it,
   and Ben approved the correction with the plan. Re-measured at `a11e1dfc` through the analysis
   reader: the marker row of Genesis 35:22 is `פפ`, and the second marker row of Exodus 20:13 and
   of Deuteronomy 5:17 is `ססס`, MAM-parsed's forms, each in both strands' selections.

### "Noticed while fixing", items 1 and 2

1. **W1: fixed in place in `72fc4097`.** The archive commit is "the removal commit's parent", and
   the Codex remediation's evidence "was retained ... until the worktree and its `.novc/` were
   removed on 2026-10-04".
2. **W2: fixed in `ca6f818b`.** The step record and its comment name MAM-parsed's `plus/` tree,
   which `py/accgram/post_stress_meteg_sources.py` reads through
   `read_books_from_mam_parsed_plus`.

### Item 8.4's census and the approved scope

The planning sub-agent attrib read all 1,653 tracked pages under `gh-pages/` at `aef25641`, 1,650 of
them English, and classified each generated family by what its generator renders. Apart from the
nine pages above, no page credits Hebrew Wikisource with a he.wikisource link. About 1,105 English
pages quote MAM material with no credit on the page: the MAM-with-doc edition's 60 pages, the
near-Aleppo edition's 65 and its 8 documentation pages, the Phonetic MAM release's 929 chapter pages
and 4 example pages, and about 40 more in a dozen families (the 23 FOI pages, 7 change logs, 9
post-stress-meteg pages, mpplus guides, misc pages, accgram pages that quote MAM forms, an UXLC
survey and two Holman pages). About 1,066 of them belong to the MAM-with-doc, near-Aleppo and
Phonetic MAM sites, whose index pages already have the prescribed credit. Eight more credit MAM's
source in another form: `gh-pages/MAM-OSIS/index.html`, `gh-pages/MAM-for-Sefaria/index.html`,
`gh-pages/MAM-parsed/plus/html/mpplus.html` and `mpplus_kq_special.html` name Wikisource with no
link; `urwotm_2` names it before two screenshots; `maqaf-nonfinal-accents.html` names it only in
hover text; and `telg-doc-notes.html` and `ps17v14-mam-doc-notes.html` credit MAM-with-doc. The
credit on all of them would touch about a dozen generators and four HTML builders, move the
near-Aleppo check's `PIN`, need a place outside `<main>` on every Phonetic MAM chapter page, and,
for `gh-pages/MAM-OSIS/index.html`, need a rerun of `py/main_mam_osis.py` that would also publish
the lag behind MAM-simple that Ben accepted on 2026-09-30. Ben approved the credit on the nine
pages alone, so the rest is a separate decision of his; nothing here starts it.

### Departures from the plan

1. **R9 was missing from wave 3's list**, though the plan gave its wording; `2efd5de5` carried it,
   and corrected the plan's wave 3 to name it.
2. **Item 8.4's line has one source for its words as well as its links.** Beside `LICENSE_URL`,
   `py/mb_misc/mam_attribution.py` has `ENGLISH_ATTRIBUTION_PARTS`, the line as (text, link or
   `None`) parts, which the seven generators render through their own HTML builders.
3. **Item 4.7's record is validated in a module of its own,**
   `py/phonetic_mam/display_corrections.py`, which `projection_check.corrected_chapters` and the
   exporter both use, where the plan put the validation in `projection_check`.
4. **A failing check did not stop the gate.** The plan's stop conditions include a failing check.
   The final suite's two failures, both Hebrew mark-order lints, had one remedy, which the lints
   name and `AGENTS.md`'s rule on mark order requires; it changes no visible character and no
   generated file; one of the five lines was this remediation's own, and the other four would have
   blocked any push of `main`. So this session applied the remedy in `bea27331` rather than
   stopping, and ran the suite again ("Checks and the final gate", item 4). Another session's
   `efe58d21`, pushed while the gate ran, gave the same five lines the same order, and `a11e1dfc`
   merged the two changes as one.

**A false claim in a pushed commit message.** `2af21b46`'s message says that the mega and the suite
were skipped because "the commit adds one planning document under doc/, which no generator, product
or test reads". `py/tests/test_prose_mark_order.py` reads every hand-authored prose file, the plan
among them, and failed on the plan's line 491 at `2af21b46`, in D4's item 3. `bea27331`'s message
and this entry correct the claim; the historical message stays as written.

### Noticed while planning, not acted on

No item names these, so each stays as it is; the plan's "Not in this remediation" records them.

1. `doc/PLAN-silluq-before-gaya-template.md:290` and `:491` begin with an unquoted
   `<home-clone>/.venv/Scripts/python.exe`, which parses only because the parser reads `<` as a
   command name, so item 9.22's parse-based census missed them.
2. `doc/PLAN-repo-maintenance-across-GitRepos.md:383` describes the forest write's refusal and its
   caller-only skip in the order that `doc/clone-forests.md` had before item 7.5.
3. The release has `ססס` for each of MAM's 328 song dividers, `מ:ששש`, which no README or schema
   describes; `py/author_misc/mp_cmn_rows_other.py:89–90` calls the divider "analogous to ססס".
4. `py/author_misc/mp_cmn_rows_other.py:57` says that `פפ` and `סס` appear "primarily in D column",
   where MAM-parsed's C cells hold them and its D cells hold none.
5. `DATA-LICENSES.md` has no row for `gh-pages/near-aleppo/` or `out/near-aleppo/`, which arrived on
   2026-10-05, after the review's window.

### Checks and the final gate

1. **Each commit** had the checks its message records: `git diff --check`; Black and ruff on its
   changed Python files; and the targeted tests that the plan names for its wave, all passing.
2. **The hand-run generators, for item 1.3.** `git archive` extracted the trees of `41f3d2bf`, the
   commit before wave 5, and of `65a744d3` into two scratch directories outside the checkout. In
   each, from its root and with this clone's interpreter, `py/main_mam4sef.py`,
   `py/main_mam4sef.py --just-ajf` and `py/main_mam_osis.py` exited 0. The two trees' outputs, 164
   files under `MAM-for-Sefaria/`, 59 under `MAM-OSIS/`, 29 under `gh-pages/MAM-OSIS/` and 3 under
   `gh-pages/MAM-for-Sefaria/`, are identical apart from the provenance line that names the
   extraction folder, in four `_provenance.md` files and `gh-pages/MAM-OSIS/index.html`, since, as
   the review found, the Sefaria reader ignores the notice and the OSIS reader drops XML comments.
   So the change reaches neither product, and their tracked files are left as they are, with the
   lag Ben accepted on 2026-09-30.
3. **The mega** ran on `03b01e85` from 23:51 on 2026-10-06 to 00:04 on 2026-10-07, New York time:
   all 60 steps exited 0 in 755.1 s of steps, with Graphviz the pinned 16.0.0 (20260814.1018), the
   claims check at 51 passed, 0 failed and 0 pending, and the `phonetic-mam-export` step
   re-exporting the release through the private adapter in 118.9 s. It left no tracked diff and no
   untracked file, so every output it regenerates, the corrected release, its pages and the surveys
   that read it among them, equals the committed one. Wave 6 had run the mega from
   `phonetic-mam-export` on, as `26c33edd`'s message records. After the second merge the mega ran
   again, on `a11e1dfc`, from 00:38 to 00:50, New York time: all 60 steps exited 0 in 674.3 s of
   steps, the claims check again at 51 passed, 0 failed and 0 pending, and `phonetic-mam-export` in
   102.0 s; it too left no tracked diff and no untracked file.
4. **The suite** first ran on `03b01e85` from 00:04 to 00:12, New York time: 1,053 passed, 5 skipped
   and 2 failed in 450.80 s. Both failures were mark-order lints, `test_mam_simple_mark_order.py`
   and `test_prose_mark_order.py`, on five lines whose Hebrew had its marks in Unicode's order
   rather than MAM's: four lines of the Lamentations 1:18 example in MAM-simple's JSON and XML
   reading guides, which `abded326` added on 2026-10-06 with the suite skipped at Ben's
   instruction, so that `origin/main` failed both lints from then until `efe58d21`; and a line of
   the plan's D4, item 3, which `2af21b46` added. `bea27331` passed the five lines through
   `uni_denorm.give_std_mark_order`, the remedy that both lints prescribe: each line keeps its
   characters, with only the order of the marks within a letter's cluster changed, and each
   reordered word now occurs verbatim in `MAM-simple/xml-vtrad-mam`, the data quoted. No generator
   reads those three files, so the mega's result stands for `bea27331`. The suite then ran on
   `bea27331` from 00:15 to 00:22, New York time: 1,055 passed and 5 skipped in 432.41 s, with
   nothing failing. After the second merge it ran on `a11e1dfc` from 00:50 to 00:58: 1,055 passed
   and 5 skipped in 428.51 s, again with nothing failing.
5. **Push and deployment.** A fetch found `origin/main` still at `cfb3a284`, and `main` went to
   `origin` as `1989be57` at 01:05 on 2026-10-07, New York time. From this clone,
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config` then deployed from
   `refs/remotes/origin/main` at `1989be57` and reported `USER_CONFIG_DEPLOYED_COUNT=8`: the
   common body, `~/.codex/AGENTS.md`, and its expected hash (item 8.8), and `hebrew-prose` (items
   8.1 and 8.9), `mam-wikisource-refresh` (items 4.4 and 4.7) and `mam-repository-topology` (item
   9.22), each in both `~/.claude/skills/` and `~/.agents/skills/`. Its `--check` reported
   `USER_CONFIG_PROBLEM_COUNT=0`, and the live copies read back with the new text and without
   `rendered-prose.md`'s "Cross-repo rule".

**Effective base State, 2026-10-07:** acted on. The remediation of the 39 items is integrated on
`main` at `a11e1dfc`, which passed the final gate, every item fixed or recorded as above. The 16
items left as they are need nothing more, and item 8.10 stays deferred until Ben starts its cleanup
task. The base report's line 3 stays as written, and this update remains `State: open` while its
base survives.

## Item 8.10 resolved by rewording the normalization rule, 2026-10-07

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-07, New York
time, in the full clone `C:/Users/BenDe/GitRepos/MAM-basics` on `main`, which began at `08fcae33`,
then `origin/main`. It worked from the prompt that the session of the previous entry wrote for
item 8.10's cleanup task. That prompt planned to replace the nine NFC calls with comparisons
through `give_std_mark_order` and to put the three NFKD calls to Ben as a possible recorded
exception; Ben's decision below replaced the plan.

**The review's measurement, re-run at `08fcae33`.** A `git grep` for `unicodedata.normalize` in
tracked Python finds the twelve calls on eleven lines that finding 8, item 10, names, each at the
line it gives, and the composability probe at `py/tests/test_transliterations.py:130`, which
passes Hebrew pairs as the item says; the seven other calls receive no Hebrew. Scratch scripts
outside the checkout put `give_std_mark_order` in place of each call in memory, without calling
`unicodedata.normalize` themselves, and measured what a replacement would do:

1. The Decalogue comparison, `py/accgram/decalogue_m_trad.py:154`, and its test,
   `py/tests/test_decalogue_m_trad.py:113`, would find the same: no difference in any strand, and
   all 284 chanted-word pairs whose bytes differ are equal under `give_std_mark_order`.
2. The holam-he check, `py/py_render/rt_validate_holam_he.py:170`, gives the same result on all 77
   rows of `holman/docs-not-served/table_data.json` under either key, and with no normalization at
   all.
3. The WLC-vs-UXLC report that `py/py_wlc_json_and_unicode/wlc_compare_mdc_with_uxlc.py:51–52`
   writes, `out/diff_mx_wlc420_uxlc.json`, would keep its 15 entries and gain 8. Each is an atom in
   which WLC 4.20 and UXLC put the same two marks on one letter in opposite orders, which NFC
   treats as the same text: meteg and munah at Exodus 20:3, 20:4 and 20:10 (twice) and
   Deuteronomy 5:8; atnah and silluq at Exodus 20:14, in WLC's numbering; geresh and patah at
   Exodus 20:4; and sheva and holam at 2 Kings 21:26.
4. With `give_std_mark_order`, the fragility test in `py/mb_cmn/uni_norm_fragile.py` would lose its
   meaning, because the test first drops four of the five marks that `give_std_mark_order` moves:
   the UXLC list that `py/main_uxlc_word_list.py` writes would fall from 7 words to 0, and the
   assertion in `py/py_misc/uni_check.py` over what MAM-simple's generator renders, which follows
   a check of MAM's order, could never fail.
5. The NFKD calls, `py/hkq_cmn/extract_docx_notes.py:52` and
   `py/tests/test_extract_docx_notes.py:89` and `:95`, decompose single presentation-form code
   points into a table that only the tests have applied since `ae663ff2` deleted the docx pipeline
   on 2026-09-03. Two of its 43 entries, U+FB2C and U+FB2D, put the dagesh before the shin or sin
   dot, which is Unicode's order.

**Where the absolute wording came from.** The rule's earliest form in this repository's history,
in the Copilot instructions of `d86e5779` (2026-03-09), read "Never apply Unicode normalization
(NFC, NFD, etc.) to Hebrew text in this project" and gave its reason: NFC "reorders combining marks
into canonical order, which destroys the project's intentional mark order". The Claude session
that restored the rule on 2026-08-04, in `2b671ae1`, wrote "Never call `unicodedata.normalize`
(NFC, NFD, any form) on Hebrew", which forbids any call rather than any change to Hebrew text. The
review counted calls against that wording.

**Ben's decision, 2026-10-07.** The session proposed leaving the twelve calls as they are and
rewording the rule. Ben wrote: "For now, please just ignore the categoricality of that language, or
perhaps de-categoricalize it rather than scurrying around the code base listing exceptions to a
supposedly ironclad rule", and, of the proposal, "What you suggest is fine".

**8.10: resolved in the rule's text, with the twelve calls unchanged.** In `AGENTS.md`, "**Never
call `unicodedata.normalize` in any form on Hebrew.** When two Hebrew strings that should match do
not, compare them through `give_std_mark_order`; do not normalize them." now reads
"`unicodedata.normalize` puts Hebrew marks in Unicode's order, not MAM's. So don't use it to produce
Hebrew that belongs in MAM's order, or to hide a mark-order mismatch that matters;
`give_std_mark_order` is the tool for both. A call that only asks what normalization would do, as
the fragility test in `py/mb_cmn/uni_norm_fragile.py` does, is fine." In
`doc/mam-normal-mark-order.md`, "**Never call `unicodedata.normalize` (NFC, NFD, any form) on
Hebrew.** When two strings that should match do not, put both through `give_std_mark_order`; do not
paper over it by normalizing." now reads the same, and the section heading has lost "— never run
NFC over them". Under the new wording none of the twelve calls conflicts with the rule: none
produces Hebrew that belongs in MAM's order, and the eight orders that the WLC-vs-UXLC report does
not show are the same text in both editions.

**Checks.** `git diff --check` passed. The suite ran on the edited tree, before this paragraph was
added, from 08:30 to 08:37 on 2026-10-07, New York time: 1,055 passed and 5 skipped, with 60
subtests passed and nothing failing. With this paragraph in place, the suite's ten tests that scan
tracked prose or the whole tree passed again: `test_prose_mark_order.py`,
`test_prose_conventions.py`, `test_h_dot_below_nfc.py`, `test_no_machine_paths_in_artifacts.py`,
`test_receipt_update_links.py`, `test_explicit_time_zones.py`, `test_review_turn_files.py`,
`test_sibling_reach.py`, `test_sigil_b2_not_a_sigil_anywhere.py` and `test_transliterations.py`.
The mega did not run: no generator reads `AGENTS.md`, `doc/mam-normal-mark-order.md` or this
file.

**Effective base State, 2026-10-07:** acted on, with nothing deferred: item 8.10 is resolved as
above, and every other item stands as the entries above record. The base report's line 3 stays as
written, and this update remains `State: open` while its base survives.

## The remediation's five noticed items, decided and fixed, 2026-10-07

Recorded by a Claude session (Claude Opus 5.5 in the Claude desktop app) on 2026-10-07, New York
time. It presented to Ben the five items of "Noticed while planning, not acted on" in the entry
"Remediation executed, 2026-10-07", re-measured at `08fcae33`; three read-only sub-agents measured
items 3 to 5, and the session re-checked their figures. At Ben's direction ("please don't use a
worktree; why not use GitRepos3 for example") it made its changes on `main` in the full clone
`C:/Users/BenDe/GitRepos3/MAM-basics`, brought to `origin/main` by a fast-forward-only forest sync.
The approved trial, `doc/review-trial.md`, governed verification: each commit had the focused checks
that its message records, and the mega and the full suite are left to the nightly run. Ben's words
are quoted verbatim; the option wording is the session's.

1. **Item 5, `DATA-LICENSES.md`: fixed in `c63019f6`.** Ben chose to add rows, then left the wording
   to the session: "I really don't care to get involved in license questions. Period. Just do what
   you think is best." Four rows cover near-Aleppo's dataset, its pages, its four crops and its
   build inputs. They name J. David Stark's Aleppo Codex index, CC BY 4.0, as the source of its
   coverage data, which `gh-pages/near-aleppo/coverage-and-status.html` now credits too. The font
   row counts sixteen copies, fifteen published. `out/near-aleppo/LICENSE.md` keeps its paraphrase
   of MAM's statement, which gives the attribution that the statement requires.
2. **Item 3, Phonetic MAM's `ססס` at MAM's shirah spacing: documented in `00c5adbb`.** Phonetic MAM
   has `ססס` at all 328 uses of `מ:ששש`, in the eight passages that MAM lays out in song form, and
   its other break rows agree with MAM-parsed's at all 23,202 verses. Ben: "I approve of your
   documentation of the triple shin versus triple samech issue, and I approve of changing this
   release to be phonetic ma'am." `Phonetic-MAM/README.md` has entry 10 and says "Phonetic MAM" in
   the 20 places where it said "this release" or "the release"; the data is unchanged.
3. **Item 4, the break-template rows of "Reading MAM-parsed-plus": fixed in `dec4b27f`.** The row
   that said "(primarily in D column)" renders on no page. The page's own row said that a break
   within a verse "takes the argument פסקא באמצע פסוק", which 94 of the 185 breaks in column E
   lack: the 78 `ססס` between the items of a list, which MAM's introduction says it has not tagged
   throughout; the 14 inside `מ:כפול`, tagged only in the strand where the break falls within a
   verse; and the two beside the inverted nuns of Numbers 10:35–36. Ben asked that the wording show
   "that this is not some arbitrary alternation", suggested "rules-based exceptions" and the list
   clause, asked for a bulleted list, and approved: "But yes, please apply the edit we're talking
   about. And I believe there were two other similar edits in comments in Python code. Please do
   those as well." The row gives the rule and its three exceptions as bullets, and the two strings
   that no page shows agree with it.
4. **Item 2, the runbook's `--sync-forest ROOT` row: fixed in `2929240b`**, a routine repair under
   the trial. The row names the skip of the calling session's own clone first, as
   `doc/clone-forests.md` and the code have it.
5. **Item 1, the unquoted placeholder commands: fixed in `2929240b`**, a routine repair. The two
   lines of `doc/PLAN-silluq-before-gaya-template.md` and the indented block at line 409 of
   `doc/PLAN-deferred-template-projection-decisions.md` begin
   `& "<home-clone>/.venv/Scripts/python.exe"`, item 9.22's form.

**Found while re-measuring, and fixed.**

1. `AGENTS.md`'s distributed-data list and `py/product_scopes.py`'s docstring omitted
   `out/near-aleppo/`; fixed in `2929240b`.
2. `py/main_0_mega.py`'s docstring and a comment said that the `near-aleppo-census` step was
   deleted, though a local census has run under that name since 2026-10-05; fixed in `2929240b`.
3. `DATA-LICENSES.md` had no row for `gh-pages/document.css`, `report.css`, `style.css` and
   `favicon.svg`, MAM-basics' own work; they take GPL-3.0 in `92dcc38a`, under Ben's licence
   delegation in item 1 above.

**Effective base State, 2026-10-07:** acted on, with nothing deferred: the five items noticed while
planning are fixed or documented as above. The base report's line 3 stays as written, and this
update remains `State: open` while its base survives.

## Archived receipt references, 2026-10-09

Recorded by Claude on 2026-10-09, New York time, in the cloud session that executed
workstream C of `doc/PLAN-maintenance-follow-up-2026-10-08.md`, after Ben approved its
deletion list and corrections that day. The base's "five lines in four dated records, which stay as written: four with the
comma form (`doc/PLAN-remediate-review-findings-2026-09-26.md:131`," cites a receipt since
retired from the tracked tree. It remains, with that line numbering, at
[September 26 remediation plan](https://github.com/bdenckla/MAM-basics/blob/38a8db9ae851b83d43b5c5ad42c007943b54d724/doc/PLAN-remediate-review-findings-2026-09-26.md),
with its [update](https://github.com/bdenckla/MAM-basics/blob/38a8db9ae851b83d43b5c5ad42c007943b54d724/doc/PLAN-remediate-review-findings-2026-09-26-update.md).
