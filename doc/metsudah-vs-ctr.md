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
  execution handed to a fresh session via task chip. Phases 0–3 below are NOT yet run.

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
  perpetuum Jerusalem forms (e.g. Song 2:7, Lam 1:7), `וּמְצֶאן ָ` (Ruth 1:9),
  `לֵ֔כְן ָ` (Ruth 1:12). A token that begins with a combining mark (or is only marks)
  belongs to the previous token; count and list each.
- Plain stray spaces mid-word: `מִן־הַ צְּבָתִ֑ים` (Ruth 2:16), `לִגְאָל־ לִ֔י` (Ruth 4:6),
  `וְעַל־הַ תְּמוּרָה֙` and `לְרֵעֵ֑ה וּ` (Ruth 4:7), `לָ֔מ וֹ` (Lam 1:19), `מִבְצָרָ֑י ו`
  (Lam 2:5), `קַשְׁתּ וֹ֙` (Lam 3:12), several in Ecclesiastes (4:5, 4:8, 4:10, 5:13,
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

Sefaria's Metsudah has `רָעָ֭ב` and `וְאִשְׁתּ֭וֹ` with U+05AD HEBREW ACCENT DEHI — a
poetic-system accent that cannot occur in Ruth — where CTR has U+0596 HEBREW ACCENT TIPEHA.
On `וְאִשְׁתּ֭וֹ` CTR encodes the TIPEHA logically **before** the vav+ḥolam (CTR's deḥi
convention); on `רָעָ֭ב` CTR's TIPEHA is in normal post-vowel order, yet Metsudah has DEHI
there too — so the mapping is not a codepoint-for-codepoint function of Chabad's exact
bytes, and quantifying where it does and does not track CTR's order convention is the
heart of Phase 2. Metsudah also has `אִ֝ישׁ` with U+059D GERESH MUQDAM where the L/MAM
reading is qadma+geresh (`וַיֵּ֨לֶךְ אִ֜ישׁ`). Lam 2:3 spotlight for the ms-snips thread:
CTR has the meteg on `אָֽכְלָ֖ה` that the Leningrad Codex, Sassoon 1053 and Cambridge Add.
1753 all lack, and Metsudah's deḥi words there (`יְמִינ֭וֹ`, `אָֽכְלָ֭ה`) are the same
DEHI-for-TIPEHA exchange as Ruth 1:1.

## Phases (each ends with a chat report; pause after Phase 1 for Ben)

**Phase 0 — inputs sanity (small).** Load both sources; confirm 745 verses each side with
identical `<book> <ch>:<v>` inventories (Sefaria row count vs CTR keys); report any verse
present on one side only. Confirm the input file sizes above.

**Phase 1 — aligned word-level diff.** Tokenize per the quirks list (CTR notes stripped
but catalogued; orphan-mark tokens rejoined; `|` and `:` handled on both sides — first
inspect what Metsudah's CSV uses for pasoleg and sof pasuq). Align chanted words per
verse (`zip_longest`, like `py/subcommands/diff_ctr_vs_mam.py`). Produce counts: verses
identical at (i) letters-only, (ii) letters+vowels, (iii) full-marks level; word-count
mismatches; then the diff list as a JSON artifact in `.novc\metsudah-vs-ctr\out\`.
Report headline numbers and 5–10 representative diffs. **Pause for Ben.**

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
