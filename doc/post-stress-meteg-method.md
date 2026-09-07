# Post-stress-meteg survey method

This is maintainer documentation for the post-stress-meteg survey. The rendered
post-stress-meteg page explains the cantillation findings without this implementation detail.

## Fit for MAS

The fit-for-MAS table asks a narrow structural question about a pair of chanted words. A candidate
has a first chanted word with a nonfinal primary stress syllable and a candidate syllable
immediately after that stress. The table includes the pair only when the stress syllable has one
conjunctive accent and the next chanted word has initial stress and a disjunctive accent. The
candidate syllable must be type 1A, 1B, 2A, 2B, or 3. Another meteg in the first chanted word
does not disqualify the candidate.
The types are Yeivin's §332 open-syllable type, §354 guttural type, and §338 closed-tsere type,
with Breuer's corresponding Ch. 8 types (j), (b), and (a). Breuer's Ch. 14 §8 lists only the
types where the poetic system's rule differs from the prose system, and item (b) there is the
guttural type.

The table is a search limited to a regular configuration of neighbouring chanted words. Phonetic
MAM supplies the first chanted word's stress position, and the survey checks the conjunctive accent
on that stress syllable. The prose or poetic accent grammar establishes the next chanted
word's disjunctive accent. The U+05BD on ר in Genesis 28:7's next chanted word, אֲרָֽם׃, is
silluq, not an absence of an accent: the sof pasuq supplies the context that classifies it.

The non-type-specific conditions deliberately define a narrower table than the MAS census. A
grammar-aware audit found 217 next-word disjunctives and 15 next-word conjunctives among the 232
MAS records; all but Jeremiah 46:14 have initial stress in the next chanted word. The Fit-for-MAS
section accounts for every difference between the table's "Has MAS" count and the total MAS count.
In particular, ten chanted words have two distinct metegs: an MBS before the primary stress and a
MAS immediately after it. Each MBS and MAS census column counts meteg marks rather than chanted
words, so each of the ten chanted words contributes one count to each column. Another meteg in the
first chanted word does not exclude the candidate from the Fit-for-MAS table.

The common conditions are a search filter, not a shared source description. Yeivin §332 specifies
initial stress in the next chanted word for the open-syllable type. Yeivin §354 specifies a
next chanted word that begins with lamed or nun for the guttural type. Breuer's description
of the closed-tsere type includes a next chanted word accented initially or a long chanted
word that begins with a closed syllable. No source statement here makes a next-word disjunctive a
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

## Snapshot currency is not source-form alignment

The JSON's `currency` section measures the difference in U+05BD counts between Phonetic MAM's
snapshot and MAM-simple today, one numbered verse at a time. It does not align chanted words or
classify the U+05C0 glyph. Its purpose is to state the scope of the census while its stress oracle
is the older Phonetic MAM snapshot, not to preserve that snapshot as a permanent comparison
target. When Phonetic MAM is regenerated, `currency` is regenerated too; it is not evidence
against the template-aware source-form result above.

## Primary stress and accent parsing

Phonetic MAM's `jta` field gives the primary-stress position. The survey uses that field rather
than inferring primary stress from the number or placement of Unicode accent marks. The potential
chanted word's stress syllable must have one regular conjunctive accent, checked directly on the
stress letter. The prose or poetic accent grammar determines whether the next chanted word has a
disjunctive accent; a next chanted word without that token does not meet the Fit-for-MAS filter.

The census classifies a U+05BD that shares a stress letter with a stress-marking accent only when
their order is defined. A U+05BD sharing a letter with a fixed-edge accent is classified by its
syllable, because that accent does not identify the primary stress.
