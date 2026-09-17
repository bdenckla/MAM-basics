# MAM repository topology, redirect hosts, and historical traps

Read this reference only for repository setup or maintenance, redirect-stub work, or questions about the location and status of an evacuated repository.

## Repo locations are decisions, not one machine's disk

Ben works on more than one machine, and they are not in step. A clone removed on one can still
be sitting on another; a sync run on one says nothing about the rest. So a sentence of the form
"X came off the disk on <date>" is a fact about one machine on one day, and reading it as a
global truth is what makes this file's history look self-contradictory when it is not. Ben's
instruction, 2026-08-31: **stop writing single-track, single-machine history here.**

Two consequences, and they apply to every location claim below.

1. **Write the decision, not the disk state.** "wlc-utils belongs on no machine" is checkable
   against the roster and stays true; "there is no local wlc-utils clone" expires the moment
   another machine is switched on. `all-repos.code-workspace` is the roster and
   `in/repo_maintenance_policy.json`'s `gitrepos_setup_rule` is the rule that reads it; between
   them they say what belongs on a machine, and nothing else does — **not** a comparison against
   `gh repo list`, which that rule's clause 4 forbids outright as the proxy that dragged the
   discontinued `trope` back onto a disk.
2. **A clone's presence is residue, not evidence that a decision was reversed.** It is far more
   likely to predate the decision, or to come from a sync that did not know about it, than to
   record a change of mind. Before concluding anything about where a clone came from, read its
   reflog: a fresh clone opens with `clone: from …`, a survivor does not.
## wlc-utils belongs on no machine, and its stub set is frozen

**wlc-utils is not in the roster**, so under `gitrepos_setup_rule` no machine clones it — Ben's
decision, 2026-08-22, reaffirmed 2026-08-31 as the general rule that **an evacuated repo does not
appear in `GitRepos`**. **The repo itself is alive** — `bdenckla/wlc-utils` is the redirect host
for `bdenckla.github.io/wlc-utils/<path>`, and only the clone is unwanted. Nothing routine wants
one: its 93 issues are read and written with `gh --repo bdenckla/wlc-utils`, which needs no
checkout (`py/github_issue_edit.py`); its site deploys from the remote by its own `pages.yml`; and no
test here resolves that sibling.

**The worked case for reading a reflog before believing a clone's story.** A machine surveyed on
2026-08-31 held a full 97.4 MB clone, and an earlier version of this section had read a clone
found that day as freshly re-cloned by an ad-hoc sweep, then predicted recurrence from that. The
reflog said otherwise: exactly one `clone:` entry, dated **2024-02-20**, running unbroken to a
`pull --ff-only` that morning — so on that machine the clone had been present continuously since
2024, and the sweep had *pulled* it rather than cloned it. The prediction was built on one
machine's disk standing for every machine's. The clone was removed 2026-08-31, along with
al-hatorah's and masorah-books', on the evacuated-repos rule above.

**Only explicitly selected redirect-host work wants a clone.**
`py/main_redirect_stubs.py build --repo wlc-utils --publish`, and
`check --repo wlc-utils` with no `--dir`, reach `py/redirect_stubs/stubs.py`'s
`source_pages_dir`. Every redirect command requires `--repo`; table order never chooses a
missing source clone. **Nothing schedules the program**: it is in no pipeline — `py/main_0_mega.py` and
`py/pipeline_graph/pipeline_graph_spec.py` never name it — and the one check that runs all the
time, `py/tests/test_redirect_manifest.py`, was hoisted into the suite precisely because it
needs no clone. It raises with the command that fixes it:

```powershell
git clone --depth 1 https://github.com/bdenckla/wlc-utils.git C:/Users/BenDe/GitRepos/wlc-utils
```

**The stub set is frozen at `in/wlc_redirect_pages.json`, the 154 URLs wlc-utils published at the
2026-08-17 move, and it can only shrink.** Until 2026-08-22 both subcommands derived it from the
live `git ls-files gh-pages/wlc`, which anchored the lint to the wrong set: a page published
*here* after the move never had a wlc-utils URL and is cited as a MAM-basics one, so it earns no
stub — but the derivation would have reported the first such page as an old URL about to 404. The
two sets coincided only because nothing had been added under `gh-pages/wlc/` since `f99996f`
(2026-08-12). So a publish is needed only if one of those 154 pages is **renamed or dropped**,
which breaks its stub; `py/tests/test_redirect_manifest.py` is the half of that lint needing
no clone, and it fires here.

**`../wlc-utils` was dropped from `all-repos.code-workspace` in the same commit, 20 folders to
19** — not tidying: `py/repo_util/repo_selection.py`'s `load_workspace_repo_dirs` raises
`FileNotFoundError` on any listed folder that is not on disk, and it runs before *every* action,
so a stale entry would kill `--run-black`, `--clean-worktrees` and the standards checks alike, not
just the part that names wlc-utils. That is the same three-step the frozen repos took on
2026-08-07 (move out, drop from the workspace file, record it).
## MAM-OSIS belongs on no machine except for explicit stub publication

Ben's decision, 2026-09-10: the completed Phase 5 lane of
`doc/PLAN-evacuate-five-MAM-products.md` makes MAM-OSIS a local product under
`MAM-OSIS/`, with published documentation under `gh-pages/MAM-OSIS/`. The source
clone is absent from both workspace rosters and `repo_visibility`; under
`gitrepos_setup_rule`, no machine should restore it during setup or maintenance.
A surviving clone is residue to inspect for recoverable work before recycling.
No `frozen_repos` or `repos_to_keep_absent` entry is needed. The unarchived
`bdenckla/MAM-OSIS` repository remains the Pages redirect host and preserves its
history; new product issues belong in MAM-basics.

The frozen legacy set is the single `index.html` in
`in/mam_osis_redirect_pages.json`. Production and the canonical suite run without a
source clone. (This sentence also named "the independent MAM-simple OSIS example" until
2026-09-12, when that example was retired along with the Sefaria one.) Keep the redirect-only
MAM-OSIS declaration in `py/tests/test_sibling_reach.py`: explicit future stub
publication still requires a temporary source host. Only when that work is selected:

```powershell
git clone --depth 1 https://github.com/bdenckla/MAM-OSIS.git C:/Users/BenDe/GitRepos/MAM-OSIS
```

From MAM-basics, run `py/main_redirect_stubs.py build --repo MAM-OSIS --publish`
and `check --repo MAM-OSIS`, commit and push the host changes, verify the source
Pages deployment, then safety-check and recycle the temporary clone again. Keep
the clone out of the workspace rosters. A local preview needs no clone: use
`build --repo MAM-OSIS --out <scratch-directory>` and
`check --repo MAM-OSIS --dir <scratch-directory>`.

## Taamey_D's decided disposition is an unarchived redirect, release, and issue host

Ben's 2026-09-16 evacuation plan keeps `bdenckla/Taamey_D` public and unarchived. Its
historical tags, releases, release assets, and issues remain at their original URLs. The
maintained documentation and downloads live in hbofonts; the one legacy HTML URL maps
from `index.html` to `https://bdenckla.github.io/hbofonts/Taamey_D.html`. The legacy
stylesheet and four WOFF2 files remain byte-for-byte static assets in the source host's
`docs/` tree rather than redirect-manifest entries.

The frozen mapping is `in/taamey_d_redirect_pages.json`. MAM-basics' redirect row names
hbofonts' `gh-pages/` as the maintained target and Taamey_D's `docs/` as the source
published directory. Phase 2 of the evacuation deliberately retains Taamey_D in
`all-repos.code-workspace`, `repo_visibility`, and `vendoring_policy.json` until the
source host is committed and deployed in Phase 3. Phase 4 removes those routine-clone
entries; after Phase 4, a Taamey_D clone belongs on no machine.

After Phase 4, only explicitly selected redirect-host work wants a temporary clone:

```powershell
git clone --depth 1 https://github.com/bdenckla/Taamey_D.git C:/Users/BenDe/GitRepos/Taamey_D
```

From MAM-basics, run `py/main_redirect_stubs.py build --repo Taamey_D --publish` and
`check --repo Taamey_D`, commit and push the host changes, verify the source Pages
deployment, then safety-check and recycle the temporary clone again. A local preview
needs no source clone: use `build --repo Taamey_D --out <scratch-directory>` and
`check --repo Taamey_D --dir <scratch-directory>`.

## codex-index-aleppo is a redirect host

**codex-index-aleppo is not in the roster**, so `gitrepos_setup_rule` does not put a clone on
any machine. Phase 2 of
`doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md` moved the live data to
`aleppo/` and its published pages to `gh-pages/aleppo/` on 2026-09-04. The source repository
stays live only as the generated-stub host for its former three Pages URLs. The frozen manifest is
`in/codex_index_aleppo_redirect_pages.json`, and `py/tests/test_redirect_manifest.py` checks it
without a clone. The source tracker has no open issues; qualified citations of its closed issues
remain source-tracker citations, while new public-side issues belong in MAM-basics.
## Cambridge 1753 data is local under `cam1753/`

Ben's decision, 2026-09-04: `codex-index-cam1753` belongs on no machine. Its archived GitHub
history remains, but its live data is `cam1753/`, its programs are under `py/`, and the MAM
word-sequence ground truth is `MAM-simple/xml-vtrad-mam/`. The fourteen source spreads are tracked;
`cam1753-pages/` is ignored output that `py/main_cam1753_split_spreads.py` regenerates for an
editor or crop task. The old clone left `all-repos.code-workspace` and
`in/repo_maintenance_policy.json`'s `repo_visibility` map in the same completed lane: a missing
workspace entry is therefore a decision, not a clone failure. The archived source tracker has no
open issues; qualified citations of its closed issues remain source-tracker citations, while new
public-side issues belong in MAM-basics.

The `../wlc-utils` paths in `doc/`'s plans are execution records of what was true when each phase
ran, and are left as written — the answer Ben chose for al-hatorah's and masorah-books' stale
citations too.
## diffable-pointed-hebrew's only data is `in/diffable-pointed-hebrew-short-name-overrides.json`

The completed Phase 4 lane of
`doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md` moved the former
diffable-pointed-hebrew product's samples and its nine short Unicode-name assignments under
`diffable-pointed-hebrew/`. Ben's decision of 2026-09-13 removed that directory: the nine
assignments moved to `in/diffable-pointed-hebrew-short-name-overrides.json`, and the two sample
pairs, a historical output, the README and the product's MIT `LICENSE` were deleted. The samples
were MAM text, which that licence could not cover, and the command's two remaining goldens are
the zarqa tables under `misc/zarqa-table-diff/`. Its command is `py/main_diffable_pointed_hebrew.py`, which uses
MAM-basics' maintained `mb_cmn` utilities plus the retained product data. The old source clone
is deliberately absent from `all-repos.code-workspace` and `repo_visibility`. The source
repository keeps its history as an archived dated breadcrumb. Ben
archived `bdenckla/diffable-pointed-hebrew` on 2026-09-04; its archive state was then confirmed
with `gh repo view --json isArchived,url`. The source tracker has no issues; new product work is
tracked in MAM-basics.
## holman-ketiv-qere belongs on no machine, and its redirect set is frozen

**holman-ketiv-qere is not in the roster**, so `gitrepos_setup_rule` does not put a clone on any
machine. Ben's decision, 2026-08-22, applies the evacuated-repository rule here: the source
repository stays alive at `bdenckla/holman-ketiv-qere` as the redirect host and issue tracker,
but its local clone is unwanted. The completed 2026-09-03 lane moved the public data and
generators to `holman/` in this repository, then removed the source clone after retiring its
clean detached review worktree.

Nothing in the ordinary suite reads `../holman-ketiv-qere`. The frozen six-page old URL set is
`in/holman_ketiv_qere_redirect_pages.json`, and `py/tests/test_redirect_manifest.py` checks it
without a source clone. If an old Holman page is renamed or dropped, temporarily re-create the
redirect host with:

```powershell
git clone --depth 1 https://github.com/bdenckla/holman-ketiv-qere.git C:/Users/BenDe/GitRepos/holman-ketiv-qere
```

Then publish and check the frozen stubs with `--repo holman-ketiv-qere`, and remove the temporary
clone again after the source repository's Pages deployment succeeds. `../holman-ketiv-qere` is
already absent from `all-repos.code-workspace`, so no workspace entry needs changing.
## UXLC-utils belongs on no machine, and its redirect set is frozen

**UXLC-utils is not in the roster**, so `gitrepos_setup_rule` does not put a clone on any machine.
Ben's 2026-09-03 evacuation moved the public data and generators to `uxlc/` and `gh-pages/uxlc/`
in this repository. The source repository remains alive at `bdenckla/UXLC-utils` as the redirect
host and issue tracker; source commit `2745c65` retains the deployed redirect stubs.

Nothing in the ordinary suite reads `../UXLC-utils`. The frozen 91-page old URL set is
`in/uxlc_utils_redirect_pages.json`, and `py/tests/test_redirect_manifest.py` checks the manifest
without a source clone. If an old UXLC page is renamed or dropped, temporarily re-create the
redirect host with:

```powershell
git clone --depth 1 https://github.com/bdenckla/UXLC-utils.git C:/Users/BenDe/GitRepos/UXLC-utils
```

Then publish and check the frozen stubs with `--repo UXLC-utils`, and remove the temporary clone
again after the source repository's Pages deployment succeeds. `../UXLC-utils` was removed from
`all-repos.code-workspace` before the primary clone was removed, so workspace sweeps do not name a
missing directory.
## codex-index-leningrad has been evacuated

**codex-index-leningrad is not in the roster.** Phase 1 of
`doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md` moved its
five retained files into `leningrad/`, repointed its Wikisource index generator to MAM-basics'
canonical `uxlc/data/lci_augrecs.json`, and archived the empty source repository on 2026-09-03.
The archived repository keeps its history and closed issue tracker; new public-side issues belong
in MAM-basics. No source Pages site or redirect manifest exists.

Nothing in the ordinary suite resolves a Leningrad sibling, and `leningrad/` is gone as well. It
held only a README and three crops Ben made, and Ben's decision of 2026-09-13 moved the crops,
with their evidence notes, into folders for the work each one serves:
`doc/meteg-after-silluq-snips/` and `doc/lam-2-3-akhla-snips/`, which took the Aleppo Codex,
Cambridge 1753 and other crops too. On Ben's decision
of 2026-09-10 the Wikisource index generator was removed, with the package and paths module it
used and its three generated files, since it "will never be run again"; phase 3 of
`doc/PLAN-mega-coverage.md` names every file removed. No Leningrad code remains, so
`py/repo_scopes.py` lists none.

Phase 5 on 2026-09-04 confirmed that the clean primary clone's `HEAD` and `origin/main` were both
`86f88c0`, and that `git worktree list` named only the primary checkout. The review forest was no
longer present, so the primary clone was moved to the Windows Recycle Bin. No Leningrad clone
belongs on a machine.
## There is no `wlc-koren-12th` repo

`~/GitRepos/wlc-koren-12th` was never a repo of its own. It was a **worktree of wlc-utils** on
branch `claude/koren-12th-site`, which is why it sat flat among the siblings and answered
`git remote -v` with `bdenckla/wlc-utils`; its copies of files such as
`py/accgram/poetic_ply_grammar.py` were the same files on an older branch, never duplicates to
reconcile or keep in sync. Repeated sessions read it as a twin repo and burned a turn
"reconciling" it — that is the whole reason for this note. Deleted 2026-07-27, along with the
fully-merged leftover branches `claude/koren-12th-site` and `claude/festive-napier-38d58d`, both
accepted by `git branch -d` (never `-D`), which is the record that nothing was lost. The only
place the name survives is old session transcripts under `~/.claude/projects/`, which is exactly
where the wrong conclusion kept being copied from.

**General lesson:** a directory sitting flat under `~/GitRepos` is not necessarily a repo. Run
`git -C <dir> rev-parse --git-common-dir` (or `git worktree list` from the repo you suspect)
before treating one as a peer whose files need syncing.

(Moved here from wlc-utils' `CLAUDE.md` on 2026-08-17, when Phase 10 of
`doc/PLAN-evacuate-the-rest-of-wlc-utils.md` shrank that file to redirect-host facts — the
disposition that plan's Phase 0 recorded for it. The note lives on because the transcripts do,
and because all wlc work now happens in this repo.)
