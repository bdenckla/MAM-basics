# Charitable Leningrad Codex (CLC) — Design

> **Living design doc for CLC.** Editorial principles, the feature set (at varying maturity — see the
> §11 status table), decisions already made, and the open questions that remain — for a new
> diplomatic edition of the Leningrad Codex (LC), kin to UXLC. Not an exhaustive spec, and not every
> future item is captured. **[TBD]** flags open questions inline; §9 consolidates them; the companion
> build plan is [doc/clc-skeleton-plan.md](clc-skeleton-plan.md).

---

## 1. The thesis: "charity"

**Name:** Charitable Leningrad Codex — **CLC**.

The defining feature relative to UXLC: **where UXLC has an *uncharitable* transcription,
CLC gives the *naqdan* (pointing-scribe) the benefit of the doubt.** All things being equal
(or even slightly unequal), CLC prefers the **"least weird"** reading — the one that makes the
naqdan look like he knew what he was doing, rather than the one that makes him look like he
blundered.

This is not "correcting" the LC and it is not "fixing" it to match a grammar. It is a
transcription stance: when the image is ambiguous, decide the ambiguity in the direction that
is internally coherent. UXLC, by contrast, often resolves the same ambiguities mechanically
(e.g. by *mark angle*), which can manufacture weirdness that the scribe probably never intended.

> Working tension to keep honest: charity must not become silent emendation. Every charitable
> choice that departs from UXLC should be **recorded as a note** (see §7.3–7.5) so the reader
> can see what we did and why. "Charitable but transparent." (First applied at Deut 5:8.2 — see
> §7.4.) Two features carry the transparency half: an **introductory essay** that *argues* the
> principle (§7.10), and a **differences-from-UXLC index** that *shows the receipts* (§7.9).

---

## 2. The core ambiguity: the vertical under-bar

The richest vein of charity is the **vertical (or near-vertical) bar written below a letter.**
The same-ish glyph can be any of:

- a **meteg** / gaʿya (metrical secondary stress; not an accent),
- a **tipexa** (accent; *prose only*),
- a **tarxa** (accent; *poetic only*),
- a **merkha** (accent; occurs in *both* prose and poetic systems),
- a **yored** (accent; *poetic only*),
- a **silluq** (accent; verse-final) — the easiest of these to distinguish, by context (it falls on the last word of the verse, before *sof pasuq*).

**UXLC already flags many of these against itself.** Its one-letter `<x>` notes mark exactly this
ambiguity in-text: **`m`** ("possible *merkha* rather than *meteg*", 42×, prose) and **`d`** ("*dexi*
re-read as *tipexa/tarxa*", 29×, poetic only). That is **~70 scribal under-bars UXLC itself is unsure about** —
the natural in-text seed for CLC's charitable resolution (see §3, §5, §7.1). UXLC's much larger
catch-all **`t`** note (233×, the largest code) is *not* an under-bar flag: it marks general
transcription uncertainty — any mark or letter, damaged or indistinct. A *few* `t` notes do concern a
sub-letter mark (e.g. "examine mark below … as possible merkha"), but most do not (a dagesh, an erased
upper accent, an artifact), so `t` is surfaced as a note yet seeds under-bar resolution only through a
per-note prose filter, never wholesale (see §5, [#18](https://github.com/bdenckla/UXLC-utils/issues/18)). Tellingly, UXLC's own
change log resolves them *by stroke angle* — *"the meteg … might be a merkha, but is not sufficiently
inclined"* — which is precisely the method §2a proposes to replace with accent grammar.

Two **distinct** sub-problems live under this heading. Keep them separate:

### 2a. Identity ambiguity — *which mark is it?*
A bar below the letter could be meteg vs. tipexa/tarxa vs. merkha vs. yored. UXLC leans on the
**angle/position** of the stroke in the image to decide. CLC's stance: **resolve primarily by
context — i.e. by accent grammar — not by mark angle.** If the accentuation of the verse makes
only one of these grammatically possible (or overwhelmingly likely), transcribe *that*, even if
the scribe's stroke is drawn at a slightly "wrong" angle.

→ This is the genuinely *new* CLC work. It leans directly on an **accent-grammar engine that
already exists** in the sibling repo `wlc-utils` (see §5).

**CLC resolves more charitably than UXLC's own binary framing.** The candidate set is *every*
under-bar mark the relevant system licenses, not just the two UXLC happened to name in a note:
- an **`m`** case (prose) ranges over **{meteg, merkha, tipexa}** — not only UXLC's meteg/merkha.
  (UXLC's change log already re-encodes both *merkha→meteg* and *tipexa→meteg* under the same `m`
  note, so all three are empirically in play.)
- a **`d`** case (poetic) ranges over **{tarxa, dexi, meteg, merkha, yored}** — never *tipexa*
  (not a poetic accent, though moot at the codepoint level — see next).
- **Codepoint collisions matter for the output.** These grammatical identities are not all distinct
  in Unicode: *tipexa = tarxa =* **U+0596** and *merkha = yored =* **U+05A5**. So a charitable
  re-reading can change a mark's *identity* without changing its codepoint — meaning some
  CLC-vs-UXLC departures live only in the **note prose / labeling** (the §8 "UXLC reading vs CLC
  reading" pair, §7.9 diff), not in the text bytes.

### 2b. Ownership ambiguity — *is a coded "early meteg" really just a normal meteg?* (minor footnote)
A much smaller, rarer issue than 2a. UXLC sometimes codes a meteg on a xatef-bearing
letter as an **early meteg** via a ZWJ trick (`meteg + U+034F` → the `ֽ͏ַ` sequence). In a **confirmed one or two cases**,
the better reading is simply a **normal meteg on the previous letter**. An old, **likely-unfinished**
exploratory program (`amb_early_mtg`) once scanned for other such candidates.

→ This is a **minor footnote, not a pillar.** CLC mostly **dissolves** the question by *not encoding
meteg position at all* (§7.13); what little remains of `amb_early_mtg` is just one "candidate UXLC
issues" lead among several in §7.12 — **not** the prototype of the note schema or of anything else.

> So: **CLC's charity is, first and foremost, (2a) under-bar identity resolved by accent grammar,
> seeded by UXLC's own ~70 `m`/`d` self-doubts (§2 intro), applied wherever the image is
> genuinely ambiguous.** The early-meteg question (2b) is a minor footnote, largely dissolved by §7.13.

---

## 3. How accent grammar resolves identity (2a)

The plan-shaped idea (kept deliberately brief):

1. For each word/verse, compute the **expected accentuation** under the relevant system
   (the 21 prose books vs. the 3 poetic books — אמ״ת = Job, Proverbs, Psalms).
2. Where the LC image shows an ambiguous under-bar, ask the grammar: *which of
   {meteg, tipexa/tarxa, merkha, yored} is licit / expected here?*
   (Start from UXLC's own under-bar `m`/`d` flags, §2. System-specific candidate sets: **prose →**
   {meteg, merkha, tipexa}; **poetic →** {meteg, merkha, tarxa, dexi, yored}.)
3. If exactly one is licit → transcribe it (charitable resolution).
4. If more than one is licit → use the grammar's **continuous grammaticality measure** to rank the legal options and
   provisionally go with the most likely; where they remain close, also weigh image evidence
   (angle, position). Either way, **record a note** disclosing the ambiguity — admitting our
   uncertainty to the interested reader rather than feigning certainty.
5. If the grammar says *none* of them is licit → that is a candidate **anomaly** (possible scribal
   error or possible transcription error upstream) — flag it, don't silently "fix" it.

This mirrors, almost exactly, the "supplied marks vs. anomalies" output of the
dual-cantillation detangler in `wlc-utils` (§5, §7.7): charitable supply where the grammar is
confident, explicit anomaly where it is not.

**[TBD]** Where does the accent-grammar engine live for CLC? Vendor `wlc-utils/py/accgram` in
the way `mb_cmn` is already vendored, or call it cross-repo? (See §5 vendoring notes.)

---

## 4. Scope / relationship to UXLC

- **Home (decided): CLC lives *in this repo*, not a separate one.** Python goes in **`py/clc/`**
  and the HTML/CSS/JS output goes in **`gh-pages/clc/`** — alongside the existing
  `gh-pages/amb-early-mtg/` and `gh-pages/fois/`. Consequence: the existing assets in §5 are
  **directly importable** (e.g. `import uxlc_amb_early_mtg…`, `uxlc_fois…`, `uxlc_changes…`,
  `uxlc_lci…`, `mb_cmn…`) rather than vendored. The only thing still arriving cross-repo is the
  accent-grammar engine from `wlc-utils` (see §9 #1).
- CLC stays **close to UXLC** — same base text, same book set, diplomatic intent. It is a
  *re-reading of the ambiguous marks* plus a *richer notes/presentation layer*, not a new
  collation from scratch.
- Versification: **primary = `vtrad-BHS`.** Also surface **`vtrad-MAM`** where it differs — in
  practice only the two Decalogue passages. **Mechanism (resolved, §7.8):** the BHS↔MAM verse map
  is hand-encoded in `py/clc/clc_versification.py` (not `mb_cmn`, whose vendored status and general
  scope make it the wrong home for four CLC-specific facts), and the overlay is **already rendered
  by the §7.7 strand split** (MAM's versification = the taḥton strand), so §7.8 itself is
  validation-only.

---

## 5. What already exists (inventory of reusable assets)

A pleasant surprise from exploring the repos: **most of CLC's plumbing already exists.** CLC is
largely an act of *composition* over existing machinery, plus the new identity-resolution work.

### In this repo (UXLC-utils)

- **UXLC's own `<x>` notes — the in-text charity seed (and most of the apparatus prose):**
  UXLC tags ambiguous/edited atoms with a one-letter note in an `<x>` element, already parsed by
  [`_handle_wc_x`](py/main_fois.py#L54-L59) into each atom's `types`. Corpus tally (39 books):

  | code | n | meaning | prose in change log |
  |---|---|---|---|
  | `t` | 233 | transcription uncertainty — general, **not** under-bar (any mark/letter; damaged/indistinct; §2, #18) | 207 |
  | `c` | 103 | cantillation / word-division oddity | 90 |
  | `m` | 42 | **under-bar: possible merkha vs meteg (prose)** — §2a seed | 39 |
  | `y` | 36 | yatir ketiv | 36 |
  | `q` | 35 | qere fix (mostly "removed unsupported dagesh" — §7.15) | 35 |
  | `d` | 29 | **under-bar: dexi↔tipexa/tarxa (poetic)** — §2a seed | 28 |
  | `4`–`8`, `X` | 38 | rarer transcription codes | 0 |

  → **Note-text source (settled — see §7.3, §9 #2):** the rendered note prose is **the actual
  tanach.us note page** for each `(atom, code)` (e.g. `Notes/Proverbs/Proverbs.5.19.4-m.html`),
  downloaded by [py/main_clc_download_notes.py](py/main_clc_download_notes.py) into committed
  [in/UXLC-notes/](in/UXLC-notes/) and read **offline** at build time by
  [py/clc/clc_note_pages.py](py/clc/clc_note_pages.py) (the build never touches the network →
  deterministic). The change-log `<correction><description>` (e.g. *"Add note 'm' for possible merkha
  rather than meteg under the gimel"*), ingested by [py/uxlc_changes/](py/uxlc_changes/), is an
  *imperative instruction to the editor*, **not** the reader-facing note — so it is **no longer the
  prose source**; it survives only as the atom-letter **consistency guard** (the table's "prose in
  change log" column is now just that guard's coverage, joinable by citation `ch:v.atom`). An atom
  whose note page has not been downloaded yet shows a bare **`[note not yet downloaded]`**
  placeholder (issue #19) — **never** a fabricated per-code gloss and never the change-log text; the
  prose must come from the real tanach.us page. The placeholder still links to that page, so it marks
  exactly where the prose will appear once fetched. That real page's own `<h2>` change-summary heading
  (e.g. *"Remove pashta from final mem. Add note 't'."*) is included **verbatim as the note's opening
  sentence** ([#30](https://github.com/bdenckla/UXLC-utils/issues/30)) — however imperative-sounding, it
  is content of this *same* downloaded, trust-boundary page, not a reintroduction of the separately-
  ingested `uxlc_changes` XML description above; only the page's own `<h1>` citation heading is excluded
  (redundant with the `ch:v.atom` context already shown alongside the note). Follow-ups, not yet done:
  stripping the redundant trailing "Add note 'X'." clause
  ([#31](https://github.com/bdenckla/UXLC-utils/issues/31)) and rephrasing the remaining imperative
  wording into descriptive prose ([#32](https://github.com/bdenckla/UXLC-utils/issues/32)).

- **Ambiguous early meteg (`amb_early_mtg`) — a *minor*, likely-unfinished side-investigation:**
  [py/uxlc_amb_early_mtg/amb_early_mtg.py](py/uxlc_amb_early_mtg/amb_early_mtg.py) — a hand-curated
  catalog of words with an ambiguous early meteg. Each record carries a charitable judgment:
  - verdicts: *"Better transcribed as a normal meteg on the first letter"* (`_BETTER_1`),
    *"…on letter 2"* (`_BETTER_2`), *"Perhaps better…"* (`_PERHAPS_BETTER_1`), *"Unclear from the
    LC image alone"* (`_UNCLEAR`);
  - cross-references to **MAM** (with a status reason *and* a Wikisource diff URL), to **AC**
    (Aleppo), to **Sassoon 1053**, to **BHS**, and to existing **UXLC change proposals**;
  - image filenames per word (LC, and sometimes BHS/AC/Sassoon comparanda).
  - Driver [py/main_amb_early_mtg.py](py/main_amb_early_mtg.py) → emits HTML to
    `gh-pages/amb-early-mtg/` (`index.html`, `dubious.html`, `full-record/`, `img/`).
  - Supporting modules: `amb_early_mtg_full.py`, `amb_early_mtg_summary.py`, `*_extend.py`,
    `*_three_and_beyond.py`, `*_html_for_img.py`, `*_url_generator.py` (Sefaria image URL gen).
  - Seed list also lives as [Possible false early meteg marks.csv](Possible%20false%20early%20meteg%20marks.csv)
    and the matching `.code-search`.

  → It is **one harvesting lead among several** (§7.12), **not** a pillar and **not** the CLC note
  schema; §7.13's "don't encode meteg position" largely moots it. Its record shape (word, bcvp,
  verdict, comparanda images, cross-refs, links) is a *prior example* the §8 schema can borrow
  from — nothing more.

- **Features of interest (FOIs):** [py/main_fois.py](py/main_fois.py) +
  [py/uxlc_fois/](py/uxlc_fois/) — collects `kq` (ketiv/qere), `mark-grammar`, `mark-grammar-2`.
  Outputs JSON + HTML to `gh-pages/fois/`.

- **UXLC change records:** [py/uxlc_changes/](py/uxlc_changes/) (`uxlc_change_prep.py`,
  `uxlc_authors.py`, `uxlc_bhl_appendix_a.py`, `uxlc_change_sanity.py`, `uxlc_changes_loc.py`).
  The raw change data is the dated `* - Changes.xml` files in `in/UXLC-misc/` (2020 → 2026).
  Download/refresh via [py/main_uxlc_download_changes.py](py/main_uxlc_download_changes.py);
  check via [py/main_uxlc_check_changes.py](py/main_uxlc_check_changes.py).

- **Image / atom-location guessing:**
  [py/main_uxlc_estimate_atom_loc.py](py/main_uxlc_estimate_atom_loc.py) +
  `uxlc_misc/my_uxlc_location.py` (`page_and_guesses`) + [py/uxlc_lci/](py/uxlc_lci/). Given
  book/chapter/verse/atom, guesses the LC folio/column/line → which image to show.

- **Page-break info:** [py/main_write_page_break_info.py](py/main_write_page_break_info.py)
  (LC line/page boundaries; builds `data/lci_augrecs.json`).

- **Existing site scaffold:** `gh-pages/` already has `index.html`, `style.css`, and a Hebrew
  font `woff2/Taamey_D.woff2`.

- **Vendored common code:** `py/mb_cmn/` (from `MAM-basics`) including `mb_cmn_bib_locales`
  (book IDs/locales) and `he_wikisource_url.he_diff_url` (used to build MAM diff links).

### In sibling repos

- **`wlc-utils` — accent grammar + bracket notes + detangling (the heavy lifting for §2a, §7.2, §7.7):**
  - WLC 4.22 in kq-u form: `wlc-utils/out/wlc422-kq-u/` (`0header.json` + `1verses_*.json` per
    book group). **Bracket notes are embedded inline** in the Hebrew text strings as `]X` codes
    (e.g. `]1`, `]c`, `]Q`).
  - Bracket-note definitions: `wlc-utils/py/cmn/wlc_bracket_note_definitions.py` (~31 codes,
    multi-source: Manual 4.22, the legacy WTS supplement, Amos.xml notes).
  - Bracket-note parsing/HTML: `wlc-utils/py/accgram/rtmsr_bracket_notes.py`.
  - **Accent-grammar engine:** `wlc-utils/py/accgram/` — the prose/poetic grammar checker.
  - **Untangled Decalogues + Gen 35:22:** `wlc-utils/py/accgram/dual_cant_detangle.py`
    (passages `gn 35:22` pashut/midrashit, `ex 20:2-17` & `dt 5:6-21` taxton/elyon). Uses
    MAM-simple as the oracle to split merged accents into two single-cantillation streams;
    produces parse trees + **4 charitably "supplied" marks** + **1 anomaly** (Deut 5:8 תעשה).
    Loader `wlc-utils/py/accgram/mam_simple_verse.py` (`vels_cant_alef` / `vels_cant_bet`).
  - Vendoring: `wlc-utils` itself vendors `mb_cmn` from `MAM-basics` and `in/UXLC-*` from this
    repo, refreshed by its `main_update_vendored_files.py`. So cross-repo vendoring is an
    established pattern here.

- **`MAM-with-doc` / `MAM-basics` — the notes presentation model (§7.3):**
  - 3-column layout: **reference | text | documentation.** No word-interrupting callouts; the
    text column stays readable.
  - **Short notes (≤ 400 chars)** render *inline* in the doc column, target word colored blue
    (`mam-doc-target-without-callout`), no marker.
  - **Long notes (> 400 chars)** get a red asterisk callout (`mam-doc-callout`) after the word +
    a link to a separate "big-doc" page with an anchor.
  - Threshold logic: `MAM-basics/py/py_misc/mwd_utils.py` `html_for_ver_ndd()`
    (`if not length_of_docs > 400`). Marking logic: `MAM-basics/py/py_misc/mam_doc_utils.py`
    `mark_doc_targets()`. Book writer: `MAM-basics/py/mwd/mwd_write_book.py`.
  - External links seen in MAM big-doc pages: NLI manuscripts, archive.org (Ginsburg), British
    Library, mgketer.org. (No Sefaria/Wikisource/tanach.us links in MAM's own output.)

---

## 6. Resolved: the `data/` dir vs. `codex-index-leningrad`

This doc originally asked: *is the LC-index info vendored here in `data/`, or is `data/` the source
and it's vendored into `codex-index-leningrad`?* Findings:

- **`data/` here is a built artifact local to UXLC-utils, not vendored from codex-index-leningrad.**
  - [data/lci_recs.json](data/lci_recs.json) is **copied** from `in/UXLC-misc/lci_recs.json` by
    [main_write_page_break_info.py:17](py/main_write_page_break_info.py#L17). Its header says
    `Derived-From: LCIndex` → `https://tanach.us/XSL/LCIndex.xml` → `USC-WSRP-Index`
    (USC West Semitic Research Project). So the *ultimate* source is tanach.us's LCIndex, not a
    local codex-index repo.
  - [data/lci_augrecs.json](data/lci_augrecs.json) is **generated** here by
    [main_write_page_break_info.py:16](py/main_write_page_break_info.py#L16) (augments each LCI
    record with word counts and start/stop line numbers).
- **The vendoring relationship with codex-index-leningrad runs the *other* direction.** Per
  [shared-with-codex-index-leningrad.md](../shared-with-codex-index-leningrad.md): **UXLC-utils
  is canonical**, and `codex-index-leningrad/UXLC-utils-sparse/` is a *sparse vendored copy of
  this repo* (refreshed by MAM-basics' `py/main_lenin_vendor_uxlc.py`, which was that repo's own
  `main_update_vendored_files.py` until 2026-08-22). That file is the whole
  authority now; it was cited here alongside `.github/copilot-instructions.md`, which was deleted
  on 2026-08-03 when the Python left this repo.
- **`codex-index-leningrad` is checked out as a sibling** in `GitRepos/`, alongside
  `codex-index-aleppo` (checked 2026-08-04; this bullet said it was absent until then). It holds
  the sparse vendored copy named above plus its own `lenin-wiki/` index. Even so, the
  image-guessing machinery CLC needs (§5) **already lives here**.

**So, for "higher-accuracy image guesses based on info in codex-index-leningrad":** the *current*
guesser uses LCI data that already lives here (`data/` ← `in/UXLC-misc/lci_recs.json` ← tanach.us).
If codex-index-leningrad holds *richer* per-line/per-column index data than tanach.us's LCIndex,
its index would have to be compared and merged. **[TBD]** — confirm what codex-index-leningrad's
`lenin-wiki/` index actually adds over the LCIndex. Nothing waits on a clone: the repo is on
disk, so this is a comparison that can be run now. (Note the same LCI data has also been
vendored into `wlc-utils/data/lci_recs.json`.) Convenience: the
`UXLC-utils.code-workspace` file lists `../codex-index-leningrad` as a second workspace folder,
and that path resolves.

---

## 7. Feature inventory

Each is a feature this doc names, organized with grounding + open questions.

### 7.1 Charitable under-bar transcription *(the headline feature)*
- Identity (2a) via accent grammar, **seeded by UXLC's own under-bar `m`/`d` notes** (§2, §5): start from
  the ~70 atoms UXLC already flags, resolve each over its system's candidate set (prose
  {meteg, merkha, tipexa}; poetic {meteg, merkha, tarxa, dexi, yored}) by grammatical licitness,
  charitably overriding UXLC's angle-based call where the grammar is confident.
- Every departure from UXLC → a CLC note carrying a verdict + rationale (§8 schema). For the seeded
  cases the rationale text is partly **free** from UXLC's own change-log description (§5).
- **[TBD]** Source the grammar from `wlc-utils/py/accgram` (vendor vs. cross-call).
- **[TBD]** Define the verdict vocabulary precisely (extend `_BETTER_1`/`_UNCLEAR`/… to cover
  the identity cases: "grammar licenses only tipexa here," etc.).

### 7.2 Restoration of WLC bracket notes
- Source: the vendored `wlc-utils/out/wlc422-kq-u/` (kq-u WLC 4.22), with definitions from
  `wlc-utils/py/cmn/wlc_bracket_note_definitions.py` (31 codes, up to 3 source-keyed prose
  definitions per code: Manual 4.22 — generally fullest — the legacy WTS supplement, and
  Amos.xml notes).
- **Caution:** apply a bracket note to a word **only after careful
  inspection** when that word **differs between UXLC and WLC** — the note may no longer apply.
  → a per-word UXLC-vs-WLC diff gate is required before attaching a bracket note (exact match
  only; no note on any mismatch — see §9 #8). wlc-utils has 4.20-vs-4.22 diff tooling
  (`py_wlc_diffs_420422/`, a different axis) and a WLC-vs-UXLC per-token diff
  (`py/accgram/wlc_uxlc_diff.py`) that is not yet bracket-note-aware — the missing
  per-atom eligibility decision is the new work.
- **Tracked in [#33](https://github.com/bdenckla/UXLC-utils/issues/33)** — the full cold-start
  plan: vendoring the WLC data + definitions (a first vendoring pair *from* wlc-utils *into*
  this repo, mirroring the existing MAM-basics vendoring pattern, §5), the diff gate, a
  `ClcNote` schema extension (`SOURCE_WLC_BRACKET_NOTE`), a new collector mirroring
  `clc_collect.py`'s shape, and reuse of the existing always-link renderer (no renderer
  changes needed). Most of the WLC-side data and code already exists (§5) — the diff gate is
  the long pole.
- **Follow-on, not a prerequisite: MAM enrichment ([#34](https://github.com/bdenckla/UXLC-utils/issues/34)).**
  Most bracket-note definitions are terse (e.g. `]n` "an anomalous form" — anomalous *how*? —
  is the canonical example). #34 cross-references MAM's ל= notes and doc-notes (§7.12) to
  attach a fuller explanation alongside a bracket note once #33 attaches it — additive only,
  depends on #33, and is a *different* use of MAM's ל= data than §7.12's charitable-diff
  harvesting (annotation here, vs. candidate-adoption there — keep the two purposes distinct
  even though the underlying MAM data overlaps).

### 7.3 UXLC notes — MAM-style, no word-interrupting callouts
- Adopt the MAM-with-doc presentation: text column stays clean; notes live in a side column /
  apparatus. **Every noted word is highlighted** in the text column (`clc-doc-target`,
  [`_noted_word`](py/clc/clc_render.py)) so the reader can see which words are annotated — this is
  MAM's own short-note treatment (colour the target word, no link).
- **Links, though, only ever go off-page (reversal — issue #6).** CLC originally linked *every*
  note uniformly ("always link", a deliberate deviation from MAM's inline-short / link-long
  threshold). That was **reversed**: a short note renders in the doc column of the *same row* as
  its target, always in the word's visual vicinity, so a same-page jump scrolls essentially
  nowhere and its `:target` highlight was dead weight. Same-page note anchors are therefore
  **dropped** — a noted word is a plain highlighted `<span>`, not a link. The **only** link that
  remains is the genuine cross-page one: a note relegated entirely to the long-notes page (below)
  makes its highlighted word an `<a>` pointing *across* to that page. Dropping the same-page
  anchors also removes the id-collision constraint that kept the singly-cantillated (א/ב) strand
  rows' noted words from being highlighted like any other (see §7.7 / [`clc_kq._member_span`](py/clc/clc_kq.py)).
- **Note text source — settled (once this doc's biggest unknown).** The `<x>` element carries
  only a one-letter *type* (cf. [`_handle_wc_x`](py/main_fois.py#L54-L59)); the rendered prose is the
  **actual tanach.us note page**, downloaded **offline** into committed [in/UXLC-notes/](in/UXLC-notes/)
  by [main_clc_download_notes](py/main_clc_download_notes.py) and read at build time by
  [clc_note_pages](py/clc/clc_note_pages.py). The change-log `<correction><description>` (ingested by
  [py/uxlc_changes/](py/uxlc_changes/)) turned out to be an editor-facing *instruction*, not the
  note, so it is **demoted to the atom-letter consistency guard only**; an atom whose page is not yet
  downloaded shows a `[note not yet downloaded]` placeholder, never a fabricated substitute (§5, §9
  #2; issue #19). That guard is a distinct thing from the tanach.us note page's *own* `<h2>`
  change-summary heading, which — unlike the `uxlc_changes` description above — **is** rendered,
  verbatim, as the note's opening sentence, since it is part of the same trusted downloaded page as
  the `<p>` prose ([#30](https://github.com/bdenckla/UXLC-utils/issues/30)). The `wlc-utils`
  bracket-note definitions cover the separate bracket-note layer (§7.2).
- **Body placement is a *separate* axis from the highlight.** The highlight (above) is just a flag
  on the word — every noted word carries it. It does **not** dictate where the note *body* renders,
  nor whether the highlight is also a link (it is a link only when the body lives off-page).
  - **Now (skeleton):** every body renders **inline in the doc column** of the same verse row
    ([`_note_block`](py/clc/clc_render.py#L197-L205)), regardless of length.
  - **Landed, case-by-case (not MAM's length threshold):** a note can be relegated to a long-notes
    page ([`clc_long_note.py`](py/clc/clc_long_note.py)) instead of rendering inline — one per main
    page (`gh-pages/clc/<label>-long-notes.html`, e.g.
    [`gh-pages/clc/Deuter-5-long-notes.html`](gh-pages/clc/Deuter-5-long-notes.html)), written only
    for a job with any long notes to hold, so its own intro can link back to that one main page
    unambiguously. The highlighted word then becomes a link pointing across to that page's anchored
    body (the sole surviving link — same-page bodies are not linked, only highlighted). **Deliberate
    deviation from MAM-with-doc:**
    MAM decides this automatically by a > 400-char length threshold; CLC never does — an editor
    opts a specific note in by hand (`clc_render._LONG_NOTE_SPECS`), so length is never inspected.
    Each long note recaps its verse (the relevant strand only) and its own short note, then adds
    whatever extra content justifies the relegation. **First instance:** Deut 5:13's taḥton pashta
    (an omitted-accent note, §7.7) — its long note cites UXLC's own Deut 5:13.2-t note (suppressed
    from its usual inline block, `clc_render._UXLC_NOTES_RELEGATED`, so it isn't shown twice),
    which in turn cites BHL Appendix A as independent grounding for saying "the LC has" rather than
    "UXLC's combined text carries" (`clc_dual_cant._HAS_LONG_NOTE`, alongside the pre-existing
    `_LC_CORROBORATED`/issue #36 pathway to the same wording). The stable anchor id scheme means
    this stays a render-time-only mechanism; the note JSON (§8) is unaffected. **Second instance:**
    Deut 5:7's elyon meteg (§7.7) — *further discussion* with no grounding role: it relegates no
    inline UXLC note (`relegated_position` is `None`, so it stays out of `_UXLC_NOTES_RELEGATED`),
    but it does carry an LC folio-102A (col 3, line 22) detail image of יהיה, credited like the
    5:13 image to Sefaria.org. It is a one-sentence pointer to Yeivin ITM §355 on the special gaʿya
    of יהיה-type verbs, closing with an aside that the word's initial yod is itself a charitable
    reading (most of its top has flaked off). **Third through sixth instances:** the four
    `_LC_CORROBORATED` cases (Exod 20:3, Deut 5:6 ×2, Deut 5:17 — §7.17) each gained their own long
    note too, all sharing one boilerplate paragraph (`clc_render._lc_corroborated_extra`): the
    `wlc-utils` grammar-checker citation that used to end the inline note directly (*"— see the
    grammar checker's supplied accents page"*) now lives *only* on the long-notes page, with just a
    "See more details in this longer note" pointer left inline. **The "and it is beyond the limits
    of CLC's charity to supply the missing X" clause itself relegates the same way, for every
    `has_long_note` case, not just these four** — including the *first* instance, Deut 5:13's
    pashta, retroactively: `clc_render._omitted_note_core` is the shared opening every non-meteg
    omitted-accent note has, with `_omitted_note_sentence` (core + the "beyond the limits" clause)
    now reserved for wherever the full explanation is wanted in one place — the long-notes page
    (`_charity_limit_paragraph`, its own paragraph there) and the main page's own inline note *only*
    when no long note exists to relegate it to. `_omitted_note_inline_pieces` is what actually
    renders inline (and what the long-notes page's own "repeated from main page" recap echoes
    verbatim), so the two never drift apart. Since a single (book, ch, v, strand) can now carry
    more than one long note (Deut 5:6's elyon wants both a tipeḥa and an etnaḥta),
    `clc_long_note.anchor_id` takes the omitted accent's `kind` too, and each section's heading
    carries `(kind)` so two same-verse-same-strand entries never look identical.

### 7.4 UXLC change records as a kind of note
- We **have** the change text (the dated `* - Changes.xml` in `in/UXLC-misc/`, processed by
  `uxlc_changes/`). Present a change record as just another note type attached to its word.
- Cross-link to the existing change-proposal references already present in `amb_early_mtg`
  records (e.g. `"existing UXLC change proposal": ("2024.04.01", "2024.01.29-4")`).
- **First instance:** Deut 5:8.2 (`t` note) is superseded by 2026.10.19 change #10 ("Change
  pashta over sin to qadma") — see `_NOTES_SUPERSEDED_BY_UXLC_CHANGE` in `py/clc/clc_collect.py`
  and the `superseding_uxlc_change` field on `ClcNote`. CLC now also *applies* that same
  correction to its own displayed text (`_UXLC_PENDING_CHANGES_APPLIED`, same file) — the
  first real `is_uxlc_departure=True` note in the skeleton
  (`diff_type=DIFF_UXLC_PENDING_CHANGE_APPLIED`); the combined/text-column reading is CLC's
  corrected qadma, with UXLC's original pashta preserved in the note's `uxlc_reading` and
  shown in its prose.

### 7.5 FOIs as a kind of note
- Surface FOIs (`kq`, `mark-grammar`, `mark-grammar-2`, …) as notes, **especially the rarer
  ones**. Reuse [py/uxlc_fois/](py/uxlc_fois/).
- **[TBD]** rarity ranking / which FOIs are worth showing inline vs. on demand.
- **Done so far — ketiv/qere display.** The `kq` FOI is already surfaced — not (yet) as a side-note
  but as the **text-column rendering itself**: each k/q unit is a boxed `<ruby>` (qere on the
  baseline, ketiv above; small bracketed placeholders for the qere-without-ketiv / ketiv-without-qere
  cases), [py/clc/clc_kq.py](py/clc/clc_kq.py). The other FOIs (`mark-grammar`, …) are **not** surfaced yet.

### 7.6 Images
- **Sefaria + MAM links:** mirror UXLC's tanach.us presentation by linking each verse to its
  Sefaria LC image and to MAM-with-doc. (The `amb_early_mtg_url_generator.py` already builds
  Sefaria image URLs — reuse it.)
- **Higher-accuracy image guesses:** §6 — current guesser uses LCI data already here; revisit if
  codex-index-leningrad offers a finer index.
- **B&W → color upgrade:** the relatively few black-and-white images embedded in notes / change
  records should be upgraded to color. Likely **manual with automatic assistance** (batch-match a
  B&W crop to the color Sefaria scan, propose the color replacement, human confirms). **[TBD]**
  pipeline.
- **Scraping:** images for changes/notes may need to be **scraped** (source **[TBD]** — tanach.us
  change pages? Sefaria? NLI?). Respect source terms.

### 7.7 Untangled Decalogues + Genesis 35:22
- Build on `wlc-utils/py/accgram/dual_cant_detangle.py`: present Exod 20, Deut 5, and Gen 35:22
  as **two clean single-cantillation streams** each (taxton/elyon; pashut/midrashit) instead of
  the merged tangle.
- The detangler's **"supplied marks" are themselves charitable acts** (marks the scribe didn't
  write because both strands share them) and its **anomalies** are exactly the kind of thing CLC
  should foot-note rather than hide. Strong fit with the CLC thesis — and CLC now does this itself
  for the narrow **maqaf/sof-pasuq** subset, supplying them **bracketed, green, and footnoted**
  rather than hidden (as raw UXLC) or silently baked in (as the detangler). **Deut 5:8 תעשה** is no
  longer an anomaly here at all: `clc_collect` applies UXLC's own pending correction (§7.4) to the
  base text before this oracle ever runs, so both the combined row and both strands simply show the
  corrected qadma as an ordinary shared mark; no omitted-accent case remains for this atom.

**Single-strand display.** Where a dual-cant verse is one row today, CLC shows **three**: the
combined form plus its two strands — labeled e.g. `35:22-C`, `35:22-א` (pashut), `35:22-ב`
(midrashit), each ref label carrying a hover description, the three grouped as one verse block.
**Genesis 35:22 is the first application** (`py/clc/clc_dual_cant.py`, rendered by
`clc_render.py`); the Decalogues follow by adding their oracle entries.

**Near-subtractive split — a deliberate, *narrowed* departure from the detangler.** The accgram
detangler — a *grammar-checker* — is *charitable* about the strand *text*: it **supplies** omitted
accents (so each strand parses) and freely **changes word division**. CLC, a *diplomatic* edition,
is far more restrained: it shows UXLC's own marks, **supplies only punctuation**, and where a strand
wants an *accent* UXLC omitted it **notes** the gap rather than inventing one. So the displayed strand
text is **near-subtractive, with two narrowly-scoped, loudly-flagged charities, plus one annotation**:
- **Position-safe subtraction.** Each strand is UXLC's own combined word with only the *other*
  strand's **divergence cluster** resolved: an accent, the **word-division punctuation that tracks
  it** (a maqaf / sof-pasuq / legarmeh belonging to that strand — so a sof-pasuq is *suppressed*
  when its silluq is, and never sits on a word whose last accent is e.g. etnaxta), and — where the
  two strands differ on one letter — the other strand's **vowel** (a QUPO word's patax vs.
  qamats) or **rafe/dagesh**. For rafe/dagesh the policy is **faithful**: where the two strands
  harden/soften a בגדכפת letter (driven by the previous word's accent — a disjunctive pause hardens,
  a conjunctive juncture softens), the **hard** strand keeps UXLC's dagesh and the **soft** strand
  keeps UXLC's rafe; where UXLC has no rafe (e.g. ex 20:9 כל) the soft letter stays **bare** — no
  rafe is ever supplied. Each such split is **no longer silent**
  ([#47](https://github.com/bdenckla/UXLC-utils/issues/47)): the **combined (`-C`) row** carries one
  note naming both strands and the shared letter, as a **target-as-heading** note like the
  omitted-accent/supplied-mark strand notes beside it — the target word is the note's heading
  and the body states just the bare visual fact, *"On the ת, the taḥton strand has a rafe
  but the elyon strand has a dagesh."* (no phonetics, no cause, no sourcing of the marks; the
  word is not named inline) — rather than the same fact duplicated per strand. That heading word
  is **stripped to its bare letters** ([#48](https://github.com/bdenckla/UXLC-utils/issues/48),
  `clc_strip.strip_to_bare_letters` — e.g. תרצח׃, keeping maqaf/sof-pasuq/legarmeh but
  dropping every point and accent), while the `-C` text column still shows the real fully-pointed word. The cluster is replaced *by name
  at its exact site*
  (`str.replace(cluster, resolution, 1)`), so a mark that recurs elsewhere in the word as a *shared*
  mark is never touched.
- **Marked supply — *punctuation only*, bracketed and footnoted, never silent.** Only an
  accent-coupled **word-division** mark a strand needs but UXLC lacks may be **supplied**, and only
  to improve legibility (e.g. the sof-pasuq that breaks Gen 35:22's pashut into its two chanted
  verses), rendered **bracketed and green** (CSS `clc-added-during-detangling`) with a synthesized
  "added out of thin air" note. The closed suppliable set is **maqaf / sof-pasuq / legarmeh** (the
  rule: *no punctuation supplied unless clearly marked as supplied* — cf. the green/bracketed
  additions in wlc-utils). Three sof-pasuqs are supplied so far — Gen 35:22 (pashut) and the taxton
  verse-ends of Exod 20:8 (לקדשו) and 20:9 (מלאכתך), where UXLC has none.
- **Omitted accent — *noted, never supplied*.** Where a strand's chanting calls for an **accent**
  UXLC left untangled (it has only the *other* strand's accent on that word), CLC does **not**
  invent one — the sharpened departure from the detangler, which *does* supply it to parse. CLC shows
  the word as UXLC has it (that accent simply absent) and emits a per-strand note that names *both*
  accents — the one wanted and the one UXLC actually has, in the mechanism's base template: *"A
  pashta is expected here, but UXLC's combined text carries only the elyon's munaḥ, and it is
  beyond the limits of CLC's charity to supply the missing pashta."* The passive "is expected"
  drops naming the strand that wants the accent (it's recoverable — the *other* strand from the one
  the LC has) and the verb "calls for"; the possessive sheds "strand" too (issue #54). The
  Decalogue cases: **Deut 5:6** (elyon's tipexa on אנכי + etnaxta on אלהיך), **5:13** (taxton's
  pashta on ימים), **5:17** (elyon's silluq on תרצח — UXLC has the sof-pasuq but not its silluq, so
  elyon shows a lone sof-pasuq). That base wording is no longer live anywhere, though: **every one
  of these six now credits the LC** ("the LC has only...") instead of UXLC, via three separate
  grounding paths — four (Exod 20:3, Deut 5:6 ×2, Deut 5:17) via independent wlc-utils corroboration,
  5:13's via its own editor-attached long note, both detailed in §7.17; 5:7's meteg note is reframed
  further still (below).
  - **Omitted *meteg* — softened, not "charity-limited".** The same divergence can leave a strand
    wanting a **meteg** (U+05BD) rather than an accent — **Deut 5:7** (elyon's gaʿya on
    יהיה, where UXLC's single mark is the taxton's merkha). A meteg is *not* an accent (§2): it is
    metrical, even the "obligatory" gaʿyot are written inconsistently, and this special gaʿya of
    יהיה-type verbs is, by Yeivin's own account (ITM §355), marked only inconsistently (its one
    "as a rule" setting — a maqqef-joined initially-stressed following word — may or may not cover
    יהיה־לך, an unsettled point the long note leaves to Yeivin rather than adjudicating). So the "calls for … / beyond
    the limits of CLC's charity to supply" framing — which treats the wanted mark as genuinely wanted —
    would over-claim. CLC instead reframes it as a transcription choice over a *single* extant mark
    (`clc_render._omitted_meteg_sentence`): *"A meteg might be expected in the elyon strand here on
    יִהְיֶה־, but the LC has only a single mark, which is best transcribed as a merkha since, unlike
    the meteg, the merkha is truly needed."* This case carries a further-discussion long note (§7.3)
    citing Yeivin's ITM §355 on that gaʿya.
- **First-class targeted notes — the word is a header, not inline prose.** A strand note (both the
  omitted-accent notes above and the supplied-punctuation "added out of thin air" notes) is
  rendered like a normal verse's note (§7.3, `clc_render._note_block`): the target word is repeated
  as the note's own **header** — demoted to bare letters, its body em-dash-joined on the same line
  (the target-as-heading layout at the end of §7.7) — and the prose no longer names the word inline,
  so a note reads *"A silluq is expected here …"* after a bare `תרצח׃` header, not
  *"… on תרצח here …"*. A supplied-mark note's header keeps the supplied mark right after the word in
  **plain square brackets** (`תרצח[׃]`-style, the green "added" formatting dropped for the header
  even though the text column still shows it green); its body is just *"maqaf added to improve
  legibility."* `clc_render._strand_note_block` / `_strand_note_header` build this from the
  atom-grouped strand notes (`clc_dual_cant._strand_notes` now tags each note with its `atom_index`);
  the snippet-free prose is the single source for both the main page and the long-notes-page recap,
  the latter staying running prose (its verse recap already shows the word) rather than re-headering.
- **QUPO vowel split** (ex 20:3, ex 20:4's מתחת, dt 5:7): where the two strands have *different
  vowels* (patax vs. qamats) on one letter (עַל־פָּנָ֗י's נ), it is the same position-safe subtraction
  bucket as rafe/dagesh — each strand keeps its own vowel, drops the other's. The one subtlety: the
  same vowel *type* can also occur **twice** in one word, once as an unrelated *shared* vowel and once,
  divergently, as the QUPO letter's own — a flat whole-word markset diff cannot tell those two
  occurrences apart, so the derivation isolates the divergence *per letter*, not per mark type. Like
  rafe/dagesh, this split is **no longer silent** ([#47](https://github.com/bdenckla/UXLC-utils/issues/47)):
  the **combined (`-C`) row** carries one target-as-heading note (as for rafe/dagesh above)
  naming both strands and the shared letter — e.g. body *"On the נ, the taḥton strand has a
  qamats but the elyon strand has a pataḥ."* under a bare-letter heading פני (stripped from the
  fully-pointed word per [#48](https://github.com/bdenckla/UXLC-utils/issues/48))
- **Unicode-PASEQ tokenization** (ex 20:4, 20:10; dt 5:8, 5:12, 5:14, 5:15): a Unicode PASEQ (׀) —
  the raw U+05C0 character, without regard to whether it functions as narrow-sense paseq or
  legarmeh (§7.16; that grammatical distinction is irrelevant here) — that one strand chants and
  the other doesn't. This class looked architecturally harder than the others — MAM's alef/bet
  strand word *counts* didn't match UXLC's own atom count, suggesting a real word-division
  divergence needing a new atom-alignment mechanism. It wasn't: MAM-simple tokenizes a standalone
  Unicode PASEQ as its own list entry, where UXLC always embeds it directly inside the *preceding*
  word's atom — a tokenization-convention mismatch, not a word-count divergence. Folding MAM's
  standalone Unicode PASEQ into its preceding word the same way (a throwaway harvest script's
  pasoleg-fold, applied before the oracle derivation, since retired) fixed the count for all 7
  affected verses;
  the Unicode PASEQ then flows through the *same* position-safe subtraction path as any other
  divergent mark — **no new runtime mechanism**. One of the 7, **dt 5:16**, resolves to *no
  divergence at all*: its taxton/elyon strands are byte-identical once folded, so it correctly
  carries no `_ORACLE` entry (`is_dual_cant` is False for it) — the two traditions simply don't
  diverge there.

All four proven divergence mechanisms — rafe/dagesh, omitted-accent notes, the QUPO vowel split, and
Unicode-PASEQ tokenization — plus pure-accent subtraction and supplied punctuation now cover **every**
Decalogue dual-cant verse. That set is **provably closed**
([#47](https://github.com/bdenckla/UXLC-utils/issues/47)): diffing the `alef`/`bet` *resolutions*
(not the shared-filler-carrying cluster string) of every `_ORACLE` atom and classifying each
divergent character yields only accents (incl. meteg/silluq), maqaf, legarmeh/pasoleg, sof-pasuq,
dagesh, rafe, qamats, and patax — no character outside that closed set, so no undiscovered "weird"
divergence mechanism remains. `_ORACLE` holds an entry for all 23 verses (across Exod 20 and Deut 5)
where the two traditions actually diverge; the other 9 verses in the two passage ranges (ex 20:7,
11, 12, 16, 17; dt 5:11, 16, 20, 21) have identical taxton/elyon readings and correctly carry no
entry. [#20](https://github.com/bdenckla/UXLC-utils/issues/20), the tracker for this feature, is
closed.

No consonant is changed and no *shared* mark removed (a mark both strands keep stays in both); only
the divergent marks — accent and the punctuation tracking it — are subtracted (subtraction, incl. of
punctuation, is not re-division). MAM (via the detangler) is consulted **only as the oracle** — for
*which* of two combined marks belongs to which strand, *where* a supplied break falls, and *which*
accent a strand wants where UXLC has only the other's. The detangler's remaining supplied-marks /
anomalies stay valuable as **logged footnotes**, never silent edits.

**MAM's Decalogue doc-notes independently corroborate the split (issues #43, #44) — a cross-check,
nothing rendered.** MAM records sof-pasuq presence *per witness, per strand*; its collation confirms
**L** is among the witnesses lacking the taḥton sof-pasuq at all five Exodus sites CLC **supplies**
one (Exod 20:3, 20:4, 20:8, 20:9, 20:10 = MAM verses 20:2, 20:3, 20:7–20:9), directly grounding the
charitable claim that L's taḥton strand ends no verse there. The apparent red-flag verses (MAM shows
L *carries* the taḥton sof-pasuq at Deut 5:8, 5:9) are consistent: CLC **keeps** UXLC's own sof-pasuq
there and supplies nothing. MAM's *two-marks-on-one-letter* doc-notes likewise corroborate the QUPO
vowel assignment — Deut 5:7 עַל־פָּנָי (qamats + silluq taḥton / patax elyon) and Exod 20:4 מתחת
(qamats + etnaḥta taḥton / patax + azla elyon) — and, at Deut 5:8 מתחת, MAM's own text follows the
witness *without* the extra patax, corroborating CLC's **non-QUPO** treatment of that atom. This is
**validation only**: MAM is consulted as signal (harvested by hand via a throwaway script,
since retired, from MAM-parsed/plus), the oracle needed no change, and
nothing of MAM is rendered inline or embedded at runtime. (Deut 5:7 / 5:12's supplied sof-pasuqs
carry no per-witness MAM note in the harvest, so they stay uncorroborated.)

**MAM also grammatically identifies every U+05C0 the split subtracts, and marks the coveting
verse's internal breaks (issue #42) — again a cross-check, nothing rendered.** The raw pasoleg (׀,
U+05C0) bars this oracle subtracts positionally (the *Unicode-PASEQ tokenization* class above) each
carry a legarmeh-vs-paseq identity the subtraction never needed — same bytes either way (§7.16). MAM
tags it explicitly (`מ:לגרמיה-2` = legarmeh, `מ:פסק` = narrow paseq), and its 15 Decalogue tags map
1:1 onto the subtracted sites; detail and the §7.16 TBD-resolutions are in §7.16. Separately, MAM's
**pisqah-be'emtsa-pasuq** markings (×8, strand-tagged) fall exactly where the taḥton strand ends a
verse *inside* the elyon strand's merged coveting verse (Exod 20:13/14/15, Deut 5:17/18/19 =
the לא־תרצח / תנאף / תגנב units), corroborating the verse-internal-break / omitted-silluq handling this
oracle already encodes there (Deut 5:17's lone-sof-pasuq elyon). Validation only, as above.

This is the same shape as the **legarmeh-vs-paseq** feature (§7.16): both *improve UXLC by importing
MAM's auxiliary adjudication* of an ambiguity that is **grammatical, not graphical**, differing only
in subject — which-accent-belongs-to-which-strand here, legarmeh-vs-paseq identity there. Every
divergence a reader would see now carries a synthesized note (all in `py/clc/clc_note.py`): a
**supplied** punctuation mark (`source` `dual-cant-addition`, `diff_type` `dual-cant-added-punct`); an
**omitted** accent (`source`/`diff_type` `dual-cant-omitted-accent`); and — no longer silently
([#47](https://github.com/bdenckla/UXLC-utils/issues/47)) — the two *one-letter* kinds:
**rafe/dagesh** (`source` `dual-cant-rafe-dagesh`, `diff_type` `dagesh`, §8's already-anticipated
bucket) and the **QUPO vowel split** (`source`/`diff_type` `dual-cant-qupo-vowel`). The supplied and
omitted notes are **per-strand** (they ride their own alef/bet row); the rafe/dagesh and QUPO notes
concern both strands equally, so each is stated **once on the combined (`-C`) row**, naming both
strands and the shared letter, rather than duplicated per strand. Each such combined-row note is a
**target-as-heading** note: its `word` field is rendered as the note's heading, **stripped to bare
letters** by `clc_strip.strip_to_bare_letters` ([#48](https://github.com/bdenckla/UXLC-utils/issues/48)
— see §8), while the body names only the shared `letter`; the `-C` text column keeps the word fully
pointed. All are lightweight dicts, **not** yet ClcNotes / §7.9 index rows — the subtractive
divergences carry no ClcNote departure record yet.

**Target-as-heading layout — shared by every headed note.** The bare-letter demotion generalizes
beyond the combined-row divergence notes above: *every* headed note renders the same way
([`clc_render._headed_note`](py/clc/clc_render.py) / `_stripped_heading`,
[#48](https://github.com/bdenckla/UXLC-utils/issues/48)) — the ordinary UXLC notes of §7.3 as well
as the omitted-accent/vowel and supplied-mark strand notes and the combined-row rafe/dagesh + QUPO
notes here. The heading is the target word **stripped to bare letters** in the **default font** (no
`lang="hbo"`/Taamey — that wrapper exists only to font-and-size *pointed* Hebrew, which bare letters
don't need; a `dir="rtl"` span still isolates the Hebrew from what follows it on the line). It keeps
only the word-level punctuation maqaf / sof-pasuq / legarmeh, so a heading reads e.g. `תרצח׃` or
`כל־`; a **supplied-mark** heading keeps the mark in **plain square brackets** with the green "added"
formatting dropped, e.g. `פני[׃]`. The note's **first body follows on the same line**, set off by a
space-surrounded **em dash**; any **further bodies spill into bullets** (`<ul class="clc-note-parts">`).
This mirrors the layout MAM-with-doc uses for a multi-paragraph doc-note
(`mwd_utils._bido_or_self_contained`: lemma + first part inline, parts 1.. as a `<ul>` — §8's parallel
`clc-*`/`mam-doc-*` vocabulary), CLC only swapping MAM's plain-space lemma/part join for an em dash.

### 7.8 Versification
- Primary `vtrad-BHS`; surface `vtrad-MAM` differences where they occur. In the whole Bible
  that difference is confined to the **two Decalogue passages** (Exodus 20, Deuteronomy 5) —
  everywhere else MAM and BHS number verses identically.
- **What MAM's Decalogue numbering is (verified).** MAM's merged-elyon verse numbering — the
  numbering MAM-with-doc's HTML anchors use (`#c{ch}v{v}`) — coincides **exactly with the
  taḥton (alef) strand's verse boundaries** of the §7.7 split, *not* the elyon strand's. BHS
  (CLC's primary) is the *finer* division: it places a boundary wherever *either* strand ends,
  so BHS = taḥton-boundaries ∪ elyon-boundaries. MAM keeps only the taḥton boundaries, so
  relative to BHS it **merges exactly the runs the elyon strand chants as one commandment-verse
  while taḥton reads through**:
  - **early split** (elyon reads "I am" / "no other gods" as separate commandment-verses):
    `MAM Ex 20:2 = BHS 20:2+20:3`; `MAM Dt 5:6 = BHS 5:6+5:7`. Shared with Sefaria.
  - **late split** (elyon reads each short commandment — murder/adultery/steal/false-witness —
    as its own verse): `MAM Ex 20:12 = BHS 20:13–16`; `MAM Dt 5:16 = BHS 5:17–20`. **BHS-only,
    absent from Sefaria.**

  Everywhere after a split the numbering shifts down (−1 per early 2-way, −3 per late 4-way).
- **Rendered surface: already rendered by §7.7 — so §7.8 is validation-only.** Because MAM's
  versification *is* the taḥton strand, and §7.7 renders both strands side by side for every
  diverging Decalogue verse, the vtrad-MAM boundary overlay is **already visible**: every place
  MAM merges is an atom where §7.7 shows the elyon strand ending a verse (silluq + sof-pasuq)
  that the taḥton strand (= MAM) reads through. So #45 adds **no new rendered surface** — the
  same validation-only shape as the §7.7 MAM cross-checks (issues #42/#43/#44). The two accounts
  are proven to agree **1:1** (`clc_versification_test.test_overlay_matches_dual_cant_oracle`:
  the taḥton reads-through points == the elyon-ends atoms of `clc_dual_cant._ORACLE`; 8 each).
- **Where the map lives (and why hand-encoded).** `py/clc/clc_versification.py` hand-encodes the
  four merge groups and derives the full BHS↔MAM map (`clc_to_mam`, `mam_merge_group`,
  `mam_boundary_after`, `mam_differs_from_bhs`). The authoritative converter lives in MAM-basics'
  `py_misc` / `versification_differences` — a **non-`mb_` dir**, hence neither importable nor
  vendorable into official CLC code (§4; only `mb_*` dirs are). So, as with §7.7's `_ORACLE` and
  the Unit A/B cross-checks, MAM is **consulted as signal and embedded nowhere at runtime**: the
  a throwaway harvest script (since retired) emitted a `.novc/` versemap dump from the
  converter, and the tiny result is hand-encoded here **once**, validated against that dump
  (all 53 Decalogue verses, both directions). Moving the general converter upstream into an
  `mb_*` entry point was the alternative, not worth it for four facts.
- **Reuse.** `clc_to_mam` is the CLC-verse → MAM-verse helper **issue #38 also needs** (to key a
  CLC verse to its MAM-with-doc doc-note anchor) — built once here, not a #45-only hack.

### 7.9 Differences-from-UXLC index *(sortable / filterable)* — *important*
A first-class **"what does CLC change vs. UXLC, and where"** index. This is the public face of
"charitable but transparent" (§1): it makes every departure auditable in one place. Mechanically
it is a **view over the CLC note schema** (§8) — every note that records a *departure* from UXLC
becomes one row.

Per-difference data (columns): location (book, ch:v, atom), the **UXLC reading vs. the CLC
reading**, the **difference type**, prose/poetic, and a link out to the full note + image.

**Filters:**
- **by biblical book.**
- **by prose vs. poetic — at the *verse* level, not book level**, because **Job mixes both.**
  Already solvable with existing code: [mb_cmn/cantsys.py](py/mb_cmn/cantsys.py) (prose/poetic
  system abstraction) + [`_is_prose_section_of_job`](py/mb_cmn/mb_cmn_bib_locales.py#L359), which
  encodes Job 1–2, 3:1, and 42:7–17 as **prose** and the rest of Job as poetic. So: a verse is
  poetic iff its book is Psalms/Proverbs/Job **and** it is not a Job prose section; the other 36
  books are all prose. (Function is currently `_`-private — promote/wrap it for CLC.)
- **by difference type** — `under-bar` is the headline type (§2); others **[TBD]**; keep a `misc`
  bucket so nothing is ever unclassified.

**Sorts:**
- **by difference type.**
- **by biblical order = LC *manuscript* order.** Because CLC is a **diplomatic** edition,
  **manuscript order wins** over printed/standard order wherever they differ. ⚠️ **Gap:** the code
  today encodes **standard printed order only** —
  [`ordered_short`](py/mb_cmn/mb_cmn_bib_locales.py#L343) (`'A1'`…`'FD'`) and
  [`get_bknu`](py/mb_cmn/mb_cmn_bib_locales.py#L63) (`1`…`39`, with 2 Chronicles **last**). L's
  manuscript order differs — e.g. **Chronicles heads the Writings**, and the Latter Prophets run
  **Jeremiah → Ezekiel → Isaiah**. So an **LC-manuscript-order key must be added** (see §9 #10).
  ("MAM book order" likely tracks the printed order too, which is exactly why manuscript order has
  to be its own thing here.)

**Implementation sketch:** one generated page under `gh-pages/clc/`, backed by a JSON array of
difference records, with **client-side JS** doing the sort/filter (this is the "JS" part of the
gh-pages/clc output). Keep the records as plain data so the *same* JSON drives both this index and
the per-verse note rendering.

### 7.10 Introductory prose — editorial principles & feature tour *(front matter)*
A human-facing **introduction** to the edition: an essay / landing page that lays out the
**editorial principles** and tours the features. The **chief principle is charity** (§1) — it gets
the most space and the clearest worked examples.

Characteristics:
- **Prose**, not just a feature list — explain *why* charity, and what "least weird" means in
  practice; state plainly that charity is bounded by transparency (every departure is logged).
- **Pointed Hebrew examples** inline (use the Taamey font already in `gh-pages/woff2/`), ideally
  the very cases already curated in `amb_early_mtg` (e.g. וַיַּעֲשׂוּ, בְּנֵי־), each shown as
  **UXLC reading vs. CLC reading** so the difference is concrete.
- **Images**: LC crops — and comparanda (AC, Sassoon 1053, BHS) — beside the examples, so the
  reader sees the ambiguous under-bar with their own eyes. Reuse the image assets/links from §7.6.
- Also introduce the rest: the no-word-interrupting-callout notes model (§7.3), bracket-note
  restoration (§7.2), change-records & FOIs as notes (§7.4–7.5), the detangled Decalogues + Gen
  35:22 (§7.7), versification (§7.8) — and link prominently to the differences-from-UXLC index
  (§7.9) as "see exactly what we changed."
- Lives as the **`gh-pages/clc/` landing page** (`index.html`) — the front door of the edition.

Pairs with §7.9: the intro **argues** charity; the index **shows the receipts**.

**Status: not started.** No `gh-pages/clc/index.html` exists yet. The only front-matter so far is a
short **per-book intro paragraph** at the top of each generated page
([`_intro_para`](py/clc/clc_render.py)) describing the skeleton — not the editorial-principles essay.

### 7.11 BHL agreement: body vs. Appendix A *(a correctness fix, not a preference)*
A reading that **agrees with the BHL body but is flagged in BHL Appendix A** should count as
**not agreeing with BHL as a whole.** Appendix A is part of BHL's verdict, not a separable
optional layer. The claim: **UXLC gets this wrong** — it presents agreement-with-body and
agreement-with-appendix as if they were the *same level* of agreement (or at least does not rank
them). CLC should model BHL agreement with that granularity:
- agrees with body **and** clean in Appendix A → genuine agreement with BHL;
- agrees with body **but** flagged in Appendix A → **not** agreement with BHL.

**What Appendix A *is* (and a naming caveat).** The BHL *body* is a **general-purpose** edition, so
where L's actual contents are unsuitable for such an edition the body departs from L; **Appendix A
records L's actual contents in exactly those cases** — it tells you *what L itself reads*, and nothing
about other witnesses. Terminology: "BHL" is used **broadly** (the whole book) or **narrowly** (the
body, as opposed to other parts — chiefly Appendix A). This doc writes "BHL body" for the narrow
sense, but **UXLC change records/notes are *not* careful about the distinction** — an unqualified
"BHL" there may mean either, so disambiguate by context. Relatedly, when a **MAM doc-note says
"Dotan"** it means Dotan's judgment of L's contents = **the Appendix A entry if one is present,
otherwise the BHL body** — so a MAM "Dotan" tag on a case that has an Appendix A entry points at that
*same* Appendix A reading, not an independent witness (its added value is the *collation* of the other
witnesses it lists alongside; see #39). And note BHL is **not** BHS: MAM's own sigil documentation
records that BHS preserves L less accurately than Dotan/BHL and BHQ.

This is framed as a **correctness** issue, not editorial taste — worth its own difference-type /
note category in §7.9 / §8.

Grounding: the repo already ingests **BHL Appendix A, but for Psalms only** so far —
[uxlc_bhl_appendix_a.py](py/uxlc_changes/uxlc_bhl_appendix_a.py) reads
`in/UXLC-misc/BHL Appendix A Psalms.csv` (book ch:v plus optional word-index locales). Extending
Appendix A coverage beyond Psalms belongs to §7.12's long tail. **[TBD]** locate how UXLC encodes
its BHL agreement, so CLC can show the corrected judgment precisely.

### 7.12 Harvesting desirable changes from other editions
Sources to mine for changes CLC might want to adopt. Each yields **candidate** notes / charitable
diffs, **reviewed before adoption** (cf. the bracket-note caution in §7.2 — a suggestion is a
candidate, not an automatic change):
- **MAM ל= ("lamed equals", i.e. "L reads…") notes** — harvest from **`MAM-parsed/plus`** (or an
  edition that renders notes, e.g. `MAM-with-doc/gh-pages`). These ל= notes point precisely at
  what L actually has, i.e. often at exactly the changes CLC would like. **Distinct from
  [#34](https://github.com/bdenckla/UXLC-utils/issues/34)'s use of the same ל= data**: #34 only
  *annotates* a WLC bracket note with MAM's commentary (read-only, no text change); this
  harvest is about *adopting* MAM's reading as a candidate CLC diff. Same source data, different
  purpose — an implementer touching one should be aware of the other so the MAM-alignment code
  isn't built twice.
  - **Decalogue doc-notes are the first, best-aligned slice of this harvest.** MAM's own doc-notes on
    Exod 20 / Deut 5 are *pre-aligned to CLC's dual-cant divergence sites* (§7.7): they flag, atom by
    atom, where L diverges from the other witnesses (MAM's `ל`/`ל!=` sigil — `X!=Y` means "X
    *surprisingly* reads Y", **not** "not-equal"), and they carry legarmeh, sof-pasuq-per-witness,
    two-marks-on-one-letter, and Breuer-vs-Dotan calls that map onto specific CLC features. Tracked in
    a family of issues: **[#38](https://github.com/bdenckla/UXLC-utils/issues/38)** (doc-note "See
    also" links + wording), **[#39](https://github.com/bdenckla/UXLC-utils/issues/39)** (Deut 5:13
    grounding), **[#40](https://github.com/bdenckla/UXLC-utils/issues/40)** (qadma, §7.4),
    **[#41](https://github.com/bdenckla/UXLC-utils/issues/41)** (Breuer-vs-Dotan gaʿya position, §7.13/§2a),
    **[#42](https://github.com/bdenckla/UXLC-utils/issues/42)** (legarmeh + pisqah, §7.16/§7.7),
    **[#43](https://github.com/bdenckla/UXLC-utils/issues/43)** (supplied sof-pasuqs, §7.7),
    **[#44](https://github.com/bdenckla/UXLC-utils/issues/44)** (QUPO vowel split, §7.7),
    **[#45](https://github.com/bdenckla/UXLC-utils/issues/45)** (vtrad-MAM versification, §7.8).
    Decode MAM sigla/operators via `MAM-basics/doc/sigil-decoding.md`; and beware MAM's Decalogue verse
    numbering (merged *elyon*) runs ~1 behind CLC's `vtrad-BHS`, so a CLC→MAM verse-map is needed (built
    once, shared by #38 and #45).
- **`book-of-job`** (sibling repo; its own `gh-pages`, with the generators and check scripts that
  write and verify it in `MAM-basics/py/` since that repo's Python moved there on 2026-08-19) —
  a **small, realistic, short-term** harvest set. Likely the first real harvesting target.
- **`amb_early_mtg`** (the early-meteg catalog, §2b/§5) — a small, **likely-unfinished** local scan
  for possible early-meteg mis-codings; a minor lead of the same flavor as the others here, mostly
  mooted by §7.13. Listed for completeness, not prioritized.
- **All of BHL Appendix A** (beyond the current Psalms-only slice, §7.11) **+ Da'at Miqra** — a
  comprehensive review would be ideal but is an explicit **long-term / "probably never get around
  to it"** goal. Don't block on it.

### 7.13 Don't encode early or medial meteg *(drop a BHS distinction now read as noise)*
CLC **does not encode early or medial meteg**: it places meteg in its default position and drops
the positional distinction. Faithfully preserving early/medial meteg placement is a **BHS feature
that some 50 years of scholarship has reframed as closer to a bug** — there is **no evidence the
placement is anything but scribal whim**, i.e. no evidence it means anything. So CLC treats meteg
position as non-significant rather than reproducing it.
- **Relationship to §2b:** declining to encode early/medial placement *largely dissolves* the 2b
  "which letter owns the early meteg?" question — meteg simply goes in its default position. 2b's
  value then shifts toward **evidence**: the candidates it surfaces are data points that the
  placement is whimsical, which is the very justification for this policy.
- Still a **logged departure** from UXLC (§1 transparency): each normalization → a note + a
  difference-index row (§7.9), difference type e.g. `meteg-position`.
- **[TBD]** pin down exactly how UXLC encodes early vs. medial meteg (the U+034F trick of §2b
  covers the early case; confirm the medial one) so every instance can be detected and normalized.

### 7.14 Remove questionable control-character use from UXLC
CLC **strips control characters UXLC uses for non-semantic reasons.** The clear case: a **joiner
used not to encode a meteg but to nudge most fonts into more felicitous spacing** — exploiting
quirky font handling for a purely cosmetic result. That is a presentation hack riding on undefined
behavior, not part of the text, so CLC removes it.
- Two distinct uses to keep separate: (a) a joiner that **encodes medial/early meteg** — a
  *legitimate* use of the joiner *if* you actually want medial meteg (but CLC drops medial meteg
  anyway, §7.13); and (b) the **spacing hack** — no textual meaning, remove. Both disappear in CLC,
  for different reasons.
- **Codepoint precision matters:** §2b's early-meteg trick is actually **U+034F (combining grapheme
  joiner)**, not a true ZWJ; the spacing hack may be an actual **ZWJ (U+200D)**. **[TBD]** audit
  UXLC for *every* control-character use and classify each as semantic (keep/transform) vs. cosmetic
  (drop); at least one spacing-hack joiner is known — find the rest.
- Log each removal as a departure (§7.9), difference type e.g. `control-char`.
- **Done so far — only the dual-cant case.** The strand splitter already drops an **orphaned CGJ**
  (U+034F) that the combined form used merely to *sequence* two combined accents: once one accent is
  removed it has nothing left to sequence, so the strand omits it
  ([py/clc/clc_dual_cant.py](py/clc/clc_dual_cant.py), §7.7). The general control-character
  **audit/strip** across UXLC (the spacing-hack ZWJ, etc.) is **not started**.

### 7.15 Charitable restoration of "unsupported" dagesh (the `q` notes)
UXLC's **`q` notes** (35×) are almost all UXLC *removing* an **"unsupported" dagesh** from a qere
(or qere-without-ketiv) word — e.g. *"Remove unsupported dagesh in yod of qere word"*, *"… from bet
in qere-without-ketiv word"*. In the spirit of charity, CLC will **supply (restore) the dagesh** in
some or all of these — UXLC's removal is the *uncharitable* reading. **Manual review per case** (a
few `q` notes instead touch a maqaf, sheva, or yod, not a dagesh). Each restoration → a logged
departure (§7.9), difference type e.g. `dagesh`. The data is in hand: the `q` note marks the atom and
the change-log description names exactly what was removed (§5).

### 7.16 Legarmeh vs. paseq distinction *(borrow MAM's calls)*
A **second** ambiguous-vertical-bar problem, **distinct from the under-bar (§2)**: a vertical bar
standing **after / between words** can be either an ordinary **paseq** (a separating stroke — *not*
an accent) or the paseq that, together with a preceding conjunctive, forms the disjunctive
**legarmeh** (in the prose books, *munax legarmeh* = *munax* + paseq; the poetic system has its own
legarmeh forms over its own conjunctives — **[TBD]** pin down the poetic inventory). A word carrying
a genuine *munax* that merely *happens* to be followed by an independent paseq looks **identical** to
*munax legarmeh*; the difference is **grammatical, not graphical** — exactly the kind of ambiguity
CLC exists to resolve charitably.

**Goal: borrow MAM's legarmeh-vs-paseq distinctions.** MAM (Miqra according to the Masorah) already
adjudicates this throughout, so — as with the ל= harvest (§7.12), the strict strand split's MAM
oracle (§7.7), and the vtrad-MAM overlay (§7.8) — CLC takes **MAM's call as the charitable oracle**,
cross-checked by accent grammar where it's checkable. Same shape as the headline under-bar
resolution (§7.1, §3): grammar/oracle fixes the identity; every departure from UXLC is **logged**
(§7.9) with a verdict + rationale.
- **Does `wlc-utils/py/accgram` (§5) already distinguish legarmeh from paseq? — resolved: yes,
  independently.** Its prose scanner (`prose_scanner.py`) tokenizes *munax + paseq* **before revia**
  as `LEGARMEH`; *not* before revia as `LEGARMEH` only inside a ported 17-passage `has_legarmeh` list
  (else plain `MUNAX` + a swallowed narrow paseq), and `prose_ply_grammar.py` carries `LEGARMEH` as
  its own terminal. So CLC has a **second, independent oracle** for the distinction (WLC bytes +
  grammar rule + passage list) alongside MAM's explicit tags — the reuse path this TBD asked for.
  Caveat: accgram is independent only on the **ordinary** prose run; its dual-cant *detangler* takes
  strand punctuation *from* MAM (§7.7), so in the Decalogue strands it concurs rather than witnesses.
- **Codepoint precision (cf. §2a) — resolved.** There is **no dedicated "legarmeh" codepoint** — it
  is *munax* (U+05A3) + *paseq* (U+05C0), the same bytes as *munax* followed by an ordinary paseq, so
  a charitable re-reading changes only the **note prose / labeling**, never bytes. UXLC does **not**
  distinguish them (same bytes either way); MAM's `מ:לגרמיה-2` template is confirmed to denote
  legarmeh (`MAM-basics/py/author_misc/mp_cmn_rows_core.py`: *"the vertical line ׀ as legarmeh … shares
  Unicode with paseq but differs in function"*), the azla-/mahapakh-/munaḥ-legarmeh sub-type read off
  the conjunctive on the word itself (munaḥ in the prose Decalogues), **not** off the `-2`.
- Difference type for §7.9 / §8: **`legarmeh-paseq`**.
- **[TBD] Visual representation, tracked in [#37](https://github.com/bdenckla/UXLC-utils/issues/37).**
  Once identity is resolved, how should CLC's rendered output *show* the distinction to the reader,
  given both share the identical glyph? Precedents and options are on the issue, not here. **This is
  the one open blocker for a *rendered* §7.16 feature** — the identity oracle is settled (above), but
  how to display two identical glyphs apart is not.
- **MAM Decalogue cross-check (issue #42) — done, validation only.** MAM already adjudicates this
  throughout the Decalogue, so #42 harvested its calls as a first, pre-made slice of the §7.16 oracle:
  **11 legarmeh** (`מ:לגרמיה-2`) + **4 paseq** (`מ:פסק`), every one landing on a U+05C0 the §7.7 split
  already subtracts positionally. Of the 15: **11** sit on dual-cant divergence atoms — legarmeh on
  בַּמַּיִם, שַׁבָּת, אַתָּה, צִוְּךָ, הָיִיתָ; paseq on פֶסֶל and בַּשָּׁמַיִם (both Decalogues) — where
  they stay **display-only** (§7.7 strands carry no ClcNote); **1** (Deut 5:16 לְמַעַן) sits on the
  folded byte-identical verse, its bar shared by both strands; and **3** (Deut 5:4 פָּנִים, 5:25
  יֹסְפִים, 5:27 וְאַתְּ) sit on **ordinary single-cant rows** — the natural first surface for a
  *rendered* `legarmeh-paseq` note, still gated on #37. (Exod 20:4's בַּשָּׁמַיִם carries its `מ:פסק`
  tag **nested as the target — param 1 — of a נוסח** note about L's disputed stroke, i.e. tagged one
  level deeper, not untagged; there is no Exod/Deut tagging asymmetry.) accgram's independent grammar
  rule agrees (no Decalogue verse is in its `has_legarmeh` list, so it reduces to *before-revia =
  legarmeh*). Nothing rendered or embedded; recorded in `clc_dual_cant._ORACLE`'s comment and §7.7.

### 7.17 LC-corroborated framing for omitted-accent notes — **done**
§7.7's omitted-accent notes framed the "carries only" clause around **UXLC**, implying a UXLC
transcription quirk even where that isn't the case. The originally-planned mechanism — matching
against `wlc-utils`'s `SuppliedMark.source == "lc"` flag — turned out to be a dead end (it fires
for a leftover-mark case that isn't a live CLC omission at all, and doesn't fire for any of the
six live cases). What worked instead: Ben's own editorial judgment, word by word, on whether
WLC's differing reading at each `wlc-utils` supplied-accent case is a *reasonable transcription*
of the LC or a *mis-transcription* — landed as prose in `wlc-utils/py/accgram/dual_cant_detangle.py`'s
`_supply_reason` (`wlc-utils` [#53](https://github.com/bdenckla/wlc-utils/issues/53), closed). Four of
CLC's six live omitted-accent notes match a "reasonable transcription" case by word: **Exodus
20:3**, **Deuteronomy 5:6** ×2, **Deuteronomy 5:17**. For those four, the note now reads *"the LC
has only..."* instead of *"UXLC's combined text carries only..."*. The evidentiary link to
`wlc-utils`'s [supplied accents](https://bdenckla.github.io/MAM-basics/wlc/accgram/supplied-marks.html)
page used to trail the inline note directly; each of these four now instead carries its own
long note (§7.3's `_HAS_LONG_NOTE` mechanism, joined by `_LC_CORROBORATED` for this reason), and
that link lives there — the inline note just points across via "See more details in this longer
note." **Deuteronomy 5:7** and **5:13** never appear in `wlc-utils`'s
supplied-accent inventory (their strand parses clean by other means, so the detangler never needed
to supply anything for them), so neither qualifies for this corroboration path —
`_LC_CORROBORATED` excludes both. Both were separately credited to the LC anyway, shortly after,
through the unrelated §7.3 long-notes mechanism (`_HAS_LONG_NOTE`): 5:13's pashta note now also
reads "the LC has only...", grounded in UXLC's own note's citation of BHL Appendix A rather than in
wlc-utils; 5:7's meteg note is reframed still further, as a transcription choice rather than a
withheld accent (§7.7 above). As of the latest commit, no live omitted-accent note uses the
original "UXLC's combined text carries only..." wording — every one credits the LC, just via a
different evidentiary basis per case.

Implementation: `clc_dual_cant.py`'s `_LC_CORROBORATED` is a hardcoded set keyed by
`(book_id, ch, v, strand.short, kind)`, checked in `_omitted_note` to set a `lc_corroborated` bool
on the note dict (threaded down from `strand_views` via a new `verse_loc` parameter). That flag now
only feeds the "the LC has" vs. "UXLC's combined text carries" wording choice (`grounded` in
`clc_render._omitted_note_sentence`); the citation link itself is entirely `_HAS_LONG_NOTE`'s
concern (§7.3) — all four `_LC_CORROBORATED` cases are also in `_HAS_LONG_NOTE`, so
`_omitted_note_block` always renders their citation on the long-notes page, never inline. Wording-
only refinement of §7.7's mechanism — no new `diff_type`, no new ClcNote/§7.9 index rows;
`clc_dual_cant_test.py`'s `test_decalogue_omitted_accent` pins both the `lc_corroborated` (dt 5:17)
and non-corroborated-but-long-noted (dt 5:13) wording, each linking to its own long note, so the
two grounding paths can't silently collapse into one.
Tracked in [#36](https://github.com/bdenckla/UXLC-utils/issues/36), closed.

---

## 8. Presentation / tech notes
- Output is a static site under **`gh-pages/clc/`** (same pattern as `gh-pages/amb-early-mtg/`
  and `gh-pages/fois/`, and as MAM).
- Reuse the Taamey font (`gh-pages/woff2/Taamey_D.woff2`) + `style.css`.
- Borrow MAM's 3-column CSS vocabulary (`mam-doc-*`) or define a parallel `clc-doc-*` set.
- **Note-body placement (see §7.3):** short notes inline in the doc column, **long notes relegated
  to a separate "big-doc" page** (MAM-with-doc model, §5); the always-link points to wherever the
  body lives. The skeleton currently inlines *all* bodies — long-note off-loading is still to-do.
- **Main-page width — done.** A main page's `<body>` (`clc_render._body_wrapper`) carries a
  `clc-main-page` class that `style.css` uses (`body:has(> div.clc-main-page)`) to widen it past
  the site-wide 40em cap to 60rem — real room for `td.clc-doc`'s own wider cap (45em, up from 32em)
  to render without narrowing the text/ref columns. The long-notes page carries no such class, so
  it stays at the site-wide width, deliberately narrower than the main pages (its content is
  running prose, not a 3-column table).
- **Long-notes → main-page back-link — done.** Each long-note entry's "Inline note (repeated from
  main page)" label — the one place the long-notes page names "the main page" for a specific entry
  — has "main page" itself link back to that entry's originating page (`out_label(book_id,
  chapters)` + `.html`, the same label scheme `write_book` uses for its own filename).
- Note schema: a single **CLC note** type that all sources (charitable under-bar verdicts, bracket
  notes, UXLC `<x>` notes + their tanach.us note-page prose, change records, FOIs, dagesh
  restorations) flow into — **one renderer, many sources**. Fields: atom text, bcvp, note text,
  source (e.g. `uxlc-x-note`, `dual-cant-addition`, `dual-cant-omitted-accent`), plus for the
  difference index (§7.9) a **`diff_type`** (`under-bar` | `transcription-uncertainty` |
  `dual-cant-added-punct` | `dual-cant-omitted-accent` | `dual-cant-qupo-vowel` | `legarmeh-paseq` |
  `dagesh` | `meteg-position` | `control-char` | `bhl-appendix` | … | `misc`), an
  **`is_uxlc_departure`** flag,
  and the **UXLC reading vs. CLC
  reading** pair. The difference index is then just "render the notes where `is_uxlc_departure`, as a
  table." (The `amb_early_mtg` record is one prior example to borrow field ideas from — not the
  definition.) **Implemented so far:** `ClcNote` (py/clc/clc_note.py) with sources `uxlc-x-note` and
  `dual-cant-addition` and diff types `under-bar`, `transcription-uncertainty` (UXLC's `t` code, §2),
and `dual-cant-added-punct`. The dual-cant **"added out of thin air"** (supplied-punctuation),
  **omitted-accent**, **rafe/dagesh**, and **QUPO vowel-split** notes (§7.7 — the last two added in
  [#47](https://github.com/bdenckla/UXLC-utils/issues/47), sources `dual-cant-rafe-dagesh` /
  `dual-cant-qupo-vowel`, diff types `dagesh` / `dual-cant-qupo-vowel`) are *separate, lightweight*
  dicts — **not** full `ClcNote`s (they carry no anchors / §7.9 row yet). The first two ride their
  own alef/bet row; the two one-letter divergences ride the combined (`-C`) row, stated once naming
  both strands, as **target-as-heading** notes whose heading word is stripped to bare letters
  (`clc_strip.strip_to_bare_letters`, [#48](https://github.com/bdenckla/UXLC-utils/issues/48)).
- **Bare-letter word stripping** (`py/clc/clc_strip.py`, [#48](https://github.com/bdenckla/UXLC-utils/issues/48)):
  `strip_to_bare_letters(text)` reduces a Hebrew word to its consonantal skeleton — base letters
  (U+05D0–U+05EA) plus maqaf, sof pasuq, and legarmeh/paseq (kept unconditionally, either sense —
  §7.16) and whitespace — dropping vowels, accents, meteg, dagesh, rafe, shin/sin dots, CGJ, and
  every other diacritic. It now demotes **every** CLC note-block heading — the §7.7 divergence-note
  headings *and* the ordinary §7.3 UXLC-note headings alike, all applied unconditionally via
  [`clc_render._stripped_heading`](py/clc/clc_render.py) (see the target-as-heading layout at the end
  of §7.7). #48's *original* motivating case is a **distinct** surface and still open: an editor-
  invokable per-note opt-in to simplify the reiterated fully-pointed word inside a **tanach.us `<h2>`**
  note line (§7.3, `clc_note_pages`) — not the CLC note-block heading — which is **not yet wired up**,
  so #48 stays open for it.

---

## 9. Open questions (consolidated)
1. **Accent grammar integration:** with CLC living here (§4), the choice narrows to: **vendor
   `wlc-utils/py/accgram`** into this repo (the established `mb_cmn`-style pattern, via a
   `main_update_vendored_files.py`-type refresh) **vs. cross-call** it. Vendoring is the more
   likely fit. (The old "CLC as its own repo" option is now off the table — see §4.)
2. **UXLC note text source** (§7.3) — **settled** (§5): the rendered prose is the **tanach.us note
   page**, downloaded offline into committed `in/UXLC-notes/` (`main_clc_download_notes`) and read by
   `clc_note_pages`; the change-log `<correction><description>` is demoted to the atom-letter
   consistency guard only. An atom whose page is **not yet fetched** shows a `[note not yet
   downloaded]` placeholder — no fabricated substitute (issue #19). Remaining gap: fetching those
   pages (every `m`/`d`/`t` note has one) and any tanach.us apparatus beyond the `<x>` notes (e.g. the
   **38 numeric/`X`** notes, which are outside the seed set).
3. **codex-index-leningrad** — confirm whether its index improves image guesses over the
   tanach.us LCIndex already vendored here (§6). The clone is on disk and the `.code-workspace`
   already references it as a 2nd folder, so nothing blocks the comparison.
4. **Image scraping source & licensing** (§7.6).
5. **B&W → color** upgrade pipeline — how much can be automated (§7.6).
6. ~~**"Always link" vs. MAM's inline-short/link-long**~~ **Reversed: highlight all, link only
   off-page** — same-page notes sit beside their target, so no jump is needed; only a note relegated
   to the long-notes page is a link (§7.3).
7. **Verdict vocabulary** for identity (2a) ambiguities (§7.1).
8. **WLC-vs-UXLC per-word diff** to gate bracket-note application (§7.2) — tracked in
   [#33](https://github.com/bdenckla/UXLC-utils/issues/33); `wlc-utils/py/accgram/wlc_uxlc_diff.py`
   exists but needs a bracket-note-eligibility decision layer added on top (exact match only).
9. ~~**Where does CLC live?**~~ **Decided:** in this repo — `py/clc/` + `gh-pages/clc/` (§4).
10. **LC manuscript book order** must be encoded for the difference-index sort (§7.9). The code
    only has standard printed order today. *(Verse-level prose/poetic, by contrast, is **already**
    available — `cantsys` + `_is_prose_section_of_job`; not an open question.)*
11. ~~**LC-corroborated omitted-accent wording**~~ **Decided and done** (§7.17,
    [#36](https://github.com/bdenckla/UXLC-utils/issues/36)): "the LC has only..." plus a link to
    `wlc-utils`'s supplied-marks page, for the four notes with independent grounding.

## 10. Rough ordering (not a plan — just gravity)
A loose sense of what unblocks what, without committing to phases:
- The **note schema + one renderer** is the spine — most features are "a new note source feeding
  one renderer." (Define it from §8's requirements, not from `amb_early_mtg`.)
- The **accent-grammar integration** is the long pole for the headline charitable feature (2a).
- The **UXLC-note-text source** is **no longer a long pole** — the real tanach.us note pages are
  downloaded offline into committed `in/UXLC-notes/` and read at build time (§5, §9 #2); an atom
  whose page is not yet fetched shows a `[note not yet downloaded]` placeholder, never invented text.
- Bracket notes, change records, FOIs, Sefaria/MAM links are comparatively cheap once the schema
  and renderer exist (the data largely exists already).
- Image color-upgrade and scraping are independent side quests.

---

## 11. Implementation status (as of 2026-06-29)

A snapshot of where the code (`py/clc/`, build driver `py/main_clc.py` + the separate offline
note-downloader `py/main_clc_download_notes.py`) stands against the §7 feature list. The **walking
skeleton (doc/clc-skeleton-plan.md) is complete and exceeded**; output exists for three pilot books
(Genesis, Proverbs, 2 Samuel) under `gh-pages/clc/`. Everything under the table is built but was
**not** named in §7.

| feature | status | where / note |
|---|---|---|
| §7.1 charitable under-bar | **seed only** | m/d under-bar (+ t transcription-uncertainty) notes *surfaced* (clc_collect); no accent grammar / resolution — `is_uxlc_departure` always False, except the one §7.4 pending-change instance (Deut 5:8.2) |
| §7.2 bracket-note restoration | not started | plan written up: [#33](https://github.com/bdenckla/UXLC-utils/issues/33) (attachment + UXLC-vs-WLC diff gate), [#34](https://github.com/bdenckla/UXLC-utils/issues/34) (MAM enrichment, depends on #33) |
| §7.3 MAM-style highlighted notes | **done (skeleton form)** | 3-col `text \| ref \| doc` renderer (clc_render); noted words highlighted (`clc-doc-target`), same-page anchors dropped (issue #6 reversal) — only off-page notes link; most bodies inline, six case-by-case relegated to a long-notes page, one per main page (`clc_render._LONG_NOTE_SPECS`, `gh-pages/clc/<label>-long-notes.html`) |
| §7.4 change records as notes | **first instance** | change log used only for the consistency guard, not as a note, EXCEPT one instance: Deut 5:8.2-t's stale note is suppressed in favor of a link to the superseding 2026.10.19 change #10 (`clc_collect._NOTES_SUPERSEDED_BY_UXLC_CHANGE`, `ClcNote.superseding_uxlc_change`) |
| §7.5 FOIs as notes | **partial** | ketiv/qere rendered as a boxed ruby (clc_kq); other FOIs not surfaced |
| §7.6 images / Sefaria links | not started | — |
| §7.7 dual-cant strands | **done** | Gen 35:22 + every Decalogue divergence verse encoded (clc_dual_cant `_ORACLE`: ex 20:2–6,8–10,13–15; dt 5:6–10,12–15,17–19 — 23 verses; the other 9 verses in the two passage ranges genuinely don't diverge and correctly carry no entry) — pure-accent + sof-pasuq suppression, supplied maqaf/sof-pasuq, rafe/dagesh by the faithful policy, omitted-accent notes (accents NOTED, never supplied), the QUPO vowel split (patax/qamats on one letter), and Unicode-PASEQ tokenization (a MAM tokenization-convention fold, no new runtime mechanism). [#20](https://github.com/bdenckla/UXLC-utils/issues/20) closed. The rafe/dagesh and QUPO splits — previously resolved silently — now each emit a reader-facing note on the combined (`-C`) row naming both strands, and the divergence set was proven closed against every `_ORACLE` atom ([#47](https://github.com/bdenckla/UXLC-utils/issues/47)). No §7.9 departure rows yet. MAM's per-witness sof-pasuq + two-marks-on-one-letter doc-notes independently corroborate the supplied taḥton sof-pasuqs and the QUPO vowel split ([#43](https://github.com/bdenckla/UXLC-utils/issues/43)/[#44](https://github.com/bdenckla/UXLC-utils/issues/44), validation only — nothing rendered or embedded); MAM's legarmeh/paseq tags + pisqah-be'emtsa-pasuq markings likewise corroborate the pasoleg subtraction and the coveting-verse internal breaks ([#42](https://github.com/bdenckla/UXLC-utils/issues/42), also validation only — see §7.16) |
| §7.8 versification | **done (validation-only)** | Primary vtrad-BHS. The MAM↔BHS Decalogue verse map is hand-encoded in `clc_versification.py` (4 merge groups → `clc_to_mam` etc.; MAM = taḥton-strand boundaries, so `MAM Ex 20:2`=BHS 20:2+3, `Ex 20:12`=BHS 20:13–16, `Dt 5:6`=BHS 5:6+7, `Dt 5:16`=BHS 5:17–20). No new rendered surface: §7.7 already renders the overlay (MAM's versification *is* the taḥton strand), proven 1:1 against `clc_dual_cant._ORACLE` in `clc_versification_test`. MAM consulted as signal, embedded nowhere at runtime (hand-encoded once vs. `.novc/mam_decalogue_versemap.json`, all 53 verses). `clc_to_mam` is the shared CLC→MAM helper [#38](https://github.com/bdenckla/UXLC-utils/issues/38) needs. [#45](https://github.com/bdenckla/UXLC-utils/issues/45) closed |
| §7.9 differences-from-UXLC index | not started | the page itself is unbuilt, still blocked on LC manuscript order (§9 #10); one real `is_uxlc_departure` instance now exists to drive it (Deut 5:8.2, §7.4) |
| §7.10 intro essay / landing page | not started | per-book `_intro_para` only; no `gh-pages/clc/index.html` |
| §7.11 BHL body vs. Appendix A | not started | Appendix A ingested for Psalms only (pre-CLC) |
| §7.12 harvesting other editions | not started | — |
| §7.13 drop early/medial meteg | not started | — |
| §7.14 strip cosmetic control chars | **partial** | orphaned CGJ dropped in the strand splitter only; no general audit |
| §7.15 restore "unsupported" dagesh (`q`) | not started | — |
| §7.16 legarmeh vs. paseq | **identity oracle settled; render gated on #37** | The two identity TBDs are resolved (§7.16): `wlc-utils/py/accgram` distinguishes legarmeh from paseq independently (grammar rule + 17-passage list), a reuse path beside MAM's explicit `מ:לגרמיה-2`/`מ:פסק` tags; and the codepoint question is closed (no dedicated legarmeh codepoint, so a re-reading changes note prose only). MAM's 14 Decalogue calls (11 legarmeh + 3 paseq) are cross-checked against the §7.7 split ([#42](https://github.com/bdenckla/UXLC-utils/issues/42), validation only — nothing rendered/embedded; `clc_dual_cant._ORACLE` comment + §7.7). No *rendered* feature yet: the one remaining blocker is [#37](https://github.com/bdenckla/UXLC-utils/issues/37) (how to show two identical glyphs apart); the 3 ordinary-row Decalogue legarmeh (Deut 5:4/5:25/5:27) are its natural first surface |
| §7.17 LC-corroborated omitted-accent wording | **done** | 4 of 6 live omitted-accent notes (Exod 20:3, Deut 5:6 ×2, Deut 5:17) say "the LC has only..." (`clc_dual_cant._LC_CORROBORATED`), with the `wlc-utils` supplied-marks citation itself now living on each one's own §7.3 long note, not inline. The other two (dt 5:7, 5:13) also credit the LC now, via that same long-notes mechanism but a different citation — no live note still uses the original UXLC-only framing. All six now carry a long note. `wlc-utils` [#53](https://github.com/bdenckla/wlc-utils/issues/53) (the prerequisite) is committed and closed. [#36](https://github.com/bdenckla/UXLC-utils/issues/36) closed |

**Ad-hoc / plumbing built (not in the §7 list):**
- **Offline note download/build split** — `main_clc_download_notes` fetches tanach.us note pages into
  committed `in/UXLC-notes/`; the build reads them locally and never hits the network (deterministic).
  Fixes the multi-word/numbered-book URL bug via `my_uxlc.book_basename` (e.g. `2Samuel` → `Samuel_2`).
- **`clc_collect.iter_noted_atoms`** — one source of truth for the noted `(atom, code)` pairs, shared
  by the build and the downloader so the two cannot drift.
- **Atom/change-log consistency guard** (`clc_collect._check_atom_consistency`,
  `_KNOWN_ATOM_MISMATCHES`) — fails loudly if atomization drifts from the recorded change positions.
- **Ketiv/qere boxed ruby** (clc_kq) and **smart-join of maqaf compounds** in running text (clc_render).
- **Column order `text | ref | doc`** with the ref as a narrow central spine (not the originally
  sketched `reference | text | doc`).
- **`clc-*` / `clc-added-*` CSS** vocabulary in `gh-pages/style.css`.
- **Unit tests:** `clc_dual_cant_test.py`, `clc_kq_test.py`.
