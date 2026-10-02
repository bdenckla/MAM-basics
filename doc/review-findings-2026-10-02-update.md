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
    translation. Wording correction: the source is a section of the Wikisource Village Pump,
    ויקיטקסט:מזנון, not a talk page.
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

Not applied. Each changes `doc/dual-agent-review.md`, "Running a trial review".

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
