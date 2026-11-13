# Bounded Basics screen, November 13, 2026, 20:00 UTC cycle

State: completed 2026-11-13; focused technical review, no product repair

Frozen endpoint `5287ba189e87bd90cb889fe7c578c8ada8c1f55b` → `4c0084f405351e36eb590180fa6a7f4a4f1ee063`: **five commits / 11 paths**, 217 insertions / 215 deletions. The complete endpoint changes remove three comparisons against nonmatching Decalogue strands, add five rows across four verses with five crops, cite underlying MAM readings instead of their Phonetic MAM derivative, and simplify the two tables. No consequential introduced defect was established; no product repair. Receipt parent: `34a4db7c6a54d0df792709df8b15b3c350577b78`, reconciling the 19:00 and 18:00 screens after the 17:00 receipt.

Actual maintained `gen-site --trust-surveys` reproduces all tracked outputs exactly. Changed-source Black passes and **37 selected tests pass** through `py/main_test.py -q -ra`: the three relevant Decalogue modules and six site/style/prose modules named in the evidence. Commands ran sequentially from the detached exact source, using the home interpreter:

```text
/workspace/MAM-basics/.venv/bin/python -B -m black --check py/author_site/stress_helper_comparison.py
/workspace/MAM-basics/.venv/bin/python -B py/main_authored.py gen-site --trust-surveys
/workspace/MAM-basics/.venv/bin/python -B py/main_test.py -q -ra py/tests/test_printed_decalogue_simanim.py py/tests/test_printed_decalogue_koren.py py/tests/test_decalogue_m_trad.py py/tests/test_site_index_links.py py/tests/test_deploy_root_html.py py/tests/test_site_links_relative.py py/tests/test_shared_html_styles.py py/tests/test_hebrew_letter_spacing.py py/tests/test_prose_conventions.py
/workspace/MAM-basics/.venv/bin/python -B py/check_html_syntax_and_sanity.py gh-pages/stress-helpers
```

The HTML checker **exits 1**, reporting precisely the four retained crops of the three removed rows; 151 CSS-class references are informational. These existing source assets are harmless retained evidence and were not deleted. No HTML-clean claim is made. The four reports are:

- `img/koren-deuter-5-13-A5-D-281-370-1.png`
- `img/koren-deuter-5-13-A5-D-281-370-2.png`
- `img/simanim-tanakh-deuter-5-6-A9-A5-10C-0351-1685-1.png`
- `img/simanim-tanakh-exodus-20-2-A9-A2-10C-0350-1684-1.png`

Independent checks pass for **52 displayed pairs** (34 Koren / 18 Simanim), all **52 underlying MAM body/qere readings**, exact page/scan labels and four-cell rows, all **183** local link/asset attributes and fragments, and integrity of **56 PNGs** (52 linked, the four above retained). Existing rows preserve their forms, categories, page/scan/crop fields; only notes change. The 11/13 redundant-helper claims match displayed double pashta and double-sheva endings. The five new supplied crops were viewed; their visible helper placements agree with the printed forms. No crops are copied into the evidence archive.

The former stored Simanim printed forms carry **merkha**. The matching mirrored manuscript-tradition עליון has **tevir on tav**; the two retained crops, also viewed here, and existing full Decalogue transcriptions support tevir at that letter. The window corrects the stored accent before removing the comparisons against a different strand. No literal equality between the former stored forms and that mirrored strand is claimed. The removed Koren compound agrees with revia on tav and absence of a telisha gedolah helper in printed-tradition תחתון, but Koren has **one additional meteg on the second vav**. Both literal forms and that exact difference are retained; full-mark identity is not claimed. The Chronicles/Genesis comparison reproduces the same letters/vowels with the helper on bet versus shin. The “likely MAM error” interpretation and **10,223 scan-check** completion claim remain owner-attributed research, not independently established here; underlying MAM is unchanged.

The unchanged actual `controls.js` passes **1,030 query/category combinations** on the current four-cell DOM data, plus range/reset and four image toggles per page, in a minimal Node model. This verifies those behaviors only; it supplies no browser/layout/accessibility-tree/font result.

| Stage (full arguments and UTC timestamps in evidence JSON) | Exit | Seconds |
| --- | ---: | ---: |
| black | 0 | 0.148145 |
| gen-site | 0 | 5.441252 |
| tests | 0 | 40.472686 |
| html | 1 | 0.629907 |
| probes | 1 | 0.37313 |
| probes-corrected | 1 | 0.741892 |
| probes-final | 0 | 1.070658 |
| javascript | 0 | 0.294857 |
| probes-simanim-clarified | 0 | 1.144353 |

Two scratch assumptions failed before the final passing probe: exact Koren full-mark identity, and using verse/strand/instance alone as comparison identity. Their original scripts, logs and empty diffs/statuses are retained; the corrected probe records the literal meteg difference and includes both displayed forms in identity. An initial `gen-site` without `--trust-surveys` unnecessarily began the unrelated post-stress survey and was stopped with SIGTERM (owned runner exit 143; child observed defunct). Partial output/diff/status and the exact invocation are retained; no completed survey result is claimed. The corrected bounded generation then passed. These are reviewer invocation/fixture corrections, not product failures. Every completed stage leaves empty tracked/untracked output diffs/statuses. A preparation retry stopped on an already-converted timestamp key before writing; the original script/log remain archived. The uncommitted status was rebuilt from the exact parent to remove duplicate draft sections, with complete prior content preservation verified.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `9ed47c6e8999ecaf56031e9b3f524bee6e01507a`. All historic pending windows, finished receipts, November 13 nightly/Windows supplement `3030161007bc393f554cf0c95cf819ed4d81a93c`, and Taamey D corpus/baseline limitations remain. Local admission was fresh; cross-machine ownership remains unverified. No broad/nightly rerun, original-source acquisition, Private or hbofonts work, editorial/rights change, main/shared integration, deployment/dispatch or schedule change.

[Evidence](review-hourly-2026-11-13-4c0084f4-basics-evidence.zip): **102298 bytes**, SHA-256 `7284a9fb4731bc03ca7930665ce66ea5e2ecd292bfc42d4559095778f062c241`; local CRC and all payload hashes verified. Only the isolated three-path receipt branch is prepared for normal publication; source and parent retain the sole manual-dispatch Pages workflow. Exact remote verification and owned-worktree cleanup/slot release are closeout steps, recorded after they occur.
