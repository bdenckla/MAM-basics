# Where the ETCBC's BHSA "corrects" its own text

Written by Claude (Opus 5.5) on 2026-11-13, New York time, in a session that the commander
session "Commander for Claude's forests" (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) started
from the brief
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/bhsa-corrections-brief-2026-11-13.md`,
which quotes Ben's request. Everything here is Claude's work and has not been reviewed by a
human. Nothing tracked changed, nothing was committed, and nothing was posted anywhere.

Every statement about a form is about a transcription: the BHSA's, WLC's, the UXLC's or MAM's.
No image of the Leningrad Codex was consulted, and nothing here says what the codex has.

## Part 1: the cases of the review of the Israel Bible

### The answer

The review has 56 cases: forms.json's 43 rows, the tour table's 5 rows in review.md and the
Decalogue table's 8. The BHSA 2021 was read at each, at the same reference, and its analysis
judged against its own written atom and against MAM's form.

1. **The BHSA corrects 4 of the 56 (class b):** Exodus 10:28, where its atom has segol and its
   analysis is the negative; Judges 19:23 and Jeremiah 47:6, where its atom has pataḥ and its
   analysis is the preposition; and 2 Samuel 11:1, where its lexeme is "king" against the
   vowels of "messengers" on mem and lamed, though its atom's rafeh on the alef already fits
   "kings". These four are the review's al/el rows that the MACULA session found, and the
   messengers-or-kings row.
2. **At 7, its analysis follows its written atom against MAM's form (class a):** Deuteronomy
   2:9 and Joshua 22:19, segol read as the preposition (though placed inside the verb's
   phrase, not in a prepositional phrase); Judges 19:4, a qal where MAM has a hiphil; Isaiah
   66:22, the noun "month" where MAM has the adjective "new"; Proverbs 12:9, a tif‘al
   participle where MAM has a hitpael; and 2 Samuel 13:33 and 15:21, a pointed and read
   conjunction where MAM has a word written but not read.
3. **At 7, the BHSA's own text has MAM's form where WLC 4.18 does not (class d), and its
   analysis fits both:** Judges 15:14, 2 Kings 18:27's qere, Deuteronomy 3:22, Isaiah 49:23,
   Lamentations 3:25, Lamentations 4:4 and Ecclesiastes 2:23. These are not corrections by
   the analysis. At six of them WLC 4.18's own notes say that WLC reads L differently from
   BHS (v, or q for a ketiv and qere), so the BHSA, a transcription of BHS, plausibly has
   BHS's form; at Isaiah 49:23, with no WLC note, the BHSA's way of writing a ḥolam before a
   vav may explain it. BHS itself was not read.
4. **At the other 38, the analysis fits both forms (class c):** the difference is in pointing
   that does not decide the lexeme, the stem or the tense.
5. **The six verses of the review's footnote on ḥataf vowels under non-gutturals**
   (`mam-hataf-ng`) are all class c: the BHSA has WLC 4.18's atom at each.

### How each case was found and compared

`scripts/part1_cases.py` follows the morphhb session's method. For each case and each side of
every ketiv and qere, MAM's verse (MAM-simple, BHS versification, read by the review's lint's own
functions) and WLC 4.18's verse (Sefaria-Data's copy of tanach.us's build 24.2, in GitRepos2's
`.novc/wlc418-tanach-us/`) were split into atoms and aligned by letters; the case's place is
where WLC 4.18's atoms match the Israel Bible's form and MAM's aligned atoms match MAM's form,
both by the review's key (`israel_bible_review_index.key`). The BHSA's verse, at the same
reference and its Latin book name, was split into atoms from its slots (`g_word_utf8` and
`trailer_utf8`; an atom ends at a trailer with a space or a maqaf) and aligned with WLC 4.18's
by letters. All 56 cases were found at the same reference in all four texts, so the review's
references, the lint's BHS versification and the BHSA's agree at every case, and the BHSA's
atoms there have WLC 4.18's letters, except the BHSA's qere at Lamentations 3:25, which has a
yod (`out/34-check-letters.txt`). WLC 4.20, WLC 4.22
and UXLC 2.6 (`in/UXLC-39`) are reported beside them.

Three facts about the BHSA's text govern the comparison:

1. **The BHSA writes a ḥolam male as a ḥolam on the letter before the vav**, its
   transliteration's `O` before `W`, where WLC and MAM put the ḥolam male dot on the vav. The
   comparison key `bkey` moves such a dot back before comparing (`bc_common.holam_to_prev`).
   Without it, five cases (2 Samuel 13:33, Hosea 2:17, Psalms 45:3, Song of Songs 5:11,
   Nehemiah 9:14) would differ from WLC in that alone.
2. **For a ketiv, `g_word_utf8` has the ketiv's letters unpointed**, `qere_utf8` the pointed
   qere, and `kq_hybrid_utf8` the ketiv's letters with the qere's points (sometimes ending with
   a sof pasuq). The ketiv side of the comparison uses `kq_hybrid_utf8`, as tanach.us's `<k>`
   elements are pointed alike; the qere side uses `qere_utf8`.
3. **The review's key ignores accents.** By the full key, the BHSA also differs from WLC at
   Deuteronomy 2:9's second atom and Isaiah 23:8, by one accent code point: HEBREW ACCENT QADMA
   where WLC has the first of two HEBREW ACCENT PASHTA marks.

**Ketiv and qere, apart from the corrections.** Three cases touch the BHSA's ketiv and qere: 2
Kings 18:27, whose form is a qere (the BHSA's ketiv is two slots, each with its own qere);
Lamentations 3:25, where the BHSA has a ketiv and qere that WLC (note q) abandoned and MAM does
not have; and Ezra 4:9 among the footnote's verses. 2 Samuel 13:33 and 15:21, words written but
not read in MAM, have no qere and no special marking in the BHSA.

WLC 4.18's notes, from its own table (`out/03-wlc418-notes-table.txt`): 1, "BHS has been
faithful to the Leningrad Codex where there might be a question of the validity of the form";
n, an anomalous form; v, "We read one or more vowels in L differently from BHS"; c, the same for
accents; q, "We have abandoned or added a ketib/qere relative to BHS"; Q, "we agree with BHQ
against BHS"; U, "We agree with both BHS 1997 and BHQ on an unexpected reading".

### The table

Columns: the review's two forms as the page shows them; the BHSA's atoms at the place, stripped
of accents as the page strips its forms and in MAM-normal mark order (the raw atoms are in
`out/10-part1-cases.txt`); the BHSA's analysis of each of its words (slots): lexeme, part of
speech, stem and tense for a verb, pronominal suffix, the phrase's type and function, and the
lexeme's gloss.

| # | Verse | Israel Bible (WLC 4.18) | MAM | BHSA | BHSA's analysis, word by word | Class | Why |
|---|---|---|---|---|---|---|---|
| 1 | Genesis 32:18 | וִשְׁאֵלְךָ | וּשְׁאֵלְךָ | וִשְׁאֵלְךָ | `W` conj (CP Conj) 'and'; `C>L[` verb qal perf suffix `K` (VP PreO) 'ask' | **c** | The conjunction `W` and a qal perfect; the conjunction's vowel does not bear on the analysis. |
| 2 | Genesis 34:11 | אָבִיה | אָבִיהָ | אָבִיה | `>B/` subs suffix `H` (PP Cmpl) 'father' | **c** | Suffix `H` (third feminine singular) on `>B/` 'father': the analysis has the suffix that both spell, though WLC's he has no qamats. |
| 3 | Exodus 1:3 | וּבְנְיָמִן | וּבִנְיָמִן | וּבְנְיָמִן | `W` conj (PrNP Subj) 'and'; `BNJMN/` nmpr (PrNP Subj) 'Benjamin' | **c** | The conjunction and the name `BNJMN/`. |
| 4 | Exodus 10:28 | אֶל־ | אַל־ | אֶל־ | `>L=` nega (NegP Nega) 'not' | **b** | Written with segol, analysed as the negative: lexeme `>L=`, part of speech `nega`, its own phrase `NegP` with function `Nega`, in a clause of type `xYq0`. |
| 5 | Numbers 2:14 | וְמַטֵּה | וּמַטֵּה | וְמַטֵּה | `W` conj (CP Conj) 'and'; `MVH/` subs (NP Subj) 'staff' | **c** | The conjunction and `MVH/` 'staff'. |
| 6 | Numbers 26:7 | הָרֻאוּבֵנִי | הָראֿוּבֵנִי | הָרֻאוּבֵנִי | `H` art (NP PreC) 'the'; `R>WBNJ/` adjv (NP PreC) 'Reubenite' | **c** | The article and the gentilic `R>WBNJ/`. |
| 7 | Deuteronomy 2:9 | אֶל־תָּצַר | אַל־תָּצַר | אֶל־תָּצַר | `>L` prep (VP Pred) 'to'; `YWR=[` verb qal impf (VP Pred) 'damage' | **a** | Written with segol and analysed as the preposition `>L`, but placed inside the verb's phrase (`VP`, `Pred`) rather than in a `PP`; no `NegP`. Its clause type is `ZYq0`, where Exodus 10:28's, with its `NegP`, is `xYq0`. The BHSA's next atom differs from WLC's in one accent code point: HEBREW ACCENT QADMA where WLC has the first of two HEBREW ACCENT PASHTA marks. |
| 8 | Deuteronomy 3:12 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי | `L` prep (PP Cmpl) 'to'; `H` art (PP Cmpl) 'the'; `R>WBNJ/` adjv (PP Cmpl) 'Reubenite' | **c** | Preposition, an unwritten article, and `R>WBNJ/`. |
| 9 | Deuteronomy 3:16 | וְלָרֻאוּבֵנִי | וְלָראֿוּבֵנִי | וְלָרֻאוּבֵנִי | `W` conj (CP Conj) 'and'; `L` prep (PP Cmpl) 'to'; `H` art (PP Cmpl) 'the'; `R>WBNJ/` adjv (PP Cmpl) 'Reubenite' | **c** | As at Deuteronomy 3:12, with the conjunction. |
| 10 | Deuteronomy 4:43 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי | `L` prep (PP Adju) 'to'; `H` art (PP Adju) 'the'; `R>WBNJ/` adjv (PP Adju) 'Reubenite' | **c** | As at Deuteronomy 3:12. |
| 11 | Joshua 12:6 | לָרֻאוּבֵנִי | לָראֿוּבֵנִי | לָרֻאוּבֵנִי | `L` prep (PP Cmpl) 'to'; `H` art (PP Cmpl) 'the'; `R>WBNJ/` adjv (PP Cmpl) 'Reubenite' | **c** | As at Deuteronomy 3:12. |
| 12 | Joshua 22:19 | אֶל־תִּמְרֹדוּ | אַל־תִּמְרֹדוּ | אֶל־תִּמְרֹדוּ | `>L` prep (VP Pred) 'to'; `MRD[` verb qal impf (VP Pred) 'rebel' | **a** | As at Deuteronomy 2:9: written with segol, analysed as the preposition `>L` inside the verb's phrase (`VP`, `Pred`); clause type `WxY0`. |
| 13 | Judges 15:14 | וּפְלִשִׁתִּים | וּפְלִשְׁתִּים | וּפְלִשְׁתִּים | `W` conj (CP Conj) 'and'; `PLCTJ/` adjv (NP Subj) 'Philistine' | **d; c** | The BHSA's text has MAM's vowels, unlike WLC 4.18, 4.20, 4.22 and UXLC 2.6. WLC 4.18's notes Q, n and v say that WLC reads the vowels of L differently from BHS here, so the BHSA, a transcription of BHS, has BHS's form. The analysis, `PLCTJ/` 'Philistine', fits both. |
| 14 | Judges 16:2 | וַהֲרְגְנֻהוּ | וַהֲרַגְנֻהוּ | וַהֲרְגְנֻהוּ | `W` conj (CP Conj) 'and'; `HRG[` verb qal perf suffix `HW` (VP PreO) 'kill' | **c** | A qal perfect, first person plural, with suffix `HW`; the sheva under resh does not change it. |
| 15 | Judges 19:4 | וַיֶּחֱזַק־ | וַיַּחֲזֶק־ | וַיֶּחֱזַק־ | `W` conj (CP Conj) 'and'; `XZQ[` verb qal wayq (VP Pred) 'be strong' | **a** | Stem `qal`, tense `wayq`: the vowels of WLC's form. MAM's form is a hiphil. |
| 16 | Judges 19:23 | אַל־בֵּיתִי | אֶל־בֵּיתִי | אַל־בֵּיתִי | `>L` prep (PP Cmpl) 'to'; `BJT/` subs suffix `J` (PP Cmpl) 'house' | **b** | Written with pataḥ, analysed as the preposition: lexeme `>L`, part of speech `prep`, in a `PP` with function `Cmpl`, whose object is the next atom. The verse's other three atoms with pataḥ are the negative `>L=`. |
| 17 | 1 Samuel 27:10 | הַיַּרְחְמְאֵלִי | הַיְּרַחְמְאֵלִי | הַיַּרְחְמְאֵלִי | `H` art (PP Cmpl) 'the'; `JRXM>LJ/` adjv (PP Cmpl) 'Jerahmeelite' | **c** | The article and the gentilic `JRXM>LJ/`. |
| 18 | 2 Samuel 11:1 | הַמַּלְאכִים | הַמְּלָאכִים | הַמַּלְאכִים | `H` art (NP Subj) 'the'; `MLK/` subs (NP Subj) 'king' | **b** | Lexeme `MLK/` 'king', against the vowels of mem and lamed, which are those of `ML>K/` 'messenger'. The written atom also has a rafeh on its alef, as WLC 4.18 does, marking the alef silent, which fits 'kings' written with an alef, as MAM has it, rather than 'messengers', whose alef has a vowel. So the written atom is mixed, and the analysis takes MAM's word. |
| 19 | 2 Samuel 13:33 | אִם־אַמְנוֹן | אם־אַמְנוֹן | אִם־אַמְנֹון | `>M` conj (CP Conj) 'if'; `>MNWN/` nmpr (PrNP Subj) 'Amnon' | **a** | MAM leaves this atom unpointed, a word written but not read; the BHSA points it, as WLC does, and analyses it as a read word: the conjunction `>M` 'if', in a phrase `CP` of its clause. |
| 20 | 2 Samuel 15:21 | כִּי אִם־ | כִּי אם | כִּי אִם־ | `KJ` conj (CP Conj) 'that'; `>M` conj (CP Conj) 'if' | **a** | As at 2 Samuel 13:33: the conjunction `>M`, read, in a phrase `CP`. The maqaf after it is WLC's too. |
| 21 | 2 Kings 10:33 | וְהָרֻאובֵנִי | וְהָראֿוּבֵנִי | וְהָרֻאובֵנִי | `W` conj (PP Objc) 'and'; `H` art (PP Objc) 'the'; `R>WBNJ/` adjv (PP Objc) 'Reubenite' | **c** | The conjunction, the article and `R>WBNJ/`. |
| 22 | 2 Kings 18:27 (qere) | מימֵי רַגְלֵיהֶם | מֵימֵי רַגְלֵיהֶם | מֵימֵי רַגְלֵיהֶם | `MJM/` subs (PP Objc) 'water'; `RGL/` subs suffix `HM` (PP Objc) 'foot' | **d; c** | The row's forms are of the qere. The BHSA's qere has MAM's tsere under the first mem, with a meteg there, and no accent on its first atom, where WLC and MAM have a merkha on the second mem; WLC 4.18's notes c, n and v say that WLC reads the accents and the vowels of L differently from BHS. The analysis, `MJM/` 'water' and `RGL/` 'foot', fits both. The BHSA's ketiv is two slots, each with its own qere. |
| 23 | Isaiah 23:8 | סֹחֲרֶיה | סֹחֲרֶיהָ | סֹחֲרֶיה | `SXR[` verb qal ptca suffix `H` (NP Subj) 'go about' | **c** | A qal participle, plural, with suffix `H`. The BHSA's atom differs from WLC's in one accent code point only: HEBREW ACCENT QADMA where WLC has the first of two HEBREW ACCENT PASHTA marks. |
| 24 | Isaiah 46:4 | שֵיבָה | שֵׂיבָה | שֵיבָה | `FJBH/` subs (PP Time) 'age' | **c** | `FJBH/` 'age': the analysis takes the letter as sin; WLC's letter, like the BHSA's (`#` in its transliteration), has neither dot. |
| 25 | Isaiah 66:22 | הַחֳדָשִׁים | הַחֲדָשִׁים | הַחֳדָשִׁים | `H` art (NP Subj) 'the'; `XDC=/` subs (NP Subj) 'month' | **a** | Lexeme `XDC=/` 'month', a noun: the vowel of the written ḥataf qamats. MAM's ḥataf pataḥ is the adjective `XDC/` 'new', which the BHSA gives to the same verse's other atom of that root. |
| 26 | Jeremiah 3:17 | וְנִקְוּוּ | וְנִקְווּ | וְנִקְוּוּ | `W` conj (CP Conj) 'and'; `QWH=[` verb nif perf (VP Pred) 'collect' | **c** | A niphal perfect of `QWH=[` 'collect'. |
| 27 | Jeremiah 47:6 | אַל־ | אֶל־ | אַל־ | `>L` prep (PP Cmpl) 'to' | **b** | Written with pataḥ, analysed as the preposition: lexeme `>L`, part of speech `prep`, in a `PP` with function `Cmpl` whose object is the next atom. |
| 28 | Hosea 2:4 | מִפָּנֶיה | מִפָּנֶיהָ | מִפָּנֶיה | `MN` prep (PP Cmpl) 'from'; `PNH/` subs suffix `H` (PP Cmpl) 'face' | **c** | Suffix `H` on `PNH/`, as at Genesis 34:11. |
| 29 | Hosea 2:17 | וִּכְיוֹם | וּכְיוֹם | וִּכְיֹום | `W` conj (PP Adju) 'and'; `K` prep (PP Adju) 'as'; `JWM/` subs (PP Adju) 'day' | **c** | The conjunction, `K`, and `JWM/` 'day'. |
| 30 | Joel 2:12 | וּבְבְכִי | וּבִבְכִי | וּבְבְכִי | `W` conj (PP Adju) 'and'; `B` prep (PP Adju) 'in'; `BKJ/` subs (PP Adju) 'weeping' | **c** | The conjunction, `B` and `BKJ/` 'weeping'. |
| 31 | Jonah 3:2 | וִּקְרָא | וּקְרָא | וִּקְרָא | `W` conj (CP Conj) 'and'; `QR>[` verb qal impv (VP Pred) 'call' | **c** | The conjunction and a qal imperative. |
| 32 | Zechariah 2:2 | וִירוּשָׁלָם | וִירוּשָׁלִָם | וִירוּשָׁלָם | `W` conj (PP Objc) 'and'; `JRWCLM/` nmpr (PP Objc) 'Jerusalem' | **c** | The conjunction and `JRWCLM/`. |
| 33 | Psalms 45:3 | בְּשְׂפְתוֹתֶיךָ | בְּשִׂפְתוֹתֶיךָ | בְּשְׂפְתֹותֶיךָ | `B` prep (PP Cmpl) 'in'; `FPH/` subs suffix `K` (PP Cmpl) 'lip' | **c** | `B` and `FPH/` 'lip', plural, with suffix `K`. |
| 34 | Proverbs 12:9 | מִמְּתַכַּבֵּד | מִמִּתְכַּבֵּד | מִמְּתַכַּבֵּד | `MN` prep (PP Adju) 'from'; `KBD[` verb tif ptca (PP Adju) 'be heavy' | **a** | Stem `tif`, which the ETCBC's documentation of `vs` calls tif‘al, and a participle: the analysis follows the written vowels of the prefix. MAM's form is a hitpael participle. |
| 35 | Proverbs 20:1 | הַיַּין | הַיַּיִן | הַיַּין | `H` art (NP Subj) 'the'; `JJN/` subs (NP Subj) 'wine' | **c** | The article and `JJN/` 'wine'. |
| 36 | Proverbs 31:12 | חַיֶּיה | חַיֶּיהָ | חַיֶּיה | `XJJM/` subs suffix `H` (NP Time) 'life' | **c** | Suffix `H` on `XJJM/`, as at Genesis 34:11. |
| 37 | Job 31:7 | מֻאוּם | מאֿוּם | מֻאוּם | `M>WM/` subs (NP Subj) 'blemish' | **c** | `M>WM/` 'blemish'. |
| 38 | Song of Songs 5:11 | קְוּצּוֹתָיו | קְוֻצּוֹתָיו | קְוּצֹּותָיו | `QWYWT/` subs suffix `W` (NP Subj) 'hairlocks' | **c** | `QWYWT/` 'hairlocks', plural, with suffix `W`. |
| 39 | Daniel 2:45 | וְהַדֶּקֶת | וְהַדֵּקֶת | וְהַדֶּקֶת | `W` conj (CP Conj) 'and'; `DQQ[` verb haf perf (VP Pred) 'crush' | **c** | A haphel perfect, third feminine singular: both vowels under the dalet fit it. |
| 40 | Daniel 5:24 | שְׁלִיַחַ | שְׁלִיחַ | שְׁלִיַחַ | `CLX[` verb peil perf (VP Pred) 'send' | **c** | A peil perfect, third masculine singular. |
| 41 | Daniel 7:20 | וְפֻם | וּפֻם | וְפֻם | `W` conj (CP Conj) 'and'; `PM/` subs (NP Subj) 'mouth' | **c** | The conjunction and `PM/` 'mouth'. |
| 42 | Nehemiah 9:14 | הוֹדַעַתָ | הוֹדַעְתָּ | הֹודַעַתָ | `JD<[` verb hif perf (VP Pred) 'know' | **c** | A hiphil perfect, second masculine singular. |
| 43 | 1 Chronicles 3:1 | דָויִד | דָוִיד | דָויִד | `DWD==/` nmpr (NP PreC) 'David' | **c** | `DWD==/` 'David'. |
| 44 | Deut 3:22 | תְִּירָאוּם | תִּירָאוּם | תִּירָאוּם | `JR>[` verb qal impf suffix `M` (VP PreO) 'fear' | **d; c** | The BHSA's text has MAM's form, with no sheva beside the ḥiriq; WLC 4.18's notes Q, n and v say that WLC reads the vowels of L differently from BHS. The analysis, a qal imperfect with suffix `M`, fits both. |
| 45 | Isa 49:23 | קוָֹי׃ | קֹוָי׃ | קֹוָי | `QWH[` verb qal ptca suffix `J` (NP Subj) 'wait for' | **d; c** | The BHSA's text has the ḥolam on the qof, as MAM does; WLC has it on the vav, with no note. The BHSA's transliteration writes a ḥolam before its vav, so this may be how its transcription renders BHS rather than a different reading. The analysis, a qal participle with suffix `J`, fits both. |
| 46 | Lam 3:25 | לְקוָֹו | לְקֹוָו | לְקֹוָו | `L` prep (PP Cmpl) 'to'; `QWH[` verb qal ptca suffix `W` (PP Cmpl) 'wait for' | **d; c** | The BHSA has a ketiv and qere here, ketiv letters only and a qere with a yod; WLC 4.18's note q says that WLC abandoned a ketiv and qere of BHS. The BHSA's ketiv with the qere's points has the ḥolam on the qof, as MAM's form does. The analysis, a qal participle, plural, with suffix `W`, fits both. |
| 47 | Lam 4:4 | אֶל־חכּוֹ | אֶל־חִכּוֹ | אֶל־חִכֹּו | `>L` prep (PP Cmpl) 'to'; `XK/` subs suffix `W` (PP Cmpl) 'palate' | **d; c** | The BHSA's text has MAM's ḥiriq under the ḥet; WLC 4.18's notes Q, n and v. The analysis, `XK/` 'palate' with suffix `W`, fits both. |
| 48 | Eccl 2:23 | לִבּו | לִבּוֹ | לִבֹּו | `LB/` subs suffix `W` (NP Subj) 'heart' | **d; c** | The BHSA's text has the ḥolam that WLC 4.20, WLC 4.22 and MAM have and WLC 4.18 lacks; WLC 4.18's notes Q, n and v. The analysis, `LB/` 'heart' with suffix `W`, fits both. |
| 49 | Exod 20:3 | עַל־פָּנָיַ | עַל־פָּנַי | עַל־פָּנָיַ | `<L` prep (PP Adju) 'upon'; `PNH/` subs suffix `J` (PP Adju) 'face' | **c** | `PNH/`, plural, with suffix `J`; the BHSA has WLC's qamats and pataḥ. |
| 50 | Deut 5:7 | עַל־פָּנָיַ | עַל־פָּנַי | עַל־פָּנָיַ | `<L` prep (PP PreC) 'upon'; `PNH/` subs suffix `J` (PP PreC) 'face' | **c** | As at Exodus 20:3. |
| 51 | Exod 20:4 | מִתַָּחַת | מִתַּחַת | מִתַָּחַת | `MN` prep (PP PreC) 'from'; `TXT/` subs (PP PreC) 'under part' | **c** | `MN` and `TXT/`; the BHSA has WLC's qamats and pataḥ under the tav. |
| 52 | Exod 20:9 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | כָּל־מְלַאכְתֶּךָ | `KL/` subs (NP Objc) 'whole'; `ML>KT/` subs suffix `K` (NP Objc) 'work' | **c** | `KL/`, construct, and `ML>KT/` with suffix `K`; the dagesh does not change it. |
| 53 | Exod 20:10 | לֹא־תַעֲשֶׂה | לֹא תַעֲשֶׂה | לֹא־תַעֲשֶׂה | `L>` nega (NegP Nega) 'not'; `<FH[` verb qal impf (VP Pred) 'make' | **c** | The negative `L>` and a qal imperfect; the BHSA has WLC's maqaf, which the analysis does not depend on. |
| 54 | Deut 5:8 | לֹא־תַעֲשֶׂה־לְךָ | לֹא תַעֲשֶׂה־לְךָ | לֹא־תַעֲשֶׂה־לְךָ | `L>` nega (NegP Nega) 'not'; `<FH[` verb qal impf (VP Pred) 'make'; `L` prep suffix `K` (PP Cmpl) 'to' | **c** | As at Exodus 20:10, with `L` and suffix `K`. |
| 55 | Deut 5:8 | מִתָּחַת | מִתַּחַת | מִתָּחַת | `MN` prep (PP PreC) 'from'; `TXT/` subs (PP PreC) 'under part' | **c** | `MN` and `TXT/`; the BHSA has WLC's qamats. |
| 56 | Deut 5:13 | כָּל־מְלַאכְתֶּךָ | כׇל־מְלַאכְתֶּךָ | כָּל־מְלַאכְתֶּךָ | `KL/` subs (NP Objc) 'whole'; `ML>KT/` subs suffix `K` (NP Objc) 'work' | **c** | As at Exodus 20:9; the BHSA has WLC 4.18's rafeh too. |

### The footnote's six verses

| Verse | WLC 4.18 | MAM | BHSA | BHSA's analysis, word by word | Class |
|---|---|---|---|---|---|
| Ezekiel 44:13 | הַקְּדָשִׁים | הַקֳּדָשִׁים | הַקְּדָשִׁים | `H` art (PP Cmpl) 'the'; `QDC/` subs (PP Cmpl) 'holiness' | **c** |
| Ezra 4:9 (qere) | אַרְכְּוָיֵא | אַרְכֳּוָיֵא | אַרְכְּוָיֵא | `>RKWJ/` adjv (PrNP Subj) 'Erechite' | **c** |
| 2 Chronicles 5:7 | הַקְּדָשִׁים | הַקֳּדָשִׁים | הַקְּדָשִׁים | `H` art (PP Cmpl) 'the'; `QDC/` subs (PP Cmpl) 'holiness' | **c** |
| Numbers 35:20 | יֶהְדָּפֶנּוּ | יֶהְדֳּפֶנּוּ | יֶהְדָּפֶנּוּ | `HDP[` verb qal impf suffix `HW` (VP PreO) 'push' | **c** |
| 1 Samuel 26:10 | יִגָּפֶנּוּ | יִגֳּפֶנּוּ | יִגָּפֶנּוּ | `NGP[` verb qal impf suffix `HW` (VP PreO) 'hurt' | **c** |
| 2 Samuel 6:5 | וּבְצֶלְצֶלִים | וּבְצֶלְצֱלִים | וּבְצֶלְצֶלִים | `W` conj (PP Adju) 'and'; `B` prep (PP Adju) 'in'; `YLYLJM/` subs (PP Adju) 'cymbals' | **c** |

At all six verses the BHSA's atom is WLC 4.18's, with no ḥataf, and its analysis fits both: `QDC/` 'holiness' (Ezekiel 44:13, 2 Chronicles 5:7), `>RKWJ/` (Ezra 4:9, a qere in the BHSA), qal imperfects with suffix `HW` (Numbers 35:20, 1 Samuel 26:10) and `YLYLJM/` 'cymbals' (2 Samuel 6:5).

## Part 2: corrections across the BHSA

Two tests were run over the whole BHSA 2021, at the level of its words (slots) and again at
the level of atoms, and every word they flagged was read. Claude read Test A's first 255 groups
and Test B's two small classes; five sub-agents of this session read the rest (the table under
"Who read what"). Every sub-agent finding adopted here was checked against the data
(`out/37-verify-p2a.txt` to `out/42-verify-p2c.txt`).

### The answer

Beyond Part 1's four corrections (Exodus 10:28, Judges 19:23, Jeremiah 47:6, 2 Samuel 11:1),
the BHSA's analysis departs from its own written atom at 11 more places, and perhaps a 12th.
Three of them take MAM's word where MAM's atom differs. At the other eight, MAM's atom is the
BHSA's.

1. **Where MAM's atom differs, and the analysis takes MAM's word:**
   - **Deuteronomy 25:7.** The BHSA's atom has a yod, as WLC 4.18, WLC 4.20 and UXLC 2.6
     have, which MAM's atom lacks. The BHSA analyses it as `M>N[` piel perfect 'refuse', MAM's
     word (`out/39-verify-deut-25-7.txt`).
   - **Leviticus 4:35.** The BHSA's atom has no mappiq in its final he, as the place name
     `XLBH/` (Judges 1:31) has none, and is analysed as `XLB=/` 'fat' with the suffix `H`, as
     MAM's atom with its mappiq spells. At Leviticus 5:12, with the same missing mappiq, the
     BHSA gives no suffix (`out/38-verify-p2d.txt`).
   - **Genesis 39:19, the reverse.** The BHSA's atom has a mappiq, as WLC 4.18 and 4.20 have,
     which spells a suffix; its analysis, a qal perfect, has none. MAM's and UXLC 2.6's atom
     has no mappiq (`out/40-verify-p2b.txt`, `out/41-verify-p2b-texts.txt`).
2. **Where MAM's atom is the BHSA's, and the analysis still departs from it.** A comparison
   with MAM cannot see these:
   - **2 Chronicles 28:19.** The atom is pointed as the noun `M<L=/` 'unfaithfulness', as 13
     other words with this pointing are, and analysed as `M<L[` qal perfect after its
     infinitive absolute. The BHSA's 5 other qal perfects, third masculine singular, of that
     verb have qamats under the mem (`out/37-verify-p2a.txt`).
   - **1 Samuel 30:26, Job 42:10 and 1 Kings 16:11.** An atom spelled and pointed as 'his
     fellow', singular, is analysed as plural.
   - **Numbers 11:15, Deuteronomy 5:27 and Ezekiel 28:14.** An atom pointed as the feminine
     'you', which the BHSA analyses as the feminine `>T=` at 44 other words with these two
     pointings, with and without the conjunction, is analysed as the masculine pronoun `>TH`.
   - **1 Samuel 27:10.** An atom pointed as the negative, as 723 other words are, is analysed
     as `>L==` 'where', a lexeme the BHSA has nowhere else.
3. **Unsure: Judges 9:2.** The BHSA's tsere before the suffix looks like a plural written
   without its yod, but the analysis is singular, as MAM's sheva spells it.

**Flagged but not corrections:**
- readings of a defective spelling: 2 Samuel 6:1, `>SP[` 'gather' written without its alef;
  Micah 1:15, 'I will bring' without its final alef; Micah 7:17, 'they will fear' with one
  yod;
- homographs that context decides: Job 24:25, the negative used as a noun, and many names and
  numbered homonyms;
- artifacts of the method.

**Analyses that follow the BHSA's own pointing against MAM's**, beyond Part 1's class a:
2 Chronicles 1:5 (a sin dot, 'put', where MAM's shin dot makes 'there'), Jeremiah 11:2 (a
singular 'you' with a suffix, where MAM has a plural 'you'), 2 Chronicles 21:4 (a lexeme of
the ETCBC's own split), 2 Chronicles 15:16 (a preposition with pataḥ and no article, where
MAM's qamats is the article's) and Leviticus 5:12.

**The ETCBC's documentation marks no such correction and states no policy on them.** Of its
pages read (the site's home page, `features/0_home`, the features `vs`, `vt`, `qere`, `g_word`,
`lex` and `typ`, and the pages `wordgrammar`, `colofon`, `news` and `cantillation`), only the
ketiv and qere features document a reading other than the written one. Its `vs` page names the
stem `tif` "tif‘al".

### The method

`scripts/part2_scan.py`, run from the MAM-basics root, reads every BHSA word (slot) with a
written form and no qere; a ketiv's slots, whose `g_word_utf8` is unpointed, are left out. A
word's **pointed key** is its language and the review's key of its `g_word_utf8`; its
**analysis** is its language, `lex`, `vs` and `vt`. An analysis is **supported** by a pointed
key when the key's words have it at least 3 times, or at least a tenth as often as the key's
commonest analysis.

1. **Test A, independent of MAM:** a word whose analysis its own pointed key does not support,
   where the key has some analysis at least 5 times.
2. **Test B, against MAM:** MAM-simple's verse (BHS versification, ketiv side, the combined
   strand of a dual cantillation, read by the review's lint) is aligned with the BHSA's atoms
   by letters. Where an atom has the same letters in both and different pointing (`bkey`), MAM's
   atom is cut into the BHSA's slots by letter count, and each slot whose key differs is
   classed by whether its analysis is supported by its own key (its other words) and by MAM's
   key (the BHSA's words with MAM's pointing).

Test B's counts (`out/33-part2-scan-run.txt`): 304,789 atoms; 1,315 with a ketiv and 1,530
whose letters differ from MAM's atom, both skipped; 7,517 atoms whose pointing differs from
MAM's. Of their slots whose keys differ:

| Class | Slots | What it means | File |
|---|---|---|---|
| mam-elsewhere | 8 | supported by MAM's key only, while its own key's other words are analysed otherwise: a correction toward MAM | `out/35-part2-test-b-mam-elsewhere.txt` |
| mam-unique | 184 | supported by MAM's key, its own pointing found nowhere else | `out/35-part2-test-b-mam-unique.txt` |
| written | 104 | supported by its own key only | `out/35-part2-test-b-written.txt` |
| neither | 169 | supported by neither key | `out/35-part2-test-b-neither.txt` |
| both | 7,059 | supported by both: pointing that does not decide the analysis | `out/32-part2-scan.json` |

**What the small classes hold.** Of mam-elsewhere's 8: the three al/el corrections, Leviticus
4:35, and four artifacts of the BHSA's cutting a conjunction or an article into a slot of its
own (Genesis 15:10, an article's dagesh; Exodus 2:10, 2 Samuel 3:32 and Job 8:1, a
wayyiqtol's prefix without its dagesh, whose tense the conjunction's pataḥ decides). Of
written's 104 slots in 46 groups: 55 slots in 20 groups are a ḥataf under a non-guttural in the
BHSA where MAM has a sheva, MAM's form occurring nowhere in the BHSA; 21 are two names that the
BHSA writes with a maqaf inside one word where MAM writes one atom (Rabshakeh, Malchishua);
others differ in a dagesh or one vowel; and the rest are the review's class a cases (Deuteronomy 2:9,
Joshua 22:19, Judges 19:4, Isaiah 66:22, 2 Samuel 13:33 and 15:21), atoms that MAM's ketiv side
leaves unpointed (2 Samuel 8:3; Daniel 5:10 and 7:19), and 2 Chronicles 1:5, where the BHSA's
atom has a sin dot and is analysed as `FJM[` 'put' while MAM's has a shin dot, the pointing of
'there'.

### The atom-level rerun

`scripts/p2d_scan_atoms.py` reruns both tests with the BHSA's atom as the unit. An atom's
pointed key is its languages and the review's key of its whole text; its analysis is the tuple,
over its slots, of lexeme, stem, tense, person, number, gender and suffix. Its counts
(`out/p2d-scan-run.txt`):

- Test A: 255 atoms in 222 groups.
- Test B: mam-elsewhere 4, mam-unique 205, written 148, both 6,909 and neither 249.

Its mam-elsewhere atoms are the three al/el corrections and Leviticus 4:35: the slot level's
four artifacts are gone. It found the number and gender departures above, and Deuteronomy 25:7.

### Who read what

| Slice | Read by | Rows | Outcome | File |
|---|---|---|---|---|
| Test A, groups 1 to 255 | Claude | 255 groups | homographs, names, numbered homonyms and artifacts; the al/el corrections; the candidates of item 2 | `out/30-part2-test-a.txt` |
| Test A, groups 256 to 305, and six candidates | sub-agent p2a | 50 groups | 2 Chronicles 28:19 a correction; 29 names, 4 numbered homonyms, 10 homographs, 6 artifacts; of the candidates, 1 Samuel 27:10 a correction | `out/p2a-test-a-review.md` |
| Test B, mam-elsewhere and written | Claude | 8 and 104 slots | as above | `out/35-part2-test-b-*.txt` |
| Test B, mam-unique | sub-agent p2b | 184 slots | another word 0, no word 98, variant 84, unsure 2 (Genesis 39:19, adopted above as a correction of the suffix; Jeremiah 11:2, which follows its pointing) | `out/p2b-mam-unique.md` |
| Test B, neither | sub-agent p2c | 169 slots | another word 1 (2 Samuel 11:1), follows its pointing 2 (Proverbs 12:9, 2 Chronicles 21:4), no word 42, variant 123, unsure 1 (Judges 9:2) | `out/p2c-neither.md` |
| The atom-level rerun, its mam-elsewhere class and its person, number, gender and suffix groups | sub-agent p2d | 4 atoms, 21 groups | the number and gender corrections, Deuteronomy 25:7 | `out/p2d-review.md` |
| The atom-level rerun's other new rows: Test A's new groups, and Test B's mam-unique and neither atoms with no slot judged before | sub-agent p2e | 156 rows: 54 groups (69 atoms) and 102 atoms | another word 3, all p2d's (the feminine 'you', Deuteronomy 25:7); follows its pointing 2 (Isaiah 66:22, 2 Chronicles 15:16); no word 44, variant 55, homograph 52 | `out/p2e-review.md` |

"No word" means a pointing that is no well-formed word, which the analysis reads through, as
at Part 1's Genesis 34:11. "Variant" means a legitimate variant of the same word.

### What the tests cannot find

1. A correction where MAM's pointing is the BHSA's: Test B never sees it, and Test A sees it
   only when the same pointing is common elsewhere with another analysis (by Test A's rule,
   369,196 of 418,274 slots and 235,366 of 303,474 atoms).
2. A word whose pointing occurs nowhere else: neither test has anything to compare its
   analysis with, so mam-unique and neither needed a reader.
3. A correction in what the tests leave out of the analysis: state, and the phrase's type and
   function (Deuteronomy 2:9's preposition inside a verb's phrase is such a case). Person,
   number, gender and suffix are compared only at the atom level.
4. Test B skips anything in a ketiv's slots and any atom whose letters differ from MAM's.
   Deuteronomy 25:7 was found by the atom-level Test A instead: its atom's key is elsewhere,
   26 times, the preposition `MN` with `>JN/` 'there is not' (`out/p2d-test-a.txt`, A43).
5. At the slot level, a conjunction's or an article's vowel is judged apart from the dagesh
   that goes with it, which made the artifacts above; the atom level removes them but has
   fewer words to compare with.

## Data, rights and files

- **The BHSA**: ETCBC/bhsa at `4db00e2157915495e1a4d3d57e41223df24775da` (master on
  2026-11-13, committed 2026-01-18), version 2021, read through the GitHub API only, one
  request at a time, nothing cloned. Twelve feature files were copied from the MACULA session's
  folder (`out/00-copy-from-macula.txt`), and 32 more fetched (`out/01-fetch-features.txt`,
  `out/fetch_log.jsonl`); every file's size and Git blob SHA-1 equal the `tf/2021` listing's.
  Their headers and value sets are in `out/02-census.txt`. The data's README puts it under
  CC BY-NC 4.0 (GitHub's licence field says MIT); it stays in this untracked folder.
- **The ETCBC's documentation**, eleven pages of https://etcbc.github.io/bhsa/, fetched through
  MAM-basics' `mb_cmn.polite_download` (robots.txt obeyed, 3 to 5 seconds apart) into
  `fetched/etcbc-docs-*`, their text in `out/docs/`.
- **Comparison texts**, all local: WLC 4.18 (above); WLC 4.20 and 4.22 as MAM-basics'
  `out/wlc420-u` and `out/wlc422-u`; UXLC 2.6 (`in/UXLC-39`, 19 Oct 2026); MAM-simple.
- **Scripts**, in `scripts/`, each with its usage in its docstring; Python scripts that read
  fetched files ran as `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -I`, from
  the MAM-basics root. `make_readme.py` writes this README from `scripts/README.template.md`.
- **Outputs**, in `out/`: `10-part1-cases.json` and `.txt` (every case, both sides, every
  slot's features), `11-part1-compact.txt`, `12-part1-hataf-ng.*`, `13-lexinfo-part1.txt`
  (lexemes `XDC/`, `XDC=/`, `MLK/`, `ML>K/` and `KBD[`, and five verses word by word),
  `14-part1-table.md`, `15-part1-hataf-table.md`, `20-docs-hits.txt`; for Part 2,
  `30-part2-test-a.txt`, `32-part2-scan.json`, `33-part2-scan-run.txt` and
  `35-part2-test-b-*.txt` (`scripts/part2_group.py`); Claude's checks of the sub-agents'
  findings, `36-lexinfo-part2.txt` to `42-verify-p2c.txt` (`scripts/verify_slots.py`,
  `scripts/show_texts.py`, `scripts/lexinfo.py`); and each sub-agent's outputs, `out/p2a-*` to
  `out/p2e-*`, from its scripts `scripts/p2a_*` to `scripts/p2e_*`.
- **The sub-agents' rule slips**, as they reported them: p2b viewed files with `sed -n` and
  a one-line `python -c` in Git Bash, and p2c ran one `python -c` inspection; both were
  read-only and wrote nothing.
