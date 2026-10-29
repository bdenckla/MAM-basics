# Taamey D QA migration: next nightly handoff

Frozen Basics source: bcfe749c68c144218f33821c9f95775a25ed032d. The maintained broad commands remain `py/main_0_mega.py` followed by `py/main_test.py`, using an isolated source checkout and its home clone's interpreter. This focused review ran only the final three mega steps, not the full mega or suite; broad-tested remains 6ac28417a243447c24eefb168202585a9949a4ea.

The full mega has64steps at this source. Its new final steps run QA on the committed TTF and `corpus --check`; the hand-run FontForge build, corpus writer and `accept-baseline` operation remain excluded. Reinspect the scope at a newer source. Do not build fonts or accept baselines merely to satisfy a check.

Linux dependencies were refreshed from this frozen requirements.txt and constraints.txt; pip check succeeds. Keep uharfbuzz0.57.0 / HarfBuzz15.0.0. The eleven added pins match the source environment's declared pins. The current cloud run produced61PASS /0FAIL /0SKIP and byte-identical49reports under this environment. Do not substitute the old renderer's0.56.0environment.

Read every QA result. A shaping FAIL tuple deliberately does not itself fail the process. Mega compares the reports with Git's index and rejects changed/untracked reports or a directory where Git tracks no reports; SKIP, unknown status and anchor-family failure are fatal. Do not stage a new font baseline to make that guard pass without the owner's approval.

The corpus checker now reads the selected checkout's own word lists, including linked-worktree inputs, and permits dirty word lists in --check mode. It is nonwriting. A pending refresh is reported in the closing REFRESH PENDING banner at exit0 by design; record its counts and leave the pinned corpus alone. The actual frozen check found no refresh pending among120425Bible-word cases. Writing mode rejects uncommitted word lists. Baseline acceptance remains an explicit writer and is not transactional across all files, an inherited limitation acknowledged in the owner's record; it was not run here.

All focused stages were awaited sequentially. No font build, baseline acceptance, canonical corpus adoption, full mega/suite, external publishing, workflow dispatch or live configuration sync occurred. Historical author/plan approval and Windows test claims remain attributed, not new operational authority.
