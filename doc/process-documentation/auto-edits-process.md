# Auto-Edits Process

I'm not sure if I ever documented this process (in GitHub, Google Docs,
MS Word, etc.), but the process just changed, so here goes.

## Steps

1. **Get a baseline** by downloading both Go (Google Sheet) and Ws
   (Wikisource) using `py/main_download.py fr-google` and
   `py/main_download.py fr-wikisource`.

2. **Run `py/main_diff.py wsgo`.**

3. **Push the differences** (in auto-edit form) up to the
   `mamgo-auto-edits` repo on GitHub.

4. **Go to the MAM Google Sheet.**

5. **Run the "Import auto-edits from GitHub" script** (a `.gs` file —
   basically JavaScript, but slightly Google-specific, hence `.gs`).

6. **Run the "Apply imported auto-edits" script.**

7. **Run `py/main_download.py fr-google`.** Auto-edits will be reflected in
   changes to CSV files in the `MAM-basics` repo and JSON files in the
   `MAM-parsed` repo.

8. **Run `py/main_diff.py wsgo`** again to verify that the diffs go empty.

## Note on `main_ws_bot.py real`

`main_ws_bot.py real` now defaults to a post-run local refresh: after it
edits live Wikisource pages, it downloads the modified chapters into
`in/mam-ws` and reparses affected books. Use `--no-post-download` only if
you intentionally want to skip that refresh.

Run artifacts for `main_ws_bot.py real` are now isolated under
`.novc/mam-ws-bot-real-runs/<timestamp>/`, with per-chapter JSON files in
`chapters/` and warnings/diff metadata in `misc/`.
