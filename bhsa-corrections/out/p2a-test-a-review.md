# Test A's last 50 groups and six candidates (sub-agent p2a)

Written by Claude (Opus 5.5) as sub-agent p2a on 2026-11-13, New York time, for the session that
wrote this folder's README.md, and not reviewed by a human. Nothing tracked changed. This page is
rendered by `scripts/p2a_render.py` from `out/p2a-review-template.md`, which holds no Hebrew:
every form here is quoted from the data by script, in MAM-normal mark order. A form is the
BHSA 2021's (`g_word_utf8`), WLC 4.18's (Sefaria-Data's copy of tanach.us's build 24.2) or MAM's
(MAM-simple, BHS versification, ketiv side), and each is named. The BHSA writes a ḥolam male as
a ḥolam on the letter before the vav (the README's Part 1), and its forms are shown so. No image
of the Leningrad Codex was consulted, and nothing here says what the codex has.

## The answer

1. **One new candidate in the last 50 groups: 2 Chronicles 28:19.**
   The BHSA's atom מַעַל has the pointing of the noun `M<L=/` 'unfaithfulness', as the
   BHSA's 13 other words of that pointed key do, and is analysed as the qal perfect of `M<L[`
   'be unfaithful', whose five other third masculine singular perfects in the BHSA are all
   spelled מָעַל, with qamats under the mem. WLC 4.18 and MAM have the BHSA's atom.
2. **The other 49 groups are not corrections:** 29 proper names spelled like a common word or
   another name, 4 pairs of the ETCBC's numbered homonym lexemes, 10 other homographs (among
   them Daniel 12:13's -in plural and 2 Chronicles 26:15's pausal perfect), and 6 artifacts of
   the slot cutting (a relative particle's dagesh, or a wayyiqtol's conjunction with qamats
   before alef, in a slot of its own).
3. **The six candidates:**
   1. 1 Samuel 27:10, `>L==` 'where': **correction**, by reinterpretation rather than
      re-pointing: the atom has the negative's pointing, and the analysed word occurs nowhere
      else in the BHSA.
   2. Job 24:25, `>L=/` 'nothingness': **homograph**: the negative itself used as a noun, which
      the ETCBC files under a lexeme of its own.
   3. 2 Samuel 6:1, `>SP[` qal wayyiqtol: **defective-or-ambiguous**: the vowels of a wayyiqtol
      of `>SP[` written without its quiescent alef, identical with `JSP[`'s hiphil wayyiqtol.
   4. Micah 1:15, `BW>[` hiphil imperfect: **defective-or-ambiguous**: the vowels of 'I will
      bring' written without its final quiescent alef, identical with 'my father'.
   5. Micah 7:17, `JR>[` 'fear': **defective-or-ambiguous**: 'they will fear' with one yod for
      two, identical with 'they will see', a pointing that the BHSA reads as 'fear' at 10 other
      words.
   6. Isaiah 52:2, `JCB[` qal imperative: **artifact**: the test's key keeps a dagesh that
      groups the imperative with 'the captivity' after the article.
4. **At each candidate's place, the BHSA's atom has WLC 4.18's and MAM's letters and marks,
   accents included** (`bc_common.bfkey`, which ignores the order of a letter's marks: at Job
   24:25 the BHSA's text has the code point HEBREW ACCENT GERESH MUQDAM before the lamed's
   sheva, where WLC 4.18's and MAM's have it after; and the BHSA's atoms here lack the sof
   pasuq, which the BHSA keeps in its trailer), so none of the seven is a correction toward
   MAM, and Test B could see none of them.
5. **The slice is 50 groups, not 51:** lines 259 to 308 of `out/30-part2-test-a.txt` hold its
   last 50 groups (groups 256 to 305 of 305); the file ends after line 308, so the line 309
   that a reader shows is empty.

## The six candidates

Each candidate gives the BHSA's analysis, its pointed key's other words (lexeme, count and one
reference), the atom in MAM and WLC 4.18, a one-sentence reason, and the verse atom by atom.

### 1. 1 Samuel 27:10: correction

- **The BHSA's analysis:** slot 158430, the atom אַל־, lexeme `>L==` (אַל),
  part of speech `inrg` (interrogative), gloss 'where', in its own phrase `InrP` with function
  `Ques`, in a clause of type `xQt0` whose predicate is פְּשַׁטְתֶּם, `PCV[` qal perfect, second
  masculine plural.
- **The pointing elsewhere:** the BHSA's other words with the key אַל are the negative
  `>L=` 723 times (Genesis 13:8 first), the preposition `>L` twice (Judges 19:23 and Jeremiah
  47:6, Part 1's corrections) and `>L=/` once (Job 24:25). `>L==` occurs only here.
- **MAM's atom:** אַל־. **WLC 4.18's:** אַל־.
- **Reason:** The pointing is the negative's, as at 723 other words, and the analysis takes it
  as an interrogative 'where' that the BHSA has nowhere else, so, unlike Exodus 10:28's
  correction, which names a word the BHSA spells otherwise elsewhere, this one shows only as a
  lexeme of its own.

1 Samuel 27:10, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `W` conj 'and' (CP Conj); `>MR[` qal wayq p3 sg m 'say' (VP Pred) | וַיֹּ֣אמֶר | וַיֹּ֣אמֶר |
| 2 | `>KJC/` nmpr sg 'Achish' (PrNP Subj) | אָכִ֔ישׁ | אָכִ֔ישׁ |
| **3** | `>L==` inrg 'where' (InrP Ques) | אַל־ | אַל־ |
| 4 | `PCV[` qal perf p2 pl m 'strip off' (VP Pred) | פְּשַׁטְתֶּ֖ם | פְּשַׁטְתֶּ֖ם |
| 5 | `H` art 'the' (NP Time); `JWM/` subs sg 'day' (NP Time) | הַיֹּ֑ום | הַיּ֑וֹם |
| 6 | `W` conj 'and' (CP Conj); `>MR[` qal wayq p3 sg m 'say' (VP Pred) | וַיֹּ֣אמֶר | וַיֹּ֣אמֶר |
| 7 | `DWD==/` nmpr sg 'David' (PrNP Subj) | דָּוִ֗ד | דָּוִ֗ד |
| 8 | `<L` prep 'upon' (PP Cmpl) | עַל־ | עַל־ |
| 9 | `NGB/` subs sg 'south' (PP Cmpl) | נֶ֤גֶב | נֶ֤גֶב |
| 10 | `JHWDH/` nmpr sg 'Judah' (PP Cmpl) | יְהוּדָה֙ | יְהוּדָה֙ |
| 11 | `W` conj 'and' (PP Cmpl); `<L` prep 'upon' (PP Cmpl) | וְעַל־ | וְעַל־ |
| 12 | `NGB/` subs sg 'south' (PP Cmpl) | נֶ֣גֶב | נֶ֣גֶב |
| 13 | `H` art 'the' (PP Cmpl); `JRXM>LJ/` adjv sg 'Jerahmeelite' (PP Cmpl) | הַיַּרְחְמְאֵלִ֔י | הַיְּרַחְמְאֵלִ֔י |
| 14 | `W` conj 'and' (PP Cmpl); `>L` prep 'to' (PP Cmpl) | וְאֶל־ | וְאֶל־ |
| 15 | `NGB/` subs sg 'south' (PP Cmpl) | נֶ֖גֶב | נֶ֖גֶב |
| 16 | `H` art 'the' (PP Cmpl); `QJNJ/` adjv sg 'Kenite' (PP Cmpl) | הַקֵּינִֽי | הַקֵּינִֽי׃ |

### 2. Job 24:25: homograph

- **The BHSA's analysis:** slot 342192, in the atom לְאַל after the preposition `L`,
  lexeme `>L=/` (אַל), a noun (`subs`), singular, absolute, gloss 'nothingness', in a
  `PP` with function `Cmpl` of יָשֵׂם, `FJM[` 'put' qal imperfect, whose object
  is מִלָּתִי 'my word'.
- **The pointing elsewhere:** the key is 1 Samuel 27:10's, אַל: the negative `>L=` 723
  times (Genesis 13:8 first). `>L=/` occurs only here.
- **MAM's atom:** לְ֝אַ֗ל. **WLC 4.18's:** לְ֝אַ֗ל.
- **Reason:** 'Nothing' is the negative itself, used as a noun after a preposition, which the
  ETCBC files under a lexeme of its own, so the analysis reads the word the pointing spells and
  differs from the 723 only in its part of speech.

Job 24:25, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `W` conj 'and' (CP Conj); `>M` conj 'if' (CP Conj) | וְאִם־ | וְאִם־ |
| 2 | `L>` nega 'not' (NegP Nega) | לֹ֣א | לֹ֣א |
| 3 | `>PW` intj 'then' (InjP Intj) | אֵ֭פֹו | אֵ֭פוֹ |
| 4 | `MJ` prin 'who' (IPrP Subj) | מִ֣י | מִ֣י |
| 5 | `KZB[` hif impf p3 sg m suffix `NJ` 'lie' (VP PreO) | יַכְזִיבֵ֑נִי | יַכְזִיבֵ֑נִי |
| 6 | `W` conj 'and' (CP Conj); `FJM[` qal impf p3 sg m 'put' (VP Pred) | וְיָשֵׂ֥ם | וְיָשֵׂ֥ם |
| **7** | `L` prep 'to' (PP Cmpl); `>L=/` subs sg 'nothingness' (PP Cmpl) | לְ֝אַ֗ל | לְ֝אַ֗ל |
| 8 | `MLH/` subs sg suffix `J` 'word' (NP Objc) | מִלָּתִֽי | מִלָּתִֽי׃ |

### 3. 2 Samuel 6:1: defective-or-ambiguous

- **The BHSA's analysis:** slot 163423, the atom וַיֹּסֶף, `>SP[` 'gather', qal
  wayyiqtol, third masculine singular, the predicate of a clause whose object (`PP Objc`) is
  atoms 4 to 9 below, 'all the chosen men in Israel, thirty thousand', with עֹוד
  'again' as a modifier (`AdvP Modi`).
- **The pointing elsewhere:** the BHSA's other 21 words with the key יֹּסֶף are `JSP[`
  'add', hiphil wayyiqtol (Genesis 8:10 first). All 23 of its other qal wayyiqtol third
  masculine singular words of `>SP[` have the alef: יֶּאֱסֹף 19 times (Genesis 29:22 first),
  then יֶּאֶסֹף once (Joshua 24:1), and three with suffixes. Its only other word of `>SP[`
  without an alef is תֹּסֵף at Psalms 104:29, a qal imperfect, second masculine singular.
  Conversely, it analyses 1 Samuel 18:29's וַיֹּאסֶף, written with an alef, as `JSP[`
  hiphil wayyiqtol.
- **MAM's atom:** וַיֹּ֨סֶף. **WLC 4.18's:** וַיֹּ֨סֶף.
- **Reason:** The vowels, ḥolam on the prefix and segol under the samekh, are those of 1 Samuel
  18:29's וַיֹּאסֶף with its alef unwritten, so the pointing permits `>SP[` without the root's
  quiescent alef, as the BHSA also reads Psalms 104:29, while being the normal spelling of
  `JSP[`; the BHSA lets the sense decide here and at 1 Samuel 18:29 alike.

2 Samuel 6:1, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| **1** | `W` conj 'and' (CP Conj); `>SP[` qal wayq p3 sg m 'gather' (VP Pred) | וַיֹּ֨סֶף | וַיֹּ֨סֶף |
| 2 | `<WD/` subs sg 'duration' (AdvP Modi) | עֹ֥וד | ע֥וֹד |
| 3 | `DWD==/` nmpr sg 'David' (PrNP Subj) | דָּוִ֛ד | דָּוִ֛ד |
| 4 | `>T` prep '<object marker>' (PP Objc) | אֶת־ | אֶת־ |
| 5 | `KL/` subs sg 'whole' (PP Objc) | כָּל־ | כׇּל־ |
| 6 | `BXWR/` subs sg 'young man' (PP Objc) | בָּח֥וּר | בָּח֥וּר |
| 7 | `B` prep 'in' (PP Objc); `JFR>L/` nmpr sg 'Israel' (PP Objc) | בְּיִשְׂרָאֵ֖ל | בְּיִשְׂרָאֵ֖ל |
| 8 | `CLC/` subs pl 'three' (PP Objc) | שְׁלֹשִׁ֥ים | שְׁלֹשִׁ֥ים |
| 9 | `>LP=/` subs sg 'thousand' (PP Objc) | אָֽלֶף | אָֽלֶף׃ |

### 4. Micah 1:15: defective-or-ambiguous

- **The BHSA's analysis:** slot 299793, the atom אָבִי, `BW>[` 'come', hiphil
  imperfect, first person singular ('I will bring'), the predicate of a clause of type `xYq0`
  whose object (`NP Objc`) is הַיֹּרֵשׁ 'the dispossessor', with עֹד 'again'
  (`AdvP Modi`) and לָךְ 'to you' (`PP Cmpl`).
- **The pointing elsewhere:** the BHSA's other 134 words with the key אָבִי are `>B/`
  'father' with the suffix `J`, 'my father' (Genesis 19:34 first). Its 16 other hiphil
  imperfects of `BW>[`, first person singular, without a suffix, are אָבִיא, with the alef
  (Exodus 11:1 first). Its only other word of `BW>[` without an alef is בָּנוּ at 1 Samuel
  25:8, a qal perfect, first person plural (Test A's line 98).
- **MAM's atom:** אָ֣בִי. **WLC 4.18's:** אָ֣בִי.
- **Reason:** The vowels are those of אָבִיא, and only the root's final quiescent alef is
  unwritten, as at 1 Samuel 25:8, so the pointing permits 'I will bring', the reading that gives
  the clause and its object a verb.

Micah 1:15, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `<WD/` subs sg 'duration' (AdvP Modi) | עֹ֗ד | עֹ֗ד |
| 2 | `H` art 'the' (NP Objc); `JRC[` qal ptca sg m 'trample down' (NP Objc) | הַיֹּרֵשׁ֙ | הַיֹּרֵשׁ֙ |
| **3** | `BW>[` hif impf p1 sg 'come' (VP Pred) | אָ֣בִי | אָ֣בִי |
| 4 | `L` prep suffix `K=` 'to' (PP Cmpl) | לָ֔ךְ | לָ֔ךְ |
| 5 | `JCB[` qal ptca sg f 'sit' (NP Voct) | יֹושֶׁ֖בֶת | יוֹשֶׁ֖בֶת |
| 6 | `MRCH=/` nmpr sg 'Mareshah' (NP Voct) | מָֽרֵשָׁ֑ה | מָֽרֵשָׁ֑ה |
| 7 | `<D` prep 'unto' (PP Cmpl) | עַד־ | עַד־ |
| 8 | `<DLM/` nmpr sg 'Adullam' (PP Cmpl) | עֲדֻלָּ֥ם | עֲדֻלָּ֥ם |
| 9 | `BW>[` qal impf p3 sg m 'come' (VP Pred) | יָבֹ֖וא | יָב֖וֹא |
| 10 | `KBWD/` subs sg 'weight' (NP Subj) | כְּבֹ֥וד | כְּב֥וֹד |
| 11 | `JFR>L/` nmpr sg 'Israel' (NP Subj) | יִשְׂרָאֵֽל | יִשְׂרָאֵֽל׃ |

### 5. Micah 7:17: defective-or-ambiguous

- **The BHSA's analysis:** slot 301390, the atom וְיִרְאוּ, `JR>[` 'fear', qal imperfect,
  third masculine plural, the predicate of a clause of type `WYq0` with מִמֶּךָּ 'of you'
  (`PP Cmpl`), after יִפְחָדוּ, `PXD[` 'tremble', qal imperfect, third masculine plural.
- **The pointing elsewhere:** the BHSA's other 28 words with the key יִרְאוּ are `R>H[`
  'see', qal imperfect (Genesis 12:12 first). Its qal imperfects of `JR>[`, third masculine
  plural, without a suffix, are יִירְאוּ, with two yods and sheva under the resh, 8 times
  (Deuteronomy 2:4 first); יִרָאוּ, with one yod and qamats under the resh, 4 times
  (Deuteronomy 17:13 first), and once more with a final nun; and יִירָאוּ, with two yods and
  qamats, 4 times (Isaiah 41:5 first). It reads the one-yod pointing with sheva as 'fear' at 9
  wayyiqtol words, יִּרְאוּ (Joshua 4:14 first), and at Ecclesiastes 3:14 (Test A's line
  261).
- **MAM's atom:** וְיִֽרְא֖וּ. **WLC 4.18's:** וְיִֽרְא֖וּ.
- **Reason:** The pointing is a defective spelling of 'they will fear', one yod for the two of
  the BHSA's eight such imperfects with sheva, and the BHSA reads the same one-yod pointing as
  'fear' at 10 other words; 'of you' and the parallel 'tremble' decide against 'see'.

Micah 7:17, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `LXK[` piel impf p3 pl m 'eat' (VP Pred) | יְלַחֲכ֤וּ | יְלַחֲכ֤וּ |
| 2 | `<PR/` subs sg 'dust' (NP Objc) | עָפָר֙ | עָפָר֙ |
| 3 | `K` prep 'as' (PP Adju); `H` art 'the' (PP Adju); `NXC/` subs sg 'serpent' (PP Adju) | כַּנָּחָ֔שׁ | כַּנָּחָ֔שׁ |
| 4 | `K` prep 'as' (PP Adju); `ZXL[` qal ptca pl m 'glide away' (PP Adju) | כְּזֹחֲלֵ֣י | כְּזֹחֲלֵ֣י |
| 5 | `>RY/` subs sg 'earth' (PP Adju) | אֶ֔רֶץ | אֶ֔רֶץ |
| 6 | `RGZ[` qal impf p3 pl m 'quake' (VP Pred) | יִרְגְּז֖וּ | יִרְגְּז֖וּ |
| 7 | `MN` prep 'from' (PP Cmpl); `MSGRT/` subs pl suffix `HM` 'bulwark' (PP Cmpl) | מִמִּסְגְּרֹֽתֵיהֶ֑ם | מִמִּסְגְּרֹֽתֵיהֶ֑ם |
| 8 | `>L` prep 'to' (PP Cmpl) | אֶל־ | אֶל־ |
| 9 | `JHWH/` nmpr sg 'YHWH' (PP Cmpl) | יְהוָ֤ה | יְהֹוָ֤ה |
| 10 | `>LHJM/` subs pl suffix `NW` 'god(s)' (PP Cmpl) | אֱלֹהֵ֨ינוּ֙ | אֱלֹהֵ֙ינוּ֙ |
| 11 | `PXD[` qal impf p3 pl m 'tremble' (VP Pred) | יִפְחָ֔דוּ | יִפְחָ֔דוּ |
| **12** | `W` conj 'and' (CP Conj); `JR>[` qal impf p3 pl m 'fear' (VP Pred) | וְיִֽרְא֖וּ | וְיִֽרְא֖וּ |
| 13 | `MN` prep suffix `K` 'from' (PP Cmpl) | מִמֶּֽךָּ | מִמֶּֽךָּ׃ |

### 6. Isaiah 52:2: artifact

- **The BHSA's analysis:** slot 230330, the atom שְּׁבִ֖י, `JCB[` 'sit', qal imperative,
  second feminine singular, the predicate of a clause of type `ZIm0`, after ק֥וּמִי,
  `QWM[` 'arise', qal imperative, second feminine singular; Jerusalem is the vocative.
- **The pointing elsewhere:** the BHSA's other 22 words with the key שְּׁבִי, with a dagesh
  in the shin, are `CBJ/` 'captivity': 20 after the article and 2 after `MN` (Ezra 2:1 and
  Nehemiah 7:6), where the dagesh is the article's or the assimilated nun's. Without the
  dagesh, the BHSA spells the qal imperative, feminine singular, of `JCB[` שְׁבִי at 6
  words (Genesis 38:11 first), as it spells the noun שְׁבִי (Isaiah 49:24 first).
- **MAM's atom:** שְּׁבִ֖י. **WLC 4.18's:** שְּׁבִ֖י. Both have the dagesh too.
- **Reason:** The test's key keeps a dagesh that here follows no article or preposition (the
  atom before, ק֥וּמִי, ends in a vowel and has merkha, a conjunctive accent, on its first
  syllable), and so it groups the imperative with 'the captivity'; without the dagesh, the
  pointing is the normal spelling of the imperative, which is the analysis.

Isaiah 52:2, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `N<R[` hit impv p2 sg f 'shake off' (VP Pred) | הִתְנַעֲרִ֧י | הִתְנַעֲרִ֧י |
| 2 | `MN` prep 'from' (PP Adju); `<PR/` subs sg 'dust' (PP Adju) | מֵעָפָ֛ר | מֵעָפָ֛ר |
| 3 | `QWM[` qal impv p2 sg f 'arise' (VP Pred) | ק֥וּמִי | ק֥וּמִי |
| **4** | `JCB[` qal impv p2 sg f 'sit' (VP Pred) | שְּׁבִ֖י | שְּׁבִ֖י |
| 5 | `JRWCLM/` nmpr sg 'Jerusalem' (PrNP Voct) | יְרֽוּשָׁלִָ֑ם | יְרוּשָׁלָ֑͏ִם |
| 6 | `PTX[` hit impv p2 sg f 'open' (VP Pred) | התפתחו | התפתחו |
| 7 | `MWSR=/` subs pl 'band' (NP Objc) | מֹוסְרֵ֣י | מוֹסְרֵ֣י |
| 8 | `YW>R/` subs sg suffix `K=` 'neck' (NP Objc) | צַוָּארֵ֔ךְ | צַוָּארֵ֔ךְ |
| 9 | `CBJH/` subs sg 'captive' (NP Voct) | שְׁבִיָּ֖ה | שְׁבִיָּ֖ה |
| 10 | `BT/` subs sg 'daughter' (NP Voct) | בַּת־ | בַּת־ |
| 11 | `YJWN==/` nmpr sg 'Zion' (NP Voct) | צִיֹּֽון | צִיּֽוֹן׃ |

## The new candidate

### 2 Chronicles 28:19: correction

- **The BHSA's analysis:** slot 420804, the atom מַ֖עַל, `M<L[` 'be unfaithful', qal
  perfect, third masculine singular, the predicate (`VP Pred`) of a clause of type `WxQ0`. The
  atom before, וּמָעֹול, is `M<L[` qal infinitive absolute, analysed as a modifier
  (`AdvP Modi`), and the atom after, בַּיהוָה, is the clause's complement (`PP Cmpl`).
- **The pointing elsewhere:** the BHSA's other 13 words with the key מַעַל are the noun
  `M<L=/` 'unfaithfulness' (Leviticus 5:15 first). Its five other qal perfects, third masculine
  singular, of `M<L[` are מָעַל (Joshua 22:20 first), with qamats under the mem; none of
  its qal perfects of `M<L[` has pataḥ there. מָעַל is also the noun's form at 3 words
  (Numbers 5:12 first).
- **MAM's atom:** מַ֖עַל. **WLC 4.18's:** מַ֖עַל.
- **Reason:** The pointing, with pataḥ under the mem, is the noun's at all 13 other words of its
  key and no qal perfect's, and the analysis reads it as the finite verb מָעַל, with the
  infinitive absolute before it as that verb's modifier.

2 Chronicles 28:19, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| 1 | `KJ` conj 'that' (CP Conj) | כִּֽי־ | כִּֽי־ |
| 2 | `KN<[` hif perf p3 sg m 'be humble' (VP Pred) | הִכְנִ֤יעַ | הִכְנִ֤יעַ |
| 3 | `JHWH/` nmpr sg 'YHWH' (PrNP Subj) | יְהוָה֙ | יְהֹוָה֙ |
| 4 | `>T` prep '<object marker>' (PP Objc) | אֶת־ | אֶת־ |
| 5 | `JHWDH/` nmpr sg 'Judah' (PP Objc) | יְהוּדָ֔ה | יְהוּדָ֔ה |
| 6 | `B` prep 'in' (PP Adju); `<BWR/` subs sg 'way' (PP Adju) | בַּעֲב֖וּר | בַּעֲב֖וּר |
| 7 | `>XZ=/` nmpr sg 'Ahaz' (PP Adju) | אָחָ֣ז | אָחָ֣ז |
| 8 | `MLK/` subs sg 'king' (PP Adju) | מֶֽלֶךְ־ | מֶֽלֶךְ־ |
| 9 | `JFR>L/` nmpr sg 'Israel' (PP Adju) | יִשְׂרָאֵ֑ל | יִשְׂרָאֵ֑ל |
| 10 | `KJ` conj 'that' (CP Conj) | כִּ֤י | כִּ֤י |
| 11 | `PR<[` hif perf p3 sg m 'let loose' (VP Pred) | הִפְרִ֨יעַ֙ | הִפְרִ֙יעַ֙ |
| 12 | `B` prep 'in' (PP Cmpl); `JHWDH/` nmpr sg 'Judah' (PP Cmpl) | בִּֽיהוּדָ֔ה | בִּֽיהוּדָ֔ה |
| 13 | `W` conj 'and' (CP Conj); `M<L[` qal infa 'be unfaithful' (AdvP Modi) | וּמָעֹ֥ול | וּמָע֥וֹל |
| **14** | `M<L[` qal perf p3 sg m 'be unfaithful' (VP Pred) | מַ֖עַל | מַ֖עַל |
| 15 | `B` prep 'in' (PP Cmpl); `JHWH/` nmpr sg 'YHWH' (PP Cmpl) | בַּיהוָֽה | בַּיהֹוָֽה׃ |

## The last 50 groups, line by line

The line is the line of `out/30-part2-test-a.txt`; the pointed key is the review's key of the
written word (accents, meteg and rafeh stripped); an analysis is the lexeme and, for a verb, its
stem and tense. The context of every word, with the slots before and after it and MAM's atom, is
in `out/p2a-groups.txt`.

Categories: correction 1, homograph: name 29, homograph: homonym 4, homograph 10, artifact 6. By the review's key, with the BHSA's way of writing a ḥolam male allowed for (`bc_common.bkey`), MAM's atom has the BHSA's pointing at 58 of the 58 words of these 50 groups.

| Line | Category | Pointed key | Flagged analysis | The key's analyses | Where | Reason |
|---|---|---|---|---|---|---|
| 259 | artifact | יָּבֹוא | `BW>[ qal impf` x1 | `BW>[ qal wayq` x19, `BW>[ qal impf` x1 | Qoheleth 2:12 | The dagesh in the yod follows the relative particle `C`, a slot of its own, not a wayyiqtol's conjunction; the qal imperfect is what the pointing spells. |
| 260 | artifact | יֹּאכַל | `>KL[ qal impf` x2 | `>KL[ qal wayq` x21, `>KL[ qal impf` x2 | Qoheleth 2:24; Qoheleth 3:13 | As at line 259: both words follow the relative particle `C`. |
| 261 | artifact | יִּרְאוּ | `JR>[ qal impf` x1 | `R>H[ qal wayq` x39, `JR>[ qal wayq` x9, `JR>[ qal impf` x1 | Qoheleth 3:14 | As at line 259 for the tense. The lexeme `JR>[` for this one-yod pointing is the key's second analysis (9 wayyiqtol words) and Micah 7:17's. |
| 262 | homograph | בַקֵּשׁ | `BQC[ piel infa` x1 | `BQC[ piel infc` x28, `BQC[ piel infa` x1 | Qoheleth 7:25 | The piel infinitives absolute and construct of `BQC[` are spelled alike; this one, after two infinitives construct with `L` and without one, is read as absolute. |
| 263 | artifact | יֹּאמְרוּ | `>MR[ qal impf` x1 | `>MR[ qal wayq` x297, `>MR[ qal impf` x1 | Lamentations 2:15 | As at line 259: the relative particle `C`. |
| 264 | homograph | נָבִיא | `BW>[ hif impf` x2 | `NBJ>/` x36, `BW>[ hif impf` x2 | Lamentations 5:9; Nehemiah 10:38 | The hiphil imperfect, first person plural, of `BW>[` ('we bring') is spelled like 'prophet'; each place has an object (`Objc`). |
| 265 | homograph: homonym | שְׁנָתֹו | `CNH=/` x1 | `CNH/` x17, `CNH=/` x1 | Daniel 2:1 | `CNH=/` 'sleep' and `CNH/` 'year', each with the suffix `W`, are spelled alike. |
| 266 | artifact | אֲדַבְּרָה | `DBR[ piel wayq` x1 | `DBR[ piel impf` x15, `DBR[ piel wayq` x1 | Daniel 10:16 | The wayyiqtol is marked only by the conjunction's qamats before alef, in the slot `W`; the first person piel imperfect and wayyiqtol are otherwise spelled alike. |
| 267 | homograph | יָּמִין | `JWM/` x1 | `JMJN/` x18, `JWM/` x1 | Daniel 12:13 | The -in plural of 'day': the BHSA's `nme` is `JN` here and on 23 other Hebrew words (13 of them `MLH/` in Job); 'at the end of the ...' decides against 'the right hand'. |
| 268 | homograph: name | מִסְפָּר | `MSPR=/` x1 | `MSPR/` x40, `MSPR=/` x1 | Ezra 2:2 | A proper name, `MSPR=/` 'Mispar', spelled like `MSPR/` 'number', the key's commonest analysis. |
| 269 | homograph: name | כְּרוּב | `KRWB=/` x2 | `KRWB/` x24, `KRWB=/` x2 | Ezra 2:59; Nehemiah 7:61 | A proper name, `KRWB=/` 'Kerub', spelled like `KRWB/` 'cherub', the key's commonest analysis. |
| 270 | homograph: homonym | יַּעֲנוּ | `<NH==[ qal wayq` x1 | `<NH[ qal wayq` x15, `<NH==[ qal wayq` x1 | Ezra 3:11 | `<NH==[` 'sing' and `<NH[` 'answer' are spelled alike. |
| 271 | artifact | אָשִׁיב | `CWB[ hif wayq` x2 | `CWB[ hif impf` x23, `CWB[ hif wayq` x2 | Nehemiah 2:20; Nehemiah 6:4 | As at line 266: the conjunction's qamats before alef. |
| 272 | homograph: homonym | יַּעַזְבוּ | `<ZB=[ qal wayq` x1 | `<ZB[ qal wayq` x11, `<ZB=[ qal wayq` x1 | Nehemiah 3:8 | `<ZB=[` (the BHSA's gloss 'flag') and `<ZB[` 'leave' are spelled alike. |
| 273 | homograph | נַעֲשֶׂה | `<FH[ nif ptca` x1 | `<FH[ qal impf` x27, `<FH[ nif ptca` x1 | Nehemiah 5:18 | The niphal participle and the qal imperfect, first person plural, of `<FH[` are spelled alike; after `HJH[` 'be' the participle is read. |
| 274 | homograph | מִרְיָם | `MRJ/` x1 | `MRJM/` x15, `MRJ/` x1 | Nehemiah 9:17 | `MRJ/` 'rebellion' with the suffix `M` ('their rebellion') is spelled like the name Miriam. |
| 275 | homograph: name | עָנָן | `<NN=/` x1 | `<NN/` x76, `<NN=/` x1 | Nehemiah 10:27 | A proper name, `<NN=/` 'Anan', spelled like `<NN/` 'cloud', the key's commonest analysis. |
| 276 | homograph: name | יֵשׁוּעַ | `JCW<=/` x1 | `JCW</` x28, `JCW<=/` x1 | Nehemiah 11:26 | A proper name, `JCW<=/` 'Jeshua', spelled like the name `JCW</` 'Jeshua', the key's commonest analysis. |
| 277 | homograph: name | אַפַּיִם | `>PJM/` x1 | `>P/` x27, `>PJM/` x1 | 1 Chronicles 2:31 | A proper name, `>PJM/` 'Appaim', spelled like `>P/` 'nose', the key's commonest analysis. |
| 278 | homograph: name | שָׁמַע | `CM<===/` x1 | `CM<[ qal perf` x72, `CM<=/` x1, `CM<===/` x1 | 1 Chronicles 2:43 | A proper name, `CM<===/` 'Shema', spelled like `CM<[ qal perf` 'hear', the key's commonest analysis. |
| 279 | homograph: name | שֶׁבֶר | `CBR===/` x1 | `CBR/` x28, `CBR=/` x4, `CBR===/` x1 | 1 Chronicles 2:48 | A proper name, `CBR===/` 'Sheber', spelled like `CBR/` 'breaking', the key's commonest analysis. |
| 280 | homograph: name | אֹהֶל | `>HL=/` x1 | `>HL/` x235, `>HL=/` x1 | 1 Chronicles 3:20 | A proper name, `>HL=/` 'Ohel', spelled like `>HL/` 'tent', the key's commonest analysis. |
| 281 | homograph: name | מְחִיר | `MXJR=/` x1 | `MXJR/` x13, `MXJR=/` x1 | 1 Chronicles 4:11 | A proper name, `MXJR=/` 'Mehir', spelled like `MXJR/` 'price', the key's commonest analysis. |
| 282 | homograph: name | רִנָּה | `RNH=/` x1 | `RNH/` x25, `RNH=/` x1 | 1 Chronicles 4:20 | A proper name, `RNH=/` 'Rinnah', spelled like `RNH/` 'cry of joy', the key's commonest analysis. |
| 283 | homograph: name | עֶצֶם | `<YM===/` x1 | `<YM/` x28, `<YM===/` x1 | 1 Chronicles 4:29 | A proper name, `<YM===/` 'Ezem', spelled like `<YM/` 'bone', the key's commonest analysis. |
| 284 | homograph: name | בָּעַל | `B<L=/` x1 | `B<L/` x15, `B<L=/` x1 | 1 Chronicles 4:33 | A proper name, `B<L=/` 'Baalath', spelled like `B<L/` 'lord, baal', the key's commonest analysis. |
| 285 | homograph: name | בַּעַל | `B<L==/` x1 | `B<L/` x64, `B<L==/` x1 | 1 Chronicles 5:5 | A proper name, `B<L==/` 'Baal', spelled like `B<L/` 'lord, baal', the key's commonest analysis. |
| 286 | homograph: name | אֲחִי | `>XJ=/` x2 | `>X/` x36, `>XJ=/` x2 | 1 Chronicles 5:15; 1 Chronicles 7:34 | A proper name, `>XJ=/` 'Ahi', spelled like `>X/` 'brother', the key's commonest analysis. |
| 287 | homograph: name | תַּחַת | `TXT==/` x2 | `TXT/` x298, `TXT==/` x2 | 1 Chronicles 6:9; 1 Chronicles 6:22 | A proper name, `TXT==/` 'Tahath', spelled like `TXT/` 'under part', the key's commonest analysis. |
| 288 | homograph: name | בִּלְעָם | `BL<M=/` x1 | `BL<M/` x51, `BL<M=/` x1 | 1 Chronicles 6:55 | A proper name, `BL<M=/` 'Bileam', spelled like the name `BL<M/` '<prophet>', the key's commonest analysis. |
| 289 | homograph: name | מָשָׁל | `MCL===/` x1 | `MCL/` x17, `MCL[ qal perf` x2, `MCL===/` x1 | 1 Chronicles 6:59 | A proper name, `MCL===/` 'Mashal', spelled like `MCL/` 'proverb', the key's commonest analysis. |
| 290 | homograph: name | עִיר | `<JR====/` x1 | `<JR/` x627, `<JR===/` x2, `<WR[ hif infc` x1, `<JR====/` x1 | 1 Chronicles 7:12 | A proper name, `<JR====/` 'Ir', spelled like `<JR/` 'town', the key's commonest analysis. |
| 291 | homograph: name | אַחֵר | `>XR==/` x1 | `>XR=/` x57, `>XR==/` x1 | 1 Chronicles 7:12 | A proper name, `>XR==/` 'Aher', spelled like `>XR=/` 'other', the key's commonest analysis. |
| 292 | homograph: name | תַחַת | `TXT==/` x2 | `TXT/` x37, `TXT==/` x2 | 1 Chronicles 7:20; 1 Chronicles 7:20 | A proper name, `TXT==/` 'Tahath', spelled like `TXT/` 'under part', the key's commonest analysis. |
| 293 | homograph: name | עָמָל | `<ML==/` x1 | `<ML/` x27, `<ML==/` x1 | 1 Chronicles 7:35 | A proper name, `<ML==/` 'Amal', spelled like `<ML/` 'labour', the key's commonest analysis. |
| 294 | homograph: name | הֹוד | `HWD=/` x1 | `HWD/` x13, `HWD=/` x1 | 1 Chronicles 7:37 | A proper name, `HWD=/` 'Hod', spelled like `HWD/` 'splendour', the key's commonest analysis. |
| 295 | homograph: name | חֹדֶשׁ | `XDC==/` x1 | `XDC=/` x231, `XDC==/` x1 | 1 Chronicles 8:9 | A proper name, `XDC==/` 'Hodesh', spelled like `XDC=/` 'month', the key's commonest analysis. |
| 296 | homograph: name | מִרְמָה | `MRMH=/` x1 | `MRMH/` x36, `MRMH=/` x1 | 1 Chronicles 8:10 | A proper name, `MRMH=/` 'Mirmah', spelled like `MRMH/` 'deceit', the key's commonest analysis. |
| 297 | homograph: name | מֶלֶךְ | `MLK==/` x2 | `MLK/` x992, `MLK==/` x2 | 1 Chronicles 8:35; 1 Chronicles 9:41 | A proper name, `MLK==/` 'Melech', spelled like `MLK/` 'king', the key's commonest analysis. |
| 298 | homograph: name | בְרָכָה | `BRKH==/` x1 | `BRKH/` x16, `BRKH==/` x1 | 1 Chronicles 12:3 | A proper name, `BRKH==/` 'Beracah', spelled like `BRKH/` 'blessing', the key's commonest analysis. |
| 299 | homograph: name | בֵּן | `BN=/` x1 | `BN/` x92, `BN=/` x1 | 1 Chronicles 15:18 | A proper name, `BN=/` 'Ben', spelled like `BN/` 'son', the key's commonest analysis. |
| 300 | homograph: name | שְׂעֹרִים | `F<RJM/` x1 | `F<RH/` x20, `F<RJM/` x1 | 1 Chronicles 24:8 | A proper name, `F<RJM/` 'Seorim', spelled like `F<RH/` 'barley', the key's commonest analysis. |
| 301 | homograph: name | קֹרֵא | `QWR>/` x1 | `QR>[ qal ptca` x13, `QR>/` x1, `QWR>/` x1 | 1 Chronicles 26:1 | A proper name, `QWR>/` 'Kore', spelled like `QR>[ qal ptca` 'call', the key's commonest analysis. |
| 302 | homograph | עֹולָה | `<LH[ qal ptca` x1 | `<LH/` x35, `<WLH/` x1, `<LH[ qal ptca` x1 | 1 Chronicles 26:16 | The qal participle, feminine singular, of `<LH[` 'ascend', after the article, is spelled like `<LH/` 'burnt offering'. |
| 303 | homograph | גָּדֹול | `GDL[ qal infa` x1 | `GDWL/` x244, `GDL[ qal infa` x1 | 2 Chronicles 2:8 | The qal infinitive absolute of `GDL[` is spelled like the adjective `GDWL/` 'great'; the BHSA has it without the dagesh, גָדֹול, at 2 Samuel 5:10 and 1 Chronicles 11:9, and here it is paired with the hiphil infinitive absolute הַפְלֵא. |
| 304 | homograph | בֹוא | `BW>[ qal impv` x1 | `BW>[ qal infc` x113, `BW>[ qal infa` x3, `BW>[ qal impv` x1 | 2 Chronicles 18:29 | The qal imperative, masculine singular, of `BW>[` is spelled like its infinitive construct; the parallel 1 Kings 22:30, וָבֹא, is analysed as an imperative too. |
| 305 | homograph: homonym | תְּדַבֵּר | `DBR=[ piel wayq` x1 | `DBR[ piel impf` x19, `DBR[ piel wayq` x15, `DBR=[ piel wayq` x1 | 2 Chronicles 22:10 | `DBR=[` 'push back' and `DBR[` 'speak' are spelled alike. |
| 306 | homograph | שָׁרֵת | `CRT/` x1 | `CRT[ piel infc` x18, `CRT/` x1 | 2 Chronicles 24:14 | The noun `CRT/` 'cultic service' is spelled like the piel infinitive construct of `CRT[`. |
| 307 | homograph | חָזָק | `XZQ[ qal perf` x1 | `XZQ/` x19, `XZQ[ qal perf` x1 | 2 Chronicles 26:15 | The verse's last atom, with silluq: the qal perfect's pausal form, spelled like the adjective `XZQ/` 'strong'; the BHSA's five other qal perfects, third masculine singular, of `XZQ[` without a suffix are חָזַק, with pataḥ under the zayin. |
| 308 | **correction** | מַעַל | `M<L[ qal perf` x1 | `M<L=/` x13, `M<L[ qal perf` x1 | 2 Chronicles 28:19 | The pointing is that of the noun `M<L=/` 'unfaithfulness'; the BHSA's five other qal perfects, third masculine singular, of `M<L[` are מָעַל, with qamats under the mem. A new candidate: see its section. |

## A related place that Test A cannot flag

1 Samuel 18:29's וַיֹּאסֶף is 2 Samuel 6:1's mirror image: written with an alef, as a
wayyiqtol of `>SP[` with a quiescent alef would be, and analysed as `JSP[` hiphil wayyiqtol
'did again', with the infinitive לֵרֹא 'to fear' after it. It is defective-or-ambiguous,
not a correction, and Test A cannot see it, since its pointed key has no other word in the BHSA.

1 Samuel 18:29, atom by atom (the reviewed atom's number in bold):

| # | The BHSA's analysis, slot by slot | The BHSA's atom | MAM's atom |
|---|---|---|---|
| **1** | `W` conj 'and' (CP Conj); `JSP[` hif wayq p3 sg m 'add' (VP Pred) | וַיֹּ֣אסֶף | וַיֹּ֣אסֶף |
| 2 | `C>WL=/` nmpr sg 'Saul' (PrNP Subj) | שָׁא֗וּל | שָׁא֗וּל |
| 3 | `L` prep 'to' (VP Pred); `JR>[` qal infc 'fear' (VP Pred) | לֵרֹ֛א | לֵרֹ֛א |
| 4 | `MN` prep 'from' (PP Cmpl); `PNH/` subs pl 'face' (PP Cmpl) | מִפְּנֵ֥י | מִפְּנֵ֥י |
| 5 | `DWD==/` nmpr sg 'David' (PP Cmpl) | דָוִ֖ד | דָוִ֖ד |
| 6 | `<WD/` subs sg 'duration' (AdvP Modi) | עֹ֑וד | ע֑וֹד |
| 7 | `W` conj 'and' (CP Conj); `HJH[` qal wayq p3 sg m 'be' (VP Pred) | וַיְהִ֥י | וַיְהִ֥י |
| 8 | `C>WL=/` nmpr sg 'Saul' (PrNP Subj) | שָׁא֛וּל | שָׁא֛וּל |
| 9 | `>JB[` qal ptca sg m 'be hostile' (VP PreC) | אֹיֵ֥ב | אֹיֵ֥ב |
| 10 | `>T` prep '<object marker>' (PP Objc) | אֶת־ | אֶת־ |
| 11 | `DWD==/` nmpr sg 'David' (PP Objc) | דָּוִ֖ד | דָּוִ֖ד |
| 12 | `KL/` subs sg 'whole' (NP Time) | כָּל־ | כׇּל־ |
| 13 | `H` art 'the' (NP Time); `JWM/` subs pl 'day' (NP Time) | הַיָּמִֽים | הַיָּמִֽים׃ |

## How this was checked

- `scripts/p2a_check.py` wrote `out/p2a-groups.txt` (each group's words in context) and
  `out/p2a-candidates.txt` (each candidate verse word by word with MAM's atoms, the candidate's
  pointed key with examples, the analysed lexeme's spellings, and the queries cited here).
  `scripts/p2a_extra.py` wrote `out/p2a-extra.txt` (the one-yod spellings of `JR>[`, the qal
  words of `>SP[` with ḥolam on their first letter, and WLC 4.18's atoms at the reviewed
  places). `scripts/p2a_render.py` wrote this page.
- Pointed keys and analyses are `scripts/part2_scan.py`'s. The BHSA's atoms are its slots joined
  as `bc_common.Bhsa.atoms` joins them, on the ketiv side. MAM's atoms, and WLC 4.18's, are
  aligned with the BHSA's by letters.
- Not done: no lexicon or commentary was consulted, so whether the ETCBC means 1 Samuel 27:10's
  `>L==` as a rare word or as an emendation, and why it reads 2 Chronicles 28:19's noun as a
  verb, rest on the BHSA's own data; the ETCBC's documentation, as the README reports, states no
  policy on either.
