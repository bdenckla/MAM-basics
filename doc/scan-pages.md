# Scan-pages index: bring up five scanned editions at a bcv — plan

Ben's ask, 2026-08-06: *"index important editions I have scanned (in 'ScansOfBooks') so
that, given a bcv (book-chapter-verse) reference, I can run a program that will bring up the
relevant page in all those editions (JC1 (Jerusalem crown), Koren, Simanim Tiqqun (if the
bcv is in Torah or haftarah), Simanim Tanakh, Dotan BHL)."*

This file is the single plan-and-findings document for the undertaking (per Ben's
one-tracked-plan rule). Findings replace plan text here as phases complete. It is written
for a fresh session that has no other context. Its thin pointer issue is #349, filed on
2026-10-31.

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
- 2026-09-10: one design change from Ben, and no code touched. Finding the page is
  separated from showing it — `lookup` returns records and prints a link per edition on
  stdout, and the generated HTML bring-up is out. In Decisions below, the bring-up bullet
  becomes two — the new design and what it replaces — and the cwd-independence bullet's
  stdout clause is rewritten. **Phase 1 has still not started**: `py/main_scan_pages.py` has `survey` and
  `check` and no `lookup` or `census`, and all 156 records across the four full-Tanakh
  editions are still unread seeds — every one has a null `start_phrase`, none has a
  `stop_phrase`, and no edition has a segment. Measured that day from
  `in/scan-pages/*.json`.
- 2026-09-10, later that day, a worktree session at `f92c061c`: **a ten-page cost probe
  ran on koren's Genesis, and Phase 1 has still not started.** Ben asked how slow the
  page-edge method is before the census commits to it, and the answer — about 29 seconds
  of session wall-clock a page, with all 20 edges located exactly — is recorded under
  Phase 1 below, in the paragraphs headed "Cost probe, 2026-09-10". The probe built no
  tooling, and none of its ten records entered `in/scan-pages/koren.json`.
- 2026-11-02: **Phase 1's first-book pilot is implemented on an isolated research
  branch.** JC and BHL each have two verified Obadiah page portions, covering all
  21 verses. At that checkpoint the catalogs contained 158 records: four completed records
  and 154 unread seeds. Exact `lookup` and whole-book `census` exist; `check`
  re-locates both edge cues and verifies complete adjacent-atom coverage for every
  declared book. This is the first-book review boundary, not a completed universal
  index. The commands, observed splits and remaining limitations are below.
- 2026-11-02, next bounded batch: Jonah is fully censused in JC and BHL, adding
  six book/page portions. The catalogs now contain 162 records: ten completed
  records and 152 unread seeds. All 69 verses of Obadiah and Jonah are covered
  in each edition. Both BHL Jonah page breaks continue verses excluded by the
  new page's printed header; the adopted records use actual running text.
- 2026-11-02, Micah batch: ten further book/page portions are censused in JC
  and BHL. All 174 verses of Obadiah, Jonah and Micah are covered in each
  edition. The catalogs contain 170 records: twenty completed records and
  150 unread seeds. Ordinary ketiv/qere is supported only when each form
  occupies one atom; phrase lookup uses its qere spelling.
- 2026-11-02, Nahum batch: six further portions complete Nahum in both
  editions, bringing coverage to 221 verses in four books per edition.
  The catalogs contain 174 records: twenty-six completed records and
  148 unread seeds. Explicit small-letter markup retains the letter within
  its word. Unique edge cues may span verses on the same page.
- 2026-11-02, Habakkuk batch: five further portions complete Habakkuk in both
  editions, bringing coverage to 277 verses in five books per edition.
  The catalogs contain 177 records: thirty-one completed records and
  146 unread seeds. No text-projection changes were needed for this batch.
- 2026-11-03, Zephaniah batch: six further portions complete Zephaniah in
  both editions, bringing coverage to 330 verses in six books per edition.
  The catalogs contain 181 records: thirty-seven completed records and
  144 unread seeds. The explicit paseq template keeps neighboring words
  separate, following the maintained atom definitions.
- 2026-11-03, Haggai batch: seven further portions complete Haggai in both
  editions, bringing coverage to 368 verses in seven books per edition.
  The catalogs contain 186 records: forty-four completed records and
  142 unread seeds. No text-projection changes were needed for this batch.
- 2026-11-03, Zechariah batch: twenty-one further portions complete Zechariah
  in both editions, bringing coverage to 579 verses in eight books per edition.
  The catalogs contain 205 records: sixty-five completed records and
  140 unread seeds. No text-projection changes were needed for this batch.
- 2026-11-03, Malachi batch: eight further portions complete Malachi in both
  editions, bringing coverage to 634 verses in nine books per edition. The
  catalogs contain 211 records: seventy-three completed records and 138 unread
  seeds. Explicit large-letter markup retains its letter within the word;
  BHL's repeated closing verse is recorded as same-page display evidence.

- 2026-11-03, Amos batch: 15 further portions complete Amos in both
  editions, bringing coverage to 780 verses in 10 books per edition. The
  catalogs contain 224 records: 88 completed records and 136 unread seeds.

- 2026-11-03, Joel batch: 9 further portions complete Joel in both
  editions, bringing coverage to 853 verses in 11 books per edition. The
  catalogs contain 231 records: 97 completed records and 134 unread seeds.

- 2026-11-03, Hosea batch: 15 further portions complete Hosea in both
  editions, bringing coverage to 1050 verses in 12 books per edition. The
  catalogs contain 244 records: 112 completed records and 132 unread seeds.

- 2026-11-03, first Ezekiel checkpoint: native page bounds are verified for
  JC 524–529 and BHL 796–802. They cover chapters 45–48 completely (107
  verses, 1,670 atoms per edition), plus differing partial spans of chapter 44.
  These thirteen portions are retained as a private boundary checkpoint;
  they have **not** entered the whole-book census or public lookup. Accepted
  coverage and catalog counts above are unchanged. The remaining Ezekiel
  inventory has 43 JC and 63 BHL portions still to verify.
  Named three-petucha/two-samekh breaks follow the maintained separator
  semantics. The written-but-not-read word follows the maintained written-atom
  policy, with strict matching one-atom forms. Both scans print the extra word
  at 48:16. All 1,269 projectable Ezekiel verses were independently compared
  with MAM-simple; 8:6, 9:11, 23:42 and 42:9 remain refused pending explicit
  multi-atom ketiv/qere alignment. The supported verses are a text-projection
  result, not verified page coverage. Continue in bounded chapter groups;
  whole-book adoption still requires all pages and all atoms.

- 2026-11-03, second Ezekiel checkpoint: fourteen further native page portions
  (JC 518–523; BHL 788–795) join the preserved first group. Chapters 40–48
  are now fully covered in private boundary evidence: 260 verses / 3,965
  atoms per edition, with 27 of 119 Ezekiel portions verified and 92 left
  (37 JC, 55 BHL). The new group completes chapters 40–44 (153 verses /
  2,295 atoms), reusing the inspected continuation pages in the first group.
  Whole-book lookup and accepted catalog counts remain unchanged.
  Ezekiel 42:9 is resolved: both scans show two ordered written words and
  two ordered qere words. Only that explicitly named special two-word
  subtype, with exactly two atoms in each stored form, is supported; qere
  spelling follows the maintained projection. Independent MAM-simple
  comparison now passes for 1,270 verses / 18,675 atoms. The three remaining
  refusals are 8:6, 9:11 and 23:42. Twenty-five cumulative page joins,
  including twenty-three split-verse cases, pass exact atom checks.

- 2026-11-03, third Ezekiel checkpoint: thirteen further native portions
  (JC 513–517; BHL 780–787) join the preserved evidence. Complete chapters
  35–48 now cover 393 verses / 5,974 atoms per edition in private evidence.
  Forty of 119 Ezekiel portions are verified; 79 remain (32 JC, 47 BHL).
  Chapters 35–39 add 133 complete verses / 2,009 atoms, reusing the JC518
  continuation. The differing partial chapter-34 spans remain explicit.
  All 38 cumulative page joins and 35 split-verse cases pass exact checks.
  No projection changes were needed; independent text comparison still
  passes for 1,270 Ezekiel verses, with the same three explicit refusals.
  Accepted catalog counts and whole-book lookup coverage are unchanged.

- 2026-11-03, fourth Ezekiel checkpoint: thirteen further native portions
  (JC 508–512; BHL 772–779) extend the private evidence to complete chapters
  30–48: 533 verses / 8,084 atoms per edition. Chapters 30–34 add 140 verses /
  2,110 atoms, using the preserved chapter-34 continuations. Fifty-three of
  119 Ezekiel portions are verified; 66 remain (27 JC, 39 BHL). All 51
  cumulative page joins and 47 split-verse cases pass exact checks. A repeated
  clause at 32:24–25 requires a longer unique boundary cue. BHL774 begins with
  a continuation of chapter 30 although its running header starts at 31:1.
  No projection changes were needed, and the three explicit refusals remain.
  Accepted whole-book lookup and catalog counts are unchanged.

- 2026-11-03, fifth Ezekiel checkpoint: ten further native portions
  (JC 504–507; BHL 766–771) complete private evidence for chapters 25–48:
  654 verses / 9,753 atoms per edition. Chapters 25–29 add 121 complete
  verses / 1,669 atoms, using preserved chapter-29 continuations. Sixty-three
  of 119 Ezekiel portions are verified; 56 remain (23 JC, 33 BHL). All 61
  cumulative page joins and 57 split-verse cases pass exact checks. No
  projection changes were needed; 8:6, 9:11 and 23:42 remain refused.
  Accepted whole-book lookup and catalog counts are unchanged. The next
  chapter group reaches the unresolved 23:42 alignment case.

- 2026-11-03, sixth Ezekiel checkpoint: seventeen further native portions
  (JC 497–503; BHL 756–765) complete private evidence for chapters 20–48:
  842 verses / 12,402 atoms per edition. Chapters 20–24 add 188 complete
  verses / 2,649 atoms, using the preserved chapter-24 continuations.
  Eighty of 119 Ezekiel portions are verified; 39 remain (16 JC, 23 BHL).
  All 78 cumulative page joins and 73 split-verse cases pass exact checks.
  At 23:42, both native editions establish one written/qere slot. The qere's
  named vowel-alternative wrapper now uses the existing consonant-identical
  branch rule, with strict string-form and single-atom guards. Independent
  MAM-simple comparison passes for 1,271 Ezekiel verses / 18,694 atoms;
  8:6 and 9:11 remain explicitly unsupported. Seven focused tests pass,
  including an independent nested-form comparison and malformed-form refusals.
  Accepted whole-book lookup and catalog counts remain unchanged.

- 2026-11-03, seventh Ezekiel checkpoint: twelve further native portions
  (JC 492–496; BHL 749–755) complete private evidence for chapters 15–48:
  983 verses / 14,351 atoms per edition. Chapters 15–19 add 141 complete
  verses / 1,949 atoms, using the preserved chapter-19 continuations.
  Ninety-two of 119 Ezekiel portions are verified; 27 remain (11 JC, 16 BHL).
  All 90 cumulative joins and 83 split-verse cases pass exact checks.
  No projection changes were needed; 8:6 and 9:11 remain unsupported.
  Seven focused tests pass, and accepted whole-book lookup and catalog
  counts remain unchanged.

## Codex entry indexes

`in/lci_recs.json` is the public Leningrad Codex entry index. Its canonical top level
has exactly `header` and `body`. The header contains `description`,
`consumer_notice`, the retained LCIndex and USC-WSRP provenance fields, and
`column-dictionary`. The body alone contains page records. Each page record uses the
fields named by `column-dictionary`, including page, column, line, book, chapter,
verse, and atom boundaries plus an optional note.

The Aleppo, Cambridge and Evr. II B 55 entry indexes use the same `{header, body}` contract;
their format-specific fields are documented in `aleppo/README.md`, `cam1753/README.md` and
`evr-ii-b-55/README.md`. Each header's `consumer_notice.documentation` points to the relevant
consumer guide.

These entry indexes are locator indexes, not manuscript transcriptions or Bible editions.
Ranges and text cues identify positions on photographed pages; a cue copied or derived
from MAM is not evidence that the manuscript has MAM's pointing or mark order. A range
can begin or end mid-verse. Gaps and incomplete coverage are meaningful and must not be
rounded to whole verses or filled from another edition. Line-break and geometry data
are separate evidence and must not be inferred from an entry-index record. A Leningrad
record's `note` can describe its page's layout as read from the page image, such as page
F132A's "column 1 has 28 lines!", where MAM-basics' location estimator assumes 27 lines per
column. Such notes are incidental: most pages have none, and a missing note says nothing
about a page's layout.

## Decisions (proposed 2026-08-06 by the planning session unless attributed to Ben; Ben can veto the proposals)

- **Home repo: MAM-basics** (any full clone of it, venv at
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
- **Verse text and counts come from the landed MAM-parsed product at runtime** (via
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
  the one that makes a page error inexpressible — now MAM-basics'.** In
  `uxlc/data/lci_augrecs.json`,
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
- **Finding the page is separated from showing it, and `lookup` prints its answer on
  stdout (Ben's decision, 2026-09-10).** The resolution — a bcv, an optional strand suffix
  and an optional phrase in; a page record or records out — is a library function under
  `py/scan_pages/` that renders nothing, writes nothing and opens nothing. Ben's reason,
  2026-09-10: *"the main point is to find the page, and that part of the code should be
  totally abstracted from what you do with the page, which might have multiple answers
  depending on the application."* **The first use of that library is deliberately a very
  short `main`** (Ben, 2026-09-10) that prints one `file:///` link into the scans folder
  per edition and nothing else. Its shortness is the test that the separation holds:
  anything the resolution left for its caller to do would show up as length right here. An
  edition whose range is not censused gets an honest refusal naming what is censused,
  never a guess. Everything beyond the link rides along later, in a JSON output shape some
  second application asks for — the record behind each answer, its phrases, the neighboring
  pages — and none of it is built until an application wants it. **The program opens
  nothing**, for Ben and for a session alike.
- **What that replaces, and why.** From 2026-08-06 to 2026-09-10 the bullet above
  specified one generated HTML page under `.novc/scan-pages/`, one section per edition,
  the page images inline via `file:///` URLs with `loading="lazy"` because the JPGs run
  1–18 MB, prev/next links, and `os.startfile` as the default when Ben ran it. Ben's
  objection, 2026-09-10: with no UI being added, an HTML page is a wrapper around links
  that an external image viewer already handles, and its one real cost — the
  lazy-loading — existed only because that page embedded the images. The three things it
  bought all survive as printed text: several editions at once become several lines,
  prev/next become two more links, and the record reads more easily as text than inside a
  generated page. What is genuinely lost is seeing several editions side by side in one
  scroll, which is thin at 5100×7100, where one page at a time is what fits. The
  `os.startfile` default went with it, against the standing rule that a link costs one
  click when the page is not already open and a duplicate window when it is.
- **The program is cwd-independent.** Scans root and repo paths are anchored in code
  (`mb_cmn.paths.book_scans_root()`: `~/OneDrive/Documents/ScansOfBooks` unless
  `BOOK_SCANS_ROOT` overrides it; `mb_cmn/paths.py` for siblings), never cwd-relative, so it
  runs from anywhere. UTF-8 stdio reconfigure first
  thing in `main()`, per the global rules — and load-bearing rather than precautionary
  since 2026-09-10, because the answer itself now goes to stdout: a JSON ride-along that
  holds the page-edge phrases puts Hebrew there. Until that day this clause said real
  output went to the HTML file and stdout got only short ASCII progress.
- **Edition ids** (used in filenames, JSON, and the CLI):

  | id | folder under ScansOfBooks | files |
  | --- | --- | --- |
  | `jc1` | `JC1 Jerusalem Crown` | 927 |
  | `koren` | `Koren Classic Tanakh` | 1332 |
  | `simanim-tanakh` | `Feldheim Simanim Tanakh` | 1552 |
  | `simanim-tiqqun` | `Feldheim Simanim Tiqqun` | 614 |
  | `bhl` | `Biblia Hebraica Leningradensia` | 1295 |

### Canonical holdings outside the current five-edition index

This subsection was added by commit `622b48fd` on 2026-09-24; no source here identifies a separately
dated decision by Ben.

The canonical Da'at Miqra scan is
`C:/Users/BenDe/OneDrive/Documents/ScansOfBooks/Da-at Miqra`. It is available and
organized by biblical book, but it is not one of the five editions currently indexed by
`py/main_scan_pages.py` and has no `in/scan-pages/` index. A Da'at Miqra index is possible
future work, not a phase of the current five-edition undertaking.

`C:/Users/BenDe/OneDrive/Documents/Tanakh/misc/Breuer-DM-mekorot-hanosah.pdf` is a
low-quality, noncanonical copy and is not a substitute for the canonical scan. It remains
untouched; deleting it would be a separate, explicitly authorized task.

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
  leaf, has the publisher's back-cover artwork over וְעַתָּה כִּתְבוּ לָכֶם אֶת־הַשִּׁירָה הַזֹּאת, with the
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

- Repos: any full MAM-basics clone (venv at `.venv/Scripts/python.exe`), with its
  product `MAM-parsed/` present (verse counts). Scans at
  `C:/Users/BenDe/OneDrive/Documents/ScansOfBooks` with the five folders named above.
- Worktree-isolable (Ben asked 2026-08-07). Every tracked write is in MAM-basics, so a
  worktree isolates the undertaking fully; the spill is read-only. The scans path is
  absolute and checkout-independent. Since the 2026-09-06 product move,
  `mb_cmn.paths.mam_parsed_path()` selects the MAM-parsed product inside the
  same checkout and fails if its plus inputs are absent. A worktree runs its
  home clone's venv by absolute path, per the global rules.
- Baseline: **915 passed, 5 skipped**, measured 2026-08-07 at `fc23077` from the repo root
  of the primary clone. The 320 this bullet used to cite, from `doc/metsudah-vs-ctr.md`, is
  stale by a wide margin — that figure predates the accgram and CLC code arriving on
  2026-08-01 — so treat the count here as the baseline and `doc/metsudah-vs-ctr.md`'s as
  a historical note. Phase 0 took it to **919**: two tests in the new lint file, and two
  more because `test_entry_point_subcommands.py` parametrizes over the entry points and
  there is now one more. **Re-measured 2026-09-10 at `f92c061c`, in a worktree with
  `REPOS_ROOT` set: 987 passed, 5 skipped, of 992 collected**, so 919 is a historical figure
  now, the suite having gained 68 tests since Phase 0's 924. Re-establish it from the repo
  root with `./.venv/Scripts/python.exe py/main_test.py`,
  and re-measure rather than trust it.
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
  than the known background noise it used to be. Running the full suite in the home clone
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

### Phase 1 pilot: exact Obadiah lookup in JC and BHL, 2026-11-02

All four original images were inspected, their printed footer numbers were read,
and the internal page breaks were re-read in native-pixel crops. The source cues
below describe the Obadiah portion of a shared page, not all of that page's text.
No image or crop is stored in this repository.

| Edition | Scan filename | Observed printed page | Obadiah interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `544-A-O.jpg` | 544 | 1:1 atom 1 through 1:9 atom 1 |
| `jc1` | `545-O-Jn.jpg` | 545 | 1:9 atom 2 through the book's final atom |
| `bhl` | `0825-A-O.jpg` | 825 | 1:1 atom 1 through 1:18 atom 2 |
| `bhl` | `0826-O-Jn.jpg` | 826 | 1:18 atom 3 through the book's final atom |

The JC break is between `וחתו` and `גבוריך`; the BHL break is between
`והיה בית` and `יעקב אש`. Those readings were checked at native resolution.

The first page in each edition also contains Amos; the second also contains Jonah.
Those neighboring book portions were uncensused at this pilot checkpoint. Jonah
was subsequently completed in the continuation below; Amos remains uncensused.
The BHL header on page 826
starts its Obadiah range at 1:19, but the actual first running text continues
1:18. The stored boundary follows the running text, not the header.

Use the home clone's interpreter from a worktree. For example:

```powershell
python py/main_scan_pages.py lookup Obadiah 1:9 --edition jc1 --edition bhl
python py/main_scan_pages.py lookup Obadiah 1:9 "גבוריך תימן" --edition jc1
python py/main_scan_pages.py lookup Obadiah 1:18 "יעקב אש" --edition bhl
python py/main_scan_pages.py check
```

An unqualified verse returns every page the verse touches: JC verse 9 returns
544 and 545; BHL verse 18 returns 825 and 826. A unique phrase resolves to the
page of its first atom: the two qualified examples return JC 545 and BHL 826.
The library returns records without rendering or opening anything. The CLI's
stdout contains only local file links; uncensused editions and strands are
reported on stderr. A request with no covered edition exits with status 1.
These commands also passed from outside the checkout.

The census command is `census <edition> <book39> <edge-json>`. Its input is a JSON
array with one entry per body page for that book, in scan order. Each entry has
`page`, an independently observed integer `printed_page`, `note`, and `start`
and `stop` arrays shaped `[chapter, verse, "letters-only cue"]`. The chapter
and verse identify the cue's first atom for a start, or last atom for a stop;
matching the cue derives its atom number. A cue may span neighboring verses,
but must match uniquely with that endpoint in the given verse and must lie
entirely within its observed page interval. Adoption checks all of the book's pages and
its first and last atoms before writing anything. The stored records retain
both cues; the input need not become a second tracked copy.

The initial body segment explicitly lists its completed `bkids` and their page
identities. It may cover only the Obadiah portions of its boundary pages. A later
whole-book batch can extend this contiguous body run in either direction;
adopting a distant book with intervening uncensused body pages is refused.
This preserves the existing plan's single contiguous body segment while making
partial coverage explicit. Lookup never treats an unread seed as coverage.

The first-phase text projection accepts Scripture strings, the target of a
`נוסח` note, vowel alternatives whose consonantal atoms agree, the explicit
legarmeh marker `מ:לגרמיה-2` and paseq `מ:פסק` as boundaries without atoms, and the main
one-atom form of the modern trivial ketiv/qere template, matching MAM-simple.
The Micah continuation adds ordinary ketiv/qere when both forms are one atom,
using the qere spelling at that common position. Ezekiel adds the named
vowel-alternative wrapper inside such a form, only with string alternatives
whose consonantal atoms agree and preserve a single slot. The Nahum continuation adds
the special-letter word wrapper and small-letter template; Malachi adds the
explicit large-letter template. All retain their Scripture parameter without
inserting a word boundary. Hosea adds the named `פפ` paragraph-break template,
which contributes a separator while its optional annotation contributes no
Scripture. Ezekiel also supports the explicitly named special two-word
ketiv/qere subtype with exactly two ordered atoms in both forms, and the
matching one-atom written-but-not-read form. Other multi-atom ketiv/qere,
unimplemented templates and named Decalogue strands remain unsupported.
Extending those cases needs explicit source alignment;
template names or argument shapes are not grounds for guessing it. An
atoms-per-page advisory band remains deferred until representative full-page
censuses exist. This pilot does not claim that every planned Phase 1 feature
is finished.

Verification: the focused scan-page and entry-point checks passed (six tests).
An independent comparison against MAM-simple covers every verse and atom of
the adopted book. Every source edge cue resolves back to its recorded page.
Additional direct checks confirmed both split verses, phrase-qualified hits,
uncensused and ambiguous-query refusals, failed-census write neutrality,
idempotent census regeneration, and cwd-independent CLI output. `survey` now
refuses before overwriting any adopted census; census-preserving inventory
refresh is not yet implemented. `check` validates without reading the scans.

### Jonah continuation, 2026-11-02

The authorized next bounded batch completed Jonah in both editions. The four
additional original images were inspected, and native crops checked both sides
of each internal page break. The beginning and end of the book were also checked
at native size. Existing Obadiah coverage remains valid.

| Edition | Scan filename | Observed printed page | Jonah interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `545-O-Jn.jpg` | 545 | 1:1 atom 1 through 1:14 atom 8 |
| `jc1` | `546-Jn.jpg` | 546 | 1:14 atom 9 through 4:8 atom 17 |
| `jc1` | `547-Jn-Mi.jpg` | 547 | 4:8 atom 18 through 4:11 atom 23 |
| `bhl` | `0826-O-Jn.jpg` | 826 | 1:1 atom 1 through 1:12 atom 1 |
| `bhl` | `0827-Jn.jpg` | 827 | 1:12 atom 2 through 3:7 atom 5 |
| `bhl` | `0828-Jn.jpg` | 828 | 3:7 atom 6 through 4:11 atom 23 |

The JC breaks are after `אל נא` and `נפשו`, with the next pages starting
`נאבדה בנפש האיש הזה` and `למות ויאמר`. BHL page 826 ends with the opening
`ויאמר` of 1:12; page 827 starts `אליהם שאוני` despite its header beginning
at 1:13. Page 827 ends with `מטעם המלך` in 3:7; page 828 starts `וגדליו לאמר`
despite its header beginning at 3:8. The final cue in both editions is
`ובהמה רבה`. The shared Micah portion of JC page 547 is not indexed yet.

For example, `lookup Jonah 1:12 --edition bhl` returns 826 and 827, while adding
the phrase `אליהם שאוני` returns only 827. Likewise, unqualified BHL 3:7 and JC
1:14 and 4:8 return both pages, with phrase-qualified lookups resolving to the
correct later page. All four breaks were checked directly.

The independent MAM-simple comparison now checks all 48 Jonah verses and 688
Jonah atoms as well as Obadiah. The six focused tests passed. Direct checks
confirmed every split above, phrase resolution, idempotent Jonah regeneration,
and the earlier Obadiah/refusal/write-neutrality checks. The full suite and mega
were not run for this isolated bounded batch under the focused-check policy.
This continuation does not authorize or imply a large census without the
first-book record-shape review below.

### Micah continuation, 2026-11-02

All ten Micah book/page portions were inspected. Nine original images were new
to this batch; shared JC 547 was re-read at the Micah opening and its final
lines. Native-pixel crops verified every page edge, the book transitions and
the four ordinary ketiv/qere positions. Printed footer numbers were read
separately from filenames. No image or crop is stored in this repository.

| Edition | Scan filename | Observed printed page | Micah interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `547-Jn-Mi.jpg` | 547 | 1:1 atom 1 through 2:10 atom 3 |
| `jc1` | `548-Mi.jpg` | 548 | 2:10 atom 4 through 4:9 atom 13 |
| `jc1` | `549-Mi.jpg` | 549 | 4:9 atom 14 through 6:10 atom 8 |
| `jc1` | `550-Mi-Na.jpg` | 550 | 6:10 atom 9 through 7:20 atom 10 |
| `bhl` | `0829-Mi.jpg` | 829 | 1:1 atom 1 through 2:5 atom 3 |
| `bhl` | `0830-Mi.jpg` | 830 | 2:5 atom 4 through 3:11 atom 15 |
| `bhl` | `0831-Mi.jpg` | 831 | 3:11 atom 16 through 5:2 atom 11 |
| `bhl` | `0832-Mi.jpg` | 832 | 5:2 atom 12 through 6:8 atom 19 |
| `bhl` | `0833-Mi.jpg` | 833 | 6:9 atom 1 through 7:16 atom 4 |
| `bhl` | `0834-Mi-Na.jpg` | 834 | 7:16 atom 5 through 7:20 atom 10 |

BHL's headers on 830, 831, 832 and 834 begin at 2:6, 3:12, 5:3 and 7:17
respectively, but their actual opening text continues the preceding verse.
JC 549 begins with the final atom of 4:9, `כיולדה`; JC 550 begins with the
final atom of 6:10, `זעומה`. A verse-only page boundary would miss these words.
The ordinary body coverage reached Micah's end at this checkpoint. The Nahum
portions of JC 550 and BHL 834 were completed in the following continuation.

Micah's ordinary ketiv/qere occurs at 1:3, 1:8, 1:10 and 3:2. In both editions
each form occupies one word position, verified in the images. The text reader
accepts only the two explicit ordinary template names `כו״ק` and `קו״כ`,
validates their current schema and requires one atom in each form. It uses
parameter 2, the qere in either display order, matching the independent
MAM-simple `kq-q` child. Phrase lookup therefore uses `במתי`, `שולל`,
`התפלשי` and `רע` at those four positions; ketiv aliases are not implemented.
Multi-atom forms still refuse, even when their atom counts agree. This batch
does not choose an alignment rule for them.

All 105 Micah verses and 1,396 atoms agree with the independent MAM-simple
export. The six focused tests passed. Direct checks covered all seven
within-verse splits, phrase-qualified lookups including a phrase spanning a
page break, the complete-verse boundary at BHL 832/833, all four qere phrases
in both editions, and idempotent census regeneration. The full suite and
mega were not run under the focused-check policy. This remains a bounded
continuation before the large-census review boundary below.

### Nahum continuation, 2026-11-02

All six Nahum portions were read, including four additional original images
and the shared pages JC 550 and BHL 834. Native-pixel crops verify both page
edges, the word at 1:3 and the book boundaries. Printed footers were checked
separately from scan filenames. No image or crop is stored in this repository.

| Edition | Scan filename | Observed printed page | Nahum interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `550-Mi-Na.jpg` | 550 | 1:1 atom 1 through 1:6 atom 1 |
| `jc1` | `551-Na.jpg` | 551 | 1:6 atom 2 through 3:11 atom 9 |
| `jc1` | `552-Na-Hb.jpg` | 552 | 3:11 atom 10 through 3:19 atom 18 |
| `bhl` | `0834-Mi-Na.jpg` | 834 | 1:1 atom 1 through 2:3 atom 1 |
| `bhl` | `0835-Na.jpg` | 835 | 2:3 atom 2 through 3:11 atom 8 |
| `bhl` | `0836-Na-Hb.jpg` | 836 | 3:11 atom 9 through 3:19 atom 18 |

JC 550 ends with only the first atom of 1:6, `לפני`; JC 552 begins with only
the last atom of 3:11, `מאויב`. BHL 835 and 836 begin with continuations of
2:3 and 3:11 although their headers start at 2:4 and 3:12 respectively.
The Habakkuk portions of JC 552 and BHL 836 were uncensused at this checkpoint;
the following continuation completed them.

Nahum 1:3 contains a special-letter word wrapper (`מ:אות-מיוחדת-במילה`)
with a nested small-letter template (`מ:אות-ק`). Their documented Scripture
parameter is parameter 1. The reader validates these two explicit schemas and
recurses into that parameter, joining `ב`, `ס` and `ופה` within one atom,
`בסופה`. Descriptive fields contribute no text. This follows the existing
MAM projection definitions and agrees with the independent MAM-simple
`slh-word` / `letter-small` structure. It makes no inference about the printed
letter's size. Other unfamiliar templates and multi-atom ketiv/qere still
refuse explicitly.

BHL 834 ends with the first `כי` of 2:3. That verse contains two occurrences,
so a one-word cue fails the uniqueness check. Its visible preceding words
give the unique stop cue `אמץ כח מאד כי`, crossing 2:2 into 2:3. The locator
now supports such cross-verse cues: a start reference anchors the phrase's
first atom, and a stop reference anchors its last. Both complete phrase spans
must remain inside the recorded page. No new record fields or exception to
unique matching is needed. Phrase lookup anchors its first atom's verse,
so `lookup Nahum 2:2 "אמץ כח מאד כי" --edition bhl` returns 834;
`lookup Nahum 2:3 "כי" --edition bhl` still refuses as ambiguous.

All 47 Nahum verses and 558 atoms agree with the independent MAM-simple
export. Six focused tests passed, now checking every adopted source cue as a
full position span. Direct checks cover all four within-verse splits,
qualified lookups, the intact one-atom word at 1:3, a phrase crossing a page
break, the cross-verse stop cue, repeated short-phrase refusal and idempotent
census regeneration. The full suite and mega were not run under the ordinary
focused-check policy. The large-census review boundary below still applies.

### Habakkuk continuation, 2026-11-02

All five Habakkuk portions were read, including three additional original
images and the shared pages JC 552 and BHL 836. Native-pixel crops verify
each start/stop cue and the book boundaries. Printed footers were checked
separately from scan filenames. No image or crop is stored in this repository.

| Edition | Scan filename | Observed printed page | Habakkuk interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `552-Na-Hb.jpg` | 552 | 1:1 atom 1 through 2:7 atom 9 |
| `jc1` | `553-Hb-Ts.jpg` | 553 | 2:8 atom 1 through 3:19 atom 11 |
| `bhl` | `0836-Na-Hb.jpg` | 836 | 1:1 atom 1 through 1:13 atom 6 |
| `bhl` | `0837-Hb.jpg` | 837 | 1:13 atom 7 through 2:18 atom 2 |
| `bhl` | `0838-Hb.jpg` | 838 | 2:18 atom 3 through 3:19 atom 11 |

JC's break falls between the complete verses 2:7 and 2:8. BHL 837 and 838
begin with continuations of 1:13 and 2:18 although their headers start at
1:14 and 2:19 respectively. BHL 837 ends with just `מה הועיל`, the first two
atoms of 2:18. The Zephaniah portion of JC 553 was uncensused at this
checkpoint; the following continuation completed it.

The existing reader projects all 56 Habakkuk verses and 671 atoms without a
new template rule; the complete stream agrees with the independent MAM-simple
export. Six focused tests passed. Direct checks cover both BHL within-verse
splits and their unique phrase hits, JC's complete-verse boundary, a phrase
spanning a BHL page break, and idempotent census regeneration in both editions.
The full suite and mega were not run under the ordinary focused-check policy.
The large-census review boundary below still applies.

### Zephaniah continuation, 2026-11-03

All six Zephaniah portions were read, including five additional original
images and the shared page JC 553. Native-pixel crops verify both page edges,
book transitions and the adjacent words at 3:15. Printed footers were checked
separately from scan filenames. No image or crop is stored in this repository.
The internal book ID used by the commands and index is `Tsefaniah`.

| Edition | Scan filename | Observed printed page | Zephaniah interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `553-Hb-Ts.jpg` | 553 | 1:1 atom 1 through 1:1 atom 14 |
| `jc1` | `554-Ts.jpg` | 554 | 1:1 atom 15 through 2:11 atom 16 |
| `jc1` | `555-Ts-Hg.jpg` | 555 | 2:12 atom 1 through 3:20 atom 21 |
| `bhl` | `0839-Ts.jpg` | 839 | 1:1 atom 1 through 2:2 atom 2 |
| `bhl` | `0840-Ts.jpg` | 840 | 2:2 atom 3 through 3:7 atom 1 |
| `bhl` | `0841-Ts-Hg.jpg` | 841 | 3:7 atom 2 through 3:20 atom 21 |

JC 553 ends within the opening verse, after `חזקיה`; JC 554 continues with
`בימי`. JC's next break is between the complete verses 2:11 and 2:12.
BHL 840 and 841 continue 2:2 and 3:7 although their headers start at 2:3 and
3:8 respectively. BHL 840 ends with only the first atom of 3:7, `אמרתי`.
The Haggai portions of JC 555 and BHL 841 were uncensused at this checkpoint;
the following continuation completed them.

The existing maintained rules in `mb_cmn/template_names.py`'s
`NO_ATOM_TMPL_NAMES` and `hkq_cmn/qere_projection.py` establish that the
explicit paseq template `מ:פסק` separates its neighbors without contributing
an atom. The scan-page reader validates its parameterless schema and emits
a separator, just as for its supported legarmeh marker. This preserves
`ישראל` and `יהוה` as distinct atoms 7 and 8 at 3:15; dropping the template
without a separator would join them. The independent MAM-simple export
represents the boundary as `lp-paseq`. This adopts the maintained convention;
it introduces no new editorial interpretation or generic template fallback.

All 53 Zephaniah verses and 767 atoms agree with MAM-simple. Six focused
tests passed. Direct checks cover all three within-verse splits, unique
phrase hits, JC's whole-verse boundary, a phrase crossing a BHL page break,
the intact adjacent words at 3:15 in both editions, and idempotent census
regeneration. The full suite and mega were not run under the ordinary
focused-check policy. The large-census review boundary below still applies.

### Haggai continuation, 2026-11-03

All seven Haggai portions were read, including five additional original
images and the shared pages JC 555 and BHL 841. Native-pixel crops verify
both page edges and the book transitions. Printed footer numbers were checked
separately from scan filenames. No image or crop is stored in this repository.

| Edition | Scan filename | Observed printed page | Haggai interval in MAM atom positions |
|---|---|---|---|
| `jc1` | `555-Ts-Hg.jpg` | 555 | 1:1 atom 1 through 1:2 atom 8 |
| `jc1` | `556-Hg.jpg` | 556 | 1:2 atom 9 through 2:12 atom 14 |
| `jc1` | `557-Hg-Zc.jpg` | 557 | 2:12 atom 15 through 2:23 atom 20 |
| `bhl` | `0841-Ts-Hg.jpg` | 841 | 1:1 atom 1 through 1:2 atom 4 |
| `bhl` | `0842-Hg.jpg` | 842 | 1:2 atom 5 through 2:4 atom 14 |
| `bhl` | `0843-Hg.jpg` | 843 | 2:4 atom 15 through 2:22 atom 13 |
| `bhl` | `0844-Hg-Zc.jpg` | 844 | 2:22 atom 14 through 2:23 atom 20 |

All five internal page breaks split verses. BHL 842, 843 and 844 continue
1:2, 2:4 and 2:22 although their headers begin at 1:3, 2:5 and 2:23.
The ending formula `נאם יהוה צבאות` occurs twice in 2:23, so the observed
stop cue is the longer unique `כי בך בחרתי נאם יהוה צבאות`. The shorter
formula still refuses as an ambiguous phrase query. The Zechariah portions
of JC 557 and BHL 844 were uncensused at that checkpoint.

The existing reader projects all 38 Haggai verses and 600 atoms without a
new rule; the entire stream agrees with MAM-simple. Six focused tests passed.
Direct checks cover every split, unique phrase hits, a phrase crossing a
page break, refusal of the repeated short formula, and idempotent census
regeneration in both editions. The full suite and mega were not run under
the ordinary focused-check policy. The large-census review boundary below
still applies.

The next natural adjacent group at that checkpoint was Zechariah and Malachi,
completing the forward end of the Twelve. Grouping their shared images does
not change the whole-book adoption gates or per-page native verification.

### Zechariah continuation, 2026-11-03

All twenty-one Zechariah portions were read in native edge bands, including
nineteen additional original images and the shared Haggai pages JC 557 and
BHL 844. Book-transition layouts were checked in full-page previews. Printed
footers were checked independently of filenames. Each cue is unique in the
whole book and lies entirely within its source page. The private evidence
retains source hashes, dimensions, crop coordinates and navigation pointers.

| Edition | Scan filename | Observed printed page | Zechariah interval in MAM atom positions |
|---|---|---:|---|
| JC | `557-Hg-Zc.jpg` | 557 | 1:1 atom 1 through 1:12 atom 13 |
| JC | `558-Zc.jpg` | 558 | 1:12 atom 14 through 3:7 atom 6 |
| JC | `559-Zc.jpg` | 559 | 3:7 atom 7 through 5:11 atom 12 |
| JC | `560-Zc.jpg` | 560 | 6:1 atom 1 through 7:14 atom 3 |
| JC | `561-Zc.jpg` | 561 | 7:14 atom 4 through 8:23 atom 12 |
| JC | `562-Zc.jpg` | 562 | 8:23 atom 13 through 10:12 atom 3 |
| JC | `563-Zc.jpg` | 563 | 10:12 atom 4 through 12:8 atom 17 |
| JC | `564-Zc.jpg` | 564 | 12:8 atom 18 through 14:10 atom 22 |
| JC | `565-Zc-Ma.jpg` | 565 | 14:10 atom 23 through 14:21 atom 24 |
| BHL | `0844-Hg-Zc.jpg` | 844 | 1:1 atom 1 through 1:14 atom 1 |
| BHL | `0845-Zc.jpg` | 845 | 1:14 atom 2 through 2:17 atom 2 |
| BHL | `0846-Zc.jpg` | 846 | 2:17 atom 3 through 4:9 atom 6 |
| BHL | `0847-Zc.jpg` | 847 | 4:9 atom 7 through 6:5 atom 2 |
| BHL | `0848-Zc.jpg` | 848 | 6:5 atom 3 through 7:7 atom 18 |
| BHL | `0849-Zc.jpg` | 849 | 7:8 atom 1 through 8:12 atom 16 |
| BHL | `0850-Zc.jpg` | 850 | 8:12 atom 17 through 9:8 atom 4 |
| BHL | `0851-Zc.jpg` | 851 | 9:8 atom 5 through 10:10 atom 5 |
| BHL | `0852-Zc.jpg` | 852 | 10:10 atom 6 through 11:17 atom 10 |
| BHL | `0853-Zc.jpg` | 853 | 11:17 atom 11 through 13:2 atom 6 |
| BHL | `0854-Zc.jpg` | 854 | 13:2 atom 7 through 14:10 atom 7 |
| BHL | `0855-Zc-Ma.jpg` | 855 | 14:10 atom 8 through 14:21 atom 24 |

Seven of eight JC breaks and ten of eleven BHL breaks split verses. The BHL
headers omit the opening continuations on 845 (1:14), 846 (2:17), 847 (4:9),
848 (6:5), 850 (8:12), 851 (9:8), 852 (10:10), 853 (11:17), 854 (13:2) and
855 (14:10); 849 begins at 7:8, matching its header. Headers alone would miss
these first atoms. JC 565 and BHL 855 also open Malachi, uncensused at that
checkpoint; the following continuation completed those portions.

The existing reader projects all 211 verses and 3,127 atoms, independently
matching MAM-simple. Six focused tests passed (30 deselected); the catalog
check reports five editions, 5,720 pages, 205 records and two segments without
problems. Direct checks cover all seventeen within-verse breaks, qualified and
cross-page phrase lookup, refusal of the twice-occurring word in 14:9,
and idempotent regeneration. Initial transcription slips and a repeated short
cue were rejected before any index write; lengthened, source-visible cues
resolve uniquely. No projection rule or record field changed.

### Malachi continuation, 2026-11-03

All eight Malachi portions were read in native edge bands and full-page
previews, including six additional images and shared JC 565/BHL 855.
Printed footers and BHL headers were checked separately from filenames.
Private evidence retains exact original identities, hashes and crop boxes.

| Edition | Scan filename | Observed printed page | Malachi interval in MAM atom positions |
|---|---|---:|---|
| JC | `565-Zc-Ma.jpg` | 565 | 1:1 atom 1 through 1:12 atom 11 |
| JC | `566-Ma.jpg` | 566 | 1:13 atom 1 through 3:5 atom 10 |
| JC | `567-Ma.jpg` | 567 | 3:5 atom 11 through 3:24 atom 15 |
| BHL | `0855-Zc-Ma.jpg` | 855 | 1:1 atom 1 through 1:3 atom 8 |
| BHL | `0856-Ma.jpg` | 856 | 1:3 atom 9 through 2:5 atom 8 |
| BHL | `0857-Ma.jpg` | 857 | 2:5 atom 9 through 3:4 atom 4 |
| BHL | `0858-Ma.jpg` | 858 | 3:4 atom 5 through 3:21 atom 15 |
| BHL | `0859-Ma.jpg` | 859 | 3:22 atom 1 through 3:24 atom 15 |

One of two JC breaks and three of four BHL breaks split verses. BHL 856,
857 and 858 begin with continuations of 1:3, 2:5 and 3:4; their headers
start at 1:4, 2:6 and 3:5. BHL 859 begins at 3:22, matching its header.

Malachi 3:22 contains the explicit large-letter template `מ:אות-ג` within
`SLH_WORD`. Its maintained `IN_WORD_TMPL_NAMES` membership and exact
parameter-1 schema establish its contribution. The reader now validates and
recurses into that parameter, preserving the zayin in `זכרו` as one atom.
The independent MAM-simple comparison handles its explicit `letter-large`
node and agrees on all 55 verses and 876 atoms. This projection says nothing
about a source edition's printed letter size.

BHL 859 prints 3:23 again, unnumbered, after 3:24. Its record's stop cue
marks the canonical 3:24 ending, and its note preserves the following
repetition. Both occurrences of 3:23 are on the same page, so verse-to-page
lookup remains exact; this index has no occurrence coordinates. Following
`mb_cmn/mam_json_verses.py`, the independent comparison explicitly validates
and excludes MAM-simple's `good-ending` node from the final verse's atoms.
It contributes no additional verse or atom interval. JC 567 ends with 3:24
without that following repetition.

Six focused tests pass (30 deselected), including complete independent atom
comparison; the catalog check reports five editions, 5,720 pages, 211 records
and two segments without problems. Direct checks cover all four within-verse
splits, qualified and cross-page lookups, ambiguous-phrase refusal, intact
3:22 word/lookup, both final verses and idempotent regeneration. Black and
whitespace checks pass. The full suite and mega were not run under the
ordinary focused-check policy. No main integration or deployment occurred.
The large-census review boundary below still applies.

### Amos continuation, 2026-11-03

All 15 Amos portions were read in native edge bands, including
13 additional images. Full-page previews were used at book
transitions. Printed footer numbers and BHL running headers were read
separately from filenames. Exact original identities, hashes and crop boxes
are retained privately.

| Edition | Scan filename | Observed printed page | Amos interval in MAM atom positions |
|---|---|---:|---|
| JC | `539-Jl-A.jpg` | 539 | 1:1 atom 1 through 1:14 atom 10 |
| JC | `540-A.jpg` | 540 | 1:14 atom 11 through 3:12 atom 13 |
| JC | `541-A.jpg` | 541 | 3:12 atom 14 through 5:11 atom 17 |
| JC | `542-A.jpg` | 542 | 5:11 atom 18 through 7:2 atom 10 |
| JC | `543-A.jpg` | 543 | 7:2 atom 11 through 8:13 atom 3 |
| JC | `544-A-O.jpg` | 544 | 8:13 atom 4 through 9:15 atom 14 |
| BHL | `0817-Jl-A.jpg` | 817 | 1:1 atom 1 through 1:10 atom 2 |
| BHL | `0818-A.jpg` | 818 | 1:10 atom 3 through 2:13 atom 7 |
| BHL | `0819-A.jpg` | 819 | 2:13 atom 8 through 4:2 atom 9 |
| BHL | `0820-A.jpg` | 820 | 4:2 atom 10 through 5:6 atom 14 |
| BHL | `0821-A.jpg` | 821 | 5:7 atom 1 through 6:2 atom 17 |
| BHL | `0822-A.jpg` | 822 | 6:2 atom 18 through 7:10 atom 11 |
| BHL | `0823-A.jpg` | 823 | 7:10 atom 12 through 8:11 atom 17 |
| BHL | `0824-A.jpg` | 824 | 8:11 atom 18 through 9:14 atom 2 |
| BHL | `0825-A-O.jpg` | 825 | 9:14 atom 3 through 9:15 atom 14 |

All five JC breaks and seven of eight BHL breaks split verses. BHL headers omit opening continuations on 818 (1:10), 819 (2:13), 820 (4:2), 822 (6:2), 823 (7:10), 824 (8:11) and 825 (9:14). BHL 821 begins at 5:7, matching its header. Shared JC 539/BHL 817 still contain uncensused Joel; the Obadiah portions of JC 544/BHL 825 were already indexed.

No new projection rule was needed; all 146 verses and 2,042 atoms match independent MAM-simple.

Six focused tests passed (30 deselected), including complete independent atom comparison. Direct checks cover all twelve within-verse breaks, qualified and cross-page lookup, repeated-atom refusal and idempotent adoption. Cue checks rejected three transcription slips before the first index write; the corrected source-visible cues are unique across the book. The full suite and mega were omitted under the ordinary focused-check policy. The catalog check reports five editions, 5,720 pages, 224 records and two segments without problems. No main integration or deployment occurred. The large-census review boundary below still applies.

### Joel continuation, 2026-11-03

All 9 Joel portions were read in native edge bands, including
7 additional images. Full-page previews were used at book
transitions. Printed footer numbers and BHL running headers were read
separately from filenames. Exact original identities, hashes and crop boxes
are retained privately.

| Edition | Scan filename | Observed printed page | Joel interval in MAM atom positions |
|---|---|---:|---|
| JC | `536-Ho-Jl.jpg` | 536 | 1:1 atom 1 through 1:3 atom 1 |
| JC | `537-Jl.jpg` | 537 | 1:3 atom 2 through 2:15 atom 5 |
| JC | `538-Jl.jpg` | 538 | 2:15 atom 6 through 4:10 atom 1 |
| JC | `539-Jl-A.jpg` | 539 | 4:10 atom 2 through 4:21 atom 7 |
| BHL | `0813-Ho-Jl.jpg` | 813 | 1:1 atom 1 through 1:6 atom 11 |
| BHL | `0814-Jl.jpg` | 814 | 1:6 atom 12 through 2:8 atom 9 |
| BHL | `0815-Jl.jpg` | 815 | 2:8 atom 10 through 2:27 atom 7 |
| BHL | `0816-Jl.jpg` | 816 | 2:27 atom 8 through 4:16 atom 6 |
| BHL | `0817-Jl-A.jpg` | 817 | 4:16 atom 7 through 4:21 atom 7 |

All three JC breaks and all four BHL breaks split verses. JC 536 ends at 1:3 atom 1, and JC 538 ends at 4:10 atom 1; each following page continues that verse. BHL headers omit opening continuations on 814 (1:6), 815 (2:8), 816 (2:27) and 817 (4:16). JC 536 and BHL 813 still contain uncensused Hosea; Amos portions on JC 539/BHL 817 are already indexed.

No new projection rule was needed; all 73 verses and 957 atoms match independent MAM-simple.

Six focused tests passed (30 deselected), including complete independent atom comparison. Direct checks cover all seven within-verse breaks, qualified and cross-page lookup, repeated-atom refusal and idempotent adoption. The cue check rejected a missing initial vav before any index write; the corrected source-visible cue is unique. The full suite and mega were omitted under the ordinary focused-check policy. The catalog check reports five editions, 5,720 pages, 231 records and two segments without problems. No main integration or deployment occurred. The large-census review boundary below still applies.

### Hosea continuation, 2026-11-03

All 15 Hosea portions were read in native edge bands, including
13 additional images. Full-page previews were used at book
transitions. Printed footer numbers and BHL running headers were read
separately from filenames. Exact original identities, hashes and crop boxes
are retained privately.

| Edition | Scan filename | Observed printed page | Hosea interval in MAM atom positions |
|---|---|---:|---|
| JC | `531-Ho.jpg` | 531 | 1:1 atom 1 through 2:19 atom 1 |
| JC | `532-Ho.jpg` | 532 | 2:19 atom 2 through 5:1 atom 17 |
| JC | `533-Ho.jpg` | 533 | 5:1 atom 18 through 7:13 atom 5 |
| JC | `534-Ho.jpg` | 534 | 7:13 atom 6 through 9:17 atom 9 |
| JC | `535-Ho.jpg` | 535 | 10:1 atom 1 through 12:8 atom 6 |
| JC | `536-Ho-Jl.jpg` | 536 | 12:9 atom 1 through 14:10 atom 16 |
| BHL | `0805-Ho.jpg` | 805 | 1:1 atom 1 through 2:10 atom 8 |
| BHL | `0806-Ho.jpg` | 806 | 2:10 atom 9 through 3:5 atom 2 |
| BHL | `0807-Ho.jpg` | 807 | 3:5 atom 3 through 5:4 atom 2 |
| BHL | `0808-Ho.jpg` | 808 | 5:4 atom 3 through 7:3 atom 3 |
| BHL | `0809-Ho.jpg` | 809 | 7:3 atom 4 through 8:13 atom 10 |
| BHL | `0810-Ho.jpg` | 810 | 8:13 atom 11 through 10:3 atom 15 |
| BHL | `0811-Ho.jpg` | 811 | 10:4 atom 1 through 11:10 atom 11 |
| BHL | `0812-Ho.jpg` | 812 | 11:11 atom 1 through 13:10 atom 12 |
| BHL | `0813-Ho-Jl.jpg` | 813 | 13:10 atom 13 through 14:10 atom 16 |

Three of five JC breaks and six of eight BHL breaks split verses. BHL headers omit opening continuations on 806 (2:10), 807 (3:5), 808 (5:4), 809 (7:3), 810 (8:13) and 813 (13:10); 811 and 812 match their opening references, 10:4 and 11:11. All shared Joel portions are already indexed, so every listed book on the Twelve's source images is now censused.

The explicit פפ rule follows maintained WHITESPACE_TMPL_NAMES/NO_ATOM_TMPL_NAMES and the current optional parameter-1 schema. It emits a separator and excludes the annotation; independent MAM-simple represents this as spi-pe2. Hosea 1:2 retains בהושע and ויאמר as separate atoms 4 and 5, with 21 atoms and no annotation words. All 197 verses and 2,381 atoms agree with independent MAM-simple. No generic fallback or new editorial convention was introduced.

Six focused tests passed (30 deselected), including complete independent atom comparison. Direct checks cover all nine within-verse breaks, qualified and cross-page lookup, repeated-atom refusal and idempotent adoption. The annotated-break check confirms separate adjacent words, excludes annotation atoms, and refuses an unknown template name or invalid parameter schema. Black and catalog/whitespace checks passed. Cue checks rejected transcription slips before any index write. The full suite and mega were omitted under the ordinary focused-check policy. The catalog check reports five editions, 5,720 pages, 244 records and two segments without problems. No main integration or deployment occurred. The large-census review boundary below still applies.

**Phase 0 — survey and tracked inventory. DONE, 2026-08-07.** The code is
`py/main_scan_pages.py` (`survey`, `check`) over `py/scan_pages/`, with the lint at
`py/tests/test_scan_pages_index.py`. Re-derive everything below with:

```
./.venv/Scripts/python.exe py/main_scan_pages.py survey
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
./.venv/Scripts/python.exe py/main_scan_pages.py check
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
`lookup <bk39> <ch>:<v>[t|e] [<phrase>]` (exact-or-refuse) as a library resolution returning
records, behind a very short `main` printing one `file:///` link per edition on stdout, and
`census` (page-edge phrases in, atoms out,
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

**Cost probe, 2026-09-10: ten koren pages took 29 seconds each of session wall-clock, and
all 20 page edges located exactly, every page meeting the next at adjacent atoms.** Ben's
ask that day: *"a test run of the analysis of perhaps 10 pages of Koren, to see how slow
this process is, where by 'process' I mean identifying what content each page starts and
stops with."* A worktree session running Claude Opus 5, at MAM-basics `f92c061c`, ran the
method below on koren's `A1-G-001.jpg` to `A1-G-010.jpg`, which have Genesis 1:1 to 8:11
between them, one page at a time and deliberately unpipelined, so that each part of a page's
cost could be timed apart. It built no Phase 1 tooling and wrote no record into
`in/scan-pages/koren.json`: these paragraphs and their two tables are its whole tracked
output. Its timing and locating scripts were throwaway, in that worktree's `.novc/`, and went
with it, so each figure is stated with what re-establishes it.

The method, per page, has three steps:

1. **Render the two edge bands** with the tracked renderer, one command per band, run from
   the repo root:
   ```
   ./.venv/Scripts/python.exe py/main_edition_transcription.py scan-page "Koren Classic Tanakh" A1-G-002 --width 1400 --crop 0.05 0.03 0.95 0.19 --name koren-probe-A1-G-002-top
   ./.venv/Scripts/python.exe py/main_edition_transcription.py scan-page "Koren Classic Tanakh" A1-G-002 --width 1400 --crop 0.05 0.80 0.95 0.96 --name koren-probe-A1-G-002-bottom
   ```
   Each band comes out 1400 × 364 pixels: the running head and about four text lines at the
   top, about four text lines and the footer at the bottom. The fractions were chosen once,
   from a full-page render of `A1-G-001.jpg`, and fit all ten pages; that render was setup
   and is in no figure below.
2. **Read both bands with the `Read` tool and transcribe six atoms at each edge**, letters
   only, the atoms of a maqaf compound taken separately.
3. **Locate each phrase among Genesis's 20,613 atoms, demanding a position unique in the
   book.** The atoms are the repo's: each verse's text cell, read by
   `mb_cmn/read_books_from_mam_parsed_plus.py` from `mb_cmn.paths.mam_parsed_path()`,
   flattened by `hkq_cmn/mam_plus_verse_data._collect_text_fragments`, split by
   `hkq_cmn/qere_projection.TOKEN_SPLIT_RE` and stripped to the letters alef to tav. That
   collector takes the qere at a ketiv/qere, so the probe matched the ketiv too, from a copy
   of each verse tree with every ketiv/qere choice flipped. Genesis's one ketiv/qere whose
   two sides differ in atom count, at 30:11, the ketiv בגד against the qere בא גד, is far
   outside these pages.

**Per page, in seconds**, from timestamps the probe's scripts logged at the start and end of
each render and each locate:

| page | cloud-only | render | read and transcribe | locate | turn between pages | wall |
| --- | --- | --- | --- | --- | --- | --- |
| `A1-G-001.jpg` | no | 0.7 | 13.4 | 0.2 | 7.3 | 21.6 |
| `A1-G-002.jpg` | yes | 1.4 | 19.1 | 0.2 | 6.7 | 27.3 |
| `A1-G-003.jpg` | yes | 1.3 | 11.8 | 0.2 | 6.3 | 19.6 |
| `A1-G-004.jpg` | yes | 1.5 | 15.0 | 0.2 | 6.0 | 22.7 |
| `A1-G-005.jpg` | yes | 1.2 | 14.5 | 0.2 | 7.3 | 23.1 |
| `A1-G-006.jpg` | yes | 1.1 | 17.9 | 0.2 | 7.4 | 26.6 |
| `A1-G-007.jpg` | yes | 1.0 | 22.3 | 0.2 | 14.4 | 37.9 |
| `A1-G-008.jpg` | yes | 1.1 | 17.4 | 18.9 | 9.2 | 46.6 |
| `A1-G-009.jpg` | yes | 1.2 | 17.4 | 0.2 | 11.3 | 30.1 |
| `A1-G-010.jpg` | yes | 1.2 | 67.7 | 0.2 | — | — |

The five timed columns:

1. **render**: the render step's run — a full read of the JPG's bytes, which on a cloud-only
   OneDrive placeholder is the download (0.2–0.6 s, mean 0.4 s over the nine cloud-only
   pages), then the two `scan-page` subprocesses (0.8 s together).
2. **read and transcribe**: from the render's end to the first locate's start — the two band
   reads and the transcription, with the model turns and tool-call round trips they take.
3. **locate**: from the first locate's start to the last locate's end. The script's run is
   0.2 s a round; `A1-G-008.jpg`'s 18.9 s is one lengthening round, almost all of it the
   model turn between its two rounds.
4. **turn between pages**: from the last locate's end to the next render's start — the model
   reading the locate result and issuing the next page's render.
5. **wall**: from one render's start to the next — the four above together.

Two rows stay out of every mean below: (1) `A1-G-001.jpg`, whose content had been seen in the
setup render before its timed run, and (2) `A1-G-010.jpg`, whose read-and-transcribe figure
includes the model writing the probe's analysis script in the same turn — a contamination the
probe session introduced and could not undo — and which has no successor to end its wall.

**The model's turns dominate, at about 95% of a page's cost; rendering is 4% of it.** Over
the eight clean pages, `A1-G-002.jpg` to `A1-G-009.jpg`, the wall averages 29.2 s (median
27.0 s, range 19.6–46.6 s): render 1.2 s (4%), read and transcribe 16.9 s (58%), locate
2.5 s (9%, nearly all of it `A1-G-008.jpg`'s lengthening turn) and the turn between pages
8.6 s (29%). The two scripts together run about 1.4 s a page, so making rendering or
locating faster buys almost nothing; a speed-up has to cut the number or the length of the
model's turns per page. Nine of the ten scans were cloud-only OneDrive placeholders when the
probe began, each downloaded by its first read and left local, and none failed. A census
therefore brings every page it reads onto the local disk: koren's 1,332 files total 2.2 GB,
measured 2026-09-10 with
`Get-ChildItem -LiteralPath "C:/Users/BenDe/OneDrive/Documents/ScansOfBooks/Koren Classic Tanakh" -File | Measure-Object -Property Length -Sum`.

**Accuracy, beside the speed — nothing wrong was found:**

1. **Every transcription was letter-exact.** All 20 phrases matched MAM as first
   transcribed: 124 atoms in all, and one wrong letter in any of them would have made its
   phrase match nowhere.
2. **All nine neighbouring pairs meet at adjacent atoms**, each shown in the last column of
   the table below.
3. **The seeded start record re-derived**: `A1-G-001.jpg`'s start phrase located at 1:1
   atom 1, the start `survey` had seeded.
4. **No page needed a second image read.** Letters were legible at 1400 pixels in all 20
   bands.
5. **One phrase of the 20 needed lengthening, and more atoms from the same band did it.**
   The six start atoms of `A1-G-008.jpg`, את שם את חם ואת יפת, are in Genesis at 6:10 as
   well as at 5:32; two more atoms pinned it, at the cost of one extra locate round and no
   second image read. Counted from a first try of three atoms instead of six, two of the 20
   would have needed lengthening — that one, to seven atoms, and the stop of
   `A1-G-009.jpg`, to four, its last three atoms אל נח אל being at 7:9 as well as at 7:15.
   The shortest unique phrase at the 20 edges was one atom 4 times, two 9 times, three 5
   times, four once and seven once. Book-wide uniqueness is a stricter demand than a start
   edge needs: the stop of `A1-G-007.jpg` already fixes the start of `A1-G-008.jpg` at the
   next atom, so a census that checks each start against the previous record's stop needs
   the start phrase only as verification.

**The ten records, for Phase 1 to re-derive.** Each phrase is as transcribed, letters only.
Once `census` exists, feeding it these phrases must give back these positions, and a mismatch
is a finding:

| page | start phrase | start | stop phrase | stop | atoms | meets the previous page |
| --- | --- | --- | --- | --- | --- | --- |
| `A1-G-001.jpg` | בראשית ברא אלהים את השמים ואת | 1:1 atom 1 | רקיע השמים ויברא אלהים את התנינם | 1:21 atom 4 | 247 | — |
| `A1-G-002.jpg` | הגדלים ואת כל נפש החיה הרמשת | 1:21 atom 5 | את האדמה ואד יעלה מן הארץ והשקה | 2:6 atom 5 | 261 | adjacent |
| `A1-G-003.jpg` | את כל פני האדמה וייצר יהוה | 2:6 atom 6 | עשה יהוה אלהים ויאמר אל האשה אף | 3:1 atom 14 | 268 | adjacent |
| `A1-G-004.jpg` | כי אמר אלהים לא תאכלו מכל | 3:1 atom 15 | אל האדמה כי ממנה לקחת כי | 3:19 atom 12 | 258 | adjacent |
| `A1-G-005.jpg` | עפר אתה ואל עפר תשוב ויקרא | 3:19 atom 13 | יקם וישם יהוה לקין אות לבלתי | 4:15 atom 14 | 263 | adjacent |
| `A1-G-006.jpg` | הכות אתו כל מצאו ויצא קין | 4:15 atom 15 | בנים ובנות ויהיו כל ימי אנוש | 5:11 atom 4 | 273 | adjacent |
| `A1-G-007.jpg` | חמש שנים ותשע מאות שנה וימת | 5:11 atom 5 | בן חמש מאות שנה ויולד נח | 5:32 atom 8 | 239 | adjacent |
| `A1-G-008.jpg` | את שם את חם ואת יפת ויהי כי | 5:32 atom 9 | רוח חיים מתחת השמים כל אשר | 6:17 atom 19 | 246 | adjacent |
| `A1-G-009.jpg` | בארץ יגוע והקמתי את בריתי אתך | 6:17 atom 20 | כל כנף ויבאו אל נח אל | 7:15 atom 4 | 270 | adjacent |
| `A1-G-010.jpg` | התבה שנים שנים מכל הבשר אשר | 7:15 atom 5 | היונה מן התבה ותבא אליו היונה | 8:11 atom 3 | 262 | adjacent |

Atoms per page run 239–273, mean 259: a first measurement for the atoms-per-page band that
the Design's last lint wants. Three of the nine page breaks fall inside a maqaf compound:
(1) between `A1-G-004.jpg` and `A1-G-005.jpg`, the compound כי־עפר; (2) between
`A1-G-008.jpg` and `A1-G-009.jpg`, אשר־בארץ; (3) between `A1-G-009.jpg` and `A1-G-010.jpg`,
אל־התבה. The records' atom-level positions express those three edges, where positions
counted in chanted words could not.

**Extrapolated at the clean mean of 29.2 s a page, koren's 1,240 body pages take 10.1 hours
of session wall-clock, and the five editions' ~5,100 pages take 41.4 hours** — about 9.3 and
38 hours at the median. So a census of koren alone is well past an afternoon and far short of
a month, and all five editions come to about a working week of session time. Three things
bound how far those figures travel:

1. **These ten pages are a best case.** They are one-column prose in koren's plainest
   layout, from Genesis 1–8, which a model knows about as well as any text, and the
   letter-exact result above may owe something to that. The layouts of the poetic verses and
   of the specially laid-out songs, pages holding two books, the Decalogue pages and the
   other four editions' layouts are all still to come, and each can only raise the figure.
2. **One session cannot hold a whole edition.** Each page put two band images into the
   session's context, about 680 tokens each by the width × height / 750 estimate for a
   1400 × 364 image, so koren's 1,240 pages would put some 1.7 million tokens of images
   alone into one session. Phase 2's book-sized chunks therefore also bound a session's
   context, and each chunk adds a session's start-up to the hours above.
3. **Two levers were not tried.** The turn between pages exists because the probe ran
   unpipelined for timing: rendering a whole book's bands up front, at about 1.2 s a page and
   off the critical path, and reading several pages' bands in each model turn would remove
   most of it. Parallel sessions divide the elapsed time, though not the total. Phase 1
   should time a batched loop before Phase 2 is planned around the hours above.

**Re-measure rather than trust any figure here.** Each depends on the model, the machine and
OneDrive's state on 2026-09-10. The timings are re-measured by running the three steps on any
ten pages with a timestamp at the start and end of each render and each locate; the
positions, by locating the records table's phrases under step 3's atom definition, or, once
`census` exists, by feeding it the phrases.

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
2. **Scope beyond the Da'at Miqra subsection added on 2026-09-24:** the other ScansOfBooks folders
   (JC2 Companion, JC3, the
   readers, the loose PDFs) stay out of the index. Confirm.
