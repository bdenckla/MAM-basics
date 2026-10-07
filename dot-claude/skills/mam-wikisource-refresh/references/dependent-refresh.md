# Dependent refresh after MAM Wikisource data changes

Use this procedure only after `SKILL.md`'s download step, or the post-run download of a live
Wikisource bot run, leaves audited tracked changes in the verified MAM-basics development
checkout. Coordinate the existing entry points under the surrounding authorization.

## Preconditions

- Read the instructions of MAM-basics and MAM-private and the applicable worktree procedure.
- Record every selected checkout's absolute path, branch, HEAD, remote relationship and
  NUL-delimited status. Recheck HEAD and task-owned status before each commit.
- Use each full clone's own environment, or the development worktree's home-clone environment.
  Run each command from the root whose files it changes.
- Assign a clean, current MAM-private development checkout before the first public mega,
  which reads its adapter, and recheck that assignment before every private write.
  A known active writer or ambiguous ownership requires a handoff. A linked private worktree
  is supported: all retained private generators write within MAM-private.
- Select the public input checkout through `REPO_MAM_BASICS_DIR` for private commands.
  The public exporter selects the corresponding private checkout through
  `REPO_MAM_PRIVATE_DIR`. Required sources and owning interpreters must exist.
- Do not push either repository until the local dependency loop and its gates pass.
  phonetic-hbo is a frozen redirect and historical issue host; this refresh never reads,
  preflights, writes or restores its clone.

## Refresh sequence

1. **Commit the source change, then run the public mega.** In the MAM-basics development
   checkout, commit the source change first: `Refresh MAM from Wikisource`, or the saving bot
   run's own record as `SKILL.md` specifies. It also takes every change the download made under
   `in/mam-ws-special/`, as a bot run's record does. Write the prediction, reading the change
   with:

   ```powershell
   ./.venv/Scripts/python.exe py/main_diff.py mpplus --old <starting HEAD> --new HEAD --output <absolute .html path in a scratch directory>
   ```

   A bare filename raises, and the report covers only MAM-parsed plus, so predict special-page
   and revision-metadata changes from `git diff`. Then run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py
   ```

   The public mega exports `Phonetic-MAM/` through the retained read-only private source
   adapter, then renders and analyzes the tracked public release. Judge every diff against the
   prediction, run whitespace checks, verify the recorded HEAD and commit the explained products
   as `Regenerate MAM products from the Wikisource refresh`, with the prediction and its
   confirmation in the message. If the mega stops at a check, "Checks that a text change can
   trip" says what to do before committing. The mega's `diff-mpplus` step rewrites
   `gh-pages/MAM-with-doc/change-log/` from committed `HEAD`, which now holds the source change:
   after the product commit, restore those paths
   (`git restore -- gh-pages/MAM-with-doc/change-log/`) so that the public checkout is clean for
   steps 2 and 3; step 4's mega rewrites them and step 5 commits them. Between the source commit
   and step 5, `py/tests/test_diff_mpplus_unpinned_latest.py` and
   `py/tests/test_mpplus_alternative_oracle.py` fail by design.

2. **Recheck private ownership and inputs before writing.** Require the selected private
   checkout clean and assigned to this workflow. `REPO_MAM_BASICS_DIR` must name the just
   committed public checkout. Stop on stale input or an unrelated writer; do not borrow,
   stash or discard another task's state.

3. **Regenerate retained private products.** From the MAM-private development root, run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py --profile mam-refresh
   ```

   Use the private home-clone interpreter by absolute path in a worktree. This updates private
   source diagnostics, comparisons and research products. Judge every diff and run the
   repository's required checks. Commit explained changes locally; a legitimate no-op
   needs no empty commit. The profile has no publication ownership in phonetic-hbo.

4. **Close the public dependency loop.** From the MAM-basics development root, run its mega
   again with `REPO_MAM_PRIVATE_DIR` selecting the verified private development checkout:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py
   ```

   The exporter is the routine public pipeline's only private dependency. Phonetic rendering,
   both meteg surveys, the Breuer survey and the Yeivin claims/rendering consume public data.
   The mega's `diff-mpplus` step rewrites the MAM change log under
   `gh-pages/MAM-with-doc/change-log/` from committed `HEAD`, which now includes step 1's
   commit, so this run leaves the change-log diff that step 5 audits and commits. Judge every
   other diff against step 1's prediction and commit the explained dependent changes, leaving
   every path under `gh-pages/MAM-with-doc/change-log/` uncommitted for step 5. Unresolved
   failed checks, stale inputs and unexplained output changes stop the workflow; "Checks that a
   text change can trip" says how each is resolved.

5. **Generate change logs from final committed public data.** Run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_diff.py mpplus --all
   ```

   This rewrites the change log from committed `HEAD`, so it reproduces what step 4's mega
   left uncommitted. Audit every change-log diff; named historical-release reports must
   remain unchanged. In an ordinary refresh only `unpinned-latest.html` and
   `unpinned-latest.json` change, with `index.html` when the count of unreleased changes
   moves. Then run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_diff.py mpplus --check
   ```

   If book data changed but no change-log diff results, stop and resolve the discrepancy.
   Otherwise commit audited logs separately as `Regenerate MAM change logs` and repeat the
   freshness guard. Do not create an empty commit.

6. **Run final gates, integrate and push.** Follow both repositories' current integration
   rules. Merge moved origin/main in the development worktree, repeat affected checks and
   fast-forward its clean home clone only after gates pass. Run the full suite after the last
   change likely to break it; later documentation does not expire that result. Generator/data
   branches still owe the final mega after current main is incorporated. Require clean,
   explained results in both repositories. Push normal fast-forwards in dependency order:
   MAM-private, then MAM-basics. If a push rejects, incorporate the moved origin in development,
   repeat affected generators and checks, and audit new diffs before retrying.

7. **Verify completion.** Fetch both origins. Require each home clone clean on main and equal
   to origin/main. Any ahead/behind commit or tracked residue means the refresh is incomplete.

## Checks that a text change can trip

A refresh is judged by its diffs, as `SKILL.md`'s "Judge every diff: the expected changes, and
only them" says. These checks remain, and a refresh that changes MAM's text can trip each of
them. Approval of the refresh approves nothing that they protect.

1. **Closed dispatch.** A parser, renderer, survey or build raises on a template or shape that it
   does not recognize. Stop: the repair is code, a new case in the named dispatch whose semantics
   come from an existing explicit policy or from Ben. If the download's parse stops at
   `py/ws/ws_get_bk_in_fmt_2.py`'s header or category assertion, a chapter page no longer names
   the chapter it was fetched as: inspect the page, then record a deliberate layout change in a
   reviewed commit of its own, or report the page on Wikisource and download again once it is
   fixed; commit nothing from the stopped run.
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
3. **Statement checks**: the MAM-parsed claims that `doc/mp-claims.md` indexes, the accgram and
   post-stress-meteg page checks, Holman's table, and the like. Repair the statement, or the
   derived record and what it records, in one reviewable edit, naming in the commit message the
   change in MAM's text that made it false.
4. **Ben's published claims wait for him.** (a) The Yeivin fraction pins and quoted forms: if the
   mega stops at `yeivin-itm-survey-meteg-claims`, leave `claim_schema.py`, `quoted_forms.py`,
   the footnote modules, `Yeivin-ITM/meteg-claims.json` and `gh-pages/yeivin-itm/` unchanged,
   give Ben `py/main_yeivin_itm.py review-claims`'s report, and finish the refresh locally with
   `./.venv/Scripts/python.exe py/main_0_mega.py --resume-from yeivin-itm-render`; until he
   approves new pins or footnote edits in his own message, `check` and the Yeivin tests that
   compare the claims with the analysis fail, and nothing is pushed; with his approval, change only what he approved, rerun with
   `--resume-from yeivin-itm-survey-meteg-claims`, and commit those changes on their own, quoting
   his approval. (b) Near-Aleppo's stored pointed ketivs (Ben, 2026-10-07): when the build stops
   because a target's ketiv or qere differs from its record, ask Ben, giving the verse, the
   recorded and current ketiv and qere, the stored pointed ketiv, and the Aleppo Codex links that
   the `verse-links` skill produces. Do not write a new pointed ketiv yourself. After his
   decision, change the record's value and parameters as he says, in a commit of their own
   quoting him, and resume from `near-aleppo-build`.

## Required scenario behavior

1. Unchanged Wikisource data stops after the download, without downstream writes.
2. Changed chapter data requires the complete two-repository loop before any push.
3. A dirty or actively owned private checkout stops before the first public mega reads it.
4. A legitimate generator no-op continues without an empty commit.
5. A one-repository cloud checkout still lacks the private adapter and regeneration inputs;
   cloud-skipped mega steps do not establish completion of a changed-data refresh.
6. A moved Yeivin fraction, a broken quoted form in Ben's footnotes, or a changed ketiv or
   qere at a stored near-Aleppo pointed ketiv waits for Ben's approval before the push; the
   rest of the refresh proceeds.
7. A failed statement check on a record that is not Ben's published claim is repaired, with
   what it records, in one reviewable edit, and the refresh continues.
