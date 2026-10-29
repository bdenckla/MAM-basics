# Taamey D

Taamey D is a font for Biblical Hebrew, derived from Taamey Frank CLM, a font designed by Yoram
Gnat. This directory holds its sources and the files its build generates from them. The pages
that document it are under [`gh-pages/taamey-d/`](../gh-pages/taamey-d/index.html), published
at https://bdenckla.github.io/MAM-basics/taamey-d/. Paths in this file are written from the
repository root, where every command below runs.

Taamey D's sources, build and pages moved here from the private hbofonts repository on
2026-10-28, and since then Taamey D work happens here. Its shaping checks with their test
corpus, and its release tool with the downloads it publishes, are still in hbofonts and follow
later. Until the release tool arrives, Taamey D's downloads remain at
https://bdenckla.github.io/hbofonts/downloads/. By Ben's decision of 2026-10-28, issues opened
before the move stay in hbofonts' tracker, and new Taamey D issues go to MAM-basics' tracker.

## What is where

- `Taamey-D/font-m-TaD/`: the font's sources and the files the build generates from them.
- [`py/main_taamey_d_build.py`](../py/main_taamey_d_build.py) and `py/taamey_d_build/`: the
  build, run by hand.
- [`py/main_taamey_d.py`](../py/main_taamey_d.py) `doc` and `py/taamey_d/doc/`: the generator
  of two of the pages.
- `gh-pages/taamey-d/`: the pages, their stylesheet and the comparison images.
- [`Taamey-D/LICENSE.md`](LICENSE.md): the terms of all of these, path by path.

## Authored sources and generated outputs

The authored font inputs, in `Taamey-D/font-m-TaD/`, are `Taamey_D.sym.fea`,
`Taamey_D-nofea.sym.sfd` and `license.sym.txt`, with the FontForge script
`ffscript_generate_sfd_n_ttf.py`. The build generates these files beside them, which must not be
hand-edited:

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
reproduces the tracked outputs byte for byte (checked 2026-10-28). A different FontForge can
change the built bytes: explain such a difference rather than accepting it.

The build is a hand-run generator, which the mega does not run. Ben's decision of 2026-10-28:
"Yes, keep FontForge run out of MAM-basics mega." So after a change to a source or to the build,
rerun the build, read every generated diff, and commit the sources and outputs together. The
build never writes `gh-pages/woff2/Taamey_D.woff2`, which "Publication" below explains.

The build and its entry point import only each other and the Python standard library, so that
they can ship in a source archive under GPL-2.0-or-later;
`py/tests/test_taamey_d_build_imports.py` checks this.

## Generating the pages

```powershell
./.venv/Scripts/python.exe py/main_taamey_d.py doc
```

The mega runs it as its step `taamey-d-doc`. Read both generated pages' diffs.

## Hebrew safeguards

Never apply Unicode normalization to Hebrew or casually reorder Hebrew marks. Exact code-point
sequences are significant to shaping tests, including deliberately constructed alternative mark
orders. A baseline acceptance, which accepts observed Taamey D output as the shaping checks'
expected output, needs Ben's approval.

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
corpus updater holds the corrections. Ben asked the same day for that updater to "reject future
wacky uses of ZWJ". It accepts a ZWJ only in a request for a meteg in the middle of a ḥataf vowel
(ḥataf vowel, ZWJ, meteg), the one use the Unicode Standard's Hebrew section gives it; any other
ZWJ that its corrections leave stops the update until someone decides the word's correct
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

The site's pages that set Hebrew in Taamey D, these among them, load the site's one copy of the
font, `gh-pages/woff2/Taamey_D.woff2`. By Ben's decision of 2026-10-28, MAM-basics' pages take
the font by pinning a released snapshot into `in/font-support/taamey-d-<version>/`; the pin is
now Taamey D 1.1, in [`in/font-support/taamey-d-1.1/`](../in/font-support/taamey-d-1.1/README.md).
So the build never writes that copy, and a new release reaches the pages only through a new pin.

New releases are to come from MAM-basics: "Yes, new releases should come from MAM-basics." (Ben,
2026-10-28). Until the release tool moves here, hbofonts' downloads index lists every release.
Publishing a release is an outward-facing act.
