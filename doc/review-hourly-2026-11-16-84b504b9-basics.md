# MAM-basics bounded Miqra review, 2026-11-16, 84b504b9

State: completed 2026-11-16; focused review and checks, no product repair

Reviewed only `1884cf59c47d85d8cb74ec3f2a2a26015444e431` ->
`84b504b9a63c75aa0ef87dadda6e7ec301a46ebe`: five commits / 12 endpoint paths.
No consequential introduced defect established. Codex reviewed public material only;
this adds bounded focused coverage and closes no earlier pending window.

## Scope and actual checks

Current repository/common guidance, review policy and latest isolated status, product scopes,
Miqra README/plan/CLI and relevant canonical worktree, topology, receipt and Hebrew-prose
skills were read. The endpoint adds picture/TOC-field DOCX handling, two text-projection kinds,
Daniel and Zephaniah records, five display registrations and Joshua title/sort-key separation,
plus the owner's plan and bot-history account. Independent read-only parser review found no
introduced consequential defect; current callers use the reconciled APIs.

Source was detached at the endpoint, using home interpreter
`/workspace/MAM-basics/.venv/bin/python` (Python 3.13.15). Tests ran through `py/main_test.py`
from its root. The selected checks require no sibling inputs. Checks ran sequentially:

| Command / bounded scope | Actual result | Wall seconds |
| --- | --- | ---: |
| `git diff --check 1884cf59c47d85d8cb74ec3f2a2a26015444e431 84b504b9a63c75aa0ef87dadda6e7ec301a46ebe` | exit 0 | 0.008621 |
| Owning Python `-m black --check`, all seven changed Python files | exit 0; unchanged | 0.308472 |
| `py/main_test.py`, 15 selected maintained modules, `-q` | exit 0; 124 passed, no skips (127.67 s pytest) | 129.738686 |
| Disposable synthetic DOCX/extraction helper | exit 0; 40 DOCX cases plus one extraction assertion | 0.132313 |
| `py/main_miqra_mevoar.py pages --out <new disposable directory>` | exit 0; 100 local base pages | 0.293208 |
| Independent committed-data/page/display/projection helper | exit 0 | 0.560249 |
| Retained-preview comparison and synthetic check-report helper | exit 0; inner CLI expected exit 1 | 0.278537 |

The maintained modules cover all five Miqra test files, mega coverage, entrypoint declarations,
source hygiene, prose conventions/mark order, transliterations, explicit time zones, stderr,
Latin diacritics and tracked filenames. Exact argument arrays, UTC times and actual output are
in the [evidence ZIP](review-hourly-2026-11-16-84b504b9-basics-evidence.zip). Every stage left source status and tracked diffs empty.

The 40 fabricated DOCX fixtures accept seven expected shapes and refuse 33 malformed shapes;
an extra extraction/source-metadata/location assertion gives 41 recorded outcomes (8 positive,
33 expected refusals). Inline/anchored pictures and title/heading/verse/empty-row locations
are checked; malformed/text-bearing or misplaced drawings, unknown XML and invalid TOC
instructions, nesting, separators, style and closure are refused. A separate maintained
`check` CLI probe on one fabricated one-verse file exits **1**, as expected: four deliberate
inventory/extraction/versification/similarity mismatches, with all four picture locations in
its report. The helper verifies that outcome and exits 0. This is synthetic behavior evidence,
not an original-book validation or an unexplained product failure.

## Decisive output evidence and limits

All 100 base pages preserve every tracked heading/paraphrase under the documented NFC page
conversion: 2,008 verses and 145 headings, 638,713 page bytes, unique titles, complete file
inventory and no terminal newline. Daniel independently counts 12 chapters / 357 verses /
14 headings; Zephaniah 3 / 53 / 3. All 85 earlier preview files equal the retained prior run's
bytes and hashes, without repeating its generator. Original JSON codepoints remain exact;
all 12 endpoint files match their committed bytes. Recorded DOCX sizes/hashes have valid
metadata shape but were not matched to original files.

All 12 local display texts match an independent raw MAM-simple verse/starts-with-sampe walk
and tracked heading inventory, including Joshua's two declared legacy sort keys. All 2,626
verse-letter projections across the 13 registered books plus committed Judges agree with an
independent explicit tree walk, including both newly supported kinds at two Judges sites.
Judges is selected through a scratch Book descriptor reading committed `Judg.json`;
its Scripture text is original tracked MAM-simple data, not fabricated fixture text.
The new five display pages contain 457 verses; local output does not establish their live
state. Daniel's base saves and Zephaniah's display registration remain intentionally pending
with their owners; neither omission is treated as a defect.

No original Word file was available or acquired, so original extraction/check, source fidelity,
source picture content and author/editorial correctness remain unverified. Owner approvals,
fetches, original checks, live saves/readbacks, page revisions and test reports stay attributed.
No live bot or online-source acquisition, email, pCloud probe, live browser/rendering, native Windows,
Private, full suite/mega, font or frozen-study execution occurred. The entrypoint declaration
lint imports modules and builds parsers; it executes no frozen-study stage.

## Anchors and publication boundary

Receipt parent is `39e03b9165063ae0784622d7acdf22f2b10c5823`. Every prior status byte and finished receipt is preserved,
including November 15 portable/HP evidence. Overall reviewed-through remains
`210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains
`647ef21ca9d09b1b50264b000cd6a31fd376e572`. Earlier pending windows, 119 text-directive
HTML-checker findings/limitation, four historical orphan crops, Windows scan/viewer,
browser/source and Taamey D limits remain distinct. They were not rechecked or relabeled.

At admission all 47 pre-existing declared local slots were released, only the home worktree
was registered and no product-check process was active. Home remained clean at
`cb878aef91e692d5561435f00021f73b75868e45`; cross-machine ownership is not independently
verified. Only this task's two detached worktrees and unique slot are owned here. Source and
receipt parent share the sole manual-dispatch Pages workflow, blob
`18ceb19405424710bda47d9a38c470cc2ed9c385`; the coordinating root's exact-branch GitHub
query found no open PR at 17:46 UTC. Only the established isolated receipt branch is prepared;
publication and cleanup have later verification. No main/shared integration, dispatch/deployment,
schedule change, baseline acceptance, frozen-font or hbofonts operation occurs.

Evidence ZIP: 25,985 bytes, SHA-256 `a0ef0b3e9f7edd6bc24a50f7b0c6dec3094bb00abb207206e41e06a83fa62876`; 26 safe unique members,
all CRCs valid. It retains methods/logs/manifests, excludes preview/source copies and private
evidence, and distinguishes the expected synthetic refusal from passing product checks.
