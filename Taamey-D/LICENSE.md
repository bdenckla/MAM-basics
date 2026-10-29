Taamey D's files carry different terms, so this file gives them path by path, as
[`DATA-LICENSES.md`](../DATA-LICENSES.md) records them, and makes no other grant. It does not
cover everything below this directory with one license. Paths are written from the repository
root.

- `Taamey-D/font-m-TaD/`: the Taamey D font, its sources and the files its build generates from
  them, under the GNU General Public License, version 2, with the font-embedding exception that
  the font's OpenType name table states.
  [`in/font-support/taamey-d-1.1/FONT-NOTICE.txt`](../in/font-support/taamey-d-1.1/FONT-NOTICE.txt)
  transcribes that notice, and
  [`in/font-support/taamey-d-1.1/GPL-2.0.txt`](../in/font-support/taamey-d-1.1/GPL-2.0.txt)
  holds the complete GPL v2 text. The exception says that embedding the font in a document does
  not by itself cause the document to be covered by the GPL. The FontForge script in that
  directory, `ffscript_generate_sfd_n_ttf.py`, is under the GNU General Public License, version 2
  or (at your option) any later version (GPL-2.0-or-later).
- `Taamey-D/README.md` and this file: MAM-basics' own work, so GPL-3.0, the license of the
  repository's root [`LICENSE`](../LICENSE).

Taamey D's files elsewhere in this repository:

- `py/main_taamey_d_build.py` and `py/taamey_d_build/`, the build: GPL-2.0-or-later, an
  exception to the GPL-3.0 of the rest of `py/`.
- `py/main_taamey_d.py` and `py/taamey_d/`, the page generator: GPL-3.0, like the rest of `py/`.
- `gh-pages/taamey-d/index.html`, `Taamey_D.html`, `Xolam_xaser_for_alef.html` and
  `Taamey-doc-styles.css`: GPL-3.0 for the three pages and their stylesheet. The Hebrew they
  quote keeps its source's terms.
- `gh-pages/taamey-d/img/comparison/`: images made with Taamey Frank CLM, SBL Hebrew and Ezra
  SIL. No grant is made or implied over the fonts, whose terms remain their makers', as each
  font's name table states and `PROVENANCE.json` records. The texts keep their sources' terms.
- `gh-pages/woff2/Taamey_D.woff2`, the copy of the font that the site's pages load, and the
  pinned release in `in/font-support/taamey-d-1.1/`: the terms that `DATA-LICENSES.md` states
  for them.
