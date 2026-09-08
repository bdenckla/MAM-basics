# Add `מ:סילוק לפני געיה` under phonetic-hbo#78

## Summary

MAM has two U+05BD marks in the verse-final atom `לְכֻלָּֽהְנָֽה` at 1 Kings
7:37: the first serves as silluq and the second is a meteg (called `געיה` in
MAM's documentation). Add a source template that identifies the first mark as
the silluq without changing MAM's text. Editions that preserve documentation
keep both marks. The noteless Sefaria and AJF renderers remove every U+05BD
after the identified silluq. OSIS keeps both marks and adds a short
machine-readable note.

The canonical progress tracker is
[phonetic-hbo#78](https://github.com/bdenckla/phonetic-hbo/issues/78). Related
issues receive cross-reference comments pointing to phonetic-hbo#78; progress
is not duplicated across their timelines.

## Decisions and public contracts

### Template name and source call

Use the exact name `מ:סילוק לפני געיה`. The spelling `סילוק` is established
throughout the mirrored MAM introduction, including the source entry for
1 Kings 7:37 at `in/mam-ws-intro/ch5.mediawiki`; do not introduce `סלוק` as an
alias. The Hebrew template name follows MAM's term `געיה`, while Python names,
MAM-simple names, and English prose use *meteg*.

The complete source at 1 Kings 7:37 becomes this nested `נוסח` target:
`{{נוסח|{{מ:סילוק לפני געיה|לְכֻלָּֽהְנָֽה|לכלֽהנה}}|2==א (קווים לסילוק וגעיה), וכך אצל ברויאר ומג"ה{{ש}}ל=לְכֻלָּֽהְנָה (קו אחד לסילוק בלבד), וכן הוא בדפוסים וקורן וסימנים ומכון ממרא}}׃`.

Sof pasuq stays outside both templates. This matches the existing convention
for verse-final template calls, including the `מ:קמץ` call documented in
`doc/holman-meteg-m13-qamats-template.md`, and lets punctuation remain an
ordinary following text node in MAM-simple.

The two positional parameters have these contracts:

1. Parameter 1 is the exact pointed and accented atom as MAM has it, excluding
   sof pasuq. Rendering the template normally returns this parameter unchanged.
2. Parameter 2 contains the same Hebrew letters in the same order, with all
   marks and punctuation removed except exactly one U+05BD at the position of
   the silluq. Parameter 2 excludes sof pasuq. For the present source call,
   parameter 2 is `לכלֽהנה`.

Validate every call while rendering the corpus:

- Each parameter has the same Hebrew-letter skeleton.
- Parameter 2 has exactly one U+05BD and no non-letter codepoint besides that
  U+05BD.
- Parameter 1 has a U+05BD at the letter boundary marked in parameter 2 and at
  least one later U+05BD.
- The cleanup operation keeps the marked U+05BD and removes every later U+05BD;
  the contract supports a future atom with more than one post-silluq meteg.
- Invalid calls fail generation with the reference and both parameter values.

### MAM-simple XML and JSON

Preserve the distinction in MAM-simple rather than flattening the new template
to ordinary text. The 1 Kings 7:37 XML sequence is an element equivalent to
`<silluq-before-meteg letters-with-silluq="לכלֽהנה" text="לְכֻלָּֽהְנָֽה"/>`
followed by the ordinary sof-pasuq text node. The JSON element is equivalent to
`{"type":"silluq-before-meteg","letters-with-silluq":"לכלֽהנה","text":"לְכֻלָּֽהְנָֽה"}`
followed by the ordinary sof-pasuq text element.

The element name deliberately uses `meteg`, not `gaya`, because MAM-simple's
public English vocabulary follows the Unicode name. Add the element and its two
attributes to the XML and JSON reading guides. Generic MAM-simple consumers
that only want MAM's text flatten the element to its `text` attribute.

### Product behavior

The generated products have these exact outcomes at 1 Kings 7:37:

| Product | Result |
| --- | --- |
| MAM-with-doc | Keep `לְכֻלָּֽהְנָֽה׃` and the existing detailed `נוסח` note. |
| MAM-parsed plain and plus | Keep both U+05BD marks; the template must not change MAM's text. |
| MAM-simple XML and JSON | Keep both U+05BD marks in `text` and retain the silluq position in `letters-with-silluq`. |
| Sefaria | Emit `לְכֻלָּֽהְנָה׃` and no note. |
| AJF | Emit `לְכֻלָּֽהְנָה׃` and no note. |
| OSIS | Emit both marks and a note immediately after the atom and before sof pasuq. |

Use the OSIS note type `x-silluq-before-meteg` and note text `סילוק לפני געיה`.
The relevant sequence is equivalent to
`לְכֻלָּֽהְנָֽה<note type="x-silluq-before-meteg">סילוק לפני געיה</note>׃`.
The note describes the encoded distinction; it does not replace the detailed
MAM-with-doc apparatus note.

## Implementation plan

### Preconditions and repository isolation

The development checkout is
`C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg`, on the
worktree-required branch `post-stress-meteg`. The primary clone is
`C:/Users/BenDe/GitRepos/MAM-basics`, and its Python interpreter is
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Do not create a
venv, junction, or symlink in the worktree.

Planning baseline, measured 2026-09-08: the worktree branch, primary `main`, and
`origin/main` were all at
`825cef66d392ecf028e36db535847eced5a234c1`, the completed and verified merge of
the post-stress-meteg work with `main`. The worktree was clean apart from this
plan before the plan's commit. Re-establish the state rather than trusting that
revision, and do not begin implementation in a dirty checkout.

Before the first edit, read the complete `hebrew-prose` skill, this repository's
`CLAUDE.md`, `doc/agent-planning-principles.md`, and the current execution record
in `doc/PLAN-evacuate-five-MAM-products.md`. Phase 5 of that evacuation may move
MAM-OSIS into MAM-basics before this plan is executed; use the landed in-repo
paths if Phase 5 is complete, and use a separate MAM-OSIS worktree only if
MAM-OSIS remains a sibling repository.

Re-establish the worktree path, commit, branch, and cleanliness with:

```powershell
git rev-parse --show-toplevel HEAD --abbrev-ref HEAD
```

```powershell
git status --short --branch
```

Re-establish primary `main` with:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse HEAD
```

### Source synchronization and external documentation

Create the live Wikisource template `תבנית:מ:סילוק לפני געיה` as a pass-through
whose body renders parameter 1, matching the behavior of `תבנית:מ:דחי`. Add the
template to the special-pointing-and-accent-template roster in MAM's
introduction appendix. Refresh `in/mam-ws-intro/` only after those live edits so
the mirror records their revision IDs.

Add an explicit one-site replacement specification under
`in/mam-ws-bot-edits/` for 1 Kings 7:37. The specification must assert the exact
old and new source strings and must change only the target atom; run the bot's
no-save mode before the live edit. Apply the identical source call to the
corresponding Google Sheet cell. Do not hand-edit downloaded Google CSV files.

After both sources are updated, refresh the Wikisource books, the MAM
introduction, and the Google Sheet; then require `main_diff.py wsgo` to report no
Wikisource-versus-Google difference. If the source-sync work must land before
the implementation because the Google download reads remote `main`, make the
source synchronization a separate commit and integrate it using the worktree
procedure under “Integration and issue closure.”

Use the production entry points from the MAM-basics worktree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_download.py fr-ws-intro
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_download.py fr-google
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py wsgo
```

Use the established Wikisource bot entry point and its documented dry-run/no-save
option after inspecting the current CLI help; do not invent a second bot path.

### Parser, MAM-simple, and shared cleanup helper

Add the new template to every template registry that governs MAM-parsed plain,
MAM-parsed plus, generic source rendering, template surveys, nesting checks, and
feature-of-interest recursion. The default rendering path returns parameter 1,
so MAM-with-doc, MAM-parsed plain, and MAM-parsed plus retain MAM's two marks.
The abstract rendering path creates `silluq-before-meteg` with the parameter-2
value as `letters-with-silluq` and parameter 1 as the element text.

Put the validation and cleanup algorithm in the canonical `mb_cmn` source as a
small shared helper named `drop_post_silluq_metegs`. Use named Unicode escapes
for standalone combining marks, including
`"\N{HEBREW POINT METEG}"`; do not place an orphan combining mark literally in
Python source. The helper accepts the fully marked atom and
`letters-with-silluq`, validates the contract above, and returns the fully
marked atom with all post-silluq U+05BD marks removed.

Copy the shared helper into `MAM-simple/py-examples/mb_cmn/` through the existing
MAM-simple support-file generator. Do not hand-edit the vendored copy. Extend
the vendoring inventory/check so the canonical and copied implementations must
remain byte-identical.

Add `silluq-before-meteg` to the XML render mapping, the JSON conversion, and
the MAM-simple XML/JSON documentation. Update any MAM-simple loaders that
currently enumerate all element types so generic flattening returns `text` and
does not lose the following sof pasuq.

### Sefaria, AJF, and OSIS consumers

Register `silluq-before-meteg` in both canonical Sefaria/AJF handlers and the
generated example copies. Both handlers call `drop_post_silluq_metegs` with the
element's `text` and `letters-with-silluq` values. Both noteless products discard
only post-silluq U+05BD marks; they keep the silluq, vowels, accents, letters,
and sof pasuq.

Register the element in the canonical OSIS handler and generated example copy.
The OSIS handler returns the unmodified element text followed by an OSIS note
with type `x-silluq-before-meteg` and text `סילוק לפני געיה`. The ordinary
following MAM-simple text node supplies sof pasuq after the note.

Update `py/py_ac_loc/mam_xml_verses.py` and the MAM-private consumer at
`C:/Users/BenDe/GitRepos/MAM-private/masorah-books/py/ocr_cmn/mam.py` if their
element allowlists would otherwise reject or omit the new public MAM-simple
element. These consumers must flatten it to `text`; neither consumer creates a
note or removes the post-silluq meteg.

The mega pipeline's near-Aleppo step must continue to reach MAM-private through
`mb_cmn.paths` and the explicit `REPO_MAM_PRIVATE_DIR` override in a worktree.
Extend the sibling-reach lint if the new consumer path adds a discoverable
dependency. Do not use a cwd-relative sibling path.

### Generated artifacts

Regenerate the complete pipeline, not a hand-selected 1 Kings artifact. Expected
changes include the source mirrors, MAM-parsed outputs, MAM-simple XML/JSON,
MAM-for-Sefaria/AJF outputs, MAM-OSIS output, template-survey artifacts, and
documentation generated from those sources. The only intended biblical-text
difference in noteless Sefaria/AJF output is removal of the second U+05BD at
1 Kings 7:37. MAM-with-doc, MAM-parsed, and MAM-simple keep the same biblical
text bytes apart from the new structural wrapper. OSIS keeps the same biblical
text bytes and gains the one note.

Set the worktree's repository routing before generation:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

```powershell
$env:REPO_MAM_PRIVATE_DIR="C:/path/to/the/verified/MAM-private-worktree"
```

If MAM-OSIS has not yet moved into MAM-basics, also set:

```powershell
$env:REPO_MAM_OSIS_DIR="C:/path/to/the/verified/MAM-OSIS-worktree"
```

Run the current production mega entry point from the verified MAM-basics
worktree after inspecting its CLI help for the all-steps spelling. Do not run a
generator, formatter, staging command, or commit in the primary MAM-basics
clone.

## Verification and acceptance criteria

Use generated-output differentials and mechanical lints. Do not add an
example-based unit test that pins only 1 Kings 7:37. The corpus-wide validation
in the real renderer is the check for template calls, and full regeneration is
the behavioral test.

Acceptance requires all of the following:

1. A corpus search finds the new template exactly once, at 1 Kings 7:37, unless
   later MAM source work has deliberately added another valid site. Every found
   call passes the parameter contract.
2. A corpus search confirms that no call includes sof pasuq in either parameter
   and that the source sof pasuq immediately follows the enclosing `נוסח`
   template.
3. MAM-with-doc, MAM-parsed plain, MAM-parsed plus, and MAM-simple have
   `לְכֻלָּֽהְנָֽה׃` at 1 Kings 7:37.
4. Sefaria and AJF have `לְכֻלָּֽהְנָה׃` at 1 Kings 7:37 and no synthetic note.
5. OSIS has both U+05BD marks, exactly one `x-silluq-before-meteg` note at the
   site, and sof pasuq after the note. The combined OSIS file and the individual
   1 Kings file agree.
6. Generic MAM-simple readers, the Aleppo reader, and the masorah-books reader
   reproduce the atom text with both marks and do not expose the structural
   wrapper as stray output.
7. The canonical and generated MAM-simple example support files are
   byte-identical under the vendoring check.
8. `main_diff.py wsgo` is empty after both live sources have the same call.
9. The full MAM-basics suite passes with no silent skips caused by a missing
   sibling checkout. The last recorded clean-main baseline was 976 passed,
   5 skipped, and 65 subtests on 2026-09-06 in
   `doc/PLAN-evacuate-five-MAM-products.md`; remeasure and treat any mismatch as
   a finding rather than trusting that figure.
10. Every changed Python file has been formatted together with Black from the
    primary clone's venv, and all unexplained generated diffs are resolved before
    commit.

Run Black only on changed Python files:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black <changed-python-files>
```

Run the canonical suite from the MAM-basics worktree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q
```

## GitHub coordination, commits, and integration

Before implementation, post an agent-attributed planning comment on
phonetic-hbo#78 stating the chosen template contract, sof-pasuq placement,
MAM-simple representation, noteless Sefaria/AJF cleanup, OSIS note, and the fact
that MAM's text remains unchanged. Treat phonetic-hbo#78 as the only progress
log.

Post short agent-attributed cross-reference comments on these open issues if
they still exist and still overlap when execution begins:

- [MAM-basics#57](https://github.com/bdenckla/MAM-basics/issues/57), which tracks
  the broader class of meteg/silluq handling.
- [MAM-private#24](https://github.com/bdenckla/MAM-private/issues/24), which
  tracks the broader downstream architecture.

Do not close, reopen, relabel, or reassign either broader issue. Historical
trackers [MAM-for-JPS#19](https://github.com/bdenckla/MAM-for-JPS/issues/19) and
[MAM-for-CCAR#6](https://github.com/bdenckla/MAM-for-CCAR/issues/6) describe the
same concrete site but belong to archived repositories. Link them from
phonetic-hbo#78; do not unarchive those repositories merely to comment.

Commit coherent stages on each worktree-required local branch. Do not push a
worktree branch. Immediately before archival, integrate each participating
repository by the established four-step procedure: merge current `main` into
the worktree branch, resolve and commit there, run the repository's complete
suite in the worktree, fast-forward the primary clone's `main` to the verified
branch, and push `main`. If the fast-forward refuses because `main` moved,
return to the worktree merge rather than creating a second merge in the primary
clone.

After all generated artifacts and public outputs are verified and pushed, post
an agent-attributed closing comment on phonetic-hbo#78 with the MAM-basics,
MAM-OSIS if still separate, and MAM-private commits plus the acceptance results.
Close phonetic-hbo#78 with that explanatory comment. No related issue changes
state without a separate explanatory comment.
