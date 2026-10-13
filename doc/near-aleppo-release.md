# Releasing near-Aleppo

State: runbook

Use this procedure when Ben requests a near-Aleppo release. It covers the
dataset ZIP, release notes, dated entry-point links, and GitHub publication.
Ben approved creating this maintained runbook on 2026-10-13. The
[October 12 release record](near-aleppo-release-status.md) supplies the
packaging and verification precedent; it remains a finished record.

## 1. Establish the checkout and release identity

Follow `AGENTS.md` and [the review trial](review-trial.md). Verify the checkout's
root, HEAD, branch or detached state, and status before editing. Record the
source checkout and starting commit, the development checkout, interpreter,
and agent responsible for final integration in the new release record. Use
the linked-worktrees skills if working in a linked worktree; its home clone
provides its interpreter and receives final integration.

Use PowerShell 7. The command examples below assume a full clone at
`$HOME/GitRepos/MAM-basics`; substitute the verified paths for another clone
or a linked worktree. Run the Python commands from the repository root.

```powershell
$releaseRoot = "$HOME/GitRepos/MAM-basics"
```

```powershell
$releasePython = "$releaseRoot/.venv/Scripts/python.exe"
```

Choose the release date and record it as `$releaseDate`, in `YYYY-MM-DD` form.
The established naming scheme is tag `near-aleppo-YYYY-MM-DD`, title
`Near-Aleppo — YYYY-MM-DD`, ZIP `near-aleppo-YYYY-MM-DD.zip`, and notes
`near-aleppo-release-notes-YYYY-MM-DD.md`. Set the tag and notes filename:

```powershell
$releaseTag = "near-aleppo-$releaseDate"
```

```powershell
$releaseNotesName = "near-aleppo-release-notes-$releaseDate.md"
```

Inspect published GitHub releases and remote tags. Verify that the chosen
identity is unused and select the preceding published near-Aleppo release
as the comparison anchor. Record its exact tag and peeled commit. GitHub's
[`releases/latest` URL](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases)
selects a release for the whole repository, which may also release other products.
Find near-Aleppo releases by their recorded tags and scope.

## 2. Prepare notes and update the release links

Write the draft in `doc/near-aleppo-release-notes-YYYY-MM-DD.md`. Compare the
selected near-Aleppo source and product changes with the preceding release.
Describe consumer actions, implemented changes, remaining limitations, and
attachment contents. Read every claimed figure from the current artifacts.
Load the Hebrew-prose skill and its MAM-basics reference for Hebrew discussion;
attribute manuscript claims to the images or prior readings actually consulted.

Give Ben the draft for his editing step. Use the authorization already given
for this release: a draft-only request does not authorize publication, while
an existing publication instruction needs no repeat approval. Once accepted,
finalize the release date, tag, title, and official notes.

Update the dated release label and tag-specific URL in both maintained sources:

- [`py/near_aleppo/doc_pages.py`](../py/near_aleppo/doc_pages.py), the paragraph
  beginning "For the dataset ZIP and release notes, see the" in `pages()`.
- [`out/near-aleppo/README.md`](../out/near-aleppo/README.md), the paragraph
  beginning with the same words.

Both links must point to
`https://github.com/bdenckla/MAM-basics/releases/tag/near-aleppo-YYYY-MM-DD`
and display that release's date. Make these edits before selecting the release
commit and packaging, so the ZIP's README contains its own release link.
The new URL becomes usable when the release is published.

Format the changed Python source, then regenerate the HTML:

```powershell
& $releasePython -m black "$releaseRoot/py/near_aleppo/doc_pages.py"
```

```powershell
& $releasePython "$releaseRoot/py/main_near_aleppo.py" --html
```

Read `gh-pages/near-aleppo/index.html` and the README. Verify their dates and
destinations agree with the selected release identity. Inspect every generated
diff; a release-link-only edit should change only the dataset index HTML.
Regenerate any other products owed by the actual source changes, following
[the build guide](near-aleppo-build.md) and the repository's refresh procedures.

## 3. Verify and freeze the source commit

Run the focused check against the prepared release tree:

```powershell
& $releasePython "$releaseRoot/py/main_near_aleppo.py" --check
```

Check the release Markdown's UTF-8 encoding, LF endings, State lines, factual
claims, and local link targets. Run the existing prose mark-order lint after
the new Markdown is staged, so the tracked-file inventory includes it:

```powershell
& $releasePython "$releaseRoot/py/main_test.py" py/tests/test_prose_mark_order.py -q
```

```powershell
git -c "safe.directory=$releaseRoot" -C $releaseRoot diff --cached --check
```

The review trial controls broad-check timing; release preparation does not
automatically require the mega or full suite. Record completed checks and any
deferred checks accurately. Stop on a failed check or unexplained generated diff.

Commit the finished preparation. Fetch origin, integrate incoming main changes
under the full-clone or linked-worktree procedure, repeat affected checks, and
push normally. Select the exact integrated commit as `$releaseCommit`, record
it, and require a clean checkout. If a later source change is to enter the release,
repeat the affected preparation and checks before selecting the final commit.

## 4. Package and verify committed bytes

Choose a fresh `$releaseAssets` directory under the checkout's ignored `.novc/`.
There is no maintained release-packaging command. Write a uniquely named UTF-8
scratch script there that reads Git blob bytes through a binary subprocess
and creates the two attachments from `$releaseCommit`.

The ZIP contains `README.md`, `LICENSE.md`, and every tracked `plus/*.json`
from that commit's `out/near-aleppo/`, with those names at the ZIP root.
Enumerate the expected files from the committed tree using a NUL-delimited
Git listing, splitting on `"\0"`. Use `git show <commit>:<path>` to obtain
each member's bytes. Export the committed notes from
`doc/near-aleppo-release-notes-YYYY-MM-DD.md` as the separate notes attachment.
Git child processes inherit the exact checkout's process-local `safe.directory`
configuration, as `AGENTS.md` requires.

Verify exact member names, no duplicate members or directory entries, ZIP CRCs,
UTF-8 JSON parsing, and byte equality between every member and its Git blob.
The notes attachment must equal its committed blob as well. Exclude HTML,
crops, fonts, review records, and scratch files. Record both attachments'
filenames, byte sizes, and SHA-256 digests.

Build directly from blob bytes. The October 12 record's passage "Fixed before
upload" documents that the initial Git ZIP export changed `LICENSE.md` from
LF to CRLF and failed this comparison. A text-mode export is not sufficient.

## 5. Upload a draft and verify the downloaded attachments

After publication has been authorized, write an annotated-tag message to a
UTF-8 file with LF endings at `$releaseAssets/tag-message.txt`. Create the tag
at the selected commit and push only that tag:

```powershell
git -c "safe.directory=$releaseRoot" -C $releaseRoot tag -a $releaseTag $releaseCommit -F "$releaseAssets/tag-message.txt"
```

```powershell
git -c "safe.directory=$releaseRoot" -C $releaseRoot push origin "refs/tags/$releaseTag"
```

Verify that the remote tag peels to `$releaseCommit`. Create a draft release
with the two verified attachments and the exported official notes as its body.
[`gh release create`](https://cli.github.com/manual/gh_release_create)'s
`--verify-tag` prevents automatic creation of a tag at a different commit.

```powershell
gh release create $releaseTag "$releaseAssets/$releaseTag.zip" "$releaseAssets/$releaseNotesName" --repo bdenckla/MAM-basics --draft --verify-tag --title "Near-Aleppo — $releaseDate" --notes-file "$releaseAssets/$releaseNotesName"
```

Choose a fresh `$releaseDownloads` directory under `.novc/` and download both
uploaded attachments. The [CLI download command](https://cli.github.com/manual/gh_release_download)
accepts a destination directory:

```powershell
gh release download $releaseTag --repo bdenckla/MAM-basics --dir $releaseDownloads --pattern "$releaseTag.zip" --pattern $releaseNotesName
```

Repeat the complete archive and notes comparison on these downloaded files,
including sizes and digests. Verify that the draft's body equals the committed
official notes and that its tag and title identify the intended release.

## 6. Publish and record the outcome

Publish the verified draft using [`gh release edit`](https://cli.github.com/manual/gh_release_edit):

```powershell
gh release edit $releaseTag --repo bdenckla/MAM-basics --draft=false
```

Read the published release back. Verify its tag-specific URL, title, body,
published state, prerelease state, peeled tag commit, and attachment metadata.
Confirm the index and README links resolve to this release. The website and
example edition remain live pages that can change after the dataset release.

Finish a new dated receipt, `doc/near-aleppo-release-record-YYYY-MM-DD.md`,
recording authorization, comparison anchor, source commit, release URL and ID,
tag object, verification results, and attachment sizes and digests. Commit and
push that record without moving the release tag. Follow the
iterative-document-editing skill for finished receipts and later corrections;
keep this runbook current in place.

The product scope is distributed data, `out/near-aleppo/`, with the overview
link also reaching published `gh-pages/`. Tag pushes and GitHub publication
are separate outward-facing acts. Replacing a published attachment, moving a
tag, or rewriting history requires Ben's authorization for that specific act.
