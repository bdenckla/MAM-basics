# Meteg after silluq: MAM's verse-final chanted words screened against UXLC 3.9 and WLC 4.22

Task B of Ben's question of 2026-09-09 -- does MAM have a verse-final chanted word with a meteg after the silluq besides 1 Kings 7:37 -- run as a differential screen of every verse-final chanted word of MAM against UXLC 3.9 and WLC 4.22, with WLC 4.20 as a second run and mgketer's transcription of Mikra'ot Gedolot ha-Keter as an optional third. Written by `.novc/mas_b_write_doc.py` from the screen's JSON, at worktree HEAD `30fb7681` (branch `claude/meteg-after-silluq-mam-9555f5`), 2026-09-09. Every Hebrew form below is lifted from the data by that script; the UXLC and WLC forms are shown in MAM's mark order (`uni_denorm.give_std_mark_order`) because `py/tests/test_prose_mark_order.py` requires it of every tracked `.md`, and the screen itself compared letter positions, never bytes, so the reordering changes nothing it reports. UXLC's m-notes and d-notes were ignored throughout (Ben's instruction, 2026-09-09): a U+05BD is a U+05BD whether or not a note sits on it.

Two terms, used exactly as the `hebrew-prose` skill defines them: an **atom** is one written
word between spaces or maqafs; a **chanted word** is a lone atom or a whole maqaf compound.
The **verse-final chanted word** is the last atom holding sof pasuq plus every atom
maqaf-joined to it. A **position** is a letter ordinal: position k means the U+05BD sits on
the k-th Hebrew base letter of the chanted word, maqafs not counted.

## 1. Headline: beyond 1 Kings 7:37, no verse-final chanted word of MAM has a meteg after the silluq that UXLC 3.9 or WLC 4.22 lacks

Seven findings, each with its disposition first.

1. **The target class has 6 members against UXLC 3.9 and the same 6 against WLC 4.22 -- 5 beyond 1 Kings 7:37.** Class (iii) holds the verse-final chanted words where MAM has a U+05BD later than the last U+05BD both sides have. The table in section 3 lists them; the six are:
   - Exodus 32:17: MAM בַּֽמַּחֲנֶֽה׃ (positions 1, 4); UXLC 3.9 records בַּֽמַּחֲנֶה׃ (positions 1); WLC 4.22 records בַּֽמַּחֲנֶה׃ (positions 1).
   - Deuteronomy 23:12: MAM הַֽמַּחֲנֶֽה׃ (positions 1, 4); UXLC 3.9 records הַֽמַּחֲנֶה׃ (positions 1); WLC 4.22 records הַֽמַּחֲנֶה׃ (positions 1).
   - 1 Kings 7:37: MAM לְכֻלָּֽהְנָֽה׃ (positions 3, 5); UXLC 3.9 records לְכֻלָּֽהְנָה׃ (positions 3); WLC 4.22 records לְכֻלָּֽהְנָה׃ (positions 3).
   - Obadiah 1:17: MAM מוֹרָֽשֵׁיהֶֽם׃ (positions 3, 6); UXLC 3.9 records מוֹרָֽשֵׁיהֶם׃ (positions 3); WLC 4.22 records מוֹרָֽשֵׁיהֶם׃ (positions 3).
   - Psalms 60:9: MAM מְחֹֽקְקִֽי׃ (positions 2, 4); UXLC 3.9 records מְחֹֽקְקִי׃ (positions 2); WLC 4.22 records מְחֹֽקְקִי׃ (positions 2).
   - Proverbs 31:28: MAM וַֽיְהַלְלָֽהּ׃ (positions 1, 5); UXLC 3.9 records וַֽיְהַֽלְלָהּ׃ (positions 1, 3); WLC 4.22 records וַֽיְהַֽלְלָהּ׃ (positions 1, 3).
2. **4 of the 6 are settled by mark position alone, and none of them is a meteg after the silluq** -- Exodus 32:17, Deuteronomy 23:12, Obadiah 1:17, Proverbs 31:28. The criterion is measured against Phonetic MAM, not assumed. Ben's syllable definition (2026-09-09): a vocal sheva by either notation -- a simple sheva or a xataf -- is not a syllable and attaches to the syllable that follows it; a furtive patax is a syllable by itself. Under that definition `.novc/mas_b_syllables.py` counted, over all 263320 chanted words of Phonetic MAM (al-hatorah's `io/a01-phonetic-std-set` in `C:/Users/BenDe/GitRepos/MAM-private`, at `3f53991`; its `jta` field has `!` before the stressed syllable, `.` between syllables and `-` between atoms, and a `jta` syllable holding `^` is a sheva syllable and one holding `8`, `6` or `0` a xataf syllable, both attaching forward), the syllables after the stressed syllable within the stressed atom: 0 in 209262, 1 in 54046, 2 in 12, and never 3 or more. All 12 are mid-verse: 10 are a stress retraction before a following chanted word stressed on its first syllable (Exodus 15:8 נֶ֣עֶרְמוּ, Deuteronomy 33:28 יַ֥עַרְפוּ, 2 Samuel 5:21 וַיַּ֥עַזְבוּ, Isaiah 40:18 תַּ֥עַרְכוּ, Isaiah 50:8 נַ֣עַמְדָה, Isaiah 63:12 בּ֤וֹקֵֽעַ, Proverbs 1:19 כׇּל־בֹּ֣צֵֽעַ, Proverbs 11:26 מֹ֣נֵֽעַ, Job 5:10 וְשֹׁ֥לֵֽחַ, 1 Chronicles 14:12 וַיַּ֥עַזְבוּ) and 2 a dexi read as the stress (Psalms 4:3 לִ֭כְלִמָּה, Psalms 71:9 אַֽל־תַּ֭שְׁלִיכֵנִי); the script sorts each into its kind from the dexi in Phonetic MAM's form or from the next chanted word's `jta`, and checks that none of them has sof pasuq (section 3 lists them). Neither kind reaches a verse end: a retraction needs a following chanted word in the verse, and none of Phonetic MAM's 2687 chanted words with a dexi is verse-final. So, relative to Phonetic MAM and not as a claim about Hebrew, a verse-final stressed syllable is followed by at most one syllable: a verse-final silluq sits on the last syllable or the one before it, and a U+05BD with two or more syllables after it is a meteg. In each of these four MAM's earlier mark has two syllables after it -- the xataf of בַּֽמַּחֲנֶֽה׃ (`bam.ma.x8.!ne`) and of הַֽמַּחֲנֶֽה׃ (`ham.ma.x8.!ne`) and the vocal sheva of וַֽיְהַלְלָֽהּ׃ (`vay.ha.l^.!lah`) attaching forward, and מוֹרָֽשֵׁיהֶֽם׃ (`mO.ra.shE.!hem`) having neither -- so MAM's earlier mark is a meteg and MAM's later mark, with no syllable after it, is MAM's silluq. UXLC 3.9 and WLC 4.22 record no U+05BD on the last syllable of any of the four: what they lack is the silluq. (At Proverbs 31:28 they record a second mark, with one syllable after it, which MAM lacks.) Section 3 gives each member's syllables beside the nuclei of `accgram.final_stress._nuclei`, which the earlier draft of this finding used and which are not Ben's syllables: that module counts a xataf as a nucleus and a furtive patax as none. Until 2026-09-09 this finding rested instead on the a-priori claim that Tiberian stress falls on the last or the penultimate syllable; Ben overruled that claim the same day, and the measurement above replaces it.
3. **The other 2 -- 1 Kings 7:37 and Psalms 60:9 -- have one syllable after the earlier mark and none after the later mark, so position alone does not settle them: either mark can be the silluq, the stress decides, and MAM's parallels point opposite ways.** At 1 Kings 7:37 (לְכֻלָּֽהְנָֽה׃) the stress is penultimate -- Ben's reading, 2026-09-09 -- and MAM's Genesis 42:36 כֻלָּֽנָה׃, the same base and the same suffix at a verse end (the letters כלנה, lifted by search), has its one U+05BD with one syllable after it: so MAM's later mark at 1 Kings 7:37 is after the silluq, and UXLC 3.9 and WLC 4.22 record the silluq only. This is the known case, and the screen confirms it. At Psalms 60:9 (מְחֹֽקְקִֽי׃) MAM's Psalms 108:9 מְחֹקְקִֽי׃, the same chanted word at a verse end, has its one U+05BD on the last syllable, with no syllable after it, and the suffixed form is finally stressed: so MAM's later mark at Psalms 60:9 is the silluq, its earlier mark on the het is a meteg, and UXLC 3.9 and WLC 4.22, which record that meteg and nothing on the last syllable, lack the silluq. Not a meteg after the silluq. **Disposition: settled by MAM's parallel and by ordinary morphology, which is Claude's reading of 2026-09-09 and not a machine verdict; no manuscript was consulted.**
4. **So the answer to Ben's question from this screen is: zero.** Every class (iii) member beyond 1 Kings 7:37 is a verse-final chanted word where UXLC 3.9 and WLC 4.22 lack the silluq MAM has, not one where MAM has a meteg after the silluq.
5. **Phonetic MAM cannot arbitrate the two undecided members, and this file does not lean on it.** `mas_b_stress.py` looked every member up in al-hatorah's `io/a01-phonetic-std-set` (the oracle `test_final_stress_vs_phonetic_mam.py` uses): its `jta` is finally stressed for all six, 1 Kings 7:37 included (`l^.khul.lah.!na`), because it takes the last U+05BD of a verse-final chanted word as the silluq. Its verdict restates the mark placement rather than testing it.
6. **The reverse class (v) has 4 members against UXLC 3.9 and 3 against WLC 4.22, 1 Samuel 17:5 among them for both** (section 4). All have one shape: the common mark on the penultimate nucleus, the source's extra mark on the last. Under penultimate stress -- which 1 Samuel 17:5's segolate has, and which the post-stress-meteg survey already records as UXLC's and WLC's meteg after the silluq there -- each is a U+05BD the transcription records after the silluq and MAM does not have.
7. **mgketer's transcription of Mikra'ot Gedolot ha-Keter is a usable third screen, and against it class (iii) is empty** (section 10): 1 Kings 7:37 falls in class (i) there, mgketer having both of MAM's marks, and no verse-final chanted word of MAM has a U+05BD later than the last one it shares with mgketer.

## 2. Counts per class per source, whole-word pass

Each source column is one run of `.novc/mas_b_screen.py` (the mgketer column,
`.novc/mas_b_mgketer.py`). Classes are mutually exclusive, assigned in the priority (iii),
(v), (iv), (i), (ii), (vi), (vii); section 11 defines them.

| Class | UXLC 3.9 | WLC 4.22 | WLC 4.20 | mgketer |
|---|---|---|---|---|
| (i) identical positions | 22741 | 22756 | 22756 | 23037 |
| (ii) MAM has extra position(s), none later than the last common position | 51 | 51 | 51 | 134 |
| (iii) MAM has an extra position LATER than the last common position (target) | 6 | 6 | 6 | 0 |
| (iv) no common position at all | 68 | 46 | 46 | 1 |
| (v) the source has an extra position later than the last common position (reverse) | 4 | 3 | 3 | 0 |
| (vi) the source has extra position(s), none later than the last common position | 190 | 193 | 193 | 2 |
| (vii) both sides have extra positions, none later than the last common position | 6 | 7 | 7 | 0 |
| verses compared in the whole-word pass | 23066 | 23062 | 23062 | 23174 |
| verses compared in the final-atom pass only (all class (i)) | 24 | 28 | 28 | 11 |
| verses skipped (section 7) | 123 | 123 | 123 | 17 |
| verses on both sides | 23213 | 23213 | 23213 | 23202 |

The final-atom pass takes the verses whose verse-final chanted word differs in base letters between MAM and the source but whose final atoms agree, and compares those final atoms alone; every one of them came out class (i), so it adds nothing to the member lists. Ben's expectation (2026-09-09) that many verse-final chanted words have fewer U+05BD in UXLC and WLC than in MAM is borne out by three rows together -- class (ii), class (iii), and the class (iv) members where the source records no U+05BD at all: 88 verse-final chanted words against UXLC 3.9 and 79 against WLC 4.22 -- while the class (vi) row, larger than any of them, is the other direction: verse-final chanted words where UXLC or WLC records a meteg before the last common position that MAM lacks.

## 3. Class (iii): MAM has a U+05BD later than the last common one -- six members, all lone atoms, and the census behind the syllable criterion

In every member the verse-final chanted word is a lone atom, so the extra mark sits on a
lone atom rather than on the final atom of a maqaf compound. Two counts are given for each
member, and they are not the same count:

1. **Syllables**, under Ben's definition of 2026-09-09 (section 1, finding 2): a full vowel
   opens a syllable, a furtive patax included; a sheva or a xataf opens none and attaches to
   the syllable after it. `.novc/mas_b_syllables.py` reads them off MAM's points with
   `accgram.final_stress`'s letter walker and checks the total against the full-vowel
   syllables of Phonetic MAM's `jta` for the same chanted word, raising on any difference;
   each mark is placed by how many syllables follow the one it is in.
2. **Nuclei**, as `accgram.final_stress._nuclei` counts them -- the module
   `py/tests/test_final_stress_vs_phonetic_mam.py` measures against Phonetic MAM, and the
   count this file's earlier draft used (`.novc/mas_b_nuclei.py`). It counts a xataf as a
   nucleus and a furtive patax as none, so its nuclei are not Ben's syllables. The two
   counts differ for Exodus 32:17 and Deuteronomy 23:12,
   whose xataf `_nuclei` counts as a nucleus, and agree for the other
   4. Sections 4 to 6 place marks by these
   nuclei ("penultimate nucleus", "last nucleus").

The first table is under Ben's definition; in it "1: two after it" means the U+05BD at
position 1 has two syllables after the syllable it is in:

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Syllables | Syllables after MAM's marks | Syllables after UXLC's and WLC's marks | Verdict |
|---|---|---|---|---|---|---|---|
| Exodus 32:17 | בַּֽמַּחֲנֶֽה׃ | בַּֽמַּחֲנֶה׃ | בַּֽמַּחֲנֶה׃ | 3 | 1: two after it; 4: none after it | 1: two after it | settled by position |
| Deuteronomy 23:12 | הַֽמַּחֲנֶֽה׃ | הַֽמַּחֲנֶה׃ | הַֽמַּחֲנֶה׃ | 3 | 1: two after it; 4: none after it | 1: two after it | settled by position |
| 1 Kings 7:37 | לְכֻלָּֽהְנָֽה׃ | לְכֻלָּֽהְנָה׃ | לְכֻלָּֽהְנָה׃ | 3 | 3: one after it; 5: none after it | 3: one after it | position alone does not settle it |
| Obadiah 1:17 | מוֹרָֽשֵׁיהֶֽם׃ | מוֹרָֽשֵׁיהֶם׃ | מוֹרָֽשֵׁיהֶם׃ | 4 | 3: two after it; 6: none after it | 3: two after it | settled by position |
| Psalms 60:9 | מְחֹֽקְקִֽי׃ | מְחֹֽקְקִי׃ | מְחֹֽקְקִי׃ | 2 | 2: one after it; 4: none after it | 2: one after it | position alone does not settle it |
| Proverbs 31:28 | וַֽיְהַלְלָֽהּ׃ | וַֽיְהַֽלְלָהּ׃ | וַֽיְהַֽלְלָהּ׃ | 3 | 1: two after it; 5: none after it | 1: two after it; 3: one after it | settled by position |

The same members against `_nuclei`'s nuclei, kept for comparison; the verdicts are the same
four, which `.novc/mas_b_write_doc.py` asserts before writing this file:

| Reference | MAM | Nuclei (`_nuclei`) | Nuclei after MAM's marks | Nuclei after UXLC's and WLC's marks |
|---|---|---|---|---|
| Exodus 32:17 | בַּֽמַּחֲנֶֽה׃ | 4 | 1: 3 nuclei before the last; 4: last nucleus | 1: 3 nuclei before the last |
| Deuteronomy 23:12 | הַֽמַּחֲנֶֽה׃ | 4 | 1: 3 nuclei before the last; 4: last nucleus | 1: 3 nuclei before the last |
| 1 Kings 7:37 | לְכֻלָּֽהְנָֽה׃ | 3 | 3: penultimate nucleus; 5: last nucleus | 3: penultimate nucleus |
| Obadiah 1:17 | מוֹרָֽשֵׁיהֶֽם׃ | 4 | 3: 2 nuclei before the last; 6: last nucleus | 3: 2 nuclei before the last |
| Psalms 60:9 | מְחֹֽקְקִֽי׃ | 2 | 2: penultimate nucleus; 4: last nucleus | 2: penultimate nucleus |
| Proverbs 31:28 | וַֽיְהַלְלָֽהּ׃ | 3 | 1: 2 nuclei before the last; 5: last nucleus | 1: 2 nuclei before the last; 3: penultimate nucleus |

The raw sources were re-read for every member by `.novc/mas_b_verify_members.py`, which
spells each side's verse-final chanted word out as Unicode names letter by letter:
members checked: 28; raw re-read mismatches: 0.

MAM's parallels for the two members position does not settle, lifted by letters from
MAM-simple (`.novc/mas_b_nuclei.py`; the syllable columns, `.novc/mas_b_syllables.py`):

| Reference | MAM | Position in the verse | Syllables | Syllables after each U+05BD | Nuclei after each U+05BD (`_nuclei`) |
|---|---|---|---|---|---|
| 1 Kings 7:37 | לְכֻלָּֽהְנָֽה׃ | verse-final | 3 | 3: one after it; 5: none after it | 3: penultimate nucleus; 5: last nucleus |
| Genesis 42:36 | כֻלָּֽנָה׃ | verse-final | 3 | 2: one after it | 2: penultimate nucleus |
| Amos 6:2 | כַֽלְנֵה֙ | mid-verse | 2 | 1: one after it | 1: penultimate nucleus |

| Reference | MAM | Position in the verse | Syllables | Syllables after each U+05BD | Nuclei after each U+05BD (`_nuclei`) |
|---|---|---|---|---|---|
| Psalms 60:9 | מְחֹֽקְקִֽי׃ | verse-final | 2 | 2: one after it; 4: none after it | 2: penultimate nucleus; 4: last nucleus |
| Psalms 108:9 | מְחֹקְקִֽי׃ | verse-final | 2 | 4: none after it | 4: last nucleus |

The census behind the syllable criterion (section 1, finding 2): the 12 chanted
words of Phonetic MAM, out of 263320, with two syllables after the stressed
syllable under Ben's definition. None is verse-final. "Next" is the chanted word that
follows in the verse, whose `jta` decides the kind: a stress retraction is one whose next
chanted word is stressed on its first syllable, and a dexi read as the stress is one whose
Phonetic MAM form holds U+05AD. MAM's forms are lifted from MAM-simple by join key; the
`jta` is Phonetic MAM's, `!` before the stressed syllable.

| Reference | MAM | Phonetic MAM's `jta` | Next chanted word | Its `jta` | Kind |
|---|---|---|---|---|---|
| Exodus 15:8 | נֶ֣עֶרְמוּ | `` !ne.`er.mu `` | מַ֔יִם | `!ma.yim` | stress retraction |
| Deuteronomy 33:28 | יַ֥עַרְפוּ | `` !ya.`ar.fu `` | טָֽל׃ | `!tal` | stress retraction |
| 2 Samuel 5:21 | וַיַּ֥עַזְבוּ | `` vay.!ya.`az.vu `` | שָׁ֖ם | `!sham` | stress retraction |
| Isaiah 40:18 | תַּ֥עַרְכוּ | `` !ta.`ar.khu `` | לֽוֹ׃ | `!lO` | stress retraction |
| Isaiah 50:8 | נַ֣עַמְדָה | `` !na.`am.da `` | יָּ֑חַד | `!yya.xad` | stress retraction |
| Isaiah 63:12 | בּ֤וֹקֵֽעַ | `` !bO.kE.a` `` | מַ֙יִם֙ | `!ma.yim` | stress retraction |
| Psalms 4:3 | לִ֭כְלִמָּה | `!likh.lim.ma` | תֶּאֱהָב֣וּן | `te.'6.ha.!vun` | dexi read as the stress |
| Psalms 71:9 | אַֽל־תַּ֭שְׁלִיכֵנִי | `'al-tash.!lI.khE.nI` | לְעֵ֣ת | `` l^.!`Et `` | dexi read as the stress |
| Proverbs 1:19 | כׇּל־בֹּ֣צֵֽעַ | `` kol-!bO.tsE.a` `` | בָּ֑צַע | `` !ba.tsa` `` | stress retraction |
| Proverbs 11:26 | מֹ֣נֵֽעַ | `` !mO.nE.a` `` | בָּ֭ר | `!bar` | stress retraction |
| Job 5:10 | וְשֹׁ֥לֵֽחַ | `v^.!shO.lE.ax` | מַ֝֗יִם | `!ma.yim` | stress retraction |
| 1 Chronicles 14:12 | וַיַּ֥עַזְבוּ | `` vay.!ya.`az.vu `` | שָׁ֖ם | `!sham` | stress retraction |

## 4. Class (v), the reverse: the source has a U+05BD later than the last common one

4 verse-final chanted words in all: 4 against UXLC 3.9, 3 against WLC 4.22. 1 Samuel 17:5 is the calibration case (the post-stress-meteg page's post-silluq section). 1 Kings 14:14 is in UXLC 3.9's list and not in WLC 4.22's, WLC 4.22 falling in class (i) there.

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Positions | Class | The source's marks |
|---|---|---|---|---|---|---|
| 1 Samuel 17:5 | נְחֹֽשֶׁת׃ | נְחֹֽשֶֽׁת׃ | נְחֹֽשֶֽׁת׃ | MAM 2; UXLC 2, 3; WLC 2, 3 | UXLC (v); WLC (v) | 2: penultimate nucleus; 3: last nucleus |
| 1 Kings 14:14 | גַּם־עָֽתָּה׃ | גַּם־עָֽתָּֽה׃ | גַּם־עָֽתָּה׃ | MAM 3; UXLC 3, 4; WLC 3 | UXLC (v); WLC (i) | 3: penultimate nucleus; 4: last nucleus |
| Psalms 70:2 | חֽוּשָׁה׃ | חֽוּשָֽׁה׃ | חֽוּשָֽׁה׃ | MAM 1; UXLC 1, 3; WLC 1, 3 | UXLC (v); WLC (v) | 1: penultimate nucleus; 3: last nucleus |
| Psalms 72:15 | יְבָרְכֶֽנְהוּ׃ | יְבָרֲכֶֽנְהֽוּ׃ | יְבָרֲכֶֽנְהֽוּ׃ | MAM 4; UXLC 4, 6; WLC 4, 6 | UXLC (v); WLC (v) | 4: penultimate nucleus; 6: last nucleus |

## 5. Class (iv): no common U+05BD position at all

70 verse-final chanted words in all: 68 against UXLC 3.9 (31 where UXLC records no U+05BD on the verse-final chanted word and 37 where both sides have one at disjoint positions), 46 against WLC 4.22 (22 and 24). Where the source records none, MAM's one mark is on the last nucleus in 29 of UXLC 3.9's 31 and 21 of WLC 4.22's 22, and on the penultimate nucleus in the rest (Judges 13:18, Psalms 28:7 against UXLC 3.9; Judges 13:18 against WLC 4.22): what the transcription lacks is MAM's silluq. Where the positions are disjoint, MAM's mark is on the last nucleus and the source's one or more nuclei earlier in 34 of UXLC 3.9's 37 and 22 of WLC 4.22's 24; the remaining members do not fit that shape -- against UXLC 3.9: Judges 9:2 (MAM: penultimate nucleus; the source: last nucleus); Job 6:27 (MAM: 3 nuclei before the last, last nucleus; the source: 2 nuclei before the last); Job 31:7 (MAM: before the first nucleus; the source: last nucleus); against WLC 4.22: Judges 9:2 (MAM: penultimate nucleus; the source: last nucleus); Job 31:7 (MAM: before the first nucleus; the source: last nucleus). Deuteronomy 5:17 is a dual-cantillation verse compared in MAM's combined form (section 8). No member of this class can be a meteg-after-silluq case, since no U+05BD is common to the two sides.

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Positions | Class |
|---|---|---|---|---|---|
| Genesis 32:24 | אֶת־אֲשֶׁר־לֽוֹ׃ | אֶת־אֲשֶׁר־לוֹ׃ | אֶת־אֲשֶׁר־לוֹ׃ | MAM 6; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Leviticus 26:28 | עַל־חַטֹּאתֵיכֶֽם׃ | עַל־חַטֹּאתֵיכֶם׃ | עַל־חַטֹּאתֵיכֶם׃ | MAM 8; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Numbers 27:9 | לְאֶחָֽיו׃ | לְאֶחָיו׃ | לְאֶחָיו׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Deuteronomy 5:17 | תִּֿרְצָ֖͏ֽח׃ | תִּֿרְצָ֖ח׃ | תִּרְצָֽח׃ | MAM 3; UXLC none; WLC 3 | UXLC (iv); WLC (i) |
| Deuteronomy 10:15 | הַזֶּֽה׃ | הַזֶּה׃ | הַזֶּה׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Deuteronomy 12:2 | רַעֲנָֽן׃ | רַעֲנָן׃ | רַעֲנָן׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Deuteronomy 23:18 | יִשְׂרָאֵֽל׃ | יִשְׂרָאֵל׃ | יִשְׂרָאֵל׃ | MAM 4; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Judges 9:2 | אָֽנִי׃ | אָנִֽי׃ | אָנִֽי׃ | MAM 1; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Judges 13:18 | וְהוּא־פֶֽלִאי׃ | וְהוּא־פֶ֛לִאי׃ | וְהוּא־פֶ֛לִאי׃ | MAM 5; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| 1 Samuel 19:18 | בְּנָיֽוֹת׃ | בְּנָיֽוֹת׃ | בְּנָֽיוֹת׃ | MAM 3; UXLC 3; WLC 2 | UXLC (i); WLC (iv) |
| Isaiah 13:7 | יִמָּֽס׃ | יִמָּס׃ | יִמָּס׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Hosea 8:3 | יִרְדְּפֽוֹ׃ | יִרְדְּֽפוֹ׃ | יִרְדְּֽפוֹ׃ | MAM 4; UXLC 3; WLC 3 | UXLC (iv); WLC (iv) |
| Hosea 11:7 | יְרוֹמֵֽם׃ | יְרוֹמֵם׃ | יְרוֹמֵם׃ | MAM 4; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Obadiah 1:16 | הָיֽוּ׃ | הָֽיוּ׃ | הָיֽוּ׃ | MAM 2; UXLC 1; WLC 2 | UXLC (iv); WLC (i) |
| Psalms 5:2 | הֲגִיגִֽי׃ | הֲגִֽיגִי׃ | הֲגִֽיגִי׃ | MAM 4; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Psalms 5:10 | יַחֲלִיקֽוּן׃ | יַחֲלִֽיקוּן׃ | יַחֲלִֽיקוּן׃ | MAM 5; UXLC 3; WLC 3 | UXLC (iv); WLC (iv) |
| Psalms 6:3 | עֲצָמָֽי׃ | עֲצָֽמָי׃ | עֲצָמָֽי׃ | MAM 3; UXLC 2; WLC 3 | UXLC (iv); WLC (i) |
| Psalms 9:9 | בְּמֵישָׁרִֽים׃ | בְּמֵישָֽׁרִים׃ | בְּמֵישָׁרִֽים׃ | MAM 5; UXLC 4; WLC 5 | UXLC (iv); WLC (i) |
| Psalms 14:7 | יִשְׂרָאֵֽל׃ | יִשְׂרָֽאֵל׃ | יִשְׂרָֽאֵל׃ | MAM 4; UXLC 3; WLC 3 | UXLC (iv); WLC (iv) |
| Psalms 15:2 | בִּלְבָבֽוֹ׃ | בִּלְבָֽבוֹ׃ | בִּלְבָבֽוֹ׃ | MAM 4; UXLC 3; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 15:3 | עַל־קְרֹבֽוֹ׃ | עַל־קְרֹֽבוֹ׃ | עַל־קְרֹֽבוֹ׃ | MAM 5; UXLC 4; WLC 4 | UXLC (iv); WLC (iv) |
| Psalms 17:14 | לְעוֹלְלֵיהֶֽם׃ | לְעוֹלְלֵֽיהֶם׃ | לְעוֹלְלֵיהֶֽם׃ | MAM 7; UXLC 5; WLC 7 | UXLC (iv); WLC (i) |
| Psalms 19:7 | מֵחַמָּתֽוֹ׃ | מֵֽחַמָּתוֹ׃ | מֵֽחַמָּתוֹ׃ | MAM 4; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Psalms 25:22 | צָרוֹתָֽיו׃ | צָֽרוֹתָיו׃ | צָֽרוֹתָיו׃ | MAM 4; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Psalms 28:7 | אֲהוֹדֶֽנּוּ׃ | אֲהוֹדֶנּוּ׃ | אֲהוֹדֶֽנּוּ׃ | MAM 4; UXLC none; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 31:5 | מָעוּזִּֽי׃ | מָֽעוּזִּי׃ | מָֽעוּזִּֽי׃ | MAM 4; UXLC 1; WLC 1, 4 | UXLC (iv); WLC (vi) |
| Psalms 31:19 | וָבֽוּז׃ | וָבוּז׃ | וָבֽוּז׃ | MAM 2; UXLC none; WLC 2 | UXLC (iv); WLC (i) |
| Psalms 31:20 | אָדָֽם׃ | אָדָם׃ | אָדָם׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 32:2 | רְמִיָּֽה׃ | רְמִיָּה׃ | רְמִיָּה׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 33:12 | לֽוֹ׃ | לוֹ׃ | לֽוֹ׃ | MAM 1; UXLC none; WLC 1 | UXLC (iv); WLC (i) |
| Psalms 37:31 | אֲשֻׁרָֽיו׃ | אֲשֻׁרָיו׃ | אֲשֻׁרָיו׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 37:32 | לַהֲמִיתֽוֹ׃ | לַהֲמִיתוֹ׃ | לַהֲמִיתוֹ׃ | MAM 5; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 38:15 | תּוֹכָחֽוֹת׃ | תּוֹכָֽחוֹת׃ | תּוֹכָחֽוֹת׃ | MAM 4; UXLC 3; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 39:4 | בִּלְשׁוֹנִֽי׃ | בִּלְשֽׁוֹנִי׃ | בִּלְשֽׁוֹנִי׃ | MAM 5; UXLC 3; WLC 3 | UXLC (iv); WLC (iv) |
| Psalms 48:7 | כַּיּוֹלֵדָֽה׃ | כַּיּוֹלֵֽדָה׃ | כַּיּוֹלֵֽדָה׃ | MAM 5; UXLC 4; WLC 4 | UXLC (iv); WLC (iv) |
| Psalms 55:14 | וּמְיֻדָּעִֽי׃ | וּמְיֻדָּֽעִי׃ | וּמְיֻדָּֽעִי׃ | MAM 5; UXLC 4; WLC 4 | UXLC (iv); WLC (iv) |
| Psalms 59:5 | וּרְאֵֽה׃ | וּרְאֵה׃ | וּרְאֵה׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 60:13 | אָדָֽם׃ | אָדָם׃ | אָדָם׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 62:4 | הַדְּחוּיָֽה׃ | הַדְּחוּֽיָה׃ | הַדְּחוּיָֽה׃ | MAM 5; UXLC 4; WLC 5 | UXLC (iv); WLC (i) |
| Psalms 66:2 | תְּהִלָּתֽוֹ׃ | תְּהִלָּֽתוֹ׃ | תְּהִלָּתֽוֹ׃ | MAM 4; UXLC 3; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 71:4 | וְחוֹמֵֽץ׃ | וְחוֹמֵץ׃ | וְחוֹמֵץ׃ | MAM 4; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 74:17 | יְצַרְתָּֽם׃ | יְצַרְתָּם׃ | יְצַרְתָּם׃ | MAM 4; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 78:13 | כְּמוֹ־נֵֽד׃ | כְּמוֹ־נֵד׃ | כְּמוֹ־נֵֽד׃ | MAM 4; UXLC none; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 78:41 | הִתְוֽוּ׃ | הִתְווּ׃ | הִתְווּ׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 79:12 | אֲדֹנָֽי׃ | אֲדֹֽנָי׃ | אֲדֹנָֽי׃ | MAM 3; UXLC 2; WLC 3 | UXLC (iv); WLC (i) |
| Psalms 89:7 | אֵלִֽים׃ | אֵלִים׃ | אֵלִים׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 89:41 | מְחִתָּֽה׃ | מְחִתָּה׃ | מְחִתָּה׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Psalms 89:42 | לִשְׁכֵנָֽיו׃ | לִשְׁכֵֽנָיו׃ | לִשְׁכֵנָֽיו׃ | MAM 4; UXLC 3; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 100:5 | אֱמוּנָתֽוֹ׃ | אֱמוּנָֽתוֹ׃ | אֱמוּנָתֽוֹ׃ | MAM 5; UXLC 4; WLC 5 | UXLC (iv); WLC (i) |
| Psalms 103:7 | עֲלִילוֹתָֽיו׃ | עֲלִילֽוֹתָיו׃ | עֲלִילֽוֹתָיו׃ | MAM 6; UXLC 4; WLC 4 | UXLC (iv); WLC (iv) |
| Psalms 104:29 | יְשׁוּבֽוּן׃ | יְשׁוּֽבוּ֥ן׃ | יְשׁוּבֽוּן׃ | MAM 4; UXLC 3; WLC 4 | UXLC (iv); WLC (i) |
| Psalms 106:37 | לַשֵּׁדִֽים׃ | לַשֵּֽׁדִים׃ | לַשֵּֽׁדִים׃ | MAM 3; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Psalms 107:37 | תְבוּאָֽה׃ | תְבֽוּאָה׃ | תְבֽוּאָה׃ | MAM 4; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Psalms 142:6 | הַחַיִּֽים׃ | הַֽחַיִּים׃ | הַֽחַיִּים׃ | MAM 3; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Proverbs 6:18 | לָרָעָֽה׃ | לָֽרָעָה׃ | לָֽרָעָה׃ | MAM 3; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Proverbs 8:28 | תְּהֽוֹם׃ | תְּהוֹם׃ | תְּהוֹם׃ | MAM 2; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Proverbs 24:15 | רִבְצֽוֹ׃ | רִבְצוֹ׃ | רִבְצוֹ׃ | MAM 3; UXLC none; WLC none | UXLC (iv); WLC (iv) |
| Job 6:27 | עַֽל־רֵיעֲכֶֽם׃ | עַל־רֵֽיעֲכֶ֥ם׃ | עַל־רֵֽיעֲכֶֽם׃ | MAM 1, 6; UXLC 3; WLC 3, 6 | UXLC (iv); WLC (vii) |
| Job 9:14 | עִמּֽוֹ׃ | עִמּוֹ׃ | עִמּֽוֹ׃ | MAM 2; UXLC none; WLC 2 | UXLC (iv); WLC (i) |
| Job 9:30 | כַּפָּֽי׃ | כַּפָּי׃ | כַּפָּֽי׃ | MAM 2; UXLC none; WLC 2 | UXLC (iv); WLC (i) |
| Job 10:15 | עׇנְיִֽי׃ | עָנְי֥‍ִי׃ | עָנְיִֽי׃ | MAM 3; UXLC none; WLC 3 | UXLC (iv); WLC (i) |
| Job 16:13 | מְרֵרָתִֽי׃ | מְרֵרָֽתִי׃ | מְרֵרָֽתִי׃ | MAM 4; UXLC 3; WLC 3 | UXLC (iv); WLC (iv) |
| Job 31:7 | מֽאֿוּם׃ | מֻאוּֽם׃ | מֻאֽוּם׃ | MAM 1; UXLC 3; WLC 2 | UXLC (iv); WLC (iv) |
| Job 31:33 | עֲוֺנִֽי׃ | עֲוֺֽנִי׃ | עֲוֺֽנִי׃ | MAM 3; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Job 33:30 | הַחַיִּֽים׃ | הַֽחַיִּים׃ | הַֽחַיִּים׃ | MAM 3; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Job 39:6 | מְלֵחָֽה׃ | מְלֵֽחָה׃ | מְלֵֽחָה׃ | MAM 3; UXLC 2; WLC 2 | UXLC (iv); WLC (iv) |
| Job 40:26 | לֶחֱיֽוֹ׃ | לֶֽחֱיוֹ׃ | לֶֽחֱיוֹ׃ | MAM 3; UXLC 1; WLC 1 | UXLC (iv); WLC (iv) |
| Job 41:25 | לִבְלִי־חָֽת׃ | לִבְלִי־חָת׃ | לִבְלִי־חָֽת׃ | MAM 5; UXLC none; WLC 5 | UXLC (iv); WLC (i) |
| Esther 2:21 | אֲחַשְׁוֵרֹֽשׁ׃ | אֲחַשְׁוֵרֹֽשׁ׃ | אֲחַשְׁוֵֽרֹשׁ׃ | MAM 5; UXLC 5; WLC 4 | UXLC (i); WLC (iv) |
| 2 Chronicles 28:20 | חֲזָקֽוֹ׃ | חֲזָֽקוֹ׃ | חֲזָקֽוֹ׃ | MAM 3; UXLC 2; WLC 3 | UXLC (iv); WLC (i) |

## 6. Class (vii): both sides have an extra U+05BD, neither later than the last common one

7 verse-final chanted words in all: 6 against UXLC 3.9, 7 against WLC 4.22. Each is a meteg before the stress placed on a different syllable by MAM and by the transcription, with the silluq in common; Job 6:27 is the one member WLC 4.22 has and UXLC 3.9 does not (against UXLC 3.9 it is class (iv), UXLC recording no U+05BD on its last nucleus).

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Positions | Class |
|---|---|---|---|---|---|
| Leviticus 23:3 | מוֹשְׁבֹֽתֵיכֶֽם׃ | מֽוֹשְׁבֹתֵיכֶֽם׃ | מֽוֹשְׁבֹתֵיכֶֽם׃ | MAM 4, 7; UXLC 1, 7; WLC 1, 7 | UXLC (vii); WLC (vii) |
| Numbers 15:40 | לֵאלֹֽהֵיכֶֽם׃ | לֵֽאלֹהֵיכֶֽם׃ | לֵֽאלֹהֵיכֶֽם׃ | MAM 3, 6; UXLC 1, 6; WLC 1, 6 | UXLC (vii); WLC (vii) |
| Numbers 25:2 | לֵאלֹֽהֵיהֶֽן׃ | לֵֽאלֹהֵיהֶֽן׃ | לֵֽאלֹהֵיהֶֽן׃ | MAM 3, 6; UXLC 1, 6; WLC 1, 6 | UXLC (vii); WLC (vii) |
| Deuteronomy 12:31 | לֵאלֹֽהֵיהֶֽם׃ | לֵֽאלֹהֵיהֶֽם׃ | לֵֽאלֹהֵיהֶֽם׃ | MAM 3, 6; UXLC 1, 6; WLC 1, 6 | UXLC (vii); WLC (vii) |
| 2 Kings 19:5 | אֶֽל־יְשַׁעְיָֽהוּ׃ | אֶל־יְשַֽׁעַיָֽהוּ׃ | אֶל־יְשַֽׁעַיָֽהוּ׃ | MAM 1, 6; UXLC 4, 6; WLC 4, 6 | UXLC (vii); WLC (vii) |
| Job 6:27 | עַֽל־רֵיעֲכֶֽם׃ | עַל־רֵֽיעֲכֶ֥ם׃ | עַל־רֵֽיעֲכֶֽם׃ | MAM 1, 6; UXLC 3; WLC 3, 6 | UXLC (iv); WLC (vii) |
| 2 Chronicles 33:21 | בִּירֽוּשָׁלָֽ͏ִם׃ | בִּֽירוּשָׁלָֽ͏ִם׃ | בִּֽירוּשָׁלִָֽם׃ | MAM 3, 6; UXLC 1, 6; WLC 1, 6 | UXLC (vii); WLC (vii) |

## 7. Skipped verses, and the verses compared by their final atom only

Three kinds of verse were left out of the whole-word pass, all counted:

1. **2 verses with no Hebrew in MAM** -- Joshua 21:36, Joshua 21:37, the two BHS verses MAM-simple has as a dash with `contents-corresponds-to="no verse in MAM"`. Both sources have them; there is nothing on MAM's side to compare.
2. **121 verses whose verse-final chanted word differs in base letters between MAM and the source, final atoms included** -- the same 121 against WLC 4.22 as against UXLC 3.9 (identical lists). Nearly all are a ketiv/qere where MAM's qere and the source's differ, a plene against a defective spelling, or a compound name that is one atom in MAM and two in the source. Positions in chanted words of different letters are not comparable, so these were not classified. The full list, with all three forms, is the appendix in section 13.
3. **24 verses (UXLC 3.9) and 28 (WLC 4.22) whose verse-final chanted word differs in base letters but whose final atoms agree** -- MAM having a maqaf compound where the transcription has separate atoms, or the transcription having one where MAM has separate atoms, an implicit maqaf of MAM among them -- were compared by their final atom alone, and every one came out class (i): Genesis 2:6, Exodus 12:45, Numbers 31:32, Joshua 5:1, Judges 8:10, Judges 20:2, Judges 20:35, 1 Samuel 26:11, Isaiah 28:28, Ezekiel 16:8, Ezekiel 27:25, Hosea 2:16, Malachi 3:10, Psalms 12:6, Psalms 18:20, Psalms 22:9, Psalms 78:1, Job 12:15, Job 36:12, Song of Songs 6:12, Lamentations 5:5, Ezra 8:36, Nehemiah 11:30, 1 Chronicles 21:5; WLC 4.22 adds Judges 20:33, 1 Samuel 6:18, 1 Samuel 17:15, 2 Samuel 22:6, Micah 4:8, Job 33:13.

No verse was absent from either side: MAM-simple's BHS-versification tree, UXLC 3.9 and WLC 4.22 all have 23213 verses, and the compact bcv keys matched one to one.

## 8. Verse-final atoms lacking sof pasuq, and the dual-cantillation verses

MAM's last letter-bearing atom lacks sof pasuq in 1 BHS verse: Numbers 25:19, the first half of MAM's Numbers 26:1, which BHS numbers 25:19; that atom was used as the verse-final chanted word all the same. UXLC 3.9 records no sof pasuq anywhere in 31 verses and WLC 4.22 in 27 (`.novc/mas_b_peek_no_sopa.py` spells their last atoms out): in each the transcription ends the verse on its last atom with the silluq on it and no U+05C3 after it -- Exodus 34:6 ends on a paseq instead -- so the screen took that last atom, which is the atom MAM's sof pasuq sits on in every case (a different atom would have landed the verse in the skip list). Their classes: against UXLC 3.9 (i) 31; against WLC 4.22 (i) 27. The verses:

- UXLC 3.9: Exodus 2:5, Exodus 14:25, Exodus 14:29, Exodus 20:3, Exodus 20:4, Exodus 20:8, Exodus 20:9, Exodus 20:10, Exodus 22:4, Exodus 34:6, Leviticus 18:17, Leviticus 19:1, Leviticus 26:7, Numbers 7:32, Numbers 7:40, Numbers 7:55, Numbers 7:68, Numbers 25:19, Deuteronomy 5:7, Deuteronomy 5:12, Deuteronomy 9:20, Deuteronomy 25:9, 1 Samuel 6:19, 1 Samuel 17:52, Ezekiel 33:20, Hosea 4:19, Hosea 8:9, Amos 1:14, Amos 6:6, Amos 9:5, Psalms 13:2.
- WLC 4.22: Exodus 2:5, Exodus 14:25, Exodus 14:29, Exodus 20:3, Exodus 20:4, Exodus 20:8, Exodus 20:9, Exodus 20:10, Exodus 34:6, Leviticus 18:17, Leviticus 19:1, Leviticus 26:7, Numbers 7:32, Numbers 7:40, Numbers 7:55, Numbers 7:68, Numbers 25:19, Deuteronomy 5:12, Deuteronomy 9:20, Deuteronomy 25:9, 1 Samuel 6:19, Ezekiel 33:20, Hosea 4:19, Hosea 8:9, Amos 1:14, Amos 6:6, Amos 9:5.

The 24 BHS verses whose MAM-simple element holds a `cant-all-three` (the two Decalogues) were compared in MAM's `cant-combined` form, which is what UXLC and WLC record there too; the post-stress-meteg survey's JSON records `dual_cantillation_verses_left_out: 18`, and this screen kept all of them. 23 came out UXLC (i) and WLC (i); 1 came out UXLC (iv) and WLC (i).

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Class |
|---|---|---|---|---|
| Deuteronomy 5:17 | תִּֿרְצָ֖͏ֽח׃ | תִּֿרְצָ֖ח׃ | תִּרְצָֽח׃ | UXLC (iv); WLC (i) |

## 9. WLC 4.20 against WLC 4.22: no difference the screen can see

The `out/wlc420-u` run has the same class counts, the same members of classes (iii), (iv), (v) and (vii), the same source forms for those members and the same skip lists as the `out/wlc422-u` run, so the two WLC releases tell one story here and the tables above show WLC 4.22 only.

## 10. mgketer's transcription of Mikra'ot Gedolot ha-Keter as a third screen

`C:/Users/BenDe/GitRepos/MAM-private/mgketer` compares MAM with the Mikra'ot Gedolot ha-Keter web text: `py/main_diff.py` massages both sides and writes per-book diffs (`out/<book>/<book>_diff.json`) whose categories include `mam-adds-meteg`, `mgketer-adds-meteg` and `meteg-moved`, so it does record meteg differences per atom, and its massaged mgketer verses are on disk as `out/<book>/mgketer-json-massaged/<book>_NN.json`, one token per atom. Its massaging (`documentation/massaging.md`) reorders marks and inserts the Decalogue CGJ but adds and removes no meteg, so it serves as a third screen with no more than a loader: `.novc/mas_b_mgketer.py` reads those tokens for all 39 books and runs the same comparison against MAM-simple's native-versification tree. mgketer numbers verses MAM's way: its 23202 verse keys and MAM's 23202 matched one to one, and the chapters BHS numbers differently (1 Samuel 24, Jeremiah 31, the Decalogues) skipped nothing.

Result: 23174 verses compared in the whole-word pass, 11 by final atom only, 17 skipped; classes (i) 23037, (ii) 134, (iii) 0, (iv) 1, (v) 0, (vi) 2, (vii) 0. Class (iii) is empty: 1 Kings 7:37 is class (i), mgketer having both of MAM's marks -- which agrees with mgketer's diff for 1 Kings, which records nothing at 7:37. The one class (iv) member is a transcription oddity rather than a meteg question:

| Reference | MAM | mgketer | Positions |
|---|---|---|---|
| Nehemiah 7:65 | וְתֻמִּֽים׃ | וְתֻמִּיֽם׃ | MAM 3; mgketer 4 |

Nothing was built on mgketer beyond this report, per the task. Its skipped verses (17 with differing letters) are the ketiv/qere and plene/defective differences of its diff, and are listed in `.novc/mas_b_mgketer_report.txt`.

## 11. Method: the verse-final chanted word, positions, classes, calibration

1. **Inputs.** MAM: `MAM-simple/json-vtrad-bhs` through `accgram.mam_simple_verse`, the
   repo's loader, which takes the qere side of a ketiv/qere, the `cant-combined` form of a
   dual-cantillation span, appends an implicit maqaf to the atom before it and drops
   scroll-difference notes and repeated endings. UXLC 3.9: `in/UXLC-39/*.xml`, the `<w>` and
   `<q>` elements with `<x>` note markers dropped, keyed by the `n` attributes. WLC 4.22 and
   4.20: `out/wlc422-u` and `out/wlc420-u`, `*ketiv` dropped, `**qere` kept, `{"word": ...}`
   dicts unwrapped, `sam_pe_inun` dicts dropped. All three keyed by WLC's compact bcv
   (`1k7:37`), which is BHS versification on every side.
2. **The verse-final chanted word** is the last atom holding sof pasuq plus every atom
   maqaf-joined to it (`maqaf_nonfinal_accents._join_on_maqaf`'s rule); a side with no sof
   pasuq at all uses its last letter-bearing atom and is flagged (section 8).
3. **Alignment** is by base letters, atom by atom: a verse whose verse-final chanted words
   differ in letters is skipped, or compared by final atom alone when only the grouping
   differs (section 7). Marks are compared as multisets of letter positions, never as
   strings, so the mark order within a cluster -- MAM's against UXLC's against WLC's --
   never enters.
4. **Classes**, with C the positions both sides have and last(C) the largest of them:
   (i) identical multisets; (iii) MAM has a position greater than last(C); (v) the source has
   a position greater than last(C); (iv) C is empty; (ii) MAM has extra positions, none
   greater than last(C), and the source none; (vi) the mirror of (ii); (vii) both sides have
   extra positions, none greater than last(C). Assigned in the priority (iii), (v), (iv),
   (i), (ii), (vi), (vii), so a verse where both sides have a position beyond last(C) --
   Proverbs 31:28 is the one such -- is (iii).
5. **Calibration** (the task's step 4): `mas_b_screen.py` raises unless 1 Kings 7:37 is in
   class (iii) and 1 Samuel 17:5 in class (v) for every source it screens; both held for
   UXLC 3.9, WLC 4.22 and WLC 4.20. The mgketer run is not calibrated, 1 Kings 7:37 being
   class (i) there by design.
6. **The syllable criterion** (section 1, finding 2) is the one interpretive step. It rests
   on a measurement relative to Phonetic MAM under Ben's syllable definition of 2026-09-09
   -- no verse-final stressed syllable is followed by more than one syllable -- and not on
   a claim about Hebrew: a U+05BD with two or more syllables after it is a meteg. It
   settles a member only when exactly one of MAM's marks can be the silluq. Until
   2026-09-09 it was stated a priori, as Tiberian stress falling on the last or the
   penultimate syllable, which Ben overruled that day; `.novc/mas_b_syllables.py` is the
   measurement, and section 3 lists the twelve chanted words it turns on.

## 12. Scripts and commands that re-establish every figure

All are gitignored under `.novc/` in the worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`, run from its
root with the primary clone's interpreter, in this order. Only the stress, syllables and
mgketer scripts read a sibling repo, `C:/Users/BenDe/GitRepos/MAM-private`, through
`REPOS_ROOT`; setting it does the others no harm:

```powershell
$env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_screen.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_verify_members.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_nuclei.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_stress.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_syllables.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_mgketer.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_peek_no_sopa.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_write_doc.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_b_verify_doc.py
```

1. `mas_b_screen.py` -- the screen; writes `mas_b_screen_results.json` (every figure in
   sections 2-9) and `mas_b_screen_report.txt`.
2. `mas_b_verify_members.py` -- re-reads the raw XML and JSON for every class (iii) and (v)
   member and spells both sides out as Unicode names; `mas_b_verify_members_report.txt`.
3. `mas_b_nuclei.py` -- the nucleus positions and verdicts of section 3, and the parallels;
   `mas_b_nuclei_results.json`, `mas_b_nuclei_report.txt`.
4. `mas_b_stress.py` -- the Phonetic MAM lookup of finding 5; `mas_b_stress_results.json`,
   `mas_b_stress_report.txt`.
5. `mas_b_syllables.py` -- the census of Phonetic MAM under Ben's syllable definition and
   the syllable counts of section 3 (finding 2), each member's count checked against its
   `jta`;
   `mas_b_syllables_results.json`, `mas_b_syllables_report.txt`.
6. `mas_b_mgketer.py` -- section 10; `mas_b_mgketer_results.json`, `mas_b_mgketer_report.txt`.
7. `mas_b_peek_no_sopa.py` -- the last atoms of the verses section 8 lists, as Unicode
   names; `mas_b_peek_no_sopa_report.txt`.
8. `mas_b_write_doc.py` -- writes this file from those JSON files, and asserts that the
   syllable verdicts of section 3 are the nucleus verdicts before writing.
9. `mas_b_verify_doc.py` -- checks this file line by line with `uni_denorm.has_std_mark_order`
   and reports any line opening on a Hebrew character.

The figures were measured against MAM-simple, `in/UXLC-39`, `out/wlc422-u` and
`out/wlc420-u` as committed at `30fb7681`, against Phonetic MAM as committed in MAM-private
at `3f53991`, and against mgketer's `out/` as it stood on
2026-09-09; a re-run after MAM-simple moves is a new measurement, and a
member appearing or vanishing is a finding rather than noise. What is not expected to
change: the calibration; the class (iii) list, which has been the same six for three
source runs; and the census's three figures of finding 2, unless Phonetic MAM is
regenerated.

## 13. Appendix: the verses whose verse-final chanted words differ in base letters

Union of the UXLC 3.9 and WLC 4.22 lists (section 7, kinds 2 and 3). "Final-atom pass"
marks a row whose final atoms agree and were compared (class (i) in every case); the rest
were skipped.

| Reference | MAM | UXLC 3.9 | WLC 4.22 | Disposition |
|---|---|---|---|---|
| Genesis 2:6 | הָֽאֲדָמָֽה׃ | אֶֽת־כָּל־פְּנֵֽי־הָֽאֲדָמָֽה׃ | אֶֽת־כָּל־פְּנֵֽי־הָֽאֲדָמָֽה׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Genesis 26:7 | הִֽוא׃ | הִֽיא׃ | הִֽיא׃ | UXLC: skipped; WLC: skipped |
| Genesis 35:23 | וּזְבֻלֽוּן׃ | וּזְבוּלֻֽן׃ | וּזְבוּלֻֽן׃ | UXLC: skipped; WLC: skipped |
| Genesis 46:13 | וְשִׁמְרֹֽן׃ | וְשִׁמְרֽוֹן׃ | וְשִׁמְרֽוֹן׃ | UXLC: skipped; WLC: skipped |
| Genesis 49:11 | סוּתֹֽה׃ | סוּתֽוֹ׃ | סוּתֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Exodus 12:45 | בּֽוֹ׃ | לֹא־יֹ֥אכַל־בּֽוֹ׃ | לֹא־יֹ֥אכַל־בּֽוֹ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Exodus 14:14 | תַּחֲרִשֽׁוּן׃ | תַּחֲרִישֽׁוּן׃ | תַּחֲרִישֽׁוּן׃ | UXLC: skipped; WLC: skipped |
| Leviticus 5:11 | הִֽוא׃ | הִֽיא׃ | הִֽיא׃ | UXLC: skipped; WLC: skipped |
| Numbers 1:17 | בְּשֵׁמֹֽת׃ | בְּשֵׁמֽוֹת׃ | בְּשֵׁמֽוֹת׃ | UXLC: skipped; WLC: skipped |
| Numbers 2:12 | בֶּן־צוּרִֽישַׁדָּֽי׃ | בֶּן־צוּרִֽי־שַׁדָּֽי׃ | בֶּן־צוּרִֽי־שַׁדָּֽי׃ | UXLC: skipped; WLC: skipped |
| Numbers 7:54 | בֶּן־פְּדָהצֽוּר׃ | בֶּן־פְּדָה־צֽוּר׃ | בֶּן־פְּדָה־צֽוּר׃ | UXLC: skipped; WLC: skipped |
| Numbers 7:59 | בֶּן־פְּדָהצֽוּר׃ | צֽוּר׃ | צֽוּר׃ | UXLC: skipped; WLC: skipped |
| Numbers 10:16 | בֶּן־חֵלֹֽן׃ | בֶּן־חֵלֽוֹן׃ | בֶּן־חֵלֽוֹן׃ | UXLC: skipped; WLC: skipped |
| Numbers 10:19 | בֶּן־צוּרִֽישַׁדָּֽי׃ | שַׁדָּֽי׃ | שַׁדָּֽי׃ | UXLC: skipped; WLC: skipped |
| Numbers 10:23 | בֶּן־פְּדָהצֽוּר׃ | בֶּן־פְּדָה־צֽוּר׃ | בֶּן־פְּדָה־צֽוּר׃ | UXLC: skipped; WLC: skipped |
| Numbers 20:17 | גְּבֻלֶֽךָ׃ | גְּבוּלֶֽךָ׃ | גְּבוּלֶֽךָ׃ | UXLC: skipped; WLC: skipped |
| Numbers 23:29 | אֵילִֽם׃ | אֵילִֽים׃ | אֵילִֽים׃ | UXLC: skipped; WLC: skipped |
| Numbers 31:32 | אֲלָפִֽים׃ | וַחֲמֵֽשֶׁת־אֲלָפִֽים׃ | וַחֲמֵֽשֶׁת־אֲלָפִֽים׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Numbers 35:19 | יְמִתֶֽנּוּ׃ | יְמִיתֶֽנּוּ׃ | יְמִיתֶֽנּוּ׃ | UXLC: skipped; WLC: skipped |
| Deuteronomy 3:25 | וְהַלְּבָנֹֽן׃ | וְהַלְּבָנֽוֹן׃ | וְהַלְּבָנֽוֹן׃ | UXLC: skipped; WLC: skipped |
| Deuteronomy 22:20 | לַֽנַּעֲרָֽ׃ | לַֽנַּעֲרָֽה׃ | לַֽנַּעֲרָֽה׃ | UXLC: skipped; WLC: skipped |
| Joshua 5:1 | יִשְׂרָאֵֽל׃ | בְּנֵֽי־יִשְׂרָאֵֽל׃ | בְּנֵֽי־יִשְׂרָאֵֽל׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Joshua 15:8 | צָפֽוֹנָה׃ | צָפֹֽנָה׃ | צָפֹֽנָה׃ | UXLC: skipped; WLC: skipped |
| Joshua 21:10 | רִאישֹׁנָֽה׃ | רִיאשֹׁנָֽה׃ | רִיאשֹׁנָֽה׃ | UXLC: skipped; WLC: skipped |
| Judges 8:10 | שֹׁ֥לֵֽף־חָֽרֶב׃ | חָֽרֶב׃ | חָֽרֶב׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Judges 11:31 | עֹלָֽה׃ | עוֹלָֽה׃ | עוֹלָֽה׃ | UXLC: skipped; WLC: skipped |
| Judges 16:23 | אוֹיְבֵֽנוּ׃ | אוֹיְבֵֽינוּ׃ | אוֹיְבֵֽינוּ׃ | UXLC: skipped; WLC: skipped |
| Judges 20:2 | שֹׁ֥לֵֽף־חָֽרֶב׃ | חָֽרֶב׃ | חָֽרֶב׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Judges 20:33 | גָֽבַע׃ | גָֽבַע׃ | מִמַּֽעֲרֵה־גָֽבַע׃ | UXLC: letters agree; WLC: final-atom pass |
| Judges 20:35 | שֹׁ֥לֵֽף־חָֽרֶב׃ | חָֽרֶב׃ | חָֽרֶב׃ | UXLC: final-atom pass; WLC: final-atom pass |
| 1 Samuel 2:20 | לִמְקוֹמֽוֹ׃ | לִמְקֹמֽוֹ׃ | לִמְקֹמֽוֹ׃ | UXLC: skipped; WLC: skipped |
| 1 Samuel 6:18 | הַשִּׁמְשִֽׁי׃ | הַשִּׁמְשִֽׁי׃ | בֵּֽית־הַשִּׁמְשִֽׁי׃ | UXLC: letters agree; WLC: final-atom pass |
| 1 Samuel 17:15 | לָֽחֶם׃ | לָֽחֶם׃ | בֵּֽית־לָֽחֶם׃ | UXLC: letters agree; WLC: final-atom pass |
| 1 Samuel 21:12 | בְּרִבְבֹתָֽו׃ | בְּרִבְבֹתָֽיו׃ | בְּרִבְבֹתָֽיו׃ | UXLC: skipped; WLC: skipped |
| 1 Samuel 26:5 | סְבִיבֹתָֽו׃ | סְבִיבֹתָֽיו׃ | סְבִיבֹתָֽיו׃ | UXLC: skipped; WLC: skipped |
| 1 Samuel 26:7 | סְבִיבֹתָֽו׃ | סְבִיבֹתָֽיו׃ | סְבִיבֹתָֽיו׃ | UXLC: skipped; WLC: skipped |
| 1 Samuel 26:11 | וְנֵלְכָה־לָּֽנוּ׃ | לָּֽנוּ׃ | לָּֽנוּ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| 1 Samuel 26:16 | מְרַאֲשֹׁתָֽו׃ | מְרַאֲשֹׁתָֽיו׃ | מְרַאֲשֹׁתָֽיו׃ | UXLC: skipped; WLC: skipped |
| 1 Samuel 29:5 | בְּרִבְבֹתָֽו׃ | בְּרִבְבֹתָֽיו׃ | בְּרִבְבֹתָֽיו׃ | UXLC: skipped; WLC: skipped |
| 2 Samuel 2:30 | וַעֲשָׂהאֵֽל׃ | וַעֲשָׂה־אֵֽל׃ | וַעֲשָׂה־אֵֽל׃ | UXLC: skipped; WLC: skipped |
| 2 Samuel 18:15 | וַיְמִתֻֽהוּ׃ | וַיְמִיתֻֽהוּ׃ | וַיְמִיתֻֽהוּ׃ | UXLC: skipped; WLC: skipped |
| 2 Samuel 18:17 | לְאֹהָלָֽו׃ | לְאֹהָלָֽיו׃ | לְאֹהָלָֽיו׃ | UXLC: skipped; WLC: skipped |
| 2 Samuel 19:2 | עַל־אַבְשָׁלֽוֹם׃ | עַל־אַבְשָׁלֹֽם׃ | עַל־אַבְשָׁלֹֽם׃ | UXLC: skipped; WLC: skipped |
| 2 Samuel 22:6 | מָֽוֶת׃ | מָֽוֶת׃ | מֹֽקְשֵׁי־מָֽוֶת׃ | UXLC: letters agree; WLC: final-atom pass |
| 1 Kings 6:4 | אֲטוּמִֽים׃ | אֲטֻמִֽים׃ | אֲטֻמִֽים׃ | UXLC: skipped; WLC: skipped |
| 1 Kings 18:42 | בִּרְכָּֽו׃ | בִּרְכָּֽיו׃ | בִּרְכָּֽיו׃ | UXLC: skipped; WLC: skipped |
| 1 Kings 22:7 | מֵאֹתֽוֹ׃ | מֵאוֹתֽוֹ׃ | מֵאוֹתֽוֹ׃ | UXLC: skipped; WLC: skipped |
| 2 Kings 14:12 | לְאֹהָלָֽו׃ | לְאֹהָלָֽיו׃ | לְאֹהָלָֽיו׃ | UXLC: skipped; WLC: skipped |
| 2 Kings 18:17 | כֹבֵֽס׃ | כוֹבֵֽס׃ | כוֹבֵֽס׃ | UXLC: skipped; WLC: skipped |
| 2 Kings 18:31 | מֵי־בֹרֽוֹ׃ | מֵֽי־בוֹרֽוֹ׃ | מֵֽי־בוֹרֽוֹ׃ | UXLC: skipped; WLC: skipped |
| 2 Kings 18:37 | רַבְשָׁקֵֽה׃ | רַב־שָׁקֵֽה׃ | רַב־שָׁקֵֽה׃ | UXLC: skipped; WLC: skipped |
| Isaiah 28:28 | יְדֻקֶּֽנּוּ׃ | לֹֽא־יְדֻקֶּֽנּוּ׃ | לֹֽא־יְדֻקֶּֽנּוּ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Isaiah 29:15 | יֹֽדְעֵֽנוּ׃ | יוֹדְעֵֽנוּ׃ | יוֹדְעֵֽנוּ׃ | UXLC: skipped; WLC: skipped |
| Isaiah 36:22 | רַבְשָׁקֵֽה׃ | שָׁקֵֽה׃ | רַב־שָׁקֵֽה׃ | UXLC: skipped; WLC: skipped |
| Isaiah 42:4 | יְיַחֵֽלוּ׃ | יְיַחֵֽילוּ׃ | יְיַחֵֽילוּ׃ | UXLC: skipped; WLC: skipped |
| Isaiah 44:25 | יְסַכֵּֽל׃ | יְשַׂכֵּֽל׃ | יְשַׂכֵּֽל׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 4:3 | אֶל־קֹצִֽים׃ | אֶל־קוֹצִֽים׃ | אֶל־קוֹצִֽים׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 5:6 | מְשֻׁבוֹתֵיהֶֽם׃ | מְשׁוּבוֹתֵיהֶֽם׃ | מְשׁוּבוֹתֵיהֶֽם׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 5:7 | יִתְגּוֹדָֽדוּ׃ | יִתְגֹּדָֽדוּ׃ | יִתְגֹּדָֽדוּ׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 18:9 | וְלִנְטֽוֹעַ׃ | וְלִנְטֹֽעַ׃ | וְלִנְטֹֽעַ׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 50:39 | וָדֹֽר׃ | וָדֽוֹר׃ | וָדֽוֹר׃ | UXLC: skipped; WLC: skipped |
| Jeremiah 52:2 | יְהוֹיָקִֽם׃ | יְהוֹיָקִֽים׃ | יְהוֹיָקִֽים׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 7:3 | כׇּל־תּוֹעֲבוֹתָֽיִךְ׃ | כָּל־תּוֹעֲבֹתָֽיִךְ׃ | כָּל־תּוֹעֲבֹתָֽיִךְ׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 16:8 | וַתִּֽהְיִי־לִֽי׃ | לִֽי׃ | לִֽי׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Ezekiel 17:6 | פֹּרֹֽאות׃ | פֹּארֽוֹת׃ | פֹּארֽוֹת׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 27:6 | כִּתִּיִּֽם׃ | כִּתִּיִּֽים׃ | כִּתִּיִּֽים׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 27:25 | יַמִּֽים׃ | בְּלֵ֥ב־יַמִּֽים׃ | בְּלֵ֥ב־יַמִּֽים׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Ezekiel 30:4 | יְסֹדוֹתֶֽיהָ׃ | יְסוֹדֹתֶֽיהָ׃ | יְסוֹדֹתֶֽיהָ׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 37:16 | חֲבֵרָֽו׃ | חֲבֵרָֽיו׃ | חֲבֵרָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 40:26 | אֶל־אֵילָֽו׃ | אֶל־אֵילָֽיו׃ | אֶל־אֵילָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 40:31 | מַעֲלָֽו׃ | מַעֲלָֽיו׃ | מַעֲלָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 40:34 | מַעֲלָֽו׃ | מַעֲלָֽיו׃ | מַעֲלָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 40:37 | מַעֲלָֽו׃ | מַעֲלָֽיו׃ | מַעֲלָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 43:26 | יָדָֽו׃ | יָדָֽיו׃ | יָדָֽיו׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 48:15 | בְּתוֹכֹֽה׃ | בְּתוֹכֽוֹ׃ | בְּתוֹכֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Ezekiel 48:21 | בְּתוֹכֹֽה׃ | בְּתוֹכֽוֹ׃ | בְּתוֹכֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Hosea 2:16 | עַל־לִבָּֽהּ׃ | לִבָּֽהּ׃ | לִבָּֽהּ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Amos 1:10 | אַרְמְנוֹתֶֽיהָ׃ | אַרְמְנֹתֶֽיהָ׃ | אַרְמְנֹתֶֽיהָ׃ | UXLC: skipped; WLC: skipped |
| Micah 2:7 | הֹלֵֽךְ׃ | הוֹלֵֽךְ׃ | הוֹלֵֽךְ׃ | UXLC: skipped; WLC: skipped |
| Micah 4:8 | יְרוּשָׁלָֽ͏ִם׃ | יְרוּשָׁלָֽ͏ִם׃ | לְבַ֥ת־יְרוּשָׁלִָֽם׃ | UXLC: letters agree; WLC: final-atom pass |
| Malachi 3:4 | קַדְמֹנִיֹּֽת׃ | קַדְמֹנִיּֽוֹת׃ | קַדְמֹנִיּֽוֹת׃ | UXLC: skipped; WLC: skipped |
| Malachi 3:10 | עַד־בְּלִי־דָֽי׃ | דָֽי׃ | עַד־בְּלִי־דָֽי׃ | UXLC: final-atom pass; WLC: letters agree |
| Psalms 12:6 | יָפִ֥יחַֽ־לֽוֹ׃ | לֽוֹ׃ | לֽוֹ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Psalms 18:20 | כִּ֘י־חָ֥פֵֽץ־בִּֽי׃ | בִּֽי׃ | בִּֽי׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Psalms 22:9 | כִּ֘י־חָ֥פֵֽץ־בּֽוֹ׃ | בּֽוֹ׃ | בּֽוֹ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Psalms 35:21 | עֵינֵֽנוּ׃ | עֵינֵֽינוּ׃ | עֵינֵֽינוּ׃ | UXLC: skipped; WLC: skipped |
| Psalms 44:15 | בַּלְאֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | UXLC: skipped; WLC: skipped |
| Psalms 45:8 | מֵחֲבֵרֶֽךָ׃ | מֵֽחֲבֵרֶֽיךָ׃ | מֵֽחֲבֵרֶֽיךָ׃ | UXLC: skipped; WLC: skipped |
| Psalms 57:10 | בַּלְאֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | UXLC: skipped; WLC: skipped |
| Psalms 60:10 | הִתְרוֹעָֽעִי׃ | הִתְרֹעָֽעִֽי׃ | הִתְרֹעָֽעִֽי׃ | UXLC: skipped; WLC: skipped |
| Psalms 68:21 | תֹּצָאֽוֹת׃ | תּוֹצָאֽוֹת׃ | תּוֹצָאֽוֹת׃ | UXLC: skipped; WLC: skipped |
| Psalms 78:1 | לְאִמְרֵי־פִֽי׃ | פִֽי׃ | לְאִמְרֵי־פִֽי׃ | UXLC: final-atom pass; WLC: letters agree |
| Psalms 83:12 | כׇּל־נְסִיכֵֽימוֹ׃ | כָּל־נְסִיכֵֽמוֹ׃ | כָּל־נְסִיכֵֽמוֹ׃ | UXLC: skipped; WLC: skipped |
| Psalms 89:18 | קַרְנֵֽינוּ׃ | קַרְנֵֽנוּ׃ | קַרְנֵֽנוּ׃ | UXLC: skipped; WLC: skipped |
| Psalms 103:3 | לְכׇל־תַּחֲלוּאָֽיְכִי׃ | לְכָל־תַּחֲלֻאָֽיְכִי׃ | לְכָל־תַּחֲלֻאָֽיְכִי׃ | UXLC: skipped; WLC: skipped |
| Psalms 106:45 | חֲסָדָֽו׃ | חֲסָדָֽיו׃ | חֲסָדָֽיו׃ | UXLC: skipped; WLC: skipped |
| Psalms 108:4 | בַּלְאֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | UXLC: skipped; WLC: skipped |
| Psalms 119:87 | פִקֻּדֶֽיךָ׃ | פִקֻּודֶֽיךָ׃ | פִקֻּודֶֽיךָ׃ | UXLC: skipped; WLC: skipped |
| Psalms 122:5 | דָּוִֽד׃ | דָּוִֽיד׃ | דָּוִֽיד׃ | UXLC: skipped; WLC: skipped |
| Psalms 123:4 | יוֹנִֽים׃ | לִגְאֵ֥יוֹנִֽים׃ | לִגְאֵ֥יוֹנִֽים׃ | UXLC: skipped; WLC: skipped |
| Psalms 135:6 | וְכׇל־תְּהֹמֽוֹת׃ | וְכָל־תְּהוֹמֽוֹת׃ | וְכָל־תְּהוֹמֽוֹת׃ | UXLC: skipped; WLC: skipped |
| Psalms 140:10 | יְכַסֵּֽימוֹ׃ | יְכַסֵּֽמוֹ׃ | יְכַסֵּֽמוֹ׃ | UXLC: skipped; WLC: skipped |
| Psalms 145:13 | וָדֹֽר׃ | וָדֽוֹר׃ | וָדֽוֹר׃ | UXLC: skipped; WLC: skipped |
| Psalms 148:2 | כׇּל־צְבָאָֽו׃ | כָּל־צְבָאָֽיו׃ | כָּל־צְבָאָֽיו׃ | UXLC: skipped; WLC: skipped |
| Psalms 149:7 | בַּלְאֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | בַּל־אֻמִּֽים׃ | UXLC: skipped; WLC: skipped |
| Psalms 150:4 | וְעֻגָֽב׃ | וְעוּגָֽב׃ | וְעוּגָֽב׃ | UXLC: skipped; WLC: skipped |
| Proverbs 1:3 | וּמֵשָׁרִֽים׃ | וּמֵישָׁרִֽים׃ | וּמֵישָׁרִֽים׃ | UXLC: skipped; WLC: skipped |
| Proverbs 1:9 | לְגַרְגְּרֹתֶֽךָ׃ | לְגַרְגְּרֹתֶֽיךָ׃ | לְגַרְגְּרֹתֶֽיךָ׃ | UXLC: skipped; WLC: skipped |
| Proverbs 4:15 | וַעֲבֹֽר׃ | וַעֲבֽוֹר׃ | וַעֲבֽוֹר׃ | UXLC: skipped; WLC: skipped |
| Proverbs 15:5 | יַעְרִֽים׃ | יַעְרִֽם׃ | יַעְרִֽם׃ | UXLC: skipped; WLC: skipped |
| Proverbs 18:11 | בְּמַשְׂכִּתֽוֹ׃ | בְּמַשְׂכִּיתֽוֹ׃ | בְּמַשְׂכִּיתֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Proverbs 31:17 | זְרוֹעֹתֶֽיהָ׃ | זְרֹעוֹתֶֽיהָ׃ | זְרֹעוֹתֶֽיהָ׃ | UXLC: skipped; WLC: skipped |
| Job 5:12 | תֻּשִׁיָּֽה׃ | תּוּשִׁיָּֽה׃ | תּוּשִׁיָּֽה׃ | UXLC: skipped; WLC: skipped |
| Job 10:11 | תְּשֹׂכְכֵֽנִי׃ | תְּסֹכְכֵֽנִי׃ | תְּסֹכְכֵֽנִי׃ | UXLC: skipped; WLC: skipped |
| Job 11:13 | כַּפֶּֽיךָ׃ | כַּפֶּֽךָ׃ | כַּפֶּֽךָ׃ | UXLC: skipped; WLC: skipped |
| Job 12:15 | וְיַ֖הַפְכוּ־אָֽרֶץ׃ | אָֽרֶץ׃ | אָֽרֶץ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Job 14:5 | יַעֲבֹֽר׃ | יַעֲבֽוֹר׃ | יַעֲבֽוֹר׃ | UXLC: skipped; WLC: skipped |
| Job 16:19 | בַּמְּרֹמִֽים׃ | בַּמְּרוֹמִֽים׃ | בַּמְּרוֹמִֽים׃ | UXLC: skipped; WLC: skipped |
| Job 20:12 | לְשֹׁנֽוֹ׃ | לְשׁוֹנֽוֹ׃ | לְשׁוֹנֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Job 20:22 | תְּבֹאֶֽנּוּ׃ | תְּבוֹאֶֽנּוּ׃ | תְּבוֹאֶֽנּוּ׃ | UXLC: skipped; WLC: skipped |
| Job 26:13 | בָּרִֽחַ׃ | בָּרִֽיחַ׃ | בָּרִֽיחַ׃ | UXLC: skipped; WLC: skipped |
| Job 33:13 | יַעֲנֶֽה׃ | יַעֲנֶֽה׃ | לֹ֣א־יַעֲנֶֽה׃ | UXLC: letters agree; WLC: final-atom pass |
| Job 36:12 | בִּבְלִי־דָֽעַת׃ | כִּבְלִי־דָֽעַת׃ | כִּבְלִי־דָֽעַת׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Song of Songs 4:4 | הַגִּבֹּרִֽים׃ | הַגִּבּוֹרִֽים׃ | הַגִּבּוֹרִֽים׃ | UXLC: skipped; WLC: skipped |
| Song of Songs 6:12 | נָדִֽיב׃ | עַמִּי־נָדִֽיב׃ | עַמִּי־נָדִֽיב׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Song of Songs 8:13 | הַשְׁמִיעִֽנִי׃ | הַשְׁמִיעִֽינִי׃ | הַשְׁמִיעִֽינִי׃ | UXLC: skipped; WLC: skipped |
| Lamentations 1:21 | כָמֹֽנִי׃ | כָמֽוֹנִי׃ | כָמֽוֹנִי׃ | UXLC: skipped; WLC: skipped |
| Lamentations 3:39 | עַל־חֲטָאָֽו׃ | עַל־חֲטָאָֽיו׃ | עַל־חֲטָאָֽיו׃ | UXLC: skipped; WLC: skipped |
| Lamentations 4:11 | יְסֹדֹתֶֽיהָ׃ | יְסוֹדֹתֶֽיהָ׃ | יְסוֹדֹתֶֽיהָ׃ | UXLC: skipped; WLC: skipped |
| Lamentations 4:18 | קִצֵּֽנוּ׃ | קִצֵּֽינוּ׃ | קִצֵּֽינוּ׃ | UXLC: skipped; WLC: skipped |
| Lamentations 5:5 | הֽוּנַֽח־לָֽנוּ׃ | לָֽנוּ׃ | לָֽנוּ׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Ecclesiastes 12:5 | הַסּוֹפְדִֽים׃ | הַסֹּפְדִֽים׃ | הַסֹּפְדִֽים׃ | UXLC: skipped; WLC: skipped |
| Esther 2:3 | תַּמְרֻקֵיהֶֽן׃ | תַּמְרוּקֵיהֶֽן׃ | תַּמְרוּקֵיהֶֽן׃ | UXLC: skipped; WLC: skipped |
| Esther 9:22 | לָֽאֶבְיֹנִֽים׃ | לָֽאֶבְיוֹנִֽים׃ | לָֽאֶבְיוֹנִֽים׃ | UXLC: skipped; WLC: skipped |
| Daniel 3:3 | נְבֻכַדְנֶצַּֽר׃ | נְבוּכַדְנֶצַּֽר׃ | נְבוּכַדְנֶצַּֽר׃ | UXLC: skipped; WLC: skipped |
| Daniel 5:19 | מַשְׁפִּֽל׃ | מַשְׁפִּֽיל׃ | מַשְׁפִּֽיל׃ | UXLC: skipped; WLC: skipped |
| Daniel 7:21 | לְהֹֽן׃ | לְהֽוֹן׃ | לְהֽוֹן׃ | UXLC: skipped; WLC: skipped |
| Daniel 11:10 | עַד־מָעֻזֹּֽה׃ | עַד־מָעֻזּֽוֹ׃ | עַד־מָעֻזּֽוֹ׃ | UXLC: skipped; WLC: skipped |
| Daniel 11:29 | וְכָאַחֲרוֹנָֽה׃ | וְכָאַחֲרֹנָֽה׃ | וְכָאַחֲרֹנָֽה׃ | UXLC: skipped; WLC: skipped |
| Daniel 11:31 | מְשֹׁמֵֽם׃ | מְשׁוֹמֵֽם׃ | מְשׁוֹמֵֽם׃ | UXLC: skipped; WLC: skipped |
| Ezra 8:36 | הָאֱלֹהִֽים׃ | וְאֶת־בֵּֽית־הָאֱלֹהִֽים׃ | וְאֶת־בֵּֽית־הָאֱלֹהִֽים׃ | UXLC: final-atom pass; WLC: final-atom pass |
| Nehemiah 7:65 | וְתֻמִּֽים׃ | וְתוּמִּֽים׃ | וְתוּמִּֽים׃ | UXLC: skipped; WLC: skipped |
| Nehemiah 11:30 | הִנֹּֽם׃ | עַד־גֵּֽיא־הִנֹּֽם׃ | עַד־גֵּֽיא־הִנֹּֽם׃ | UXLC: final-atom pass; WLC: final-atom pass |
| 1 Chronicles 2:13 | הַשְּׁלִשִֽׁי׃ | הַשְּׁלִישִֽׁי׃ | הַשְּׁלִישִֽׁי׃ | UXLC: skipped; WLC: skipped |
| 1 Chronicles 6:4 | לַאֲבֹתֵיהֶֽם׃ | לַאֲבוֹתֵיהֶֽם׃ | לַאֲבוֹתֵיהֶֽם׃ | UXLC: skipped; WLC: skipped |
| 1 Chronicles 11:42 | שְׁלֹשִֽׁים׃ | שְׁלוֹשִֽׁים׃ | שְׁלוֹשִֽׁים׃ | UXLC: skipped; WLC: skipped |
| 1 Chronicles 21:5 | שֹׁ֥לֵֽף־חָֽרֶב׃ | חָֽרֶב׃ | חָֽרֶב׃ | UXLC: final-atom pass; WLC: final-atom pass |
| 1 Chronicles 23:23 | שְׁלוֹשָֽׁה׃ | שְׁלֹשָֽׁה׃ | שְׁלֹשָֽׁה׃ | UXLC: skipped; WLC: skipped |
| 1 Chronicles 25:4 | מַחֲזִיאֹֽת׃ | מַחֲזִיאֽוֹת׃ | מַחֲזִיאֽוֹת׃ | UXLC: skipped; WLC: skipped |
| 2 Chronicles 3:5 | וְשַׁרְשְׁרֹֽת׃ | וְשַׁרְשְׁרֽוֹת׃ | וְשַׁרְשְׁרֽוֹת׃ | UXLC: skipped; WLC: skipped |
| 2 Chronicles 32:28 | לָאֲוֵרֹֽת׃ | לָאֲוֵרֽוֹת׃ | לָאֲוֵרֽוֹת׃ | UXLC: skipped; WLC: skipped |
