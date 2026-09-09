# Add `מ:סילוק לפני געיה` under phonetic-hbo#78

State: live

## Summary

MAM has two U+05BD marks in the verse-final atom `לְכֻלָּֽהְנָֽה` at 1 Kings
7:37: the first serves as silluq and the second is a meteg (called `געיה` in
MAM's documentation). Add a source template that identifies the first mark as
the silluq without changing MAM's text. Editions that preserve documentation
keep both marks. The noteless Sefaria and AJF renderers remove every U+05BD
after the identified silluq. OSIS keeps both marks and adds a short
machine-readable note.

The same site makes a published page wrong. The `mtgmtg` feature-of-interest page,
`gh-pages/MAM-with-doc/foi/foi-mtgmtg.html`, opens by calling the very concern this
plan encodes "unfounded". This plan also corrects that page's introduction and its
group labels, whose source is the authored prose in
`py/foi/mtgmtg_explanations.py`.

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

### The mtgmtg feature-of-interest page stops calling the concern unfounded

`gh-pages/MAM-with-doc/foi/foi-mtgmtg.html` is published at
`https://bdenckla.github.io/MAM-basics/MAM-with-doc/foi/foi-mtgmtg.html` and linked from
`gh-pages/MAM-with-doc/foi/index.html`. Its four introductory paragraphs come from
`OVERALL_EXPLANATION` in `py/foi/mtgmtg_explanations.py`, and the parenthesis under each
group heading comes from `_mtg_count_description` in the same module. The first paragraph
says the concern "turns out to be unfounded": that a verse-final word might contain a
meteg in the narrow sense (געיה) after the mark that serves as silluq. That is the
concern this plan exists to encode, and 1 Kings 7:37 is a case of it, so the sentence
is false. Re-read the two defects with:

```powershell
Select-String -Path C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/MAM-with-doc/foi/foi-mtgmtg.html -Pattern 'unfounded|verse-final one'
```

Ben settled the reading on 2026-09-09, disposing of finding 1 of
`doc/review-findings-2026-09-08.md`: MAM has a meteg after silluq at 1 Kings 7:37, and the
post-stress-meteg research deliberately misreads that word as meteg-then-silluq, which it
now says on its own pages in Ben's wording (`gh-pages/post-stress-meteg-methods.html`, and
footnote φ1 on `gh-pages/post-stress-meteg.html`; commit `3b0225e0`). The `mtgmtg` page
has no such research to protect. It is a census of the feature itself, so it says plainly
that MAM has the case.

Five decisions, Ben's finding of 2026-09-09 applied to this page:

1. **The first paragraph names the site.** Drop "which turns out to be unfounded",
   and add the one MAM case with its reference and its form, following the wording
   Ben approved for the post-stress-meteg pages: at 1 Kgs. 7:37, in MAM, there is a
   meteg after silluq in לְכֻלָּֽהְנָֽה׃. MAM's source entry for that verse names the two
   marks in their written order, silluq then געיה: the entry reads `קווים לסילוק וגעיה`.
   That is how Ben reads it (phonetic-hbo#78, 2026-09-08: "this silluq-then-meteg is
   not only present in MAM, it is confirmed by MAM's doc-note"). Find the entry with:

   ```powershell
   Select-String -Path C:/Users/BenDe/GitRepos/MAM-basics/in/mam-ws-intro/ch5.mediawiki -Pattern 'קווים לסילוק וגעיה'
   ```

   Merely deleting the "unfounded" clause is rejected: it would leave the page
   raising a concern and never answering it, and the page's tables cannot answer it,
   the word being one of 354 in a group whose first five only are shown.
2. **The group labels keep their partition, and one phrase goes.**
   `_mtg_count_description` labels a sof-pasuq group as "N Unicode METEG marks in addition to
   the verse-final one serving as silluq", which renders at three group headings. Read as
   "the last one", that puts the silluq after the meteg, which at 1 Kings 7:37 is backwards.
   Delete "verse-final" from both branches, leaving "in addition to the one serving as
   silluq"; the same sentence already says "with sof pasuq present", so nothing is lost. The
   counts stay right either way: `_get_qualifiers` in `py/foi/foiz_wt_mtgmtg.py` subtracts one
   for the silluq without claiming which mark it is, so 1 Kings 7:37's `1/sopa-y/maq-n` is a
   true statement of one meteg beside one silluq.
3. **No new group, and no footnote on the group.** Once the new template is
   registered in `foiz_wt_mtgmtg.py`, a template-derived qualifier becomes
   available, so a `silluq-first` group would be possible; it is rejected anyway.
   `fp` is a public key in `foi-mtgmtg.json`, and re-partitioning a 354-member group
   for one member changes that key for every consumer while telling a reader nothing
   the introduction does not. A one-member group is also a worse home for the fact
   than a sentence at the top of the page. A footnote on the group is rejected as
   redundant for the same reason: the only reader who reaches it has already read the
   introduction, and the word is not among the five shown.
4. **Plain "word" stands on this page, and no terminology sweep rides along.** The
   `hebrew-prose` skill bans a loose "word", and this page is not one of the nine
   post-stress-meteg pages that `CLAUDE.md` exempts. Plain "word" stands here on the skill's
   own exemption for a context that settles the sense: the page's second paragraph groups by
   whether maqaf is present, and its tables show a maqaf compound as one row, so a "word"
   here is a chanted word. The added sentences avoid the noun anyway, attaching the marks to
   the form as Ben's post-stress-meteg wording does. Do not sweep "word" out of
   `explanation_for_path` or `_mtg_count_description` under this plan; that sweep is Ben's
   call and its own change.
5. **The page's new claim is pinned against the collected data.** The `hebrew-prose` skill
   forbids retyping an accent, and `OVERALL_EXPLANATION` is a module constant rather than a
   generation-time lookup, so the form is typed once and an assertion re-derives it.
   `py/foi/foi_finals.py`'s `_write_finals3` holds the complete `mtgmtg` collection in
   `outs["rowdics"]` before either output is written; add the pin there, for that stem alone,
   raising unless exactly one record has `bcv_short` `1K7:37` and an `r` equal to the typed
   form. Copy the shape of `maqaf_nonfinal_accents_page.pin_claims`: re-derive and raise,
   never warn.

**Two of those four introductory paragraphs arrived on 2026-09-09, after the five decisions
above were written, and this plan does not touch them.** Commit `9f851c2f` appended a third
and fourth element to `OVERALL_EXPLANATION`, saying that the empty `2/sopa-y/maq-n` group is
scarcity rather than a rule and pointing at `doc/foi-mtgmtg-empty-cell.md`, which carries the
Yeivin and Breuer citations and the arithmetic. They were appended rather than woven in, so
decision 1 still edits the first element alone and decision 2 still edits
`_mtg_count_description` alone; the added paragraphs never call the concern unfounded and
never locate the silluq, so acceptance criteria 8 and 9 are unaffected, and the regeneration
left `foi-mtgmtg.json` byte-identical. This section said "two introductory paragraphs" until
this note was added.

**One question for Ben that decision 4 did not face: the page is now mixed on "word".** Those
two added paragraphs say "chanted word" and "atom", glossed inline at first use, because the
empty group is about a lone atom and plain "word" cannot say that; the older paragraphs say
plain "word". Decision 4 bans a terminology *sweep* and settles that plain "word" stands, but
it was written against a two-paragraph page and does not say what to do about a mixed one.
Rewording the added paragraphs down to "word", rewording the older ones up, and leaving the
page mixed are all open; none of them is done here.

`doc/holman-meteg-m23-isaiah-23-12.md` vouches for the false sentence and is corrected with
it. Its item 4 under "The post-silluq meteg: one case, in the Leningrad Codex, not in MAM"
reports `py/foi/mtgmtg_explanations.py` lines 41-49 as recording the concern as unfounded for
MAM, with no note that the record is wrong. Correct that one sentence and that heading, which
counts one case where there are two, one in the Leningrad Codex at 1 Samuel 17:5 and one in
MAM at 1 Kings 7:37. Leave the rest of that document alone: its item 3 census figure and its
framing belong to the post-stress-meteg survey, which Ben settled separately on 2026-09-09.

## Implementation plan

### Preconditions and repository isolation

The primary clone is `C:/Users/BenDe/GitRepos/MAM-basics`. Work in a secondary
worktree of it, on a worktree-required non-`main` branch, and run the primary
clone's interpreter by absolute path,
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Do not create a
venv, junction, or symlink in the worktree.

**The checkout this section named until 2026-09-09 is gone, and nothing is named
in its place.** It named
`C:/Users/BenDe/.codex/worktrees/MAM-basics-post-stress-meteg` on the branch
`post-stress-meteg`, with a planning baseline of 2026-09-08 putting that branch,
primary `main` and `origin/main` all at
`825cef66d392ecf028e36db535847eced5a234c1`. Measured 2026-09-09 from the worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eager-leakey-2ff58c`: that
directory is absent from disk, `git worktree list` does not name it, and the
branch `post-stress-meteg` does not exist locally, its work having reached `main`.
Primary `main` and `origin/main` both stood at
`becc6f0014e1646d47c3b63239945e3b7838d17e`, seven commits past `825cef66`, which
is still an ancestor. Three other worktrees stood clean at the same time, two
Claude worktrees at `becc6f00` and the Codex worktree
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` at `5636d38a`, so
expect a co-present session and prove non-collision rather than serializing
against it. Within the hour that co-present session integrated its review record
and `main` moved again, to `5636d38a` at 08:19 that same morning, with `becc6f00`
still an ancestor. Two measurements of `main` inside one session is why the
instruction below is to re-measure rather than to trust any revision written here.
Use whichever checkout is named when this plan is launched; a fresh worktree is
correct if none is.

Re-establish the state rather than trusting either revision, and do not begin
implementation in a dirty checkout.

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

### The mtgmtg feature-of-interest page's authored prose

Edit `py/foi/mtgmtg_explanations.py`: `OVERALL_EXPLANATION`'s first paragraph and
`_mtg_count_description`'s two sof-pasuq branches, per the decisions above, plus
the pinned form and the pin function. Call the pin from
`py/foi/foi_finals.py`'s `_write_finals3`, after its loop fills `outs` and before
`_write_json`. Do not edit `gh-pages/MAM-with-doc/foi/foi-mtgmtg.html` or
`foi-mtgmtg.json`; both are generated, as the comment at the head of the HTML says.

Lift the Hebrew form from tracked data rather than typing it. The file-writing
tools put Hebrew into Unicode-normal mark order, which this repository's
`CLAUDE.md` forbids; check the result with `has_std_mark_order` and repair it with
`give_std_mark_order`, both in `py/mb_cmn/uni_denorm.py`, before committing any
file that gained Hebrew.

This correction does not depend on the source template. It may be its own earlier
commit, and it stays correct if the rest of this plan is deferred.

### Generated artifacts

Regenerate the complete pipeline, not a hand-selected 1 Kings artifact. Expected
changes include the source mirrors, MAM-parsed outputs, MAM-simple XML/JSON,
MAM-for-Sefaria/AJF outputs, MAM-OSIS output, template-survey artifacts, and
documentation generated from those sources. The only intended biblical-text
difference in noteless Sefaria/AJF output is removal of the second U+05BD at
1 Kings 7:37. MAM-with-doc, MAM-parsed, and MAM-simple keep the same biblical
text bytes apart from the new structural wrapper. OSIS keeps the same biblical
text bytes and gains the one note.

`gh-pages/MAM-with-doc/foi/foi-mtgmtg.html` and `foi-mtgmtg.json` are among the
artifacts this regeneration rewrites, so both are touched whether or not the prose
changes. Expect a diff in the HTML and **no diff at all in the JSON**: the JSON
carries records rather than prose, and the template must not change what the FOI
collects. A JSON diff is a finding, and the first thing to suspect is the new
template's handler in `py/foi/foiz_wt_mtgmtg.py`.

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
8. `gh-pages/MAM-with-doc/foi/foi-mtgmtg.html` no longer calls the concern
   unfounded, names 1 Kings 7:37 with the form לְכֻלָּֽהְנָֽה׃, and has no group label
   locating the silluq as the verse-final U+05BD. Read the rendered page, not the
   module.
9. `gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` is byte-identical to the file this
   plan was widened against: 718 records in five groups, `1/sopa-y/maq-n` 354,
   `1/sopa-y/maq-y` 229, `2/sopa-n/maq-n` 19, `2/sopa-n/maq-y` 102 and
   `2/sopa-y/maq-y` 14, with 1 Kings 7:37 in `1/sopa-y/maq-n` and its `r` holding
   both U+05BD marks. Those five figures were re-derived from the tracked JSON on
   2026-09-09 at `becc6f0014e1646d47c3b63239945e3b7838d17e`; re-measure and treat
   any mismatch as a finding. A count of 353 in the first group means the new
   template's handler recursed on parameter 2 or ran `drop_post_silluq_metegs`,
   and this MAM-with-doc artifact keeps MAM's text.
10. `main_diff.py wsgo` is empty after both live sources have the same call.
11. The full MAM-basics suite passes with no silent skips caused by a missing
    sibling checkout. The last recorded clean-main baseline was 976 passed,
    5 skipped, and 65 subtests on 2026-09-06 in
    `doc/PLAN-evacuate-five-MAM-products.md`; remeasure and treat any mismatch as
    a finding rather than trusting that figure.
12. Every changed Python file has been formatted together with Black from the
    primary clone's venv, and all unexplained generated diffs are resolved before
    commit.

Re-derive criterion 9's five figures with:

```powershell
Get-Content C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/MAM-with-doc/foi/foi-mtgmtg.json -Raw | ConvertFrom-Json | Group-Object fp | Select-Object Name,Count
```

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
MAM-simple representation, noteless Sefaria/AJF cleanup, OSIS note, the mtgmtg
page correction, and the fact that MAM's text remains unchanged. Treat
phonetic-hbo#78 as the only progress log.

Post short agent-attributed cross-reference comments on these open issues if
they still exist and still overlap when execution begins:

- [MAM-basics#57](https://github.com/bdenckla/MAM-basics/issues/57), "review words
  with two געיה marks", which is the mtgmtg page's own subject and so bears
  directly on the page correction, not only on the broader class of meteg/silluq
  handling.
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
