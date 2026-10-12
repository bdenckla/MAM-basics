# Support and annotate silluq before a later meteg

State: live

## Approved execution snapshot, 2026-10-12

Ben instructed Codex: "Proceed as you suggest." He confirmed: "we want to remove the
meteg in editions without notes", identifying Sefaria/AJF, and requested documentation
in MAM-parsed-plus, MAM-simple and the older Sefaria encoding guide. This snapshot
supersedes the one-site, source-first implementation sequence proposed on 2026-09-08.
The undertaking remains tracked by [phonetic-hbo#78](https://github.com/bdenckla/phonetic-hbo/issues/78).

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
- **Active: support integration.** Commit coherent public and private support, update
  private vendoring provenance from the committed public source, integrate through the
  linked-worktree procedure, and push normally before live source annotation.
- **Active: Wikisource.** Create the pass-through template and its documentation, add it
  to the introduction appendix roster, then run the existing bot with `--no-save`, inspect
  exactly the two chapter previews, and apply the reviewed specification. The user's
  execution authorization includes these named live edits; no unrelated page is changed.
- **Active: refresh.** Complete `mam-wikisource-refresh`, including the source commit,
  public/private/public dependency loop, separately committed MAM change logs, and affected
  hand-run Sefaria/AJF and OSIS exports. Refresh the introduction independently as its
  README specifies. Inspect all generated diffs and annotate the two-site inventory.
- **Implemented: published prose.** Correct the mtgmtg page's false "unfounded" concern, name
  both MAM sites, and remove "verse-final" from its silluq group labels. Keep its grouping
  and text records unchanged. Correct any maintained prose that vouches for that false
  sentence under the receipt rules, without rewriting finished historical records.
- **Active: closeout.** Verify every actual call, both sites in every affected product,
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

The deliberately regenerated hand-run exports also caught up with previously lagging
inputs: Sefaria and OSIS now show the existing qere-first pairs at 2 Samuel 20:23,
Jeremiah 48:21, Ezekiel 39:25 and 2 Chronicles 13:19; Sefaria/AJF now include the existing
second telisha at Judges 19:23 and selected qamats at 2 Kings 22:1. These six known
differences were audited separately from the new template, which still has zero calls.
