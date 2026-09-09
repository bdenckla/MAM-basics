# Meteg after silluq: what MAM's documentation and the secondary literature name

**The documentation names no further case. The one verse-final chanted word it names with a meteg after the silluq is the one already known, 1 Kings 7:37 לְכֻלָּֽהְנָֽה, and every other place the documentation brings near it is a different phenomenon.** Searched 2026-09-09 in the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583` (branch `claude/meteg-after-silluq-mam-9555f5`, HEAD `30fb7681`), as task A of a three-way investigation; the two sibling tasks screen MAM against UXLC and WLC and build a Koren lookup list, and nothing here duplicates them. Ben Denckla set the question and the four sources on 2026-09-09; the classifications below are Claude's, by the rules stated at each finding.

Four sources were searched, and the figures are the ones the scripts in the last section print:

1. MAM's source wikitext, `in/mam-ws/*.json`: 23,283 verse segments parsed (23,202 distinct verses, every verse MAM-simple has), holding 16,665 top-level template calls, of which 3,601 are the documentation template `נוסח` and 35 more are `נוסח` calls wrapping a verse header with a seder note. Every template call was searched, not only `נוסח`, so the ketiv-qere, qamats-variant and dual-cantillation templates are covered too.
2. The parsed doc-note index `C:/Users/BenDe/GitRepos/MAM-private/al-hatorah/io/a06-mam-doc-notes.json` (3,856 notes), used as a cross-check of the wikitext scan, not as a source.
3. The MAM introduction mirror, all thirteen pages of `in/mam-ws-intro/*.mediawiki`, at the revisions `in/mam-ws-intro/manifest.json` records.
4. Breuer, *The Cantillation of Scripture*, chapter 8 (the ga'aya chapter), and Yeivin, *Introduction to the Tiberian Masorah*, the ga'ya run of sections 309–357, both from the OCR exports under `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/`, with every verse either book names as having a ga'ya after the accent looked up in MAM.

A note on vocabulary. This file says **meteg** in its voice and **ga'ya** or **ga'aya** where it reports Yeivin or Breuer, and it quotes MAM's term `געיה` where it quotes a doc-note; the three names are one mark, U+05BD, which also serves as the silluq. "Silluq" here always means the U+05BD on the stressed syllable of a verse-final chanted word, and "meteg after silluq" a further U+05BD later in that chanted word.

## Finding 1 — NOT FOUND among the doc-notes that mention silluq: 31 template calls in 29 verses, one of them the known case

The string `סילוק` occurs in 29 lines of `in/mam-ws`, all of them verse lines, holding 31 template calls that mention it (two verses, Exodus 20:12 and Deuteronomy 5:16, hold two each). The a06 index flags the same 29 verses and no other (`.novc/mas_a_compare_a06_ws_report.txt`). Each call is classified below; only 1 Kings 7:37 is the phenomenon. Reading the notes rather than the marks matters here: eleven of them concern a silluq that one manuscript or one typing LACKS, six concern a silluq that one manuscript has on ANOTHER syllable, and five concern the Decalogue's dual cantillation, where the עליון's silluq shares a letter with an accent of the תחתון — none of which puts a second U+05BD after a silluq.

| # | Reference | Template | Target | Note | Classification |
|---|---|---|---|---|---|
| 1 | A1-Genesis בראשית 32:24 | `נוסח` | אֶת־אֲשֶׁר־לֽוֹ | 2==ש,ק3,ו וכמו כן בתיגאן ובדפוסים / ל!=אֶת־אֲשֶׁר־לוֹ (חסר סילוק באות למ"ד) / הערות דותן וברויאר (במהדורתו האחרונה) והמקליד | different: L lacks the silluq (one U+05BD at issue) |
| 2 | A2-Exodus שמות 20:12 | `מ:כפול` | כפול=לֹ֥֖א {{נוסח\|תִּֿרְצָ֖{{מ:טעם ומתג באות אחת}}ח\|2==ל,ל1,ב,ש,ש1,ק3,ו (באות צד"י נכתבו קמץ לטעם התחתון והעליון כאחד, טפחא לטעם התחתון וסילוק לטעם העליון) / מ"ש ובדפוסים=תִּֿרְצַ֖+צָֽח (תִּֿרְצַ֖͏ָֽח) (פתח וטפחא לטעם התחתון, קמץ וסילוק לטעם העליון) וכך בקורן. / את סימן הרפה השאירו כאן, ליתר בהירות (וכמו כן ב"תנאף" ו"תגנב"), אף במהדורות שנוהגות בדרך כלל להשמיט אותו, וביניהם BHS ומהדורת ברויאר}}׃ | א=לֹ֥א תִרְצָ֖ח ב=לֹ֖א תִּרְצָֽח׃ | different: dual cantillation of the Decalogue, the עליון's silluq and the תחתון's tipcha on one letter |
| 3 | A2-Exodus שמות 20:12 | `מ:כפול` | כפול=לֹ֣֖א {{נוסח\|תִּֿנְאָ֑{{מ:טעם ומתג באות אחת}}ף\|2==ל,ל1,ש,ש1,ק3,ו (אתנח לטעם התחתון וסילוק לטעם העליון). האתנח נכתב מתחת לסילוק בכתי"ל, אבל קצת לימינו. בכתי"ב הסילוק בדיוק למטה מהאתנח. בשאר כתבי־היד האתנח קודם לסילוק באופן ברור.}}׃ | א=לֹ֣א תִנְאָ֑ף ב=לֹ֖א תִּנְאָֽף׃ | different: dual cantillation, the עליון's silluq and the תחתון's atnach on one letter |
| 4 | A2-Exodus שמות 32:17 | `נוסח` | בַּֽמַּחֲנֶֽה | 2==ל1,ב,ש,ש1,ק3,ו ובדפוסים / ל!=בַּֽמַּחֲנֶה (חסר סילוק) / הערות דותן והמקליד | different: L lacks the silluq; the target's other U+05BD is a meteg before the stress |
| 5 | A3-Levit ויקרא 4:17 | `נוסח` | אֵ֖ת פְּנֵ֥י הַפָּרֹֽכֶת | 2==ל,ל1,ב,ש,ש1,ק3,ו (טפחא ומרכא וסילוק) / דפוסים=אֵֽת־פְּנֵ֖י הַפָּרֹֽכֶת (תיבה מוקפת בגעיה וטפחא, וסילוק) | unrelated: printed editions have a maqaf compound with a ga'ya where MAM has tipcha and merkha |
| 6 | A3-Levit ויקרא 26:28 | `נוסח` | עַל־חַטֹּאתֵיכֶֽם | 2==ל1,ש,ש1?,ק3,ו / ל!,ב!=עַל־חַטֹּאתֵיכֶם (חסר סילוק) / ש=חַטֹּֽאתֵיכֶֽם (געיה וסילוק) וכן בדפוסים / הערות דותן והמקליד | different: L and B lack the silluq; ש has a meteg before the stress and the silluq |
| 7 | A4-Numbers במדבר 1:10 | `נוסח` | בֶּן־פְּדָהצֽוּר | 2==ל,ב,ש1,ק3 ומסורת טברנית וספרי התורה בכל העדות ("פדהצור" תיבה אחת); בכל כתבי־היד האלה אין מקף ואין שווא מתחת לאות ה"א, אך מכיוון שאין טעם עצמאי ב"בֶּן־פְּדָה" יוצא שהיא נסכמת אל הסילוק ב"צֽוּר". והשווה להלן בפרשת נשֹא (ז,נד; ז,נט) ובהערות הנוסח שם. / ל1,ש,ו=<בֶּן־פְּדָה־צֽוּר> ("פדה צור" בשתי תיבות מוקפות) | unrelated: one atom against two maqaf-joined atoms; the silluq is named only as the compound's accent |
| 8 | A4-Numbers במדבר 2:25 | `נוסח` | בֶּן־עַמִּֽישַׁדָּֽי | 2==ל,ש,ש1 ובדפוסים (געיה וסילוק) / מ"ג דפוס ונציה=<בֶּן־עַמִּ֥ישַׁדָּֽי> (מרכא וסילוק), וברויאר ציין בספק מרכא באופן דומה בכתי"ל; אמנם הקו ישר בכתב־היד ונראה שהוא געיה, וכך דעתם של דותן והמקליד. / ל1,ב,ק3[מחיקה?],ו=בֶּן־עַמִּישַׁדָּֽי (אין געיה) | different: a meteg before the stress and the silluq, read as merkha in one printing |
| 9 | A4-Numbers במדבר 27:9 | `נוסח` | לְאֶחָֽיו | 2==ל1,ב,ש,ש1,ק3,ל3 וכמו כן בדפוסים וקורן / ל!=לְאֶחָיו (חסר סילוק) / הערות ברויאר והמקליד | different: L lacks the silluq |
| 10 | A4-Numbers במדבר 30:2 | `נוסח` | יְהֹוָֽה | 2==ל / הקלדה=יְהֹוָה (המקליד השמיט את הסילוק בטעות בגירסאות הראשונות). | different: an early typing lacked the silluq |
| 11 | A5-Deuter דברים 5:6 | `מ:כפול` | כפול={{נוסח\|לֹ֣א־יִהְיֶ֥{{מ:טעם ומתג באות אחת}}ה־לְךָ֛֩\|2==ש,ש1,ק3,ו וכמו כן בדפוסים / ל!,ל1?,ל3=<לֹ֣א יִהְיֶ֥ה־לְךָ֛֩> (חסר מקף אחרי "לא" לטעם התחתון); וכמו כן נראה בצילום כתר ארם צובה חסר בסוף השורה אבל קשה להבחין. בכתבי־היד ל1,ק3,ו,פטרבורג-EVR-II-B-8 יש געיה באות יו"ד הראשונה.}} אֱלֹהִ֥֨ים אֲחֵרִ֖֜ים {{נוסח\|עַל־פָּנָֽ{{שני טעמים באות אחת קמץ-תחתון-פתח-עליון\|{{מ:טעם\|נ֗}}}}י\|2==א?,ל?,ל1,ש,ש1,ו,ל3,פטרבורג-EVR-II-B-8 (קמץ וסילוק לטעם התחתון לפני פתח לטעם העליון) / בכתי"ק3 קמץ ופתח וסילוק.}}׃ | א=לֹא־יִהְיֶ֥ה לְךָ֛ אֱלֹהִ֥ים אֲחֵרִ֖ים עַל־פָּנָֽי׃ ב=לֹ֣א יִהְיֶֽה־לְךָ֩ אֱלֹהִ֨ים אֲחֵרִ֜ים עַל־פָּנַ֗י | different: dual cantillation, the תחתון's qamats and silluq before the עליון's patah and revia on one letter |
| 12 | A5-Deuter דברים 5:16 | `מ:כפול` | כפול=לֹ֥֖א {{נוסח\|תִּֿרְצָ֖{{מ:טעם ומתג באות אחת}}ח\|2==א(צילום),ל1,ש,ש1,ק3,ו,ל3[טפחא וקמץ וסילוק],פטרבורג-EVR-II-B-8 (קמץ וטפחא וסילוק בצד"י) / ל=תִּֿרְצָֽח (חסר טפחא לטעם התחתון); לפי ברויאר הקו המאונך תחת האות צד"י משמש בכתי"ל כטפחא וסילוק כאחד. / הערות דותן וברויאר}}׃ | א=לֹ֥א תִרְצָ֖ח ב=לֹ֖א תִּרְצָֽח׃ | different: dual cantillation, tipcha and silluq on one letter; L has one stroke for both |
| 13 | A5-Deuter דברים 5:16 | `מ:כפול` | כפול=וְלֹ֣֖א {{נוסח\|תִּֿנְאָ֑{{מ:טעם ומתג באות אחת}}ף\|2==א(צילום)?,ל1,ש,ש1,ק3,ו,ל3,פטרבורג-EVR-II-B-8 (אתנח וסילוק) וכמו כן בדפוסים / ל!=תִּֿנְאָֽ֑ף (בסדר הפוך: סילוק ואתנח) / הערות דותן וברויאר}}׃ | א=וְלֹ֣א תִנְאָ֑ף ב=וְלֹ֖א תִּנְאָֽף׃ | different: dual cantillation, atnach and silluq on one letter, L in the reverse order |
| 14 | A5-Deuter דברים 10:15 | `נוסח` | הַזֶּֽה | 2==ל1,ש,ש1,ק3,ו?,ל3,ל9 וכמו כן בדפוסים וקורן / ל!=הַזֶּה (חסר סילוק) / הערות דותן והמקליד | different: L lacks the silluq |
| 15 | A5-Deuter דברים 12:2 | `נוסח` | רַעֲנָֽן | 2==ל1,ש,ש1,ק3,ו,ל3,ל9 וכמו כן בדפוסים וקורן / ל!=רַעֲנָן (חסר סילוק) / הערת המקליד | different: L lacks the silluq |
| 16 | A5-Deuter דברים 23:12 | `נוסח` | הַֽמַּחֲנֶֽה | 2==ל1,ש,ש1,ק3,ו,ל3,ל9 / ל!=הַֽמַּחֲנֶה (חסר סילוק) / הערות דותן והמקליד | different: L lacks the silluq; the target's other U+05BD is a meteg before the stress |
| 17 | A5-Deuter דברים 23:18 | `נוסח` | יִשְׂרָאֵֽל | 2==ל1,ש,ש1,ק3,ו,ל3,ל9 / ל!=יִשְׂרָאֵל (חסר סילוק) / הערות דותן והמקליד | different: L lacks the silluq |
| 18 | BC-1Kings מלכים א 7:37 | `נוסח` | לְכֻלָּֽהְנָֽה | 2==א (קווים לסילוק וגעיה), וכך אצל ברויאר ומג"ה / ל=לְכֻלָּֽהְנָה (קו אחד לסילוק בלבד), וכן הוא בדפוסים וקורן וסימנים ומכון ממרא | THE PHENOMENON: A has two strokes, silluq then ga'ya; L, the printed editions, Koren, the Simanim Tiqqun and Mechon Mamre have the silluq alone |
| 19 | C1-Isaiah ישעיהו 40:7 | `נוסח` | אָכֵ֥ן חָצִ֖יר הָעָֽם | 2==א,ל (מרכא וטפחא וסילוק) וכן הוא במ"ג דפוס ונציה / בחלק מהדפוסים וקורן=<אָכֵ֖ן חָצִ֥יר הָעָֽם> (טפחא ומרכא וסילוק) ובעקבותיהם גם במהדורת סימנים (נגד הכתר!) בהסתמך על ההפטרה שבחומשים לפי ר' וולף היידנהיים. | unrelated: the order of merkha and tipcha before the silluq |
| 20 | C2-Jeremiah ירמיהו 48:22 | `נוסח` | דִּבְלָתָֽיִם | 2=א=דִּבְלָתָ֛יִם? (יש נקודה או כתם והטעם נראה בגללו כמו טעם תביר במקום סילוק) | unrelated: a spot beside A's silluq makes it look like tevir |
| 21 | CD-Obadiah עובדיה 1:16 | `נוסח` | הָיֽוּ | 2==ק ובדפוסים / ל!=הָֽיוּ (מקום הסילוק) לפי ברויאר, ונראה שהצדק עמו. | different: L has its one U+05BD on another syllable (silluq position) |
| 22 | CD-Obadiah עובדיה 1:17 | `נוסח` | מוֹרָֽשֵׁיהֶֽם | 2=ל!=מוֹרָֽשֵׁיהֶם (חסר סילוק) / הערת המקליד | different: L lacks the silluq; the target's other U+05BD is a meteg before the stress |
| 23 | D1-Psalms תהלים 15:2 | `נוסח` | בִּלְבָבֽוֹ | 2==ש1,גסטר1,ק-מ / ל!=בִּלְבָֽבוֹ (מקום הסילוק) והשוו "קְרֹבֽוֹ" בפסוק הבא / הערות ברויאר ודותן | different: L has its one U+05BD on another syllable (silluq position) |
| 24 | D1-Psalms תהלים 15:3 | `נוסח` | עַל־קְרֹבֽוֹ | 2==ש1,ק13,גסטר1,ק-מ / ל!=עַל־קְרֹֽבוֹ (מקום הסילוק) / הערות ברויאר ודותן, וראו גם "בִּלְבָבֽוֹ" בפסוק הקודם. | different: L has its one U+05BD on another syllable (silluq position) |
| 25 | D1-Psalms תהלים 17:14 | `נוסח` | לְעוֹלְלֵיהֶֽם | 2==ש1?,ק-מ (מקום הסילוק) / גסטר1=לְעֽוֹלְלֵיהֶֽם (געיה וסילוק) / ל!=לְעוֹלְלֵֽיהֶם (מקום הסילוק) אבל המקליד ציין סילוק ימני באות ה"א דווקא (!) / הערות ברויאר ודותן | different: L has its one U+05BD on another syllable; the manuscript MAM's sigla call גסטר1 has a meteg before the stress and the silluq |
| 26 | D1-Psalms תהלים 18:10 | `נוסח` | רַגְלָֽיו | 2=ל=רַגְלָֽיו בסילוק ימני (!); בשאר כתבי־היד (ש1,ק13,גסטר1) נכתב הסילוק כרגיל. / הערת דותן וכן בהקלדה | unrelated: L has its silluq to the right of the vowel (glyph placement) |
| 27 | D1-Psalms תהלים 19:7 | `נוסח` | מֵחַמָּתֽוֹ | 2==ש1 / ל!=מֵֽחַמָּתוֹ (מקום הסילוק, או געיה וחסר סילוק לאחריה) / הערות ברויאר ודותן והמקליד | different: L has one U+05BD on the first syllable, read either as the silluq misplaced or as a meteg with the silluq lacking |
| 28 | D1-Psalms תהלים 25:22 | `נוסח` | צָרוֹתָֽיו | 2==א,ש1 (אין געיה) / ל!=צָֽרוֹתָיו (געיה וחסר סילוק) / הערות ברויאר ודותן והמקליד | different: L has a meteg and lacks the silluq |
| 29 | D1-Psalms תהלים 98:8 | `נוסח` | יְרַנֵּֽנוּ | 2==ל / א!=יְרַנֵּנֽוּ (מקום הסילוק) | different: A has its one U+05BD on another syllable (silluq position) |
| 30 | D1-Psalms תהלים 147:8 | `נוסח` | {{ר0}} | 2=לפי הטעם המפסיק יש לחלק כאן; אך המונח לקראת סוף הפסוק ("הָרִ֣ים") בא במקום רביע מוגרש ולכן ברויאר חילק שם. אמנם הקיצור בסוף הפסוק (תיבה קצרה אחת בלבד אחרי התיבה שראוי להיות בה רביע מוגרש) מכתיב את הטעמים הקיימים, וכך קוראים בפועל: טעם מפסיק מחלק כאן את השורה הראשונה, שהיא קצת יותר ארוכה ומורכבת מהשורה האחרונה, ובשורה האחרונה יש רק טעמים מחברים לפני סילוק. חילקנו לפני הקריאה בפועל. | unrelated: line division of a poetic verse |
| 31 | D2-Proverbs משלי 6:16 | `נוסח` | נַפְשֽׁוֹ | 2==א,ל,ק13 ובדפוסים (סילוק באות שי"ן) / בכתר יש נקודה לשמאלו של קו הסילוק מתחת לאות שי"ן (כאילו נקודת תביר), אבל לפי צבעה מדובר על כתם בלבד (ניתן להבחין בצבע בתוך הצילום באיכות גבוהה). | unrelated: a spot beside A's silluq |

The 1 Kings 7:37 note in full, from `in/mam-ws/BC-1Kings.json` line 353: the target is לְכֻלָּֽהְנָֽה and the note reads `=א (קווים לסילוק וגעיה), וכך אצל ברויאר ומג"ה` then `ל=` לְכֻלָּֽהְנָה `(קו אחד לסילוק בלבד), וכן הוא בדפוסים וקורן וסימנים ומכון ממרא`. So MAM's documentation itself names the two marks in their written order, silluq then ga'ya, attributes the two-stroke form to the Aleppo Codex, Breuer and Mikra'ot Gedolot ha-Keter, and the one-stroke form to L, the printed editions, Koren, the Simanim Tiqqun and Mechon Mamre. "L has" here is MAM's note's statement about the manuscript, not a reading of it made for this file.

## Finding 2 — NOT FOUND among the verse-final template calls with a meteg keyword or a two-U+05BD form: 166 calls, 111 of them holding such a form

A template call counts as verse-final when nothing but sof pasuq, tags and end-of-verse templates follows it on the verse line (the scan's `classify_after`). 166 verse-final calls mention `געיה`, `געיות`, `קווים`, `קו`, `מתג` or `סילוק`, or hold a chanted word with two or more U+05BD in the target or in a quoted alternative. Sorted by what the note is about (first matching category wins; the test for each is in `.novc/mas_a_write_doc.py`):

- 32: ketiv and qere
- 31: a hataf against a sheva after a meteg
- 23: L has a ga'ya to the right of its vowel (glyph placement)
- 16: a maqaf compound with a ga'ya against an accented atom
- 14: other
- 12: a ga'ya present or absent, or its letter, in one manuscript
- 12: a silluq lacking in one manuscript or typing
- 10: qamats variant
- 6: two ga'yot before the stress in one manuscript or printing
- 5: dual cantillation of the Decalogue
- 5: the silluq on another syllable in one manuscript

The 111 calls holding a two-U+05BD chanted word were then classified by syllable: 149 distinct strings, each matched to its Phonetic MAM entry (`C:/Users/BenDe/GitRepos/MAM-private/al-hatorah/io/a01-phonetic-std-set/`) and parsed with the post-stress-meteg survey's `_parse` (`py/accgram/post_stress_meteg.py`), so that each U+05BD gets a syllable index. **Phonetic MAM is no oracle for the question**: for 1 Kings 7:37 its `jta` is `l^.khul.lah.!na`, the stress on the ultima, so it reads the last U+05BD of a verse-final chanted word as the silluq by construction, and every one of the 122 parsed verse-final strings duly came back "silluq last". What the parse does give is adjacency, and the basis of the adjacency test is measured, relative to Phonetic MAM, not assumed.

`.novc/mas_a_stress_after_census.py` counts, over all 263,320 chanted words of Phonetic MAM, the syllables after the stressed syllable within the stressed atom, under Ben's syllable definition (Ben Denckla, 2026-09-09): a vocal sheva by either notation, a simple sheva or a xataf, is not a syllable and attaches to the syllable that follows it, and a furtive patax is a syllable of its own. The count is 0 in 209,262 chanted words, 1 in 54,046 and 2 in 12, never 3 or more; over the 23,265 chanted words whose form has sof pasuq it is 0 in 17,270 and 1 in 5,995, never 2. Each of the 12 chanted words with two syllables after the stress either stands before a chanted word that Phonetic MAM stresses on its first syllable, the shape of stress retraction, or has a dexi on the letter Phonetic MAM marks as stressed, a dexi read as the stress; none is verse-final:

1. Exodus 15:8 נֶ֣עֶרְמוּ, before מַ֔יִם
2. Deuteronomy 33:28 יַ֥עַרְפוּ, before טָֽל
3. 2 Samuel 5:21 וַיַּ֥עַזְבוּ, before שָׁ֖ם
4. Isaiah 40:18 תַּ֥עַרְכוּ, before לֽוֹ
5. Isaiah 50:8 נַ֣עַמְדָה, before יָּ֑חַד
6. Isaiah 63:12 בּ֤וֹקֵֽעַ, before מַ֙יִם֙
7. Psalms 4:3 לִ֭כְלִמָּה, a dexi on the stressed letter
8. Psalms 71:9 אַֽל־תַּ֭שְׁלִ֭יכֵנִי, a dexi on the stressed letter, before לְעֵ֣ת
9. Proverbs 1:19 כׇּל־בֹּ֣צֵֽעַ, before בָּ֑צַע
10. Proverbs 11:26 מֹ֣נֵֽעַ, before בָּ֭ר
11. Job 5:10 וְשֹׁ֥לֵֽחַ, before מַ֝֗יִם
12. 1 Chronicles 14:12 וַיַּ֥עַזְבוּ, before שָׁ֖ם

So, relative to Phonetic MAM, a verse-final silluq sits on the last syllable or the one before it, and a meteg after it can only sit on the last syllable, with the silluq on the one before: the last two U+05BD must be on adjacent syllables, the last on the ultima. Until 2026-09-09 this step asserted that placement a priori and counted syllables as the `jta` does, a sheva syllable and a xataf syllable each counting as one; Ben overruled the assertion and rejected that count on 2026-09-09. `.novc/mas_a_stress_classify.py` applies Ben's definition to the `jta`'s notation — a syllable holding `^` or a xataf vowel is counted with the syllable after it, and so is a U+05BD on a sheva letter where the `jta` has a `^` syllable — and keeps the earlier count beside it.

Under Ben's definition 10 strings have the shape: the 6 the earlier count found and 4 it had ranked as not adjacent, marked in the column "Under the earlier `jta` count". The stress of each was judged morphologically (Claude, 2026-09-09); no candidate of the earlier count was dropped:

| # | Reference | String | MAM's chanted word | Phonetic MAM `jta` | Under the earlier `jta` count | Judgment |
|---|---|---|---|---|---|---|
| 1 | A1-Genesis בראשית 6:20 | לְהַֽחֲיֽוֹת | לְהַֽחֲיֽוֹת | `l^.ha.x8.!yOt` | not adjacent: a xataf syllable stood between the two U+05BD | an infinitive stressed on the ultima, so the silluq is the last U+05BD and the meteg on the first syllable stands before it |
| 2 | A1-Genesis בראשית 10:22 | וַֽאֲרָֽם | וַֽאֲרָֽם | `va.'8.!ram` | not adjacent: a xataf syllable stood between the two U+05BD | stressed on the ultima, so the silluq is the last U+05BD and the meteg on the first syllable stands before it |
| 3 | A1-Genesis בראשית 11:6 | לַֽעֲשֽׂוֹת | לַֽעֲשֽׂוֹת | `` la.`8.!sOt `` | not adjacent: a xataf syllable stood between the two U+05BD | an infinitive stressed on the ultima, so the silluq is the last U+05BD and the meteg on the first syllable stands before it |
| 4 | A4-Numbers במדבר 5:18 | הַמְאָֽרֲרִֽים | הַמְאָֽרְﬞרִֽים | `ham.'a.r^.!rIm` | adjacent, as here | stressed on the plural ending, so the silluq is the last U+05BD and the meteg on the second syllable stands before it |
| 5 | B1-Joshua יהושע 14:7 | עִם־לְֽבָבִֽי | עִם־לְבָבִֽי | `` `im-l^.va.!vI `` | not adjacent: the meteg on a vocal sheva was counted with the syllable before it | MAM's note's doubtful reading of the Aleppo Codex (ink under the lamed, left of the sheva), adopted in Mikra'ot Gedolot ha-Keter's print and not in its digital edition; the compound's last atom is stressed on the suffix, so the silluq is the last U+05BD and the meteg on the vocal sheva stands before it |
| 6 | BC-1Kings מלכים א 7:37 | לְכֻלָּֽהְנָֽה | לְכֻלָּֽהְנָֽה | `l^.khul.lah.!na` | adjacent, as here | stressed on the penult (the 3fp ending), so the silluq is the first U+05BD and the second, on the ultima, follows it: THE PHENOMENON |
| 7 | D1-Psalms תהלים 12:6 | יָפִ֥יחַֽ־לֽוֹ | יָפִ֥יחַֽ־לֽוֹ | `ya.fI.ax-!lO` | adjacent, as here | a maqaf compound whose silluq is on its last atom; the meteg on the furtive patah of the first atom stands before it (Yeivin ITM section 354, with the maqaf of section 357) |
| 8 | D1-Psalms תהלים 27:11 | שֽׁוֹרֲרָֽי | שֽׁוֹרְﬞרָֽי | `shO.r^.!ray` | adjacent, as here | stressed on the suffix, so the silluq is the last U+05BD and A's meteg before the hataf stands before it |
| 9 | D1-Psalms תהלים 60:9 | מְחֹֽקֲקִֽי | מְחֹֽקְﬞקִֽי | `m^.xO.k^.!kI` | adjacent, as here | stressed on the suffix, so the silluq is the last U+05BD and A's meteg before the hataf stands before it |
| 10 | FB-Nehemiah נחמיה 7:52 | נְפִֽישְׁסִֽים | נְפִֽישְׁסִֽים | `n^.fI.sh^.!sIm` | adjacent, as here | the qere, stressed on the plural ending, so the silluq is the last U+05BD and the meteg on the first syllable stands before it |

26 strings could not be parsed against Phonetic MAM (a quoted alternative whose syllable count differs from MAM's form, a compound MAM does not have, or the Name). Each was judged by eye under Ben's definition; none has two U+05BD on adjacent syllables with the last on the ultima of a penultimately stressed chanted word, and the re-reading of 2026-09-09 changed no verdict: in every string but Lamentations 5:5 הֽוּנַֽח a full-vowel syllable stands between the last two U+05BD (the Name counted as read), and הֽוּנַֽח is the first atom of a compound whose silluq is on the last atom:

| # | Reference | String | Why the parse failed | Judgment |
|---|---|---|---|---|
| 1 | A1-Genesis בראשית 2:6 | אֶֽת־כָּל־פְּנֵֽי־הָֽאֲדָמָֽה | parse failed: 4 jta syllables against 7 Hebrew nuclei | L's four-atom compound; the silluq is on the last atom's final syllable and the metegs stand two or more syllables before it |
| 2 | A1-Genesis בראשית 13:18 | לַֽיהֹוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 3 | A1-Genesis בראשית 13:18 | לַֽיהוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 4 | A1-Genesis בראשית 24:26 | לַֽיהֹוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 5 | A1-Genesis בראשית 24:26 | לַֽיהוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 6 | A1-Genesis בראשית 24:52 | לַֽיהֹוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 7 | A1-Genesis בראשית 24:52 | לַֽיהוָֽה | no Phonetic MAM match | the Name; metegs on the first and the stressed final syllable; the last U+05BD is the silluq |
| 8 | A1-Genesis בראשית 43:28 | וַיִּֽשְׁתַּחֲוֻּֽ | no Phonetic MAM match | the ketiv form; metegs on the second and the final syllable, not adjacent |
| 9 | A2-Exodus שמות 20:3 | לֹֽ֣א־תַעֲשֶֽׂ֨ה־לְךָ֥֣ | no Phonetic MAM match | the Decalogue's עליון compound; not the verse's final chanted word in the תחתון, and its two U+05BD are on the first atom and on the penult before a further atom |
| 10 | A2-Exodus שמות 28:41 | וְכִֽהֲנוּ־לִֽי | parse failed: 1 jta syllables against 4 Hebrew nuclei | the printed editions' compound; metegs on the first atom and on the last atom's one syllable, which is the silluq |
| 11 | A3-Levit ויקרא 26:28 | חַטֹּֽאתֵיכֶֽם | no Phonetic MAM match | ש's form; metegs on the second and the stressed final syllable, not adjacent |
| 12 | A4-Numbers במדבר 2:12 | צוּרִֽישַׁדָּֽי | no Phonetic MAM match | metegs on the second and the stressed final syllable, not adjacent |
| 13 | A4-Numbers במדבר 2:12 | צוּרִֽי־שַׁדָּֽי | no Phonetic MAM match | metegs on the second and the stressed final syllable, not adjacent |
| 14 | A4-Numbers במדבר 10:19 | צוּרִֽישַׁדָּֽי | no Phonetic MAM match | metegs on the second and the stressed final syllable, not adjacent |
| 15 | A4-Numbers במדבר 10:19 | צוּרִֽי־שַׁדָּֽי | no Phonetic MAM match | metegs on the second and the stressed final syllable, not adjacent |
| 16 | A4-Numbers במדבר 31:32 | וַחֲמֵֽשֶׁת־אֲלָפִֽים | parse failed: 3 jta syllables against 7 Hebrew nuclei | L's compound; metegs on the first atom and on the last atom's stressed final syllable |
| 17 | A5-Deuter דברים 5:7 | לֹֽ֣א־תַעֲשֶֽׂ֨ה־לְךָ֥֣ | no Phonetic MAM match | the Decalogue's עליון compound; not the verse's final chanted word in the תחתון, and its two U+05BD are on the first atom and on the penult before a further atom |
| 18 | A5-Deuter דברים 5:7 | לֹֽ֣א־תַעֲשֶֽׂה־לְךָ֥֣ | no Phonetic MAM match | the Decalogue's עליון compound; not the verse's final chanted word in the תחתון, and its two U+05BD are on the first atom and on the penult before a further atom |
| 19 | A5-Deuter דברים 22:20 | לַֽנַּעֲרָֽה | no Phonetic MAM match | the qere; metegs on the first and the stressed final syllable, not adjacent |
| 20 | A5-Deuter דברים 33:28 | יַֽעַרְפוּ־טָֽל | parse failed: 1 jta syllables against 4 Hebrew nuclei | L's compound; metegs on the first atom and on the last atom's one syllable |
| 21 | BB-2Samuel שמואל ב 22:6 | מֹֽקְשֵׁי־מָֽוֶת | parse failed: 2 jta syllables against 4 Hebrew nuclei | the printed editions' compound; the last atom is a segolate with its silluq on its penult and no U+05BD after it |
| 22 | D3-Job איוב 23:5 | מַה־יֹּֽאמַר־לִֽי | parse failed: 1 jta syllables against 4 Hebrew nuclei | A's compound; metegs on the middle atom and on the last atom's one syllable |
| 23 | E3-Lamentations איכה 5:5 | הֽוּנַֽח | no Phonetic MAM match | the first atom of a verse-final compound whose silluq is on the last atom; both metegs stand before it |
| 24 | E5-Esther אסתר 9:22 | לָֽאֶבְיוֹנִֽים | no Phonetic MAM match | L's plene form; metegs on the first and the stressed final syllable, not adjacent |
| 25 | FA-Ezra עזרא 8:36 | וְאֶת־בֵּֽית־הָאֱלֹהִֽים | parse failed: 4 jta syllables against 6 Hebrew nuclei | L's compound; metegs on the middle atom and on the last atom's stressed final syllable |
| 26 | FB-Nehemiah נחמיה 11:30 | עַד־גֵּֽיא־הִנֹּֽם | parse failed: 2 jta syllables against 4 Hebrew nuclei | L's compound; metegs on the middle atom and on the last atom's stressed final syllable |

The 52 NON-verse-final template calls holding a two-U+05BD chanted word (`(c')` in `.novc/mas_a_ws_docnotes_report.txt`) are outside the question by definition, and were read only to confirm that each is mid-verse; they are the well-known double-ga'ya notes (Breuer's "doubts with no decision", the hitpael forms of Yeivin's section 356, L's double ga'yot on maqaf compounds).

## Finding 3 — FOUND ONCE in the MAM introduction, as the one entry of its kind: chapter 5 line 426

The thirteen mirrored pages were scanned for `סילוק`, `סלוק`, `געיה`, `געיות`, `קווים`, `קו אחד`, `מתג` and `מתגים` (550 matches; `.novc/mas_a_intro_grep_report.txt`), and read through four filtered views: the five lines where a silluq word and a meteg word co-occur, the 74 lines holding a Hebrew run with two or more U+05BD, the 27 lines that mention silluq at all, and the 31 lines with an "after the accent" or "two ga'yot" phrase. Six entries are worth naming; the first is the case and the other five are different phenomena:

1. `ch5.mediawiki` line 426, in the per-book list of pointing and accent deviations of the Aleppo Codex: 1 Kings 7:37 `(א=לְכֻלָּֽהְנָֽה): קווים לסילוק וגעיה`. The same reading as the doc-note, silluq then ga'ya, and the only entry in the introduction that names a silluq with a ga'ya after it.
2. `ch2.mediawiki` line 307, the list of every place in the 21 books where the Aleppo Codex and MAM have a maqaf on an atom with a conjunctive accent — the shape of Yeivin's section 357, a ga'ya after the accent followed by a maqaf. Two of its poetic entries are verse-final compounds in the manuscripts MAM's sigla call ק13 and גסטר1, Psalms 18:20 חָ֥פֵֽץ־בִּֽי and Psalms 22:9 חָ֥פֵֽץ־בּֽוֹ: the ga'ya follows the merkha on the first atom and the silluq is on the last atom, so the meteg stands before the silluq, not after it.
3. `ch2.mediawiki` line 515, in a footnote: Psalms 18:46, where L has מִֽמִּסְגְּרֽוֹתֵיהֶֽם with three strokes. MAM's introduction reads them as a heavy ga'ya, a light ga'ya and the silluq, while Mikra'ot Gedolot ha-Keter reads the second stroke as a secondary tipcha; either way both extra marks stand before the silluq.
4. `ch2.mediawiki` line 394, in a footnote on the small strokes that mark the stressed syllable of a deḥi word: Yeivin's reason for their merkha-like slant is that a vertical stroke would be taken for "a ga'ya after the accent, which is found at times in the Crown" — the introduction's one general remark on the post-accent ga'ya, made about mid-verse chanted words.
5. `ch3.mediawiki` line 1365: MAM's editorial rule that where L has two or more ga'yot in one atom, or in maqaf-joined atoms, MAM has one, in the place the rules assign it, with the single exception Numbers 15:14. This is the rule under which MAM's verse-final chanted words with a meteg before the silluq have one meteg — and 1 Kings 7:37 has both strokes because the authority there is the Aleppo Codex, not L.
6. `ch4.mediawiki` line 518: Psalms 19:7, where L's one stroke sits on the first syllable, read as either the silluq misplaced or a ga'ya with the silluq lacking after it; and the same page's lines 473–513, the Obadiah and Psalms entries of finding 1 in their index form.

The appendix's template roster (`appendices.mediawiki`, 67 distinct template names linked as `[[תבנית:...]]`) has no template with silluq or meteg in its name. The dual-cantillation template the Decalogue notes use for a silluq sharing a letter with another accent, `מ:טעם ומתג באות אחת`, is not in that roster; the appendix names the companion `שני טעמים באות אחת` at its lines 408 and 410.

## Finding 4 — FOUND ONCE in Breuer, as a type's exception, with no second case: chapter 8 section 46 note [^81]

In the OCR (`C08-S041.md`), section 46 defines the ga'aya of a big vowel in an open syllable at the end of a cantillated word (Breuer's type j, Yeivin's section 332), gives its three tiers of examples, and closes on the sentence "If this condition is not met, then the ga'aya is very rare", to which note [^81] is attached (file line 177; the `<!-- §47 -->` marker follows at line 179). The note names Jeremiah 46:14 and 2 Chronicles 8:11 as exceptional cases before a word stressed on its second syllable, then: "In one place this ga'aya appears in a word with a mafsik: לכלהנה (I Kings 7:37)", and lastly 1 Chronicles 2:53, where "the ga'aya follows a servant that appears in the word of the mafsik". So Breuer files 1 Kings 7:37 under the open-syllable type, as its one instance in a chanted word with a disjunctive — which at a verse end is the silluq — and names no other such word anywhere in the chapter. Ben cites the passage as chapter 8 section 47, page 355, print footnote 54; the OCR's numbering differs and the print was not consulted (see the last section).

Every verse Breuer's sections 5, 9 and 46 and Yeivin's sections 308, 325, 332, 338, 354 and 357 name as having a ga'ya after the accent was looked up in MAM (`MAM-simple/xml-vtrad-mam/`, MAM's versification). The chanted word is picked out by a plain-letter hint; a hint that matches several tokens takes the one with a U+05BD. Letter positions count from 0 within the atom; "after the last accent" is read off the positions:

| Reference | Source | MAM's chanted word | U+05BD | U+05BD at letter | Accents at letter | Verse-final |
|---|---|---|---|---|---|---|
| Gen. 28:2 | Breuer ch.8 §46 ex. I | פַּדֶּ֣נָֽה | 1 | 2 | munah | no |
| Gen. 28:5 | Breuer ch.1 §41 / ch.8 §46 ex. I | פַּדֶּ֣נָֽה | 1 | 2 | munah | no |
| 1 Sam. 9:24 | Breuer ch.8 §46 ex. I | שִׂים־לְפָנֶ֣יךָֽ | 1 | 4/atom 1 | munah (atom 1) | no |
| Isa. 48:6 | Breuer ch.8 §46 ex. I | שָׁמַ֤עְתָּֽ | 1 | 3 | mahapakh | no |
| Isa. 32:11 | Breuer ch.8 §46 ex. I | פְּשֹׁ֣טָֽה | 1 | 2 | munah | no |
| Deut. 32:13 | Breuer ch.8 §46 ex. I / Yeivin §332 | וַיֵּנִקֵ֤הֽוּ | 1 | 4 | mahapakh | no |
| Jer. 9:18 | Breuer ch.8 §46 ex. I / Yeivin §332 | בֹּ֤שְׁנֽוּ | 1 | 2 | mahapakh | no |
| Eccl. 2:11 | Breuer ch.8 §46 ex. I | וּפָנִ֣יתִֽי | 1 | 4 | munah | no |
| Num. 9:14 | Breuer ch.8 §46 ex. I | וְעָ֤שָֽׂה | 1 | 2 | mahapakh | no |
| 1 Sam. 15:6 | Breuer ch.8 §46 ex. I / Yeivin §332 | עָשִׂ֤יתָֽה | 1 | 3 | mahapakh | no |
| Jer. 9:20 | Breuer ch.8 §46 ex. I / Yeivin §332 | כִּי־עָ֤לָֽה | 1 | 1/atom 1 | mahapakh (atom 1) | no |
| 2 Chr. 13:7 | Breuer ch.8 §46 ex. I | הָ֤יָֽה | 1 | 1 | mahapakh | no |
| 2 Kgs. 9:26 | Breuer ch.8 §46 ex. II | רָאִ֤יתִֽי | 1 | 3 | mahapakh | no |
| Isa. 14:31 | Breuer ch.8 §46 ex. II / Yeivin §332 | הֵילִ֤ילִֽי | 1 | 4 | mahapakh | no |
| Zech. 11:7 | Breuer ch.8 §46 ex. II | קָרָ֤אתִֽי | 1 | 3 | mahapakh | no |
| Mal. 2:3 | Breuer ch.8 §46 ex. II | וְזֵרִ֤יתִֽי | 1 | 4 | mahapakh | no |
| 1 Chr. 12:26 | Breuer ch.8 §46 ex. II / Yeivin §332 | גִּבּ֤וֹרֵֽי | 1 | 3 | mahapakh | no |
| 1 Kgs. 3:13 | Breuer ch.8 §46 ex. III | כָמ֥וֹךָֽ | 1 | 3 | merkha | no |
| 2 Kgs. 1:13 | Breuer ch.8 §46 ex. III / Yeivin §332 | עֲבָדֶ֥יךָֽ | 1 | 4 | merkha | no |
| Lev. 20:4 | Breuer ch.8 §46 ex. III | יַעְלִ֩ימֽוּ֩ | 1 | 4 | telisha qetana, telisha qetana | no |
| Jer. 46:14 | Breuer ch.8 §46 note [^81] | וְהַשְׁמִ֣יעֽוּ | 1 | 5 | munah | no |
| 2 Chr. 8:11 | Breuer ch.8 §46 note [^81] | אֲשֶׁר־בָּ֥אָֽה־אֲלֵיהֶ֖ם | 1 | 1/atom 1 | merkha (atom 1), tipeha (atom 2) | no |
| 1 Kgs. 7:37 | Breuer ch.8 §46 note [^81] | לְכֻלָּֽהְנָֽה | 2 | 2, 4 | none | yes |
| 1 Chr. 2:53 | Breuer ch.8 §46 note [^81] | וְהָאֶשְׁתָּ֖אֻֽלִֽי | 2 | 5, 6 | tipeha | yes |
| Num. 17:23 | Breuer ch.8 §5 (type a) / Yeivin §338 | וַיָּ֣צֵֽץ | 1 | 2 | munah | no |
| Num. 24:22 | Breuer ch.8 §5 (type a) / Yeivin §357 | לְבָ֣עֵֽר | 1 | 2 | munah | no |
| Judg. 8:10 | Breuer ch.8 §5 (type a) | שֹׁ֥לֵֽף־חָֽרֶב | 2 | 1/atom 0, 0/atom 1 | merkha (atom 0) | yes |
| Isa. 66:3 | Breuer ch.8 §5 (type a) / Yeivin §338 | עֹ֣רֵֽף | 1 | 1 | munah | no |
| Isa. 66:3 (second) | Yeivin §338 | מְבָ֣רֵֽךְ | 1 | 2 | munah | no |
| Isa. 66:8 | Breuer ch.8 §5 (type a) | אִם־יִוָּ֥לֵֽד־גּ֖וֹי | 1 | 2/atom 1 | merkha (atom 1), tipeha (atom 2) | no |
| Jer. 23:29 | Breuer ch.8 §5 (type a) | יְפֹ֥צֵֽץ | 1 | 2 | merkha | no |
| 2 Sam. 7:24 | Breuer ch.8 §5 (type a) | וַתְּכ֣וֹנֵֽן | 1 | 4 | munah | no |
| Isa. 63:12 | Breuer ch.8 §5 (type a) / Yeivin §308 | בּ֤וֹקֵֽעַ | 1 | 2 | mahapakh | no |
| Isa. 59:16 | Breuer ch.8 §9 ex. I (type b) / Yeivin §357 | וַתּ֤וֹשַֽׁע־לוֹ֙ | 1 | 3/atom 0 | mahapakh (atom 0), pashta (atom 1) | no |
| Jer. 22:14 | Breuer ch.8 §9 ex. I (type b) | וְקָ֤רַֽע | 1 | 2 | mahapakh | no |
| Ezek. 1:4 | Breuer ch.8 §9 ex. I (type b) / Yeivin §354 | וְנֹ֥גַֽהּ־ל֖וֹ | 1 | 2/atom 0 | merkha (atom 0), tipeha (atom 1) | no |
| Ezek. 16:8 | Breuer ch.8 §9 ex. I (type b) | וָאֶשָּׁ֣בַֽע | 1 | 3 | munah | no |
| 2 Chr. 14:6 | Breuer ch.8 §9 ex. I (type b) | וַיָּ֥נַֽח־לָ֖נוּ | 1 | 2/atom 0 | merkha (atom 0), tipeha (atom 1) | no |
| Ruth 1:21 | Breuer ch.8 §9 ex. I (type b) / Yeivin §354 | הֵ֥רַֽע | 1 | 1 | merkha | no |
| Deut. 29:19 | Breuer ch.8 §9 ex. I (type b) / Yeivin §354 | סְלֹ֣חַֽ | 1 | 2 | munah | no |
| Judg. 19:25 | Breuer ch.8 §9 ex. I (type b) / Yeivin §354 | לִשְׁמֹ֣עַֽ | 1 | 3 | munah | no |
| Lam. 5:6 | Breuer ch.8 §9 ex. I (type b) / Yeivin §357 | לִשְׂבֹּ֥עַֽ | 1 | 3 | merkha | no |
| Hos. 14:7 | Breuer ch.8 §9 ex. I (type b) | וְרֵ֥יחַֽ | 1 | 3 | merkha | no |
| Isa. 52:11 | Yeivin §332 | ס֤וּרוּ | 0 | none | mahapakh | no |
| Ezek. 21:16 | Yeivin §332 | הִֽיא־הוּחַ֤דָּה | 1 | 0/atom 0 | mahapakh (atom 1) | no |
| Ezek. 41:7 | Yeivin §332 | לְמַ֨עְלָה | 0 | none | qadma | no |
| Isa. 40:7 | Yeivin §338 | נָ֣בֵֽל־צִ֔יץ | 1 | 1/atom 0 | munah (atom 0), zaqef qatan (atom 1) | no |
| Isa. 40:8 | Yeivin §338 | נָ֣בֵֽל | 1 | 1 | munah | no |
| Isa. 49:7 | Yeivin §308 | לִמְתָ֤עֵֽב | 1 | 3 | mahapakh | no |
| 1 Kgs. 2:8 | Yeivin §354 | וָאֶשָּׁ֨בַֽע | 1 | 3 | qadma | no |
| Ezek. 1:27 | Yeivin §354 | וְנֹ֥גַֽהּ | 1 | 2 | merkha | no |
| Jer. 49:23 | Yeivin §357 | בּ֤וֹשָֽׁה | 1 | 2 | mahapakh | no |
| 1 Kgs. 2:30 | Yeivin §325 (before paseq) | וַיֹּ֥אמֶֽר | 1 | 3 | merkha | no |

What the table shows, in four points:

1. Only two roster verses have a verse-final chanted word with two U+05BD: 1 Kings 7:37 לְכֻלָּֽהְנָֽה, the case, and 1 Chronicles 2:53 וְהָאֶשְׁתָּ֖אֻֽלִֽי. In the second the tipcha is a secondary accent inside the silluq's chanted word, the meteg follows it, and the silluq is the last U+05BD, on the stressed gentilic ending — Breuer's description in the note. A meteg after a secondary accent and before the silluq is a different phenomenon.
2. Judges 8:10 שֹׁ֥לֵֽף־חָֽרֶב is a verse-final compound with the ga'ya after the merkha on its first atom and the silluq on its segolate last atom; 2 Chronicles 14:6 וַיָּ֥נַֽח־לָ֖נוּ and Ezekiel 1:4 are the same shape mid-verse. In every such compound the meteg stands before the silluq.
3. Every other roster chanted word that MAM has with the ga'ya after the accent is mid-verse and has exactly one U+05BD (the column "after the last accent" is what the two books describe). MAM lacks the mark at three of Yeivin's section 332 examples, Isaiah 52:11, Ezekiel 21:16 and Ezekiel 41:7, as `doc/holman-meteg-m23-isaiah-23-12.md` already records for the first.
4. The verse-final chanted word of Ezekiel 16:8, וַתִּֽהְיִי־לִֽי, appears in the table only because it shares the verse with a roster word; its two U+05BD are one per atom, the second being the silluq.

## Finding 5 — NOT FOUND in Yeivin: the ga'ya run never names silluq, and its after-the-accent verses are all mid-verse in MAM

Sections 309–357 (`N0309.md`, `N0328.md`, `N0329.md`, `N0338.md`, `N0342.md`, `N0345.md`) mention neither silluq nor sof pasuq, as `doc/foi-mtgmtg-empty-cell.md` measured on 2026-09-09 and as a grep for `after the accent` over the whole ITM export confirms: the phrase occurs at the section 332 heading (`N0329.md` line 48), the section 338 heading (line 184), section 357 (`N0345.md` lines 284–286) and the index. Section 357's four verses — Jeremiah 49:23, Numbers 24:22, Isaiah 59:16, Lamentations 5:6 — are mid-verse in MAM (table above), and section 325's ga'ya before paseq, 1 Kings 2:30, is mid-verse too. Yeivin's one general statement that touches the question is section 332's condition that the word "stands before a word with the accent on the first syllable", which a verse-final chanted word cannot meet; Breuer's section 46 has the same following-word condition. Neither book has a category for a ga'ya after a silluq, and neither says such a ga'ya is impossible.

## Finding 6 — RE-VERIFIED: what the four prerequisite documents say stands

1. `gh-pages/post-stress-meteg-post-silluq.html` shows MAM's 1 Samuel 17:5 with one U+05BD against BHS's two; MAM-simple has נְחֹֽשֶׁת there, one U+05BD, re-read for this file.
2. `doc/foi-mtgmtg-empty-cell.md` reports the `2/sopa-y/maq-n` group of the `mtgmtg` survey empty — no lone verse-final atom with a silluq and two metegs — and that is consistent with everything above: no MAM verse-final atom in the documentation has more than two U+05BD, and the only one whose second U+05BD follows the silluq is 1 Kings 7:37. The three-stroke atoms the notes quote belong to other texts, and all their marks stand before the stress: Koren's Leviticus 23:31 מֹֽשְׁבֹֽתֵיכֶֽם (MAM has מֹשְׁבֹֽתֵיכֶֽם) and L's Psalms 18:46 מִֽמִּסְגְּרֽוֹתֵיהֶֽם.
3. `doc/PLAN-silluq-before-gaya-template.md` plans a template for 1 Kings 7:37 alone, and its clause that the cleanup "supports a future atom with more than one post-silluq meteg" stays unexercised: no documented site would call it.
4. `doc/holman-meteg-m23-isaiah-23-12.md`'s section on the post-silluq meteg counts 1 Samuel 17:5 as the one case, in the Leningrad Codex; with 1 Kings 7:37 in MAM the count is two, one per text, as `doc/PLAN-silluq-before-gaya-template.md` already says of that heading.

## What could not be verified

1. Breuer's print page and footnote numbers. Ben's citation is chapter 8 section 47, page 355, footnote 54; the OCR attaches the note as [^81] to section 46's closing sentence and numbers its footnotes continuously across the chapters 6–8 export. The scans under `C:/Users/BenDe/OneDrive/Documents/ScansOfBooks/The Cantillation of Scripture - English/` (`C355-...jpg` would be page 355) were not opened, this task being confined to what is on disk and a OneDrive file being a network fetch.
2. The OCR of section 46's example columns and of section 47's hyphenated list is partly garbled; the roster took the references that could be read (the section 46 examples I–III, the note's four verses, section 5's eight and section 9's ten), and section 47's hyphenated compounds were left out because their ga'aya is on the unaccented first atom, before the compound's accent.
3. The stress judgments in finding 2's two tables are morphological, by Claude, not from an oracle: Phonetic MAM reads the last U+05BD of every verse-final chanted word as the silluq, so it cannot adjudicate the question, and no other stress model is on disk.
4. Coverage of the wikitext scan. 23,283 verse segments were parsed, 23,202 distinct (book, chapter, verse) keys against 23,202 verses in MAM-simple; verses of MAM-simple that no segment matched: 0; keys with no MAM-simple verse: 0. The 81 keys that occur twice are the song-layout pages the wikitext transcludes beside the running text (A2-Exodus 8, A5-Deuter 9, B1-Joshua 8, E4-Ecclesiastes 14, E5-Esther 28, FC-1Chronicles 14), each of whose verses was scanned twice. A line holding two verses (75 lines, a verse after a parasha note or at a portion's start with no space) is split at the second header, so the first verse's last template is judged verse-final against its own verse and not against the next. The scanner met no unbalanced template construct.
5. The introduction's 550 keyword matches were read through the four filtered views named in finding 3, not line by line; a passage that describes a silluq with a ga'ya after it without using any of the eight keywords, a two-U+05BD form, or an "after the accent" phrase would have been missed.
6. The a06 index is dated 2026-08-31 and `in/mam-ws` is the current mirror; for the two criteria compared (verses whose notes mention silluq; verses whose notes hold a two-U+05BD form) the index flags no verse the wikitext does not, and the 15 verses the wikitext adds are all non-`נוסח` templates the index does not cover.

## Scripts and commands

All scripts are gitignored under `.novc/` in the worktree and run from its root on the primary clone's interpreter; each prints a labelled report beside itself and keeps Hebrew off stdout. They are throwaway: unformatted, `sys.path.insert` where a repo module is reused.

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

1. `.novc/mas_a_ws_docnotes.py` — parses `in/mam-ws`, writes `mas_a_ws_docnotes_report.txt` (sections (a), (b), (c), (c'), the per-book verse comparison), `mas_a_ws_docnotes_b_compact.txt`, `mas_a_ws_docnotes_hits.json` and `mas_a_ws_docnotes_summary.json`; finding 1's table and finding 2's counts.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_ws_docnotes.py
   ```

2. `.novc/mas_a_stress_after_census.py` — counts, over every chanted word of Phonetic MAM, the syllables after the stressed syllable within the stressed atom under Ben's syllable definition, and the same over the chanted words whose form has sof pasuq, writes `mas_a_stress_after_census_report.txt` and `mas_a_stress_after_census_summary.json`; the basis of finding 2's adjacency test.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_stress_after_census.py
   ```

3. `.novc/mas_a_stress_classify.py` — classifies every two-U+05BD string of (c) by syllable against Phonetic MAM under Ben's syllable definition, keeping the earlier `jta` count beside it, writes `mas_a_stress_classify_report.txt` and `mas_a_stress_classify_summary.json`; finding 2's candidates and failures.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_stress_classify.py
   ```

4. `.novc/mas_a_a06_scan.py` — scans the a06 index, writes `mas_a_a06_scan_report.txt` and `mas_a_a06_scan_keys.json`.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_a06_scan.py
   ```

5. `.novc/mas_a_compare_a06_ws.py` — the index-versus-wikitext cross-check, `mas_a_compare_a06_ws_report.txt`.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_compare_a06_ws.py
   ```

6. `.novc/mas_a_intro_grep.py` — the introduction scan, `mas_a_intro_grep_report.txt`; finding 3.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_intro_grep.py
   ```

7. `.novc/mas_a_lookup.py` — the Breuer and Yeivin roster looked up in MAM-simple, `mas_a_lookup_report.txt`; finding 4's table.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_lookup.py
   ```

8. `.novc/mas_a_write_doc.py` — writes this file from the JSON summaries, lifting every Hebrew form from the data by consonantal skeleton with a uniqueness assertion, then checks the whole file with `has_std_mark_order`.

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mas_a_write_doc.py
   ```

Re-measure rather than trust: a change in any figure above is a finding. The run this file records used `in/mam-ws` and `in/mam-ws-intro` as tracked at `30fb7681`, MAM-simple as tracked there, and MAM-private's al-hatorah `io/` files dated 2026-08-31 (a06) and 2026-09-05 (Phonetic MAM).
