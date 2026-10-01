# Updates to the HBCE Psalms comparison receipt of 2026-09-26

State: open, first entry 2026-09-30.

Every entry here corrects or supplements `doc/hbce-psalms-vs-mam-2026-09-26.md`, which is left
exactly as written. Ben's decision of 2026-09-11 (D12): a finished dated document is left as
written, and a correction or later fact goes in its single update.

## Two defects found by the 2026-09-29 review, 2026-09-30

Recorded by Claude on 2026-09-30, New York time, under the approved remediation plan for the
2026-09-29 dual-agent review (its finding 21).

1. **Two summary sections share one heading.** `hbce-psalms/out/compare_summary.txt` heads both of
   its Leningrad comparisons "=== ML vs MAM (Leningrad) ===". The first covers the 170 verses of
   Psalms 15:1–25:1 and writes `compare_ML_range.tsv`; the second covers all 801 verses of HBCE's
   Leningrad transcription, Psalms 1:1–51:21, and writes `compare_ML.tsv`.
   `py/hbce_psalms/compare.py` writes the heading without the range. `compare_summary.txt` and
   `compare.py` stay unchanged until the HBCE work resumes and reruns the comparison, since a
   change to that hand-run program would owe the rerun that Ben's frozen-record decision of
   2026-09-26 does not waive.
2. **The receipt cites more than its opening says.** "Everything it cites is in `hbce-psalms/`,
   `py/hbce_psalms/` and `py/main_hbce_psalms.py`" is too broad: the receipt also cites
   `DATA-LICENSES.md`, `MAM-simple/xml-vtrad-mam/Ps.xml`, `MAM-parsed/plus/D1-Psalms.json`,
   `explicit_xataf.extract.find_docnote_tmpls`, `in/mam-ws-intro/`, `in/UXLC-39/Psalms.xml`,
   `in/meteg_after_silluq_cases.json`, `aleppo/line-breaks/`, `py/tests/test_transliterations.py`,
   `py/tests/test_prose_conventions.py`, `py/tests/test_prose_mark_order.py` and
   `py/main_verse_links.py`.
