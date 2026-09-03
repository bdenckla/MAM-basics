# Scan-pages index: bring up five scanned editions at a bcv — plan

Ben's ask, 2026-08-06: *"index important editions I have scanned (in 'ScansOfBooks') so
that, given a bcv (book-chapter-verse) reference, I can run a program that will bring up the
relevant page in all those editions (JC1 (Jerusalem crown), Koren, Simanim Tiqqun (if the
bcv is in Torah or haftarah), Simanim Tanakh, Dotan BHL)."*

This file is the single plan-and-findings document for the undertaking (per Ben's
one-tracked-plan rule). Findings replace plan text here as phases complete. It is written
for a fresh session that has no other context.

## Status

- 2026-08-06, session 1 (Ben + Claude): scan folders surveyed (findings below); plan
  written. No phase has run; no code exists yet.
- 2026-08-07, session 1 continued: two design corrections from Ben. Versification: a page
  does not absorb an off-by-one numbering difference (first fixed as a ±1-page display
  floor, `e136ba8`). Then the deeper one: **no page error is acceptable, estimates
  included** — so the containment-anchor-plus-interpolation design, and that ±1 floor
  with it, were replaced by the exact page-record model of `codex-index-leningrad`. Also
  settled by Ben the same day: the Simanim Tiqqun's unpointed D section stays out of
  lookup ("don't worry about unpointed").
- 2026-08-07, session 2 (a worktree): **Phase 0 ran and is done** — findings below, in
  place of what that phase's plan text said. The `survey` and `check` subcommands, the
  `py/scan_pages/` library and the pytest lint exist; all 5,720 files are classified and
  the five indexes are tracked. Three of Phase 0's claims were refuted by measuring
  them, one of them by Ben mid-session; each correction is recorded where the claim was.
- 2026-08-07, still session 1, three more decisions from Ben: the Decalogues get
  strand-aware lookup (a bare bcv → the body Decalogue, whichever strand the edition's
  body has; a `t`/`e` suffix names the strand wanted); lookup is by phrase-qualified or
  phrase-unqualified verse (both in Decisions below); and "phrase" is used in its broad
  sense throughout this undertaking — a run of one or more consecutive atoms, so a lone
  chanted word or even a lone atom counts.

## Decisions (proposed 2026-08-06 by the planning session unless attributed to Ben; Ben can veto the proposals)

- **Home repo: MAM-basics** (`C:/Users/BenDe/GitRepos/MAM-basics`, venv at
  `.venv/Scripts/python.exe`). All of Ben's Python lives here now and new issues are filed
  here. The scans themselves stay where they are and no image enters the repo; the repo
  tracks only index *metadata* (filenames, page-boundary records) — uncopyrightable
  facts, fine in a public repo.
- **One name token everywhere: `scan_pages` / `scan-pages`.** Entry point
  `py/main_scan_pages.py` with subcommands (`survey`, `lookup`, `census`, `check`); library
  code under `py/scan_pages/`; tracked index data under `in/scan-pages/`; this doc
  `doc/scan-pages.md`.
- **Lookup input: bk39 id, chapter:verse, an optional strand suffix, an optional
  phrase** — `lookup Genesis 12:3`, `lookup Exodus 20:3e תעשה`. The bk39 ids are the
  ones `py/mb_cmn/bib_locales.py` documents ("A pithy example of a valid value for
  book39 is 1Samuel"); nothing fancier — per Ben's standing "CLI ergonomics aren't worth
  it," the program has essentially one user and he can type the canonical id. Two rules
  of Ben's, 2026-08-07. **Phrase**, here and everywhere in this undertaking, has its
  broad sense: a run of one or more consecutive atoms, so a lone chanted word or even a
  lone atom counts. And lookup is either by **phrase-qualified verse** — an error if the
  phrase does not pin a unique spot within that verse — or by **phrase-unqualified
  verse**, in which case the first unique phrase of the verse is substituted silently.
  Either way lookup resolves to an atom position and returns the page whose record
  covers that atom, so a phrase deep in a page-straddling verse brings up the later
  page.
- **Verse text and counts come from the MAM-parsed sibling at runtime** (via
  `mb_cmn/read_books_from_mam_parsed_plus.py`), not from a second tracked copy — no
  duplicated artifact to drift. Versification: MAM's, and only MAM's. A page record is
  made by locating each page-edge phrase in MAM's text (the record shape below), so an
  edition's printed verse numbers never enter the data, and the scattered loci where an
  edition's numbering differs from MAM's by a verse or two cannot produce a wrong
  record. (An earlier version of this bullet claimed a page absorbs an off-by-one
  numbering difference; Ben refuted that on 2026-08-07 — a verse at a page edge spills to the
  neighboring page when the numberings disagree about it. The first fix, a ±1-page
  display floor, treated a page error as acceptable, which Ben also refused. The exact
  record model replaced both.)
- **Ben's decision, 2026-08-07: no page error is ever acceptable, so the data model is
  the one that makes a page error inexpressible — codex-index-leningrad's.** In
  `C:/Users/BenDe/GitRepos/codex-index-leningrad/UXLC-utils-sparse/data/lci_recs.json`,
  every page has a record of where it starts and where it stops, down to the atom
  within the verse (`bkid`, `startc`, `startv`, `startp`, `stopc`, `stopv`, `stopp` —
  bkids in the `mb_cmn/bib_locales.py` convention, e.g. `Levit`), and consecutive pages
  meet at adjacent atoms, so complete records are a contiguous partition of the text into
  pages. Any bcv then maps to its page — and to both pages, when its atoms genuinely
  split across two records — with no estimate anywhere. The data can still be wrong; the
  model cannot hide it, because a gap, an overlap, or a skipped page is a lint failure
  (below). Page level only: the line/column fields those Leningrad records have as nulls
  — and the line-level depth the Aleppo repo's Job data goes to — are deliberately out of
  scope here, at least for now.
- **Lookup is exact or it refuses.** Within a censused range (a book, or a segment such
  as one haftarah, whose every body page has its record), lookup returns the page the
  bcv starts on, plus the next page when the records show the verse continuing onto it. Outside a
  censused range it says so and names what is censused — it never guesses. No
  interpolation, no uncertainty window, nothing labeled "estimate": Ben, 2026-08-07,
  twice — a page error is not acceptable.
- **The Decalogues are strand-aware (Ben, 2026-08-07).** A bare bcv in either Decalogue
  brings up the **body** Decalogue — and whether an edition's body has the תחתון
  (taxton) or the עליון (elyon) there is an edition fact, established by reading the
  page during its census and recorded in its JSON. On top of that, a **bcvs** syntax —
  the bcv plus a strand letter, `Exodus 20:3t` / `Exodus 20:3e` — asks for the named
  strand: the body page when the body strand matches, the page of a separate Decalogue
  section (an appendix segment, tagged with its strand) when the edition has one, and an
  honest "this edition has no separate <strand> Decalogue" when it has none. A
  strand-suffixed phrase is located in that strand's text as MAM-parsed has it, so the
  strands' differing verse divisions never enter the records. bhl's `Appendix` ×5 and
  koren's `V` ×55 are natural places for a second strand's Decalogue to surface; Phase
  0's classification should look.
- **Records are captured from page-edge phrases, located in MAM's text.** The Leningrad
  records were derived from an existing index (tanach.us' LCIndex); no such index exists
  for these five printed editions, so each record here gets read off the scan: the
  phrase at each edge of the page — its first and its last few atoms — stored as
  `start_phrase` / `stop_phrase` evidence. **Phrases are stored letters-only** (no
  vowels, no accents): a phrase read off a scan is typed by the model reading it, and
  model transcription of pointed Hebrew silently reorders marks (proven in the Metsudah
  comparison, `doc/metsudah-vs-ctr.md` — all 39 chapter hashes mismatched — and warned
  about in this repo's `CLAUDE.md` mark-order section), while letters survive
  transcription. Letters-only also makes locating a phrase in MAM-parsed text a plain
  search over accent-and-vowel-stripped text. The `census` tooling locates each phrase in MAM-parsed text and derives the
  atom numbers from it — no hand-counting of atoms, no reading of printed verse numbers —
  and demands a longer phrase whenever the current one fails to pin a unique position in
  the candidate neighborhood (Ben's "verse-unique phrase" requirement). The stored phrase
  keeps every record independently re-verifiable, against the image and against the
  text, forever after.
- **The bring-up is one generated HTML page, opened by the program.** Written under
  `.novc/scan-pages/` (gitignored), one section per edition: the page image(s) the
  records give, inline via `file:///` URLs into the scans folder (`loading="lazy"` —
  these JPGs run 1–18 MB), prev/next links, and the record behind the answer, phrases
  included. Default behavior when *Ben*
  runs it: open via `os.startfile`, because "bring up" is the ask. A Claude session runs
  it with `--no-open` and hands Ben the `file:///` link, per the global
  don't-launch rule.
- **The program is cwd-independent.** Scans root and repo paths are anchored in code
  (`Path.home() / "OneDrive" / "Documents" / "ScansOfBooks"`; `mb_cmn/paths.py` for
  siblings), never cwd-relative, so it runs from anywhere. UTF-8 stdio reconfigure first
  thing in `main()`, per the global rules — though real output goes to the HTML file, and
  stdout gets only short ASCII progress.
- **Edition ids** (used in filenames, JSON, and the CLI):

  | id | folder under ScansOfBooks | files |
  | --- | --- | --- |
  | `jc1` | `JC1 Jerusalem Crown` | 927 |
  | `koren` | `Koren Classic Tanakh` | 1332 |
  | `simanim-tanakh` | `Feldheim Simanim Tanakh` | 1552 |
  | `simanim-tiqqun` | `Feldheim Simanim Tiqqun` | 614 |
  | `bhl` | `Biblia Hebraica Leningradensia` | 1295 |

## Survey findings (measured 2026-08-06 against the live OneDrive folder)

Scans root: `C:/Users/BenDe/OneDrive/Documents/ScansOfBooks`. The file counts above and
every claim below were read from the folder on 2026-08-06 with ad hoc PowerShell not worth
preserving; Phase 0's `survey` subcommand is the re-derivation command for all of them, and
a mismatch when it runs is a finding, not an error in this doc. Caveat: the folder is under
OneDrive, so files can be cloud-only placeholders; `survey` should fail loudly on a
zero-availability file rather than index it silently.

**Four editions share one book-code family in their filenames** (Koren-style: Torah
`G E L N D`; Former Prophets `Js Ju 1S 2S 1K 2K`; Latter Prophets `I Je Ee` + twelve
`Ho Jl A O Jn Mi Na Hb Ts Hg Zc Ma`; Writings `Ps Pr Jb S R La Ec Es Da Er Ne 1C 2C`).

**Phase 0 found that family is this repo's, exactly, so no table was written for it.** A
book token is `bib_locales.short(bk39id)` and a koren-family section token is
`bib_locales.ordered_short(bk39id)`, both verbatim; `py/scan_pages/book_codes.py` inverts
those two functions instead of restating them, and so cannot drift from the convention the
rest of the repo uses. It also means a koren-family body filename names its book twice,
once per code, and the parser rejects any filename where the two disagree. Only bhl needed
tables written by hand, for its longforms.

The body-page filename shapes:

- **jc1**: `NNN-<bk>.jpg` (e.g. `220-Js.jpg`) — NNN is the scan sequence and likely the
  printed page number; front matter `#NN-<desc>.jpg`; end matter `NNN-NN-<desc>.jpg`;
  service tokens `blank`, `ToC` appear as the `<bk>` slot.
- **koren**: `<sec><n>-<bk>-NNN.jpg` for big books with per-book numbering restarting at
  001 (`A1-G-001.jpg`), but `<secletter><sub>-<bk>-NNN.jpg` with *continuous* printed page
  numbers for the books scanned later (`BA-1S-087.jpg` … `CL-Ma-589.jpg`,
  `FA-Er-229.jpg` … `FD-2C-374.jpg`). Sections: A Torah, B Former Prophets, C Latter
  Prophets, D Ps/Pr/Jb, E Megillot, F Da/Er/Ne/Chronicles, then `V` ×55, `W`,
  `X-back-cover`, `Y` spine. **`V` is Koren's back matter**, 58 separately numbered pages
  whose printed contents page is `V-001.jpg` (read 2026-08-07): 3 ספר התנ״ך שבהוצאת קורן,
  9 דברי ברכה, 13 חילופי נוסחאות, 17 and 33 the Hebrew renderings of the Aramaic in Daniel
  and in Ezra, 38 עשרת הדיברות בטעם העליון, 40–42 the Torah readings, 46 ברכות ההפטרה,
  47 סדר ההפטרות, 58 שמות הטעמים. In `V` the scan number equals the printed page number,
  which `V-030.jpg` confirms: it has printed page 30, inside the Daniel rendering the
  contents page places at 17–33. Only printed 38 and 39 hold biblical text, and both were
  read: they are the Decalogue in the עליון, `V-038.jpg` headed
  עשרת הדיברות שבפרשת יתרו and `V-039.jpg` עשרת הדיברות שבפרשת ואתחנן. `W-001.jpg` is the
  edition's colophon. Printed-number gaps exist (e.g. `BC-1K-187` then `BC-1K-189`); see
  the divider-leaf finding below, which is what most of them are.
- **simanim-tanakh**: `<sec>-<bk>-NNNN.jpg` (`B1-Js-0360.jpg`, `D2-Pr-1150.jpg`); front
  matter in **three** separately numbered runs, `1-*`, `2-*` (including `2-03-ToC.jpg`) and
  `3-*`. The `3-` run was missed by the 2026-08-06 tally and by Phase 0's first pass at the
  filename shapes, and `survey` refusing to classify it is how it surfaced — the two files
  are the Torah divider, `3-1.jpg` the title page תורה and `3-2.jpg` its contents page.
  The `A9-*` singletons are **an עליון Decalogue appendix**: `A9-0349.jpg` is its section
  title page, reading עשרת הדברות בטעם עליון, and `10C` in `A9-A2-10C-0350.jpg` and
  `A9-A5-10C-0351.jpg` is the Ten Commandments, qualified by the section code of the book
  each is drawn from. `V` ×83 is the מאורעות התנ״ך supplement, כולל סדר ההפטרות — apparatus,
  not biblical text, so out of lookup (`V-1463.jpg` its title page, `V-1500.jpg` a topical
  index under the running head נושאי המאורעות בכתובים). `W-1552.jpg`, the last numbered
  leaf, has the publisher's back-cover artwork over וְעַתָּה כִּתְבוּ לָכֶם אֶת־הַשִּׁירָה הַזֹּאת, with the
  scanned back cover proper filed separately as `X-back-cover.jpg`.
- **bhl**: `NNNN-<bk>.jpg` with continuous scan numbering (`0296-D.jpg`,
  `0620-Isaiah.jpg`) — but the book token is *mixed-convention*: mostly the short family
  (`G`, `Js`, `Ps`) with longform outliers (`Isaiah` ×62, `Ruth` ×5, `Song` ×5, and
  singleton `Deut`/`Exod` section-title pages), plus service tokens `blank` ×40, `title`
  ×27, `Appendix` ×5, `ToC` (in `#08-v-ToC.jpg`-style front matter), `back-cover`,
  `spine`. The book-code table in `py/scan_pages/` gets the longforms as extra rows.
  bhl's five `Appendix` files are the appendices' title pages (A Manuscript Variants,
  B Petuhot and Setumot, C The Shape of the Songs, D Deviation in Gemination, E Scripture
  Readings), and its 28 bare-numbered `NNNN.jpg` files are their continuation pages. Its
  second-strand Decalogue is not there but named outright: `1227-Exod-Decalogue-Upper.jpg`
  and `1228-Deut-Decalogue-Upper.jpg`.

**A filename number is a PRINTED page number, in every edition — and a book's first file is
usually not its first page of text.** Ben established the first half on 2026-08-07, against
a Phase 0 claim that simanim-tanakh's numbers counted scans: he had worked to name the files
by printed page, and the apparent 2-page discrepancy that prompted the claim had another
cause entirely. `BB-2S-0505.jpg` settles it directly — the page has `505` printed at its
foot. What the discrepancy really shows is the second half: **each book opens with a divider
leaf, named with the book's codes and so indistinguishable by name from a page of its text.**
simanim-tanakh's `A2-E-0085.jpg` is the Torah contents with שמות 87 picked out, koren's
`A2-E-081.jpg` is a bare שמות, and simanim-tanakh's Torah contents page independently gives
שמות as starting at printed 87 — so the text of Exodus begins at `A2-E-0087.jpg`, two leaves
after the book's first file. This matters because the plan assumed a book's first body page
came free from the filename codes; it does not.

**The divider leaves are found from the listing, and the pass is built to miss rather than
invent.** A divider's blank verso was generally not scanned, so a missing number straight
after a book's first file betrays it; that signal caught 21 of them in koren and 22 in
simanim-tanakh, and every case checked against an image was indeed a divider. It has false
negatives, though — simanim-tanakh gives the כתובים section its divider under Psalms' codes
as `D1-Ps-0993.jpg`, whose verso *was* scanned, so nothing in the listing marks it and only
reading it did (Psalms' text begins at `D1-Ps-0994.jpg`). The pass is therefore deliberately
one-sided: a miss costs a seeded record one leaf early, which the census corrects, whereas a
false positive would move a book's start off a page that really does hold text. `survey`
reports every book whose divider it did not find — 18 in koren, 17 in simanim-tanakh, mostly
the books that continue a book24 and genuinely have none — so the census reads those first.

**A koren-family book's first text page generally also holds the end of the previous book,
and the filename does not say so.** `BB-2S-0505.jpg` is named for 2Samuel and has the whole
of 1Samuel 31 before 2Samuel 1 begins near its foot. jc1 and bhl name both books in such a
case (`544-A-O.jpg`, `0825-A-O.jpg`) and the parser reads both; the koren family names only
the later one. So a `bkids` list from a koren-family filename is the book that *starts*
there, not the complete contents, and the census puts two records on such a page.

**simanim-tiqqun is the special one.** Five filename sections, meanings established by
reading sample pages (`B10.jpg`, `B60.jpg`, `C012.jpg`, `C400.jpg`, `D10.jpg`,
`E10-06.jpg` on 2026-08-06; `C300.jpg`, `C395.jpg`, `C408.jpg`, `C415.jpg`, `C420.jpg`,
`C440.jpg` on 2026-08-07):

- `A01`–`A04`: covers/endpapers.
- `B01`–`B74`: separately page-numbered front matter — introductory essays and
  the per-parasha simanim apparatus (`B60.jpg` is apparatus page 60, פרשת משפטים).
- `C001`–`C444`: the main body. **Scan number = printed page number** (`C012.jpg` is
  printed page 12). The running head has book · chapter range · parasha (e.g.
  `בראשית · יא יב · לך לך`), and the text appears twice per page (pointed and unpointed
  columns). The C range holds more than Torah, and both further contents are observed,
  not presumed. **Haftarot**: `C300.jpg`'s running head is הפטרת בהר; the top of the page
  is the end of the previous haftarah (Ezekiel 44, haftarat Emor), and mid-page the
  heading הפטרת בהר with the source line בירמיה פרק לב introduces Jeremiah 32 — the same
  pointed-and-unpointed dual layout as the Torah pages. So the haftarot are in C, in
  parasha order, each under a heading naming it and its source book and chapter (a gift
  to the census). **Megillot — three of the five, not all.** Ben suspected on 2026-08-07
  that far from all of the Five Scrolls would be here, and the reads confirm it: a
  מגילות section in festival-calendar order — `C395.jpg` is מגילת שיר השירים, `C400.jpg`
  is מגילת רות chapter 3, `C408.jpg` is מגילת איכה chapters 4–5, all three in the same
  dual layout as the Torah pages: one column with full pointing and accents, the facing
  column unpointed (Ben asked on 2026-08-07; unpointed megillot would have been useless
  here) — and then the full text stops. Ecclesiastes and Esther have no full text anywhere in C. (The other half of the
  suspicion, Ruth as a haftarah-like reading, is not what the book does: Ruth sits under
  the מגילות running head, not among the haftarot.) **The tail, ~C410–C444, is a notes
  apparatus, not full text**: masorah/diqduq notes per parasha (`C415.jpg` is ספר
  בראשית notes, `C420.jpg` is ספר שמות notes), and by `C440.jpg` the running head is חמש
  מגילות, with Esther's notes ending and notes on שיר השירים beginning mid-page — so the
  notes treat all five megillot though only three have their full text. The notes tail is
  out of lookup, like B and E.
  Exact segment boundaries inside C are still unknown; finding them is Phase 3, and the
  cheap route is the printed ToC (in B or A), since C scan numbers equal printed numbers —
  a ToC page read gives the whole haftarah/megillot map in a handful of image reads.
- `D01`–`D60`: a compact, *unpointed-only* Torah, scanned rotated 90° (`D10.jpg` is
  Devarim). Out of lookup — Ben, 2026-08-07: "don't worry about unpointed."
- `E01`–`E32` (`E05-01.jpg`-style dual numbering): a color promotional/method booklet.
  Excluded from lookup.

**Not covered by masoretica.org** — that site maps verses to *manuscript* pages (187
manuscripts); none of these five printed editions is there, so there is no shortcut around
building this index.

## Design

Tracked index, one JSON per edition at `in/scan-pages/<edition-id>.json`:

```json
{
  "edition": "jc1",
  "folder": "JC1 Jerusalem Crown",
  "pages": [
    {"file": "#01-front-cover.jpg", "kind": "cover"},
    {"file": "220-Js.jpg", "kind": "body", "bkids": ["Joshua"]},
    {"file": "876-02-Exod-Decalogue.jpg", "kind": "decalogue",
     "bkids": ["Exodus"], "strands": ["taxton", "elyon"],
     "note": "both strands, side by side on the one page"}
  ],
  "segments": [],
  "recs": [
    {"page": "013-G.jpg",
     "bkid": "Genesis", "startc": 1, "startv": 1, "startp": 1,
     "stopc": 1, "stopv": 31, "stopp": 12,
     "start_phrase": null, "stop_phrase": "...", "note": null}
  ]
}
```

- `pages` is the complete sorted listing (front and back matter included, classified), so
  the index is meaningful — and lintable — on a clone with no scans folder at all. Phase 0
  made each entry an object rather than the bare filename this sample first drew, because
  the classification has to live somewhere and not all of it is derivable from a filename:
  koren's `V-038.jpg` is a Decalogue page and nothing in that name says so. Storing it does
  not create a drift risk — `check` re-derives every classification from the listing and
  compares, which makes the stored copy a differential check rather than a second truth.
  The kinds are defined in `py/scan_pages/page_kinds.py`, and exactly two of them,
  `body` and `decalogue`, hold text a lookup may return.
- `recs` reuse `lci_recs.json`'s column dictionary at page level (its line/column fields
  simply don't exist here), plus the two phrase-evidence fields. Recording *both* ends of
  every page is deliberate redundancy: each record is verifiable against its own page
  image alone, and the contiguity lint then cross-checks every adjacent pair.
- `survey` seeds each book's first body page with its start half — `startc/startv/startp`
  of 1:1 atom 1, `start_phrase` null because no page was read for it. The census fills
  everything else. That "comes free from the filename book codes" as first written, but
  only after the divider-leaf pass above; the null `start_phrase` is what marks a seed as
  unread, and for the 35 books whose divider was not found it is doing real work.
- **All four full-Tanakh editions have a separate עליון Decalogue, and jc1's page has both
  strands on it.** The inventory, all read on 2026-08-07: jc1's supplements have
  `876-02-Exod-Decalogue.jpg` and `877-03-Deut-Decalogue.jpg`, each printing the two
  strands side by side, the right column headed בטעם התחתון and with verse numbers, the
  left בטעם העליון and without; koren's `V-038.jpg` and `V-039.jpg` have the עליון alone;
  simanim-tanakh's `A9-A2-10C-0350.jpg` and `A9-A5-10C-0351.jpg` sit under a section title
  page reading עשרת הדברות בטעם עליון; bhl's `1227-Exod-Decalogue-Upper.jpg` and
  `1228-Deut-Decalogue-Upper.jpg` are headed "The Decalogue with Upper Cantillation
  (טעם עליון)", the Exodus one naming its range as 20:2–13. **So a page can belong to two
  strand-tagged segments at once**, and the tiling lint below exempts strand-tagged
  segments from disjointness for exactly that reason. Which strand each edition's *body*
  Decalogue has is still an open edition fact, established during its census.
- Every edition's JSON has a `segments` list: maximal runs of body pages over which the
  text advances contiguously. A full-Tanakh edition's whole body is one segment; a
  separate Decalogue section is a small strand-tagged segment; in simanim-tiqqun the
  Torah, each haftarah and each megillah are segments (consecutive haftarot are not
  textually contiguous, so contiguity holds within a haftarah, never across two). The
  simanim-tiqqun JSON additionally has the haftarah table: per haftarah, the name and
  bcv range the book has for it — whatever rites the book has, not a liturgical
  calendar's computation — and its C-page range. A haftarah bcv can hit several
  haftarot; `lookup` returns every hit.

**Lint, not example tests.** `check` (also run as a pytest lint, one new file
`py/tests/test_scan_pages_index.py`) verifies over the tracked JSONs:

- every rec's page is in `pages`, is of a kind a rec may sit on, and names a book that
  page holds; every position parses against MAM verse counts (FAIL, never skip, when
  MAM-parsed is absent — per the repo's missing-input rule);
- every stored classification is re-derived from the listing and compared — a differential
  check of all 5,720 pages against an independent derivation of the same fact, and the one
  lint that already does full-scale work at Phase 0;
- within a segment, recs in page order have strictly advancing text positions and
  consecutive recs meet at adjacent atoms in text order — no gap, no overlap, no page
  silently skipped — and segments' page ranges tile the classified body pages without
  overlap, **except that strand-tagged segments may share pages**, since jc1 prints the
  תחתון and the עליון on one sheet;
- each stored phrase, re-located in MAM-parsed text, lands exactly at its rec's recorded
  atoms — a differential check of every record against an independent derivation;
- atoms-per-page stays within a sane band, flagging the outliers a misread produces.

The last two arrive with Phase 1: both need the phrase locator and the atom splitter that
the census builds, and neither has data to run on until stop halves exist. Phase 0 built
the rest, and `check` prints how much it verified so a green run that checked nothing would
be visible.

The model cannot express a page error; these lints are what catch wrong *data*. A
boundary placed at the wrong atom has to lie about two adjacent pages consistently to
survive contiguity, and fool the phrase re-location besides. This is the mechanical-lint
shape Ben's test rules allow; no example-based unit tests.

**The cost of exactness is a census, and it is bounded.** Every body page's edges get
read once: ~900–1500 pages per edition, ~5100 in all. That is the price of "a page error
is not possible at the data-model level," paid once per edition, in book-sized chunks
with lints, a chat report and a commit after each chunk (Ben's standing
work-in-responsive-chunks rule). A censused book is exact immediately; everything else
keeps refusing rather than guessing, so partial progress is always safe to use.

## Preconditions for the executing session

- Repos: `C:/Users/BenDe/GitRepos/MAM-basics` (venv at `.venv/Scripts/python.exe`);
  sibling `C:/Users/BenDe/GitRepos/MAM-parsed` present (verse counts). Scans at
  `C:/Users/BenDe/OneDrive/Documents/ScansOfBooks` with the five folders named above.
- Worktree-isolable (Ben asked 2026-08-07). Every tracked write is in MAM-basics, so a
  worktree isolates the undertaking fully; the spill is read-only. The scans path is
  absolute and checkout-independent. The MAM-parsed sibling must be named explicitly
  from a worktree — `REPOS_ROOT=C:/Users/BenDe/GitRepos` (or `REPO_MAM_PARSED_DIR`) —
  because the default `repo_root().parent` lands in `.claude/worktrees/`;
  `mb_cmn/paths.py` documents the chain, and its `require_sibling` fails loudly naming
  both overrides when the sibling is absent. All new sibling-path construction goes
  through `mb_cmn.paths.sibling_repo` + `require_sibling`, never a `../MAM-parsed`
  literal. A worktree runs the primary clone's venv by absolute path, per the global
  rules.
- Baseline: **915 passed, 5 skipped**, measured 2026-08-07 at `fc23077` from the repo root
  of the primary clone. The 320 this bullet used to cite, from `doc/metsudah-vs-ctr.md`, is
  stale by a wide margin — that figure predates the accgram and CLC code arriving on
  2026-08-01 — so treat the count here as the baseline and `doc/metsudah-vs-ctr.md`'s as
  a historical note. Phase 0 took it to **919**: two tests in the new lint file, and two
  more because `test_entry_point_subcommands.py` parametrizes over the entry points and
  there is now one more.
- **A worktree now runs the suite green, as of 2026-08-07 — same 919 passed, 5 skipped,
  with `REPOS_ROOT=C:/Users/BenDe/GitRepos` set.** Until that day it could not, and this
  bullet said so and told a future session to expect the failures. Two separate defects
  caused them, neither anything to do with scan-pages, and both were measured before Phase 0
  wrote a line:
  - `py/mb_cmn/read_books_from_mam_parsed_plus.py` is on the repo `CLAUDE.md`'s
    vendored-file exception list, so its cwd-relative `"../MAM-parsed"` default — which
    neither `REPOS_ROOT` nor `REPO_MAM_PARSED_DIR` reaches — had to stay. The seventeen call
    sites that had been taking that default now pass `mb_cmn.paths.mam_parsed_path()`
    instead, which is the same thing `py/scan_pages/check.py` already did.
  - `py/mb_cmn/provenance.py` built its generated-by breadcrumb from the checkout
    directory's name, which in a worktree is the worktree's, so
    `MAM-simple/doc/versification-differences.md` regenerated as "generated by
    busy-chebyshev-613a3b/py/..." and its differential test failed. `this_repo_name()` now
    resolves the main clone through the worktree's `.git` file.

  So a worktree suite is trustworthy, and an unexplained failure in one is a finding rather
  than the known background noise it used to be. Running the full suite in the primary clone
  after merging is still worth doing, but no longer the only way to see a real result.
- Tracked files this undertaking may touch: this doc, `py/main_scan_pages.py`,
  `py/scan_pages/*`, `in/scan-pages/*`, `py/tests/test_scan_pages_index.py`. **Nothing
  else is expected to change** — no MAM data, no generated artifacts, no sibling repos; an
  unexpected diff elsewhere is a finding.
- No `sys.path` surgery (the entry point in `py/` gives `scan_pages.*` imports for free);
  black on every touched `.py`; commit and push per the global rules; load the
  `hebrew-prose` skill before writing findings prose into this doc (parasha names,
  megillot, "the Simanim Tiqqun" never a bare "Simanim").
- Image reads: the executing session verifies scan-page claims by `Read` on the JPG —
  never by launching a viewer.

## Phases (each ends with a chat report and a commit; pause for Ben where marked)

**Phase 0 — survey and tracked inventory. DONE, 2026-08-07.** The code is
`py/main_scan_pages.py` (`survey`, `check`) over `py/scan_pages/`, with the lint at
`py/tests/test_scan_pages_index.py`. Re-derive everything below with:

```
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_scan_pages.py survey
```

All **5,720** files classify, and the per-edition file counts match the ones this doc
recorded on 2026-08-06 exactly. Pages by kind, and the seeded records:

| edition | files | body | text out of lookup | seeded recs |
| --- | --- | --- | --- | --- |
| `jc1` | 927 | 861 | — | 39 |
| `koren` | 1332 | 1240 | — | 39 |
| `simanim-tanakh` | 1552 | 1401 | — | 39 |
| `simanim-tiqqun` | 614 | 0 | 444 unassigned, 60 unpointed | 0 |
| `bhl` | 1295 | 1162 | — | 39 |

Each of the four full-Tanakh editions has all 39 books present with body pages, and 39
seeded records on 39 distinct pages — the outcome the plan predicted. The rest of each
edition is front and back matter, covers, blanks, title pages and, in simanim-tiqqun,
apparatus; the full breakdown is in the survey's output and in the tracked JSONs.
simanim-tiqqun's 444 C pages are classified `body-unassigned`, awaiting Phase 3 to say
which is Torah, which a haftarah and which one of the three full-text megillot.

`check` re-classifies all 5,720 pages and validates all 156 records against MAM-parsed:

```
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_scan_pages.py check
```

**What Phase 0 got wrong, and how.** Three claims failed when measured, which is the point
of measuring: the plan's book-code table turned out to be this repo's two functions
(above); simanim-tanakh's filename numbers are printed page numbers after all, Ben's
correction, and chasing why they had looked otherwise is what found the divider leaves; and
the first pass at the filename shapes missed simanim-tanakh's `3-*` run entirely — `survey`
refusing to classify those two files is the only reason they were not silently dropped,
which is the whole argument for making it refuse.

**Anomalies worth carrying forward.** Obadiah has a single body page in koren
(`CD-O-553.jpg`) and in simanim-tanakh (`CD-O-0952.jpg`), and none to itself in jc1 or bhl,
where it shares `544-A-O.jpg`/`545-O-Jn.jpg` and `0825-A-O.jpg`/`0826-O-Jn.jpg` — correct,
being 21 verses, but it makes Obadiah the sharpest test of the record model and a good
first census subject. And 18 books in koren and 17 in simanim-tanakh have no divider leaf
found, so their opening page is recorded as text unconfirmed; `survey` lists them by name
and the census reads those first.

**Phase 0 read 17 page images**, all with the `Read` tool and no viewer, to settle what
filenames do not say, and every one of them is cited at the finding it settles above and in
the tables that encode it in `py/scan_pages/classify.py`. In edition order: jc1
`876-02-Exod-Decalogue.jpg`; koren `V-001.jpg`, `V-030.jpg`, `V-038.jpg`, `V-039.jpg`,
`W-001.jpg`, `A2-E-081.jpg`; simanim-tanakh `3-1.jpg`, `3-2.jpg`, `A9-0349.jpg`,
`A2-E-0085.jpg`, `BB-2S-0505.jpg`, `D1-Ps-0993.jpg`, `V-1463.jpg`, `V-1500.jpg`,
`W-1552.jpg`; bhl `1227-Exod-Decalogue-Upper.jpg`. The list is here so a later phase can
see at a glance what has been looked at and what has only been inferred.

**Phase 1 — tooling, proven on one small book.** Implement
`lookup <bk39> <ch>:<v>[t|e] [<phrase>]` (exact-or-refuse) → HTML bring-up, and `census` (page-edge phrases in, atoms out,
contiguity checked against the previous record as each new one lands). Then census one
small book end to end in one edition and verify: `check` clean, and
spot-read several lookups against the page images, straddling verses included, confirming
the verse is really on the returned page(s). Record the spot results here. **Pause for
Ben:** he tries it and confirms the record shape before ~5100 pages get read into it.

Three things Phase 0 established that bear on how Phase 1 starts:

- **Census Obadiah, not Ruth.** Phase 0 wrote "Ruth in jc1, say" before knowing the shape of
  the data. Obadiah is the better first subject because it exercises every hard case at
  minimum cost: one body page in koren (`CD-O-553.jpg`) and in simanim-tanakh
  (`CD-O-0952.jpg`), and in jc1 and bhl no page to itself at all — it starts mid-page on
  `544-A-O.jpg` / `0825-A-O.jpg` and ends mid-page on `545-O-Jn.jpg` / `0826-O-Jn.jpg`. So it
  forces two records on one page, and a book whose every page is shared, before any of it is
  built at scale. Ruth in jc1 is four clean pages and would prove much less.
- **Verify a book's opening page before recording it.** A koren-family book opens with a
  divider leaf indistinguishable by filename from its text, and `survey` names the 18 books in
  koren and 17 in simanim-tanakh whose divider it could not find. Those seeded start records
  are the ones most likely to be a leaf early, and reading the page is what settles it.
- **A koren-family page can hold two books without saying so.** `BB-2S-0505.jpg` is named for
  2Samuel and has the whole of 1Samuel 31 first. So `census` must not assume the page's
  `bkids` is its complete contents, and the contiguity lint must tolerate two records on one
  page — which `check` already does, keying records by book rather than by page.

**Phase 2 — the censuses, edition by edition.** For each of jc1, bhl, koren,
simanim-tanakh: read every body page's edges, one book-sized chunk at a time — lints, a
chat report and a commit per chunk. Edition order is Ben's call (open question below).

**Phase 3 — simanim-tiqqun.** Find the printed ToC in the B (or A) section and read the
haftarah/megillot start pages straight off it (C scan numbers equal printed numbers, so
the ToC maps the whole C body in a handful of image reads); fall back to bisection sweeps
of C only if the ToC disappoints. Fill `segments`, then census the C body — Torah, the
haftarot (each with the name and bcv range the book has for it, in the haftarah table),
and the three full-text megillot (שיר השירים, רות, איכה; Ecclesiastes and Esther have
notes only, so no census there, and the ~C410–C444 notes tail is not censused at all) —
and extend `lookup` so a Nakh bcv inside a printed haftarah yields the simanim-tiqqun
hit(s). The unpointed D section is out (Ben, 2026-08-07). Report the haftarah inventory
here. Independent of Phase 2, so the two can interleave.

## Open questions for Ben (defaults chosen so no phase blocks on them)

1. **Census order across the four full-Tanakh editions?** Default: jc1, bhl, koren,
   simanim-tanakh.
2. **Scope:** the other ScansOfBooks folders (JC2 Companion, JC3, Da'at Miqra, the
   readers, the loose PDFs) stay out of the index. Confirm.
