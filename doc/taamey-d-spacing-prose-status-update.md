# Taamey D spacing prose continuation update

State: open; first entry 2026-10-14

## Approved main integration — 2026-10-14

Ben approved the pending merge: “Yes please merge.” This supersedes the base
record's branch-only restriction and authorizes integrating
`codex/taamey-d-spacing-prose`, source commit
`9d08534ede06290e2d1d4a709d0dcef50f443701`, into current main and pushing normally.
Deployment and new spacing policy remain outside the request.

Fresh main was `bd8f3c3f12b6940b38696118c6ed3f20871f5265`. Its newer owner commit
refreshes the Introduction mirror and does not overlap the spacing changes.
It was merged without conflicts in `/workspace/MAM-basics-taamey-d-spacing`;
the home checkout `/workspace/MAM-basics` receives only fast-forwards.
The incoming mirror bytes and the spacing page are preserved.

The effective base State is executed 2026-10-14; approved main integration
prepared and verified. From the worktree root using the home checkout's interpreter,
`py/main_near_aleppo.py --html --check` passed. The focused corpus-preservation,
prose, transliteration, NFC, prose mark-order and changed-document link/encoding
checks passed all 18 selected tests, including this staged update. The owner mirror
files match fresh main exactly; the spacing page, generator, classifier and CSS
match the approved source commit. No generated output needed changing.

The mega and full suite remain deferred under `doc/review-trial.md`: the incoming
owner work is a mirror refresh, and the spacing change itself remains prose and
examples, with no new spacing rules or font/dataset changes. The existing Pages
workflow has scheduled and manual triggers; this integration does not dispatch it.
