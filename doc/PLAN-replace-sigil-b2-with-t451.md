# Replace the sigil ב2 with ת451 on Wikisource, and propagate

Written 2026-08-27, at `d7df398`. Closes [#260](https://github.com/bdenckla/MAM-basics/issues/260)
and one bullet of [#259](https://github.com/bdenckla/MAM-basics/issues/259); their umbrella is
[#257](https://github.com/bdenckla/MAM-basics/issues/257).

Two of the seven phases can only be run by Ben, and they sit in the middle rather than at the end:
Phase 3 needs the pywikibot bot password, and Phase 5 happens inside the MAM Google Sheet. So this
is a chain with two hand-offs built into it, not a plan a single session runs start to finish.

## Status

| Phase | State |
|---|---|
| 1 — the bot edit | **DONE 2026-08-27**, `52aa7b8`. Six files as specified. Suite **951 passed, 5 skipped, 59 subtests** before, **965 passed, 1 failed, 5 skipped, 65 subtests** after. The one failure is the new lint test, by design; the 15 added test functions are 13 in the payload test and 2 in the lint, and the 6 added subtests are the six real Daniel chapters |
| 2 — local proto rehearsal | **DONE 2026-08-27**, same commit. **FOUR** tracked artifacts moved, not the two predicted; the two book files' diffs are the 32 replacements and nothing else, proven byte for byte |
| 3 — the live Wikisource edit | **DONE 2026-08-27 12:23–12:24 local**, `a31d0ec`. Six pages saved, the six diff links in the execution record below. The refreshed download matches the Phase 2 rehearsal byte for byte in all twelve chapters. The appendices check found what it expected: no ב2 there at all |
| 4 — emit the Google-Sheet auto-edits | **DONE 2026-08-27**, `1aa95ff`, pushed. **32 auto-edits**, one per sigil — no neighbour-merge and no whole-cell fallback. Both wsgo outputs went `[]` → 32 Daniel entries |
| 5 — the Sheet round trip, then regenerate | **DONE 2026-08-27.** Ben ran the two Apps Script items; `8fe3dff` here, `46209cd` in MAM-parsed, `c4dd986` in MAM-with-doc, all pushed. **The lint is GREEN — this plan's completion criterion is met.** Both wsgo outputs back to `[]` |
| 6 — correct the two sigil documents | **DONE 2026-08-27**, `f58716e` here and `80f4a3f` in MAM-with-doc. Four places in `doc/sigil-decoding.md` plus one ripple `c691af8` created, and the one hand-maintained row in `MAM-with-doc/gh-pages/sigil-decoding.html` |
| 7 — the trackers | **NOT STARTED** |

## Context

MAM's manuscript sigil ב2 and its sigil ת451 name the **same** manuscript. The MAM editor
(`skadish1`) said so himself on 2026-04-09, in
[this #259 comment](https://github.com/bdenckla/MAM-basics/issues/259#issuecomment-5432094840): he
first chose ב2 for its proximity to ב1, then abandoned it because ב2 is used in the literature for
other things and the manuscript is not in the British Library, and switched to the number the
manuscript carried when Meir Benayahu held it — but by then many uses of ב2 were already written
and he never updated them. On 2026-04-10 he answered Ben's "shall I replace all uses of ב2 with
ת451?" with *"Yes, please."*
([this #260 comment](https://github.com/bdenckla/MAM-basics/issues/260#issuecomment-5432095104)),
and on 2026-08-27 restated it on #259: *"Change all ב2 to ת451."*

The replacement is to be made **in Hebrew Wikisource**, which is the source MAM is edited in, and
then carried through `doc/process-documentation/auto-edits-process.md`'s chain so that MAM-parsed
and everything published from it follow. That chain matters more than it looks: `main_0_mega.py`'s
first step is `parse-go`, so **MAM-parsed derives from the Google Sheet, not from Wikisource**. A
Wikisource edit on its own changes nothing that is published, and leaves `main_diff.py wsgo`
non-empty until the Sheet catches up.

Both `doc/sigil-decoding.md` and `MAM-with-doc/gh-pages/sigil-decoding.html` currently assert the
opposite conclusion — that the local evidence *leans against* ב2 = ת451 — so correcting them is
part of this work rather than a follow-up to it.

## Baselines — measured 2026-08-27

Repo heads, all working trees clean:

| Repo | HEAD |
|---|---|
| `C:\Users\BenDe\GitRepos\MAM-basics` | `d7df398` |
| `C:\Users\BenDe\GitRepos\MAM-parsed` | `0128e69` |
| `C:\Users\BenDe\GitRepos\MAM-with-doc` | `4f4c9ab` |
| `C:\Users\BenDe\GitRepos\MAM-simple` | `b3c7a60` |
| `C:\Users\BenDe\GitRepos\MAM-OSIS` | `2f783d1` |
| `C:\Users\BenDe\GitRepos\MAM-for-Sefaria` | `cf19347` |
| `C:\Users\BenDe\GitRepos\MAM-private` | `580fecc` |

| Measure | Value |
|---|---|
| suite | **941 passed, 5 skipped, 59 subtests** — the figure `doc/review-findings-2026-08-26.md` records at `629d73b`. Re-measure; a mismatch is a finding. **Superseded 2026-08-27: 951/5/59 at `87d37b7`**, the ten being `test_repo_visibility_declared.py`, added by `6cb65ef` after this plan measured |
| wsgo outputs | `out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json` both `[]`, so any wsgo output this work produces is its own |
| ב2 as a sigil | **32 occurrences, all in `in/mam-ws/F1-Daniel.json`** — **understated, corrected 2026-08-27: a further 32 stand in `in/mam-go/F-KetAx.csv`**, the Google Sheet's own copy of the same cells, and 32 in each of the three `out/` serializations of Daniel. Phase 5 below already expects the Sheet's 32 to go; it is this row that undercounted. The Phase 1 lint reports **64** across the two `in/` trees it scans |
| ב2 not as a sigil | **648 occurrences**, none of them touchable — see the four classes below. **Did not reproduce, 2026-08-27**: no whole-tree count yields 648. What did reproduce exactly is class 1's 432 — 216 across the five Torah books of `in/mam-ws/` plus the same 216 in `in/mam-go/A-Torah.csv`. 648 is 216 × 3, which is exactly class 4's three `out/` serializations of the Torah, so the figure appears to count those rather than every non-sigil occurrence. Nothing in the design turns on it: both guards are per-page |
| ת451 in Daniel | **5 occurrences**, in chapters ג, ה, ו — disjoint from every ב2 chapter |
| pywikibot config | **`C:\Users\BenDe\.pywikibot\` DOES NOT EXIST** — neither `user-config.py` nor `password.py`, so `main_ws_bot.py real` fails fast |

Run the suite from the repo root, never from `py/`, and keep the `-q` — default verbosity drops the
subtests count and reads as a mismatch:

```bash
.venv/Scripts/python.exe py/main_test.py -q
```

Load before the prose edits of Phase 6: the `hebrew-prose` skill.

## What is actually there — re-measure, do not trust these figures

The sigil occurs in **exactly one book**, over six of Daniel's twelve chapters:

| Chapter | Hebrew | ב2 occurrences |
|---|---|---|
| 7 | ז | 17 |
| 8 | ח | 2 |
| 9 | ט | 3 |
| 10 | י | 3 |
| 11 | יא | 6 |
| 12 | יב | 1 |
| — | total | **32** |

Three facts make a plain string replacement exact:

1. **Every one of the 32 is preceded by a comma.** The sigil is never the first member of an
   authority list, always a later one.
2. **No occurrence is followed by a digit.** The following characters are `,` (15), space (12),
   `?` (2), `(` (1), `)` (1), `=` (1). So the sigil is always a whole token; there is no ב20 and
   no ב21 to guard against.
3. **The two sigils never share a chapter.** Daniel's five ת451 occurrences are in chapters ג (1),
   ה (2) and ו (2). So no note can end up naming ת451 twice, and none can end up asserting two
   different readings for one manuscript.

Re-derive all of that with a throwaway script under `.novc/` — a Python script, not assembled
shell, per `~/.claude/CLAUDE.md`. Read `in/mam-ws/F1-Daniel.json` (a dict from Hebrew chapter to a
list of lines), count `"\N{HEBREW LETTER BET}2"` per chapter, and tabulate the character before and
after each occurrence.

### Four classes of ב2 that are NOT the sigil and must not be touched

This is why a global find-and-replace across the corpus would be a disaster. Outside Daniel the
string occurs 648 more times and not one of those is a sigil:

1. **The aliyah template's named parameter.** 216 occurrences across the five Torah books of
   `in/mam-ws`, inside `{{מ:עלייה|א=…|ב0=…|ב1=…|ב2=כהן}}` — Genesis 48, Exodus 44, Leviticus 40,
   Numbers 40, Deuteronomy 44 — plus the same 216 in `in/mam-go/A-Torah.csv` and again in every
   parsed serialization of the Torah under `out/` and in MAM-parsed's `plain/` and `plus/`.
   **Distinguishing feature: the aliyah parameter is always preceded by `|` and followed by `=`,
   where the sigil is always preceded by `,`.**
2. **Verse-reference disambiguators in Ben's authored Wikisource intro** — "verse ב, second
   occurrence" and the like, in `py/author_misc/he_ws_intro_to_mam_pasleg.mediawiki` and
   `py/author_misc/he_ws_intro_to_mam_pasleg_footnotes.py`. These are preceded by a comma, exactly
   like the sigil. That page is not a MAM book chapter, so the bot never visits it; the safety
   here comes from the bot's page selection, not from the search string.
3. **The same aliyah parameter names as Python string literals**, in
   `py/tmpl_survey/column_d_0_store_the_mpasuq_call.py` and its `_plus.py` twin, which index
   `named_params` by `"ב0"`, `"ב1"`, `"ב2"`, `"ב3"`.
4. **Generated artifacts that merely echo class 1** — `out/mam-ws-bot/proto*/A*.json`,
   `out/mam-ws-parsed-fmt-2/A*.json`, and MAM-parsed's Torah `plain/` and `plus/`.

## Approach

A new **untargeted global page transform** for the existing JSON-driven Wikisource bot, guarded by
a per-chapter expected-count table.

Not the bot's existing `explicit-replacement` kind, which a fresh session will otherwise reach for
first. It asserts each `old` string occurs **exactly once** per chapter, so all 32 entries would
need enough surrounding pointed Hebrew to be unique — chapter ז alone repeats
`ש1,ק-מ,ב1,ב2 ובדפוסים` four times — and 32 hand-typed Hebrew context strings is precisely the
fiddly work that goes wrong silently. A counted transform is also the stronger guard, because it
checks the total as well as each site.

## Phase 1 — the bot edit, in this repo

Runs in the main clone (`C:\Users\BenDe\GitRepos\MAM-basics`), not a worktree. Files to add:

1. `py/ws/ws_bot_edit_sigil_b2_to_t451.py` — the transform. Follow
   `py/ws/ws_bot_edit_kq_triv_rename_extra_alef_sug.py`, the shortest existing example of the same
   shape: `edit_page_text(bk39id, he_chnu, page_text)` plus `get_warnings()`. Write both sigils as
   named escapes, never as bare literals — `"\N{HEBREW LETTER BET}2"` and
   `"\N{HEBREW LETTER TAV}451"`. Behavior:
   - hold `_EXPECTED = {"Daniel": {"ז": 17, "ח": 2, "ט": 3, "י": 3, "יא": 6, "יב": 1}}`;
   - for a `(bk39id, he_chnu)` pair not in that table, return `page_text` **unchanged**;
   - for a pair that is, assert the page contains no aliyah parameter `|ב2=` (a page carrying one
     is not a page this transform may touch), assert `page_text.count(B2)` equals the expected
     number, then `page_text.replace(B2, T451)`;
   - append a per-chapter record to the warnings list, so the run's `misc/warnings.json` carries
     the counts actually applied.
2. `in/mam-ws-bot-edits/sigil-b2-to-t451.json` — the spec, in the two-line shape of
   `in/mam-ws-bot-edits/kq-trivial-2-rename-extra-alef-sug.json`:
   ```json
   {
     "summary": "Replace sigil ב2 with ת451 in Daniel doc-notes (one manuscript, two sigils), per MAM-basics#260",
     "edit-kind": "sigil-b2-to-t451",
     "edits": {}
   }
   ```
3. `py/tests/test_ws_bot_sigil_b2_to_t451.py` — pin the edit payload before it is sent. This is
   the `ws_bot` exception `CLAUDE.md` grants to the testing rule: a Wikisource edit is
   irreversible and outward-facing, with no regeneratable artifact to diff afterwards. Model it on
   `py/tests/test_ws_bot_kq_triv_rename_extra_alef_sug.py`. Cover a comma-list occurrence; the
   `ב2?` and `ב2?[…]` uncertainty-marker forms; the one occurrence followed by `=`; a Torah page
   carrying `|ב2=כהן` passing through untouched; and a wrong count raising.
4. `py/tests/test_sigil_b2_not_a_sigil_anywhere.py` — a lint over the source tree, the second
   sanctioned test shape. Assert that in every file under `in/mam-ws/` and `in/mam-go/`, every
   occurrence of ב2 is preceded by `|` and followed by `=`. That passes all 216 aliyah parameters
   and fails all 32 sigils, so it is **red until Phase 5 completes** and is this plan's completion
   criterion. It also guards the real recurrence channel: the Google Sheet holds its own copy of
   these cells, and finding 1 of `doc/review-findings-2026-08-26.md` is the standing example of
   Sheet content arriving again on every download.

Files to edit:

5. `py/ws/ws_bot_edit.py` — register the new kind. Add the import and an entry in
   `_UNTARGETED_EDIT_KINDS` (anchor: the dict literal holding
   `"kuk-special-callsite-migration"`), and add a paragraph to the module docstring beside the
   other per-kind paragraphs.
6. `py/ws/ws_bot_edit_history.md` — append an era entry after "Issue 67: migrate deprecated כו״ק
   call sites", and move that entry's "— current" marker onto the new one.

Mandatory before committing:

```bash
.venv/Scripts/python.exe -m black py/ws/ws_bot_edit_sigil_b2_to_t451.py py/ws/ws_bot_edit.py py/tests/test_ws_bot_sigil_b2_to_t451.py py/tests/test_sigil_b2_not_a_sigil_anywhere.py
```

## Phase 2 — rehearse locally, no live edit

```bash
.venv/Scripts/python.exe py/main_ws_bot.py proto --edits in/mam-ws-bot-edits/sigil-b2-to-t451.json --book39 Daniel
```

That rewrites two **git-tracked** artifacts, `out/mam-ws-bot/proto/F1-Daniel.json` and
`out/mam-ws-bot/proto-fmt-2/F1-Daniel.json`, so the tracked diff is the evidence. Expect exactly 32
changed sigils and nothing else: the proto roundtrip through fmt-2 is currently faithful for Daniel
(the sigil line numbers in `out/mam-ws-bot/proto/F1-Daniel.json` match `in/mam-ws/F1-Daniel.json`
exactly), so any other difference in that diff is a finding.

**Corrected 2026-08-27: it rewrites FOUR tracked artifacts, not two.**
`out/mam-ws-bot/proto-misc/warnings.json` and `out/mam-ws-bot/proto-misc/modified-chapters.json`
are tracked too, and both stood at `[]`. The first now carries the six per-chapter records Phase 1
above asks the transform to append, and the second the six chapters Phase 3 will save — in the
`{"book39": …, "chapter": …}` shape that `main_download.py fr-wikisource --book-chapters-json`
takes, so it is worth keeping rather than merely tolerating. Both were a consequence of this plan's
own Phase 1 design; only the count in the sentence above was wrong.

Pass `--book39 Daniel` and never a bare `proto` — a bare run rewrites all 39 books' proto outputs,
and a full-corpus diff would bury the 32 lines that matter.

Commit Phases 1 and 2 together, with the proto diff as the demonstration. Push. The new lint test
is expected red at this point; say so in the commit message rather than letting a later session
discover it.

## Phases 1 and 2 — execution record, 2026-08-27

Committed as `52aa7b8`, run in the main clone at `87d37b7` — three commits past the `d7df398` this
plan measured at. A
second session was co-present in the worktree `.claude/worktrees/vibrant-mirzakhani-3e2369`, on
`out/sigil-inventory.json`, `py/main_0_mega.py` and `py/sigils/inventory.py`; it merged that work
into `main` as `d5d9896` partway through this one. The two file sets are disjoint, the working tree
held only this work's paths throughout, and the push landed fast-forward.

**Every figure this plan gives about the sigil itself re-measured exactly.** 32 occurrences over
six chapters of Daniel — ז 17, ח 2, ט 3, י 3, יא 6, יב 1 — all 32 preceded by a comma, none
followed by a digit, the following characters being `,` (15), space (12), `?` (2), `(` (1), `)` (1)
and `=` (1); ת451 at 5, in chapters ג, ה and ו, disjoint from every ב2 chapter; and no `|ב2=`
anywhere in Daniel. The three rows of the Baselines table that did **not** re-measure are annotated
in place above: the suite count, the sigil's whereabouts, and the 648.

Two departures from the letter of Phase 1, both in spelling rather than behaviour:

1. **The count table is keyed by integer chapter and converted through
   `hebrew_verse_numerals.INT_TO_STR_DIC`**, rather than holding hand-typed Hebrew numerals. Same
   table, same six chapters; the reason is that the table doubles as a skip list, so a mistyped
   Hebrew key would not raise — it would silently pass its whole chapter through untouched, which
   is the one failure mode neither guard catches.
2. **`py/tests/test_ws_bot_sigil_b2_to_t451.py` asserts across two corpus states.** Its strongest
   test runs the transform over the real `in/mam-ws/F1-Daniel.json`, and Phase 3 below re-downloads
   that very file, so a single-state assertion would have gone red the moment Phase 3 landed — a
   test destroying itself halfway through its own plan. The invariant it asserts instead holds
   before and after: each table chapter carries either its counted ב2 and no ת451, or no ב2 and its
   counted ת451.

**The transform is one-shot, which follows from the expected-count table and is worth knowing
before Phase 3.** Once the live edit's re-download has refreshed `in/mam-ws/F1-Daniel.json`, a
table chapter holds zero occurrences, so re-running the proto rehearsal raises on the count
assertion rather than quietly doing nothing. That is the right failure for a bot era that runs
once; it is recorded here so it is not met as a surprise.

Phase 2's evidence, stronger than reading the diff: for both book artifacts, applying the
replacement to the `HEAD` blob reproduces the working-tree file **byte for byte**, so the diff
contains the 32 replacements and nothing else — no normalization noise, no reordering, no
whitespace drift. ב2 went 32 → 0 and ת451 5 → 37 in each.

## Phase 3 — the live Wikisource edit (Ben's step)

Six pages change, all of them `/טעמים` subpages of Daniel chapters 7 through 12. The other six
Daniel chapters are visited and pass through unchanged, so nothing is saved for them.

First, if `C:\Users\BenDe\.pywikibot\` is still absent, set it up per `py/ws/pywikibot-setup.md`:
copy `py/ws/pywikibot-user-config.py` to `user-config.py`, and create `password.py` holding
`("BDencklaBot", "<password>")`.

The dry run is **expected to fail**, listing exactly those six chapters, because `--no-save` treats
"a chapter would change" as an error. That failure is the pre-flight result, not a problem:

```bash
.venv\Scripts\python.exe py\main_ws_bot.py real --edits in/mam-ws-bot-edits/sigil-b2-to-t451.json -dir:$env:USERPROFILE/.pywikibot --book39 Daniel --no-save
```

The live run:

```bash
.venv\Scripts\python.exe py\main_ws_bot.py real --edits in/mam-ws-bot-edits/sigil-b2-to-t451.json -dir:$env:USERPROFILE/.pywikibot --book39 Daniel
```

It writes run artifacts under `.novc/mam-ws-bot-real-runs/<timestamp>/`, including
`misc/modified-chapter-diffs.md` — the six Wikisource diff links, which Phase 7 wants — and
`misc/warnings.json`. By default it then re-downloads the six modified chapters into
`in/mam-ws/F1-Daniel.json` and reparses Daniel; do **not** pass `--no-post-download`.

While on Wikisource, also check whether any non-book page uses ב2 as a sigil. The bot only visits
book chapters, so an appendix or introduction use would be left dangling. Fetch the appendices
verbatim, save the file, and grep the saved file — do not use a summarizing fetch, which on
2026-08-06 merged two neighbouring entries and reported a gloss that was not there. The URL is the
appendices title with `&action=raw`, about 144,000 characters; `doc/sigil-decoding.md`'s "Source
Hierarchy" section carries the title and the same warning. That document records that the appendix
has an entry for ת451 (as `כתי"ת451`) and **none at all** for ב2 as of 2026-08-06, so the expected
result is that nothing needs adding there. A different result is a finding for #259.

Commit the refreshed `in/mam-ws/F1-Daniel.json` and the regenerated
`out/mam-ws-parsed-fmt-2/F1-Daniel.json`. Push.

## Phase 3 — execution record, 2026-08-27

Ben ran both commands in his integrated terminal; this session verified the results. Run
artifacts are under `.novc/mam-ws-bot-real-runs/20260827-121725-669570` (the dry run) and
`.novc/mam-ws-bot-real-runs/20260827-122332-348995` (the live run).

**The dry run failed exactly as this plan predicted, naming those six chapters and no others.**
It visited all twelve, so the six that pass through unchanged were exercised too. Its
`misc/warnings.json` recorded 17, 2, 3, 3, 6 and 1 against text fetched from the live wiki, which
is the count table confirmed against Wikisource rather than against the local snapshot. Its
post-transform text was then compared chapter by chapter against
`out/mam-ws-bot/proto/F1-Daniel.json`: **identical in all twelve**, so the live pages had not
drifted from the snapshot and the save was known in advance to produce what Phase 2 had already
committed.

**The six pages, with the diff links Phase 7 wants** (they are `misc/modified-chapter-diffs.md`
of the live run, kept here because `.novc/` is not tracked):

| Chapter | Page | Diff |
|---|---|---|
| 7 | דניאל ז/טעמים | [oldid 2988419](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%96%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=2988419) |
| 8 | דניאל ח/טעמים | [oldid 2988420](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%97%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=2988420) |
| 9 | דניאל ט/טעמים | [oldid 2988421](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%98%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=2988421) |
| 10 | דניאל י/טעמים | [oldid 2988422](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%99%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=2988422) |
| 11 | דניאל יא/טעמים | [oldid 3008060](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%99%D7%90%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=3008060) |
| 12 | דניאל יב/טעמים | [oldid 2988424](https://he.wikisource.org/w/index.php?title=%D7%93%D7%A0%D7%99%D7%90%D7%9C_%D7%99%D7%91%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=next&oldid=2988424) |

**Page titles use a space, not a slash, between book and chapter** — `דניאל ז/טעמים`, url-encoded
with an underscore. Recorded because this session twice wrote them as `דניאל/ז/טעמים` before the
dry run's own output corrected it.

The post-download and reparse ran as intended, since `--no-post-download` was not passed, and moved
exactly the two files this plan named. The refreshed `in/mam-ws/F1-Daniel.json` matches the Phase 2
rehearsal in **all twelve chapters**, and both it and the reparsed
`out/mam-ws-parsed-fmt-2/F1-Daniel.json` now hold **ב2 at 0 and ת451 at 37** — the 5 that were
already in chapters ג, ה and ו, plus the 32 replaced. So the Wikisource round trip introduced
nothing of its own.

**The appendices check came out as this plan expected, so there is no finding for #259.** The
wikitext was fetched verbatim with `action=raw` and saved before being searched, per the warning in
`doc/sigil-decoding.md` about the 2026-08-06 summarizing fetch — 145,802 characters over 559 lines.
It holds **no ב2 at all**, so the bot left nothing dangling on a page it does not visit, and **two
occurrences of ת451**, both spelled `כתי"ת451`, at lines 94 and 163. The second corroborates the
editor's own account independently: it glosses the manuscript as
`ספריה לא ידועה, לשעבר כת"י מאיר בניהו T 451` — unknown library, formerly Meir Benayahu Ms. T 451.

**The Google Sheet is untouched, as it must be at this stage**: `in/mam-go/F-KetAx.csv` still holds
its own 32 occurrences of ב2. That is what Phases 4 and 5 exist to fix, and it is why the Phase 1
lint stays red — it now reports 32 rather than 64, the Wikisource half having gone.

## Phase 4 — emit the Google-Sheet auto-edits

```bash
.venv/Scripts/python.exe py/main_diff.py wsgo
```

Wikisource and the Sheet now disagree, so `out/diff_mamws_mamgo.json` and
`out/diff_mamws_mamgo-auto-edits.json` go from `[]` to Daniel entries. Each auto-edit should be
column `E` (verse-body), tab `כתובים אחרונים`, its `search_str` naming ב2 and its `replace_str`
naming ת451.

Read the file rather than trusting the count. `py/diff_wsgo/wsgo_auto_edits.py` merges a search
string that is not unique within its cell into its neighbour, and falls back to a whole-cell
replacement — printing "Reverting to whole Wikitext sequence as diff" — when it cannot make the set
apply cleanly. So an entry count above or below 32 can be legitimate; what must hold is that
applying the set to the Sheet's text reproduces Wikisource's, which is what that module already
asserts before returning.

Commit and push both files. The Google Apps Script fetches the auto-edits file from GitHub, so an
unpushed commit is a broken step, not merely an untidy one.

## Phase 4 — execution record, 2026-08-27

`1aa95ff`, committed **and pushed**. Both outputs went from `[]` to **32 entries** each.

**32 is the happy case rather than the only acceptable one, and it is worth saying which
happened.** `py/diff_wsgo/wsgo_auto_edits.py` merges a search string that is not unique within its
cell into its neighbour, and falls back to a whole-cell replacement when it cannot make the set
apply cleanly. Neither fired: "Reverting to whole Wikitext sequence as diff" was not printed once,
and the auto-edits stand one per sigil.

Read rather than counted, as this plan asks. All 32 are column `E`; all carry
`"sena": "כתובים אחרונים"`, which is the field the plan's "tab" means; and every `replace_str` is
its own `search_str` with the sigil swapped and nothing else touched — zero exceptions, and no
`replace_str` still holding ב2.

**The 32 entries of `out/diff_mamws_mamgo.json` reproduce the per-chapter counts from the far end
of the pipeline**, which is worth more than the total agreeing. Their `bcv` values run `Da7:4` to
`Da12:2` and distribute as 17, 2, 3, 3, 6 and 1 over chapters 7 through 12 — the same figures the
transform's own table holds, now arrived at by comparing two independently-derived corpora rather
than by counting one. All 32 are `"field": "verse-body"` and `"sena": "KetAx"`; every `ws-full`
holds ת451 and every `go-full` holds ב2, so no book but Daniel appears.

One incidental check, since `main_diff.py` has no `sys.stdout.reconfigure` either: its `wsgo`
progress output is ASCII book names only, so it does not need one and none was added. That is the
opposite finding from `main_ws_bot.py`'s, and it is why the rule is to look rather than to add the
two lines everywhere.

## Phase 5 — the Sheet round trip (Ben's step) and regeneration

Steps 4 through 6 of `doc/process-documentation/auto-edits-process.md` happen inside the MAM Google
Sheet and cannot be done from a checkout: open the Sheet, run "Import auto-edits from GitHub", then
run "Apply imported auto-edits". Then, back in `MAM-basics`:

```bash
.venv/Scripts/python.exe py/main_download.py fr-google
```

Expect `in/mam-go/F-KetAx.csv` to lose its 32 sigils, and MAM-parsed's `plain/F1-Daniel.json` and
`plus/F1-Daniel.json` to follow. Then confirm the loop closes — both wsgo outputs must return to
`[]`:

```bash
.venv/Scripts/python.exe py/main_diff.py wsgo
```

Then rebuild everything downstream of MAM-parsed:

```bash
.venv/Scripts/python.exe py/main_0_mega.py
```

and, separately, the one tracked sigil artifact the mega does not regenerate:

```bash
.venv/Scripts/python.exe py/main_sigil_inventory.py
```

That second command is needed because `py/main_sigil_inventory.py` is absent from
`main_0_mega.py`'s `_STEPS` list, so `out/sigil-inventory.json` goes stale unless it is run by
hand — the same gap the mega's own comments describe having closed for eight other artifacts on
2026-08-04. A separate task was spawned for that on 2026-08-27 to add the step; if it has landed by
the time this phase runs, the mega covers it and the second command is a no-op. Run it anyway and
check.

Then commit in each repo that moved, and push each one.

## Phase 5 — execution record, 2026-08-27

Ben ran the Sheet's two Apps Script items; this session ran the four commands and verified.
Commits: `8fe3dff` here, `46209cd` in MAM-parsed, `c4dd986` in MAM-with-doc, all pushed.

**`py/tests/test_sigil_b2_not_a_sigil_anywhere.py` is GREEN, so this plan's completion criterion
is met.** ב2 survives nowhere under `in/mam-ws/` or `in/mam-go/` except as the Torah's 216 aliyah
parameters. Its trajectory across the phases is the clearest summary of what happened: **64** when
`52aa7b8` committed it red, **32** after the Wikisource edit of `a31d0ec`, **0** now.

**This is the phase where anything published actually moved**, the point the Context section makes
about `parse-go`. `in/mam-go/F-KetAx.csv` went ב2 32 → 0 and ת451 6 → 38; MAM-parsed's
`plain/F1-Daniel.json` and `plus/F1-Daniel.json` followed to 0 and 37. `in/mam-go/A-Torah.csv`
still holds all **216** aliyah `ב2=` parameters, which is the check worth stating rather than
assuming — it is what a global replace would have destroyed.

Both wsgo outputs return to `[]`, so the loop closes and `1aa95ff`'s 32 auto-edits have done their
work.

**Two artifacts moved for reasons that are not the replacement, and both are benign.**
`out/mam-ws-bot/proto-misc/modified-chapters.json` returns to `[]` because `main_0_mega.py` runs
the proto bot with no edit spec, so its transform is the identity and it records no modified
chapters; the proto book outputs are unchanged, their input being already repointed, and only the
run metadata resets. `out/explicit-xataf-extras.json` went ב2 2 → 0 and ת451 0 → 2, the sigil swap
alone explaining its whole diff.

**`out/sigil-inventory.json` bears on verification item 4 below, which needs one word added.** ב2
is gone from all three sections — expressions, expression_tokens and prose_tokens, zero items
containing it anywhere. ת451 rises 6 → 33 in expression_tokens and 10 → 42 in **prose_tokens**, and
prose_tokens is where the predicted rise of exactly 32 holds. The expression_tokens rise is 27; the
five sites between the two figures are the ones whose surrounding punctuation keeps them out of the
expression tokenizer — the parenthesized `ב2(ית' י')`, the bracketed `ב2?[…]`, and the one followed
by `=`. Header counts move with them: `distinct_expression_tokens` 2371 → 2370 and
`distinct_prose_tokens` 678 → 677, while `distinct_expressions` holds at 1721, no repointed
expression having collided with an existing ת451 one.

**`py/main_sigil_inventory.py` is now a no-op, so that instruction can be dropped from future
runs.** `e37b8ad` wired it into the mega earlier the same day, which this plan anticipated as
possible; re-running it after the mega leaves the artifact byte-identical, checked by hash rather
than by eye.

Verification item 5 passed. Daniel 8:2's note on the published page now reads
`ל,ש1,ק13,פטרבורג-EVR-II-B-92=וַיְהִי֙ (אין געיה) וכמו כן בכתבי־היד התימנים (ק-מ,ב1,ת451).` — the
sigil replaced in place, mid-list, and the Hebrew sentence intact. Read with the Read tool off
`../MAM-with-doc/gh-pages/F1-Daniel.html`, no browser opened.

**MAM-simple, MAM-OSIS and MAM-for-Sefaria did not move**, as "What is NOT expected to change"
requires: they carry no ב2 at all and stayed at zero.

**A second session was live in this clone throughout, and this is the collision case
`~/.claude/CLAUDE.md` describes.** It was editing `doc/sigil-decoding.md` for issue #262 and
committed it as `c691af8`, "Act on Avi's #262 answer: decode the siglum dalet, retire the siglum
lamed-dalet", between this session's staging and its commit. No collision occurred, because the
remedy is the cheap one that file already prescribes: stage your own paths **by name**, then check
that nothing else is pending. **Phase 6 must be planned against `c691af8` rather than against what
this plan saw on 2026-08-27 morning** — its four anchors are quoted rather than numbered so they
should still resolve, but the ב2 section now sits beside a freshly written account of another
retired siglum, and the two accounts should be read together before either is edited.

## Phase 6 — correct the two documents that now assert the opposite

Load the `hebrew-prose` skill first.

In `doc/sigil-decoding.md`, four places. Search for the anchors quoted below rather than for line
numbers, which will have drifted:

1. The ת451 row of "Manuscript Sigla" (anchor: `formerly Meir Benayahu Ms T 451`). Its Notes cell
   currently ends *"This bears on the ב2 question below: the appendix has an entry for ת451 and
   none at all for ב2."* Replace that sentence with the resolution, and with the reason the
   appendix is silent: ב2 was an abandoned sigil for this same manuscript, so it was never given
   an entry of its own.
2. The `### ב2` section. **Keep the heading** — the "2026-08-26 run" subsection further down cites
   ב2 as one of three sigils documented under a `###` heading rather than in a table, and that
   citation has to keep resolving. Rewrite the body: `skadish1`'s own account of the two sigils,
   the dates he gave it, the replacement, and **why this file's earlier inference was wrong**. The
   negative evidence was that Daniel carries separate `ק-מ,ת451` and `ב1,ק-מ,ת451` expressions,
   and an incomplete rename explains that exactly as well as two distinct manuscripts would.
   State that plainly: the file reasoned carefully from local corpus evidence to a conclusion the
   editor's own testimony overturned, which is a standing lesson about the limits of
   corpus-internal inference.
3. The "Current Inventory-Derived Target Set" table (anchor: `| Form | Priority |`). Its single row
   is ב2, so with ב2 resolved the table has no rows left. Do not leave an empty table and do not
   silently delete the section: say that the target set is now empty, and note that the
   neighbouring subsection's "Until 2026-08-06 the table above listed ב2 alone, which read as 'one
   sigil left to decode'" is a warning against exactly the complacency an empty table invites.
4. Add a short "Retired sigla" note under "Confirmed Items", recording that ב2 means ת451 in any
   pre-replacement text. The sigil survives in Wikisource page history, in MAM's Sefaria and
   Accordance derivatives until those refresh, and in this repo's own git history, so a reader
   meeting it still needs to be able to decode it. Give the count, the six Daniel chapters, and
   the date.

In `..\MAM-with-doc\gh-pages\sigil-decoding.html`, one place: the table row whose first cell is
`<bdi lang="hbo">ב2</bdi>`. Rewrite that row — the meaning becomes ת451, the status becomes
Confirmed, and the Notes cell records that the corpus was repointed and that the old sigil may
still be met in older text. **That page is hand-maintained, not generated**: its own workflow note
at the top says so and asks that edits merge into the current HTML rather than replace it
wholesale, so edit the row in place and keep the existing `<bdi lang="hbo">` and `class="nowrap"`
conventions.

Out of scope, recorded so it is not mistaken for an oversight: that HTML page still cites
MAM-with-doc issues 6 and 8, which the 2026-08-26 transfer turned into MAM-basics #257 and #259.
Both resolve through GitHub's transfer redirect, and repointing them belongs to #259's
documentation pass.

## Phase 6 — execution record, 2026-08-27

The `hebrew-prose` skill was loaded first, as this plan requires. All four anchors this plan gives
resolved unchanged: `c691af8` had touched nine regions of `doc/sigil-decoding.md` and none of them
was a Phase 6 target.

**`c691af8` changed what to write, though, in the one way worth recording.** It added item 6 to
"Source Hierarchy" — Avi Kadish's issue answers as a source that outranks the five documentary
ones, and that can settle what no document can, "because a sigil MAM used at one stage and later
abandoned leaves no trace in an appendix that describes the finished edition". That is the ב2 case
stated in general before this phase reached it, so the four edits **cite item 6 rather than
re-deriving the lesson**, which would have been its third telling in one file.

The four edits, plus two more the work turned out to need:

1. The ת451 row keeps its observation and reverses its meaning. "The appendix has an entry for
   ת451 and none at all for ב2" now introduces the reason rather than a doubt.
2. The `### ב2` section keeps its heading, as this plan requires, and its body is rewritten:
   Avi Kadish's account with its dates, the replacement, and why the earlier inference failed.
   **Most of that entry holds up and is said to**; what failed is the last step only, and it
   failed on a real observation — an incomplete rename explains Daniel's separate `ק-מ,ת451` and
   `ב1,ק-מ,ת451` exactly as well as two manuscripts do, and the corpus cannot tell the two
   explanations apart.
3. The "Current Inventory-Derived Target Set" table is replaced by prose saying the set is empty
   **because the question was answered, not because the row was dropped**, and pointing at the
   neighbouring subsection as the warning against reading an empty table as "nothing left".
4. A `### Retired sigla` subsection under "Confirmed Items", with the count, the six chapters, the
   date, and where ב2 can still be met. It says why it is not simply another row in the manuscript
   table beside `ד`'s: the corpus still has `ד` at eleven sites, so that row is a decoder for MAM
   as it stands, where ב2 is a decoder for older text only.
5. **A ripple `c691af8` created and this plan could not have known about.** The "2026-08-26 run"
   subsection warns that `ק-מ`, `ב2` and `ל-מ` are documented under `###` headings and in no table,
   so a table-only parse reports all three as undecoded. Giving ב2 a Retired-sigla row makes that
   false for ב2, so the sentence now carries a parenthesis saying so and confirming the warning
   still stands for the other two.
6. `MAM-with-doc/gh-pages/sigil-decoding.html`'s one ב2 row, edited in place per that page's own
   workflow note, keeping its `<bdi lang="hbo">` and `class="nowrap"` conventions. Status goes
   Provisional → Confirmed.

Checks: the repo's `test_prose_conventions` lint passes; the HTML parses with no unclosed or
mismatched tags, 28 `<tr>` and 79 `<td>` balanced, one ב2 row; and a scratch check confirmed that
no added line's first strong character is Hebrew except the two table rows, where a cell of its own
is the form the `hebrew-prose` skill prescribes.

**One thing seen and deliberately not fixed**: two rows of that HTML page neighbouring ב2's call
manuscripts "a Yemenite witness" and "a Sephardic witness", and the `hebrew-prose` skill bans
"witness" outright. They are pre-existing and outside this phase, which is scoped to the one row.
Worth a separate pass over that page.

## Phase 7 — the trackers

1. Comment on #260 with the six Wikisource diff links from `misc/modified-chapter-diffs.md`, the
   count, and the corrected reasoning; then close it. Cite repo files as blob/main markdown links,
   not bare backticked paths.
2. Comment on #259 that its ב2 bullet is resolved by replacement rather than by documentation, and
   that the remaining eight sigils of its first candidate batch are untouched by this work.
3. Leave #257 alone unless the workstream's scope picture changed. `doc/sigil-decoding.md`'s own
   Maintenance Notes ask that per-sigil changes not be mirrored into the umbrella.

## Verification

1. `.venv/Scripts/python.exe py/main_test.py -q` green, above the 941 baseline by however many test
   functions the two new files hold. Re-measure rather than predicting the number.
2. `py/tests/test_sigil_b2_not_a_sigil_anywhere.py` passes — zero sigil-shaped ב2 under
   `in/mam-ws/` and `in/mam-go/`, with all 216 aliyah parameters still present.
3. `.venv/Scripts/python.exe py/main_diff.py wsgo` leaves both outputs `[]`.
4. `out/sigil-inventory.json` has no ב2 entry, and its ת451 count has risen by 32.
5. Read one repointed note end to end on the published page. Daniel 8:2's prose said
   `וכמו כן בכתבי־היד התימנים (ק-מ,ב1,ב2)` and should now name ת451 in that list while still
   reading as a coherent Hebrew sentence. Hand Ben a `file:///` link to
   `C:/Users/BenDe/GitRepos/MAM-with-doc/gh-pages/F1-Daniel.html` and verify the content with the
   Read tool; do not open a browser.
6. `black --check` and `ruff check py` clean on the files touched.

## What is NOT expected to change

Anything in this list moving is a finding, not noise:

1. The 216 aliyah `ב2=` parameters, in `in/mam-ws/A*.json`, `in/mam-go/A-Torah.csv`, MAM-parsed's
   Torah `plain/` and `plus/`, and every `out/` serialization of the Torah.
2. `py/author_misc/he_ws_intro_to_mam_pasleg.mediawiki` and its `_footnotes.py` — verse references,
   not sigils.
3. `py/tmpl_survey/column_d_0_store_the_mpasuq_call.py` and its `_plus.py` twin.
4. Any book but Daniel, in any repo. MAM-simple, MAM-OSIS and MAM-for-Sefaria carry no ב2 at all
   and should stay at zero; if a mega run moves them, it moved them for some other reason.
5. Daniel chapters 1 through 6, on Wikisource and locally — the five existing ת451 occurrences in
   chapters ג, ה and ו included.

Two further notes on scope.

**No Unicode normalization is involved and none may be introduced.** Both sigils are a plain Hebrew
letter followed by ASCII digits, with no combining marks, so nothing here goes near
`unicodedata.normalize`, which `CLAUDE.md` forbids over Hebrew outright.

**The replacement is strictly in place.** So `ש1,ק-מ,ב1,ב2` becomes `ש1,ק-מ,ב1,ת451`, which leaves
ת451 mid-list in the 15 cases where another sigil follows, whereas Daniel's five existing ת451
expressions happen to put it last. MAM's authority lists are not consistently ordered anyway
(`ש1,ק-מ,…` and `ק-מ,ש1,…` both occur), and repositioning a sigil would be an editorial change
`skadish1` did not ask for.
