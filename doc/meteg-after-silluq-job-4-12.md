# Meteg after silluq at Job 4:12: what the repositories hold

Written 2026-09-10 by a Claude session in the MAM-basics worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c`, on the branch `claude/interesting-taussig-6aa52b`, starting from its head `683a3a31`. That head contains `5e61a2d1`, the commit recording Ben's Koren reading of Job 4:12, and does not contain `7d0888b3`, the head of `main` that day. Ben's instruction, 2026-09-10, was to investigate further "the one case that seems to have turned up a possible additional case of meteg after silluq (beyond the known 1 Kings 7:37 case ...)". That case is Job 4:12, rank 3 in `doc/meteg-after-silluq-koren-lookup-candidates.md`, where Ben found that the Koren edition has only one of MAM's two U+05BD, the one on the mem (`in/meteg_after_silluq_koren_readings.json`). The prompt that started this session, written by the Claude session running the Koren lookups, asked it to establish what the repositories already hold about this chanted word and to report that to Ben before doing anything further. Everything below is this session's account of the data, and each interpretive step says so. Revised the same day: the first version, `6e1d4164`, argued from where a meteg stroke stands relative to its vowel, and that argument is withdrawn (section 4). Later that day Ben read both codices at this verse and found them agreeing on that placement; section 4 records it, and why it leaves the disposition as it was.

Terms. An **atom** is one written word between spaces or maqafs; a **chanted word** is a lone atom or a whole maqaf compound. The verse-final chanted word of Job 4:12 is the lone atom מֶֽנְהֽוּ׃ and the verse, as MAM-simple has it, is וְ֭אֵלַי דָּבָ֣ר יְגֻנָּ֑ב וַתִּקַּ֥ח אׇ֝זְנִ֗י שֵׁ֣מֶץ מֶֽנְהֽוּ׃ In this file's voice **meteg** is U+05BD, and **silluq** is the U+05BD on the stressed syllable of a verse-final chanted word, so which of this atom's two U+05BD is the silluq depends on where its stress is. A **stroke** is a short vertical mark under a letter in a photograph of a manuscript; in these manuscripts a meteg and a silluq have the same shape. Yeivin's gaʿya and Breuer's ga'aya are this file's meteg, and their silluq and siluk are its silluq; each book's term is kept where the book is reported.

## 1. Summary: every text consulted but Koren has both U+05BD, and the evidence on disk favours penultimate stress

1. **MAM has both U+05BD with no note on the atom, and the Aleppo Codex is their source: established.** MAM's source line, `in/mam-ws/D3-Job.json` line 123, has the atom as plain text; the verse's one template is a `מ:דחי` on its first atom. MAM-parsed plus (`MAM-parsed/plus/D3-Job.json` line 1191) and MAM-simple (`MAM-simple/xml-vtrad-mam/Job.xml` line 140) have the same atom. MAM copies the meteg as the Aleppo Codex has it wherever that manuscript survives (`in/mam-ws-intro/ch3.mediawiki` line 1328, the section `נוסח הגעיות במהדורתנו`), and Job survives in it in full (`in/mam-ws-intro/ch5.mediawiki` line 658). MAM's list of the Aleppo Codex's pointing and accent deviations in Job, lines 660–668 of that page, has no entry at 4:12.
2. **The Aleppo Codex has two strokes, one under the mem and one under the he: established at the resolution of the tracked photograph, and Ben's reading of mgketer.org's image of Job 4, 2026-09-10.** Section 3.
3. **The Leningrad Codex has two strokes, one under the mem and one under the he, as UXLC 3.9 and WLC record: Ben's reading of an image of the Codex, 2026-09-10.** Sections 2 and 3.
4. **The photograph of Cambridge University Library MS Add. 1753 shows two strokes, one under the mem and one under the he: established at the resolution of the derived page image.** Section 3.
5. **mgketer's transcription of Mikra'ot Gedolot ha-Keter records both U+05BD: established.** Section 2.
6. **Koren has only the U+05BD on the mem: Ben's reading, 2026-09-10, on its page D3-Jb-118.** Koren's text is not on disk, so the reading is Ben's alone. Ben also reported Koren's simple sheva under the nun as silent (`in/meteg_after_silluq_koren_readings.json`).
7. **The Simanim Tanakh has both U+05BD, on the mem and on the he, and its simple sheva under the nun is silent: Ben's reading, 2026-09-10, on its page 1172.** Its base text is the Aleppo Codex (`doc/simanim-tanakh-signs.md`, ma'ala 1). It prints a vocal sheva as two enlarged squares and a silent one as two small round dots (ma'ala 7), so on the sheva it agrees with Koren and with Phonetic MAM. It also supplies metegs the manuscripts omit, chiefly before a vocal sheva and before a hataf (ma'ala 12); neither of its two marks here stands before either. Having both marks, it does not bear on which one is the silluq.
8. **Phonetic MAM stresses the last syllable, which it does by construction and which therefore decides nothing.** Its `jta` for the atom is `men.!hu`. It takes the last U+05BD of every verse-final chanted word as the silluq (`doc/meteg-after-silluq-koren-lookup-candidates.md`, figure 7 of its section on the figures).
9. **The evidence on disk favours penultimate stress, which makes the U+05BD on the he a meteg after the silluq, as at 1 Kings 7:37: favoured, not proven, and raised for Ben in section 4.** Koren, at this verse and at Psalms 72:15, the Simanim Tanakh at Psalms 72:15, and MAM's parallels with the same suffix favour it. Against it there is only that Yeivin and Breuer both describe, in other words, a meteg of the shape the U+05BD on the mem would have if the stress were on the last syllable.
10. **Neither Yeivin nor Breuer mentions Job 4:12, this form, or where the stress of its suffix falls: not found.** Section 5.
11. **In both codices the stroke under the mem stands to the right of its segol, a placement that Yeivin says both use only in very few exceptions: Ben's reading, 2026-09-10.** Ben finds the agreement unlikely to be chance, but nobody knows how to interpret it, or whether it should be interpreted at all, so it leaves item 9's disposition as it was (section 4); section 5 has Yeivin's statement.

## 2. What each transcription and edition has at Job 4:12

| Text | Form | Its U+05BD | Where |
| --- | --- | --- | --- |
| MAM | מֶֽנְהֽוּ׃ | on the mem and on the he | `in/mam-ws/D3-Job.json` line 123; MAM-parsed plus and MAM-simple as in section 1 |
| UXLC 3.9 | מֽ͏ֶנְהֽוּ׃ | on the mem and on the he | `in/UXLC-39/Job.xml` line 1816 |
| WLC 4.22 and WLC 4.20 | the same letters and marks as UXLC 3.9's form, without its U+034F | on the mem and on the he | line 1242 of `out/wlc422-u/1verses_09_jbpr.json` and of `out/wlc420-u/1verses_09_jbpr.json` |
| mgketer (Mikra'ot Gedolot ha-Keter) | מֶֽנְהֽוּ | on the mem and on the he | `C:/Users/BenDe/GitRepos/MAM-private/mgketer/out/D3-Job/mgketer-json-massaged/D3-Job_04.json` line 445; the unmassaged token, line 457 of `chapters-json-phase-2/D3-Job_04.json`, has the same marks |
| Koren | מֶֽנְהוּ׃ | on the mem only | Ben, 2026-09-10, page D3-Jb-118; the form is the "First mark only" cell of rank 3 in `doc/meteg-after-silluq-koren-lookup-candidates.md` |
| The Simanim Tanakh | not shown: Ben's report names the marks, not the whole pointing | on the mem and on the he | Ben, 2026-09-10, page 1172; its simple sheva under the nun is silent |

UXLC's form has U+034F COMBINING GRAPHEME JOINER between the meteg and the segol on the mem, which is UXLC's coding of what its header calls a leading meteg (`uxlc/in/UXLC-rest/TanachHeader.xml` line 939); the WLC conversions have the meteg ahead of the segol with no joiner. Where a meteg stands relative to its vowel is taken up in section 4. Every transcription has MAM's two letter positions, so under the definitions of the screen of MAM against UXLC, WLC and mgketer (`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md`) Job 4:12 falls in its class (i) against all four, which is why that screen lists it nowhere. This is Claude's inference from the forms, not a figure the screen reports. The pages are named as in the scan-pages index (`doc/scan-pages.md`): Koren's page D3-Jb-118 is the file `D3-Jb-118.jpg` in `in/scan-pages/koren.json`, and the Simanim Tanakh's page 1172 is `D3-Jb-1172.jpg` in `in/scan-pages/simanim-tanakh.json`; both are body pages of Job there.

## 3. The manuscript photographs: the Aleppo Codex, Cambridge Add. 1753 and the Leningrad Codex each have two strokes

The Aleppo Codex's Job leaves are tracked at `aleppo/aleppo-pages/` as the Internet Archive's scale=2 JPEGs (`aleppo/aleppo-pages-provenance.md`), about 1,650 × 1,955 pixels a page, so a stroke is two or three pixels wide. Job 4:12 fills line 5 of column 2, the left column, of leaf 271r (`aleppo/line-breaks/271r.json` lines 814–836), and its verse-final atom ends that line; the column geometry is `aleppo/column-coordinates/271r.json`.

1. **The Aleppo Codex, leaf 271r, column 2, line 5: two strokes, one under the mem and one under the he.** Under the atom, from right to left: a stroke at about x 268 and the mem's segol at about x 256–262; the nun's sheva at about x 237; a stroke at about x 219, under the he. Positions are pixel columns of `271r.jpg`, read off a ruler to about two pixels. Ben read the same two strokes, with the one under the mem to the right of its segol, in his crop of 2026-09-10 from mgketer.org's image of Job 4, `aleppo/page-snips/271r-col2-line5-Job4v12-menhu.png`.

Cambridge Add. 1753 is the manuscript MAM's sigla call `כתי"ק-מ` (`in/mam-ws-intro/appendices.mediawiki` lines 100 and 171). That appendix describes it as a Yemenite manuscript of the Writings, of an estimated sixteenth-century date, close to the Tiberian Masorah and to the Aleppo Codex's text. Its page 0073B is derived, and gitignored, from the tracked spreads under `cam1753/cam1753-spreads/`; the image read was the primary clone's `cam1753/cam1753-pages/0073B.jpg`, 2,312 × 3,040 pixels. Job 4:12's last three atoms open line 13 of column 2 (`cam1753/cam1753-line-breaks/0073B.json` lines 909–919).

2. **Cambridge Add. 1753, page 0073B, column 2, line 13: two strokes, one under the mem and one under the he.** Under the atom, from right to left: the mem's segol at about x 605–620 and a stroke at about x 600; the nun's sheva at about x 586; a stroke at about x 569, under the he.

The Leningrad Codex's folio 398A has Job 3:14–5:9 (`uxlc/data/lci_augrecs.json`, the record at line 15754). Sefaria's image of the folio is `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F398A.jpg`, and tanach.us's page for the verse is `https://tanach.us/Tanach.xml?Job4:12`. The atom-location estimator (`page_and_guesses` in `py/py_uxlc/my_uxlc_location.py`) puts the verse-final atom, the verse's seventh, at column 2, line 4.0; the column and line have not been read off the image.

3. **The Leningrad Codex, folio 398A: two strokes, one under the mem and one under the he.** Ben's reading, 2026-09-10, from an image of the folio; his crop is `leningrad/page-snips/398A-Job4v12-menhu.png`. The stroke under the mem stands to the right of its segol, as in the Aleppo Codex, and UXLC records it as a leading meteg. Ben also sees signs of a possible erasure after the segol and around the stroke under the he.

## 4. Which U+05BD is the silluq: the evidence for each stress

### Penultimate stress, which makes the U+05BD on the he a meteg after the silluq

The syllables are then those of 1 Kings 7:37, לְכֻלָּֽהְנָֽה׃: a stressed closed syllable, then an open last syllable with a long vowel, and the meteg on that last syllable.

1. **Koren has only the U+05BD on the mem** (Ben, 2026-09-10). On Ben's premise that Koren never has a meteg after the silluq, that one mark is Koren's silluq, on the mem.
2. **In MAM's parallels, the stress is on the syllable before the suffix.**

| Reference | Verse | MAM-simple's form | What marks the stress | Phonetic MAM's `jta` |
| --- | --- | --- | --- | --- |
| Psalms 72:15 | poetic, verse-final | יְבָרְכֶֽנְהוּ׃ | the U+05BD on the kaf, its only one | `y^.va.r^.!khen.hu` |
| Jeremiah 5:22 | prose, mid-verse | יַעַבְרֶ֑נְהוּ | the atnach on the resh | `ya.`av.!ren.hu` |
| Jeremiah 5:22 | prose, verse-final | יַעַבְרֻֽנְהוּ׃ | the U+05BD on the resh, its only one | `ya.`av.!run.hu` |
| Psalms 68:24 | poetic, verse-final | מִנֵּֽהוּ׃ | the U+05BD on the nun, its only one | `min.!nE.hu` |

Psalms 72:15 and Jeremiah 5:22's mid-verse atom have the same last three letters and points as Job 4:12's atom, with a segol before them as there; the mid-verse atom is the example that `doc/meteg-after-silluq-koren-lookup-candidates.md` gives for Job 4:12's twin evidence, "no exact twin; suffix-3 2: first 2". Jeremiah 5:22's verse-final atom has the same last three letters and points with a qubuts before them. Psalms 68:24 has the same preposition with the same suffix, pointed differently. In all four rows MAM marks the stress on the syllable before the suffix, and Phonetic MAM's `jta` puts it there too. At Psalms 72:15 MAM's source also has a varika on the resh, which MAM-simple's form lacks (`in/mam-ws/D1-Psalms.json` line 2148). Koren at Psalms 72:15 has a U+05BD on the bet and on the kaf and none on the he, which Ben reads as a meteg and then the silluq, the stress penultimate (Ben, 2026-09-10, Koren's page D1-Ps-038; `doc/meteg-after-silluq-psalms-72-15.md`). The Simanim Tanakh has its two marks in the same places there (its page 1053). This is Claude's argument from MAM's parallels; no grammar on disk states the stress of Job 4:12's form (section 5).

3. **The Leningrad Codex has the same two-mark shape at Psalms 72:15, יְבָרֲכֶֽנְהֽוּ׃ as UXLC 3.9 and WLC record it; Ben confirmed both strokes from its image on 2026-09-10 (`doc/meteg-after-silluq-psalms-72-15.md`).** The screen of MAM against UXLC and WLC (`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md`, section 4) classed that as a U+05BD recorded after the silluq that MAM lacks. MAM's note there quotes the Aleppo Codex as יְבָרֲכֶֽנְהוּ, with the U+05BD on the kaf only (`in/mam-ws/D1-Psalms.json` line 2148; the note is about the hataf), and Ben confirmed from the Codex itself on 2026-09-10 that it has that one stroke. At Jeremiah 5:22's verse end UXLC 3.9 records יַעַבְרֻֽנְהוּ׃, with no U+05BD on the he (`in/UXLC-39/Jeremiah.xml` line 3006).
4. **The U+05BD on the he would be Breuer's type j**, the ga'aya of a big vowel in an open syllable at the end of a cantillated word. Breuer names 1 Kings 7:37 as its one occurrence in a word with a mafsik (CoS chapter 8 §46 note [^81]; `doc/meteg-after-silluq-search-in-mam-documentation.md`, finding 4).

### Stress on the last syllable, which makes the U+05BD on the mem a meteg before the silluq

The meteg is then on a short vowel in a closed syllable immediately before the stressed syllable, and that syllable begins with a guttural, the he.

1. **Both books describe such a meteg, in other words.** Breuer's irregular heavy ga'aya can stand on the first syllable before the accent, and he takes its cause to be phonetic where the next syllable begins with a guttural, a labial or a soft bgdkpt letter (CoS chapter 8 §25). Yeivin's phonetic gaʿya includes a short vowel before a syllable beginning with a guttural (ITM §350), and he counts about 60 closed-syllable gaʿyas immediately before the accent (§324). Against it: Yeivin calls such a closed syllable generally unsuitable for gaʿya in the poetic system (§374), and Breuer's poetic-system section puts a first-before-the-accent irregular heavy ga'aya mostly in a merkha word serving revia' mugrash, naming no siluk word (CoS chapter 14 §8c).
2. **Breuer's note names only 1 Kings 7:37.** If his editions have both strokes at Job 4:12, the note did not count the one on the he as a type-j ga'aya after the siluk, which it would be under penultimate stress. This is Claude's inference; his editions were not consulted.
3. **Phonetic MAM's stress on the last syllable is no evidence**, since it follows by construction (section 1, item 8).

### Stroke position: the argument from it is withdrawn, and the two codices' agreement on it leaves the disposition as it was

The first version of this file, `6e1d4164`, argued for stress on the last syllable from where the strokes stand. In the Aleppo Codex's photograph the stroke under the mem is to the right of the segol, as is the meteg that MAM's note at Job 8:3 records as right-side, while the silluq on a segol stands to the segol's left at Job 4:6, 5:1 and 8:3; and UXLC codes the Leningrad Codex's stroke on the mem as a leading meteg. That argument is withdrawn on Ben's judgment of 2026-09-10: BHS's editors thought a meteg's position relative to its vowel likely enough to be meaningful that they reproduced it throughout the Bible, and later scholars are, as far as he knows, agreed that this was a waste of effort and a misleading suggestion of meaning. MAM's introduction says of the Leningrad Codex that the right-side position has no significance (`in/mam-ws-intro/ch3.mediawiki` line 1371, section `געיה ימנית`), and `uxlc/doc/clc-design.md` §7.13 leaves meteg position unencoded. Do not re-propose a survey or calibration of stroke positions unless Ben asks for one.

Later the same day Ben read both codices at this verse (section 3). In the Aleppo Codex the stroke under the mem stands to the right of its segol exactly as in the Leningrad Codex, and he finds it unlikely that scribal whim coincided here by chance. The placement was visible before his reading, in the tracked photograph of the Aleppo Codex (section 3, item 1) and in UXLC's leading meteg, and the withdrawn argument above was built on both; his reading confirmed it from the two codices. He calls such a stroke an early metsil, metsil being his shorthand for meteg/silluq, because at this word whether it is a meteg or a silluq is exactly what is in question. His impression had been that an early metsil is commoner in the Leningrad Codex, though he suspects that he sees it there more only because BHS and the editions close to it, UXLC among them, keep it. The sources on disk bear on that as follows.

1. **Yeivin says both codices keep a gaʿya to the left of a vowel under the same letter, with very few exceptions, which he puts down mostly to correction or to lack of space in the usual position; C, S and S1, in his sigla, often have it to the right for no particular reason** (ITM §314; section 5, item 7). The possible erasure Ben sees in the Leningrad Codex fits the first of those two causes. Against the second, at Psalms 72:15, where a kaf with a segol and a stroke stands before a nun with a sheva as the mem does here, UXLC 3.9 records the Leningrad Codex's stroke after the segol, with no leading meteg. Both are Claude's observations.
2. **MAM's introduction says the Leningrad Codex has a meteg to the right of its vowel in dozens of places, most of them in the first part of Genesis, and that the placement has no meaning** (`in/mam-ws-intro/ch3.mediawiki` line 1371, the section `געיה ימנית`). MAM puts every meteg to the left, and where the Aleppo Codex is missing it records the Leningrad Codex's right-side meteg in a note. Of the 259 verses whose notes in MAM's source name a right-side meteg, 228 are in the Torah, and 3 name the Aleppo Codex, Job 8:3 among them; Job 4:12's atom has no note. The introduction's source for where a meteg stands is Yeivin's study of the Aleppo Codex (section 6).
3. **UXLC 3.9 records a leading meteg in 727 atoms, 243 of them in Genesis and 10 in Job, out of the 40,709 atoms with a U+05BD.** A leading meteg is counted here as a U+05BD U+034F with no vowel between its letter and it and a vowel after it. UXLC has U+05BD U+034F in 146 further atoms, 144 forms of Jerusalem and the Decalogue's פני at Exodus 20:3 and Deuteronomy 5:7, where the U+034F comes before a second vowel on the same letter; UXLC's header names Jerusalem and the Decalogue beside leading metegs as the U+034F's uses (`uxlc/in/UXLC-rest/TanachHeader.xml` line 939). By the vowel after it, the 727 are patah 412, qamats 184, segol 59, tsere 37, hiriq 28, sheva 4, hataf patah 2 and qubuts 1. 623 are on the atom's first letter, among them 371 of the 412 on a patah, the letter being a vav 157 times, a he 69 times and a lamed 33 times, and 52 of the 59 on a segol, Job 4:12's mem among them. In 31 verse-final atoms the leading meteg is the atom's last U+05BD, so in UXLC's record a silluq, 29 of them in Psalms, Proverbs and Job and two on a segol, at Job 7:9 and Proverbs 22:7 (the table below); in 50, Job 4:12 among them, it stands before another U+05BD. No transcription on disk records where the Aleppo Codex puts a meteg, so there is no count to set beside these, which fits Ben's suspicion that he sees the Leningrad Codex's more because the editions keep them. This is Claude's inference.

The 31 verse-final atoms whose leading meteg is their last U+05BD, and so in UXLC's record an early silluq, are these. Ben, 2026-09-10: "I find those observations pretty interesting and pretty relevant to our Job 4:12 word." They show that in UXLC's record of the Leningrad Codex an early stroke can be the silluq: three times in Job, and twice on a segol, once of those at Job 7:9. So the early position of Job 4:12's stroke on the mem does not mark it as a meteg rather than a silluq; this is Claude's observation.

| Reference | UXLC 3.9's form | Vowel after the leading meteg |
| --- | --- | --- |
| 1 Samuel 15:22 | אֵילֽ͏ִים׃ | hiriq |
| Isaiah 33:15 | בְּרֽ͏ָע׃ | qamats |
| Psalms 7:10 | צַדּֽ͏ִיק׃ | hiriq |
| Psalms 9:13 | עֲנָוֽ͏ִים׃ | hiriq |
| Psalms 10:1 | בַּצָּרֽ͏ָה׃ | qamats |
| Psalms 10:12 | עֲנָוֽ͏ִים׃ | hiriq |
| Psalms 16:6 | עָלֽ͏ָי׃ | qamats |
| Psalms 17:12 | בְּמִסְתָּרֽ͏ִים׃ | hiriq |
| Psalms 18:10 | רַגְלֽ͏ָיו׃ | qamats |
| Psalms 49:5 | חִידָתֽ͏ִי׃ | hiriq |
| Psalms 57:1 | בַּמְּעָרֽ͏ָה׃ | qamats |
| Psalms 68:10 | כֽוֹנַנְתּֽ͏ָהּ׃ | qamats |
| Psalms 83:7 | וְהַגְרֽ͏ִים׃ | hiriq |
| Psalms 86:13 | תַּחְתִּיּֽ͏ָה׃ | qamats |
| Psalms 95:9 | פָעֳלֽ͏ִי׃ | hiriq |
| Psalms 137:5 | יְמִינֽ͏ִי׃ | hiriq |
| Psalms 137:6 | שִׂמְחָתֽ͏ִי׃ | hiriq |
| Psalms 142:8 | עָלֽ͏ָי׃ | qamats |
| Psalms 148:12 | נְעָרֽ͏ִים׃ | hiriq |
| Proverbs 5:6 | תֵדֽ͏ָע׃ | qamats |
| Proverbs 5:10 | נָכְרֽ͏ִי׃ | hiriq |
| Proverbs 7:22 | אֱוֽ͏ִיל׃ | hiriq |
| Proverbs 12:10 | אַכְזָרֽ͏ִי׃ | hiriq |
| Proverbs 14:32 | צַדּֽ͏ִיק׃ | hiriq |
| Proverbs 18:12 | עֲנָוֽ͏ָה׃ | qamats |
| Proverbs 22:7 | מַלְוֽ͏ֶה׃ | segol |
| Proverbs 25:19 | צָרֽ͏ָה׃ | qamats |
| Proverbs 29:13 | יְהוֽ͏ָה׃ | qamats |
| Job 7:9 | יַעֲלֽ͏ֶה׃ | segol |
| Job 29:19 | בִּקְצִירֽ͏ִי׃ | hiriq |
| Job 31:5 | רַגְלֽ͏ִי׃ | hiriq |

Ben's view, the same day: that the two codices agree on both strokes was expected, since MAM, which follows the Aleppo Codex's metegs, has both, and UXLC and WLC record both for the Leningrad Codex. The only surprising information is that they agree on the earliness of the first stroke, and nobody knows how to interpret that, or whether it should be interpreted at all. It therefore leaves the disposition below as it was.

### Disposition: penultimate stress favoured, not proven

With stroke position set aside, the evidence on disk for penultimate stress is Koren, at this verse and at Psalms 72:15, the Simanim Tanakh at Psalms 72:15, and MAM's parallels. For stress on the last syllable there remain only a meteg type both books describe in other words, and Breuer's silence, which is Claude's inference from a note about 1 Kings 7:37. Nothing on disk states the stress of this form. If the stress is penultimate, Job 4:12 is a second verse-final chanted word in MAM with a meteg after the silluq, and the Aleppo Codex has both strokes, as MAM's meteg policy implies and its photograph shows. Section 6 lists what would bear on the question. The two codices' agreement on the early metsil leaves this disposition as it was, for the reason the subsection above gives.

## 5. Yeivin and Breuer: nothing on this word, the closed-syllable meteg in both, and Yeivin on where a gaʿya stands

A background search of both books' OCR exports, made for this file, found the following. Paths are relative to `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/` for ITM and `.../books/cos/md-export-of-docx/` for CoS; all 53 ITM files and all 57 CoS files were searched.

1. **Job 4:12 is cited in neither book: not found.** Patterns `\bJ(?:ob|b)\.?\s*4\s*[:.,;]\s*12\b|\b4\s*[:.,;]\s*12\s*\.?\s*J(?:ob|b)\b` (case-insensitive) and the book name `איוב` found nothing at 4:12; the four hits in Job chapter 4 are at 4:1 and 4:2.
2. **The letters מנהו in Job 4:12's sense occur in neither book: not found.** The pattern with any marks between the letters found only three Aramaic words in ITM Masoretic notes (`N0131.md` lines 1281 and 1397, `N0127.md` line 36).
3. **Neither book says where the stress of this form or of the energic suffix falls: not found.** Patterns `energ|paragog|epenthe`, Jeremiah 5:22 in either citation order, and word-final נהו found nothing on stress; Psalms 72:15 is cited once, in CoS chapter 10 §4 (`C10-S001.md` line 365), as an unpointed verse-division example.
4. **Neither book describes a ga'aya after the siluk in a verse-final chanted word of the poetic system: not found.** CoS chapter 14 §8 (`C14-S001.md` lines 285–307), on the poetic system's ga'aya, names five types in which it differs from the 21 books, and the type-j ga'aya is not among them. ITM §§358–374 (pp. 264–274) have nothing on a gaʿya after the silluq, and §359 says nothing of a second mark in the silluq's chanted word.
5. **Both describe the closed-syllable meteg immediately before the stress: found.** CoS chapter 8 §21 (`C08-S021.md` lines 3 and 25) defines the irregular heavy ga'aya; §25 (lines 179–203) gives it on the first syllable before the accent, with 1 Samuel 5:12 and 2 Samuel 22:2 among the examples; chapter 14 §8c (`C14-S001.md` lines 297–301) is the poetic system. ITM §319 and §324 (`N0309.md` lines 199–200 and 323–370, pp. 244 and 247), §345 and §350 (`N0345.md` lines 1–4 and 115–122, pp. 257–260) and §374 (`N0374.md` lines 1–20, pp. 273–274). The ITM OCR drops the examples of §324's class immediately before the accent.
6. **Two ga'yas in one chanted word, in both books, are examples from prose verses before the accent: found, and not this case.** ITM §§339–341, §356 and §210; CoS chapter 8 §21 says the irregular heavy ga'aya occurs only once in a word.
7. **Yeivin says where a gaʿya stands relative to its vowel, and Breuer does not: found in ITM, not found in CoS.** This item comes from a second search, made later the same day. ITM §314 (`N0309.md` lines 148–150, p. 241): a gaʿya is generally written to the left of a vowel under the same letter; A and L keep to this carefully, with very few exceptions, mostly from correction or from lack of space in the usual position, while C, S and S1 often have it to the right for no particular reason; with a sheva too the gaʿya is generally to its left, though some manuscripts often put it to the right. §313 (the same file, line 141) is about the stroke's slant, not its position. In CoS, `ga'?aya` within 200 characters of `right` or `left`, and `(right|left) of the (vowel|letter|point)`, found nothing on where a ga'aya stands; chapter 8 §1 leaves the optional ga'ayas to each naqdan's discretion (`C08-S001.md` lines 27–33), which is about which syllables have one, not where its stroke stands.

## 6. Not consulted, and what would bear on the question

1. **Breuer's editions**, the Horev edition and the Jerusalem Crown, at Job 4:12: not on disk. MAM's introduction says Breuer prints the ga'ayot written in the manuscripts as long ga'ayot, to distinguish them (`in/mam-ws-intro/ch3.mediawiki` line 1328). If his print makes one of the two strokes a long ga'aya, that would show which stroke he read as the silluq.
2. **Yeivin's study of the Aleppo Codex**, *כתר ארם צובה: ניקודו וטעמיו* (Jerusalem: Magnes, 5729; `in/mam-ws-intro/appendices.mediawiki` line 234), which MAM's introduction cites, chapter 11.3, pages 90–91, for where a meteg is written (`in/mam-ws-intro/ch3.mediawiki` line 1371): not on disk. It may say how often the Aleppo Codex has a meteg to the right of its vowel, which bears on Ben's question whether the placement is commoner in the Leningrad Codex.
3. **`doc/PLAN-silluq-before-gaya-template.md`** (phonetic-hbo#78) plans a template identifying the silluq at 1 Kings 7:37. Job 4:12 would be a candidate for it if its stress is penultimate. Raised for Ben, not acted on.

## 7. How the figures were made

The scripts below are throwaway scripts, which are not tracked; each wrote its Hebrew to a file, not to stdout.

1. One spelled out the atom with the letters מנהו, Job 4:12's and Psalms 68:24's, codepoint by codepoint in every source above and in Phonetic MAM, and another did the same for Psalms 72:15's atom.
2. Three made the crops and ruled enlargements of section 3. The crops kept in the repository are under `aleppo/page-snips/` and `leningrad/page-snips/`.
3. One wrote this file from a template, lifting every pointed form and every `jta` from the data with a uniqueness assertion, and checked the result with `has_std_mark_order`.
4. One estimated the Leningrad Codex's column and line for the verse-final atom and built the links of section 3. The tracked `py/main_verse_links.py` builds links of the same kinds.
5. The counts of MAM's notes in section 4's subsection on stroke position are ripgrep line counts (the Grep tool's count mode) over `in/mam-ws/*.json`, which has a line per verse: `בגעיה ימנית|געיה ימנית`, and `א[?!]*=ב?געיה ימנית` for the notes naming the Aleppo Codex. The counts of UXLC 3.9's leading metegs came from one more script, which listed every verse-final atom that section 4's item 3 counts and made section 4's table of the 31 early silluqs, lifted from `in/UXLC-39/*.xml` and put into MAM-normal mark order with `give_std_mark_order`.

The literature search of section 5 ran as a throwaway script in the session's scratchpad, which does not outlast the session; the patterns in section 5 are its durable record.
