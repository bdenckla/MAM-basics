# Findings of the 2026-09-08 review of the public repos since 2026-09-07

State: not yet acted on, except findings 1 and 3, which Ben settled on 2026-09-09 before the
Codex half ran. Finding 1: the Methods page and footnote φ1 now define "ignore" in Ben's words
— treat the word as a meteg-then-silluq word, i.e. deliberately misinterpret the marks, which
has little effect on the census and none on the bulk of the results — and the survey module's
comment says the same; the survey's classification is unchanged. Finding 3: Ben read the
printed BHS at 1 Samuel 17:5 on 2026-09-09 and confirms the two marks, meteg after silluq, so
the page's claim about BHS rests on that reading, recorded in `_post_silluq_comparison`'s
docstring and under the 2026-09-07 review's disposition table and not on the page (Ben's
decision); and the objection to "editions" for UXLC and WLC is withdrawn, the skill itself
calling WLC diplomatic and Ben's account being that WLC became an edition of its own and UXLC
diverged from both — an account github-misc `25a8955` (2026-09-09) put into the skill's source
table, which also brought finding 5.6's diverged `~/.agents` copy back into step. Separately
from the findings, three census figures this review re-derived below have since been
corrected, on 2026-09-09: 12,828 prose MBS_O chanted words and 14,614 in all are 12,849 and
14,635, and the Methods page's 143 two-meteg MBS_O words are 122. The census identified a
chanted word by its form until that day, so 21 prose forms occurring twice in one numbered
verse, each occurrence carrying one meteg, read as one chanted word carrying two. **This
review could not have caught it**: the arithmetic it checked, 12,962 + 1,805 less 143 and 10
= 14,614, is internal to the census and closes under either key, as 12,962 + 1,805 less 122
and 10 = 14,635 does now. The independent oracle that does catch it is
`py/foi/foiz_wt_mtgmtg.py`; `doc/post-stress-meteg-method.md` has the correction in full.
Written 2026-09-08, late evening, as the Claude half of the third
dual-agent review under `doc/dual-agent-review.md`, Design A: this file was frozen before any Codex
reviewer read it, and the Claude session neither read nor sought a Codex half (no file named
`codex-review-findings-2026-09-08*` exists, and nothing under `~/.codex/` or `Documents/Codex/` was
read beyond directory listings). Nothing was fixed. Before this file was committed, a check with
`has_std_mark_order` over its nine Hebrew runs found six in Unicode-normal order — lifted from the
data, which is in MAM-normal order, and reordered by the file-writing tool on the way in, which is
the mechanism CLAUDE.md's first section names — and `give_std_mark_order` put them back
(`.novc/review-2026-09-08/fix_findings_marks.py`). The reconciliation goes at the end of this file under
`## Reconciliation with the Codex review` once the Codex review is stable, and the dispositions
under a later `## Dispositions after remediation` section, per that document.

## Scope, anchors and census

Fifth review under the public-repos-only scope. It covers committed work from the 2026-09-07
review's anchor through the moment this review started, 2026-09-08 about 22:20 local, when
MAM-basics' HEAD was **`38a606e2`** (2026-09-08 21:49, "Record that the ITM and CoS gloss divergence
was accepted, not missed"), the tree was clean and `origin/main` stood at the same commit. **The
tree did not move under the review**: HEAD was `38a606e2` at the start and at every later check,
and the one live worktree, `C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg`, stood
clean at the same commit throughout. The six commits the 2026-09-07 review deliberately left
unreviewed (`6b5e4a40` … `d5a2238f`, 2026-09-07 11:26–11:56) are inside this window and were
reviewed here, as that review's remediation plan said they would be.

Anchors (start → end) and counts, re-measurable with
`git -C C:/Users/BenDe/GitRepos/<repo> log <start>..<end> --oneline`, or with
`gh api "repos/bdenckla/<repo>/commits?since=2026-09-07T14:35:00Z"` for the repos read on GitHub:

| Repo | Range | Commits | Non-merge |
|---|---|---|---|
| MAM-basics | `8bf586a3..38a606e2` | 98 | 92 |
| MAM-simple (GitHub, redirect host) | `9a350be5..376912a7` | 1 | 1 |

That is **99 commits across two public repos**. Fourteen public repos were quiet: the three other
clones MAM-OSIS, phonetic-hbo and Taamey_D (each clean, `main` at `origin/main`), and on GitHub
MAM-parsed, MAM-with-doc, MAM-for-Sefaria, codex-index-aleppo, codex-index-cam1753,
codex-index-leningrad, diffable-pointed-hebrew, book-of-job, holman-ketiv-qere, UXLC-utils and
wlc-utils. Three clones are private and fall to the private series: MAM-private (3 in-window
commits, one of them the goldens refresh the public Wave 3 record names), github-misc (2) and
hbofonts (0); the series' one deliberate exception was applied again, github-misc's
instruction-file plumbing being byte-compared (finding 5.6).

All 98 MAM-basics commits are authored Ben Denckla. **43 carry no `Co-Authored-By` trailer and 42
are subject-only**, all 43 on the `post-stress-meteg` branch's line — 39 page and prose commits
between 2026-09-07 13:00 and 2026-09-08 12:40 (`a572e20d` has a body but no trailer), and the four
`Merge branch 'main' into post-stress-meteg` merges. The 55 that carry one spell it four ways:
`Co-Authored-By: Codex <noreply@openai.com>` 18, `Co-authored-by: Codex <noreply@openai.com>` 16,
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` 14, `Co-Authored-By: Claude Fable 5.1
<noreply@anthropic.com>` 7. Six commits are merges: the four above, `d5a2238f` (`Merge branch
'post-stress-meteg'`, 2026-09-07 11:56) and `825cef66` (`Merge main, keeping plain "word" on the
nine post-stress-meteg pages`, 2026-09-08 19:00), after which `main` and the branch are one line, so
81 commits sit on `main`'s first-parent line (76 non-merge). The window changed 513 paths between
its endpoints — 19 added, 14 deleted, 480 modified — taking the tree from 5,507 to **5,512** tracked
files, 1,219 to 1,216 `.py`, `gh-pages/` 1,756 to 1,763 files (574 to 576 HTML), `doc/*.md` 51 to
57, `doc/PLAN-*.md` 10 to 13. By top-level directory: `gh-pages/` 327, `MAM-simple/` 51, `py/` 47,
`MAM-for-Sefaria/` 41, `doc/` 18, `out/` 8, `aleppo/` 6, `misc/` 5, the root 3 (`CLAUDE.md`,
`README.md`, `DATA-LICENSES.md`), `MAM-parsed/` 3, `book-of-job/` 2, `MAM-with-doc/` 1,
`cam1753/` 1. The 19 additions are six `doc/` files (three plans, two Codex reviews and the
2026-09-07 review), five manuscript crops under `gh-pages/img/`, five post-stress-meteg pages and
three tests; the 14 deletions are the four landed copies of `test_h_dot_below_nfc.py`,
`MAM-simple/py/main_test.py` and its `tests/__init__.py`, the three post-stress-meteg pages the
consolidation replaced (`-type-1-lacks-mas`, `-type-2-lacks-mas`, `-type-2`) and five files under
`misc/linux-sh/` (`window_census.py`, `window_name_status.txt`).

The window's substance is three things. 1. The `post-stress-meteg` branch's page work — the
Fit-for-MAS model's 2Af/2Bf refinement, the consolidation of the case pages, the Methods, not-fit,
next-conjunctive, 2 Chronicles 8:11 and 1 Kings 7:37 pages with four new manuscript crops, and a
38-item grammar pass — about 70 commits. 2. The remediation of the 2026-09-07 review, Waves 1–6 of
`doc/PLAN-remediate-review-findings-2026-09-07.md`, six implementation commits (`c76239a5`,
`e91d7358`, `4afe3ebc`, `a42216ee`, `9cf48863`, `975a16c5`) and their records, plus the two Codex
halves of that review (`e0b19b05`, `5dfbd7bd`). 3. The merge `825cef66` that reconciled the two
after they had fixed the same alt-text defect in opposite directions, implementing Ben's decision
of 2026-09-08 that the nine pages say plain "word", with the lint `a3e3f6eb` that enforces it,
followed by the silluq-before-meteg template plan (`772545d5`), two prose-liberty reverts and issue
#265 (filed 21:48, one minute before the anchor).

`GitRepos` holds 7 clones for a 7-folder roster, and no residue directory (the MAM-for-Sefaria
clone left for the Recycle Bin in Wave 5). The review ran as four agent streams plus the main
session: (A) the post-stress-meteg survey model and its generated artifacts; (B) remediation Waves
1, 3 and 4 and the six previously excluded commits; (C) the post-stress-meteg prose, the two
manuscript-evidence pages, the plain-"word" exemption, the two new plans and #265; (D) remediation
Waves 5 and 6, the disposition table, the two Codex files, `doc/dual-agent-review.md` and the
public records. Every script and output is untracked under `.novc/review-2026-09-08/` on the
machine that ran the review (copied there from the session scratchpad before this file was
committed; prefixed `A_` … `D_` per stream, unprefixed for the main session).

## Tree health at `38a606e2`: green, with the suite at 983

- Suite: **983 passed, 5 skipped, 65 subtests passed** (`.venv/Scripts/python.exe py/main_test.py
  -q`, 134.61 s, clean tree before and after apart from the self-ignored `.pytest_cache` the run
  rewrites). The chain from the last review's 976: Wave 4 (`a42216ee`) +5, then the plain-"word"
  lint (`a3e3f6eb`) +2 (`test_every_page_is_present`, `test_no_page_qualifies_word_as_chanted`);
  the merge message's "983 passed, 5 skipped" and the suite line print the same figures, and the
  suite does print a subtest line (finding 11.1). CLAUDE.md's "976 passed, 5 skipped" is the dated
  2026-09-07 record; nothing has carried 983 into it.
- `ruff check py` clean; `black --check py` clean at **1,167** files (1,164 at the last review).
- Zero `sys.path` mutations in tracked `.py`: the grep's 20 matches are the 13 `py/main_ac_*` /
  `py/main_cam1753_*` wrapper docstrings, `main_test.py`'s and `check_repo_standards.py`'s rule
  text. `--check-repo-standards --workspace-file all-repos.code-workspace --visibility public`
  sweeps 4 repos and reports exactly what the Wave 6 record says: MAM-basics LINKED_WORKTREES=1
  (the Codex worktree), AGENT_BRANCHES=0, ORPHAN_MARKS=0, HEX_ESCAPES 80, NFC_H_DOT 30, NFC_LATIN 49;
  Taamey_D GITATTRIBUTES_LF=False as before (`standards-public.txt`).
- Mark order over every `.py`, `.md`, `.json`, `.html`, `.css`, `.js` and `.txt` file the window
  added or modified outside the landed data trees, `in/mam-ws*`, `out/` and `misc/` (391 files,
  10,398 Hebrew runs): **zero non-MAM-normal runs on lines new in the window**; 37 sit on
  pre-existing lines of nine files (`doc/PLAN-holman-meteg-rollout-programme.md` 6,
  `doc/PLAN-post-stress-meteg-page-and-holman-m23.md` 3, `doc/holman-meteg-m13-qamats-template.md`
  3, `doc/holman-meteg-m23-isaiah-23-12.md` 10, `gh-pages/uxlc/amb-early-mtg/full-record/amb-early-mtg-15.html`
  1, and four `gh-pages/wlc/accgram/` pages 14), the same class the last two reviews left
  unexamined. The nine post-stress-meteg pages (1,007 runs) and the three `gh-pages/aleppo/` pages
  (481 runs) are clean (`mark_order_window_scan.py`, `A_12_overlap_stress_and_mark_order.py`).
- Markdown links: 243 relative links in 169 tracked `.md` files, one dead and pre-existing, the
  same `misc/what-is-mam/img/provenance-misc.md:6` as the last review (`md_links_check.py`).
- Pages: all 23 MAM-basics deploy runs created in the window succeeded, from `9e6e9e17` to
  `38a606e2`; MAM-simple's run at `376912a7` succeeded (`gh_runs.py`, `gh_census.py`).
- Issues: #265 was opened at 21:48 on 2026-09-08 by a Claude session and has 0 comments; nothing
  else was opened, closed, commented on or relabelled; 96 open.
- The MAM-OSIS clone, which the window's mega runs wrote into (directory modified 2026-09-08
  17:22), is clean at `697dc98`, so the runs reproduced it byte for byte.

## What verifies sound, stream by stream

**The post-stress-meteg survey model and its artifacts (stream A).** All eleven deploy-root pages
regenerate byte-identically from the tracked `out/accgram/post-stress-meteg.json` (the nine
post-stress pages with `trust_survey=True`, `unicode-proposals.html`, `index.html`), with
`pin_claims` raising nothing. **The merge kept Wave 2's census and the branch's fit model**: the
JSON counts 233,277 prose and 29,542 poetic chanted words (262,819), MBS_O 12,828 and 1,786
(14,614), MAS 178 and 54 (232), and a qamats-variant census of 309 + 61 = 370 rows and 309 + 63 =
372 duplicate entries, so that 263,191 source entries = 262,819 + 372; the main page shows those
figures; the five qamats-variant functions and the `build_survey` invariants are present; and
`FIT_TYPE_2_AF` / `FIT_TYPE_2_BF`, the vocal-shewa condition and the fit table 377 / 200 / 53.1% /
177 with 2Af 38 / 35 / 92.1% / 3 and 2Bf 45 / 15 / 33.3% / 30 are on the page, never the older
384 / 184 / 52.1%. All 56 JSON-derived figures on the nine pages re-derive (`A_07_page_figures.py`):
the type table 123 / 60 / 42 / 7 with its prose–poetic splits, the subtype tables, the fit table
row by row, "93.5%" = 217 of 232, the 15 next-conjunctive, 177 lacks-MAS and 32 not-fit cases, the
Methods page's 143 two-meteg MBS_O words, its ten MAS-with-MBS words and their labels, its 6
oleh-sharing metegs and its template counts, φ2's four nonfinal cases, φ6's 56 of 60 and 154 / 136
/ 18. The JSON's arithmetic closes (`by_fit_type`, the 32 not-fit records, 53,964 candidate chanted
words, the partition of the 232, the two per-system qamats invariants, 12,962 + 1,805 less 143 and
10 = 14,614). **The public oracle matches the JSON exactly**: a walk over phonetic-hbo's pages at
`7322b665` (23,202 numbered verses, no parse problem) gives 233,277 / 29,542 chanted words, 12,962 /
1,805 pre-stress, 178 / 54 post-stress, 18,738 / 4,465 silluq, and the same 232 MAS records with the
page's stressed syllable agreeing in 232 of 232; the 9 currency differences are all genuine deḥi
cases and 38,161 against 38,170 re-derives; φ6's "all 154 in Aramaic" is true (the 5 tsere-plus-he
words outside Daniel and Ezra all have a furtive pataḥ); the author module's guttural, resh, bet
and mem lists re-derive. The poetic accent-grammar artifacts (`out/accgram/poetic/*`,
`_servi_xcheck.txt`, `_grammaticality.txt`, `research-oddballs.json`, `gh-pages/wlc/accgram/poetic.html`)
regenerate byte-identically, so `5772cd50`'s cross-chanted-word yored fusion (two MAS records'
next word reclassified, 215 / 17 → 217 / 15) and `a572e20d`'s cross-atom rule re-derive. Each model
commit's mechanism is at HEAD with its figures (`7155065d`, `bdcdc5e2`, `97a1b46f`, `dadab0ba`,
`4a454eeb`, `39133db0`, `a5435a41`, `c027784d`, `d7049855`, `c5b170ad`, `0afbae68`); Wave 2's
type-3 finality in all three places, the completed type-2 rename, the deferred next-word mismatch,
the tolerant `_intervening_punctuation`, the 2-tuple `_TYPE_SOURCES` and the one-file `_wlc_words`
all hold; the three reverts changed no data; and the three typed Leningrad forms of the 2
Chronicles 8:11 page are in MAM order.

**The remediation's Waves 1, 3 and 4 and the six previously unreviewed commits (stream B).** The
`<scrdfftar>` reader now handles every live shape: 32 targets in five shapes across the 24
`MAM-simple/xml-vtrad-mam/` files (24 with a `text` attribute, 3 with a `spi-pe2` child, 2 with an
`slh-word` child, 2 empty, and Deuteronomy 32:6 alone with `slh-word` then `text`), and it returns
13 chanted words for Deuteronomy 32:6 where the reader at `c76239a5^` returned 12; an unknown child
raises. The three line-data edits agree with the three scan crops (both atoms of the Deuteronomy
32:6 target on 004r line 15; nothing after 005v's last line-end; 006r column 1 line 1 opening on
the Deuteronomy 33:29 chanted word), and both line-break reports recompute to scratch byte-identical
to the tracked ones (Aleppo 91 issues, Cambridge 1753 "All checks passed"); adverse probes of a
vowel, an accent and a dagesh are caught by both checks while a removed meteg or rafe is tolerated,
which is exactly the narrowing `no_marks_comparison_key` now implements (it removes U+05BD and
U+05BF and nothing else of 122 probed codepoints). `letter-small-job` reads
`MAM-simple/xml-vtrad-mam/Job.xml`, reproduces the tracked SHA-256 `a0ac8005…` in memory, and an
adverse missing-input run raises before creating the output or its `.tmp`. Wave 3's 390 files are
377 pure host rewrites, 6 host rewrites that also moved a line wrap, and exactly the seven other
files the record names; the old-host census at HEAD is 47 hits in 45 files, the record's three
categories with `doc/PLAN-evacuate-public-repos-programme.md` as the one documentation file. All
44 `MAM-simple/py-examples/` copies are blob-identical to their sources at HEAD and at every commit
from `7b11fd6b` on (39 of 44 at `8bf586a3`), every copy is LF, and the inventory and provenance
outputs reproduce to scratch. `REPO_MAM_PARSED_DIR` is the absolute consolidated `MAM-parsed/`. The
Wave 4 NFC scopes re-derive to the record's ten counts (1,491 at `a42216ee`, 1,489 today); the
mark-order scope is 241 files with both required files present; the machine-path lint scans 1,436
files (the record's 1,435 plus the ninth page) and both excerpts are present; the two Aleppo pages
equal `give_std_mark_order` of their parent-commit text with no other change; `diff_mpp` prefixes
`legacy:` before choosing the output path and the adverse test iterates all five releases; the +5
from 976 to 981 are Wave 4's five new test items and the +2 to 983 the plain-"word" lint's. Every
claim in the six commits `6b5e4a40` … `d5a2238f` re-derives (the four repo-name sites, 44 of 44
copies at `7b11fd6b`, the literal `"MAM-basics"` at `scan_pages/index_io.py:54`, the inventory's
38 + 6 `last_synced` dates).

**The post-stress-meteg prose, the manuscript-evidence pages, the plain-"word" exemption, the two
new plans and #265 (stream C).** "chanted" occurs 0 times in each of the nine pages, attributes
included, and the lint passes, names exactly the nine tracked pages from `site_data`, fails on a
missing page and folds case; nothing outside the nine leaks the plain-"word" register (the 19 other
`gh-pages/` pages using "chanted" are accgram, MAM-simple, MAM-for-Sefaria and MAM-with-doc pages
where "chanted word" is the house term). Every figure in #265 re-derives (578 tracked pages under
the link graph's count, 19 pages, the nine at 0, 149 `word` matches on 131 lines, the
`("Words", "chanted words checked")` tuple, the `# combining-ok` escape hatch, 13 files and 32 hunks
by a read-only `git merge-tree`, 440 case-sensitive). On the nine pages every Hebrew cell is
`dir="rtl"` (505 of 505) and no rtl cell lacks Hebrew; no line opens on a Hebrew letter; 0 hits for
"witness", bare "Simanim", "the former/latter", transliterated strand names, prose or poetic "books",
"cantillation accent", "proclitic", "word-division", hyphenated section ranges or "ṣere"; ITM/CoS
citations take one shape; the pashta helper is described as a helper; every heading names its
subject; MAM is nowhere a Breuer edition. Every `<img src>` names one of the six tracked files under
`gh-pages/img/`, and every Leningrad and Aleppo claim on the three evidence pages stands beside its
crop, the one exception being finding 3. The five post-stress docs quote the JSON's figures exactly
(232 = 178 + 54; 233,277 / 29,542; 12,828 / 1,786; 18,738 / 4,465; 12,962 / 1,805; 370 rows and
372 duplicate entries; 23,184 verses, 9 differing, 38,161 against 38,170; the 217 / 15 split; the
ten MAS words with an MBS). The silluq plan's data claims hold from public data: two U+05BD in the
verse-final atom at 1 Kings 7:37 in MAM-simple, MAM-parsed and `in/mam-ws`, its quoted source
call byte-for-byte the wikitext's, `ch5.mediawiki:426` spelled `סילוק`, phonetic-hbo#78 open,
MAM-basics#57 open, MAM-for-JPS and MAM-for-CCAR archived. The two reverts and the grammar pass
left the pages as their messages say, and `38a606e2`'s comment records the ITM/CoS decision with
Ben's words and the date.

**The remediation's Waves 5 and 6, the disposition table, the two Codex files and the public
records (stream D).** Row 7 holds in full: bare `check` and bare `build` exit 2 for the missing
`--repo`, and `build --repo wlc-utils` to scratch yields 154 stubs plus `404.html` that `check`
accepts. The MAM-for-Sefaria clone is gone and `GitRepos` holds exactly the roster's seven
directories; the MAM-simple redirect host's README is dated (`376912a7`); the fourth-stage plan
records the retirement with the `34c94a8` / `746d6d2` patch match; the third-stage records, the
manifest spelling, the runbook's forest and clone rules, the 37 = 24 + 13 JPEG count and the
162 = 83 + 72 + 7 line-break JSON count re-derive; `misc/linux-sh/` holds only
`linux-clone-MAM-basics.sh`; `README.md` names none of the four retired options or programs and
numbers its two declarations; `DATA-LICENSES.md` numbers its three things, covers the six crops and
the twelve byte-identical `Taamey_D.woff2` copies, and places the MAM statement in the four landed
`LICENSE.md` files. The link graph at `8bf586a3` gives Sol's 576 / eleven / zero exactly and at
HEAD 578 / the nine recorded orphans / zero, the ninth post-stress page being linked from the main
page. Row 22's plumbing is identical everywhere it is tracked (`~/.claude/CLAUDE.md` 98,434 bytes,
`~/.codex/AGENTS.md` 85,629 bytes and 1,077 lines, both skills, both `dot-Codex/skills/` copies)
with the one exception of finding 5.6. Six of `py/check_all.py`'s seven checks pass when run
read-only (mark order over 459 files, escapes over 296 `.py`, QR consistency over 160 files, the
HTML lints); the seventh, the spell check, writes two tracked frequency files and was not run. The
Terra and Sol files' commit, path, whitespace-total and link-graph claims re-derive, and the
review's two reconciliation sections state what the Codex files state. No figure in the messages of
`f5df191e`, `47edbee6`, `9cf48863`, `975a16c5`, `15ec6f4d`, `e0b19b05`, `5dfbd7bd` or `9e6e9e17`
is contradicted by its diff.

**Main session.** The commit, trailer and merge census; the roster and clone census; the doc/
`State:` lines; the HTML counts at four commits (574 → 575 → 576 under `gh-pages/`, 9 → 10 → 11 at
the deploy root); the read-only merge dry run (13 files, 32 hunks); the "chanted" counts (440 and
442 at `15ec6f4d`, 0 on the nine pages, 19 other pages); the suite, black, ruff, the standards
sweep, the mark-order and markdown-link scans; the Pages runs and issue state; and the independent
re-derivations recorded under findings 1, 2, 3, 4, 5.1, 5.6, 6, 7.1 and 17 below.

## Findings

In rough order of consequence. Nothing was fixed. Line numbers are as measured at `38a606e2`.

1. **Published-page claim against the classification the survey makes, unfixed: the Methods page says
   MAM has a meteg after silluq at 1 Kings 7:37 and that "we ignore it for the purposes of this
   research", while the survey files that word as a meteg-before-stress word and pins MAM's
   post-silluq count at zero.** `gh-pages/post-stress-meteg-methods.html:72–77` (heading "Meteg
   after silluq in 1 Kgs. 7:37"; "in MAM, there is a meteg after silluq in לְכֻלָּֽהְנָֽה׃. We ignore
   it for the purposes of this research"), the two crops' alt texts (`:78`, `:82`), footnote φ1 on
   the main page, `py/accgram/post_stress_meteg.py:2242` ("MAM's post-silluq case, which the
   research ignores") and `doc/PLAN-silluq-before-gaya-template.md:5–7` ("the first serves as
   silluq and the second is a meteg") all take the first U+05BD, on the atom's לָּ, as the silluq.
   The survey's stress oracle does not: phonetic-hbo's public page for 1 Kings 7 renders the
   verse-final word `le·khul·lah·[na]`, stress on the last syllable, so under the survey's rules the
   U+05BD on לָּ is a meteg before the stress and the U+05BD on נָה is the silluq; the JSON has no
   `post_stress` record at 1k7:37, its `post_silluq.in_mam` is 0 and `pin_claims` asserts that 0
   (`py/author_site/post_stress_meteg.py:1183–1185, :1212`), and the word is one of the 12,828
   prose MBS_O words rather than a word the research ignores. The oracle reads the same suffix at
   Genesis 42:36, whose verse-final כֻלָּֽנָה has one U+05BD, as `khul·[la]·na`, stress on the
   syllable of that mark; and in all 597 verse-final chanted words with two or more U+05BD on the
   public pages the stress falls on the syllable of the last one (583 as meteg + silluq, 14 as
   meteg + meteg + silluq), so the oracle's readings never yield a post-silluq meteg and
   `in_mam == 0` reports those readings rather than a measurement independent of them. Against
   that, `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:1145` says "MAM HAS NO POST-SILLUQ
   METEG, and this run is what establishes it". Which reading of 1 Kings 7:37 is right — the page's,
   which is also MAM's documentation note's and the silluq plan's, or the oracle's — is not settled
   here and is Ben's; what the page states as a fact about MAM contradicts the classification the
   census makes of the same word, the page does not say so, and the record claims more than the run
   shows. Re-establish: `A_06_focus_verses_probe.py`, `A_08_two_meteg_verse_final.py`; `Grep
   '"in_mam"' out/accgram/post-stress-meteg.json`.

2. **Record error, unfixed: disposition row Sol-1 says "fixed", and every one of the 210 whitespace
   findings is still in the tree.** `doc/review-findings-2026-09-07.md:908` says `4afe3ebc`
   "regenerates the affected artifacts and makes the current `git diff --check` pass", and the Wave
   3 record (`doc/PLAN-remediate-review-findings-2026-09-07.md:448–451`) says the same. At
   `38a606e2` all 189 files Sol flagged for a blank final line still end in one (111 under
   `MAM-simple/misc/unicode-names-*` and `MAM-simple/py-examples-out/sefaria/`, 78 under
   `MAM-for-Sefaria/misc/unicode-names*`), and all 21 trailing-whitespace lines are still in the
   same four files (`MAM-for-Sefaria/csv-ajf/Deuteronomy.csv` 5, `Exodus.csv` 4,
   `gh-pages/MAM-for-Sefaria/index.html` 11, `style-color-scheme-light.css` 1). None of those 193
   files is among the 390 files of `4afe3ebc`. The blank final line is generator-emitted
   (`py/mb_misc/write_utils.py::_write_verse_un` writes a newline after every verse) and the
   trailing spaces sit on the Decalogue rows of the AJF CSVs and in the generated MAM-for-Sefaria
   index, all MAM-basics-owned outputs. The three checks the record ran can only pass: a
   no-argument `git diff --check` on a clean tree compares the working tree with its index, and a
   range form flags added lines only, so untouched offenders are invisible to both — the shape of
   verification that cannot fail. Re-establish: `whitespace_now.py` (main session) or
   `B_11_whitespace.py`; `git diff --check b4706759 8bf586a3` for the file list.

3. **Rendered-page claim restored by Ben's blanket revert, and two disposition rows now false: the
   post-silluq page again says the meteg "is correctly recorded in BHS and in BHS-derived editions
   such as UXLC and WLC", over a "BHS" row derived from UXLC 3.9 and WLC 4.22.**
   `gh-pages/post-stress-meteg-post-silluq.html:75–76` and `:83` (MAM נְחֹֽשֶׁת׃ against the row
   labelled BHS, נְחֹֽשֶֽׁת׃); `_post_silluq_comparison` (`py/author_site/post_stress_meteg.py:2545–2571`)
   binds `bhs_form_from_uxlc` and `bhs_form_from_wlc`, asserts them equal and labels the result
   `"BHS"`, `_post_silluq_leningrad_form` (`:2621–2624`) calls it "The BHS transcription", and
   `pin_claims` (`:1188`) asserts that "BHS" form has two U+05BD; no BHS text is read anywhere.
   That is the last review's finding 13.3, fixed by `e91d7358`, kept by the merge (its message,
   item 1) and restored by `a9edd4f9` (21:45), whose message records Ben's decision of 2026-09-08
   to "revert every unrequested rewrite `e91d7358` … made" and lists this sixth revert by name,
   justifying it as undoing a regression against `f05738e6`'s one-row table rather than as a
   judgment on the claim. The manuscript sentence itself (line 64) rests on the crop and is sound;
   what rests on the transcriptions is the claim about BHS and the word "editions" for UXLC and WLC
   (the global rule "A transcription is evidence about the transcription, never about the
   manuscript" and the skill's "WLC, BHS 1997 and BHQ are usually ONE transcription"). Rows 13 and
   21 of the disposition table (`doc/review-findings-2026-09-07.md:896, :904`) and the plan's Wave
   2 result (`doc/PLAN-remediate-review-findings-2026-09-07.md:355–358`, "identifies UXLC 3.9 and
   WLC 4.22 as the transcriptions actually read, defines the dual cantillation labels, uses one
   shared ITM/CoS link implementation") say "fixed" for this and for what the two reverts undid
   with it: the "cant-alef" / "cant-bet" gloss is gone again (`post-stress-meteg-methods.html:175`),
   the shared `almost_errors_html_shared.itm` / `cos` gave way to local glosses (`:193–199,
   :1276–1283`, recorded as accepted by `38a606e2`), the φ1 callout again sits on "In every MAS
   case, the stressed syllable has a conjunctive accent" with no sentence saying why a meteg after
   silluq in the Leningrad Codex bears on it (`post-stress-meteg.html:113`), and "on a page of their
   own" is back (`:178`). Both reverts postdate `15ec6f4d` "Close the 2026-09-07 remediation"
   (18:04) by three and a half hours and nothing re-opened the rows. Ben's decision: whether the
   BHS wording stands knowingly; the rows want a dated correction either way. Re-establish: `git
   show a9edd4f9 -- gh-pages/post-stress-meteg-post-silluq.html`; `C_diff_a9edd4f9.txt`;
   `A_10_commits/a9edd4f9_src.patch`.

4. **Record error introduced by `9cf48863`, unfixed: the maintenance runbook's new scope paragraph
   tells a session to do what the roster rule it cites forbids.**
   `doc/PLAN-repo-maintenance-across-GitRepos.md:21–24` ("Current scope … corrected 2026-09-08")
   says `repos_to_keep_absent` "names repositories that must not be cloned" and instructs "Apply
   every clause, including the frozen-repository and keep-absent subtractions and the two added gist
   clones." Clause 4 of `gitrepos_setup_rule` (`in/repo_maintenance_policy.json:70`) says "There is
   no exclusion list to consult … neither key is READ to reach that result — omission alone does
   the work", the `gists` key says neither gist is cloned on any machine, `all-repos.code-workspace`
   lists seven folders and no gist, and `GitRepos` holds exactly those seven. The paragraph
   re-creates the enumerate-and-subtract proxy the rule exists to reject, in the runbook a
   maintenance session reads first. Re-establish: `Read` the two files at the lines named.

5. **Disposition rows that hold only in part, unfixed — the residue of the 2026-09-07 remediation,
   row by row.** Rows 1–6, 8, 12, 16 and 17 hold through their commits and the streams' code and
   data checks; rows 7, 14, 15, 19, 20, 23 and 24 hold; rows 13 and 21 are finding 3, row Sol-1 is
   finding 2, and row 3 is finding 8.1. The residue:
   1. **Row 11**: `doc/PLAN-evacuate-the-rest-of-three-repos.md:1853` still says "The current suite
      no longer prints a subtest line" (this review's run printed `65 subtests passed`);
      `doc/review-findings-2026-09-04.md:743` still says "Six merged local MAM-basics branches" and
      rejects "changing the deliberate primary-clone constant" removed by `4195440e`, and `:567`
      still says `~/.Codex/plans/` "does not exist" (it holds four entries) — frozen finding text
      that wanted a dated correction beside it, and got none; and
      `gh-pages/holman/table_data_findings_suppressed.html` still has **49** Hebrew-holding
      comparison cells with no `dir="rtl"` (32 `comparison-name-col`, 17 `comparison-symval-col`)
      and `table_data_findings.html` 1, the exact counts of the last review's finding 11.5
      (`holman_rtl_cells.py`, main session).
   2. **Row 9**: `doc/PLAN-evacuate-public-repos-programme.md:832` still says a sparse checkout
      "neither exists today" while `MAM-simple/README.md` and `MAM-parsed/README.md` give one;
      its row 43 (`:43`) still credits `3c8c9750` with the workspace and visibility-map removal
      that `19df42f3` made; its row 42 (`:42`) still says the MAM-for-Sefaria clone "remains pending
      its separate safety report" after `9cf48863` itself recorded the retirement; and
      `doc/PLAN-evacuate-five-MAM-products.md:555` still lists the MAM-with-doc host's files
      without its two dotfiles.
   3. **Row 10**: `cam1753/doc/reading-mam-simple.md:30` still says "and this repo's was deleted"
      of codex-index-cam1753's copy.
   4. **Row 18**: `py/tests/test_sibling_reach.py:34–35` still quotes the argparse help "Old git
      revision (in ../MAM-parsed repo)", which now occurs nowhere but in that docstring
      (`diff_mpp.py:198–203` reads "Stored release or MAM-basics revision"); and, unnamed by the
      finding, `py/vendoring/gen_inventory.py:350` writes "These Python files live outside
      MAM-basics and are intentionally maintained in their destination repos" into
      `doc/vendoring-inventory.md:33` above four rows whose paths are all inside MAM-basics.
   5. **Row 21**: `doc/PLAN-evacuate-public-repos-programme.md:915` keeps "its own docstring says";
      the 2026-09-04 review's "Six merged" (item 1) is still an announced count with no numbered
      items; three "own" sites in the named files fail the contrast test (`doc/dual-agent-review.md:210`,
      `CLAUDE.md:80`, `DATA-LICENSES.md:56`).
   6. **Row 22**: the identity result it relies on had lapsed before the remediation began.
      `C:/Users/BenDe/.agents/skills/hebrew-prose/references/sources-and-corpora.md` (17,893 bytes)
      differs from `C:/Users/BenDe/.claude/skills/hebrew-prose/references/sources-and-corpora.md`
      (18,023 bytes), which is byte-identical to github-misc's tracked copy; the divergence dates
      from github-misc's commit of 2026-09-07 12:44, after the last review's plumbing check and
      before the remediation started. The other four files of the skill are identical between the
      two homes; the `~/.agents` copy is tracked nowhere (`dot-Codex/skills/` tracks
      `prune-claude-state` and `worktree-forest` only). Wave 6's "No instruction file changed
      during remediation" is true of the remediation window and false as the premise for carrying
      finding 22 forward. Re-establish: `skill_copies.py` (main session), `D_plumbing_compare.py`.

6. **Stale since the merge `825cef66`, unfixed: eight sites, seven saying ten deploy-root pages
   or eight post-stress-meteg pages and one saying 34 anchors.** The deploy root has held eleven HTML files
   and nine `gh-pages/post-stress-meteg*.html` pages since 19:00 on 2026-09-08, when the merge
   brought `post-stress-meteg-next-conjunctive.html` (`39133db0`, 14:12 on the branch) onto `main`.
   Written earlier that afternoon and true then:
   1. `README.md:67` — "the ten deploy-root pages … the eight `gh-pages/post-stress-meteg*.html`
      pages" (`9cf48863`).
   2. `DATA-LICENSES.md:72` — "the eight generated post-stress-meteg pages" (`9cf48863`).
   3. `py/main_authored.py:9–12` — "the ten published pages … the eight", the hunk the merge took
      from `main` while updating the comment at `:134` to "all nine pages" and the page set to
      nine, so the merge message's "py/main_authored.py … the counts are the branch's" is true of
      the comment and not of the docstring.
   4. `py/main_0_mega.py:404–406` — "the ten deploy-root pages … eight post-stress-meteg pages"
      (`9cf48863`).
   5. `py/check_html_syntax_and_sanity.py:28` — "the ten HTML files" (`a42216ee`); the checker
      globs the directory and checks all eleven.
   6. `doc/PLAN-post-stress-meteg-page-and-holman-m23.md:13` — "ten deploy-root pages, including
      eight" (`e91d7358`).
   7. The same plan's line 100 — "it regenerates ten, including eight post-stress pages".
   8. `py/tests/test_site_index_links.py:84` — "this page carries 34", where the walk returns 35
      since `9cf48863` added the MAM-for-Sefaria entry; the floor asserted is 25.
   `site_data.py:98` and
   `:108`, the plain-"word" lint and the merge message have eleven and nine. Re-establish:
   `html_count.py` (main session); `git grep -n -E 'ten HTML files|ten deploy-root pages|ten
   published pages|eight generated post-stress|eight post-stress-meteg|including eight' 38a606e2`.

7. **Two new plans with no `State:` line, one of them spent, and the standard's docstring wrong
   by three, unfixed.** The doc/ standard (`py/repo_util/check_repo_standards.py:269–272`) puts
   `State: <word> [date]` at line 3 of every `doc/PLAN-*.md`; nothing checks it (`State:` occurs in
   that module only in its docstring), and line 270's "At 2026-09-08, all ten tracked `doc/PLAN-*.md`
   files carry it" was wrong by one when `9cf48863` wrote it (11 plans then, the remediation plan
   having arrived at 12:08) and is wrong by three now: 13 plans, 11 with the line.
   1. `doc/PLAN-merge-post-stress-meteg-into-main.md` (`27f729e8`, `3fa7a592`, 18:11–18:12): line 3
      is prose. It was executed by `825cef66` 49 minutes later and does not say so; its lines
      100–102 list "census 263,191 words, 14,752 MBS_O" among the figures that "must not change",
      while its line 56 gives `main` the survey module — and `main`'s module (Wave 2's qamats-variant
      fix, the last review's finding 3) yields 262,819 and 14,614, which is what the merged page
      shows (`post-stress-meteg.html:101–102`) and what the merge message explains at length; the
      fit figures it protected did survive. Its line 87 pairs the figure 440 with `grep -c chanted …`,
      which counts matching lines (381), not occurrences. With the merge base, the conflict counts,
      the resolution rule and the figures all history, it is a doc that "only records finished
      work" under the standard's first sentence.
   2. `doc/PLAN-silluq-before-gaya-template.md` (`772545d5`, 19:55): line 3 is `## Summary`. Its
      filename says "gaya" where its text decides that "Python names, MAM-simple names, and English
      prose use *meteg*" (lines 25–26, 65–66), its element is `silluq-before-meteg`, its OSIS note
      type `x-silluq-before-meteg`, and its commit subject "silluq-before-meteg"; the filename is
      the one English site "gaya" survives in (the skill's table: meteg, not ga'ya). Against the
      fresh-session rules, no decision in its "Decisions and public contracts" section is attributed
      or dated. Its line 279 calls "976 passed, 5 skipped, and 65 subtests on 2026-09-06" the last
      recorded baseline, where `CLAUDE.md` records 976 on 2026-09-07, the remediation plan 976 / 5 /
      65 on 2026-09-08 and the branch 978 at `a3e3f6eb`; and its baseline "all at `825cef66`" is
      four commits stale, which its re-measure clause covers. Its data claims all hold (stream
      C above), and its reading of the two marks is the one finding 1 is about.
   Re-establish: `git ls-files doc/PLAN-*.md`; `Grep '^State:' doc/*.md`; `git blame -L 269,271
   py/repo_util/check_repo_standards.py`.

8. **Post-stress records that misdescribe the model, unfixed:**
   1. **Row 3 and the Wave 2 result attribute the 368 / 370 versus 370 / 372 difference to the source
      having moved, when it is a difference of scope.** `doc/PLAN-remediate-review-findings-2026-09-07.md:334–336`
      ("The review-era Sol correction of 368 qamats-variant rows and 370 duplicate entries had become
      historical: the current source has 370 rows and 372 duplicate entries") and
      `doc/review-findings-2026-09-07.md:886`. phonetic-hbo has had no commit since `7322b665`, and
      its public pages today give exactly Sol's 368 rows and 370 duplicated chanted words outside
      dual-cantillation verses (307 / 61 rows, 307 / 63 duplicates); the two rows that make 370 / 372
      are the qamats rows inside the dual-cantillation verses Exodus 20:4 and Deuteronomy 5:8, both
      the row of תעבדם, which Sol's public-page method excluded and the survey counts. Both counts
      were and are right for their scopes; neither record says which scope each counts
      (`A_03_variant_rows.py`, `A_03b_dual_qamats_rows.py`).
   2. `doc/post-stress-meteg-method.md:14–15` says "Type 3 is a closed, final, tsere-vowelled
      syllable after a retracted stress"; the classifier tests penultimate stress with a conjunctive
      accent and nothing about retraction (`py/accgram/post_stress_meteg.py:1399–1411`). The
      sentence is `main`'s type-3 gloss, which the merge message says the method doc kept.

9. **Licence and evidence-page records, unfixed:**
   1. `DATA-LICENSES.md:83` says `MAM-with-doc/` holds a "retained source-hygiene test" — written
      by `9cf48863` at 17:32, 73 minutes after `a42216ee` deleted
      `MAM-with-doc/py/tests/test_h_dot_below_nfc.py`; `git ls-files MAM-with-doc` lists four files.
      The same commit rightly dropped the phrase from the `MAM-for-Sefaria/` row.
   2. `DATA-LICENSES.md:73` covers the six crops under `gh-pages/img/` in one row that names no
      photograph source or rights holder for any of them, where the last review's finding 14.1
      asked for one and the neighbouring `aleppo/aleppo-pages/` row (`:87`) names its source; and
      only one of the six captions names folio, column and line (`post-stress-meteg-post-silluq.html:66`,
      the 1 Samuel 17:5 crop of F159A), the other five naming codex and verse only.
   3. `post-stress-meteg-methods.html:78` shows the Aleppo Codex crop of 1 Kings 7:37 with no
      visible sentence saying what the Aleppo Codex has there; only the `alt` text says "it has a
      meteg after the silluq", and the paragraph above is about MAM.

10. **`doc/dual-agent-review.md` does not know about this window's precedent, unfixed.** Line
    24 still says "Eight such files exist, from 2026-07-29 to 2026-09-04; the 2026-09-04 file has
    the first Codex counterpart": nine files exist through 2026-09-07, and the 2026-09-07 file has
    two Codex counterparts, the second under a `-sol` suffix the naming section (`:165–174`) does
    not mention; the calibration section (`:55–58`) describes the 2026-09-04 run only; the `State:`
    vocabulary is unreconciled (`doc/codex-review-findings-2026-09-04.md` says `acted on
    2026-09-07`, the two 2026-09-07 Codex files say `completed 2026-09-08`, and the standard's glob
    `doc/review-findings-*.md` matches neither Codex name); and line 249, added by `9cf48863`,
    spells its command's path with backslashes (`C:\Users\BenDe\.Codex\AGENTS.md`), against the
    authored-paths rule. Its line count of `~/.codex/AGENTS.md` (1,077) is right. The rename
    measurement's command gives 97 lines across 30 files at HEAD (81 across 26 at `8bf586a3`).

11. **Internal contradictions and imprecision in the remediation records, unfixed:**
    1. `doc/PLAN-remediate-review-findings-2026-09-07.md:523` (Wave 4) says "The current suite output
       had no subtest line, so this record does not infer one", while its Waves 1, 2, 3 and 6
       (`:268, :366–367, :455–456, :639`) report "65 subtests passed"; the suite at HEAD prints
       `983 passed, 5 skipped, 65 subtests passed`, and none of the six test files `a42216ee`
       touched uses `subTest`, so the missing line was a reporting artifact of that one run. The
       three-repos plan's line 1853 (finding 5.1) says the opposite of the same fact.
    2. The plan's Wave 1 and Wave 2 checklists (`:210–225`, `:282–315`) are still `- [ ]` under
       headings that say completed, while Waves 3–6 are `- [x]`.
    3. Wave 6's "all 25 Python files changed in Wave 5": `9cf48863` changed 26, the 25 under `py/`
       plus `MAM-simple/py-examples/mb_cmn/paths.py`. Wave 6's "`py/check_all.py` passed all seven
       repository checks" records a run whose spell check rewrites two tracked files
       (`book-of-job/out/custom-dict-freqs-ordered-by-*.json`), which left no diff only because the
       pages had not changed.
    4. The Sol file (`:59–60`) and the reconciliation (`doc/review-findings-2026-09-07.md:858–859`)
       give the 210 whitespace errors "across 87 `MAM-for-Sefaria/` paths, 111 `MAM-simple/` paths,
       and 12 `gh-pages/MAM-for-Sefaria/` paths": those are finding counts; the distinct files are
       80, 111 and 2.
    5. `9e6e9e17`'s "415 files" under `.novc/review-2026-09-07/` is 416, the extra being the commit
       message file written at commit time.

12. **The tracked vendoring artifacts now record the running clone's line endings, unfixed, Ben's
    decision.** `py/vendoring/compare.py` compares working-tree bytes; after `4afe3ebc` every one
    of the 44 copies is LF while 25 of the 44 sources under `py/` are `w/crlf` in the primary clone
    (all 88 index entries `i/lf`), so the tracked `out/vendoring_compare_out.txt` says `eol-only`
    for exactly those 25 rows and `doc/vendoring-inventory.md` has 8 rows; regenerated from blobs,
    or from any fresh checkout, all 44 read `identical` and the inventory has 4 rows, which is what
    `11fb9c24` produced from the Codex worktree. The record's "8 inventory rows", "zero CRLF
    destinations" and "44 rows" are accurate for this clone, and the artifact will alternate with
    the machine that runs the mega until the 25 sources are rewritten LF or the comparison reads
    blobs. Smaller and of the same mechanism: row 12 (`paths.py`) of the compare report says
    `last_synced 2026-09-07` where the audit derives `2026-09-08`, because `9cf48863` re-vendored
    that copy in the commit that regenerated the report — the born-stale shape `11fb9c24`'s message
    describes — so the next audit or mega run yields a one-line diff. Re-establish:
    `B_09_vendoring.py`; `git ls-files --eol -- py/mb_cmn py/mb_misc py/mb_sefaria py/osis
    MAM-simple/py-examples`.

13. **Code tolerances and unpinned claims, unfixed, all latent today:**
    1. `_fit_type`'s `assert len(fit_types) <= 1` (`py/accgram/post_stress_meteg.py:1518`) aborts
       the survey on a candidate meeting both `TYPE_GUTTURAL` and `TYPE_CLOSED_TSERE` whose next
       word begins with lamed or a guttural without vocal shewa — a shape the survey itself records
       as a corpus fact (`type_2_type_3_overlap`, 154 words), unreachable today only because all 154
       are final-stressed and so never candidates. Introduced with `763b5578`'s per-class `_fit_type`.
    2. `_census_chanted_word_summary` (`:1630–1635`) asserts exactly one post-stress record per MAS
       chanted word and exactly one pre-stress record per MAS-with-MBS word, while its `what`
       (`:1639–1644`) defines the categories over "one or more" marks; a word with two MAS, or two
       MBS and a MAS, aborts the run, so the Methods sentence "No MAS word has more than one meteg
       mark after the stress" is one the survey cannot fail to make true. Introduced by `a5435a41`.
    3. `_hebrew_cell` (`py/author_site/post_stress_meteg.py:1296–1298`) passes every displayed MAM
       form through `_as_mam_would_write_it`, which drops U+05AF, U+05C4, U+05C5 and U+FB1E and folds
       the tilde, while the survey's docstring for that table (`py/accgram/post_stress_meteg.py:2319–2324`)
       says it is used "never to build a displayed form"; a MAM form with a punctum or varika would
       be silently altered on the page. None of the 1,370 reader-facing forms holds one today.
    4. `_fuse_cross_chanted_word_yored`'s closing assertion in `py/accgram/poetic_scanner.py`
       (`a572e20d`, "the pass must never create or remove an oleh-we-yored reading") compares the
       count before and after a loop that only replaces a pair with one token of the same type, so
       it cannot fail; and `pin_claims`' `in_mam == 0` (`:1183–1185, :1212`) cannot fail while the
       oracle reads verse-final stress as finding 1 describes.
    5. The survey docstring says a syllable-count mismatch "is recorded as a MISMATCH and left out of
       every count" (`:37–40`); `_problems` (`:2605–2610`) raises on any mismatch, so no survey with
       one completes and the record exists only in the exception's message. `build_survey`'s
       docstring (`:2872–2874`) states the raise-at-the-end design; the module docstring does not.
    6. The repaired `<scrdfftar>` reader returns an empty string for a lone `spi-pe2` child (3 sites)
       and for an empty target (2 sites) rather than raising; none of the five holds visible text or
       lies in the Aleppo or Cambridge page ranges.
    7. Stated in prose and pinned by nothing: "All 154 occur in Aramaic" (φ6; true today by
       `A_05_aramaic_probe.py`, only the by-book split being pinned); the 2 Chronicles 8:11 page's
       two typed Leningrad forms and its edition attributions ("Breuer (Da-at Miqra), Dotan (BHL)",
       "BHS"), which have no oracle in the repo; and "In every MAS case, the stressed syllable has a
       conjunctive accent", pinned only through counts the survey computes from the same rule.

14. **The plain-"word" exemption's machinery, unfixed, three record defects and one gap:**
    1. The sentence "the main page's second paragraph defines both 'word' and 'atom' before any
       other sentence uses either" is in six places (`py/tests/test_post_stress_meteg_plain_word.py:10–13`,
       `CLAUDE.md`'s section, `py/author_site/post_stress_meteg.py:33–34`, `a3e3f6eb`'s message,
       `doc/PLAN-merge-post-stress-meteg-into-main.md:46–47`, #265) and is off by one sentence and
       one paragraph: `gh-pages/post-stress-meteg.html:60–61` reads "A meteg almost always comes
       before the stressed syllable of its word" before the definition paragraph at lines 72–75,
       the page's third `<p>`. The licence is unaffected; the record misdescribes the page.
    2. `py/tests/test_post_stress_meteg_plain_word.py:61–62` says the names come "from site_data
       rather than by a glob, so a page added there without a decision about its vocabulary fails
       here": a tuple of nine constants cannot see a tenth, and `site_data.py` exposes nine separate
       `POST_STRESS_METEG_*_FNAME` constants and no list, so a tenth page would be hand-listed in
       three places (`site_data.py`, `main_authored.py`'s `_SURVEY_READING_PAGES`, the lint) and
       silently unlinted until it was. A glob would have the property the comment claims.
    3. The lint's docstring, `CLAUDE.md`'s section and #265 all say the merge conflicted in "32
       hunks" of the generator, and the merge dry run reproduces 32; the merge commit's message
       says "36 hunks" (finding 17).
    4. The exemption's basis is recorded in three places in the tree and in the skill nowhere,
       which is #265's subject; and a fourth prose-recorded exception of the same shape was added
       three minutes before #265 was filed — `38a606e2`'s comment (`py/author_site/post_stress_meteg.py:193–197`)
       records Ben's acceptance that this page's ITM and CoS hover glosses name Yeivin and Breuer
       where `almost_errors_html_shared.ITM_TITLE` / `COS_TITLE` (`:154, :158`), shared by three
       accgram pages, do not, against `references/rendered-prose.md`'s "call `itm()` / `cos()`
       rather than building an abbr locally". Raised, not fixed: whether the skill lists it is Ben's.

15. **Prose on the nine pages and in their source, unfixed, listed by rule:**
    1. Romanizations outside `span.romanized`: 15 visible occurrences of "meteg mark(s)" and
       "meteg/merkha marks" on three pages (`post-stress-meteg.html:107–109` ×4,
       `post-stress-meteg-methods.html:85, 88, 91, 93, 95` ×9, `post-stress-meteg-2chr-8-11.html:65`
       ×2), while "meteg" is wrapped everywhere else including `post-stress-meteg-methods.html:238`;
       the main-page sentence is the one `1095f029` reworded to "meteg marks" at Ben's report.
       The `title=` and `<title>` sites cannot carry markup and are exempt.
    2. An announced count left unnumbered across pages: the "fit for MAS" criteria are a three-item
       `<ul>` at `post-stress-meteg.html:280`, and `post-stress-meteg-not-fit.html:65` calls them
       "the three 'fit for MAS' criteria" and heads its columns 1, 2 and 3 by position in that list.
    3. `post-stress-meteg-methods.html:175` mixes "We have not analyzed" and "I think" in one
       parenthetical (Ben's wording, restored by `a9edd4f9`), and has "cant-alef" and "cant-bet"
       undefined for a reader (finding 3).
    4. In the survey module: `py/accgram/post_stress_meteg.py:941` "one strand's chanted verse can
       end at the numbered verse's boundary and the other can run on past it" ("one … the other";
       name the two strands); `:2459` "two annotations MAM does not write" ("write" for "has", a
       negated form the agentive-verb lint does not see). `py/author_site/post_stress_meteg.py:38`
       "The survey's own vocabulary" (`a3e3f6eb`; a survey-versus-pages contrast) and
       `site_data.py:46` "THE PAGES' OWN" (pre-existing; no contrast).
    5. `doc/post-stress-meteg-method.md` says twice in its Fit-for-MAS section that another meteg in
       the first chanted word does not disqualify the candidate, once as "disqualify" and once as
       "exclude"; "tsere-vowelled" there and in the JSON category name against "tsere-voweled" on
       the pages (`fe4e602f`'s standardisation).
    6. `post-stress-meteg-misc.html:128` "the gaʿya-before-paseq pattern described in ITM §325" —
       a source's phenomenon name, borderline under "meteg, not ga'ya", as the last review left it.

16. **Prose-rule hits in the window's record changes, unfixed, all low** (`D_window_prose.py` over
    2,589 added record lines): "hand-authored whitespace" (`doc/PLAN-remediate-review-findings-2026-09-07.md:203`);
    "Seven commits past `c73a2ad3`:" followed by an inline run-on and "converted one to the other"
    (`doc/PLAN-merge-post-stress-meteg-into-main.md:174, :74`); "carries"/"carry" for a file or
    directory having text (`DATA-LICENSES.md:38, :76`, `README.md:138`,
    `py/py_render/rt_mam_suggestion_card.py:352`, `py/repo_util/check_repo_standards.py:270`);
    "hand transcriptions" and "hand corrections" surviving in `DATA-LICENSES.md:16, :63, :88`
    against the script-regenerable / Ben-written vocabulary `b4706759` adopted. No "witness", no
    bare "Simanim", no "the former/latter" was added; every added heading names its subject; every
    disposition row opens with its disposition.

17. **Immutable-message slips, the window's census, recorded only.** (a) `825cef66`'s "36 hunks"
    in `py/author_site/post_stress_meteg.py`: a read-only `git merge-tree --write-tree` of its two
    parents yields 13 conflicted files and 32 conflict hunks in that file (2 in `site_data.py`, 3
    in `main_authored.py`, 1 in the method doc, 1 in the JSON, 17 on the main page, 179 on the
    lacks-MAS page; `CLAUDE.md` auto-merges), the figure the plan, the lint and #265 give; its
    other figures re-derive (983 / 5; 91 changed lines over five pages against `a3e3f6eb`; 309 +
    63 = 372). (b) `fe4e602f` "the census (263,191 / 14,752 / 232)": 262,819 / 14,614 / 232 since
    the merge. (c) `bdcdc5e2` "Restrict fit for MAS to type 2A and 2B": `97a1b46f` replaced 2A/2B
    with 2Af/2Bf. (d) `24f1e4a3` "Add post-stress meteg type 1 page": `3a698b71` consolidated the
    case pages two hours later and no type-1 page exists among the nine. (e) `95c457c2` "a
    paragraph under it paraphrasing what §8 says about each of the three types": the φ5 section at
    HEAD holds two sentences and two tables. (f) `e91d7358`'s "reconcile the current records and
    source-based prose": the prose half was reverted by `1095f029`, `a9edd4f9` and the merge's
    resolution rule; the model half stands. (g) `15ec6f4d` "Close the 2026-09-07 remediation" and
    `975a16c5`'s rows: findings 2, 3, 5 and 8.1. (h) `9e6e9e17` "415 files": 416.

18. **Process and hygiene, recorded for Ben's decisions:**
    1. Trailers: 43 of the 98 commits carry none and 42 are subject-only, all on the
       `post-stress-meteg` branch's line (39 page and prose commits plus the four `Merge branch
       'main' into post-stress-meteg` merges); the Codex trailer is spelled two ways in the window
       (`Co-Authored-By` 18, `Co-authored-by` 16). Census only, the last two reviews having rejected
       rewriting.
    2. The last review's finding 23.2 is unchanged and is Ben's separate track: the Codex worktree is
       live and clean at `38a606e2`, its branch equal to `main`; `origin/post-stress-meteg` stands
       at `9239ac3a`, 150 commits behind; `C:/Users/BenDe/.codex/worktrees/d4d1/MAM-basics-post-stress-meteg`
       is still an empty directory. Findings 23.3 and 23.4, referred to maintenance, are as they
       were: the dated Codex task folder still holds its 20 scripts and three reports (names only
       read), and `MAM-basics/.pytest_cache` exists, rewritten by this review's suite run;
       `~/.codex/plans` now holds four entries (not read).
    3. Cadence: the branch merged `main` four times in the window and `main` took the branch twice,
       the second time by the two-way merge the plan of 18:11 was written for; after `825cef66` the
       two lines are one, and the four later commits (`772545d5` … `38a606e2`) sit on both. The
       global Git section's "merge just before the session is archived" describes a different
       cadence, as the last review also noted. Census only.

## Open ends the window itself declares (not findings)

The fourth stage's Phase 5 (MAM-OSIS) and Phase 6 are unstarted, and MAM-OSIS is still the one
public sibling the mega writes (`doc/PLAN-evacuate-five-MAM-products.md`, `State: live`). No file
under `in/` changed in the window, so the next `fr-wikisource` refresh still brings the eleven
deferred Holman meteg edits and the ten extra phonetic-hbo verses of the last review's finding 23.5,
a known-cause future diff that wants a mega. `doc/PLAN-silluq-before-gaya-template.md` is
unexecuted and is tracked on phonetic-hbo#78 (open); finding 1 bears on it, since the plan and the
survey read the two marks of its one site differently. Issue #265's registry proposal is filed and
undecided; until it is decided, `py/tests/test_post_stress_meteg_plain_word.py` stands as the
exemption's only enforcement. The Codex worktree `C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg`
is live and clean at `38a606e2`, its branch `post-stress-meteg` equal to `main`; `origin/post-stress-meteg`
still stands at `9239ac3a`, 150 commits behind — the housekeeping Ben took on separately on
2026-09-08 (the last review's finding 23.2). The last review's findings 23.3 and 23.4 (the dated
Codex task folder and `.pytest_cache`) were referred to repository maintenance and remain as they
were, `.pytest_cache` rewritten by this review's suite run. The Codex halves of this dual-agent
window have not been run.

## What this review did not check

1. Anything in MAM-private, github-misc beyond the plumbing identity, or hbofonts: the Phonetic MAM
   standard set itself (phonetic-hbo's public pages were the oracle, and they agree with the JSON in
   every category), Yeivin's ITM and Breuer's CoS (every citation on the post-stress-meteg pages was
   checked for form only), and the MAM-private goldens refresh the Wave 3 record names, which is the
   private series' to review.
2. Regeneration of any generator that writes tracked files in place: the mega, the line-break
   checkers, the MAM product generators, `copy-support-files`, the vendoring audit, the survey.
   Regenerated to scratch or recomputed in memory instead: the eleven deploy-root pages, the poetic
   accent-grammar artifacts, the two line-break reports, the letter-small-Job report, the vendoring
   comparison and inventory, the redirect stubs. The Wave 3 and Wave 6 records' two-run mega
   determinism and their MAM-private cleanliness are taken from the record, with the MAM-OSIS
   clone's cleanliness at `697dc98` confirmed on disk.
3. The recorded suite counts of the intermediate commits (978 on the branch at `a3e3f6eb`, 981 at
   Wave 4); only the 983 at HEAD was re-run.
4. The six crops' image content beyond their existence, `src` and captions, and no reading of any
   manuscript or printed edition is adjudicated (finding 1 reports a contradiction, not a reading);
   the Recycle Bin; the Pages runs beyond their metadata; `py/check_all.py`'s spell check, which
   writes two tracked files.
5. Whether the 37 pre-existing non-MAM-normal Hebrew runs on nine window-changed files are
   deliberate illustrations of Unicode-normal order, as the last two reviews also left them.
6. Whether Ben was shown the last review's finding 13.3 before `a9edd4f9`'s sixth revert restored
   the BHS wording: the message records the revert, not the choice, and no transcript was read.

## Inputs for the reconciliation with the Codex review

Anchors for comparison: MAM-basics `8bf586a3..38a606e2`; MAM-simple `9a350be5..376912a7` on
GitHub; the fourteen quiet public repos at the heads `gh_census.txt` records. Each finding above
gives the commit, the file and line as of `38a606e2`, the claim, the measurement, and the command
or `.novc/review-2026-09-08/` script that re-establishes it, so a disagreement can be checked by
hand without re-deriving the whole window. Findings 1, 2, 3, 4, 5.1, 5.6, 6, 7.1 and 17(a) were
re-derived by the main session as well as by their streams (the JSON and the page read for 1, the
193 files re-scanned for 2, the page, the generator and the message read for 3, the runbook and the
rule read for 4, the cells counted for 5.1, the two copies hashed for 5.6, the HTML counted at four
commits for 6, `git ls-files` for 7.1, the merge dry run for 17(a)). The reconciliation section goes
below this one, under `## Reconciliation with the Codex review`, per `doc/dual-agent-review.md`.

## Reconciliation with the Codex review

Completed 2026-09-09 under Design A. The companion is
[`codex-review-findings-2026-09-08.md`](codex-review-findings-2026-09-08.md).
The review ranges remain MAM-basics `8bf586a3..38a606e2` and MAM-simple
`9a350be5..376912a7`. The comparison also recognizes the September 9 decisions recorded at
`3b0225e0` and `becc6f00`. Claude's original findings above remain unchanged.

The commit/trailer/path census reproduces, MAM-simple's sole change is its README date,
and all fourteen quiet public repositories have no commits in the bounded review interval.
The suite at the Codex review checkout's starting commit `becc6f00` passed with 983 tests,
5 skips and 65 subtests; the tracked tree was clean before and after. This run does not
reconstruct any historical run's output.

"Confirmed" below applies only to the named observations. It does not approve a remedy.
"Rejected" and "qualified" describe Codex's assessment of a claim, without rewriting the
claim above. An unfixed finding is not marked fixed because the comparison is complete.

| Claude finding | Codex comparison | Disposition after comparison |
|---|---|---|
| 1 | The historical explanation/classification discrepancy is confirmed. The September 9 explanation defines the deliberate interpretation; the classifier did not change. | Settled by Ben on September 9. Preserve the explanation and classification. The full 597-form stress-alignment claim was not repeated. |
| 2 | Confirmed: all 210 whitespace findings remain in 193 files; none is among `4afe3ebc`'s 390 changed files. A clean-tree diff check does not establish their repair. | Unfixed. The earlier Sol-1 fixed disposition remains unsupported. |
| 3 | The BHS-labelled form's code provenance is confirmed. Ben's direct BHS inspection is now recorded, and the edition objection was withdrawn. Other reverted wording reflects deliberate decisions. | The BHS and edition questions are settled. The older broad fixed rows still need dated descriptions of the retained and reversed work; those corrections must not reinstate the rejected prose. |
| 4 | Confirmed: the current maintenance runbook prescribes exclusions and gist clones that its cited policy expressly replaces with the workspace roster. | Unfixed current instruction contradiction. |
| 5 | Partly confirmed: the 49 plus 1 missing RTL declarations, current sparse-checkout guidance, commit attribution, moved-document referent, argparse-help description and inventory's outside-repo wording reproduce. Later filesystem state does not disprove an earlier dated observation. The named skill copies are identical on September 9. | Confirmed current gaps remain unfixed. Finding 5.6 is resolved. Historical observations and style judgments do not justify wholesale rewriting; the broad claim that all remaining rows hold was not independently repeated. |
| 6 | Confirmed: 11 deploy-root pages, nine MAS pages, and seven stale 10/8 descriptions. The authored-anchor count is 35. The test comment dates its 34 count to an earlier state, and its floor of 25 still functions. | Current count descriptions remain unfixed. Qualify the claim that the historical 34 count itself is false. |
| 7 | Confirmed: 13 plans, 11 State lines; the newly written "all ten" was already wrong when 11 plans existed. | State omissions and current record errors remain unfixed. Renaming or deleting plans is not authorized by this review. Exact 381/440 occurrence counts were not repeated. |
| 8 | Confirmed independently: public Phonetic MAM has 368 ordinary qamats rows and 370 alternate-reading chanted words; the dual-cantillation rows add two to each total, giving 370/372. The difference is scope. The implementation checks structural conditions rather than a retraction analysis. | The source-movement explanation remains a record error. Source-based retraction is not adjudicated; wording requires Ben's decision. |
| 9 | Confirmed: the retained-test claim is false, and the named provenance details are absent. The Aleppo observation concerns presentation. | Record/provenance gaps remain unfixed. No license violation was established; no manuscript reading or added reader-facing explanation is prescribed. |
| 10 | Confirmed procedure lag. Codex additionally found the false premise that Codex cannot load the Hebrew prose skill, despite the procedure's account that it already did. | Unfixed record error. The suffix and State conventions remain policy questions, not grounds to invalidate completed reviews. |
| 11 | Confirmed unchecked completed-wave boxes, 26-versus-25 path wording and findings-versus-files counts. Reject the asserted explanation of Wave 4's missing subtest output line: different runs do not establish its cause. | Current record imprecision remains unfixed. Preserve the historical observation unless evidence from that run supports a correction. The 415/416 scratch count and spell-check side effect were not independently repeated. |
| 12 | Confirmed: all 44 pinned source/copy pairs are identical LF, while the committed working-tree audit has 25 eol-only rows. The synchronization date is one commit behind. | The date discrepancy remains unfixed. Comparing working-tree bytes is intentional; changing that purpose or checkout handling needs a design decision. No damaged copy was found. |
| 13 | Mixed. The guards stop on unsupported overlap/multiplicity; the rendering/comment mismatch is latent; the fusion invariant follows from the loop; mismatch documentation omits the fatal-build consequence. Reject the claim that multiplicity guards manufacture agreement and the claim that conjunctive stress is unpinned: adverse probes raise. `_problems` returns the problems; the build raises. | No current MAS output error was established. Keep the working guards. The verified documentation limits remain; 13.6 and the language/edition parts of 13.7 were not independently checked. See Codex C1. |
| 14 | Mixed. The definition is the second expository paragraph; counting the control makes it the third HTML paragraph. The before-any-earlier-use claim is false. The enumerated lint cannot discover an added page. The context-based permission quoted as skill text is in repository instructions, not the loaded skill's opening. The 32-hunk figure reproduces. | Record/lint-coverage observations remain unfixed. The plain-word and author-gloss exceptions remain valid; registry design is Ben's decision. |
| 15 | Independently confirmed only 15.1's formatting count: 15 unwrapped mark names, split 4/9/2 across the named pages. | Formatting observation retained without applying edits. Findings 15.2–15.6 were not independently audited; Ben's restored wording and accepted exceptions remain in force. |
| 16 | Reject the generalized ban on files having text with the verb carry and the blanket ban on hand transcriptions/corrections. The cited rule and `b4706759` do not establish those extensions. Particular enumeration/referent observations remain style observations. | Reject the blanket cleanup premise. No prose sweep is authorized. See Codex C3. |
| 17 | The 32-versus-36 merge-hunk discrepancy reproduces. Reject 17(b)–(e): the stated census, type names, added page and paragraph all exist in their respective original commits. Later reversals describe history. Unfinished work supports qualifying completion claims independently of those reversals. | Record 17(a) without rewriting history. Reject the error classification for 17(b)–(e); preserve accurate historical messages. The 416 scratch count was not independently established. See Codex C2. |
| 18 | Trailer and merge-topology census confirmed. The physical housekeeping inventory, historical remote-branch distance and reasons for integration timing were not independently audited. | Census only; housekeeping remains Ben's separate track. No branch, worktree or folder was retired. |

The additional process finding is that the remediation plan at `47edbee6` already gives broad
MAS editorial instructions without identifying concrete wording approved by Ben. The public
revert messages establish that those instructions resulted in unrequested rewrites. A later
remediation checklist must distinguish verified technical defects from proposed changes to
MAS terminology, organization, scholarly interpretation and source attribution. Present
unsettled concrete wording changes for Ben's approval; follow decisions already given.

The Codex review changed only its companion findings file and this appended comparison.
No remediation disposition was newly claimed as fixed. Private-source research, manuscript
adjudication, the full mega/survey regeneration, historical test reconstruction, and the
complete set of Claude's negative or soundness claims remain outside the independently
checked scope. The compaction investigation stays outside these public records.

## Dispositions after remediation

Wave 1A checkpoint, 2026-09-09, recorded by Codex. The original findings and reconciliation
above remain historical records. Ben's approved work is being completed in smaller tasks;
this section records only completed work and does not declare Wave 1 complete.

| Date | Finding or decision | Disposition and verification |
|---|---|---|
| 2026-09-09 | 14.4 / D2; fresh deployment check for 5.6 | Applied Ben's exact approved sentence to the live Claude skill, then copied the entire skill directory to the tracked review-worktree copy and live Codex copy. Both required whole-directory Git comparisons are empty; an independent SHA-256 inventory confirms identical bytes for all five files in each home. Only the approved opening sentence changed. The contextual permission and explicit MAS-page exception remain intact. The review-exchange correction about where permission already existed remains for Wave 1D. |
| 2026-09-09 | Remaining Wave 1, Waves 2-4, and the separate editorial phase | Pending under the approved remediation plan. D2 does not complete the dated historical corrections, crop-provenance inventory, accepted-corrections section, technical remedies, or editorial work. |

Wave 1B checkpoint, 2026-09-09, recorded by Codex under Ben's Step-5 approval. The rows below
update the completed current-documentation items only. Wave 1C's historical corrections and
Wave 1D's complete accepted-corrections section and disposition reconciliation remain pending.

| Date | Finding or decision | Disposition and verification |
|---|---|---|
| 2026-09-09 | 4 | Added the exact approved dated correction immediately after the maintenance runbook's old scope paragraph, linking the workspace roster and its setup policy. The current roster has six folders after `63ac5b84` removed `github-misc`; no roster or policy changed, and no maintenance ran. |
| 2026-09-09 | 5.3 / N1 | Applied the exact named-referent correction in `cam1753/doc/reading-mam-simple.md`: codex-index-cam1753's copy was deleted. The historical equivalence figures and comparison rule are unchanged. |
| 2026-09-09 | 5.4a / N2 | Changed the test docstring to say the argparse help formerly said the quoted text. The current help says `Stored release or MAM-basics revision`; the test's behavior is unchanged. Finding 5.4b remains assigned to Wave 4. |
| 2026-09-09 | 5.5 / N4-N6 | Applied only the approved current fragments in `doc/dual-agent-review.md`, `CLAUDE.md`, and the `in/scan-pages/` license row. The dated programme wording is preserved. No procedure redesign or license grant changed. |
| 2026-09-09 | 6.1-6.5; 6.8 / D8 and N9 | Updated current descriptions to the measured eleven deploy-root pages and nine MAS pages. The real `_authored_anchors()` walker returns 35; the comment now says 35 after the 2026-09-08 additions, with floor 25 and test behavior preserved. The historical 34 was true when written, as turn 5 confirms. Findings 6.6-6.7 remain for Wave 1C. |
| 2026-09-09 | 9.1 | Removed the nonexistent retained source-hygiene test from the MAM-with-doc inventory. `git ls-files MAM-with-doc` gives `.gitattributes`, `.gitignore`, `LICENSE.md`, and `README.md`; license terms are unchanged. |
| 2026-09-09 | 9.2 / P2 | Added `doc/post-stress-meteg-image-provenance.md` and linked it from the `gh-pages/img/` row. The inventory names exactly the six tracked crops and records unrecorded photograph sources and rights holders. Only the already-captioned Leningrad 1 Samuel 17:5 crop has F159A, column 3, line 8. The missing inventory is supplied; source and rights-holder identification remains deferred. All crop bytes and no-grant terms are unchanged. |
| 2026-09-09 | 15.4 / N7, Misc-title sentence only | Applied `THE MISC TITLES MATCH THE PAGES' TITLES.` in `py/author_site/site_data.py`. The remaining survey/module editorial items are deferred to the separate editorial phase. |
| 2026-09-09 | 16 / D6, Aleppo attribution only | Attributed the `aleppo/aleppo-wiki/` hand corrections to Ben Denckla exactly as approved. The withdrawn carry/hand-transcription sites and unrelated wording are unchanged; N8 and the accepted-corrections reconciliation remain assigned to later Wave 1 tasks. |

Wave 1C1 checkpoint, 2026-09-09, recorded by Codex under Ben's Step-5 approval. These
rows cover only the evacuation records and September 4 review. Wave 1 remains incomplete.

| Date | Finding or decision | Disposition and verification |
|---|---|---|
| 2026-09-09 | 5.1a / D4, three-repos record and September 4 review | Added dated notes superseding the claim that the suite no longer prints a subtest line, while preserving Wave 4's command-unrecorded/cause-unknown limit and citing Wave 6's recorded 65 subtests. The September 4 review now distinguishes its historical absent-directory observation from the September 8 recorded state, enumerates the six branches and tips from the retained September 7 deletion-output record, and records that `4195440e` had already removed the primary-clone constant. Original records remain intact; no current branch census or cleanup was performed. Finding 11.1's separate September 7 record and the accepted-corrections append remain for later Wave 1 work. |
| 2026-09-09 | 5.2 | Added dated notes linking the landed MAM-simple and MAM-parsed sparse-checkout instructions, attributing workspace/visibility removal to `19df42f3`, and citing `9cf48863`'s recorded MAM-for-Sefaria retirement. The historical MAM-with-doc host list now has a dated note naming `.gitattributes` and `.gitignore`, verified in the fixed `904c9fa` public Git tree. No evacuation, filesystem safety audit, or retirement was repeated. |

Wave 1C2 checkpoint, 2026-09-09, recorded by Codex under Ben's Step-5 approval.
These rows cover only the assigned September 7 historical records; Wave 1 is incomplete.

| Date | Finding or decision | Disposition and verification |
|---|---|---|
| 2026-09-09 | 2, historical fixed claim only | Corrected the September 7 Sol-1 disposition and Wave 3 record by dated notes. The bounded current-file scan reproduces 210 findings in 193 files, with no overlap against the 390 files changed by `4afe3ebc`. All whitespace defects remain assigned to Wave 2; no output was repaired. |
| 2026-09-09 | 3 | Added dated status notes to the September 7 Wave 2 result and the existing rows 13/21 clarification. Retained model fixes are distinguished from `1095f029`/`a9edd4f9`'s reversals, `38a606e2`'s accepted local ITM/CoS glosses, and `3b0225e0`'s settled BHS/edition questions. No prose was reinstated. |
| 2026-09-09 | 8.1 | Added dated scope corrections to the September 7 review, remediation plan, and Sol review. Fixed public Phonetic MAM HTML at `7322b665` reproduces 368 ordinary rows / 370 duplicated chanted words, plus two dual-cantillation rows giving 370/372. Source movement did not cause the difference; no survey changed. |
| 2026-09-09 | 11.1 / D4, September 7 record | Added the command-unrecorded/cause-unknown note beside Wave 4's preserved output observation. Wave 6 recorded 65 subtests with the same 981 passing-test count. The separate three-repos correction completed in Wave 1C1 is preserved; no historical invocation was reconstructed. |
| 2026-09-09 | 11.2 | Added dated status notes naming `c76239a5` and `e91d7358` beside their original unchecked checklists. Original boxes remain; the notes distinguish implemented work, failed record correction, and deliberately reversed editorial work. |
| 2026-09-09 | 11.3 | Corrected Wave 6's count to 25 formatted source files plus the copied Python file in `9cf48863`; the source and copied `paths.py` blobs are identical there. Code inspection confirms that the spell-check call writes both tracked custom-dictionary frequency reports. The recorded successful run remains; the spell checker was not rerun. |
| 2026-09-09 | 11.4 | Added dated finding-versus-file corrections in the Sol review and September 7 reconciliation: 87/111/12 findings correspond to 80/111/2 distinct files, totaling 210 findings in 193 files. The bounded scan preserves the exact offending set and confirms no overlap between blank-final-line and trailing-space files. |
| 2026-09-09 | 17f–17g, assigned completion qualifications only | Qualified the September 7 completion statements by the continuing Sol-1 defects and incorrect scope explanation. Later deliberate prose reversals do not falsify `e91d7358`'s original message. Other completion/disposition reconciliation remains with later Wave 1 work. |

Wave 1C3 checkpoint, 2026-09-09, recorded by Codex under Ben's Step-5 approval.
These rows cover only the assigned MAS-plan and standards historical corrections.
Wave 1D retains the complete accepted-corrections append and disposition reconciliation.

| Date | Finding or decision | Disposition and verification |
|---|---|---|
| 2026-09-09 | 1, older-plan overclaim | Added a dated note identifying the zero post-silluq count as the research's chosen interpretation, settled by Ben in `3b0225e0`. The classifier, census, and approved pages are unchanged; no silluq-template implementation ran. |
| 2026-09-09 | 6.6-6.7 | Added dated notes beside both old ten/eight descriptions. The Git trees reproduce ten deploy-root/eight MAS pages at `15ec6f4d`, eleven/nine at `825cef66`, and eleven/nine at `1b86afa8`. The ninth MAS page reached main with that merge; earlier execution counts remain intact. |
| 2026-09-09 | 7.1 | Added the approved executed State line to the merge plan. Retained `ad44dba7`'s already-landed census correction. All eight MAS HTML blobs at `15ec6f4d` reproduce 440 occurrences of `chanted` on 381 lines; the dated note distinguishes occurrence counting from `grep -c`. |
| 2026-09-09 | 7.2 | Recorded the already-landed State and later dated notes from `7f0e4bdd`, `527011b7`, and `2de7a969`. Attributed the original contracts to the September 8 plan `772545d5` without inventing approval of every contract. Added a dated baseline correction distinguishing the September 6 result from later recorded runs. Filename and product contracts are retained; the plan remains unexecuted by this remediation. |
| 2026-09-09 | 7, standards docstring census / D10 pointer | Replaced only the false current plan census with a dated correction: `9cf48863` had eleven plans with State lines and omitted the September 7 remediation plan from its claim of ten; `38a606e2` had thirteen plans with eleven State lines. Preserved the State format rule and added the procedure pointer for D10's review naming/State rules. No standards behavior or gate changed. |
| 2026-09-09 | 16 / N8 | Added the exact approved numbered commit list and direction-neutral quotation-mark note, preserving the original records. The fixed `c73a2ad3..a3e3f6eb` non-merge log reproduces the seven entries. The blanket cleanup premise remains rejected; no withdrawn stylistic site was swept. D6's separate attribution is preserved. |
| 2026-09-09 | 14.3 / 17a | Recorded that the merge plan already gives 32 author-module hunks and 13 conflicted files, independently established in the review and reconciliation. The merge message's 36-hunk claim is retained as an immutable historical error; no message amendment, issue communication, or historical checkout merge occurred. |
