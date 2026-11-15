# Focused morphhb report review, 2026-11-15 21:00 UTC cycle

State: completed 2026-11-15; bounded portable review and focused checks

No consequential introduced defect or product repair established in **f689951f802051fbae4ffda794be31ce0f1de7a3 -> 2a108647c4b17e587a00549eb9fa8de8958e0e3e**: four reachable commits / 42 endpoint paths. Codex reviewed the actual committed public implementation and report inputs, with two bounded read-only source passes and one writer/executor. Current instructions, product scopes and canonical Hebrew prose/receipt/worktree skills were read. No sibling input is required or read by these focused checks; all public inputs are pinned by the source commit.

The endpoint tracks 29 copied report files plus an omission note, adds four generator/link-check modules and three outputs, and integrates the new step immediately after `israel-bible-review`. The final merge and tip change licensing documentation. Owner approvals, byte equality with omitted originals, source research, provenance and the reported 1,465-pass/5-skip/90-subtest full suite and mega remain attributed to the source commits.

## Actual checks

Commands ran from `/workspace/scratch/basics-2a108647` with `/workspace/MAM-basics/.venv/bin/python`; the existing native-tool activation was loaded and no environment was changed. Exact argv/logs/diffs are in the [evidence archive](review-hourly-2026-11-15-2a108647-basics-evidence.zip).

| Check | Actual result | Seconds / exit |
| --- | --- | --- |
| Endpoint `git diff --check` | clean | 0.029015 / 0 |
| Black `--check` on all seven changed Python files | unchanged | 0.680492 / 0 |
| `py/main_authored.py gen-israel-bible-review` | dependency output byte-identical | 1.284310 / 0 |
| `py/main_authored.py gen-morphhb-corrections` | all three outputs byte-identical; 173,085-byte page, 214 links, 127 into the review, three departures | 1.231150 / 0 |
| Selected `py/main_test.py ... -q` | 34 passed, no skips; 73.77 s pytest | 75.608345 / 0 |
| Independent DOM/JSON/Unicode/attribute probe | all stated bounded comparisons pass | 0.335936 internal / 0 |
| Instrumented generator callback | exact output hashes and scoped I/O; corrected audit | 0.292224 internal / 0 |
| `py/check_html_syntax_and_sanity.py gh-pages/morphhb-corrections` | **119 text-fragment reports**, triaged below | 0.108170 / **1** |
| Three additional maintained HTML lint modules | eight passed, no skips; 16.36 s pytest | 16.576857 / 0 |

The 34-test selection covers mega coverage, product scopes, the Israel Bible review's MAM forms, prose conventions/order, transliterations, Latin composition, tracked filenames, time zones and both `main_authored` subcommand nodes. The eight additional tests cover relative site links, shared stylesheet/font dependencies and generated-artifact machine paths. These are separate focused invocations, not a full suite.

The independent probe compares all 56 actual review Where cells and decoded displayed form pairs with the link table, decodes every directive's verse/page/prefix terms, checks the 10 footnote anchors and all 127 generated review hrefs, and resolves all four stylesheet paths. Only row 55 needs a prefix to distinguish its repeated verse/page. It recomputes the copied report's 1/5/46/4 case population and census of 4,930 unique corpus IDs, 4,924 one-to-one aligned records and 17 classified mismatches. All 3,811 copied stress-helper pairs agree by an independent per-letter mark-multiset comparison after their declared accent exchange. Eight copied Decalogue units yield five mark differences, one maqaf difference and two complete unions. These are snapshot consistency checks, not independent corpus research or editorial judgments.

The fresh checkout lacks the omitted research folders. An audit of Python `open` events during imports and the generator callback observes the tracked README, 27 report `out/` inputs and the existing review's tracked inputs/page; only the expected three product files are written, with identical SHA-256 values. No sibling input is read. The report fetch log is provenance, not a runtime input. All 30 tracked input-folder files match their committed blobs. Eight `out/` files have CRLF and five have trailing blanks or terminal blank lines; 32 attribute probes confirm preservation applies only beneath this report's `out/`, without affecting its notes or neighboring paths.

The HTML checker actually failed: all 119 reports concern `#:~:text=` links into the existing review. Its `_fragment_found` accepts literal or percent-decoded element IDs and has no text-directive model. The generator's six offline matching models and the separate decoded-term/target checks pass; they do not establish native browser scroll/highlight behavior or live links. The 2,046 undefined CSS references are explicitly informational in that checker. No checker repair, suppression or clean-pass label is substituted for its exit 1. The four historical orphan crops are separate and remain unresolved.

All product-stage tracked diffs and source status remain empty. Preserved reviewer diagnostics include an optional package-metadata lookup failure before product execution, a scratch DOM identity bug, and the first audit's reporting-window mistake. That first audit callback also exited 0 with identical outputs (0.318160 s); its corrected callback was a deliberate bounded repeat. Original helpers/results and corrected methods are archived; these do not represent product fixes.

## Limits and lineage

The report-copy comparison uses the review's existing key, which deliberately permits documented sof-pasuq/qamats-qatan differences; it is not full-codepoint equality with the copied report. Displayed forms come from the exact current link table. The four-module literal-Hebrew lint does not prove copy/escape preservation against omitted scripts. Original research, omitted-source reproduction, historical conclusions and licensing/publication approval remain owner-attributed. No acquisition, online-source review, browser/native rendering, OCR, HP, broad mega/full suite or font/baseline operation ran. Next broad coverage remains with the independently managed November 16 nightly.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d` and broad-tested remains `647ef21ca9d09b1b50264b000cd6a31fd376e572`. Only this bounded endpoint gains focused coverage; every older pending window, browser/source gap, Windows scan/viewer limitation, Taamey D limit and prior nightly/HP receipt is preserved.

Receipt parent **413ca85fb9075c37af54708c353bdf562c8f59c2** and every prior maintained status byte/finished receipt are retained. Admission found 45 released prior slots, no active local checks and a clean unchanged home; cross-machine liveness is not independently verified. Source and receipt parent have the same sole manual-dispatch Pages workflow, blob `18ceb19405424710bda47d9a38c470cc2ed9c385`; the coordinator separately verified no open PR for this exact receipt branch. Only the existing isolated `review-hourly-20261113-7173440e-basics-receipts` is a publication target. No main/shared integration, dispatch/deployment, Private review, schedule or frozen-font work occurs. Exact remote verification, owned-checkout cleanup and slot release follow publication and are reported at closeout.

Evidence ZIP SHA-256: `14e5de84787646fde6fd2c331888e2791c8f8997d2039ca1ac6190e5bf53242d`. Its 38 payload members have checked size/SHA-256 entries and pass ZIP CRC validation.
