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

## Primary stress and accent parsing

Phonetic MAM's `jta` field gives the primary-stress position. The survey uses that field rather
than inferring primary stress from the number or placement of Unicode accent marks. The prose and
poetic accent grammars still tokenize each word, and the JSON records their token-count
distribution as a diagnostic. Tokenization does not exclude a structural candidate.

Earlier code used Phonetic MAM's `jta` field to find stress, then classified the accent by raw
Unicode marks on the stress letter. That raw-mark step could not recognize fixed-edge accents or a
verse-final U+05BD as silluq. The table now retains the following-word conditions, but establishes
the accent condition through the accent grammar instead.
