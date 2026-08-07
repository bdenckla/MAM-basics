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

## Decisions (all proposed 2026-08-06 by the planning session; Ben can veto any)

- **Home repo: MAM-basics** (`C:\Users\BenDe\GitRepos\MAM-basics`, venv at
  `.venv\Scripts\python.exe`). All of Ben's Python lives here now and new issues are filed
  here. The scans themselves stay where they are and no image enters the repo; the repo
  tracks only index *metadata* (filenames, page↔bcv anchors) — uncopyrightable facts, fine
  in a public repo.
- **One name token everywhere: `scan_pages` / `scan-pages`.** Entry point
  `py/main_scan_pages.py` with subcommands (`survey`, `lookup`, `record`, `check`); library
  code under `py/scan_pages/`; tracked index data under `in/scan-pages/`; this doc
  `doc/scan-pages.md`.
- **bcv input format: bk39 id plus chapter:verse**, e.g. `lookup Genesis 12:3`,
  `lookup 1Samuel 17:4`. The bk39 ids are the ones `py/mb_cmn/bib_locales.py` documents
  ("A pithy example of a valid value for book39 is 1Samuel"). Nothing fancier — per Ben's
  standing "CLI ergonomics aren't worth it," the program has essentially one user and he
  can type the canonical id.
- **Verse counts come from the MAM-parsed sibling at runtime** (via
  `mb_cmn/read_books_from_mam_parsed_plus.py`), not from a second tracked copy — no
  duplicated artifact to drift. Versification: MAM's. The editions' own versification
  differs from MAM's at scattered loci, by one or two verses within a chapter. This plan
  first claimed a whole page absorbs such a difference; Ben's correction, 2026-08-07: it
  does not — a verse that is first or last on its page (about 2 in 23) spills to the
  neighboring page when the numberings disagree about it, and a verse can genuinely
  straddle two pages regardless of numbering. What absorbs both is a **floor on the
  bring-up window: never narrower than ±1 page, however dense the anchors get.** The same
  floor covers a `recorded` anchor that is itself off by one verse because Ben read the
  edition's printed verse number at a discrepancy locus — a slip the monotonicity lint
  cannot catch, since a one-verse slip is still monotonic.
- **Anchor semantics: "this bcv appears on this page."** Containment, not page-start —
  containment is what a human looking at a page can record without checking whether the
  page's first verse began on the previous page. Anchor kinds: `book-start` (derived from
  filenames by `survey`), `recorded` (added by Ben via `record`), `head` (read from a
  running head by a vision pass, Phase 4).
- **Lookup interpolates between anchors and shows its uncertainty.** Between the two
  anchors that bracket the requested bcv in verse order, estimate the page linearly by
  verse index; present the estimated page plus neighbors covering the uncertainty (at
  least ±1 page; wider in proportion to the anchor gap). Misses in a big book are expected
  at first — see "Honest accuracy expectations" below — and every miss is one `record`
  away from never happening again.
- **The bring-up is one generated HTML page, opened by the program.** Written under
  `.novc\scan-pages\` (gitignored), one section per edition: the candidate page image(s)
  inline via `file:///` URLs into the scans folder (`loading="lazy"` — these JPGs run
  1–18 MB), prev/next links, and the anchor evidence used. Default behavior when *Ben*
  runs it: open via `os.startfile`, because "bring up" is the ask. A Claude session runs
  it with `--no-open` and hands Ben the `file:///` link, per the global
  don't-launch rule.
- **The program is cwd-independent.** Scans root and repo paths are anchored in code
  (`Path.home() / "OneDrive" / "Documents" / "ScansOfBooks"`; `mb_cmn/paths.py` for
  siblings), never cwd-relative, so it runs from anywhere. UTF-8 stdio reconfigure first
  thing in `main()`, per the global rules — though real output goes to the HTML file, and
  stdout carries only short ASCII progress.
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
reading sample pages on 2026-08-06 (`B10.jpg`, `B60.jpg`, `C012.jpg`, `C400.jpg`,
`D10.jpg`, `E10-06.jpg`):

- `A01`–`A04`: covers/endpapers.
- `B01`–`B74`: front matter with its own printed page numbers — introductory essays and
  the per-parasha simanim apparatus (`B60.jpg` is apparatus page 60, פרשת משפטים).
- `C001`–`C444`: the main body. **Scan number = printed page number** (`C012.jpg` is
  printed page 12). Running head carries book · chapter range · parasha (e.g.
  `בראשית · יא יב · לך לך`), and the text appears twice per page (pointed and unpointed
  columns). The C range holds more than Torah: `C400.jpg` is מגילת רות chapter 3 — so
  megillot, and presumably the haftarot Ben's ask names, live in C between the Torah's end
  and the back. Segment boundaries inside C are unknown; finding them is Phase 3, and the
  cheap route is the printed ToC (in B or A), since C scan numbers equal printed numbers —
  a ToC page read gives the whole haftarah/megillot map in a handful of image reads.
- `D01`–`D60`: a compact, *unpointed-only* Torah, scanned rotated 90° (`D10.jpg` is
  Devarim). Whether Torah lookups should also surface a D hit is an open question below.
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
  "anchors": [
    {"page": "013-G.jpg", "bcv": "Genesis 1:1", "kind": "book-start"},
    {"page": "220-Js.jpg", "bcv": "Joshua 10:12", "kind": "recorded", "date": "2026-08-07"}
  ]
}
```

- `pages` is the complete sorted listing (front and back matter included, classified), so
  the index is meaningful — and lintable — on a clone with no scans folder at all.
- `anchors` sorted by MAM verse order; `survey` seeds `book-start` anchors from the
  filename book codes (first page of each book's run contains that book's 1:1).
- The simanim-tiqqun JSON additionally carries a `segments` map (Torah / haftarot /
  megillot ranges within C, filled by Phase 3) and a haftarah table: entries of
  `{"name": "...", "range": ["Isaiah 40:1", "Isaiah 40:26"], "page": "C…"}` — recorded as
  the book prints them, whatever rites it prints, not computed from a liturgical calendar.
  A haftarah bcv can hit several haftarot; `lookup` returns every hit.

**Lint, not example tests.** `check` (also run as a pytest lint, one new file
`py/tests/test_scan_pages_index.py`) verifies over the *tracked JSONs only*: every anchor's
page is in `pages`; every bcv parses against MAM verse counts when MAM-parsed is present
(FAIL, never skip, when the sibling is absent — per the repo's missing-input rule);
anchors strictly increase in verse order as pages advance; segments don't overlap. This is
the mechanical-lint shape Ben's test rules allow; no example-based unit tests.

**Honest accuracy expectations.** ~23k verses over ~1000 body pages per full-Tanakh
edition is ~23 verses/page. With only `book-start` anchors, interpolation across a long
book (Psalms is 93 pages in jc1, 128 in simanim-tanakh) can miss by several pages where
text density shifts (poetic layout, seder heads). The design absorbs this three ways: the
uncertainty window widens with anchor distance, every miss is one `record` from becoming
an anchor, and Phase 4 can densify any edition to chapter-level anchors if the misses
annoy in practice.

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
what it is in this doc). Emit the five JSONs with `pages` + `book-start` anchors; implement
`check` + the pytest lint; report per-edition/per-book page counts and anomalies here.
Expected result: 39 `book-start` anchors in each of jc1, koren, simanim-tanakh, bhl (fewer
only if a book genuinely shares its opening page), none yet for simanim-tiqqun.

**Phase 1 — lookup and bring-up.** Implement `lookup <bk39> <ch>:<v>` → interpolation →
HTML bring-up as designed above. Covers the four full-Tanakh editions everywhere, and
simanim-tiqqun for Torah once its Torah segment inside C is bounded — bound it in this
phase by bisection on running heads (`Read` on ~10 C pages). Verify on a handful of spot
bcvs by reading the produced candidate pages and checking the requested verse is on or
adjacent to the estimated page; record the spot results here. **Pause for Ben:** he tries
it on real lookups.

**Phase 2 — the record loop.** `record <edition> <page-filename> <bk39> <ch>:<v>` appends
a `recorded` anchor (validated, sorted, linted); the bring-up HTML shows, next to each
image, the exact `record` command that would pin it, so a confirmed hit is a paste away
from becoming an anchor. Small; can land with Phase 1.

**Phase 3 — simanim-tiqqun haftarot and megillot.** Find the printed ToC in the B (or A)
section and read the haftarah/megillot start pages straight off it (C scan numbers equal
printed numbers, so the ToC is the whole map); fall back to bisection sweeps of C only if
the ToC disappoints. Fill `segments` and the haftarah table; extend `lookup` so a Nakh bcv
inside a printed haftarah yields the simanim-tiqqun hit(s), and a megillot bcv the megillah
page. Verify each haftarah's start page by reading it. Report the haftarah inventory here.

**Phase 4 — optional densification, per edition, on demand.** A vision pass reading each
body page's running head (book + chapter range on every edition sampled) to emit `head`
anchors at chapter granularity; the monotonicity lint plus interpolation-residual outliers
catch misreads. Roughly a thousand image reads per edition — so per edition, only after
Phase 1–2 experience shows its interpolation actually misses enough to annoy. Default:
deferred.

## Open questions for Ben (defaults chosen so no phase blocks on them)

1. **Should a Torah bcv also bring up the simanim-tiqqun D section** (the compact
   unpointed Torah)? Default: no D hit until asked; it is 60 rotated pages, cheap to
   anchor later (book-level bisection, ~10 image reads, plus a CSS rotation in the
   bring-up HTML).
2. **Phase 4:** wanted anywhere, and if so which edition first? Default: defer.
3. **Scope:** the other ScansOfBooks folders (JC2 Companion, JC3, Da'at Miqra, the
   readers, the loose PDFs) stay out of the index. Confirm.
