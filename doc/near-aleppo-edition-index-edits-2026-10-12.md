# Near-Aleppo edition index edits

State: executed 2026-10-12

## Approval and checkout

Ben requested the six edits below on 2026-10-12 and then instructed Codex to
"implement the plan". This is the approval snapshot and cumulative edit ledger.
No decisions remain unresolved.

Source, development and integration checkout:
`C:/Users/BenDe/GitRepos/MAM-basics`. The verified execution baseline is
`f1b04e9b7590ec1bd117a200273c51dd7f0001f7`, on clean `main`. Codex owns final
integration. Verify the root, HEAD, branch and status before editing; the baseline
must equal HEAD or be its ancestor. Use this clone's
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` from the repository root.
The edit also works in a linked worktree using its home clone's interpreter and
the linked-worktrees skill's integration procedure.

Follow `AGENTS.md`, `doc/review-trial.md`, the iterative-document-editing skill,
and the Hebrew-prose skill with its MAM-basics and rendered-prose references.

## Approved edits

1. **Implemented:** Replace "an example HTML edition of the near-Aleppo dataset."
   with "an example HTML edition based on the near-Aleppo dataset."
2. **Implemented:** Replace the sentence beginning "Ketiv is the primary text" with:
   "The pointed ketiv is shown as the primary text; the pointed qere appears above
   it; both are enclosed in a rounded box or “cartouche”."
3. **Implemented:** Delete the passage beginning "The edition uses each stored pointed
   ketiv" through "See the documentation for the near-Aleppo dataset.", including
   the documentation link.
4. **Implemented:** Replace the passage beginning "Where near-Aleppo's text of a note's
   target differs from MAM's" through "gives one of near-Aleppo's flags." with:
   "MAM’s doc-notes have been adjusted in some cases where the note’s “target”, or
   subject, differs between near-Aleppo and MAM."
5. **Implemented:** Replace the passage beginning "Vowels and accents that the codex
   writes under no letter" through "for other editions' display options.",
   including the GAV documentation link, with: "Orphan vowels and accents—marks
   associated with no letter or whose association is unclear—are shown on
   placeholder letters (alef, vav, or dalet) between double guillemets."
6. **Implemented:** Give the unchanged sentence beginning "Every paseq glyph is shown"
   its own paragraph.

## Implementation and verification

Edit `_edition_index` in `py/near_aleppo/edition.py`; use
`mb_author.author.dquote` for “cartouche” and “target”. The note and placeholder
sentences stay together in the existing paragraph. Regenerate the index rather
than editing its generated HTML. No rendering, styling, dataset or API changes.
The only expected generated change is
`gh-pages/near-aleppo/edition/index.html`; every other generated output must remain
unchanged. Treat an unexplained diff as a finding.

Run these commands sequentially from the development repository root:

```powershell
./.venv/Scripts/python.exe -m black py/near_aleppo/edition.py
```

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --html
```

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --html --check
```

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics diff --check
```

Read the generated index and inspect the complete diff. Under `doc/review-trial.md`,
use focused verification for these prose changes; leave the mega and full suite
to the nightly checks. Commit finished authorized work, fetch `origin`, merge
`origin/main` if it moved and repeat checks affected by the merge, then push
`main` normally. Record the execution result here in the same commit.

## Execution result, 2026-10-12

Codex implemented all six edits in the generator and regenerated the HTML. Black
passed with the changed Python file already formatted. The HTML comparison passed
before and after the edit, checking 95 files and two font copies. Reading the
generated index and its diff confirmed the approved wording, curly double quotes,
removed passages and links, and separate paseq paragraph. The index was the only
generated file changed; no dataset or stylesheet changed. `git diff --check`
passed. No new tests were added; regeneration and the inspected diff verify these
prose changes. The full mega and suite were deferred to nightly checks under the
approved review trial. Fetching `origin` found `origin/main` still at the execution
baseline, so no merge was needed.
