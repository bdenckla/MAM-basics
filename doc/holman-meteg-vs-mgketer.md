# Notes: the 30 meteg suggestions M1–M33 lined up against the mgketer comparison reports

Evidence for the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md). Its table of
30 records is the target set of that programme's items 2, 3 and 6, and the by-type totals at the
foot are what its item 7 re-reads after the mgketer refresh.

Captured 2026-09-03 in a plan-mode session of MAM-basics (`C:/Users/BenDe/GitRepos/MAM-basics`,
HEAD `3829585`, clean tree), one of a set of six notes; the two beside it here are
[`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md) and
[`holman-meteg-m23-isaiah-23-12.md`](holman-meteg-m23-isaiah-23-12.md). All six were written
under `C:/Users/BenDe/.claude/plans/` because concurrent work in git-tracked areas had not
concluded, and were moved into `doc/` on 2026-09-03.

Sources compared, both read-only:

- **A.** The `M` records of `C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/holman/table_data_findings.html`
  (this path moved out of the now-retired `holman-ketiv-qere` repo during this session, in a
  concurrent session — see the path note in
  [`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md)),
  article ids `mam001`–`mam033`. **Three ids do not exist**, `mam017`, `mam024` and `mam032`,
  so the 30 records are M1–M16, M18–M23, M25–M31 and M33, every one with the badge "meteg".
- **B.** `C:/Users/BenDe/GitRepos/MAM-private/mgketer/out-reports/`, whose records are
  `diff-card` divs carrying a `ref-text`, a category badge, a `diff-hash` of the form
  `1K7:24#8701a1ff`, a `subcat-text` such as "MAM adds meteg on tsadi", an optional massaging
  tooltip, and a `mam-side` and `mgk-side` with the differing letter marked. Each record is in
  its book's `by-book/<book>/diffs.html` and in one `by-type/*.html`.

Two facts about the hash worth knowing before searching: **it is content-addressed, not
verse-addressed**, so the same 8 hex digits recur wherever the same diff recurs (`47bf0ab0` is
1K12:18, 2S12:31, 2S15:37 and Je17:21; `5db01408` is 1K15:5 and 2S11:3; `65ca7700` is Ju1:7 and
2K21:12), and only the full `Book Ch:V#hash` is unique. The book abbreviations are `1K`, `2K`,
`1S`, `2S`, `Ju`, `Js`, `I` for Isaiah (not `Isa`), `Je`, `1C`, `2C`, `Ps`, `Jb`, `Pr`, `Ee`,
`D`, `R`, `Er`, `G`, `N`, `Ts`, `Zc`, `Mi`, `Na`, `Ma`.

## Result: all 30 have a matching mgketer record, and no reading disagrees

| count | of what |
|---|---|
| 30 of 30 | M records with a mgketer record for the same atom |
| 29 | in `by-type/mam-adds-meteg.html` (which holds 67 diffs Tanakh-wide) |
| 1 (M23) | in `by-type/mgketer-adds-meteg.html` (which holds 5 Tanakh-wide) |
| 0 | in `meteg-moved`, `misc-pointing`, `misc`, `parashah`, `structural`, `xaser-malei` |
| 0 | in any `suppressed.html` or `surprises.html` |

In every case mgketer's `mam-side` equals Holman's MAM form and mgketer's `mgk-side` equals
Holman's Aleppo form, character for character, apart from the two display artifacts noted
under M13 and M18 below. So Holman's page and the mgketer comparison are two routes to the same
30 differences, and neither reports an Aleppo reading the other contradicts.

Ben's example, M1 = `1K7:24#8701a1ff`, is confirmed and is the pattern for all 29 "MAM adds
meteg" cases.

| M | verse.atom | MAM | Aleppo per Holman | Holman's note | mgketer record | mgketer's subcat |
|---|---|---|---|---|---|---|
| M1 | 1Kings 7:24.17 | בִּיצֻֽקָתֽוֹ׃ | בִּיצֻקָתֽוֹ׃ | no Meteg under Tzadi | `1K7:24#8701a1ff` | MAM adds meteg on tsadi |
| M2 | 1Kings 11:1.13 | צֵֽדְנִיֹּ֖ת | צֵדְנִיֹּ֖ת | no Meteg under Tzadi | `1K11:1#89ecc089` | MAM adds meteg on tsadi |
| M3 | 1Kings 12:18.21 | יְרֽוּשָׁלָֽ͏ִם׃ | יְרוּשָׁלָֽ͏ִם׃ | no Meteg under Resh | `1K12:18#47bf0ab0` | MAM adds meteg on resh |
| M4 | 1Kings 15:5.19 | הַֽחִתִּֽי׃ | הַחִתִּֽי׃ | no Meteg under Hey | `1K15:5#5db01408` | MAM adds meteg on he |
| M5 | 1Kings 15:19.23 | מֵֽעָלָֽי׃ | מֵעָלָֽי׃ | no Meteg under Mem | `1K15:19#cafc8dde` | MAM adds meteg on mem |
| M6 | 1Kings 17:16.14 | אֵֽלִיָּֽהוּ׃ | אֵלִיָּֽהוּ׃ | no Meteg under Alef | `1K17:16#8fc59827` | MAM adds meteg on alef |
| M7 | 1Kings 18:1.20 | הָֽאֲדָמָֽה׃ | הָאֲדָמָֽה׃ | no Meteg under Hey | `1K18:1#09622a75` | MAM adds meteg on 1st he |
| M8 | 1Kings 22:7.6 | לַֽיהֹוָ֖ה | לַיהֹוָ֖ה | no Meteg under Lamed | `1K22:7#1401a557` | MAM adds meteg on lamed |
| M9 | 1Samuel 18:9.6 | מֵֽהַיּ֥וֹם | מֵהַיּ֥וֹם | no Meteg under Mem | `1S18:9#489fce9c` | MAM adds meteg on mem |
| M10 | 1Samuel 27:3.15 | וַֽאֲבִיגַ֥יִל | וַאֲבִיגַ֥יִל | no Meteg under Vav | `1S27:3#672abe3f` | MAM adds meteg on vav |
| M11 | 2Chronicles 6:27.17 | וְנָֽתַתָּ֤ה | וְנָתַתָּ֤ה | no Meteg under Nun | `2C6:27#bd6775e1` | MAM adds meteg on nun |
| M12 | 2Chronicles 6:28.9 | וְיֵֽרָק֜וֹן | וְיֵרָק֜וֹן | no Meteg under Yod | `2C6:28#cdca1a8e` | MAM adds meteg on yod |
| M13 | 2Chronicles 18:33.21 | הׇֽחֳלֵֽיתִי׃ | הׇחֳלֵֽיתִי׃ | no Meteg under Hey | `2C18:33#8e58aa4c` | MAM adds meteg on he |
| M14 | 2Chronicles 24:25.13 | יְהֽוֹיָדָ֣ע | יְהוֹיָדָ֣ע | no Meteg under Hey | `2C24:25#afdff6fe` | MAM adds meteg on he |
| M15 | 2Chronicles 32:7.18 | מֵֽעִמּֽוֹ׃ | מֵעִמּֽוֹ׃ | no Meteg under first Mem | `2C32:7#10b8f3ac` | MAM adds meteg on 1st mem |
| M16 | 2Kings 7:12.19 | וַיֵּֽצְא֤וּ | וַיֵּצְא֤וּ | no Meteg under Yod | `2K7:12#e4463df0` | MAM adds meteg on yod |
| M18 | 2Kings 21:12.11 | עַל־יְרֽוּשָׁלַ֖͏ִם | עַל־יְרוּשָׁלַ֖͏ִם | no Meteg under Resh | `2K21:12#65ca7700` | MAM adds meteg on resh |
| M19 | 2Samuel 11:3.14 | הַֽחִתִּֽי׃ | הַחִתִּֽי׃ | no Meteg under Hey | `2S11:3#5db01408` | MAM adds meteg on he |
| M20 | 2Samuel 12:31.25 | יְרֽוּשָׁלָֽ͏ִם׃ | יְרוּשָׁלָֽ͏ִם׃ | no Meteg under Resh | `2S12:31#47bf0ab0` | MAM adds meteg on resh |
| M21 | 2Samuel 15:37.8 | יְרֽוּשָׁלָֽ͏ִם׃ | יְרוּשָׁלָֽ͏ִם׃ | no Meteg under Resh | `2S15:37#47bf0ab0` | MAM adds meteg on resh |
| M22 | 2Samuel 18:3.9 | לֹֽא־יָשִׂ֧ימוּ | לֹא־יָשִׂ֧ימוּ | no Meteg under Lamed | `2S18:3#df68039b` | MAM adds meteg on lamed |
| M23 | Isaiah 23:12.11 | ק֣וּמִי | ק֣וּמִֽי | Aleppo HAS a Meteg under Mem | `I23:12#e5e7ccd9` | mgketer adds meteg on mem |
| M25 | Judges 1:7.21 | יְרֽוּשָׁלַ֖͏ִם | יְרוּשָׁלַ֖͏ִם | no Meteg under Resh | `Ju1:7#65ca7700` | MAM adds meteg on resh |
| M26 | Judges 1:32.9 | הֽוֹרִישֽׁוֹ׃ | הוֹרִישֽׁוֹ׃ | no Meteg under Hey | `Ju1:32#0c7fe116` | MAM adds meteg on he |
| M27 | Judges 5:6.7 | חָֽדְל֖וּ | חָדְל֖וּ | no Meteg under Chet | `Ju5:6#07a4411d` | MAM adds meteg on het |
| M28 | Judges 5:11.13 | יָֽרְד֥וּ | יָרְד֥וּ | no Meteg under Yod | `Ju5:11#c33f86f3` | MAM adds meteg on yod |
| M29 | Judges 6:1.2 | בְנֵֽי־יִשְׂרָאֵ֛ל | בְנֵי־יִשְׂרָאֵ֛ל | no Meteg under Nun | `Ju6:1#9abe09f1` | MAM adds meteg on nun |
| M30 | Judges 6:4.1 | וַיַּֽחֲנ֣וּ | וַיַּחֲנ֣וּ | no Meteg under Yod | `Ju6:4#fafbb459` | MAM adds meteg on yod |
| M31 | Judges 6:5.4 | יַֽעֲל֜וּ | יַעֲל֜וּ | no Meteg under Yod | `Ju6:5#24c3e32f` | MAM adds meteg on yod |
| M33 | Judges 21:16.3 | הָֽעֵדָ֔ה | הָעֵדָ֔ה | no Meteg under Hey | `Ju21:16#00d8d510` | MAM adds meteg on 1st he |

Every Holman note in the "MAM adds meteg" 29 reads "Aleppo has no Meteg under X", except M33's,
which reads "Aleppo no Meteg under Hey" with the verb missing, near line 8146 of the findings
page. That is a typo on Holman's page, not a different claim.

## Aside from Ben: five of these verse-final atoms lack the sof pasuq in the Aleppo Codex, and MAM will not follow that

Ben's observation, 2026-09-03, recorded here as an aside and not verified in this session: in
the Aleppo Codex, the atom of each of these five records lacks the expected sof pasuq mark (׃).
**There are no plans to reflect that lack in MAM.** The five, all verse-final:

1. M1, 1 Kings 7:24, בִּיצֻֽקָתֽוֹ׃
2. M4, 1 Kings 15:5, הַֽחִתִּֽי׃
3. M5, 1 Kings 15:19, מֵֽעָלָֽי׃
4. M20, 2 Samuel 12:31, יְרֽוּשָׁלָֽ͏ִם׃
5. M26, Judges 1:32, הֽוֹרִישֽׁוֹ׃

Neither Holman's page nor the mgketer reports record the missing sof pasuq: Holman's Aleppo
column has ׃ on all five, and mgketer's `mgk-side` has it too, so mgketer's transcription of
the Aleppo Codex supplies the mark. The aside is therefore a statement about the manuscript that
no transcription consulted here makes, which is exactly why it is worth writing down beside the
suggestion rather than leaving it to be rediscovered from the images. Where a meteg suggestion
among the five is implemented, the sof pasuq stays.

## Aside from Ben: in M10 the spot where a meteg would go is occupied by a lamed ascender from the line below, and M27 and M33 are milder cases of the same

Ben's observation, 2026-09-03, recorded as an aside and not verified in this session against
the images:

1. **M10, 1 Samuel 27:3, וַֽאֲבִיגַ֥יִל.** Placing a meteg under the vav in question would be
   slightly challenging in the Aleppo Codex, because the ascender of a lamed on the line below
   intrudes into the space beneath that vav. Ben's reading of it: the naqdan would have found
   a way to place the meteg had he wanted one, and there are cases where the naqdan did find
   such a way around an intruding ascender. **Where those cases are is an open question Ben
   raised in the same breath ("where?") and this note does not answer it**; nobody has yet
   collected them. So Ben has no reason to believe the naqdan was dissuaded from a meteg here
   by the lamed ascender. The M10 card now names the encroachment so a reader can read the image
   with that context; the card does not answer the open question about other cases. The aside is
   worth having only because the first place the eye goes to look for such a meteg is occupied.
2. **M27, Judges 5:6, חָֽדְל֖וּ, and M33, Judges 21:16, הָֽעֵדָ֔ה.** A similar situation, less
   severe: something from the neighbouring line encroaches on the space where the meteg would
   go, but more room for a meteg is present than in M10. The M27 and M33 cards now name that
   smaller encroachment and link to M10 for the fuller image-reading note.

None of this changes the three records' disposition. Holman's page and mgketer both record no
meteg in the Aleppo Codex at all three atoms, and the aside says only why the image is harder
to read at those spots than at the other 27.

## Two records whose mgketer card needs a footnote

1. **M13, `2C18:33#8e58aa4c`, has a display artifact and no disagreement.** Holman writes both
   forms with U+05C7 qamats qatan on the he; mgketer's original MAM string is the same, and the
   card carries the tooltip "MAM: M4: qamats qatan → qamats" and displays the massaged form with
   U+05B8. The meteg claim agrees. (The M13 note,
   [`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md), is about
   the `מ:קמץ` template this same atom sits in.)
2. **M22, 2 Samuel 18:3, is one of two look-alike compounds in one verse, filed in opposite
   categories.** The verse has לא־ישימו twice. `2S18:3#df68039b` (`by-book/BB-2Samuel/diffs.html`
   near line 212) is Holman's M22: MAM לֹֽא־יָשִׂ֧ימוּ, mgketer לֹא־יָשִׂ֧ימוּ, "MAM adds meteg on
   lamed", atom 9 with a darga. `2S18:3#d300caba` (near line 232, and in
   `by-type/mgketer-adds-meteg.html`) is the other compound: MAM לֹא־יָשִׂ֤ימוּ, mgketer
   לֹֽא־יָשִׂ֤ימוּ, "mgketer adds meteg on lamed", with a mahpakh, and **no Holman record covers
   it**. Only the accent tells the two apart, so anything matching on letters alone will
   conflate them.

## mgketer records with no Holman counterpart, noticed in passing

- `2K21:12#0ebb56b0`, וִֽיהוּדָ֑ה, "MAM adds meteg on 1st vav", in the same verse as M18.
- `2S18:3#d300caba`, above.
- The other 38 of `mam-adds-meteg.html`'s 67 and the other 4 of `mgketer-adds-meteg.html`'s 5
  were not examined one by one.

## How to re-establish

- Count the M records: search the findings page for `id="mam0`; 30 hits, ids 001–033 less
  017, 024, 032.
- For any M record, search `out-reports/by-book/<book>/diffs.html` for its `ref-text` verse
  (mgketer spells 2 Kings as `2Kgs`, for example) and match the `mam-side` against Holman's MAM
  form; the card's `diff-hash` is the record id used above.
- The by-type totals: count `diff-card` in `by-type/mam-adds-meteg.html` (67) and
  `by-type/mgketer-adds-meteg.html` (5), at MAM-private's state on 2026-09-03.

## Status, 2026-09-04: the refresh has happened and these totals are now HISTORICAL

**Every figure above is pre-refresh.** Item 7 of
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md)
ran `py/main_diff.py --all` on mgketer on 2026-09-04, after items 3 and 5 had put
the thirty suggestions into MAM. Counted as diff cards on the pages themselves:
`mam-adds-meteg.html` fell from **67 to 37** and `mgketer-adds-meteg.html` from
**5 to 4**, "Meteg moved" stayed at 5, and a new `by-type/accent.html` arrived
holding one card, Zechariah 2:4, which is M34. The non-common total therefore
went from 281 to 251.

**The section above headed "mgketer records with no Holman counterpart, noticed
in passing" predicted the shape of the drop, and it was right.** Thirty cards
left `mam-adds-meteg.html` where twenty-nine records asked for it, because
2 Kings 21:12 shed two: M18's meteg on the resh, and `2K21:12#0ebb56b0`,
וִֽיהוּדָ֑ה, the one this note had already noticed as covered by no Holman record.

**One expectation of the larger programme did NOT hold, and it is worth knowing
before re-establishing anything here.** Joshua 10:12 shows no mgketer diff,
before the refresh or after: mgketer's `py/python_modules/strip_stress_helpers.py`
strips stress helpers by design, so M24's doubled pashta cannot produce one.
