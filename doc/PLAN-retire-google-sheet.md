# Retire the MAM Google Sheet pipeline

State: live

## Summary

Retire the Google Sheet as a maintained source, remove its download, parse,
comparison, and auto-edit pipeline from MAM-basics, and make Hebrew Wikisource the
only maintained textual source. Preserve the Sheet and its change log as a frozen
archive. Move the special-page inventory into the Wikisource downloader. Repository
changes are implemented normally; Google Sheet and Hebrew Wikisource changes are
supplied only as manual-edit drafts and verified afterward by downloading the live
results.

## Execution setup

- Perform the implementation from whichever MAM-basics checkout is assigned. Before
  editing, record `git rev-parse --show-toplevel`, HEAD, branch or detached state, and
  `git status --porcelain`. Do not assume that
  `C:/Users/BenDe/GitRepos/MAM-basics` is the development checkout.
- If a new Codex-managed worktree is detached, create
  `codex-worktree-<worktree-id>` after confirming that the name is unused. Preserve
  an existing branch.
- Use
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` as the shared
  interpreter, while running scripts, Git operations, and tests from the verified
  development checkout.
- Read `CLAUDE.md`, `py/product_scopes.py`, and the `hebrew-prose`,
  `spreadsheets`, and `computer-use` skills before editing.
- Re-establish the baseline before implementation. The planning snapshot was clean
  `main` at `39cdd0e3`, with 1,002 collected tests: 997 expected passes and 5 skips
  when pytest uses a writable `--basetemp`. Treat changed figures as findings rather
  than failures of this plan.

## Remove the Google Sheet pipeline

- Delete `in/mam-go/`, including the downloaded CSVs and search/replace recipes.
- Delete `MAM-parsed/google/` and its generated JSON.
- Delete the Google downloader, the CSV-to-JSON parser, and Google-specific read
  helpers.
- Delete `py/diff_wsgo/` and `out/diff_mamws_mamgo*.json`.
- Delete the two repository `.gs` copies of the auto-edit scripts. Do not alter the
  Google Drive copies attached to the Sheet.
- Remove the CLI interfaces `fr-google`, parser target `go`, and diff target `wsgo`.
- Remove mega stages `parse-go` and `diff-wsgo`. Remeasure the stage count; 57 are
  expected if the planning snapshot's 59 stages have not otherwise changed.
- Remove the retired products and stages from product scopes, coverage checks,
  runner maps, imports, help text, `.vscode/launch.json`, and repository-standard
  checks.
- Adjust source-tree lints so Google inputs and outputs are no longer expected. The
  `ב2` input lint should inspect only `in/mam-ws`.
- Search tracked files for retired paths, `diff_wsgo`, `wsgo`, the Sheet URL and
  purl, `גיליון הנתונים`, and auto-edit terminology. Preserve only frozen-status
  statements and intentional historical records.

## Add the Wikisource special-page mirror

- Extend every `fr-wikisource` run, including chapter-scoped runs, to maintain
  `in/mam-ws-special/`. Apply `--force-download` to chapter and special-page
  downloads.
- Declare the 36-page inventory from the Sheet's `מיוחד special` tab:
  - The Decalogue base, pointing, cantillation, and `Decalogue` alias pages.
  - Base, alternate-layout or pointing, and cantillation pages for שירת הים,
    שירת האזינו, מלכי כנען, שירת דבורה, שירת דוד, שירת העתים, עשרת בני המן, and
    שירת אסף.
  - The eight associated תתת pages for Exodus 15, Deuteronomy 32, Joshua 12,
    Judges 5, II Samuel 22, Ecclesiastes 3, Esther 9, and I Chronicles 16.
- Correct `שירת דוברה/טעמים` to `שירת דבורה/טעמים`. Follow redirects such as
  `Decalogue`, recording the requested and resolved titles.
- Store one byte-verbatim `.mediawiki` file per ASCII slug and a manifest containing
  the requested title, resolved title, page ID, revision ID, revision timestamp,
  byte size, and SHA-256.
- Fetch metadata first, download only changed pages unless forced, validate the
  complete response before replacing files, and write the manifest last.
- Fail closed on missing or unexpected pages, duplicate or converging identities,
  malformed metadata, and undeclared inventory changes.

## Update repository documentation

- Update the current READMEs, `DATA-LICENSES.md`, `CLAUDE.md`, generated MAM-parsed
  documentation, and relevant product pages to describe Wikisource as the maintained
  source and the Sheet as frozen on September 12, 2026.
- Preserve the verbatim Sheet-derived license text. Change its wrapper in
  `DATA-LICENSES.md` and the product licenses to identify a frozen historical source;
  add the special-page mirror to the source table.
- Correct the MAM-for-Sefaria HTML page's contradictory source claims.
- Replace the auto-edits runbook with a compact retirement page dated September 12,
  2026. Explain that `diff_wsgo`, its results, and the repository script copies were
  removed, with Git history as the reconstruction path.
- Remove the Google pipeline and feedback loop from the structured process graph and
  Ben-authored Graphviz source. Add the Wikisource special-page mirror and a dated
  frozen-Sheet note, then regenerate the SVGs with `py/main_pipeline_graph.py`.
- Regenerate authored MAM-parsed documentation with
  `py/main_authored.py gen-mam-parsed-docs`.
- Leave historical receipts unchanged, including finished dated plans and reviews,
  validation JSON, Holman records, the historical OSIS revision statement, bot-era
  histories, the archived `mamgo-auto-edits` declaration, and the original Google
  Drawing SVG.

## Generate manual Sheet and Wikisource edit drafts

- Do not edit the Google Sheet or Hebrew Wikisource during implementation.
- Generate two human-reviewable, uniquely named draft files under the verified
  checkout's gitignored `.novc/` directory and provide links to them.
- The Sheet instructions must preserve every tab, all data, published access, and
  attached Drive scripts. Direct the editor to add a merged, wrapped, high-contrast,
  always-visible first row across every used column on every tab except
  `שינויים changes`.
- Hebrew banner: `הדף הזה מוקפא מ־12 בספטמבר 2026 ואינו מתעדכן עוד. ויקיטקסט העברי הוא המקור המתוחזק. רק הדף „שינויים changes” עשוי להמשיך להתעדכן.`
- English banner: `This tab has been frozen since September 12, 2026 and is no longer maintained. Hebrew Wikisource is the maintained source. Only the “שינויים changes” tab may continue to be updated.`
- The Sheet instructions must also supply a draft expansion for the README tab
  explaining that the text, templates, special-page inventory, and AutoEdits
  material are archival; only the change log may still receive hand-authored
  updates.
- The Wikisource packet must contain exact modern-Hebrew draft replacements, keyed
  by live page title and a searchable existing-text anchor, for:
  - The root introduction.
  - The data-sheet technical guide.
  - The appendices, dating the Sheet's primary-source period as 2015–2026 while
    preserving historical upload and contributor facts.
  - Chapter 2's Sheet-navigation note.
  - Additional current-maintenance claims found by searching live Wikisource for
    the full Sheet URL, its purl, and `גיליון הנתונים`.
- Include the proposed edit summary
  `עדכון התיעוד לאחר הקפאת גיליון הנתונים; נכתב בסיוע Codex`, but prescribe no
  editing mechanism. The drafts must support either manual edits or a separately
  chosen tool.

## Verify the manual edits afterward

- After Ben reports that the Sheet edits are complete, download a fresh public
  workbook export to `.novc/` and inspect it with the spreadsheet tooling. Verify in
  spirit that:
  - Every non-change-log tab has a conspicuous bilingual warning.
  - The README communicates the retirement status.
  - `שינויים changes` remains exempt.
  - No tabs or existing data were removed.
- After Ben reports that the Wikisource edits are complete, download the live pages
  and compare their meaning with the draft packet. Then refresh the tracked
  `in/mam-ws-intro/` mirror using the existing downloader and review the exact diff.
- Do not claim the overall retirement complete until both external verifications
  occur. Distinguish completed Git work from pending manual Sheet or Wikisource work
  in every interim report.

## Verification and integration

- Format changed Python files with the primary clone's absolute interpreter and
  Black.
- Run a chapter-scoped `fr-wikisource` invocation twice. The first run should
  establish the special-page mirror; the second should produce no diff. Explain any
  unrelated chapter updates from newer Wikisource revisions.
- Confirm that removed commands and stages no longer appear in help,
  `--resume-from`, launch configurations, imports, or coverage declarations. Confirm
  that ordinary runs cannot recreate the deleted Google paths.
- Run the full suite from the verified checkout:

  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py --basetemp .novc/pytest-retire-google-sheet -p no:cacheprovider
  ```

- Run the mega pipeline from the verified checkout:

  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
  ```

- Inspect the complete Git diff. Expected changes are the Google-pipeline deletions,
  frozen-status documentation and licenses, regenerated graphs and documentation,
  and the new special-page mirror. MAM-simple corpus data, the MAM-for-Sefaria corpus
  CSV, MAM-with-doc book content, and MAM-OSIS corpus content must not change.
- Commit finished implementation. In the primary checkout, commit directly to
  `main` and push. In a secondary worktree, commit locally; immediately before
  archival, merge `main` into the branch, run the mega pipeline and commit every
  explained generated change, fast-forward the primary checkout, and push `main`.
- This work changes product-facing generated artifacts and public documentation.
  Pushes to `main` are hard-to-undo outward-facing acts. The Sheet and Wikisource
  writes are excluded from task-owned actions. Repository deletions remain
  recoverable through Git history.
