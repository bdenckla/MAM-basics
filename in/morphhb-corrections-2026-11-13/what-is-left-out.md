# What this folder holds, and what it leaves out

Written by Claude (Opus 5.5) on 2026-11-15, when the files beside it were copied.

1. **What this folder is.** It holds 29 of the 387 files of a report that a Claude session wrote
   on 2026-11-13, copied byte for byte on 2026-11-15. The report is Claude's analysis of which
   of WLC's readings morphhb, the Open Scriptures Hebrew Bible, corrects; no human has reviewed
   it. The 29 files are:
   - its `README.md`;
   - the 27 files of its `out/` that `gh-pages/morphhb-corrections/index.html` reads;
   - `out/fetch_log.jsonl`, the log of every file it fetched.

   Ben asked on 2026-11-15 for the page and its sources to be tracked, "as long as they are not
   large", and chose this set that day; everything else in the report's folder counts as large.
   The files are not edited: `README.md` is the report's own, so its paths name the report's
   folder as it stood untracked, and 14 of the files name paths on the machine where the report
   ran. Eight of the `out/` files end their lines with CRLF, and five have line-final blanks or
   blank lines at their end, so a rule in `.gitattributes` keeps the bytes of every `out/` file
   here.
2. **What was left out, with sizes.** The report's folder, with all of these, stays untracked in
   the ignored `.novc/` folder of the clone where it was written.
   1. `fetched/`: 229 files, 144,018,723 bytes:
      - morphhb's `wlc/` at its commit `d4265dfa`: 40 files, 28,634,506 bytes;
      - 137 older versions of 10 books: 110,194,602 bytes;
      - GitHub's records of morphhb's commits, issues and comments, with one listing: 52 files,
        5,189,615 bytes.
   2. `scripts/`: 74 files, 603,954 bytes: 64 scripts (412,761 bytes), `README.template.md`
      (27,490 bytes) and 9 bytecode files (163,703 bytes).
   3. The other 55 files of `out/`: 29,610,687 bytes, among them `out/51-general-test.json`,
      20,407,848 bytes, and `out/42-text-units.json`, 5,803,158 bytes.
3. **What regenerating each would take.**
   1. **`fetched/`:** fetching every file again. `out/fetch_log.jsonl` has one line for each of
      the 229, with its API path, byte count, SHA-256 and Git blob hash, so a file fetched again
      at its pinned commit can be checked byte for byte. GitHub's records of issues and comments
      would differ wherever morphhb has had activity since 2026-11-13.
   2. **The other `out/` files:** running the report's scripts on `fetched/`.
   3. **`scripts/`:** nothing regenerates them; they are the report's source. None of them runs
      from the tracked tree. 33 of the 64 modify `sys.path`, which tracked code never does. 13
      name an untracked folder of WLC 4.18's files, and they read `fetched/`. Porting them is a
      separate and much larger task than tracking these files.
4. **What is generated from this folder.** `gh-pages/morphhb-corrections/index.html` and its link
   table in `out/morphhb-corrections/` are generated from these files and from the review of the
   Israel Bible's generated page. `py/author_misc/morphhb_corrections_index.py` is the generator:
   `py/main_authored.py gen-morphhb-corrections` and the mega's step `morphhb-corrections` run it.
   Where the report's data show its README to be wrong or imprecise, the page says so, in its
   section "Where this page departs from the report"; the copies here stay as the report wrote
   them.
