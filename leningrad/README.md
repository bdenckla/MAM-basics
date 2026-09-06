# Leningrad Codex index data in MAM-basics

This product directory holds data for the Leningrad Codex index. MAM-basics owns the generator; this directory holds its input-adjacent artifacts and the hand-made image evidence.

- [`lenin-wiki/`](lenin-wiki/) holds the generated Wikisource-page index files. [`../py/main_lenin_wikisource_page.py`](../py/main_lenin_wikisource_page.py) reads MAM-basics' canonical `uxlc/data/lci_augrecs.json` and writes the three files in `lenin-wiki/`. Its wikitext is a starting point for manual Wikisource work, not a mirror of the page that Wikisource now publishes.
- [`page-snips/`](page-snips/) holds hand-made crops of Leningrad Codex page images, one crop for each fact established from a manuscript image. [`page-snips/README.md`](page-snips/README.md) describes the naming convention, sources, and evidence for every crop.
