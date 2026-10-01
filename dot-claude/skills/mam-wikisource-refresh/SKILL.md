---
name: mam-wikisource-refresh
description: Refresh MAM chapter and declared special-page data from Hebrew Wikisource and regenerate, audit, commit, and publish affected products and MAM change logs. Use when Ben asks to download, update, or refresh Hebrew Wikisource book data, and after a live Wikisource bot run whose post-run download changed tracked book data. Do not use for the separately mirrored MAM introduction, for preparing or saving bot edits, or for the frozen Google Sheet.
---

# Refresh MAM from Hebrew Wikisource

Use this workflow for MAM chapter and declared special-page downloads from Hebrew Wikisource.
Every `fr-wikisource` run refreshes the selected chapters and all 36 special pages. Coordinate the
repositories' existing entry points; do not create a new orchestration program. A changed chapter
refresh is committed before dependent regeneration, and MAM change logs are committed only after
the dependency loop returns to its final MAM-basics state. The change-log generator compares the
latest release with committed `HEAD`; dirty `MAM-parsed/plus` data is invisible to that comparison.

The commands below run from the verified MAM-basics development checkout. A full clone uses
its own interpreter; a linked worktree names its home clone's interpreter by absolute path.
The examples show Windows `.venv/Scripts/python.exe`; a Linux checkout uses `.venv/bin/python`
from its own environment hydrated against tracked requirements and constraints.
Keep network approval, integration, and push
authority within the surrounding user and repository instructions; this skill does not grant
them.

## Claude cloud preflight

Before starting a chapter download in a Claude cloud session, read
`references/dependent-refresh.md` and require every checkout, environment, owned input,
generator and integration capability needed for its complete dependency loop. The download
command also reparses affected books and can write products. A successful public API request
does not establish that the full refresh can finish.

The ordinary one-repository cloud checkout lacks MAM-private and phonetic-hbo, so stop before
the download and report the unavailable dependency loop. Installing this skill supplies its
rules without enabling a partial refresh. A mega run with declared cloud skips does not
verify the missing private regeneration or satisfy the complete refresh procedure. Keep
pywikibot account configuration and authorization separate from this public download workflow.

## Verify the checkout

Before downloading anything:

1. Record the absolute top level, current `HEAD`, and branch. Require a branch or establish the
   worktree branch through the applicable worktree procedure.
2. Require clean `git status --porcelain=v1 -z` output, and record the starting `HEAD` for the
   collision check before the first commit.
3. When a required source commit was supplied, require that commit to equal `HEAD` or be an
   ancestor. Refresh `origin/main` when the surrounding instructions require a current remote
   baseline.
4. Confirm that the selected clone's interpreter exists. A worktree uses its home clone's
   interpreter; never copy, junction, or symlink the home clone's `.venv` into a worktree.
5. On Windows when repository ownership differs, pass the development checkout's exact absolute
   path through `git -c "safe.directory=<DEV>" -C "<DEV>"` on every Git invocation. Never add a
   global trust exception.

Keep one writer in the checkout. If the starting state is dirty or the checkout identity is not
the expected one, stop before the download.

## Download and decide whether work exists

Run the book-data download without `--force-download`:

```powershell
./.venv/Scripts/python.exe py/main_download.py fr-wikisource
```

Use `--force-download` only when Ben explicitly requests a forced download. After the command,
inspect NUL-delimited Git status before running another generator. Classify raw chapter
outputs under `in/mam-ws/`, chapter metadata in `in/mam-ws-revisions.json` and special-page
outputs under `in/mam-ws-special/` separately from the download's own regeneration. That
regeneration writes affected book JSON under `out/mam-ws-parsed-fmt-2/` and `MAM-parsed/plus/`,
the declared support files under `MAM-parsed/py-examples/`, documentation under
`gh-pages/MAM-parsed/` and `doc/mp-claims.md`. Inspect every generated diff against the actual
`parse_ws.almost_main` and `parse_ws_products.generate_production` outputs; an unexplained
path or diff blocks the workflow. If status is completely clean, report that the Wikisource data is
already current and stop: do not run mega, commit, or push. If no tracked file changed but
expected untracked output remains, report that unexpected residue and stop for cleanup or
direction; do not run mega, commit, or push. Generated changes without chapter data or metadata
changes also need an explanation; do not report unchanged source data as a completed refresh
with dirty products.

## After a Wikisource bot run

A live `py/main_ws_bot.py real` run that saves pages includes a download: unless
`--no-post-download` is given, it calls `download_wikisource.run`, the function every
`fr-wikisource` download runs, with a forced download. That download refetches all 36 declared
special pages into `in/mam-ws-special/`, then force-downloads exactly the chapters the bot saved
into `in/mam-ws/` and `in/mam-ws-revisions.json`, and reparses those books. It takes the place of
the one above. Ben decided on 2026-09-27 that a bot run which changes tracked book data owes the same
dependent refresh as a download, since it changes `MAM-parsed/plus` just as a download does and
leaves MAM-private's census stale until the refresh runs. Complete the dependent refresh below.
Its first commit is the bot run's own record, the saved chapters' regenerated outputs with a new
entry in `py/ws/ws_bot_edit_history.md`, rather than a separate `Refresh MAM from Wikisource`.

## Complete the dependent refresh

When chapter data or chapter metadata changed, read and follow
[references/dependent-refresh.md](references/dependent-refresh.md) before running a generator.
That reference governs the complete MAM-basics → MAM-private → phonetic-hbo → MAM-basics
dependency loop, the separate change-log commit, final gates, push order, and clean remote-state
check.

When only `in/mam-ws-special/` changed, inspect its manifest and all changed raw pages, run the
suite, and commit the special-page refresh without entering the dependent product loop. The
special-page mirror is archival input and no product generator reads it.

The downstream preflight happens before any downstream write. A clean checkout is necessary but
does not prove that the checkout is unowned: if MAM-private or phonetic-hbo is dirty, is attached
to another active task, or cannot be assigned unambiguously to this refresh, stop and require a
handoff. Expected dependent regeneration is regeneration, not a failed census. A dependent
generator that legitimately produces no diff needs no commit; never create an empty commit.

Any unexplained diff, failed gate, stale input, changed recorded `HEAD`, or ambiguous ownership
stops the workflow before pushing. The surrounding user and repository instructions govern
integration and push authority; this skill does not grant them.

## Separate workflows

- The separately mirrored MAM introduction is not this workflow. Read
  `in/mam-ws-intro/README.md` completely and follow its independent refresh procedure; do not
  treat the bare `py/main_download.py fr-ws-intro` command as the whole procedure.
- Preparing, dry-running, and saving Wikisource bot edits is an outward-facing workflow of its
  own, documented in `py/ws/pywikibot-setup.md`. Only the dependent refresh after a saving run
  belongs here.
- The former MAM Google Sheet has been a frozen historical archive since September 12, 2026; it
  has no refresh workflow.

This skill's canonical copy is `MAM-basics/dot-claude/skills/mam-wikisource-refresh/`. It is
shared with Codex through `dot-claude/shared-skills.txt` and reaches both live skill homes only
through the deployment procedure in `MAM-basics/dot-claude/README.md`.
