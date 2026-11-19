# The Google Sheet's credits ported to the MAM change logs, 2026-11-19

State: executed 2026-11-19; 61 credits ported from the old Google Sheet's changes tab, and the change logs regenerated with them

Written by a Claude (Opus 5.5) session on 2026-11-19 while executing
[PLAN-change-log-credits.md](PLAN-change-log-credits.md), Phase 3, steps 5 to 7. A script wrote
its tables and every Hebrew form and Sheet quotation in it, copying them from the change logs'
JSON, `in/mam-change-log-credits.json` and the capture of the Sheet's changes tab.

## Summary

- `in/mam-change-log-credits.json` holds 62 records: Phase 1's record for 2 Samuel 4:6, and 61
  records ported from the Sheet, one for each change in the change logs that a Sheet row credits
  to an outsider. They credit 8 contributors, named as the Sheet names them.
- Regenerated, the change logs have the 61 credits on cards of four named releases: 2025-03-19a
  39, 2026-03-06 4, 2026-03-16 1 and 2026-09-17 17. A credited card has a line such as "Credit
  to Daniel Holman: Sheet row 5.", whose link opens that row of the frozen Sheet.
- The 2 Samuel 4:6 card, in `unpinned-latest`, now credits Asael Reiter rather than Asael
  (decision 2).
- The other 200 rows crediting outsiders got no record, and row 28 credits no one; the last
  section gives each its reason. Two of them, rows 79 and 101, describe changes that the change
  logs do not show.

## Ben's decisions

The executing session put six decisions to Ben on a decision page, with a recommendation for
each but the second, which asked whether two names are one person. Ben replied on 2026-11-19:

> Assume עשהאל is Asael Reiter. Follow all other recommendations.

So:

1. **The survey's 60 matched credits are recorded,** one record for each pair of the change logs
   that a row's credit describes. Rows 9 and 240, both Daniel Holman's, describe one pair,
   Isaiah 42:24's in 2026-09-17, so its one record cites both rows, row 9 first.
2. **The Sheet's "Asael Reiter" is the Hebrew Wikisource user `עשהאל`, whom Avi's request calls
   Asael.** One contributor, `asael-reiter`, now has the credits of both names. It is named
   "Asael Reiter", as Ben's reply and the Sheet name him, and is linked to that user page. The 2
   Samuel 4:6 record moved to this id from `asael`, which no longer exists.
3. **Row 142 is credited with the change at 2 Samuel 24:10,** release 2025-03-19a, entry 13,
   pair 1, although the row's *where* names Malachi 2:7. The decision page said this record
   would note the slip. The row's *what* reads:

   > Changed accent zaqeph qaton to ravia` in "יְהֹוָ֗ה". Credit to Asael Reiter. To be imported via auto-edits.

   In Malachi 2:7 MAM has those letters only as the first atom of a maqaf compound, which has a
   meteg and no accent, so no zaqef or revia can have been exchanged there. In 2 Samuel 24:10,
   entry 13's old form of the atom has zaqef and its new form revia, and no other Sheet row
   claims that change. The card's evidence link reads "Sheet row 142".
4. **Row 249's Psalms 86:5 item is not credited.** Daniel Holman's list of meteg deletions in
   Psalms, dated 2024-01-09, includes that verse, but the change logs have the deletion only in
   2026-03-16, and Ben's own row 58, whose place in the tab puts it in March 2026, lists it with
   credit to himself. Ben's own credits are not ported.
5. **Rows 264 (1 Kings 11:1) and 273 (2 Samuel 18:3) are not credited.** Each of these lists of
   Daniel Holman's, dated December 2023, has an item equal to a meteg deletion in 2026-09-17.
   Both deletions were made in that release, among its 29 meteg changes that no Sheet row of 2026
   names; at the release's start, MAM still had both metegs.
6. **Row 104's thanks to Prof. Yosef Ofer is left out.** Its two records, at Proverbs 11:12 and
   14:21, credit the anonymous contributor the row credits, and their "Sheet row 104" links show
   the row's "and thanks to Prof. Yosef Ofer for his assistance".

## The capture

The port reads `in/mam-go-changes-tab/changes.csv`, committed in `5ed853e2` ("Capture the old
Google Sheet's changes tab for the change-log credits"). Its `manifest.json` records:

- the URL,
  `https://docs.google.com/spreadsheets/d/e/2PACX-1vQrnXDxQJ3pojK_9K4TiRwCpz-NCMmW5mWE9fH5ITpV0IF9aV4-XVtmShTyyIoB_PGRCk4o_YQYWPsU/pub?output=csv&gid=953964633`;
- the retrieval time, 2026-11-19T16:30:05+00:00, which is 11:30:05 New York time on 2026-11-19;
- 189,511 bytes, SHA-256 `030cb757027c00754600a43a989d8fd5bf6b8f2ed3f6196f23d39d6f1567684e`;
- 1,084 records. Record 1 is the freeze banner and record 2 the header, so record N is Sheet row
  N.

The SHA-256, recomputed from the file for this record, equals the manifest's and the planning
session's read of the published tab at 15:35:32 UTC (10:35:32 New York time) the same day, so
the frozen tab did not change between the two reads.

## Counts against the plan's figures

The survey repeated the planning session's measurements on the capture, and this record
recounted them from the survey's data. By the plan's test, a row is *tied* to an entry when the
entry is at the row's verse and shares a word with the Hebrew the row quotes; two atoms share a
word when their letters are equal and number two or more.

| Figure | Plan | Port |
| --- | --- | --- |
| Rows with a word of credit or thanks | 267 | 267 |
| Rows saying "Credit to" and a name | 266 | 266 |
| ... crediting Ben Denckla, not ported | 38 | 38 |
| ... crediting outsiders | 228 | 228 |
| Outsider rows naming one verse, tied to an entry | 24 | 24 |
| ... in 2025-03-19a, 2026-03-06, 2026-03-16 and 2026-09-17 | 5, 2, 1, 16 | 5, 2, 1, 16 |
| Outsider rows naming one verse, with an entry the test cannot tie | 9 | 9 |
| Outsider rows naming one verse that no change log touches | 165 | 167 |
| Outsider rows naming several verses, in the logs' span | 2 (rows 79, 104) | 2 (rows 79, 104) |
| Outsider rows naming several verses, before the logs | not counted | 26 |
| Ben's rows tied to an entry | 23 | 23 |
| Rows read month-first | 56 | 55 |

The survey found five departures from the plan's figures:

1. **167 one-verse rows that no change log touches, not 165.** Rows 283 and 477 read as one
   verse here only through named variants: row 283's *where* spells Joshua's name with an extra
   letter, and row 477's ends with the book tab's column letter C. A parser built like the
   removed precedent rejects both. Neither verse has an entry.
2. **55 rows read month-first, not 56.** The plan's figure comes from reading each row against
   the row above it; the survey read the rows together, choosing the readings that put the most
   rows in newest-first order. The two readings differ only on rows 64 to 69 and 613, none a
   credit row.
3. **One of the 24 ties is false.** Row 142 ties at Malachi 2:7 only through the letters of the
   divine name; the entry there, 2025-03-19a's entry 50, is another change, which row 141
   records. Decision 3 credits row 142 at 2 Samuel 24:10 instead.
4. **The plan's counts leave out rows that name several verses before the logs.** Rows 144 and
   145 (Daniel Holman, 2024-11-28 and 2024-11-27) list 6 and 28 meteg changes in the Twelve
   Prophets, made by auto-edits that landed in 2025-03-19a: 34 records that a one-verse test
   cannot see.
5. **Two names hold full stops.** Rows 521 and 526 credit "anonymous reader at alhatorah.org"
   and "anonymous reader at mg.alhatorah.org", which the plan's list from the 2023 snapshot, cut
   at the first full stop, gives as "anonymous reader at alhatorah" and "anonymous reader at
   mg". Neither row is in the logs' span.

The plan's figures count rows, and the records count changes. The 61 Sheet records come from 28
rows: the 24 tied one-verse rows give 25, since row 12's credit covers both pairs of its entry;
row 104, one of the 2 rows that name several verses in the span, gives 2; rows 144 and 145 give
34; and row 240's one matched item is row 9's change, whose record cites it. The 9 rows the test
cannot tie all match nothing, and row 79, the span's other row that names several verses,
describes changes that the change logs do not show.

## The records

| Release | Records | Sheet rows |
| --- | --- | --- |
| 2025-03-19a | 39 | 112, 138, 139, 142 to 145 |
| 2026-03-06 | 4 | 87, 94, 104 |
| 2026-03-16 | 1 | 82 |
| 2026-09-17 | 17 | 5 to 18, 30, 31, 240 |
| unpinned-latest | 1 | none: 2 Samuel 4:6, credited from Wikisource |
| All | 62 |  |

| Contributor | Id | Records | Sheet rows |
| --- | --- | --- | --- |
| Asael Reiter | `asael-reiter` | 3 | 94, 142, and 2 Samuel 4:6 from Wikisource |
| Daniel Holman | `daniel-holman` | 50 | 5 to 18, 143 to 145, 240 |
| anonymous contributor at Wikisource | `anonymous-contributor-at-wikisource` | 2 | 30, 31 |
| Moshe Greenberg | `moshe-greenberg` | 2 | 82, 87 |
| anonymous contributor at Hebrew Wikisource | `anonymous-contributor-at-hebrew-wikisource` | 2 | 104 |
| anonymous contributor at AlHatorah | `anonymous-contributor-at-alhatorah` | 1 | 112 |
| Timothy Leininger | `timothy-leininger` | 1 | 138 |
| anonymous editor at Hebrew Wikisource | `anonymous-editor-at-hebrew-wikisource` | 1 | 139 |

Each id is the lowercase ASCII slug of its name. Only `asael-reiter` has a `user_page`, the user
name the 2 Samuel 4:6 record's contributor had; the others are `null`, since the plan's decision
3 leaves a ported credit unlinked. The Sheet's records follow 2 Samuel 4:6's in Sheet-row order,
and within a row in the order of its items. Each cites its row as evidence of kind
`mam-sheet-changes-row`, and each was recorded on 2026-11-19 on the basis "Ben's decisions of
2026-11-19 on the Sheet port (doc/change-log-credits-sheet-port-2026-11-19.md)". Every record's
Hebrew forms were copied by script from its pair in the change log's JSON and checked against
the survey's copy. The file's `_header` gained a line saying where these records came from.

## Changes the change logs do not show

Two rows crediting outsiders describe changes made in the logs' span that the change logs have
no entry for, so no credit can attach to them:

1. **Row 79** ("anonymous Wikisource contributer", as the Sheet spells it, 2026-02-14) moved
   seder divisions:

   > Changed "seder" division in the following places: 1 Samuel 3:20 (from 3:19); 2 Samuel 2:7 (from 2:6); Isaiah 65:9 (was previously missing). Credit to anonymous Wikisource contributer.

   All three changes are in release 2026-03-16's span. The change log compares only each verse's
   text column, and a seder is a parameter of the verse's template, outside that column, so none
   of the five verses has an entry.
2. **Row 101** (Adrian Hills, 2025-05-18, Job 16:14) moved the small final tsadi:

   > Moved small letter final-tsadi (ץ) from the first instance ("פֶ֭רֶץ") to the second instance ("עַל־פְּנֵי־פָ֑רֶץ"), as properly found in old printed versions and Koren. Credit to Adrian Hills. To be imported via auto-edits.

   The move is in release 2026-03-06's span. The change log finds a verse's changes by comparing
   its flattened text, its templates' counts and the structure of their nesting, and all three
   are the same before and after the move, so it has no entry. (The quotation has MAM's mark
   order, which this repository's prose requires: on the pe of the second form it puts the
   dagesh before the sheva, where the capture has the sheva first.)

Ben asked on 2026-11-19, when told of these two rows: "create a github issue regarding extending
the comparison code to catch such things". MAM-basics issue
[#374](https://github.com/bdenckla/MAM-basics/issues/374) is that issue; until the change logs
show such changes, neither row can be credited.

## Checks

Run from the clone's root with its `./.venv/Scripts/python.exe`, after the records were written:

- `mpplus_credits.load_credits()` validates the file: 62 records, each selecting a `change`.
- `py/main_diff.py mpplus --all` regenerated the change logs, and its check that each record
  matches exactly one entry passed. `py/main_diff.py mpplus --check` then printed "MAM
  change-log artifacts are current."
- The diff is the credits file and the JSON and HTML of 2025-03-19a, 2026-03-06, 2026-03-16,
  2026-09-17 and `unpinned-latest`. Read back against `HEAD`, each report's JSON entries differ
  only by their `credits`, which are on the entries the records name: 39, 4, 1, 17 and 1. Each
  HTML report differs only by its credit lines, 39, 4, 1 and 17, each on its record's card, and
  `unpinned-latest` by the one line whose name changed. 2025-03-19b, 2026-04-14, `index.html`,
  `releases.json`, `style.css` and `filter.js` are byte-identical.
- `git diff --check` found nothing.
- `py/main_test.py` on the five change-log test files of the plan's Phase 1, step 6: "41 passed
  in 74.98s (0:01:14)", the count Phase 1 had.
- `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc`: "No HTML output issues found.",
  with the 16980 undefined CSS class references it reports as informational, as before the port.

## Every record

In file order. Verses are named as the change logs' cards name them, and the release, entry and
pair locate the credited pair in that release's JSON.

| Record | Sheet row | Contributor | Release | Entry | Pair | Verse | Category | Old | New |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | none (Wikisource) | Asael Reiter | unpinned-latest | 8 | 1 | 2Samuel 4:6 | accent-change | וְ֠הֵנָּ֠ה | וְ֠הֵ֠נָּה |
| 2 | 5 | Daniel Holman | 2026-09-17 | 74 | 1 | 2Chronicles 28:19 | meteg-addition | מֶלֶךְ־יִשְׂרָאֵ֑ל | מֶֽלֶךְ־יִשְׂרָאֵ֑ל |
| 3 | 6 | Daniel Holman | 2026-09-17 | 50 | 1 | Isaiah 24:18 | meteg-addition | וְ֠הָיָ֠ה | וְֽ֠הָיָ֠ה |
| 4 | 7 | Daniel Holman | 2026-09-17 | 58 | 1 | Tsefaniah 3:13 | meteg-removal | וְלֹֽא־יִמָּצֵ֥א | וְלֹא־יִמָּצֵ֥א |
| 5 | 8 | Daniel Holman | 2026-09-17 | 52 | 1 | Isaiah 50:7 | meteg-removal | יַֽעֲזׇר־לִ֔י | יַעֲזׇר־לִ֔י |
| 6 | 9, 240 | Daniel Holman | 2026-09-17 | 51 | 1 | Isaiah 42:24 | meteg-removal | מִֽי־נָתַ֨ן | מִי־נָתַ֨ן |
| 7 | 10 | Daniel Holman | 2026-09-17 | 48 | 1 | Isaiah 22:5 | meteg-removal | לַֽאדֹנָ֧י | לַאדֹנָ֧י |
| 8 | 11 | Daniel Holman | 2026-09-17 | 73 | 1 | 2Chronicles 26:15 | meteg-removal | כִּֽי־חָזָֽק׃ | כִּי־חָזָֽק׃ |
| 9 | 12 | Daniel Holman | 2026-09-17 | 47 | 1 | 2Kings 21:12 | meteg-removal | עַל־יְרֽוּשָׁלַ֖͏ִם | עַל־יְרוּשָׁלַ֖͏ִם |
| 10 | 12 | Daniel Holman | 2026-09-17 | 47 | 2 | 2Kings 21:12 | meteg-removal | וִֽיהוּדָ֑ה | וִיהוּדָ֑ה |
| 11 | 13 | Daniel Holman | 2026-09-17 | 45 | 1 | 2Kings 6:23 | meteg-removal | אֶל־אֲדֹֽנֵיהֶ֑ם | אֶל־אֲדֹנֵיהֶ֑ם |
| 12 | 14 | Daniel Holman | 2026-09-17 | 29 | 1 | 1Samuel 22:22 | meteg-removal | כִּֽי־שָׁם֙ | כִּי־שָׁם֙ |
| 13 | 15 | Daniel Holman | 2026-09-17 | 26 | 1 | 1Samuel 1:6 | meteg-removal | כִּֽי־סָגַ֥ר | כִּי־סָגַ֥ר |
| 14 | 16 | Daniel Holman | 2026-09-17 | 12 | 1 | Joshua 19:8 | meteg-removal | בְנֵֽי־שִׁמְע֖וֹן | בְנֵי־שִׁמְע֖וֹן |
| 15 | 17 | Daniel Holman | 2026-09-17 | 59 | 1 | Zechariah 2:4 | misc | אֲשֶׁר־זֵ֣רוּ | אֲשֶׁר־זֵר֣וּ |
| 16 | 18 | Daniel Holman | 2026-09-17 | 10 | 1 | Joshua 10:12 | accent-addition | יְהוֹשֻׁעַ֙ | יְהוֹשֻׁ֙עַ֙ |
| 17 | 30 | anonymous contributor at Wikisource | 2026-09-17 | 8 | 1 | Numbers 16:18 | misc | וַֽיַּעַמְד֗וּ | וַיַּֽעַמְד֗וּ |
| 18 | 31 | anonymous contributor at Wikisource | 2026-09-17 | 7 | 1 | Numbers 11:24 | meteg-removal | וַֽיַּעֲמֵ֥ד | וַיַּעֲמֵ֥ד |
| 19 | 82 | Moshe Greenberg | 2026-03-16 | 70 | 1 | Isaiah 10:17 | accent-addition | וְאָכְלָ֛ה | וְאָ֥כְלָ֛ה |
| 20 | 87 | Moshe Greenberg | 2026-03-06 | 3 | 1 | 2Samuel 15:12 | legarmeih-paseq | יוֹעֵ֣ץ | יוֹעֵ֣ץ׀ |
| 21 | 94 | Asael Reiter | 2026-03-06 | 1 | 1 | Judges 7:7 | varika | הַֽמְלַקְﬞקִים֙ | הַֽמְﬞלַֽקְﬞקִים֙ |
| 22 | 104 | anonymous contributor at Hebrew Wikisource | 2026-03-06 | 22 | 1 | Proverbs 11:12 | vowel-change | בׇּז־לְרֵעֵ֥הוּ | בָּז־לְרֵעֵ֥הוּ |
| 23 | 104 | anonymous contributor at Hebrew Wikisource | 2026-03-06 | 23 | 1 | Proverbs 14:21 | vowel-change | בׇּז־לְרֵעֵ֥הוּ | בָּז־לְרֵעֵ֥הוּ |
| 24 | 112 | anonymous contributor at AlHatorah | 2025-03-19a | 57 | 1 | Job 21:24 | misc | עֲ֭טִינָיו | עֲ֭טִנָיו |
| 25 | 138 | Timothy Leininger | 2025-03-19a | 56 | 1 | Proverbs 5:13 | meteg-removal | לֹֽא־הִטִּ֥יתִי | לֹא־הִטִּ֥יתִי |
| 26 | 139 | anonymous editor at Hebrew Wikisource | 2025-03-19a | 2 | 1 | Genesis 45:14 | misc | בִנְיָמִֽן־אָחִ֖יו | בִנְיָֽמִן־אָחִ֖יו |
| 27 | 142 | Asael Reiter | 2025-03-19a | 13 | 1 | 2Samuel 24:10 | accent-change | יְהֹוָ֔ה | יְהֹוָ֗ה |
| 28 | 143 | Daniel Holman | 2025-03-19a | 38 | 1 | Zechariah 2:9 | meteg-removal | אֶֽהְיֶ֥ה | אֶהְיֶ֥ה |
| 29 | 144 | Daniel Holman | 2025-03-19a | 18 | 1 | Hosea 2:10 | meteg-addition | אָנֹכִי֙ | אָֽנֹכִי֙ |
| 30 | 144 | Daniel Holman | 2025-03-19a | 21 | 1 | Hosea 12:3 | meteg-addition | לַיהֹוָ֖ה | לַֽיהֹוָ֖ה |
| 31 | 144 | Daniel Holman | 2025-03-19a | 30 | 1 | Micah 3:3 | meteg-addition | וּפָרְשׂוּ֙ | וּפָֽרְשׂוּ֙ |
| 32 | 144 | Daniel Holman | 2025-03-19a | 31 | 1 | Micah 3:5 | meteg-addition | וַאֲשֶׁר֙ | וַֽאֲשֶׁר֙ |
| 33 | 144 | Daniel Holman | 2025-03-19a | 39 | 1 | Zechariah 10:6 | meteg-addition | לֹא־זְנַחְתִּ֑ים | לֹֽא־זְנַחְתִּ֑ים |
| 34 | 144 | Daniel Holman | 2025-03-19a | 48 | 1 | Malachi 2:3 | meteg-addition | וְזֵרִ֤יתִי | וְזֵרִ֤יתִֽי |
| 35 | 145 | Daniel Holman | 2025-03-19a | 19 | 1 | Hosea 6:3 | meteg-removal | מֹֽצָא֑וֹ | מֹצָא֑וֹ |
| 36 | 145 | Daniel Holman | 2025-03-19a | 20 | 1 | Hosea 11:8 | meteg-removal | נִֽחוּמָֽי׃ | נִחוּמָֽי׃ |
| 37 | 145 | Daniel Holman | 2025-03-19a | 22 | 1 | Joel 2:2 | meteg-removal | עַל־הֶֽהָרִ֑ים | עַל־הֶהָרִ֑ים |
| 38 | 145 | Daniel Holman | 2025-03-19a | 23 | 1 | Joel 2:27 | meteg-removal | וְלֹֽא־יֵבֹ֥שׁוּ | וְלֹא־יֵבֹ֥שׁוּ |
| 39 | 145 | Daniel Holman | 2025-03-19a | 24 | 1 | Joel 3:5 | meteg-removal | תִּֽהְיֶ֣ה | תִּהְיֶ֣ה |
| 40 | 145 | Daniel Holman | 2025-03-19a | 25 | 1 | Joel 4:17 | meteg-removal | יְרֽוּשָׁלַ֙͏ִם֙ | יְרוּשָׁלַ֙͏ִם֙ |
| 41 | 145 | Daniel Holman | 2025-03-19a | 26 | 1 | Amos 2:6 | meteg-removal | בַּֽעֲב֥וּר | בַּעֲב֥וּר |
| 42 | 145 | Daniel Holman | 2025-03-19a | 27 | 1 | Amos 5:14 | meteg-removal | וִֽיהִי־כֵ֞ן | וִיהִי־כֵ֞ן |
| 43 | 145 | Daniel Holman | 2025-03-19a | 28 | 1 | Amos 8:11 | meteg-removal | וְלֹֽא־צָמָ֣א | וְלֹא־צָמָ֣א |
| 44 | 145 | Daniel Holman | 2025-03-19a | 29 | 1 | Jonah 3:10 | meteg-removal | אֶֽת־מַ֣עֲשֵׂיהֶ֔ם | אֶת־מַ֣עֲשֵׂיהֶ֔ם |
| 45 | 145 | Daniel Holman | 2025-03-19a | 32 | 1 | Micah 6:13 | meteg-removal | הֶֽחֱלֵ֣יתִי | הֶחֱלֵ֣יתִי |
| 46 | 145 | Daniel Holman | 2025-03-19a | 34 | 1 | Tsefaniah 1:11 | meteg-removal | יֹֽשְׁבֵ֣י | יֹשְׁבֵ֣י |
| 47 | 145 | Daniel Holman | 2025-03-19a | 36 | 1 | Tsefaniah 3:13 | meteg-removal | כִּֽי־הֵ֛מָּה | כִּי־הֵ֛מָּה |
| 48 | 145 | Daniel Holman | 2025-03-19a | 35 | 1 | Tsefaniah 3:9 | meteg-removal | כִּֽי־אָ֛ז | כִּי־אָ֛ז |
| 49 | 145 | Daniel Holman | 2025-03-19a | 37 | 1 | Tsefaniah 3:16 | meteg-removal | לִירֽוּשָׁלַ֖͏ִם | לִירוּשָׁלַ֖͏ִם |
| 50 | 145 | Daniel Holman | 2025-03-19a | 40 | 1 | Zechariah 11:13 | meteg-removal | וָֽאַשְׁלִ֥יךְ | וָאַשְׁלִ֥יךְ |
| 51 | 145 | Daniel Holman | 2025-03-19a | 41 | 1 | Zechariah 12:2 | meteg-removal | אֶת־יְרֽוּשָׁלַ֧͏ִם | אֶת־יְרוּשָׁלַ֧͏ִם |
| 52 | 145 | Daniel Holman | 2025-03-19a | 42 | 1 | Zechariah 13:2 | meteg-removal | הָֽעֲצַבִּים֙ | הָעֲצַבִּים֙ |
| 53 | 145 | Daniel Holman | 2025-03-19a | 43 | 1 | Zechariah 13:3 | meteg-removal | כִּֽי־יִנָּבֵ֣א | כִּי־יִנָּבֵ֣א |
| 54 | 145 | Daniel Holman | 2025-03-19a | 44 | 1 | Zechariah 14:10 | meteg-removal | יְרֽוּשָׁלָ֑͏ִם | יְרוּשָׁלָ֑͏ִם |
| 55 | 145 | Daniel Holman | 2025-03-19a | 45 | 1 | Malachi 1:2 | meteg-removal | וַֽאֲמַרְתֶּ֖ם | וַאֲמַרְתֶּ֖ם |
| 56 | 145 | Daniel Holman | 2025-03-19a | 46 | 1 | Malachi 1:7 | meteg-removal | וַֽאֲמַרְתֶּ֖ם | וַאֲמַרְתֶּ֖ם |
| 57 | 145 | Daniel Holman | 2025-03-19a | 47 | 1 | Malachi 1:8 | meteg-removal | וְכִֽי־תַגִּישׁ֨וּן | וְכִי־תַגִּישׁ֨וּן |
| 58 | 145 | Daniel Holman | 2025-03-19a | 49 | 1 | Malachi 2:6 | meteg-removal | לֹֽא־נִמְצָ֣א | לֹא־נִמְצָ֣א |
| 59 | 145 | Daniel Holman | 2025-03-19a | 51 | 1 | Malachi 2:11 | meteg-removal | בָּֽגְדָ֣ה | בָּגְדָ֣ה |
| 60 | 145 | Daniel Holman | 2025-03-19a | 52 | 1 | Malachi 3:4 | meteg-removal | וִירֽוּשָׁלָ֑͏ִם | וִירוּשָׁלָ֑͏ִם |
| 61 | 145 | Daniel Holman | 2025-03-19a | 53 | 1 | Malachi 3:7 | meteg-removal | אֲבֹֽתֵיכֶ֜ם | אֲבֹתֵיכֶ֜ם |
| 62 | 145 | Daniel Holman | 2025-03-19a | 54 | 1 | Malachi 3:8 | meteg-removal | קֹֽבְעִ֣ים | קֹבְעִ֣ים |

## Rows crediting outsiders that got no record

Of the 228 rows crediting outsiders, 200 got no record, and row 28, which credits no one, is
listed with them. A row dated before the logs is dated before 2024-12-17, MAM's state where the
earliest release begins. Release 2025-03-19b, which many reasons name, is Ben's release-wide
removal of one-argument deḥi and tsinnor stress-helper templates, which his row 109 records; its
565 entries change no text.

### Rows with reasons of their own

| Row | Date | Credit to | Where | Why no record |
| --- | --- | --- | --- | --- |
| 28 | 2026-08-07 | none | Psalms 132:11 | Credits no one: it thanks Nahum at Hebrew Wikisource for feedback that led to reverting the previous day's change, row 29's. |
| 29 | 2026-08-06 | anonymous contributor at Wikisource | Psalms 132:11 | Its move of a line divider was reverted the next day, as row 28 records, so release 2026-09-17 begins and ends with the divider in one place. The verse's one entry is 2025-03-19b's. |
| 79 | 2026-02-14 | anonymous Wikisource contributer | 1Samuel, 2Samuel, Isaiah: 5 verses | Its seder changes are in release 2026-03-16's span, in its verses' template rather than their text, which is all the change logs compare: none of its 5 verses has an entry. See "Changes the change logs do not show". |
| 101 | 2025-05-18 | Adrian Hills | Job 16:14 | Its change is in release 2026-03-06's span, but the change log has no entry for it; the verse's one entry is 2025-03-19b's. See "Changes the change logs do not show". |
| 178 | 2024-08-13 | Asael Reiter | Job 5:27 | Dated before the logs, and MAM's first stored state, 2024-12-17, already has its change. The verse's one entry is 2025-03-19b's. |
| 185 | 2024-06-29 | Daniel Holman | Ezekiel: 36 verses | Dated before the logs; none of its 36 verses has an entry. |
| 220 | 2024-01-29 | Daniel Holman | Jeremiah: 8 verses | Dated before the logs; none of its 8 verses has an entry. |
| 221 | 2024-01-29 | Daniel Holman | Jeremiah: 54 verses | Dated before the logs; none of its 54 verses has an entry. |
| 239 | 2024-01-16 | Daniel Holman | Isaiah: 16 verses | Dated before the logs; none of its 16 verses has an entry. |
| 241 | 2024-01-11 | Daniel Holman | Song of Songs: 1 verse | Dated before the logs; its one verse has no entry. |
| 242 | 2024-01-11 | Daniel Holman | Song of Songs: 4 verses | Dated before the logs; none of its 4 verses has an entry. |
| 243 | 2024-01-11 | Daniel Holman | Ruth: 3 verses | Dated before the logs; none of its 3 verses has an entry. |
| 244 | 2024-01-11 | Daniel Holman | Ruth: 8 verses | Dated before the logs; none of its 8 verses has an entry. |
| 245 | 2024-01-10 | Daniel Holman | Proverbs: 4 verses | Dated before the logs; all 4 of its verses have entries, all 2025-03-19b's. |
| 246 | 2024-01-10 | Daniel Holman | Proverbs: 16 verses | Dated before the logs; 1 of its 16 verses has an entry, 2025-03-19b's. |
| 247 | 2024-01-09 | Daniel Holman | Psalms 107:18 | Dated before the logs, and no stored state has its change: the maqaf it removed is there from 2024-12-17 on. The verse's one entry is 2025-03-19b's. |
| 248 | 2024-01-09 | Daniel Holman | Psalms: 17 verses | Dated before the logs; 3 of its 17 verses have entries, all 2025-03-19b's. |
| 249 | 2024-01-09 | Daniel Holman | Psalms: 70 verses | Ben's decision 4. Its one item whose change is in the logs, at Psalms 86:5 in 2026-03-16, is also Ben's own row 58's. Its other verses' entries are other changes. |
| 257 | 2023-12-31 | Daniel Holman | Job: 19 verses | Dated before the logs; 2 of its 19 verses have entries, all 2025-03-19b's. |
| 258 | 2023-12-30 | Daniel Holman | Job: 6 verses | Dated before the logs; 2 of its 6 verses have entries, all 2025-03-19b's. |
| 261 | 2023-12-28 | Daniel Holman | 1Chronicles, 2Chronicles: 32 verses | Dated before the logs. Its verses' one entry, at 1 Chronicles 21:12 in 2026-04-14, adds a narrow-sense paseq between two other atoms. |
| 262 | 2023-12-27 | Daniel Holman | 1Chronicles, 2Chronicles: 58 verses | Dated before the logs. Its verses' one entry, at 1 Chronicles 21:12 in 2026-04-14, adds a narrow-sense paseq between two other atoms. |
| 264 | 2023-12-18 | Daniel Holman | 1Kings, 2Kings: 92 verses | Ben's decision 5. Its 1 Kings 11:1 item's meteg deletion is in 2026-09-17, made in 2026 without a Sheet row; its 2 Kings 6:23 entry, row 13's, is on another atom. |
| 265 | 2023-12-18 | Daniel Holman | 1Kings, 2Kings: 13 verses | Dated before the logs. Its verses' one entry, at 2 Kings 22:1 in unpinned-latest, is another change in the item's atom: the meteg the item added is in both forms. |
| 271 | 2023-12-11 | Daniel Holman | 1Samuel, 2Samuel: 18 verses | Dated before the logs. Its verses' one entry, at 2 Samuel 24:10 in 2025-03-19a, is row 142's change, on another atom. |
| 273 | 2023-12-10 | Daniel Holman | 1Samuel, 2Samuel: 57 verses | Ben's decision 5. Its 2 Samuel 18:3 item's meteg deletion is in 2026-09-17, made in 2026 without a Sheet row; its verses' other entries are on other atoms. |
| 274 | 2023-12-09 | Daniel Holman | Judges: 5 verses | Dated before the logs; none of its 5 verses has an entry. |
| 275 | 2023-12-09 | Daniel Holman | Judges: 12 verses | Dated before the logs; none of its 12 verses has an entry. |
| 389 | 2023-03-26 | Daniel Holman | Deuter 32:30 | Dated before the logs. The verse's one entry, in 2026-03-16, deletes a meteg from another atom. |
| 406 | 2023-03-10 | Daniel Holman | Psalms 89:20 | Dated before the logs. The verse's one entry is 2025-03-19b's. |
| 422 | 2023-03-06 | Daniel Holman | Job 6:29 | Dated before the logs. The verse's one entry is 2025-03-19b's. |
| 426 | 2023-03-05 | Daniel Holman | Proverbs 23:31 | Dated before the logs. The verse's one entry, in 2026-03-16, deletes a meteg from another atom, as Ben's row 76 records. |
| 517 | 2023-01-22 | Bezalel Ariel | 2Chronicles: 2 verses | Dated before the logs; none of its 2 verses has an entry. |
| 599 | 2022-07-05 | Moshe Greenberg | Psalms 35:17 | Dated before the logs. The verse's one entry is 2025-03-19b's. |

### One-verse rows whose verse has no entry

No change log has an entry at the verse of any of these 167 rows, and each is dated before the
logs. One row names a verse that MAM lacks: row 191's *where* names Leviticus 24:44, and the
atoms it quotes are in 23:44, which has no entry either.

| Row | Date | Credit to | Verse |
| --- | --- | --- | --- |
| 175 | 2024-08-25 | Asael Reiter | Ezra 9:9 |
| 176 | 2024-08-25 | anonymous contributer at Hebrew Wikisource | 2Chronicles 25:17 |
| 177 | 2024-08-23 | anonymous contributer at Hebrew Wikisource | Ezekiel 27:15 |
| 182 | 2024-06-30 | Daniel Holman | Ezekiel 48:15 |
| 183 | 2024-06-30 | Daniel Holman | Ezekiel 34:2 |
| 184 | 2024-06-30 | Daniel Holman | Ezekiel 1:4 |
| 186 | 2024-06-29 | Daniel Holman | Ezekiel 21:37 |
| 191 | 2024-05-21 | anonymous contributor at Hebrew Wikisource | Levit 24:44, which MAM lacks |
| 202 | 2024-03-05 | Ephraim at Hebrew Wikisource | Proverbs 14:10 |
| 203 | 2024-03-05 | Ephraim at Hebrew Wikisource | Ezekiel 16:4 |
| 209 | 2024-02-09 | anonymous contributor at Hebrew Wikisource | Exodus 24:5 |
| 210 | 2024-02-08 | anonymous contributor at Hebrew Wikisource | Exodus 24:11 |
| 228 | 2024-01-27 | Daniel Holman | Jeremiah 37:16 |
| 230 | 2024-01-25 | Daniel Holman | Ezekiel 26:2 |
| 253 | 2024-01-03 | Daniel Holman | Psalms 74:13 |
| 254 | 2024-01-03 | Daniel Holman | Psalms 59:12 |
| 255 | 2023-12-31 | Daniel Holman | Job 31:2 |
| 256 | 2023-12-31 | Daniel Holman | Job 23:5 |
| 263 | 2023-12-27 | Daniel Holman | 1Chronicles 5:11 |
| 268 | 2023-12-11 | Daniel Holman | 2Samuel 13:15 |
| 269 | 2023-12-11 | Daniel Holman | 1Samuel 25:11 |
| 270 | 2023-12-11 | Daniel Holman | 1Samuel 7:11 |
| 276 | 2023-12-08 | Daniel Holman | Judges 18:21 |
| 277 | 2023-12-08 | Daniel Holman | Judges 16:5 |
| 278 | 2023-12-08 | Daniel Holman | Judges 10:11 |
| 280 | 2023-12-05 | Asael Reiter | 1Kings 20:28 |
| 281 | 2023-12-04 | Daniel Holman | Joshua 11:20 |
| 282 | 2023-12-04 | Daniel Holman | Joshua 11:4 |
| 283 | 2023-12-04 | Daniel Holman | Joshua 10:31 |
| 284 | 2023-12-04 | Daniel Holman | Joshua 10:29 |
| 285 | 2023-12-04 | Daniel Holman | Joshua 8:14 |
| 286 | 2023-12-04 | Daniel Holman | Joshua 11:12 |
| 287 | 2023-12-03 | Daniel Holman | Joshua 10:26 |
| 288 | 2023-12-03 | Daniel Holman | Joshua 2:15 |
| 290 | 2023-11-27 | Daniel Holman | Deuter 32:47 |
| 291 | 2023-11-27 | Daniel Holman | Daniel 2:17 |
| 292 | 2023-11-24 | Asael Reiter | 2Samuel 21:16 |
| 293 | 2023-11-23 | Daniel Holman | Deuter 28:49 |
| 294 | 2023-11-10 | Daniel Holman | Numbers 18:19 |
| 309 | 2023-10-26 | Daniel Holman | Levit 9:1 |
| 310 | 2023-10-26 | Daniel Holman | Numbers 31:32 |
| 311 | 2023-10-26 | Daniel Holman | Numbers 16:31 |
| 312 | 2023-10-26 | Daniel Holman | 2Kings 18:9 |
| 331 | 2023-10-03 | Daniel Holman | 2Chronicles 29:31 |
| 333 | 2023-09-11 | Asael Reiter | Joshua 10:15 |
| 349 | 2023-08-13 | Asael Reiter | Proverbs 24:31 |
| 350 | 2023-08-13 | Asael Reiter | Psalms 80:11 |
| 351 | 2023-08-13 | Asael Reiter | Psalms 72:20 |
| 353 | 2023-07-24 | anonymous contributor at Hebrew Wikisource | Job 17:4 |
| 354 | 2023-07-24 | anonymous contributor at Hebrew Wikisource | Job 6:20 |
| 359 | 2023-06-15 | Daniel Holman | Joshua 14:10 |
| 360 | 2023-06-12 | Daniel Holman | Proverbs 25:11 |
| 365 | 2023-06-05 | Ittai Yehudah | Joshua 1:4 |
| 373 | 2023-04-07 | Daniel Holman | Daniel 8:25 |
| 374 | 2023-04-07 | Daniel Holman | Daniel 8:7 |
| 375 | 2023-04-07 | Daniel Holman | Nehemiah 2:20 |
| 376 | 2023-04-07 | Daniel Holman | Nehemiah 5:14 |
| 383 | 2023-03-26 | Daniel Holman | Deuter 28:56 |
| 384 | 2023-03-26 | Daniel Holman | Deuter 28:62 |
| 385 | 2023-03-26 | Daniel Holman | Deuter 29:17 |
| 386 | 2023-03-26 | Daniel Holman | Deuter 31:19 |
| 387 | 2023-03-26 | Daniel Holman | Deuter 31:19 |
| 388 | 2023-03-26 | Daniel Holman | Deuter 32:21 |
| 390 | 2023-03-26 | Daniel Holman | Deuter 33:10 |
| 392 | 2023-03-25 | Daniel Holman | Psalms 53:6 |
| 393 | 2023-03-20 | Daniel Holman | Psalms 78:32 |
| 398 | 2023-03-15 | Moshe Greenberg | Micah 2:12 |
| 401 | 2023-03-12 | Daniel Holman | Psalms 138:3 |
| 405 | 2023-03-10 | Daniel Holman | Psalms 108:3 |
| 407 | 2023-03-10 | Daniel Holman | Psalms 88:4 |
| 408 | 2023-03-10 | Daniel Holman | Psalms 78:71 |
| 409 | 2023-03-10 | Daniel Holman | Psalms 57:9 |
| 418 | 2023-03-06 | Daniel Holman | Job 42:10 |
| 420 | 2023-03-06 | Daniel Holman | Job 29:16 |
| 421 | 2023-03-06 | Daniel Holman | Job 20:8 |
| 423 | 2023-03-05 | anonymous contributor at Wikisource | Numbers 3:6 |
| 424 | 2023-03-05 | Daniel Holman | Proverbs 31:6 |
| 425 | 2023-03-05 | Daniel Holman | Proverbs 22:20 |
| 428 | 2023-03-05 | Daniel Holman | Exodus 12:28 |
| 429 | 2023-03-05 | Daniel Holman | Genesis 5:21 |
| 435 | 2023-02-27 | Moshe Greenberg | Psalms 5:8 |
| 436 | 2023-02-26 | anonymous contributor at Wikisource | Esther 1:5 |
| 452 | 2023-02-21 | Moshe Greenberg | Isaiah 30:32 |
| 453 | 2023-02-19 | anonymous contributor at Wikisource | Isaiah 23:17 |
| 456 | 2023-02-19 | Daniel Holman | Ezekiel 44:24 |
| 457 | 2023-02-19 | Daniel Holman | Ezekiel 33:8 |
| 458 | 2023-02-19 | Daniel Holman | Ezekiel 18:21 |
| 459 | 2023-02-19 | Daniel Holman | Ezekiel 18:2 |
| 460 | 2023-02-19 | Daniel Holman | Ezekiel 11:1 |
| 461 | 2023-02-17 | Daniel Holman | Jeremiah 48:28 |
| 462 | 2023-02-17 | Daniel Holman | Jeremiah 48:7 |
| 463 | 2023-02-17 | Daniel Holman | Jeremiah 48:6 |
| 464 | 2023-02-17 | Daniel Holman | Jeremiah 36:29 |
| 465 | 2023-02-17 | Daniel Holman | Jeremiah 34:3 |
| 466 | 2023-02-17 | Daniel Holman | Jeremiah 18:16 |
| 467 | 2023-02-17 | Daniel Holman | Jeremiah 13:13 |
| 468 | 2023-02-16 | Daniel Holman | Jeremiah 4:19 |
| 469 | 2023-02-16 | Daniel Holman | 2Chronicles 27:7 |
| 470 | 2023-02-16 | Daniel Holman | Micah 4:8 |
| 471 | 2023-02-16 | Daniel Holman | 2Samuel 19:41 |
| 472 | 2023-02-16 | Daniel Holman | 2Samuel 19:33 |
| 473 | 2023-02-16 | Daniel Holman | 2Samuel 15:26 |
| 474 | 2023-02-16 | Daniel Holman | 1Samuel 3:13 |
| 475 | 2023-02-16 | Daniel Holman | Judges 21:3 |
| 476 | 2023-02-15 | Daniel Holman | Deuter 33:29 |
| 477 | 2023-02-13 | Bezalel Ariel | Proverbs 6:27 |
| 478 | 2023-02-12 | Moshe Greenberg | Psalms 86:9 |
| 490 | 2023-02-07 | Daniel Holman | Ezekiel 23:36 |
| 497 | 2023-02-05 | Asael Reiter | Jeremiah 9:11 |
| 499 | 2023-02-05 | Moshe Greenberg | Psalms 72:17 |
| 502 | 2023-01-31 | anonymous contributor at Wikisource | 2Kings 12:22 |
| 503 | 2023-01-31 | anonymous contributor at Wikisource | 2Kings 17:4 |
| 520 | 2023-01-10 | Asael Reiter | Isaiah 25:10 |
| 521 | 2023-01-05 | anonymous reader at alhatorah.org | 2Kings 9:20 |
| 522 | 2023-01-05 | anonymous contributor at Hebrew Wikisource | 1Kings 8:36 |
| 526 | 2022-12-15 | anonymous reader at mg.alhatorah.org | Genesis 38:17 |
| 527 | 2022-12-14 | Moshe Greenberg | Daniel 2:31 |
| 528 | 2022-12-14 | Moshe Greenberg | Daniel 2:20 |
| 529 | 2022-12-13 | Moshe Greenberg | Ezra 9:4 |
| 531 | 2022-12-07 | Moshe Greenberg | Daniel 6:28 |
| 532 | 2022-12-07 | Moshe Greenberg | 1Samuel 18:19 |
| 533 | 2022-12-07 | Moshe Greenberg | Hosea 13:14 |
| 534 | 2022-11-20 | Daniel Holman | 2Kings 23:12 |
| 535 | 2022-11-20 | Daniel Holman | 2Kings 19:6 |
| 536 | 2022-11-20 | Daniel Holman | 2Kings 1:2 |
| 539 | 2022-10-26 | Asael Reiter | Joshua 17:2 |
| 540 | 2022-10-24 | Asael Reiter | Joshua 8:2 |
| 561 | 2022-10-04 | Daniel Holman | 1Samuel 30:15 |
| 562 | 2022-09-07 | Moshe Greenberg | Daniel 4:27 |
| 563 | 2022-08-29 | David Kochav | Isaiah 54:1 |
| 564 | 2022-08-28 | David Kochav | Isaiah 51:15 |
| 565 | 2022-08-23 | Moshe Greenberg | Job 39:2 |
| 566 | 2022-08-22 | Moshe Greenberg | 1Chronicles 22:4 |
| 567 | 2022-08-22 | Moshe Greenberg | Proverbs 31:27 |
| 568 | 2022-08-22 | Moshe Greenberg | Proverbs 6:35 |
| 569 | 2022-08-22 | Moshe Greenberg | Ezekiel 32:30 |
| 570 | 2022-08-22 | Moshe Greenberg | Ezekiel 27:36 |
| 571 | 2022-08-22 | Moshe Greenberg | Ezekiel 11:9 |
| 572 | 2022-08-17 | anonymous editor at Wikisource | 1Chronicles 6:39 |
| 574 | 2022-08-16 | Moshe Greenberg | Isaiah 43:19 |
| 575 | 2022-08-16 | Moshe Greenberg | 2Kings 25:7 |
| 576 | 2022-08-16 | Moshe Greenberg | 2Kings 13:17 |
| 577 | 2022-08-16 | Moshe Greenberg | 2Kings 6:8 |
| 578 | 2022-08-16 | Moshe Greenberg | 1Samuel 4:19 |
| 579 | 2022-08-16 | Moshe Greenberg | 1Kings 20:25 |
| 580 | 2022-08-16 | Moshe Greenberg | 1Kings 10:3 |
| 581 | 2022-08-16 | Moshe Greenberg | 2Samuel 24:13 |
| 582 | 2022-08-16 | Moshe Greenberg | 2Samuel 24:7 |
| 583 | 2022-08-14 | Moshe Greenberg | 2Samuel 21:1 |
| 584 | 2022-08-14 | Moshe Greenberg | Judges 16:18 |
| 585 | 2022-08-02 | Asael Reiter | Psalms 44:19 |
| 586 | 2022-07-29 | Asael Reiter | Daniel 5:20 |
| 587 | 2022-07-24 | Moshe Greenberg | Psalms 61:9 |
| 588 | 2022-07-24 | Moshe Greenberg | Psalms 137:9 |
| 589 | 2022-07-24 | Moshe Greenberg | Psalms 83:11 |
| 590 | 2022-07-24 | Moshe Greenberg | Psalms 119:170 |
| 591 | 2022-07-24 | Moshe Greenberg | Psalms 92:10 |
| 592 | 2022-07-20 | Moshe Greenberg | Psalms 89:53 |
| 593 | 2022-07-18 | Moshe Greenberg | Psalms 81:6 |
| 594 | 2022-07-13 | Moshe Greenberg | Isaiah 34:11 |
| 595 | 2022-07-13 | Moshe Greenberg | Ezekiel 23:42 |
| 596 | 2022-07-13 | Moshe Greenberg | Psalms 68:18 |
| 597 | 2022-07-10 | Moshe Greenberg | Psalms 58:7 |
| 598 | 2022-07-09 | Moshe Greenberg | Psalms 51:16 |
| 600 | 2022-07-05 | Moshe Greenberg | Psalms 10:7 |
| 601 | 2022-07-03 | anonymous editor at Wikisource | Job 9:10 |
| 796 | 2021-11-22 | Michael Escott | 1Kings 8:11 |
