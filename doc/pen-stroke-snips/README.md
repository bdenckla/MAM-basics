# Crops for the pen-stroke exemplars

Six crops of the Leningrad Codex, each with its stroke-SVG, and `overlays.html`, which draws
every stroke-SVG over its crop. Four are of one chanted word each, the first exemplars of the
representation that [../pen-stroke-representation.md](../pen-stroke-representation.md)
describes; two, added on 2026-10-31, are of whole lines that are well kept and sharply
photographed. [../pen-stroke-exemplars-2026-10-30.md](../pen-stroke-exemplars-2026-10-30.md)
and its update report what they showed. Claude traced every stroke by eye, a script of
Claude's smoothed each into curves and fitted its widths and ends to the ink, and Claude judged
every residual piece. Ben has checked the readings of the marks in the two crops on page F043A
and of the vowels under the nun of F102A's על־פני, and on 2026-10-31 he answered round 3's nine
questions about the two line crops; no human has reviewed the rest.

A mark the crop shows little or no ink of, but that the transcription or the layout implies,
is a **supplied stroke** (decision 15 of the schema note). `overlays.html` draws every supplied
stroke hatched in orange and outlined with dashes, and nothing else that way. F102A's על־פני
has two, the bar and the tick of the qamats under its nun, which Ben reads there from the
faintest remnants and the space they leave.

## The crops

Each crop is a QUPO atom of the Decalogue: in one strand its letter has a qamats and an accent
under it, and in the other a pataḥ and an accent over it. MAM-parsed/plus has four such atoms in
its 34 dual-cantillation units: פני and מתחת, each in both Decalogues.

| Crop | Page, column, line | Verse in MAM | Verse in the UXLC | Box in the source image |
| --- | --- | --- | --- | --- |
| `leningrad-043A-col2-Ex20v2-PNY.png` | F043A, 2, 20 | Exodus 20:2 | Exodus 20:3 | 2247 2480 2346 2593 |
| `leningrad-043A-col2-Ex20v3-MFXF.png` | F043A, 2, 22 | Exodus 20:3 | Exodus 20:4 | 1778 2662 1974 2776 |
| `leningrad-102A-col3-Deut5v6-3L0PNY.png` | F102A, 3, 23 | Deuteronomy 5:6 | Deuteronomy 5:7 | 585 2798 852 2927 |
| `leningrad-102A-col3-Deut5v7-MFXF.png` | F102A, 3, 26 | Deuteronomy 5:7 | Deuteronomy 5:8 | 555 3084 721 3214 |

The filenames follow MAM's verse numbers, and their slugs are `consensus_to_ascii` of the
consonants: PNY for פני, MFXF for מתחת and 3L0PNY for על־פני. In MAM, the תחתון strand has
the chanted words עַל־פָּנָֽי׃ and מִתָּ֑חַת, and the עליון strand has עַל־פָּנַ֗י and מִתַּ֜חַת.

**The primary transcription is the UXLC's,** which puts both strands' marks on one letter
(decision 13 of the schema note). Each stroke-SVG gives it as `data-combined-chanted-word`:
the form עַל־פָּנָֽ͏ַ֗י in both Exodus 20:3 and Deuteronomy 5:7, the UXLC's verse numbers;
the form מִתָּ֑͏ַ֜חַת in Exodus 20:4; and the form מִתָּ֑֜חַת in Deuteronomy 5:8.
In the first two, a combining grapheme joiner separates the תחתון strand's vowel and accent
from the עליון strand's. The third has no pataḥ. Where Ben says the UXLC should be changed,
the stroke-SVG takes his change, and its `data-combined-source` says so.

1. **F043A's פני is one atom of a chanted word that a line break splits.** The atom opens line
   20 and על־ ends line 19, so the crop holds the atom alone.
2. **F102A's על־פני ends line 23,** so its crop holds the whole chanted word.
3. **Both מתחת crops hold the UXLC's atom 12 of 16** of their verse.

Each box keeps the word's ink whole, so some ink of the line above, the next line or a
neighbouring word is inside it. Those strokes are traced and grouped like the rest, with a note
saying whose they are.

**The column and line** are Claude's count, from each column's horizontal ink profile: 27 text
lines in F043A's column 2, the fifteenth holding only the atom לאמר, and 27 in F102A's column 3. The
atom-location estimator put the four atoms at lines 20.3, 23.0, 23.9 and 27.0. That is the
line counted or one below it, as it has run low before.

## The crops of whole lines

Ben chose these two lines on 2026-10-31 from a survey of pages F043A and F102A that ranked
their text lines by focus, flaking and contrast. Each crop holds its line's ink whole, so the
feet of the line above and the marks under it reach in from the top, and the marks over the
line below from the foot. Those strokes are traced and grouped as the other lines' ink.

| Crop | Page, column, line | Verse | The line's atoms in the UXLC | Box in the source image |
| --- | --- | --- | --- | --- |
| `leningrad-043A-col2-line4-Ex19v23.png` | F043A, 2, 4 | Exodus 19:23 | atoms 5 to 10 of 20 | 1574 930 2332 1066 |
| `leningrad-102A-col2-line2-Deut4v42.png` | F102A, 2, 2 | Deuteronomy 4:42 | atoms 18 to 22 of 22 | 1562 834 2309 966 |

Unpointed, the first line is לא־יוכל העם לעלת אל־הר and the second אחת מן־הערים האל וחי׃; each stroke-SVG
gives its line pointed, as the UXLC 2.6 has it, as `data-combined-line`, and the lines above
and below as `data-line-above` and `data-line-below`. Neither verse has two cantillations, so
the UXLC's text is the combined transcription. Each line is counted from the top of its
column. Every column of the page begins on the same ruled line, and no line above either of
these is blank, so the count is the same whether blank lines are counted or not. Charles
Loder's TEI of the codex, at commit `15405046fe811d4e1064a7ebcd7cb92261ce72db`, numbers both
lines the same and breaks their neighbours where the image does.

## The source images

Every crop is cut from Sefaria's image without resampling and stored as lossless PNG, its pixels
unchanged from the decoded JPEG.

| Page | Source | Size | Pixels | SHA-256 |
| --- | --- | --- | --- | --- |
| F043A | `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F043A.jpg` | 5,938,828 bytes | 3989 × 4258 | `1B06B6F4A8EF7DF166CF90667A7F7B6F111B1E6B0ED4FA2A9DEF861B0C93DE48` |
| F102A | `https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F102A.jpg` | 5,634,809 bytes | 3943 × 4272 | `93C81513C1A21D0B11BD6D9461FA9679AED038C27104DBD7D8FF9182CF05D54E` |

Both carry a Last-Modified date of 2021-01-13. The two images were downloaded on 2026-10-30 with
Ben's approval and are not tracked. The host serves no robots.txt. The two line crops are cut
from the same two images.

**Sefaria's images are the best available copy.** The Internet Archive's item
`Leningrad_Codex_Color_Images` has the same-named files in its raw zip, uploaded 2021-05-25.
Its F043A, 3,511,835 bytes, was downloaded to compare. It is 4479 × 5279 pixels, but it is the
same photograph uncropped: Sefaria's image matches it at one offset, 490 pixels right and 596
down, with a normalized correlation of 0.94 to 0.997 at four patches far apart. The extra pixels
are the West Semitic Research Project's scale and colour target. The Internet Archive's JPEG is
the more compressed, with quantization tables of about quality 75 against about 95.

**The scale.** The centimetre bar in the Internet Archive's F043A has 240.0 pixels to each
dark-and-light pair of squares. That makes about 120 pixels a centimetre, or 0.083 mm a pixel,
in the bar's plane, which may not be the page's. Sefaria's F043A has the same pixels. F102A's
photograph has no measured scale, but its page is about as many pixels wide.

## Judgments of the residual pieces

A piece judged `ink` is ink that the threshold or the tracer left out: a speck of a stroke
broken by the threshold, a pale spot inside a stroke, or the faint top of a letter of the next
line. A piece judged `damage` is a pale spot where the ink round it has visibly flaked, as in
F102A's מתחת. A one-pixel piece at a stroke's edge is `noise`. A dark dot that belongs to no
stroke is a `speck`. In the line crops, a speck at the crop's edge that is the tip of another
line's letter, which the edge cuts, is `ink`; a pale smudge on the parchment is a `stain`; and
the filled hole in a ring of ink is `paper`.

## Regenerating

From the repository root:

```powershell
./.venv/Scripts/python.exe py/main_pen_stroke.py derive
```

```powershell
./.venv/Scripts/python.exe py/main_pen_stroke.py render
```

`py/tests/test_pen_stroke_svgs.py` fails if a stroke-SVG differs from what its crop and its
authored parts give. The crops are each rights holder's, as `DATA-LICENSES.md` says.
