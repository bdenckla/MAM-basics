# Part 2, slice p2e: the atom-level rows that no slice had judged

Written by Claude (Opus 5.5) on 2026-11-13, New York time, as a sub-agent of the session that wrote this folder's `README.md`, by `scripts/p2e_review.py` from `out/p2e-candidates.json` (`scripts/p2e_select.py`) and the checks in `out/p2e-checks.txt` (`scripts/p2e_checks.py`) and `out/p2e-texts.txt` (`scripts/show_texts.py`). Not reviewed by a human. Nothing tracked changed. Every form here is a transcription's, the BHSA 2021's (`g_word_utf8`), MAM's (MAM-simple, as the scan read it), WLC 4.18's, WLC 4.20's or UXLC 2.6's, emitted by script and stripped of accents as the review's page strips its forms; nothing here says what the Leningrad Codex has.

## The answer

| Category | Test A groups | Test A atoms | Test B atoms | All rows |
|---|---|---|---|---|
| another-word | 3 | 4 | 0 | 3 |
| follows-pointing | 0 | 0 | 2 | 2 |
| no-word | 0 | 0 | 44 | 44 |
| variant | 0 | 0 | 55 | 55 |
| homograph | 51 | 65 | 1 | 52 |
| artifact | 0 | 0 | 0 | 0 |
| unsure | 0 | 0 | 0 | 0 |
| all | 54 | 69 | 102 | 156 |

1. **Test B over atoms adds no correction toward MAM.** None of its 102 unjudged atoms is another-word; 2 follow the BHSA's pointing where MAM's would give another analysis: Isaiah 66:22 (the review's class a case); 2 Chronicles 15:16 (new: the preposition's pataḥ, analysed without the article, where MAM's qamats is the article's). The rest are pointings that spell no well-formed word (44) or variant spellings of the analysed word (55), and one homograph of person and gender (Isaiah 31:8).
2. **Of Test A's 54 new groups, 3 are another-word, all already raised by out/p2d-review.md for Ben's judgment:** A34 (Numbers 11:15; Ezekiel 28:14, the feminine pronoun's pointing analysed as the masculine); A40 (Deuteronomy 5:27, the feminine pronoun's pointing analysed as the masculine); A43 (Deuteronomy 25:7, letters with a yod, which spell 'from nothing', analysed as 'refuses'). The other 51 groups are homographs that context decides: 15 a name against a common noun; 10 two of the ETCBC's lexemes of one spelling (numbered homonyms or a split lexeme); 24 two forms or parts of speech spelled alike; 2 with or without the article.
3. **No row is artifact or unsure.** The four slot-level mam-elsewhere artifacts (Genesis 15:10, Exodus 2:10, 2 Samuel 3:32, Job 8:1) fall in this slice by its rule, since none of their slots is in p2b's or p2c's JSON; over atoms each is a missing dagesh forte, judged no-word as p2b and p2c judge the same lack.

## The another-word rows and their evidence

### A34: Numbers 11:15; Ezekiel 28:14

- The BHSA's analysis: `>TH p2.sg.m +n/a`; its slots: `>TH` prps 'you'.
- The other analyses of its pointing in the BHSA (Test A's key): `>T= p2.sg.f +n/a` x32, as at Genesis 24:23.
- The BHSA's slots of `>TH`, by pointing: אַתָּה x685, as at Genesis 3:14; אָתָּה x54, as at Genesis 3:11; את (ketiv; qere אַתָּה) x5, as at 1 Samuel 24:19; אַתְּ x3, as at Numbers 11:15.
- The BHSA's slots of `>T=`, by pointing: אַתְּ x44, as at Genesis 24:23; אתי (ketiv; qere אַתְּ) x6, as at Judges 17:2; אָתְּ x5, as at Genesis 12:11; אתי (ketiv; qere אָתְּ) x1, as at Ezekiel 36:13; אָתּ x1, as at Ruth 3:9.
- Why: The pointing is the feminine pronoun 'you' (`>T=`), which the BHSA gives the other 32 atoms of this pointing; the analysis is the masculine `>TH`, by context: Moses addresses God (Numbers 11:15), God the prince of Tyre (Ezekiel 28:14). The BHSA has no qere at either place; where it has the ketiv's two letters with the masculine's qere, at 5 places, it analyses the masculine too (out/p2e-checks.txt, part 5). A correction of gender by context.

| Text | Numbers 11:15 | Ezekiel 28:14 |
|---|---|---|
| WLC 4.18 | אַתְּ־ | אַתְּ־ |
| WLC 4.20 | אַתְּ־ | אַתְּ־ |
| UXLC 2.6 | אַתְּ־ | אַתְּ־ |
| MAM | אַתְּ־ | אַתְּ־ |
| BHSA | אַתְּ־ | אַתְּ־ |

### A40: Deuteronomy 5:27

- The BHSA's analysis: `W + >TH p2.sg.m +n/a`; its slots: `W` conj 'and'; `>TH` prps 'you'.
- The other analyses of its pointing in the BHSA (Test A's key): `W + >T= p2.sg.f +n/a` x12, as at Numbers 5:20.
- The BHSA's slots of `>TH`, by pointing: אַתָּה x685, as at Genesis 3:14; אָתָּה x54, as at Genesis 3:11; את (ketiv; qere אַתָּה) x5, as at 1 Samuel 24:19; אַתְּ x3, as at Numbers 11:15.
- The BHSA's slots of `>T=`, by pointing: אַתְּ x44, as at Genesis 24:23; אתי (ketiv; qere אַתְּ) x6, as at Judges 17:2; אָתְּ x5, as at Genesis 12:11; אתי (ketiv; qere אָתְּ) x1, as at Ezekiel 36:13; אָתּ x1, as at Ruth 3:9.
- Why: As at A34, with the conjunction: the pointing is the feminine pronoun, which the BHSA gives the other 12 atoms of this pointing (`W + >T=`); the analysis is the masculine, the people addressing Moses.

| Text | Deuteronomy 5:27 |
|---|---|
| WLC 4.18 | וְאַתְּ |
| WLC 4.20 | וְאַתְּ |
| UXLC 2.6 | וְאַתְּ |
| MAM | וְאַתְּ |
| BHSA | וְאַתְּ |

### A43: Deuteronomy 25:7

- The BHSA's analysis: `M>N[ piel perf p3.sg.m`; its slots: `M>N[` verb 'refuse'.
- The other analyses of its pointing in the BHSA (Test A's key): `MN + >JN/ -.sg.m` x26, as at Isaiah 5:9.
- The BHSA's slots of `M>N[` (vs piel, vt perf, ps p3, nu sg, gn m), by pointing: מֵאֵן x4, as at Exodus 7:14; מֵאֵין x1, as at Deuteronomy 25:7.
- The BHSA's slots of `M>N[`, by pointing: יְמָאֵן x10, as at Genesis 37:35; מֵאֲנוּ x10, as at Jeremiah 5:3; מָאֵן x5, as at Exodus 7:27; מֵאֵן x4, as at Exodus 7:14; יְמָאֲנוּ x4, as at 1 Samuel 8:19; מֵאֲנָה x4, as at Jeremiah 15:18; תְּמָאֵן x2, as at Exodus 4:23; מֵאַנְתָּ x1, as at Exodus 10:3; מֵאַנְתֶּם x1, as at Exodus 16:28; מֵאֵין x1, as at Deuteronomy 25:7; תְּמָאֲנוּ x1, as at Isaiah 1:20; מֵאַנְתְּ x1, as at Jeremiah 3:3; מֵּאֲנִים x1, as at Jeremiah 13:10; תְּמָאֵנוּ x1, as at Proverbs 1:24.
- Why: The BHSA's letters have a yod after the second tsere, which MAM's lack. So pointed, the atom is 'from' and 'nothing' (`MN + >JN/`), the BHSA's analysis of the other 26 atoms of this pointing; the analysis is the one word that MAM's letters spell, the piel perfect 'refuses' (`M>N[`), which the BHSA has without the yod at 4 other words (out/p2e-checks.txt, part 4): it takes the yod for a vowel letter. WLC 4.18, WLC 4.20 and UXLC 2.6 have the yod. Test B skips the atom, its letters differing from MAM's.

| Text | Deuteronomy 25:7 |
|---|---|
| WLC 4.18 | מֵאֵין |
| WLC 4.20 | מֵאֵין |
| UXLC 2.6 | מֵאֵין |
| MAM | מֵאֵן |
| BHSA | מֵאֵין |

## The categories

- **another-word**: the BHSA's pointing is a well-formed spelling of another word, or of another person, number, gender or suffix, attested in the BHSA, and the analysis takes it as a different one. A correction candidate.
- **follows-pointing**: the analysis is what the BHSA's pointing spells, while MAM's pointing would give another (Part 1's class a).
- **no-word**: the pointing breaks a rule that the analysed word needs and spells no other word; the analysis reads through it. Here: a dagesh forte missing from a letter with a full vowel; a missing mappiq, furtive pataḥ or final kaf's sheva; a missing vowel; a conjunction's or preposition's vowel that no rule gives; two vowels for one syllable; a ḥataf before a doubled letter (as p2c judges it; p2b calls it a variant); an atom-initial dagesh after a disjunctive accent.
- **variant**: a recognized spelling of the same word, MAM's and the BHSA's alike: a ḥataf for a vocal sheva or a sheva for a ḥataf; a full vowel for a ḥataf under a guttural; a dagesh forte that a letter with sheva has or lacks; an atom-initial dagesh lene or conjunctive dagesh that depends on the atom before (after a conjunctive accent or maqaf); a usual vowel before a guttural or resh where MAM has another; a compound name divided; Jerusalem without its orphaned ḥiriq; a pausal vowel.
- **homograph**: the same pointing is a normal spelling of both analyses, and context decides; its kinds: **name**, a name against a common noun; **lexeme**, two of the ETCBC's lexemes of one spelling (numbered homonyms or a split lexeme); **form**, two forms or parts of speech spelled alike; **article**, with or without the article.
- **artifact** of the test's method, and **unsure**: no row.

Both no-word and variant say that the analysis reads the same word as MAM's pointing; they differ only in whether the BHSA's pointing is well formed, and p2b and p2c drew that line slightly differently (a ḥataf before a doubled letter). Neither is a correction.

## Which rows

1. **Test A over atoms (`out/p2d-test-a.txt`, `out/p2d-scan.json`), the groups marked new**, of the kinds lexeme, stem/tense and segmentation: 54 groups, 69 atoms (lexeme 44, stem/tense 7, segmentation 3). p2d reviewed the 21 new ps/nu/gn/prs groups.
2. **Test B over atoms, classes mam-unique and neither, with no slot among the rows of `out/p2b-mam-unique.json` or `out/p2c-neither.json`**: 102 atoms. By the slot-level class of their slots: mam-unique from both 46; mam-unique from mam-elsewhere 4; mam-unique from no slot-level row 2; neither from both 33; neither from written 17. MAM's whole atom occurs nowhere in the BHSA at 48 of the 50 neither atoms.

`scripts/p2e_select.py` recomputes the atoms as `scripts/p2d_scan_atoms.py` makes them and checks every row against `out/p2d-scan.json`; `out/p2e-candidates.txt` has each row's slots, features, context, per-letter difference from MAM's atom, WLC 4.18's atom and the BHSA's other atoms of the same pointing and of the same letters and analysis.

## Where the BHSA's atom differs from WLC 4.18's

At 10 of these 171 atoms the BHSA's atom differs in pointing from WLC 4.18's aligned atom (by `bkey`, accents aside); at the 2 compound names WLC 4.18 has two atoms where the BHSA has one, which is not counted. A difference with no WLC note may be the BHSA's transcription of BHS; BHS itself was not read.

| # | Reference | BHSA | WLC 4.18 | WLC 4.18's notes |
|---|---|---|---|---|
| B114192 | 2 Samuel 3:27 | לְדַּבֵּר | לְדַבֵּר | - |
| B119742 | 2 Samuel 16:19 | לִפָנֶיךָ | לְפָנֶיךָ | - |
| B185728 | Jeremiah 49:37 | לפְנֵי | לִפְנֵי | - |
| B191270 | Ezekiel 12:10 | בִּירוּשָׁלַם | בִּירוּשָׁלִַם | v |
| B193102 | Ezekiel 16:54 | וִנִכְלַמְתְּ | וְנִכְלַמְתְּ | v |
| B121506 | 2 Samuel 19:33 | בְשִׁיבָתֹו | בְּשִׁיבָתוֹ | - |
| B199639 | Ezekiel 32:30 | מִגְּבוּרָתָם | מִגְבוּרָתָם | - |
| B223241 | Psalms 21:14 | בְעֻזֶּךָ | בְּעֻזֶּךָ | - |
| B247316 | Job 36:3 | וְלְפֹעֲלִי | וּלְפֹעֲלִי | - |
| B256127 | Ruth 2:2 | וַאֲלַקֳטָה | וַאֲלַקֳטָּה | Q, n, p |

## The rows: Test A's new groups

A slot is `lex [vs vt] [ps.nu.gn] [+prs]`, with `-` for NA and `?` for unknown; slots are joined by ` + `.

| # | Kind | Reference | BHSA | MAM | BHSA's analysis | The pointing's other analyses | Category | Reason |
|---|---|---|---|---|---|---|---|---|
| A5 | lexeme | Genesis 7:13 | וְשֵׁם־ | וְשֵׁם־ | `W + CM=/ -.sg.m +n/a` | `W + CM/ -.sg.m` x89 | **homograph** (name) | The name Shem (`CM=/`) and the noun 'name' (`CM/`, 89 atoms with the conjunction) are pointed alike; the verse lists Noah's sons. |
| A6 | lexeme | Genesis 14:18 | שָׁלֵם | שָׁלֵם | `CLM===/ -.sg.? +n/a` | `CLM=/ -.sg.m` x17 | **homograph** (name) | The place name Salem and the adjective 'complete' (`CLM=/`, 17 atoms) are pointed alike; here 'king of Salem'. |
| A10 | lexeme | Genesis 25:7 | חָי | חָי | `XJH[ qal perf p3.sg.m` | `XJ/ -.sg.m` x21 | **homograph** (form) | The short qal perfect of `XJH[` 'be alive' and the adjective 'alive' (`XJ/`, 21 atoms) are pointed alike; here 'which he lived', of Abraham's years. |
| A11 | stem/tense | Genesis 26:28 | וְנִכְרְתָה | וְנִכְרְתָה | `W + KRT[ qal impf p1.pl.?` | `W + KRT[ nif perf p3.sg.f` x17 | **homograph** (form) | The niphal perfect third feminine singular and the qal cohortative first plural of `KRT[` are pointed alike; here 'let us make a covenant'. |
| A18 | lexeme | Genesis 49:27; Isaiah 33:23 | עַד / עַד־ | עַד / עַד־ | `<D==/ -.sg.m` | `<D` x1015; `<D/ -.sg.m` x10 | **homograph** (lexeme) | The ETCBC's `<D==/` 'prey' and the preposition 'until' (`<D`) are pointed alike; here 'devours prey' and 'prey of great spoil'. |
| A25 | lexeme | Exodus 16:1 | אֵילִם | אֵילִם | `>JLM=/ -.sg.? +n/a` | `>JL=/ -.pl.m` x25 | **homograph** (name) | The place name Elim and the plural of 'ram' spelled without the yod of its ending (`>JL=/`, 25 atoms) are pointed alike; here 'between Elim and Sinai'. |
| A26 | lexeme | Exodus 21:8 | רָעָה | רָעָה | `R<<[ qal perf p3.sg.f` | `R<H/ -.sg.f` x103; `R</ -.sg.f` x24 | **homograph** (form) | The qal perfect third feminine singular of `R<<[` 'be evil' and the noun 'evil' (`R<H/`) or the adjective (`R</`) are pointed alike, accents aside; here 'if she displeases her master'. |
| A28 | lexeme | Leviticus 13:45; Isaiah 52:1 | וְטָמֵא | וְטָמֵא | `W + VM>/ -.sg.m` | `W + VM>[ qal perf p3.sg.m` x22 | **homograph** (form) | The adjective 'unclean' (`VM>/`) and the stative verb's perfect (`VM>[`, 22 atoms with the conjunction) are pointed alike; here the cry 'unclean' and 'the uncircumcised and the unclean'. |
| A31 | lexeme | Numbers 6:12 | טָמֵא | טָמֵא | `VM>[ qal perf p3.sg.m` | `VM>/ -.sg.m` x41 | **homograph** (form) | As at A28, the other way: here the verb, 'because his consecration was defiled'. |
| A34 | lexeme | Numbers 11:15; Ezekiel 28:14 | אַתְּ־ | אַתְּ־ | `>TH p2.sg.m +n/a` | `>T= p2.sg.f +n/a` x32 | **another-word** | The pointing is the feminine pronoun 'you' (`>T=`), which the BHSA gives the other 32 atoms of this pointing; the analysis is the masculine `>TH`, by context: Moses addresses God (Numbers 11:15), God the prince of Tyre (Ezekiel 28:14). The BHSA has no qere at either place; where it has the ketiv's two letters with the masculine's qere, at 5 places, it analyses the masculine too (out/p2e-checks.txt, part 5). A correction of gender by context. |
| A35 | lexeme | Numbers 11:33; Psalms 78:31 | וְאַף | וְאַף | `W + >P/ -.sg.m` | `W + >P` x23 | **homograph** (form) | The noun 'nose, anger' (`>P/`, construct) and the particle 'also' (`>P`, 23 atoms with the conjunction) are pointed alike; here 'the anger of the LORD' and 'the anger of God'. |
| A36 | stem/tense | Numbers 14:4 | נִתְּנָה | נִתְּנָה | `NTN[ qal impf p1.pl.?` | `NTN[ nif perf p3.sg.f` x17 | **homograph** (form) | As at A11, for `NTN[`: here 'let us appoint a head'. |
| A38 | lexeme | Numbers 23:19 | הַהוּא | הַהוּא | `H= + HW> p3.sg.m +n/a` | `H + HW> p3.sg.m +n/a` x312 | **homograph** (form) | Before a he, the interrogative he and the article both have pataḥ; here the question 'has he said, and will he not do it?'. |
| A40 | lexeme | Deuteronomy 5:27 | וְאַתְּ | וְאַתְּ | `W + >TH p2.sg.m +n/a` | `W + >T= p2.sg.f +n/a` x12 | **another-word** | As at A34, with the conjunction: the pointing is the feminine pronoun, which the BHSA gives the other 12 atoms of this pointing (`W + >T=`); the analysis is the masculine, the people addressing Moses. |
| A41 | stem/tense | Deuteronomy 8:11 | שְׁמֹר | שְׁמֹר | `CMR[ qal infc ?.?.?` | `CMR[ qal impv p2.sg.m` x11 | **homograph** (form) | The qal infinitive construct and the imperative of `CMR[` (11 atoms) are pointed alike; here after 'so as not to'. |
| A43 | segmentation | Deuteronomy 25:7 | מֵאֵין | (not aligned) | `M>N[ piel perf p3.sg.m` | `MN + >JN/ -.sg.m` x26 | **another-word** | The BHSA's letters have a yod after the second tsere, which MAM's lack. So pointed, the atom is 'from' and 'nothing' (`MN + >JN/`), the BHSA's analysis of the other 26 atoms of this pointing; the analysis is the one word that MAM's letters spell, the piel perfect 'refuses' (`M>N[`), which the BHSA has without the yod at 4 other words (out/p2e-checks.txt, part 4): it takes the yod for a vowel letter. WLC 4.18, WLC 4.20 and UXLC 2.6 have the yod. Test B skips the atom, its letters differing from MAM's. |
| A44 | lexeme | Deuteronomy 30:3; Zephaniah 2:7 | וְשָׁב | וְשָׁב | `W + CWB=[ qal perf p3.sg.m` | `W + CWB[ qal perf p3.sg.m` x29 | **homograph** (lexeme) | The ETCBC's second lexeme `CWB=[` (its gloss 'gather'), used with 'fortunes', and `CWB[` 'return' (29 atoms with the conjunction) are pointed alike. |
| A54 | lexeme | Judges 21:19; Ecclesiastes 3:21 | הָעֹלָה | הָעֹלָה | `H + <LH[ qal ptca ?.sg.f` | `H + <LH/ -.sg.f` x61 | **homograph** (form) | The feminine participle 'going up' (`<LH[`) and the noun 'burnt offering' (`<LH/`, 61 atoms), each with the article, are pointed alike; here 'the highway that goes up' and the spirit 'that goes upward'. |
| A58 | stem/tense | 1 Samuel 9:24; Obadiah 1:4 | שִׂים־ / שִׂים | שִׂים־ / שִׂים | `FJM[ qal ptcp ?.sg.m` | `FJM[ qal impv p2.sg.m` x23; `FJM[ qal infc ?.?.?` x1 | **homograph** (form) | The qal passive participle of `FJM[` 'put', its imperative (23 atoms) and its infinitive are pointed alike; the BHSA reads 'set' at both verses: what is left, 'set before you', and a nest 'set among the stars'. |
| A73 | lexeme | 1 Kings 6:24 | קְצֹות | קְצוֹת | `QYWT/ -.pl.f` | `QYH/ -.pl.f` x14; `QYH[ qal infc ?.?.?` x1 | **homograph** (lexeme) | The ETCBC's lexemes `QYH/` (14 atoms) and `QYWT/`, both glossed 'end', have this plural construct alike; which of the two an atom gets is the ETCBC's lexicography, not its pointing. |
| A76 | lexeme | 1 Kings 7:46; 2 Chronicles 4:17 | הָאֲדָמָה | הָאֲדָמָה | `H + >DMH==/ -.sg.? +n/a` | `H + >DMH/ -.sg.f` x111 | **homograph** (name) | The place name Adamah and the noun 'ground' (`>DMH/`, 111 atoms with the article) are pointed alike; the BHSA takes the place name at both verses, 'the ford of Adamah', where they are also read 'the clay ground'. |
| A78 | stem/tense | 1 Kings 18:29 | לַעֲלֹות | לַעֲלוֹת | `L + <LH[ hif infc ?.?.?` | `L + <LH[ qal infc ?.?.?` x18 | **homograph** (form) | After a preposition the hiphil infinitive can lack its he, and then it is pointed as the qal infinitive is (18 atoms); the BHSA reads 'until the offering up of the oblation'. |
| A82 | lexeme | 2 Kings 14:7 | הַסֶּלַע | הַסֶּלַע | `H + SL<=/ -.sg.? +n/a` | `H + SL</ -.sg.m` x11 | **homograph** (name) | The place name Sela and the noun 'rock' (`SL</`, 11 atoms with the article) are pointed alike; here 'he took Sela'. |
| A85 | lexeme | Isaiah 3:6 | לְכָה | לְכָה | `L +K` | `HLK[ qal impv p2.sg.m` x26 | **homograph** (form) | The long form of 'to you' and the imperative 'go' (`HLK[`, 26 atoms) are pointed alike; here 'you have a cloak'. |
| A87 | lexeme | Isaiah 10:8 | שָׂרַי | שָׂרַי | `FR/ -.pl.m +J` | `FRJ/ -.sg.f +n/a` x13 | **homograph** (name) | 'My princes' (`FR/` with suffix `J`) and the name Sarai (`FRJ/`, 13 atoms) are pointed alike; here 'are not my princes all kings?'. |
| A99 | lexeme | Isaiah 45:9; Jeremiah 51:36 | רָב | רָב | `RJB[ qal ptca ?.sg.m` | `RB/ -.sg.m` x47; `RJB[ qal perf p3.sg.m` x3; `RB=/ -.sg.m` x3 | **homograph** (form) | The participle of `RJB[` 'contend' and the adjective 'much' (`RB/`, 47 atoms) are pointed alike; here 'him who strives with his maker' and 'I am pleading your cause'. |
| A104 | lexeme | Isaiah 57:10; Psalms 74:19 | חַיַּת | חַיַּת | `XJH==/ -.sg.f` | `XJH/ -.sg.f` x31 | **homograph** (lexeme) | The ETCBC's homonyms `XJH/` 'animal' (31 atoms) and `XJH==/` 'life' are pointed alike. |
| A108 | lexeme | Jeremiah 9:5 | דַעַת־ | דַעַת־ | `JD<[ qal infc ?.?.?` | `D<T/ -.sg.f` x11 | **homograph** (form) | The qal infinitive of `JD<[` 'know' and the noun 'knowledge' (`D<T/`, 11 atoms) are pointed alike; here with an object, 'they refuse to know me'. |
| A120 | lexeme | Jeremiah 50:27; Ezekiel 21:34 | יֹומָם | יוֹמָם | `JWM/ -.sg.m +M` | `JWMM` x47 | **homograph** (form) | 'Their day' (`JWM/` with suffix `M`) and the adverb 'by day' (`JWMM`, 47 atoms) are pointed alike; here 'their day has come'. |
| A125 | lexeme | Ezekiel 6:13 | אֵלָה | אֵלָה | `>LH/ -.sg.f` | `>LH===/ -.sg.m +n/a` x12 | **homograph** (name) | The noun 'big tree' (`>LH/`) and the name Elah (`>LH===/`, 12 atoms) are pointed alike; here 'under every leafy terebinth'. |
| A126 | lexeme | Ezekiel 17:22 | הָרָמָה | הָרָמָה | `H + RWM[ qal ptca ?.sg.f` | `H + RMH==/ -.sg.? +n/a` x12 | **homograph** (name) | The feminine participle 'lofty' (`RWM[`) and the place name Ramah (`RMH==/`, 12 atoms), each with the article, are pointed alike; here 'the lofty cedar'. |
| A131 | lexeme | Ezekiel 40:5 | קְנֵה | קְנֵה | `QNH/ -.sg.m` | `QNH[ qal impv p2.sg.m` x12 | **homograph** (form) | The construct of 'reed' (`QNH/`) and the imperative 'buy' (`QNH[`, 12 atoms) are pointed alike; here 'a measuring reed'. |
| A132 | lexeme | Ezekiel 40:14 | אֵילִים | אֵילִים | `>JL===/ -.pl.m` | `>JL=/ -.pl.m` x16 | **homograph** (lexeme) | The ETCBC's homonyms `>JL=/` 'ram' (16 atoms) and `>JL===/` 'pillar' are pointed alike; here the gate's pillars. |
| A136 | lexeme | Hosea 11:7 | עַל | עַל | `<L=/ -.sg.m` | `<L` x3476 | **homograph** (form) | The noun 'height' (`<L=/`) and the preposition 'upon' (`<L`, 3476 atoms) are pointed alike; here after a preposition, 'they call him upward'. |
| A140 | lexeme | Joel 1:12 | תָּמָר | תָּמָר | `TMR/ -.sg.m` | `TMR===/ -.sg.f +n/a` x16 | **homograph** (name) | The noun 'date-palm' (`TMR/`) and the name Tamar (`TMR===/`, 16 atoms) are pointed alike; here in a list of trees. |
| A142 | lexeme | Amos 6:12 | לְרֹאשׁ | לְרֹאשׁ | `L + R>C=/ -.sg.m` | `L + R>C/ -.sg.m` x23 | **homograph** (lexeme) | The ETCBC's homonyms `R>C/` 'head' (23 atoms with the preposition) and `R>C=/` 'poison' are pointed alike; here 'you have turned justice into poison'. |
| A145 | stem/tense | Micah 7:18; Psalms 5:5 | חָפֵץ | חָפֵץ / חָפֵץ־ | `XPY[ qal ptca ?.sg.m` | `XPY[ qal perf p3.sg.m` x28; `XPY=/ -.sg.m` x1 | **homograph** (form) | The stative verb's perfect (28 atoms) and its participle (`XPY[`) are pointed alike; here 'he delights in mercy' and 'a God who delights in wickedness'. |
| A149 | stem/tense | Zephaniah 3:8 | קוּמִי | קוּמִי | `QWM[ qal infc ?.?.? +J` | `QWM[ qal impv p2.sg.f` x14 | **homograph** (form) | The infinitive with suffix `J` and the feminine imperative of `QWM[` (14 atoms) are pointed alike; here 'the day of my rising'. |
| A156 | lexeme | Psalms 25:21 | תֹּם־ | תֹּם־ | `TM=/ -.sg.m` | `TMM[ qal infc ?.?.?` x11 | **homograph** (form) | The noun 'integrity' (`TM=/`) and the qal infinitive of `TMM[` (11 atoms) are pointed alike; here 'integrity and uprightness'. |
| A157 | lexeme | Psalms 28:8; Psalms 29:11 | עֹז־ / עֹז | עֹז־ / עֹז | `<Z=/ -.sg.m` | `<Z/ -.sg.m` x32 | **homograph** (lexeme) | The ETCBC's homonyms `<Z/` 'power' (32 atoms) and `<Z=/` 'protection' are pointed alike. |
| A174 | lexeme | Job 42:10 | שָׁב | שָׁב | `CWB=[ qal perf p3.sg.m` | `CWB[ qal perf p3.sg.m` x33; `CWB[ qal ptca ?.sg.m` x3; `CWB=[ qal ptca ?.sg.m` x1 | **homograph** (lexeme) | As at A44: `CWB=[` with 'fortunes', pointed as `CWB[` 'return' is (33 atoms). |
| A177 | lexeme | Proverbs 8:30 | אָמֹון | אָמוֹן | `>MWN=/ -.sg.m` | `>MWN==/ -.sg.m +n/a` x16; `>MWN===/ -.sg.m +n/a` x1 | **homograph** (name) | The noun 'fondling' (`>MWN=/`) and the name Amon (`>MWN==/`, 16 atoms) are pointed alike; here Wisdom 'beside him'. |
| A179 | lexeme | Proverbs 14:4 | אֲלָפִים | אֲלָפִים | `>LP/ -.pl.m` | `>LP=/ -.pl.m` x119 | **homograph** (lexeme) | The ETCBC's homonyms `>LP=/` 'thousand' (119 atoms) and `>LP/` 'cattle' are pointed alike; here 'where there are no oxen'. |
| A184 | lexeme | Ruth 1:21 | מְלֵאָה | מְלֵאָה | `ML>/ -.sg.f` | `ML>[ qal ptca ?.sg.f` x18 | **homograph** (form) | The adjective 'full' (`ML>/`) and the participle of `ML>[` (18 atoms) are pointed alike; here 'I went away full'. |
| A185 | lexeme | Song of Songs 5:15; Esther 1:6 | שֵׁשׁ | שֵׁשׁ | `CC==/ -.sg.m` | `CC/ -.sg.?` x83; `CC=/ -.sg.m` x16 | **homograph** (lexeme) | The ETCBC's homonyms `CC/` 'six' (83 atoms), `CC=/` 'linen' (16) and `CC==/` 'alabaster' are pointed alike; here 'pillars of alabaster'. |
| A187 | lexeme | Ecclesiastes 7:27 | חֶשְׁבֹּון | חֶשְׁבּוֹן | `XCBWN/ -.sg.m` | `XCBWN==/ -.sg.? +n/a` x23 | **homograph** (name) | The noun 'account' (`XCBWN/`) and the place name Heshbon (`XCBWN==/`, 23 atoms) are pointed alike; here 'to find the account'. |
| A189 | lexeme | Esther 1:6 | חוּר | חוּר | `XWR/ -.sg.m` | `XWR=/ -.sg.m +n/a` x11 | **homograph** (name) | The noun 'linen' (`XWR/`) and the name Hur (`XWR=/`, 11 atoms) are pointed alike; here in a list of fabrics. |
| A192 | segmentation | Ezra 3:10 | בַּחֲצֹצְרֹות | בַּחֲצֹצְרוֹת | `B + H + XYYRH/ -.pl.f` | `B + XYYRH/ -.pl.f` x13 | **homograph** (article) | Before a ḥataf pataḥ the preposition has pataḥ with or without the article, so the pointing spells 'with trumpets', the analysis of the other 13 atoms of this pointing, and 'with the trumpets', this analysis, alike. |
| A197 | lexeme | Nehemiah 8:7 | יָמִין | יָמִין | `JMJN=/ -.sg.m +n/a` | `JMJN/ -.sg.f` x21 | **homograph** (name) | The name Jamin and the noun 'right hand' (`JMJN/`, 21 atoms) are pointed alike; here in a list of names. |
| A198 | lexeme | Nehemiah 8:15 | עֲלֵי־ | עֲלֵי־ | `<LH=/ -.pl.m` | `<L` x38 | **homograph** (form) | The plural construct of 'leafage' (`<LH=/`) and the poetic preposition 'upon' (`<L`, 38 atoms) are pointed alike; here 'olive branches'. |
| A207 | lexeme | 1 Chronicles 6:29; 2 Chronicles 29:12 | עַבְדִּי | עַבְדִּי | `<BDJ/ -.sg.m +n/a` | `<BD/ -.sg.m +J` x52 | **homograph** (name) | The name Abdi and 'my servant' (`<BD/` with suffix `J`, 52 atoms) are pointed alike; here in genealogies. |
| A208 | lexeme | 1 Chronicles 6:44 | עָשָׁן | עָשָׁן | `<CN==/ -.sg.? +n/a` | `<CN/ -.sg.m` x12 | **homograph** (name) | The place name Ashan and the noun 'smoke' (`<CN/`, 12 atoms) are pointed alike; here in a list of towns. |
| A216 | lexeme | 1 Chronicles 20:8 | אֵל | אֵל | `>L=== -.pl.? +n/a` | `>L/ -.sg.m` x162; `>JL===/ -.sg.m` x1 | **homograph** (form) | The short demonstrative 'these' (`>L===`) and 'God' (`>L/`, 162 atoms) are pointed alike; here 'these were born to the giant'. |
| A222 | segmentation | 2 Chronicles 30:10 | לָעִיר | לָעִיר | `L + <JR/ -.sg.f` | `L + H + <JR/ -.sg.f` x25 | **homograph** (article) | Before a stressed monosyllable in a paired phrase the qamats under the preposition can be its vowel, with no article: here 'from city to city', whose first atom has no article, as the BHSA reads 'from gate to gate' at Exodus 32:27 and 'from generation to generation' at Isaiah 34:10 (out/p2e-checks.txt, part 2). The other 25 atoms of this pointing have the article. |

## The rows: Test B's atoms

| # | Reference | Class (slot level) | BHSA | MAM | BHSA's analysis | Category | Reason |
|---|---|---|---|---|---|---|---|
| B4762 | Genesis 15:10 | mam-unique (mam-elsewhere) | הַצִפֹּר | הַצִּפֹּר | `H + YPWR/ -.sg.?` | **no-word** | No dagesh forte in the tsadi after the article, where MAM has one; with pataḥ and no dagesh the he is not the interrogative either, and the analysis reads the article and 'bird' (`YPWR/`) through it (WLC 4.18 has the BHSA's, with note 1). One of the four slot-level mam-elsewhere artifacts of out/p2d-review.md. |
| B11268 | Genesis 30:19 | mam-unique (both) | לְּיַעֲקֹב | לְיַעֲקֹב | `L + J<QB/ -.sg.m +n/a` | **no-word** | A dagesh in the preposition's lamed at the start of the atom, which MAM lacks, after an atom with tipeḥa, a disjunctive accent, where the rules of the conjunctive dagesh give none; spells no other word (WLC 4.18 has it, with note 1). |
| B12313 | Genesis 31:51 | mam-unique (both) | הַמַצֵּבָה | הַמַּצֵּבָה | `H + MYBH/ -.sg.f` | **no-word** | No dagesh forte in the mem after the article, where MAM has one, as the BHSA has it twice in the next verse; spells no other word (WLC 4.18 has the BHSA's, with note 1). |
| B15635 | Genesis 40:3 | mam-unique (both) | הַטַבָּחִים | הַטַּבָּחִים | `H + VBX=/ -.pl.m` | **no-word** | No dagesh forte in the tet after the article, where MAM has one, as the BHSA has it at its 5 other atoms of this analysis (as at Genesis 37:36); spells no other word (WLC 4.18 note 1). |
| B16215 | Genesis 41:24 | mam-unique (both) | הָשִׁבֳּלִים | הַשִּׁבֳּלִים | `H + CBLT/ -.pl.f` | **no-word** | The article has qamats and the shin no dagesh forte, where MAM has pataḥ and the dagesh; the article has qamats instead of a dagesh only before a guttural or resh, and the verse's other atom of this noun has pataḥ (WLC 4.18 has the BHSA's, with note 1). |
| B20938 | Exodus 2:10 | mam-unique (mam-elsewhere) | וַיִגְדַּל | וַיִּגְדַּל | `W + GDL[ qal wayq p3.sg.m` | **no-word** | No dagesh forte in the yod of the wayyiqtol's prefix after the conjunction's pataḥ, where MAM has one; the conjunction marks the tense, and the analysis reads the regular wayyiqtol (WLC 4.18 has the BHSA's, with note 1). One of the four slot-level mam-elsewhere artifacts of out/p2d-review.md. |
| B32091 | Exodus 29:23 | mam-unique (both) | וַחַלַּת | וְחַלַּת | `W + XLH/ -.sg.f` | **no-word** | The conjunction has pataḥ, its vowel before a ḥataf pataḥ, but the ḥet after it has a full pataḥ, before which the conjunction has sheva, as MAM's atom has; outside the wayyiqtol the BHSA has the conjunction with pataḥ before a guttural with a full pataḥ only here, at Numbers 16:21 and at Daniel 5:12 (out/p2e-checks.txt, part 3). |
| B36526 | Exodus 39:20 | mam-unique (both) | מִלְמַטָּה | מִלְּמַטָּה | `MN + L + MVH==/ -.sg.m` | **variant** | No dagesh forte in the lamed, which has sheva, after the preposition `MN`, where MAM has one: a dagesh forte that a letter with sheva may lack. |
| B49943 | Numbers 2:14 | mam-unique (both) | וְמַטֵּה | וּמַטֵּה | `W + MVH/ -.sg.m` | **no-word** | A sheva under the conjunction's vav before mem, where the rule gives a shuruq, as MAM has (the review's case 5, Part 1's class c). |
| B57361 | Numbers 17:12 | mam-unique (both) | תֹּוך | תּוֹךְ | `TWK/ -.sg.m` | **no-word** | No sheva in the final kaf, which MAM has (WLC 4.18 has the BHSA's, with note 1). |
| B60481 | Numbers 24:9 | mam-unique (both) | מְבָרֲכֶיךָ | מְבָרְכֶיךָ | `BRK[ piel ptca ?.pl.m +K` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B60987 | Numbers 26:7 | mam-unique (both) | הָרֻאוּבֵנִי | הָראוּבֵנִי | `H + R>WBNJ/ -.sg.m` | **no-word** | A qubuts under the resh as well as the shuruq after the alef, where MAM has no vowel under the resh and a rafeh on the alef: two vowels for one syllable, as p2c judged the same pattern at Job 31:7 (the review's case 6, Part 1's class c; WLC 4.18 note 1). |
| B67025 | Deuteronomy 3:16 | mam-unique (both) | וְלָרֻאוּבֵנִי | וְלָראוּבֵנִי | `W + L + H + R>WBNJ/ -.sg.m` | **no-word** | As at Numbers 26:7 (the review's case 9, Part 1's class c; WLC 4.18 note U). |
| B95325 | Judges 11:34 | mam-unique (both) | בְתֻפִּים | בְּתֻפִּים | `B + TP/ -.pl.m` | **variant** | No dagesh lene in the bet that begins the atom, which MAM has, after an atom ending in a vowel: a dagesh lene that depends on the atom before. |
| B95348 | Judges 11:35 | mam-unique (both) | הָיִיתְ | הָיִית | `HJH[ qal perf p2.sg.f` | **variant** | A sheva under the final tav of the second feminine singular perfect, which MAM lacks; it marks the feminine ending, and the word is the same (WLC 4.18 has it, with note U). |
| B111052 | 1 Samuel 26:11 | mam-unique (both) | וְנֵלֲכָה | וְנֵלְכָה־ | `W + HLK[ qal impf p1.pl.?` | **variant** | A ḥataf pataḥ under the lamed for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B114192 | 2 Samuel 3:27 | mam-unique (both) | לְדַּבֵּר | לְדַבֵּר | `L + DBR[ piel infc ?.?.?` | **no-word** | A dagesh in the dalet after the preposition's vocal sheva, where neither a dagesh lene nor the piel's doubling, which is in the bet, belongs; WLC 4.18 and MAM lack it. |
| B114276 | 2 Samuel 3:32 | mam-unique (mam-elsewhere) | וַיִשָּׂא | וַיִּשָּׂא | `W + NF>[ qal wayq p3.sg.m` | **no-word** | No dagesh forte in the yod of the wayyiqtol's prefix after the conjunction's pataḥ, where MAM has one; the conjunction marks the tense, and the analysis reads the regular wayyiqtol (WLC 4.18 has the BHSA's, with note 1). One of the four slot-level mam-elsewhere artifacts of out/p2d-review.md. |
| B119492 | 2 Samuel 16:4 | mam-unique (both) | לִמְפִי־בֹשֶׁת | לִמְפִיבֹשֶׁת | `L + MPJBCT/ -.sg.m +n/a` | **variant** | The compound name in two parts joined by a maqaf, where MAM has one atom: the same name, divided. |
| B119742 | 2 Samuel 16:19 | mam-unique (both) | לִפָנֶיךָ | לְפָנֶיךָ | `L + PNH/ -.pl.m +K` | **no-word** | A ḥiriq under the preposition before a letter with a full vowel, where the rule gives sheva, as WLC 4.18 and MAM have; the verse's earlier 'before your father' has the ḥiriq of the construct. |
| B126114 | 1 Kings 4:17 | mam-unique (both) | בְּיִשָׂשכָר | בְּיִשָּׂשכָר | `B + JFFKR/ -.sg.? +n/a` | **no-word** | No dagesh forte in the first sin of Issachar, which MAM has; the BHSA has the name so at 13 other words (slot level), against 29 with MAM's dagesh. |
| B135147 | 1 Kings 20:13 | mam-unique (both) | הְרָאִיתָ | הֲרָאִיתָ | `H= + R>H[ qal perf p2.sg.m` | **variant** | A sheva under the interrogative he for MAM's ḥataf pataḥ: a sheva for a ḥataf; the BHSA's interrogative he has sheva at 2 other words (slot level). |
| B135837 | 1 Kings 21:8 | mam-unique (both) | הַזְקֵנִים | הַזְּקֵנִים | `H + ZQN/ -.pl.m` | **variant** | No dagesh forte in the zayin, which has sheva, after the article, where MAM has one: a dagesh forte that a letter with sheva may lack (WLC 4.18 note 1). |
| B136611 | 1 Kings 22:29 | mam-unique (both) | וְיהֹושָׁפָט | וִיהוֹשָׁפָט | `W + JHWCPV/ -.sg.m +n/a` | **no-word** | A sheva under the conjunction's vav and no vowel under the name's yod, where the rule gives the vav a ḥiriq, as MAM has; spells no other word (WLC 4.18 note 1). |
| B137860 | 2 Kings 3:9 | mam-unique (both) | וּמֶלֶך־ | וּמֶלֶךְ־ | `W + MLK/ -.sg.m` | **no-word** | No sheva in the final kaf, which MAM has. |
| B140816 | 2 Kings 9:2 | mam-unique (both) | מִתֹּוך | מִתּוֹךְ | `MN + TWK/ -.sg.m` | **no-word** | No sheva in the final kaf, which MAM has (WLC 4.18 note 1). |
| B144095 | 2 Kings 15:30 | mam-unique (both) | עֻזִיָּה | עֻזִּיָּה | `<ZJH/ -.sg.m +n/a` | **no-word** | No dagesh forte in the zayin of Uzziah, which the qubuts before it needs and MAM has, as p2c judged 1 Chronicles 11:44's Uzzia; the BHSA has this name so at 2 other words (slot level). |
| B144293 | 2 Kings 16:6 | mam-unique (both) | הַיְהוּדִים | הַיְּהוּדִים | `H + JHWDJ/ -.pl.m` | **variant** | No dagesh forte in the yod, which has sheva, after the article, where MAM has one: a dagesh forte that a letter with sheva may lack. |
| B153887 | Isaiah 20:1 | mam-unique (both) | בִּשְׁלֹח | בִּשְׁלֹחַ | `B + CLX[ qal infc ?.?.?` | **no-word** | No furtive pataḥ under the final ḥet, which MAM has. |
| B157860 | Isaiah 36:9 | mam-unique (both) | הַקְטַנִּים | הַקְּטַנִּים | `H + QVN=/ -.pl.m` | **variant** | No dagesh forte in the qof, which has sheva, after the article, where MAM has one: a dagesh forte that a letter with sheva may lack. |
| B158377 | Isaiah 37:20 | mam-unique (both) | מִיָדֹו | מִיָּדוֹ | `MN + JD/ -.sg.? +W` | **no-word** | No dagesh forte in the yod, which has qamats, after the preposition `MN`, where MAM has one; spells no other word (WLC 4.18 note 1). |
| B164844 | Isaiah 62:3 | mam-unique (both) | וְהָיִיתְ | וְהָיִית | `W + HJH[ qal perf p2.sg.f` | **variant** | As at Judges 11:35: a sheva under the final tav of the second feminine singular perfect (WLC 4.18 note 1). |
| B185728 | Jeremiah 49:37 | mam-unique (both) | לפְנֵי | לִפְנֵי | `L + PNH/ -.pl.m` | **no-word** | No vowel under the preposition's lamed, where WLC 4.18 and MAM have ḥiriq. |
| B188595 | Ezekiel 3:10 | mam-unique (both) | שְׁמָע | שְּׁמָע | `CM<[ qal impv p2.sg.m` | **variant** | No dagesh in the shin that begins the atom, where MAM has the conjunctive dagesh after an atom with merkha ending in qamats: a dagesh that depends on the atom before. |
| B191270 | Ezekiel 12:10 | mam-unique (no slot-level row) | בִּירוּשָׁלַם | בִּירוּשָׁלִַם | `B + JRWCLM/ -.sg.? +n/a` | **variant** | Jerusalem without the orphaned ḥiriq of the implicit yod, which MAM and WLC 4.18 have (WLC's note v); most of the BHSA's words of this analysis have it. |
| B191748 | Ezekiel 13:16 | mam-unique (both) | הַנִבְּאִים | הַנִּבְּאִים | `H + NB>[ nif ptca ?.pl.m` | **no-word** | No dagesh forte in the nun, which has ḥiriq, after the article, where MAM has one; spells no other word (WLC 4.18 note 1). |
| B193102 | Ezekiel 16:54 | mam-unique (both) | וִנִכְלַמְתְּ | וְנִכְלַמְתְּ | `W + KLM[ nif perf p2.sg.f` | **no-word** | A ḥiriq under the conjunction's vav before a nun with ḥiriq, where the rule gives sheva, as MAM and WLC 4.18 have (WLC's note v). |
| B194351 | Ezekiel 20:8 | mam-unique (both) | לִּשְׁמֹעַ | לִשְׁמֹעַ | `L + CM<[ qal infc ?.?.?` | **no-word** | A dagesh in the preposition's lamed at the start of the atom, which MAM lacks, after an atom with pashta, a disjunctive accent, where the rules of the conjunctive dagesh give none (WLC 4.18 has it). |
| B208609 | Hosea 12:5 | mam-unique (both) | וָיָּשַׂר | וַיָּשַׂר | `W + FWR[ qal wayq p3.sg.m` | **no-word** | Qamats under the wayyiqtol's conjunction before the prefix's yod with dagesh, where the rule gives pataḥ, as MAM has. The analysis's lexeme, `FWR[` (gloss '<uncertain>'), is one of the two that the BHSA gives MAM's pointing: `FWR[` at 1 Chronicles 20:3, `FRR[` at Judges 9:22. |
| B209170 | Joel 1:15 | mam-unique (both) | מִשַׁדַּי | מִשַּׁדַּי | `MN + CDJ/ -.sg.m +n/a` | **no-word** | No dagesh forte in the shin, which has pataḥ, after the preposition `MN`, where MAM has one; spells no other word (WLC 4.18 note U). |
| B212015 | Obadiah 1:3 | mam-unique (both) | סֶּלַע | סֶלַע | `SL</ -.sg.m` | **variant** | A dagesh in the samekh that begins the atom, which MAM lacks, after an atom joined to it by maqaf: a conjunctive dagesh, which depends on the atom before (WLC 4.18 has it). |
| B212655 | Jonah 3:2 | mam-unique (both) | וִּקְרָא | וּקְרָא | `W + QR>[ qal impv p2.sg.m` | **no-word** | The conjunction's vav has a shuruq dot and a ḥiriq, where MAM has a shuruq (the review's case 31, Part 1's class c; WLC 4.18 note U). |
| B217248 | Zechariah 2:2 | mam-unique (no slot-level row) | וִירוּשָׁלָם | וִירוּשָׁלִָם | `W + JRWCLM/ -.sg.? +n/a` | **variant** | Jerusalem without the orphaned ḥiriq of the implicit yod, which MAM has (the review's case 32, Part 1's class c; WLC 4.18 note U). |
| B232471 | Psalms 87:5 | mam-unique (both) | וּלֲצִיֹּון | וּלְצִיּוֹן | `W + L + YJWN==/ -.sg.? +n/a` | **variant** | A ḥataf pataḥ under the preposition's lamed for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B240515 | Psalms 150:4 | mam-unique (both) | בְתֹף | בְּתֹף | `B + TP/ -.sg.m` | **variant** | No dagesh lene in the bet that begins the atom, which MAM has, after an atom ending in a vowel: a dagesh lene that depends on the atom before. |
| B242039 | Job 8:1 | mam-unique (mam-elsewhere) | וַיֹאמַר | וַיֹּאמַר | `W + >MR[ qal wayq p3.sg.m` | **no-word** | No dagesh forte in the yod of the wayyiqtol's prefix after the conjunction's pataḥ, where MAM has one; the conjunction marks the tense, and the analysis reads the regular wayyiqtol (WLC 4.18 has the BHSA's, with note 1). One of the four slot-level mam-elsewhere artifacts of out/p2d-review.md. |
| B250288 | Proverbs 7:22 | mam-unique (both) | טָבַח | טֶבַח | `VBX/ -.sg.m` | **variant** | Qamats under the tet, the vowel of the noun's pausal form, which the BHSA has at 4 other words of this noun (as at Isaiah 34:2 and Ezekiel 21:20), where MAM has the contextual segol; here the atom has munaḥ, a conjunctive accent, so the vowel is unexpected (WLC 4.18 has the BHSA's, with note U). The qal perfect of `VBX[` would be pointed alike, but the BHSA has no such word, and the context wants the noun (out/p2e-checks.txt, part 1). |
| B257311 | Song of Songs 2:9 | mam-unique (both) | הַחֲלֹּנֹות | הַחַלֹּנוֹת | `H + XLWN/ -.pl.f` | **no-word** | A ḥataf pataḥ under the ḥet before the doubled lamed, whose doubling closes the syllable, where MAM has a full pataḥ; p2c judges such a ḥataf no-word, p2b a variant, and neither makes it a correction. |
| B263747 | Esther 3:6 | mam-unique (both) | לִשְׁלֹח | לִשְׁלֹחַ | `L + CLX[ qal infc ?.?.?` | **no-word** | No furtive pataḥ under the final ḥet, which MAM has (WLC 4.18 note U). |
| B269698 | Daniel 7:20 | mam-unique (both) | וְפֻם | וּפֻם | `W + PM/ -.sg.m` | **no-word** | A sheva under the conjunction's vav before pe, where the rule gives a shuruq, as MAM has (Aramaic; the review's case 41, Part 1's class c). |
| B290458 | 1 Chronicles 27:18 | mam-unique (both) | לְיִשָׂשכָר | לְיִשָּׂשכָר | `L + JFFKR/ -.sg.? +n/a` | **no-word** | No dagesh forte in the first sin of Issachar, which MAM has; the BHSA has the name so at 13 other words (slot level), against 29 with MAM's dagesh. |
| B304199 | 2 Chronicles 35:15 | mam-unique (both) | וְהַמְשֹׁרֲרִים | וְהַמְשֹׁרְרִים | `W + H + CJR[ piel ptca ?.pl.m` | **variant** | A ḥataf pataḥ under the first resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B9969 | Genesis 27:29 | neither (both) | וּמְבָרֲכֶיךָ | וּמְבָרְכֶיךָ | `W + BRK[ piel ptca ?.pl.m +K` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B10335 | Genesis 28:6 | neither (written) | בְּבָרֲכֹו | בְּבָרְכוֹ | `B + BRK[ piel infc ?.?.? +W` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B12607 | Genesis 32:18 | neither (both) | וִשְׁאֵלְךָ | וּשְׁאֵלְךָ | `W + C>L[ qal perf p3.sg.m +K` | **no-word** | A ḥiriq under the conjunction's vav before a shin with sheva, where the rule gives a shuruq, as MAM has (the review's case 1, Part 1's class c; WLC 4.18 note 1). |
| B19615 | Genesis 48:9 | neither (written) | וַאֲבָרֲכֵם | וַאֲבָרְכֵם | `W + BRK[ piel impf p1.sg.? +M` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B52248 | Numbers 6:27 | neither (written) | אֲבָרֲכֵם | אֲבָרְכֵם | `BRK[ piel impf p1.sg.? +M` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B67849 | Deuteronomy 4:35 | neither (both) | מִלְבַדֹּו | מִלְּבַדּוֹ | `MN + L + BD/ -.sg.m +W` | **variant** | No dagesh forte in the lamed, which has sheva, after the preposition `MN`, where MAM has one: a dagesh forte that a letter with sheva may lack (WLC 4.18 note U). |
| B76818 | Deuteronomy 28:29 | neither (both) | הָעִוֵּר | הַעִוֵּר | `H + <WR/ -.sg.m` | **variant** | The article has qamats before the ayin, its usual vowel there, where MAM has pataḥ. |
| B78808 | Deuteronomy 32:6 | neither (both) | הֲ־ | הַ | `H=` | **variant** | The interrogative he as a separate atom, with ḥataf pataḥ, its vowel before the next atom's pataḥ, and a maqaf; MAM's atom has pataḥ, its vowel before the sheva of MAM's next atom. Both are the interrogative. |
| B78809 | Deuteronomy 32:6 | neither (both) | לַיְהוָה | לְיְהֹוָה | `L + JHWH/ -.sg.m +n/a` | **variant** | Pataḥ under the preposition and a sheva under the divine name's yod, a sheva that the BHSA's 572 other atoms of this analysis with that pataḥ lack (as at Genesis 4:3); MAM's atom has a sheva under the preposition, the same sheva under the yod and a ḥolam on the he. Both are the preposition with the divine name. |
| B104213 | 1 Samuel 13:10 | neither (written) | לְבָרֲכֹו | לְבָרְכוֹ | `L + BRK[ piel infc ?.?.? +W` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B105206 | 1 Samuel 14:49 | neither (written) | וּמַלְכִּי־שׁוּעַ | וּמַלְכִּישׁוּעַ | `W + MLKJ_CW</ -.sg.m +n/a` | **variant** | The compound name in two parts joined by a maqaf, where MAM has one atom: the same name, divided. |
| B121506 | 2 Samuel 19:33 | neither (both) | בְשִׁיבָתֹו | בְּשִׁיבָתוֹ | `B + CJBH/ -.sg.f +W` | **variant** | No dagesh lene in the bet that begins the atom, which WLC 4.18 and MAM have, after an atom ending in a consonant: a dagesh lene that depends on the atom before. |
| B143798 | 2 Kings 15:13 | neither (both) | לְעֻזִיָּה | לְעֻזִּיָּה | `L + <ZJH/ -.sg.m +n/a` | **no-word** | No dagesh forte in the zayin of Uzziah, which the qubuts before it needs and MAM has, as p2c judged 1 Chronicles 11:44's Uzzia; the BHSA has this name so at 2 other words (slot level). |
| B152607 | Isaiah 14:3 | neither (both) | וּמֵרָגְזֶךָ | וּמִרָגְזֶךָ | `W + MN + RGZ/ -.sg.m +K` | **variant** | The preposition `MN` has tsere before the resh, its usual vowel there, where MAM has ḥiriq. |
| B154111 | Isaiah 21:11 | neither (both) | מִלַּיְלָה | מִּלַּיְלָה | `MN + LJLH/ -.sg.m` | **variant** | No dagesh in the mem that begins the atom, where MAM has the conjunctive dagesh after 'what' joined by maqaf: a dagesh that depends on the atom before. |
| B154114 | Isaiah 21:11 | neither (both) | מִלֵּיל | מִּלֵּיל | `MN + LJL/ -.sg.m` | **variant** | No dagesh in the mem that begins the atom, where MAM has the conjunctive dagesh after 'what' joined by maqaf: a dagesh that depends on the atom before. |
| B156861 | Isaiah 31:8 | neither (both) | תֹּאכֲלֶנּוּ | תֹּאכְלֶנּוּ | `>KL[ qal impf p3.sg.f +HW` | **homograph** (form) | The second masculine and third feminine singular are pointed alike; the subject is 'a sword', feminine, and the BHSA's other 5 atoms of this pointing are second masculine (as at Numbers 18:10). The ḥataf pataḥ under the kaf, where MAM has sheva, is the BHSA's pointing of those 5 atoms too. out/p2d-review.md lists this atom among Test B's departures in person, number, gender or suffix. |
| B166062 | Isaiah 66:22 | neither (written) | הַחֳדָשִׁים | הַחֲדָשִׁים | `H + XDC=/ -.pl.m` | **follows-pointing** | The noun 'month' (`XDC=/`), which the ḥataf qamats spells; MAM's ḥataf pataḥ spells the adjective 'new' (`XDC/`), which the BHSA gives the verse's other atom of that root (the review's case 25, Part 1's class a). |
| B169391 | Jeremiah 8:19 | neither (both) | הַיהוָה | הַיהֹוָה | `H= + JHWH/ -.sg.m +n/a` | **variant** | The interrogative he and the divine name, without the ḥolam on the he that MAM's atom has. |
| B169418 | Jeremiah 8:22 | neither (written) | הַצֳרִי | הַצֳּרִי | `H= + YRJ/ -.sg.m` | **variant** | The interrogative he with pataḥ before a letter with ḥataf qamats, without the dagesh that MAM's atom has after it; that dagesh is optional after the interrogative, and without it the atom cannot have the article, so the pointing spells the analysis. |
| B178161 | Jeremiah 31:34 | neither (both) | לְמִקְטַנָּם | לְמִקְּטַנָּם | `L + MN + QVN=/ -.sg.m +M` | **variant** | No dagesh forte in the qof, which has sheva, after the preposition `MN`, where MAM has one: a dagesh forte that a letter with sheva may lack. |
| B195406 | Ezekiel 21:31 | neither (both) | וְהַגָּבֹהַ | וְהַגָּבֹהַּ | `W + H + GBH/ -.sg.m` | **no-word** | No mappiq in the final he, which has a furtive pataḥ, a vowel that only a consonant has; MAM has the mappiq (WLC 4.18 note 1). |
| B195815 | Ezekiel 22:26 | neither (written) | וּמִשַׁבְּתֹותַי | וּמִשַּׁבְּתוֹתַי | `W + MN + CBT/ -.pl.f +J` | **no-word** | No dagesh forte in the shin, which has pataḥ, after the preposition `MN`, where MAM has one; spells no other word. |
| B196336 | Ezekiel 23:36 | neither (written) | תֹועֲבֹותֵיהֶן | תּוֹעֲבוֹתֵיהֶן | `TW<BH/ -.pl.f +HN` | **variant** | No dagesh lene in the tav that begins the atom, which MAM has, after an atom ending in a consonant: a dagesh lene that depends on the atom before. WLC 4.18 lacks it too. |
| B197674 | Ezekiel 27:20 | neither (both) | בְבִגְדֵי־ | בְּבִגְדֵי־ | `B + BGD/ -.pl.m` | **variant** | No dagesh lene in the bet that begins the atom, which MAM has, after an atom ending in a consonant: a dagesh lene that depends on the atom before. |
| B199639 | Ezekiel 32:30 | neither (both) | מִגְּבוּרָתָם | מִגְבוּרָתָם | `MN + GBWRH/ -.sg.f +M` | **variant** | A dagesh forte in the gimel, which has sheva, after the preposition `MN`, which MAM and WLC 4.18 lack: a dagesh forte that a letter with sheva may have or lack. |
| B203044 | Ezekiel 40:25 | neither (both) | כְּהַחֲלֹּנֹות | כְּהַחַלֹּנוֹת | `K + H + XLWN/ -.pl.f` | **no-word** | A ḥataf pataḥ under the ḥet before the doubled lamed, whose doubling closes the syllable, where MAM has a full pataḥ; p2c judges such a ḥataf no-word, p2b a variant, and neither makes it a correction. |
| B206999 | Hosea 2:17 | neither (both) | וִּכְיֹום | וּכְיוֹם | `W + K + JWM/ -.sg.m` | **no-word** | The conjunction's vav has a shuruq dot and a ḥiriq, where MAM has a shuruq (the review's case 29, Part 1's class c; WLC 4.18 note U). |
| B209394 | Joel 2:12 | neither (both) | וּבְבְכִי | וּבִבְכִי | `W + B + BKJ/ -.sg.m` | **no-word** | A sheva under the preposition before a bet with sheva, two sheva marks in a row, where the rule gives the preposition ḥiriq, as MAM has (the review's case 30, Part 1's class c; WLC 4.18 note U). |
| B209651 | Joel 3:3 | neither (written) | וְתִימֲרֹות | וְתִימְרוֹת | `W + TJMRH/ -.pl.f` | **variant** | A ḥataf pataḥ under the mem for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B218909 | Zechariah 9:17 | neither (written) | יָפְיֹו | יָּפְיוֹ | `JPJ/ -.sg.m +W` | **variant** | No dagesh in the yod that begins the atom, where MAM has the conjunctive dagesh after 'and how' joined by maqaf: a dagesh that depends on the atom before. |
| B223241 | Psalms 21:14 | neither (both) | בְעֻזֶּךָ | בְּעֻזֶּךָ | `B + <Z/ -.sg.m +K` | **variant** | No dagesh lene in the bet that begins the atom, which WLC 4.18 and MAM have, after an atom ending in a vowel: a dagesh lene that depends on the atom before. |
| B224820 | Psalms 34:2 | neither (written) | אֲבָרֲכָה | אֲבָרְכָה | `BRK[ piel impf p1.sg.?` | **variant** | A ḥataf pataḥ under the resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B236945 | Psalms 119:14 | neither (written) | שַׂשְׂתִּי | שַּׂשְׂתִּי | `FWF[ qal perf p1.sg.?` | **variant** | No dagesh in the sin that begins the atom, where MAM has the conjunctive dagesh after an atom ending in qamats: a dagesh that depends on the atom before. |
| B241402 | Job 4:17 | neither (both) | מֵאֱלֹוהַ | מֵאֱלוֹהַּ | `MN + >LWH/ -.sg.m` | **no-word** | No mappiq in the final he, which has a furtive pataḥ, a vowel that only a consonant has; MAM has the mappiq. |
| B245426 | Job 27:9 | neither (both) | הַצַעֲקָתֹו | הֲצַעֲקָתוֹ | `H= + Y<QH/ -.sg.f +W` | **variant** | The interrogative he with pataḥ for MAM's ḥataf pataḥ: a full vowel for a ḥataf under a guttural; with no dagesh after it, it cannot be the article. |
| B247140 | Job 34:33 | neither (both) | הַמֵעִמְּךָ | הֲמֵעִמְּךָ | `H= + MN + <M +K` | **variant** | The interrogative he with pataḥ for MAM's ḥataf pataḥ: a full vowel for a ḥataf under a guttural; with no dagesh after it, it cannot be the article. |
| B247316 | Job 36:3 | neither (both) | וְלְפֹעֲלִי | וּלְפֹעֲלִי | `W + L + P<L[ qal ptca ?.sg.m +J` | **no-word** | A sheva under the conjunction's vav before the preposition's sheva, two sheva marks in a row, where the rule gives a shuruq, as WLC 4.18 and MAM have. |
| B247812 | Job 38:12 | neither (both) | הְמִיָּמֶיךָ | הֲמִיָּמֶיךָ | `H= + MN + JWM/ -.pl.m +K` | **variant** | A sheva under the interrogative he for MAM's ḥataf pataḥ: a sheva for a ḥataf (WLC 4.18 note 1). |
| B248163 | Job 39:20 | neither (both) | הְתַרְעִישֶׁנּוּ | הֲתַרְעִישֶׁנּוּ | `H= + R<C[ hif impf p2.sg.m +HW` | **variant** | A sheva under the interrogative he for MAM's ḥataf pataḥ: a sheva for a ḥataf. |
| B256127 | Ruth 2:2 | neither (written) | וַאֲלַקֳטָה | וַאֲלַקֳּטָה | `W + LQV[ piel impf p1.sg.?` | **variant** | No dagesh forte in the piel's qof, which has ḥataf qamats, a vocal sheva's vowel, where MAM has one: a dagesh forte that such a letter may lack (WLC 4.18 has none in the qof and one in the tet, with notes Q, n and p). |
| B256188 | Ruth 2:7 | neither (written) | אֲלַקֳטָה־ | אֲלַקֳּטָה־ | `LQV[ piel impf p1.sg.?` | **variant** | No dagesh forte in the piel's qof, which has ḥataf qamats, a vocal sheva's vowel, where MAM has one: a dagesh forte that such a letter may lack. |
| B257474 | Song of Songs 3:6 | neither (written) | כְּתִימֲרֹות | כְּתִימְרוֹת | `K + TJMRH/ -.pl.f` | **variant** | A ḥataf pataḥ under the mem for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B258854 | Ecclesiastes 2:22 | neither (both) | שֶׁהוּא | שְׁהוּא | `C + HW> p3.sg.m +n/a` | **variant** | The relative particle with segol, its usual vowel before he, where MAM has sheva; both are the relative particle. |
| B265966 | Daniel 1:4 | neither (both) | וּלֲלַמְּדָם | וּלְלַמְּדָם | `W + L + LMD[ piel infc ?.?.? +M` | **variant** | A ḥataf pataḥ under the preposition's lamed, before a second lamed, for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B268467 | Daniel 5:12 | neither (both) | וַאַחֲוָיַת | וְאַחֲוָיַת | `W + XWH[ afel infc ?.?.?` | **no-word** | As at Exodus 29:23, in Aramaic: the conjunction has pataḥ before an alef with a full pataḥ, where MAM has sheva. |
| B275395 | Ezra 10:21 | neither (both) | וְעֻזִיָּה | וְעֻזִּיָּה | `W + <ZJH/ -.sg.m +n/a` | **no-word** | No dagesh forte in the zayin of Uzziah, which the qubuts before it needs and MAM has, as p2c judged 1 Chronicles 11:44's Uzzia; the BHSA has this name so at 2 other words (slot level). |
| B276742 | Nehemiah 4:7 | neither (written) | מִתַּחְתִּיֹּות | מִתַּחְתְּיוֹת | `MN + TXTJ/ -.pl.f` | **variant** | Ḥiriq under the second tav and a dagesh in the yod, the usual feminine plural of an adjective ending in ḥiriq and yod, where MAM has a sheva under the tav and no dagesh in the yod. |
| B292869 | 2 Chronicles 5:13 | neither (both) | וְלַמְשֹׁרֲרִים | וְלַמְשֹׁרְרִים | `W + L + H + CJR[ piel ptca ?.pl.m` | **variant** | A ḥataf pataḥ under the first resh for MAM's vocal sheva: a ḥataf for a vocal sheva, the same word. |
| B296463 | 2 Chronicles 15:16 | neither (both) | לַאֲשֵׁרָה | לָאֲשֵׁרָה | `L + >CRH/ -.sg.f` | **follows-pointing** | With pataḥ, the preposition before a ḥataf pataḥ has no article, and the analysis has none (`L + >CRH/`); MAM's qamats is the article's, as the BHSA analyses that pointing at 1 Kings 15:13 and 2 Kings 23:7 (`L + H + >CRH/`). |

## Files

- `scripts/p2e_select.py`: the selection and its evidence, `out/p2e-candidates.txt` and `.json`.
- `scripts/p2e_checks.py`: `out/p2e-checks.txt`, the checks that reasons cite (part 1, Proverbs 7:22 and the spellings of `VBX/`; part 2, the preposition with qamats and no article; part 3, the conjunction with pataḥ before a guttural with pataḥ; part 4, `M>N[`; part 5, `>TH` and `>T=`; part 6, the differences from WLC 4.18; part 7, accents).
- `scripts/show_texts.py` (not edited): `out/p2e-texts.txt`, the another-word verses in five texts.
- `scripts/p2e_review.py`: the judgments (`JUDGMENTS`), this page and `out/p2e-review.json`.
