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
