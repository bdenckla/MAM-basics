# Programme: the seven-item Holman meteg rollout

Written 2026-09-03, consolidating into git a plan that until then existed only
in one untracked sketch and in agent-call transcripts. Ben's instruction that
day: *"I want all these consolidated into git and related to each other at this
point, as I fear loosing track of this larger context."*

**STATUS: items 2 through 7 are a SKETCH, not an approved plan.** They were
assembled from three research-agent reports and one Plan-agent validation pass,
synthesized in conversation, and never reviewed against repository state a
second time. Re-verify every path, command and figure below before acting on
any of them. Item 1 alone has a reviewed, tracked plan of its own.

Execute everything here from `C:/Users/BenDe/GitRepos/MAM-basics`, venv
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

## What the programme is for

Holman sent 34 suggestions about MAM, rendered as cards M1–M34 on
`gh-pages/holman/table_data_findings.html`. Thirty of them differ from their
comparison form in metegs alone. This programme applies those thirty to MAM by
Wikisource bot, carries the change through the MAM update pipeline, archives
the thirty records, and refreshes the mgketer comparison.

**Twenty-nine of the thirty remove a meteg from MAM; one, M23 at Isaiah 23:12,
adds one.** That asymmetry is the single most common way to get this work
wrong, and it recurs in items 2, 3 and 7. Measured 2026-09-03 over
`holman/docs-not-served/mam_suggestions.json`: 29 records where MAM carries the
extra meteg, one where the Aleppo comparison does.

**The letter M is the MAM-suggestion series prefix, not an abbreviation of
meteg.** `py/py_render/rt_mam_suggestion_card.py` renders it as
`M{case_number}`. There are 34 M records; the 30 meteg ones are M1–M16,
M18–M23, M25–M31 and M33 — that is, all of them except M17, M24, M32 and M34,
which are accent-placement records and are NOT part of this programme.

## The seven items

| # | Item | Status |
|---|---|---|
| 1 | Track the notes, publish a gh-pages page, link it from the M23 card, rename the archive label | Planned in detail, reviewed — see the plan named below |
| 2 | Build the Wikisource bot edit files for all 30 | Sketch only |
| 3 | Run the bot | Sketch only |
| 4 | Download the affected chapters, plus Joshua 10 and Zechariah 2 | Sketch only |
| 5 | Run the wsgo diff and the standard MAM update pipeline | Sketch only |
| 6 | Archive the 30 records | Sketch only; the terminology-rename half is in item 1's plan |
| 7 | Refresh the mgketer comparison | Sketch only |

Items 2 through 7 are ordered by dependency, not by preference: each needs the
one before it. Item 1 is independent of all of them and can be done first or
last.

### Item 1: the notes, the page, the M23 link, the terminology rename

Covered in full by
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md),
which was reviewed on 2026-09-03 and corrected the same day. That plan
publishes a survey of MAM's 231 post-stress metegs at
`gh-pages/post-stress-meteg.html`, gives the M23 card a neutral link to it, and
renames the reader-facing Holman archive label from "Suppressed" to "Archived".

It deliberately does NOT archive any record, edit Wikisource, or run the mega
pipeline. Those are items 2 through 6 here.

### Item 2: build the Wikisource bot edit files

The mechanism is `py/ws/ws_bot_edit.py` and `py/main_ws_bot.py`. `edit-kind` is
a FILE-LEVEL key, so one JSON file cannot mix kinds, and **two files are needed**:

1. `edit-kind: meteg-removal`, for the 29 removals, roughly 24 chapters across
   seven books (1 Kings, 1 Samuel, 2 Chronicles, 2 Kings, 2 Samuel, Isaiah,
   Judges). Each entry carries `ch`, `old` and an optional `comment`; `old`
   must occur exactly once in that chapter's raw wikitext, and the bot removes
   the FIRST U+05BD in `old`. Twenty-eight records are one entry each.
   **M13, 2 Chronicles 18:33, is two entries in the same chapter**, one per
   parameter of a `{{מ:קמץ|ד=...|ס=...}}` template call: `old="הׇֽחֳלֵֽיתִי"` for
   the ד parameter and `old="הָֽחֳלֵֽיתִי"` for the ס parameter. Removing the
   meteg from ד alone would leave the two forms differing in something other
   than the qamats, which is the only thing that template exists to vary.
2. `edit-kind: explicit-replacement`, one entry, for M23 at Isaiah 23:12 — the
   sole addition-direction record: `old="ק֣וּמִי"`, `new="ק֣וּמִֽי"`. Verify
   uniqueness within Isaiah chapter 23 at execution time; the corpus holds
   fifteen similarly-spelled קומי atoms elsewhere, so a chapter-scoped
   uniqueness check matters here specifically.

**Build every `old` string from each record's `mam_form` field verbatim, never
retyped by hand.** The pre-flight gate is an arithmetic check: stripping the
first U+05BD from `mam_form` must reproduce `comparison_form` exactly. A
Plan-agent pass ran that over all 30 records on 2026-09-03 with zero
mismatches. Re-run it on the assembled JSON before touching the wiki.

Before constructing the files, re-download the target chapters
(`py/main_download.py fr-wikisource`, scoped) so the `old` strings are built
against current text rather than a stale local snapshot.

**Not yet checked**: whether any of the other 28 removal records sit inside a
template the way M13 does. The method is to grep `in/mam-ws/<Book>.json` for
the exact form, one record at a time, before assembling the edit files.

### Item 3: run the bot

`proto --edits <file>` validates against local `in/mam-ws/` text. That is
necessary and not sufficient: it does not prove the strings are still unique on
the live wiki. `real --no-save` fetches live text, runs the identical
assertion, and skips only the final `page.save()`. **Run `--no-save` across the
full target set immediately before the real save.** A report of every chapter
that would change is the expected outcome, not a failure to fix.

**The bot has no crash recovery** — no try/except anywhere in the apply loop.
A failure partway through leaves whatever was already saved standing on live
Wikisource with none of the run's bookkeeping written. Mitigation: run `real`
in `--book39`-scoped slices rather than one 30-entry sweep, checking
`modified-chapters.json` after each slice, so a failure's blast radius is one
book.

This item needs Ben's own `~/.pywikibot/password.py`, a bot password under the
account `BDencklaBot`. Verify it exists before starting. **A session must never
see, create or handle that credential**, and editing a live wiki is an
irreversible outward-facing action: it is Ben's to authorize each time.

### Item 4: download the affected chapters, plus Joshua 10 and Zechariah 2

The `real` run auto-downloads and reparses modified chapters afterward unless
`--no-post-download` is passed. Do not pass it.

Separately, re-download Joshua chapter 10 and Zechariah chapter 2. Checked
2026-09-03: `in/mam-ws/B1-Joshua.json` and `MAM-parsed/plain/B1-Joshua.json`
both still held the single-pashta, pre-correction form at Joshua 10:12 even
though the fix had been live on Wikisource since 2026-08-28. Zechariah 2:4's
local copy already had the corrected form, so downloading it is consistency
rather than repair.

**Joshua 10:12 is not expected to go quiet downstream**, and this is the
programme's other standing trap. The mark added there is a stress helper, a MAM
notational convention the source manuscripts are not expected to carry, so
mgketer showing a diff at that word afterward is correct. It needs no
suppression entry.

### Item 5: the wsgo diff and the standard update pipeline

In order:

1. `py/main_diff.py wsgo` — compares `in/mam-ws/` against `MAM-parsed/plain/`,
   writing `out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json`.
2. Commit and push the auto-edits JSON, because the next step fetches it over
   HTTP from GitHub.
3. **Ben, manually, in the MAM Google Sheet**: "Import auto-edits from GitHub",
   then "Apply imported auto-edits", both Apps Scripts under
   `misc/Google Sheet Apps Scripts/`. No session can automate this step.
4. `py/main_download.py fr-google` — downloads and reparses, producing fresh
   `MAM-parsed/plus/` and `plain/`.
5. Re-run `py/main_diff.py wsgo` and confirm it is empty for the touched verses.
6. `py/main_0_mega.py` from the repository root, from scratch. Regenerates
   MAM-parsed, MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS, and this
   repository's own `out/` and `gh-pages/`.
7. Commit and push every touched sibling repository. Each has its own
   `gh-pages/` Pages-deploy workflow firing on push to `main`.

### Item 6: archive the 30 records

For each of M1–M16, M18–M23, M25–M31 and M33, add a `Disposition` entry to
`DISPOSITION_BY_REF` in `py/hkq_cmn/mam_suggestion_dispositions.py`: outcome
"Suggestion taken", a one-line summary naming the letter and the direction,
`decided_by` "Ben Denckla", `decided_on` the execution date.

**Look up each record's actual `ref` field from the suggestions JSON by
`case_number`; do not construct it from the displayed "BookName ch:v.atom"
form.** `book_abbrev`, which `ref` uses (for example "2Ch"), differs from
`std_book_name`, which the display string uses (for example "2Chronicles"), so
a guessed ref fails to match silently.

Re-run the ingest so the dispositions reach the suggestions JSON, confirm
`require_every_disposition_applied()` passes — it raises loudly on any stale or
unmatched key — then re-render and confirm all 30 appear under Archived.

The reader-facing rename of that page's label from "Suppressed" to "Archived"
is item 1's Phase 4, not this item.

### Item 7: refresh the mgketer comparison

mgketer lives in `C:/Users/BenDe/GitRepos/MAM-private/mgketer` and is **outside
the MAM-basics pipeline**: `py/main_0_mega.py` does not reach it, and this
repository only ever reads its reports. Precondition:
`MAM-parsed/plus/<Book>.json` current for the seven affected books, from item
5's mega run.

```powershell
C:/Users/BenDe/GitRepos/MAM-private/mgketer/.venv/Scripts/python.exe py/main_diff.py --all
```

No re-scrape is needed, since mgketer's scraped data does not change when MAM
does, and no suppression entry is needed, since a diff simply disappears when
the texts agree. Re-read `out-reports/index.html`'s by-type table: "MAM adds
meteg" (67 before) should drop by however many of the 28 non-M13 removals are
extant in the Aleppo Codex, and "mgketer adds meteg" (5 before) should drop to
4, M23 leaving that category. Commit and push MAM-private.

Joshua 10:12, per item 4, is expected to show a new diff here. That is correct.

## The evidence notes, and where they still live

Seven files under `C:/Users/BenDe/.claude/plans/` are the evidence base for
this programme. **They are not in git**, which is the loss this document was
written against, and moving them into a tracked location is unfinished work as
of 2026-09-03.

| File under `C:/Users/BenDe/.claude/plans/` | What it holds |
|---|---|
| `writing-only-to-a-robust-teapot-M23.md` | The M23 question, the Yeivin and Breuer sections for each post-stress type, the census summary, and the 1 Samuel 17:5 post-silluq case |
| `writing-only-to-a-robust-teapot-M-vs-mgketer.md` | The 30-row table of verses and forms, and the M13 and M22 special cases |
| `writing-only-to-a-robust-teapot.md` | M13's `{{מ:קמץ}}` template finding, which item 2 turns into two bot entries |
| `writing-only-to-a-robust-teapot-accent-placement-four.md` | M17, M24, M32 and M34 — the four records this programme excludes — and why Joshua 10:12 stays noisy |
| `writing-only-to-a-robust-teapot-archived-terminology.md` | The five rendered uses of "Suppressed" that item 1 renames |
| `writing-only-to-a-robust-teapot-census-report.md` | The 2026-09-03 census output, the legacy baseline item 1's Phase 1 measures against |
| `writing-only-to-a-robust-teapot-census.py` | The throwaway script producing that report |

The census script **cannot be tracked as it stands**: line 49 is a
`sys.path.insert`, which `~/.claude/CLAUDE.md` bans in tracked source at a
count of zero per repository. Its job is taken over by item 1's Phase 1
generator, so the report is worth tracking and the script is not.

`although-the-forest-of-peppy-lampson.md`, in the same directory, belongs to
the **evacuation** programme rather than this one — see
[`PLAN-evacuate-the-rest-of-three-repos.md`](PLAN-evacuate-the-rest-of-three-repos.md).

## Preconditions common to every item

Another session may be live in MAM-basics or a sibling repository. Record HEAD,
inspect status, and record the intended-path list before editing; never stage a
path this programme did not touch. Items 4 through 7 reach MAM-parsed,
MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS and MAM-private, none of
whose revisions were recorded when this programme was sketched — re-check all
of them before starting.

In a worktree, sibling repositories do not resolve by default:
`paths.repos_root()` returns `repo_root().parent`, which is the worktree's
parent rather than `GitRepos`. Set `REPOS_ROOT=C:/Users/BenDe/GitRepos`, or a
per-repository `REPO_<NAME>_DIR`, and the failure is loud rather than silent
either way.
