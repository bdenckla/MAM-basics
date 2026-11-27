# The masorah circle: how it is stored and drawn

The masorah circle, HEBREW MARK MASORA CIRCLE (U+05AF), is the small raised circle that an
edition prints above its text to mark a word or phrase that has a Masoretic note; the SBL Hebrew
manual calls it the masora circle. This document records what the SBL Hebrew Font User Manual,
Unicode's texts and Taamey D say about where the circle is stored in text, where a font draws it
and how a line breaks around it. Ben asked on 2026-11-27 that this research be kept in Git, so
that it need not be redone from the manual. The manual and Unicode were read, and the renderings
below measured, on 2026-11-27.

## In brief

1. **The manual stores the circle after the character it stands over:** a letter, a maqaf or a
   word space (p. 15). On a letter it comes after the letter's other above marks and before the
   postpositive ones (pp. 11–12). For a circle printed between two letters, the manual puts ZWNJ
   between the first letter's marks and the circle (p. 15).
2. **Unicode says nothing about the circle** beyond its name and its properties. Its general
   guidance deprecates SPACE as the base of a combining mark in favour of NO-BREAK SPACE, so the
   manual's encoding of a circle over a word space is where the circle's documented use departs
   from Unicode's general guidance.
3. **Line breaking follows the character before the circle:** after a letter, a ZWNJ or a maqaf,
   the circle stays with that character; after a SPACE, a line can break between the space and
   the circle, which then begins the next line; after a NO-BREAK SPACE, the line cannot break on
   either side of the space.
4. **HarfBuzz 15.0.0 ignores the manual's ZWNJ.** HarfBuzz is the shaping engine that its
   README lists in Android, Chrome, Firefox and many other systems. Shaped with it, Taamey D 1.2
   and SBL Hebrew 1.56a both draw a circle stored after a ZWNJ over the letter before the ZWNJ.
   SBL Hebrew centres a circle over a maqaf and over a word space, which it widens for the
   circle. Taamey D draws a circle stored after a maqaf or a space at that character's left
   edge.

## Sources

- **The manual:** SBL Hebrew Font User Manual, manual version 1.51 of February 2008, for font
  version 1.5x, prepared by John Hudson, Tiro Typeworks, for the Society of Biblical Literature.
  Page numbers below are this version's. Ben keeps a copy in his OneDrive, as
  `Documents/Tanakh/misc/SBL Hebrew User Manual 1.5x.pdf`. Unicode's document register holds the
  earlier manual version 1.5 of June 2007, for font version 1.50, as L2/19-183
  (https://www.unicode.org/L2/L2019/19183-sbl-hebrew-man-v1-5.pdf); its pages on the circle, 11,
  12, 15 and 22, say the same as version 1.51's.
- **Unicode 18.0.0:** the core specification of 2026-09-16, UAX #14 (Unicode Line Breaking
  Algorithm) revision 57 of 2026-09-01, and the Unicode Character Database files
  `LineBreak-18.0.0.txt`, `DerivedAge-18.0.0.txt` and `NamesList.txt`.
- **Taamey D 1.2:** `Taamey-D/font-m-TaD/Taamey_D.fea`, its lookup `mark4AbvMarks` and its
  "Note on Masorah circle".
- **Renderings:** HarfBuzz 15.0.0, through uharfbuzz 0.57.0 in this repository's environment,
  shaping right to left with script `Hebr`, language `he` and HarfBuzz's default features. The
  fonts were the tracked `Taamey-D/font-m-TaD/Taamey_D.ttf`, version 1.2, and SBL Hebrew
  "Version 1.56a Build 016", the copy from which the comparison images of `Taamey_D.html` were
  rendered (`gh-pages/taamey-d/img/comparison/PROVENANCE.json`, SHA-256 beginning `98eca8ec`).
  Positions are in font units, from HarfBuzz's glyph positions and each glyph's outline.

Ben's own notes on problems in SBL Hebrew, of 2020, 2021 and 2024, say nothing about the circle.

## What the SBL Hebrew manual says

### Where the circle stands, and the character it is stored after (p. 15)

The manual's section "Masora circle handling" says that the circle can stand over a letter,
between two letters, over a maqaf or over a word space. Ideally it would be centred over the
word, but neither Unicode's encoding of combining marks nor OpenType Layout can express that, so
whoever encodes the text has to place the circle with care. By default the font "places the
masora circle above the preceding consonant, maqaf or word space": the circle is stored after
the character that it stands over. The manual's three examples come from Genesis 1:

| Verse | Form as the manual encodes it | The circle is stored after |
|---|---|---|
| Genesis 1:2 | מְרַחֶ֖֯פֶת | the ḥet, the middle letter of five, and its vowel and accent |
| Genesis 1:9 | אֶל־֯מָק֣וֹם | the maqaf |
| Genesis 1:11 | עֵ֣ץ ֯פְּרִ֞י | the space between the two chanted words |

The circle's glyph is centred on a zero advance width. So when the font's default positioning is
inhibited, the circle falls between the character it follows and the next one. ZWNJ (ZERO WIDTH
NON-JOINER, U+200C) between the circle and its letter, maqaf or word space inhibits that
positioning; for a letter, the sequence is the letter, its vowels and accents, ZWNJ, then the
circle. The manual's three examples, again from Genesis 1:

| Verse | Form as the manual encodes it | The manual's page shows the circle |
|---|---|---|
| Genesis 1:10 | וּלְמִ‌֯קְוֵ֥ה | between the mem and the qof, the two middle letters of six |
| Genesis 1:22 | בַּיַּ‌֯מִּ֔ים | between the yod and the mem |
| Genesis 1:28 | וַיְבָ֣רֶךְ‌֯ | after the final kaf, at the atom's end |

The manual adds that ZWNJ can also place a circle after a word at the end of a line, as in its
Genesis 1:28 example. Each ZWNJ form above holds an invisible ZWNJ before the circle.

### The circle's order among a letter's marks (pp. 11–12, 21–22)

The manual's recommended order enters a letter's above marks, the circle among them, as they
stand from right to left, except the postpositive marks, which come last (p. 11). Its Table 1
lists the circle last among the other above marks, and puts the postpositive segolta, pashta,
telisha qetana and zinor in a last group of their own. Note 4 to the table says that although
the circle may be drawn slightly right of the other above marks, it is usually entered after
them (p. 12). Appendix B, which suggests combining classes for a custom normalization, gives
the circle class 230, its class in Unicode (p. 22).

### What the manual does not say

The manual names no edition for its circle examples. Its example of the masora/number dot, from
Numbers 32:24 (p. 15), shows text bearing circles beside a marginal Masoretic note, also without
naming an edition. It says nothing of line breaking at a circle over a word space, of NO-BREAK SPACE, or
of normalization moving the circle. It describes its tests of the font's shaping with
Microsoft's Uniscribe (pp. 6–7) and, briefly, with applications on the Mac and Linux
(pp. 18–19).

## What Unicode says

U+05AF has been in Unicode since version 2.0 of 1996 (`DerivedAge-18.0.0.txt`). Its general
category is Mn (nonspacing mark), its canonical combining class 230 (above), its bidirectional
class NSM and its line-breaking class CM (`LineBreak-18.0.0.txt`). The names list gives it no
annotation, and the core specification's section on Hebrew, 9.1, does not mention it. So the
circle's encoding beyond "a nonspacing mark above" is left to practice, which the manual
documents.

A combining mark follows its base. To show a mark with no letter as its base, the core
specification recommends NO-BREAK SPACE (U+00A0) as the base; using SPACE for this is no longer
recommended, because of conflicts with the handling of runs of SPACE in contexts such as XML
(§2.11.4, "Exhibiting Nonspacing Marks in Isolation", and §7.9). UAX #14 calls the use of SPACE
for this deprecated and says that the two bases look the same but break lines differently
(§5.1, under CM, and §9.2, "Legacy Support for Space Character as Base for Combining Marks").

So the manual's circle over a word space, a SPACE followed by the circle, is the encoding that
Unicode's general guidance discourages. A NO-BREAK SPACE followed by the circle follows that
guidance, but it replaces the edition's word space with a no-break space.

## Line breaking (UAX #14, revision 57)

Rule LB9 gives a combining mark the line-breaking class of the character before it, and rule
LB10 treats a combining mark that follows a space as an alphabetic character. The circle's line
breaking therefore follows the character it is stored after:

| The circle is stored after | Line breaking |
|---|---|
| a letter, or a ZWNJ after a letter | The circle stays with its letter (LB9; ZWNJ is also class CM). |
| a maqaf, class HH | No break before the maqaf (LB21); a break after the circle, before the next atom, is allowed. At a line's end, the circle stays with the maqaf and the atom before it. |
| a SPACE | A break after the space is allowed (LB18) and the circle counts as alphabetic (LB10), so a line can end at the space; the circle then begins the next line, joined to the next atom (LB28). §9.2 allows a tailoring that treats a SPACE and its marks as an ideograph instead. |
| a NO-BREAK SPACE | No break after it (LB12) and none before it, except after a space or a hyphen (LB12a): the two chanted words stay on one line. |

The manual's advice for a circle at the end of a line, the last letter followed by ZWNJ and the
circle, keeps the circle at the end of the line, with the atom before it.

## What Taamey D does

Taamey D's feature file puts the circle in the anchor class `@A23_impo`, the class of the
impositive accents, so a circle on a letter is centred above that letter. Every letter, and the
dotted circle, has an anchor for that class; the maqaf, the space and the no-break space have
none. The file's "Note on Masorah circle" says that a circle on a character with no such anchor
stays unattached, centred on that character's left edge, and that in MAM's documentation notes,
where Taamey D draws the circle, it never shares a letter with another above mark.

Shaped with HarfBuzz 15.0.0, the manual's examples come out as follows in Taamey D 1.2 and, for
comparison, in SBL Hebrew 1.56a:

| Encoding | Taamey D 1.2 | SBL Hebrew 1.56a |
|---|---|---|
| on a letter (Genesis 1:2) | centred over the letter | centred over the letter |
| after a maqaf (Genesis 1:9) | at the maqaf's left end, where the next atom's first letter begins | centred over the maqaf |
| after a SPACE (Genesis 1:11) | at the space's left edge, over the right edge of the next atom's first letter | centred over the space, which the font widens from 554 to 1,244 font units, of 2,048 to the em |
| after a NO-BREAK SPACE | as after a SPACE | as after a SPACE |
| a letter, ZWNJ, the circle (Genesis 1:10, 1:22, 1:28) | centred over the letter before the ZWNJ, as with no ZWNJ | centred over the letter before the ZWNJ, as with no ZWNJ |

The last row is HarfBuzz's doing, not the fonts': each font drew exactly the same positions with
and without the ZWNJ, so HarfBuzz 15.0.0 attaches the circle to the letter across the ZWNJ.
Shaped by it, a circle encoded between two letters as the manual encodes it is drawn over the
first of the two. Neither another HarfBuzz version nor DirectWrite, the shaping of current
Windows applications such as Word, was tested.

A circle over a maqaf or a word space would be centred in Taamey D, as in SBL Hebrew, only if
the font gave the maqaf and the space anchors for the circle; it gives them none today.

## The encodings side by side

| The edition prints the circle | Stored as | Source | Taamey D 1.2 in HarfBuzz |
|---|---|---|---|
| over a letter | the letter, its marks, the circle before any postpositive mark | the manual, pp. 11–12, 15 | over the letter |
| between two letters | the first letter, its marks, ZWNJ, the circle | the manual, p. 15 | over the first letter |
| over a maqaf | the maqaf, the circle | the manual, p. 15 | at the maqaf's left end |
| over a word space | SPACE, the circle | the manual, p. 15 | at the space's left edge |
| over a word space | NO-BREAK SPACE, the circle | Unicode's recommended base for a mark with no letter | at the space's left edge |
| over the space at a line's end | the last letter, its marks, ZWNJ, the circle | the manual, p. 15 | over the last letter |

Which of these encodings a transcription uses, and how it shows them, is that transcription's
own decision, recorded with it.

## Related documents

- [MAM-normal order for Hebrew marks](mam-normal-mark-order.md) also cites the manual's
  Appendix B, for the order of shin dot, sin dot, dagesh and rafe.
- [Taamey D](../Taamey-D/README.md) describes the font's sources, build and shaping checks.
