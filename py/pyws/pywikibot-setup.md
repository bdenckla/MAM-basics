# Pywikibot setup for the Wikisource bot

The live bot (`main_ws_bot.py`) uses pywikibot, which needs a config
directory with credentials.  This repo tracks the config file as
`pywikibot-user-config.py` but does **not** store the password.

## One-time setup

1. Create `~/.pywikibot/` (i.e. `C:\Users\<you>\.pywikibot\`).

2. Copy the config file into it:

       cp py/pyws/pywikibot-user-config.py ~/.pywikibot/user-config.py

3. Create `~/.pywikibot/password.py` containing a single tuple with the
   bot account name and password:

       ("BDencklaBot", "your-password-here")

4. That's it.  The VS Code launch config ("Wikisource bot") already
   passes `-dir:${env:USERPROFILE}/.pywikibot` so pywikibot will find these
   files automatically.  For command-line use, pass the same `-dir`
   argument or set `PYWIKIBOT_DIR=~/.pywikibot`.
