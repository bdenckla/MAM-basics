# Cambridge 1753 data under MAM-basics

No Python lives in this directory. Cambridge 1753 code lives under
`C:/Users/BenDe/GitRepos/MAM-basics/py/`, and every data path goes through
`cam1753_paths.py`. The corpus root is this directory; the shared MAM word-sequence
snapshot is `C:/Users/BenDe/GitRepos/MAM-basics/MAM-XML/`.

The fourteen tracked source spreads are the image inputs. `cam1753-pages/` is a
gitignored, derived 28-JPEG tree: run `main_cam1753_split_spreads.py` when an editor
or crop task needs it. The splitter also rewrites the 15 tracked split records. Do
not rerender `cam1753-gutter-profiles.png` as a verification step: matplotlib version
changes make that chart non-reproducible. `check_cam1753_all.py` is the artifact
oracle; it reports four checks and includes the 160-case word-finding check.

The column and line-break editors load page JPEGs from port 8119. Start that local
server in `C:/Users/BenDe/GitRepos/MAM-basics/cam1753` so their existing
`http://localhost:8119/cam1753-pages/` URLs resolve. The word-image previewer keeps
its explicit port 8753 and serves its gitignored `.novc` output there.

Preserve the stored Hebrew data exactly; do not normalize it. The MAM-basics
mark-order, escape-sequence, and NFC checks include this tree. The Ktiv source,
attribution, educational-and-research, and non-commercial terms for the image data
are recorded in `cam1753-spreads-provenance.md` and `../DATA-LICENSES.md`.
