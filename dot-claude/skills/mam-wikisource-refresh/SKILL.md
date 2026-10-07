---
name: mam-wikisource-refresh
description: Refresh MAM chapter and declared special-page data from Hebrew Wikisource and regenerate, audit, commit, and publish affected products and MAM change logs. Use when Ben asks to download, update, or refresh Hebrew Wikisource book data, and after a live Wikisource bot run whose post-run download changed tracked book data. Do not use for the separately mirrored MAM introduction, for preparing or saving bot edits, or for the frozen Google Sheet.
---

# Refresh MAM from Hebrew Wikisource

Use this workflow for MAM chapter and declared special-page downloads from Hebrew Wikisource.
Every `fr-wikisource` run refreshes the selected chapters and all 36 special pages. Coordinate the
repositories' existing entry points; do not create a new orchestration program. The source change
is committed before the mega runs, as "Judge every diff: the expected changes, and only them"
says, and MAM change logs are committed only after the dependency loop returns to its final
MAM-basics state. The change-log generator compares the latest release with committed `HEAD`;
dirty `MAM-parsed/plus` data is invisible to that comparison.

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

The ordinary one-repository cloud checkout lacks the private adapter and regeneration inputs,
so stop before the download and report the unavailable dependency loop. Installing this skill supplies its
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
dependent refresh as a download, since it changes `MAM-parsed/plus` just as a download does.
Complete the dependent refresh below. Its first commit is the bot run's own record, rather than a
separate `Refresh MAM from Wikisource`: the post-run download's chapters, revisions and reparse,
with a new entry in `py/ws/ws_bot_edit_history.md`. That record is the source change that "Judge
every diff: the expected changes, and only them" commits before the mega runs; the mega's
products follow in commits of their own.

Ben decided on 2026-10-01 that the bot run's own commit also takes every change that the post-run
download made under `in/mam-ws-special/`. The bot saves only chapter pages, and only eight of the
36 special pages are chapter pages, so a special page that the bot changed is one of those eight
that it saved in this run; every other change there is someone else's edit made since the mirror
was last downloaded. The commit message names each changed special page and says whether the bot
saved it.

## Judge every diff: the expected changes, and only them

The agent's judgment keeps a refresh honest; no hash, fingerprint or pinned population
does. Ben chose this standard on 2026-10-07 as "a good use of AI's approximate
not-quite-reasoning".

1. **Commit the source change first.** Commit the download's chapters, revisions and
   reparse, or a saving bot run's record, before the mega runs.
2. **Predict.** Read the change verse by verse with `py/main_diff.py mpplus --old
   <starting HEAD> --new HEAD --output <scratch path>`. Write down what it should cause:
   which verses, in which products, of what kind (a renamed template, a reordered
   ketiv/qere pair, a changed accent), and which counts move, by how much.
3. **Judge.** After each regeneration, read every tracked diff and check (a) that every
   predicted change is present and (b) that nothing else changed. Explain anything else,
   or stop.
4. **Record.** Each regeneration commit's message states the prediction and confirms (a)
   and (b), product by product.

The checks that remain are closed dispatch, and checks that a hand-made statement about
the data still holds: a prose claim, a quoted form, a stored pointed ketiv. Such a
statement does not change when the data does, so no diff shows it going stale. When one
fails, repair the statement, or the derived record and what it records, in one
reviewable edit. When the statement is Ben's published claim, stop for his approval and
let the rest of the refresh proceed.

## Complete the dependent refresh

When chapter data or chapter metadata changed, read and follow
[references/dependent-refresh.md](references/dependent-refresh.md) before running a generator.
That reference governs the complete MAM-basics → MAM-private → MAM-basics dependency
loop, the public Phonetic-MAM release, the separate change-log commit, final gates, push
order and clean remote-state check. phonetic-hbo remains a frozen redirect and historical
issue host; dependent refresh does not restore or write its clone.

When only `in/mam-ws-special/` changed, inspect its manifest and all changed raw pages, run the
suite, and commit the special-page refresh without entering the dependent product loop. One
generator family reads the mirror: the printed-Decalogue data and the accgram pages built on it
read `decalogue-base.mediawiki`. When that page changed, run
`./.venv/Scripts/python.exe py/main_accgram.py run-printed-decalogue` and
`./.venv/Scripts/python.exe py/main_accgram.py generate-html` after the special-page commit,
judge their diffs as "Judge every diff: the expected changes, and only them" says, and commit the
explained products in a commit of their own.

The downstream preflight happens before the first public exporter read and before every private
write. A clean checkout is necessary but does not prove that the checkout is unowned: if MAM-private is dirty, is attached
to another active task, or cannot be assigned unambiguously to this refresh, stop and require a
handoff. Expected dependent regeneration is regeneration, not a failed census. A dependent
generator that legitimately produces no diff needs no commit; never create an empty commit.

Any unexplained diff, unresolved failed check, stale input, changed recorded `HEAD`, or
ambiguous ownership stops the workflow before pushing; a check that awaits Ben's approval holds
only the push. The surrounding user and repository instructions govern integration and push
authority; this skill does not grant them.

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
