# Bounded MAM-basics hourly review, 2026-11-18 UTC

State: completed 2026-11-18; review only

Exact endpoint `f996f75630e19241d055215450165bd1da5fed80` -> `333f8e899688ff9a34f72ca3cb2c19d4a5bdac5c` (28 paths).
Only an owned isolated committed checkout was used with its home interpreter. Local
slots/processes were clear at admission; checks were sequential. Cross-machine ownership
is unverified. No sibling inputs required. [Commands, logs, helpers and evidence](review-hourly-2026-11-18-333f8e89-basics-evidence.zip).

Independent maintained commands (owning /workspace/MAM-basics/.venv/bin/python,
isolated source root):

| Command | Exit; wall time |
| --- | --- |
| git diff --check BASE HEAD | 0; 1.261679 s |
| -m black --check (seven changed Python paths) | 0; 0.467301 s |
| py/main_edition_transcription.py build koren_dt_elyon --derive-only | 0; 0.241244 s |
| py/main_accgram.py run-printed-decalogue | 0; 0.542713 s |
| py/main_accgram.py generate-html-printed-decalogue-koren | 0; 0.945300 s |
| py/main_accgram.py generate-html-printed-decalogue-simanim | 0; 0.656984 s |
| py/main_accgram.py generate-html-maqaf-nonfinal-accents | 0; 5.396520 s |
| py/main_authored.py gen-site --trust-surveys | 0; 5.568908 s |
| py/main_test.py (12 relevant modules) -q -ra | 0; 87.271662 s |

Actual selection: edition_transcriptions, printed_decalogue_koren, printed_decalogue_simanim,
printed_decalogue_page, maqaf_nonfinal_accents_page, transliterations, prose_conventions,
prose_mark_order, shared_html_styles, site_links_relative, site_index_links and
h_dot_below_nfc (test_*.py under py/tests). **228 passed, 6 skipped in 87.01 s**. The six
skips are intentional diverging-transcription controls, explicitly named in the raw log.
All maintained stages leave exact committed output and empty normal status/diffs.

The 895-assertion preservation helper (exit 0, 0.946207 s tool wall) checks the exact one-line
Koren JSON correction and its corrected_from provenance. All 125 stress records retain every
field except prose notes (74 records); all 93 ordered rows keep filter membership, pointed
forms and crop paths. All 8 Simanim verdict rows retain labels/pages/strands and final two
cells while five columns become three. WLC executable CSS is identical after removing comments.
All 433 local href/src occurrences and applicable fragments resolve. The unchanged stored
survey supports no MAM-prose same-accent pair, one UXLC and two WLC pairs, and no two mun
atoms in MAM's two genres. This is committed-data consistency, not a new census or scan audit.

A separate exit 0 probe (0.168161 s tool wall) verifies the derived JSON changes only the
koren_dt_elyon transcription; the other 11 transcriptions and all top-level values remain
exact. It keeps nine chanted verses and 1 ungrammatical verse, now two mun-mun compounds. One
existing crop reference is intentionally added for the fourth maqaf case, with unchanged
PNG bytes and bounded overlay geometry. Original reviewer schema/image assumptions and
their failures are retained in the archive, with the correction explained in method-note.md.

Offline HTML: stress exits 1 (0.913042 s), four historical orphan crops; WLC exits 1
(1.227101 s), ten historical orphan images and one XML file-type finding. All 15 file blobs
and the checker are unchanged; these are retained failures, not clean passes. CSS notices
remain informational. A provisional last-rung prose concern was withdrawn against the
page's explicit maqaf/conjunctive comparison rule; no consequential introduced defect
or repair established. No source/Hebrew/editorial choice changed.

Owner full-suite 1,497-pass/6-skip/90-subtest and focused 206/230 results, native/source/crop conclusions
and approval history remain attributed; not added to our counts. No full mega/suite,
browser/Windows, original scans, external source requests, research or font work ran.
The former Koren correction decision is now owner-recorded approved, not still pending.

Frozen sources: [Koren comparison](https://github.com/bdenckla/MAM-basics/blob/333f8e899688ff9a34f72ca3cb2c19d4a5bdac5c/py/accgram/printed_decalogue_koren_page.py), [transcription](https://github.com/bdenckla/MAM-basics/blob/333f8e899688ff9a34f72ca3cb2c19d4a5bdac5c/in/accgram/edition_transcriptions/koren_dt_elyon.json), [stress generator](https://github.com/bdenckla/MAM-basics/blob/333f8e899688ff9a34f72ca3cb2c19d4a5bdac5c/py/author_site/stress_helper_comparison.py).

Receipt parent `b3f8139d7bb63cdcd27d74486e3ae685839f824e` and all earlier status bytes/finished receipts are preserved.
Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested stays November 18 nightly
`8c2c3378487c9587659cd0b4a8f3db4690dbcf08`. All older pending windows and source/browser/native/font limitations remain.
Only the established isolated receipt branch changes; no main/shared integration, PR,
deployment/dispatch, schedule or configuration changes. Remote parent/scope/bytes and
owned-worktree/slot cleanup are verified at closeout.
