# Reading MAM-simple

The guide to the MAM-simple format lives under MAM-basics' MAM-simple product tree, and is
canonical there:

- [doc/reading-mam-simple.md](../../MAM-simple/doc/reading-mam-simple.md) — file layout, and reading MAM-simple from Python
- [doc/reading-mam-simple-xml.md](../../MAM-simple/doc/reading-mam-simple-xml.md) — the XML hierarchy, element types, and verse attributes
- [doc/reading-mam-simple-json.md](../../MAM-simple/doc/reading-mam-simple-json.md) — the JSON format

This file used to be a fuller copy of that guide. The copy went stale — it still had the
XML under `out/xml-vtrad-mam`, a directory MAM-simple moved to the repo root — so on
2026-08-03 its content was merged into the canonical guide and this pointer left behind.
What remains below is what is specific to this repo.

## What this repo has

`../../MAM-simple/xml-vtrad-mam/` is the MAM word-sequence ground truth. It is the
landed MAM-simple product, regenerated from MAM-parsed by MAM-basics' export pipeline.

`../../py/py_ac_loc/mam_xml_verses.py` reads it. Its entry point is
`get_verses_in_range(xml_path, book_osis_prefix, start_cv, end_cv)`, which returns one
dict per verse with `cv`, `words`, `ketiv_indices`, and `parashah_before`.

Two choices in it belong to this repo, not to MAM-simple:

- **It takes the ketiv, not the qere**, because the point is alignment against what the
  Aleppo Codex has on the page, and the ketiv is what is written there. So a ketiv that is
  not read is taken too, and a qere that is not written contributes nothing (Ben's
  decisions of 2026-09-26, which the module docstring records with the rest).
  `ketiv_indices` says which entries of `words` hold a ketiv, which is unpointed.
- **It joins the atoms across each maqaf into a single entry of `words`**, so an entry is
  normally a chanted word rather than an atom. The exceptions are these, and none of them
  falls in the verses this repo's Aleppo streams cover:
  - Where the atom before a qere that is not written ends in a maqaf, one entry joins the
    atoms on either side of the qere, as 2 Sam 16:23's יִשְׁאַל־בִּדְבַ֣ר.
    The same happens at 2 Sam 18:20 and Jer 50:29.
  - Where MAM has a maqaf after a ketiv that is not read, at 2 Kgs 5:18 and 2 Sam 13:33,
    the reader has none (Ben, 2026-09-26). So where MAM has one compound, the reader gives
    two entries: in 2 Kgs 5:18, יִסְלַח־נא and then יְהֹוָ֥ה,
    and in 2 Sam 13:33, כִּֽי־אם and then אַמְנ֥וֹן.
  - In the Decalogue the reader takes MAM's combined text, which has the maqafs of both
    strands, so one entry can join atoms that each strand alone divides between two chanted
    words: Deut 5:6's entries include לֹ֣א־יִהְיֶ֥͏ֽה־לְךָ֛֩.
