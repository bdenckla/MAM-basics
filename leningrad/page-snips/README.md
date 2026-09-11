# page-snips

Crops of Leningrad Codex page images, kept as the evidence behind a stated fact about the
manuscript. One file per fact, named `<folio><side>-col<N>-line<N>-<ref>-<slug>.png` when the line
has been read off the image, and `<folio><side>-<ref>-<slug>.png` when it has not, which is the
usual case: Ben does not report lines and columns (2026-09-10).

Images come from the two sets that the Leningrad Codex index on Hebrew Wikisource links, which
are the same photographs:

- <https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F430B.jpg> (direct JPEG)
- <https://archive.org/details/Leningrad_Codex_Color_Images/page/n859/mode/1up?view=theater>

That index page, mirrored at `../../in/mam-ws-intro/index-leningrad.mediawiki`, has both links
for every folio — 982 of them, checked 2026-09-10 — so it is the way to get from a folio number
to an image. <https://www.masoretica.org/> is the other way, and covers 187
manuscripts rather than this one — `?book=Lamentations&chapter=2&verse=3&manuscript=leningrad`
addresses a verse directly and answers with the page, the folio and the Internet Archive scan
number.

A snip of a manuscript with no repo of its own goes to `MAM-basics/doc/ms-snips/` instead.

## 430B-col2-line10-Lam2v3-akhla.png

Lamentations 2:3, the word אָכְלָ֖ה, on **folio 430B, column 2, line 10**.

**The Leningrad Codex has no meteg on this word** — confirmed by Ben from this image on
2026-08-04. The qamats under the alef stands alone, so nothing in the manuscript marks the
qamats as gadol or the shewa as na.

Why it was cropped: a Sefaria correction request of 2026-07-22 asked that Lamentations 2:3
read אָֽכְלָ֖ה rather than אָכְלָ֖ה, "and therefore both קמץ are קמץ גדול". MAM has no meteg
there, as does Mikraot Gedolot Haketer; Metsudah (Lakewood 2001) has one. This crop settles
what the Leningrad Codex has, which is what MAM follows.

Two further facts about the same verse, from `../../in/UXLC-39/Lamentations.xml`
rather than from the image: the verse has a meteg on בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus
the silluq on the verse-final סָבִֽיב׃. So the absence on אָכְלָ֖ה sits among three marks
present, not on a page sparing with them.

Codex Sassoon 1053 and Cambridge Add. 1753 have no meteg on this word either, both confirmed
the same day: `../../doc/ms-snips/sassoon1053-p740-Lam2v3-akhla.png` for Sassoon 1053 page 740,
and `../../cam1753/page-snips/0105B-col2-Lam2v3-akhla.png` for Cambridge Add. 1753 leaf 0105B
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

## 380A-col2-line3-Ps72v15-yevarkhenhu.png

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
`../../doc/meteg-after-silluq-psalms-72-15.md`.

### Calibration note for the atom-location estimator

`page_and_guesses` in `MAM-basics/py/py_uxlc/my_uxlc_location.py` put this word at folio 380A,
column 2, line 5.5 — two and a half lines low against the line 3 Ben read off the image:

```
{'page': '380A', 'fline-guess': '32.5', 'line-guess': '5.5', 'column-guess': 2}
```

The folio is right and the column is not independently confirmed: Ben named the line only, and
the column in this file's name is the estimator's.

## 398A-Job4v12-menhu.png

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
the mem in the same place (`../../aleppo/page-snips/271r-col2-line5-Job4v12-menhu.png`); Ben had
taken the placement for scribal whim, and finds that agreement unlikely to be chance.

Why it was cropped: MAM has מֶֽנְהֽוּ׃, with both U+05BD, and Koren has only the one on the mem, so
which of the two is the silluq is the open question; this crop settles what the Leningrad Codex
has, which until then only UXLC and WLC recorded. The whole account is
`../../doc/meteg-after-silluq-job-4-12.md`.

### No calibration point for the atom-location estimator

`page_and_guesses` in `MAM-basics/py/py_uxlc/my_uxlc_location.py` put this word at folio 398A,
column 2, line 4.0:

```
{'page': '398A', 'fline-guess': '31.0', 'line-guess': '4.0', 'column-guess': 2}
```

Ben did not read the column or the line off the image, so this crop gives no calibration point.
