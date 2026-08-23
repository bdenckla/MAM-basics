# PLAN: near-aleppo — a MAM-parsed-plus nearer to the Aleppo Codex

| | |
|---|---|
| **Status** | Step-through of the massaging inventory in progress: **steps 1–9 of 41 decided** (2026-08-23). The plan proper (phases, commands, verification) is not written yet; it goes in this file when the step-through ends. |
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
  realignment), `py/python_modules/massage_mam.py` and, beside it, the module that massages the
  other side (the two massaging passes, each docstring listing its steps in execution order), `diff_engine.py` and the modules
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
| 7 | M15 strip ole when co-located with merkha (yored) — the comparison's step is a 13-entry lookup table captured from an earlier algorithm | **APPLY**: in a poetic verse, remove the ole (U+05AB) from any letter that also has the yored (U+05A5, whose Unicode name is MERKHA). MAM's introduction says so outright. Ch. 2 §"עולה ויורד": where the yored's atom is stressed on its first syllable, and the atom before it is end-stressed or has a disjunctive, "כתבי־היד מסמנים **רק** את ה'יורד' ומשמיטים את ה'עולה' לגמרי" (לְאֵ֢ל חָ֥י, וְאֵשֵׁ֢ב רֹ֥אשׁ, קֶ֗דֶם סֶ֥לָה); the printed editions instead put the ole on the yored's letter, MAM follows the printed editions as a תיקון קוראים, and a footnote there says the optimal solution would have been a **gray ole**, like the gray maqaf. Ch. 5 §"עולה ויורד" part א lists all 13 such verses with Aleppo's form (`א=לְמָח֢וֹל לִ֥י` …), saying Aleppo omits the ole in them consistently. Yeivin ITM §360 (`N0345.md`) gives the same rule, with Ps 42:3, 55:20 and Job 29:25, and notes that printed texts may mark the upper sign on the same letter as the lower. **The mechanical criterion reproduces ch. 5's list exactly, so no list is hard-coded**: the census finds those 13 atoms and no others — Ps 30:12 לִ֥֫י, 42:3 חָ֥֫י, 55:20 סֶ֥֫לָה, 68:20 י֥֫וֹם, 86:2 אָ֥֫נִי, 109:16 חָ֥֫סֶד, 125:2 לָ֥֫הּ; Prov 24:24 אָ֥֫תָּה, 30:15 הַ֥֫ב; Job 8:6 אָ֥֫תָּה, 9:22 הִ֥֫יא, 29:25 רֹ֥֫אשׁ, 34:20 לָ֥֫יְלָה. **11 of the 13 also have a local נוסח note** giving Aleppo's form (`א=אָ֥נִי (השמטת סימן העולה)`); Ps 42:3 and Job 9:22 have none, being in ch. 5's list only, and Ps 30:12's note says `השמטת נקודת הרביע` where the other ten say `סימן העולה` — its `א=לִ֥י` form is without the ole like the rest, so that wording looks like a slip. All 13 are where Aleppo is extant. Documentation: this is the gray ole ch. 2's footnote wished for, realised as absence. **Two neighbouring features M15 does not touch, neither needing any code, since MAM already has Aleppo's form** — for the HTML documentation: (a) the **ole on the preceding atom**, 55 verses (ch. 5 part ב), e.g. Ps 56:9 סָפַ֢רְתָּ֫ה אָ֥תָּה, Ps 115:1 לֹ֫א־לָ֥נוּ; the maqaf between the two atoms is step 30's. (b) the **ole's position within an atom** — MAM puts it on the syllable fit for a light ga'ya, and on the yod of the divine name, which is Aleppo's practice, against the printed editions' syllable-before-the-stress and first he (ch. 2 part ג, ch. 5 part ג); where Aleppo's ole sits on a letter MAM's rule does not choose, MAM has a local note with Aleppo's form — Ps 32:10 `א!=לָרָ֫שָׁ֥ע (סימן העולה באות רי"ש)`, Ps 52:9 `א=מָע֫וּזּ֥וֹ` — so those are step 36's. |
| 8 | M13 strip rafe — a blanket removal of U+05BF from every MAM token | **KEEP all 95 rafe sites in the base text, plus a LIMITATION.** This is the first step where MAM has *less* than Aleppo rather than more. Ch. 2 §"סימן הרפה" opens by saying the important Tiberian manuscripts, "כתר ארם צובה וכתי"ל", mark a letter lacking a light dagesh (בג"ד כפ"ת) or a mappiq (he) with a rafe; most editions omit it entirely, and ch. 2 names seven of them that do, so a step stripping the rafe would move away from the codex in all 95. **The 87** whose letter has no dagesh are ch. 2's three manuscript categories: a he lacking an expected mappiq (וְרַחְמָ֖הֿ), a quiescent alef (יְר֧אֿוּ, לָרֽאֿוּבֵנִ֖י), and an undageshed בג"ד כפ"ת (קַֽו־תֹֿ֖הוּ). Ch. 2 says MAM preserved these as written in the manuscripts — "ובכולן השתדלנו לשמור על סימן הרפה הכתוב בכתבי־היד" — and its footnote on the third says "בכל אחת מהן יש סימן רפה ברור בכתר ארם צובה ובכתי"ל". Its list has 81 entries against the census's 87, the difference being words with two rafes, counted once each in the list and twice in the census. **The 8 Decalogue sites**, where one letter has both a dagesh and a rafe, are Exod 20:8 and Deut 5:12 כׇּֿל־, and Exod 20:12 and Deut 5:16 תִּֿרְצָ֖͏ֽח, תִּֿנְאָ֑͏ֽף, תִּֿגְנֹֽ֔ב. **They are a manuscript feature, not a MAM presentational device** — Ben's correction, 2026-08-23, against a first draft of this row that called them MAM's device for showing two accentuations at once. MAM's notes at Deut 5:16 quote Leningrad as `ל=תִּֿרְצָֽח` and `ל!=תִּֿנְאָֽ֑ף`, each quoted form having dagesh U+05BC immediately followed by rafe U+05BF on the tav, exactly as MAM's base text does; neither note is *about* the rafe — one reports Leningrad lacking the tipeha for the lower accentuation, the other a reversed silluq and atnaḥ — so the pairing passes without comment, which is how a quoted form shows what a manuscript simply has. Aleppo is attested here too: both passages fall in the lost portion (the appendix dates the surviving Torah from Deut 28:17 וּמִשְׁאַרְתֶּֽךָ), but the same appendix records photographs taken while the codex was complete, among them "שני עמודים מספר דברים הכוללים את עשרת הדברות", cited `א-צילום`, which rule 4 counts as a reading of the codex rather than testimony to a lost part; MAM's apparatus draws on it inside that Decalogue at Deut 5:11 שָׁמ֛֣וֹר, "=א-צילום,ל (תביר ומונח)". Where that photograph is silent, Leningrad is the rule-4 proxy. A further **25** rafes sit inside נוסח note bodies, which rule 2 leaves alone. **LIMITATION to document**: Aleppo marks the rafe in many places MAM does not, and how many is not knowable. Yeivin ITM §397 (`N0381.md`): "The *rafe* sign is not used consistently. It is used more frequently where there is some possibility of confusion … but even there it is not marked consistently. Some MSS, such as B, mark *rafe* very rarely, and others, such as C and S, mark it frequently" — and ITM's description of C says its rafe is "used more frequently than in A (#397) and L", so Aleppo is among the sparing users. **So do not derive the missing rafes by rule**: that would fabricate a regularity Yeivin says the manuscripts lack. The census's 180,542 is a count of *eligible* letters (every בג"ד כפ"ת with no dagesh, plus every word-final he with no mappiq) — an upper bound on eligibility, never a count of what Aleppo has. near-aleppo is therefore sparser in rafe than the codex and does not attempt to make up the difference. |
| 9 | Strip extraordinary dots (U+05C4 upper, U+05C5 lower) — a blanket removal of both from every MAM token | **KEEP.** These are the classical puncta extraordinaria, part of the consonantal text tradition the manuscripts hold, and Aleppo has them. Census (`.novc/dots_census.py`): **17 dotted atoms in 15 verses** of the base text, plus 7 inside note bodies. Ten Torah places (Gen 16:5, 18:9, 19:33, 33:4, 37:12; Num 3:39, 9:10, 21:30, 29:15; Deut 29:28), four in the Prophets (2 Sam 19:20; Isa 44:9; Ezek 41:20, 46:22), one in the Writings (Ps 27:13) — matching Yeivin ITM §79's table (`N0072.md`) place for place. Deut 29:28 supplies three of the 17 atoms; Ps 27:13 is the only place with dots below as well as above. **At both verses where MAM's apparatus discusses the dots, MAM's base text follows Aleppo specifically, against Leningrad** — for the HTML documentation, alongside steps 4 and 6. Deut 29:28: "=א,ל1,ש,ש1,ק3,ל9 ומ"ש (11 נקודות מעל האותיות כולל האות עי"ן של "עַׄד־"); אבל כתי"ל,ל3=עַד־עוֹלָ֔ם (בלי נקודה מעל האות עי"ן)" — MAM has Aleppo's eleven dots including the one over the ayin, where Leningrad has ten, and Yeivin's table agrees with Aleppo ("all in two words, plus ʿayin"). Ps 27:13 לׅׄוּׅׄלֵׅ֗ׄאׅׄ: "=א ומסורת-א <נקוד מלמע' ולמטה>", against ל and ש1, which lack the dot under the vav — and that is the reading Yeivin's table prints ("all dotted above, and all but waw below"). So MAM here prefers Aleppo over Leningrad and over Yeivin's printed table alike. **A step-36 item falls out of the same Deut 29:28 note, and it overrides a step-5 rule**: "א=וּׄלְׄבָׄנֵׄיׄנׄוּ֙ׄ בפשטא אחת בלבד, כנראה בגלל הצפיפות שנגרמה ע"י הנקודות (הערת ברויאר ע"פ ייבין, כתר, כג הערה 1)". MAM's base text has **2** pashtas on that atom and the quoted Aleppo form **1** (counted by codepoint, `.novc/dt2928_pashta.py`). Step 5's pashta rule keeps a doubled pashta unless no letter stands between the stressed letter and the last letter, and a yod does stand between here, so that rule alone would keep both; the note overrides it. Worked example that a נוסח note beats a positional rule — which is what step 36 is for. |
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
  `py/accgram/ps17v14_mam_doc_notes_body.py` glossed ק13 as "Cambridge T-S 13" on its rendered
  page; `doc/sigil-decoding.md` marked the row Conflicting and said the page wanted fixing.
  Fixed 2026-08-23: the gloss is "Cairo 13" in the module and the regenerated page, and the
  row is Confirmed.
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
  varika count `(Get-Content C:\Users\BenDe\GitRepos\MAM-parsed\plus\*.json -Raw | Select-String -Pattern ([string][char]0xFB1E) -AllMatches | ForEach-Object { $_.Matches.Count } | Measure-Object -Sum).Sum` gave 685 (the same form with another codepoint gives each of the other codepoint counts here); `out/explicit-xataf.json` 666 mappings / 579 with `א`; `מ:קמץ` 375 templates; `מ:דחי` 2,316; `מ:צינור` 56; U+05A2 196 (Ps 173, Prov 8, Job 15), U+05AA 56; U+0598 and U+05AE per book as in step 6. **Step 7's figures come from one throwaway, `.novc/ole_census.py`** (`.venv\Scripts\python.exe .novc\ole_census.py`), which walks every verse's `EP` column and prints all of them: the ole U+05AB occurs only in Psalms (353), Proverbs (29) and Job (41), 423 in all and one apiece in 423 verses; same-letter ole-and-yored sites 13, matching ch. 5 part א; two-atom ole-veyored verses 55, matching ch. 5 part ב with an empty symmetric difference either way. Re-measure rather than trust; a mismatch is a finding. **Two traps that census records, both worth carrying into the real code**: a separator template must flatten to a **space**, never to the empty string — the line-break family `ר0`–`ר3`, the gray maqaf, the paseq and the legarmeh all separate atoms, and flattening one to the empty string fuses the atoms on either side of it, which lost Ps 31:19 (שִׂפְתֵ֫י + gray maqaf + שָׁ֥קֶר) and gave 54 against ch. 5's 55; and the base text is parameter `1` of a נוסח template, never the note body (rule 2 above). Unreconciled, and it does not bear on step 7: ch. 2's footnote says **421** verses are divided in their primary division by ole-veyored, where **423** verses have an ole. **Step 8's figures come from `.novc/rafe_census.py`**, which walks every template parameter and reports each rafe as base text, Decalogue dagesh-plus-rafe, or note body: **87**, **8** and **25** respectively, plus **180,542** eligible letters. Its walk is the one to copy for the real code — `ext.flatten_text` raises on `מ:כפול`, so a census that swallows that exception silently drops the whole Decalogue, which is how a first pass reported 0 Decalogue sites. The check scripts were throwaways under `.novc/` (`varika_notes_no_alef.py`, `qamats_tmpl_params.py`, `ole_census.py`, `rafe_census.py`, `dots_census.py`, `dt2928_pashta.py`) and are not tracked; each is a few dozen lines walking the raw JSON and is quicker to rewrite than to recover.
