# Qere-without-ketiv page edits

State: executed 2026-10-12; page edits pushed and skill deployed

Codex accumulated these requests from Ben on 2026-10-12. Ben then approved the skill
clarification and instructed: "Also, please execute the plan".

## Cumulative request ledger

1. **Implemented:** Add a period after "An image showing what the case looks like in Aleppo".
2. **Implemented:** Center the "Template" and "Meaning" header cells in the encoding-conventions table.
3. **Implemented; revised by Ben:** Use "Also as expected, none of the nine have any qere or ketiv
   letters in the body text, i.e. in the large-lettered main columns of the manuscript."
4. **Implemented:** Use "In the manuscript, all nine have the expected marginal note containing the
   qere letters."
5. **Superseded; canceled by Ben:** Retain "The cases differ in whether, in the body text:".
6. **Implemented:** Replace "Three artificial alefs" with "Three artificial alef letters". Use an
   English noun for plurals of romanized Hebrew letter or mark names on this page.
7. **Implemented; approved by Ben:** Clarify the Hebrew prose skill: "Do not pluralize romanized
   Hebrew letter or mark names with English suffixes or Hebrew plural endings. Pluralize an
   English noun instead: 'three alef letters', 'two meteg marks', 'two tsinnor marks'."

## Execution baseline and ownership

Source, development and integration checkout: `C:/Users/BenDe/GitRepos/MAM-basics`.
The checkout is a full clone on `main`; Codex owns execution, commit, push and configuration
deployment. The original planning baseline, `aa276529fc9667edc325d828fd225595e5dc4cbf`, is an
ancestor of the clean execution baseline, `90568303457c6ed916c2af0ceff47711e095fefa`.
The task's source files did not change between these commits. A fresh fetch confirmed that
`origin/main` equaled the execution baseline.

Follow `AGENTS.md`, `doc/review-trial.md`, the iterative-document-editing and hebrew-prose skills
and their applicable references, and the skill-creator guidance. Use
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` from the development checkout root.
The edits also work in a linked worktree with its home clone's interpreter and integration rules.

## Implementation and verification

- Edit the introduction and bullet in `py/near_aleppo/foi_qere_without_ketiv.py`, the header
  alignment in its sibling CSS, and the "Three artificial alefs" explanation in
  `in/near-aleppo/qere-without-ketiv-readings.json`.
- Replace the skill's "No transliterated plurals" rule with the approved wording in
  `dot-claude/skills/hebrew-prose/references/terminology.md`, outside the accgram-specific section.
- Run Black on the changed Python file, then regenerate with `py/main_near_aleppo.py --html`.
  The only expected generated change is `gh-pages/near-aleppo/foi/qere-without-ketiv.html`.
  Treat any additional output change as a finding. The manuscript observations are Ben's
  requested prose edits; this task does not independently reread the manuscript images.
- Run `py/main_near_aleppo.py --build --check` and `py/main_near_aleppo.py --html --check`.
  Run the existing qere/body differential with
  `py/main_test.py py/tests/test_near_aleppo.py -k qere_only -q` and validate the skill using
  the skill-creator's `scripts/quick_validate.py`.
- Read every changed diff and run `git diff --check`. Recheck HEAD and task-owned status before
  staging. Commit the completed requests and this record on `main`, fetch again, merge
  `origin/main` if it moved, repeat affected checks, and push normally.
- Deploy the updated skill through the complete `py/main_repo_util.py --sync-user-config`
  operation after pushing. Inspect its verification of both shared-skill destinations.
- Focused regeneration and checks suffice under the approved review trial; no immediate full
  suite or mega is owed for these prose, CSS and instruction edits. Record that scope in the
  commit message.

## Verification results

Before editing, `py/main_near_aleppo.py --html --check` passed against the execution baseline.

Black left the changed Python file unchanged. HTML regeneration produced the expected changes
to the target page, and `--html --check` passed. `--build --check` confirmed that the dataset and
build population file remained current. The existing qere/body differential passed with
`1 passed, 7 deselected`. The skill-creator validator passed with Python's `-X utf8` option;
the validator's implicit text decoding failed under the sandbox's initial Windows code page.
Source and generated diffs were read, and `git diff --check` passed.

The changes were committed as `12b6988eaa84163f6e394a665bf0b583d9c58c08` and pushed normally to
`origin/main`. The complete `--sync-user-config` operation deployed from that exact commit and
reported both `~/.claude/skills/hebrew-prose` and `~/.agents/skills/hebrew-prose` clean. The
operation also synchronized the other declared configuration destinations, as its procedure
requires. Its verified deployment count was 9.

The co-present "Update near-Aleppo page description" task paused its writes and retained
ownership of its two staged files, `py/near_aleppo/features_of_interest.py` and
`gh-pages/near-aleppo/foi/interesting-ketiv-qere.html`. This task's path-limited commit preserved
those staged files. No full suite or mega was run, under the focused-check trial and the scope
recorded above. All active requests are implemented; request 5 remains canceled.
