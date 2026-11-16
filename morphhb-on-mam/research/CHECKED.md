# The root session's checks of the research reports (2026-11-15)

Written by Claude (Opus 5.5), the root session of the morphhb-on-MAM study, on 2026-11-15.
Both sub-agents' own writes of FINDINGS.md were refused by the harness; the root session saved
condensed copies of their returned text as `upstream/FINDINGS.md` and
`upkeep-shape/FINDINGS.md`. These are the material claims the page relies on and how each was
checked.

**Tracked copy, 2026-11-16.** This file was tracked in `morphhb-on-mam/research/` when the
study was put on ice. The decoded morphhb files that items 1 and 4 of the next section
cite, in `upstream/decoded-db6c5c9b/`, stayed untracked in the study folder,
`.novc/morphhb-on-mam-2026-11-15/research/` (`morphhb-on-mam/README.md`, "What is not tracked").

## upstream/FINDINGS.md

1. The validator's word checks cover `wlc/` only, and MAPM gets milestone, text and inventory
   checks: read `upstream/decoded-db6c5c9b/.github/scripts/validate_data.py` lines 31-40, 98-105,
   126-140, 165-170, 178-184 and 311-319. Confirmed.
2. "That file is a companion text" (Jesse Griffin, openscriptures/morphhb#116): found in
   `upstream/03-local-threads-114-115-116.txt`. Confirmed.
3. Every book's ids are distinct and carry the book's two-digit prefix
   (`upstream/11-id-census.txt`), and the tails number 21,976, Jeremiah's word count
   (`upstream/13-id-tail-sequences.txt`). Confirmed.
4. The id paragraph is `README.md` line 23 at `db6c5c9b` (`upstream/decoded-db6c5c9b/README.md`).
   Confirmed.
5. Not checked by the root session: the maintainers' activity figures, the morphhb-parsing
   generator's lines, and OSIS's rule against a lowercase `id` (openscriptures/morphhb#84). The page
   attributes them to the sub-agent's report.

## upkeep-shape/FINDINGS.md

1. MAM-morphhb reads MAM-simple's BHS JSON and takes only structure from MAM-parsed's plus/:
   `py/mam_morphhb/morphhb_runner.py` lines 8 and 86, `py/mam_morphhb/morphhb_plus.py` line 1,
   `py/main_mam_morphhb.py` line 7. Confirmed.
2. MAM-morphhb is hand-run and may lag MAM-simple by Ben's decision of 2026-11-03: AGENTS.md, the
   products section, read in this session. Confirmed.
3. Since 2026-09-16 the downloads' text and ketiv/qere changes are the 12 entries of
   `unpinned-latest.json`: the first rows of `upkeep-shape/out/crosscheck_unpinned.txt` pair each
   verse with its download and change-log category. Consistent; not recounted.
4. The commits between `374d9436` and `f689951f` touch only `DATA-LICENSES.md`,
   `doc/commander-prompt.md` and `dot-claude/skills/hebrew-prose/SKILL.md`: `git diff --name-only`.
   Confirmed; none is an input of this study.
5. Not checked by the root session: the per-download medians and the year's class counts, which
   rest on the sub-agent's own projection of the wikitext; the page attributes them to its report.
