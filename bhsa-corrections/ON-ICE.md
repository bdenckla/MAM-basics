# The BHSA-corrections study, on ice

**Claude (Opus 5.5) wrote this note on 2026-11-17. The study it describes is Claude's work of
2026-11-13, and no human has reviewed the study.**

This directory is the frozen record of a study: Claude's research, of 2026-11-13, into where the
ETCBC's BHSA (Biblia Hebraica Stuttgartensia Amstelodamensis), version 2021, "corrects" its own
text, that is, where the ETCBC's analysis of a word departs from the word as the BHSA's own text
writes it. [`README.md`](README.md) is the study's report; its two sections "The answer", in
Part 1 and Part 2, give what the study found. The study was written in the folder
`.novc/bhsa-corrections-2026-11-13/` of the clone `C:/Users/BenDe/GitRepos/MAM-basics`, a
folder that Git ignores. That folder, here called the study folder, stays there, untracked.

## Put on ice

Ben's instruction of 2026-11-17, verbatim:

> Put this "on ice", i.e. git-track this work somewhere (assuming it is less that 15Mb) so that
> we can return to it some day (or never, but we'd like to have the option)

The session that received the instruction decided to track the study here, as a new top-level
directory of MAM-basics, and to leave the BHSA's data out. That session followed two
precedents: the frozen record
[`../in/morphhb-corrections-2026-11-13/`](../in/morphhb-corrections-2026-11-13/), whose
`what-is-left-out.md` this note follows, and the on-ice study
[`../morphhb-on-mam/`](../morphhb-on-mam/). Nothing here is a generator: no program in `py/`
writes these files or builds anything from them, and the mega runs nothing here.

## What this directory holds

87 files: this note, and 86 others, 4,059,816 bytes, copied or made on 2026-11-17.

1. **`README.md`**, 36,486 bytes: the study's report, byte for byte. It is not edited, so its
   paths name the study folder as it stood untracked, and its statement that nothing was
   committed describes 2026-11-13. It names files that are not tracked here: those of the study
   folder's `fetched/`; those of its `scripts/`, which are in `scripts.zip` instead; and
   `out/32-part2-scan.json`, which its Test B table gives as the file of the class "both". Left
   as written, it says that the study fetched eleven pages of the ETCBC's documentation, where
   `in/fetch_log.jsonl` and `out/docs/` have twelve, the twelve that its Part 2 names.
2. **`out/`**, 80 files, 3,740,258 bytes: every file of the study folder's `out/` and
   `out/docs/` but the two scans named under "What was left out", byte for byte.
   - `00-` to `03-`, 4 files, 19,299 bytes: the checks of the copies and fetches of the BHSA's
     files, the census of their headers and values, and WLC 4.18's table of notes.
   - Part 1, `10-` to `15-`, `20-` and `34-`, 10 files, 502,476 bytes.
   - Part 2, `30-`, `31-`, `33-`, `35-` and `36-`, 8 files, 166,013 bytes.
   - Claude's checks of the sub-agents' findings, `37-` to `42-`, 6 files, 12,083 bytes.
   - The outputs of the five sub-agents' scripts, `p2a-` to `p2e-`, 39 files, 2,995,927 bytes.
   - `fetch_log.jsonl`, 18,349 bytes, the log of the study's 44 fetches: 32 of the BHSA's
     feature files, each by one GitHub API request, and 12 documentation pages.
   - `docs/`, 12 files, 26,111 bytes: the text of those 12 pages.
3. **`in/`**, 4 files, 136,529 bytes, which pin the BHSA's data and state its licence:
   - `fetch_log.jsonl`, the same bytes as `out/fetch_log.jsonl`, which stays in `out/` because
     `README.md` names it there. Its 32 `raw` records give each feature file's API path at the
     pinned commit, its size, its SHA-256 and its Git blob SHA-1; its 12 `polite` records give
     each page's URL, size and SHA-256.
   - `etcbc-bhsa-tf2021-listing.json`, 108,321 bytes: the GitHub API's listing of the folder
     `tf/2021/` of ETCBC/bhsa at the commit `4db00e2157915495e1a4d3d57e41223df24775da`, here
     called the pinned commit, with the size and Git blob SHA-1 of each of its 118 entries: 117
     feature files and `__checkout__.txt`.
   - `etcbc-bhsa-tf-listing.json`, 5,171 bytes: the listing of `tf/` at the pinned commit,
     which names its seven version folders.
   - `etcbc-bhsa-README.md`, 4,688 bytes: ETCBC/bhsa's `README.md` at the pinned commit, which
     states the data's licence.

   The last three are byte for byte the study folder's
   `fetched/etcbc-bhsa-tf2021-listing/contents.json`,
   `fetched/etcbc-bhsa-tf-listing/contents.json` and `fetched/etcbc-bhsa-readme/README.md`. An
   earlier Claude session, here called the MACULA session, fetched them on 2026-11-13, one
   GitHub API request each, into its untracked folder `.novc/macula-al-beiti-2026-11-12/`, and
   the study copied them from there. Each one's SHA-256 equals the one that the MACULA
   session's `out/fetch_log.jsonl` recorded.
4. **`scripts.zip`**, 146,543 bytes: the study folder's `scripts/` but its `__pycache__/`, with
   its paths kept: 49 Python scripts and `README.template.md`, from which
   `scripts/make_readme.py` wrote `README.md`; 414,168 bytes uncompressed. The scripts put
   directories on `sys.path`, which tracked code never does, and they name absolute paths on
   the machine where the study ran, so they are archived rather than tracked as `.py` files.
   Each entry was checked against its source.

Four files of `out/` end their lines with CRLF, 19 others have line-final blanks or blank lines
at their end, and `in/etcbc-bhsa-README.md` has three line-final blanks, so rules in
`.gitattributes` keep their bytes and stop `git diff --check` from reporting them.

## What was left out

The study folder keeps these, untracked. Of its 197 files, 93,069,796 bytes, not counting the
folder `ice/` in which this directory was assembled, 134 are tracked here, 50 of them inside
`scripts.zip`, and these 63 are not:

1. **58 of the 61 files of `fetched/`**, 78,474,741 of its 78,592,921 bytes; the other three are
   in `in/`. The 58 are:
   - the 44 feature files of the BHSA 2021, 77,987,780 bytes, the largest `oslots.tf`, of
     13,526,306 bytes;
   - the 12 documentation pages, from https://etcbc.github.io/bhsa/, 475,876 bytes;
   - GitHub's records of the repository ETCBC/bhsa and of its branch `master`, `repo.json` and
     `branch.json`, 11,085 bytes.
2. **The two scans**, 10,229,546 bytes, which their scripts regenerate:
   `out/32-part2-scan.json`, 3,681,738 bytes, from `scripts/part2_scan.py`, and
   `out/p2d-scan.json`, 6,547,808 bytes, from `scripts/p2d_scan_atoms.py`.
3. **`scripts/__pycache__/`**, 3 files of bytecode, 56,417 bytes.

## How to return to the work

1. Unzip `scripts.zip` into a new untracked folder, for example a new folder under the `.novc/`
   of the clone `C:/Users/BenDe/GitRepos/MAM-basics`. The scripts take the folder that holds
   their `scripts/` as theirs: they read its `fetched/` and write its `out/`.
2. Copy `in/etcbc-bhsa-tf2021-listing.json` to `fetched/etcbc-bhsa-tf2021-listing/contents.json`
   in that folder, where `scripts/fetch_bhsa_features.py` reads it.
3. Fetch again the 44 feature files of the BHSA 2021 at ETCBC/bhsa
   `4db00e2157915495e1a4d3d57e41223df24775da`, one GitHub API request at a time. Twelve were
   first fetched by the MACULA session and copied into the study folder by
   `scripts/copy_from_macula.py`, as `out/00-copy-from-macula.txt` records: `book`, `chapter`,
   `function`, `g_word_utf8`, `lex`, `oslots`, `otype`, `pdp`, `sp`, `trailer_utf8`, `typ` and
   `verse`. The other 32 were fetched by `scripts/fetch_bhsa_features.py`, as
   `out/01-fetch-features.txt` records. That script fetches any of the 44 by name, each by one
   request through `scripts/gh_fetch.py`, into `fetched/etcbc-bhsa-2021-<feature>/`, and logs
   each in `out/fetch_log.jsonl`; its docstring gives its arguments. While the MACULA session's
   folder still exists, `scripts/copy_from_macula.py` can copy the twelve from it instead. It
   copies the listing too, so it takes the place of step 2, and it must run before
   `scripts/fetch_bhsa_features.py`.
4. Check each file against the tracked listing's size and Git blob SHA-1.
   `scripts/fetch_bhsa_features.py` and `scripts/copy_from_macula.py` both do so, and stop at a
   mismatch. `in/fetch_log.jsonl` also gives the SHA-256 of the 32 that the study fetched
   itself.
5. Fetch the documentation pages again only if they are needed, with `scripts/fetch_docs.py`,
   which reads through MAM-basics' `mb_cmn.polite_download`, obeying robots.txt; their 12 URLs
   are in `in/fetch_log.jsonl`. The site may have changed since 2026-11-13.
6. Rerun the scripts as the section "Data, rights and files" of `README.md` and each script's
   docstring say: from the MAM-basics root, with
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -I`. Then compare what they
   write with the tracked `out/`: every difference is a finding until it is explained.

## Inputs outside this directory

- **WLC 4.18** is untracked: Sefaria-Data's copy of tanach.us's build 24.2, under the
  `.novc/wlc418-tanach-us/` of the clone `C:/Users/BenDe/GitRepos2/MAM-basics`.
  `scripts/bc_common.py` names its folder of books by absolute path.
- **MAM-basics.** `scripts/bc_common.py` names the clone `C:/Users/BenDe/GitRepos/MAM-basics` by
  absolute path, puts its `py/` on `sys.path` and imports its modules, among them
  `author_misc.israel_bible_review_index` and `mb_cmn.uni_denorm`. The scripts read that clone's
  MAM-simple, `out/wlc420-u/`, `out/wlc422-u/` and `in/UXLC-39/`. The study did not record
  which commit it read. That clone's reflog shows its HEAD at `df516a00` from 2026-11-12 to
  2026-11-14, so the study presumably read the files of `df516a00`, unless the working tree
  then held uncommitted changes.
- **The MACULA session's folder**,
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/macula-al-beiti-2026-11-12/`, untracked, which
  `scripts/copy_from_macula.py` reads. On 2026-11-17 it still held the twelve feature files and
  its fetch log.
- **The study's brief**, `.novc/commander-session/bhsa-corrections-brief-2026-11-13.md` in the
  clone `C:/Users/BenDe/GitRepos/MAM-basics`, untracked, which quotes Ben's request; `README.md`
  and several scripts' docstrings name it.
- **GitHub's command-line tool**, `gh`, which `scripts/gh_fetch.py` runs for each API request.

Several tracked files name absolute paths on the machine where the study ran, among them every
record of `in/fetch_log.jsonl` and `out/fetch_log.jsonl`.

## Licence

- **The BHSA's data are the ETCBC's, under CC BY-NC 4.0.** The BHSA's README,
  `in/etcbc-bhsa-README.md`, says so, as does the home page of its documentation, whose text is
  `out/docs/index.txt`. Both ask that the data be cited by their persistent identifier, DOI
  10.17026/dans-z6y-skyh, and not be used commercially without consent. GitHub's licence field
  for the repository says MIT; this directory follows the README. So the files of `out/` that
  quote or derive from the BHSA or its documentation are the ETCBC's, under that licence.
- **Claude's prose and code are MAM-basics' own work, so GPL-3.0:** `README.md`, this note, the
  scripts in `scripts.zip`, the sub-agents' reviews in `out/`, and the fetch logs. What they
  quote from the BHSA keeps the ETCBC's licence.
- **The forms quoted from other texts keep their own terms:** WLC's text is in the public
  domain, the UXLC's keeps tanach.us's terms, and MAM's is under CC BY-SA 4.0.
