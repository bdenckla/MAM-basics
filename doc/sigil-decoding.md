# Decoding the sigla in MAM's נוסח notes

MAM's textual notes — the second parameter of each `נוסח` template in MAM-parsed-plus — cite
manuscripts, editions and reference works by short sigla, in the shape `<sigla>=<reading> (<remark>)`,
e.g. `א(ס),ל=וּֽזֲהַ֛ב (חטף)`. This file decodes the sigla. It exists because `א(ס)` needed decoding
for the near-Aleppo work (2026-08-23) and the decoding was scattered: a 20-entry table in
`py/accgram/telg_doc_notes.py` (`_SOURCE_KEY`), four glosses in `py/accgram/ps17v14_mam_doc_notes_body.py`,
and otherwise only MAM's own introduction.

**Source of record:** MAM's introduction, appendix "רשימת מקורות (כתבי־יד, דפוסים ומחקרים)",
<https://he.wikisource.org/wiki/ויקיטקסט:מבוא_למקרא_על_פי_המסורה/נספחים>, read 2026-08-23. Every
definition below that gives a shelfmark or a date is that page's, condensed; where MAM's page defines a
siglum only by usage, the row says so. **Counts** are from `out/sigil-inventory.json`
(`py/main_sigil_inventory.py`, which scans 3,847 notes), `expression_tokens` — the number of notes in
which the token appears before an `=`. They are here to say which sigla matter, not as exact figures: the
inventory counts a leading `ו` ("and") as part of the token, so `ושיטת-א` (120) and `שיטת-א` (9) are one
siglum, and the count for a single letter such as `ה` includes some prose noise.

## The Aleppo Codex and the testimonies to its lost parts

| Siglum | Meaning | Notes |
|---|---|---|
| `א` | The Aleppo Codex itself (כתר ארם צובה, Ben-Zvi Institute 1), read from the photographs. Also written `הכתר` and `כתי"א` in prose. | 1,373 |
| `א(ו)` | Aleppo's reading in a lost section, per the notes of R. Shmuel **V**ital in the responsa *Be'er Mayim Ḥayyim* §27. | — |
| `א(ס)` | Aleppo's reading in a lost section, per the notes of Jacob **S**apir in *Me'orot Natan* (the second copy, in manuscript). | Appears mostly inside an angle-bracket query, `<א(ס)=חטף פתח? כן>` — "does Sapir record a hataf patah here? yes". 194 prose occurrences. |
| `א(ע)` | Aleppo's reading in a lost section, per the notes of Yishai **A**madi, as published in Yitzhak Penkower, *Nusaḥ ha-Torah be-Keter Aram Tsova: Edut Ḥadasha* (Bar-Ilan, 1993). | — |
| `א(ק)` | Aleppo's reading in a lost section, per the notes of Yehoshua **K**imḥi, as published in Yosef Ofer's article on the Aleppo Codex and the Tanakh of R. Shalom Shakhna Yellin. | — |
| `א(ר)` | Aleppo's reading in a lost section, per the **lists** (רשימות) of M. D. Cassuto, as published by Yosef Ofer; these carry the Torah's ketiv as recorded by R. Menashe Sathon on a slip pasted into the codex. | — |
| `א-צילום` | The photographs of a few Torah pages taken while the codex was complete (one page of Genesis, two of Deuteronomy with the Decalogue). | Also `א(צילום)`. |
| `א-כתיב` | Aleppo's ketiv — the form written in the body text, where it differs from the qere. | 64. E.g. Judges 19:3 `א-כתיב=לַהֲשִׁיבָ֔ו`. |
| `שיטת-א` | "Aleppo's practice": the reading that Aleppo's general habit implies, cited where the codex itself is lost. An inference from the codex's system, not a reading of it. | 129 |
| `מסורות-א` / `מסורת-א` | The masoretic notes (masora parva/magna) written in the Aleppo Codex, as distinct from its body text. | 63 |

For the near-Aleppo work: `א`, `א-צילום` and `א-כתיב` are readings of the codex; `א(ו)`, `א(ס)`, `א(ע)`,
`א(ק)` and `א(ר)` are testimony to what the lost parts once read, and count as Aleppo; `שיטת-א` is an
inference and `מסורות-א` is the codex's margin, not its text.

## The Leningrad Codex and the other Tiberian-type manuscripts

| Siglum | Meaning | Notes |
|---|---|---|
| `ל` | The Leningrad Codex (St Petersburg, Russian National Library, EVR I B 19a). Written `כתי"ל` in prose. `ל!` marks a reading of Leningrad's that surprised the editors; `ל?` an uncertain one. | 1,144 |
| `ל1` | St Petersburg, Firkovich B 17 (Yeivin's ל¹): Torah, written 930 by Solomon ben Buya'a, the scribe of the Aleppo Codex's letters. | 566 |
| `ל3` | St Petersburg EVR II B 10 (Tanis, 946; Babylonian masora): most of the Torah from Genesis 11. | 194 |
| `ל9` | St Petersburg EVR II B 59 (1022): Torah, with gaps. | 143 |
| `ל-מ` | The Lehmann manuscript (Breuer's ל^מ), formerly #14 of the Karaite synagogue in Cairo: Torah, written by Samuel ben Jacob, the scribe of the Leningrad Codex. Often cited "ע"פ עדותו של ברויאר", i.e. from Breuer's report of it. | 46 |
| `ל-א` | St Petersburg EVR II B 55, formerly B 247 (Yeivin's ל^א): Prophets and Writings, close to Aleppo and covering much of what Aleppo lacks there. | — |
| `ש` | The Damascus Keter, Sassoon 507 (National Library of Israel 24°5702; Breuer's ש): Torah from Genesis 9:26. 10th century. | 702 |
| `ש1` | Sassoon 1053 (Yeivin's ש1, Breuer's שׂ): a complete Tanakh, early 10th century. | 1,019 |
| `ש2` | "Keter Shem Tov", an exact Sephardic Tanakh manuscript close to the Tiberian masora. | 82 |
| `ק` | The Cairo Codex of the Prophets. | 130 |
| `ק2` | Cairo 27: Former Prophets, written by Samuel ben Jacob; rarely cited. | — |
| `ק3` | Cairo 18: Torah, 10th century, corrected by Mishael ben Uzziel (author of the *Book of Differences*), very close to Aleppo. | 705 |
| `ק13` | Cairo 13: Writings, written 1028 by Zechariah ben Anan; complete. | 63 |
| `ק25` | Cairo 25: Latter Prophets, c. 11th century; rarely cited. | — |
| `ק-מ` | Cambridge Add. 1753 (Breuer's ק^מ): Writings, an exact Yemenite manuscript in Tiberian book order. The codex-index-cam1753 repo indexes this manuscript. | 336 |
| `ב` | London, British Library Or 4445 (Ginsburg's א, Breuer's ב): Torah, late 9th century. | 403 |
| `ב1` | British Library Or 2210 + Or 2211 (Prophets) and Or 2375 (Writings): exact Yemenite manuscripts by Benaya the scribe. | 241 |
| `ו` | Museum of the Bible, Washington, Ms. 882: Torah, 11th century, Tiberian. Written `כתי"ו` in prose. (`telg_doc_notes.py` left this one undecoded; this is it.) | 586 |
| `ה` | "Codex Hilleli", `כתי"ה`: a Sephardic manuscript. | 41 (includes noise) |
| `ט3` | Tbilisi 3, the "Lailashi Keter": Torah, 10th–11th century, close to Aleppo. Listed as not used in establishing the text. | 1 |
| `ג` | British Library Or 9879, the first Gaster manuscript (`גסטר1` in `ps17v14_mam_doc_notes_body.py`): fragments of the Writings, Egypt, 10th century. | 3 |
| `ת451` | The former Meir Benayahu manuscript ת 451: Writings, an exact Yemenite manuscript by Yosef ben Benaya. | 6 |
| `פטרבורג-EVR-II-B-8`, `-B-80`, `-B-92`, `-B-34`, `-C-1`, `ותיקן-448`, `פריז 25`, `תנ"ך ליסבון`, `טולדו` | Further manuscripts, cited by shelfmark or common name rather than a siglum; MAM's appendix describes each. | — |
| `תיגאן` / `תאג'` | The Yemenite manuscripts generally (the Taj tradition); `תאג' חבשוש` and `תאג' דפוס ראשון` are two named ones. | 42 |
| `טברניות` / `מסורת טברנית` | The Tiberian manuscripts generally, or the Tiberian masora. | 101 |
| `מסורת-ל` | The masoretic notes written in the Leningrad Codex, as distinct from its body text. | 115 |
| `ב"א` / `ב"נ` | Ben Asher / Ben Naphtali, as reported in Mishael ben Uzziel's *Book of Differences* (`חילופי מישאל`). | — |

## Masoretic literature and modern scholarship

| Siglum | Meaning | Notes |
|---|---|---|
| `מ"ש` | *Minḥat Shai* (Yedidya Norzi), consulted throughout. | 69 |
| `רמ"ה` | R. Meir ha-Levi Abulafia, *Masoret Seyag la-Torah*. | 78 |
| `ייבין` | Israel Yeivin, above all *The Aleppo Codex: Its Vocalization and Accentuation* (כתר ארם צובה: ניקודו וטעמיו). | — |
| `ברויאר` | R. Mordechai Breuer — his writings, lists and three editions (Mossad Harav Kook 1989; Ḥorev 1997; Keter Yerushalayim 2000). `רשימת ברויאר ב"ספיקות שאין להם הכרע"` is his list of undecidable doubts, cited with a note number. `הערת ברויאר` closes a note taken from him. | 152 + 59 for the list |
| `דותן` | Aharon Dotan's editions of Leningrad (Adi 1986; *Biblia Hebraica Leningradensia* 2001/2003) and his lists of its readings. | 34 |
| `גינצבורג` | Christian D. Ginsburg's *Massorah* and his edition of the Bible. | — |
| `ויינברג`, `אריאל`, `לאופר`, `דוידזון` | Sources for qamats qatan: Weinberg's JBL article (the principal one), Ḥanan Ariel, Asher Laufer, Davidson's lexicon. | — |

## Editions

| Siglum | Meaning | Notes |
|---|---|---|
| `מג"ה` | *Miqra'ot Gedolot ha-Keter*, ed. Menachem Cohen (Bar-Ilan). | 34 |
| `מכון ממרא` | Mechon Mamre's online text (based on Breuer). | — |
| `סימנים` | *Tanakh Simanim* (Feldheim 2008), partly based on Aleppo. | — |
| `BHS` | *Biblia Hebraica Stuttgartensia* 1984. | — |
| `הקלדה` / `המקליד` | The Westminster transcription of Leningrad, now UXLC; `המקליד` is its transcriber, cited for his notes. | — |
| `מ"ג` | The second Venice *Miqra'ot Gedolot* (1524–26; Breuer's ד). `מ"ג דפוס ורשה`, `מ"ג דפוס נעטטער` are later *Miqra'ot Gedolot* printings. | — |
| `דפוסים` | The common printed editions of the 19th–early 20th century, named individually as `היידנהיים`, `ליסר`, `לטריס`, `במברגר`, `בר-דליטש`, `גינצבורג`. | 218 + 101 |
| `קורן` | The Koren Tanakh (Jerusalem 1962). | 34 |

## Marks on a siglum

`!` after a siglum: the reading surprised the editors (`ל!`, `א!`). `?` after a siglum: the reading is
uncertain, usually because the photograph is unclear (`ל?`, `ק3?`). `(צילום)` after `א`: read from the
old photographs. A leading `=` with no siglum before it, as in `=ל1,ש,ק3 (אין חטף)`, introduces the
reading MAM itself adopts, and the sigla after it are the witnesses for it.
