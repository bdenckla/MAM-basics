# Updates to the 2026-09-14 Surface Laptop mega timing record

State: open, first entry 2026-09-18. Every entry here supplements
`doc/mega-timing-laptop-2026-09-14.md`, whose substantive wording is left exactly as written apart
from the mechanically required paragraph join and update pointer.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. The paragraph join and update pointer are the only edits to the document this
file supplements; its substantive wording remains unchanged.

## 2026-09-18: the unlabelled clock reads imply an offset of `-04:00`

The clock read in the sentence beginning “The runs ran from 15:20 to 15:46” and the run table's
`Started` column are unlabelled. The record's checkout associations and commit chronology imply
an offset of `-04:00`: run 1 ended at 15:25:25.9 on the record's clock before `823be50b` was
committed at 2026-09-14T15:26:31-04:00, and run 2 began at 15:29:35 after `8834ce4b` was
committed at 2026-09-14T15:27:44-04:00. Those constraints bracket the clock's offset between
approximately -04:01:05 and -03:58:09, making `-04:00` the only ordinary civil offset in the
interval. The offset is inferred; the record names no zone.
