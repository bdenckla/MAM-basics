# Post-stress-meteg survey method

This is maintainer documentation for the post-stress-meteg survey. The rendered
post-stress-meteg page explains the cantillation findings without this implementation detail.

## Fit for MAS

The fit-for-MAS table asks a broad structural question. For every word whose primary stress is
not final, the survey considers the following syllable. The survey places that syllable in each
of the three source-derived types it meets, then records whether MAM has a meteg on the syllable.
The types are Yeivin's §332 open-syllable type, §354 guttural type, and §338 closed-tsere type,
with Breuer's corresponding Ch. 8 types (j), (b), and (a).

The table is not a search limited to the regular configuration of a pair of neighbouring words.
The page's general facts are observations about MAM's MAS cases, not universal preconditions for
the structural table. In particular, the word after a MAS has initial stress in every case except
Jeremiah 46:14. The survey does not currently screen the table by the following word's accent.

The earlier raw-mark check could not determine whether the following accent was disjunctive: it
treated U+05BD as neither accent nor silluq. Genesis 28:7 shows the error plainly: the following
word, אֲרָֽם׃, has its primary stress on ר, and the U+05BD there is the verse-final silluq.
A grammar-aware audit on 2026-09-06 found 215 following disjunctives and 17 following
conjunctives among the 232 MAS records. The 17 conjunctives are six munax, five mahapakh, three
merkha, one azla, one merkha kefula, and one telisha qetana. A following disjunctive is therefore
not a general fact about MAS and cannot be a screen for the whole structural table.

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

Earlier code did exclude candidates unless a raw stress-letter test reported a conjunctive on the
MAS word, an initially stressed following word, and a disjunctive on the following word. That
screen combined observations and type-specific conditions into one rule. It also could not
recognize U+05BD as a verse-final silluq on the stress letter, and so could falsely report that
the word had no accent. The structural survey replaced that screen so that the table can count
both MAS and non-MAS instances of each type.
