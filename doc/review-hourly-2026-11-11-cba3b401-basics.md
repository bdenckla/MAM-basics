# MAM-basics bounded relocation and header review

State: completed 2026-11-11; focused screen only

Codex reviewed `b1bdd3787ee2ab2a1e6315b01d8a1019894c9b48..cba3b401666aa0a49147fdc54294086ff343de81`: three commits, 57 rename-aware paths. Source checkout `/workspace/scratch/basics-cba3b401-checkout` used its home interpreter `/workspace/MAM-basics/.venv/bin/python` (3.13.15; tracked requirements/constraints match). Receipt lineage continues `83114a7c6194f8651dec51a9ad4ece1d00003c02` without importing source main. No consequential introduced defect or product repair.

Commands ran sequentially from the exact head, except the explicitly marked base comparison. [Evidence](review-hourly-2026-11-11-cba3b401-basics-evidence.zip) retains complete command arrays, UTC timestamps, exits, timings, logs, empty per-stage diffs/statuses, endpoint patch, independent checker and payload manifest.

| Command (after the owning interpreter) | Result | Wall seconds |
| --- | --- | --- |
| `py/main_authored.py gen-israel-bible-review` | exit 0; clean output/status | 1.533836 |
| `py/main_authored.py gen-misc` | exit 0; clean output/status | 2.112085 |
| `py/main_authored.py gen-site --trust-surveys` | exit 0; clean output/status | 5.766425 |
| `py/main_verify_and_render_table.py` | exit 0; clean output/status | 1.142407 |
| `py/main_mam_morphhb.py` | exit 0; clean output/status | 1.374043 |
| `py/main_mam_osis.py` | exit 0; clean output/status | 0.703505 |
| `-m black --check (all 15 changed Python files)` | exit 0; clean output/status | 0.462149 |
| `py/main_test.py (17 explicitly named test files; full list in evidence)` | 85 passed; 113.67 s pytest; no skips/failures | 116.099026 |
| `py/check_html_syntax_and_sanity.py gh-pages/israel-bible-review` | exit 0; clean output/status | 0.114293 |
| `py/check_html_syntax_and_sanity.py gh-pages/post-stress-meteg` | exit 0; clean output/status | 0.130824 |
| `py/check_html_syntax_and_sanity.py --deploy-root` | exit 0; clean output/status | 0.075913 |
| `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc` | exit 0; clean output/status | 1.965051 |
| `py/check_html_syntax_and_sanity.py gh-pages/holman` | exit 1; inherited five Holman issues | 0.230708 |
| `py/check_html_syntax_and_sanity.py gh-pages/holman` **at base** | exit 1; inherited five Holman issues | 0.264384 |
| `check.py (retained independent checker)` | exit 0; clean output/status | 0.863339 |
| `git diff --check` | exit 0; clean output/status | 0.007349 |

The six generators reproduce committed outputs exactly. Both full XML exports and their headers differ from base only by the three named title/description/URL corrections; history remains untouched. All sixteen post-stress pages reconstruct exactly with 48 stylesheet and 37 crop-path prefixes; their Hebrew, prose, tables and links otherwise retain their bytes. Israel Bible HTML reconstructs with only five banner/path substitutions; CSS rules change only the font URL and the crop is byte-identical. All 124 checked relative destinations exist. The redirect has agreeing canonical, refresh, script and visible targets; its script expression retains query/fragment (static verification, no browser run). Three offline probes verify the missing-root-exception guard and sub-site scoping.

Four HTML scopes pass, retaining informational CSS counts of 10 (Israel Bible), 1,163 (post-stress), zero (root) and 16,966 (MAM-with-doc). Holman is **not a clean pass**: both exact endpoints return 1 with the same five issues (three lang=he versus en reports and two orphan reports), plus 826 informational CSS references. Complete stdout is byte-identical. No new issue is introduced by this window.

Owner commit claims about prior test counts, visual/source checks and the last Pages dispatch remain attributed. This execution establishes output consistency, not source/editorial correctness or rights decisions. The README's licensing question remains with Ben and the originating editor; this review grants no rights and changes no terms. No broad mega/suite, fresh sources/live requests, manuscript/PDF/browser/font verification, hbofonts, deployment, workflow dispatch, main/shared integration or schedule work. Cross-machine HP ownership was unavailable; actual local inventory was clear and all work used task-owned isolation.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. All inherited pending windows and historical failures survive in the maintained status. No further execution is owed for this bounded window. Existing nightly ownership covers broad work; the originating editor handles the license record only after Ben's decision. Only a fresh isolated nondeployment receipt branch is authorized for publication; the sole workflow at source and receipt parent is manual dispatch.
