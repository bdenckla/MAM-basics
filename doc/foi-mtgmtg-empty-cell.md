# Why the mtgmtg survey's `2/sopa-y/maq-n` group is empty: coincidental, not structural

**The answer is coincidental scarcity.** Neither Yeivin nor Breuer states a rule that would forbid
a lone verse-final atom from having a silluq and two metegs, and the arithmetic puts the expected
number of such atoms in MAM at about one or below, so an empty group is what the corpus should
produce with no rule at all. Investigated 2026-09-09 at MAM-basics commit `becc6f00`.

A note on vocabulary before anything else. This file says **meteg** where it speaks in its voice,
per the `hebrew-prose` skill's rule for accgram, and says **ga'ya** (Yeivin) and **ga'aya**
(Breuer) where it reports what those two books say, per the same rule's instruction not to reword a
quotation. The three names are the same mark.

## The figures, and how to re-establish them

Run from `C:/Users/BenDe/GitRepos/MAM-basics`, on that clone's interpreter (a worktree spells the
interpreter absolutely and runs from the worktree root):

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-mtgmtg
```

That rewrites `gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` and `foi-mtgmtg.html`. On 2026-09-09 the
run left the working tree clean, so the figures below are the tracked ones. Treat any change from
them as a finding.

| Group | Count |
| --- | --- |
| `1/sopa-y/maq-n` | 354 |
| `1/sopa-y/maq-y` | 229 |
| `2/sopa-n/maq-n` | 19 |
| `2/sopa-n/maq-y` | 102 |
| `2/sopa-y/maq-y` | 14 |
| `2/sopa-y/maq-n` | 0 |

**Only one of the grid's three empty cells is a real gap.** `py/foi/foiz_wt_mtgmtg.py` collects a
chanted word only when it has at least two U+05BD, and for a `sopa-n` chanted word every U+05BD
is a meteg, so `1/sopa-n/maq-n` and `1/sopa-n/maq-y` cannot be populated however the corpus
behaves. The question is about `2/sopa-y/maq-n` alone.

## What Yeivin says: two rules about ga'ya count, none about silluq

The full OCR is `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/`,
where the ga'ya run §§309–357 sits in `N0309.md`, `N0328.md`, `N0329.md`, `N0338.md`, `N0342.md`
and `N0345.md`.

1. **§339 makes two ga'yot on one word rare in principle**, and it draws no line between an atom
   and a maqaf compound: "In early MSS, such as A, L, C, two *gaʿyas* are only rarely marked on
   the same word (or on a group of words joined by *maqqef*). Where a word or word group could
   have more than one *gaʿya*, only one of them is generally marked." §340 and §341 give the
   preference rules that decide which single ga'ya wins: a closed syllable over an open one in
   general (§340), and, where the choice is between an open syllable and a closed syllable with
   a long vowel, the closed one when it stands immediately before the stress and the open one
   otherwise (§341).
2. **§356 names the one configuration that escapes §339**, and it is the configuration MAM's
   two-meteg atoms are in: "It was noted above (#339) that only one musical *gaʿya* was normally
   marked on a word, even where more than one could appear. This is not, however, the case where a
   phonetic *gaʿya* is involved. In this case two *gaʿyas* are marked on the same word even in MSS
   like A and L, where this is otherwise very rare." Its worked examples are Judges 7:7,
   Job 42:10, 2 Chronicles 7:14, Ezekiel 36:3, 1 Chronicles 7:3, Nehemiah 6:10, Hosea 4:17 and
   Lamentations 5:5 — every one of which MAM has in `2/sopa-n/maq-n` or `2/sopa-y/maq-y`.
3. **The ga'ya run never mentions silluq, sof pasuq, or the end of a verse.** `grep -i` over those
   six files returns nothing for `sof pasuq` and nothing for `silluq`; the five silluq hits in
   `N0345.md` all fall after line 288, inside "THE ACCENTS OF THE THREE BOOKS" (§358 onward),
   which begins in the same file. Yeivin's categories are keyed to syllable structure and to the
   accent's disjunctive-or-conjunctive character (§316, §320), not to which accent it is.
4. **§320 makes the verse end more hospitable to a ga'ya, not less.** The heavy ga'ya of regular
   structure "is generally marked" when the accent is disjunctive and generally not when it is
   conjunctive, and silluq is the strongest disjunctive there is.
5. **§332 is the one ga'ya category a verse end genuinely excludes**, and it is not the category
   at issue. A ga'ya on an open syllable after the accent is marked when the word "stands before a
   word with the accent on the first syllable" — a following word being part of the condition. A
   verse-final word has none. §357 is its companion, on the maqaf written after such a word.

## What Breuer says: rules keyed to the accent's distance, and to verse-initial ethnakhta

The OCR is `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/`;
Chapter 8 is the ga'aya chapter, in `C08-S001.md` through `C08-S041.md`. Breuer spells it
**ga'aya**, so a grep for `ga'ya` or `gaya` misses the whole chapter.

1. **Ch. 8 §1 separates the two marks the way this repo does** — "The shape of the *ga'aya* is
   similar to that of the *siluk*. But the *ga'aya* — unlike the *siluk* — is always written
   beside a *sheva* or beside an unaccentuated vowel. And it indicates a secondary accent, in
   addition to the main accent of the word." A ga'aya therefore never competes with a silluq for a
   syllable: the silluq has the accented one and the ga'aya has an unaccented one.
2. **Breuer has verse-position rules, and they are about the verse's beginning.** The regular
   heavy ga'aya "never appears in the definite article ה — or in the letters בכלמ which are
   vocalized with its vowel — if the vowel that follows it is a *kholam*. The only exception to
   this rule is a word written at the beginning of the verse and cantillated with an *ethnakhta*"
   (Ch. 8 §15, `C08-S011.md`). The ga'aya of sheva likewise "only appears before *ethnakhta* at
   the beginning of the verse" (`C08-S021.md` note 70). Nothing anywhere in the chapter conditions
   a ga'aya on the presence or absence of a siluk.
3. **Breuer states the two-ga'aya case that Yeivin's §356 states**, in `C08-S001.md` note 59: the
   words there sometimes have "a regular heavy *ga'aya* … or a *ga'aya* of *sheva*" beside the
   ga'aya of the guttural, and "the other mss. sometimes omit the *ga'aya* of the guttural in a
   word which is also cantillated with another *ga'aya*", citing Numbers 30:6. So the pairing is
   attested and is a point of manuscript variation, not a prohibition.
4. **Ch. 9 §37 (`C09-S031.md`) says the maqaf survives a secondary mark** — "all the secondary
   cantillation marks in the 21 books appear even in a hyphenated word, and the hyphen is never
   cancelled after them" — which is the nearest either book comes to a rule about the maqaf
   compounds that populate `2/sopa-y/maq-y`, and it permits rather than forbids.

## The quantitative check: the expected count is about one, and it is observed as zero

The census scripts are gitignored, under
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/`: `mtgmtg_population.py`, `mtgmtg_shape_test.py`,
`mtgmtg_controlled.py` and `mtgmtg_verse_final_stems.py`. Each reads the same MAM-parsed-plus data
through the same `wt_qere` handlers the survey uses, and writes a report beside itself. They are
throwaway, so they are unformatted and use `sys.path.insert`. A sixth, `verify_doc_claims.py`,
re-derives every figure and presence claim in this file and raises on drift.

1. **MAM has 263,133 chanted words, and no atom of any of them has more than two U+05BD.** The
   most any chanted word has is three, and every such case is a maqaf compound. So
   `2/sopa-y/maq-n` asks for a lone atom one mark beyond the corpus-wide maximum for a lone atom.
2. **The step-up from one meteg to two, among lone atoms mid-verse, is 19 in 7,451 — 0.255%.**
   Applied to the 354 lone verse-final atoms that already have one meteg, that predicts **0.90**
   such atoms. Under a Poisson model the probability of observing zero is **40.5%**.
3. **Controlling for opportunity does not change the verdict.** Grouping lone atoms by their
   number of reduced vowels — sheva and hataf, which are what most ga'ya categories are triggered
   by — and applying each group's mid-verse step-up rate to the verse-final atoms in it predicts
   **1.00**, for a 36.8% chance of zero. Carrying through the verse-final depression of clause 5
   as well predicts **0.49**, for a 61.5% chance of zero.
4. **The 19 shapes that do have two metegs mid-verse hardly ever end a verse.** They are
   thirteen distinct consonantal skeletons: hitpael forms of פלל, theophoric names in ־יה, and
   one each of מלקקים, להיותכם, ויטיבך and ואחוית. Those thirteen skeletons occur 48 times as lone
   atoms in MAM and **not once at a verse end**. Widening the match to the bare stem finds three
   verse-final instances in all, against 132 mid-verse — and each of the three has one meteg
   fewer than its mid-verse counterparts:

   | Verse-final | Form | U+05BD | Mid-verse counterpart | Form | U+05BD |
   | --- | --- | --- | --- | --- | --- |
   | Psalms 5:3 | אֶתְפַּלָּֽל׃ | 1 | 2 Chronicles 6:26 | וְהִֽתְפַּֽלְל֞וּ | 2 |
   | Nehemiah 12:6 | יְדַֽעְיָֽה׃ | 2 | Nehemiah 12:19 | לִֽידַֽעְיָ֖ה | 2 |
   | 1 Chronicles 4:37 | בֶּן־שְׁמַֽעְיָֽה׃ | 2 | Nehemiah 6:10 | שְֽׁמַֽעְיָ֧ה | 2 |

   Psalms 5:3 shows the mechanism plainly. Where 2 Chronicles 6:26 has a sheva under the
   second lamed, the pausal form at Psalms 5:3 has a full vowel there instead, and with the
   sheva goes the site the meteg would have had.
5. **A lone atom has a meteg at about half the rate at a verse end that it does mid-verse, and
   that holds at every length.** Verse-final lone atoms with at least one meteg number 354 in
   19,764, or 1.79%; mid-verse, 7,451 in 202,147, or 3.69%. Split by reduced-vowel count the
   mid-verse-to-verse-final ratio runs 2.11, 2.39, 1.46 and 2.38. Verse-final lone atoms are not
   shorter — they average 2.30 full vowels against 2.09 mid-verse — so length does not explain it.
   §332's requirement of a following word accounts for part of it and pausal vowel restoration for
   more, but this file does not claim to have measured either. The thinning also runs against
   Yeivin §320, which makes a disjunctive accent favour the heavy ga'ya, so whatever produces
   the thinning is strong enough to outweigh that.
6. **An atom that has a silluq is perfectly free to have a meteg as well.** The 354 members of
   `1/sopa-y/maq-n` are all of them, הָֽאֲדָמָֽה׃ and לַֽיהֹוָֽה׃ and their like; and in 38 of the 229
   members of `1/sopa-y/maq-y` the extra meteg is on the final atom, the one that has the silluq, rather than
   earlier in the compound. Whatever thins the verse end, it is not a bar on the atom itself.

## Why the fourteen members of `2/sopa-y/maq-y` do not disprove any of this

In every one of the 14, the final atom has exactly one U+05BD, its silluq, and both metegs sit on
an earlier atom of the compound. Twelve of the 14 distribute as 2+1, Psalms 81:9 אִם־תִּֽשְׁמַֽע־לִֽי׃
as 0+2+1 and Job 18:21 לֹֽא־יָדַֽע־אֵֽל׃ as 1+1+1. So the 14 are not cases of an atom that has a silluq
also having two metegs; they are cases of a compound spreading two metegs over the atoms that precede
the silluq. Read that way they say nothing about `2/sopa-y/maq-n` except that a compound has more
room, which is the same thing the maq-y column says everywhere else in the grid: the step-up rate
is 1.49% for mid-verse compounds against 0.255% for mid-verse lone atoms.

## What this file does not claim

1. **It does not claim Yeivin and Breuer are silent about ga'ya near a verse end in general.**
   Yeivin §332 and §357 are squarely about it. What neither book has is a rule that would govern
   how many ga'yot a verse-final chanted word may have.
2. **It does not claim the verse-final thinning of clause 5 is understood.** The effect is
   measured and is large; its cause is not established here, and a following-word condition and
   pausal vowel restoration are candidates rather than findings.
3. **It does not rest on any manuscript reading.** Every count is MAM's, and where Yeivin reports
   what A, L, C or S have, that is Yeivin reporting, not this file.
