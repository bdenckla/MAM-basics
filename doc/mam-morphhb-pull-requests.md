# MAM-morphhb's pull requests to morphhb and OpenScriptorium

State: paused 2026-11-04, waiting for morphhb's maintainers to accept openscriptures/morphhb#114

Written by Claude (Opus 5.5) on 2026-11-04, on top of `825032c0`, at Ben's word ("Yes, track
it"), so that a fresh session can post the second pull request once the first is accepted.
Ben's words are quoted; everything else is Claude's.

## What is done

1. **The product.** `py/main_mam_morphhb.py` writes `MAM-morphhb/MAPM.xml`: today's MAM in the
   form of the 2014 OSIS file that openscriptures/morphhb keeps as `MAPM/MAPM.xml`.
   `MAM-morphhb/README.md` says what it keeps and what it changes. Ben approved the design on
   2026-11-03 ("Yes, as recommended"): BHS numbering, a marked qere, no song tables for now,
   and a minimal patch to OpenScriptorium's importer. The build is `83caf168`; `825032c0`
   records his exemption of the generator from reruns after a refresh of MAM's text ("Yes,
   exempt it").
2. **The morphhb pull request, posted.** On 2026-11-04 Ben decided the order: "I think it
   would make more sense to post the morphhb pull request and wait to see if it is accepted
   rather than post both pull requests with a caveat on the OpenScriptorium one that it
   shouldn't be merged unless and until the morphhb one is accepted". At his "Yes, post it",
   openscriptures/morphhb#114 was opened the same day from the branch `update-mapm` of his
   fork bdenckla/morphhb. Its one commit, `d266b727`, on morphhb's master `3d15126f`,
   replaces `MAPM/MAPM.xml` with `MAM-morphhb/MAPM.xml` of `83caf168` (Git blob `a267d742`)
   and updates `MAPM/readme.txt` and `README.md`.
3. **The OpenScriptorium pull request, drafted.** OpenScriptorium's
   `app/services/importers/oshb_features_importer.rb` downloads morphhb's `MAPM.xml` unless it
   has a cached copy, and reads it line by line with regular expressions that would misread
   the new file's marked qere. [The patch](mam-morphhb-pull-requests/oshb_features_importer.rb.diff)
   and [the pull request's description](mam-morphhb-pull-requests/openscriptorium-description.md)
   are ready. Asked what the patch's "minimal" meant, Ben answered: "Didn't we already agree
   to stick to the ugly-but-less-invasive "keep with regex" approach?" So the patch keeps the
   importer's regular expressions and line loop and makes four changes: it reads the qere seg
   beside a ketiv seg, in either order; it fixes the reset of a pending paragraph break; it
   updates the licence comment and the counts; and it says that a cached `tmp/oshb/MAPM.xml`
   must be deleted. The description names the three limitations it leaves.

## When morphhb has accepted openscriptures/morphhb#114

Run in a full MAM-basics clone in a forest the executing agent owns, with this file's commit
as an ancestor of `HEAD`, from the clone's root, in PowerShell 7. Every GitHub request goes
through `gh api`, one at a time; clone neither repository, and run none of their code. The
executing session owns the posting and commits its record to `main`. Nothing else in
MAM-basics changes, unless step 6 changes the patch or the description.

1. **Read the pull request's state**, with its reviews and comments:
   `gh api repos/openscriptures/morphhb/pulls/114 --jq '[.state, .merged, .merged_at] | @tsv'`.
   If it was closed unmerged, or changes were requested, report to Ben and stop. If a
   maintainer accepted it without merging it, reword the description's "Why" section and its
   item 4, which assume the merge.
2. **Check the file morphhb merged.** Master should hold `MAPM/MAPM.xml` as blob `a267d742`:
   `gh api repos/openscriptures/morphhb/contents/MAPM --jq '.[] | [.name, .sha] | @tsv'`.
   If a maintainer changed the file, re-derive the description's figures (step 6).
3. **Check OpenScriptorium's importer.** It must still be blob
   `5a6c6b519e3794a9392ed5d2adede1e303fe94a5`, the file the patch was made against:
   `gh api repos/OpenScriptorium/OpenScriptorium/contents/app/services/importers/oshb_features_importer.rb --jq .sha`.
   If it changed, re-derive the patch and the figures (step 6).
4. **Ask Ben for the go.** Posting forks OpenScriptorium/OpenScriptorium into his account,
   commits the patched file to a branch of the fork and opens the pull request: three outward
   acts.
5. **Post, at his go,** as the morphhb pull request was posted:
   - read the default branch and the file's mode, and fork the default branch only;
   - apply the patch to the file as GitHub has it with
     `git -c core.autocrlf=false apply`, since Git for Windows' system configuration sets
     `core.autocrlf=true` and `git apply` would otherwise write CRLF line endings; the result
     must be Git blob `f361a7f44a1b65ebc15048b41b37520719539c65`
     (`git hash-object --no-filters`), and so must the blob that the upload returns;
   - make a tree on the default branch's tree that replaces only that path, a commit whose
     message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, and a
     branch; compared with the default branch, it must change that one file;
   - open the pull request with the description's `Title:` line as its title and its text
     from "## Why" to the end as its body, maintainers allowed to edit. First check the body
     for an at-sign, which notifies the GitHub user it names, and for HTML comments; then
     read the pull request back and compare it with the description.
6. **Re-derive figures,** if step 2 or 3 needs it. The description's figures came from a
   scratch Python port of the importer's regular expressions and line loop, mirroring Ruby's
   ASCII-only `\s` and `String#strip`, with WLC's verses modelled by MAM-simple's BHS
   inventory, run without and with the patch on the 2014 file (`MAM-OSIS/MAPM-orig/MAPM.xml`)
   and on the new one. It is not tracked; the description's "How this was checked" is its
   specification.
7. **Record the posting here:** a dated item under "What is done", and the State.

Load the `hebrew-prose` skill before changing the description's prose about accents, and
check by script every Hebrew form written into it against the file it comes from.
