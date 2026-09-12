# MAM-OSIS
This product directory has an extract of MAM in OSIS format.

Its source is MAM's Hebrew Wikisource text, through the Wikisource-derived
`MAM-parsed/plus/` and `MAM-simple/` products in this repository.

This OSIS MAM is intended for conversion to SWORD format, for use by STEPBible &amp; CrossWire.

## How current this product is

**This product is not kept continuously current, and has not been since 2026-09-12.**
Until that date, MAM-basics' whole-pipeline run, "mega", regenerated it on every run,
so it tracked the Wikisource text within a run.
It is now regenerated only when someone runs `py/main_mam_osis.py` deliberately,
which means it can lag `MAM-simple/` and `MAM-parsed/plus/` by any amount.

The reason is that this extract reaches STEPBible and CrossWire only when
Ben Denckla converts and delivers it,
so a continuously regenerated extract was not reaching anyone any sooner.

To bring it up to date, run, from the MAM-basics repository root:

```
.venv/Scripts/python.exe py/main_mam_osis.py
```

That reads `MAM-simple/`, so regenerate MAM-simple first if the Wikisource text has
moved since this product was last written.

MAM-basics also publishes [documentation for MAM OSIS](https://bdenckla.github.io/MAM-basics/MAM-OSIS/) via GitHub Pages.
