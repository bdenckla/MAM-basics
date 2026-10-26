# October 26 Sefaria-guide focused evidence

State: completed 2026-10-26; review only

Source: `ee700b4713ea242e5d27f18bdff3093756df97d7`. Reviewed window begins at
`3c6b216c13c3ffa043501a485ea5481a6ab31e93`; receipt history continues from
`556df8b0dcc46be5998a1850f4b85c33e143775e`. This receipt checkout is not the tested source.
The [compact receipt](../review-hourly-2026-10-26-sefaria.json) records all executed commands.

`focused_census.py` is a formatted copy of the one-off independent helper, importing neither
new survey nor page module. On a fresh isolated source checkout, place it at
`.novc/hourly-sefaria/test_census.py` and invoke it through `py/main_test.py`, with the home
clone's interpreter and the working directory at that checkout's root. It is evidence,
outside the maintained suite. `census-result.json` is its actual output.

Both independent checks passed in 1.43 s, with zero skips. They read all 78 CSV files and
compare the rendered folder totals, all 92 code-point counts in both variants, and all 14
element/class counts with a separate CSV/HTML reader. They also verify local links and
fragments, the viewport, RTL on all 47 marked Hebrew cells, and all six displayed two-vowel
clusters against actual product clusters with the CGJ retained. All 17 documentation font
copies retain the canonical 0.921 bytes and hash.

The real guide CLI, `gen-misc`, and `gen-site --trust-surveys` all returned 0; final source
status is clean. The existing six focused test modules returned 22 passed, zero skips in
42.27 s. `gen-misc` inadvertently began while that first pytest process was still finishing;
the receipt records the overlap. Both completed, and the independent census ran afterward.
No fully sequential claim is made for that overlap. Raw evidence was preserved outside the
temporary worktrees before cleanup. No broad run, CSV refresh, font build, baseline acceptance,
Private/Fonts/HP action or publication was performed.
