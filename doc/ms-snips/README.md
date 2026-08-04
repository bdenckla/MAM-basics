# ms-snips

Crops of manuscript page images, kept as the evidence behind a stated fact about what a
manuscript MAM cites actually has. One file per fact, named
`<manuscript>-<page>-<ref>-<slug>.png`.

**Where a snip goes.** A manuscript with a repo of its own gets its snips there —
`../../../codex-index-leningrad/page-snips/`, `../../../codex-index-aleppo/`,
`../../../codex-index-cam1753/`. This folder is for the rest, which is why the Leningrad
half of the Lamentations 2:3 question below lives in the sibling repo rather than here.
MAM-basics is the fallback because it is where MAM's sigla are decoded — see
[sigil-decoding.md](../sigil-decoding.md).

## masoretica.org is how to find a page

<https://www.masoretica.org/> serves 187 manuscripts — Masoretic, Samaritan and Greek —
addressable straight to a verse:

```
https://www.masoretica.org/?book=Lamentations&chapter=2&verse=3&manuscript=sassoon
```

It gives the page and folio and, where the images are on the Internet Archive, the scan
number, so it turns "which page is this verse on" into one URL. It has the Leningrad Codex,
the Aleppo Codex and Codex Sassoon 1053 among others. Checked 2026-08-04: it does **not**
have Cambridge University Library MS Add. 1753, so the leaf hunt for that manuscript still
runs through `../../../codex-index-cam1753/`.

## sassoon1053-p740-Lam2v3-akhla.png

Lamentations 2:3, the word אָכְלָ֖ה, in **Codex Sassoon 1053 (MAM's ש1), page 740**, found
through the masoretica.org URL above.

**Sassoon 1053 has no meteg on this word** — confirmed by Ben from this image on 2026-08-04.
So do the other two manuscripts, confirmed the same day:
`../../../codex-index-leningrad/page-snips/430B-col2-line10-Lam2v3-akhla.png` for the
Leningrad Codex, and `../../../codex-index-cam1753/page-snips/0105B-col2-Lam2v3-akhla.png`
for Cambridge Add. 1753.

The three together answer a Sefaria correction request of 2026-07-22 that asked for
אָֽכְלָ֖ה rather than אָכְלָ֖ה. Sassoon 1053 matters here because it is one of the two
manuscripts MAM leans on throughout Lamentations: of the 38 נוסח notes in the book, ש1
appears in 16 and Cambridge Add. 1753 (ק-מ) in 24, while the Aleppo Codex is absent —
Lamentations is one of the books lost from it entirely, and the four notes that do invoke
the Keter do so at second hand through Yehoshua Kimḥi's record (`א(ק)`, decoded in
[sigil-decoding.md](../sigil-decoding.md)). MAM has no note at all on אָכְלָ֖ה, and these
three crops are why: nothing to report.

Mikraot Gedolot Haketer has no meteg here either — read out of `mgketer/out/E3-Lamentations/`,
codepoint-identical to MAM. Metsudah (Lakewood, 2001) has one, which is the printed tradition
doing what it does.

### MAM answers the qamats question without a meteg

The request asked for the meteg and reasoned from it that "both קמץ are קמץ גדול". MAM says
that second part outright, in the text rather than through a helper mark, because it
distinguishes the two qamats codepoints:

| | form | first qamats |
| --- | --- | --- |
| Lam 2:3, "consuming" | אָכְלָ֖ה | U+05B8 HEBREW POINT QAMATS |
| Gen 1:29, "for food" | לְאׇכְלָֽה׃ | U+05C7 HEBREW POINT QAMATS QATAN |

Both are base text in `MAM-parsed/plus/`, not a `מ:קמץ` template alternative — that template
is for places MAM is making a call worth flagging, as at בׇּֽחֳרִי־אַ֗ף in this very verse.
So no edit to MAM's text would convey anything the text does not already convey.

What MAM's text does not speak to is the shewa. Phonetic MAM does, and agrees it is na:
`’a·kh(e)·la` at <https://bdenckla.github.io/phonetic-hbo/tnkh/E3-Lamentations/02.html>,
against `le·’okh·la` for Gen 1:29.

Nor is this verse's pointing simply sparing with meteg: the Leningrad Codex has one on
בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus the silluq on the verse-final סָבִֽיב׃.
