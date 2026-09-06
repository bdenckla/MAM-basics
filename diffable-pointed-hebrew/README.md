# diffable-pointed-hebrew in MAM-basics

This product directory preserves the former diffable-pointed-hebrew samples and the product-specific short Unicode-name overrides. MAM-basics now provides the command at [`../py/main_diffable_pointed_hebrew.py`](../py/main_diffable_pointed_hebrew.py).

The command accepts a UTF-8 source file and an output-file path, expands each character to the product's short Unicode name, and writes JSON. `short_unicode_name_overrides.json` records the nine names that intentionally differ from MAM-basics' general Unicode-name mapping. The tracked standard and tiny samples are the differential artifacts for the command; `tiny-sample-output-normalized.json` is preserved historical data rather than a current command output.
