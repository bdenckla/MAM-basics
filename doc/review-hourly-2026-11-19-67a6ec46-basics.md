# Bounded MAM-basics refresh review, 2026-11-19

State: completed 2026-11-19; review only

Exact endpoint `54aaab9300e1559c891275a547dd516a84207354` -> `67a6ec467ba0cf078e9790760a2ee8452f722382`. 24 maintained tests pass; candidate parser reproduces all 24 groups; 16 text changes / five notes / 21 rendered rows and 617 local links reconcile. Narrow generation leaves committed products exact. No consequential introduced defect.

The complete endpoint has **six commits / 152 paths**. Independent data joins find **20 changed raw chapters/revision records, 16 text-change verses (13 helper additions, two moves, one removal), and five separate note changes**. All other source metadata is preserved and both old/new captured chapter hashes agree locally. This does not verify live revision freshness, editor identity or the reported request count. Actual candidate parsing from committed raw arrays reproduces **all 24 production JSON groups byte for byte**, with maintained parser/plus validation; this is not a claim to have rerun the owner's 59-test command.

MAM-simple changes at exactly the 16 verses, only those helper code points. Each supported BHS/Sefaria versification has nine matching changes. Near-Aleppo's 16 source-edit rows remain byte-exact; its only changed rows are the five notes. The two changed ledger rows remain reviewed/recast: Numbers 11:8 uses candidate clause2, keeping clauses0/1 as MAM context; Jeremiah11:10 keeps candidate1 and context0/2. Other 1,556 ledger rows remain exact, and maintained fresh census/build/note-review checks pass through the selected tests. No semantic interpretation or source decision is made.

Published MAM-with-doc has exactly21 changed verse rows and **617 resolving local href/src occurrences**. Phonetic MAM has exactly16 changed verses, Hebrew changes confined to helper marks;15 transcription records change and 2Samuel13:20's transcription stays exact. Word inventory removes16/adds7; both post-stress candidate and one-token-bucket counters grow by7, with other fields exact. Logs retain12 old entries and add the exact16 endpoint entries (28 total); named historical reports are byte-exact, and the maintained currentness guard passes. Exempt Sefaria/OSIS/morphhb products, Taamey-D, special-page mirror, explicit-xataf, Yeivin and stress-helper inputs/pages remain untouched. The14 pending stress-helper presentations remain an owner decision, not a new issue from this screen.

The new qere-without-ketiv hover is one shared span. Frozen-function differential checking covers24 plain-text/name cases, escaping, exact surrounding markup/Hebrew and actual shared title/CSS. The entire page matches after only removing the span and ignoring wrapping whitespace. Raw title text intentionally adds the shared Hebrew sigil; visible Hebrew stays exact. **24 repository tests pass in78.57s (79.257614s wall), no skips**. Final data/published probes pass2 tests in12.08s; the hover probe passed in the earlier mixed draft command. Four draft checker versions/traces remain with their corrections; no product command was repeated for them.

Owner-recorded downloads, first mega stop/resume, final mega/profile and source/editorial conclusions remain attributed. The tip's full-suite statement is a promise conditional on success, not an execution result available to this reviewer. No broad mega/full suite or fresh download ran here. Next independent broad coverage stays with nightly; source/browser/scan/research/rights limits are unchanged.

Actual maintained commands run from `/workspace/scratch/hourly-20261119-refresh/basics-source`, using home interpreters, sequentially:

| Command | Exit | Wall seconds |
| --- | ---: | ---: |
| `git diff --check 54aaab9300e1559c891275a547dd516a84207354 67a6ec467ba0cf078e9790760a2ee8452f722382` | 0 | 0.948533 |
| `/workspace/MAM-basics/.venv/bin/python -m black --check py/near_aleppo/foi_qere_without_ketiv.py` | 0 | 0.452838 |
| `/workspace/MAM-basics/.venv/bin/python py/main_parse.py ws-products --output-dir /workspace/scratch/hourly-20261119-refresh/candidate` | 0 | 8.670277 |
| `/workspace/MAM-basics/.venv/bin/python py/main_diff.py mpplus --old 54aaab9300e1559c891275a547dd516a84207354 --new 67a6ec467ba0cf078e9790760a2ee8452f722382 --output /workspace/scratch/hourly-20261119-refresh/public-artifacts/endpoint.html` | 0 | 1.327752 |
| `/workspace/MAM-basics/.venv/bin/python py/main_diff.py mpplus --check` | 0 | 6.719448 |
| `/workspace/MAM-basics/.venv/bin/python py/main_near_aleppo.py --html` | 0 | 27.431428 |
| `/workspace/MAM-basics/.venv/bin/python py/main_test.py py/tests/test_near_aleppo.py py/tests/test_near_aleppo_note_content.py py/tests/test_near_aleppo_clc_style.py py/tests/test_shared_html_styles.py py/tests/test_diff_mpplus_unpinned_latest.py py/tests/test_mpplus_alternative_oracle.py -q -ra` | 0 | 79.257614 |

Receipt parent is the existing HP supplement `3a0bae60cb5e29db36f1b2fe3376d1aa4d13e4a6`, a documentation-only descendant of prior branch tip `30549ecfa596b5bda8b27abc4f7a5e50fce262cf`. Its17 payload hashes/CRC verify; all HP files and status remain byte-preserved. HP execution is coordinator evidence on source54aaab93, not this executor's native/browser coverage. Publishing the established receipt branch is a normal fast-forward through that existing commit plus this new receipt; no main/source integration.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d` and independent broad-tested remains November19 nightly `54aaab9300e1559c891275a547dd516a84207354`. Every previous status byte/finished receipt and historical gap is preserved. Local slots/processes were clear at admission; isolated owned checkouts preserve clean homes; cross-machine ownership is unverified. Source/parent deployment rules and no-open-PR observations were checked. Only the isolated receipt branch changes: no main/shared integration, new PR/issue, issue closure/contact, deployment/dispatch, live source request, font build/corpus refresh/baseline, hbofonts, configuration or schedule action. Remote scope/bytes/parent and owned cleanup/slot release are verified at closeout.

[Evidence](review-hourly-2026-11-19-67a6ec46-basics-evidence.zip): 96124 bytes; SHA-256 `a8ad3c669006726793ec2709003ad80efbca4907912da2e157f81da464d0658e`; 46 regular safe-relative payloads plus a self-excluding hash manifest, all sizes/hashes and CRCs verified. Complete command output, source manifests, independent comparisons and preserved failed attempts distinguish actual execution from author/coordinator evidence.
