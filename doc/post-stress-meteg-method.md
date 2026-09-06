# Post-stress-meteg survey method

This is maintainer documentation for the post-stress-meteg survey. The rendered
post-stress-meteg page explains the cantillation findings without this implementation detail.

## Fit for MAS

The fit-for-MAS table asks a broad structural question. For every word whose primary stress is
not final, the survey considers the following syllable. The survey places that syllable in each
of the three source-derived types it meets, then records whether MAM has a meteg on the syllable.
The types are Yeivin's §332 open-syllable type, §354 guttural type, and §338 closed-tsere type,
with Breuer's corresponding Ch. 8 types (j), (b), and (a).

The table is a search limited to a regular configuration of neighbouring words. A candidate has a
following word with initial stress and a disjunctive accent, as established by the prose or poetic
accent grammar. The U+05BD on ר in Genesis 28:7's following word, אֲרָֽם׃, is silluq, not an
absence of an accent: the sof pasuq supplies the context that classifies it.

The following-word conditions deliberately define a narrower table than the MAS census. A
grammar-aware audit on 2026-09-06 found 215 following disjunctives and 17 following conjunctives
among the 232 MAS records; all but Jeremiah 46:14 have initial stress in the following word. The
fit-for-MAS footnote accounts for every resulting difference between the table's "Has MAS" count
and the total MAS count, including the seven MAS cases that meet none of the three structural
types.

The three source descriptions also do not supply one shared following-word condition. Yeivin §332
specifies initial stress in the following word for the open-syllable type. Yeivin §354 specifies a
following word that begins with lamed or nun for the guttural type. Breuer's description of the
closed-tsere type includes a following word accented initially or a long word that begins with a
closed syllable. No source statement here makes a following disjunctive a condition for all three
types.

## Phonetic MAM source-form alignment

The Fit-for-MAS records use Phonetic MAM for primary stress and MAM today for reader-facing forms.
Those are not interchangeable inputs. On 2026-09-06, the 3,181 Fit-for-MAS records' first and
following chanted words were compared directly with MAM-parsed-plus: 6,362 pairs in all. This was
a template-aware comparison, not a comparison against MAM-simple's flattened stream.

The selected MAM-parsed-plus form has the following explicit choices.

1. A `מ:כפול` template selects parameter `א`, the cant-alef (taxton) branch. The combined form
   and parameter `ב` describe different cantillation choices.
2. A `מ:דחי` or `מ:צינור` template selects parameter `2`, the stress-helped form. Parameter `1`
   would omit the repeated deḥi or tsinnor that Phonetic MAM has.
3. A standard ketiv/qere template selects its qere argument; a trivial ketiv/qere template selects
   its first argument; and the same implicit-qere helper used for Phonetic MAM is then applied.
4. The comparison removes Phonetic MAM's upper dot and rafe, which the reader-facing MAM-form
   projection also removes. A shared varika stays in the form.

Under that policy, 6,308 pairs are identical and 16 more agree with the shared varika retained.
The remaining 38 pairs are not text differences. Each has `מ:לגרמיה-2` immediately after the
matching MAM chanted word, and each Fit-for-MAS record has the following chanted word's
disjunctive accent. MAM-simple represents the U+05C0 glyph in a separate stream position, while
the MAM-parsed-plus template records the legarmeh analysis. Four of the 38 numbered verses also
have a `מ:פסק` template elsewhere; that template does not describe the candidate chanted word.
After those semantic agreements, no form pair remains unaccounted for.

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
than inferring primary stress from the number or placement of Unicode accent marks. The prose and
poetic accent grammars still tokenize each word, and the JSON records their token-count
distribution as a diagnostic. Tokenization does not exclude a structural candidate.

Earlier code used Phonetic MAM's `jta` field to find stress, then classified the accent by raw
Unicode marks on the stress letter. That raw-mark step could not recognize fixed-edge accents or a
verse-final U+05BD as silluq. The table now retains the following-word conditions, but establishes
the accent condition through the accent grammar instead.
