# St. Petersburg Evr. II B 55 page-location data

This directory holds a partial page index of the biblical codex St. Petersburg, National Library
of Russia, Evr. II B 55. It was read from the National Library of Israel's images. B 55 holds
nearly all of the codex's surviving text. Its direct continuation, Evr. II B 247, is a few folios
of Chronicles, and its pages belong in the same index when they are read, each record carrying
its own shelfmark. The index follows the conventions of [`../cam1753/`](../cam1753/README.md) and
[`../aleppo/`](../aleppo/README.md). No program in this repository reads it.

**Claude sessions made every reading here and wrote this directory's files, on 2026-09-25 and
2026-09-26, at Ben's request. Ben has not checked the readings of page edges. The two locations
that the NLI session read online are also recorded as Ben's report, as "Located verses" says.**

Five contributors are named below, and each keeps its name throughout:

1. **The first reading session**, a Claude session on 2026-09-25, read pages of the download from
   reduced images.
2. **The page-index session**, a Claude session on 2026-09-25, read the eight downloaded pages
   indexed first, at full resolution, and wrote this directory.
3. **The NLI session**, a Claude session on 2026-09-25, viewed images that the download lacks in
   the NLI's online viewer, and located 1 Samuel 17:5 and 1 Kings 14:14.
4. **The findings sub-agent**, a research sub-agent of the page-index session, compiled the NLI
   session's findings from its transcript on 2026-09-25 and read the NLI session's screenshots.
   Its readings of those screenshots are marked as its own wherever they appear.
5. **The image-list session**, a Claude session on 2026-09-26, read the NLI viewer's list of
   volume 2's images and added the NLI session's findings to this directory.

## Data

- [`evr-ii-b-55-page-index.json`](evr-ii-b-55-page-index.json) is the page index. It is partial
  and grows page by page. The consumer guide below describes it.
- [`evr-ii-b-55-nli-fl-ids.json`](evr-ii-b-55-nli-fl-ids.json) gives the NLI's file id of each of
  volume 2's images 1–495, most of which the download lacks. "Reaching images 005–495 online"
  describes it.
- [`evr-ii-b-55-images-provenance.md`](evr-ii-b-55-images-provenance.md) records where the
  images read so far came from, and what the NLI's record and image service showed.
- No image is tracked here. The images are the NLI's. Ben's download of them holds about half of
  the codex's images, and the provenance record describes it. The crops made while reading are
  scratch files and are not kept. Ben's own crops of the last chanted words of six verses, taken
  from these images, are published with the post-silluq case pages, and
  [`../doc/meteg-after-silluq-snips/README.md`](../doc/meteg-after-silluq-snips/README.md)
  documents them.

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

A body record has these fields, in this order. It carries a field only when what the field
records was read:

| Field | Meaning |
| --- | --- |
| `de_shelfmark` | The page's shelfmark. It follows `de_nli_part`: volume 2's images, part `B`, are taken to be B 55's (see "The NLI's images" below). |
| `de_nli_part` | The volume of the NLI's record that holds the image: `A` for volume 1 and `B` for volume 2, as the download's folders name them. |
| `de_nli_image` | The image's canvas number in its volume, which the NLI's viewer labels "Page N". For volume 2 it equals the number in the image's downloaded filename. |
| `de_fl_id` | The NLI file id, such as `FL48719250`. The download's filenames carry it, and the viewer's link takes it after `#$`. |
| `de_layout` | The page's layout: columns or half-lines, ruled lines, and blank lines. |
| `de_first_atom_ref`, `_num`, `_text`, `_state` | The first atom the page held. Present only when the page's edges were read. |
| `de_first_atom_basis` | Present only when the first atom is lost. It says how the atom was inferred. |
| `de_first_surviving_atom_ref`, `_num`, `_text`, `_state` | Present only when the first atom is lost. They name the first atom that survives. |
| `de_last_atom_ref`, `_num`, `_text`, `_state` | The page's last atom. Present only when the page's edges were read. |
| `de_pencil_numbers` | The pencilled numbers seen at the foot or in the lower-left margin, each with `de_number`, `de_place` and, where the reading is uncertain, `de_doubt`. Present only when both places were examined. An empty list means that none was seen there. |
| `de_text_at_line`, `de_text_at_line_ref` | A located verse. The first field gives the verse's atoms on one line, and the second names that line, and on a three-column page its column. |
| `de_note` | Who read or located the record, when, and at what resolution, with any damage that affects the reading. |

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

`evr-ii-b-55-nli-fl-ids.json` has the same two-part top level, but its header has only a
`description`. Each body record has two fields: `de_nli_image`, an image's canvas number in
volume 2, and `de_fl_id`, its file id. The file holds no text and no reading.

The subordinate formats of the other two manuscripts, line-break streams and page geometry, do
not exist here yet.

## The NLI's images

The NLI has one record for the codex, NNL_ALEPH990000991240205171.
Its title is נביאים וכתובים : עם ניקוד וטעמים, מסורה קטנה וגדולה, which in a Claude translation means
"Prophets and Writings: with vowel points and accents, Masorah parva and magna". The record's
viewer page is <https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI>. The
folder names in Ben's download call the codex "Ms. EVR II B 247, 55" and its two volumes Part A
and Part B; the NLI's record uses neither name.

The NLI session found these facts on 2026-09-25. An item that names the image-list session also
says what that session re-checked on 2026-09-26:

- **Two volumes.** The viewer's volume menu has two entries, both labelled "SP RNL EVR II B 55".
  Volume 1 holds the download's Part A, 32 images. Volume 2 holds its Part B, 989 images, of
  which the download has 498.
- **Links.** The link to volume 2's image with FL id `FL<id>` is
  `https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL<id>`.
  Open it in a fresh tab, or navigate to it and then reload: a change to the part after `#`
  alone does not move the viewer. Without `?volumeItem=2` the viewer opens volume 1.
- **The manifest.** The viewer reads volume 2 from
  `https://iiif.nli.org.il/IIIFv21/DOCID/NNL_ALEPH21185775100005171/manifest/IE48716902`. The NLI
  session fetched it from inside the record page, and the image-list session did the same;
  nobody has opened it directly. Its 989 canvases are labelled only "Page N", and it has no table
  of contents or book labels. Volume 1's manifest, `…/manifest/IE47676429`, appears in the record
  page's HTML and has not been fetched.
- **The numbering is confirmed.** Volume 2's image n is the download's Part B image n. The NLI
  session found the same FL id in the manifest and in the download at images 1, 4, 496, 568, 623
  and 714, and the viewer's own image list agreed there and at images 120 and 186, which the
  download lacks. The image-list session found that the viewer's ids for all 498 of the
  download's images equal the ids in its filenames.
- **The download's filename labels are not the NLI's.** Since the manifest labels every canvas
  only "Page N", labels such as `_Psalms-14` came from whoever prepared the download.
- **Which shelfmark volume 1 holds is unresolved.** Only its first image, FL47676695, has been
  seen: a microfilm START frame. Each reading has support:
  - *B 247.* The download labels the folder of volume 1's images CHRONICLES, and the catalog
    says that B 247 holds fragments of Chronicles.
  - *B 55.* The viewer labels both volumes "SP RNL EVR II B 55", and so does each of the record's
    two MARC 907 fields, one for each volume's set of images. B 55 holds fragments of Chronicles
    too, as the catalog's note on B 55 says.

## The manuscript

- **Layout.** Each image is one page, meaning one side of a folio. Every page read so far has 19
  ruled lines of main text. On the Psalms and Job pages each line is in two halves, with a blank
  line between psalms. The Chronicles page, image 497, is in three columns, and the NLI session
  reported three columns on images 120 and 186, in 1 Samuel and 1 Kings, with two lines of
  Masorah above them. Masorah magna runs at the top and bottom of the page, and Masorah parva in
  the margins. The catalog gives the layout as three columns of 19 lines, and the written area
  as 320 × 297 mm.
- **Pencilled numbers at the foot.** Image 621 has 302, whose last digit is uncertain. Image 623
  has 303, and image 635 has 309. Those are all odd-numbered images. The even-numbered images read
  so far, 622, 632, 634 and 714, have none at the foot, and image 497's foot is torn away. The
  three numbers fit image = 2 × folio + 17. So in this stretch an odd-numbered image is a recto,
  the folio's "a" side, and the next image is its verso, the "b" side. Ben identifies the sides
  in the same way in
  [`../doc/meteg-after-silluq-snips/README.md`](../doc/meteg-after-silluq-snips/README.md):
  image 623 is folio 303a, and images 632, 634 and 714 are folios 307b, 308b and 348b.
- **Pencilled chapter-and-verse numbers** stand in the lower-left margin of three pages: 12,2 on
  image 497, 71,10 on image 632 and 57 on image 714. Each names the verse in which its page ends.
- **The foliation question, which is unresolved.** The catalog cites these folios:
  - B 55, fol. 78b, where 2 Samuel 1:16 ends;
  - B 55, fol. 79a, where 1 Kings 8:61 resumes;
  - B 55, fol. 256, which ends at 2 Chronicles 9:18;
  - B 247, fol. 10, which continues from there.

  By the Psalms relation, fol. 256 would end around image 530. But image 497 already starts in
  2 Chronicles 11:16, which puts the end of fol. 256 around image 494, by the first reading
  session's estimate. The Prophets pages do not fit the Psalms relation either. Ben reads the
  folio number 57 at the bottom of image 120, in 1 Samuel, and identifies the page as folio 57a.
  There, image = 2 × folio + 6, and a recto falls on an even-numbered image. That relation would put
  fol. 78b at image 163, where the Psalms relation would put it at image 174. An estimate from
  letter counts puts the end of 2 Samuel 1:16 near the end of image 166 ("Open questions" under
  "Reaching images 005–495 online" gives it). The catalog gives the extent as "482, 13" folios.
  There are three possibilities, and none has been checked:
  - somewhere the images don't run two per folio;
  - the numbers at the foot are not the catalog's foliation;
  - the catalog's number is wrong.

  Image 497 cannot test the relation, because its foot is torn away.

## The NLI catalog's contents list

The record's MARC 500 fields list the contents, and the record page shows the same notes below
the viewer. The NLI session fetched the MARC fields on 2026-09-25 from
`https://iiif.nli.org.il/IIIFv21/marc/bib/990000991240205171`. The list below is a translation
made for Ben on 2026-09-25. The image-list session compared it with the MARC fields on
2026-09-26 and corrected one reference: the fields give Amos 9:1 – Obadiah 1:1, and the
translation had "Obadiah 1". The references use Hebrew chapter and verse numbers, and "end" means
the end of the book. The two volumes together contain the following:

- Joshua 22:30–end; Judges 1:1–10:18 and 11:37–end.
- 1 Samuel 1:1 – 2 Samuel 1:16, ending on fol. 78b.
- 1 Kings 8:61–13:2, beginning on fol. 79a, and 1 Kings 13:21 – 2 Kings 25:25.
- Isaiah 13:19–25:7, 26:21–36:7, 37:36–40:30, 51:15–52:11 and 54:4–65:17.
- Jeremiah 6:1–25, 11:8–12:2, 13:21–17:13, 21:8–23:7, 24:9–30:18, 31:35–32:14, 32:15–36:10,
  39:16–45:5 and 51:51–52:3.
- Ezekiel 10:8–11:5, 18:20–20:44, 22:25–23:15, 23:35–24:6, 29:3–30:1, 33:16–34:18 and 48:24–end.
- The Twelve: Hosea 1:1–4:8, then Hosea 10:9 – Joel 2:14, Amos 4:7–6:8, Amos 9:1 – Obadiah 1:1,
  Micah 5:7 – Zephaniah 2:7, Zechariah 11:14–14:17, and Malachi 1:12–3:16.
- 1 Chronicles 6:51–62, 6:65–7:7, 7:8–19, 7:21–33, 7:36–8:12, 8:17–36, 8:36–9:9, 9:12–20,
  9:22–34, 9:35–10:3, 12:40–14:4, 14:6–15:13, 15:14–16:4, 22:6–23:32, 24:1–13, 24:14–30, and
  1 Chronicles 25:24 – 2 Chronicles 2:8.
- 2 Chronicles 4:6–9:18, 9:18–10:6, 10:6–25:14, 29:19–30:17, 34:32–35:15 and 36:22–end.
- Psalms 1:1–74:15, 77:7–102:18 and 104:1–end.
- Job 1:1–9:19, 11:3–16:19, 18:20–38:7 and 39:4–end.
- Proverbs, Ruth, the Song of Songs, Lamentations, Esther, Daniel and Ezra, each complete. For
  Esther the field adds "see above", which points to the Ecclesiastes entry.
- Ecclesiastes 1:1–2:11, where part of chapter 2 and what follows strayed into Esther chapter 2,
  and Ecclesiastes 8:1–end.
- Nehemiah 1:1–9:17.

**The Samuel–Kings gap.** 2 Samuel ends at 1:16 on fol. 78b, and 1 Kings resumes at 8:61 on fol.
79a. So 2 Samuel 1:17 – 1 Kings 8:60 is missing between those two folios.

The MARC fields also say the following:

- B 55 holds most of the Prophets; from Chronicles, 1 Chronicles 25:24 – 2 Chronicles 2:8,
  2 Chronicles 4:6–9:18, 10:6–25:14 and 29:19–30:7; and Psalms, Job, Proverbs, the five Megillot,
  and Daniel through Nehemiah. The combined list above gives 2 Chronicles 29:19–30:17, and one of
  the two ends is presumably a typo.
- B 247 holds fragments of Chronicles. Its fol. 10 (2 Chronicles 9:18) directly continues B 55's
  fol. 256. The record gives B 247's film number as F 62497 and B 55's as F 65045.
- The folios missing after fol. 78 are in MS Cairo, Karaite Synagogue 22, whose siglum in Yeivin
  is written ק(א).
- Yeivin's list of manuscripts, in *HaMasorah LaMiqra* (5763), gives this codex the siglum ל(א).
  Y. Wagner discusses it in *Hatzi Giborim* 9 (Nisan 5776), pp. 645–656.
- The spelling tradition is identical to Breuer's edition.
- The layout is three columns of 19 lines, the written area is 320 × 297 mm, and the extent is
  "482, 13" folios.
- The codex dates from the 10th–11th century, in Eastern square script, and came from the Second
  Firkovich Collection.
- Some pages carry "holy to the LORD", "not to be sold" or "not to be redeemed" in the upper or
  lower margin, fol. 1a for example. Fol. 79a carries one too, apparently written after the
  manuscript was split and the folios between 78 and 79 were lost.
- The concordance lists National Library of Russia Ms. EVR II B 55 and EVR II B 247, and Friedberg
  Genizah Project numbers 55977 and 247977.
- The images are "From the collections of The National Library of Russia, The National Library
  of Israel. "Ktiv" Project, The National Library of Israel."

## Located verses

Six records carry a located verse in `de_text_at_line`: 1 Samuel 17:5, 1 Kings 14:14, Psalms
60:10, 70:2 and 72:15, and Job 4:12. They are six of the seven cases in
[`../doc/meteg-after-silluq-bhl-observations.md`](../doc/meteg-after-silluq-bhl-observations.md).
The seventh, 1 Kings 7:37, falls in the Samuel–Kings gap. Ben's crops of the six verse-final
chanted words are published with the post-silluq case pages, and
[`../doc/meteg-after-silluq-snips/README.md`](../doc/meteg-after-silluq-snips/README.md)
documents them.

The NLI session located the two verses that the download lacks on 2026-09-25, in the NLI's online
viewer through Claude in Chrome. It read from the viewer's full-screen view, zoomed with the
Chrome tool rather than with the viewer's own zoom, at atom level for the lines named below. It
did not read either page's edges.

1. **1 Samuel 17:5** is on image 120, FL48718013, in the middle column, lines 1–7 of 19. 1 Samuel
   17:4's last atom opens line 1. The verse's last chanted word is one atom, the first atom on
   line 7. The link is
   <https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48718013>.
2. **1 Kings 14:14** is on image 186, FL48718079, in the right column, lines 14–19 of 19. The
   verse's last chanted word is a maqaf compound: its first atom ends line 18, and its second atom
   begins line 19. The link is
   <https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48718079>.

Opened fresh, each link showed volume 2 and the image's "Page N" label. The snips README records
the same two positions as "Ben's report from the NLI image", and Ben made his crops of the two
verses from these images.

## Extending the index

1. **Estimate, then read.** Interpolate MAM letter counts between verified pages to estimate the
   target page, then read the target page's edges. Two sessions measured how well this works:
   - In Psalms, the first reading session's first estimate, from the filename labels alone, was
     about 1.2 images early. After one verified page nearby, its estimates were within about half
     an image.
   - In the Prophets, the NLI session's first estimate put 1 Samuel 17:5 around image 116. It
     assumed that the text begins on image 005 and that a page holds 555–595 letters, and the
     findings sub-agent found that the estimate follows from 595. The verse is on image 120,
     four images later. After reading image 116, the NLI session estimated the bottom of image
     120's third column, using a rough 510 letters per page. It explained later that it had
     estimated image 116's two columns from the 367 letters of 1 Samuel 15:21–27. The verse is in
     the middle column, about half a page earlier. After recalibrating to about 565 letters per
     page, the NLI session found 1 Kings 14:14 on image 186, the first image it tried.
   - The findings sub-agent recounted the Prophets rates, taking the page edges from its own
     reading of the NLI session's screenshots, which nobody has checked at zoom. It found 564.8
     letters per page from the start of image 116 to the start of image 120. From the start of
     image 120 to the start of image 186 it found 568.2, leaving out the Samuel–Kings gap and
     1 Kings 13:3–20. Single pages hold 550, 601 and 582 letters on images 116, 120 and 186.
     Counting 1 Kings 13:3–20 as present would give 585.3 letters per page and would have put
     1 Kings 14:14 about two images later, so the find at image 186 fits the catalog's list,
     which skips from 1 Kings 13:2 to 13:21. The image-list session reproduced these figures on
     2026-09-26.
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

   The Prophets figures in item 1 come from another counter, the NLI session's own, which read
   MAM-simple's JSON rather than the atoms of the consumer guide. On 2026-09-26 the image-list
   session compared the two counters verse by verse over Joshua through Kings, the Latter
   Prophets, Chronicles and the Writings. They agree on all 17,358 verses but Psalms 10:5, where
   `get_verse_words` drops an atom (item 6).
4. **Crop at full resolution.** The images read so far are 6,048 to 6,384 pixels wide and 7,056 to
   7,824 pixels tall, and the Read tool shrinks a whole page to about 1,700 pixels wide. So crop
   each edge with Pillow into scratch files, a half or a third of a line at a time, and read the
   crops. Images that the download lacks are read in the NLI's viewer instead, as "Reaching
   images 005–495 online" describes.
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

   The NLI session's letter counter, written on 2026-09-25 before those decisions, made its own
   choices for four of the seven elements. It counted a ketiv that is not read, skipped a qere
   that is not written and a repeated ending, and read `<cant-all-three>` through its
   `<cant-combined>`. Those choices give the same letters as Ben's decisions, as item 3's
   comparison shows.

   One defect remains, found on 2026-09-26 and not yet fixed. `get_verse_words` takes a
   `<kq-trivial>`'s text only from its `text=` attribute. Psalms 10:5 holds the one
   `<kq-trivial>` in MAM-simple that has child elements instead, so the reader drops that verse's
   second atom and the legarmeh after it. No record reaches Psalms 10.

## Reaching images 005–495 online

Ben's download lacks volume 2's images 005–495. They presumably hold the Prophets and whatever of
Chronicles comes before 2 Chronicles 11. This section records what a later session needs in order
to index them through the NLI's website. Every estimate here is marked as one.

### How to view an image

The NLI session's procedure worked on 2026-09-25, and the image-list session followed its first
steps on 2026-09-26:

1. Use Claude in Chrome, which drives Ben's own Chrome, with his approval in each session. Keep
   its window visible: while the window was hidden, the NLI session's screen captures timed out.
2. Take the image's FL id from `evr-ii-b-55-nli-fl-ids.json`.
3. Open the link, with `?volumeItem=2` and the FL id after `#$`, in a fresh tab, and wait about
   ten seconds.
4. Confirm the canvas with this check, run in the page. It returns the volume, which should be
   "2", the canvas's position and its label, and the manifest:

   ```js
   const w = document.querySelector('iframe[src*="Mirador.html"]').contentWindow; const x = w.Mirador.viewer.workspace.windows[0]; const canv = x.imagesList; const cur = x.currentCanvasID || x.canvasID; const idx = canv.findIndex(c => c['@id'] === cur); ({href: location.href, cur, index1: idx + 1, label: idx >= 0 ? canv[idx].label : null, manifest: x.manifest.uri, vol: document.querySelector('#volumesItems').value})
   ```

5. Run `window.scrollTo(0, 0)`, because a reload keeps the old scroll position, then click the
   viewer's full-screen button.
6. Zoom on half a column at a time, or on two or three lines at a time for atom-level reading.
   The NLI session zoomed with the Chrome tool on regions of the screen, and never used the
   viewer's own zoom.
7. Save nothing.

### Dead ends

The NLI session tried each of these on 2026-09-25, and none worked:

1. The built-in browser, against `www.nli.org.il`, `merhav.nli.org.il` and
   `iiif.nli.org.il/presentationapi.html`. Each showed Cloudflare's check, and on
   `www.nli.org.il` the check looped: the page answered 403 again after each "Verification
   successful".
2. Direct requests to the IIIF image service, which answered "unauthorized". The provenance
   record gives the details.
3. The manifest URLs `https://iiif.nli.org.il/IIIFv21/` followed by
   `DOCID/NNL_ALEPH990000991240205171/manifest`, `DOCID/IE48716902/manifest`,
   `IE48716902/manifest` or `IE47676429/manifest`, which answered "Forbidden" or "Internal
   error". `…/DOCID/PNX_MANUSCRIPTS990000991240205171/manifest` answers but lists no canvases.
4. A viewer link without `?volumeItem=2`, which opens volume 1, and a change to the part after
   `#` without a reload.
5. The browser tool's network log, to discover the manifest. The manifest's URL came from the
   record page's HTML instead.
6. Web searches for a record of Part B of its own. There is none.
7. Guessing FL ids arithmetically above image 363.
8. WebFetch of the NLI's IIIF documentation pages, which answered 403.

### FL ids

- For images 1–363, FL = 48717893 + the image number. The NLI session's run analysis of the
  manifest showed this for all 363 on 2026-09-25, and the image-list session found it again in
  the viewer's list on 2026-09-26. The zip's central directory confirms it at images 001–004.
- From image 364 the ids rise irregularly, so they cannot be computed.
- `evr-ii-b-55-nli-fl-ids.json` lists the ids of images 1–495. The image-list session read them
  from the viewer's image list on 2026-09-26, through Claude in Chrome. It found that the ids rise
  strictly across all 989 canvases and that images 364–409 match what the NLI session's run
  analysis gave. Its transcribed ids reproduce two sums computed in the page, of the ids and of
  each id times its image number. The same two sums over images 1–4 and 496–989 equal those of
  the ids in the download's 498 filenames.
- Canvas sizes identify nothing. Most of the manifest's canvases carry a placeholder size,
  3685 × 2693, and canvas 3's size changed between 2026-09-25 and 2026-09-26.

### What is known of images 116, 120 and 186

Nothing in this table has been checked at zoom, and nobody has read these pages' edges. The
image-list session matched the findings sub-agent's quoted words to MAM's atoms by script.

| Image | FL id | What the NLI session read | How finely | The findings sub-agent's reading of the NLI session's screenshots |
| --- | --- | --- | --- | --- |
| 116 | FL48718009 | 1 Samuel 15:20–27, in the right and middle columns. It did not read the left column. | Verse range, from the whole page in the full-screen view, without zoom | From 1Sam 15:20 atom 17 to 1Sam 15:30 atom 15, the verse's last. The right column runs to 15:23 atom 13, the middle column from 15:23 atom 14 to 15:27 atom 2, and the left column from 15:27 atom 3. |
| 120 | FL48718013 | 1 Samuel 17:5, in the middle column, lines 1–7 | Atoms, for the middle column's lines 1–7 | From 1Sam 17:1 atom 5 to 1Sam 17:11 atom 4 |
| 186 | FL48718079 | 1 Kings 14:14, in the right column, lines 14–19. Lines 1–9 of that column hold 1 Kings 14:11–13, and the middle column holds 14:15–17. | Atoms, for the right column | From 1Kgs 14:11 atom 11 to 1Kgs 14:21 atom 5, a word the screenshot cuts |

- **Image 116's two readings agree.** The NLI session said only "1 Samuel 15:20–27" of image 116.
  After its findings had been compiled, it explained that the range covered only the two columns
  it read, so the two readings agree where they overlap.
- **Image 116's ownership notes.** The NLI session and the findings sub-agent each read two
  ownership notes on image 116, in the unzoomed full-screen view: קדש ליהוה in the upper
  margin at the left and ולא יגאל in the lower margin. The catalog names such notes on fol. 1a
  and fol. 79a, so they do not by themselves identify those folios.

### Open questions

1. **Does the text begin on image 005?** Images 001–004 are in the download and can be viewed
   there. They are small files, 0.19 to 0.84 MB each, against 4.8 to 5.3 MB for the eight pages
   read so far. Image 001 is a microfilm START frame, and image 004's filename label, CONTENTS, is
   the download preparer's.
2. **Where do fol. 78b and fol. 79a fall?** Three estimates disagree:
   1. At about 568 letters per page from the start of image 120, the end of 2 Samuel 1:16 comes
      near the end of image 166, so 1 Kings 8:61 would begin around image 167.
   2. Ben's folio 57a on image 120 puts fol. 78b at image 163, if the images run two per folio in
      between. That would take about 605 letters per page.
   3. If fol. 1a were image 005, fol. 78b would be image 160.
3. **What is canvas 416?** It is FL48718854, the file id that the record's MARC 907 field for
   volume 2 names, and the manifest gives it a real image size, 6304 × 7632. Nobody has looked at
   it.
4. **What is the mark at the foot of image 116?** The findings sub-agent saw a faint mark there,
   illegible in the screenshots. On image 120 the mark is the folio number 57, by Ben's reading.
   By the relation at image 120, image 116 would be folio 55a.
5. **Does the catalogued text fit images 005–495?** The text that the catalog lists before
   2 Chronicles 11 holds 296,806 letters, by the findings sub-agent's count, which the image-list
   session reproduced. At 565–568 letters per page that takes about 523–525 pages, an estimate,
   but images 005–495 are 491 pages. So either later pages are denser, or the catalog's ranges
   overstate what survives. Re-anchor within each surviving stretch rather than carry one rate
   across the catalog's gaps.

### Filling out the download

Whether to obtain the missing images is Ben's decision. Nothing has been downloaded, and no
download path has been tested. The provenance record gives the facts so far in detail:

- The image service serves each image in tiles 1,024 pixels square, under an IIIF level-1
  profile that caps a direct request at 526 × 526 pixels. Direct requests for an image were
  refused as "unauthorized", while the image descriptions (`info.json`) and the MARC record
  answered. The full image 623 is 6288 × 7568 pixels, the size of the download's copy.
- The rights statements conflict. Volume 2's manifest gives its license as the NLI's "public
  domain non commercial use" page, and the MARC record says "Public domain" in field 903 and
  "public domain non commercial use" in field 939. The license of the catalog-only PNX manifest
  and the rights link in `info.json` point to the NLI's "copying prohibited" pages.

The options include these five, and the evidence favours none of them:

1. Keep reading images 005–495 live in the viewer, as the NLI session did.
2. Ask whoever prepared the pCloud folder, who is not known, whether the other images exist.
3. Ask the NLI for the images, or for permission, in view of its conflicting statements.
4. Ask the National Library of Russia, which holds the codex.
5. Check whether the Friedberg Genizah Project's records 55977 and 247977 offer images.

### Segmentation of these books

Since 2026-09-26 `get_verse_words` refuses no verse ("Extending the index", item 6). Of the 4,827
verses that the catalog lists before 2 Chronicles 11, 25 hold one of the seven formerly refused
elements: a ketiv that is not read, with its maqaf, in 2 Kings 5:18; a qere that is not written
in four verses; and a parashah break within the verse in twenty. A later indexer needs no
workaround.
