# Pywikibot setup for the Wikisource bot

The live bot (`main_ws_bot.py real`) uses pywikibot, which needs a config
directory with credentials.  This repo tracks the config file as
`pywikibot-user-config.py` but does **not** store the password.

## One-time setup

1. Create `~/.pywikibot/` (i.e. `C:\Users\<you>\.pywikibot\`).

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

       .venv\Scripts\python.exe py\main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot

       $env:PYWIKIBOT_DIR = "$env:USERPROFILE/.pywikibot"
       .venv\Scripts\python.exe py\main_ws_bot.py real --edits path.json

`main_ws_bot.py real` now fails fast if neither mechanism is used.

Runtime files such as `apicache/` and `throttle.ctrl` are written under
the resolved pywikibot base directory. Supplying `-dir:` or
`PYWIKIBOT_DIR` makes that location explicit and predictable.

It also fails fast if either of these files is missing in the resolved
pywikibot directory:

- `user-config.py`
- `password.py`

## Post-run download behavior

By default, after `main_ws_bot.py real` completes its live edits, it
automatically downloads the modified chapters into `in/mam-ws` and
reparses affected books.

Use `--no-post-download` only when you intentionally want to skip this
automatic local refresh:

       .venv\Scripts\python.exe py\main_ws_bot.py real --edits path.json -dir:$env:USERPROFILE/.pywikibot --no-post-download
