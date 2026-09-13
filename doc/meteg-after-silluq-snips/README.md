# Crops for the meteg-after-silluq work

Crops of manuscript and printed-edition page images for the two meteg-after-silluq accounts,
[`../meteg-after-silluq-psalms-72-15.md`](../meteg-after-silluq-psalms-72-15.md) and
[`../meteg-after-silluq-job-4-12.md`](../meteg-after-silluq-job-4-12.md), each kept as the evidence
behind a stated fact about what one manuscript or edition has. Tiny crops like these are kept as
fair use (Ben, 2026-09-10). Each section says whose crop it is and which image it was read from.

Each file is named `<source>-<page>-<ref>-<slug>.png`: the manuscript or edition, then the page in
that source's form, with `col<N>-line<N>` after the page where the column and line have been
established.

Crops are kept in a folder for the work they serve, not in one for the manuscript they come from
(Ben's decision, 2026-09-13). Until then these five were in `aleppo/page-snips/`,
`leningrad/page-snips/` and `doc/ms-snips/`.

## Finding a page and its image

### The Aleppo Codex

The page is a leaf in `{leaf_number}{r|v}` form (`../../aleppo/README.md`). A column and line go
into a crop's name when they have been established, as they have for the Job leaves through
`../../aleppo/line-breaks/`.

Ben's crops are from mgketer.org unless he says otherwise (Ben, 2026-09-10). mgketer.org presents
the Codex a chapter at a time, a psalm at a time in Psalms, as what looks like a single image,
often several pages long; whether it is one image or pages joined by the page's script, Ben does
not know.

### The Leningrad Codex

Images come from the two sets that the Leningrad Codex index on Hebrew Wikisource links, which
are the same photographs:

- <https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F430B.jpg> (direct JPEG)
- <https://archive.org/details/Leningrad_Codex_Color_Images/page/n859/mode/1up?view=theater>

That index page, mirrored at `../../in/mam-ws-intro/index-leningrad.mediawiki`, has both links
for every folio — 982 of them, checked 2026-09-10 — so it is the way to get from a folio number
to an image. The page is a folio and side, as in `430B`. Ben does not report lines and columns
(2026-09-10), so a Leningrad crop's name has a column and line only where he gave the line
unprompted.

### The Second Rabbinic Bible

A printed edition's crop is named like a manuscript's, the edition in the manuscript's place. Its
page is named by a pencil mark on it, as in `pencil99`.

## aleppo-253v-Ps72v15-yevarkhenhu.png

Psalms 72:15, the verse-final word, on **leaf 253v**, which has Psalms 71:18–73:10 (MAM's index of
the Aleppo Codex, `../../in/mam-ws-intro/index-aleppo.mediawiki` line 613). Ben's crop,
2026-09-10, from mgketer.org's image of Psalm 72.

**The Aleppo Codex has one meteg/silluq stroke on this word, under the kaf** — confirmed by Ben
from this image on 2026-09-10. The stroke slants like a merkha, but reading it as a merkha is
implausible. There is nothing under the he.

Why it was cropped: the Leningrad Codex has a second stroke, under the he, as UXLC 3.9 records
it, יְבָרֲכֶֽנְהֽוּ׃, and Ben confirmed from its image the same day
(`leningrad-380A-col2-line3-Ps72v15-yevarkhenhu.png`). With the stress
penultimate, that second stroke is a meteg after the silluq. MAM follows the Aleppo Codex here,
and MAM's note at the verse quotes it as יְבָרֲכֶֽנְהוּ, with the one mark; this crop shows that the
manuscript agrees. The whole account is `../meteg-after-silluq-psalms-72-15.md`.

## leningrad-380A-col2-line3-Ps72v15-yevarkhenhu.png

Psalms 72:15, the verse-final word יְבָרֲכֶֽנְהֽוּ׃ as UXLC 3.9 records it, on **folio 380A, line 3**, in
the early middle of the line.

**The Leningrad Codex has a meteg/silluq stroke under the kaf and another under the he** —
confirmed by Ben from this image on 2026-09-10. The stroke under the he stands farther left and a
little lower than he expected, but it plainly belongs to this line and not to the line below,
which would be the other way to read it.

Why it was cropped: UXLC 3.9 and WLC 4.22 record two U+05BD on this word where MAM has
יְבָרְﬞכֶֽנְהוּ, with one, on the kaf, which is its silluq. With that penultimate stress the stroke
under the he is a meteg after the silluq. MAM follows the Aleppo Codex here, and MAM's note at
the verse quotes that manuscript with the one mark. The whole account is
`../meteg-after-silluq-psalms-72-15.md`.

### Calibration note for the atom-location estimator

`page_and_guesses` in `MAM-basics/py/py_uxlc/my_uxlc_location.py` put this word at folio 380A,
column 2, line 5.5 — two and a half lines low against the line 3 Ben read off the image:

```
{'page': '380A', 'fline-guess': '32.5', 'line-guess': '5.5', 'column-guess': 2}
```

The folio is right and the column is not independently confirmed: Ben named the line only, and
the column in this file's name is the estimator's.

## aleppo-271r-col2-line5-Job4v12-menhu.png

Job 4:12, the verse-final word, which ends **line 5 of column 2 of leaf 271r**
(`../../aleppo/line-breaks/271r.json` lines 814–836). Ben's crop, 2026-09-10, from
mgketer.org's image of Job 4.

**The Aleppo Codex has two meteg/silluq strokes on this word, one under the mem and one under the
he** — confirmed by Ben from this image on 2026-09-10. The Internet Archive's photograph of the
leaf, `../../aleppo/aleppo-pages/271r.jpg`, has the same two strokes at its resolution.

The stroke under the mem stands to the right of its segol, in the same place as the Leningrad
Codex's (`leningrad-398A-Job4v12-menhu.png`). Ben calls it an early
metsil, metsil being his shorthand for meteg/silluq, because at this word whether it is a meteg or
a silluq is exactly what is in question. He had taken the placement for scribal whim, and finds
the two manuscripts' agreement on it unlikely to be chance. Yeivin says that both manuscripts keep
a gaʿya to the left of its vowel, with very few exceptions (ITM §314, reported in section 5 of
`../meteg-after-silluq-job-4-12.md`).

Why it was cropped: MAM has מֶֽנְהֽוּ׃, with both U+05BD, following the Aleppo Codex, and Koren has
only the one on the mem, so which of the two is the silluq is the open question. The whole
account is `../meteg-after-silluq-job-4-12.md`.

## leningrad-398A-Job4v12-menhu.png

Job 4:12, the verse-final word מֽ͏ֶנְהֽוּ׃ as UXLC 3.9 records it, on **folio 398A**. Ben's crop,
2026-09-10.

**The Leningrad Codex has a meteg/silluq stroke under the mem and another under the he** —
confirmed by Ben from this image on 2026-09-10. UXLC 3.9 and WLC record the same two marks.

The stroke under the mem stands to the right of its segol, which UXLC records as a leading meteg.
Ben calls it an early metsil, metsil being his shorthand for meteg/silluq, because at this word
whether it is a meteg or a silluq is exactly what is in question. His impression is that the
placement is common with a sheva, uncommon with a segol, and commonest on a word's first letter,
where it causes no confusion; this one is on the first letter. He also sees signs of a possible
erasure after the segol and around the stroke under the he. The Aleppo Codex has the stroke under
the mem in the same place (`aleppo-271r-col2-line5-Job4v12-menhu.png`); Ben had
taken the placement for scribal whim, and finds that agreement unlikely to be chance.

Why it was cropped: MAM has מֶֽנְהֽוּ׃, with both U+05BD, and Koren has only the one on the mem, so
which of the two is the silluq is the open question; this crop settles what the Leningrad Codex
has, which until then only UXLC and WLC recorded. The whole account is
`../meteg-after-silluq-job-4-12.md`.

### No calibration point for the atom-location estimator

`page_and_guesses` in `MAM-basics/py/py_uxlc/my_uxlc_location.py` put this word at folio 398A,
column 2, line 4.0:

```
{'page': '398A', 'fline-guess': '31.0', 'line-guess': '4.0', 'column-guess': 2}
```

Ben did not read the column or the line off the image, so this crop gives no calibration point.

## second-rabbinic-bible-vol4-pencil99-Job4v12-menhu.png

Job 4:12, the verse-final atom, מֶֽנְהֽוּ׃ in MAM, in **the Second Rabbinic Bible, volume IV**:
the Venice Mikra'ot Gedolot of 1524–25, edited by Jacob ben Hayyim. Ben cropped it on 2026-09-11
from a scan titled "The Second Rabbinic Bible (Mikraot Gedolot) (מקראות גדולות) Volume IV",
on the page marked with a 99 in pencil, which is the `pencil99` in the file name.

**The Second Rabbinic Bible appears to have one meteg/silluq on this atom, under the mem, and none
under the he** — Ben's reading of this image; diacritics, he says, do not come through well in
the scan. MAM has one under the mem and one under the he, and so do both codices, in
`aleppo-271r-col2-line5-Job4v12-menhu.png` and
`leningrad-398A-Job4v12-menhu.png`. At the crop's resolution Claude sees what Ben
sees: under the mem a short stroke beside the segol, under the nun a sheva, and under the he
nothing; the one dark mark below the he is the top of a lamed of the next line.

**The crop is of Job 4:12 and not of Psalms 68:24**, whose last atom, מִנֵּֽהוּ׃, is the only other
atom in MAM with the letters מנהו. Here the atom comes after the ץ of שמץ, and the next line has
the לילה of Job 4:13; in Psalms 68:24 the atom comes after מאיבים.

The question the crop was made for is which of MAM's two meteg/silluq marks on this atom is the
silluq. [meteg-after-silluq-job-4-12.md](../meteg-after-silluq-job-4-12.md) has the evidence, and
counts the Second Rabbinic Bible with Koren, which also has only the mark under the mem, as
evidence that the stress is penultimate.
