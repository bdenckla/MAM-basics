# Historical release inputs

These snapshots are permanent, tracked inputs to the change-log generator.
They contain the plus JSON at each boundary of the named pre-migration
releases. Each directory is named by its full original MAM-parsed commit.
`manifest.json` records the source repository, commit dates, source blob
identifiers, and migration information. Preserve the JSON bytes, including
historical schema and filename differences; the reader handles those
differences without rewriting these inputs.

Ben's decision, 2026-09-06: common change-log generation must not require a
sibling MAM-parsed clone. Arbitrary historical comparisons remain available
through explicit, read-only use of a sibling clone. No history cache or
automatic fetch is used.

From the MAM-basics root, the usual command compares the latest named release
with committed `MAM-parsed/plus/` at MAM-basics HEAD:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp
```

`--all` also regenerates every named release. Explicit `--old` and `--new`
accept stored release hashes or MAM-basics refs. The original migration
source commit also resolves to the byte-identical Land commit. Dates for
that initial tree retain the source date; subsequent product changes use
the date of the commit that last changed the plus tree.

For an arbitrary pre-migration comparison, supply both revisions and opt
into the sibling clone:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp --legacy-history --old 9ce6ee5 --new 51082036e5907991d0d322cb6dfcc6404802099f
```

The clone must already exist, normally at
`C:/Users/BenDe/GitRepos/MAM-parsed`. `REPO_MAM_PARSED_DIR` or `REPOS_ROOT`
can locate a clone elsewhere. Missing history fails with an error; the
command never modifies or fetches the clone. The redirect host's current
HEAD contains no plus data, so select an explicit pre-evacuation revision.
An individual `legacy:<ref>` argument permits a comparison between an
arbitrary legacy revision and a MAM-basics revision.

The snapshots retain MAM's CC-BY-SA 4.0 terms; see [the product licence](../LICENSE.md).
