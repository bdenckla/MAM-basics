# Auto-Edits Process

I'm not sure if I ever documented this process (in GitHub, Google Docs,
MS Word, etc.), but the process just changed, so here goes.

## Steps

1. **Get a baseline** by downloading both Go (Google Sheet) and Ws
   (Wikisource) using `py/main_download_fr_google.py` and
   `py/main_download_fr_wikisource.py`.

2. **Run `py/main_diff_wsgo.py`.**

3. **Push the differences** (in auto-edit form) up to the
   `mamgo-auto-edits` repo on GitHub.

4. **Go to the MAM Google Sheet.**

5. **Run the "Import auto-edits from GitHub" script** (a `.gs` file —
   basically JavaScript, but slightly Google-specific, hence `.gs`).

6. **Run the "Apply imported auto-edits" script.**

7. **Run `py/main_download_fr_google.py`.** Auto-edits will be reflected in
   changes to CSV files in the `trope` repo and JSON files in the
   `MAM-parsed` repo.

8. **Run `py/main_diff_wsgo.py`** again to verify that the diffs go empty.
