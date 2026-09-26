# St. Petersburg Evr. II B 55 page-location data

This directory holds a partial page index of the biblical codex St. Petersburg, National Library
of Russia, Evr. II B 55. It was read from the National Library of Israel's images. B 55 holds
nearly all of the codex's surviving text. Its direct continuation, Evr. II B 247, is a few leaves
of Chronicles, and its pages belong in the same index when they are read, each record carrying
its own shelfmark. The index follows the conventions of [`../cam1753/`](../cam1753/README.md) and
[`../aleppo/`](../aleppo/README.md). No program in this repository reads it.

**A Claude session read every record so far and wrote this directory's files, on 2026-09-25, at
Ben's request. Ben has not yet checked the readings.**

## Data

- [`evr-ii-b-55-page-index.json`](evr-ii-b-55-page-index.json) is the page index. It is partial
  and grows page by page. The consumer guide below describes it.
- [`evr-ii-b-55-images-provenance.md`](evr-ii-b-55-images-provenance.md) records where the
  images read so far came from.
- No image is tracked here. The images are the NLI's. Ben's download of them holds about half of
  the codex's images, and the provenance record describes it. The crops made while reading are
  scratch files and are not kept.

## Consumer guide

`evr-ii-b-55-page-index.json` is a page-entry index. Its canonical top level has exactly `header`
and `body`:

```json
{
  "header": {
    "description": "...",
    "consumer_notice": {"summary": "...", "critical_rules": ["..."], "documentation": "https://..."}
  },
  "body": ["...page records only..."]
}
```

The records are locators. They are not a transcription of the manuscript and not a Bible
edition. A page can begin or end mid-verse, and that boundary is meaningful: do not round it to a
whole verse. The index records nothing of what the manuscript has in pointing, accents or meteg.
What the manuscript has at a word is for Ben to read.

A body record has these fields, in this order:

| Field | Meaning |
| --- | --- |
| `de_shelfmark` | The page's shelfmark. It follows the NLI part: Part B's images are taken to be B 55's (see "The NLI's images" below). |
| `de_nli_part` | The part of the NLI's presentation that the image belongs to, `A` or `B`. |
| `de_nli_image` | The image's number within its part, as its downloaded filename gives it. |
| `de_fl_id` | The NLI file id in the same filename, such as `FL48719250`. |
| `de_layout` | The page's layout: columns or half-lines, ruled lines, and blank lines. |
| `de_first_atom_ref`, `_num`, `_text`, `_state` | The first atom the page held. |
| `de_first_atom_basis` | Present only when the first atom is lost. It says how the atom was inferred. |
| `de_first_surviving_atom_ref`, `_num`, `_text`, `_state` | Present only when the first atom is lost. They name the first atom that survives. |
| `de_last_atom_ref`, `_num`, `_text`, `_state` | The page's last atom. |
| `de_pencil_numbers` | The pencilled numbers seen at the foot or in the lower-left margin, each with `de_number`, `de_place` and, where the reading is uncertain, `de_doubt`. An empty list means that none was seen there. |
| `de_text_at_line`, `de_text_at_line_ref` | A located verse. The first field gives the verse's atoms on one line, and the second names that line. |
| `de_note` | Who read the record, when, and at what resolution, with any damage that affects the reading. |

An atom is one written form between spaces or maqafs. These rules define its fields:

1. **A `_ref` names a verse** in the form of the verse labels in `../aleppo/line-breaks/` and
   `../cam1753/cam1753-line-breaks/`: MAM-simple's book id, then the chapter and verse, as in
   `2Chr 11:16`, `Ps 58:4` or `Job 4:11`.
2. **A `_num` counts the verse's atoms from 1** in MAM's word sequence in
   [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/). The segmentation is the one
   behind the Aleppo and Cambridge 1753 flat streams:
   [`../py/py_ac_loc/mam_xml_verses.py`](../py/py_ac_loc/mam_xml_verses.py)'s
   `get_verse_words`, then the split after every maqaf that each package's
   `gen_flat_stream.py` makes. So the paseq glyph and a sof pasuq belong to the atom before
   them, and where MAM has a ketiv/qere, the atoms are the ketiv's. A ketiv that is not read is
   an atom too. A qere that is not written contributes no atom, and neither does the repeated
   ending that MAM adds after the last verse of four books. A parashah break within a verse
   does not interrupt the count. The numbers count the same units as the word sequences of
   those two line-break trees, so the existing flat-stream and line-break tools could extend
   to this manuscript later.
3. **A `_text` is MAM's letters for the atom or atoms, unpointed**, one space between atoms,
   whether MAM joins them with a space or a maqaf. A script lifted every one from MAM-simple.
   None was typed. A cue helps a reader find the place. It is not a reading of the manuscript,
   and pointing it would suggest that the pointing had been read off the image, which it has not
   been.
4. **A `_state` is `complete`, `damaged` or `lost`.** A damaged atom is partly legible, for
   example when a tear cuts the tops of its letters. A lost atom was not seen at all. A lost first
   atom is recorded only with its basis, never as seen.
5. **Lines are the page's 19 ruled lines of main text**, counted from the top. Blank lines count,
   and the Masorah does not. On a three-column page each column has its own 19 lines, and the
   columns count from the right.
6. **A page's edges are fixed by the layout.** The first atom a page held is at the right end of
   its first line, in the rightmost column on a three-column page. Its last atom is at the left
   end of its last line, in the leftmost column.

The subordinate formats of the other two manuscripts, line-break streams and page geometry, do
not exist here yet.

## The NLI's images

The NLI presents the codex as "Ms. EVR II B 247, 55", in two parts, A and B.

- **Part A** opens at <https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI>.
  Its first image is FL47676695, and it has the catalog note described below. Its 32 images in the
  download sit in a folder labelled CHRONICLES, and the note says that B 247 holds leaves of
  Chronicles, so Part A is apparently B 247. No Part A image has been viewed yet.
- **Part B**'s address in the NLI viewer is not recorded here yet.
- **Numbering.** The first reading session, an earlier Claude session on 2026-09-25 that read these
  pages from reduced images, took a Part B image's number in the download to be its sequence
  number in the NLI's presentation. FL ids increase with that number across all 498 Part B
  filenames in the zip, checked on 2026-09-25.

## The manuscript

- **Layout.** Each image is one page, meaning one side of a leaf. Every page read so far has 19
  ruled lines of main text. On the Psalms and Job pages each line is in two halves, with a blank
  line between psalms. The Chronicles page, image 497, is in three columns. Masorah magna runs at
  the top and bottom of the page, and Masorah parva in the margins. The catalog gives the layout
  as three columns of 19 lines, and the written area as 320 × 297 mm.
- **Pencilled numbers at the foot.** Image 621 has 302, whose last digit is uncertain. Image 623
  has 303, and image 635 has 309. Those are all odd-numbered images. The even-numbered images read
  so far, 622, 632, 634 and 714, have none at the foot, and image 497's foot is torn away. The
  three numbers fit image = 2 × leaf + 17. So in this stretch an odd-numbered image is a recto,
  and the next image is its verso.
- **Pencilled chapter-and-verse numbers** stand in the lower-left margin of three pages: 12,2 on
  image 497, 71,10 on image 632 and 57 on image 714. Each names the verse in which its page ends.
- **The foliation question, which is unresolved.** The catalog cites these folios:
  - B 55, fol. 78b, where 2 Samuel 1:16 ends;
  - B 55, fol. 79a, where 1 Kings 8:61 resumes;
  - B 55, fol. 256, which ends at 2 Chronicles 9:18;
  - B 247, fol. 10, which continues from there.

  By the relation above, fol. 256 would end around image 530. But image 497 already starts in
  2 Chronicles 11:16, which puts the end of fol. 256 around image 494, by the first reading
  session's estimate. There are three possibilities, and none has been checked:
  - somewhere the images don't run two per leaf;
  - the pencilled numbers are not the catalog's foliation;
  - the catalog's number is wrong.

  Image 497 cannot test the relation, because its foot is torn away.

## The NLI catalog's contents list

The catalog note in Part A was translated for Ben on 2026-09-25. Its references use Hebrew chapter
and verse numbers, and "end" means the end of the book. It says that the two parts together
contain the following:

- Joshua 22:30–end; Judges 1:1–10:18 and 11:37–end.
- 1 Samuel 1:1 – 2 Samuel 1:16, ending on fol. 78b.
- 1 Kings 8:61–13:2, beginning on fol. 79a, and 1 Kings 13:21 – 2 Kings 25:25.
- Isaiah 13:19–25:7, 26:21–36:7, 37:36–40:30, 51:15–52:11 and 54:4–65:17.
- Jeremiah 6:1–25, 11:8–12:2, 13:21–17:13, 21:8–23:7, 24:9–30:18, 31:35–32:14, 32:15–36:10,
  39:16–45:5 and 51:51–52:3.
- Ezekiel 10:8–11:5, 18:20–20:44, 22:25–23:15, 23:35–24:6, 29:3–30:1, 33:16–34:18 and 48:24–end.
- The Twelve: Hosea 1:1–4:8, then Hosea 10:9 – Joel 2:14, Amos 4:7–6:8, Amos 9:1 – Obadiah 1,
  Micah 5:7 – Zephaniah 2:7, Zechariah 11:14–14:17, and Malachi 1:12–3:16.
- 1 Chronicles 6:51–62, 6:65–7:7, 7:8–19, 7:21–33, 7:36–8:12, 8:17–36, 8:36–9:9, 9:12–20,
  9:22–34, 9:35–10:3, 12:40–14:4, 14:6–15:13, 15:14–16:4, 22:6–23:32, 24:1–13, 24:14–30, and
  1 Chronicles 25:24 – 2 Chronicles 2:8.
- 2 Chronicles 4:6–9:18, 9:18–10:6, 10:6–25:14, 29:19–30:17, 34:32–35:15 and 36:22–end.
- Psalms 1:1–74:15, 77:7–102:18 and 104:1–end.
- Job 1:1–9:19, 11:3–16:19, 18:20–38:7 and 39:4–end.
- Proverbs, Ruth, the Song of Songs, Lamentations, Esther, Daniel and Ezra, each complete.
- Ecclesiastes 1:1–2:11, where part of chapter 2 and what follows strayed into Esther chapter 2,
  and Ecclesiastes 8:1–end.
- Nehemiah 1:1–9:17.

**The Samuel–Kings gap.** 2 Samuel ends at 1:16 on fol. 78b, and 1 Kings resumes at 8:61 on fol.
79a. So 2 Samuel 1:17 – 1 Kings 8:60 is missing between those two folios.

The catalog note also says the following:

- The leaves missing after fol. 78 are in MS Cairo, Karaite Synagogue 22, whose siglum in Yeivin is written ק(א).
- B 55 alone holds 2 Chronicles 29:19–30:7. The combined list gives 30:17, and one of the two is
  presumably a typo.
- B 247's fol. 10 (2 Chronicles 9:18) directly continues B 55's fol. 256.
- The spelling tradition is identical to Breuer's edition.
- The layout is three columns and 19 lines, and the written area is 320 × 297 mm.
- The concordance lists National Library of Russia Ms. EVR II B 55 and EVR II B 247, and Friedberg
  Genizah Project numbers 55977 and 247977.

## Located verses

Four records carry a located verse in `de_text_at_line`: Psalms 60:10, 70:2 and 72:15, and Job
4:12. They are four of the seven cases in
[`../doc/meteg-after-silluq-bhl-observations.md`](../doc/meteg-after-silluq-bhl-observations.md).
Of the other three, 1 Kings 7:37 falls in the Samuel–Kings gap. 1 Samuel 17:5 and 1 Kings 14:14
are presumably among Part B's images 005–495, which the download lacks.

## Extending the index

1. **Estimate, then read.** Interpolate MAM letter counts between verified pages to estimate the
   target page, then read the target page's edges. The first reading session measured how well
   this works. From the filename labels alone, its first Psalms estimate was about 1.2 images
   early. After one verified page nearby, its estimates were within about half an image.
2. **Read both sides of a boundary at once.** A page's first line also gives the previous page's
   last atom.
3. **Use these letters per page.** The counts run from the first atom the page held to its last
   atom, inclusive. They count letters, U+05D0 to U+05EA, in MAM's atoms as the consumer guide
   defines them, taking the ketiv where MAM has a ketiv/qere. They were counted on 2026-09-25
   against MAM-simple at `6eb743dc`:

   | Image | Span | Letters |
   | --- | --- | --- |
   | 497 | 2Chr 11:16 atom 6 – 2Chr 12:2 atom 4 | 554 |
   | 621 | Ps 58:4 atom 4 – Ps 59:9 atom 7 | 615 |
   | 622 | Ps 59:10 atom 1 – Ps 60:7 atom 6 | 556 |
   | 623 | Ps 60:8 atom 1 – Ps 62:3 atom 8 | 570 |
   | 632 | Ps 69:36 atom 1 – Ps 71:10 atom 8 | 592 |
   | 634 | Ps 72:5 atom 1 – Ps 73:2 atom 4 | 581 |
   | 635 | Ps 73:2 atom 5 – Ps 73:26 atom 6 | 633 |
   | 714 | Job 4:11 atom 1 – Job 5:7 atom 4 | 524 |

   The first reading session counted 571 letters for image 622's span, Psalms 59:10–60:7, at
   verse resolution. That figure does not match the 556 here, and the reason is not known.
4. **Crop at full resolution.** The images read so far are 6,048 to 6,384 pixels wide and 7,056 to
   7,824 pixels tall, and the Read tool shrinks a whole page to about 1,700 pixels wide. So crop
   each edge with Pillow into scratch files, a half or a third of a line at a time, and read the
   crops.
5. **Don't list the download's folder.** Take the images' exact names from the zip's central
   directory, which the provenance record describes. The download sits under OneDrive, where a
   listing or search can pull cloud-only files down to disk.
6. **The segmentation's two former limits were removed on 2026-09-26.**
   - `get_verses_in_range` read only a file's first book, so 2 Samuel, 2 Kings, 2 Chronicles,
     Nehemiah and Joel through Malachi were out of its reach, and 2 Chronicles had to be read
     verse by verse through `get_verse_words`. It now reads the `<book39>` whose `osisID` it is
     given, and raises if the file has none or more than one.
   - `get_verse_words` refused 149 of MAM-simple's 23,202 verses, those holding one of seven
     elements it did not handle. Ben decided on 2026-09-26 what each contributes, keeping the
     atoms what is written on the page. A ketiv that is not read is an atom, like any ketiv. A
     qere that is not written, a maqaf after a ketiv that is not read, and a repeated ending
     contribute nothing. A parashah break within a verse contributes nothing either, so the
     verse's atom numbers run straight through it. In the two Decalogues and at Gen 35:22 the
     atoms are those of `<cant-combined>`, the text with the marks of both strands, whose atom
     numbers and letters are the same as either strand's. The reader's module docstring gives
     each decision with an example. No verse is refused now, and
     `py/tests/test_mam_xml_verses.py` checks both fixes over the whole of MAM-simple.

   The fixes changed no atom of any verse that the reader already accepted, so no `_num` in the
   index and no letter count in item 3 changed.
