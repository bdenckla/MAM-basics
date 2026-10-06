# Near-Aleppo documentation edit status

State: live

Codex maintains this ledger for [Ben's requested edits](near-aleppo-requested-doc-edits.md).

## A96 — Stored note bodies and HTML presentation

**Status:** implemented by Codex, 2026-10-06.

**Assessment:** The quoted sentence remains true for the JSON dataset, but its scope was unclear.
The HTML edition's reviewed note presentations recast source clauses beside near-Aleppo's form;
the original JSON note bodies remain about MAM's target.

**Authorized scope:** Clarify the passage beginning “Two are MAM's note templates” in
`py/near_aleppo/doc_page.py`, regenerate `gh-pages/near-aleppo/reading-json.html`, and record
A96 here. Ben's request file is unchanged. The JSON dataset and example edition HTML are
expected to remain unchanged. The execution baseline is MAM-basics `617ceb42`.

**Change:** The JSON reference now explicitly scopes unchanged note bodies to the JSON dataset.
A following paragraph explains how the HTML edition recasts reviewed clauses as agreements
with near-Aleppo, places the remaining clauses after MAM's labelled form, and displays the
complete original note when a recast would require uncertain interpretation.

**Evidence:** `py/near_aleppo/phase6_mam_targets.py`, `MamTargets.add_to_e_cell`, rejects changes
to note parameters other than the target. `py/render_wt/render_wikitext_handlers.py`,
`_reviewed_doc_parts`, renders reviewed clauses beside near-Aleppo's form and the remaining
clauses with MAM's labelled form. Genesis 1:1 in `out/near-aleppo/plus/A1-Genesis.json` and
`gh-pages/near-aleppo/edition/A1-Genesis.html` demonstrates the stored and displayed versions.

**Verification:** Run from the MAM-basics repository root:

- `./.venv/Scripts/python.exe -m black py/near_aleppo/doc_page.py` passed.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --html` passed, including the shared
  renderer's comparison with the pinned tracked MAM-with-doc files. Only `reading-json.html`
  changed among the generated files; the dataset and example edition HTML remained unchanged.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --check-note-review` passed the fresh
  source enumeration and clause reviews.
- `git diff --check` passed.

The mega and full suite were skipped because the change clarifies rendered prose without
changing data or rendering logic.
