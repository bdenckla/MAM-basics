# Bounded Basics screen, November 13, 2026, 17:00 UTC cycle

State: completed 2026-11-13; focused technical review, no product repair

Frozen endpoint `05191160832cba00e6bcd86959b16520c2f74d7b` -> `3badbc72b8e57f99617980c4e6383a7cf52dd4d6`: one commit / 62 paths, fully examined. The new shared generator renders two authored comparison inputs, links both pages from the site index, and supplies search, outcome, size and crop controls, 51 supplied PNG crops, and explicit source-rights attribution. No consequential introduced defect was established; no Hebrew, editorial, licensing or publication decision changed. Receipt lineage continues from `00d973a398fd018f68a1abc93e6d6ad639bc82eb`.

The maintained `py/main_authored.py gen-site` reproduces every tracked output exactly. Changed-source Black passes for all three Python files; **13 selected tests pass** through `py/main_test.py -q -ra` (site index/deploy root/relative links/shared styles/letter spacing/prose conventions). The comparison-folder HTML checker passes; its 140 shared/external CSS-class references are informational under the maintained checker, not output failures.

Independent checks reconcile **50 displayed pairs** (31 Koren / 19 the Simanim Tanakh), every category and crop association, **48** MAM body/qere readings and the **two explicitly linked printed-tradition note clauses**, all **26** linked Phonetic MAM final-stress rows, **205** local link/asset attributes and fragments, and all **51** PNGs' format/integrity and inventory. The 11 Koren and 13 the Simanim Tanakh redundant-helper entries have the displayed doubled pashta and double-sheva ending. Four supplied crop samples were viewed and agree with their listed mark configurations. **14** malformed/duplicate/missing-evidence rejection probes pass. All 62 endpoint files match their committed blobs; no crop is copied into the evidence archive.

The actual `controls.js` runs in a minimal Node DOM model: **837** query/category combinations, range changes, reset and four image toggles per page pass. This establishes the tested control behavior, not browser layout, accessibility-tree or font behavior.

| Recorded stage (exact arguments in evidence JSON) | Exit | Seconds |
| --- | ---: | ---: |
| black | 0 | 0.225718 |
| gen-site | 0 | 141.105571 |
| tests | 0 | 41.280158 |
| html | 0 | 0.70707 |
| probes | 1 | 0.82314 |
| probes-qere | 1 | 1.14082 |
| probes-corrected | 0 | 1.370905 |
| javascript | 0 | 0.317755 |

Two scratch checker assumptions failed and were corrected without changing the product: qere brackets obstructed a raw-text comparison, and two comparison readings belong to their explicitly linked printed-tradition clauses rather than the body page. Both original scripts, logs and empty source diffs remain in the archive. The corrected checks use the actual qere markup and those exact clauses. All maintained and scratch-command tracked diffs/statuses are empty.

Research coverage/OCR/reverse-catalogue totals, the historic Wikisource correction and unsampled printed-edition claims remain attributed authored research. The original full research catalogues/scans and live correction were not acquired or independently reproduced. Reproducibility and public-text agreement do not establish editorial correctness or source publication rights. No live acquisition, broad/nightly rerun, private review, font/baseline or hbofonts work, native Windows execution, browser verification, main/shared integration, deployment/dispatch or schedule change occurred.

Reconciled nightly `04ce8be904bbd1f15e33a5101976a7e9e6f9f7ca` and Windows supplement `3030161007bc393f554cf0c95cf819ed4d81a93c` at source `9ed47c6e8999ecaf56031e9b3f524bee6e01507a`: the former records 66 mega steps and 1,449 passed / five intentional skips; the latter records 41 focused platform-sensitive tests plus native resource-API probes. These are prior attributed results, not this run. Latest broad-tested stays at that source. Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; every other pending window, immutable receipt and Taamey D corpus/baseline limitation remains. The prior admission is reused; cross-machine ownership remains unverified.

Only this fresh isolated receipt/status/evidence branch is published. Source and receipt parent retain the sole manual-dispatch Pages workflow. [Evidence](review-hourly-2026-11-13-3badbc72-basics-evidence.zip): 61676 bytes, SHA-256 `b7149764889148650eaa622b884a7478dc6e85725d4712ab38df430eaadb4aee`; CRC and all payload sizes/hashes verified. Exact remote scope/bytes and owned-worktree cleanup/slot release are verified at closeout; home checkout and unrelated work are preserved.
