# October 26 focused note-extractor evidence

State: completed 2026-10-26; review only

Source: `3c6b216c13c3ffa043501a485ea5481a6ab31e93`. The parent receipt is
`c6a28fc5388f84017064e7d48e75234426b8e912`; the receipt checkout is not the tested code.
The [compact receipt](../review-hourly-2026-10-26-doc-notes.json) records the precise scope.

`focused_checks.py` is the formatted copy of the one-off scratch helper. It uses an
independent raw-JSON walker/character scanner and the real FOI CLI. On a fresh isolated
checkout of the source, place it at `.novc/hourly/test_doc_note_focused.py` and invoke it
through `py/main_test.py` with the home clone's interpreter. It is not a new maintained
suite module. `all-foi.log` is the single full FOI-only regeneration; the two selected-FOI
logs and `result.json` belong to the later focused continuation.

The first invocation returned 1: six checks passed and the remaining scratch assertion
counted a literal sentence without allowing HTML line wrapping. After correcting only that
assertion, the remaining check passed (one passed, six deselected). No full FOI job was repeated.
No combined all-green suite invocation is claimed. All 51 root FOI products reproduced;
source status stayed clean. The fully empty synthetic page existed only in pytest scratch.
The raw helper and evidence were also preserved outside the temporary worktrees before cleanup.
