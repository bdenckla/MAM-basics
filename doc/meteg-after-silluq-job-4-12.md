# Meteg after silluq at Job 4:12: what the repositories hold

Written 2026-09-10 by a Claude session in the MAM-basics worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c`, on the branch `claude/interesting-taussig-6aa52b`, starting from its head `683a3a31`. That head contains `5e61a2d1`, the commit recording Ben's Koren reading of Job 4:12, and does not contain `7d0888b3`, the head of `main` that day. Ben's instruction, 2026-09-10, was to investigate further "the one case that seems to have turned up a possible additional case of meteg after silluq (beyond the known 1 Kings 7:37 case ...)". That case is Job 4:12, rank 3 in `doc/meteg-after-silluq-koren-lookup-candidates.md`, where Ben found that the Koren edition has only one of MAM's two U+05BD, the one on the mem (`in/meteg_after_silluq_koren_readings.json`). The prompt that started this session, written by the Claude session running the Koren lookups, asked it to establish what the repositories already hold about this chanted word and to report that to Ben before doing anything further. Everything below is this session's account of the data, and each interpretive step says so. Revised the same day: the first version, `6e1d4164`, argued from where a meteg stroke stands relative to its vowel, and that argument is withdrawn (section 4).

Terms. An **atom** is one written word between spaces or maqafs; a **chanted word** is a lone atom or a whole maqaf compound. The verse-final chanted word of Job 4:12 is the lone atom מֶֽנְהֽוּ׃ and the verse, as MAM-simple has it, is וְ֭אֵלַי דָּבָ֣ר יְגֻנָּ֑ב וַתִּקַּ֥ח אׇ֝זְנִ֗י שֵׁ֣מֶץ מֶֽנְהֽוּ׃ In this file's voice **meteg** is U+05BD, and **silluq** is the U+05BD on the stressed syllable of a verse-final chanted word, so which of this atom's two U+05BD is the silluq depends on where its stress is. A **stroke** is a short vertical mark under a letter in a photograph of a manuscript; in these manuscripts a meteg and a silluq have the same shape. Yeivin's gaʿya and Breuer's ga'aya are this file's meteg, and their silluq and siluk are its silluq; each book's term is kept where the book is reported.

## 1. Summary: every text consulted but Koren has both U+05BD, and the evidence on disk favours penultimate stress

1. **MAM has both U+05BD with no note on the atom, and the Aleppo Codex is their source: established.** MAM's source line, `in/mam-ws/D3-Job.json` line 123, has the atom as plain text; the verse's one template is a `מ:דחי` on its first atom. MAM-parsed plus (`MAM-parsed/plus/D3-Job.json` line 1191) and MAM-simple (`MAM-simple/xml-vtrad-mam/Job.xml` line 140) have the same atom. MAM copies the meteg as the Aleppo Codex has it wherever that manuscript survives (`in/mam-ws-intro/ch3.mediawiki` line 1328, the section `נוסח הגעיות במהדורתנו`), and Job survives in it in full (`in/mam-ws-intro/ch5.mediawiki` line 658). MAM's list of the Aleppo Codex's pointing and accent deviations in Job, lines 660–668 of that page, has no entry at 4:12.
2. **The photograph of the Aleppo Codex shows two strokes, one under the mem and one under the he: established at the resolution of the tracked image.** Section 3.
3. **UXLC 3.9 and WLC record both U+05BD: established for the transcriptions. The Leningrad Codex itself was not consulted.** Section 2.
4. **The photograph of Cambridge University Library MS Add. 1753 shows two strokes, one under the mem and one under the he: established at the resolution of the derived page image.** Section 3.
5. **mgketer's transcription of Mikra'ot Gedolot ha-Keter records both U+05BD: established.** Section 2.
6. **Koren has only the U+05BD on the mem: Ben's reading, 2026-09-10, on its page D3-Jb-118.** Koren's text is not on disk, so the reading is Ben's alone. Ben also reported Koren's simple sheva under the nun as silent (`in/meteg_after_silluq_koren_readings.json`).
7. **The Simanim Tanakh has both U+05BD, on the mem and on the he, and its simple sheva under the nun is silent: Ben's reading, 2026-09-10, on its page 1172.** Its base text is the Aleppo Codex (`doc/simanim-tanakh-signs.md`, ma'ala 1). It prints a vocal sheva as two enlarged squares and a silent one as two small round dots (ma'ala 7), so on the sheva it agrees with Koren and with Phonetic MAM. It also supplies metegs the manuscripts omit, chiefly before a vocal sheva and before a hataf (ma'ala 12); neither of its two marks here stands before either. Having both marks, it does not bear on which one is the silluq.
8. **Phonetic MAM stresses the last syllable, which it does by construction and which therefore decides nothing.** Its `jta` for the atom is `men.!hu`. It takes the last U+05BD of every verse-final chanted word as the silluq (`doc/meteg-after-silluq-koren-lookup-candidates.md`, figure 7 of its section on the figures).
9. **The evidence on disk favours penultimate stress, which makes the U+05BD on the he a meteg after the silluq, as at 1 Kings 7:37: favoured, not proven, and raised for Ben in section 4.** Koren, at this verse and at Psalms 72:15, the Simanim Tanakh at Psalms 72:15, and MAM's parallels with the same suffix favour it. Against it there is only that Yeivin and Breuer both describe, in other words, a meteg of the shape the U+05BD on the mem would have if the stress were on the last syllable.
10. **Neither Yeivin nor Breuer mentions Job 4:12, this form, or where the stress of its suffix falls: not found.** Section 5.

## 2. What each transcription and edition has at Job 4:12

| Text | Form | Its U+05BD | Where |
| --- | --- | --- | --- |
| MAM | מֶֽנְהֽוּ׃ | on the mem and on the he | `in/mam-ws/D3-Job.json` line 123; MAM-parsed plus and MAM-simple as in section 1 |
| UXLC 3.9 | מֽ͏ֶנְהֽוּ׃ | on the mem and on the he | `in/UXLC-39/Job.xml` line 1816 |
| WLC 4.22 and WLC 4.20 | the same letters and marks as UXLC 3.9's form, without its U+034F | on the mem and on the he | line 1242 of `out/wlc422-u/1verses_09_jbpr.json` and of `out/wlc420-u/1verses_09_jbpr.json` |
| mgketer (Mikra'ot Gedolot ha-Keter) | מֶֽנְהֽוּ | on the mem and on the he | `C:/Users/BenDe/GitRepos/MAM-private/mgketer/out/D3-Job/mgketer-json-massaged/D3-Job_04.json` line 445; the unmassaged token, line 457 of `chapters-json-phase-2/D3-Job_04.json`, has the same marks |
| Koren | מֶֽנְהוּ׃ | on the mem only | Ben, 2026-09-10, page D3-Jb-118; the form is the "First mark only" cell of rank 3 in `doc/meteg-after-silluq-koren-lookup-candidates.md` |
| The Simanim Tanakh | not shown: Ben's report names the marks, not the whole pointing | on the mem and on the he | Ben, 2026-09-10, page 1172; its simple sheva under the nun is silent |

UXLC's form has U+034F COMBINING GRAPHEME JOINER between the meteg and the segol on the mem, which is UXLC's coding of what its header calls a leading meteg (`uxlc/in/UXLC-rest/TanachHeader.xml` line 939); the WLC conversions have the meteg ahead of the segol with no joiner. Where a meteg stands relative to its vowel is not evidence here (section 4). Every transcription has MAM's two letter positions, so under the definitions of the screen of MAM against UXLC, WLC and mgketer (`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md`) Job 4:12 falls in its class (i) against all four, which is why that screen lists it nowhere. This is Claude's inference from the forms, not a figure the screen reports. The pages are named as in the scan-pages index (`doc/scan-pages.md`): Koren's page D3-Jb-118 is the file `D3-Jb-118.jpg` in `in/scan-pages/koren.json`, and the Simanim Tanakh's page 1172 is `D3-Jb-1172.jpg` in `in/scan-pages/simanim-tanakh.json`; both are body pages of Job there.

## 3. The manuscript photographs: the Aleppo Codex and Cambridge Add. 1753 each have two strokes

The Aleppo Codex's Job leaves are tracked at `aleppo/aleppo-pages/` as the Internet Archive's scale=2 JPEGs (`aleppo/aleppo-pages-provenance.md`), about 1,650 × 1,955 pixels a page, so a stroke is two or three pixels wide. Job 4:12 fills line 5 of column 2, the left column, of leaf 271r (`aleppo/line-breaks/271r.json` lines 814–836), and its verse-final atom ends that line; the column geometry is `aleppo/column-coordinates/271r.json`.

1. **The Aleppo Codex, leaf 271r, column 2, line 5: two strokes, one under the mem and one under the he.** Under the atom, from right to left: a stroke at about x 268 and the mem's segol at about x 256–262; the nun's sheva at about x 237; a stroke at about x 219, under the he. Positions are pixel columns of `271r.jpg`, read off a ruler to about two pixels.

Cambridge Add. 1753 is the manuscript MAM's sigla call `כתי"ק-מ` (`in/mam-ws-intro/appendices.mediawiki` lines 100 and 171). That appendix describes it as a Yemenite manuscript of the Writings, of an estimated sixteenth-century date, close to the Tiberian Masorah and to the Aleppo Codex's text. Its page 0073B is derived, and gitignored, from the tracked spreads under `cam1753/cam1753-spreads/`; the image read was the primary clone's `cam1753/cam1753-pages/0073B.jpg`, 2,312 × 3,040 pixels. Job 4:12's last three atoms open line 13 of column 2 (`cam1753/cam1753-line-breaks/0073B.json` lines 909–919).

2. **Cambridge Add. 1753, page 0073B, column 2, line 13: two strokes, one under the mem and one under the he.** Under the atom, from right to left: the mem's segol at about x 605–620 and a stroke at about x 600; the nun's sheva at about x 586; a stroke at about x 569, under the he.

**The Leningrad Codex was not consulted.** Its folio 398A has Job 3:14–5:9 (`uxlc/data/lci_augrecs.json`, the record at line 15754). No image of it is on disk; `doc/boj-leningrad-word-crops.md` gives Sefaria's URL pattern, which for this folio is `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F398A.jpg`.

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

3. **The Leningrad Codex has the same two-mark shape at Psalms 72:15, יְבָרֲכֶֽנְהֽוּ׃ as UXLC 3.9 and WLC record it; Ben confirmed both strokes from its image on 2026-09-10 (`doc/meteg-after-silluq-psalms-72-15.md`).** The screen of MAM against UXLC and WLC (`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md`, section 4) classed that as a U+05BD recorded after the silluq that MAM lacks. MAM's note there quotes the Aleppo Codex as יְבָרֲכֶֽנְהוּ, with the U+05BD on the kaf only (`in/mam-ws/D1-Psalms.json` line 2148; the note is about the hataf). At Jeremiah 5:22's verse end UXLC 3.9 records יַעַבְרֻֽנְהוּ׃, with no U+05BD on the he (`in/UXLC-39/Jeremiah.xml` line 3006).
4. **The U+05BD on the he would be Breuer's type j**, the ga'aya of a big vowel in an open syllable at the end of a cantillated word. Breuer names 1 Kings 7:37 as its one occurrence in a word with a mafsik (CoS chapter 8 §46 note [^81]; `doc/meteg-after-silluq-search-in-mam-documentation.md`, finding 4).

### Stress on the last syllable, which makes the U+05BD on the mem a meteg before the silluq

The meteg is then on a short vowel in a closed syllable immediately before the stressed syllable, and that syllable begins with a guttural, the he.

1. **Both books describe such a meteg, in other words.** Breuer's irregular heavy ga'aya can stand on the first syllable before the accent, and he takes its cause to be phonetic where the next syllable begins with a guttural, a labial or a soft bgdkpt letter (CoS chapter 8 §25). Yeivin's phonetic gaʿya includes a short vowel before a syllable beginning with a guttural (ITM §350), and he counts about 60 closed-syllable gaʿyas immediately before the accent (§324). Against it: Yeivin calls such a closed syllable generally unsuitable for gaʿya in the poetic system (§374), and Breuer's poetic-system section puts a first-before-the-accent irregular heavy ga'aya mostly in a merkha word serving revia' mugrash, naming no siluk word (CoS chapter 14 §8c).
2. **Breuer's note names only 1 Kings 7:37.** If his editions have both strokes at Job 4:12, the note did not count the one on the he as a type-j ga'aya after the siluk, which it would be under penultimate stress. This is Claude's inference; his editions were not consulted.
3. **Phonetic MAM's stress on the last syllable is no evidence**, since it follows by construction (section 1, item 8).

### Stroke position is not evidence, and the argument from it is withdrawn

The first version of this file, `6e1d4164`, argued for stress on the last syllable from where the strokes stand. In the Aleppo Codex's photograph the stroke under the mem is to the right of the segol, as is the meteg that MAM's note at Job 8:3 records as right-side, while the silluq on a segol stands to the segol's left at Job 4:6, 5:1 and 8:3; and UXLC codes the Leningrad Codex's stroke on the mem as a leading meteg. That argument is withdrawn on Ben's judgment of 2026-09-10: BHS's editors thought a meteg's position relative to its vowel likely enough to be meaningful that they reproduced it throughout the Bible, and later scholars are, as far as he knows, agreed that this was a waste of effort and a misleading suggestion of meaning. MAM's introduction says of the Leningrad Codex that the right-side position has no significance (`in/mam-ws-intro/ch3.mediawiki` line 1371, section `געיה ימנית`), and `uxlc/doc/clc-design.md` §7.13 leaves meteg position unencoded. A survey or calibration of stroke positions is not a route to which U+05BD is the silluq; do not re-propose one.

### Disposition: penultimate stress favoured, not proven

With stroke position set aside, the evidence on disk for penultimate stress is Koren, at this verse and at Psalms 72:15, the Simanim Tanakh at Psalms 72:15, and MAM's parallels. For stress on the last syllable there remain only a meteg type both books describe in other words, and Breuer's silence, which is Claude's inference from a note about 1 Kings 7:37. Nothing on disk states the stress of this form. If the stress is penultimate, Job 4:12 is a second verse-final chanted word in MAM with a meteg after the silluq, and the Aleppo Codex has both strokes, as MAM's meteg policy implies and its photograph shows. Section 6 lists what would bear on the question.

## 5. Yeivin and Breuer: nothing on this word, and the closed-syllable meteg in both

A background search of both books' OCR exports, made for this file, found the following. Paths are relative to `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/` for ITM and `.../books/cos/md-export-of-docx/` for CoS; all 53 ITM files and all 57 CoS files were searched.

1. **Job 4:12 is cited in neither book: not found.** Patterns `\bJ(?:ob|b)\.?\s*4\s*[:.,;]\s*12\b|\b4\s*[:.,;]\s*12\s*\.?\s*J(?:ob|b)\b` (case-insensitive) and the book name `איוב` found nothing at 4:12; the four hits in Job chapter 4 are at 4:1 and 4:2.
2. **The letters מנהו in Job 4:12's sense occur in neither book: not found.** The pattern with any marks between the letters found only three Aramaic words in ITM Masoretic notes (`N0131.md` lines 1281 and 1397, `N0127.md` line 36).
3. **Neither book says where the stress of this form or of the energic suffix falls: not found.** Patterns `energ|paragog|epenthe`, Jeremiah 5:22 in either citation order, and word-final נהו found nothing on stress; Psalms 72:15 is cited once, in CoS chapter 10 §4 (`C10-S001.md` line 365), as an unpointed verse-division example.
4. **Neither book describes a ga'aya after the siluk in a verse-final chanted word of the poetic system: not found.** CoS chapter 14 §8 (`C14-S001.md` lines 285–307), on the poetic system's ga'aya, names five types in which it differs from the 21 books, and the type-j ga'aya is not among them. ITM §§358–374 (pp. 264–274) have nothing on a gaʿya after the silluq, and §359 says nothing of a second mark in the silluq's chanted word.
5. **Both describe the closed-syllable meteg immediately before the stress: found.** CoS chapter 8 §21 (`C08-S021.md` lines 3 and 25) defines the irregular heavy ga'aya; §25 (lines 179–203) gives it on the first syllable before the accent, with 1 Samuel 5:12 and 2 Samuel 22:2 among the examples; chapter 14 §8c (`C14-S001.md` lines 297–301) is the poetic system. ITM §319 and §324 (`N0309.md` lines 199–200 and 323–370, pp. 244 and 247), §345 and §350 (`N0345.md` lines 1–4 and 115–122, pp. 257–260) and §374 (`N0374.md` lines 1–20, pp. 273–274). The ITM OCR drops the examples of §324's class immediately before the accent.
6. **Two ga'yas in one chanted word, in both books, are examples from prose verses before the accent: found, and not this case.** ITM §§339–341, §356 and §210; CoS chapter 8 §21 says the irregular heavy ga'aya occurs only once in a word.

## 6. Not consulted, and what would bear on the question

1. **Breuer's editions**, the Horev edition and the Jerusalem Crown, at Job 4:12: not on disk. MAM's introduction says Breuer prints the ga'ayot written in the manuscripts as long ga'ayot, to distinguish them (`in/mam-ws-intro/ch3.mediawiki` line 1328). If his print makes one of the two strokes a long ga'aya, that would show which stroke he read as the silluq.
2. **The Leningrad Codex, folio 398A**: Sefaria's image, `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F398A.jpg`, where the verse-final atom, the verse's seventh, is estimated at column 2, line 4.0 (`page_and_guesses` in `py/py_uxlc/my_uxlc_location.py`); tanach.us's page for the verse is `https://tanach.us/Tanach.xml?Job4:12`. It would turn UXLC's record of two strokes into a reading of the manuscript; it cannot show which stroke is the silluq.
3. **`doc/PLAN-silluq-before-gaya-template.md`** (phonetic-hbo#78) plans a template identifying the silluq at 1 Kings 7:37. Job 4:12 would be a candidate for it if its stress is penultimate. Raised for Ben, not acted on.

## 7. Scripts and commands that re-establish every figure

All are throwaway scripts, gitignored under `.novc/` in the worktree named at the top, run from its root on `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`; each writes its Hebrew to a file, not to stdout.

1. `.novc/job412_spell.py` spells out the atom with the letters מנהו, Job 4:12's and Psalms 68:24's, codepoint by codepoint in every source above and in Phonetic MAM, and writes `.novc/job412_spell_report.txt`.
2. `.novc/job412_spell2.py` does the same for Psalms 72:15's atom and writes `.novc/job412_spell2_report.txt`.
3. `.novc/job412_crops.py`, `.novc/job412_zoom.py` and `.novc/job412_cam_line.py` (the last with the arguments `550 1268 660 1372`) make the crops and ruled enlargements of section 3.
4. `.novc/job412_write_doc.py` writes this file from `.novc/job412_doc_template.md`, lifting every pointed form and every `jta` from the data with a uniqueness assertion, and checks the result with `has_std_mark_order`.
5. `.novc/lookup_links.py` estimates the Leningrad Codex's column and line for the verse-final atom and builds the links of section 6.

The literature search of section 5 ran as a throwaway script in the session's scratchpad, which does not outlast the session; the patterns in section 5 are its durable record.
