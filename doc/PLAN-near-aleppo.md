# PLAN: near-aleppo — moved to MAM-private

State: pointer

The plan for the near-Aleppo edition is **not in this repo**. It lives in MAM-private, at

    MAM-private/doc/PLAN-near-aleppo.md

beside its privacy criteria, `MAM-private/doc/near-aleppo-privacy.md`.

Moved there 2026-08-25, at Ben's instruction, because MAM-basics is a public repo and the plan
draws throughout on private work in MAM-private. Moving the plan's privacy criteria alone,
earlier the same day, was not enough: the criteria were only one section of it.

The public deliverable is `out/near-aleppo/plus/`, a version of MAM-parsed-plus
whose text is nearer to what the Aleppo Codex contains, with its example edition
and documentation under `gh-pages/near-aleppo/`. Its local entry point is
`py/main_near_aleppo.py`; `out/near-aleppo/README.md` gives the build and check
commands. The public build reads local MAM data and stored pointing inputs.

The mega runs the five local MAM population checks, dataset build and HTML
rendering. These steps write only this checkout. The broader research census,
comparison work, scan archive and private approval history remain in MAM-private.

**If you are running the step-through, read the plan in MAM-private, and do not re-create it
here.** A session holding an older copy of it in context should re-read it there before its next
edit.
