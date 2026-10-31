# Updates to the codex-index image-work retirement plan

State: open, first entry 2026-09-28.

Every entry corrects or supplements `PLAN-retire-codex-index-image-work.md`.

## 2026-09-28: historical editor inventory and change credits

Recorded by ChatGPT-Codex on 2026-09-28, New York time, under Ben's approved September 26 review
remediation plan.

**Corrected here; the executed base remains unchanged.** The passage “Three editors remain”
was a historical inventory after `f2a9ead4` and before the full retirement at `65f5a1c6`. That
inventory had four editors: the Aleppo and Cambridge column-quadrilateral editors,
`py/accgram/transcription_editor.py`, and the highlight picker
`py/accgram/gen_highlight_picker.py`, invoked through
`py/main_edition_transcription.py highlight-picker`. None was a crop editor or line-break
editor. The later full retirement removed the two column-quadrilateral editors; this correction
does not restore any program.

The claim that `139f631e`, `009b6378` and `46e2e524` all “extended the module to implement Ben's
decisions” conflated implementation and documentation. `139f631e` changed the reader's
implementation; `009b6378` and `46e2e524` changed its docstring only.

The original opening's “Both sections follow ‘Decisions recorded on 2026-09-12’” failed to name
its subjects. The current executed opening names “Executed in part on 2026-09-26”, “Decisions
recorded on 2026-09-26” and “Executed on 2026-09-26”. That current opening was already present
at the execution handoff; no additional substantive base edit is authorized here.

## 2026-10-31: the three unused accessors deleted

Recorded by Claude (Opus 5.5) on 2026-10-31, New York time, in the small-fixes session that the
session "Commander for Claude's forests" started that day. The base's finding 2, "**Left for
Ben: `py/boj_paths.py` keeps three accessors that nothing calls.**", left `jobn_img_dir()`,
`aleppo_img_dir()` and `enriched_quirkrecs_path()` in place. Ben decided on 2026-10-31, in the
session that looked for records no issue points to: "delete these with prejudice, e.g. don't
launch a whole new investigation to confirm that they are still not used, i.e. assume that the
previous analysis still holds, i.e. assume that nothing has started using them." The commit
that adds this entry deletes all three from `py/boj_paths.py`, with no new search for callers.
