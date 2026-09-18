# Updates to the 2026-09-11 record of where a mega run spends its time

State: open, first entry 2026-09-14. Every entry here supplements `doc/mega-timing-2026-09-11.md`,
which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later addition goes in a sibling file named `<stem>-update.md`. This file is
that sibling for `doc/mega-timing-2026-09-11.md`. Nothing here edits the document it supplements.

## 2026-09-14: the status of §7's proposals is kept in `doc/PLAN-mega-speedup.md`

§7, "Speedups proposed for Ben, largest first", describes its twelve proposals as they stood on
2026-09-11. Their current status is kept in `doc/PLAN-mega-speedup.md`, which also records how the
mega has changed since the runs measured here, and plans new measurements. Five of the 60 steps
timed here have since left the mega: `near-aleppo-census` on 2026-09-11, and `mam4sef-and-ajf`,
`mam-osis`, `vendored-mam4sef` and `vendored-mam-osis` on 2026-09-12.

## 2026-09-14: the current mega on a second machine is timed in `doc/mega-timing-laptop-2026-09-14.md`

That record times four full runs of the mega's 55 steps on `LAPTOP-DBLE8UKA`, a Surface Laptop 4
with an AMD Ryzen 7 of 16 logical processors, all of one kind. The step loop took a median of
262.9 s. Outside the first run, every step of 5 s or more stayed within 4% of its fastest time,
against the up-to-2.6-times variation that §1 here measured on the i5-13500T. It is a different
machine and later code, so its figures are not a re-measurement of this record's.

## 2026-09-16: `accgram-run-prose` scans prose verses, not prose books

In section 4 item 7, replace only `prose books` with `prose verses`; the remainder of the
entry—“19,531 verse bodies, with the prose scanner and the PLY grammar, and writes
`out/accgram/prose/`”—continues unchanged.
