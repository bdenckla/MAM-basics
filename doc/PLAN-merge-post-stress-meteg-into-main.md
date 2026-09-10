# Merge `main` into `post-stress-meteg`, then integrate and push

State: executed 2026-09-08; merge 825cef66; retained as a review record.

Written 2026-09-08 for a fresh session. The branch is finished; only its integration remains,
and that integration is a real two-way merge rather than a closing step, because both sides
rewrote the same generator after they diverged.

**CORRECTION, 2026-09-09: THE MERGE THIS PLAN DESCRIBES WAS EXECUTED, AND THE CENSUS FIGURES
IN "WHAT MUST NOT CHANGE" ARE HISTORICAL.** The 263,191 words and 14,752 MBS_O chanted words
were the branch's, before the merge brought `main`'s qamats-variant fix in; the tracked survey
counts 262,819 words and, since 2026-09-09, 14,635 MBS_O chanted words — 14,614 between the
merge and that date, the census having identified a chanted word by its form until then, so
that 21 prose forms occurring twice in one numbered verse each read as one chanted word.
The MAS figures the section names, 232 as 178 prose and 54 poetic, and the type and fit-model
figures are current. `doc/post-stress-meteg-method.md` has the correction in full.

## Checkout, and how to verify it

Work in **`C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg`**, branch
**`post-stress-meteg`**. Do not create a new worktree. Do not write anything in the primary
clone `C:/Users/BenDe/GitRepos/MAM-basics` except the final fast-forward in step 9.

Before the first edit, check all four and compare against this file:

```powershell
git rev-parse --show-toplevel; git rev-parse HEAD; git branch --show-current; git status --porcelain
```

The branch head when this plan was written is **`a3e3f6eb`**, tree clean. A later head is fine
if `a3e3f6eb` is an ancestor; a head that does not contain it is a finding — stop and ask Ben.

## Python

The worktree has no `.venv`. Use the primary clone's, by absolute path, and set `REPOS_ROOT`
or sibling-repo resolution lands in the worktree's parent:

```powershell
$env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

## Load first

Invoke the **`hebrew-prose`** skill before touching any prose. `~/.claude/CLAUDE.md` and this
repo's `CLAUDE.md` load on their own; the repo file's section **"The post-stress-meteg pages say
plain 'word' — do not qualify it as 'chanted'"** is the rule this merge implements, and its
mark-order section matters because the conflicted files hold pointed Hebrew.

## The decision this merge implements

**Ben's decision, 2026-09-08: plain "word" stands on the nine post-stress-meteg pages.** They are
a deliberate exception to the `hebrew-prose` skill's "Never a loose 'word'" rule, licensed by the
skill's own clause that plain "word" survives wherever context settles the sense — the main page's
second paragraph defines both "word" and "atom" before any other sentence uses either.

`main`'s review-remediation Waves 2 and 5 went the other way and introduced "chanted word" into
these pages, 440 times across the eight pages `main` has. **That part of `main`'s work is reversed
for these nine pages and for nothing else.**

**Resolution rule, applied hunk by hunk:**

- The **branch** wins on the nine pages' reader-facing wording — prose, headings, tooltips, alt
  text, page titles.
- **`main`** wins on structure, on the survey module, and on everything outside these pages.
- Where a `main` hunk improves wording *and* changes terminology in the same breath, keep the
  improvement and drop the terminology change. `_FIT_FOR_MAS_CRITERIA` is the worked example:
  `main` turned `"Its word has penultimate stress from a conjunctive accent."` into
  `"The candidate chanted word has penultimate stress from a conjunctive accent."`, so the
  merged text should read `"The candidate word has penultimate stress from a conjunctive
  accent."`

## Two constraints on how the resolution is edited

1. **Never retype a Hebrew form, and never run `unicodedata.normalize` over one.** The conflicted
   files hold pointed Hebrew, and the Write and Edit tools reorder combining marks into
   Unicode-normal order where this repo's order is MAM-normal. Move an existing generator
   expression rather than re-keying it, and prefer a Python script doing byte-precise replacement
   for any edit whose text contains Hebrew. `.novc/check_mark_order_post_stress_meteg_20260908.py`
   is the check; `mb_cmn/uni_denorm.has_std_mark_order` is the authority.
2. **The same caution covers quotes.** These files mix straight and curly quotation marks, and the
   Edit tool has silently converted one to the other before. Quoted terms in rendered prose go
   through `author.dquote()` — see `py/mb_author/author.py` — and never through a typed curly
   quote. Do not touch `author.std_anchor`: it hardcodes period-inside quoting, this generator
   does not use it, and other pages do.

   **Clarification, 2026-09-09 (finding 16 / N8):** The recorded problem was a change
   between straight and curly quotation marks; the record does not establish the direction.

## Preconditions — re-measure each, and treat a mismatch as a finding

| Fact | Command |
| --- | --- |
| merge base `c73a2ad3` | `git merge-base HEAD main` |
| 8 branch commits `main` lacks, ending at `27f729e8` | `git log --oneline main..HEAD` |
| 12 `main` commits the branch lacks, `main` at `15ec6f4d` | `git log --oneline HEAD..main` |
| suite on the branch: 978 passed, 5 skipped | `py/main_test.py` |
| "chanted" in the branch's nine pages: 0 | `grep -c chanted gh-pages/post-stress-meteg*.html` |
| "chanted" in `main`'s eight pages: 440 | same, against `git show main:...` |

**Correction, 2026-09-09 (finding 7.1):** the eight MAS HTML blobs at `15ec6f4d`
contain 440 case-sensitive occurrences of `chanted` on 381 matching lines, remeasured
from all eight blobs. `grep -c` counts matching lines; it does not establish the
occurrence total in the table. Re-establish both totals by summing `text.count("chanted")`
and, separately, the number of lines containing `chanted` across those fixed blobs.
The earlier census correction at the top of this plan already records the merge's
changed survey figures; that correction remains intact.

**`main` is actively moving, so a HIGHER count on the `main` side is expected rather than a
finding.** It advanced twice on 2026-09-08 while this plan was being written, from `1a489a6e` to
`975a16c5` to `15ec6f4d`, and was fully pushed each time — another session is at work in the
primary clone. What must match is the **merge base** and the **branch** side; if the merge base is
no longer `c73a2ad3`, or the branch head does not contain `27f729e8`, stop and ask Ben. Re-check
`git rev-parse main origin/main` before step 9, with `git fetch` first, and expect the conflict
counts below to have grown with `main`.

## What must not change, and the trap inside it

The nine pages' figures, all of which the branch already renders:

- census **263,191** words, **14,752** MBS_O, **232** MAS (**178** prose, **54** poetic)
- types **123 / 60 / 42 / 7 = 232**
- fit for MAS **377** fit, **200** with MAS, **177** lacking, **53.1%**; 2Af **38 / 35 / 92.1% / 3**;
  2Bf **45 / 15 / 33.3% / 30**

**The trap: `main` still carries the OLDER fit model** — subtypes 2A/2B and the figures
384 / 200 / 184 / 52.1%. The branch's `97a1b46f` "Refine type 2 Fit-for-MAS criteria" is the newer
model and `main` lacks it. **If the merged tree regenerates to `main`'s figures, the merge has
silently lost `97a1b46f`** — that is a finding to fix by redoing the resolution, never by editing
prose to match the wrong numbers.

The eighth and ninth pages, `post-stress-meteg-next-conjunctive.html` (from `39133db0`) and its
φ4, exist only on the branch and must survive.

## The conflicts, as measured on 2026-09-08

`git merge --no-edit main` produced **13 conflicted files**:

- **Regenerate, never resolve by hand:** the eight `gh-pages/post-stress-meteg*.html` pages and
  `out/accgram/post-stress-meteg.json`. Take either side to clear the conflict, then overwrite by
  running the generator in step 3.
- **Resolve by hand:** `py/author_site/post_stress_meteg.py` (**32 hunks**),
  `py/author_site/site_data.py` (2), `py/main_authored.py` (3),
  `doc/post-stress-meteg-method.md` (1). `CLAUDE.md` may also conflict, the branch having added
  its plain-"word" section in `a3e3f6eb`; keep both sides' sections.

**Record, 2026-09-09 (finding 17a):** the 13 conflicted files and 32 author-module
hunks above already give the corrected counts. The September 8 review's read-only
merge calculation and Codex's reconciliation independently established those counts
for the parents of `825cef66`. The merge message's "36 hunks" is an immutable
historical error; this note records the correction without amending that message
or repeating the historical merge in a checkout.

**The hazard is a file that does NOT conflict.** `py/accgram/post_stress_meteg.py` auto-merges,
and both sides changed it: the branch's `97a1b46f` added `FIT_TYPE_2_AF`/`FIT_TYPE_2_BF` and the
"next word does not begin with vocal shewa" condition, while `main` renamed
`TYPE_2_FOLLOWING_FILTER_GROUPS` to `TYPE_2_NEXT_WORD_FILTER_GROUPS`, deleted
`_fit_for_mas_intervening_punctuation` and `_FIT_FOR_MAS_NON_PUNCTUATION_MATERIAL`, and added five
qamats-variant functions. A clean textual merge of two semantic changes is to be verified, not
trusted — read that file's merged state before running anything.

`main` also moved `cos` and `itm` into `accgram.almost_errors_html_shared` and deleted
`_ITM_GLOSS`/`_COS_GLOSS`, and reshaped `_TYPE_SOURCES` from 3-tuples to 2-tuples by dropping the
grading element. Both are `main`'s to keep. `main` independently made the same en-dash fix to the
section ranges the branch made, so those hunks agree in substance.

## Steps

1. `git merge --no-edit main` in the worktree.
2. Resolve the four hand-resolved source files plus `CLAUDE.md` by the rule above.
3. Regenerate: `py/main_authored.py gen-site` with `REPOS_ROOT` set, from the worktree root.
4. `git add` the regenerated pages and JSON.
5. Run black on every source file the resolution touched.
6. `py/main_test.py`. **`py/tests/test_post_stress_meteg_plain_word.py` passing is the check that
   the terminology decision survived the merge**; it fails loudly if any "chanted" came through.
7. Verify the figures above by reading them out of the regenerated pages, not from this file.
8. Commit the merge on the branch, with `-F` and a message file under `.novc/`.
9. Integrate, per `~/.claude/CLAUDE.md`'s Git section: `git -C C:/Users/BenDe/GitRepos/MAM-basics
   merge --ff-only post-stress-meteg`, then push `main`. If `--ff-only` refuses, `main` moved
   between steps 1 and 9 — go back to step 1 rather than letting a second merge happen in the
   primary clone.

## Verification scripts already written

Under `.novc/`, written 2026-09-08. **`.novc/` is gitignored, so these exist only on the machine
that wrote them** — re-create any that is absent. Each compares against `HEAD`, so **re-point them
at `a3e3f6eb`** once the merge commit exists:

- `compare_numeric_cells_20260908.py` — every numeric table cell on the nine pages
- `compare_hebrew_forms_20260908.py` — every rendered Hebrew run, plus its mark order
- `check_mark_order_post_stress_meteg_20260908.py` — MAM-normal mark order in the source
- `summarize_html_diff_20260908.py` — the rendered diff with repeated lines collapsed, which is
  what makes a 400-line tooltip change readable
- `dump_page_prose_20260908.py` — each page's prose and distinct tooltips, for a read-through
- `read_key_figures_20260908.py` — the census, type and Fit for MAS rows read out of the
  regenerated main page, which is how step 7 is done

## What the branch contains, for context

Seven commits past `c73a2ad3`: `97a1b46f` (the 2Af/2Bf fit model), `39133db0` (the φ4 page), then
five from 2026-09-08 — the 38-item grammar and spelling pass, the Methods table's structural
subtype, the derived references and four follow-ups, the predictor paragraph closing the Fit for
MAS section, and the plain-"word" lint. Each commit message states its own decisions and evidence.

**Clarification, 2026-09-09 (finding 16 / N8):** The seven non-merge commits from
`c73a2ad3` to `a3e3f6eb` were:

1. `97a1b46f`: type-2 Fit-for-MAS criteria.
2. `39133db0`: next-conjunctive page.
3. `fe4e602f`: grammar and spelling.
4. `c5b170ad`: Methods structural subtype.
5. `d7049855`: derived references and Ben's follow-ups.
6. `0afbae68`: Fit-for-MAS predictor paragraph.
7. `a3e3f6eb`: plain-word lint.

Re-established with `git log --reverse --no-merges --format='%h %s' c73a2ad3..a3e3f6eb`.
The original paragraph remains as the dated branch record.

**The branch's rendered pages at `a3e3f6eb` are the specification for this merge's prose.** The
merge does not need to re-derive those decisions; it needs to keep those nine pages' wording
intact while absorbing `main`'s structure. Diff the merged pages against `a3e3f6eb`'s and account
for every difference.
