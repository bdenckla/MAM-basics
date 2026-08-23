# PLAN: near-aleppo — a MAM-parsed-plus nearer to the Aleppo Codex

| | |
|---|---|
| **Status** | Step-through of the massaging inventory in progress: **steps 1–6 of 41 decided** (2026-08-23). The plan proper (phases, commands, verification) is not written yet; it goes in this file when the step-through ends. |
| **Deliverable** | `C:\Users\BenDe\GitRepos\MAM-basics\out\near-aleppo\` — a version of MAM-parsed-plus (the JSON under `C:\Users\BenDe\GitRepos\MAM-parsed\plus\`) whose text is nearer to what the Aleppo Codex contains, or to what its lost sections probably contained. Plus HTML documentation of the edition at `gh-pages/near-aleppo/`. |
| **Owner** | Ben Denckla. Every decision below is Ben's unless marked otherwise. |
| **Run from** | `C:\Users\BenDe\GitRepos\MAM-basics`, venv `.venv\Scripts\python.exe`. Sibling repos read: `..\MAM-parsed` (measurements below at its commit `95f64d7`), `..\MAM-private` (at `cc88ca9`). |
| **Load first** | The `hebrew-prose` skill (anything here touches accentuation prose); `doc/sigil-decoding.md` (what each siglum in a MAM note means, and which count as Aleppo). |

## 1. Goal and constraints (Ben, 2026-08-23)

- **Keep the JSON structure of MAM-parsed-plus** — templates, נוסח notes, ketiv/qere apparatus
  all intact — and change only the Hebrew strings underneath it, "at least to a large extent".
- **Based on the comparison work in MAM-private**, which massages MAM and an Aleppo-based online
  edition toward each other so they can be diffed. That work is private: **this file and
  everything generated from it must not name that edition or that project**. "MAM-private" may
  be named. Write "the comparison project" and "the comparison edition".
- **No information from the comparison edition is used directly.** The massaging steps were
  *inspired* by the comparison, and that is fine. But where MAM does not contain the information
  needed to move toward Aleppo (Ben's example: Aleppo's pointing of the divine name), that is
  **documented as a limitation**, not borrowed. One stated exception, §3 step 1 below.
- **Every step of the comparison's massaging is stepped through, in both directions**, even the
  ones that are obviously Unicode housekeeping and get an immediate "ignore".
- **The HTML documentation is part of the plan.** Each limitation and each notable case (hataf
  hiriq, divine-name pointing, the pointed-ketiv review flags, the places where MAM is *already*
  nearer Aleppo than the comparison edition) is to be mentioned there.

## 2. Where the inventory comes from

The comparison project is the subdirectory of `C:\Users\BenDe\GitRepos\MAM-private` whose
`documentation\` folder holds **`massaging.md`** — find it with
`Get-ChildItem -Recurse C:\Users\BenDe\GitRepos\MAM-private -Filter massaging.md`. Within it:

- `documentation/massaging.md` — the catalogue: M1–M26 plus three unnumbered steps ("Strip
  Ketiv-Maqaf", "Strip Extraordinary Dots", and the trivial-qere pre-step that took M12's
  number); M3 and M9 are deliberate holes. Checked against the code 2026-08-23: in sync.
- `documentation/mpu-parsing.md` — how MAM-parsed-plus is read into tokens (which parameter of
  each template is taken; what is skipped).
- `py/main_diff.py` (`run()` — the pipeline order, the trivial-qere pre-step, Decalogue verse
  realignment), `py/python_modules/massage_mam.py` and `massage_mgk.py` (the two massaging
  passes, each docstring listing its steps in execution order), `diff_engine.py` and the modules
  it imports (diff-time suppressions: nusach-note matching, maqaf fusion, fallbacks, manual
  suppressions, Aleppo-extant flagging).

Read those for the mechanics of any step; this file records only the **disposition** of each for
near-aleppo and the reasons.

## 3. Standing rules settled so far

1. **Pointed ketiv.** near-aleppo represents Aleppo's *body text*, i.e. the **pointed ketiv**.
   MAM holds a pointed ketiv only inside the `קו"כ-אם` (trivial-qere) template; elsewhere the
   ketiv is consonantal and only the qere is pointed, and the comparison never reconstructed it
   (it strips the other side's ketiv pointing instead — its M6 — and diffs ketiv letters only).
   **Decision: infer the pointed ketiv algorithmically** — transplant the qere's vowels and
   accents onto the ketiv's letters — and leave the ketiv unpointed when (a) the algorithm does
   not know how; (b) **the inferred pointing disagrees with the comparison edition — flag these
   in the JSON for Ben's later review against the manuscript** (Ben's one stated exception to
   the no-borrowing rule: the comparison edition is used *only* to flag words to look up, never
   as a source of pointing); (c) the word is a ketiv-without-qere (כתיב ולא קרי), which the
   manuscripts leave unpointed anyway. Plan consequence (not yet decided by Ben): the
   disagreement check needs private data, so the inference runs in MAM-basics and the
   disagreement list is produced from MAM-private as bare verse references, consumed here under
   a generic name.
2. **Massage base text only — never a נוסח note body** (the template's parameter `2`): notes
   quote other editions' forms verbatim (Deut 14:24 `הקלדה=תוּכַ֘ל`) and must stay as quoted.
3. **Recurse into template parameters.** Templates nest (Ps 27:6, 55:18, 61:5 have a `מ:דחי`
   inside a `מ:קמץ` parameter), so a massaging walks into parameters rather than treating them
   as strings.
4. **Which sigla count as Aleppo**: `א`, `א-צילום`, `א-כתיב`/`א-קרי` are readings of the codex;
   `א(ו)`, `א(ס)`, `א(ע)`, `א(ק)`, `א(ר)` are testimony to its lost parts and count as Aleppo;
   `שיטת-א` is an inference and `מסורת-א` the margin, not the text. Where Aleppo is lost and
   untestified, **Leningrad (`ל`) is an acceptable proxy** (Ben, on step 2). Full decoding:
   `doc/sigil-decoding.md`.

## 4. The inventory, with dispositions

Disposition codes: **IGNORE** (a representation or Unicode matter; says nothing about Aleppo),
**APPLY** (massage MAM toward Aleppo from MAM's own information), **KEEP** (MAM is already the
Aleppo-faithful side; applying the comparison's step would move *away* from Aleppo), **LIMITATION**
(MAM lacks the information; document), **PENDING** (not yet stepped through).

### Tier 1 — catalogued massagings, MAM side, in execution order

| # | Step (catalogue name) | Disposition |
|---|---|---|
| 1 | Trivial-qere pre-step (the catalogue's M12) — replaces the `קו"כ-אם` token's text by its qere, inferring the pointed qere for the he→vav and vav→yod-vav patterns | **IGNORE** as a massaging (it lines up two token representations of the same apparatus). It raised the pointed-ketiv question, settled as rule 1 above. |
| 2 | M11 varika-shva → hataf — MPU marks a manuscript hataf on a non-guttural with a varika (U+FB1E) on the shva's consonant; the comparison infers the hataf vowel by rule (hataf qamats before guttural+qamats, hiriq before guttural+hiriq, else hataf patah) | **APPLY, wherever there is a varika**, except where the note says Aleppo does *not* have the hataf — **there are none such**: of the 87 varika notes whose hataf sigla lack `א`, none mentions Aleppo at all (most are in lost sections: Genesis 26, Numbers 16, Daniel 11, Nehemiah 9; about a dozen are in books where Aleppo is extant — Ps 3, Eccl 3, Jer 2, Mic, Zech, Song, Lam, Ezra — and the rule applies there too; say so in the documentation). **Source of the hataf word: the note, not the inference** — `py/main_explicit_xataf.py` → `out/explicit-xataf.json` takes the explicit-hataf word verbatim from the note with its sigla (666 mappings, 579 citing `א`; the inference agrees with all 666 and serves as a cross-check). Hataf hiriq: Aleppo has at least one famous case; representation to decide (probably shva + plain hiriq); it must be noted locally with a נוסח (probably already is) and in the HTML documentation. The 6 `ac-differs` notes in `out/explicit-xataf-extras.json` (hataf on a word *without* varika) belong to step 36. |
| 3 | M4 qamats qatan → qamats | **APPLY**: collapse every U+05C7 to U+05B8. `מ:קמץ` (375 templates): after the collapse its `ד` and `ס` parameters are identical in 373; the other two (Ps 35:10, Prov 19:7) differ only by a gray maqaf in `ד` against a space in `ס`, which step 30 makes a non-difference. Ben's rule: flag any remaining `ד`≠`ס` for manual handling unless the Aleppo-ish choice is obvious. Whether the vacuous template is left or collapsed: open, for the plan. |
| 4 | M7 atnah hafukh → yerah ben yomo (U+05A2 → U+05AA) | **KEEP** both codepoints as MAM has them. Ben: "MAM's AH vs YBY distinction is preserving something really present in the Aleppo manuscript." See `py/author_misc/urwotm_4_atnax_hafukh.py` (Ps 5:10 in א, ל, ש1). Document as a place where MAM is already nearer Aleppo than the comparison edition. |
| 5 | M14 strip stress-helper accents (MAM doubles a prepositive/postpositive accent on the stressed syllable; the comparison strips the copy by position, with a diff-time fallback for telisha qetana and zarqa) | **APPLY, with these rules** — sources: MAM's introduction ch. 2, sections "טעם כפול בהברה המוטעמת" (prose) and "…בספרי אמ"ת" (poetic), and "גרש או גרשיים ותלישא גדולה בתיבה אחת"; Yeivin ITM §239 (full OCR). (1) **Pashta**: keep MAM's doubled pashta except where *no letter stands between the stressed letter and the last letter* — Aleppo's rule per Yeivin §239 — and strip that adjacent copy; verify in the plan whether a mater lectionis counts as a letter between (Yeivin's examples and Qimḥi's quote pull slightly apart). (2) **Prose zarqa, segolta, telisha gedola, telisha qetana**: strip the duplicate by position; Aleppo's rare doubt-driven doublings would be recorded in MAM's ch. 5 lists or notes → step 36. (3) **Dehi, tsinnor**: take parameter `1` of `מ:דחי` / `מ:צינור`. Not a limitation: Aleppo's small stress line on the dehi words MAM's ch. 5 lists as "(סימון מקום הטעם לדחי)" (Ps 44:27, 57:9, 69:29, 86:7, 108:3, 138:3, 139:7; Job 29:16 — ch. 2 says nine; recount from the source) is **already in MAM's base text as a meteg** (verified Ps 86:7 צָ֭רָתִֽי, 139:7 אָ֭נָֽה), the note giving "דחי ומרכא?" as the alternative; and at Ps 49:15 the doubled tsinnor is `ק13,ת` only, Aleppo single, the note saying so. (4) The five telisha-gedola + geresh/gershayim words: remove MAM's extra stressed-syllable copies at Lev 10:4 and Ezek 48:10. (5) The fallback mechanism: ignore. |
| 6 | M10 zarqa ↔ zinor (U+0598 ↔ U+05AE, by poetic/prose verse) | **KEEP** both codepoints as MAM has them. Prose: U+05AE is MAM's postpositive zarqa; U+0598 occurs only as the stress-helper copy in a word that also has U+05AE (all prose books; the four Torah "lone" U+0598 are inside note bodies), so after step 5 none remains. Poetic: U+05AE is tsinnor, U+0598 is tsinnorit — two accents (Ps 168, Prov 16, Job 27 words), whose distinction is real in the manuscript (Yeivin §241) and which MAM's introduction forbids sharing a character. |
| 7 | M15 strip ole when co-located with merkha (yored) | PENDING |
| 8 | M13 strip rafe | PENDING — MAM's introduction ch. 2 has a section "סימן הרפה". |
| 9 | Strip extraordinary dots (U+05C4 / U+05C5) | PENDING |
| 10 | M25 merge the standalone הַ pseudo-word (Deut 32:6) | PENDING |

### Tier 1 — catalogued massagings, comparison-edition side, in execution order

All are the comparison edition being massaged toward MAM. For near-aleppo each asks: is the
feature the comparison edition has, and MAM lacks, something the *manuscript* has?

| # | Step | Disposition |
|---|---|---|
| 11 | M1 decompose presentation forms | PENDING |
| 12 | M2 omit invariant token text | PENDING |
| 13 | Strip ketiv-maqaf (a maqaf between ktiv and kri) | PENDING |
| 14 | Isa 9:6 retype mila as ktiv (לםרבה) | PENDING |
| 15 | M24 holam → holam haser for vav | PENDING — MAM ch. 2 "חולם בוי"ו עיצורית". |
| 16 | M21 CGJ between accent and meteg (Decalogue) | PENDING |
| 17 | M22 CGJ in dual-vowel clusters (Decalogue) | PENDING |
| 18 | M23 tipeha → dehi (poetic) | PENDING |
| 19 | M26 patah+sheva+geresh reorder | PENDING |
| 20 | M18 combining-mark order standardisation | PENDING — see `CLAUDE.md` on MAM-normal mark order. |
| 21 | M19 hiriq-qamats CGJ (ירושלם) | PENDING — MAM ch. 2 "הניקוד בתיבת ירושלם". |
| 22 | M5 add holam to the divine name (יְהֹוָה) | PENDING — Ben's own example of a likely LIMITATION; MAM ch. 2 "שם הוי"ה". |
| 23 | M16 add holam to Adonai | PENDING |
| 24 | M17 hataf segol in YHVH-Elohim | PENDING |
| 25 | M8 add revia to geresh muqdam (revia mugrash) | PENDING — MAM ch. 2 "רביע מוגרש". |
| 26 | M6 strip ketiv pointing | PENDING — largely settled by rule 1; confirm. |
| 27 | M20 split baked-in legarmeh into its own token | PENDING — MAM ch. 2 "פסק ולגרמיה". |

### Tier 2 — MPU parsing decisions (MAM side, before any massaging)

| # | Step | Disposition |
|---|---|---|
| 28 | `מ:קמץ` → parameter `ד` kept, `ס` dropped | PENDING — largely settled by step 3; confirm. |
| 29 | `מ:דחי` / `מ:צינור` → parameter `1` kept | PENDING — settled by step 5 rule 3; confirm. |
| 30 | `מ:מקף אפור` (gray maqaf) skipped | PENDING — MAM's gray maqaf marks a maqaf the manuscript leaves unwritten (116 sites; `py/accgram/maqaf_nonfinal_accents.py`); Ben on step 3: "we will collapse gray maqaf to space anyway". |
| 31 | `נוסח` template: parameter `1` walked, parameter `2` kept as a note | PENDING |
| 32 | Notes and decorative templates skipped (`מ:הערה`, `מ:הערה-2`, `ר0`, `ר2`, `ש`, `ששש`, inverted nun) | PENDING |
| 33 | Special-letter templates flattened to text | PENDING |
| 34 | Parashah markers from non-EP columns attached to the previous verse | PENDING |
| 35 | Decalogue verse realignment | PENDING |

### Tier 3 — diff-time suppressions and reconciliations

| # | Step | Disposition |
|---|---|---|
| 36 | Nusach-note suppression: a diff is dropped when the comparison edition's text matches an `א=` reading in the note | PENDING — this is **the** MAM-internal source of Aleppo readings: apply the note's `א=` reading to the base text. Feeds from steps 2 (`ac-differs` extras), 3 (hataf qamats for qamats qatan), 5 (rare doublings). |
| 37 | Maqaf fusion (one mila vs a maqaf-split pair) | PENDING |
| 38 | Fallback resolution | PENDING — ignore, per step 5 rule 5. |
| 39 | Ktiv/qere planes; qere-without-ketiv merge | PENDING |
| 40 | Manual suppressions (human-judged) | PENDING |
| 41 | Aleppo-extant flagging (`ac-lost`, from codex-index) | PENDING — relevant to "lost sections" wording. |

## 5. Findings in passing (not part of this plan)

- **`ק13` is Cairo 13, not "Cambridge T-S 13".** MAM's appendix defines `כתי"ק13` as a Writings
  manuscript written 1028 by Zechariah ben Anan, and calls him "the scribe of כת"י קהיר 13".
  `py/accgram/ps17v14_mam_doc_notes_body.py` glosses ק13 as "Cambridge T-S 13" on its rendered
  page; `doc/sigil-decoding.md` now marks the row Conflicting and says the page wants fixing.
- `doc/sigil-decoding.md` was overwritten by mistake in `20ec7f2` and restored with additions in
  `5be1054`; its history is the record.

## 6. How the step-through is run, and what to measure

- **One step per message.** State what the comparison does (direction, lossless or not, whether
  its expectation held), propose a disposition with the MAM-internal source that justifies it,
  ask whether it stands, and wait. Ben answers one at a time and wants room to ask back. Record
  each answer in §4 and commit.
- **Sources that settled steps so far**, and how to re-fetch them (no local mirror exists):
  MAM's introduction on Wikisource, raw wikitext via
  `https://he.wikisource.org/w/index.php?title=<url-encoded title>&action=raw` for the titles
  `ויקיטקסט:מבוא למקרא על פי המסורה/פרק ב` (chapter 2: every pointing and accent convention,
  section per phenomenon — the first place to look for any step), `…/פרק ה` (chapter 5: per-book
  lists of Aleppo's oddities, verse by verse) and `…/נספחים` (the source list). Yeivin's ITM, full
  OCR: `C:\Users\BenDe\GitRepos\MAM-private\masorah-books\books\itm\md-export-of-docx\N0239.md`
  and siblings, one file per section. `doc/sigil-decoding.md` for sigla.
- **Figures above and the commands that re-establish them** (against MAM-parsed `95f64d7`):
  varika count `(Get-Content C:\Users\BenDe\GitRepos\MAM-parsed\plus\*.json -Raw | Select-String -Pattern ([string][char]0xFB1E) -AllMatches | ForEach-Object { $_.Matches.Count } | Measure-Object -Sum).Sum` gave 685 (the same form with another codepoint gives each of the other codepoint counts here); `out/explicit-xataf.json` 666 mappings / 579 with `א`; `מ:קמץ` 375 templates; `מ:דחי` 2,316; `מ:צינור` 56; U+05A2 196 (Ps 173, Prov 8, Job 15), U+05AA 56; U+0598 and U+05AE per book as in step 6. Re-measure rather than trust; a mismatch is a finding. The three check scripts were throwaways under `.novc/` (`varika_notes_no_alef.py`, `qamats_tmpl_params.py`) and are not tracked; each is a few dozen lines walking the raw JSON and is quicker to rewrite than to recover.
