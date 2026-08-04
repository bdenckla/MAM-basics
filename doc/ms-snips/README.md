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
It agrees with the Leningrad Codex, whose crop and confirmation are at
`../../../codex-index-leningrad/page-snips/430B-col2-line10-Lam2v3-akhla.png`.

The two together answer a Sefaria correction request of 2026-07-22 that asked for
אָֽכְלָ֖ה rather than אָכְלָ֖ה. Sassoon 1053 matters here because it is one of the two
manuscripts MAM leans on throughout Lamentations: of the 38 נוסח notes in the book, ש1
appears in 16 and Cambridge Add. 1753 (ק-מ) in 24, while the Aleppo Codex is absent —
Lamentations is one of the books lost from it entirely, and the four notes that do invoke
the Keter do so at second hand through Yehoshua Kimḥi's record. MAM has no note at all on
אָכְלָ֖ה, and these two crops are why: nothing to report.

Cambridge Add. 1753 has not been looked at for this word.
