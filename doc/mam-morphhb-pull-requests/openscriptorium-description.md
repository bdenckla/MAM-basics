<!-- Draft by Claude (Opus 5.5) for Ben Denckla, 2026-11-03; revised 2026-11-04, when Ben
decided that it is posted only once morphhb accepts the MAPM pull request,
openscriptures/morphhb#114, posted 2026-11-04. Not posted. The text assumes morphhb has
merged that pull request; if it is accepted but not yet merged, reword "Why" and item 4
before posting. -->

Title: Read the marked qere in the new MAPM.xml, and fix the paragraph-break reset

---

## Why

`OshbFeaturesImporter` downloads `MAPM/MAPM.xml` from openscriptures/morphhb. That file was the 2014 OSIS conversion of *Miqra according to the Masorah* (MAM) until morphhb merged openscriptures/morphhb#114, which replaced it with today's MAM, written in the same line layout so that this importer's line-by-line regular expressions keep working.

The new file marks the qere in a way the current importer misreads. Run on the new file, a Python port of the current importer gets every ketiv/qere note wrong: it takes `<seg` as the qere wherever the ketiv comes first, and the following word wherever the qere comes first. An import that finds no cached copy now downloads the new file.

### How the new file writes ketiv and qere

A ketiv and its qere are two adjacent segs, in MAM's order:

```xml
<seg type="x-ketiv">KETIV</seg> <seg type="x-qere">QERE</seg>
<seg type="x-qere">QERE</seg> <seg type="x-ketiv">KETIV</seg>
```

- Of the 1,047 pairs, 133 have the qere first. In two pairs, in 1 Chronicles 9:4 and Isaiah 26:20, both with the ketiv first, a maqaf (U+05BE) separates the segs instead of a space.
- A seg can hold a nested element. In five pairs the qere holds a narrow-sense paseq, written as `<seg type="x-paseq">` after a no-break space. In Job 7:5 the ketiv holds a small letter, `<seg type="x-small">`, and a note describing it, `<note type="x-slh-word">`.
- A ketiv without a qere, and a qere without a ketiv, have seg types of their own, `x-ketiv-velo-qere` and `x-qere-velo-ketiv`, holding "(ketiv)" and "[qere]".

The 2014 file has the qere as plain text after the ketiv seg, and the importer takes the text up to the next space as the qere. So some notes imported from the 2014 file today are wrong as well, and the new file with this patch corrects them:

| Verse | Ketiv | Qere imported today, from the 2014 file | Qere imported with this patch, from the new file |
| --- | --- | --- | --- |
| Genesis 30:11 | בגד | only the first word, בָּ֣א | בָּ֣א גָ֑ד |
| Genesis 36:5 | יעיש | the word after the ketiv, וְאֶת־יַעְלָ֖ם, since this qere comes before its ketiv | יְע֥וּשׁ |
| Job 7:5 | וגיש | none: the small letter's seg inside the ketiv seg stops the pattern | וְג֣וּשׁ |

A qere at the end of a verse is also imported today with the start of the end milestone, `<verse`, attached (Genesis 27:3, for example).

## What this pull request changes

1. **Ketiv and qere.** `parse_mapm` now checks once per file whether the file contains `<seg type="x-qere">`. If it does, `extract_ketiv_qere` matches a ketiv seg and the qere seg beside it, in either order, separated by a space or a maqaf. In each seg it removes any `<note>` together with its text and then strips the remaining tags, so a nested paseq or small letter keeps its text and a note's text never becomes part of the ketiv or qere. The note body keeps its form, `Ketiv: …; Qere: …`. If the file has no `x-qere` seg, the old pattern runs unchanged, so the 2014 file still imports the same ketiv/qere notes.

2. **Paragraph-break reset.** `<lb/>` lines set a pending break, which the next verse start records. Until now a pending break was cancelled by any line that is not blank and holds neither `<lb/>` nor the letters "verse". In the 2014 file that has two effects:
   - A tag-only line between the `<lb/>` lines and the next verse, such as `<chapter …/>` or `<lg>`, cancels a real break: for example before the first verse of a Torah chapter, where the 2014 file writes the `<lb/>` lines before `<chapter …/>`, and before a poetic verse that follows a petuḥah, as at Psalm 2:1.
   - When a break falls inside a verse, the line holding the rest of that verse ends with `<verse eID=…/>`. Since it holds "verse", it does not cancel the break, which lands on the next verse instead, as at Genesis 35:23.

   Now a pending break is cancelled by a line that holds no verse start and still holds text once its tags are removed and the surrounding whitespace is stripped. Tag-only lines leave the break pending, and the rest of a broken verse cancels it.

3. **Licence comment.** MAM is released under CC BY-SA 4.0; the 2014 file said CC BY-SA 3.0. The class comment now says so and gives MAM's attribution: "Miqra according to the Masorah" was prepared by Seth (Avi) Kadish from materials he developed at Hebrew Wikisource, and attribution in languages other than Hebrew is to "Hebrew Wikisource", with a link to <https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning>. The comment's counts are updated for the new file: 959 ketiv/qere notes and 59 sections.

4. **Cached download.** The importer downloads MAPM.xml only when `tmp/oshb/MAPM.xml` is missing, so a cached copy of the 2014 file would go on being imported. A comment by `DEFAULT_PATH` now says so. **Delete `tmp/oshb/MAPM.xml` before the next import, so that the import downloads the new file.**

Nothing else changes.

## Limitations this pull request leaves in place

- **A ketiv without a qere, and a qere without a ketiv, are not imported.** The new file's 8 `x-ketiv-velo-qere` and 9 `x-qere-velo-ketiv` segs are not pairs, and the new pattern does not match them. From the 2014 file, a ketiv without a qere is imported with the following word as its qere. Importing them would be a small extension: a scan for each of the two seg types, with a note body such as `Ketiv: (…); no qere`.
- **Only lines holding a verse start are scanned.** A pair on a later line of its verse is not imported: on the second or third `<l>` line of a poetic verse, or after a break inside a verse. 959 of the new file's 1,047 pairs are on lines holding a verse start. Scanning every line would mean tracking the current verse from line to line.
- **Paragraph breaks already stored are kept.** The importer only ever sets `markup["paragraph_break"]`, and the wipe at the start of `perform` covers notes and parashot, not breaks. So on a database that already holds an import of the 2014 file, a new import adds breaks but removes none: the 47 breaks that leaked onto the verse after a verse broken in the middle stay, and so do the breaks that the 2014 file placed by MAM's own verse numbers. Clearing `paragraph_break` on WLC's work units before an import would remove them, and any break another importer may have set there. The figures under "How this was checked" are for imports into a database with no breaks.

## How this was checked

No Ruby was run, and none of this repository's code. Instead, a Python port of the importer's regular expressions and line loop, with the patch applied line for line, mirrors Ruby's ASCII-only `\s` and `String#strip` and replaces the database lookups with a list of WLC-numbered verses. It was run on three inputs.

1. **The 2014 file**, as morphhb had it before openscriptures/morphhb#114. The ketiv/qere notes (957) and the sections (59: 54 parashot and the five books of Psalms) are identical with and without the patch. Paragraph breaks go from 2,721 to 3,030: 359 gained and 50 lost. Each change was traced to its layout and compared with the paragraph breaks, petuḥah or setumah, that MAM's own data marks before each verse.
   - 321 of the gains are breaks in MAM that a `<chapter …/>`, `<lg>`, `</p>` and `<p>`, or table-row line used to cancel. The other 38 are not breaks in MAM's data: the first verses of the five books of Psalms, and 33 chapters that open with a poetic verse and no break, where the 2014 file nevertheless writes one `<lb/>` before `<lg>`. The new file writes no `<lb/>` there.
   - 47 of the losses are breaks that leaked onto the verse after a verse broken in the middle, Genesis 35:23 and 46 more. The other 3 are breaks in MAM, lost next to layout that the new file does not have: two arrow characters, a downwards and an upwards arrow, on the `<lb/>` line before Exodus 20:2 and before Deuteronomy 5:6; and the inverted nun on its own line before Numbers 10:35, whose break the old test kept only because the seg type `x-reversednun` contains the letters "verse".
2. **The new file.** 959 ketiv/qere notes, 59 sections and 3,067 paragraph breaks. Each imported ketiv and qere equals the pair as an XML parser reads it, from two adjacent ketiv and qere segs with notes left out, and the breaks match those that MAM's own data marks.
3. **A sample written for these checks**, from MAM's text: pairs with the ketiv first and with the qere first, a maqaf between the segs, two pairs on one line, a narrow-sense paseq inside a qere (as a seg and, in a variant, as a bare paseq glyph), a small letter and a note inside a ketiv, both singleton seg types, and a pair on a poetic verse's second line. The ten pairs on lines holding a verse start were imported as expected; the singletons and the second-line pair were not imported.

## Other differences in the new file, needing no code change

- Verse numbers follow BHS, as WLC's do, also where the 2014 file followed MAM's own numbering (Numbers 25–26, Joshua 21, 1 Samuel 23–24 and Jeremiah 30–31), so notes and newly marked breaks there land on the matching WLC verse; breaks stored by an earlier import stay where they are (see the limitations above). English `<note type="variant">` elements say where MAM's own numbering differs.
- The last parashah's scope ends at Deuteronomy 34:12; the 2014 file has 34:7.
- 13 of the 54 parashah names carry vowel points as MAM has them, for example נֹח, where the 2014 file has נח.
- The text is MAM's on the date that `MAPM/readme.txt` gives.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
