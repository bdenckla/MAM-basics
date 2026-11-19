# Plan: credit outsiders' contributions in the MAM change logs

State: live; written and approved by Ben on 2026-11-19, not yet executed

## Origin, and whose words are whose

Written by Claude (Opus 5.5) on 2026-11-19, in a planning session that the commander session
"Commander for Claude's forests" (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) started at Ben's
word. Ben typed this in the commander at 10:00 New York time on 2026-11-19, as the commander's
brief, `change-log-credit-plan-brief-2026-11-19.md`, copies it:

> launch a planning session that will investigate how, in the MAM change logs (MAM-basics/gh-pages/MAM-with-doc/change-log/index.html), to add credit (attribution) for MAM improvements contributed by "outsiders" (where "outsiders" are neither me nor Avi), to be able to do things like this request from Avi (which could be the first application of this credit/attribution mechanism):
>
> This morning I saw [a correction report](https://he.wikisource.org/wiki/%D7%A9%D7%99%D7%97%D7%AA_%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi#%D7%94%D7%98%D7%A2%D7%9E%D7%94_%D7%91%D7%A9%D7%9E%D7%95%D7%90%D7%9C_%D7%91%27_%D7%93%27_%D7%95%27) the placement of a double accent in 2 Samuel 4:6, which I [corrected](https://he.wikisource.org/w/index.php?title=%D7%A9%D7%9E%D7%95%D7%90%D7%9C_%D7%91_%D7%93/%D7%98%D7%A2%D7%9E%D7%99%D7%9D&curid=237011&diff=3102555&oldid=2987851). This obviously impacts the Phonetic Tanakh. Is there a way to give credit to [Asael](https://he.wikisource.org/wiki/%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:%D7%A2%D7%A9%D7%94%D7%90%D7%9C)?
>
> A more general challenge/use of this new credit mechanism would be to port over attributions from the old Google Sheet change log (for the changes for which the old Google Sheet change log overlaps with the new MAM-with-doc-housed change logs)

The second and third paragraphs are Avi's request, as Ben quoted it. Everything else in this
plan is Claude's reconstruction and design, not Ben's words, until a decision below quotes him.

## Decisions

The planning session put seven decisions to Ben on its decision page,
`https://claude.ai/artifact/AhYxzigjhUi25Mw2Lffqg9`, each with a recommendation. Ben answered in
that session at about 10:34 New York time on 2026-11-19: "I approve of all of your
recommendations in the decision document." So:

1. **The planning session read the frozen Sheet's changes tab once** and measured the overlap.
   The figures are under "The old Google Sheet change log"; Phase 3 repeats the capture as a
   tracked mirror.
2. **Credits live in `in/mam-change-log-credits.json`,** hand-maintained, and a credit is
   recorded only on Ben's word; Avi's requests reach it through Ben. DATA-LICENSES.md terms:
   CC0 1.0 for the credits file, and CC-BY-SA 4.0 for Phase 3's capture of the Sheet's tab, the
   terms the deleted `in/mam-go/` row gave the Sheet's book tabs.
3. **A contributor is named as Ben or Avi names them, as the Sheet did,** and linked to their
   Wikisource user page when the credit comes from a Wikisource report and the account is
   confirmed. For 2 Samuel 4:6 that is "Asael", the name Avi's request gives, linked to the user
   page of `עשהאל`, the account Avi's request links. A ported credit keeps the name the Sheet
   writes, unlinked. Whether the Sheet's "Asael Reiter" is the same person is put to Ben at
   Phase 3's stopping point, where it first matters; until he answers, the two are separate
   contributors.
4. **A credited change shows a line on its card,** "Credit to <name>", with links to the
   evidence, and a `credits` list on its entry in the release's JSON. The contributors page comes
   with the Sheet port (Phase 4).
5. **What counts:** changes an outsider reported or suggested and MAM took, when Ben or Avi
   credits them: 2 Samuel 4:6 now, and the Sheet's credits that match a change in the logs,
   anonymous ones included and worded as the Sheet words them. An outsider is, in Ben's words,
   neither him nor Avi, so the Sheet's "Credit to Ben Denckla" rows are not ported. Holman's MAM
   suggestions marked taken in `py/hkq_cmn/mam_suggestion_dispositions.py` and other reports on
   Avi's Wikisource talk page are not in this plan.
6. **The Phonetic Tanakh shows no credit;** the MAM change logs only.
7. **This plan lives at `doc/PLAN-change-log-credits.md` in MAM-basics.**

## What exists today

Figures in this section were read at MAM-basics `b8fc953d` (origin's `main` at 10:21 New York
time on 2026-11-19) and on Hebrew Wikisource the same morning. They are dated observations; the
steps below re-read what they depend on.

### The change logs and their generator

- **Pages:** `gh-pages/MAM-with-doc/change-log/` holds `index.html`, `releases.json`, one HTML
  report and one JSON report for each named release (`2025-03-19a`, `2025-03-19b`, `2026-03-06`,
  `2026-03-16`, `2026-04-14`, `2026-09-17`), `unpinned-latest.html` and `.json` for the changes
  since the latest release, and the generated `style.css` and `filter.js`. The earliest release
  begins at MAM's state of 2024-12-17.
- **Generator:** `py/main_diff.py mpplus`, in `py/subcommands/diff_mpplus.py`, with the package
  `py/mb_diff_mpu/`. `generate_report` diffs two MAM-parsed/plus states
  (`mpplus_extract.diff_all_books`), classifies and verifies the diffs, and writes the JSON
  (`mpplus_json.write_json`, whose `_serialize_diff` builds one entry per verse diff, with its
  narrowed `changes` pairs) and the HTML (`mpplus_html.write_report`, whose `_expand_diffs` splits
  a verse diff into one card per changed span and `_render_card` draws each card).
  `mpplus_assets.write_shared_assets` writes `style.css`; `mpplus_index.write_index` writes
  `index.html`. `run_all` regenerates every named release, `unpinned-latest` and the index; the
  mega's step `diff-mpplus` is `diff_mpplus.run_all` (`py/main_0_mega.py`, its `StepRecord`
  "diff-mpplus"). `--check` regenerates into a temporary folder and compares bytes; `--pin`
  names a new release ending at `HEAD`.
- **Nothing in the change logs credits anyone today.** A card shows the reference, links to
  MAM-with-doc ("MwD") and Wikisource ("WS"), a category badge, an English description, the old
  and new forms, any changed alternative and any `נוסח` note.
- **`py/clc/clc_attribution.py` is unrelated.** The commander's brief pointed at it; it writes the
  Charitable Leningrad Codex's credit to UXLC and tanach.us, and `py/clc/` is that edition's
  package, not the change logs'.
- **How the refresh treats the logs:** `dot-claude/skills/mam-wikisource-refresh/` (canonical
  copy), `references/dependent-refresh.md`, step 5, regenerates them with `--all` and `--check`
  after the dependency loop and commits them as "Regenerate MAM change logs"; "named
  historical-release reports must remain unchanged" in an ordinary refresh.

### The first application: 2 Samuel 4:6

- **The report.** On Hebrew Wikisource's `שיחת משתמש:Dovi` (Avi's talk page), section
  `הטעמה בשמואל ב' ד' ו'`, user `עשהאל` (user id 94) wrote at 19:10 UTC on 2026-11-12 (revision
  3102539) that the atom והנה was marked, by its doubled telisha gedolah, as having final stress,
  which he judged very unlikely, since by his count the atom has penultimate stress at its other
  two occurrences in the Bible. Avi replied at 05:20 UTC on 2026-11-13 (revision 3102556), thanking
  him by his username and saying that he had corrected it.
- **The fix.** Revision 3102555 of `שמואל ב ד/טעמים` (page id 237011), by Dovi at 05:17:52 UTC on
  2026-11-13, parent 2987851, whose edit summary says that the double accent in verse 6 belongs
  on the he, giving penultimate stress. It changes only verse 6: MAM had the
  telisha gedolah's stress helper on the nun, in וְ֠הֵנָּ֠ה, and now has it on the he, the first letter
  of the stressed syllable, in וְ֠הֵ֠נָּה. The prepositive telisha gedolah on the vav is unchanged.
- **In MAM-basics.** The refresh pushed at about 09:00 New York time on 2026-11-19 took that
  revision: `in/mam-ws-revisions.json` records `שמואל ב ד/טעמים` at `revision_id` 3102555.
  `gh-pages/MAM-with-doc/change-log/unpinned-latest.json` has the entry `"book": "2Samuel"`,
  `"chapter": 4`, `"verse": 6`, `"category": "accent-change"`, with the one `changes` pair
  `"old": "וְ֠הֵנָּ֠ה"`, `"new": "וְ֠הֵ֠נָּה"`. Its card in `unpinned-latest.html` reads "Accent change —
  telisha-gedola on nun in old, on he in new". The same refresh changed the Phonetic Tanakh's page
  for the chapter, `gh-pages/phonetic-mam/tnkh/BB-2Samuel/04.html` (commit `ed5c5633`).

### The old Google Sheet change log

- **What it is.** The `שינויים changes` tab (gid 953964633) of MAM's Google Sheet,
  `https://docs.google.com/spreadsheets/d/1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs/`. The
  mirrored MAM introduction says it records the corrections from 2020-08-28 to 2026-09-12, when
  the whole Sheet was frozen (`in/mam-ws-intro/appendices.mediawiki`, section
  `רשימת תיקונים ושינויים`; `in/mam-ws-intro/root.mediawiki`). Since the freeze, Wikisource's page
  histories are the maintained record.
- **Its overlap with the change logs** is therefore the Sheet's rows from about 2024-12 to
  2026-09-12: the releases from `2025-03-19a` to `2026-09-17`. Rows near a release boundary are
  matched by their change, not by date, since a release's boundaries are MAM-parsed states, which
  lag the Sheet.
- **The frozen tab as the planning session read it,** at 15:35:32 UTC on 2026-11-19, by decision
  1, through its published CSV (URL below), obeying robots.txt: 189,511 bytes, SHA-256
  `030cb757027c00754600a43a989d8fd5bf6b8f2ed3f6196f23d39d6f1567684e`, 1,084 records. Record 1
  is the freeze banner and record 2 the header, so a data record's index plus one is its Sheet
  row: data rows 3 to 1084. The copy is in that session's scratchpad, not tracked; Phase 3
  captures it again. The measurements below are dated observations from that copy and the
  change logs at `b8fc953d`; Phase 3 repeats them.
- **Dates:** the rows run newest first. 1,026 rows read as day/month/year, as the header says;
  the newest 56 read only as month/day/year (row 3 is `09/10/2026`, which as a day-first date
  would fall after the freeze). A parser chooses, per row, the reading that falls neither after
  the freeze nor after the row above.
- **Credits:** 267 rows hold a word of credit or thanks. 266 say "Credit to <name>", in rows
  dated 2021 1, 2022 52, 2023 114, 2024 43, 2025 16 and 2026 40. Row 28 (Psalms 132:11,
  2026-08-07) instead thanks Nahum at Hebrew Wikisource for feedback that reverted the previous
  day's change. Of the 266, 38 credit Ben Denckla, who is no outsider, and 228 credit outsiders:
  Daniel Holman 132, Moshe Greenberg 46, Asael Reiter 16, anonymous contributors 24 (each
  described by where they wrote, as "anonymous contributor at Wikisource", with variants in
  wording and spelling), Ephraim at Hebrew Wikisource 2, Bezalel Ariel 2, David Kochav 2, and
  Adrian Hills, Timothy Leininger, Ittai Yehudah and Michael Escott 1 each. One credit
  continues "and thanks to Prof."
  with a name, so a parser that stops at the first full stop cuts it short.
- **The overlap with the change logs is small.** A test by script, that the row's verse has an
  entry in some change log whose forms share a word with the Hebrew the row quotes, ties 24 of
  the outsiders' credits to an entry: 5 in release `2025-03-19a`, 2 in `2026-03-06`, 1 in
  `2026-03-16` and 16 in `2026-09-17`; by name, Daniel Holman 15, Moshe Greenberg 2, Asael
  Reiter 2, "anonymous contributor at Wikisource" 2, and "anonymous contributor at AlHatorah",
  Timothy Leininger and "anonymous editor at Hebrew Wikisource" 1 each. Two of the 24 are dated
  shortly before the logs begin, 2024-11-28 and 2024-12-03, and sit in `2025-03-19a`, so a row's
  date does not decide its release. The test cannot confirm 9 more outsider rows that have an
  entry at their verse, and their dates or descriptions suggest that most are coincidences; 2
  outsider rows in the logs' span name more than one verse (rows 79 and 104); 165 name one verse
  that no change log touches, all dated before the logs begin. The same test ties 23 of Ben's
  credits to entries; they are not ported.
- **No current copy is tracked.** The retired Google downloader fetched only the six book tabs and
  the template-documentation tab (`in/mam-go/`, deleted in `a41fbcdd` on 2026-09-27). The only
  tracked copy of the changes tab is a snapshot of 2023-04-06, tracked from `d86e5779` until
  `fa3b9b29` removed it on 2026-03-25:
  `git show "fa3b9b29^:in/mam-go-2023-04-06/Miqra_al_pi_ha-Masorah - שינויים changes.csv"`.
- **Its columns** in that snapshot: `dd/mm/y`, `who`, `where`, `what`, `what-x (Hebrew)`,
  `what-y (Hebrew)`. `who` is who recorded the change (`S(A)K` 492 rows, `BD` 219, `BD & S(A)K`
  1, of 712). `where` is a Hebrew reference such as `דניאל ח,כה` or `בראשית לה כב`, or a book, a
  range or a word such as `special מיוחד`.
- **Its credits are prose in `what`:** "Credit to Daniel Holman." 120 rows of the 2023 snapshot
  credit someone that way: Daniel Holman 55, Moshe Greenberg 44, Asael Reiter 6, "anonymous
  contributor at Wikisource" 5, Bezalel Ariel 2, David Kochav 2, "anonymous editor at Wikisource"
  2, and one each for "anonymous reader at alhatorah", "anonymous contributor at Hebrew
  Wikisource", "anonymous reader at mg" and Michael Escott. By year: 2021 1, 2022 52, and 2023
  (to April) 67. None of these rows is in the change logs' span; the frozen tab's later rows are.
- **How the tab can be read.** The retired downloader read each book tab's published CSV,
  `https://docs.google.com/spreadsheets/d/e/2PACX-1vQrnXDxQJ3pojK_9K4TiRwCpz-NCMmW5mWE9fH5ITpV0IF9aV4-XVtmShTyyIoB_PGRCk4o_YQYWPsU/pub?output=csv&gid=<gid>`,
  through `mb_cmn.polite_download` with `obey_robots_txt=True`
  (`git show a41fbcdd^:py/subcommands/download_google.py`). The planning session's read showed
  that the publication includes the changes tab, gid 953964633. The freeze of 2026-09-27 put a
  banner in row 1 of every tab (`git show eea4c583:doc/PLAN-retire-google-sheet.md`), which is
  why the header is in row 2.
- **A precedent for matching:** `fa3b9b29` also removed a program that joined the changes tab's
  rows to diffs by verse: `py/main_mgc_match_go_changes_to_gogo_diffs.py` and `py/pymgc/`,
  whose `mgc_add_eng_bcv.py` turned `where` into an English book, chapter and verse. Read it with
  `git show fa3b9b29^:<path>`; do not restore it.

## Design

### The credits file

`in/mam-change-log-credits.json`, hand-maintained, UTF-8, LF, two-space indentation, in the shape
below. The Hebrew forms in a record are copied by script from the change log's JSON, never typed:
an editor or a normalizing tool can reorder marks, and the match below is exact.

```json
{
  "_header": ["What the file is, who may add to it, and how the change log uses it."],
  "contributors": {
    "<ascii-id>": {"name": "<the name to show>", "user_page": "<Hebrew Wikisource user name, or null>"}
  },
  "credits": [
    {
      "contributor": "<ascii-id>",
      "book": "2Samuel",
      "chapter": 4,
      "verse": 6,
      "change": {"old": "<copied>", "new": "<copied>"},
      "evidence": [
        {"kind": "he-wikisource-section", "page": "שיחת משתמש:Dovi", "oldid": 3102556, "section": "הטעמה בשמואל ב' ד' ו'"},
        {"kind": "he-wikisource-diff", "page": "שמואל ב ד/טעמים", "diff": 3102555, "oldid": 2987851}
      ],
      "recorded": {"on": "2026-11-19", "basis": "Ben's decision of 2026-11-19 on Avi's request"}
    }
  ]
}
```

- A record identifies its change by `book`, `chapter`, `verse` and exactly one of `change`, a
  pair of the entry's `changes`, or `templates`, `{"added": [...], "removed": [...]}`, equal to a
  structural entry's `templates_added` and `templates_removed`. Any other key raises. A third
  selector, for an `alternative_changes` item, is added only if the Sheet port needs one
  (Phase 3, step 4's stopping point).
- `evidence` kinds are closed: `he-wikisource-section`, `he-wikisource-diff` and, for the port,
  `mam-sheet-changes-row` (`{"kind": "mam-sheet-changes-row", "row": <Sheet row number>}`).
  Code builds every URL: `mb_cmn/he_wikisource_url.py`'s `he_diff_url` and `he_page_url`, and two
  helpers that this plan adds, one for a revision's permanent link with a section anchor and one
  for a Sheet row,
  `https://docs.google.com/spreadsheets/d/1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs/edit?gid=953964633#gid=953964633&range=A<row>`.
  A section anchor is the section title with spaces as underscores. The talk page will be
  archived some day; the permanent link to revision 3102556 survives that.
- `name` is shown as given. A Hebrew `name` is isolated with `<bdi>`, without `lang`, as an
  unpointed name in English prose.

### Matching, and when generation stops

- A new module, `py/mb_diff_mpu/mpplus_credits.py`, loads and validates the file and matches
  records to the serialized entries of each report. `generate_report` attaches every matching
  record whatever the entry point, so that a standalone report and the published one agree
  (`py/tests/test_diff_mpplus_unpinned_latest.py`,
  `test_standalone_release_reports_match_published_reports`, compares them).
- Within an entry a `change` record credits every pair equal to its `change`.
- `run_all`, which the mega, `--all`, `--check` and `--pin` all reach, requires every record to
  match exactly one entry across the reports it generates, and raises otherwise, naming each
  record and the entries it matched. A run that writes one report (no arguments, or `--old` and
  `--new`) attaches what matches and checks nothing further. `run_all` writes each report as it
  goes, so its check runs before `mpplus_index.write_index`, and its error says to restore
  `gh-pages/MAM-with-doc/change-log/` with `git restore` once the record is mended.
- The HTML card for a credited pair is found as `_distribute_docnote` finds a `נוסח` note's
  card: the raw pairs and the display pairs are narrowed separately, and the credited raw pair's
  index is the card's index. Where the two narrowings give different counts, raise rather than
  attach the credit to some card; `_distribute_docnote`'s fallback to the last card is not
  acceptable for a credit, which names a person.
- These failures are closed dispatch over a hand-made statement, the kind of check
  `AGENTS.md`, "What this repository's products are", allows: they test exactly what the
  statement depends on, the change it credits.

### What a credited change shows

- **JSON:** the entry gains `"credits"`, a list with, for each record, `contributor`, `name`, the
  pair or templates it credits, and the evidence URLs.
- **HTML:** under the card's forms, a line `<p class="credit">Credit to <name>: <a>report</a>,
  <a>fix</a>.</p>`, the name linked to its user page when there is one; a ported credit's
  evidence link reads "Sheet row <n>". A `.credit` rule joins `mpplus_assets.py`'s stylesheet,
  using its existing color tokens.
- Nothing else changes: the index, the categories, the filter and the counts stay as they are.

## Execution

### Preconditions and checkouts

1. The executor is a fresh session in a full MAM-basics clone in Claude's forests that the
   commander grants (`C:/Users/BenDe/GitRepos/MAM-basics` or `C:/Users/BenDe/GitRepos2/MAM-basics`).
   Record `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch and
   `git status --porcelain`. Require a clean `main` that contains the commit adding this plan.
   Every Git call carries `-c safe.directory=<that exact path>`; set `GIT_TERMINAL_PROMPT=0`,
   `GCM_INTERACTIVE=never`, `GIT_SSH_COMMAND=ssh -o BatchMode=yes` and `GH_PROMPT_DISABLED=1`.
2. Interpreter: that clone's `./.venv/Scripts/python.exe`, run from the clone's root.
3. Read first: `AGENTS.md`; `doc/review-trial.md`; the `mam-wikisource-refresh` skill's
   `SKILL.md` and `references/dependent-refresh.md`; `iterative-document-editing`; and
   `hebrew-prose` before any prose about accents. Read every module named under "The change logs
   and their generator", and the two tests named under "Matching".
4. The executor owns integration: commit on `main`, naming paths in `git add` and `git commit`,
   messages in files that quote Ben's decisions; fetch and merge `origin/main` before each push;
   push `main` normally. Stop on a merge conflict, unexpected `HEAD` movement or an unowned change.
5. Checks follow `doc/review-trial.md`: focused checks per phase, no daytime mega or full suite,
   and the last commit of each push says what was skipped and why, citing that file.
6. Nothing outward: the executor does not dispatch `.github/workflows/pages.yml`, edit Wikisource
   or write to anyone. The credits reach the live site at Ben's next Pages dispatch.

### Phase 1: the mechanism and 2 Samuel 4:6

1. **Baseline.** Run `./.venv/Scripts/python.exe py/main_diff.py mpplus --check` and require
   "MAM change-log artifacts are current." If it fails, stop: the logs are stale and that is a
   refresh's business, not this plan's.
2. **Credits file.** Write `in/mam-change-log-credits.json` with a header, the contributor of
   decision 3 (id `asael`, name "Asael", `user_page` `עשהאל`) and the 2 Samuel 4:6 record, by a
   scratch script that copies `old` and `new` from the `2Samuel` 4:6 entry of
   `gh-pages/MAM-with-doc/change-log/unpinned-latest.json`, or of
   whichever report holds that entry by then. Evidence as in the design's example; `recorded`
   quotes decision 2's basis.
3. **Code.** Add `py/mb_diff_mpu/mpplus_credits.py`; the two URL helpers; the attachment in
   `generate_report`; `credits` in `mpplus_json._serialize_diff`; the card line in
   `mpplus_html._expand_diffs` and `_render_card`; the `.credit` rule in `mpplus_assets.py`; the
   completeness check in `run_all`; and a paragraph in `diff_mpplus.py`'s module docstring that
   names the credits file and says when generation stops. Run Black on every changed Python file.
4. **Regenerate.** `./.venv/Scripts/python.exe py/main_diff.py mpplus --all`, then `--check`.
   Expected diff, and only it: `unpinned-latest.json` gains `credits` on the `2Samuel` 4:6 entry;
   `unpinned-latest.html` gains the credit line on that card; `style.css` gains the `.credit`
   rule. Every named release's two files, `index.html`, `filter.js` and `releases.json` are
   byte-identical. **Stop** on any other diff.
5. **Fault check, not committed.** Copy the credits file aside, delete one mark from the record's
   `new`, run `--check`, which generates into a temporary folder, confirm that it raises and names
   the record, and put the copy back. Save the command and its output under `.novc/` and cite
   them in the commit message.
6. **Focused checks.** `git diff --check`; `./.venv/Scripts/python.exe py/main_test.py
   py/tests/test_diff_mpplus_unpinned_latest.py py/tests/test_mpplus_alternative_oracle.py
   py/tests/test_shared_html_styles.py py/tests/test_mpplus_extract.py
   py/tests/test_mpplus_historical_archives.py`; and
   `./.venv/Scripts/python.exe py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc` before
   and after, comparing issue counts: a new issue is a finding.
7. **DATA-LICENSES.md.** Add a row for `in/mam-change-log-credits.json` with decision 2's terms.
8. **Commit and push.** One commit, "Credit outsiders in the MAM change logs, starting with
   2 Samuel 4:6", quoting Ben's request and his approval of the decisions.

### Phase 2: the refresh runbook

Edit the canonical skill only, in `dot-claude/skills/mam-wikisource-refresh/`, in a commit of its
own:

1. In `SKILL.md`, after the paragraph in "Judge every diff" that begins "Some hand-made
   statements have no check", add:

   > The MAM change logs credit contributors who are neither Ben nor Avi, from
   > `in/mam-change-log-credits.json`. A credit is Ben's statement: record one only on his word,
   > in a commit of its own that quotes him, never on an agent's reading of Wikisource. When a
   > refresh's change came from such a contributor's report, as 2 Samuel 4:6 did on 2026-11-19,
   > say so to Ben with the report's link, and record nothing until he answers.

2. In `references/dependent-refresh.md`, "Checks that a text change can trip", add a seventh item:

   > 7. **The change logs' credits.** `py/main_diff.py mpplus --all` stops when a record of
   >    `in/mam-change-log-credits.json` matches no entry of the change logs, or more than one.
   >    A refresh trips it when it changes a credited form again before the release is pinned.
   >    Show Ben the record and the entry's new forms; change the record as he says, in a commit
   >    of its own that quotes him, then resume. A change to the credits file legitimately
   >    changes the named releases that hold its entries; an ordinary refresh changes no record.

3. Commit, push, then deploy the live skill copies by the procedure in `dot-claude/README.md`,
   "Main-sourced deployment and check", from the clone's own environment.

### Phase 3: the Google Sheet port

1. **Capture.** Read robots.txt, then fetch the tab's published CSV once through
   `mb_cmn.polite_download` with `obey_robots_txt=True`, as the retired downloader did, into
   `in/mam-go-changes-tab/changes.csv`, byte for byte, with `manifest.json` recording the URL,
   the retrieval time with its offset, the byte size and the SHA-256. Require record 1 to be the
   freeze banner and record 2 the header `dd/mm/y, who, where, what, what-x (Hebrew), what-y
   (Hebrew)`; then a record's index plus one is its Sheet row. **Stop** if the publication omits
   the tab or the header differs, and ask Ben to download the tab himself. Compare the SHA-256
   with the planning session's, under "The old Google Sheet change log": a different hash means
   the frozen tab changed, so stop and tell Ben what differs. Add a DATA-LICENSES.md row with
   decision 2's terms for the capture. Never normalize the capture.
2. **Survey,** by a script under `.novc/`: every row whose `what` holds "credit" or "thank" in
   any case, parsed by a closed list of recognized phrasings ("Credit to <name>.", the continuation
   "and thanks to Prof. <name>", and any variant the survey finds); a credit-like row that no
   phrasing recognizes stops the survey until a phrasing is added or the row is listed as no
   credit, with the reason. Row 28, Nahum's feedback behind a revert, is such a row: list it with
   whatever the logs show at Psalms 132:11. Leave out the rows crediting Ben Denckla, by decision
   5, and count them. Read each date as "The old Google Sheet change log" says. Parse `where` into
   book, chapter and verse where it names one verse, with the book names of
   `mb_cmn/mam_bknas_and_std_bknas.py` and the numerals of `mb_cmn/hebrew_verse_numerals.py`;
   list every other `where` with its row.
3. **Candidates.** For each credit row, list the change-log entries at its verse in every report,
   with release, category and forms, beside the row's date, `what`, `what-x` and `what-y`.
   Expect about the planning session's figures: 24 outsider credits tied to an entry, 9 more with
   an entry at their verse, and 2 naming more than one verse in the logs' span. A large departure
   is a finding: explain it before going on.
4. **Judge,** row by row: which entry and pair the row describes, if any. A row whose change is
   confined to a documentation note, lies outside the logs' span or matches nothing gets a reason.
   **Stop** and report to Ben on a decision page: matched, unmatched by reason, the rows that
   remain ambiguous, and whether the Sheet's "Asael Reiter" is the Wikisource user `עשהאל` whom
   Avi's request calls Asael (decision 3). Wait for his answers. If he says they are one person,
   use one contributor id, with the name he gives, for 2 Samuel 4:6 and the Sheet's credits.
5. **Write the records** by script, copying forms from the change log's JSON, with evidence
   `mam-sheet-changes-row` and `name` as the Sheet writes it.
6. **Regenerate** with `--all` and `--check`. Expected: the named releases that hold matched
   entries gain credits, in JSON and HTML; nothing else changes. Same focused checks as Phase 1.
7. **Record** the port in a dated receipt, `doc/change-log-credits-sheet-port-<date>.md`: the
   capture, the counts, and every unmatched row with its reason. Commit the capture, the records,
   the regenerated logs and the receipt, then push.

### Phase 4: a contributors page, with the Sheet port

By decision 4, the contributors page lands with Phase 3, in the same push or right after it:
`gh-pages/MAM-with-doc/change-log/contributors.html`, generated by `run_all` from the credits
file: each contributor, then each credited change with its release and a link to its card. Give
each card an `id` for that link. Add the page to `generated_artifact_names` so that `--check`
covers it, and link it from `index.html`. Expected diff: the new page, the `id`s on credited
cards, and the index's link.

### Expected unchanged

The MAM-with-doc book pages, MAM-parsed, MAM-simple, Phonetic-MAM and the Phonetic Tanakh pages,
`releases.json`, `MAM-parsed/historical/`, and every product outside
`gh-pages/MAM-with-doc/change-log/`. An unexpected diff there is a finding: stop.

## Outside this plan

- Dispatching Pages, which publishes the credits, is Ben's.
- Telling Avi or the contributors that the credits exist is Ben's, or Avi's.
- Crediting further sources, such as Holman's MAM suggestions marked taken in
  `py/hkq_cmn/mam_suggestion_dispositions.py` or earlier reports on Avi's talk page, needs Ben's
  word and a plan revision.
