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
is for places MAM is making a call worth flagging, as at בׇּֽחֳרִי־אַ֗ף in this very verse.
So no edit to MAM's text would convey anything the text does not already convey.

What MAM's text does not speak to is the shewa. Phonetic MAM does, and agrees it is na:
`’a·kh(e)·la` at <https://bdenckla.github.io/phonetic-hbo/tnkh/E3-Lamentations/02.html>,
against `le·’okh·la` for Gen 1:29.

Nor is this verse's pointing simply sparing with meteg: the Leningrad Codex has one on
בָּֽחֳרִי and another on לֶֽהָבָ֔ה, plus the silluq on the verse-final סָבִֽיב׃.

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
<https://bdenckla.github.io/MAM-with-doc/misc/rocc_2_pre_vowel_accents_in_ctr.html>.
