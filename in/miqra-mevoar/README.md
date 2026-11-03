# Miqra Mevoar: the tracked text of Rabbi Kokhav's Word files

The files here hold Rabbi David Kokhav's Miqra Mevoar, a paraphrase of the Bible, for six books
of the Prophets: Joshua, Hosea, Joel, Amos, Obadiah and Jonah. Each `<stem>.json` is extracted
from one of the Word files that reach Avi, for publication on Hebrew Wikisource as the base
chapters of its Miqra Mevoar project. The project's main page gives its license as Creative
Commons Attribution-ShareAlike 3.0 Unported, and says that the attribution the license asks for
is a direct link to that page.

`py/main_miqra_mevoar.py` writes these files, `py/main_ws_bot.py miqra-mevoar` creates the
pages from them, and `doc/PLAN-miqra-mevoar.md` is the plan of record.

## What each file holds

Each file is one book: the book's name as the page titles give it; the Word file's name, size
and SHA-256; and the book's chapters, each verse with the heading before it, or null, and its
paraphrase. The extraction joins a cell's paragraphs and makes each run of whitespace one space;
it changes nothing else.

The Word files' Bible column is not kept. It is MAM's text, copied from Wikisource, which
Wikisource and MAM-simple already hold. `check` compares it with MAM-simple's verse of the same
number, so that no paraphrase lands on the wrong verse.

The Hebrew keeps each Word file's own mark order deliberately. This JSON is a faithful
intermediate of the Word files, so neither MAM-normal mark order nor Unicode normalization is
applied to it. The pages are generated in NFC, the form in which MediaWiki stores every page.

## What is not here

Neither the Word files nor the Wikisource pages are tracked, and the pCloud folder that holds the
Word files is not linked here or anywhere else in the repository. `fetch` reads the folder's
link from a file outside Git and writes it nowhere.

## Regenerating

Run each command from the repository root. First download the folder into a new directory,
`.novc/miqra-mevoar/pcloud/<timestamp>/`, giving a file that holds its public link:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py fetch --link-file <file holding the link>
```

Its `manifest.json` has each file's SHA-256. A file that differs from the previous fetch's is new
material from Rabbi Kokhav. Extract the JSON from that directory:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py extract .novc/miqra-mevoar/pcloud/<timestamp>
```

Check the extraction against the tracked JSON and MAM-simple. The check writes a report under
`.novc/miqra-mevoar/checks/`, writes nothing tracked, and exits non-zero on a failure:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py check .novc/miqra-mevoar/pcloud/<timestamp>
```

Write the pages into a new directory to preview them:

```powershell
./.venv/Scripts/python.exe py/main_miqra_mevoar.py pages --out .novc/miqra-mevoar/pages/<timestamp>
```

Then read `git diff -- in/miqra-mevoar` before any page goes to Wikisource.

The mega runs none of these commands: `fetch` downloads from a third-party host, and `extract`
and `check` read Word files that exist only where `fetch` ran. A refresh of MAM's text owes
`extract` no rerun, since it reads nothing but Word files. `check` and the suite's
`py/tests/test_miqra_mevoar_versification.py` read MAM-simple.
