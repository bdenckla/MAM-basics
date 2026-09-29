# AGENTS.md

## Compatibility note for historical instruction citations

`AGENTS.md` is the common repository instruction body. Codex loads it directly, and Claude Code
loads it through the minimal `CLAUDE.md` wrapper. Historical prose that cites “`CLAUDE.md`'s
section X” means either the matching section here or the task-specific reference to which that
section now points; do not mechanically rewrite historical citations.

## Hebrew marks go in MAM-normal order, not Unicode-normal order

MAM-normal order gives priority to shin dot, sin dot, dagesh/mapiq/shuruq dot,
dagesh ḥazaq (U+05C9), and rafe. The two dagesh code points share a priority while
preserving the other marks' relative order. `py/mb_cmn/uni_denorm.py` is the authority:
`give_std_mark_order` applies the order and `has_std_mark_order` checks it.

**Never call `unicodedata.normalize` in any form on Hebrew.** When two Hebrew strings that should
match do not, compare them through `give_std_mark_order`; do not normalize them. Hebrew copied
from a browser is especially suspect because the two orders render identically.

Do not “repair” faithful external captures or intermediates upstream of the pipeline's deliberate
denormalization. Known examples include `in/mam-ws/`, its faithful intermediates, and verbatim
source captures. For scope, census evidence, and the checks covering authored prose, Python,
JSON, data, and generated pages, read `doc/mam-normal-mark-order.md` before changing mark order.

## Tracked filenames do not use Hebrew letters; Git filename output is NUL-delimited

No tracked filename contains a Hebrew letter. Convert a Hebrew filename component with
`consensus_to_ascii` from `py/author_boj_util/author.py`; do not invent another
transliteration.

Every programmatic Git command returning filenames requests NUL delimiters with `-z` and splits
on `"\0"`, never on lines. Spaces, tabs, newlines, quoting characters, and future non-ASCII
filenames remain possible. `py/tests/test_tracked_filenames.py` enforces both rules.

## Invoke the `hebrew-prose` skill before accentuation prose

Before writing, editing, or reviewing prose about Hebrew accentuation or cantillation, load the
user-level `hebrew-prose` skill. This includes rendered text, headings, tables, tooltips, alt
text, docstrings, comments, commit messages, issue text, and chat. The skill covers atom versus
chanted word, the one-scale maqaf rule, paseq versus legarmeh, silluq versus meteg, prose and
poetic verses, corpus choice, primary sources, rendered-prose conventions, and verification.

For MAM-basics work, the skill requires its `references/mam-basics.md` reference. That reference
carries this repository's exceptions and page-specific rules, including the deliberate plain
“word” terminology on the post-stress-meteg pages and the accgram rendered-prose rules.

The canonical shared skill is `dot-claude/skills/hebrew-prose/`; the live copies under
`~/.claude/skills/` and `~/.agents/skills/` are what the agents load. `dot-claude/` and
`dot-Codex/` are version-controlled storage, not project instruction trees. Edit a canonical
copy, commit and integrate it, then deploy from any full MAM-basics clone with the
`--sync-user-config` procedure in `dot-claude/README.md`. Never edit a live copy.

### Claude Code cloud SessionStart installation

`.claude/hooks/install-user-config.sh` supplies a Claude Code cloud session from the session's
checked-out branch because the machine-level files do not travel with the clone. The hook is
network-free, reports what it installed, and exits without reading anything on Ben's machines.
Codex does not run this Claude hook. The checked-out branch, not necessarily `main`, is the
cloud source. `doc/user-level-config-in-cloud-sessions-update.md` carries the current diagnosis.

## The MAM introduction is mirrored locally

Read `in/mam-ws-intro/README.md` and the mirror itself instead of fetching a summarized web copy.
The README maps all thirteen files, gives the independent refresh command, explains the
byte-verbatim mark-order exception, and distinguishes the two manually maintained index pages
from their retired one-off generators. `manifest.json` records each source revision and
timestamp.

## MAM special pages are mirrored with every Wikisource chapter download

Every `py/main_download.py fr-wikisource` run maintains the 36 declared Decalogue,
song-form, and corresponding chapter pages under `in/mam-ws-special/`, even when the
chapter selection is narrow. The `.mediawiki` files are byte-verbatim captures and
`manifest.json` records requested and resolved titles, exact revisions, byte sizes,
and SHA-256 hashes. `py/ws/ws_special_page_download.py` owns the literal inventory,
checks it against the two tables in `in/mam-ws-intro/ch2.mediawiki`, and permits only
the eight declared identities to overlap the chapter mirror. Do not hand-edit the
mirror or its manifest.

## Holman and book-of-Job work has local routing documentation

Before touching Holman mailboxes, correspondence derivatives, dispositions, or authored assets,
read `holman/WORKFLOW.md`. Raw mail remains untracked; public derivatives exclude addresses; MAM
suggestion dispositions contain substantive judgments rather than personal circumstances; and
authored CSS and JavaScript live in `holman/assets/`, not in generated `gh-pages/` copies.

Before touching `py/author_boj*`, read the relevant `doc/boj-*.md` procedure. Those four
procedures began as Copilot instructions and have not all been re-verified, so current
user-level and repository instructions win when a command conflicts. The two procedures for
reading the evacuated product live under `book-of-job/doc/`.

## The HBCE Psalms snapshot is never refreshed from its site's API

Before touching `hbce-psalms/`, `py/hbce_psalms/` or `py/main_hbce_psalms.py`, read
`hbce-psalms/README.md`. Never fetch from hbcepsalms.manuscriptroom.com's web-service API, which
the site's robots.txt disallows: the snapshot is a good-faith download made before anyone had read
that file. If the work resumes, fresh data comes only through the INTF or its documented exports,
and whether to contact the INTF is Ben's decision. `hbce-psalms/out/` is a frozen record of one
run: by Ben's decision of 2026-09-26, a change to MAM's data does not oblige rerunning
`py/main_hbce_psalms.py compare`, as the hand-run rule below would otherwise require.

## Issue citations in MAM-basics

Load the `github-issues` skill for any issue operation or citation audit. The always-needed
MAM-basics rules are:

1. A bare `#NN` in current MAM-basics files means a MAM-basics issue. Cite another tracker as
   `repo#NN`. In an issue or comment, use the other issue's full URL.
2. A number that is not an issue never takes a bare `#NN` form. Name an ITM section, a design-doc
   item, a UXLC change, or a CSS color in a form that cannot link to an unrelated issue.
3. Imported wlc-utils documents under `doc/` and `in/`, and imported UXLC-utils documents under
   `uxlc/doc/`, retain their original bare-number meaning. Read the surrounding sentence before
   changing a citation.
4. `py/py_render/rt_issue_tags.py` and `py/hkq_cmn/table_row_github_issues.py` render
   holman-ketiv-qere issue numbers as data. Repository constants supply that tracker; prefixing
   the stored numbers would corrupt the output.

For collision history, evacuated tracker dispositions, transferred issues, and the exact traps
encountered by past sweeps, read the skill's `references/mam-basics-trackers.md`.

## Review filenames and finished dated documents

Follow `doc/dual-agent-review.md`, “Review filenames and State lines”, for the filename matching
the agent and review round, author and turn ownership, and review State exceptions. Private
review records stay in MAM-private; `doc/periodic-review.md` owns the series procedure.

Load `iterative-document-editing`, “Finished receipts and maintained documents” and
“MAM-basics and MAM-private State conventions”, for receipt corrections and non-review State.
Load `mam-repository-topology`, “Manual document retirement”, before retiring a receipt family
or carrying out Ben-authorized reclassification.

## Repository topology is task-specific

Load the shared `mam-repository-topology` skill before setting up or synchronizing GitRepos,
performing repository maintenance, publishing redirect stubs, retiring a clone, or deciding
where an evacuated repository or sibling dependency lives. If the skill is not installed in a
cloud session, read `dot-claude/skills/mam-repository-topology/SKILL.md` from the checkout and
follow its reference routing.

`in/repo_maintenance_policy.json` and `all-repos.code-workspace` are the sources of truth. A
clone's presence on one machine is residue, not evidence that a topology decision changed. Do
not infer the desired clone set from `gh repo list` or a disk set difference. Evacuated public
repositories can remain redirect hosts or issue trackers while belonging on no machine; the
skill's `references/evacuated-repositories.md` carries their exact current dispositions,
temporary-stub procedures, and historical traps.

## What this repository's products are, and which check a change owes

`py/product_scopes.py` is the declaration of record, enforced by
`py/tests/test_product_scopes.py`. The product tiers are:

1. **Published:** `gh-pages/`, published from `main` once daily at 4:17 AM, New York time, and
   on manual dispatch.
2. **Distributed data:** `MAM-parsed/`, `MAM-simple/`, `MAM-for-Sefaria/`, `MAM-with-doc/`, and
   `MAM-OSIS/`.
3. **Generators:** the entry points run by `py/main_0_mega.py`.

A change that can reach a mega generator owes a mega run and an explanation of every tracked
diff. A documentation-only change owes neither a mega run nor the suite. Any other change that
cannot reach a mega generator owes the suite. A hand-run generator can reach a product even though
the mega does not run it. A change to a hand-run generator, or to any input it reads, requires
rerunning every affected hand-run generator and inspecting its tracked outputs. Product reach and
whether an act is hard to undo are separate risk axes, as the user-level instructions explain.

Ben decided on 2026-09-11 that `py/main_0_mega.py` writes nothing outside this repository;
MAM-private runs its own near-Aleppo census.

## Generated clock dates and timestamps shown on pages use New York time and say so

A date or timestamp that repository code generates from a clock for display on a page or report
is converted through `py/mb_cmn/new_york_time.py` and followed by “, New York time”. Historical
decision dates, citations, quotations, release or revision dates, and date-like names—including
release names, change ids and dated filenames—take no label. Stored timestamps retain full ISO
8601 offsets. Git dates retain their offset with `%cI` or `%ct`, never `%cs`; clock reads name
their zone. `py/tests/test_explicit_time_zones.py` enforces the mechanical rule.

## A code path reads MAM-private every time it runs, or never

A code path that depends on MAM-private reads it unconditionally. Every other code path must
fail loudly if it unexpectedly needs MAM-private; it must not probe for the private tree only
when particular data happens to require it. Use `py/mb_cmn/paths.py`'s required-sibling helpers.
The cloud-only suite exception is declared on the test module that reads Phonetic MAM.

## Integrating a worktree branch here: run the mega unless the branch is exempt

For final worktree integration, after merging the home clone's `main` into the worktree branch,
run from the worktree root using the home clone's interpreter by absolute path. The full-clone
form is:

```powershell
./.venv/Scripts/python.exe py/main_0_mega.py
```

A failing step or unexplained tracked diff is a failure. Commit each explained generated change
on the worktree branch before the worktree's home clone is fast-forwarded. Running the suite too is
optional. A branch changing only documentation, comments, docstrings, or instruction text needs neither a mega run
nor the suite. This exemption describes the changed content, not its directory.
Executable hooks and helpers, tests, schemas, shared data, and execution-changing
configuration receive the applicable checks even below `doc/`, `dot-claude/`, or
`dot-Codex/`. Generator or product changes still require their applicable generator checks. The user-level
Git section gives the remaining integration order.

## Running tests: use the one entrypoint from the repository root

Run the suite from the verified MAM-basics repository root. A full clone uses its own
environment; a linked worktree uses its home clone's interpreter by absolute path:

```powershell
./.venv/Scripts/python.exe py/main_test.py
```

Arguments pass through to pytest. A linked worktree normally finds MAM-private through Git's
common-directory metadata and needs no `REPOS_ROOT`; the variable remains an override for an
unusual layout. Always run from the repository root because some inputs are intentionally
cwd-relative.

`py/main_test.py` is the only runner. A bare `pytest` or `pytest py/tests` failing imports is the
designed state; do not add `sys.path` surgery, a root `conftest.py`, pytest `pythonpath`, a `.pth`,
`PYTHONPATH`, or an editable installation. Pytest discovers `test_*.py` and `*_test.py`
automatically; no registry exists.

Compare pytest summary counts using the same options.

Sibling paths use `mb_cmn.paths.repo_root()`, `repos_root()`, `sibling_repo(name)`, and the
required-sibling helpers, not cwd-relative parent paths or ad hoc `Path.parents` chains. The
local product directories do not require sibling clones.

## Writing tests: differential and lint-shaped only

Follow the common instruction body's “Tests are differential or lint-shaped” rule.
The `ws_bot` tests remain the deliberate exception because a live Wikisource edit is an
outward-facing act with no regeneratable artifact. `doc/agent-planning-principles.md`,
“Generated Outputs Are the Tests”, carries the dated evidence and rationale.

## This is the only repository instruction body

Codex loads this file directly. Claude Code's minimal `CLAUDE.md` imports it. Retired Copilot and
disabled instruction files are historical records, not additional instruction sources.
