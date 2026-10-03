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
reparses affected books.

That download changes tracked book data just as
`py/main_download.py fr-wikisource` does, so a saving run owes the same
dependent refresh: the public mega and Phonetic-MAM release, retained MAM-private
products, the final public mega, and MAM change logs. The `mam-wikisource-refresh`
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
