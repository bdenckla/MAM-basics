# CLC changes and UXLC caveats

State: live. Reframed by Ben's decision of 2026-10-28 to abandon any goal of changing the UXLC.
Section 4's finding was sent to Chris Kimball, the UXLC's editor, on 2026-10-19, in Ben's report
"Errors in BHL claims in UXLC change-record notes"; nothing else here has been sent to the UXLC.

Ben, 2026-10-28:

> ditch all notion/hope of corrections to UXLC. reframe the issues of this word (and reframe the
> whole file) in terms of what changes should be made to CLC. as for things not part of CLC that
> are part of the broader tanach.us site, like I think change proposals would fall in this
> category, e.g. false assertions about BHLA and/or BHLB, keep those but frame those as sort of
> "caveats with which UXLC should be read with". This fits in with the general theme of abandoning
> any goal of changing UXLC.

Each section is therefore one of two kinds:

1. A **CLC change**, a change CLC should make to the text it takes from the UXLC, or has made:
   sections 8, 11 and 12.
2. A **caveat**, tanach.us material outside the UXLC's text, such as a change record, change list
   or note page, that a reader of the UXLC should not take at face value: sections 1 to 7, 9
   and 10.

The file began on 2026-10-15 as "Potential UXLC corrections", a record of problems Ben had
decided not to report ("I don't care about mistakes in UXLC any more"), kept in case he ever
wanted to. On 2026-10-20 he limited it to corrections the UXLC's editor might want. The reframing
of 2026-10-28 replaces both purposes.

MAM-basics' archive of the UXLC's change records, `in/UXLC-misc/all_changes.json`, lists Ben as
the author of every record in changeset 2026.02.05, "Corrections from Ben Denckla's list of
contended words in Job." The corrections are Chris Kimball's. Ben, 2026-10-28: "the corrections
inspired by my list are Kimball's; by and large, my list is just a list, though I may in my
review, offer an opinion, these change records more likely reflect Kimball's opinion, not mine".
This file therefore calls them Kimball's.

On 2026-10-19 a Claude session rechecked every record then in this file against its change list as
tanach.us then served it. Five of the six lists matched MAM-basics' archived copies record for
record. The sixth, the 2026.10.19 list, had changed, and sections 2 and 3 say how.

A change record's **locator** is its page, column and line, written here as page, then
column:line, such as F063A 2:20. The UXLC's locators count only lines that hold text, so a
citation below blank lines has a line number lower, by the number of blank lines above it, than a
count of every ruled line gives.
Before relying on any locator below, count every ruled line from the column's top on the page
image, and allow for that convention.

## 1. Three locators that disagree with the page images, found 2026-10-14

A comparison of UXLC change records with Charles Loder's leningrad-codex-tei v0.5.0, then a TEI
encoding of pages F001B–F091B, found three records whose locators disagree with the TEI and with a
Claude session's reading of Sefaria's photographs: 2021.02.22-15 (Lev 13:3.12, page F063A),
2021.12.28-2 (Lev 26:35.3, F073A) and 2022.04.04-6 (Num 9:17.6, F080B). On 2026-10-31 a Claude
session reread all three on the photographs, and MAM-basics corrected them in its override copies.
Section 9 points to the manifest that gives each corrected value and its evidence, including, for
2021.12.28-2, the UXLC's own earlier record that agrees with the correction.

Caveat: a change record's locator can be off by a line or two, as these three are; check it on the
page image before relying on it.

## 2. A pending UXLC 2.6 record that cited the wrong position, found 2026-10-14

Daniel Holman's record 2026.08.05-10, in the proposed UXLC 2.6 change list with file date
2026.10.19, cited Lev 25:20.3 for "Remove mahapakh under the kaf. Remove note 'c'." Its reference
text is at position 4 of the verse; position 3 holds the other atom of that maqaf compound. The
installed list, as tanach.us served it on 2026-10-19, cites Lev 25:20.4, so the UXLC has fixed the
position. The record still leaves its column and line empty. MAM-basics' override copy gives
F071B 2:16, the line that Ben's record 2020.12.22-2, the TEI and a reading of the photograph all
give; section 9 points to the manifest that records it.

Caveat: record 2026.08.05-10 gives no column or line, and the proposed list cited the wrong atom
for it.

## 3. Defects in the proposed UXLC 2.6 change list, noted 2026-08-12

UXLC-utils commit
[3435fc81](https://github.com/bdenckla/UXLC-utils/commit/3435fc8130642528cfc8a134a645bf4dc7af1141)
recorded these in the copy of `2026.10.19 - Changes.xml` taken from hcanat.us on 2026-08-12. On
2026-10-20 `uxlc/in/UXLC-misc/2026.10.19 - Changes.xml` became the installed list, with 140
records, as hcanat.us served it that day, byte for byte the copy that tanach.us served on
2026-10-19. The UXLC had fixed items 1 and 3 there, but not item 2.

1. 2026.08.05-27 (Job 11:6.3) gave its book as `job`, lowercase. The installed list gives `Job`.
2. 2026.08.05-5 (Ex 20:3.2), 2026.08.05-10 (Lev 25:20.3) and 2026.08.05-25 (Job 34:20.4) give a
   page but an empty column and line, and so does 2026.08.05-47 (Ps 14:7.1), which the proposed
   list lacked. MAM-basics rejects an empty line, so its override copy fills the four, which held
   the location estimator's values until 2026-10-31 and since then hold readings of Sefaria's
   photographs. Section 9 points to the manifest that records them.
3. 2026.08.05-19 (2 Sam 5:21.1), Daniel Holman's, described removing a maqaf, but its change text
   was the same as its reference text, maqaf included. In the installed list its change text lacks
   the maqaf, so the record proposes the removal that its description names.

Caveat: four records of the installed UXLC 2.6 list give a page but no column or line; MAM-basics'
override copy fills them with readings of Sefaria's photographs.

## 4. Wrong letter name in a change-record note, found 2026-10-17

Daniel Holman's record `UXLC2022.08.29#20` (also written 2022.08.29-20), released in 2022.12.07,
cites 1 Sam 18:28.11. Its note
says "patah under the ayin" where it should say "patah under the aleph". Caveat: the note names the
wrong letter; it means the alef. The record's vowel change and its Approved status are unaffected.
The note's exact wording is retained below.

<details>
<summary>Exact UXLC note</summary>

> Ben Denckla: BHL has a hataf-patah under the aleph; BHL Appendix A finds a patah under the ayin in the LC but notes the difficulty reading the LC.

</details>

Source: [archived UXLC change records](../in/UXLC-misc/all_changes.json), record `/404`, note `/404/notes/0` (changeset
`2022.08.29`, number `20`; release `2022.12.07`; manuscript locator `Folio_161A 1:23`).

Ben reported this correction to Chris Kimball on 2026-10-19, in his report "Errors in BHL claims
in UXLC change-record notes", sent as an HTML file and a PDF. The report lists this record under
"Other errors about BHLA" and suggests replacing the passage with "BHL Appendix A finds a patah
under the aleph in the LC but notes the difficulty reading the LC." MAM-basics tracks the HTML
sent, less its ten BHLA scan crops, as
[uxlc/doc/uxlc-bhl-claim-errors-2026-10-19.html](../uxlc/doc/uxlc-bhl-claim-errors-2026-10-19.html),
and gives each of the report's findings, and each crop's recipe, as data in
[uxlc/doc/uxlc-bhl-claim-errors-2026-10-19.json](../uxlc/doc/uxlc-bhl-claim-errors-2026-10-19.json).
The report's working files are untracked, under `.novc/uxlc-bhl-claims/` in the primary forest's
MAM-basics clone, with the two files sent in its `sent-2026-10-19/`.

## 5. Wrong letter name in a change-record note at Proverbs 12:10, found 2026-10-19

Daniel Holman's record `UXLC2023.06.09#10` (also written 2023.06.09-10), released in 2023.10.19,
cites Prov 12:10.7. Its first note says "The mark below the qof" where it should say "The mark
below the resh": the word has no qof, and the record's description names the resh. Caveat: the
note names the wrong letter; it means the resh. The record's change and its Approved status are
unaffected. The note's exact wording is retained below. The record's second note is in Ben's
report of 2026-10-19 (section 4) for a different error: it says that BHLA has no entry for this
verse, and the report finds that BHLA has an entry for this word.

<details>
<summary>Exact UXLC note</summary>

> The mark below the qof has the northeast-to-southwest inclination of a merkha. Since this word occurs at the end of the verse, the mark should be a meteg acting as a siluq; a merkha is inappropriate here. Adding note 't'.

</details>

Source: [archived UXLC change records](../in/UXLC-misc/all_changes.json), record `/818`, note `/818/notes/0` (changeset
`2023.06.09`, number `10`; release `2023.10.19`; manuscript locator `Folio_413B 2:10`).

CLC's Proverbs page shows this note as tanach.us has it (`uxlc/doc/clc-design.md` §7.3); CLC has
no way yet to mark an error in a note it shows.

## 6. Change texts that UXLC 2.6 did not install, found 2026-10-20

Probably the UXLC's practice. A check on 2026-10-31 found nine
records of the two types that change no text, NoTextChange and NoAction, whose change text is a
reading that the UXLC did not adopt: the two below; 2020.07.31-2 (Lam 3:33.6) and 2022.07.02-10
(Ex 5:22.11); and 2024.04.12-14 (Ezek 43:15.4), 2024.04.12-36, -37 and -39 (Deut 22:25.7, 22:26.2
and 22:27.6) and 2024.07.01-2 (Dan 5:10.19). They date from 2020 to 2026, and the five of 2024 are
by CVK, the UXLC's editor.

Two of Daniel Holman's records in the installed UXLC 2.6 list are typed NoTextChange, and each
record's first note says the change it examines will not be made. UXLC 2.6's text has only the
note each record adds, but each record's change text has the change:

1. 2026.08.05-81 (Ps 105:40.1) examines a possible maqaf. Its note says that the putative maqaf
   "will not be added", but its change text, שָׁאַ֣ל־, ends in a maqaf that its reference text,
   שָׁאַ֣ל, lacks. UXLC 2.6 adds a "t" note to the atom.
2. 2026.08.05-128 (Ezra 8:18.15) examines the meteg under the resh as a possible merkha. Its note
   says that the mark lacks the inclination "to be transcribed as a merkha", but its change text,
   וְשֵׁרֵ֥בְיָ֛ה, has a merkha under the resh where its reference text, וְשֵׁרֵֽבְיָ֛ה, has a meteg. UXLC 2.6
   adds an "m" note to the atom.

These change texts misled MAM-basics until 2026-10-31. `py/main_find_uxlc_accent_changes.py`
decided from a record's reference and change texts alone, so `in/accgram/uxlc_accent_changes.json`
listed three of the nine records, 2022.07.02-10, 2026.08.05-81 and 2026.08.05-128, as accent
changes that the UXLC never made, and `out/accgram/uxlc_grammar_test.txt` counted the two of them
in prose verses, Ex 5:22 and Ezra 8:18. Since then the finder dispatches on the record's type
first, and a record of either type is never an accent change.

Caveat: these nine records' change texts are not UXLC 2.6's text; read the installed text, not the
change text.

## 7. Duplicate records in the installed UXLC 2.6 list, found 2026-10-20

Two pairs of records in the installed UXLC 2.6 list make the same change at the same atom, with the
same reference text, change text and locator. Unlike 2026.08.05-16, whose note says that it
"follows on Ben Denckla's change of 2026.04.10 - 7", neither later record mentions the earlier
one.

1. Jer 10:3.11, F251A 3:11: 2026.04.10-8 and 2026.08.05-97, both Daniel Holman's, change
   יְדֵ֥י־ to יְדֵֽי־, with a meteg rather than a merkha under the dalet. 2026.04.10-8 also
   adds an "m" note, which UXLC 2.6 has; 2026.08.05-97 adds none.
2. Jer 46:4.6, F271B 1:5: 2026.04.10-9, which the UXLC's editor wrote from Ben's emailed
   suggestion, and 2026.08.05-100, Daniel Holman's, change
   בְּכ֥וֹבָעִ֑ים to בְּכֽוֹבָעִ֑ים, with a meteg rather than a merkha under the kaf. 2026.08.05-100
   carries the aBHL tag, and its tanach.us page says that the UXLC agrees with the BHL body
   text. 2026.04.10-9 carries neither BHL tag, so its page says "The UXLC does not agree with
   either BHL text", though its note says that BHL has a meteg under the kaf.

Caveat: each pair records one change twice, and 2026.04.10-9's page says the UXLC agrees with
neither BHL text although its note says BHL has the meteg.

## 8. A ZWJ between two marks in three atoms of Job, found 2026-10-27

Three atoms in Job have a zero-width joiner (ZWJ) between two marks. In Job 32:6 and 10:15 the
joiner keeps an accent before a ḥiriq, an order that normalization would otherwise change, so the
Unicode Standard calls for a combining grapheme joiner (CGJ) there. In Job 19:16 the joiner is
between a revia and a geresh muqdam, whose order normalization never changes, so that atom needs
no joiner. Ben, 2026-10-27, of Job 32:6: "The editor of UXLC doesn't understand the difference
between ZWJ and CGJ, or at least, confused them in this case."

| Citation | Atom | Locator | Marks in the UXLC's order | Record that added the ZWJ | Release |
| --- | --- | --- | --- | --- | --- |
| Job 32:6.11 | יְשִׁישׁ֑‍ִים | F406A 1:20 | shin dot, atnaḥ, ZWJ, ḥiriq, on the second shin | Daniel Holman's 2023.06.10-39 | 2023.10.19 |
| Job 10:15.12 | עָנְי֥‍ִי׃ | F400A 1:14 | merkha, ZWJ, ḥiriq, on the first yod | Kimball's 2026.02.05-35 | 2026.04.01 |
| Job 19:16.6 | פִ֗‍֝י | F402B 1:9 | ḥiriq, revia, ZWJ, geresh muqdam, on the pe | Kimball's 2026.02.05-65 | 2026.04.01 |

Both joiners have combining class 0, so the text survives normalization either way; the
difference is meaning. The Unicode Standard 18.0 (section 23.2.4) gives the CGJ the job of
keeping canonically equivalent mark orders distinct, with a Hebrew example (lamed,
pataḥ, CGJ, ḥiriq), and warns against confusing it with the ZWJ, which (section 23.2.2)
requests a more connected rendering, such as a ligature. Its Hebrew section (9.1, "Meteg")
uses the CGJ to keep a meteg-vowel order under normalization and the ZWJ only to request a
meteg in the middle of a ḥataf vowel. A revia and a geresh muqdam have the same combining
class, 230, so either order of the two survives normalization without a joiner.

UXLC 2.6's text (MAM-basics `in/UXLC-39/`) has 1,141 CGJs, 264 of them directly between an
accent and a vowel, as in the atom בִנְיָמ֑͏ִן at Num 7:60. It has 83 ZWJs: 80 between a ḥataf
vowel and a meteg, the medial-meteg request, and these three. It has no ZWNJ.

The one record that states a reason gives the display: 2026.02.05-65 says the ZWJ is there
"to achieve the ordering in the display". 2026.02.05-35 replaced Job 10:15's existing CGJ
(silluq, CGJ, ḥiriq) with a ZWJ when it changed the silluq to a merkha, and Kimball's
2026.02.05-115 re-examined the order at Job 32:6 and kept the ZWJ. The ZWJ gives that display
only by breaking mark positioning: with HarfBuzz, the shaping engine Chrome and Firefox use,
Taamey D leaves the mark after each ZWJ unpositioned, at its letter's edge. With a CGJ,
Taamey D positions Job 32:6's ḥiriq under the shin, left of the atnaḥ.

CLC change, when CLC covers Job: in Job 32:6 and 10:15, replace the ZWJ with a CGJ; in Job 19:16,
remove it.

## 9. Locators corrected in override copies, 2026-10-31

A comparison of the UXLC change records with Charles Loder's leningrad-codex-tei found nine records
whose locators disagree with Sefaria's photographs, on a Claude session's reading of crops of them.
Ben decided on 2026-10-31 to "record them (i.e. record fixes to them) in uxlc/in/UXLC-misc-fixed",
with only a pointer here. Later that day, asked whether the same should be done for section 1's
three and for the estimate that section 2 finds two lines off, he answered "Yes, fix them". Asked
then to accept five recommendations, among them the manifest and test below, he answered "Accept
all five".

The folder holds MAM-basics' override copies of the change lists, which
`py/uxlc_changes/uxlc_misc_path.py` reads in place of the copies in `uxlc/in/UXLC-misc/`. Its
`corrections.json` lists every value in which a copy differs from its original: the list, the
record, the field, the UXLC's value, MAM-basics' value, whether that value is a reading of
Sefaria's photograph or the location estimator's estimate, and a summary of the evidence.
`py/tests/test_uxlc_misc_fixed.py` checks that each copy differs from its original exactly as
`corrections.json` says. When the UXLC adopts a correction and its list is downloaded again, the
original holds MAM-basics' value and the test fails on that entry, which is then retired; a copy
that no longer holds any correction is deleted.

The copies and `corrections.json` count a column's lines as the UXLC's locators do, only those that
hold writing: NIB, not including blank lines. MAM-basics elsewhere counts IB, including blank
lines, and `corrections.json` gives each corrected line IB as well. The two counts differ for one
record, 2023.11.10-3, whose atom is on line 12/11 IB/NIB of page F109B's column 3.

On 2026-10-31 the copies held the locators of sixteen records: twelve whose line the photographs
show to be wrong, and the four of section 3 whose column and line the UXLC leaves empty. All
sixteen are readings of the photographs. The last three of the four to be read, 2026.08.05-5, -25
and -47, replaced the location estimator's values that day: the readings confirm the first two and
put 2026.08.05-47 one line higher, at F367B 2:21.

## 10. Two problems recorded in a program's docstring, 2026-09-04

The docstring of `py/main_map_changes_to_book_of_job.py`, under "FOUR PROBLEMS NOTICED IN REVIEW AND
NOT RESOLVED", records problems in changeset 2026.02.05 of the 2026.04.01 list, Chris Kimball's port
of Ben's book-of-job work into the UXLC. They moved there on 2026-09-04, in `d8a63afd`, from a
report that was then deleted. Of the four it lists, 2026.02.05-115 is in section 8, and
2026.02.05-109 was withdrawn on 2026-10-31, as the end of this section says. The docstring remains
the fuller record of the other two.

1. 2026.02.05-83 (Job 23:5.6, NoAction) examines the end of the word for a maqaf. The docstring
   says that it discusses a different maqaf than intended, and that the question is an Aleppo
   Codex quirk, not relevant to the UXLC.
2. 2026.02.05-161 (Job 42:10.10, NoAction): the docstring says that the record's image link on
   tanach.us is broken. The record itself holds no image, so the link belongs to the UXLC's web
   pages. This was not rechecked on 2026-10-31.

The docstring listed 2026.02.05-109 (Job 31:15.1, NoTextChange) as misusing a ZWJ against the
Unicode Standard. It does not. Its he has ḥataf pataḥ, ZWJ, meteg, which the Unicode Standard
18.0, section 9.1, under "Meteg", gives as its example of a medially positioned meteg; UXLC 2.6
has 80 such joiners, as section 8 says. Its reference and change texts are the same, as a
NoTextChange record's normally are. On 2026-10-31, at Ben's request, the docstring was corrected
to say so.

## 11. Three letters whose marks are stored out of order, found 2026-10-28

| Citation | Atom | Letter | Marks as stored | CLC change |
| --- | --- | --- | --- | --- |
| Job 36:29.7 | סֻכָּֽתֽוֹ׃ | kaf | meteg, dagesh, qamats, in UXLC 2.6 | when CLC covers Job: no meteg; if one is kept, dagesh, qamats, meteg |
| Ex 32:19.17 | וַיְּשַׁבֵּ֥ר | yod | sheva, dagesh, in UXLC 2.6 | when CLC covers Exodus 32: dagesh, sheva |
| Ex 20:4.2, elyon strand | תֽ͏ַעֲשֶׂה־ | tav | meteg, pataḥ, in CLC until 2026-10-31 | made 2026-10-31: meteg, CGJ, pataḥ, as in UXLC 2.6 |

This section writes each atom with its marks as its CLC change gives them, because this file's
mark-order lint, `py/tests/test_prose_mark_order.py`, rejects a dagesh after another mark of its
letter.

A meteg has Unicode combining class 22, a dagesh 21 and every vowel a class from 10 to 20, so a
meteg stored before its letter's vowel, with no CGJ between them, is canonically equivalent to the
same marks with the meteg last. Normalization moves the meteg after the vowel, and so does
HarfBuzz, the shaping engine Chrome and Firefox use, so Taamey D shows the meteg left of the vowel,
a meteg's ordinary place. UXLC 2.6 keeps a meteg before a vowel with a CGJ between them, 871 times,
as the Unicode Standard's Hebrew section (9.1, "Meteg") does; section 8 cites it.

In Job 36:29.7, the only letter in UXLC 2.6's text with a meteg before its vowel and no CGJ, the
meteg came from Kimball's 2026.02.05-136 (F407B 1:23, release 2026.04.01): "Examine whether kaf has
a meteg. Add a meteg under the kaf and a transcription note 't'." Its change text puts the meteg
directly after the kaf, and nothing in the record gives its position. MAM-basics' mark-grammar FOI
page, `gh-pages/uxlc/fois/foi-mark-grammar.html`, shows the atom as UXLC 2.6 has it. Ben,
2026-10-28: "if there's a meteg here at all (for the record, I think not), it is a perfectly
normally-placed, i.e. after-vowel, i.e. after-qamats meteg." Of the stored order: "the encoding
order is insane: of course dagesh should come before either qamats or meteg."

That remark led to a search of UXLC 2.6's text for any other dagesh stored after a vowel, a meteg
or an accent of its letter. The yod of Ex 32:19.17 is the only one; it displays as it would with
the dagesh first.

CLC's elyon strand of Ex 20:4.2 stored the tav's meteg before its pataḥ with no CGJ until
2026-10-31, so Taamey D showed the meteg left of the pataḥ. UXLC 2.6 has meteg, CGJ, pataḥ there,
an early meteg, as in תֽ͏ַעֲשֶׂ֨ה־, and CLC's combined row shows that. CLC's strand splitter
kept the elyon strand's meteg but dropped the CGJ after it; it now keeps the CGJ in a strand that
keeps the meteg (`py/clc/clc_dual_cant_oracle.py`).

The scan that found the first and third, of the text on every page MAM-basics publishes, made while
assessing Taamey D 1.1, also found three forms on MAM-basics' Holman pages with a meteg stored
before a vowel and no CGJ: Ps 31:24.1, Prov 30:15.1 and Ezek 40:36.3's qere. They are copies of a
UXLC text that has, or had before UXLC 2.6, the CGJ, and they need no CLC change; the Holman pages
now show them with it, the two from Holman's emails as bracketed corrections. The scan's results
are untracked, in `.novc/taamey-d-1.1-atoms/results/` (`reorder-scan.txt` and `reorder-scan.json`)
in the `GitRepos2` forest's MAM-basics clone.

## 12. The UXLC's fragile words, noted 2026-10-28

`py/main_uxlc_word_list.py`, the mega's `uxlc-word-list` step, writes a list of fragile UXLC words,
`uxlc/out/uxlc-words-fragile.json`. An atom is on it if normalization or HarfBuzz could change the
order of its marks in a way a reader could see: `py/mb_cmn/uni_norm_fragile.py` gives the
definition, and `_is_uxlc_fragile` in the word-list program adds an allowance for the UXLC's vowel
order in Jerusalem. The list holds one atom, Job 36:29.7, which section 11 covers.

Until `408377df`, on 2026-10-28, the definition considered normalization alone and counted any
reordering, and the list held six more atoms. In each of the six, normalization moves a mark below
a letter past a mark above it. Fonts place the marks below a letter independently of those above
it, so that order cannot show, and CLC needs no change for the six.
