# HBCE Psalms versus MAM: the digital differences, and the manuscript questions they raise

Claude-written on 2026-09-26 for Ben Denckla, who has not reviewed it.
Updates and later status: [hbce-psalms-vs-mam-2026-09-26-update.md](hbce-psalms-vs-mam-2026-09-26-update.md).

Claude Fable 5.1 drafted this report on 2026-09-26 as an untracked scratch file, and Claude Opus
5.5 revised it the same day, when the comparison moved into this repository. Everything it cites
is in `hbce-psalms/`, `py/hbce_psalms/` and `py/main_hbce_psalms.py`, listed in section 9.

## 1. Answer in brief

The Critical Edition of the Hebrew Psalter, a project of the series Hebrew Bible: A Critical
Edition co-directed by Brent Strawn and Drew Longacre at Duke University, publishes its diplomatic
transcriptions of Tiberian codices through a Virtual Manuscript Room (VMR), the platform of the
Institut für Neutestamentliche Textforschung (INTF), at hbcepsalms.manuscriptroom.com. This
report calls the project HBCE, as that address does. On 2026-09-26 a Claude session downloaded
HBCE's transcriptions of Psalms from that platform's web-service API before anyone had read the
site's robots.txt, which disallows the API to every agent. The download was made in good faith,
and it must not be repeated: if this work resumes, fresh data comes only by contacting the INTF
or through its documented exports (section 2).

HBCE's Aleppo Codex transcription (siglum MA) covers Psalms 1:1–14:7 and 25:2–51:14: the codex
lacks 15:1–25:1, and the transcription's last page ends inside 51:14. Against MAM the
transcription agrees on 4,004 of 4,510 chanted words. Of the 506 that differ, 311 differ only by
MAM's documented design policies, 23 are set aside, and 172 are reading differences: MAM has a
doc-note on the chanted word for 36 of those, a doc-note elsewhere in the verse for 22, and no
doc-note for 114.

Those 172 are questions, not findings. Of the 136 without a doc-note on the chanted word, 68 have
exactly the UXLC's form, which suggests that the transcribers edit a Leningrad-like base text and
that some of its forms survive into the Aleppo transcription. The one difference in letters, at
42:6, looks like such a survival on the drafting session's reading of the page image, which Ben
has not confirmed (section 6). So what the site offers MAM is a research queue with locations and
links (section 5), and four side assets (section 7), not a text to adopt.

## 2. Where the data came from, and why no more may be fetched

### 2.1 The download and robots.txt

The site's robots.txt, kept as evidence at `hbce-psalms/in/metadata/robots.txt`, disallows the
platform's web-service API to every user agent, asks for a crawl delay of 10 seconds, and asks
bulk data consumers to contact the INTF or to use its documented exports rather than walk the API.
On 2026-09-26 the drafting session made about 85 requests to that API before anyone had read
robots.txt, and every file under `hbce-psalms/in/` comes from those responses. The download was
made in good faith, by a session that had not read robots.txt. It must not be repeated.

If the work resumes, fresh data comes only by contacting the INTF or through its documented
exports, which is robots.txt's own advice. This session's instructions, which quote Ben, were to
keep the snapshot in MAM-basics as long as nothing here advises defying robots.txt, and not to
contact the INTF for now; whether to contact the INTF or HBCE later is Ben's decision. No fetcher
is kept in this repository, and nothing here gives the API's addresses or parameters.

### 2.2 What the snapshot holds

1. `hbce-psalms/in/transcriptions/` holds 35 TEI files, one per codex page, byte for byte as the API
   served them. `MA_25000.xml` to `MA_25140.xml` are the Aleppo Codex's 15 pages, Psalms
   1:1–14:7 and 25:2–51:14; `ML_25000.xml` to `ML_25190.xml` are the Leningrad Codex's 20 pages,
   Psalms 1:1–51:21. The number is the platform's page id. Each file is the transcription owned by
   the project account, since the platform's published transcription of each page was empty. All
   the pages are at the platform's confidence tier 2 and were still changing: Aleppo page 25010
   changed on 2026-09-24, the other Aleppo pages on 2026-09-10, and the Leningrad pages on
   2026-09-10 or 2026-09-16.
2. `hbce-psalms/in/metadata/` holds the API's catalogue responses for those documents:
   `MA_meta.json` and `ML_meta.json`, with each page's verse range and folio; `MA_pages.json`,
   `ML_pages.json` and `MS1_pages.json`, the pages that have the project's transcription (15, 20
   and 18; MS1 is Sassoon 1053, whose pages the snapshot does not hold); `MA_coverage.json`; and
   `MA_document_groups.json`, whose "HBCE ALL" group lists 109 documents. `MA_pages.json` and
   `ML_pages.json` were converted to LF line endings; every other file is byte for byte as served.
   The API's page describing its own usage was downloaded too, and is deliberately not kept.
3. The folio of an Aleppo page is the page index (n) of the Internet Archive's Aleppo_Codex item,
   as the drafting session identified it: 242r is n484 and 247v is n495. Three Aleppo pages have
   no folio in the catalogue. The research queue's locations use this index.
4. The TEI has letters, vowels, accents, meteg, maqaf (a `<w>` ending in a maqaf), paseq attached
   to the preceding chanted word, line and column breaks, spaces with a character count,
   corrections as `<app>` with `orig`, `corr` and `alt` readings by the first hand or a corrector,
   `<unclear>`, `<supplied>` and notes. It has no rafe on either codex's pages, and a few of the
   first hand's ketiv forms are unpointed. The Aleppo pages have sof pasuq in about a fifth of
   the verses, and U+059C GERESH 6 times against U+059D GERESH MUQDAM 392 times.
5. Each TEI file's header states "(C) 2026 Institut für Neutestamentliche Textforschung" and a
   Creative Commons Attribution 4.0 license; the platform generates that statement. The catalogue
   responses and robots.txt have no license statement. `DATA-LICENSES.md` records the terms.

## 3. How the comparison was made

- `py/main_hbce_psalms.py compare` regenerates every file under `hbce-psalms/out/` from the
  snapshot and from this repository's data, and `py/main_hbce_psalms.py lint-receipt` checks this
  report's Hebrew. The code is the package `py/hbce_psalms/`. Nothing touches the network.
- MAM's text is `MAM-simple/xml-vtrad-mam/Ps.xml`. MAM's doc-notes, 620 in Psalms, are found in
  `MAM-parsed/plus/D1-Psalms.json` by `explicit_xataf.extract.find_docnote_tmpls`, this
  repository's closed dispatch for doc-notes. MAM's general policies are in chapters 2 and 5 of the
  mirrored introduction, `in/mam-ws-intro/`. The UXLC's Psalms is `in/UXLC-39/Psalms.xml`.
- The unit is the chanted word as each source has it: a lone atom, or atoms joined by a maqaf of
  the text. MAM's gray maqaf is a reading aid, not a maqaf of the text, so it joins nothing here.
  Both sides are compared in MAM-normal mark order, and nothing is Unicode-normalized. A legarmeh or
  a narrow-sense paseq counts as a stroke after its chanted word, qamats qatan as qamats, and
  U+05BA HOLAM HASER FOR VAV as ḥolam.
- Each differing chanted word is classified mark by mark. A difference that one of MAM's documented
  policies explains is labelled `policy:` and set aside; the rest are reading differences, checked
  against the doc-notes of their verse and against the UXLC, and read beside HBCE's Leningrad
  transcription.
- U+05BD is labelled by its function where the data settles it. MAM's last U+05BD in a verse's
  final atom is the silluq, since `in/meteg_after_silluq_cases.json` puts Psalms' meteg-after-silluq
  cases at 60:10, 70:2 and 72:15, beyond both transcriptions. An HBCE U+05BD elsewhere in that
  atom is labelled `meteg-or-silluq` when HBCE lacks the mark on MAM's silluq syllable, and every
  other U+05BD is labelled `meteg`. A U+05BD on one side against a merkha, tipeḥa or munaḥ on the
  other, on the same letter, is also labelled `stroke-shape`: one stroke under the letter, read two
  ways.
- The revia of revia mugrash is set aside only when MAM has it on the geresh muqdam's letter, the
  case MAM's introduction states in chapter 2 and lists in chapter 5, 260 verses of Psalms,
  Proverbs and Job; a missing revia anywhere else is a finding.
- A ḥataf on a non-guttural letter where MAM has a sheva is set aside only when MAM has a doc-note
  on the chanted word, as MAM normally does for such a ḥataf (chapter 2); otherwise the row is
  labelled `hataf-without-mam-note` and is a finding. The one such row is at 7:9.

## 4. Results in numbers

| Comparison | Verses | Chanted words | Identical | Differing | Policy only | Set aside | Reading differences |
|---|---|---|---|---|---|---|---|
| HBCE's Aleppo transcription (MA) vs MAM, Psalms 1:1–14:7 and 25:2–51:14 | 624 | 4,510 | 4,004 | 506 | 311 | 23 | 172 |
| HBCE's Leningrad transcription (ML) vs MAM, Psalms 15:1–25:1, where MAM follows the Leningrad Codex | 170 | 1,212 | 1,112 | 100 | 69 | 6 | 25 |

The policy labels on the Aleppo rows, where a row can have several, are: the ḥolam of the divine
name, 222 rows; an atnaḥ hafukh that HBCE has with the galgal's code point, U+05AA, 67 rows; a
ḥataf on a non-guttural letter, 29; the revia of revia mugrash on the geresh muqdam's letter, 12;
and a supplied oleh, 2. The 23
Aleppo rows set aside are 8 that differ only in mark order (7 with the meteg before the vowel in
HBCE's form, and 35:6 with the atnaḥ before the ḥolam), 10 ketiv/qere rows, and 5 unpointed
first-hand ketivs with a pointed alternative.

Of the 136 Aleppo reading differences with no doc-note on the chanted word, 68 have exactly the
UXLC's form, 23 have MAM's form equal to the UXLC's, 20 differ from both, and 25 could not be
checked, because no UXLC atom matched or HBCE has no chanted word there.

The Leningrad comparison over MAM's Leningrad-based stretch leaves 25 reading differences: 23 with
a doc-note on the chanted word, 1 with a doc-note in the verse, and 1 with none, at 18:51. There
HBCE's Leningrad transcription has מִגְדַּל֮ where MAM has מַגְדִּל֮, and HBCE's editorial note says
that it points the ketiv as a construct.

`hbce-psalms/out/figures.txt` recomputes the row counts above that no other output states.

## 5. The research queue

`hbce-psalms/out/research_queue.md` lists the 172 reading differences with MAM's form, HBCE's
Aleppo and Leningrad forms, the UXLC's form, the difference, the doc-note status, the Aleppo
location (page index n, column, and line from HBCE's line breaks) and the mgketer, MwD, tica and
UXLC links. It has three tiers.

**Tier A, 68 rows: HBCE's Aleppo form differs from both MAM and the UXLC, and MAM has no doc-note
on the chanted word.** These are most likely the transcribers' deliberate decisions, and the first
to look at: accent 12, dagesh or shuruq dot 7, maqaf or grouping 18, meteg 13, silluq 1 (10:6),
stroke shape 10, vowel or dot 6, and the ḥataf at 7:9. For example:

- HBCE has a revia that MAM and the UXLC lack at 7:2 אֱ֭לֹ֗הַי, at 7:9 כְּצִדְ֗קִ֖י,
  at 43:3 אֶל־הַֽ֗ר־קָ֝דְשְׁךָ֗ and at 50:19 בְרָ֗עָ֑ה, and no galgal at 28:5, where MAM has לֹ֪א and HBCE לֹא.
- HBCE has a dagesh that MAM and the UXLC lack at 10:2 יִּדְלַ֣ק and 35:17 תִּ֫רְאֶ֥ה.
- HBCE has a qamats at 9:7 לָ֫נֶ֥צָח where MAM has a pataḥ, and lacks MAM's ḥolam
  at 44:24 אֲדנָ֑י and 45:3 אֱלהִ֣ים.
- At 13:6 and 31:25 HBCE has a tipeḥa, in לַ֖יהוָ֑ה and לַ֖יהוָֽה, where MAM has a meteg; at 46:11 a
  merkha, in כִּ֥י־אָנֹכִ֣י, where MAM has a meteg.
- At 30:10 HBCE has the compound אֶ֫ל־שָׁ֥חַת, where MAM has a gray maqaf and the UXLC a space; at
  34:10 HBCE has a space between אֶת and יְהוָ֣ה, where MAM and the UXLC have a maqaf.
- Of the 9 revia rows that fix 4 of section 10 turned into findings, 47:6 and 49:17 are here, and
  the other 7 are in tier B. The ḥataf at 7:9, שָׁפֲטֵ֥נִי, is fix 5's one finding.
- The 3 rows at 51:14 are not findings: the last Aleppo page ends inside the verse, so the rest of
  the verse is missing from the transcription, not from the codex.

**Tier B, 68 rows: HBCE's Aleppo form equals the UXLC's, and MAM has no doc-note on the chanted
word.** Accent 8, letters 1 (42:6), maqaf or grouping 4, meteg 38, oleh 1 (35:15), rafe 2, silluq
6 (5:10, 31:20, 37:31, 37:32, 39:4, 48:7), stroke shape 7, vowel or dot 1. In 30 of the 38 meteg
rows HBCE and the UXLC have a meteg that MAM lacks, and in the other 8 MAM has one that they lack.
Seven of the 8 accent rows are fix 4's revia rows, 2:2, 14:2, 28:6, 31:5, 35:20, 35:28 and 47:3:
MAM has the revia of revia mugrash on a later syllable than the geresh muqdam, and HBCE and the
UXLC lack it. Any of these rows may be a real feature of the codex that MAM lacks, or a form of
the base text that the transcribers left; only the page decides.

**Tier C, 36 rows: MAM documents the chanted word.** HBCE is a second opinion here, and it
sometimes disagrees with what MAM's doc-note says the codex has. At 7:6 MAM's doc-note says the
codex has the compound יִ֥רַדֹּֽף־אוֹיֵ֨ב, and HBCE has two chanted words, יִֽרַדֹּ֥ף with a merkha
and אוֹיֵ֨ב; at 12:6 MAM's doc-note says the codex has יָפִ֥יחַֽ־לֽוֹ, and HBCE has a space where the note
has the maqaf. At 39:13 MAM's doc-note gives the codex two chanted words with a ḥataf under the
mem, and HBCE has the compound שִֽׁמְעָ֥ה־תְפִלָּתִ֨י with a sheva. Elsewhere HBCE agrees with MAM's
note: at 32:10 HBCE has לָרָ֫שָׁ֥ע, the codex's form as MAM's doc-note gives it, where
MAM has לָ֫רָשָׁ֥ע.

## 6. Four page readings, not confirmed

Before Ben asked to stop, the drafting session looked at four places in the Internet Archive's
page images at two to three times magnification. These are that session's screen readings, which
Ben has not confirmed; they are not results.

1. At 42:6, n495, column 1, line 20, the session saw הוחלי with no yod after the ḥet, which is
   MAM's spelling; HBCE's הוֹחִ֣ילִי is the UXLC's form.
2. At 30:10, n489 (inferred: the catalogue gives that page no folio), column 2, line 17, the session
   saw no maqaf between אֶ֫ל and שָׁ֥חַת, where MAM has a gray maqaf; HBCE's maqaf is in neither MAM
   nor the UXLC.
3. At 36:7, n492, column 1, line 26, the session saw no maqaf between אָ֤דָֽם and וּבְהֵמָ֖ה, where MAM
   has a gray maqaf and its introduction's chapter 2 names the verse; HBCE's maqaf is the UXLC's.
4. At 34:10, n491, column 1, line 23, the session saw no maqaf between אֶת and יְהוָ֣ה, where MAM
   has אֶת־יְהֹוָ֣ה with no doc-note. If that reading holds, this one is a question for MAM.

If the readings hold, three of the four go against the transcription and one against MAM, as the
UXLC cross-check would lead one to expect: the transcription raises questions and settles none.

## 7. Four side assets

1. **The Leningrad transcription, 20 pages.** Over MAM's Leningrad-based Psalms 15:1–25:1 it
   leaves one reading difference without a doc-note (section 4). For the rest of Psalms 1–51 it
   gives MAM's doc-notes a machine-readable Leningrad form to cite or check
   (`hbce-psalms/out/compare_ML.tsv`).
2. **Sassoon 1053.** HBCE lists 18 pages of it with the project's transcription
   (`MS1_pages.json`), and many of MAM's Psalms doc-notes cite ש1. The snapshot does not hold
   the pages, and nothing compared them.
3. **Layout.** Every Aleppo page has column breaks, line breaks and spaces with character counts:
   the information that `aleppo/line-breaks/` holds, in Ben Denckla's annotations, for 35 other
   Aleppo pages, 24 of them in Job. A mechanical conversion could seed Aleppo page locations for
   Psalms.
4. **Physical-state notes and corrections.** The Aleppo pages have five notes: at 7:18 an editorial
   note that "It looks like עליון has been intentionally scraped off", and at 26:1, 26:11, 37:9 and
   37:14 notes on darker ink, some of it traced over faded text. They also have 18 `<app>` entries
   with first-hand and corrector forms, for example at 3:3, where a corrector erased the
   dagesh of בֵּאלֹהִ֬ים.

## 8. A workflow for the manuscript research, if it resumes

1. **Refresh** the snapshot only through the INTF or its documented exports, and only if the work
   resumes, never from the API (section 2). Then rerun `py/main_hbce_psalms.py compare` and read
   the diff of `hbce-psalms/out/`. The transcriptions were still being reconciled in 2026-09, so
   the queue will shrink and shift.
2. **Triage mechanically:** drop policy rows, mark-order rows and ketiv/qere rows; rank tier A
   before B before C, and within a tier letters, maqaf and grouping, accents, dagesh and vowels,
   meteg, and stroke shape.
3. **Present each item** as the queue does: MAM's form, HBCE's Aleppo and Leningrad forms, the
   UXLC's form, MAM's doc-note if any, the page n with column and line, and the links. Ben reads the
   page and decides.
4. **Record** each decision where it belongs: a Wikisource doc-note when MAM changes or explains
   its text, nothing when the transcription is wrong. Reporting corrections to HBCE, whose CC BY
   4.0 data would improve from them, would mean contacting the project, which is Ben's decision.
5. **Extend** the chain to Sassoon 1053, for MAM's ש1 citations, once its pages come through the
   INTF, and, if wanted, convert the layout markup into `aleppo/line-breaks/` files for Psalms.

## 9. Files

- `doc/hbce-psalms-vs-mam-2026-09-26.md`: this report.
- `hbce-psalms/README.md`: the directory's provenance, license and file map.
- `hbce-psalms/in/`: the snapshot (section 2).
- `hbce-psalms/out/research_queue.md`: the 172-row queue.
- `hbce-psalms/out/compare_MA.tsv`, `compare_ML_range.tsv` and `compare_ML.tsv`: every differing
  row, with labels, details, doc-note status and mentions in MAM's introduction;
  `compare_summary.txt` has the label counts.
- `hbce-psalms/out/candidates_MA_full.txt`: the Aleppo reading differences grouped by doc-note
  status, with the notes' text; `candidates_with_ML.tsv` and `candidates_with_ML_UXLC.tsv` add
  HBCE's Leningrad form and the UXLC's form.
- `hbce-psalms/out/mam_psalms_docnotes.tsv`: MAM's 620 doc-notes in Psalms, by chapter and verse.
- `hbce-psalms/out/tei_survey.txt`: the snapshot's element, attribute and mark inventory.
- `hbce-psalms/out/figures.txt`: the row counts this report quotes that no other output states.
- `py/main_hbce_psalms.py` and `py/hbce_psalms/`: the program.

## 10. Changes made while the scripts moved

The drafting session moved its scratch scripts into an untracked directory of MAM-private and
fixed six defects on the way. Each fix changed the outputs, and each difference was traced to its
fix:

1. The doc-note census took any template whose name has the Hebrew for "note", which caught 8
   link templates inside notes; after the fix it took the doc-note template by name: 620
   doc-notes, not 628.
2. Every U+05BD difference was labelled meteg; the silluq, meteg-or-silluq and stroke-shape labels
   of section 3 replaced that.
3. The Leningrad comparisons labelled their side "Aleppo"; they say "Leningrad" now.
4. The revia-mugrash rule set aside any missing revia in a chanted word with a geresh muqdam. MAM's
   policy (introduction, chapter 2) and its list of 260 verses (chapter 5) cover only the case
   with both marks on one letter, so 9 Aleppo rows became findings: 2:2, 14:2, 28:6, 31:5, 35:20,
   35:28, 47:3, 47:6 and 49:17.
5. The ḥataf rule set aside every ḥataf where MAM has a sheva, but MAM normally documents such a
   ḥataf in a doc-note on the chanted word, so a ḥataf with no such note, at 7:9, became a finding.
   A "(NO varika)" suffix on those labels was dropped: MAM-simple has no varika at all.
6. Every `<pc>` is a sof pasuq, which the TEI has in three ways: the character itself; once on the
   Aleppo pages as the character followed by "caes", a mistyped caesura; and 23 times on the
   Leningrad pages as an ASCII colon. The scratch run skipped the last two silently.

The move into MAM-basics, the same day, made five more changes. Each was checked by regenerating
every output and comparing it byte for byte with the MAM-private output once the change was
undone:

7. The doc-note census uses `explicit_xataf.extract.find_docnote_tmpls` in place of its own walk
   through every template parameter, which Ben's rule for closed template dispatch forbids;
   `mam_psalms_docnotes.tsv` came out byte-identical.
8. Two labels have x for ḥet, as `py/tests/test_transliterations.py` requires:
   `policy:atnax-hafukh-encoded-as-galgal` and `policy:dexi-doubled`. The queue's heading "maqaf or
   word division" is "maqaf or grouping", as `py/tests/test_prose_conventions.py` requires.
9. The queue shows every form in MAM-normal mark order, as `py/tests/test_prose_mark_order.py`
   requires of every tracked `.md`; 8 of HBCE's Aleppo forms there changed order. The TSVs keep
   each source's order.
10. The queue's links come from the two functions that `py/main_verse_links.py` prints them from,
    not from running that program once per verse; no link changed.
11. `tei_survey.txt`, which the MAM-private runner was to save but never had, and `figures.txt` are
    new. `candidates_MA_full.txt` has LF line endings where the MAM-private copy had CRLF.
