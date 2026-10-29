# Taamey D

Taamey D is a font for Biblical Hebrew, derived from Taamey Frank CLM, a font designed by Yoram
Gnat. This directory holds its sources and the files its build generates from them. The pages
that document it are under [`gh-pages/taamey-d/`](../gh-pages/taamey-d/index.html), published
at https://bdenckla.github.io/MAM-basics/taamey-d/. Paths in this file are written from the
repository root, where every command below runs.

Taamey D's sources, build and pages moved here from the private hbofonts repository on
2026-10-28, and since then Taamey D work happens here. Its shaping checks, their test corpus,
the corpus refresh and the baseline acceptance followed on 2026-10-29, and so did the release
tool, so new releases are published from here. The releases published from hbofonts stay in
hbofonts' downloads, at https://bdenckla.github.io/hbofonts/downloads/, and the downloads index
that the release tool writes here links them. By Ben's decision of 2026-10-28, issues opened
before the move stay in hbofonts' tracker, and new Taamey D issues go to MAM-basics' tracker.

## What is where

- `Taamey-D/font-m-TaD/`: the font's sources and the files the build generates from them.
- `Taamey-D/qa-in/`: the shaping checks' corpus, test cases with their expected Taamey D output.
- `Taamey-D/qa-out/Taamey_D/`: the shaping checks' reports on the font.
- [`py/main_taamey_d_build.py`](../py/main_taamey_d_build.py) and `py/taamey_d_build/`: the
  build, run by hand.
- [`py/main_taamey_d.py`](../py/main_taamey_d.py) `doc` and `py/taamey_d/doc/`: the generator
  of two of the pages.
- `py/main_taamey_d.py` `qa`, `corpus` and `accept-baseline`, and `py/taamey_d/qa/`: the
  shaping checks, the corpus refresh and the baseline acceptance.
- `py/main_taamey_d.py` `release-check` and `release-publish`, and `py/taamey_d/release.py`:
  the release tool.
- `gh-pages/taamey-d/`: the pages, their stylesheet and the comparison images.
- `gh-pages/taamey-d/downloads/`: the published releases, which the release tool writes.
- [`Taamey-D/LICENSE.md`](LICENSE.md): the terms of all of these, path by path.

## Authored sources and generated outputs

The authored font inputs, in `Taamey-D/font-m-TaD/`, are `Taamey_D.sym.fea`,
`Taamey_D-nofea.sym.sfd` and `license.sym.txt`, with the FontForge script
`ffscript_generate_sfd_n_ttf.py`. The build generates the following files beside them; do not
hand-edit these generated files:

- `Taamey_D.fea`, `Taamey_D-nofea.sfd` and `license.txt`, the three templates filled in;
- `Taamey_D.sfd`, `Taamey_D.ttf`, `Taamey_D.woff` and `Taamey_D.woff2`, FontForge's outputs.

The plain `.fea` and `.sfd` files are tracked and public. They are deterministic regenerations
of the symbolic sources that every source archive publishes, and publishing them was decided on
2026-10-28, when Ben approved the plan for this move. Source archives hold the symbolic sources
rather than these plain `.fea` and `.sfd` files.

The release notes, `Taamey-D/font-m-TaD/release-notes.txt`, are also authored. Rewrite them
before each release to list that release's changes; their first line must be
`Taamey D <version>`, with the version from `py/taamey_d_build/font_version.py`.

`py/main_taamey_d.py doc` generates exactly two pages, `gh-pages/taamey-d/Taamey_D.html` and
`gh-pages/taamey-d/Xolam_xaser_for_alef.html`. The landing page, `gh-pages/taamey-d/index.html`,
and the stylesheet, `gh-pages/taamey-d/Taamey-doc-styles.css`, are authored.

`gh-pages/taamey-d/img/comparison/` holds the 102 comparison images of `Taamey_D.html`, in
Taamey Frank CLM, SBL Hebrew and Ezra SIL, with their `PROVENANCE.json`. They were rendered
once, on 2026-10-28, and are frozen outputs: do not hand-edit them. The generator refuses to
write the page if a comparison cell no longer matches its image's record.

## Building the font

```powershell
./.venv/Scripts/python.exe py/main_taamey_d_build.py
```

The build fills the three templates, then runs the FontForge script with `Taamey-D/` as
FontForge's working directory, so that the script's relative base, `font-m-TaD/Taamey_D`,
resolves here and in an extracted source archive alike. On Windows it clears each filled file's
read-only attribute before filling it and sets the attribute again afterwards, as a reminder not
to edit the file.

FontForge must be installed separately, with its Python scripting support and WOFF2 support.
The build uses the executable or batch file that `--fontforge` names, else `fontforge` on PATH,
else, on Windows, `FontForgeBuilds/fontforge.bat` under `ProgramFiles` or `ProgramFiles(x86)`.
It runs a Windows batch file through the Windows command processor. FontForge 20251009
reproduces the tracked outputs byte for byte (checked 2026-10-28, and on 2026-10-29 for 1.2,
also from nothing but the files of its source archive). A different FontForge can change the
built bytes: explain such a difference rather than accepting it.

The build is a hand-run generator, which the mega does not run. Ben's decision of 2026-10-28:
"Yes, keep FontForge run out of MAM-basics mega." So after a change to a source or to the build,
rerun the build, read every generated diff, and commit the sources and outputs together. The
build never writes `gh-pages/woff2/Taamey_D.woff2`, which "Publication" below explains.

A build that changes the font also owes a run of the shaping checks, as "Checking the font's
shaping" below says, reading every result: a `FAIL` or `SKIP` is a finding that needs
explaining.

The build's package, `py/taamey_d_build/`, and its entry point import only each other and the
Python standard library, so that they can ship in a source archive under GPL-2.0-or-later;
`py/tests/test_taamey_d_build_imports.py` checks this.

## Generating the pages

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py doc
```

The mega runs it as its step `taamey-d-doc`. Read both generated pages' diffs.

## Checking the font's shaping

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py qa
```

The shaping checks shape every test case in `Taamey-D/qa-in/` with
`Taamey-D/font-m-TaD/Taamey_D.ttf` and rewrite the reports in `Taamey-D/qa-out/Taamey_D/`. They
print a result for each check and test-case file. They fail on a `SKIP`, and on a `FAIL` from the
anchor-family lint, which checks statically that the glyphs of each letter agree on their
mark-to-base anchors; a deliberate difference among a letter's glyphs goes, with its reason, in
that lint's closed exception table, in `py/taamey_d/qa/anchor_families.py`. A shaping check's
`FAIL` does not fail the run, but its failing cases go into the reports. Read every result: a
`FAIL` or `SKIP` is a finding that needs explaining, not a green check.

The mega runs the checks as its step `taamey-d-qa`, which also fails if the reports then differ
from Git's index. So after an approved baseline acceptance, stage the accepted `Taamey-D/qa-in/`
and `Taamey-D/qa-out/` files before running the mega.

## Refreshing the corpus

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py corpus
```

The corpus refresh rewrites the `Taamey-D/qa-in/bible_words_*.testcases.json` test cases from
this repository's word lists, `out/mam-qere-words.json` and `uxlc/out/uxlc-words.json`, which the
mega's `wordlist` and `uxlc-word-list` steps write. It reads them in the checkout it runs in, a
linked worktree's own files included. It refuses to run while either list has uncommitted
changes, and it prints the commit it read, which the refresh's commit message records. It
rewrites no other `Taamey-D/qa-in/` file, appends new test cases in sorted order to the
highest-numbered `bible_words` file, and stops on an SLH word that the multirun check could not
split. It computes every file's new contents before writing any, and prints how many test cases
each file drops, adds and relabels.

With `--check`, it computes the same refresh but writes nothing, and reads the word lists as they
stand, committed or not. It exits 0 when its only finding is a pending refresh, which its last
line calls `REFRESH PENDING`, and non-zero on any error that would stop a refresh. The mega runs
it that way as its last step, `taamey-d-corpus`, and reports a pending refresh at the end of its
output rather than failing. By Ben's decision of 2026-10-28, a refresh of MAM's text does not
oblige refreshing the corpus: the corpus is a pinned test population, refreshed deliberately.

New test cases arrive without expected outputs, so a refresh needs a baseline acceptance. The
corpus holds expected outputs for Taamey D only.

## Accepting a baseline

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py accept-baseline
```

A baseline acceptance takes the output that the last `qa` run observed for each failing
regression case, from the reports in `Taamey-D/qa-out/Taamey_D/`, and writes it into the test
cases of `Taamey-D/qa-in/` as Taamey D's expected output. It is an explicit baseline operation,
not a test, and it needs Ben's approval. Then run `qa` again, read every result, and commit the
accepted test cases and reports together.

## Publishing a release

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py release-check
```

`release-check` checks the published releases in `gh-pages/taamey-d/downloads/` and writes
nothing. Each release is an immutable snapshot directory,
`snapshots/<version>-MAM-basics-<first 12 hex digits of its source commit>/`, holding the binary
archive `Taamey_D.zip`, the corresponding-source archive `Taamey_D-sources.zip`, their checksums
and a provenance manifest. `latest/` is a byte-identical copy of the snapshot that
`release-publish` installed last, and `index.html` lists them all. The check compares every snapshot's archives with the files of its
source commit and checks the index's links, and it fails if a committed snapshot changed or
disappeared, in the working tree or in Git's history. Before the first release it says that no
snapshot is published. The mega runs it as its step `taamey-d-release-check`, which a cloud
session skips when its shallow checkout lacks a snapshot's source commit.

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py release-publish --snapshot-commit <full HEAD>
```

`release-publish` is outward-facing release preparation, never a verification command, so the
mega does not run it. Before it, set the version in `py/taamey_d_build/font_version.py`, rewrite
the release notes, run the build, `doc` and `qa`, read every result, and commit. Then run
`release-publish` with that commit in full. It refuses a commit other than `HEAD`, a release input
that differs from its committed bytes, and release notes whose first line is not
`Taamey D <version>`. It checks the existing releases, builds the snapshot twice in scratch
directories and compares the two builds, installs the new snapshot, replaces `latest/` with a
copy of it only once the new snapshot is verified, and rewrites the index. Then run `release-check`, read both outputs, and commit the
snapshot, `latest/` and the index together. Do not hand-edit those generated files: snapshot
directories are append-only, and only `latest/` is ever replaced.

The binary archive holds the TTF, WOFF and WOFF2 with `license.txt` and the release notes. The
source archive holds the three templates, `license.txt`, the FontForge script and the build, each
at its path in this repository, so that the build runs from the extracted archive's root; the
tool refuses plain `.sfd` and `.fea` files there. The index lists this repository's snapshots
first, then, by absolute URL, the releases published from hbofonts, whose `downloads/latest/`
stays frozen at Taamey D 1.1. A release reaches the site only at the next Pages dispatch, which
needs Ben's go-ahead, and the site's pages take it only through a new pin, as "Publication" below
says.

## Hebrew safeguards

Never apply Unicode normalization to Hebrew or casually reorder Hebrew marks. Exact code-point
sequences are significant to shaping tests, including deliberately constructed alternative mark
orders. A baseline acceptance, which accepts observed Taamey D output as the shaping checks'
expected output, needs Ben's approval.

The corpus keeps its exact code points, so a few of its words are not in MAM-normal
order. It is outside `py/check_mark_order.py`'s scope, and `doc/mam-normal-mark-order.md` lists
it among the trees that preserve another order on purpose.

## Taamey D support scope

Add Taamey D support for a mark combination only when it has a concrete need, such as a word in
the corpus or a MAM documentation note. A collision that occurs only in a combination with no
such need, including an artificial mark order, is not work to pursue. Ben, 2026-10-22, declining
to fix a ḥataf vowel's overlap with a final nun's descender: "I'm barely willing to add support
for known weird things like the pointing we just added support for on final nun. I certainly
don't want to go 'looking for trouble', supporting things that not only have no concrete need,
but I can't even imagine a concrete need for."

Taamey D also does not accommodate a source's encoding errors. Ben, 2026-10-27, of the UXLC's
zero-width joiner (ZWJ) where a combining grapheme joiner belongs in Job 32:6: "We don't need to
(and should not) bend over backwards to support incorrectly encoded words in Taamey D." Such a
word enters the corpus in its correct encoding instead, with a provenance suffix saying so; the
corpus refresh holds the corrections. Ben asked the same day for the refresh to "reject future
wacky uses of ZWJ". It accepts a ZWJ only in a request for a meteg in the middle of a ḥataf vowel
(ḥataf vowel, ZWJ, meteg), the one use the Unicode Standard's Hebrew section gives it; any other
ZWJ that its corrections leave stops the refresh until someone decides the word's correct
encoding.

Below a letter, Taamey D places marks generally since 1.1: in `mkmk0BlwChainGeneral` every below
mark hangs off the below mark before it, whatever their kinds, and `ccmp00DeleteCgj` deletes every
CGJ, so an accent before a vowel, a second vowel, or two below accents need no rule for the pair.
The rule of 2026-10-22 above still governs the rest: marks above a letter, whose chaining covers
only the corpus's pairs, and special cases such as a below mark that meets a letter's descender or
a deḥi or yetiv at the letter's right edge. Ben, 2026-10-27, after the measurement in
`Taamey-D/font-m-TaD/Taamey_D.sym.fea`'s "Note on the general below-mark chain": "Prepare the
general below-mark chain for main."

## Publication

The site's pages that set Hebrew in Taamey D, `gh-pages/taamey-d/Taamey_D.html` among them, load
the site's one copy of the font, `gh-pages/woff2/Taamey_D.woff2`. By Ben's decision of
2026-10-28, MAM-basics' pages take the font by pinning a released snapshot into
`in/font-support/taamey-d-<version>/`; the pin is now Taamey D 1.2, the first release published
from here, in [`in/font-support/taamey-d-1.2/`](../in/font-support/taamey-d-1.2/README.md). So
the build never writes that copy, and a new release reaches the pages only through a new pin,
which `py/py_html/taamey_d_assets.py` checks. `git log -- in/font-support/` lists the commits
that made each pin, and so every file a new pin must change.

New releases come from MAM-basics: "Yes, new releases should come from MAM-basics." (Ben,
2026-10-28). "Publishing a release" above says how. Publishing a release is an outward-facing
act.
