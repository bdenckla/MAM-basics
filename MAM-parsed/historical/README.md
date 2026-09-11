# Historical release inputs

These snapshots are permanent, tracked inputs to the change-log generator.
They contain the plus JSON at each boundary of the named pre-migration
releases. Each snapshot is an uncompressed ZIP archive named by its full
original MAM-parsed commit. Members retain their original `plus/...` names and
exact bytes.
`manifest.json` records the source repository, commit dates, source blob
identifiers, and migration information. Preserve the JSON bytes, including
historical schema and filename differences; the reader handles those
differences without rewriting these inputs.

The archives are deterministic: member names are sorted, timestamps are fixed
at 1980-01-01 00:00:00, the creating platform is fixed to Unix, regular-file
permissions are 0644, and members use `ZIP_STORED`. Archive and member comments
and extra fields are empty. The reader checks the complete manifest/archive
member set, rejects duplicate or unlisted members, validates this metadata and
member CRCs, and reads members directly without extraction.

Ben's decision, 2026-09-06: common change-log generation must not require a
sibling MAM-parsed clone. Arbitrary historical comparisons remain available
through explicit, read-only use of a sibling clone. No history cache or
automatic fetch is used.

From the MAM-basics root, the usual command compares the latest named release
with committed `MAM-parsed/plus/` at MAM-basics HEAD:

```powershell
.venv/Scripts/python.exe py/main_diff.py mpplus
```

`--all` also regenerates every named release. Explicit `--old` and `--new`
accept stored release hashes or MAM-basics refs. The original migration
source commit also resolves to the byte-identical Land commit. Dates for
that initial tree retain the source date; subsequent product changes use
the date of the commit that last changed the plus tree.

For an arbitrary pre-migration comparison, supply both revisions and opt
into the sibling clone:

```powershell
.venv/Scripts/python.exe py/main_diff.py mpplus --legacy-history --old 9ce6ee5 --new 51082036e5907991d0d322cb6dfcc6404802099f
```

The clone must already exist. `REPO_MAM_PARSED_DIR` or `REPOS_ROOT` locates it.
Missing history fails with an error; the
command never modifies or fetches the clone. Select explicit pre-migration
commits so comparisons do not depend on the redirect host's current contents.
An individual `legacy:<ref>` argument permits a comparison between an
arbitrary legacy revision and a MAM-basics revision.

The snapshots retain MAM's CC-BY-SA 4.0 terms; see [the product licence](../LICENSE.md).
