# Phase 6 command map and frozen baseline

Measured on 2026-09-10 at MAM-basics
`9ea4e39abf6ceae3e52f0cb37a3ba4abf470b05f`, by task
`01a08c21-6520-7493-b9a5-8ec6ee5abf5f` (6A). The development checkout is
`C:/Users/BenDe/GitRepos/MAM-basics`, on primary `main`.

The authoritative path lists are in
[`in/mam_products_phase6_baseline.json`](../in/mam_products_phase6_baseline.json):
`commands` gives full argument arrays, absolute cwds, prerequisites, exact data
inputs and expected output paths; `sets` gives every membership; `files` records
mode, Git blob ID, byte count and SHA-256. Expected output counts below include
conditional writes. They are not measured mtime counts.

Use `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` for every
Python command. All commands run from the development root except the explicitly
named product examples. A fresh task reads current user-wide instructions,
`CLAUDE.md`, the dedicated plan's common lane/README rules and complete Phase 6
section, then its predecessor's record. Load `hebrew-prose` before editing prose
about accentuation. The assigned work does not include unrelated editorial changes.

## 6B: parsing, template surveys and MAM-simple

Run the commands in this order, prefixing each argument list with the absolute
interpreter above. Run each command from `C:/Users/BenDe/GitRepos/MAM-basics`.

| Arguments | Inputs and prerequisites | Expected output set |
| --- | --- | --- |
| `py/main_parse.py go` | Six frozen section CSVs in `in/mam-go/`; existing plain/plus survey JSON for the embedded documentation checks | 48 corpus JSONs, two support/provenance files, 23 published HTML/CSS files and `doc/mp-claims.md`: 74 paths |
| `py/main_foi_features_of_interest.py` | The freshly parsed plus corpus | 49 files in `gh-pages/MAM-with-doc/foi/`: HTML, JSON, CSS and provenance |
| `py/main_tmpl_survey.py` | Fresh plain/plus corpus; both `py/tmpl_survey/expanded_stack_grammar_*.lock.json` inputs | 14 files in `out/tmpl-survey-{plain,plus}/` and 12 SVGs in `gh-pages/MAM-parsed/{plain,plus}/svg/`: 26 paths |
| `py/main_authored.py gen-mam-parsed-docs` | Fresh corpus and fresh survey JSON | The 24 documentation paths already written by parse, checked again with current surveys |
| `py/main_mam_simple.py` | Fresh plus corpus, canonical support modules, authored CSS and `doc/woff2/Taamey_D.woff2` | 216 XML/JSON/Unicode-name corpus files, 44 support modules plus provenance, and five documentation/assets paths: 266 paths |

The parser itself invokes documentation generation and claim verification before
the later survey step. Keep the frozen survey JSON available for that first pass;
the explicit documentation command after survey generation completes the dependency
order. Do not use `--skip-verify-mp`. A first-pass failure is evidence to inspect,
not permission to bypass verification. The historical lane reported 79 passed
claim checks and one pending `mp.plain.docs.book39-skeleton.common` check;
re-measure the current result.

The bare MAM-simple CLI means `all`, including the documentation and support
copies. The mega calls `almost_main`, which does not include that CLI documentation
dispatch, so copying the mega's Python call would miss work. The source lists in
`py/py_misc/mam_simple_copy_py_files.py` and
`py/py_misc/mam_parsed_copy_py_files.py` name the support copies; the four example
entry programs are maintained separately. Before either production copy routine
recreates its support directories, confirm those directories contain no independent
untracked work. The production routines must resolve within this exact MAM-basics
checkout.

Graphviz is installed at `C:/Program Files/Graphviz/bin/dot.exe`. Its verified
stamp is `16.0.0 (20260814.1018)`, matching `mb_cmn/graphviz_pin.py`.
`dot` was absent from the shell PATH in 6A, but `survey_dot._find_dot` uses this
Program Files fallback. Recheck the stamp before rendering. Preserve the grammar
locks; do not pass `--write-expanded-stack-grammar-lock`.

Relevant existing checks include `test_main_mam_simple_cli.py`,
`test_mam_simple_mark_order.py`, `test_mam_simple_dualcant_loader.py`,
`test_versification_differences_doc.py`, `test_versification_and_cantillation_doc.py`,
the `test_tmpl_survey_*.py` files, `test_graphviz_version_pin.py`,
`test_no_machine_paths_in_artifacts.py` and `test_sibling_reach.py`, under
`py/tests/`. Run selected files through `py/main_test.py`; do not add a test runner.

## 6C: MAM-with-doc and historical comparisons

| Arguments from the development root | Inputs and prerequisites | Expected output set |
| --- | --- | --- |
| `py/main_mam_with_doc.py` | Fresh plus corpus; 6B FOI outputs must already exist for linked pages | 62 root files under `gh-pages/MAM-with-doc/`, including corpus pages, conditional big-document pages, index and CSS |
| `py/main_authored.py gen-misc` | Authored `py/author_misc/` modules; existing linked static assets | 20 files directly under `gh-pages/MAM-with-doc/misc/`, plus the retained `tsinnorit_oleh/` redirect page: 21 paths |
| `py/main_diff.py mpp --all` | All six historical boundaries, historical manifest, release table, current committed plus data, and the existing misc font | Five named HTML/JSON pairs, unpinned HTML/JSON, index, CSS, JavaScript and font: 16 paths |

The historical boundaries and ordering are authoritative in
`MAM-parsed/historical/manifest.json` and
`gh-pages/MAM-with-doc/change-log/releases.json`. The named pairs are:

| Release | Old | New |
| --- | --- | --- |
| `2025-03-19a` | `b5e8f94` | `3d5ecfd` |
| `2025-03-19b` | `3d5ecfd` | `049e636` |
| `2026-03-06` | `049e636` | `cc43fe0` |
| `2026-03-16` | `cc43fe0` | `1880cbb` |
| `2026-04-14` | `1880cbb` | `9ce6ee5` |
| `unpinned-latest` | `9ce6ee5` | current MAM-basics `HEAD` |

Commit any accepted 6B corpus changes before this task: `HEAD` comparisons read
Git objects, while stored historical comparisons read the protected local files.
No `--legacy-history`, clone recreation or downloads are needed. Confirm all 144
historical JSONs remain the recorded 84,572,003 bytes with their original Git IDs.
The 16 expected outputs include conditionally written shared assets. In particular,
the font-copy routine's size check does not prove byte identity; compare the source
and destination font bytes independently.

Existing history checks are `test_diff_mpp_unpinned_latest.py` and the
`test_mpplus_*.py` files. Include link, mark-order and source-hygiene checks relevant
to any accepted change. Preserve the prior distinction between immutable Land and
the thirteen documented Phase 4 published-file adaptations.

## 6D: Sefaria, OSIS and independent examples

| Arguments | Absolute cwd | Expected outputs and comparison |
| --- | --- | --- |
| `py/main_mam4sef.py --both-sef-and-ajf` | `C:/Users/BenDe/GitRepos/MAM-basics` | 156 data files and four provenance files in `MAM-for-Sefaria/`; standard Sefaria reads simple `json-vtrad-sef`, AJF reads `json-vtrad-bhs` |
| `py/main_mam_osis.py` | `C:/Users/BenDe/GitRepos/MAM-basics` | 24 `MAM-OSIS/MAPM-24/` books, combined `mapm.osis.xml`, index and CSS: 27 files; input is simple `xml-vtrad-bhs`, `header.xml`, and the two local XSDs |
| `py/main_tmpl_survey_toy.py` | `C:/Users/BenDe/GitRepos/MAM-basics` | `py-examples-out/tmpl_survey_toy.json`, from parsed `plus/BA-Samuel.json` |
| `py/main_letter_small_job.py` | `C:/Users/BenDe/GitRepos/MAM-basics` | `py-examples-out/letter-small-job.txt`, from simple `xml-vtrad-mam/Job.xml` |
| `py-examples/main_tmpl_survey_toy_example.py` | `C:/Users/BenDe/GitRepos/MAM-basics/MAM-parsed` | One product-local toy output; exact comparison with the canonical toy output |
| `py-examples/main_letter_small_job_example.py` | `C:/Users/BenDe/GitRepos/MAM-basics/MAM-simple` | One product-local letter output; exact comparison with the canonical letter output |
| `py-examples/main_mam4sef_example.py` | `C:/Users/BenDe/GitRepos/MAM-basics/MAM-simple` | 80 files under `py-examples-out/sefaria/`; 39 CSV and 39 Unicode-name outputs match production; each provenance file retains its own generator path |
| `py-examples/main_mam_osis_example.py` | `C:/Users/BenDe/GitRepos/MAM-basics/MAM-simple` | 24 `py-examples-out/osis/` books, exactly matching production |

The baseline lists all 106 comparison pairs. At the frozen commit, 104 match
exactly and the two Sefaria `_provenance.md` files differ by design. Preserve each
provenance file's own frozen bytes. All 45 support module pairs also match: 44 in
MAM-simple and one in MAM-parsed. Independent entry programs share those support
modules; the recorded oracle is the independent entry/output comparison, with
frozen historical byte evidence, not a claim of wholly separate implementations.

OSIS validates combined XML with `in/osisCore.2.1.1-cw6.xsd` and `in/xml.xsd`.
Keep `MAM-OSIS/MAPM-orig/` and `MAPM-orig-24/` protected and retain the separate
current/historical licence scopes. Production and example schemas/paths were
freshly verified in 5F; repeat the assigned 6D checks after 6B's outputs.

## 6E: publication, vendoring and source references

Run `py/main_test.py py/tests/test_redirect_manifest.py -q` from the root.
For each product, the baseline provides separate `build` and `check` argument
arrays with `--repo` and explicit scratch `--out`/`--dir`. The directories are
`.novc/phase6e-mam-simple-stubs`, `.novc/phase6e-mam-for-sefaria-stubs`,
`.novc/phase6e-mam-parsed-stubs`, `.novc/phase6e-mam-with-doc-stubs` and
`.novc/phase6e-mam-osis-stubs`. Each expected scratch set includes `404.html`.
Never substitute `--publish` or an argument-less `check`.

Freeze membership from the existing redirect manifests, not today's target page
discovery: MAM-simple has 2 legacy HTMLs, MAM-for-Sefaria 1, MAM-parsed 22,
MAM-with-doc 113 and MAM-OSIS 1. Verify all 139 old/target HTML pairs, relevant
custom-404 routes and all 340 target published files, with byte hashes against the
accepted target commit and source Git objects. URL-encode path components when
requesting paths containing spaces or non-ASCII. Record response status separately
from body correctness. Earlier browser proof is reusable only after matching
deployed script and target bytes; retain every stated limitation. The short Phase 4
record documents representative HTTP checks, so 6E must supply the complete fresh
MAM-with-doc URL census.

| Arguments from the development root | Inputs | Expected outputs |
| --- | --- | --- |
| `py/main_vendoring.py --all` | `in/vendoring_policy.json`, canonical modules, 44 simple support copies and their Git history | `doc/vendoring-inventory.md` and all three `out/vendoring_*` reports: four paths |
| `py/main_pipeline_graph.py` | Structured pipeline specification and authored `doc/process-documentation/MAM-process.dot`; pinned Graphviz | `pipeline.dot`, `pipeline.svg` and `MAM-process.dot.svg` in that documentation directory |
| `py/main_authored.py gen-site --trust-surveys` | Authored site data and tracked `out/accgram/post-stress-meteg.json` | 11 deploy-root pages; verify product navigation and preserve unrelated content |

The vendoring command audits copies; 6B's production commands make the copies.
The mega's old comment saying the audit has three artifacts misses its JSON
provenance report. Current policy ignores MAM-private. `gen-site --trust-surveys`
uses the tracked survey without private recomputation. The graph command renders
the hand-authored process DOT without rewriting that DOT input.

Audit tracked operational references with Git/`rg` and a labelled UTF-8 scratch
report: sibling path constructions, `REPO_MAM_*`, `sibling_repo`, `../MAM-*`, old
GitHub/raw/Pages URLs, both workspace rosters, visibility and vendoring declarations,
pipeline labels, product READMEs and root navigation. Search dynamic path builders
as well as literal paths. Classify dated plans, original mirrors/manifests,
intentional redirects and explicit optional history separately from current
operational references. The five redirect-only sibling declarations remain.
Existing checks include sibling reach, redirects, site links, machine paths,
vendoring policy paths and repository visibility. Read-only MAM-private inspection
is allowed for the source-reference audit; no private text enters public evidence.

## Baseline reproduction, preservation and 6F accounting

Re-establish Git facts against the fixed commit, not the moving working tree:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics ls-tree -r -l -z 9ea4e39abf6ceae3e52f0cb37a3ba4abf470b05f
```

Use a uniquely named `.novc/` Python file to capture that command as bytes and parse
NUL-delimited records. Compare the named `sets` against the returned paths. Read
each recorded object with `git cat-file --batch` or `git cat-file blob <git_blob>`;
the object byte length must equal `bytes`, and SHA-256 must equal the recorded
hash. The Git ID is SHA-1 of the Git blob header plus those bytes. Every historical
source inventory includes its exact `gh api .../git/trees/<commit>?recursive=1`
command. No working-tree EOL conversion or Unicode normalization participates.

The baseline covers 2,450 files / 351,416,216 bytes; the complete target Git tree
has 5,642 files / 828,491,627 bytes. Sets overlap, so their totals must not be added.
The `implementation_tree` set conservatively freezes all 1,225 `py/` files to detect
code changes invalidating an older result; it does not assert that every module is
executed. All five product/published trees total 1,154 files / 332,326,974 bytes.

Protect the explicit `preserved_product_static` set: 188 paths, including fonts,
scans, Sefaria's static published tree, MAM-with-doc `sigil-decoding.html`,
`foi/poetic-verlen.csv`, `misc/aliyot-styles.css`, MAM-simple's Torah-letter samples,
product notices and independent entry programs. Historical sets are additional
protected paths. A clean status on those files proves no regeneration; their proof
is frozen byte identity. Preserve all earlier manifests and original historical
values, including decomposed Latin text serialized with JSON Unicode escapes.

For each generator, record before/after nanosecond mtimes, sizes, raw byte hashes
and blob identities across tracked files plus non-cache working files in the
entire MAM-basics root. Keep actual changed-path sets distinct from expected output
sets. Check each of the five actual sibling paths with `os.path.lexists` before
and after. Existing ignored helpers are not evidence unless their scope is inspected;
do not rerun old inventory, Empty or Remove helpers.

6F must reconcile every command, comparison and URL record with the final input
and output blobs, repeating any result invalidated by an intervening change.
Then run the canonical suite, redirect and affected checks, and whitespace checks;
re-measure Git totals, workspaces, `repo_visibility`, all five local product and
published roots, source absence, breadcrumbs, current heads and deployments.
Finish only with a clean pushed and deployed primary `main`. Earlier plans remain
execution records. The full mega, a mega suffix, downloaded-input refreshes,
source-clone recreation, source recycling and MAM-private writes are not commands
in this map.
