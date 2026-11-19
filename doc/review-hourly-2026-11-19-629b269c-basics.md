# Bounded frozen-capture NFC exclusion review

State: completed 2026-11-19; review only

Codex (GPT-6, xhigh), November 19 21:00 UTC screen: `45c6f6a85cb5f144447f678781b75eb2b4b331a8` -> `629b269c93910191182c4b726eaf8ef7f30b8feb` (1 commit / 1 path). **No consequential introduced defect or product repair established.** Current repository, review and routed skills were read; all owner decisions and pending source work remain separate from this bounded verification.

The complete endpoint adds only one directory prefix and its explanatory comment to `py/tests/test_h_dot_below_nfc.py`. Removing that one AST tuple element reconstructs the base AST exactly; validator logic, other exclusions and scope floors are unchanged. The real main scope changes **2,353 -> 2,351 files**, excluding exactly `in/mam-go-changes-tab/changes.csv` and its manifest. Named ordinary handwritten JSON/prose/Python examples remain checked. A disposable seven-file fixture, with five retained paths, proves the directory's trailing slash does not swallow similarly named sibling directories/files; every retained handwritten fixture still triggers the unchanged decomposed-character detectors.

The capture and manifest are byte-identical to the base. CSV: **189,511 bytes**, SHA-256 `030cb757027c00754600a43a989d8fd5bf6b8f2ed3f6196f23d39d6f1567684e`. Its decomposed source cluster remains on line 159. No capture or Hebrew normalization occurred.

**Six maintained NFC tests pass in 40.54s, plus three independent boundary/AST probes in 0.12s, no skips.** Black on the one changed Python file and whitespace checks pass. No credit generation, credit decision, site/browser/source verification, mega or full-suite run is warranted by this four-line maintenance-only delta. The author's 47 combined and 138 other results remain attributed, not additional execution here.

Actual sequential commands, using the owning home interpreter (Python 3.13.15) and the recorded source/subtree cwd:

| Command | Exit | Wall seconds |
| --- | ---: | ---: |
| `git diff --check 45c6f6a85cb5f144447f678781b75eb2b4b331a8 629b269c93910191182c4b726eaf8ef7f30b8feb` | 0 | 0.034631 |
| `/workspace/MAM-basics/.venv/bin/python -m black --check py/tests/test_h_dot_below_nfc.py` | 0 | 0.201005 |
| `/workspace/MAM-basics/.venv/bin/python py/main_test.py py/tests/test_h_dot_below_nfc.py -q -ra` | 0 | 40.776775 |
| `/workspace/MAM-basics/.venv/bin/python py/main_test.py /workspace/scratch/hourly-20261119-controls/public-artifacts/test_nfc_boundary_review.py -q -ra` | 0 | 0.297929 |

All executed checks exit 0 and leave tracked products exact; there are no failed scratch attempts or unclassified generated differences in this run. No full suite/mega, archived/BHSA, hbofonts/frozen font, baseline acceptance, source acquisition/research, issue/contact, configuration or schedule action. Expected negative fixture cases are passes, not product failures. Claims beyond committed-input consistency and the recorded tests remain attributed or unrun.

Admission `2026-11-19T21:25:16.204459+00:00` found clean homes, released previous slots, no running check process and only this visible task. Detached committed source/receipt worktrees use the corresponding home environments; no sibling runtime input was consumed. Cross-machine owner activity remains unverified; owner-managed deep visual/editorial work was not duplicated.

Only isolated branch `review/hourly-20261117-3691d51b` advances from sole parent `46a45a223a3dc36429908c68ccaa785cd42f9a2a`. All prior status bytes, immutable receipts, nightly/HP evidence, global anchors and historical gaps remain. Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; independent broad-tested stays November 19 nightly `54aaab9300e1559c891275a547dd516a84207354`. Source/parent workflows and fresh no-open-PR searches establish no deployment dependency. Remote SHA/parent/three-path bytes and owned cleanup are verified at publication/closeout; no main/shared integration.

[Evidence](review-hourly-2026-11-19-629b269c-basics-evidence.zip): **11093 bytes**, SHA-256 `5f881cafee1067308a1bde8ec843c423ccf8a1361f0bf4b80301d1465cfecff7`, **23** safe regular payloads plus self-excluding `manifest.json`; CRCs and all payload hashes/sizes verified. Complete endpoint patch, immutable source manifest, actual commands/logs, exact probe helpers/results and status-preservation proof included.
