# morphhb's corrections of WLC: the Israel Bible review's cases, then all of morphhb

Written by Claude (Opus 5.5) on 2026-11-13, New York time, in the session that the commander
session "Commander for Claude's forests" (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) started
from the brief
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/morphhb-corrections-brief-2026-11-13.md`.
Ben's request, as the brief quotes it:

> ask the commander to start a session that will investigate all other such corrections in morphhb, or at least to start with, see whether there are corrections for all or some of the other cases identified in my israel bible review.

Everything else here is Claude's work and has not been reviewed by a human. Nothing tracked
changed, nothing was committed, and nothing was posted anywhere. `README.md` is written by
`scripts/make_readme.py` from `scripts/README.template.md`, so that every Hebrew form in it is
copied by script from the review's inputs or from morphhb's files.

A **correction**, as the brief defines it, is a word whose text keeps WLC's reading while its
lemma or its morph analyses another reading, typically MAM's. A place where morphhb changed the
text itself is a separate kind, a **text change**. Every reading below is attributed to the
transcription that has it: WLC, the UXLC or MAM. Nothing here says what the Leningrad Codex has.

## The answer in brief

1. **Of the review's 56 cases, morphhb corrects 5, and they are all five of its al/el rows**:
   Exodus 10:28, Deuteronomy 2:9, Joshua 22:19, Judges 19:23 and Jeremiah 47:6 (Part 1).
2. **In all of morphhb there are nine corrections**: those five; Hosea 13:15, where the lemma
   reads MAM's word and the letters differ; and three words that differ only by a mappiq, where
   the morph reads MAM's form (Genesis 39:19, Deuteronomy 22:29, Leviticus 4:35). Each of the
   nine lemmas' numbers is already in morphhb's first GitHub commit, of 2009-12-28, and no
   record of morphhb's own describes any of the nine (Part 2).
3. **morphhb's text is WLC 4.20's**, apart from systematic differences of encoding, the
   Decalogues' divided accents, 12 words divided for exegesis and one ketiv and qere at
   Daniel 2:39 (Part 2).

## Part 1: the review's cases

### The answer

Each of the review's 56 cases falls in one of four classes, which the commander's brief
defined: (a) morphhb's lemma and morph fit only WLC's form; (b) the lemma, the morph or both
fit only MAM's form, so morphhb corrects WLC there; (c) they fit both forms, because the two
differ only in pointing that neither the lemma nor the morph records; (d) morphhb's text is not
WLC 4.18's.

1. **morphhb corrects 5 of the review's 56 cases, and they are all five of its al/el rows**:
   Exodus 10:28, Deuteronomy 2:9, Joshua 22:19, Judges 19:23 and Jeremiah 47:6. At each,
   morphhb's text keeps WLC's atom while its lemma reads MAM's: lemma 408, the negative, on
   WLC's segol form אֶל־ (Exodus 10:28, Deuteronomy 2:9, Joshua 22:19), and
   lemma 413, the preposition, on WLC's patah form אַל־ (Judges 19:23,
   Jeremiah 47:6). At Exodus 10:28 the morph, `HTn`, the negative particle, reads MAM's form
   too; at the other four the morph reads WLC's atom as written. All five lemmas have been on
   their words since morphhb's first GitHub commit, `c299c30a` of 2009-12-28; the morphs came
   with the parsing work of 2017 and 2018.
2. **One case reads WLC's form where MAM's differs (class a)**: at Judges 19:4 the morph
   `HC/Vqw3ms`, a Qal, analyses WLC's atom, while MAM's atom is a Hiphil.
3. **Four cases are text changes (class d)**. At Judges 15:14 and Ecclesiastes 2:23 morphhb's
   text is WLC 4.20's, which morphhb took on 2016-03-04; at Ecclesiastes 2:23 that is also
   MAM's form. At Exodus 20:4 and at the first of the two Deuteronomy 5:8 rows, morphhb's
   separation of the Decalogues' two accentuations, on 2010-07-13, changed the review's form:
   it dropped WLC's patah at Exodus 20:4 and a maqaf at Deuteronomy 5:8.
4. **The other 46 cases are class c**: the difference between WLC's form and MAM's is one of
   pointing that neither the lemma nor the morph encodes, and morphhb's text there is WLC
   4.18's by the review's own comparison key.
5. **The six verses of the footnote `mam-hataf-ng` are all class c**: at each, morphhb's text
   has WLC's vowel where MAM has a ḥataf, and the lemma and morph are the same for both.
6. **No openscriptures/morphhb issue, pull request or comment mentions any of these verses**:
   117 issues and pull requests, 390 comments and 6 review comments, fetched on 2026-11-13,
   were searched for each verse in several spellings and for the five words' ids.

### The five corrections

| Verse | WLC 4.18, 4.20, 4.22 and UXLC 2.6 | MAM | morphhb's lemma | morphhb's morph | WLC's note at the chanted word | Lemma since | Morph since |
|---|---|---|---|---|---|---|---|
| Exodus 10:28 | אֶל־ | אַל־ | 408, the negative: MAM's | `HTn`, the negative: MAM's | none in 4.18 or 4.20; note 1 in 4.22 | `c299c30a`, 2009-12-28 | `f0b4e882`, 2018-12-14 |
| Deuteronomy 2:9 | אֶל־תָּצַר | אַל־תָּצַר | 408, the negative: MAM's | `HR`, the preposition: WLC's | U in 4.18, 4.20 and 4.22 | `c299c30a`, 2009-12-28 | `f0b4e882`, 2018-12-14 |
| Joshua 22:19 | אֶל־תִּמְרֹדוּ | אַל־תִּמְרֹדוּ | 408, the negative: MAM's | `HR`, the preposition: WLC's | none in 4.18 or 4.20; note 1 in 4.22 | `c299c30a`, 2009-12-28 | `f0b4e882`, 2018-12-14 |
| Judges 19:23 | אַל־בֵּיתִי | אֶל־בֵּיתִי | 413, the preposition: MAM's | `HTn`, the negative: WLC's | U in 4.18, 4.20 and 4.22 | `c299c30a`, 2009-12-28 | `097d0e42`, 2017-12-10 |
| Jeremiah 47:6 | אַל־ | אֶל־ | 413, the preposition: MAM's | `HTn`, the negative: WLC's | none in 4.18 or 4.20; note 1 in 4.22 | `c299c30a`, 2009-12-28 | `097d0e42`, 2017-12-10 |

1. **The texts.** WLC 4.18, 4.20 and 4.22 and UXLC 2.6 have the same atom at each of the five
   places (`out/13-verses.txt`), and morphhb's text has it too. morphhb carries WLC's notes as
   WLC 4.20 has them: note U where 4.20 has it, and none of the three notes 1 that WLC 4.22 added.
2. **The lemmas.** Each lemma is the same in the first commit as now, and in every version
   probed between them (`out/21-history.txt`). So each correction is at least as old as the
   files that David Troidl kept in Google's SVN before 2009-12-28, which were not read.
3. **The morphs.** `097d0e42`, "added phase 1 parsings--ruth, obad, jonah, joel complete;
   other books partial", gave Judges and Jeremiah their morphs; `f0b4e882`, "Addition of almost
   all verifieds", gave Exodus, Deuteronomy and Joshua theirs. Every version probed after those
   commits has the same morph.
4. **Context.** Where the verse has other al/el atoms, in Deuteronomy 2:9, Joshua 22:19 and
   Judges 19:23, morphhb gives them the lemma and morph that their own vowels call for: in
   Joshua 22:19, for example, the first atom of the segol form has lemma 413 and morph `HR`,
   and the atom of the patah form has lemma 408 and morph `HTn` (`out/13-verses.txt`).

### How Part 1 was done

1. **The cases.** The 43 rows of `in/israel-bible-review/forms.json`, the 5 rows of the tour's
   table in `review.md` and the 8 rows of its Decalogues' table, read with the review module's
   own readers (`py/author_misc/israel_bible_review_index.py`): 56 cases, as the brief's draft
   counted. The footnote `mam-hataf-ng` names six more verses, handled apart.
2. **Versification.** The review's references are in BHS's numbering: its lint,
   `py/tests/test_israel_bible_review_mam_forms.py`, reads MAM-simple's `json-vtrad-bhs`
   (`_VTRAD = "bhs"`), and its docstring says that the page's verses are the Israel Bible's,
   that is WLC's. morphhb's `wlc/` uses the same numbering: its plain `<note>` elements give
   the KJV's, as `KJV:Gen.31.55` at `Gen.32.1`. So every case was looked up under its own
   reference in every source.
3. **The texts.** morphhb's `wlc/<book>.xml` at `d4265dfa`, master's head; WLC 4.18 in
   Sefaria-Data's copy of tanach.us's build 24.2
   (`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/wlc418-tanach-us/sefaria-data-0f63a5fe/`); WLC
   4.20 and 4.22 in MAM-basics' tracked Unicode conversions `out/wlc420-u` and `out/wlc422-u`;
   UXLC 2.6 in `in/UXLC-39/`; MAM in MAM-simple's BHS JSON, read by the review's lint's own
   functions.
4. **Matching.** In each verse, WLC 4.18's atoms and MAM's were aligned by their letters, and
   the case is the run of WLC 4.18's atoms that matches the Israel Bible's form where MAM's
   aligned atoms match MAM's form. Forms are compared by the review's own key
   (`israel_bible_review_index.key`), which strips accents, meteg and the like and sorts each
   letter's marks, so mark order cannot hide a match. Every one of the 56 forms of the Israel
   Bible matched WLC 4.18 at exactly one place, as the review's premise says it should.
   morphhb's atoms and WLC 4.20's and 4.22's were then aligned with WLC 4.18's the same way.
5. **The classes**, as the brief gives them: (a) the lemma and the morph fit only the form as
   written; (b) the lemma, the morph or both fit only MAM's form, a correction; (c) both forms
   fit, because the difference is only in pointing; (d) morphhb's text differs from WLC 4.18's.
   The class is Claude's reading of the evidence, and each case that is not plainly class c
   says why in the table's last column.
6. **History.** For each class b and class d case, a binary search over every version of its
   book (from 53 to 71 versions each) found the commit that brought the current value, and
   chosen versions around morphhb's WLC updates were probed as well (`out/21-history.txt`,
   `out/22-probes.txt`). The search assumes that a value, once it came, did not leave and come
   back; the probes found exactly that pattern at Judges 15:14 and Ecclesiastes 2:23, which is
   why they were made.

### Every case

The Israel Bible's form and MAM's are as the review stores them. morphhb's text is shown
stripped as the review strips forms and in MAM-normal mark order; `out/10-part1-cases.txt` has
the raw `<w>` elements. "WLC 4.18 notes" and "morphhb notes" are the note letters at the
case's atoms: WLC's notes are at the end of the chanted word, and so are morphhb's copies of
them.

| # | Verse | Israel Bible (WLC 4.18) | MAM | morphhb `<w>`: text · lemma · morph · id | WLC 4.18 notes | morphhb notes | Class | What, and since when |
|---|---|---|---|---|---|---|---|---|
| 1 | Genesis 32:18 | וִשְׁאֵלְךָ | וּשְׁאֵלְךָ | וִשְׁאֵלְךָ · c/7592 · `HC/Vqq3ms/Sp2ms` · `01PwH` | 1 | 1 | c |  |
| 2 | Genesis 34:11 | אָבִיה | אָבִיהָ | אָבִיה · 1 · `HNcmsc/Sp3fs` · `011Dh` | 1 | 1 | c |  |
| 3 | Exodus 1:3 | וּבְנְיָמִן | וּבִנְיָמִן | וּבְנְיָמִן · c/1144 · `HC/Np` · `02yNB` | 1 | 1 | c |  |
| 4 | Exodus 10:28 | אֶל־ | אַל־ | אֶל־ · 408 · `HTn` · `02ubY` | – | – | **b** | lemma 408 and morph `HTn` (the negative) both read MAM's patah form; WLC has no note at the chanted word; lemma: since `c299c30a` (2009-12-28), morphhb's first GitHub commit; morph: `f0b4e882` (2018-12-14, "Addition of almost all verifieds") |
| 5 | Numbers 2:14 | וְמַטֵּה | וּמַטֵּה | וְמַטֵּה · c/4294 · `HC/Ncmsc` · `04qjY` | – | – | c |  |
| 6 | Numbers 26:7 | הָרֻאוּבֵנִי | הָראֿוּבֵנִי | הָרֻאוּבֵנִי · d/7206 · `HTd/Ngmsa` · `04ZHi` | 1 | 1 | c |  |
| 7 | Deuteronomy 2:9 | אֶל־תָּצַר | אַל־תָּצַר | אֶל־ · 408 · `HR` · `057a3`; תָּצַר · 6696 b · `HVqj2ms` · `05k23` | U | U | **b** | lemma 408 (the negative) reads MAM's patah form; morph `HR` (the preposition) reads WLC's segol form; WLC's note U ends the chanted word, and morphhb carries it; lemma: since `c299c30a` (2009-12-28), morphhb's first GitHub commit; morph: `f0b4e882` (2018-12-14, "Addition of almost all verifieds") |
| 8 | Deuteronomy 3:12 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי · l/7206 · `HRd/Ngmsa` · `05pDQ` | U | U | c |  |
| 9 | Deuteronomy 3:16 | וְלָרֻאוּבֵנִי | וְלָראֿוּבֵנִי | וְלָרֻאוּבֵנִי · c/l/7206 · `HC/Rd/Ngmsa` · `05EJP` | U | U | c |  |
| 10 | Deuteronomy 4:43 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי · l/7206 · `HRd/Ngmsa` · `05f8m` | U | U | c |  |
| 11 | Joshua 12:6 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי · l/7206 · `HRd/Ngmsa` · `06eix` | – | – | c |  |
| 12 | Joshua 22:19 | אֶל־תִּמְרֹדוּ | אַל־תִּמְרֹדוּ | אֶל־ · 408 · `HR` · `06Umo`; תִּמְרֹדוּ · 4775 · `HVqj2mp` · `067NW` | – | – | **b** | lemma 408 (the negative) reads MAM's patah form; morph `HR` (the preposition) reads WLC's segol form; no note in WLC 4.18, 4.20 or morphhb (WLC 4.22 adds note 1); lemma: since `c299c30a` (2009-12-28), morphhb's first GitHub commit; morph: `f0b4e882` (2018-12-14, "Addition of almost all verifieds") |
| 13 | Judges 15:14 | וּפְלִשִׁתִּים | וּפְלִשְׁתִּים | וּפִלְשִׁתִּים · c/6430 · `HC/Ngmpa` · `07fz2` | Q, n, v | Q, n, v | **d** | morphhb's text is WLC 4.20's (and 4.22's) form, neither WLC 4.18's nor MAM's; lemma and morph fit all three; text: MAM's form until `d1325011` (2013-07-11, "Update to WLC 4.18") brought WLC 4.18's; `2201c6a7` (2016-03-04, "Update to WLC 4.20") brought the present form |
| 14 | Judges 16:2 | וַהֲרְגְנֻהוּ | וַהֲרַגְנֻהוּ | וַהֲרְגְנֻהוּ · c/2026 · `HC/Vqp1cp/Sp3ms` · `07YiE` | U | U | c |  |
| 15 | Judges 19:4 | וַיֶּחֱזַק־ | וַיַּחֲזֶק־ | וַיֶּחֱזַק־ · c/2388 · `HC/Vqw3ms` · `07GJ8` | – | – | **a** | morph `HC/Vqw3ms` is a Qal, WLC's form; MAM's form is a Hiphil; the lemma fits both; morph: `097d0e42` (2017-12-10, "added phase 1 parsings") |
| 16 | Judges 19:23 | אַל־בֵּיתִי | אֶל־בֵּיתִי | אַל־ · 413 · `HTn` · `07HwX`; בֵּיתִי · 1004 b · `HNcmsc/Sp1cs` · `07Lda` | U | U | **b** | lemma 413 (the preposition) reads MAM's segol form; morph `HTn` (the negative) reads WLC's patah form; WLC's note U ends the chanted word, and morphhb carries it; lemma: since `c299c30a` (2009-12-28), morphhb's first GitHub commit; morph: `097d0e42` (2017-12-10, "added phase 1 parsings") |
| 17 | 1 Samuel 27:10 | הַיַּרְחְמְאֵלִי | הַיְּרַחְמְאֵלִי | הַיַּרְחְמְאֵלִי · d/3397 · `HTd/Ngmsa` · `09KmV` | – | – | c |  |
| 18 | 2 Samuel 11:1 | הַמַּלְאכִים | הַמְּלָאכִים | הַמַּלְאכִים · d/4428 · `HTd/Ncmpa` · `10264` | 1 | 1 | c | WLC's rafeh marks the alef silent, so WLC's form too reads as lemma 4428, 'kings'; morphhb keeps the rafeh, which WLC 4.22 drops |
| 19 | 2 Samuel 13:33 | אִם־אַמְנוֹן | אם־אַמְנוֹן | אִם־ · 518 b · `HC` · `10kX9`; אַמְנוֹן · 550 · `HNp` · `103n3` | – | – | c | MAM writes this atom without reading it; morphhb, like WLC, points it and analyses it as the conjunction |
| 20 | 2 Samuel 15:21 | כִּי אִם־ | כִּי אם | כִּי · 3588 b · `HC` · `107eY`; אִם־ · 518 b · `HC` · `105KS` | – | – | c | MAM writes this atom without reading it; morphhb, like WLC, points it and analyses it as the conjunction |
| 21 | 2 Kings 10:33 | וְהָרֻאובֵנִי | וְהָראֿוּבֵנִי | וְהָרֻאובֵנִי · c/d/7206 · `HC/Td/Ngmsa` · `12imA` | – | – | c |  |
| 22 | 2 Kings 18:27 (qere) | מימֵי רַגְלֵיהֶם | מֵימֵי רַגְלֵיהֶם | מימֵי · 4325 · `HNcmpc` · `12cPo`; רַגְלֵיהֶם · 7272 · `HNcfdc/Sp3mp` · `12HCo` | c, n, v | c, n | c |  |
| 23 | Isaiah 23:8 | סֹחֲרֶיה | סֹחֲרֶיהָ | סֹחֲרֶיה · 5503 · `HVqrmpc/Sp3fs` · `23F8H` | – | – | c | outside the form: morphhb has HEBREW ACCENT QADMA on the first syllable where WLC has a second pashta, since `380f4219` (2014-02-04, "Corrected pashta in the middle of a word") |
| 24 | Isaiah 46:4 | שֵיבָה | שֵׂיבָה | שֵיבָה · 7872 · `HNcfsa` · `23F41` | 1 | 1 | c | WLC's letter has no dot; lemma 7872 reads it as sin, as MAM writes it |
| 25 | Isaiah 66:22 | הַחֳדָשִׁים | הַחֲדָשִׁים | הַחֳדָשִׁים · d/2319 · `HTd/Aampa` · `23kzo` | – | – | c |  |
| 26 | Jeremiah 3:17 | וְנִקְוּוּ | וְנִקְווּ | וְנִקְוּוּ · c/6960 b · `HC/VNq3cp` · `24r8g` | – | – | c |  |
| 27 | Jeremiah 47:6 | אַל־ | אֶל־ | אַל־ · 413 · `HTn` · `242CG` | – | – | **b** | lemma 413 (the preposition) reads MAM's segol form; morph `HTn` (the negative) reads WLC's patah form; no WLC note; lemma: since `c299c30a` (2009-12-28), morphhb's first GitHub commit; morph: `097d0e42` (2017-12-10, "added phase 1 parsings") |
| 28 | Hosea 2:4 | מִפָּנֶיה | מִפָּנֶיהָ | מִפָּנֶיה · m/6440 · `HR/Ncbpc/Sp3fs` · `28PGK` | U | U | c |  |
| 29 | Hosea 2:17 | וִּכְיוֹם | וּכְיוֹם | וִּכְיוֹם · c/k/3117 · `HC/R/Ncmsc` · `282gM` | U | U | c |  |
| 30 | Joel 2:12 | וּבְבְכִי | וּבִבְכִי | וּבְבְכִי · c/b/1065 · `HC/R/Ncmsa` · `29c6V` | U | U | c |  |
| 31 | Jonah 3:2 | וִּקְרָא | וּקְרָא | וִּקְרָא · c/7121 · `HC/Vqv2ms` · `32ki2` | U | U | c |  |
| 32 | Zechariah 2:2 | וִירוּשָׁלָם | וִירוּשָׁלִָם | וִירוּשָׁלָם · c/3389 · `HC/Np` · `38ZpQ` | U | U | c |  |
| 33 | Psalms 45:3 | בְּשְׂפְתוֹתֶיךָ | בְּשִׂפְתוֹתֶיךָ | בְּשְׂפְתוֹתֶיךָ · b/8193 · `HR/Ncfpc/Sp2ms` · `19K1g` | – | – | c |  |
| 34 | Proverbs 12:9 | מִמְּתַכַּבֵּד | מִמִּתְכַּבֵּד | מִמְּתַכַּבֵּד · m/3513 · `HR/Vtrmsa` · `20f6y` | – | – | c | morph `HR/Vtrmsa` names MAM's Hithpael participle; WLC's vowels are anomalous but admit no other stem or form |
| 35 | Proverbs 20:1 | הַיַּין | הַיַּיִן | הַיַּין · d/3196 · `HTd/Ncmsa` · `20Rm3` | U | U | c |  |
| 36 | Proverbs 31:12 | חַיֶּיה | חַיֶּיהָ | חַיֶּיה · 2416 e · `HNcmpc/Sp3fs` · `20cd3` | U | U | c |  |
| 37 | Job 31:7 | מֻאוּם | מאֿוּם | מֻאוּם · 3971 a · `HNcmsa` · `18Wom` | 1 | 1 | c |  |
| 38 | Song of Songs 5:11 | קְוּצּוֹתָיו | קְוֻצּוֹתָיו | קְוּצּוֹתָיו · 6977 · `HNcfpc/Sp3ms` · `22k23` | U | U | c |  |
| 39 | Daniel 2:45 | וְהַדֶּקֶת | וְהַדֵּקֶת | וְהַדֶּקֶת · c/1855 · `AC/Vhp3fs` · `27Z1J` | – | – | c |  |
| 40 | Daniel 5:24 | שְׁלִיַחַ | שְׁלִיחַ | שְׁלִיַחַ · 7972 · `AVQp3ms` · `27sKp` | 1 | 1 | c |  |
| 41 | Daniel 7:20 | וְפֻם | וּפֻם | וְפֻם · c/6433 · `AC/Ncmsa` · `275bQ` | – | – | c |  |
| 42 | Nehemiah 9:14 | הוֹדַעַתָ | הוֹדַעְתָּ | הוֹדַעַתָ · 3045 · `HVhp2ms` · `16tnE` | U | U | c |  |
| 43 | 1 Chronicles 3:1 | דָויִד | דָוִיד | דָויִד · 1732 · `HNp` · `13ZNU` | 1 | 1 | c |  |
| 44 | Deut 3:22 | תְִּירָאוּם | תִּירָאוּם | תְִּירָאוּם · 3372 · `HVqi2mp/Sp3mp` · `05wNE` | Q, n, v | Q, n, v | c |  |
| 45 | Isa 49:23 | קוָֹי׃ | קֹוָי׃ | קוָֹי · 6960 a · `HVqrmpc/Sp1cs` · `23zh5` | – | – | c |  |
| 46 | Lam 3:25 | לְקוָֹו | לְקֹוָו | לְקוָֹו · l/6960 a · `HR/Vqrmpc/Sp3ms` · `25eec` | Q, q | Q, q | c |  |
| 47 | Lam 4:4 | אֶל־חכּוֹ | אֶל־חִכּוֹ | אֶל־ · 413 · `HR` · `257tY`; חכּוֹ · 2441 · `HNcmsc/Sp3ms` · `252Dp` | Q, n, v | Q, n, v | c |  |
| 48 | Eccl 2:23 | לִבּו | לִבּוֹ | לִבּוֹ · 3820 a · `HNcmsc/Sp3ms` · `21nzj` | Q, n, v | – | **d** | morphhb's text is WLC 4.20's (and 4.22's) form, which is MAM's; lemma and morph fit both; text: MAM's form until `57e5e441` (2010-03-31, "Update to WLC 4.12") brought the form IB has; `2201c6a7` (2016-03-04, "Update to WLC 4.20") brought back the present form |
| 49 | Exod 20:3 | עַל־פָּנָיַ | עַל־פָּנַי | עַל־ · 5921 a · `HR` · `02qKv`; פָּנָיַ · 6440 · `HNcbpc/Sp1cs` · `02CuC` | 1 | 1 | c | morphhb's text has WLC's two vowels; its accents are divided as `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |
| 50 | Deut 5:7 | עַל־פָּנָיַ | עַל־פָּנַי | עַל־ · 5921 a · `HR` · `05oYz`; פָּנָיַ · 6440 · `HNcbpc/Sp1cs` · `05dD2` | – | – | c | morphhb's text has WLC's two vowels; its accents are divided as `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |
| 51 | Exod 20:4 | מִתַָּחַת | מִתַּחַת | מִתָּחַת · m/8478 · `HR/D` · `02p5S` | 1 | 1 | **d** | morphhb's text has the qamats alone; WLC 4.18, 4.20 and 4.22 have the qamats and the patah; morphhb's alternative-accent note has the qamats too; lemma and morph fit both; text: `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |
| 52 | Exod 20:9 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | כָּל־ · 3605 · `HNcmsc` · `02pGd`; מְלַאכְתֶּךָ · 4399 · `HNcfsc/Sp2ms` · `02S8b` | 1 | 1 | c |  |
| 53 | Exod 20:10 | לֹא־תַעֲשֶׂה | לֹא תַעֲשֶׂה | לֹא־ · 3808 · `HTn` · `02Jx8`; תַעֲשֶׂה · 6213 a · `HVqi2ms` · `02BdY` | – | – | c |  |
| 54 | Deut 5:8 (Decalogue row 6) | לֹא־תַעֲשֶׂה־לְךָ | לֹא תַעֲשֶׂה־לְךָ | לֹא־ · 3808 · `HTn` · `052t9`; תַעֲשֶׂה · 6213 a · `HVqi2ms` · `05fou`; לְךָ · l · `HR/Sp2ms` · `05DL4` | – | – | **d** | morphhb's main text has no maqaf after the second atom; its alternative-accent note has MAM's עליון form exactly; lemma and morph fit both; text: `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |
| 55 | Deut 5:8 (Decalogue row 7) | מִתָּחַת | מִתַּחַת | מִתָּחַת · m/8478 · `HR/R` · `05jMY` | – | – | c | morphhb's text has WLC's qamats; its accents are divided as `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |
| 56 | Deut 5:13 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | כָּל־ · 3605 · `HNcmsc` · `05YWx`; מְלַאכְתֶּךָ · 4399 · `HNcfsc/Sp2ms` · `05d4u` | – | – | c | morphhb's main text has WLC's dagesh without its rafeh; its alternative-accent note has the rafeh without the dagesh, since `73784451` (2010-07-13, "Separated the accents of the Ten Commandments, to conform with the WLC versification") |

| Verse | WLC 4.18 | MAM | morphhb `<w>`: text · lemma · morph · id | Class |
|---|---|---|---|---|
| Ezekiel 44:13 | הַקְּדָשִׁים | הַקֳּדָשִׁים | הַקְּדָשִׁים · d/6944 · `HTd/Ncmpa` · `267mi` | c |
| Ezra 4:9 (qere) | אַרְכְּוָיֵא | אַרְכֳּוָיֵא | אַרְכְּוָיֵא · 756 · `ANgmpd/Td` · `15mQU` | c |
| 2 Chronicles 5:7 | הַקְּדָשִׁים | הַקֳּדָשִׁים | הַקְּדָשִׁים · d/6944 · `HTd/Ncmpa` · `14CoS` | c |
| Numbers 35:20 | יֶהְדָּפֶנּוּ | יֶהְדֳּפֶנּוּ | יֶהְדָּפֶנּוּ · 1920 · `HVqi3ms/Sp3ms` · `04Nxj` | c |
| 1 Samuel 26:10 | יִגָּפֶנּוּ | יִגֳּפֶנּוּ | יִגָּפֶנּוּ · 5062 · `HVqi3ms/Sp1cp` · `09hk6` | c |
| 2 Samuel 6:5 | וּבְצֶלְצֶלִים | וּבְצֶלְצֱלִים | וּבְצֶלְצֶלִים · c/b/6767 d · `HC/R/Ncmpa` · `10zyy` | c |

The footnote's six cases are in the second table. Outside the question asked here, morphhb's
morph at 1 Samuel 26:10, `HVqi3ms/Sp1cp`, gives the suffix as first person plural; the
energic suffix with a dagesh in the nun is third person masculine singular.

### What the cases show about morphhb's text

1. **It is WLC 4.20's text**, not 4.18's or 4.22's: Judges 15:14 and Ecclesiastes 2:23 have
   WLC 4.20's forms; 2 Samuel 11:1 keeps the rafeh that WLC 4.22 dropped; and the notes follow
   WLC 4.20 (Genesis 32:18's note 1, which WLC 4.22 turned into U; 2 Kings 18:27's notes c and n,
   without WLC 4.18's v; no notes at Ecclesiastes 2:23, where WLC 4.20 dropped 4.18's three; and
   none of the notes 1 that WLC 4.22 added at Exodus 10:28, Joshua 22:19 and Jeremiah 47:6).
   morphhb's history names its updates: WLC 4.12 (`57e5e441`, 2010-03-31), 4.14 (`57206c9b`,
   2011-01-22), 4.16 (`11626b6f`, 2012-07-19), 4.18 (`d1325011`, 2013-07-11) and 4.20
   (`2201c6a7`, 2016-03-04), and none later (`out/04-commit-list.txt`). Part 2 tests this for
   the whole text.
2. **It encodes the first of two pashtas as a qadma.** At Deuteronomy 2:9, Exodus 10:28 and
   Isaiah 23:8 morphhb has HEBREW ACCENT QADMA on the stressed syllable where WLC has a second
   HEBREW ACCENT PASHTA, since `380f4219` (2014-02-04, "Corrected pashta in the middle of a
   word"). Outside the review's forms, which carry no accents.
3. **It divides the Decalogues' two accentuations.** Since `73784451` (2010-07-13, "Separated
   the accents of the Ten Commandments, to conform with the WLC versification"), the main text
   of each Decalogue has one accentuation and a `<note type="alternative">` gives the other
   reading of the words that differ. In the review's eight Decalogue rows the main text keeps
   WLC 4.18's form six times and changes it twice (Exodus 20:4 and Deuteronomy 5:8's first row).
   David Troidl described the division in a comment on openscriptures/morphhb#30
   (2017-03-04).

## Part 2: all other such corrections in morphhb

Part 2 ran through three sub-agents of this session, one after another, each writing only its
own scripts (`scripts/p2_text_*`, `scripts/p2_lemma_*`, `scripts/p2_records_*`) and outputs
(`out/40-*` to `out/79-*`) here. Before adopting a figure, Claude reran its pipeline or
checked it independently, as each section says. The judgment of each candidate is Claude's.

### The answer

1. **morphhb has nine corrections in all: Part 1's five and four more**, listed in the table
   below.
   - **Hosea 13:15.** WLC 4.18, 4.20 and 4.22 and UXLC 2.6 spell the word as "son", with no
     yod, under WLC's note U; MAM has "between". morphhb's lemma, 996, is "between": morphhb
     gives it to 167 of the 168 other words with MAM's form (the other is Aramaic, lemma 997),
     and gives 83 of the 84 other words spelled as WLC spells this one lemma 1121 a, "son" (the
     other is a name, lemma 1122). The morph, `HNcmsc`, a noun in the construct, fits "son". Read as a defective spelling of "between", the word would be an
     anomaly instead of a correction.
   - **Genesis 39:19, Deuteronomy 22:29 and Leviticus 4:35** differ only by a mappiq, and in
     each the morph reads MAM's form. At Genesis 39:19 WLC has a mappiq, which makes the verb
     "he did it", and MAM and UXLC 2.6 have none; morphhb's morph has no suffix. At
     Deuteronomy 22:29, where WLC's notes call the form anomalous, and at Leviticus 4:35, WLC has
     no mappiq and MAM has one; morphhb's morph has a third feminine singular suffix.
2. **No other correction of the al/el kind exists.** Of morphhb's 4,930 words whose last
   morpheme has the letters alef and lamed, 17 have a vowel, lemma and morph that disagree: the
   five corrections; three slips of morphhb's own where WLC and MAM agree (at Jeremiah 51:3 two
   words carry each other's lemmas, as they have since the first commit, and at Genesis 37:22
   the negative has lemma 3808, the other negative's); one anomaly at Psalms 35:22; and eight
   defensible analyses (lemma 516 in the title Al-tashheth, four times, and Aramaic 409, four
   times).
3. **The three mappiq cases are not like the four of the review's cases where both forms have
   the suffix** (Genesis 34:11, Isaiah 23:8, Hosea 2:4, Proverbs 31:12, all in class c of Part
   1). There WLC's letters still show the suffix and only a
   vowel is missing, so one analysis fits both forms. Here the mappiq alone marks the suffix, so
   having it or not changes the analysis.
4. **morphhb's text is WLC 4.20's.** Compared atom by atom over all 23,213 verses, every
   difference falls into a systematic class and none is left over. Changes of letters, vowels or
   maqaf are confined to three words of the Decalogues, Daniel 2:39's ketiv and qere and the 12
   words that morphhb divides for exegesis.
5. **morphhb's own records describe none of the nine corrections**: no commit message, header
   revision entry, exegesis note, issue, pull request or comment.

### The nine corrections

| Verse | morphhb id | WLC 4.20 | MAM | morphhb's lemma | morphhb's morph | Reads MAM's form | WLC notes at the chanted word | Lemma's number since | Morph since |
|---|---|---|---|---|---|---|---|---|---|
| Exodus 10:28 | `02ubY` | אֶל־ | אַל־ | 408 | `HTn` | lemma and morph | none | `c299c30a` 2009-12-28 | `f0b4e882` 2018-12-14 |
| Deuteronomy 2:9 | `057a3` | אֶל־ | אַל־ | 408 | `HR` | lemma | U | `c299c30a` 2009-12-28 | `f0b4e882` 2018-12-14 |
| Joshua 22:19 | `06Umo` | אֶל־ | אַל־ | 408 | `HR` | lemma | none | `c299c30a` 2009-12-28 | `f0b4e882` 2018-12-14 |
| Judges 19:23 | `07HwX` | אַל־ | אֶל־ | 413 | `HTn` | lemma | U | `c299c30a` 2009-12-28 | `097d0e42` 2017-12-10 |
| Jeremiah 47:6 | `242CG` | אַל־ | אֶל־ | 413 | `HTn` | lemma | none | `c299c30a` 2009-12-28 | `097d0e42` 2017-12-10 |
| Hosea 13:15 | `28sYk` | בֵּן | בֵּין | 996 | `HNcmsc` | lemma (the letters differ) | U | `c299c30a` 2009-12-28 | `ba378e75` 2018-01-04 |
| Genesis 39:19 | `01oc4` | עָשָׂהּ | עָשָׂה | 6213 a | `HVqp3ms` | morph (no suffix: no mappiq) | 1 | `c299c30a` 2009-12-28 | `097d0e42` 2017-12-10 |
| Deuteronomy 22:29 | `05ENP` | שַׁלְּחָה | שַׁלְּחָהּ | 7971 | `HVpc/Sp3fs` | morph (a suffix: a mappiq) | Q, n, p | `c299c30a` 2009-12-28 | `f0b4e882` 2018-12-14 |
| Leviticus 4:35 | `03caE` | חֶלְבָּה | חֶלְבָּהּ | 2459 | `HNcmsc/Sp3fs` | morph (a suffix: a mappiq) | none | `c299c30a` 2009-12-28 | `f0b4e882` 2018-12-14 |

"Lemma's number since" is the number's: the augment letters and the prefixes came in January
2011 (`b17c7e6e`, `a52c1012`, `fe661292`). At Deuteronomy 22:29 morphhb's own text had the
mappiq until its update to WLC 4.14 (`57206c9b`, 2011-01-22) brought WLC's form; the other
eight texts have been as now since the first commit (`out/21-history.txt`,
`out/71-history.txt`). Written out by `scripts/part2_table.py`; Claude checked the four newer
words in every source with its own script (`out/63-check-new-corrections.txt`).

### Method 3: morphhb's text against WLC 4.18, 4.20 and 4.22

`scripts/p2_text_compare.py` turned every verse of every source into atoms (`/`, sof pasuq
and whitespace dropped, a maqaf kept, paseq as a flag), keyed them with every mark kept and each
letter's marks sorted, aligned them by letters and gave each difference one class by an explicit
test (`out/40-text-compare-summary.txt` defines them all).

1. **Which version.** Once the systematic classes are taken out, nothing is left against WLC
   4.20; 16 units are left against WLC 4.18, and WLC 4.20 has morphhb's reading at all 16; 38
   are left against WLC 4.22, and WLC 4.20 has morphhb's reading at 36 (the other two are
   Leviticus 13:3, equal to WLC 4.20 by the review's key, and Daniel 2:39). The WLC notes
   agree: morphhb's note letters differ from WLC 4.18's in 54 verses, from 4.20's in 13 and from
   4.22's in 199.
2. **The classes, against WLC 4.20, in units:**
   1. a qadma for the first of two pashtas: 3,811 (since `380f4219`, 2014-02-04, "Corrected
      pashta in the middle of a word": exactly so in Deuteronomy, the one book whose saved
      versions include its version just before that commit, and within the saved versions'
      brackets in the seven other books with saved history,
      `out/78-check-zwj-qadma-history.txt`);
   2. the Decalogues' and Genesis 35:22's divided accents: 122 units in 24 verses (since
      `73784451`, 2010-07-13);
   3. encoding only: 82, that is 79 ZERO WIDTH JOINERs before a medial meteg, which WLC 4.18,
      4.20 and 4.22 have and morphhb lacks, with no joiner left anywhere in its files; the saved
      versions date the removal exactly only in Deuteronomy and Hosea, to `56b51322`
      (2013-12-12, "First release of morphology"), and bracket it in Jeremiah, Judges and
      Leviticus; and 3 final letters inside ketivs, where morphhb agrees with WLC 4.18 and
      only MAM-basics' conversion of WLC 4.20 differs;
   4. word division: 12, one for each note "A single word in the text has been divided for
      exegesis";
   5. ketiv and qere: 1, Daniel 2:39, where morphhb has a ketiv and a qere for WLC 4.20's single
      word, as WLC 4.22, UXLC 2.6 and MAM do; it arrived with `019b22f6` (2018-04-15), was
      undone and redone, and has stood since `456c54c6` (2019-01-13);
   6. paseq: 0; residual: 0.
3. **The Decalogues.** At six words WLC 4.20's atom is not the union of morphhb's main text and
   its alternative-accent note (`out/46-text-divided-accents.txt`): at Exodus 20:4 one word
   lost WLC's patah (Part 1's class d) and another its meteg; Exodus 20:5 has a hataf patah for WLC's sheva, as MAM has;
   Deuteronomy 5:7 has a maqaf that WLC lacks, as MAM has; and the alternative notes at
   Exodus 20:8 and Deuteronomy 5:17 have an accent that WLC 4.20's atom lacks. So three of the
   six differ in a vowel or the maqaf, one in a meteg and two in an accent. At Deuteronomy 5:8
   one catchWord does not match the main text it names.
4. **Checks.** A rerun reproduced the summary byte for byte. Independently, outside the 24
   divided verses morphhb has 3,807 fewer pashtas and 3,807 more qadmas than WLC 4.20, with the
   same total of the two, and the units of the qadma class number 3,807 there and 4 inside them
   (`out/48-check-marks.txt`, `out/48-check-qadma-units.txt`). WLC 4.18, 4.20 and 4.22 each
   have 79 zero-width joiners and morphhb none. A later check over whole files
   (`out/78-check-zwj-qadma-history.txt`) finds no ZERO WIDTH JOINER, COMBINING GRAPHEME JOINER
   or ZERO WIDTH NON-JOINER in any of morphhb's files at `d4265dfa`, notes and headers
   included. Against each book's complete commit listing, Deuteronomy's and Hosea's saved
   versions have their joiners up to `1dee0226` (2013-09-17) and none from the next commit to
   touch them, `56b51322`, on; Jeremiah's and Judges' lose theirs between saved versions whose unsaved
   commits include `56b51322`, and Leviticus's between 2009 and 2016. No commit message, issue
   or comment mentions the joiners of `wlc/` (`out/78-check-topic-mentions.txt`).

### Methods 2 and 1: the lemma and the morph against the text

`scripts/p2_lemma_run_all.py` runs the three tests (`out/61-summary.txt` first). A full rerun
reproduced all 16 of its outputs byte for byte (`out/62-*`).

1. **The al/el census** (`out/50-alel-census.txt`): the 4,930 words and 17 mismatches above.
   Only six alef-lamed words have another vowel under the alef in MAM: the five corrections and
   Psalms 35:22.
2. **The general test** (`out/51-general-test.txt`). morphhb's atoms and MAM's were aligned by
   letters, ketiv side with ketiv side and qere side with qere side, giving 7,757 one-to-one
   pairs whose letters agree and whose forms differ by the review's key; 6,466 of them differ
   only by a holam in MAM's form, 6,459 of those in the Tetragrammaton. A word is flagged when
   its lemma, morph or both are common among MAM's form's occurrences elsewhere (at least 50%)
   and rare among its own form's (at most 10% of at least 5 other occurrences). Of the 6,892
   pairs testable so, 8 are flagged: the five corrections, Daniel 3:15 (an anomaly) and two
   that are noise (Exodus 12:27, 1 Chronicles 29:16); a looser grid of thresholds flags nothing
   more (`out/59-threshold-sensitivity.txt`). The test flags all five corrections and not
   Judges 19:4. Of the 865 pairs whose own form is rarer, a back-off test flags 54, among which
   Genesis 39:19 is the one correction. Of the 1,017 pairs whose letters differ, 27 are flagged,
   among which Hosea 13:15 is the one correction. Claude's reading of 13 unflagged pairs found
   Deuteronomy 22:29 and Leviticus 4:35.
3. **WLC's notes** (`out/60-wlc-notes.txt`): 1,072 notes on 800 chanted words. Of note U's 79
   chanted words, 59 differ from MAM by the review's key, and the general test flags 3:
   Deuteronomy 2:9, Judges 19:23 and Hosea 13:15. Under the other letters it flags only
   Daniel 3:15, under note 1.

### Method 4: morphhb's own records

1. **Commit messages** (`out/73-*`): of the commits whose messages name a correction without
   saying what, only two change the text, and both bring it to WLC: `6887dd0a` (2016-03-08,
   "Textual corrections.") removed a letter that morphhb's own text had added at Job 19:2 and
   at Proverbs 1:28, and `c8f43473` (2017-02-11, "Textual corrections from tanach.us.") changed
   a vowel at 2 Kings 21:26 and an accent at Genesis 5:29 and Zephaniah 2:15 from WLC 4.18's
   readings to 4.20's (checked from the saved commit patches, `out/76-check-commit-patches.txt`).
   The others change lemmas, morphs, the `n` attribute or markup, and none touches the nine
   words.
2. **The files' headers**: 273 `revisionDesc` entries, 12 distinct (the 2008 conversion, the
   WLC 4.14 to 4.20 updates, the morphology releases), none naming a correction
   (`out/74-*`).
3. **Exegesis notes**: of 21, 12 mark the word divisions above, and the other 9 say "WLC has
   this word divided as" and give WLC's form, Daniel 2:39's among them
   (`out/74-exegesis-notes.txt`; Daniel 2:39's history, from the saved versions:
   `out/77-check-dan239.txt`).
4. **Issues and pull requests** (`out/75-*`): none mentions any of the nine verses, Jeremiah
   51:3 or Daniel 2:39. In openscriptures/morphhb#27, David Troidl wrote on 2017-02-03 that
   "the OSHB should respect the WLC, because that is our source". openscriptures/morphhb#113,
   open, reports swapped lemmas at 1 Chronicles 12:39 and 2 Chronicles 3:17; Jeremiah 51:3's
   pair is not reported anywhere.

### What these methods cannot find

1. A correction where WLC and MAM agree, or where the lemma and morph are the same for both
   forms.
2. A correction carried by marks that the review's key strips, such as accents.
3. A correction at a word whose own form is too rare for the general test, beyond what the
   back-off test and Claude's reading of 13 pairs caught, and at the 49 pairs whose MAM form
   never occurs in morphhb.
4. A letter difference outside a one-to-one block of the alignment.
5. A ketiv analysed by its qere: at Isaiah 52:5 the ketiv carries the qere's lemma, while 205
   other ketivs carry their own (`out/58-ketiv-qere-analyses.txt`).
6. Anything about the Leningrad Codex itself: no image was consulted.

## Files in this folder

- `scripts/`: every script used, each with its usage in its docstring. Each script that reads
  fetched files ran as `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -I`.
  `gh_fetch.py` is the MACULA session's; `fetch_morphhb_wlc.py`, `fetch_listing_pages.py`,
  `attr_history.py` and `probe_versions.py` made this session's requests, one at a time.
- `fetched/`: each fetched file in its own folder, unchanged: `morphhb-wlc-<book>/` (the 39
  books and `VerseMap.xml` at `d4265dfa`, each checked against the listing's Git blob hash),
  `morphhb-wlc-listing/`, `morphhb-commits-p*/` (all 325 commits), `hist-<book>-*` (older
  versions and the path-filtered commit listings), `morphhb-issues-p*/`,
  `morphhb-issue-comments-p*/` and `morphhb-pr-review-comments-p*/`.
- `out/fetch_log.jsonl`: one line per request, with byte count, SHA-256 and Git blob SHA-1.
- `out/00-fetch-morphhb-wlc.txt`, `out/03-fetch-commit-pages.txt`: the fetch runs.
- `out/01-wlc418-tag-census.txt`, `out/02-morphhb-census.txt`: the element censuses that fix
  the readers' closed dispatch.
- `out/04-commit-list.txt`, `out/04-commits.json`: morphhb's commits, oldest first.
- `out/10-part1-cases.txt`, `out/10-part1-cases.json`: every case in every source.
- `out/11-part1-hataf-ng.txt`, `out/11-part1-hataf-ng.json`: the footnote's six verses.
- `out/12-part1-table.md`, `out/12-part1-table.json`: the table above, with the classes.
- `out/13-verses.txt`: whole verses in WLC 4.18, UXLC 2.6, WLC 4.20, WLC 4.22 and morphhb.
- `out/20-history-spec.json`, `out/21-history.txt`, `out/21-history.json`,
  `out/22-probes.txt`: the history searches.
- `out/30-issues-list.txt`, `out/31-issues-hits.txt`: morphhb's issues and the searches.
- Part 2, method 3: `out/40-text-compare-summary.txt` (start here), `out/40-text-compare-data.json`,
  `out/41-text-residuals.*`, `out/42-text-units.json`, `out/43-text-class-lists.txt`,
  `out/44-text-notes.txt`, `out/45-text-version-evidence.txt`,
  `out/46-text-divided-accents.txt`, `out/47-text-explore-census.txt`; Claude's checks
  `out/48-check-marks.txt` and `out/48-check-qadma-units.txt`.
- Part 2, methods 2 and 1: `out/61-summary.txt` (start here), `out/50-*` to `out/60-*`; the
  rerun's log and hashes `out/62-*`; Claude's check `out/63-check-new-corrections.txt`.
- Part 2, method 4: `out/70-*` to `out/75-*`, every command in `out/79-commands.txt`; the
  fetched versions `fetched/hist-*` and commits `fetched/rec-*`; Claude's check
  `out/76-check-commit-patches.txt`.
- Claude's later checks, made while writing the follow-up briefs:
  `out/78-check-zwj-qadma-history.txt` (`scripts/check_zwj_qadma_history.py`: the joiner,
  qadma and pashta counts in every file at `d4265dfa` and in every saved version, against each
  book's complete commit listing) and `out/78-check-topic-mentions.txt`
  (`scripts/check_topic_mentions.py`: where morphhb's commit messages, issues and comments
  mention the joiners, the pashta and the Decalogues).
- `out/80-part2-corrections-table.md`: the nine corrections' table above.
