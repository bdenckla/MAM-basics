# The morphhb pull request on the Decalogues' and Genesis 35:22's strands, on ice

State: paused 2026-11-16, on ice at Ben's request: prepared and not posted; its 14 decisions open.

Written by Claude (Opus 5.5) on 2026-11-16, New York time. Ben, that morning: "put this work
"on ice": git-track it for deep storage, perhaps never to return to it, but perhaps we will."
Ben's words are quoted; everything else is Claude's work, not reviewed by a human.

## What this is

A pull request to openscriptures/morphhb, prepared on 2026-11-15 and not posted, that gives
`wlc/`'s 24 dual-cantillation verses (Genesis 35:22; Exodus 20:2–6, 8–10 and 13–15;
Deuteronomy 5:6–10, 12–15 and 17–19) one scheme. Every span, an atom with the maqaf, paseq or
sof pasuq after it, has a main version and up to three labelled alternates:

1. the main text, CLC's תחתון (at Genesis 35:22 CLC's מדרשית), meaning the division rules of
   MAM-basics' Charitable Leningrad Codex applied to WLC 4.20's text;
2. CLC's עליון (פשוטה) where it differs: `<note type="alternative" subType="x-elyon">`
   (`x-peshutah`);
3. a MAM-informed תחתון (מדרשית) where CLC's is not legal: `x-taxton-mam-informed`
   (`x-midrashit-mam-informed`);
4. a MAM-informed עליון (פשוטה) where CLC's is not legal: `x-elyon-mam-informed`.

Ben's request of 2026-11-15 at 13:12 New York time is quoted in full on the decision page and in
the brief that the archive holds (`inputs/`). The branch would start at Ben's fork's
`pashta-helpers`, `696e21ce`, the head of openscriptures/morphhb#118, and the pull request would
be merged after #118. No `MAPM/` change.

## What is tracked here

1. **This README.**
2. **`change.diff`**: the draft change to `wlc/Gen.xml`, `wlc/Exod.xml` and `wlc/Deut.xml`
   against `696e21ce`'s files. Applied with `git -c core.autocrlf=false apply change.diff` to a
   folder holding `wlc/` at `696e21ce`, it gives the draft byte for byte (checked on 2026-11-16;
   without that setting, Git for Windows writes CRLF line ends and the result differs).
3. **`work-folder.zip`**: the untracked work folder
   `.novc/morphhb-strands-pr-versions-2026-11-15/` of the clone `C:/Users/BenDe/GitRepos/MAM-basics`,
   as it stood on 2026-11-16 at 09:43 New York time, under that folder's name. It holds:
   - its scripts;
   - its research reports;
   - its data;
   - the decision page's sources and HTML;
   - the description and commit message to post;
   - the three base files;
   - under `inputs/`, copies of the folder's two inputs from outside it: folder S's
     `out/22-clc-answers.json` and `.md`, and the brief.

   Left out, as regenerable or refetchable:
   - the posting dry run's request bodies;
   - the built XML, which `change.diff` gives;
   - master's XML (openscriptures/morphhb at `db6c5c9b`);
   - sub-agent I's XML copies;
   - Python caches.

   Every entry was checked against its source after packing.

The description and the decision page stay inside the archive because they quote WLC 4.20's and
morphhb's forms in those texts' own mark order, which this repository's prose lint would read as
MAM-basics prose. The description's bare #118 and #116 are openscriptures/morphhb's, the
repository it was written for.

## The state when it was put on ice

- **Decision page:** https://claude.ai/artifact/7228EtGy2bVvT4bWWBLkFu (a private artifact),
  version 2. Its source is `out/decisions.html` in the archive. Its 14 decisions are all open,
  and the draft follows every recommendation:
  1. Genesis 35:22's main text is still the מדרשית (1A).
  2. A span is one atom with the punctuation after it (2A).
  3. "CLC's תחתון" means CLC's rules applied to WLC 4.20's text (3A).
  4. The עליון's version takes the qadma code point where WLC 4.20 writes the pashta's (4A).
  5. Four criteria of illegality, the accent grammar's among them (5A).
  6. A MAM-informed version takes MAM's accents, added or removed, and vowels, added or moved,
     and nothing else (6A).
  7. A `subType` labels each note (7A).
  8. There is one note per alternate (8A).
  9. A span's notes follow its punctuation seg when an alternate's punctuation differs (9A).
  10. A MAM-informed version is given even where it repeats another (10A).
  11. An illegal main-text atom is coded in `n` from its strand's tree (11A).
  12. Codes are relative to the chanted verse where the main strand changes (12A).
  13. The scheme is explained in the description only (13A).
  14. Post it? (not answered).
- **The draft:**
  - 148 notes: 135 for CLC's other strand, 13 MAM-informed;
  - 17 main-text atoms changed, in 16 verses, 8 of them changing strand;
  - `n` recomputed from MAM-basics' accent grammar at 26 atoms in 9 verses.
- **Checks:**
  - Every version, rebuilt from the XML alone, equals the intended one.
  - Nothing outside the 24 verses changes.
  - All 32 chanted verses are grammatical.
  - The apps' accent catalogs miss only at 4 atoms whose main text is not legal.
  - A dry run of the posting script passed.
- **Remote state, read at 15:09 New York time on 2026-11-15:**
  - morphhb's master was `db6c5c9b`.
  - openscriptures/morphhb#118 was open and mergeable at `696e21ce`.
  - The fork had no `decalogue-strands` branch.

## How to resume

1. Unzip `work-folder.zip` into `.novc/` at the root of a MAM-basics full clone.
2. Copy `inputs/folder-S/out/22-clc-answers.json` to
   `.novc/morphhb-strands-pr-2026-11-14/out/`, where `scripts/strands_core.py` reads it, unless
   that folder still exists there. `scripts/make_fragments.py` and `scripts/ice_pack.py` read the
   brief from the commander's shared notes folder; point them at `inputs/` instead.
3. Read the remote state again (`scripts/fetch_state.py` and `scripts/summarize_state.py`, each
   with a new round number). If #118 has been merged, closed or changed, or master has moved, the
   base changes: fetch it, and run the scripts on it.
4. Build, check and rebuild the page with `scripts/i_rebuild_all.py "<HH:MM>" "<state html>"`.
   The work folder's own `README.md` maps every file and gives the plan and Ben's requirements.
5. Ask Ben the open decisions on the page. Post only at his own "post it":
   `scripts/post_pr.py <work folder> <new bodies folder> --dry-run`, then `--post`.

## The meteg cases: noted, none supplied

Ben asked for these cases to be noted, since a meteg never makes a form legal or illegal. In the
עליון, MAM has a meteg where WLC 4.20 has none or has it elsewhere:

1. Exodus 20:4, atom 2: WLC 4.20 has the meteg on the tav, and MAM's עליון has it on the shin.
2. Deuteronomy 5:7, atom 2: MAM's עליון has a meteg that WLC 4.20 lacks.
3. Deuteronomy 5:8, atom 2: likewise.

**What MAM's documentation says about them.** This is attributed to MAM's notes; no
manuscript image was consulted. The archive's `out/51-mam-documentation.md` has the details.

- **Exodus 20:4, atom 2.** MAM's note gives the meteg on the shin as the reading of ל1, ל-מ, ש,
  ש1, ק3 and the printed editions. It says the Leningrad Codex has the meteg on the tav, and
  that Breuer corrected it according to ל-מ.
- **Deuteronomy 5:7, atom 2.** MAM explains this meteg in its note on Exodus 20:3. There Dotan
  and Breuer take the Leningrad Codex's single stroke as both the תחתון's merkha and the עליון's
  meteg.
- **Deuteronomy 5:8, atom 2.** MAM's note says the Leningrad Codex has the meteg and lacks only
  the qadma. WLC 4.20 has a merkha there.

## Other findings

- **Exodus 20:5's ḥataf pataḥ.** It is morphhb's only change, anywhere in `wlc/`, to the point
  under a ḥet. It came with `73784451` (2010-07-13), in the same edit that divided that word's
  two accents.
  - WLC 4.20 has the sheva under this verb's ḥet nowhere else.
  - WLC 4.20 has the same kind of sheva in other words, at Exodus 27:15 and Ezekiel 35:15, and
    morphhb keeps those.
  - Every version in the draft has WLC 4.20's sheva.
- **CLC's notes and illegality.**
  - CLC's rules, applied to WLC 4.20, note 8 missing marks. The 6 accents and vowels among them
    each mark an illegal version, and the 2 metegs mark none.
  - 7 of the 13 illegal versions have no note.
- **`n`.** The codes are read off the trees of MAM's strands. Read the same way, they equal
  morphhb's hand-made codes at 50,831 of 50,853 atoms in Genesis, Exodus and Deuteronomy.
