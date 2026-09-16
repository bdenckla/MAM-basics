# AGENTS.md

## Compatibility note for historical instruction citations

`AGENTS.md` is the common repository instruction body. Codex loads it directly, and Claude Code
loads it through the minimal `CLAUDE.md` wrapper. Historical prose that cites “`CLAUDE.md`'s
section X” means either the matching section here or the task-specific reference to which that
section now points; do not mechanically rewrite historical citations.

## Hebrew marks go in MAM-normal order, not Unicode-normal order

MAM-normal order puts shin dot, sin dot, dagesh/mapiq, and rafe before every other mark while
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
`heb_alef_bet_to_ascii` from `py/py_ac_word_image_helper/alef_bet_to_ascii.py`; do not invent
another transliteration.

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
“word” terminology on the nine post-stress-meteg pages and the accgram rendered-prose rules.

The canonical shared skill is `dot-claude/skills/hebrew-prose/`; the live copies under
`~/.claude/skills/` and `~/.agents/skills/` are what the agents load. `dot-claude/` and
`dot-Codex/` are version-controlled storage, not project instruction trees. Edit a canonical
copy, commit and integrate it, then deploy from the primary MAM-basics clone with the
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

## Holman and book-of-Job work has local routing documentation

Before touching Holman mailboxes, correspondence derivatives, dispositions, or authored assets,
read `holman/WORKFLOW.md`. Raw mail remains untracked; public derivatives exclude addresses; MAM
suggestion dispositions contain substantive judgments rather than personal circumstances; and
authored CSS and JavaScript live in `holman/assets/`, not in generated `gh-pages/` copies.

Before touching `py/author_boj*`, `py/py_ac_word_image_helper/`, or
`py/py_cam1753_word_image/`, read the relevant `doc/boj-*.md` procedure. Those seven procedures
began as Copilot instructions and have not all been re-verified, so current user-level and
repository instructions win when a command conflicts. The two procedures for reading the
evacuated product live under `book-of-job/doc/`.

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

An unprefixed `doc/review-findings-<date>.md` is the single-agent Claude review series and the
Claude half of blind Design B. A Codex Design B review of the same window is
`doc/codex-review-findings-<date>.md`. A standard sequential alternating round instead uses
`doc/dual-agent-review-<date>-turn-<NN>-<claude|codex>.md`; Agent 1 owns odd turns, Agent 2 owns
even turns, and either Claude or Codex may be Agent 1. The private series stays in MAM-private.
`doc/periodic-review.md` and `doc/dual-agent-review.md` are the procedures of record.

A finished dated review, remediation plan, completed plan, or execution record is never edited.
Correct it in `<stem>-update.md`, then `<stem>-update-2.md`, and name the corrected passage by
its words rather than by a drifting line number. A document describing the present—this file,
README files, docstrings, and a plan still being executed—is kept true in place. The `State:`
rules live in `py/repo_util/check_repo_standards.py`'s module docstring.

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

1. **Published:** `gh-pages/`, deployed by a push to `main`.
2. **Distributed data:** `MAM-parsed/`, `MAM-simple/`, `MAM-for-Sefaria/`, `MAM-with-doc/`, and
   `MAM-OSIS/`.
3. **Generators:** the entry points run by `py/main_0_mega.py`.

A change that can reach a mega generator owes a mega run and an explanation of every tracked
diff. A change that cannot reach a mega generator owes the suite. A hand-run generator can reach
a product even though the mega does not run it; regenerate the outputs of the hand-run generator
when it changes. Product reach and whether an act is hard to undo are separate risk axes, as the
user-level instructions explain.

## Dates shown on pages are New York dates and say so

Every date shown by repository code on a page or report is converted through
`py/mb_cmn/new_york_time.py` and followed by “, New York time”. Stored timestamps retain full
ISO 8601 offsets. A date used as a name—a release name, change id, or dated filename—takes no
label. Git dates retain their offset with `%cI` or `%ct`, never `%cs`; clock reads name their
zone. `py/tests/test_explicit_time_zones.py` enforces the rule.

## A code path reads MAM-private every time it runs, or never

A code path that depends on MAM-private reads it unconditionally. Every other code path must
fail loudly if it unexpectedly needs MAM-private; it must not probe for the private tree only
when particular data happens to require it. Use `py/mb_cmn/paths.py`'s required-sibling helpers.
The cloud-only suite exception is declared on the test module that reads Phonetic MAM.

## Integrating a worktree branch here: run the mega and read its diff

For final worktree integration, after merging `main` into the worktree branch, run from the
worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

A failing step or unexplained tracked diff is a failure. Commit each explained generated change
on the worktree branch before the primary clone is fast-forwarded. Running the suite too is
optional. A branch changing only instruction files—`AGENTS.md`, `CLAUDE.md`, `dot-claude/`, or
`dot-Codex/`—needs no mega run. The user-level Git section gives the remaining integration order.

## Running tests: use the one entrypoint from the repository root

Run the suite from the MAM-basics root through the primary clone's shared interpreter:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Arguments pass through to pytest. A linked worktree normally finds MAM-private through Git's
common-directory metadata and needs no `REPOS_ROOT`; the variable remains an override for an
unusual layout. Always run from the repository root because some inputs are intentionally
cwd-relative.

`py/main_test.py` is the only runner. A bare `pytest` or `pytest py/tests` failing imports is the
designed state; do not add `sys.path` surgery, a root `conftest.py`, pytest `pythonpath`, a `.pth`,
`PYTHONPATH`, or an editable installation. Pytest discovers `test_*.py` and `*_test.py`
automatically; no registry exists.

Sibling paths use `mb_cmn.paths.repo_root()`, `repos_root()`, `sibling_repo(name)`, and the
required-sibling helpers, not cwd-relative parent paths or ad hoc `Path.parents` chains. The
local product directories do not require sibling clones.

## Writing tests: differential and lint-shaped only

Do not add an example-based unit test unless Ben asks. Add tests in one of two shapes:

1. A differential check against an independent oracle.
2. A mechanical lint over source text or the repository tree.

Otherwise regenerate the tracked artifact with the real command and read its diff; the artifact
is the test. A missing input fails rather than skips, and an empty parametrization must not report
green. The `ws_bot` tests are the deliberate exception because a live Wikisource edit is an
outward-facing act with no regeneratable artifact. `doc/agent-planning-principles.md`, “Generated
Outputs Are the Tests”, carries the evidence and full rationale.

## This is the only repository instruction body

Codex loads this file directly. Claude Code's minimal `CLAUDE.md` imports it. Retired Copilot and
disabled instruction files are historical records, not additional instruction sources.
