# Updates to the mega-pipeline review's public finding disposition companion

State: open, first entries 2026-09-12. Every entry here corrects or supplements
`doc/mega-pipeline-review-findings-public-2026-09-01.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction to one goes in a sibling file named `<stem>-update.md`. This file is that sibling
for the 2026-09-01 companion. Nothing here edits the document it corrects.

## The atomicity findings have a neighbour in MAM-basics #278

**Thirteen** of the companion's findings are about atomicity, and all thirteen are recorded there
as `Open — queued`: `MP01-03`, `MP02-07`, `MP03-04`, `MP04-03`, `MP05-03`, `MP05-04`, `MP06-02`,
`MP06-04`, `MP07-04`, `MP08-06`, `MP09-03`, `MP11-01` and `MP12-05`. Twelve are **P2**; `MP06-02`,
a live bot failure leaving partial remote publication and stale local state, is the one **P1**.

Four carry the companion's `atomicity root cause` tag — `MP01-03`, `MP02-07`, `MP03-04` and
`MP06-02` — and that tag is not a reliable index of the subject: nine atomicity findings lack it,
and `MP12-05` ("Four vendoring outputs can be mixed or truncated after failure") states the problem
without using any of the words *atomic*, *transaction* or *incremental*, so a text search for those
misses it. Anyone counting these should count the thirteen above rather than re-derive them.

**#278 is about the same unit of concern and a different failure**, and the two should be read
together. Those thirteen are about a **crash** leaving a half-written set: each individual file is
replaced atomically through `mb_cmn/file_io.py`'s `with_tmp_openw` and `os.replace`, and what is
missing is a transaction spanning the set. `MP11-01`'s Phase 11 write-up says so in as many words
while reporting the defect, and demonstrates it with a `.novc` probe that let one page's writer
finish and made the other raise. #278 is about a **successful** run leaving a wrong set: a writer
that silently stopped running, or an output renamed so that a file under the old name goes on
serving stale content. Its check — `written_this_run == intended == on_disk` — would not fix any of
the thirteen, and a set-level transaction would not catch either failure #278 names.

Ben asked for the cross-reference on 2026-09-12, having raised the connection himself. #278's body
carries the other direction.

## `Open — queued` is a 2026-09-01 snapshot, and by 2026-09-12 it no longer sorts the list

Re-measured 2026-09-12 by parsing the companion's own finding index: of its **85** findings, **81
are `Open — queued`** — 8 P1, 55 P2, 18 P3 — against 2 `Fixed in remediation`, 1 `Already fixed
before Phase 13` and 1 `Fixed in closeout`. Sixty-three of the 81 name no root cause; the rest
name ten, of which `atomicity` is the largest at four.

**Three remediation waves ran, all on 2026-09-02, and all three were `MP02-0x` work**:
wave 1 for `MP02-02` and `MP02-03`, wave 2 for `MP02-01`, wave 3 the architectural severing of the
dated WLC private dependency. `doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md` records all
three, and twice records that `MP02-07` batch atomicity stayed outside the wave. **No fourth wave
followed.** The later `doc/PLAN-remediate-review-findings-*.md` files belong to the separate
periodic review series of 2026-09-07, 2026-09-08 and 2026-09-09, not to this one.

**So the 81 were never revisited as a list — but some of them have since been fixed by work that
arose independently and never looked at this file.** Two confirmed, both fixed by `7b3bed38` of
2026-09-09, "Pin Graphviz at 16.0.0, and make a missing dot fail instead of skip":

- **`MP13-01`**, unpinned Graphviz version drift rewriting all 12 generated call-graph SVGs. Now
  `py/mb_cmn/graphviz_pin.py` pins the full version stamp bidirectionally, with
  `py/tests/test_graphviz_version_pin.py` beside it.
- **`MP03-02`**, a missing Graphviz silently preserving stale SVGs. The commit's own title says it
  now fails instead of skipping.

And others are still exactly as reported. The three terminology findings that name the reader-facing
spelling `legarmeih` — `MP02-08`, `MP04-09` and `MP06-07` — were re-checked on 2026-09-12 and that
spelling stands in **17** tracked files under `gh-pages/` and `out/`.

**The problem this creates is not that findings are open; it is that `Open — queued` no longer
distinguishes the two cases.** A reader cannot tell a finding that is still real from one that was
quietly fixed eight days later without re-verifying it against current code, and there are 81 of
them. Neither kind is wrong in the companion: that file states what was true on 2026-09-01, which
is what a dated document is for. What is missing is anything that says what is true now.

## Nothing here changes a GitHub issue's state

No issue was opened, closed or relabelled for any of the above. #278 was created on 2026-09-12 as
an `enhancement`, and it is a new proposal rather than a disposition of any `MP` finding.
