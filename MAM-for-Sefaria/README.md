# MAM-for-Sefaria in MAM-basics

This product directory contains an extract of MAM (Miqra According to the Masorah) suitable for import into Sefaria.

The source of this data is MAM's Hebrew Wikisource text, through the
Wikisource-derived `MAM-parsed/plus/` and `MAM-simple/` products in this repository.

## How current this product is

**This product is not kept continuously current, and has not been since 2026-09-12.**
Until that date, MAM-basics' whole-pipeline run, "mega", regenerated it on every run,
so it tracked the Wikisource text within a run.
It is now regenerated only when someone runs `py/main_mam4sef.py` deliberately,
which means it can lag `MAM-simple/` and `MAM-parsed/plus/` by any amount.

The reason is that Sefaria takes an update only when Ben Denckla asks it to,
so a continuously regenerated extract was not reaching anyone any sooner.
The extract already differed from the edition published on the Sefaria web site,
because Sefaria does not take updates as frequently as this directory received them;
what has changed is that this directory no longer receives them automatically either.

To bring it up to date, run, from the MAM-basics repository root:

```
.venv/Scripts/python.exe py/main_mam4sef.py --both-sef-and-ajf
```

That reads `MAM-simple/`, so regenerate MAM-simple first if the Wikisource text has
moved since this product was last written.

Other versions/formats of MAM (each with their tradeoffs) include:

* [MAM-simple](../MAM-simple/)
* [MAM-parsed](../MAM-parsed/README.md)

MAM-basics publishes the [documentation of the MAM-for-Sefaria encoding](https://bdenckla.github.io/MAM-basics/MAM-for-Sefaria/).

Questions? Email maintainer@miqra.simplelogin.com.
