# Proverbs 30:19: the example precedes MAM’s maqaf change

The Introduction’s example matched MAM’s spaced main form when it was added.
The chapter later changed to maqaf. The older example remains in the audit’s
Introduction snapshot. This establishes staleness of the example relative to
MAM’s later main form. Ben approved the correction on 2026-10-15 at 16:11 UTC;
the proposal remains unsubmitted and unapplied.

| Event | Dated revision evidence (UTC) |
| --- | --- |
| Linked MAM draft has the spaced main form | [486384](https://he.wikisource.org/w/index.php?oldid=486384), 2013-05-27 06:07:40, the latest draft revision before the example was added |
| Example added to the original, unsplit Introduction | [486388 → 486389](https://he.wikisource.org/w/index.php?diff=486389&oldid=486388), 2013-05-27 06:39:35 |
| Example copied into the new chapter 2 | [487519](https://he.wikisource.org/w/index.php?oldid=487519), 2013-06-05 05:19:24 |
| Chapter still has the spaced main form | [904820](https://he.wikisource.org/w/index.php?oldid=904820), 2019-06-13 12:03:30 |
| Chapter main form changes to maqaf | [904820 → 997545](https://he.wikisource.org/w/index.php?diff=997545&oldid=904820), 2020-11-08 05:24:42 |
| Introduction still has the old example | [997158](https://he.wikisource.org/w/index.php?oldid=997158), 2020-11-06 11:11:55, and [997664](https://he.wikisource.org/w/index.php?oldid=997664), 2020-11-08 13:25:10 |

The Introduction’s inserted main form is **עֲלֵ֫י צ֥וּר**. Its own note already
gives Aleppo’s **עֲלֵ֫י־צ֥וּר**. The 2020 chapter edit promotes the latter to the
main form and explicitly assigns the spaced form to printed editions.
The edit summary says:

> מקף בשתי תיבות של עולה ויורד כמו בכתר ארם צובה (בשני פסוקים)

It describes adding maqaf in two-word oleh–veyored groups following Aleppo,
in two verses. The history therefore explains the space as MAM’s older choice;
the current printed-edition attribution alone had not established why the old
example used that form.

## Predecessor, moves and templates

The 2013 example is an addition in an adjacent revision diff, not merely a form
found in the oldest available chapter-2 snapshot. In revision 486388 the four-unit
paragraph has an empty example slot; revision 486389 inserts the Proverbs example
and links to the earlier user draft. Earlier neighboring examples used section
transclusion, but this inserted Proverbs example contains its own literal verse.

The original page was then under Dovi’s user namespace. Its history records the
2012 Torah-to-MAM title change and the [2025 move to the Wikisource Introduction
namespace](https://he.wikisource.org/w/index.php?oldid=2897779). Chapter 2’s
[corresponding move](https://he.wikisource.org/w/index.php?oldid=2897787) preserves
its page history. The 2013 split copies the example into chapter 2; the parent
page subsequently links to the new chapter rather than supplying its verse.

The linked draft’s 22/22 visible revisions were read: its first revision has a
different chapter, and the remaining 21 have the spaced main form, including its
final historical-page version. All 41/41 visible chapter-page revisions were read:
four have the spaced main form, beginning in 2011, and 37 have maqaf beginning
with revision 997545. Thus an Aleppo maqaf in the earlier note is not confused
with maqaf in the selected main text.

The note template’s historical definitions at [435533](https://he.wikisource.org/w/index.php?oldid=435533)
and [985698](https://he.wikisource.org/w/index.php?oldid=985698) both display only
their first argument. The main form is therefore identified from the template
argument, not from an arbitrary occurrence of the word pair in its notes.

## Evidence and limits

[Source captures](proverbs-30-19-history-sources.json) retain exact historical
excerpts, revision metadata, the two change diffs and the move records.
[Machine-readable result](proverbs-30-19-history.json) records the classification
and coverage. Full raw API responses remain in the local research cache;
`py/intro_doc_audit/revision_history.py` supplies bounded read-only metadata/content
queries and the existing wikitext parser for main-argument extraction.

Root metadata accounts for 860 visible revisions and chapter-2 metadata for 1,423.
Only selected content snapshots from these large histories were read. The actual
adjacent insertion and chapter-change diffs prove the sequence; adaptive snapshots
do not prove that no earlier, removed or unidentified draft ever contained a
similar example. No claim of continuous unchanged Introduction text is made for
every intervening revision. Suppressed/deleted history was not assessed.

The audit’s original base commit and cached source revisions remain unchanged:
`89cb865729b0876f1fd32a8a3579eaec80b4fc0c`, Introduction chapter 2 revision
3087893 and Proverbs 30 revision 3008043. This is supplemental read-only live
history research authorized by `Sentinel_daff81a9d8e0819182ae17f268dd2f41`.
No wiki edit, source-cache refresh, issue, submission or main integration occurred.

## Ben’s approval

Ben approved replacing the space with maqaf in the Introduction’s layout example
on 2026-10-15 at 16:11 UTC
(`Sentinel_a0613408f38c8191804afc8c85a5733c`), based on the stale-example chronology.
The case is settled and appears in Reviewed. The exact proposal is retained in
[adjudications.json](adjudications.json):

> עֲלֵ֫י צ֥וּר → עֲלֵ֫י־צ֥וּר

Only the one boundary changes in the full proposed example. The separate Aleppo
quotation and all historical source evidence are preserved. This approval records
a proposal; no wiki edit or submission to Avi has occurred.

## Submitted to Avi

On 2026-10-17 at 20:20 UTC Ben asked for an issue for each correction he had approved in this review: “Sure, go ahead and file those 12 issues”. #323 proposes this correction to Avi; it is not applied.

## The example's note template, 2026-10-18

At Ben's request a bot edit gave every `{{נוסח}}` call in the Introduction the
form MAM's chapter pages use, with the note as parameter 2 written `2=`. In this
example it changed only that ([chapter 2 revision 3090585](https://he.wikisource.org/w/index.php?diff=3090585&oldid=3087893)). The
proposal's full example in [adjudications.json](adjudications.json) now has `2=`
too, and #323's before and after show it.
