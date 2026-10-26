# October 26 prose-font focused evidence

State: completed 2026-10-26; review only

Source: `fab8bd0a886d623c4fd6b2a324594f8aee19af87`; window begins at
`c6701099fd146832cb74a523d549a0e4c09c97b1`. Receipt history continues from
`505af0986bf7a1dff8e5fcc3cebe2c75a664b306`; the receipt checkout is not the tested source.
See the [compact receipt](../review-hourly-2026-10-26-prose-font.json).

Three-page regeneration reproduced tracked output. The initial focused invocation reports
three passed (two maintained checks and the 53-cell ordered text comparison), one failed,
zero skips. Its failure was in the scratch adapter: it fed rendered layout whitespace to
the authoring constructor, which rejects that whitespace. The corrected adapter uses the
plain node representation that the guard consumes. Only that check reran and passed,
including mutations of all 11 unpointed prose fragments and inline/line-break boundaries.
No source repair or combined all-green invocation is claimed.

`focused_style.py` is the formatted corrected helper, `initial-helper.txt` the failed version,
and `style-result.json` the targeted continuation's output. For reproduction in a fresh isolated
source checkout, place the helper at `.novc/hourly/test_font_style.py` and run it through
`py/main_test.py`, using the home clone's interpreter. All commands, timestamps and raw logs
are preserved; logs use byte-exact gzip, so diagnostic whitespace is not edited.

All test/generator stages across the two repositories were awaited sequentially. Prior receipt
history and broad-tested evidence remain unchanged. No browser rendering judgment, font upgrade,
source repair, export refresh, main/shared integration or publication was performed.
