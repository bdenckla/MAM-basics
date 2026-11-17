# Part 2, slice p2d: the two tests over atoms

Written by Claude (Opus 5.5) on 2026-11-13, New York time, as a sub-agent of the session that wrote `README.md`, by `scripts/p2d_review.py` from `out/p2d-scan.json`. Not reviewed by a human. Nothing tracked changed. Every form here is from a transcription, the BHSA's (`g_word_utf8`) or MAM's (MAM-simple), and once WLC 4.18's, emitted by script, stripped of accents as the review's page strips its forms; nothing here says what the Leningrad Codex has.

## The answer

1. **Test B over atoms finds 4 atoms of class mam-elsewhere, against 8 slots at the slot level:** the review's three al/el corrections (Exodus 10:28, Judges 19:23, Jeremiah 47:6) and Leviticus 4:35, still borderline (one atom on each side).
2. **The four slot-level artifacts are gone from mam-elsewhere.** Genesis 15:10, Exodus 2:10, 2 Samuel 3:32, Job 8:1 each move to mam-unique: the BHSA's whole atom, conjunction or article included, has a pointing found nowhere else in the BHSA (a dagesh missing after the article or after the wayyiqtol's conjunction), and its analysis is the one the BHSA gives MAM's pointing of the atom. The conjunction's and the article's pataḥ already spell that analysis, so the missing dagesh changes nothing in it.
3. **Test A over atoms flags 255 atoms in 222 groups, against 359 slots in 305 groups.** 21 groups (22 atoms) depart from their key's commonest analysis only in person, number, gender or suffix, a kind that the slot-level test could not see. In none does the analysis give a person, gender or suffix that the pointing does not spell: 18 groups are homographs that context decides, 13 of them prefix-conjugation verbs that are second masculine and third feminine singular alike. The number departures are the ones to judge:
   - **1 Samuel 30:26 and Job 42:10, 'his friend' analysed as plural ('his friends').** The pointing is the same for both numbers and the letters lack the plural's yod, so the analysis gives a number that the atom spells only with an unwritten yod. The BHSA analyses 1 Kings 16:11 the same way (וְרֵעֵהוּ, `W + R<=/ -.pl.m +HW`); Test A could not judge that atom: its key, with the conjunction, has no other atom in the BHSA.
   - **2 Samuel 3:34, 'your hand' analysed as dual:** the pointing spells it (a segol with munaḥ, a conjunctive accent, where the singular has sheva); only the yod is unwritten. At Jeremiah 40:4 the same atom has segolta, where the segol can be the pausal singular's.
4. **Two more departures over atoms, beyond the brief, worth Ben's judgment.** The BHSA analyses the atom pointed as the feminine 'you' as the masculine 'you' (`>TH`) at Numbers 11:15, Deuteronomy 5:27, Ezekiel 28:14, where a man or God is addressed; at the slot level the 3 slots supported one another. And at Deuteronomy 25:7 it analyses an atom whose letters have a yod that MAM's lack as the verb 'refuses', the word MAM's letters spell.

## Method

`scripts/p2d_scan_atoms.py` adapts `part2_scan.py` without editing it. Its unit is a BHSA atom (`bc_common.Bhsa.atoms`, ketiv side); 1315 atoms with a slot that has a qere are skipped. An atom's **pointed key** is the set of its slots' languages and `bc_common.skey` of its text, final maqaf stripped; the languages are a set, so that the number of slots belongs to the analysis. Its **analysis** is the tuple, over its slots, of `lex`, `vs`, `vt`, `ps`, `nu`, `gn` and `prs`. Support, Test A and Test B are `part2_scan.py`'s, applied to whole atoms: Test B compares the BHSA's atom with MAM's whole atom, MAM's key being `bkey` of MAM's atom, final maqaf stripped. A Test A group's kind compares its analysis with its key's commonest: **segmentation** (another number of slots), **lexeme**, **stem/tense**, or **ps/nu/gn/prs** (the same `lex`, `vs` and `vt` in every slot). In the analyses below a slot is `lex [vs vt] [ps.nu.gn] [+prs]`, with `-` for NA and `?` for unknown, and slots are joined by ` + `.

## Counts against the slot level

| Class | Atoms | Slots at the slot level (`out/33-part2-scan-run.txt`) |
|---|---|---|
| mam-elsewhere | 4 | 8 |
| mam-unique | 205 | 184 |
| written | 148 | 104 |
| both | 6909 | 7059 |
| neither | 249 | 169 |

Both runs read 304789 atoms, of which 1315 have a ketiv and 1530 letters that differ from MAM's atom; 7517 atoms have pointing that differs from MAM's. Over atoms, 2 of these have equal keys after all: at Daniel 5:6 and 5:9 MAM's atom has HEBREW POINT HOLAM HASER FOR VAV on a consonantal vav, which `bkey` leaves in place, while it moves the BHSA's ḥolam on that vav to the letter before.

Where the slot-level rows went, by the atom that holds each slot:

| Slot-level class | Atom-level class | Slot rows |
|---|---|---|
| both | both | 6908 |
| both | mam-unique | 48 |
| both | neither | 36 |
| both | written | 67 |
| mam-elsewhere | mam-elsewhere | 4 |
| mam-elsewhere | mam-unique | 4 |
| mam-unique | mam-unique | 153 |
| mam-unique | neither | 31 |
| neither | neither | 169 |
| written | neither | 22 |
| written | written | 82 |

A slot-level `both` becomes `mam-unique` when the BHSA's whole atom is found nowhere else though each slot's pointing is (a conjunction's unusual vowel, a dagesh missing after the article). It becomes `written` or `neither` when MAM's whole atom does not occur in the BHSA, as with MAM's ḥolam in the divine name after a preposition: so at 67 of the 67 such `written` atoms and 33 of the 35 such `neither` atoms. A slot-level `mam-unique` becomes `neither` when MAM's whole atom does not occur in the BHSA, or when the finer analysis differs, as at Leviticus 5:12 (below). Examples are in `out/p2d-class-changes.txt`.

**Test A:** 255 atoms in 222 groups, against 359 slots in 305 groups. By kind, atoms: segmentation 4, lexeme 200, stem/tense 29, ps/nu/gn/prs 22. Groups that the slot level did not flag at all: segmentation 3 (3 atoms), lexeme 44 (57 atoms), stem/tense 7 (9 atoms), ps/nu/gn/prs 21 (22 atoms). Test A can judge an atom only when its key has some analysis at least 5 times: 235366 of 303474 keyed atoms, against 369196 of 418274 keyed slots at the slot level. Of the slot level's 62 stem/tense words, 20 are still flagged, 41 lie in atoms whose key is too small to judge, and 1 is supported; of its 297 lexeme words, 144 are still flagged (1 of them as segmentation), 104 lie in atoms whose key is too small, and 49 are supported.

## The mam-elsewhere atoms

Each is analysed as MAM's pointing is analysed elsewhere in the BHSA, while the BHSA's own pointing is analysed otherwise elsewhere. Counts are of the BHSA's other atoms; where a count is 3 or less, its references follow.

| Verse | BHSA | MAM | BHSA's analysis | Its own key's other atoms | MAM's key's atoms in the BHSA |
|---|---|---|---|---|---|
| Exodus 10:28 | אֶל־ | אַל־ | `>L=` | `>L` x3539 | `>L=` x575, `>L` x2 (Judges 19:23, Jeremiah 47:6), `>L==` x1 (1 Samuel 27:10) |
| Leviticus 4:35 | חֶלְבָּה | חֶלְבָּהּ | `XLB=/ -.sg.m +H` | `XLBH/ -.sg.? +n/a` x1 (Judges 1:31) | `XLB=/ -.sg.m +H` x1 (Leviticus 4:31) |
| Judges 19:23 | אַל־ | אֶל־ | `>L` | `>L=` x575, `>L` x1 (Jeremiah 47:6), `>L==` x1 (1 Samuel 27:10) | `>L` x3539, `>L=` x1 (Exodus 10:28) |
| Jeremiah 47:6 | אַל־ | אֶל־ | `>L` | `>L=` x575, `>L` x1 (Judges 19:23), `>L==` x1 (1 Samuel 27:10) | `>L` x3539, `>L=` x1 (Exodus 10:28) |

Exodus 10:28, Judges 19:23 and Jeremiah 47:6 are the review's al/el corrections, and Part 1 reads them. Leviticus 4:35 stays borderline: the BHSA's atom has no mappiq in its final he, the pointing of the place name Helbah at its one other atom, and is analysed with the suffix that MAM's atom, with the mappiq, spells at its one other atom in the BHSA.

## The four slot-level artifacts

| Verse | Slot level | BHSA atom | MAM atom | BHSA's analysis | Atom level | MAM's key's atoms in the BHSA |
|---|---|---|---|---|---|---|
| Genesis 15:10 | mam-elsewhere, `YPWR/` | הַצִפֹּר | הַצִּפֹּר | `H + YPWR/ -.sg.?` | mam-unique | `H + YPWR/ -.sg.?` x8 |
| Exodus 2:10 | mam-elsewhere, `GDL[ qal wayq` | וַיִגְדַּל | וַיִּגְדַּל | `W + GDL[ qal wayq p3.sg.m` | mam-unique | `W + GDL[ qal wayq p3.sg.m` x10 |
| 2 Samuel 3:32 | mam-elsewhere, `NF>[ qal wayq` | וַיִשָּׂא | וַיִּשָּׂא | `W + NF>[ qal wayq p3.sg.m` | mam-unique | `W + NF>[ qal wayq p3.sg.m` x41 |
| Job 8:1 | mam-elsewhere, `>MR[ qal wayq` | וַיֹאמַר | וַיֹּאמַר | `W + >MR[ qal wayq p3.sg.m` | mam-unique | `W + >MR[ qal wayq p3.sg.m` x122 |

Over atoms each has no other atom of its own pointing, so it is mam-unique, the class that needs a reader (like the review's Genesis 34:11). The slot-level Test A had also flagged the slots of Exodus 2:10, 2 Samuel 3:32 and Job 8:1 (stem/tense); over atoms their keys, each found once, are too small for Test A to judge.

## Test A: departures only in person, number, gender or suffix

All 21 groups; none was flagged at the slot level. "Spelled?" says whether the pointing spells the person, number, gender or suffix that the BHSA gives. MAM's atom has the BHSA's pointing at every one of their atoms, by `bkey` (accents, and the BHSA's way of writing a ḥolam male, aside).

| # | Verse | BHSA | BHSA's analysis | The key's analyses | Departs in (this for the key's commonest) | Spelled? | Why |
|---|---|---|---|---|---|---|---|
| A16 | Genesis 49:11 | בְּנִי | `BN/ -.sg.m` | `BN/ -.sg.m +J` x78, `BN/ -.sg.m` x1 | prs absent for J | yes | Pointed alike as 'my son' and as the construct 'son of' with the old ending -î, the ḥiriq compaginis. The ETCBC's morphology gives the ḥiriq and yod to a univalent final (`g_uvf_utf8`) in the construct state, not to a suffix; the next atom, 'his she-ass', makes the phrase 'his she-ass's colt'. |
| A29 | Leviticus 20:17 | תִרְאֶה | `R>H[ qal impf p3.sg.f` | `R>H[ qal impf p2.sg.m` x13, `R>H[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | The prefix t- with no ending is second masculine and third feminine singular alike; the subject is the feminine pronoun just before it. |
| A61 | 1 Samuel 30:26 | לְרֵעֵהוּ | `L + R<=/ -.pl.m +HW` | `L + R<=/ -.sg.m +HW` x19, `L + R<=/ -.pl.m +HW` x1 | nu pl for sg | only with an unwritten yod | Pointed and written as the singular 'to his friend': the plural ending's tsere is the singular's vowel too, and the plural's yod is not written. The ETCBC's morphology gives the tsere to the plural ending (`g_nme_utf8`) and only the he and shuruq to the suffix, where its singular atoms of the key give the tsere to the suffix. The context, spoil sent 'to the elders of Judah, his friends', is the evident ground. |
| A63 | 2 Samuel 3:34; Jeremiah 40:4 | יָדֶךָ | `JD/ -.du.? +K` | `JD/ -.sg.? +K` x26, `JD/ -.du.? +K` x2 | nu du for sg | yes at 2 Samuel 3:34; either at Jeremiah 40:4 | See the accents below: at 2 Samuel 3:34 the segol, with a conjunctive accent, is the vowel of the suffix on a plural or dual noun, whose yod is not written; at Jeremiah 40:4, with a disjunctive accent, it can be the pausal singular's. |
| A66 | 2 Samuel 12:10 | וַתִּקַּח | `W + LQX[ qal wayq p2.sg.m` | `W + LQX[ qal wayq p3.sg.f` x31, `W + LQX[ qal wayq p2.sg.m` x1 | ps p2 for p3; gn m for f | yes | The wayyiqtol with t- is second masculine and third feminine singular alike; Nathan is addressing David ('you despised me'). |
| A77 | 1 Kings 13:22 | וַתָּשָׁב | `W + CWB[ qal wayq p2.sg.m` | `W + CWB[ qal wayq p3.sg.f` x12, `W + CWB[ qal wayq p2.sg.m` x1 | ps p2 for p3; gn m for f | yes | As at 2 Samuel 12:10: the old prophet addresses the man of God, and the verse's next two wayyiqtol verbs are also analysed as second masculine. |
| A93 | Isaiah 26:17 | תַּקְרִיב | `QRB[ hif impf p3.sg.f` | `QRB[ hif impf p2.sg.m` x11, `QRB[ hif impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is 'a pregnant woman'. |
| A97 | Isaiah 34:1 | תִּשְׁמַע | `CM<[ qal impf p3.sg.f` | `CM<[ qal impf p2.sg.m` x23, `CM<[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is 'the earth'. |
| A102 | Isaiah 53:10 | תָּשִׂים | `FJM[ qal impf p3.sg.f` | `FJM[ qal impf p2.sg.m` x11, `FJM[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine ('if you make his soul a guilt offering') and third feminine ('if his soul makes a guilt offering') are spelled alike; the BHSA makes 'his soul' the subject, an interpretive choice that the pointing allows. |
| A111 | Jeremiah 15:19 | כְּפִי | `K + PH/ -.sg.m +J` | `K + PH/ -.sg.m` x14, `K + PH/ -.sg.m +J` x1 | prs J for absent | yes | 'My mouth' and the construct 'mouth of' (in the sense 'according to') are pointed alike; here 'you shall be as my mouth'. |
| A117 | Jeremiah 44:16 | אֵינֶנּוּ | `>JN/ -.sg.m +NW` | `>JN/ -.sg.m +HW` x35, `>JN/ -.sg.m +NW` x1 | prs NW for HW | yes | 'He is not' and 'we are not' are pointed alike with this suffix; the plural participle 'listening' that follows makes it 'we'. |
| A128 | Ezekiel 22:4 | וַתָּבֹוא | `W + BW>[ qal wayq p2.sg.m` | `W + BW>[ qal wayq p3.sg.f` x20, `W + BW>[ qal wayq p2.sg.m` x1 | ps p2 for p3; gn m for f | yes | The atom is second masculine or third feminine singular. The BHSA takes the person from the context, an address to Jerusalem, and the gender from the atom: a second feminine singular would end in -î, as the verse's preceding wayyiqtol does. So the analysis does not correct the atom to the feminine. |
| A139 | Hosea 13:4 | בִּלְתִּי | `BLT/ -.sg.? +J` | `BLT/ -.sg.?` x22, `BLT/ -.sg.? +J` x1 | prs J for absent | yes | The particle 'except' and 'besides me' are pointed alike; the ETCBC gives the ḥiriq and yod to a univalent final in its other atoms of the key and to a first singular suffix here, where the verse ends 'there is no savior besides me'. |
| A151 | Malachi 1:4 | תֹאמַר | `>MR[ qal impf p3.sg.f` | `>MR[ qal impf p2.sg.m` x22, `>MR[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is Edom, as a feminine. |
| A158 | Psalms 37:30 | תְּדַבֵּר | `DBR[ piel impf p3.sg.f` | `DBR[ piel impf p2.sg.m` x18, `DBR[ piel impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is 'his tongue', feminine. |
| A164 | Psalms 97:3 | תֵּלֵךְ | `HLK[ qal impf p3.sg.f` | `HLK[ qal impf p2.sg.m` x19, `HLK[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is 'fire', feminine. |
| A165 | Psalms 118:21 | וַתְּהִי | `W + HJH[ qal wayq p2.sg.m` | `W + HJH[ qal wayq p3.sg.f` x85, `W + HJH[ qal wayq p2.sg.m` x1 | ps p2 for p3; gn m for f | yes | The wayyiqtol with t- is second masculine and third feminine alike; God is addressed ('you answered me'). |
| A173 | Job 33:28 | תִּרְאֶה | `R>H[ qal impf p3.sg.f` | `R>H[ qal impf p2.sg.m` x16, `R>H[ qal impf p3.sg.f` x1 | ps p3 for p2; gn f for m | yes | Second masculine and third feminine alike; the subject is 'life', feminine (a ketiv 'my life' and a qere 'his life', in the BHSA and in MAM). |
| A175 | Job 42:10 | רֵעֵהוּ | `R<=/ -.pl.m +HW` | `R<=/ -.sg.m +HW` x82, `R<=/ -.pl.m +HW` x1 | nu pl for sg | only with an unwritten yod | As at 1 Samuel 30:26: Job prayed for his three friends, and the ETCBC again gives the tsere to the plural ending. |
| A186 | Song of Songs 6:12 | עַמִּי | `<M/ -.sg.m` | `<M/ -.sg.m +J` x178, `<MJ/ -.sg.m +n/a` x1, `<M/ -.sg.m` x1 | prs absent for J | yes | As at Genesis 49:11: the construct with the ḥiriq compaginis (univalent final, construct state) before 'noble'. The BHSA's atom has a maqaf after it, binding it to the next atom; MAM's has none. |
| A199 | Nehemiah 9:9 | וַתֵּרֶא | `W + R>H[ qal wayq p2.sg.m` | `W + R>H[ qal wayq p3.sg.f` x28, `W + R>H[ qal wayq p2.sg.m` x1 | ps p2 for p3; gn m for f | yes | The wayyiqtol with t- is second masculine and third feminine alike; God is addressed throughout the prayer. |

**The accents of A63's key.** The key's 26 singular atoms all have disjunctive accents (atnaḥ 12, silluq 9, zaqef 3, revia 1, oleh-weyored 1), where the segol under the dalet is the pausal singular's. The two dual atoms: 2 Samuel 3:34, munaḥ (conjunctive); Jeremiah 40:4, segolta (disjunctive).

**The plurals of 'his friend'.** Every BHSA slot of `R<=/` that is plural with a third masculine singular suffix: suffix `HW`, slot רֵעֵהוּ, at 1 Samuel 30:26, 1 Kings 16:11, Job 42:10; suffix `W`, slot רֵעָיו, at Job 32:3. 1 Kings 16:11's atom is וְרֵעֵהוּ (MAM וְרֵעֵהוּ), analysed `W + R<=/ -.pl.m +HW`. These plurals of the suffix `HW` are the person, number, gender and suffix departures that correct the written atom: they correct its spelling, by context, not its pointing (`out/p2d-check.txt`, part 2).

## Other things that the atom-level tests show

1. **The segmentation kind, 4 groups.**
   - A43, Deuteronomy 25:7, מֵאֵין: `M>N[ piel perf p3.sg.m`; the key: `MN + >JN/ -.sg.m` x26, `M>N[ piel perf p3.sg.m` x1. The BHSA's atom, like WLC 4.18's (a near-copy of BHS, so not an independent check), has a yod after the second tsere that MAM's lacks. The BHSA analyses it as one slot, the piel perfect 'refuses' (`M>N[`), the word that MAM's letters spell, where its other atoms of this pointing are two slots, 'from' and 'nothing'. Its own letters spell 'refuses' only with the yod as a vowel letter. Test B skips the atom, its letters differing from MAM's. MAM מֵאֵן; WLC 4.18 מֵאֵין.
   - A162, Psalms 73:20, בָּעִיר: `B + <WR[ hif infc ?.?.?`; the key: `B + H + <JR/ -.sg.f` x45, `B + <WR[ hif infc ?.?.?` x1. 'When (you) arouse', the hiphil infinitive of `<WR[` with its he unwritten after the preposition, where the key's other atoms are 'in the city'. The pointing spells both; context decides.
   - A192, Ezra 3:10, בַּחֲצֹצְרֹות: `B + H + XYYRH/ -.pl.f`; the key: `B + XYYRH/ -.pl.f` x13, `B + H + XYYRH/ -.pl.f` x1. An unwritten article ('with the trumpets'), where the key's other atoms have none. Before a ḥataf pataḥ the preposition has pataḥ with or without the article, so the pointing spells both.
   - A222, 2 Chronicles 30:10, לָעִיר: `L + <JR/ -.sg.f`; the key: `L + H + <JR/ -.sg.f` x25, `L + <JR/ -.sg.f` x1. No article ('from city to city'), where the key's other atoms have one. The qamats under the preposition is elsewhere always analysed as the article's; whether it can be the preposition's own in this paired phrase is for a reader to judge.
2. **The pronoun 'you'.** A34: אַתְּ, `>TH p2.sg.m +n/a`, key `>T= p2.sg.f +n/a` x32, `>TH p2.sg.m +n/a` x2 (Numbers 11:15; Ezekiel 28:14). A40: וְאַתְּ, `W + >TH p2.sg.m +n/a`, key `W + >T= p2.sg.f +n/a` x12, `W + >TH p2.sg.m +n/a` x1 (Deuteronomy 5:27). The BHSA analyses the atom pointed as the feminine 'you' as the masculine (`>TH`, second masculine singular) where a man or God is addressed: Moses to God at Numbers 11:15, the people to Moses at Deuteronomy 5:27, God to the king of Tyre at Ezekiel 28:14. MAM's atoms there have the same pointing. Over slots the three supported one another: `part2_scan.py`'s key of the pronoun's slot has `>T=` x44, `>TH` x3, and 3 meets the support threshold. Over atoms the conjunction at Deuteronomy 5:27 splits them. A correction of gender by context, for Ben's judgment.
3. **Test B with the finer analysis.** 5 atoms of Test B depart from MAM's key's commonest analysis only in person, number, gender or suffix, all of class neither (`out/p2d-test-b-png.txt`). None is a correction toward MAM. One shows the BHSA not correcting where it corrects elsewhere: at Leviticus 5:12 its atom אַזְכָּרָתָה has no mappiq, MAM's אַזְכָּרָתָהּ has one, and the BHSA analyses it with no suffix (`>ZKRH/ -.sg.f`), following the missing mappiq, while at Leviticus 4:35 the same lack is analysed with the suffix. The others are second masculine or third feminine homographs (Deuteronomy 15:20, Isaiah 31:8), a suffix written with a shuruq where MAM's has a ḥolam male (2 Samuel 20:8), and Jeremiah 11:2, where the BHSA's atom is pointed and analysed as second singular with a suffix, and MAM's atom is pointed as second plural.
4. **New lexeme and stem/tense groups.** 44 lexeme groups and 7 stem/tense groups were not flagged at the slot level. Apart from the pronoun, read above, they were skimmed, not read one by one: they look like homographs that context decides (a name against a common noun, the ETCBC's numbered homonyms, an adjective against a participle, a niphal perfect against a qal cohortative). They are marked `(new)` in `out/p2d-test-a.txt`.

## What the atom-level tests cannot find

1. **Less of Test A is testable.** A whole atom's key is narrower than a slot's, so fewer keys reach 5 atoms of one analysis; 145 slot-level Test A words lie in atoms that are too few to judge, 1 Kings 16:11's plural among them. The two runs complement each other; neither replaces the other.
2. **A conjunction or a preposition splits a key.** The same word with and without a prefix has two keys. That is what unmasks the pronoun above, and what hides 1 Kings 16:11.
3. **Test B still skips atoms whose letters differ from MAM's**, as at Deuteronomy 25:7, and the slots of a ketiv.
4. **The finer analysis splits support.** An analysis that differs only in a feature the pointing does not decide counts as another analysis. For example, 67 of the BHSA's 3866 noun lexemes have the gender `unknown` in some slots and `m` or `f` in others (`out/p2d-check.txt`, part 6).

## Files

- `scripts/p2d_scan_atoms.py`: the scan. Its outputs: `out/p2d-scan-run.txt` (counts and the cross-tabulations against the slot level), `out/p2d-test-a.txt`, `out/p2d-test-b.txt`, `out/p2d-scan.json`, and the run's log `out/p2d-scan-log.txt`.
- `scripts/p2d_detail.py`: `out/p2d-detail-png.txt`, each ps/nu/gn/prs group with the ETCBC's morphology features and its verse, atom by atom.
- `scripts/p2d_check.py`: `out/p2d-check.txt`, the accents of the keys behind the judgments, the BHSA's plurals of 'friend', Job 33:28's ketiv and qere, and the segmentation groups' verses.
- `scripts/p2d_explore.py`: `out/p2d-class-changes.txt`; `scripts/p2d_png_b.py`: `out/p2d-test-b-png.txt`; `scripts/p2d_wait.py`, a helper that was not needed.
- `scripts/p2d_review.py`: this page.
