# Verse-final chanted words where UXLC 3.9 or WLC 4.22 records a U+05BD later than MAM's last

Written 2026-09-10 by `.novc/masuw_write_doc.py`, a throwaway script of a Claude session, from the JSON of the run this file reports, in the MAM-basics worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c` on the branch `claude/interesting-taussig-6aa52b`, whose head was `5f996d0e` when the run was made. The run is the one `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md` plans, and Ben's instruction of 2026-09-10 asked for it: "a more complete run for verse-final words in which UXLC or WLC (using a Unicode version of WLC) has a meteg/silluq later than MAM's last meteg/silluq on that word." Everything else here is that session's account of the data. Every pointed form below is lifted from the data by the script. The UXLC and WLC forms are shown in MAM's mark order (`uni_denorm.give_std_mark_order`), because `py/tests/test_prose_mark_order.py` requires that order of every tracked `.md`; the run compares letter positions, never bytes, so the reordering changes nothing it reports. No manuscript was consulted for this file, and a claim about the Leningrad Codex made from UXLC or WLC is written "UXLC 3.9 records" or "WLC 4.22 records".

Terms, as the `hebrew-prose` skill defines them: an **atom** is one written word between spaces or maqafs, and a **chanted word** is a lone atom or a whole maqaf compound. The **verse-final chanted word** is the last atom holding sof pasuq plus every atom maqaf-joined to it. **Meteg** is U+05BD, and **silluq** is the U+05BD on the stressed syllable of a verse-final chanted word. A **position** is a letter ordinal within the chanted word, maqafs not counted: position k means that the U+05BD is on the chanted word's k-th letter. **Syllables** are counted the Masoretic way, by Ben's definition of 2026-09-09: a full vowel opens a syllable, a furtive patah included, and a sheva or a hataf opens none and attaches to the syllable after it. **Phonetic MAM** is al-hatorah's `io/a01-phonetic-std-set` in `C:/Users/BenDe/GitRepos/MAM-private`, whose `jta` field has `!` before the stressed syllable, `.` between syllables and `-` between atoms. The **transcriptions** are UXLC 3.9, WLC 4.22 and WLC 4.20, each compared with MAM separately. A **hit** is Ben's criterion as the plan's step 3 states it: a verse-final chanted word whose last U+05BD in the transcription is at a later position than MAM's last U+05BD, or which has a U+05BD in the transcription and none in MAM.

## 1. Summary: 5 hits with a U+05BD after MAM's silluq, 2 with the silluq on another letter, and class 3 empty

Eight findings, each with its disposition first.

1. **7 hits against UXLC 3.9, 6 against WLC 4.22, and the same 6 against WLC 4.20: established.** Section 2 has the counts by pass and class.
2. **Class 1 has 5 members against UXLC 3.9 and 4 against WLC 4.22, and all of them have one shape: established.** They are 1 Samuel 17:5, 1 Kings 14:14 (against UXLC 3.9 only), Psalms 60:10, Psalms 70:2 and Psalms 72:15. In each, the transcription records MAM's last U+05BD and a later one: MAM's last U+05BD is on the chanted word's penultimate syllable, with one syllable after it, and the transcription's later U+05BD is on the last syllable. At 1 Kings 14:14 WLC 4.22 records MAM's one U+05BD, and UXLC added the second in its release 2022.12.07 (section 3).
3. **In each class 1 member MAM has one U+05BD, which is therefore MAM's silluq, so the transcription's later U+05BD is after MAM's silluq; these are the plan's candidates for a meteg after the silluq in the transcription: raised for Ben, whose reading of the Leningrad Codex decides each case.** Phonetic MAM stresses the syllable of MAM's U+05BD in all five, but it takes the last U+05BD of a verse-final chanted word as the silluq, so that agreement confirms the run's syllable count and is no evidence about the stress. Two of the five are already settled from an image of the Leningrad Codex, which has the second stroke at both: Psalms 72:15, read by Ben on 2026-09-10 (`doc/meteg-after-silluq-psalms-72-15.md`), and 1 Samuel 17:5, whose crop is on `gh-pages/post-stress-meteg-post-silluq.html`. Section 6 has the links for the other three, 1 Kings 14:14, Psalms 60:10 and Psalms 70:2.
4. **Psalms 60:10 is new, and only this run's supplementary aligned pass finds it: raised for Ben with the rest of class 1.** The plan's alignment skips the verse, as the screen did, because MAM has a holam male where UXLC 3.9 and WLC 4.22 record a holam on the resh, so the letters differ. Section 7 describes the pass, which has this one hit among the 121 verses it compares against each transcription.
5. **Class 2 has 2 members against each transcription, Judges 9:2 and Job 31:7, and neither has a U+05BD after the silluq: established from the forms.** At Judges 9:2 MAM has its one U+05BD on the alef, the penultimate syllable, where Phonetic MAM has the stress, and the transcriptions record their one U+05BD on the nun, the last syllable: the texts differ in which syllable has the silluq. At Job 31:7 they differ in the pointing: MAM has no vowel under the mem and a rafe on the alef, one syllable in Phonetic MAM, and the transcriptions record a qubuts under the mem, two syllables, with their one U+05BD on the second of them (section 4).
6. **Class 3 is empty: neither 1 Kings 7:37 nor Job 4:12 is a hit.** At 1 Kings 7:37 UXLC 3.9 and WLC 4.22 record one U+05BD, at position 3, before MAM's last, at position 5; at Job 4:12 they record MAM's two positions, 1 and 3 (section 5). No hit has a U+05BD in the transcription and none in MAM, and the final-atom pass has no hit.
7. **The plan's precondition holds: the screen's class (v) has 4 members against UXLC 3.9 and 3 against WLC 4.22, in the screen's report and in this run's recount.** On the whole pass class 1 is exactly the screen's class (v) (section 9, item 4). The recount differs from the screen's section 2 only in class (i), one lower, and class (vi), one higher, against each transcription, because MAM-simple changed at 2 Chronicles 26:15 between the two runs; that verse is not a hit either way (section 8).
8. **WLC 4.20 has the same 6 hits as WLC 4.22, with the same forms and positions: established.** The tables therefore give WLC 4.22 only.

## 2. Counts by pass and class

Each column is one comparison of MAM with one transcription, made by `.novc/masuw_run.py`. The passes are defined in section 9, item 3; the aligned pass is this run's addition to the plan.

| | UXLC 3.9 | WLC 4.22 | WLC 4.20 |
|---|---|---|---|
| verses on both sides | 23213 | 23213 | 23213 |
| verses not compared, Joshua 21:36 and 21:37, which MAM-simple has as a dash (the screen's section 7) | 2 | 2 | 2 |
| compared in the whole pass | 23066 | 23062 | 23062 |
| compared in the final-atom pass | 24 | 28 | 28 |
| compared in the aligned pass | 121 | 121 | 121 |
| class 1 hits in the whole pass | 4 | 3 | 3 |
| class 1 hits in the aligned pass | 1 | 1 | 1 |
| class 2 hits in the whole pass | 2 | 2 | 2 |
| class 2 hits in the aligned pass | 0 | 0 | 0 |
| hits in the final-atom pass | 0 | 0 | 0 |
| class 3 hits | 0 | 0 | 0 |
| hits with a U+05BD in the transcription and none in MAM | 0 | 0 | 0 |
| all hits | 7 | 6 | 6 |

## 3. Class 1: the transcription records MAM's last U+05BD and a later one

In the column of syllables after each U+05BD, "2: one after it" means that the U+05BD at position 2 has one syllable after the syllable it is in. The WLC 4.22 column gives WLC 4.22's form even where it is not a hit, and the positions column says so.

| Reference | Pass | MAM | UXLC 3.9 | WLC 4.22 | Positions | Syllables | Syllables after each U+05BD | Phonetic MAM's `jta` |
|---|---|---|---|---|---|---|---|---|
| 1 Samuel 17:5 | whole | נְחֹֽשֶׁת׃ | נְחֹֽשֶֽׁת׃ | נְחֹֽשֶֽׁת׃ | MAM 2; UXLC 2, 3; WLC 2, 3 | 2 | MAM 2: one after it; UXLC and WLC 2: one after it, 3: none after it | `n^.!xO.shet` |
| 1 Kings 14:14 | whole | גַּם־עָֽתָּה׃ | גַּם־עָֽתָּֽה׃ | גַּם־עָֽתָּה׃ | MAM 3; UXLC 3, 4; WLC 3, not a hit | 3 | MAM 3: one after it; UXLC 3: one after it, 4: none after it; WLC 3: one after it | `` gam-!`at.ta `` |
| Psalms 60:10 | aligned | הִתְרוֹעָֽעִי׃ | הִתְרֹעָֽעִֽי׃ | הִתְרֹעָֽעִֽי׃ | MAM 5; UXLC 4, 5; WLC 4, 5, counted in each text's letters (section 7) | 4 | MAM 5: one after it; UXLC and WLC 4: one after it, 5: none after it | `` hit.rO.!`a.`I `` |
| Psalms 70:2 | whole | חֽוּשָׁה׃ | חֽוּשָֽׁה׃ | חֽוּשָֽׁה׃ | MAM 1; UXLC 1, 3; WLC 1, 3 | 2 | MAM 1: one after it; UXLC and WLC 1: one after it, 3: none after it | `!xu.sha` |
| Psalms 72:15 | whole | יְבָרְכֶֽנְהוּ׃ | יְבָרֲכֶֽנְהֽוּ׃ | יְבָרֲכֶֽנְהֽוּ׃ | MAM 4; UXLC 4, 6; WLC 4, 6 | 3 | MAM 4: one after it; UXLC and WLC 4: one after it, 6: none after it | `y^.va.r^.!khen.hu` |

Four of the five have more on disk.

1. **1 Samuel 17:5 is the screen's calibration case, and the Leningrad Codex has the second stroke: established from an image.** The post-stress-meteg survey's page `gh-pages/post-stress-meteg-post-silluq.html` says that the Codex has a meteg after the silluq at this chanted word, with a crop of folio 159A, column 3, line 8.
2. **1 Kings 14:14 is a hit against UXLC 3.9 alone because UXLC added its second U+05BD: established from UXLC's change record.** Change 2022.08.31 - 17 of UXLC's release 2022.12.07 (`uxlc/in/UXLC-misc/2022.12.07 - Changes.xml`), from Daniel Holman, is "Add meteg under tav." It changes עָֽתָּה׃ to עָֽתָּֽה׃ and places the atom at folio 195B, column 2, line 27. Its notes say that BHL has the meteg only on the ayin, and include Ben's note "Breuer-DM reads the L as in the proposed change with an unexpected second meteg." WLC 4.22 and WLC 4.20 record MAM's one U+05BD, on the ayin.
3. **Psalms 60:10 is found by the aligned pass alone** (section 7): MAM's form has a vav after the resh that the transcriptions lack.
4. **Psalms 72:15 is settled for both codices: established from Ben's readings of their images, 2026-09-10.** The Leningrad Codex has both strokes and the Aleppo Codex has one, under the kaf (`doc/meteg-after-silluq-psalms-72-15.md`).

## 4. Class 2: the silluq on another letter, at Judges 9:2 and Job 31:7

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Positions | Syllables | Syllables after each U+05BD | Phonetic MAM's `jta` |
|---|---|---|---|---|---|---|---|
| Judges 9:2 | אָֽנִי׃ | אָנִֽי׃ | אָנִֽי׃ | MAM 1; UXLC 2; WLC 2 | 2 | MAM 1: one after it; UXLC and WLC 2: none after it | `!'a.nI` |
| Job 31:7 | מֽאֿוּם׃ | מֻאוּֽם׃ | מֻאֽוּם׃ | MAM 1; UXLC 3; WLC 2 | MAM 1; UXLC and WLC 2 | MAM 1: before the first syllable, by the letter walker; UXLC 3: none after it; WLC 2: none after it | `!mum` |

At Job 31:7 the letter walker the run uses, `ben_onsets`, puts MAM's U+05BD before the first syllable. It takes a shuruq's syllable to begin at the letter before the vav, which here is the alef; but MAM has a rafe on that alef, so the alef is silent and MAM's one syllable begins at the mem, where the U+05BD is. Phonetic MAM's `jta` has that one syllable, and the walker's count of one agrees with it. Job 31:7 is the one hit where Phonetic MAM's stress is not on the syllable the walker gives MAM's last U+05BD.

## 5. Class 3: 1 Kings 7:37 and Job 4:12, flagged, and neither a hit

Class 3 flags two verses whatever else holds. At neither is the transcriptions' last U+05BD later than MAM's last:

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Positions | Why it is flagged |
|---|---|---|---|---|---|
| 1 Kings 7:37 | לְכֻלָּֽהְנָֽה׃ | לְכֻלָּֽהְנָה׃ | לְכֻלָּֽהְנָה׃ | MAM 3, 5; UXLC 3; WLC 3 | MAM's last U+05BD is a meteg after the silluq (Ben's reading, 2026-09-09) |
| Job 4:12 | מֶֽנְהֽוּ׃ | מֽ͏ֶנְהֽוּ׃ | מֶֽנְהֽוּ׃ | MAM 1, 3; UXLC 1, 3; WLC 1, 3 | MAM's last U+05BD is a meteg after the silluq if the stress is penultimate (`doc/meteg-after-silluq-job-4-12.md`) |

## 6. Links for Ben's look at the Leningrad Codex: tanach.us and Sefaria's folio images

Built by `py/main_verse_links.py`, the user-level `verse-links` skill's command, which `.novc/masuw_links.py` runs with the UXLC's text of each verse-final atom. The folio comes from the UXLC's page index, and the column and line are interpolated from the atom count, so they are estimates; the skill records that both of the estimator's lines checked against an image so far put the atom lower on the page than it is. An atom number counts the UXLC's atoms. The two members already read from images are included, with where the atom was found.

| Reference | MAM's final atom | tanach.us | Sefaria's image of the folio | Where the atom is |
|---|---|---|---|---|
| 1 Samuel 17:5 | נְחֹֽשֶׁת׃ | [tanach.us](https://tanach.us/Tanach.xml?1Sam17:5) | [folio 159A](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F159A.jpg) | estimated at column 3, line 8.7 (atom 14 of 14); column 3, line 8 in the crop on `gh-pages/post-stress-meteg-post-silluq.html` |
| 1 Kings 14:14 | עָֽתָּה׃ | [tanach.us](https://tanach.us/Tanach.xml?1Kings14:14) | [folio 195B](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F195B.jpg) | estimated at column 3, line 1.9 (atom 16 of 16); column 2, line 27 in UXLC's change record 2022.08.31 - 17 |
| Psalms 60:10 | הִתְרוֹעָֽעִי׃ | [tanach.us](https://tanach.us/Tanach.xml?Ps60:10) | [folio 377B](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F377B.jpg) | estimated at column 1, line 6.9 (atom 10 of 10) |
| Psalms 70:2 | חֽוּשָׁה׃ | [tanach.us](https://tanach.us/Tanach.xml?Ps70:2) | [folio 379B](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F379B.jpg) | estimated at column 1, line 23.2 (atom 5 of 5) |
| Psalms 72:15 | יְבָרְכֶֽנְהוּ׃ | [tanach.us](https://tanach.us/Tanach.xml?Ps72:15) | [folio 380A](https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F380A.jpg) | estimated at column 2, line 5.5 (atom 11 of 11); column 2, line 3 in Ben's reading, 2026-09-10 (`doc/meteg-after-silluq-psalms-72-15.md`) |

## 7. The supplementary aligned pass: the 121 verses the plan's alignment skips, with one hit

The plan's step 2 skips a verse whose verse-final chanted words differ in letters, final atoms included, and counts it. There are 121 such verses against each transcription, the same 121 each time: the rows of the screen's section 13 marked skipped, which its section 7 describes as nearly all a ketiv and qere, a plene against a defective spelling, or a compound name that is one atom in MAM and two in the transcription. Ben's criterion covers every verse-final chanted word, so this run compares those verses too and reports them apart: difflib aligns the two chanted words' letters, and the transcription's last U+05BD is placed among MAM's letters through that alignment. Against each transcription, in all 121 verses, both the letter with the transcription's last U+05BD and the letter with MAM's last U+05BD are letters the alignment pairs, so no placement fell between two letters.

One of the 121 is a hit, Psalms 60:10, where MAM has הִתְרוֹעָֽעִי׃ and UXLC 3.9 and WLC 4.22 record הִתְרֹעָֽעִֽי׃. MAM's vav after the resh has no partner, so MAM's position 5, the first ayin, pairs with the transcriptions' position 4, and their position 5, the second ayin, pairs with MAM's position 6.

## 8. The screen re-measured: its class (v), and MAM-simple's one change to a verse-final chanted word since

The plan's precondition 1 asks for the screen's class (v) to be re-measured before this run relies on it, expecting 4 members against UXLC 3.9 and 3 against WLC 4.22. The screen's report, `.novc/mas_b_screen_report.txt` in the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`, read on 2026-09-10, has 4, 3 and 3 against UXLC 3.9, WLC 4.22 and WLC 4.20. This run recounts the screen's classes with the screen's `classify` and has the same members: 1 Samuel 17:5, 1 Kings 14:14, Psalms 70:2 and Psalms 72:15 against UXLC 3.9, and 1 Samuel 17:5, Psalms 70:2 and Psalms 72:15 against WLC 4.22 and WLC 4.20.

MAM-simple changed between the screen's commit, `30fb7681`, and this run's, `5f996d0e`, when `main` was merged into this branch on 2026-09-10: `MAM-simple/json-vtrad-bhs` differs on 12 lines. 10 of them hold sof pasuq, and on one alone does the last chanted word change: at 2 Chronicles 26:15 MAM-simple had כִּֽי־חָזָֽק׃ at `30fb7681`, with a U+05BD on the non-final atom, and has כִּי־חָזָֽק׃ at `5f996d0e`, without it; MAM's last U+05BD is at the same position in both. UXLC 3.9 and WLC 4.22 record כִּֽי־חָזָֽק׃, with both U+05BD, so the verse was in the screen's class (i) against each transcription and is now in its class (vi). That is the whole difference between this run's recount and the screen's section 2: class (i) one lower and class (vi) one higher against each transcription, and every other class the same. The verse is not a hit either way.

## 9. Method

1. **Inputs, as in the screen** (its section 11, item 1): MAM from `MAM-simple/json-vtrad-bhs` through `accgram.mam_simple_verse`, which takes the qere of a ketiv and qere and the `cant-combined` form of a dual-cantillation span; UXLC 3.9 from `in/UXLC-39/*.xml`, its `<w>` and `<q>` elements with the `<x>` note markers dropped; WLC 4.22 and WLC 4.20 from `out/wlc422-u` and `out/wlc420-u`, a ketiv dropped and a qere kept. All are keyed by WLC's compact bcv, which is BHS versification on every side. The loaders are `.novc/masuw_screen_lib.py`, a verbatim copy of the screen's `.novc/mas_b_screen.py`, and UXLC's notes are ignored, as in the screen.
2. **The verse-final chanted word** is the last atom holding sof pasuq plus every atom maqaf-joined to it; a side with no sof pasuq in the verse uses its last atom with letters, as in the screen's section 8.
3. **Three passes.** The whole pass compares verse-final chanted words whose letters agree atom by atom. The final-atom pass compares the final atoms of verse-final chanted words whose letters differ but whose final atoms agree. Both are the plan's step 2 and the screen's. The aligned pass compares the rest, the verses the plan skips (section 7).
4. **The criterion and the classes** are the plan's steps 3 and 4: class 1 when the transcription also has a U+05BD at MAM's last position, class 2 when it has none there, class 3 for 1 Kings 7:37 and Job 4:12 whatever else holds, and a separate group, empty, for a U+05BD in the transcription and none in MAM. On the whole pass class 1 is exactly the screen's class (v). Where the transcription has MAM's last position, that is the last position both have, so a later position of the transcription is beyond the last common position while no position of MAM's is, which is class (v); and in every class (v) member MAM's last position is the last common one.
5. **Syllables** are read off each text's points by the letter walker `ben_onsets`, copied from the screen's `.novc/mas_b_syllables.py` and built on `accgram.final_stress`: a full vowel opens a syllable, a furtive patah included, a sheva or a hataf none, and a holam male or a shuruq belongs to the consonant before its vav. For every hit the run checks MAM's count against the full-vowel syllables of Phonetic MAM's `jta` for the same chanted word, and whether Phonetic MAM's stress is on the syllable of MAM's last U+05BD. The count agrees for every hit, and the stress for every hit but Job 31:7 (section 4).
6. **Calibration**, the plan's step 5: the run raises unless 1 Samuel 17:5 and Psalms 72:15 are class 1 hits against UXLC 3.9 and WLC 4.22, and 1 Kings 14:14 against UXLC 3.9. It asks the first two of WLC 4.20 as well. All held.
7. **The precondition**: the screen's class (v), recounted with the screen's `classify` on the whole pass and compared with 4, 3 and 3 (section 8).

## 10. Scripts and commands that re-establish every figure

All are throwaway scripts, gitignored under `.novc/` in the worktree named at the top. Each moves to that worktree's root itself, so it runs from any directory on the primary clone's interpreter; run them in this order. Only `masuw_run.py` reads MAM-private, which holds Phonetic MAM, and it finds it through `REPOS_ROOT`:

```powershell
$env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c/.novc/masuw_run.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c/.novc/masuw_links.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c/.novc/masuw_moved_check.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c/.novc/masuw_write_doc.py
```

1. `masuw_screen_lib.py`: the screen's loaders, verse-final chanted word, positions and `classify`, a verbatim copy of `.novc/mas_b_screen.py` in the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`. The other scripts import it, and it is not run by itself.
2. `masuw_run.py`: the run. It writes `masuw_run_results.json`, which holds every figure of sections 1 to 5 and 7 and the recount of section 8, and `masuw_run_report.txt`, which spells every hit's forms out by Unicode name. It copies the syllable and Phonetic MAM functions of the screen's `.novc/mas_b_syllables.py` and `.novc/mas_b_stress.py`.
3. `masuw_links.py`: runs `py/main_verse_links.py` for each class 1 member and writes `masuw_links_results.json` and `masuw_links_report.txt` (section 6).
4. `masuw_moved_check.py`: MAM-simple's changes since the screen's commit (section 8), written to `masuw_moved_check_results.json` and `masuw_moved_check_report.txt`.
5. `masuw_write_doc.py`: writes this file from those three JSON files and from UXLC's change record for 1 Kings 14:14. Before writing, it asserts every count, list and position the prose states against the data; after building, it checks every line with `uni_denorm.has_std_mark_order` and for a first strong character that is Hebrew. It raises on any failure.

The figures were measured against this worktree at `5f996d0e`, that is, MAM-simple, `in/UXLC-39`, `out/wlc422-u` and `out/wlc420-u` as committed there, and against Phonetic MAM in MAM-private at `ecab7264`. What is not expected to change: the calibration and the class 1 list. A re-run after MAM-simple, UXLC or WLC moves is a new measurement, and a hit appearing or vanishing is a finding rather than noise.
