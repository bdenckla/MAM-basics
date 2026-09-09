# PLAN — remediate the 2026-09-09 review of the tracked agent-instruction files

State: live. Proposed 2026-09-09, nothing acted on; Ben's decision, 2026-09-09, was to record
the review as a plan rather than act on it in the reviewing session, which he called overwhelming.

**The review this plan remediates was a ONE-OFF, not an instalment of the periodic
`doc/review-findings-<date>.md` series** — Ben's decision, 2026-09-09. That is why this file is
named as a plan and carries no `review-findings` date, and why no `doc/review-findings-2026-09-09.md`
exists or should be written. §7 answers what the one-off leaves open.

Moved here from `github-misc/doc/` on 2026-09-09 with the repointing pass §0 describes, when the
twelve files it reviews became canonical in MAM-basics. The move is argued in
`doc/assessment-two-stranded-artifacts-2026-09-09.md` §5, whose privacy screen found nothing
requiring redaction.

## 0. What produced this plan, and what its figures were measured against

On 2026-09-09 a Claude session reviewed, as a single pass, every tracked agent-instruction file
then in `C:/Users/BenDe/GitRepos/github-misc`: `dot-claude/CLAUDE.md`, `dot-Codex/AGENTS.md`,
`dot-claude/README.md`, `dot-Codex/README.md`, the five files of `dot-claude/skills/hebrew-prose/`,
`dot-claude/skills/prune-claude-state/SKILL.md`, `dot-Codex/skills/prune-claude-state/SKILL.md` and
`dot-Codex/skills/worktree-forest/SKILL.md` — 326 KB, all read in full. **Those are the names the
review read them under. All twelve are tracked in `C:/Users/BenDe/GitRepos/MAM-basics` now, at the
same paths but for two renames — `dot-claude/user-wide-CLAUDE.md` and
`dot-Codex/user-wide-AGENTS.md`, renamed so that a nested `CLAUDE.md` does not load itself inside
MAM-basics — and every work item below names the MAM-basics path.** The review exists because
the 2026-09-09 session before it was asked to fix four stale statements in
`references/verifying.md` and found every further defect reactively, one adjacent passage at a
time, over nine commits (`9ea78d2` … `810ffd0`); Ben asked whether one thorough pass would serve
better. It did: this plan records 13 mechanical fixes and 16 decisions, none of which that session
found.

The five defect classes the nine commits defined, used as the headings of §2 and §3 below:

1. A figure restated in two or more files, stale in one of them.
2. A rule stated only in a file nothing loads.
3. Two documents prescribing opposite procedures.
4. A statement true when written and since overtaken.
5. A procedure that names a step without giving its command.

Measured against: `github-misc` at `810ffd0` (the worktree
`C:/Users/BenDe/GitRepos/github-misc/.claude/worktrees/elastic-montalcini-f28420`, whose branch
`claude/elastic-montalcini-f28420`, the primary clone's `main` and `origin/main` all stood at that
commit, both trees clean); `MAM-basics` at `d8a0fdae` (2026-09-09 11:11, with a second session live
there — see §1); `MAM-private` at `267a3e25` (2026-09-08), whose `masorah-books/` tree the skill
cites as its authority. Disk and GitHub were read between 10:40 and 11:15 local on 2026-09-09.
Re-measure rather than trust any figure below; a mismatch is a finding.

**Every `github-misc <sha>` this plan cites is right as written and must NOT be repointed.** The
twelve files were copied into MAM-basics rather than filtered in with their commits, so all their
history before 2026-09-09 is github-misc's — the rule `dot-claude/user-wide-CLAUDE.md` states for
itself. `C:/Users/BenDe/GitRepos/github-misc` was retired on 2026-09-09, so that history is now
reachable only from the private remote:

    gh api repos/bdenckla/github-misc/commits/<sha> --jq .commit.message
    git clone https://github.com/bdenckla/github-misc.git C:/tmp/github-misc

M1, M3, M4, M11, D3 and §4 item 1 each rest on that history, and §6's `substitution_proof.py`
cannot run without a clone of it.

## 1. Preconditions and setup for the session that executes this plan

1. **Which checkout.** Prefer the primary clone, `C:/Users/BenDe/GitRepos/MAM-basics` on `main`:
   the deploy commands and drift checks in `dot-claude/README.md` §"Shared-skill deployment to
   Claude and Codex" name that path, and the live files edited here are machine-global. If the
   session is given a worktree instead, substitute the worktree path in those commands, and
   integrate immediately after the last commit rather than at archival — `~/.claude/CLAUDE.md`'s
   Git section allows early integration "when a concrete need requires the primary checkout to
   contain the work", and the need here is that the live files must not sit ahead of the primary
   clone's tracked copies, which every drift check on this machine compares against.
2. **Live-first order, for every file that has a live copy.** Edit `~/.claude/CLAUDE.md`,
   `~/.codex/AGENTS.md` and `~/.claude/skills/hebrew-prose/`, then copy back to the tracked copy
   and commit. For the skill, run the four steps of `dot-claude/README.md` §"Shared-skill
   deployment to Claude and Codex", including the copy to `~/.agents/skills/hebrew-prose/` and
   **both** `git diff --no-index` comparisons, before committing. `dot-claude/README.md` and
   `dot-Codex/README.md` have no live copy and are edited in place.
3. **Load the `hebrew-prose` skill before editing its five files.** Its `when_to_use` covers any
   file whose text discusses accents, which its own files do. Nothing in this plan changes an
   accentuation rule; the edits are paths, issue prefixes, dates and pointers.
4. **The venv, black and the suite — this changed with the move.** github-misc tracked no Python
   and had no `.venv`, so the plan owed neither a black run nor a test run. MAM-basics owes both.
   The work items below edit Markdown only, so black has nothing to format unless an item grows a
   Python edit — if one does, `.venv/Scripts/python.exe -m black <files>`. The suite is not
   optional: run `.venv/Scripts/python.exe py/main_test.py` from
   `C:/Users/BenDe/GitRepos/MAM-basics`, never from `py/`, before the first edit and after the
   last. The baseline on 2026-09-09 was **983 passed, 5 skipped, 65 subtests passed**, about 84
   seconds. In a worktree, set `$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"` first and name the
   primary clone's venv by absolute path. `py/tests/test_prose_conventions.py` reads the skill, so
   an edit there can turn it red; and if the branch that
   `doc/assessment-two-stranded-artifacts-2026-09-09.md` §3 recommends merging has landed,
   `py/tests/test_prose_mark_order.py` fails on any tracked `.md` whose Hebrew is not in MAM-normal
   mark order — which is a live hazard here, because the Write and Edit tools silently produce the
   other order. Re-measurements against MAM-basics run on that same venv, from that repo's root.
5. **Another session may be live.** On 2026-09-09 the MAM-basics primary clone held untracked
   `doc/user-level-config-in-cloud-sessions.md` and `.claude/` from a session then running; its
   name suggests it concerns these same instruction files. Before editing, check for a newer
   MAM-basics commit touching `dot-claude/` or `dot-Codex/` than the one this plan is read at, and
   read it.
6. **Baseline: no drift anywhere.** At `810ffd0` all twelve files hashed identically at every home
   — the five skill files at the canonical, `~/.claude/skills/` and `~/.agents/skills/` homes, the
   two instruction files and the three single-home skills against their live copies. Re-establish
   with `python C:/Users/BenDe/GitRepos/MAM-basics/.novc/review-2026-09-09/drift_check.py`
   (§6), and start from a clean result.
7. **Cite issues with their tracker.** `MAM-basics/CLAUDE.md` §"Five issue trackers: a bare
   `#NN` here means MAM-basics" is the rule every edit below follows; M12 is the sweep for it.

## 2. Mechanical fixes — 13 items, ready on Ben's go-ahead

Each item: the disposition, the file and a searchable anchor (line numbers are as of `810ffd0`
and will drift), the evidence with its command, and the replacement. "Both instruction files"
means `dot-claude/user-wide-CLAUDE.md` and `dot-Codex/user-wide-AGENTS.md`, which carry the same
passage. **A bare `CLAUDE.md` or `AGENTS.md` below names the LIVE copy, `~/.claude/CLAUDE.md` or
`~/.codex/AGENTS.md`, which keep those names; the tracked copies are the two `user-wide-` files.**
Where a bare name means some other file — MAM-basics' own project `CLAUDE.md`, mgketer's, or a
literal filename inside a quoted command result — the sentence says so.

**M1 — Class 4. `CLAUDE.md`'s two Gist sentences are stale; replace the half-bullet.**
§"all-repos.code-workspace is the roster", last bullet, anchor "A gist's clone URL is not derivable
from its name". It says "`Gist-ArtScroll` is in the roster and its URL is in `repo_selection.py`'s
`_NON_REPO_WORKSPACE_FOLDERS`; `Gist-Hebrew-World` is in no workspace file … its URL is recorded in
`gitrepos_setup_rule`'s `gists` key". Overtaken the day it was written: the roster's `folders`
array has 7 entries and no gist; clause 3 of `gitrepos_setup_rule` says "THAT MAP IS EMPTY as of
2026-08-31, Gist-ArtScroll having been its only entry"; the `gists` key holds both URLs;
`MAM-basics/py/repo_util/repo_selection.py` line 46 reads
`_NON_REPO_WORKSPACE_FOLDERS: dict[str, tuple[str, str]] = {}`. Commands:
`python .novc/review-2026-09-09/show_policy.py`;
`cat C:/Users/BenDe/GitRepos/MAM-basics/all-repos.code-workspace`. Replacement for everything after
"only if its URL was written down.": "Neither gist is in any workspace file, so under clause 1
neither is cloned; both URLs are in `gitrepos_setup_rule`'s `gists` key, which since 2026-08-31
has been the only record on the machine that either gist exists. `repo_selection.py`'s
`_NON_REPO_WORKSPACE_FOLDERS` map is kept empty for a future folder whose URL is not guessable;
`Gist-ArtScroll` was its only entry until that gist left the roster on 2026-08-31, its content
evacuated into MAM-basics as `py/author_misc/review_of_artscroll_transliterated_linear_siddur.py`.
This bullet said Gist-ArtScroll was in the roster and its URL in the map until 2026-09-09; both
had been true for a few hours of 2026-08-31."

**M2 — Class 4. Five wlc-utils-era paths in both instruction files; repoint to MAM-basics.** All
five files have been `MAM-basics/py/…` since 2026-08-01, and `MAM-basics/CLAUDE.md` §"wlc-utils
belongs on no machine" governs. Command:
`python .novc/review-2026-09-09/resolve_paths.py`, the `wlc-utils/…` rows of `paths_report.txt`.

1. Tests §: "`wlc-utils/py/tests/test_transliterations.py` (issue #26) still fires" →
   "`MAM-basics/py/tests/test_transliterations.py` (wlc-utils#26; in MAM-basics since
   2026-08-01) still fires".
2. §"No `sys.path` surgery": "`wlc-utils`' `py/main_accgram.py` is the worked example" →
   "MAM-basics' `py/main_accgram.py` (wlc-utils' until 2026-08-01) is the worked example".
3. Paseq §: "`wlc-utils/py/accgram` (the accent-grammar parser) already models" → "MAM-basics'
   `py/accgram` (the accent-grammar parser, wlc-utils' until 2026-08-01) already models".
4. Silluq §: "**wlc-utils** `py/accgram/meteg_silluq_context.py`" → "**MAM-basics**
   `py/accgram/meteg_silluq_context.py` (in MAM-basics since 2026-08-01)".
5. Maqaf §: "wlc-utils `py/accgram/printed_decalogue_strands.py`" → "MAM-basics
   `py/accgram/printed_decalogue_strands.py`". (The bullet's closing "Issue #76." is M12's.)

**M3 — Classes 3 and 4. `AGENTS.md` §"What belongs under GitRepos is defined in
repo_maintenance_policy.json" prescribes the enumerate-GitHub rule the policy forbids; replace the
whole section.** Lines 116–156 say "enumerate `gh repo list bdenckla` keeping non-archived
non-forks, subtract `repos_to_keep_absent`, subtract `frozen_repos`, then add the gists". Clause 4
of `gitrepos_setup_rule`: "CLONE NOTHING ELSE. There is no exclusion list to consult and no GitHub
enumeration to filter". `CLAUDE.md` §"all-repos.code-workspace is the roster: clone only what it
lists" (`dcffa4d`, 2026-08-31) is the current rule. Cause: `AGENTS.md` was created on 2026-09-01
(`f8898a9`) from a `CLAUDE.md` snapshot older than `dcffa4d` — the substituted snapshot differs
from `AGENTS.md` at creation in exactly this section and the ones in M4 and D3
(`python .novc/review-2026-09-09/substitution_proof.py` → `substitution_diff.txt`). Replacement:
transplant `CLAUDE.md`'s section verbatim, with M1 applied; it contains no Claude-specific text.

**M4 — Class 4. Eleven `claude`→`Codex` substitutions in `AGENTS.md` are false statements;
restore the true names.** `AGENTS.md` is a mechanical substitution of `CLAUDE.md`
(`substitution_proof.py`: 115 residual lines of 998 at `f8898a9`, all in the sections M3 and D3
name), and these eleven changed a fact:

1. Line 385–386 "**Codex** Code's own tool descriptions push the other way: the Bash tool
   says…" — the 2026-08-31 case was a Claude session and those are Claude Code's tools. Restore
   "Claude Code's own tool descriptions"; whether Codex's harness exerts the same pull is D2.
2. Lines 401 and 413 "`mgketer/AGENTS.md`" → "`mgketer/CLAUDE.md`", adding `CLAUDE.md`'s clause
   "That file is `MAM-private/mgketer/CLAUDE.md` now, having moved there with mgketer's content
   on 2026-08-09" (the file exists; `ls C:/Users/BenDe/GitRepos/MAM-private/mgketer/*.md`).
3. Line 452 "`ls "$d/.Codex" 2>/dev/null | tr …`" → `.claude`; the 2026-08-24 pipeline was over
   `.claude` directories.
4. Line 509 "**14 sit in commits carrying a `Co-Authored-By: Codex`/Copilot trailer**" →
   `Co-Authored-By: Claude`. The 2026-07-30 blame crawl predates Codex on this machine
   (`~/.codex/installation_id` is dated 2026-08-31).
5. Lines 611–612 "mgketer's own `AGENTS.md` wins:" → `CLAUDE.md`'s wording: "mgketer's own
   `CLAUDE.md` wins — that file is `MAM-private/mgketer/CLAUDE.md`, … and the rule deferred to is
   its §"UTF-8 Everywhere" rule 6:" (verified present: `python .novc/review-2026-09-09/final_checks.py`).
6. Lines 683–686 "its `AGENTS.md` is deliberately small … `Codex-disabled.md`" → "its `CLAUDE.md`
   is deliberately small … `CLAUDE-disabled.md`" — both bare names here are **MAM-basics' own
   project instruction file**, not the user-level one, the passage being about MAM-basics
   (`ls C:/Users/BenDe/GitRepos/MAM-basics/AGENTS.md` fails; only that repository's `CLAUDE.md`
   exists). Also transplant `CLAUDE.md`'s 2026-08-31 mgketer clause from
   the same bullet ("**mgketer's is not at `bdenckla/mgketer` any more** … archived on
   2026-08-27"), which `ae29b3d` added to `CLAUDE.md` after the snapshot was taken.
7. Lines 724 and 1000 "`MAM-basics/AGENTS.md`" and "MAM-basics' own `AGENTS.md`" →
   "`MAM-basics/CLAUDE.md`" and "MAM-basics' own `CLAUDE.md`" — again that repository's project
   file, which is why the replacement keeps the bare name rather than taking `user-wide-`.
8. Line 797, Ben's quotation: "a few remarks in AGENTS.md is no match for your original
   training" → "CLAUDE.md", which is what he wrote on 2026-08-25. **This one is a verbatim
   quotation, so the replacement is the bare word `CLAUDE.md` and nothing else** — writing
   `user-wide-CLAUDE.md` here would put into Ben's mouth a filename that did not exist until
   2026-09-09.
9. Line 248 "A transcript under `~/.Codex/projects/<repo-slug>/` names in its first line the
   phase" — Codex has no `projects/` (`ls C:/Users/BenDe/.codex`: `sessions/`,
   `session_index.jsonl`). Restore the measured statement as Claude's — "A Claude transcript
   under `~/.claude/projects/<repo-slug>/` names in its first line…" — and add "Codex's session
   transcripts are under `~/.codex/sessions/`, indexed by `~/.codex/session_index.jsonl`"; whether
   a Codex transcript's first line names its task was not verified and should not be asserted.
10. Line 1051 "`.Codex/launch.json`" → "`.claude/launch.json`" (a Claude Code artifact).
11. Line 15 "what is deliberately *not* tracked (`settings*.json`, `projects/`)" →
    "(`auth.json`, `config.toml`, `settings*.json`, session transcripts)", which is what
    `dot-Codex/README.md`'s closing paragraph actually lists.

Two substitutions are true and stay: line 217 "A commit carries `Co-Authored-By: Codex`" (113 such
trailers in MAM-basics' last 400 commits:
`git -C C:/Users/BenDe/GitRepos/MAM-basics log -400 --format=%b`, then count the
`Co-Authored-By` lines) and line 375 "`.Codex/worktrees/<sibling>`", which is where a Codex
worktree's `repo_root().parent` lands.

**M5 — Class 4. `AGENTS.md` cites UXLC-utils for `clc-design.md`; repoint, and align the paseq
section's repo list with `CLAUDE.md`.** Lines 892 and 929 "**UXLC-utils** `doc/clc-design.md`" →
"**MAM-basics** `uxlc/doc/clc-design.md`" (UXLC-utils evacuated 2026-09-03; §2 at line 34 and §7.16
at line 863 of that file verified). Line 898 "(vendored into UXLC-utils and wlc-utils)" →
"(formerly vendored into UXLC-utils and wlc-utils)". Lines 860–861 "Across my Hebrew-text repos
(UXLC-utils, wlc-utils, MAM-basics, MAM-simple, al-hatorah, book-of-job, TMC, ...)" → `CLAUDE.md`'s
"Across MAM-basics and my other Hebrew-text repos (MAM-simple, al-hatorah, TMC, ...)". Command:
`python .novc/review-2026-09-09/section_compare.py` → `section_compare.txt`, the two Terminology
hunks.

**M6 — Class 4. The skill says the CoS diacritics pass is "still outstanding"; it closed
2026-08-04.** `masorah-books#16` is CLOSED, closed 2026-08-04
(`gh issue view 16 --repo bdenckla/masorah-books --json state,closedAt`); the README's
§"CoS — 57 files, chapter-scoped numbering" says "**The diacritics repair pass is done**, as
masorah-books #16". `#15` (page anchors) is still OPEN.

1. `SKILL.md`, anchor "Page anchors and a diacritics repair pass are still outstanding, one issue
   each in `masorah-books` — #15 for the page anchors, #16 for the diacritics." → "The page
   anchors are still outstanding, `masorah-books` #15; the diacritics repair pass is done,
   `masorah-books` #16 (closed 2026-08-04), as a stage of `cos-convert`."
2. `references/sources-and-corpora.md`, anchor "Page anchors and the diacritics repair pass are
   later phases, and each has its own issue in `masorah-books`" through "modelled on ITM's
   `books/itm/historical-docs-fix-diacritics/`." → "The page anchors are a later phase,
   `masorah-books` **#15** (open), which wants a `page_section_map.json` derived from the scans.
   The diacritics repair pass is done, **#16** (closed 2026-08-04): it is `repair` in
   `py/cos/fix_diacritics.py`, a stage of `cos-convert`, with its log and manual-review report
   under `books/cos/fix-diacritics/`." Keep the sentences that follow ("Say which repo…" and "Do
   not start a later phase unasked").

**M7 — Class 4. `references/terminology.md` sends the reader to an archived, de-listed repo for
the proposals index.** Anchor "`../document-index` (repo `bdenckla/document-index`) indexes every
proposal Ben has authored, in `Unicode-and-ISO-Proposals.md`:". `gh repo view bdenckla/document-index
--json isArchived` → true; clause 1 of `gitrepos_setup_rule` records MAM-basics `c0b3195`
de-listing it on 2026-08-31, "whose two documents this repo's site generates now"; the index is
`MAM-basics/py/author_site/unicode_proposals.py`, rendered as `gh-pages/unicode-proposals.html`
(`git -C C:/Users/BenDe/GitRepos/MAM-basics grep -l Unicode-and-ISO-Proposals`). Replacement:
"`MAM-basics/py/author_site/unicode_proposals.py`, rendered as
`MAM-basics/gh-pages/unicode-proposals.html`, indexes every proposal Ben has authored. It was
`document-index`'s `Unicode-and-ISO-Proposals.md` until 2026-08-31, when that repo's content was
evacuated into MAM-basics (`c0b3195` de-listed it from the roster) and the repo archived:".

**M8 — Class 4. `references/terminology.md` names three pages as unswept "witness" holdouts; all
three are clean.** Anchor "**Not** swept and worth offering if you touch them:
`almost-errors.html` ("three standard witnesses (Aleppo, Leningrad, Cairo)"), `poetic.html`,
`telg-doc-notes.html`." Each has 0 occurrences of "witness" under
`MAM-basics/gh-pages/wlc/accgram/` (`python .novc/review-2026-09-09/remeasure.py`; or
`grep -ci witness` on each); `git log -S witness` over their MAM-basics paths is empty, so the
sweep happened in wlc-utils before the 2026-08-12 move. Replacement: "Swept: the printed-Decalogue
trio, and — measured 2026-09-09 — `almost-errors.html`, `poetic.html` and `telg-doc-notes.html`,
which have no "witness" left; this entry listed those three as unswept holdouts until then."

**M9 — Class 4. `references/terminology.md` line 56 contradicts line 315 of the same file about
the page title.** Anchor "The rendered title that came out of this is "Accents on a Non-Final Atom
of a Compound"". The page's `<title>` and `<h1>` are "Strange Spreaders in Koren and Simanim"
(`remeasure.py`), which line 315 records as Ben's decision of 2026-07-30. Replacement: "The
rendered title that first came out of this was "Accents on a Non-Final Atom of a Compound" —
"maqaf" dropped only for space, since there is no other kind of compound; the page has been titled
"Strange Spreaders in Koren and Simanim" since Ben's decision of 2026-07-30 (§"Never a bare
"Simanim"" below)."

**M10 — Classes 1 and 4. `dot-claude/README.md`'s `hebrew-prose` row restates a stale list the
skill keeps current.** Anchor "Supersedes the scattered copies in `~/.claude/CLAUDE.md`,
`wlc-utils/CLAUDE.md`, `printed_decalogue_strands.py`'s docstring and the wlc-utils auto-memory".
`wlc-utils/CLAUDE.md` was shrunk to redirect-host facts on 2026-08-17 and the module is
`MAM-basics/py/accgram/printed_decalogue_strands.py`; `SKILL.md` §"Where these rules used to live"
carries the current list (the wlc-utils auto-memory still exists:
`ls C:/Users/BenDe/.claude/projects/c--Users-BenDe-GitRepos-wlc-utils/memory`, 2 files).
Replacement: "Supersedes the scattered copies its own §"Where these rules used to live" lists —
those stay as pointers, and a rule change goes into the skill first."

**M11 — Class 1. `dot-claude/README.md`'s "the five of 2026-09-09" is seven.** Anchor "commit
`1925699` of 2026-09-07 and the five of 2026-09-09 that followed it each edited
`~/.claude/skills/hebrew-prose/` and copied outwards from there". Commits touching
`dot-claude/skills/hebrew-prose` between `1925699` and `14c17d4`: `25a8955`, `560239c`, `9ea78d2`,
`1956966`, `d1e061d`, `d612071`, `3895194` — seven
(`git log --format=%h 1925699..14c17d4 -- dot-claude/skills/hebrew-prose`; `14c17d4`'s own message
says six). `560239c` did not reach `~/.agents`, so "copied outwards" also overstates. Replacement:
"commit `1925699` of 2026-09-07 and the seven of 2026-09-09 that followed it
(`git log --format=%h 1925699..14c17d4 -- dot-claude/skills/hebrew-prose`) each edited
`~/.claude/skills/hebrew-prose/` first and copied outwards from there — one of them, `560239c`,
only as far as the canonical copy."

**M12 — Citation resolution. Eighteen bare wlc-utils issue numbers collide with MAM-basics
issues; prefix every one `wlc-utils#`.** Under `MAM-basics/CLAUDE.md` §"Five issue trackers" a
bare `#NN` names MAM-basics. Every number below is a wlc-utils issue (titles verified: #13
transliteration standardization, #26 transliteration linter, #27 decomposed-ḥ guard, #49 NFC,
#75 maqaf token, #76 maqaf-on-one-scale) and every number also exists in MAM-basics with an
unrelated title (#13 multi-change verses, #26 and #27 `main_diff_mpp`, #49 trivial-qere FOI, #75
paths convention, #76 `copy_support_files`). Command:
`python .novc/review-2026-09-09/resolve_issues.py` → `issues_report.txt`. The sites:

1. `dot-claude/user-wide-CLAUDE.md`: Tests § "(issue #26)"; Tests § "#27→#49"; Maqaf §
   "Issue #76."
2. `dot-Codex/user-wide-AGENTS.md`: the same three passages (lines 704, 719, 1000).
3. `references/terminology.md`: "Issue #13 (closed)", "since #49 (2026-07-01)", "the one place
   #13's text is genuinely out of date", "#49 inverted that", "`tests/test_transliterations.py`
   (#26)" twice.
4. `references/verifying.md`: "#27 → #49 is the cautionary tale"; "gone since #49".
5. `references/rendered-prose.md`: "(issue #75)".

`CLAUDE.md`'s "(issue #187 …)" in the Unicode section is MAM-basics #187 and is correct as a bare
number under the rule; note that wlc-utils#49 carries the identical title, so "MAM-basics #187"
would remove the last ambiguity.

**M13 — Class 1. `references/verifying.md`'s "fourteen call sites" needs re-measuring with a
call-site filter.** Anchor "Every MAM-basics caller does pass it — fourteen call sites,
`git grep -n read_parsed_plus_bk39s`". The command the file gives counts lines, imports included:
17 outside the defining module at `d8a0fdae`
(`git -C C:/Users/BenDe/GitRepos/MAM-basics grep -n read_parsed_plus_bk39s -- "py/*.py"`, less the
`def` line and the defining module). Re-measure with `grep -n "read_parsed_plus_bk39s("` less
imports, write that count and that command, or drop the count and keep "every caller passes it".

## 3. Fixes that need a decision from Ben — 16 items, one of them since answered

**D1 — Class 4. holman-ketiv-qere is cited as a live Python repo in both instruction files.**
§"No `sys.path` surgery": "holman-ketiv-qere 51 [tests] … through `python py/main_test.py`" and
"Of those two repos only holman-ketiv-qere still has one [registry]". Its Python moved into
MAM-basics on 2026-08-18 and the repo is a redirect host with no `py/`
(`gh api repos/bdenckla/holman-ketiv-qere/contents/ --jq '.[].name'` → `.gitattributes .github
.gitignore CLAUDE.md README.md gh-pages`). The registry-check bullet ("Where a registry exists,
compare `py/main_test.py --list` against `git ls-files`…") now has no live instance. Decide: keep
it as dated history, or delete the bullet and the test count.

**D2 — `AGENTS.md`'s "Default to Codex's built-in tools (Read, Write, Edit, Grep, Glob)".** Those
are Claude Code's tool names. Whether Codex has equivalents, and whether its harness pushes
heredocs the way M4.1 describes for Claude Code, is for Ben to say; the review did not examine
Codex's tooling.

**D3 — Class 1 at section scale. `AGENTS.md` lacks four `CLAUDE.md` sections and parts of nine
shared ones, and two ~90 KB copies have diverged in 9 of 23 shared headings in eight days.**
Missing whole sections: "Authored paths use forward slashes" (2026-09-02); "Prose: a reported
finding says what HAPPENED to it" (2026-09-02); "A transcription is evidence about the
transcription, never about the manuscript" (`2513bf4`, 2026-09-01 12:44 — before `AGENTS.md`'s
16:15 creation, so the snapshot predated that day's tracked copy); the roster section (M3).
Missing inside shared sections: the Git section's "A worktree Codex made, under
`C:/Users/BenDe/.codex/worktrees/<repo>-<branch>` …" bullet, which is the one most about Codex;
the handoff section's OFFER, symptoms, SAY-so and defuses bullets and the primary-checkout form
of the spawn-last bullet; "(its step 7)" in the maintenance section. Some are Claude-specific
(task chips, `<total_tokens>`); "forward slashes", "reported finding says what happened" and
"transcription" are agent-neutral. Command: `python .novc/review-2026-09-09/section_compare.py`.
Decide, per section, what belongs on the Codex side — and the structural question: keep two full
copies with a periodic section-level compare (§7), or make `AGENTS.md` a short Codex-specific
file that names `~/.claude/CLAUDE.md` as the rule of record. `MAM-basics/doc/dual-agent-review.md`
§"A precondition this document does not own" says Codex "will never load" `CLAUDE.md`, which is
the fact that decides between the two.

**D4 — Class 4. `SKILL.md` cites a deleted plan.** Anchor
"`MAM-basics/doc/PLAN-evacuate-the-rest-of-wlc-utils.md`" in §"Where these rules used to live".
Deleted by MAM-basics `80c9ad85` (2026-09-03, "Close second-stage evacuation bookkeeping"); the
survivor is `doc/PLAN-evacuate-the-rest-of-three-repos.md`
(`git -C C:/Users/BenDe/GitRepos/MAM-basics log --diff-filter=D --name-status --
"doc/PLAN-evacuate-the-rest*"`). Decide: cite the successor plan, or the deleting commit, or
`MAM-basics/CLAUDE.md` §"wlc-utils belongs on no machine".

**D5 — Class 4. The masorah-books example in §"A worktree runs the primary clone's venv" no
longer illustrates its hazard.** Both instruction files: "Anything computing
`repo_root().parent / "<sibling>"` lands in `.claude/worktrees/<sibling>` … In `masorah-books`
exactly one pass is affected and it takes an override flag." The one sibling-reaching pass,
`itm-liberality`, uses a hardcoded absolute path
(`MAM-private/masorah-books/py/itm/liberality_metric.py` line 33,
`HTML_DIR = Path(r"C:/Users/BenDe/GitRepos/phonetic-hbo/gh-pages")`) with an `--html-dir`
override, so a worktree does not break it; another machine does
(`python .novc/review-2026-09-09/remeasure2.py`). Decide: drop the example, or reword it as the
other-machine case.

**D6 — Class 4. `SKILL.md`'s frontmatter description names five repos where no prose is written
any more** — UXLC-utils, al-hatorah, book-of-job, mgketer, codex-index-aleppo (each evacuated,
archived or a redirect host per `MAM-basics/CLAUDE.md`'s repo-location sections and mgketer's
2026-08-27 archival). Harmless for triggering; false as a statement. Decide whether to trim it to
MAM-basics and MAM-private.

**D7 — Class 4. The Codex `prune-claude-state` skill describes Claude's state, not Codex's.**
`dot-Codex/skills/prune-claude-state/SKILL.md` says plans are `~/.Codex/plans/*.md` — Codex's are
`~/.codex/plans/<thread-id>/<turn-id>/PLAN.md` (4 on 2026-09-09, no repo name in the path); says
to read `MEMORY.md` in the memory directory — no `MEMORY.md` exists under `~/.codex`, whose memory
is `memories_1.sqlite`; and names `AskUserQuestion` and "an Explore (or general-purpose) agent"
(`remeasure.py`, `remeasure2.py`). Decide: rewrite against Codex's actual layout, or drop the
skill. Also, both prune skills quote the Claude system prompt as "You have a persistent,
file-based memory system at …"; the 2026-09-09 wording is "You have a persistent file-based memory
at", so the quoted search string fails — decide whether to quote loosely.

**D8 — `.Codex` spellings.** `dot-Codex/README.md` line 9 and `AGENTS.md` lines 8, 12, 248, 375,
1051 write `~/.Codex/…`; the directory is `C:/Users/BenDe/.codex`, as `CLAUDE.md` and
`dual-agent-review.md` spell it (that document's line 273 already warns that a case-sensitive glob
misses `dot-codex`). NTFS hides the difference; a case-sensitive tool does not. Decide whether to
lower-case the live-path spellings while keeping the tracked directory `dot-Codex`.

**D9 — Class 1. The CoS export figures and the scan count are in three places.** "522 sections
in 57 files" in `SKILL.md` and `references/sources-and-corpora.md`, the per-chapter section counts
(Ch. 1 44 … Ch. 15 50) in the latter, and "719 page images" in both — all restated from
`MAM-private/masorah-books/README.md` §"CoS — 57 files, chapter-scoped numbering" and §"What is in
this repo". In step on 2026-09-09 (57 files on disk; `python .novc/review-2026-09-09/remeasure.py`,
`numeral_dupes.py`). Ben's rule of 2026-09-09: where an external authority exists, point at it.
Decide whether these follow the gate figures home.

**D10 — Class 1. The maqaf survey headline in `references/sources-and-corpora.md`.** "WLC 4.22
(36,806 compounds, 139 hits) to MAM (36,786; 233; 0.63%)" restates
`MAM-basics/out/accgram/maqaf-nonfinal-accents.json` (`corpora.wlc422.prose` 36806/139,
`corpora.mam_simple.prose` 36786/233; `remeasure2.py`). In step, and the entry is a worked
example of corpus choice; but the same file's §"Where the survey of this lives" says "never
restate its numbers in another docstring". Decide: keep as a worked example, or replace the
numerals with the JSON keys.

**D11 — Class 1. `references/terminology.md`'s "About 7,800 words … roughly 3,800"** restates
Ben's L2/25-242 §9M. The PDF is the authority. Low; decide whether to keep.

**D12 — Class 1. The makaf entry could point at the README section that holds the counts
`d612071` removed.** `d612071` (2026-09-09) dropped "36 occurrences on 27 lines" from the skill
on the premise that "masorah-books records them nowhere"; `MAM-private/masorah-books/README.md`
§"Breuer's English mostly says "hyphen" — grep `hyphen`, `makaf` and `מקף`" carries 219 lines /
389 occurrences, 36 on 27 lines across nine files, and מקף once. Nothing in the skill is wrong now;
decide whether `references/sources-and-corpora.md`'s makaf entry gains a pointer to that section,
as the gate entries gained one on 2026-09-09.

**D13 — Class 3. `worktree-forest/SKILL.md`'s "Push every authorized forest-branch commit
according to the repository's Git instructions"** against the Git section's "In a secondary
worktree, commit only to its local non-`main` branch … Do not push that worktree branch merely as
a backup." Reconcilable through "authorized", but the skill (2026-09-01) predates the 2026-09-06/07
protocol. Decide whether to define "authorized" there or point at the Git section.

**D14 — Class 2. Rules that live only in the two READMEs.** The `Copy-Item -Recurse` nesting
hazard in `dot-claude/README.md` ("A plain `Copy-Item <src> <dst> -Recurse -Force` where `<dst>`
already exists … produces `skills/hebrew-prose/hebrew-prose/`"), and the copy-back commands for
the two Codex-only skills in `dot-Codex/README.md`. Both are reachable by the pointers added on
2026-09-09; decide whether the nesting hazard needs the same promotion the three-home rule got.
No other README-only rule was found.

**D15 — Class 5. Two steps without their command.** "Retire verified folders through the Windows
Recycle Bin, not permanent deletion" (both instruction files' maintenance section, and step 7 of
`MAM-basics/doc/PLAN-repo-maintenance-across-GitRepos.md`) has no command anywhere; a working
spelling is `Add-Type -AssemblyName Microsoft.VisualBasic` followed by
`[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory("<path>", "OnlyErrorDialogs",
"SendToRecycleBin")`. "To thaw a repo, un-archive it on GitHub" (black section, and the policy's
`location_comment`) gives no `gh repo unarchive bdenckla/<repo>`. Decide the one home for each —
the runbook step for the Recycle Bin, the policy comment for the thaw — with the instruction files
pointing.

**D16 — Whether this review joins the periodic review series, and where its scripts live —
ANSWERED 2026-09-09; it needs no decision from Ben.** He decided that this review is a one-off, and
the move to MAM-basics put the twelve files inside the public series' ordinary scope; the scripts
were copied to `MAM-basics/.novc/review-2026-09-09/`. §7 carries the reasoning and the one live
proposal it leaves. It keeps its number so that D1–D15 keep theirs, so **fifteen of the sixteen
still need a decision.**

## 4. Verified sound — what is not expected to change

1. **SHAs.** All 23 unique SHAs cited resolve — 8 in github-misc, 6 in MAM-basics, 6 in
   wlc-utils (`25a7800`, `51e2748`, `cda21f9`, `ee21ebb`, `80ca0df`, `9c95cf9`), one each in
   mgketer (`efa95ccf`), al-hatorah (`cab47317`) and breuer-cos (`54440aa`) — with the dates the
   prose gives (`python .novc/review-2026-09-09/resolve_shas.py` → `shas_report.txt`).
2. **Sections.** All 13 `§"…"` citations resolve, as do `clc-design.md` §2 and §7.16,
   `PLAN-near-aleppo.md` §3 rule 7 and its step-40 row, the maintenance runbook's step 7,
   `edition-transcription-workflow.md` §2, `review-findings-2026-07-29.md` item 14,
   `mgketer/CLAUDE.md` §"UTF-8 Everywhere" rule 6, and finding 5.6 and row 22 of
   `review-findings-2026-09-08.md` (`final_checks.py`).
3. **Identifiers.** 87 cited identifiers, subcommands and phrases exist in MAM-basics or
   MAM-private; the only absences are the ones the prose asserts (`--line-length` in
   `run_black.py`, `pypdf` in any venv, `WLC_SIBLINGS_ROOT` outside its rename docstring) and M8–M9.
   `generate-html-goerwitz`, `-almost-errors` and `-supplied-marks` exist among the 34 subcommands
   of `py/main_accgram.py --help` (`identifier_sweep.py`, `final_checks.py`).
4. **Counts.** masorah-books 19 issues, al-hatorah 124, wlc-utils 93, trope 111 open, breuer-cos
   holding only #1, #4 and #5 (all closed), MAM-private #13 and #14 open, 11 deploy-root pages
   (nine `post-stress-meteg*` plus `index` and `unicode-proposals`), ITM 53 and CoS 57 export
   files, the maqaf survey's 36,786 / 233 (`resolve_issues.py`, `remeasure.py`, `remeasure2.py`).
5. **Three-home drift: none**, and `~/.codex/skills/` exists empty, so there is no fourth home
   (`drift_check.py`).
6. **The 2026-09-09 fixes hold**: the `REPOS_ROOT` bullet, the withdrawn worktree ban and its
   caution, the gate-figure pointers, the ZEROs in the spelling traps, the eighteen-pass count,
   the live-first deploy order.
7. **Not touched by this plan**: every accentuation rule in the skill; the two READMEs' procedures
   and commands; `dot-claude/skills/prune-claude-state/SKILL.md` beyond D7's quotation;
   `worktree-forest/SKILL.md` beyond D13; `dot-emacs` and `dot-gitconfig`, which were out of
   scope.

## 5. Order of operations, commit grouping, verification, integration

1. **Preconditions** (§1): read any newer `dot-*/` commit; `drift_check.py` clean; both trees
   clean; record `HEAD` of github-misc and MAM-basics.
2. **The skill, one commit**: M6, M7, M8, M9, M12's three skill files, M13, plus whichever of
   D4, D6, D9, D10, D11, D12 Ben has decided. Edit `~/.claude/skills/hebrew-prose/`, run the four
   deploy steps and both comparisons, commit with the skill's three homes byte-identical.
3. **`CLAUDE.md`, one commit**: M1, M2, M12's `CLAUDE.md` sites, plus D1, D5, D14, D15 as
   decided. Edit `~/.claude/CLAUDE.md`, copy back, commit.
4. **`AGENTS.md`, one commit**: M2's five, M3, M4, M5, M12's `AGENTS.md` sites, plus D1, D2, D3,
   D5, D8, D15 as decided. Edit `~/.codex/AGENTS.md`, copy back, commit.
5. **The READMEs and the Codex skills, one commit**: M10, M11, plus D7, D8, D13, D14 as decided.
6. **Verify**: re-run `extract_citations.py`, `resolve_paths.py`, `resolve_issues.py`,
   `section_compare.py` and `drift_check.py`; the named dangling paths and the eighteen bare
   numbers must be gone, the three homes identical, and `section_compare.txt` must show only the
   divergences Ben chose to keep under D3.
7. **Commit messages** state each defect, its evidence and Ben's dated decision, and carry the
   disposition "has been fixed" up front, per `~/.claude/CLAUDE.md` §"Prose: a reported finding
   says what HAPPENED to it".
8. **Integrate**: in the primary clone, run `.venv/Scripts/python.exe py/main_test.py` from the
   repository root and then push `main`; in a worktree, immediately after step 5 by the Git
   section's four steps (`git merge --no-edit main` in the worktree, run the suite there with
   `$env:REPOS_ROOT` set as §1 item 4 says, `--ff-only` in the primary clone, push), for the reason
   in §1 item 1. **The suite is the step github-misc did not have**: `main` must not carry a commit
   nothing has verified.

## 6. The review's scripts and outputs, and how to run them

**The thirteen scripts and their reports were copied to
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/review-2026-09-09/` on 2026-09-09, before github-misc's
clone was retired**, so every `python .novc/review-2026-09-09/<name>.py` cited in §2–§4 resolves
from the MAM-basics repository root. `.novc/` is ignored, which is the arrangement MAM-basics'
reviews use — so that copy is machine-local, exists on one machine, and no clone of MAM-basics
restores it. They are throwaway-grade — `~/.claude/CLAUDE.md` §"Throwaway scripts: the lowest bar of
software" — and each prints a labelled report or writes one beside itself. **A session that does not
find them should rewrite the one it needs from the descriptions below rather than hunt for them.**
Run each as `python <that directory>/<name>.py` with the system Python; none needs a venv.

Two things about the copies are stale by construction, and neither is worth fixing until a script is
actually run. `drift_check.py`, `extract_citations.py` and `section_compare.py` name the checkout
whose tracked copies they read in a `WT` constant near the top; **it still says
`C:/Users/BenDe/GitRepos/github-misc` and must be repointed to
`C:/Users/BenDe/GitRepos/MAM-basics`**, or to a worktree. And **`substitution_proof.py` cannot run
from the copy at all**: it reads the repository at `f8898a9`, a github-misc commit, so it needs a
fresh clone of the private remote — see §0.

1. `drift_check.py` — sha256 of all twelve files at every home; the §1 baseline. **Stale twice
   over: the `WT` constant above, and the two renames — its `dot-claude/CLAUDE.md` and
   `dot-Codex/AGENTS.md` rows are `dot-claude/user-wide-CLAUDE.md` and
   `dot-Codex/user-wide-AGENTS.md` now.**
2. `extract_citations.py` — every path, SHA, issue number, `§"…"` heading and numeral in the
   twelve files, to `citations.json` and `citations_report.txt` (1,064 records at `810ffd0`: 608
   paths, 45 SHAs, 67 issue refs, 13 sections, 331 numerals).
3. `resolve_paths.py` — resolves each path against the roots and by basename →
   `paths_report.txt`.
4. `resolve_shas.py` — each SHA against the seven local clones, then `gh api` against eight
   remote repos → `shas_report.txt`.
5. `resolve_issues.py` — `gh issue view` for 32 cited issues, `gh issue list` counts for six
   repos, `gh repo view` archival state for nine → `issues_report.txt`.
6. `numeral_dupes.py` — numerals appearing in two or more files, and every numeral in the skill →
   `numerals_report.txt`.
7. `identifier_sweep.py` — `git grep -F` of 87 cited identifiers over MAM-basics and MAM-private
   → `identifiers_report.txt`.
8. `section_compare.py` — `##`-section comparison of the current `CLAUDE.md` and `AGENTS.md`
   after `claude`→`Codex` substitution → `section_compare.txt`.
9. `substitution_proof.py` — the same comparison at `f8898a9`, proving `AGENTS.md`'s origin →
   `substitution_diff.txt`.
10. `show_policy.py`, `remeasure.py`, `remeasure2.py`, `final_checks.py` — the policy registers,
    and the re-measurements cited in §2–§4.

## 7. Whether this review joins the periodic series: ANSWERED, and it does not — it was a one-off

**Disposition: Ben decided on 2026-09-09 that this review is a one-off, and the move to MAM-basics
dissolved the obstacle that made D16 hard to answer.** This section replaces its 2026-09-09
original, which was written while the twelve files were still in a private repository.

### The two properties of the series, and what each one actually excluded

The process is defined in `doc/dual-agent-review.md` §"What the periodic review is, and what Codex
joined" — every four to eight days, public repositories only since 2026-08-26, doc-only since
2026-09-01 — with each `doc/review-findings-<date>.md` restating its scope, anchors and streams. The
convention of record for both properties is the "The doc/ directory standard" section of
`py/repo_util/check_repo_standards.py`'s module docstring. Read it there rather than re-deriving it.

1. **The public-only property did exclude these files, and no longer does.** github-misc is private
   (`gh repo view bdenckla/github-misc --json isPrivate`), so until 2026-09-09 the twelve fell to
   the private series, which has run once (`MAM-private/doc/review-findings-2026-08-26.md`); the
   public series reached them only through its "one deliberate exception", the byte-compare
   recorded as row 22 and finding 5.6. **All twelve are tracked in public MAM-basics now, so they
   fall inside the public series' ordinary scope, with no exception and no special instruction.**
2. **The doc-only property never excluded them, and reading it as a limit on what a review READS is
   a misreading.** "Doc-only since 2026-09-01" (`5b89033`) says where a review is RECORDED: the
   thin tracking issue each review used to file is retired, and the `State:` line in the doc now
   carries the open/closed state that issue held. It says nothing about which files a review may
   read. The reviews settle it themselves — `doc/review-findings-2026-09-08.md` is headed "review
   of the public repos", counts 99 commits across two repositories and 513 changed paths, and reads
   Python, pages and data throughout. **So `dot-claude/` and `dot-Codex/` need neither a scope
   widening nor a deliberate exception: a doc-only review already reaches any tracked file in a
   public repository.** This is worth stating because two documents written on 2026-09-09 both read
   "doc-only" the other way, and either reading would have sent a future session to Ben for a
   decision he does not owe.

### The series' standing exception is spent

`doc/dual-agent-review.md`'s "one deliberate exception" — the byte-compare of github-misc's
instruction-file plumbing, applied at row 22 and finding 5.6 — **is spent, and is recorded as spent
in that document rather than deleted**, so a reader of finding 5.6 can still see why it existed. The
files it reached are in MAM-basics and the ordinary sweep reads them; and github-misc's clone was
retired on 2026-09-09, so performing the byte-compare on this machine would now mean re-cloning a
private remote to compare a file against itself.

### What a future review of these twelve files should do

Ben's decision of 2026-09-09 makes THIS review a one-off, so the three items below are proposals for
the ordinary series rather than a schedule this plan sets. **Recommendation 1's blocking objection
died with the move**, which is the one substantive change from this section's original.

1. **Run §6's mechanical sweep, items 1 to 8, as part of the ordinary review rather than as an
   exception.** It costs minutes and would have caught M12, D4, M11 and the `~/.agents` lag. Its
   original blocker was that the scripts wanted a tracked home while github-misc tracked no Python
   and had no venv, leaving two poor candidates; **MAM-basics has both**, so one candidate remains
   — a `py/main_repo_util.py` action, or a module under `py/repo_util/`, tracked here beside the
   checks that already run. Whether to build it is Ben's, and nothing here builds it.
2. **Read the sections a window changed, as a stream, whenever the window holds a `dot-*/`
   commit.** Classes 2–5 need judgment; a diff-scoped read is small. Unchanged by the move, except
   that those commits are MAM-basics commits now and enter the window by themselves.
3. **A full read only after a burst.** This review's findings come from two events — the
   2026-09-01 creation of `AGENTS.md` and the 2026-09-07 port — not from slow drift. Unchanged.

So D16 is answered in three parts: the review does not join the series as an instalment, the twelve
files it reviewed join the series' scope automatically, and item 1 is the one live proposal left.
