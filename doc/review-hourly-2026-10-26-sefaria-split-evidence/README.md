# October 26 Sefaria page-split focused evidence

State: completed 2026-10-26; review only

Source: `c6701099fd146832cb74a523d549a0e4c09c97b1`. This review starts at
`ee700b4713ea242e5d27f18bdff3093756df97d7`; receipt history continues from
`86c1afedd4b8fd693d709b168143e82ee7bf3444`. The receipt checkout is not the tested source.
See the [compact receipt](../review-hourly-2026-10-26-sefaria-split.json).

`generate`, `maintained`, `independent` and `listing-followup` each have a command/timing JSON
and actual output log. Their timestamps are strictly sequential: each process completed before
the next started. The generator reproduced all three pages with clean tracked status; the
seven maintained modules returned 25 passed, zero skips. No previous broad run was repeated.

`focused_split.py` is the formatted one-off raw-file differential helper. It imports neither
new survey nor generator code. `initial-helper.txt` preserves the version with the false
assertion: it mistook an unindented SPACE actually present in a non-dual CSV row's combined
field for a stripped final-field space. The first run reported two passed, one failed.
The CSV writer strips only the last field; after accounting for retained spaces, only the
failed check reran and passed, independently identifying the nine documented cases and 3,482
retained trailing spaces. `independent-result.json` combines those actual completed results.
No combined all-green invocation is claimed, and no source repair was needed.

For reproduction in a fresh isolated source checkout, place `focused_split.py` at
`.novc/split/test_split.py` and `run_stage.py` beside it. Run each selected stage through the
home clone's interpreter, from that checkout's root, awaiting completion before the next.
The helper is evidence, outside the maintained suite. The runner refuses to overwrite a
completed stage's evidence.

Raw evidence was preserved outside the temporary worktrees before cleanup. The previous
receipt's overlap record stays unchanged. This run made no main, deployment, baseline, font
build, source-export, licensing, permission, Fonts, Private or HP change.

The initial independent pytest failure log is `independent.log.gz`, a byte-exact gzip copy.
Pytest's diagnostic contains trailing spaces, which the initial staged whitespace check
reported. Its text was preserved without edits; the raw log also remains in the scratch archive.
