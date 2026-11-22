# Miqra Mevoar: the places of the headings in the Torah's base chapters

Each `<OSIS abbreviation>.json` here, `Gen.json`, `Exod.json`, `Lev.json`, `Num.json` and
`Deut.json`, records where the base chapters of one book of the Torah on Hebrew Wikisource have
a heading of Rabbi David Kokhav's Miqra Mevoar, for the Torah's display pages, which
`py/main_ws_bot.py miqra-mevoar-display` creates. The five books of the Torah reached Avi long
ago as a single Word file, which `py/main_miqra_mevoar.py` never read, so `in/miqra-mevoar/`
holds none of them: their 187 base chapters were made on Wikisource before this project's bot
made the other books'. So the display pages take the places of their headings from the base
chapters themselves, through these records.

`py/main_miqra_mevoar.py base-headings` writes these files through
`py/miqra_mevoar/base_headings.py`, `py/miqra_mevoar/display_page.py` reads them, and Stage 12 of
`doc/PLAN-miqra-mevoar.md` is the plan of record.

## What each file holds

Each file is one book: the book's name, as the base chapters' titles give it, and its chapters,
each with its base chapter's page id, the id of the revision that was read, and the verses before
which that revision has a heading section, in order. A display page transcludes each heading from
its base chapter by the name of the heading's section, so it needs only the heading's place.

No text of the base chapters is kept, neither a heading nor a paraphrase: Wikisource holds them.
Nor is the time of the reading kept, so a run that finds nothing changed leaves the files as
they were.

## How the places are read

`base-headings` reads the latest revision of every base chapter anonymously and uncached,
twelve titles to a request, since a request for fifty of these long titles was refused as too
long. It parses each by a closed parser, which accepts only the line shapes that the 187 base
chapters had on 2026-11-22: those that the bot writes and a few more, which the docstring of
`py/miqra_mevoar/base_headings.py` lists. A heading line must stand directly before the verse
line of its own verse, and a base chapter's verse sections must be MAM-simple's verses of its
chapter, in order, once each. A page with any other line or order stops the run before anything
is written. A tag of another verse's section inside a verse line, as in Leviticus 21:20, is
reported and accepted, since it moves no heading.

## Regenerating and checking

Run each command from the repository root. Read the base chapters and write the records:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py base-headings
```

Then read `git diff -- in/miqra-mevoar-base-headings` before any display page of the Torah goes
to Wikisource. To check the records against the live pages, writing nothing:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py base-headings --check
```

It lists each chapter whose revision has changed since its record, and exits non-zero if any
heading has moved, appeared or vanished, or if a page does not parse. A changed revision alone is
not a failure, since the places of the headings are all that the display pages take from the
records.

The mega runs neither command, since both read live Hebrew Wikisource. Besides Wikisource,
`base-headings` reads MAM-simple's verses of each chapter, so a change to MAM-simple is a change
to its input; when nothing that it reads has changed, its records do not change. The suite's
`py/tests/test_miqra_mevoar_display.py` reads these files and MAM-simple.
