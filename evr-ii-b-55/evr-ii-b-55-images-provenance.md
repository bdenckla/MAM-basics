# Provenance of the Evr. II B 55 images read so far

A Claude session wrote this record on 2026-09-25, at Ben's request. Each item says whether it was
re-measured that day. The others come from the first reading session, an earlier Claude session on
2026-09-25 that read the same pages from reduced images. No image is tracked in this repository.
The section on the NLI's record and image service was added on 2026-09-26 by the image-list
session, from what the NLI session saw on 2026-09-25; [`README.md`](README.md) names these
sessions.

## Source

- Ben downloaded `C:/Users/BenDe/Downloads/public-archivedwl-808.zip` from a pCloud public link.
  The images in it are the National Library of Israel's images of the codex. Who prepared the
  pCloud folder is not known.
- The zip's Mark of the Web is its `Zone.Identifier` stream. It has `ZoneId=3`,
  `ReferrerUrl=https://u.pcloud.link/`, and a `HostUrl` of `https://apinyc1.pcloud.com/getpubzip`
  followed by a query string, which is left out here. This was re-measured on 2026-09-25.

## The zip

Everything in this section was re-measured on 2026-09-25 from the zip's central directory alone.
Ben asked that sessions never unzip it.

- It is 2,599,554,083 bytes.
- It has 533 entries: 3 directories and 530 files. Every file is stored uncompressed, 2,599,272,011
  bytes in all, and every entry is flagged as having a UTF-8 name.
- The files are dated 2022-04-11, from 03:27:54 to 04:09:58. Zip timestamps have no time zone.
  The top folder's entry and Part A's are dated 2025-11-25, and Part B's is dated 2026-04-06.
- Everything is under a top folder, `L-A_EVR-II-B-247_55/`, in two subfolders:
  - Part B's subfolder is named `Ms. EVR II B 247, 55 Part B נביאים וכתובים (מזרחית, מאה י-יא; החסר בקהיר 22), סנקט פטרבורג, רוסיה - MOST KETUVIM`. It holds 498 images, numbered 001–004 and 496–989 and named `B247, B55 B (Large)-<NNN>-FL<id>.jpg`, and their FL ids increase with the number. The first reading session found that they run from 2 Chronicles 11 through Nehemiah, so the Prophets, presumably images 005–495, are not in the download. In the NLI's viewer the NLI session found 1 Samuel on images 116 and 120 and 1 Kings on image 186.
  - Part A's subfolder is named ` Part A נביאים וכתובים (מזרחית, מאה י-יא; החסר בקהיר 22), סנקט פטרבורג, רוסיה  -  CHRONICLES`, beginning with a space. It holds 32 images named `FL<id>.jpg`, from FL47676695 to FL47676850.
- The Hebrew in both subfolder names is the NLI's title for the codex. In a Claude translation it
  means "Prophets and Writings (Eastern, 10th–11th century; the missing part in Cairo 22),
  St. Petersburg, Russia".
- 34 of Part B's filenames have a label after the FL id. Examples are `_CONTENTS` on image 004,
  `_CHRONICLES-II-11` on image 496 and `_Psalms-14` on image 577. They are not the NLI's: the
  NLI's manifest labels every canvas only "Page N" and has no table of contents, as the NLI session
  found on 2026-09-25. They presumably come from whoever prepared the pCloud folder. The page
  index leaves them out because they are unverified.

## The extraction

- On 2026-09-25 Ben extracted the zip into
  `C:/Users/BenDe/OneDrive/Documents/Tanakh/L-A_EVR-II-B-247_55/`. The first reading session
  dated the extraction between 09:53:56 and 09:55:14, New York time. That day's re-measurement
  covered only the eight images read so far. They were modified between 09:53:58 and 09:54:25,
  New York time, inside that window. Their creation times equal their zip timestamps, read as New
  York time.
- The first reading session found each of the 530 files the same size as its zip entry. The eight
  images read so far were re-checked on 2026-09-25, and each matches its zip entry in size and
  CRC-32.
- Two names changed on extraction, as the first reading session found:
  - The zip entry `B247, B55 B (Large)-831-FL48719670_Song-3:11.jpg` has a colon, which Windows
    forbids in a filename. The file is on disk as `B247, B55 B (Large)-831-FL48719670_Song-3_11.jpg`,
    and its CRC-32 matches the zip's. The zip's spelling was re-measured on 2026-09-25, but the
    file on disk was not re-checked.
  - The zip's Part A subfolder name begins with a space, and Windows dropped the space. This was not
    re-checked.
- **The Windows error dialog.** During the extraction Ben saw a Try Again / Skip / Cancel dialog.
  He retried a few times and then chose Skip. The first reading session found that the extraction's
  only pause, of 9.2 s, came right after image 831 was written. So the dialog concerned that one
  item, and Skip lost none of its content. The session also found a `Zone.Identifier` stream on
  every extracted file, so the skipped step wasn't that either. Each of the eight images re-checked
  on 2026-09-25 has one, with `ZoneId=3` and the zip's own path as its `ReferrerUrl`.

## The NLI's record and image service

Everything here is as the NLI session saw it on 2026-09-25, unless an item names the image-list
session, which re-read it on 2026-09-26. The NLI session read the record page and volume 2's
manifest in Claude in Chrome. It read the other addresses below in the built-in browser, which
reached them without Cloudflare's check.

- **The record** is NNL_ALEPH990000991240205171, and its MARC 001 is 990000991240205171.
  Its title is נביאים וכתובים : עם ניקוד וטעמים, מסורה קטנה וגדולה. The viewer page is
  <https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI>.
- **The volumes.** The viewer's volume menu lists two volumes, both labelled "SP RNL EVR II B 55".
  The MARC record has one 907 field for each volume's set of images:
  - `IE47676429`: 32 images, $h 20210124, $d FL47676757, $n 0008.tif;
  - `IE48716902`: 989 images, $h 20210130, $d FL48718854, $n 0469.tif.

  Both fields give $e "SP RNL EVR II B 55", $g "microfilm" and $k "AR_EVERYONE". The image-list
  session found FL48718854 at volume 2's canvas 416.
- **Volume 2's manifest** is
  `https://iiif.nli.org.il/IIIFv21/DOCID/NNL_ALEPH21185775100005171/manifest/IE48716902`, the
  manifest that the viewer reads. The NLI session fetched it with `fetch()` inside the record page,
  and it answered HTTP 200. Its `sequences[0]` holds all 989 canvases, labelled "Page 1" to
  "Page 989". Its `sequences[1]`, also labelled "SP RNL EVR II B 55", is empty, and its one structure,
  "REP47676694", has no canvases and no ranges. A canvas's `@id` and its image service's `@id` are
  both `https://iiif.nli.org.il/IIIFv21/FL<id>`. The image-list session fetched the manifest the
  same way and read its license and attribution, given with the rights statements below.
- **Volume 1's manifest**, `https://iiif.nli.org.il/IIIFv21/DOCID/NNL_ALEPH21185775100005171/manifest/IE47676429`,
  appears in the record page's HTML and has not been fetched.
- **The PNX manifest**, `https://iiif.nli.org.il/IIIFv21/DOCID/PNX_MANUSCRIPTS990000991240205171/manifest`,
  answers with the record's metadata and no canvases.
- **Canvas sizes.** In the manifest of 2026-09-25, canvases 1–415 and 417–622 were all
  3685 × 2693. Canvas 416 was 6304 × 7632, and canvas 623 was 6288 × 7568, image 623's size in
  `info.json` and in the download. The NLI session judged the 3685 × 2693 sizes to be
  placeholders. The findings sub-agent saw image 116, whose canvas the manifest gives as
  3685 × 2693, displayed taller than wide. On 2026-09-26 the image-list session found canvas 3 at
  3408 × 4160.
- **`info.json` for FL48719462**, image 623, is at
  `https://iiif.nli.org.il/IIIFv21/FL48719462/info.json`. It gives the image as 6288 × 7568
  pixels, with pre-scaled sizes from 49 × 59 up to 3144 × 3784, and tiles of 1024 × 1024 at scale
  factors 1 to 128. Its profile is the IIIF Image API's level 1, with the format jpg; the qualities
  native, color, gray and bitonal; and a maxWidth and maxHeight of 526 and a maxArea of 111,111.
- **Direct image requests were refused.** The NLI session requested
  `https://iiif.nli.org.il/IIIFv21/FL48718854/full/393,/0/default.jpg`, and the same image at
  width 256, in the built-in browser. Each answered with an XML error whose parameter is
  "unauthorized" and whose text is "Error, no permissions, please contact administrator". Neither
  request was retried in Chrome. The `info.json` above, the PNX manifest and the MARC record all
  answered.
- **The MARC record** is at `https://iiif.nli.org.il/IIIFv21/marc/bib/990000991240205171`.
- **The rights statements**, verbatim:
  - volume 2's manifest, read by the image-list session: `license`
    `https://www.nli.org.il/contenteditors/pages-for-terms-of-use/public-domain-non-commercial-use`,
    and `attribution` "From the collections of The National Library of Russia, The National Library
    of Israel. "Ktiv" Project, The National Library of Israel.";
  - the PNX manifest: `license`
    `https://www.nli.org.il/contenteditors/pages-for-terms-of-use/nli-copying-prohibited`;
  - `info.json`: `rights`
    `http://web.nli.org.il/sites/NLI/Hebrew/library/items-terms-of-use/Pages/nli-copying-prohibited.aspx`;
  - MARC 903: $a "No restrictions;", $b "000000011", $c "Public domain" and $d "Over 140 years
    from publishing date";
  - MARC 939: $a "public domain non commercial use".

## The images read so far

These figures were re-measured on 2026-09-25 from the files on disk. No other file in the
download's folder was opened or listed.

| Part B image | FL id | Bytes | Pixels |
| --- | --- | --- | --- |
| 497 | FL48719250 | 5,038,570 | 6144 × 7824 |
| 621 | FL48719460 | 4,914,259 | 6384 × 7120 |
| 622 | FL48719461 | 4,761,552 | 6288 × 7312 |
| 623 | FL48719462 | 5,147,732 | 6288 × 7568 |
| 632 | FL48719471 | 5,302,513 | 6240 × 7520 |
| 634 | FL48719473 | 4,764,952 | 6240 × 7056 |
| 635 | FL48719474 | 5,319,555 | 6128 × 7568 |
| 714 | FL48719553 | 4,991,317 | 6048 × 7104 |

The page index also has records for images 120 and 186, which the NLI session located in the
NLI's viewer. The download lacks them, so they have no row here.
