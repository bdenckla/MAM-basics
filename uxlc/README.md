# UXLC and CLC resources in MAM-basics

This product directory holds data and documentation around UXLC (the Unicode/XML Leningrad Codex) and the planned CLC edition. MAM-basics owns the programs that read and write those resources.

- `in/` holds the arriving UXLC inputs, including notes, non-canonical source members, change logs, and corrected overrides.
- `out/` holds the arriving generated change-log artifacts and hand-authored mapping prose.
- `data/` holds the arriving lookup table that other MAM-basics code reads.
- `doc/` holds the [CLC design](doc/clc-design.md) and its skeleton plan.

The canonical UXLC book XML, `in/UXLC-39/`, and the canonical shared change-log inputs remain at the MAM-basics root rather than being duplicated under `uxlc/`. The published pages are under [`../gh-pages/uxlc/`](../gh-pages/uxlc/) and are served at [bdenckla.github.io/MAM-basics/uxlc/](https://bdenckla.github.io/MAM-basics/uxlc/).

From the MAM-basics root, [`../py/main_0_mega.py`](../py/main_0_mega.py) regenerates the UXLC output, in its five steps from `uxlc-check-changes` to `uxlc-word-list`, and [`../py/main_clc.py`](../py/main_clc.py) regenerates the CLC output. An unexplained generated diff is a failure.
