# Pywikibot setup for the Wikisource bot

The live bot (`main_ws_bot.py real`) uses pywikibot, which needs a config
directory with credentials.  This repo tracks the config file as
`pywikibot-user-config.py` but does **not** store the password.

## One-time setup

1. Create `~/.pywikibot/` (i.e. `C:/Users/<you>/.pywikibot/`).

2. Copy the config file into it:

       cp py/ws/pywikibot-user-config.py ~/.pywikibot/user-config.py

3. Create `~/.pywikibot/password.py` containing a single tuple with the
   bot account name and password:

       ("BDencklaBot", "your-password-here")

4. That's it.  The VS Code launch config ("Wikisource bot") already
   passes `-dir:${env:USERPROFILE}/.pywikibot` so pywikibot will find these
   files automatically.  For command-line use, pass the same `-dir`
   argument or set `PYWIKIBOT_DIR=~/.pywikibot`.

## Always pass config location explicitly

To avoid accidental cache/control files in the repo root and avoid
interactive auth surprises, always provide one of these when running
`main_ws_bot.py real` from the command line:

1. `-dir:$env:USERPROFILE/.pywikibot`
2. `PYWIKIBOT_DIR` environment variable

Examples (PowerShell):

       .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot

       $env:PYWIKIBOT_DIR = "$env:USERPROFILE/.pywikibot"
       .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json

`main_ws_bot.py real` now fails fast if neither mechanism is used.

Runtime files such as `apicache/` and `throttle.ctrl` are written under
the resolved pywikibot base directory. Supplying `-dir:` or
`PYWIKIBOT_DIR` makes that location explicit and predictable.

It also fails fast if either of these files is missing in the resolved
pywikibot directory:

- `user-config.py`
- `password.py`

## Post-run download behavior

By default, after `main_ws_bot.py real` completes its live edits, it runs
the same download function as `py/main_download.py fr-wikisource`, with a
forced download: it refetches all 36 declared special pages into
`in/mam-ws-special/`, downloads the modified chapters into `in/mam-ws` and
reparses affected books. It does so only when the run changed a chapter;
otherwise it downloads nothing.

That download changes tracked book data just as
`py/main_download.py fr-wikisource` does, so a saving run owes the same
dependent refresh: the bot run's own record, committed as the source change before
the public mega and Phonetic-MAM release, then retained MAM-private products, the
final public mega, and MAM change logs. The `mam-wikisource-refresh`
skill's section "After a Wikisource bot run" gives the procedure.

Use `--no-post-download` only when you intentionally want to skip this
automatic local refresh:

       .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-post-download

## Dry runs before a save

Neither `--no-save` nor `--identity-run` saves a live page, and each turns
off the post-run download.

`--no-save` is the dry run for an edit file. Give it the edit file and the
selector that the save will use:

       .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save

It fetches every selected chapter, applies the edits in memory, writes each
resulting chapter to the run's `chapters/` directory, and saves nothing.
Before a save it is expected to exit non-zero: after the last chapter it
stops with "no-save run found chapters that would change" and lists each
chapter that the save would change. That list should name exactly the
chapters that the edit file targets. Any other failure, such as an
`AssertionError` from an edit's guard or "Selector includes chapters outside
this edit spec target set", must be resolved before saving. An exit of zero
before a save means that no selected chapter would change, so the edit file
or the selector is wrong.

Run again after the save, with the same edit file and selector, `--no-save`
checks idempotence only for an edit kind that is idempotent, one that leaves
its own output unchanged: `kq-trivial-to-kq-trivial-2`,
`kq-trivial-2-rename-extra-alef-sug` and `kuk-special-callsite-migration`.
For those kinds an exit of zero confirms that every selected chapter already
has the edited text. The other kinds are one-shot. `meteg-removal` and
`explicit-replacement` require each `old` string to occur exactly once, and
`sigil-b2-to-t451` requires a per-chapter count of the old sigil, so after
the save a re-run fails at the first chapter whose guard it checks. That
failure shows that the old text is gone, not that the saved text is right;
compare the saving run's `chapters/` files with the dry run's instead.

`--identity-run` is a null bot. It reads no edit file, although the parser
still requires `--edits`; it gives each selected chapter back its own text
and saves nothing, so it cannot fail on a change. Use it only to exercise a
run's plumbing: the pywikibot configuration, the selector, the page reads
and the run's artifact directory.

       .venv/Scripts/python.exe py/main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --identity-run

## Introduction pages

`main_ws_bot.py intro` edits pages of MAM's introduction, which the chapter bot
cannot select. Its edit file has `"summary"`, `"edit-kind": "explicit-replacement"`
and `"pages"`, which maps a key of `in/mam-ws-intro/manifest.json`, such as `ch2`, to
a list of `{"old", "new", "comment"}` objects; each `old` must occur exactly once in
its page. It takes the same `-dir:` argument:

       .venv/Scripts/python.exe py/main_ws_bot.py intro --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-save

As with the chapter bot, `--no-save` saves nothing and, before a save, is expected to
exit non-zero, listing exactly the pages the edit file targets. A saving run then
refreshes the introduction's mirror, as `py/main_download.py fr-ws-intro` does, unless
`--no-post-download` is given; that refresh rewrites all thirteen mirrored pages, so
read its whole diff. Each run writes the edited page texts to
`.novc/mam-ws-bot-intro-runs/<timestamp>/pages/` and the saved pages' diff links to
`misc/saved-pages.json` there.

## Miqra Mevoar base chapters

`main_ws_bot.py miqra-mevoar` creates the base-chapter pages of Rabbi David Kokhav's Miqra
Mevoar from the tracked JSON in `in/miqra-mevoar/`, which `py/main_miqra_mevoar.py` writes; it
reads no edit file. `--book` names a book by its Word file's stem, such as `yehoshua`, and may be
given more than once; `--chapters FIRST-LAST` narrows the chapters of a single book. A saving
run needs `--summary`, the edit summary, which Ben approves with the run:

       .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar --book yehoshua --chapters 1-2 --no-save -dir:$env:USERPROFILE/.pywikibot

       .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar --book yehoshua --chapters 1-2 --summary "<summary>" -dir:$env:USERPROFILE/.pywikibot

Each chapter has one of four outcomes. It is a create when its page does not exist, saved with
`createonly`, so that a page someone else made in the meantime is not overwritten. It is
unchanged when the live text equals the generated text. It is an update when the texts differ
and every revision of the page is BDencklaBot's, saved with `nocreate`. It is refused when the
texts differ and someone else has edited the page: nothing is saved for it, and the run exits
non-zero, listing the other editors' revisions, since people, not the bot, reconcile a revision
from Rabbi Kokhav with an edit made on Wikisource.

`--no-save` saves nothing and, before a save, is expected to exit non-zero, listing each page
that a save would create or update. A saving run reads each saved revision back through the
API, uncached, and exits non-zero unless its bytes equal the generated text's. No MAM page
changes, so there is no post-run download. Each run writes the generated pages to
`.novc/mam-ws-bot-miqra-mevoar-runs/<timestamp>/pages/`, each chapter's outcome to
`misc/outcomes.json` there, and the saved pages' revision ids and diff links to
`misc/saved-pages.json`.

## Miqra Mevoar's base-chapter index

`main_ws_bot.py miqra-mevoar-index` completes the index of the base chapters, the page
`מקרא מבואר/פרקי בסיס`, so that it links every chapter that MAM-simple has, 929 in 39 books.
`py/miqra_mevoar/index_page.py` generates the new text from the live text: the framing above
the book sections and the category line below them keep their bytes, every old section
reappears, and the Twelve's old runs reappear within its new section. Every run reads the
index's latest revision through the API, uncached, and writes `old.wiki`, `new.wiki`,
`index.diff` and `misc/index-run.json` to `.novc/mam-ws-bot-miqra-mevoar-index-runs/<timestamp>/`:

       .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar-index --no-save -dir:$env:USERPROFILE/.pywikibot

       .venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar-index --base-revid <revision id> --summary "<summary>" -dir:$env:USERPROFILE/.pywikibot

`--no-save` prints the base revision id and the number of links, saves nothing, and, before
the save, is expected to exit non-zero, since the index would change. A saving run needs
`--base-revid`, the revision whose diff Ben reviewed, and `--summary`, both approved with the
run. It refuses unless that revision is still the latest, saves with `nocreate` and with
that revision as `baserevid` and its time as `basetimestamp`, so that an edit made since makes
MediaWiki detect a conflict, then reads the saved revision back and exits non-zero unless its
bytes equal the generated text's. The saved revision's ids and diff link go to
`misc/saved-pages.json`.

## Real-run artifact layout

Each `main_ws_bot.py real` run now writes artifacts to a fresh timestamped
directory under `.novc/mam-ws-bot-real-runs/`:

- `.novc/mam-ws-bot-real-runs/<timestamp>/chapters/`
- `.novc/mam-ws-bot-real-runs/<timestamp>/misc/warnings.json`
- `.novc/mam-ws-bot-real-runs/<timestamp>/misc/modified-chapters.json`
- `.novc/mam-ws-bot-real-runs/<timestamp>/misc/modified-chapter-diffs.md`

The chapter files are per-chapter (not per-book) and use this naming rule:

- Psalms: `D1-Psalms-009.json` (3-digit chapter padding)
- All other books: `A1-Genesis-07.json` (2-digit chapter padding)
