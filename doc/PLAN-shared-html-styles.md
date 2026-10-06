# Shared HTML styles

State: live

Codex execution plan, 2026-10-06. Ben authorized implementation: “Can you go ahead
and do this, using your judgment (or flipping a coin, if no one alternative seems
clearly better) as to 'who to consolidate towards whom', starting with the
strongest candidates first?” Ben also delegated the choice of planning depth and
agent coordination. This plan records Codex's implementation choices.

## Checkout and ownership

The source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`. Work began in this clean full clone on `main`
at `101888a166385c3fbe180d626d416dc65850bfc3`. This commit is the required baseline;
verify it is an ancestor of HEAD when continuing. The root Codex agent owns all
writes, staging, commits and final integration. Sub-agents investigate and review
read-only until the root explicitly hands over exclusive writing ownership.

Run commands from that repository root with its own
`C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe`. A successor in a
linked worktree instead follows `codex-worktree-tasks` and uses its home clone's
interpreter. Read `AGENTS.md`, `hebrew-prose` with its MAM-basics reference,
`iterative-document-editing`, and `holman/WORKFLOW.md` for the report work.
Verify exact root, HEAD, branch and NUL-delimited status before editing and before
staging. Stop for unexpected HEAD movement or unowned modifications.

## Decisions and source manifest

- Use mpplus's ordinary English typography as the shared prose default: unspecified
  English family, 14pt, normal line spacing, centered 40em measure and justified
  prose. Remove MAM abbreviation small caps and explicit inline-code families in
  the consolidated prose families. Keep JSON-block and specialized display rules.
  The canonical base is the hand-authored served `gh-pages/document.css`, following
  the existing root and WLC stylesheet pattern without a second deployment copy.
- Keep family-specific Hebrew sizing, font features, wide tables, control behavior
  and meaningful colors in additional sheets. Preserve the near-Aleppo decision
  recorded by `7d3d7437` to leave unpointed Hebrew in the default font.
- Consolidate the exact Phonetic MAM/Yeivin ITM overlap toward the Yeivin base.
  Retain pronunciation controls and print behavior in Phonetic MAM's own sheet.
- Keep the edition stylesheet and its MAM-with-doc oracle bytes unchanged. Other
  edition families will load `MAM-with-doc/two_col_style.css` directly. Preserve
  `near_aleppo.edition.PIN` and the independent 62-file comparison.
- Consolidate related report components toward Holman's current report theme.
  Preserve filters, category colors, images and old/new display semantics. Ordinary
  English and inline code use their default families. Standalone report generation
  must retain a usable asset bundle outside the published tree.

The baseline inventory is supported by these authoritative sources:

| Family | Sources |
|---|---|
| Prose | `py/mb_misc/styles_mam_parsed.css`, `styles_authored.css`; `py/boj_render/two_col_css_styles_a.py` |
| Phonetic MAM and Yeivin ITM | `py/phonetic_mam/assets/style.css`, `py/yeivin_itm/assets/style.css` |
| Editions | `py/mb_misc/styles_mam_with_doc.css`; `py/near_aleppo/edition.py`, searchable `PIN` and `check_mam_mode` |
| WLC and UXLC | `gh-pages/wlc/style.css`, `gh-pages/uxlc/style.css` |
| MAM-simple document | `py/versification_and_cantillation/versification-and-cantillation.css` |
| Reports | `holman/assets/mam-suggestions-report.css`, `uxlc_corrections.css`; `py/mb_diff_mpu/mpplus_assets.py` |

## Cumulative implementation ledger

| Stage | Status | Work |
|---|---|---|
| Shared prose | implemented | Hand-authored `gh-pages/document.css`; miscellaneous and Book of Job prose join the base; body text is unchanged |
| Phonetic MAM and Yeivin ITM | implemented | Both load `document.css` and the Yeivin family stylesheet; Phonetic MAM retains only pronunciation/print extensions; row shading/highlights have matching dark colors |
| Identical edition copies | implemented | FOI, OSIS and near-Aleppo share unchanged MAM-with-doc CSS; canonical bytes, PIN and 62-file oracle are unchanged; Book of Job shares its root family sheet; four deployed duplicates and one unused source duplicate are retired |
| Remaining prose families | implemented | WLC/UXLC, MAM-simple, root pages and indexes join the base; the full mega regenerated the WLC/UXLC families; ten static compatibility pages also load the base |
| Related reports | implemented | Holman and change logs share hand-authored report.css; standalone bundles package the base under report-assets to avoid sibling specialty filename collisions |
| Verification and delivery | active | Regenerate affected products, inspect every tracked diff, run final gates, commit and push main |

## Verification and integration

Every coherent commit gets Black on changed Python files, `git diff --check`,
directly relevant checks and regeneration of affected products. HTML text, data
and binary fonts must remain unchanged except stylesheet references and ordinary
serializer wrapping. Any other generated change requires an explicit explanation.

Use the actual entrypoint's help to confirm each command before running it. The
affected routes include `py/main_authored.py`, `py/main_gen_misc_authored_english_documents.py`,
`py/main_near_aleppo.py --html`, `py/main_phonetic_mam.py render`,
`py/main_yeivin_itm.py render`, `py/main_mam_simple.py`, and the report generators.
Changing OSIS's generator or its stylesheet references also owes the hand-run
`py/main_mam_osis.py`; this is a generator change, not the exempt MAM text refresh.
The Sefaria and frozen HBCE generators are outside the changed inputs.

The required full OSIS run refreshed three XML files from existing MAM-simple
inputs: Judges 19:23 adds U+05A0, and 2 Kings 22:1 uses U+05C7 instead of the
stored OSIS's U+05B8. An independent XML comparison verifies each complete
refreshed verse against MAM-simple and verifies exactly those two changes in
the combined file. This explained refresh is committed separately from the CSS.
The refresh commit is `525464700d78cf938e6324cc61d8192ff3df7ad0`.

## Verification record, 2026-10-06

The full mega completed all 60 steps successfully, including the affected report,
WLC/UXLC, Phonetic MAM, Yeivin ITM and near-Aleppo generators. The required
hand-run OSIS generator also completed and validated its XML.

The generated-page comparison against the required baseline covers 1,583 changed
HTML pages and 4,069 stylesheet links. Head metadata and body content are
unchanged. The change-log index alone adds its reviewed styling class. All links
resolve. Data, fonts, JavaScript and other binary assets remain unchanged except
the three explained OSIS XML files in the separate refresh commit.

Independent CSS reviews verified the retained Hebrew sizes and font rules,
semantic emphasis, wide tables, controls and report routing. Sequential standalone
Holman generation into one directory preserved both specialty stylesheets and
the shared base. Packaged base and font hashes match their canonical files.
Black passed on all 43 changed or added Python files. The shared asset graph lint
passed. The full suite passed 1,051 tests and 60 subtests, with five skips; its five
file-census failures all named the removed duplicate Python module, which the
unstaged Git index still listed. After staging the reviewed additions and
deletions, all five affected lints passed, including a final `--lf` run. No source
change or weakened lint was needed. All 1,056 tests are verified. Final delivery
remains active.

The final combined tree owes these commands from the development root:

```powershell
./.venv/Scripts/python.exe py/main_0_mega.py
```

```powershell
./.venv/Scripts/python.exe py/main_test.py -q
```

Also verify the local stylesheet/font dependency graph and unchanged visible HTML
text against the baseline. A missing asset fails. Add only differential or
mechanical lint checks. Keep the existing edition oracle independent and passing.

Commit finished stages to `main`. Before pushing, fetch `origin`, merge if it moved,
and rerun checks owed by the combined changes. Push normally; repeat fetch, merge
and affected checks if origin moves again. No history rewriting or work discards.
At completion, reconcile every ledger row, mark this plan executed, and report the
final commit, checks and any explicit limitation.
