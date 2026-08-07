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
- 2026-08-07, still session 1, three more decisions from Ben: the Decalogues get
  strand-aware lookup (a bare bcv → the body Decalogue, whichever strand the edition's
  body has; a `t`/`e` suffix names the strand wanted); lookup is by phrase-qualified or
  phrase-unqualified verse (both in Decisions below); and "phrase" is used in its broad
  sense throughout this undertaking — a run of one or more consecutive atoms, so a lone
  chanted word or even a lone atom counts.

## Decisions (proposed 2026-08-06 by the planning session unless attributed to Ben; Ben can veto the proposals)

- **Home repo: MAM-basics** (`C:\Users\BenDe\GitRepos\MAM-basics`, venv at
  `.venv\Scripts\python.exe`). All of Ben's Python lives here now and new issues are filed
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
  `C:\Users\BenDe\GitRepos\codex-index-leningrad\UXLC-utils-sparse\data\lci_recs.json`,
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
  phrase at each edge of the page — its first and its last few atoms — stored verbatim
  as `start_phrase` / `stop_phrase` evidence. The `census` tooling locates each phrase in MAM-parsed text and derives the
  atom numbers from it — no hand-counting of atoms, no reading of printed verse numbers —
  and demands a longer phrase whenever the current one fails to pin a unique position in
  the candidate neighborhood (Ben's "verse-unique phrase" requirement). The stored phrase
  keeps every record independently re-verifiable, against the image and against the
  text, forever after.
- **The bring-up is one generated HTML page, opened by the program.** Written under
  `.novc\scan-pages\` (gitignored), one section per edition: the page image(s) the
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

Scans root: `C:\Users\BenDe\OneDrive\Documents\ScansOfBooks`. The file counts above and
every claim below were read from the folder on 2026-08-06 with ad hoc PowerShell not worth
preserving; Phase 0's `survey` subcommand is the re-derivation command for all of them, and
a mismatch when it runs is a finding, not an error in this doc. Caveat: the folder is under
OneDrive, so files can be cloud-only placeholders; `survey` should fail loudly on a
zero-availability file rather than index it silently.

**Four editions share one book-code family in their filenames** (Koren-style: Torah
`G E L N D`; Former Prophets `Js Ju 1S 2S 1K 2K`; Latter Prophets `I Je Ee` + twelve
`Ho Jl A O Jn Mi Na Hb Ts Hg Zc Ma`; Writings `Ps Pr Jb S R La Ec Es Da Er Ne 1C 2C`).
The body-page filename shapes:

- **jc1**: `NNN-<bk>.jpg` (e.g. `220-Js.jpg`) — NNN is the scan sequence and likely the
  printed page number; front matter `#NN-<desc>.jpg`; end matter `NNN-NN-<desc>.jpg`;
  service tokens `blank`, `ToC` appear as the `<bk>` slot.
- **koren**: `<sec><n>-<bk>-NNN.jpg` for big books with per-book numbering restarting at
  001 (`A1-G-001.jpg`), but `<secletter><sub>-<bk>-NNN.jpg` with *continuous* printed page
  numbers for the books scanned later (`BA-1S-087.jpg` … `CL-Ma-589.jpg`,
  `FA-Er-229.jpg` … `FD-2C-374.jpg`). Sections: A Torah, B Former Prophets, C Latter
  Prophets, D Ps/Pr/Jb, E Megillot, F Da/Er/Ne/Chronicles, then `V` ×55 (unidentified —
  Phase 0 eyeballs one), `W`, `X-back-cover`, `Y` spine. Printed-number gaps exist (e.g.
  `BC-1K-187` then `BC-1K-189`); harmless, since lookup works on the sorted pages list,
  never on printed numbers.
- **simanim-tanakh**: `<sec>-<bk>-NNNN.jpg` with continuous numbering (`B1-Js-0360.jpg`,
  `D2-Pr-1150.jpg`); front matter `1-*` and `2-*` (includes `2-03-ToC.jpg`); oddball
  singletons `A9-A2-*`, `A9-A5-*` to classify in Phase 0. The 2026-08-06 quick tally
  matched only dash-terminated prefixes, so Samuel/Kings/minor-prophets/Chronicles files
  (presumably `BA-`/`CA-`-style, as in koren) were not tallied — Phase 0 must classify
  **every** file and fail on any it cannot, precisely so nothing drops out that way.
- **bhl**: `NNNN-<bk>.jpg` with continuous scan numbering (`0296-D.jpg`,
  `0620-Isaiah.jpg`) — but the book token is *mixed-convention*: mostly the short family
  (`G`, `Js`, `Ps`) with longform outliers (`Isaiah` ×62, `Ruth` ×5, `Song` ×5, and
  singleton `Deut`/`Exod` section-title pages), plus service tokens `blank` ×40, `title`
  ×27, `Appendix` ×5, `ToC` (in `#08-v-ToC.jpg`-style front matter), `back-cover`,
  `spine`. The book-code table in `py/scan_pages/` gets the longforms as extra rows.

**simanim-tiqqun is the special one.** Five filename sections, meanings established by
reading sample pages (`B10.jpg`, `B60.jpg`, `C012.jpg`, `C400.jpg`, `D10.jpg`,
`E10-06.jpg` on 2026-08-06; `C300.jpg` on 2026-08-07):

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
  to the census). **Megillot**: `C400.jpg` is מגילת רות chapter 3, further on in C.
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

Tracked index, one JSON per edition at `in\scan-pages\<edition-id>.json`:

```json
{
  "edition": "jc1",
  "folder": "JC1 Jerusalem Crown",
  "pages": ["#01-front-cover.jpg", "...", "220-Js.jpg", "..."],
  "recs": [
    {"page": "013-G.jpg",
     "bkid": "Genesis", "startc": 1, "startv": 1, "startp": 1,
     "stopc": 1, "stopv": 31, "stopp": 12,
     "start_phrase": null, "stop_phrase": "...", "note": null}
  ]
}
```

- `pages` is the complete sorted listing (front and back matter included, classified), so
  the index is meaningful — and lintable — on a clone with no scans folder at all.
- `recs` reuse `lci_recs.json`'s column dictionary at page level (its line/column fields
  simply don't exist here), plus the two phrase-evidence fields. Recording *both* ends of
  every page is deliberate redundancy: each record is verifiable against its own page
  image alone, and the contiguity lint then cross-checks every adjacent pair.
- `survey` seeds each book's first body page with its start half — `startc/startv/startp`
  of 1:1 atom 1 comes free from the filename book codes, `start_phrase` null because no
  page was read for it. The census fills everything else.
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

- every rec's page is in `pages`; every position parses against MAM verse counts (FAIL,
  never skip, when MAM-parsed is absent — per the repo's missing-input rule);
- within a segment, recs in page order have strictly advancing text positions and
  consecutive recs meet at adjacent atoms in text order — no gap, no overlap, no page
  silently skipped — and segments' page ranges tile the classified body pages without
  overlap;
- each stored phrase, re-located in MAM-parsed text, lands exactly at its rec's recorded
  atoms — a differential check of every record against an independent derivation;
- atoms-per-page stays within a sane band, flagging the outliers a misread produces.

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

- Repos: `C:\Users\BenDe\GitRepos\MAM-basics` (venv at `.venv\Scripts\python.exe`);
  sibling `C:\Users\BenDe\GitRepos\MAM-parsed` present (verse counts). Scans at
  `C:\Users\BenDe\OneDrive\Documents\ScansOfBooks` with the five folders named above.
- Baseline: 320 tests pass via `.venv/Scripts/python.exe py/main_test.py` (320 measured
  2026-08-04 per `doc/metsudah-vs-ctr.md`; re-measure before starting — a different
  count is a finding). After each phase the suite still passes; Phase 0 raises the count
  by exactly one file's worth (the new lint).
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

**Phase 0 — survey and tracked inventory.** No image reads. Implement `survey`: walk the
five folders, classify every filename (edition-specific parsers + the shared book-code
table), fail loudly listing any file it cannot classify (the `A9-*` singletons and koren's
`V` run will surface here; if a classification needs eyes, read that one page and record
what it is in this doc). Emit the five JSONs with `pages` and the seeded start halves;
implement `check` + the pytest lint; report per-edition/per-book page counts and
anomalies here. Expected result: 39 seeded book-first pages in each of jc1, koren,
simanim-tanakh, bhl (fewer only if a book genuinely shares its opening page), none yet
for simanim-tiqqun.

**Phase 1 — tooling, proven on one small book.** Implement
`lookup <bk39> <ch>:<v>[t|e] [<phrase>]` (exact-or-refuse) → HTML bring-up, and `census` (page-edge phrases in, atoms out,
contiguity checked against the previous record as each new one lands). Then census one
small book end to end in one edition — Ruth in jc1, say — and verify: `check` clean, and
spot-read several lookups against the page images, straddling verses included, confirming
the verse is really on the returned page(s). Record the spot results here. **Pause for
Ben:** he tries it and confirms the record shape before ~5100 pages get read into it.

**Phase 2 — the censuses, edition by edition.** For each of jc1, bhl, koren,
simanim-tanakh: read every body page's edges, one book-sized chunk at a time — lints, a
chat report and a commit per chunk. Edition order is Ben's call (open question below).

**Phase 3 — simanim-tiqqun.** Find the printed ToC in the B (or A) section and read the
haftarah/megillot start pages straight off it (C scan numbers equal printed numbers, so
the ToC maps the whole C body in a handful of image reads); fall back to bisection sweeps
of C only if the ToC disappoints. Fill `segments`, then census the C body — Torah, the
haftarot (each with the name and bcv range the book has for it, in the haftarah table),
the megillot — and extend `lookup` so a Nakh bcv inside a printed haftarah yields the
simanim-tiqqun
hit(s). The unpointed D section is out (Ben, 2026-08-07). Report the haftarah inventory
here. Independent of Phase 2, so the two can interleave.

## Open questions for Ben (defaults chosen so no phase blocks on them)

1. **Census order across the four full-Tanakh editions?** Default: jc1, bhl, koren,
   simanim-tanakh.
2. **Scope:** the other ScansOfBooks folders (JC2 Companion, JC3, Da'at Miqra, the
   readers, the loose PDFs) stay out of the index. Confirm.
