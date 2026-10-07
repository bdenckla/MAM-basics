# Historical release inputs

These snapshots are permanent, tracked inputs to the change-log generator.
They contain the plus JSON at each boundary of the named releases in
`gh-pages/MAM-with-doc/change-log/releases.json`: the six boundaries of the
pre-migration releases, which are MAM-parsed commits, and each boundary pinned
since, which is a MAM-basics commit. Each snapshot is an uncompressed ZIP
archive named by the full hash of its commit. Each member is named
`plus/<file>`, the file's path relative to the MAM-parsed product root, and
holds that file's exact bytes at the commit. A MAM-basics snapshot holds only
the `.json` files of `MAM-parsed/plus/`, which are what the reader compares.
`manifest.json` records the source repository, commit dates in New York time,
source blob identifiers, and migration information. An entry's `repository`
names the repository its commit is in; an entry without one comes from the
manifest-wide `source_repository`, MAM-parsed. Preserve the JSON bytes,
including historical schema and filename differences; the reader handles
those differences without rewriting these inputs.

The archives are deterministic: member names are sorted, timestamps are fixed
at 1980-01-01 00:00:00, the creating platform is fixed to Unix, regular-file
permissions are 0644, and members use `ZIP_STORED`. Archive and member comments
and extra fields are empty. The reader checks the complete manifest/archive
member set, rejects duplicate or unlisted members, validates this metadata and
member CRCs, and reads members directly without extraction. The six
pre-migration archives were written on 2026-09-10, from loose JSON copies of
their files stored on 2026-09-06, by a program that was never tracked.
`py/mb_diff_mpu/mpplus_archive.py` writes the MAM-basics snapshots and, given
the members of each pre-migration archive, reproduces it byte for byte.

Ben's decision, 2026-09-06: common change-log generation must not require a
sibling MAM-parsed clone. Arbitrary historical comparisons remain available
through explicit, read-only use of a sibling clone. No history cache or
automatic fetch is used.

Ben's decisions, 2026-09-28: archive each MAM-basics boundary when it is
pinned, and label it as the older snapshots are labelled, by its full hash and
New York date. Snapshots of the six boundaries that lived in MAM-parsed had
been stored since 2026-09-06, as loose JSON until 2026-09-10 and as archives
since, and a later boundary was read from MAM-basics history, which a shallow
clone lacks beyond its depth. On 2026-09-28
the depth-50 clone of main at 8c2fa6c3 in a Claude cloud container held 117
commits and not cb95915, the boundary that 78559eba pinned on 2026-09-17, so
the mega's diff-mpplus step stopped there. cb95915 was archived that day. Its
new labels changed five published change-log files once: `2026-09-17.html` and
`.json`, `unpinned-latest.html` and `.json`, and `index.html`.

From the MAM-basics root, the usual command compares the latest named release
with committed `MAM-parsed/plus/` at MAM-basics HEAD:

```powershell
.venv/Scripts/python.exe py/main_diff.py mpplus
```

`--all` also regenerates every named release. Explicit `--old` and `--new`
accept stored release hashes or MAM-basics refs. The original migration
source commit also resolves to the byte-identical Land commit. A stored
release, whether a MAM-parsed or a MAM-basics commit, is labelled by its full
hash and that commit's date in New York time; any other MAM-basics ref, such
as HEAD, is labelled by the git tree id of `MAM-parsed/plus` and has no date.

To pin a release ending at HEAD, commit `MAM-parsed/plus/` and run, from the
MAM-basics root:

```powershell
.venv/Scripts/python.exe py/main_diff.py mpplus --pin "<name>"
```

The command appends `{"old": <the latest release's end>, "new": <HEAD's
7-character hash>, "name": <name>}` to `releases.json`, writes HEAD's snapshot
and manifest entry, regenerates the change log, and prints the paths to stage.
It commits nothing. The name is required and never derived: the earlier names
begin with their end commit's New York date, but release 2026-09-17 ends at a
commit dated 2026-09-16. The command refuses uncommitted changes under
`MAM-parsed/plus/`, a name already in `releases.json`, a release whose
`plus/*.json` blobs are those of the latest release's end, and a short hash that
already begins a snapshot's hash. Each pin adds a snapshot of about 13 MB to
every checkout, sparse checkouts of `MAM-parsed/` included, and to Git history
for good.

Before comparing anything, a change-log run refuses each boundary of
`releases.json` that it checks and that has no snapshot, and names the fix.
Which boundaries it checks depends on the run. `--all`, `--check` and the
mega's diff-mpplus step check every boundary. A run without arguments checks
only the latest release's end, the one boundary it compares. `--pin` checks the
latest release's end before it writes anything, and the other boundaries only
when it regenerates the change log, after it has written HEAD's snapshot, its
manifest entry and its line in `releases.json`; the fix a refusal names then
completes the pin. A run with explicit `--old` and `--new` checks no boundary.
A snapshot counts as stored when `manifest.json` lists it, so a listed snapshot
whose archive file is missing passes every guard and stops the run at its first
read, with an error that names the missing file but not the fix. For a boundary
pinned without `--pin`, run this in a clone that has the boundary's commit, then
run `--all`:

```powershell
.venv/Scripts/python.exe py/main_diff.py mpplus --archive "<boundary>"
```

A shallow clone that lacks the commit can fetch it once by its full hash:

```powershell
git fetch --depth=1 origin "<full hash>"
```

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
