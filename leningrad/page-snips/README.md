# page-snips

Crops of Leningrad Codex page images, kept as the evidence behind a stated fact about the
manuscript. One file per fact, named `<folio><side>-col<N>-line<N>-<ref>-<slug>.png`.

Images come from the two sets the wiki index links, which are the same photographs:

- <https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F430B.jpg> (direct JPEG)
- <https://archive.org/details/Leningrad_Codex_Color_Images/page/n859/mode/1up?view=theater>

`lenin-wiki/index.wiki` has both links for every folio, so it is the way to get from a folio
number to an image. <https://www.masoretica.org/> is the other way, and covers 187
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

Two further facts about the same verse, from `../UXLC-utils-sparse/in/UXLC-39/Lamentations.xml`
rather than from the image: the verse has a meteg on בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus
the silluq on the verse-final סָבִֽיב׃. So the absence on אָכְלָ֖ה sits among three marks
present, not on a page sparing with them.

Codex Sassoon 1053 and Cambridge Add. 1753 have no meteg on this word either, both confirmed
the same day: `MAM-basics/doc/ms-snips/sassoon1053-p740-Lam2v3-akhla.png` for Sassoon 1053
page 740, and `codex-index-cam1753/page-snips/0105B-col2-Lam2v3-akhla.png` for Cambridge
Add. 1753 leaf 0105B column 2.

### Calibration note for the atom-location estimator

`MAM-basics/py/main_uxlc_estimate_atom_loc.py` put this word at folio 430B, column 2, line
12.9 — three lines low against the line 10 Ben read off the image:

```
{'page': '430B', 'fline-guess': '39.9', 'line-guess': '12.9', 'column-guess': 2}
```

The folio is right and the column is not independently confirmed: Ben's correction named the
line only, and the column is still the estimator's. Recorded here as one data point about how
close the estimate runs, not as a defect report.
