# Retire the MAM Google Sheet pipeline

State: live

## Summary

Retire the Google Sheet as a maintained source, remove its download, parse,
comparison, and auto-edit pipeline from MAM-basics, and make Hebrew Wikisource the
only maintained textual source. Preserve the Sheet and its change log as a frozen
archive. Move the special-page inventory into the Wikisource downloader. Repository
changes are implemented normally; Google Sheet and Hebrew Wikisource changes are
supplied only as manual-edit drafts and verified afterward by downloading the live
results. Ben made these retirement and authority-boundary decisions on 2026-09-12.

## Execution setup

- Perform the implementation from whichever MAM-basics checkout is assigned. Before
  editing, record `git rev-parse --show-toplevel`, HEAD, branch or detached state, and
  `git status --porcelain`. Do not assume that
  `C:/Users/BenDe/GitRepos/MAM-basics` is the development checkout.
- Confirm that no other task is writing the assigned checkout. Preserve an existing
  branch. If the assigned checkout is detached, follow the managing environment's
  verified detached-worktree rule rather than assuming a Codex branch name.
- Read the applicable user instructions and the assigned checkout's repository
  instructions. Load `codex-worktree-tasks` only when the assigned checkout is
  Codex-managed.
- Use
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` as the shared
  interpreter, while running scripts, Git operations, and tests from the verified
  development checkout.
- Read `py/product_scopes.py`. Load the installed user `hebrew-prose` skill before
  editing relevant prose. Load the executing environment's `spreadsheets` and
  `computer-use` skills if they are available; stop if any skill required for the
  assigned work is unavailable rather than implying that those skills are tracked
  in this repository.
- Re-establish the baseline before implementation. The planning snapshot was clean
  `main` at `39cdd0e3`, with 1,002 collected tests: 997 expected passes and 5 skips
  when pytest uses a writable `--basetemp`. Rerun the full-suite command under
  “Verification and integration” before editing; treat a changed count as a finding
  rather than silently retaining the dated figure.

## Remove the Google Sheet pipeline

Before editing, write `.novc/remeasure_google_sheet_retirement.py` to parse
`py/main_0_mega.py` with `ast`, enumerate the literal `_STEPS` `StepRecord` calls,
and print their step IDs. Run it from the verified checkout with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/remeasure_google_sheet_retirement.py
```

- Delete `in/mam-go/`, including the downloaded CSVs and search/replace recipes.
- Delete `MAM-parsed/google/` and its generated JSON.
- Delete the Google downloader, the CSV-to-JSON parser, and Google-specific read
  helpers.
- Delete `py/diff_wsgo/` and `out/diff_mamws_mamgo*.json`.
- Delete the two repository `.gs` copies of the auto-edit scripts. Do not alter the
  Google Drive copies attached to the Sheet.
- Remove the CLI interfaces `fr-google`, parser target `go`, and diff target `wsgo`.
- Recompute the current `_STEPS` inventory before editing. Removing `parse-go` and `diff-wsgo`
  must reduce that remeasured set by exactly two; do not preserve a dated absolute count.
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
- Declare this exact 36-title inventory from `in/mam-ws-intro/ch2.mediawiki` at
  `dab5d091`, anchored by `טבלה לדפים של עשרת הדברות` around lines 361–388 and the
  song-form table around lines 746–804:

  1. Four Decalogue pages: `עשרת הדברות/טעמים`, `Decalogue`,
     `עשרת הדברות בסיס/טעמים`, and `עשרת הדברות/ניקוד`.
  2. For each of `שירת הים`, `שירת האזינו`, `מלכי כנען`, `שירת דבורה`, `שירת דוד`,
     `שירת העתים`, `עשרת בני המן`, and `שירת אסף`, the three pages `/טעמים`,
     `/צורת השיר`, and `/צורות נוספות`.
  3. Eight chapter pages: `שמות טו/טעמים`, `דברים לב/טעמים`, `יהושע יב/טעמים`,
     `שופטים ה/טעמים`, `שמואל ב כב/טעמים`, `קהלת ג/טעמים`, `אסתר ט/טעמים`, and
     `דברי הימים א טז/טעמים`.
- Correct `שירת דוברה/טעמים` to `שירת דבורה/טעמים`. Follow redirects such as
  `Decalogue`, recording the requested and resolved titles.
- Store one byte-verbatim `.mediawiki` file per ASCII slug and a manifest containing
  the requested title, resolved title, page ID, revision ID, revision timestamp,
  byte size, and SHA-256.
- Fetch metadata first, download only changed pages unless forced, validate the
  complete response before replacing files, and write the manifest last.
- Before downloading, write a scratch extractor that parses the two named tables in
  `ch2.mediawiki`, asserts that the selected set equals the literal 36-title set
  above, and records both requested and redirect-resolved titles. The mirror is
  independent: all 36 requested titles must be unique; all resolved identities
  within `in/mam-ws-special/` must be unique; exactly the eight declared chapter
  identities may overlap the existing book mirror; and any other cross-mirror
  overlap, missing page, undeclared redirect convergence, malformed metadata, or
  inventory change fails before replacement. Write the manifest last, only after
  all responses validate.

The same scratch extractor must rediscover and assert these eight Sheet-side `תתת`
chapter rows and their `/צורות נוספות` targets, pinned to `dab5d091`. Parse the CSV
and match the `תתת` field and target; the line numbers are searchable evidence, not
parser input:

1. `in/mam-go/A-Torah.csv:2078`, `ספר שמות/טו`;
2. `in/mam-go/A-Torah.csv:6173`, `ספר דברים/לב`;
3. `in/mam-go/B-NevRish.csv:327`, `ספר יהושע/יב`;
4. `in/mam-go/B-NevRish.csv:859`, `ספר שופטים/ה`;
5. `in/mam-go/B-NevRish.csv:2912`, `ספר שמואל/שמ"ב כב`;
6. `in/mam-go/E-XamMeg.csv:462`, `מגילת קהלת/ג`;
7. `in/mam-go/E-XamMeg.csv:818`, `מגילת אסתר/ט`; and
8. `in/mam-go/F-KetAx.csv:1756`, `ספר דברי הימים/דה"א טז`.

Run that extractor from the verified checkout with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/extract_google_sheet_special_pages.py
```

At `dab5d091`, `out/diff_mamws_mamgo.json` and
`out/diff_mamws_mamgo-auto-edits.json` both contain `[]`. Reproduce that pinned fact
before editing with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py wsgo
```

A different result is a finding.

## Update repository documentation

- Update the current READMEs, `DATA-LICENSES.md`, `AGENTS.md`, generated MAM-parsed
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
  `עדכון התיעוד לאחר הקפאת גיליון הנתונים; נכתב בסיוע <Claude|Codex>`, substituting
  the executing agent's name, but prescribe no editing mechanism. The drafts must
  support either manual edits or a separately chosen tool.

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
