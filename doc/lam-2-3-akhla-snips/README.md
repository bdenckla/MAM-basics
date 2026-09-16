# Crops for the Lamentations 2:3 meteg question

Crops of three manuscripts' pages at Lamentations 2:3, kept as the evidence behind a stated fact
about what each manuscript has. A Sefaria correction request of 2026-07-22 asked for a meteg on
one atom of that verse, and none of the three manuscripts has one there; the section on the Codex
Sassoon 1053 crop, below, has the whole account. Tiny crops like these are kept as fair use (Ben,
2026-09-10).

Each file is named `<manuscript>-<page>-<ref>-<slug>.png`, the page in that manuscript's form,
with a column and line after the page where they have been read off the image.

Crops are kept in a folder for the work they serve, not in one for the manuscript they come from
(Ben's decision, 2026-09-13). Until then these three were in `leningrad/page-snips/`,
`cam1753/page-snips/` and `doc/ms-snips/`.

## Finding a page and its image

### masoretica.org

<https://www.masoretica.org/> serves 187 manuscripts — Masoretic, Samaritan and Greek —
addressable straight to a verse:

```
https://www.masoretica.org/?book=Lamentations&chapter=2&verse=3&manuscript=sassoon
```

It gives the page and folio and, where the images are on the Internet Archive, the scan
number, so it turns "which page is this verse on" into one URL. It has the Leningrad Codex,
the Aleppo Codex and Codex Sassoon 1053 among others. Checked 2026-08-04: it does **not**
have Cambridge University Library MS Add. 1753, so the leaf hunt for that manuscript still
runs through `../../cam1753/`.

### The Leningrad Codex

Images come from the two sets that the Leningrad Codex index on Hebrew Wikisource links, which
are the same photographs:

- <https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F430B.jpg> (direct JPEG)
- <https://archive.org/details/Leningrad_Codex_Color_Images/page/n859/mode/1up?view=theater>

That index page, mirrored at `../../in/mam-ws-intro/index-leningrad.mediawiki`, has both links
for every folio — 982 of them, checked 2026-09-10 — so it is the way to get from a folio number
to an image. The page is a folio and side, as in `430B`. A Leningrad crop may include both column
and line when Ben has read the line from the image; the section must say when the column comes only
from the estimator. For another source, include only coordinates established from its image or
retained index.

### Cambridge Add. 1753

The page is a leaf and side in `{leaf:04d}{side}` form, as in `0105B`. To get from a verse to a
page: `../../cam1753/cam1753-page-index.json` for the low-resolution index and
`../../cam1753/cam1753-line-breaks/` for the Job pages that have line-level data. The BookReader
URL is `https://archive.org/details/ketuvim-cambridge-ms-add-1753-images/page/n<spread>/mode/1up`,
where `<spread>` is the entry's `de_archive_spread`. masoretica.org does **not** have this
manuscript.

## leningrad-430B-col2-line10-Lam2v3-akhla.png

Lamentations 2:3, the word אָכְלָ֖ה, on **folio 430B, column 2, line 10**.

**The Leningrad Codex has no meteg on this word** — confirmed by Ben from this image on
2026-08-04. The qamats under the alef stands alone, so nothing in the manuscript marks the
qamats as gadol or the sheva as na.

Why it was cropped: a Sefaria correction request of 2026-07-22 asked that Lamentations 2:3
read אָֽכְלָ֖ה rather than אָכְלָ֖ה, "and therefore both קמץ are קמץ גדול". MAM has no meteg
there, nor does Mikra'ot Gedolot ha-Keter; Metsudah (Lakewood 2001) has one. This crop settles
what the Leningrad Codex has, which is what MAM follows.

UXLC 3.9 has a meteg on בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus silluq on the verse-final
סָבִֽיב׃. This records the transcription; it does not establish what the Leningrad Codex
manuscript has.

Codex Sassoon 1053 and Cambridge Add. 1753 have no meteg on this word either, both confirmed
the same day: `sassoon1053-p740-Lam2v3-akhla.png` for Sassoon 1053 page 740,
and `cam1753-0105B-col2-Lam2v3-akhla.png` for Cambridge Add. 1753 leaf 0105B
column 2.

### Calibration note for the atom-location estimator

`MAM-basics/py/main_uxlc_estimate_atom_loc.py` put this word at folio 430B, column 2, line
12.9 — three lines low against the line 10 Ben read off the image:

```
{'page': '430B', 'fline-guess': '39.9', 'line-guess': '12.9', 'column-guess': 2}
```

The folio is right and the column is not independently confirmed: Ben's correction named the
line only, and the column is still the estimator's. Recorded here as one data point about how
close the estimate runs, not as a defect report.

## cam1753-0105B-col2-Lam2v3-akhla.png

Lamentations 2:3, the word אָכְלָ֖ה, on **leaf 0105B, column 2, third line up from the
bottom** — so line 24, if the column is the usual 26 of `../../cam1753/cam1753-col-quads/`. It is the
right-hand page of archive.org spread n110.

**Cambridge Add. 1753 has no meteg on this word** — confirmed by Ben from this image on
2026-08-04. It agrees with the Leningrad Codex and with Codex Sassoon 1053, whose crops and
confirmations are at `leningrad-430B-col2-line10-Lam2v3-akhla.png`
and `sassoon1053-p740-Lam2v3-akhla.png`.

Those three are what MAM follows here. A Sefaria correction request of 2026-07-22 asked that
Lamentations 2:3 read אָֽכְלָ֖ה rather than אָכְלָ֖ה; MAM has no meteg, and neither does
Mikra'ot Gedolot ha-Keter. This manuscript matters most of the three, being the one MAM cites
most across Lamentations — ק-מ appears in 24 of the book's 38 נוסח notes, against Sassoon
1053's 16, and the Aleppo Codex is absent, Lamentations being one of the books lost from it
entirely.

### How the page was found

By interpolating between column readings Ben made off the images, all now in
`../../cam1753/cam1753-page-index.json`: Lamentations begins on 0105A col 2, 0105B col 2 opens at
Lam 1:17, and 0107A col 1 opens at Lam 3:55. Those bracket Lam 2:3 tightly enough that only
one column is a candidate. The interpolation was originally a fitted lines model, but it
carries nothing now — the readings on either side do the work.

That column also has a centered ספר איכה above it, which first looked like a start-of-book
heading and is not. `../../cam1753/things-noticed-in-cam1753.md` distinguishes it from the איכה that
marks the actual start of the book on 0105A col 2.

## sassoon1053-p740-Lam2v3-akhla.png

Lamentations 2:3, the word אָכְלָ֖ה, in **Codex Sassoon 1053 (MAM's ש1), page 740**, found
through the masoretica.org URL above.

**Sassoon 1053 has no meteg on this word** — confirmed by Ben from this image on 2026-08-04.
So do the other two manuscripts, confirmed the same day:
`leningrad-430B-col2-line10-Lam2v3-akhla.png` for the Leningrad Codex,
and `cam1753-0105B-col2-Lam2v3-akhla.png`
for Cambridge Add. 1753.

The three together answer a Sefaria correction request of 2026-07-22 that asked for
אָֽכְלָ֖ה rather than אָכְלָ֖ה. Sassoon 1053 matters here because it is one of the two
manuscripts MAM leans on throughout Lamentations: of the 38 נוסח notes in the book, ש1
appears in 21 and Cambridge Add. 1753 (ק-מ) in 30, while the Aleppo Codex is absent —
Lamentations is one of the books lost from it entirely, and the four notes that do invoke
the Keter do so at second hand through Yehoshua Kimḥi's record (`א(ק)`, decoded in
[sigil-decoding.md](../sigil-decoding.md)). MAM has no note at all on אָכְלָ֖ה, and these
three crops are why: nothing to report.

Those counts are of the siglum appearing anywhere in a note's `נוסח` documentation, read out
of `MAM-parsed/plus/E3-Lamentations.json`. That is a wider net than "agrees with MAM": ש1 is
cited outside the agreement clause in three notes (4:9, 4:15, 4:16) and ק-מ in one (4:16), so
counting agreement alone gives ש1 18 and ק-מ 29. The figures here read 16 and 24 until
2026-08-04, and reproduced under no counting rule.

Mikra'ot Gedolot ha-Keter has no meteg here either — checked directly, and it agrees
with MAM at this word (private annex §5). Metsudah
(Lakewood, 2001) has one, which is the printed tradition doing what it does.

### MAM answers the qamats question without a meteg

The request asked for the meteg and reasoned from it that "both קמץ are קמץ גדול". MAM says
that second part outright, in the text rather than through a helper mark, because it
distinguishes the two qamats codepoints:

| | form | first qamats |
| --- | --- | --- |
| Lam 2:3, "consuming" | אָכְלָ֖ה | U+05B8 HEBREW POINT QAMATS |
| Gen 1:29, "for food" | לְאׇכְלָֽה׃ | U+05C7 HEBREW POINT QAMATS QATAN |

Both are base text in `MAM-parsed/plus/`, not a `מ:קמץ` template alternative — that template
is for places MAM is making a call worth flagging, as at בׇּֽחֳרִי־אַ֗ף in this very verse.
So no edit to MAM's text would convey anything the text does not already convey.

What MAM's text does not speak to is the sheva. Phonetic MAM does, and agrees it is na:
`’a·kh(e)·la` at <https://bdenckla.github.io/phonetic-hbo/tnkh/E3-Lamentations/02.html>,
against `le·’okh·la` for Gen 1:29.

UXLC 3.9 has a meteg on בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus silluq on the verse-final
סָבִֽיב׃. This records the transcription; it does not establish what the Leningrad Codex
manuscript has.

### The correction request quotes UXLC, not MAM

Checked 2026-08-04 against `UXLC-utils/in/UXLC-39/Lamentations.xml`: the verse as quoted in
the request is byte-identical to UXLC — Sefaria's "Tanach with Ta'amei Hamikra" — across all
17 word atoms, and differs from MAM at exactly two points. UXLC has בָּֽחֳרִי and אַ֗ף
as two atoms separated by a space where MAM has the maqaf compound בׇּֽחֳרִי־אַ֗ף, and UXLC has
plain U+05B8 where MAM has U+05C7. **UXLC uses U+05C7 zero times in all 39 books**, so the
edition the request quotes cannot express the qamats distinction the request argues for,
which is a likely reason it argues from a meteg instead. The section above answers a
question about MAM that was probably asked of a different text.

The space is not UXLC's doing. MAM's note on the verse is `ל!=<בָּֽחֳרִי אַ֗ף> (חסר מקף)`, and a missing maqaf in
the Leningrad Codex recurs rather than being a one-off: MAM notes `חסר מקף` in 31 places
corpus-wide, 23 of them naming the Leningrad Codex — among them Gen 18:18, Ex 38:20,
Lev 8:16, Num 4:49, Deut 1:38, Jer 32:13, Esther 5:14 and Lam 5:5. Deut 1:38 adds that the
atoms are written touching even so. That count is a floor, since MAM has a note only where
it has something to report.

### The Metsudah digital edition confuses deḥi and tipeḥa

The Metsudah Five Megillot (Lakewood, 2001) text quoted into the correction thread on
2026-08-04 has U+05AD HEBREW ACCENT DEHI on both of the verse's tipḥas — יְמִינ֭וֹ and
אָֽכְלָ֭ה — where MAM has U+0596 HEBREW ACCENT TIPEHA on יְמִינ֖וֹ and אָכְלָ֖ה.
Deḥi belongs to the poetic system and Eikhah takes the prose accents, so neither atom can
have one, and two of two is not a stray character. The same quotation has no accent on
כֹּל where MAM has U+059A YETIV (כֹּ֚ל), and ends with an ASCII colon rather than
U+05C3 SOF PASUQ.

Deḥi and tipeḥa are the same lookalike pair that
`py/author_misc/rocc_2_pre_vowel_accents_in_ctr.py` documents for Chabad's CTR, which abuses
them in the opposite direction: CTR has the TIPEHA codepoint where a deḥi is meant and tells
the two apart by whether the accent is encoded before or after the vowel, which leaves a bare
deḥi indistinguishable from a bare tarḥa. Rendered at
<https://bdenckla.github.io/MAM-basics/MAM-with-doc/misc/rocc_2_pre_vowel_accents_in_ctr.html>.

The comparison this pair of clues prompted — Metsudah's five Megillot against CTR's, run
2026-08-04/05 — is written up in [metsudah-vs-ctr.md](../metsudah-vs-ctr.md): the
DEHI-for-TIPEHA exchange is corpus-wide (744 of the 745 verses have at least one chanted
word where Metsudah has DEHI and CTR has TIPEHA), and the two texts are independent
conversions of one shared digital ancestor, neither a transform of the other. At this
verse, the meteg the correction request asked for is in both digital texts — Metsudah has
אָֽכְלָ֭ה, CTR has אָֽכְלָ֖ה — though the three manuscripts above lack it; and CTR has the
yetiv, logically before its ḥolam, that the Metsudah quotation lacks.
