# Potential UXLC corrections

State: live. Section 4's correction was sent to Chris Kimball, the UXLC's editor, on 2026-10-19,
in Ben's report "Errors in BHL claims in UXLC change-record notes". Nothing else here has been
sent to the UXLC, to its editor or to the author of any change record.

Ben decided on 2026-10-15 to report none of the UXLC problems in sections 1 and 2: "Leave all of
this as is. I don't care about mistakes in UXLC any more." He then added: "who knows, maybe I'll start caring
again at some point in the future. Which, come to think of it, suggests that maybe these UXLC
potential corrections should be recorded in a file in the "doc" folder somewhere, in case I ever
care to report them in the future." This file is that record. Add any later potential UXLC
correction here.

Ben's clarification of 2026-10-20: the file holds potential corrections that the UXLC's editor,
Chris Kimball, might be interested in, "not the (rather huge) set of potential corrections we
might want to make in CLC". A correction argued from grammar alone belongs with CLC, since the
UXLC "does not often (if ever) accept grammatical arguments".

On 2026-10-19 a Claude session rechecked every record below against its change list as tanach.us
then served it. Five of the six lists matched MAM-basics' archived copies record for record. The
sixth, the 2026.10.19 list, had changed, and sections 2 and 3 say how.

A change record's **locator** is its page, column and line, written here as page, then
column:line, such as F063A 2:20. The UXLC's locators count only lines that hold text, so a
citation below blank lines has a line number lower, by the number of blank lines above it, than a
count of every ruled line gives.
Before reporting any locator below, count every ruled line from the column's top on the page
image, and allow for that convention.

## 1. Three locators that disagree with the page images, found 2026-10-14

A comparison of UXLC change records with Charles Loder's leningrad-codex-tei v0.5.0 found these.
That edition is a TEI encoding of pages F001B–F091B, whose line breaks are Gemini's readings of
Sefaria's photographs. For each record, a Claude session's reading of a crop of Sefaria's
photograph, made on 2026-10-14, agrees with the TEI's line. Ben has not checked these three on
the images. In the TEI, none of the three atoms has an empty line above it in its column.

| Change record | Release | Citation | Locator | TEI and Claude's reading | Author |
| --- | --- | --- | --- | --- | --- |
| 2021.02.22-15 | 2021.04.01 | Lev 13:3.12 | F063A 2:20 | line 21 | Stephen Salisbury |
| 2021.12.28-2 | 2022.04.01 | Lev 26:35.3 | F073A 1:1 | line 3 | Todd Shandelman |
| 2022.04.04-6 | 2022.07.04 | Num 9:17.6 | F080B 3:26 | line 25 | Daniel Holman |

The UXLC disagrees with itself about Lev 26:35.3: its earlier record 2021.02.22-17, by Stephen
Salisbury, gives F073A 1:3, as the TEI and Claude's reading do.

The comparison's working files are untracked, under `.novc/lc-tei-phase1/` in the primary
forest's MAM-basics clone, with the crops in its `out/crops/`.

## 2. A pending UXLC 2.6 record that cited the wrong position, found 2026-10-14

Daniel Holman's record 2026.08.05-10, in the proposed UXLC 2.6 change list with file date
2026.10.19, cites Lev 25:20.3 for "Remove mahapakh under the kaf. Remove note 'c'." Its
reference text is at position 4 of the verse; position 3 holds the other atom of that maqaf
compound. Ben's record 2020.12.22-2 cites the same atom as Lev 25:20.4.

The record also leaves its column and line empty. Ben's 2020.12.22-2 gives Folio_71v 2:16 for the
atom, which is page F071B, column 2, line 16, and the TEI and Claude's reading agree. MAM-basics'
override copy of the change list, `uxlc/in/UXLC-misc-fixed/2026.10.19 - Changes.xml`, fills the
empty fields with an estimate, 2:14; section 3 says why.

The change list as tanach.us served it on 2026-10-19, described at the end of section 3, cites
Lev 25:20.4 for this record, so its position is now right. The record still leaves its column and
line empty.

## 3. Defects in the proposed UXLC 2.6 change list, noted 2026-08-12

UXLC-utils commit
[3435fc81](https://github.com/bdenckla/UXLC-utils/commit/3435fc8130642528cfc8a134a645bf4dc7af1141)
recorded these in the copy of `2026.10.19 - Changes.xml` taken from hcanat.us on 2026-08-12, which
`uxlc/in/UXLC-misc/2026.10.19 - Changes.xml` held until 2026-10-20. A later copy is compared at the
end of this section.

1. 2026.08.05-27 (Job 11:6.3) gives its book as `job`, lowercase.
2. 2026.08.05-5 (Ex 20:3.2), 2026.08.05-10 (Lev 25:20.3) and 2026.08.05-25 (Job 34:20.4) give a
   page but an empty column and line. MAM-basics' override copy fills each from the repository's
   location estimator, so those three values are estimates, not readings of the manuscript.
3. 2026.08.05-19 (2 Sam 5:21.1), Daniel Holman's, describes removing a maqaf, but its change text
   equals its reference text, maqaf included, so the record proposes no change.

A Claude session compared these items with the change list as tanach.us served it on 2026-10-19,
when the list had 140 records and was marked installed rather than proposed. Items 1 and 3 are
fixed there, and item 2 is not. Record 2026.08.05-27 gives its book as `Job`. Record
2026.08.05-19's change text no longer has the maqaf that its reference text has, so the record
now proposes the removal that its description names. Four records of the installed list give a
page but an empty column and line: item 2's three, and 2026.08.05-47, which the proposed list
lacked.

| Record | Citation in the installed list | Page | Override's estimate |
| --- | --- | --- | --- |
| 2026.08.05-5 | Ex 20:3.2 | F043A | 2:19 |
| 2026.08.05-10 | Lev 25:20.4 | F071B | 2:14 |
| 2026.08.05-25 | Job 34:20.4 | F406B | 2:27 |
| 2026.08.05-47 | Ps 14:7.1 | F367B | 2:22 |

Since 2026-10-20, `uxlc/in/UXLC-misc/2026.10.19 - Changes.xml` has been the installed list, as
hcanat.us served it that day, byte for byte the copy that tanach.us served on 2026-10-19. The
override copy was rebuilt from it the same day. It fills the four empty locators with the location
estimator's values in the table, the first three unchanged, and it no longer needs item 1's
correction.

## 4. Wrong letter name in a change-record note, found 2026-10-17

Daniel Holman's record `UXLC2022.08.29#20` (also written 2022.08.29-20), released in 2022.12.07,
cites 1 Sam 18:28.11. Its note
says "patah under the ayin" where it should say "patah under the aleph". This is a correction to
the letter named in the note: alef. It does not change the record's proposed vowel change or its
Approved status. The note's exact wording is retained below.

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
below the resh": the word has no qof, and the record's description names the resh. This corrects
only the letter named in the note. It does not change the record's proposed change or its Approved
status. The note's exact wording is retained below. This correction has not been reported. The
record's second note is in Ben's report of 2026-10-19 (section 4) for a different error: it says
that BHLA has no entry for this verse, and the report finds that BHLA has an entry for this word.

<details>
<summary>Exact UXLC note</summary>

> The mark below the qof has the northeast-to-southwest inclination of a merkha. Since this word occurs at the end of the verse, the mark should be a meteg acting as a siluq; a merkha is inappropriate here. Adding note 't'.

</details>

Source: [archived UXLC change records](../in/UXLC-misc/all_changes.json), record `/818`, note `/818/notes/0` (changeset
`2023.06.09`, number `10`; release `2023.10.19`; manuscript locator `Folio_413B 2:10`).

## 6. Change texts that UXLC 2.6 did not install, found 2026-10-20

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
