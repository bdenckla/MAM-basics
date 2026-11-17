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
   The BHSA's atom {atomk:420804} has the pointing of the noun `M<L=/` 'unfaithfulness', as the
   BHSA's 13 other words of that pointed key do, and is analysed as the qal perfect of `M<L[`
   'be unfaithful', whose five other third masculine singular perfects in the BHSA are all
   spelled {gk:125766}, with qamats under the mem. WLC 4.18 and MAM have the BHSA's atom.
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

- **The BHSA's analysis:** slot 158430, the atom {atomk:158430}, lexeme `>L==` ({vl:158430}),
  part of speech `inrg` (interrogative), gloss 'where', in its own phrase `InrP` with function
  `Ques`, in a clause of type `xQt0` whose predicate is {gk:158431}, `PCV[` qal perfect, second
  masculine plural.
- **The pointing elsewhere:** the BHSA's other words with the key {gk:158430} are the negative
  `>L=` 723 times (Genesis 13:8 first), the preposition `>L` twice (Judges 19:23 and Jeremiah
  47:6, Part 1's corrections) and `>L=/` once (Job 24:25). `>L==` occurs only here.
- **MAM's atom:** {mam:158430}. **WLC 4.18's:** {wlc:158430}.
- **Reason:** The pointing is the negative's, as at 723 other words, and the analysis takes it
  as an interrogative 'where' that the BHSA has nowhere else, so, unlike Exodus 10:28's
  correction, which names a word the BHSA spells otherwise elsewhere, this one shows only as a
  lexeme of its own.

{verse:1Sam:27:10:158430}

### 2. Job 24:25: homograph

- **The BHSA's analysis:** slot 342192, in the atom {atomk:342192} after the preposition `L`,
  lexeme `>L=/` ({vl:342192}), a noun (`subs`), singular, absolute, gloss 'nothingness', in a
  `PP` with function `Cmpl` of {gk:342190}, `FJM[` 'put' qal imperfect, whose object
  is {gk:342193} 'my word'.
- **The pointing elsewhere:** the key is 1 Samuel 27:10's, {gk:342192}: the negative `>L=` 723
  times (Genesis 13:8 first). `>L=/` occurs only here.
- **MAM's atom:** {mam:342192}. **WLC 4.18's:** {wlc:342192}.
- **Reason:** 'Nothing' is the negative itself, used as a noun after a preposition, which the
  ETCBC files under a lexeme of its own, so the analysis reads the word the pointing spells and
  differs from the 723 only in its part of speech.

{verse:Job:24:25:342192}

### 3. 2 Samuel 6:1: defective-or-ambiguous

- **The BHSA's analysis:** slot 163423, the atom {atomk:163423}, `>SP[` 'gather', qal
  wayyiqtol, third masculine singular, the predicate of a clause whose object (`PP Objc`) is
  atoms 4 to 9 below, 'all the chosen men in Israel, thirty thousand', with {gk:163424}
  'again' as a modifier (`AdvP Modi`).
- **The pointing elsewhere:** the BHSA's other 21 words with the key {gk:163423} are `JSP[`
  'add', hiphil wayyiqtol (Genesis 8:10 first). All 23 of its other qal wayyiqtol third
  masculine singular words of `>SP[` have the alef: {gk:15344} 19 times (Genesis 29:22 first),
  then {gk:126636} once (Joshua 24:1), and three with suffixes. Its only other word of `>SP[`
  without an alef is {gk:328516} at Psalms 104:29, a qal imperfect, second masculine singular.
  Conversely, it analyses 1 Samuel 18:29's {atomk:152786}, written with an alef, as `JSP[`
  hiphil wayyiqtol.
- **MAM's atom:** {mam:163423}. **WLC 4.18's:** {wlc:163423}.
- **Reason:** The vowels, ḥolam on the prefix and segol under the samekh, are those of 1 Samuel
  18:29's {atomk:152786} with its alef unwritten, so the pointing permits `>SP[` without the root's
  quiescent alef, as the BHSA also reads Psalms 104:29, while being the normal spelling of
  `JSP[`; the BHSA lets the sense decide here and at 1 Samuel 18:29 alike.

{verse:2Sam:6:1:163423}

### 4. Micah 1:15: defective-or-ambiguous

- **The BHSA's analysis:** slot 299793, the atom {atomk:299793}, `BW>[` 'come', hiphil
  imperfect, first person singular ('I will bring'), the predicate of a clause of type `xYq0`
  whose object (`NP Objc`) is {atomk:299792} 'the dispossessor', with {gk:299790} 'again'
  (`AdvP Modi`) and {gk:299794} 'to you' (`PP Cmpl`).
- **The pointing elsewhere:** the BHSA's other 134 words with the key {gk:299793} are `>B/`
  'father' with the suffix `J`, 'my father' (Genesis 19:34 first). Its 16 other hiphil
  imperfects of `BW>[`, first person singular, without a suffix, are {gk:34457}, with the alef
  (Exodus 11:1 first). Its only other word of `BW>[` without an alef is {gk:156661} at 1 Samuel
  25:8, a qal perfect, first person plural (Test A's line 98).
- **MAM's atom:** {mam:299793}. **WLC 4.18's:** {wlc:299793}.
- **Reason:** The vowels are those of {gk:34457}, and only the root's final quiescent alef is
  unwritten, as at 1 Samuel 25:8, so the pointing permits 'I will bring', the reading that gives
  the clause and its object a verb.

{verse:Mic:1:15:299793}

### 5. Micah 7:17: defective-or-ambiguous

- **The BHSA's analysis:** slot 301390, the atom {atomk:301390}, `JR>[` 'fear', qal imperfect,
  third masculine plural, the predicate of a clause of type `WYq0` with {gk:301391} 'of you'
  (`PP Cmpl`), after {gk:301388}, `PXD[` 'tremble', qal imperfect, third masculine plural.
- **The pointing elsewhere:** the BHSA's other 28 words with the key {gk:301390} are `R>H[`
  'see', qal imperfect (Genesis 12:12 first). Its qal imperfects of `JR>[`, third masculine
  plural, without a suffix, are {gk:93807}, with two yods and sheva under the resh, 8 times
  (Deuteronomy 2:4 first); {gk:103265}, with one yod and qamats under the resh, 4 times
  (Deuteronomy 17:13 first), and once more with a final nun; and {gk:226135}, with two yods and
  qamats, 4 times (Isaiah 41:5 first). It reads the one-yod pointing with sheva as 'fear' at 9
  wayyiqtol words, {gk:114735} (Joshua 4:14 first), and at Ecclesiastes 3:14 (Test A's line
  261).
- **MAM's atom:** {mam:301390}. **WLC 4.18's:** {wlc:301390}.
- **Reason:** The pointing is a defective spelling of 'they will fear', one yod for the two of
  the BHSA's eight such imperfects with sheva, and the BHSA reads the same one-yod pointing as
  'fear' at 10 other words; 'of you' and the parallel 'tremble' decide against 'see'.

{verse:Mic:7:17:301390}

### 6. Isaiah 52:2: artifact

- **The BHSA's analysis:** slot 230330, the atom {atom:230330}, `JCB[` 'sit', qal imperative,
  second feminine singular, the predicate of a clause of type `ZIm0`, after {atom:230329},
  `QWM[` 'arise', qal imperative, second feminine singular; Jerusalem is the vocative.
- **The pointing elsewhere:** the BHSA's other 22 words with the key {gk:230330}, with a dagesh
  in the shin, are `CBJ/` 'captivity': 20 after the article and 2 after `MN` (Ezra 2:1 and
  Nehemiah 7:6), where the dagesh is the article's or the assimilated nun's. Without the
  dagesh, the BHSA spells the qal imperative, feminine singular, of `JCB[` {gk:21002} at 6
  words (Genesis 38:11 first), as it spells the noun {gk:229576} (Isaiah 49:24 first).
- **MAM's atom:** {mam:230330}. **WLC 4.18's:** {wlc:230330}. Both have the dagesh too.
- **Reason:** The test's key keeps a dagesh that here follows no article or preposition (the
  atom before, {atom:230329}, ends in a vowel and has merkha, a conjunctive accent, on its first
  syllable), and so it groups the imperative with 'the captivity'; without the dagesh, the
  pointing is the normal spelling of the imperative, which is the analysis.

{verse:Isa:52:2:230330}

## The new candidate

### 2 Chronicles 28:19: correction

- **The BHSA's analysis:** slot 420804, the atom {atom:420804}, `M<L[` 'be unfaithful', qal
  perfect, third masculine singular, the predicate (`VP Pred`) of a clause of type `WxQ0`. The
  atom before, {atomk:420803}, is `M<L[` qal infinitive absolute, analysed as a modifier
  (`AdvP Modi`), and the atom after, {atomk:420805}, is the clause's complement (`PP Cmpl`).
- **The pointing elsewhere:** the BHSA's other 13 words with the key {gk:420804} are the noun
  `M<L=/` 'unfaithfulness' (Leviticus 5:15 first). Its five other qal perfects, third masculine
  singular, of `M<L[` are {gk:125766} (Joshua 22:20 first), with qamats under the mem; none of
  its qal perfects of `M<L[` has pataḥ there. {gk:125766} is also the noun's form at 3 words
  (Numbers 5:12 first).
- **MAM's atom:** {mam:420804}. **WLC 4.18's:** {wlc:420804}.
- **Reason:** The pointing, with pataḥ under the mem, is the noun's at all 13 other words of its
  key and no qal perfect's, and the analysis reads it as the finite verb {gk:125766}, with the
  infinitive absolute before it as that verb's modifier.

{verse:2Chr:28:19:420804}

## The last 50 groups, line by line

The line is the line of `out/30-part2-test-a.txt`; the pointed key is the review's key of the
written word (accents, meteg and rafeh stripped); an analysis is the lexeme and, for a verb, its
stem and tense. The context of every word, with the slots before and after it and MAM's atom, is
in `out/p2a-groups.txt`.

{groups}

## A related place that Test A cannot flag

1 Samuel 18:29's {atomk:152786} is 2 Samuel 6:1's mirror image: written with an alef, as a
wayyiqtol of `>SP[` with a quiescent alef would be, and analysed as `JSP[` hiphil wayyiqtol
'did again', with the infinitive {atomk:152789} 'to fear' after it. It is defective-or-ambiguous,
not a correction, and Test A cannot see it, since its pointed key has no other word in the BHSA.

{verse:1Sam:18:29:152786}

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
