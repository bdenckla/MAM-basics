# Reading MAM-simple

The guide to the MAM-simple format lives under MAM-basics' MAM-simple product tree, and is
canonical there:

- [doc/reading-mam-simple.md](../../MAM-simple/doc/reading-mam-simple.md) — file layout, and reading MAM-simple from Python
- [doc/reading-mam-simple-xml.md](../../MAM-simple/doc/reading-mam-simple-xml.md) — the XML hierarchy, element types, and verse attributes
- [doc/reading-mam-simple-json.md](../../MAM-simple/doc/reading-mam-simple-json.md) — the JSON format

This file used to be a fuller copy of that guide. The copy went stale — it still had the
XML under `out/xml-vtrad-mam`, a directory MAM-simple moved to the repo root — so on
2026-08-03 its content was merged into the canonical guide and this pointer left behind.
What remains below is what is specific to the Cambridge 1753 data.

## What MAM-basics has for Cambridge 1753

`../../MAM-simple/xml-vtrad-mam/` is the MAM word-sequence ground truth. It is the
landed MAM-simple product, regenerated from MAM-parsed by MAM-basics' export pipeline.

`../../py/py_ac_loc/mam_xml_verses.py` reads it, and
`../../py/py_cam1753_loc/gen_flat_stream.py` is what calls it. The entry point is
`get_verses_in_range(xml_path, book_osis_prefix, start_cv, end_cv)`, which returns one
dict per verse with `cv`, `words`, `ketiv_indices`, and `parashah_before`.

**The shared reader came from codex-index-aleppo, deliberately.** codex-index-cam1753 had a
separate copy at `py_mam_xml/mam_xml_verses.py` until 2026-08-22; the two were the same tool
with 43 lines of drift, and a census of every tag in Ps, Job and Prov found exactly one
they treated differently — `spi-invnun`, the seven inverted nuns of Psalm 107, which
the codex-index-aleppo copy raised on and the codex-index-cam1753 copy silently skipped. The shared copy was
given the missing skip clause and codex-index-cam1753's copy was deleted, the equivalence having been
checked over all three books: 4512 verses, 30322 words, 0 mismatches.

Two choices in the shared reader belong to the Aleppo and Cambridge 1753 workflows, not to MAM-simple:

- **It takes the ketiv, not the qere**, because the point is alignment against what
  Cambridge MS Add. 1753 has on the page, and the ketiv is what is written there.
  `ketiv_indices` says which entries of `words` came out unpointed as a result.
- **It joins maqaf compounds into a single entry of `words`**, so an entry is a chanted
  word rather than an atom.
