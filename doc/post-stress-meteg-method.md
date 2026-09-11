# Post-stress-meteg survey method

This is maintainer documentation for the post-stress-meteg survey. The rendered
post-stress-meteg page explains the cantillation findings without this implementation detail.

## Fit for MAS

The fit-for-MAS table asks a narrow structural question about a pair of chanted words. A candidate
has a first chanted word with a penultimate primary stress syllable and a candidate syllable
immediately after that stress. The table includes the pair only when the stress syllable has one
conjunctive accent and the next chanted word has initial stress and a disjunctive accent. The
candidate syllable must be type 1A, 1B, 2Af, 2Bf, or 3. Types 2Af and 2Bf are the
Fit-for-MAS versions of the general type-2 subtypes 2A and 2B; both additionally require
that the next chanted word not begin with vocal shewa. The Fit-for-MAS implementation requires
a closed, final, tsere-voweled syllable for type 3; its common criteria require penultimate
stress with a conjunctive accent. Another meteg in the first chanted word does not disqualify
the candidate.
The types are Yeivin's §332 open-syllable type, §354 guttural type, and §338 closed-tsere type,
with Breuer's corresponding Ch. 8 types (j), (b), and (a). Breuer's Ch. 14 §8 lists only the
types where the poetic system's rule differs from the prose system, and item (b) there is the
guttural type.

The table is a search limited to a regular configuration of neighbouring chanted words. Phonetic
MAM supplies the first chanted word's stress position, and the survey checks the conjunctive accent
on that stress syllable. The prose or poetic accent grammar establishes the next
chanted word's disjunctive accent. The U+05BD on ר in Genesis 28:7's next chanted word, אֲרָֽם׃, is
silluq, not an absence of an accent: the sof pasuq supplies the context that classifies it.

The non-type-specific conditions deliberately define a narrower table than the MAS census. A
grammar-aware audit found 217 next-chanted-word disjunctives and 15 next-chanted-word conjunctives
among the 232 MAS records; all but Jeremiah 46:14 have initial stress in the next chanted word. The Fit-for-MAS
section accounts for every difference between the table's "Has MAS" count and the total MAS count.
In particular, ten chanted words have two distinct metegs: an MBS before the primary stress and a
MAS immediately after it. The MBS_O census category counts chanted words with one or more MBS
marks and no MAS, while the MAS category counts chanted words with a MAS regardless of whether a
chanted word also has an MBS. The ten chanted words therefore appear only in the MAS census category.

The common conditions are a search filter, not a shared source description. Yeivin §332 specifies
initial stress in the next chanted word for the open-syllable type. Yeivin §354 specifies a
next chanted word that begins with lamed or nun for the guttural type. Breuer's description
of the closed-tsere type includes a next chanted word accented initially or a long chanted word that begins
with a closed syllable. No source statement here makes a next-chanted-word disjunctive a
condition for all three types.

## Phonetic MAM source-form alignment

The Fit-for-MAS records use Phonetic MAM for primary stress and MAM today for reader-facing forms.
Those are not interchangeable inputs. Each displayed MAM form is found from its Phonetic-MAM
counterpart by a template-aware comparison, not by matching MAM-simple's flattened stream alone.

The selected MAM-parsed-plus form has the following explicit choices.

1. A `מ:כפול` template selects parameter `א`, the cant-alef (taxton) branch. The combined form
   and parameter `ב` describe different cantillation choices.
2. A `מ:דחי` or `מ:צינור` template selects parameter `2`, the stress-helped form. Parameter `1`
   would omit the repeated deḥi or tsinnor that Phonetic MAM has.
3. A standard ketiv/qere template selects its qere argument; a trivial ketiv/qere template selects
   its first argument; and the same implicit-qere helper used for Phonetic MAM is then applied.
4. The comparison removes Phonetic MAM's upper dot and rafe, which the reader-facing MAM-form
   projection also removes. A shared varika stays in the form.

When a matching MAM chanted word is followed by a `מ:לגרמיה-2` template, the two inputs agree
semantically rather than textually: MAM-simple represents U+05C0 in a separate stream position,
while the MAM-parsed-plus template records the legarmeh analysis. A `מ:פסק` template elsewhere in
the numbered verse does not describe the candidate chanted word.

MAM-simple remains appropriate where this survey needs its current reader-facing forms or a
per-numbered-verse U+05BD count. MAM-parsed-plus is the input where the question depends on a
template's selected argument or on the legarmeh-versus-narrow-sense-paseq analysis. This result
does not support a blanket migration from MAM-simple to MAM-parsed-plus.

## Qamats-variant rows and MAM chanted words

A `מ:קמץ` row in Phonetic MAM contains a qamats-dal reading and a qamats-sam reading. The
source-entry count includes both readings, but the MAM census selects the qamats-dal reading once.
In template terms, the census takes parameter `ד` and does not also take parameter `ס`. Ben's
decision, 2026-09-08: selecting exactly one of `ד` or `ס` is the required treatment; which one is
selected need not receive a separate effect analysis. The present choice of `ד` is acceptable,
analogous to the survey's selection of cant-alef for a dual-cantillation template.
The 2026-09-08 survey found 309 such rows in prose verses and 61 in poetic verses. Those 370
rows contribute 372 duplicate phonetic-reading entries because Psalms 35:10 and Proverbs 19:7
each form one chanted word in the qamats-dal reading and two chanted words in the qamats-sam
reading.

The fatal invariants connect all three quantities per verse system: source entries equal MAM
chanted words plus duplicate phonetic-reading entries, and duplicate entries equal variant rows
plus the two measured grouping differences. The resulting MAM denominators are 233,277 prose
chanted words and 29,542 poetic chanted words. The corresponding MBS_O chanted-word counts are
12,842 and 1,786; MAS counts are 178 and 54; and silluq counts are 18,738 and 4,465. The
positional census separately counts 12,955 and 1,805 individual pre-stress marks. The two prose
figures were 12,849 and 12,962 until 2026-09-11; "Eleven meteg edits reached the survey on
2026-09-11" below says why.

## A census chanted word is identified by position, not by form

The census counts chanted words, and one numbered verse can hold the same form twice. So a
chanted word is identified by its numbered verse and by its position among that verse's parsed
entries. Keying it by form instead — the numbered verse, the chanted word and its `jta` — makes
each such pair read as a single chanted word carrying both occurrences' meteg marks.

The census was keyed by form until 2026-09-09, and reported 12,828 prose MBS_O chanted words
and 143 MBS_O chanted words with more than one meteg. Twenty-one of those 143 were one form
counted against itself, each occurrence carrying one meteg, so the MBS_O counts were 21 short
of the chanted words they are described as counting and the multiple-meteg count was 21 too
many. All 21 are in prose verses. The corrected figures were 12,849 prose MBS_O chanted words
and 122 with more than one meteg. (The 12,849 has been 12,842 since 2026-09-11, for a reason
that has nothing to do with the key: "Eleven meteg edits reached the survey on 2026-09-11"
below.) The poetic MBS_O count, both MAS counts and every positional
count are unaffected: no MAS chanted word shares a numbered verse with another chanted word of
the same form.

The independent oracle is `py/foi/foiz_wt_mtgmtg.py`, which counts U+05BD per chanted word
straight from MAM-parsed-plus with no stress oracle at all. Its tracked output
`gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` has 135 chanted words carrying two meteg marks
beside any verse-final silluq: the groups `2/sopa-n/maq-n` 19, `2/sopa-n/maq-y` 102 and
`2/sopa-y/maq-y` 14. Those 135 reconcile against the census as the 122 MBS_O chanted words, the
ten MAS chanted words that also carry one meteg before the stress, and three cant-bet Decalogue
forms — לֹֽא־יִהְיֶֽה־לְךָ֩ at Exodus 20:2 and לֹֽא־תַעֲשֶֽׂה־לְךָ֣ at Exodus 20:3 and Deuteronomy 5:7 — which the
features-of-interest survey counts because its `מ:כפול` handler concatenates both cantillation
strands where the census counts cant-alef alone.

## Snapshot currency is not source-form alignment

The JSON's `currency` section measures the difference in U+05BD counts between Phonetic MAM's
snapshot and MAM-simple today, one numbered verse at a time. It does not align chanted words or
classify the U+05C0 glyph. Its purpose is to state the scope of the census while its stress oracle
is the older Phonetic MAM snapshot, not to preserve that snapshot as a permanent comparison
target. The 2026-09-08 measurement compares 23,184 numbered verses and finds nine differences,
all cases where MAM-simple has one more U+05BD than the snapshot. When Phonetic MAM is regenerated,
`currency` is regenerated too; it is not evidence against the template-aware source-form result
above.

## Eleven meteg edits reached the survey on 2026-09-11

The tracked survey had last been regenerated on 2026-09-09, in `ad44dba7`. Regenerated on
2026-09-11, it found both of its inputs moved. The Wikisource refresh of 2026-09-10, MAM-basics
`209b4c05`, brought into `in/mam-ws/` and MAM-simple the eleven meteg edits made on Hebrew
Wikisource on 2026-08-30 and 2026-08-31, which `doc/PLAN-holman-meteg-rollout-programme.md`
recorded on 2026-09-03 as not yet downloaded. That evening, MAM-private `65ee486` brought the
same eleven into the Phonetic MAM snapshot the survey reads. All eleven are in prose verses,
and each changes one chanted word by one meteg and nothing else. Nine removed the chanted
word's one meteg before the stress, and two added one:

| Verse | Before the edit | After the edit |
| --- | --- | --- |
| Joshua 19:8 | בְנֵֽי־שִׁמְע֖וֹן | בְנֵי־שִׁמְע֖וֹן |
| 1 Samuel 1:6 | כִּֽי־סָגַ֥ר | כִּי־סָגַ֥ר |
| 1 Samuel 22:22 | כִּֽי־שָׁם֙ | כִּי־שָׁם֙ |
| 2 Kings 6:23 | אֶל־אֲדֹֽנֵיהֶ֑ם | אֶל־אֲדֹנֵיהֶ֑ם |
| Isaiah 22:5 | לַֽאדֹנָ֧י | לַאדֹנָ֧י |
| Isaiah 24:18 | וְ֠הָיָ֠ה | וְֽ֠הָיָ֠ה |
| Isaiah 42:24 | מִֽי־נָתַ֨ן | מִי־נָתַ֨ן |
| Isaiah 50:7 | יַֽעֲזׇר־לִ֔י | יַעֲזׇר־לִ֔י |
| Zephaniah 3:13 | וְלֹֽא־יִמָּצֵ֥א | וְלֹא־יִמָּצֵ֥א |
| 2 Chronicles 26:15 | כִּֽי־חָזָֽק׃ | כִּי־חָזָֽק׃ |
| 2 Chronicles 28:19 | מֶלֶךְ־יִשְׂרָאֵ֑ל | מֶֽלֶךְ־יִשְׂרָאֵ֑ל |

At 2 Chronicles 26:15 the chanted word still has its silluq. The eleven account for every survey
figure that moved except the two in item 6:

1. Prose metegs before the stressed syllable went from 12,962 to 12,955: nine fewer and two
   more. The dual-cantillation section's whole-census counts, which total both verse systems
   for each strand, moved by the same seven, from 14,767 to 14,760 for cant-alef and from
   14,768 to 14,761 for cant-bet.
2. Prose MBS_O chanted words went from 12,849 to 12,842. None of the eleven chanted words has a
   meteg after the stress, so the nine left MBS_O and the two joined it.
3. Prose metegs sharing a letter with a non-stress-marking accent went from 27 to 28, and the
   JSON's diagnostics list of them gained Isaiah 24:18's record. The meteg added there is on
   the vav that has the telisha gedolah, whose place on the first letter does not mark the
   stress. As "Primary stress and accent parsing" below says, such a meteg is classified by its
   syllable, so it is counted among the metegs before the stress as well as here.
4. The comparison with the 2026-09-03 census moved with items 1 and 3. The prose difference in
   metegs before the stressed syllable went from −169 to −176, and a prose row for metegs
   sharing a letter, 27 in the census against 28 measured, appeared, since the comparison lists
   only the categories that differ.
5. `currency` went from 38,161 U+05BD in the snapshot against 38,170 in MAM-simple to 38,154
   against 38,163. Both texts have the same eleven edits, so the same nine numbered verses
   differ.
6. Two fit-for-MAS figures moved because of an edit in a poetic verse that is not a meteg edit.
   At Psalms 4:3, MAM's לִ֭כְלִמָּה now stands in a `מ:דחי` template whose stress-helped form,
   לִ֭כְלִמָּ֭ה, has the deḥi's stress helper on the last syllable (issue #266). Phonetic MAM has
   the stress-helped form, as "Phonetic MAM source-form alignment" above says, and its `jta`
   now has the chanted word's stress on that last syllable rather than on its first. No
   syllable follows the stress, so the chanted word is no longer a fit-for-MAS candidate:
   `candidate_chanted_words` went from 53,964 to 53,963, and the one-token row of
   `accent_grammar_token_counts` from 53,157 to 53,156. MAM-simple has the template's other
   form, לִ֭כְלִמָּה, and did not change there.

Re-establish these with `py/main_accgram.py survey-post-stress-meteg` and the diff of
`out/accgram/post-stress-meteg.json` against `ad44dba7`. The main page's MBS_O cells moved with
item 2, and `pin_claims` in `py/author_site/post_stress_meteg.py` states 12,842.

## Primary stress and accent parsing

Phonetic MAM's `jta` field gives the primary-stress position. The survey uses that field rather
than inferring primary stress from the number or placement of Unicode accent marks. The potential
chanted word's stress syllable must have one regular conjunctive accent, checked directly on the
stress letter. The prose or poetic accent grammar determines whether the next chanted word has a
disjunctive accent; a next chanted word without that token does not meet the Fit-for-MAS filter.

The census classifies a U+05BD that shares a stress letter with a stress-marking accent only when
their order is defined. A U+05BD sharing a letter with a fixed-edge accent is classified by its
syllable, because that accent does not identify the primary stress.
