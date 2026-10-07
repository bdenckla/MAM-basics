# Remediate the 2026-10-04 review of MAM-basics

State: live; written 2026-10-06 and awaiting Ben's approval; nothing in it has been executed

Written on 2026-10-06, New York time, by a Claude session (Claude Opus 5.5 in the Claude desktop
app) as close-out step 2 of the 2026-10-04 review (`doc/periodic-review.md`, "Close-out: from
findings to dispositions"). The session worked in the full clone `C:/Users/BenDe/GitRepos/MAM-basics`
on clean `main` at `aef25641fa746df27c2fd9765c25e33ab057c782`, equal to `origin/main` after a fetch.
Ben opened it by pasting a prompt that another Claude session wrote the same day, the session that
wrote the entry "Ben's decisions on the open items, 2026-10-06" of
[`review-findings-2026-10-04-update.md`](review-findings-2026-10-04-update.md). That prompt quotes
Ben's instruction to that session, verbatim: "Is this all documentation? Just do what you
recommend. I don't have time for any of this and it feels low stakes. I need this review to end".
The rest of the prompt is that session's reconstruction, and this plan attributes none of it to
Ben.

**What is approved and what is not.** The update file's entry of 2026-10-06 gives each of the
review's open items a disposition. Ben selected 16 of them in dialogs and replaced one selection,
item 8.1's, in his own words; the entry records that those selections "are not considered approvals
of each wording: the remediation plan puts each wording to him again". The other 40 dispositions
are that session's recommendations, adopted under his instruction above without his reading them.
This plan gives the concrete wording and mechanism for the 39 items whose disposition changes a file
or assesses one, and asks Ben to approve all of it in one message ("Ben's part", below). Writing,
committing or pushing this plan implements none of it; execution begins only when Ben explicitly
says to execute.

**How it was prepared.** The root session re-read every passage and the code that each item cites,
on the tree at `aef25641`, and re-ran the measurements that decide a disposition. Six read-only
sub-agents worked in parallel, each writing only under the session's scratch directory outside the
checkout: ps-blocks parsed every `powershell` fence for item 9.22 and drafted each block's
replacement; attrib took the census of English pages that credit Hebrew Wikisource for item 8.4;
pm-code re-measured and drafted items 4.5, 7.11 and 9.39; tool-code re-measured and drafted items
7.2, 7.5, 7.8 and the noticed `_reference_matches` item; break-markers compared the release's break
markers with MAM-parsed's for item 4.6 and the noticed break-marker item; and sim-4-6 simulated item
4.6's correction in memory against every consumer of the release. Each reported
`git status --porcelain` empty at its start and, at its end, empty or showing only this plan's
draft, which the root session was writing meanwhile. The root session re-read the passages that each
adopted proposal rests on and says below where it departs from a sub-agent's draft. Nothing in
MAM-private or hbofonts was read, nor in the private `bdenckla/trope` or `bdenckla/al-hatorah`.

**Citations.** Review items are cited by the review's numbers, 1.3 to 9.39. The review's section
"Noticed outside the diff, not findings" supplies N2 (`_reference_matches`) and N3 (the break
markers at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17); the first update entry's "Noticed
while fixing, not acted on" supplies W1 and W2; finding 3's governing question is G. Line numbers are
those of `aef25641`; a passage's own quoted words, not its number, identify it. This plan names no
path inside a private repository, under Ben's rule of 2026-08-27 in
`in/repo_maintenance_policy.json`'s `repo_visibility` comment.

## Ben's part

One message approves the whole plan:

1. every wording in "1. Reader-facing documents and pages" and "3. Lower-risk changes", including
   item 8.4's narrower scope, which departs from the recorded disposition for the reason R8 gives;
2. the public data changes in "2. Public data", including, under item 4.7's approved-exception
   path, two display corrections of the Phonetic MAM release: the strand of the narrow-sense paseq
   rows of Exodus 20:3 and Deuteronomy 5:7 (item 4.6, D2), and the break forms at Genesis 35:22,
   Exodus 20:13 and Deuteronomy 5:17 (N3, D3);
3. the execution, in the waves below.

A reply such as "approved; execute" does all three. A reply that changes a wording or withholds an
item, such as N3's correction, revises this plan before execution, and the executor applies only
what Ben approved. Nothing else needs Ben during execution unless a stop condition below fires.

## Standalone executor contract

**Checkout.** The development and integration checkout is the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, on `main`. Another verified full clone may serve; its path
then replaces this one throughout. Commit each wave to the local `main` and push `main` only after
the final gate. One agent writes at a time; read-only sub-agents may investigate and check. The
executor owns final integration, pushes `main`, and deploys the user-level configuration.

**Baselines.** Before any edit, require each of these to be an ancestor of `HEAD`, with
`git -C <checkout> merge-base --is-ancestor <commit> HEAD`: `aef25641fa746df27c2fd9765c25e33ab057c782`;
the commit that adds this plan (`git -C <checkout> log --format="%H %s" -- doc/PLAN-remediate-review-findings-2026-10-04.md`);
and the commit that records Ben's approval (wave 0). Record the checkout's path and the exact
`HEAD` at which editing begins in the update entry of wave 7. Then re-measure every passage this plan
cites in a file that changed since `aef25641` (`git -C <checkout> diff --stat aef25641 HEAD`), and
stop on any that no longer reads as quoted here.

**Interpreter.** The full clone's own `./.venv/Scripts/python.exe`, run from the clone's root. In
this plan `py/main_test.py <paths>` means `./.venv/Scripts/python.exe py/main_test.py <paths>`.

**Instructions and skills to load first.**

1. `AGENTS.md` and the user-level instructions.
2. `doc/periodic-review.md`: "Close-out: from findings to dispositions", "Verification cadence
   during remediation", "Separate defects from editorial proposals" and "Present remediation by
   public-facing risk".
3. `iterative-document-editing`: "Executable plans", "Finished receipts and maintained documents"
   and "MAM-basics and MAM-private State conventions".
4. `hebrew-prose`, with `references/core-rules.md`, `terminology.md`, `rendered-prose.md` and
   `mam-basics.md`, before items 1.3, 4.1, 4.6, 8.1, 8.9 and 9.2 and before any docstring or comment
   about accentuation.
5. `mam-wikisource-refresh`, before editing its canonical reference (items 4.4 and 4.7), and
   `mam-repository-topology`, before editing its canonical reference (item 9.22).

Edit only the canonical copies under `dot-claude/` and `dot-Codex/`, never a live deployed copy.

**Before every wave**, verify with separate commands, each naming the checkout with `-C`:
`git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git branch --show-current` and
`git status --porcelain`. Recheck `HEAD` and the task-owned status before staging.

**Stop conditions.** Stop and report, with a standalone continuation prompt, on unexpected `HEAD`
movement, another writer's files, a passage that no longer reads as quoted here, a failing check, an
unexplained generated diff, a refused push, or a fact this plan does not settle. A stop that leaves
work unpushed keeps it in this checkout; the continuation runs here.

**Not authorized:** amending, rebasing, force-pushing, resetting, dropping a stash or discarding
work; any GitHub issue operation; any Wikisource edit or refresh; reading MAM-private or hbofonts
beyond what the suite's and the mega's tracked code read; running `py/main_mam4sef.py` or
`py/main_mam_osis.py` in this checkout (wave 5 runs them only in scratch trees); running
`py/main_hbce_psalms.py compare`; the write form of `--sync-forest`; running
`py/main_repo_maintenance.py`; editing a live deployed instruction or skill except through
`--sync-user-config`; adding an example-based test.

## Decisions this plan follows

1. **The dispositions of 2026-10-06**, in `doc/review-findings-2026-10-04-update.md`, "Ben's
   decisions on the open items, 2026-10-06". Each item below quotes the text that entry records, or
   drafts the text where the entry leaves it to this plan.
2. **Ben's instruction**, quoted at the head of this plan, under which that entry's recommendations
   were adopted.
3. **Ben's decision of 2026-09-30** that a refresh of MAM's text does not oblige rerunning
   `py/main_mam4sef.py` or `py/main_mam_osis.py`, so that MAM-for-Sefaria and MAM-OSIS may lag
   MAM-simple (`AGENTS.md`, "What this repository's products are, and which check a change owes").
   Item 1.3 is not a text refresh, so wave 5 reruns both, in scratch.
4. **The 16 items left as they are and item 8.10's deferral** stand ("Not in this remediation").

## The 39 items, re-measured at `aef25641`

Every item below was re-read on the current tree. None has gone stale or been resolved since the
review's end commit `139e2d63`, though some files changed: Ben's near-Aleppo commits of 2026-10-05
and 2026-10-06 added an entry to the landing page's dataset list (item 8.3 still holds), and the
qere-first documentation of 2026-10-06 rewrote parts of `MAM-simple/README.md` and its guides
(item 1.3's three sentences are unchanged). "Section" names where the item's wording is given.

| Item | Change | Risk class | Section | Wave |
|---|---|---|---|---|
| 1.3 | MAM-simple's narpas label names `lp-paseq`: notice in 70 data files, README, two guides | public data and documents | 1, 2 | 5 |
| 2.1 | `DATA-LICENSES.md`: the printed-Decalogue capture gets its own CC-BY-SA row | document | 1 | 3 |
| 2.2 | `DATA-LICENSES.md` rows 84 and 91 credit each source of the Hebrew | document | 1 | 3 |
| 4.1 | `Phonetic-MAM/README.md` gains departure 9, the inverted nuns | document | 1 | 3 |
| 4.4 | The refresh procedure says what to do when every chapter has left the comparison | instructions | 3 | 1 |
| 4.5 | The exporter's time limit holds whatever the adapter starts | code | 3 | 2 |
| 4.6 | Strand-labelled marker rows; Exodus 20 and Deuteronomy 5 regenerated | public data and pages | 1, 2, 3 | 6 |
| 4.7 | A tracked list of approved display corrections leaves the comparison | code, documents | 1, 3 | 6 |
| 5.2 | D11's final integration runs the suite or records a skip | procedure document | 3 | 1 |
| 5.3 | `AGENTS.md`: a skip note that follows the last commit goes in an empty commit | instructions | 3 | 1 |
| 5.4 | `py/product_scopes.py`'s docstring stops restating the hand-run rule | docstring | 3 | 1 |
| 6.1 | The two procedure documents say that MAM-basics' trial instance ran | procedure documents | 3 | 1 |
| 6.2 | "Records only what pairing adds" gains the D10 and D12 exception | procedure documents | 3 | 1 |
| 6.3 | A brief names the private repositories outside the workspace too | procedure documents | 3 | 1 |
| 6.4 | `doc/periodic-review.md` credits D9 and D11 only with what they say | procedure document | 3 | 1 |
| 6.5 | D9's "public evidence only" follows property 2 | procedure document | 3 | 1 |
| 7.2 | The parser-stage lint's docstring says what it reads | test docstring | 3 | 1 |
| 7.5 | `doc/clone-forests.md` and the module docstring follow the code's skip | document, docstring | 3 | 1 |
| 7.8 | Repository maintenance goes on after step 2 fails | code | 3 | 2 |
| 7.11 | A compute reply that cannot be encoded is rejected | code | 3 | 2 |
| 8.1 | The Job footnote says "orphaned"; the skill's reservation is replaced | page, skill | 1, 3 | 4, 1 |
| 8.3 | The landing page lists Phonetic-MAM among the datasets | page | 1 | 4 |
| 8.4 | The prescribed MAM credit on the nine English pages the disposition names; the census recorded | pages | 1 | 4 |
| 8.5 | MAM's terms for the Hebrew that `examples/display.json` quotes | documents | 1 | 3 |
| 8.6 | `Yeivin-ITM/README.md`'s two sentences in the past tense | document | 1 | 3 |
| 8.7 | `doc/PLAN-mega-speedup.md`'s carried-forward items 1 and 3 | maintained plan | 3 | 1 |
| 8.8 | The common body's Unicode section names stderr's handler | instructions | 3 | 1 |
| 8.9 | `rendered-prose.md` drops its "Cross-repo rule" sentence | skill | 3 | 1 |
| 9.2 | The footnote's heading says "the similar cases" | page | 1 | 4 |
| 9.4 | `DATA-LICENSES.md` rows 52 and 57 cover the two product `LICENSE.md` files | documents | 1 | 3 |
| 9.8 | `README.md`'s "Code: GPL-3.0" item uses dashes | document | 1 | 3 |
| 9.22 | Twelve command blocks made to parse | documents, skill | 1, 3 | 1 |
| 9.39 | `doc/phonetic-mam-compute.md` counts the line terminator | document | 3 | 1 |
| G | The MAM-private entry says which document governs which session | policy comment | 3 | 1 |
| 3.5 | The `repo_visibility` comment records the rule's scope | policy comment | 3 | 1 |
| N2 | `_reference_matches` counts `path:line` citations | code | 3 | 2 |
| N3 | Break markers at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17 assessed and corrected | public data and pages | 2, 3 | 6 |
| W1 | Two stale claims in live update files corrected in place | records | 3 | 1 |
| W2 | The post-stress-meteg step record names `MAM-parsed/plus/` | code comment | 3 | 1 |

## 1. Reader-facing documents and pages (high risk)

Each entry gives the current wording and the proposed wording. Formatting changes are named
separately; rewrapping a paragraph at its existing width is the only one, and it is said where it
happens.

### R1. MAM-simple's narpas label (item 1.3, documents)

The data half is D1. MAM-parsed's notice, README and guide keep `מ:פסק`.

1. `MAM-simple/README.md:44`, the pointer to its cautions:
   - Current: "ketiv/qere pair, and text spacing around narpas (narrow-sense paseq, ׀)."
   - Proposed: "ketiv/qere pair, and text spacing around narpas (narrow-sense paseq, `<lp-paseq>`)."
2. `MAM-simple/doc/reading-mam-simple.md:89`, the bullet in "Consumer notice":
   - Current: "- Narpas (narrow-sense paseq, מ:פסק) forms no compound of any kind; only maqaf joins atoms"
   - Proposed: "- Narpas (narrow-sense paseq, `<lp-paseq>`) forms no compound of any kind; only maqaf joins atoms"
3. `MAM-simple/doc/reading-mam-simple-xml.md:225`, in "Legarmeh and paseq":
   - Current: "group the surrounding text. Narpas (narrow-sense paseq, מ:פסק) forms no compound of any kind;"
   - Proposed: "group the surrounding text. Narpas (narrow-sense paseq, `<lp-paseq>`) forms no compound of any kind;"
   - Formatting: the paragraph, lines 224 to 229, is rewrapped at 100 columns, since the line grows
     past them.

### R2. Licence statements (items 2.1, 2.2, 8.5 and 9.4)

All in `DATA-LICENSES.md` unless named otherwise. A table cell's last sentence keeps the table's
style of no final period, except where the quoted text is inserted mid-cell.

1. **Item 2.1, row 79 and a new row after it.**
   - Current row 79: "| `in/accgram/edition_transcriptions/`, `in/accgram/printed_decalogue_teamim.json` | Ben Denckla's hand transcriptions of the accentuation of printed Decalogue editions, and the table that indexes them | CC0 1.0 — the dedication at the end of this file |"
   - Proposed row 79: "| `in/accgram/edition_transcriptions/` | Ben Denckla's hand transcriptions of the accentuation of printed Decalogue editions | CC0 1.0 — the dedication at the end of this file |"
   - Proposed new row 80: "| `in/accgram/printed_decalogue_teamim.json` | a capture of MAM's eight Decalogue versions from the Hebrew Wikisource page עשרת הדברות בסיס/טעמים, at the revision its `provenance` block records, with a folded form derived from it for the scanners | CC-BY-SA 4.0 — the statement below. It is the same page as one of `in/mam-ws-special/`'s, and what is derived from MAM carries MAM's terms |"
   - Re-measured: the file's `provenance` block names that page, page id 344500 and revision
     3025606, which `in/mam-ws-special/manifest.json` records for the same page; it has 8
     `"book"` versions; its `resolution_notes` call `chanted_verses` "the FOLDED, scanner-ready
     form", derived from `faithful_chanted_verses`.
2. **Item 2.2, rows 84 and 91.**
   - Current end of row 84's terms: "The biblical Hebrew each file quotes comes from the WLC and the UXLC and keeps their terms above"
   - Proposed: "The biblical Hebrew each file quotes keeps the terms of its source above: the WLC's and the UXLC's, or, where a file quotes MAM, as the printed-Decalogue outputs do, MAM's CC-BY-SA 4.0"
   - Current end of row 91's terms: "The biblical Hebrew the pages display comes from the WLC and the UXLC and keeps their terms above"
   - Proposed: "The biblical Hebrew the pages display keeps the terms of its source above: the WLC's and the UXLC's, or, where a page quotes MAM, as the printed-Decalogue pages do, MAM's CC-BY-SA 4.0"
3. **Item 8.5, three places.**
   - `Phonetic-MAM/LICENSE.md:3`. Current: "This statement applies equally to the MAM text and its derivative display in `data/`." Proposed: "This statement applies equally to the MAM text and its derivative display in `data/`, and to the MAM Hebrew that `examples/display.json` quotes."
   - Row 56's terms (`Phonetic-MAM/examples/display.json`), with the sentence inserted after the
     first one. Current: "Ben Denckla's commentary retains its existing terms; Jacobson's quoted material remains its rights holder's. No additional rights over third-party material are granted or implied by the move. The scope is the five previously published pages, without new excerpts". Proposed: "Ben Denckla's commentary retains its existing terms; Jacobson's quoted material remains its rights holder's. The pointed Hebrew forms the tables quote are MAM's text and keep MAM's CC-BY-SA 4.0 terms above. No additional rights over third-party material are granted or implied by the move. The scope is the five previously published pages, without new excerpts"
   - The preface to the MAM statement, lines 154 to 155. Current: "or, for `Phonetic-MAM/`, the MAM text and its derivative display in `Phonetic-MAM/data/`." Proposed: "or, for `Phonetic-MAM/`, the MAM text and its derivative display in `Phonetic-MAM/data/` and the MAM Hebrew that `Phonetic-MAM/examples/display.json` quotes." Formatting: that paragraph is rewrapped.
4. **Item 9.4, rows 52 and 57, and `Yeivin-ITM/LICENSE.md`.**
   - Current row 52: "| `Yeivin-ITM/README.md`, `Yeivin-ITM/schema/` | the product's README, with the adaptation's permission notice and bibliographic scope, and the closed JSON Schema of its claim data | MAM-basics' own work, so GPL-3.0. The adaptation the README describes keeps the terms of the `py/yeivin_itm/content/` row below |"
   - Proposed row 52: "| `Yeivin-ITM/README.md`, `Yeivin-ITM/LICENSE.md`, `Yeivin-ITM/schema/` | the product's README, with the adaptation's permission notice and bibliographic scope, its licence statement, and the closed JSON Schema of its claim data | MAM-basics' own work, so GPL-3.0. The adaptation the README describes keeps the terms of the `py/yeivin_itm/content/` row below |"
   - Current row 57: "| `Phonetic-MAM/README.md`, `Phonetic-MAM/schema/` | the product's README and the closed JSON Schema of its display data | MAM-basics' own work, so GPL-3.0 |"
   - Proposed row 57: "| `Phonetic-MAM/README.md`, `Phonetic-MAM/LICENSE.md`, `Phonetic-MAM/schema/` | the product's README, its licence statement, and the closed JSON Schema of its display data | MAM-basics' own work, so GPL-3.0, apart from the MAM statement that `LICENSE.md` repeats verbatim |"
   - `Yeivin-ITM/LICENSE.md:8`, its restatement of row 52. Current: "- `README.md` and `schema/`: MAM-basics' own work, so GPL-3.0." Proposed: "- `README.md`, `LICENSE.md` and `schema/`: MAM-basics' own work, so GPL-3.0."

### R3. `README.md`'s "Code: GPL-3.0" item (item 9.8, README half)

- Current, lines 116 to 121: "This covers MAM-basics' work in code and prose — everything under `py/`, `.github/` and `doc/` except the adapted excerpts and their remarks under `py/yeivin_itm/content/`, the third-party font under `doc/woff2/`, and the page crops in `doc/*-snips/` and the Hebrew Wikisource Village Pump discussion captured and translated in `doc/wikisource-dagesh-discussion-*`, and the generated indexes and reports under `out/` that carry no corpus text."
- Proposed: "This covers MAM-basics' work in code and prose: everything under `py/`, `.github/` and `doc/` — except the adapted excerpts and their remarks under `py/yeivin_itm/content/`, the third-party font under `doc/woff2/`, and the page crops in `doc/*-snips/` and the Hebrew Wikisource Village Pump discussion captured and translated in `doc/wikisource-dagesh-discussion-*` — and the generated indexes and reports under `out/` that carry no corpus text."
- Its following sentences are unchanged. Formatting: the list item is rewrapped.

### R4. `Phonetic-MAM/README.md` (items 4.1 and 4.7)

1. **Item 4.1's question.** The list under "How the Hebrew differs from MAM's text" gains, after
   item 8: "9. **Inverted nuns.** This release has none of MAM's 9 inverted nuns, `MAM-simple/`'s
   `spi-invnun`, though it keeps MAM's parashah breaks and narrow-sense paseqs as rows of their
   own." Re-measured: 9 `spi-invnun` in `MAM-simple/json-vtrad-mam/`, 2 in `Num.json` and 7 in
   `Ps.json`; no U+05C6 in the 39 book files of `Phonetic-MAM/data/`; and
   `py/phonetic_mam/display_schema.py`'s `LAYOUT_MARKERS` has no inverted-nun marker.
2. **Item 4.7.** After "a change to a chapter's first verse also makes the chapter before it leave,
   and a change to its last verse the chapter after it." the paragraph gains: "A chapter whose
   display has been deliberately corrected leaves the comparison too, and its diff is reviewed
   instead: `in/phonetic_mam_display_corrections.json` lists each such chapter with the approval
   and the reason, and `py/main_phonetic_mam.py check` lists it."

### R5. `Yeivin-ITM/README.md` (item 8.6)

1. Lines 52 to 53. Current: "Its source is pinned to MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`." Proposed: "The migration took its source from MAM-private commit `84c3ddbcfbc338f6a2d261cf01e8400b5027ef75`; no test pins the adaptation to it now."
2. Lines 58 to 59. Current: "All 17 existing filenames, internal links, and anchors are preserved." Proposed: "The migration preserved all 17 existing filenames, internal links, and anchors."

Formatting: the two paragraphs are rewrapped.

### R6. The Book of Job 38:12 footnote (items 8.1 and 9.2)

The page is `gh-pages/book-of-job/jobn-details/3812-YD3F_HJXR.html`, generated from
`py/author_boj_qr/qr_38.py` by `py/main_gen_misc_authored_english_documents.py`, the mega's
`book-of-job-site` step, which also writes the record's strings into
`book-of-job/out/enriched-quirkrecs.json`.

1. Item 8.1, line 78. Current: " In $Ezekiel_42_9, however, the פתח is unattached;" Proposed: " In $Ezekiel_42_9, however, the פתח is orphaned;"
2. Item 8.1, line 104, the Ezekiel caption. Current: "μA, Ezekiel 42:9, page 186r. The unattached פתח is visible between " Proposed: "μA, Ezekiel 42:9, page 186r. The orphaned פתח is visible between "
3. The 2 Samuel sentence at line 131, "It is not orphaned between the two words as it is in
   Ezekiel.", is unchanged.
4. Item 9.2, line 188, the footnote's heading. Current: "φ1 — Attachment of the פתח in the parallel passages" Proposed: "φ1 — Attachment of the פתח in the similar cases"

The skill half of item 8.1 is in section 3.

### R7. The landing page's dataset list (item 8.3)

`py/author_site/site_data.py`, `_DATASETS`, gains after the MAM-OSIS entry and before the
near-Aleppo entry: `_entry("Phonetic-MAM", f"{_REPO_MAIN}/Phonetic-MAM/README.md"),`. The
regenerated `gh-pages/index.html` gains, after the MAM-OSIS item, the line
`<li><a href="https://github.com/bdenckla/MAM-basics/blob/main/Phonetic-MAM/README.md">Phonetic-MAM</a></li>`.
It is generated by the mega's `gen-site` step.

### R8. The prescribed MAM credit on English pages (item 8.4)

**The line.** Each page below keeps its existing credit and link and gains, after that credit, the
sentence "Source attribution: Hebrew Wikisource, under CC-BY-SA 4.0." as this HTML:

```html
Source attribution: <a href="https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning">Hebrew Wikisource</a>, under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC-BY-SA 4.0</a>.
```

This is the MAM statement's prescription (`DATA-LICENSES.md:174–176`: attribution in English "shall
be to "Hebrew Wikisource" ... with a direct link to" that en.wikisource page) and the licence link
of `:170`. `py/mb_misc/mam_attribution.py` holds the attribution URL as `ENGLISH_ATTRIBUTION_URL`
and nothing else; it gains `LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"`, and
each generator below builds the line with its own HTML builder from those two constants. The two
index pages that C15.8 corrected, and the near-Aleppo edition's index since 2026-10-05, say
"License: CC-BY-SA 4.0. Source attribution: Hebrew Wikisource" through
`py/mwd/mwd_write_index_dot_html.py`'s `license_para()`, whose wording is not the disposition's
sentence, so it is not reused. No test pins any attribution text.

**The nine pages,** re-measured by attrib at `aef25641`; all are `lang="en"`.

1. `gh-pages/MAM-with-doc/misc/he_ws_intro_to_mam_gray_maqaf_1.html`,
   `he_ws_intro_to_mam_pasleg.html` and `he_ws_intro_to_mam_gaya_text.html`. Each opens with a
   paragraph such as "The Hebrew text below is from Avi Kadish's introduction to the Miqra al pi
   ha-Masora edition (Chapter 2) on [Hebrew Wikisource, a he.wikisource link]. The English translation
   is original to this project." The line follows that paragraph as a paragraph of its own. Source:
   `_PROVENANCE` and `_CBODY` in `py/author_misc/he_ws_intro_to_mam_gray_maqaf_1.py`,
   `he_ws_intro_to_mam_pasleg.py` and `he_ws_intro_to_mam_gaya_text.py`; regenerated by
   `py/main_authored.py gen-misc`, the mega's `gen-misc` step.
2. `gh-pages/aleppo/missing_sections_torah.html` and `missing_sections_nakh.html`, which no program
   generates. Inside each `<div class="acknowledgement">`, after the `</a>` that closes the
   he.wikisource link, a new line `<br>` followed by the line above, before "The English translation
   was prepared separately.".
3. `gh-pages/wlc/accgram/printed-decalogue.html`: its "Source" section's credit paragraph, "taken
   from the Wikisource base page [he.wikisource link]", is followed by the line as a paragraph of its
   own (`py/accgram/printed_decalogue_page.py`, `_provenance_section`).
4. `gh-pages/wlc/accgram/printed-decalogue-simanim.html` and `printed-decalogue-koren.html`: the
   introduction's paragraph that says "The comparison throughout is against [Hebrew Wikisource's
   p-trad, a he.wikisource link]" is followed by the line as a paragraph of its own
   (`py/accgram/printed_decalogue_simanim_page.py` and `printed_decalogue_koren_page.py`, `_intro`).
5. `gh-pages/wlc/accgram/printed-decalogue-uvinkha.html`, which names Hebrew Wikisource in a table
   row's label with no link: the introduction's paragraph that begins "Hebrew Wikisource has a meteg
   and no accent on ובנך" is followed by the line as a paragraph of its own
   (`py/accgram/printed_decalogue_uvinkha_page.py`, `_intro`).

The four accgram pages are regenerated by `py/main_accgram.py generate-html-<name>`, the mega's
`accgram-generate-html` step.

**The census, and the scope this plan proposes.** The disposition adds "any other English page that
quotes MAM material". attrib read all 1,653 tracked pages under `gh-pages/`, 1,650 of them English,
recording each page's credits and its MAM-text signals and classifying each generated family by what
its generator renders, so the census is complete over the tracked tree; whether a hand-written page
quotes MAM is a judgment for eight `misc` pages. No other page credits Hebrew Wikisource with a
he.wikisource link. But about 1,105 English pages quote MAM material with no credit on the page:
the MAM-with-doc edition's 60 pages, the near-Aleppo edition's 65 and its 8 documentation pages,
the Phonetic MAM release's 929 chapter pages and 4 example pages, and about 40 more in a dozen
families (the 23 FOI pages, 7 change logs, 9 post-stress-meteg pages, mpplus guides, misc pages,
accgram pages that quote MAM forms, an UXLC survey and two Holman pages). Eight more credit MAM's
source in another form: `gh-pages/MAM-OSIS/index.html`, `gh-pages/MAM-for-Sefaria/index.html`,
`gh-pages/MAM-parsed/plus/html/mpplus.html` and `mpplus_kq_special.html` name Wikisource with no
link; `urwotm_2` names it before two screenshots; `maqaf-nonfinal-accents.html` names it only in
hover text; and `telg-doc-notes.html` and `ps17v14-mam-doc-notes.html` credit MAM-with-doc.

Putting the line on all of them is a change of another size from the finding's nine pages: it
touches about a dozen generators and four HTML builders; it moves the pin of the near-Aleppo
check, `near_aleppo/edition.py`'s `PIN`, since that check compares MAM-with-doc's pages; it needs a
place outside `<main>` on every Phonetic MAM chapter page, where `projection_check` admits only
`h2`, `table` and `nav`; and for `gh-pages/MAM-OSIS/index.html` it needs a rerun of the hand-run
`py/main_mam_osis.py`, which would also publish MAM-OSIS's lag behind MAM-simple that Ben accepted
on 2026-09-30. And about 1,066 of the uncredited pages belong to the MAM-with-doc, near-Aleppo
and Phonetic MAM sites, whose index pages already carry the prescribed credit. **This plan
therefore adds the line to the nine pages only, and records the census in the update entry of the
final records step**, so that the rest is a separate decision of Ben's rather than a by-product of
this one. This departs from the disposition's census clause, and
Ben's approval of this plan is what approves the narrower scope; a reply asking for the credit on
every census page instead makes that a separate plan.

### R9. Three command blocks in `MAM-parsed/historical/README.md` (item 9.22, reader-facing part)

This README is inside the distributed `MAM-parsed/` product, so its three blocks are listed here;
the other nine are in section 3. Each placeholder is quoted, as the disposition prescribes for a
placeholder that no one value always fills; every proposed line parses with
`[System.Management.Automation.Language.Parser]::ParseInput` with no error.

1. Line 65. Current: `.venv/Scripts/python.exe py/main_diff.py mpplus --pin <name>` Proposed: `.venv/Scripts/python.exe py/main_diff.py mpplus --pin "<name>"`
2. Line 96. Current: `.venv/Scripts/python.exe py/main_diff.py mpplus --archive <boundary>` Proposed: `.venv/Scripts/python.exe py/main_diff.py mpplus --archive "<boundary>"`
3. Line 102. Current: `git fetch --depth=1 origin <full hash>` Proposed: `git fetch --depth=1 origin "<full hash>"`

### R10. Three Phonetic MAM chapter pages (item 4.6 and N3, pages)

sim-4-6 rendered both chapters in memory through `py/phonetic_mam/renderer.py`, whose unpatched
render reproduces every tracked page of both books byte for byte. The renderer needs no change: it
already renders a labelled cell as a `<span>` whose `title` is the label, as it does each strand's
Hebrew and transcription.

1. **Item 4.6.** Only `gh-pages/phonetic-mam/tnkh/A2-Exodus/20.html` (lines 181 and 205) and
   `A5-Deuter/05.html` (lines 421 and 445) change, each of the four lines from
   `<td><span class="pronunciation-sephardic">מ:פסק</span><span class="pronunciation-ashkenazic">מ:פסק</span></td>`
   to
   `<td><span class="pronunciation-sephardic"><span title="טעם עליון">מ:פסק</span></span><span class="pronunciation-ashkenazic"><span title="טעם עליון">מ:פסק</span></span></td>`.
   The marker keeps its column; a reader learns its strand from the label, as for the strands'
   other cells.
2. **N3.** The marker text of one line on each of three pages:
   `A1-Genesis/35.html:1183`, `פפפ` to `פפ` in both pronunciations' spans; `A2-Exodus/20.html:883`
   and `A5-Deuter/05.html:1241`, `סס` to `ססס`.

All three chapters then differ from their frozen projections; the corrections record takes them out
of the comparison (item 4.7).

## 2. Public data (high risk)

No change touches MAM's text. MAM-parsed's plus files do not change.

### D1. MAM-simple's consumer notice, in all 70 data files (item 1.3)

The notice that `py/mb_cmn/public_data_consumer_notice.py` embeds in each of MAM-simple's 35 JSON
and 35 XML files (24 `mam`, 6 `bhs` and 5 `sef` book groups in each format) shares its narpas rule
with MAM-parsed's notice through `NARPAS_GROUPING_RULE`. The rule becomes product-specific: one text
with the label as its only difference, so that MAM-parsed's 24 plus files are unchanged.

- Current narpas rule in MAM-simple's notice: "Narpas (narrow-sense paseq, מ:פסק) forms no compound of any kind: only maqaf joins atoms into a chanted word. Within the Scripture stream, MAM encodes no whitespace before or after narpas; that absence expresses neither grouping nor a display-spacing preference. An edition chooses whether to display spacing before and/or after narpas, while an analytical consumer need not make a display-spacing decision."
- Proposed: the same, opening "Narpas (narrow-sense paseq, lp-paseq) forms no compound of any kind: only maqaf joins atoms into a chanted word."
- Expected diff: one line in each of the 70 files (`git diff --numstat -- MAM-simple` shows 70 files,
  each 1 and 1), the JSON's rule line and the XML's one-line comment. Nothing else in MAM-simple
  changes.
- MAM-for-Sefaria and MAM-OSIS: wave 5 shows, in scratch, that their generators' output does not
  change (re-measured by the review at `139e2d63`: the Sefaria reader ignores `consumer_notice`, and
  the OSIS reader drops XML comments).

### D2. The release's four marker rows (item 4.6, data)

At Exodus 20:3 and Deuteronomy 5:7, MAM-parsed's dual-cantillation template `מ:כפול` has two
narrow-sense paseqs (`מ:פסק`) in its `ב` parameter, the טעם עליון strand, and none in its `א`
parameter, the טעם תחתון strand (`MAM-parsed/plus/A2-Exodus.json:7988–8002` against `:7987`;
`A5-Deuter.json:2782–2796` against `:2781`); MAM-simple has its two `<lp-paseq />` in `cant-bet`
and none in `cant-alef` (`MAM-simple/xml-vtrad-mam/Exod.xml:912–917`, `Deut.xml:277–282`). The
release has each as an unlabelled marker row, rows 2 and 6 of each verse, which the analysis reader
counts in both strands. break-markers' census found these four the only layout templates in all 34
dual-cantillation templates that one strand has and the other lacks.

- Current, in both pronunciations of each of the four rows:
  `"transcriptions":{"sephardic":[["מ:פסק"],null],"ashkenazic":[["מ:פסק"],null]}`
- Proposed:
  `"transcriptions":{"sephardic":[[{"kind":"reading","label":"טעם עליון","content":["מ:פסק"]}],null],"ashkenazic":[[{"kind":"reading","label":"טעם עליון","content":["מ:פסק"]}],null]}`
- Expected diff, simulated by sim-4-6: exactly these four rows of `Phonetic-MAM/data/A2-Exodus.json`
  and `A5-Deuter.json`, each file one line of canonical JSON that grows by 236 bytes. The JSON Schema
  file accepts the new cells as it stands; the validator does not until section 3's change. Read
  through the patched analysis reader, the two rows belong to `cant-bet`, a `cant-alef` selection
  drops them, and no other marker row of the two books is labelled.
- The release then agrees with MAM here, so `Phonetic-MAM/README.md` needs no note, as the
  disposition says.

### D3. The break markers at Genesis 35:22, Exodus 20:13 and Deuteronomy 5:17 (N3)

**The assessment.** break-markers compared the release's rows with MAM-parsed, MAM-simple, MAM's
mirrored introduction and MAM's mirrored Decalogue special page at `aef25641`; the root session
re-read the definitions, MAM-simple's elements and the release's rows. Each reading below is of
those transcriptions, not of a manuscript.

1. **Genesis 35:22.** The break between the verse's two parts is MAM-parsed's second
   dual-cantillation template, which has `פפ` in all three of its parameters
   (`MAM-parsed/plus/A1-Genesis.json:16009–16031`; its כפול parameter wraps the `פפ` in a note of
   MAM's, which reports a blank line in three manuscripts). MAM-simple has `<spi-pe2 />`
   (`MAM-simple/xml-vtrad-mam/Gen.xml:1551`), and MAM's special page has `{{פפ}}` in both of its
   columns for the verse. The release has `פפפ` (row 13 of the verse).
2. **Exodus 20:13 and Deuteronomy 5:17**, MAM's numbers for the verse of the coveting
   commandment. MAM-parsed's E cell has a mid-verse `ססס` (`A2-Exodus.json:8463–8468`,
   `A5-Deuter.json:3275–3280`), MAM-simple has `<spi-samekh3 />` (`Exod.xml:1010`, `Deut.xml:407`), and
   all eight tables of MAM's special page have `{{ססס}}`. The release has `סס` (row 5 of each verse;
   its row 0 is the `סס` before the verse, from MAM-parsed's C cell, and agrees).
3. **What the forms mean.** MAM's introduction defines `פפ` as the regular open parashah, with a
   blank line, and `פפפ` as an open parashah in special places, without one; `סס` as the regular
   closed parashah at the start of a new line, and `ססס` as a closed parashah in the middle of a line
   (`in/mam-ws-intro/appendices.mediawiki:383–388`).
4. **Not a projection.** No README, schema or public code describes either difference, and every
   other break row of the release agrees with MAM-parsed in name and order (break-markers' census of
   all 23,202 verses), apart from one systematic mapping outside this item: the release has `ססס`
   for each of MAM's 328 song dividers, `מ:ששש`. The three rows came with the legacy display:
   Genesis 35, Exodus 20 and Deuteronomy 5 still match their frozen hashes.

So at each verse the release has the same kind of break as MAM, but not MAM's form of it: it
misrepresents MAM there. Under the disposition, a correction takes item 4.7's path and needs Ben's
approval, which approving this plan gives.

**The correction.** The three rows take MAM-parsed's template: in Genesis 35:22 the verse's only
marker row becomes `פפ`, and in Exodus 20:13 and Deuteronomy 5:17 the verse's second marker row
becomes `ססס`. In the data each row's cell changes in both pronunciations, from `["פפפ"]`
to `["פפ"]` and from `["סס"]` to `["ססס"]`; on the pages, the marker text of those three rows of
`gh-pages/phonetic-mam/tnkh/A1-Genesis/35.html`, `A2-Exodus/20.html` and `A5-Deuter/05.html`
changes. Genesis 35 joins Exodus 20 and Deuteronomy 5 among the corrected chapters. The analyses
that read the release treat `סס` and `ססס` alike as a setumah and `פפ` and `פפפ` alike as a petuḥah
(`py/accgram/post_stress_meteg_model.py:55–57`). The mechanism is the corrections record of items
4.6 and 4.7 (section 3). If Ben withholds this correction, the three rows stay as they are and
nothing else in this plan changes.

### D4. Generated outputs that read the release (items 4.6 and N3)

sim-4-6 ran every consumer of the release in memory, first unpatched, when each reproduced its
tracked file byte for byte, and then with item 4.6's data and code patched:

1. `out/accgram/meteg-before-stress.json` changes on its input hashes alone: the SHA-256 of each
   changed book file and of the manifest, in its `"input"` block. No case, count or selection
   changes, since the survey reads only readings from its `cant-alef` selection. N3's correction
   adds Genesis's hash to the changed lines.
2. `Yeivin-ITM/meteg-claims.json`, a distributed product, changes on one line, its `input.sha256`,
   the hash of the file above. The claim population's hash still equals
   `APPROVED_POPULATION_SHA256`, all 20 fraction pins pass, and no Yeivin page changes, so the
   refresh procedure's stop for new pins does not arise.
3. `out/accgram/post-stress-meteg.json` does not change. In the `cant-alef` scans the two chanted
   words before the paseqs, פֶ֙סֶל֙ and בַּשָּׁמַ֙יִם֙, lose the paseq from their intervening punctuation,
   but neither is a record of the survey, which needs a meteg after the stress, and neither has a
   meteg. N3's forms are read alike, as a setumah or a petuḥah.
4. The final-stress comparison of `py/tests/test_final_stress_vs_phonetic_mam.py`, the
   meteg-before-stress scanner tokens and the Breuer word-length reader are unchanged: they read
   readings only.

So the public data that change are the three release book files, the two Yeivin and
meteg-before-stress files on their hashes, and the three chapter pages; nothing else.

## 3. Lower-risk changes

### Summary by type

1. **Agent instructions and skills:** `AGENTS.md` (5.3); the common body
   `dot-Codex/user-wide-AGENTS.md` (8.8); `hebrew-prose`'s `terminology.md` and `core-rules.md`
   (8.1) and `rendered-prose.md` (8.9); `mam-wikisource-refresh`'s `dependent-refresh.md` (4.4,
   4.7); `mam-repository-topology`'s `repository-maintenance.md` (9.22).
2. **Policy file comments:** two sentences in `in/repo_maintenance_policy.json` (G, 3.5).
3. **Procedure and maintained documents under `doc/`:** `doc/dual-agent-review.md` and
   `doc/periodic-review.md` (5.2, 6.1 to 6.5); `doc/clone-forests.md` (7.5);
   `doc/PLAN-mega-speedup.md` (8.7); `doc/phonetic-mam-compute.md` (9.39); eight command blocks in
   four documents (9.22).
4. **Dated records corrected in place:** one passage in each of two live update files (W1).
5. **Python docstrings and comments:** `py/product_scopes.py` (5.4),
   `py/tests/test_parser_stage_node_keys.py` (7.2), `py/repo_util/forest_sync.py` (7.5),
   `py/main_0_mega.py` (W2), and the docstrings that item 4.6's and 4.7's code changes touch.
6. **Code and tests:** `py/phonetic_mam/exporter.py` (4.5), `py/main_repo_maintenance.py` (7.8),
   `py/phonetic_mam/compute.py` (7.11), `py/repo_util/worktree_retirement_inspection.py` (N2), and the
   display contract, analysis reader, projection check and its test (4.6, 4.7).

### Agent instructions and skills

1. **Item 5.3, `AGENTS.md`**, "What this repository's products are, and which check a change owes".
   After "say what you skipped, and why, in the message of the last commit you push." insert: "If
   that decision follows the last commit, as when a worktree branch is fast-forwarded unchanged,
   push an empty commit (`git commit --allow-empty`) whose message says it, rather than amending."
2. **Item 8.8, `dot-Codex/user-wide-AGENTS.md:406–407`**, "Unicode in source and at runtime".
   Current: "A Windows Python entry point that may emit non-ASCII reconfigures stdout and stderr to
   UTF-8 at the start of `main()`." Proposed: "A Windows Python entry point that may emit non-ASCII
   reconfigures stdout to UTF-8, and stderr to UTF-8 with `errors="backslashreplace"`, at the start of
   `main()`." Deployed after the push, in "Final gate and records".
3. **Item 8.1, the skill half.** `dot-claude/skills/hebrew-prose/references/terminology.md:380`,
   "Strand vocabulary". Current: "- **orphaned** is RESERVED for the ḥiriq of the implicit yod
   in ירושלם-style spellings." Proposed: "- **orphaned** = a point that belongs to no letter: the
   ḥiriq of the implicit yod in ירושלם-style spellings, a qere point that no letter of the ketiv
   carries, or a point left between two written words. Never "unattached", a second name for the same thing. A
   stress-helper written without its fusion partner is unpaired, and an accent or verse number
   displaced by BHS versification is marooned; neither is orphaned." And
   `dot-claude/skills/hebrew-prose/references/core-rules.md:144`, the vocabulary table's row, current
   "| strand; unpaired; marooned; orphaned | thread; stranded |", proposed "| strand; unpaired;
   marooned; orphaned | thread; stranded; unattached |". This defines the word by the sense its Job
   uses share, as Ben asked, and names the cases where it is wrong instead of allowing only one: the
   two neighbouring senses that the same list gives other words. Ben's words of 2026-10-06, in the
   update entry under finding 8: "I don't like using two words for the same thing so I'd rather
   stick with "orphaned"".
4. **Item 8.9, `dot-claude/skills/hebrew-prose/references/rendered-prose.md:23–24`.** Delete
   "Cross-repo rule; cf. MAM-basics `py/versification_and_cantillation/doc.py`." The sentence before
   it, "Verbatim quoted source Hebrew keeps whatever it says.", ends the paragraph.
5. **Item 4.4, `dot-claude/skills/mam-wikisource-refresh/references/dependent-refresh.md`**, item 2,
   "The legacy display projection". After "Never regenerate either file; no source exists for the old
   pages' display of new text." insert: "If every chapter has left the comparison, the suite fails
   with "every chapter left the comparison": stop, and ask Ben whether to retire the legacy
   projection comparison." Wave 6 then adds item 4.7's sentence after it: "A chapter whose display
   Ben approved correcting is listed, with his approval, in
   `in/phonetic_mam_display_corrections.json`; it has left the comparison too, and `check` lists it
   apart from the chapters whose input changed. Add a chapter there only with Ben's approval of that
   correction."
6. **Item 9.22, `dot-claude/skills/mam-repository-topology/references/repository-maintenance.md:18`.**
   Current: `./.venv/Scripts/python.exe py/main_repo_util.py --run-black --workspace-file all-repos.code-workspace --repos <repo>`
   Proposed: `./.venv/Scripts/python.exe py/main_repo_util.py --run-black --workspace-file all-repos.code-workspace --repos "<repo>"`

### Policy file comments (G and 3.5)

Both in `in/repo_maintenance_policy.json`. Each records its source in the update file rather than
calling the disposition a decision of Ben's, since it is a recommendation adopted under his
instruction.

1. **G.** The `MAM-private` entry's `comment` gains, at its end: " That statement governs a session
   that may read MAM-private. A public-only session, such as a review of the public series, cannot
   read it, and judges what may cross by the 2026-08-27 rule in repo_visibility's comment above
   (doc/review-findings-2026-10-04-update.md, finding 3, 2026-10-06)."
2. **3.5.** The `repo_visibility` `comment` gains, after "...and findings about them.": " Existing
   text was left as written on 2026-10-06 rather than swept, and the rule does not reach agent
   routing in skills and instructions, code comments and docstrings, dated records, or the policy and
   manifest files under in/, this one included, which name private paths for sessions that can read
   them or record what happened (doc/review-findings-2026-10-04-update.md, finding 3, 2026-10-06)."

### Procedure and maintained documents

1. **Item 5.2, `doc/dual-agent-review.md`**, D11's final integration. Before "Then fetch in the
   designated full integration clone" insert: "Run the suite there too, or record a judged skip, as
   `AGENTS.md`'s rule for a push of `main` asks."
2. **Items 6.1 and 6.2, `doc/periodic-review.md`'s opening paragraph, lines 11 to 17.** Current:
   "Read this before starting a periodic review. Read `doc/dual-agent-review.md` as well only when the
   window is to be reviewed by two agents. Its **Next review: independent reviews and one disposition
   list** section records Ben's 2026-10-02 choice for the next review in each of MAM-basics and
   MAM-private and takes precedence over D9's alternating procedure for that trial." Proposed: "Read
   this before starting a periodic review. Read `doc/dual-agent-review.md` as well only when the
   window is to be reviewed by two agents, apart from two rules there that every review follows: D10's
   filename and State rules, in "Review filenames and State lines", and D12's rule for correcting a
   finished dated document. Its **Next review: independent reviews and one disposition list** section
   records Ben's 2026-10-02 choice for the next review in each of MAM-basics and MAM-private and takes
   precedence over D9's alternating procedure for that trial. MAM-basics' instance ran on 2026-10-02;
   the procedure for a later two-agent window of MAM-basics is Ben's choice when he starts one." The
   paragraph's last two sentences are unchanged.
3. **Item 6.2, `doc/periodic-review.md:22–23`.** Current: "`doc/dual-agent-review.md` records only
   what pairing adds." Proposed: "`doc/dual-agent-review.md` records only what pairing adds, apart
   from two rules that every review follows and that other instructions cite there: D10's filename
   and State rules and D12's rule for correcting a finished dated document."
4. **Item 6.2, `doc/dual-agent-review.md:26–27`.** Current: "A rule about how one reviewer finds,
   checks or records findings goes there too, even when a dual-agent round taught it." Proposed: "A
   rule about how one reviewer finds, checks or records findings goes there too, even when a
   dual-agent round taught it, apart from D10's filename and State rules and D12's rule for correcting
   a finished dated document, which every review follows and which other instructions cite here."
5. **Item 6.1, `doc/dual-agent-review.md`'s opening, lines 9 to 10.** Current: "**For the next review,
   Ben selected the simplified independent-review trial below on 2026-10-02.**" Proposed: the same
   sentence followed by "Its MAM-basics instance ran on 2026-10-02; the procedure for a later
   two-agent window of MAM-basics is Ben's choice when he starts one."
6. **Item 6.1, `doc/dual-agent-review.md:31`**, the section "Next review: independent reviews and
   one disposition list". After "**Use this simplified process for the next review in each of
   MAM-basics and MAM-private.**" insert: "MAM-basics' instance ran on 2026-10-02, as "The MAM-basics
   trial review, kicked off 2026-10-02" below records; for a later two-agent window of MAM-basics, the
   procedure is Ben's choice when he starts one." What both documents say of MAM-private's instance
   is unchanged.
7. **Item 6.3, both documents.** `doc/dual-agent-review.md:86–87`, current: "and the private
   repositories it must not read, as `in/repo_maintenance_policy.json`'s `repo_visibility` lists
   them." Proposed: "and the private repositories it must not read: those that
   `in/repo_maintenance_policy.json`'s `repo_visibility` lists, and the private repositories outside
   the workspace that the tree cites, today `bdenckla/trope` and `bdenckla/al-hatorah`."
   `doc/periodic-review.md:198–200`, current: "nor any other repository that
   `in/repo_maintenance_policy.json`'s `repo_visibility` declares private." Proposed: "nor any other
   repository that `in/repo_maintenance_policy.json`'s `repo_visibility` declares private, nor a
   private repository outside the workspace that the tree cites, today `bdenckla/trope` and
   `bdenckla/al-hatorah`." The brief rule that follows, "Every brief the reviewer gives a sub-agent
   names those repositories", and item 1 of "What a reviewer reads, runs and records", which cites
   "the private repositories of property 2", then cover both.
8. **Item 6.4, `doc/periodic-review.md:260–262`.** Current: "and a claim that only a transcript can
   check goes to Ben in chat rather than into the file, as D9 and D11 of `doc/dual-agent-review.md`
   require of a turn." Proposed: "and a claim that only a transcript can check goes to Ben in chat
   rather than into the file; D9 and D11 of `doc/dual-agent-review.md` likewise keep such a claim out
   of a tracked turn."
9. **Item 6.5, `doc/dual-agent-review.md:293–295`.** Current: ""Public evidence only" means that the
   turn reads nothing in MAM-private: the series' public-only property, as `doc/periodic-review.md`,
   "Two standing properties of the series", states it." Proposed: ""Public evidence only" means that
   the turn reads no repository that the series' public-only property, property 2 of
   `doc/periodic-review.md`, "Two standing properties of the series", names as private."
10. **Item 7.5, second half, `doc/clone-forests.md:49–50`.** Current: "One occupied clone is skipped
    rather than refused: the clone that only the calling Claude session occupies." Proposed: "One
    occupied clone is skipped rather than refused, even when it is dirty, off `main`, mid-operation
    or locked: the clone that only the calling Claude session occupies." The page's sentence at
    `:40–41`, "A clone that is dirty, off `main`, mid-operation, locked or occupied is refused before
    any fetch.", then reads with that exception. Re-measured by tool-code at `aef25641`:
    `py/repo_util/forest_sync.py`'s skip, at `:288–294`, returns before the dirty, off-`main`,
    mid-operation and lock reasons collected at `:277–283` are consulted at `:295–301`; with Git and
    the session records stubbed in memory, a caller-only clone on another branch with a change,
    `MERGE_HEAD` and `index.lock` was skipped unfetched, and the same clone with a second session was
    refused with every reason listed. The four states are named because the sentence at `:40–41`
    and the module docstring list exactly those; the disposition's "whatever its state" means the
    same.
11. **Item 8.7, `doc/PLAN-mega-speedup.md`**, the list of five things Phase 2 carries forward.
    Item 1, current: "the one step a cloud run skips, `accgram-survey-post-stress-meteg`, is the
    mega's most expensive on Ben's machine at 40.9 s, or 16.5% of a comparable run there." Proposed:
    "the one step a cloud run skipped in these runs, `accgram-survey-post-stress-meteg`, was the
    mega's most expensive on Ben's machine at 40.9 s, or 16.5% of a comparable run there. Since
    `9a67d51b` (2026-10-01) a cloud run runs that survey, which reads the public Phonetic MAM release,
    and skips only `phonetic-mam-export`." Item 3, current: "for every step but the one it skips."
    Proposed: "for every step but the one it skips, now `phonetic-mam-export`." The executed Phase 2
    steps stay as written.
12. **Item 9.39, `doc/phonetic-mam-compute.md:19–20`.** Current: "A request line is limited to 16
    Mi characters; an oversized request terminates the stream." Proposed: "A request line, including
    its line terminator, is limited to 16 Mi characters; an oversized request terminates the
    stream." Re-measured by pm-code by subprocess: with `MAX_REQUEST_CHARS` = 16,777,216
    (`py/phonetic_mam/compute.py:24`), a line of that many characters is answered when unterminated
    and ends the stream with no reply when an LF ends it, and a line one character shorter ends the
    stream when CR and LF end it, since `serve` reads `readline(MAX_REQUEST_CHARS + 1)` and standard
    input keeps the CR (`py/main_phonetic_mam.py:73`). The sentences after it stay true.
13. **Item 9.22, the other eight blocks.** Each parses afterwards with no error.
    1. `doc/user-wide-instruction-conversion-reconciliation.md:103`. The placeholder `<clone>` has
       one value that always works, the primary forest's clone, so it takes that value, as C15.24
       did, and the instructions above it change to match. Current command:
       `(git -c safe.directory=<clone> -C <clone> show 71f96ca3801863f6fa64c1fd0e75ccfde773439b:dot-claude/user-wide-CLAUDE.md).Where({ $_ -match '^#{2,3} ' })`
       Proposed: `(git -c safe.directory=$HOME/GitRepos/MAM-basics -C $HOME/GitRepos/MAM-basics show 71f96ca3801863f6fa64c1fd0e75ccfde773439b:dot-claude/user-wide-CLAUDE.md).Where({ $_ -match '^#{2,3} ' })`
       Lines 98 to 100, current: "Run this read-only command from any PowerShell 7 working
       directory, with `<clone>` replaced by the absolute path, in forward slashes, of any full
       MAM-basics clone. It reads only that repository at the pinned commit; it does not require the
       obsolete full live Claude body." Proposed: "Run this read-only command from any PowerShell 7
       working directory. It names the primary forest's clone, `$HOME/GitRepos/MAM-basics`, which
       every machine has; the absolute path, in forward slashes, of any other full MAM-basics clone
       may replace it. It reads only that repository at the pinned commit; it does not require the
       obsolete full live Claude body." ps-blocks ran the proposed command with
       `GIT_TEST_ASSUME_DIFFERENT_OWNER=1`: Git accepted PowerShell's expansion of the
       `safe.directory` value and printed 36 headings, matching the document's "35 level-2 headings
       and one level-3 heading".
    2. `doc/PLAN-repo-maintenance-across-GitRepos.md:427` and `:431`: `--report-txt <file>` becomes
       `--report-txt "<file>"` in both.
    3. `doc/PLAN-repo-maintenance-across-GitRepos.md:770`, the unlabelled block after "Re-establish
       with:". Insert `$(` before `foreach` and `)` after the loop's closing brace, before
       ` | Format-Table -AutoSize`, so that the middle reads
       `…; $(foreach ($f in $ws.folders) { … ClaudeBr=$cb} }) | Format-Table -AutoSize`. The block
       stays unlabelled and chained, since the disposition asks only that it parse; `continue` still
       skips inside the loop (shown by ps-blocks on synthetic data).
    4. `doc/PLAN-silluq-before-gaya-template.md:266`: `git -C <home-clone> rev-parse HEAD` becomes
       `git -C "<home-clone>" rev-parse HEAD`. The home clone may be in any forest, so no one value
       fills it.
    5. `doc/PLAN-silluq-before-gaya-template.md:485`:
       `<home-clone>/.venv/Scripts/python.exe -m black <changed-python-files>` becomes
       `& "<home-clone>/.venv/Scripts/python.exe" -m black "<changed-python-files>"`, the call
       operator standing where the placeholder is a command's path.
    6. `doc/edition-transcription-workflow.md:244`, inside a list item, keeping its two-space indent:
       `zoom-line <export.json> 12` becomes `zoom-line "<export.json>" 12`.
    7. `doc/edition-transcription-workflow.md:279`:
       `build <stem> --export <path>... --corrections <path>` becomes
       `build "<stem>" --export "<path>..." --corrections "<path>"`.

### Dated records corrected in place (W1)

As items 9.28 and 9.33 were corrected in place elsewhere:

1. `doc/review-findings-2026-10-02-update.md:530–531`, "Remediation implemented; final gates
   pending, 2026-10-03". Current: "Wave 0's `cbd405b11ef990040031ccf19699db54a69a489d` is the archive
   commit, the last whose tree holds every file that the relay's removal deleted, and" Proposed:
   "Wave 0's `cbd405b11ef990040031ccf19699db54a69a489d` is the archive commit, the removal commit's
   parent, whose tree holds every file that the relay's removal deleted, and". Re-measured:
   `4573b007`'s parent is `cbd405b1`, and `d168e22e`, whose parent is `074af13a`, also holds the ten
   files, so "the last" was false. `4573b007`'s commit message stays as written.
2. `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md:241`, "Remediation execution by Codex,
   2026-10-01". Current: "Public verification evidence is retained under this worktree's ignored
   `.novc/`:" Proposed: "Public verification evidence was retained under this worktree's ignored
   `.novc/`, until the worktree and its `.novc/` were removed on 2026-10-04:". The same file's "The
   relay's end on BENS-HP-MINI, 2026-10-04" records that removal.

### Python docstrings and comments

1. **Item 5.4, `py/product_scopes.py:48–52`.** Delete the two sentences from "A change to a hand-run
   generator, or to any input it reads," through "their products may lag it, as their READMEs say.",
   so that the docstring's "this docstring does not restate it" is true. The paragraph then ends
   "...and reading the first as the second is the mistake this paragraph exists to stop."
2. **Item 7.2, `py/tests/test_parser_stage_node_keys.py:1–8`.** Lines 1 to 7 stay; before the
   closing `"""` the docstring gains this paragraph:
   ```
   The lint reads only the tests of ``node_type_and_subtype``'s top-level ``if`` statements
   and the string constants in the ``return`` of ``dic_is_template`` and of ``is_abtag``, so a
   node admitted through an ``elif``, an ``else``, another kind of statement or a change to
   ``is_template``, whose body it does not read, passes it.  Nor does the lint read the body of
   ``_validate_no_parser_stage_encoding``: it pins only the key set, so a refusal that tests
   fewer keys passes it too.
   ```
   No injection test is added, as the approved plan of 2026-10-02 decided. Re-measured by
   tool-code against mutated copies in scratch: an `is_template` that admits a further shape beside
   `dic_is_template`'s, an `elif`, an `else` holding an `if`, a `match` statement and the refusal
   reverted to `assert "stmpl" not in node` all pass the lint; a third top-level `if`, a fourth key
   in `dic_is_template`'s return and a widened first test fail it.
3. **Item 7.5's module docstring, `py/repo_util/forest_sync.py:9–11`.** Current: "A clone that only
   the calling Claude session occupies is not refused: a write skips it unfetched and does not count
   it as a failure, since that session updates its own checkout." Proposed: "A clone that only the
   calling Claude session occupies is not refused, even when it is dirty, off main, mid-operation or
   locked: a write skips it unfetched and does not count it as a failure, since that session updates
   its own checkout." Lines 9 to 12 are rewrapped.
4. **W2, `py/main_0_mega.py`**, the `accgram-survey-post-stress-meteg` step record and the comment
   above it. The record's description, current "reads public Phonetic-MAM and MAM-simple's
   json-vtrad-mam, and writes the tracked out/accgram/post-stress-meteg.json; runs in a cloud
   session; must come before gen-site", becomes "reads public Phonetic-MAM, MAM-simple's
   json-vtrad-mam and MAM-parsed's plus/ tree, and writes the tracked
   out/accgram/post-stress-meteg.json; runs in a cloud session; must come before gen-site". The
   comment's sentence ending "whose json-vtrad-mam it reads (paths.mam_simple_vtrad_mam_dir)." is
   followed by: "It also reads MAM-parsed's plus/ tree, which parse-ws writes far earlier
   (py/accgram/post_stress_meteg_sources.py, through read_books_from_mam_parsed_plus)." Re-measured:
   `_written_stress_helpers` calls `read_books_from_mam_parsed_plus.read_parsed_plus_bk39s`.

### Code and tests

Each code change is demonstrated in memory or by subprocess, with nothing reaching MAM-private, and
the demonstration is recorded in its commit message, as the 2026-10-05 fixes were. No example-based
test is added.

1. **Item 4.5, `py/phonetic_mam/exporter.py`.** Re-measured by pm-code at `aef25641`, with
   `exporter._adapter_command` replaced in memory by a fake adapter whose child inherits its
   pipes and sleeps 20 seconds, and the limit patched to 5 seconds: both `iter_source_books` and
   `source_test_pages` raise their limit errors only after 20.15 to 20.19 seconds, whether the child
   holds stderr, stdout or both. Thread dumps show the two waits the review names: the main thread
   reading stdout, then `Popen.__exit__` closing stderr under the drain thread's pending read, for
   the books; and the post-kill `communicate()` that `subprocess.run` repeats on Windows only, for
   the test pages. The change, which pm-code tried on a patched copy:
   - a constant `_PIPE_GRACE_SECONDS = 5`, the wait that `_StderrTail.join` already uses, with a
     comment saying that once the adapter has ended or the limit has passed its pipes are waited for
     at most this long and then left to the threads reading them;
   - `_Watchdog` gains a `deadline`, the start plus the limit plus the grace, and an `ended()` that
     cancels the timer and brings the deadline to the grace after the adapter is seen to end;
   - every blocking read of the adapter's stdout is made on a daemon thread and waited for only until
     the deadline (a small `_PipeReads` class), and `_StderrTail` joins until the deadline and holds
     the stream as the `Popen` gives it, reading through its binary buffer, so that a stream left to
     its thread is not finalized under the pending read;
   - a shared `_stop()` kills and reaps the adapter, joins stderr until the deadline, and sets a pipe
     still being read to `None` on the `Popen`, so that `Popen.__exit__` does not wait to close it;
   - `source_test_pages` uses the same `Popen`, readers and watchdog instead of `subprocess.run`,
     whose Windows post-kill `communicate()` cannot be bounded from outside;
   - the error messages and `_tail_text` stay as they are.

   On the patched copy the same fake adapters end at 10.01 to 10.03 seconds, the limit plus the
   grace, or at 5.13 to 5.19 seconds when the adapter exits at once and its child holds stderr; a
   normal run gives the same results in the same time, with no thread, handle or `ResourceWarning`
   left over; the messages are byte-identical, except that a test-page adapter that exits 1 at once
   now reports "failed (exit status 1)" where the old code, blocked past the 5-second test limit,
   reported the limit. The executor reruns that matrix of fake adapters on the committed code and
   records its times in the commit message. A POSIX run was not made.
2. **Item 7.8, `py/main_repo_maintenance.py`.** Re-measured: `main()` runs step 1 inside
   `try: clean_novc() except OSError` (`:219–224`) but step 2 as a bare
   `ok = clean_worktrees() and ok` (`:226–227`), and `git_worktree_cleanup.clean_worktrees` raises
   `RetirementError` outside its per-worktree catch when `git worktree list` fails, when no default
   branch is available, or when a branch ref cannot be read (`py/repo_util/git_worktree_cleanup.py:38–83`).
   tool-code stubbed every step and Git in memory: at `aef25641` a missing default branch ends the
   run with a traceback after step 1, and steps 3 to 7 never run. The change:
   - import `RetirementError` from `repo_util.worktree_retirement`, beside the module's other
     imports;
   - replace `:226–227` with
     ```python
         if not args.skip_worktrees:
             try:
                 ok = clean_worktrees() and ok
             except (RetirementError, OSError) as exc:
                 print(f"worktrees: FAILED ({exc})")
                 ok = False
     ```
   - in the docstring's step 2, after "All owners use the same safety and .novc policy.", add "A
     refused audit sets the overall exit status but does not block later steps.", as steps 3 to 5
     say of theirs.

   The catch includes `OSError`, beyond the disposition's `RetirementError`, because a Git that
   cannot be launched is the audit's other failure and `py/main_repo_util.py:519` catches the same
   pair for the same inspection; without it "Seven independent steps" would still be false. On a
   patched copy the same faults print `worktrees: FAILED (no default branch is available for the
   integration check)` and the run goes on through step 7 and exits 1, as for step 1's failure; the
   executor's demonstration adds a `FileNotFoundError` from a Git that cannot be launched.
   Other exceptions that can still end a run, such as a non-UTF-8 reflog read in step 2 or a
   non-UTF-8 Git child in step 3, are left as they are: the finding names step 2's
   `RetirementError`.
3. **Item 7.11, `py/phonetic_mam/compute.py`, `serve`.** Re-measured by pm-code by subprocess, with
   `PYTHONUTF8=0` and no `PYTHONIOENCODING`: a `phrase` request whose untangler key is the
   JSON-escaped lone surrogate `"\ud800"`, followed by a good line, gets no reply at all, and the
   process exits 1 with `UnicodeEncodeError`, since the reply is encoded at `:312` but written to the
   strict UTF-8 standard output at `:323`, outside the `try`. pm-code found a second echo route the
   review did not name: an `accents` request whose value ends in the same escape. The change: inside
   the `try`, after `encoded = json.dumps(response, ensure_ascii=False, allow_nan=False)`, add
   ```python
               # Standard output is strict UTF-8. A result that echoes a lone
               # surrogate, which a request's JSON can escape, is rejected here,
               # whichever operation echoes it, rather than ending the stream.
               encoded.encode("utf-8")
   ```
   and end the docstring's paragraph with "A result that cannot be encoded as UTF-8 gets a
   ``UnicodeEncodeError`` reply." A lone surrogate is the only code point that UTF-8 cannot encode,
   so the one line covers every echo route. In a patched stream of 14 lines, each test request
   followed by a good line, every line got one reply, both echo routes got the ordinary error reply
   with the message "computation rejected", and the process exited 0. The corpus-wide check in
   `py/tests/test_phonetic_untangler_preparation.py:59–60`, commented "Each reply must encode as
   compute.serve encodes it.", gains `.encode("utf-8")` on its `json.dumps(...)`, so that its comment
   stays true.
4. **N2, `py/repo_util/worktree_retirement_inspection.py`, `_reference_matches` (`:264–295`).**
   Re-measured by tool-code in memory at `aef25641`: the bare path is accepted in backticks, at a
   line's end and before `.` or `:`, but `path:3`, `path:3:`, `path:3-5`, `path:3–5` and `path#L3`
   are rejected, since the tail after the path must begin with a delimiter or punctuation that a
   delimiter follows. Tracked files spell a line range with an en dash on 1,058 lines and with a
   hyphen on 25; the one `.novc` citation with a locator is the review's example,
   `doc/dual-agent-review-comparison-2026-10-01.md:488–489`. The change:
   - `import re` among the module's imports;
   - before the function:
     ```python
     # A file citation may end in a line locator: path:3, path:3-5 (hyphen or en dash) or
     # path#L3.  The colon that ends path:3: is trailing punctuation, which the boundary
     # test below already admits.  normcase lowercases the line on Windows, so the L of
     # path#L3 may arrive as l.
     _LINE_LOCATOR = re.compile(r":[0-9]+(?:[-\N{EN DASH}][0-9]+)?|#[Ll][0-9]+")
     ```
   - inside the loop, after the directory-slash adjustment and before the punctuation count:
     ```python
             if not directory and (locator := _LINE_LOCATOR.match(tail)):
                 tail = tail[locator.end() :]
     ```

   On a patched copy, all four forms and the en dash range are accepted after every spelling of a
   reference, and every near miss stays rejected: `path:3:7`, `path.mdx`, `path.md.bak`, `path:3x`,
   `path:3-`, `path#L`, `path#section` and `::3`, among others; a directory reference followed by
   `:3` stays rejected. Lines 488 and 489 of the comparison now match their `.novc` file. The
   simulation test's citation oracle, `py/repo_util/worktree_retirement_simulation_test.py`, writes
   no locator, so its expectations are unchanged; it is outside the default suite and is not run
   here.
5. **Items 4.6 and 4.7, with N3's correction.** All public; the private adapter and its input
   format are unchanged, and the strand of a marker comes from public MAM-parsed, where MAM records
   it.
   1. **The display contract, `py/phonetic_mam/display_schema.py`.** A new tuple
      `CANTILLATION_LABELS = ("טעם פשוטה", "טעם מדרשית", "טעם תחתון", "טעם עליון")`, the labels in
      `READING_LABELS` that name a strand alone. In `validate_book`'s marker-row check, each
      pronunciation's first cell may be either `[marker]`, as now, or
      `[{"kind": "reading", "label": L, "content": [marker]}]`, with `marker` in `LAYOUT_MARKERS`
      and `L` in `CANTILLATION_LABELS`; the other cells stay `None`, and the two pronunciations'
      first cells must still be equal. The module docstring gains: "A layout marker that one strand
      of a dual-cantillation template has alone carries that strand's label." The JSON Schema file
      already admits such a cell, since its `transcriptionCell` allows a `transcriptionReading`, so
      the file and the schema id `phonetic-mam-public-v1` are unchanged.
   2. **Which strand has a marker: a new module, `py/phonetic_mam/strand_layouts.py`,** reading
      public MAM-parsed plus. For each verse whose E cell has `מ:כפול` templates among its top-level
      elements, it returns the layout templates of those templates' `א` parameters and of their `ב`
      parameters, each list in order. Dispatch is closed. Each top-level template of an E cell passes
      `template_names.validate_current_plus_template`, and only `מ:כפול` is read. Inside a strand, a
      string contributes nothing; a list, its items in order; a template named in
      `display_schema.LAYOUT_MARKERS`, its name, a `פסקא באמצע פסוק` parameter being ignored; the
      legarmeh template `מ:לגרמיה-2`, nothing, since the release keeps a legarmeh inside the
      chanted word's Hebrew; the note template `נוסח`, its parameter 1 only; the qamats
      template `מ:קמץ`, its `ד` and `ס` parameters, which must give the same list; and any other
      template raises. The module also raises unless every `מ:כפול` that a
      walk of the whole file finds is one that it read at the top level of an E cell.
      break-markers' census at `aef25641`: 34 `מ:כפול` templates in 18 verses, every one at the top
      level of an E cell, with only נוסח, מ:פסק, מ:לגרמיה-2, סס, פפ and מ:קמץ inside their parameters.
   3. **The projection, `py/phonetic_mam/display_projection.py`.** `project_book` takes the book's
      entries from that reader. In `_verse`, when a verse's two lists differ, its layout elements
      are labelled only if one list is empty and the verse's layout labels, in order, equal the
      other; each then gets that strand's label, `טעם` and the name from `_CANT_NAMES`. Any other
      difference raises `PublicReleaseError("unsupported strand-specific layout")`, and equal lists
      label nothing. At `aef25641` this labels exactly the two marker rows of Exodus 20:3 and the two
      of Deuteronomy 5:7, each `טעם עליון`. The module docstring's "Only generic display Hebrew and
      the existing transcriptions enter this module." becomes "Only generic display Hebrew, the
      existing transcriptions and, from public MAM-parsed, the strand of a layout marker that one
      strand of a dual-cantillation template has alone enter this module."
   4. **The record of approved corrections, a new tracked file
      `in/phonetic_mam_display_corrections.json`** (item 4.7, with N3's correction):
      ```json
      {
        "schema": "phonetic-mam-display-corrections-v1",
        "chapters": {
          "tnkh/A1-Genesis/35.html": "<approval>",
          "tnkh/A2-Exodus/20.html": "<approval>",
          "tnkh/A5-Deuter/05.html": "<approval>"
        },
        "marker_labels": [
          {"book": "Genesis", "chapter": 35, "verse": 22, "marker": 0, "from": "פפפ", "to": "פפ"},
          {"book": "Exodus", "chapter": 20, "verse": 13, "marker": 1, "from": "סס", "to": "ססס"},
          {"book": "Deuter", "chapter": 5, "verse": 17, "marker": 1, "from": "סס", "to": "ססס"}
        ]
      }
      ```
      Each `<approval>` names the chapter's corrections and Ben's approval, for example "Exodus
      20:3's two narrow-sense paseq marker rows take the טעם עליון strand (item 4.6), and 20:13's
      second marker row becomes ססס (N3), as doc/review-findings-2026-10-04.md and its update
      record; approved by Ben on <date> with doc/PLAN-remediate-review-findings-2026-10-04.md".
      `marker` counts a verse's layout elements from 0. `chapters` lists every chapter whose display
      a correction changed while its input did not, item 4.6's two included, though their strand
      labels are derived rather than listed. Every `marker_labels` entry names a listed chapter. No
      code writes this record.
   5. **Applying N3's corrections, in `py/phonetic_mam/exporter.py` and `display_projection.py`.**
      The exporter reads the record and passes each book's `marker_labels` entries to
      `project_book`, which, before projecting the verse, requires the named layout element to have
      the `from` label and gives it the `to` label. An entry that matches no such element, or that no
      verse uses, raises. If Ben withholds N3's correction, `marker_labels` is an empty list and
      Genesis 35 is not listed.
   6. **The analysis reader, `py/phonetic_mam/analysis_reader.py`.** `Row` gains
      `marker_cantillation: str | None = None`; `_row` reads a marker row's cell through `_cell`,
      requires its qamats part to be `None`, and keeps its strand; and `Verse.select(...,
      cantillation=c)` keeps a marker whose strand is `None` or `c` and drops any other, keeping
      every marker when `c` is `None`.
   7. **The comparison, `py/phonetic_mam/projection_check.py`.** A new `corrected_chapters(record,
      inputs)` validates the record (its fields and schema, chapter paths among the 929 recorded
      ones, nonempty approvals, and well-formed `marker_labels` that name listed chapters) and
      returns the listed chapters. `verify_site` takes the record and skips the listed chapters as it
      skips the chapters a refresh changed, and its "every chapter left the comparison" check counts
      both. `report_chapters_left`, which `check` runs, prints the corrected chapters after the
      refreshed ones, saying that they left by an approved correction. The module docstring gains
      that sentence, and its "No code writes either record." becomes "No code writes any of the
      three records." `py/tests/test_phonetic_display_release.py`'s
      `test_complete_release_and_unified_projection` reads the record and passes it.
   8. **Documents:** R4's README sentence and the `dependent-refresh.md` sentence above.
      `py/main_phonetic_mam.py`'s `check` help already says that it lists the chapters that have
      left the comparison, and stays.

   No test is added: the frozen comparison still covers the other 926 chapters, and the three
   corrected chapters' data and page diffs are read against D2, D3 and R10 instead, as item 4.7
   prescribes.

## Execution waves

Each wave begins with the checks of "Before every wave". Every commit gets `git diff --check` and,
for its changed Python files, Black at defaults and `ruff check`; its message names the items it
carries and the measurement re-run for each, and ends with the attribution line. Commit to the
local `main`; push nothing before the final gate. A generated diff that this plan does not predict
stops the wave.

**Wave 0: Ben's approval.** Append to `doc/review-findings-2026-10-04-update.md` an entry "Ben's
approval of the remediation plan, <date>" that quotes his message verbatim and says what it
approves. Set this plan's State to "live; approved by Ben on <date>; executing". If his message
changes a wording or withholds an item, revise this plan to match in the same commit. Commit:
"Record Ben's approval of the 2026-10-04 remediation plan".

**Wave 1: text outside the products,** four commits.

1. Procedure documents: items 5.2 and 6.1 to 6.5. Check:
   `py/main_test.py py/tests/test_review_turn_files.py`.
2. Instructions, skills and policy comments: items 5.3, 8.8, 8.1's skill half, 8.9, 4.4, 9.22's
   skill block, G and 3.5. Checks: `in/repo_maintenance_policy.json` still parses as JSON;
   `py/main_test.py py/tests/test_repo_visibility_declared.py py/tests/test_prose_conventions.py`;
   the changed block parses.
3. Maintained documents and records: items 7.5's page sentence, 8.7, 9.39, 9.22's eight document
   blocks and W1. Check: every changed `powershell` block, and the unlabelled block, parses with
   `[System.Management.Automation.Language.Parser]::ParseInput`, run from a scratch script.
4. Docstrings and comments: items 5.4, 7.2, 7.5's docstring and W2. Check:
   `py/main_test.py py/tests/test_product_scopes.py py/tests/test_parser_stage_node_keys.py py/tests/test_mega_coverage.py`.

**Wave 2: code fixes,** one commit each for items 4.5, 7.11, 7.8 and N2. Each re-runs its
demonstration on the committed code from scratch, as section 3 describes, with nothing reaching
MAM-private and nothing of repository maintenance run for real. Checks: for 4.5 and 7.11,
`py/main_test.py py/tests/test_phonetic_compute_boundary.py py/tests/test_phonetic_untangler_preparation.py py/tests/test_phonetic_display_release.py`;
for 7.8 and N2, `py/main_test.py py/tests/test_worktree_retirement_policy.py`.

**Wave 3: reader-facing documents that no program generates,** one commit: R2, R3, R4's item 1 and
R5. Check: `py/main_test.py py/tests/test_product_scopes.py py/tests/test_phonetic_display_release.py`.

**Wave 4: generated pages,** three commits.

1. R6 (items 8.1 and 9.2): edit `py/author_boj_qr/qr_38.py`, then run
   `./.venv/Scripts/python.exe py/main_gen_misc_authored_english_documents.py`, the
   `book-of-job-site` step, whose closing spell check must pass. Expected diff: the 38:12 details
   page under `gh-pages/book-of-job/jobn-details/` and `book-of-job/out/enriched-quirkrecs.json`,
   on the three changed strings alone.
2. R7 (item 8.3): edit `py/author_site/site_data.py`, then run
   `./.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys`. Expected diff: the
   one line of `gh-pages/index.html`. Check: `py/main_test.py py/tests/test_site_index_links.py`.
3. R8 (item 8.4): add `LICENSE_URL` to `py/mb_misc/mam_attribution.py`, edit the three
   `py/author_misc/` modules and the four `py/accgram/` page modules, and edit the two Aleppo pages
   by hand; then run `./.venv/Scripts/python.exe py/main_authored.py gen-misc` and
   `./.venv/Scripts/python.exe py/main_accgram.py generate-html-<name>` for `printed-decalogue`,
   `printed-decalogue-simanim`, `printed-decalogue-koren` and `printed-decalogue-uvinkha`. Expected
   diff: the nine pages, each gaining the line and nothing else. Check:
   `./.venv/Scripts/python.exe py/check_html_syntax_and_sanity.py gh-pages/aleppo`, and the same for
   `gh-pages/wlc` and `gh-pages/MAM-with-doc`, report nothing that the same runs at the wave's start
   did not.

**Wave 5: MAM-simple's notice (item 1.3),** one commit, then the hand-run check.

1. In `py/mb_cmn/public_data_consumer_notice.py`, `NARPAS_GROUPING_RULE` becomes a function of the
   label, `_narpas_grouping_rule(label)`, whose text is the current rule's with `{label}` in place
   of `מ:פסק`; `MAM_PARSED_NARPAS_GROUPING_RULE = _narpas_grouping_rule("מ:פסק")` goes into
   `mam_parsed_notice()` and `MAM_SIMPLE_NARPAS_GROUPING_RULE = _narpas_grouping_rule("lp-paseq")`
   into `mam_simple_notice()`. In `py/tests/test_public_data_consumer_notices.py`,
   `_assert_narpas_rule` takes the product's rule, and each notice test passes its own. R1's three
   sentences change.
2. Run `./.venv/Scripts/python.exe py/main_mam_simple.py core-only`, the export that the mega's
   `mam-simple` step runs. Expected diff: D1's 70 lines and nothing else under `MAM-simple/`;
   MAM-parsed's 24 plus files are not regenerated and do not change. Check:
   `py/main_test.py py/tests/test_public_data_consumer_notices.py`.
3. **The hand-run generators**, in scratch, since `AGENTS.md` requires rerunning them for this input
   change and Ben's exemption of 2026-09-30 covers only a text refresh. Extract the trees of the
   commit before wave 5 and of wave 5's commit with `git archive` into two scratch directories, and
   in each, from its root and with this clone's interpreter by absolute path, run
   `py/main_mam4sef.py`, `py/main_mam4sef.py --just-ajf` and `py/main_mam_osis.py`. Compare the two
   trees' outputs under `MAM-for-Sefaria/`, `MAM-OSIS/` and `gh-pages/MAM-OSIS/`. Expected: identical
   apart from the provenance lines that name the extraction folder, so the change reaches neither
   product, and their tracked files in this clone, with the lag Ben accepted, are left as they are.
   Record the comparison in the wave 7 entry.

**Wave 6: the Phonetic MAM correction (items 4.6 and 4.7, and N3),** one commit.

1. Make the code changes of section 3's item 5 and write the record, with each approval naming
   Ben's approval from wave 0. Add item 4.7's sentence to `dependent-refresh.md` and R4's item 2 to
   `Phonetic-MAM/README.md`.
2. Run `./.venv/Scripts/python.exe py/main_0_mega.py --resume-from phonetic-mam-export`, which
   re-exports the release through the private adapter, renders the site, and runs the surveys, the
   Yeivin claim projection and the site steps that follow. Expected diffs: D2, D3, D4 and R10, and
   nothing else.
3. Checks: `./.venv/Scripts/python.exe py/main_phonetic_mam.py check` lists no refreshed chapter
   and the three corrected ones;
   `py/main_test.py py/tests/test_phonetic_display_release.py py/tests/test_meteg_before_stress.py py/tests/test_final_stress_vs_phonetic_mam.py py/tests/test_yeivin_itm.py`.

## Final gate and records

1. **Integrate.** `git -C <checkout> fetch origin`. If `origin/main` moved, merge it into the local
   `main`, resolve any conflict there, and re-run the checks that the merged changes owe.
2. **Gate.** Run the mega and the suite on the integrated tree,
   `./.venv/Scripts/python.exe py/main_0_mega.py` and then `./.venv/Scripts/python.exe py/main_test.py`.
   The mega must leave no tracked diff and no untracked file; a failing step, a failing test or an
   unexplained diff stops the gate.
3. **Record (wave 7).** Append to `doc/review-findings-2026-10-04-update.md` the entry "Remediation
   executed, <date>", which records:
   1. the checkout, the `HEAD` at which editing began, and every commit;
   2. for each of the 39 items, its disposition: "fixed in `<commit>`" only after the item's own
      measurement was re-run on the changed tree and every site this plan names was checked against
      the commits that changed it, as `doc/periodic-review.md`, "Close-out: from findings to
      dispositions", step 3, requires; otherwise the reason it is not fixed;
   3. the 16 items left as they are and item 8.10's deferral, unchanged;
   4. item 8.4's census and the scope Ben approved;
   5. the hand-run comparison of wave 5;
   6. the checks and the gate's results;
   7. **Effective base State, <date>:** acted on; the remediation of the 39 items was integrated on
      `main` at `<commit>` on `<date>`, apart from any item the entry names as not fixed. The base
      report's line 3 stays as written, and the update remains `State: open` while its base
      survives.

   Set this plan's State to "executed <date>" in the same commit, whose message says that it
   changes only records, so the gate's results stand for it.
4. **Push.** Fetch again; if `origin/main` moved, return to step 1. Push `main`; a refused push
   returns to step 1.
5. **Deploy.** From this full clone run
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config`, which deploys items 8.8,
   8.1's skill half, 8.9, 4.4, 4.7's skill sentence and 9.22's skill block from the freshly fetched
   `refs/remotes/origin/main`, and then
   `./.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check`, which must report
   `USER_CONFIG_PROBLEM_COUNT=0`. Add both results to the entry in a last commit, whose message
   records that it skips the mega and the suite because it changes only the record, and push it.

## Not in this remediation

1. **The 16 items left as they are**, each with the reason the update entry gives: 3.1, 3.2, 3.3
   and 3.4 (under item 3.5's scope), 5.5, 7.4, 7.6, 8.2, 9.12, 9.13, 9.18, 9.21, 9.36, 9.38 and 9.42,
   and issue #296, which keeps the outward act of editing it out of this remediation.
2. **Item 8.10, deferred** to a separate cleanup task that Ben starts.
3. **Noticed while planning, not acted on**, since no item names them; each stays as it is:
   1. `doc/PLAN-silluq-before-gaya-template.md:290` and `:491` also begin with an unquoted
      `<home-clone>/.venv/Scripts/python.exe`, which parses only because the parser reads `<` as a
      command name, so item 9.22's parse-based census missed them (ps-blocks).
   2. `doc/PLAN-repo-maintenance-across-GitRepos.md:383` describes the forest write's refusal and its
      caller-only skip in the same order as `doc/clone-forests.md` did before item 7.5 (tool-code).
   3. The release has `ססס` for each of MAM's 328 song dividers, `מ:ששש`, which no README or schema
      describes; `py/author_misc/mp_cmn_rows_other.py:89–90` calls the divider "analogous to ססס"
      (break-markers).
   4. `py/author_misc/mp_cmn_rows_other.py:57` says that `פפ` and `סס` appear "primarily in D
      column", where MAM-parsed's C cells hold them and its D cells hold none (break-markers).
   5. `DATA-LICENSES.md` has no row for `gh-pages/near-aleppo/` or `out/near-aleppo/`, which arrived
      on 2026-10-05, after the review's window (attrib).
