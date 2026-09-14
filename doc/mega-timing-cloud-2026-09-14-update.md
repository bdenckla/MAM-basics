# Updates to the 2026-09-14 record of a mega run in a cloud container

State: open, first entry 2026-09-14. Every entry here supplements
`doc/mega-timing-cloud-2026-09-14.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. Nothing here edits the document it supplements.

## 2026-09-14: the container's setup script failed on a path, and the runs were on the wrong Python

**The record's figures were all measured on Python 3.11.15, and the environment intends 3.13.**
Re-measured on 3.13 the same day in the same container, a mega run is **7.7% faster** and the
record's central comparison moves from 1.13 to **1.04**. The record's account of why the packages
had to be installed by hand is also incomplete. Both follow from one cause, which the record could
not see.

### What the record says, and what was actually wrong

The record's section 1 says, under the words "**The packages had to be installed, and the plan's
command for it does not work as written**", that
`python3 -m pip install -r requirements.txt` failed on a Debian-managed `packaging`, and its
environment table gives `python3 --version` as 3.11.15 with the note "**Python is 3.11.15, not the
3.13.12 Phase 2 expected**". Both statements are true as written and both mislead, because they
describe a workaround rather than the fault.

**The fault was the environment's setup script, whose output only Ben can see.** He quoted it on
2026-09-14:

```
Setup script failed with exit code 2.

Script output:
Using CPython 3.13.12 interpreter at: /usr/bin/python3.13
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
error: File not found: `requirements.txt`
```

**The cause is a working directory, exactly as Ben guessed when he asked whether "our assumption
that the cwd would be the MAM-basics (shallow) clone" was false. It is false.** The setup script
runs in `/home/user`, the parent of the clone, not in `/home/user/MAM-basics`. Four measurements
in the container establish it:

| What | Value |
|---|---|
| The virtual environment the script created | `/home/user/.venv`, from its relative `.venv` |
| That environment's Python | 3.13.12, and empty of every requirement |
| Everything in `/home/user` | `.venv` and `MAM-basics`, and nothing else |
| Where `requirements.txt` actually is | `/home/user/MAM-basics/requirements.txt` |

So the script selected `/usr/bin/python3.13`, which is installed in the container, built a 3.13.12
environment, and then looked for `requirements.txt` one directory above the file. It installed
nothing and exited 2.

**The Debian `packaging` conflict the record describes was a consequence, not the cause.** Because
the setup script had installed nothing, the session reached for the system interpreter, `python3`,
which is 3.11.15 and whose `site-packages` is managed by dpkg. That is where the unremovable
`packaging` 24.0 lives. **A run inside the 3.13 environment never meets it**: installing the
requirements there took **3.0 s** and exited 0.

```bash
uv pip install --python /home/user/.venv/bin/python -r /home/user/MAM-basics/requirements.txt
```

The fix to the setup script is a path, nothing more: give it the clone's directory, or name
`MAM-basics/requirements.txt`. **The record's advice to prefer a virtual environment stands and its
reasoning was right for the wrong reason** — the setup script was already making one.

**Ben fixed the setup script on 2026-09-14**, reporting so in the session that wrote this entry.
The fix is not verified here and could not be: the container this entry was written in was built
before it, and its failed environment at `/home/user/.venv` is the evidence of the fault rather
than of the repair. **The next cloud session is what confirms it**, and confirms it by finding a
populated 3.13 environment before it runs anything, which step 3 of `doc/PLAN-mega-speedup.md`'s
Phase 2 now requires. A session that finds one needs none of the workaround above.

### The 3.13 re-measurement, and every figure it moves

Two further full runs were made in the same container with
`/home/user/.venv/bin/python py/main_0_mega.py`, after the requirements were installed there. Both
exited 0 and ran all 55 steps, with the same one cloud-skipped step, the same 14 skipped SVG
renders, and the same four shallow-clone file changes, none committed. The two agree to within
0.6 s on every step, as the record's 3.11 pair did.

| | Wall (s) | The mega's own step-loop total (s) |
|---|---:|---:|
| 3.13 run 1 | 233.4 | 230.0 |
| 3.13 run 2 | 232.0 | 229.4 |

**Python 3.13 runs the mega 7.7% faster than 3.11 on identical hardware**, 229.8 s against 248.9 s,
comparing medians of the warm runs of each. **One step is over half of that difference**:
`wlc-json-and-unicode` falls from 32.8 s to 22.6 s, a ratio of 0.69.

**The record's headline comparison changes, and the direction of its conclusion with it.** Over
the same 52 steps that ran to completion in both places:

| Compared with | Record, on 3.11 | Re-measured on 3.13 |
|---|---:|---:|
| Ben pinned to logical processors 0-11 | 235.0 s, ratio **1.13** | 216.3 s, ratio **1.04** |
| Ben unpinned, run 1 of the dated record | 235.0 s, ratio **1.01** | 216.3 s, ratio **0.93** |
| Per-step ratio, median | 1.23 | 1.12 |
| Steps worth at least 2 s on Ben's machine, aggregate | 1.11 | 1.03 |

So **a cloud container is within a few percent of Ben's pinned machine, not 13% behind it**, and it
is faster than his machine unpinned. The record's summary item 3, which reads "the cloud takes
235.0 s against Ben's pinned 207.6 s, a ratio of **1.13**", should be read as 216.3 s and 1.04; its
item 4, "**Against Ben's *unpinned* run the cloud is a dead heat**", understates the container,
which is ahead by 7%.

**The record's section 5 names the wrong step first.** It says "**`wlc-json-and-unicode` is the one
to look at first**", on a ratio of 1.78 that was the worst of any large step. On 3.13 that ratio is
**1.23** and the step ranks sixth, so most of what that section attributed to the container was the
interpreter. The same section's suggestion that "the accgram scanners suit the i5-13500T better
than this Xeon" weakens for the same reason: `accgram-generate-html` moves from 1.61 to 1.38,
`accgram-run-prose` from 1.57 to 1.35, and `accgram-grammaticality` from 1.60 to 1.15. The largest
remaining ratios on 3.13 are `diff-wsgo` and `accgram-generate-html`, both 1.38.

**What does not change.** Every conclusion that does not rest on the interpreter stands as written:
that normalizing for the cloud's skips matters, and that
`accgram-survey-post-stress-meteg` is worth 40.9 s on Ben's machine; that step-by-step comparison
rather than total-to-total is the whole of the normalization needed; that the container is far more
repeatable than Ben's machine; that a first run in a fresh container is a cold-cache run; and the
graft-boundary finding of the record's section 7, which reproduced identically on 3.13.

**A caveat this entry does not resolve.** `py/mb_cmn/file_io.py` says its `json.dumps` choice was
made for "the Python this repo runs (3.13)", where `json.dump` encodes in pure Python and
`json.dumps` reaches the C encoder. Whether 3.11 behaves differently was not tested; Ben declined
that test on 2026-09-14. It is a plausible part of the 3.11-to-3.13 difference in the
JSON-heavy steps and is recorded as unmeasured rather than claimed.

## 2026-09-14: section 7's graft-boundary finding has another cause, and has been fixed

**The finding has been fixed by `b5dd2ffb`**, which labels unpinned-latest by the git tree id of
`MAM-parsed/plus` and gives it no date, by Ben's choice on 2026-09-14. That id is the same in every
clone, shallow or full, so a shallow clone no longer changes `unpinned-latest.json` or
`unpinned-latest.html`. **The fix is verified in a local depth-50 clone and not yet in a cloud
container**, where a mega run confirms it by leaving both files unchanged. The rest of section 7's
finding went with the `vendoring-audit` step, which `25bcabf6` removed from the mega the same day,
so a cloud mega run should now leave the tree clean.

Measured on 2026-09-14, the record's account of the mechanism is wrong in two places, which the next
two subsections correct.

### A boundary commit looks added because `.git/shallow` lists it, not because its parent is absent

Section 7 says "**A shallow clone's graft boundaries have no parent object, so git shows every file
in such a commit as added**", and item 4 of section 8 says of `d3ab7cf`'s absent parent `eb79e61`
that it "is what makes git treat every file in it as added". **The absent parent is not the
cause.** A depth-50 clone of `89f10bb4` matches the three figures the record gives for the
container: 153 commits, three boundaries, and `d3ab7cf` the newest of them. In that clone
`git log --full-history -1 -- MAM-parsed/plus` returned `d3ab7cf`. With `eb79e61` then fetched into
the clone, the walk still returned `d3ab7cf`, because `.git/shallow` still listed it: git treats
every commit that file lists as having no parents, whatever objects are present. After
`git fetch --unshallow` emptied the list, the walk returned `73c6b113`, the answer a full clone
gives.

### A real change inside the window does not stop the walk

Section 7 explains that the 2026-09-11 container escaped because "3 commits inside its 221-commit
window genuinely touched `MAM-parsed/plus`, so its walk stopped at a real one before reaching a
graft boundary". **A real change inside the window is not enough.** The walk lists commits newest
first and returns the first that seems to change the path, so it returns a boundary commit whenever
one is newer than the last real change, wherever that change lies. In clones of `89f10bb4` at seven
depths, every depth below 150 returned a boundary, including depths 50, 75 and 100, whose windows
all contain `73c6b113`:

| Depth | Commits in window | Boundaries | The walk returned | Listed in `.git/shallow` | Window holds `73c6b113` |
|---:|---:|---:|---|---|---|
| 1 | 1 | 1 | `89f10bb`, 2026-09-14 11:17 | yes | no |
| 10 | 11 | 2 | `797709e`, 2026-09-13 14:25 | yes | no |
| 25 | 43 | 2 | `5e7715d`, 2026-09-13 11:11 | yes | no |
| 50 | 153 | 3 | `d3ab7cf`, 2026-09-12 21:05 | yes | yes |
| 75 | 305 | 6 | `e1e8e28`, 2026-09-12 17:51 | yes | yes |
| 100 | 442 | 5 | `3f962e6`, 2026-09-11 18:02 | yes | yes |
| 150 | 639 | 2 | `73c6b113`, 2026-09-11 15:55 | no | yes |

The times are committer times, every one at -04:00. At depth 100 the boundary `3f962e6` was
committed about two hours after `73c6b113`, and that order decided the answer, not what the window
held. So what let the 2026-09-11 container's walk stop at a real change, as section 7 reports, was
that none of its boundaries was newer than that change, not that its window held real changes.

### How the fix was verified

1. **Before the fix**, in an ordinary depth-50 clone of `main` at `c1af93cb` (121 commits, five
   boundaries), the kind of clone a cloud container has rather than a partial one, the walk returned
   the boundary `217fd90`. Running `py/main_diff.py mpplus` there changed the two unpinned-latest
   files and nothing else: `new_rev` became `217fd90`'s full hash, and the title and the End date
   became 2026-09-12, where the committed files named `73c6b113` and 2026-09-11.
2. **After the fix**, the same clone moved to `b5dd2ffb` held 117 commits and nine boundaries, and
   the old walk would still have returned a boundary, `c141f54`, so the check could have failed.
   Running `py/main_diff.py mpplus` there left `git status --porcelain` empty.
3. **On Ben's machine**, a full mega run on `b5dd2ffb` left no tracked file changed.

### Commands behind the figures

1. **The depth table and the parent-object test.** Bare blobless clones of MAM-basics' primary clone
   at `89f10bb437d60af3279a72c72be9b6aa866c5bf8`, made in a scratch directory by a throwaway script:
   `git init --bare`; `core.repositoryformatversion 1` and `extensions.partialClone origin`; a
   `file://` remote with `remote.origin.promisor true`, `remote.origin.partialCloneFilter blob:none`
   and the `uploadpack` override `git -c uploadpack.allowFilter=true -c
   uploadpack.allowAnySHA1InWant=true upload-pack`; then `git fetch --depth=<d> --filter=blob:none
   origin <that commit>`. In each clone, `git rev-list --count` gives the window, the `shallow` file
   the boundaries, `git log --full-history -1 --format="%H %ci" <that commit> -- MAM-parsed/plus`
   the walk's answer, and `git rev-list` whether `73c6b113` is in the window. `eb79e61` was fetched
   by `git cat-file -e`, which git 2.43 answers by fetching a missing object from a promisor remote,
   and its presence before and after was read with
   `git cat-file --batch-all-objects --batch-check`, which fetches nothing.
2. **The before-and-after clones.**
   `git clone --depth 50 --sparse file:///C:/Users/BenDe/GitRepos/MAM-basics <scratch directory>`
   and `git sparse-checkout add py MAM-parsed/historical gh-pages/MAM-with-doc/change-log`, then the
   primary clone's interpreter running `py/main_diff.py mpplus` from the clone's root. For the
   second run, `git restore` of the change log, `git fetch --depth=50 origin main` and
   `git checkout --detach origin/main`.
3. **The 2.6 MiB that `resolve`'s docstring in `py/mb_diff_mpu/mpplus_revisions.py` gives for the
   option not taken**, fetching the history a shallow clone lacks without file contents: the growth
   of `size-pack` in `git count-objects -v`, from 356 KiB to 3,033 KiB, across
   `git fetch --unshallow --filter=blob:none origin <that commit>` in a fresh blobless depth-50
   clone of `89f10bb4`.
