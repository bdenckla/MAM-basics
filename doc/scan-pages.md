# Scan-pages index: bring up five scanned editions at a bcv

State: runbook

Ben's ask, 2026-08-06: *"index important editions I have scanned (in 'ScansOfBooks') so
that, given a bcv (book-chapter-verse) reference, I can run a program that will bring up the
relevant page in all those editions (JC1 (Jerusalem crown), Koren, Simanim Tiqqun (if the
bcv is in Torah or haftarah), Simanim Tanakh, Dotan BHL)."*

This file is the single plan-and-findings document for the undertaking (per Ben's
one-tracked-plan rule). The current instructions are under [Using the index](#using-the-index). Dated
findings below record the work as it stood at each checkpoint. Its thin pointer issue is #349, filed on
2026-10-31.

## Using the index

Jerusalem Crown, Dotan BHL, Koren and Simanim Tanakh have ordinary-body
lookup for all 39 books. The Simanim Tiqqun covers the indexed Torah,
haftarah and megillah occurrences and two Decalogue appendix intervals.
Its unpointed D section is outside the lookup scope.

Run from the repository root with its Python environment. Lookup prints
local scan links. A verse across a page break returns both scans. To select
a page by its text, add a phrase that locates a unique atom position.
Append `t` or `e` to a Decalogue reference to select the named reading.

```powershell
./.venv/Scripts/python.exe py/main_scan_pages.py lookup Exodus 20:9
```

```powershell
./.venv/Scripts/python.exe py/main_scan_pages.py lookup Exodus 20:9e --edition jc1
```

Use `check` to validate the tracked catalogs and report page-density
advisories. It uses the tracked MAM text. Use `survey` to refresh the inventory
from the scan folder in `BOOK_SCANS_ROOT`, which defaults to
`$HOME/OneDrive/Documents/ScansOfBooks`. Refresh preserves the adopted page
intervals and refuses unreviewed changes to the text-page inventory. Use
`census` with a whole book's verified page-edge file to adopt a replacement
partition, following the [OCR workflow](#ocr-workflow-for-future-censuses).

## Status

The entries below describe the dated state of the research branch and catalogs.

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

- 2026-11-03, Ezekiel completion: the seven remaining opening portions
  (JC 481-483; BHL 733-736) are verified, completing chapters 1-4 (82 verses /
  1,213 atoms). Both unequal ketiv/qere cases now have explicit, closed
  one-written-word/two-qere-word mappings with indivisible page spans.
  All 119 Ezekiel portions are adopted: 49 JC and 70 BHL, covering all
  1,273 verses / 18,732 atoms per edition without gaps. The independent
  MAM-simple comparison agrees for every verse. All 116 prior interval
  observations relocate unchanged; four formerly partial pages are closed.
  The accepted total is 13 books / 2,323 verses per edition, with 231 completed
  portions and 130 unread seeds across the five catalogs (361 records).
  These results are on the isolated research branch; main is unchanged.

- 2026-11-03, Jeremiah completion: all 136 ordinary-body portions are now
  adopted on the isolated research branch after explicit approval: 56 JC
  and 80 BHL, covering 1,364 verses / 21,833 atoms per edition. Accepted
  lookup reaches 14 books / 3,687 verses per edition. The five catalogs
  contain 495 records: 367 completed portions and 128 unread seeds, with
  two body segments. Exact guarded mappings and source correspondences
  remain intact. No main integration or deployment occurred.

- 2026-11-04, approved Psalms adoption: **173 ordinary-body portions** are now
  adopted on the isolated research branch: **93 JC and 80 BHL**, covering all
  **150 psalms /2,527 verses /19,586 canonical atoms** per edition. Accepted
  coverage reaches **15 books /6,214 verses** per edition. The five catalogs
  contain **666 records: 540 completed portions and 126 unread seeds**, with two
  body segments. New records contain the approved relative filenames, printed
  page numbers, canonical ranges and consonantal boundary cues; every new note
  is null. No scans, crops or private research files are included.
  Persisted records exactly match the approved fields. Actual lookup passes all
  **56 split-verse cases** and seven CLI cases, including BHL145:18 on printed
  pages942-943 and phrase-qualified lookup on either side of that split. The
  maintained catalog check and ten focused index tests pass (one repetitive
  existing edge-query test deselected). The other three editions remain
  uncensused for Psalms. Main integration and
  deployment remain outside this research-branch adoption.

- 2026-11-06, **Ben adopted local letter-only OCR followed by visual review for
  all future scan indexing.** The trial found the verified break as the sole best
  suggestion for 22 of 23 joins, including all six joins in the fresh sample.
  The scan crops resolved the remaining tie. The workflow below supersedes
  reading and transcribing each scan before locating its boundaries in MAM.

- 2026-11-13, **Ben authorized local adoption of the five-edition patches on
  `codex/scan-index-laptop-20261104` in GitRepos3.** Koren and Simanim Tanakh
  have all 39 ordinary-body books. Jerusalem Crown and Dotan BHL now cover 27
  books each, from Jeremiah through the last body page. The Simanim Tiqqun
  lookup covers the verified Torah, haftarot, megillot and two appendices.
  See [Local adoption on 2026-11-13](#local-adoption-on-2026-11-13) for the
  catalog scope, lookup decisions and checks.
- 2026-11-14, the local main integration adopts the finished five-edition
  indexes, named lookups, inventory refresh and density review. See
  [Local main integration](#local-main-integration-2026-11-14).

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
  verse**, which returns each page covering part of the verse.
  A phrase-qualified lookup returns the page covering the phrase's first atom,
  so a phrase deep in a page-straddling verse brings up the later page.
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
  brings up the **body** Decalogue. The catalog records which strands the source
  review verifies in the running text. A **bcvs**, such as `Exodus 20:3t` or
  `Exodus 20:3e`, requests a named strand. The lookup selects the body scan
  when the running text carries that strand and the appendix when the appendix
  alone carries it. Named phrase lookup uses MAM's atom coordinates for the
  requested strand. The records use the same coordinates for both strands.
  bhl's `Appendix` ×5 and
  koren's `V` ×55 are natural places for a second strand's Decalogue to surface; Phase
  0's classification should look.
- **Records are captured from visually verified page-edge phrases, located in MAM's
  text.** Following Ben's 2026-11-06 decision, use the [OCR workflow](#ocr-workflow-for-future-censuses)
  to propose the first and last atoms on each page. Store letters-only `start_phrase`
  and `stop_phrase` evidence confirmed on the scans. `census` locates each phrase in
  MAM-parsed and derives the atom numbers. Lengthen a cue when needed to resolve its
  position uniquely. Each stored phrase can be checked against the scan and the text.
- **Finding the page is separated from showing it, and `lookup` prints its answer on
  stdout (Ben's decision, 2026-09-10).** The resolution — a bcv, an optional strand suffix
  and an optional phrase in; a page record or records out — is a library function under
  `py/scan_pages/` that renders nothing, writes nothing and opens nothing. Ben's reason,
  2026-09-10: *"the main point is to find the page, and that part of the code should be
  totally abstracted from what you do with the page, which might have multiple answers
  depending on the application."* **The first use of that library is deliberately a very
  short `main`** (Ben, 2026-09-10) that prints one `file:///` link per matching scan.
  Its shortness is the test that the separation holds:
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
  to the census). **Megillot.** The printed contents on `B04.jpg` list all five
  megillot. The Ecclesiastes opening is observed on `C367.jpg`, and its
  closing portion shares `C378.jpg` with the Esther opening. Esther ends
  on `C391.jpg`. Song of Songs opens on `C392.jpg` and ends on the shared page
  `C397.jpg`, where Ruth begins. Ruth ends on the shared page `C402.jpg`,
  where Lamentations begins. `C409.jpg` has Lamentations' final numbered
  verse 5:22 followed by another printed occurrence of 5:21. These inspected
  portions have parallel pointed and unpointed columns of running text.
  The local adoption verified all intervening body pages. **The notes supplement.**
  `C410.jpg` is blank, `C411.jpg` is the קומץ מנחת שי title, `C412.jpg` is blank,
  and running notes begin on
  `C413.jpg` under ספר בראשית / פרשת בראשית. Earlier reads recorded notes
  on `C415.jpg`, `C420.jpg` and `C440.jpg`. The catalog classifies `C413.jpg`
  through `C443.jpg` as the notes supplement. The notes and auxiliary pages
  are outside lookup.
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
  segments from disjointness for exactly that reason. The local adoption sections
  below record which named ranges have been verified.
- The four full-Tanakh catalogs use `segments` for runs of censused body pages.
  The Simanim Tiqqun uses `tiqqun.occurrences`. Each occurrence has a section,
  a book and a printed-reading identifier. Its page records have inclusive
  canonical atom ranges and may name a scan that also carries another occurrence.
  The validator checks contiguity within each occurrence. Approved rite ranges
  select and clip a haftarah occurrence. The library returns all matching
  occurrences and the CLI prints one link per physical scan.

**Lint, not example tests.** `check` (also run as a pytest lint, one new file
`py/tests/test_scan_pages_index.py`) verifies over the tracked JSONs:

- every rec's page is in `pages`, is of a kind a rec may sit on, and names a book that
  page holds; every position parses against MAM verse counts (FAIL, never skip, when
  MAM-parsed is absent — per the repo's missing-input rule);
- every stored classification is re-derived from the listing and compared — a differential
  check of all 5,720 pages against an independent derivation of the same fact, and the one
  lint that already does full-scale work at Phase 0;
- within an ordinary segment or a printed occurrence, consecutive records in reading
  order meet at adjacent atoms. The Simanim Tiqqun permits distinct occurrences to
  share a scan. Strand-tagged segments may also share a scan, as with the two
  Decalogue strands on one Jerusalem Crown sheet;
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
  `py/scan_pages/*`, `in/scan-pages/*`, `py/tests/test_scan_pages_index.py`, and
  the scan entry point declarations in `py/tests/test_mega_coverage.py`. **Nothing
  else is expected to change** — no MAM data, no generated artifacts, no sibling repos; an
  unexpected diff elsewhere is a finding.
- No `sys.path` surgery (the entry point in `py/` gives `scan_pages.*` imports for free);
  black on every touched `.py`; commit and push per the global rules; load the
  `hebrew-prose` skill before writing findings prose into this doc (parasha names,
  megillot, "the Simanim Tiqqun" never a bare "Simanim").
- Scan evidence: the executing session reads local image crops or original JPGs to verify
  OCR suggestions and printed page numbers. Batch the paired crops for review.

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
matching one-atom written-but-not-read form. A read-but-not-written word
contributes no atom, following the maintained written-atom reader; its
matching one-atom display/reading forms are checked before omission.
The four native-verified unequal forms at Ezekiel 8:6 and 9:11 and
Jeremiah 6:29 and 18:3 select the maintained qere pair and declare
both canonical atoms an indivisible source-written-word span. The template
subtype and both consonantal forms must match exactly; unknown forms and
ambiguous span locations are refused. Census, check and lookup reject a
page start or end inside a mapped pair. The named two-word special subtype
also admits an explicit parameterless paseq between its two qere atoms;
other nested forms refuse. The named three-samekh break is a separator
without an atom, following the maintained definitions. Other multi-atom ketiv/qere,
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

### Ezekiel completion, 2026-11-03

Ten bounded native-inspection checkpoints complete all 49 JC and 70 BHL
ordinary-body portions of Ezekiel. The final opening group adds these
directly observed intervals; earlier checkpoints supply every later page.

| Edition | Scan image | Printed page | Observed interval |
|---|---|---:|---|
| JC | `481-Ee.jpg` | 481 | 1:1 atom 1 through 1:28 atom 9 |
| JC | `482-Ee.jpg` | 482 | 1:28 atom 10 through 3:16 atom 1 |
| JC | `483-Ee.jpg` | 483 | 3:16 atom 2 through 4:14 atom 1 |
| BHL | `0733-Ee.jpg` | 733 | 1:1 atom 1 through 1:21 atom 9 |
| BHL | `0734-Ee.jpg` | 734 | 1:21 atom 10 through 2:10 atom 5 |
| BHL | `0735-Ee.jpg` | 735 | 2:10 atom 6 through 3:19 atom 5 |
| BHL | `0736-Ee.jpg` | 736 | 3:19 atom 6 through 4:9 atom 10 |

BHL headers omit the physical opening continuations on 734 (1:21),
735 (2:10) and 736 (3:19). The body text supplies the exact boundaries.
The seven new portions join the previously inspected chapter-4 continuations
without gaps. Printed page numbers were checked separately from image identities.

The native forms and maintained selected-qere semantics establish one written
word corresponding to two canonical qere atoms at 8:6 (atoms 7-8) and 9:11
(atoms 12-13). JC486/BHL741 contain the first whole pair; JC487/BHL742 contain
the second. Both native written forms and their qere annotations were already
inspected in the preceding checkpoints, and those originals were rehashed.
Only the exact two subtype/form combinations are admitted. Protected spans
propagate through the selected Scripture target, including 9:11's enclosing
note; documentation contributes no atoms. A repeated pair within a verse
is refused rather than assigned an occurrence. This closes the four partial
physical pages without changing the older fragment observations.

All 1,273 verses / 18,732 atoms match the independently decoded MAM-simple
export. Whole-book partitions pass 117 adjacent joins and 107 split-verse
checks. Four deliberately invalid page partitions, one per mapping and edition,
remain canonically contiguous but split a protected pair; all are rejected.
Fourteen malformed-form checks and two ambiguous-span checks also refuse.
Each edition refuses 1,131 repeated-atom queries. Original scans and detailed
source provenance remain private; no image enters either repository.

The whole book is now available through `lookup` on the research branch.
The catalog check passes for five editions, 5,720 pages, 361 records and two
segments. Eight focused tests passed (30 deselected, 122.55 seconds), covering
every adopted edge, independent atom agreement and the invalid-boundary
regression. Black and whitespace checks passed. Full suite and mega remain
deferred under the ordinary focused-check policy. Universal completion still
requires 26 ordinary-body books per edition, source-classification reconciliation,
strand handling and the deferred refresh/density work. Main integration and
deployment are separate from this research-branch adoption.

### Jeremiah completion, 2026-11-03

The three opening portions completed the whole-book census.
All **136 Jeremiah portions** are now available through `lookup` on the
isolated research branch, following explicit approval. Each edition covers
**1,364 verses / 21,833 canonical atoms**, from 1:1 atom 1 through 52:34
atom 17, with no gaps or overlaps.

| Edition | Adopted Jeremiah portions | First scan | Last scan |
|---|---:|---|---|
| JC | 56 | `425-Je.jpg` | `480-Je.jpg` |
| BHL | 80 | `0651-Je.jpg` | `0730-Je.jpg` |

The final opening pages are JC 425 (1:1 atom 1 through 2:8 atom 5),
BHL 651 (1:1 atom 1 through 1:19 atom 3) and BHL 652 (1:19 atom 4
through 2:20 atom 17). Their running Scripture, printed numbers and
continuations were inspected directly. Printed header ranges do not replace
body boundaries. Canonical cues retain the verified source-to-MAM atom
correspondences; source orthography or numbering can differ from the query.
Original scans and detailed source provenance remain private.

The exact one-written-word/two-reading-word mappings at 6:29 and 18:3
remain indivisible. Both atoms of each pair stay on the same source page;
an internal page start or stop is rejected. Selected Scripture targets,
ordinary one-word qere and read-without-written-word behavior retain their
existing maintained semantics. Unknown or ambiguous forms still refuse.
No projection or lookup implementation changed for adoption.

Whole-book partitions preserve every verified interval and pass **134 adjacent
joins / 120 split-verse checks**. Each atom belongs to exactly one page per
edition. Independent MAM-simple comparison agrees on the complete book.
Lookup supports unqualified verses, unique phrases and lone unique atoms;
ambiguous repeated-atom queries still refuse. For example:

```powershell
python py/main_scan_pages.py lookup Jeremiah 1:19 --edition jc1 --edition bhl
python py/main_scan_pages.py lookup Jeremiah 6:29 --edition jc1 --edition bhl
python py/main_scan_pages.py lookup Jeremiah 39:13 --edition jc1 --edition bhl
```

Accepted coverage is now **14 books / 3,687 verses per edition**. Across the
five catalogs there are **5,720 pages, 495 records, 367 completed portions,
128 unread seeds and two segments**. Nine focused tests passed (30 deselected),
including independent adopted-book atoms, every adopted edge query, guarded
mapping regressions and CLI wiring; the catalog check also passes. Full suite
and mega remain deferred under the focused-check policy. Universal completion still needs 25
ordinary-body books per edition, source-classification reconciliation,
strand handling and deferred refresh/density work. Other incomplete books
remain unavailable through lookup. Main integration and deployment are
separate from this research-branch adoption.

**Phase 0 - survey and tracked inventory. DONE, 2026-08-07.** The code is
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
simanim-tiqqun's 444 C pages are classified `body-unassigned`, awaiting Phase 3 to
identify their actual contents and verify their segments of running text.

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

### OCR workflow for future censuses

Ben's decision, 2026-11-06: “use this workflow for all future work.” Apply it to
future scan-indexing batches in every edition, including the Simanim Tiqqun. Use a
scan-capable local checkout and the edition's known inventory. Resume from the latest
verified checkpoint for that edition.

1. Batch local OCR over the outer body lines on each side of a join. Choose body
   regions by edition, page parity and column order, and check the regions on a few
   representative pages before using them across a new layout. Keep raw text and
   coordinates in scratch space. The trial used Tesseract 5.5.3 via `tesserocr` 2.12.0
   and the official `tessdata_best` Hebrew model. It segmented lines by dark-pixel
   density, cropped each line around the bulk of the letter shapes, scaled to 65%,
   and recognized each band in single-line mode.
2. Compare letters from the two sides with the projected MAM text. Rank candidate
   joins using both edges, with the stop and start at adjacent reference atoms.
   Retain ties and the reference positions. OCR and approximate matching supply
   suggestions for review. Validate the production projection through the maintained
   scan-pages code and resolve unsupported forms explicitly.
3. Review both scan crops together for every join. Confirm the exact boundary cues
   against the visible running text. Check both ends of each book and the relevant
   text on any shared page. Read the wider scan when a crop misses a line, a repeated phrase
   is ambiguous, or the edition differs from MAM. Verify printed page numbers
   separately. Keep an unresolved join out of the census until the evidence supports
   an exact placement.
4. Give the verified cues and printed page numbers to `census`. Run `check` and the
   focused scan-pages tests from the repository root before committing the verified
   metadata. Inspect the catalog diff. Keep scans, crops, raw OCR and candidate lists
   in local scratch space.

The trial covered 30 scans and 23 joins in Koren, Jerusalem Crown and Dotan BHL.
It tuned the OCR settings on 22 scans and kept eight Psalms scans for a fresh check.
Only two joins met the strict exact-match rule. The approximate match ranked the
verified break uniquely first at 22 joins and tied first at Dotan BHL 941/942.
Visual review confirmed all 23. The six fresh joins took about 17 seconds for OCR,
matching, preparation and visual review after setup. The timing covers joins with
existing reference answers and excludes printed page-number verification and census
adoption. The trial used MAM-simple to match Genesis because the maintained
scan-pages projection rejects a template outside the sampled passage.

**Phase 2 — the censuses, edition by edition.** Ordinary lookup now covers all
39 books in Jerusalem Crown, Dotan BHL, Koren and Simanim Tanakh. The local
adoption sections below record the coverage and verification.

**Phase 3 — the Simanim Tiqqun.** The verified occurrence catalog entered the
local branch on 2026-11-13. The unpointed D section stays out of lookup under
Ben’s 2026-08-07 decision. The available strand requests and remaining scope are
recorded below.

### Local adoption on 2026-11-13

Ben authorized applying, verifying and committing the prepared patches on the
local branch `codex/scan-index-laptop-20261104` in GitRepos3. The checkout
started at `c81ddf9151ef46831ab8ef74c13cda92392038a0` with the reviewed
projection prerequisite already present. Adoption proceeded through Jerusalem
Crown and Dotan BHL, Koren and Simanim Tanakh, then the Simanim Tiqqun. The
table records the coverage at that checkpoint.

| Edition | Adopted coverage |
| --- | --- |
| Jerusalem Crown | 27 ordinary-body books on 440 scans, from `425-Je.jpg` to `874-2C.jpg` |
| Dotan BHL | 27 ordinary-body books on 540 scans, from `0651-Je.jpg` to `1225-2C.jpg` |
| Koren | 39 ordinary-body books on 1,240 scans |
| Simanim Tanakh | 39 ordinary-body books on 1,398 scans |
| Simanim Tiqqun | 496 body intervals on 396 scans and two appendix intervals, in 116 occurrences |

Jerusalem Crown `766-Es-Da.jpg` contains Esther. Daniel starts on `767-Da.jpg`.
Dotan BHL `0946-Pr.jpg` and `0974-Jb.jpg` are blank. The earlier completed
records and pre-Jeremiah unread seeds in both editions are preserved. Koren’s
`D1-Ps-107.jpg` is printed page 60. The catalog keeps filename order and the
census puts that scan between printed pages 59 and 61.

Ben’s 2026-11-12 decisions assign both printed forms of 2 Samuel 21:12 to
canonical atoms 22–24 on Koren p. 178 and Simanim Tanakh p. 545. For the four
split Simanim Tanakh pairs at 2 Kings 18:27, Jeremiah 49:39, Daniel 5:16 and
Ezra 2:1, the page with the pointed form owns the canonical interval. The
adjacent scan’s printed form links to that owner. The optional `--printed-form`
query exposes recorded edition spellings while ordinary phrase lookup keeps
its canonical behavior. Source verification found both instances of להם
on Simanim Tanakh p. 842 at Ezekiel 1:18, atoms 3 and 5. The first was missing
from the earlier transcription of the scan.

The Simanim Tiqqun rite selector `vayetze-sephardi` uses Hosea 11:7–12:12.
The printed table’s endpoint is 12:14 and both occurrences of 12:13–14
remain in ordinary lookup. The selector `shabbat-shuvah-joel-most-ashkenazi`
uses Joel 2:15–26. Joel 2:27 remains in ordinary lookup. A `t` suffix can
select the verified תחתון appendix on `C246.jpg` for Exodus or `C247.jpg`
for Deuteronomy. A bare reference uses ordinary body coverage. The named
עליון body ranges were verified separately, as recorded below.

Refresh the Simanim Tiqqun inventory with
`py/main_scan_pages.py survey --edition simanim-tiqqun`. The refresh
retains the portable occurrence, rite and nontext assignments and checks
them against the inventory before writing. It refuses missing assigned
scans and newly unassigned pointed scans. Scans, raw OCR, and source
receipts remain in local research storage.

The maintained checker passed on the adoption checkout with 5,720 scans,
4,188 records and 120 segments or occurrence groups. All 18 focused tests
passed, including ordinary page-edge lookup and the MAM-simple comparison.
The receipt replay checked 922 post-Psalms cues and 11,074 whole-verse lookups
in Jerusalem Crown and Dotan BHL. The Simanim Tiqqun replay covered all 498
intervals, 8,389 ordinary verse lookups, 50 rite cases, and 26 appendix phrase
queries. Refresh reproduced the catalog byte for byte and preserved it on
both inventory failures. The live Tiqqun inventory matched all 614 filenames.
Black and Git whitespace checks passed.

### Simanim Tiqqun main Decalogue lookup, 2026-11-13

The local branch adopted named `e` lookup from `94476fdb` under Ben’s
2026-11-13 authorization to continue local scan-index adoption. Both main
passages have printed-tradition עליון. The hand transcriptions record nine
chanted verses in each. In Exodus, the Simanim Tiqqun has separate chanted
words at ובנך ובתך and a maqaf in the opening לא־תחמד of 20:13. Its
Deuteronomy transcription agrees with the reference at all 164 accent tokens.
The source review checked the headings and the beginning, split and end of
each passage against the scan crops. [Exodus transcription](../in/accgram/edition_transcriptions/simtiq_ex_elyon.txt) · [Deuteronomy transcription](../in/accgram/edition_transcriptions/simtiq_dt_elyon.txt)

| Scan | Inclusive MAM atom range |
| --- | --- |
| `C083.jpg` | Exodus 20:2 atom 1 through 20:5 atom 4 |
| `C084.jpg` | Exodus 20:5 atom 5 through 20:13 atom 15 |
| `C208.jpg` | Deuteronomy 5:6 atom 1 through 5:13 atom 16 |
| `C209.jpg` | Deuteronomy 5:13 atom 17 through 5:17 atom 16 |

The `e` suffix selects these intervals. The lookup intersects the verified
passage bounds with the existing ordinary page ranges. A split verse
returns both scans, and a unique phrase selects the scan containing its
first atom. MAM-simple’s `cant-bet` agrees with the maintained canonical
atom coordinates for both ranges. The `t` suffix still selects the verified
appendices.

The checkout replay verified all 24 named verse queries, 358 unique atom
cues and eight CLI boundary cases. The existing Tiqqun replay covered all
498 occurrence intervals and both approved rites. The maintained checker,
Black and Git whitespace checks passed. The focused suite returned 200
passed and five skipped. Refresh preserved the catalog byte for byte on an
unchanged inventory and refused incomplete inventory before writing.

### Simanim Tanakh named Decalogue lookup, 2026-11-13

Ben authorized local adoption from `c620898f` under the existing
`t`/`e` policy. The six local edition scans matched the source hashes
and dimensions in the maintained editor exports. Both named atom
arrays in MAM-simple agreed with MAM-parsed in each passage.

The Simanim Tanakh body has manuscript-tradition תחתון and its appendices
have manuscript-tradition עליון. The Deuteronomy body’s transcribed qadma
on ויום differs from the reference’s pashta. The chanted-verse boundaries
and canonical atom coordinates agree. [Exodus body transcription](../in/accgram/edition_transcriptions/simtan_ex_taxton.txt) · [Deuteronomy body transcription](../in/accgram/edition_transcriptions/simtan_dt_taxton.txt)

| Named lookup | Scan | Inclusive MAM atom range |
| --- | --- | --- |
| Exodus `t` | `A2-E-0119.jpg` | 20:2 atom 1 through 20:12 atom 7 |
| Exodus `t` | `A2-E-0120.jpg` | 20:12 atom 8 through 20:13 atom 15 |
| Exodus `e` | `A9-A2-10C-0350.jpg` | 20:2 atom 1 through 20:13 atom 15 |
| Deuteronomy `t` | `A5-D-0297.jpg` | 5:6 atom 1 through 5:11 atom 1 |
| Deuteronomy `t` | `A5-D-0298.jpg` | 5:11 atom 2 through 5:17 atom 16 |
| Deuteronomy `e` | `A9-A5-10C-0351.jpg` | 5:6 atom 1 through 5:17 atom 16 |

The lookup uses the existing body partition for named body requests. The
appendix scans are assigned directly to the verified passage ranges.
[Exodus appendix transcription](../in/accgram/edition_transcriptions/simtan_ex_elyon.txt) · [Deuteronomy appendix transcription](../in/accgram/edition_transcriptions/simtan_dt_elyon.txt)

The checkout replay passed all 48 named verse requests, 716 unique
phrase cues and four CLI boundary cases. The maintained checker
passed across all five catalogs. The focused suite returned 200 passed
and five skipped. The Simanim Tiqqun replay covered all 498 occurrence
intervals and both approved rites, and its inventory refresh checks
passed.

### Jerusalem Crown and Dotan BHL named Decalogue appendices, 2026-11-13

The local continuation adopted six named ranges from four appendix scans.
The source review checked the running text and each chanted-verse
boundary against the MAM coordinates. The Jerusalem Crown has תחתון in
the right column and עליון in the left, with 12 and 10 chanted verses
respectively in each passage. Dotan BHL has 10 chanted verses of עליון
in each appendix.

| Edition and suffix | Scan | Inclusive MAM atom range |
| --- | --- | --- |
| Jerusalem Crown `t` or `e` | `876-02-Exod-Decalogue.jpg` | Exodus 20:2 atom 1 through 20:13 atom 15 |
| Jerusalem Crown `t` or `e` | `877-03-Deut-Decalogue.jpg` | Deuteronomy 5:6 atom 1 through 5:17 atom 16 |
| Dotan BHL `e` | `1227-Exod-Decalogue-Upper.jpg` | Exodus 20:2 atom 1 through 20:13 atom 15 |
| Dotan BHL `e` | `1228-Deut-Decalogue-Upper.jpg` | Deuteronomy 5:6 atom 1 through 5:17 atom 16 |

At Deuteronomy 5:9 atom 6 the three columns print ketiv מצותו in the
running text and give qere מצותי separately. The canonical phrase lookup
uses מצותי at that coordinate. Dotan BHL’s Deuteronomy appendix has
pashta on אנכי where the manuscript-tradition עליון reference has tipeḥa.
The chanted-verse boundaries agree.

At this checkpoint, the Jerusalem Crown’s named requests selected the
verified appendix columns. Ordinary body coverage in Exodus and
Deuteronomy was still uncensused in both editions, and Dotan BHL `t`
was unavailable.

The checkout replay passed 72 named verse requests, 1,074 phrase cues
and eight CLI cases. The maintained checker passed across all five
catalogs. All 18 scan-index tests passed using the existing scratch runner,
which caches repeated catalog validation in two differential tests.

### Koren named Decalogue lookup, 2026-11-13

After the stress-helper comparison finished, Ben released the Koren catalog
and authorized adopting the verified patch from `aa594dab`. Ben’s direct
transcriptions and their editor exports establish
printed-tradition תחתון on `A2-E-113.jpg` and `A2-E-114.jpg` in Exodus and
on `A5-D-280.jpg` and `A5-D-281.jpg` in Deuteronomy. The named body ranges
split at Exodus 20:11 between atoms 13 and 14 and at Deuteronomy 5:9 between
atoms 5 and 6. The printed-tradition עליון appendices `V-038.jpg` and
`V-039.jpg` each cover the whole corresponding Decalogue.
[Exodus body transcription](../in/accgram/edition_transcriptions/koren_ex_taxton.txt) · [Deuteronomy body transcription](../in/accgram/edition_transcriptions/koren_dt_taxton.txt) · [Exodus appendix transcription](../in/accgram/edition_transcriptions/koren_ex_elyon.txt) · [Deuteronomy appendix transcription](../in/accgram/edition_transcriptions/koren_dt_elyon.txt)

The Exodus appendix transcription has separate chanted words at יהיה לך
and ובנך ובתך, where the reference has maqaf. Both preserve the canonical
atom positions. Bare references use the ordinary body records. Named
`t` requests clip those records to the Decalogue, and `e` requests select
the appendix. Each starts at Exodus 20:2 atom 1 or Deuteronomy 5:6 atom 1
and runs through Exodus 20:13 atom 15 or Deuteronomy 5:17 atom 16.

The adopted catalog matched the verified scratch catalog byte for byte.
The checkout replay passed 48 named verse requests, 716 phrase cues,
48 ordinary regression queries and six CLI cases. The five-catalog
checker passed, and the focused transcription tests returned 199 passed
and five skipped.

### Census-preserving inventory refresh, 2026-11-13

`py/main_scan_pages.py survey` can now refresh all five inventories. For a
full-Tanakh edition with adopted lookup data, the command reclassifies
the complete filename listing and preserves all census records, unread
seeds, named ranges and recorded printed forms. It accepts changes to
nontext scans and refuses any addition, removal or reclassification of
a text page. The Simanim Tiqqun still validates the recorded occurrence
assignments against its refreshed inventory. All requested editions
are prepared before any catalog is written.

The survey entry point reproduced all five catalogs byte for byte from
the 5,720 saved filenames. Scratch replays added and removed a nontext
scan in each edition, refused missing and new text scans, and verified
that a refusal in the last edition left all catalogs byte-identical.

### Page-density advisory and local completion, 2026-11-13

The `check` command reports unusual atom counts on ordinary interior
pages that carry a single book. The advisory applies once an edition
and book have at least eight such pages. It flags counts below half
or above one and a half times the median for that edition and book.
The band is a review heuristic. All reported pages pass the exact cue
and partition checks. An independent calculation over 3,258 eligible
pages agreed with the five advisories. The six focused scan-index and
mega coverage tests passed.
The mega coverage lint now declares `census` and `lookup` as hand-run
commands, following their documented input and output contracts.

### Jerusalem Crown and Dotan BHL body coverage, 2026-11-13

Ben directed the local adoption of the existing verification records for
Genesis through Isaiah. The Jerusalem Crown added 422 book-page portions
on 420 scans, and Dotan BHL added 622 portions on 620 scans. Each edition
now has ordinary lookup for all 39 books. The new portions cover 11,451
verses and 166,527 canonical atoms per edition. MAM-parsed and MAM-simple
agree on the ordered atom sequence for all 12 added books.

The saved 2 Samuel source review establishes that Jerusalem Crown
`316-2S-blank.jpg` is blank. The catalog now classifies the scan as blank.
Both catalogs retain the completed records from Jeremiah onward.
The import used observed printed page numbers and shortened saved
selectors to the first or last unique sequence at each boundary. Six
boundaries use cues derived from MAM at the verified position. The scan
evidence remains in local research storage.

The replay verified all 2,088 new boundary cues and 22,902 whole-verse
lookups, including 914 split verses. The maintained checker passed
across all five catalogs and reported a new density advisory for
Jerusalem Crown Judges `234-Ju.jpg` at 187 atoms against a book median of
394. The saved boundaries for that scan pass the cue and partition
checks.

Bare Decalogue references now select the body scans in both editions.

### Jerusalem Crown and Dotan BHL named body lookup, 2026-11-13

The Jerusalem Crown prints both strands in the running text of Exodus and
Deuteronomy. At the opening אנכי, the running text has both pashta and
tipeḥa. The short prohibitions also carry marks from both strands.
Dotan BHL prints תחתון in the running text, with a single accent at
the opening אנכי and continuous cantillation across the short
prohibitions. Its notes on pp. 109 and 266 direct readers to the עליון
appendices on pp. 1227 and 1228.

| Edition and suffix | Body scan | Inclusive MAM atom range |
| --- | --- | --- |
| Jerusalem Crown `t` or `e` | `069-E.jpg` | Exodus 20:2 atom 1 through 20:9 atom 3 |
| Jerusalem Crown `t` or `e` | `070-E.jpg` | Exodus 20:9 atom 4 through 20:13 atom 15 |
| Jerusalem Crown `t` or `e` | `171-D.jpg` | Deuteronomy 5:6 atom 1 through 5:17 atom 16 |
| Dotan BHL `t` | `0109-E.jpg` | Exodus 20:2 atom 1 through 20:13 atom 15 |
| Dotan BHL `t` | `0266-D.jpg` | Deuteronomy 5:6 atom 1 through 5:16 atom 10 |
| Dotan BHL `t` | `0267-D.jpg` | Deuteronomy 5:16 atom 11 through 5:17 atom 16 |

The Jerusalem Crown catalog retains the separately verified appendix
locations. A range with `body: true` and `appendix` records both locations
and selects the body at lookup. Dotan BHL `e` selects its verified appendices.
The replay passed 96 named verse requests, 1,432 phrase requests and
35 CLI cases.

### Scan-page density source review, 2026-11-14

Direct review of the six flagged scans confirmed the first and last
Scripture atoms of each catalog interval. The low counts reflect the
printed layouts. All six intervals stand.

| Edition and scan | Inclusive MAM atom range | Atoms | Printed layout |
| --- | --- | ---: | --- |
| Jerusalem Crown `234-Ju.jpg` | Judges 5:12 atom 13 through 5:28 atom 11 | 187 | Spaced lines of the Song of Deborah |
| Koren `B1-Js-021.jpg` | Joshua 12:9 atom 1 through 12:22 atom 3 | 87 | List of kings, with the names and counts in widely separated columns |
| Simanim Tanakh `E4-Ec-1248.jpg` | Ecclesiastes 3:5 atom 2 through 3:15 atom 10 | 125 | Short paired clauses across two columns, followed by full-width text |
| Dotan BHL `1037-Ec.jpg` | Ecclesiastes 2:25 atom 4 through 3:7 atom 7 | 84 | Short paired clauses across two columns |
| Dotan BHL `1091-Er.jpg` | Ezra 2:37 atom 5 through 2:49 atom 3 | 84 | Full-width text followed by the entry-per-line list |
| Dotan BHL `1092-Er.jpg` | Ezra 2:49 atom 4 through 2:57 atom 8 | 54 | Entry-per-line list continued from the preceding scan |

## Local main integration, 2026-11-14

The completed scan indexes come from `7294eb46616bbd747b9cfadd1d20eef24f64fccc`.
The scoped integration applies the finished scan catalog and code changes to
`1c8a68e00c86b2c50930078cc4854af93139101d` and preserves upstream declarations
in the mega coverage lint. The original branch retains the interim research
checkpoints and the separate Job 16:6 TEI documentation correction in
`c81ddf9151ef46831ab8ef74c13cda92392038a0`.

## Scope beyond the five editions

The Da'at Miqra subsection records the canonical holding for future work. The
JC2 Companion, JC3, readers and loose PDFs are outside the current index.
