# morphhb's morphology on MAM: a feasibility study, on ice

**Claude (Opus 5.5) wrote this study on 2026-11-15 and this record of it on 2026-11-16. No human
has reviewed any of it.**

This directory is the frozen record of a feasibility study: can the morphology of
[morphhb](https://github.com/openscriptures/morphhb), the Open Scriptures Hebrew Bible, be
applied to MAM's text? morphhb's `wlc/` files mark up the Westminster Leningrad Codex word by
word, giving each word, a `<w>` element, a lemma, a morph code and an id. The study aligned
those words with MAM's atoms, an atom being one written form between spaces or maqaf marks,
and asked how many atoms could take morphhb's analysis as it stands. Its page,
[`out/morphhb-on-mam.html`](out/morphhb-on-mam.html), gives the method, the results and
examples; [`out/40-page-text.txt`](out/40-page-text.txt) is the page's visible text.

## Put on ice

Ben's instruction of 2026-11-16, verbatim:

> put this work "on ice" (deep storage), i.e. git-track it somewhere. Whether that "somewhere"
> should be MAM-basics or my fork of morphhb is your choice.

The session that received it chose MAM-basics, following the frozen HBCE Psalms study in
[`../hbce-psalms/`](../hbce-psalms/). The study's working folder,
`.novc/morphhb-on-mam-2026-11-15/`, which was never tracked, became this directory, the package
[`../py/morphhb_on_mam/`](../py/morphhb_on_mam/) and its entry point
[`../py/main_morphhb_on_mam.py`](../py/main_morphhb_on_mam.py). The outputs record one run.
The program is rerun only if the work resumes; the mega does not run it, and
`py/tests/test_mega_coverage.py` declares why.

## What the study found

From `out/30-figures.json`: of MAM's 306,525 atoms, 99.64% take morphhb's lemma, morph and id
with evidence that they fit. 297,837 (97.17%) have the same form as their morphhb word, and
7,597 (2.48%) differ in form but have that lemma and morph elsewhere in morphhb. The other
1,091 (0.36%) need a rule or a person: 707 are untested, because MAM's form occurs nowhere else
in morphhb; 59 are flagged, because MAM's form occurs elsewhere in morphhb but never with this
lemma and morph; and 325 are structural, with no one-to-one partner. The page explains each
tier, shows examples, and says what the study could not establish.

The research behind the page's sections 6 and 7 is in `research/`: what morphhb's maintainers
say and do about other codices, ids and `MAPM/` (`research/upstream/FINDINGS.md`), how
MAM-morphhb is made and how much MAM's text changes from one refresh to the next
(`research/upkeep-shape/FINDINGS.md`), and which of those reports' claims the study's root
session checked (`research/CHECKED.md`).

## The decision page

The questions that the study raises for Ben are on its decision page, a private artifact at
https://claude.ai/artifact/6cWmkc1DXdxMcr797YU4TX. Its source is
[`decisions.html`](decisions.html), the artifact's second version, of 2026-11-16, which says
that the study is on ice and names the study's page by its path here; it was written to the
Artifact page contract, so it has no doctype of its own. All six decisions are open, and wait
until the work resumes.

## Inputs

- **morphhb** `wlc/` at `db6c5c9b` (openscriptures/morphhb's master on 2026-11-15). Its `wlc/`
  tree, `0ee59fa2`, is the same tree as `d4265dfa`'s. morphhb's files are not in this
  repository. [`in/fetched/morphhb-wlctree-1.json`](in/fetched/morphhb-wlctree-1.json) is the
  GitHub API's listing of that tree, byte for byte as the study fetched it, with the Git blob
  SHA-1 of each of its 40 files, the 39 books and `VerseMap.xml`;
  [`in/fetch_log.jsonl`](in/fetch_log.jsonl) logs that read and the study's four others, of two
  commits and two root trees, whose responses were not kept here. The study read the copies
  that the 2026-11-13 study had fetched, described in
  [`../in/morphhb-corrections-2026-11-13/README.md`](../in/morphhb-corrections-2026-11-13/README.md).
- **MAM**: MAM-simple's JSON in the BHS versification (`MAM-simple/json-vtrad-bhs/`, falling
  back to `json-vtrad-mam/` as MAM-simple's incremental rule says), as it stood
  at the checkout's `374d9436`.
- **The page's own inputs**: [`in/page-spec.md`](in/page-spec.md), the specification its
  builder followed, and [`in/page-fragment.html`](in/page-fragment.html), the sections that the
  study's root session wrote from the research reports. Their paths were updated on 2026-11-16
  to this layout, and `in/page-spec.md` says so.

`py/morphhb_on_mam/build_page.py` reads three of these facts from this README, as the study's
script read them from the study folder's: the commits in the first two items and the time in
the next section. Keep those sentences' wording when editing them.

## Regenerating the outputs

From the root of a full MAM-basics clone, with its own environment (a linked worktree uses its
home clone's interpreter by absolute path), and with `$wlc` naming morphhb's `wlc/` directory at
`db6c5c9b`, a flat directory of its 40 files, such as a morphhb checkout's `wlc/`:

```powershell
./.venv/Scripts/python.exe py/main_morphhb_on_mam.py all $wlc
```

`all` checks the directory against the tracked listing (`verify-morphhb`), writes the censuses of
MAM's atoms (`census`), aligns each of MAM-simple's three strands (`align`), writes the
breakdowns, lists, figures and views (`analyze`), and builds the page and checks it (`page`).
`py/main_morphhb_on_mam.py --help` describes each subcommand.
`align.py` takes about 20 seconds per strand, as the study measured it on 2026-11-15; on
2026-11-16 it took 38 to 39 seconds a strand, reading MAM-simple included, and `all` took
about 5 minutes. The program reads only morphhb's `wlc/` directory and this repository's files,
and never touches the network. Then read `git diff -- morphhb-on-mam/out`: the outputs are the
test, and every difference is a finding until it is explained.

The large intermediates, `10-atoms*.jsonl` (one record per MAM atom, about 148 MB per strand)
and `11-unmatched-morphhb*.jsonl`, go to the work directory, `--work-dir`, by default
`.novc/morphhb-on-mam/work/`, which Git ignores. The page names that directory's files by their
path relative to the repository root, so the page step refuses a work directory outside the
repository.

On the machine where the study ran, the 2026-11-13 study's copies of morphhb's files are under
`.novc/morphhb-corrections-2026-11-13/fetched/`, one directory per file; for the regeneration of
2026-11-16 they were copied into one flat directory, `.novc/morphhb-on-mam/morphhb-wlc-db6c5c9b/wlc/`,
which `verify-morphhb` found identical to the listing, blob for blob.

## The program

| The study's script | Now, in `py/morphhb_on_mam/` |
| --- | --- |
| `mhb_common.py` | `morphhb_reader.py`, keeping its morphhb reader and form keys; its readers of WLC 4.18, 4.20 and 4.22 went |
| `mam_reader.py` | `mam_reader.py`, closed dispatch on MAM-simple's element types |
| `census_mam.py`, `find_mixed.py`, `check_fused_ketiv.py` | `census.py` |
| `align.py`, `analyze.py`, `analyze2.py`, `analyze3.py`, `strands.py`, `figures.py` | the same names |
| `show_list.py`, `show_examples.py`, `show_pair.py` | `views.py`, for the five files that the page links or reads |
| `build_page.py`, `page_text.py`, `page_check.py`, `page_selftest.py` | the same names |
| `verify_morphhb.py` | `verify.py`, which checks a directory against the tracked listing |
| `gh_read.py`, `show_tree.py`, `show_mam_verse.py`, `page_peek.py` | left out: network reads and conveniences |

`record_paths.py` says where everything is. No algorithm, threshold or classification changed in
the move; the name of one shape of class C blocks and some of the page's wording did, as
"How the outputs differ from the study folder's" says.

## The outputs

Under `out/`, each written by the subcommand named:

- `census`: `01-mam-census.txt`, `03-mixed-atoms.txt`, `31-check-fused-ketiv.txt`;
- `align`: `12-align-summary.txt`, `12-align-summary-cant-alef.txt`,
  `12-align-summary-cant-bet.txt`;
- `analyze`: `20-coverage.txt`, `21-examples.json`, `22-refine.txt`, `23-lists.json`,
  `25-strands.txt`, `26-kq-ids-slashes.txt`, `27-kq-ids-slashes.json`, `30-figures.json`,
  `30-figures.txt`, and the views `28-show-a2-contradicted.txt`, `28-show-b-contradicted.txt`,
  `28-show-qatan.txt`, `28-show-stress.txt` and `29-show-pairs.txt`;
- `page`: `morphhb-on-mam.html` and `40-page-text.txt`.

**Mark order.** The text outputs and the page show every pointed form in MAM-normal mark order,
through `give_std_mark_order`. The JSON outputs, `21-`, `23-` and `27-`, keep each form as its
source has it, MAM-simple's or morphhb's; on 2026-11-16 every line of them was in MAM-normal
order as well. The evidence files under `research/upstream/` quote GitHub's text as GitHub
served it, and the Hebrew in six of them, `01-`, `02-`, `03-`, `06-`, `15-` and `18-`, is in
another order. They are captures: do not repair them (`doc/mam-normal-mark-order.md`).

## How the outputs differ from the study folder's

The regeneration of 2026-11-16, at `babc6ba7`, whose MAM-simple is `374d9436`'s, reproduced the
study folder's records, `10-atoms*.jsonl` and `11-unmatched-morphhb*.jsonl`, byte for byte, and
every output under `out/` except these:

1. `03-mixed-atoms.txt`: the study's copy lists 55 atoms that join a ketiv to the plain atom
   after it. It was written before the study's last change to `mam_reader.py`, which ends an atom
   where a one-sided segment meets a two-sided one and flags it (`01-mam-census.txt`'s
   "boundary added after (k)", 55). Regenerated, it lists none, after a new first line that
   counts them.
2. `31-check-fused-ketiv.txt`, `30-figures.json` and `30-figures.txt`: a line naming the script
   or its inputs now names `census.py`, or `py/morphhb_on_mam/figures.py` and the work directory.
3. `20-coverage.txt` and `21-examples.json`: the shape of class C blocks that the study called
   "word division differs (same letters)" is now "division into atoms differs (same letters)",
   since `py/tests/test_prose_conventions.py` bans the phrase "word division" in `py/`.
4. The page and `40-page-text.txt`: every path is the new one; "This folder's" README is now
   "The record folder's"; and, for the same lint, which bans "MAM writes", the seven places
   where the study's page said "MAM writes" now say "MAM has" (five) or "MAM's one form is"
   (two), and the one "morphhb writes" beside them says "morphhb has". In `40-page-text.txt`,
   the tier table's last row no longer ends in spaces, since `page_text.py` now strips a row
   whose last cells are empty.

## What is not tracked

- The large intermediates, `10-atoms*.jsonl` and `11-unmatched-morphhb*.jsonl`, about 445 MB.
- morphhb's data.
- From the study folder, which stays untracked on the machine where the study ran: the scripts
  left out above; the outputs of the conveniences, `02-show-num-10-35.txt`, `24-show-c.txt`,
  `28-show-rd.txt`; the raw responses of the study's API reads, `fetched/`, apart from the tree
  listing; and, under `research/`, the sub-agents' scripts, the raw API dumps
  (`upstream/fetched/`), the decoded third-party files (`upstream/decoded-db6c5c9b/`,
  `upstream/decoded-morphhb-parsing-65dfd513/`), `upkeep-shape/out/mam_ws_U0.patch` (13 MB)
  and every other file of `upkeep-shape/out/` that neither `FINDINGS.md` nor `CHECKED.md`
  names.

The evidence files under `research/` are byte for byte as written in the study folder, but for
their line endings, which the repository stores as LF, and so are the three reports, but for a
dated note under each one's heading saying what stayed behind. The evidence files under
`research/upstream/` keep the line-final blanks of the GitHub text they quote, which
`.gitattributes` exempts from `git diff --check`.
Their paths are as written there: relative to that folder, or, in a few evidence files,
absolute paths on the machine where the study ran.
