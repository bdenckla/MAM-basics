# Metsudah Megillot (Sefaria) vs. Chabad CTR — plan, then findings

Ben's ask, 2026-08-04: *"Compare Sefaria's Metsudah Megillot to Chabad CTR's corresponding
five books."* The motivating clue is in [ms-snips/README.md](ms-snips/README.md): the
Metsudah Five Megillot digital text quoted into a Sefaria correction thread has U+05AD
HEBREW ACCENT DEHI on prose-book tipḥas, and Chabad's CTR abuses the same lookalike pair in
the opposite direction (`py/author_misc/rocc_2_pre_vowel_accents_in_ctr.py`). The question
this comparison answers: **is Sefaria's Metsudah Hebrew text a deterministic transform of
CTR (or of a shared Judaica Press/Davka ancestor — see `rocc_1_on_the_provenance_of_ctr.py`),
and what exactly is the transform?**

This file is the single plan-and-findings document for the undertaking (per Ben's
one-tracked-plan rule). Findings replace plan text here as phases complete.

## Status

- 2026-08-04, session 1 (Ben + Claude): inputs acquired and verified; plan written;
  execution handed to a fresh session via task chip. Phases 0–3 below were not yet run.
- 2026-08-04, session 2 (the chip session): Phases 0 and 1 run; results in "Phase 0–1
  results" below. Phase 2 awaits Ben's go-ahead. Recording the results here, in a public
  repo, is Ben's call of 2026-08-04 — comparison results and metadata are fine to publish,
  while both full texts stay in `.novc`. Sefaria's version metadata has license CC-BY for
  the Metsudah version, Hebrew and English alike (read 2026-08-04 from
  `https://www.sefaria.org/api/texts/versions/Ruth` and `.../Esther`; the CSV downloads
  lack the field), so the Metsudah side is doubly covered; chabad.org grants no license
  for CTR, so CTR quotation stays at the scale of chanted words.

## Decisions already made (all Ben, 2026-08-04)

- Data path is "option (b)": CTR text taken **byte-exactly** from a blob download out of
  the browser tab that scraped chabad.org — not from any text that passed through a
  model's hands, because model transcription silently reorders Hebrew marks to canonical
  order (proven by per-chapter hash mismatches, all 39 chapters, session 1).
- Work style: small responsive chunks with a short status report after each; no
  long-running silent stretches. Report each phase's results in chat before starting the
  next.
- A first-chunk chip executes Phase 0 + Phase 1 only, then pauses for Ben.

## Inputs (all in `C:\Users\BenDe\GitRepos\MAM-basics\.novc\metsudah-vs-ctr\`)

- `ctr-megillot-2026-08-04.json` (186,166 bytes) — CTR's five Megillot, 745 verses:
  `books.{ruth,song,lam,eccl,esther}.verses` maps `"<ch>:<v>"` to accent-exact text, plus
  per-book chapter `aids`. Extraction: per-chapter `td.hebrew` cells with `a.co_VerseNum`;
  `span[class*=instructional]` (ketiv notes on some pages) removed; NBSP→space; bare
  setuma/petuha markers dropped; whitespace-joined — the same cleaning as
  `py/accgram/ctr_decalogue_fetch.py`'s `clean_verse`. Verse counts: Ruth 85, Song 117,
  Lamentations 154, Ecclesiastes 222, Esther 167. Verified 2026-08-04 against per-chapter
  djb2 hashes computed inside the page (h = (h*33 + codepoint) mod 2^32, seed 5381, over
  `"<ch>:<v>=<text>\n"` in verse order): 39/39 chapters byte-identical.
- `Ruth.csv`, `Song of Songs.csv`, `Lamentations.csv`, `Ecclesiastes.csv`, `Esther.csv` —
  Sefaria's full-version downloads of versionTitle **"The Metsudah Five Megillot,
  Lakewood, N.J., 2001"**, language `he`, fetched 2026-08-04 from
  `https://www.sefaria.org/download/version/<book> - he - <versionTitle>.csv` (the same
  endpoint `py/subcommands/download_sefaria.py` uses for MAM). Format: five header rows
  (Index Title / Version Title / Language / Version Source / Version Notes), then rows of
  `<Book> <ch>:<v>,<Hebrew text>`. Parse with `encoding="utf-8"` and a real CSV reader
  (verse text can contain commas).

Do **not** re-scrape chabad.org: Cloudflare blocks curl and urllib outright (verified
2026-08-04; the vendoring UA in `ctr_decalogue_fetch.py` gets 403 too), and the browser
route is slow. Everything needed is on disk. If a re-scrape is ever unavoidable, the
recipe that worked: in-app browser to any chabad.org page, wait out the challenge, then
same-origin `fetch()` from page context, walking `link[rel="next"]`.

## Preconditions for the executing session

- Repos: `C:\Users\BenDe\GitRepos\MAM-basics` (venv at `.venv\Scripts\python.exe`);
  sibling `C:\Users\BenDe\GitRepos\MAM-parsed` (for `plus/E*.json` MAM text, used only for
  spot checks — MAM is not a primary in this comparison).
- Scratch scripts live in `.novc\metsudah-vs-ctr\` (gitignored), stdlib-only, run from the
  repo root with the venv python. No `sys.path` surgery; run black on any `.py` written.
- Baseline: 320 tests pass via `.venv/Scripts/python.exe py/main_test.py`; **nothing in
  this undertaking should change that**, and no tracked file changes except this doc (and,
  at the end, possibly a cross-link in `doc/ms-snips/README.md`).
- Load the **hebrew-prose** skill before writing any findings prose (accentuation
  vocabulary rules: atom vs chanted word, named referents, no "witness", etc.).

## Known CTR quirks the parser must handle (all observed 2026-08-04)

- Sof pasuq is an ASCII colon `:`; pasoleg is an ASCII `|` between spaces.
- Parenthetical inline notes survive in the verse text on Megillot pages (unlike the
  Decalogue pages, where they sit in `instructional` spans): ketiv notes like
  `(וּבִמְל֣וֹאת כתיב)` (Esther 1:5), editorial notes like `(חסר א)` (Ruth 1:14),
  `(א במקום ה)` (Ruth 1:20), `(ל זעירא)` (Lam 1:12), and qere-with-no-ketiv marked as a
  parenthesized word with a leading space, e.g. `( אֵלַ֖י)` (Ruth 3:5, 3:17). Strip or
  classify them before word-splitting; keep a catalogue of every occurrence.
- Orphan-vowel spacing hacks: a space before a bare vowel inside a word — the qere
  perpetuum Jerusalem forms (e.g. Song 2:7, Lam 1:7), `וּמְצֶ֣אן ָ` (Ruth 1:9),
  `לֵ֔כְן ָ` (Ruth 1:12). A token that begins with a combining mark (or is only marks)
  belongs to the previous token; count and list each.
- Plain stray spaces mid-word: `מִן־הַ צְּבָתִ֑ים` (Ruth 2:16), `לִגְאָל־ לִ֔י` (Ruth 4:6),
  `וְעַל־הַ תְּמוּרָה֙` and `לְרֵעֵ֑ה וּ` (Ruth 4:7), `לָ֔מ וֹ` (Lam 1:19), `מִבְצָרָ֑י ו`
  (Lam 2:5), `קַשְׁתּ וֹ֙` (Lam 3:12), several in Ecclesiastes (4:5, 4:8, 4:10, 5:13,
  5:18, 6:3, 6:7, 6:12, 7:15, 8:1, 9:2, 9:15, 12:5). Same attach-to-neighbor handling.
- Esther oddities: 3:1 ends with a stray orphan ḥolam after the colon; 8:13 has an ASCII
  comma and closes with an **unaccented** `להנקם מאיביהם` (pointed but accentless); 8:7
  lacks its final colon; ZWJ (U+200D) appears inside some words (e.g. the עֲו‍ֹנ- words in
  Lam 2:14, 4:22); Esther 2:3 has a stray U+200E LEFT-TO-RIGHT MARK after `הֵגֶ֛א`.
- CTR's lookalike-pair conventions (full statement in `rocc_2_pre_vowel_accents_in_ctr.py`):
  TIPEHA/GERESH/YETIV codepoints double for deḥi/geresh-muqdam/mahapakh, distinguished by
  the accent's logical order relative to a vowel (before-vowel = the prepositive reading);
  bare occurrences are ambiguous. In these five prose books a genuine deḥi/geresh-muqdam
  is impossible, so every "pre-vowel" occurrence is really a tipḥa/geresh — which is
  exactly what makes them a provenance fingerprint (see the worked example).

## Worked example already in hand (Ruth 1:1, checked 2026-08-04)

Sefaria's Metsudah has `רָעָ֭ב` and `וְאִשְׁתּ֭וֹ` with U+05AD HEBREW ACCENT DEHI — a
poetic-system accent that cannot occur in Ruth — where CTR has U+0596 HEBREW ACCENT TIPEHA.
On `וְאִשְׁתּ֭וֹ` CTR encodes the TIPEHA logically **before** the vav+ḥolam (CTR's deḥi
convention); on `רָעָ֭ב` CTR's TIPEHA is in normal post-vowel order, yet Metsudah has DEHI
there too — so the mapping is not a codepoint-for-codepoint function of Chabad's exact
bytes, and quantifying where it does and does not track CTR's order convention is the
heart of Phase 2. Metsudah also has `אִ֝ישׁ` with U+059D GERESH MUQDAM where the L/MAM
reading is qadma+geresh (`וַיֵּ֨לֶךְ אִ֜ישׁ`). Lam 2:3 spotlight for the ms-snips thread:
CTR has the meteg on `אָֽכְלָ֖ה` that the Leningrad Codex, Sassoon 1053 and Cambridge Add.
1753 all lack, and Metsudah's deḥi words there (`יְמִינ֭וֹ`, `אָֽכְלָ֭ה`) are the same
DEHI-for-TIPEHA exchange as Ruth 1:1.

## Phase 0–1 results (2026-08-04, session 2)

Every number below was read out of the generated artifacts, not retyped from memory. The
artifacts and the scripts behind them are in `.novc\metsudah-vs-ctr\` — gitignored and
machine-local, like the inputs, which cannot be re-fetched without the browser recipe above.
To re-derive any number (a mismatch is a finding), run from the repo root:

```
.venv\Scripts\python.exe .novc\metsudah-vs-ctr\phase0_sanity.py
.venv\Scripts\python.exe .novc\metsudah-vs-ctr\phase1_diff.py
```

`phase0_sanity.py` checks the inventories and censuses every non-letter character;
`phase1_inspect.py` writes the quirk catalogue (`out/inspect.txt`) behind the tokenization
decisions; `phase1_diff.py` states its cleaning decisions in its docstring and writes
`out/phase1_diffs.json` (every aligned diff plus all catalogues) and
`out/phase1_report.txt` (the same, human-readable).

### Phase 0 — inputs sanity: pass

745 verses per side; chapter:verse inventories identical; no duplicates; the CTR JSON is
186,166 bytes as recorded above. Metsudah has the same verse punctuation as CTR — an ASCII
colon for sof pasuq, an ASCII `|` between spaces for the pasoleg — itself a kinship signal,
and the answer to Phase 1's "first inspect" question. Neither side has U+05C7 QAMATS QATAN,
settling a Phase 2 expectation early.

The census also surfaced Metsudah-side quirks the plan did not know, all catalogued in
`out/inspect.txt`:

- Markup: `<big><strong>` around large letters, `<small>` around small letters, `<br>`.
- Apparatus in `<small>(...)</small>`: where the main text has the qere, the note has the
  ketiv — 112 parenthetical notes in all, against CTR's 16. Also `(ס)` and `(פ)`
  setuma/petuha markers padded with NBSP and em-space runs, and U+05AF masora circles as
  apparatus pointers (10, of which 8 sit outside the notes). Both sides have the
  qere-with-no-ketiv אלי of Ruth 3:5 and 3:17 in the readable text.
- Lam 5:22 and Eccl 12:14 each have the liturgically repeated verse a second time, in
  parentheses; CTR lacks the repeats.
- A prepositive accent can stand as the first character of its chanted word: Metsudah has
  ֚בָּאוּ at Ruth 1:22 where CTR has בָּ֚אוּ — the same yetiv, logically before the whole
  word against logically after the vowel.

### Phase 1 — the aligned diff

The tokenizer strips the markup and notes (cataloguing every one), rejoins CTR's spacing
hacks — 22 stray spaces (21 in CTR, one in Metsudah at Eccl 4:14) and 18 orphan-mark
tokens, 15 of them the Jerusalem qere-perpetuum forms — and pairs chanted words per verse
by letters-only similarity. "Pointing" below means vowel points, dagesh/mapiq and the
shin/sin dots; accents and meteg count only at the full level.

| book | verses | identical, full | identical, letters+pointing | identical, letters | grouped differently |
| --- | --- | --- | --- | --- | --- |
| Ruth | 85 | 0 | 74 | 80 | 2 |
| Song | 117 | 0 | 100 | 111 | 3 |
| Lamentations | 154 | 0 | 133 | 146 | 3 |
| Ecclesiastes | 222 | 0 | 194 | 216 | 3 |
| Esther | 167 | 0 | 85 | 153 | 4 |
| all five | 745 | 0 | 586 | 706 | 15 |

2419 aligned pairs differ at the full level: 58 at the letters level, 152 more at the
pointing level, 358 only in mark order within a cluster, and 1851 in the marks themselves.
No verse is identical at the full level, and one exchange explains that by itself: **744 of
the 745 verses have at least one chanted word where Metsudah has U+05AD DEHI and CTR has
U+0596 TIPEHA** — 1317 chanted words. Only 6 TIPEHA remain in all of Metsudah's five books,
and CTR lacks DEHI entirely. The Ruth 1:1 example above holds corpus-wide — and Metsudah
has the DEHI both where CTR's TIPEHA is in its before-vowel ("deḥi") order and where it is
in plain after-vowel order, so the exchange is not a byte-for-byte function of CTR's
encoding; quantifying that split is Phase 2's job.

The other systematic patterns (full signature table in the artifacts):

- 136 chanted words: Metsudah has QADMA where CTR has PASHTA; 3 the other way. A second
  lookalike pair, one the plan did not predict.
- 123: Metsudah has GERESH MUQDAM where CTR has GERESH. Exactly one GERESH remains in
  Metsudah (Lam 2:17), and CTR lacks GERESH MUQDAM entirely.
- Telishas: 58 chanted words where CTR has a TELISHA QETANA that Metsudah lacks, 33
  likewise with TELISHA GEDOLA. The census totals (Metsudah 24 and 46, CTR 85 and 81) make
  this systematic rather than incidental; whether CTR's extra copies are stress helpers is
  a Phase 2 question.
- Mark order: 356 of the 358 order-only pairs are chanted words with a ḥolam, and in the
  tabulated cases CTR has the accent or meteg logically before the ḥolam where Metsudah
  has the ḥolam first.
- Meteg: 47 chanted words where CTR has a meteg that Metsudah lacks, 11 the reverse. Lam
  2:3's אָֽכְלָ֖ה meteg — the ms-snips spotlight — is in both texts, so that finding
  stands.

Letters-level and grouping differences worth naming (all 58 letters-level pairs are listed
in `out/phase1_report.txt`):

- Metsudah lacks the archaic ending ןָ twice in Ruth: it has וּמְצֶ֣א at 1:9 and קְרֶ֤א at
  1:20 where CTR has וּמְצֶ֣אןָ and קְרֶ֤אןָ (CTR's spacing hack rejoined) — the hack and
  the lack at the same places, presumably two answers to one rendering difficulty.
- Lam 1:6: Metsudah's main text has וַיֵּצֵ֥א צִיּ֭וֹן, with a note `(מִן בַּת־)` for what
  it lacks; CTR has וַיֵּצֵ֥א מִבַּת צִיּ֖וֹן, three chanted words.
- Esther's Mordokhai: 56 of Esther's 92 pointing-level pairs (48 of its 73
  pointing-differing verses) are the name — Metsudah has מָרְדְּכַ֣י with a sheva where
  CTR has מָרְדֳּכַ֣י with a ḥataf qamats. This is most of why Esther's letters+pointing
  row is 85 of 167.
- Plene against defective: Metsudah has הָֽעֲשֻׁקִ֗ים (Eccl 4:1) and הַפֻּרִ֛ים (Esther
  9:29) where CTR has הָֽעֲשׁוּקִ֗ים and הַפּוּרִ֛ים, and שַׁרְבִ֣ט (Esther 8:4) where
  CTR has שַׁרְבִ֣יט.
- Esther 9:2: Metsudah has בִּפְנֵיהֶ֔ם where CTR has לִפְנֵיהֶ֔ם — a bet against a lamed.
- Grouping: 15 verses group atoms into chanted words differently. Ruth 1:21: Metsudah has
  הֵֽרַע־לִֽי, one chanted word with a maqaf, where CTR has הֵֽרַע לִֽי, two chanted
  words, the first with a meteg and no accent. Esther 9:29: Metsudah has אֶת־אִגֶּ֧רֶת, a
  maqaf compound, where CTR has אֵ֣ת with a munaḥ — and a tsere against Metsudah's segol.
- Sof pasuq bookkeeping: CTR lacks the final colon of Esther 8:7 (Metsudah has it), and
  CTR's stray orphan ḥolam after Esther 3:1's colon was dropped and catalogued.

## Phases (each ends with a chat report; pause after Phase 1 for Ben)

**Phase 0 — done 2026-08-04.** Results in "Phase 0–1 results" above.

**Phase 1 — done 2026-08-04.** Results in "Phase 0–1 results" above; the diff artifact is
`.novc\metsudah-vs-ctr\out\phase1_diffs.json`. One deviation from the plan as written:
plain `zip_longest` smears a grouping difference across the rest of its verse, so chanted
words are paired by letters-only similarity (difflib blocks, `zip` within a block) and
`zip_longest` runs only inside unaligned blocks. **Paused for Ben before Phase 2.**

**Phase 2 — encoding-signature analysis (the provenance verdict).** For every Metsudah
occurrence of U+05AD DEHI, U+059D GERESH MUQDAM, U+05AE ZINOR (if any), and U+05A4 MAHAPAKH
vs U+059A YETIV: tabulate the CTR counterpart codepoint **and its order class**
(pre-vowel / post-vowel / bare / pre-ḥolam), and vice versa for every CTR pre-vowel
accent. Also compare: qamats-qatan (U+05C7) usage (CTR count expected 0 — confirm both
sides), meteg order relative to its vowel, ketiv/qere presentation, the orphan-vowel
hacks, letters-only divergences from Phase 1. Verdict: deterministic transform of CTR /
shared ancestor with independent conversion / unrelated. State the rule(s) and the
exception count for each.

**Phase 3 — findings write-up.** Replace the plan sections of this doc with dated
findings (hebrew-prose skill loaded first); add the Lam 2:3 outcome to
`doc/ms-snips/README.md` §"The Metsudah digital edition confuses deḥi and tipeḥa" as a
cross-link, not a restatement. Commit and push (commit-at-will stands). If any CTR verse
deserves a permanent vendored copy, follow the `in/chabad-ctr/` spot-sample pattern
(`D1-Psalms.json` shape) rather than inventing a new one.

## What session 1 left behind that should NOT be used

The per-book JSONs in session 1's scratchpad
(`...\Temp\claude\C--Users-BenDe-GitRepos-MAM-basics\0897281c-...\scratchpad\chabad-ctr-megillot\`)
were transcribed through the conversation and carry canonically re-ordered marks — same
mark multiset, wrong mark order, all 39 chapter hashes mismatched. The `.novc` JSON above
is the authoritative CTR copy. The `-merged.json` files there inherit the same defect.
