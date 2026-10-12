# Support and annotate silluq before a later meteg

State: executed 2026-10-12

## Approved execution snapshot, 2026-10-12

Ben instructed Codex: "Proceed as you suggest." He confirmed: "we want to remove the
meteg in editions without notes", identifying Sefaria/AJF, and requested documentation
in MAM-parsed-plus, MAM-simple and the older Sefaria encoding guide. This snapshot
supersedes the one-site, source-first implementation sequence proposed on 2026-09-08.
Ben subsequently confirmed: "Follow both explicit annotations (Recommended)" for
the post-stress-meteg survey. This supersedes its deliberate misreading of
1 Kings 7:37, chosen on 2026-09-09. The survey follows Phonetic MAM's computed stress
and reconciles verse-final records with the source annotations actually used.
The undertaking is completed in [phonetic-hbo#78](https://github.com/bdenckla/phonetic-hbo/issues/78),
closed with Codex's dated completion comment on 2026-10-12.

The source and integration checkout is `C:/Users/BenDe/GitRepos2/MAM-basics`, initially
`7fb93c9259f3dd4929016f14079f1a768496d580`, on clean main. Development is
`C:/Users/BenDe/.codex/worktrees/silluq-before-meteg/MAM-basics`, initially the same
commit, on `codex-worktree-silluq-before-meteg`. Use the home interpreter
`C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe` from the development root.
Private support uses the isolated checkout
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/private-silluq-before-meteg`, initially
`016c086b78e5d416dae07c2810c1ff5280a32316`, with its own home clone's environments.
The root Codex agent owns final integration in both repositories; private implementation
is delegated in that separate checkout. Verify HEAD, branch, ancestry and NUL-delimited
status before each stage and commit.

## Source and product contract

Both live source notes explicitly identify the earlier mark as silluq and the later mark
as meteg: 1 Kings 7:37 and Job 4:12. The live template did not exist and neither chapter
called it at the initial API check. These are source-note findings, not new manuscript
readings. The two atoms are:

| Site | Full atom | Silluq scaffold |
|---|---|---|
| 1 Kings 7:37 | לְכֻלָּֽהְנָֽה | לכלֽהנה |
| Job 4:12 | מֶֽנְהֽוּ | מֽנהו |

Use the exact Wikisource name `מ:סילוק לפני געיה`, with exactly two positional parameters:

1. Parameter 1 is the full marked atom, unchanged, excluding sof pasuq.
2. Parameter 2 is the same letter skeleton with exactly one U+05BD identifying silluq,
   with no other marks or punctuation. The full atom must have that mark and at least
   one later U+05BD. Earlier metegs remain permitted. All later U+05BD marks are removed
   by the noteless projection, including a future atom with several later metegs.

Validate each actual call and fail with its context and both values on invalid input.
Unknown templates and malformed shapes continue to fail. The template renders parameter
1 unchanged on Wikisource and sits inside the existing `נוסח` target. Sof pasuq stays
outside both wrappers. The bot specification copies exact current source strings and
changes only the two targets, preserving the existing detailed notes and every text mark.

MAM-parsed-plus preserves the wrapper. MAM-with-doc and generic text consumers select
parameter 1. MAM-simple XML and JSON preserve `silluq-before-meteg`, with `text` and
`letters-with-silluq`; the scaffold is metadata, never additional Scripture text. Both
formats keep sof pasuq as the following ordinary text node.

Sefaria/AJF remove every later U+05BD, preserving the identified silluq and all other text,
and supply no explanatory note for this annotation. OSIS preserves both marks and emits
`<note type="x-silluq-before-meteg">סילוק לפני געיה</note>` before sof pasuq. Near-Aleppo
selects parameter 1 as plain text. Phonetic MAM retains both marks in its Hebrew display
and uses the explicit silluq position for primary stress. Private readers preserve text;
private metadata is not added to the public release schema.

## Cumulative requirements and stages

- **Implemented: support before source use.** Add closed registries, parameter schemas, renderer
  and consumer handlers, accepted nesting, and strict position validation. Supported
  capability may have zero occurrences. Corpus inventories remain inventories of what
  occurs; update their occurrence claims only after source annotation and refresh.
- **Implemented: documentation.** Cover MAM-parsed-plus, MAM-simple XML and JSON, Sefaria/AJF
  README and authored static encoding guide, OSIS README and generated guide, near-Aleppo
  template projection, and the Phonetic MAM display/computation distinction. Do not restore
  retired Sefaria/OSIS example programs or unused vendored files.
- **Implemented: zero-use and offline verification.** Regenerate affected products with zero
  calls and judge every diff. Exercise both proposed source calls through the real parser
  and product paths in scratch inputs, and use meaningful differential checks for the
  cleanup and explicit stress calculation. Format changed Python with the home Black and
  run relevant focused tests. Follow `doc/review-trial.md` for verification cadence.
- **Implemented: support integration.** Commit coherent public and private support, update
  private vendoring provenance from the committed public source, integrate through the
  linked-worktree procedure, and push normally before live source annotation.
- **Implemented: Wikisource.** Create the pass-through template and its documentation, add it
  to the introduction appendix roster, then run the existing bot with `--no-save`, inspect
  exactly the two chapter previews, and apply the reviewed specification. The user's
  execution authorization includes these named live edits; no unrelated page is changed.
- **Implemented: refresh.** Complete `mam-wikisource-refresh`, including the source commit,
  public/private/public dependency loop, separately committed MAM change logs, and affected
  hand-run Sefaria/AJF and OSIS exports. Refresh the introduction independently as its
  README specifies. Inspect all generated diffs and annotate the two-site inventory.
- **Implemented: published prose.** Correct the mtgmtg page's false "unfounded" concern, name
  both MAM sites, and remove "verse-final" from its silluq group labels. Keep its grouping
  and text records unchanged. Correct any maintained prose that vouches for that false
  sentence under the receipt rules, without rewriting finished historical records.
- **Implemented: closeout.** Verify every actual call, both sites in every affected product,
  generated docs, changed-file formatting and required checks. Integrate and push private
  before public after the refresh loop. Update this plan and the canonical tracker with
  committed outcomes. Keep broad related issues open unless separately authorized.

## Commands and verification ownership

Read `AGENTS.md`, the Hebrew prose skill and MAM reference, `py/product_scopes.py`, the
iterative-document-editing and linked-worktrees skills, both repositories' instructions,
`py/ws/pywikibot-setup.md`, `in/mam-ws-intro/README.md`, and the refresh skill plus its
dependent-refresh reference before their stages. Use explicit account configuration for
pywikibot; credentials and bot runtime files stay outside tracked source.

All commands below run from the public development root with its home interpreter:

```powershell
& "C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe" py/main_authored.py gen-mam-parsed-docs
```

```powershell
& "C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe" py/main_mam_simple.py
```

```powershell
& "C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe" py/main_mam4sef.py --both-sef-and-ajf
```

```powershell
& "C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe" py/main_mam_osis.py
```

Use the actual CLI help for bot selectors and generation commands. Before any Git child
process runs, provide its exact development path through process-local `GIT_CONFIG_*`.
No wildcard/global Git trust is used. After the live bot, follow the refresh runbook's
prediction and diff judgment rather than restoring unexpected output.

Expected zero-use changes are source support, guides, their generated pages and unused-tag
reports. Biblical text and corpus occurrence inventories remain unchanged. After annotation,
expect structural wrappers at exactly the two sites, the intended noteless meteg removals,
two OSIS notes, and primary-stress corrections. Any other text or output difference requires
an explanation before integration. Record actual check results and stage commits here as
work completes.

## Support-stage results, 2026-10-12

Codex's zero-use mega passed all 60 steps. Real parser and product paths accepted both
proposed source annotations in scratch inputs; MAM-with-doc text remained identical,
MAM-simple retained both marks and explicit position, Sefaria/AJF removed the later meteg,
OSIS retained both marks with a note, and Phonetic MAM computed the earlier primary stress
while retaining both marks. Differential and focused tests passed (35 tests, 8 subtests).
The private retained diagnostics regenerated all 39 books without a tracked output change.
A fresh independent dispatch review found no blocker.
The full suite passed: 1,050 tests, five declared skips and 82 subtests. Both live
bot preview artifacts equal exactly their intended one-line substitution, with all
other mirrored source lines unchanged.
After incorporating current main, all 60 mega steps passed again and 13 focused
integration tests passed. Survey support then passed zero-use generation and site
claim checks, 15 focused tests, and a separate two-site candidate check: two
disjunctive silluq records, each without a following word. Its occurrence inventory
was empty throughout the support stage. The parser's preservation handler explicitly
evaluates Scripture parameter 1 and preserves validated position metadata parameter 2.

The deliberately regenerated hand-run exports also caught up with previously lagging
inputs: Sefaria and OSIS now show the existing qere-first pairs at 2 Samuel 20:23,
Jeremiah 48:21, Ezekiel 39:25 and 2 Chronicles 13:19; Sefaria/AJF now include the existing
second telisha at Judges 19:23 and selected qamats at 2 Kings 22:1. These six known
differences were audited separately from the new template, which had zero calls during
the support-stage check.

## Live source results, 2026-10-12

Support was pushed before source use (`efb2c407`). The template is revision 3088395,
the appendix entry is revision 3088396, and the chapter annotations are revisions
3088397 (1 Kings 7) and 3088398 (Job 4). Exact template expansion, saving-artifact
comparison and downloaded-mirror comparison passed. Each chapter has exactly its
one new wrapper; the full atoms and existing notes are unchanged. The observed
template tables now include the actually used name and all 57 MAM-parsed claims pass.

## Completed refresh and verification, 2026-10-12

The source is committed at `c486ccad`, its explained products at `accced5d`,
the generated grammar locks at `13c79810`, and the separately audited change logs
at `22eac9b4`. The public/private/public dependency loop is complete. The selected
private checkout passed its refresh profile and affected integration checks, then
was integrated and pushed before the public implementation at `3f9746e8`.
Both home clones were verified clean on main and equal to origin/main.

MAM-simple adds exactly the two structured leaves while retaining every text mark.
Sefaria/AJF remove only the later meteg at each site. OSIS retains both marks and
adds the two explanatory notes; its schema validation passes. MAM-with-doc text
is unchanged. Phonetic MAM changes only the two primary-stress spans, from na/no
to lah/loh in 1 Kings 7:37 and from hu to men in Job 4:12, retaining its Hebrew.
The post-stress-meteg survey adds these two verse-final records: 232 cases become
234, with one additional prose case and one additional poetic case. Its source
annotation differential passes. The Methods page follows both annotations.

The live refresh exposed two bounded statement checks: the next-conjunctive
appendix's partition omitted absent following words, and the active survey
docstring claimed all cases had conjunctive stress. Both now distinguish the
verse-final silluq cases. Near-Aleppo's wrapper resolution preserves the full atoms
and newly inventories their two unchanged notes; the fresh reviews retain both
source clauses in explicit MAM context. The final mega passes all 60 steps,
including the 1,554-note differential, 24 near-Aleppo books and 95 rendered files.
It adds no further product differences after the dependency loop.

The final suite reports 1,075 passed, five declared skips and one outdated
independent XML-oracle failure. The production XML reader already accepted the
new leaf. `py/tests/test_mam_xml_verses.py` now independently recognizes its exact
two-attribute, childless shape and reads only its marked text. All three
full-corpus XML-reader checks then pass. Black and whitespace checks pass.
The full suite and mega were not repeated after this isolated oracle edit;
production behavior, source data and products remained unchanged, so the other
results remain applicable under the approved review trial.

The final change-log generation adds exactly the two template changes, moving
the unreleased count from eight to ten. Named historical releases remain unchanged.
The freshness guard passes before and after the log commit. The runbook's separate
2 Kings 22:1 check still finds only one qamats reading in the release and rendered
page, with 309 prose variant rows in the survey; its existing README disclosure
remains applicable.

Documentation is complete in MAM-parsed-plus, MAM-simple XML and JSON, Sefaria/AJF
and its older encoding guide, OSIS, Phonetic MAM and near-Aleppo. The mtgmtg page's
two-site explanation and labels are corrected. The canonical issue is closed with
the [agent-written completion record](https://github.com/bdenckla/phonetic-hbo/issues/78#issuecomment-6132516648).
Generated pages follow the existing scheduled Pages deployment.
