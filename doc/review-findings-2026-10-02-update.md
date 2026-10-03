# Updates to the 2026-10-02 review of MAM-basics

State: open; first entry 2026-10-02.

Every entry here corrects or supplements `doc/review-findings-2026-10-02.md`, which is left as
written. Under `doc/dual-agent-review.md`, "Running a trial review", step 3, this file also holds
the trial's one disposition list, which covers that report and the Codex report,
`doc/codex-review-findings-2026-10-02.md`.

## The owner's disposition list, 2026-10-02

Recorded on 2026-10-02 by the trial's owner, the kickoff session: Claude Opus 5.5 at `max` in the
Claude desktop app, working in `C:/Users/BenDe/GitRepos2/MAM-basics`, with both reports on
`origin/main` at `09be20b3`.

**The two reports.** Both reviewed MAM-basics `7549ebf7..db59ef5e`, the kickoff's window, and both
treated item 4 of the kickoff section as evidence only. Both ran the suite (1,056 passed, 5
skipped, 60 subtests passed) and a clean 57-step mega. The Claude report, committed as `58df29bd`,
has 15 findings holding 67 items, 31 of them in its one-line finding 15. The Codex report, committed
as `09be20b3`, states that "No actionable introduced defect was established" and adds one wording
note. No finding appears in both reports, so every Claude item is a unique finding. Several Codex
statements bear on Claude findings. Each is settled as a conflicting claim, either in the
finding's entry or under "What the trial showed".

**How the dispositions were checked.** Six read-only sub-agents divided the Claude items among
them and re-derived every item from public evidence at `db59ef5e`. They read nothing in
MAM-private or hbofonts and wrote nothing in the repository, and they demonstrated mechanisms in
memory or on scratch copies wherever a finding asserts one. The owner checked finding 3's live
state directly, re-read the citations behind finding 4.4, and re-read the lines behind several
corrections adopted below. No item was refuted, though C15.1 is rejected. Sixteen carry a
correction to their wording, a figure, a citation or their reach, given in their entries.

**Ben's decision after kickoff.** Told that the full mega's `phonetic-mam-export` step reads
MAM-private through its adapter, Ben answered on 2026-10-02: "Thanks for pointing that out about
mega but I'll just let them do what they want. It seems harmless if we ignore the wasted time."
Both reviewers ran the full mega; it left no tracked diff.

**Defaults.** Every accepted finding is fixed later, in the remediation phase. Where a fix needs
Ben's choice, the remediation plan presents it with concrete wording. Of the 67 items:

1. 64 are accepted and unfixed;
2. one, finding 3, was fixed after the review;
3. one, finding 15.1, is rejected;
4. one, finding 14, is a question for Ben.

The two most consequential are C1, which will stop the next Wikisource refresh that changes MAM's
text, and C2, which puts 11 wrong fractions into `Yeivin-ITM/meteg-claims.json` and onto three
published Yeivin pages.

### The list

Claude finding `n` is cited as `C<n>`. The Codex report numbers none of its statements, so each is
cited by its report section.

1. **C1. Accepted, unfixed; lower risk, but it blocks the next text refresh.** A refresh that
   changes MAM's text changes the Phonetic MAM release, two gates then fail by construction, and
   no procedure says how to re-approve them. Verified:
   - Changing one release file's recorded hash, in memory, makes `claim_schema.pin_claims` raise
     while all 20 fractions stay equal to their approved values (C1.1).
   - A one-point change to a displayed chapter breaks the frozen legacy hashes that
     `test_complete_release_and_unified_projection` reads and no code writes (C1.2).
   - No tracked text gives a re-approval procedure, and `py/phonetic_mam/legacy_projection.py` has
     no importer and runs only against a legacy tree (C1.3).

   Codex checked only the current state, where both gates pass. Remedy notes: `Yeivin-ITM/README.md:75–78`
   states the whole-input pin as deliberate design, so narrowing it is Ben's choice. Regenerating
   the legacy oracle from the new renderer would make its test circular, and its original source can
   no longer be produced. A refresh made before remediation will stop the mega at
   `yeivin-itm-survey-meteg-claims`.
2. **C2. Accepted, unfixed; published pages and public data.** The meteg-before-stress survey
   classifies a one-chanted-word oleh-weyored, whose oleh and yored are on the same chanted word, as
   conjunctive. Its closed table selects the yored's U+05A5 as the primary accent, and the poetic
   conjunctive list holds U+05A5 as merkha. Verified independently, the survey rebuilt in memory
   reproducing all 6,119 records:
   - exactly 13 records, all in poetic verses of Psalms, are affected, as the report lists them;
   - accgram's poetic scanner reads all 13 as the disjunctive `OLEH_WEYORED`;
   - reclassifying them changes exactly 11 of the 20 pinned fractions, every value as the report
     gives it;
   - no record is misclassified the other way.

   Corrections: on `gh-pages/yeivin-itm/yeivin_itm-318_344.html` the affected lines run to 557, not
   553, because the FR3 figure at line 556 changes as well. Two printed roundings change: "about 7%"
   becomes "about 5%" for FR3, and "about 29%" becomes "about 28%" for FR1. The legacy page printed
   "about 28%" before Ben's approved correction to 29%.

   Codex ("What verifies sound", Yeivin ITM) calls the revised claim "supported by the public
   analysis and mechanical claim check"; that is a reproduction check and does not test the
   classification.

   Remedy notes:
   - Key the exception on an oleh before the final U+05A5 in the accent vector, so that it covers
     all three table shapes.
   - Keep U+05A5 in the poetic conjunctive list, where an ordinary merkha belongs.
   - Do not substitute the scanner's tokens wholesale; that would misclassify 25 records that the
     survey gets right.
   - Handle or refuse a yored whose oleh is on the previous chanted word. There are 17 such, none a
     candidate today.

   A fix changes the approved input hash and the pins, so the corrected prose is Ben's to approve
   in remediation.
3. **C3. Fixed after the review, by a deployment rather than a commit.** The live user-level files
   lagged `4f4cbb66` and `d0c660c9` when the reviewer checked, at 15:24 and about 15:50 New York
   time. They were rewritten at 16:21:04 New York time on 2026-10-02, and
   `py/main_repo_util.py --sync-user-config --check` at `09be20b3` reports
   `USER_CONFIG_PROBLEM_COUNT=0`. The residue phonetic-hbo clone that the report's open end 6 names
   remains Ben's decision.
4. **C4.1. Accepted, unfixed; reader-facing document.** `DATA-LICENSES.md:88` links the font's
   licence at a path inside the private hbofonts repository, against the 2026-08-27 rule that
   `in/repo_maintenance_policy.json` records. The same text is public as
   `in/font-support/taamey-d-0.921/FONT-NOTICE.txt`. Introduced by `066eb650`. Owner's notes:
   - the Claude report repeats that path;
   - two older documents also name hbofonts file paths: `doc/windows-long-paths.md:131–137` and
     `doc/PLAN-checkout-kinds-and-portable-knowledge.md:261`;
   - a replacement link into the public `bdenckla/Taamey_D` must name a path that exists at the
     commit it cites.
5. **C4.2. Accepted, unfixed; published pages and a reader-facing document.** `DATA-LICENSES.md:88`
   states GPL v2 duties for all fourteen tracked copies of `Taamey_D.woff2`. Only the two new
   products' `woff2/` directories hold the notice, the licence text and the source pointer.
   Corrections:
   - the every-copy coverage predates the window: `9cf48863`, on 2026-09-08, said twelve copies;
   - `066eb650` added the GPL v2 terms and the duties sentence;
   - the count of fourteen came with the merge `9a67d51b`;
   - the two landing pages link `woff2/SOURCE.txt`, not `FONT-NOTICE.txt`.

   Remedy note: the `../../font-sources/` path in `PRODUCT-WOFF2-SOURCE.txt` is wrong for the four
   deeper directories.
6. **C4.3. Accepted, unfixed; distributed data and a reader-facing document.** `Phonetic-MAM/` and
   `Yeivin-ITM/` have no `LICENSE.md`. `DATA-LICENSES.md` assigns no terms to their READMEs, to their
   `schema/` directories, or to the six notice files beside their fonts. Addition: a third closed
   file set, in `py/yeivin_itm/claims.py:17–26`, would also reject a `Yeivin-ITM/LICENSE.md`.
7. **C4.4. Accepted, unfixed; reader-facing document; any change is Ben's.**
   `MAM-with-doc/LICENSE.md:3–4` extends the CC-BY-SA statement over `gh-pages/MAM-with-doc/`. That
   tree also holds third-party crops and four Taamey D copies, which `DATA-LICENSES.md:96–97`
   excepts. Correction: Ben's approval is recorded at
   `doc/PLAN-remediate-review-findings-2026-09-29.md:186–187`; the cited `:540–550` holds the
   proposed wording.
8. **C4.5. Accepted, unfixed; lower risk; which modules count as adaptation is Ben's call.** The
   GPL exclusion of `py/yeivin_itm/content/` covers six modules of rendering code, 637 lines in all,
   and the GPL-3.0 renderer and helpers import five of them. Owner's notes: `py/yeivin_itm/substitutions.py` imports
   two more content modules, and all six modules are hash-pinned in
   `in/yeivin_itm_legacy_differential.json`, so moving them breaks those pins.
9. **C4.6. Accepted, unfixed; reader-facing document.** `DATA-LICENSES.md:58` puts the passage from
   Yeivin's separate 1968 study under the permission for the 1980 book, and the repository records
   no permission or rights holder for the 1968 work. The passage is a source comment rendered on no
   page.
10. **C4.7. Accepted, unfixed; reader-facing documents.** `README.md:114–117` and
    `DATA-LICENSES.md:5–11` place all of `doc/` under GPL-3.0. That reaches
    `doc/wikisource-dagesh-discussion-2026-10-01.mediawiki`, a CC BY-SA 4.0 capture, and its
    translation. Wording correction: the source is a section of the Wikisource
    Village Pump, ויקיטקסט:מזנון, not a talk page.
11. **C4.8. Accepted, unfixed; reader-facing document.** The root README's "Product and corpus
    directories" omits `Phonetic-MAM/`, `Yeivin-ITM/` and their entry points.
12. **C5.1. Accepted, unfixed; distributed data and its README.** `Phonetic-MAM/README.md` does not
    say how the release departs from MAM's written text:
    - it shows only the qere at perpetual-qere sites;
    - it has no extraordinary points;
    - it uses the second parameter of the stress-helper templates;
    - it keeps varika;
    - it writes Latin vowel marks decomposed.

    Corrections:
    - The display has only the qere at 7,710 chanted words, not 7,706, and folds one more at
      Deuteronomy 32:6. The report's join key missed four gray-maqaf compounds that contain the
      Tetragrammaton.
    - Only U+05C4 is guarded against, not U+05C5, though the release holds neither.
    - "Explained nowhere" is too strong. Older comments in `py/accgram/post_stress_meteg_model.py`
      and `py/tests/test_final_stress_vs_phonetic_mam.py` say that the join keys drop the points.
    - "Generic" is the codebase's term for un-annotated Hebrew, so the defect is the README's
      silence, not the word.
13. **C5.2. Accepted, unfixed; distributed data and published pages.** The release lacks MAM's
    qamats alternative at 2 Kings 22:1. At 2 Chronicles 25:17 it shows an atom with the ketiv's final
    kaf and the qere's points. Neither the README nor the schema discloses either. Independent
    recounts agree:
    - 23,200 of 23,202 verses agree with MAM-simple;
    - 2 Kings 22:1 is the only one of the 357 verses with a qamats template that lacks
      qamats-labelled readings.

    Nuance: MAM's own note at 2 Chronicles 25:17 reports that the Aleppo Codex has לְךָ֖ with no qere
    note. The displayed atom is therefore the form MAM's apparatus attributes to that manuscript;
    the manuscript itself was not consulted. Not re-derived: that the current exporter reproduces
    the omission, which needs the private adapter. This bears on the September 29 round's deferred
    finding 22.
14. **C6.1. Accepted, unfixed; published page; the intended verse is Ben's to confirm.**
    `gh-pages/yeivin-itm/yeivin_itm-207_285.html` cites "2K 52:1", a verse that does not exist, from
    `py/yeivin_itm/content/my_yeivin_sec_239.py:8`. The citation was inherited from phonetic-hbo's
    page and is deployed. Corrections:
    - The list holding it is Is 19:19, 2K 10:30, 2K 52:1 and Ho 2:5, so its neighbours are not all
      from Isaiah.
    - The 17 pages carry 715 distinct references, 717 counting two found only in visible text, not
      807. Every one was checked, and this is the only one that names no verse.

    MAM evidence for the intent: of MAM's 25 atoms spelled ירושלם with pashta, Isaiah 52:1's is the
    only one numbered 52:1. Confirming it needs Yeivin's printed text, which only private OCR holds,
    and the correction cannot pass the tests until C6.2 is settled.
15. **C6.2. Accepted, unfixed; lower risk; whether to keep the migration gate is Ben's decision.**
    Nothing documents how to edit the "editable adaptation", and `py/tests/test_yeivin_itm.py`
    freezes it against the legacy pages. A simulated correction of C6.1 fails at the hard-coded set
    of changed pages (`:46`) and at the example comparison (`:82`). Correction: no instruction file
    addresses editing the adaptation, so the reach is the tests and the "editable" claim in two
    documents, not agent instructions.
16. **C7. Accepted, unfixed; lower risk; instructions for an outward-facing act.**
    `py/ws/pywikibot-setup.md:72–77` gives `--no-save`'s behaviour to `--identity-run`, which is a
    null bot and cannot fail on a change; older than the window. Remedy note: the rewritten guide
    should say two things:
    - that `--no-save` is expected to exit non-zero before a save;
    - that it checks idempotence only for edit kinds that are idempotent.
17. **C8. Accepted, unfixed; lower risk.** Once step 1's commit exists, the mega writes the
    change-log diff, and the dependent refresh's step 4 commits it. Step 5's stop rule then fires on
    a correct refresh. This is older than the window. Ben chooses the fix in remediation: holding the
    change-log paths back at step 4, or accepting an already-committed log that `--check` confirms.
18. **C9.1. Accepted, unfixed; lower risk; see question 2.** On Windows, routine maintenance stops
    at its first step after any suite run: the plain `shutil.rmtree` in `_clean_one_novc` fails on
    read-only Git objects under `.novc/t`. The failure was reproduced on a copy. The read-only files
    come only from the two relay test modules, which are evidence here, and the wipe is older than
    the window. `--skip-novc` bypasses the step. Remedy note:
    `py/tests/test_worktree_retirement_policy.py:143–165` pins the form of this call, so adding an
    error handler means changing the lint with it.
19. **C9.2. Accepted, unfixed; lower risk; see question 2.** `ruff check py` reports 17 errors: 13
    from `9a67d51b`, 3 from `a0016209`, and one F841 from `2e120b85`, in a relay test file. The
    import order in `py/phonetic_mam/compute.py` is deliberate, so its eleven E402 want a `noqa` or a
    per-file ignore. Codex ran no lint.
20. **C9.3. Accepted, unfixed; lower risk.** `--sync-forest`'s write form refuses the calling
    session's own clone and exits 1. Correction: this holds for a Claude session, whose session
    record marks its clone occupied, but not for every agent; the Codex reviewer's own run reported
    zero problems. Older than the window.
21. **C9.4. Accepted, unfixed; lower risk; introduced in the window.** The forest launch lint checks
    that a bound keyword is present, not that it bounds, so `timeout=None` passes. It also misses
    relative imports, against its docstring; synthetic sources demonstrated both. Today's launches
    are bounded. This goes beyond Codex's "No substantive introduced defect" for subprocess bounds.
22. **C9.5. Accepted, unfixed; lower risk.** Cross-volume `.novc` relocation removes its source with
    the same plain `rmtree`. On read-only files it stops partway, leaving a state that
    `_reconcile_relocations` refuses; this was reproduced at function level. The default
    same-volume path is unaffected. The code is older than the window, and the window makes the case
    easier to reach.
23. **C10.1. Accepted, unfixed; lower risk.** Help text and comments still say that the
    post-stress-meteg survey needs MAM-private and is skipped in the cloud. The survey ran with no
    MAM-private and in a simulated cloud environment, and reproduced the tracked output. Addition:
    `py/tests/test_redirect_manifest.py:39–40`, "Like that module, it asks
    `graphviz_pin.in_cloud_session()`", is stale too.
24. **C10.2. Accepted, unfixed; lower risk.** `doc/phonetic-mam-preparation.md:7–8` and `:77–79` still
    call deployment and the legacy redirect cutover future steps. In fact, the Pages run for
    `38c0116f` finished at 15:39:45 New York time on 2026-10-01, and phonetic-hbo's redirects from
    `2ca51088` deployed at 17:10:52 New York time that day. Addition: `:52`, "live deployment still
    requires its own checks", is stale as well. No tracked record shows a live URL check after
    deployment, so a fix should not claim one. Codex's wording note calls the sentences ambiguous;
    the evidence supports this finding, because the commit that wrote them deferred both steps
    explicitly.
25. **C10.3. Accepted, unfixed; lower risk.** `hebrew-prose`'s `references/sources-and-corpora.md:70–72`
    says the old private Yeivin copy remains, while a tracked record says that private integration
    removed it. Correction: the skill asserts that the copy exists; it does not send readers to it.
    The eighth al-hatorah citation site that `references/mam-basics.md` counts no longer exists.
26. **C10.4. Accepted, unfixed; lower risk.** The docstrings of `py/product_scopes.py` and
    `py/tests/test_product_scopes.py` say five products where the tuple has seven. Addition: the
    product list in `AGENTS.md:157–158` has a stray "and".
27. **C11. Accepted, unfixed; reader-facing documentation and a lint's record; what the graph
    depicts is Ben's decision.** The pipeline graph draws 12 of the mega's 57 steps and none of the
    five new ones. It also draws four programs that the mega does not run, and nothing compares it
    with the step table. Corrections:
    - the split between mega steps and external prerequisites exists only as comments in
      `pipeline.dot`; the SVG marks nothing;
    - the root README's "Core pipeline" itself includes `py/main_mam4sef.py` and
      `py/main_mam_osis.py`, so the charge holds against the `.dot` and the coverage lint's reliance
      on it, not against the README; `osis_split_mapm` is wrong under any framing;
    - `dd4f85df` added only the bot's edge to plus.
28. **C12.1. Accepted, unfixed; lower risk.** The pre-write check that plus holds no parser-stage
    encoding recognizes only `stmpl`. Injected `tmpl` nodes and custom tags pass, both in a cell and
    inside a parameter. Citation correction: custom tags are at `py/mb_cmn/ws_tmpl1.py:87–89`;
    `:54–56` and `:108–119` support only the `tmpl` claim. The check is older than the window, and
    `41d73299`'s remediation of it was incomplete.
29. **C12.2. Accepted, unfixed; lower risk.** `test_meteg_before_stress` has no independent oracle,
    and no tracked record supports the docstring's claim that the classifier preserves the existing
    algorithm. C2 is what that cost.
30. **C12.3. Accepted, unfixed; lower risk.** `py/tests/test_phonetic_untangler_preparation.py` has
    two problems:
    - an example-based fault-injection test for which `AGENTS.md` declares no exception;
    - an equality check that can fail only if the dispatch wiring breaks. The file-access half of
      that test is a real check.
31. **C12.4. Accepted, unfixed; lower risk; latent.** `_written_stress_helpers` skips every element
    other than the two stress-helper templates without raising on an unknown one. It never indexes
    the 68 nested stress helpers. All 378 `snapshot_before_qere` fields are unchanged. A closed fix
    must name, for each container template, which parameter and which alternative to index, and
    that policy is Ben's choice.
32. **C13.1. Accepted, unfixed; lower risk.** One undecodable byte ends the compute stream and drops
    replies already owed, against the promises in `doc/phonetic-mam-compute.md`. Reproduced by
    subprocess.
33. **C13.2. Accepted, unfixed; published pages; low.** The Ashkenazic display switches only through
    the CSS `:has()` selector, with no fallback. A browser without it shows Sephardic transcriptions
    under an Ashkenazic label. Confirmed from code; no browser was run.
34. **C14. Unresolved question for Ben; see question 1.** Correction: the report's counts, 385,991
    U+0301 and 73,384 U+0306, cover `Phonetic-MAM/data/` alone. The published pages hold 386,313 and
    73,384, in 933 of their 974 HTML files.
35. **C15, the one-line items.** Each is accepted and unfixed unless the table says otherwise.

    | Item | Disposition | Owner's note |
    |---|---|---|
    | 15.1 | Rejected | The text is as quoted, but both procedure documents carve out the trial explicitly: `doc/periodic-review.md:12–16` and the trial text of `doc/dual-agent-review.md`. So no rule conflicts, and Codex's "The trial's precedence clause resolves the retained older review procedures" holds. |
    | 15.2 | Accepted | The same miss recurs at `doc/PLAN-remediate-review-findings-2026-09-26.md:621` and `:728`. |
    | 15.3 | Accepted | Older than the window; neither program can crash. |
    | 15.4 | Accepted | Only lone surrogates could now raise. |
    | 15.5 | Accepted | An older claim, kept by `d54e12df`. |
    | 15.6 | Accepted | Older than the window. Recounted: 113 tilde-joined readings and 12 prose non-joins. |
    | 15.7 | Accepted | A distributed product's README. |
    | 15.8 | Accepted | A published page. Inheritance from phonetic-hbo is unverifiable, and MAM-with-doc's index, older, has the same link. |
    | 15.9 | Accepted | |
    | 15.10 | Accepted | The 11-of-17 distribution is inherited. |
    | 15.11 | Accepted | The support files match their recorded hashes today. |
    | 15.12 | Accepted | Git's content detection treats both zips as binary today. |
    | 15.13 | Accepted | |
    | 15.14 | Accepted | JSON Schema does not require `$id` to resolve. Changing it changes the schema's identity, which is Ben's choice. |
    | 15.15 | Accepted; Ben's call | Correction: `hebrew-prose` is inconsistent here. Its `SKILL.md` item 7 states the rule generally. `references/rendered-prose.md` and the SCOPE paragraph of `printed_decalogue_strands.py` limit Hebrew strand names to the printed-Decalogue pages, and the published methods page already romanizes these branches. So this is not a clear violation. |
    | 15.16 | Accepted | |
    | 15.17 | Accepted | The description's "reads" half also omits the font inputs. |
    | 15.18 | Accepted | Confirmed from code. |
    | 15.19 | Accepted | Correction: an adapter that dies early reports "source adapter ended early or exceeded its book limit"; "source adapter failed" appears only on a nonzero exit after every book. |
    | 15.20 | Accepted | |
    | 15.21 | Accepted | |
    | 15.22 | Accepted | |
    | 15.23 | Accepted | Correction: the pointer once covered the general test-shape rule. Placed after the two exceptions, it reads as covering them, and for them it is false. |
    | 15.24 | Accepted | |
    | 15.25 | Accepted; Ben's call | The count of five is a framing Ben chose on 2026-08-27. |
    | 15.26 | Accepted | Addition: a Git operation in progress also fails the check form, and the list omits it. |
    | 15.27 | Accepted | |
    | 15.28 | Accepted | Older than the window; not a regression. |
    | 15.29 | Accepted; Ben's call | Correction: Ben approved `cb5bcda1`'s census fixes on 2026-10-01, so whether those two Holman records are receipts is his decision. "Recorded by" is a house convention, not a rule, and the other dated entry by `d0c660c9` has it. |
    | 15.30 | Accepted | |
    | 15.31 | Accepted; Ben's call | 13 comment lines in 6 modules link 9 issues. The tracker's privacy rests on the reviewer's metadata query. What replaces the links is Ben's call. |

**Not findings.** The Claude report's six items noticed outside the diff and its seven declared open
ends get no disposition. Its opening discloses read-only departures from the rules, among them a
read of a licence file in the private hbofonts clone; nothing in this list relies on what was read
there. During verification, the meteg checker noticed one more thing outside the window. accgram's
fusion across chanted words misses the oleh-weyored at Psalms 44:4: the scanner writes that
chanted word's geminate dagesh as U+05C4, which the oleh-to-yored pattern
(`py/accgram/poetic_scanner.py:102–108`) refuses. No record of either survey is affected.

### What the trial showed

1. **The two reviews hardly overlapped.** Codex reported no findings and Claude 67 items, so no
   finding was shared. The two reports applied different bars:
   - the Codex report counted only actionable defects that the window introduced;
   - the Claude report also counted defects older than the window that the window carries forward,
     and it recorded minor items in one line each.
2. **Codex's conflicting statements were reproduction checks.** Wherever a Codex "verifies sound"
   statement bore on a Claude finding, it described a reproduction or preservation check: true as
   stated, but not a test of correctness. The evidence favoured the Claude finding on C1, C2, C5,
   C9.1, C9.2, C9.4, C10.2, C13.1 and C13.2, and the Codex statement on C15.1.
3. **The owner's verification changed the record.** No item was refuted, but 16 needed a
   correction, among them two counts (7,710 for 7,706; 715 for 807), a reach, a citation, and the
   page location of a published figure.
4. **The kickoff prompt's checkout guard worked.** The Claude reviewer's session opened in the
   owner's clone; the guard stopped it, and Ben moved it before any work.

### Proposed procedure changes, for Ben's approval

Ben approved all three on 2026-10-03, and they were applied that day; see "Ben's close-out
decisions, 2026-10-03" below. Each changes `doc/dual-agent-review.md`, "Running a trial review".

1. **Correct a kickoff sentence.** In step 3, replace "Agreement between the two reports is not
   itself evidence, and an owner who wrote one of the reports checks its own claims against the
   evidence rather than against its report." with "A finding that both reports make needs no further
   check unless their accounts differ, and an owner who wrote one of the reports checks its own
   claims against the evidence rather than against its report." The replaced sentence, written at
   kickoff, contradicts Ben's step 2, which asks the owner to check unique findings and conflicting
   claims.
2. **One reporting bar for both reviewers.** In step 1, after "It offers no view of the window's
   content.", add "Both prompts set the same reporting bar: defects that the window introduced, and
   older defects that the window carries forward or that the reviewer notices, each labelled as one
   or the other, with each minor wording item in one line." This addresses what the trial showed
   in its first point.
3. **Prompts name the private repositories.** In step 1, replace "and the reviewer's checkout,
   output path, line-3 `State:` and effort level." with "the reviewer's checkout, output path,
   line-3 `State:` and effort level, and the private repositories it must not read, as
   `in/repo_maintenance_policy.json`'s `repo_visibility` lists them." Reason: the Claude reviewer's
   stream brief misclassified hbofonts as public, and two streams read in it before the error was
   caught.

### Questions for Ben

Ben answered all three on 2026-10-03; see "Ben's close-out decisions, 2026-10-03" below.

1. **Finding 14, decomposed Latin vowel marks in Phonetic MAM.** There are two options:
   - keep the release's decomposed acute and breve vowels as the legacy bytes, as the exemption
     that `9a67d51b` wrote does;
   - compose them to NFC, which changes the published pages, C1.2's frozen legacy oracle and
     `py/phonetic_mam/analysis_reader.py`.

   Which?
2. **The relay software, behind C9.1 and C9.2.** C9.1's maintenance failure comes only from the
   relay test modules' read-only Git objects, and C9.2's F841 is in a relay test file. Should this
   remediation retire the relay, removing both causes, or fix both in place and leave the relay for
   later?
3. **The three procedure changes above.** Approve all three, some, or none?

## Ben's close-out decisions, 2026-10-03

Recorded on 2026-10-03, at about 01:00 New York time, by the trial's owner, the kickoff session.
Ben answered close-out step 1's questions in the desktop app's dialog, which put four questions:
the three above, and first, whether he approved the list as the close-out package. His selections,
verbatim:

1. **The package: "Approve as listed (Recommended)".** Ben approved the disposition list above as
   the close-out package. The 64 accepted findings are fixed later, in remediation; C3 stands as
   fixed and C15.1 as rejected. The approval records dispositions only. It does not execute
   remediation, and it does not approve wording that the remediation plan must present under
   `doc/periodic-review.md`, "Separate defects from editorial proposals", in particular C1's gate
   design and C2's corrected Yeivin prose.
2. **Finding 14: "Keep the legacy bytes".** C14 is resolved with no change to the release, the
   pages or `py/phonetic_mam/analysis_reader.py`. The decomposed acute and breve vowels of
   `Phonetic-MAM/` and `gh-pages/phonetic-mam/` stay as the legacy bytes, and the exemption at
   `py/tests/test_h_dot_below_nfc.py:191–195` is now Ben's decision of 2026-10-03. Remediation
   cites this decision at the exemption, so that a later review does not raise the forms again.
3. **The relay: "Retire the relay now".** The remediation adds the retirement of the automated
   dual-agent review relay. That covers its code, tests, runbook, plan, configuration, agent file
   and deployed copy, its registered scheduled task, and the procedure text that describes it.
   The retirement removes C9.1's trigger, the relay tests' read-only Git objects, and C9.2's F841,
   which is in a relay test file. The plan settles three further points:
   - whether C9.1's plain `rmtree`, and C9.5's, still need an error handler once the trigger is
     gone;
   - how the relay's historical round records are kept;
   - each act the retirement needs outside the repository, such as unregistering the scheduled
     task and removing the deployed agent file, named separately so that each can be authorized
     on its own.
4. **The procedure: "1: fix the kickoff sentence,2: one reporting bar,3: name private repos".**
   All three proposed changes were applied to `doc/dual-agent-review.md`, "Running a trial
   review", with the wording proposed above, in the commit that records this entry. Step 1's
   paragraph was rewrapped as well.

**Next: close-out step 2.** A fresh-task remediation plan, with concrete editorial wording and
presented by public-facing risk, now including the relay's retirement. Later State and the
remediation's dispositions are recorded in this file.

## Remediation plan prepared; approval pending, 2026-10-03

Recorded on 2026-10-03 by the close-out step-2 session: Claude Opus 5.5 at `max` in the Claude
desktop app, on the machine `LAPTOP-DBLE8UKA`, working in `C:/Users/BenDe/GitRepos2/MAM-basics` on
clean `main` at `644a6c9c` after a fetch. The session worked from a prompt that the trial's owner
session wrote on 2026-10-03 and Ben pasted in; the prompt quotes Ben's instruction that started the
review and his selections recorded above, and is otherwise the owner session's reconstruction. Eight
read-only sub-agents gathered the evidence; the session verified what the plan rests on.

**The plan** is [`PLAN-remediate-review-findings-2026-10-02.md`](PLAN-remediate-review-findings-2026-10-02.md),
State "live". It covers the 64 accepted items, the citation of Ben's finding-14 decision at the
exemption in `py/tests/test_h_dot_below_nfc.py`, and the relay's retirement. It presents the changes
in `doc/periodic-review.md`'s risk order: published pages and distributed data, then reader-facing
documents, then the rest. It keeps reproducible defects apart from editorial proposals, with current
and proposed wording for each; names eleven acts outside the repository, A0 to A10, which were
separate authorization points until Ben authorized them in advance (next entry); and orders the work
in waves with their checks and the integration sequence. It executes nothing.

**Found while planning:**

1. **The relay ran on another machine.** The scheduled task, the dispatcher's registry and evidence,
   the three locked worktrees and their branches are, by the tracked records, on the machine that
   ran the relay, which those records do not name. They are not on `LAPTOP-DBLE8UKA`, whose
   GitRepos2 clone dates from 2026-09-29 and never held a relay commit. Only the deployed agent file
   is on both. The plan's acts outside the repository are written for that.
2. **C9.1's trigger outlives the relay.** Read-only Git objects remain under every clone's `.novc/t`
   from relay tests already run, and agent scratch repositories in a `.novc` add more, so C9.1's and
   C9.5's error handler is still needed.
3. **Four of the notes above are inexact,** and the plan uses the corrected figures:
   - C10.3: `9a67d51b` removed five of the eight al-hatorah citation sites, not one; three remain.
   - C12.2: the "25 records that the survey gets right" hold only for `Reading.scanner_word()`
     input; with the plain displayed Hebrew, 18 disagreements remain after C2's fix.
   - C15.25: on 2026-08-27 Ben deferred the framing and that session kept "Five"
     (`97b559b0`); the choice now stays Ben's, as the list says.
   - C2: the last changed line of `yeivin_itm-318_344.html` is 556; line 557 ends the FR3 sentence
     unchanged.

**What waited for Ben,** until the next entry: his approval of the plan's wording and execution, and
the thirteen choices in its "Choices for Ben": C2's corrected prose; C6.1's intended verse; C15.15;
C4.4; C4.5; C11; C1's gate design; C6.2; C8; C12.4; C15.25; C15.29; and C15.31. Until C1 lands, a
Wikisource refresh that changes MAM's text still stops the mega at `yeivin-itm-survey-meteg-claims`.

## Ben's choices and advance authorization, 2026-10-03

Recorded on 2026-10-03, at about 09:30 New York time, by the close-out step-2 session that prepared
the plan, after `286d2e8c` pushed it. Ben's words in that session, verbatim: "Regarding my choices, I
accept all your recommendations. Are there any choices for which you had no recommendation?" The
session then named six items for which the plan stated no recommendation, recommended one course for
each, and said that accepting them would not authorize the acts outside the repository in advance.
His reply, in one message: "I accept all those recommendations as well." and "Please authorize those
acts in advance. I want this all to be as unattended as possible."

1. **The thirteen choices:** the recommended option of each, which the plan's "Choices for Ben,
   answered 2026-10-03" names: C2's figures-only correction, keeping "roughly"; "Is 52:1" for C6.1;
   option 1 for C15.15, C4.4, C4.5, C8, C12.4, C15.25, C15.29 and C15.31; option 2 for C11; Gate B
   and Oracle A for C1; and option C for C6.2.
2. **The six further items:** the flagged addition under C15.13 is made; A5, A8, A9 and A10 are
   done; A6 is not, so `origin/dar-2026-10-01` stays.
3. **The acts outside the repository, A0 to A10, are authorized in advance,** read as all of them,
   since Ben asked for everything to be as unattended as possible.

**The plan, revised to match in the commit that records this entry**
([`PLAN-remediate-review-findings-2026-10-02.md`](PLAN-remediate-review-findings-2026-10-02.md)):
its State; "Decisions this plan follows", item 4, which quotes Ben; an "Unattended" rule in the
executor contract; the chosen option named in the ledger, the waves and the expected outputs; C2's
prose and C15.13's addition marked approved; a read-only visibility check of `bdenckla/trope` before
C15.31's label is used; "Final integration" and "Records" reordered for an unattended run; and "Acts
outside the repository" rewritten as authorized, with a new section, "The relay-machine session". In
that rewrite the acts changed only toward caution. No act deletes anything: A2 and A8 move the agent
file and the rehearsal home into the retention folder `$HOME/relay-retirement-2026-10/`, since a
plain deletion would be permanent and a recycling without confirmation dialogs can delete
permanently a folder too large for the Recycle Bin. A7's selection is spelled out, and A9 is left to
Ben in the Codex app, since the plan has no verified command that deletes a Codex follow-up.

**What remains for Ben:** starting the executor's session on `LAPTOP-DBLE8UKA`, and after its final
integration, the relay-machine session on the relay machine, with the prompt in the plan's section
of that name; deleting the paused Codex follow-up in the Codex app if it is still listed (A9); and
deleting `$HOME/relay-retirement-2026-10/` on a machine whenever he wants the space.

## Remediation implemented; final gates pending, 2026-10-03

Recorded by Claude Opus 5.5 on 2026-10-03, New York time, in the executor session of the
remediation plan: Claude Opus 5.5 at `max` in the Claude desktop app on `LAPTOP-DBLE8UKA`. It worked
from a prompt that the plan-preparing session wrote on 2026-10-03 and Ben pasted in; that prompt
quotes the three instructions of Ben's that "Ben's choices and advance authorization, 2026-10-03"
records, and is otherwise that session's reconstruction, which this session checked against the
plan and the tree. **Implemented: every row of the plan's "Finite execution ledger" that the
repository holds**: R1 to R7, the 64 accepted items, and the citation of Ben's finding-14 decision,
in waves 0 to 8 as the plan orders them, apart from the departures listed below. The full suite
passed at `7bd5ee8c`, after the last executable change: 1,047 tests passed, with 5 skipped and 60
subtests passed. Pending: final integration, meaning the merge of the current `origin/main`, the
mega and the push of `main`; acts A3, A2 and A10 on this machine; the closing records; and then
the relay-machine session.

**Checkout and baseline.** The development and integration checkout is the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics` on `LAPTOP-DBLE8UKA`, on the branch
`remediate-review-2026-10-02`. Editing began there at `074af13a78789ffe8c6c3b1cc88b13aa3d422da2`,
equal to `origin/main` after a fetch, with the tree clean and `644a6c9c`, `286d2e8c` and `074af13a`
ancestors of `HEAD`. Wave 0's `cbd405b11ef990040031ccf19699db54a69a489d` is the archive commit, the
last whose tree holds every file that the relay's removal deleted, and
`4573b0070be6eab2d31257a1cdf766b60ae766af` is the removal commit. Each of the 40 commits before this
entry was pushed to `origin/remediate-review-2026-10-02` as soon as it was made, never forced. This
session was the only writer. The plan-preparing session's session record also named this clone;
`HEAD` was verified before every commit and moved only by this session's commits.

**Ben's thirteen answers, as implemented,** numbered as the plan's "Choices for Ben, answered
2026-10-03" numbers them:

1. C2's corrected Yeivin prose: the figures-only correction, keeping "roughly", in `c17de175`.
2. C6.1's intended verse: "Is 52:1", on MAM's evidence, in `f2774cea`. Yeivin's printed text was
   not read.
3. C15.15: option 1, in `7bd5ee8c`. No file under `Yeivin-ITM/` changed.
4. C4.4: option 1, the exception in `MAM-with-doc/LICENSE.md`, in `007f9f31`.
5. C4.5: option 1, the six rendering-helper modules declared GPL-3.0 code, in `007f9f31`.
6. C11: option 2, the core pipeline that the root README names, marked and linted, with the floor
   fix, in `8ad4c1d2`.
7. C1: Gate B and Oracle A, in `a363e5ce`.
8. C6.2: option C, in `59e41a99`.
9. C8: option 1, in `d875e0b1`.
10. C12.4: option 1, in `4039acd3`.
11. C15.25: option 1, in `7bd5ee8c`.
12. C15.29: option 1, in `b7f7e204`.
13. C15.31: option 1, in `d1d8d1ce`, after `gh repo view bdenckla/trope --json visibility` printed
    `PRIVATE`.

Of the six further items, C15.13's flagged addition is made, in `1ad77de0`. A10 falls to final
integration, A5 and A8 to the relay-machine session, and A9 to Ben; A6 is not done.

### Dispositions of the ledger's rows

| Item | Execution disposition |
|---|---|
| C1.1 | Implemented in `a363e5ce`: Gate B, with `Yeivin-ITM/README.md`. |
| C1.2 | Implemented in `a363e5ce`: Oracle A, with `in/phonetic_mam_legacy_projection_inputs.json` and `Phonetic-MAM/README.md`. |
| C1.3 | Implemented in `a363e5ce`: `py/phonetic_mam/legacy_projection.py` removed, and the refresh procedure's text, in wave 3 rather than wave 6 (departure 3); `d875e0b1` keeps its pointer. |
| C2 | Implemented in `c17de175`: the classifier, the survey, the claims, the pins and the three pages. |
| C4.1 to C4.8 | Implemented in `007f9f31`, with every `DATA-LICENSES.md` change in one sequence. |
| C5.1 | Implemented in `82235e8c`, with the U+05C5 guard. |
| C5.2 | Implemented in `82235e8c`, with the finding-22 pointer in the September 29 update; the sentence that the plan adds to it if this remediation's mega leaves `Phonetic-MAM/data/BD-2Kings.json` unchanged waits for that mega. |
| C6.1 | Implemented in `f2774cea`, with the reference lint and the README clause that wave 2 held back (departure 1). |
| C6.2 | Implemented in `59e41a99`. |
| C7 | Implemented in `6c303371`. |
| C8 | Implemented in `d875e0b1`. |
| C9.1 | Implemented in `a1c4a746`. |
| C9.2 | Implemented: the F841 by the relay's removal, `4573b007`; the three content-module findings in `88f35055`; the eleven E402 by C15.18, in `38cf30ea`; and the two unused imports in `e2d71ac7`. `ruff check py` reports "All checks passed!". |
| C9.3 | Implemented in `00974386`. The write form was not run against a real forest. |
| C9.4 | Implemented in `936d7b45`. |
| C9.5 | Implemented in `a1c4a746`. |
| C10.1 | Implemented: item 8 in `db700ec6`, items 1 to 7 and 9 in `41196f57`. |
| C10.2 | Implemented in `1ad77de0`. |
| C10.3 | Implemented in `7bd5ee8c`. |
| C10.4 | Implemented in `9595d3aa`. |
| C11 | Implemented in `8ad4c1d2`. |
| C12.1 | Implemented in `1c42c5b1`. |
| C12.2 | Implemented in `c17de175`. |
| C12.3 | Implemented in `ac25adc9`. |
| C12.4 | Implemented in `4039acd3`; `out/accgram/post-stress-meteg.json` is unchanged. |
| C13.1 | Implemented in `38cf30ea`. |
| C13.2 | Implemented in `582cd783`. |
| C14 | Implemented in `e2d71ac7`: the citation of Ben's decision at the exemption. The legacy bytes stay. |
| C15.2 | Implemented in `1ad77de0`. |
| C15.3, C15.4 | Implemented in `750844b9`. |
| C15.5 | Implemented in `6a55f8e0`. |
| C15.6 | Implemented in `8a12d906`. |
| C15.7 | Implemented in `82235e8c`. |
| C15.8 | Implemented in `7f4c147f`. |
| C15.9, C15.10 | Implemented in `007f9f31`. |
| C15.11 | Implemented in `498dc333`. |
| C15.12 | Implemented in `6581e5a4`. |
| C15.13 | Implemented in `1ad77de0`, with the addition Ben approved. |
| C15.14 | Implemented in `7a571cc7`. |
| C15.15 | Implemented in `7bd5ee8c`. |
| C15.16 | Implemented in `59e41a99`, in wave 2 rather than wave 3 (departure 2). |
| C15.17 | Implemented in `db700ec6`. |
| C15.18 | Implemented in `38cf30ea`. |
| C15.19 | Implemented in `95683791`. |
| C15.20 | Implemented in `55226123`, completed by `e0717e63` (departure 6), with the export check through the adapter. |
| C15.21, C15.22 | Implemented in `e2d71ac7`. |
| C15.23 | Implemented in `e88f2f55`. |
| C15.24, C15.25 | Implemented in `7bd5ee8c`. |
| C15.26, C15.27 | Implemented in `6a55f8e0`. |
| C15.28 | Implemented in `a1c4a746`. |
| C15.29 | Implemented in `b7f7e204`. |
| C15.30 | Implemented in `007f9f31`. |
| C15.31 | Implemented in `d1d8d1ce`. |
| C3 | Superseded: fixed after the review, by a deployment; no action. The residue phonetic-hbo clone stays Ben's decision. |
| C15.1 | Superseded: rejected in the disposition list that Ben approved; no action. |
| R1 to R7 | Implemented in `4573b007`; `75a1127b` names the removal commit in R7's entry (departure 11). |
| A0 to A10 | Deferred: A3, A2 and A10 to final integration on this machine; A0, A1, A7, A3, A2, A4, A5 and A8 to the relay-machine session; A9 to Ben in the Codex app. A6 is not done, by Ben's choice. |

The items of this file's "Not findings" paragraph get no action, as the plan says.

### Departures from the plan, and corrections

1. Wave 2 held back C6.1's reference lint and the README clause that names it, since the lint fails
   until "@2K 52:1" is corrected; both landed with C6.1, in `f2774cea`.
2. C15.16, planned for wave 3, went into wave 2's `59e41a99`, since the gate's retirement rewrote the
   passages it corrects.
3. C1.3's procedure text, planned for wave 6, landed in wave 3's `a363e5ce`, so that the references
   that commit adds resolve. That commit also adds one precision to the plan's README and refresh
   texts: the claim population is drawn from the survey's ordinary population, as the plan's design
   states.
4. Conforming edits that the plan did not list: `82235e8c` corrects the docstring of
   `py/phonetic_mam/display_schema.py`, which still said that release approval compares the output
   with the projection module that wave 3 removed, and in `py/py_html/forbidden_phonetic_marks.py`
   puts the plan's sentence in place of the old clause about a genuine source dot rather than
   beside it; `7a571cc7` names "The claim file" where C15.14's insertion made "It" ambiguous.
5. C15.21's comment names the exporter's call by its function, `_adapter_location`, rather than by
   the plan's `py/phonetic_mam/exporter.py:34-35`, since C15.19 had moved it (`e2d71ac7`).
6. `55226123` committed C15.20's rename without the fifteen importer updates that its message
   describes, because one pathspec of the staging command failed, so that commit alone does not
   import. `e0717e63` completes it, and every later commit chains staging and committing so that a
   failed `git add` stops the commit.
7. C15.20's export check needs the private adapter, which this forest's MAM-private clone,
   `C:/Users/BenDe/GitRepos2/MAM-private`, lacked: it was clean on `main` at `3dfbc5ed`, from
   2026-09-29. The executor fetched that clone and fast-forwarded it to its `origin/main`,
   `ccd80315`, before the export: an act outside this repository that the plan's list does not
   name. The adapter wrote nothing there, and that clone is clean on `main`.
8. C13.2's browser check used a short-lived static server on `127.0.0.1`, stopped afterwards,
   because the in-app browser's page tools cannot act on a `file://` page.
9. C10.2's two deployment times were re-read with `gh run list`, a read-only query of the Actions
   runs of MAM-basics and phonetic-hbo.
10. The executor's repetition of the retirement's reference audit scanned 296 issues and pull
    requests and 312 comments, where the planning scan counted 295 issues and pull requests; issue
    296 was created at 06:17:53 UTC on 2026-10-03, after that scan. Neither scan found a relay
    name.
11. R7's entry was written in the removal commit, which cannot name its own hash; `75a1127b` names
    it. The entry also carries a "Recorded by" line, as this repository's update entries do.
12. The plan calls C2's survey diff "an 82-line diff". `git show -U0` prints 84 lines for it, 62 of
    them changed lines (19 removed, 43 added) in 18 hunks, and the changes are exactly those the
    plan lists.
13. The Markdown checks owed by `00974386` and `6a55f8e0` ran at `6a55f8e0`, after both commits, and
    passed.
14. The full suite ran after wave 8 and before this entry, rather than in wave 9, so that a failure
    could still be fixed before this record; no executable, test, schema or shared-data change
    follows it.
15. `88f35055`, which edited three adaptation modules, names its plan item, C9.2, but not the
    approval of Ben's that it carries out, as `Yeivin-ITM/README.md`'s editing procedure asks: his
    approval on 2026-10-03 of the disposition list, which accepted C9.2, and his acceptance that day
    of the plan's recommendations. The pushed message stays as it is; the other commits that edited
    adaptation modules, `f2774cea` and `d1d8d1ce`, name Ben's choice.
16. Wrapping only, with no word changed: where a replacement changed a line's length, the rest of
    its paragraph was rewrapped (C10.1's items 6, 7 and 9, and C15.24's explanation). The commit
    that records this entry rewraps two lines of `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`
    that R7's corrections 4 and 5 had lengthened to 115 and 107 columns, and one line of the
    refresh skill's `references/dependent-refresh.md` that C1.3's insertion had lengthened to 131
    columns; that skill change takes effect with the rest at act A3.

### Verification before final integration

Each commit's message records its own checks: `git diff --check`; Black on every changed Python
file and ruff, with `ruff check py` reporting "All checks passed!" since `e2d71ac7`; the three
Markdown lints on every Markdown, update and instruction commit; and each item's own verification
as the plan gives it, with the scratch demonstrations that the message describes. Every generated
diff was read line by line and explained in its commit: C2's survey, claims and three Yeivin pages
(`c17de175`), C6.1's two lines of `yeivin_itm-207_285.html` (`f2774cea`), C13.2's `style.css` and
`pronunciation.js` (`582cd783`), C15.8's two index lines (`7f4c147f`) and C11's `pipeline.dot` and
`pipeline.svg` (`8ad4c1d2`). Every Hebrew form that the remediation added was lifted from its source
by a script.

**The full suite.** `./.venv/Scripts/python.exe py/main_test.py` ran at `7bd5ee8c`, the last commit
before this entry and later than every executable, test, schema and shared-data change; it ended at
13:56:04 New York time with 1,047 passed and 5 skipped, in 369.11 seconds. Run again with `-q`,
which the subtest count needs, it ended at 14:04:16 New York time with 1,047 passed, 5 skipped and
60 subtests passed, in 388.57 seconds. Against `644a6c9c`'s 1,056 passed, 5 skipped and 60 subtests: the relay's
removal took 15 tests (11 dispatch and 4 turn tests) and R5 added the turn-file lint; C12.2 added two
oracle tests, and C6.1, C4.3, C11 and C12.1 one lint each; C12.3 removed one test; and wave 2
removed the module-pin test and added the anchor test: 1,056 − 15 + 1 + 2 + 4 − 1 − 1 + 1 = 1,047.
The skips and subtests are unchanged.

**Read-only verification of the whole plan.** Four read-only sub-agents each checked one part of the
plan against the committed tree at `7bd5ee8c`: the published pages and distributed data; the
reader-facing documents; the code and test defects; and the editorial proposals with the relay's
retirement in the repository. Each found every item of its part as the plan words it, every output
that the plan says must not change unchanged, and no change that no item accounts for. Their
points of process are departures 3, 7, 15 and 16 above; C5.2's conditional sentence in the
finding-22 entry waits for this remediation's mega, as the plan says.

### Noticed outside the plan

1. Unfixed, because the review and the plan scope C15.4 to the eleven programs of `33470e2d`: 34
   other entry points under `py/` still call `sys.stderr.reconfigure(encoding="utf-8")` with no
   error handler, which resets stderr's `backslashreplace` to `strict`.

**What remains.** Final integration as the plan's "Final integration" describes: merging the current
`origin/main`, the mega, the fast-forward and push of `main`, then A3, A2 and A10 on this machine;
then the closing records; then the relay-machine session on the relay machine. This update remains
`State: open` while its base survives.

## Final integration completed, 2026-10-03

Recorded by Claude Opus 5.5 on 2026-10-03, New York time, in the executor session, at step 6 of the
plan's "Final integration". **Completed: the remediation is on `main` at
`e9c72f2b2e7c81b457d66852b0faace839525e1e`; this machine's live configuration is deployed from it,
its deployed agent file is retired, and the remediation branch is deleted. The relay machine's acts
remain.**

1. **The full suite** passed at `7bd5ee8c` with 1,047 passed, 5 skipped and 60 subtests passed, as
   the entry above explains. The one later commit, `e9c72f2b`, changes only documentation and the
   wrapping of one skill reference, so that result stands.
2. **The merge.** A fetch found `origin/main` still at `074af13a`, an ancestor of the branch, so the
   merge of `origin/main` made no commit.
3. **The mega.** `./.venv/Scripts/python.exe py/main_0_mega.py`, with no `REPOS_ROOT`, ran at
   `e9c72f2b` from 14:15:59 to 14:26:05 New York time and exited 0: 57 steps in 600.9 seconds, with
   Graphviz confirmed as the pinned 16.0.0 (20260814.1018). It left no tracked diff and no untracked
   file. Its `phonetic-mam-export` step re-exported the release through the private adapter in
   107.3 seconds and left `Phonetic-MAM/` unchanged, `BD-2Kings.json` included.
4. **Integration.** After a fetch, `origin/remediate-review-2026-10-02` was exactly `e9c72f2b`, the
   mega-verified commit. The clone switched to `main`, fast-forwarded it from `074af13a` to
   `e9c72f2b`, and pushed it at 14:26:33 New York time, never forced. The push reaches the published
   Pages tree at the next 04:17 deployment and the distributed products at once.
5. **A3 on `LAPTOP-DBLE8UKA`.** `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config`
   deployed from `refs/remotes/origin/main` at `e9c72f2b` and reported
   `USER_CONFIG_DEPLOYED_COUNT=8`: the four changed skills, `github-issues`, `hebrew-prose`,
   `mam-repository-topology` and `mam-wikisource-refresh`, in both `~/.claude/skills/` and
   `~/.agents/skills/`, whose directories that run recreated. `--sync-user-config --check` then
   reported `USER_CONFIG_PROBLEM_COUNT=0`.
6. **A2 on `LAPTOP-DBLE8UKA`.** The deployed `$HOME/.claude/agents/dual-agent-review-turn.md`, SHA-256
   `2CB3B50A719FF019162C9BF7B0684094106A99EE22AE0E60A9CD5ACA907E4308` and 2,494 bytes, byte-identical
   to its canonical blob at the archive commit `cbd405b1`, was moved at 14:27:21 New York time to
   `$HOME/relay-retirement-2026-10/dual-agent-review-turn.md`, which keeps that hash. The old path no
   longer exists, and the retention folder holds only that file.
7. **A10.** With `origin/main` at the branch's tip `e9c72f2b`, `git push origin --delete
   remediate-review-2026-10-02` and `git branch -d remediate-review-2026-10-02` deleted both at
   14:27:37 New York time. Undo: push the recorded tip again.

**The closing records** are the commit that adds this entry, made directly on `main`: this entry;
"Relay retirement acts on LAPTOP-DBLE8UKA, 2026-10-03" in the October 1 round's update; the
sentence that item 5 of "The MAM-basics trial review, kicked off 2026-10-02" in
`doc/dual-agent-review.md` gains; C5.2's sentence in the finding-22 entry of the September 29
round's update; and the plan's State. They change no source, product or canonical configuration,
so the suite, mega and deployment evidence above stands.

**Effective base State, 2026-10-03:** acted on; the remediation of the 64 accepted findings, with the
citation of Ben's finding-14 decision and the relay's retirement in the repository, was integrated
on `main` at `e9c72f2b` on 2026-10-03. The base report's line 3 stays as written.

**What remains:** the relay-machine session, which Ben starts on the machine that ran the relay with
the prompt in the plan's section of that name. It performs A0, A1, A7, A3, A2, A4, A5 and A8 there,
records their outcomes, and sets the plan's State to executed. A9 stays Ben's, in the Codex app, and
Ben may delete `$HOME/relay-retirement-2026-10/` on this machine whenever he wants the space. This
update remains `State: open` while its base survives.
