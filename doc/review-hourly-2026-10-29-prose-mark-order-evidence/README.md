# Focused raw-quotation prose-lint follow-up

State: executed 2026-10-29; known check failure remains unresolved

Source is `8339eb1352a745c5c2e16945a42b73b50aa30864`. No source repair or
new endpoint review was performed. The single focused command is recorded with actual UTC
timestamps in `prose-lint.result.json` and complete output in `prose-lint.log`.
It exits 1: one failed test in 0.15s, reporting only `py/ws/ws_bot_edit_history.md:490`.

`quotation-audit.json` independently identifies the exact inline token in the bot payload
at `edits.Deuter[0].new` and in the committed raw Wikisource chapter. Git blame and the
pre-introduction comparison identify `4d72e9336ef2b57e59d17692b6646bbe19989c7b`.
This is a legitimate literal quotation of raw input, rather than evidence of a new
transcription error. The payload's packed form also retains its original CGJ sequence.
No source, Hebrew mark order, capture, editorial decision or lint scope was changed.

The earlier 20:00 and 21:00 focused-stage passes remain valid for their listed commands.
Neither ran this lint. They omitted the owner's separately acknowledged failure; this
follow-up makes that limitation explicit without rewriting either finished receipt.

Nightly handoff: the prose lint at this exact source is known to fail. Do not call a
suite passing or silently exclude the failure. Preserve the raw quote; any eventual
repair should exempt only the verified literal quotation and continue checking authored
prose. No blanket file/line exemption or normalization was implemented. Recording the
failure requires no new editorial decision. No broad rerun or broad-anchor advancement.

The saved home checkout was restored to its clean original branch. No new clone/worktree,
sibling executor, font job, main/shared push, deployment or live source operation was used.
The zip contains exact helpers/logs/audits; `manifest.json` lists each member's size/hash.
